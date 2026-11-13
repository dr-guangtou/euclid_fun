---
title: "Euclid Quick Data Release (Q1). The shape of cluster haloes revealed by intracluster light"
short_name: arxiv_2610.29683
first_author: Kolcu
series: "arXiv 2610.29683 (Euclid Q1, cluster team ICL)"
local_pdf: ~/Desktop/euclid/papers_extra/arxiv_2610.29683.pdf
local_text: ~/Desktop/euclid/text/papers_extra/arxiv_2610.29683.txt
topics: [ICL, BCG, isophote fitting, AutoProf, ellipticity, position angle, low surface brightness, masking, background subtraction, stacking, Hydrangea forward modelling, Euclid Q1, band choice]
relevance_extended_galaxies: medium   # method transfer (LSB isophotes, masking, background, mock injection) high; science (cluster haloes) low
---

# Cluster ICL halo shapes with Euclid Q1 (Kolcu et al. 2026)

## TL;DR
The paper measures radius-dependent ellipticity and position angle (PA) of the BCG+ICL light for 205 clusters at 0.1 <= z <= 0.8 in Euclid Q1, using a special low-surface-brightness (LSB) reprocessing of the calibrated single-exposure frames (pipeline of companion paper B26, arXiv:2610.29682) and non-parametric AutoProf isophote fitting. Individual clusters give reliable shapes only out to about 0.1 R200c (~100 kpc) for 63% of the sample; stacking pushes ellipticity to 0.3-0.4 R200c and surface brightness to 0.6-0.8 R200c. For a galaxy-imaging user the science result (ICL ellipticity ~0.5, matching lensing) matters less than the transferable method: masking recipe tested on mocks, 1-Mpc-box background, shape-parameter regularisation at low S/N, band choice (HE best at z>0.2, IE at z<0.2), 3-sigma limiting-SB definition, and forward-modelled simulation comparison that shows masking itself biases isophote shapes.

## Key facts and numbers
- Sample: 205 clusters, 0.1 <= z <= 0.8, 10^14 <= M200c/Msun <= 10^15.2; 76 from eRASS1 (M200c >= 1e14) plus 174 DES Y3 redMaPPer overlapping Q1, cross-matched on BCG position within 10 arcsec; masses converted M200m/M500c -> M200c with Colossus, NFW + Duffy+08 concentration (p. 2-3). Flat LCDM H0=70, Om=0.3 (p. 2).
- Fields used: EDF-S and EDF-F (p. 3). Bands IE (VIS), YE, JE, HE (NISP) and a coadded YJHE weighted by bandwidth (p. 3).
- Pixel grid: VIS native 0.1 arcsec resampled to NISP 0.3 arcsec/pix; per-cluster coadds of 0.5 x 0.5 deg (p. 3).
- Limiting surface brightness (definition): 3 sigma of the SB fluctuations measured in elliptical apertures at ~1000 random positions in 2.5 x 2.5 deg regions of each Q1 field, after source masking and large-scale background subtraction; on scales of several arcmin this is ~27.5 mag/arcsec^2 in YE, JE, HE and ~29 in IE (p. 5). Example cluster: R3sigma ~350-500 kpc, ~27.5 (HE, YJHE) and ~28.7 (IE) (p. 5).
- R3sigma (radius where spline-fitted BCG+ICL profile hits the 3 sigma noise curve) ranges from ~25 kpc to >400 kpc in HE; weak anti-correlation with z (Pearson r=-0.27; Spearman -0.28) and positive with mass (r=0.30; rho=0.23) -- the z trend attributed to cosmological dimming (p. 7). At z~0.2, logM~14.2: 150-250 kpc; z~0.3-0.4, logM~14.5: 300-400+ kpc; z~0.7 similar mass: <150 kpc (p. 7).
- Band comparison: mean Delta R3sigma relative to HE: IE -7.9 kpc, JE -6.3 kpc, YE -30 kpc (worst; zodiacal light ~1 micron plus faint ICL), YJHE +1.8 kpc (p. 6). HE-IE difference correlates with z (Pearson r=0.31, p=1e-5); crossover near z~0.2 (16-84%: 0.07-0.26), so IE better at z<0.2, HE at higher z (p. 6). ICL is red, IE-HE ~1.5 (cited from Golden-Marx+2026) (p. 12).
- Shape radius Rshape (outermost radius with robust ellipticity/PA): measurable to 0.1 R200c for 63% (130/205) of clusters; ~6% beyond 0.2 R200c; completeness >=80% at low/intermediate z, ~60% at z>~0.6 (p. 5, 7).
- ICL ellipticity at 0.1 R200c: median 0.513, mean 0.489+/-0.01, sigma ~0.179; 9% have e<=0.2, 26% have e>=0.6 (34 clusters, of which 15 affected by residual systematics) (p. 7). Agrees with lensing: Okabe+20 0.482+/-0.028 (39 strong-lens clusters), Oguri+10 0.46+/-0.04, Cui+25 median ~0.52 (299 HSC redMaPPer clusters) (p. 7).
- Radial trend: BCG-dominated core e ~0.15-0.2, rising to >0.5 by 0.1 R200c; PA offset from BCG PA (at 10 kpc) ~5 deg in BCG region, ~10 deg near 0.1 R200c, <~20 deg for 75% of clusters, i.e. a stretch with little twist (p. 9-10).
- Stacks (163 clusters with 1-3e14 Msun, bins 0.1-0.3, 0.3-0.4, 0.4-0.6, 0.6-0.8 with 31/39/41/52 clusters): ICL above 3 sigma to ~0.8 R200c (~800 kpc) in two bins, ~0.55-0.6 R200c (~600 kpc) in the others; ellipticity traced beyond 0.3 R200c (300-400 kpc); stacked e plateaus at 0.40-0.45 beyond 0.1 R200c, no redshift dependence (p. 10).
- ICL-BCG PA alignment: median ~11 deg, 45% within 10 deg, 87% within 30 deg (130 clusters). ICL-satellite alignment: median 22 deg, 28% within 10 deg, 61% within 30 deg, but only 57 clusters (~30%) have satellite PA uncertainty <30 deg (p. 12). Mean 19 members within 500 kpc of BCG (p. 11-12).
- Hydrangea comparison: 86 unique clusters at z=0.2,0.4,0.5,0.7 in 3 projections = 636 mocks; 542 (85%) yield robust shapes after forward modelling vs 63% observed (sim ICL brighter than real) (p. 8). Mean e: observed 0.49, forward-modelled 0.43 (KS D=0.27, p=2.9e-7), noiseless unbound-ICL 0.24 (p. 8-9).

## Data products and data model
- Started from Q1 Level-2 (LE2) single-exposure, flat-fielded, astrometrically and flux-calibrated frames from the VIS and NISP SGS pipelines (not the standard Q1 MER mosaics), reprocessed with the B26 LSB pipeline: removal of residual atemporal background signals, correction of time-dependent artefacts, subtraction and masking of NIR charge persistence, resampling to 0.3 arcsec, detector-level background matching, coadding (p. 3). Full description deferred to B26 (arXiv:2610.29682); the products are custom, not in Q1/DR1.
- External catalogues: eRASS1 cluster and member catalogue (Bulbul+24, Kluge+24; erass-cluster-inspector.com), DES Y3 redMaPPer clusters and members with P_mem (p. 2, 11). No Euclid MER catalogues are used in this paper.
- Outputs defined: per-band AutoProf elliptical profiles (SB, ellipticity, PA vs semi-major axis), Rshape, R3sigma, stacked images aligned by ICL PA (p. 4-5, 10).

## Processing and methods
1. BCG centring (p. 3): cutout around catalogue BCG; sigma-clipped median background on 10x10 pixel mesh (3x3 filter); photutils detect_sources + deblend; pick the nearest segment, then centroid vs brightest pixel (brightest pixel usually preferred after visual check). Needed because ground-based catalogue centres blend multiple nuclei; offsets typically a few pixels.
2. Two-zone source masking (p. 3-4):
   - BCG+ICL region: adaptive Gaussian smoothing (sigma_s up to 20 pix), detection at 2x background noise (noise in 300-pixel box); region dilated to cover the diffuse light (typically ~100-150 kpc). Compact sources inside it found by median-filtering (scale 0.25 sigma_s), detecting at 2 sigma, aggressively deblending, then growing each (except BCG) by 25%.
   - Outside: Gaussian smoothing sigma = 1 pix, detect at 3x noise (500-pixel box), >=5 pixels, photutils deblending, masks expanded by 50% to cover extended galaxy haloes.
   - NIR bands share one mask derived from YJHE; IE is masked independently. All choices tuned on mock simulated clusters (details in B26).
3. Global background (p. 4): masked image, boxes of 1 Mpc at the cluster redshift, 3x3 filtering, so background comes from >=1 Mpc from the BCG; then BCG+ICL mask is removed.
4. Isophote fitting with AutoProf (Stone+21) (p. 4-5): centres fixed on BCG; ap_set_background set to 0 to avoid a second subtraction/over-subtraction; semi-major axes start at 1 pixel and step by 0.15 dex; ellipticity (e=1-b/a) and PA free per isophote via Fourier analysis (second mode), with a regularisation that penalises jumps between neighbouring isophotes; fit extends to where per-pixel S/N ~1; beyond Rshape the shape is frozen and photometry continues on frozen isophotes.
5. Cross-band consistency (p. 5): all bands measured on the same isophotes taken from the coadded YJHE image; SB = median pixel value in each elliptical annulus after masking.
6. Uncertainties (p. 5): SB error = MAD-scaled 1-sigma scatter in annulus, background term dominates at large radius, Poisson only in the BCG core, added in quadrature. Ellipticity/PA errors from MAD of (measured - true) for mock clusters (B26). R3sigma from a weighted cubic UnivariateSpline in log radius fitted to points above 3 sigma, with 1000 bootstrap perturbations (16-84%).
7. Stacking (p. 10): background-subtracted, masked images rotated to align the ICL PA at 0.1 R200c (or at the outermost measurable radius for 75 clusters), mean with 3-sigma clipping, equal weight, no rescaling by R200c in the quoted description; AutoProf on stack; noise from the EDF-S noise profile (1 Mpc box at mid-bin z) divided by sqrt(N); ellipticity errors by bootstrapping clusters.
8. Satellite shape tensor (p. 11-12): P_mem-weighted second-moment tensor of members within an iteratively updated elliptical aperture starting at 500 kpc; iterate until axis ratio changes <0.5%; bootstrap errors (1e5 resamples); keep PA error <30 deg. PA differences folded to [0,90] deg.
9. Hydrangea forward model (p. 8): star particles with SEDs through Euclid HE curve, mass-loss corrected, smoothed before projection, convolved with extended HE PSF (Cuillandre+25), injected into random real Euclid sky patches (so real noise, gradients, artefacts), then processed identically (mask, background, AutoProf). A noiseless "unbound-ICL" version (Subfind-unbound only) isolates the true ICL.

## Validation and performance
- Mock tests on simulated clusters validate masking aggressiveness vs over-masking of ICL (details in B26) (p. 4).
- Inter-band checks: ellipticity at 0.1 R200c relative to HE has median offsets -0.02 to -0.05; ~90% of clusters within +/-0.3; the other ~10% are driven by residual systematics (imperfect masks of foreground stars and diffraction spikes, extended haloes of bright members) (p. 7).
- Forward-modelled Hydrangea reproduces the BCG-to-ICL ellipticity rise and PA twist but is rounder at large radii and ~0.05 more elliptical at the BCG; the transition is more gradual (p. 9-10).
- Stacked vs individual: stacks are rounder (0.40-0.45 vs ~0.5) because of PA misalignment before stacking and extra background homogenisation (p. 10).

## Known issues, caveats, limitations
- Rshape < 0.1 R200c for 75 clusters (37%): shapes there only measured where ICL overlaps the BCG; these are dropped from most analyses (p. 5). Completeness falls to ~60% at z>~0.6 (p. 5).
- Residual masking systematics (stars, spikes, bright-member haloes) bias ellipticity and differ per band; they inflate the high-e tail (15 of 34 e>=0.6 clusters) (p. 7).
- Masking bias: satellite masking leaves weakly bound outer-satellite stars in the "ICL", making measured ellipticity systematically higher than that of the truly unbound ICL (0.43 vs 0.24 in mocks); so measured ICL e is likely biased high relative to the dark-matter halo, and simulations must be forward-modelled with the same masking to be compared (p. 8-9).
- Simulation sample has only 86 unique clusters; sim ICL is brighter than observed (p. 8).
- YE is the least sensitive band (zodiacal light near 1 micron) (p. 6); IE is deeper (29 vs 27.5 mag/arcsec^2) but ICL is red so HE traces further at z>0.2.
- Cosmological dimming suppresses R3sigma at higher z (p. 7).
- Fixed fractional-radius shape (0.1 R200c) vs lensing's global projected shape is not a like-for-like comparison (p. 8). No redshift evolution detected, probably limited by number of clusters per bin (p. 10).
- Isophote shapes inside 2 x PSF FWHM are excluded from radial-profile statistics (p. 9). No explicit PSF-wing scattered-light correction is applied for the shape analysis beyond using the PSF in mocks (see Gully paper for deconvolution of stacks).

## Implications for extended-galaxy photometry, 2-D modelling and low-surface-brightness work
- Transferable recipe for any LSB outskirt measurement: starting from calibrated single exposures with custom background/persistence handling gives ~27.5 mag/arcsec^2 (3 sigma, several-arcmin scales, NIR) and ~29 (IE); the standard MER mosaics are not the starting point here, so this depth should not be assumed for DR1 products without a similar reprocessing.
- Limiting SB should be quoted with scale and confidence: here 3 sigma on several-arcmin scales from random-aperture fluctuations after masking and background subtraction (not pixel-level noise). Large-scale background inhomogeneity, not Poisson noise, sets the outer limit.
- Use a two-zone mask (aggressive growth of faint detections outside the target region, light growth (25%) of compact sources inside it) and calibrate growth factors on mocks; check stability of shape between bands as a systematics diagnostic (inconsistencies flag masking failures).
- Estimate the background on a scale much larger than the target (1 Mpc; for galaxies use a few times R_max) on masked images, set the profile fitter's own background to zero to avoid double subtraction.
- For isophotal shapes at low S/N, regularise ellipticity/PA between adjacent isophotes, log-spaced semi-major axes (0.15 dex), freeze shape beyond the last reliable radius (Rshape), and report both.
- Ellipticity/PA error bars should come from injection-recovery on mocks in real Euclid sky, not from formal fit errors.
- Forward-model any simulation comparison with the same masking; otherwise tidal/halo components are misattributed (mask-defined "diffuse" light is more elongated than unbound light).
- Band choice: for red diffuse light (ICL, old stellar haloes) HE or YJHE reaches furthest at z>~0.2, IE only at very low z; YE is worst. For bluer tidal features or LSB discs IE depth may win; test per object.
- Stacking aligned by PA recovers outskirts to ~0.6-0.8 R200c-equivalent but dilutes ellipticity if PA estimates are noisy.

## Practical recommendations for users
- Do: build cutouts from calibrated frames with persistence and atemporal background handled if outskirts below ~27 mag/arcsec^2 matter; mask in two zones; estimate sky on masked large boxes; fit isophotes with regularisation; quote R3sigma/limiting SB with its definition; check shape consistency across IE/HE/YJHE; inject mocks into real sky to calibrate biases.
- Do not: trust isophote shapes beyond Rshape; interpret ellipticity inside 2 x PSF FWHM; use YE as the primary band for faint diffuse light; compare observed diffuse-light shapes to simulations without matching the masking.
- Do not assume Q1/DR1 pipeline mosaics reach these depths; these are bespoke B26 products.

## Objects, fields and figures worth revisiting
- Example cluster 1eRASS J040508.4-464833: z=0.37, M200c=8.8e14 Msun, R200c ~1490 kpc; approx. RA 61.285, Dec -46.809 (converted from the name; not stated in degrees in the paper) (p. 4-5, Fig. 2 p. 4).
- Fields: Euclid Deep Field South (EDF-S) and Fornax (EDF-F) (p. 3). No other named objects with coordinates.
- Figures: Fig. 1 (sample vs R3sigma, p. 3), Fig. 2 (images, masks, AutoProf contours, PA/e/SB profiles, p. 4), Fig. 3-5 (band comparisons, p. 6), Fig. 6 (Rshape/R200c, p. 7), Fig. 7 (ellipticity vs lensing and Hydrangea, p. 8), Fig. 8 (radial shape profiles, p. 9), Figs. 9-10 (stacks, p. 11), Fig. 11 (alignment, p. 12).

## Cross-references
- arXiv:2610.29682 (Bamford et al. 2026, "B26") LSB pipeline, mask testing, mocks and noise profiles.
- Euclid Collaboration: Bellhouse et al. 2025 (ICL detection model, figure 12 trend); Golden-Marx et al. 2026 (ICL colours); Gully et al. (arXiv:2610.29684, ICL fraction); Fernandez et al. 2026 (simulated ICL shapes); Cuillandre et al. 2025 (extended PSF); Q1 overview (Aussel et al. 2026), VIS (McCracken+26), NISP (Polenta+26).
- DR1 shear maps proposed for calibrating ICL shape vs dark-matter shape (p. 9).
