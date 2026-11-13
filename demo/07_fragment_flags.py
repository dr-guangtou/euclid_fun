"""Step 7 of the demo: can MER catalogue columns tell fragments of a large galaxy from real sources?

Test case: NGC 1483 (D ~ 2'), which the MER pipeline splits into a handful of large entries plus hundreds of small
detections in its outer disc. Method (statistical, no truth labels needed):
  1. ESA TAP cone (7.2' radius) on the wide (DR1_R2) and deep (EDF-South, DR1_R1) MER catalogues, with every
     column that could flag an unreliable entry;
  2. number density of entries versus radius, normalised to the field density measured at 200"-420";
     the excess over 1 inside 40"-100" is the fragment population (a lower limit, because the disc also hides
     some real background sources);
  3. for each candidate indicator: the fraction of the excess it flags versus the fraction of field sources it
     flags (an indicator with no discriminating power lies on the 1:1 line).

Outputs: figures/dr1_fragment_flags.png and figures/dr1_fragment_flags.json

Usage: uv run python demo/07_fragment_flags.py
"""

import json
import sys
from pathlib import Path

import astropy.units as u
import matplotlib.pyplot as plt
import numpy as np
from astropy.io import fits
from astropy.nddata import Cutout2D, block_reduce
from astropy.table import Table
from astropy.wcs import WCS
from dr1_access import catalogue_zero_point_ujy, default_data_root, run_query
from targets import lsb_target, lsb_wide_tile

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from plot_style import figure_width_double, use_publication_style  # noqa: E402

figure_dir = Path(__file__).resolve().parents[1] / "figures"
catalogue_dir = default_data_root / "catalogs"
tile_dir = default_data_root / "tiles" / str(lsb_wide_tile)
cone_radius_deg = 0.12
fragment_zone_arcsec = (40.0, 100.0)
field_zone_arcsec = (200.0, 420.0)
spurious_threshold = 0.7  # DR1 advice (Kuemmel et al. 2026)
indicator_labels = {  # LaTeX label and hand-placed (x, y, alignment) in panel (c) data units
    "spurious_prob_above_0.7": (r"\texttt{spurious\_prob} $>0.7$", (1.0, 9.0, "left")),
    "spurious_flag": (r"\texttt{spurious\_flag}", (1.0, 52.0, "left")),
    "nir_only": (r"NIR-only (\texttt{vis\_det}=0)", (31.0, 64.0, "right")),
    "deblended_flag": (r"\texttt{deblended\_flag}", (16.5, 28.0, "left")),
    "spurious_prob_above_0.7_or_nir_only": (r"$p_{\rm sp}>0.7$ or NIR-only", (31.0, 83.0, "right")),
}
reliability_columns = (
    "object_id, right_ascension, declination, tile_index, flux_detection_total, vis_det, spurious_prob, "
    "spurious_flag, det_quality_flag, deblended_flag, parent_id, blended_prob, extended_prob, segmentation_area, "
    "mumax_minus_mag"
)
survey_tables = {"wide": "dr1.mer_catalogue_wide_survey", "deep": "dr1.mer_catalogue_deep_survey"}


def load_cone(survey: str) -> Table:
    path = catalogue_dir / f"ngc1483_{survey}_cone_flags.fits"
    if path.exists():
        return Table.read(path)
    centre = lsb_target.coordinate
    table = run_query(
        f"SELECT {reliability_columns} FROM {survey_tables[survey]} WHERE 1 = CONTAINS("
        f"POINT('ICRS', right_ascension, declination), CIRCLE('ICRS', {centre.ra.deg}, {centre.dec.deg}, "
        f"{cone_radius_deg}))"
    )
    catalogue_dir.mkdir(parents=True, exist_ok=True)
    table.write(path, overwrite=True)
    return table


def column(table: Table, name: str, fill: float = np.nan) -> np.ndarray:
    values = table[name]
    return np.asarray(values.filled(fill) if hasattr(values, "filled") else values, dtype=float)


def prepare(table: Table) -> dict[str, np.ndarray]:
    centre = lsb_target.coordinate
    east = (column(table, "right_ascension") - centre.ra.deg) * np.cos(centre.dec.radian) * 3600.0
    north = (column(table, "declination") - centre.dec.deg) * 3600.0
    flux = column(table, "flux_detection_total")
    with np.errstate(invalid="ignore", divide="ignore"):
        magnitude = np.where(flux > 0, catalogue_zero_point_ujy - 2.5 * np.log10(flux), np.nan)
    quality = column(table, "det_quality_flag", 0).astype(int)
    parent = column(table, "parent_id", -9).astype(np.int64)
    vis_detected = column(table, "vis_det", -9) == 1
    spurious = column(table, "spurious_prob")
    radius = np.hypot(east, north)
    brightest = np.nanargmin(np.where(vis_detected & (radius < 15.0), magnitude, np.inf))
    tile = column(table, "tile_index", -9).astype(np.int64)
    # parent_id is a detection number local to each tile
    family = (parent == parent[brightest]) & (tile == tile[brightest])
    family[brightest] = True
    return {
        "east": east,
        "north": north,
        "radius": radius,
        "magnitude": magnitude,
        "family": family,
        "vis_detected": vis_detected,
        "clean": vis_detected & (spurious <= spurious_threshold),
        "indicators": {
            "spurious_prob_above_0.7": spurious > spurious_threshold,
            "spurious_flag": column(table, "spurious_flag", 0) == 1,
            "nir_only": ~vis_detected,
            "deblended_flag": column(table, "deblended_flag", 0) == 1,
            "spurious_prob_above_0.7_or_nir_only": (spurious > spurious_threshold) | ~vis_detected,
        },
        "quality": quality,
        "parent": parent,
        "null_fraction": {
            name: float(np.mean(np.isnan(column(table, name))))
            for name in ("blended_prob", "extended_prob", "spurious_prob")
        },
    }


def annulus_area_arcmin2(inner: float, outer: float) -> float:
    return np.pi * (outer**2 - inner**2) / 3600.0


def density_ratio(sample: dict, selection: np.ndarray, edges: np.ndarray) -> np.ndarray:
    field = selection & (sample["radius"] > field_zone_arcsec[0]) & (sample["radius"] < field_zone_arcsec[1])
    field_density = field.sum() / annulus_area_arcmin2(*field_zone_arcsec)
    counts, _ = np.histogram(sample["radius"][selection & ~sample["family"]], bins=edges)
    areas = np.array([annulus_area_arcmin2(inner, outer) for inner, outer in zip(edges[:-1], edges[1:], strict=True)])
    return counts / areas / field_density


def indicator_performance(sample: dict) -> dict[str, dict[str, float]]:
    radius = sample["radius"]
    zone = (radius > fragment_zone_arcsec[0]) & (radius < fragment_zone_arcsec[1]) & ~sample["family"]
    field = (radius > field_zone_arcsec[0]) & (radius < field_zone_arcsec[1])
    field_density = field.sum() / annulus_area_arcmin2(*field_zone_arcsec)
    expected_real = field_density * annulus_area_arcmin2(*fragment_zone_arcsec)
    excess = zone.sum() - expected_real
    result = {
        "_zone": {"entries": int(zone.sum()), "expected_real": float(expected_real), "excess": float(excess)},
    }
    for name, flagged in sample["indicators"].items():
        field_fraction = flagged[field].mean()
        excess_fraction = (flagged[zone].sum() - field_fraction * expected_real) / excess
        result[name] = {"field_fraction": float(field_fraction), "excess_fraction": float(excess_fraction)}
    return result


def load_image_region(size_arcsec: float, bin_factor: int) -> np.ndarray:
    """I_E BGSUB + BGMOD (MER sky step undone) around NGC 1483, block-averaged (mosaic axes: north up, east left)."""
    regions = []
    for prefix in ("EUC_MER_BGSUB-MOSAIC-VIS", "EUC_MER_BGMOD-VIS"):
        path = next(tile_dir.glob(f"{prefix}_TILE*.fits"))
        with fits.open(path, memmap=True) as hdu_list:
            cutout = Cutout2D(
                hdu_list[0].data, lsb_target.coordinate, size_arcsec * u.arcsec, wcs=WCS(hdu_list[0].header), copy=True
            )
        regions.append(cutout.data.astype(np.float32))
    return block_reduce(regions[0] + regions[1], bin_factor, func=np.mean)


def plot(samples: dict, performance: dict, image: np.ndarray, pixel_arcsec: float, output: Path) -> None:
    use_publication_style()
    figure = plt.figure(figsize=(figure_width_double, 2.55))
    grid = figure.add_gridspec(1, 3, width_ratios=[1.0, 1.15, 1.0], wspace=0.38)

    axis = figure.add_subplot(grid[0])
    scale = 0.004
    stretched = np.arcsinh(image / scale)
    low, high = np.nanpercentile(stretched, [20, 99.7])
    axis.imshow(stretched, cmap="gray_r", vmin=low, vmax=high)
    wide = samples["wide"]
    centre_pixel = np.array(image.shape[::-1]) / 2.0 - 0.5
    x_pixel = centre_pixel[0] - wide["east"] / pixel_arcsec
    y_pixel = centre_pixel[1] + wide["north"] / pixel_arcsec
    inside = (x_pixel > 0) & (x_pixel < image.shape[1]) & (y_pixel > 0) & (y_pixel < image.shape[0])
    flagged = wide["indicators"]["spurious_prob_above_0.7_or_nir_only"]
    keep = inside & ~wide["family"] & ~flagged
    drop = inside & ~wide["family"] & flagged
    axis.scatter(x_pixel[keep], y_pixel[keep], s=1.2, c="#1f77b4", lw=0, label="kept")
    axis.scatter(x_pixel[drop], y_pixel[drop], s=2.5, c="#ff7f0e", marker="x", lw=0.4, label="flagged")
    axis.scatter(
        x_pixel[wide["family"]],
        y_pixel[wide["family"]],
        s=22,
        facecolor="none",
        edgecolor="#d62728",
        lw=0.8,
        label="main pieces",
    )
    for radius in fragment_zone_arcsec:
        axis.add_patch(plt.Circle(centre_pixel, radius / pixel_arcsec, fill=False, ls=":", lw=0.6, color="k"))
    axis.set_xlim(0, image.shape[1])
    axis.set_ylim(0, image.shape[0])
    axis.set_xticks([])
    axis.set_yticks([])
    axis.legend(
        loc="lower left",
        handletextpad=0.1,
        borderpad=0.25,
        markerscale=1.5,
        fontsize=6.3,
        frameon=True,
        framealpha=0.85,
        edgecolor="none",
    )
    axis.text(
        0.03,
        0.97,
        r"(a) NGC\,1483, $I_E$ wide",
        transform=axis.transAxes,
        va="top",
        fontsize=7.5,
        bbox={"facecolor": "white", "edgecolor": "none", "alpha": 0.85, "pad": 1.0},
    )
    bar_pixels = 60.0 / pixel_arcsec
    axis.plot([image.shape[1] * 0.95 - bar_pixels, image.shape[1] * 0.95], [image.shape[0] * 0.05] * 2, "k-", lw=1.0)
    axis.text(image.shape[1] * 0.95 - bar_pixels / 2, image.shape[0] * 0.07, r"$1'$", ha="center", fontsize=7)

    axis = figure.add_subplot(grid[1])
    edges = np.concatenate([np.arange(25.0, 130.0, 10.0), np.arange(130.0, 260.0, 20.0)])
    centres = 0.5 * (edges[:-1] + edges[1:])
    styles = {"wide": ("k", "o"), "deep": ("#1f77b4", "s")}
    for survey, sample in samples.items():
        colour, marker = styles[survey]
        all_entries = np.ones_like(sample["radius"], dtype=bool)
        axis.plot(
            centres,
            density_ratio(sample, all_entries, edges),
            color=colour,
            marker=marker,
            ms=2.5,
            label=f"{survey}: all entries",
        )
        axis.plot(
            centres,
            density_ratio(sample, sample["clean"], edges),
            color=colour,
            ls="--",
            lw=0.9,
            label=rf"{survey}: VIS, $p_{{\rm sp}}\le0.7$",
        )
    axis.axhline(1.0, color="0.5", lw=0.6)
    axis.axvspan(*fragment_zone_arcsec, color="0.92", zorder=0)
    axis.set_xlabel("distance from NGC 1483 [arcsec]")
    axis.set_ylabel("entry density / field density")
    axis.set_xlim(25, 250)
    axis.set_ylim(0, 4.0)
    axis.legend(loc="upper right", fontsize=6.3, handlelength=1.8)
    axis.text(0.03, 0.96, "(b)", transform=axis.transAxes, va="top")

    axis = figure.add_subplot(grid[2])
    axis.plot([0, 100], [0, 100], color="0.5", lw=0.6)
    for name in performance["wide"]:
        if name.startswith("_"):
            continue
        pair = [performance[survey][name] for survey in ("wide", "deep")]
        axis.plot(
            [100 * values["field_fraction"] for values in pair],
            [100 * values["excess_fraction"] for values in pair],
            color="0.7",
            lw=0.5,
            zorder=0,
        )
    for survey, colour_marker in styles.items():
        colour, marker = colour_marker
        for name, values in performance[survey].items():
            if name.startswith("_"):
                continue
            axis.plot(
                100 * values["field_fraction"],
                100 * values["excess_fraction"],
                marker=marker,
                color=colour,
                ms=3.5,
                ls="none",
                mfc=colour if survey == "wide" else "none",
            )
    for name in performance["wide"]:
        if name.startswith("_"):
            continue
        label, (x_label, y_label, alignment) = indicator_labels[name]
        axis.text(x_label, y_label, label, fontsize=6.0, ha=alignment, va="center")
    axis.set_xlim(0, 32)
    axis.set_ylim(0, 100)
    axis.set_xlabel(r"field sources flagged [\%]")
    axis.set_ylabel(r"fragment excess flagged [\%]")
    axis.text(0.04, 0.96, "(c)", transform=axis.transAxes, va="top")
    axis.plot([], [], "ko", ms=3.5, label="wide")
    axis.plot([], [], "s", color="#1f77b4", mfc="none", ms=3.5, label="deep")
    axis.legend(loc="lower right", fontsize=6.5)

    output.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output)
    plt.close(figure)


def main() -> None:
    samples = {survey: prepare(load_cone(survey)) for survey in survey_tables}
    performance = {survey: indicator_performance(sample) for survey, sample in samples.items()}
    summary = {}
    for survey, sample in samples.items():
        family = sample["family"]
        zone = (sample["radius"] > fragment_zone_arcsec[0]) & (sample["radius"] < fragment_zone_arcsec[1]) & ~family
        summary[survey] = {
            "main_pieces": int(family.sum()),
            "main_piece_magnitudes": np.round(np.sort(sample["magnitude"][family]), 2).tolist(),
            "zone_fraction_with_parent": float(np.mean(sample["parent"][zone] != -1)),
            "zone_fraction_quality_bit_512": float(np.mean((sample["quality"][zone] & 512) > 0)),
            "null_fraction": sample["null_fraction"],
            "indicators": performance[survey],
        }
        print(f"[{survey}] {summary[survey]['main_pieces']} main pieces; zone {performance[survey]['_zone']}")
        for name, values in performance[survey].items():
            if not name.startswith("_"):
                print(
                    f"   {name:45s} field {100 * values['field_fraction']:5.1f}%  "
                    f"excess {100 * values['excess_fraction']:5.1f}%"
                )
    bin_factor = 4
    image = load_image_region(size_arcsec=230.0, bin_factor=bin_factor)
    output = figure_dir / "dr1_fragment_flags.png"
    plot(samples, performance, image, 0.1 * bin_factor, output)
    output.with_suffix(".json").write_text(json.dumps(summary, indent=2))
    print("wrote", output)


if __name__ == "__main__":
    main()
