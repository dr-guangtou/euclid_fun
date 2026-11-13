> **Provenance.** Survey of the IRSA HATS Euclid DR1 catalogues and LSDB cross-match partners made on 2026-11-13
> (agent run, then re-run and checked; see [../14_hats_lsdb_access.md](../14_hats_lsdb_access.md) for the synthesis).
> **Correction:** the row below saying Legacy Surveys DR11 is "not hosted" is wrong. DR11.0 North and South are listed in
> the data.lsdb.io portal (`/data/catalogs.json`) and served from `http://slac.data.lsdb.io:10942/lsdb/legacysurvey_dr11.0_{north,south}`;
> DR11 South was opened and cross-matched (4349 matches in the 5' NGC 1483 cone). References to scratch files
> (`run2.out`, `survey.jsonl`) point to the original working folder and were not kept.

# Euclid DR1 via IRSA / LSDB HATS: findings (2026-11-13)

Legend: **[V]** = verified by running code on 2026-11-13 (lsdb 0.11.1, hats 0.11.2, anonymous access, home network);
**[D]** = from documentation / metadata files only.
Script: `demo/06_hats_crossmatch.py` (run log in this folder: `run2.out`; catalogue survey: `survey.jsonl`).

## 1. Where the data are

- **[V]** The real location is the IRSA AWS Open Data bucket `s3://nasa-irsa-euclid-dr1/contributed/dr1/hats/reformatted_catalogs/<table>` (region us-east-1, anonymous).
  `lsdb.open_catalog("s3://.../<table>")` finds the catalogue, the 10 arcsec margin cache and the `object_id` index inside the collection.
- **[V]** The data.lsdb.io portal pages `https://data.lsdb.io/Euclid/Euclid_DR1/<PF>/<Table>/` are only JS landing pages (Apache index of folders, then a single-page app).
  Their metadata (`https://data.lsdb.io/data/Euclid/Euclid_DR1/MER/Catalogue_(Wide_Survey)/catalog.json`) simply points to the same S3 URL; no data are hosted at data.lsdb.io for Euclid. The portal lists 482 columns for MER wide (see column counts below).
- **[V]** The portal tree has MER (7 tables), PHZ (13), SIR (1), SPE (36) = 57 HATS collections, the same 57 as the S3 listing (the IRSA tutorial says "56 + 1 spectra").
- **[D]** IRSA tutorial says Euclid DR1 has ~25 tables / 93 individual catalogues; HATS exists for 57; `phz_photo_z_wide` is "Not yet" released; `mer_catalogue_deep_mode`, `mer_catalogue_wide_mode` (COSMOS/CDFS/AEGIS, calibration fields) and their photometry/morphology tables have no HATS version yet. No merged-objects product (like Q1) yet, "in the near future".
- **[V]** `https://` instead of `s3://` for the IRSA S3 bucket: `open_catalog` works (metadata files are fetched fine), but `.compute()` fails with `NotADirectoryError`, because IRSA partitions are *directories* (`hats_npix_suffix=/`, `.../Npix=8588/part0.snappy.parquet`) and fsspec/HTTP cannot list S3 directories. Use `s3://` (needs `s3fs`; `uv add s3fs`).
- **[V]** Other surveys on data.lsdb.io work with `https://` (their partitions are single files). Gaia opens from the collection root; **Legacy Surveys collection root does not open** (`FileNotFoundError: Failed to read HATS`), open `.../legacysurvey_dr10.1/legacysurvey` plus `margin_cache=".../legacysurvey_10arcs"` instead.
- **[V]** IRSA wide MER README: version date 2026-11-07, 734 GB on disk, 888,152,165 rows, "483 columns (477 original + 6 HATS/HEALPix)". `lsdb` reports 479 selectable columns (the 3 hive columns Norder/Dir/Npix are hidden) and, wrongly, "estimated size 764 MB" (the `hats_estsize` property is in kB: it is 734 GB).

## 2. Catalogue table

### 2.1 Euclid DR1 (all with a 10 arcsec margin cache and an `object_id` index table; hats_builder `irsa-parquet`, all **[V]** from `hats.properties`, `partition_info.csv`, `_common_metadata`)

Rows match the numbers in the IRSA tutorial. "Columns" counts the Parquet schema (including `_healpix_9/19/29`, `ra_from_object_id`, `dec_from_object_id`, and Norder/Dir/Npix).
Wide-survey MER: `hats_order=6`; HEALPix column hats_col_ra/dec = `ra_from_object_id`/`dec_from_object_id` (see pitfalls).

| Catalogue (`s3://nasa-irsa-euclid-dr1/contributed/dr1/hats/reformatted_catalogs/<name>`) | Rows | Columns (incl. 6 HATS/HEALPix) | Partitions | Orders | Margin | Index |
|---|---|---|---|---|---|---|
| `mer_catalogue_deep_survey` | 51,820,952 | 483 | 30 | 3-6 | 10 arcsec | object_id |
| `mer_catalogue_deep_survey_photometry` | 26,008,743 | 724 | 19 | 3-5 | 10 arcsec | object_id |
| `mer_catalogue_wide_survey` | 888,152,165 | 483 | 768 | 3-6 | 10 arcsec | object_id |
| `mer_cutouts_deep_survey` | 51,820,952 | 36 | 17 | 2-5 | 10 arcsec | object_id |
| `mer_cutouts_wide_survey` | 888,152,165 | 36 | 224 | 2-5 | 10 arcsec | object_id |
| `mer_morphology_deep_survey` | 51,820,952 | 117 | 14 | 1-5 | 10 arcsec | object_id |
| `mer_morphology_wide_survey` | 888,152,165 | 117 | 209 | 2-5 | 10 arcsec | object_id |
| `phz_classification_deep_survey` | 51,550,740 | 22 | 17 | 2-5 | 10 arcsec | object_id |
| `phz_classification_wide` | 847,313,811 | 24 | 62 | 0-4 | 10 arcsec | object_id |
| `phz_galaxy_sed_wide` | 846,826,349 | 131 | 555 | 2-5 | 10 arcsec | object_id |
| `phz_nir_physical_parameters_deep_survey` | 6,415,078 | 74 | 25 | 3-5 | 10 arcsec | object_id |
| `phz_nir_physical_parameters_wide` | 187,662,926 | 68 | 1845 | 3-7 | 10 arcsec | object_id |
| `phz_photo_z_deep_survey` | 51,550,740 | 50 | 91 | 4-6 | 10 arcsec | object_id |
| `phz_physical_parameters_deep_survey` | 51,550,740 | 85 | 32 | 3-6 | 10 arcsec | object_id |
| `phz_physical_parameters_wide` | 847,313,811 | 85 | 750 | 3-6 | 10 arcsec | object_id |
| `phz_qso_physical_parameters_deep_survey` | 6,154,637 | 73 | 11 | 1-5 | 10 arcsec | object_id |
| `phz_qso_physical_parameters_wide` | 116,564,738 | 67 | 204 | 0-6 | 10 arcsec | object_id |
| `phz_star_sed_wide` | 12,275,216 | 131 | 13 | 0-2 | 10 arcsec | object_id |
| `phz_star_template_deep_survey` | 7,275,888 | 72 | 23 | 1-5 | 10 arcsec | object_id |
| `phz_star_template_wide` | 189,466,498 | 66 | 60 | 0-4 | 10 arcsec | object_id |
| `sir_combined_spectra` | 309,078,775 | 15 | 3557 | 3-9 | 10 arcsec | object_id |
| `spectro_line_features_spe_atomic_indices_deep` | 402,756,480 | 17 | 27 | 1-6 | 10 arcsec | object_id |
| `spectro_line_features_spe_atomic_indices_wide` | 3,329,048,376 | 17 | 87 | 0-6 | 10 arcsec | object_id |
| `spectro_line_features_spe_atomic_indices_wide_survey` | 3,033,760,428 | 17 | 74 | 0-4 | 10 arcsec | object_id |
| `spectro_line_features_spe_continuum_features_deep` | 22,375,360 | 17 | 23 | 1-5 | 10 arcsec | object_id |
| `spectro_line_features_spe_continuum_features_wide` | 184,947,132 | 17 | 11 | 0-1 | 10 arcsec | object_id |
| `spectro_line_features_spe_continuum_features_wide_survey` | 168,542,246 | 17 | 10 | 0-1 | 10 arcsec | object_id |
| `spectro_line_features_spe_line_features_deep` | 943,908,942 | 46 | 68 | 4-6 | 10 arcsec | object_id |
| `spectro_line_features_spe_line_features_wide` | 10,275,874,115 | 46 | 824 | 3-9 | 10 arcsec | object_id |
| `spectro_line_features_spe_line_features_wide_survey` | 9,524,030,381 | 46 | 745 | 3-6 | 10 arcsec | object_id |
| `spectro_line_features_spe_molecular_indices_deep` | 67,126,080 | 17 | 12 | 1-5 | 10 arcsec | object_id |
| `spectro_line_features_spe_molecular_indices_wide` | 554,841,396 | 17 | 18 | 0-2 | 10 arcsec | object_id |
| `spectro_line_features_spe_molecular_indices_wide_survey` | 505,626,738 | 17 | 13 | 0-2 | 10 arcsec | object_id |
| `spectro_model_spe_galaxy_models_deep` | 36,936,097 | 32 | 10 | 0-4 | 10 arcsec | object_id |
| `spectro_model_spe_galaxy_models_wide` | 848,103,802 | 32 | 226 | 2-7 | 10 arcsec | object_id |
| `spectro_model_spe_galaxy_models_wide_survey` | 800,701,396 | 32 | 202 | 2-5 | 10 arcsec | object_id |
| `spectro_model_spe_qso_models_deep` | 36,082,862 | 32 | 12 | 1-5 | 10 arcsec | object_id |
| `spectro_model_spe_qso_models_wide` | 778,784,939 | 32 | 50 | 0-3 | 10 arcsec | object_id |
| `spectro_model_spe_qso_models_wide_survey` | 735,094,834 | 32 | 47 | 0-3 | 10 arcsec | object_id |
| `spectro_model_spe_star_models_deep` | 13,629,798 | 19 | 10 | 0-4 | 10 arcsec | object_id |
| `spectro_model_spe_star_models_wide` | 293,768,741 | 19 | 18 | 0-2 | 10 arcsec | object_id |
| `spectro_model_spe_star_models_wide_survey` | 277,559,167 | 19 | 16 | 0-2 | 10 arcsec | object_id |
| `spectro_z_spe_classification_deep` | 7,456,278 | 16 | 10 | 0-4 | 10 arcsec | object_id |
| `spectro_z_spe_classification_wide` | 171,046,741 | 16 | 14 | 0-2 | 10 arcsec | object_id |
| `spectro_z_spe_classification_wide_survey` | 161,471,115 | 16 | 13 | 0-2 | 10 arcsec | object_id |
| `spectro_z_spe_galaxy_candidates_deep` | 36,910,593 | 29 | 10 | 0-5 | 10 arcsec | object_id |
| `spectro_z_spe_galaxy_candidates_wide` | 848,016,459 | 29 | 537 | 2-7 | 10 arcsec | object_id |
| `spectro_z_spe_galaxy_candidates_wide_survey` | 800,614,053 | 29 | 504 | 2-5 | 10 arcsec | object_id |
| `spectro_z_spe_qso_candidates_deep` | 36,063,712 | 26 | 10 | 0-5 | 10 arcsec | object_id |
| `spectro_z_spe_qso_candidates_wide` | 778,703,735 | 26 | 296 | 2-7 | 10 arcsec | object_id |
| `spectro_z_spe_qso_candidates_wide_survey` | 735,013,630 | 26 | 251 | 2-5 | 10 arcsec | object_id |
| `spectro_z_spe_quality_deep` | 51,930,919 | 42 | 10 | 0-4 | 10 arcsec | object_id |
| `spectro_z_spe_quality_wide` | 933,172,778 | 42 | 71 | 0-5 | 10 arcsec | object_id |
| `spectro_z_spe_quality_wide_survey` | 875,837,267 | 42 | 62 | 0-4 | 10 arcsec | object_id |
| `spectro_z_spe_star_candidates_deep` | 13,622,726 | 22 | 12 | 1-5 | 10 arcsec | object_id |
| `spectro_z_spe_star_candidates_wide` | 293,737,969 | 22 | 37 | 0-3 | 10 arcsec | object_id |
| `spectro_z_spe_star_candidates_wide_survey` | 277,528,395 | 22 | 35 | 0-3 | 10 arcsec | object_id |
### 2.2 Cross-match targets (**[V]** properties read; rows/columns/orders from `hats.properties`, `partition_info.csv`, `_common_metadata`)

| Survey | URL for `lsdb.open_catalog` | Rows | Columns | Margin cache | Orders (partitions) |
|---|---|---|---|---|---|
| Gaia DR3 (gaia_source, J2016.0) | `https://data.lsdb.io/hats/gaia_dr3/` | 1,811,709,771 | 153 | 10 arcsec (default) and 5 arcmin; index on source_id | 2-6 (2016) |
| DESI DR1 zcat (zall-pix-iron, 136 cols; key `TARGETID,SURVEY,PROGRAM`; coords `TARGET_RA/TARGET_DEC`) | `https://data.lsdb.io/hats/desi/desi_dr1_zcat/` (identical to `desi_dr1_zcat_2026-10`; `desi_dr1_zcat_2026-02-06` is an older build with 5 arcsec margin, hats 0.8) | 28,425,963 | 137 | 10 arcsec (`desi_dr1_zcat_10arcs`); TARGETID index | 0-3 (75) |
| Legacy Surveys DR10.1 (DECam, **South only**, RELEASE=10000) | `https://data.lsdb.io/hats/legacysurvey_dr10.1/legacysurvey` + `margin_cache="https://data.lsdb.io/hats/legacysurvey_dr10.1/legacysurvey_10arcs"` (collection root fails) | 2,827,055,986 | 228 (UPPERCASE names: `RA`, `DEC`, `OBJID`, `TYPE`, `FLUX_R`) | 10 arcsec (separate dir); OBJID index | 3-10 (13,389); `moc_sky_fraction=0.607` (about 25,000 deg^2) |
| Legacy Surveys DR10 North / DR11 | **(wrong, see Provenance note: DR11 is on a SLAC server)** not under `data.lsdb.io/hats/` (no `legacysurvey_dr11`, no North): probes at (180,+40) and EDF-N (269.6,+66.6) returned 0 sources; COSMOS (150.1,+2.2) returned DR10 sources | | | | |
| AllWISE | `https://data.lsdb.io/hats/wise/allwise/` | 747,634,026 | 299 | 10 arcsec; indexes cntr, designation | 3-4 (1071) |
| NEOWISE (single-exposure) | `https://data.lsdb.io/hats/wise/neowise/` | 18,668,416,994 | 144 | 5 arcsec; no collection index | 5-9 (39,774) |
| unWISE, CatWISE | **not on data.lsdb.io** (no matching directory under `/hats/`; not probed on CDS vizcat, which timed out) | | | | |
| 2MASS | `https://data.lsdb.io/hats/two_mass/` | 470,992,970 | 61 | 5 arcsec | 1-4 (219) |
| HSC PDR3 forced, one catalogue per band (G, R, I, Z, Y); no collection wrapper | `https://data.lsdb.io/hats/hsc_pdr3/hsc_pdr3-forced-I` (and G/R/Z/Y) | G 783,961,389; R 779,192,787; I 757,603,782; Z 771,110,298; Y 731,099,731 | 242 | sibling dirs `hsc_pdr3-forced-<B>_10arcs` exist (HTTP 200); pass via `margin_cache=` | 2/4-10 (2010-2574) |

Other data.lsdb.io top-level directories seen **[V]**: alerce, delve, des, desi, dp1, dp2, erosita, erosita_dr2_erass3, euclid_q1, gaia_dr3, gaia_dr3_epoch_phot, gaia_edr3_distances, heasarc_photon, hsc_pdr3, legacysurvey_dr10.1, macho, mock_dp1, rubin_alert_archive, sdss_dr7_spectra, sdss_dr18_specphotoall, skymapper_dr4, tess, the_monster, tns, two_mass, vsx, wise, ztf_dr14/16/20/22.
No HSC or DESI cross-match was run (neither is expected to cover NGC 1483).

## 3. IRSA tutorials (source: github.com/Caltech-IPAC/irsa-tutorials, `tutorials/euclid/`) **[D]**

- `hats-catalogs/1-euclid-dr1-hats-intro.md` (updated 2026-11-11; the page asked): catalogue list and row counts; naming (`euclid_dr1_reformatted_catalogs_<table>-hats` inside collection `<table>`); schema from `_common_metadata` with units/descriptions via pyarrow; pyarrow-dataset filter query (bright point sources); `lsdb.open_catalog(s3://..., columns=[...]).cone_search(...)`; EX Dra spectrum from `sir_combined_spectra` (nested `spectrum` column; use `mask`, `FSCALE=1e-16`).
  Gotchas listed there: (a) `object_id` is **not unique** (truncated-coordinate IDs; SPE tables have several rows per object, one per redshift solution/line/grism); `id_search` returns all rows; joins need a rule for duplicates. (b) All column names lower-cased, `-.()` become `_` (`E(B-V)` -> `e_b_v_`). (c) MER renames: `ra`=RIGHT_ASCENSION, `dec`=DECLINATION, `tileid`=TILE_INDEX. (d) Added columns `ra_from_object_id`, `dec_from_object_id`, `_healpix_9/19/29`; HATS columns `Norder/Npix/Dir` are not inside the files. (e) Table name is NOT prepended to column names (unlike the Q1 merged catalogue). (f) `signal` unit metadata of the spectra omits the 1e-16 scale.
- `hats-catalogs/1-euclid-q1-hats-intro.md`, `4-euclid-q1-hats-magnitudes.md` (Q1 merged-objects HATS, flux types, aperture vs template magnitudes), `techniques-and-tools/irsa-hats-with-lsdb.md` (Q1 + ZTF DR24: cone/box/index searches, crossmatch, light curves). Not DR1.
- TAP-based DR1 intros (updated 2026-11-12): `1_Euclid_intro_MER_images`, `2_Euclid_intro_MER_catalog` (four MER tables, `spurious_prob < 0.7` recommended, total-flux cookbook, DR1 vs Q1 fluxes must not be mixed), `3_Euclid_intro_1D_spectra`, `4_Euclid_intro_PHZ_catalog`, `5_Euclid_intro_SPE_catalog`, `euclid-cloud-access` (cutouts and spectra from S3). No DR1 tutorial uses a MOC/footprint; none covers cross-matching Euclid DR1 with other surveys.

## 4. Hands-on results (NGC 1483, RA 58.19837, Dec -47.47752, 5 arcmin cone)

### 4.1 Timings **[V]** (single run each; home network to us-east-1 and to the ESA archive; not repeated)

| Operation | Time |
|---|---|
| `lsdb.open_catalog(s3 collection, columns=7 cols)` | 10.4 s (also 9.7 s in an earlier run) |
| HATS 5 arcmin cone, first call | 51.0 s (9,942 rows) |
| HATS same cone again ("warm") | 50.7 s -> no data cache in LSDB; fsspec/S3 give no benefit |
| TAP async 5 arcmin cone (anonymous, 8 columns) | 8.7 s (9,942 rows) |
| HATS 30 arcmin cone, 5 columns | 41.4 s, 356,927 rows (8,631 rows/s); in-memory 20.0 MB; 623 MB received system-wide during the call (psutil net counter, includes other traffic) |
| HATS box 1 deg (RA, not cos(dec)-corrected, so ~0.68 deg^2) x 1 deg Dec | 42.3 s, 306,630 rows (7,252 rows/s) |
| TAP async 30 arcmin cone, 5 columns | 15.5 s, 356,927 rows (23,030 rows/s); identical row count to HATS |
| MER cone + Gaia DR3 crossmatch (1 arcsec, `n_neighbors=1`) | 38.6 s total (MER cone alone 35.6 s in that run) |
| MER cone + Legacy Surveys DR10.1 crossmatch (1 arcsec) | 35.6 s total |
| 3 cone computes (MER, morphology, PHZ physical params) + pandas merge | 116.3 s |
| `lsdb.join` MER x morphology on object_id (cone-restricted left) | 83.7 s, 9,942 rows |

Why the HATS cone is slow **[V]**: the cone touches 2 order-5 partitions (pixels 8582 and 8588), each ~1.5 M rows in one ~1.3 GB parquet file (`part0.snappy.parquet`, 1283.9 MB for pixel 8582). LSDB reads the requested column chunks of both whole partitions (3.0 M rows) and then filters to the cone. Run time is dominated by partition size, not by cone size: a 30 arcmin cone is as fast as a 5 arcmin cone. HATS only pays off for large areas, many columns' worth of cross-matching, or no-TAP-queue workflows; for small cones ESA TAP is faster (5.8x for the 5' cone, 2.7x for the 30' cone in these runs).
A pyarrow `dataset(...).to_table(filter=_healpix_9 isin [cone order-9 pixels])` on the full dataset was *slower* (162 s for 35,553 rows in a 5' cone, 12-column read incl. `_healpix_9`; the 3.3 s was just dataset discovery) than LSDB; do not use it for cones.

### 4.2 HATS (IRSA) vs ESA TAP, same cone **[V]**

- Rows: 9,942 vs 9,942. `object_id` overlap: both 9,942; only-HATS 0; only-TAP 0. No duplicated `object_id` in either.
- Total table rows: ESA `SELECT COUNT(*) FROM dr1.mer_catalogue_wide_survey` = 888,152,165 = HATS `hats_nrows`. ESA `GROUP BY data_set_release_part3` gives a single value, 2, for all 888,152,165 rows. So IRSA's HATS hosts the same wide-survey DR1 table as ESA, i.e. the DR1_R2 wide release (identical row count and identical values; the HATS table itself has **no** `data_set_release*` columns, so the version cannot be read from HATS; it has to be inferred from equality with ESA).
- Values (9,942 shared unique ids): `ra`/`dec` vs `right_ascension`/`declination` identical (max difference 0.0 arcsec); `tileid` identical; `flux_vis_sersic`, `flux_detection_total`, `spurious_prob` identical after casting TAP float64 to float32 (9,942 of 9,942; max relative difference 0.0). HATS stores `float` (float32); TAP delivers float64 (values are the float32 numbers).
- NaN/null: `flux_vis_sersic` has 12 null/NaN in both; LSDB returns pyarrow dtypes (`float[pyarrow]`, `<NA>`); TAP gives masked/NaN floats. Convert with `.astype("float64")` for NumPy-style NaN.
- Column naming: HATS names are the lower-case ESA names except three renames (`right_ascension` -> `ra`, `declination` -> `dec`, `tile_index` -> `tileid`). Name-set comparison with `TAP_SCHEMA.columns`: ESA 478 columns, HATS 483 (479 selectable). ESA-only: `data_set_release`, `data_set_release_part1/2/3`, `declination`, `right_ascension`, `tile_index`. HATS-only: `ra`, `dec`, `tileid`, `has_spectrum`, `ra_from_object_id`, `dec_from_object_id`, `_healpix_9/19/29`, `Norder`, `Dir`, `Npix`.
- Cone geometry: LSDB's cone uses `ra_from_object_id/dec_from_object_id` (the HATS ra/dec columns), not `ra/dec`. They differ from the barycentre by median 0.0002 arcsec, max 0.0004 arcsec in this cone, so the sets agreed exactly; only sources within ~0.0004 arcsec of the cone edge could differ.

### 4.3 Cross-matches **[V]** (1 arcsec, `n_neighbors=1`, cone of 9,942 MER sources; crossmatch returns matched rows only)

- Gaia DR3 (10 arcsec margin present): 64 matches, median separation 0.084 arcsec. A plain LSDB cone on Gaia DR3 with the same radius returned 67 sources (LSDB cone on Gaia, earlier probe), so 3 Gaia sources have no MER counterpart within 1 arcsec (bright stars/saturation expected; not investigated). Gaia epoch 2016.0 vs Euclid ~2024: no proper-motion correction applied.
- Legacy Surveys DR10.1: 4,568 matches (46%), all RELEASE 10000; types REX 2262, PSF 1490, EXP 518, DEV 189, SER 109. The LS probe cone of the same radius around the target held 4,408 LS sources (earlier probe; the cross-match counts MER sources with a neighbour, which can exceed the LS count when MER deblends). Resulting columns are suffixed: `object_id_euclid`, `source_id_gaia`, ... plus `_dist_arcsec`. Pass `suffix_method="all_columns"` explicitly (lsdb 0.11 emits a FutureWarning that the default will change to overlapping columns only).
- MER x morphology x PHZ physical parameters on `object_id`: 9,942 rows in each catalogue's cone, no duplicate object_id in the cone, 9,942 merged rows (`phz_pp_median_stellarmass` non-null in all). `lsdb.join(left_on="object_id", right_on="object_id")` also works (9,942 rows). Morphology/PHZ have their own partitioning (orders 2-5 and 3-6), but the HEALPix coordinates are the same object_id-derived ones, so alignment works.

### 4.4 Footprint / MOC **[V]**

- `catalog.hc_structure.moc` is `None`: IRSA's catalogue ships no `moc.fits` and `hats.properties` has no `moc_sky_fraction` (the Legacy Surveys one does: 0.60724).
- `partition_info.csv`: 768 partitions, adaptive HEALPix orders 3 (3 partitions), 4 (46), 5 (685), 6 (34). Order 5 pixel = 3.36 deg^2; the partitions are sparse in density-adaptive sense, so partition areas (sum 3,107 deg^2) overstate the footprint.
- `skymap.fits` (order 6, nside 64, sparse explicit table PIXEL/VALUE): 2,940 non-empty order-6 pixels, counts sum to 888,152,165, area 2,468 deg^2 (0.839 deg^2 per pixel). The README names `skymap.fits` as "row counts per order-6 pixel".
- `healpix9_to_partition.txt` (columns `_healpix_9,Norder,Dir,Npix,num_rows`): 159,788 non-empty order-9 pixels (0.0131 deg^2, ~0.1 deg), sum of `num_rows` = 888,152,165. A MOC built from them with `mocpy.MOC.from_healpix_cells(..., max_depth=9)` has area **2,095 deg^2**; keeping only pixels with >= 0.1 / >= 0.5 x median source count (median 5,725/pixel) gives 2,061 / 1,997 deg^2. This is an upper bound on the true covered area (edge pixels counted whole) and is ~5-10% above the quoted ~1,900 deg^2 (DR1 Foundation EWS, from the IRSA tutorial). NGC 1483 is inside the MOC. Saved as `~/data/euclid/hats_cache/euclid_dr1_mer_wide_order9_moc.fits` (66 kB) by the script.
- `catalog.moc_search(moc)` works lazily (0.04 s, but with the catalogue's own coverage MOC it keeps all 768 partitions).

## 5. Pitfalls and lessons

1. **s3 vs https [V]**: Euclid HATS must be opened with `s3://` (anonymous; needs `s3fs`). `https://...s3.us-east-1.amazonaws.com/...` opens but fails on compute (`NotADirectoryError`). Metadata files (`hats.properties`, `partition_info.csv`, `skymap.fits`, `healpix9_to_partition.txt`, `schema.txt`) are fine over https.
2. **Slow small queries [V]**: ~1.3 GB per order-5 partition; every cone costs ~40-50 s; there is no local cache; repeated calls pay again. Save results (`frame.to_parquet(~/data/euclid/hats_cache/...)`). Chain `columns=` selection (reads only those column chunks) and cone/box restriction before `.compute()`; do not call `.compute()` on a full catalogue.
3. **`SELECT *` on the ESA TAP fails [V]** for `dr1.mer_catalogue_wide_survey` in astroquery (`E01: Invalid size specifier '100x' for a char field (in field 'calblock_id_list')`); list columns explicitly. HATS has no such problem.
4. **No release-version column in HATS [V]**: `data_set_release_part3` exists only in ESA TAP; equality with ESA (rows 888,152,165, values identical) is the evidence that IRSA has DR1_R2 wide survey.
5. **Positions used by LSDB [V]**: partitioning/cone/crossmatch use `ra_from_object_id/dec_from_object_id` (object_id-derived, truncated), not the catalogue `ra/dec`; differences are <= 0.0004 arcsec here, negligible for 1 arcsec matching. Use `ra`/`dec` for science positions.
6. **Dtypes [V]**: pyarrow-backed (`float[pyarrow]`, `int64[pyarrow]`), nulls are `<NA>`; convert before NumPy/astropy math. `lsdb` 0.11 returns `NestedFrame` (pandas subclass).
7. **object_id not unique [D, none in this cone]**: expected for SPE tables (several rows per object) and wide SIR spectra (RGS/BGS). Negative object_ids are normal at Dec < 0 (e.g. -582420995475493496).
8. **Legacy Surveys collection root fails [V]**; use the `/legacysurvey` catalogue directory with explicit `margin_cache`. Uppercase column names. DR10.1 is South only (RELEASE 10000); the user's North/DR11 needs are not served by LSDB. unWISE/CatWISE not found on data.lsdb.io.
9. **Crossmatch API [V]**: `left.crossmatch(right, radius_arcsec=1.0, n_neighbors=1, suffixes=(...), suffix_method="all_columns")`; both catalogues must have margins for correct results at partition edges (all Euclid, Gaia, DESI, Legacy, AllWISE do; the HSC margins are separate folders and must be passed via `margin_cache`). Gaia margin: default 10 arcsec; a 5 arcmin one also exists.
10. **Column counts differ by source [V]**: ESA 478, README 483, `catalog.json` portal 482, lsdb 479 selectable. Use the schema (`_common_metadata`, `schema.txt` with units and descriptions) as truth.
11. **lsdb "estimated size" is wrong in units [V]**: shows 764 MB for the 734 GB catalogue.
12. **Wide vs wide_survey SPE tables [V row counts only]**: SPE tables come in `_deep`, `_wide_survey` and `_wide` variants (`_wide` has more rows, presumably adding wide-mode fields, not checked; e.g. `spectro_z_spe_quality_wide` 933,172,778 rows vs `_wide_survey` 875,837,267). MER and PHZ use `_wide_survey` / `_wide` suffix as listed in the tutorial.
13. **astropy / lsdb warnings**: `UnitsWarning: 'Angstrom' deprecated` appears with TAP results; `FutureWarning` for `suffix_method`. Harmless.
14. Environment: `uv add s3fs psutil` were added to `pyproject.toml` (psutil only for the network-byte counter in section 4; remove it from the script if unwanted). `uv add s3fs` also pinned `python-dateutil` back to 2.9.0.post0.
15. **Not done**: Euclid-on-HSC cross-match (HSC not covering NGC 1483), DESI cross-match (no DESI target in the cone, not run), repeat timings for variance, https vs s3 speed (https cannot compute), `hats_cache` content is two small files (22.1 MB parquet, 66 kB MOC, 55 kB skymap).
