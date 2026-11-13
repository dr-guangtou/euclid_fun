"""Stage 7: Euclid and Legacy Surveys cutouts, colour composites and contact sheets for visual inspection.

Objects: every tier A and tier B object of both fields, the known confirmed objects with Euclid coverage, and a
sample of control-field tier C objects (what contaminants look like). Each object gets three thumbnails of 12 arcsec:
VIS greyscale, Euclid colour (H, Y+J, VIS) and Legacy grz. A triage template is written for the visual notes;
notes never change tiers or ranks.

Usage: uv run python -m ucd.stages.stage_7_cutouts [--smoke]
Products: stage_7_cutouts/tables/cutout_index.csv, visual_triage_template.csv, figures/sheet_*.png, summary.json
"""

import argparse
from concurrent.futures import ThreadPoolExecutor

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from PIL import Image

from ucd.lib import cutouts, qa_plots, run_state

stage_name = "stage_7_cutouts"
objects_per_sheet = 24
workers = 4


def select_objects(tables: dict, smoke: bool) -> pd.DataFrame:
    fornax, control = tables["fornax"], tables["control"]
    known = (fornax["known_state"] == "confirmed") & fornax["cut_euclid_available"]
    groups = [
        ("fornax_known_confirmed", fornax[known]),
        ("fornax_tier_a_not_in_catalogue", fornax[(fornax["tier"] == "A") & fornax["known_object_id"].isna()]),
        (
            "fornax_tier_a_other_known",
            fornax[(fornax["tier"] == "A") & fornax["known_state"].isin(["rejected", "uncertain"])],
        ),
        ("fornax_tier_b", fornax[(fornax["tier"] == "B") & ~known]),
        ("control_tier_a", control[control["tier"] == "A"]),
        ("control_tier_b", control[control["tier"] == "B"]),
        ("control_tier_c_sample", control[control["tier"] == "C"].sort_values("euclid_ie_mag").iloc[::28]),
    ]
    frames = []
    for group, frame in groups:
        frame = frame.sort_values("euclid_ie_mag").copy()
        frame["group"] = group
        frames.append(frame.head(3) if smoke else frame)
    selected = pd.concat(frames, ignore_index=True)
    selected["label"] = [f"{row.group}_{index:03d}" for index, row in enumerate(selected.itertuples())]
    return selected


def fetch_object(config: dict, lookup: dict, row, folder) -> dict:
    tile = lookup.get(str(int(row.euclid_tile_index)), {})
    paths = cutouts.fetch_euclid(tile, row.ra, row.dec, folder / "euclid", row.label)
    legacy_path = folder / "legacy" / f"{row.label}.jpg"
    layer = cutouts.fetch_legacy_jpeg(config, row.ra, row.dec, legacy_path)
    return {
        "label": row.label,
        "euclid_bands": len(paths),
        "legacy_layer": layer,
        **{f"path_{band.lower()}": str(path) for band, path in paths.items()},
        "path_legacy": str(legacy_path) if layer else "",
    }


def draw_sheet(config: dict, lookup: dict, rows: pd.DataFrame, index: pd.DataFrame, title: str, path) -> None:
    columns = 2
    lines = int(np.ceil(len(rows) / columns))
    figure, axes = plt.subplots(lines, columns * 4, figsize=(qa_plots.double_width, 0.95 * lines + 0.35), squeeze=False,
                                gridspec_kw={"width_ratios": [1, 1, 1, 1.55] * columns})  # fmt: skip
    for axis in axes.ravel():
        axis.set_axis_off()
    paths = index.set_index("label")
    for position, row in enumerate(rows.itertuples()):
        line, block = divmod(position, columns)
        entry = paths.loc[row.label]
        tile = lookup.get(str(int(row.euclid_tile_index)), {})
        images = {}
        for band in cutouts.euclid_bands:
            band_path = entry.get(f"path_{band.lower()}", "")
            if isinstance(band_path, str) and band_path and band in tile:
                images[band] = cutouts.read_flux(band_path, tile[band]["zero_point"])
        panels = axes[line, block * 4 : block * 4 + 4]
        if "VIS" in images:
            panels[0].imshow(cutouts.vis_greyscale(images["VIS"]), cmap="gray_r", vmin=0, vmax=1, origin="lower")
        colour = cutouts.euclid_colour(images)
        if colour is not None:
            panels[1].imshow(colour, origin="lower")
        if isinstance(entry["path_legacy"], str) and entry["path_legacy"]:
            panels[2].imshow(np.asarray(Image.open(entry["path_legacy"])))
        known = {"confirmed": "known UCD", "rejected": "known, not UCD", "uncertain": "known, uncertain"}.get(
            row.known_state, "new"
        )
        text = (
            rf"\textbf{{{row.sheet_number}}} \quad tier {row.tier or '--'} \quad {known}" + "\n"
            rf"$I_{{\rm E}}={row.euclid_ie_mag:.2f}$, $G={row.phot_g_mean_mag:.2f}$" + "\n"
            rf"$\mu-{{\rm m}}={row.euclid_mumax_minus_mag:.2f}$, "
            rf"$r_{{\rm S}}={row.euclid_sersic_sersic_vis_radius:.2f}''$" + "\n"
            rf"$g-r={row.legacy_g_minus_r:.2f}$, $\epsilon={row.euclid_ellipticity:.2f}$, {row.legacy_type}"
        )
        panels[3].text(0.02, 0.5, text, fontsize=5.6, va="center", ha="left", transform=panels[3].transAxes)
    figure.suptitle(title + r" \quad (VIS, Euclid $H$/$YJ$/VIS, Legacy $grz$; 12 arcsec)", fontsize=8, y=0.995)
    figure.subplots_adjust(
        left=0.005, right=0.995, top=1 - 0.3 / (0.95 * lines + 0.35), bottom=0.005, wspace=0.04, hspace=0.06
    )
    figure.savefig(path, dpi=200)
    plt.close(figure)
    print(f"  sheet: {path}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    arguments = parser.parse_args()
    config = run_state.load_config()
    run_state.require_stages(config, ["stage_5_cutflow"])
    folder = run_state.stage_dir(config, stage_name, smoke=arguments.smoke)
    for child in ("euclid", "legacy"):
        (folder / "tables" / child).mkdir(exist_ok=True)
    stage_5 = run_state.run_dir(config) / "stage_5_cutflow" / "tables"
    tables = {name: pd.read_parquet(stage_5 / f"master_{name}.parquet") for name in ("fornax", "control")}
    for name, frame in tables.items():
        frame["field"] = name
    selected = select_objects(tables, arguments.smoke)
    selected["sheet_number"] = selected.groupby("group").cumcount() + 1

    representatives = selected.groupby("euclid_tile_index")[["ra", "dec"]].first()
    lookup = cutouts.mosaic_lookup(
        {int(tile): (row.ra, row.dec) for tile, row in representatives.iterrows()},
        run_state.stage_dir(config, stage_name) / "tables" / "mosaic_lookup.json",
    )
    print(f"{len(selected)} objects in {len(representatives)} tiles; downloading cutouts")
    with ThreadPoolExecutor(max_workers=workers) as pool:
        results = list(
            pool.map(lambda row: fetch_object(config, lookup, row, folder / "tables"), selected.itertuples())
        )
    index = pd.DataFrame(results)
    selected_columns = ["label", "group", "sheet_number", "field", "source_id", "ra", "dec", "tier", "known_state",
                        "phot_g_mean_mag", "euclid_ie_mag", "euclid_mumax_minus_mag", "euclid_sersic_sersic_vis_radius",
                        "euclid_ellipticity", "legacy_g_minus_r", "legacy_r_minus_z", "legacy_type",
                        "tier_a_below_galaxy_sequence", "displacement_significance"]  # fmt: skip
    index = selected[selected_columns].merge(index, on="label")
    index.to_csv(folder / "tables" / "cutout_index.csv", index=False)
    template = index[["label", "group", "sheet_number", "field", "source_id", "tier"]].copy()
    template["visual_flag"] = ""
    template["visual_note"] = ""
    template_path = folder / "tables" / "visual_triage_template.csv"
    template.to_csv(template_path, index=False)

    titles = {
        "fornax_known_confirmed": "Fornax: known confirmed UCDs with Euclid entry",
        "fornax_tier_a_not_in_catalogue": "Fornax: tier A, not in the literature catalogue",
        "fornax_tier_a_other_known": "Fornax: tier A, known compact objects that are not UCDs",
        "fornax_tier_b": "Fornax: tier B (large)",
        "control_tier_a": "Control field: tier A",
        "control_tier_b": "Control field: tier B (large)",
        "control_tier_c_sample": "Control field: tier C sample (contaminants)",
    }
    sheets = 0
    for group, rows in selected.groupby("group", sort=False):
        for page, start in enumerate(range(0, len(rows), objects_per_sheet), start=1):
            part = rows.iloc[start : start + objects_per_sheet]
            pages = int(np.ceil(len(rows) / objects_per_sheet))
            draw_sheet(config, lookup, part, index, rf"{titles[group]} ({page}/{pages})",
                       folder / "figures" / f"sheet_{group}_{page}.png")  # fmt: skip
            sheets += 1

    complete = (index["euclid_bands"] == 4) & index["path_legacy"].astype(bool)
    metrics = {
        "objects": len(index),
        "by_group": index["group"].value_counts().to_dict(),
        "with_four_euclid_bands": int((index["euclid_bands"] == 4).sum()),
        "with_legacy_image": int(index["path_legacy"].astype(bool).sum()),
        "legacy_layers_used": index["legacy_layer"].fillna("none").value_counts().to_dict(),
        "complete_fraction": float(complete.mean()),
        "contact_sheets": sheets,
        "tiles": len(representatives),
    }
    gates = [
        run_state.gate(
            "cutouts_complete",
            "Euclid (4 bands) and Legacy images for at least 95% of the objects",
            round(metrics["complete_fraction"], 3),
            metrics["complete_fraction"] >= 0.95,
        ),
        run_state.gate(
            "triage_template_written", "visual triage template written", str(template_path), template_path.exists()
        ),
    ]
    run_state.write_summary(config, stage_name, metrics, gates, smoke=arguments.smoke)


if __name__ == "__main__":
    main()
