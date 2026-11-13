---
title: "Euclid Data Release 1 (DR1): Euclid Lens Identification Pipeline and Scientific Exploration (ECLIPSE) D: Photometric redshifts and the first census of strong lenses in the galaxy evolution framework"
short_name: nersesian
first_author: Nersesian
series: A&A Special Issue DR1-Foundation (Nov 2026)
local_pdf: ~/Desktop/euclid/papers/nersesian.pdf
local_text: ~/Desktop/euclid/text/papers/nersesian.txt
topics: [deblended photometry, Sersic, multiwavelength photometry, photometric redshift, Phosphoros, SED fitting, Prospector, stellar mass, size-mass relation, UVJ, massive early-type galaxies, DR1 MER mosaics, PSF FWHM, depths]
relevance_extended_galaxies: high
---

# ECLIPSE D: deblended photometry, photo-z and SED fits of DR1 strong lenses (Nersesian et al. 2026)

## TL;DR
The paper turns the ECLIPSE-C lens models into band-by-band deblended Sersic photometry for the foreground lens galaxies (VIS, NISP and ground-based UNIONS or DES), then derives photo-z with Phosphoros and stellar masses, SFRs, ages and metallicities with Prospector for 9538 DR1 lenses (plus 275 from Q1) (p. 2-9). The sample is massive and mostly quiescent (median log M* = 11.39 with Salpeter IMF, median z_phot = 0.68, 86-87% UVJ-quiescent) and follows the van der Wel quiescent size-mass relation (p. 9-11). For a group doing multi-band galaxy photometry this is the most directly relevant DR1 lensing paper: it documents the DR1 band depths and PSF FWHM, a fixed-structure multiband Sersic scheme, an empirical error calibration, and quantifies how blending biases photo-z and SED parameters.

## Key facts and numbers
- Sample: 15 072 DR1 grade A+B candidates plus 328 Q1 lenses (methodology development set) (p. 2). Quality cuts leave 9538 DR1 and 275 Q1 = 9813 lenses (Table 3, p. 9). 279 lenses have spectroscopic redshifts (DESI, OzDES, PRIMUS); 236 from the DR1 sample (p. 4).
- Results: z_phot range 0.13-1.98, DR1 median 0.68 (+0.33, -0.29), Q1 median 0.67 (+0.27, -0.24); stellar mass 1e10-1e12.1 Msun, median log M* = 11.39 (+0.29, -0.33), Salpeter IMF (abstract p. 1; p. 7). Median log SFR = 0.15; median log sSFR = -11.3; mass-weighted age 4.4 Gyr; log Z/Zsun = -0.06; median R_eff = 5.7 kpc; median Einstein radius R_E = 6.4 kpc (p. 9).
- Photo-z accuracy vs 279 spectra with the adopted luminosity prior: NMAD = 0.037, bias 0.032, sigma 0.043, outlier fraction 4.3% (outlier if |dz| > 0.15 (1+z)); no prior NMAD 0.046 and 4.7% outliers; volume prior NMAD 0.051 and 7.5% outliers (Fig. 3, p. 6-7). Median zPDF uncertainty sigma_z/(1+z) = 0.046 (p. 7).
- Stellar mass 1-sigma typical uncertainty 0.08 dex; tau_dust,2 uncertainty 0.18; mass-weighted age 0.7 Gyr (p. 21-22 Appendix C).
- Typical H_E S/N above 100; no S/N cut (p. 9).
- Table 1 (p. 3), MER mosaics, DR1 EWS 10-sigma depths (total flux in I_E, 2 x FWHM aperture in other bands) and median PSF FWHM measured on the MER PSF stamps at the lens positions: I_E 24.8 mag, 0.20 arcsec; Y_E 23.2, 0.49; J_E 23.3, 0.51; H_E 23.3, 0.56; UNIONS u (CFIS) 23.2, 1.02; g (HSC) 24.5, 0.96; r (CFIS) 24.0, 0.83; i (Pan-STARRS) 23.6, 1.29; z (HSC) 23.0, 0.77; DES g 24.7, 1.26; r 24.3, 1.13; i 23.8, 1.05; z 23.0, 1.01. Q1 5-sigma depths for comparison: I_E 26.0, Y_E 23.8, J_E 24.0, H_E 24.0 (p. 3-4). Depth range quoted 23.7-26.0 (5 sigma) and 23.0-24.8 (10 sigma) (p. 4).
- Inter-band astrometric shifts fitted in the multiband step: median offsets from I_E of 18, 20, 26 mas in Y_E, J_E, H_E and 86, 65, 56, 50 mas in DES g, r, i, z (p. 5).
- Size-mass: median offset from van der Wel et al. 2014 quiescent relation 0.04 dex (max 0.2 dex per mass bin) at 0.5 < z < 1 (p. 11). Only 4.7% of lenses lie within 0.3 dex of the Leja et al. 2022 star-forming main sequence; median 1.1 dex below it (p. 10).
- Einstein radius versus mass: Spearman 0.61, Pearson 0.57, partial correlation with R_eff fixed 0.47; at fixed M*, R_E nearly independent of R_eff (partial 0.13) (p. 11-12). SLACS lenses have 0.3 dex smaller R_E at fixed mass (p. 11).
- About 9% of lenses have Sersic index near the prior upper limit (n > 9.5) (p. 13).

## Data products and data model
- Imaging: MER mosaics of VIS, NISP, and EXT (UNIONS in the north: HSC g and z, CFIS u and r, Pan-STARRS i; DES g, r, i, z in the south), all resampled to a common 0.1 arcsec/pixel grid; cutouts of 10 x 10 arcsec (100 x 100 pixels) as a datacube of background-subtracted images in all filters, RMS noise maps and per-band PSFs (p. 2-3). PSF is tile- and position-dependent (MER PSF stamps; Romelli et al. 2026) (p. 3). Data via the ESA Science Archive Service and ESA Datalabs.
- Zero-point multiplicative corrections (ZPC) were needed for Q1 photometry (1-5%, Pan-STARRS i about 9%) but are not needed for DR1 because of improved calibration and homogenisation (p. 4).
- MER catalogue columns used: DET_QUALITY_FLAG (cut at < 4), 4 x FWHM aperture flux uncertainties from A-PHOT; OU-PHZ catalogue column PHZ_FLAGS (cut at 0, entries without OU-PHZ kept) (p. 6, 8).
- Released catalogue (Zenodo, record 19654904; same ECLIPSE record as ECLIPSE-A): z_phot (median of zPDF, Phosphoros), spectroscopic z where available, M*, SFR, sSFR, mass- and light-weighted ages, metallicity, dust optical depths, R_eff (kpc, circularised), R_E (kpc), rest-frame colours (U-V, V-J), deblended per-band lens photometry (p. 7-9, 16).
- Prospector model grid: 12 free parameters (Table 2, p. 8): log M* uniform 8-12.5; Z* uniform 0.1-1.6 Zsun in linear space; seven SFR ratios (continuity prior, Student t, sigma 0.3, nu 2) over eight bins ([0, 30], [30, 100] Myr, up to 0.9 t_H, last bin 0.9-1 t_H); diffuse and birth-cloud dust optical depth; dust slope n_a in [-1, 0.4] (Kriek and Conroy UV bump). FSPS with MILES and MIST, Salpeter IMF, dynesty sampler; Charlot and Fall two-component dust (p. 7-8).

## Processing and methods
1. Lens model from ECLIPSE-C in I_E: MGE lens and source light, SIE plus shear, ML segmentation of lens, source and contaminants. Note this paper says the source MGE has one set of 30 Gaussians, whereas ECLIPSE-C says 20 (p. 4).
2. I_E Sersic fit: single elliptical Sersic for lens and source, mass fixed; free centre, ellipticity, n (uniform prior 0.5-10) and R_eff, where R_eff = sqrt(a b) is the circularised effective radius (p. 5).
3. Other bands (Euclid NISP and ground EXT): same I_E segmentation and mask, Sersic n, R_eff and shape fixed to I_E values; only the flux normalisation per band and a (y, x) astrometric shift are free (p. 5).
4. Lens flux = unconvolved Sersic model summed inside the circular lens-modelling mask (radius set by the lensed-source extent plus a buffer) (p. 5). Total flux used for SED fits; the lens-model magnification is lensed over intrinsic source flux.
5. Aperture photometry: unconvolved lens models are convolved with the PSF of the lowest-resolution band (DES g in the south, Pan-STARRS i in the north), then measured in circular apertures of integer multiples of that band's FWHM (as in MER); no PSF-matching kernels are required (p. 4-6). 4 x FWHM aperture used for photo-z (Appendix A: NMAD 0.030 for 4 x FWHM vs 0.051 for 1 x FWHM and 0.041 for total, N = 73) (p. 21).
6. Uncertainties: MER A-PHOT 4 x FWHM errors, plus empirical Sersic-model error (control sample of 500 non-lens galaxies matched to lens z and photometry, drawn from about 83 000 spectroscopic galaxies in Q1; typical scatter 0.07 mag about 6% flux, magnitude- and band-dependent; HSC, MegaCam and Pan-STARRS bands borrow the nearest DECam calibration), plus 2% systematic floor in every band (beta = 0.02) (p. 6-7, 22).
7. Photo-z with Phosphoros: grid z = 0.1-2.0 step 0.01; SED library as in Tucci et al. 2026 (33 COSMOS-like templates from Ilbert et al. 2009, Polletta and Bruzual and Charlot models, nebular lines at 200 km/s); E(B-V) 0-0.5 (young) and 0-0.2 (old); SMC and modified Calzetti laws; IGM of Inoue et al. 2014; Galactic extinction from Gordon et al. 2023. Optional volume prior and luminosity prior (-24 < M_r < 0). Fiducial: luminosity prior, median of zPDF (p. 6-7).
8. SED fitting with Prospector at fixed z (spectroscopic if available, else photometric) on total fluxes (p. 7).
9. Quality cuts (p. 8-9, Table 3): DET_QUALITY_FLAG < 4; successful lens model (at least 75% SC votes; No Consensus retained); detected in at least six bands; PHZ_FLAGS = 0; 70% credible interval of zPDF narrower than 1; Prospector fit not flagged (chi2 p > 0.01, no band deviates more than 5 sigma); log M* >= 10. Counts DR1: 15 072 total, 14 281 with deblended photometry, 13 766, 11 500, 10 683, 10 594, 10 557, 9700, 9538 after each successive cut.

## Validation and performance
- Photo-z versus spectroscopy (Fig. 3, p. 6): described above. Deblending improves photo-z mostly for systems with a bright lensed source (source/lens I_E flux ratio high); systems with faint sources lie near the one-to-one line with OU-PHZ (Fig. 4, p. 7).
- Aperture choice (Appendix A, Fig. A.1, p. 21): 4 x FWHM best; OU-PHZ (Kron I_E plus 2 x FWHM) has lower outlier fraction (2.7%) but worse bias, scatter, NMAD on N = 73.
- Deblended-model magnitudes versus MER catalogue magnitudes (4 x FWHM): agreement good, model magnitudes systematically fainter than MER because the lensed source is removed; scatter larger in faint ground-based u, g, r bands (Fig. A.2, p. 21).
- Prospector versus Euclid PHZ-PF/NNPZ (Appendix D, p. 23-24): with identical photometry and redshift Prospector masses are 0.23 dex higher and SFRs 0.55 dex lower; NNPZ gives broader ages and unrealistically high SFRs (> 100 Msun/yr) for some lenses; blended versus deblended photometry changes Prospector masses by 0.09 dex and SFRs by 0.7 dex (blending raises SFR through blue source light).
- Posterior degeneracies: age-dust (median Spearman -0.47), M*-age (0.72), sSFR-dust (0.50) (p. 22).
- UVJ: 87% quiescent by UVJ (Muzzin et al. 2013) in Sect. 5.3 (86% in the summary, p. 14); 72% of lenses with log D > -1.3 lie inside the quiescent region, 38% of those in the quiescent box are transitioning; 91% of UVJ-quiescent lenses have n > 2.5 (p. 9-10).

## Known issues, caveats, limitations
- Not complete or random: I_E < 23 or H_E < 22.5 cut, S/N and R_E dependence of lens finding, lens-source colour contrast, model-success requirement, and the paper's own cuts; selection effects are not corrected (p. 13).
- Structure is fixed to I_E (single Sersic with fixed n and R_eff) in all bands; real R_eff varies with wavelength because of colour gradients and dust, so fluxes and colours can be biased (p. 13). Authors note n is only weakly wavelength dependent but R_eff clearly depends on wavelength.
- Total flux is within the lens-modelling circular mask; for galaxies extending beyond (the about 9% with n > 9.5) it is a lower limit and stellar masses may be underestimated (p. 13). The 4 x FWHM aperture usually lies inside the mask, so photo-z are unaffected.
- Single-Sersic formal errors are unrealistically small, hence the empirical calibration (p. 6).
- Disc-dominated lenses: the lens model does not treat internal dust attenuation; effect on magnification, R_E and enclosed mass unquantified (p. 13).
- Stellar mass depends on IMF and SED code: Chabrier or Kroupa would lower masses by about 0.2-0.25 dex (p. 7); Prospector gives masses 0.23 dex above NNPZ (p. 11). Metallicity posteriors broad, peaking near the prior upper limit (p. 22).
- Source galaxy photometry, photo-z and properties are not provided (p. 2).
- Cluster-scale, multi-deflector and group-scale lenses excluded (p. 2).
- Stellar-population templates are calibrated on general galaxies and may not suit extreme massive lenses (p. 13).

## Implications for extended-galaxy photometry, 2-D modelling and low-surface-brightness work
- Directly shows how a single-component, I_E-anchored Sersic model can be propagated to NISP and ground bands by freeing only flux and an astrometric shift; for ellipticals colour gradients are argued small, but for discs and edge-on systems this assumption fails and the recovered colours should be treated with care (p. 13, 22).
- The paper quantifies the blending penalty on catalogue photometry: MER magnitudes within a 4 x FWHM aperture are brighter than model-based lens magnitudes when a lensed source is present, with consequences of 0.09 dex in mass and 0.7 dex in SFR (p. 21, 23). Analogous contamination applies to any galaxy with a bright companion or HII-region-rich disc.
- Gives realistic noise floors for Euclid photometry: an extra 0.07 mag (about 6%) Sersic-modelling scatter plus 2% systematic floor (p. 6, 22). Use as a guide for error budgets of model-based photometry.
- The DR1 per-band median PSF FWHM (I_E 0.20 arcsec at the lens positions, versus 0.16 quoted as nominal) is the measured value on MER PSF stamps; use this when planning PSF-matched or aperture photometry (p. 3).
- Size-mass relation check: I_E sizes were corrected to rest-frame 5000 A using van der Wel et al. 2014 colour gradients before comparison, a practical recipe for comparing Euclid sizes with CANDELS (p. 11).
- Ground-based bands have lower resolution, so deblending is poorer in u, g, r; model-based photometry inherits the PSF of the worst-resolution band.
- No LSB, halo or ICL content; photometry is confined to a 10 arcsec cutout and a lens-mask-limited total flux.

## Practical recommendations for users
- For massive early-type galaxy photometry in DR1 use the 4 x FWHM aperture on the lowest-resolution band PSF for photo-z, and total (mask-limited) model flux for stellar mass; treat n > 9.5 galaxies' masses as lower limits.
- Apply the cuts DET_QUALITY_FLAG < 4, PHZ_FLAGS = 0, at least six detected bands, log M* >= 10 as in Table 3 when building clean samples.
- Add a 2% flux error floor and an empirical model error (about 0.07 mag) to model-based photometry.
- Fix redshift to spectroscopic values where available (DESI DR1) and use the luminosity prior in Phosphoros for lens-like samples; avoid the volume prior.
- State the IMF (Salpeter here) when comparing to other mass estimates; shift by -0.2 to -0.25 dex for Chabrier or Kroupa.
- DR1 does not need extra ZPC factors (Q1 did).

## Objects, fields and figures worth revisiting
- No named lens systems or coordinates are given in this paper. Fig. 2 (p. 5) shows one example multiwavelength fit (anonymous DR1 lens) across DES griz and Euclid I_E, Y_E, J_E, H_E, with data, lens model, lens-subtracted and source columns; Fig. C.1 (p. 22) shows posteriors for three random lenses at z_phot = 0.44, 0.67, 0.98.
- Key tables and figures: Table 1 depths and PSF FWHM (p. 3); Fig. 3 photo-z versus spec (p. 6); Fig. 4 deblended versus OU-PHZ photo-z (p. 7); Table 2 Prospector priors (p. 8); Table 3 quality cuts (p. 9); Fig. 5 mass-redshift (p. 9); Fig. 6 property distributions (p. 10); Fig. 7 UVJ (p. 10); Fig. 8 SFMS and size-mass (p. 11); Fig. 9 R_E versus M* (p. 12); Fig. A.1-A.2 aperture and MER-versus-model photometry (p. 21); Fig. D.1-D.2 Prospector versus NNPZ (p. 23-24).
- For showcase massive early-type targets, use the coordinates in the lines.md and nightingale.md notes.

## Cross-references
- ECLIPSE-A (Lines et al.), ECLIPSE-B (Holloway et al.), ECLIPSE-C (Nightingale et al.).
- MER catalogue and PSF papers (Kummel et al. 2026; Romelli et al. 2026), Euclid photo-z paper (Tucci et al. 2026) and OU-PHZ catalogue, Enia et al. 2026 (Euclid star-forming main sequence), Nersesian et al. 2026 (Prospector setup on Euclid), spectroscopic-redshift compilation (Saulder et al., in prep.), DESI vetting (Storfer et al., in prep.), Euclid VIS (Cropper et al. 2025) and NISP (Jahnke et al. 2025) instrument papers, Martorano et al. 2023 (wavelength dependence of Sersic parameters).
