# ESA web pages, archive help pages and astroquery documentation (DR1)

Local copies: `~/Desktop/euclid/web/` (HTML/rst), `~/Desktop/euclid/eds_help_mirror/` (Euclid Data Space help, 49
pages), `~/Desktop/euclid/docs/` (memos); plain text in `~/Desktop/euclid/text/{web,eds_help,docs}/`.

## ESA Cosmos pages

| Page | Content |
|---|---|
| https://www.cosmos.esa.int/web/euclid/euclid-dr1 | DR1-Foundation released 2026-11-12: ~13 months of observations (spring 2024 - spring 2025), ~1900 deg^2 EWS (14% of the final survey), >900 M galaxies, ~15 000 strong-lens candidates, >60 M quasar candidates, spectra of >160 M sources, 1.7 PB |
| https://www.cosmos.esa.int/web/euclid/dr1-data | Euclid Data Space = data discovery (archive, IVOA APIs, astroquery), visualisation (ESASky + HiPS), analysis (ESA Datalabs, moderated beta). Anonymous access allowed; registering (ESA Cosmos) adds longer ADQL time-outs, user space, Datalabs access. Alternative: IRSA (IPAC). Licence CC BY-NC 3.0 IGO. Helpdesk link |
| https://www.cosmos.esa.int/web/euclid/dr1-documentation | links to the Explanatory Supplement, the DR1 papers page and the "public memo" with the detailed product list |
| https://www.cosmos.esa.int/web/euclid/est-publications | ESA/EST memos, incl. `DR1-memo_260922.pdf` (EUCL-EST-ME-8-020 v1.3, content of DR1) and EUCL-ESAC-RP-8-017 v42 (list of supported data products, 2026-07-30) |

### DR1 memo (EUCL-EST-ME-8-020, 2026-09-22)
- Two stages: DR1-Foundation (2026-11-12: all raw data and calibrated images, catalogues, spectra) and full DR1
  (mid-2027: higher-level clustering/weak-lensing products). No reprocessing of DR1-Foundation products.
- WS: complete and valid observations 2024-02-14 to 2025-05-21 not crossing RA = 0 h; observations without
  ground-based counterpart or with one instrument down are "incomplete" and excluded; data between the two
  decontaminations (2024-03-23 to 2024-06-07) invalid, partly re-observed (RSD2025A infill).
- DR1-Foundation = all products of section 3 of RP-8-017 except 3.2.7 (SHE). Deep fields get one extra product
  (`DpdPhzDeepOutputCatalog`). For North CPC fields 13, 28, 29, 84, 85, 90 only LE1. PV LE2 only for SelfCal PV-001
  (single pass), F-014 and PV-005 COSMOS (Nov 2023).
- "No software will be made available by the Science Ground Segment for the DR1 release."
- Calibration products used by the SGS are released.

### List of supported data products (EUCL-ESAC-RP-8-017 v42)
LE1: `DpdVisRawFrame`, `DpdNispRawFrame`. LE2: VIS (`DpdVisCalibratedQuadFrame` = calibrated frame + background map
+ weight map + PSF; `DpdVisStackedFrame` = stack + weight + PSF; calibrated and stacked catalogues), NIR (calibrated
frame + background + PSF; stacked frame + PSF; catalogues), SIR (science frame, combined spectra), MER
(`DpdMerBksMosaic` = mosaic + background model + PSF + flag + RMS; segmentation map; final catalogue = catalogue +
morphology + cutouts), PHZ (photo-z + SED catalogues; L3 classification + physical parameters (galaxy, NIR, QSO) +
star template; deep output), SPE (redshift, models, lines), SHE (full DR1), SLE (`DpdSleDetectionOutput`). LE3 for
full DR1: VMPZ-ID, VMSP-ID, SEL-ID, WL, GC, clusters, PHZ for LE3.

## Euclid Data Space help pages (mirrored)

Most useful: `Images.html` (MER/stack/calibrated file lists and archive tables, join examples), `Catalogues.html`
(five MER data groups with row counts; PHZ/SPE/SIR tables), `Spectra.html` (DataLink, tables), `Bulk_download_of_data.html`
(curl recipe; note `release=sedm` in the example is Q1-only), `ADQL_*`, `Frequently_Asked_Questions_(FAQs).html`,
`Euclid_Archive_release_notes.html`, and the DR1-labelled known-issue pages:
- Ambiguous Gaia identifier: `gaia_id` = Gaia **DR3** source_id.
- Epoch of coordinates hidden: ICRS/Gaia-CRF3, epoch = `<ReferenceObservationDateTime>` of the tile XML (varies per
  tile; e.g. J2024.632); ignore `EQUINOX`.
- `basic_download_data_oid` and `to_be_published` are archive-internal columns.
- Multiple spectra per MER `object_id` (SelfCal repeated WIDE visits; COSMOS repeated; CDFS inside EDF-F).
- Mosaic `fov` sometimes larger than the real coverage (target "inside" but no data).
- SPE catalogue incomplete for 14 tile indices near tile edges (101365713, 101279563, 102009788, 102026534, 102036731,
  102038463, 102038572, 102042948, 102045496, 102139292, 102140855, 102154845, 102156286).
- Q1-era issues still relevant: NULLs stored as NaN or -99 (use `NULLIF`), list-typed fields garbled, conflicting
  data types, some DPDD columns absent from the archive, missing DPDD column descriptions, shopping-basket failures
  for large selections, bulk-download XML errors via DataLink.

## astroquery.esa.euclid documentation

Source: https://github.com/astropy/astroquery/blob/main/docs/esa/euclid/euclid.rst (docs.astropy.org is behind a
Cloudflare check). Default environment `PDR` (https://eas.esac.esa.int/); others `IDR`, `OTF`, `REG` are internal.
Documented methods: `get_status_messages`, `load_tables`/`load_table`, `cone_search` (preferred over `query_object`),
`launch_job`/`launch_job_async` (sync limit 2000 rows; async 7200 s), on-the-fly upload (`upload_resource`),
`get_product`, `query_sia` (SIA 2.0: calibrated/stacked/MER images), `get_cutout` (MER mosaics only, radius
<= 0.5 deg), `get_spectrum` + `get_datalinks` (DataLink), `login`/`login_gui`/`logout`, job management (10 GB user
quota). The docs' examples use Q1 (`q1.*`, `sedm`) - for DR1 use `dr1.*` tables and `schema='dr1'`
(see [../03_data_access.md](../03_data_access.md)).
