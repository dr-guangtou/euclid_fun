# Glossary: Euclid DR1 acronyms and jargon

> Alphabetical. One-line definitions with a pointer to the KB note or paper summary where the term matters. Sources: the paper
> summaries in [papers/](papers/), the DPDD notes in [data_model/](data_model/), archive help pages and the acronym tables of
> [Tereno+26](papers/tereno.md) (survey/operations) and [Ruffenach+26](papers/ruffenach.md) (ground segment). Note pointers: 
> [01](01_dr1_overview.md) overview, [04](04_imaging_processing.md) imaging processing, [05](05_psf.md) PSF, [07](07_photoz_physical_parameters.md)
> photo-z/physical parameters, [08](08_spectroscopy.md) spectroscopy, [10](10_low_surface_brightness.md) LSB.
>
> Processing-function (PF) chain in one line: LE1 (raw) -> VIS, NIR, EXT -> **MER** -> **PHZ**, **SHE** (photometric branch) and
> **SIR** -> **SPE** (spectroscopic branch) -> **VMPZ-ID** -> LE3 (WL, GC, clusters; not in DR1-Foundation) (Ruffenach+26, p. 4-6).
> Items not defined in the local sources are marked as such (SLE, PDCC).


## A

| Term | Definition | Where |
|---|---|---|
| **AA (alpha angle)** | Euclid's roll angle about the boresight, one of the two attitude angles constraining pointing; with SAA it fixes the spacecraft attitude (stray-light-driven range -8.5 to -2.9 deg in the survey design). | [Tereno+26](papers/tereno.md) |
| **ADQL** | Astronomical Data Query Language, the SQL dialect used by the TAP service of the archive (joins on `object_id`). | [07](07_photoz_physical_parameters.md), [08](08_spectroscopy.md) |
| **AEGIS** | Euclid Auxiliary Field (strip) for colour-gradient calibration; no EXT (ground-based) processing in DR1. | [Tereno+26](papers/tereno.md); [Aussel+26](papers/aussel.md) |
| **Amazed** | Redshift engine of the SPE PF (its error codes appear in the SPE flag tables). | [dpdd_spectroscopy.md](data_model/dpdd_spectroscopy.md) |
| **A-PHOT** | MER aperture photometry on PSF-matched cutouts: `FLUX_<band>_<n>FWHM_APER`, circular apertures of n x FWHM (n = 1-4) of the worst-PSF band; basis of colours and of PHZ input. | [Kuemmel+26](papers/kuemmel.md); [dpdd_mer.md](data_model/dpdd_mer.md); [07](07_photoz_physical_parameters.md) |
| **ASTErIsM** | Clustering-based (DBSCAN/DENCLUE) software component used by MER to deblend sources on the VIS and NIR detection images. | [Kuemmel+26](papers/kuemmel.md); [Q1 MER](papers/q1_romelli_mer.md) |
| **astroquery (`astroquery.esa.euclid`)** | Python client for the Euclid archive (TAP queries, cutouts, `get_product`, `get_spectrum`, `get_datalinks`); PyPI 0.4.11 failed for DR1 cutouts, git main works. | [verified_on_archive.md](data_model/verified_on_archive.md); [08](08_spectroscopy.md) |
| **AUX / AUX fields** | In PHZ the combined COSMOS + CDFS auxiliary-field test sample; see EAF. | [Hartley+26](papers/hartley.md) |

## B

| Term | Definition | Where |
|---|---|---|
| **BC03** | Bruzual & Charlot stellar-population models; used for the PHZ physical-parameter labels and for the SPE galaxy continuum. | [Enia+26](papers/enia.md); [Le Brun+26](papers/lebrun.md) |
| **BGMOD (`EUC_MER_BGMOD-*`)** | MER background-model mosaic (the sky that was subtracted); add it to BGSUB to undo the MER sky step; cutout service fails for it (HTTP 500). | [verified_on_archive.md](data_model/verified_on_archive.md); [10](10_low_surface_brightness.md) |
| **BGS (blue grism)** | NISP blue grism BGS000, 926-1366 nm, 1.239 nm/px; used only in Euclid Deep Fields in DR1. | [Fumana+26](papers/fumana.md); [08](08_spectroscopy.md) |
| **BGSUB (`EUC_MER_BGSUB-MOSAIC-*`)** | MER background-subtracted mosaic (`DpdMerBksMosaic`), the science image per tile and band (VIS in ADU/s, NIR in electron/s, 0.1"/px). | [verified_on_archive.md](data_model/verified_on_archive.md); [Q1 MER](papers/q1_romelli_mer.md) |

## C

| Term | Definition | Where |
|---|---|---|
| **CalBlock (CALBLOCK-PV-xxx, CALBLOCK-F-xxx)** | Calibration block: a named calibration observing sequence (PV-xxx in performance verification, F-xxx in routine operations: F-001 self-calibration, F-002 EDFs, F-003 CPC, F-004/F-005 EAFs, F-006 EWS, F-008 PSF fields, F-010 PN, F-014 self-cal-centre monitoring); `calblock_id_list` in tables. | [Tereno+26](papers/tereno.md); [Schirmer+26 calibration](papers/schirmer-calibration.md) |
| **CalF** | Calibration Framework: the in-flight calibration plan (18 CALBLOCKs) derived from the mission requirements. | [Schirmer+26 calibration](papers/schirmer-calibration.md) |
| **CAS** | Concentration-Asymmetry-Smoothness (plus Gini and M20) morphology parameters measured by MER on VIS-detected sources. | [Kuemmel+26](papers/kuemmel.md); [dpdd_mer.md](data_model/dpdd_mer.md) |
| **CDFS** | Chandra Deep Field South; EAF for photo-z calibration, inside EDF-F (`deep_mode` data group); duplicated object ids with EDF-F. | [Tereno+26](papers/tereno.md); [08](08_spectroscopy.md) |
| **Chabrier IMF** | Initial mass function assumed by the PHZ physical parameters (ECLIPSE-D uses Salpeter, about +0.2-0.25 dex higher masses). | [Enia+26](papers/enia.md); [Nersesian+26](papers/nersesian.md) |
| **COORS / IAL** | COmmon ORchestration System (Processing Plans to Pipeline Processing Orders) and Infrastructure Abstraction Layer (meta-scheduler + pipeline runner at each SDC). | [Ruffenach+26](papers/ruffenach.md) |
| **COSMOS** | Cosmic Evolution Survey field (PV-005 / EAF); the sole source of the PHZ reference sample (2 deg^2, COSMOS2020 CLASSIC); also the blue-grism line-map test field. | [Hartley+26](papers/hartley.md); [Gabarra+26](papers/gabarra.md) |
| **CPC** | Completeness and Purity Calibration: repeated EDF visits with different orientations to decontaminate spectra (F-003). | [Tereno+26](papers/tereno.md) |
| **CRV / IDS / OPT** | SIR geometric calibration models: trace curvature, inverse dispersion solution, optical (sky to focal plane) model. | [Fumana+26](papers/fumana.md) |

## D

| Term | Definition | Where |
|---|---|---|
| **Datalabs (ESA Datalabs)** | ESA Jupyter e-science platform next to the archive; read files via `datalabs_path` without downloading. | [Ruffenach+26](papers/ruffenach.md); [08](08_spectroscopy.md) |
| **DataLink** | IVOA protocol used by the archive to expose spectra (double-chain icon in the web GUI; `get_datalinks`/`get_spectrum` in astroquery). | [08](08_spectroscopy.md) |
| **DECam / DES** | Dark Energy Camera and Dark Energy Survey: ground-based g, r, i, z in the southern sky (EXT). | [Corcho-Caballero+26](papers/corcho-caballero.md) |
| **deep_mode / deep_survey / deep_visits (data groups)** | Archive data groups: `deep_survey` = EDF-N/F/S deep stacks, `deep_mode` = CDFS and COSMOS deep processing, `deep_visits` = every individual EDF visit at EWS depth. Wide groups: `wide_survey` (EWS) and `wide_mode` (everything else wide-like); PHZ/SPE/SIR merge them into `wide`. | [07](07_photoz_physical_parameters.md); archive help `Catalogues.md` |
| **DESI** | Dark Energy Spectroscopic Instrument; main external spec-z truth (DR1) for PHZ and SPE validation; not an archive table. | [Hartley+26](papers/hartley.md); [Le Brun+26](papers/lebrun.md) |
| **DET_QUALITY_FLAG** | MER detection-step flag; non-zero means the Kron flux and `MAG_STARGAL_SEP` may be corrupted; standard cut `< 4`. | [dpdd_mer.md](data_model/dpdd_mer.md); [Dunn+26](papers/dunn.md) |
| **DPDD** | Data Product Description Document: official per-product column/format documentation (euclid.esac.esa.int/dr/dr1/dpdd); known to differ from the archive in places. | [dpdd_*.md](data_model/dpdd_mer.md); archive help `Some_columns_described_in_the_DPDD_are_not_available_in_the_archive` |
| **Dpd... (e.g. `DpdPhzPfOutputCatalog`)** | Data product descriptor: the XML metadata product that references FITS files in the archive; named per processing function. | [Ruffenach+26](papers/ruffenach.md); [dpdd_phz.md](data_model/dpdd_phz.md) |
| **DQ / DQC** | Data quality (pixel mask extensions in frames, e.g. SIR `DETn.DQ`) / data quality control parameters. | [dpdd_spectroscopy.md](data_model/dpdd_spectroscopy.md); [Fumana+26](papers/fumana.md) |
| **DR1 vs DR1-Foundation** | DR1-Foundation (public 2026-11-12): LE1 + validated LE2 images, spectra, catalogues, HEALPix masks; full DR1 (planned June 2027): shear and LE3 weak-lensing/clustering products; Foundation products are not re-released. DR2 ~2029 (about 3 years), DR3 full survey. | [Aussel+26](papers/aussel.md); [01](01_dr1_overview.md) |

## E

| Term | Definition | Where |
|---|---|---|
| **EAF (Euclid Auxiliary Field)** | Well-known fields visited many times for calibration: COSMOS (27 visits), CDFS (34), AEGIS (18); 4.8 deg^2 in total. | [Tereno+26](papers/tereno.md); [Aussel+26](papers/aussel.md) |
| **EAS (Euclid Archive System)** | SGS central metadata repository on the common data model (Distributed Storage System + Data Processing System); not to be confused with the public Science Archive. | [Ruffenach+26](papers/ruffenach.md) |
| **EC (Euclid Consortium)** | Consortium building the instruments and the Science Ground Segment (SGS) and exploiting the data. | [Tereno+26](papers/tereno.md) |
| **ECLIPSE** | Euclid Lens Identification Pipeline and Scientific Exploration: A strong-lens catalogue, B discovery pipeline, C lens modelling, D photo-z and physical properties of lenses. | [Lines+26](papers/lines.md); [Holloway+26](papers/holloway.md); [Nightingale+26](papers/nightingale.md); [Nersesian+26](papers/nersesian.md) |
| **EDF-N / EDF-S / EDF-F (Euclid Deep Fields)** | North (near NEP, 11 visits in DR1: 8 red + 3 blue), South (largest, 10 red visits) and Fornax (smallest, 2 visits: 1 red + 1 blue, contains CDFS); 77 deg^2 in total; tile prefix 101. | [Aussel+26](papers/aussel.md); [Tereno+26](papers/tereno.md) |
| **EDS** | Two meanings: **Euclid Deep Survey** (the deep tier of the surveys; EDF-N/S/F) and, in archive web pages, the **Euclid Data Space** (see EDS portal). | [Tereno+26](papers/tereno.md); archive help `EDS_Help_Pages.md` |
| **EDS portal / Euclid Data Space** | ESA portal integrating the Euclid Science Archive, ESASky and Datalabs (euclid.dataspace.esa.int); hosts the help pages. | [Ruffenach+26](papers/ruffenach.md) |
| **EES / EGBS** | Euclid Ecliptic Survey (Solar System objects, PDC thermalisation time) / Euclid Galactic Bulge Survey (Q2 data). | [Tereno+26](papers/tereno.md) |
| **EFF_COV** | Per-object flag in the MER catalogue (second extension): 1 if the position lies on a pixel with non-zero initial effective coverage in the VMPZ-ID mask. | [Odier+26](papers/odier.md) |
| **EMDS** | Euclid Medium-Deep Survey: PDC science fillers about 1 mag deeper and 10x smaller than the EWS (EMDS-1..4; EMDS-1/-2 VIS only). | [Aussel+26](papers/aussel.md); [Tereno+26](papers/tereno.md) |
| **ERO** | Early Release Observations (public 2024-05-23; 17 ERO fields observed in PV). | [Tereno+26](papers/tereno.md); [01](01_dr1_overview.md) |
| **ESASky** | ESA web sky viewer integrated in the Euclid Data Space. | [Ruffenach+26](papers/ruffenach.md) |
| **EUDF** | Euclid Ultra-Deep Field: self-calibration field plus F-014 data near the NEP (deepest field; release planned early 2027). | [Aussel+26](papers/aussel.md) |
| **EWS (Euclid Wide Survey)** | Main survey: ~2092 deg^2 VIS area, ~1900 deg^2 validated in DR1 (north ~500, south ~1400-1600 deg^2); 4-dither ROS per tile; tile prefix 102. | [Tereno+26](papers/tereno.md); [Aussel+26](papers/aussel.md) |
| **EXT / OU-EXT** | External ground-based imaging: UNIONS (CFHT u, r; Subaru/HSC g, z; Pan-STARRS i) in the north, DES griz in the south, HSC/DECam in the deep fields; resampled to MER tiles. | [Corcho-Caballero+26](papers/corcho-caballero.md) |

## F

| Term | Definition | Where |
|---|---|---|
| **FGS** | Fine Guidance Sensor. | [Tereno+26](papers/tereno.md) |
| **FILLING_FACTOR** | MER tile coverage fraction (> 0.5 for good astrometry, > 0.8 for typical use). | [Kuemmel+26](papers/kuemmel.md) |
| **FSCALE** | FITS keyword of SIR spectra, deprecated (1E-16); the SIGNAL unit already includes the 1e-16 scaling. | [08](08_spectroscopy.md); [dpdd_spectroscopy.md](data_model/dpdd_spectroscopy.md) |
| **FWA / GWA** | Filter-wheel assembly / grism-wheel assembly of NISP (`GWA_POS` = RGS000, RGS180, BGS000, ...). | [Tereno+26](papers/tereno.md); [Fumana+26](papers/fumana.md) |

## G

| Term | Definition | Where |
|---|---|---|
| **GC (galaxy clustering) / WL / 3x2pt** | Cosmological probes of LE3 (galaxy clustering; weak lensing; combination of shear, galaxy-galaxy lensing, clustering); not in DR1-Foundation. | [Ruffenach+26](papers/ruffenach.md) |
| **GELSA** | Python package (ELSA project, github.com/elsa-euclid/gelsa) to extract custom 1-D/2-D spectra and fixed-wavelength emission-line maps from SIR science frames; a method, not a DR1 product. | [Gabarra+26](papers/gabarra.md); [Bergamini+26](papers/bergamini.md); [08](08_spectroscopy.md) |
| **grism** | Grating prism of NISP-S for slitless spectroscopy (RGS red x3, BGS blue x1; RGS270 unused). | [Fumana+26](papers/fumana.md); [08](08_spectroscopy.md) |

## H

| Term | Definition | Where |
|---|---|---|
| **H2RG** | HAWAII-2RG infrared detectors of NISP (16 per focal plane); source of persistence. | [Kubik+26](papers/kubik.md); [Polenta+26](papers/polenta.md) |
| **HEALPix** | Equal-area sky pixelisation; the VMPZ-ID masks are full-sky maps at Nside = 16384 (~12.9" pixels). | [Odier+26](papers/odier.md); [dpdd_masks_vmpz.md](data_model/dpdd_masks_vmpz.md) |
| **HKTM** | Housekeeping telemetry (LE1 product, only released with full DR1). | [Aussel+26](papers/aussel.md) |

## I

| Term | Definition | Where |
|---|---|---|
| **Ice age / decontamination** | Ice accumulation on optics (from Feb 2024) reducing VIS throughput; decontaminations on 2024-03-14 and 2024-06-08; VIS data 2024-03-23 to 2024-06-07 are invalid and excluded from DR1; NISP ice causes slow wavelength-dependent drift (5-15 % in the blue grism). | [Aussel+26](papers/aussel.md); [Tereno+26](papers/tereno.md); [Fumana+26](papers/fumana.md) |
| **ICL** | Intra-cluster light; see the Q1 ICL papers. | [Bamford+26 (Q1)](papers/q1_icl_processing_bamford.md); [10](10_low_surface_brightness.md) |
| **I_E / Y_E / J_E / H_E (also IE, YE, JE, HE)** | Euclid bands: VIS broad optical band I_E (zero point 24.5, ADU/s) and NISP Y_E, J_E, H_E (zero points 29.8, 30.1, 30.0, electron/s); catalogue fluxes in uJy (ZP 23.9). EWS 10-sigma depths (2xFWHM aperture): 24.8 / 23.2 / 23.3 / 23.3. | [Enia+26](papers/enia.md); [verified_on_archive.md](data_model/verified_on_archive.md) |
| **ILS** | Independent Legacy Scientists: two scientists outside the EC with rights to a PDC filler field (ILS-WAVES-S; chosen partly for dwarf/LSB work). | [Tereno+26](papers/tereno.md) |
| **IMF** | Initial mass function (also an integer column `imf` in `phz_physical_parameters_*`, code table not documented). | [07](07_photoz_physical_parameters.md) |
| **IOT / SOC / MOC / SOST** | Instrument Operations Team / Science Operations Centre (ESA: planning, LE1, archive) / Mission Operations Centre / Survey Operations Support Team (produces the RSD). | [Tereno+26](papers/tereno.md) |

## K

| Term | Definition | Where |
|---|---|---|
| **Kron flux (`FLUX_DETECTION_TOTAL`)** | MER total flux in an elliptical Kron aperture on the detection mosaic (VIS if `VIS_DET` = 1, else NIR stack); `FLUX_SEGMENTATION` is the flux in segmented pixels. | [dpdd_mer.md](data_model/dpdd_mer.md); [Kuemmel+26](papers/kuemmel.md) |
| **Kron radius / `kron_radius`** | Major semi-axis of the elliptical Kron aperture in pixels (0.1"); used as an extent measure in cuts (SPE cosmology sample: < 50 px). | [dpdd_mer.md](data_model/dpdd_mer.md); [08](08_spectroscopy.md) |

## L

| Term | Definition | Where |
|---|---|---|
| **L2 / Lagrange point** | Sun-Earth L2 orbit of Euclid. | [Schirmer+26 spacecraft](papers/schirmer-spacecraft.md) |
| **LE1 / LE2 / LE3** | Level 1 = raw uncalibrated data (SOC); Level 2 = calibrated frames, stacks, mosaics, catalogues and spectra by the SGS PFs (VIS, NIR, EXT, MER, PHZ, SHE, SIR, SPE); Level 3 = cosmological/science products and VMPZ-ID, mostly not in DR1-Foundation. | [Tereno+26](papers/tereno.md); [Ruffenach+26](papers/ruffenach.md) |
| **LSB** | Low surface brightness. | [10](10_low_surface_brightness.md) |
| **LSF (large-scale flat)** | In VIS/NISP calibration: the large-scale flat field, residuals 0.08-0.14 % per VIS quadrant. (In SPE, `spe_lsf_*` = line spread function: sigma of the Gaussian LSF.) | [Schirmer+26 calibration](papers/schirmer-calibration.md); [08](08_spectroscopy.md) |

## M

| Term | Definition | Where |
|---|---|---|
| **MER (MERge)** | Processing function (OU-MER) that mosaics VIS, NIR and EXT frames onto a common 0.1"/px tile grid, detects/deblends sources (SourceXtractor++) and measures photometry (Kron, A-PHOT, T-PHOT, Sersic) and morphology; produces the 'primary' catalogue. | [Kuemmel+26](papers/kuemmel.md); [Q1 MER](papers/q1_romelli_mer.md) |
| **MUMAX_MINUS_MAG** | MER compactness estimator (MU_MAX minus `MAG_STARGAL_SEP`); `> -2.6` is the cut that removes compact/stellar sources in PHZ/Sersic samples. | [Enia+26](papers/enia.md); [Hartley+26](papers/hartley.md) |

## N

| Term | Definition | Where |
|---|---|---|
| **NEP** | North ecliptic pole, always visible; location of EDF-N and the self-calibration field. | [Tereno+26](papers/tereno.md) |
| **NIR / OU-NIR / NISP-P / NISP-S** | Near-infrared processing function for the NISP photometric channel (NISP-P: Y_E, J_E, H_E) and the spectroscopic channel (NISP-S: grisms; calibrated by SIR). NISP = Near-Infrared Spectrometer and Photometer. | [Polenta+26](papers/polenta.md); [da Silva+26](papers/dasilva.md); [Fumana+26](papers/fumana.md) |
| **NMAD** | Normalised median absolute deviation, 1.48 x median|dz - bias|, the photo-z scatter metric; outlier = |dz| > 0.15 with dz = (z_phot - z_spec)/(1+z_spec). | [Hartley+26](papers/hartley.md); [07](07_photoz_physical_parameters.md) |
| **NNPZ** | Nearest-Neighbour Photo-Z: PHZ code that estimates redshift PDFs, physical parameters and SEDs from the 30 nearest COSMOS reference objects (chi2 distance, log-normal amplitude prior). | [Hartley+26](papers/hartley.md); [Enia+26](papers/enia.md); [07](07_photoz_physical_parameters.md) |
| **NoiseChisel** | Background-estimation software used for the VIS (separate background map) and NIR sky subtraction. | [McCracken+26](papers/mccracken.md); [Polenta+26](papers/polenta.md) |
| **NOT_USE / ABS_FLUX (SIR mask bits)** | Spectrum mask values: NOT_USE (outside 25 % of band-edge throughput) and ABS_FLUX (suspicious absolute flux, 25-85 % of band-edge throughput). | [Fumana+26](papers/fumana.md); [08](08_spectroscopy.md) |

## O

| Term | Definition | Where |
|---|---|---|
| **OBJECT_ID** | MER unique object identifier (`object_id`, int64, often negative), shared by all catalogues and used for joins; encodes the position at ~3.6 mas resolution, so it can repeat by chance across visits; in `spectra_source` it is called `source_id`. | [dpdd_mer.md](data_model/dpdd_mer.md); archive help `Catalogues.md` |
| **Observation id (ObsID / ObservationType)** | Identifier shared by one ROS (4 dithers) or one calibration sequence; `CALBLOCK-F-xxx` / `CALBLOCK-PV-xxx` name the observation type. | [Tereno+26](papers/tereno.md); [Aussel+26](papers/aussel.md) |
| **OSS / RSD / ESSOT / ICR / POR / SSR** | Operational Sky Survey; Reference Survey Definition (schedule of pointings and slews); ESS operational tool; Instrument Commanding Request; Payload Operations Request; Survey Schedule Request: operations products, not user data. | [Tereno+26](papers/tereno.md) |
| **OTF** | On-the-fly processing campaigns (near-real-time), as opposed to the frozen DR1 reprocessing. | [Ruffenach+26](papers/ruffenach.md); [McCracken+26](papers/mccracken.md) |
| **OU (Organisation Unit)** | SGS team responsible for one PF: OU-VIS, OU-NIR, OU-EXT, OU-MER, OU-PHZ, OU-SHE, OU-SIR, OU-SPE, OU-LE3, OU-SIM. | [Ruffenach+26](papers/ruffenach.md) |

## P

| Term | Definition | Where |
|---|---|---|
| **Patch id / skypatch** | Contiguous survey patch: 'a compact set of fields with a valid observation sequence' (EWS has 50 skypatches; EDS 23); `patch_id_list` column; deep visits are identified through it. | [McCracken+26](papers/mccracken.md); [Aussel+26](papers/aussel.md); [Le Brun+26](papers/lebrun.md) |
| **PDC (Phase-Diversity Calibration)** | In-flight campaign of roughly 70 days (PDC-1 earlier on the NEP, PDC-2 ... PDC-8 starting around 2023-12) to calibrate the telescope wavefront model; thermal-stabilisation periods were used for EMDS/ILS/SSO science. **PDCC** (listed in the task) was not found in the local sources; probably 'PDC campaign'. | [Tereno+26](papers/tereno.md); [Aussel+26](papers/aussel.md) |
| **PDZ / zPDF / `phz_pdf`** | Photo-z probability distribution: 601 values, z = 0-6 step 0.01, smoothed with sigma_z = 0.02. | [07](07_photoz_physical_parameters.md) |
| **Persistence** | Residual charge release in NISP H2RG detectors after bright exposures; masked conservatively in DR1 (up to > 10 % of pixels in some frames, not corrected). | [Kubik+26](papers/kubik.md); [Polenta+26](papers/polenta.md) |
| **PF (processing function)** | Specialised SGS pipeline (VIS, NIR, EXT, MER, PHZ, SHE, SIR, SPE, VMPZ-ID, LE3 PFs); versions frozen for DR1 (e.g. MER 11.3.1, PHZ 2.16.13, SIR 6.0.2, SPE 25.0.1). | [Ruffenach+26](papers/ruffenach.md) |
| **Phosphoros** | Bayesian template-fitting code of PHZ; in DR1 used for the reference-sample labels and for the QSO, star and NIR-detected tables (core photo-z is NNPZ). | [Hartley+26](papers/hartley.md); [Nersesian+26](papers/nersesian.md) |
| **`phz_classification`** | PHZ class code: 1 star, 2 galaxy, 3 both, 0 none (TAP description swapped); do not rely on bits 4/8 from the DPDD. | [verified_on_archive.md](data_model/verified_on_archive.md); [07](07_photoz_physical_parameters.md) |
| **PHZ / OU-PHZ** | Photometric-redshift PF: photo-z PDFs, classification, physical parameters, SEDs, UNIF photometry; uses NNPZ and Phosphoros. | [Hartley+26](papers/hartley.md); [Enia+26](papers/enia.md); [07](07_photoz_physical_parameters.md) |
| **PIT / Frac68 / KL** | Probability integral transform and related zPDF calibration diagnostics (fraction of truths in the 68 % interval; Kullback-Leibler divergence). | [Hartley+26](papers/hartley.md) |
| **PN (planetary nebula SMC-SMP-20)** | Wavelength standard of the SIR calibration (PV-009 / F-010). | [Fumana+26](papers/fumana.md) |
| **point_like_prob / POINT_LIKE_FLAG** | MER probability that a source is point-like (empty values are NaN, use `NULLIF(point_like_prob, 'NaN')`). | [dpdd_mer.md](data_model/dpdd_mer.md); [Kuemmel+26](papers/kuemmel.md) |
| **PPO** | Pipeline Processing Order: unit of SGS production (200 830 PPOs, 34 million jobs in the DR1 campaign). | [Ruffenach+26](papers/ruffenach.md) |
| **pRF** | Probabilistic random forest used by PHZ for the star and galaxy classification. | [Hartley+26](papers/hartley.md) |
| **PSF field** | Calibration field (CALBLOCK-F-008) observed every 2-6 weeks with 100 short VIS dithers; no NISP LE2 and no MER in DR1; PSF models of VIS/NIR in [da Silva+26](papers/dasilva.md). | [Aussel+26](papers/aussel.md); [McCracken+26](papers/mccracken.md) |
| **PV (Performance Verification)** | Early operations phase (from 2023-08-01 to about 2023-12) with PV CALBLOCKs (e.g. PV-001 self-cal, PV-003 white dwarf, PV-005 COSMOS, PV-009 planetary nebula); only some PV fields are in LE2. | [Tereno+26](papers/tereno.md); [Schirmer+26 calibration](papers/schirmer-calibration.md) |

## Q

| Term | Definition | Where |
|---|---|---|
| **Q1 / Q2** | Quick Data Release 1 (2025-03-19; one visit of each EDF + LDN 1641) and Quick Release 2 (Galactic bulge, public 2026-06-24, not in DR1); neither is cosmology-grade. | [Aussel+26](papers/aussel.md); [Tereno+26](papers/tereno.md) |

## R

| Term | Definition | Where |
|---|---|---|
| **RGS (red grism)** | NISP red grisms (RGS000, RGS180 used in surveys), 1206-1892 nm, 1.372 nm/px; sole grism of the EWS. | [Fumana+26](papers/fumana.md); [08](08_spectroscopy.md) |
| **RMS / FLAG maps** | MER per-tile noise and flag mosaics (`stype` RMS and FLAG); FLAG maps work in the cutout service, RMS and BGMOD do not. | [verified_on_archive.md](data_model/verified_on_archive.md) |
| **RoI** | Region of Interest: the extragalactic sky where the EWS is built (16 200 deg^2 in two mainlands + two islands). | [Tereno+26](papers/tereno.md) |
| **ROS (Reference Observing Sequence)** | Standard 4-dither sequence of EWS/EDS/EAF observations (VIS in parallel with NISP spectroscopy, then Y_E/J_E/H_E; ~4204 s), the unit of one ObsID; ROS-blue uses BGS000. | [Tereno+26](papers/tereno.md) |

## S

| Term | Definition | Where |
|---|---|---|
| **SAA (solar aspect angle)** | Euclid's pitch angle (angle between telescope and Sun directions); with AA it fixes the attitude; survey design restricts SAA to 87-120 deg. | [Tereno+26](papers/tereno.md) |
| **SAS / Science Archive (System)** | Public ESA Euclid Science Archive: TAP/ADQL, cutout service, data downloads (`eas.esac.esa.int/sas-dd/data`, release `dr1`); part of the Euclid Data Space. | [Aussel+26](papers/aussel.md); [verified_on_archive.md](data_model/verified_on_archive.md) |
| **SDC** | Science Data Centre; nine national SDCs (FR, IT, NL, DE, UK, CH, FI, ES, US) process the data. | [Ruffenach+26](papers/ruffenach.md) |
| **SelfCal (self-calibration field)** | ~2 deg^2 field near the NEP inside EDF-N (CALBLOCK-F-001 and PV-001) observed repeatedly for flat-field/zero-point calibration; with F-014 forms the EUDF; objects are observed many times (duplicate spectra). | [Aussel+26](papers/aussel.md); [Schirmer+26 calibration](papers/schirmer-calibration.md) |
| **Sersic fits (MER)** | SE++ single-Sersic PSF-convolved fits per band (`sersic_sersic_vis_*`, n limit raised to 8 in DR1); the Disk+Sersic columns are empty in DR1. | [Kuemmel+26](papers/kuemmel.md); [verified_on_archive.md](data_model/verified_on_archive.md) |
| **SE++ (SourceXtractor++)** | Source detection and model-fitting software used by MER (detection, deblending, single-Sersic fits to VIS/NIR/EXT bands). | [Kuemmel+26](papers/kuemmel.md); [Dunn+26](papers/dunn.md) |
| **SGA** | Siena Galaxy Atlas: large nearby galaxies masked by ellipses in the VMPZ-ID masks (20-30 % enlarged). | [Odier+26](papers/odier.md) |
| **SGS** | Science Ground Segment (EC): produces science-ready images and catalogues; together with the ESA SOC forms the data pipeline. | [Ruffenach+26](papers/ruffenach.md) |
| **SHE** | Shear PF (weak-lensing shapes via LensMC and MetaCalibration); shear catalogues come with the full DR1 (June 2027). | [Ruffenach+26](papers/ruffenach.md); [Aussel+26](papers/aussel.md) |
| **SIR (spectroscopic reduction) / OU-SIR** | PF extracting and combining NISP slitless 1-D spectra (`DpdSirCombinedSpectra`) and science frames (`DpdSirScienceFrame`). | [Fumana+26](papers/fumana.md); [08](08_spectroscopy.md) |
| **SLE** | Strong-lens identification/modelling work (ECLIPSE: A lens catalogue, B discovery pipeline, C lens modelling, D photo-z and stellar masses). The expansion 'SLE' is **not given** in the local sources. | [Lines+26](papers/lines.md); [Holloway+26](papers/holloway.md); [Nightingale+26](papers/nightingale.md); [Nersesian+26](papers/nersesian.md) |
| **SOPS** | Special Operations Periodic: spacecraft/orbit maintenance windows (6 h every 4 weeks). | [Tereno+26](papers/tereno.md) |
| **Special objects / shredding** | MER scheme for galaxies larger than ~2' (no special tile processed in DR1); large nearby galaxies are over-deblended into many catalogue entries. | [Kuemmel+26](papers/kuemmel.md); [verified_on_archive.md](data_model/verified_on_archive.md) |
| **SpectraPyle** | Tool used to stack spectra (templates and quality-tier stacks in the SPE paper). | [Le Brun+26](papers/lebrun.md) |
| **SPE / OU-SPE** | Spectroscopic-redshift PF: classification, up to 5 redshift candidates, line fluxes and indices from SIR 1-D spectra (pipeline tuned for Halpha at 0.84 < z < 1.88). | [Le Brun+26](papers/lebrun.md); [08](08_spectroscopy.md) |
| **SPURIOUS_FLAG / SPURIOUS_PROB** | MER flag/probability that a detection is spurious; standard cut `SPURIOUS_FLAG = 0` or `spurious_prob < 0.5`. | [dpdd_mer.md](data_model/dpdd_mer.md); [Dunn+26](papers/dunn.md) |
| **SSO** | Solar-system-object survey field near the ecliptic (PDC filler, 19.2 deg^2). | [Aussel+26](papers/aussel.md) |

## T

| Term | Definition | Where |
|---|---|---|
| **TAP** | Table Access Protocol; the archive endpoint `https://eas.esac.esa.int/tap-server/tap` (schemas `dr1`, `q1`). | [verified_on_archive.md](data_model/verified_on_archive.md) |
| **TILEID / tile index (`tile_index`)** | 9-digit MER tile identifier: `102xxxxxx` wide tiles (32'x32' extended, 30' core), `101xxxxxx` deep tiles (17'x17', 15' core), `1025xxxx` special (none in DR1); present in MER, `combined_spectra`, `spe_catalogue` (as list) but not in PHZ/SPE tables. | [Kuemmel+26](papers/kuemmel.md); archive help `Catalogues.md` |
| **Tomographic bin (`tom_bin_id`)** | Photo-z bin for cosmology (equipopulated `tom_bin_id`, equidistant `alt_tom_bin_id`, clustering `pos_tom_bin_id`) with SOM calibratability flags; mean-z calibration not in DR1-Foundation. | [07](07_photoz_physical_parameters.md) |
| **T-PHOT** | MER template-fitting photometry (VIS high-resolution prior, `FLUX_<band>_TEMPLFIT`), best in NISP bands and at faint magnitudes (a bug affecting bright points was found after DR1 processing). | [Kuemmel+26](papers/kuemmel.md); [Gasparetto+26](papers/gasparetto.md) |

## U

| Term | Definition | Where |
|---|---|---|
| **UNIF (unified photometry)** | PHZ fluxes standardised to the DECam filter set and corrected for Galactic extinction (`flux_*_unif`); galaxies only, no errors. | [Hartley+26](papers/hartley.md); [07](07_photoz_physical_parameters.md) |
| **UNIONS / CFIS / WHIGS / WISHES** | Ground-based northern consortium: CFHT/MegaCam u, r (CFIS), Subaru/HSC g (WHIGS) and z (WISHES), Pan-STARRS i; u present only over about half of the north. | [Corcho-Caballero+26](papers/corcho-caballero.md); [Hartley+26](papers/hartley.md) |

## V

| Term | Definition | Where |
|---|---|---|
| **VIS_DET** | MER flag: 1 = detected on the VIS image, 0 = detected only on the NIR stack (about 1/4 of EWS objects); `phz_flags` = 10 corresponds to `vis_det` = 0. | [Hartley+26](papers/hartley.md); [07](07_photoz_physical_parameters.md) |
| **VIS / OU-VIS** | Visible instrument (wide-field optical imager, band I_E, 0.1"/px mosaic, ~0.16-0.18" resolution) and its processing function. | [McCracken+26](papers/mccracken.md) |
| **VMPZ-ID** | Visibility Mask PhotoZ-Internal Data: OU-LE3 PF producing HEALPix photometric masks, depth/coverage/PSF/astrometry maps, Pan-STARRS artefact map and random catalogues (the footprint to use for statistics). | [Odier+26](papers/odier.md); [dpdd_masks_vmpz.md](data_model/dpdd_masks_vmpz.md) |

## W

| Term | Definition | Where |
|---|---|---|
| **WAVES** | Wide Area VISTA Extragalactic Survey; WAVES-VISTA field in DR1 (VIS only, no MER). | [Aussel+26](papers/aussel.md) |

## Z

| Term | Definition | Where |
|---|---|---|
| **Zoobot** | Deep-learning visual-morphology model (vote fractions in MER for a subsample: I_E < 21 or segmentation area > 700 px per verified; DPDD says VIS < 20.5 or > 1200 px). | [Kuemmel+26](papers/kuemmel.md); [verified_on_archive.md](data_model/verified_on_archive.md) |
