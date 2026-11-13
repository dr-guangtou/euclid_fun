"""Stage 0: preflight. Snapshot bubbletea inputs, verify the selector and the services, choose the control field.

Usage: uv run python -m ucd.stages.stage_0_preflight
Products: reference/ (snapshot + manifest), stage_0_preflight/tables/fields.json, figures/field_map.png, summary.json
"""

import io
import json
import shutil
import subprocess
import time

import astropy.units as u
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
from astropy.coordinates import SkyCoord
from astropy.io import ascii as astropy_ascii
from mocpy import MOC
from PIL import Image

from ucd.lib import euclid_catalogue, gaia_access, qa_plots, run_state, selector

stage_name = "stage_0_preflight"
snapshot_files = {
    "repository": [
        "data/literature/validation/point_source_logistic_model_v1.json",
        "data/literature/validation/point_source_logistic_model_v1.joblib",
        "data/literature/sources/point_source_logistic_policy_v1.json",
        "data/literature/validation/canonical_reference_catalog.csv",
        "data/literature/catalogs/host_association_register_v1.csv",
        "data/literature/catalogs/canonical_gaia_dr3_crossmatch.csv",
        "data/literature/catalogs/canonical_legacy_survey_dr10_crossmatch.csv",
        "data/literature/validation/saifollahi_reference_roles.csv",
        "data/literature/validation/saifollahi_selection_pool.csv",
        "data/literature/catalogs/ucd_visual_review_gaia_neighbors_v1.csv",
        "data/results/background/large_sky_development_scale_summary_v1.csv",
        "data/results/background/large_sky_field_grid_v1.csv",
        "data/galaxy_sample/galaxy_sample_ranked.csv",
        "reference/saifollahi2021/tablea1.dat",
        "reference/saifollahi2021/tablea5.dat",
        "reference/saifollahi2021/tablea6.dat",
        "reference/saifollahi2021/ReadMe.txt",
        "reference/liu2020/table4.dat",
        "reference/liu2020/ReadMe.txt",
        "reference/fahrion2019/tableb1.dat",
        "reference/fahrion2019/ReadMe.txt",
    ],
    "external_data": ["m60_positive_control_v1/scored_sources.csv"],
}


def snapshot_bubbletea(config: dict) -> dict:
    """Copy the needed bubbletea files once; record hashes and the bubbletea commit."""
    reference = run_state.reference_dir(config)
    repository = run_state.expand(config["bubbletea"]["repository"])
    external = run_state.expand(config["bubbletea"]["external_data"])
    commit = subprocess.run(
        ["git", "-C", str(repository), "rev-parse", "HEAD"], capture_output=True, text=True, check=True
    ).stdout.strip()
    entries = []
    for origin, root in (("repository", repository), ("external_data", external)):
        for relative in snapshot_files[origin]:
            source = root / relative
            target = reference / origin / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            source_hash = run_state.file_sha256(source)
            if not target.exists() or run_state.file_sha256(target) != source_hash:
                shutil.copy2(source, target)
            entries.append({"origin": origin, "path": relative, "sha256": source_hash, "bytes": source.stat().st_size})
    manifest = {
        "bubbletea_commit": commit,
        "snapshot_date": time.strftime("%Y-%m-%d"),
        "note": "Read-only copy of bubbletea inputs; bubbletea itself is never modified.",
        "files": entries,
    }
    (reference / "manifest.json").write_text(json.dumps(manifest, indent=2))
    return manifest


def check_selector(config: dict) -> dict:
    """Scores from the JSON re-implementation must equal bubbletea's stored joblib scores."""
    reference = run_state.reference_dir(config)
    stored = pd.read_csv(reference / "external_data" / "m60_positive_control_v1" / "scored_sources.csv")
    model = selector.FrozenSelector(
        reference / "repository" / "data/literature/validation/point_source_logistic_model_v1.json"
    )
    scored = model.score(stored[selector.raw_gaia_columns])
    difference = np.abs(scored["selector_probability"].to_numpy() - stored["point_source_logistic_probability"])
    decisions_equal = (
        scored["selector_selected"].to_numpy() == stored["point_source_logistic_selected"].astype(bool).to_numpy()
    )
    return {
        "rows": len(stored),
        "maximum_probability_difference": float(difference.max()),
        "decision_mismatches": int((~decisions_equal).sum()),
        "selected_stored": int(stored["point_source_logistic_selected"].astype(bool).sum()),
    }


def build_fornax_reference(config: dict) -> dict:
    """Known compact objects within 3 deg of NGC 1399, with sizes and magnitudes from Saifollahi et al. 2021."""
    reference = run_state.reference_dir(config)
    repository = reference / "repository"
    field = config["fields"]["fornax"]
    centre = SkyCoord(field["ra_deg"], field["dec_deg"], unit="deg")
    catalogue = pd.read_csv(
        repository / "data/literature/validation/canonical_reference_catalog.csv", dtype={"gaia_dr3_ids": str}
    )
    coordinates = SkyCoord(catalogue["ra"].to_numpy(), catalogue["dec"].to_numpy(), unit="deg")
    catalogue["separation_deg"] = coordinates.separation(centre).deg
    fornax = catalogue[catalogue["separation_deg"] < 3.0].copy()
    fornax_coordinates = SkyCoord(fornax["ra"].to_numpy(), fornax["dec"].to_numpy(), unit="deg")
    readme = repository / "reference/saifollahi2021/ReadMe.txt"
    for label, file_name in (("a1", "tablea1.dat"), ("a6", "tablea6.dat")):
        table = astropy_ascii.read(repository / "reference/saifollahi2021" / file_name, readme=readme, format="cds")
        table_coordinates = SkyCoord(np.array(table["RAdeg"]), np.array(table["DEdeg"]), unit="deg")
        index, distance, _ = fornax_coordinates.match_to_catalog_sky(table_coordinates)
        matched = distance.arcsec < 0.5
        for column, source in (("half_light_radius_pc", "rh"), ("g_mag", "gmag"), ("i_mag", "imag")):
            values = np.where(matched, np.ma.filled(table[source][index].astype(float), np.nan), np.nan)
            target = f"saifollahi_{label}_{column}"
            fornax[target] = values
    fornax["half_light_radius_pc"] = fornax["saifollahi_a1_half_light_radius_pc"].fillna(
        fornax["saifollahi_a6_half_light_radius_pc"]
    )
    fornax["g_mag"] = fornax["saifollahi_a1_g_mag"].fillna(fornax["saifollahi_a6_g_mag"])
    fornax["in_target_field"] = fornax["separation_deg"] < field["radius_deg"]
    fornax.to_parquet(reference / "fornax_reference.parquet", index=False)
    in_field = fornax[fornax["in_target_field"]]
    return {
        "within_3_deg": fornax["classification_state"].value_counts().to_dict(),
        "within_target_field": in_field["classification_state"].value_counts().to_dict(),
        "with_half_light_radius_in_field": int(in_field["half_light_radius_pc"].notna().sum()),
        "with_gaia_id_in_field": int(in_field["gaia_dr3_ids"].notna().sum()),
    }


def check_services(config: dict) -> dict:
    """One small real request per service; returns timing and a short result for each."""
    field = config["fields"]["fornax"]
    ra_deg, dec_deg = field["ra_deg"], field["dec_deg"] + 0.3  # away from the centre of NGC 1399
    radius = config["smoke_test"]["radius_deg"]
    results = {}

    def attempt(name, function):
        start = time.time()
        try:
            results[name] = {"ok": True, "result": function(), "seconds": round(time.time() - start, 1)}
        except Exception as error:
            results[name] = {"ok": False, "error": f"{type(error).__name__}: {error}"[:300]}
        print(f"  service {name}: {results[name]}")

    attempt("gaia_tap", lambda: gaia_access.count_cone(config, ra_deg, dec_deg, radius))
    attempt("euclid_tap", lambda: euclid_catalogue.count_cone(config, ra_deg, dec_deg, radius))

    def legacy_lsdb():
        import lsdb

        catalogue = lsdb.open_catalog(config["legacy"]["lsdb_url"], columns=["RA", "DEC", "TYPE", "FLUX_R"])
        frame = catalogue.cone_search(ra=ra_deg, dec=dec_deg, radius_arcsec=60.0).compute()
        return {"rows_in_1_arcmin": len(frame), "margin": catalogue.margin is not None}

    attempt("legacy_dr11_lsdb", legacy_lsdb)

    def legacy_cutout(layer):
        response = requests.get(
            f"{config['legacy']['cutout_url']}/jpeg-cutout",
            params={"ra": ra_deg, "dec": dec_deg, "layer": layer, "pixscale": 0.262, "size": 96},
            timeout=120,
        )
        response.raise_for_status()
        image = np.asarray(Image.open(io.BytesIO(response.content)).convert("RGB"))
        unique_colours = len(np.unique(image.reshape(-1, 3), axis=0))
        return {"shape": list(image.shape), "unique_colours": unique_colours, "mean_level": float(image.mean())}

    for layer in config["legacy"]["cutout_layers"]:
        attempt(f"legacy_cutout_{layer}", lambda layer=layer: legacy_cutout(layer))

    def euclid_cutout():
        mosaics = euclid_catalogue.find_mosaics(ra_deg, dec_deg)
        vis = mosaics[mosaics["filter_name"] == "VIS"][0]
        folder = run_state.stage_dir(config, stage_name) / "tables"
        path = euclid_catalogue.get_cutout(
            vis["file_path"], vis["file_name"], ra_deg, dec_deg, 0.1, folder / "service_check_vis_cutout.fits"
        )
        from astropy.io import fits

        data = fits.getdata(path)
        return {"shape": list(data.shape), "finite_fraction": float(np.isfinite(data).mean())}

    attempt("euclid_cutout", euclid_cutout)
    return results


def choose_control_field(config: dict) -> tuple[dict, pd.DataFrame]:
    """Wide-survey field without nearby galaxies, at Fornax-like Galactic latitude and Gaia density."""
    target = config["fields"]["fornax"]
    rules = config["fields"]["control"]["selection"]
    radius_deg = config["fields"]["control"]["radius_deg"]
    centre = SkyCoord(target["ra_deg"], target["dec_deg"], unit="deg")
    moc = MOC.from_fits(run_state.expand(config["euclid"]["footprint_moc"]))
    galaxies = pd.read_csv(run_state.reference_dir(config) / "repository/data/galaxy_sample/galaxy_sample_ranked.csv")
    galaxy_coordinates = SkyCoord(galaxies["ra"].to_numpy(), galaxies["dec"].to_numpy(), unit="deg")
    rng = np.random.default_rng(20261113)
    disc_radius = radius_deg * np.sqrt(rng.uniform(size=3000))
    disc_angle = rng.uniform(0, 2 * np.pi, size=3000)

    def coverage(position: SkyCoord) -> float:
        points = position.spherical_offsets_by(
            disc_radius * np.cos(disc_angle) * u.deg, disc_radius * np.sin(disc_angle) * u.deg
        )
        return float(moc.contains_skycoords(points).mean())

    step = rules["grid_step_deg"]
    offsets = np.arange(-rules["maximum_separation_deg"], rules["maximum_separation_deg"] + step / 2, step)
    rows = []
    for offset_east in offsets:
        for offset_north in offsets:
            position = centre.spherical_offsets_by(offset_east * u.deg, offset_north * u.deg)
            separation = position.separation(centre).deg
            if not rules["minimum_separation_deg"] <= separation <= rules["maximum_separation_deg"]:
                continue
            rows.append(
                {
                    "ra_deg": position.ra.deg,
                    "dec_deg": position.dec.deg,
                    "separation_deg": separation,
                    "galactic_latitude_deg": position.galactic.b.deg,
                    "coverage_fraction": coverage(position),
                    "galaxies_nearby": int(
                        (galaxy_coordinates.separation(position).deg < rules["galaxy_exclusion_radius_deg"]).sum()
                    ),
                    "clear_of_avoid_list": all(
                        position.separation(SkyCoord(item["ra_deg"], item["dec_deg"], unit="deg")).deg
                        > item["radius_deg"]
                        for item in rules["avoid"]
                    ),
                }
            )
    grid = pd.DataFrame(rows)
    target_latitude = centre.galactic.b.deg
    grid["latitude_difference_deg"] = (grid["galactic_latitude_deg"] - target_latitude).abs()
    grid["eligible"] = (
        (grid["coverage_fraction"] >= rules["minimum_coverage_fraction"])
        & (grid["galaxies_nearby"] == 0)
        & grid["clear_of_avoid_list"]
        & (grid["latitude_difference_deg"] <= rules["maximum_galactic_latitude_difference_deg"])
    )
    eligible = grid[grid["eligible"]].sort_values("latitude_difference_deg").head(6).copy()
    if eligible.empty:
        raise RuntimeError("no eligible control field; relax the rules in the configuration and document it")
    target_count = gaia_access.count_cone(config, target["ra_deg"], target["dec_deg"], target["radius_deg"])
    eligible["gaia_count"] = [
        gaia_access.count_cone(config, row.ra_deg, row.dec_deg, radius_deg) for row in eligible.itertuples()
    ]
    eligible["gaia_count_ratio"] = eligible["gaia_count"] / target_count
    best = eligible.iloc[(eligible["gaia_count_ratio"] - 1).abs().argmin()]
    control = {
        "role": "control",
        "ra_deg": round(float(best["ra_deg"]), 5),
        "dec_deg": round(float(best["dec_deg"]), 5),
        "radius_deg": radius_deg,
        "separation_from_target_deg": round(float(best["separation_deg"]), 2),
        "galactic_latitude_deg": round(float(best["galactic_latitude_deg"]), 2),
        "coverage_fraction": float(best["coverage_fraction"]),
        "gaia_count": int(best["gaia_count"]),
        "gaia_count_ratio_to_target": round(float(best["gaia_count_ratio"]), 3),
        "target_gaia_count": target_count,
        "target_galactic_latitude_deg": round(float(target_latitude), 2),
        "eligible_grid_points": int(grid["eligible"].sum()),
        "grid_points": len(grid),
    }
    return control, grid


def plot_field_map(config: dict, fields: dict, grid: pd.DataFrame) -> None:
    reference = run_state.reference_dir(config)
    moc = MOC.from_fits(run_state.expand(config["euclid"]["footprint_moc"]))
    known = pd.read_parquet(reference / "fornax_reference.parquet")
    galaxies = pd.read_csv(reference / "repository/data/galaxy_sample/galaxy_sample_ranked.csv")
    target = fields["fornax"]
    half_width = config["fields"]["control"]["selection"]["maximum_separation_deg"] + 1.5
    ra_axis = np.linspace(
        target["ra_deg"] - half_width / np.cos(np.radians(target["dec_deg"])),
        target["ra_deg"] + half_width / np.cos(np.radians(target["dec_deg"])),
        500,
    )
    dec_axis = np.linspace(target["dec_deg"] - half_width, target["dec_deg"] + half_width, 500)
    ra_grid, dec_grid = np.meshgrid(ra_axis, dec_axis)
    covered = moc.contains_lonlat(ra_grid.ravel() * u.deg, dec_grid.ravel() * u.deg).reshape(ra_grid.shape)

    figure, axis = plt.subplots(figsize=(qa_plots.double_width, 0.82 * qa_plots.double_width))
    axis.pcolormesh(ra_axis, dec_axis, covered, cmap="Greys", vmin=0, vmax=4, shading="auto", rasterized=True)
    eligible = grid[grid["eligible"]]
    axis.scatter(
        eligible["ra_deg"],
        eligible["dec_deg"],
        s=10,
        marker="+",
        color=qa_plots.colors["control"],
        linewidths=0.6,
        label=r"eligible control centres",
    )
    nearby = galaxies[
        (np.abs(galaxies["dec"] - target["dec_deg"]) < half_width)
        & (np.abs(galaxies["ra"] - target["ra_deg"]) < half_width / np.cos(np.radians(target["dec_deg"])))
    ]
    axis.scatter(
        nearby["ra"],
        nearby["dec"],
        s=14,
        facecolor="none",
        edgecolor=qa_plots.colors["star"],
        linewidths=0.6,
        label=r"galaxies, $D<25$ Mpc",
    )
    for state, color, size in (
        ("confirmed", qa_plots.colors["known"], 3),
        ("candidate", qa_plots.colors["candidate"], 3),
    ):
        subset = known[known["classification_state"] == state]
        axis.scatter(subset["ra"], subset["dec"], s=size, color=color, label=rf"known {state} ({len(subset)})")
    angle = np.linspace(0, 2 * np.pi, 200)
    for name, field in fields.items():
        color = qa_plots.colors["known"] if field["role"] == "target" else qa_plots.colors["control"]
        axis.plot(
            field["ra_deg"] + field["radius_deg"] * np.cos(angle) / np.cos(np.radians(field["dec_deg"])),
            field["dec_deg"] + field["radius_deg"] * np.sin(angle),
            color=color,
            lw=1.3,
        )
        axis.annotate(
            name, (field["ra_deg"], field["dec_deg"] + field["radius_deg"] + 0.15), ha="center", color=color, fontsize=9
        )
    axis.set_xlim(ra_axis.max(), ra_axis.min())
    axis.set_ylim(dec_axis.min(), dec_axis.max())
    axis.set_aspect(1 / np.cos(np.radians(target["dec_deg"])))
    axis.set_xlabel(r"RA (deg)")
    axis.set_ylabel(r"Dec (deg)")
    axis.set_title(r"Stage 0: fields on the Euclid DR1 wide footprint (grey = covered)")
    axis.legend(loc="lower left", frameon=True, framealpha=0.9)
    qa_plots.save(figure, run_state.stage_dir(config, stage_name) / "figures", "field_map")


def main() -> None:
    config = run_state.load_config()
    folder = run_state.stage_dir(config, stage_name)
    print("snapshot of bubbletea inputs")
    manifest = snapshot_bubbletea(config)
    print("selector regression test")
    selector_check = check_selector(config)
    print("Fornax reference table")
    reference_counts = build_fornax_reference(config)
    print("service checks")
    services = check_services(config)
    print("control field")
    control, grid = choose_control_field(config)
    fields = {"fornax": {**config["fields"]["fornax"]}, "control": control}
    (folder / "tables" / "fields.json").write_text(json.dumps(fields, indent=2))
    grid.to_csv(folder / "tables" / "control_field_grid.csv", index=False)
    plot_field_map(config, fields, grid)

    total_area = sum(np.pi * field["radius_deg"] ** 2 for field in fields.values())
    essential = ["gaia_tap", "euclid_tap", "euclid_cutout"]
    optional = [name for name in services if name not in essential]
    gates = [
        run_state.gate("snapshot", "all files copied with hashes", f"{len(manifest['files'])} files", True),
        run_state.gate(
            "selector_reproduces",
            "max |probability difference| < 1e-6 and no decision mismatch",
            selector_check,
            selector_check["maximum_probability_difference"] < 1e-6 and selector_check["decision_mismatches"] == 0,
        ),
        run_state.gate(
            "essential_services",
            "Gaia TAP, Euclid TAP and Euclid cutouts answer",
            {name: services[name]["ok"] for name in essential},
            all(services[name]["ok"] for name in essential),
        ),
        run_state.gate(
            "optional_services",
            "Legacy DR11 LSDB and cutout layers answer",
            {name: services[name]["ok"] for name in optional},
            all(services[name]["ok"] for name in optional),
            fatal=False,
        ),
        run_state.gate(
            "control_field",
            "coverage >= 0.99, |delta b| <= 5 deg, no D<25 Mpc galaxy within 1.5 deg, Gaia count within 30% of target",
            control,
            abs(control["gaia_count_ratio_to_target"] - 1) < 0.3,
        ),
        run_state.gate(
            "area_budget",
            f"total area <= {config['budgets']['maximum_area_square_deg']} deg2",
            round(total_area, 2),
            total_area <= config["budgets"]["maximum_area_square_deg"],
        ),
    ]
    metrics = {
        "bubbletea_commit": manifest["bubbletea_commit"],
        "selector_check": selector_check,
        "fornax_reference": reference_counts,
        "services": services,
        "fields": fields,
        "total_area_square_deg": total_area,
    }
    run_state.write_summary(config, stage_name, metrics, gates)


if __name__ == "__main__":
    main()
