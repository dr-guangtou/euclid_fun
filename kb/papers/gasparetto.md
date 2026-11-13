---
title: "Euclid Data Release 1 (DR1): Multi-band photometry validation on COSMOS extragalactic sources"
short_name: gasparetto
first_author: Gasparetto
series: A&A Special Issue DR1-Foundation (Nov 2026)
local_pdf: ~/Desktop/euclid/papers/gasparetto.pdf
local_text: ~/Desktop/euclid/text/papers/gasparetto.txt
topics: [OU-MER, photometry validation, COSMOS2025, SED fitting, aperture photometry, template fitting, Sersic model fitting, deblending, Eddington bias, IE YE JE HE]
relevance_extended_galaxies: high   # directly validates MER total fluxes (APHOT, TPHOT, SERSIC) on galaxies; weak on size dependence
---

# Multi-band photometry validation on COSMOS extragalactic sources (Gasparetto et al. 2026)

## TL;DR
The paper tests the three MER total-flux methods (A-PHOT aperture, T-PHOT template fitting, SE++ Sersic model fitting) on galaxies in the COSMOS deep and wide-like DR1 tiles. The reference is a set of IE/YE/JE/HE fluxes predicted by SED fitting of COSMOS2025 (JWST-based) photometry at fixed redshift. In general the MER fluxes are a few percent above the predictions (within about 10%), but the reference itself carries a similar uncertainty (the authors say the accuracy of the test is of the same order as the offsets). Template fitting is the most accurate in the NISP bands and towards faint magnitudes, while blended (deblended) objects have larger offsets, especially for aperture photometry. The test is on total fluxes of detected sources, not on structural parameters or surface-brightness profiles.

## Key facts and numbers
- COSMOS field centre RA = 150.119 deg, Dec = +2.21 deg, about 2.0 deg2 (p. 1). COSMOS2025 (C25, COSMOS-Web, released June 2025) covers 0.54 deg2, has more than 700,000 sources (784,016 in the catalogue), and uses JWST NIRCam F115W/F150W/F277W/F444W plus MIRI F770W with ground and HST data (p. 3).
- DR1 COSMOS data: repeated observations 22-28 Nov 2024 stacked for deep tiles. 60 deep tiles are released, 19 overlap C25. Wide data is a single observation of that campaign. Eight wide tiles overlap C25 (p. 2). Wide extended tile area is 32'x32'; deep is 17'x17' (p. 2). Tile ID prefixes: deep 10154xxxx; wide 1020xxxxx (Fig. 1, p. 3). Wide data in the archive: Header.DataSetRelease==COSMOS-WIDELIKE-DR1 (p. 2, footnote 1).
- MER sources in the C25 footprint: 477,600 (deep), about 91% detected in IE (VIS_DET=1); 200,201 (wide), about 74% IE-detected (p. 2).
- C25 sample selection: LePhare type=0 (galaxies), warn_flag=0, abs(mag_model_f444w) < 30, flag_star_hsc=0, leaving 576,143 galaxies. S/N > 10 in all four NIRCam bands leaves 15,268 (spec-z) and 120,008 (photo-z) sources. Spec-z: quality_flag >= 3 (CL > 95%) from the Khostovan et al. 2025 compilation; photo-z from the zfinal column; only 5% of sources have |dz|/(1+z) > 0.1 between spec and photo (p. 4).
- SED fitting: zphot code, redshift fixed. 37 C25 filters (0.32 to about 10 um; 34 used) plus the 4 Euclid filters. Bruzual and Charlot 2003, delayed exponential SFH (tau 0.1-7 Gyr), Chabrier IMF, Calzetti extinction E(B-V) up to 1.1, 2%-250% Z_sun, z 0-10 in steps of 0.025 (App. B, p. 20). Reduced chi2 cut: < 4 for spec-z and < 2 for photo-z (about 70% of fits kept) (p. 5).
- Cross-match with stilts, 0.1" radius. Final samples: spec-z deep 8631, wide 9081; photo-z deep 69,729, wide 54,146 (p. 7). A further cut of MER S/N > 3 per band and method (p. 7).
- Median relative flux offset (MER minus prediction)/prediction (Table C.1, p. 25; limits: mag 25 wide / 27 deep for IE, 24 wide / 25 deep for NIR). Wide, deep values:
  - IE: SERSIC spec 0.033, 0.027; photo 0.012, 0.034. APHOT spec 0.029, 0.038; photo 0.017, 0.041. No TPHOT in IE.
  - YE: SERSIC spec 0.036, 0.049; photo 0.071, 0.129. APHOT spec 0.031, 0.042; photo 0.064, 0.070. TPHOT spec -0.002, 0.030; photo -0.010, 0.052.
  - JE: SERSIC spec 0.030, 0.042; photo 0.068, 0.116. APHOT spec 0.014, 0.031; photo 0.035, 0.053. TPHOT spec -0.015, 0.021; photo -0.026, 0.039.
  - HE: SERSIC spec 0.055, 0.054; photo 0.085, 0.116. APHOT spec 0.029, 0.037; photo 0.044, 0.048. TPHOT spec 0.006, 0.032; photo -0.012, 0.039.
- Abstract: deep photo-z model-fitting NIR offsets of about 12-13%; all other cases well within 10% (p. 1, Table C.1).
- Reference check: for the 4 HSC bands (deep only) MER fluxes are about 5-8% below C25 in HSC g and r (mag 21-25) (p. 8) and close to zero in HSC i (SERSIC about -0.5%). zphot underestimates the HSC fluxes by 3-5% relative to C25 (p. 12, Fig. D.1), which suggests the positive MER-minus-prediction offsets may be partly an artefact of the SED fit.
- The check of C25 vs zphot over 37 bands: median differences within 5-10%, with no wavelength trend. IRAC ch1 and ch2 show the largest offsets (p. 10, App. D). Convolving C25 SEDs with Euclid filters agrees with zphot to 5-10 mmag at bright mags (Fig. A.1).

## Data products and data model
- MER products named (p. 2): MerBksMosaic (background-subtracted mosaic per band, the base for photometry); MerDetectionMosaic; MerSegmentationMap; MerFinalCatalog (all sources; plus a deep photometric catalogue for deep tiles).
- Catalogue columns and flags used: VIS_DET (1 = detected in IE, 0 = NIR-stack detection); DEBLENDED_FLAG (0 = not affected by deblending, 1 = initially contaminated by neighbours and then split by ASTErIsM) (p. 7, footnote 11); FLUX_DETECTION_TOTAL (flux in an ellipse of 2.5 Kron radii, Eq. 2 of Romelli et al. 2026; this is the IE total flux under APHOT); FLUX_*_TEMPLFIT and FLUX_VIS_TO_*_TEMPLFIT (T-PHOT template-fit fluxes and VIS-to-band template colours) (p. 7, App. C.4).
- Total-flux recipes (p. 7, 22): APHOT in NIR = flux within a 2 FWHM aperture in the NIR band times the ratio of IE Kron flux to the IE 2 FWHM flux (both on images PSF-matched to the worst PSF of the data set, typically a ground-based EXT band). TPHOT total: either the FLUX_*_TEMPLFIT columns taken directly as totals ('TPHOT'), or a colour term scaling the Kron detection flux: Flux_J = FLUX_DETECTION_TOTAL x FLUX_J_TEMPLFIT / FLUX_VIS_TO_J_TEMPLFIT ('TPHOT-color'). The two differ by only 1-2% here (Fig. C.7), while Kong et al. (in prep.) find larger differences in favour of TPHOT-color. SERSIC = SE++ Sersic 2D total flux. The exact column names of the SERSIC and APHOT aperture fluxes are not given; refer to the Photometry Cookbook (PCQ1: euclid.esac.esa.int/dr/q1/dpdd/merdpd/merphotometrycookbook.html).
- COSMOS2025 columns: flux_model_* and flux_err-cal_model_* (Sersic total fluxes in microJy) in the extension 'PHOTOMETRY HOTCOLD AND SE++'; the 'LePhare' extension (type, zfinal, zchi2). Catalogue version 1.1 (p. 3).
- No new product is released by this paper.

## Processing and methods
1. MER photometry (three methods, summarised in MER25) is taken as given. Deblending uses ASTErIsM on SE++ detections (p. 7, footnote 11).
2. Build a reference: fit zphot SEDs to C25 Sersic-model total fluxes (flux_model) at fixed z and predict IE, YE, JE, HE.
3. Cross-match and cut by chi2, MER S/N > 3, VIS_DET=1, DEBLENDED_FLAG as stated; compute (MER - zphot)/zphot per magnitude bin with median and NMAD (Figs. 6-7).
4. Checks: HSC g/r/i/z direct comparison (Fig. 8); emission-line redshift windows excluded (Fig. D.3, negligible effect); MAG_AUTO vs Sersic as C25 inputs (Fig. D.4, consistent within errors); reprocessing of deep COSMOS tiles with a different ASTErIsM deblending configuration (Fig. 9).

## Validation and performance
- Bright and isolated sources: offsets of a few percent, no trend with magnitude down to about 23-24 (p. 7).
- Deep: positive bias of up to 5% at mag < 23. SERSIC is best in IE; TPHOT best in NIR bands, with almost no trend; model fitting has a larger bias at the faint end in NISP; APHOT a small positive bias at the very bright end (p. 7).
- Wide: IE flat across the magnitude range, SERSIC about 5% high at the bright end. All three methods turn up at the faint end of NISP, up to about +10%. TPHOT shows no bias to about AB 24 but slightly underestimates the brightest sources (p. 8). Consistent with synthetic source injection (Kong et al., in prep.).
- Eddington-like bias: all faint-end upturns lie at the same position relative to the 5 sigma limit in each HSC band (Fig. 13, p. 14), so they are a selection effect and not a measurement bias. In wide data it begins about 2 mag brighter than in deep (p. 20).
- The sign of the offset is opposite to the routine MER validation on Gaia stars, which are fainter than expected in YE, JE, HE (p. 8). The authors conclude that photometric validation approaches have intrinsic uncertainties.
- Spec-z deep sample: about 40% of matches have DEBLENDED_FLAG=1 (about 20% for photo-z) (p. 9). Deblended objects have larger offsets, strongly method-dependent: largest for APHOT; SERSIC and TPHOT differ little between the two classes; TPHOT is the least biased at faint magnitudes (p. 9-13).

## Known issues, caveats, limitations
- Deep-field deblending in DR1 is sub-optimal, in particular for bright, large galaxies with extended halos that are blended with a neighbour in the deep data but not in wide data. These sources are under-deblended, their segmentation map includes neighbour pixels and their flux is overestimated. This explains why the deep spec-z cross-match (8631) has fewer sources than the wide one (9081) (p. 8-9). A reprocessing with a new ASTErIsM configuration fixes the example (ID 686933); a full analysis is ongoing (p. 14).
- APHOT: segmentation does not cover the faint wings of galaxies, so pixels of neighbours can still contaminate aperture flux; NIR-detected sources (VIS_DET=0) are dominated by spurious detections in the wide catalogue and are excluded here (p. 2, 7, 13).
- The reference is itself model-based. There is no ground truth. C25 uses 2D Sersic fluxes (flux_model); JWST photometry may be affected by calibration, background subtraction, local sky variations and model assumptions (p. 12). zphot appears to underestimate flux by 3-5% (HSC test).
- The sample is restricted to S/N > 10 in JWST bands, IE-detected, S/N > 3 in MER, matched within 0.1" and excluding C25 stars/QSOs/warn_flag objects. It covers a single field at one Galactic latitude (p. 15).
- APHOT loses faint sources at S/N > 3 (fewer than the other methods beyond mag 23; worst in YE) (p. 13).
- Emission lines and breaks can bias the SED forecasts, but excluding the affected redshift ranges changed nothing.
- No dependence on galaxy size, ellipticity, Sersic index or morphology is analysed; "bright/extended" appears only through the spec-z sample being bright and through blending.

## Implications for extended-galaxy photometry, 2-D modelling and low-surface-brightness work
- The test samples bright, mostly compact-to-moderate galaxies with spec-z. For very large nearby galaxies (tens of arcsec and bigger) the paper offers no validation. Treat its offsets as a lower bound on systematics.
- The IE-detected total flux (FLUX_DETECTION_TOTAL, 2.5 Kron radius ellipse) is the anchor for APHOT totals; Kron-like apertures miss the outskirts of extended or low-surface-brightness galaxies. Sersic model fluxes extrapolate beyond the segmentation and can recover faint wings (SERSIC is the best method in IE here) but depend on the fit being appropriate (single Sersic).
- Under-deblending of large galaxies with extended halos in the deep tiles is directly relevant: expect inflated fluxes and merged segmentation maps around large galaxies and in groups or clusters. Use DEBLENDED_FLAG and inspect the segmentation.
- For multiband colours of extended galaxies, the T-PHOT fluxes are PSF-matched template fits and best for the NISP bands, per this paper. Colours from the Kron-scaled APHOT recipe rely on a fixed 2 FWHM aperture colour on PSF-matched images.
- For LSB/ICL work this paper only informs the total-flux level (about 1-5% positive offsets, up to about 10% towards the faint end), not the sky-subtraction or outer-profile accuracy.

## Practical recommendations for users
- Do use TPHOT for YE/JE/HE colours and totals for faint sources (to about AB 24 in wide). Do use SERSIC or APHOT in IE (comparable; SERSIC slightly lower offsets in deep).
- Do cut on VIS_DET=1 and consider DEBLENDED_FLAG=0 for clean photometry. For DEBLENDED_FLAG=1 avoid APHOT.
- Don't trust fluxes within about 1-2 mag of the detection limit (Eddington-like bias), or NIR-only detections in wide data.
- Do not use APHOT where S/N is low (fewer sources survive S/N > 3).
- Do expect a few percent positive offsets (up to about 5% deep, 10% faint wide) and treat them as uncertain at the same level.
- For deep COSMOS tiles, be aware of the deblending issue; DR2 or a reprocessing may fix it.
- Do not mix the TPHOT total with TPHOT-color without checking: they differ by 1-2% here.

## Objects, fields and figures worth revisiting
- COSMOS: RA 150.119, Dec +2.21 deg (p. 1); tile footprint RA about 149-151, Dec about 1-3 (Fig. 1, p. 3).
- C25 source ID 2112 (zfinal = 1.149), a well-constrained SED example (Fig. 5, p. 6). C25 source ID 686933: blended in the deep tile, correct in wide and in the reprocessed deep (Fig. 9, p. 11).
- Key figures: Fig. 6 (summary of median offsets, p. 8); Fig. 7 (offsets vs magnitude, p. 9); Fig. 8 (HSC bands, p. 10); Fig. 10 (DEBLENDED_FLAG, p. 12); Fig. 13 (Eddington bias, p. 14); Table C.1 (p. 25).

## Cross-references
- Romelli et al. 2026 (MER25, Q1) and Kummel et al. 2026 (MER26, DR1): photometry and deblending.
- Kong et al. (in prep.): synthetic source injection photometry test.
- Corcho-Caballero et al. 2026 (EXT); Polenta et al. 2026 (NIR); McCracken et al. 2026 (VIS).
- Shuntov et al. 2025 (COSMOS2025); Weaver et al. 2022 (COSMOS2020, only used for filter curves and context, with no direct comparison in this paper); Photometry Cookbook for Q1 (PCQ1).
