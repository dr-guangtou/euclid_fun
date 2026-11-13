---
title: "Euclid Data Release 1 (DR1): Persistence in NISP detectors"
short_name: kubik
first_author: Kubik
series: A&A Special Issue DR1-Foundation (Nov 2026)
local_pdf: ~/Desktop/euclid/papers/kubik.pdf
local_text: ~/Desktop/euclid/text/papers/kubik.txt
topics: [NISP, H2RG, persistence, charge trapping, masking, background, flat-field stabilisation, energetic particle hits]
relevance_extended_galaxies: medium   # NIR-only; matters for YE/JE/HE masking, background and faint-feature contamination
---

# Persistence in NISP detectors (Kubik et al. 2026)

## TL;DR
The paper characterises persistence (residual charge release) in the 16 NISP H2RG detectors from ground and in-flight data. It fits empirical power-law decay models, and explains how DR1 uses them to mask persistence pixels in photometric and spectroscopic exposures. Persistence is typically below 1% of the stimulus but varies by up to two orders of magnitude across the focal plane. Its effect on the background and the DR1 masking choices are what matter for NISP imaging of faint extended light. The DR1 masking is deliberately conservative: over 10% of pixels in some photometric exposures are masked, and a persistence correction is not applied. The paper gives no flag column names or dedicated LSB tests.

## Key facts and numbers
- Standard sequence (ROS): 0.53 deg2, 4 dithers of about 15 min each. Each dither has one spectroscopic exposure (about 9 min, two grisms covering 1206-1892 nm) followed by three photometric exposures (about 2 min each) in JE (1168-1567 nm), HE (1522-2021 nm), YE (950-1212 nm) (p. 2).
- Readout: MACC (multi-accumulation). Frame time 1.45408 s. Spectroscopic MACC(15,16,11): 574.4 s total, 549.6 s integration. Photometric MACC(4,16,4): 112.0 s total, 87.2 s integration (p. 2). Signal and a quality factor (QF) are computed on board; QF flags energetic particle hits (EPHs).
- Detector: 2048x2048 pixels, full well about 130 ke- (p. 2).
- Persistence amplitude is typically below 1% of the stimulus fluence, with a modest nonlinearity (lower P/S at higher fluence below saturation) (abstract, p. 14).
- Variation of up to two orders of magnitude between and within detectors (p. 1). Each detector splits into a low-persistence region (LPR) and a high-persistence region (HPR). HPRs are often semicircular (detectors 11, 14, 21, 24, 31, 34, 44), and detector 41 is homogeneous (p. 4, Figs. 1-2).
- Decay: power law, the "brighter-faster" effect. The decay index varies by about 13% (HPR) and 35% (LPR) for fluences of 20-80 ke- (p. 4).
- Ground model (Eq. 1): I_P = alpha(S) [tau/(t - t0 + tau)]^beta(S). Flight model (Eq. 2): I_P = alpha~(S) (t - t0~)^(-beta~(S)), with t0~ the source-exposure midpoint. The parameters are not comparable between the two (p. 3-4).
- Temperature dependence: DCL about 100 K, TV1 87 K, in flight about 95 K. TV1 persistence is lower (p. 5).
- Mission evolution: from PV-016 (Sept 2023) to F-018 (Mar 2025), P/S at 60 ke- fell by about 37% on average in HPRs and about 59% in LPRs. The monthly 8 ke- F-007 series since Mar 2024 shows a gradual decrease of about 10% (HPR) and about 25% (LPR) (p. 6). The decay index changed by less than 5% (p. 7). Spatial morphology is stable apart from small elongated or diffuse reduced-persistence regions linked to prior saturation by spectra or bright stars (p. 6-7).
- Over-saturation: persistence behaves differently above full well. HPR and LPR contrast can reverse, and alpha exceeds the extrapolation of the low-fluence model. Eight hours after a 400 ke- over-saturation, persistence from a 70 ke- stimulus is about 40% lower on average; the reduction may last months (p. 7).
- Flat-field stabilisation: the response after a change in illumination stabilises to within 1% within about 10 min, independent of flux and wavelength. The initial deviation is at most about 3%, found in detectors 13, 14, 44 HPRs, and below 1% elsewhere (p. 7-8).
- SkyPatch 38 (EDF-N, 43 observations, 2024-06-12 to 14, enhanced EPH rates from solar activity) was used on DET13. Of the pixels above 5000 e- in the first spectroscopic exposure, 55% were stars or galaxies, 37% EPHs, 8% already saturated (p. 3, 9).
- The model underpredicts persistence from stars and galaxies in the first science exposure after illumination by a factor of about 2.5-3.5 (DET13). It overpredicts at long times and high fluence (S > 40,000 e- and t > 30 min). It overpredicts EPH persistence by about 2 (p. 12).
- Pixels above 1 ke- in spectroscopic exposures: about 5-15% (these feed spectro-to-photo persistence). Photo-to-spectro: below 0.5% (p. 11).

## Data products and data model
- No catalogue columns or flag names are defined in this paper. The persistence masks live in the NISP calibrated frames and are described in the DR1 processing paper (Polenta et al. 2026a). Check that paper for the actual HDU and flag names.
- Persistence image: a model-predicted map of persistence charge in electrons, integrated over the photometric integration time (87.2 s). Values are rescaled for spectroscopic exposures (p. 2).
- Masking: pixels whose predicted persistence exceeds a threshold are masked. Pixels saturated in any history exposure are tracked separately (blue in Fig. 13, p. 13).
- Calibration sets used: TV1 (2019 thermal vacuum), PV-010, PV-016 (Sept 2023), F-007 (monthly from Mar 2024), F-018 (monthly from Mar 2025) (Table 1, p. 3), DCL (2017 acceptance), SkyPatch 38 (science data).

## Processing and methods
1. Persistence parameterisation: fit Eq. 1 to ground UTR data and Eq. 2 to flight exposure-integrated data. Fluence dependence is described by Eq. 3 (alpha) and Eq. 4 (beta) for under-saturation (p. 4).
2. Intra-detector regions (HPR/LPR) are found from the histogram of the first dark exposure after a 60 ke- flat. Persistence is modelled per pixel (p. 4).
3. Q1 processing used the ground-derived fast-decay model with fluence dependence. Only spectroscopic-to-photometric persistence within the same dither (15 min history) was handled, and spectroscopic targets were not processed (p. 11).
4. DR1 processing was refactored. It uses the PV-016 flight model at 60 ke-, with the fluence dependence neglected. It accounts for 5 h of preceding exposures, includes spectroscopic targets, and adds a Hough-transform streak detection to improve masking in photometric images (p. 11).
5. DR1 masking thresholds: 2 e- for photometric targets (independent of the underlying signal) and 30 e- for spectroscopic targets (p. 12).
6. Optimisation study (not applied in DR1): a 3 h history is a reasonable compromise. The threshold of 5 e- cuts the JE masked fraction to under 5% per detector and about 2% over the focal plane while still removing visible persistence features. 10 e- leaves residuals (p. 12-13).

## Validation and performance
- Model accuracy was tested against SkyPatch 38 science exposures (Fig. 10, p. 12-13): systematic underprediction for sources and overprediction for EPHs, as in Key facts. The authors state that a full accuracy assessment is deferred.
- In the DR1 configuration, 2 e- in JE masks 1-10% of pixels per detector, about 5% on average over the focal plane. HE and YE are slightly lower. Including photometric history adds only about 0.5% (p. 13).
- 50% of pixels in the worst detectors take about 7 h to fall below 2 e- after a 100 ke- flat (about 4 h for 4 e-, under 2 h for 10 e-) (p. 12).
- A simple power law does not fully capture the early decay or the science-data decay (p. 10).

## Known issues, caveats, limitations
- The DR1 masking is conservative. More than 10% of pixels are sometimes masked in photometric targets, so expect coverage holes from masking, especially in the JE image directly after a spectroscopic exposure (p. 11-12).
- Persistence is masked, not corrected. A correction is deferred to DR2 or later (Awad et al., in prep.) (p. 14).
- The model underpredicts persistence from sources in the first exposures after illumination. Faint residual persistence may remain below the mask threshold, and the threshold does not depend on the target signal (p. 12).
- Self-persistence (the same source seen in three photometric exposures a few pixels apart within a dither) still contaminates a source's own flux and is not fully mitigated. Large-scale background structure also remains a challenge (p. 11, 14). For a bright galaxy this can bias the aperture flux and outer isophotes slightly.
- Background: charge trapping and release imprint large-scale patterns. In photometric exposures, especially JE after a spectroscopic exposure, the background in HPRs is higher than elsewhere by typically up to 2% and up to 5% in DET11, DET14 and DET44. In spectroscopic exposures it is up to 1% lower. Backgrounds are about 100 e- in photometric and about 1000 e- in spectroscopic exposures (p. 9-10).
- Detectors 11, 13, 14, 44 have the strongest and most contrasted persistence.
- Persistence is temporally non-stationary (about 10% decline over 2024-2026) and depends on saturation history (p. 6-7).
- The photometric model amplitudes are quoted for the photometric integration time only.

## Implications for extended-galaxy photometry, 2-D modelling and low-surface-brightness work
- Residual NISP background structure of up to about 2% of a roughly 100 e- sky (and 5% in the worst detectors) is a systematic for LSB work in YE/JE/HE. This is a few percent of the sky level and so the same order as or larger than the surface brightness of faint outskirts. Expect detector-pattern background residuals that correlate with HPR morphology (semicircular regions). Large-scale background modelling of NISP images should be treated with caution.
- JE is the most affected band (it follows the spectroscopic exposure), then HE and YE. Treat JE faint-feature measurements with extra caution.
- Masked pixels reduce effective coverage per dither. Check the coverage and mask maps around large galaxies, because a conservative mask can cut across extended galaxies.
- The paper has no VIS component. Persistence is NIR only, and so is irrelevant to VIS LSB work.
- Bright galaxy cores and stars in dithered exposures can leave self-persistence in the same dither (a few pixels offset), which can alter central and halo flux in NISP bands.

## Practical recommendations for users
- Do use the DR1 persistence masks and respect the NISP masked and flagged pixels (names are in the DR1 processing paper).
- Do verify NISP background residual patterns near the 4 strongest-persistence detectors (11, 13, 14, 44) before trusting NISP outskirts or LSB profiles.
- Do prefer HE or YE over JE when faint structure is critical and a choice exists.
- Don't treat masks as a guarantee that all persistence is removed (model underpredicts early persistence by 2.5-3.5x for sources).
- Don't assume stable amplitudes: persistence varies with time and saturation history.
- Expect a possible reprocessing with lower masking in future releases (3 h, 5 e-).

## Objects, fields and figures worth revisiting
- Field: SkyPatch 38 in the Euclid Deep Field North (EDF-N), 2024-06-12 to 14, DET13. No coordinates are given.
- No named galaxies are studied.
- Key figures: Fig. 1 (persistence maps across detectors, p. 5); Fig. 2 (HPR/LPR, p. 6); Fig. 9 (NoiseChisel background in spectroscopic vs photometric exposures, p. 10); Fig. 10 (model vs science data, p. 12); Fig. 12-13 (masked fractions and thresholds, p. 13).

## Cross-references
- Polenta et al. 2026a (DR1 processing; mask details) and Polenta et al. 2026b (Q1).
- Kubik et al. 2026 (A&A 707, A230; NISP detectors and readout).
- Romelli et al. 2026 (NIR/VIS catalogue and spurious detections from persistence); Copin et al. 2026 (spectroscopy).
- Awad et al. (in prep.; persistence correction methods).
- Jahnke et al. 2025; Schirmer et al. 2026 (performance verification).
