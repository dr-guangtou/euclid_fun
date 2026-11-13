---
title: "Euclid Data Release 1 (DR1): Euclid photometric masks"
short_name: odier
first_author: Odier
series: A&A Special Issue DR1-Foundation (Nov 2026)
local_pdf: ~/Desktop/euclid/papers/odier.pdf
local_text: ~/Desktop/euclid/text/papers/odier.txt
topics: [photometric masks, VMPZ-ID, HEALPix, effective coverage, footprint, depth maps, bright-star masks, bleeding trails, Siena Galaxy Atlas, random catalogues, zodiacal light, Galactic extinction, persistence]
relevance_extended_galaxies: medium
---

# Euclid DR1 photometric masks (VMPZ-ID) (Odier et al. 2026)

## TL;DR
The OU-LE3 VMPZ-ID pipeline converts MER per-tile information (RMS maps, flags, layering files, Gaia star polygons) into 104 full-sky HEALPix maps (Nside = 16384, about 12.9" pixels, nested, explicit indexing) for the EWS and EDS: footprint, coverage, effective coverage, depth, RMS, PSF FWHM, bit mask, integration time, satellite angles, persistence, NIR astrometric scatter, Pan-STARRS artefacts, zodiacal light, Galactic extinction and star density/brightness maps, plus random catalogues. They are designed for cosmology (clustering systematics, selection of clean samples), NOT for pixel-level masking: the Nside = 16384 resolution smears out the original masks, and the star/galaxy masking is coarse (circles around Gaia stars, ellipses around large SGA galaxies, 20-30% enlarged). For galaxy-imaging users the useful bits are the area/depth/PSF statistics, the per-object EFF_COV flag, and the knowledge of what regions get masked around bright stars and nearby galaxies. The paper contains nothing on LSB scattered-light/ghost masks.

## Key facts and numbers
- HEALPix Nside = 16384, nested ordering, explicit indexing, about 12.88" resolution; chosen as a compromise so that an all-sky mask fits in memory of a Science Data Centre node (p. 2).
- 104 photometric masks produced for DR1; some redundant/correlated (p. 2).
- DR1 EWS total area 2008.8 deg2 (sum of regions with at least one VIS exposure); effective coverage preserves 1642.4 deg2, i.e. 82% (abstract; p. 6). Pixels with effective coverage > 0.8 hold ~99% of the effective area. Conclusions: reduction of 18.1% in EWS and 11-26% in EDFs (p. 8).
- EDS total area 74.7 deg2; 81% preserved. Per field: observed (effective) area EDF-F 13.2 (11.8) deg2, EDF-N 28.5 (21.1), EDF-S 33.0 (27.9); preserved 89.3%, 74.0%, 84.5%; fraction of preserved region with coverage > 0.8: 75%, 72%, 92% (p. 6).
- EWS typical IE integration time: mean 2735 s, median 2421 s (Table 2, p. 8); NISP bands mean ~338 s, median 349 s. Most area covered by 3 or 4 single-dither exposures (p. 6).
- EWS 5 sigma depth for 2" apertures (Table 2): IE median 25.69 AB (std 0.22); YE 24.14 (0.17); JE 24.29-24.3 (0.17); HE 24.28-24.29 (0.17) (pp. 6, 8). Standard deviation < 0.2 mag.
- EWS median PSF FWHM: IE 0.2028", YE 0.488", JE 0.514", HE 0.559"; spatial std ~0.004" (IE), ~0.01" (NISP) (Table 2).
- RMS noise EWS median: IE 0.003716 ADU, YE 2.077, JE 2.379, HE 2.183 ADU (Table 2). Noise vs integration time follows sigma(t) = sqrt(A t_ref/t + B) (Fig. 5).
- EDFs median IE depth (integration): EDF-F 25.93 (4842 s), EDF-N 26.91 (25330 s), EDF-S 26.85 (23560 s), consistent with 2, 11, 10 visits (p. 8). Combined EDS medians over IE, YE, JE, HE: 26.91, 25.30, 25.44, 25.45 AB mag; depth std below 0.16, 0.44, 0.40 mag for EDF-F, N, S (p. 8). EDF-S IE median FWHM 0.2034", YE 0.492, JE 0.518, HE 0.563 (Table B.3).
- MER mosaic size quoted as 19,200 x 19,200 pixels (= 32' x 32' at 0.1"/pix), at which the initial effective coverage mask is built (p. 3).
- Unobserved-pixel criterion: RMS equals 0 or exceeds sigma_thresh = 10,000 ADU (p. 2).

## Data products and data model
Product types (all HEALPix, nested, Nside = 16384; p. 2):
- DpdHealpixFootprintMaskVMPZ: integer 1 if observed, 0 otherwise; per band for IE, YE, JE, HE and all EXT bands. Built from MerBksMosaic maps (RMS and flags); MER tile pixels within a HEALPix pixel combined by logical OR.
- DpdHealpixCoverageVMPZ (table lists DpdHealpixCoverageMaskVMPZ): float 0-1 = fraction of valid MER tile pixels per HEALPix pixel, per band; for Euclid bands, polygon masks of bright-star emission are also excluded.
- DpdHealpixEffectiveCoverageVMPZ (EffectiveCoverageMaskVMPZ): float 0-1, the effective coverage combining Euclid and EXT bands (see below).
- DpdHealpixBitMaskVMPZ: uint32; bitwise OR of the MerBksMosaic flag bits of all pixels in the HEALPix pixel; meaning of bits in the MER data model (Kuemmel et al.). Persistence = bit 13 of that bit mask.
- DpdHealpixDepthMapVMPZ: float32, AB mag, per band: m = -2.5 log10( RMS * d_thresh * sqrt(A_aper/A_pixel) ) + ZP (Eq. 3), d_thresh = 5, 2"-diameter aperture, RMS and ZP taken from the MerBksMosaic maps (p. 4). (This documents that MER mosaics carry an RMS map in ADU and a photometric zero point ZP so that AB mag = -2.5 log10(ADU) + ZP; the mosaic product here is called MerBksMosaic.)
- DpdHealpixInfoMapVMPZ: float maps with an "InfoMap type" (Table 1, p. 3):
  - Tile (int64, signed): MER tile index for each HEALPix pixel.
  - SAA, AA, BA (deg): solar aspect angle, alpha, beta angle; exposure-time weighted mean from the MER layering (layer) files; not per band.
  - Exposures (s): integration time per Euclid band.
  - Noise (ADU): mean RMS per band (0 in unobserved regions).
  - PSF (arcsec): mean FWHM per band (measured only at bright stars, interpolated by cubic spline then nearest-neighbour, starting from a coarse grid).
  - Persistence: 0-1 fraction of HEALPix pixel affected by persistence (NIR only; no information on level).
  - NIR_PRMS (mas): maximum RMS offset of NIR-stack astrometric residuals, at about 30" resolution (Radovich et al. 2026), EWS.
  - PanStarrsArtefacts: binary mask, Pan-STARRS i only (see below).
  - ZodiacalLight: F/lambda* in erg/cm2/Angstrom/arcsec2, Euclid bands (Scaramella et al. 2022 Table 4).
  - GalacticExtinction (mag): Euclid bands (Scaramella 2022 Eq. 5).
  - StarNumberDensity (counts/pixel), StarBrightnessMean / StarBrightnessRms / StarBrightnessStd (e-/s in Gaia G): from DpdExtGaiaCutout (stars with G flux > 0 and valid parallax), built by VMPZ_Star_Pipeline.
- DpdHealpixRandomCatalogueVMPZ: random galaxy catalogues per tile, uniform and weighted by effective coverage (e.g. fixed mean density 80 gal/arcmin2 in Fig. 2); RA, Dec tables.
- Per-object flag EFF_COV: 1 if the object position falls on a pixel with non-zero initial (MER-resolution) effective coverage, else 0 (position only, extension ignored); stored in the second extension of the effective-coverage FITS file; defined for each object of DpdMerFinalCatalog (p. 4). This is the only masking information available at the full MER resolution.
- Pipelines: VMPZ_Star_Pipeline (stellar-distribution masks) and VMPZ_Mosaic_Pipeline (survey, satellite, instrument, sky), triggered per tile once MER products exist; first OU-LE3 PF after OU-LE2 (p. 2).
- Archive: ESA DR1 (DOI 10.57780/esa-d079c51). Exact archive table names are not given in the paper.

## Processing and methods
1. Per tile, MER mosaics (RMS maps, flags, layering files with exposure times and angles) and Gaia cutouts are combined (p. 2).
2. Masks at MER resolution are averaged/ORed and projected onto the HEALPix grid (weighted averages with zero weight for bad RMS pixels) (p. 4).
3. Effective coverage construction (p. 3-4), at MER mosaic resolution (19200 x 19200):
   - For each VIS, NIR or EXT band, pixels with RMS 0 or > 10,000 ADU are unobserved.
   - Equivalent EXT bands (e.g. HSC R, R2, I, I2) are first combined with logical OR into "effective bands"; the effective bands plus Euclid bands are then combined with logical AND (only regions observed in all bands are kept).
   - Bright-star exclusion: for IE, YE, JE, HE, the stellar polygons (central diffraction lobe plus diffraction spikes, derived from Gaia) are rasterised directly. For EXT, an extra mask uses Gaia stars with G_RP < 14 masked by circles of radius r*(G_RP) = -0.01972 G^3 + 0.65849 G^2 - 7.31734 G + 27.75053 arcmin (Eq. 1, polynomial in G_RP), enlarged by 20%. Bleeding trails for G_RP < 10.3: rectangle of total width 2 r_bleed with r_bleed(G_RP) = 0.06158 G^4 - 1.98886 G^3 + 23.65131 G^2 - 123.78714 G + 245.65947 (Eq. 2; polynomial saturated at G_RP = 4), extending 0.488' perpendicular to the bleed direction (p. 3-4; the units of r_bleed are not stated in the text, presumably arcmin like Eq. 1).
   - Extended objects masked: globular clusters and planetary nebulae from the NGC/OpenNGC catalogue (masked using their radii) and nearby galaxies from the Siena Galaxy Atlas SGA-2020 with approximate Vega magnitude MAG_LEDA < 16.5, masked with ellipses using the major/minor axes and position angles, with dimensions enlarged by 30% (p. 4).
   - Projected and averaged to Nside = 16384 -> effective coverage float between 0 and 1.
4. Pan-STARRS artefact mask: select MER sources with anomalous Pan-STARRS/VIS flux ratio (F_PS/F_VIS > 3.5 or < 1/3.5) with flux-ratio S/N > 3; Epanechnikov KDE with 30" bandwidth on 10" RA-Dec grid; adaptive density threshold; discard connected regions smaller than 30 grid pixels; project as binary HEALPix mask (p. 5).
5. Depth, noise, PSF maps from MER mosaic RMS and bright-star-based PSF FWHM measurements (see above).
6. Random catalogues from effective coverage weights.

## Validation and performance
- No explicit external validation of the masks; the paper shows that distributions look as expected: integration time uniform across the survey; noise follows 1/sqrt(t) (Fig. 5; fitted with R^2); depth std < 0.2 mag; PSF FWHM std ~0.01"; angles within survey specifications; beta angle and solar aspect angle anti-correlated; FWHM measured larger in tile overlap regions where multiple exposures combine; persistence masks show tile-correlated structures and correlate with bright-star positions (pp. 6-8, App. A).
- Consistency of EDF depths with the number of visits (2, 11, 10 visits for F, N, S) (p. 8).
- Effective-coverage losses: EWS 18.1%, EDFs 11-26% (p. 8).

## Known issues, caveats, limitations
- Resolution: Nside = 16384 (12.9") means the original small-scale masks (circles, spikes, bleed trails drawn at 0.1"/pix) are "smeared out", lowering the apparent coverage near stars (Fig. 2 middle). The HEALPix mask is therefore not suitable for masking individual objects or for pixel-level work; use EFF_COV (object-position test at MER resolution) or the MER DET_QUALITY_FLAG instead (pp. 3-5).
- EFF_COV ignores the object's extent (footnote 6, p. 4): large galaxies whose centre is in unmasked sky but whose outskirts lie under masked regions will be passed.
- Several masks are redundant or correlated (p. 2).
- PSF FWHM mask is interpolated from sparse bright-star measurements (coarse grid), so small-scale variations are not trustworthy (p. 4).
- Persistence mask gives only the fraction of pixels affected, not the level; interpretation of tile-correlated structure "more difficult" (pp. 4, 6).
- Pan-STARRS artefact mask is empirical (flux-ratio outliers), binary, with arbitrary thresholds (p. 5).
- Masking of nearby galaxies (SGA, MAG_LEDA < 16.5) removes those galaxies from the effective coverage - i.e. bright nearby galaxies are largely excluded from the effective area (the paper masks them to avoid spurious detections/shredded objects). A user studying nearby extended galaxies should NOT apply the effective-coverage mask blindly.
- Only stars with G_RP < 14 are masked for EXT bands; fainter stars are not masked in the effective coverage. For Euclid bands the polygons come from the MER bright-star product (see kuemmel); details of the polygon sizes are not given here.
- Masks do not describe ghosts, scattered light, satellite/asteroid trails, cosmic rays or other artefacts (not mentioned in the paper); NIR persistence is the only NIR artefact mask.
- Effective area requires data in ALL bands, including EXT, so Euclid-only users lose area where EXT data are missing.
- The paper's depth definition is for 2" apertures and point-like detection: not a surface-brightness limit.

## Implications for extended-galaxy photometry, 2-D modelling and low-surface-brightness work
- Direct use is limited: these are survey-level maps for cosmology. Useful for (a) quoting depth and PSF FWHM for a field or tile, (b) checking whether a target lies in a region of low coverage, high persistence, or masked bright-star area, (c) understanding why bright nearby galaxies and bright stars appear as holes in the effective coverage.
- For LSB work: depth maps are 5 sigma point-source depths (2" aperture); converting to surface-brightness limits requires your own RMS/area analysis using the mosaic RMS map and zero point ZP (the formula in Eq. 3 is a useful template: mag = ZP - 2.5 log10(5 RMS sqrt(A_aper/A_pix)); an analogous surface-brightness limit per arcsec2 uses A_aper = 1 arcsec2 and accounts for correlated noise). Per-pixel RMS is white-noise only and underestimates the noise on large scales.
- The IE zero point and RMS are in ADU units: converting ADU (per-pixel counts in the stacked image) to AB mag uses the mosaic ZP (as given in the MER mosaic header; exact keyword not given here), a convention consistent with Eq. 3. Cross-check with kuemmel/Q1 documentation for the keyword name.
- Bright-star mask radii for EXT bands follow the Eq. 1 polynomial of G_RP (evaluate it yourself; not tabulated in the paper), enlarged by 20%; for Euclid bands only the central lobe and spikes are masked. For stellar haloes/ICL near bright stars, the halo scattered light is NOT masked; you must build your own mask from Gaia (the empirical relation r*(G_RP) can serve as a guide).
- Sky emission maps (zodiacal light, Galactic extinction) are per-tile estimates from model prescriptions; the Galactic extinction map gives A in Euclid bands for correcting magnitudes and surface brightness (units mag), useful for low-Galactic-latitude targets. Zodiacal light indicates the strength of the sky background that MER subtracts.
- The random catalogues are only useful for statistical studies of number counts/clustering.

## Practical recommendations for users
- Use EFF_COV = 1 (object-level, MER-resolution) rather than HEALPix pixel lookups when you want to mimic the cosmology cut; but for extended nearby galaxies consider not applying it, because SGA galaxies with MAG_LEDA < 16.5 are masked on purpose.
- If you do use HEALPix masks, pick effective-coverage > 0.8 (keeps ~99% of the effective area).
- Look up depth, PSF FWHM, exposure time, Tile for your target positions via healpy (nested, nside=16384, ang2pix with nest=True).
- Check NIR persistence and NIR_PRMS around targets for the NISP photometry.
- Treat Pan-STARRS-i photometry within the PanStarrsArtefacts mask with caution.
- Use depth values (2" aperture, 5 sigma) as point-source depths only.

## Objects, fields and figures worth revisiting
- Tile 102015162: example of initial effective coverage mask at MER resolution with circular star masks, spikes and bleed trails (Fig. 2, p. 5); compare with the smeared HEALPix mask.
- Fig. 1 (p. 5): empirical star-mask radius and bleeding-trail width vs Gaia G_RP.
- Fig. 3 (p. 7): full-sky EWS masks; Table 2 (p. 8): per-band statistics; Fig. 5 (p. 9): noise vs integration time, depth and FWHM distributions.
- Fig. 6-7 (pp. 10-11), Tables B.1-B.3 (pp. 18-20): EDF-F, EDF-N, EDF-S masks and statistics.
- Appendix A (pp. 16-18): zoom-in on EWS Patch ID 4: tile index, angles, integration time, coverage, noise, depth, PSF, NIR_PRMS, persistence, extinction, zodiacal light, stellar maps.
- No named galaxies or coordinates; the SGA-2020 and OpenNGC catalogues are used for the extended-object masks.

## Cross-references
- Kuemmel et al. 2026 (MER): provides MerBksMosaic images, RMS maps, flags (bit mask definition), layering files, Gaia star polygons, DET_QUALITY_FLAG, FILLING_FACTOR, Table 5 fields.
- Aussel et al. 2026a (Q1) and 2026b (DR1 overview); Tereno et al. 2026 (DR1 survey, observed area, visits); Ruffenach et al. 2026 (processing); Corcho-Caballero et al. 2026 (EXT data); Radovich et al. 2026 (NIR astrometry, PRMS); Kubik et al. 2026 (NISP persistence); Scaramella et al. 2022 (Euclid survey, zodiacal light and extinction models); Hartley et al. 2026 (photo-z).
