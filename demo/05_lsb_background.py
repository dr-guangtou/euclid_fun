"""Step 5 of the demo: what the MER background subtraction does to a large galaxy (NGC 1483, EDF-South).

Inputs (from demo/download_lsb_tiles.py): for the wide-survey tile 102021980 (single visit, DR1_R2) and the EDF-South
deep tile 101287204 (10 visits, DR1_R1), the VIS and H_E background-subtracted mosaics (BGSUB) and the subtracted
MER background models (BGMOD).

For each of the four images (wide/deep x VIS/H):
  1. read an 8'x8' region around NGC 1483 (memory-mapped) and block-average it to 1"x1" pixels;
  2. build "as delivered" (BGSUB) and "MER background restored" (BGSUB + BGMOD) versions;
  3. mask all sources except the galaxy (photutils segmentation on the smoothed restored image, dilated);
  4. restored version only: subtract our own sky = sigma-clipped median in the elliptical annulus 3'-4';
  5. measure the surface-brightness profile in fixed elliptical annuli (sigma-clipped median per annulus);
  6. measure the 3-sigma surface-brightness limit in 10"x10" boxes (random boxes on masked sky beyond 2.5'),
     and compare with the naive white-noise extrapolation from the native-pixel RMS.

Outputs: figures/dr1_lsb_ngc1483.png and figures/dr1_lsb_ngc1483_limits.json

Usage: uv run python demo/05_lsb_background.py
"""

import json
import sys
from pathlib import Path

import astropy.units as u
import matplotlib.pyplot as plt
import numpy as np
from astropy.convolution import Gaussian2DKernel, convolve
from astropy.io import fits
from astropy.nddata import Cutout2D, block_reduce
from astropy.stats import sigma_clipped_stats
from astropy.wcs import WCS
from dr1_access import default_data_root
from matplotlib.patches import Ellipse
from photutils.segmentation import detect_sources
from scipy.ndimage import binary_dilation
from targets import lsb_target

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from plot_style import figure_width_double, use_publication_style  # noqa: E402

figure_dir = Path(__file__).resolve().parents[1] / "figures"
region_size_arcsec = 480.0
bin_factor = 10  # 0.1" -> 1" pixels
axis_ratio = 0.80  # NGC 1483 outer isophotes (checked by eye on the deep VIS image)
position_angle_deg = 160.0  # east of north
sky_annulus_arcsec = (180.0, 240.0)
limit_min_radius_arcsec = 150.0
random_generator = np.random.default_rng(20261112)


def load_region(path: Path) -> np.ndarray:
    with fits.open(path, memmap=True) as hdu_list:
        hdu = hdu_list[0] if hdu_list[0].data is not None else hdu_list[1]
        wcs = WCS(hdu.header)
        cutout = Cutout2D(
            hdu.data,
            lsb_target.coordinate,
            region_size_arcsec * u.arcsec,
            wcs=wcs,
            mode="partial",
            fill_value=np.nan,
            copy=True,
        )
    data = cutout.data.astype(np.float32)
    data[data == 0] = np.nan  # MER mosaics are zero outside the covered area
    return data


def elliptical_radius(shape: tuple[int, int], pixel_arcsec: float) -> np.ndarray:
    """Semi-major-axis radius (arcsec) for an ellipse centred on the image centre; RA increases to the left (-x)."""
    y_index, x_index = np.indices(shape, dtype=float)
    centre_y, centre_x = (shape[0] - 1) / 2.0, (shape[1] - 1) / 2.0
    east = -(x_index - centre_x) * pixel_arcsec
    north = (y_index - centre_y) * pixel_arcsec
    angle = np.deg2rad(position_angle_deg)
    along_major = east * np.sin(angle) + north * np.cos(angle)
    along_minor = east * np.cos(angle) - north * np.sin(angle)
    return np.hypot(along_major, along_minor / axis_ratio)


def source_mask(binned_restored: np.ndarray, radius: np.ndarray) -> np.ndarray:
    _, median, sigma = sigma_clipped_stats(binned_restored[radius > limit_min_radius_arcsec], sigma=3.0)
    smoothed = convolve(np.nan_to_num(binned_restored - median), Gaussian2DKernel(1.0))
    segmentation = detect_sources(smoothed, threshold=1.5 * sigma, n_pixels=5)
    labels = segmentation.data
    centre = (labels.shape[0] // 2, labels.shape[1] // 2)
    galaxy_label = labels[centre]
    mask = (labels > 0) & (labels != galaxy_label)
    mask = binary_dilation(mask, iterations=2)
    return mask | ~np.isfinite(binned_restored)


def surface_brightness(value: np.ndarray, zero_point: float) -> np.ndarray:
    with np.errstate(divide="ignore", invalid="ignore"):
        return np.where(value > 0, zero_point - 5.0 - 2.5 * np.log10(value), np.nan)


def profile(binned: np.ndarray, mask: np.ndarray, radius: np.ndarray, edges: np.ndarray):
    centres, values, errors = [], [], []
    for inner, outer in zip(edges[:-1], edges[1:], strict=True):
        selection = (radius >= inner) & (radius < outer) & ~mask & np.isfinite(binned)
        if selection.sum() < 8:
            continue
        _, median, sigma = sigma_clipped_stats(binned[selection], sigma=3.0, maxiters=5)
        centres.append(np.sqrt(inner * outer))
        values.append(median)
        errors.append(1.253 * sigma / np.sqrt(selection.sum()))
    return np.array(centres), np.array(values), np.array(errors)


def box_limit(binned: np.ndarray, mask: np.ndarray, radius: np.ndarray, box: int = 10, trials: int = 3000) -> float:
    """1-sigma scatter of the mean level in random box x box (arcsec) boxes on masked sky."""
    medians = []
    size_y, size_x = binned.shape
    for _ in range(trials):
        y0 = random_generator.integers(0, size_y - box)
        x0 = random_generator.integers(0, size_x - box)
        if radius[y0 + box // 2, x0 + box // 2] < limit_min_radius_arcsec:
            continue
        patch = binned[y0 : y0 + box, x0 : x0 + box]
        good = ~mask[y0 : y0 + box, x0 : x0 + box] & np.isfinite(patch)
        if good.mean() < 0.7:
            continue
        medians.append(np.mean(patch[good]))
    medians = np.asarray(medians)
    return float(1.4826 * np.median(np.abs(medians - np.median(medians)))), len(medians)


def analyse(label: str, entry: dict) -> dict:
    directory = Path(entry["directory"])
    zero_point = entry["zero_point"]
    bgsub = load_region(directory / entry["files"]["BGSUB"])
    bgmod = load_region(directory / entry["files"]["BKG"])
    restored = bgsub + bgmod
    binned = {
        name: block_reduce(image, bin_factor, func=np.nanmean)
        for name, image in (("bgsub", bgsub), ("restored", restored), ("bgmod", bgmod))
    }
    radius = elliptical_radius(binned["bgsub"].shape, pixel_arcsec=1.0)
    mask = source_mask(binned["restored"], radius)

    sky_selection = (radius >= sky_annulus_arcsec[0]) & (radius < sky_annulus_arcsec[1]) & ~mask
    _, own_sky, _ = sigma_clipped_stats(binned["restored"][sky_selection], sigma=3.0)
    _, delivered_sky, _ = sigma_clipped_stats(binned["bgsub"][sky_selection], sigma=3.0)
    restored_sky_subtracted = binned["restored"] - own_sky

    # Sky systematic: scatter between 8 azimuthal sectors of the sky annulus.
    y_index, x_index = np.indices(radius.shape)
    azimuth = np.arctan2(y_index - radius.shape[0] / 2, x_index - radius.shape[1] / 2)
    sector_levels = []
    for sector in range(8):
        lower = -np.pi + sector * np.pi / 4
        selection = sky_selection & (azimuth >= lower) & (azimuth < lower + np.pi / 4)
        sector_levels.append(np.nanmedian(restored_sky_subtracted[selection]))
    sky_systematic = float(np.std(sector_levels))

    edges = np.geomspace(2.0, 230.0, 32)
    profiles = {
        "bgsub": profile(binned["bgsub"], mask, radius, edges),
        "restored": profile(restored_sky_subtracted, mask, radius, edges),
        "bgmod": profile(binned["bgmod"] - np.nanmedian(binned["bgmod"][sky_selection]), mask, radius, edges),
    }
    sigma_box_bgsub, boxes_bgsub = box_limit(binned["bgsub"], mask, radius)
    sigma_box_restored, boxes_restored = box_limit(restored_sky_subtracted, mask, radius)
    full_radius = np.repeat(np.repeat(radius, bin_factor, axis=0), bin_factor, axis=1)[
        : bgsub.shape[0], : bgsub.shape[1]
    ]
    full_mask = np.repeat(np.repeat(mask, bin_factor, axis=0), bin_factor, axis=1)[: bgsub.shape[0], : bgsub.shape[1]]
    _, _, sigma_pixel = sigma_clipped_stats(bgsub[(full_radius > limit_min_radius_arcsec) & ~full_mask], sigma=3.0)
    naive_sigma_box = sigma_pixel / np.sqrt(100.0 * 100.0)  # 10"x10" = 100x100 native pixels
    result = {
        "label": label,
        "zero_point": zero_point,
        "own_sky_minus_delivered_mu": float(surface_brightness(np.array(abs(own_sky - delivered_sky)), zero_point)),
        "own_sky_sign": "positive" if own_sky - delivered_sky > 0 else "negative",
        "sky_systematic_mu": float(surface_brightness(np.array(sky_systematic), zero_point)),
        "limit_3sigma_10arcsec_bgsub": float(surface_brightness(np.array(3 * sigma_box_bgsub), zero_point)),
        "limit_3sigma_10arcsec_restored": float(surface_brightness(np.array(3 * sigma_box_restored), zero_point)),
        "limit_3sigma_10arcsec_naive_pixel_rms": float(surface_brightness(np.array(3 * naive_sigma_box), zero_point)),
        "number_of_boxes": [boxes_bgsub, boxes_restored],
        "bgmod_peak_mu_near_galaxy": float(
            surface_brightness(np.array(np.nanmax(profiles["bgmod"][1][:10])), zero_point)
        ),
    }
    return {"result": result, "profiles": profiles, "images": binned, "mask": mask, "own_sky": own_sky}


def main() -> None:
    use_publication_style()
    manifest = json.loads((default_data_root / "tiles" / "lsb_manifest.json").read_text())
    analyses = {}
    for key in ["deep_VIS", "wide_VIS", "deep_NIR_H", "wide_NIR_H"]:
        if key not in manifest:
            continue
        files = manifest[key]["files"]
        if not all((Path(manifest[key]["directory"]) / files[kind]).exists() for kind in ("BGSUB", "BKG")):
            print(f"{key}: files missing, skipped")
            continue
        analyses[key] = analyse(key, manifest[key])
        print(json.dumps(analyses[key]["result"]))

    (figure_dir / "dr1_lsb_ngc1483_limits.json").write_text(
        json.dumps({key: value["result"] for key, value in analyses.items()}, indent=2)
    )

    figure = plt.figure(figsize=(figure_width_double, figure_width_double * 0.80))
    grid = figure.add_gridspec(2, 3, height_ratios=[1.0, 1.05], hspace=0.42, wspace=0.62)
    half = region_size_arcsec / 2
    extent = [half, -half, -half, half]

    reference = analyses.get("deep_VIS") or analyses.get("wide_VIS")
    axis = figure.add_subplot(grid[0, 0])
    mu_map = surface_brightness(
        reference["images"]["restored"] - reference["own_sky"], reference["result"]["zero_point"]
    )
    image = axis.imshow(
        np.where(np.isfinite(mu_map), mu_map, 31), origin="lower", extent=extent, cmap="Greys", vmin=21, vmax=29.5
    )
    for semi_major in sky_annulus_arcsec:
        axis.add_patch(
            Ellipse(
                (0, 0),
                2 * semi_major * axis_ratio,
                2 * semi_major,
                angle=-position_angle_deg,
                fill=False,
                ls="--",
                lw=0.6,
                color="tab:blue",
            )
        )
    axis.set_title(r"(a) deep $I_E$, restored", fontsize=7.5)
    colorbar = figure.colorbar(image, ax=axis, fraction=0.046, pad=0.02)
    colorbar.set_label(r"$\mu$ [mag arcsec$^{-2}$]", fontsize=7)
    colorbar.ax.invert_yaxis()
    axis.set_xlabel(r"$\Delta\alpha$ [$''$]")
    axis.set_ylabel(r"$\Delta\delta$ [$''$]")

    for column, key in zip((1, 2), ("deep_VIS", "wide_VIS"), strict=True):
        if key not in analyses:
            continue
        axis = figure.add_subplot(grid[0, column])
        background = analyses[key]["images"]["bgmod"]
        background = background - np.nanmedian(background)
        scale = np.nanpercentile(np.abs(background), 99.5)
        image = axis.imshow(
            background * 1e3, origin="lower", extent=extent, cmap="RdBu_r", vmin=-scale * 1e3, vmax=scale * 1e3
        )
        axis.contour(
            elliptical_radius(background.shape, 1.0),
            levels=[60.0],
            extent=extent,
            colors="k",
            linewidths=0.5,
            origin="lower",
        )
        survey = "(b) deep (10 visits)" if key.startswith("deep") else "(c) wide (1 visit)"
        axis.set_title(rf"{survey}: MER BGMOD, $I_E$", fontsize=7.5)
        colorbar = figure.colorbar(image, ax=axis, fraction=0.046, pad=0.02)
        colorbar.set_label(r"$10^{-3}$ ADU s$^{-1}$ pix$^{-1}$", fontsize=7)
        axis.set_xlabel(r"$\Delta\alpha$ [$''$]")
        axis.set_yticklabels([])

    styles = {
        ("deep", "restored"): ("k", "-", "deep, restored"),
        ("deep", "bgsub"): ("k", ":", "deep, BGSUB"),
        ("wide", "restored"): ("tab:red", "-", "wide, restored"),
        ("wide", "bgsub"): ("tab:red", ":", "wide, BGSUB"),
    }
    for column, band in enumerate(["VIS", "NIR_H"]):
        axis = figure.add_subplot(grid[1, column])
        for survey in ("deep", "wide"):
            key = f"{survey}_{band}"
            if key not in analyses:
                continue
            zero_point = analyses[key]["result"]["zero_point"]
            for kind in ("restored", "bgsub"):
                radius_values, flux, error = analyses[key]["profiles"][kind]
                good = flux > 2 * error
                colour, style, label = styles[(survey, kind)]
                axis.plot(
                    radius_values[good],
                    surface_brightness(flux[good], zero_point),
                    color=colour,
                    ls=style,
                    lw=1.0,
                    label=label,
                )
            limit = analyses[key]["result"]["limit_3sigma_10arcsec_restored"]
            axis.axhline(limit, color=styles[(survey, "restored")][0], lw=0.6, ls="-.", alpha=0.7)
        axis.set_xscale("log")
        axis.set_xlim(2, 230)
        axis.set_ylim(31 if band == "VIS" else 29.5, 18 if band == "VIS" else 17)
        axis.set_xlabel(r"semi-major axis [arcsec]")
        axis.set_ylabel(r"$\mu$ [mag arcsec$^{-2}$]")
        axis.set_title(r"(d) $I_E$ profile" if band == "VIS" else r"(e) $H_E$ profile", fontsize=7.5)
        if column == 0:
            axis.legend(loc="upper right", fontsize=5.5, handlelength=2.2)
        axis.text(
            0.04,
            0.30,
            r"dash-dot: $3\sigma$ ($10''\times10''$)",
            transform=axis.transAxes,
            ha="left",
            va="bottom",
            fontsize=6,
        )

    axis = figure.add_subplot(grid[1, 2])
    for key, colour in (("deep_VIS", "k"), ("wide_VIS", "tab:red"), ("deep_NIR_H", "0.5"), ("wide_NIR_H", "salmon")):
        if key not in analyses:
            continue
        radius_values, restored, restored_error = analyses[key]["profiles"]["restored"]
        _, delivered, _ = analyses[key]["profiles"]["bgsub"]
        positive = restored > 5 * restored_error  # only where the restored profile is well measured
        removed = np.where(positive, 1.0 - delivered / restored, np.nan)
        band = r"$I_E$" if "VIS" in key else r"$H_E$"
        axis.plot(
            radius_values[positive], 100 * removed[positive], color=colour, lw=1.0, label=f"{key.split('_')[0]} {band}"
        )
    axis.axhline(0, color="0.6", lw=0.5)
    axis.set_xscale("log")
    axis.set_xlim(2, 230)
    axis.set_ylim(-10, 85)
    axis.set_xlabel(r"semi-major axis [arcsec]")
    axis.set_ylabel(r"light removed by MER sky [\%]")
    axis.set_title(r"(f) $1-I_{\rm BGSUB}/I_{\rm restored}$", fontsize=7.5)
    axis.legend(loc="upper left", fontsize=6)

    output = figure_dir / "dr1_lsb_ngc1483.png"
    figure.savefig(output)
    print(f"saved {output}")


if __name__ == "__main__":
    main()
