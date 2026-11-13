"""Step 6 of the demo: the IRSA / LSDB HATS route to Euclid DR1 catalogues, checked against the ESA TAP.

Checks (all timed, nothing needs credentials; anonymous S3 / HTTPS and anonymous ESA TAP):
 1. open the IRSA MER wide-survey HATS collection with ``lsdb.open_catalog`` and run a 5 arcmin cone
    around NGC 1483 (cold and warm), over S3 and over plain HTTPS;
 2. run the same cone on the ESA TAP and compare rows, object_id overlap, column names and values;
 3. cross-match the cone with Gaia DR3, Legacy Surveys DR10.1 and DR11.0 (South) at 1 arcsec, and join MER with
    the Euclid morphology and PHZ physical-parameter HATS catalogues on object_id;
 4. a larger query (30 arcmin cone, 5 columns): rows/s on HATS and on TAP;
 5. footprint: what the HATS metadata give (partition_info, skymap.fits, healpix9_to_partition.txt), a
    DR1 MOC built from it and its sky area compared with the ~1900 deg^2 of DR1 Foundation.

Usage: uv run python demo/06_hats_crossmatch.py [--skip-large] [--skip-tap]
Large results are written below ~/data/euclid/hats_cache/ (a few tens of MB).
"""

from __future__ import annotations

import argparse
import time
from contextlib import contextmanager
from pathlib import Path

import astropy.units as u
import lsdb
import numpy as np
import pandas as pd
import psutil
import requests
from astropy.coordinates import SkyCoord
from astropy.io import fits
from dr1_access import run_query
from mocpy import MOC
from targets import gallery_targets

irsa_bucket = "nasa-irsa-euclid-dr1"
irsa_prefix = "contributed/dr1/hats/reformatted_catalogs"
irsa_s3_root = f"s3://{irsa_bucket}/{irsa_prefix}"
irsa_https_root = f"https://{irsa_bucket}.s3.us-east-1.amazonaws.com/{irsa_prefix}"
lsdb_root = "https://data.lsdb.io/hats"

mer_wide_collection = "mer_catalogue_wide_survey"
mer_wide_catalog_name = "euclid_dr1_reformatted_catalogs_mer_catalogue_wide_survey-hats"

# hats 0.11.2 cannot open the Legacy Surveys collection root: open the catalogue and its margin separately.
legacy_catalog_url = f"{lsdb_root}/legacysurvey_dr10.1/legacysurvey"
legacy_margin_url = f"{lsdb_root}/legacysurvey_dr10.1/legacysurvey_10arcs"
gaia_collection_url = f"{lsdb_root}/gaia_dr3/"
# DR11 is not under data.lsdb.io/hats/: the portal (data.lsdb.io/data/DESI/) points to a SLAC server (plain HTTP).
# North: .../legacysurvey_dr11.0_north (Dec >= 32.375 deg, BASS/MzLS); South: DECam.
legacy_dr11_south_url = "http://slac.data.lsdb.io:10942/lsdb/legacysurvey_dr11.0_south"

cone_radius_arcmin = 5.0
crossmatch_radius_arcsec = 1.0
full_sky_area_deg2 = 41252.96
cache_dir = Path.home() / "data" / "euclid" / "hats_cache"

mer_columns = ["object_id", "ra", "dec", "tileid", "flux_vis_sersic", "flux_detection_total", "spurious_prob"]
tap_columns = (
    "object_id, right_ascension, declination, tile_index, flux_vis_sersic, flux_detection_total, "
    "spurious_prob, data_set_release_part3"
)
tap_to_hats_name = {"right_ascension": "ra", "declination": "dec", "tile_index": "tileid"}
compared_value_columns = ["flux_vis_sersic", "flux_detection_total", "spurious_prob"]


@contextmanager
def timer(label: str):
    start = time.perf_counter()
    holder = {}
    yield holder
    holder["seconds"] = time.perf_counter() - start
    print(f"  [time] {label}: {holder['seconds']:.2f} s", flush=True)


def tap_cone_query(ra_deg: float, dec_deg: float, radius_deg: float, columns: str) -> str:
    return (
        f"SELECT {columns} FROM dr1.mer_catalogue_wide_survey "
        f"WHERE CONTAINS(POINT('ICRS', right_ascension, declination), CIRCLE('ICRS', {ra_deg}, {dec_deg}, "
        f"{radius_deg})) = 1"
    )


def tap_table_to_frame(table) -> pd.DataFrame:
    frame = table.to_pandas()
    return frame.rename(columns=tap_to_hats_name)


def hats_frame_to_numpy(frame: pd.DataFrame) -> pd.DataFrame:
    """LSDB returns pyarrow-backed dtypes with <NA>; convert to NumPy dtypes with NaN for float columns."""
    plain = pd.DataFrame(index=frame.index)
    for name in frame.columns:
        series = frame[name]
        plain[name] = (
            series.astype("float64") if series.dtype.kind == "f" or "float" in str(series.dtype) else series.to_numpy()
        )
    return plain


def section_1_cone_search(target_ra: float, target_dec: float) -> pd.DataFrame:
    print("\n== 1. HATS cone search (MER wide survey) ==", flush=True)
    with timer("open_catalog over s3") as open_timer:
        catalog = lsdb.open_catalog(f"{irsa_s3_root}/{mer_wide_collection}", columns=mer_columns)
    info = catalog.hc_structure.catalog_info
    pixels = catalog.get_healpix_pixels()
    print(
        f"  total_rows={info.total_rows:,}, partitions={len(pixels)}, "
        f"margin_cache={'yes' if catalog.margin is not None else 'no'}, "
        f"ra/dec columns used by LSDB: {info.ra_column}/{info.dec_column}"
    )
    cone = catalog.cone_search(ra=target_ra, dec=target_dec, radius_arcsec=cone_radius_arcmin * 60.0)
    touched = cone.get_healpix_pixels()
    print(f"  cone touches {len(touched)} partitions: {[f'order {p.order} pixel {p.pixel}' for p in touched]}")
    with timer("cone compute, first call (cold)") as cold:
        frame = cone.compute()
    with timer("cone compute, same query again (warm)") as warm:
        frame_again = cone.compute()
    print(
        f"  rows={len(frame)} (repeat: {len(frame_again)}); cold/warm = {cold['seconds']:.1f}/{warm['seconds']:.1f} s"
    )
    print(f"  (open_catalog {open_timer['seconds']:.1f} s; LSDB keeps no data cache, so warm is not faster)")

    https_catalog = lsdb.open_catalog(f"{irsa_https_root}/{mer_wide_collection}", columns=mer_columns)
    print(f"  open_catalog over https works: {len(https_catalog.get_healpix_pixels())} partitions")
    try:
        https_catalog.cone_search(ra=target_ra, dec=target_dec, radius_arcsec=cone_radius_arcmin * 60.0).compute()
        print("  cone compute over https: works")
    except Exception as error:
        print(
            f"  cone compute over https FAILS: {type(error).__name__} (partitions are directories; HTTP "
            f"cannot list them)"
        )
    return frame


def section_2_compare_with_tap(hats_frame: pd.DataFrame, target_ra: float, target_dec: float) -> None:
    print("\n== 2. Same cone on the ESA TAP ==", flush=True)
    with timer("TAP async cone query"):
        tap_table = run_query(tap_cone_query(target_ra, target_dec, cone_radius_arcmin / 60.0, tap_columns))
    tap_frame = tap_table_to_frame(tap_table)
    hats_plain = hats_frame_to_numpy(hats_frame)
    print(f"  rows: HATS={len(hats_plain)}, TAP={len(tap_frame)}")
    print(
        f"  data_set_release_part3 values in the TAP cone: {sorted(set(tap_frame['data_set_release_part3'].tolist()))}"
    )
    print(
        f"  duplicated object_id rows: HATS={hats_plain['object_id'].duplicated().sum()}, "
        f"TAP={tap_frame['object_id'].duplicated().sum()}"
    )
    hats_ids, tap_ids = set(hats_plain["object_id"]), set(tap_frame["object_id"])
    print(
        f"  object_id overlap: both={len(hats_ids & tap_ids)}, only HATS={len(hats_ids - tap_ids)}, only "
        f"TAP={len(tap_ids - hats_ids)}"
    )
    centre = SkyCoord(target_ra * u.deg, target_dec * u.deg)
    for label, frame, ra_name, dec_name, only_ids in (
        ("only-HATS rows", hats_plain, "ra_from_object_id", "dec_from_object_id", hats_ids - tap_ids),
        ("only-TAP rows", tap_frame, "ra", "dec", tap_ids - hats_ids),
    ):
        subset = frame[frame["object_id"].isin(only_ids)]
        if len(subset):
            separation = centre.separation(
                SkyCoord(subset[ra_name].to_numpy() * u.deg, subset[dec_name].to_numpy() * u.deg)
            ).arcmin
            print(
                f"  {label}: separation from centre {separation.min():.4f}..{separation.max():.4f} arcmin "
                f"(cone radius {cone_radius_arcmin})"
            )

    offset = (
        SkyCoord(hats_plain["ra"].to_numpy() * u.deg, hats_plain["dec"].to_numpy() * u.deg)
        .separation(
            SkyCoord(
                hats_plain["ra_from_object_id"].to_numpy() * u.deg, hats_plain["dec_from_object_id"].to_numpy() * u.deg
            )
        )
        .arcsec
    )
    print(
        f"  HATS ra/dec (barycentre) vs ra_from_object_id/dec_from_object_id: "
        f"median {np.median(offset):.4f} arcsec, max {offset.max():.4f} arcsec"
    )

    unique_hats = hats_plain.drop_duplicates("object_id", keep=False).set_index("object_id")
    unique_tap = tap_frame.drop_duplicates("object_id", keep=False).set_index("object_id")
    shared = unique_hats.index.intersection(unique_tap.index)
    print(f"  compared on {len(shared)} object_ids that are unique in both")
    separation = (
        SkyCoord(unique_hats.loc[shared, "ra"].to_numpy() * u.deg, unique_hats.loc[shared, "dec"].to_numpy() * u.deg)
        .separation(
            SkyCoord(unique_tap.loc[shared, "ra"].to_numpy() * u.deg, unique_tap.loc[shared, "dec"].to_numpy() * u.deg)
        )
        .arcsec
    )
    print(f"  position HATS ra/dec vs TAP right_ascension/declination: max {separation.max():.3e} arcsec")
    print(f"  tile id identical: {bool((unique_hats.loc[shared, 'tileid'] == unique_tap.loc[shared, 'tileid']).all())}")
    for column in compared_value_columns:
        hats_values = unique_hats.loc[shared, column].to_numpy(dtype="float64")
        tap_values = unique_tap.loc[shared, column].to_numpy(dtype="float64")
        both_nan = np.isnan(hats_values) & np.isnan(tap_values)
        same_float32 = np.asarray(hats_values.astype("float32") == tap_values.astype("float32")) | both_nan
        finite = np.isfinite(hats_values) & np.isfinite(tap_values)
        relative = np.abs(hats_values[finite] - tap_values[finite]) / np.maximum(np.abs(tap_values[finite]), 1e-30)
        print(
            f"  {column}: HATS dtype={hats_frame[column].dtype}, TAP dtype={tap_table[column].dtype}; "
            f"NaN/null HATS={int(np.isnan(hats_values).sum())}, TAP={int(np.isnan(tap_values).sum())}; "
            f"identical after float32 cast: {int(same_float32.sum())}/{len(shared)}; max relative "
            f"difference {relative.max():.2e}"
        )


def section_3_crossmatch(target_ra: float, target_dec: float) -> None:
    print("\n== 3. Cross-matches and joins ==", flush=True)
    mer = lsdb.open_catalog(
        f"{irsa_s3_root}/{mer_wide_collection}", columns=["object_id", "ra", "dec", "flux_vis_sersic"]
    )
    mer_cone = mer.cone_search(ra=target_ra, dec=target_dec, radius_arcsec=cone_radius_arcmin * 60.0)
    with timer("MER cone alone (compute)") as base:
        n_mer = len(mer_cone.compute())
    print(f"  MER sources in cone: {n_mer}")

    gaia = lsdb.open_catalog(gaia_collection_url, columns=["source_id", "ra", "dec", "phot_g_mean_mag", "parallax"])
    print(
        f"  Gaia DR3: rows={gaia.hc_structure.catalog_info.total_rows:,}, "
        f"margin_cache={'yes' if gaia.margin is not None else 'no'}"
    )
    with timer("crossmatch MER cone x Gaia DR3 (1 arcsec, nearest neighbour), compute") as gaia_timer:
        matched = mer_cone.crossmatch(
            gaia,
            radius_arcsec=crossmatch_radius_arcsec,
            n_neighbors=1,
            suffixes=("_euclid", "_gaia"),
            suffix_method="all_columns",
        ).compute()
    n_gaia = int(matched["source_id_gaia"].notna().sum())
    print(
        f"  Gaia DR3 matches: {n_gaia} of {n_mer} MER sources; median separation "
        f"{matched['_dist_arcsec'].median():.3f} arcsec; columns: {list(matched.columns)}"
    )

    legacy = lsdb.open_catalog(
        legacy_catalog_url,
        margin_cache=legacy_margin_url,
        columns=["OBJID", "RA", "DEC", "TYPE", "FLUX_R", "RELEASE", "MASKBITS"],
    )
    print(
        f"  Legacy Surveys DR10.1: rows={legacy.hc_structure.catalog_info.total_rows:,}, "
        f"margin_cache={'yes' if legacy.margin is not None else 'no'}"
    )
    with timer("crossmatch MER cone x Legacy Surveys DR10.1 (1 arcsec), compute") as legacy_timer:
        matched_legacy = mer_cone.crossmatch(
            legacy,
            radius_arcsec=crossmatch_radius_arcsec,
            n_neighbors=1,
            suffixes=("_euclid", "_ls"),
            suffix_method="all_columns",
        ).compute()
    n_legacy = int(matched_legacy["OBJID_ls"].notna().sum())
    print(
        f"  Legacy Surveys matches: {n_legacy} of {n_mer} MER sources; RELEASE values "
        f"{sorted(set(matched_legacy['RELEASE_ls'].dropna().tolist()))}; "
        f"types {matched_legacy['TYPE_ls'].value_counts().to_dict()}"
    )
    legacy_dr11 = lsdb.open_catalog(
        legacy_dr11_south_url, columns=["OBJID", "RA", "DEC", "TYPE", "FLUX_R", "RELEASE", "MASKBITS"]
    )
    print(
        f"  Legacy Surveys DR11.0 South (SLAC server): rows={legacy_dr11.hc_structure.catalog_info.total_rows:,}, "
        f"margin_cache={'yes' if legacy_dr11.margin is not None else 'no'}"
    )
    with timer("crossmatch MER cone x Legacy Surveys DR11.0 South (1 arcsec), compute") as dr11_timer:
        matched_dr11 = mer_cone.crossmatch(
            legacy_dr11,
            radius_arcsec=crossmatch_radius_arcsec,
            n_neighbors=1,
            suffixes=("_euclid", "_ls"),
            suffix_method="all_columns",
        ).compute()
    n_dr11 = int(matched_dr11["OBJID_ls"].notna().sum())
    print(
        f"  Legacy Surveys DR11 matches: {n_dr11} of {n_mer} MER sources; RELEASE values "
        f"{sorted(set(matched_dr11['RELEASE_ls'].dropna().tolist()))}; "
        f"types {matched_dr11['TYPE_ls'].value_counts().to_dict()}"
    )
    print(
        f"  (timings: cone {base['seconds']:.1f} s, Gaia {gaia_timer['seconds']:.1f} s, Legacy DR10.1 "
        f"{legacy_timer['seconds']:.1f} s, Legacy DR11 {dr11_timer['seconds']:.1f} s)"
    )

    morphology = lsdb.open_catalog(
        f"{irsa_s3_root}/mer_morphology_wide_survey",
        columns=["object_id", "sersic_sersic_vis_radius", "sersic_sersic_vis_index"],
    )
    physical = lsdb.open_catalog(
        f"{irsa_s3_root}/phz_physical_parameters_wide",
        columns=["object_id", "phz_pp_median_stellarmass", "phz_pp_median_sfr"],
    )
    morphology_cone = morphology.cone_search(ra=target_ra, dec=target_dec, radius_arcsec=cone_radius_arcmin * 60.0)
    physical_cone = physical.cone_search(ra=target_ra, dec=target_dec, radius_arcsec=cone_radius_arcmin * 60.0)
    with timer("join MER x morphology x PHZ physical parameters on object_id (three cone computes + pandas merge)"):
        mer_frame = mer_cone.compute()
        morphology_frame = morphology_cone.compute()
        physical_frame = physical_cone.compute()
    print(
        f"  rows in cone: MER={len(mer_frame)}, morphology={len(morphology_frame)}, PHZ physical "
        f"parameters={len(physical_frame)}; "
        f"duplicated object_id: MER={mer_frame['object_id'].duplicated().sum()}, "
        f"morphology={morphology_frame['object_id'].duplicated().sum()}, "
        f"PHZ={physical_frame['object_id'].duplicated().sum()}"
    )
    joined = (
        mer_frame.drop_duplicates("object_id", keep=False)
        .merge(morphology_frame.drop_duplicates("object_id", keep=False), on="object_id", suffixes=("", "_morph"))
        .merge(physical_frame.drop_duplicates("object_id", keep=False), on="object_id", suffixes=("", "_phz"))
    )
    print(
        f"  pandas merge on unique object_id: {len(joined)} rows; stellar mass non-null "
        f"{int(joined['phz_pp_median_stellarmass'].notna().sum())}"
    )
    try:
        with timer("lsdb.join MER x morphology on object_id (compute)"):
            lsdb_joined = mer_cone.join(
                morphology,
                left_on="object_id",
                right_on="object_id",
                suffixes=("_mer", "_morph"),
                suffix_method="all_columns",
            ).compute()
        print(f"  lsdb join rows: {len(lsdb_joined)}")
    except Exception as error:  # report which API route fails instead of hiding it
        print(f"  lsdb.join failed: {type(error).__name__}: {str(error)[:200]}")


def network_megabytes() -> float:
    counters = psutil.net_io_counters()
    return counters.bytes_recv / 1e6


def section_4_large_query(target_ra: float, target_dec: float, skip_tap: bool) -> None:
    print("\n== 4. Larger query: 30 arcmin cone, 5 columns ==", flush=True)
    columns = ["object_id", "ra", "dec", "flux_vis_sersic", "spurious_prob"]
    radius_arcmin = 30.0
    catalog = lsdb.open_catalog(f"{irsa_s3_root}/{mer_wide_collection}", columns=columns)
    cone = catalog.cone_search(ra=target_ra, dec=target_dec, radius_arcsec=radius_arcmin * 60.0)
    before = network_megabytes()
    with timer("HATS 30 arcmin cone compute") as hats_timer:
        frame = cone.compute()
    transferred = network_megabytes() - before
    memory_megabytes = frame.memory_usage(deep=True).sum() / 1e6
    print(
        f"  HATS: {len(frame):,} rows, {len(frame) / hats_timer['seconds']:,.0f} rows/s, in-memory "
        f"{memory_megabytes:.1f} MB, "
        f"system-wide network receive during the query {transferred:.0f} MB (includes other traffic)"
    )
    cache_dir.mkdir(parents=True, exist_ok=True)
    output_path = cache_dir / "ngc1483_mer_wide_30arcmin_hats.parquet"
    frame.to_parquet(output_path)
    print(f"  wrote {output_path} ({output_path.stat().st_size / 1e6:.1f} MB)")
    box = catalog.box_search(ra=(target_ra - 0.5, target_ra + 0.5), dec=(target_dec - 0.5, target_dec + 0.5))
    with timer("HATS 1 deg x 1 deg box (box_search) compute") as box_timer:
        box_frame = box.compute()
    print(f"  HATS box: {len(box_frame):,} rows, {len(box_frame) / box_timer['seconds']:,.0f} rows/s")
    if skip_tap:
        return
    adql = tap_cone_query(
        target_ra,
        target_dec,
        radius_arcmin / 60.0,
        "object_id, right_ascension, declination, flux_vis_sersic, spurious_prob",
    )
    with timer("TAP async 30 arcmin cone") as tap_timer:
        tap_table = run_query(adql)
    print(
        f"  TAP: {len(tap_table):,} rows, {len(tap_table) / tap_timer['seconds']:,.0f} rows/s; "
        f"HATS rows minus TAP rows = {len(frame) - len(tap_table)}"
    )


def read_text(url: str) -> str:
    response = requests.get(url, timeout=120)
    response.raise_for_status()
    return response.text


def section_5_footprint() -> None:
    print("\n== 5. Footprint / MOC ==", flush=True)
    catalog = lsdb.open_catalog(f"{irsa_s3_root}/{mer_wide_collection}", columns=["object_id"])
    structure = catalog.hc_structure
    print(f"  hc_structure.moc is {structure.moc!r} (the IRSA catalogue ships no moc.fits)")
    orders = [pixel.order for pixel in catalog.get_healpix_pixels()]
    print(
        f"  partitions: {len(orders)}, HEALPix orders {min(orders)}..{max(orders)}, order counts "
        f"{dict(zip(*np.unique(orders, return_counts=True), strict=True))}"
    )
    area_by_order = {order: full_sky_area_deg2 / (12 * 4**order) for order in (3, 4, 5, 6, 9)}
    print(f"  pixel area deg^2: {', '.join(f'order {k}: {v:.4f}' for k, v in area_by_order.items())}")
    print(
        f"  sum of partition areas (adaptive, mixed orders): "
        f"{sum(full_sky_area_deg2 / (12 * 4**order) for order in orders):.1f} deg^2"
    )

    base = f"{irsa_https_root}/{mer_wide_collection}/{mer_wide_catalog_name}"
    cache_dir.mkdir(parents=True, exist_ok=True)
    skymap_path = cache_dir / "mer_wide_skymap.fits"
    with timer("download skymap.fits"):
        skymap_path.write_bytes(requests.get(f"{base}/skymap.fits", timeout=120).content)
    with fits.open(skymap_path) as hdus:
        pixels = np.asarray(hdus[1].data["PIXEL"])
        counts = np.asarray(hdus[1].data["VALUE"])
        skymap_order = int(np.log2(hdus[1].header["NSIDE"]))
    skymap_area = len(pixels) * full_sky_area_deg2 / (12 * 4**skymap_order)
    print(
        f"  skymap.fits: order {skymap_order}, {len(pixels)} non-empty pixels, sum of counts "
        f"{counts.sum():,}, area {skymap_area:.0f} deg^2"
    )

    with timer("download healpix9_to_partition.txt"):
        order_nine = pd.read_csv(f"{base}/healpix9_to_partition.txt")
    order_nine_pixels = order_nine["_healpix_9"].to_numpy()
    print(
        f"  healpix9_to_partition.txt: {len(order_nine_pixels)} rows, {len(np.unique(order_nine_pixels))} "
        f"unique order-9 pixels, sum num_rows {order_nine['num_rows'].sum():,}"
    )
    moc = MOC.from_healpix_cells(
        np.unique(order_nine_pixels), np.full(len(np.unique(order_nine_pixels)), 9, dtype=np.uint8), max_depth=9
    )
    print(
        f"  MOC from non-empty order-9 pixels: max_order {moc.max_order}, area "
        f"{moc.sky_fraction * full_sky_area_deg2:.0f} deg^2"
    )
    density = order_nine.groupby("_healpix_9")["num_rows"].sum()
    median_density = float(density.median())
    for fraction in (0.1, 0.5):
        selected = density.index[density >= fraction * median_density].to_numpy()
        selected_moc = MOC.from_healpix_cells(selected, np.full(len(selected), 9, dtype=np.uint8), max_depth=9)
        print(
            f"  order-9 pixels with >= {fraction:g} x median count ({median_density:,.0f} sources/pixel): "
            f"{len(selected)} pixels, area {selected_moc.sky_fraction * full_sky_area_deg2:.0f} deg^2"
        )
    moc_path = cache_dir / "euclid_dr1_mer_wide_order9_moc.fits"
    moc.save(str(moc_path), format="fits", overwrite=True)
    print(
        f"  wrote {moc_path} ({moc_path.stat().st_size / 1e3:.0f} kB); EWS DR1 Foundation area to compare: ~1900 deg^2"
    )
    target = [t for t in gallery_targets if t.name == "NGC 1483"][0]
    print(f"  NGC 1483 inside the MOC: {bool(moc.contains_lonlat(target.ra_deg * u.deg, target.dec_deg * u.deg)[0])}")
    try:
        with timer("catalog.moc_search with the order-9 MOC (lazy, no compute)"):
            restricted = catalog.moc_search(moc)
        print(f"  moc_search partitions kept: {len(restricted.get_healpix_pixels())} of {len(orders)}")
    except Exception as error:
        print(f"  moc_search failed: {type(error).__name__}: {str(error)[:200]}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--skip-large", action="store_true", help="skip the 30 arcmin / 1 deg box test")
    parser.add_argument("--skip-tap", action="store_true", help="skip the large TAP query")
    arguments = parser.parse_args()

    target = [t for t in gallery_targets if t.name == "NGC 1483"][0]
    print(f"Target {target.name}: RA={target.ra_deg}, Dec={target.dec_deg}; lsdb {lsdb.__version__}")
    hats_frame = section_1_cone_search(target.ra_deg, target.dec_deg)
    section_2_compare_with_tap(hats_frame, target.ra_deg, target.dec_deg)
    section_3_crossmatch(target.ra_deg, target.dec_deg)
    if not arguments.skip_large:
        section_4_large_query(target.ra_deg, target.dec_deg, arguments.skip_tap)
    section_5_footprint()


if __name__ == "__main__":
    main()
