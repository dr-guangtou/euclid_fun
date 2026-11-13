---
title: "Euclid: Data Release 1 (DR1) - Bayesian 3D shape inference of star-forming galaxy populations"
short_name: dunn
first_author: Dunn
series: A&A Special Issue DR1-Foundation (Nov 2026)
local_pdf: ~/Desktop/euclid/papers/dunn.pdf
local_text: ~/Desktop/euclid/text/papers/dunn.txt
topics: [intrinsic 3D shapes, triaxiality, prolate, oblate, Sersic axis ratio, effective radius, Hamiltonian Monte Carlo, star-forming galaxies, SourceXtractor++, VIS, population inference]
relevance_extended_galaxies: medium
---

# Bayesian 3D shape inference of DR1 star-forming galaxies (Dunn et al. 2026)

## TL;DR
Applies the Pandya et al. (2024) population-level Bayesian (HMC/NUTS in PyMC) framework to the projected axis ratio and effective radius from single-Sersic fits of VIS (IE) images, for 40 864 304 star-forming galaxies with log M* = 9-10.5 at 0 < z < 1.2 (IE <= 24.5), in 18 mass-redshift bins. It recovers the known decline of the prolate fraction at low mass towards z = 0 and finds oblate dominance everywhere at low z. For 2-D modelling users the useful part is the explicit list of DR1 Sersic-fit quality cuts and the appendix comparing DR1 single-Sersic parameters with HST (ACS-GC) and with the isophotal catalogue values, showing which structural quantities are reliable down to IE = 24.5 (q and Re yes, n no).

## Key facts and numbers
- Sample: 104 540 419 star-forming galaxies after sSFR and UVJ selection; 70 498 316 after quality cuts; 40 864 304 final in mass 1e9-1e10.5 Msun, 0 < z < 1.2, IE <= 24.5 (p. 3-4). Bins: Delta log M* = 0.5 (3 bins), Delta z = 0.2 (6 bins). Bin counts range from 21 000 (z < 0.2, 10-10.5) to 4 717 101 (0.6-0.8, 9-9.5) (Table F.1, p. 24). More than 9 million galaxies at z < 0.5 (abstract; z < 0.4 bins alone total about 5.3 million).
- Parameters inferred per bin (7): mean 3D ellipticity E = 1 - C/A, triaxiality T = (A^2 - B^2)/(A^2 - C^2), log10 A (kpc), their standard deviations and the E-log A covariance (p. 2-3). Model library: 1 million ellipsoids on uniform E-T-log A grid, 100 000 viewing angles, 20 x 20 grid in b/a vs log10 a, Rice scatter Delta(b/a) = 0.04, Gaussian 0.03 dex size smearing (p. 2).
- Inference: Poisson likelihood on 2-D histogram of b/a in [0,1] and log10(a/kpc) in [-1,1] (about 0.1-10 kpc); NUTS with 4 chains, 5000 tuning + 2000 draws, target acceptance 0.95; all R-hat < 1.01 (max 1.004 in table F.1), no divergences; days of cluster time per bin (p. 3-4, 12).
- Results (Table F.2, p. 25): mean ellipticity mu_E = 0.600-0.821 in all bins (about 0.80-0.82 at z < 0.2 for all masses); mu_T declines towards z = 0 (e.g. 0.547 at z 1.0-1.2 and 0.275 at z < 0.2 for 9-9.5; high-mass bins hit T = 0 boundary at z < 0.6); rho(E, log A) rises to 0.854-0.875 at z < 0.2.
- Low-mass (9-9.5) prolate fraction: 0.419 (1.0-1.2), 0.349 (0.8-1.0), 0.281 (0.6-0.8), 0.177 (0.4-0.6), 0.080 (0.2-0.4), 0.043 (0.0-0.2); oblate 0.544 -> 0.763-0.798 (dips from 0.798 at 0.2-0.4 to 0.763 at 0-0.2); spheroid 0.04 -> 0.19 at z < 0.2. Intermediate mass (9.5-10) at z < 0.2: oblate 0.965. High mass (10-10.5): spheroid 0.599 at 1.0-1.2 falling to 0.003 at z < 0.2.
- Prolate fractions of ~16-18% at z ~0.5 in every mass bin disagree with TNG50, which predicts essentially none (p. 11).
- Statistical errors are 6-100x smaller than Z19 (HST-CANDELS) and P24 (JWST-CEERS) (p. 4, 7); sample is 440-52 800x larger than those studies' comparable bins (abstract).
- Mass completeness (Appendix E, p. 23): at least 90% complete in all bins except 9-9.5 at 0.8-1.0 (75%) and 1.0-1.2 (50%).
- Mock test: HMC recovers parameters for N >= 50, struggles at lower N, especially mu_T, sigma_T (p. 22-23).
- Q1 trial: 929 344 Q1 star-forming galaxies gave posteriors that struggled to converge (mainly triaxiality), unlike DR1 (p. 10).

## Data products and data model
Uses DR1 MER and PHZ catalogues (no new product released). Exact selections (Appendix A, p. 17):
- Magnitude: IE <= 24.5 implemented as FLUX_SEGMENTATION > ~0.575 (flux in segmented pixels, uJy).
- VIS_DET = 1; SPURIOUS_FLAGS = 0; DET_QUALITY_FLAG < 4; POINT_LIKE_PROB <= 0.1 (discard point-like); MUMAX_MINUS_MAG > -2.6 (appendix says "remove extended sources" but the intent, in line with enia.md/hartley.md, is to remove compact ones).
- PHYS_PARAM_FLAGS = 0; PHZ_CLASSIFICATION = 2.
- Consistency of PHZ: |PHZ_PP_MEDIAN_Z - PHZ_MEDIAN| < 0.2 and |PHZ_PP_MEDIAN_Z - PHZ_PP_MODE_Z| < 0.2.
- Sersic (SourceXtractor++, VIS band, single Sersic, PSF-convolved forward model; Quilley et al. 2026): 
  - 0.01 a < SERSIC_SERSIC_VIS_RADIUS < 20 a (a = isophotal semi-major axis in VIS pixels);
  - 0.302 < SERSIC_SERSIC_VIS_INDEX < 5.45;
  - 0.05 < SERSIC_SERSIC_VIS_AXIS_RATIO < 1.0;
  - SERSIC_SERSIC_VIS_AXIS_RATIO_ERR < 0.10 and SERSIC_SERSIC_VIS_RADIUS_ERR < 0.10 (fractional >10% rejected; no cut on Sersic-n error);
  - SERSIC_SERSIC_VIS_RADIUS > 0.16" (VIS PSF FWHM);
  - finite SERSIC_SERSIC_VIS_RADIUS, SERSIC_SERSIC_VIS_AXIS_RATIO, PHZ_PP_MEDIAN_STELLARMASS, PHZ_PP_MEDIAN_SFR, PHZ_PP_MEDIAN_REDSHIFT.
- Also used: MER SEMIMAJOR_AXIS and ELLIPTICITY (isophotal; q_iso = 1 - ELLIPTICITY; not PSF-corrected) for comparison; PHZ photo-z, stellar mass, SFR, rest-frame magnitudes and AV (medians of posteriors) for sSFR and UVJ selection.
- Size a = angular Sersic effective semi-major axis (van der Wel+14b convention); b/a = Sersic axis ratio; physical size via photo-z (p. 3).

## Processing and methods
1. Build magnitude-limited parent sample from MER + PHZ with the cuts above (p. 3, 17).
2. Star-forming selection: median sSFR of zero-slope SFMS per z slice (Pandya+17), scatter 0.45 dex; star-forming = less than 1 sigma below; transition = 1.5-3.5 sigma; quiescent > 3.5 sigma (Fig. C.1) (p. 3).
3. UVJ selection: reject galaxies in the quiescent wedge of Van Dokkum+15 ((V-J) < 1.5, (U-V) > 1.3, (U-V) > 0.8 (V-J) + 0.7) using Euclid rest-frame colours and AV from PHZ (Fig. C.2) (p. 3-4).
4. Convert angular a to kpc with photo-z; redshift-uncertainty effect tested by redrawing z within the 68% PHZ interval: scatter <= 0.03 dex, hence not propagated (p. 4).
5. Bin, histogram b/a-log10 a, fit the trivariate Gaussian parent distribution by HMC, derive class fractions by sampling the posterior in C/A-B/A space with Zhang+19/van der Wel+14a boundaries (p. 7). Class fractions are a posteriori summaries, not constraints.
6. Appendix G: per-galaxy class probabilities from observed (b/a, log a) only; only 34 galaxies have P(prolate) > 75%, mostly barely resolved (Re only 1.1-1.4x PSF FWHM) (p. 26).

## Validation and performance
- Sersic vs HST (Appendix B, p. 17-18): single-visit EDF-F (EWS depth) vs ACS-GC (GALAPAGOS, F606W) in GEMS, IE <= 24.5. Dispersion of Re difference rises from <~10% at IE < 23 to ~16% at 24.0 < IE < 24.5; q dispersion <~3% to ~7%; biases at faint limit: Re high by ~7%, q by <~2%; Sersic n by far worst (dispersion ~0.57 at IE = 24.5). Close to the Q1-ACS-GC comparison in Quilley et al. 2026. Colour-gradient and bandpass differences (F606W vs VIS) add scatter.
- Sersic vs isophotal (Fig. B.3-B.4, p. 18-19): median log10(a_Sersic/a_iso) = 0.081 dex, scatter 0.074 dex; median q_Sersic - q_iso = -0.093, scatter 0.091, offset present at all Sersic n because isophotal shapes are PSF-rounded. Pure discs (n ~1) span 0.1 < q <= 1 in Sersic but are truncated at higher q in isophotal values.
- Morphological completeness (Appendix E, Fig. E.1): mocks from the Euclid Morphology Challenge, single-Sersic SE++ fits; detection fraction stays high for large face-on discs (large Re, high b/a) within IE <= 24.5; incompleteness is concentrated in faint (IE > 24.5) compact sources.
- Photo-z quality context (p. 3): citing Enia et al., sigma_NMAD 0.021 / outliers 3.7% (EWS-N) and 0.027 / 7.6% (EWS-S) overall, degrading to 0.034-0.048 and 9.4-16.2% at 23 < IE <= 25.
- Fit diagnostics: per-bin observed/model/residual histograms (Figs. H.1-H.18, p. 27-31) show systematic data-model differences not captured by statistical errors.

## Known issues, caveats, limitations
- Single-Sersic global axis ratios describe the whole light distribution; for bulge+disc systems q follows the disc for face-on or B/T <~ 0.1, but edge-on discs with significant bulges bias towards thicker oblate/spheroidal inference (p. 11). Median Sersic n ~1.1 in the lowest-mass bins.
- Sersic q and size believed unbiased down to S/N ~20 (literature) and to IE = 24.5 here (p. 11); Sersic n is poorly constrained and was not error-cut (p. 17-18).
- Blends/mergers/close pairs fitted as a single galaxy give anomalous q and size, increasing with z (p. 11).
- Size cut Re > PSF FWHM (0.16") excludes compact, round, high surface brightness objects, biasing sizes upward at high z and low mass (p. 3, 11).
- VIS-only: rest-frame wavelength changes with z (UV at z > ~1) and inclination-dependent dust attenuation affects apparent ellipticity and size; the reason for z < 1.2 limit (p. 11).
- Triaxiality is the least reliable output: single unimodal Gaussian; in intermediate/high-mass bins mu_T is pinned to the T = 0 boundary with large, tightly determined sigma_T (dip near z 0.4-0.6), so precise does not mean accurate; spheroid fractions are inflated by broad sigma_E/sigma_T (p. 9, 11-12).
- The edge-on disc examples with large b/a and size beyond the model library range are extrapolations (log a in [-1,1] only) (p. 26).
- Statistical errors only (Table F.2); systematics from photo-z, bands, classification boundaries not propagated.
- Bin sample incompleteness at 9-9.5, z > 0.8 (75% and 50%) (p. 23).
- Compute: days per bin; SBI suggested for future (p. 12).

## Implications for extended-galaxy photometry, 2-D modelling and low-surface-brightness work
- Direct evidence that DR1 single-Sersic fits (SourceXtractor++ on VIS, PSF-convolved) give usable axis ratios (to ~7% at IE 24-24.5) and effective radii (to ~16% dispersion, ~7% bias high) to IE <= 24.5 for typical star-forming galaxies; Sersic index should not be trusted individually (dispersion ~0.6). These are "cheap" global measurements: for bulge/disc decomposition, tidal features and haloes a dedicated 2-D fit is still required.
- Isophotal MER shapes (SEMIMAJOR_AXIS, ELLIPTICITY) are PSF-rounded: q_iso is about 0.09 too round vs Sersic q on average; do not use them to measure inclination of thin discs.
- Median Sersic radii are ~0.08 dex larger than isophotal semi-major axes; remember the definitions differ.
- Single-Sersic q for a bulge+disc galaxy is a flux-weighted compromise; for B/T > ~0.1 and edge-on systems the disc inclination is underestimated.
- Low-z coverage: >9 million galaxies at z < 0.5, though the lowest-z, highest-mass bin (10-10.5, z < 0.2) has only 21 000 galaxies; the size limit of log a up to 10 kpc and Re > 0.16" mean nearby, large galaxies are out of the library range, so large angular size objects (nearby ellipticals/discs) are not represented.
- Surface-brightness completeness: mocks suggest large face-on discs are retained at IE <= 24.5, but this is for simulated single-Sersic galaxies, not true LSB galaxies; no LSB statements are made.
- Not relevant for ICL/halo/tidal-feature work except as a caveat on blended and merging systems being fitted as single Sersic profiles.

## Practical recommendations for users
- Reuse the Appendix A cuts when selecting DR1 galaxies with Sersic fits: VIS_DET = 1, SPURIOUS_FLAGS = 0, DET_QUALITY_FLAG < 4, POINT_LIKE_PROB <= 0.1, PHYS_PARAM_FLAGS = 0, PHZ_CLASSIFICATION = 2, SERSIC_SERSIC_VIS_* errors < 10% for radius and axis ratio, 0.302 < n < 5.45, 0.05 < q < 1, Re > 0.16", and photo-z consistency |PHZ_PP_MEDIAN_Z - PHZ_MEDIAN| < 0.2.
- Do not select on Sersic-n uncertainty as if it were reliable; do not use n for individual objects.
- Prefer Sersic q to isophotal q for inclination; correct for the ~0.09 offset only if you must use isophotal values.
- Apply stellar-mass completeness (Appendix E; Pozzetti method) before comparing bins.
- Do not interpret mu_T/sigma_T in the T = 0-bounded bins or per-galaxy class probabilities as definitive.
- Do not push the analysis above z ~1.2 using VIS alone (rest-frame UV, dust, clumpy light).
- For star-forming selection use sSFR (< 0.45 dex below the zero-slope SFMS) plus UVJ wedge rejection (Eq. 3).

## Objects, fields and figures worth revisiting
- Fields (no coordinates given): EDF-F single-visit (EWS depth) compared with HST ACS-GC in the GEMS field; Euclid Morphology Challenge mocks. No named galaxies.
- Fig. 1 (p. 5): b/a vs log a histograms per bin with PSF-FWHM line; Fig. 2 (p. 6) shape parameter evolution vs P24/Z19; Fig. 3 (p. 8) C/A-B/A distributions; Fig. 4-5 (p. 9) class fractions.
- Fig. B.1-B.2 (p. 17-18): Sersic parameters and errors vs IE against HST - most useful figures for 2-D modelling users; Fig. B.3-B.4 (p. 19) Sersic vs isophotal; Fig. E.1-E.2 (p. 23) completeness; Fig. G.1 (p. 26) VIS cutouts (5" x 5") of high-probability prolate/oblate/spheroid candidates, made with Cutana on ESA Datalabs; Table F.1-F.2 (p. 24-25).

## Cross-references
- Quilley et al. 2026 (Q1 Sersic morphology with SE++, A&A 710, A277; the origin of the quality cuts and the ACS-GC comparison); Kümmel et al. 2026 (MER catalogue, columns/flags); enia.md (PHZ stellar mass, SFR, rest-frame colours, AV); hartley.md (photo-z, classification); Zhang et al. 2019 and Pandya et al. 2024 (method and comparison); van der Wel et al. 2014a,b; Euclid Morphology Challenge (Merlin et al. 2023; Bretonnière et al. 2023); Walmsley et al. 2026 (Zoobot morphology, suggested for merger/blend screening); McCracken et al. 2026 (VIS processing).
