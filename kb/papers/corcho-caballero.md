---
title: "Euclid Data Release 1 (DR1): Colouring Euclid with external ground-based imaging data"
short_name: corcho-caballero
first_author: Corcho-Caballero
series: A&A Special Issue DR1-Foundation (Nov 2026)
local_pdf: ~/Desktop/euclid/papers/corcho-caballero.pdf
local_text: ~/Desktop/euclid/text/papers/corcho-caballero.txt
topics: [OU-EXT, ground-based imaging, DES, UNIONS, CFHT MegaCam, Subaru HSC, Pan-STARRS, DECam, co-addition, SWarp, PSF models, photometric calibration, Gaia XP, depth, colour homogeneity, StackedFrame]
relevance_extended_galaxies: medium   # context for how griz/u ground data were built; no PSF-homogenisation or resampling to Euclid pixel scale; some background-subtraction detail
---

# Colouring Euclid with external ground-based imaging data (Corcho-Caballero et al. 2026)

## TL;DR
OU-EXT turns heterogeneous ground-based optical imaging into co-added, Euclid-tiled "StackedFrames" with PSF models, which feed the MER pipeline for photometric redshifts and SED-weighted VIS PSFs. DR1 covers about 2500 deg2: DES/DECam griz in the south, UNIONS (CFHT/MegaCam u,r; Subaru/HSC g,z; Pan-STARRS i) in the north, and HSC/DECam in the deep fields. The paper concentrates on point-source depth, zero-point stability and colour homogeneity, validated with stars. It says nothing about PSF homogenisation across bands. Each band keeps its native pixel scale and PSF, and only the PSF models are stacked. Galaxy-extended-source quality (sky subtraction of faint outskirts, shredding) is not tested.

## Key facts and numbers
- Coverage: about 2500 deg2. 10,322 MER tiles in the EWS; EDFs and EAFs are about 130 deg2 and 1651 MER deep tiles (p. 3). EWS-North is about 30% of the DR1 EWS tile footprint and EWS-South about 70% (p. 3).
- 50,292 StackedFrames in total: 42,354 wide and 7938 deep (Table 1, p. 3). Per band (wide / deep): DECam-g 7512/1043, r 7511/1046, i 7511/1046, z 7511/1047; HSC-g 2729/867, HSC-r 64/195, HSC-r2 130/743, HSC-i 0/234, HSC-i2 147/708, HSC-z 2527/780; MegaCam-u 1391/82, MegaCam-r 2603/65; Pan-STARRS-i 2718/82.
- EWS-North (UNIONS, Gwyn et al. 2025): MegaCam u and r (CFHT, MegaPipe), HSC g (WHIGS, LSST pipeline v23), HSC z (WISHES, HSC pipeline as in Aihara et al. 2022), Pan-STARRS GPC1 i (p. 3). The data arrive already reduced and calibrated by their teams.
- EWS-South: DECam griz, mostly DES (Abbott et al. 2021) plus archival DECam. This is the only part reduced from raw data by OU-EXT Stage 1, using a modified CosmoDM pipeline (p. 3-4).
- EDF-N: H2O survey (HSC g, r, r2, i, i2, z) with archival HEROES and AKARI-NEP data, reduced with hscPipe v8.4. jointcal was used for both astrometry and photometry instead of FGCM, a change from HSC-SSP PDR3 (p. 3-4). EDF-F: HSC (H2O) plus DECam griz from archive and the DES supernova fields. EDF-S: DES griz at EWS depth. COSMOS: HSC SSP (g, r, r2, i, i2, z) plus archival DECam griz (p. 4).
- EWS 10-sigma point-source depth (2" diameter apertures, background-only noise, no correlated-noise correction) is 24.8/24.3/24.0/23.0 AB for griz (abstract). Requirements: DECam griz 24.7/24.4/23.8/23.1; MegaCam r 23.9; HSC g 24.5, z 23.4; PS i 23.6 (p. 6). North tiles meeting the requirement: 78% (g), 96% (r), 98% (i), 20% (z) (p. 7). Tile-to-tile depth scatter is 0.1-0.3 mag (p. 7). Deep fields are 1-2 mag deeper than the EWS (EDF-S is EWS depth), with ranges over 1 mag within a field (p. 7).
- Photometric stability: more than 95% of EWS-South stacks meet the 10 mmag relative requirement. In EWS-North the fractions are 55/68/85/78% for griz, with tails of 20-30 mmag in MegaCam-r, HSC-g and HSC-z (p. 9). Tile-to-tile spatial variation stays under 10 mmag, under 5 mmag for DECam (p. 9).
- Colour homogeneity (stellar locus): south deviations under 5-10 mmag. North residuals 10-25 mmag. Method noise floor 5.0/2.8/2.5 mmag (g-r, r-i, i-z) in the south and 6.3/3.2/2.5 in the north (p. 11-12).
- Stack zero-point: Euclid StackedFrame zero point is 30 mag, i.e. 3.631 nJy/ADU (p. 5). The Stage 2 zero-point adjustment is below 1% in the EWS and 2-3% in the EDFs and EAFs (p. 5). Table 2 (p. 6) lists per-band corrections: for example DECam g -0.2, r -2.1, i -3.4, z -2.2 mmag; HSC-r +31.1, HSC-r2 +25.5, HSC-i -35.3, HSC-i2 +17.0, HSC-z +5.8 mmag; MegaCam-r +2.3; PS-i -2.0; MegaCam-u 0.
- Validation flag policy for DR1: stacks with |offset| > 50 mmag or more than 3 NMAD from the global band median are flagged. Fraction rejected is about 1-1.5% in the EWS; deep fields up to about 20% (p. 12).

## Data products and data model
- DpdExtSingleEpochFrame (SEF): per-CCD calibrated exposure with science image, inverse-variance or RMS map, per-pixel flag map, WCS, PSF information and source catalogue. Stage 1 output (p. 4).
- DpdExtStackedFrame: the released co-added product, in the Euclid (MER) tiling. Extensions are flux, weights, RMS and flag bitmask (4 extensions). A SEF coverage map stores the number of contributing SEFs per pixel (p. 5). It also carries co-added PSF models (p. 4).
- Related: DpdExtCoaddCatalogue, DpdExtValidationReport (PF1 outputs, Fig. 2, p. 5); DpdExtAnalysisResults (PF2 QC parameters and SourceExtractor++ catalogue), stored in DPS/DSS (p. 6); DpdExtConfigurationSet, DpdMerTile (inputs).
- Reference catalogues (names used in the paper): GRC (Gaia XP synthetic photometry, m < about 17.7), SCC (SEF composite catalogue), ERC (DES DR2 and PS1/UNIONS forced PSF photometry mapped into the GRC frame by a random-forest colour transformation) (p. 7-8, App. B).
- Flag tables (App. A, Table A.1, p. 20): bit values per survey. DES (DECam) bits 1-128: hot/dead pixel, saturated, interpolated, poor read, cosmic ray, bright star, bleed trail, bright star interpolated. In the DES table all are marked F (not rejected in co-addition). CFIS/MegaCam bits 1-128 are all rejected. Pan-STARRS has bits to 32768 (including diffraction spike 512, optical ghost 1024, streak 2048, bright star core 4096; these are not rejected). HSC (WHIGS/WISHES, H2O, SSP) include "bright-star halo region" (bit 512 in WHIGS/WISHES and SSP, rejected), "detected as source footprint" (32, not rejected) and "detected as source footprint with negative flux" (64, rejected). All SEF flags are propagated by OR to the StackedFrame flag extension (p. 5, 20). Pixel dimensions and PSF FWHM are not tabulated in this paper.
- Where the data live: Euclid Archive System (DPS/DSS); MER consumes StackedFrames. The MER catalogue is documented in Romelli et al. 2026 and Kummel et al. 2026. Public file names are not given here.

## Processing and methods
1. Stage 1 (survey-specific). DECam: detrending, Gaia astrometry, masking and interpolation of defects, background model, PSF model, catalogue extraction. North: format conversion only (p. 4).
2. Stage 1 zero-point recalibration: weighted linear least squares of CCD zero points over "SuperTiles" spanning tens of degrees, with absolute constraints from Gaia XP synthetic photometry and relative constraints from repeated star measurements (p. 4).
3. Stage 2, PF1 step 1: apply a per-filter delta zero point (from stacks of EDF-N/S/F, EDMS, COSMOS against GRC (mag 16-17.6) and SCC (mag 18-21)). Background subtraction with SWarp, only for MegaCam and DECam, with BACK_SIZE 128 (MegaCam) and 256 (DECam) pixels and BACK_FILTERSIZE 3. HSC and Pan-STARRS keep their native sky subtraction (p. 5, footnote 5).
4. PF1 step 2: scale each SEF to zero point 30. SWarp resamples onto the MER tile grid with a Lanczos-3 kernel, preserving the instrument-specific pixel scale, and combines with a weighted mean (COMBINE_TYPE=WEIGHTED), weights from the background-only RMS or WEIGHT map. Flags are propagated. No extra pixel rejection (no clipping) is done in co-addition, unlike the UNIONS stacking (p. 5, 13). A SExtractor detection catalogue is made (DECam detects on i,z; MegaCam on u/r; HSC on g/z) (p. 6).
5. PF1 step 3: PSFEx PSF models on the stack. Per-SEF PSF models are co-added at the sources either source by source (DECam) or in non-overlapping layers (HSC, MegaCam), which gives identical results (p. 6). Details are in Vassallo et al. (in prep.).
6. PF2: SourceExtractor++ on each stack gives PSF photometry, circular apertures (diameters 1" to 10") and Kron photometry. Checks: Gaia astrometry and photometry, PSF FWHM from Gaussian fits to the models vs stars, brightness profile of stars vs PSF, pixel RMS and depth (p. 6). EQUAL performs survey-level analysis.

## Validation and performance
- Metrics per stack: median offset and NMAD of PSF minus GRC, SCC, ERC or AUTO (Kron) magnitude (stars). Internal NMAD (PSF vs Kron) is typically within 1%. Pan-STARRS-i exceeds 10 mmag, attributed to its extended PSF tails (p. 9).
- HSC-g NMAD vs GRC about 11.4 mmag. HSC bands are sensitive to saturation of the bright GRC stars (p. 9).
- Colour test: XDGMM with 26 components on the dereddened (g-r, r-i, i-z) stellar locus. Local colour offsets were fitted in RA/Dec bins of about 200 stars each (p. 11).
- Deep fields: EDF-N, EDF-F (HSC) and COSMOS (HSC) show large offsets against the SCC. HSC-i and HSC-z in EDF-F and the HSC bands in COSMOS reveal a zero-point inconsistency between SEF and StackedFrame levels. EDF-S outliers trace to astrometric errors in input SEFs (p. 10-11).
- Valid fractions (Table 3, p. 13): EWS north 97.7-99.7% and south 98.4-98.7% per band. EDF-N HSC-r 0/127 and HSC-i 0/77 valid; EDF-F HSC-i 3/94; COSMOS HSC-i 2/85. i2 and r2 perform far better in the same fields. EDF-S: 77-93%.

## Known issues, caveats, limitations
- Photometric solution of the deep-field HSC data is the least reliable: use HSC-r2 and HSC-i2 rather than HSC-r and HSC-i in EDF-N, EDF-F and COSMOS (Table 3). The fails are linked to the SEF/StackedFrame zero-point definition (p. 12-13).
- A patch of EWS-North Pan-STARRS stacks with wrong calibration was removed from the public release. Many PS stacks have image artefacts not in the input masks, which require an extra mask (Odier et al. 2026), because PF1 does no extra pixel rejection (p. 13).
- A batch of DECam stacks near RA about 5 deg was removed (wrong SEF selection from a software bug); the RA about 5 deg meridian is flagged invalid in the release (p. 13, 26).
- Noise propagation: in DR1 only the background RMS is propagated. Source Poisson noise is missing, which can bias model-fitting photometry and underestimate flux errors. This is planned for DR2 (p. 14).
- PSF models are not sampled at every detection. The nearest model is used, which can affect PSF photometry in crowded fields or rapidly varying seeing (p. 14).
- Passband effective-wavelength variations across the field and in time are not corrected in DR1 (target of 10 A precision in DR2), causing colour-dependent biases (p. 14).
- Northern depth is heterogeneous, and MegaCam-u is still incomplete. The northern z band is the shallowest (only 20% of tiles reach the requirement) (p. 7, 24).
- The Stage 2 products are not PSF-homogenised. Seeing varies from band to band and tile to tile (not mentioned in the text as a correction).
- Documents the DES, UNIONS and HSC native sky subtraction only briefly. Large-galaxy outskirt flux can be over-subtracted by local sky estimation (a general risk; the paper does not test it). Only MegaCam and DECam get a SWarp background subtraction with a 128 or 256 pixel mesh, a scale smaller than big galaxies; HSC and PS keep the sky subtraction of their original pipelines.
- Colour offsets in the south correlate with Galactic extinction, reflecting an imperfect extinction correction (p. 12). Notes that the Euclid mission aims at 10 mmag but DR1 flags only the above 50 mmag.

## Implications for extended-galaxy photometry, 2-D modelling and low-surface-brightness work
- For multiband (griz + Euclid) Sersic or bulge-disc modelling you must handle band-to-band PSF differences yourself. The EXT PSF models (PSFEx-based stacked models) are provided as co-added PSF stamps at selected locations; they are the only PSF description for ground bands.
- Ground-based stacks are sky-subtracted per SEF (DECam, MegaCam with SWarp mesh 256 and 128 pixels; HSC/PS natively). For nearby, large galaxies (several arcmin) the local sky model may eat the outskirts, so ground-based outer profiles and ICL colours are unreliable at the faint end unless you redo the sky. This is not studied in the paper.
- Noise maps lack Poisson noise from sources. For bright galaxies, per-pixel chi2 fits on ground bands will underestimate errors.
- The depth is quoted for point sources (10 sigma, 2" aperture); surface-brightness depth for LSB is not given. The tile-to-tile depth scatter (0.1-0.3 mag) and the coverage map are useful when selecting areas.
- Colour zero-point reliability of 10 mmag (about 1%) is more than sufficient for integrated colours of bright galaxies. The north has 10-25 mmag residual structures.
- The deep fields (COSMOS, EDF-F, EDF-N) offer 1-2 mag deeper imaging, but avoid the HSC-i and HSC-r stacks there.

## Practical recommendations for users
- Do use DECam griz (EWS-South, EDF-S, EDF-F, COSMOS) where you need the most stable photometry. Do treat the north (UNIONS) stacks with greater caution (tails of 20-30 mmag).
- Do prefer HSC-r2 and HSC-i2 over HSC-r and HSC-i in deep fields (Table 3).
- Do apply the StackedFrame flag extension. Remember some flags are propagated but not rejected (bright star core, diffraction spikes, optical ghosts in PS), so inspect them.
- Do check the stack validity flag (set by the |offset| < 50 mmag and 3 NMAD cuts) before using a tile.
- Don't use photometric uncertainties from the RMS maps as complete errors (no source Poisson term).
- Don't assume matched PSF across bands.
- Do not rely on EDF-N, EDF-F (HSC) and COSMOS (HSC) absolute zero points to better than the large offsets quoted.

## Objects, fields and figures worth revisiting
- Fields: EDF-N (HSC H2O, near the north ecliptic pole), EDF-S (DES), EDF-F (Fornax; HSC and DECam), COSMOS (HSC SSP and DECam), EDMS (reference field in Table 2). The paper gives no centre coordinates for these.
- Region noted: RA about 5 deg stripe in EWS-South (invalid stacks); Pan-STARRS bad-calibration patch in the north (Fig. D.1).
- No individual galaxies.
- Figures and tables: Table 1 (p. 3, stack counts); Table 2 (p. 6, zero-point adjustments); Fig. 4-5 (depth distributions, p. 8); Fig. 6 (EWS photometric stability, p. 9); Table 3 (p. 13, validity per field and band); Table A.1 (p. 20, flag bits); Figs. C.1-C.5 (depth maps, p. 24-25); Figs. D.1-D.5 (offset maps, p. 26-27).

## Cross-references
- Kummel et al. 2026 and Romelli et al. 2026 (MER pipeline that ingests StackedFrames).
- Gwyn et al. 2025 (UNIONS); Odier et al. 2026 (extra mask for PS artefacts); Vassallo et al. (in prep.; PSF co-addition); Ruffenach et al. 2026 (SGS/archive); Aussel et al. 2026 (DR1 footprint); Hartley et al. 2026 (photo-z validation); McPartland et al. 2025 and Zalesky et al. 2025 (H2O).
