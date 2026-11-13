---
title: "Euclid Data Release 1 (DR1): Photometric-redshift pipeline overview and validation"
short_name: hartley
first_author: Hartley
series: A&A Special Issue DR1-Foundation (Nov 2026)
local_pdf: ~/Desktop/euclid/papers/hartley.pdf
local_text: ~/Desktop/euclid/text/papers/hartley.txt
topics: [photo-z, NNPZ, Phosphoros, PHZ processing function, zPDF, COSMOS reference sample, star/galaxy classification, UNIF photometry, PSF SEDs, DR1-Foundation, validation]
relevance_extended_galaxies: medium
---

# Photo-z pipeline (PHZ PF) overview and validation (Hartley et al. 2026)

## TL;DR
Describes how the PHZ processing function produces DR1 photo-z (now with the nearest-neighbour code NNPZ, trained on a COSMOS-based reference sample, replacing Phosphoros template fitting used in Q1), object classification, unified photometry and SEDs for PSF modelling, and validates them against spectroscopy. At the nominal EWS depth (IE < 24.5) point-estimate quality is about twice outside the mission requirement (outliers ~20%, NMAD 0.07-0.08) but at IE < 24 it nearly meets it (outliers 7-13%, NMAD 0.04-0.054). For a low-z, bright/extended-galaxy group the key point is a self-declared weakness: the reference sample has very few z < 0.2 and very massive galaxies, so the brightest, nearest galaxies are the worst-served (p. 19); the paper gives no performance table binned in redshift. Photo-z inputs are PSF-matched 2FWHM aperture fluxes (not total/model fluxes), so these products do not substitute for dedicated photometry of extended galaxies.

## Key facts and numbers
- DR1 covers ~1900 deg2 (EWS at Q1-like depth; EDFs same area as Q1 but deeper; calibration fields incl. EAFs); 8960 MER tiles in the EWS area, 93.6% valid through the whole photometric chain, ~95% of nominal area usable (p. 1, 20).
- Requirements (cosmology): sigma(dz) < 0.05, outlier fraction < 10% (|dz| > 0.15, dz = (zphot - zspec)/(1+zspec)); mean-z accuracy per tomographic bin 0.002 (p. 2). Abstract: current performance short by "40% in scatter and factor 2 in outliers" at IE < 24.5.
- Depths are 10 sigma in 2" apertures; cosmology: Planck 2016 (H0 = 67.74, Om = 0.3089) (p. 2).
- External bands: south = DECam (g r i z); north = UNIONS = CFHT u,r (CFIS), HSC g,z (WHIGS, WISHES), Pan-STARRS i. u band present only over about half of the north (p. 5, 19). Deep tiles may have DECam, HSC (g, r, r2, i, i2, z) or both (p. 7). Euclid bands IE, YE, JE, HE.
- NNPZ settings: 30 neighbours; median effective neighbour number 24.64 for IE < 24.5, dropping sharply for IE < 23 (p. 5-6). Amplitude prior log-normal with mu = 0.04, sigma = 0.2, clipped at p(A) < 1e-10 (about +/-1.5 mag amplitude range) (p. 4, 6). Neighbours with weight < 1e-3 -> PHZ_FLAGS = 1 (p. 4). zPDFs smoothed with Gaussian sigma_z = 0.02 (p. 6).
- Intended 2% systematic flux error was interpreted as a variance (config error), so effective systematic error is far smaller (p. 6); in deep pipeline no systematic error was applied at all (p. 8, 16).
- Reference sample: COSMOS only (Euclid ~1/3 of final depth, ~3x EWS S/N; CDFS observed to full depth but no EXT catalogue, so unused). COSMOS2020 CLASSIC catalogue, 723 896 objects after FLAG_COMBINED cut; truth photo-z from Phosphoros with 33 Ilbert+09 templates (192 SEDs incl. interpolation and two emission-line strengths), E(B-V) up to 0.51 in 0.03 steps, 5 dust laws, Meiksin IGM, zmax = 10; photometric errors inflated by 20%; weak volume prior (effectiveness 0.3) (p. 8-9). Wide reference cut at union IE < 26 or HE < 25 (p. 9).
- Redshift-prior weighting of reference objects (weights truncated to 0.25-4), computed in HE-magnitude bins using 0.2-wide coarse z bins and 0.025 fine bins; COSMOS structures at z ~0.35, 0.7, 0.9 are the main targets (p. 10).
- Augmentation (<1% of reference size) of z < 0.1 objects with 16 < i < 18 via boosted SED amplitudes to cover missing bright low-z galaxies (p. 10).
- QSO catalogue definition: not a star (default threshold) and MUMAX_MINUS_MAG < -2.6 (p. 5). PSF-star cut: S/N > 50 and MUMAX_MINUS_MAG <= -1.5 loose extended rejection (p. 7).
- ~1/4 of EWS objects are NIR-detected only (p. 7).

## Data products and data model
Table 1 (p. 3); archive table names get suffix _wide (EWS), _deep (EDS incl. AUX and medium-deep), _deep_visits (EWS-like visits of the deep fields).
- phz_photoz (container dpdPhzPfOutputCatalog): NNPZ photo-z, full zPDF and summary stats. Point-estimate columns named in text: PHZ_MEDIAN (median of zPDF; the one used for validation), PHZ_MODE_1 (mean of the most probable zPDF peak after peak decomposition), PHZ_MODE_2 (mean of the zPDF of the single closest neighbour, ML-like). Neither "mode" is the true mode (p. 6). Also central percentile ranges, PHZ_FLAGS, PHOTOMETRIC_SYSTEM (number of missing bands) (p. 5).
- phz_classification (dpdPhzPfOutputForL3; summary also in dpdPhzPfOutputCatalog): two probabilistic random forests (star, galaxy), thresholds stored in the catalogue; consolidated column PHZ_CLASSIFICATION (object may be accepted as one class, both, or neither). Names of missing bands are in this catalogue (p. 5).
- phz_galaxy_sed, phz_star_sed (dpdPhzPfOutputCatalog): SEDs at 10 nm spacing, 450-1000 nm (55 wavelengths), uJy; no uncertainties in DR1 (p. 7, 11).
- Unified photometry (UNIF): standardised to DECam filter set; UNIF fluxes for both north and south sets; reddening corrected; galaxies only (do not use for stars); no uncertainty propagation (p. 6-7).
- phz_physical_parameters (dpdPhzPfOutputForL3): stellar mass, SFR etc.; details in the companion paper (see enia.md). Represented via 50 samples per reference object -> 1500 weighted samples per target; neighbour IDs, distance weights, scaling factors stored; statistics median, closest-neighbour value, 15.9-84.1 percentiles. Deep tiles additionally output a table of 50 posterior samples (ordered across quantities) (p. 6, 8).
- phz_qso_physical_parameters, phz_star_template, phz_nir_physical_parameters (Phosphoros, Q1-like): QSO+host (Salvato+09) fits z <= 6, step 0.05, SMC reddening E(B-V) <= 0.04; star fits to Serrano+24 synthetic SEDs; NIR-detected sources z grid to 10 (EWS) / 12 (deep), with integrated P(z > 6) provided (p. 7-8).
- DpdBinMeanRedshift (calibrated n(z), SOM-based, bin width dz = 0.01): NOT part of DR1-Foundation (p. 3, 8).
- Zero-point offset table: FITS table in second extension of the output file, star-based, computed but NOT applied (p. 27).
- Input photometry (all PHZ products): MER final catalogue 2FWHM_APER fluxes (circular aperture of diameter 2 x FWHM of worst-PSF image), scaled to pseudo-total with FLUX_DETECTION_TOTAL (Kron-like); GAL_EBV (Planck map) for reddening (p. 5, 7).

## Processing and methods
1. Pre-processing: identify photometric system (DECam vs UNIONS), missing bands; kNN (15 neighbours) imputation of missing bands for classification features, after SED-dependent Galactic reddening correction (p. 5).
2. Classification: two pRFs on asinh-magnitude colours; deep tiles use max 62 colours (HSC generations combined by inverse variance; same-type cross-instrument colours dropped) (p. 5, 8).
3. Photo-z: NNPZ with chi2 (Mahalanobis) distance, log-normal amplitude prior, Galactic reddening forward-modelled on the fly per reference object; filter-variation across the field of view is NOT corrected in DR1 (p. 3-4).
4. UNIF photometry from neighbour flux ratios (Eqs. 2-3), SEDs from medium-band-bracketed template-assisted interpolation regularised toward the best-fit template at fixed S/N = 3 (galaxies), Gaia XP spectra + models (stars) (p. 6, 11).
5. Validation reports per tile with pass / dubious / fail gates (MER input depth and zero points, classification vs reference, photo-z vs COSMOS reference distributions, catalogue content) (p. 11-12).
6. Variant runs (north only): (a) without u band, to give a homogeneous north; (b) without u and Pan-STARRS i because of residual artefacts in the i-band coadds (no outlier rejection in the mosaics). Not published in DR1-Foundation; used by LE3 products (p. 19-20).

## Validation and performance
Truth = compiled spectroscopic redshifts (Saulder et al. in prep.), median of acceptable measurements, stars and QSOs removed, spurious and masked sources removed, point sources removed for IE-limited samples. Spec-z samples are magnitude-weighted to mimic flux-limited samples. Spectroscopy is a lower-limit test (some wrong spec-z, esp. DESI/PRIMUS) (p. 13-14).

Table 2, EWS, point estimate = PHZ_MEDIAN (p. 14). Columns: IE < 24.5 (EWS-like pass of EDF-F, and COSMOS EWS-like with COSMOS2020 photo-z as truth); IE < 24 and HE samples split into north with u / north without u / south.
- 17 < IE < 24.5 (EWS spec-z): outliers 20.16%, NMAD 0.072, sigma68 0.094, median bias -0.001, mean bias -0.064; zPDF outliers 5.41%, KL 0.014 nats. COSMOS: outliers 21.75%, NMAD 0.080, sigma68 0.106.
- 17 < IE < 24 (N w/u, N w/o u, S): outliers 13.10%, 18.53%, 12.50%; NMAD 0.054, 0.066, 0.054; sigma68 0.068, 0.090, 0.065; median bias -0.004, 0.002, 0.002. The u band removes ~5 points of outliers and ~20% of scatter in the north.
- 17 < HE < 22 (N w/u, N w/o u, S): outliers 7.12%, 9.07%, 7.61%; NMAD 0.038, 0.044, 0.039; sigma68 0.043, 0.050, 0.044; zPDF KL 0.009, 0.0421, 0.007.
- 22 < HE < 23.5: outliers 19.15%, 28.55%, 19.13%; NMAD 0.068, 0.098, 0.076.
- With outliers removed sigma68 is ~0.037-0.06; biases ~0.00-0.006. Gaussian sigma = 0.1 alone would give 13% outliers, so true catastrophic failures are likely moderate (p. 15).
- zPDF calibration: PIT is broadly flat for EWS, with Frac68 near 0.68 at all IE magnitudes (weak magnitude dependence) (Fig. 6, 7, p. 15-16); worst case is north without u (KL 0.075 at IE < 24; 0.107 for 22 < HE < 23.5).
- Improvements over Q1: scatter at matched conditions lower than Q1, and a group of outliers at zspec ~0.6, zphot ~0.2 largely removed thanks to the implicit population prior of NNPZ (p. 15).
- Table 3 (deep, unweighted, HE < 25.5; p. 15): EDF-N 28 105 spectra, outliers 4.14%, NMAD 0.033, sigma68 0.037; EDF-F 34 018, 6.82%, 0.035, 0.040; AUX (COSMOS + CDFS) 44 344, 4.02%, NMAD 0.018, sigma68 0.022. These match CANDELS/DES-DF/UDS (NMAD 0.02-0.03). Deep zPDFs are under-dispersed (PDF outliers 14.6-17.5%; KL 0.05-0.09) because of the missing systematic error (p. 16).
- Low-z specifics: the paper does NOT tabulate metrics versus redshift; Fig. 5 / 8 are zphot-zspec scatter plots only. Low-z/bright limitation described qualitatively in Sect. 5.1 (below).
- Stellar SEDs vs Gaia XP: fractional mean-wavelength bias in the south mostly 1.5e-4 to 5.7e-4 (requirement 5e-4); north up to -2.4e-3 for red low-reddening stars (Table 4, p. 18). Galaxy SEDs vs MUSYC medium bands (CDFS, EWS-like EDF-F): 3-sigma-clipped mean wavelength bias 2.0e-3 to 5.0e-3 across 6 bins in 0.2 < z < 2.5, worsening with z, ~10x the end-of-mission requirement; ~7% outliers at the edge of the MUSYC area (p. 18).
- Classification vs DESI in EDF-N (29 436 galaxies, 3121 stars, 2103 QSOs): 93% of DESI stars (2894) pass the strict PSF-star threshold; all but 49 (0.2%) of DESI galaxies classified as galaxies (58 also accepted as stars); 99% (1678/1689) of compact DESI QSOs are "not star"; 20% of DESI QSOs are not compact in Euclid so excluded from the QSO table (p. 19). Not formal purity/completeness since DESI is brighter.
- Zero points (Appendix A): star-based per-tile band offsets stable in the south; gradient across the south repeated in every band; outline of early data taken before first ice decontamination visible (IE passband differs, not modelled) (p. 27).

## Known issues, caveats, limitations
- Reference sample is COSMOS-only (2 deg2): very few z < 0.2 galaxies, very massive galaxies at z < 0.4, and other rare classes; NNPZ disfavours them. Augmentation and explicit prior only partly fix this: redshifts are "mostly reasonable" but stellar masses and other amplitude-dependent properties are biased low for these galaxies (p. 19). Directly relevant to bright, nearby, extended galaxies.
- Amplitude prior limits the SED rescaling to +/-1.5 mag, so very bright objects cannot be matched to fainter references (p. 10, 19).
- Redshift focussing: point estimates cluster at preferred values, some coinciding with COSMOS structures (z ~0.35) (p. 19). Use the full zPDF or PHZ_MEDIAN with care for narrow z slices.
- Configuration error in the EWS: systematic flux error interpreted as variance (p. 6); in deep fields, no systematic error -> over-confident zPDFs and ~15% outliers by the "truth outside PDF" definition (p. 16-17).
- No filter-bandpass-variation correction across the field of view (to come in DR2) (p. 3, 6).
- Uncertainties not provided for UNIF photometry and SEDs (p. 6-7).
- UNIF and galaxy SED products are valid for galaxies only, not stars (p. 7).
- u-band only in half the north; Pan-STARRS i-band mosaics have residual artefacts (Healpix map of affected areas in Odier et al. 2026) (p. 19-20).
- Invalid tiles: ~1% of area lost to tiles that are tiny or highly incomplete; 0.5% of tiles fail PHZ-specific tests (mostly star-classification mismatches, or reference-distribution or zero-point (up to 0.5 mag) anomalies) (p. 12-13). EXT/MER-invalidated tiles are flagged in Fig. 3.
- Stellar SED reference was built from an earlier MER release and a few PSF fields; north stellar SEDs ~2x the requirement (p. 17-18).
- Classification thresholds are tuned for cosmology (complete galaxies, pure stars at S/N > 50); users should set their own (p. 5).
- Spec-z truth contains an unknown fraction of wrong redshifts and is not flux-limited, so metrics depend on the weighting (p. 13-14).

## Implications for extended-galaxy photometry, 2-D modelling and low-surface-brightness work
- Not a photometry paper: it uses MER 2FWHM_APER fluxes (PSF-homogenised aperture), scaled to FLUX_DETECTION_TOTAL. Colour-based quantities (photo-z, UNIF) are therefore aperture-colour based and are not appropriate as total-galaxy colours of large, nearby galaxies with colour gradients. No LSB, sky-subtraction or halo content.
- For bright (HE < 22) and low-z extended targets, NNPZ is the weakest part of parameter space (few reference analogues, amplitude prior clip, low-z population missing). Photo-z for nearby large galaxies may be adequate in redshift but ought to be cross-checked; where spec-z exist (e.g. SDSS/DESI/GAMA) prefer them for rest-frame quantities.
- Stellar masses/SFR from this pipeline are biased low for the most massive and the lowest-z galaxies; if you use mass-dependent selections or scale radii to physical kpc, propagate the possible systematic offset.
- The classification thresholds favour galaxy completeness; for large resolved galaxies with bright nuclei or foreground-star confusion check PHZ_CLASSIFICATION against MUMAX_MINUS_MAG and the MER point-like probability. MUMAX_MINUS_MAG < -2.6 is the adopted compactness cut.
- Masks: PhotoZ visibility mask (VMPZ; Odier et al. 2026) is the recommended footprint definition (see Enia). Pan-STARRS i-band artefact map matters if you want ground-based colours in the north.
- Useful reference values: HE 17-22 galaxies reach NMAD ~0.04 with ~7-9% outliers, i.e. the bright sample is much better than the faint ones, but numbers are dominated by z ~0.3-1 galaxies; no explicit z < 0.5 statistic.

## Practical recommendations for users
- Use PHZ_MEDIAN as the default point estimate; avoid PHZ_MODE_1/2 names as if they were true modes (p. 6). Use the zPDF for any z-sensitive analysis.
- Check PHZ_FLAGS (non-zero = no neighbour with weight > 1e-3), PHOTOMETRIC_SYSTEM (missing bands) and PHZ_CLASSIFICATION; pick your own class thresholds.
- Prefer IE < 24 (or HE < 22) samples when you need the stated quality; expect ~20% outliers at IE < 24.5.
- Treat northern tiles without u band as noticeably worse (outliers +5 pts, scatter +20%, worse zPDF calibration).
- Do not use deep-field zPDFs naively: widen them or allow ~15% outliers (DR2 will fix).
- Do not use UNIF photometry or galaxy SED tables for stars.
- Do not rely on the zero-point offsets stored in extension 2 as calibration; they are diagnostics only.
- For low-z (z < 0.2) or very massive galaxies cross-check PHZ stellar masses and redshifts with spectroscopy.
- Use tile-validation status (Fig. 3, EXT/MER invalidation) when assembling samples.

## Objects, fields and figures worth revisiting
- Fields (no coordinates given in the paper): COSMOS (2 deg2, EAF and reference sample; E(B-V) ~0.017; strong structures z ~0.35, 0.7, 0.9), CDFS (0.5 deg2 EAF, one pointing), AEGIS (colour-gradient calibration field, no EXT data), EDF-N, EDF-F (two Euclid layers in DR1), PSF fields (stellar SED reference). No individual galaxies named.
- Table 2 (p. 14) and Table 3 (p. 15): main photo-z metrics. Fig. 5 (p. 14) zphot vs zspec, Fig. 6 (p. 15) PIT, Fig. 7 (p. 16) Frac68 vs IE, Fig. 8 (p. 17) EDF-N scatter.
- Fig. 3 (p. 12): tile validation map; Fig. A.1-A.4 (p. 27-29): zero-point maps; Fig. 2 (p. 10): sample-variance suppression; Table B.1 (p. 29): COSMOS2020 band zero-point factors and systematic errors.
- Fig. 4 (p. 13): magnitude distributions of spec-z samples; Table 4 and Figs. 9-10 (p. 17-18): SED validation; Fig. 11 (p. 19): DESI class Sankey diagram.

## Cross-references
- Companion: Enia et al. 2026 (physical properties, see enia.md); Tucci et al. 2026 (Q1 PHZ, EC:T26); Kümmel et al. 2026 (MER catalogue; column definitions, flags); Corcho-Caballero et al. 2026 (external data); Odier et al. 2026 (visibility masks, incl. PhotoZ mask and Pan-STARRS artefact map); Saulder et al. in prep. (spec-z compilation); Wright et al. in prep. (n(z) calibration); Tarsitano et al. 2026 (galaxy SED requirements); Romelli et al. 2026, Matamoro Zatarain et al. 2026 (compactness cut validation); Schirmer et al. 2026 (ice decontamination / IE passband change); Weaver et al. 2022 (COSMOS2020); Euclid DR1 Explanatory Supplement (https://euclid.esac.esa.int/dr/dr1/expsup).
