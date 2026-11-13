---
title: "Euclid Data Release 1 (DR1): SIR spectroscopic calibration"
short_name: fumana
first_author: Fumana
series: A&A Special Issue DR1-Foundation (Nov 2026)
local_pdf: ~/Desktop/euclid/papers/fumana.pdf
local_text: ~/Desktop/euclid/text/papers/fumana.txt
topics: [NISP-S, slitless spectroscopy, grisms, SIR calibration, wavelength solution, flux calibration, geometric models, white dwarf standard, planetary nebula]
relevance_extended_galaxies: low   # for photometry / 2-D modelling / LSB of low-to-intermediate-z galaxies
---

# SIR spectroscopic calibration pipelines and accuracy (Fumana et al. 2026)

## TL;DR
Describes the calibration pipelines (not the science extraction) that feed the SIR spectral pipeline for DR1: geometric models (focal-plane metrology, optical, curvature, PSF, inverse dispersion) and spectro-photometric models (detector scaling, relative flux, absolute flux). It states DR1 spectra (>170 million validated spectra in red and blue grism modes, p. 1) meet the mission wavelength (0.3 px) and flux-stability (0.7%) requirements, with known weak points (FPA metrology, GWA jitter, ice-driven flux drift in the blue grism, band edges). For a galaxy-imaging group this is background: it tells you how far to trust wavelengths and fluxes of the 1-D spectra, and which spectral edges to mask. It says nothing about imaging photometry.

## Key facts and numbers
- NISP-S covers 950-2000 nm with a 4-grism wheel: three red (RGS000/180/270) and one blue (BGS000). RGS270 is non-conforming and unused in surveys (p. 2).
- Euclid Wide Survey (EWS) uses RGS000 and RGS180 only: nominal range 1206-1892 nm, dispersion 1.372 nm/px, R > 480 for a 0.5" diameter source (p. 2). Requirement driver: R >= 380 for sigma_z/(1+z) <= 0.001 and Halpha flux limit ~2e-16 erg/s/cm2 (p. 1).
- Four red grism-tilt configurations per reference observing sequence (ROS): RGS000+0, RGS180+4, RGS000-4, RGS180+0 (extra +/-4 deg tilt for decontamination) (p. 2).
- Euclid Deep Survey (EDS) also uses the blue grism: 926-1366 nm, 1.239 nm/px, R > 400 (p. 2). Five grism-tilt configs calibrated independently (4 red + BGS).
- Spectrogram length ~530 px (RGS) and ~350 px (BGS) (p. 5). Detector mosaic 4x4 with gaps of ~6 mm (along dispersion) and ~3 mm (across); sources in gaps give split spectra (p. 1, 3).
- Only first and zeroth orders are modelled in DR1; orders -1 and +2 (peak flux at percent level of the main orders) are ignored, including in decontamination (p. 4).
- Calibration fields (all from performance-verification phase): CALBLOCK-PV-001 (self-calibration star field; 4 visits x 15 frames per RGS config, 16 per BGS), PV-009 (planetary nebula SMC-SMP-20, 5-point quincunx on each of 16 detectors = 80 positions per config), PV-003 (white dwarf GRW+70 5824, flux standard) (p. 2). DR1 calibration uses PV data only; repeat visits (CALBLOCK-F-001, F-010) are not used (p. 2).
- Wavelength accuracy: residuals 0.137-0.205 nm rRMS (Table 3, p. 11), below the requirement of 0.3 px = 0.40 nm (red) / 0.37 nm (blue) (p. 10). Median line-position residual scatter at the 0.15-0.2 px level (Fig. 1 colour scale up to 0.24 px, p. 3).
- Trace curvature (CRV) residuals: sMAD 0.13-0.16 px before, ~0.10 px after an ad hoc per-exposure, per-detector correction (Table 2, p. 10); requirement 0.3 px.
- OPT first-order reference residuals: sMAD 0.23-0.31 px along dispersion, 0.135-0.16 px across (Table 1, p. 10); zeroth order ~0.12-0.14 px.
- Flux calibration: sensitivity curve from 80 single-dither WD spectra per config, formal relative error mostly < 1%, up to 1.5% at blue end of BGS, versus 0.5% requirement (p. 8). Uniformity across the FP confirmed at < 1% for most of the spectrum (p. 7).
- Flux stability test with ~6e5 Gaia stars in low-extinction (E(B-V) < 0.02) HEALPix tiles (Nside = 32): SIR/Gaia scaling spread <= 0.7% (Fig. 13, p. 11-12), consistent with the 0.7% clustering requirement (p. 11).
- Relative flux corrections reach ~10% locally for tilted grisms (vignetting) (p. 7). DR1 relative response taken as achromatic (wavelength-averaged map per config).
- Ice contamination: impact on RGS spectra <~1% over DR1; BGS variations potentially 5-15%, worst at the shortest wavelengths (p. 12).

## Data products and data model
Calibration products (documented in the DR1 Data Products Description; used internally by SIR, not science-level):
- DpdSirOptModel: sky (alpha, delta) to FP reference position for dispersion orders +1 and 0; 6x6 (L = 5) polynomial matrices; includes the effective FPA metrology (no stand-alone FPA product in DR1) (p. 4).
- DpdSirCrvModel: Chebyshev trace-curvature model, N = 3 (along-trace) and M = 2 (spatial FP) (p. 5-6).
- DpdSirSpectralPsfModel: cross-dispersion width sigma(x, y, lambda), Chebyshev in lambda and FP position (p. 6).
- DpdSirIdsModel: inverse dispersion solution lambda to offset delta-x; M = 4, N = 3 (RGS) or N = 2 (BGS) (p. 6).
- DpdSirDetectorScaling: ground-based QE scaling, combined with per-exposure zodiacal spectrum estimate (no in-flight version yet) (p. 6).
- DpdSirRelativeFluxScaling: wavelength-averaged 2-D relative flux map per config (p. 7).
- DpdSirAbsoluteFluxScaling: sensitivity function (e-/s/A per erg/s/cm2/A) per config, with mask bits: NOT_USE (outside 25% of band-edge throughput) and ABS_FLUX ("suspicious", between 25% and 85% of band-edge throughput) (Fig. 5, p. 8).
- Quality-control (DQC) parameters embedded in products (p. 8).
- SIR works in a rotated frame (X, Y)_SIR = (+Z, -Y)_MOSAIC with spectrograms near horizontal (p. 3). Input source positions come from the MER catalogue.
- The 1-D spectrum product format and redshift catalogue are NOT described here (see SIR-DR1 / Scodeggio et al.).

## Processing and methods
1. FPA: 16 per-detector linear WCS transforms; DR1 only rigid translations (CRVAL1/2 adjusted) fitted against a fifth-order global WCS using astrometrically calibrated photometric frame and bright point sources (p. 3-4).
2. OPT: pointing registration on zeroth orders (DAOStarFinder, iterated ~3 times), zeroth-order polynomial fit, then first-order fit using stellar absorption features (blended Mg I 1504 nm for RGS, Pa-beta 1282 nm for BGS) of 2MASS stars with J = 12-16; ~30% of fits rejected; 4300-5400 sources per config (p. 4-5).
3. CRV: cross-dispersion slices every 10 px, Gaussian-error-function fit, local Chebyshev per source, global 2-D Chebyshev over the FP (> 5500 sources) (p. 5). During DR1 production an extra per-exposure/per-detector sub-pixel correction was needed because of metrology errors and GWA jitter (<~0.1 deg RMS) (p. 5, 11).
4. PSF: sigma(x, y, lambda) from the same slices; no meaningful resolution difference between red grism-tilt configs (p. 6).
5. IDS: Gaussian centroids of 11 (RGS) or 7 (BGS) tabulated emission lines of PN SMC-SMP-20 at 80 FP positions, local Chebyshev then global 2-D model (p. 6).
6. Flux: detector scaling (ground QE + zodiacal), self-calibration RFX using stars 16 < HE < 18, AFX from pull-clipped average of 80 WD spectra divided by CALSPEC model grw_70d5824_mod_001 (smoothed to 3.3 nm) (p. 7).

## Validation and performance
- Geometric residual statistics in Tables 1-3 (p. 10-11), maps in Figs 8-9; all within 0.3 px requirement; larger deviations at edges of some detectors owing to FPA limitations (p. 9).
- Detector 41 (corner) shows structured FPA residuals of 0.79 +/- 0.22 px versus 0.22 +/- 0.14 px for detector 22 (Fig. 7, p. 9); mitigated by OPT.
- IDS: 1282.596 nm line is problematic (blended with 1279.281 nm) with sMAD sometimes > 0.3 px, attributed to measurement not model (p. 10).
- Flux: sensitivity relative error and Gaia-based stability (above). Moire fringing in tilted-grism WD extractions adds a small (< 0.5%) ripple in final sensitivity for tilted RGS (p. 8).

## Known issues, caveats, limitations
- Band edges: spectral pixels outside 25% throughput flagged NOT_USE, between 25% and 85% flagged ABS_FLUX (suspicious); DR2 will narrow to 25-50% (p. 8, 11). FP-dependent sensitivity variations at band edges can add noise for a few pixels (p. 7).
- Extra low-frequency/Moire pattern from resampled, undersampled PSF in bright-source optimal extraction; optimal extraction is sensitive to cross-dispersion mis-centring and underestimates flux of ~5% of bright WD spectra (p. 8).
- Relative flux map assumed achromatic and time-invariant; time variability not measured for DR1 (p. 7).
- Detector-scaling (QE) is from ground data, no in-flight calibration yet (p. 6).
- Orders -1 and +2 not modelled; split spectra in detector gaps need the global geometric model.
- Time evolution not included (PV-only calibration); ice contamination: <~1% RGS, 5-15% BGS at shortest wavelengths (p. 12).
- Wavelength zero-point can absorb OPT x-offsets via the IDS zero-point term (p. 9). Global polynomial IDS susceptible to Runge oscillations at FP edges (sparse 80 PN positions) (p. 11).

## Implications for extended-galaxy photometry, 2-D modelling and low-surface-brightness work
Essentially irrelevant to imaging photometry. Indirect points: (a) the spectral resolving power depends on source morphology (extended galaxies degrade R below the point-source/0.5" values, p. 1, 2), so line widths and redshift precision of resolved low-z galaxies are worse than the quoted R > 480; (b) the 4x4 mosaic gaps mean large galaxies can have partially lost or split spectrograms; (c) the flux calibration is tuned for point sources (stars/WD), so aperture/slit-loss corrections for extended galaxies are not covered here. Wavelength coverage for z < 1: the red grism (1206-1892 nm) catches Halpha only for z ~ 0.84-1.88, so most low-z galaxies show no Halpha in RGS; the blue grism (926-1366 nm, EDS only) covers Halpha for z ~ 0.41-1.08 (computed from rest wavelength, not stated in paper).

## Practical recommendations for users
- Respect the NOT_USE and ABS_FLUX bits at band edges of the 1-D spectra; do not interpret features in the outer ~25-85% throughput region.
- Treat blue-grism (EDS) fluxes with extra caution (ice-driven drift up to 5-15% at short wavelengths; 1.5% formal error at the blue end).
- Wavelength accuracy of ~0.15-0.2 nm (<0.3 px) is adequate for redshifts; velocity offsets/kinematics at the level of a few tens of km/s are not guaranteed.
- Flux uniformity across the survey ~0.7% for point sources; add a systematic for extended sources.

## Objects, fields and figures worth revisiting
- Calibration targets (coordinates not given in text): planetary nebula SMC-SMP-20 (wavelength standard, PV-009); white dwarf GRW+70 5824 (flux standard, PV-003); self-calibration field CALBLOCK-PV-001; EDF-N and EDF-S faint WDs planned as secondary standards (p. 11).
- Fig. 1 (p. 3): quincunx PN pattern and IDS accuracy map. Fig. 3 (p. 6): PN spectrum with reference lines. Fig. 5 (p. 8): sensitivity curves and mask boundaries. Fig. 13 (p. 12): flux stability. Tables 1-3 (p. 10-11).

## Cross-references
- SIR-Q1 (Copin et al. 2026) and SIR-DR1 (Scodeggio et al. 2026, science pipeline; spectral extraction, formats, ad hoc CRV correction).
- Schirmer et al. 2026 (spectroscopic calibration strategy/DR1 overview), Gillard et al. 2026 (ground calibration), Kubik et al. 2026 (detectors), Polenta et al. 2026a,b (NIR pre-processing, astrometry), Kuemmel et al. 2026 (MER catalogue), Jahnke et al. 2025 (NISP), Tereno et al. 2026 (EWS).
