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
