---
title: "Euclid Data Release 1 (DR1): Euclid Lens Identification Pipeline and Scientific Exploration (ECLIPSE) B: Discovery pipeline overview"
short_name: holloway
first_author: Holloway
series: A&A Special Issue DR1-Foundation (Nov 2026)
local_pdf: ~/Desktop/euclid/papers/holloway.pdf
local_text: ~/Desktop/euclid/text/papers/holloway.txt
topics: [strong lensing, discovery pipeline, machine learning, ensemble classifier, Space Warps, citizen science, expert grading, completeness, selection function, MER catalogue cuts, DR1 cutouts]
relevance_extended_galaxies: low
---

# ECLIPSE B: DR1 strong lens discovery pipeline (Holloway et al. 2026)

## TL;DR
The paper describes how the 15 072 grade A+B lens candidates in DR1 were found: a MER-catalogue cut (68 M objects), five neural networks plus an ensemble, two Space Warps citizen-science stages, and expert grading (p. 1-2). It also documents exactly how the DR1 cutouts were produced from MER stacks (10 x 10 arcsec, I_E luminance with NISP colour) (p. 3). For a galaxy-photometry group this is mostly background: the lens-finding machinery is of low direct relevance, but the catalogue cuts, cutout recipe and the completeness/selection-function discussion tell you what kind of massive early-type galaxy sample results and which ones are missed.

## Key facts and numbers
- DR1 covers 2000 deg2; EWS will cover 14 000 deg2 and about 1.5 billion galaxies; I_E PSF FWHM 0.16 arcsec (p. 1). Q1: 63.1 deg2, about 600 high-grade lenses (p. 1).
- Pipeline funnel (Fig. 1, p. 2): 6.1e7 ML-classified objects, about 200 000 to SW-Classify, 43 000 to SW-Refine, 24 000 to researcher grading ("Galaxy Judges", GJ). Totals in conclusions: 68 M ML-classified, 300 000 by volunteers, 30 000 graded by researchers (p. 10). Only 0.04% of 6.8e7 objects reached researchers (p. 6).
- Comprehensive search table (p. 7, excludes 200 and 50 deg2 areas): ML stage 8.5e3 directly to GJ, 1.4e5 to SW-Classify, 6.0e7 rejected; SW-Classify 2.5e3 to GJ, 2.8e4 to SW-Refine, 1.1e5 rejected; SW-Refine 4.9e3 to GJ, 2.3e4 rejected.
- SW-Classify: started 21 April 2026, 3.4 million classifications in 5 months; SW-Refine: started 21 May 2026, 570 000 classifications (p. 7). 50 deg2 pilot: 16 Feb 2026, one month, 796 volunteers, 490 000 classifications, about 60 000 subjects (p. 6).
- Phase 1, 200 deg2 rapid search: 701 grade A and 544 grade B, used to retrain networks (p. 5).
- Final: 15 072 grade A+B candidates (p. 10). Completeness: 0.73 (+0.08, -0.15) for grade A and 0.34 (+0.05, -0.06) for A+B in the comprehensive search area (abstract, p. 1); full-DR1 grade A completeness 0.81 (+0.09, -0.17) (p. 10).
- Direct ML to GJ path alone: 74% grade A+B purity at 21% completeness (p. 10). 60% of grade A lenses were found via the ML-to-GJ path (p. 8).
- Expert grading uses median 10 classifications per system, min 3 for X-consensus systems (p. 10).
- Forecast for DR2 (7500 deg2) and full EWS (14 000 deg2): 35 000 (65 000) high-scoring systems, of which 25 000 (48 000) high-grade lenses (p. 10). Euclid-Roman overlap 470 deg2; Euclid-LSST 7000-11 000 deg2 (p. 9).

## Data products and data model
- Inputs: stacked MER mosaics accessed via the ESA Science Archive Service and ESA Datalabs (p. 3). Bands I_E (VIS, 0.1 arcsec/pix) and Y_E, J_E (NISP, 0.3 arcsec/pix); H_E used by NN5 (p. 3-4).
- Cutouts: 10 x 10 arcsec. Human inspection images: I_E, I_E/Y_E, I_E/J_E, I_E/Y_E/J_E RGB composites with per-band arcsinh or mid-tone transfer (MTF) stretch; I_E sets luminosity, NISP bands set hue and saturation, to retain VIS resolution (p. 3). NN1-NN4 use compressed JPEG images (I_E arcsinh), NN5 uses FITS (I_E-only network plus I_E+J_E+H_E network, logit-mean) (p. 3-4).
- MER catalogue columns used: VIS_DET, MU_MAX, MUMAX_MINUS_MAG, I_E and H_E magnitudes (p. 3). Q1-era columns SPURIOUS_PROB and GAIA_CROSSMATCH were dropped (p. 3).
- Per-system outputs (published in the ECLIPSE catalogue, see ECLIPSE-A): calibrated expert grade (A/B/C/X), lens score; SW-Classify score p_SWC = P(Lens | classifications), SW-Refine score p_SWR = P(grade in {A,B} | classifications) (p. 2, 4).
- Grade boundaries on mean (calibrated) score s: A s >= 2.5; B 1.5-2.5; C 0.5-1.5; X below 0.5 (p. 5). Early searches used A >= 2, C >= 1, X < 1 initially; the published catalogue uses the revised half-integer boundaries including re-graded 200 and 50 deg2 systems (p. 5, footnote 4).
- Training simulations: S1 (real galaxies for lens and source, Rojas et al. 2026) and S2 (GLAMER with Flagship deflectors and HUDF-based sources) (p. 18).
- Segmentation maps masking lens, source and neighbours per candidate will be released with Vincken et al. (in prep.) (p. 2).

## Processing and methods
1. Catalogue cut (p. 3): VIS_DET = 1; MU_MAX > 15 (peak surface brightness, removes saturated stars); MUMAX_MINUS_MAG > -2.6 (compactness, removes point-like objects); I_E < 23 or H_E < 22.5. No colour cuts, deliberately, so that spiral deflectors and red arcs survive (p. 3). Result 68 M objects excluding deep tiles and Q1 overlap.
2. Five networks (p. 3-4): NN1 AstroVink (Vision Transformer, DINOv3 encoder fine-tuned); NN2 OU-100 CNN (Wilde et al. 2022); NN3 four-layer CNN; NN4 Zoobot ConvNeXt foundation model fine-tuned; NN5 deeper Zoobot ConvNeXt-Base ensemble using FITS. Training sets: Q1 lenses and non-lenses, 200 deg2 DR1 lenses, simulations.
3. Ensemble of NN1 and NN5 via the independent-classifier Bayesian combination (Holloway et al. 2024), calibrated on 50% of the A+B systems from the 50 deg2 search (p. 4).
4. 50 deg2 calibration search: for each network 100% of top 2000, 50% of next 4000, 25% of next 8000; plus about 30 000 random objects; maps raw network score to A+B purity (p. 5-6). Rank R_8% is where A+B purity is 8%; all systems above R_8% in any network or ensemble, about 160 000, went to SW-Classify, plus 50 000 randoms and 30 000 from a preliminary ensemble (p. 6). Systems above R_80% went directly to experts.
5. SWAP (Space Warps Analysis Pipeline): each volunteer has a 2 x 2 skill matrix S_ij = (1 + N_Ci|Gj)/(2 + N_Gj); each subject starts with prior 5e-4 and is updated by Bayes per classification; removal if score < 1e-5 after at least 6 classifications or after 25 classifications (p. 4). SW-Refine uses the same machinery with A/B/C/X grades, 10 classifications per subject (p. 4-5). Thresholds: p_SWC > 1 - 10^-8.875 goes straight to GJ (50-85% A+B purity previously); p_SWC > 0.01 to SW-Refine; p_SWR > 0.87 to GJ (p. 6).
6. Expert grading: leave-one-out calibration of each grader's skill (scores A=3, B=2, C=1, X=0), skill matrix with (1 + N)/(4 + N), then recalculated grades with flat prior 0.25 (p. 5). Optimism varies strongly between graders (Fig. 9, p. 10).
7. Completeness (Appendix E, p. 18-19): Beta posteriors with Jeffreys prior for lenses lost at each stage, using 50 000 randoms (ML-stage losses, divided by SW completeness), about 1000 randoms from SW-Classify and about 2000 from SW-Refine shown in full to GJ.

## Validation and performance
- ML purity versus rank: ensemble beats individual networks; many individual networks are strong; most lenses lie below rank 20 000 (Fig. 2-3, p. 6-7).
- Higher SW-Refine rank gives a higher fraction of A+B than SW-Classify rank, justifying the second stage (Fig. 4-5, p. 7).
- Simulated-lens selection function (Fig. 6, p. 7-8): S/N is the dominant factor, then Einstein radius; stages compound, motivating direct-to-GJ shortcuts. S/N defined as maximum ratio of cumulative lensed-source flux to cumulative RMS background noise.
- Recovery of known candidates by SW thresholds (p. 9): 64% for Q1 grade A+B, 44% for the 50 deg2 candidates, 48% for the 200 deg2 candidates; the DR1 threshold p_SWC > 0.01 is far above the Q1 value 1e-5 and the prior 5e-4, which lowers completeness.
- Pathway of grade A lenses (Fig. 8, p. 9): largest loss at the SW-Refine to GJ threshold, set by expert inspection budget. Thousands of A+B lenses lost there (p. 8).

## Known issues, caveats, limitations
- Completeness numbers in the paper are not mutually consistent: Sect. 4.1.2 quotes 78 (+8, -16)% grade A and 42 (+7, -8)% A+B "in ECLIPSE-A" (p. 8), the abstract quotes 0.73 and 0.34 for the comprehensive area (p. 1), while ECLIPSE-A quotes 0.81 and 0.43 for full DR1. Treat as roughly 0.8 (A) and 0.4 (A+B) and read ECLIPSE-A for the final numbers; they refer to the catalogue-selected parent, not all lenses (p. 18).
- Selection depends on S/N and Einstein radius; also on lens-source colour contrast (not modelled); ML selection function not yet characterised (p. 8).
- Expert grades are subjective with strong inter-grader variability; calibration only partly mitigates this (p. 5, 10).
- Possible circular training bias (networks retrained on lenses found by earlier network versions); mitigated by random-sample inspection and simulations (p. 5).
- Deep tiles and Q1 overlap excluded; the 50 deg2 and 200 deg2 areas were graded under different protocols (p. 5).
- Training and SW inputs include JPEG-compressed images for NN1-NN4, so ML scores do not use the science FITS pixels except for NN5.
- Dropped GAIA_CROSSMATCH and SPURIOUS_PROB cuts because Gaia crossmatch removed low-redshift lens candidates (p. 3); MER SPURIOUS_PROB therefore not used as a quality cut.

## Implications for extended-galaxy photometry, 2-D modelling and low-surface-brightness work
- Largely irrelevant to LSB, haloes and ICL. The useful pieces: (i) the documented MER-based galaxy selection with saturation (MU_MAX) and compactness (MUMAX_MINUS_MAG) cuts, which gives a quick way to get a bright, extended, unsaturated galaxy sample from MER (p. 3); (ii) the recipe for colour cutouts (I_E luminance, NISP colour) when a 0.1 arcsec resolution RGB image is wanted; (iii) the note that Gaia crossmatch cuts remove low-redshift extended galaxies, relevant when building low-z samples from MER (p. 3).
- The resulting lens population are massive early types, so the lens catalogue is a ready target list for deep Sersic/MGE modelling of ellipticals (see ECLIPSE-A, C, D).
- The cutouts are 10 arcsec and stretched; they are not suitable for outer-profile or LSB work.

## Practical recommendations for users
- Use the published calibrated grades or lens score, not raw individual grades; choose grade A for purity, A+B for completeness, and be aware that thresholds in the catalogue follow the half-integer boundaries (p. 5).
- If reproducing the parent selection, use the four cuts listed above; do not add SPURIOUS_PROB or Gaia crossmatch cuts if low-redshift galaxies matter.
- If using the cutouts for ML, note NN5 works on FITS I_E (+J_E+H_E); fine-tuning foundation models (Zoobot, DINOv3) works well for morphology tasks (p. 3-4).
- Do not treat the lens sample as complete or volume-limited without the selection function (S/N, theta_E) (p. 8).

## Objects, fields and figures worth revisiting
- No named individual lens systems or coordinates are given in this paper; see ECLIPSE-A for named systems.
- Fig. 1 pipeline flow chart and thresholds (p. 2); Fig. 2-3 ML purity and yield versus rank (p. 6-7); Fig. 6 selection function versus S/N and theta_E (p. 8); Fig. 8 grade-A pathway (p. 9); Fig. 9 grader optimism spread (p. 10); Fig. B.1-B.2 simulated lens collages (p. 19); Fig. D.1 flagged and missed examples.

## Cross-references
- ECLIPSE-A (Lines et al.): catalogue; ECLIPSE-C (Nightingale et al.): modelling; ECLIPSE-D (Nersesian et al.): photo-z and SED.
- MER catalogue and mosaics (Kummel et al. 2026); Q1 Strong Lens Discovery Engine papers (Walmsley et al., Rojas et al., Lines et al., Li et al., Holloway et al. 2026b, Ecker et al.); Vincken et al. (network comparison, segmentation maps); Fogliardi et al. (NN5 training); Wielders et al. (multi-galaxy lenses); Li et al. and Ecker et al. (DSPL, edge-on); 4SLSLS (Collett et al. 2023).
