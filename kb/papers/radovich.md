---
title: "Euclid Data Release (DR1): NIR astrometric calibration"
short_name: radovich
first_author: Radovich
series: A&A Special Issue DR1-Foundation (Nov 2026)
local_pdf: ~/Desktop/euclid/papers/radovich.pdf
local_text: ~/Desktop/euclid/text/papers/radovich.txt
topics: [NISP, astrometry, SCAMP, Gaia DR3, distortion, PV, SIP, WCS keywords, aberration, parallax, persistence masking, DET13, DET14, overlaps]
relevance_extended_galaxies: medium
---

# NIR astrometric calibration (Radovich et al. 2026)

## TL;DR
Documents how the NISP (YE, JE, HE) WCS is computed per dither with SCAMP against Gaia DR3 and how good it is: mean precision ~10 mas (about 0.03 px at 0.3 arcsec/px), <20 mas for 99% of dithers, offsets <2 mas, meeting the 30 mas goal for 97% of area. Residual problem: excessive persistence flagging in DET13/DET14 degrades astrometry (>30 mas) in 3% of the area. For galaxy-photometry users this means NIR frames can be registered to VIS to well below a NIR pixel almost everywhere; the paper also lists the astrometric header keywords and the quality maps to identify bad regions. It says nothing about photometry or sky.

## Key facts and numbers
- NISP: 16 H2RG, 2048 x 2048 px, 0.3 arcsec/px, 0.57 deg2 FoV (p. 1). Wide survey OBSID = 4 dithers; self-cal field = 76 dithers (p. 1).
- Requirements: DR1/DR2: 200 mas RMS absolute (vs external), 100 mas relative; DR3 goal 30 mas per axis (0.1 px); distortion calibrated within 0.015% over 3 arcmin scales (p. 1).
- Result: mean RMS ~10 mas; offsets vs Gaia within 2 mas; <20 mas for 99% of dithers in all bands (p. 3); RMS decreases YE -> JE -> HE (YE ~15 mas, HE ~10 mas in stacks, p. 6), tied to PSF undersampling.
- Data sample: 4000 EWS OBSIDs per filter, 1950 deg2 after removing overlaps, Feb 2024-May 2025 (p. 3).
- Gaia reference stars G=15-21 (about 16-22.5 in NIR); Gaia epoch J2016.0 propagated with proper motion only; final positions barycentric ICRS (p. 2).
- Stack vs Gaia: median sigma ~10 mas, 95% within 15 mas (p. 5). Focal-plane residual offsets <5 mas in all bands (p. 6).
- Overlaps between adjacent stacks (>=50 arcmin2 overlap; 560 deg2 total): in 99% of overlaps sigma<25 mas, median offsets <10 mas (p. 7).
- Geometric distortion: for pairs separated 2.5-3.5 arcmin, RMS of fractional separation error <0.01%, 95% below 0.02% (requirement 0.015%) (p. 7).
- Position-angle dependence: sinusoid amplitudes 0.08-0.14 mas in RMS, <=0.08 mas in offsets; time trend 0.04-0.11 mas/yr (p. 5).
- Colour dependence: chromaticity slope R_xi < 1 mas/mag, R_eta << 1 mas/mag; <1 mas difference between low- and high-extinction stacks (p. 6).
- Aberration: plate scale changes follow expected stellar aberration, k = 0.997 +- 0.001 in wide fields (predicted displacement within +-100 mas; up to ~20 arcsec uniform shift near the NEP self-cal field); 68% of fields deviate from prediction by <2 mas (p. 8).
- Parallax: 152/126/157 probe stars in YE/JE/HE; k = 1.03+-0.11 (JE), 1.12+-0.16 (HE), 0.73+-0.29 (YE); zero-point offset ~-1 mas (-0.92+-0.49, -1.18+-0.52) in JE/HE (p. 9).
- Persistence problem: threshold 2 e- reduces Gaia matches from ~30 to a few per detector; RMS exceeds 30, 60, 90 mas in 3%, 0.3%, 0.1% of the area (vs VIS and Gaia, median RMS ~20 mas); NISP-to-NISP (vs HE) 1%, 0.2%, 0.1%; RMS<30 mas over >=97% of area vs VIS, 99% across NISP bands (p. 9). Individual detectors (mostly DET13, DET14) reach 60-150 mas in at most 0.15% of cases (HE) (p. 3).
- DR2 fix: discard a detection only if pixels within Rp=5 px of its centre exceed Ip=5 e- (p. 9-10).
- One third of dithers flagged invalid in the NIR PF are flagged at this astrometric step (p. 3).

## Data products and data model
No new products. Relevant header keywords written to calibrated frames (p. 2-3):
- WCS in PV formalism (SCAMP): CRPIX (reference pixel), CD (CD matrix: scale+rotation), PV keywords (3rd-order distortion polynomial amn, bmn), CRVAL (tangent point). Per dither and per detector.
- Quality keywords: ASTRNM (number of matched sources), ASTRELL (median ellipticity of matched sources), ASTROFF1/2 (average RA/Dec offset vs reference), ASTIRMS1/2 (standard deviation of residuals between dithers, i.e. internal), ASTRRMS1/2 (residuals vs Gaia reference). Computed per detector and per dither.
- Dither is flagged in validation if any dither-level ASTIRMS1/2 or ASTRRMS1/2 > 50 mas, or detector-level ASTIRMS > 50 mas (p. 3). Other tests: ASTRELL > 0.3 (or > twice the median over dithers) indicates FGS failure; detector with <5 detections or <10% matched fraction is unreliable.
- Spacecraft keywords used: VEL_X/Y/Z (barycentric velocity), POS_X/Y/Z (geocentric spacecraft position), CRVAL1/2 (p. 7-8).
- Region quality maps (VMPZ-ID InfoMaps) are based on the RMS maps (cross-ref Polenta). The pipeline module is NIR_AstrometricCalibration (NIR_Astrometry), using a re-engineered SCAMP, EL_ScampPP.

## Processing and methods
1. Distortion per dither because optics tilt and filter-centre offset make it vary between exposures (p. 2). PV model: (X,Y) = CD*(x-px, y-py); xi=sum a_mn X^m Y^n; eta=sum b_mn X^m Y^n; order N=3 (p. 2). SIP alternative (A_ij, B_ij) is rotation independent (p. 2).
2. External reference Gaia DR3, not VIS: VIS coverage incomplete, and VIS saturates for IE<18.5 whereas NISP saturates near AB~16 (p. 2).
3. Source catalogues from SExtractor + PSFEx (PSF-fit centroids); quality maps exclude saturated pixels, cosmic rays, persistence (p. 2).
4. Presolution (initial distortion from self-cal field, accuracy ~1 arcsec) converted PV->SIP->PV with the rotation absorbed by the CD matrix using analytic sympy-derived expressions (p. 2-3).
5. SCAMP first run only adjusts CRVAL; align with Gaia via presolution; per-dither QC tests (ellipticity, number of detections, match fraction); second SCAMP run for the full distortion (p. 3).
6. Validation: stacked catalogues per OBSID (independent from the calibration), strict mutual nearest-neighbour Gaia match with 1 arcsec maximum separation; residual maps in 2.5 x 2.5 arcmin cells (~1e4 detections per cell, 3 sigma clipping, >=100 detections) and 1 arcmin strips; offsets computed in instrument frame (xi, eta) to avoid dilution by rotation (p. 3, 6).
7. Aberration and parallax checks (Sect. 3.4-3.5): Gaia positions are propagated with proper motions only; aberration is absorbed in the fitted plate scale (delta s/s = v.n/c).
8. RMS map for persistence impact: 30 arcsec grid, moving window radius 4 arcmin (Gaia, >=10 matches) or 2 arcmin (VIS, >=20 matches), radius increased in 10 arcsec steps; match radius 5 arcsec; VIS sources with |spread_model|<0.05; map element = largest RMS over bands (p. 9).

## Validation and performance
See Key facts. Highlights: no systematic bias (offsets <2 mas); no focal-plane trends >5 mas; modest increase of scatter at stack edges because fewer dithers contribute (Fig. 4); distortion stable over time to ~10 mas, test using 15 self-cal visits of 76 dithers each comparing a fixed presolution with SCAMP distortions (Fig. 7); aberration and parallax consistent with expectation.

## Known issues, caveats, limitations
- Persistence masking (threshold 2 e-) removes Gaia reference stars in DET13/DET14, giving local RMS >30 mas (3% of area), >60 mas (0.3%), >90 mas (0.1%) (p. 9). The bright-star persistence maps appear in the RMS maps as small green/yellow spots (Fig. 10). Fix developed but not in DR1.
- FGS failures (elongated sources) and particle showers cause invalid dithers; the current ASTRELL threshold 0.3 might be lowered (passed dithers have mean ellipticity <0.16) (p. 3).
- YE is the most undersampled band and has the largest astrometric scatter (p. 3, 9).
- NISP-measured parallaxes show a possible ~-1 mas zero-point offset in JE/HE (marginal, ~2 sigma) (p. 9).
- Larger stack-edge residuals (reduced number of dithers) (p. 5).
- A constant distortion with only linear terms refitted is not sufficient; a second-order term would be needed (p. 10); distortion model in DR1 is a full cubic fit per dither, hence possible over-fitting in sparse detectors.
- Aberration is not corrected in the reference positions; it is absorbed into the plate scale (not a problem for relative work).

## Implications for extended-galaxy photometry, 2-D modelling and low-surface-brightness work
- Relevance is indirect. Astrometry at ~10 mas (0.03 NIR pixel, 0.1 VIS pixel) means NIR-VIS co-registration and cross-band (YE, JE, HE) alignment are good enough for multiwavelength Sersic/bulge-disc modelling and colour maps, apart from the 3% (RMS>30 mas) of area affected by persistence masking where you should check/refit offsets (0.1 NIR px).
- Positional accuracy at 30-60 mas in affected tiles might still blur PSF-matched colour gradients at the VIS resolution (FWHM ~0.14 arcsec): offsets of 60 mas are ~0.4 VIS FWHM. Re-register NIR cutouts to VIS locally for resolved-colour work.
- Persistence flagging in DET13/DET14 also means those detectors have extensive masked areas, which affects extended galaxies falling there.
- Relative pixel-scale effects: aberration changes the NISP plate scale by up to ~100 mas RMS over the FoV in wide fields; the calibrated WCS already absorbs it, so do not apply further scale corrections.
- No information here about background, flats, ghosts or scattered light.

## Practical recommendations for users
- Read ASTRRMS1/2, ASTIRMS1/2, ASTRELL, ASTRNM in each detector header to select reliable frames/detectors; treat >50 mas as bad.
- Use VMPZ-ID InfoMaps/RMS maps to avoid or locally re-register areas near DET13/DET14 with degraded WCS.
- Cross-match to Gaia with proper-motion propagation; remember Euclid positions are barycentric (no aberration correction) and parallax is retained in positions.
- For registration with VIS, consider an additional local offset fit; Gaia is the common reference of both instruments.
- Prefer HE/JE over YE for the best astrometry.

## Objects, fields and figures worth revisiting
- No named galaxies. Fields: wide-survey fields near 8-12 h, +60 to +75 deg and 1-5 h, +45 to +60 deg are shown in the RMS maps (Fig. 10, p. 10); the self-calibration field near the North Ecliptic Pole (RA ~17h54m, Dec ~+65 deg from companion paper white dwarf coordinates).
- Figures: Fig. 1 (distortion map, up to ~8-9 arcsec at edges, p. 2); Fig. 2 (dither/detector residual histograms, p. 4); Figs. 3-4 (focal-plane residual maps, p. 4-5); Fig. 8-9 (aberration, parallax, p. 8-9); Fig. 10-11 (persistence RMS maps and fix, p. 10).

## Cross-references
- Polenta et al. 2026 (NIR processing; persistence masking, products, quality maps); da Silva et al. 2026 (PSF); Kubik et al. 2026 (persistence; Ip=5 e-); McCracken et al. 2026 (VIS; used for validation); Jahnke et al. 2025 (NISP, detector layout and saturation); Schirmer et al. 2022, 2026 (optics, decontamination); Odier et al. 2026 (VMPZ-ID InfoMaps); Lindegren et al. 2021 (Gaia ruwe).
