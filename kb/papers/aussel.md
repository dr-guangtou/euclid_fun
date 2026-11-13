---
title: "Euclid First Data Release 1 (DR1): Data release overview"
short_name: aussel
first_author: Aussel
series: A&A Special Issue DR1-Foundation (Nov 2026)
local_pdf: ~/Desktop/euclid/papers/aussel.pdf
local_text: ~/Desktop/euclid/text/papers/aussel.txt
topics: [DR1-Foundation, release overview, EWS, EDS, EAF, EMDS, data products, data volume, processing functions, VMPZ-ID masks, EXT, photo-z, spectra]
relevance_extended_galaxies: medium
---

# DR1-Foundation data release overview (Aussel et al. 2026)

## TL;DR
Top-level map of what DR1-Foundation (public 12 Nov 2026) contains: about 12 months of Euclid survey data (about 2000 deg2 wide plus 77 deg2 deep, plus calibration, auxiliary, and special fields), with LE1 raw frames, LE2 calibrated frames, stacks, catalogues, spectra and HEALPix masks. Weak-lensing shear and Level 3 cosmology products follow in June 2027, but nothing in Foundation will be reprocessed. For galaxy-imaging users it defines which fields and data sets exist, which processing function (PF) produced what, and where the known problems are (EXT Pan-STARRS flags, NIR astrometry tail, VIS PSF size underestimate, no NISP in some sets). It is a signpost paper; pixel-level and catalogue-column details are in the VIS, NIR, MER, VMPZ-ID papers.

## Key facts and numbers
- DR1 = DR1-Foundation (12 Nov 2026: LE1 + validated LE2 images, spectra, catalogues) + full DR1 (June 2027: shear measurements and LE3 weak-lensing/clustering products). DR1-Foundation products "will not be re-released" in 2027 (p. 1, 4, 10). DR2 (about 3 yr of survey) scheduled 2029; DR3 = full survey (p. 1, 10).
- Headline: around 1 billion catalogued objects; Wide Survey 1975 deg2 (EWS, in Table 3 NIR-valid area; VIS area 2092.2 deg2), Euclid Deep Fields (EDS) 77 deg2 (abstract p. 1; Table 3 p. 5). Total VIS area in Table 3: 2268.7 deg2 (p. 5). Conclusion: "around 2000 deg2", largest area observed from space in optical+NIR (p. 9).
- Mission timeline (p. 2): launch 1 Jul 2023; commissioning to 31 Jul 2023; PV from 1 Aug 2023 (FGS recommissioned 23-30 Sep 2023); PV to phase-diversity calibration (PDC) around 1 Dec 2023; survey start 14 Feb 2024; nominal survey end currently 2 Jan 2030. DR1 ends with last self-calibration block about 2025-05-21T19:12Z. About 8700 deg2 observed by writing time (p. 10).
- VIS "ice age": throughput loss from ice in the instrument cavity; decontaminations on 14 Mar 2024 and 8 Jun 2024; about 3 months early in the EWS (between them) is EXCLUDED from DR1 because of VIS photometric and PSF calibration uncertainty. Since then VIS throughput has dropped only 1-1.5% over about 2.5 yr (p. 2). NISP ice causes slow wavelength-dependent sensitivity change, not yet corrected for blue-grism data (p. 2).
- Instrument recap: 1.2 m mirror, 0.54 deg2 FoV; VIS IE resolution 0.18 arcsec; NISP YE, JE, HE imaging plus slitless grisms (p. 1). Nominal VIS exposure 565 s; PSF-field exposure 289 s (p. 4).
- EWS: two blocks, EWS-South about 1600 deg2 and EWS-North about 500 deg2 (p. 3). VIS: 17 143 nominal exposures collected out of 19 588 scheduled (about 87%) (p. 4); 16 913 validated LE2 IE frames over 2092.2 deg2; NISP-valid frames 16 111 (YE), 15 787 (JE), 15 977 (HE) with all-three-band area 1975.4 deg2 (Table 3, p. 5).
- EDS: EDF-N visited 11 times, EDF-S 10 times, EDF-F 2 times; each pass = single EWS-field depth; deep maximum-overlap areas EDF-N 24.3 deg2 (VIS)/19.8 (NISP), EDF-F 13.1/13.0, EDF-S 27.8/23.2; total 65.2 / 56.0 deg2; total EDF footprint 77.0 deg2 (Table 3). EDF-N 2408 IE exposures, EDF-F 184, EDF-S 1976. No EWS data under EDF-N; EDF-S area also observed as EWS; no EWS in EDF-F (Fig. 3 caption, p. 7).
- Red grism used throughout the EDS except 3 EDF-N passes in blue grism; target final blue:red effective exposure ratio about 25:15 (p. 3).
- EMDS (Euclid Medium-Deep Survey): about 1 mag deeper and 10x smaller than EWS; EMDS-1..4 with 15.1, 13.0, 15.9, 13.9 deg2 VIS. EMDS-1 and -2 taken during PDC thermal stabilisation with NISP idle: VIS only (p. 3, Table 3). EMDS-3/-4 NISP areas 15.7, 12.2 deg2.
- EAFs (calibration fields for photo-z and colour-gradient/chromatic-PSF tests): COSMOS, CDFS, AEGIS; total 4.8 deg2; 895 IE exposures (p. 3, Table 3). AEGIS has no EXT processing (p. 8).
- SelfCal field: about 2.0 deg2 near the north ecliptic pole, inside EDF-N and the continuous viewing zone (CALBLOCK-F-001, PV-001; extra CALBLOCK-F-014 monitoring data); 1215 IE exposures, 2.2 deg2. Together these form the Euclid Ultra-Deep Field (EUDF) to be released early 2027 (McCracken et al., in prep.) (p. 4).
- PSF-calibration fields (CALBLOCK-F-008): observed every 2-6 weeks, 100 dithers with 289 s VIS exposures each; 2130 IE exposures, 6.3 deg2; no NISP photometry LE2 (Table 3). VIS-only; NISP takes off-sky nonlinearity calibration meanwhile (p. 4).
- Other sets: ILS (Independent Legacy Scientists fields, 37.5 deg2 VIS), WAVES (WAVES-VISTA wide-area field, 14.8 deg2 VIS, no NISP LE2), SSO (Solar-system field near ecliptic, 19.2 deg2), F010 (1.8 deg2), F014 (1.6 deg2) (Table 3).
- LE1 counts, Table 2 (p. 5): total 48 524 scheduled observations; 39 274 VIS nominal, 13 375 VIS short, 30 764 NISP spectro, 30 221 YE, 28 562 JE, 28 562 HE frames; EWS: 17 143 VIS nominal, 8572 VIS short, 17 231 NISP per band.
- Data volume: about 1.7 PB (p. 8). More than 120 000 calibrated VIS+NISP frames (VIS 42 092 images per McCracken; NISP 80 695 calibrated frames, p. 9). More than 170 million validated 1-D spectra (red+blue), >60 million photometric quasar candidates, >1 billion catalogued sources. Galaxies (PHZ_CLASSIFICATION=2): over 900 million = EWS 817 846 065 + EDS 49 393 051 + EAFs 34 427 023 (p. 8). Photo-z and classification for 880 million sources over 1900 deg2 of EWS (p. 8).
- Processing cost: 35 million jobs, 6.7 million core hours (p. 9).
- NISP astrometry: 0.7% of DR1 area has error >50 mas; flagged in HEALPix map from VMPZ-ID (p. 5).
- Spectra: extracted for every MER-catalogue object with HE < 23.5 (one mag deeper than Q1); SPE redshifts vs DESI show scatter half that of Q1 (p. 8).

## Data products and data model
- LE1 (raw): VIS raw frame, NISP raw frame, HKTM housekeeping/telemetry. Only VIS+NISP raw frames are distributed in DR1-Foundation; HKTM comes with the full DR1 (used by SHE for pointing history) (p. 4).
- Observation identification: ObservationType = CALBLOCK-PV-XXX (PV) or CALBLOCK-F-XXX (routine); Observation ID (shared by the whole Reference Observation Sequence, ROS, in a field); Patch ID for contiguous survey patches (p. 2). Table 1 (p. 2): EWS = CALBLOCK-F-006; EDS = F-002 and F-003; EAFs = F-004, F-005 + PV ObsID 65879; SelfCal = F-001 except Patch 91a (lost to solar activity) + PV ObsIDs 65765, 65776, 65803, 65811; PSF = F-008 except Patch 158a; F-010; F-014; ILS = ObsIDs 65914-66048 (135); WAVES 66059-66190 (132); SSO 66202-66350 (149); EMDS-1 66358-66491; EMDS-2 66517-66660; EMDS-3 66680-66819; EMDS-4 66826-66962.
- Level-2 chain (Fig. 2, p. 6): VIS PF -> calibrated frames and stacks; NIR PF -> calibrated NISP frames (YE, JE, HE) and PSF models; EXT -> ground-based imaging (UNIONS in the north, DES in the south; plus Pan-STARRS and others in EDFs/EAFs); MER -> stacks on a common astrometric grid and multiwavelength catalogue (local noise level and new catalogue quantities vs Q1); PHZ -> photo-z, SED fits, classification, physical properties; SIR -> extracted 1-D spectra; SPE -> redshift, classification, line measurements; VMPZ-ID -> HEALPix masks and maps (effective coverage, astrometric-error map, EXT-quality map).
- MER processing variants per data set (Table 4, p. 8): "MER Wide" = standard per-ROS (EWS, SelfCal, F014); "MER Deep + Wide" = EDFs, EAF-COSMOS, EAF-CDFS (Deep combines all ROSs); "MER VIS + NIR" = triggered without EXT to enable SIR (AEGIS, F010, ILS, SSO, EMDS-3, EMDS-4); no MER for PSF, WAVES, EMDS-1, EMDS-2.
- VMPZ-ID only run on EWS and EDF data sets (p. 8).
- Archive: Science Archive System (SAS) via the Euclid Data Space, https://euclid.dataspace.esa.int; DR1 landing page https://www.cosmos.esa.int/web/euclid/data-release-dr1; DPDD (Data Product Description Document) at https://euclid.esac.esa.int/dr/dr1/dpdd; DR1 content memo Pettorino and Ferruit 2026 (p. 1-4). Catalogue column names are NOT listed here (see Kuemmel, Hartley, Le Brun, Odier).
- Key classification flag cited: PHZ_CLASSIFICATION = 2 means galaxy (p. 8).

## Processing and methods
- All DR1 data reprocessed with the SGS processing functions in a frozen DR1 configuration for homogeneity (p. 4). EXT reprocessing began May 2025; LE2 spectroscopic processing finished end Sep 2025; imaging LE2 up to PHZ ready mid-Sep 2025; SHE PSF and shape measurements end Oct 2025 (p. 4).
- VIS PF improvements: cosmic-ray rejection, photometric calibration, background estimation, coaddition (details in McCracken 2026a,b) (p. 4).
- NIR PF: updated in-flight calibration plan enabling better persistence masking (p. 5). NIR PSF modelled by da Silva et al.
- EXT: UNIONS (north) and DES (south) re-ingested, recalibrated and quality-assessed (Corcho-Caballero) (p. 6).
- MER: stacks plus detection and measurement; compared with COSMOS2025 (Shuntov 2025) in Gasparetto et al. (p. 6).
- PHZ: NNPZ reference sample now calibrated with EAFs (p. 8). SIR: extraction for all HE<23.5 sources with more efficient algorithm, better persistence flagging, full dispersion/curvature/PSF(lambda) calibration (p. 8).
- Validation by each Organisation Unit against science requirements; can take 1-2 months for complex products (p. 4).

## Validation and performance
- VIS/NISP astrometric and photometric precision stated "within requirements" (p. 9); mission data reliability: >99% of pre-planned science and telemetry files retrieved (p. 4); about 87% of scheduled EWS VIS exposures delivered as valid and complete (p. 4).
- SPE vs DESI redshifts: good agreement, scatter half that of Q1 (p. 8).
- Details of numeric validation live in the individual papers (Table 5, p. 10).

## Known issues, caveats, limitations
- VIS PSF model underestimates VIS PSF size (found early 2026); this compromised shear, hence the staggered release with SHE in June 2027 (p. 4). Implication: any PSF-model-based product (PSF images for shear) should be cross-checked; see McCracken/ the VIS PSF papers in prep.
- Ice-age period (about 3 months early EWS) excluded (p. 2). VIS throughput stable within 1-1.5% since.
- Incomplete EXT: Pan-STARRS flags incorrectly handled by SGS, giving areas of degraded EXT photometry; a HEALPix info map in VMPZ-ID flags them; not a UNIONS problem; fixed for DR2 (p. 6). EXT missing for AEGIS (p. 8). Missing stellar SEDs (EXT incomplete) limited PSF calibration (p. 4).
- NIR astrometry: 0.7% of area with error >50 mas; use VMPZ-ID HEALPix astrometric-error map (p. 5).
- MER absent for PSF, WAVES, EMDS-1, EMDS-2; MER VIS+NIR sets lack EXT photometry hence no PHZ-quality colours (p. 6, 8). EMDS-1/-2 are VIS-only.
- Spectra: an SPE entry exists for every HE<23.5 object, many with no measurable features; do not use redshifts blindly, use reliability flags (Le Brun 2026a) (p. 8). NISP ice evolution not corrected for blue-grism data (p. 2).
- Self-cal Patch 91a and PSF Patch 158a lost to high solar activity (Table 1 note, p. 2).
- Released data are not homogeneous: EDF visits are processed both as individual EWS-like observations and co-added deep stacks (p. 2).
- No shear/WL/LE3 catalogues until June 2027; HKTM not released yet.

## Implications for extended-galaxy photometry, 2-D modelling and low-surface-brightness work
- The overview itself gives no LSB depth numbers; consult McCracken (VIS), Polenta (NIR) and Kuemmel (MER) for background subtraction, sky-level handling and surface-brightness limits. This paper tells you which data sets exist for each use case.
- Deepest imaging for LSB/ICL on large galaxies and clusters: EDF-N/S/F deep stacks (MER Deep) and the future EUDF (SelfCal, early 2027); EMDS fields are about 1 mag deeper than EWS but VIS-only in EMDS-1/-2. EWS is the wide sample for statistical galaxy structure.
- Background estimation and coaddition were reworked for DR1 relative to Q1 (p. 4); check whether the extended-object sky-bias issues reported in Q1 persist (McCracken 2026a).
- MER "local noise level" and extra catalogue quantities are new vs Q1 (p. 6); Sersic/morphology catalogues are not described here.
- COSMOS EAF is the natural field for validating Euclid photometry against deep HST/ground data (COSMOS2025).
- Ground-based EXT (UNIONS, DES) can supply g/r/i/z/u optical context, and DES and UNIONS are also deep for LSB; but note Pan-STARRS-affected areas.

## Practical recommendations for users
- Start from the correct data set definition: select by Observation ID/Patch ID via Table 1, and check Table 3/4 to see whether VIS, NISP, EXT, MER exist for your field.
- Use the VMPZ-ID HEALPix maps to flag NIR astrometric outliers (>50 mas, 0.7% of area) and degraded Pan-STARRS EXT regions.
- Use PHZ_CLASSIFICATION = 2 to select galaxies; use SPE reliability flags, do not trust every redshift.
- For sub-arcsec morphology rely on IE (0.18 arcsec); NISP YE/JE/HE are coarser.
- Avoid DR1 for shear; the VIS PSF model size is known to be biased low.
- For extended-object work avoid fields without MER or without NISP (PSF, WAVES, EMDS-1/-2).
- Cite as DOI https://doi.org/10.57780/esa-d079c51 (DR1 data DOI).

## Objects, fields and figures worth revisiting
- Carousel Lens, strong-lens system at z = 0.49 (Fig. 1, p. 3), image 1.5 x 1.4 arcmin, north up east left; coordinates not given in this paper (literature: Huang 2021, O'Donnell 2022). Illustrates the quality gain from Q1 to DR1 processing; lens galaxy is a massive early-type.
- Fig. 2 (p. 6): DR1 data-processing and product flow diagram.
- Fig. 3 (p. 7): sky distribution of all DR1 data sets north/south (EWS-N/-S, EDF-N, EDF-S, EDF-F, EAF AEGIS and CDFS, SelfCal, etc.).
- Tables 1-4 (p. 2, 5, 8): data-set definitions, LE1 counts, LE2 frame counts/areas, MER types.
- Table 5 (p. 10): list of 18 supporting papers plus those in preparation (VIS PSF model/calibration, shear, MetaCal, photometric masks, ...).
- EAF fields: COSMOS, CDFS (in EDF-F centre), AEGIS (north); no coordinates given in this paper.

## Cross-references
- Tereno et al. (survey definition, fields, footprints); Ruffenach et al. (SGS architecture, processing statistics, Fig. 8 timeline); McCracken et al. 2026a,b (VIS); Polenta 2026a,b, Radovich, da Silva, Kubik (NISP); Corcho-Caballero (EXT); Kuemmel and Gasparetto (MER, photometry validation); Hartley and Enia (PHZ); Fumana, Copin, Scodeggio (SIR); Le Brun (SPE); Odier (VMPZ-ID masks); Schirmer 2026a,b (calibration; spacecraft L2 performance); earlier Q1 overview (Euclid Collab.: Aussel 2026, A&A 711, A1).
