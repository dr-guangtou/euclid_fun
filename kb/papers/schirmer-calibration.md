---
title: "Euclid Data Release 1 (DR1): Calibration strategy and observations"
short_name: schirmer-calibration
first_author: Schirmer
series: A&A Special Issue DR1-Foundation (Nov 2026)
local_pdf: ~/Desktop/euclid/papers/schirmer-calibration.pdf
local_text: ~/Desktop/euclid/text/papers/schirmer-calibration.txt
topics: [calibration plan, self-calibration, large-scale flat, zero point, VIS shutter, persistence, ice contamination, PSF calibration, phase diversity, CALBLOCK, photometric transformations]
relevance_extended_galaxies: medium
---

# Euclid calibration strategy, in-flight calibration observations and DR1 limitations (Schirmer et al. 2026)

## TL;DR
The paper explains how the Euclid mission requirements (MRD, CalCD-A/B) were turned into an in-flight calibration plan (the "CalF" with 18 CALBLOCKs) centred on repeated dithered "self-calibration" visits of one field near the North Ecliptic Pole. It states that DR1 already meets most spectrophotometric requirements, while the VIS PSF model and the spectroscopic purity/completeness are not yet met (p. 2-3). For galaxy-imaging users the most useful parts are Sect. 5 and 7: how the large-scale flat (LSF) is built and what its residual errors are (0.08-0.14% per VIS quadrant, 0.9% NISP; chromatic 1-1.5% stellar-vs-galaxy bias; 4.7% shutter gradient in short VIS exposures), the NISP persistence masking (about 5% of pixels), NISP astrometric glitches, and the growing ice-driven NISP photometric drift that DR1 only partly corrects (p. 10-14). It also provides stellar-based colour transformations Euclid to Roman/JWST/CSST (Table B.1, p. 29). It contains little about stray light and ghosts apart from a few calibration-plan details.

## Key facts and numbers
- DR1-Foundation released Nov 2026; full DR1 mid-2027 (p. 1). 2.7 years of science operations covered (p. 3).
- Requirement hierarchy: MRD (22 weak-lensing, 9 clustering, 7 EWS, 5 EDS requirements), CalCD-A (15 top-level calibration requirements, must be met by DR3), CalCD-B (about 350 entries, frozen 2018) (p. 1-2).
- Unmet in DR1: VIS PSF model (MRD-WL-006/007/018, R-CAL-A-VS-1000/2000) and spectroscopic purity/completeness. Purity in COSMOS 85% (93-100%) at SPE_Z_PROB > 0.99 (> 0.999); EWS purity about 75% at D > 1700 deg^-2; completeness proxy [D, P] about [750 deg^-2, 62%] in COSMOS (p. 3).
- VIS image-quality numbers in Table A.1 (p. 23): median PSF FWHM about 0.140" at 800 nm (requirement <= 0.18"); pixel scale 0.0991-0.1007"/pix across FoV; PSF ellipticity <~ 0.025; (R_PSF/R_ref)^2 about 1.9; typical PSF FWHM 1.4 pixel (p. 9); distortion RMS 0.08 mas over 4' (8e-5 %) vs required 0.003 %.
- NISP-P: pixel scale 0.296-0.299"/pix; EE50 radius <= 0.28", EE80 <= 0.56" in all bands (p. 23); EWS depth 25.0 mag (2x FWHM aperture, 5 sigma) vs requirement 24 (p. 24).
- VIS depth: turn-around point about 25.5 mag vs requirement 24.5 mag for 10 sigma extended sources (p. 24). Area useful for cosmology 88.3% (11.7% loss) (p. 25).
- VIS photometry: relative error 0.76 mmag internal, 1.4 mmag external (vs Gaia) at quadrant level; mean offset to Gaia DR3 3.8 mmag (p. 24, 26). NISP-P relative error 0.9% (self-cal) plus 0.3% (absolute level propagation); absolute scale tied to HST standard to 0.5% (limited by standard-star variability at 1%) (p. 23, 26).
- VIS off-band throughput about 2e-3 in 300-525 nm (requirement < 1e-3; FoM3 dielectric coating replaced by silver) and <~ 8e-4 in 935-1600 nm (p. 23-24).
- Reference observing sequence (ROS): 4 dithers; per field 4 x 566 s + 2 x 95 s VIS (IE), NISP 4 x 112 s in each of YE, JE, HE plus 4 x 574 s red-grism; average duration 73.9 min incl. about 230 s slew; one NISP slew dark per ROS (p. 4, 8). VIS nominal exposure effective 560.5 s, short 89.5 s (p. 11).
- Thermo-optical e-folding timescale 21 h (pre-launch and verified in PV by flipping AA from +3.5 to -7.5 deg); 2-10 days to reach stability after a major excursion (p. 4, 8). SAA changes have a far larger effect than AA changes (p. 8).
- Allowed attitude for VIS stray-light control: AA in [-8, -3] deg, SAA in [87, 112] deg (p. 4).
- Absolute pointing about 3" (30 VIS pixels); minimum dither (eigenslew) 73"; high-gain antenna repoint every 50 min; minimum replanning time 5 weeks; SOPS windows 6 h every 4 weeks, relaxed to every 8 weeks from Jan 2026 (p. 4-5).
- Self-calibration field: centre (RA, Dec) = (268.8127, +65.286) deg, 2.0 deg^2 pattern, within 2.3 deg of the NEP; 60 pseudo-random dither points (1000 candidates optimised); each visit 23.5 h every 25-35 days (p. 6-7). Three visits lost to radiation storms (p. 6). Also called EUDF (Euclid Ultra Deep Field), about 1.5 mag deeper than EDS over 2 deg^2 (p. 9).
- Relative photometric accuracy required after LSF: VIS 1.0%, NISP-P 1.5%, NISP-S 0.7% (p. 7).
- EWS tile overlaps are only about 2.2% of area, too little for an uber-calibration (p. 6).
- Calibration fields (Table 2, p. 9): AEGIS (214.827, +52.82; 1.0 deg^2; 4x EWS depth planned; 100% in DR1), CDFS (53.117, -27.81; 0.5 deg^2; 5x; 100%), EUDF (268.813, +65.29; 2.0 deg^2; 8x; 50%), COSMOS (150.119, +2.21; 2.0 deg^2; 5x; 61%), GOODS-N (189.250, +62.25; 0.5; 4x; 0%), VVDS (36.500, -4.50; 0.5; 5x; 0%), SXDS (34.500, -5.00; 2.0; 5x; 0%). COSMOS: 2x2 mosaic with 50% of area at 30% depth plus a central PV pointing at 100% depth.
- PSF calibration: 23 PSF fields (24 in Table D.1), each visit 100 x 289 s exposures on a Vogel spiral, S/N 5x EWS, stars 17.5 < IE < 21, every 2-6 weeks, at least 3 days after patch start (p. 10).
- Phase-diversity campaign (PDC): M2 moved +-18 um shifts the focus by 113 um, PSF becomes an 8-pixel disc; 150 x 289 s per focus position, 10 [SAA, AA] configurations (3 with defocus), 2.5-month block Dec 2023 - Feb 2024 (p. 9-10).

## Data products and data model
- Calibration products are called CALPRODUCTs and calibration observations CALBLOCKs, tracked in the Calibration Framework (CalF, python-sphinx html base) (p. 3). Appendices list them:
  - Table C.1 (p. 35): survey/system characterisations SURV-001..004 (depth, relative photometry, sensitivity, zodiacal model), TEL-001..003 (thermal timescale, PLM contamination, external stray light), TARGET-001..004 (colour-gradient, photo-z, noise-bias, completeness/purity fields).
  - Table D.1 (p. 36-37): CALBLOCK F-001..F-018 (self-cal; noise-bias; CPC; colour-gradient; photo-z; wide survey; VIS nonlinearity/PTC/BFE + NISP LED flats; VIS PSF calibration + NISP photo-nonlinearity; NISP spectro-nonlinearity; NISP wavelength dispersion; NISP reciprocity failure; VIS flatband voltage shift; PDC; contamination scan; serial trap pumping; CTI injection timing; grism sanity; NISP persistence).
  - Table E.1 (p. 38-39): NISP common products NI-001..015 (bad pixel map, baseline map, BFE, crosstalk about 0.001%, dark current about 0.02 e-/s, IPSV, IPC, inoculation (deactivated), LED flats, nonlinearity, persistence, reciprocity failure, slew darks, snowballs).
  - Table F.1 (p. 40): NISP-P products NP-001..011 (absolute standards, astrometric solution, LSF, dichroic ghost model, PSF model, stray-light check, small-scale flat, zodiacal model ...).
  - Table G.1 (p. 41): NISP-S products NS-001..012.
  - Table H.1 (p. 42-43): VIS products VS-001..028 (absolute standards, bias, BFE, CTI, cosmetic map, crosstalk, darks, astrometry, PTC, dichroic ghost model, LSF VS-013, LED PRNU, nonlinearity, PSF, blooming, stray-light check, small-scale flat VS-022, flatband shift, trap pumping, CTI covariance, persistence, shutter map VS-028).
- HEALPix maps of NISP astrometric error as a function of sky position are provided alongside SGS products (p. 12).
- Spectroscopic quality column SPE_Z_PROB is mentioned (p. 3). Persistence masking appears as a pixel mask on NISP images (p. 12).
- Table B.1 (p. 29): polynomial colour transformations between Euclid (IE, YE, JE, HE) and Roman (F062..F184), JWST (F070W..F200W) and CSST (r, i, WV, WI, z) for stars.

## Processing and methods
1. Self-calibration (Sect. 5): repeated, widely dithered observations of the NEP field give differential photometry of the same stars at different focal-plane positions, from which the LSF (a photometric flat correcting residual large-scale illumination errors of the LED flats) is solved (p. 5-6). VIS LSF uses Gaia stars with S/N > 80 (to reduce sensitivity to faint cosmic rays), restricted to G_BP-G_RP = 0.2-2.5 and IE = 18.5-19.8 (p. 7, 11).
2. Why NEP and not SEP: perennial visibility requires SAA >= 87 deg, restricting to within 2.3 deg of a pole; the SEP line of sight is crowded with blue LMC main-sequence stars (p. 6). Field centre chosen to avoid reddening, the 6' planetary nebula NGC 6543 and stars brighter than 7 AB mag, and to include three faint HST-calibrated hot white dwarfs (J175318+644502 is the NISP-P absolute anchor) (p. 6, 10).
3. Dither pattern (Sect. 5.3): 60 points, four-point clusters <= 5' for spectroscopic order decontamination, scales from FPA diagonal down to 10"; optimised among 1000 realisations by matching the mean distribution of 1770 segment lengths (p. 6-8). Pattern frozen for the mission.
4. Each dither executes ROS_D1 (first dither of the ROS); four visit variants cycle through red-grism configurations; blue-grism done in brackets with AA offsets of +-1.4 to 2.0 deg (p. 7-8).
5. DR1 zero points: VIS piecewise linear before the first decontamination, constant after the second; NISP-P piecewise constant (p. 10). VIS absolute flux tied to HST CALSPEC through Gaia DR3 G (p. 10). VIS uses one LSF combining five self-cal visits; NISP uses a monthly LSF, applied piecewise without interpolation (p. 7, 10).
6. NISP persistence: masked rather than corrected; empirical power-law model from PV data, up to 5 h of illumination history; Hough-transform step for spectroscopic streaks; mask fraction about 5% (p. 12).
7. NISP distortion determined per exposure by NIR-PF because filter-wheel positioning is not reproducible (p. 12).
8. Ice contamination: DR1 relies on the monthly relative flux calibration (monthly LSF) to absorb it to first order; DR2/3 plan: four-layer AR-coating-stack model of the H2RG, fit ice thickness and growth rate from monthly flats at five wavelengths, derive time-dependent effective QE and passbands (p. 14).
9. Cross-survey transformations (Sect. 8): Besancon model on two sightlines (EDF-S and EUDF) -> Phoenix synthetic spectra -> synthetic AB photometry; stars with IE - YE < 0.69 (removes 92% of Teff < 4000 K, keeps 97% of FGK) and Teff 4500 K to T_max; second-order polynomial fits with 2.5 sigma clipping; extinction effect only about 1 mmag (p. 14-15).

## Validation and performance
- Multi-stage validation/verification (pipeline check, instrument scientists, calibration scientist vs CalCD-B), weekly reviews; full CalCD-A verification at each DR on reprocessed data (p. 2).
- LSF relative photometric accuracy: 0.08-0.14% at VIS quadrant level, 0.9% global for NISP (p. 10-11).
- VIS: stable throughput allowed five visits to be combined, with about 30 deg field rotation between monthly visits (p. 7).
- Zero-point stability: VIS LSF shows monthly low-spatial-frequency changes of about 0.4%, probably from slight contamination of folding mirror 3 (p. 11); NISP unaffected by FoM3 but ice acts on the detectors (p. 11).
- Photometric transformation validation: slopes within a few per cent of Durbin et al. (2025), absolute scale to 8% or better after AB renormalisation (p. 15). RMS of fits mostly 0.0005-0.006 mag, worst WV_CSST (0.052) (p. 29).
- Self-calibration, PV zodiacal-light and stray-light models were validated in PV; zodiacal uncertainty before launch 5-10%; zodiacal would need to be 30% higher than expected to force exposure-time changes (p. 8, 35).

## Known issues, caveats, limitations
- VIS shutter gradient (p. 11-12): exposure-time difference about 4.0 s across the FPA along the horizontal axis (map 1-4 s, Fig. 7) gives a zero-point change of 0.8% for nominal 560.5 s exposures and 4.7% for 89.5 s short exposures. It is purely geometric, achromatic, stable. In DR1 it is mixed into the LSF (optical LSF itself varies about 1%); in DR2 it will be removed explicitly (shutter map VS-028).
- LSF chromaticity (p. 11): built from stars (blue relative to typical EWS galaxies); splitting stars into blue/green/red bins gives up to 1.0-1.5% difference near the right edge of the VIS FPA. The LSF is achromatic per pixel, so galaxy photometry can have a field-position-dependent bias; fine-tuning of the G_BP-G_RP range planned. NISP chromaticity expected much smaller.
- VIS LSF time dependence about 0.4% (monthly), single LSF used in DR1 (p. 10-11).
- NISP ice contamination (p. 13-14): at DR2 peak expected uncalibrated variations of YE 0.08-0.12 mag, JE 0.03-0.06 mag, HE 0.01-0.03 mag, blue grism 15-20% (930-1350 nm), red grism 3-7% (1250-1850 nm); DR1 imaging corrected only to first order via monthly relative flux calibration with small residual colour terms; blue-grism data not updated monthly so fully affected. May cause differences between EDF-N and EDF-S spectroscopic samples.
- NISP persistence (p. 12): masking only, about 5% of pixels masked (target 2% for DR2); persistence response has decreased with time (inoculation by bright-source saturation every 2-3 months). Persistence also affects the NISP LSF.
- NISP astrometry/colour fringes (p. 12-13, Fig. 8): aggressive persistence masking in two detectors in low source-density areas leaves insufficient astrometric sources, so 0.70%, 0.23%, 0.14% of DR1 area have residuals > 0.05", 0.08", 0.1" (up to 0.8 pixel = 0.24" in an extreme case); affected areas 1'-3' wide; shows as residual colour gradient across sources. Photometry of individual compact sources there needs care; use the HEALPix astrometric-error maps. Fixed in DR2 by a threshold change.
- NISP crosstalk about 0.001%: only super-saturated stars; unproblematic in EWS but masking needed in EDF at DR2 (p. 38).
- NISP snowballs (energetic cosmic-ray-like events producing extended round/elliptical features, possible saturation and surrounding hot pixels) need masking in following exposures (p. 39). Random telegraph noise pixels not covered (p. 38).
- Slew darks contain persistence from zodiacal light, cosmic rays and sources (p. 38-39).
- VIS flats always contain astrophysical sources because the shutter must stay open; each flat is paired with a 2 s exposure to flag affected pixels (p. 5).
- VIS stray-light pattern differs between open- and closed-shutter configurations (p. 5). Sunlight reaches the instrument cavity via a scattering chain from an illuminated thruster nozzle (discovered in commissioning); mitigated by rotating the spacecraft so the nozzle is shadowed, defining the usable "dark" AA/SAA subspace (TEL-003, p. 35). VIS darks (ROS) primarily measure residual stray sunlight, which never fully vanishes (p. 42).
- Dichroic ghosts: VIS ghost from dichroic backside reflection with amplitude ratio < 2e-6 for sources brighter than 15 AB mag, validated once in PV (VS-012, p. 42); focal-plane reflection ghosts blocked by design, NISP reflection ghosts about 4 orders lower. NISP dichroic ghost to be masked for sources brighter than 14.6 AB mag with ratio 8e-8 (NP-004, p. 40). Masking thresholds are being tuned with EDS data (p. 9).
- Stray-light/glint checks: star about 6 AB mag placed adjacent to the focal plane (glints from detector edges) and 0-2 AB mag stars at logarithmically decreasing separations from the FPA edge to verify the bright-star avoidance radius (NDI model) (NP-008, p. 40; VS-021, p. 43).
- Radiation/space weather: solar flares make some VIS detectors unusable for hours; three self-cal visits lost; PDC exposure count raised to 150 for margin (p. 6, 10). VIS flatband voltage shift and CTI monitored regularly (F-012, VS-005, VS-024) (p. 37, 42-43).
- VIS charge persistence/trap pumping: serial trap pumping (every 2-6 weeks) causes a bias offset for hours; followed by PSF calibration (p. 37).
- Spectroscopic: wavelength errors up to 0.7 nm (red) / 0.6 nm (blue) at field edges, plus common scale error |delta| <~ 1.5e-4 (p. 13); not relevant for imaging.
- NISP intrapixel sensitivity variation not yet calibrated in flight (p. 38).
- Pointing: Euclid cannot make sub-pixel dithers (p. 4).

## Implications for extended-galaxy photometry, 2-D modelling and low-surface-brightness work
- Large-scale photometric flatness: the quoted 0.08-0.14% (VIS quadrant level) refers to relative zero-point accuracy from stars, not to surface-brightness flatness for diffuse light. The LSF removes 1-2% static illumination variations on scales >~ 1' but is built from point sources; it cannot guarantee flatness at the sub-per-cent level for LSB features, and the 0.4% monthly variation (single LSF in DR1) and 1.0-1.5% chromatic bias are the same order as the signal when probing outskirts at the 1% of sky level.
- Colour dependence: because the LSF is achromatic but stellar-derived, galaxies redder than the calibration stars have a position-dependent photometric bias of up to about 1-1.5% at the right edge of the VIS FPA. This matters for total magnitudes and colour gradients of bright galaxies, and for comparing galaxies placed at different focal-plane positions in different dithers.
- Short VIS exposures (89.5 s) have a 4.7% shutter gradient, so avoid using them for galaxy photometry/LSB; nominal exposures only 0.8% (mostly absorbed in the DR1 LSF but not separated).
- NISP: expect time-dependent, colour-dependent QE drift, strongest in YE (0.08-0.12 mag at DR2 peak). Use YE-based colours or SED fits of nearby galaxies cautiously and check the observation epoch. About 5% of NISP pixels are persistence-masked and persistence residuals (not corrected) can contaminate diffuse light, especially after bright sources and near saturated stars; NISP snowballs can mimic faint extended blobs.
- NISP astrometric glitches (0.05-0.24" in 1'-3' patches) produce colour gradients across sources and so bias VIS-NISP matched aperture colours and colour-gradient analysis in 2-D bulge/disc modelling; check the HEALPix astrometric map.
- PSF: VIS PSF FWHM about 0.14", ellipticity <~ 0.025, (R/R_ref)^2 about 1.9; the PSF model is not yet meeting requirement (in development); PSF depends on SAA/AA thermal state and has a 21 h e-folding time, so fields observed shortly after attitude changes have a less well known PSF. For Sersic fits, prefer PSFs from stars in the same tile/exposure; extended wings are not discussed in this paper.
- Ghosts: bright stars (< about 15 AB mag VIS, < 14.6 NISP) produce dichroic ghosts (VIS ratio < 2e-6) that are masked in the pipeline; for LSB work around bright stars the residual ghost light and glints within the NDI avoidance radius must still be checked.
- The EUDF/self-cal field (~2 deg^2 at 8x EWS depth in DR3, 50% in DR1) and the AEGIS/CDFS/COSMOS deep fields are the best places to test deep LSB measurements.
- Little on scattered-light models or sky background; the paper only states that zodiacal/Galactic backgrounds were validated in PV (uncertainty 5-10% pre-launch) and that COSMOS needed about 2x exposure to compensate higher backgrounds (p. 3, 8). See the spacecraft companion paper for stray light.

## Practical recommendations for users
- Prefer nominal-length VIS exposures/stacks for galaxy photometry; be cautious with data taken in the 95 s short exposures (4.7% shutter-related zero-point gradient in DR1).
- Allow a floor of about 1-2% (colour- and position-dependent) in photometric systematics for bright extended galaxies near FPA edges; test for position dependence of the measured magnitude using the multiple dithers.
- For NISP, check the observation epoch and expected ice-related drift, prefer VIS/JE/HE for LSB-sensitive modelling, and use HEALPix astrometric-error maps to exclude areas with > 0.05" residuals when matching VIS to NISP.
- Check persistence-masked regions and snowball masks in NISP before trusting faint diffuse structure.
- Use Table B.1 transformations only for stars with IE - YE < 0.69 (FGK-type) and in the stated colour ranges; do not apply them to galaxies.
- Expect improved shutter, ice/QE, persistence and continuous zero-point treatment in DR2.

## Objects, fields and figures worth revisiting
- Self-calibration field / EUDF: (268.8127, +65.286) deg, near NEP; NGC 6543 (6' planetary nebula) nearby to NE; WD standard J175318+644502 (RA about 268.3, Dec about +64.75 inferred from name).
- Euclid Auxiliary Fields (p. 9, Table 2): AEGIS (214.827, +52.82), CDFS (53.117, -27.81), COSMOS (150.119, +2.21), GOODS-N (189.250, +62.25), VVDS (36.500, -4.50), SXDS (34.500, -5.00).
- Lines of sight used for transformations: EDF-S (l = 256, b = -47; E(B-V) 0.01-0.02) and EUDF (l = 95, b = +30; E(B-V) 0.04-0.05) (p. 14).
- Key figures/tables: Fig. 2 (CMD of galaxies vs NEP/SEP stars, p. 6); Fig. 3 self-calibration dither pattern (p. 7); Fig. 7 VIS shutter map (p. 12); Fig. 8 NISP distortion residual colour gradient (p. 12); Fig. 9 wavelength systematics (p. 13); Tables A.1/A.2 requirement vs DR1 status (p. 23-27); Table B.1 transformations (p. 29); Tables D.1-H.1 calibration products (p. 36-43); Fig. B.1 PV schedule (p. 28); Fig. 5 PDC schedule (p. 9).

## Cross-references
- Companion paper: Schirmer et al. 2026, spacecraft performance in the L2 environment (thermal, stray light, contamination, sections 4-6 referenced repeatedly).
- McCracken et al. 2026a (VIS processing/astrometry/photometry: LSF, zero points, chromatic astrometric residuals); Polenta et al. 2026a,b (NISP photometry, NIR-PF); Kubik et al. 2026a,b (NISP persistence/detectors); Fumana et al. 2026 (NISP-S calibration); Romelli et al. 2026 (MER, ghost masking); Kuemmel et al. 2026 (VIS absolute calibration vs Gaia); Tereno et al. 2026 (survey/PDC/PSF-field implementation); Anselmi et al. 2026 (thermo-optics); Aussel et al. 2026b (DR1 overview); Ruffenach et al. 2026 (SGS processing); Radovich et al. 2026 (NISP astrometric errors); Miller, Duncan, Kim et al. (in prep., PSF model/calibration).
