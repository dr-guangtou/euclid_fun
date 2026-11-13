---
title: "Euclid Quick Data Release (Q1): From images to multiwavelength catalogues: the Euclid MERge Processing Function"
short_name: romelli_etal
first_author: Romelli
series: "Euclid Q1 coordinated release (2025); reference for DR1 processing"
local_pdf: ~/Desktop/euclid/papers_q1/romelli_etal.pdf
local_text: ~/Desktop/euclid/text/papers_q1/romelli_etal.txt
topics: [MER, tiling, mosaicing, SWarp, bilinear kernel, median combine, background subtraction, BGMOD, SourceExtractor++, detection, ASTErIsM deblending, A-PHOT, T-PHOT, Kron, Sersic, CAS, PSF propagation, bright-star masks, Q1 known issues]
relevance_extended_galaxies: high
---

# The MERge Processing Function at Q1 (Romelli et al. 2025; A&A 2026)

## TL;DR
Q1 reference description of the whole MER pipeline that the DR1 MER paper (Kuemmel; see kuemmel.md) only amends. It defines the 32'x32' tiles on a 0.1"/pix grid, the SWarp mosaicing (bilinear kernel, median combine, RMS weights), the one and only MER-level sky step (a 256x256 px mesh, 3x3-cell median filter, source-masked, spline-interpolated model that is subtracted and stored as BGMOD), the VIS and NIR detection/deblending, and the four photometry families. For LSB and extended-galaxy users the critical points are: (i) the MER sky is a second background subtraction applied after the per-exposure VIS and NIR subtractions, (ii) the paper never quantifies its effect on large galaxies, (iii) the delivered BGMOD file lets you undo only the MER step, and (iv) the mosaic pixel unit and flux zero point are not given in this paper (only that the co-add ZP is the rounded median of the input ZPs).

## Key facts and numbers
- Tiling (p. 3-5): tiles independent of survey strategy, cover -88 < Dec < +88 deg; extended area 32'x32' in tangent projection; centres spaced by 30', so 2' overlap between neighbours; centres start at (0,0) in constant-Dec strips; core areas are HEALPix Nside = 13 pixels (a pixel is assigned to the tile in which it is farthest from the border); catalogue output only for the core area, imaging output for the whole extended area (p. 3-4).
- Large galaxies (size > 2' from public catalogues) that cross a tile boundary make the tile holding their centre "breathe" (be enlarged); example: tile 102158273 (EDF-N) height raised to 33' to contain PGC61126 (p. 5, Fig. 3). Covered all large galaxies in the Q1 area.
- Mosaic pixel scale 0.1"/pix (VIS native 0.1", NIR native 0.3"); EXT frames (e.g. DES 0.264"/pix) rebinned with a BILINEAR kernel (p. 5).
- VIS+NIR co-add: kernel BILINEAR, combine type MEDIAN, RMS maps used as weights, software CT_SWarp (SWarp integrated in Euclid environment) (p. 5).
- Co-add zero point: global weights are scaled so the zero point of the co-added image equals the median of the input zero points, rounded to one decimal place (p. 5). No numeric value, pixel unit or ZP keyword name is quoted in this paper.
- Flag handling: a new BILINEAR_FLAGS interpolation kernel in CT_SWarp combines input flag information with a bitwise XOR (p. 5).
- MER sky (p. 5-6): mesh 256x256 px (= 25.6"), filter box 3 cells (= 768 px = 76.8" across), see Processing section.
- Detection parameters (Table 1, p. 6): segmentation-filter Gaussian FWHM 2.4 px (VIS) / 5.0 px (NIR); detection-threshold 0.9 / 0.4; detection-minimum-area 10 / 10 px; core-threshold-value 1.3 / 0.55; core-minimum-area 10 / 10 px. Tuned on simulations for < 1% false detections (p. 7).
- About 20% of sources in a test cutout are NIR-only; 141 VIS and 31 NIR detections in the Fig. 4 cutout (p. 8).
- PSF FWHM check (Table 2, p. 9): EWS IE 0.203" (min 0.197, max 0.212) vs Gaia stars 0.204"; YE/JE/HE propagated 0.475/0.504/0.542" vs Gaia stars 0.492/0.513/0.552" (propagated NIR PSFs 1.75-3.5% too compact). Propagated VIS/NIR PSFs are 30-35% wider than the input PSFs because of stacking; the BILINEAR kernel (instead of LANCZOS3) adds about 15% extra broadening (p. 8).
- PSF stamp separation: stamps smaller than 3"; propagation repeated three times with different source subsets to avoid overlap; more than 80% of sources get their own stamp, the rest use the nearest stamp (p. 8).
- Kron: aperture semi-major axis 2.5 R_Kron, circular region of radius about 6a for the first moment, boundary pixels split into 10 sub-pixels (p. 9).
- A-PHOT circular apertures: diameters are integer multiples of the FWHM of the worst-resolution band (typically an EXT band with FWHM about 1"), so 2 FWHM is about 2" (p. 9, p. 16).
- Zoobot (Q1): galaxies with IE < 20.5 or segmentation area > 1200 pix (about 1% of galaxies); ConvNeXt Nano, fine-tuned on 1.56 million labels from an August 2024 campaign (p. 12).
- POINT_LIKE_FLAG = POINT_LIKE_PROB > 0.96 and DET_QUALITY_FLAG = 0; star rule of thumb IE < 17 or POINT_LIKE_PROB > 0.96; only VIS-detected objects are classified (p. 13).
- SPURIOUS_PROB threshold 50% by default (90% of true spurious recovered, 0.13% of real lost); 75% gives 80% / 0.04% (p. 14). RFC trained on 430 000 simulated sources, 26 features.
- Gaia match radius 0.3" (epoch-propagated); 800-3000 Gaia matches per catalogue (p. 14-15).
- Q1 run: about 140 core hours per tile; mosaicing + background + PSF 13%, detection + deblending 10%, photometry and kernels 75% (p. 3).
- Validation (p. 15-18): depth from random empty 2" apertures (tile 102021017: depths roughly 24-25.6 mag, 5 sigma, Fig. 12); Gaia validation sources IE < 19.5. EDF-S mean offsets vs Gaia: A-PHOT IE -0.0688 +- 0.0029, YE -0.0202, JE -0.0306, HE -0.0078 mag; T-PHOT YE -0.0809, JE -0.0746, HE -0.0426 mag; DECam g/r/i/z A-PHOT -0.0285/-0.0086/+0.0007/-0.0018 (p. 17). Authors state offsets drift over the campaign and causes are under investigation (p. 18).
- Tile 102021017 (EDF-S): 88 317 VIS and 27 808 NIR detections, 3 370 bright-star-masked, 1 104 Gaia matches (Fig. 13, p. 17).

## Data products and data model
(Appendix A, p. 23; DPDD at euclid.esac.esa.int/dr/q1/dpdd)
- File name pattern: EUC_MER_[TYPE]_TILE[INDEX]-[RND]_[TIME].fits.gz (or json), e.g. tile index 102022523.
- Image-type files per band (band labels in Table 3, p. 14: VIS (=IE), Y, J, H, NIR_STACK, and EXT labels such as G_EXT_DECAM, R_EXT_MEGACAM, I_EXT_PANSTARRS, Z_EXT_HSC, U_EXT_MEGACAM):
  - BGSUB-MOSAIC-<band>: background-subtracted mosaic image (DPDD product DpdMerBksMosaic).
  - MOSAIC-<band>-RMS: mosaic RMS map.
  - MOSAIC-<band>-FLAG: mosaic flag map (flags combined with XOR in resampling; individual bit definitions are not listed in this paper).
  - BGMOD-<band>: the background model subtracted from the mosaic.
  - FILTER-TRANSMISSION-<band>: average filter transmission wavelength per pixel.
  - DETECTOR-LAYERING-<band>: input layer information.
  - CATALOG-PSF-<band>: PSF stamps at catalogue positions (FITS with a grid of stamps plus a table of sky/pixel coordinates; p. 8). GRID-PSF-<band>: PSF on a grid. Stamp size and radius are not stated for MER in this paper (input VIS/NIR stamps are under 3"; DR1 paper says MER stamps are limited to 5").
  - STAR-MASKS-<band>: bright-star polygons (JSON list; p. 14).
  - Detection mosaics: VIS and NIR_STACK background-subtracted images used for detection (DpdMerDetectionMosaic); NIR stack is a weighted sum of YE, JE, HE with a common zero point (p. 6).
  - FINAL-SEGMAP: segmentation map of the combined VIS + NIR-only detections (DpdMerSegmentationMap); refers only to the inner (core) tile region; sources between the outer and inner region are not catalogued and their pixels are set to -1 (Fig. A.1, p. 23).
- Catalogues (p. 13-14, 23): EUC_MER_FINAL-CAT (OBJECT_ID, coordinates, quality flags, photometry), FINAL-DEEP-CAT (extra EXT filters in deep fields), FINAL-MORPH-CAT (morphology; shares OBJECT_ID), FINAL-CUTOUTS-CAT (cutout corners). More than 3 200 columns in total.
- Important columns named: OBJECT_ID, PARENT_VISNIR (marks artificial VIS/NIR-only blends touching without sky between them, p. 8), DET_QUALITY_FLAG (bright-star-mask membership in two separate bits: IE mask vs any of YE/JE/HE masks, p. 14), DEBLENDED_FLAG, FLAG_<band>, POINT_LIKE_PROB, POINT_LIKE_FLAG, SPURIOUS_PROB, SPURIOUS_FLAG, MU_MAX, MAG_AUTO, GAIA_ID, GAIA_MATCH_QUALITY (squared Euclid-Gaia distance), FILLING_FACTOR and ASTROMETRY_RA/DEC_OFFSET (tile-level validation quantities), E(B-V) with error from Planck R1.20 (p. 13).
- Photometry in catalogue (p. 8-10): Kron total flux on detection mosaic (FLUX_AUTO-like), flux in the segmentation area (FLUX_ISO-like, p. 10), PSF-matched aperture fluxes in all bands, T-PHOT template-fit fluxes in all bands plus detection-band flux smoothed to each band's resolution, PSF-fit flux in VIS only, Sersic fluxes in all bands.
- Pixel unit of mosaics, MAGZERO/ZP header keyword, conversion to microJy and to mag/arcsec^2: NOT given in this paper. Magnitudes are AB. For the single-exposure inputs: VIS is in ADU with ZP 24.57 (see q1_mccracken_vis.md) and NISP in electrons with ZP/inverse sensitivity in the header (see q1_polenta_nir.md); the mosaic ZP is the rounded median of those. Check the SCI header and the DPDD for the actual keyword.

## Processing and methods
1. Initialisation and mosaicing (Sect. 2-3.2, p. 3-5): decompress and sort inputs; for each tile take all VIS (nominal + short) and NIR calibrated frames; subtract the background estimate supplied with the VIS/NIR frames; rebin and co-add with BILINEAR kernel, MEDIAN combination, RMS-based weights; zero-point-aware global weights; flags combined with BILINEAR_FLAGS (XOR). Output per band: co-add, RMS, flag. EXT stacks (already per tile, native scale) rebinned to 0.1"/pix with BILINEAR. NIR and EXT are on the same grid/centre/size as VIS.
2. MER background subtraction (Sect. 3.3, p. 5-6), applied to every mosaic (VIS, NIR bands, EXT bands; Fig. 1 shows a background-subtraction box in each branch). Purpose stated: remove residual background because a flat background is essential for precise photometry (p. 3).
   - Pre-masking: a segmentation mask from an SE++ detection run is applied to avoid contamination by bright extended sources. Which SE++ parameters are used for this masking pass, and whether the mask is grown, is not stated.
   - Grid: cells of 256x256 pixels (25.6" on the 0.1" grid; for the 0.3" NISP native data this is irrelevant because all bands share the 0.1" mosaic grid).
   - Per-cell estimate: iterative clipping to convergence at 2 sigma around the mean. If after convergence the mean and median differ by more than 3 sigma (crowded fields) the cell value is the mean of the clipped histogram; otherwise it is the mode estimated as B = 2.5 M - 1.5 mu (M median, mu mean of clipped histogram).
   - Cells with no unflagged pixels: gaps filled with a distance-weighted average of the edge cells around the gap.
   - Smoothing: median filter over the grid with a box of 3 cells to suppress local overestimates from bright-star residuals.
   - Model at full resolution: spline interpolation of the cell values; subtracted from the mosaic; the model itself is stored as BGMOD-<band>.
   - Only two parameters control it: grid size 256x256 px and filter box 3 cells. A single pass; no iteration of mask-estimate beyond the clipping is described.
   - Aperture photometry afterwards does no local background subtraction because "two background subtraction steps have already been performed" (p. 9): the first is the per-exposure VIS/NIR step, the second this MER step.
3. Detection (Sect. 4.2, p. 6-7): SE++; convolve image and RMS with the segmentation filter, threshold on S/N per pixel, keep connected sets above the minimum area. Because a low threshold would make detections around large galaxies pick up the outer parts as separate "objects", a second, higher "core" threshold requirement validates objects (need core-minimum-area pixels above core-threshold-value), allowing a low main threshold that follows bright galaxies out to fainter isophotes while rejecting noise peaks. VIS detection image = BGSUB mosaic; NIR detection image = weighted sum of YE+JE+HE BGSUB mosaics.
4. Deblending (Sect. 4.3, p. 7): ASTErIsM-derived component (DBSCAN to identify sources, modified DENCLUE with kernel density estimation replaced by image convolution to separate overlapping sources and spiral-arm-like features) run independently on the VIS mosaic and NIR stack on downsampled segmentation clusters. Two parameters (typical blend scale; convergence criterion for local maxima) were tuned on True Universe simulations by minimising the number of over- and under-deblended objects against a ground-truth segmentation map.
5. VIS + NIR merging (Sect. 4.4, p. 7-8): all VIS objects are kept; NIR objects whose projected centre falls on a non-zero VIS segmentation pixel are dropped; the rest are "NIR-only". Segmentation map = VIS map plus NIR-only pixels (VIS pixels never overwritten; NIR-only areas shrink and properties are recomputed; objects falling below the minimum area are discarded). Admitted drawback: red sources close to VIS objects can be disfavoured.
6. PSF propagation (Sect. 5, p. 8): VIS PSFs from PSFEx per quadrant, assumed constant for an observation; NIR PSFs per detector and frame from PSFEx; they are propagated by running SWarp on zero-valued images with PSF stamps injected at deblended source positions (keeping ZP, WCS, flags, RMS), giving an averaged stamp per source and band. No colour dependence of the PSF. Convolution kernels between bands use Wiener filtering with a tunable regularisation (Boucaud et al. 2016), computed from higher- to lower-resolution bands.
7. Photometry (Sect. 6, p. 8-10): (a) Kron total flux on the detection mosaic with R_Kron = max(a lower bound proportional to the semi-major axis a from deblending, and the first-moment radius; the printed formula reads 7a, check the PDF) and aperture 2.5 R_Kron; (b) A-PHOT PSF-matched circular apertures, total in band B from f_tot,B = f_ap,B * f_tot,det / f_ap,det (Eq. 3); errors from the PSF-matched RMS map; (c) T-PHOT template fitting with detection-band cutouts convolved to the measurement resolution as priors, chi-squared minimisation, fitted individually per source in a cell containing its contaminants and removed after fit (not the full image); direct output is a proxy for total flux; detection-band flux smoothed to each band's resolution also given for alternative colours; (d) PSF-fit flux (VIS only, T-PHOT); (e) Sersic fits with SE++ (below). Error budgets are noise-only (no systematics such as blending).
8. Sersic (Sect. 7.2, p. 12): SE++ model-fitting mode (from v0.21) with inputs given in a table (centres, fitting areas, starting values). Step 1 on VIS+NIR: R, ellipticity, n fitted independently for IE and for the NIR bands (separate sets), common position angle for VIS and NIR, centres fixed, fluxes in IE, YE, JE, HE. Step 2 on EXT g,r,i,z: Sersic shape fixed to the VIS values, only flux fitted. Errors from the covariance matrix. Scientific evaluation delegated to Quilley et al. The paper does not say what fitting area or PSF stamp size is used, nor how neighbours are handled.
9. CAS, Gini and M20 (Sect. 7.1, p. 11-12) computed on IE images covering each segmentation map; ML morphology (Zoobot, p. 12); S/G (p. 13); spurious classifier (p. 14); bright-star masks (below).
10. Bright-star masking (Sect. 8.3, p. 14): Gaia stars (up to magnitude 8 are observed) mapped as a central circle, rectangles for the three diffraction spikes and a rectangle for the VIS blooming pattern, sizes scaling with brightness, built on single calibrated frames and unioned after projection to the mosaic; saved as polygons in JSON; objects inside are flagged in DET_QUALITY_FLAG.

## Validation and performance
- Astrometry (p. 15): tile-mean offset vs Gaia within about +-0.03" for EDF-S tiles (Fig. 11); larger offsets occur at field borders (low FILLING_FACTOR) from VIS systematic residuals.
- Depth (p. 15-16): empty random 2" apertures; authors explicitly caution that resampling and variable exposure time make the numbers relative quality indicators, not absolute.
- Detection checks (p. 16): FILLING_FACTOR (fraction of HEALPix pixels with at least one detection); vertical lines of NIR detections in Fig. 13 come from insufficiently masked persistence.
- PSF (p. 16-17): Gaia stars with CLASSPROB_DSC_COMBMOD_STAR > 0.99, G > 18, 300-600 stars per tile; stamps of 2.1" (Euclid) and 4.5" (EXT); VIS PSF FWHM varies by more than 20% across a tile; agreement within +-2% for VIS (Fig. 15).
- Photometry (p. 16-18): see numbers above; only bright stars validated; checks against galaxy catalogues "reasonable" but too uncertain to quantify. Authors' qualitative result from direct checks on mosaics: aperture photometry is best for bright point sources whereas template fitting is better for extended objects and in blends (Fig. 5: T-PHOT magnitudes typically fainter because neighbour light is removed; example 19.81 +- 0.02 from colour-scaled aperture vs 19.99 +- 0.01 template).
- Point-like check (p. 18): tile 102021017: 1 104 Gaia matches vs 1 070 objects with POINT_LIKE_PROB > 0.96 (744 matched, 326 not, the latter fainter than the Gaia limit).

## Known issues, caveats, limitations
- MER sky subtraction effect on large/bright galaxies and diffuse light is not quantified or discussed anywhere in this paper; the step is justified only by a flat background for photometry (p. 3, 5-6). It is a second subtraction on top of the per-exposure VIS NoiseChisel/SExtractor and NIR SExtractor background subtraction (p. 5, 9). Independent analysis (Bamford et al., see q1_icl_processing_bamford.md) finds that the combination removes diffuse light above about 10" in VIS and about 0.5' in NIR and that photometry of sources below about 10" is safe.
- No detection-aware iteration of the background: the mask comes from one SE++ detection pass; the 256 px mesh and the 3-cell filter can therefore still absorb the faint outskirts of objects larger than the 25.6" cell, and the median filter over 3 cells (about 77") is the only protection against bright-star residuals (the paper's own wording for the filter's purpose).
- Gap filling by distance-weighted edge values and spline interpolation can produce smooth model structure at tile borders and around masked large objects (inferred from the algorithm; not discussed in the paper).
- Detection around large, extended galaxies still yields false sources in the outskirts if the single threshold is low; the core-threshold scheme is the mitigation (p. 6). Deblending parameters are tuned on simulations and the authors acknowledge the difficulty of dense fields (p. 7); no statistics on fragmentation of large resolved galaxies are given.
- Merging favours VIS objects: NIR-only sources adjacent to VIS objects may be lost (p. 8). Artificial VIS-NIR blends are marked only via PARENT_VISNIR.
- Bilinear resampling in MER (not LANCZOS) correlates noise and adds about 15% to PSF FWHM; propagated PSFs are 30-35% wider than input PSFs (p. 8).
- NIR propagated PSFs are 1.75-3.5% too compact vs Gaia stars; NIR PSF issues make T-PHOT NIR total fluxes of bright point-like sources worse than A-PHOT (p. 8, 10).
- A-PHOT/T-PHOT colour offsets and absolute offsets of a few percent (up to -0.08 mag in IE and T-PHOT NIR) varied during the campaign; causes under investigation (p. 17-18). Error budgets exclude systematics such as blending (p. 10).
- A-PHOT does no local sky subtraction; any residual sky error (including over-subtraction in extended galaxies) goes straight into aperture and Kron fluxes (p. 9).
- Star/galaxy classifier is high purity, low completeness (p. 13); spurious classifier trained on simulations, 50% default threshold (p. 14).
- Persistence residuals in NIR create spurious NIR detections (Fig. 13, p. 16).
- Solar X-ray bursts hitting VIS reduce detections (p. 18).
- VIS blooming, saturated cores and spikes are handled only by polygon masks; no ghost masks are described in this paper.
- Status in DR1 (check against kuemmel.md, mccracken.md, polenta.md): PSF stamps no longer renormalised to unit sum (Q1 renormalised, up to about 10% offsets in broad-PSF bands) (fixed/changed); NIR PSFs much improved (da Silva); Sersic n_max raised from 5.5 to 8.0; CAS asymmetry noise measured locally (Q1 asymmetry biased in low-coverage tiles) (fixed); Zoobot selection widened (IE < 21 or segmentation area > 700 px); deep 17'x17' tiles added; special-object tiles for galaxies larger than 2' defined but not run in DR1; T-PHOT bug found after DR1 processing; SPURIOUS threshold advice 0.7; VIS/NIR per-exposure background is still supplied separately and NoiseChisel is now used in NIR (10x10 px tessellation); VIS ghosts and serial bleeding remain. The DR1 MER paper does not describe the MER background step at all, so assume it is unchanged until the Explanatory Supplement or the DR1 products show otherwise.

## Implications for extended-galaxy photometry, 2-D modelling and low-surface-brightness work
- Treat every BGSUB mosaic as sky-subtracted at 25.6" mesh scale with a 77" filter. Any galaxy halo, ICL or tidal feature smoother than roughly the filter scale and larger than about 10" is partially subtracted; the effect is strongest where the object fills the mesh (for example a nearby galaxy with D25 over 2').
- The MER subtraction can be undone by adding BGMOD-<band> back to BGSUB-MOSAIC-<band> (same grid; the model is stored at the mosaic resolution). This recovers the light removed at the MER step only. It does not recover what the per-exposure subtraction removed before co-adding (VIS NoiseChisel per quadrant, NIR 64x64 px SExtractor background in Q1, NoiseChisel 10x10 px tessellation in DR1), because the co-add used background-subtracted frames (p. 5). In Q1 the VIS/NIR background maps were delivered with each calibrated frame; re-stacking from calibrated frames is the only way to avoid both steps.
- Tile size and breathing: a 32'x32' tile with 2' overlap holds all galaxies smaller than about 2'; larger galaxies were handled by enlarging the home tile (Q1) but they are exactly the cases where the sky mesh is least safe. A galaxy near a tile edge sees a one-sided mesh.
- Median combination with bilinear resampling is robust against artefacts but noisier and smoother than a weighted mean; surface-brightness profiles at the faint end carry correlated noise (pixels are not independent after bilinear rebinning).
- Photometry: for extended galaxies use Sersic or Kron fluxes with awareness that the Kron aperture (2.5 R_Kron) is built from a deblended semi-major axis and that A-PHOT contains no local sky correction; T-PHOT is better in blends; aperture-colour-scaled totals use f_ap ratios (Eq. 3). Large nearby galaxies may be shredded by DENCLUE deblending; there is no safeguard documented.
- 2-D modelling: PSF in the catalogue stamps is much broader than the native one (bilinear kernel, 30-35% wider); if you fit on the mosaic you must use the MER-propagated PSF, not the VIS PSF model. PSF wings are not characterised in this paper (stamp sizes below 3" for inputs).
- The paper gives no surface-brightness limit, no MAGZERO/pixel-unit recipe and no mag/arcsec^2 conversion; derive the SB zero point from the mosaic header and the pixel area (0.01 arcsec^2 per pixel).

## Practical recommendations for users
- Do read the mosaic header for the ZP and unit before converting to mag/arcsec^2; do not assume it matches the single-exposure values (the co-add ZP is the rounded median of the inputs, p. 5).
- Do add BGMOD back (BGSUB + BGMOD) and re-estimate your own large-scale, object-masked sky for any target larger than about 10", then compare with the original.
- Do inspect FLAG and STAR-MASKS near very bright stars; do not interpret faint structure inside diffraction-spike or blooming polygons.
- Do prefer T-PHOT for blended extended galaxies in NIR (Q1 finding) and A-PHOT for bright point sources; do not combine templates-based totals across bands without checking against Kron colour scaling.
- Do use FILLING_FACTOR, DET_QUALITY_FLAG, SPURIOUS_FLAG (consider threshold 0.7 as in DR1) and POINT_LIKE_FLAG; do not use PSF-fit photometry for galaxies (VIS only, point-source oriented).
- Do not rely on catalogue entries for the outskirts of large galaxies (source fragmentation, false sources); work from the mosaic with your own masks.
- Do check whether your target crosses a tile border (2' overlap) and, if so, mosaic neighbouring tiles yourself.

## Objects, fields and figures worth revisiting
- Tile 10215949 (EDF-N), centre (RA, Dec) = (272.9038602, 66.5) deg: tile geometry (Fig. 2, p. 4-5; core in magenta, extended in blue).
- PGC61126 (large galaxy in EDF-N) inside enlarged tile 102158273 (RA about 17h50m-18h05m, Dec about +64.0 to +65.0, read off Fig. 3 axes): the breathing-tile example (p. 5).
- Tile 102021017 (EDF-S, RA about 63.2-63.8 deg, Dec about -48.3 to -48.7 deg from Fig. 13 axes; cutouts at 4h15m, -48d33'): Fig. 4 (detections VIS vs NIR, p. 7), Fig. 10 (bright-star masks, p. 15), Fig. 12 (depth), Fig. 13 (detection maps and persistence lines, p. 17).
- Tile 102021019 (EDF-S): Fig. 14-15 (PSF FWHM map and Gaia comparison, p. 17).
- Fig. 5 (p. 10): template-fit vs aperture magnitude for a blended galaxy in HE; Fig. 6 (p. 11): g-HE colour consistency.
- Key tables: Table 1 (detection parameters, p. 6); Table 2 (PSF FWHM, p. 9); Table 3 (bands and filter labels, p. 14).

## Cross-references
- kuemmel.md (DR1 MER, delta paper), mccracken.md and q1_mccracken_vis.md (VIS inputs, background maps), polenta.md and q1_polenta_nir.md (NIR inputs, background maps), q1_icl_processing_bamford.md (independent analysis of the double sky subtraction), odier.md (DR1 photometric masks), da Silva (NISP PSF), Quilley et al. (Sersic validation), Walmsley et al. (Zoobot), Tucci et al. (PHZ).
- MER Photometry and Morphology Cookbooks and DPDD (Q1 Explanatory Supplement: euclid.esac.esa.int/dr/q1/expsup).
- Merlin et al. 2015/2016/2019 (T-PHOT, A-PHOT), Tramacere et al. 2016 (ASTErIsM), Bertin et al. 2002 (SWarp), Kuemmel et al. 2022 (SE++ and tiling).
