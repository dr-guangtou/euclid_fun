# MER catalogue for galaxy work: tables, photometry, morphology, classification, flags

> **Key points**
>
> - The MER catalogue is split into **five data groups** (`wide_survey` 888 M rows, `wide_mode`, `deep_survey`, `deep_mode`, `deep_visits`); within a group the tables `mer_catalogue_*`, `mer_morphology_*`, `mer_cutouts_*` (and PHZ tables) join on **`object_id`**. A source seen in two groups (for example an EDF in a wide-like tile and in a deep tile) has two different `object_id`s.
> - **Total flux**: `FLUX_DETECTION_TOTAL` (Kron, I_E when `VIS_DET = 1`). Other bands: scale it by an aperture or template colour, or use `FLUX_<band>_SERSIC`. Validation (COSMOS, mostly compact galaxies): Sersic or aperture best in I_E, T-PHOT best in Y/J/H; median offsets -1.5 to +5.5 % (spec-z samples), up to +13 % for deep photo-z NIR model fits. **No validation exists for large nearby galaxies.**
> - **Bulge+disc (`DISK_SERSIC`) columns exist but are empty in DR1**; `t_type` is empty; single-Sersic `q` and `R_e` are usable to I_E ~ 24 (about 7 % and 16 % scatter vs HST) but **`n` is not** (pile-up at the limit n = 8).
> - **Large nearby galaxies are shredded** into many catalogue entries; in a measured case essentially all of them carry `DET_QUALITY_FLAG` bit 512 ("extended-object area"), so the popular cut `DET_QUALITY_FLAG < 4` throws the galaxy away. Re-measure such targets from the mosaic.
> - Known catalogue defects: T-PHOT bugs, SE++ Sersic "guesses" in partially covered tiles, FLUX_RADIUS limited to the segmentation, duplicates at tile borders, NaN instead of NULL, hidden coordinate epoch.

**Conventions.** Citations are `(Author+26, p. N)` with N the page numbers recorded in the paper summaries under `papers/`; `(DPDD)` = [dpdd_mer.md](data_model/dpdd_mer.md) and the DPDD pages it digests; `(TAP)` = the column dumps under [data_model/tap/](data_model/tap/README.md); `(verified)` = [verified_on_archive.md](data_model/verified_on_archive.md), which wins over everything else; `(measured)` = a check run for this note on 2026-11-13 against wide tile 102021980 (EDF-S, contains NGC 1483), i.e. a single-tile observation, not a survey statistic. Related notes: [10_low_surface_brightness.md](10_low_surface_brightness.md) (sky subtraction, LSB limits; not repeated here) and [09_masks_flags_coverage.md](09_masks_flags_coverage.md) (flag maps, masks, coverage).

---

## 1. Data groups, tables and joins

### 1.1 The five data groups (table suffix `<SUFFIX>`)

Row counts and descriptions are from the archive help page *Catalogues* (`eds_help/Catalogues.md`); they were not re-counted.

| Group (`<SUFFIX>`) | Content | MER rows |
|---|---|---|
| `wide_survey` | The Euclid Wide Survey proper (about 1900 deg2 in DR1) | 888,152,165 |
| `wide_mode` | Wide-like data **not** in the wide survey: self-calibration field (all visits), ecliptic survey, EMDS, other ancillary/calibration fields | 58,488,372 |
| `deep_survey` | The three Euclid Deep Fields (EDF-N, -F, -S) processed in deep mode (many visits stacked) | 51,820,952 |
| `deep_mode` | CDFS and COSMOS (inside EDF-F), deep mode | 4,719,299 |
| `deep_visits` | Individual visits of the three EDFs (EDF-N 11 visits, EDF-F 2, EDF-S 10) | 252,948,682 |

- Tile indices: wide tiles are 32' x 32' with 9-digit index `102...`; deep tiles are 17' x 17' with `101...` (Catalogues.md; [Kuemmel+26](papers/kuemmel.md), pp. 2-3). Special-object tiles (`1025...`) were defined but **not processed** (Kuemmel+26, p. 3).
- The help page does not say in which group the wide-like (single-visit-depth) catalogues of the EDFs/COSMOS live. Measured: tile 102021980 (EDF-S area, wide-like) is in `mer_catalogue_wide_survey`.
- For PHZ/SPE/SIR the groups are merged to **`wide`** (= wide_survey + wide_mode), **`deep`** (= deep_survey + deep_mode) and `deep_visits` (Catalogues.md). Join a MER `wide_*` table to `dr1.phz_*_wide`.
- Do not simply concatenate groups: the same sky can be in a wide-like tile and a deep tile (wide vs deep comparison: 96,704 of 114,810 wide objects matched in the deep list within 0.3"; [Kuemmel+26](papers/kuemmel.md), p. 11), each with its own `object_id`. In `deep_visits` an object normally gets a different `object_id` per visit but "by chance" can get the same one (Catalogues.md).

### 1.2 Table families

| Table | Columns (TAP) | DPDD file | Content |
|---|---|---|---|
| `dr1.mer_catalogue_<S>` | 478 (479 in `deep_survey`, `deep_mode`) | `EUC_MER_FINAL-CAT` (470) | positions, flags, all photometry families, detection-band shape. **Only table with `right_ascension`/`declination`** |
| `dr1.mer_morphology_<S>` | 113 (114) | `FINAL-MORPH-CAT` (106) | FLUX_RADIUS, CAS/Gini/M20, Sersic and Disk+Sersic fits, Zoobot, merger columns |
| `dr1.mer_cutouts_<S>` | 32 (33) | `FINAL-CUTOUTS-CAT` (25) | cutout and deblending-region corners (RA/Dec), semi-major/minor axes in **deg** |
| `dr1.mer_catalogue_<S>_photometry` | 721 | `FINAL-DEEP-PHOTO-CAT` (713) | **only `deep_survey` and `deep_mode`**: extra deep-field EXT bands (Subaru IA427..IA856, HSC, VISTA, UKIRT, IRAC, GALEX, extra MegaCam); same flux families as the main table (TAP) |

The extra TAP columns relative to the DPDD are metadata (`data_set_release`, `_part1..3`, `patch_id_list`, `calblock_id_list`, `basic_download_data_oid`, `designation`; `catalogue_oid` in the deep groups) (derived from the TAP dumps). Product-level (file) tables: `dr1.mer_final_catalogue` (one row per catalogue file, includes `xml_file_content`, `tile_index_list`), `dr1.mer_segmentation_map`, `dr1.mosaic_product`, `dr1.aux_mosaic` ([verified](data_model/verified_on_archive.md)). **There is no `FILLING_FACTOR` column** in any catalogue table (TAP); it lives in the overview FITS tables (see [09](09_masks_flags_coverage.md)).

### 1.3 Join keys

| Join | Key | Note |
|---|---|---|
| catalogue / morphology / cutouts / deep photometry / PHZ | `object_id` | `object_id` is indexed in `mer_catalogue`, `mer_morphology` and the PHZ tables, **not** in `mer_cutouts` or `*_photometry` (TAP "Indexed" column) |
| catalogue to PHZ | `object_id` (verified); product-level `dr1.phz_catalogue*` join on `tile_index = ANY(tile_index_list)` (help page *Other data products*) | |
| catalogue to tile products | `tile_index`; or `FLOOR(segmentation_map_id / 1e6)` | measured: no mismatch among the 112,244 rows of tile 102021980 |
| SIR spectra | `source_id` (= `object_id`) | |

Performance (measured): a cone search joined to two other tables without a `tile_index` restriction hit the sync-service timeout (HTTP 408 after about 100 s); the same query restricted to the tile ran in about 60 s, and a plain tile query in about 10 s. Filter on `tile_index` (or `object_id`) first.

---

## 2. Identifiers

| Identifier | Definition | Notes |
|---|---|---|
| `OBJECT_ID` | `sign(Dec) * ( int(RA*1e7) * 1e9 + int(abs(Dec)*1e7) )` (DPDD, eq. 10) | negative in the south; changes between data releases because positions change. Check (help page *Epoch of source coordinates*): `object_id = 2648676745562592022` has RA 264.8676745..., Dec +56.2592022..., matching the formula. The help page quotes a "3.6 mas" resolution; the formula gives 1e-7 deg = 0.36 mas (derived) |
| `SEGMENTATION_MAP_ID` | `TILE_INDEX * 10^6 + SOURCE_DETECTION_ID` (DPDD, eq. 12) | the pixel value in `EUC_MER_FINAL-SEGMAP`. Example: 102152525004780 belongs to tile 102152525. DPDD: -1 for sources outside the tile core; measured: no negative value in tile 102021980 |
| `TILE_INDEX` | tile of the source | 102... wide, 101... deep. Catalogue lists only sources of the tile *core* area (Romelli+26, p. 3-4) |
| `PARENT_ID`, `PARENT_VISNIR` | parent of a deblended object | same description in the DPDD and TAP. `PARENT_VISNIR` flags artificial VIS/NIR blends that touch without sky between them ([Romelli+26](papers/q1_romelli_mer.md), p. 8). Measured (tile 102021980): `-1` for 94,887 non-deblended sources (`DEBLENDED_FLAG = 0`), `-2` for 1,709 sources with `DEBLENDED_FLAG = 1` (**meaning undocumented**), positive for the other 15,648 |
| `GAIA_ID`, `GAIA_MATCH_QUALITY` | Gaia match (radius 0.3", epoch-propagated; Romelli+26, p. 14) | `GAIA_ID` is a **Gaia DR3** id (help page *Ambiguous Gaia identifier*) |
| `data_set_release*`, `patch_id_list`, `calblock_id_list` | provenance | `data_set_release_part3 = 2` is `DR1_R2` for wide tiles ([verified](data_model/verified_on_archive.md)) |

---

## 3. Detection: VIS versus NIR

- Detection runs independently on the **VIS** background-subtracted mosaic and on a **NIR stack** (weighted sum of Y+J+H); the lists are merged with **VIS priority**: NIR objects whose centre falls on a VIS segment are dropped, VIS segmentation pixels are never overwritten ([Romelli+26](papers/q1_romelli_mer.md), p. 7-8; DPDD).
- SE++ parameters (identical for wide and deep): Gaussian filter FWHM 2.4 px (VIS) / 5.0 px (NIR); S/N threshold per pixel 0.9 / 0.4; minimum area 10 px; core threshold 1.3 / 0.55 on 10 px ([Kuemmel+26](papers/kuemmel.md), p. 4). The extra **core-threshold** requirement lets the main threshold be low enough to follow bright galaxies to faint isophotes without breaking them into noise detections (Romelli+26, p. 6).
- `VIS_DET = 1`: detected on VIS; `= 0`: NIR-stack only. About 20 % of objects are NIR-only (Kuemmel+26, p. 11); measured 89,280 of 112,244 (79.5 %) VIS-detected in tile 102021980. In the wide catalogue **NIR-only detections are dominated by spurious sources** (false diffuse NIR detections, persistence, unmasked cosmics; Kuemmel+26, p. 11; [Gasparetto+26](papers/gasparetto.md), pp. 2, 7, 13).
- For `VIS_DET = 0` the "detection" fluxes and `FLUX_DETECTION_TOTAL` refer to the (non-physical) NIR stack; `POINT_LIKE_PROB` is NaN; use `MUMAX_MINUS_MAG` as the compactness indicator (DPDD).
- Everything measured *on the detection image* (Kron flux, `SEMIMAJOR_AXIS`, `ELLIPTICITY`, `POSITION_ANGLE`, `MU_MAX`, `SEGMENTATION_AREA`, `FLUX_SEGMENTATION`) is bounded by the segmentation, i.e. by the detection threshold on the background-subtracted mosaic (see [10](10_low_surface_brightness.md) for what the sky subtraction removes). Isophotal shapes are PSF-rounded: `q_iso` is on average 0.09 too round compared with the Sersic `q`, and `a_Sersic` is on average 0.08 dex larger than `SEMIMAJOR_AXIS` ([Dunn+26](papers/dunn.md), pp. 18-19).

---

## 4. Flux families

All fluxes are in microJy; `m_AB = 23.9 - 2.5 log10(F_uJy)` in every band (DPDD; MER Photometry Cookbook). Each `FLUX_*` has a `FLUXERR_*` twin; errors are noise-only (no systematics such as blending; Romelli+26, p. 10). The TAP descriptions of `FLUX_DETECTION_TOTAL`, `FLUXERR_DETECTION_TOTAL`, `FLUX_SEGMENTATION`, `FLUXERR_SEGMENTATION` are **shifted by one row** (for example `flux_detection_total` is described as "total flux error (Kron aperture)"); the Cookbook is unambiguous: `FLUX_DETECTION_TOTAL` is the Kron flux, `FLUX_SEGMENTATION` the segmented-pixel flux (TAP; DPDD).

| Family and columns | Bands | What it measures | Good for | Bad for / caveats |
|---|---|---|---|---|
| `FLUX_DETECTION_TOTAL` (Kron; SExtractor FLUX_AUTO analogue) | detection band: I_E if `VIS_DET=1`, NIR stack if 0 | flux in an ellipse of 2.5 Kron radii on the detection mosaic ([Romelli+26](papers/q1_romelli_mer.md), p. 9; Gasparetto+26, p. 7) | reference total I_E flux; independent of the PSF model and PSF normalisation ([Kuemmel+26](papers/kuemmel.md), p. 10); anchor for colour-scaled totals | NIR-stack value is non-physical; truncated in outskirts of extended objects; **no local sky subtraction** (sky errors go straight into the flux; Romelli+26, p. 9); inflated by under-deblending (section 6); reliability given by `DET_QUALITY_FLAG`. Whether `KRON_RADIUS` is R_Kron or 2.5 R_Kron is not stated (TAP: "major semi-axis of the elliptical aperture used") |
| `FLUX_SEGMENTATION` (SExtractor FLUX_ISO analogue) | detection band | sum in the segmented pixels | magnitude cuts that do not depend on the Kron aperture ([Dunn+26](papers/dunn.md), p. 17: I_E <= 24.5 as `FLUX_SEGMENTATION > ~0.575` uJy) | lower limit for extended objects |
| `FLUX_<band>_<n>FWHM_APER`, n = 1..4 | I_E, Y, J, H, NIR_STACK, 17 EXT (22 bands) | circular aperture, diameter n x FWHM of the **worst PSF** (usually an EXT band, about 1"), on PSF-matched cutouts, per source; the used FWHM is in column `FWHM` (arcsec) | **colours** (aperture colours across Euclid + ground bands) | not a total flux; apertures are a few arcsec (2 FWHM about 2"; Romelli+26, pp. 9, 16), so for large galaxies they sample the core only; faint wings of neighbours contaminate the aperture (Kuemmel+26, p. 4); fewer sources reach S/N > 3 (Gasparetto+26, p. 13); wrong worst-PSF assignment in partially covered EXT tiles (section 8); Y/J/H `2FWHM` columns suffer the NaN problem (section 8) |
| `FLUX_<band>_TEMPLFIT`, `FLUX_VIS_TO_<band>_TEMPLFIT` | Y, J, H + 17 EXT (20) | T-PHOT template fit using the I_E image as high-resolution template; the second column is the I_E flux degraded to the `<band>` resolution | NISP colours and totals, blends (best NISP method in Gasparetto+26, p. 7; Romelli+26, p. 10 prefers it for extended and blended objects) | **T-PHOT bugs** (section 8); direct total limited by segmentation area and PSF extent (Kuemmel+26, p. 4); no I_E T-PHOT flux (I_E is the template) |
| `FLUX_<band>_SERSIC` | I_E, Y, J, H + 17 EXT (21) | integrated flux of the single-Sersic model (SourceXtractor++); shape fixed to the VIS fit in EXT bands | model total that extrapolates beyond the segmentation; best I_E method for COSMOS galaxies (Gasparetto+26, p. 7) | meaningless where a single Sersic is wrong (bulge+disc, shredded objects); **not measured in uncovered areas of partial tiles** (section 8); uses the non-normalised 5" PSF stamp (factor S, section 5.3); fit-box limits for big objects (section 7) |
| `FLUX_<band>_DISK_SERSIC`, `SERSIC_FRACT_<band>_DISK_SERSIC` | 21 bands | two-component fit | nothing in DR1 | **100 % NaN in DR1** ([verified](data_model/verified_on_archive.md)) |
| `FLUX_VIS_PSF` | I_E only | PSF-fit flux | point sources | not for galaxies; offset about -0.13 mag vs Gaia partly due to the T-PHOT bug (Kuemmel+26, p. 8) |
| `AVG_TRANS_WAVE_<band>` | 21 bands | mean filter-transmission wavelength, Angstrom | rest-frame / colour-term work | |

Column counts per family in the TAP dump: 22 `FLAG_<band>`, 22 x 4 aperture fluxes (+ errors), 20 TEMPLFIT, 20 VIS_TO_TEMPLFIT, 21 SERSIC, 21 DISK_SERSIC (measured from the TAP dump of `mer_catalogue_wide_survey`).

### 4.1 Cookbook recipes (MER Photometry Cookbook; DPDD)

| Task | Recipe |
|---|---|
| Magnitude | `m_AB = 23.9 - 2.5 log10(flux_uJy)` |
| Colour, aperture | `H - g = -2.5 log10( FLUX_H_nFWHM_APER / FLUX_G_EXT_DECAM_nFWHM_APER )` (same n; PSF-matched) |
| Colour, template | `H - VIS = -2.5 log10( FLUX_H_TEMPLFIT / FLUX_VIS_TO_H_TEMPLFIT )` |
| Colour, model | `g - J = -2.5 log10( FLUX_G_EXT_DECAM_SERSIC / FLUX_J_SERSIC )` |
| Total flux in band B, aperture scaling | `F_B,tot = FLUX_DETECTION_TOTAL * FLUX_B_nFWHM_APER / FLUX_VIS_nFWHM_APER` (`VIS_DET=1`); denominator `FLUX_NIR_STACK_nFWHM_APER` if `VIS_DET=0` |
| Total flux, template scaling | `F_B,tot = FLUX_DETECTION_TOTAL * FLUX_B_TEMPLFIT / FLUX_VIS_TO_B_TEMPLFIT` ("TPHOT-color") |
| Total flux, direct | `FLUX_B_TEMPLFIT` (especially EXT bands) or `FLUX_B_SERSIC` |
| Aperture corrections | **none documented** for the 1-4 FWHM apertures; the colour scaling of the Kron flux is the only route to a total |

Choice among them: Gasparetto+26 find "TPHOT" and "TPHOT-color" differ by 1-2 % in COSMOS (p. 7), while Kong+ (in prep., quoted there) find larger differences in favour of TPHOT-color; Kuemmel+26 (practical recommendations) prefer colour-scaled Kron totals over direct T-PHOT totals.

### 4.2 PSF normalisation (DR1 change; Kuemmel+26, Sect. 4, pp. 9-10)

- MER PSF stamps are cut at 5", so their pixel sum `S` is below 1 (typical median `S`: I_E 0.957-0.961, Y/J/H 0.984-0.987, DECam 0.97-0.99, Pan-STARRS i 0.880; Table 4, tiles 102020534 and 102159192). Q1 renormalised the stamps to `S = 1` (up to ~10 % offsets in broad-PSF bands); **DR1 does not**.
- First-order relations between a Q1-style flux (n, normalised) and a DR1 flux (nn): A-PHOT/T-PHOT `F_nn(B) = F_n(B) / (S_nn(B) / S_nn(D))` with D the detection band; Sersic `F_nn(B) = F_n(B) / S_nn(B)`; VIS PSF-fit `F_nn(I_E) = F_n(I_E) / S_nn(I_E)`; `FLUX_DETECTION_TOTAL` does not depend on the PSF. Check the sign convention in Kuemmel+26 Eqs. 1-3 before use; this note only has the summary.
- `S` is **not a catalogue column** (TAP). It can be computed from the PSF stamps (`EUC_MER_CATALOG-PSF-<band>`, one stamp per catalogue object in NIR-H; [verified](data_model/verified_on_archive.md)) (inference, untested).
- The I_E normalisation (tile-to-tile and within-tile scatter of about 1 %) limits DR1 absolute photometry; I_E-based colours cancel it (Kuemmel+26, p. 10). The authors themselves note non-normalised PSFs are "not the best choice in all cases, e.g. large extended sources".

---

## 5. Photometry validation (what is and is not known)

### 5.1 COSMOS galaxies ([Gasparetto+26](papers/gasparetto.md), Table C.1, p. 25)

Median relative offset (MER - prediction)/prediction in percent, spec-z samples, wide | deep (limits: AB 25 wide / 27 deep in I_E, 24 / 25 in NIR; reference = SED prediction from COSMOS2025 Sersic fluxes):

| Band | SERSIC | APHOT | TPHOT |
|---|---|---|---|
| I_E | +3.3 \| +2.7 | +2.9 \| +3.8 | n/a |
| Y_E | +3.6 \| +4.9 | +3.1 \| +4.2 | -0.2 \| +3.0 |
| J_E | +3.0 \| +4.2 | +1.4 \| +3.1 | -1.5 \| +2.1 |
| H_E | +5.5 \| +5.4 | +2.9 \| +3.7 | +0.6 \| +3.2 |

- Photo-z samples give larger deep NIR offsets (SERSIC +12.9 % Y_E, +11.6 % J_E, +11.6 % H_E), "all other cases well within 10 %" (abstract; Table C.1).
- **Which method per band**: I_E, SERSIC or APHOT (comparable; SERSIC slightly lower in deep); Y/J/H, TPHOT (almost no trend to AB 24 in wide); avoid APHOT for `DEBLENDED_FLAG = 1` and at low S/N; do not trust fluxes within 1-2 mag of the detection limit (Eddington-like bias, starts about 2 mag brighter in wide than in deep); use `VIS_DET = 1` (Gasparetto+26, pp. 7-13).
- The reference is itself model-based and appears to underestimate HSC fluxes by 3-5 %, so part of the positive offsets may be an artefact; the sign is opposite to the Gaia-star validation (NIR offsets -0.036 to -0.126 mag; [Kuemmel+26](papers/kuemmel.md), p. 8). I_E offset vs Gaia about -0.02 mag. Relative-photometry NMAD (Gaia stars): I_E 15 mmag, Y/J/H 35/40/47 mmag (Kuemmel+26, Table 3, p. 9).
- Source injection (Cornifer): recovery within 5 % (Kuemmel+26, p. 8).
- The sample is bright, mostly compact-to-moderate galaxies; **no dependence on size, Sersic index or morphology was tested**, so treat these offsets as a lower bound for large nearby galaxies (Gasparetto+26, p. 15 and implications).

### 5.2 Deblending inflation for bright, large galaxies

- Deep tiles: bright, large galaxies with extended haloes that are blended with a neighbour in the deep data but not in the wide data are **under-deblended**; their segmentation includes neighbour pixels and the **flux is overestimated** (Gasparetto+26, pp. 8-9; example C25 ID 686933 fixed by a reprocessing with a new ASTErIsM configuration, p. 14). About 40 % of deep spec-z matches have `DEBLENDED_FLAG = 1` (about 20 % for the photo-z sample); offsets of deblended objects are larger, strongly method-dependent, largest for APHOT (pp. 9-13).
- Wide tiles: **over-deblending** (Kuemmel+26, p. 11). Same SE++/ASTErIsM parameters for wide and deep; per-depth tuning is a DR2 topic.
- Wide vs deep photometry otherwise agrees to <= 0.01 mag over a large dynamic range (Kuemmel+26, p. 12).

---

## 6. Morphology columns (`dr1.mer_morphology_<S>`)

| Group | Columns | Status and reliability |
|---|---|---|
| Size | `FLUX_RADIUS` (+`_ERR`) | **pixels** (0.1"); median 4.4 px for I_E < 22.5 ([verified](data_model/verified_on_archive.md)). SExtractor-like radius containing 50 % of the flux in a disc of 6 a_M, 64 annuli ([Kuemmel+26](papers/kuemmel.md), pp. 4-5). **Bug**: DR1 limited the flux sum strictly to the segmentation area (section 8) |
| Single Sersic, VIS+NIR joint fit | `SERSIC_SERSIC_VIS_{RADIUS,AXIS_RATIO,INDEX}` (+`_ERR`), same with `NIR`, `SERSIC_ANGLE`, `SERSIC_VISNIR_{REDUCED_CHI2,ITERATIONS,FLAGS,DURATION}` | radius in arcsec; DPDD says only "Sersic radius", [Dunn+26](papers/dunn.md) (p. 3) treat it as the effective semi-major axis. I_E shape is fitted separately from the NIR shape, common position angle (Romelli+26, p. 12). Median 0.59" (I_E < 22.5); index range 0.3-8.0 with a **pile-up at the n = 8 limit** ([verified](data_model/verified_on_archive.md)). Flags: section 7.3 |
| Single Sersic, EXT | `SERSIC_EXT_*` | VIS shape held fixed, fluxes only |
| Disk+Sersic | `DISK_SERSIC_*` | **empty in DR1** (all NaN, `disk_sersic_flags = 0`; verified). Bulge/disc decompositions must be done by the user |
| CAS, Gini, M20 | `CONCENTRATION`, `ASYMMETRY`, `SMOOTHNESS`, `GINI`, `MOMENT_20` (+`_ERR`) | VIS-detected sources, measured in the segmentation cutout (Conselice 2003, Lotz+2004; DPDD). DR1 fix: noise measured locally, because Q1 asymmetry was biased low in tiles with low `FILLING_FACTOR` (Kuemmel+26, p. 5); redo Q1-based analyses. Because they use the segmentation area they inherit its limits (and shredding, section 10). No DR1-specific validation of CAS/Gini/M20 is in the summaries |
| Zoobot | `SMOOTH_OR_FEATURED_*`, `BAR_*`, `BULGE_SIZE_*`, `HAS_SPIRAL_ARMS_*`, `SPIRAL_ARM_COUNT_*`, `SPIRAL_WINDING_*`, `DISK_EDGE_ON_*`, `EDGE_ON_BULGE_*`, `LOPSIDED_*`, `HOW_ROUNDED_*`, `MERGING_*`, `RING_*`, `DWARF_*`, `PECULIAR_*`, `AGN_*`, `CLUMP_COUNT_*` | Dirichlet concentrations; convert to a fraction with `answer / sum of answers to the same question`, e.g. `SMOOTH_OR_FEATURED_SMOOTH / (SMOOTH + FEATURED_OR_DISK + ARTIFACT_STAR_ZOOM)` (Morphology Cookbook). Filled only for a subsample: DR1 **I_E < 21 or segmentation area > 700 px** (Kuemmel+26, p. 6), about 38 % of VIS-detected sources brighter than I_E = 22.5 in the test tile (verified). The DPDD still says VIS < 20.5 or area > 1200 px (about 2 % of sources); trust the paper and the measurement |
| Other ML | `ETG_OR_LTG`, `T_TYPE`, `MAJOR_MERGER` (+`_UNCERTAINTY`), `MAJOR_MERGER_STAGE` (+`_PROBABILITY`, `_UNCERTAINTY`) | **`T_TYPE` is empty** (verified). Fill status of `ETG_OR_LTG` and the merger columns was not checked |

### 6.1 Reliability of the Sersic fits

| Test | Result |
|---|---|
| Wide (single visit) vs deep, same sources, I_E < 23.5 ([Kuemmel+26](papers/kuemmel.md), p. 12, 56,194 valid galaxies, 48,641 with fits in both) | `R_e`: median relative difference < 1 %, 68 % within +-10 %; `q`: median difference < 0.012 (< 0.005 for I_E < 23.5); `n`: slightly higher in wide for the brightest bins (6.4 % and 2.6 % median difference), scatter grows quickly with magnitude. Poor fits removed: 6.1 % for I_E < 23, 13.4 % at all magnitudes. Sersic parameters robust to depth at least to I_E ~ 23 |
| Wide-depth DR1 vs HST ACS-GC (F606W, GEMS), I_E <= 24.5 ([Dunn+26](papers/dunn.md), App. B, pp. 17-18) | `R_e` dispersion < ~10 % at I_E < 23 rising to ~16 % at 24.0-24.5, bias about +7 % at the faint limit; `q` dispersion < ~3 % rising to ~7 %, bias < ~2 %; **`n` by far worst (dispersion ~0.57 at I_E = 24.5)** |
| Sersic vs isophotal (Dunn+26, pp. 18-19) | median log10(a_Sersic / a_iso) = 0.081 dex (scatter 0.074); `q_Sersic - q_iso` = -0.093 (scatter 0.091) |

Caveats: single-Sersic `q` follows the disc only for face-on or B/T <~ 0.1 systems; blends, mergers and close pairs fitted as one galaxy give anomalous `q` and size (Dunn+26, p. 11). Dunn+26 do not cut on the `n` error and recommend not using `n` for individual objects. Because a single Sersic is a flux-weighted compromise, **bulge+disc and LSB outskirts need your own 2-D fit** on the mosaic (Kuemmel+26, implications).

### 6.2 Morphology Cookbook advice (DPDD) and DR1 paper advice

- Prefer I_E < 23 for morphology (Euclid Morphology Challenge limit; Kuemmel+26, p. 12). Cuts used by Dunn+26 (App. A, p. 17) for DR1 single-Sersic work: `VIS_DET=1`, `SPURIOUS_FLAG=0`, `DET_QUALITY_FLAG < 4`, `POINT_LIKE_PROB <= 0.1`, `0.01 a < R_e < 20 a` (a = isophotal semi-major axis in VIS pixels), `0.302 < n < 5.45`, `0.05 < q < 1`, fractional errors of `R_e` and `q` < 10 %, `R_e > 0.16"`. (Their `n < 5.45` is the Q1 convention; DR1 allows up to 8.)
- Sersic flag use: require the **error bits (0, 4, 9, 12)** clear and consider bits 5 and 1 (downsampled or resized fit box, typical for big objects); treat `n` close to 8 as not converged (Kuemmel+26, practical recommendations). Do **not** require `SERSIC_VISNIR_FLAGS == 0`: bit 7 is set for essentially all fits ([verified](data_model/verified_on_archive.md); measured: every one of the 10 sources of the clean query in section 11 has bit 7 set).

---

## 7. Classification and quality flags

### 7.1 Star/galaxy and spurious

| Quantity | Definition and use |
|---|---|
| `POINT_LIKE_PROB` | probability of being point-like from `MU_MAX - MAG_AUTO` (column `MAG_STARGAL_SEP`) calibrated on simulations; **VIS-detected only (NaN for NIR-only)**; "heavily biased towards high purity, low completeness" (Morphology Cookbook). There is **no `MAG_AUTO` column**; `MAG_STARGAL_SEP` is the magnitude used (TAP) |
| `POINT_LIKE_FLAG` | 1 if `POINT_LIKE_PROB > 0.96` and `DET_QUALITY_FLAG = 0`, otherwise NaN (TAP; DPDD). 0.96 gives 99 % star purity in the SC8 simulation ([Kuemmel+26](papers/kuemmel.md), p. 6). Star rule of thumb: I_E < 17 (even if saturated) or `POINT_LIKE_PROB > 0.96`; add PHZ for completeness |
| galaxy cut | `POINT_LIKE_PROB <= 0.1` ([Dunn+26](papers/dunn.md)); for the opposite use (stars) a loose `> 0.05` plus a colour polygon was used by Gatto+26 (see [10](10_low_surface_brightness.md), section 9). Both are analysis choices, not Euclid recommendations |
| `PHZ_CLASSIFICATION` (tables `dr1.phz_photo_z_wide`, `dr1.phz_classification_wide`) | **1 = star, 2 = galaxy**, 4 = QSO, 8 = globular cluster (DPDD); **the TAP description ("+1 galaxy, +2 star") is swapped**, verified: class 1 median `point_like_prob` 0.98, class 2 0.00 ([verified](data_model/verified_on_archive.md)). Bit-coded, so composites (3, 6, ...) exist; `= 2` selects clean galaxies |
| `SPURIOUS_PROB`, `SPURIOUS_FLAG` | random-forest classifier trained on 430,000 simulated sources with 26 features (Romelli+26, p. 14). Q1 default threshold 0.5 (recovers 90 % of true spurious, loses 0.13 % of real; 0.75 gives 80 % / 0.04 %); **DR1 advice: 0.7, because 0.5 is too aggressive** (Kuemmel+26, p. 6). Trained on wide-like simulations only (no deep-like training set). Around a large galaxy only a minority of the fragments have `SPURIOUS_PROB > 0.7` (NGC 1483: 125 of 721 entries within 70" of its centre; 23% of the field-corrected fragment excess, section 10.1) |
| `EXTENDED_PROB/FLAG`, `BLENDED_PROB`, `SHE_FLAG`, `VARIABLE_FLAG`, `BINARY_FLAG` | present in TAP; **bit/threshold semantics are not documented** (DPDD); treat as 0/1 flags or probabilities. `SHE_FLAG`: objects SHE may want to remove (e.g. bright stars); SHE itself is not part of DR1-Foundation |

### 7.2 `DET_QUALITY_FLAG` and `FLAG_<band>`

`DET_QUALITY_FLAG` says whether `FLUX_DETECTION_TOTAL` and `MAG_STARGAL_SEP` may be corrupted (MER Photometry Cookbook; "Bit set" is 1-based, the integer is the value to test with `&`). The last column is measured: share of the 112,244 sources of tile 102021980 with the bit set (the 39 most frequent distinct values, covering 112,241 rows, were tallied; combinations are possible).

| Bit set | Value | Meaning (DPDD) | Measured share |
|---|---|---|---|
| 1 | 1 | contaminated by close neighbours or bad pixels | 0.25 % |
| 2 | 2 | blended with another source (must comply with `PARENT_ID != -1`) | 13.9 % |
| 3 | 4 | saturated | 0.19 % |
| 4 | 8 | close to a border | < 0.01 % |
| 5-7 | 16, 32, 64 | **not documented** | not observed |
| 8 | 128 | inside the VIS bright-star mask | 2.0 % |
| 9 | 256 | inside the NIR bright-star mask | 1.2 % |
| 10 | 512 | inside an extended-object area | 5.2 % |
| 11 | 1024 | skipped by the deblending algorithm (large pixel size) | 2 rows |

- 92.4 % of the sources have `DET_QUALITY_FLAG < 4`; 80.6 % have `= 0` (measured, same tile).
- The measured share of bit 2 (15,648 sources, 13.9 %) equals the number of sources with a positive `PARENT_ID`; the 1,709 sources with `PARENT_ID = -2` and `DEBLENDED_FLAG = 1` do not have bit 2 set.
- `DET_QUALITY_FLAG` carries more than the single-band `FLAG_<band>` (22 bands: I_E, Y, J, H, NIR_STACK, 17 EXT), which use only bits 1-4 (contaminated or bad pixels, blended, saturated, close to border) and "keep track of the flagged pixels in the `<band>` flag image" (Cookbook; TAP).
- **Choosing a cut.** Dunn+26 and Nersesian+26 use `< 4` (keeps bits 1-2, removes saturated, border, both star-mask bits, extended-object area, skipped-by-deblender). Strict `= 0` is what `POINT_LIKE_FLAG` uses. For nearby extended galaxies see section 10: bit 512 is the *normal* state of entries in their area.

### 7.3 Sersic flags (`SERSIC_VISNIR_FLAGS`, `SERSIC_EXT_FLAGS`)

Combined SourceXtractor++ and Levmar stop-reason bits; here the Cookbook "Bit set" is **0-based** (DPDD; [Kuemmel+26](papers/kuemmel.md), Table 2, p. 5). `DISK_SERSIC_FLAGS` bits are not separately documented.

| Bit | Value | Meaning | Bit | Value | Meaning |
|---|---|---|---|---|---|
| 0 | 1 | error flag (levmar) | 7 | 128 | small step (informational; set for essentially all fits) |
| 1 | 2 | size correction (fitting box manually resized) | 8 | 256 | maximum iterations |
| 2 | 4 | outside the measurement frame (no fit run) | 9 | 512 | singular matrix (raises the error flag) |
| 3 | 8 | insufficient data (no fit run) | 10 | 1024 | no further error reduction possible |
| 4 | 16 | some or all parameters could not be fitted | 11 | "2028" | small residual |
| 5 | 32 | fit done on a downsampled image (maximum size exceeded) | 12 | "4056" | invalid (NaN/Inf) model values (raises the error flag) |
| 6 | 64 | small gradient | | | |

The printed values "2028" and "4056" are almost certainly typos for 2048 and 4096 (derived). Measured: the main NGC 1483 entry has `SERSIC_VISNIR_FLAGS = 160` (= 128 + 32, i.e. fitted on a downsampled image).

### 7.4 Other

- `DEBLENDED_FLAG`: object was originally blended and split by ASTErIsM (DPDD; Gasparetto+26, p. 7). Use `DEBLENDED_FLAG = 0` for clean photometry.
- `BLENDED_PROB`: probability of being blended; no documented threshold.
- `FILLING_FACTOR`, `ASTROMETRY_*_OFFSET` are tile-level quantities, not catalogue columns here (see [09](09_masks_flags_coverage.md)).

---

## 8. Known catalogue issues

Sources: Explanatory Supplement 15.3 (`expsup/Ch15.S3.*`) and archive help pages (`eds_help/`), all dated 12 Nov 2026 unless stated.

| Issue | Effect | What to do |
|---|---|---|
| **T-PHOT bugs** (Expsup 15.3.2) | (i) PSF-fitting re-centring applied in the wrong direction; (ii) PSF-homogenisation (numpy order) and photometry (FITS order) transposed rows and columns, affecting **all** template-fitting runs. Effect "not dramatic on galaxies" because the central PSF is sharp and round; mainly point sources. Gaia-star A-PHOT/T-PHOT differences in NISP vanish after correction. [Kuemmel+26](papers/kuemmel.md) (p. 8) says the bug was found after DR1 processing, Expsup says during; DR1 catalogue values are uncorrected | do not use `FLUX_VIS_PSF` or T-PHOT for bright point-like sources; for galaxies treat T-PHOT NIR fluxes with a small systematic in mind |
| **SE++ "guesses" in partially covered tiles** (Expsup 15.3.3) | for sources in an area missing in a band, SE++ does not fit but outputs (mostly) its input guess, so `FLUX_<band>_SERSIC` and `SERSIC_*` are **not measured** values. Found after DR1 processing | Helpdesk tool `bad_objects.py --tiles <ID>` (request via euclid-helpdesk@cosmos.esa.int with subject "Bad MER catalog Sersic fitting results"; the tool reads the local DR1 data store, i.e. Datalabs) writes cleaned copies of the catalogue, morphology and deep-photometry files. A source is bad in a band if flux is NaN or its error is 0/NaN; if `log10(FLUXERR)` is outside [-5, 5]; or if the Sersic flux equals the detection flux to <= 1e-6 fractionally. You can apply the same three tests in ADQL/pandas yourself (inference) |
| **Worst-PSF assignment** (Expsup 15.3.4) | in a few partially covered tiles (example tile 10183462, HSC r) sources in uncovered EXT regions got the low-resolution PSF of that band: aperture photometry used too-large apertures, more noise | check the `FWHM` column for a patchy spatial pattern |
| **FLUX_RADIUS** (Expsup 15.3.5) | DR1 version limits the flux sum strictly to the segmentation area (SE2/SE++ do not), so `FLUX_RADIUS` is biased low and compressed; point-source spike near 1.1 px drifts lower at faint magnitudes; fixed post-DR1 | treat as a lower limit; prefer `SERSIC_SERSIC_VIS_RADIUS` or your own growth curve. (Kuemmel+26 p. 4-5 describes the intended 6 a_M disc; the Supplement describes what DR1 did) |
| **Duplicates at tile borders** (Expsup 15.3.7) | the inner-area test is made on the parent cluster before deblending, so a border source can be in both tiles; duplicate fraction 1e-5 of all sources; three kinds by `DEBLENDED_FLAG` (0/0, 1/1, 0/1); DR2 will select per object | de-duplicate by sky position across neighbouring `tile_index` values for targets on tile borders |
| **NaN instead of NULL** (help pages, 2025-03 and 2026-11-12) | `IS NOT NULL` does not work; empty values are NaN (also `-99` in some spectro tables). Affects at least `point_like_prob` and `flux[err]_{y,j,h}_2fwhm_aper` | `WHERE NULLIF(col, 'NaN') > 0`. The help page's example table `dr1.mer_catalogue_deep` does not exist; use `..._deep_survey` or `..._deep_mode` |
| **Coordinate epoch hidden** (help page) | `right_ascension`/`declination` are ICRS (Gaia-CRF3); the epoch is not in the table and varies from tile to tile (example: J2024.632 for tile 102152525). FITS keyword `EQUINOX` is meaningless | read `ReferenceObservationDateTime` from the tile XML (`dr1.mer_final_catalogue.xml_file_content`) or `REFERENCE_TIME` in the overview FITS ([09](09_masks_flags_coverage.md)); irrelevant for galaxies, relevant for Gaia cross-matches |
| **Ambiguous `gaia_id`** | means Gaia DR3 | |
| **Column mismatches DPDD vs archive** (help pages) | PHZ and SPE columns listed in the DPDD but absent from the archive, and archive columns without DPDD description | check the TAP dump first |
| **FLUX_* descriptions rotated** (DPDD and TAP) | see section 4 | |
| **`FWHM`, `*_FWHM_APER` have no unit or description in TAP** | the `FWHM` unit is arcsec (Cookbook) | |
| **Target inside the mosaic `fov` but outside the real field of view** (help page) | `dr1.mosaic_product.fov` can be inexact | confirm with a cutout or a MER cone search |

---

## 9. Special notes on the pipeline relevant to extended sources

- **Fitting limits** (Morphology Cookbook): objects whose segmentation implies a fitting area above 300 x 300 px had their fitting box reduced to **50 x 50 px** (to spare saturated stars); a later modification, tuned on Q1, exempts large galaxies; DR1 uses `DET_QUALITY_FLAG` to cap the area of saturated stars only (Kuemmel+26, p. 5). All objects descended from one parent are fitted jointly (at most 150 per group). Expect `SERSIC_*_FLAGS` bits 1 (size correction) and 5 (downsampled) on big objects.
- **PSF**: the Sersic model is convolved with the MER propagated PSF (non-normalised, stamp <= 5"); propagated PSFs are 30-35 % wider than the input PSFs because of bilinear resampling and stacking (Romelli+26, p. 8). The PSF wings beyond 5" are not modelled.
- **Sky**: aperture, Kron and Sersic fluxes are measured on a mosaic that went through two background subtractions with no local sky correction; see [10](10_low_surface_brightness.md).

---

## 10. How large nearby galaxies are represented

- **Special-object scheme**: 164,526 objects larger than 2' (HyperLEDA, HECATE, EDD, SIMBAD, RC3, UNGC, plus Galactic globular clusters) each get a dedicated large tile (index `1025...`, bounding box 4 x the isophotal diameter, 2'-120'). **None was processed in DR1** ([Kuemmel+26](papers/kuemmel.md), p. 3). In Q1 the home tile was enlarged instead (example: tile 102158273 stretched to 33' to contain PGC 61126; [Romelli+26](papers/q1_romelli_mer.md), p. 5). In DR1 the same tile's wide-survey mosaic was all zeros at PGC 61126 although the `fov` polygon contained it; use the deep stack there ([verified](data_model/verified_on_archive.md)).
- **Shredding** (verified): NGC 1483 (D ~ 2') appears as 6 large deblended entries sharing one `PARENT_ID` (I_E Kron 12.8-18.7, out to 50"), and its faint outer disc yields hundreds of extra entries (measured excess in section 10.1). No statistics on fragmentation of large galaxies are given in the papers (Romelli+26, Kuemmel+26).
- **Measured, same galaxy** (721 entries within 70" of RA 58.198, Dec -47.476, tile 102021980): 507 have `DET_QUALITY_FLAG = 512`, 210 have 514, 1 has 513, 2 have 515, 1 has 899. So the **extended-object-area bit (512) is set for practically the whole shredded area**, and `DET_QUALITY_FLAG < 4` removes them all. A variant that tolerates bit 512 is in section 11. Among the five brightest fragments passing the section 11 variant, all have `PHZ_CLASSIFICATION = 2`, photo-z 0.05-0.33 (0.07 with `PHZ_FLAGS = 1` for the brightest), and Sersic radii of 17-19" with `n` 0.47-0.79 for the three brightest but 92-117" with `n` ~3 for the next two: **the per-fragment Sersic and Kron values are not physical measurements of the galaxy** (measured).
- Consequences: for any target with D >~ 30" do not use catalogue photometry or Sersic parameters; define the galaxy region yourself, sum or re-fit on the mosaic with the MER PSF and your own masks and sky ([10](10_low_surface_brightness.md)). Use the segmentation map (`SEGMENTATION_MAP_ID`) and the `FLAG` map to mask neighbours.
- Large galaxies near a tile border may be cut; the wide tiles overlap by 2' (Romelli+26, p. 3-5); mosaic the neighbours yourself and remove duplicate catalogue entries (section 8).
- In the VMPZ HEALPix products, SGA galaxies with MAG_LEDA < 16.5 are deliberately masked out of the effective coverage ([Odier+26](papers/odier.md); see [09](09_masks_flags_coverage.md)).

### 10.1 Can catalogue columns tell a fragment from a real source? (measured, `demo/07_fragment_flags.py`)

**Short answer: no single column does.** There is no "fragment" flag. The columns that could carry this
information are partly empty in DR1, and the ones that are filled flag fragments only statistically, at the cost of
also removing many real field sources.

Method: ESA TAP cones of 7.2' around NGC 1483 in the wide (DR1_R2) and deep (EDF-S, DR1_R1) catalogues. Entry density
versus radius is normalised to the field density at 200"-420". The excess inside 40"-100" is the fragment population.
It is a lower limit, because the disc also hides some real background sources. For each column we then compare the
fraction of the excess it flags with the fraction of field sources it flags. Figure: `figures/dr1_fragment_flags.png`;
numbers: `figures/dr1_fragment_flags.json`.

| Survey | Main pieces (one `PARENT_ID`) | Entries in 40"-100" | Expected real | Excess (fragments) |
|---|---|---|---|---|
| wide | 6 (I_E 12.8-18.7, out to 50") | 1432 | 907 | 525 (+58%) |
| deep | 38 (out to 75") | 2911 | 1667 | 1244 (+75%) |

The density ratio peaks at 2.5-3 just outside the main pieces (55"-70" wide, 60"-80" deep). It returns to 1 at
~100" (wide) and ~140" (deep), so the deeper stack shreds a larger area.

| Indicator | Field sources flagged (wide / deep) | Fragment excess flagged (wide / deep) | Verdict |
|---|---|---|---|
| `SPURIOUS_PROB > 0.7` | 2.6% / 2.5% | 23% / 25% | cheap and safe, but catches only a quarter |
| `SPURIOUS_FLAG` (prob > 0.5) | 4.7% / 7.3% | 32% / 45% | |
| NIR-only (`VIS_DET = 0`) | 22% / 11% | 57% / 24% | most wide-survey fragments are NIR-only detections on the disc |
| `DEBLENDED_FLAG = 1` (equivalently `PARENT_ID != -1`; DQ bit 2 is a subset) | 15% / 18% | 34% / 41% | weak: ~78% of wide fragments are independent detections, not deblended children |
| `SPURIOUS_PROB > 0.7` or NIR-only | 24% / 13% | 76% / 49% | the best simple cut, but costs a quarter of real wide-survey sources; ~125 excess entries remain (wide) |
| `DET_QUALITY_FLAG` bit 512 | 0% | 100% of all entries inside the area | marks the **region** (real and fake alike), not the fragment |

Columns that exist but are **100% NULL** in DR1 (tile 102021980 and both cones): `BLENDED_PROB`,
`EXTENDED_PROB`, `EXTENDED_FLAG`, `SHE_FLAG`. `POINT_LIKE_PROB` is NaN for NIR-only sources and for the bright
(I_E < 16.5) entries. For those, use `MUMAX_MINUS_MAG`: stars sit at about -3, galaxies above about -2.

**What the catalogue does give you:**
1. **`PARENT_ID` families reassemble a deblended galaxy.** All children of one parent share `PARENT_ID`, a detection
   number that is **local to each tile**: always match on (`tile_index`, `parent_id`). Summing their fluxes recovers the
   deblended body (6 pieces wide, 38 deep for NGC 1483). It does not recover the outer-disc fragments, which have
   `PARENT_ID = -1`. `PARENT_ID = -2` occurs only for NIR-only sources (1709 in the tile).
2. **Bit 512 delineates the affected area.** Treat every entry with bit 512 as unreliable for counts and colours,
   and measure the galaxy itself on the image.
3. **A family can also be an artefact.** In tile 102021980 the second-"largest galaxy" family (17 entries, summed
   segmentation area equivalent to r = 78") is pieces of a saturated star's halo plus a rectangular detector artefact
   (RA 57.980, Dec -47.342).

**Recommendation for environments of large galaxies** (satellite counts, colour profiles, lensing around a big
galaxy): define the galaxy region on the image (isophote or bit-512 area, grown by ~50%). Inside it, do not trust
catalogue entries individually. Correct number counts statistically with the field density measured in the same
catalogue, as done here. If a cleaner list is essential, cross-check against an independent catalogue (e.g. Legacy
Surveys, HSC through LSDB, see [14](14_hats_lsdb_access.md)), keeping in mind that those surveys handle large
galaxies differently.

---

## 11. Recommended clean galaxy sample (ADQL)

Low-z galaxy sample from the wide survey with MER + morphology + PHZ. **Tested** on 2026-11-13 on tile 102021980 (returns 10 rows in about 11 s with `TOP 10`; the tile restriction keeps the sync service from timing out). The cut values are starting points, not Euclid recommendations; every cut is sourced in sections 6-7.

```sql
SELECT TOP 10
  mer.object_id, mer.tile_index, mer.right_ascension, mer.declination,
  mer.vis_det, mer.det_quality_flag, mer.deblended_flag,
  mer.spurious_prob, mer.point_like_prob,
  mer.flux_detection_total,
  23.9 - 2.5*LOG10(mer.flux_detection_total) AS ie_kron_mag,
  mer.flux_vis_sersic, mer.semimajor_axis, mer.ellipticity,
  mor.sersic_sersic_vis_radius, mor.sersic_sersic_vis_index,
  mor.sersic_sersic_vis_axis_ratio, mor.sersic_visnir_flags, mor.flux_radius,
  pz.phz_median, pz.phz_flags, pz.phz_classification
FROM dr1.mer_catalogue_wide_survey AS mer
JOIN dr1.mer_morphology_wide_survey AS mor ON mor.object_id = mer.object_id
JOIN dr1.phz_photo_z_wide           AS pz  ON pz.object_id  = mer.object_id
WHERE mer.tile_index = 102021980                     -- keep the query small
  AND mer.vis_det = 1                                -- VIS-detected only
  AND mer.det_quality_flag < 4                       -- no saturation, border, star masks, extended-object area
  AND NULLIF(mer.spurious_prob, 'NaN') < 0.7         -- DR1 advice (Kuemmel+26)
  AND NULLIF(mer.point_like_prob, 'NaN') < 0.1       -- drop point-like (Dunn+26)
  AND mer.flux_detection_total > 3.63                -- I_E(Kron) < 22.5; 23.9 - 2.5 log10(3.63) = 22.5
  AND pz.phz_classification = 2                      -- galaxy (1 = star in the data, not in TAP text)
  AND pz.phz_median < 0.3                            -- low redshift; choose your own limit
  AND pz.phz_flags = 0                               -- PHZ processing OK
ORDER BY mer.flux_detection_total DESC
```

Notes:

- Add `AND mer.deblended_flag = 0` for clean photometry (Gasparetto+26); this removes many real galaxies in groups.
- For Sersic work add Dunn+26-style cuts on `sersic_sersic_vis_radius` (> 0.16"), `sersic_sersic_vis_index` (< 8, treat > ~7.9 as unconverged), `sersic_sersic_vis_axis_ratio`, and the `_err` columns; test the error bits one by one, e.g. `MOD(FLOOR(sersic_visnir_flags / 16), 2) = 0` for bit 4, rather than requiring `= 0`. (Untested.)
- **Variant for large nearby galaxies** (tolerates the extended-object bit 512 and the deblender-skip bit 1024; rejects bits 128/256 star masks and saturation). `MOD` is supported by the service (tested):
  `AND MOD(mer.det_quality_flag, 512) < 4`
  Tested on the NGC 1483 cone (tile 102021980, 70" radius, `phz_classification = 2`, `spurious_prob < 0.7`): returns the shredded fragments including the 12.8-mag main entry; the result is only a candidate list for visual checking, not a measurement.
- PHZ for the wide survey is in `dr1.phz_photo_z_wide` (photo-z, `phz_flags`, `phz_classification`) and `dr1.phz_physical_parameters_wide` (`phz_pp_median_stellarmass`, `phz_pp_median_sfr`, `phys_param_flags`, join on `object_id`; not tested here). `phz_flags`: 0 OK, +1 no close NNPZ neighbour, +2 incomplete flux set (TAP).
- To use the `wide_mode` group, replace the MER table names accordingly and keep the `..._wide` PHZ tables.

---

## 12. Which column for which science (extended galaxies)

| Science goal | Use | Do not use / warning |
|---|---|---|
| Total I_E magnitude, bright galaxies | `FLUX_DETECTION_TOTAL` (Kron) with `VIS_DET=1`; cross-check with `FLUX_VIS_SERSIC` | Kron is truncated in the outskirts; both biased if the MER sky removed galaxy light ([10](10_low_surface_brightness.md)) |
| Magnitude-limited selection | `FLUX_SEGMENTATION` (Dunn+26) or `FLUX_DETECTION_TOTAL` | do not use near the detection limit (Eddington-like bias) |
| Optical-NIR colours (core) | `FLUX_<band>_<n>FWHM_APER` ratios (same n); T-PHOT ratio for NISP | A-PHOT with `DEBLENDED_FLAG=1`; apertures <= a few arcsec for large galaxies |
| Total fluxes in Y/J/H/EXT | colour-scaled Kron (4.1) or `TEMPLFIT` | direct totals limited by segmentation |
| Size | `SERSIC_SERSIC_VIS_RADIUS` (arcsec) for I_E < ~24, `R_e` to ~16 % | `FLUX_RADIUS` (bug, segmentation-limited), `SEMIMAJOR_AXIS`/`KRON_RADIUS` (isophotal) |
| Inclination / shape | `SERSIC_SERSIC_VIS_AXIS_RATIO` | isophotal `ELLIPTICITY` (too round by ~0.09); single Sersic `q` underestimates inclination for B/T > ~0.1 and edge-on bulges |
| Sersic index | only as a population statistic, I_E < 23 | individual `n` (scatter ~0.6; pile-up at 8) |
| Bulge/disc | **own 2-D fit** on the mosaic with the MER PSF; Zoobot `BULGE_SIZE_*`, `DISK_EDGE_ON_*`, `HAS_SPIRAL_ARMS_*` as priors/selection | `DISK_SERSIC_*`, `T_TYPE` (empty) |
| Non-parametric structure | `CONCENTRATION`, `ASYMMETRY`, `SMOOTHNESS`, `GINI`, `MOMENT_20` | Q1 values; low-`FILLING_FACTOR` tiles; shredded galaxies |
| Visual-like type, mergers, bars, rings | Zoobot fractions (normalise; subsample I_E < 21 or area > 700 px); `MERGING_*`, `MAJOR_MERGER*` | blended sources and mergers fitted as single objects |
| Galaxy vs star | `PHZ_CLASSIFICATION = 2` plus `POINT_LIKE_PROB` low; stars: `POINT_LIKE_FLAG` | `POINT_LIKE_PROB` for NIR-only sources (NaN) |
| Redshift, mass, SFR | `dr1.phz_photo_z_*`, `dr1.phz_physical_parameters_*` | see the PHZ notes (`phz_flags`, `phys_param_flags`) |
| Galactic extinction | `GAL_EBV`, `GAL_EBV_ERR` (Planck map at the centroid) | correct surface brightness yourself |
| Blending / environment | `DEBLENDED_FLAG`, `PARENT_ID`, `BLENDED_PROB`, `SEGMENTATION_AREA` | `PARENT_ID = -2` (undocumented) |
| Exposure depth at the object | overview-file tables, layer files ([09](09_masks_flags_coverage.md)) | `FWHM` is the aperture-matching FWHM, not the I_E PSF |

---

## 13. Discrepancies between sources (for the maintainer)

| Topic | Source A | Source B | Used here |
|---|---|---|---|
| `PHZ_CLASSIFICATION` coding | TAP description: +1 galaxy, +2 star | DPDD and [verified](data_model/verified_on_archive.md): 1 star, 2 galaxy | verified |
| Zoobot subsample | DPDD / Cookbook: VIS < 20.5 or area > 1200 px (~2 %) | [Kuemmel+26](papers/kuemmel.md) p. 6: I_E < 21 or area > 700 px; verified ~38 % of bright VIS sources | Kuemmel+26, verified |
| Spurious threshold | [Romelli+26](papers/q1_romelli_mer.md) p. 14: 0.5 default | Kuemmel+26 p. 6: use 0.7 | 0.7 |
| `FLUX_RADIUS` | Kuemmel+26 pp. 4-5: disc of 6 a_M | Expsup 15.3.5: DR1 limited to the segmentation area | Expsup |
| T-PHOT bug timing | Expsup 15.3.2: found during DR1 processing | Kuemmel+26 p. 8: after DR1 processing | no impact |
| `object_id` resolution | help page: 3.6 mas | formula in DPDD: 0.36 mas | formula (derived) |
| Source count / tiles | Kuemmel+26: 8388 wide tiles in Table 5, 8887 released | verified: 8975 VIS wide tiles (+16 duplicates) | verified |
| `n` limit | DR1 `n_max` = 8 | Dunn+26 cut `n < 5.45` (Q1 convention) | both, labelled |
