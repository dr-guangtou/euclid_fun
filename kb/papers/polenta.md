---
title: "Euclid Data Release 1 (DR1): Near-infrared processing and data products"
short_name: polenta
first_author: Polenta
series: A&A Special Issue DR1-Foundation (Nov 2026)
local_pdf: ~/Desktop/euclid/papers/polenta.pdf
local_text: ~/Desktop/euclid/text/papers/polenta.txt
topics: [NISP, NIR PF, YE JE HE, persistence, bad pixel mask, PRNU flat, NoiseChisel background, 1/f noise, PSF, stacking, SWarp, zero point, white dwarf, ice contamination, arcs]
relevance_extended_galaxies: high
---

# NIR processing and data products (Polenta et al. 2026)

## TL;DR
Describes the DR1 revision of the NIR processing function for NISP photometry (YE, JE, HE): 71 659 calibrated NIR images over >1900 deg2 (p. 1). New relative to Q1: first NIR stacks (DpdNirStackedFrame, in uJy), NoiseChisel background (replacing SExtractor), in-flight persistence model with 5 h look-back and conservative masking, PSF models derived from the self-calibration field, multi-aperture photometry. For LSB/extended-source users the paper is essential on sky subtraction (10x10 px tiles, 30th-quantile, not subtracted from single frames), residual 1/f striping, residual large-scale structure from persistence/flat, and heavy persistence masking in some detectors.

## Key facts and numbers
- NISP photometric channel: 950-2021 nm, filters YE, JE, HE; 16 H2RG detectors of 2048 x 2048 px, pixel scale 0.3 arcsec, FoV 0.57 deg2 (p. 1). Saturation near AB~16 for bright sources (from companion paper).
- DR1 NIR observations: 1 Oct 2023 to 21 May 2025; >1900 deg2; EWS+EDS+COSMOS+calibration fields; 71 659 calibrated images (p. 1).
- Bad pixels: 239 878 INVALID pixels (~0.4% of the focal plane); 5177-31 700 per detector, mean 14 992 (p. 2).
- Non-linearity: 4th-degree polynomial per pixel, recalibrated with PV-018 (Nov 2023) and F-008 (Feb-Oct 2024): 2136 exposures in MACC(4,16,4), six flux levels 8-750 e-/s (p. 2).
- Persistence: look-back 5 h; photometric masking threshold 2 e-; spectroscopic 30 e-; Hough-transform line step adds ~2% more flagged pixels (p. 3). Some detectors exceed 10% masked pixels in high solar activity (skypatch 38, 43 observations in EDF-North) (Fig. 2, p. 3).
- PRNU small-scale amplitude sigma68 = 1.269% (first) to 1.272% (last epoch); sub-percent temporal scatter (0.326% reference-relative; 0.359% adjacent-epoch; structure function 0.254% to 0.265%) (p. 4).
- Background: NoiseChisel v0.16, quantile threshold 0.3, 10 x 10 px tessellation, Manhattan nearest-neighbour interpolation, 3 px flat smoothing kernel (p. 5).
- PSF-photometry vs aperture: MAG_PSF - MAG_APER slope Q1 -> DR1: YE 0.0192 -> 0.0040, JE 0.0045 -> 0.0017, HE 0.0024 -> -0.0019; RMS 0.074 -> 0.017, 0.026 -> 0.011, 0.018 -> 0.010 mag (Table 1, p. 5).
- Multi-aperture photometry: radii 0.6, 0.9, 1.5, 2.25, 3.0 arcsec (diameters 4, 6, 10, 15, 20 px) (p. 6).
- Astrometry: offsets vs Gaia within 2 mas, mean RMS 10 mas, <20 mas for 99% of dithers in all bands (requirement 30 mas); local degradation >50 mas in DET13/DET14 where persistence masking removes Gaia matches; affects ~3% (RMS>30 mas) and 0.3% (RMS>60 mas) of DR1 area (p. 8).
- Throughput: variations of a few percent from ice; time stability ~2 mmag RMS except Nov 2023-Mar 2024 (p. 8); relative flux calibration 0.9% for bright sources (brighter than 19 mag) in YE/JE/HE vs 1.5% requirement (Fig. 8, p. 8-9); focal-plane spatial residuals <=0.01 mag overall (p. 9).
- Ice growth ~10 nm per month; calibration LED stability 0.1% (p. 2).
- Arcs from bright stars present in ~3% of images (p. 11).
- Absolute calibration: WDJ175318.65+644502.15 (HAB=18.36); three other WDs for validation (Table 3, p. 10).

## Data products and data model
All DPs are XML (Euclid Common Data Model) with DataStorage (MEF file) and QualityParams (App. C, p. 19).
- DpdNirCalibratedFrame: calibrated single-dither exposure, MEF with three layers per detector - SCI (image), RMS, DQ (data quality flags) (p. 7). Storages: DataStorage; BackgroundStorage (separate MEF with the NoiseChisel background, NOT subtracted from the image); PsfStorage (two FITS: PSF model and PSF image derived from self-cal field); PsfSingleStorage (new in DR1: PSF model and image derived from the calibrated image itself) (p. 19).
- DpdNirCalibratedFrameCatalog: MEF with 17 HDUs (primary + 16 detector catalogue tables); multi-aperture, PSF-fit and MAG_AUTO photometry; no aperture correction applied; magnitudes AB but fluxes in e- (p. 19).
- DpdNirStackedFrame (new in DR1): MEF with a single SCI HDU over the whole stack, plus RMS and DQ extensions; combines 4 dithers (EWS) or 76 (self-cal); metadata Filter, WCS, ZeroPoint (effective), DateRange; no BackgroundStorage because the background is subtracted before stacking; calibration applied so the image is in uJy (p. 19).
- DpdNirStackedFrameCatalog (new): MEF with primary + one catalogue HDU; no aperture correction; magnitudes AB, fluxes uJy (p. 19).
- Stack RMS layer = sqrt(co-added variance); variance = 1/weight; zero-weight pixels get variance 1e16; DQ in stack: derived from weights only (1 where weight=0, 0 elsewhere) because flag propagation is switched off (p. 8).
- Single-exposure DQ flags: bit 0 INVALID (unusable pixel); informational flavours DISCONN, ZEROQE, SUPERQE, BADBASE, SAT, FLOWER, LOWQE, HOT (static BPM, Table A.1, p. 17); transient flags PERSIST, PERMODFAIL. FLOWER/INVALID applied to flower centre and 4 neighbours (p. 2). Header gets persistence thresholds and per-detector counts of masked/corrected/failed/invalid pixels (p. 3). Flags combined with OR / bitwise sum in resampling (p. 7).
- VMPZ-ID InfoMaps (Odier et al. 2026): maps flagging regions where astrometry is degraded (p. 8, 11).
- Keywords in headers: see Radovich paper (ASTRRMS1/2, ASTIRMS1/2, ASTROFF1/2, ASTRELL, ASTRNM).

## Processing and methods
1. Common NIR-SIR pre-processing (p. 2-4): master bad pixel mask (disconnected pixels from PV-010 flats LedId=B, Intensity=60, PwmDutyCycle=28.7; hot pixels from 500 PV photo darks PV-012; permanently saturated pixels from dark ramps; flower pixels via Laplace filter on 30 LED flats, central pixel in >=2 exposures); non-linearity correction; persistence masking.
2. Persistence: power-law decay I_P(S,t) = alpha S (t - t0)^(-beta), time-integrated over N preceding exposures within 5 h; saturated pixels masked for the entire look-back; additive, signal-driven, sky ignored; amplitude/decay index independence of previous illumination neglected; for photometric targets only spectroscopic exposures are included in the history, for spectroscopic targets both. Pixels above threshold flagged PERSIST+INVALID; PERMODFAIL if estimate unreliable; Hough line detection (scikit-image probabilistic_hough_line; components >10 000 px removed; minimum line length 200 px) for residual streaks (p. 2-3).
3. PRNU/flat: filter-dependent master flats from LED B, C, D exposures (30 each) for YE, JE, HE, via QE map and filter transmission; one set used throughout DR1 (p. 4). Large-scale flat is derived from source fluxes (self-cal field) and monthly per-detector offsets (p. 11).
4. Background: NoiseChisel as above, estimated per detector, supplied separately (p. 4-5).
5. PSF: PSFEx models derived in advance from the 76-dither self-cal field, stored in EAS and retrieved at run time (p. 5); companion paper da Silva et al. 2026.
6. Astrometry: SCAMP, PSF centres vs Gaia DR3 (proper-motion corrected), 3rd-order polynomial per detector, presolution from self-cal field converted PV-SIP-PV analytically to account for rotation; new pre-check to reject exposures with FGS failures or particle showers (p. 6).
7. Catalogue extraction: SExtractor with initial detection threshold lowered 5 -> 2; FLUX_RADIUS>0.65 and FWHM_IMAGE>0 requirement; SExtractor FLAGS must be 0 for calibration sources (p. 6).
8. Resampling (new): SWarp C++ variant (propagates DQ); config FSCALE_KEYWORD set at runtime, FSCALASTRO_TYPE VARIABLE, OVERSAMPLING 5, RESAMPLING_TYPE LANCZOS2, WEIGHT_TYPE MAP_VARIANCE, COMBINE_TYPE WEIGHTED; background-subtracted images; fluxes rescaled for local pixel scale; flux scale factor with exposure time and inverse sensitivity applied to convert to AB (uJy) (p. 7). Lanczos-2 yields mean signed magnitude difference <0.005 mag and 0.015 arcsec RMS in position (Lanczos-3: 0.003 mag, 0.010 arcsec but more flagged pixels; bilinear 0.010 mag, 0.020 arcsec).
9. Stacking (new): SWarp WEIGHTED combination with map weights; median also tested; stack pixel scale not stated in this paper.
10. Photometric calibration: step-wise inverse-sensitivity (IS) values tracking throughput from self-cal visits, referenced to the June 2024 visit after the second decontamination; absolute from WDJ175318.65+644502.15 (CALSPEC, HST WFC3/IR + STIS) (p. 8-10).

## Validation and performance
- Astrometry: see Key facts; within the 30 mas (0.1 px) goal.
- Photometric time stability ~2 mmag RMS; repeatability 0.9% for sources brighter than 19 mag; spatial residual maps (Fig. 9) at <=0.01 mag overall; bright-source-only maps (17<YE<19, Fig. 10) show structures resembling persistence patterns (p. 9-10).
- Four WDs: median IS values of the other three lie within 2 sigma (SMAD) of the primary calibrator over Jun 2024-Jun 2025 (Fig. 12). The primary calibrator appears more variable than initially thought in VIS (p. 10).
- Flat-field monitoring: 24 HE master flats (Mar 2024-Apr 2026); late-to-early residual sigma68=0.264%, P95 0.534%, P99 0.734%; 27 of 64 detector edges show positive edge excess median 0.087%; 639 compact positive regions (median 5.4 px, contrast 0.22%); negative feature on DET42 (74 x 291 px, -0.499%), vertical band on DET43, broad negative ellipse on DET13; detector-wide scale drifts -0.100% (DET33) to +0.039% (DET22) (App. B, p. 17-20).
- Resampling tests (Lanczos kernels) in Sect. 3.3.1.

## Known issues, caveats, limitations
- Persistence masking is conservative: some detectors lose >10% of pixels in high-solar-activity periods; masked regions can accumulate and invalidate images; proton showers keep masks active (p. 3, 11). Persistence is masked, not corrected, because the model cannot yet predict the excess flux (p. 4, 11).
- DET13 and DET14: persistence masking removes Gaia matches (from ~30 to a few per detector), causing >50 mas (up to 150 mas) astrometric errors in ~3% of the area; fix not in DR1, planned for DR2; use VMPZ-ID InfoMaps (p. 8).
- 1/f readout noise leaves horizontal stripes visible after background subtraction; to be handled in the DR2 background scheme (p. 5, 11).
- Master background from many stacked frames shows spatial patterns similar to persistence images and to the bright-source photometric residuals; the source-derived large-scale flat does not fully remove them; if dithering is insufficient these residuals give an excess of diffuse faint signal (p. 11).
- Background is estimated independently per detector; uniformity on focal-plane scales is not guaranteed (p. 11).
- Flat-field: one static set of master flats in DR1; boundary haloes, compact positive regions and a few extended features exist at ~0.1-0.5% level; origin unassigned (App. B).
- Spikes from bright stars and snowballs are partially masked in pre-processing; no dedicated masking step. Arcs from bright stars (about 3% of images) not masked; positions depend on the bright star location (p. 11).
- Stacks: flag propagation disabled (DQ in the stack only reflects zero weight), so persistence/bad-pixel flags are lost in the stack DQ; the corresponding pixels are only down-weighted/zero-weighted through the weights (p. 8).
- No aperture correction applied in the NIR catalogues (fluxes in e- for single frames, uJy for stacks) (p. 19).
- Inter-detector variations of ice not corrected; ZP step-wise rather than smooth; no calibration products in Nov 2023-Mar 2024 so larger ZP residuals there (p. 8, 11).
- Absolute calibration tied to a single epoch of a single WD (p. 11).
- PSF models for stacks not tuned; PSFEx parameter tuning planned (p. 6).
- Paper itself states that remaining effects may matter for LSB and galaxy-cluster studies (p. 10).

## Implications for extended-galaxy photometry, 2-D modelling and low-surface-brightness work
- NIR sky: NoiseChisel with 10 px (3 arcsec) tiles and a 3 px smoothing is tuned to preserve extended-source light (Fig. 4, NGC 1483 comparison), but it is a local, source-masked estimate; large galaxies that fill much of a detector (2048 px = 10.2 arcmin) can still be partly absorbed. Re-estimating sky with larger-scale models on the calibrated frames (using BackgroundStorage as a baseline) is advisable for outskirts and ICL.
- The stack is already background-subtracted (units uJy), so any sky bias propagates; for LSB work prefer starting from calibrated frames + background maps + weights/DQ.
- Residual 1/f horizontal striping, persistence-like large-scale structure in the master background, and unflagged arcs all produce low-level faint structure at detector or focal-plane scales; avoid interpreting diffuse structure aligned with detector rows/boundaries; the dither pattern (4 dithers in EWS) may not average these out.
- The sub-percent PRNU stability, 0.9% photometric repeatability, and ~10 mas astrometry are ample for Sersic/bulge-disc fits; zero-point per-detector structure at 0.01 mag is not a concern for integrated photometry.
- Bright galaxy cores saturating at AB~16 will be flagged as saturated; persistence from them will be masked for 5 h in later exposures, producing masked areas in spectroscopic/photometric follow-ups. Heavy masking can also remove parts of extended galaxies in affected detectors.
- Stacked-frame DQ does not carry persistence flags; check the individual-dither DQ layers when interpreting stack features.
- NIR pixel scale (0.3 arcsec) undersamples the PSF; combine with VIS (0.1 arcsec) for morphology and use the PSF images from the self-cal field (PsfStorage) or the per-image PSF (PsfSingleStorage) with caution (see da Silva et al.).
- No explicit surface-brightness limit is given in this paper.

## Practical recommendations for users
- Use the DQ layer and apply INVALID (bit 0); additionally respect PERSIST/PERMODFAIL; know that FLOWER/INVALID pixels come in cross patterns.
- Fetch BackgroundStorage with single-frame products; remember to subtract it (calibrated frame SCI is not background-subtracted).
- For catalogue photometry, apply aperture corrections yourself (none applied); prefer multi-aperture flux growth curves for extended sources.
- Check VMPZ-ID InfoMaps to locate regions with degraded astrometry (DET13/DET14 persistence issue) before doing cross-band/VIS registration at the 30-60 mas level.
- Do not use stack DQ to find bad pixels; inspect weights and single-dither DQ.
- Be cautious with MAG_PSF in DR1 NIR; PSF-aperture agreement improved but still has residual slopes up to 0.004 mag/mag.
- Watch for horizontal striping and arcs near bright stars (3% of images).

## Objects, fields and figures worth revisiting
- NGC 1483 (barred spiral) in a 750 x 500 px JE cutout, used to demonstrate SExtractor vs NoiseChisel sky subtraction (Fig. 4, p. 6). Coordinates not given in the paper (NGC 1483 lies in the south, near Dorado; check catalogue).
- White dwarf calibrators (Table 3, p. 10): WDJ175318+644502 at 17:53:18.65 +64:45:02.15 (HAB 18.36; self-cal field); WDJ174911+643533 at 17:49:11.78 +64:35:33.54 (18.26); WDJ181144+654916 at 18:11:44.96 +65:49:16.42 (19.14); WDJ041345-473726 at 04:13:45.06 -47:37:26.29 (18.27; EDF-South). Two are in EDF-North, one in EDF-South (p. 9).
- Fields: EDF-North skypatch 38 (43 observations, high persistence), self-cal field (76 dithers), COSMOS, EWS.
- Key figures: Fig. 1-2 (persistence masking Q1 vs DR1, masked fractions, p. 3); Fig. 4 (background comparison, p. 6); Fig. 7 (ZP evolution, p. 9); Fig. 9-10 (FPA photometric residual maps, p. 10); Fig. B.1 (flat-field residual map, p. 18); Table A.1 (bad-pixel statistics per detector, p. 17).

## Cross-references
- Q1 NIR paper (NIRQ1, Polenta et al. 2026, A&A 711, A3).
- Radovich et al. 2026 (NIR astrometric calibration); da Silva et al. 2026 (PSF); Kubik et al. 2026 (persistence); Awad et al. in prep. (persistence correction).
- Schirmer et al. 2026a (calibration strategy, PV/F programmes) and 2026b (decontamination/ice); Jahnke et al. 2025 (NISP instrument; arcs, fig. 21); Hormuth et al. 2025 (calibration unit); Odier et al. 2026 (VMPZ-ID InfoMaps); Le Brun et al. 2026 (spectroscopic persistence threshold); McCracken et al. 2026 (VIS DR1); Tereno et al. 2026, Scaramella et al. 2022 (survey design).
