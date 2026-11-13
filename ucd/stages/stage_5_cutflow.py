"""Stage 5: transparent cut flow from all Gaia sources to UCD candidates, and candidate tiers.

Every criterion is a boolean column on the Gaia-anchored master table; nothing is deleted. Thresholds come from
the frozen Gaia selector, the stage 1 limits (stellar locus, simulated size shift), the stage 3 calibration
(displacement threshold) and reference UCDs outside Fornax (colour box). Known Fornax objects are used only to
report recovery after each cut. Photo-z and the PHZ probabilities are carried as information and never used.

Usage: uv run python -m ucd.stages.stage_5_cutflow
Products: stage_5_cutflow/tables/master_<field>.parquet, candidates_<field>.csv, cutflow.csv, QA figures
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from astropy.coordinates import SkyCoord

from ucd.lib import qa_plots, run_state
from ucd.stages import stage_1_limits

stage_name = "stage_5_cutflow"
parsec_per_arcsec_per_mpc = 4.848137
secure_motion_significance = 5.0
compact_limit = -2.6
maximum_ellipticity = 0.4
minimum_legacy_snr = 5.0
colour_padding = 0.05
galaxy_sequence_quantile = 0.05
tier_names = ("A", "B", "C", "D")
tier_meaning = {
    "A": "all cuts passed, size up to the 95th percentile of reference UCDs",
    "B": "all cuts passed, size between that percentile and 100 pc",
    "C": "Gaia and Euclid size cuts passed, but exactly one of roundness or colour failed",
    "D": "outside Euclid catalogue coverage: Gaia cuts, Legacy colour box and non-PSF Tractor type only",
}
cut_order = [
    ("gaia_selector", "Gaia: frozen selector passed, G in valid range"),
    ("gaia_no_secure_motion", "Gaia: no parallax or proper motion above 5 sigma"),
    ("euclid_available", "Euclid: inside catalogue coverage with an entry at the Gaia position"),
    ("euclid_quality", "Euclid: VIS-detected, not spurious, not saturated, not at a border"),
    ("euclid_not_moving_star", "Euclid: not a compact source displaced since Gaia 2016.0"),
    ("euclid_resolved", "Euclid: less concentrated than 99% of stars at its magnitude"),
    ("euclid_size_in_range", "Euclid: no larger than a 100 pc object at the host distance"),
    ("euclid_round", "Euclid: ellipticity below 0.4"),
    ("legacy_colour", "Legacy: g-r and r-z inside the reference-UCD colour box"),
]


def reference_colour_box(config: dict) -> dict:
    """g-r and r-z range of confirmed UCDs outside Fornax (Virgo, DR10 photometry from bubbletea)."""
    repository = run_state.reference_dir(config) / "repository"
    catalogue = pd.read_csv(repository / "data/literature/validation/canonical_reference_catalog.csv",
                            dtype={"gaia_dr3_ids": str})  # fmt: skip
    legacy = pd.read_csv(repository / "data/literature/catalogs/canonical_legacy_survey_dr10_crossmatch.csv")
    coordinates = SkyCoord(catalogue["ra"].to_numpy(), catalogue["dec"].to_numpy(), unit="deg")
    fornax = config["fields"]["fornax"]
    far_from_fornax = coordinates.separation(SkyCoord(fornax["ra_deg"], fornax["dec_deg"], unit="deg")).deg > 10
    virgo = coordinates.separation(SkyCoord(187.7, 12.4, unit="deg")).deg < 8
    reference = catalogue[far_from_fornax & virgo & (catalogue["classification_state"] == "confirmed")]
    merged = reference.merge(legacy, on="canonical_object_id")
    merged = (
        merged[(merged["ambiguous_match"] == 0) & (merged["r_mag"] < 21.5)] if "ambiguous_match" in merged else merged
    )
    g_minus_r = (merged["g_mag"] - merged["r_mag"]).dropna()
    r_minus_z = (merged["r_mag"] - merged["z_mag"]).dropna()
    return {
        "reference_objects": int(len(merged)),
        "source": "confirmed Virgo objects in bubbletea, Legacy DR10 photometry, not dereddened (E(B-V) ~ 0.02)",
        "g_minus_r": [
            float(g_minus_r.quantile(0.01)) - colour_padding,
            float(g_minus_r.quantile(0.99)) + colour_padding,
        ],
        "r_minus_z": [
            float(r_minus_z.quantile(0.01)) - colour_padding,
            float(r_minus_z.quantile(0.99)) + colour_padding,
        ],
    }


def add_cut_columns(frame: pd.DataFrame, limits: dict) -> pd.DataFrame:
    locus, shift_at_maximum_size, maximum_size_arcsec, box, moving_validated = (
        limits["locus"], limits["shift_at_maximum_size"], limits["maximum_size_arcsec"], limits["colour_box"],
        limits["displacement_validated"],
    )  # fmt: skip
    centres = 0.5 * (locus["ie_low"] + locus["ie_high"]).to_numpy()
    ie_mag = frame["euclid_ie_mag"].to_numpy(dtype=float)
    inside_locus_range = (ie_mag >= locus["ie_low"].min()) & (ie_mag <= locus["ie_high"].max())
    upper = np.interp(ie_mag, centres, locus["mumax_minus_mag_upper"])
    median = np.interp(ie_mag, centres, locus["mumax_minus_mag_median"])
    sersic_upper = np.interp(ie_mag, centres, locus["sersic_radius_arcsec_upper"])
    compactness = frame["euclid_mumax_minus_mag"].to_numpy(dtype=float)
    sersic_radius = frame["euclid_sersic_sersic_vis_radius"].to_numpy(dtype=float)
    quality_flag = frame["euclid_det_quality_flag"].fillna(-1).astype("int64")

    cuts = pd.DataFrame(index=frame.index)
    cuts["gaia_selector"] = frame["selector_selected"] & frame["selector_in_valid_g_range"]
    cuts["gaia_no_secure_motion"] = ~(
        (frame["parallax_significance"] > secure_motion_significance)
        | (frame["proper_motion_zero_significance"] > secure_motion_significance)
    )
    cuts["euclid_available"] = frame["euclid_covered"] & frame["euclid_matched"]
    cuts["euclid_quality"] = (
        (frame["euclid_vis_det"] == 1)
        & (frame["euclid_spurious_flag"] == 0)
        & ((quality_flag & 12) == 0)
        & inside_locus_range
    )
    compact = compactness < compact_limit
    moving = frame["displacement_moving"].fillna(False).astype(bool)
    cuts["euclid_not_moving_star"] = ~(compact & moving) if moving_validated else True
    cuts["euclid_resolved"] = compactness > upper
    size_from_compactness = compactness < median + shift_at_maximum_size
    size_from_sersic = ~(np.isfinite(sersic_radius) & (sersic_radius > maximum_size_arcsec))
    cuts["euclid_size_in_range"] = size_from_compactness & size_from_sersic
    cuts["euclid_round"] = frame["euclid_ellipticity"] < maximum_ellipticity
    good_colour = (
        frame["legacy_matched"]
        & (frame["legacy_snr_g"] > minimum_legacy_snr)
        & (frame["legacy_snr_r"] > minimum_legacy_snr)
        & (frame["legacy_snr_z"] > minimum_legacy_snr)
    )
    cuts["legacy_colour"] = (
        good_colour
        & frame["legacy_g_minus_r"].between(*box["g_minus_r"])
        & frame["legacy_r_minus_z"].between(*box["r_minus_z"])
    )
    result = pd.concat([frame, cuts.add_prefix("cut_").fillna(False).astype(bool)], axis=1)
    result["euclid_compactness_above_stellar_upper"] = compactness - upper
    result["euclid_sersic_above_stellar_upper"] = sersic_radius > sersic_upper
    result["moving_but_extended_information"] = moving & ~compact
    names = [f"cut_{name}" for name, _ in cut_order]
    passed = result[names].to_numpy()
    result["cuts_passed_in_sequence"] = np.where(passed.all(axis=1), len(names), np.argmin(passed, axis=1))
    result["first_failed_cut"] = np.where(
        passed.all(axis=1), "none", np.array([name for name, _ in cut_order])[np.argmin(passed, axis=1)]
    )
    gaia = result["cut_gaia_selector"] & result["cut_gaia_no_secure_motion"]
    euclid_core = (
        result["cut_euclid_available"] & result["cut_euclid_quality"] & result["cut_euclid_not_moving_star"]
        & result["cut_euclid_resolved"] & result["cut_euclid_size_in_range"]
    )  # fmt: skip
    # Size class inside the allowed range: "typical" = up to the 95th percentile of reference UCDs outside Fornax.
    typical = (compactness < median + limits["shift_at_typical_size"]) & ~(
        np.isfinite(sersic_radius) & (sersic_radius > limits["typical_size_arcsec"])
    )
    result["euclid_size_typical"] = typical
    all_cuts = gaia & euclid_core & result["cut_euclid_round"] & result["cut_legacy_colour"]
    tier = np.full(len(result), "", dtype=object)
    tier[gaia & ~result["euclid_covered"] & result["cut_legacy_colour"] & (result["legacy_type"] != "PSF")] = "D"
    tier[gaia & euclid_core & (result["cut_euclid_round"] ^ result["cut_legacy_colour"])] = "C"
    tier[all_cuts & ~typical] = "B"
    tier[all_cuts & typical] = "A"
    result["tier"] = tier
    return result


def galaxy_sequence(control: pd.DataFrame, control_field: dict) -> pd.DataFrame:
    """Lower envelope (5% quantile) of the background-galaxy sequence in compactness versus I_E.

    Measured on the northern half of the control field only, so that the southern half stays an independent
    background sample for objects selected with this envelope.
    """
    north = control["dec"] > control_field["dec_deg"]
    galaxies = control[
        north
        & control["cut_gaia_selector"]
        & control["cut_gaia_no_secure_motion"]
        & control["cut_euclid_available"]
        & control["cut_euclid_quality"]
        & control["cut_euclid_resolved"]
    ]
    rows = []
    edges = np.arange(17.5, 21.01, 0.5)
    for low, high in zip(edges[:-1], edges[1:], strict=True):
        members = galaxies[galaxies["euclid_ie_mag"].between(low, high)]["euclid_mumax_minus_mag"].dropna()
        if len(members) >= 25:
            rows.append(
                {
                    "ie_low": low,
                    "ie_high": high,
                    "galaxies": len(members),
                    "lower_envelope": float(members.quantile(galaxy_sequence_quantile)),
                    "median": float(members.median()),
                }
            )
    return pd.DataFrame(rows)


def add_galaxy_sequence_columns(
    frame: pd.DataFrame, sequence: pd.DataFrame, control_field: dict | None
) -> pd.DataFrame:
    centres = 0.5 * (sequence["ie_low"] + sequence["ie_high"]).to_numpy()
    envelope = np.interp(frame["euclid_ie_mag"].to_numpy(dtype=float), centres, sequence["lower_envelope"])
    frame["euclid_below_galaxy_sequence"] = frame["euclid_mumax_minus_mag"].to_numpy(dtype=float) < envelope
    frame["tier_a_below_galaxy_sequence"] = (frame["tier"] == "A") & frame["euclid_below_galaxy_sequence"]
    if control_field is not None:
        frame["control_half"] = np.where(frame["dec"] > control_field["dec_deg"], "sequence_definition", "evaluation")
    return frame


def cutflow_table(tables: dict, areas: dict) -> pd.DataFrame:
    rows = []
    for name, frame in tables.items():
        alive = pd.Series(True, index=frame.index)
        known = frame["known_state"] == "confirmed"
        rows.append(
            {
                "field": name,
                "step": 0,
                "cut": "all Gaia sources",
                "description": "all Gaia DR3 sources in the field",
                "sources": len(frame),
                "known_confirmed_surviving": int(known.sum()),
                "area_square_deg": areas[name]["field"],
            }
        )
        for step, (cut, description) in enumerate(cut_order, start=1):
            alive &= frame[f"cut_{cut}"]
            rows.append(
                {
                    "field": name,
                    "step": step,
                    "cut": cut,
                    "description": description,
                    "sources": int(alive.sum()),
                    "known_confirmed_surviving": int((alive & known).sum()),
                    "area_square_deg": areas[name]["covered"] if step >= 3 else areas[name]["field"],
                }
            )
    table = pd.DataFrame(rows)
    table["density_per_square_deg"] = table["sources"] / table["area_square_deg"]
    return table


def plot_cutflow(cutflow: pd.DataFrame, folder) -> None:
    figure, axes = plt.subplots(1, 2, figsize=(qa_plots.double_width, 3.4))
    labels = ["all Gaia", "selector", "no secure\nmotion", "Euclid\nentry", "quality", "not moving\nstar", "resolved",
              "size", "round", "colour"]  # fmt: skip
    for name, color in (("fornax", qa_plots.colors["known"]), ("control", qa_plots.colors["control"])):
        rows = cutflow[cutflow["field"] == name]
        axes[0].plot(rows["step"], rows["density_per_square_deg"], marker="o", ms=4, color=color, label=rf"{name}")
        if name == "fornax":
            axes[1].plot(
                rows["step"],
                rows["known_confirmed_surviving"],
                marker="s",
                ms=4,
                color=color,
                label=r"known confirmed (with Gaia source)",
            )
    axes[0].set_yscale("log")
    axes[0].set_ylabel(r"sources per deg$^2$ (effective area)")
    axes[0].legend()
    axes[1].set_ylabel(r"known Fornax objects surviving (verification)")
    axes[1].set_ylim(0, None)
    axes[1].legend()
    for axis in axes:
        axis.set_xticks(range(len(labels)))
        axis.set_xticklabels(labels, rotation=60, ha="right", fontsize=7)
    figure.tight_layout()
    qa_plots.save(figure, folder, "cutflow")


def plot_survivors(tables: dict, limits: dict, folder) -> None:
    locus, box = limits["locus"], limits["colour_box"]
    centres = 0.5 * (locus["ie_low"] + locus["ie_high"])
    figure, axes = plt.subplots(len(tables), 3, figsize=(qa_plots.double_width, 2.6 * len(tables)), squeeze=False)
    for row, (name, frame) in enumerate(tables.items()):
        base = frame[frame["cut_gaia_selector"] & frame["cut_gaia_no_secure_motion"] & frame["cut_euclid_available"]
                     & frame["cut_euclid_quality"]]  # fmt: skip
        groups = [
            (base, qa_plots.colors["all"], 1.5, r"Gaia + Euclid quality"),
            (frame[frame["tier"] == "C"], qa_plots.colors["galaxy"], 4, r"tier C"),
            (frame[frame["tier"] == "B"], qa_plots.colors["selected"], 8, r"tier B"),
            (frame[frame["tier"] == "A"], qa_plots.colors["candidate"], 10, r"tier A"),
        ]
        known = frame[(frame["known_state"] == "confirmed") & frame["euclid_matched"]]
        panels = [("euclid_ie_mag", "euclid_mumax_minus_mag"), ("euclid_ie_mag", "euclid_sersic_sersic_vis_radius"),
                  ("legacy_g_minus_r", "legacy_r_minus_z")]  # fmt: skip
        for column, (x_name, y_name) in enumerate(panels):
            axis = axes[row, column]
            for subset, color, size, label in groups:
                axis.scatter(subset[x_name], subset[y_name], s=size, color=color, rasterized=True, label=label)
            if len(known):
                axis.scatter(
                    known[x_name],
                    known[y_name],
                    s=22,
                    facecolor="none",
                    edgecolor=qa_plots.colors["known"],
                    linewidths=0.6,
                    label=r"known confirmed",
                )
        axes[row, 0].plot(centres, locus["mumax_minus_mag_upper"], color="k", lw=0.8)
        axes[row, 0].plot(
            0.5 * (limits["sequence"]["ie_low"] + limits["sequence"]["ie_high"]),
            limits["sequence"]["lower_envelope"],
            color=qa_plots.colors["control"],
            lw=1.0,
        )
        axes[row, 0].plot(
            centres, locus["mumax_minus_mag_median"] + limits["shift_at_maximum_size"], color="k", lw=0.8, ls="--"
        )
        axes[row, 0].plot(
            centres, locus["mumax_minus_mag_median"] + limits["shift_at_typical_size"], color="k", lw=0.8, ls=":"
        )
        axes[row, 0].set_xlim(17.3, 22.2)
        axes[row, 0].set_ylim(-3.4, 0.5)
        axes[row, 0].set_xlabel(r"$I_{\rm E}$ (mag)")
        axes[row, 0].set_ylabel(rf"{name}: $\mu_{{\rm max}}-{{\rm mag}}$")
        axes[row, 1].axhline(limits["maximum_size_arcsec"], color="k", lw=0.8, ls="--")
        axes[row, 1].plot(centres, locus["sersic_radius_arcsec_upper"], color="k", lw=0.8)
        axes[row, 1].set_yscale("log")
        axes[row, 1].set_xlim(17.3, 22.2)
        axes[row, 1].set_ylim(5e-3, 5)
        axes[row, 1].set_xlabel(r"$I_{\rm E}$ (mag)")
        axes[row, 1].set_ylabel(r"S\'ersic radius (arcsec)")
        g_low, g_high = box["g_minus_r"]
        z_low, z_high = box["r_minus_z"]
        axes[row, 2].plot(
            [g_low, g_high, g_high, g_low, g_low], [z_low, z_low, z_high, z_high, z_low], color="k", lw=0.8
        )
        axes[row, 2].set_xlim(-0.3, 2.0)
        axes[row, 2].set_ylim(-0.4, 1.6)
        axes[row, 2].set_xlabel(r"$g-r$")
        axes[row, 2].set_ylabel(r"$r-z$")
    axes[0, 0].legend(fontsize=6, markerscale=1.2, frameon=True, loc="upper left")
    figure.tight_layout()
    qa_plots.save(figure, folder, "survivors_size_colour")


def explain_known_misses(frame: pd.DataFrame) -> pd.DataFrame:
    """One line per known confirmed object with a Gaia source: where it left the cut flow and the measured values."""
    known = frame[frame["known_state"] == "confirmed"]
    columns = [
        "known_object_id", "phot_g_mean_mag", "known_half_light_radius_pc", "selector_probability",
        "parallax_significance", "proper_motion_zero_significance", "euclid_covered", "euclid_matched",
        "euclid_ie_mag", "euclid_mumax_minus_mag", "euclid_compactness_above_stellar_upper",
        "euclid_sersic_sersic_vis_radius", "euclid_ellipticity", "euclid_det_quality_flag",
        "displacement_significance", "legacy_g_minus_r", "legacy_r_minus_z", "legacy_type", "first_failed_cut", "tier",
    ]  # fmt: skip
    return known[columns].sort_values("first_failed_cut")


def main() -> None:
    config = run_state.load_config()
    summaries = run_state.require_stages(config, ["stage_1_limits", "stage_3_euclid", "stage_4_legacy"])
    folder = run_state.stage_dir(config, stage_name)
    stage_1 = run_state.run_dir(config) / "stage_1_limits" / "tables"
    stage_4 = run_state.run_dir(config) / "stage_4_legacy" / "tables"
    fields = run_state.load_fields(config)
    locus = pd.read_csv(stage_1 / "stellar_locus.csv")
    simulation = pd.read_csv(stage_1 / "compactness_simulation.csv")
    king = simulation[simulation["profile"] == "king_c30"]
    definition = config["ucd_definition"]
    host_distance = fields["fornax"]["host_distance_mpc"]
    maximum_size_arcsec = definition["maximum_half_light_radius_pc"] / (host_distance * parsec_per_arcsec_per_mpc)
    population = stage_1_limits.load_population(config)
    reference = population[
        ~population["in_fornax"]
        & (population["half_light_radius_pc"] >= definition["minimum_half_light_radius_pc"])
        & (population["absolute_v"] <= definition["maximum_absolute_v_magnitude"])
    ]
    typical_size_pc = float(reference["half_light_radius_pc"].quantile(0.95))
    typical_size_arcsec = typical_size_pc / (host_distance * parsec_per_arcsec_per_mpc)
    limits = {
        "typical_size_pc": typical_size_pc,
        "typical_size_reference_objects": len(reference),
        "typical_size_arcsec": typical_size_arcsec,
        "shift_at_typical_size": float(
            np.interp(typical_size_arcsec, king["half_light_radius_arcsec"], king["shift_from_point_source"])
        ),
        "locus": locus,
        "maximum_size_arcsec": maximum_size_arcsec,
        "shift_at_maximum_size": float(
            np.interp(maximum_size_arcsec, king["half_light_radius_arcsec"], king["shift_from_point_source"])
        ),
        "colour_box": reference_colour_box(config),
        "displacement_validated": bool(summaries["stage_3_euclid"]["metrics"]["displacement_validated_as_cut"]),
    }

    tables, areas, metrics = {}, {}, {"fields": {}}
    for name in fields:
        tables[name] = add_cut_columns(pd.read_parquet(stage_4 / f"gaia_euclid_legacy_{name}.parquet"), limits)
    sequence = galaxy_sequence(tables["control"], fields["control"])
    sequence.to_csv(folder / "tables" / "galaxy_sequence.csv", index=False)
    for name, field in fields.items():
        frame = add_galaxy_sequence_columns(tables[name], sequence, fields["control"] if name == "control" else None)
        tables[name] = frame
        frame.to_parquet(folder / "tables" / f"master_{name}.parquet", index=False)
        field_area = np.pi * field["radius_deg"] ** 2
        areas[name] = {"field": field_area, "covered": field_area * float(frame["euclid_covered"].mean())}
        candidates = frame[frame["tier"] != ""].sort_values(["tier", "euclid_ie_mag"])
        candidates.to_csv(folder / "tables" / f"candidates_{name}.csv", index=False)
        tiers = frame["tier"].value_counts().to_dict()
        new = frame[(frame["tier"] != "") & frame["known_object_id"].isna()]
        metrics["fields"][name] = {
            "effective_area_square_deg": areas[name],
            "tiers": {tier: int(tiers.get(tier, 0)) for tier in tier_names},
            "tier_a_below_galaxy_sequence": int(frame["tier_a_below_galaxy_sequence"].sum()),
            "tiers_not_in_known_catalogue": {tier: int((new["tier"] == tier).sum()) for tier in tier_names},
            "tier_a_density_per_square_deg": float(tiers.get("A", 0) / areas[name]["covered"]),
            "tier_b_density_per_square_deg": float(tiers.get("B", 0) / areas[name]["covered"]),
            "moving_but_extended_information": int(
                (frame["moving_but_extended_information"] & (frame["tier"] != "")).sum()
            ),
        }
    cutflow = cutflow_table(tables, areas)
    cutflow.to_csv(folder / "tables" / "cutflow.csv", index=False)
    plot_cutflow(cutflow, folder / "figures")
    limits["sequence"] = sequence
    plot_survivors(tables, limits, folder / "figures")
    misses = explain_known_misses(tables["fornax"])
    misses.to_csv(folder / "tables" / "known_confirmed_cut_report.csv", index=False)

    fornax = tables["fornax"]
    known = fornax[fornax["known_state"] == "confirmed"]
    known_euclid = known[known["cut_euclid_available"]]
    recovery = {
        "known_confirmed_with_gaia_source": len(known),
        "of_those_with_euclid_entry": len(known_euclid),
        "tier_a": int((known["tier"] == "A").sum()),
        "tier_a_below_galaxy_sequence": int(known["tier_a_below_galaxy_sequence"].sum()),
        "tier_b": int((known["tier"] == "B").sum()),
        "tier_c": int((known["tier"] == "C").sum()),
        "tier_d_no_euclid_coverage": int((known["tier"] == "D").sum()),
        "first_failed_cut_counts": known["first_failed_cut"].value_counts().to_dict(),
        "rejected_class_objects_reaching_tier_a_or_b": int(
            ((fornax["known_state"] == "rejected") & fornax["tier"].isin(["A", "B"])).sum()
        ),
        "rejected_class_objects_with_gaia_and_euclid": int(
            ((fornax["known_state"] == "rejected") & fornax["cut_euclid_available"]).sum()
        ),
    }
    metrics["known_object_recovery_verification"] = recovery
    control = tables["control"]
    evaluation = control[control["control_half"] == "evaluation"]
    half_area = 0.5 * areas["control"]["covered"]
    metrics["galaxy_sequence"] = {
        "definition": "5% quantile of mu_max - mag per I_E bin; selector-passed resolved sources; north control half",
        "bins": sequence.round(3).to_dict("records"),
        "control_evaluation_half_area_square_deg": half_area,
        "control_evaluation_half_tier_a": int((evaluation["tier"] == "A").sum()),
        "control_evaluation_half_tier_a_below_sequence": int(evaluation["tier_a_below_galaxy_sequence"].sum()),
        "status": "information column and sub-tier only; not a cut in this run",
    }
    metrics["limits_used"] = {
        "maximum_size_arcsec": maximum_size_arcsec,
        "compactness_shift_at_maximum_size": limits["shift_at_maximum_size"],
        "typical_size_pc": typical_size_pc,
        "typical_size_arcsec": typical_size_arcsec,
        "typical_size_reference_objects": len(reference),
        "tier_meaning": tier_meaning,
        "colour_box": limits["colour_box"],
        "displacement_cut_applied": limits["displacement_validated"],
        "euclid_colour_cut": "not applied: no reference UCD sample with Euclid photometry outside Fornax",
    }
    metrics["cutflow"] = cutflow[["field", "step", "cut", "sources", "known_confirmed_surviving"]].to_dict("records")
    final = cutflow[cutflow["step"] == len(cut_order)].set_index("field")["density_per_square_deg"]
    start = cutflow[cutflow["step"] == 1].set_index("field")["density_per_square_deg"]
    reduction = float(start["control"] / max(final["control"], 1e-9))
    gates = [
        run_state.gate(
            "contamination_reduction_measured",
            "control-field density after the Gaia selector and after all cuts",
            {
                "after_selector_per_deg2": round(float(start["control"]), 1),
                "after_all_cuts_per_deg2": round(float(final["control"]), 2),
                "reduction_factor": round(reduction, 1),
            },
            True,
        ),
        run_state.gate(
            "known_recovery_reported",
            "recovery per cut written, every known object has a first failed cut",
            recovery,
            True,
        ),
        run_state.gate(
            "candidates_written",
            "candidate tables written for both fields",
            {name: item["tiers"] for name, item in metrics["fields"].items()},
            True,
        ),
    ]
    run_state.write_summary(config, stage_name, metrics, gates)


if __name__ == "__main__":
    main()
