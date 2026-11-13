---
title: "Euclid Data Release 1 (DR1): The MERge processing"
short_name: kuemmel
first_author: Kuemmel
series: A&A Special Issue DR1-Foundation (Nov 2026)
local_pdf: ~/Desktop/euclid/papers/kuemmel.pdf
local_text: ~/Desktop/euclid/text/papers/kuemmel.txt
topics: [MER, mosaics, tiling, special objects, detection, deblending, SourceExtractor++, A-PHOT, T-PHOT, Sersic, FLUX_RADIUS, CAS, PSF normalisation, photometric validation, EDF, catalogues]
relevance_extended_galaxies: high
---

# The MERge (MER) processing for Euclid DR1 (Kuemmel et al. 2026)

## TL;DR
Describes the MER processing function that turns calibrated VIS (IE) and NISP-P (YE, JE, HE) frames plus ground-based (EXT) images into tile mosaics on a common 0.1"/pix grid, detects and deblends sources, measures four kinds of photometry (Kron total in the detection band, A-PHOT aperture on PSF-matched cutouts, T-PHOT template fitting, 2-D Sersic fits) and morphology (CAS, FLUX_RADIUS, Sersic, Zoobot), and publishes the catalogues. It is a DELTA paper with respect to the Q1 MER paper (Romelli et al. 2026): many algorithmic details (sky/background modelling, mosaicing, kernels) are NOT repeated here and must be taken from Romelli et al. (Q1) and the Explanatory Supplement. For galaxy-imaging users the key DR1-specific news are: new Deep tiling, a "special objects" scheme for galaxies > 2' (but no special tile was processed in DR1), PSFs no longer renormalised (big effect on photometry, especially for extended sources), Sersic n limit raised to 8, FLUX_RADIUS added, local noise in CAS, and the known wide-vs-deep over/under-deblending.

## Key facts and numbers
- DR1 = ~1900 deg2 of EWS plus EDS (three EDFs) (p. 1); MER output: coadds in IE, YE, JE, HE (+ EXT bands rebinned), and a unified multi-band catalogue (p. 1).
- Common mosaic pixel scale 0.1"/pix, close to VIS native (p. 3). EXT data rebinned to this grid.
- Wide tile: extended area 32' x 32'; same tiling as Q1 so TILEID covers the same area as in Q1 (p. 2). Wide tile indices start with "102".
- Deep tile (new): 17' x 17' tangential projection, centres spaced by 15' => 2' overlap between neighbours, core area defined at HEALPix Nside = 8192; indices start with "101" (pp. 2-3). Deep tiling is independent of Wide; EDFs have both Deep and Wide-like (single reference observing sequence) processing (p. 2, Fig. 2 for EDF-Fornax).
- Special-object tiles: index prefix "1025", typically larger than a wide tile, one per special object (p. 3). None processed in DR1 (p. 3).
- Special-object catalogue: 164,526 objects with size > 2' from HyperLEDA, HECATE, EDD, SIMBAD, RC3, Updated Nearby Galaxy Catalog, plus Milky Way globular clusters (Harris 1996); fake/absent/stars removed. Bounding box = square of side 4x the isophotal diameter (Holmberg a26 or D25), limited to 2'-120'; for globular clusters 3 r_t clipped to [30', 120'] (p. 3). Aim: undisturbed images incl. tidal features.
- Local disk requirement ~50 GB per Euclid band for a normal wide tile (motivates Deep tiling) (p. 2).
- 8388 wide tiles listed for EWS in Table 5 (coverage > 0.3); text says 8887 tiles released in DR1 in total, 7803 (88%) with coverage > 80% (pp. 13, 15).
- Nominal exposure (median tile): EWS IE 2274 s, YE 314 s, JE 313 s, HE 314 s; source density 116 per arcmin2 (Table 5, p. 15). EDF-N IE ~20.8 ks, EDF-S ~20.3 ks, EDF-F ~4.0 ks; COSMOS 51.9 ks IE; CDFS 45.8 ks; AEGIS 29.0 ks (Table 5).
- Reference observing sequence: 6 exposures IE, 4 in NIR (p. 4).
- Detection (SE++ Table 1, p. 4), identical for EWS and EDS: segmentation-filter Gaussian FWHM 2.4 pix (VIS) / 5.0 pix (NIR); detection-threshold S/N per pixel 0.9 (VIS) / 0.4 (NIR); detection-minimum-area 10 pix; core-threshold-value 1.3 / 0.55; core-minimum-area 10 pix. NIR detection is done on a stack of YE+JE+HE.
- Deblending: dedicated ASTErIsM-based component (Tramacere 2016, two topometric clustering algorithms), run independently in VIS and NIR, then merged (p. 4).
- Aperture photometry: A-PHOT apertures with diameters 1, 2, 3, 4 times the FWHM of the worst PSF (usually an EXT band); per-object value in column FWHM (p. 4).
- PSF stamps limited to <= 5" in MER (runtime/memory) (p. 9). Typical stamp sum S: IE ~0.957-0.961, YE/JE/HE ~0.984-0.987, DECam bands 0.97-0.99, Pan-STARRS i only ~0.880 (Table 4, p. 10).
- Sersic: SE++ v1.0.2, max Sersic index raised from 5.5 (Q1) to 8.0 (p. 5); fits in all bands.
- FLUX_RADIUS: disk of radius 6 a_M (a_M = SEMIMAJOR_AXIS), 64 annuli of equal width, radius containing 50% of the flux within the disk, SExtractor2-style (pp. 4-5).
- POINT_LIKE_FLAG: POINT_LIKE_PROB > 0.96 (99% star purity in SC8 simulation) for VIS-detected objects (p. 6). Spurious: authors suggest SPURIOUS_PROB > 0.7 rather than 0.5 for SPURIOUS_FLAG (p. 6).
- Zoobot subsample: all galaxies with IE < 21.0 or segmentation area > 700 pix (4x larger than Q1) (p. 6).
- Astrometry vs Gaia (proper-motion corrected): offsets < 10 mas in RA and Dec for tiles with FILLING_FACTOR > 0.5 (p. 7).
- PSF FWHM agreement with Gaia stars on mosaics: percent-level for VIS and NIR, sub-percent for EXT; tiles with > 5% discrepancy flagged but not invalidated (p. 7). Q1 NIR PSFs were 1.75-3.5% too large; much improved in DR1 thanks to the new NISP PSF method (da Silva et al.) (p. 4). VIS PSF FWHM ~0.203-0.210" (Fig. 20, p. 14/16).
- Depth: 5 sigma AB depth from median flux in random 2" diameter empty apertures (p. 7). EDF-N patch 64 plotted: IE ~24.5-25.5, YE/JE/HE ~23.6-24.2 (Fig. 9, p. 7).
- Photometry vs Gaia: IE offset about -0.02 +- 0.004 mag; NIR offsets -0.036 to -0.126 mag depending on method, scatter ~0.015; PSF fitting about -0.13 mag; the A-PHOT/T-PHOT difference in NIR and PSF-fitting offset are due to a T-PHOT bug found after DR1 processing (mainly bright point-like sources) (p. 8, Fig. 10).
- Relative photometry error (NMAD of A-PHOT vs Gaia colour curves, Table 3, p. 9): IE 15 mmag, YE 35, JE 40, HE 47, DECam-g/r/i/z 27/22/21/26, MegaCam-u 97, MegaCam-r 26, HSC-g 33, HSC-z 29, PS-i 20 mmag. Sample sizes 0.07 to 1.9 million Gaia stars.
- Source injection (Cornifer, Kong et al. in prep.): recovered photometry within 5% (p. 8).
- Bright-star masked fraction via DET_QUALITY_FLAG: 1-5% of EWS tile area (Galactic-latitude dependent); 2-10% (EDF-S) and 3-15% (EDF-N) upper limits for multi-roll data (p. 6).

## Data products and data model
- Mosaics (per tile, per band IE, YE, JE, HE and EXT bands): all on the 0.1"/pix tile grid. (The FITS layer structure, science/RMS/flag extensions, units and zero points are NOT listed in this paper; see Q1 paper Romelli et al. 2026 and the Explanatory Supplement.) Tiles have the 0.0-filled empty areas outside covered regions (p. 5, Sect. 2.6.1).
- NEW in DR1: "layer files" for every co-added IE, YE, JE, HE image. For each calibrated input exposure that contributes: exposure time; the three orientation angles (solar aspect angle, alpha, beta); observing date; coordinates of the image corners (p. 3). Allows reconstructing exposure-time maps and number-of-layers maps (Fig. 3, EDF-N tile 101837492) and transferring them to catalogue objects.
- Catalogue files (p. 6): EUC_MER_FINAL-CAT (main photometry catalogue), EUC_MER_FINAL-MORPH-CAT (morphology), EUC_MER_FINAL-CUTOUTS-CAT (cutouts catalogue), EUC_MER_FINAL-DEEP-CAT (photometry of the bands used in EDFs, calibration and extra fields; Table 5).
- Segmentation map: combined VIS+NIR deblended map; sources are labelled by SEGMENTATION_MAP_ID (Fig. 14 caption, p. 11).
- Catalogue columns / quantities named in the paper:
  - FILLING_FACTOR: fraction of HEALPix pixels in the tile containing at least one detection (coverage measure) (p. 5).
  - ASTROMETRY_RA_OFFSET, ASTROMETRY_DEC_OFFSET (arcsec; tile-level offsets, Fig. 5).
  - FLUX_DETECTION_TOTAL: Kron flux in detection band (IE or NIR stack); independent of PSF model and normalisation (p. 10).
  - FWHM: worst-PSF FWHM used for the A-PHOT apertures (p. 4).
  - SEMIMAJOR_AXIS, FLUX_RADIUS (new), MU_MAX, MAG_AUTO (used for S/G), POINT_LIKE_PROB, POINT_LIKE_FLAG, SPURIOUS_PROB, SPURIOUS_FLAG, VIS_DET (=1 for VIS-detected).
  - DET_QUALITY_FLAG: detection flags including saturated cores and diffraction spikes of bright Gaia stars on IE/YE/JE/HE; also used to select fit area (p. 5-6, 10).
  - SERSIC_VISNIR_FLAGS (VIS+NIR) and SERSIC_EXT_FLAGS (EXT): binary flags combining SE++ model-fitting flags and levmar stopping criteria (Table 2, p. 5).
  - CAS non-parametric morphology: concentration C, asymmetry A, smoothness S (columns not named in this paper).
  - Zoobot "visual-like" morphology (details in Walmsley et al. 2026).
  - Sersic parameters in all bands: integrated flux, Re, n, q (axis ratio), etc. (exact column names not given here).
- SERSIC flag bits (Table 2, p. 5): 0 error flag (levmar); 1 size correction (manual resizing of fitting box, set for big objects); 2 outside measurement frame (no fit run); 3 insufficient data (no fit run); 4 some/all model parameters could not be fitted; 5 fit on downsampled image because maximum size exceeded; 6 small gradient (J^T e); 7 small step (Delta p); 8 maximum iterations reached; 9 singular matrix J^T J + mu I (raises error flag); 10 no further error reduction possible; 11 small residual; 12 invalid (NaN/Inf) model values (raises error flag). Bits 6-12 are levmar stopping criteria.
- Photometry types in the catalogue: aperture (4 apertures), template fit, Sersic, PSF fit (VIS), and Kron in detection band; recipes (combining Kron with colours to get total fluxes in each band) are in the Photometry Cookbook in the Explanatory Supplement (p. 4, p. 14). Units/AB conversion: all magnitudes quoted are AB (Fig. 11 caption); the flux unit and zero point convention are not given in this paper.
- Extra metadata: tile indices, exposure times, detection numbers, python scripts to enhance catalogues, plus Photometry and Morphology cookbooks in the Explanatory Supplement (p. 14).
- Archive: http://po.pages.euclid-sgs.uk/ExplanatorySupplement/release-DR1-Foundation/ ; ESA DR1 DOI 10.57780/esa-d079c51 (pp. 14-16).

## Processing and methods
1. Tiling (Sect. 2.1): wide 32' x 32' tiles (as in Q1); new deep 17' x 17' tiles; special-object tiles defined but not run. Wide tiles near large objects were enlarged in Q1 (extended wide tiles) to avoid cutting them; remaining objects get dedicated special tiles.
2. Mosaic creation (Sect. 2.2): co-add calibrated VIS and NIR frames on 0.1"/pix tile grid; rebin EXT images to the same grid, method as in Romelli et al. 2026. THE PAPER DOES NOT DESCRIBE BACKGROUND/SKY SUBTRACTION, mesh or filter sizes, or its effect on large sources; it only states (p. 12) that inconsistencies from "problems in the background modeling" between wide and deep would show up in the wide-vs-deep photometry comparison (Fig. 15), and that none were seen (offsets <= ~0.01 mag, constant over a large dynamic range). For the actual background scheme go to Romelli et al. 2026 (Q1 MER) and OU-VIS/OU-NIR papers (McCracken et al., Polenta et al.) - to be cross-checked in those papers' summaries.
3. Detection (Sect. 2.3): independent SE++ detection on VIS and NIR (YE+JE+HE stack) coadds using Table 1 parameters; ASTErIsM-based deblending independently in VIS and NIR; merge into one object list and one segmentation map.
4. PSF mapping (Sect. 2.4): PSF models from OU-VIS, OU-NIR, OU-EXT are propagated to the mosaic grid including stacking effects. PSF stamps limited to 5". DR1 change: PSFs are NOT renormalised to unit sum (see below).
5. Photometry (Sect. 2.5): (i) A-PHOT aperture photometry (custom version) on cutouts PSF-matched on the fly to the worst PSF per object; segmentation pixels of other sources are excluded but faint extended wings of neighbours remain; Kron elliptical aperture flux in detection band; total flux in other bands obtained by scaling Kron by aperture colours. (ii) T-PHOT template fitting (custom), with detection-band stamps convolved to the measurement resolution as priors; direct total flux limited by segmentation area and PSF extent, so colour-based totals are an alternative. (iii) Sersic photometry (integrated flux). Methods are optimised for faint, extended sources, not for bright stars, so Gaia-star validation is sub-optimal (p. 4-5).
6. Non-parametric morphology (Sect. 2.6.1): CAS. DR1 fix: noise (median and NMAD) now measured locally in the cutout instead of globally over all segmentation = 0 pixels, because zero-filled empty areas in partially covered tiles biased A low in low FILLING_FACTOR tiles (Fig. 4, EDF-S). FLUX_RADIUS added (see above).
7. Parametric morphology (Sect. 2.6.2): 2-D Sersic fits in all bands with SE++ 1.0.2 in no-detection mode (given centres and fitting areas plus initial guesses); levmar fitting engine. Changes: n_max 5.5 -> 8.0; fitting-area cap (for runtime) now uses DET_QUALITY_FLAG so bright saturated stars get a limited fit area while bright galaxies are fitted with the full area; combined flag columns; non-normalised PSFs are used in Sersic fits.
8. Star/galaxy (Sect. 2.6.3): MU_MAX - MAG_AUTO plus a calibration from SC8 gives POINT_LIKE_PROB (VIS-detected only).
9. Zoobot morphology (Sect. 2.6.4): deep foundation model fine-tuned from Zoobot (Walmsley et al. 2026), applied to wide and deep.
10. Spurious identification (Sect. 2.7): model trained on pre-launch simulations; no DEEP-like training set so optimised for WIDE; threshold advice 0.7.
11. Bright-star masking (Sect. 2.8): imprint of bright Gaia stars (saturated centres and diffraction spikes) mapped onto IE, YE, JE, HE coadds; objects in these regions flagged in DET_QUALITY_FLAG. Masked area 1-5% of EWS tiles. For multi-roll deep data the spikes of different roll angles partly cancel, so the quoted 2-10% / 3-15% are upper limits. (Separate photometric masks: see odier.)

### PSF normalisation (Sect. 4, critical for photometry of extended sources)
- PSF model sum S = sum of pixels should be 1; MER stamps are cut to 5", so S_stamp < 1 (e.g. 0.9 means 10% of the flux lies outside the stamp).
- Q1 re-normalised stamps to S = 1, which caused photometric offsets up to ~10% in bands with large PSFs (Pan-STARRS i, FWHM > 5"). DR1 does not renormalise.
- First-order relations between old (n) and new (nn) fluxes: A-PHOT and T-PHOT in band B: F_nn(B) = F_n(B) / (S_nn(B)/S_nn(D)), D = detection band; Sersic: F_nn(B) = F_n(B)/S_nn(B); VIS PSF fitting: F_nn(IE) = F_n(IE)/S_nn(IE). FLUX_DETECTION_TOTAL does not depend on the PSF.
- S varies across each tile and from tile to tile (depends on mapping, orientation, layering); Table 4 gives statistics for tiles 102020534 (EDF-S) and 102159192 (EDF-N), e.g. IE median 0.957 (NMAD 0.011), YE/JE/HE ~0.985 (NMAD ~0.005-0.007), PS-i 0.880.
- The IE PSF normalisation is the limiting factor of DR1 photometric accuracy (Fig. 12: A-PHOT offsets in DECam-i vary by tens of mmag with IE normalisation); IE-based colours cancel this dependence. McCracken et al. reach the same conclusion.
- Explicit caveat: non-normalised PSFs are "not the best choice in all cases, e.g. large extended sources" (p. 10), but were adopted to fix point-source-driven offsets. Pan-STARRS has local defects in isolated areas and was excluded from a separate photo-z run (Hartley et al.).

## Validation and performance
- Validation pipeline per tile (Sect. 3): no strict automatic limits; aggregated statistics inspected per patch; few tiles invalidated, mainly for severe processing errors (p. 6).
- Astrometry (3.1): < 10 mas for FILLING_FACTOR > 0.5.
- Detections (3.2): lower-branch ratio of VIS to NIR detections typical; tiles with unusually many NIR detections have incomplete VIS coverage (solar proton showers).
- Point-like probability (3.3): count of POINT_LIKE_PROB > 0.96 compared with Gaia DR3 matches per tile (Fig. 7).
- PSF (3.4): see above.
- Depth (3.5): empty 2" apertures; scales as expected with exposure time (Fig. 9).
- Photometry vs Gaia (3.6): transformation functions G, BP, RP -> IE, YE, JE, HE from synthetic spectra (Serrano et al. 2024) for 0 < BP-RP < 2.5; EXT bands use the transformations of the EXT calibration; more than 1000 Gaia matches per wide tile; IE offset about -0.02 mag (better than Q1); NIR offsets larger than Q1 (-0.036 to -0.126 mag); EXT offsets a few percent.
- External catalogues (3.7.1): Gasparetto et al. 2026 compares A-PHOT, T-PHOT and Sersic fluxes of extended sources in COSMOS against COSMOS2025 (Shuntov et al.): all methods slightly overestimate flux relative to COSMOS2025; T-PHOT agrees best in NIR; method systematics comparable to the bias.
- Source injection (3.7.2): Cornifer injects synthetic stars/galaxies into real VIS/NIR/EXT images and reruns MER; photometry recovered within 5%; photometric offset smaller than that against Gaia.
- Gaia homogeneity (3.7.2, the section header is garbled into the text on p. 8): selection of 0.2-1.9 million clean Gaia stars (S/N cuts G > 500, BP > 25, RP > 35; non-single-star = 0; single-star probability > 0.99; flux excess |C*| < sigma; VIS_DET = 1; no holes in central cutouts 1.5" x 1.5" VIS / 2.1" NISP / 5.1" EXT; below saturation and high S/N, magnitude ranges per band in Table 3). NMAD scatter 15-97 mmag (upper limits; includes <= 3 mmag Gaia error, colour terms and differential extinction).
- Wide vs deep (Sect. 5): tile 102020534 (EDF-S), wide exposure ~2.5/0.35/0.35/0.35 ks vs deep (9 overlapping deep tiles) ~27/2.8/2.8/2.8 ks. 96,704 of 114,810 wide objects matched within 0.3" in the deep list. Unmatched wide sources: 54% VIS-detected, 46% NIR-detected (NIR over-represented since only ~20% of objects are NIR-detected). Causes (Fig. 13): diffraction spikes that differ between wide and deep; differing deblending at different S/N; diffuse NIR detections not confirmed in deep (NIR detection limit too shallow); unmasked cosmics/bad pixels in NIR. Conclusion: over-deblending in wide, under-deblending in deep; parameter tuning per depth is under study for DR2. A smaller deblender scale factor improves most critical cases but over-deblends others (Fig. 14, cutouts near RA 149.92, Dec 2.43 etc., COSMOS).
- Wide vs deep photometry: offsets <= ~0.01 mag over a wide dynamic range, Malmquist bias at faint end (Fig. 15, p. 12).
- Wide vs deep morphology (5.3): 56,194 valid galaxies (cleaning as Quilley et al. 2026), 48,641 with successful Sersic fits in both; for IE < 23 (Euclid Morphology Challenge limit: negligible bias, < 10% scatter) only 6.1% removed for poor fit vs 13.4% at all magnitudes. Re: median relative difference < 1% for IE < 23.5, 68% within +-10%. Sersic n: slightly higher in wide for the brightest bins (median relative difference 6.4% and 2.6%), scatter grows faster with magnitude. q: median difference < 0.012 (< 0.005 for IE < 23.5) with mild asymmetry (upper tail wider; (median-P16)/(P84-median) 1.09-1.81). No trend of differences with parameter value. Conclusion: Sersic parameters are robust to depth at least to IE ~ 23. See Sazonova et al. 2026 for image-quality effects on morphology.

## Known issues, caveats, limitations
- T-PHOT bug (found after processing) affects bright, point-like sources; template-fit and PSF-fit photometry (esp. PSF photometry, about -0.13 mag) should be used with caution (p. 8).
- NIR photometry offsets vs Gaia (-0.04 to -0.13 mag) larger than in Q1; derived with theoretical transformations (p. 8).
- PSF stamp limited to 5"; flux beyond stamp is accounted for via non-normalised PSF, but not recoverable for extended wings; photometry of large extended sources may be suboptimal with non-normalised PSFs (p. 10). T-PHOT total flux limited by segmentation area and PSF extension (p. 4).
- A-PHOT: pixels of other segmented sources are masked but contamination from faint extended wings of neighbours (and from the target's own outskirts in the aperture-matched images) persists (p. 4). Total flux relies on Kron in the detection band scaled by colours; Kron is truncated for large galaxies with outskirts (not discussed in the paper beyond that).
- Methods optimised for faint and extended sources, not bright stars; comparisons with Gaia are therefore sub-optimal (pp. 4-5).
- Over-deblending in wide, under-deblending in deep; no per-depth parameter tuning in DR1; same SE++ parameters for EWS and EDS (pp. 4, 11). Spurious classifier trained on wide-like simulations only. NIR detection threshold too low for wide: false diffuse NIR detections; unmasked bad pixels/cosmics give false NIR detections (p. 11).
- False VIS detections along diffraction spikes (wide); flagged in DET_QUALITY_FLAG (p. 10).
- Partially covered border tiles: zeros in empty areas; S/N falls towards borders; 88% of tiles have coverage > 80%. Incomplete coverage in a band (> 10% smaller than the VIS+NIR coverage): 34 (IE), 405 (YE), 560 (JE), 510 (HE) tiles (pp. 13-14). Tile 102015130 JE has only 2 layers instead of 4 (Fig. 18); tile 102015171 has JE/YE/HE ~50% filled (Fig. 19). Caused by solar proton showers.
- CAS asymmetry in Q1 was biased in low-FILLING_FACTOR tiles; fixed in DR1 by local noise (Fig. 4). Q1-derived analyses should be redone.
- Pan-STARRS i PSF > 5" normalisation 0.88; local PS defects (p. 10).
- IE PSF-normalisation uncertainty (tile-to-tile and within tile, ~1% NMAD) limits absolute photometry (Fig. 12).
- VIS PSF FWHM drifted from 0.210" to ~0.203" in ILS-WAVES-S after de-focused PDC campaign (p. 14).
- No special tiles processed in DR1: galaxies larger than the overlap of normal wide tiles (> ~2' size, tile overlap/enlargement in Q1) may still be cut at tile boundaries in DR1 (the text says adjustments to wide tiling were made; the special tile solution exists but was not run).
- Spurious classification: SPURIOUS_FLAG at 0.5 too aggressive; use 0.7.
- Pan-STARRS was excluded from a second photo-z processing.

## Implications for extended-galaxy photometry, 2-D modelling and low-surface-brightness work
- LSB/background: this paper gives almost no information on the sky-background model. It merely notes that wide-vs-deep photometry shows no sign of background problems at the ~0.01 mag level for compact/cross-matched sources, which says little about the LSB regime. You must read the Q1 MER paper (Romelli 2026) and the VIS/NIR papers for the background strategy (mesh size, masking, over-subtraction around large galaxies), and test on your own targets (e.g. growth curves vs. sky annuli).
- Large galaxies: the special-object catalogue (164,526 objects > 2') is designed to protect large galaxies from tile edges and to include their tidal features (box = 4 x diameter), but the DR1 processing only used normal and extended Wide tiles; special tiles ("1025...") were not run in DR1. Check whether a target of interest crosses a tile border; in that case you may need to mosaic neighbouring tiles yourself (tile overlap in wide tiling unspecified in this paper; deep overlap 2').
- Shredding: deblending (ASTErIsM, scale factor) is tuned for compact sources; wide-tile over-deblending is documented. Large, resolved low-z galaxies are likely to be fragmented into several catalogue entries (spiral arms, HII regions, bulges), especially in IE; the paper provides no dedicated statistic for large galaxies. Use SEGMENTATION_MAP_ID, DET_QUALITY_FLAG, and visual checks; for nearby galaxies, plan to re-measure from the mosaics with your own masks.
- Sersic fits: SE++ with fit area derived from the segmentation area; the fit area is limited only for saturated stars in DR1, so bright galaxies get the full area, but segmentation-limited areas may truncate the outskirts of galaxies with faint wings. The PSF stamp (5") is small compared with the extent of the VIS/NIR PSF wings; PSF convolution used non-normalised PSF (flux beyond the stamp is not added), which changes Sersic fluxes by the factor S_nn(B) (about 4% in IE) - Eq. (2). Sersic n_max is 8.0; n > ~7.9 is a boundary value. Wide-vs-deep reproducibility is good (Re within 1%, n within a few percent, q within 0.01) for IE < 23.5, which supports using the fits for bright (IE < ~23) galaxies. For bright low-z galaxies, single-Sersic is inadequate; bulge-disc decompositions must be done by yourselves from the cutouts/mosaics (no bulge-disc catalogue is described here).
- Fluxes: for total flux of extended galaxies prefer Sersic or FLUX_DETECTION_TOTAL (Kron) over the 1-4 FWHM apertures; A-PHOT fluxes in apertures are PSF-matched to the worst PSF (EXT bands), so they are aperture colours rather than total fluxes.
- FLUX_RADIUS: SExtractor-style radius at 50% flux within 6 a_M; a_M is the catalogue semi-major axis, so it depends on segmentation; not a robust half-light radius for galaxies with extended outskirts.
- Bright-star masks: diffraction spikes and saturated cores are flagged; large halo/scattered-light areas around stars are NOT described here (see odier for photometric masks, and da Silva for PSF wings).
- ICL/halo work: the 5" PSF stamp and the segmentation-based photometry are not appropriate; use the mosaics directly.

## Practical recommendations for users
- Use TILEID prefixes to separate data: 102xxxxxx = wide tiling, 101xxxxxx = deep tiling, 1025xxxx = special (none in DR1).
- Check FILLING_FACTOR (tile coverage; > 0.5 for good astrometry, > 0.8 for typical tiles) and the layer file (number of layers, exposure time) before interpreting depth near tile edges or in tiles with solar-proton-affected data.
- Cut on DET_QUALITY_FLAG (spikes, saturated cores), SPURIOUS_FLAG with SPURIOUS_PROB < 0.7, POINT_LIKE_FLAG for stars.
- For Sersic fits require SERSIC_VISNIR_FLAGS to be free of error bits (0, 4, 9, 12) and consider bits 5 and 1 (downsampled or resized fit boxes, typical for big objects); treat n close to 8 as non-converged.
- Prefer IE < 23 for morphology; for IE colours the IE PSF normalisation cancels.
- Use colour-scaled Kron totals (see Photometry Cookbook) rather than direct T-PHOT totals; avoid PSF-fit photometry and be careful with T-PHOT NIR fluxes for bright point-like sources.
- When comparing with Q1, remember: new PSF normalisation (Eqs. 1-3), different CAS noise, n_max 8.0, new input calibrations.
- For wide-vs-deep consistency studies use EDF data processed in both tilings (e.g. EDF-F).
- Use the Explanatory Supplement cookbooks for details.

## Objects, fields and figures worth revisiting
- Tiles: 101837492 (EDF-N deep, exposure time map, Fig. 3, p. 3); 102020534 (EDF-S wide, wide-vs-deep tests, Figs. 12, 13, 15, 16); 102159192 (EDF-N, Table 4); 102036162 (EWS border tile, 52% coverage, Fig. 17, RA ~3h49m-3h50m = ~57.4 deg, Dec ~ -34.3 to -34.8 deg, read off the axes); 102015130 (JE shallow coverage, Fig. 18, RA ~1h43m-1h45m, Dec ~ -54.8 to -55.2); 102015171 (partial NIR coverage, Fig. 19, RA ~4h03m-4h06m, Dec ~ -54.8 to -55.3). Coordinates are read from figure axes, not from the text.
- Cutouts in COSMOS region (Fig. 14, p. 11): around (RA, Dec) = (149.92, 2.43), (149.88, 2.46), (149.95, 2.54) deg - examples of segmentation under different deblending configurations.
- Fig. 2 (p. 2): Wide/Deep tiling in EDF-F, RA ~52.75-54.25, Dec ~ -28.2 to -27.2 deg.
- Table 5 (p. 15): all DR1 fields: EWS, EDF-N, EDF-S, EDF-F, CDFS, COSMOS, AEGIS, SELFCAL, F-014, PN, SSO-ECLIPTIC, EMDS-HSC-HL-3, EMDS-HSC-HL-4, ILS-WAVES-S, with tiling, number of tiles, exposure times, source density, EXT bands.
- Fig. 4 (CAS asymmetry vs filling factor), Fig. 10 and Table 3 (photometry accuracy), Fig. 12 (IE PSF normalisation), Fig. 13-14 (deblending), Fig. 16 (Sersic wide vs deep).
- No named individual galaxies are given in this paper; the special-object catalogue is built from HyperLEDA, HECATE, EDD, SIMBAD, RC3, UNGC.
- Recommended figure views: p. 11 (Figs. 13, 14), p. 12 (Fig. 16) - not viewed here (text only).

## Cross-references
- Romelli et al. 2026 (Q1 MER, A&A 711, A4): mosaicing, background, kernels, photometry details, Photometry Cookbook basis.
- da Silva et al. 2026 (NISP-P PSF), Ruffenach et al. 2026 (processing / OTF and PSF processing), McCracken et al. 2026 (OU-VIS), Polenta et al. 2026 (OU-NIR), Corcho-Caballero et al. 2026 (OU-EXT).
- Gasparetto et al. 2026 (photometry comparison with COSMOS2025), Kong et al. in prep. (Cornifer source injection), Quilley et al. 2026 (Sersic validity), Sazonova et al. 2026 (image quality effects on morphology), Walmsley et al. 2026 (Zoobot), Bretonniere et al. 2023 (Morphology Challenge), Hartley et al. 2026 (photo-z), Aussel et al. 2026a,b (Q1, DR1 overview), Odier et al. (photometric masks), Schirmer et al. 2026 (calibration fields), Neumann et al. 2026 (PDC campaign).
- Explanatory Supplement: Photometry and Morphology cookbooks, MER product chapters.
