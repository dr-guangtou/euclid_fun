---
title: "Euclid: Data Release 1 (DR1) - First NISP emission-line maps: Methodology, validation, and applications to galaxy evolution"
short_name: gabarra
first_author: Gabarra
series: A&A Special Issue DR1-Foundation (Nov 2026)
local_pdf: ~/Desktop/euclid/papers/gabarra.pdf
local_text: ~/Desktop/euclid/text/papers/gabarra.txt
topics: [emission-line maps, slitless spectroscopy, blue grism, GELSA, H-alpha, resolved star formation, mass-metallicity, COSMOS, drizzle, kinematics]
relevance_extended_galaxies: high   # for photometry / 2-D modelling / LSB of low-to-intermediate-z galaxies
---

# First NISP emission-line maps from the blue grism: GELSA method, validation, applications (Gabarra et al. 2026)

## TL;DR
Shows that NISP slitless data can be resampled onto the sky at a fixed observed wavelength to give continuum-subtracted H-alpha maps that act like narrow-band images, using the GELSA Python package (ELSA project) on SIR science frames. It is a method and software demonstration, not a released map catalogue: the maps are produced on demand as cutouts for chosen galaxies, here for galaxies at 0.4 < z < 0.9 in the 0.5 deg2 COSMOS performance-verification field with 116 blue-grism exposures. The effective resolution is set by the NISP PSF (EE50 = 0.265", FWHM ~0.53", 1.4-2.3 kpc radius at 0.4 < z < 1.8), and the quoted surface-brightness sensitivity is 2.0e-16 erg/s/cm2/arcsec2 at S/N = 7 for four exposures. Directly relevant to resolved studies of extended galaxies, with strong caveats about line blending, single-orientation continuum subtraction and contamination.

## Key facts and numbers
- NISP blue channel: 926-1366 nm, dispersion 1.24 nm/px, R = 440-900 for a 0.5" source; red channel 1206-1892 nm, 1.37 nm/px, R = 550-740; native sampling 0.3"/px (p. 1). EWS requirement: 3.5 sigma line flux 2e-16 erg/s/cm2 at 1.6 um for 0.5" source; EDS expected 5e-17 (red) and 6e-17 (blue) (p. 1-2).
- Data: Euclid performance-verification COSMOS field (PV-005), Nov 2023, 0.5 deg2; 116 blue-grism exposures x 549 s = 63 684 s (17.7 h) at a single dispersion orientation (constant roll), i.e. 29 observation sequences; plus 68 red-grism exposures in four orientations not used here (p. 2).
- Map construction: output on RA/Dec grid at 0.1"/px matched to the MER cutout; drizzle with pixel-shrink 0.5 and 100 sub-pixel drops (p. 3). The finer grid does not improve intrinsic resolution (p. 3).
- Resolution: median EE50 = 0.265" over 295 MER point sources (derived from Gaussian sigma of cross-dispersion traces, EE50 = sigma sqrt(2 ln 2) x 0.3"), consistent with diffraction scaling for the 1.2 m aperture and with Gillard et al. (p. 6-7). Equivalent Gaussian FWHM 0.53" = 2.8-4.6 kpc at 0.4 < z < 1.8, i.e. between ground IFUs (KROSS, KMOS3D: 5-6 kpc) and HST/WFC3 grism (~1 kpc) (p. 7). The YE image has EE50 = 0.22" (p. 14).
- Depth: from source injection (4 blue-grism exposures, 1152 synthetic Gaussian sources of intrinsic FWHM 0.1" and 0.5", H-alpha flux 5e-17 to 5e-15 erg/s/cm2, 0.4 < z < 0.9): mean H-alpha surface-brightness sensitivity (2.0 +/- 0.2)e-16 erg/s/cm2/arcsec2 at S/N = 7, averaged within the PSF-convolved half-light radius, <Sigma> = F/(2 pi R50_obs^2) (p. 5). Not a flux limit but a surface-brightness limit for four exposures; 116 exposures will go much deeper.
- Flux recovery for sources above the S/N = 7 threshold and YE > 19.9 (continuum fainter than 1e-17 erg/s/cm2/A): median fractional residual within ~5%; scaled MAD 14% (H-alpha), 20% ([NII]6584), 17% (ratio) for 0.1" sources and 24%, 21%, 12% for 0.5" sources (p. 5). Brighter continuum (YE < 19.9) increases scatter, especially for [NII] and the ratio.
- Radial profiles: recovered half-light radii agree with source-only stacks within ~10%; outer regions of faint sources limited by residual background (p. 6).
- Residual cross-dispersion offset after SIR per-detector correction ~0.3 px (0.1"), could be reduced with local star-based corrections (p. 6).
- Samples: 87 355 SPE sources in field; 32 235 with spe_z_prob > 0.999; 7644 at 0.4 < z < 0.9; 6060 with H-alpha S/N > 3.5; after additional line criterion 4954; 4533 matched to COSMOS2020 Classic (0.36" radius); 2987 star-forming galaxies after NUVrJ and clean photometry flags (FLAG_COMBINED = 0, lp_type = 0); 980 with GELSA S/N > 7 for both H-alpha and [NII]6584; 885 after rejecting width-bound fits for the mass-metallicity analysis; 2634 for radial stacks (p. 2, 11-13).
- Mass-metallicity relation from 2D deblending agrees with SPE 1D deblending (Fig. 13, p. 12-13), both slightly offset from Wuyts et al. 2014, likely a selection effect; N2 calibration 12 + log(O/H) = 8.90 + 0.57 log N2 (Pettini and Pagel 2004) (p. 12).
- Stacked H-alpha radial profiles: R50(Halpha)/R50(YE) = 1.27, 1.12, 1.11, 1.10 in four YE size bins (R50,YE 1.50-2.70, 2.70-3.23, 3.23-3.80, 3.80-7.28 kpc); mean 1.15; YE PSF-matched to H-alpha PSF with simple Gaussian matching (p. 14).

## Data products and data model
- Method versus product: the paper presents GELSA v3.1 (https://github.com/elsa-euclid/gelsa; Granett and Gabarra 2026) and calls the maps a "novel Euclid data product" (p. 7), but the maps are produced by user-run software as cutouts; the paper does not describe an archive table or released map catalogue. Treat them as a method, not a DR1 catalogue product (inference from the text).
- Inputs: intermediate DpdSirScienceFrame products from SIR (background-subtracted NISP grism exposures with non-linearity correction and bad-pixel masking), SIR astrometric, dispersion and flux-calibration solutions and DQ flags; MER mosaic cutouts and MER catalogue for astrometry, point-like sources, position angle and axis ratio; SPE catalogue for redshifts and 1D line fluxes (p. 2-3).
- Additional masks applied by GELSA: persistence mask (threshold 30 ADU) and zero-order masks (p. 3). Pixels with non-zero DQ, non-finite values or non-positive variance are excluded; variance maps are corrected by squared relative and absolute flux calibration factors and resampled with the same drizzle footprints; variances summed assuming independent exposures (p. 3-4).
- Output: signal and coverage/variance maps on a 0.1" RA/Dec grid at a chosen observed wavelength (user-defined central wavelength), analogous to narrow-band images. Fixed-wavelength maps are not monochromatic: neighbouring lines (H-alpha and [NII] doublet) appear as shifted copies along the dispersion direction (p. 3).
- External catalogues used: COSMOS2020 Classic (Weaver et al. 2022), Khostovan et al. 2026 COSMOS spectroscopic compilation (DR1.1; 0.4 < z < 0.9 and I_AB <= 22.5 for illustrative galaxies).

## Processing and methods
1. Start from SIR science frames; apply persistence mask (30 ADU) and zero-order masks (p. 3).
2. Resample dispersed images to RA/Dec at fixed observed wavelength using SIR astrometric, dispersion and flux solutions (p. 3). No prior detection needed; can be applied to larger areas (p. 3).
3. Drizzle all exposures to the 0.1" grid (pixel fraction 0.5, 100 drops) (p. 3).
4. Continuum subtraction (fast method requiring same dispersion direction in all exposures): after co-adding, rotate map so dispersion is along rows; per pixel estimate continuum as sigma-clipped median over 400 A (97 resampled pixels); mask ~41 A (10 px, ~1") either side of expected H-alpha, [NII]6549, [NII]6584 using the spectroscopic redshift; rotate back and subtract (p. 3, 11). Not possible in this form for multiple dispersion orientations (p. 3).
5. 2D fitting: smooth with sigma = 1 px; DAOStarFinder (2.3 sigma, FWHM 1 px) to locate H-alpha peak within 6 px of the expected position; fit three 2D Gaussians (H-alpha, [NII]6549, [NII]6584) with relative offsets fixed from redshift and dispersion direction, shared geometry, [NII]6549 = 1/3 of [NII]6584, widths initialised from YE morphology and allowed to vary by 0.65-2.0, centre free by +/-0.5 px, constant background (p. 11-12).
6. Clump finding: DAOStarFinder, FWHM 4.5 px, 3 sigma threshold; clump aperture fluxes compared with YE (p. 2, 7).
7. Radial profile: azimuthal average; radius from first bin beyond which background-subtracted profile stays below 10% of centre for three bins (p. 7). Stacking in physical 0.5 kpc/px grid after normalising by YE flux, masking [NII] rectangular regions aligned with dispersion (p. 13-14).

## Validation and performance
- Source-injection tests (Figs 2-4, p. 4-5) on real blue-grism frames, including detector noise, slitless contamination, persistence masking, cosmic rays; 43% of injections rejected because Gaussian width hit the upper bound (39% for 0.1", 47% for 0.5") (p. 5). Tests include only circular Gaussians; no bulge-disc, elongated or clumpy morphologies (p. 4-5).
- Astrometric/wavelength mapping check using IE vs H-alpha maps, stellar continua and SIR spectra (p. 6).
- PSF determination from 295 MER point sources (Fig. 5, p. 5-7).
- Comparison with SPE 1D: MZR consistency (Fig. 13); [NII]6584/H-alpha ratios from GELSA and SPE shown for individual examples (Fig. 12).
- Offsets between DAOStarFinder and WCS positions in Fig. 11 (p. 11).

## Known issues, caveats, limitations
- Sample and coverage: single field (0.5 deg2), blue grism only, single dispersion orientation, so analyses restricted to 0.4 < z < 0.9 (p. 14).
- Blending and non-monochromatic maps: H-alpha and [NII] images overlap along dispersion; with one orientation a [NII] counterpart can be confused with a genuine clump aligned with dispersion (p. 3, 9). Combining orientations naively is not allowed; model each orientation separately (p. 9).
- Kinematics degenerate with morphology: velocity gradients shift emission along dispersion (e.g. clump offsets +0.15" and -0.19" = +6.7 and -8.4 A, 407 km/s separation, v_rot sin i ~ 204 km/s for the z = 0.6959 galaxy), but offsets can also come from continuum/line morphology differences, astrometric, wavelength or redshift errors; opposite (180 deg) orientations needed to separate them (p. 7-9).
- 1D extraction pitfalls: spatial structure in the collapsed 1D spectrum can mimic [NII] lines and bias redshifts, fluxes and FWHM (p. 7). Redshift from SPE depends on the adopted source position because position and wavelength are coupled along dispersion; blended interacting systems in MER can give a displaced position (p. 9-11).
- Continuum residuals: bright galaxies (YE < 19.9) leave residuals that inflate [NII] and ratio scatter (p. 5).
- Spectral contamination from overlapping neighbours not explicitly modelled; crowded regions may retain neighbour lines (p. 14).
- Fit prior: YE-morphology prior (0.65-2.0 width factors) may bias against galaxies whose H-alpha is much more compact than YE (p. 12).
- Outer regions of faint sources limited by residual background (p. 6). No upper limit on recoverable angular extent has been established (p. 15).
- Residual cross-dispersion offset ~0.1" (p. 6). MZR selection requires detection of both lines, favouring higher [NII]/H-alpha at low mass (p. 13).
- PSF matching of YE to H-alpha is a simple Gaussian approximation; intrinsic PSF-corrected sizes deferred (p. 14).

## Implications for extended-galaxy photometry, 2-D modelling and low-surface-brightness work
- Resolved line emission: a ~0.5" FWHM H-alpha image for galaxies at 0.4 < z < 0.9 (blue grism; only EDS and PV fields have it), and with the red grism for z > 0.84 (not yet demonstrated, p. 14-15). Resolution is 2-3x poorer than the IE (0.16") image, so for sizes of a few kpc the maps resolve disc/bulge-scale structure (R50 of 1.5-7 kpc in the sample) but not small clumps; at 0.4 < z < 0.9 the PSF EE50 is ~1.4-2.3 kpc.
- For bulge-disc or Sersic work, YE (and IE/JE/HE) images should be PSF-matched to the 0.265" EE50 H-alpha PSF before comparing profiles; the paper does this with a simple Gaussian match (p. 14). Quantitative surface-brightness profile comparison with stacked H-alpha profiles: line emission is ~10-27% more extended than YE light in R50.
- Low surface brightness: the sensitivity of 2.0e-16 erg/s/cm2/arcsec2 at S/N = 7 (4 exposures) is a high surface-brightness limit; 116 exposures lower the noise but outer-disc profiles are floor-limited by residual background structure in the faint sources (p. 6). No LSB or tidal-feature claims are made.
- Spectroscopic redshift for extended galaxies is affected by morphology and by the position used for extraction (p. 9-11); the maps provide a cross-check by constructing H-alpha images at trial redshifts and requiring spatial alignment with IE/YE.
- Maps can also reject foreground/background neighbours and associate close companions at the same redshift (Fig. 9, p. 9-10), useful for interacting systems.
- Low-z (z < 0.4) is not covered: H-alpha is below the blue-grism range (926 nm / 656.46 nm gives z ~ 0.41) so low-z galaxies would need other lines ([SIII], Paschen, HeI), which are not yet mapped (future work lists H-beta, [OIII], [OII], Pa-beta; p. 15).

## Practical recommendations for users
- Do not expect a released emission-line map catalogue: use GELSA (v3.1 or later) on SIR science frames, MER cutouts and SPE redshifts.
- Use identical dispersion orientation when using the fast continuum subtraction; for multiple orientations, model each separately.
- Mask the predicted [NII] positions along dispersion before measuring H-alpha profiles; use the YE profile as a morphology prior but check for compact H-alpha.
- Use S/N > 7 on each line in 2D fits for line-ratio work; reject fits whose Gaussian widths hit the allowed bounds (excluded 9.7% in the MZR sample).
- Treat sources with YE < 19.9 with caution for [NII] and ratios.
- For redshift checks, compare maps at trial redshifts with direct images; consult MER position of blended systems.
- Apply local star-based cross-dispersion corrections if sub-0.1" astrometric registration is needed.

## Objects, fields and figures worth revisiting
All in COSMOS (PV-005), J2000, with adopted z (Table 1, p. 2):
- J100106.88+015815.4 (RA 10h01m06.88s, Dec +01d58m15.4s; = RA 150.2787, Dec +1.9710), z = 0.528, face-on spiral, Fig. 1 construction of the map.
- J095955.98+022847.1 (149.9833, +2.4798), z = 0.7043 (SPE), face-on galaxy with clumps, Fig. 6.
- J100059.32+022247.7 (150.2472, +2.3799), z = 0.6959, inclined spiral, three clumps, velocity gradient, Fig. 7.
- J100038.66+021643.3 (150.1611, +2.2787), z = 0.4267, compact galaxy showing H-alpha and [NII]6584 peaks separated by 0.64" (2.79 nm), Fig. 8.
- J095936.59+020647.9 (149.9025, +2.1133), z = 0.5366, galaxy pair, Fig. 9a-c; J100022.52+023014.2 (150.0938, +2.5039), z = 0.751, interacting system with foreground galaxy at z = 0.268 and PSF-like H-alpha source on the spiral arm, Fig. 9d-f.
- J100011.59+023530.1 (150.0483, +2.5917), z = 0.8003 (GELSA; SPE secondary 0.7942, primary 2.1590), interacting galaxy, Fig. 10.
- J100030.82+022510.0 (150.1284, +2.4195), z = 0.7405, deblending example, Fig. 12; J100004.73+015702.3 (150.0197, +1.9506), z = 0.4390, Fig. 14.
- (Decimal coordinates are converted from the sexagesimal values in the paper by the summariser.)
- Key figures/tables: Fig. 1 (p. 3) workflow; Figs 2-4 (p. 4-5) injection tests; Fig. 5 (p. 5) EE50 vs wavelength; Fig. 12 (p. 12) 2D deblending; Fig. 13 (p. 12) MZR; Fig. 15 (p. 13) stacked profiles; Table 1 (p. 2) targets.

## Cross-references
- Fumana et al. 2026 (SIR calibration; per-detector cross-dispersion corrections), Scodeggio et al. and Copin et al. 2026 (SIR), Le Brun et al. 2026 (SPE redshifts and line fluxes), Gillard et al. 2026 (NISP PSF/ground calibration), Jahnke et al. 2025 (NISP), Kuemmel et al. 2026 (MER), Polenta et al. 2026 (persistence), Aussel et al. 2026 (DR1 overview), Granett et al. (GELSA), Rigamonti et al. (multi-orientation maps), Bergamini et al. 2026 (arcs and multiple images using GELSA), Griggio et al. 2026 (datacube reconstruction from slitless data), Khostovan et al. 2026 (COSMOS redshifts).
