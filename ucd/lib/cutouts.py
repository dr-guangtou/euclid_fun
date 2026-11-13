"""Small Euclid (VIS, Y, J, H) and Legacy Surveys cutouts centred on the Gaia position, and colour composites."""

import io
import json
import time

import numpy as np
import requests
from astropy.io import fits
from astropy.visualization import make_lupton_rgb
from PIL import Image
from scipy import ndimage

from ucd.lib import euclid_catalogue

euclid_bands = ("VIS", "NIR_Y", "NIR_J", "NIR_H")
half_size_arcmin = 0.1  # 12 arcsec box on the 0.1 arcsec mosaic grid


def mosaic_lookup(representatives: dict, cache_path) -> dict:
    """File path, name and zero point of the four mosaics of each tile; one archive query per tile, cached as JSON."""
    lookup = json.loads(cache_path.read_text()) if cache_path.exists() else {}
    for tile, (ra_deg, dec_deg) in representatives.items():
        if str(tile) in lookup:
            continue
        mosaics = euclid_catalogue.find_mosaics(ra_deg, dec_deg)
        entry = {}
        for row in mosaics:
            if int(row["tile_index"]) == int(tile) and row["filter_name"] in euclid_bands:
                entry[str(row["filter_name"])] = {
                    "file_path": str(row["file_path"]),
                    "file_name": str(row["file_name"]),
                    "zero_point": float(row["zero_point"]),
                }
        lookup[str(tile)] = entry
        cache_path.write_text(json.dumps(lookup, indent=1))
    return lookup


def fetch_euclid(tile_entry: dict, ra_deg: float, dec_deg: float, folder, label: str) -> dict:
    """Download the four band cutouts of one object; returns {band: path} for those that succeeded."""
    paths = {}
    for band in euclid_bands:
        if band not in tile_entry:
            continue
        path = folder / f"{label}_{band.lower()}.fits"
        try:
            euclid_catalogue.get_cutout(
                tile_entry[band]["file_path"], tile_entry[band]["file_name"], ra_deg, dec_deg, half_size_arcmin, path
            )
            paths[band] = path
        except Exception as error:
            print(f"    cutout failed for {label} {band}: {type(error).__name__}")
    return paths


def fetch_legacy_jpeg(config: dict, ra_deg: float, dec_deg: float, path, *, size_pixels: int = 120) -> str | None:
    """Legacy Surveys grz JPEG at 0.1 arcsec per pixel; tries the configured layers in order, returns the one used."""
    if path.exists():
        return "cached"
    for layer in config["legacy"]["cutout_layers"]:
        for attempt in range(3):
            try:
                response = requests.get(
                    f"{config['legacy']['cutout_url']}/jpeg-cutout",
                    params={"ra": ra_deg, "dec": dec_deg, "layer": layer, "pixscale": 0.1, "size": size_pixels},
                    timeout=60,
                )
                response.raise_for_status()
                image = np.asarray(Image.open(io.BytesIO(response.content)).convert("RGB"))
                if len(np.unique(image.reshape(-1, 3), axis=0)) > 10:  # placeholder tiles have a handful of colours
                    path.write_bytes(response.content)
                    return layer
                break
            except Exception:
                time.sleep(2 * (attempt + 1))
    return None


def read_flux(path, zero_point: float) -> np.ndarray:
    """Cutout in micro-jansky per pixel with the local sky (border median) removed."""
    data = fits.getdata(path).astype(float) * 10 ** (-0.4 * (zero_point - 23.9))
    border = np.concatenate([data[:6].ravel(), data[-6:].ravel(), data[:, :6].ravel(), data[:, -6:].ravel()])
    return data - np.nanmedian(border)


def vis_greyscale(vis: np.ndarray) -> np.ndarray:
    """Arcsinh-stretched VIS image scaled to 0-1 (noise visible, core not saturated)."""
    border = np.concatenate([vis[:8].ravel(), vis[-8:].ravel()])
    noise = 1.4826 * np.nanmedian(np.abs(border - np.nanmedian(border))) + 1e-12
    scaled = np.arcsinh(vis / (3 * noise))
    upper = np.arcsinh(np.nanmax(vis) / (3 * noise))
    return np.clip((scaled + 1.0) / (upper + 1.0), 0, 1)


def euclid_colour(images: dict) -> np.ndarray | None:
    """Colour composite: red = H, green = (Y + J) / 2, blue = VIS; channels balanced for an old stellar population."""
    if not all(band in images for band in euclid_bands):
        return None
    shape = min(image.shape for image in images.values())
    crop = {band: np.nan_to_num(image[: shape[0], : shape[1]]) for band, image in images.items()}
    # VIS is much sharper than NISP; smooth it so that compact cores do not turn blue.
    red = crop["NIR_H"] * 0.75
    green = 0.5 * (crop["NIR_Y"] + crop["NIR_J"])
    blue = ndimage.gaussian_filter(crop["VIS"], 1.5) * 1.9
    peak = max(float(np.nanpercentile(green, 99.0)), 1e-9)
    return make_lupton_rgb(red / peak, green / peak, blue / peak, stretch=0.6, Q=8, minimum=-0.02)
