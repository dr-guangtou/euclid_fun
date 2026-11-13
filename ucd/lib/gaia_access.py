"""Gaia DR3 access through a TAP service: counts and full cone retrieval with an exact row-count check.

The primary service is the NOIRLab Data Lab copy (Q3C cone syntax, synchronous queries, declination strips of at
most a few thousand rows, as established in bubbletea). The ESA archive syntax is supported as a fallback.
"""

import time

import numpy as np
import pandas as pd
import pyvo

from ucd.lib import selector

quality_columns = [
    "ref_epoch",
    "astrometric_params_solved",
    "visibility_periods_used",
    "duplicated_source",
    "phot_g_mean_flux_over_error",
    "phot_bp_mean_flux_over_error",
    "phot_rp_mean_flux_over_error",
    "ra_error",
    "dec_error",
    "ipd_gof_harmonic_amplitude",
    "in_qso_candidates",
    "in_galaxy_candidates",
    "non_single_star",
    "classprob_dsc_combmod_star",
    "classprob_dsc_combmod_galaxy",
    "classprob_dsc_combmod_quasar",
    "l",
    "b",
]
retrieval_columns = selector.raw_gaia_columns + quality_columns
integer_columns = [
    "astrometric_params_solved",
    "visibility_periods_used",
    "duplicated_source",
    "in_qso_candidates",
    "in_galaxy_candidates",
    "non_single_star",
]


def run_query(settings: dict, adql: str, *, maximum_rows: int = 100000, attempts: int = 4) -> pd.DataFrame:
    """Synchronous TAP query with retries. `source_id` is kept as an exact 64-bit integer."""
    service = pyvo.dal.TAPService(settings["tap_url"])
    for attempt in range(1, attempts + 1):
        try:
            table = service.run_sync(adql, maxrec=maximum_rows).to_table()
            break
        except Exception as error:
            if attempt == attempts:
                raise
            print(f"  Gaia query failed ({type(error).__name__}); retry {attempt}/{attempts - 1}")
            time.sleep(15 * attempt)
    source_ids = np.array(table["source_id"]).astype(np.int64) if "source_id" in table.colnames else None
    frame = table.to_pandas()
    if source_ids is not None:
        frame["source_id"] = source_ids
    return frame


def cone_clause(settings: dict, ra_deg: float, dec_deg: float, radius_deg: float) -> str:
    if settings["cone_syntax"] == "q3c":
        return f"'t' = Q3C_RADIAL_QUERY(ra, dec, {ra_deg:.8f}, {dec_deg:.8f}, {radius_deg:.8f})"
    return f"1 = CONTAINS(POINT(ra, dec), CIRCLE({ra_deg:.8f}, {dec_deg:.8f}, {radius_deg:.8f}))"


def count_cone(config: dict, ra_deg: float, dec_deg: float, radius_deg: float, extra: str = "") -> int:
    settings = config["gaia"]
    frame = run_query(
        settings,
        f"SELECT COUNT(*) AS source_count FROM {settings['table']} "
        f"WHERE {cone_clause(settings, ra_deg, dec_deg, radius_deg)}{extra}",
    )
    return int(frame["source_count"].iloc[0])


def retrieve_cone(config: dict, ra_deg: float, dec_deg: float, radius_deg: float) -> pd.DataFrame:
    """Every Gaia source in the cone, fetched in declination strips; raises if any count disagrees."""
    settings = config["gaia"]
    cone = cone_clause(settings, ra_deg, dec_deg, radius_deg)
    limit = settings["maximum_rows_per_query"]
    total = count_cone(config, ra_deg, dec_deg, radius_deg)
    strips = []

    def plan(dec_low: float, dec_high: float, last: bool) -> None:
        upper = "<=" if last else "<"
        clause = f" AND dec >= {dec_low:.8f} AND dec {upper} {dec_high:.8f}"
        count = count_cone(config, ra_deg, dec_deg, radius_deg, clause)
        if count > limit and dec_high - dec_low > 1e-4:
            middle = 0.5 * (dec_low + dec_high)
            plan(dec_low, middle, False)
            plan(middle, dec_high, last)
        elif count > 0:
            strips.append((clause, count))

    plan(dec_deg - radius_deg, dec_deg + radius_deg, True)
    frames = []
    for clause, count in strips:
        frame = run_query(
            settings,
            f"SELECT {', '.join(retrieval_columns)} FROM {settings['table']} WHERE {cone}{clause}",
            maximum_rows=count + 1,
        )
        if len(frame) != count:
            raise RuntimeError(f"strip returned {len(frame)} rows, expected {count}")
        frames.append(frame)
    result = pd.concat(frames, ignore_index=True)
    if len(result) != total:
        raise RuntimeError(f"Gaia retrieval returned {len(result)} rows, count query said {total}")
    if result["source_id"].duplicated().any():
        raise RuntimeError("duplicate Gaia source_id in retrieval")
    for column in integer_columns:
        result[column] = result[column].astype("Int64")
    return result
