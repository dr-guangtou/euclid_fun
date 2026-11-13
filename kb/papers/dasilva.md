---
title: "Euclid Data Release 1 (DR1): NISP-P point-spread function modelling pipelines"
short_name: dasilva
first_author: da Silva
series: A&A Special Issue DR1-Foundation (Nov 2026)
local_pdf: ~/Desktop/euclid/papers/dasilva.pdf
local_text: ~/Desktop/euclid/text/papers/dasilva.txt
topics: [NISP, PSF, PSFEx, NIR PF, YE, JE, HE, encircled energy, undersampling, IPC, IPS, brighter-fatter effect, PSF-fitting photometry, SPREAD_MODEL, self-calibration field]
relevance_extended_galaxies: medium
---

# NISP-P PSF modelling pipelines for DR1 (da Silva et al. 2026)

## TL;DR
Describes how the NIR processing function (OU-NIR) builds PSF models for the NISP photometric channel (YE, JE, HE) with SourceExtractor + PSFEx, either per single-dither exposure or on the stacked frame, and how they were validated (encircled energy, PSF-fit vs aperture photometry, SPREAD_MODEL, ellipticity stability). Models are oversampled by 6 (0.05"/pix), constant within each of the 16 detectors, and cover only ~3" (scientific pipeline) or ~7" (calibration-pipeline "extended" models) across: the faint far wings/scattered light of the PSF are NOT modelled. Requirements on EE radii and centroids are met, but there are known issues (MAG_PSF offset, stacked-frame PSF not optimised, uncorrected brighter-fatter effect). Very little in the paper concerns surface-brightness or galaxy work; its main relevance is the extent and accuracy of the NIR PSF that MER propagates into the mosaics and uses for PSF-matching and Sersic fitting.

## Key facts and numbers
- NISP: 4x4 HgCdTe H2RG detectors; pixel scale ~0.3"; PSF undersampled; 1.2 m primary (pp. 1-2). NISP median 5 sigma point-source depth ~24.4 AB (p. 1).
- Nominal survey start 14 Feb 2024; Q1 covers 63.1 deg2; DR1 ~1900 deg2 (p. 1). EWS pointing = 4 dithered exposures per channel (p. 1).
- Requirements (p. 2): r_EE50 < 0.4" and r_EE80 < 0.7" (below 1486 nm); PSF centroid accuracy better than 0.1 NISP pixel; relative photometric error < 1.5% and absolute < 5% (goal); PSF models as function of position, wavelength and time.
- Oversampling: PSF models sampled at 1/6 detector pixel = 0.05" (pixel 3 micron vs 18 micron) (pp. 3-4).
- Model sizes: scientific pipeline (single dithers AND stacked frames) 61/6 x 61/6 detector pixels, about 10 x 10 detector pixels = ~3" (5x the HE FWHM). PSF calibration pipeline ("extended models", single dithers only): 141/6 x 141/6 detector pixels = ~23.5 pixels = ~7" (>10x HE FWHM), "large enough to include the most prominent diffraction patterns (rings and spikes)" (p. 3). MDB (physical-optics) library models are 512/6 detector pixels wide (p. 8).
- Flux outside the 141/6 stamp (long diffraction spikes): about 1% (YE), 1.8% (JE), 2.1% (HE), estimated from the MDB models; the authors deliberately do not use larger stamps to avoid contamination by neighbours (p. 8). A 6-pixel (1.8") diameter aperture encloses ~94%, 93%, 92% (YE, JE, HE) of the flux in the 141/6 stamps (p. 7).
- MDB library: 2160 PSF shapes (5 focal-plane positions per each of 16 detectors; 9 monochromatic wavelengths over each of 3 passbands) (p. 3). Used only for tests (MDB mode).
- Table 1 (single-dither, 16 detectors; p. 5), approximate values: r_EE50 = 0.22-0.225" (YE), 0.24-0.246" (JE), 0.276-0.281" (HE); r_EE80 = 0.375-0.387" (YE), 0.44-0.45" (JE), 0.55-0.56" (HE); FWHM 0.35 (YE), 0.35 (JE), 0.365-0.374" (HE); aperture correction for 6-pixel aperture 1.06 (YE), 1.07 (JE), 1.083 (HE) (i.e. fluxes in that aperture need to be multiplied by these factors). Stacked frame (Obs. 2955): r_EE50 = 0.268, 0.281, 0.300"; r_EE80 = 0.405, 0.438, 0.496"; FWHM = 0.465, 0.488, 0.511"; aperture correction 1.023, 1.027, 1.014. Note the running text (p. 4) quotes ranges that do not match the table columns (e.g. r_EE80 0.27-0.30 single, 0.38-0.56 stacked); trust Table 1. All are well below requirements. Detectors differ very little.
- Multi-aperture photometry (new in DR1 NIR catalogues): circular apertures with radii 0.6, 0.9, 1.5, 2.25, 3.0" (diameters 4, 6, 10, 15, 20 detector pixels); Q1 had only the single 0.9" aperture (p. 10). Table 2 (p. 11): median EE radii from these aperture curves: r_EE50 = 0.336/0.346/0.370" and r_EE80 = 0.538/0.554/0.591" for YE/JE/HE (single detector 11); stacked 0.335/0.345/0.370 and 0.536/0.552/0.591 (coarsely sampled, minimum aperture 0.6").
- Centroid accuracy from PSF fitting on simulations: mean < 0.003 and std < 0.03 detector pixels (p. 8).
- MAG_APER relative precision for repeated sources (>= 10 dithers) within 0.005 mag (0.5% flux); absolute vs Gaia: within 2%, 3%, 5% for YE, JE, HE (p. 10).
- PSF-fit minus aperture offsets (Figs. 5-6, p. 8): HE Q1 code and models -0.008 +- 0.018 mag; DR1 code with old models 0.010 +- 0.013; DR1 code with extended models 0.052-0.058 +- 0.010 mag (sign/format approximated from garbled numbers; the magnitude of the offset rises while the scatter falls). YE: Q1 0.021 +- 0.074 -> DR1 0.047 +- 0.017; JE: 0.019 +- 0.026 -> 0.050 +- 0.011 mag. Slopes drop from ~0.02 to ~0.004 (YE).
- Ellipticity stability: within 0.05 for most PSF models and sources over > 180 days in three EWS patches (p. 13, Fig. E.1).
- Number of sources: calibration pipeline uses SCF (self-calibration field) data, ~50 sources per detector per dither x 76 dithers = thousands (e.g. 3131 YE, 2936 JE, 2991 HE for Fig. 1); the EWS science pipeline typically has fewer than ~100 good point sources per 4-dither observation (and 810, 863, 614 for the stacked example) (pp. 5, 19).

## Data products and data model
- PSF models are products of two OU-NIR pipelines (p. 2): NIR scientific pipeline (single-dither "simplified" PSF models, 3" stamps, per detector per exposure; stacked-frame PSF models for the stack); NIR PSF calibration pipeline ("extended" PSF models, ~7" stamps, from SCF CALBLOCK-F-001, single dithers). Output is a FITS file with 16 extensions (one per detector) for a given position and wavelength in MDB mode (p. 3); the per-detector PSF structure is the same in Inflight mode (PSFEx output, one model per detector, constant across the detector: PSFVAR_DEGREES = 0).
- DR1 data used in the paper are in the Euclid science archive at ESAC (ESDC; https://eas.esac.esa.int/sas/) (p. 2). Table A.1 (p. 21): SCF CALBLOCK-F-001 extended PSF models: Patch 41, Obs. 2174 (processed 2025-01-24) and Patch 8, Obs. 519 (2025-04-12); single-dither exposures and catalogues Patch 131, Obs. 6185 (2025-02-04); single-dither catalogues Patch 255, Obs. 10614 (2025-11-09); photo-z calibration field CALBLOCK-F-005: stacked frames and catalogues Patch 56, Obs. 2955 (2025-04-23), single-dither exposures Obs. 2955-2971, 4876-4983 (Patch 98), 6125-6141 (Patch 129).
- SourceExtractor output columns discussed (Table A.4, p. 22): MAG_APER, FLUX_APER, MAG_PSF, MAGERR_PSF, FLUX_RADIUS, SNR_WIN, SPREAD_MODEL, FLAGS, IMAFLAGS_ISO, XWIN_IMAGE, YWIN_IMAGE, VIGNET.
- NIR catalogues (NIR_CatalogExtraction task): per calibrated image, with detection from a second-derivative-image source map, then PSF-fitting and aperture photometry (p. 8).
- NIR data-quality layer in multi-extension FITS: flags saturated, poor-quality, contaminated, cosmic-ray pixels (INVALID flagged sources are excluded) (p. 3).
- The user-facing mapping of these into DR1 archive products (which table holds which PSF, per tile or per position) is NOT specified in this paper; MER uses these PSFs as inputs and propagates them to the mosaics (kuemmel Sect. 2.4). For MER mosaic PSFs use the MER PSF products (stamps limited to 5", variable across the tile) - check Explanatory Supplement.

## Processing and methods
1. NIR scientific pipeline (p. 2): pre-processing -> astrometric and photometric calibration of single dithers -> catalogue extraction + first PSF models (per exposure) -> resample the 4 EWS dithers to a common grid and stack -> second PSF derivation on the stack and second catalogue extraction.
2. NIR PSF calibration pipeline: only pre-processing, then PSF models from SCF single dithers (large source sample).
3. Two modes (p. 2-3): MDB mode (library of physical-optics PSFs oversampled x6 convolved with IPS (parabolic sub-pixel response, 6x6 grid, std ~0.0325, drop ~8.5%) and IPC (3x3 kernel) kernels; single dithers only; not used for delivered models) and Inflight mode (empirical; standard for survey processing).
4. Inflight: SourceExtractor builds catalogues (Table A.3: DETECT_MINAREA 4, DETECT_THRESH 3 sigma, ANALYSIS_THRESH 1.5 sigma, BACK_TYPE AUTO, BACKPHOTO_TYPE LOCAL, PHOT_APERTURES 6 pixels, SATUR_LEVEL 64511 ADU, GAIN 2 e-/ADU) -> PSFEx selects unflagged point-like sources (SAMPLE_FWHMRANGE, SAMPLE_MINSN, SAMPLE_MAXELLIP = 0.05 for single dithers, 0.2 for stacks; SAMPLE_FLAGMASK 0x00fe, SAMPLE_IMAFLAGMASK 0x0001; centres from XWIN/YWIN_IMAGE) and models the profile as polar shapelets (Gauss-Laguerre basis) with global chi2 minimisation (Appendix C).
5. Tuning (Appendix C, Table A.2): BASIS_NUMBER (n_max; N_max = (n_max+1)(n_max+2)/2 basis vectors), BASIS_SCALE and PSF_ACCURACY tuned per band to minimise scatter and slope of MAG_PSF - MAG_APER vs MAG_APER. Science single dither: n_max 5/9/5 (N 21/55/21) for YE/JE/HE; stacked: 9/9/7 (55/55/36); calibration (extended): 36/40/40 (N 703/861/861). BASIS_SCALE: 1.40/1.38/1.70 (sci), 2.10/2.05/2.10 (stack), 1.35/1.40/1.57 (calib). Selection FWHM ranges in detector pixels: e.g. calibration 1.45-1.70 (YE), 1.55-1.80 (JE), 1.82-1.98 (HE).
6. PSF constant within each detector (no significant improvement from polynomial variation), variable between detectors (p. 3, 12).
7. The PSF models feed the NIR astrometric calibration (centroids) and the photometric calibration (aperture corrections -> zero points) (p. 3).
8. PSF-fit photometry uses SourceExtractor's MAG_PSF with the detector PSF model; fixed-aperture MAG_APER is the validation reference (Gaia was considered but has larger scatter) (p. 7).

## Validation and performance
- EE curves: all within requirements (Sect. 4.2, Table 1, Figs. 2, 4); model wings are slightly wider than the wavefront-based MDB models, expected because of pixelisation, IPC, IPS and jitter; MDB + IPC + IPS alone cannot reproduce the observed profile.
- Stacked-frame PSF models "not optimised": EE reaches 100% at ~1" for HE but at much larger radius for YE and JE (unexpected); the first diffraction rings in the models do not match the stacked stamps (HE brightest, YE faintest); small negative pixels (> -0.0015 YE, > -0.0008 HE) from PSFEx resampling; model size (3") smaller than the extended one (pp. 4, 14).
- PSF vs aperture photometry (Sect. 4.3): new catalogue code (lower initial detection threshold, adaptive threshold, extra spurious filter) and extended PSFs reduce scatter and slope; stacked catalogues show no significant change from Q1 to DR1 because stacked PSF fitting was already cleaner (flatter background, lower noise) (pp. 8-10).
- Sub-pixel dependence: MAG_PSF becomes brighter than MAG_APER as the centroid moves from pixel centre to pixel edge (up to systematic offset ~0.05 mag overall); caused by the PSF-fit sensitivity to sampling, amplified by IPC and IPS; MAG_APER is flat. PSFEx normalises models via a reference flux (default FLUX_APER) which also contributes to the offset (Sect. 4.3.2, Fig. D.2).
- SPREAD_MODEL vs SNR_WIN (Fig. 9): compact sources should lie at |SPREAD_MODEL| < 0.002-0.003; stars do not follow a perfect vertical locus (especially YE, HE; JE asymmetric) => PSF models still improvable (p. 11).
- Brighter-fatter effect: FLUX_RADIUS grows for brighter sources (Fig. 10); BFE is NOT corrected in the NIR PF (it is in the VIS PF, McCracken et al.), so bright sources may have slightly overestimated flux (p. 12).
- Time/position/wavelength: encircled-energy curves from different SCF visits (Jan vs Apr 2025) show larger differences than detector-to-detector differences (Fig. 11); ellipticity within 0.05 over > 180 days (Fig. E.1); monitored by the NIR DQC pipeline (Appendix E) via r_EE50, r_EE80, FWHM(x,y), ellipticity, number of sources.

## Known issues, caveats, limitations
- PSF stamp extent: ~3" (scientific/stacked) or ~7" (extended, single-dither only) vs the spikes of NISP which are long; 1-2% of the flux is outside even the 7" stamp (p. 8). No model of the far wings or scattered light beyond that. Stacked models (the ones relevant for mosaics) are only 3" wide and currently the weakest (p. 4, 14).
- Stacked PSF models: wrong EE growth, wrong diffraction rings, negative pixels, based on few sources and few basis vectors (pp. 4, 11, 14).
- Constant PSF within each detector; no wavelength (SED) dependence within a passband (models are broad-band; recommendation to use different models for different spectral types is "future work") (pp. 3, 14).
- IPC/IPS kernels are simplified and constant across the FoV although they in reality vary with position, temperature, signal, wavelength (p. 4); BFE is uncorrected.
- MAG_PSF vs MAG_APER systematic offset (~0.05 mag in DR1 PSF-fit photometry with extended models) that depends on sub-pixel position: the authors recommend applying a correction to MAG_PSF of point-like sources until fixed (p. 10).
- Spurious detections remain in NIR catalogues (persistence residuals, noise, unflagged saturated/cosmic pixels, diffraction spikes) (p. 10).
- Q1 NIR PSF models were too large; Q1 vs DR1 comparisons show improvement for single dithers. Kuemmel notes DR1 MER NIR PSF FWHM now agree to ~percent with Gaia stars (Q1: +1.75-3.5%).
- NISP 6-pixel aperture photometry requires the aperture correction of Table 1; the correction applies per detector during absolute calibration.
- Analysis of VIS PSF is not in this paper (see McCracken et al.).
- Results derive from a single SCF visit processed with a specific code version; retuning with more recent data is required (p. 12).

## Implications for extended-galaxy photometry, 2-D modelling and low-surface-brightness work
- Relevance is indirect: the DR1 NIR PSFs are inputs to MER for the mosaics (kuemmel limits PSF stamps to 5" and does not renormalise them). For Sersic/bulge-disc fits in YE, JE, HE the core of the PSF (FWHM ~0.46-0.51" in the stack) is adequate (EE radii agree with requirements, FWHM agrees with Gaia stars to percent level), but the stacked-frame PSF models have wrong diffraction rings, are undersampled and have no wing information beyond ~3".
- LSB: no information on the PSF wings at > 7" (single-dither) or > 3" (stack), no scattered light model, no ghosts. The paper does state ~1-2% of the flux of a point source lies outside the 7" stamp in the NISP bands (diffraction spikes), which sets the order of magnitude of the missing PSF flux; for stellar haloes and ICL in NIR you should build empirical large-radius PSFs from bright stars yourself. The VIS PSF paper (McCracken) may give the IE wings.
- The 6-pixel (1.8") aperture contains 92-94% of the flux (single dither) so aperture photometry of galaxies relies on aperture corrections derived for stars; NIR zero points are tied to this.
- The brighter-fatter effect not being corrected in NISP can slightly inflate bright stellar fluxes and PSF widths; relevant when using bright stars to build custom PSFs (choose unsaturated stars, avoid the brightest).
- Galaxy shape/size measurements in the NIR bands from MER Sersic fits depend on this PSF; the slight overestimate in PSF width for Q1 is reduced in DR1.
- Detector-to-detector variations are small (EE curves nearly coincide); positional PSF variation within a detector is not modelled. For NISP, the stack mixes detectors, so the stacked PSF is a variable average.

## Practical recommendations for users
- Use the extended (7") single-dither PSFs if you need detailed NISP PSF shape, otherwise the MER-propagated mosaic PSFs.
- Do not trust the stacked PSF models outside the central ~3" or for diffraction-ring details; consider constructing your own PSF from stars in the mosaic.
- If using NIR catalogue MAG_PSF for point-like sources, apply the offset correction recommended by the authors (about 0.05 mag, band-dependent; derive from MAG_APER).
- For aperture photometry with the DR1 multi-aperture set (radii 0.6, 0.9, 1.5, 2.25, 3") use the aperture corrections from the PSF models (Table 1: 6-pixel aperture = 1.06-1.08 single-dither).
- Be careful with bright saturated stars (BFE, diffraction spikes, spurious detections).
- Check SPREAD_MODEL for star/galaxy classification only as a rough guide: |SPREAD_MODEL| < 0.002-0.003 compact; positive = extended; negative = artefacts.

## Objects, fields and figures worth revisiting
- Fields: SCF (CALBLOCK-F-001) and photo-z calibration field (CALBLOCK-F-005) observations listed in Table A.1 (Obs. IDs 519, 2174, 6185, 10614, 2955, 4876-4983, 6125-6141; Patch IDs 8, 41, 131, 255, 56, 98, 129). No sky coordinates are given and no individual galaxies are studied.
- Fig. 1 (p. 5): extended PSF models (rings, spikes, coma, trefoil) vs median star stamps; Fig. 2 (p. 5): cross sections and EE curves; Fig. 3-4 (p. 6): stacked PSFs; Table 1 (p. 7); Figs. 5-7 (pp. 8-9): PSF-fit vs aperture; Fig. 8 (p. 11): multi-aperture EE curves; Fig. 9-10 (p. 12): SPREAD_MODEL and BFE; Fig. 11 (p. 13): time variation; Appendix A tables (pp. 21-22): PSFEx and SourceExtractor configuration.
- Essential page to view if needed for wings: p. 5 (Fig. 1) and p. 6 (Fig. 3, stacked) - not viewed here.

## Cross-references
- Polenta et al. 2026a,b (NIR PF / OU-NIR), McCracken et al. 2026 (OU-VIS incl. VIS PSF and BFE correction), Kuemmel et al. 2026 (MER: PSF propagation to mosaics, 5" stamps, normalisation), Jahnke et al. 2025 (NISP instrument), Schirmer et al. 2026 (calibration blocks, SCF), Kubik et al. 2026 (persistence), Radovich et al. 2026 (NIR astrometry), Ruffenach et al. 2026 (processing).
- External: PSFEx (Bertin 2011), SourceExtractor (Bertin & Arnouts 1996), polar shapelets (Massey & Refregier 2005).
