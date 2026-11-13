---
title: "Euclid Data Release 1 (DR1): The Euclid surveys at DR1"
short_name: tereno
first_author: Tereno
series: A&A Special Issue DR1-Foundation (Nov 2026)
local_pdf: ~/Desktop/euclid/papers/tereno.pdf
local_text: ~/Desktop/euclid/text/papers/tereno.txt
topics: [survey design, reference survey definition, ROS, EWS footprint, EDF, EAF, EMDS, ILS, calibration fields, PV, PDC, exposure maps, ice age, ECTile, field coordinates]
relevance_extended_galaxies: medium
---

# The Euclid surveys at DR1 (Tereno et al. 2026)

## TL;DR
Defines every sky component in DR1: the Euclid Wide Survey (EWS), the three Euclid Deep Fields (EDF-N, -S, -F), the Euclid Auxiliary Fields (COSMOS, CDFS, AEGIS), calibration fields (Self-calibration/EUDF, PSF fields, SMC planetary nebula), Performance-Verification (PV) fields including the 17 ERO fields, and the Phase-Diversity-Calibration (PDC) surveys (Euclid Medium-Deep Survey, ILS field, Ecliptic Survey). It gives field centres, areas, number of visits, exposure-count statistics, observing sequence (ROS) timing, and the reasons for coverage losses (ice age, missing ground data, outages). For galaxy-imaging users it tells you what depth/dither pattern a given field really has, which fields are deepest, and why EWS tiles are tilted and overlap by 14%. It is an operations/planning paper: no pixel-level photometry, but essential for choosing fields and understanding depth and PSF-orientation inhomogeneity.

## Key facts and numbers
- EWS requirement 14 000 deg2; EWS started 14 Feb 2024, nominal end 31 Dec 2029 (p. 1). DR1 = all complete LE1 data until 21 May 2025 (p. 1); 462.8 days from 14 Feb 2024 to 21 May 2025: 4 days special ops (SOPS), 1.2 days Galactic Bulge Survey (Q2), 457.6 days of RSD observing of which 46.8 days slewing (p. 8-9).
- DR1 RSD built from RSDs 2024A, 2024B (repair of 2024A, from 15 Jul 2024), 2024C (from 16 Nov 2024), 2025A (from 28 Feb 2025); RSD 2025A contains all DR1 information. 11 697 RSD observations in the DR1 period (p. 2, 8, 9).
- Reference Observing Sequence (ROS), p. 2-3: 4 dithers (S-pattern); in each dither a VIS exposure runs in parallel with NISP spectroscopy, then NISP YE/JE/HE photometry; first and second dithers also include a VIS short exposure during NISP YE; dither duration 996 s (first three) and 1006 s (fourth); ROS 4204 s excluding lead time (20 s), dither slews (70 s each) and field slew (>= 170 s); about 19 ROS per day. ROS-blue variant uses blue grism BGS000 in all dithers (used in some EDF/EAF visits). Dither slew 70 s; field slews 170-283 s.
- Field of view: common VIS+NISP FoV 0.525 deg2; tessellation tile 0.551 deg2 (p. 4). Original tile overlap about 4%; after the stray-light-driven change (AA restricted to -8.5 to -2.9 deg, SAA 87-120 deg) tiles tolerate up to 3.5 deg misalignment between FoV and tile position angle, giving mean overlap 14% (hence data are "a little deeper than planned", but survey efficiency is lower) (p. 4).
- Region of interest (RoI): 16 200 deg2 in two "mainlands" + two "islands" (p. 4). Polar caps at |ecliptic latitude| > 77.8 deg use local tessellations (22 sectors). Bright stars < 4 AB mag get exclusion radii.
- DR1 EWS area (p. 9-10): RSD-scheduled EWS footprint 2639.1 deg2 (already excluding 60.5 deg2 around bright stars) -> DR1 LE1 area 2099.3 deg2 (north mainland 560.7 deg2, south mainland 1538.6 deg2), a loss of 539.8 deg2; SGS-validated LE2 EWS area about 1900 deg2 (p. 1, 10, Table 6). Exclusions: ice age (328 obsIDs not re-observed in time, 147.4 deg2, of which 9.7 deg2 polar); no ground-based data (302.3 deg2, 633 tiles; DES south, UNIONS north); instrument outages (five, 53 tiles, 25.4 deg2); not executed (124 obsIDs, 56.5 deg2, including north-cap-06 delayed by second decontamination); RA = 0 h crossing tiles (39 tiles, extra 8.2 deg2 as 22 overlap with no-ground-data); solar-activity radiation hits: 94 EWS obsIDs (ObsIDs 8-14, 2757-2774, 3802-3812, 4861-4875, 5644-5660, 6580-6586, 7040-7052, 7074-7079) reducing useful area by 44.5 deg2 (already scheduled for re-observation).
- EWS in RSD 2025A: 5384 ROS observations (21 536 pointings); each ROS = one obsID (p. 9). 6313 other observations are EDF/EAF/calibration (p. 10).
- Ice age (p. 8-9): ice formed on optics in Feb 2024; decontamination 12-21 Mar 2024 (9 days), VIS data degraded again, second decontamination ended 12 Jun 2024 (5.5 days; first heating 6 Jun). VIS data 23 Mar - 7 Jun 2024 declared invalid. 1166 EWS obsIDs (1092 tessellation tiles + 74 polar) executed in this period; 838 tiles re-observed in RSD 2025A and in DR1; NISP observations were not invalidated but the observations were rescheduled with the ROS (p. 8-9). RSD 2025A also rescheduled EDF-N (3 visits), CPC-N (4 visits), polar caps (3 patches), COSMOS (1 visit), 12 infill patches totalling 1119 tiles.
- Q1 (19 Mar 2025) = one visit to each EDF + LDN 1641; ERO release was 23 May 2024; Q2 (Galactic bulge, 23-24 Mar 2025) released 24 Jun 2026 and not in DR1 (p. 2, 21). Commissioning data not in DR1 (lack metadata) (p. 2).
- Exposure map statistics (p. 12-13): EDF-S (10 visits, VIS): 40 dithers nominal, up to 48, median 33, half of pixels 31.5-34.5, none below 20. COSMOS (27 ROS visits, NISP): 108 nominal, up to 122, median 85; less homogeneous because all visits share one orientation (and its 180-deg rotation), imprinting an orthogonal detector-gap pattern. Self-calibration (VIS, 11 F-001 visits, 76 ROS-D1 pointings each): 836 exposures total, roughly circular 2.0 deg2 footprint.
- Cadence/special: SOPS 6 h every 4 weeks in RSD 2025A, every 8 weeks from RSD 2026A (p. 4).
- Fields included and coordinates in "Objects" section below.

## Data products and data model
- Operational (not user-facing science) products defined here: RSD (reference survey definition, XML `rsd.xml`, built with ECTile input files `ectile.cfg`, `targets.d`, `plan.d`, `wide-plan.d`, `backlog.d`, binary `survey.sur`); OSS (operational sky survey XML from ESSOT); ICR (instrument commanding requests); SSR_FD, SSR_DEBUG, ESS_EVENT, POR XML, CRFG (command request file group) delivered to MOC each planning cycle (p. 2-5, 13-14).
- Identification scheme: ObsID (one per ROS of 4 dithers; for calibration sequences one ObsID for a whole multi-pointing sequence); CALBLOCK names CALBLOCK-F-001, 007 through 018 (13 calibration blocks) and CALBLOCK-PV-xxx; F-002 = EDFs, F-003 = completeness/purity calibrations (CPC, EDF-N and EDF-S at fixed cadence with different orientations), F-004 = EAF colour-gradient calibration, F-005 = EAF photo-z calibration, F-006 = EWS, F-001 = self-calibration (ROS-D1, monthly), F-007 = VIS nonlinearity, F-008 = PSF field main VIS sequence (100 pointings), F-012 = PSF closed shutter, F-013 = single ROS at PSF field, F-015 = short PSF sequence, F-010 = planetary-nebula NISP calibration, F-014 = self-cal-centre throughput monitoring (p. 4, 12, 15).
- Field summary tables: Table 1 (EDFs/EAFs), Table 2 (RSD calibration fields), Table 3 (PV fields), Table 4 (PDC calibration fields), Table 5 (PDC science fields), Table 6 (survey summary, p. 23). Exposure maps in Fig. 7 and Appendix A (Figs. A.1-A.4; pixel counts of single-dither exposures per instrument).
- LE2 availability by component (Table 6, p. 23): EWS 1900 deg2 LE2; EDFs LE2 (RSD only; PV EDF data not in LE2); EAFs LE2 for RSD fields (only COSMOS PV-005 in LE2); calibration fields in LE2: only Self-calibration PV-001 and F-014; PV science fields (PV-006, PV-007/ERO, stray-light) LE1 only; PDC EMDS/ILS/EES LE2 per Aussel Table 3.

## Processing and methods
- RSD computation with ECTile (tools plan, wide, surv) in three stages (p. 2-7): Stage 0 configuration (orbit file, slew thresholds 130 arcsec/3.5 deg, dither pattern, SAA/AA constraints, RoI, tessellation, bright star and planet avoidance, ground-survey footprints (DES, UNIONS), SOPS); Stage 1 manual scheduling of EDF/EAF/calibration targets into a calibration plan with visibility windows by Sun ecliptic longitude; Stage 2 EWS filling of the remaining survey windows with patches via a "diffusion algorithm" (priority to high ecliptic latitude, minimise solar-angle changes, mainlands first, prefer DES/UNIONS coverage; DR1 RSDs prioritised south because DES came earlier). About 100 survey windows per RSD; up to about 200 tiles per 10-day patch. PSF fields scheduled in Stage 2 so that solar angles match the contemporary EWS patch.
- Replanning (p. 7-8): infill patches (backlog.d) recover gaps; RoI, tessellation, polar patches and EDF-S shape are frozen. Fast ("palaeolithic") and optimised ("neolithic") SOC replanning for decontamination.
- PV planning with LabVIEW-based scheduler: 31 PV CALBLOCKS split into 114 variants and 132 execution blocks, ten sets of SSR_FD (p. 15).
- PDC: phase-diversity wavefront calibration with out-of-focus (3.2 days) and in-focus (1.25 days) VIS runs PDC-2 to PDC-8 (PDC-1 earlier on NEP); thermal stability less than 10 mK (out of focus) / 60 mK (in focus); 7-day thermal stabilisation before each run (50 days total, 70% of PDC campaign of about 70 days); science fillers (EMDS, ILS, EES) observed during stabilisation with large patch overlaps and constant SAA/AA (p. 17-18). NISP had to be switched off during stabilisation of out-of-focus runs (60 mK baseplate temperature drop when NISP was turned off in PDC-2), which is why only EMDS-HSC-3 and -4 have NISP (p. 18-19).

## Validation and performance
- Not a validation paper; reliability numbers are coverage statistics (see Aussel: ~87% of scheduled EWS VIS exposures valid). Area bookkeeping from scheduled to LE1 to LE2 is the main quantitative output (2639.1 -> 2099.3 -> about 1900 deg2).
- DES/UNIONS coverage plus Rubin LSST later fills no-ground-data areas.

## Known issues, caveats, limitations
- Ice age data excluded; 328 tiles not yet re-observed (p. 9). Orientation of FoV relative to tessellation varies (up to 3.5 deg), so per-tile PSF/background orientation varies (p. 4).
- RA = 0 h crossing tiles cannot be processed by the SGS in DR1 and are excluded (fixed for DR2) (p. 9-10). Expect a stripe of missing tiles in the south (red stripe in Fig. 6, p. 11).
- Tiles without DES/UNIONS data (302.3 deg2) excluded; Pan-STARRS-handling issues are described in Aussel/Corcho-Caballero.
- Depth is non-uniform within fields: EDF/EAF depth peaks at the centre because each visit has a different position angle; "1-pass" area much larger than "design" area (Table 1, p. 10-11). Visits to EDF-N were lost (7 visits, PatchID 44 lost half of VIS data) (p. 10, Table 6).
- COSMOS exposure pattern is orthogonal/less homogeneous (single orientation + 180 deg rotation) (p. 12-13); NISP pattern more visible than VIS.
- DR1 depth state: EDF-N 28%, EDF-S 22%, EDF-F 4% of final depth; EAFs: COSMOS 36% (27/75 visits), CDFS and AEGIS 100% (p. 11, 23).
- EDF red:blue grism ratio is far from the 5:3 blue-to-red goal (DR1: EDF-N 8R+3B, EDF-S 10R+0B, EDF-F 1R+1B) (p. 10-11).
- PV fields other than Self-calibration (PV-001, F-014) and COSMOS (PV-005) cannot be processed to LE2 with the standard SGS (p. 17).
- EMDS far from original goal (500 deg2 at 6 visits): only 67 deg2 with at least 1 VIS pass, 43 deg2 with 4 VIS passes, 7.3 deg2 with 4 passes in both VIS and NISP; the two first EMDS fields have no NISP (p. 18-19). No plan to extend, but all five EMDS fields will be re-observed as EWS later.
- PSF-12 (high Dec) outside ground-based reach and later dropped from the PSF set; PSF-01 and PSF-02 lie outside the RoI (p. 12).

## Implications for extended-galaxy photometry, 2-D modelling and low-surface-brightness work
- Depth planning: single EWS visit = 4 dithers; deeper fields: EDF-N (11 visits), EDF-S (10), EDF-F (2), COSMOS (27), CDFS (34), AEGIS (18), EMDS (about 4-5 VIS passes in 4 of 5 fields), SelfCal/EUDF (deepest, 836 exposures from F-001 alone). EAFs and EDFs give the best LSB depth for a few deg2.
- Dither rotation: because every visit of an EDF/EAF has a different position angle, the PSF orientation, diffraction spikes and detector-gap footprints average out in EDFs (circular patterns in EDF-S exposure map) but not in COSMOS (single orientation + 180 deg), which matters for spikes, ghosts and gap-related depth variations that mimic LSB structure.
- EWS depth is slightly higher than nominal due to 14% mean tile overlap, and varies tile to tile: overlap strips will have more exposures; per-pixel exposure maps are required when quoting limiting surface brightness.
- ILS field (35.6 deg2 any exposure, 26.5 deg2 with at least 1 ROS, depth 1-2 x ROS; 135 obsIDs) was selected primarily to study dwarf/LSB galaxies in the local volume (p. 19-20) and overlaps WAVES-Wide South with KiDS/VIKING data: a good test bed for LSB dwarf detection.
- EMDS-HSC fields overlap HSC-SSP (very deep grizy ground data) -- ideal for cross-checking Euclid VIS photometry/LSB against HSC for extended galaxies; VIS only in HL-1, HL-2.
- Irrelevant: operations sections (ESSOT, SSR/POR generation, PV scheduler).

## Practical recommendations for users
- Check field depth with exposure maps (Figs. 7, A.1-A.4) rather than assuming nominal depth; compute local exposure counts.
- For LSB/ICL/halo work prefer EDFs, COSMOS, CDFS, AEGIS and the Self-calibration area; for statistical samples use EWS with LE2 validation (about 1900 deg2).
- For EWS targets near RA = 0 h (south) or in ice-age gaps expect no data; verify coverage before targeting.
- EMDS-1/-2 and ILS are partly VIS-only/NISP-limited; check NISP footprints (LE1 vs LE2 differ, e.g. NISP-only exposures on edges of EMDS-WAVES-S are not in LE2) (p. 19).
- Use ObsID/CALBLOCK to pick calibration vs science frames; do not mix CPC-N/-S visits unintentionally (they are EDF-N/S visits at special orientations used for spectroscopy completeness/purity but they still count as depth).
- When using Q1 data, note it is a subset (1 visit per EDF) of DR1 EDFs.

## Objects, fields and figures worth revisiting
- EDF-N: RA 269.733, Dec +66.02; 20.0 deg2 design / 30.6 deg2 1-pass; 11 of 40 visits (8 red, 3 blue). EDF-S: RA 61.241, Dec -48.42; 22.7 / 33.0 deg2; 10/45 (10R). EDF-F (Fornax): RA 52.932, Dec -28.09; 10.0 / 13.2 deg2; 2/52 (1R, 1B) (Table 1, p. 11).
- EAFs: COSMOS RA 150.120, Dec +2.21, 2.0/2.6 deg2, 27/75 visits; CDFS RA 53.118, Dec -27.81, 0.5/0.8 deg2, 34/34 (sits in EDF-F centre); AEGIS RA 214.827, Dec +52.82, 1.0/1.4 deg2, 18/18 (Table 1).
- Self-calibration centre RA 268.813, Dec +65.29 (2.0 deg2; 11 F-001 ObsIDs, 2.3 deg2 1-pass); SelfCal-faint RA 268.000, Dec +65.00 (F-007 nonlinearity); NEP RA 270.000, Dec +66.56; EUDF will come from these (Table 2/3, p. 12, 16).
- PN SMC-SMP-20: RA 14.035, Dec -70.30 (NISP wavelength calibration, 456 pointings).
- PSF fields (centres RA/Dec): PSF-01 292.48/+53.53, PSF-02 285.03/+49.83, PSF-04 265.72/+48.09, PSF-05 254.20/+49.37, PSF-06 247.27/+52.69, PSF-07 239.80/+56.89, PSF-09 225.35/+61.91, PSF-12 218.16/+82.06, PSF-16 59.25/-55.16, PSF-18 73.52/-49.10 (Table 2); PDC extras PSF-10 221.47/+67.43, PSF-23 87.60/-47.50, PSF-24 265.07/+71.35, Polarised 328.00/+70.76 (Table 4).
- PV calibrators: WDJ175318+644502 (268.345, +64.76); GRW+70 (204.650, +70.28); VIS-AST-1 (LMC, 90.000, -66.50); alpha Lyr (279.858, +39.50); HD 165906 (271.109, +64.83); Euclid Blank Fields EBF-06 (257.790, +19.47), EBF-08 (43.945, -17.63), EBF-10 (350.268, +1.32), EBF-12 (0.251, -75.21); LDN 1641 (85.754, -8.39) (Table 3, p. 16).
- PDC science fields (Table 5, p. 19): ILS-WAVES-S (355.7, -31.2; intersects Blanco 1 open cluster at 234 pc, ten new ultracool cluster-member candidates); EMDS-WAVES-S (8.2, -30.7); EMDS-HSC-HL-1 (208.9, +43.5); HL-2 (237.2, +44.2); HL-3 (214.7, +44.3); HL-4 (230.2, +43.6); SSO-ECLIPTIC (9.8, +4.2; about 4000 trailed moving objects).
- ERO fields (PV-007, 17 fields, 6 programmes, 24 h of data; listed on Fig. 14, p. 22, no coordinates in this paper): Horsehead, Messier 78, Taurus, Barnard, NGC 6254, NGC 6397 (globular clusters), nearby galaxies NGC 6822, Holmberg II, IC 10, IC 342, NGC 2403, NGC 6744, Fornax cluster, Dorado group, Perseus cluster, Abell 2390, Abell 2764. (Approximate literature positions, not from the paper, to be verified: NGC 6822 296.24/-14.80; IC 10 5.07/+59.30; IC 342 56.70/+68.10; NGC 2403 114.21/+65.60; NGC 6744 287.44/-63.86; Holmberg II 124.77/+70.72.) Good demo targets for nearby extended galaxies and clusters (ICL in Perseus, Fornax, A2390, A2764), but only LE1 in DR1 (not LE2) per Table 6 (check Cuillandre 2025 for ERO products).
- Key figures: Fig. 1 ROS timeline (p. 3); Fig. 3 visibility windows with 3.5 deg tilt (p. 6); Fig. 4 DR1 schedule timeline (p. 9); Fig. 6 EWS DR1 footprint with exclusion categories (p. 11); Fig. 7 exposure maps (p. 13); Fig. 14 complete survey map (p. 22); Table 6 summary (p. 23).

## Cross-references
- Aussel et al. (DR1 overview, LE2 counts and products); Ruffenach et al. (SGS and processing); Schirmer et al. 2026a (calibration strategy, CALBLOCK list) and 2026b (spacecraft, ice); McCracken et al. (VIS); Polenta et al. (NIR); Corcho-Caballero (EXT: DES, UNIONS, HSC, KiDS); Scaramella et al. 2022 (survey design); Mellier et al. 2025 (mission); Cuillandre et al. 2025 (ERO); Q1 overview (Aussel 2026a); Q2: Beaulieu et al.; Miller et al. in prep. and Neumann et al. 2026 (PSF/wavefront); Pontinen et al. and Irureta-Goyena et al. (EES asteroids).
