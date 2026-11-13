"""Legacy Surveys DR11 South access through the LSDB (HATS) server at SLAC, and image cutouts from the viewer."""

import pandas as pd

wanted_columns = [
    "RELEASE", "BRICKID", "BRICKNAME", "OBJID", "RA", "DEC", "TYPE", "SERSIC", "SHAPE_R", "SHAPE_R_IVAR",
    "SHAPE_E1", "SHAPE_E2", "FLUX_G", "FLUX_R", "FLUX_I", "FLUX_Z", "FLUX_W1", "FLUX_W2",
    "FLUX_IVAR_G", "FLUX_IVAR_R", "FLUX_IVAR_I", "FLUX_IVAR_Z", "FLUX_IVAR_W1", "FLUX_IVAR_W2",
    "MW_TRANSMISSION_G", "MW_TRANSMISSION_R", "MW_TRANSMISSION_I", "MW_TRANSMISSION_Z",
    "FRACFLUX_G", "FRACFLUX_R", "FRACFLUX_Z", "FRACMASKED_R", "FRACIN_R", "RCHISQ_G", "RCHISQ_R", "RCHISQ_Z",
    "PSFSIZE_G", "PSFSIZE_R", "PSFSIZE_Z", "NOBS_G", "NOBS_R", "NOBS_Z", "MASKBITS", "FITBITS",
    "REF_CAT", "REF_ID", "MJD_MIN", "MJD_MAX", "PSFDEPTH_G", "PSFDEPTH_R", "PSFDEPTH_Z",
]  # fmt: skip


def download_cone(config: dict, ra_deg: float, dec_deg: float, radius_deg: float, cache_path) -> pd.DataFrame:
    """All DR11 South Tractor entries in a cone (lower-case column names), cached as Parquet."""
    if cache_path.exists():
        return pd.read_parquet(cache_path)
    import lsdb

    url = config["legacy"]["lsdb_url"]
    available = {name.upper(): name for name in lsdb.open_catalog(url).all_columns}
    columns = [available[name] for name in wanted_columns if name in available]
    missing = [name for name in wanted_columns if name not in available]
    if missing:
        print(f"    Legacy columns not available: {missing}")
    catalogue = lsdb.open_catalog(url, columns=columns)
    frame = catalogue.cone_search(ra=ra_deg, dec=dec_deg, radius_arcsec=radius_deg * 3600.0).compute()
    frame = pd.DataFrame(frame).reset_index(drop=True)
    frame.columns = [name.lower() for name in frame.columns]
    for name in frame.columns:
        if str(frame[name].dtype).startswith(("string", "large_string")) or frame[name].dtype == object:
            frame[name] = frame[name].astype(str).str.strip()
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    frame.to_parquet(cache_path, index=False)
    return frame
