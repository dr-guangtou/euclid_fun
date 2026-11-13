# Euclid DR1 catalogues through IRSA HATS and LSDB (and cross-matching with other surveys)

> **Bottom line (checked hands-on, 2026-11-13; lsdb 0.11.1, hats 0.11.2; script `demo/06_hats_crossmatch.py`)**
> - IRSA serves 57 Euclid DR1 catalogues as HATS (HEALPix-partitioned Parquet) in the public AWS bucket
>   `s3://nasa-irsa-euclid-dr1/contributed/dr1/hats/reformatted_catalogs/<table>`.
>   - Coverage: MER, PHZ, SPE and SIR combined spectra; the MER wide survey alone has 888,152,165 rows.
>   - data.lsdb.io only has landing pages that point to this bucket.
> - **Same data as the ESA archive.** A 5' cone around NGC 1483 returns the same 9942 `object_id`s with identical
>   positions and fluxes on both. The ESA table has the same total row count, and every row carries
>   `data_set_release_part3 = 2`, so IRSA hosts the **DR1_R2** wide-survey catalogue.
> - **Use `s3://`, not `https://`.** The https form opens the catalogue but fails at `.compute()`.
> - **For small cones the ESA TAP is faster.** A HATS cone reads whole partitions of about 1.3 GB each, so any cone
>   costs ~40-50 s; TAP takes ~9 s for 5' and ~16 s for 30'.
> - **HATS pays off** for wide-area or full-survey work, for cross-matching against other HATS surveys, and for
>   workflows without TAP queues or job limits.
> - **Cross-match partners via LSDB:**
>   - Gaia DR3, DESI DR1 redshifts, AllWISE, NEOWISE, 2MASS, HSC PDR3 (per band);
>   - Legacy Surveys DR10.1, on data.lsdb.io;
>   - Legacy Surveys **DR11.0 North and South**, on a SLAC server linked from the data.lsdb.io portal.
>
>   Every Euclid HATS catalogue has a 10" margin cache, so cross-matches are correct at partition edges.

Related notes: ESA access routes in [03](03_data_access.md); the footprint in [09 §7.6](09_masks_flags_coverage.md);
catalogue columns in [06](06_catalogues_photometry_morphology.md).

## 1. What HATS/LSDB is

- **HATS** (Hierarchical Adaptive Tiling Scheme) partitions a catalogue into HEALPix pixels of adaptive order, with
  about equal rows per partition. It is stored as Parquet: `dataset/Norder=k/Dir=d/Npix=n/part0.snappy.parquet`,
  plus `hats.properties`, `partition_info.csv`, `skymap.fits`, `healpix9_to_partition.txt` and
  `_common_metadata` (the schema with units and descriptions).
- **Collection layout.** A "collection" directory holds the catalogue, a **margin cache** (sources within 10" of each
  partition edge, needed for correct cross-matches) and an **index table** (here `object_id`) for ID lookups.
- **LSDB** is the Python client (built on dask and nested-pandas). Operations are lazy: `open_catalog`,
  `cone_search`, `box_search`, `polygon_search`, `moc_search`, `id_search`, `crossmatch`, `join`. `.compute()`
  executes them and returns a `NestedFrame`, a pandas subclass with pyarrow dtypes.

## 2. The Euclid DR1 HATS catalogues (IRSA)

Root: `s3://nasa-irsa-euclid-dr1/contributed/dr1/hats/reformatted_catalogs/`. All 57 collections have a 10" margin
cache and an `object_id` index. All are anonymous, in AWS region us-east-1, and need `s3fs`.

| Collection | Rows | Columns | Partitions (orders) |
|---|---|---|---|
| `mer_catalogue_wide_survey` | 888,152,165 | 483 | 768 (3-6) |
| `mer_morphology_wide_survey` | 888,152,165 | 117 | 209 (2-5) |
| `mer_cutouts_wide_survey` | 888,152,165 | 36 | 224 (2-5) |
| `mer_catalogue_deep_survey` | 51,820,952 | 483 | 30 (3-6) |
| `mer_catalogue_deep_survey_photometry` | 26,008,743 | 724 | 19 (3-5) |
| `mer_morphology_deep_survey`, `mer_cutouts_deep_survey` | 51,820,952 | 117 / 36 | 14 / 17 |
| `phz_physical_parameters_wide` | 847,313,811 | 85 | 750 (3-6) |
| `phz_classification_wide` | 847,313,811 | 24 | 62 (0-4) |
| `phz_galaxy_sed_wide` | 846,826,349 | 131 | 555 (2-5) |
| `phz_nir_physical_parameters_wide` | 187,662,926 | 68 | 1845 (3-7) |
| `phz_*_deep_survey` (photo_z, physical_parameters, classification, ...) | 6-52 M | 50-85 | |
| `sir_combined_spectra` (1-D spectra, nested `spectrum` column) | 309,078,775 | 15 | 3557 (3-9) |
| `spectro_z_spe_*`, `spectro_model_spe_*`, `spectro_line_features_spe_*` (`_deep`, `_wide`, `_wide_survey`) | up to 10.3 G | 16-46 | |

The full 57-row table (rows, columns, partition orders) is in
[data_model/hats_irsa_survey_2026-11-13.md](data_model/hats_irsa_survey_2026-11-13.md).

**Not (yet) in HATS** (IRSA tutorial): `phz_photo_z_wide`, the `*_wide_mode`/`*_deep_mode` MER tables (EAFs and
calibration fields) and a merged-objects table like the Q1 one.

The column counts differ by source: ESA TAP 478, IRSA README 483, portal 482, LSDB 479 selectable. Use the
`_common_metadata` schema as the truth.

## 3. Differences from the ESA TAP tables (verified)

| Aspect | ESA TAP (`dr1.mer_catalogue_wide_survey`) | IRSA HATS (`mer_catalogue_wide_survey`) |
|---|---|---|
| Position / tile columns | `right_ascension`, `declination`, `tile_index` | `ra`, `dec`, `tileid` (only these three renamed; all names lower case, `-.()` -> `_`) |
| Extra columns | `data_set_release`, `_part1..3` | `has_spectrum`, `ra_from_object_id`, `dec_from_object_id`, `_healpix_9/19/29` |
| Release version | `data_set_release_part3 = 2` (DR1_R2) | no release column; equality with ESA shows it is DR1_R2 |
| Float type | float64 (values are float32 numbers) | float32; pyarrow dtypes with `<NA>`; use `.astype("float64")` before NumPy maths |
| Positions used for partitioning, cones and cross-matches | | `ra_from_object_id`/`dec_from_object_id` (derived from `object_id`; within 0.0004" of `ra`/`dec` in the test cone). Use `ra`/`dec` for science |
| `SELECT *` | **fails** in astroquery (`calblock_id_list` char-size error): list the columns | fine |
| `object_id` uniqueness | | not unique in SPE tables (one row per solution, line or grism) and in wide SIR spectra; joins need a rule |

## 4. Measured timings (single runs, home network)

| Operation | HATS (LSDB, S3) | ESA TAP |
|---|---|---|
| `open_catalog` (7 columns) | ~10 s | |
| 5' cone, MER wide (9942 rows) | 51 s, and again 46-51 s on repeat (no cache); 32 s in a later run | 8.7-9.9 s |
| 30' cone, 5 columns (356,927 rows; same count on both) | 41 s (8.6k rows/s; ~620 MB transferred) | 15.5 s (23k rows/s) |
| 1 deg x 1 deg box, 5 columns (306,630 rows) | 42 s | |
| 5' cone + Gaia DR3 cross-match (1") | 39 s (64 matches, median separation 0.084") | |
| 5' cone + Legacy Surveys DR10.1 cross-match (1") | 36 s (4568 matches) | |
| Legacy Surveys DR11.0 South, 5' cone (SLAC server) | open 23 s, cone 5.8 s (4171 sources, `RELEASE = 11010`; DR10.1 has 4408 in the same cone) | |
| 5' cone + Legacy Surveys DR11.0 South cross-match (1") | 45 s (4349 matches; types REX 1857, PSF 1734, EXP 407, DEV 243, SER 108) | |
| MER join morphology on `object_id` (`lsdb.join`, cone-restricted) | 84 s | |

Why the HATS cone is slow:
- The MER wide catalogue's order-5 partitions hold ~1.5 M rows in one ~1.3 GB file.
- A cone reads the selected columns of every partition it touches; NGC 1483 touches two.
- So run time scales with partition size, not cone size: a 30' cone is no slower than a 5' cone.
- A pyarrow `_healpix_9` filter over the whole dataset is slower still (162 s).

## 5. Cross-match partners available through LSDB (verified that each opens; cross-matches run where noted)

| Survey | URL for `lsdb.open_catalog` | Rows | Notes |
|---|---|---|---|
| Gaia DR3 | `https://data.lsdb.io/hats/gaia_dr3/` | 1.81 G | margins 10" and 5'; epoch J2016.0 (no proper-motion correction applied); cross-match run |
| Legacy Surveys DR10.1 (South, DECam) | `https://data.lsdb.io/hats/legacysurvey_dr10.1/legacysurvey` with `margin_cache=".../legacysurvey_dr10.1/legacysurvey_10arcs"` | 2.83 G | **the collection root fails to open**; upper-case column names (`RA`, `DEC`, `TYPE`, `FLUX_R`, `MASKBITS`); `RELEASE = 10000`; cross-match run |
| **Legacy Surveys DR11.0 South** (DECam griz: DECaLS, DES, DELVE, DeROSITAS) | `http://slac.data.lsdb.io:10942/lsdb/legacysurvey_dr11.0_south` | 3.56 G | not under `data.lsdb.io/hats/`; listed in the portal (`data.lsdb.io/data/DESI/`); margin present; 130 default columns (217 with `columns="all"`), including unWISE W1-W4 forced photometry and photo-z sweeps; `RELEASE = 11010`; cross-match run in `demo/06` |
| **Legacy Surveys DR11.0 North** (BASS/MzLS grz, Dec >= 32.375 deg) | `http://slac.data.lsdb.io:10942/lsdb/legacysurvey_dr11.0_north` | | listed in the portal; 115 default / 185 total columns; not opened here |
| DESI DR1 redshifts (zcat) | `https://data.lsdb.io/hats/desi/desi_dr1_zcat/` | 28.4 M | coordinates `TARGET_RA`, `TARGET_DEC`; key (`TARGETID`, `SURVEY`, `PROGRAM`); 10" margin; no DESI target in the NGC 1483 cone |
| HSC PDR3 forced photometry | `https://data.lsdb.io/hats/hsc_pdr3/hsc_pdr3-forced-<G,R,I,Z,Y>` | 0.73-0.78 G per band | one catalogue per band; margins in sibling `..._10arcs` folders, passed via `margin_cache=`; HSC overlaps the northern EWS and EMDS fields, not NGC 1483 |
| AllWISE / NEOWISE / 2MASS | `https://data.lsdb.io/hats/wise/allwise/`, `.../wise/neowise/`, `.../two_mass/` | 0.75 G / 18.7 G / 0.47 G | unWISE/CatWISE not found on data.lsdb.io (DR11 carries unWISE forced photometry) |
| Others on data.lsdb.io | DES, DELVE, SkyMapper DR4, eROSITA (eRASS1, DR2/eRASS3), SDSS DR18 spectra, ZTF, TESS, Rubin DP1/DP2, Euclid Q1 | | not checked; the home page also links CDS VizieR HATS (`vizcat.cds.unistra.fr/hats`, timed out from here), LIneA and Multimodal Universe |

Cross-match recipe:

```python
import lsdb  # uv add lsdb s3fs

euclid = lsdb.open_catalog(
    "s3://nasa-irsa-euclid-dr1/contributed/dr1/hats/reformatted_catalogs/mer_catalogue_wide_survey",
    columns=["object_id", "ra", "dec", "flux_vis_sersic", "spurious_prob", "det_quality_flag"],
)
legacy = lsdb.open_catalog(
    "http://slac.data.lsdb.io:10942/lsdb/legacysurvey_dr11.0_south",
    columns=["OBJID", "RA", "DEC", "TYPE", "FLUX_R", "MASKBITS"],
)
matched = (
    euclid.cone_search(ra=58.198, dec=-47.478, radius_arcsec=300)
    .crossmatch(legacy, radius_arcsec=1.0, n_neighbors=1, suffixes=("_euclid", "_ls"), suffix_method="all_columns")
    .compute()  # nothing is read before this line
)
```

## 6. Lessons and pitfalls

1. **`s3://` only for the Euclid bucket.** IRSA partitions are directories, which fsspec cannot list over HTTP.
   Metadata files (`hats.properties`, `partition_info.csv`, `skymap.fits`, `healpix9_to_partition.txt`) are fine
   over https.
2. **Restrict first, compute last.** Pass `columns=[...]` to `open_catalog` (Parquet reads only those column chunks)
   and apply the cone, box or polygon before `.compute()`. Never compute a full catalogue.
3. **No local cache.** Repeating a query pays the full cost again, so save results to Parquet under
   `~/data/euclid/hats_cache/`.
4. **Small cone around one galaxy: use the ESA TAP** (or the cutout service for images). Thousands of targets, area
   statistics or survey-scale cross-matches: use HATS. The cost is per partition, so batch targets that share
   partitions.
5. **Margins matter.** Cross-match only against catalogues opened with a margin cache. Legacy Surveys DR10.1 and HSC
   need it passed explicitly.
6. **Version is implicit.** HATS carries no release column; record the IRSA README date (2026-11-07) and the bucket
   path in your provenance.
7. **Ambiguous `object_id`s.** In SPE/SIR tables, choose a rule (best redshift solution, grism) before joining. MER,
   morphology and PHZ joins on `object_id` were 1:1 in the test cone.
8. **lsdb's "estimated size" is wrong.** It printed 764 MB for the 734 GB MER table (`hats_estsize` is in kB).
9. **No coverage MOC is shipped.** `catalog.hc_structure.moc` is `None`. Build one from `healpix9_to_partition.txt`
   (order 9; 2095 deg^2) or use the tile-polygon MOC ([09 §7.6](09_masks_flags_coverage.md)).
10. **External surveys handle large galaxies differently.** Legacy Surveys fits SGA galaxies as single objects, while
    Euclid shreds them ([06 §10.1](06_catalogues_photometry_morphology.md)). For a big galaxy, a missing LS
    counterpart does not prove that a Euclid entry is a fragment, because Euclid is deeper. In the 5' NGC 1483 cone,
    46% of the 9942 MER entries have a DR10.1 counterpart within 1".

## 7. Sources

- IRSA tutorial "Euclid DR1 HATS intro" (caltech-ipac.github.io/irsa-tutorials, updated 2026-11-11) and its sibling DR1
  TAP tutorials (MER images/catalogue, 1-D spectra, PHZ, SPE, cloud access).
- IRSA MER wide README (2026-11-07) in the bucket; `hats.properties` files.
- data.lsdb.io portal (`/data/catalogs.json`, `/data/DESI/Legacy_Survey_DR11.0_*/catalog.json`).
- Hands-on: `demo/06_hats_crossmatch.py` (all timings and comparisons above).
