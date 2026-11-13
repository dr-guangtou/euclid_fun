---
title: "Euclid Data Release 1 (DR1): The PHZ processing function for the physical properties of galaxies"
short_name: enia
first_author: Enia
series: A&A Special Issue DR1-Foundation (Nov 2026)
local_pdf: ~/Desktop/euclid/papers/enia.pdf
local_text: ~/Desktop/euclid/text/papers/enia.txt
topics: [physical parameters, stellar mass, SFR, NNPZ, photo-z, COSMOS2020 reference sample, SED fitting, absolute magnitudes, star-forming main sequence, mass completeness, DR1-Foundation]
relevance_extended_galaxies: medium
---

# PHZ physical properties of galaxies in DR1 (Enia et al. 2026)

## TL;DR
Describes the non-cosmology branch of the PHZ pipeline for DR1: for each source, NNPZ takes the 30 nearest neighbours in a COSMOS reference sample (Euclid + ground-based photometry, labels from COSMOS2020 SED fitting) and returns photo-z, stellar mass, SFR, dust, SFH parameters and absolute magnitudes with percentile statistics. Photo-z quality at EWS depth is NMAD ~0.02-0.03 with 4-8% outliers (spec-z samples); SFRs vs DESI emission lines scatter ~0.5 dex with ~16% outliers. For our group this is the source of M*, SFR and rest-frame magnitudes used to select galaxies and set physical sizes, but it is built on aperture (2FWHM) colours scaled to Kron total flux, so it carries no structural information, and the parent paper (hartley.md) warns that mass is biased low for the lowest-z and most massive galaxies.

## Key facts and numbers
- DR1 totals: 880 955 708 unique detected sources, 850 146 468 in the EWS and 30 809 240 in the EDFs; ~9000 tiles; ~1900 deg2 (p. 2). EWS tiles 32' x 32'; EAF/EDF tiles 17' x 17' (p. 2).
- Depths (Table 1, 10 sigma, extended source in 2xFWHM aperture; 5 sigma is about +0.75 mag deeper) (p. 2): EWS / EDF-N / EDF-F / EDF-S / PV-005 / CDFS: IE 24.8 / 26.2 / 24.9 / 25.8 / 26.2 / 26.4; YE 23.2 / 24.5 / 23.4 / 24.3 / 24.7 / 24.8; JE 23.3 / 24.7 / 23.5 / 24.4 / 24.8 / 25.0; HE 23.3 / 24.7 / 23.5 / 24.4 / 24.8 / 25.0. EWS ground-based: u(CFHT) 23.2 (only about half of EWS-N), r(CFHT) 24.0, i(PS1) 23.6, g(HSC) 24.5, z(HSC) 23.0, DECam g 24.7, r 24.3, i 23.8, z 23.0. Field areas: EDF-N ~20 deg2, EDF-F ~10, EDF-S ~20, PV-005 ~1, CDFS ~0.1.
- Number of Euclid passes in DR1: EDF-F 2 (about +0.4 mag over EWS), EDF-S 10 (about +1 mag), EDF-N 11 (p. 2, 10).
- Cosmology: Planck 2016; Chabrier IMF; AB mags (p. 2).
- NNPZ: k = 30 neighbours, weights from chi2 distance; log-normal prior on SED amplitude scaling (in Q1 this was free, giving unphysical M* > 1e14 and SFRs 1e3-1e4 Msun/yr for low-z galaxies placed at high z) (p. 4-6).
- Reference samples (p. 5-6): EDF version 628 281 galaxies (no magnitude cut, effectively UltraVISTA H limit); EWS version 374 829 galaxies cut at HE < 24 or IE < 25. Labels: 50 redshift draws from the core-science Phosphoros PDZ, then a fixed-redshift Phosphoros run on COSMOS2020 (u-to-K plus first two IRAC channels) with BC03 (2016 update, MILES, plus emission lines) templates; models with log10(age/yr) < 8 removed, dz = 0.01 grid, redshift-dependent age prior.
- Reference-sample quality (Fig. 3, p. 7): vs spec-z (Khostovan+26, Qf = 4): NMAD 0.007, 2.3% outliers, no bias for both EWS (33 269) and EDF (33 543) versions. vs COSMOS2020 LePhare photo-z: NMAD 0.020 / 10.6% outliers (EWS version), 0.039 / 19.1% (EDF version, fainter). >95% of reference sources agree with COSMOS2020 M* within 0.2-0.4 dex and SFR within 1 dex.
- Quality cuts used for validation (p. 3): SPURIOUS_FLAG = 0; DET_QUALITY_FLAG < 4; MUMAX_MINUS_MAG > -2.6 (drops stars/compact); PHZ_CLASSIFICATION = 2; PHYS_PARAM_FLAGS = 0; plus HE magnitude cut such that S/N (2xFWHM aperture) >= 5. Explicitly "not a blueprint" for science.
- Metrics (p. 6): NMAD = 1.48 x median(|dz - bias|); outlier |dz| > 0.15 for z, |dy| > 0.4 dex for stellar mass, > 0.8 dex for SFR; PIT for PDF calibration.
- Photo-z quality by field and IE bin (Table 4, p. 9) - sigma_NMAD / outlier % / bias:
  - EWS-N (EWS-like EDF-N, 19 291 spec-z): all 0.021/3.7%/+0.01; 15<IE<=21.5: 0.017/0.4%; 21.5<IE<=23: 0.022/3.8%; 23<IE<=25: 0.034/9.4%.
  - EWS-S (EWS-like EDF-F, 52 582): all 0.027/7.6%/0.00; bright 0.024/4.4%; mid 0.025/7.2%; faint 0.048/16.2%.
  - EDF-N deep: 0.022/2.8%; bright 0.023/1.6%; mid 0.018/2.5%; faint 0.023/5.5%.
  - EDF-F deep: 0.025/8.0%; bright 0.025/5.6%; mid 0.024/7.6%; faint 0.036/14.2%.
  - EDF-S: only 74 spec-z (none with IE > 23): 0.023/6.8%/+0.01.
  - CDFS (1536): 0.030/5.6%/+0.01; PV-005 COSMOS (27 574): 0.012/5.5%/0.00; bright 0.010/1.8%.
- Improvement vs Q1: NMAD ~0.03 -> ~0.02 and ~10% fewer catastrophic outliers (p. 8-9).
- SFR validation (p. 9-10): vs DESI Halpha/Hbeta (Kennicutt 1998) SFR for ~3000 sources in EWS-N (Fig. 5) sigma_NMAD 0.505 dex, 15.9% outliers (> 0.8 dex), bias 0; EDF-N deep 0.513 / 17.1% / 0; vs 3D-HST SED-fit SFR (GOODS-S) in EDF-F: 0.419 / 16.0% / -0.12 dex. Outliers mostly low-z galaxies misplaced at high z. The DESI comparison sample is ~5000 sources at 0 < z < 0.6 (p. 3), the best low-z test in the paper.
- Stellar mass completeness (Pozzetti+10 method with HE limits; Fig. 8, p. 12): 95% limit rises from log M* ~8 at z ~0.1 to ~9.0-9.3 at z ~1 and ~10-10.3 at z ~2.5-3 for the EDFs; EDF-F ~0.25 dex higher; EWS values higher still (no N/S difference); passive galaxies 0.4-0.6 dex higher than star-forming; going to a 5-sigma limit lowers the curves by 0.30 +/- 0.02 dex.
- SFMS check (Fig. 7, p. 11): four zphot bins [0.2,0.5], [0.5,0.8], [0.8,1.5], [1.5,3.0]; UVJ-selected SFGs follow Popesso+23, Daddi+22, Enia+26 relations well at intermediate z, ~0.1-0.2 dex above at high z. Redshifts good to z ~1.5, still fine to z ~3, degraded only at high sSFR.

## Data products and data model
Output files (Table 2, p. 4). Names as printed in the text extraction (underscores may have been lost: e.g. PHYSPARAM = likely PHYS_PARAM, PPSAMPLINGINDEX = likely PP_SAMPLING_INDEX; check the Explanatory Supplement for exact table/column names):
- PHZCAT: core-science photo-z and PDZs.
- PPSAMPLINGINDEX: indices, weights, scaling factors of the 30 neighbours (compact full-posterior representation).
- PPSAMPLINGFILE: 50 samples from the combined posterior of all neighbours per parameter; released only for Deep processing (p. 6).
- PHYSPARAM: median, mode and 68% interval of every quantity in Table 3.
- PHYSPARAMNIR: Phosphoros photo-z/PDZ for NISP-detected galaxies; PHYSPARAMQSO: same for QSO-classified; CLASSCAT and STARCLASS: classification outputs for galaxies and stars.
- Parameters (Table 3, p. 4), each with median, mode, 68% CI: STELLARMASS (log10 M*/Msun), SFR (log10 Msun/yr), MASSFORMED (log10 Msun, total ever formed), SFHAGE (Gyr, time since onset of SF), SFHTIMESCALE (Gyr, tau of delayed-exponential SFH), STELLARMETALLICITY (Z/Zsun), AV (mag); absolute magnitudes M_VIS, M_[FUV, NUV, U, B, V], M_[R, I, Z], M_[Y, J, H, KS].
- Column names used in dunn.md (verbatim from that paper's selection): PHZ_PP_MEDIAN_REDSHIFT / PHZ_PP_MEDIAN_Z, PHZ_PP_MODE_Z, PHZ_PP_MEDIAN_STELLARMASS, PHZ_PP_MEDIAN_SFR, PHYS_PARAM_FLAGS, PHZ_CLASSIFICATION, PHZ_MEDIAN.
- Flags: PHYS_PARAM_FLAGS = 0 means at least one neighbour with weight > 1e-3; PHZ_CLASSIFICATION = 2 means accepted as galaxy (p. 3).
- Data model is dictated by DMDR1 (Euclid DR1 Data Model) so LE3 products stay compatible (p. 6).
- Input catalogue: MER tile catalogues; photometry = 2 x FWHM circular aperture flux (images degraded to worst PSF among bands), converted to total using Kron-aperture (A-PHOT) flux of the detection image (IE or NIR stack): F_total,band = F_total,det x F_ap,band / F_ap,det (Eq. 1, p. 2-3).
- Recommended footprint: Euclid PhotoZ visibility mask VMPZ (Odier et al. 2026) for statistical work (p. 3).

## Processing and methods
1. Two reference samples (EWS, EDF) built by matching Euclid DR1 COSMOS photometry to COSMOS2020 CLASSIC (p. 5).
2. Core labels: Phosphoros photo-z on u..K bands with 33 interpolated SED models, volume prior (Hartley et al.).
3. PP labels: 50 random redshifts from each PDZ; Phosphoros at fixed z with BC03 templates, adds IRAC ch1-2; so each reference galaxy has 50 correlated (z, M*, SFR, ...) realisations (Fig. 1, p. 4).
4. NNPZ run on target galaxy: 30 neighbours, each with chi2 weight x a COSMOS-structure smoothing weight (Hartley et al.) and an SED amplitude scaling factor (log-normal prior); mass-like parameters are rescaled by the amplitude factor, which lets NNPZ reach masses absent from COSMOS (>= 1e12.5) (p. 5-6).
5. Output = weighted distribution over neighbours and their 50 samples (1500 weighted samples per target), summarised as median/mode/68% interval (p. 4, 6).
6. Validation against spec-z, COSMOS2020, 3D-HST, DESI VAC (Siudek et al. 2024), SFMS and mass completeness. X-ray detected sources removed in EAF comparisons (p. 8).

## Validation and performance
See Key facts for all numbers. Additional points:
- PIT of photo-z PDFs broadly flat in EAFs, EWS-like and deep fields, with mild PDF over-estimation in deep fields (p. 10) (contrast hartley.md, which finds deep zPDFs under-dispersed in its own metric; the two papers use different truth samples and metrics).
- Spec-z validation samples are biased bright/high S/N (Qf = 4 cut), so the quoted NMAD and outlier numbers are mild underestimates for the full population, esp. faint (p. 7).
- Stellar masses and SFR vs COSMOS2020/3D-HST in EAFs are shown as Delta M*, Delta SFR plots (Fig. 4) but without quoted numbers beyond the reference-sample agreement; for EWS no mass truth exists, only SFMS consistency.
- SFR scatter is attributed mostly to broad-band-only SFR inference, plus catastrophic photo-z outliers (low-z to high-z) (p. 9-10).
- Far-IR stacking cross-check by Hill et al. 2026 (Q1) found consistent SFRs for SFMS galaxies (p. 11).

## Known issues, caveats, limitations
- No object-level uncertainty beyond the posterior statistics; only the Deep products carry 50 posterior samples (PPSAMPLINGFILE); in the EWS you must reconstruct posteriors from neighbours (p. 6).
- Reference sample is COSMOS only (2 deg2): risk of imprinting COSMOS structures and of lacking very massive (log M* >= 12.5) and rare galaxies; mitigations = weights and amplitude prior (p. 5). Hartley et al. (p. 19) report that despite these, M* and other amplitude-dependent quantities remain biased low for low-z (< 0.2) and very massive (z < 0.4) galaxies.
- AGN and QSOs are not modelled (galaxy-only SED templates); extended sources assumed to be galaxies; performance on AGN/QSOs not discussed (p. 3).
- Validation sample selection excludes compact sources (MUMAX_MINUS_MAG cut), so statistics do not describe compact/low-mass dwarfs.
- EDF-S validation is nearly empty (74 spec-z), EDF-F only two Euclid passes; EWS performance is inferred from EWS-like passes of EDF-N/EDF-F, not from the EWS itself (p. 8).
- u band exists for only about half of the EWS-N, so performance varies with region (see hartley.md).
- SFR comparisons with DESI are for 0 < z < 0.6 and mainly the north/south region of DESI footprint; Halpha-based SFR itself uncertain (p. 3).
- Internal inconsistency: the conclusions quote 28 118 spec-z galaxies for PV-005, while Fig. 4 and Table 4 give 27 574 (p. 12 vs p. 8-9).

## Implications for extended-galaxy photometry, 2-D modelling and low-surface-brightness work
- Provides M*, SFR, sSFR, AV, SFH age/tau and rest-frame magnitudes (incl. M_VIS, M_[Y,J,H,KS]) for essentially every Euclid galaxy: useful for sample selection, mass-matched comparisons, converting angular to physical size (via the photo-z), and for rest-frame colour-based classification (UVJ). Dunn et al. (dunn.md) use exactly these for 41 million star-forming galaxies.
- Because fluxes are 2FWHM aperture colours scaled to Kron total, the M*/SFR are effectively "colour + total flux" quantities: no PSF-deconvolved profile, no bulge/disc decomposition, nothing about outskirts, tidal features or ICL. Expect M* to be biased for galaxies with strong colour gradients or large extent when the aperture misses the outer disc.
- Low-z (< 0.2) regime: the strongest published check is the ~5000 DESI galaxies at 0 < z < 0.6 for SFR; no stated M* validation at z < 0.2. Reference sample under-represents these galaxies (see Hartley). Mass completeness 95% at log M* ~8 at z ~0.1 for EDFs (higher for EWS).
- Bright-end photo-z: EWS-N 15 < IE <= 21.5 has NMAD 0.017 and 0.4% outliers; EWS-S 0.024 and 4.4%, so bright galaxies are well served on average (but Hartley notes issues at the extreme low-z/high-mass end).
- Useful flag combination to select "clean extended galaxies": SPURIOUS_FLAG = 0, DET_QUALITY_FLAG < 4, MUMAX_MINUS_MAG > -2.6, PHZ_CLASSIFICATION = 2, PHYS_PARAM_FLAGS = 0.

## Practical recommendations for users
- Use the PHZ_PP_* median columns for M*, SFR, redshift; use the 68% limits; inspect the PDFs via PPSAMPLINGINDEX when you need non-Gaussian errors; in deep fields use the 50 samples (PPSAMPLINGFILE).
- Apply PHYS_PARAM_FLAGS = 0 and PHZ_CLASSIFICATION = 2; cross-check consistency of core photo-z (PHZ_MEDIAN) and PP redshift (|diff| < 0.2 is the Dunn et al. cut).
- Use the VMPZ mask for area-dependent work; apply stellar-mass completeness limits from Fig. 8 (95%) and your own HE depth; for passive galaxies add 0.4-0.6 dex.
- Do not trust SFR for individual galaxies better than ~0.5 dex; do not use PP for QSO/AGN hosts without checking the QSO/NIR tables.
- Expect larger errors at IE > 23 (EWS-S faint-bin 16% outliers).
- Do not use PHZ M* for the most massive or lowest-z galaxies without an independent check (see hartley.md).

## Objects, fields and figures worth revisiting
- Fields (no coordinates given): COSMOS and its PV-005 inner pointing (EAF; ~1 deg2), CDFS (sub-field of EDF-F; ~0.1 deg2 here), EDF-N (near North Ecliptic Pole), EDF-F (Fornax cluster region, contains GOODS-S), EDF-S (low Galactic extinction). Example: OBJECT ID 2726366616668607648 in EDF-N, zspec 0.26, zphot 0.24, DESI SFR log -0.2 vs PHZ -0.1 (Fig. 2, p. 5). No named galaxies.
- Table 1 (p. 2): depths per band and field; Table 2-3 (p. 4): products and parameters; Table 4 (p. 9): photo-z vs IE; Fig. 3 (p. 7): reference sample validation; Fig. 4 (p. 8): EAFs; Fig. 5 (p. 9): EWS-like; Fig. 6 (p. 10): deep; Fig. 7 (p. 11): SFMS; Fig. 8 (p. 12): mass completeness.

## Cross-references
- hartley.md (pipeline, reference sample, known issues); Tucci et al. 2026 (Q1 PHZ); Enia et al. 2026b (Q1 physical parameters; A&A 711, A14); Enia et al. 2024 (metrics and simulations); Kümmel et al. 2026 (MER catalogue, flags); Corcho-Caballero et al. 2026 (EXT data); Gasparetto et al. 2026 (MER photometry); Odier et al. 2026 (VMPZ mask); Khostovan et al. 2026 (COSMOS spec-z compilation); Weaver et al. 2022 (COSMOS2020); Euclid DR1 Explanatory Supplement for exact table/column names.
