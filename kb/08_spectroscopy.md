# NISP slitless spectroscopy in Euclid DR1 (SIR spectra, SPE redshifts, emission-line maps)

> Scope: what the NISP grisms deliver in DR1-Foundation (public 2026-11-12), the 1-D spectrum products (SIR), the
> redshift/line catalogue (SPE), how to retrieve both, how reliable they are, and what this means for a low-to-intermediate
> redshift galaxy programme. Citation style as in [07_photoz_physical_parameters.md](07_photoz_physical_parameters.md):
> `(Author+26, p. N)` = KB paper summary, `(DPDD)` = [dpdd_spectroscopy.md](data_model/dpdd_spectroscopy.md), `(verified)` = checked on
> the archive, *(checked 2026-11-13)* = quick queries run while writing this note (public TAP, tile 102021980). Wavelengths below
> are rest/observed in nm or Angstrom as stated; "z-range" columns are **computed by this note** from rest wavelengths and the
> nominal grism limits, not quoted from a paper.

> **Key points**
>
> - DR1 has **red-grism (RGS, 1206-1892 nm, R > 480) spectra for the whole Wide Survey** and red+blue (BGS, 926-1366 nm) only in
>   the Deep Fields (EDF-N: 8 red + 3 blue visits; EDF-S: 10 red; EDF-F: 1 red + 1 blue); spectra exist for every MER object with
>   H_E < 23.5, but a spectrum is not a redshift ([Aussel+26](papers/aussel.md), p. 3, 8; [Fumana+26](papers/fumana.md), p. 2).
> - The redshift pipeline is tuned for Halpha emitters at **0.84 < z < 1.88**; at 0.1 < z < 0.84 only ~40-60 % of EWS redshifts are
>   right and at z < 0.1 less than 10 %; in the best (EDF-N deep) data ~75 % at z > 0.84 and 42 % at z < 0.1
>   ([Le Brun+26](papers/lebrun.md), p. 7, 10). **For z < 0.84 the red grism sees no Halpha**: only Pa-beta, He I 1083 nm,
>   Pa-gamma, [S III] 907/953 nm (section 3).
> - Products: combined 1-D spectra per MER tile (FITS, up to 1000 objects per file, flux in 1e-16 erg/s/cm2/A already scaled),
>   SIR science frames (2-D dispersed, background subtracted), and SPE tables (classification, up to 5 redshift candidates per
>   object, line fluxes, quality flags). Retrieval is via `dr1.spectra_source_*` + DataLink / `Euclid.get_spectrum` (DR1 use of
>   `get_spectrum` not tested here).
> - Emission-line **maps** are a method (GELSA, user-run), not a released product ([Gabarra+26](papers/gabarra.md), p. 7).
> - Known pitfalls: duplicates (self-cal/COSMOS/CDFS overlaps), 13 SPE-incomplete tiles (14 entries listed), contamination and **morphological
>   smearing along the dispersion direction** for extended galaxies, band-edge masks, blue-grism ice drift of 5-15 %.

## 1. Grisms, coverage, resolution, depth, calibration

| Quantity | Red grism (RGS) | Blue grism (BGS) | Source |
|---|---|---|---|
| Nominal range | 1206-1892 nm | 926-1366 nm | Fumana+26, p. 2; Le Brun+26, p. 1; Bergamini+26, p. 3 |
| Dispersion | 1.372 nm/px (NISP pixel 0.3") | 1.239 nm/px | Fumana+26, p. 2 |
| Resolving power (0.5" source) | R > 480 (requirement R >= 380); R = 550-740 quoted by Gabarra | R > 400; R = 440-900 quoted by Gabarra | Fumana+26, p. 1-2; [Gabarra+26](papers/gabarra.md), p. 1 |
| Spectrogram length | ~530 px | ~350 px | Fumana+26, p. 5 |
| Wheel positions | RGS000 and RGS180 used in surveys (RGS270 non-conforming, unused); tilts RGS000+0, RGS180+4, RGS000-4, RGS180+0 | BGS000 | Fumana+26, p. 2 |
| Used in | EWS (4 dithers per ROS); EDF-N, EDF-S, EDF-F, calibration/auxiliary fields | EDFs only in DR1 (EDF-N 3 visits, EDF-F 1, COSMOS PV-005 116 exposures); **none in the EWS**; Q1 had none | [Tereno+26](papers/tereno.md), p. 10-11; [Aussel+26](papers/aussel.md), p. 3; Gabarra+26, p. 2 |
| Line-flux requirement / expected depth | 2e-16 erg/s/cm2 at 3.5 sigma at 1.6 um, 0.5" source (EWS); ~5e-17 expected at full EDS depth | ~6e-17 expected at full EDS depth | Fumana+26, p. 1; Bergamini+26, p. 3; Gabarra+26, p. 1-2 |
| Flux/surface-brightness sensitivity achieved (blue, COSMOS PV-005) | | 2.0e-16 erg/s/cm2/arcsec2 at S/N = 7 for 4 exposures (Halpha maps) | Gabarra+26, p. 5 |
| End-of-survey EDS depth | 15 RGS visits | 25 BGS visits (blue:red about 25:15) | Le Brun+26, p. 1; Aussel+26, p. 3 |

- **Depth in DR1**: EDF-N 28 %, EDF-S 22 %, EDF-F 4 % of final depth ([Tereno+26](papers/tereno.md), p. 11). Dithers: 4 (wide) vs 60 (deep) per source (DPDD).
- **Calibration accuracy (Fumana+26)**: wavelength residuals 0.137-0.205 nm rRMS (requirement 0.3 px = 0.40 nm red, 0.37 nm blue), trace curvature sMAD 0.10-0.16 px;
  relative flux calibration error mostly < 1 % and up to 1.5 % at the blue end of BGS versus a 0.5 % requirement (p. 8, 10-11); flux stability vs ~6e5 Gaia stars <= 0.7 %
  (p. 11-12); relative-flux corrections reach ~10 % locally for tilted grisms (p. 7); ice contamination: <~1 % on RGS, **5-15 % on BGS at short wavelengths**, not corrected for blue-grism data (p. 12; Aussel+26, p. 2).
  Redshift precision sigma_dz/(1+z) = 3-4e-4 in DR1 (0.0008 in Q1) (Le Brun+26, p. 7, 18). Wavelengths: a few tens of km/s kinematics are **not** guaranteed (Fumana+26).
- **Only first and zeroth orders are modelled**; orders -1 and +2 (percent-level) are ignored; the 4x4 detector mosaic gaps (~6 mm along, ~3 mm across dispersion) split spectra (Fumana+26, p. 1, 3-4).
- Flux calibration is tuned for point sources (white dwarf standard); extended-source slit losses are **not** corrected (Fumana+26; inference from the point-source basis).

## 2. Which lines fall in the red grism (computed)

Observed range 1206-1892 nm (RGS) and 926-1366 nm (BGS) from the papers; **usable range is narrower**: pixels below 25 % of the band-edge throughput are flagged `NOT_USE` and between 25 % and 85 % `ABS_FLUX`
(DR2 will narrow this to 25-50 %) (Fumana+26, p. 8, 11). Rest wavelengths (vacuum) are standard values.

| Line (rest, A) | RGS z-range | BGS z-range (EDFs only) | Comment |
|---|---|---|---|
| Pa-beta 12822 | z < 0.476 | z < 0.065 | strongest low-z line in the red grism for dusty/starburst galaxies; SPE measures it (Le Brun+26, p. 3) |
| Pa-gamma 10941 | 0.10 - 0.73 | z < 0.25 | |
| He I 10830 | 0.11 - 0.75 | z < 0.26 | |
| Pa-delta 10052 | 0.20 - 0.88 | z < 0.36 | secondary line |
| [S III] 9531 (9532) | 0.27 - 0.99 | z < 0.43 | measured by SPE; low-z "helper" (Le Brun+26, p. 7) |
| [S III] 9069 | 0.33 - 1.09 | 0.02 - 0.51 | measured by SPE |
| [S II] 6718/6732 | 0.80 - 1.82 | 0.38 - 1.03 | |
| **Halpha 6565 (+ [N II] 6585)** | **0.84 - 1.88** | **0.41 - 1.08** | **target of the pipeline; only for z > 0.84 in the EWS** |
| Hbeta 4863 / [O III] 5008 | 1.48-2.89 / 1.41-2.78 | 0.90-1.81 / 0.85-1.73 | interlopers at low z, real lines at z > 1.4 |
| [O II] 3727 | 2.24 - 4.08 | 1.49 - 2.67 | |
| Pa-alpha 18756 | z < 0.01 | | irrelevant |

Consequences: for the EWS (red only), a z < 0.84 galaxy shows no Halpha; its SPE redshift depends on weak Paschen/He I/[S III] lines (or the continuum of bright quiescent galaxies; Le Brun+26 show a z = 0.232,
H_E = 15.5 quiescent galaxy fitted by the QG template, p. 5), so success is low (section 6). Blue-grism Halpha enters at z ~ 0.41 (Gabarra+26, p. 15), but only EDFs have BGS.
Below z ~ 0.1 essentially no strong line is in range (consistent with < 10 % success, Le Brun+26, p. 10). Halpha interlopers in the SPE solutions: [O III], [S III]9532, He I, Pa-beta, Hbeta, [O II] (Le Brun+26, p. 10).

## 3. SIR products

SIR extracts and combines spectra for all MER-catalogue objects with H_E < 23.5 (one magnitude deeper than Q1; the archive help writes "NIR_H = 23.5") (Aussel+26, p. 8). Only two SIR products are public: the **combined spectra**
and the **science frames**; single-dither extracted spectra, location tables and decontamination products are not archived (DPDD).

### 3.1 Combined spectra (`DpdSirCombinedSpectra`)

- One product per MER tile and grism family; file name `EUC_SIR_W-COMBSPEC_<TILEID>_<timestamp>Z.fits(.gz)`; DPDD: a collection of FITS files with **1000 `CombinedSpectrum` entries each**; primary header keyword `LRANGE` = `RGS` or `BGS`
  (a tile with both gets two products, so an object can have one combined spectrum per grism family); `N_OBJ`, `TILE_ID`, `MSK_FLAG_*` dictionary (DPDD).
- Per object `m` (running index in the file, **not** the object ID): `m_META` (header only: `N_DITH`, `OBJ_ID` = MER id, `RA_OBJ`, `DEC_OBJ`; the only HDU if no spectrum was extracted), `m_DITH1D_n_SIGNAL`
  (one binary table per dither, `n` = pointing id; header `GWA_POS`, `GWA_TILT`, `DITH_ID`, `PTGID`, `EXPTIME`, `WMIN`, `BINWIDTH`, `BINCOUNT`, `DET_ID`, `DET_ID_2`, `LSF_SIG`, `EXT_PROF`),
  `m_DITH1D_n_CONTAMINANTS` (column `OBJ_ID`: ids of contaminating objects), and `m_COMBINED1D_SIGNAL` (the combined spectrum) (DPDD).

| Column | In dither / combined table | Unit / values |
|---|---|---|
| `WAVELENGTH` | both | Angstrom |
| `SIGNAL` | both | **1e-16 erg s-1 cm-2 A-1**; the 1e-16 scaling is already in the unit; header `FSCALE` is deprecated (1E-16): do **not** multiply again (DPDD; the astroquery Q1 example plots `SIGNAL` directly) |
| `VAR` | both | variance of the flux in 1e-32 erg2 s-2 cm-4 A-2; 1-sigma = `sqrt(VAR)` in 1e-16 units (DPDD, inference) |
| `MASK` | both | bit values (DPDD calls them positions but the numbers are powers of two): 0 GOOD, 1 NOT_USE, 2 LOW_SNR, 4 EXT_PRB, 8 HIGH, 16 LOW, 32 REL_FLUX, 64 ABS_FLUX; AND with `MASK` (inference); read the actual dictionary in the header |
| `QUALITY` | both | 0-1, fraction of available weight used in a flux bin |
| `NDITH` | combined only | number of dithers contributing to each bin |

NOT_USE / ABS_FLUX at the band edges follow the throughput thresholds in section 1; the other bit names are not defined in prose in the DPDD. Wavelength grid per spectrum: `WMIN`, `BINWIDTH`, `BINCOUNT`.
Wide objects have up to ~4 dithers per grism configuration, deep objects many more (`NDITH` column).

### 3.2 Science frames (`dr1.sir_science_frame`, `dr1.sir_frame_detectors`)

Background-subtracted dispersed images, one multi-extension FITS per dither/exposure: **48 extensions = 3 per detector** (`DETn.SCI`, `DETn.VAR`, `DETn.DQ`, n = detector, 16 detectors); DQ bit numbers: 0 hot, 1 cold, 2 saturated, 3 cosmic ray, 4 satellite trail,
5 interpolated, 6 bleeding, 7 on-board masking, 8 bad pixel, 9 non-linear, 10 persistent charge, 11 ghost masking, 12 transient, 13 extended object, 14 scattered light, 15 charge injection, 16 near charge injection (DPDD, bit numbers here, unlike the spectrum mask).
File name `EUC_SIR_W-SCIFRM_BKGSUB_<OBSID>_<PTGID>_<DITH>_<GWA>_<TILT>_<timestamp>Z.fits.gz`. The table `dr1.sir_science_frame` (30 columns: `observation_id`, `file_path`, `file_name`, `fov`, `ra`, `dec`, `datalabs_path`...) finds frames by
footprint: `1 = INTERSECTS(CIRCLE(spe.ra_obj, spe.dec_obj, 2/3600.), sf.fov)`; `dr1.sir_frame_detectors` holds gain, readout noise, zero point, CRVAL/CRPIX per detector (archive help `Spectra.md`; not described in the DPDD).
Science frames are the input of GELSA (section 8) and of custom extractions ([Bergamini+26](papers/bergamini.md), p. 3). The `observation_id` columns may be typed as character (archive help `Fields_with_multiple,_conflicting_data_types`).

## 4. How to retrieve spectra

| Step | Tested? | Detail |
|---|---|---|
| 1. Find sources with spectra | **verified** *(checked 2026-11-13)* | `dr1.spectra_source_wide`, `_deep`, `_deep_visits` (12 columns: `source_id` (= MER `object_id`), `ra_obj`, `dec_obj`, `file_name`, `file_path`, `hdu_index`, `dith_num`, `combined_spectra_fk`, `combined_spectra_product_fk`, `datalabs_path`, `to_be_published`, `spectra_source_oid`). The all-groups table `dr1.spectra_source` has 16 columns incl. `lambda_range` and `sourcepatch_id` |
| 2. Join to MER | verified | `... JOIN dr1.mer_catalogue_wide_survey AS mer ON mer.object_id = ss.source_id` (archive help example). `dith_num` suggests the rows relate to dithers (unverified); repeated objects arise at least for the reasons below |
| 3. Grism and tile | verified | `JOIN dr1.combined_spectra cs ON cs.combined_spectra_oid = ss.combined_spectra_fk` gives `lambda_range` (RGS/BGS), `tile_index`, `file_number`. In wide tile 102021980: 28 772 spectra, all RGS; file `EUC_SIR_W-COMBSPEC_102021980_20250826T103304.426942Z.fits`, `hdu_index` values up to 1980 and `dith_num` 3-4 were seen. **`hdu_index` semantics unverified** (the DPDD says 1000 objects per file; values above 1000 suggest it indexes HDUs or a multi-file set) |
| 4. File | not downloaded | `dr1.combined_spectra_product` has `file_path`, `file_name`, `access_url`, `datalabs_path` (up to 1000 spectra per file); Datalabs users read directly from `datalabs_path` |
| 5. DataLink (web GUI) | **Q1 help page only** | ADQL job in the archive form, query output **must contain `source_id`**; click the double-chain icon, "Show Data"; "Download format" selector is ineffective (always FITS), "Data release" only offers `sedm` on the Q1 page; red file `SPECTRA_RGS_COMBINED.fits`, blue `SPECTRA_BGS_COMBINED.fits` (empty in Q1). DR1 behaviour (BGS file for deep fields, `dr1` release) is **not verified** |
| 6. astroquery | **verified** (2026-11-13, astroquery git main) | `Euclid.get_spectrum(ids='-582334178474562017', schema='dr1', retrieval_type='SPECTRA_RGS', output_file='x.fits')` writes `SPECTRA_RGS-dr1 <id>.fits`: one BINTABLE (EXTNAME = object id) with 531 rows, columns `WAVELENGTH` [Angstrom, 11900-19002, 13.4 A bins], `SIGNAL` [1e-16 erg/s/cm2/A], `MASK`, `QUALITY` (0-1), `VAR` [1e-32 ...], `NDITH`; header `FSCALE = 1e-16` (already applied in the unit), `EXPTIME`, `LSF_SIG` (~8.6 A), `SOURC_ID`. MASK bit values seen: 1, 2, 4, 64 and sums; LOW_SNR (2) and EXT_PRB (4) cover long ranges even for an H_E = 16.2 galaxy, so hide only NOT_USE (1) and ABS_FLUX (64). Demo: `demo/04_spectra.py` |

Duplicates: JOINs MER-SIR can return several spectra per `object_id` (`spectra_source_wide`, `_deep`, `_deep_visits`): the self-cal field is observed many times in wide-like mode, COSMOS is observed twice in the deep set, and CDFS lies inside
EDF-F (archive help `Multiple_spectra_associated_with_the_same_MER_object_id`); in `deep_visits` an object normally gets a different id per visit but can by chance get the same id (archive help `Catalogues.md`). (The archive help page on missing COMBSPEC files in tile 102160055 concerns **Q1** only.)

## 5. SPE catalogue (redshifts, classification, lines)

SPE tables (TAP names `dr1.spectro_<kind>_spe_<...>_<group>`; groups **`wide`** (all single-visit data incl. calibration fields), **`wide_survey`** (EWS only), **`deep`** (EDS stacks, RGS+BGS fitted together) and **`deep_visits`** (single EDF visits, one row per visit);
the SPE paper calls the deep stacks `deep_survey`; Le Brun+26, p. 4).

| Table (suffix per group) | Content and key columns (TAP names) |
|---|---|
| `spectro_z_spe_quality_*` (38) | `spe_error_flag`, `spe_warning_flag`, per-stage error/warning flags (`spe_gal_error_flag`, `spe_class_error_flag`, ...), `spe_grism` (BGS, RGS, BGS\|RGS), `spe_w_min`, `spe_w_max`, `spe_npix`, `spe_n_dith_max`, `spe_n_dith_med`, `spe_n_dith_red_l/m/h`, `spe_n_dith_blue_l/m/h`, `spe_lsf_red`, `spe_lsf_blue` (DPDD says `SPE_LSF`), `spe_gal_cont_*` |
| `spectro_z_spe_classification_*` (12) | `spe_class` (**lower-case** `galaxy`, `star`, `qso`; undefined possible) and `spe_gal_prob`, `spe_star_prob`, `spe_qso_prob` |
| `spectro_z_spe_galaxy_candidates_*` (25) | up to 5 rows per object, `spe_rank` 0 = best: `spe_z`, `spe_z_err`, `spe_z_prob`, `spe_z_rel`, `spe_cont_snr`, `spe_z_reduced_chi2`, `spe_z_p_value`, `spe_z_residual_normality`, continuum versions, `spe_subclass`, `spe_pdf` window (`spe_pdf_zmin/zmax/deltaz`, 80 samples) |
| `spectro_z_spe_qso_candidates_*` (22) | same without the continuum columns |
| `spectro_z_spe_star_candidates_*` (18) | `spe_rvel`, `spe_rvel_err`, `spe_model_prob`, `spe_model_rel`, ... (radial velocity, one row) |
| `spectro_model_spe_{galaxy,star,qso}_models_*` | best-fit model parameters per candidate (`spe_cnt_tpl_id`, `spe_vel_disp_e/a`, `spe_lines_id/amp`, ...) |
| `spectro_line_features_spe_line_features_*` (42) | one row per object x rank x line: `spe_line_name`, `spe_line_flux_gf/_di`, `_flux_err_`, `_snr_gf/di`, `_ew_`, `_fwhm_gf`, `_central_wl_`, `_lum_`, `spe_line_n_dith`, `spe_line_qual_gf/di`, `spe_line_aon` |
| `..._atomic_indices_*`, `..._molecular_indices_*`, `..._continuum_features_*` | Lick, molecular and continuum indices (D4000 only where continuum S/N > 10 in 1350-1750 nm; Le Brun+26, p. 4); DPDD descriptions of the continuum-feature table are copy-pasted and unreliable |
| `dr1.spe_catalogue` | file-level metadata with `tile_index_list`; join `basic_download_data_oid` (archive help) |

All SPE tables join to MER on `object_id`; the candidate/model/line tables are one-to-many (join on `object_id` **and** `spe_rank`). SPE tables have no `tile_index`: filter via MER or `spe_catalogue`.
Missing archive columns: `SPE_LYA_IGM` in the galaxy/QSO model tables (archive help). `spe_lsf_blue/red` are undocumented in the DPDD. The SPE PDF-catalogue file is not described in the DPDD. Line measurements: main lines Lyman-alpha, [O II], Hbeta, [O III], Halpha, [N II]6585,
[S II]6718, [S III]9068, [S III]9530, Pa-gamma, Pa-beta (secondary lines only if A/N > 2.5); GF fits give doublet totals, DI gives blended Halpha+[N II], and DI fluxes are ~15 % larger than GF (to be removed in DR2) (Le Brun+26, p. 3). `spe_line_qual_*`: three digits (method 1 DI, 2 GF, 3 QSO Halpha / quality 1 good, 2 S/N < 2, 3 EW > 0, 4 combination issue, 5 acceptable up to 15 % pixels missing, 7 merge error, 8 unreliable / grism 1 BGS, 2 RGS, 3 both); good GF-RGS values are **212** (also 252, 222 if conservative) (Le Brun+26, p. 11; DPDD).

**Verified counts** *(checked 2026-11-13)*, wide tile 102021980: 28 772 RGS spectra, of which 22 145 have a classification row (21 954 `galaxy`, 151 `star`, 40 `qso`): "a spectrum exists" does not imply "an SPE solution exists".

## 6. Quality cuts and performance

### 6.1 Recommended cuts

| Use | Cut (Le Brun+26, p. 6-7 unless stated) |
|---|---|
| processing sanity | `spe_error_flag = 0`, `spe_gal_error_flag = 0` (DPDD; for stars/QSOs the matching flag) |
| best candidate | `spe_rank = 0` |
| high-quality galaxy redshifts (cosmology-like) | EDS: `spe_npix >= 800`, `spe_n_dith_med >= 12` (to 15); EWS: `spe_npix >= 300`, `spe_n_dith_med >= 3`; `spe_z_prob > 0.99` (or > 0.94 together with `spe_z_rel > 0.05`); MER `point_like_prob < 0.05`, `spurious_prob < 0.5`, **`kron_radius < 50`**; velocity dispersion < 1500 km/s |
| extra purity | require the SPE redshift to lie within the 95 % interval of the PHZ redshift (`phz_95_int`): > 80 % correct everywhere at probability 0.99 and 98 % at 0.84 < z < 1.6 |
| line fluxes | `spe_line_snr_gf > 0` (S/N > 5-10 for science); `spe_line_qual_gf` = 212 or 252 (222); prefer GF over DI |
| real quasars | use `spe_cnt_tpl_id` (templates `optical_nir_qso_template_v1.txt`, `ComposantesPCA4_meanqso.txt`); other `qso` rows with galaxy templates are quiescent or type-2 candidates |
| stars | `point_like_prob` from MER; star-class purity ~99 % |
| `spe_z_prob` caveat | it is a relative, not an absolute, significance; `spe_z_rel` was trained on EL-COSMOS simulations and is sub-optimal on DR1 data (p. 7) |

### 6.2 Success rate and purity (Le Brun+26)

| Sample / redshift | Correct fraction (|dz| < 0.003 unless stated) | Page |
|---|---|---|
| EDF-N deep, high-quality 'galaxy' sample vs DESI, 0.84 <= z < 1.6 | ~75 % (never above 80 % even at the highest probability thresholds) | 7 |
| same, 0.1 < z < 0.41 and 0.41 < z < 0.84 | similar, no significant change (Halpha entering the BGS is not essential; [S III] helps) | 7 |
| same, z < 0.1 | 42 % | 7 |
| with PHZ agreement and probability 0.99 | > 80 % everywhere, 98 % at 0.84 < z < 1.6 | 7 |
| EWS (single EDF-N visits, RGS only), z < 0.1 | < 10 % | 10 |
| EWS, 0.1 < z < 0.84 | ~40 %, rising to ~60 % with a probability threshold (< ~10 % in Q1) | 10 |
| EWS, 0.84 < z < 1.88 | about 10 points better against EDS than against DESI | 10 |
| EWS, z > 1.88 | ~64 % at probability 0.99 vs EDS, but < ~3 % vs the few DESI matches | 10 |
| EDF-N visual inspection of 4000 sources (cosmology sample 0.85-1.85, F(Halpha) > 2e-16) | uncertain 1.3 %, marginal 17.4 %, reliable 50.9 %, secure 30 % | 8 |
| spectra-only selection vs DESI (3985 objects) | 98.5 % agreement; 98.9 % with `spe_z_prob > 0.94` and `spe_z_rel > 0.05` (3863 objects) | 7 |

- **Classification vs DESI** (Table 1, p. 6): galaxies 64.6 % (EWS) / 78.6 % (EDS) agree on spectra only, 98.2 % / 98.4 % after requiring MER extended (`point_like_prob < 0.5`); stars 99.6 % / 98.6 %; QSO purity 88.2 % / 95.5 % but < 5 % of DESI quasars recovered
  as `qso` (most leak into `galaxy`); the classification is biased in favour of `galaxy`.
- **Quantities**: 160 million redshifts in the Wide Survey and 7.0 million in the Deep Fields (2.7 million in EDF-N) (Le Brun+26, p. 12); the overview quotes > 170 million validated spectra ([Aussel+26](papers/aussel.md), p. 8). High-quality EWS sample in EDF-N: 974 487 sources (p. 10).
- **Redshift scatter** (z_SPE - z_DESI)/(1 + z_DESI): median ~1e-5, scatter 4.1e-4 (EWS) and 3.2e-4 (EDS) (p. 18). **Halpha flux**: EWS vs EDS median -2 (+19, -26) % above 2e-16 erg/s/cm2; vs FMOS +7 (+43, -28) % (p. 11); EWS flux errors a factor sqrt(17/4) larger than EDS (as the summary reads; p. 11).
- Bright low-z galaxies: DESI is reliable to z = 1.6 as reference, so the low-z success statistics are against DESI, which preferentially has bright/extended targets.

## 7. Known issues and caveats

1. **Halpha prior**: pushes noise redshifts into 0.84-1.88 and creates Halpha interlopers; too strong for DR1, to be retuned in DR2 (Le Brun+26, p. 10).
2. **Galaxy model = emission-line objects only**; quiescent galaxies and type-2 AGN appear in the `qso` class via extra templates; classification is biased to galaxy; stars/QSOs leak into galaxy (p. 3, 6).
3. **Low-z**: lines few and faint; large angular size dilutes the signal; `kron_radius > 50` is excluded for the cosmology sample (p. 7, 10).
4. **Extended sources smear along the dispersion direction**: the spectrum is the object convolved with its own morphology along dispersion, so lines broaden beyond the instrumental resolution, kinematic information is not clean, and a 1D extraction of resolved structure can mimic [N II] or
   shift redshifts: position and wavelength are coupled (1 NISP pixel = 0.3" = 1.372 nm; for Halpha this is delta z of about 0.002 per pixel, i.e. ~0.007 per arcsecond along dispersion, **computed**) (Bergamini+26, p. 5; Gabarra+26, p. 7, 9-11; Fumana+26, p. 1-2).
5. **Contamination** by neighbours' spectra is not explicitly modelled in the SPE, only listed in `CONTAMINANTS`; blended/interacting systems may have a displaced MER position (Gabarra+26, p. 9-11, 14). Persistence masking is conservative (> 10 % of pixels masked in some exposures; [Kubik+26](papers/kubik.md)).
6. **Duplicates** (section 4) and **SPE-incomplete tiles** near tile edges (13 distinct, 14 entries): 101365713, 101279563, 102009788, 102026534, 102036731, 102038463, 102038572, 102042948, 102045496, 102139292, 102140855, 102154845, 102156286 (the archive help `SPE_catalogue_incompleteness` lists 102045496 twice).
7. **Band edges** (`NOT_USE`, `ABS_FLUX`), blue-grism ice drift (5-15 %), RGS < 1 % (Fumana+26, p. 8, 12); blue-grism redshifts in EDFs are not ice-corrected (Aussel+26, p. 2).
8. Deep fields: EDF-F has one visit per grism, EDF-S RGS only, EDF-N most complete; a spurious plateau at 4.1 < z < 5 in EDF-N, a drop at z ~ 2.8 where [O III]/Hbeta exit (Le Brun+26, p. 8, 18). Redshift distributions reflect detection biases.
9. Stacked spectra of low-quality tiers can mimic good spectra (aligned noise), so stacked-line detections do not validate individual redshifts (p. 9-10).
10. Orientation: EDF visits have different position angles, so dispersion directions differ; COSMOS has one orientation plus its 180-degree flip ([Tereno+26](papers/tereno.md), p. 12-13); this matters for overlap contamination and for GELSA.

## 8. Emission-line maps (GELSA)

- GELSA (`github.com/elsa-euclid/gelsa`, v3.1 in Gabarra+26; ELSA project) resamples the SIR science frames onto the sky (0.1"/px RA/Dec grid) at a fixed observed wavelength, drizzles exposures (pixel fraction 0.5, 100 drops) and subtracts the continuum
  (sigma-clipped median over 400 A, or a 100-px median filter in Bergamini+26); the maps look like narrow-band images but are **not monochromatic**: Halpha and [N II] appear as shifted copies along the dispersion direction. **It is a software method, not a released DR1 product**:
  the archive has no map table (Gabarra+26, p. 7, 14; Bergamini+26, p. 3).
- Demonstrated: blue grism, COSMOS PV-005 (116 exposures x 549 s, one orientation), 0.4 < z < 0.9; effective resolution EE50 = 0.265" (FWHM ~0.53", 1.4-2.3 kpc), Halpha surface-brightness sensitivity 2.0 +/- 0.2e-16 erg/s/cm2/arcsec2 at S/N = 7 for 4 exposures,
  flux recovery within ~5 % median (scaled MAD 14-24 %); Halpha is 10-27 % more extended than the Y_E light (R50 ratio 1.10-1.27, mean 1.15) (Gabarra+26, p. 5-7, 14). Red-grism maps at z > 0.84 and other lines (Hbeta, [O III], [O II], Pa-beta) are future work; **z < 0.4 (Pa-beta, [S III], He I) is not covered** (p. 15).
- Cautions: with a single orientation a [N II] counterpart can masquerade as a clump; velocity gradients shift emission along dispersion and are degenerate with morphology (opposite 180-degree orientations needed); bright continua (Y_E < 19.9) leave residuals; 43 % of injected sources were rejected because fitted widths hit the bounds;
  only circular Gaussians were injected (no bulge+disc tests); the SPE redshift depends on the adopted extraction position (Gabarra+26, p. 3-9, 11-12). For multiple orientations model each separately; masks for persistence (30 ADU) and zero orders are applied by GELSA.
- Lensed arcs: custom extractions with 0.9" apertures and 3-38 exposures give single- to three-line redshifts, but the automated SPE fails on crowded/extended lenses (Bergamini+26, p. 1, 5, 15).

## 9. Advice for a low-to-intermediate-z extended-galaxy programme

1. **Redshifts at z < 0.84**: use external spectroscopy (DESI DR1, SDSS, GAMA) where available; the SPE redshift is a cross-check only: 40-60 % correct at 0.1 < z < 0.84, < 10 % at z < 0.1 in the EWS. Require `spe_z_prob > 0.99` **and** agreement with `phz_95_int` if you must use it; never use a single-line redshift without independent confirmation.
2. **Targets at 0.84 < z < 1.9** (Halpha above ~2e-16 erg/s/cm2): SPE is competitive (up to 98 % with PHZ agreement) for galaxies up to ~`kron_radius` 50 px (5"); larger objects are the worst case for slitless work.
3. **Resolved line emission**: use GELSA on the science frames (blue grism 0.4 < z < 0.9 in EDFs/COSMOS; red grism z > 0.84 expected); budget a PSF of 0.5" FWHM, PSF-match the Euclid image to it before comparing profiles, and mask [N II] positions along the dispersion direction (Gabarra+26, p. 14-15).
4. **Line fluxes** (Halpha, Pa-beta, [S III] SFR proxies) are integrated within the extraction aperture, not total fluxes of extended galaxies; apply aperture considerations yourself (inference; Fumana+26 note point-source flux calibration).
5. **Catalogue queries**: always select `spe_rank = 0`, `spe_error_flag = 0`, join on `object_id`; remove duplicated spectra (self-cal, COSMOS, CDFS, `deep_visits`); drop the 13 incomplete tiles for completeness statistics.
6. **Redshift-dependent selection effects**: the SPE success is a steep function of z, line flux and extent; do not treat spec-z-completeness as flat when stacking.
7. Cross-reference [07_photoz_physical_parameters.md](07_photoz_physical_parameters.md) for the PHZ alternative and [10_low_surface_brightness.md](10_low_surface_brightness.md) for images.

## 10. ADQL example (MER + PHZ + SPE)

Tested 2026-11-13 on tile 102021980 as an **async** job (the same query as a sync request timed out after ~60 s; the 5-way join returned 8 rows after a few minutes). Columns are real TAP names.

```sql
SELECT TOP 8 m.object_id, m.tile_index, m.point_like_prob, m.spurious_flag, m.kron_radius,
       -2.5*LOG10(m.flux_detection_total) + 23.9 AS i_e_kron_mag,
       c.spe_class, c.spe_gal_prob,
       g.spe_rank, g.spe_z, g.spe_z_err, g.spe_z_prob, g.spe_z_rel, g.spe_cont_snr,
       qu.spe_error_flag, qu.spe_gal_error_flag, qu.spe_npix, qu.spe_n_dith_med, qu.spe_grism,
       p.phz_median
FROM dr1.mer_catalogue_wide_survey AS m
JOIN dr1.spectro_z_spe_classification_wide AS c ON c.object_id = m.object_id
JOIN dr1.spectro_z_spe_galaxy_candidates_wide AS g ON g.object_id = m.object_id
JOIN dr1.spectro_z_spe_quality_wide AS qu ON qu.object_id = m.object_id
JOIN dr1.phz_photo_z_wide AS p ON p.object_id = m.object_id
WHERE m.tile_index = 102021980
  AND g.spe_rank = 0 AND c.spe_class = 'galaxy'
  AND qu.spe_error_flag = 0 AND qu.spe_gal_error_flag = 0
  AND qu.spe_npix >= 300 AND qu.spe_n_dith_med >= 3 AND g.spe_z_prob > 0.99
```

The returned rows were all at `spe_z` 0.9-1.75 (RGS, 3-6 median dithers, `spe_z_prob` > 0.99, `spe_z_rel` 0.05-0.56), `spe_cont_snr` empty (NULL/NaN) for these faint emitters, consistent with the Halpha-prior bias of the pipeline; no low-z solution
passed. (Eight rows only; not a statistic.) Spectra file names for the same objects come from `dr1.spectra_source_wide` + `dr1.combined_spectra` as in section 4.

## 11. Contradictions between sources

| # | Topic | Sources | Note |
|---|---|---|---|
| 1 | Grism wavelength ranges | archive help `Spectra.md`: BGS ~0.92-1.25 um, RGS ~1.25-1.85 um; papers: BGS 926-1366 nm, RGS 1206-1892 nm | papers are the instrument/calibration references (Fumana, Le Brun, Bergamini); the help page rounds differently, and cuts a few hundred nm at the red end of the BGS |
| 2 | Resolving power | Fumana: R > 480 (RGS), > 400 (BGS); Gabarra: 550-740 (RGS), 440-900 (BGS) | requirement-like lower bounds vs quoted ranges |
| 3 | Number of spectra | Aussel > 170 million validated; Le Brun > 160 million (wide) + 7.0 million (deep) | about consistent; different counting (validated vs redshift entries) |
| 4 | Combined-spectra file size | DPDD: 1000 `CombinedSpectrum` entries per file; `spectra_source_wide.hdu_index` up to 1980 seen for one file name | unresolved; open the first file to check |
| 5 | EDF-N visits | Le Brun: 7 complete RGS + 3 BGS (8 visits in `deep_visits`); Aussel/Tereno/archive help: 8 red + 3 blue | one RGS visit incomplete |
| 6 | SPE group names | archive help: `deep`; Le Brun: `deep_survey`; TAP: `_deep`, `_deep_visits`, `_wide`, `_wide_survey` | use TAP names |
| 7 | `SPE_LSF` | DPDD `SPE_LSF`; archive `spe_lsf_red`, `spe_lsf_blue` | help page confirms |
| 8 | Mask semantics | DPDD "bit position" but values 1, 2, 4... | read the header dictionary |
| 9 | SPE incompleteness list | archive help says tile list; 102045496 appears twice | 13 distinct tiles (14 entries) listed |

## 12. References (KB summaries)

[Le Brun+26](papers/lebrun.md) (SPE) - [Fumana+26](papers/fumana.md) (SIR calibration) - [Gabarra+26](papers/gabarra.md) (GELSA maps) - [Bergamini+26](papers/bergamini.md) (arcs) - [Aussel+26](papers/aussel.md), [Tereno+26](papers/tereno.md) (fields, visits) -
[Kubik+26](papers/kubik.md) (persistence) - DPDD [dpdd_spectroscopy.md](data_model/dpdd_spectroscopy.md) - TAP dumps `data_model/tap/dr1.spectra_source*.md`, `dr1.combined_spectra*.md`, `dr1.sir_science_frame.md`, `dr1.spectro_*.md`.
