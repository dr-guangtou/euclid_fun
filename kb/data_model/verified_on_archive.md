# Facts verified hands-on against the Euclid Science Archive (DR1 release day, 2026-11-12/13)

These were checked by running queries and downloading files (scripts in `scripts/` and `demo/`). Where they differ
from the papers, DPDD or archive help pages, **this note wins** (and the discrepancy is listed in
[../11_known_issues.md](../11_known_issues.md)).

## Archive structure

- TAP endpoint `https://eas.esac.esa.int/tap-server/tap`; the public schemas include `dr1` (134 tables incl. `ivoa`),
  `q1`, `tap_schema`. Full column dump: [tap/README.md](tap/README.md).
- `dr1.data_release`: two DR1 releases, `DR1_R1` (version 1) and `DR1_R2` (version 2), plus internal on-the-fly sets.
  - `dr1.mer_catalogue_wide_survey` rows carry `data_set_release_part3 = 2` (= `DR1_R2`);
    `dr1.mer_catalogue_deep_survey` rows carry version 1 (= `DR1_R1`).
- `dr1.mosaic_product` columns `release_name`, `purpose`, `processing_mode` distinguish the mosaic families:

  | Family | release_name | purpose | processing_mode | tile prefix / size | # VIS tiles |
  |---|---|---|---|---|---|
  | Wide survey | DR1_R2 | DATA_RELEASE | WIDE | 102..., 32'x32' (19200^2 px) | 8975 (+16 duplicates) |
  | Deep stacks (EDF-N/S/F) | DR1_R1 (+ some DR1_R2) | DATA_RELEASE_DEEP | DEEP | 101..., 17'x17' (~10200^2 px) | 1117 (R1) + 251 (R2) |
  | Single visits of the deep fields at wide depth | DR1_R1/DR1_R2 | DATA_RELEASE_DEEP | WIDE | 102... (several per tile, one per visit) | 2048 (R1) + 918 (R2) |
  | Other wide-like fields (self-cal, EMDS, ...) | DR1_R1 | DATA_RELEASE | WIDE/DEEP | | 617 + 122 |

- A few wide tiles (e.g. 102158273) have **two mosaic files per band** in the same release; choose the most recent
  `creation_date`.
- Inside the Euclid Deep Fields the `DATA_RELEASE`/`WIDE` mosaic can be **all zeros at the target although the `fov`
  polygon contains it** (seen for PGC 61126 in EDF-N, tile 102158273); use the deep stack (`DATA_RELEASE_DEEP`/`DEEP`)
  or the deep-visit mosaics there. Always check a cutout for zeros/NaNs.
- Auxiliary MER files per mosaic (`dr1.aux_mosaic`, join on `mosaic_product_oid`), with `stype`:
  `RMS`, `FLAG`, `BKG` (= `EUC_MER_BGMOD-*`, the subtracted background model), `PSF` (= `EUC_MER_CATALOG-PSF-*`),
  `GRID_PSF`, `BRIGHT_STAR_MASKS` (JSON), `LAYERS` (`EUC_MER_DETECTOR-LAYERING-*`, VIS/NIR only),
  `FILTER_TRANSMISSION` (EXT only).
- Other product tables: `dr1.observation_stack` (VIS `DpdVisStackedFrame` 6367 in DR1_R1; NIR `DpdNirStackedFrame`
  15165 R1 + 1167 R2), `dr1.calibrated_frame` (VIS `DpdVisCalibratedQuadFrame` 42092; NIR `DpdNirCalibratedFrame`
  66723 R1 + 4936 R2), `dr1.basic_download_data` (catalogue files: `dpdMerFinalCatalog` 14064, `dpdPhzPfOutputCatalog`
  11135, `dpdPhzPfOutputForL3` 12670, `dpdPhzDeepOutputCatalog` 1535, `dpdSpePfOutputCatalog` 12728, VMPZ HEALPix maps).

## Files and units (headers of tile 102021980)

| File | Shape / type | BUNIT | MAGZERO | Notes |
|---|---|---|---|---|
| `EUC_MER_BGSUB-MOSAIC-VIS_TILE*.fits` | 19200x19200 float32, 1.47 GB, primary HDU | `ADU/s` | 24.5 | `COMBINET = MEDIAN`, `SOFTNAME = CT_SWarp`, CD matrix, 0.1"/px |
| `EUC_MER_BGSUB-MOSAIC-NIR-H_TILE*.fits` | same | `ELECTRON/s` | 30.0 (Y 29.8, J 30.1) | |
| `EUC_MER_BGMOD-<band>_TILE*.fits` | same grid and unit, no MAGZERO | as mosaic | use the mosaic's | add to BGSUB to undo the MER sky step |
| `EUC_MER_GRID-PSF-VIS_TILE*.fits` | HDU1 19200x19200 "PSF image" (stamps on a 120-px grid), HDU2 table `x, y, FWHM` (25 597 rows) | ADU | | stamp centres at x, y = 61, 181, 301, ... (1-based); each stamp is 21x21 px (2.1"), peak at (10, 10); stamp sums: median 0.958 (9 stamps < 0.9); median FWHM 0.201" |
| `EUC_MER_CATALOG-PSF-NIR-H_TILE*.fits` | HDU1 13455x13455 mosaic of 45x45-px stamps (4.5"), HDU2 table `x_center, y_center, x, y, RA, Dec, FWHM` (88 820 rows) | | | one stamp per catalogue object; median sum 0.984, median FWHM 0.559"; 0.73 GB |
| `EUC_MER_STAR-MASKS-VIS_TILE*.json` | 2 MB JSON | | | bright-star mask polygons |
| `dr1.mosaic_product.zero_point` | | | | equals MAGZERO (VIS 24.5, Y 29.8, J 30.1, H 30.0, EXT 30.0) |

Conversions: `m_AB = MAGZERO - 2.5 log10(pixel)`, `mu = MAGZERO - 5 - 2.5 log10(pixel)` [mag/arcsec^2],
`F[microJy] = pixel * 10**(-0.4 (MAGZERO - 23.9))`; catalogue fluxes in microJy (ZP 23.9).

## Services

- **Cutouts**: `https://eas.esac.esa.int/sas-cutout/cutout?filepath=<file_path>/<file_name>&POS=CIRCLE,<ra>,<dec>,<r_deg>`
  works anonymously for `BGSUB` mosaics and `FLAG` maps; fails (HTTP 500 "CTYPE1 not found") for `BGMOD` and `RMS`
  maps, and is not meant for PSF files. `file_path` is the `/data/euclid/repository_dr1/...` value from the table.
  Under load it sometimes returns HTTP 200 with a non-FITS body: retry. A 1' radius VIS cutout (1201^2 px) took
  2-20 s (up to minutes under load). Maximum radius 0.5 deg (astroquery check).
- **Full files**: `https://eas.esac.esa.int/sas-dd/data?file_name=<name>&release=dr1&RETRIEVAL_TYPE=FILE` works
  anonymously for every DR1 product tested (mosaics, BGMOD, PSF, JSON). With the Q1 default `release=sedm`
  (astroquery `schema='sedm'`) the request fails with HTTP 401. A 1.47 GB mosaic streamed in ~230 s (~6.5 MB/s).
- **astroquery**: PyPI 0.4.11 (Nov 2026) `get_cutout` produced empty files for DR1 and has no `query_sia`; the GitHub
  `main` version (0.4.12.dev) works (`get_cutout(file_path=..., coordinate=..., radius=...)`) and has
  `query_sia` + `dsr_part1/2/3` release selectors. `login()` with ESA Cosmos credentials works for TAP, data, cutout
  and SIA services.
- **SIA** (`Euclid.query_sia`) returned only Q1 products on 2026-11-12 (0 rows for DR1 positions, also when logged
  in): use TAP on `dr1.mosaic_product` instead.
- **SIMBAD TAP** was down (capabilities 404) that night; `SkyCoord.from_name` (Sesame) worked.

## Catalogue contents (wide tile 102021980, VIS-detected sources)

- `dr1.mer_catalogue_wide_survey` has 478 columns; `dr1.mer_morphology_wide_survey` 113; joins on `object_id`.
- **Disk+Sersic (bulge/disc) columns exist but are empty in DR1**: `flux_*_disk_sersic`,
  `sersic_fract_*_disk_sersic` (catalogue) and `disk_sersic_*` (morphology) are 100% NaN (`disk_sersic_flags = 0`).
- `t_type` (Dominguez Sanchez+2022 regression) is NaN for all; Zoobot vote fractions (`smooth_or_featured_*`, `bar_*`,
  `has_spiral_arms_*`, `disk_edge_on_*`, `merging_*`, `ring_*`, `dwarf_*`, ...) are filled for ~38% of VIS-detected
  sources brighter than I_E = 22.5 (Zoobot subsample: I_E < 21 or segmentation area > 700 px).
- Single-Sersic morphology columns: `sersic_sersic_vis_radius` (arcsec; median 0.59" for I_E < 22.5),
  `sersic_sersic_vis_index` (range 0.3-8.0; pile-up at the n = 8 limit), `sersic_sersic_vis_axis_ratio`,
  `sersic_sersic_nir_*`, `sersic_visnir_flags` (bit 7 = 128 "small step" set for essentially all fits: a levmar
  stopping criterion, informational).
- `flux_radius` is in pixels (0.1"): median 4.4 px for I_E < 22.5. `semimajor_axis` and `kron_radius` are in pixels.
- **`phz_classification`: 1 = star, 2 = galaxy** (verified: class 1 median `point_like_prob` = 0.98, class 2 = 0.00).
  The TAP column description ("+1 galaxy, +2 star") is swapped; the DPDD is correct. 3 = star+galaxy ambiguity,
  0 = unclassified.
- `phz_70_int`, `phz_90_int`, `phz_95_int` are 2-element arrays (lower, upper); `phz_pdf` is a 601-element vector
  (z = 0-6, step 0.01).
- Large nearby galaxies are **shredded**: NGC 1483 (D ~ 2') appears as 6 large deblended entries of one parent out to
  50" (brightest I_E = 12.8 Kron), and its faint outer disc (40"-70") produces 760 entries where the field density
  (123.4 per arcmin^2, measured at 200"-420" in the 7.2' wide cone) predicts 356. (Corrected 2026-11-13: an earlier
  count said 5 entries and ~420 expected.) Flag statistics in [../06](../06_catalogues_photometry_morphology.md) §10.1.
- Source density far from bright objects: ~120 per arcmin^2 (VIS+NIR detections), consistent with the 116 arcmin^-2
  median quoted for the EWS.
- `phys_param_flags = 1` for 251 of 256 galaxies with I_E < 18 in tile 102021980 (bright galaxies are flagged); `phz_flags` takes decimal codes 0, 1, 10, 11, 12; `phz_classification` takes -1, 0, 1, 2, 3 (checked by the KB-synthesis agent, see [07](../07_photoz_physical_parameters.md)).

## Added 2026-11-13 (second session: fragments, ICL inputs, footprint, HATS)

- **Empty reliability columns**: `blended_prob`, `extended_prob` (100% NULL), `extended_flag`, `she_flag` (NULL; astropy
  shows the masked filler 16959) in tile 102021980 and in the NGC 1483 wide and deep cones. `point_like_prob` is NaN
  for NIR-only sources and for the bright (I_E < 16.5) entries; `mumax_minus_mag` is filled (stars ~ -3).
- **`parent_id`** is a tile-local detection number (e.g. 3423), -1 for non-deblended sources, -2 only for NIR-only
  sources (1709 in the tile). `deblended_flag = 1` exactly when `parent_id != -1`; `DET_QUALITY_FLAG` bit 2 is a
  subset (98.5% agreement). NGC 1483 = 6 children of parent 3423 (wide) and 38 children of parent 3090 (deep tile
  101287204).
- **Fragment statistics** (demo 07): see [../06_catalogues_photometry_morphology.md](../06_catalogues_photometry_morphology.md) section 10.1.
- **Calibrated/raw/SIR frames** (public, anonymous HTTP 200 with `release=dr1`): `dr1.calibrated_frame` VIS 42,092
  (R1), NISP 66,723 (R1) + 4936 (R2); `dr1.aux_calibrated` VIS `BKG`/`WGT`/`PSF MODEL`/`QUALITY_PARAMETERS` 42,092 each,
  NISP `BKG`/`PSF`/`PSF MODEL`/`PSF SINGLE STORAGE`(`MODEL`) 71,659 each; `dr1.sir_science_frame` 26,581
  (`EUC_SIR_W-SCIFRM_BKGSUB_*`); `dr1.raw_frame` 201,082 rows (`EUC_LE1_VIS-*`, `EUC_LE1_NISP-*`).
  `GROUP BY` or `TOP` queries on `dr1.raw_frame` with some columns return HTTP 500; selecting `file_name` works.
- **NIR calibrated frame** `EUC_NIR_W-CAL-IMAGE_H-2683-0_*.fits`: 799 MB, 49 HDUs `DETij.SCI/RMS/DQ`, `BUNIT =
  ELECTRON`, sky ~65 e- not subtracted, `ZPAB` per detector, primary `MJD-OBS`, `EXPTIME`, `OBS_ID`, `DITHOBS`,
  `PTGID`; BZERO/BSCALE present (open with `memmap=False`). `EUC_NIR_W-CAL-IMAGE-BKG_H-*`: 799 MB, same layout,
  NoiseChisel model ~63 e-. DQ bit 13 (PERSIST) set on 4.6-5.7% of pixels (DET11/14/44). Download ~3 MB/s.
- **Q1 ICL test cluster MCXC J1754.6+6803** (268.665, +68.056): 13 DR1 observations within 0.4 deg (Q1: obs 2683
  only), 196 calibrated frames, 76 SIR science frames.
- **VMPZ footprint per tile** (`EUC_LE3_VMPZ-ID_HPFOOTPRINTMASK-102021980_*`): 8 files (bands), 0.24 MB each,
  `NSIDE 16384`, `NESTED`, `COORDSYS = 'celestial'`, 19,420 pixels = 0.2487 deg^2. No survey-wide VMPZ file exists;
  the 27,390 `HPEFFECTIVECOVERAGE-WL/-CL` files are also per tile (`TILEID` in the header). File names come from
  `dr1.files_table` (selecting `file_name_list` from `dr1.vmpz_*`/`basic_download_data` returns HTTP 500).
- **Tile-polygon MOC** (demo 08, order 13): wide 8975 tiles = 2235.4 deg^2; deep 1368 tiles (R1 + R2) = 86.9 deg^2.
- **IRSA HATS** (demo 06): MER wide = 888,152,165 rows = ESA row count; ESA rows all `data_set_release_part3 = 2`;
  identical `object_id`s and values in a 5' cone. Details in [../14_hats_lsdb_access.md](../14_hats_lsdb_access.md).
- **`SELECT *`** on `dr1.mer_catalogue_wide_survey` fails in astroquery (`calblock_id_list` char size): list columns.
- ESASky ("temporarily unavailable") and CDS vizcat HATS (timeout) could not be reached on 2026-11-13.
- **HTTP range requests** work on `sas-dd/data` (HTTP 206, `Accept-Ranges: bytes`; HEAD gives `Content-Length`).
  Each request costs several seconds of latency; a 50 MB range took 12-18 s (3-4 MB/s). The server closes reused
  keep-alive connections (use a fresh connection per request). Layouts: VIS `DET` = 17,280-byte primary +
  144 x (SCI, RMS, FLG) of 3 x 16,934,400 bytes (quadrants 2048 x 2066, `RA---TPV`, CRPIX at the quadrant centre)
  = 7,315,678,080 bytes; NIR `CAL` = 11,520-byte primary + 16 x 49,959,360 bytes (SCI header 8640 bytes, RMS/DQ 5760)
  = 799,361,280 bytes. VIS `BKG` and `WGT` = 2438.6 MB each; NIR `BKG` and SIR `SCIFRM_BKGSUB` = 799.3 MB each;
  VIS `QUALITY_PARAMETERS` is a 0.5 MB JSON.
- A 1' row-range cutout of `EUC_MER_BGMOD-VIS_TILE102021980` (46 MB, 26 s) is identical to the same region of the
  downloaded tile.
