"""Stage 4: Legacy Surveys DR11 South Tractor entries at the Gaia positions (grz + W1 W2 photometry, morphology).

The Gaia position is the anchor (Legacy imaging has a mean epoch of about 2016.4, so no propagation is needed).
Tractor uses Gaia DR3 as its reference catalogue (`ref_cat = G3`, `ref_id = source_id`), which gives an independent
check of the positional match. Caveat recorded in the outputs: Tractor forces a PSF model for Gaia sources that Gaia's
excess noise marks as point-like, so the Tractor type is not independent of Gaia.

Usage: uv run python -m ucd.stages.stage_4_legacy [--smoke]
Products: stage_4_legacy/tables/gaia_euclid_legacy_<field>.parquet, QA figures, summary.json
"""

import argparse

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from astropy.coordinates import SkyCoord

from ucd.lib import crossmatch, legacy_access, qa_plots, run_state

stage_name = "stage_4_legacy"
candidate_match_radii = [1.0, 0.7, 0.5, 0.3]
positional_magnitude_limit = 23.5
bands = ("g", "r", "i", "z", "w1", "w2")


def add_photometry(legacy: pd.DataFrame) -> pd.DataFrame:
    for band in bands:
        flux = legacy[f"flux_{band}"].astype(float)
        legacy[f"mag_{band}"] = 22.5 - 2.5 * np.log10(flux.where(flux > 0))
        legacy[f"snr_{band}"] = flux * np.sqrt(legacy[f"flux_ivar_{band}"].astype(float).clip(lower=0))
        if f"mw_transmission_{band}" in legacy:
            legacy[f"dered_mag_{band}"] = legacy[f"mag_{band}"] + 2.5 * np.log10(
                legacy[f"mw_transmission_{band}"].astype(float).clip(lower=1e-3)
            )
    legacy["ellipticity_component"] = np.hypot(legacy["shape_e1"].astype(float), legacy["shape_e2"].astype(float))
    return legacy


def match_field(name: str, frame: pd.DataFrame, legacy: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """Tractor entry per Gaia source: by Gaia reference id, else nearest bright entry in a calibrated radius."""
    legacy = legacy[legacy["type"] != "DUP"].reset_index(drop=True)
    anchor = SkyCoord(frame["ra"].to_numpy(), frame["dec"].to_numpy(), unit="deg")
    catalogue = SkyCoord(legacy["ra"].to_numpy(dtype=float), legacy["dec"].to_numpy(dtype=float), unit="deg")
    reference = legacy[legacy["ref_cat"] == "G3"]
    by_id = pd.Series(reference.index.to_numpy(), index=reference["ref_id"].to_numpy(dtype=np.int64))
    by_id = by_id[~by_id.index.duplicated()]
    id_index = frame["source_id"].map(by_id).fillna(-1).astype(np.int64).to_numpy()
    # Positional fallback only among entries bright enough to be a Gaia counterpart (any of g, r, z < 23.5).
    bright = (legacy[["mag_g", "mag_r", "mag_z"]].min(axis=1) < positional_magnitude_limit).to_numpy()
    bright_rows = np.flatnonzero(bright)
    rates = {
        str(radius): crossmatch.displaced_match_fraction(anchor, catalogue[bright_rows], radius)
        for radius in candidate_match_radii
    }
    adopted = next((radius for radius in candidate_match_radii if rates[str(radius)] < 0.01), candidate_match_radii[-1])
    positional = crossmatch.nearest_match(anchor, catalogue[bright_rows], adopted)
    positional_index = np.where(
        positional["catalogue_index"] >= 0, bright_rows[positional["catalogue_index"].clip(lower=0)], -1
    )
    index = np.where(id_index >= 0, id_index, positional_index)
    has_match = index >= 0
    method = np.where(id_index >= 0, "gaia_reference_id", np.where(positional_index >= 0, "position", "none"))
    index = np.clip(index, 0, None)
    separation = anchor.separation(catalogue[index]).arcsec
    around = crossmatch.nearest_match(anchor, catalogue, 1.0)
    matched = pd.DataFrame(
        {
            "separation_arcsec": np.where(has_match, separation, np.nan),
            "matches_in_radius": around["matches_in_radius"].to_numpy(),
            "second_separation_arcsec": around["second_separation_arcsec"].to_numpy(),
        }
    )
    result = frame.copy()
    new_columns = {
        "legacy_matched": has_match,
        "legacy_match_method": method,
        "legacy_separation_arcsec": matched["separation_arcsec"].to_numpy(),
        "legacy_matches_in_radius": matched["matches_in_radius"].to_numpy(),
        "legacy_second_separation_arcsec": matched["second_separation_arcsec"].to_numpy(),
    }
    for column in legacy.columns:
        values = legacy[column].to_numpy()[index]
        if column in ("type", "ref_cat", "brickname"):
            new_columns[f"legacy_{column}"] = np.where(has_match, values, None)
        elif column in ("ref_id", "objid", "brickid", "release", "maskbits", "fitbits"):
            new_columns[f"legacy_{column}"] = np.where(has_match, values.astype(np.int64), -1)
        else:
            new_columns[f"legacy_{column}"] = np.where(has_match, values.astype(float), np.nan)
    result = pd.concat([result, pd.DataFrame(new_columns, index=result.index)], axis=1)
    result["legacy_reference_is_this_gaia_source"] = result["legacy_ref_id"] == result["source_id"]
    for first, second in (("g", "r"), ("r", "z"), ("g", "i"), ("g", "z"), ("z", "w1")):
        result[f"legacy_{first}_minus_{second}"] = result[f"legacy_dered_mag_{first}"] - (
            result[f"legacy_dered_mag_{second}"] if second != "w1" else result["legacy_mag_w1"]
        )
    statistics = {
        "legacy_entries": len(legacy),
        "matched": int(has_match.sum()),
        "match_fraction": float(has_match.mean()),
        "matched_by_gaia_reference_id": int((method == "gaia_reference_id").sum()),
        "matched_by_position": int((method == "position").sum()),
        "positional_radius_arcsec": adopted,
        "positional_false_match_rates": rates,
        "positional_false_match_rate": rates[str(adopted)],
        "median_separation_of_id_matches_arcsec": float(np.nanmedian(separation[method == "gaia_reference_id"])),
        "ambiguous_two_or_more_in_radius": int((result["legacy_matches_in_radius"] > 1).sum()),
        "reference_is_this_gaia_source": int((has_match & result["legacy_reference_is_this_gaia_source"]).sum()),
        "reference_is_other_gaia_source": int(
            (has_match & (result["legacy_ref_cat"] == "G3") & ~result["legacy_reference_is_this_gaia_source"]).sum()
        ),
        "not_a_gaia_reference_entry": int((has_match & (result["legacy_ref_cat"] != "G3")).sum()),
        "types_all": result.loc[has_match, "legacy_type"].value_counts().to_dict(),
        "types_selector_passed": result.loc[has_match & result["selector_selected"], "legacy_type"]
        .value_counts()
        .to_dict(),
        "median_epoch_year": float(
            2000.0 + (np.nanmedian(0.5 * (legacy["mjd_min"] + legacy["mjd_max"])) - 51544.5) / 365.25
        ),
        "median_psf_depth_5_sigma": {
            band: float(
                np.nanmedian(
                    22.5 - 2.5 * np.log10(5 / np.sqrt(legacy[f"psfdepth_{band}"].astype(float).clip(lower=1e-9)))
                )
            )
            for band in ("g", "r", "z")
        },
    }
    return result, statistics


def photometric_offsets(tables: dict) -> dict:
    """Median Legacy total minus MER DECam 2-FWHM aperture magnitude for secure stars (an aperture loss)."""
    combined = pd.concat(tables.values(), ignore_index=True)
    stars = combined[
        combined["legacy_matched"]
        & combined.get("euclid_matched", False)
        & combined["gaia_star_like_motion"]
        & (combined["legacy_type"] == "PSF")
        & combined["phot_g_mean_mag"].between(17.5, 20.0)
    ]
    offsets = {}
    for band in ("g", "r", "i", "z"):
        difference = (stars[f"legacy_mag_{band}"] - stars[f"euclid_decam_{band}_aperture_mag"]).dropna()
        offsets[band] = {
            "stars": len(difference),
            "median": float(difference.median()) if len(difference) else None,
            "scatter": float(1.4826 * (difference - difference.median()).abs().median()) if len(difference) else None,
        }
    return offsets


def compare_with_dr10(config: dict, fornax: pd.DataFrame) -> tuple[dict, pd.DataFrame]:
    dr10 = pd.read_csv(
        run_state.reference_dir(config)
        / "repository/data/literature/catalogs/canonical_legacy_survey_dr10_crossmatch.csv"
    )
    merged = fornax[fornax["legacy_matched"] & fornax["known_object_id"].notna()].merge(
        dr10, left_on="known_object_id", right_on="canonical_object_id", suffixes=("", "_dr10")
    )
    result = {"objects_compared": len(merged)}
    for band in ("g", "r", "z"):
        column = f"{band}_mag"
        if column in merged:
            difference = (merged[f"legacy_mag_{band}"] - merged[column]).dropna()
            result[band] = {
                "median": float(difference.median()),
                "scatter": float(1.4826 * (difference - difference.median()).abs().median()),
            }
    if "type" in merged:
        result["same_type_fraction"] = float((merged["legacy_type"] == merged["type"].astype(str).str.strip()).mean())
    return result, merged


def plot_qa(tables: dict, dr10: pd.DataFrame, folder) -> None:
    figure, axes = plt.subplots(len(tables), 3, figsize=(qa_plots.double_width, 2.6 * len(tables)), squeeze=False)
    for row, (name, frame) in enumerate(tables.items()):
        matched = frame[frame["legacy_matched"]]
        star = matched["gaia_star_like_motion"]
        selected = matched["selector_selected"] & ~star
        known = matched[matched["known_state"] == "confirmed"]
        axes[row, 0].hist(frame["legacy_separation_arcsec"].dropna(), bins=np.linspace(0, 1, 51), color="0.5")
        axes[row, 0].set_yscale("log")
        axes[row, 0].set_xlabel(r"separation Gaia--Legacy (arcsec)")
        axes[row, 0].set_ylabel(rf"{name}: sources")
        axis = axes[row, 1]
        axis.scatter(
            matched.loc[star, "legacy_g_minus_r"],
            matched.loc[star, "legacy_r_minus_z"],
            s=1,
            color=qa_plots.colors["star"],
            rasterized=True,
            label=r"Gaia stars",
        )
        axis.scatter(
            matched.loc[selected, "legacy_g_minus_r"],
            matched.loc[selected, "legacy_r_minus_z"],
            s=1.5,
            color=qa_plots.colors["selected"],
            rasterized=True,
            label=r"selector passed, no motion",
        )
        if len(known):
            axis.scatter(
                known["legacy_g_minus_r"],
                known["legacy_r_minus_z"],
                s=12,
                facecolor="none",
                edgecolor=qa_plots.colors["known"],
                linewidths=0.6,
                label=r"known confirmed",
            )
        axis.set_xlim(-0.5, 2.2)
        axis.set_ylim(-0.6, 2.6)
        axis.set_xlabel(r"$g-r$")
        axis.set_ylabel(r"$r-z$")
        axis.legend(fontsize=6, markerscale=3, frameon=True)
        axis = axes[row, 2]
        for band, color in zip(("g", "r", "z"), ("#4477AA", "#228833", "#CC3311"), strict=True):
            if f"euclid_decam_{band}_aperture_mag" in matched:
                good = star & (matched["legacy_type"] == "PSF")
                axis.scatter(matched.loc[good, f"legacy_mag_{band}"],
                             (matched[f"legacy_mag_{band}"] - matched[f"euclid_decam_{band}_aperture_mag"])[good], s=1,
                             color=color, rasterized=True, label=rf"${band}$")  # fmt: skip
        axis.axhline(0, color="k", lw=0.6)
        axis.set_xlim(15, 23)
        axis.set_ylim(-1, 1)
        axis.set_xlabel(r"Legacy DR11 magnitude (stars)")
        axis.set_ylabel(r"Legacy $-$ MER DECam aperture")
        axis.legend(fontsize=6, markerscale=4)
    figure.tight_layout()
    qa_plots.save(figure, folder, "legacy_match_colours_photometry")

    figure, axes = plt.subplots(1, 2, figsize=(qa_plots.double_width, 2.8))
    if len(dr10):
        for band, color in zip(("g", "r", "z"), ("#4477AA", "#228833", "#CC3311"), strict=True):
            if f"{band}_mag" in dr10:
                axes[0].scatter(
                    dr10[f"{band}_mag"],
                    dr10[f"legacy_mag_{band}"] - dr10[f"{band}_mag"],
                    s=4,
                    color=color,
                    label=rf"${band}$",
                )
        axes[0].axhline(0, color="k", lw=0.6)
        axes[0].set_ylim(-0.6, 0.6)
        axes[0].set_xlabel(r"DR10 magnitude (known Fornax objects, bubbletea)")
        axes[0].set_ylabel(r"DR11 $-$ DR10")
        axes[0].legend(fontsize=6, markerscale=2)
    order = ["PSF", "REX", "EXP", "DEV", "SER"]
    width = 0.25
    groups = []
    for name, frame in tables.items():
        matched = frame[frame["legacy_matched"]]
        groups.append((rf"{name}: Gaia stars", matched[matched["gaia_star_like_motion"]]))
        groups.append(
            (rf"{name}: selector passed", matched[matched["selector_selected"] & ~matched["gaia_star_like_motion"]])
        )
        known = matched[matched["known_state"] == "confirmed"]
        if len(known):
            groups.append((rf"{name}: known confirmed", known))
    width = 0.8 / len(groups)
    for position, (label, group) in enumerate(groups):
        fractions = [float((group["legacy_type"] == kind).mean()) if len(group) else 0 for kind in order]
        axes[1].bar(np.arange(len(order)) + position * width, fractions, width=width, label=label)
    axes[1].set_xticks(np.arange(len(order)) + 0.4 - width / 2)
    axes[1].set_xticklabels(order)
    axes[1].set_ylabel(r"fraction with Tractor type")
    axes[1].legend(fontsize=5.5)
    figure.tight_layout()
    qa_plots.save(figure, folder, "legacy_dr10_comparison_and_types")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    arguments = parser.parse_args()
    config = run_state.load_config()
    summaries = run_state.require_stages(config, ["stage_2_gaia"])
    stage_3 = run_state.run_dir(config) / "stage_3_euclid" / "tables"
    stage_2 = run_state.run_dir(config) / "stage_2_gaia" / "tables"
    fields = run_state.load_fields(config)
    folder = run_state.stage_dir(config, stage_name, smoke=arguments.smoke)
    full_folder = run_state.stage_dir(config, stage_name)

    tables, metrics, notes = {}, {"fields": {}}, []
    for name, field in fields.items():
        path = stage_3 / f"gaia_euclid_{name}.parquet"
        if path.exists():
            frame = pd.read_parquet(path)
        else:
            frame = pd.read_parquet(stage_2 / f"gaia_{name}.parquet")
            notes.append(f"{name}: stage 3 table missing, Legacy match run on the Gaia table only (provisional)")
        legacy = legacy_access.download_cone(
            config,
            field["ra_deg"],
            field["dec_deg"],
            field["radius_deg"],
            full_folder / "tables" / f"legacy_cone_{name}.parquet",
        )
        if arguments.smoke:
            radius = config["smoke_test"]["radius_deg"]
            centre = SkyCoord(field["ra_deg"], field["dec_deg"], unit="deg")
            frame = frame[
                SkyCoord(frame["ra"].to_numpy(), frame["dec"].to_numpy(), unit="deg").separation(centre).deg < radius
            ]
            frame = frame.reset_index(drop=True)
        legacy = add_photometry(legacy.copy())
        tables[name], metrics["fields"][name] = match_field(name, frame, legacy)
        tables[name].to_parquet(folder / "tables" / f"gaia_euclid_legacy_{name}.parquet", index=False)
    metrics["legacy_minus_mer_decam_aperture_stars"] = photometric_offsets(tables)
    metrics["dr11_versus_dr10_known_objects"], dr10 = compare_with_dr10(config, tables["fornax"])
    plot_qa(tables, dr10, folder / "figures")

    false_rates = {name: round(item["positional_false_match_rate"], 4) for name, item in metrics["fields"].items()}
    gates = [
        run_state.gate(
            "false_match_rate",
            "chance-match rate < 1% for the positional fallback at its calibrated radius (id matches have none)",
            false_rates,
            all(rate < 0.01 for rate in false_rates.values()),
        ),
        run_state.gate(
            "reference_id_agreement_reported",
            "Tractor Gaia reference id versus positional match written",
            {
                name: [item["reference_is_this_gaia_source"], item["matched"]]
                for name, item in metrics["fields"].items()
            },
            True,
        ),
        run_state.gate(
            "photometric_offsets_measured",
            "Legacy minus MER DECam offsets measured in g, r, z",
            {band: value["median"] for band, value in metrics["legacy_minus_mer_decam_aperture_stars"].items()},
            all(metrics["legacy_minus_mer_decam_aperture_stars"][band]["stars"] > 20 for band in ("g", "r", "z"))
            or arguments.smoke,
            fatal=False,
        ),
    ]
    del summaries
    run_state.write_summary(config, stage_name, metrics, gates, smoke=arguments.smoke, notes=notes)


if __name__ == "__main__":
    main()
