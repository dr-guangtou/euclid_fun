"""Step 3 of the demo: DR1 catalogues for low-z galaxies -- MER photometry + morphology + photo-z + stellar mass.

(a) How the MER catalogue describes a large nearby galaxy (NGC 1483): all MER entries inside its optical
    extent, drawn as ellipses on the VIS cutout (shredding / deblending of a resolved galaxy).
(b) Single-Sersic VIS size versus index for the galaxies of the same wide tile (102021980).
(c) Photometric redshift versus VIS magnitude.
(d) Stellar mass versus photometric redshift for z < 1.

The tile-level sample is the ADQL join of four DR1 tables on object_id:
dr1.mer_catalogue_wide_survey, dr1.mer_morphology_wide_survey, dr1.phz_photo_z_wide,
dr1.phz_physical_parameters_wide (+ dr1.phz_classification_wide for the class).

Usage: uv run python demo/03_catalog_demo.py
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from astropy.table import Table
from astropy.visualization import AsinhStretch, ImageNormalize
from dr1_access import catalogue_zero_point_ujy, default_data_root, query_mer_sources, read_image, run_query
from matplotlib.patches import Ellipse
from targets import lsb_target, lsb_wide_tile

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from plot_style import figure_width_double, use_publication_style  # noqa: E402

figure_dir = Path(__file__).resolve().parents[1] / "figures"
catalogue_dir = default_data_root / "catalogs"

tile_query = f"""
SELECT m.object_id, m.right_ascension, m.declination, m.flux_detection_total, m.fluxerr_detection_total,
       m.flux_vis_sersic, m.flux_h_sersic, m.flux_vis_2fwhm_aper, m.flux_h_2fwhm_aper,
       m.point_like_prob, m.spurious_prob, m.det_quality_flag, m.deblended_flag, m.vis_det,
       m.semimajor_axis, m.ellipticity, m.position_angle, m.kron_radius, m.mu_max,
       mo.sersic_sersic_vis_radius, mo.sersic_sersic_vis_index, mo.sersic_sersic_vis_axis_ratio,
       mo.sersic_visnir_flags, mo.flux_radius, mo.concentration, mo.asymmetry,
       mo.smooth_or_featured_smooth, mo.smooth_or_featured_featured_or_disk,
       p.phz_median, p.phz_mode_1, p.phz_flags,
       c.phz_classification, c.phz_gal_prob,
       pp.phz_pp_median_stellarmass, pp.phz_pp_median_sfr, pp.phys_param_flags
FROM dr1.mer_catalogue_wide_survey AS m
JOIN dr1.mer_morphology_wide_survey AS mo ON mo.object_id = m.object_id
JOIN dr1.phz_photo_z_wide AS p ON p.object_id = m.object_id
JOIN dr1.phz_classification_wide AS c ON c.object_id = m.object_id
LEFT OUTER JOIN dr1.phz_physical_parameters_wide AS pp ON pp.object_id = m.object_id
WHERE m.tile_index = {lsb_wide_tile} AND m.vis_det = 1 AND m.flux_detection_total > 0.912
"""


def ab_magnitude(flux_ujy: np.ndarray) -> np.ndarray:
    with np.errstate(divide="ignore", invalid="ignore"):
        return np.where(flux_ujy > 0, -2.5 * np.log10(flux_ujy) + catalogue_zero_point_ujy, np.nan)


def load_tile_sample() -> Table:
    catalogue_dir.mkdir(parents=True, exist_ok=True)
    path = catalogue_dir / f"tile_{lsb_wide_tile}_mer_morph_phz.fits"
    if path.exists():
        return Table.read(path)
    table = run_query(tile_query)
    for column in table.colnames:  # VOTable masked arrays -> plain arrays with NaN for FITS output
        if hasattr(table[column], "filled") and table[column].dtype.kind == "f":
            table[column] = table[column].filled(np.nan)
    table.write(path, overwrite=True)
    return table


def galaxy_selection(table: Table) -> np.ndarray:
    classification = np.asarray(table["phz_classification"])
    return (
        ((classification & 2) != 0)  # PHZ class bit 2 = galaxy (bit 1 = star): verified against POINT_LIKE_PROB
        & (np.asarray(table["spurious_prob"], float) < 0.7)
        & (np.asarray(table["det_quality_flag"]) == 0)
        & (np.asarray(table["phz_flags"]) == 0)
    )


def panel_shredding(axis: plt.Axes) -> None:
    cutout_dir = default_data_root / "cutouts" / lsb_target.slug
    image, header = read_image(cutout_dir / "VIS.fits")
    size = image.shape[0]
    extent_arcsec = size * 0.1
    sources = query_mer_sources(
        lsb_target.ra_deg,
        lsb_target.dec_deg,
        95.0,
        columns="object_id, right_ascension, declination, flux_detection_total, semimajor_axis, ellipticity, "
        "position_angle, deblended_flag, point_like_prob, spurious_prob, segmentation_map_id",
    )
    norm = ImageNormalize(image, vmin=-0.005, vmax=1.5, stretch=AsinhStretch(0.02))
    half = extent_arcsec / 2
    axis.imshow(image, origin="lower", cmap="gray_r", norm=norm, extent=[half, -half, -half, half])
    cos_dec = np.cos(np.deg2rad(lsb_target.dec_deg))
    for row in sources:
        dx = (float(row["right_ascension"]) - lsb_target.ra_deg) * cos_dec * 3600.0
        dy = (float(row["declination"]) - lsb_target.dec_deg) * 3600.0
        major = 3.0 * float(row["semimajor_axis"]) * 0.1  # SExtractor A_IMAGE in pixels -> 3A in arcsec
        minor = major * (1.0 - float(row["ellipticity"]))
        if float(row["spurious_prob"]) > 0.7:
            colour = "tab:orange"
        elif int(row["deblended_flag"]) == 1:
            colour = "tab:red"
        else:
            colour = "tab:blue"
        # THETA_IMAGE is counter-clockwise from +x; with RA increasing to the left the sky angle flips sign.
        axis.add_patch(
            Ellipse(
                (dx, dy), 2 * major, 2 * minor, angle=-float(row["position_angle"]), fill=False, lw=0.5, color=colour
            )
        )
    brightest = sources[np.argsort(-np.asarray(sources["flux_detection_total"], float))][:3]
    for row in brightest:
        print(
            f"  NGC 1483 MER entry {int(row['object_id'])}: mag {ab_magnitude(float(row['flux_detection_total'])):.2f}"
            f", 3A = {3 * float(row['semimajor_axis']) * 0.1:.1f} arcsec, deblended {int(row['deblended_flag'])}"
        )
    axis.set_xlim(half, -half)
    axis.set_ylim(-half, half)
    axis.set_xlabel(r"$\Delta\alpha\cos\delta$ [arcsec]")
    axis.set_ylabel(r"$\Delta\delta$ [arcsec]")
    separation = np.asarray(sources["separation_arcsec"], float)
    inner = np.sum(separation < 40.0)
    annulus = np.sum((separation >= 40.0) & (separation < 70.0))
    field_density = np.sum(separation >= 80.0) / (np.pi * (95.0**2 - 80.0**2))
    expected = field_density * np.pi * (70.0**2 - 40.0**2)
    axis.text(
        0.03,
        0.97,
        rf"NGC 1483 (wide tile): {inner} MER entries at $r<40''$;"
        "\n"
        rf"{annulus} at $40''$--$70''$ (field density predicts {expected:.0f})",
        transform=axis.transAxes,
        ha="left",
        va="top",
        fontsize=6.5,
        bbox={"facecolor": "white", "alpha": 0.8, "edgecolor": "none", "pad": 1.5},
    )
    axis.plot([], [], color="tab:blue", lw=0.8, label="isolated")
    axis.plot([], [], color="tab:red", lw=0.8, label=r"\texttt{DEBLENDED\_FLAG}=1")
    axis.plot([], [], color="tab:orange", lw=0.8, label=r"\texttt{SPURIOUS\_PROB}$>0.7$")
    axis.legend(
        loc="lower left",
        fontsize=6.0,
        handlelength=1.2,
        borderaxespad=0.3,
        frameon=True,
        framealpha=0.85,
        edgecolor="none",
    )
    print(f'  NGC 1483: {inner} entries r<40", {annulus} at 40-70" vs {expected:.0f} expected from field density')


def main() -> None:
    use_publication_style()
    sample = load_tile_sample()
    galaxies = galaxy_selection(sample)
    vis_magnitude = ab_magnitude(np.asarray(sample["flux_detection_total"], float))
    photo_z = np.asarray(sample["phz_median"], float)
    sersic_radius = np.asarray(sample["sersic_sersic_vis_radius"], float)
    sersic_index = np.asarray(sample["sersic_sersic_vis_index"], float)
    stellar_mass = np.asarray(sample["phz_pp_median_stellarmass"], float)
    print(f"tile {lsb_wide_tile}: {len(sample)} VIS-detected sources with IE < 24, {galaxies.sum()} clean galaxies")

    figure, axes = plt.subplots(2, 2, figsize=(figure_width_double, figure_width_double * 0.86))
    panel_shredding(axes[0, 0])

    bright = galaxies & (vis_magnitude < 22.0) & np.isfinite(sersic_radius) & (sersic_radius > 0)
    axis = axes[0, 1]
    points = axis.scatter(
        sersic_radius[bright],
        sersic_index[bright],
        c=photo_z[bright],
        s=2,
        cmap="viridis",
        vmin=0,
        vmax=1.5,
        rasterized=True,
        lw=0,
    )
    axis.axhline(8.0, color="0.4", ls="--", lw=0.7)
    axis.text(0.4, 7.75, r"$n_{\rm max}=8$ (fit boundary)", fontsize=6.5, color="0.3", va="top")
    axis.axvline(0.16, color="0.4", ls=":", lw=0.7)
    axis.text(0.145, 4.5, "VIS PSF FWHM", fontsize=6.5, color="0.3", rotation=90, va="center", ha="right")
    axis.set_xscale("log")
    axis.set_xlim(0.05, 30)
    axis.set_ylim(0.2, 8.6)
    axis.set_xlabel(r"VIS S\'ersic $R_{\rm e}$ [arcsec]")
    axis.set_ylabel(r"VIS S\'ersic index $n$")
    colorbar = figure.colorbar(points, ax=axis, pad=0.01)
    colorbar.set_label(r"$z_{\rm phot}$ (PDF median)")
    axis.text(
        0.97,
        0.97,
        rf"galaxies, $I_E<22$ ($N={bright.sum()}$)",
        transform=axis.transAxes,
        ha="right",
        va="top",
        fontsize=7,
    )

    axis = axes[1, 0]
    shown = galaxies & np.isfinite(vis_magnitude)
    axis.hexbin(
        vis_magnitude[shown],
        photo_z[shown],
        gridsize=(60, 50),
        extent=(16, 24, 0, 3),
        bins="log",
        cmap="Greys",
        mincnt=1,
        linewidths=0.1,
    )
    axis.axhspan(0, 0.5, color="tab:orange", alpha=0.12, lw=0)
    axis.text(16.3, 0.25, r"low-$z$ ($z<0.5$)", fontsize=7, va="center", color="tab:orange")
    axis.set_xlim(16, 24)
    axis.set_ylim(0, 3)
    axis.set_xlabel(r"$I_E$ (Kron, \texttt{FLUX\_DETECTION\_TOTAL}) [AB mag]")
    axis.set_ylabel(r"$z_{\rm phot}$ (\texttt{PHZ\_MEDIAN})")

    axis = axes[1, 1]
    flags = np.asarray(sample["phys_param_flags"], float)
    massive = galaxies & np.isfinite(stellar_mass) & (photo_z < 1.0) & (flags == 0)
    axis.scatter(photo_z[massive], stellar_mass[massive], s=1.5, c="k", alpha=0.35, lw=0, rasterized=True)
    axis.set_xlim(0, 1)
    axis.set_ylim(6.5, 12.2)
    axis.set_xlabel(r"$z_{\rm phot}$")
    axis.set_ylabel(r"$\log_{10}(M_\star/M_\odot)$ (PHZ, NNPZ)")
    axis.text(
        0.03,
        0.97,
        r"$I_E<24$ galaxies, \texttt{PHYS\_PARAM\_FLAGS}=0",
        transform=axis.transAxes,
        ha="left",
        va="top",
        fontsize=7,
    )

    for label, axis in zip("abcd", axes.flat, strict=True):
        axis.text(-0.02, 1.02, f"({label})", transform=axis.transAxes, ha="right", va="bottom", fontsize=9)
    figure.tight_layout(w_pad=1.0, h_pad=1.0)
    output = figure_dir / "dr1_catalog_demo.png"
    figure.savefig(output)
    print(f"saved {output}")


if __name__ == "__main__":
    main()
