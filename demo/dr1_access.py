"""Small, dependency-light helpers for Euclid DR1 data access (ESA Euclid Science Archive).

Everything here was tested against the archive on the DR1-Foundation release day (2026-11-12):

* catalogue and metadata queries go through TAP (ADQL) via ``astroquery.esa.euclid``;
* mosaic tiles are found with ``INTERSECTS(CIRCLE(ra, dec, r), fov)`` on ``dr1.mosaic_product``
  (the SIA service did not index DR1 yet);
* cutouts of background-subtracted (BGSUB) mosaics and FLAG maps come from the cutout service;
* full files (BGMOD background models, RMS maps, PSFs, star masks, catalogues) are streamed from the
  data service with ``release=dr1`` (anonymous access works; the Q1 default ``sedm`` gives HTTP 401).

Pixel units of MER mosaics: VIS in ADU/s, NISP and EXT in arbitrary scaled units; in all cases
``m_AB = -2.5 log10(value) + ZP`` with ZP = header ``MAGZERO`` (= ``zero_point`` column of
``dr1.mosaic_product``). Catalogue fluxes are in microJansky (``m_AB = -2.5 log10(flux) + 23.9``).
"""

from __future__ import annotations

import time
from dataclasses import dataclass
from pathlib import Path

import astropy.units as u
import numpy as np
import requests
from astropy.coordinates import SkyCoord
from astropy.io import fits
from astropy.table import Table
from astroquery.esa.euclid import Euclid

data_service_url = "https://eas.esac.esa.int/sas-dd/data"
cutout_service_url = "https://eas.esac.esa.int/sas-cutout/cutout"
default_data_root = Path.home() / "data" / "euclid" / "dr1_demo"
mosaic_pixel_scale_arcsec = 0.1
catalogue_zero_point_ujy = 23.9

# The three ways DR1 mosaics were produced (see kb/03_data_access.md):
#   wide survey tiles (32'x32', TILEID 102...): release DR1_R2, purpose DATA_RELEASE, processing_mode WIDE
#   deep-field stacks (17'x17', TILEID 101...): release DR1_R1, purpose DATA_RELEASE_DEEP, processing_mode DEEP
#   single deep-field visits at wide depth:     purpose DATA_RELEASE_DEEP, processing_mode WIDE (one per visit)
wide_survey_selection = {"release_name": "DR1_R2", "purpose": "DATA_RELEASE", "processing_mode": "WIDE"}
deep_survey_selection = {"release_name": "DR1_R1", "purpose": "DATA_RELEASE_DEEP", "processing_mode": "DEEP"}


@dataclass
class Target:
    name: str
    ra_deg: float
    dec_deg: float
    galaxy_type: str
    source_paper: str
    note: str = ""

    @property
    def coordinate(self) -> SkyCoord:
        return SkyCoord(self.ra_deg * u.deg, self.dec_deg * u.deg)

    @property
    def slug(self) -> str:
        return "".join(character if character.isalnum() else "_" for character in self.name).strip("_").lower()


def run_query(adql: str, *, retries: int = 3) -> Table:
    """Run an asynchronous ADQL query on the public Euclid archive and return an astropy Table."""
    for attempt in range(1, retries + 1):
        try:
            return Euclid.launch_job_async(adql, verbose=False).get_results()
        except Exception:  # network hiccups are common for long queries; retry quietly
            if attempt == retries:
                raise
            time.sleep(5 * attempt)
    raise RuntimeError("unreachable")


def selection_clause(selection: dict[str, str], alias: str = "") -> str:
    prefix = f"{alias}." if alias else ""
    return " AND ".join(f"{prefix}{key} = '{value}'" for key, value in selection.items())


def find_mosaics(
    ra_deg: float,
    dec_deg: float,
    *,
    selection: dict[str, str] | None = None,
    instruments: tuple[str, ...] = ("VIS", "NISP"),
    margin_deg: float = 0.0,
) -> Table:
    """Return the DR1 MER mosaics whose footprint contains (ra, dec), one row per band and tile.

    A few tiles (e.g. 102158273) have two mosaic files per band in the same release; only the most
    recently created file is kept (the older one can fail in the cutout service).
    """
    selection = selection or wide_survey_selection
    instrument_list = ", ".join(f"'{name}'" for name in instruments)
    adql = (
        "SELECT mosaic_product_oid, tile_index, instrument_name, filter_name, file_name, file_path, "
        "zero_point, release_name, purpose, processing_mode, ra, dec, creation_date "
        "FROM dr1.mosaic_product "
        f"WHERE INTERSECTS(CIRCLE({ra_deg}, {dec_deg}, {max(margin_deg, 1e-4)}), fov) = 1 "
        f"AND instrument_name IN ({instrument_list}) AND {selection_clause(selection)} "
        "ORDER BY tile_index, filter_name, creation_date DESC"
    )
    table = run_query(adql)
    if len(table) == 0:
        return table
    keys = [f"{tile}_{band}" for tile, band in zip(table["tile_index"], table["filter_name"], strict=True)]
    _, first_index = np.unique(keys, return_index=True)
    return table[np.sort(first_index)]


def pick_tile(mosaics: Table, ra_deg: float, dec_deg: float) -> int:
    """Choose the tile whose centre is closest to the target (the target is then far from tile edges)."""
    target = SkyCoord(ra_deg * u.deg, dec_deg * u.deg)
    centres = SkyCoord(np.asarray(mosaics["ra"], float) * u.deg, np.asarray(mosaics["dec"], float) * u.deg)
    return int(mosaics["tile_index"][int(np.argmin(target.separation(centres)))])


def find_auxiliary_files(mosaic_product_oid: int) -> Table:
    """Auxiliary MER files of one mosaic: RMS, FLAG, BKG (BGMOD), PSF, GRID_PSF, BRIGHT_STAR_MASKS, LAYERS, ..."""
    return run_query(
        "SELECT stype, file_name, file_path FROM dr1.aux_mosaic "
        f"WHERE mosaic_product_oid = {int(mosaic_product_oid)} ORDER BY stype"
    )


def download_file(file_name: str, output_dir: Path, *, overwrite: bool = False, chunk_bytes: int = 8 << 20) -> Path:
    """Stream one archive file (any DR1 product) to output_dir; skips files that already exist."""
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / file_name
    if output_path.exists() and output_path.stat().st_size > 0 and not overwrite:
        return output_path
    partial_path = output_path.with_suffix(output_path.suffix + ".part")
    parameters = {"file_name": file_name, "release": "dr1", "RETRIEVAL_TYPE": "FILE"}
    with requests.get(data_service_url, params=parameters, stream=True, timeout=600) as response:
        if response.status_code != 200:
            raise RuntimeError(f"download of {file_name} failed with HTTP {response.status_code}")
        with partial_path.open("wb") as handle:
            for chunk in response.iter_content(chunk_size=chunk_bytes):
                handle.write(chunk)
    partial_path.rename(output_path)
    return output_path


fits_block_bytes = 2880


def range_get(file_name: str, start: int, length: int, *, attempts: int = 6) -> bytes:
    """Bytes [start, start + length) of an archive file via an HTTP range request (the data service answers 206).

    Each request costs several seconds of latency, so ask for few large ranges rather than many small ones.
    The server drops reused keep-alive connections: every request opens a fresh one.
    """
    parameters = {"file_name": file_name, "release": "dr1", "RETRIEVAL_TYPE": "FILE"}
    for attempt in range(attempts):
        try:
            response = requests.get(
                data_service_url,
                params=parameters,
                headers={"Range": f"bytes={start}-{start + length - 1}", "Connection": "close"},
                timeout=600,
            )
            if response.status_code == 206 and len(response.content) == length:
                return response.content
        except requests.RequestException:
            pass
        time.sleep(3 * (attempt + 1))
    raise RuntimeError(f"range request failed for {file_name} at byte {start}")


def remote_file_size(file_name: str) -> int:
    parameters = {"file_name": file_name, "release": "dr1", "RETRIEVAL_TYPE": "FILE"}
    return int(requests.head(data_service_url, params=parameters, timeout=120).headers["Content-Length"])


def read_remote_header(file_name: str, offset: int = 0) -> tuple[fits.Header, int]:
    """FITS header starting at byte `offset` of an archive file, and its size in bytes (whole 2880-byte blocks)."""
    raw = b""
    while True:
        raw += range_get(file_name, offset + len(raw), 4 * fits_block_bytes)
        text = raw.decode("ascii", errors="replace")
        for card_start in range(0, len(text), 80):
            if text[card_start : card_start + 8] == "END     ":
                header_bytes = (card_start // fits_block_bytes + 1) * fits_block_bytes
                return fits.Header.fromstring(text[: card_start + 80]), header_bytes


def remote_rows_cutout(file_name: str, coordinate: SkyCoord, half_size_arcmin: float) -> tuple[np.ndarray, fits.Header]:
    """Square cutout of a single-HDU mosaic (e.g. BGMOD or RMS, which the cutout service rejects) from one range
    request covering only the image rows around the target. Returns the cutout and a header with its WCS."""
    from astropy.nddata import Cutout2D
    from astropy.wcs import WCS

    header, header_bytes = read_remote_header(file_name)
    if header["NAXIS"] != 2 or header.get("BZERO", 0) or header.get("BSCALE", 1) != 1:
        raise ValueError("expected an unscaled two-dimensional primary image")
    wcs = WCS(header)
    width, height = header["NAXIS1"], header["NAXIS2"]
    pixel_bytes = abs(header["BITPIX"]) // 8
    x_centre, y_centre = wcs.world_to_pixel(coordinate)
    half_pixels = half_size_arcmin / 60.0 / abs(wcs.proj_plane_pixel_scales()[1].to_value(u.deg))
    first_row = int(np.clip(np.floor(y_centre - half_pixels) - 1, 0, height - 1))
    last_row = int(np.clip(np.ceil(y_centre + half_pixels) + 1, 0, height - 1))
    row_count = last_row - first_row + 1
    raw = range_get(file_name, header_bytes + first_row * width * pixel_bytes, row_count * width * pixel_bytes)
    dtype = {-32: ">f4", -64: ">f8", 16: ">i2", 32: ">i4", 8: "u1"}[header["BITPIX"]]
    big_endian = np.dtype(dtype)
    strip = np.frombuffer(raw, dtype=big_endian).reshape(row_count, width).astype(big_endian.newbyteorder("="))
    strip_wcs = wcs.slice((slice(first_row, last_row + 1), slice(None)))
    cutout = Cutout2D(strip, coordinate, 2 * half_size_arcmin * u.arcmin, wcs=strip_wcs, mode="partial")
    cutout_header = header.copy()
    cutout_header.update(cutout.wcs.to_header())
    return cutout.data, cutout_header


def get_cutout(
    file_path: str,
    file_name: str,
    ra_deg: float,
    dec_deg: float,
    radius_arcmin: float,
    output_path: Path,
    *,
    overwrite: bool = False,
    retries: int = 4,
) -> Path:
    """Cut a square of half-size radius_arcmin out of a BGSUB mosaic (or FLAG map) on the server."""
    if output_path.exists() and output_path.stat().st_size > 0 and not overwrite:
        return output_path
    output_path.parent.mkdir(parents=True, exist_ok=True)
    parameters = {
        "filepath": f"{file_path}/{file_name}",
        "POS": f"CIRCLE,{ra_deg},{dec_deg},{radius_arcmin / 60.0}",
    }
    # The service occasionally answers HTTP 200 with a non-FITS body under load: retry with back-off.
    for attempt in range(1, retries + 1):
        response = requests.get(cutout_service_url, params=parameters, timeout=600)
        if response.status_code == 200 and response.content.startswith(b"SIMPLE"):
            output_path.write_bytes(response.content)
            return output_path
        time.sleep(10 * attempt)
    raise RuntimeError(f"cutout of {file_name} failed after {retries} attempts (HTTP {response.status_code})")


def read_image(path: Path, extension: int | str = 0) -> tuple[np.ndarray, fits.Header]:
    with fits.open(path, memmap=False) as hdu_list:
        hdu = hdu_list[extension]
        if hdu.data is None and len(hdu_list) > 1:
            hdu = hdu_list[1]
        return np.asarray(hdu.data, dtype=np.float32), hdu.header.copy()


def pixel_to_ujy(values: np.ndarray, zero_point: float) -> np.ndarray:
    """Convert MER mosaic pixel values to microJansky per pixel."""
    return values * 10.0 ** (-0.4 * (zero_point - catalogue_zero_point_ujy))


def surface_brightness(values: np.ndarray, zero_point: float, pixel_scale_arcsec: float = 0.1) -> np.ndarray:
    """mag/arcsec^2 from pixel values; NaN where values <= 0."""
    with np.errstate(divide="ignore", invalid="ignore"):
        result = -2.5 * np.log10(values) + zero_point + 5.0 * np.log10(pixel_scale_arcsec)
    return np.where(values > 0, result, np.nan)


def query_mer_sources(
    ra_deg: float,
    dec_deg: float,
    radius_arcsec: float,
    *,
    catalogue: str = "dr1.mer_catalogue_wide_survey",
    columns: str = "*",
) -> Table:
    """Cone search on a DR1 MER catalogue table (the only MER tables carrying coordinates)."""
    radius_deg = radius_arcsec / 3600.0
    return run_query(
        f"SELECT {columns}, DISTANCE({ra_deg}, {dec_deg}, right_ascension, declination) * 3600.0 AS separation_arcsec "
        f"FROM {catalogue} "
        f"WHERE 1 = CONTAINS(POINT(right_ascension, declination), CIRCLE({ra_deg}, {dec_deg}, {radius_deg})) "
        "ORDER BY separation_arcsec"
    )
