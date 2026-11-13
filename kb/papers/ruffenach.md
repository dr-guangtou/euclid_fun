---
title: "Euclid Data Release 1 (DR1): An overview of the Science Ground Segment architecture and operations"
short_name: ruffenach
first_author: Ruffenach
series: A&A Special Issue DR1-Foundation (Nov 2026)
local_pdf: ~/Desktop/euclid/papers/ruffenach.pdf
local_text: ~/Desktop/euclid/text/papers/ruffenach.txt
topics: [Science Ground Segment, SDC, processing functions, EAS, Science Archive, TAP ADQL, Astroquery, Euclid Data Space, MER tiles, PF versions, DR1 production, data volume]
relevance_extended_galaxies: low
---

# Science Ground Segment architecture and DR1 operations (Ruffenach et al. 2026)

## TL;DR
Describes the distributed computing system that produced DR1: nine national Science Data Centres (SDCs), the Euclid Archive System (EAS) with a common data model, the orchestration layer (COORS, IAL), daily/on-the-fly processing and the DR1 production campaign (35 million jobs, 6.7 million core-hours, about 1.3 PB). For galaxy-imaging users the useful parts are: the pipeline chain (VIS/NIR/EXT -> MER -> PHZ/SHE/SIR/SPE -> VMPZ-ID), the MER tile geometry (30 arcmin wide tiles, 15 arcmin deep tiles), the frozen PF software versions used for DR1, the archive access routes (Science Archive TAP+/ADQL, Astroquery, ESASky, ESA Datalabs), and the MER photometry/morphology methods listed in passing (including 2-D Sersic fitting). Otherwise it is an infrastructure paper with little direct bearing on image analysis.

## Key facts and numbers
- SGS = ESA SOC (survey planning, LE1 production, Science Archive and Euclid Data Space) + EC SGS (processing). Processing at nine SDCs: FR, IT, NL, DE, UK, CH, FI, ES, US (p. 2-4, Fig. 2). Target shares: FR 25%, IT 25%, UK 10%, DE 10%, NL 10%, CH/ES/FI/US 5% each (Fig. 2). SHE is the most expensive PF (about 50% of budget) (p. 3).
- DR1 production perimeter (p. 12): Feb 2024 - May 2025 data; EWS 2375 deg2 input, three EDS fields 53 deg2 input, plus eight special categories (PV, calibration, auxiliary, PDC). Input excludes decontamination periods, technical reboots, high solar activity, and tiles crossing RA = 0 deg. (Note: this input perimeter differs from the validated areas in Aussel/Tereno.)
- 6942 Euclid observations processed (p. 10); distribution of EWS data across SDCs (Table 1, p. 10): 4897 observations, 2448 deg2 total: FR 1786 obs/893 deg2 (36.47%), IT 1772/886 (36.18%), UK 772/386 (15.76%), NL 231/115 (4.72%), FI 188/94 (3.84%), DE 148/74 (3.02%). Only 10% of observations duplicated to another SDC in the DR1 campaign (vs up to 75% in on-the-fly mode).
- Raw data volume: 18 TB VIS and 6 TB NISP raw frames; one VIS raw frame 1.2 GB uncompressed (400 MB compressed; 2.4 GB compressed per observation); one NISP raw frame 200 MB uncompressed, about 50 MB compressed, 800 MB per observation; EXT single-epoch frames about 315 GB (p. 10).
- Compute and output per observation (Table 2, p. 11): VIS 111.6 CPUh, 60 GB (26.0% of output); NIR 16.7 CPUh, 11 GB; MER 334.8 CPUh, 59 GB (25.7%); PHZ 167.4 CPUh, 1.8 GB; SHE PSF fitting 372 CPUh; SHE LensMC+Metacal 1255.5 CPUh (36.1% of compute); SIR 150.2 CPUh, 37 GB; SPE 418.5 CPUh; VMPZ 8.4 CPUh; EXT DES 41.9, CFIS 27.9, WHIGS 27.9, WISHES 44.6, Pan-STARRS i 502.2 CPUh/obs; total 3479.6 CPUh per observation and 231.1 GB per observation.
- DR1 campaign totals (p. 14): 34.4 million jobs via 200 830 Pipeline Processing Orders (PPOs); 774 CPU years (about 6.7 million hours); final archive 1.31 PB excluding EXT; PPO error rate 0.7%. Abstract and Aussel quote 35 million jobs. DR1 public volume 1.7 PB (p. 8). As of Jan 2026: 80 million files, 4.5 PB in the DSS across SDCs; metadata databases (DPS+DSS) 7.5 TB (p. 14).
- Daily operations (p. 11): about 4 h daily ground pass (Cebreros, New Norcia, or Malargue); about 100 GB per day; science files reach SOC about 4 h after pass; HKTM sync within 12 h.
- Tile geometry for MER processing: "wide tiles" with 30 x 30 arcmin core area, "deep tiles" with 15 x 15 arcmin core area (p. 12).
- Pipeline limits: a single pipeline can have up to 106 steps (p. 9). More than 100 pipelines overall (p. 7).
- Versions of PFs frozen for DR1 (Table E.1, p. 24): EXT 0.12.9; VIS 18.0.4; NIR 6.1.2; MER 11.3.1; SIR 6.0.2; LE3-ID-VMPZ 1.6.4 and 1.6.5; SPE 25.0.1; PHZ 2.16.13; SHE 9.12.2.
- DR1 timeline (Fig. 8, p. 13; stated in text): EXT processing launched May 2025; VIS/NIR parallel from June 2025; MER launched only after VIS/NIR validation by the OUs (not automatic); a calibration error found in validation forced reprocessing of 13 EWS sky patches and 7 EDS patches (MER invalidated and relaunched); late PHZ deliveries delayed SHE start to late Sep 2025.

## Data products and data model
- LE1 (SOC): VIS and NISP raw-frame products and HKTM products; aggregated FITS files with decompressed detector data, UTC timestamps and pointing information (p. 4).
- Common Data Model (CDM): one XML schema describing all interfaces; data products are XML metadata files referencing FITS data files in the DSS; a FITS Data Model (XML schemas per FITS file) underpins the Data Product Description Document (DPDD) at https://euclid.esac.esa.int/dr/dr1/dpdd/ (p. 7).
- Product levels: LE1 raw; LE2 (VIS, NIR, EXT calibrated frames and stacks; MER mosaics and catalogues; PHZ, SHE, SIR spectra, SPE catalogues); LE3 (WL, GC, clusters; NOT in DR1-Foundation) plus VMPZ-ID survey-characterisation products (p. 5-6, Fig. 3).
- VMPZ-ID products (p. 6): (i) survey footprint from MER tiling as a HEALPix Multi-Order Coverage map; (ii) bit masks from VIS, NIR, EXT combined into a unified coverage mask; (iii) instrumental/environmental information (noise maps, PSF characterisation, Galactic extinction, zodiacal light) for limiting magnitudes and visibility masks; (iv) depth maps from rms noise; (v) photometric visibility masks and random catalogues. (See Odier et al.)
- Science Archive content (p. 8): calibrated and stacked images of VIS and NIR, MER mosaics in all bands, SIR spectra, catalogues of MER (the "Euclid primary catalogue"), PHZ (photo-z) and SPE (spectroscopy) in several tables. Intermediate products and data lineage are not in the Science Archive.
- Access routes (p. 8): Euclid Science Archive with IVOA TAP+ (ADQL queries on large catalogues); Astroquery module for Python (programmatic queries, metadata inspection, bulk retrieval); Euclid Data Space https://euclid.dataspace.esa.int integrating the Science Archive, ESASky (interactive visualisation) and ESA Datalabs (Jupyter notebooks near the data; persistent personal and shared workspaces); DR1 comes with documentation and notebook examples for catalogue queries, images and spectra access, cutouts. The DR1 release also launches the Data Space publicly (p. 8).
- Mission Database holds key parameters and reference models (e.g. Galactic extinction map, telescope optical properties) under Configuration Control Board (p. 6).

## Processing and methods
- PF chain (p. 4-6, Fig. 3): LE1 -> VIS and NIR (in parallel, instrument-specific calibration) plus EXT -> MER -> PHZ and SHE (photometric branch) and SIR -> SPE (spectroscopic branch) -> VMPZ-ID -> LE3.
- VIS (p. 4): bias subtraction, crosstalk and non-linearity removal, brighter-fatter-effect modelling, PRNU flattening, then cosmic-ray rejection and source detection; astrometric calibration against Gaia DR3; per-exposure zero points from quality-selected Gaia DR3 stars in the self-calibration field; VIS_DifSpike diffraction-spike monitoring step (p. 12-13).
- NIR (p. 4-5): 16 HAWAII-2RG detectors; bad-pixel masking, dark-current subtraction, non-linearity correction, flat-fielding; persistence masking needing up to 5 h of exposure history (NIR_Persistence); astrometry vs Gaia DR3; photometric calibration based on a selected white dwarf observed in self-calibration visits; stacks per ROS with SWarp; catalogues and PSF models with PSFex.
- EXT (p. 5): UNIONS = CFIS + HSC + Pan-STARRS in the north; DES in the south; single-epoch frames calibrated, resampled onto the MER tile grid, stacked by weighted mean; stacked PSF models at source positions (source-by-source or ensemble depending on density). EXT sub-pipelines in Table 2: DES, CFIS, WHIGS, WISHES, Pan-STARRS i; also HSC.
- MER (p. 5): SExtractor++ detection independently on VIS and NIR (three-band) co-adds; photometry via Kron aperture, PSF-matched aperture, template fitting and 2-D Sersic profile fitting; morphology: CAS (concentration, asymmetry, smoothness) and FLUX_RADIUS. Tasks: MER_ProcessTile, MER_AnalyzeTile (p. 12).
- PHZ (p. 5): Phosphoros (Bayesian SED fitting) and NNPZ (nearest neighbour with COSMOS spectroscopic calibration), full photo-z PDFs; classification (star/galaxy/QSO) with probabilistic Random Forests; tomographic bins.
- SHE (p. 5): about 1.5 billion galaxies; physical PSF model; LensMC (forward modelling) and MetaCalibration.
- SIR/SPE (p. 5-6): spectra extracted using MER catalogue targets; SPE does redshift on discrete grids for galaxy/star/QSO, classification by chi2 evidence, emission lines by Direct Integration and Gaussian Fitting.
- Orchestration (p. 8-9): COORS Processing Plans -> PPOs; IAL (Meta-Scheduler + Pipeline-Runner, pilot-job model) at each SDC; Elastic Stack/Grafana monitoring at SDC-DE; Argo Workflows for automated on-the-fly chains (p. 12).
- Processing cases (p. 9-10): on-the-fly (OTF) near-real-time for instrument health and PF validation vs reprocessing for releases with fixed PF versions after a regression campaign on a representative subset. EDS handling (p. 13): each visit reduced independently in "wide-like" mode (EWS depth, external data down-selected), then a "full stack" deep reprocessing integrating all passes with a PHZ Deep pipeline and combined blue+red grism spectroscopy at deep tile level (using HSC and DES external data).
- Tile-level triggering via IntersectionMaps and coverage thresholds; observation-level PFs vs tile-level PFs (p. 12).
- Calibration scheduling: self-calibration monthly; VIS PSF monitoring / NISP nonlinearity every 2-6 weeks (p. 12).
- Validation: sky-patch Data Quality Check pipelines; calibration products validated by instrument scientists and then the Calibration Scientist (p. 12, 14).

## Validation and performance
- Pipeline-level only: 0.7% PPO error rate; reprocessing of 13 EWS + 7 EDS patches after a calibration error; regression campaigns before production (p. 10, 13-14). No image-quality metrics here (see McCracken, Polenta, Kuemmel).
- Profiling per task, e.g. MER initialise task resource use vs number of sources and Gaia sources per tile (Fig. D.1, p. 25).

## Known issues, caveats, limitations
- The paper does not list image-level artefacts; it documents process limits: no GPUs or multi-node MPI because of heterogeneous SDCs (p. 4); calibration error forced reprocessing of 20 patches (p. 13); late PHZ deliveries delayed SHE (p. 13-14); RA = 0 deg tiles omitted due to coordinate wrap handling, planned for later releases (p. 12).
- DR1 observations needing external ground-based data are only processed where EXT coverage and processing succeeded (p. 12).
- Input perimeter numbers here (EWS 2375 deg2, EDS 53 deg2) differ from the released/validated areas in Aussel (EWS 1975 deg2 NIR-valid; EDF 77 deg2) and Tereno (1900 deg2 LE2): do not mix these.
- Minor inconsistency: 35 million jobs (abstract) vs 34.4 million (p. 14).

## Implications for extended-galaxy photometry, 2-D modelling and low-surface-brightness work
- Mostly irrelevant to LSB scientific content. Relevant notes: MER stacks are produced per fixed grid tile (wide 30x30 arcmin core; deep 15x15 arcmin core), so very extended objects (nearby galaxies, clusters, ICL) can cross tile boundaries; MER photometry is per-tile, so check tile edges and use the MER mosaics (all bands in the Science Archive) for large objects.
- MER already includes Kron, PSF-matched aperture, template-fitting and 2-D Sersic fits plus CAS and FLUX_RADIUS, which gives baseline structural measurements and a cross-check for independent 2-D fits (details in Kuemmel et al.).
- VIS includes brighter-fatter-effect modelling, PRNU flattening, diffraction-spike monitoring; PSF models are generated (PSFex for NIR; SHE uses its own physical PSF model). Details for PSF/background belong to the VIS and NIR papers.
- EDS deep stacks ("full stack") are made in a separate reprocessing on deep tiles using HSC/DES external data: for LSB/ICL work these deep tiles and the per-visit wide-like products are separate product sets.
- VMPZ-ID depth maps from rms noise and masks are the SGS-provided route to limiting-depth and masking information.

## Practical recommendations for users
- Access: use the Euclid Data Space (https://euclid.dataspace.esa.int); TAP+/ADQL for catalogues; Astroquery module for scripted queries and cutouts; ESA Datalabs to avoid moving PB-scale data; follow the DR1 example notebooks (p. 8).
- Record the PF versions (EXT 0.12.9, VIS 18.0.4, NIR 6.1.2, MER 11.3.1, SIR 6.0.2, VMPZ 1.6.4/1.6.5, SPE 25.0.1, PHZ 2.16.13, SHE 9.12.2) in any paper (p. 24).
- Consult the DPDD for exact product and column definitions (p. 7).
- For deep fields, decide between per-visit wide-like products and the deep full-stack products.
- Do not use this paper as the source for field areas or depths (use Tereno, Aussel).

## Objects, fields and figures worth revisiting
- No named galaxies. Figures: Fig. 1 SGS organisation (p. 2); Fig. 2 SDC resources and sky share (p. 3); Fig. 3 PF/product flow diagram (p. 5; the base for Aussel Fig. 2); Fig. 5 OTF processing tasks (p. 12); Figs. 6-7 DR1 input northern/southern coverage (AEGIS, contamination scan, DEEP, self-calibration, PSF calibration, WIDE) (p. 13); Fig. 8 EWS and EDF-N processing timeline May-Nov 2025 (p. 13).
- Tables: Table 1 EWS sharing; Table 2 per-PF compute and output; Table 3 SGS resource roadmap 2024-2030 (cores and TB per SDC); Table E.1 PF versions.
- Appendix B (LE3 pipelines: WL, GC, clusters, random catalogues, KS+ mass mapping), Appendix C (IAL design), Appendix D (budget profiling) are infrastructure/cosmology specific.

## Cross-references
- Aussel et al. (overview; Fig. 2 adapted from Fig. 3 here, and states reprocessing timeline is in Fig. 8 here); Tereno et al. (surveys); McCracken (VIS); Polenta (NIR); Corcho-Caballero (EXT); Kuemmel and Romelli (MER); Hartley/Tucci (PHZ); Congedo (SHE); Copin/Scodeggio/Fumana (SIR); Le Brun (SPE); Odier (VMPZ-ID masks); Euclid Archive System and Euclid Data Space papers (in prep.); DPDD.
