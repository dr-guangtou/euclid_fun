---
title: "Euclid Data Release 1 (DR1): VIS processing and data products"
short_name: mccracken
first_author: McCracken
series: A&A Special Issue DR1-Foundation (Nov 2026)
local_pdf: ~/Desktop/euclid/papers/mccracken.pdf
local_text: ~/Desktop/euclid/text/papers/mccracken.txt
topics: [VIS, calibrated frames, stacks, NoiseChisel background, astrometry, photometry, zero point, PSF, chromatic shift, ghosts, bleeding, persistence, noise floor, EUDF depth, quality control]
relevance_extended_galaxies: high
---

# VIS processing and data products (McCracken et al. 2026)

## TL;DR
Describes the VIS DR1 reprocessing (VIS PF v18.0.4): 42 092 calibrated frames, 2092 deg2 of validated nominal exposures (p. 1). Algorithms are essentially unchanged from Q1; the paper's value is a global validation of astrometry/photometry at quadrant and source level, plus a list of remaining systematics. For LSB users the key points are: single exposures are NOT background-subtracted (a NoiseChisel background map is supplied separately), the stack is built after subtracting that background, unmasked ghosts and serial-register bleeding from very bright stars persist, and the deepest VIS data hit a noise floor attributed to diffuse light of faint galaxies (p. 10-11). It gives no explicit large-scale flat-field/background accuracy in surface-brightness units.

## Key facts and numbers
- Detector: 36 back-illuminated CCDs, 40 um thick, 4132 x 4096 px, 12 um pixels, 4 quadrants each (144 quadrants); pixel scale 0.100 arcsec at FPA centre, varies 1.5% across the FPA (p. 1).
- Reference observing sequence (ROS): 4 dithered nominal exposures of 566 s in an S pattern, plus two short 95 s exposures at the first two positions (p. 1). Obs_id may contain more than one ROS.
- DR1 survey data from 14 Feb 2024 to 21 May 2025 (15.2 months), plus PV and calibration fields; nominal exposures cover 2092.2 deg2 (EWS+EDS+COSMOS+calibration fields) (p. 1). EWS has 50 skypatches (49 used for astrometry). EDS: 3 deep fields (EDF North, South, Fornax) = 23 skypatches, up to 52 visits per skypatch (p. 8).
- Previous releases: Q1 61.3 deg2, Q2 4.8 deg2 (p. 1). DR2 expected ~5800 deg2, >120 000 calibrated frames, >1.5 PB (p. 11).
- QC: of 42 092 images, 37 875 pass DQC thresholds and 4217 are flagged, but all 42 092 are delivered (Fig. 2, p. 3). Main rejection reason: cosmic-ray hits from solar activity.
- Astrometry (reference sample 18.5 < IE < 19.8, Gaia RUWE<1.2, sigma_pm<0.5 mas/yr): internal/external dispersion 0.08/0.18 mas at quadrant level, 3.4/5.6 mas at source level; patch level 0.004/0.06 mas (Table 1, p. 5). External mean quadrant-averaged residual RMS 0.41 mas, max 0.88 mas; systematic offset (dX,dY)=(0.30,-0.04) mas (p. 5). Per-exposure mean residual <3 mas for 99.8% of images (p. 5).
- Photometry: internal/external dispersion 0.76/1.4 mmag (quadrant), 11/25 mmag (source), patch-level 0.07/2.3 mmag; external mean offset vs Gaia 3.8 mmag; requirement 5% absolute, 1% relative (p. 8). Quadrant-mean internal offsets within about -2.7 to +1.5 mmag; outermost CCD rows in YFPA at -0.7 and +0.9 mmag relative to inner rows (p. 8).
- Image quality: focal-plane median FWHM_IMAGE 0.140 arcsec; 16-84 percentile across quadrants 0.135-0.150; edge quadrants up to ~0.176 arcsec; requirement <0.18 arcsec (Fig. 9, p. 9). Red stars (BP-RP>1.5) have median FWHM 3.3% larger than blue in the same quadrant; (BP-RP>2)/(BP-RP<1) ratio -1 = 5.16% (Fig. 10).
- Self-cal field: monthly visits, 60 dithers (+16 for blue grism) = 76 nominal + 72 short exposures per visit; 16 visits Oct 2023-May 2025 used; 4352-star reference sample (p. 8).
- Zero-point residual scatter in self-cal: 1.5 mmag (all visits), 0.55 mmag post-decontamination; WD J175318+644502 scatter 9.6/6.6 mmag, so Gaia-based ZPs preferred (Table 2, p. 8-9).
- Depth-scaling in EUDF: 5 sigma IE limit in empty 0.5 arcsec apertures reaches ~29-29.5 mag at ~2e5-5e5 s (read off Fig. 12 axis, p. 10); the deepest points fall 0.2 mag below the extrapolated sqrt(t) relation.
- Shutter: shutter motion 2.739 s open and close; RSU fully open ~7.7 s after DATE-OBS (~9.6 s before 2024-01-26 00:35 UTC), spread ~0.1 s; beam starts opening 0.17 s after motion start, fully open after 2.20 s (App. C, p. 18).
- DR1 PF version: VIS PF 18.0.4, source released with DR1 (p. 1).

## Data products and data model
Archive data product types (p. 2):
- DpdVisRawFrame: unprocessed Level-1 input, 144-extension FITS (one per quadrant), compressed.
- DpdVisCalibratedQuadFrame: calibrated frame (144 quadrant extensions), plus background map, weight map and PSF model (PSF model added in DR1).
- DpdVisCalibratedFrameCatalog: single-exposure SExtractor-based catalogues (new columns added in DR1).
- DpdVisStackedFrame: per-ROS stack (SWarp). In DR1 the background FITS is no longer included and the RMS and FLG extensions were removed from the stack FITS (p. 3). Weight map still accompanies it (not detailed in this paper).
- DpdVisStackedFrameCatalog: catalogue from the stack.
- DQC reports as json and xml with the release; per-exposure plots and the list of rejected frames are in the Explanatory Supplement (p. 3).
Header/flag changes (p. 3): extension headers now contain MJD-OBS and TIMESYS='UTC'; flag name GOOD removed from the VIS flag definition (numeric values unchanged). DATE-OBS is the start of the instrument event sequence, not the shutter-open time (App. C).
Catalogue quantities mentioned: FLUX_RADIUS, MAG_APER (50 px diameter, plus 13 px diameter fixed aperture with APERCORR = 0.0655 mag), MAG_APER_1/2 (0.7 and 1.3 arcsec diameter), FWHM_IMAGE, MAG_MODEL (PSF-fitted; see caveats), spread_model. Units of the frame images (ADU vs electrons vs flux) and exact HDU names are not given in this paper; consult the DPDD.
DQC statistics per image: score, spread_peak (pointing stability), mean_residual (astrometric), max_cr, max_cr_norm, fpa_cr_norm (p. 3).
Merged analysis catalogues (not delivered): per-skypatch, with group_id for repeat observations, XFPA/YFPA in mm, quadrant id (p. 4).

## Processing and methods
Pipeline (p. 2): 16 calibration pipelines + science pipeline.
1. Block 1 (detector level): saturation flagging, crosstalk, bias, non-linearity, cosmic-ray flagging with LACosmic (DR1 adds a second detection pass on the stacked image), brighter-fatter effect (BFE) correction, PRNU correction, gain equalisation. Inputs: cosmetic maps, crosstalk model, master bias, NL model, BFE model, master PRNU, gain model. CTI is NOT corrected in DR1 (trap density is monitored).
2. Block 2: illumination correction, background estimate with NoiseChisel (supplied but not subtracted from calibrated frames), intermediate SExtractor catalogue, astrometric solution (Gaia DR3; WCS fitted per quadrant, using apparent directions including parallax, then converted to ICRS), ghost flagging (ghost model), second photometric catalogue, photometric calibration (zero point from Gaia stars, PSFEx PSF model, zero-point reference photometry).
3. Block 3: for each ROS, background-subtracted exposures are stacked with SWarp; SExtractor catalogue and PSF model on the stack.
Calibration validity (p. 2): a single product for the whole period for gain, PSF model, readout noise, saturation, BFE, ghost mask, crosstalk, stellar mask; time-varying products for flag maps, master bias, PRNU, astrometric distortion (7 distortion models from 7 self-cal visits) and zero point. Zero point: two-segment linear model in time with a constant after the decontamination, fitted to all self-cal zero points (Fig. 1); ice contamination on a folding mirror caused ZP validity to last ~1 week until March 2024. A period of heavy ice degradation is excluded from DR1.
Aperture-correction error in the ZP of nominal vs short exposures was found and has been fixed in later pipeline versions (p. 2-3).
Gaia-to-IE transformation: Gaia G, BP, RP converted from Vega to AB (add 0.1136, 0.0155, 0.3561); IE = G + 0.1136 - f(C), C = BP-RP-0.3406, valid 0.079<C<2.921 (App. A, Table A.1; f runs 0.043 to 0.618 mag).
Validation catalogues (p. 4): point-source selection 1.0<FLUX_RADIUS<1.3, nominal 18.5<MAG_APER<22.0 (texp>500 s), short 16.5<MAG_APER<21.0 (texp<100 s); match to Gaia within 0.5 arcsec with proper motion and parallax (Euclid at ~Earth+0.01 au; mean parallax displacement 0.73 mas along +XFPA).
EUDF depth analysis (p. 10): custom Drizzle pipeline, 50 mas pixels, tiles; depth from variance of sky in empty 0.5 arcsec apertures on 100 mas block-summed mosaics after masking objects (Gaia-based bright-star mask).

## Validation and performance
- Astrometry vs requirement: the 4 arcmin-aperture distortion requirement (3e-5) is met: RMS gradient (7.0+-0.3)e-7, max (2.04+-0.08)e-5 over 16 702 nominal exposures (p. 4). But the spurious edge ellipticity between adjacent quadrant WCS fits exceeds 3e-5 at scales <22 arcsec (Fig. 4, p. 5-7); peak-to-peak mean-residual profile across quadrant boundaries ~0.2 mas. To be addressed for DR2.
- Deep fields give practically the same accuracy as the wide survey: quadrant-level astrometric 0.07/0.18 mas, photometric 0.50/1.2 mmag; source-level 5.7 mas, 24 mmag (p. 9).
- No evidence for residual BFE or non-linearity from nominal-minus-short comparisons of peak surface brightness, curve of growth and FWHM versus magnitude in 18.5-21 (Fig. 11, p. 9-10). Small constant offsets: slight BFE overcorrection (peak SB), a constant curve-of-growth magnitude offset consistent with an uncorrected shutter effect, and a small FWHM difference that depends on XFPA.
- Chromatic shift: red-minus-blue centroid shift of up to a few mas, primarily along XFPA, depends on FPA position (Figs. 6-7); Table B.1 gives shift vs BP-RP (about -1.4 mas at BP-RP 0.6 up to +3 mas at 1.35 for the G-GRP column; values relative to the mean calibration-star colour). Corrections needed for sub-mas work.
- Depth-time scaling in the EUDF: straight-line fit over 1.5e4<t<8e4 s; the median flattens and is 0.2 mag shallower than extrapolation in the deepest regions (Fig. 12). Aggressive object masking removes the excess but leaves almost no sky; correlation analysis shows the excess light at all scales and tied to detected sources; the authors attribute it to diffuse light of faint galaxies, not excluding unmasked ghosts or background-subtraction residuals (p. 10-11, Fig. 13).

## Known issues, caveats, limitations
- Skypatches 39 (EDS) and 40 (EWS): processed with an inappropriate distortion model after focal-plane warping along a diagonal between 15 and 18 June 2024 (shortly after the 8 June 2024 decontamination); skypatch 40 shows a median largest per-quadrant residual of 23 mas vs 9 mas elsewhere; use with caution, excluded from astrometric statistics (p. 3, 11).
- Calibrated frames are not background-subtracted; the NoiseChisel background is slightly oversubtracting in places (the sky in Fig. 13 is slightly negative) (p. 11).
- CTI not corrected (p. 2). Uncorrected shutter effect (exposure-time gradient across the FPA, see Schirmer et al. fig. 7) leaves small magnitude and FWHM offsets (p. 9-10, 18).
- MAG_MODEL (PSF-fitting) magnitudes have anomalous scatter due to inconsistent PSF normalisation between quadrants (second-order polynomial over-fit of the PSF). Treat with caution; a first-order polynomial PSF is in preparation for DR2. PSF-fit photometry is not used inside VIS PF, so other products are unaffected (p. 11).
- Bleeding along the serial register from very bright stars (IE~10) produces bands in calibrated exposures and in MER mosaics; readout-node persistence smears bright pixels along the serial direction; fixes planned for DR2 (p. 11).
- Unmasked ghosts remain in deep images, sometimes seen as small diffuse objects, producing spurious detections in the MER catalogues; improved masking (e.g. different mask threshold for the parent star) in DR2 (p. 11).
- Time-dependent photometric offsets (ice, throughput 4-5 mmag change across decontamination) and focal-plane-dependent photometric residuals of ~1 mmag (outer CCD rows) (p. 8).
- Cosmic-ray hits are the main reason for frame rejection; unmatched point sources in the reference sample are mostly cosmic-ray hits (p. 3-4).
- Gaia-matching: 1.5% of Gaia stars lack a VIS counterpart (high proper motion matched at 2016 epoch; or near bright stars) (p. 4).
- The VIS passband is broad, so FWHM and centroid depend on colour.
- DATE-OBS does not equal integration start (App. C).

## Implications for extended-galaxy photometry, 2-D modelling and low-surface-brightness work
- The VIS frames are background-unsubtracted, so for LSB work you may prefer to re-estimate the sky yourself on the calibrated frames or on the stack with a large-scale, aggressively masked model; the supplied NoiseChisel background is designed to preserve faint extended light but is known to oversubtract slightly near sources (p. 11) and its tile/mesh scale is not given in this paper (check the Explanatory Supplement).
- The stack in DR1 has the NoiseChisel background already subtracted per exposure before SWarp combination (p. 2); any bias of that sky over a large galaxy is therefore baked into the stack. For outskirts, stellar haloes and ICL start from the calibrated frames plus background map and redo the combination, or at least compare.
- The EUDF test shows the noise floor in the deepest data is set by extended diffuse galaxy light, which also indicates that blank-sky depth estimates in deep fields are biased by faint-galaxy wings; sky-variance based depths will not reflect true LSB limits in crowded fields.
- Flat-field/illumination accuracy: no direct SB-scale numbers, but the internal quadrant-scale photometric means are consistent within ~2 mmag and the outer CCD rows differ by <1 mmag, which bounds large-scale illumination errors at about the 0.1-0.2% level for stars (p. 8); this is not a statement about the sky level.
- Unmasked ghosts and serial-bleeding bands are potential contaminants of faint outskirts: inspect flags and masks around bright stars; DR2 will improve.
- PSF: use the delivered PSF model with caution (normalisation problems between quadrants); for 2-D Sersic fits PSF FWHM ~0.14 arcsec with ~3% colour dependence; undersampled PSF at 0.1 arcsec pixels. The paper gives no wings/halo PSF characterisation; look to the dedicated PSF paper.
- Photometric accuracy for extended galaxies: zero-point is derived from point-source aperture photometry (13 px aperture with APERCORR 0.0655 mag), so total magnitudes depend on the PSF-aperture correction and on shutter/BFE offsets at the ~0.01 mag level (p. 9-10).
- Astrometric precision (a few mas per source; sub-0.5 mas systematic per quadrant) is more than sufficient for multi-exposure registration of galaxy images; chromatic shift matters only for very red or very blue point sources.

## Practical recommendations for users
- Do use the weight map and the flag map (not described in detail here) with each calibrated quad frame; apply the cosmic-ray and ghost flags and check bright-star neighbourhoods by eye.
- Do remember to add back or independently estimate the sky: calibrated frames are not background-subtracted, while stacks already are.
- Prefer the aperture-based fluxes over MAG_MODEL in single-frame catalogues for DR1.
- Don't trust skypatches 39/40 astrometry without checking; look at the DQC json/xml and the rejected-frame list in the Explanatory Supplement; the 4217 flagged images are still delivered.
- For time-domain or moving-object work compute the shutter-open time from HKTM (App. C), not DATE-OBS.
- For sub-mas astrometry on individual frames apply the chromatic shift correction (App. B); G-GRP is a better predictor than BP-RP for red stars.
- Absolute ZP check: external mean offset vs Gaia is +3.8 mmag; the short-exposure ZPs had an aperture correction error in this processing (small differences from nominal).

## Objects, fields and figures worth revisiting
- Fields: Euclid Wide Survey skypatches 1-50 (not individually listed); EDF North, EDF South, EDF Fornax (23 deep skypatches, up to 52 visits); self-calibration field / EUDF near the North Ecliptic Pole (more than 3000 VIS exposures); COSMOS. No coordinates given in this paper (the white dwarf J175318+644502 is the HST secondary standard in the self-cal field; coordinates 17:53:18.65 +64:45:02.15 appear in the NIR paper).
- No named galaxies.
- Figures: Fig. 1 (ZP evolution, p. 3); Fig. 2 (DQC statistics, p. 3); Fig. 4 (spurious edge ellipticity, p. 7); Figs. 6-7 (chromatic shift, p. 7); Fig. 9-10 (FWHM, p. 9); Fig. 11 (BFE/NL test, p. 10); Figs. 12-13 (EUDF depth scaling and masked-sky residuals, p. 10-11), which are the most relevant for LSB; Table 1 (p. 5); App. A-C (p. 18).

## Cross-references
- Q1 VIS paper (McCracken et al. 2026, A&A 711, A2; "Q1VIS") for full description of each PF step, BFE (sect. 3.9), NL (sect. 3.6), PSF.
- Schirmer et al. 2026a (calibration strategy, requirements, self-cal field, shutter effect fig. 7) and Schirmer et al. 2026b (ice contamination and decontamination).
- Ruffenach et al. 2026 (SGS), Tereno et al. 2026 (survey/ROS), Aussel et al. 2026 (DR1 overview), MER PF paper (mosaics and catalogues affected by ghosts/bleeds).
- DR1 DPDD (https://euclid.esac.esa.int/dr/dr1/dpdd/) and Explanatory Supplement (https://euclid.esac.esa.int/dr/dr1/expsup/) for HDU layout, flags and the full list of known processing issues.
- McCracken et al. in prep. (EUDF processing); Miller et al. in prep. (chromatic shift).
