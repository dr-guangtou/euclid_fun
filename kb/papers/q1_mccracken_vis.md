---
title: "Euclid Quick Data Release (Q1): VIS processing and data products"
short_name: mccracken_etal
first_author: McCracken
series: "Euclid Q1 coordinated release (2025); reference for DR1 processing"
local_pdf: ~/Desktop/euclid/papers_q1/mccracken_etal.pdf
local_text: ~/Desktop/euclid/text/papers_q1/mccracken_etal.txt
topics: [VIS, calibrated quad frames, NoiseChisel background, ADU units, zero point 24.57, gain 3.48, flag map, brighter-fatter, CTI, ghosts, large-scale flat, shutter, PSFEx, astrometry, quality control, Q1]
relevance_extended_galaxies: high
---

# VIS processing and data products at Q1 (McCracken et al. 2025; A&A 2026)

## TL;DR
Q1 reference for the VIS processing function (VIS PF) that DR1 only updates (see mccracken.md). It lists every pixel-level correction (bias, crosstalk, non-linearity, cosmic rays, BFE, PRNU, gain), the per-quadrant NoiseChisel background estimate (delivered as a separate map and subtracted by MER before stacking), the large-scale illumination flat, the Gaia-based astrometric and photometric calibration (images in ADU with ZP 24.57 and gain 3.48 e-/ADU), ghost flagging and the Q1 products. For LSB work the main facts are the multi-tier NoiseChisel strategy with an explicit statement that objects larger than one quadrant are over-subtracted in their inner regions, that no CTI or shutter correction is applied, and that ghosts are only flagged, not subtracted.

## Key facts and numbers
- Detector (p. 2-3): 36 CCDs, 4132x4096 px, 12 um pixels, pixel scale about 0.1" at FPA centre (intrinsic pixel-size variation under 1%); 4 readout nodes per CCD, 144 quadrants; frames delivered as 144-extension MEFs. Prescan 51, serial overscan 29, parallel overscan 20 px.
- ROS (p. 3): four dithers of 566 s nominal exposure plus two 95 s short exposures; EXPTIME 560.52 s and 89.52 s is the shutter-fully-open time; actual per-pixel exposure varies over the FPA (footnote 1).
- Stack: six images (4 nominal + 2 short), 2422 s per pixel, 10 sigma depth IE = 25.6 measured as variance in 1.3" apertures, versus requirement 24.5 (p. 12-13). VIS stacks are not delivered in Q1; MER tiles are used.
- Gain: 3.48 e-/ADU for Q1, after gain equalisation across quadrants (p. 8). Images are delivered in ADU (p. 8, 20).
- Zero point: 24.57 (quoted with units "s^-1", in ADU); it is the median of all per-exposure Gaia-derived zero points between 1 July and 1 September 2024 (p. 12, 20). Header keyword APERCOR holds the correction from the 13 px aperture to total magnitude (13 vs 50 px aperture ratio on non-blended stars; p. 12).
- Gaia-to-IE transformation (p. 12): C = G_BP - G_RP - 0.3406 (AB offset); IE = G + 0.1136 - (p0 + p1 C + p2 C^2 + p3 C^3 + p4 C^4) with p = (-0.00489071, 0.405557, -0.0256434, -0.0627437, 0.0204569); sources 18.5 < IE < 19.8 (nominal) and 16.5 < IE < 19.8 (short), 0 < C < 2.5, spread_model point-source selection, 13 px (1.3") aperture.
- Throughput history (p. 11-12): ice build-up on mirrors; decontamination on 12 March 2024 (FoM3 and M3 heated to 160 K) and 6 June 2024 (FoM3 only); a single ZP is inadequate, hence per-exposure Gaia ZPs.
- PSF (p. 8-9): PSFEx model from short exposures of the self-cal field (March 2024), 21 px stamps, second-degree polynomial per quadrant (PSFVAR_DEGREES=2, BASIS_TYPE=PIXEL_AUTO), Gaussian FWHM 0.157-0.164", mean 0.158" (sigma 0.001"); PSFEx PSF is slightly larger and rounder than reality due to undersampling; no chromatic dependence (p. 8).
- Image quality in Q1: FWHM about 0.16" stable (abstract); image-to-image photometric scatter 0.6-0.7% (requirement 1%) (p. 15); Gaia astrometric residual 5.5/5.7 mas (RA/Dec MAD) on an example image, 7/8 mas rms over all exposures, residual field below 8 mas (p. 11, 15); internal registration better than 1 mas.
- Q1 content: 852 VIS images in EDF-N, EDF-S, EDF-F and the Dark Cloud LDN1641; 16 rejected by QC (1.9%), 836 retained (p. 13).
- Cosmic rays: LACosmic (sigclip 10, sigfrac 0.4, objlim 20, cleantype medfilter; true-positive rate 78.3%, false-positive rate 0.03%, 1.1% of stars with IE < 20 misclassified); about 1.6% of pixels flagged in nominal images; quadrant with more than 5% CR pixels gets CR_REGION flag (p. 6).
- Blooming thresholds 40-61 kADU (mean 51 kADU); ADC limit 65 535 ADU (p. 4).
- Dichroic ghosts for stars with IE < 14, attenuation about 1e-6, offset a few hundred pixels; an IE = 5.5 star gives ghost pixels 3000-4000 ADU above background (p. 11).
- Shutter: 2.7 s to open/close, about 6% left-right flux gradient in short and 1% in nominal exposures; uncorrected magnitude error about 0.05 mag in nominal exposures before the large-scale flat; long exposures about 2% fainter than short ones after normalising by EXPTIME (p. 9-10, 16).
- Q1 calibrated frame catalogue aperture diameters 7, 13, 26, 50 px, DETECT_THRESH 1.5 (Appendix C, p. 21).

## Data products and data model
(Appendix A, p. 20-21; DPDD at the Q1 data-product-doc site)
- VIS calibrated quad frame (DpdVisCalibratedQuadFrame): three kinds of FITS file.
  - DET MEF with SCI, RMS and FLG extensions for each of 144 quadrants (quadrant order as in Fig. 1, p. 3). SCI: science image in ADU, gain 3.48 e-, zero point 24.57, for both nominal and short exposures. RMS: noise map = photon noise of the science image plus readout noise (both in electrons) summed in quadrature and converted to ADU; readout noise from the median of the standard deviations of the serial overscan. FLG: signed-integer quality image.
  - WGT: weight map = the small-scale flat (PRNU) with all INVALID pixels set to zero.
  - BKG: the NoiseChisel background map (not subtracted from SCI) (p. 20-21).
- FLG bit indices quoted (listing 1, p. 20): 0 INVALID (convenience flag combining most bad regions), 1 HOT, 2 COLD, 3 SAT, 4 COSMIC, 5 GHOST, 7 BAD_COLUMN, 8 BAD_CLUSTER, 9 CR_REGION, 12 OVRCOL, 15 CHARINJ, 17 SATXTALKGHOST, 21 ADCMAX, 22 NO_DATA; bit 18 STARSIGNAL and bit 24 OBJECTS mark object pixels. Other bits (for example stitch-block boundaries) exist but are not listed.
- Pixel flagging concepts (p. 4): ADC limit, saturated/blooming pixels, hot/dark pixels (6-7 sigma), stitch-block boundaries (512x256 px blocks), bad clusters and columns.
- VIS calibrated quad frame catalogue (SExtractor, 144 extensions): standard SExtractor columns plus calibrated fluxes in microJy with suffix _CAL (p. 21). Quadrant id CCD_QUADID is added in the merged validation catalogue (p. 14).
- Quality control per frame (xml + json, 144 quadrants): FPA_spreadmodel_peak (above 0.002 indicates guiding errors), FPA_spreadmodel_sigma, FPA_max_cr, FPA_fpa_cr, FPA_cr_regions, FPA_mean_residual, FPA_e1_med, FPA_e2_med, FPA_r2_med, SCORE (images with score above 60 get manual QC) (p. 13, 21).
- PSF model: delivered with the calibrated frames for use by MER (p. 3-4, 8); in DR1 the PSF model is part of the calibrated quad frame product (see mccracken.md).
- Stacked VIS images with weight map and catalogue are described but not delivered in Q1 (p. 12-13).
- Raw frames and calibrated frames are available through the Euclid Science Archive; "VIS calibrated frame" (CCD-grouped) is an older product (footnote 8, p. 20).

## Processing and methods
Pipeline order (Sect. 3-5; Fig. 2, 7, 14):
1. LE1 assembly of raw MEF with preliminary astrometric solution (p. 3).
2. Bad-pixel and saturation flagging (p. 4).
3. Crosstalk: 1584 coefficients, correction not applied for coefficients below 4e-5; maximum effect about 30 ADU (p. 5).
4. Bias (per-quadrant offset from overscan plus master bias from at least 60 frames) and dark (325 s darks; used mainly to assess stray light) (p. 5).
5. Non-linearity from LED pulses (correction applied from 300 ADU; 2-4% at high signal) (p. 5-6).
6. Cosmic-ray flagging with LACosmic (p. 6).
7. CTI: not corrected in Q1; modelled effect at end of May 2024 about -3e-4 fractional flux loss and 2e-3 px shift for a bright star far from the register (p. 6).
8. Brighter-fatter effect: 11x11 flux-conserving iterative kernel correction (convergence 1e-6), visible for IE < 19, not significant after correction (p. 7-8).
9. PRNU: small-scale flat from four-wavelength LED flats (10 kADU level), applied by division (p. 8).
10. Background estimation (Sect. 3.11, p. 8): see next list.
11. Gain equalisation to 3.48 e-/ADU (p. 8).
12. PSF model (PSFEx, p. 8-9).
13. Large-scale illumination flat (p. 10): built from 15 000 unique stars observed over 76 dither positions in the self-cal field by minimising magnitude differences; coarse grid of 3x3 cells per quadrant; derived separately for nominal and short exposures; accounts for shutter, QE, gain errors; normalised to the mean exposure time of the FPA, i.e. the relative shutter flux effect is not corrected in absolute terms (p. 16).
14. Astrometry: Gaia DR3 with proper motion, parallax and aberration; SIP-based FPA model then converted to TPV WCS in each of 144 headers (p. 10-11).
15. Photometric calibration with 13 px aperture + APERCOR (p. 11-12).
16. Ghost flagging by a position/brightness model from in-flight data; ghosts flagged by a flux threshold into the flag map, not subtracted (p. 11).
17. Stacking with SWarp and SExtractor catalogue (not delivered in Q1) (p. 12-13).

Background estimation, per quadrant (p. 8; highest-priority item):
- Tool: NoiseChisel (GNU Astronomy Utilities v0.16, Akhlaghi and Ichikawa 2015) run on each quadrant. It applies an initial threshold below the sky level and uses erosion/dilation to detect faint signal; the background is the mean of pixels outside detected sources; the stated goal is to preserve low surface brightness signal in stacks instead of subtracting it as background.
- Cosmic-ray pixels are set to NaN before the estimate (works up to about 15% CR pixels).
- Multi-tier fallback: if a quadrant contains considerable signal (large galaxy, cirrus), NoiseChisel is re-run with less restrictive options; if there is too little noise left in the quadrant, the SExtractor background map is used instead. The paper states that this results in over-subtraction in the inner regions of objects larger than one quadrant (a quadrant is about 2066x2048 px, i.e. about 3.4' x 3.4') and that this will be addressed in future versions (p. 8). It argues such objects are rare.
- NoiseChisel parameters used for Euclid (tile size, quantile threshold, kernel) are not given in this paper (DR1 VIS paper and DR1 NIR paper indicate NoiseChisel with small tessellation for NIR; check mccracken.md and polenta.md).
- Output: the background map is a separate BKG file; SCI frames are not background-subtracted (p. 20-21). The VIS background is subtracted by MER before the co-add (Romelli p. 5), then MER subtracts a second background (see q1_romelli_mer.md).

## Validation and performance
- PSF stability over time and across the FPA versus mission requirements (Fig. 9-10, p. 9-10); BFE effect on short vs nominal flux (Fig. 5-6, p. 7-8).
- Astrometry (Fig. 12, 18-19; p. 11, 15): external 5.5/5.7 mas on one image, 7/8 mas across Q1; Q1 distortion matrix not updated since PV, so residuals have a non-zero curl; later reprocessing improves this.
- Photometry (p. 15-16): repeat-observation scatter 0.6-0.7% over the mag range; corrected 13 px magnitudes agree with MER total magnitudes within 1% for IE < 19.5 (origin under investigation).
- Counts (p. 16, Fig. 21): galaxy counts in EDF-N/S/F consistent; cumulative counts reach about 30 arcmin^-2 and agree with COSMOS2020-based IE counts; three- vs four-image stack depth differs by about 0.2 mag.
- Quality control (p. 13-14): rejection thresholds on spread_peak, score, astrometric residual, CR_REGION coverage and ZP availability.

## Known issues, caveats, limitations
- Background: over-subtraction inside objects larger than one quadrant (p. 8); SExtractor fallback in the most signal-dominated quadrants; the delivered frames are not sky-subtracted (p. 20-21). Status in DR1 (from mccracken.md): NoiseChisel still used, slight over-subtraction still reported, stack built from background-subtracted exposures; not declared fixed.
- CTI not corrected (p. 6); in DR1 still not corrected.
- Shutter-induced exposure-time gradient not removed in absolute terms; nominal exposures about 2% fainter than short; 1% mismatch with MER total fluxes; planned fix with a shutter model (p. 16). DR1 still lists small shutter offsets.
- Ghosts only flagged, with an attenuation of 1e-6 relative to the star; unflagged or fainter ghosts remain (p. 11). DR1 reports unmasked ghosts still in deep images.
- Dichroic ghost model depends on the astrometric solution; blooming and serial bleeding around very bright stars exist; saturated pixels invalidate crosstalk victims (p. 4-5). DR1 notes serial-register bleeding bands still present.
- The VIS PSF model is simple (second-order polynomial, no chromaticity, slightly rounder and larger than the true PSF); real PSF is chromatic via dichroic and broad bandpass (p. 8, 13).
- Solar-flare proton showers give "X-ray" CR patterns; CR_REGION masks affected quadrants (p. 6-7).
- Distortion matrix from PV; larger residual curl in Q1 (p. 15).
- Large-scale flat built from only three visits in Fig. 11 (June-July 2024) and a self-cal field, so errors below 1 arcmin scales and time dependence are not constrained (p. 10).
- Flux normalisation: ZP is a single median over July-September 2024 although per-exposure ZPs vary.
- FLG bit names listed are a subset (p. 20).
- Q1 products do not contain stacks or a PSF wing characterisation.

## Implications for extended-galaxy photometry, 2-D modelling and low-surface-brightness work
- For galaxies larger than about 3' (one quadrant) the VIS per-exposure background is biased low inside the object by construction (Sect. 3.11); on smaller objects NoiseChisel is designed to protect faint extended signal. The BKG map is delivered, so you can add it back to SCI to obtain a not-subtracted frame; you then must handle the true sky yourself.
- The per-pixel units are ADU: flux in ADU/s per pixel times exposure normalisation (EXPTIME); magnitude = ZP - 2.5 log10(ADU/s) with ZP = 24.57 (per the paper's wording of "zero-point of 24.57 s^-1"; verify against the header ZP/MAGZERO keyword and whether SCI is per second or total ADU). Surface brightness in mag/arcsec^2 additionally needs the pixel area (0.01 arcsec^2). Fluxes in microJy are provided only in the catalogue _CAL columns.
- Calibrated frames carry sub-percent relative photometry but the shutter/BFE/ZP aperture-correction chain gives total-magnitude systematics at the 0.01 mag level, irrelevant for outskirts at SB 28+ but relevant for global magnitudes.
- Small-scale flat plus a 3x3-per-quadrant large-scale flat only constrain illumination on scales above about 1 arcmin at the 0.1% level; quadrant-to-quadrant offsets in sky level are part of what NoiseChisel absorbs. For LSB work, re-estimate the sky level quadrant by quadrant on source-masked frames and match levels across overlaps.
- Ghosts (IE < 14 stars, 3000-4000 ADU above sky for IE = 5.5) are offset by a few hundred pixels; mask them yourself beyond the flagged area when working around bright stars near nearby galaxies.
- Stray light and zodiacal background vary with solar aspect angle; the dark-frame comparison monitors this only qualitatively (p. 5).
- PSF: if modelling VIS frames directly, use the delivered PSFEx model with caution (undersampled, no wings); for stack-level fits use the MER-propagated PSF.

## Practical recommendations for users
- Do apply the FLG INVALID bit (bit 0) and use the WGT map; do consider bits 5 (GHOST), 4 (COSMIC), 9 (CR_REGION), 17 (SATXTALKGHOST), 18 (STARSIGNAL) and 24 (OBJECTS) depending on purpose.
- Do add the BKG map to SCI if you want to recover "unsubtracted" light, then estimate your own sky on source-masked data; do not assume the NoiseChisel map is safe for objects over 3'.
- Do use per-exposure ZP and APERCOR from headers; do not assume a single ZP of 24.57 applies to all exposures (Q1 uses the July-September 2024 median).
- Do check SCORE, spread_peak and CR_REGION in the xml/json before using an exposure; do not mix in the 16 rejected exposures.
- Do not trust sub-percent photometry between short and nominal exposures without accounting for the shutter effect.
- Do not expect stacks or CTI-corrected data in Q1; for DR1 see mccracken.md.

## Objects, fields and figures worth revisiting
- Self-calibration field in EDF-North at 17h55m15s, +65d17'08" (PSF and flat calibration; p. 8); WD J175318.65+644502.15 (Gaia DR3 1440758225532172032), the primary photometric standard (p. 11).
- Q1 fields: EDF-N, EDF-S, EDF-F, Lynds Dark Nebula LDN1641 (coordinates not given here).
- Figures: Fig. 1 (quadrant layout, p. 3); Fig. 4 (flagmap, p. 6); Fig. 8-10 (PSF, p. 9-10); Fig. 11 (large-scale flats, p. 11); Fig. 13 (ghost, p. 11); Fig. 15 (single frame vs stack, p. 14); Fig. 17 (QC distributions, p. 14); Fig. 20-21 (photometric scatter and counts, p. 15-16). No figure shows background subtraction around a large galaxy.

## Cross-references
- mccracken.md (DR1 VIS paper: changes, NoiseChisel remains, stack no longer carries BKG), q1_romelli_mer.md (second background subtraction, resampling, flags), q1_polenta_nir.md (large-scale flat code shared with NIR), schirmer-calibration.md and schirmer-spacecraft.md (ice contamination, shutter, calibration strategy), ruffenach.md, tereno.md.
- Q1 VIS DPDD and Explanatory Supplement for HDU layout, MAGZERO keyword and the full flag list.
