"""Step 2 of the demo: colour gallery of DR1 galaxies of different types taken from the DR1 papers.

Colour mapping: R = H_E, G = mean(Y_E, J_E), B = I_E (VIS), each converted to microJy per pixel with its
mosaic zero point, then an arcsinh (Lupton et al. 2004) stretch. All four bands are on the common
0.1 arcsec/pixel MER grid, so no resampling is needed; the NISP bands have a ~0.5 arcsec PSF, so colour
detail is NIR-limited while the luminance is dominated by VIS on small scales.

Usage: uv run python demo/02_gallery.py   ->  figures/dr1_gallery.png
"""

import json
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from astropy.visualization import make_lupton_rgb
from dr1_access import default_data_root, pixel_to_ujy, read_image
from scipy.ndimage import gaussian_filter, median_filter
from targets import gallery_targets

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from plot_style import figure_width_double, use_publication_style  # noqa: E402

figure_dir = Path(__file__).resolve().parents[1] / "figures"


def load_bands(target_dir: Path) -> tuple[dict[str, np.ndarray], dict]:
    metadata = json.loads((target_dir / "metadata.json").read_text())
    images = {}
    for band, info in metadata["bands"].items():
        data, _ = read_image(target_dir / info["file"])
        images[band] = pixel_to_ujy(np.nan_to_num(data, nan=0.0), info["zero_point"])
    return images, metadata


# (stretch in units of the sky noise, Q) of the arcsinh mapping, tuned per object: low stretch values bring out
# low-surface-brightness light, high values keep bright galaxy centres unsaturated.
display_parameters = {
    "NGC 1483": (60.0, 12.0),
    "PGC 61126": (60.0, 12.0),
    "LVDw 11 (LEDA 166124)": (2.5, 8.0),
    "LVDw 9": (2.5, 8.0),
    "J170734+555259": (25.0, 10.0),
    "J022455-601236": (12.0, 8.0),
    "J100937+724953": (6.0, 8.0),
    "J042911-204453": (25.0, 10.0),
}


def clean_nir(image: np.ndarray) -> np.ndarray:
    """3x3 median (kills isolated hot pixels / cosmic rays) then a 1-pixel Gaussian (NIR PSF FWHM ~5 pixels)."""
    return gaussian_filter(median_filter(image, size=3), sigma=1.0)


def robust_sigma(image: np.ndarray) -> float:
    finite = image[np.isfinite(image) & (image != 0)]
    return float(1.4826 * np.median(np.abs(finite - np.median(finite))))


def make_rgb(images: dict[str, np.ndarray], stretch: float, q_value: float) -> np.ndarray:
    red = clean_nir(images["NIR_H"])
    green = clean_nir(0.5 * (images["NIR_Y"] + images["NIR_J"]))
    blue = gaussian_filter(images["VIS"], sigma=0.7)
    shape = np.min([red.shape, green.shape, blue.shape], axis=0)
    red, green, blue = (array[: shape[0], : shape[1]] for array in (red, green, blue))
    # Normalise each channel by its robust sky noise so that faint structure has a neutral colour.
    red, green, blue = (array / max(robust_sigma(array), 1e-12) for array in (red, green, blue))
    return make_lupton_rgb(red, green, blue, minimum=-0.5, stretch=stretch, Q=q_value)


def main() -> None:
    use_publication_style()
    figure, axes = plt.subplots(2, 4, figsize=(figure_width_double, figure_width_double * 0.56))
    for axis, target in zip(axes.flat, gallery_targets, strict=False):
        target_dir = default_data_root / "cutouts" / target.slug
        if not (target_dir / "metadata.json").exists():
            axis.set_axis_off()
            continue
        images, metadata = load_bands(target_dir)
        rgb = make_rgb(images, *display_parameters[target.name])
        size_arcsec = rgb.shape[0] * 0.1
        extent = [-size_arcsec / 2, size_arcsec / 2, -size_arcsec / 2, size_arcsec / 2]
        axis.imshow(rgb, extent=extent, origin="lower")
        axis.set_xticks([])
        axis.set_yticks([])
        bar = 30.0 if size_arcsec > 120 else (10.0 if size_arcsec > 40 else 5.0)
        x0 = extent[0] + 0.07 * size_arcsec
        y0 = extent[2] + 0.08 * size_arcsec
        axis.plot([x0, x0 + bar], [y0, y0], color="white", lw=1.2)
        axis.text(
            x0 + bar / 2,
            y0 + 0.03 * size_arcsec,
            rf"${bar:.0f}''$",
            color="white",
            ha="center",
            va="bottom",
            fontsize=7,
        )
        axis.set_title(target.name.replace("(LEDA 166124)", ""), fontsize=8, pad=2)
        axis.text(
            0.03, 0.97, target.galaxy_type, transform=axis.transAxes, color="white", fontsize=6.5, ha="left", va="top"
        )
        axis.text(
            0.97,
            0.03,
            f"tile {metadata['tile_index']}",
            transform=axis.transAxes,
            color="0.85",
            fontsize=5.5,
            ha="right",
            va="bottom",
        )
    figure.subplots_adjust(wspace=0.03, hspace=0.12)
    figure_dir.mkdir(exist_ok=True)
    output = figure_dir / "dr1_gallery.png"
    figure.savefig(output)
    print(f"saved {output}")


if __name__ == "__main__":
    main()
