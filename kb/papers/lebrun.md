---
title: "Euclid Data Release 1 (DR1): Performance of the redshift measurement and spectroscopic analysis"
short_name: lebrun
first_author: Le Brun
series: A&A Special Issue DR1-Foundation (Nov 2026)
local_pdf: ~/Desktop/euclid/papers/lebrun.pdf
local_text: ~/Desktop/euclid/text/papers/lebrun.txt
topics: [SPE processing function, spectroscopic redshifts, classification, emission-line fluxes, quality flags, DESI validation, visual inspection, interlopers, Science Archive tables]
relevance_extended_galaxies: medium   # for photometry / 2-D modelling / LSB of low-to-intermediate-z galaxies
---

# DR1 spectroscopic redshifts, classification and line fluxes: pipeline and performance (Le Brun et al. 2026)

## TL;DR
Describes the SPE pipeline that turns the SIR combined 1-D slitless spectra into redshifts (up to five candidates per object, with PDFs and probabilities), a galaxy/star/QSO classification and emission-line and absorption-index measurements, and validates them against DESI DR1, deeper Euclid Deep Field data and a visual-inspection campaign. DR1 has >160 million redshifts in the Wide Survey and 7.0 million in the Deep Fields (2.7 million in EDF-N) (p. 12), but the pipeline is tuned for Halpha emitters at 0.84 < z < 1.88: for z < 0.84 only ~40-60% of redshifts are correct and at z < 0.1 under 10% (EWS) (p. 10). For a low-to-intermediate-z galaxy group, the redshift catalogue is useful mainly for bright star-forming/AGN emitters and in the Deep Fields; for most low-z galaxies, external spectroscopic redshifts or photo-z remain essential.

## Key facts and numbers
- Target range: 0.84 < z < 1.88 via Halpha in the red grism (RGS), R ~ 500, 1206-1892 nm (p. 1). Blue grism (BGS) only in the Euclid Deep Survey (EDS) (p. 3).
- Spectra extracted for sources with HE < 23.5 over the three Euclid Deep Fields and 1900 deg2 of the Euclid Wide Survey (EWS) in DR1 (p. 1). Note: DR1 galaxy sources only produce a measurable spectrum if the source is in the MER catalogue and the trace falls at least partly on detectors (p. 1).
- Redshift precision: median (z_SPE - z_DESI)/(1+z_DESI) ~ 1e-5 (0.8e-5 EWS, 3.5e-5 EDS), scatter 4.1e-4 (EWS) and 3.2e-4 (EDS) (Fig. A.1, p. 18); sigma_dz/(1+z) = 0.0003 in DR1 EDFs vs 0.0008 in Q1 (p. 7).
- EDF-N has 7 complete RGS + 3 BGS visits; EDF-S 10 RGS visits; EDF-F one visit per grism (p. 6, 7). End-of-survey EDS depth: 25 BGS and 15 RGS visits (p. 1).
- Redshift success vs DESI, EDF-N high-quality 'galaxy' sample (spe_npix > 800, >= 12 median dithers, point-like prob < 0.05, vel. disp. < 1500 km/s, gal.spe_z_prob > 0.99): ~75% correct (|dz| < 0.003) at 0.84 <= z < 1.6; no significant change between 0.1-0.41 and 0.41-0.84 (H-alpha entering BGS not essential, [SIII] helps); 42% at z < 0.1 (p. 7). Even at highest probability thresholds the correct fraction stays below 80% (p. 7).
- With photo-z agreement (SPE z within 95% interval of PHZ): >80% correct everywhere at prob 0.99 and 98% for 0.84 < z < 1.6 (p. 7).
- Visual inspection of 4000 EDF-N sources (cosmology sample 0.85-1.85, F(Halpha) > 2e-16): quality tiers uncertain 1.3%, marginal 17.4%, reliable 50.9%, secure 30% (Table 2, p. 8). Spectroscopy-only selection gives 98.5% agreement with DESI over 3985 objects; adding gal.spe_z_prob > 0.94 and gal.spe_z_rel > 0.05 gives 98.9% over 3863 objects (p. 7).
- EWS performance (single EDF-N visits, RGS only): z < 0.1: < 10% correct; 0.1 < z < 0.84: ~40% rising to ~60% with probability threshold (vs <~10% in Q1); 0.84-1.88: ~10 percentage points higher against EDS reference than DESI; z > 1.88: ~64% correct at prob 0.99 vs EDS but only <~3% vs the few DESI matches (p. 10-11). EWS high-quality sample in EDF-N: 974 487 sources (~140 000 per visit) (p. 10).
- Line-flux validation: median EWS-vs-EDS Halpha flux difference -2 (+19, -26)% above F(Halpha) > 2e-16 erg/s/cm2; versus Subaru FMOS median +7 (+43, -28)% for Halpha+[NII] (p. 11).
- Halpha line interlopers: [OIII], [SIII]9532, HeI, Paschen-beta, H-beta, [OII]; [OIII] and [SIII]9532 peaks contain 12 and 44 times fewer objects than the correct-redshift peak respectively (p. 10). Noise interlopers mostly pile up in 0.84-1.88 because of the Halpha prior (p. 10).

## Data products and data model
Euclid Science Archive, SPE tables (12 per survey configuration, suffix <SURVEY> = deep_survey, wide_survey, deep_visits, wide) (p. 4):
- deep_survey: EDS stacks, RGS+BGS measured together. wide_survey: EWS only. deep_visits: individual RGS visits of EDFs (objects repeat once per visit with distinct IDs; patch_id_list retrieves visits; 8 visits in EDF-N with 7 complete, 1 in EDF-F, 10 in EDF-S). wide: all single-visit data including calibration fields (p. 4).
- catalogue.spectro_z_spe_quality_<S>: spe_npix (valid pixels), wavelength range, spe_n_dith_med/spe_n_dith_max (dithers), spe_lsf_red, processing errors (p. 4-5, 19).
- catalogue.spectro_z_spe_classification_<S>: spe_class, spe_gal_prob, spe_qso_prob, spe_star_prob.
- catalogue.spectro_z_spe_{galaxy,star,qso}_candidates_<S>: up to five solutions per object ranked by spe_rank (0 = best): spe_z, spe_z_err, spe_z_prob (RedshiftProba, integral of PDF peak within +/-3 sigma, relative not absolute significance), spe_z_rel (ML reliability, galaxy table only), spe_z_reduced_chi2, spe_z_p_value, spe_z_residual_normality. Star table uses spe_rvel, spe_rvel_err, spe_model_prob instead of z (p. 5, 19).
- catalogue.spectro_model_spe_{galaxy,star,qso}_models_<S>: model parameters per solution, e.g. spe_vel_disp_e, spe_cnt_tpl_id (template ID; QSO template names optical_nir_qso_template_v1.txt and ComposantesPCA4_meanqso.txt identify real quasars) (p. 6).
- Four spectral-feature tables (spectro_line_features_spe_line_features_<S> and tables for continuum features CNT_FEAT, Lick atomic indices AT_IDX, molecular indices MOL_IDX): one row per feature per redshift rank; SPE_LINE_NAME, SPE_RANK. Line rows give integrated flux, position, EW, continuum, mean number of dithers under the line, uncertainties for both DI and GF methods (spe_line_flux_gf, spe_line_flux_err_gf, spe_line_snr_gf, spe_line_n_dith, spe_line_qual_gf), plus FWHM for GF (p. 3, 5, 19).
- Main lines measured for every spectrum: Lyman-alpha, [OII], Hbeta, [OIII], Halpha, [NII]6585, [SII]6718, [SIII]9068, [SIII]9530, Pagamma, Pabeta; secondary lines stored only if AoN > 2.5 (p. 3). Lick indices/D4000 only if continuum S/N > 10 in 1350-1750 nm (p. 4).
- Line quality flag SPE_LINE_QUAL: 3 digits (method 1=DI, 2=GF, 3=Halpha QSO fit; quality digit; grism 1=BGS, 2=RGS, 3=both) (Tables D.1, D.2, p. 21): quality 1 good; 2 low S/N (< 2); 3 EW > 0 (EW set to 0); 4 combination issue; 5 acceptable (up to 15% pixels missing); 7 merging error; 8 unreliable (> 15% pixels missing for GF, > 1 missing for DI); 0 not measured; 9 outside range (negative values -91/-92/-93). Good GF RGS values are 212 (and 252, 222 if conservative) (p. 11).
- Doublet convention: GF gives total flux of [OIII], [NII], [SII] doublets (split 1/3:2/3 for [OIII]/[NII], 1/2:1/2 for [SII]); DI gives the blended Halpha+[NII] complex, GF deconvolves them (p. 3).
- Input: SIR combined 1-D spectra with signal, variance and per-pixel flags (details in Scodeggio et al.) (p. 2). Sample ADQL join is in Appendix C (p. 18-19) and combines classification, candidates, models, line features, quality and MER columns (flux_*_sersic, kron_radius, point_like_prob, spurious_prob, tile_index).
- Archive layout is a direct copy of pipeline files and will be simplified later (p. 5).

## Processing and methods
1. Pixel selection: drop 'do not use' pixels, pixels with poor absolute flux calibration (band edges) and isolated pixels; require > 100 valid pixels (p. 2). Tiles invalidated if no reliable galaxy measurements (gal.spe_z_prob > 0.99 criterion) (p. 2).
2. Three categories with chi2 fits over redshift grids and a joint-likelihood PDF; up to five peaks fitted with Gaussians, ranked by integral within +/-3 sigma (p. 2). Galaxy: z = 0.01-5, steps 1e-4 in log(1+z), emission-line-only model after iterative median filtering of continuum, VVDS line-ratio templates, Halpha prior; unsuitable for z < 0.84 and quiescent galaxies (p. 2). Star: v range -0.01 to +0.01 in z, Pickles library plus ultracool dwarfs; no solution if continuum not detected (fainter than HE ~19 in EWS/EDF-F, ~19.5 in EDF-N/S) (p. 2). QSO: z = 0.01-8, SDSS and Euclid-built mean quasar templates plus five extra galaxy templates (QG, SFG, blue SFG, red SFG at U-V = 1.27, type-2 AGN from DESI), stacked from Q1 spectra with SpectraPyle (12 190 QGs, 21 641 blue SFGs, 7810 red SFGs) (p. 2-4).
3. Classification: Bayesian model evidence among the three categories; galaxy continuum fit with BC03 for the chi2, leaving a bias in favour of 'galaxy' (p. 3).
4. Line fluxes: direct integration (multi-scale continuum, wavelet removal of 10 strongest peaks) and Gaussian fit (line position free within +/-1e-3, constant continuum in 30 nm window, ~20 px); blended complexes fit with tied widths; QSO mode for velocity dispersion > 1500 km/s with narrow+broad Halpha and 80 nm window (p. 3-4). When both grisms are present, fluxes in overlap are averaged.

## Validation and performance
- Classification vs DESI (Table 1, p. 6): galaxies agree 64.6% (EWS) / 78.6% (EDS) using spectra only, rising to 98.2% / 98.4% after requiring MER extended (point-like prob < 0.5); stars 99.6% / 98.6% agree; QSO 88.2% / 95.5% purity but <5% of DESI quasars are recovered as QSO (most leak into galaxy). Many DESI stars (35 082) are classified as galaxies vs 21 997 as stars. Matching radius 0.2 arcsec; minimum 300 pixels and 3 dithers (EWS), 800 and 12 (EDS) (p. 6).
- Redshift accuracy (Sect. 4-5, Fig. 3, 5): see key facts; reference samples DESI DR1 (reliable up to z = 1.6) and EDF-N EDS + PHZ.
- Visual inspection quality tiers validated by median stacks; Secure/Reliable stacks show [OII], Hbeta, [OIII], Halpha+[NII], [SII], plus weak [NeIII], HeI, [OI], [ArIII], [SIII] (Fig. 4, p. 9).
- Flux validation vs EDS and FMOS (Sect. 5.4, Fig. 6). Flux errors scale with the number of observations: EWS errors are a factor sqrt(17/4) larger than EDS ones (17 and 4 observations) (p. 11). Rest-frame NIR lines [SIII]9530, Pagamma, Pabeta cross-checked with slinefit (p. 12).

## Known issues, caveats, limitations
- Halpha prior: favours Halpha identification; causes interlopers and pushes noise redshifts into 0.84-1.88; probably too strong for DR1 data and will be retuned for DR2 (p. 10).
- RedshiftProba is only relative; spe_z_rel was trained on EL-COSMOS simulations, so it is sub-optimal on DR1 data (p. 7).
- Galaxy category is for emission-line objects; quiescent galaxies and type-2 AGN appear in the QSO category through the extra templates (use spe_cnt_tpl_id to separate real quasars) (p. 6).
- Classification bias in favour of 'galaxy' (continuum-subtracted model); stars and QSOs leak into galaxy class; use MER point_like_prob (p. 3, 6).
- Low-z galaxies: correct fraction < 10% at z < 0.1 (EWS) and 42% at z < 0.1 in EDF-N; large angular size dilutes the signal and lines are few/faint (p. 7, 10).
- DI continuum estimation too aggressive: DI fluxes ~15% larger than GF; will be removed in DR2 (footnote p. 3).
- Moderate completeness in deep fields: EDF-F one visit per grism, EDF-S 10 RGS visits, EDF-N most complete (p. 8).
- Plateau at 4.1 < z < 5 in EDF-N redshift distribution is likely artificial; PHZ agreement removes it; drop at z ~ 2.8 where [OIII]/Hbeta exit (p. 18).
- Redshift distributions reflect detection biases; not physical (p. 18).
- Stellar templates external; Euclid-based templates planned for DR2 (p. 12).
- Redshift measurement only on spectra with > 100 valid pixels (p. 2).

## Implications for extended-galaxy photometry, 2-D modelling and low-surface-brightness work
- Which lines fall in range (computed from rest wavelengths and the stated grism ranges, not tabulated in the paper): RGS 1206-1892 nm catches Halpha for 0.84 < z < 1.88 (p. 10), [SII]6718 for z ~ 0.8-1.8, [SIII]9532 for z ~ 0.27-0.99 and [SIII]9069 for z ~ 0.33-1.09, HeI 1083 for z ~ 0.11-0.75, Pagamma for z ~ 0.10-0.73 and Pabeta for z up to ~0.47. So at z < 0.84 only weak [SIII]/Paschen/HeI lines are available, not Halpha; below z ~ 0.1 essentially no strong line is in range (the paper confirms <10% success). BGS (EDS only, 926-1366 nm) brings Halpha for z ~ 0.41-1.08 and the [SIII] lines and Pabeta for z < ~0.4 (the paper identifies z = 0.41 as Halpha entering BGS, p. 7).
- Therefore for low-z (z < 0.5) extended galaxies, DR1 redshifts will be mostly unreliable or missing; use spectroscopic redshifts from SDSS/DESI/GAMA where available. Use SPE redshifts for galaxies at z ~ 0.84-1.9 with Halpha above ~1.5-2e-16 erg/s/cm2.
- Large angular size smears the slitless signal and reduces resolving power (see Fumana), so bright, extended nearby galaxies are the worst-case for slitless redshifts; the pipeline recommends excluding kron_radius > 50 for the cosmology sample (p. 7).
- Emission-line fluxes are integrated over the slitless extraction aperture, not resolved. For resolved studies, see Gabarra et al. (emission-line maps).
- Stacking (SpectraPyle) of low-quality tiers can mimic good spectra (noise features align), so stacked-line detections do not validate individual redshifts (p. 9-10).
- Quiescent galaxy example: z = 0.232, HE = 15.5 template fit (Fig. 2, p. 5), showing that the QG template can give a continuum-based redshift for bright low-z ellipticals.

## Practical recommendations for users
- Select high-quality galaxy redshifts with: spe_npix >= 800 and spe_n_dith_med >= 12-15 (EDS) or >= 300 and >= 3 (EWS); gal.spe_z_prob > 0.99 (or > 0.94 together with gal.spe_z_rel > 0.05); spe_rank = 0; mer.point_like_prob < 0.05; mer.spurious_prob < 0.5; mer.kron_radius < 50 (p. 6-7).
- For fluxes, require spe_line_snr_gf > 0 (S/N > 5 or 10 for science), spe_line_qual_gf = 212 or 252 (and possibly 222); prefer GF over DI; remember GF gives doublet totals (p. 3, 11).
- Use PHZ agreement (95% interval) to raise purity to 98% at z ~ 0.84-1.6 and >80% elsewhere (p. 7).
- Identify real quasars via spe_cnt_tpl_id; treat 'qso' class with galaxy templates as quiescent/type-2 candidates (p. 6).
- Exclude stars with MER point-like probability; star-class purity ~99%.
- When querying, join candidate and model tables on object_id AND spe_rank; use ADQL in Appendix C as a template (p. 18).
- EDS data in EDF-N give the most reliable redshifts; individual-visit catalogues duplicate objects.

## Objects, fields and figures worth revisiting
- Fields: Euclid Deep Field North (EDF-N), Fornax (EDF-F), South (EDF-S), COSMOS (FMOS-COSMOS overlap, EL-COSMOS simulations). Coordinates not given.
- Fig. 2 (p. 5): templates and z = 0.232 quiescent galaxy (HE = 15.5). Fig. 3 (p. 8) and Fig. 5 (p. 11): redshift comparison and fraction correct vs probability and redshift bin. Table 1 (p. 6): classification vs DESI. Table 2 (p. 8): visual quality. Fig. 4 (p. 9): composite spectra. Fig. 6-7 (p. 12-13): flux validation and FMOS spectrum of z = 1.613 galaxy (F(Halpha) = 3.4e-16). Tables D.1-D.2 (p. 21): line quality flags. Appendix E (p. 22-24): example spectra.

## Cross-references
- Le Brun et al. 2026 (Q1 SPE paper, A&A 711, A7), Scodeggio et al. (SIR-DR1, input spectra), Fumana et al. (calibration), Quai et al. 2026 (SpectraPyle, visual inspection), Mao et al. 2026 (UVJ classification, Lick indices), Granett et al. 2026 (interlopers), Hartley et al. 2026 (PHZ photo-z), Kuemmel et al. 2026 (MER), Markovic et al. (galaxy clustering sample), Lopez Lopez et al. (type 2 AGN), Euclid Data Product Description (SPE catalogue card).
