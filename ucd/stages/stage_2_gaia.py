"""Stage 2: retrieve every Gaia source in the fields and score it with bubbletea's frozen selector.

Usage: uv run python -m ucd.stages.stage_2_gaia [--smoke]
Products: stage_2_gaia/tables/gaia_<field>.parquet, QA figures, summary.json
"""

import argparse

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from astropy.coordinates import SkyCoord

from ucd.lib import crossmatch, gaia_access, qa_plots, run_state, selector

stage_name = "stage_2_gaia"
significance_limit = 3.0
latitude_band_edges = [20.0, 28.27, 37.24, 47.46, 60.27, 90.0]  # bubbletea large-sky grid, equal-area |b| bands


def add_flags(frame: pd.DataFrame) -> pd.DataFrame:
    """Simple, transparent flags computed next to the frozen score (comparison and later cuts)."""
    g = frame["phot_g_mean_mag"]
    frame["has_five_parameter_astrometry"] = frame["parallax"].notna() & frame["pmra"].notna()
    frame["parallax_significance"] = frame["parallax"] / frame["parallax_error"]
    frame["significant_parallax"] = frame["parallax_significance"] > significance_limit
    frame["significant_proper_motion"] = frame["proper_motion_zero_significance"] > significance_limit
    frame["gaia_star_like_motion"] = frame["significant_parallax"] | frame["significant_proper_motion"]
    # Voggel et al. 2020 (ApJ 899, 140) 98th-percentile stellar boundaries; comparison only.
    frame["voggel_excess_noise_boundary"] = 0.12 + 2.66e-6 * np.exp(0.7 * g)
    frame["voggel_bp_rp_excess_boundary"] = 1.39 + 2.18e-7 * np.exp(0.76 * g)
    component_significance = np.maximum(
        (frame["pmra"] / frame["pmra_error"]).abs(), (frame["pmdec"] / frame["pmdec_error"]).abs()
    )
    no_motion = ~((frame["parallax_significance"] >= 4) | (component_significance >= 4))
    frame["voggel_style_selected"] = (
        (g < 19)
        & no_motion
        & (frame["astrometric_excess_noise"] > frame["voggel_excess_noise_boundary"])
        & (frame["phot_bp_rp_excess_factor"] > frame["voggel_bp_rp_excess_boundary"])
        & frame["bp_rp"].between(0.6, 1.6)
    )
    return frame


def attach_known_objects(frame: pd.DataFrame, known: pd.DataFrame, radius_arcsec: float = 0.5) -> pd.DataFrame:
    """Link Gaia sources to known Fornax objects by position (verification bookkeeping only)."""
    gaia_coordinates = SkyCoord(frame["ra"].to_numpy(), frame["dec"].to_numpy(), unit="deg")
    known_coordinates = SkyCoord(known["ra"].to_numpy(), known["dec"].to_numpy(), unit="deg")
    matched = crossmatch.nearest_match(gaia_coordinates, known_coordinates, radius_arcsec)
    has_match = matched["catalogue_index"] >= 0
    index = matched["catalogue_index"].where(has_match, 0).to_numpy()
    frame["known_object_id"] = np.where(has_match, known["canonical_object_id"].to_numpy()[index], None)
    frame["known_state"] = np.where(has_match, known["classification_state"].to_numpy()[index], None)
    frame["known_half_light_radius_pc"] = np.where(has_match, known["half_light_radius_pc"].to_numpy()[index], np.nan)
    frame["known_separation_arcsec"] = matched["separation_arcsec"].to_numpy()
    return frame


def bubbletea_density_range(config: dict, galactic_latitude_deg: float) -> dict:
    summary = pd.read_csv(
        run_state.reference_dir(config)
        / "repository/data/results/background/large_sky_development_scale_summary_v1.csv"
    )
    band = np.digitize(abs(galactic_latitude_deg), latitude_band_edges) - 1
    low, high = latitude_band_edges[band], latitude_band_edges[band + 1]
    rows = summary[summary["galactic_latitude_deg"].abs().between(low, high)]
    density = rows["selected_source_density_per_square_deg"].dropna()
    return {
        "band_abs_latitude_deg": [low, high],
        "fields": len(density),
        "median": float(density.median()),
        "range_68": [float(density.quantile(0.16)), float(density.quantile(0.84))],
        "range_95": [float(density.quantile(0.025)), float(density.quantile(0.975))],
    }


def plot_colour_magnitude(tables: dict, folder) -> None:
    figure, axes = plt.subplots(1, len(tables), figsize=(qa_plots.double_width, 3.4), sharey=True)
    for axis, (name, frame) in zip(np.atleast_1d(axes), tables.items(), strict=True):
        selected = frame[frame["selector_selected"]]
        axis.scatter(
            frame["bp_rp"],
            frame["phot_g_mean_mag"],
            s=1,
            color=qa_plots.colors["all"],
            rasterized=True,
            label=rf"all Gaia ({len(frame)})",
        )
        axis.scatter(
            selected["bp_rp"],
            selected["phot_g_mean_mag"],
            s=2.5,
            color=qa_plots.colors["selected"],
            rasterized=True,
            label=rf"selector passed ({len(selected)})",
        )
        known = frame[frame["known_state"] == "confirmed"]
        if len(known):
            axis.scatter(
                known["bp_rp"],
                known["phot_g_mean_mag"],
                s=14,
                facecolor="none",
                edgecolor=qa_plots.colors["known"],
                linewidths=0.7,
                label=rf"known confirmed ({len(known)})",
            )
        axis.set_xlim(-0.6, 3.6)
        axis.set_ylim(21.6, 11)
        axis.set_xlabel(r"$G_{\rm BP}-G_{\rm RP}$")
        axis.set_title(rf"{name}")
        axis.legend(loc="upper right", frameon=True, framealpha=0.9, markerscale=2)
    np.atleast_1d(axes)[0].set_ylabel(r"$G$ (mag)")
    qa_plots.save(figure, folder, "gaia_colour_magnitude")


def plot_features(tables: dict, folder) -> None:
    features = [
        ("astrometric_excess_noise", r"astrometric excess noise (mas)", True),
        ("phot_bp_rp_excess_factor", r"BP/RP excess factor", True),
        ("ruwe", r"RUWE", True),
        ("selector_probability", r"frozen selector probability", False),
    ]
    figure, axes = plt.subplots(
        len(tables), len(features), figsize=(qa_plots.double_width, 2.1 * len(tables) + 0.5), sharex=True, squeeze=False
    )
    for row, (name, frame) in enumerate(tables.items()):
        selected = frame[frame["selector_selected"]]
        known = frame[frame["known_state"] == "confirmed"]
        for column, (feature, label, log_scale) in enumerate(features):
            axis = axes[row, column]
            values = frame[feature].clip(lower=1e-3) if log_scale else frame[feature]
            axis.scatter(frame["phot_g_mean_mag"], values, s=0.6, color=qa_plots.colors["all"], rasterized=True)
            selected_values = selected[feature].clip(lower=1e-3) if log_scale else selected[feature]
            axis.scatter(
                selected["phot_g_mean_mag"], selected_values, s=1.2, color=qa_plots.colors["selected"], rasterized=True
            )
            if len(known):
                known_values = known[feature].clip(lower=1e-3) if log_scale else known[feature]
                axis.scatter(
                    known["phot_g_mean_mag"],
                    known_values,
                    s=10,
                    facecolor="none",
                    edgecolor=qa_plots.colors["known"],
                    linewidths=0.6,
                )
            if log_scale:
                axis.set_yscale("log")
            if feature == "astrometric_excess_noise":
                grid = np.linspace(14, 21, 50)
                axis.plot(grid, 0.12 + 2.66e-6 * np.exp(0.7 * grid), color="k", lw=0.8, ls="--")
            if feature == "phot_bp_rp_excess_factor":
                grid = np.linspace(14, 21, 50)
                axis.plot(grid, 1.39 + 2.18e-7 * np.exp(0.76 * grid), color="k", lw=0.8, ls="--")
                axis.set_ylim(0.9, 30)
            if row == len(tables) - 1:
                axis.set_xlabel(r"$G$ (mag)")
            if row == 0:
                axis.set_title(label, fontsize=8)
            if column == 0:
                axis.set_ylabel(rf"{name}")
            axis.set_xlim(13, 21.5)
    figure.suptitle(
        r"grey: all; orange: selector passed; red circles: known confirmed; dashed: Voggel+20 boundary",
        fontsize=8,
        y=1.0,
    )
    figure.tight_layout()
    qa_plots.save(figure, folder, "gaia_features")


def plot_sky(tables: dict, fields: dict, folder) -> None:
    figure, axes = plt.subplots(1, len(tables), figsize=(qa_plots.double_width, 3.6), squeeze=False)
    for axis, (name, frame) in zip(axes[0], tables.items(), strict=True):
        field = fields[name]
        cos_dec = np.cos(np.radians(field["dec_deg"]))
        x = (frame["ra"] - field["ra_deg"]) * cos_dec
        y = frame["dec"] - field["dec_deg"]
        selected = frame["selector_selected"]
        axis.scatter(x, y, s=0.4, color=qa_plots.colors["all"], rasterized=True)
        axis.scatter(x[selected], y[selected], s=2.5, color=qa_plots.colors["selected"], rasterized=True)
        known = frame["known_state"] == "confirmed"
        if known.any():
            axis.scatter(x[known], y[known], s=12, facecolor="none", edgecolor=qa_plots.colors["known"], linewidths=0.6)
        limit = 1.05 * field["radius_deg"]
        axis.set_xlim(limit, -limit)
        axis.set_ylim(-limit, limit)
        axis.set_aspect("equal")
        axis.set_xlabel(r"$\Delta{\rm RA}\cos\delta$ (deg)")
        axis.set_title(rf"{name}: {int(selected.sum())} selected of {len(frame)}")
    axes[0, 0].set_ylabel(r"$\Delta{\rm Dec}$ (deg)")
    qa_plots.save(figure, folder, "gaia_sky_selected")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    arguments = parser.parse_args()
    config = run_state.load_config()
    run_state.require_stages(config, ["stage_0_preflight"])
    fields = run_state.load_fields(config)
    if arguments.smoke:
        fields = run_state.smoke_fields(config, fields)
    folder = run_state.stage_dir(config, stage_name, smoke=arguments.smoke)
    reference = run_state.reference_dir(config)
    model = selector.FrozenSelector(
        reference / "repository/data/literature/validation/point_source_logistic_model_v1.json"
    )
    known = pd.read_parquet(reference / "fornax_reference.parquet")

    tables, metrics = {}, {"fields": {}}
    for name, field in fields.items():
        print(f"retrieving Gaia sources for {name}")
        frame = gaia_access.retrieve_cone(config, field["ra_deg"], field["dec_deg"], field["radius_deg"])
        frame = add_flags(model.score(frame))
        frame = attach_known_objects(frame, known)
        frame["field"] = name
        frame.to_parquet(folder / "tables" / f"gaia_{name}.parquet", index=False)
        tables[name] = frame
        area = np.pi * field["radius_deg"] ** 2
        selected = frame["selector_selected"]
        metrics["fields"][name] = {
            "rows": len(frame),
            "area_square_deg": area,
            "selected": int(selected.sum()),
            "selected_density_per_square_deg": float(selected.sum() / area),
            "selected_outside_valid_g_range": int((selected & ~frame["selector_in_valid_g_range"]).sum()),
            "selected_without_five_parameter_astrometry": int(
                (selected & ~frame["has_five_parameter_astrometry"]).sum()
            ),
            "voggel_style_selected": int(frame["voggel_style_selected"].sum()),
            "selected_and_voggel_style": int((selected & frame["voggel_style_selected"]).sum()),
            "g_magnitude_percentiles_5_50_95": [float(v) for v in frame["phot_g_mean_mag"].quantile([0.05, 0.5, 0.95])],
            "duplicate_source_ids": int(frame["source_id"].duplicated().sum()),
        }

    plot_colour_magnitude(tables, folder / "figures")
    plot_features(tables, folder / "figures")
    plot_sky(tables, fields, folder / "figures")

    target = tables["fornax"]
    target_field = fields["fornax"]
    known_coordinates = SkyCoord(known["ra"].to_numpy(), known["dec"].to_numpy(), unit="deg")
    centre = SkyCoord(target_field["ra_deg"], target_field["dec_deg"], unit="deg")
    known_in_field = known[known_coordinates.separation(centre).deg < target_field["radius_deg"]]
    recovery = {}
    for state in ("confirmed", "candidate", "rejected"):
        members = known_in_field[known_in_field["classification_state"] == state]
        linked = target[target["known_object_id"].isin(members["canonical_object_id"])]
        recovery[state] = {
            "known_in_field": len(members),
            "with_gaia_source_within_0p5_arcsec": int(linked["known_object_id"].nunique()),
            "selector_passed": int(linked[linked["selector_selected"]]["known_object_id"].nunique()),
            "voggel_style_passed": int(linked[linked["voggel_style_selected"]]["known_object_id"].nunique()),
        }
    metrics["known_object_recovery_consistency_check"] = recovery

    control_metrics = metrics["fields"]["control"]
    background = bubbletea_density_range(config, fields["control"].get("galactic_latitude_deg", -54.0))
    metrics["bubbletea_random_field_density"] = background
    density = control_metrics["selected_density_per_square_deg"]
    gates = [
        run_state.gate(
            "row_counts",
            "retrieved rows equal the count query (enforced in retrieval)",
            {name: item["rows"] for name, item in metrics["fields"].items()},
            True,
        ),
        run_state.gate(
            "unique_source_ids",
            "no duplicate source_id",
            {name: item["duplicate_source_ids"] for name, item in metrics["fields"].items()},
            all(item["duplicate_source_ids"] == 0 for item in metrics["fields"].values()),
        ),
        run_state.gate(
            "control_density_vs_bubbletea",
            "control-field selected density inside bubbletea's 95% range",
            {"control_density": round(density, 1), "bubbletea_range_95": background["range_95"]},
            arguments.smoke or background["range_95"][0] <= density <= background["range_95"][1],
            fatal=False,
        ),
        run_state.gate("known_recovery_reported", "recovery of known objects written (no threshold)", recovery, True),
    ]
    run_state.write_summary(config, stage_name, metrics, gates, smoke=arguments.smoke)


if __name__ == "__main__":
    main()
