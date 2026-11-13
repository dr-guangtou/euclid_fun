"""Step 9 of the demo: cut a small region out of DR1 calibrated single exposures without downloading whole files.

The ESA data service honours HTTP range requests (HTTP 206, `Accept-Ranges: bytes`), and the calibrated frames have a
regular layout: a primary header followed by one (SCI, RMS, FLG/DQ) triple per detector unit (VIS: 144 CCD
quadrants of 2048 x 2066 px; NISP: 16 detectors of 2040 x 2040 px), every triple the same size. So:

  1. the layout of a file follows from its first headers plus the total size (HTTP HEAD);
  2. a focal-plane model (the sky corners of every unit relative to the pointing `ra`, `dec`, `pa` of
     `dr1.calibrated_frame`) is built once per instrument from one exposure's SCI headers and cached;
  3. for each exposure covering a target, the model predicts which units overlap a circle of the requested
     radius, and each such unit is fetched with one contiguous range request (SCI + RMS + FLG/DQ, ~50 MB);
  4. the region is cut out with the unit's own WCS and written to a small FITS file.

Target: ESO 248-G006, the BCG of Abell 3112 (z = 0.075, so 1' is about 86 kpc), observation 5897.
Outputs: ~/data/euclid/dr1_demo/frames/abell3112_bcg/*.fits, figures/dr1_frame_cutouts.json (units, bytes, time).

Usage: uv run python demo/09_frame_cutouts.py [--radius-arcmin 0.5] [--bands VIS NIR_Y NIR_J NIR_H] [--dry-run]
"""

import argparse
import io
import json
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import astropy.units as u
import numpy as np
from astropy.coordinates import SkyCoord
from astropy.io import fits
from astropy.nddata import Cutout2D
from astropy.wcs import WCS
from dr1_access import default_data_root, range_get, read_remote_header, remote_file_size, run_query

target_name = "ESO 248-G006 (Abell 3112 BCG)"
target_slug = "abell3112_bcg"
target = SkyCoord(49.4903, -44.2381, unit="deg")
frame_dir = default_data_root / "frames"
figure_dir = Path(__file__).resolve().parents[1] / "figures"
fits_block = 2880  # FITS block size in bytes
hdus_per_unit = 3


def data_size(header: fits.Header) -> int:
    if header.get("NAXIS", 0) == 0:
        return 0
    size = abs(header["BITPIX"]) // 8
    for axis in range(1, header["NAXIS"] + 1):
        size *= header[f"NAXIS{axis}"]
    return -(-size // fits_block) * fits_block


def file_layout(file_name: str) -> dict:
    """Primary size, size of one (SCI, RMS, FLG/DQ) unit and the number of units; checked against the file size."""
    primary_header, primary_bytes = read_remote_header(file_name, 0)
    offset = primary_bytes
    hdu_spans = []
    for _ in range(hdus_per_unit):
        header, header_bytes = read_remote_header(file_name, offset)
        hdu_spans.append((header.get("EXTNAME"), header_bytes, data_size(header)))
        offset += header_bytes + data_size(header)
    unit_bytes = offset - primary_bytes
    total = remote_file_size(file_name)
    unit_count, remainder = divmod(total - primary_bytes, unit_bytes)
    if remainder:
        raise ValueError(f"{file_name}: irregular layout")
    return {
        "primary_bytes": primary_bytes,
        "unit_bytes": unit_bytes,
        "unit_count": unit_count,
        "sci_header_bytes": hdu_spans[0][1],
        "total_bytes": total,
        "primary_header": primary_header.tostring(),
    }


def pointing_frame(row) -> "SkyCoord":
    centre = SkyCoord(float(row["ra"]), float(row["dec"]), unit="deg")
    return centre.skyoffset_frame(rotation=float(row["pa"]) * u.deg)


def build_focal_plane_model(reference_row, workers: int = 12) -> dict:
    """Sky corners of every unit, as offsets in the rotated frame of the reference pointing (cached per instrument)."""
    instrument = str(reference_row["instrument_name"])
    path = frame_dir / f"focal_plane_model_{instrument.lower()}.json"
    if path.exists():
        return json.loads(path.read_text())
    file_name = str(reference_row["file_name"])
    layout = file_layout(file_name)
    offsets = [layout["primary_bytes"] + index * layout["unit_bytes"] for index in range(layout["unit_count"])]
    with ThreadPoolExecutor(max_workers=workers) as pool:
        headers = list(pool.map(lambda offset: read_remote_header(file_name, offset)[0], offsets))
    frame = pointing_frame(reference_row)
    units = []
    for index, header in enumerate(headers):
        wcs = WCS(header)
        width, height = header["NAXIS1"], header["NAXIS2"]
        corners = wcs.pixel_to_world([0, width - 1, width - 1, 0], [0, 0, height - 1, height - 1])
        offsets_in_frame = corners.transform_to(frame)
        units.append(
            {
                "index": index,
                "extname": header["EXTNAME"],
                "lon_deg": offsets_in_frame.lon.deg.tolist(),
                "lat_deg": offsets_in_frame.lat.deg.tolist(),
            }
        )
    model = {"instrument": instrument, "reference_file": file_name, "layout": layout, "units": units}
    frame_dir.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(model))
    return model


def polygon_hits_circle(corners_arcmin: np.ndarray, radius_arcmin: float) -> bool:
    """Does a convex quadrilateral (tangent plane at the target, arcmin) overlap a circle of the radius at (0, 0)?"""
    x, y = corners_arcmin[:, 0], corners_arcmin[:, 1]
    edges = np.roll(corners_arcmin, -1, axis=0) - corners_arcmin
    cross = edges[:, 0] * (-y) - edges[:, 1] * (-x)
    if np.all(cross >= 0) or np.all(cross <= 0):
        return True  # target inside the unit
    for start, edge in zip(corners_arcmin, edges, strict=True):
        fraction = np.clip(-(start @ edge) / (edge @ edge), 0.0, 1.0)
        if np.hypot(*(start + fraction * edge)) <= radius_arcmin:
            return True
    return False


def units_overlapping(model: dict, row, radius_arcmin: float) -> list[int]:
    frame = pointing_frame(row)
    target_frame = target.skyoffset_frame()
    hits = []
    for unit in model["units"]:
        corners = SkyCoord(unit["lon_deg"] * u.deg, unit["lat_deg"] * u.deg, frame=frame).transform_to(target_frame)
        corners_arcmin = np.column_stack([corners.lon.arcmin, corners.lat.arcmin])
        if polygon_hits_circle(corners_arcmin, radius_arcmin):
            hits.append(unit["index"])
    return hits


def fetch_unit_cutout(row, layout: dict, unit_index: int, size_arcmin: float, output_dir: Path) -> dict:
    file_name = str(row["file_name"])
    start = layout["primary_bytes"] + unit_index * layout["unit_bytes"]
    clock = time.perf_counter()
    raw = range_get(file_name, start, layout["unit_bytes"])
    seconds = time.perf_counter() - clock
    with fits.open(io.BytesIO(fits.Header.fromstring(layout["primary_header"]).tostring().encode() + raw)) as unit:
        hdus = [fits.PrimaryHDU(header=fits.Header.fromstring(layout["primary_header"]))]
        inside = False
        for hdu in unit[1:]:
            wcs = WCS(hdu.header)
            cutout = Cutout2D(
                hdu.data,
                target,
                size_arcmin * u.arcmin,
                wcs=wcs,
                mode="partial",
                fill_value=np.nan if hdu.data.dtype.kind == "f" else 0,
            )
            header = hdu.header.copy()
            header.update(cutout.wcs.to_header(relax=True))
            for key in ("NAXIS1", "NAXIS2"):
                header.remove(key, ignore_missing=True)
            hdus.append(fits.ImageHDU(cutout.data, header=header, name=hdu.name))
            inside |= bool(np.isfinite(cutout.data).any()) if hdu.data.dtype.kind == "f" else False
        output_dir.mkdir(parents=True, exist_ok=True)
        output = output_dir / f"{Path(file_name).stem}_unit{unit_index:03d}.fits"
        fits.HDUList(hdus).writeto(output, overwrite=True)
    return {"unit": unit_index, "bytes": len(raw), "seconds": seconds, "file": output.name, "has_data": inside}


def exposures_covering(radius_deg: float = 0.6):
    return run_query(
        "SELECT observation_id, instrument_name, filter_name, ra, dec, pa, duration, start_time_mjd, file_name "
        "FROM dr1.calibrated_frame WHERE 1 = CONTAINS(POINT('ICRS', ra, dec), "
        f"CIRCLE('ICRS', {target.ra.deg}, {target.dec.deg}, {radius_deg})) ORDER BY start_time_mjd"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--radius-arcmin", type=float, default=0.5, help="half-size of the region to cut out")
    parser.add_argument("--field-radius-arcmin", type=float, default=4.5, help="radius used only for counting units")
    parser.add_argument("--bands", nargs="+", default=["VIS", "NIR_Y", "NIR_J", "NIR_H"])
    parser.add_argument("--dry-run", action="store_true", help="count units and bytes, download nothing")
    arguments = parser.parse_args()

    exposures = exposures_covering()
    is_short_vis = (exposures["instrument_name"] == "VIS") & (exposures["duration"] < 100.0)
    long_exposures = exposures[~is_short_vis]  # drop the 89.5 s VIS short exposures
    models = {}
    summary = {"target": target_name, "ra": target.ra.deg, "dec": target.dec.deg, "exposures": []}
    for row in long_exposures:
        if str(row["filter_name"]) not in arguments.bands:
            continue
        instrument = str(row["instrument_name"])
        if instrument not in models:
            models[instrument] = build_focal_plane_model(row)
        model = models[instrument]
        science_units = units_overlapping(model, row, arguments.radius_arcmin)
        field_units = units_overlapping(model, row, arguments.field_radius_arcmin)
        entry = {
            "file": str(row["file_name"]),
            "observation": str(row["observation_id"]),
            "filter": str(row["filter_name"]),
            "units_science": science_units,
            "units_field": len(field_units),
            "unit_bytes": model["layout"]["unit_bytes"],
            "file_bytes": model["layout"]["total_bytes"],
        }
        print(
            f"{entry['filter']:6s} {entry['file'][:44]}: units within {arguments.radius_arcmin}' = {science_units}, "
            f"within {arguments.field_radius_arcmin}' = {len(field_units)} of {model['layout']['unit_count']}",
            flush=True,
        )
        if science_units and not arguments.dry_run:
            entry["downloads"] = [
                fetch_unit_cutout(row, model["layout"], index, 2 * arguments.radius_arcmin, frame_dir / target_slug)
                for index in science_units
            ]
            for download in entry["downloads"]:
                print(
                    f"    unit {download['unit']:3d}: {download['bytes'] / 1e6:6.1f} MB in {download['seconds']:5.1f} s"
                    f" -> {download['file']} (data at target: {download['has_data']})",
                    flush=True,
                )
        summary["exposures"].append(entry)
    total_bytes = sum(d["bytes"] for e in summary["exposures"] for d in e.get("downloads", []))
    total_seconds = sum(d["seconds"] for e in summary["exposures"] for d in e.get("downloads", []))
    summary["downloaded_bytes"], summary["download_seconds"] = total_bytes, total_seconds
    print(f"downloaded {total_bytes / 1e6:.0f} MB in {total_seconds:.0f} s")
    suffix = "_dry_run" if arguments.dry_run else ""
    output = figure_dir / f"dr1_frame_cutouts{suffix}.json"
    output.write_text(json.dumps(summary, indent=2))
    print("wrote", output)


if __name__ == "__main__":
    main()
