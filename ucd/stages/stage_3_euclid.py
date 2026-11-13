"""Stage 3: Euclid MER entries at the Gaia positions, and the Gaia-to-Euclid displacement.

The Gaia source is the anchor. For each one we take the nearest MER entry at the Gaia position (propagated to the
Euclid epoch when Gaia has a proper motion), record ambiguity and neighbours, and measure how far the Euclid position
lies from the Gaia 2016.0 position. The time baseline and the frame offset are fitted per Euclid tile from stars
with good Gaia proper motions, so no epoch has to be read from tile metadata.

Usage: uv run python -m ucd.stages.stage_3_euclid [--smoke]
Products: stage_3_euclid/tables/gaia_euclid_<field>.parquet, tile_calibration.csv, QA figures, summary.json
"""

import argparse

import astropy.units as u
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from astropy.coordinates import SkyCoord

from ucd.lib import crossmatch, euclid_catalogue, qa_plots, run_state

stage_name = "stage_3_euclid"
calibration_radius_arcsec = 2.0
search_radius_arcsec = 1.0
candidate_match_radii = [1.0, 0.7, 0.5, 0.3]
coverage_radius_arcsec = 20.0
candidate_moving_thresholds = [3.0, 4.0, 5.0, 6.0, 8.0]
compact_limit = -2.6  # mu_max - mag below this: point-like or nearly so
thresholds = {"moving": 3.0}
magnitude_bins = np.array([16.0, 17.5, 18.5, 19.5, 20.25, 21.0])


def magnitude(flux: pd.Series) -> pd.Series:
    return 23.9 - 2.5 * np.log10(flux.where(flux > 0))


def robust_sigma(values: np.ndarray) -> float:
    values = values[np.isfinite(values)]
    return float(1.4826 * np.median(np.abs(values - np.median(values)))) if len(values) else np.nan


def fit_tile(offset_east: np.ndarray, offset_north: np.ndarray, pm_east: np.ndarray, pm_north: np.ndarray) -> dict:
    """Fit offset = zero_point + baseline * proper_motion (shared baseline), with 3-sigma clipping."""
    keep = np.ones(len(offset_east), dtype=bool)
    for _ in range(4):
        count = keep.sum()
        design = np.zeros((2 * count, 3))
        design[:count, 0] = 1
        design[:count, 2] = pm_east[keep]
        design[count:, 1] = 1
        design[count:, 2] = pm_north[keep]
        target = np.concatenate([offset_east[keep], offset_north[keep]])
        solution, *_ = np.linalg.lstsq(design, target, rcond=None)
        residual_east = offset_east - solution[0] - solution[2] * pm_east
        residual_north = offset_north - solution[1] - solution[2] * pm_north
        scatter = robust_sigma(np.concatenate([residual_east[keep], residual_north[keep]]))
        keep = np.hypot(residual_east, residual_north) < 3 * np.sqrt(2) * scatter
    return {
        "zero_east_mas": float(solution[0]),
        "zero_north_mas": float(solution[1]),
        "baseline_years": float(solution[2]),
        "stars_used": int(keep.sum()),
        "residual_scatter_mas": scatter,
    }


def process_field(config: dict, name: str, field: dict, gaia: pd.DataFrame, folder, smoke: bool) -> tuple:
    settings = config["euclid"]
    print(f"{name}: MER cone")
    cone = euclid_catalogue.download_cone(
        config, field["ra_deg"], field["dec_deg"], field["radius_deg"], folder / "tables" / f"cone_{name}",
        strips=1 if smoke else settings["download_strips"],
    )  # fmt: skip
    cone["ie_mag"] = magnitude(cone["flux_detection_total"])
    bright = cone[cone["ie_mag"] < settings["match_maximum_magnitude"]].reset_index(drop=True)
    mer = SkyCoord(bright["right_ascension"].to_numpy(), bright["declination"].to_numpy(), unit="deg")
    all_mer = SkyCoord(cone["right_ascension"].to_numpy(), cone["declination"].to_numpy(), unit="deg")
    raw = SkyCoord(gaia["ra"].to_numpy(), gaia["dec"].to_numpy(), unit="deg")

    # 1. Calibration: baseline and frame offset per tile from well-measured stars matched at the raw position.
    first = crossmatch.nearest_match(raw, mer, calibration_radius_arcsec)
    matched = first["catalogue_index"] >= 0
    tile = np.where(matched, bright["tile_index"].to_numpy()[first["catalogue_index"].clip(lower=0)], -1)
    pm_error = np.hypot(gaia["pmra_error"], gaia["pmdec_error"])
    star = (
        matched
        & gaia["has_five_parameter_astrometry"]
        & gaia["phot_g_mean_mag"].between(16.5, 20.0)
        & (gaia["ruwe"] < 1.4)
        & (pm_error < 0.8)
        & (first["matches_in_radius"] == 1)
    ).to_numpy()
    east = first["offset_east_arcsec"].to_numpy() * 1e3
    north = first["offset_north_arcsec"].to_numpy() * 1e3
    pm_east, pm_north = gaia["pmra"].to_numpy(), gaia["pmdec"].to_numpy()
    overall = fit_tile(east[star], north[star], pm_east[star], pm_north[star])
    tile_rows = []
    for tile_index in np.unique(tile[star]):
        members = star & (tile == tile_index)
        fit = (
            fit_tile(east[members], north[members], pm_east[members], pm_north[members])
            if members.sum() >= 40
            else overall
        )
        tile_rows.append({"field": name, "tile_index": int(tile_index), "stars_available": int(members.sum()), **fit})
    tiles = pd.DataFrame(tile_rows)
    lookup = tiles.set_index("tile_index")

    def per_source(column: str) -> np.ndarray:
        values = pd.Series(tile).map(lookup[column]).to_numpy(dtype=float)
        return np.where(np.isfinite(values), values, overall[column])

    baseline = per_source("baseline_years")
    zero_east, zero_north = per_source("zero_east_mas"), per_source("zero_north_mas")

    # 2. Final match: at the propagated position when Gaia has a proper motion, else at the raw position.
    has_motion = gaia["has_five_parameter_astrometry"].to_numpy()
    shift_east = np.where(has_motion, np.nan_to_num(pm_east) * baseline, 0.0)
    shift_north = np.where(has_motion, np.nan_to_num(pm_north) * baseline, 0.0)
    anchor = raw.spherical_offsets_by(shift_east * u.mas, shift_north * u.mas)
    final = crossmatch.nearest_match(anchor, mer, search_radius_arcsec)
    has_match = (final["catalogue_index"] >= 0).to_numpy()
    index = final["catalogue_index"].clip(lower=0).to_numpy()
    false_match_rates = {
        str(radius): crossmatch.displaced_match_fraction(anchor, mer, radius) for radius in candidate_match_radii
    }

    result = gaia.copy()
    result["euclid_matched"] = has_match
    result["euclid_separation_arcsec"] = final["separation_arcsec"].to_numpy()
    result["euclid_matches_in_radius"] = final["matches_in_radius"].to_numpy()
    result["euclid_second_separation_arcsec"] = final["second_separation_arcsec"].to_numpy()
    result["euclid_raw_separation_arcsec"] = first["separation_arcsec"].to_numpy()
    for column in bright.columns:
        values = bright[column].to_numpy()[index]
        if values.dtype.kind in "iu":
            result[f"euclid_{column}"] = np.where(has_match, values, -1)
        else:
            result[f"euclid_{column}"] = np.where(has_match, values, np.nan)
    neighbour_index, _, _, _ = all_mer.search_around_sky(anchor, 3.0 * u.arcsec)
    result["euclid_entries_within_3_arcsec"] = np.bincount(neighbour_index, minlength=len(gaia))
    coverage_index, _, _, _ = all_mer.search_around_sky(raw, coverage_radius_arcsec * u.arcsec)
    result["euclid_covered"] = np.bincount(coverage_index, minlength=len(gaia)) > 0

    # 3. Displacement of the Euclid position from the Gaia 2016.0 position, frame offset removed.
    offset_east, offset_north = raw.spherical_offsets_to(mer[index])
    displacement_east = np.where(has_match, offset_east.mas - zero_east, np.nan)
    displacement_north = np.where(has_match, offset_north.mas - zero_north, np.nan)
    result["euclid_baseline_years"] = baseline
    result["displacement_east_mas"] = displacement_east
    result["displacement_north_mas"] = displacement_north
    result["displacement_mas"] = np.hypot(displacement_east, displacement_north)
    result["implied_proper_motion_mas_per_year"] = result["displacement_mas"] / baseline
    return result, tiles, cone, {"false_match_rates": false_match_rates, "overall_fit": overall}


def add_displacement_significance(tables: dict) -> dict:
    """Euclid centroid scatter per magnitude bin from stars with Gaia proper motions; significance for everyone."""
    combined = pd.concat(tables.values(), ignore_index=True)
    star = (
        combined["euclid_matched"]
        & combined["has_five_parameter_astrometry"]
        & (combined["ruwe"] < 1.4)
        & (combined["euclid_matches_in_radius"] == 1)
    )
    residual_east = combined["displacement_east_mas"] - combined["pmra"] * combined["euclid_baseline_years"]
    residual_north = combined["displacement_north_mas"] - combined["pmdec"] * combined["euclid_baseline_years"]
    gaia_east = np.hypot(combined["ra_error"], combined["pmra_error"] * combined["euclid_baseline_years"])
    gaia_north = np.hypot(combined["dec_error"], combined["pmdec_error"] * combined["euclid_baseline_years"])
    centres, scatter_rows = [], []
    for low, high in zip(magnitude_bins[:-1], magnitude_bins[1:], strict=True):
        members = star & combined["phot_g_mean_mag"].between(low, high)
        if members.sum() < 30:
            continue
        measured = robust_sigma(np.concatenate([residual_east[members], residual_north[members]]))
        gaia_term = float(np.median(np.concatenate([gaia_east[members], gaia_north[members]])))
        euclid_term = float(np.sqrt(max(measured**2 - gaia_term**2, 1.0)))
        centres.append(0.5 * (low + high))
        scatter_rows.append(
            {"g_low": low, "g_high": high, "stars": int(members.sum()), "residual_scatter_mas": measured,
             "median_gaia_term_mas": gaia_term, "euclid_centroid_scatter_mas": euclid_term}
        )  # fmt: skip
    scatter = pd.DataFrame(scatter_rows)
    for frame in tables.values():
        euclid_term = np.interp(frame["phot_g_mean_mag"], centres, scatter["euclid_centroid_scatter_mas"])
        sigma_east = np.hypot(euclid_term, frame["ra_error"])
        sigma_north = np.hypot(euclid_term, frame["dec_error"])
        frame["displacement_significance"] = np.hypot(
            frame["displacement_east_mas"] / sigma_east, frame["displacement_north_mas"] / sigma_north
        )
        expected = np.hypot(frame["pmra"], frame["pmdec"]) * frame["euclid_baseline_years"]
        frame["expected_displacement_significance"] = expected / np.hypot(
            euclid_term, np.hypot(frame["ra_error"], frame["dec_error"]) / np.sqrt(2)
        )
    return {"scatter": scatter}


def adopt_match_radius(tables: dict, rates: dict) -> float:
    """Largest candidate radius whose displaced-position (false) match rate is below 1% in every field."""
    adopted = next(
        (radius for radius in candidate_match_radii if all(rates[name][str(radius)] < 0.01 for name in tables)),
        candidate_match_radii[-1],
    )
    for frame in tables.values():
        beyond = frame["euclid_matched"] & (frame["euclid_separation_arcsec"] > adopted)
        frame.loc[beyond, "euclid_matched"] = False
        for column in frame.columns:
            if not column.startswith(("euclid_", "displacement_", "implied_")):
                continue
            if column in (
                "euclid_matched",
                "euclid_covered",
                "euclid_entries_within_3_arcsec",
                "euclid_baseline_years",
            ):
                continue
            if frame[column].dtype.kind == "f":
                frame.loc[beyond, column] = np.nan
            elif frame[column].dtype.kind in "iu" and column != "euclid_matches_in_radius":
                frame.loc[beyond, column] = -1
    return adopted


def calibrate_displacement(tables: dict) -> dict:
    """Choose the significance threshold for 'moving' from stars and compact non-moving sources (never from UCDs)."""
    combined = pd.concat(tables.values(), ignore_index=True)
    usable = (
        combined["euclid_matched"]
        & combined["has_five_parameter_astrometry"]
        & (combined["euclid_matches_in_radius"] == 1)
    )
    compact = combined["euclid_mumax_minus_mag"] < compact_limit
    movers = usable & (combined["expected_displacement_significance"] > 5)
    still_compact = usable & compact & (combined["expected_displacement_significance"] < 1)
    still_extended = usable & ~compact & (combined["expected_displacement_significance"] < 1)
    significance = combined["displacement_significance"]
    rows = []
    for threshold in candidate_moving_thresholds:
        rows.append(
            {
                "threshold": threshold,
                "mover_recovery_fraction": float((significance[movers] > threshold).mean()),
                "still_compact_false_flag_fraction": float((significance[still_compact] > threshold).mean()),
                "still_extended_flag_fraction": float((significance[still_extended] > threshold).mean()),
            }
        )
    passing = [
        row
        for row in rows
        if row["mover_recovery_fraction"] >= 0.9 and row["still_compact_false_flag_fraction"] <= 0.05
    ]
    adopted = passing[0]["threshold"] if passing else candidate_moving_thresholds[2]
    thresholds["moving"] = adopted
    for frame in tables.values():
        frame["displacement_moving"] = frame["displacement_significance"] > adopted
    result = {
        "threshold_scan": rows,
        "adopted_threshold": adopted,
        "validated_for_compact_sources": bool(passing),
        "stars_expected_to_move_over_5_sigma": int(movers.sum()),
        "still_compact_sources": int(still_compact.sum()),
        "still_extended_sources": int(still_extended.sum()),
        "note": "For extended sources a displacement can be a centroid difference; use it for compact ones.",
    }
    for label, limits in (("g_under_19", (0, 19)), ("g_19_to_20", (19, 20)), ("g_20_to_21", (20, 21))):
        members = movers & combined["phot_g_mean_mag"].between(*limits)
        result[f"mover_recovery_{label}"] = [int((significance[members] > adopted).sum()), int(members.sum())]
    return result


def fetch_extras(config: dict, name: str, frame: pd.DataFrame, folder) -> pd.DataFrame:
    """Morphology, PHZ classification and (optional, unused) photo-z rows for the matched objects."""
    settings = config["euclid"]
    object_ids = frame.loc[frame["euclid_matched"], "euclid_object_id"].astype("int64").tolist()
    groups = [
        ("morphology", settings["morphology"], euclid_catalogue.morphology_columns),
        ("classification", settings["classification"], euclid_catalogue.classification_columns),
    ]
    if settings["with_photo_z"]:
        groups.append(("photo_z", settings["photo_z"], euclid_catalogue.photo_z_columns))
    for label, table_name, columns in groups:
        print(f"{name}: {label} rows by object_id")
        extra = euclid_catalogue.fetch_by_object_id(
            table_name, columns, object_ids, folder / "tables" / f"{label}_{name}.parquet"
        )
        extra = extra.rename(columns={column: f"euclid_{column}" for column in columns})
        frame = frame.merge(extra, how="left", left_on="euclid_object_id", right_on="object_id").drop(
            columns="object_id"
        )
    return frame


def add_magnitudes(frame: pd.DataFrame) -> pd.DataFrame:
    frame["euclid_ie_mag"] = magnitude(frame["euclid_flux_detection_total"])
    frame["euclid_ie_psf_mag"] = magnitude(frame["euclid_flux_vis_psf"])
    for band in ("vis", "y", "j", "h"):
        frame[f"euclid_{band}_aperture_mag"] = magnitude(frame[f"euclid_flux_{band}_2fwhm_aper"])
    for band in ("g", "r", "i", "z"):
        frame[f"euclid_decam_{band}_aperture_mag"] = magnitude(frame[f"euclid_flux_{band}_ext_decam_2fwhm_aper"])
    return frame


def plot_separation(tables: dict, radius: float, folder) -> None:
    figure, axes = plt.subplots(1, 2, figsize=(qa_plots.double_width, 2.9))
    bins = np.linspace(0, 2, 81)
    for name, frame in tables.items():
        color = qa_plots.colors["known"] if name == "fornax" else qa_plots.colors["control"]
        axes[0].hist(
            frame["euclid_raw_separation_arcsec"].dropna(),
            bins=bins,
            histtype="step",
            color=color,
            ls=":",
            label=rf"{name}: raw Gaia 2016.0 position",
        )
        axes[0].hist(
            frame["euclid_separation_arcsec"].dropna(),
            bins=bins,
            histtype="step",
            color=color,
            label=rf"{name}: propagated where possible",
        )
        edges = np.arange(13, 22.01, 0.5)
        centres = 0.5 * (edges[:-1] + edges[1:])
        group = pd.cut(frame["phot_g_mean_mag"], edges)
        fraction = frame.groupby(group, observed=False)["euclid_matched"].mean()
        axes[1].plot(centres, fraction.to_numpy(), marker="o", ms=3, color=color, label=rf"{name}")
    axes[0].axvline(radius, color="k", lw=0.7, ls="--")
    axes[0].set_yscale("log")
    axes[0].set_xlabel(r"separation Gaia--Euclid (arcsec)")
    axes[0].set_ylabel(r"sources")
    axes[0].legend(fontsize=6.5)
    axes[1].set_xlabel(r"$G$ (mag)")
    axes[1].set_ylabel(rf"fraction with Euclid entry within {radius:.1f}$''$")
    axes[1].set_ylim(0, 1.05)
    axes[1].legend()
    qa_plots.save(figure, folder, "euclid_match_separation")


def plot_displacement(tables: dict, scatter: pd.DataFrame, folder) -> None:
    combined = pd.concat(tables.values(), ignore_index=True)
    star = (
        combined["euclid_matched"]
        & combined["has_five_parameter_astrometry"]
        & (combined["euclid_matches_in_radius"] == 1)
    )
    figure, axes = plt.subplots(1, 3, figsize=(qa_plots.double_width, 2.6))
    for axis, (measured, motion, label) in zip(
        axes[:2], (("displacement_east_mas", "pmra", "east"), ("displacement_north_mas", "pmdec", "north")), strict=True
    ):
        expected = combined.loc[star, motion] * combined.loc[star, "euclid_baseline_years"]
        axis.scatter(expected, combined.loc[star, measured], s=1, color=qa_plots.colors["star"], rasterized=True)
        axis.plot([-400, 400], [-400, 400], color="k", lw=0.6)
        axis.set_xlim(-400, 400)
        axis.set_ylim(-400, 400)
        axis.set_xlabel(rf"Gaia proper motion $\times$ baseline, {label} (mas)")
        axis.set_ylabel(rf"Euclid $-$ Gaia 2016.0, {label} (mas)")
    axes[2].step(scatter["g_high"], scatter["residual_scatter_mas"], where="pre", color="k", label=r"residual scatter")
    axes[2].step(
        scatter["g_high"],
        scatter["euclid_centroid_scatter_mas"],
        where="pre",
        color=qa_plots.colors["selected"],
        label=r"Euclid centroid term",
    )
    axes[2].step(
        scatter["g_high"],
        scatter["median_gaia_term_mas"],
        where="pre",
        color=qa_plots.colors["star"],
        label=r"Gaia term (median)",
    )
    axes[2].set_xlabel(r"$G$ (mag)")
    axes[2].set_ylabel(r"scatter per axis (mas)")
    axes[2].set_yscale("log")
    axes[2].legend()
    figure.tight_layout()
    qa_plots.save(figure, folder, "displacement_calibration")

    figure, axes = plt.subplots(1, 2, figsize=(qa_plots.double_width, 2.9), sharey=True)
    for axis, (name, frame) in zip(axes, tables.items(), strict=True):
        matched = frame[frame["euclid_matched"]]
        groups = [
            (
                matched["has_five_parameter_astrometry"] & matched["gaia_star_like_motion"],
                qa_plots.colors["star"],
                r"Gaia: significant motion",
            ),
            (
                matched["has_five_parameter_astrometry"] & ~matched["gaia_star_like_motion"],
                qa_plots.colors["all"],
                r"Gaia: no significant motion",
            ),
            (~matched["has_five_parameter_astrometry"], qa_plots.colors["selected"], r"no Gaia proper motion"),
        ]
        for mask, color, label in groups:
            axis.scatter(
                matched.loc[mask, "phot_g_mean_mag"],
                matched.loc[mask, "displacement_significance"].clip(0.05, 900),
                s=1.2,
                color=color,
                rasterized=True,
                label=label,
            )
        known = matched[matched["known_state"] == "confirmed"]
        if len(known):
            axis.scatter(
                known["phot_g_mean_mag"],
                known["displacement_significance"].clip(0.05, 900),
                s=14,
                facecolor="none",
                edgecolor=qa_plots.colors["known"],
                linewidths=0.7,
                label=r"known confirmed",
            )
        axis.axhline(thresholds["moving"], color="k", lw=0.7, ls="--")
        axis.set_yscale("log")
        axis.set_xlim(13, 21.8)
        axis.set_xlabel(r"$G$ (mag)")
        axis.set_title(rf"{name}")
    axes[0].set_ylabel(r"displacement significance")
    axes[0].legend(fontsize=6.5, markerscale=3, frameon=True)
    qa_plots.save(figure, folder, "displacement_significance")


def plot_photometry_and_compactness(tables: dict, folder) -> None:
    figure, axes = plt.subplots(len(tables), 3, figsize=(qa_plots.double_width, 2.5 * len(tables)), squeeze=False)
    for row, (name, frame) in enumerate(tables.items()):
        matched = frame[frame["euclid_matched"]]
        star = matched["gaia_star_like_motion"]
        known = matched[matched["known_state"] == "confirmed"]
        panels = [
            (
                "bp_rp",
                matched["phot_g_mean_mag"] - matched["euclid_ie_mag"],
                r"$G_{\rm BP}-G_{\rm RP}$",
                r"$G-I_{\rm E}$ (Kron)",
                (-0.5, 3.5),
                (-1.5, 2.5),
            ),
            (
                "euclid_ie_mag",
                matched["euclid_mumax_minus_mag"],
                r"$I_{\rm E}$ (mag)",
                r"$\mu_{\rm max}-{\rm mag}$",
                (15, 22.5),
                (-4.5, 1.0),
            ),
            (
                "euclid_ie_mag",
                matched["euclid_sersic_sersic_vis_radius"].clip(lower=1e-3),
                r"$I_{\rm E}$ (mag)",
                r"S\'ersic radius (arcsec)",
                (15, 22.5),
                (5e-3, 5),
            ),
        ]
        for column, (x_column, y_values, x_label, y_label, x_limits, y_limits) in enumerate(panels):
            axis = axes[row, column]
            axis.scatter(
                matched.loc[~star, x_column],
                y_values[~star],
                s=1.2,
                color=qa_plots.colors["selected"],
                rasterized=True,
                label=r"no significant Gaia motion",
            )
            axis.scatter(
                matched.loc[star, x_column],
                y_values[star],
                s=1.2,
                color=qa_plots.colors["star"],
                rasterized=True,
                label=r"Gaia stars (motion $>3\sigma$)",
            )
            if len(known):
                axis.scatter(
                    known[x_column],
                    y_values[known.index],
                    s=14,
                    facecolor="none",
                    edgecolor=qa_plots.colors["known"],
                    linewidths=0.7,
                    label=r"known confirmed",
                )
            axis.set_xlim(*x_limits)
            axis.set_ylim(*y_limits)
            axis.set_xlabel(x_label)
            axis.set_ylabel(y_label)
            if column == 2:
                axis.set_yscale("log")
            if column == 0:
                axis.set_title(rf"{name}", loc="left")
        axes[row, 0].legend(fontsize=6, markerscale=3, frameon=True)
    figure.tight_layout()
    qa_plots.save(figure, folder, "euclid_photometry_compactness")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    arguments = parser.parse_args()
    config = run_state.load_config()
    run_state.require_stages(config, ["stage_0_preflight", "stage_2_gaia"])
    fields = run_state.load_fields(config)
    gaia_folder = run_state.run_dir(config) / "stage_2_gaia" / "tables"
    if arguments.smoke:
        fields = run_state.smoke_fields(config, fields)
    folder = run_state.stage_dir(config, stage_name, smoke=arguments.smoke)

    tables, tile_tables, metrics = {}, [], {"fields": {}}
    for name, field in fields.items():
        gaia = pd.read_parquet(gaia_folder / f"gaia_{name}.parquet")
        if arguments.smoke:
            centre = SkyCoord(field["ra_deg"], field["dec_deg"], unit="deg")
            inside = (
                SkyCoord(gaia["ra"].to_numpy(), gaia["dec"].to_numpy(), unit="deg").separation(centre).deg
                < field["radius_deg"]
            )
            gaia = gaia[inside].reset_index(drop=True)
        frame, tiles, cone, extra = process_field(config, name, field, gaia, folder, arguments.smoke)
        tables[name] = frame
        tile_tables.append(tiles)
        metrics["fields"][name] = {"gaia_sources": len(gaia), "mer_entries_downloaded": len(cone), **extra}
    rates = {name: metrics["fields"][name]["false_match_rates"] for name in tables}
    radius = adopt_match_radius(tables, rates)
    metrics["adopted_match_radius_arcsec"] = radius
    calibration = add_displacement_significance(tables)
    validation = calibrate_displacement(tables)
    for name in tables:
        tables[name] = add_magnitudes(fetch_extras(config, name, tables[name], folder))
        frame = tables[name]
        matched = frame["euclid_matched"]
        own_id = frame["euclid_gaia_id"] == frame["source_id"]
        selected = frame["selector_selected"]
        no_motion = ~frame["has_five_parameter_astrometry"]
        metrics["fields"][name].update(
            {
                "matched": int(matched.sum()),
                "match_fraction": float(matched.mean()),
                "covered_fraction": float(frame["euclid_covered"].mean()),
                "match_fraction_covered_g_17_to_20p5": float(
                    matched[frame["euclid_covered"] & frame["phot_g_mean_mag"].between(17, 20.5)].mean()
                ),
                "ambiguous_two_or_more_in_radius": int((frame["euclid_matches_in_radius"] > 1).sum()),
                "mer_gaia_id_equals_source_id": int((matched & own_id).sum()),
                "mer_gaia_id_other_source": int((matched & ~own_id & (frame["euclid_gaia_id"] > 0)).sum()),
                "mer_gaia_id_empty": int((matched & (frame["euclid_gaia_id"] <= 0)).sum()),
                "selected_matched": int((selected & matched).sum()),
                "selected_without_gaia_motion_matched": int((selected & no_motion & matched).sum()),
                "selected_without_gaia_motion_flagged_moving": int(
                    (selected & no_motion & frame["displacement_moving"]).sum()
                ),
                "selected_flagged_moving": int((selected & frame["displacement_moving"]).sum()),
                "with_morphology": int(frame["euclid_sersic_sersic_vis_radius"].notna().sum()),
                "with_classification": int(frame["euclid_phz_star_prob"].notna().sum()),
            }
        )
        known = frame[frame["known_state"] == "confirmed"]
        if len(known):
            metrics["fields"][name]["known_confirmed_consistency_check"] = {
                "with_gaia": len(known),
                "euclid_matched": int(known["euclid_matched"].sum()),
                "flagged_moving": int(known["displacement_moving"].sum()),
                "median_displacement_significance": float(known["displacement_significance"].median()),
            }
        frame.to_parquet(folder / "tables" / f"gaia_euclid_{name}.parquet", index=False)
    tile_table = pd.concat(tile_tables, ignore_index=True)
    tile_table.to_csv(folder / "tables" / "tile_calibration.csv", index=False)
    calibration["scatter"].to_csv(folder / "tables" / "displacement_scatter.csv", index=False)
    metrics["tile_calibration"] = {
        "tiles": len(tile_table),
        "baseline_years_min_median_max": [float(v) for v in tile_table["baseline_years"].quantile([0, 0.5, 1])],
        "zero_point_mas_abs_max": float(tile_table[["zero_east_mas", "zero_north_mas"]].abs().to_numpy().max()),
    }
    metrics["displacement_scatter"] = calibration["scatter"].round(2).to_dict("records")
    metrics["displacement_validation"] = validation
    validated = validation["validated_for_compact_sources"]
    metrics["displacement_validated_as_cut"] = bool(validated)

    plot_separation(tables, radius, folder / "figures")
    plot_displacement(tables, calibration["scatter"], folder / "figures")
    plot_photometry_and_compactness(tables, folder / "figures")

    false_rates = {name: round(item["false_match_rates"][str(radius)], 4) for name, item in metrics["fields"].items()}
    fractions = {
        name: round(item["match_fraction_covered_g_17_to_20p5"], 4) for name, item in metrics["fields"].items()
    }
    covered = {name: round(item["covered_fraction"], 4) for name, item in metrics["fields"].items()}
    gates = [
        run_state.gate(
            "false_match_rate",
            f"displaced-position match rate < 1% at the adopted radius ({radius} arcsec)",
            false_rates,
            all(rate < 0.01 for rate in false_rates.values()),
        ),
        run_state.gate(
            "match_fraction",
            "Euclid entry for > 90% of Gaia sources with 17 < G < 20.5 inside the catalogue coverage",
            {"match_fraction_in_coverage": fractions, "covered_fraction_of_field": covered},
            all(value > 0.9 for value in fractions.values()),
            fatal=False,
        ),
        run_state.gate(
            "gaia_id_agreement_reported",
            "agreement with MER gaia_id written (no threshold)",
            {name: [item["mer_gaia_id_equals_source_id"], item["matched"]] for name, item in metrics["fields"].items()},
            True,
        ),
        run_state.gate(
            "displacement_test",
            "movers > 5 sigma recovered >= 90% and false flags <= 5% (else information only)",
            validation,
            validated,
            fatal=False,
        ),
    ]
    run_state.write_summary(config, stage_name, metrics, gates, smoke=arguments.smoke)


if __name__ == "__main__":
    main()
