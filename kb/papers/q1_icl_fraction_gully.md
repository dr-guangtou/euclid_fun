---
title: "Euclid Quick Data Release (Q1). A systematic study of the intracluster light fraction at 0.2 < z < 1.5"
short_name: arxiv_2610.29684
first_author: Gully
series: "arXiv 2610.29684 (Euclid Q1, cluster team ICL)"
local_pdf: ~/Desktop/euclid/papers_extra/arxiv_2610.29684.pdf
local_text: ~/Desktop/euclid/text/papers_extra/arxiv_2610.29684.txt
topics: [ICL fraction, BCG, aperture photometry, rest-frame standardisation, k-correction, cosmological dimming, stacking, PSF deconvolution, photo-z overdensity, BCG identification, Hydrangea, Euclid Q1, LSB]
relevance_extended_galaxies: medium   # method transfer (aperture LSB photometry, PSF-wing test, stacking, systematics) high; science (cluster ICL) low
---

# ICL fraction at 0.2 < z < 1.5 with Euclid Q1 (Gully et al. 2026)

## TL;DR
Using the same bespoke LSB reprocessing of Q1 calibrated frames as the companion shapes paper (B26 pipeline, arXiv:2610.29682), the authors measure BCG (a<50 kpc), ICL (50-200 kpc) and satellite light in 66 SPT SZ-selected and 269 Euclid-selected clusters (36 in common) at 0.2<z<1.5, and compare with Hydrangea mocks. ICL is detected in individual massive clusters (M500 >~ 10^14.2 Msun) to z~1.5 (70-80% detection in confirmed clusters); the BCG-to-ICL fraction f_diff ~ 40% and total f_tot ~ 20% are constant with z at fixed mass. For a galaxy-photometry user the paper is mostly a source of tested methodology and quantified systematics: fixed-aperture BCG/ICL split, empirical blank-sky error budget with covariance, rest-frame interpolation across bands, PSF-wing deconvolution test, robustness to background scale, inner-split radius, stacking estimator and wavelength, and the finding that selection (low S/N, misidentified BCGs) can mimic redshift evolution.

## Key facts and numbers
- Q1 coverage: EDF-N ~23 deg2, EDF-S ~28 deg2, EDF-F ~12 deg2 (p. 2). Bands IE (VIS), YE, JE, HE (NISP) (p. 2).
- Depth after B26 reprocessing: ~27.5 mag/arcsec^2 in YE, JE, HE and ~29 in IE on scales of several arcmin (p. 2). (Limiting-SB definition lives in B26 and in Kolcu et al.: 3 sigma of SB fluctuations in random elliptical apertures after masking and background removal.)
- Samples: SPT-3G SZ catalogue (Archipley+26; 57 deg2 overlap with EDF-S, 217 clusters, 121 in EDF-S); BCGs identified in 81/121; Euclid AMICO+PZWav joint catalogue (Bhargava+26), 426 clusters, BCGs in 303; after visual checks and removing 47 clusters affected by very bright stars or poor imaging: 66 SPT + 269 Euclid, 36 common (347 unique before cuts) (p. 2-3, 19).
- Hydrangea: 181 mass-matched clusters (12 unique haloes at multiple snapshots), 3 projections each = 543 mocks, 0.3 arcsec/pix, within 3 r200; mock images in rest-frame IE (p. 3).
- Aperture definitions (p. 4): BCG = flux within elliptical aperture a<50 kpc; ICL = annulus 50<a<200 kpc; galaxy light within a<200 kpc. f_diff = F_ICL/(F_BCG+F_ICL); f_tot = F_ICL/(F_BCG+F_ICL+F_gal) (p. 7-8).
- Detection rates (ICL S/N>3 in 50-200 kpc): 83% (30/36; 92% at S/N>2) for clusters in both catalogues; SPT 71% (88% at S/N>2); Euclid 54% (68%). Euclid fraction with S/N<2 rises from 5% (z<0.5) to 56% (z>0.8) (p. 6).
- Stacks: SPT in 3 z bins (0.20-0.58, 0.58-0.95, 0.95-1.46; 20/20/21 clusters), Euclid 5 bins of 51-52; high-S/N Euclid (excluding individual S/N<2) 5 bins of 35-36; low-S/N Euclid 4 bins of 19 (p. 5, 7). Richness>150 (13 clusters) and 5 SPT clusters with logM500>14.6 excluded (p. 5).
- Results (rest-frame IE, 0.71 micron): f_diff SPT 36-38% (quoted 37-40% range in text), Euclid full 32-36%, Euclid high-S/N 37-43%; f_tot SPT 15-21% (text: 16-22%), high-S/N Euclid 17-21%, full Euclid declining 20% -> 12% with z (constant model rejected at 3.3 sigma, driven by low-S/N systems; low-S/N stacks have f_tot only 1-7%) (p. 7-8, Table D.1 p. 22). Constant-with-z hypothesis: SPT f_diff consistent; high-S/N Euclid 1.8 sigma (p. 7-8). Individual clusters: f_diff 20-60%, f_tot 10-30% (p. 10).
- Luminosities nearly constant with z for BCG and ICL, satellites fade with decreasing z (passive evolution); simulations: ICL 0.2-0.3 dex brighter than SPT stacks, BCG within ~0.1 dex, satellites ~0.3 dex fainter at low z; sim f_diff 45-55% (p. 5-8). L_sun in IE = 53.40 Jy (Table D.1 note, p. 22).
- Outer-radius test (p. 9): f_diff rises monotonically and flattens near ~300 kpc; f_tot rises to ~200-300 kpc and is flat within errors between 200 and 600 kpc; analysis truncated at 600 kpc because the background box is 1 Mpc. 200 kpc ~ 0.35 R500 at z=1.11 and ~240-280 kpc-equivalent scaling at lower z; scaled vs fixed apertures give consistent results.
- Inner BCG/ICL split tested at 30, 50, 80 kpc: normalisation changes systematically but redshift trend unchanged (p. 9).
- Wavelength dependence (App. C, p. 20-21): relative to the 0.71 micron reference, fractions drop ~15% by ~1.2 micron, flat down to ~0.5 micron, rise at shorter wavelengths (driven by two highest-z bins); same in f_diff and f_tot, so not due to satellites but to differing BCG vs ICL stellar populations.
- PSF deconvolution (App. B, p. 19-20): fluxes change by <=+/-1% within 50-200 kpc; only the innermost region is affected (light moved back to the centre).
- Masking incompleteness: residual light from galaxy haloes biases ICL flux by ~10% (cited from B26, p. 4 footnote).

## Data products and data model
- Images: custom LSB-optimised IE/YE/JE/HE mosaics built from Q1 LE2 calibrated single exposures via B26: atemporal background correction, removal of a "tartan" pattern and persistence in NIR, resampling to 0.3 arcsec grid, per-detector background matching, weighted-mean combine (p. 2). Also uses RMS noise maps to define valid pixels (p. 17).
- Euclid catalogues: OU-PHZ photometric-redshift PDFs and physical properties (Tucci+26, Q1), MER columns for selection and flux: mer.det_quality_flag (>3 excluded from photo-z stacks), mer.spurious_flag (>0 excluded), phz.phz_flags (>0 excluded), mer.mumax_minus_mag (> -2.6, compactness/star-galaxy cut), mer.flux_h_sersic (HE single-Sersic total flux used to pick the BCG), Kron radius (BCG must exceed median Kron radius of members), and single-Sersic fluxes in all four bands for galaxy light (p. 4, 17-18). Flagged objects were kept for the association scores because obvious BCGs were sometimes removed by these flags (p. 17).
- Cluster catalogues: SPT-3G (Archipley+26); Euclid AMICO/PZWav joint catalogue (Bhargava+26); redshifts and BCGs re-derived in-house (Fig. A.3 p. 19).
- Simulations: Hydrangea (EAGLE-based); Subfind + Cantor satellite assignment (p. 3).
- Derived: per-cluster BCG/ICL/galaxy luminosities, S/N, f_diff, f_tot; stack table (Table D.1, p. 22).

## Processing and methods
1. Redshift and BCG identification (App. A, p. 17-19): stack galaxy photo-z PDFs weighted by a Gaussian in angular separation (sigma 1 arcmin initially), normalise by effective area from a convolved valid-pixel mask, subtract the mean of 500 random-region stacks and divide by their scatter (Sigma(z)); take the most significant region with Sigma>2 and fit a Gaussian for z and its error. Association score M_i = w_i * integral G(z) P_i(z) dz (a ranking, not a probability). BCG = brightest HE-Sersic-flux galaxy with M_i>0.5 and large Kron radius. Second iteration re-weights with a physical radial scale (R_scale ~0.5 R200, from SPT masses via zeta-mass relation of Benson+13/Bleem+24, RANSAC linear fit to z for Euclid clusters) re-centred on the BCG; accept only if consistent after recentring (up to ~3 rounds). 18 of 347 BCGs were visually found misidentified (low M_i from broad photo-z PDFs) and reselected by hand.
2. Background (p. 4): photutils Background2D on source-masked images, box = 1 Mpc at cluster z, 3x3 median filter.
3. Masks (p. 4): bad-pixel, regular objects (grown to 150% of size) outside the ICL zone, central compact objects (grown to 125%); separate for IE and YJHE.
4. Isophotes (p. 4): AutoProf on masked HE images (HE gives highest ICL S/N, per Kolcu+), BCG-centred fixed, PA/e free per isophote via Fourier analysis, fitted out to 1 sigma background level then frozen. Profiles in all filters extracted on the HE isophotes using sigma-clipped median per annulus, times area for flux; cumulative flux profile interpolated for apertures.
5. Error budget (p. 4): blank-sky patches 2.5 x 2.5 deg per EDF, 1000 random pointings with ellipticity 0.5, same masking and background treatment; annular fluxes cumulated, 1 sigma from sigma-clipped scatter; covariance across apertures from the ensemble propagates into f_diff and f_tot.
6. Galaxy light (p. 4-5): sum single-Sersic fluxes of all sources with M_i>1% inside the 200 kpc aperture, minus a per-cluster contamination estimate from 1000 field analogues with the same z and spatial selection (median and 16-84% as value and error). In simulations the satellite-only images are summed inside the BCG+ICL a=200 kpc isophote. Test: adding 5 kpc to the sim aperture changes galaxy flux by ~0.01 dex (p. 6 footnote).
7. Stacking (p. 5): images rotated so the HE-isophote PA interpolated at 100 kpc is horizontal; no rescaling by R500; 100 bootstrap resamplings of clusters; pixel-wise median (3-sigma-clipped mean gives same conclusions); weight map = fraction of valid pixels, pixels with weight <25% excluded; BCG/ICL apertures re-derived from stack isophotes; galaxy light from the stack aperture applied to each member cluster, median across clusters; stack noise = max single-cluster noise per band divided by sqrt(N), propagated to rest-frame IE (p. 6 footnote).
8. PSF deconvolution (App. B): empirical PSF from stacked stellar profiles (Cuillandre+25) per band, many sub-pixel-shifted realisations stacked in the same way as the clusters, unsupervised Wiener deconvolution (Orieux+10) on each bootstrap stack; not applied to individual clusters (noise too high) (p. 19-20).
9. Rest-frame standardisation (p. 5): linear interpolation, component by component (BCG, ICL, members), of the observed-band fluxes to the rest-frame IE wavelength 0.71 micron, then luminosity via Hogg+02. Effectively a band-interpolating k-correction with no template SEDs.

## Validation and performance
- Highest-purity test: the 36 clusters detected by both SZ and Euclid; 83% show ICL at S/N>3 (p. 6).
- Low-S/N stacking test: stacking 19 Euclid clusters at a time with individual S/N<2 recovers no significant ICL at z>~0.6 (S/N<2), and S/N~5 at lowest z, vs S/N 25-70 for SPT stacks of similar N (p. 7) -- these are likely misidentified BCGs, groups, projections or genuinely weak ICL.
- Robustness: results insensitive to stacking estimator (median vs clipped mean), outer radius (200-600 kpc), inner split (30/50/80 kpc), fixed vs R500-scaled aperture, PSF deconvolution (<1%), and BCG offset (no correlation of ICL fraction with BCG-centre offset) (p. 5, 8-9, 20).
- Simulation comparison: sims reproduce trends (constant fractions) but offsets in normalisation (ICL +0.2-0.3 dex) that cannot be attributed between sim, observation and mock-construction assumptions (SPS, IMF, dust) (p. 6).

## Known issues, caveats, limitations
- Sample not representative: quality cuts and BCG identification reduce samples relative to parents; results apply to clusters with robust BCG ID and ICL measurement (p. 3). Euclid sample lacks individual masses, so mass-matching with SPT cannot be tested (p. 7).
- Selection biases: excluding low-S/N systems makes f_diff and f_tot look higher and flatter; including them makes f_tot fall with z (3.3 sigma) -- a spurious evolution signal (p. 8).
- Pipeline-specific: photo-z biases cause misidentified BCGs (18/347); automated flags (mer.det_quality_flag, spurious_flag) can remove real BCGs (p. 17-19).
- Aperture biases: galaxy flux in observations is biased high because members just inside the 200 kpc aperture contribute their full flux (negligible, ~0.01 dex) (p. 6).
- Background scale of 1 Mpc limits reliable ICL measurement beyond ~600 kpc; measurements near that scale depend on background subtraction (p. 9).
- BCG/ICL separation has no unique physical radius; literature uses 30, 50 or ~80 kpc, so absolute fractions are not comparable across papers; wavelength differences also shift fractions by ~15% (p. 9-10, 20).
- Residual masking of galaxy haloes biases ICL flux by ~10% (B26) (p. 4).
- ICL fractions measured at different rest-frame wavelengths are not directly comparable (p. 10).
- Q1 only: single reference observing sequence; ICL products are not standard Q1/DR1.

## Implications for extended-galaxy photometry, 2-D modelling and low-surface-brightness work
- Concrete tested numbers for LSB fixed-aperture photometry in Euclid: ~27.5 (NIR) / ~29 (IE) mag/arcsec^2 3 sigma on arcmin scales; empirical blank-sky random-aperture noise with covariance is the preferred error budget (background-structure dominated) rather than Poisson.
- Non-parametric BCG/diffuse split: choose and quote a physical radius, then test 30/50/80 kpc; for galaxy outskirts the analogue is bulge/disc or inner/outer splits whose normalisation, not trend, changes.
- Cosmological dimming and band shift: measure at a fixed rest-frame wavelength by interpolating among Euclid bands (IE, YE, JE, HE span rest 0.5-1.2 micron to z~1.5); the band choice alone shifts fractions by ~15%, important for colour-dependent outskirt studies.
- PSF wings: Wiener-deconvolving stacks with empirical extended-PSF stack changes flux by <1% at 50-200 kpc scales in the HE band, so wings are a minor issue at such radii in NIR for stacks, but light is moved from the centre inwards; for single faint galaxies deconvolution is too noisy.
- Stacking: rotating to a common PA, pixel-wise median, valid-pixel weight maps with a 25% cutoff, and bootstrap over objects is a reproducible recipe for faint outskirts of a galaxy population.
- Use satellite/neighbour contamination subtraction from field analogues rather than hard membership cuts when summing component light; the same idea applies to subtracting neighbour light in galaxy outskirts.
- Ground-truth with mocks: Hydrangea mocks (particle SEDs through IE, PSF-convolved) give particle-level BCG+ICL vs satellite decomposition unavailable in data; similar decomposition could validate Sersic/bulge-disc plus halo fits.
- Selection-induced pseudo-evolution is a general warning for any redshift-dependent LSB measurement.

## Practical recommendations for users
- Do: define apertures physically and test alternative split radii; build errors from blank-sky random apertures with covariance; use median-in-annulus rather than mean to resist leakage from masks; estimate sky on masked images with a box much larger than the target (1 Mpc here); interpolate to a fixed rest-frame band; report both full-sample and high-S/N subsample results; visually inspect centre/BCG identification.
- Do not: trust automated photo-z-based BCG/centre selection without checks; compare diffuse-light fractions across studies with different aperture, band or depth; extend measurements beyond about 60% of the background box scale.
- Useful columns: mer.flux_h_sersic and single-Sersic band fluxes, Kron radius, mer.det_quality_flag, mer.spurious_flag, phz.phz_flags, mer.mumax_minus_mag, OU-PHZ PDFs (Q1 names as given in the paper; check DR1 naming).
- These LSB mosaics are bespoke (B26) and may not exist in DR1.

## Objects, fields and figures worth revisiting
- Fields: EDF-N, EDF-S, EDF-F (Q1). SPT-3G 57 deg2 region overlapping EDF-S. No individual named clusters with coordinates are given in the main text.
- Figures: Fig. 1 (mass-z of samples, p. 3), Fig. 2 (rest-frame IE luminosities of BCG/ICL/galaxies vs z, p. 6), Fig. 3 (ICL S/N and S/N<2 fraction vs z, p. 7), Figs. 4-5 (f_diff and f_tot vs z, p. 8), Fig. 6 (radial dependence of fractions, p. 9), Fig. A.1-A.3 (photo-z overdensity and BCG identification, p. 18-19), Fig. B.1 (deconvolution test, p. 20), Fig. C.1 (wavelength dependence, p. 21), Table D.1 (stack properties, p. 22).

## Cross-references
- arXiv:2610.29682 (Bamford et al. 2026, B26): pipeline, Appendix B ICL workflow, masking tests.
- arXiv:2610.29683 (Kolcu et al. 2026): ICL shapes; HE band best for ICL S/N.
- Euclid Collaboration: Bellhouse et al. 2025 (aperture optimisation 50/200 kpc); Bhargava et al. 2026 (Q1 cluster catalogue); Tucci et al. 2026 (OU-PHZ); Cuillandre et al. 2025 (extended PSF); Golden-Marx et al. 2026 (ICL colours); Fernandez et al. 2026; Brown et al. 2026; Martin et al. 2026 (ICL origin in simulations).
