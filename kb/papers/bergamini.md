---
title: "Euclid Data Release 1 (DR1): NISP spectroscopy of gravitational arcs and multiple images"
short_name: bergamini
first_author: Bergamini
series: A&A Special Issue DR1-Foundation (Nov 2026)
local_pdf: ~/Desktop/euclid/papers/bergamini.pdf
local_text: ~/Desktop/euclid/text/papers/bergamini.txt
topics: [strong lensing, slitless spectroscopy, GELSA, emission-line maps, giant arcs, Einstein ring, custom spectral extraction, photo-z]
relevance_extended_galaxies: low   # for photometry / 2-D modelling / LSB of low-to-intermediate-z galaxies
---

# NISP slitless spectra and emission-line maps of four strongly lensed sources (Bergamini et al. 2026)

## TL;DR
A pilot study that uses the GELSA package to perform custom, non-pipeline extractions of NISP red-grism spectra for four strongly lensed background sources (two cluster arcs, one quad AGN candidate, one Einstein ring), measuring redshifts from one to three emission lines and building continuum-subtracted emission-line maps. It is a method demonstration rather than a data release: none of the extracted spectra or maps are DR1 products, and the standard SPE pipeline fails on such crowded, extended systems. For a galaxy-imaging group it is mainly useful as a worked example of how the slitless data can be turned into custom 1-D spectra and 2-D line maps with GELSA, and of what morphological smearing does to slitless line profiles.

## Key facts and numbers
- Spectra: red grisms RGS000 and RGS180 in all DR1 orientations; R > 480; 1206-1892 nm; 1.372 nm/px; 550 s per exposure (p. 3).
- Line sensitivity: EWS depth ~2e-16 erg/cm2/s at 3.5 sigma at 1.6 um for a 0.5" diameter source; ~5e-17 expected at full EDS depth (p. 3).
- Extraction aperture: 3 NISP pixels = 0.9", oriented perpendicular to dispersion for each exposure (p. 5). NISP pixel = 0.3".
- Emission-line maps resampled to the IE native pixel scale (0.1") and smoothed with a Gaussian of sigma = 2 px (0.2") (Fig. 1, p. 4).
- Number of exposures stacked: 38 (SPT-CLJ0411-4819, EDF-S), 9 (Abell 2280, EDF-N), 3 (WHJ181607.9+681651, EDF-N), 4 (PS1J1821+7130, EWS: RGS000+0, RGS000-4, RGS180+0, RGS180+4) (Table 1, p. 4).
- Redshifts (Table 1, p. 4): SPT-CLJ0411-4819 lensed source z = 1.771 +/- 0.006 (Halpha 1819.1 nm, [OIII]5008 1387.8 nm, Hbeta 1347.4 nm); Abell 2280 z = 1.670 +/- 0.012 (single line assumed Halpha, 1752.8 nm); WHJ181607.9+681651 z = 2.649 +/- 0.007 ([OIII] doublet at 1810.0 and 1827.5 nm plus tentative Hbeta at 1774.4 nm; strong [OIII]/Hbeta suggests AGN); PS1J1821+7130 z = 1.366 +/- 0.008 (single Halpha at 1553.1 nm, confirmed by [OII] doublet in DESI DR1) (p. 5-7).
- Redshift uncertainties come from the Gaussian-fit line width and include morphological broadening by the extended source along dispersion (p. 5). Forward-modelling that would improve this is not yet available (p. 5).
- Rough Einstein-radius masses (p. 7): 1e13 Msun (SPT-CLJ0411, theta_E ~7.5"), 3e13 Msun (Abell 2280, ~13.5"), 2e12 Msun (WHJ181607, ~2.5"), 3e11 Msun (PS1J1821, ~1.5").
- Photometric-redshift control sample of 160 DESI galaxies (0.3 < z < 2.5): sigma_z = 0.1; systematic underestimation of Delta z ~ 0.3 at 1 < z < 2.5 (p. 15). Photo-z of lensed sources: 1.8 +/- 0.1, 1.8 +/- 0.1, 2.5 +/- 0.4 (p. 15).

## Data products and data model
- No new released product. Inputs are the SIR-calibrated NISP-S dispersed frames and SIR calibration products (trace mapping, flux calibration) (p. 3); Euclid IE, YE, JE, HE imaging; ground-based DECam, MegaCam, HSC, UNIONS/DES data from OU-EXT (Appendix A).
- GELSA (https://github.com/elsa-euclid/gelsa, ELSA project; Gabarra et al. 2026) is the Python tool producing: (i) 2-D and 1-D spectra by resampling the dispersed images onto a wavelength grid; (ii) emission-line maps by resampling dispersed images in RA/Dec at fixed wavelength and drizzling (Fruchter and Hook 2002) multi-orientation exposures (p. 3).
- Colour images produced with the azulero code (Basset et al. 2026, v2.1.0) from IE, YE, JE, HE (p. 3).

## Processing and methods
1. Custom extraction on the calibrated NISP-S frames with GELSA; tilted exposures are rotated so that dispersion runs along pixel rows (p. 3).
2. Continuum removal: 1-D median filter of width 100 px (~137 nm) applied to each row of the dispersed image along dispersion; subtract to isolate emission-line signal (p. 3).
3. Emission-line map: resample at fixed wavelength in sky coordinates, drizzle-combine different dispersion directions (S/N gain and decontamination) (p. 3).
4. 1-D spectra extracted at hand-chosen positions on counter-images (cyan crosses), chosen so that traces do not cross other counter-images (p. 5).
5. Redshift from the peak of the most prominent line in Spec1, error from Gaussian fit width (p. 5). Photo-z cross-check with eazy-py and 11 Benitez templates after PSF-matching all bands to the worst-resolution filter (Appendix A, p. 15).

## Validation and performance
- Emission appearing at the same wavelength across multiple images with morphology matching the lensed features rules out contamination by unrelated sources (p. 6).
- Photo-z consistent within 1 sigma for SPT-CLJ0411 and WHJ181607; Abell 2280 spectroscopic z lies at the edge of the 1 sigma interval (Delta z ~ 0.13) (p. 6, 15).
- PS1J1821+7130 validated independently by DESI DR1 [OII] doublet; DESI fibre ~1.5" and PSF ~1.1" so ring light enters the lens-centred fibre (p. 6).
- No systematic accuracy benchmark of the method is provided beyond these four systems.

## Known issues, caveats, limitations
- Slitless spectra of extended sources are convolved with source morphology along dispersion: lines are broadened beyond the instrumental resolution (p. 5); line-width/velocity information is not clean.
- Emission-line maps are not monochromatic: adjacent lines (e.g. Halpha and [NII]) displaced along dispersion are superimposed on the map (p. 3). They differ from narrow-band imaging and integral-field data.
- Single-line redshifts (Abell 2280, PS1J1821) rely on the Halpha assumption; photo-z is a weak check (sigma ~0.1, offset up to 0.3) (p. 5, 15).
- The automatic SPE/MER pipeline cannot deblend lensed features near lens galaxies or in crowded cluster fields, so hand-tailored apertures are required (p. 1, 15).
- Photometry-based photo-z in crowded fields has PSF-matching issues between ground and space data (p. 15).
- Mass estimates are rough (point-like Einstein estimate) (p. 7).

## Implications for extended-galaxy photometry, 2-D modelling and low-surface-brightness work
- Limited direct relevance (high-z lensed sources at z = 1.4-2.6; lens deflectors at z = 0.24-0.68). Takeaways: (a) emission-line maps from slitless NISP data are feasible for extended sources with several grism orientations, with ~0.2" smoothed output sampled at 0.1", although true resolution is limited by the 0.3" NISP pixel and the PSF; (b) the approach (continuum-subtracting with a 100 px median filter then drizzling) is a template for studying Halpha morphology of larger low-z galaxies, but the red grism only reaches Halpha at z > 0.84, so low-z galaxies need other lines; (c) automated pipeline photometry fails to deblend arcs near lens galaxies: lens-galaxy modelling with Sersic profiles will need manual masking or lens-aware modelling.
- The three deflector galaxies are bright early types useful as isolated test cases for 2-D modelling: see objects below (PS1J1821+7130 lens at z = 0.235 is a relevant low-z case, with HE = 17.1 integrated ring magnitude).

## Practical recommendations for users
- For custom extractions use GELSA on SIR-calibrated frames; use all available grism orientations (EDF systems have 3-38 exposures, EWS 4) to improve S/N and mitigate contamination (p. 3).
- Choose extraction positions where traces avoid other bright sources and counter-images; use 0.9" wide apertures perpendicular to dispersion (p. 5).
- Do not trust single-line redshifts without an independent check (photo-z, ground optical spectra such as DESI).
- Treat emission-line map flux as including neighbouring blended lines along dispersion.

## Objects, fields and figures worth revisiting
Coordinates from Table 1 (J2000 deg, lens centre; p. 4):
- SPT-CLJ0411-4819 (cluster, z_d = 0.424, EDF-S): RA 62.79574, Dec -48.32765; lensed arc z = 1.771; HE = 19.7 (Fig. 1).
- Abell 2280 (cluster, z_d = 0.326, EDF-N): RA 265.87663, Dec +63.69491; red giant arc z = 1.670; HE = 18.2 (Fig. 2).
- WHJ181607.9+681651 (galaxy-scale quad/Einstein cross, early-type lens z_ph = 0.68, EDF-N): RA 274.03285, Dec +68.28095; source z = 2.649, probable AGN; HE = 21.1 (Fig. 3).
- PS1J1821+7130 (galaxy-galaxy Einstein ring, lens z = 0.235 from DESI DR1, EWS): RA 275.41843, Dec +71.50267; source z = 1.366; HE = 17.1 integrated (Fig. 4).
- Figures: Figs. 1-4 (p. 4-7) show RGB image, emission-line map and 1-D spectra; Fig. A.1 (p. 14) photo-z posteriors and SEDs.

## Cross-references
- Gabarra et al. 2026 (GELSA and emission-line maps), Fumana et al. 2026 (SIR calibration), Copin et al. 2026 (SIR Q1), Scodeggio et al. (SIR-DR1), Bergamini et al. 2026 (Q1 lens catalogue, B26), Walmsley et al. 2026, Lines et al. 2026a,b (lens discovery), Vincken et al., Fogliardi et al., Nightingale et al. 2026 (Einstein radii), Aussel et al. 2026 (DR1 overview), Corcho-Caballero et al. 2026 (EDF ground-based data).
