---
title: "Euclid Data Release 1 (DR1): Pushing back the borders of the invisible with Euclid. Discovery of fifteen resolved low-surface-brightness stellar systems from the Milky Way to the Local Volume"
short_name: gatto
first_author: Gatto
series: A&A Special Issue DR1-Foundation (Nov 2026)
local_pdf: ~/Desktop/euclid/papers/gatto.pdf
local_text: ~/Desktop/euclid/text/papers/gatto.txt
topics: [low surface brightness, resolved stars, isochrone filter, ultra-faint dwarfs, Local Volume dwarfs, M81 group, TRGB distances, MER catalogue, POINT_LIKE_PROB, star counts, globular clusters]
relevance_extended_galaxies: medium   # LSB discovery by resolved star counts, not integrated-light photometry; useful as demo targets and for MER star/galaxy flags
---

# Resolved LSB stellar systems from the Milky Way halo to the Local Volume in DR1 (Gatto et al. 2026)

## TL;DR
The authors search the roughly 1900 deg2 of the Euclid Wide Survey in DR1 for overdensities of resolved stars using a colour-magnitude isochrone filter on the MER catalogue, over distances of 10 kpc to about 4 Mpc. They report 15 systems: 5 new (3 Milky Way halo ultra-faint stellar systems, 2 dwarfs beyond the Local Group at about 4 Mpc) and 10 previously catalogued but unresolved dwarfs, now resolved into stars and given first distances, sizes and masses. The detection is by star counts, not by integrated-light surface brightness, so this is not a photometry-pipeline paper, but it shows what DR1 reaches in surface brightness (mean mu_V within r_h of about 27-31 mag/arcsec2 for resolved systems) and gives a list of faint, diffuse, nearby targets that are good demonstration objects for LSB tools.

## Key facts and numbers
- Data: DR1 Euclid Wide Survey, about 1900 deg2; 5 sigma point-source depths IE=26.7, YE=JE=HE=24.4 (p. 2).
- Final EWS is about 14 000 deg2 (about 7 times DR1 area); expected yield by end of mission: about 15 new MW-halo systems, about 15 Local Volume dwarfs, plus the about 10 M81-group systems, so at least about 40 (p. 12-13).
- Star selection: POINT_LIKE_PROB > 0.05 (conservative, purity above 80 percent at all magnitudes) (p. 2); then a polygon cut in the dereddened (IE-HE) vs (YE-HE) colour-colour plane, vertices (-1.5,-1.5), (-1.5,-0.4), (0.9,0.8), (1.4,0.8), (1.4,-0.4), (0.9,-0.4) (p. 2, Fig. 1).
- Extinction: Planck reddening maps converted with R_IE=2.28, R_YE=1.14, R_JE=0.79, R_HE=0.51 (R_V=3.1; Cardelli+O'Donnell law via PARSEC) (p. 2).
- Isochrone filter: PARSEC, log10(t/yr)=10.12 (about 13 Gyr), [Fe/H]=-2.2; selection in HE vs (IE-HE) within 0.05 mag in colour, added in quadrature to the propagated colour error; 27 distance moduli, 15 <= (m-M)0 <= 28 in 0.5 mag steps (p. 3).
- Density maps: 30 arcsec pixels, Gaussian smoothing bandwidth 1 arcmin; significance S = (N - N_bkg)/sigma_bkg with background from an annulus of 6 to 15 arcmin radius (p. 3).
- Recovery test: of 42 known galaxies/ambiguous objects with (m-M)<28 in the DR1 footprint (Pace 2025 catalogue), 37 recovered (about 88 percent); 100 percent within about 3.6 Mpc; about 55 percent beyond 3.6 Mpc and fainter than M_V about -11.85. Smallest recovered: M_V about -8.1 (dw0944+69); most distant recovered: DDO 165 at (m-M)=28.42 (p. 3).
- Structural fits restricted to IE <= 25.7 (1 mag brighter than 5 sigma depth); LVDw DR1 12 needed IE <= 26.2 (p. 7-8).
- TRGB calibration used: M_TRGB(IE) = -3.30 +/- 0.05 (SMC-anchored, Bellazzini and Pascale 2024) (p. 5).
- M_V = M_IE + 0.3 for old metal-poor systems (p. 9). Stellar masses from synthetic CMDs of a 10^6 Msun PARSEC population, Kroupa IMF, 10 000 Monte Carlo realisations (p. 8).
- Surface-brightness regime of the sample (mean mu_V within r_h): Ursa Minor II about 31; LVDw DR1 2 about 28.3, LVDw 9 about 28.5, LVDw 5 about 27.9, LVDw 1 about 27.4; the 11 systems beyond the Local Group span 25.0 to 28.5 mag/arcsec2, -11.3 <= M_V <= -7.3, 135 <= r_1/2 <= 380 pc, M* of 1e5 to 4e6 Msun (p. 9-11). Three reach or exceed mu_V = 28 mag/arcsec2, which no galaxy at 1-6 Mpc in the Pace 2025 compilation exceeds (p. 11); NGC253-SNFC-dw1 at 29.4 is a known counter-example not in that compilation (p. 11).

## Data products and data model
- Search catalogue: MER catalogue, template-fitting photometry (IE, YE, JE, HE), column POINT_LIKE_PROB used for star/galaxy separation (p. 2). Not stacked-image detection.
- Images: deep Euclid VIS stacked images were used for visual inspection of each candidate to rule out artefacts and chance projections (p. 5). Colour composites (Fig. 2) built from the four MER stacked images with the eummy code (p. 4-5, footnote 4).
- Characterisation catalogues: for the 15 confirmed systems, the analysis switched from MER to dedicated PSF-fitting stellar photometry (Libralato et al. 2024, 2026; Griggio et al. 2026), described as more efficient and precise than MER in crowded regions (p. 5). These catalogues are not described as a DR1 product here; check the DR1 explanatory supplement.
- External: Pace (2025) local-volume galaxy catalogue and Harris globular-cluster catalogue; PARSEC isochrones; Planck reddening maps.
- Naming: MW systems as Euclid UFSS DR1 1-3 plus constellation names; Local Volume dwarfs as Euclid LVDw DR1 1-12 (p. 5).

## Processing and methods
1. Select stars: POINT_LIKE_PROB > 0.05, then colour-colour polygon (removes compact background galaxies and galaxy groups that mimic dwarfs), dereddened magnitudes (p. 2).
2. Isochrone filter over 27 distance moduli; stellar density map per distance slice; local significance map (p. 3).
3. Candidate vetting: visual inspection on VIS stacks; independent recovery of the 5 new systems by the erose algorithm (Rusterucci et al. 2026) (p. 3-5).
4. Distances: visual PARSEC isochrone fit (old, 13 Gyr; start [Fe/H]=-2.2, more metal-rich for brighter dwarfs); uncertainty from the shift at which the fit is no longer acceptable. TRGB fit (Bayesian, RGB + AGB + field LF) for the 6 systems with populated RGBs (LVDw 4, 5, 7, 8, 10, 11), adopted as fiducial for those (p. 5-7, App. A p. 19-21).
5. Structure: maximum-likelihood (Martin et al. 2008, 2016): exponential profile plus constant background; six free parameters (RA, Dec, r_h, ellipticity, PA, N*); emcee, 1000 walkers, 10 000 steps, 1000 burn-in (p. 7-8).
6. Luminosity and mass: Monte Carlo synthetic CMD population including stars below the detection limit (p. 8-9).
7. Environment: M81 group membership via Monte Carlo 3-D distance to M81 (3.6 +/- 0.1 Mpc) and zero-velocity radius R0 = 0.89 +/- 0.05 Mpc (p. 11-12).

## Validation and performance
- Recovery of known systems 88 percent overall (see above) (p. 3).
- Visual vs TRGB distance moduli agree within about 1 sigma for all 6 systems; largest difference about 1.1-1.2 sigma for LVDw DR1 11, likely because bright intermediate-age AGB stars above the tip pull the visual fit brighter (p. 5, App. A p. 19).
- Fornax 7 independently found by Saifollahi et al. 2026: (m-M)=20.8, r_h=5.0 +/- 1.0 pc, M_V=+0.3 +/- 0.3, M* about 170 Msun, consistent with this paper (p. 9-10).
- Structural parameters stable within 1 sigma when varying the magnitude cut down to the unfiltered catalogue (p. 8).
- Typical distance-modulus uncertainty: 0.3 mag (MW systems) and 0.5 mag (LV visual fits), i.e. about 1 Mpc at 4 Mpc (Table 1, p. 7).

## Known issues, caveats, limitations
- Not an integrated-light method: sensitivity depends on the number of resolved RGB/AGB stars, so the fraction recovered drops beyond about 3.6 Mpc for faint dwarfs (p. 3).
- False-positive sources: compact background galaxies and small galaxy groups mimic dwarfs; mitigated by POINT_LIKE_PROB and the colour-colour polygon; every candidate was checked by eye on VIS stacks for artefacts (p. 2, 5). Selection function to be quantified in Rusterucci et al. (in prep.).
- Crowding: central regions of galaxies beyond 3 Mpc have lower stellar detection efficiency in the catalogues, which may bias r_h high and total luminosity and mass low; no artificial-star tests were done (p. 8).
- LVDw DR1 8 sits near the footprint edge; no structural fit possible (p. 8).
- Stellar masses rely on extrapolation of the IMF below the detection limit (only up to about 3 percent of the population is detected for MW systems); shallower mass functions would give lower masses (p. 8-9).
- TRGB calibration assumes SMC-like metallicity; the systems may be more metal-poor (p. 5). Metallicity values are loose (+/- 0.3 dex shown in Fig. 3).
- Distances for LVDw 1 and 2 are especially uncertain (only a handful of bright RGB stars) (p. 10).
- Membership of M81 or other hosts cannot be established without velocities; P(<R0) is a geometric measure, not a binding probability (p. 12).

## Implications for extended-galaxy photometry, 2-D modelling and low-surface-brightness work
- Complements, rather than overlaps, integrated-light LSB work: here the LSB regime is reached through resolved stars, which avoids the sky-background and over-subtraction problems that affect diffuse-light photometry (see the Q1 ICL processing paper in this KB). It is a useful independent check: for nearby targets, star-count profiles can be compared with integrated-light surface-brightness profiles.
- It shows that DR1 MER catalogues and VIS stacks are sufficient to find mean mu_V of 28 to 31 mag/arcsec2 systems when they are resolved, which sets expectations for what small LSB dwarfs look like in Euclid (extended, clumpy, resolved into RGB stars).
- Practical lesson for catalogue-based work: in crowded galaxy bodies the MER catalogue is less complete and less precise than dedicated PSF-fitting photometry; do not rely on MER for stellar photometry in galaxy centres.
- Fitting exponential profiles to star counts with a constant background (Martin et al. method) is an alternative to Sersic fits for resolved dwarfs; they report the circularised r_1/2 = r_h sqrt(1-e).
- Not relevant to bulge/disc decomposition, ICL or stellar-halo photometry of massive galaxies at intermediate redshift.

## Practical recommendations for users
- Use POINT_LIKE_PROB (> 0.05 is permissive but high-purity) plus the (IE-HE) vs (YE-HE) locus for star selection; apply Planck-based extinction with the R coefficients listed above.
- For resolved dwarfs, adopt a magnitude cut of about IE <= 25.7 for structural fits (1 mag above the 5 sigma point-source depth).
- Use TRGB with M_TRGB(IE) = -3.30 where the RGB is populated; otherwise treat distance moduli as having 0.5 mag errors.
- Do not use detections close to footprint edges for structure fits.
- Always vet candidates visually on the VIS stack, particularly for diffuse single objects.

## Objects, fields and figures worth revisiting
Coordinates are J2000 deg from Table 2 (p. 9); distances from Table 1 (p. 7; fiducial = TRGB for LVDw 4, 5, 7, 8, 10, 11). M_V and r_h from Table 2.

Milky Way halo (new discoveries)
- Ursa Minor II / Euclid UFSS DR1 1: RA 196.1542, Dec +75.5724; 20 +/- 3 kpc; M_V +2.0; r_h 2.25 arcmin (13 pc); M* about 42 Msun; mu_V about 31. Faintest of the three; spectroscopy by Balbinot et al. in prep.
- Fornax 7 / UFSS DR1 2: RA 38.8244, Dec -33.9567; about 145 kpc; r_h 5 pc; M_V +0.5; M* about 117 Msun; near tidal limit of Fornax dSph (1.1 deg NW, about 2.8 kpc projected). Ambiguous GC/UFD.
- Eridanus V / UFSS DR1 3: RA 28.8623, Dec -47.7105; about 166 kpc; r_h 12 pc; M_V -1.45; M* about 550 Msun; GC/UFD ambiguous.

Beyond the Local Group (new discoveries)
- Euclid LVDw DR1 1: RA 150.0281, Dec +74.2053; 3.8 Mpc; M_V -8.06; r_h about 400 pc; mu_V about 27.4; candidate M81 member (P=0.66).
- Euclid LVDw DR1 2: RA 42.8359, Dec -54.3617; 4.4 Mpc; M_V -7.9; r_h about 420 pc; mu_V about 28.3; possible satellite of ESO 154-023 (about 50 arcmin away).

Previously catalogued, resolved here for the first time
- LVDw 3 (KK2022 Dw0916+6944): RA 139.1833, Dec +69.7354; 3.02 Mpc; M_V -8.07; M81 candidate.
- LVDw 4 (PYY2023 J123423+764330): RA 188.5979, Dec +76.7248; 3.22 Mpc (TRGB); M_V -9.79; P=0.44.
- LVDw 5 (PYY2023 J095637+722617): RA 149.1518, Dec +72.4392; 3.25 Mpc (TRGB); M_V -8.58; mu_V about 27.9; strongest M81 candidate (P=0.87).
- LVDw 6 (SDSS J095022.73+621537.8): RA 147.6009, Dec +62.2599; 3.8 Mpc; M_V -7.94.
- LVDw 7 (Dw1155+78): RA 178.9786, Dec +78.0790; 3.91 Mpc (TRGB); M_V -9.62.
- LVDw 8 (PYY2023 J121704+750321): RA 184.263, Dec +75.057; 4.06 Mpc (TRGB); near footprint edge, no structure; P=0.27.
- LVDw 9 (SDSS J094132.57+660505.0): RA 145.3759, Dec +66.0859; 4.2 Mpc; M_V -7.31; mu_V about 28.5 (faintest surface brightness of known galaxies at these distances).
- LVDw 10 (MAGE1223+6908): RA 185.7589, Dec +69.1367; 4.49 Mpc (TRGB); M_V -8.82; candidate satellite of NGC 4236 (about 40 kpc along line of sight).
- LVDw 11 (LEDA 166124): RA 183.1684, Dec +68.9277; 4.74 Mpc (TRGB); M_V -11.30; M* 4.1e6 Msun; brightest and best-populated; about 0.6 deg from NGC 4236 but about 290 kpc behind it.
- LVDw 12 (SMDG J0329164-494928): RA 52.3191, Dec -49.8249; 5.5 Mpc; M_V -8.61; about 52 arcmin from IC 1959.

Figures and tables: Fig. 1 colour-colour selection (p. 3); Fig. 2 colour composites of all 15 (p. 4-5); Fig. 3 CMDs with isochrones and control fields (p. 6-7); Fig. 4 MCMC corner plot and star map for Eridanus V (p. 8); Fig. 5 M_V vs r_1/2 with mu_V = 28, 30, 32 lines (p. 10); Fig. 6 M_V vs distance (p. 11); Fig. 7 3-D layout of M81 group (p. 12); Fig. A.1-A.2 TRGB fits (p. 20-21). Tables 1-3 (p. 7, 9, 12).
Demo-target note: the M81-direction dwarfs lie at Dec +62 to +78 deg; LVDw 11 is the best-populated target and LVDw 5/9 are the most diffuse.

## Cross-references
- Kümmel et al. 2026 (MER processing/catalogue); Romelli et al. 2026 (MER, POINT_LIKE_PROB); Mellier et al. 2025 (mission, depths); Cropper et al. 2025 (VIS); Jahnke et al. 2025 (NISP).
- Libralato et al. 2024, 2026 and Griggio et al. 2026 (PSF-fitting stellar photometry).
- Saifollahi et al. 2026 (Fornax 7 and M_V conversion); Rusterucci et al. 2026 and in prep. (erose, selection function); Annibali et al. 2026 and in prep. (dwarf satellites, colour-colour selection); Bellazzini and Pascale 2024 (TRGB in IE).
- KB companion: q1_icl_processing_bamford (integrated-light LSB processing issues).
