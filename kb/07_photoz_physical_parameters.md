# Photometric redshifts, classification and physical parameters (PHZ) in Euclid DR1

> Scope: what the PHZ processing function (PF) delivers in DR1-Foundation (public 2026-11-12), which archive tables and
> columns carry it, how good it is (with emphasis on low redshift, z < 0.5, and bright extended galaxies), and how a
> low-to-intermediate-z galaxy-structure programme should use or avoid it.
> Citation style: `(Author+26, p. N)` = A&A DR1-Foundation paper, page as given in the KB summary; `(DPDD)` = DPDD notes in
> [dpdd_phz.md](data_model/dpdd_phz.md); `(verified)` = facts checked hands-on on the archive, see
> [verified_on_archive.md](data_model/verified_on_archive.md) and the checks marked *(checked 2026-11-13)* below.
> Related notes: [01_dr1_overview.md](01_dr1_overview.md), [04_imaging_processing.md](04_imaging_processing.md),
> [10_low_surface_brightness.md](10_low_surface_brightness.md), spectroscopy in [08_spectroscopy.md](08_spectroscopy.md),
> acronyms in [13_glossary.md](13_glossary.md).

> **Key points**
>
> - Photo-z, physical parameters and SEDs come from **NNPZ** (nearest neighbours in a COSMOS-only reference sample) using
>   **2xFWHM PSF-matched aperture fluxes scaled to the Kron total flux**; they are colour-plus-total-flux quantities with no
>   structural information ([Hartley+26](papers/hartley.md), p. 5-6; [Enia+26](papers/enia.md), p. 2-3).
> - Quality is good for typical galaxies (bright EWS-like: NMAD 0.02-0.04, outliers 0.4-9 %; at I_E < 24.5 about 20 % outliers),
>   but **the PHZ authors themselves state that z < 0.2 galaxies and very massive galaxies at z < 0.4 are
>   under-represented in the reference sample: redshifts are "mostly reasonable", stellar masses are biased low**
>   (Hartley+26, p. 19). No metric is published binned in redshift.
> - Archive reality check *(checked 2026-11-13, tile 102021980)*: among bright galaxies (Kron I_E < ~18, class 2) 251 of 256
>   objects have `phys_param_flags = 1` (no usable neighbour), so the standard `PHYS_PARAM_FLAGS = 0` cut removes most bright
>   nearby galaxies. Use external spec-z (DESI etc.) and your own masses for them.
> - `phz_classification`: **1 = star, 2 = galaxy, 3 = ambiguous, 0 = none, -1 also occurs**; the TAP text is swapped (verified).
>   `phz_flags` is a plain code (0, 1, 10, 11, 12), not independent bits *(checked)*.
> - Join everything on `object_id` with the MER catalogue; PHZ tables exist for four data groups (`wide`, `deep_survey`,
>   `deep_mode`, `deep_visits`), and an ADQL join example with real column names is in section 8.

## 1. Pipeline in one paragraph

PHZ takes the MER final catalogue (VIS I_E, NISP Y_E/J_E/H_E, ground-based u/g/r/i/z) and, per object, (i) identifies the
photometric system (DECam in the south, UNIONS = CFHT u,r + HSC g,z + Pan-STARRS i in the north; part of the north has no u)
and imputes missing bands for classification only, (ii) classifies star/galaxy/QSO with two probabilistic random forests
on asinh colours, (iii) estimates photo-z PDFs and physical parameters with **NNPZ**: the 30 nearest neighbours (chi2 /
Mahalanobis distance) in a COSMOS reference sample, weighted by distance and a COSMOS-structure smoothing weight, with a
log-normal SED-amplitude prior (mu = 0.04, sigma = 0.2, about +/-1.5 mag) that lets the target reach brighter/more massive
objects than the reference ([Hartley+26](papers/hartley.md), p. 4-6, 9-10; [Enia+26](papers/enia.md), p. 5-6). The reference
sample is COSMOS2020 CLASSIC (723 896 objects after flags; Euclid photometry at ~1/3 of final depth), with "truth" photo-z from
Phosphoros (33 Ilbert+09 templates) and, for physical parameters, BC03 fixed-redshift fits with 50 samples per object; the
wide physical-parameter version is cut at H_E < 24 or I_E < 25 (Enia+26, p. 5-6), the photo-z one at I_E < 26 or H_E < 25 (Hartley+26, p. 9; see section 9). **Input photometry** = MER `FLUX_<band>_2FWHM_APER`
(circular aperture of diameter 2 x FWHM of the worst-PSF image) converted to pseudo-total flux with the Kron flux of the detection
band, F_tot,band = FLUX_DETECTION_TOTAL x F_ap,band / F_ap,det (Enia+26, p. 2-3; Hartley+26, p. 5). Template-based **Phosphoros**
is still used for the QSO, star and NIR-detected-only tables (QSO+host z <= 6; NIR sources up to z = 10 wide / 12 deep, with
P(z > 6)) (Hartley+26, p. 7-8). zPDFs are smoothed with sigma_z = 0.02; PHZ software version 2.16.13 ([Ruffenach+26](papers/ruffenach.md), Table E.1).

## 2. Data groups and tables

PHZ/SPE/SIR tables are organised by four data groups (archive help, `Catalogues.md`): **wide** (EWS "wide survey" plus all other
wide-like data such as SelfCal, EMDS, ancillary fields), **deep_survey** (stacked EDF-N/F/S), **deep_mode** (CDFS and COSMOS
inside EDF-F) and **deep_visits** (every individual visit of the EDFs at EWS depth; objects may reappear with different or even
identical `object_id`). MER has five groups (`wide_survey`, `wide_mode`, ...) but PHZ merges the two wide ones into `wide`
(archive help; TAP lists no `phz_*_wide_survey` table). Where the archive help says "deep" is the combination of deep survey and
deep mode, the TAP schema still lists them separately (see section 9, discrepancy 6).

| TAP table (suffix `_wide`, `_deep_survey`, `_deep_mode`, `_deep_visits`) | Content | Columns (wide / deep) | Groups present |
|---|---|---|---|
| `dr1.phz_photo_z_<g>` | photo-z PDF + statistics, flags, tomography, UNIF fluxes | 68 / 48 (deep_visits 68) | all four |
| `dr1.phz_classification_<g>` | star/galaxy/QSO/GC probabilities, thresholds, bit-coded class, `missing_band`, `vis_det` | 20 | all four |
| `dr1.phz_physical_parameters_<g>` | galaxy M*, SFR, Av, SFH, absolute magnitudes (median, mode, 68 %) | 81 | all four |
| `dr1.phz_nir_physical_parameters_<g>` | Phosphoros fit for NIR-detected sources (z PDF, best SED, `high_z_prob`) | 64 / 72 | all four |
| `dr1.phz_qso_physical_parameters_<g>` | Phosphoros QSO fit (best z, SED, E(B-V), z PDF) | 63 / 71 | all four |
| `dr1.phz_star_template_<g>` | Phosphoros star-template fit | 62 / 70 | all four |
| `dr1.phz_galaxy_sed_<g>`, `dr1.phz_star_sed_<g>` | 55 x 100 A top-hat flux bins, 450-1000 nm, uJy, no errors in DR1 | 127 | **`wide` and `deep_visits` only** |
| `dr1.phz_catalogue`, `_deep`, `_l3` | file-level metadata (paths, tile_index_list, release), not source rows | 27 | n/a |

Table list from [tap/README.md](data_model/tap/README.md). Deep (`deep_survey`, `deep_mode`) photo-z tables omit the HSC, LSST,
MegaCam and Pan-STARRS UNIF flux columns present in wide/deep_visits (DECam only). Deep NIR/QSO/star tables add HSC r, r2, i, i2 total flux columns.
The DPDD "sampled physical parameters" binary files (50 posterior samples, Deep only; Enia+26, p. 6) and the DPDD tables
`PHYSPARAMQAGN`, `GLOBULARCLUSTERCAT` have **no TAP table** (not found in the dump; how to retrieve the samples is unknown).
Only the DPDD documents the `DpdBinMeanRedshift`, `PHZCoAddedPDZBiasMap` and analysis-result products as absent from DR1-Foundation (DPDD).

All tables carry `object_id` (long, = MER id), `patch_id_list`, `calblock_id_list` and `data_set_release*`; **none has a `tile_index`
column**, so filter by tile or position through the MER table (`tile_index`, indexed) (TAP dump).

## 3. Key columns

### 3.1 `phz_photo_z_*`

| Column | Meaning | Note |
|---|---|---|
| `phz_median` | median of the zPDF; **default point estimate** and the quantity validated in the paper | (Hartley+26, p. 6, 14) |
| `phz_70_int`, `phz_90_int`, `phz_95_int` | smallest PDF interval with 70/90/95 % probability; **2-element arrays** (lower, upper) | verified; array columns need care in TAP/VOTable |
| `phz_pdf` | **601 values, z = 0-6, step 0.01** | verified; not in the default downloads of a plain `SELECT *` for large samples (size) |
| `phz_mode_1`, `phz_mode_1_area` | mean of the most probable zPDF peak after peak decomposition, and its area | (Hartley+26, p. 6) |
| `phz_mode_2` (`phz_mode_2_area`) | **meaning disputed**, see section 9 (Hartley: mean z of the zPDF of the single closest neighbour; DPDD: global maximum a posteriori; TAP: "second mode"); `_area` is "not used" (DPDD) | neither "mode" is a true mode (Hartley+26, p. 6); avoid |
| `phz_flags` | processing flag, section 4 | |
| `phz_weight`, `ie_cuts_weights` | probability to be a usable source at I_E = 23.5, and at I_E = 20.25/21.25/22.25/24.5 (4-vector) | weak-lensing/clustering weights; (DPDD) |
| `photometric_system` | encodes the available band set (and number of missing bands) | values seen in one wide tile: 20 (most), 21, 22, 23, -99 *(checked)*; code table not documented |
| `best_chi2` | chi2 of best neighbour | use to reject poor matches (DPDD, inference) |
| `bias_id`, `tom_bin_id`, `alt_tom_bin_id`, `pos_tom_bin_id`, `flag_som_*` | tomography and bias-map identifiers for cosmology | `DpdBinMeanRedshift` not in DR1-Foundation (Hartley+26, p. 3, 8) |
| `flux_*_unif`, `fluxerr_*_unif` | **unified** fluxes (uJy): reddening-corrected, standardised to the DECam filter set (u, g, r, i, z) plus VIS, Y, J, H | galaxies only, no error propagation; do not mix with MER fluxes in colours (Hartley+26, p. 6-7) |

### 3.2 `phz_classification_*`

`phz_star_prob`, `phz_gal_prob`, `phz_qso_prob`, `phz_glob_cl_prob` (probabilities); `star_threshold`, `galaxy_threshold`,
`qso_threshold`, `globc_threshold` (per-object acceptance thresholds); `phz_classification` (accepted class); `missing_band`
(names of missing photometry); `vis_det`; `configuration` (= `photometric_system`). Class thresholds are tuned for cosmology
(complete galaxies, pure stars at S/N > 50), so re-threshold for your use (Hartley+26, p. 5). The QSO catalogue definition
is "not a star" and MUMAX_MINUS_MAG < -2.6 (Hartley+26, p. 5). Validation against DESI in EDF-N: 93 % of DESI stars pass the
strict PSF-star threshold; all but 49 (0.2 %) of 29 436 DESI galaxies are classified galaxy (58 also star); 99 % of compact DESI QSOs are
"not star" (Hartley+26, p. 19).

### 3.3 `phz_physical_parameters_*` (galaxies)

For each parameter X three columns: `phz_pp_median_X`, `phz_pp_mode_X`, `phz_pp_68_X` (2-element lower/upper). X in
`redshift`, `stellarmass` (log10 M*/Msun), `sfr` (log10 Msun/yr), `massformed`, `stellarmetallicity` (Z/Zsun), `sfhage`, `sfhtimescale`
(Gyr), `av` (mag), `luminosity` (solar luminosities, undocumented in DPDD; added in the archive) and 13 absolute magnitudes
`mfuv, mnuv, mu, mb, mv, mr, mi, mz, mvis, my, mj, mh, mks`. Other columns: `phz_pdf_nn_id/_weight/_scale` (the 30 neighbours: IDs, weights, amplitude
scalings, enough to rebuild a posterior with the reference-sample samples), `phys_param_flags`, `quality_flag`, `imf`, `sfhtype`
(integer codes without code table) (TAP dump; [Enia+26](papers/enia.md), p. 4). IMF is Chabrier, AB magnitudes (Enia+26, p. 2).
Verified on tile 102021980: stellar mass is log10 M*/Msun (values 8.5-11.9 for bright galaxies) and M_VIS negative absolute
magnitudes (-20 to -24) *(checked)*. **Not in the archive although in the DPDD**: `SCALING`, `AGNEBV`, `AGNLBOL`, `AGNLUMFRAC`, `DUSTLAWHEIGHT/SLOPE/WIDTH`
(median/mode/68 each), `GALAXYCLASS` (archive help `Some_columns_described_in_the_DPDD_are_not_available_in_the_archive`).
AGN and QSO are not modelled by the galaxy fit (Enia+26, p. 3).

### 3.4 NIR-based, QSO and star tables

`phz_nir_physical_parameters_*`: Phosphoros on NIR-detected sources (about 1/4 of EWS objects are NIR-detected only,
Hartley+26, p. 7): `z`, `z_1d_pdf`, `z1dpdf_peak_z`, `high_z_prob` (P(z > 6)), `sed`, `sed_index`, `reddeningcurve`, `e_b_v_`, `scale`,
`posterior_log`, `likelihood_log`, `region_index`, and the `flux_*_total_corrected` inputs. `phz_qso_physical_parameters_*` has the
same layout (QSO + host, Salvato+09 templates, SMC reddening E(B-V) <= 0.04, z step 0.05; Hartley+26, p. 7-8).
`phz_star_template_*` has the same Phosphoros columns for stellar templates (Serrano+24 synthetic SEDs).
`missing_data_flag`, `reference_luminosity` are undocumented in the DPDD (archive help `Missing_column_descriptions_in_the_DPDD`).

## 4. Flags and recommended selections

| Flag | Documented | Seen *(checked 2026-11-13, tile 102021980, ~111 000 rows)* |
|---|---|---|
| `phz_flags` | DPDD: 0 OK; 1 NNPZ no close neighbour (weight > 1e-3); 10 not VIS-detected; 11 missing band; 12 too faint. TAP: "bitwise ... +1 no close neighbor, +2 incomplete set of flux" (text truncated) | (rows with positive Kron flux) values 0 (62 412, all `vis_det` = 1), 12 (26 733, all VIS-detected, mean I_E(Kron) 25.9, brightest 22.7), 10 (22 925, all `vis_det` = 0), 1 (103, mean I_E 16.5, brightest 12.8), 11 (28): **decimal codes, as in the DPDD; no 2, 3, 4...** |
| `phz_classification` | DPDD: OR-able bits 1 star, 2 galaxy, 4 QSO, 8 globular cluster. TAP: 1 galaxy, 2 star (swapped) | values -1, 0, 1, 2, 3 only (class 2: 108 860 of ~111 000 rows; no 4 or 8): 1 star, 2 galaxy, 3 both, 0 neither, -1 unexplained; QSOs are **not** a class value, use `phz_qso_prob` (1 = star, 2 = galaxy verified in [verified_on_archive.md](data_model/verified_on_archive.md)) |
| `phys_param_flags`, `quality_flag` | DPDD "TBD"; Enia: 0 = at least one neighbour with weight > 1e-3 ([Enia+26](papers/enia.md), p. 3) | only 0.0 and 1.0 occur (110 764 vs 1 480 rows in the physical-parameter table of that tile), the two columns agree; 1 = no usable neighbour |
| `flag_som_*_tomobin` | 1 = calibratable SOM-cell/bin | cosmology only |

Recommended selections (from the papers; **bold** = low-z modification, inference):

| Purpose | Selection |
|---|---|
| clean galaxy sample for statistics | `phz_classification = 2`, `phz_flags = 0`, `phys_param_flags = 0`, MER `vis_det = 1`, `spurious_flag = 0`, `det_quality_flag < 4`, `mumax_minus_mag > -2.6` (compactness cut) ([Enia+26](papers/enia.md), p. 3; [Dunn+26](papers/dunn.md), p. 17) |
| consistency of redshifts | `abs(phz_pp_median_redshift - phz_median) < 0.2` (Dunn+26 cut); note this is loose compared with the NMAD 0.02-0.04 |
| stellar-mass-limited samples | apply the Pozzetti-type completeness limits of Enia+26 Fig. 8 (95 % complete: log M* ~ 8 at z ~ 0.1, ~9.0-9.3 at z ~ 1 for EDFs; EWS higher; passive galaxies +0.4-0.6 dex; 5-sigma limit lowers by 0.30 dex) |
| area-dependent work | use the VMPZ photometric visibility mask ([Odier+26](papers/odier.md)); per-object `EFF_COV` |
| **bright extended low-z targets** | **do not require `phys_param_flags = 0` blindly** (it removes most of them, section 5.3); keep `phz_flags` in {0, 1}, inspect `phz_70_int`/`phz_pdf`, and prefer external spec-z and your own masses |
| faint end | prefer I_E < 24 or H_E < 22 to obtain the stated quality; expect ~20 % outliers at I_E < 24.5 ([Hartley+26](papers/hartley.md), p. 14) |
| shear/clustering-like use | `phz_weight` or the `ie_cuts_weights` entry nearest to your magnitude limit (DPDD) |

Archive caveats: empty values in `point_like_prob`, `flux_{y,j,h}_2fwhm_aper` and errors are stored as NaN, not NULL: use
`NULLIF(point_like_prob, 'NaN') < 0.1` (archive help `Empty_values_in_catalogues_are_mistakenly_treated_as__NaN_`).

## 5. Performance

### 5.1 Photo-z versus magnitude and region

Metrics (Hartley+26, p. 13): dz = (z_phot - z_spec)/(1 + z_spec); outlier |dz| > 0.15; NMAD = 1.48 x median|dz - bias|. Spec-z truth is a
compilation (Saulder+ in prep.) weighted to mimic flux-limited samples; it is biased bright and a lower-limit test (some DESI/PRIMUS values wrong).

| Sample (point estimate `phz_median`) | Outliers | NMAD | sigma68 | Source |
|---|---|---|---|---|
| EWS-like EDF-F, 17 < I_E < 24.5 | 20.2 % | 0.072 | 0.094 | Hartley+26, Table 2, p. 14 |
| COSMOS EWS-like, 17 < I_E < 24.5 (COSMOS2020 truth) | 21.8 % | 0.080 | 0.106 | same |
| 17 < I_E < 24: north with u / north without u / south | 13.1 / 18.5 / 12.5 % | 0.054 / 0.066 / 0.054 | 0.068 / 0.090 / 0.065 | same |
| 17 < H_E < 22: N with u / N without u / S | 7.1 / 9.1 / 7.6 % | 0.038 / 0.044 / 0.039 | 0.043 / 0.050 / 0.044 | same |
| 22 < H_E < 23.5: N with u / N without u / S | 19.2 / 28.6 / 19.1 % | 0.068 / 0.098 / 0.076 | | same |
| deep (unweighted, H_E < 25.5): EDF-N / EDF-F / AUX | 4.1 / 6.8 / 4.0 % | 0.033 / 0.035 / 0.018 | 0.037 / 0.040 / 0.022 | Hartley+26, Table 3, p. 15 |

Enia+26 (Table 4, p. 9; Qf = 4 spec-z, outlier |dz| > 0.15; sigma_NMAD / outlier / bias):

| Field | all | bright I_E 15-21.5 | mid 21.5-23 | faint 23-25 |
|---|---|---|---|---|
| EWS-N (EWS-like EDF-N, 19 291) | 0.021 / 3.7 % / +0.01 | 0.017 / 0.4 % | 0.022 / 3.8 % | 0.034 / 9.4 % |
| EWS-S (EWS-like EDF-F, 52 582) | 0.027 / 7.6 % / 0.00 | 0.024 / 4.4 % | 0.025 / 7.2 % | 0.048 / 16.2 % |
| PV-005 COSMOS (27 574) | 0.012 / 5.5 % / 0.00 | 0.010 / 1.8 % | | |

The two papers differ by a factor of ~2-3 in NMAD at similar magnitude (e.g. Enia EWS-S all 0.027 vs Hartley EWS-like 0.072 for 17 < I_E < 24.5): different spec-z
samples, weighting and magnitude limits ("Qf = 4" spec-z are bright), so quote the paper whose sample resembles yours. Improvement over Q1:
NMAD ~0.03 to ~0.02 and ~10 % fewer catastrophic outliers; a group at z_spec ~ 0.6, z_phot ~ 0.2 largely removed (Enia+26, p. 8-9; Hartley+26, p. 15).
zPDF calibration: PIT broadly flat in the EWS, Frac68 near 0.68 at all magnitudes; worst case north without u (KL 0.075 at I_E < 24) (Hartley+26, p. 15-16).

### 5.2 Low redshift (z < 0.5): what is known and what is not

- **No metric binned in redshift is published.** The Hartley+26 figures (5, 8) are z_phot-z_spec scatter plots; the statistics above are dominated by 0.3 < z < 1
  ([Hartley+26](papers/hartley.md) summary). Treat the bright-bin numbers (NMAD 0.017-0.04) as an upper bound on the quality at z < 0.3.
- **Reference-sample limits** (Hartley+26, p. 19; Enia+26, p. 5): COSMOS is 2 deg2 and was chosen to avoid low-z structure, so z < 0.2 galaxies, z < 0.4 very massive galaxies and
  bright objects are almost absent; the amplitude prior is clipped at +/-1.5 mag, so bright nearby galaxies cannot be matched to faint references. Mitigation = augmentation (< 1 % of the
  sample: z < 0.1, 16 < i < 18, boosted SED amplitudes) and a redshift prior (weights truncated 0.25-4), "unfortunately not as effective as we would have liked": redshifts mostly reasonable,
  **stellar masses and other amplitude-dependent properties biased low** (Hartley+26, p. 10, 19). Enia+26 gives no stellar-mass validation at z < 0.2.
- **Redshift focussing / aliasing** at COSMOS over-densities (z ~ 0.35, also 0.7 and 0.9): point estimates cluster; use the zPDF or wide bins for narrow-z slices (Hartley+26, p. 10, 19).
- **Best low-z test available**: ~5000 DESI galaxies at 0 < z < 0.6; SFR (PHZ vs Halpha/Hbeta Kennicutt98) NMAD 0.505 dex, 15.9 % outliers (> 0.8 dex), no bias in EWS-N; EDF-N deep 0.513 dex / 17.1 %;
  outliers are mostly low-z galaxies placed at high z (Enia+26, p. 9-10). Stellar-mass completeness 95 % at log M* ~ 8 at z ~ 0.1 in the EDFs, higher in EWS (Enia+26, Fig. 8, p. 12).
- Classification at low z: all but 0.2 % of DESI galaxies are classed galaxy; compact low-mass dwarfs are removed by the compactness cut used in all validation samples (Enia+26 p. 3, 11).
- **North without u**: +5 points outliers and +20 % scatter at I_E < 24; zPDF calibration worst there (Hartley+26, p. 14-16). u exists only for about half of the north (Hartley+26, p. 5, 19; [Enia+26](papers/enia.md), Table 1). A no-u variant run exists but is *not* published in DR1-Foundation.
- **Deep fields**: a configuration error (2 % systematic flux error interpreted as a variance in the EWS; no systematic error at all in the deep pipeline) makes deep zPDFs over-confident: ~15 % "truth outside the PDF" (PDF outliers 14.6-17.5 %, KL 0.05-0.09)
  (Hartley+26, p. 6, 8, 16-17); **Enia+26 (p. 10) reports a mild PDF over-estimation in the deep fields with its own metric**: widen deep PDFs or allow ~15 % outliers (DR2 will fix).
- Filter-bandpass variation across the field of view is not corrected in DR1; UNIF fluxes and SEDs have no uncertainties; the zero-point offset table in the second PHZCAT extension is diagnostic only and not applied (Hartley+26, p. 3, 6-7, 27).

### 5.3 Archive check on bright galaxies *(checked 2026-11-13, wide tile 102021980, `phz_classification = 2`, `flux_detection_total` > 229 uJy, i.e. Kron I_E < 18)*

| `phz_flags` | `phys_param_flags` | N | `phz_median` range (mean) | median-z from physical-parameter fit (mean) | log M* mean (range) |
|---|---|---|---|---|---|
| 1 | 1 | 102 | 0.05-1.69 (0.10) | 0.09 | 10.6 (9.9-11.7) |
| 0 | 1 | 87 | 0.01-0.53 (0.14) | 0.18 | 10.8 (9.1-11.9) |
| 0 | 0 | 4 | 0.06-0.17 (0.09) | 0.07 | 9.0 (8.5-9.6) |
| 10 | 1 | 57 | 0.01-0.97 (0.09) | 0.08 | 10.6 (9.7-10.8) |
| 11 | 1 | 5 | 0.07-0.08 | 0.08 | 10.7 |
| 10 | 0 | 1 | 0.08 | 0.08 | 10.2 |

Single tile, one magnitude cut: a pointer, not a statistic. Most bright objects are flagged (pp flag = 1) even when `phz_flags` = 0, the objects span z ~ 0.01-0.5 and log M* 9-12; objects with the
flag set still have values in the columns (they come from the nearest neighbours). The brightest objects have very large Kron radii (66-870 px in the 8 rows of the example query, section 8), so blending or shredding of large galaxies is likely and some `phz_*` rows may belong to fragments (not checked object by object; see NGC 1483 in [verified_on_archive.md](data_model/verified_on_archive.md)).

## 6. Comparison with external surveys and codes

| Comparison | Result | Source |
|---|---|---|
| compiled spec-z (DESI, PRIMUS, COSMOS/VUDS etc.) | Table 2 above; the spec-z compilation is Saulder+ (in prep.) and COSMOS Khostovan+26; not distributed as an archive table (no such table in `all_tables.csv`) | Hartley+26, p. 13-14; Enia+26, p. 7 |
| COSMOS2020 LePhare photo-z (EAF) | reference-sample agreement: EWS version NMAD 0.020 / 10.6 %, EDF version 0.039 / 19.1 %; vs spec-z (Qf = 4) the reference "truth" has NMAD 0.007, 2.3 % outliers | Enia+26, Fig. 3, p. 7 |
| CANDELS / DES-DF / UDS deep photo-z | deep NMAD 0.02-0.03 matches | Hartley+26, p. 15 |
| DESI classification (EDF-N) | numbers in section 3.2 | Hartley+26, p. 19 |
| Gaia XP spectra (stars) | fractional mean-wavelength bias 1.5e-4 to 5.7e-4 in the south (requirement 5e-4), up to -2.4e-3 for red low-reddening stars in the north | Hartley+26, Table 4, p. 18 |
| MUSYC medium bands (galaxy SEDs, CDFS) | 3-sigma-clipped mean-wavelength bias 2.0e-3 to 5.0e-3, worse with z, ~10x the end-of-mission requirement | Hartley+26, p. 18 |
| DESI Halpha SFR (0 < z < 0.6), 3D-HST SED SFR (GOODS-S) | NMAD 0.505 dex / 15.9 %; 0.419 dex / 16.0 %, bias -0.12 dex | Enia+26, p. 9-10 |
| Prospector (ECLIPSE-D lenses, same photometry and redshift) | Prospector masses 0.23 dex higher and SFR 0.55 dex lower than NNPZ; NNPZ SFR unrealistically high (> 100 Msun/yr) for some massive lenses; Salpeter IMF there (Chabrier/Kroupa -0.2 to -0.25 dex) | [Nersesian+26](papers/nersesian.md), p. 7, 11, 23-24 |
| MER total fluxes vs COSMOS2025 SED predictions | within ~10 %, a few percent high; template fitting best in NISP | [Gasparetto+26](papers/gasparetto.md) |
| Star-forming main sequence | follows Popesso+23 / Daddi+22 / Enia+26 at 0.2 < z < 1.5 (~0.1-0.2 dex above at high z) | Enia+26, Fig. 7, p. 11 |

## 7. Known issues (summary)

1. Reference sample COSMOS-only: z < 0.2, massive (z < 0.4) and bright galaxies disfavoured; masses biased low (Hartley+26, p. 19).
2. Amplitude prior clipped at +/-1.5 mag; redshift focussing (z ~ 0.35); configuration error on the systematic flux error (EWS) / missing (deep) (Hartley+26, p. 6, 16, 19).
3. North: u band on half the area; Pan-STARRS i-band mosaics with residual artefacts (no outlier rejection); the affected areas are flagged in a HEALPix map of the VMPZ-ID package ([Odier+26](papers/odier.md); [Aussel+26](papers/aussel.md), p. 6).
4. Photometry basis is 2xFWHM aperture colours, not model/total colours; the pseudo-total flux inherits any Kron-flux error (`det_quality_flag`) and any deblending error of the MER catalogue (shredded large galaxies).
5. UNIF photometry and galaxy SEDs: galaxies only, no uncertainties (Hartley+26, p. 6-7); stellar SEDs ~2x requirement in the north.
6. ~1 % of area lost to tiny/incomplete tiles; 0.5 % of tiles fail PHZ-specific tests (Hartley+26, p. 12-13); SFR good to no better than ~0.5 dex per galaxy (Enia+26).
7. AGN/QSO not in the galaxy fit; the PHZ M*/SFR of AGN hosts is unreliable (Enia+26, p. 3).
8. DPDD columns missing in the archive (section 3.3) and codes without tables (`imf`, `sfhtype`, `photometric_system`).

## 8. ADQL: MER + PHZ join

Tested 2026-11-13 on the public TAP sync endpoint (anonymous, `TOP 8`, tile 102021980; ~3.5 s). Magnitude conversion uses the catalogue zero point 23.9 (uJy to AB). Omitting `ORDER BY` and using inner joins avoided a
sync-timeout seen with `LEFT OUTER JOIN` + `ORDER BY` on the same tile (use async jobs for larger samples).

```sql
SELECT TOP 8
       m.object_id, m.right_ascension, m.declination, m.tile_index,
       -2.5*LOG10(m.flux_detection_total) + 23.9 AS i_e_kron_mag,
       m.flux_vis_2fwhm_aper, m.flux_h_2fwhm_aper, m.kron_radius, m.point_like_prob,
       p.phz_median, p.phz_flags, p.phz_classification, p.phz_weight,
       q.phz_pp_median_redshift, q.phz_pp_median_stellarmass, q.phz_pp_median_sfr,
       q.phz_pp_median_av, q.phz_pp_median_mvis, q.phys_param_flags
FROM dr1.mer_catalogue_wide_survey AS m
JOIN dr1.phz_photo_z_wide AS p ON p.object_id = m.object_id
JOIN dr1.phz_physical_parameters_wide AS q ON q.object_id = m.object_id
WHERE m.tile_index = 102021980
  AND m.vis_det = 1 AND m.spurious_flag = 0 AND m.det_quality_flag < 4
  AND m.flux_detection_total > 229          -- Kron I_E < ~18
  AND p.phz_classification = 2
```

Notes. (a) For all other groups swap the suffix: `mer_catalogue_deep_survey` + `phz_photo_z_deep_survey` + `phz_physical_parameters_deep_survey`, same column names (untested here).
(b) `kron_radius`, `semimajor_axis`, `flux_radius` are in pixels (0.1"); `point_like_prob` may be NaN, use `NULLIF(m.point_like_prob, 'NaN')`. (c) Position cone searches go through the MER table
(`INTERSECTS(CIRCLE('ICRS', m.right_ascension, m.declination, 0.01), ...)` pattern from the archive ADQL help; not tested here) because PHZ tables carry no coordinates. (d) Selecting `phz_pdf` (601 doubles per
row) is possible but heavy: restrict to a small list of `object_id`s. (e) Every PHZ product of one object joins one-to-one on `object_id`; deep-visits `object_id` may repeat across visits ([verified_on_archive.md](data_model/verified_on_archive.md), archive help).

## 9. Contradictions between sources

| # | Topic | Sources | Resolution / note |
|---|---|---|---|
| 1 | `phz_classification` codes | TAP: +1 galaxy, +2 star; DPDD and verified: 1 star, 2 galaxy | verified wins; DPDD "bits 4 = QSO, 8 = GC" not seen: only -1, 0, 1, 2, 3 *(checked, one tile)* |
| 2 | `phz_mode_2` | DPDD: global max a posteriori; TAP: "second mode"; Hartley+26, p. 6: mean of the zPDF of the closest neighbour | use `phz_median`; do not use mode_2 |
| 3 | `phz_flags` | DPDD decimal values (1, 10, 11, 12); TAP bitwise (+1, +2 ...) | decimal values observed *(checked)* |
| 4 | physical-parameter columns | DPDD lists 28 parameters incl. SCALING, AGN*, DUSTLAW*, GALAXYCLASS; archive has `luminosity` instead and lacks those | archive help page confirms the omission |
| 5 | deep zPDF calibration | Hartley+26: under-dispersed (~15 % outliers); Enia+26: mild PDF over-estimation | different truth samples/metrics; treat deep zPDFs with care |
| 6 | PHZ deep tables | archive help (`Catalogues.md`): "deep" = deep survey + deep mode combined; TAP lists `_deep_survey` and `_deep_mode` separately | query both |
| 7 | spec-z accuracy statistics | Hartley Table 2 (NMAD 0.072 at I_E < 24.5) vs Enia Table 4 (0.027) | different samples and magnitude ranges |
| 8 | DPDD says Phosphoros config input; NNPZ is the core photo-z | DPDD vs Hartley+26 | consistent: Phosphoros for labels, QSO, star, NIR tables |
| 9 | wide reference-sample cut | Hartley+26, p. 9: I_E < 26 or H_E < 25; Enia+26, p. 5-6: 374 829 galaxies, H_E < 24 or I_E < 25 | possibly different reference versions (core vs physical-parameter); unresolved |

## 10. Advice for a low-to-intermediate-z extended-galaxy programme

1. **Redshift**: for z < 0.3 and for galaxies with I_E < 18-19 use **external spec-z** (DESI DR1, SDSS, GAMA, 6dF, etc.) wherever it exists; cross-match externally by position
   (DESI-in-archive is not found in the TAP dump). Euclid SPE (slitless) is poor at z < 0.84 ([08_spectroscopy.md](08_spectroscopy.md)), so it does not replace this.
   If only PHZ exists: take `phz_median` with `phz_70_int`; do not trust narrow z slices (focussing at z ~ 0.35); check `phz_median` against `phz_pp_median_redshift` and `phz_pdf` multimodality.
2. **Which photometry for masses**: PHZ masses use 2xFWHM aperture colours (PSF of the worst band, ~1" ground-based, i.e. a 2" aperture) scaled to the Kron total of the detection band. For galaxies much larger than the aperture
   with colour gradients this gives the central colour, not the global one; for shredded or blended galaxies the Kron flux is a fragment's. To get masses of extended galaxies: take your own total (model) fluxes in VIS and NISP
   (and ground bands), run your own SED fit (Prospector-like; Nersesian+26 gives workable priors and a 2 % floor + ~0.07 mag model-error recipe), or **rescale the PHZ mass by log(F_total,yours / F_total,MER)**
   (valid to first order only if the colour is unchanged; inference, not a documented procedure; NNPZ rescales neighbour masses by the amplitude factor, Enia+26, p. 5-6). Nersesian+26 find the 4xFWHM aperture
   gives better photo-z than 1xFWHM or total on 73 lenses (NMAD 0.030 vs 0.051 / 0.041), another sign that aperture choice matters (p. 21).
3. **Aperture vs total for colours**: use MER `flux_<band>_templfit`/`flux_<band>_sersic` or your own forward-modelled photometry for global colours; use `flux_*_4fwhm_aper` only as a local-colour check. Do not use UNIF fluxes as total colours of large galaxies.
4. **Mass and SFR systematics**: add at least 0.2-0.3 dex (inference) for z < 0.2 or log M* > 11 PHZ masses and treat them as lower limits; SFR scatter ~0.5 dex (Enia+26); IMF Chabrier (shift by about +0.2 dex to compare with Salpeter).
5. **Selecting extended galaxies**: `phz_classification = 2` and `phz_gal_prob` high, but also MER `point_like_prob`, `mumax_minus_mag`, `spurious_flag`, `det_quality_flag`; large nearby galaxies with bright nuclei can be double-classed (class 3); the classification thresholds were tuned for cosmology.
6. **Footprint**: use VMPZ masks for area/density work; check EXT coverage (u band, Pan-STARRS-affected north) through `photometric_system` / `missing_band`.
7. **Deep fields**: widen zPDFs (~15 % outliers); EDF-S validation is nearly empty (74 spec-z; Enia+26); use deep_visits tables only with duplicates handled.
8. **Do not** use PHZ SEDs/UNIF for stars, the zero-point table as calibration, or PHZ products as a substitute for dedicated structural measurements (no profile, bulge/disc or outskirts information; see [Dunn+26](papers/dunn.md) for how DR1 Sersic quantities are used with these cuts).

## 11. References (KB summaries)

[Hartley+26](papers/hartley.md) (pipeline, validation) - [Enia+26](papers/enia.md) (physical properties) - [Dunn+26](papers/dunn.md) (selection recipe using PHZ + MER Sersic cuts) -
[Nersesian+26](papers/nersesian.md) (Phosphoros/Prospector for lenses) - [Odier+26](papers/odier.md) (masks) - [Aussel+26](papers/aussel.md), [Ruffenach+26](papers/ruffenach.md) (context) -
DPDD: [dpdd_phz.md](data_model/dpdd_phz.md), [dpdd_masks_vmpz.md](data_model/dpdd_masks_vmpz.md) - TAP dumps `data_model/tap/dr1.phz_*.md`.
