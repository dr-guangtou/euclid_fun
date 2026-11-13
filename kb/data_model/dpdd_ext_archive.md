# Euclid DR1 DPDD: EXT products, Science Archive (SAS) contents, and missing/undocumented products

**How to use this note.** Answers three practical questions: (1) what does the DPDD say about EXT (ground-based) products, (2) which products can actually be downloaded from the DR1-Foundation Science Archive Service (SAS), and (3) which products exist in the data model but have no DPDD card. Use it to decide quickly whether a product you want (e.g. a stacked VIS image or a ground-based frame) is available at all. For the content of the available products see `dpdd_mer.md` and `dpdd_vis_nir.md`.

**Sources** (in `~/Desktop/euclid/text/dpdd/`): `extdpd__extintro.md`, `extdpd__extindex.md`, `sasdataproducts.md`, `missing__missing-index.md`, `Introduction.md`, `purpose.md`, `system.md`.

---

## 1. EXT (external, ground-based) products

- The whole EXT introduction is one sentence: **"There are no EXT products distributed in DR1-Foundation."** `extindex.md` holds only a table of contents (Introduction). There are no EXT data-product cards.
- The ground-based photometry nevertheless reaches users in two indirect ways (documented in the MER cards):
  1. **MER mosaics of EXT bands** (`DpdMerBksMosaic`): EXT stacked frames were already background-subtracted by EXT; MER only rebins them to the 0.1" Euclid grid. Pixel units are "arbitrary" (not ADU/s, not electrons); convert with the mosaic `MAGZERO`. EXT RMS maps do **not** include a Poisson-noise term. The mosaic flag map carries the EXT-side flag definitions (not documented in the DPDD).
  2. **MER catalogue columns** per EXT band (see `dpdd_mer.md` §4): aperture, template-fitting and Sersic fluxes in uJy, `FLAG_<band>`, `AVG_TRANS_WAVE_<band>`. Main catalogue EXT bands: DECam u,g,r,i,z; LSST u,g,r,i,z (listed as `_EXT_LSST`); MegaCam u and r; JPCam g; Pan-STARRS i and z; HSC g and z. DEEP-field extra bands: Subaru intermediate bands IA427 to IA856, MegaCam u* and u', HSC r, r2, i, i2, y, VISTA Y,J,H,Ks, UKIRT J,H,K, IRAC ch1 and ch2, GALEX FUV and NUV.
- Not distributed (declared in DM 10.1.4 but undocumented; see section 3): `DpdExtStackedFrame`, `DpdExtSingleEpochFrame`, `DpdExtValidatedSingleEpochFrame`, `DpdExtCoaddCatalog`, `DpdExtSuperTile`, `DpdExtGaiaCatalog`, `DpdExtGaiaCutout`, `DpdExtTwoMassCatalog`, `DpdExtTwoMassCutout`, `DpdExtBandpass`, `DpdExtValidatedBandpass`, `DpdExtConfigurationSet`, `DpdExtAnalysisResult`, `DpdExtValidation{Report,Requirements,Result}` and the EXT-DES (DECam/DES, 15 items) and EXT-LSS (4 items) families.
- Consequence for LSB/photometry work: ground-based pixel data are only available through the MER mosaics (already background-subtracted, rebinned to 0.1", PSF info via the MER PSF stamp file), never as individual ground-based frames in DR1-Foundation.

---

## 2. Products available in the DR1-Foundation SAS

From `sasdataproducts.md`. ESA serves only a **subset** of SGS products. For every product served, **each FITS file belonging to it is served**, but the DPS metadata that lets SGS pipelines query and select subsets is **not** available in the SAS. The DPDD text still applies to the SAS version of each product. `purpose.md` adds: SAS products are often stripped of metadata, keeping only the core FITS images and tables; the scope of this DPDD (v2.0) is "the products served by SAS", and users who believe other products should be distributed are asked to tell the SGS scientists.

| Level | Processing function | Data product (DPD name) | In this knowledge base |
|---|---|---|---|
| Level 1 | (PV phase only, **all** data) | `DpdVisRawFrame` | not covered here (LE1 cards) |
| Level 1 | (PV phase only, **all** data) | `DpdNispRawFrame` | not covered here (LE1 cards) |
| Level 2 | VIS | `DpdVisCalibratedQuadFrame` | `dpdd_vis_nir.md` |
| Level 2 | VIS | `DpdVisCalibratedFrameCatalog` | `dpdd_vis_nir.md` |
| Level 2 | NIR | `DpdNirCalibratedFrame` | `dpdd_vis_nir.md` |
| Level 2 | NIR | `DpdNirCalibratedFrameCatalog` | `dpdd_vis_nir.md` |
| Level 2 | MER | `DpdMerBksMosaic` | `dpdd_mer.md` |
| Level 2 | MER | `DpdMerFinalCatalog` | `dpdd_mer.md` |
| Level 2 | MER | `DpdMerSegmentationMap` | `dpdd_mer.md` |
| Level 2 | PHZ | `DpdPhzPfOutputCatalog` | not covered here |
| Level 2 | PHZ | `DpdPhzPfOutputForL3` | not covered here |
| Level 2 | SIR | `DpdSirScienceFrame` | not covered here |
| Level 2 | SIR | `DpdSirCombinedSpectra` | not covered here |
| Level 2 | SPE | `DpdSpePfOutputCatalog` | not covered here |
| Level 3 | VMPZ-ID | `DpdHealpixBitMaskVMPZ` | not covered here |
| Level 3 | VMPZ-ID | `DpdHealpixCoverageVMPZ` | not covered here |
| Level 3 | VMPZ-ID | `DpdHealpixCoverageMaskVMPZ` (the page links it to the depth-map card; listing as printed) | not covered here |
| Level 3 | VMPZ-ID | `DpdHealpixFootprintMaskVMPZ` | not covered here |
| Level 3 | VMPZ-ID | `DpdHealpixInfoMapVMPZ` | not covered here |

Notes:
- The **DpdVisCalibratedQuadFrame** entry is spelled out in the SAS page: the VIS individual exposure FITS file with its SCI, RMS and FLG extensions (numerous, one per quadrant), the VIS weight map FITS file, the VIS background map FITS file, and the VIS PSF FITS file.
- The MER card for the bks mosaic enumerates the mosaic auxiliary files (RMS, FLAG, PSF stamps, filter transmission, detector layering, bright-star masks JSON, background model); whether every one of these files is exposed in the SAS follows the "each FITS file that belongs to the product is served" rule, but the SAS page does not list them individually (and the JSON mask file is not a FITS file), so confirm in the archive.
- **Not in the SAS (DR1-Foundation)**: stacked VIS/NIR frames and their catalogues, MER detection mosaic, SHE products, any EXT product, LE3 products other than the five VMPZ-ID HEALPix masks/maps, all calibration products, all validation/analysis products (see section 3).
- The VIS, NIR and MER intros each label the non-served items as "Not distributed in DR1-Foundation" (VIS: `DpdVisStackedFrame`, `DpdVisStackedFrameCatalog`, `DpdVisDiffractionSpikesFocus`, `DpdVisFlagMap`, `DpdVisAnalysisResults`, `DpdVisGhostCatalogue`, `DpdVisPSFModel`, plus 23 calibration products; NIR: `DpdNirStackedFrame`, `DpdNirStackedFrameCatalog`, plus 15 calibration products; MER: `MERTile`, `MERDetectionMosaic`, `EXTExtStackedFrame`, `MERConfigurationSet`, `MERMachineLearningModels`, `MERDqcStaticFlagLimits`, `EXTExtGaiaCutout`, `MERAnalysisResult`, true-universe catalogues).
- SHE is not run for DR1-Foundation (`system.md`); the only LE3 PF to run partially is VMPZ-ID.

### DR1 pipeline context (from `system.md`, `Introduction.md`)
- Flow: LE1 (SOC) -> VIS (calibrated VIS exposures) -> NIR (uses VIS as astrometric/photometric reference; also pre-processes NISP spectroscopic frames for SIR) in parallel with EXT (ground photometry calibrated in two steps) -> MER (detects on VIS, forced photometry in all other bands) -> SIR (spectra extraction at MER positions) -> SPE (redshifts, lines) ; PHZ (photo-z, PDFs, classification, stellar masses) ; LE3 VMPZ-ID (photometric masks).
- DPDD is organised to mirror the SGS Common Data Model (DM tag 10.1.4 for this document, DPDD version 2.0). Each product has a "card" (name, custodian, schema file, elements Header/Data/QualityFlags/Parameters, creating/using elements, detailed description). Introduction.md contains embedded editorial comments from the document authors (e.g. suggestions about trimming cards, adding keyword tables); they are not product information.

---

## 3. Products declared in the data model (DM 10.1.4) but not documented in DPDD v2.0

`missing__missing-index.md`: "declared in data model DM 10.1.4 but are not documented in the present version (2.0) of the DPDD because they are not published as part of DR1-Foundation". The table has about 405 rows (a few names are repeated). Per processing function (row counts as listed):

| PF | Rows | Examples / relevance to galaxy photometry and LSB |
|---|---|---|
| **VIS** | 37 | **`DpdVisStackedFrame`, `DpdVisStackedFrameCatalog`** (no VIS stacks); `DpdVisCalibratedFrame` (deprecated predecessor); **`DpdVisFlagMap`** (flag definitions: use `download__VIS_Flags.txt`); `DpdVisAnalysisResults`; `DpdVisStarMask`; `DpdVisGhostCatalogue`, `DpdVisGhostModel`; `DpdVisDiffractionSpikesFocus`; `DpdPSFModel`; `DpdVisZeroPoint`; calibration set (master bias/dark/flat/CI frames, `DpdVisMasterFlatFrame`, CTI, BFE, blooming, gain, RON, non-linearity, persistence, pixel-bounce, shutter, trap pumping, X-talk models); validation and configuration products |
| **NIR** | 21 | **`DpdNirStackedFrame`, `DpdNirStackedFrameCatalog`**; `DpdNirSuperFlatFrame`, `DpdNirLargeFlatFrame`, `DpdNirMasterFlatFrame`, `DpdNirMasterDarkFrame`; bad-pixel / persistence / non-linearity masks and models; geometric distortions; relative and absolute photometric calibrations; `DpdNirGhostModel`; `DpdNirTransientCatalog`; `DpdNirConfigurationSet` |
| **MER** | 19 | `DpdMerMosaic`, `DpdMerDetectionMosaic`, `DpdMerTile`, `DpdMerTileList`, `DpdMerObjectCatalog`, `DpdMerSingleBandCatalog`, `DpdMerCrossMatchedCatalog`, `DpdMerMorphologyCatalog` (content is inside the final catalogue product), `DpdMerPsfStampCollection`, `DpdMerPsfTransformationKernel`, `DpdMerConfigurationSet` (the background/photometry parameters), `DpdMerMachineLearningModels`, `DpdMerDqcStaticFlagLimits`, analysis/validation products, true-universe catalogues |
| **EXT** | 16 | all general EXT products (stacked, single-epoch, coadd catalogue, supertile, Gaia/2MASS catalogues and cutouts, bandpasses, configuration, validation) |
| **EXT-DES** | 15 | DECam-DES calibrated frames, stacks, catalogues, master calibrations (raw frame, bias, flat, X-talk, ...) |
| **EXT-LSS** | 4 | `DpdExtLss` master bias, dark, flat and single-visit image |
| **SIR** | 13 | decontaminated spectra, extracted spectra collections, location tables, flux scalings, models |
| **SHE** | 30 | shear measurement, PSF-field and bias products |
| **PHZ** | 11 | model grids, bias-correction, classification and validation products |
| **SPE** | 6 | analysis, calibration, configuration, PDF catalogue, redshift reference catalogue |
| **SLE** | 8 | classification sets/models, visual-grade and model catalogues, model images (expansion of the acronym not given in the DPDD) |
| **SIM** | 10 | simulation inputs and true-universe outputs |
| **SOC** | 18 | operations, housekeeping, raw telemetry, mission events |
| **LE3-CL** | 71 | cluster-related products |
| **LE3-GC** | 26 | galaxy-clustering products |
| **LE3-ID** | 41 | VMPZ-ID parameters, MOC and visibility masks, WL position/shear catalogues, VMSP products |
| **LE3-WL** | 49 | weak-lensing power spectra, 2PCF, mass maps |
| **LE3-ED** | 2 | `DpdLE3edConfigurationFile`, `DpdLE3edMatchedCatalog` |
| DIS, GTD, MAP, MDB, ORC, PSF | 1, 1, 2, 1, 3, 1 | `DpdDistributionMap`, `DpdGroundTestDataSet`, `DpdIntersectionMaps`, `DpdSkyPatch`, `DpdMdbDataBase`, `DpdProductionReport`, `DpdTileSetSelection`, `DpdTriggeringRules`, `DpdSimulatedPSF` |

Reverse mismatch: a product declared in DPDD 2.0 but absent from DM 10.1.4: `DpdsimPSF` (PSF).

### What this means for the research use case
- **No stacked VIS or NIR images, no EXT frames, no master flats/darks, no VIS ghost/star-mask catalogues, no PSF model products** in DR1-Foundation. Deep LSB stacks must be rebuilt from `DpdVisCalibratedQuadFrame` (+ weights, backgrounds) and `DpdNirCalibratedFrame`, or taken from MER mosaics.
- The MER background configuration and the PSF stamp/kernel machinery are not published as separate products, so their parameters must come from papers or release notes.
- Documentation for flags of the VIS flag map and the NIR DQ layer is partial: VIS bits come from a PDF dump (`download__VIS_Flags.txt`), NIR bits appear only in a figure.
