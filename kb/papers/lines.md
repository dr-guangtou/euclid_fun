---
title: "Euclid Data Release 1 (DR1): Euclid Lens Identification Pipeline and Scientific Exploration (ECLIPSE) A: Strong lens catalogue overview"
short_name: lines
first_author: Lines
series: A&A Special Issue DR1-Foundation (Nov 2026)
local_pdf: ~/Desktop/euclid/papers/lines.pdf
local_text: ~/Desktop/euclid/text/papers/lines.txt
topics: [strong lensing, lens catalogue, DR1, machine learning, Space Warps, citizen science, VIS cutouts, MER catalogue selection, deflector galaxies, completeness, double-source-plane lenses, disc lenses]
relevance_extended_galaxies: medium
---

# DR1 strong lens catalogue overview (Lines et al. 2026)

## TL;DR
The paper presents the ECLIPSE catalogue of strong lens candidates in Euclid DR1 (about 2000 deg2): 6073 grade A, 8999 grade B and 9010 grade C candidates (plus 2580 grade X non-lenses), found by combining five ML networks, Space Warps citizen science and expert grading (p. 1, 5). Automated lens models and deblended deflector photometry, photometric redshifts and stellar masses are provided for the A+B systems. For a galaxy-imaging user the value is twofold: a ready-made list of about 15 000 massive early-type galaxies (median log M* = 11.39, z_phot = 0.68) with deblended light models, and a documented recipe for the DR1 cutouts and MER-catalogue cuts used (p. 3, 10). It is an overview paper; method detail sits in ECLIPSE-B (search), -C (modelling) and -D (photometry/SED).

## Key facts and numbers
- Search area about 2000 deg2 of DR1 single-visit coverage; Q1 area and the deep fields were deliberately excluded to avoid duplication, because the ML models were trained on Q1, and to keep the search homogeneous (p. 2).
- About 900 million MER-detected sources in DR1; after catalogue cuts and removing Q1/deep areas, 68 million objects were searched (p. 3).
- Depths quoted: NISP point-source 5 sigma Y_E = 24.6, J_E = 24.6, H_E = 24.5; VIS I_E = 26.0 for extended sources (p. 2). VIS pixel 0.1 arcsec, PSF FWHM 0.16 arcsec; NISP pixel 0.3 arcsec, PSF FWHM 0.35 arcsec (p. 3).
- Catalogue: 26 662 unique objects: 6073 A, 8999 B, 9010 C, 2580 X (p. 5). A+B = 15 072 high-confidence candidates, about 8 per deg2 (p. 11). 417 A, 161 B and 55 C were previously reported; overall 93% of A, 98% of B, 99% of C are new (p. 5, 14).
- Human effort: 6975 citizen scientists (over 4.5 million classifications, median 25 per volunteer), 67 experts, average about 10 expert grades per candidate (p. 3, 14). Space Warps classified 220 000 ML-prioritised images plus 50 000 random images; about 30 000 were flagged as likely lenses and went to experts (p. 3).
- Deflector properties (A+B, ECLIPSE-D sample of 9538 systems): log10 M*/Msun = 11.39 (+0.29, -0.33) with Salpeter IMF; log sSFR/yr = -11.25 (+0.57, -0.37); z_phot = 0.68 (+0.33, -0.29); median I_E about 21.3 (p. 10-11). Effective Einstein radius median 0.85 (+0.44, -0.24) arcsec; 1st-99th percentile 0.42-2.32 arcsec (7980 successful lens models) (p. 1, 10).
- Comparison medians of lens redshift: SLACS 0.22, BELLS 0.52, SL2S 0.46, HSC 0.59, COWLS (JWST) 0.81, ECLIPSE 0.68 (p. 10).
- Rare classes: 84 double-source-plane candidates, 1060 disc lenses (projected axis ratio q <= 0.5, i >~ 60 deg, S0 included), about 300 with AGN counterparts, about 65 with the activity confidently tied to the lens, about 500 flagged by morphology as possible lensed quasars (p. 6-9).
- Completeness (relative to expert grades on the 68 M parent): 0.81 (+0.09, -0.17) for grade A, 0.43 (+0.07, -0.08) for A+B (p. 12). Only 0.04% of the parent sample could be seen by experts (p. 12).
- Known-lens recovery: 428 of 549 (78%) re-inspected previous candidates inside the search footprint; 96% (290/303) of "sure" and 56% (138/246) of "possible" (p. 13).
- Spectroscopy: DESI DR1 vetted redshifts for 379 systems: 351 deflector-only, 8 source-only, 20 both; deflector z 0.05-1.1, source z 0.3-2.7 (p. 5, 14). About 2400 candidates have DESI spectra (950 in DR2) (p. 13).
- Forecasts: about 100 000 candidates in the full Euclid Wide Survey; 60 000 cumulative at DR2 (mid 2029), 110 000 at DR3 (late 2031) (p. 1, 14).
- Cosmology: Planck 2016 flat LCDM, H0 = 67.74, Om = 0.3089 (p. 2).

## Data products and data model
- Input imaging: DR1 VIS I_E and NISP Y_E, J_E, H_E mosaics via the MER pipeline; 10 x 10 arcsec cutouts per candidate (p. 3). The cutouts are display images, not science stamps: luminance from VIS I_E for maximal resolution, colour from NIR fluxes (as in Walmsley et al. 2026). Processing variants: arcsinh and mid-tone transfer function scalings, applied to grey-scale I_E and to I_E+Y_E, I_E+J_E and I_E+Y_E+J_E composites (p. 3).
- Input catalogue: official MER object detection catalogue (Kummel et al. 2026). Columns used: VIS_DET, I_E, H_E, MU_MAX, MUMAX_MINUS_MAG (p. 3).
- Released catalogue (Zenodo, doi 10.5281/zenodo.19654904): every object reaching expert inspection, with grade (A/B/C/X), a continuous lens score aggregated from inspector classifications, earliest publication reporting the lens (where previously known), lens-model parameters, deflector photo-z and stellar population properties. Interactive browser: https://euclid-eclipse-lenses.org (p. 5, 14). The Q1 lens catalogue is at doi 10.5281/zenodo.15025832 (p. 2). DR1 data itself at https://www.cosmos.esa.int/web/euclid/data-release-dr1.
- Object naming: "Euclid DR1 JHHMMSS.sss+DDMMSS.ss" (abbreviated in figures); coordinates are decodable from the names.
- Lens-model products (from ECLIPSE-C): effective Einstein radius (from tangential critical curve area), deblended deflector and source photometry, pixelised source reconstructions, vetting category (success, failure, outside model scope, unsure if lens, no consensus) (p. 4).
- Not part of this catalogue: lensed-quasar-specific catalogue (future work), multi-deflector and DSPL models (Wielders et al., Li et al., in prep.).

## Processing and methods
1. Catalogue-level selection on the MER catalogue (p. 3): VIS_DET = 1; (I_E < 23) or (H_E < 22.5); MU_MAX > 15 mag/arcsec2 (rejects saturated peaks); MUMAX_MINUS_MAG > -2.6 (compactness filter removing objects whose flux is dominated by few pixels). Compared with Q1 (I_E < 22.5) the magnitude limit is deeper and admits redder systems.
2. Five ML networks from different teams score all 68 M cutouts; scores combined using performance on a calibrated test set. Top 220 000 go to Space Warps (p. 3).
3. Space Warps Classify (lens / non-lens), then Space Warps Refine (grades), each object seen by 6 to 25 volunteers; Bayesian aggregation (Marshall et al. 2016) (p. 3).
4. Expert "Galaxy Judges" grading A/B/C/X with calibrated aggregation into a lens score; highest ML and SWC scores bypass later stages (p. 3-4, 12).
5. Lens modelling with PyAutoLens on A+B (p. 4): ML-based decomposition into deflector light, source light and other line-of-sight objects gives masks and priors; deflector light = multi-Gaussian expansion (MGE), deflector mass = SIE plus external shear. Three stages: (i) MGE deflector and source to set mass model; (ii) pixelised source on adaptive Delaunay mesh; (iii) Sersic deflector and source with mass fixed, giving deblended photometry. Assumes one deflector and one source plane.
6. Deblended photometry (p. 4): single Sersic for deflector and for source in I_E (n, R_e, flux). The same fixed mass model and I_E-based mask are applied in all other bands with n and R_e fixed and only the flux free, producing unconvolved deflector and source images per band, including ground-based UNIONS (north) and DES (south). Aperture photometry is done on PSF-matched model images.
7. Photo-z with Phosphoros (same SED library as the main Euclid photo-z), validated on spectroscopic lenses; SED fitting with Prospector / FSPS, non-parametric SFH, Salpeter IMF (p. 4).
8. Completeness estimated from 50 000 random objects (plus about 1000 and 2000 random objects at SWC and SWR stages shown fully to experts), with Beta-distribution posteriors (Jeffreys prior) for lost lenses (p. 11-12); selection function of visual stages measured by injecting simulated lenses (real Euclid galaxies; GLAMER with Flagship deflectors and HUDF-based sources) (p. 12).

## Validation and performance
- Two top ML networks: none of their 1000 highest-scoring objects was graded non-lens; top 117 unique objects (mean of two networks) were all grade A (p. 3, 24).
- Lens model vetting (at least 4 inspectors, 75% agreement): success for 67% of A and 43% of B; outside scope 5% / 4%; failure 10% / 13%; unsure-if-lens 0.1% / 1.4%; no consensus 17% / 38% (p. 5). Even at 50% agreement, models cast doubt on only 0.4% of A and 4.8% of B (p. 5).
- Visual-inspection selection function: recovery is driven mainly by lensed-source S/N; S/N <~ 10 gives cumulative recovery below 20%; at fixed S/N larger Einstein radius helps (p. 12).
- Lost-lens estimates for grade A: 490 (+5300, -490) at ML stage (prior-dominated), 270 at SWC, 860 at SWR; A+B: 5300, 7100, 7000 respectively (p. 12).
- Missed known lenses: only 8 of 549 (1.5%) lost at catalogue level, six of those because MER never detected them due to imaging artefacts; most losses at Space Warps (66) and ML (44) (p. 13).
- Spectroscopy cross-check: of 12 NGPS follow-ups, one grade A looked like a non-lens (p. 6).

## Known issues, caveats, limitations
- Catalogue selection (MU_MAX, compactness) excludes very compact or saturated deflectors and lensed-quasar-dominated systems (p. 8).
- Search images are colour composites with VIS luminance, so lens-light subtraction was not used; faint arcs buried in bright deflector cores are missed, and the brightest deflectors are under-represented relative to the Collett (2015) forecast; Einstein radii are systematically larger and sources about a magnitude brighter than forecast (p. 11).
- Very red deflectors look faint in VIS-based inspection images despite clear NIR detection (Fig. 6m); VIS-dropout sources are undetectable (p. 9).
- Imaging artefacts near bright objects or overlapping tiles can cause MER non-detections (five "possible" and one "sure" known lens missed this way) (p. 13). Two ML rejections of known lenses were due to image-processing problems and two to arcs not fully contained in the 10 arcsec cutout (p. 13).
- Modelling and ECLIPSE-D property samples are not random: models fail preferentially for small Einstein radii or complex deflector morphology; disc deflectors with dust or spiral structure give poor light subtraction (p. 8, 10). ECLIPSE-D needs detection in at least six bands and M* > 1e10 Msun (p. 10).
- Disc-lens sample is a lower limit because face-on and moderately inclined discs cannot be separated from ellipticals by axis ratio (p. 7).
- Grades are subjective; use the continuous lens score for custom purity/completeness trade-offs (p. 5, 24). Completeness for grade A+B is only 43%, limited by expert capacity (p. 12).
- Simulation-based selection function likely overestimates recovery for discs, mergers and multi-deflector systems (p. 13).

## Implications for extended-galaxy photometry, 2-D modelling and low-surface-brightness work
- Not a photometry paper, but it provides a large, homogeneous sample of massive quiescent galaxies at z about 0.3-1.1 with I_E about 21 and independent deblended Sersic photometry; useful as a comparison set for Sersic or MGE fits to early types in DR1 (p. 10).
- The modelling strategy (fit Sersic or MGE in I_E, then fix structure and fit only fluxes in other bands on a common mask) is a practical template for multi-band deflector photometry when a companion (lensed arc) contaminates the light (p. 4).
- Catalogue-level MER photometry of deflectors is blended with arcs; the deblended values are preferred for lens galaxies (p. 4).
- The saturation (MU_MAX > 15) and compactness (MUMAX_MINUS_MAG) columns are useful quick quality cuts for building clean galaxy samples.
- Dust and spiral structure break automated smooth-profile light subtraction in disc galaxies; relevant for bulge-disc work (p. 8).
- Irrelevant to LSB, stellar haloes and ICL, apart from the Appendix C collisional ring galaxies (empty-centred rings detected in no band) which are a curiosity of very low central stellar density (p. 25).

## Practical recommendations for users
- Select a lens sample by grade A or A+B, or threshold the continuous lens score; remember the sample is not complete (A: 81%, A+B: 43%) and biased towards high S/N, larger theta_E, bright sources.
- For deflector photometry use the ECLIPSE-D deblended values rather than MER catalogue fluxes; check the lens-model vetting category (success / failure / outside scope) before using any model-derived quantity.
- To reproduce the parent sample from the MER catalogue: VIS_DET = 1, (I_E < 23 or H_E < 22.5), MU_MAX > 15, MUMAX_MINUS_MAG > -2.6 (p. 3).
- Remember 10 x 10 arcsec cutouts truncate extended arcs; for light modelling of large galaxies use larger stamps from the MER mosaics rather than these display cutouts.
- Use DESI-vetted redshifts (379 systems) where available as ground truth for photo-z checks.

## Objects, fields and figures worth revisiting
Names encode J2000 coordinates; decimal degrees computed from the names (RA, Dec). Sky is mostly the Euclid Wide southern fields (around RA 36-90, Dec -60 to -20) plus a northern strip around Dec +55 to +78.
- J045008.828-571519.90 (72.5368, -57.2555): first showcase lens, Fig. 2a (p. 5).
- J045417.497-340950.95 (73.5729, -34.1642): clearest double-source-plane lens, two concentric near-complete rings of different colours, Fig. 3a (p. 6).
- J022455.052-601235.97 (36.2294, -60.2100): low S/N candidate with two Einstein rings around an edge-on disc, Fig. 3m, described as the first of its kind (p. 6-7).
- J042911.429-204453.48 (67.2976, -20.7482): face-on spiral lens with a complete ring (Fig. 4a) with DESI deflector and source redshifts; subject of Enzi et al. (in prep.) (p. 7-8).
- J023656.861-583041.95 (39.2369, -58.5117): bright extended arcs with resolved source structure, Fig. 6f, sensitive to substructure (p. 9).
- J170734.355+555258.98 (256.8931, +55.8830): grade C bright early-type at z = 0.258 with source at z = 0.468 (DESI) (p. 24).
- J171525.314+583731.15 (258.8555, +58.6253): inclined disc at z = 0.302, source z = 0.731 (p. 24).
- J094904.876+652707.32 (147.2703, +65.4520): compact red deflector z = 0.805, source z = 1.485 (p. 24-25): a high-z massive early-type.
- J100937.880+724953.06 (152.4078, +72.8314): "empty ring" (probable collisional ring); all-band cutouts and failed lens model, Fig. C.2 (p. 26). J175700.256+631344.17: ring plus companion pair with DESI z = 0.7718 and 0.7732 (p. 25).
- Known lensed quasars rediscovered: DES J0408-5354, DES J0420-4037, ATLAS J2344-3056, DES J0115-5244, SDSS J1524+4409, J0316-4106 (J031600.711-410609.60 = 49.0030, -41.1027, Fig. 5j) (p. 8-9).
- Key figures: Fig. 1 (lens counts versus area, p. 2), Fig. 7 (property distributions, p. 10), Fig. 8 (z versus theta_E against SLACS, BELLS, SL2S, HSC, COWLS, p. 11), Fig. 10 (visual selection function, p. 13), Fig. A.2 (random examples per grade, p. 24).

## Cross-references
- ECLIPSE-B (Holloway et al.): discovery pipeline, ML calibration, completeness derivation.
- ECLIPSE-C (Nightingale et al.): lens modelling with PyAutoLens, vetting.
- ECLIPSE-D (Nersesian et al.): deblended photometry, photo-z, SED fitting.
- MER catalogue paper (Kummel et al. 2026), Q1 lens papers (Walmsley et al. 2026; Rojas et al. 2026; Lines et al. 2026a,b; Li et al. 2026), Euclid photo-z papers (Tucci et al.; Hartley et al.), Vincken et al. (ML networks), Rojas et al. (re-inspection of known lenses), Storfer et al. (DESI vetting), Acevedo Barroso et al. and Moustakas et al. (lensed AGN), Sonnenfeld et al. 2026 (M/L of ellipticals from Q1 lenses).
