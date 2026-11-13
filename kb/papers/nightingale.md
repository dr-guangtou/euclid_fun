---
title: "Euclid Data Release 1 (DR1): Euclid Lens Identification Pipeline and Scientific Exploration (ECLIPSE) C: Lens modelling pipeline overview"
short_name: nightingale
first_author: Nightingale
series: A&A Special Issue DR1-Foundation (Nov 2026)
local_pdf: ~/Desktop/euclid/papers/nightingale.pdf
local_text: ~/Desktop/euclid/text/papers/nightingale.txt
topics: [strong lens modelling, PyAutoLens, multi-Gaussian expansion, MGE lens light, Sersic, VIS PSF, MER effective PSF, segmentation, deblended photometry, Einstein radius, source reconstruction, visual vetting]
relevance_extended_galaxies: medium
---

# ECLIPSE C: automated lens modelling of 15 072 DR1 lenses (Nightingale et al. 2026)

## TL;DR
Automated PyAutoLens-JAX models of all 15 072 grade A+B lens candidates, each fitted in three sequential stages (MGE light and source, pixelised Delaunay source, Sersic light) using 10 x 10 arcsec VIS cutouts with the MER effective PSF (p. 2-5). More than 20 experts vetted the models: 67.5% of grade A and 43.1% of grade B were judged successful at 75% agreement, giving 7980 usable models (p. 8, 11). For galaxy modellers the relevant lessons are the MGE lens-light recipe (two sets of 20 Gaussians), the use of the MER effective PSF, the ML-based masking of neighbours, and a catalogued list of lens-light failure modes (dust, asymmetric structure, edge-on discs, AGN) (p. 4, 10, 15). Released products include Sersic structural parameters for deflectors, masks, segmentation maps and mass maps.

## Key facts and numbers
- Modelled sample: 15 072 grade A+B (6073 A, 8999 B); over ten times larger than any earlier modelled lens sample (p. 1-2, 12). Earlier comparison: 419 JWST COWLS lenses (p. 2); about 500 Q1 lenses (p. 2).
- Image cutouts: 100 x 100 pixel VIS I_E cutouts = 10.0 x 10.0 arcsec at 0.1 arcsec/pix, containing science image, RMS noise map and PSF (p. 3). VIS PSF FWHM about 0.16 arcsec (p. 2).
- Software: PyAutoLens version 2026.10.7.1; PyAutoLens-JAX run on CPUs; nested sampler nautilus; also PyAutoLens-Assistant for workflow management (p. 3-4). Pipeline repository: euclid_strong_lens_modeling_pipeline under PyAutoLabs on GitHub (p. 4).
- Number of non-linear parameters: 15 (MGE fit), 10 (pixelised fit), 12 (Sersic fit) (p. 4).
- MGE lens light: two sets of 20 Gaussians, logarithmically spaced widths from 0.0001 arcsec to the mask radius, shared centre, independent axis ratio and orientation per set (6 non-linear parameters). Source: one set of 20 Gaussians (p. 4-5, 23). Reference He et al. 2024 used up to six sets of 30 Gaussians for HST; two sets chosen as compromise, helped S0 galaxies with bulge+disc (p. 4).
- Mass: singular isothermal ellipsoid plus external shear; effective Einstein radius theta_E = sqrt(A_crit / pi) from the tangential critical curve (p. 4).
- Nautilus settings (Table A.3, p. 25): MGE fit 750 live points, 200 000 evaluation limit; pixelised 300 live points, 100 000; Sersic 100 live points, 100 000. Convergence f_live < 0.01 and N_eff >= 500 (p. 25).
- Compute: fewer than 250 000 CPU hours in total, individual fits typically under 5 hours (p. 14). Inspection: about 10 seconds per lens, four votes each, around 167 person-hours (p. 15).
- Results (75% agreement), grade A: success 4098 (67.5%), failure 580 (9.6%), multi-galaxy lens 317 (5.2%), DSPL 15 (0.2%), unsure-if-lens 7 (0.1%), no consensus 1032 (17.0%), incomplete 24 (0.4%). Grade B: success 3882 (43.1%), failure 1161 (12.9%), MGL 385 (4.3%), DSPL 4, UIL 123 (1.4%), NC 3385 (37.6%), incomplete 59 (0.7%) (Table 2, p. 8). 83 candidates have no completed pixelised model (p. 8).
- Failure modes, from a 2990-candidate subset with 210 failures at 75%: lens-light subtraction 66 (31.4%), segmentation 39 (18.6%), source/mass 12 (5.7%), no consensus 44.3% (Table 3, p. 10; p. 15).
- Successful models (N = 7980): median theta_E = 0.85 arcsec, 16th-84th percentile 0.61-1.29 arcsec, tail beyond 2 arcsec; Einstein radii peak near 0.7 arcsec (p. 11). Median I_E-band total source magnification 8.1 (16th-84th 4.2-16.8), 43 systems above 120 (p. 12-13).
- Lens effective radius versus Einstein radius: Spearman coefficient 0.46 for 7976 systems (p. 12). Four of 7980 SC systems lack a VIS Sersic fit (p. 12).

## Data products and data model
- Inputs: VIS I_E MER stack cutouts plus RMS map and PSF stamp; NISP Y_E, J_E, H_E and ground-based EXT bands (UNIONS, DES) on the same 0.1 arcsec grid from MER, no extra PSF subsampling (p. 3). Data obtained via the ESA Science Archive Service (https://eas.esac.esa.int/sas/) and ESA Datalabs (p. 2-3, 17).
- PSF: effective PSFs supplied by the MER pipeline (position- and band-dependent PSF models propagated through resampling and stacking); not the colour-dependent SHE PSF (p. 3).
- Preprocessing products from the ML segmentation framework (AstroVink-TREX, Vincken et al. 2026a): maps of lens light, lensed source and contaminating galaxies; fitting mask (circle extending 2 arcsec beyond the furthest segmented source pixel); candidate conjugate points (p. 3).
- Released through the ECLIPSE catalogue (Zenodo doi 10.5281/zenodo.19654904; browse at https://euclid-eclipse-lenses.org): inspection classifications and consensus outcome, lens-model parameters (theta_E, SIE shape, shear), magnifications (Sersic-based and Delaunay-based), FITS images of deblended lens and source light and source reconstructions in VIS, NISP and EXT bands (see ECLIPSE-D), convergence, potential and deflection maps, masks and segmentation maps, COOLEST-format models, Witt-Wynne diagnostics for lensed-transient prediction (p. 12, 17).
- Sersic lens-light structural parameters (Sersic index, effective radius, axis ratio, luminosity) in VIS for all vetted models; the paper explicitly suggests using these for a census of lens-galaxy morphology (p. 15).

## Processing and methods
1. Segmentation and masking by ML (p. 3): brightest pixel of the predicted lens-light map sets the mask centre and initial lens-light and mass centre, refined with nearby VIS light; first-fit lens-light centre prior is uniform within +-0.1 arcsec. Contaminating galaxies are removed from the likelihood by zeroing data and setting RMS to 1e8 in flux units, while keeping the pixels for ray tracing (p. 3).
2. Conjugate-point penalty: candidate image-plane peaks are ray-traced at each likelihood call; penalty if maximum source-plane separation exceeds a threshold (0.3-0.5 arcsec from a pre-fit in the first fit; later three times the updated separation, minimum 0.2 arcsec) (p. 3, 5-6, 25).
3. Semi-linear inversion: lens-light and source intensities are solved jointly as non-negative linear parameters (JAX primal-dual interior-point NNLS), a ridge of 1e-3 added for unregularised amplitudes; only shape and mass parameters are sampled (p. 4, 24).
4. Fit 1: MGE lens, MGE source, SIE plus shear; sets the mass model and lens-light subtraction (p. 5).
5. Fit 2: lens MGE geometry fixed to fit 1 (intensities re-solved linearly), source replaced by Delaunay mesh from Hilbert-curve placement (500 points plus 30 boundary points), barycentric interpolation, adaptive split (cross) regularisation with strength inferred; SIE centre freed within 0.1 arcsec (p. 6, 24).
6. Fit 3: mass model fixed to fit 1; lens and source replaced by elliptical Sersic profiles in VIS; lens and source magnitudes from total flux; magnification from lensed over intrinsic source flux (p. 6). Spatially varying sub-pixel oversampling (4, 4, 2 inside 0.1, 0.1-0.3, beyond 0.3 arcsec in MGE fit; 16, 4, 2 in Sersic fit) (p. 23).
7. Other bands: the same fixed VIS mass model with Sersic lens and source is fitted independently in each NISP and EXT band (see ECLIPSE-D) (p. 6, 25).
8. Visual inspection: preliminary round with 12 experts on 200 models of 569 modelled grade-A lenses; main campaign more than 20 experts, 4-7 votes per model, 75% consensus rule; categories SC, FL, UIL, DSPL, MGL, with secondary failure categories assigned in causal order (segmentation, lens light, source/mass) (p. 6-7, 25-26).

## Validation and performance
- Qualitative vetting rather than numerical truth: Einstein radius is judged reliable by experts at SC; no individual parameter uncertainties are reported, calibration against systematics deferred (p. 11).
- At 100%, 75% and 50% consensus the grade A success rates are 49.6%, 67.5%, 72.6% and the grade B rates 24.0%, 43.1%, 53.6% (Table 2, p. 8).
- Four DSPL "consensus" objects re-inspected by DSPL experts: four of nine were not convincing (p. 9-10).
- Einstein radii are relatively robust to modelling choices (Etherington et al. 2022) (p. 15). Magnifications assume an isothermal profile and can be biased for other slopes, especially in the high-magnification tail (p. 12).
- Comparison with machine-learning initialisation (LeMoN, Busillo et al. 2026) suggests combining approaches could raise the success rate (p. 14).

## Known issues, caveats, limitations
- Model assumes one deflector and one source plane, so multi-galaxy lenses (5% of A) and DSPLs are out of scope (p. 6, 10).
- Lens-light subtraction fails for dusty or asymmetric galaxies, edge-on discs (residuals at both ends), and radial profiles rising away from the centre; adding more concentric Gaussians cannot fix this because each component has monotonically decreasing brightness, so a non-parametric light model and explicit dust treatment would be needed; a central point-like component (as in He et al. 2024) is not included, relevant for AGN (p. 10-11, 15).
- Residual segmentation errors remain even in models judged successful (unmasked neighbours, wrongly masked multiple images), limiting use for detailed source reconstruction or complex mass models (Fig. 4, p. 8).
- MER effective PSF may not be sufficient for power-law mass models or radial-slope constraints; authors recommend contacting the Strong Lensing SWG about PSF limitations before fitting more complex models (p. 3).
- Fitting-mask truncation may bias the Sersic half-light radii; "potential biases ... remain unquantified" (p. 12).
- Fitted external shear can absorb unmodelled mass complexity and is not a physical tidal measurement (p. 4).
- A search can stop at its evaluation limit without convergence (p. 5).
- Cutout is only 10 x 10 arcsec, so the model sees only the inner galaxy light within the mask; this suits lenses but not outer profiles.

## Implications for extended-galaxy photometry, 2-D modelling and low-surface-brightness work
- Gives a tested template for 2-D modelling of massive early types in VIS: MGE with two Gaussian sets (bulge-like and disc-like axis ratios and orientations), PSF-convolved with the MER effective PSF, followed by a Sersic refit and then fixed-structure multi-band flux fitting (p. 4-6). The MGE has non-negative amplitudes solved linearly, which stabilises fits (p. 4).
- The explicit failure statistics suggest what to expect for Sersic or MGE fits to galaxies with dust lanes, discs, nuclear AGN or asymmetric light: residual rings and ripples (Fig. 9, p. 11). For bulge-disc work, the authors state future bulge-disc decompositions could follow (p. 15).
- The MER effective PSF is the practical default for VIS modelling in DR1; the authors did not need the SHE PSF for Einstein radii, but flagged limits for high-fidelity modelling (p. 3).
- Mask strategy (zero data, huge RMS, keep pixels) is a useful pattern for neighbouring-galaxy masking in any 2-D fit (p. 3).
- Not relevant to LSB, stellar haloes or ICL: fits are confined to a 10 arcsec cutout and a mask of a few arcsec radius.

## Practical recommendations for users
- Use only models with the SC consensus (7980 systems at 75%) for theta_E and deblended lens photometry; check the secondary flags for failed ones and treat NC as ambiguous.
- Use the Sersic parameters from the VIS fit for lens-galaxy structure but remember mask truncation and single-Sersic limitations; bulge-disc not provided.
- Do not use shear or magnification of high-mu systems as physical quantities without remodelling with a free-slope mass profile.
- For own modelling with VIS data, take the science image, RMS and effective PSF from MER, and consider the same ML segmentation masks (released).
- Contact the Strong Lensing SWG before attempting complex models that depend on fine PSF details.
- Prefer GPU or JAX implementation for large samples; CPU cost per lens is under 5 hours.

## Objects, fields and figures worth revisiting
- Euclid-DR1 J030313.592-580619.97 (RA 45.8066, Dec -58.1055): demonstration lens used for the full preprocessing and model summary, with a neighbouring galaxy to the north-east that is masked (Fig. 1 p. 3; Fig. 2 p. 5). Lens type not stated; grade A SC example.
- No other named systems with coordinates are given in the main text; example panels in Figs. 3-11 and C.1 are anonymous.
- Key figures and tables: Fig. 2 (model summary layout, p. 5); Table 1 and 2 (categories and counts, p. 7-8); Fig. 4 (SC models with residual segmentation problems, p. 8); Fig. 7 (multi-galaxy lenses, p. 10); Fig. 8-10 (segmentation, lens-light and source/mass failures, p. 10-11); Fig. 12-14 (theta_E, theta_eff versus theta_E, magnification, p. 13-14); Table A.1-A.3 (stage parameters, priors, nautilus settings, p. 24-26).

## Cross-references
- ECLIPSE-A (Lines et al.), ECLIPSE-B (Holloway et al.), ECLIPSE-D (Nersesian et al.: multiband photometry from the fixed mass model, photo-z, SED).
- Vincken et al. 2026a (AstroVink-TREX segmentation), Euclid MER paper and Romelli et al. 2026 (effective PSFs), McCracken et al. 2026b (SHE PSF), Wielders et al. (multi-galaxy lenses), Busillo et al. 2026 (LeMoN), Walmsley et al. 2026 (Q1 lens modelling), He et al. 2024 (MGE method), Nightingale et al. 2025 (COWLS-I).
