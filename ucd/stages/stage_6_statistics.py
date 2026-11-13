"""Stage 6: spatial distribution of the candidates around the host and its statistical significance.

Effective area comes from the Euclid catalogue itself (random points with a catalogue entry within 20 arcsec; the
tile-polygon footprint overestimates coverage). The background is the control field, with a Poisson (gamma) term
and a field-to-field term measured from cells of the control field. A null result passes this stage.

Usage: uv run python -m ucd.stages.stage_6_statistics
Products: stage_6_statistics/tables/radial_profile.csv, excess_summary.json, QA figures, summary.json
"""

import astropy.units as u
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from astropy.coordinates import SkyCoord
from scipy import stats

from ucd.lib import qa_plots, run_state

stage_name = "stage_6_statistics"
coverage_radius_arcsec = 20.0
random_points = 150000
annulus_edges_arcmin = np.array([0, 3, 6, 9, 12, 16, 20, 25, 30, 40, 50, 60])
kpc_per_arcmin_per_mpc = 0.29089
systematic_fraction_default = 0.18  # bubbletea field-to-field factor for Gaia-selected densities
monte_carlo_draws = 200000
samples = {
    "tier_a": "tier A (all cuts, typical size)",
    "tier_a_below_galaxy_sequence": "tier A below the galaxy sequence",
    "tier_a_or_b": "tier A or B (all cuts, up to 100 pc)",
}


def load_cone(config: dict, name: str) -> SkyCoord:
    folder = run_state.run_dir(config) / "stage_3_euclid" / "tables" / f"cone_{name}"
    cone = pd.concat(
        [pd.read_parquet(path, columns=["right_ascension", "declination"]) for path in sorted(folder.glob("*.parquet"))]
    )
    return SkyCoord(cone["right_ascension"].to_numpy(), cone["declination"].to_numpy(), unit="deg")


def random_coverage(field: dict, catalogue: SkyCoord, rng: np.random.Generator) -> pd.DataFrame:
    """Uniform random points in the field with a flag for catalogue coverage."""
    centre = SkyCoord(field["ra_deg"], field["dec_deg"], unit="deg")
    radius = field["radius_deg"] * np.sqrt(rng.uniform(size=random_points))
    angle = rng.uniform(0, 2 * np.pi, size=random_points)
    points = centre.spherical_offsets_by(radius * np.cos(angle) * u.deg, radius * np.sin(angle) * u.deg)
    index, _, _, _ = catalogue.search_around_sky(points, coverage_radius_arcsec * u.arcsec)
    covered = np.bincount(index, minlength=random_points) > 0
    east, north = centre.spherical_offsets_to(points)
    return pd.DataFrame(
        {"east_deg": east.deg, "north_deg": north.deg, "radius_deg": points.separation(centre).deg, "covered": covered}
    )


def grid_coverage_fraction(field: dict, catalogue: SkyCoord, cell_arcsec: float = 30.0) -> float:
    """Independent coverage estimate: fraction of 30 arcsec grid cells in the field that contain a catalogue entry."""
    centre = SkyCoord(field["ra_deg"], field["dec_deg"], unit="deg")
    east, north = centre.spherical_offsets_to(catalogue)
    cells = int(2 * field["radius_deg"] * 3600 / cell_arcsec)
    edges = np.linspace(-field["radius_deg"], field["radius_deg"], cells + 1)
    occupied, _, _ = np.histogram2d(east.deg, north.deg, bins=[edges, edges])
    middle = 0.5 * (edges[:-1] + edges[1:])
    grid_east, grid_north = np.meshgrid(middle, middle, indexing="ij")
    inside = np.hypot(grid_east, grid_north) < field["radius_deg"] - cell_arcsec / 3600
    return float((occupied[inside] > 0).mean())


def sample_mask(frame: pd.DataFrame, sample: str) -> pd.Series:
    if sample == "tier_a":
        return frame["tier"] == "A"
    if sample == "tier_a_below_galaxy_sequence":
        return frame["tier_a_below_galaxy_sequence"]
    return frame["tier"].isin(["A", "B"])


def control_background(control: pd.DataFrame, coverage: pd.DataFrame, field_area: float, sample: str) -> dict:
    """Background density with its Poisson posterior and the cell-to-cell dispersion in the control field."""
    mask = sample_mask(control, sample)
    usable = pd.Series(True, index=control.index)
    area_fraction = float(coverage["covered"].mean())
    if sample == "tier_a_below_galaxy_sequence":  # only the half not used to define the sequence
        usable = control["control_half"] == "evaluation"
        area_fraction = float((coverage["covered"] & (coverage["north_deg"] <= 0)).mean())
    count = int((mask & usable).sum())
    area = field_area * area_fraction
    centre_dec = control["dec"].mean()
    cell_counts, cell_areas = [], []
    east = (control["ra"] - control["ra"].mean()) * np.cos(np.radians(centre_dec))
    north = control["dec"] - centre_dec
    angle_sources = np.degrees(np.arctan2(north, east)) % 360
    angle_random = np.degrees(np.arctan2(coverage["north_deg"], coverage["east_deg"])) % 360
    sectors = (
        [(180, 225), (225, 270), (270, 315), (315, 360)]
        if sample == "tier_a_below_galaxy_sequence"
        else [(start, start + 45) for start in range(0, 360, 45)]
    )
    for low, high in sectors:
        cell_counts.append(int((mask & usable & (angle_sources >= low) & (angle_sources < high)).sum()))
        cell_areas.append(
            field_area * float((coverage["covered"] & (angle_random >= low) & (angle_random < high)).mean())
        )
    cell_counts, cell_areas = np.array(cell_counts), np.array(cell_areas)
    expected = count * cell_areas / cell_areas.sum()
    chi_square = float(((cell_counts - expected) ** 2 / np.maximum(expected, 1e-9)).sum())
    dispersion = chi_square / (len(sectors) - 1)
    extra_fraction = float(np.sqrt(max(dispersion - 1, 0) / max(expected.mean(), 1e-9)))
    return {
        "count": count,
        "area_square_deg": area,
        "density_per_square_deg": count / area,
        "density_interval_68": [float(stats.gamma.ppf(q, count + 0.5) / area) for q in (0.16, 0.84)],
        "cell_counts": cell_counts.tolist(),
        "cell_dispersion_index": dispersion,
        "extra_fraction_from_cells": extra_fraction,
        "systematic_fraction_used": max(extra_fraction, systematic_fraction_default),
    }


def excess_significance(observed: int, area: float, background: dict, rng: np.random.Generator) -> dict:
    """Probability of at least `observed` objects from background alone, marginalised over its uncertainty."""
    density = rng.gamma(background["count"] + 0.5, 1.0 / background["area_square_deg"], size=monte_carlo_draws)
    density *= rng.lognormal(0.0, background["systematic_fraction_used"], size=monte_carlo_draws)
    expected = density * area
    p_value = float(np.mean(stats.poisson.sf(observed - 1, expected))) if observed > 0 else 1.0
    p_value = max(p_value, 1e-16)  # numerical floor: reported significances saturate near 8.2 sigma
    return {
        "observed": int(observed),
        "expected_background": float(np.median(expected)),
        "expected_interval_68": [float(np.quantile(expected, 0.16)), float(np.quantile(expected, 0.84))],
        "excess": float(observed - np.median(expected)),
        "p_value": p_value,
        "gaussian_sigma": float(stats.norm.isf(p_value)),
    }


def radial_profile(fornax: pd.DataFrame, coverage: pd.DataFrame, field: dict, backgrounds: dict, rng) -> pd.DataFrame:
    centre = SkyCoord(field["ra_deg"], field["dec_deg"], unit="deg")
    radius_arcmin = SkyCoord(fornax["ra"].to_numpy(), fornax["dec"].to_numpy(), unit="deg").separation(centre).arcmin
    field_area = np.pi * field["radius_deg"] ** 2
    known = (fornax["known_state"] == "confirmed").to_numpy()
    rows = []
    for low, high in zip(annulus_edges_arcmin[:-1], annulus_edges_arcmin[1:], strict=True):
        in_annulus = (radius_arcmin >= low) & (radius_arcmin < high)
        random_in = (coverage["radius_deg"] * 60 >= low) & (coverage["radius_deg"] * 60 < high)
        covered_area = field_area * float((random_in & coverage["covered"]).mean())
        geometric_area = field_area * float(random_in.mean())
        row = {
            "radius_low_arcmin": low,
            "radius_high_arcmin": high,
            "radius_mid_kpc": 0.5 * (low + high) * kpc_per_arcmin_per_mpc * field["host_distance_mpc"],
            "covered_area_square_deg": covered_area,
            "covered_fraction": covered_area / geometric_area,
            "known_confirmed_with_gaia": int((in_annulus & known).sum()),
        }
        for sample in samples:
            observed = int((in_annulus & sample_mask(fornax, sample).to_numpy()).sum())
            result = excess_significance(observed, covered_area, backgrounds[sample], rng) if covered_area > 0 else {}
            row[f"{sample}_count"] = observed
            row[f"{sample}_density"] = observed / covered_area if covered_area > 0 else np.nan
            low_count, high_count = stats.gamma.ppf([0.16, 0.84], observed + 0.5)
            row[f"{sample}_density_low"] = low_count / covered_area if covered_area > 0 else np.nan
            row[f"{sample}_density_high"] = high_count / covered_area if covered_area > 0 else np.nan
            row[f"{sample}_expected_background"] = result.get("expected_background", np.nan)
            row[f"{sample}_gaussian_sigma"] = result.get("gaussian_sigma", np.nan)
        rows.append(row)
    return pd.DataFrame(rows)


def plot_profile(profile: pd.DataFrame, backgrounds: dict, folder) -> None:
    figure, axes = plt.subplots(1, 2, figsize=(qa_plots.double_width, 3.1))
    middle = 0.5 * (profile["radius_low_arcmin"] + profile["radius_high_arcmin"])
    styles = {
        "tier_a": (qa_plots.colors["candidate"], "o"),
        "tier_a_below_galaxy_sequence": (qa_plots.colors["known"], "s"),
        "tier_a_or_b": (qa_plots.colors["selected"], "^"),
    }
    for sample, (color, marker) in styles.items():
        density = profile[f"{sample}_density"].to_numpy()
        lower = density - profile[f"{sample}_density_low"].to_numpy()
        upper = profile[f"{sample}_density_high"].to_numpy() - density
        axes[0].errorbar(
            middle,
            np.where(density > 0, density, np.nan),
            yerr=[lower, upper],
            color=color,
            marker=marker,
            ms=4,
            lw=0.8,
            capsize=2,
            label=rf"{samples[sample]}",
        )
        background = backgrounds[sample]
        axes[0].axhspan(*background["density_interval_68"], color=color, alpha=0.15, lw=0)
        axes[0].axhline(background["density_per_square_deg"], color=color, lw=0.7, ls="--")
        cumulative = np.cumsum(profile[f"{sample}_count"] - profile[f"{sample}_expected_background"])
        axes[1].plot(profile["radius_high_arcmin"], cumulative, color=color, marker=marker, ms=4)
    axes[0].set_xscale("log")
    axes[0].set_yscale("log")
    axes[0].set_xticks([2, 5, 10, 20, 50], labels=["2", "5", "10", "20", "50"])
    axes[0].set_xticks([], minor=True)
    axes[0].set_xlabel(r"projected radius from NGC 1399 (arcmin)")
    axes[0].set_ylabel(r"candidates per deg$^2$ (covered area)")
    axes[0].legend(fontsize=6.5, frameon=True)
    axes[0].set_title(r"bands and dashed lines: control-field background", fontsize=8)
    secondary = axes[0].secondary_xaxis("top", functions=(lambda x: x * 5.818, lambda x: x / 5.818))
    secondary.set_xticks([10, 20, 50, 100, 200, 300], labels=["10", "20", "50", "100", "200", "300"])
    secondary.set_xticks([], minor=True)
    secondary.set_xlabel(r"kpc at 20 Mpc")
    axes[1].axhline(0, color="k", lw=0.6)
    axes[1].set_xlabel(r"projected radius from NGC 1399 (arcmin)")
    axes[1].set_ylabel(r"cumulative excess over background")
    figure.tight_layout()
    qa_plots.save(figure, folder, "radial_profile")


def plot_maps(tables: dict, coverages: dict, fields: dict, config: dict, folder) -> None:
    galaxies = pd.read_csv(run_state.reference_dir(config) / "repository/data/galaxy_sample/galaxy_sample_ranked.csv")
    figure, axes = plt.subplots(1, 2, figsize=(qa_plots.double_width, 3.7))
    for axis, (name, frame) in zip(axes, tables.items(), strict=True):
        field = fields[name]
        coverage = coverages[name]
        hole = coverage[~coverage["covered"]].iloc[::6]
        axis.scatter(hole["east_deg"], hole["north_deg"], s=0.3, color="0.85", rasterized=True)
        cos_dec = np.cos(np.radians(field["dec_deg"]))
        east = (frame["ra"] - field["ra_deg"]) * cos_dec
        north = frame["dec"] - field["dec_deg"]
        for tier, color, size in (
            ("D", "0.55", 3),
            ("B", qa_plots.colors["selected"], 7),
            ("A", qa_plots.colors["candidate"], 9),
        ):
            members = frame["tier"] == tier
            axis.scatter(
                east[members], north[members], s=size, color=color, label=rf"tier {tier} ({int(members.sum())})"
            )
        known = frame["known_state"] == "confirmed"
        if known.any():
            axis.scatter(
                east[known],
                north[known],
                s=26,
                facecolor="none",
                edgecolor=qa_plots.colors["known"],
                linewidths=0.6,
                label=rf"known confirmed, in Gaia ({int(known.sum())})",
            )
        near = galaxies[
            np.hypot((galaxies["ra"] - field["ra_deg"]) * cos_dec, galaxies["dec"] - field["dec_deg"])
            < field["radius_deg"]
        ]
        axis.scatter(
            (near["ra"] - field["ra_deg"]) * cos_dec,
            near["dec"] - field["dec_deg"],
            marker="x",
            s=28,
            color="k",
            linewidths=0.8,
            label=r"galaxies, $D<25$ Mpc",
        )
        circle = np.linspace(0, 2 * np.pi, 200)
        axis.plot(field["radius_deg"] * np.cos(circle), field["radius_deg"] * np.sin(circle), color="k", lw=0.6)
        axis.set_xlim(1.05, -1.05)
        axis.set_ylim(-1.05, 1.05)
        axis.set_aspect("equal")
        axis.set_xlabel(r"$\Delta{\rm RA}\cos\delta$ (deg)")
        axis.set_title(rf"{name} (grey area: no Euclid catalogue)", fontsize=8)
        axis.legend(fontsize=5.5, loc="lower left", frameon=True, markerscale=1.2)
    axes[0].set_ylabel(r"$\Delta{\rm Dec}$ (deg)")
    figure.tight_layout()
    qa_plots.save(figure, folder, "candidate_maps")


def main() -> None:
    config = run_state.load_config()
    run_state.require_stages(config, ["stage_5_cutflow"])
    folder = run_state.stage_dir(config, stage_name)
    fields = run_state.load_fields(config)
    fields["fornax"].setdefault("host_distance_mpc", config["fields"]["fornax"]["host_distance_mpc"])
    stage_5 = run_state.run_dir(config) / "stage_5_cutflow" / "tables"
    rng = np.random.default_rng(20261114)
    tables = {name: pd.read_parquet(stage_5 / f"master_{name}.parquet") for name in fields}
    coverages, area_checks = {}, {}
    for name, field in fields.items():
        catalogue = load_cone(config, name)
        coverages[name] = random_coverage(field, catalogue, rng)
        area_checks[name] = {
            "random_point_covered_fraction": float(coverages[name]["covered"].mean()),
            "grid_occupancy_fraction": grid_coverage_fraction(field, catalogue),
            "gaia_source_covered_fraction": float(tables[name]["euclid_covered"].mean()),
        }
    field_area = np.pi * fields["fornax"]["radius_deg"] ** 2
    backgrounds = {
        sample: control_background(tables["control"], coverages["control"], field_area, sample) for sample in samples
    }
    profile = radial_profile(tables["fornax"], coverages["fornax"], fields["fornax"], backgrounds, rng)
    profile.to_csv(folder / "tables" / "radial_profile.csv", index=False)
    covered_area = field_area * float(coverages["fornax"]["covered"].mean())
    totals = {}
    for sample in samples:
        observed = int(sample_mask(tables["fornax"], sample).sum())
        totals[sample] = excess_significance(observed, covered_area, backgrounds[sample], rng)
        inner = profile[profile["radius_high_arcmin"] <= 20]
        totals[sample]["within_20_arcmin"] = excess_significance(
            int(inner[f"{sample}_count"].sum()), float(inner["covered_area_square_deg"].sum()), backgrounds[sample], rng
        )
    plot_profile(profile, backgrounds, folder / "figures")
    plot_maps(tables, coverages, fields, config, folder / "figures")

    differences = {
        name: abs(item["random_point_covered_fraction"] - item["grid_occupancy_fraction"])
        for name, item in area_checks.items()
    }
    metrics = {
        "area_checks": area_checks,
        "fornax_covered_area_square_deg": covered_area,
        "backgrounds": backgrounds,
        "totals": totals,
        "profile": profile.round(3).to_dict("records"),
        "note": "Significances include Poisson noise in both fields and a field-to-field term; they are not corrected "
        "for the choice of annuli (trial factor) and tier A contains known Fornax globular clusters.",
    }
    gates = [
        run_state.gate(
            "area_estimates_agree",
            "random-point and grid-cell coverage fractions agree within 0.02",
            {name: {key: round(value, 4) for key, value in item.items()} for name, item in area_checks.items()},
            all(value < 0.02 for value in differences.values()),
        ),
        run_state.gate(
            "profile_written",
            "radial profile with background and significance written (null passes)",
            {
                sample: {
                    "observed": totals[sample]["observed"],
                    "expected": round(totals[sample]["expected_background"], 1),
                    "sigma": round(totals[sample]["gaussian_sigma"], 1),
                }
                for sample in samples
            },
            True,
        ),
    ]
    run_state.write_summary(config, stage_name, metrics, gates)


if __name__ == "__main__":
    main()
