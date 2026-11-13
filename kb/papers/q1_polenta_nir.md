---
title: "Euclid Quick Data Release (Q1): NIR processing and data products"
short_name: polenta_etal
first_author: Polenta
series: "Euclid Q1 coordinated release (2025); reference for DR1 processing"
local_pdf: ~/Desktop/euclid/papers_q1/polenta_etal.pdf
local_text: ~/Desktop/euclid/text/papers_q1/polenta_etal.txt
topics: [NISP, NIR PF, YE JE HE, SExtractor background, over-subtraction, persistence, PRNU LED flat, large-scale flat, bad-pixel mask, DQ bits, PSF PSFEx, inverse sensitivity, white dwarf calibration, Q1]
relevance_extended_galaxies: high
---

# NIR processing and data products at Q1 (Polenta et al. 2025; A&A 2026)

## TL;DR
Q1 description of the NISP photometric processing function (NIR PF) that the DR1 NIR paper revises (see polenta.md). It covers detector-level corrections, LED-flat PRNU, the self-calibration-based large-scale flat, a SExtractor-style background map (64x64 px boxes, 3x3 median filter, delivered separately and not subtracted), PSF models from PSFEx, Gaia astrometry, and white-dwarf-based absolute flux calibration (images in electrons, inverse sensitivity in microJy per e-/s). The authors explicitly warn that this background over-subtracts extended bright galaxies and limits LSB studies, and promise a refined method for DR1 (DR1 now uses NoiseChisel; see polenta.md). Persistence is only masked, not corrected, and a diffuse residual persistence pattern is suspected in the data.

## Key facts and numbers
- NISP-P (p. 2-3): 16 H2RG detectors of 2048x2048 px (science area 2040x2040 in Level 2 coordinates), pixel scale 0.3"; photometric readout MACC(4,16,4) (4 groups of 16 averaged frames, 4 dropped); bands YE, JE, HE (950-2021 nm). Operating temperature 94 K.
- Q1 content (p. 18): 1620 raw exposures, 7 rejected by DQC (0.4%), 1613 delivered; 63.1 deg^2 in EDF-N, EDF-S, EDF-F and Dark Cloud.
- Dither statistics in the EWS: 1%, 8%, 40%, 42% of sky seen n = 1..4 times (p. 7); self-cal field up to 76 dithers.
- Astrometry (p. 18): residuals about 15, 12, 9 mas (YE, JE, HE) vs Gaia DR3; requirement 100 mas internal and 200 mas external; abstract quotes 9-15 mas. Distortion model: 3rd-order polynomial per detector with SCAMP, pre-solution from the 76-dither self-cal field (p. 15-16).
- Photometry (abstract, p. 11, 18): relative accuracy 5 mmag; after the large-scale flat the floor is at least 2-3 mmag; self-cal July vs August 2024 differences 2.9, 0.9, 0.7 mmag (YE, JE, HE), i.e. stable to better than 0.3% (p. 18); DET13 in YE has a drifting ZP, +0.02 mag in sky patch 71 (p. 18).
- Absolute calibration (p. 16): WD J175318.65+644502.15 (Gaia 1440758225532172032), HE = 18.36, tied to HST CALSPEC (1% accuracy); aperture of 6 px diameter, outside-aperture flux corrected with the PSF model; inverse sensitivity IS = F_true[uJy] / F_obs[e-/s]. Example from Fig. 14: HE IS = 0.335 +- 0.001 uJy per e-/s (June 2024 self-cal). NISP saturates near AB 16.5.
- PSF (p. 12-14): sampling 0.05" (1/6 NISP pixel), 40x40 px stamps in Fig. 11; PSFEx with Gauss-Laguerre basis (BASIS_SCALE/BASIS_NUMBER 1.4/5 YE, 1.38/9 JE, 1.7/5 HE), 30-40 stars per dither per detector; all-dithers mode default; encircled energy meets requirement rEE50 < 0.4" and rEE80 < 0.7" (p. 14). A 6 px aperture holds 99.99% (YE), 98.8% (JE), 99.7% (HE) of point-source flux. PSF-fit vs aperture magnitudes: HE better than 1%, JE PSF magnitudes brighter by about 3%, YE offset above 6% with larger scatter (p. 14).
- Persistence (p. 5-7): effective model, mask where the predicted charge exceeds 2 e-; typical masked fraction not above 2%.
- Linearity validity 1000-30 000 ADU, saturation expected at 40 000-50 000 ADU (p. 5).
- Cosmic rays (p. 6-8): LAcosmic single-frame (NIR_CrRejectionSingleFrame; COSMIC bit 16 + INVALID, 8 neighbours masked for inter-pixel capacitance) plus multi-frame pull-clipping (pull of 10 or more, needs 3 or more unflagged dithers; rejected if the 3x3 sums agree within 3%).
- Large-scale flat (p. 10-11): built from 76 dithers of the self-cal field; corrects 6-7 mmag of bright-star systematics; fit underfits (Rloss about 3); residual features resemble diffuse persistence.
- Ghost/arc masking (p. 16): dichroic and filter ghosts flagged with GHOST (bit 18) + INVALID; arcs of radius about 1.7' for stars brighter than 11 mag flagged with PERSIST (bit 13) + INVALID.
- Catalogue extraction (p. 17): CuTEx-like second-derivative detection, SExtractor APER (3 px fixed radius; the 6 px diameter is the default aperture in NIR PF), AUTO and PSF photometry; 16 detector layers plus primary (17 HDUs).
- DR1 timeline stated in paper: DR1 expected October 2026; NIR PF release for DR1 preparation scheduled end of 2025 (p. 5, 19).

## Data products and data model
(Sect. 4, p. 17-18; Appendix B, p. 24; DPDD v1.1 nirdpd)
- DpdNirCalibratedFrame: MEF with 49 HDUs: primary header plus, for each of 16 detectors, SCI (image in electrons, header contains detector WCS and zero point), RMS, and DQ (bit mask). DataStorage = this MEF; BackgroundStorage = a FITS file with the same structure containing the background image (not subtracted from SCI); PsfStorage = two FITS files (PSF model and PSF image). QualityParams metadata used by the DQC pipeline.
- DpdNirCalibratedFrameCatalog: MEF with 17 HDUs, catalogue columns for coordinates, size, ellipticity, fluxes and magnitudes from APER, AUTO and PSF.
- No NIR stacks or stack catalogues in Q1 (made by MER, p. 2-3, 12); NIR stacks first appear in DR1 (polenta.md).
- DQ bit mask (Appendix B, p. 24): 0 INVALID (convenience), 1 OBMASK, 2 DISCONNECTED, 3 ZEROQE, 4 BADBASE, 5 LOWQE, 6 SUPERQE, 7 HOT, 8 RTN, 9 SNOWBALL, 10 SATUR, 11 NLINEAR, 12 NLMODFAIL, 13 PERSIST, 14 PERMODFAIL, 15 DARKNODET, 16 COSMIC, 17 FLATLH, 18 GHOST, 19 SCATTER, 20 MOVING, 21 TRANS, 22 CROSSTALK, 23 FLOWER, 24 VIGNET. Flags marked "Yes" in the invalid column raise INVALID: DISCONNECTED, ZEROQE, BADBASE, SUPERQE, RTN, SNOWBALL, SATUR, NLMODFAIL, PERSIST, COSMIC, GHOST, FLOWER (per the extracted table; check the PDF for exact column alignment). Informational flags in Q1: HOT and LOWQE not invalid (p. 5). INVALID pixels always give an odd DQ value (p. 4).
- Units: SCI in electrons; fluxes for calibration in e-/s; microJy via IS (zero point/IS in the SCI header) (p. 16, 17).
- Background map: separate FITS, same detector structure; 64x64 px grid spline-interpolated (see below).
- Static pixel-flag statistics per detector and dark current in Table 1 (p. 6).

## Processing and methods
Order of processing elements (Sect. 3):
1. Common NIR-SIR pre-processing (p. 3-8): baseline validation (64 dark exposures MACC(1,16,1) at 94 K; kTC noise map); channel gradients (top-bottom slope corrected with reference pixels on 6 channels; quadratic gradients in long spectroscopy ramps not correctable); bad-pixel master mask; non-linearity (per-pixel 4th-degree polynomial from LED fluences 1000-30 000 ADU, validity extends linearly beyond; includes gain conversion); persistence model and mask; master dark (87 s photo-darks, 548 s spectro-darks); cosmic-ray identification (single- and multi-frame).
2. Calibration (p. 8-16): PRNU from LED flats (LED B for YE, C for JE, D for HE; 30 LED flats per filter; propagator P converts a monochromatic LED flat to a broad-band flat; the LED Lambertian cosine illumination profile, about 10%, is not removed at this stage and is folded into the large-scale flat); masks for VIGNET (detectors 11, 14, 24, 34, 44), FLOWER pixels (Laplacian kernel) and FLATLH (more than 50% deviation from the median of the 30 frames).
3. Large-scale flat and relative detector sensitivities: model m_{i,d}(x,y) = m_i + LSF_d(x,y) + s_d fitted in magnitudes from 76 dithers; resolution element 200x200 px; applied to science images in NIR_SelfCalib (p. 10-11).
4. Background estimation (Sect. 3.2.3, p. 11; highest-priority item): see below.
5. PSF modelling (physical-optics MDB mode for single exposures; in-flight PSFEx mode as default) (p. 11-14).
6. Astrometric calibration (SCAMP vs Gaia DR3, pre-solution, conversion PV <-> SIP) (p. 14-16).
7. Absolute flux calibration with the white dwarf (p. 16).
8. Ghost and arc masking (p. 16); catalogue extraction (p. 16-17); DQC (p. 17).

Background estimation (p. 11), all details given:
- Built with SourceExtractor (not NoiseChisel in Q1). Local background in rectangular boxes of 64x64 pixels (19.2" on the 0.3" NISP pixels) by iterative clipping of the pixel histogram until convergence at 3 sigma around the median; value set to the mode = 2.5 median - 1.5 mean (Eq. 11).
- The grid of box values is median-filtered with a 3x3 box (to remove high estimates caused by bright stars) and spline-interpolated to full resolution.
- Not subtracted from the calibrated science image; stored as a companion file in BackgroundStorage. MER later subtracts it per exposure before co-adding (Romelli p. 5) and then applies its own 256x256 px mesh step on the mosaic.
- No source mask is mentioned for this background step (only the median filter and sigma clipping protect against sources); no iteration beyond the clipping.
- Authors' statement: consistent for compact and faint objects but "considerable over-subtraction" for extended, bright galaxies, limiting LSB and diffuse targets; a more refined method promised for DR1 (p. 11, again in the conclusions: positive correlation between the estimated background and the position of very bright objects, over-subtraction in the outskirts of extended objects, limiting both LSB measurements and their detection; p. 18).
- Status in DR1 (from polenta.md): NoiseChisel v0.16 (quantile threshold 0.3, 10x10 px tessellation, Manhattan interpolation, 3 px flat kernel) replaces the SExtractor estimate; the background is still supplied separately and subtracted before stacking; residual 1/f striping and persistence-like patterns remain.

## Validation and performance
- Astrometry vs Gaia and overlaps (p. 18-19, Fig. 15-16): residuals of 15/12/9 mas; focal-plane dependence below 1/10 pixel except one YE detector.
- Photometric focal-plane map (sky patch 71, Fig. 17, p. 18-20): no major structure; DET13 in YE +0.02 mag.
- Stability from monthly self-cal visits (Fig. 18, p. 18): 2.9/0.9/0.7 mmag.
- Repeatability with and without large-scale flat (Fig. 10, p. 11): 6-7 mmag corrected, 2-3 mmag floor.
- Absolute IS uncertainty 3 sigma inside 5% (Fig. 14).
- PSF-vs-aperture photometry check (Fig. 13, p. 14-15).
- DQC pipeline (p. 17): PASS/FAIL/WARN/N/A reports per processing order using PSF quality, flagged pixel percentage, astrometric rms, background level and photometric zero point; metadata-based so it cannot capture all effects; visual inspection found diffuse arcs from internal reflections not modelled (p. 19).

## Known issues, caveats, limitations
- Background: over-subtraction around extended bright galaxies (p. 11, 18). DR1 switches to NoiseChisel; remaining over-subtraction possibility still noted in polenta.md for galaxies filling a detector.
- Persistence: only persistence from the previous spectroscopic exposure is modelled (photometric-to-photometric persistence and spectroscopic masking not used in Q1); 2 e- threshold; the model ignores superposition of exposures and charge trapping; residual streaks and a diffuse, low-level persistence-like pattern (probably from alternating zodiacal levels through the filter/grism sequence) leak into the flats and the photometry (p. 6, 11, 18). In DR1 an in-flight persistence model with longer look-back and conservative masks replaces it (polenta.md).
- Large-scale flat underfits (Rloss about 3) and effectively absorbs persistence-like residuals multiplicatively (p. 11); Q1 relative photometry floor 2-3 mmag.
- Ground-based calibration products (bad-pixel baseline updated in flight only for BADBASE; calibration data from PV not reflected) (p. 4, 19); non-linearity validity limited to the TV1 fluence range (p. 5); DR1 expands it.
- PSF: Q1 models are tuned on EWS stars in 3"x3" stamps with tens of basis vectors; PSF wings poorly characterised; a better PSF from the self-cal field with larger stamps (7"x7") and hundreds of basis vectors was being prepared (p. 14, 18); PSF photometry is available only for bright sources and is offset in YE by more than 6% (p. 14). In DR1 PSFs are derived from the self-cal field (polenta.md; dasilva.md).
- Ghost handling: only dichroic and filter ghosts and the star arcs masked; other ghosts and internal-reflection arcs remain (p. 16, 19).
- Detector baseline gradients: quadratic channel gradients cannot be corrected; six channels corrected linearly (p. 4).
- Only one visit per Q1 field; NISP saturates near AB 16.5 (p. 16).
- Hot and low-QE pixels are tracked but not invalid; DARKNODET is informational (p. 5, 7).
- NIR stacks, resampling kernel and stack PSFs are not covered (MER; DR1 NIR PF uses SWarp with Lanczos-2 for its own stacks per polenta.md).
- Background estimate is per detector and per exposure; vertical/horizontal striping from readout correlations (1/f) is not addressed here (see DR1).

## Implications for extended-galaxy photometry, 2-D modelling and low-surface-brightness work
- In Q1 NIR the sky was subtracted with a 19.2" mesh and a 3x3 median filter (about 58") per exposure, without a source mask, before the MER mosaic step (256 px at 0.1" = 25.6" mesh). Combined, this removes extended emission on scales above about 0.5' (independent finding in q1_icl_processing_bamford.md) and cannot be undone from the mosaic; only calibrated frames plus the delivered BackgroundStorage map allow a restart.
- The authors themselves say the Q1 NIR product is not appropriate for LSB features of bright extended galaxies. For DR1 the improved NoiseChisel estimate should help but still is a local, source-masked per-detector estimate (polenta.md).
- Persistence ghosts and the large-scale-flat residuals add additive errors on scales of 100-200 px (the cluster-ICL paper estimates about 5% additive structure in NIR, not this paper); if your NIR outskirts show diffuse structure at detector or dither scales, suspect these first.
- Convert to flux: SCI is in electrons; divide by exposure time to get e-/s and multiply by IS (microJy per e-/s; HE about 0.335 from the example figure; the actual IS and ZP are in the SCI header) to get microJy; mag_AB = 23.9 - 2.5 log10(F/uJy); mag/arcsec^2 needs the pixel area (0.09 arcsec^2 for 0.3" native pixels).
- PSF model and PSF magnitudes: use the PSF only for point sources; PSF wings are underestimated, which matters for halo and 2-D Sersic deconvolution in NIR (the MER PSF stamps in Q1 were too compact by 1.75-3.5%, see q1_romelli_mer.md).
- Astrometric accuracy (9-15 mas) and relative photometry (5 mmag) are ample for multi-band galaxy structure.

## Practical recommendations for users
- Do use the DQ mask (INVALID bit 0 plus PERSIST 13, GHOST 18, COSMIC 16) and RMS with each detector layer; do not use PERSIST-affected pixels for faint outskirts.
- Do fetch the BackgroundStorage file if you want the background that was subtracted in the Q1 mosaics; do not expect SCI to be sky-subtracted.
- Do treat NIR LSB measurements in Q1 data of bright extended galaxies as lower limits on faint emission; do not rely on stacks.
- Do convert e- to microJy with the IS and exposure time from the header rather than assuming a global constant.
- Do not use NIR PSF photometry in YE for accurate fluxes in Q1 (6% offset); do not trust single-visit zero points per detector better than about 0.02 mag in YE DET13.

## Objects, fields and figures worth revisiting
- White dwarf WDJ175318.65+644502.15 in the self-calibration field near the NEP (17h53m18.65s, +64d45'02.15"), HE = 18.36 (p. 16).
- Observation ID 3800 (EWS) used for PSF models in Fig. 11 (p. 13); sky patches 49 and 71 for photometric residual maps (p. 18).
- Figures: Fig. 4 (persistence masking scheme, p. 7); Fig. 8-10 (flats and large-scale-flat residuals, p. 10-13); Fig. 9 shows large-scale flats for 14 June 2024; Fig. 13 (PSF vs aperture photometry, p. 15); Fig. 14 (IS vs counts, p. 17); Fig. 18 (stability, p. 20). No figure shows the background subtraction around a large galaxy (the DR1 paper's NGC 1483 comparison does; see polenta.md).

## Cross-references
- polenta.md (DR1 NIR paper), q1_romelli_mer.md (MER subtraction of this background and mosaicing), q1_mccracken_vis.md (shared large-scale-flat code), q1_icl_processing_bamford.md (tartan, atemporal background, persistence mitigation), dasilva.md (NISP PSF), kubik.md (NISP detectors/persistence), schirmer-calibration.md, lebrun.md and fumana.md (SIR).
- Q1 NIR DPDD (nir_calibratedframe card) for the DQ definition; Morris and Kubik 2022 for the common NIR pipeline flags.
