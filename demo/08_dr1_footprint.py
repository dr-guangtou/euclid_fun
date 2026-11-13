"""Step 8 of the demo: a DR1 footprint as MOC files, built from the archive's MER tile polygons.

DR1-Foundation has no single survey-wide footprint file. The official LE3 VMPZ-ID HEALPix maps (Nside 16384) come
per MER tile and per band. For quick "is my target in DR1?" checks, and for cross-matching, a MOC built from the
tile polygons (`dr1.mosaic_product.stc_s`, VIS mosaics) is enough. Each polygon is the full 32' (wide) or 17' (deep)
tile including its overlap margin, so near survey edges the MOC is slightly larger than the data.

Outputs:
  ~/data/euclid/dr1_demo/footprint/dr1_{wide,deep}_vis_tiles_moc_order13.fits   (MOC, order 13 = 25.8")
  figures/dr1_footprint.png, figures/dr1_footprint.json (tile counts and MOC areas)

Usage: uv run python demo/08_dr1_footprint.py
"""

import json
import sys
from pathlib import Path

import astropy.units as u
import matplotlib
import matplotlib.lines
import matplotlib.patches
import matplotlib.pyplot as plt
import numpy as np
from astropy.coordinates import SkyCoord
from dr1_access import default_data_root, run_query, selection_clause, wide_survey_selection
from mocpy import MOC

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from plot_style import figure_width_double, use_publication_style  # noqa: E402

figure_dir = Path(__file__).resolve().parents[1] / "figures"
footprint_dir = default_data_root / "footprint"
moc_order = 13
full_sky_deg2 = 4.0 * np.pi * (180.0 / np.pi) ** 2
# deep stacks exist in both DR1_R1 (1117 tiles) and DR1_R2 (251 tiles): do not restrict the release here
selections = {"wide": wide_survey_selection, "deep": {"purpose": "DATA_RELEASE_DEEP", "processing_mode": "DEEP"}}


def tile_polygons(selection: dict[str, str]) -> dict[int, np.ndarray]:
    """One (lon, lat) vertex array per tile; duplicate mosaics of a tile share the polygon."""
    # TAP returns HTTP 500 for DISTINCT on the array column `fov`; the string column `stc_s` works
    table = run_query(
        f"SELECT tile_index, stc_s FROM dr1.mosaic_product WHERE filter_name = 'VIS' AND {selection_clause(selection)}"
    )
    polygons = {}
    for tile_index, region in zip(table["tile_index"], table["stc_s"], strict=True):
        vertices = np.array(region.split()[2:], dtype=float).reshape(-1, 2)  # "Polygon J2000 lon lat lon lat ..."
        polygons.setdefault(int(tile_index), vertices)
    return polygons


def build_moc(survey: str) -> tuple[MOC, int]:
    path = footprint_dir / f"dr1_{survey}_vis_tiles_moc_order{moc_order}.fits"
    count_path = path.with_suffix(".count")
    if path.exists() and count_path.exists():
        return MOC.from_fits(path), int(count_path.read_text())
    polygons = tile_polygons(selections[survey])
    skycoords = [SkyCoord(vertices[:, 0] * u.deg, vertices[:, 1] * u.deg) for vertices in polygons.values()]
    tile_mocs = MOC.from_polygons(skycoords, max_depth=moc_order)
    moc = tile_mocs[0].union(*tile_mocs[1:])
    footprint_dir.mkdir(parents=True, exist_ok=True)
    moc.save(path, format="fits", overwrite=True)
    count_path.write_text(str(len(polygons)))
    return moc, len(polygons)


def mollweide_x(right_ascension_deg: np.ndarray) -> np.ndarray:
    """Matplotlib Mollweide abscissa (radians) with right ascension increasing to the left."""
    return -np.deg2rad(((np.asarray(right_ascension_deg) + 180.0) % 360.0) - 180.0)


def break_wraps(x: np.ndarray, y: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    jumps = np.where(np.abs(np.diff(x)) > np.pi)[0] + 1
    return np.insert(x, jumps, np.nan), np.insert(y, jumps, np.nan)


def plot(mocs: dict[str, MOC], output: Path) -> None:
    use_publication_style()
    figure = plt.figure(figsize=(figure_width_double, 3.9))
    axis = figure.add_subplot(1, 1, 1, projection="mollweide")
    step_deg = 0.2
    longitude = np.arange(-180.0 + step_deg / 2, 180.0, step_deg)
    latitude = np.arange(-90.0 + step_deg / 2, 90.0, step_deg)
    grid_longitude, grid_latitude = np.meshgrid(longitude, latitude)
    right_ascension = (-grid_longitude) % 360.0  # x = -RA so that RA increases to the left
    colours = {"wide": "#1f77b4", "deep": "#d62728"}
    for survey in ("wide", "deep"):
        inside = mocs[survey].contains_lonlat(right_ascension.ravel() * u.deg, grid_latitude.ravel() * u.deg)
        image = np.where(inside.reshape(grid_longitude.shape), 1.0, np.nan)
        axis.pcolormesh(
            np.deg2rad(grid_longitude),
            np.deg2rad(grid_latitude),
            image,
            cmap=matplotlib.colors.ListedColormap([colours[survey]]),
            shading="auto",
            rasterized=True,
        )
    sample = np.linspace(0.0, 360.0, 1441)
    for latitude_galactic, style in [(0.0, "-"), (-20.0, ":"), (20.0, ":")]:
        plane = SkyCoord(l=sample * u.deg, b=np.full(sample.size, latitude_galactic) * u.deg, frame="galactic").icrs
        axis.plot(*break_wraps(mollweide_x(plane.ra.deg), plane.dec.radian), style, color="0.45", lw=0.6)
    ecliptic = SkyCoord(lon=sample * u.deg, lat=np.zeros(sample.size) * u.deg, frame="barycentrictrueecliptic").icrs
    axis.plot(*break_wraps(mollweide_x(ecliptic.ra.deg), ecliptic.dec.radian), "--", color="#2ca02c", lw=0.6)
    tick_positions = np.arange(-150, 151, 30)
    axis.set_xticks(np.deg2rad(tick_positions))
    axis.set_xticklabels([rf"${(-position) % 360:d}^\circ$" for position in tick_positions], fontsize=6.5)
    axis.set_yticks(np.deg2rad(np.arange(-60, 61, 30)))
    axis.set_yticklabels([rf"${value:+d}^\circ$" for value in range(-60, 61, 30)], fontsize=7)
    axis.grid(True, color="0.85", lw=0.4)
    axis.set_xlabel("right ascension")
    axis.set_ylabel("declination")
    handles = [
        matplotlib.patches.Patch(color=colours["wide"], label="wide-survey tiles"),
        matplotlib.patches.Patch(color=colours["deep"], label="deep-field stacks"),
        matplotlib.lines.Line2D([], [], color="0.45", lw=0.6, label=r"Galactic plane ($b = 0^\circ$)"),
        matplotlib.lines.Line2D([], [], color="0.45", lw=0.6, ls=":", label=r"$|b| = 20^\circ$"),
        matplotlib.lines.Line2D([], [], color="#2ca02c", lw=0.6, ls="--", label="ecliptic"),
    ]
    axis.legend(handles=handles, loc="lower center", bbox_to_anchor=(0.5, -0.13), ncol=5, fontsize=6.5)
    output.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output)
    plt.close(figure)


def main() -> None:
    summary = {}
    mocs = {}
    for survey in selections:
        moc, tile_count = build_moc(survey)
        mocs[survey] = moc
        summary[survey] = {"tiles": tile_count, "moc_order": moc_order, "area_deg2": moc.sky_fraction * full_sky_deg2}
        print(f"{survey}: {tile_count} tiles, MOC area {summary[survey]['area_deg2']:.1f} deg2")
    union = mocs["wide"].union(mocs["deep"])
    summary["wide_or_deep_area_deg2"] = union.sky_fraction * full_sky_deg2
    print(f"wide or deep: {summary['wide_or_deep_area_deg2']:.1f} deg2")
    output = figure_dir / "dr1_footprint.png"
    plot(mocs, output)
    output.with_suffix(".json").write_text(json.dumps(summary, indent=2))
    print("wrote", output)


if __name__ == "__main__":
    main()
