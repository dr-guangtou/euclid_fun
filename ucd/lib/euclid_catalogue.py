"""Euclid DR1 archive access for the UCD pipeline; reuses the tested helpers in demo/dr1_access.py."""

import sys

from ucd.lib.run_state import repository_root

sys.path.insert(0, str(repository_root / "demo"))
import dr1_access  # noqa: E402

run_query = dr1_access.run_query
find_mosaics = dr1_access.find_mosaics
get_cutout = dr1_access.get_cutout


def cone_clause(ra_deg: float, dec_deg: float, radius_deg: float, alias: str = "") -> str:
    prefix = f"{alias}." if alias else ""
    return (
        f"1 = CONTAINS(POINT({prefix}right_ascension, {prefix}declination), "
        f"CIRCLE({ra_deg:.8f}, {dec_deg:.8f}, {radius_deg:.8f}))"
    )


def count_cone(config: dict, ra_deg: float, dec_deg: float, radius_deg: float) -> int:
    table = config["euclid"]["catalogue"]
    result = run_query(f"SELECT COUNT(*) AS n FROM {table} WHERE {cone_clause(ra_deg, dec_deg, radius_deg)}")
    return int(result["n"][0])


catalogue_columns = [
    "object_id", "right_ascension", "declination", "tile_index", "vis_det",
    "flux_detection_total", "fluxerr_detection_total", "flux_segmentation", "flux_vis_psf", "fluxerr_vis_psf",
    "flux_vis_sersic", "fluxerr_vis_sersic",
    "flux_vis_1fwhm_aper", "flux_vis_2fwhm_aper", "fluxerr_vis_2fwhm_aper",
    "flux_y_2fwhm_aper", "fluxerr_y_2fwhm_aper", "flux_j_2fwhm_aper", "fluxerr_j_2fwhm_aper",
    "flux_h_2fwhm_aper", "fluxerr_h_2fwhm_aper",
    "flux_y_templfit", "flux_j_templfit", "flux_h_templfit",
    "flux_g_ext_decam_2fwhm_aper", "fluxerr_g_ext_decam_2fwhm_aper",
    "flux_r_ext_decam_2fwhm_aper", "fluxerr_r_ext_decam_2fwhm_aper",
    "flux_i_ext_decam_2fwhm_aper", "fluxerr_i_ext_decam_2fwhm_aper",
    "flux_z_ext_decam_2fwhm_aper", "fluxerr_z_ext_decam_2fwhm_aper",
    "fwhm", "semimajor_axis", "ellipticity", "position_angle", "kron_radius", "segmentation_area",
    "mu_max", "mumax_minus_mag", "point_like_prob", "spurious_prob", "spurious_flag", "det_quality_flag",
    "deblended_flag", "parent_id", "parent_visnir", "flag_vis", "flag_y", "flag_j", "flag_h",
    "gaia_id", "gaia_match_quality", "gal_ebv",
]  # fmt: skip
morphology_columns = [
    "sersic_sersic_vis_radius", "sersic_sersic_vis_index", "sersic_sersic_vis_axis_ratio", "sersic_angle",
    "sersic_visnir_reduced_chi2", "sersic_visnir_flags", "flux_radius", "concentration", "gini",
]  # fmt: skip
classification_columns = ["phz_star_prob", "phz_gal_prob", "phz_qso_prob", "phz_glob_cl_prob", "phz_classification"]
photo_z_columns = ["phz_median", "phz_flags"]
integer_columns = ["object_id", "tile_index", "parent_id", "gaia_id"]


def table_to_frame(table):
    """astropy Table to pandas without losing 64-bit identifiers (masked integers become -1)."""
    import numpy as np

    exact = {}
    for name in integer_columns:
        if name in table.colnames:
            column = table[name]
            values = np.ma.filled(column, -1) if hasattr(column, "mask") else np.asarray(column)
            exact[name] = np.asarray(values).astype(np.int64)
    frame = table.to_pandas()
    for name, values in exact.items():
        frame[name] = values
    return frame


def download_cone(config: dict, ra_deg: float, dec_deg: float, radius_deg: float, cache_dir, *, strips: int):
    """MER catalogue entries brighter than the configured flux limit in a cone, cached in declination strips.

    Only the catalogue table is queried by position: joining the morphology and PHZ tables inside a cone query
    took more than 6 min for a 5 arcmin cone (2026-11-14), so those rows are fetched by object_id afterwards.
    """
    import numpy as np
    import pandas as pd

    settings = config["euclid"]
    cache_dir.mkdir(parents=True, exist_ok=True)
    edges = np.linspace(dec_deg - radius_deg, dec_deg + radius_deg + 1e-6, strips + 1)
    frames = []
    for index in range(strips):
        path = cache_dir / f"strip_{index:02d}_of_{strips:02d}.parquet"
        if not path.exists():
            query = (
                f"SELECT {', '.join(catalogue_columns)} FROM {settings['catalogue']} "
                f"WHERE {cone_clause(ra_deg, dec_deg, radius_deg)} "
                f"AND flux_detection_total > {settings['minimum_flux_ujy']} "
                f"AND declination >= {edges[index]:.8f} AND declination < {edges[index + 1]:.8f}"
            )
            frame = table_to_frame(run_query(query))
            frame.to_parquet(path, index=False)
            print(f"    strip {index + 1}/{strips}: {len(frame)} rows", flush=True)
        frames.append(pd.read_parquet(path))
    result = pd.concat(frames, ignore_index=True)
    if result["object_id"].duplicated().any():
        raise RuntimeError("duplicate object_id in the MER cone")
    return result


def fetch_by_object_id(table_name: str, columns: list[str], object_ids, cache_path, *, batch_size: int = 1000):
    """Rows of a DR1 table for a list of object_id values (batched IN lists), cached as one Parquet file."""
    import pandas as pd

    if cache_path.exists():
        return pd.read_parquet(cache_path)
    object_ids = sorted({int(value) for value in object_ids})
    frames = []
    for start in range(0, len(object_ids), batch_size):
        batch = object_ids[start : start + batch_size]
        query = (
            f"SELECT object_id, {', '.join(columns)} FROM {table_name} "
            f"WHERE object_id IN ({', '.join(str(value) for value in batch)})"
        )
        frames.append(table_to_frame(run_query(query)))
        print(f"    {table_name}: {min(start + batch_size, len(object_ids))}/{len(object_ids)}", flush=True)
    result = pd.concat(frames, ignore_index=True) if frames else pd.DataFrame(columns=["object_id", *columns])
    result = result.drop_duplicates("object_id")
    result.to_parquet(cache_path, index=False)
    return result
