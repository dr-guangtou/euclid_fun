"""Positional cross-matching anchored on the Gaia source, with ambiguity bookkeeping and a false-match control."""

import astropy.units as u
import numpy as np
import pandas as pd
from astropy.coordinates import SkyCoord, search_around_sky


def nearest_match(anchor: SkyCoord, catalogue: SkyCoord, radius_arcsec: float) -> pd.DataFrame:
    """For every anchor position: nearest catalogue entry, its separation, and how many entries lie in the radius.

    Returned columns: catalogue_index (-1 if none in radius), separation_arcsec, offset_east_arcsec,
    offset_north_arcsec (catalogue minus anchor), matches_in_radius, second_separation_arcsec.
    """
    result = pd.DataFrame(
        {
            "catalogue_index": np.full(len(anchor), -1, dtype=np.int64),
            "separation_arcsec": np.full(len(anchor), np.nan),
            "offset_east_arcsec": np.full(len(anchor), np.nan),
            "offset_north_arcsec": np.full(len(anchor), np.nan),
            "matches_in_radius": np.zeros(len(anchor), dtype=np.int64),
            "second_separation_arcsec": np.full(len(anchor), np.nan),
        }
    )
    if len(catalogue) == 0 or len(anchor) == 0:
        return result
    anchor_index, catalogue_index, separation, _ = search_around_sky(anchor, catalogue, radius_arcsec * u.arcsec)
    if len(anchor_index) == 0:
        return result
    pairs = pd.DataFrame(
        {"anchor": anchor_index, "catalogue": catalogue_index, "separation": separation.arcsec}
    ).sort_values(["anchor", "separation"])
    pairs["rank"] = pairs.groupby("anchor").cumcount()
    first = pairs[pairs["rank"] == 0].set_index("anchor")
    second = pairs[pairs["rank"] == 1].set_index("anchor")
    counts = pairs.groupby("anchor").size()
    rows = first.index.to_numpy()
    result.loc[rows, "catalogue_index"] = first["catalogue"].to_numpy()
    result.loc[rows, "separation_arcsec"] = first["separation"].to_numpy()
    result.loc[counts.index.to_numpy(), "matches_in_radius"] = counts.to_numpy()
    result.loc[second.index.to_numpy(), "second_separation_arcsec"] = second["separation"].to_numpy()
    east, north = anchor[rows].spherical_offsets_to(catalogue[first["catalogue"].to_numpy()])
    result.loc[rows, "offset_east_arcsec"] = east.arcsec
    result.loc[rows, "offset_north_arcsec"] = north.arcsec
    return result


def displaced_match_fraction(
    anchor: SkyCoord, catalogue: SkyCoord, radius_arcsec: float, displacement_arcsec: float = 20.0
) -> float:
    """Fraction of anchors that still find an entry within the radius after being moved away (false-match rate)."""
    fractions = []
    for position_angle in (45, 135, 225, 315):
        moved = anchor.directional_offset_by(position_angle * u.deg, displacement_arcsec * u.arcsec)
        matched = nearest_match(moved, catalogue, radius_arcsec)
        fractions.append((matched["catalogue_index"] >= 0).mean())
    return float(np.mean(fractions))
