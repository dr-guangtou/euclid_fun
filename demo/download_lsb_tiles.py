"""Download the full MER tile products needed for the low-surface-brightness demo (NGC 1483).

For the wide tile (32'x32', ~1.5 GB per layer) and the EDF-South deep tile (17'x17', ~0.4 GB per layer)
this fetches, for VIS and NIR_H: the BGSUB mosaic, the subtracted background model (BGMOD), and
for VIS also the RMS and FLAG maps, plus the PSF products. Files go to ~/data/euclid/dr1_demo/tiles/<tile>/.

Usage: uv run python demo/download_lsb_tiles.py [--dry_run]
"""

import argparse
import json
import time

from dr1_access import default_data_root, download_file, find_auxiliary_files, run_query, selection_clause
from targets import lsb_selections

wanted_auxiliary = {"VIS": {"BKG", "RMS", "FLAG", "PSF", "GRID_PSF", "BRIGHT_STAR_MASKS"}, "NIR_H": {"BKG", "PSF"}}
# Skipped to stay within the ~15 GB budget: the wide FLAG and RMS maps (1.5 GB each; FLAG cutouts come from the
# cutout service and the noise is measured empirically) and the per-object CATALOG-PSF files (0.7-2 GB each;
# GRID-PSF is kept for VIS). One wide NIR_H CATALOG-PSF was already fetched in a first run and is kept.
skipped = {
    ("wide", "VIS", "FLAG"),
    ("wide", "VIS", "RMS"),
    ("wide", "VIS", "PSF"),
    ("deep", "VIS", "PSF"),
    ("deep", "NIR_H", "PSF"),
    ("deep", "VIS", "GRID_PSF"),
}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry_run", action="store_true")
    arguments = parser.parse_args()

    manifest = {}
    for label, (selection, tile_index) in lsb_selections.items():
        mosaics = run_query(
            "SELECT mosaic_product_oid, filter_name, file_name, zero_point FROM dr1.mosaic_product "
            f"WHERE tile_index = {tile_index} AND {selection_clause(selection)} AND filter_name IN ('VIS', 'NIR_H')"
        )
        output_dir = default_data_root / "tiles" / str(tile_index)
        for mosaic in mosaics:
            band = str(mosaic["filter_name"])
            files = {"BGSUB": str(mosaic["file_name"])}
            for row in find_auxiliary_files(int(mosaic["mosaic_product_oid"])):
                if str(row["stype"]) in wanted_auxiliary[band] and (label, band, str(row["stype"])) not in skipped:
                    files[str(row["stype"])] = str(row["file_name"])
            manifest[f"{label}_{band}"] = {
                "tile_index": tile_index,
                "zero_point": float(mosaic["zero_point"]),
                "directory": str(output_dir),
                "files": files,
            }
            for kind, file_name in files.items():
                if arguments.dry_run:
                    print(f"[dry run] {label} {band} {kind}: {file_name}")
                    continue
                start = time.time()
                path = download_file(file_name, output_dir)
                size_mb = path.stat().st_size / 1e6
                print(f"{label} {band} {kind}: {size_mb:.0f} MB in {time.time() - start:.0f} s", flush=True)

    manifest_path = default_data_root / "tiles" / "lsb_manifest.json"
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, indent=2))
    print(f"manifest: {manifest_path}")


if __name__ == "__main__":
    main()
