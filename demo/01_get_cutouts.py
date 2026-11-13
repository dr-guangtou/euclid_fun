"""Step 1 of the demo: find the DR1 MER tile for each gallery target and download VIS + NISP cutouts.

For every target in targets.gallery_targets:
  1. TAP query on dr1.mosaic_product (footprint INTERSECTS a small circle around the target);
  2. choose the tile whose centre is closest to the target;
  3. request server-side cutouts of the background-subtracted mosaics in VIS, NIR_Y, NIR_J, NIR_H
     (plus the VIS FLAG map) and store them in ~/data/euclid/dr1_demo/cutouts/<target>/;
  4. write a metadata.json with tile index, zero points and file names.

Usage: uv run python demo/01_get_cutouts.py
"""

import json
import time

from dr1_access import default_data_root, find_auxiliary_files, find_mosaics, get_cutout, pick_tile
from targets import cutout_radius_arcmin, gallery_targets, mosaic_selection

bands = ("VIS", "NIR_Y", "NIR_J", "NIR_H")


def main() -> None:
    for target in gallery_targets:
        start = time.time()
        output_dir = default_data_root / "cutouts" / target.slug
        mosaics = find_mosaics(target.ra_deg, target.dec_deg, selection=mosaic_selection[target.name])
        if len(mosaics) == 0:
            print(f"{target.name}: no DR1 mosaic found")
            continue
        tile_index = pick_tile(mosaics, target.ra_deg, target.dec_deg)
        tile_mosaics = mosaics[mosaics["tile_index"] == tile_index]
        radius = cutout_radius_arcmin[target.name]
        metadata = {
            "name": target.name,
            "ra_deg": target.ra_deg,
            "dec_deg": target.dec_deg,
            "galaxy_type": target.galaxy_type,
            "source_paper": target.source_paper,
            "tile_index": tile_index,
            "radius_arcmin": radius,
            "bands": {},
        }
        for row in tile_mosaics:
            band = str(row["filter_name"])
            if band not in bands:
                continue
            path = get_cutout(
                str(row["file_path"]),
                str(row["file_name"]),
                target.ra_deg,
                target.dec_deg,
                radius,
                output_dir / f"{band}.fits",
            )
            metadata["bands"][band] = {
                "file": path.name,
                "zero_point": float(row["zero_point"]),
                "mosaic_file_name": str(row["file_name"]),
            }
            if band == "VIS":
                for auxiliary in find_auxiliary_files(int(row["mosaic_product_oid"])):
                    if str(auxiliary["stype"]) == "FLAG":
                        flag_path = get_cutout(
                            str(auxiliary["file_path"]),
                            str(auxiliary["file_name"]),
                            target.ra_deg,
                            target.dec_deg,
                            radius,
                            output_dir / "VIS_FLAG.fits",
                        )
                        metadata["bands"]["VIS"]["flag_file"] = flag_path.name
        (output_dir / "metadata.json").write_text(json.dumps(metadata, indent=2))
        print(
            f"{target.name}: tile {tile_index}, bands {sorted(metadata['bands'])}, {time.time() - start:.0f} s",
            flush=True,
        )


if __name__ == "__main__":
    main()
