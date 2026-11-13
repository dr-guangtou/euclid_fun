# Euclid DR1 DPDD: spectroscopy (SIR 1-D spectra and science frames, SPE redshift catalogue)

**How to use this note.** A reference for the NISP slitless-spectroscopy products: SIR (spectra extraction and combination) and SPE (spectroscopic redshift measurement). Sections 1-3 cover SIR, sections 4-7 cover SPE, section 8 explains how to join to MER and how to choose reliable redshifts. Statements marked **(DPDD)** come from the DPDD text; **(inference)** marks my interpretation or suggested practice. Where the DPDD is ambiguous this is stated.

**Source files** (in `~/Desktop/euclid/text/dpdd/`): `sirdpd__sirintro.md`, `sirdpd__sirindex.md`, `sirdpd__dpcards__sir_combinedspectra.md`, `sirdpd__dpcards__sir_scienceframe.md`, `spedpd__speintro.md`, `spedpd__speindex.md`, `spedpd__dpcards__spe_spepfoutputcatalog.md`. Online: https://euclid.esac.esa.int/dr/dr1/dpdd/sirdpd/sirindex.html and `.../spedpd/speindex.html`.

## 1. SIR overview: what is and is not distributed

SIR reduces all NISP spectroscopic data (wide and deep). Wide fields have 4 dithers, deep fields 60 dithers **(DPDD)**.

| Stage | Product | In DR1-Foundation? |
|---|---|---|
| Calibration products (`DpdSirDetectorScaling`, `DpdSirOptModel`, `DpdSirCrvModel`, `DpdSirIdsModel`, `DpdSirSpectralPsfModel`, `DpdSirRelativeFluxScaling`, `DpdSirAbsoluteFluxScaling`) | internal SIR inputs | no |
| `SIRLocationTable` (16 per dither, one per detector), `SIRLE3LocationTable` | spectra location / geometry | no |
| `SIRExtractedSpectraCollection` (16 per dither) | single-dither calibrated 1-D spectra | no |
| `SIRConfigurationSet` | pipeline configuration | no |
| **`DpdSirScienceFrame`** | background-subtracted dispersed frames | yes |
| **`DpdSirCombinedSpectra`** | all-dither combined 1-D spectra per MER tile | yes |

Two science pipelines: *SpectraExtraction* (per observation, LE1 frame to calibrated 1-D spectra per dither) and *SpectraCombination* (per MER tile, stacks all dithers). Per dither SpectraExtraction produces 1 background-subtracted frame, 16 location tables, 1 LE3 location table, and 16 extracted-spectra collections. Spectra decontamination is applied but its products are not archived **(DPDD)**.

## 2. `DpdSirCombinedSpectra` (the 1-D spectra you will use)

### 2.1 Organisation

- One `DpdSirCombinedSpectra` per MER Final Catalog (per tile). It contains one `CombinedSpectrum` for every object in the MER catalogue (empty if no spectrum was extracted) **(DPDD)**.
- Stored as a **collection of FITS files, each holding 1000 CombinedSpectrum entries**. File name: `EUC_SIR_W-COMBSPEC_<TILEID>_<TIMESTAMP>.fits.gz` (example `EUC_SIR_W-COMBSPEC_102007590_20250117T184200.082829Z.fits.gz`). The DPDD does not say how multiple 1000-object files of the same tile are numbered (the file name pattern has no sequence index; check real file names).
- **Red versus blue grism**: the primary header keyword `LRANGE` gives the grism set used in the combination, `RGS` (red) or `BGS` (blue). If a tile's MER catalogue covers both a red-grism field and a blue-grism field, there are **two** `CombinedSpectra` products for it, one RGS and one BGS (the DPDD writes "RSG and BGS" once, a typo). So an object can have up to two combined spectra, one per grism family, each combining only the dithers of that family **(DPDD)**. The DPDD does not state the wavelength coverage of the grisms; the actual range is in `WMIN`, `BINWIDTH`, `BINCOUNT` per spectrum.
- **Spectra per source**: within one CombinedSpectrum there are *n* single-dither spectra (one `DITH1D_n_SIGNAL` HDU per pointing ID that covers the object; the figure example shows 5 dithers with pointing IDs 3197, 3198, 3199, 3318, 3319) and exactly one combined spectrum. Wide-field objects typically have up to 4 dithers per grism configuration; the example shows 5 because it spans more than one observation **(partly inference)**.

### 2.2 PRIMARY header (per file)

| Keyword | Meaning |
|---|---|
| `FITS_DEF` | `sir.combinedSpectra` |
| `FITS_VER` | 0.2 |
| `TELESCOP`, `INSTRUME` | EUCLID, NISP (NISPsim for simulations) |
| `DATE`, `ORIGIN`, `SOFTVERS`, `VERSION` | creation date, originator, pipeline version, data-release version |
| `N_OBJ` | number of sources in the file |
| `TILE_ID` | MER tile index |
| `LRANGE` | BGS or RGS |
| `MSK_FLAG_*` | mask bit dictionary (section 2.4) |
| (described in prose) | counts and comma-separated lists of contributing Observation IDs, Patch IDs and CalBlock IDs |

### 2.3 HDUs for object number `m`

`m` is a running index inside the file (not the object ID). Each HDU name starts with `m`. The DPDD text sometimes writes names with a `SIR_` prefix (`SIR_m_META`, `SIR_m_COMBINED1D_SIGNAL`, ...). Use the `m_META` header to map `m` to the MER ID **(DPDD)**.

| HDU | Contents |
|---|---|
| `m_META` | header only: `N_DITH` (number of dithers containing the object), `OBJ_ID` (MER ID), `RA_OBJ`, `DEC_OBJ` (double). If no spectrum was extracted this is the only HDU for `m`. |
| `m_DITH1D_n_SIGNAL` | binary table of one dither's extracted spectrum; `n` is the pointing ID. Header: `GWA_POS` (RGS270, RGS000, RGS180, BGS000, OPEN), `GWA_TILT`, `DITH_ID`, `PTGID`, `EXPTIME`, `FSCALE` (deprecated, 1E-16), `WMIN`, `BINWIDTH`, `BINCOUNT`, `DET_ID`, `DET_ID_2` (present only if the spectrum spans two detectors), `LSF_SIG` (sigma of the Gaussian line-spread function), `EXT_PROF` (extraction profile NONE, OPT_THUMB, OPT_PSF). |
| `m_DITH1D_n_CONTAMINANTS` | one column `OBJ_ID` (K, int64): IDs of contaminating objects for that dither. Header: `GWA_POS`, `GWA_TILT`, `DITH_ID`, `PTGID`. |
| `m_COMBINED1D_SIGNAL` | binary table of the combined spectrum. Header: `EXPTIME`, `FSCALE`, `WMIN`, `BINWIDTH`, `BINCOUNT`, `LSF_SIG`, `EXT_PROF`. |

### 2.4 Table columns

| Column | `DITH1D_n_SIGNAL` | `COMBINED1D_SIGNAL` | Unit | Format |
|---|---|---|---|---|
| `WAVELENGTH` | yes | yes | Angstrom | E |
| `SIGNAL` (flux) | yes | yes | 1e-16 erg s^-1 cm^-2 A^-1 | E |
| `MASK` | yes | yes | bit mask (see below) | J (int32) |
| `VAR` (variance of flux) | yes | yes | 1e-32 erg^2 s^-2 cm^-4 A^-2 | E |
| `QUALITY` | yes | yes | 0 to 1 | E (float32) |
| `NDITH` | no | yes | number | I (int16) |

- **Flux calibration**: the scale factor 1e-16 is already embedded in the unit; `FSCALE` is deprecated and fixed at 1E-16, so do not multiply by it again **(DPDD, with inference on the "do not re-apply" reading)**. Flux is absolute (calibrated by the SIR absolute flux calibration step); the DPDD gives no accuracy figure.
- `VAR` is the variance, so the 1-sigma error is `sqrt(VAR)` in 1e-16 units **(inference)**.
- `QUALITY`: fraction of potentially available pixel weight that was actually used for that flux bin (1 = all, 0 = none), accounting for rejected pixels (bad pixels, cosmic rays) and weights in the 2-D resampling and 1-D extraction.
- `NDITH`: number of spectra contributing to that wavelength bin (at most the header `N_DITH`).

### 2.5 Mask bit dictionary (primary header)

| Keyword | Value |
|---|---|
| `MSK_FLAG_GOOD` | 0 |
| `MSK_FLAG_NOT_USE` | 1 |
| `MSK_FLAG_LOW_SNR` | 2 |
| `MSK_FLAG_EXT_PRB` | 4 |
| `MSK_FLAG_HIGH` | 8 |
| `MSK_FLAG_LOW` | 16 |
| `MSK_FLAG_REL_FLUX` | 32 |
| `MSK_FLAG_ABS_FLUX` | 64 |

The DPDD labels these "Mask bit position" but the numbers 1, 2, 4, 8, 16, 32, 64 are powers of two, so they are most likely bit **values** to be AND-ed with `MASK` (GOOD = 0 means no bit set) **(inference; ambiguous in the DPDD)**. The DPDD gives no prose definitions of the flag names; plausible readings are: NOT_USE = do not use the pixel, LOW_SNR = low signal-to-noise, EXT_PRB = extraction problem, HIGH/LOW = value above/below a limit, REL_FLUX/ABS_FLUX = problem with relative/absolute flux calibration **(inference from names only)**. Always read the dictionary from the file header.

## 3. `DpdSirScienceFrame` (background-subtracted dispersed frames)

- Custodian SIR; consumers SIR and LE3. Proposed for SAS: yes. Elements: Header, Data (`sir:scienceFrame`), QualityFlags, Parameters.
- One multi-extension FITS per dither/exposure covering the whole field of view. The primary HDU holds only pointing metadata. Data are in **48 extensions: 3 per detector** (16 detectors): `DETn.SCI` (dispersed image values), `DETn.VAR` (variance), `DETn.DQ` (pixel data-quality bit mask). The frame also carries the pointing correction computed by SIR.
- `DETn.DQ` bit numbers: 0 hot pixel, 1 cold pixel, 2 saturated, 3 cosmic ray, 4 satellite trail, 5 interpolated, 6 bleeding, 7 on-board masking, 8 bad pixel, 9 non-linear, 10 persistent charge, 11 ghost masking, 12 transient object, 13 extended object, 14 scattered light, 15 charge injection, 16 near charge injection. (Here the DPDD list is a list of bit numbers, in contrast to the combined-spectra mask.)
- File name: `EUC_SIR_W-SCIFRM_BKGSUB_<OBSID>_<PTGID>_<DITH>_<GWA>_<TILT>_<TIMESTAMP>.fits.gz`; example `EUC_SIR_W-SCIFRM_BKGSUB_65879_270539_0_RGS000_0_20250410T105605.065923Z.fits.gz`. `GWA` is the grism wheel position (for example RGS000); `TILT` the grism tilt.
- Not described: units of `SCI` (presumably electrons per second or ADU-like detector units; check header `BUNIT`) and WCS conventions. These frames are 2-D dispersed images, so they are of little use for imaging science (no direct imaging), except for spectroscopic 2-D work **(inference)**.

## 4. SPE overview

SPE measures spectroscopic redshifts from the SIR combined 1-D spectra, also emission-line fluxes and spectral features, with estimates of reliability and a star/galaxy/QSO classification. Input is the SIR product over one MER tile; output is one `DpdSpePfOutputCatalog` per MER tile, used by LE3 **(DPDD)**. Created by the SPE merge element from "SPE process spectra" and "SPE feature measurements". The redshift engine is called "Amazed" in flag tables **(DPDD naming of error table)**.

The product is split into **4 FITS files**: Redshift catalog, PDF catalog, Lines catalog, Models catalog. The DPDD describes only the first, third and fourth in detail; the PDF catalog file has no description there (redshift PDFs also appear as `SPE_PDF` columns in the candidate tables).

## 5. SPE Redshift catalogue file

File name: `EUC_SPE_WIDE-CAT-Z-[TILE_ID]_[INSTANCE_ID]_[YYYYMMDDThhmmss.s]Z_[VERSION].fits`. 5 binary-table HDUs. For processed spectra the classification and candidate HDUs have rows only for objects that were processed **(inference)**. Candidate tables have up to 5 rows per object for galaxies and QSOs (ranks 0 to 4) and 1 for stars.

| HDU # | EXTNAME | Rows | Columns |
|---|---|---|---|
| 1 | `QUALITY` | per spectrum | 30 |
| 2 | `CLASSIFICATION_CATALOG` | per processed spectrum | 5 |
| 3 | `GALAXY_CANDIDATES_CATALOG` | up to 5 per object | 18 |
| 4 | `STAR_CANDIDATES_CATALOG` | 1 per object | 11 |
| 5 | `QSO_CANDIDATES_CATALOG` | up to 5 per object | 15 |

### 5.1 `QUALITY` (30 columns)

| Column | Format | Meaning |
|---|---|---|
| `OBJECT_ID` | K | MER ID |
| `SPE_ERROR_FLAG` | I | overall processing error flag (bit-coded, table in section 5.7) |
| `SPE_WARNING_FLAG` | I | overall processing warning flag |
| `SPE_CONTEXT_ERROR_FLAG`, `SPE_CLASS_ERROR_FLAG`, `SPE_STAR_ERROR_FLAG`, `SPE_GAL_ERROR_FLAG`, `SPE_QSO_ERROR_FLAG` | K | per-stage error flags (Amazed error codes) |
| `SPE_CONTEXT_WARNING_FLAG`, `SPE_CLASS_WARNING_FLAG`, `SPE_STAR_WARNING_FLAG`, `SPE_GAL_WARNING_FLAG`, `SPE_QSO_WARNING_FLAG` | K | per-stage warning flags |
| `SPE_GAL_CONT_MIN_REDUCED_CHI2` | E | minimum over z of the continuum reduced chi2 (galaxy model) |
| `SPE_GAL_CONT_MAX_P_VALUE` | E | maximum over z of the continuum p-value |
| `SPE_GAL_CONT_MIN_RESIDUAL_NORMALITY` | E | minimum over z of the continuum residual normality test |
| `SPE_GAL_CONT_REMOVED` | L | true if the spectrum was median-filtered |
| `SPE_GRISM` | 8A | BGS, RGS, or BGS\|RGS |
| `SPE_W_MIN`, `SPE_W_MAX` | E, Angstrom | wavelength limits of the used spectrum |
| `SPE_NPIX` | I | number of pixels |
| `SPE_N_DITH_MAX`, `SPE_N_DITH_MED` | I | maximum / median number of dithers |
| `SPE_N_DITH_RED_L/M/H`, `SPE_N_DITH_BLUE_L/M/H` | I | dithers in red / blue at low / middle / high wavelength |
| `SPE_LSF` | E, Angstrom | sigma of the Gaussian line-spread-function model |

### 5.2 `CLASSIFICATION_CATALOG` (5 columns)

`OBJECT_ID` (K); `SPE_STAR_PROB`, `SPE_GAL_PROB`, `SPE_QSO_PROB` (E); `SPE_CLASS` (8A): class with the highest probability, one of `STAR`, `GALAXY`, `QSO`, `UNDEF`.

### 5.3 `GALAXY_CANDIDATES_CATALOG` (18 columns) and `QSO_CANDIDATES_CATALOG` (15 columns)

| Column | Format | Meaning | In galaxy | In QSO |
|---|---|---|---|---|
| `OBJECT_ID` | K | MER ID | yes | yes |
| `SPE_RANK` | I | rank of the estimate (0 = best) | yes | yes |
| `SPE_Z` | E | estimated spectroscopic redshift | yes | yes |
| `SPE_Z_ERR` | E | redshift uncertainty | yes | yes |
| `SPE_Z_PROB` | E | probability of the redshift | yes | yes |
| `SPE_Z_REL` | E | reliability of the redshift | yes | yes |
| `SPE_SUBCLASS` | 48A | sub-classification | yes | yes |
| `SPE_CONT_SNR` | E | continuum signal-to-noise | yes | yes |
| `SPE_Z_REDUCED_CHI2` | E | reduced chi2 at z | yes | yes |
| `SPE_Z_CONT_REDUCED_CHI2` | E | continuum reduced chi2 at z | yes | no |
| `SPE_Z_P_VALUE` | E | p-value at z | yes | yes |
| `SPE_Z_CONT_P_VALUE` | E | continuum p-value at z | yes | no |
| `SPE_Z_RESIDUAL_NORMALITY` | E | residual normality test (for example Kolmogorov-Smirnov) at z | yes | yes |
| `SPE_Z_CONT_RESIDUAL_NORMALITY` | E | same, continuum only | yes | no |
| `SPE_PDF_ZMIN`, `SPE_PDF_ZMAX`, `SPE_PDF_DELTAZ` | E | redshift window of the candidate PDF | yes | yes |
| `SPE_PDF` | 80E | PDF values on that window | yes | yes |

### 5.4 `STAR_CANDIDATES_CATALOG` (11 columns)

`OBJECT_ID`, `SPE_RANK`, `SPE_RVEL` (km/s radial velocity), `SPE_RVEL_ERR` (km/s), `SPE_MODEL_PROB`, `SPE_MODEL_REL`, `SPE_SUBCLASS` (48A), `SPE_CONT_SNR`, `SPE_REDUCED_CHI2`, `SPE_P_VALUE`, `SPE_RESIDUAL_NORMALITY`.

### 5.5 Redshift quality: recommended checks (DPDD)

The DPDD states the quality must be read per object type, and advises:

1. `SPE_ERROR_FLAG == 0`.
2. For galaxy solutions also `SPE_GAL_ERROR_FLAG == 0`.
3. For star solutions `SPE_STAR_ERROR_FLAG == 0`.
4. For QSO solutions `SPE_QSO_ERROR_FLAG == 0`.

No numeric thresholds are given for `SPE_Z_REL`, `SPE_Z_PROB`, `SPE_CONT_SNR`, or chi2; the DPDD does not define a recommended reliability cut. Use `SPE_RANK == 0` for the best candidate **(inference)**. Warning flags have no definition table in the DPDD.

### 5.6 Practical selection recipe (inference)

Join `QUALITY` (flags) + `CLASSIFICATION_CATALOG` + `GALAXY_CANDIDATES_CATALOG` where `SPE_RANK == 0`; require the error flags above to be 0, `SPE_CLASS == 'GALAXY'`, and then choose a cut on `SPE_Z_REL` (and optionally `SPE_Z_PROB`, `SPE_Z_ERR`) calibrated against your own comparison with known spec-z or PHZ; the thresholds must come from validation, not from the DPDD. Check `SPE_GRISM` and `SPE_N_DITH_*` to understand depth: objects with only one grism or few dithers have less reliable lines.

### 5.7 Flag tables

`SPE_ERROR_FLAG` (bit number to meaning): 0 error in context stage (see Amazed table); 1 error in classification stage; 2 unable to read the SIR combined spectrum; 3 empty spectrum; 4 NaN values in the SIR spectrum; 5 data arrays of different size after filtering; 6 short-size spectrum.

`AMAZED_ERROR` codes for the per-stage error flags (value to name): 1 INTERNAL_ERROR, 2 EXTERNAL_LIB_ERROR, 3 INVALID_SPECTRA_FLUX, 4 INVALID_NOISE, 5 SMALL_WAVELENGTH_RANGE, 6 NEGATIVE_CONTINUUMFIT, 7 BAD_CONTINUUMFIT, 8 NULL_AMPLITUDES, 9 PEAK_NOT_FOUND_PDF, 10 MAX_AT_BORDER_PDF, 11 MISSING_PARAMETER, 12 BAD_PARAMETER_VALUE, 13 UNKNOWN_ATTRIBUTE, 14 BAD_LINECATALOG, 15 BAD_LOGSAMPLEDSPECTRUM, 16 BAD_COUNTMATCH, 17 BAD_TEMPLATECATALOG, 18 INVALID_SPECTRUM, 19 OVERLAPFRACTION_NOTACCEPTABLE, 20 DZ_NOT_COMPUTABLE, 21 INCOHERENT_INPUTPARAMETERS, 22 BAD_CALZETTICORR, 23 SPECTRUM_NOT_LOADED, 24 MULTILSF_NOT_HANDLED, 25 UNALLOWED_DUPLICATES, 26 UNSORTED_ARRAY, 27 INVALID_DIRECTORY, 28 INVALID_FILEPATH, 29 INVALID_PARAMETER, 30 MISSING_CONFIG_OPTION, 31 BAD_FILEFORMAT, 32 INCOHERENT_CONFIG_OPTIONS, 33 ATTRIBUTE_NOT_SUPPORTED, 34 INCOMPATIBLE_PDF_MODELSHAPES, 35 UNKNOWN_RESULT_TYPE, 36 RELIABILITY_NEEDS_TENSORFLOW, 37 OUTPUT_READER_ERROR, 38 PYTHON_API_ERROR, 39 INVALID_NAME, 40 INVALID_FILTER_INSTRUCTION, 41 INVALID_FILTER_KEY, 42 NO_CLASSIFICATION, 43 INVALID_PARAMETER_FILE. For the per-stage flags the DPDD only requires "equal to 0" for a clean result.

## 6. SPE Lines catalogue file

File name `EUC_SPE_WIDE-CAT-LIN-[TILE_ID]_[INSTANCE_ID]_[timestamp]Z_[VERSION].fits`. 4 binary-table HDUs, one row per (object, rank, line/index/feature). The `SPECTRAL_LINES_CATALOG` header carries `FSCALE` (scaling factor for flux unit; the table says erg/s/cm2 so check whether to multiply).

| HDU | Columns |
|---|---|
| `SPECTRAL_LINES_CATALOG` (35 columns) | `OBJECT_ID`, `SPE_RANK`, `SPE_LINE_ID` (ID in the reference line catalogue), `SPE_LINE_FLAG`, `SPE_LINE_NAME` (12A), `SPE_LINE_N_DITH`; Gaussian-fit (suffix `_GF`): `SPE_LINE_CENTRAL_WL_GF` (A), `..._WL_ERR_GF`, `SPE_LINE_FLUX_GF` (erg/s/cm2), `SPE_LINE_FLUX_ERR_GF`, `SPE_LINE_EW_GF` (A), `SPE_LINE_EW_ERR_GF`, `SPE_LINE_FWHM_GF` (A), `SPE_LINE_FWHM_ERR_GF`, `SPE_LINE_INTVAR_GF` (erg2/s2/cm4, integrated variance within 3 sigma), `SPE_LINE_SNR_GF`, `SPE_LINE_CONT_GF`, `SPE_LINE_CONT_ERR_GF`, `SPE_LINE_TOTAL_FLUX_ERR_GF` (error on flux of related complex lines), `SPE_LINE_LUM_GF`, `SPE_LINE_LUM_ERR_GF` (erg/s, D), `SPE_LINE_QUAL_GF`; direct-integration (suffix `_DI`): `SPE_LINE_CENTRAL_WL_DI`, `..._WL_ERR_DI`, `SPE_LINE_FLUX_DI`, `..._FLUX_ERR_DI`, `SPE_LINE_EW_DI`, `..._EW_ERR_DI`, `SPE_LINE_SNR_DI`, `SPE_LINE_CONT_DI`, `SPE_LINE_CONT_ERR_DI`, `SPE_LINE_LUM_DI`, `SPE_LINE_LUM_ERR_DI`, `SPE_LINE_QUAL_DI`; and `SPE_LINE_AON` (peak amplitude over local rms noise). |
| `ATOMIC_INDICES_CATALOG` (6) | `OBJECT_ID`, `SPE_RANK`, `SPE_AT_IDX_NAME` (12A, atomic Lick index), `SPE_AT_IDX_VAL` (A), `SPE_AT_IDX_ERR` (A), `SPE_SPEC_SNR` (SNR in a "TBD" window) |
| `MOLECULAR_INDICES_CATALOG` (6) | `OBJECT_ID`, `SPE_RANK`, `SPE_MOL_IDX_NAME`, `SPE_MOL_IDX_VAL` (mag), `SPE_MOL_IDX_ERR` (mag), `SPE_SPEC_SNR` |
| `CONTINUUM_FEATURES_CATALOG` (6) | `OBJECT_ID`, `SPE_RANK`, `SPE_CNT_FEAT_NAME`, `SPE_CNT_FEAT_VAL`, `SPE_CNT_FEAT_ERR`, `SPE_SPEC_SNR` (descriptions copy-pasted from the molecular index) |

### 6.1 Line-measurement quality flag (`SPE_LINE_QUAL_GF`, `SPE_LINE_QUAL_DI`)

A 3-digit integer: digit 1 = measurement type, digit 2 = quality, digit 3 = grism. Values are quoted for both Gaussian fit (GF) and direct integration (DI).

- Digit 1: 1 direct integration; 2 Gaussian fit; 3 H-alpha GF for QSOs; "-" line outside the redshift range.
- Digit 3: 1 blue grism; 2 red grism; 3 blue and red.
- Digit 2:

| 2nd digit | Meaning | Applies to |
|---|---|---|
| 0 | not measured by the standard pipeline (codes 101-103, 201-203, 301-303) | all |
| 1 | good, reliable measurement (111-113, 211-213, 311-313) | all |
| 2 | low SNR, SNR < 2.0 (121-123, 221-223, 321-323) | all |
| 3 | EW > 0, probably negative continuum; EW set to 0, other values kept (231-233, 331-333) | GF or H-alpha QSO |
| 4 | issue for combination, the two grism measures are not both good; weighted average given when possible (143, 243, 343) | BGS+RGS only |
| 5 | acceptable, up to 15 percent of the pixels in the line missing (251, 252, 351, 352) | GF or H-alpha QSO |
| 7 | merging error in blue+red combination (173, 273) | BGS+RGS only |
| 8 | unreliable or wrong flux: more than 15 percent pixels missing (GF/QSO) or more than 1 pixel missing (DI) (181, 182, 281, 282, 381, 382) | all |
| 9 | line not measurable in the redshift range (-91, -92, -93) | all |

Recommended (inference): keep digit 2 = 1 for clean line fluxes (for example `SPE_LINE_QUAL_GF` in {211, 212, 213}), and use digit 3 to see which grism supplied the line.

## 7. SPE Models catalogue file

File name `EUC_SPE_WIDE-CAT-MOD-[TILE_ID]_[INSTANCE_ID]_[timestamp]Z_[VERSION].fits`; 4 HDUs, the best-fit model parameters per candidate (to rebuild the model spectrum).

| HDU | Columns |
|---|---|
| `LINES_CATALOG` (4) | `SPE_LINE_ID` (I), `SPE_LINE_WL` (A), `SPE_LINE_NAME` (12A), `SPE_LINE_TYPE` ('A' absorption, 'E' emission); the reference line list |
| `GALAXY_MODELS_CATALOG` (22) | `OBJECT_ID`, `SPE_RANK`, `SPE_Z`, `SPE_CNT_TPL_ID` (continuum template), `SPE_CNT_TPL_AMP`, `SPE_CNT_IGM_TPL_ID`, `SPE_CNT_ISM_COEF` (E(B-V) in [0,1]), `SPE_TPL_RAT_ID`, `SPE_TPL_RAT_E_AMP`, `SPE_TPL_RAT_A_AMP`, `SPE_TPL_RAT_ISM_COEFF`, `SPE_LINES_ID` (60I), `SPE_LINES_AMP` (60E, erg/s/cm2/A), `SPE_VEL_DISP_E`, `SPE_VEL_DISP_A` (km/s), `SPE_LYA_OFFSET`, `SPE_LYA_WIDTH`, `SPE_LYA_ASSYM_COEF`, `SPE_LYA_IGM`, `SPE_ICAL_FACTOR_B` (red-to-blue inter-calibration factor), `SPE_FLUX_OFFSET_R`, `SPE_FLUX_OFFSET_B` (erg/s/cm2/A) |
| `STAR_MODELS_CATALOG` (8) | `OBJECT_ID`, `SPE_RANK`, `SPE_Z`, `SPE_CNT_TPL_ID`, `SPE_CNT_TPL_AMP`, `SPE_ICAL_FACTOR_B`, `SPE_FLUX_OFFSET_R`, `SPE_FLUX_OFFSET_B` |
| `QSO_MODELS_CATALOG` (22) | same layout as the galaxy models (here `SPE_TPL_RAT_ID` is an integer, in the galaxy table a 48A string) |

## 8. Joining to MER

- **Key**: `OBJECT_ID` (K, int64), "unique ID of the object in the survey, as set by MER", present in every SPE table. For SIR combined spectra the ID is `OBJ_ID` in the `m_META` header (and `OBJ_ID` in the contaminant tables).
- SPE and SIR products are per MER tile (`TILE_ID` in the SIR primary header and SPE file name). Match tile-wise to the MER Final Catalog of the same tile.
- Candidate/line/model tables are one-to-many in `OBJECT_ID`: filter `SPE_RANK == 0` before joining one row per object to MER.
- The SPE products are spectroscopy of the MER catalogue objects, but only objects with an extracted SIR spectrum have meaningful rows; most MER objects will not appear in the SPE tables (use a left join from MER).

## 9. Caveats and gaps

1. No numeric reliability thresholds in the DPDD; calibrate yourself against known spec-z.
2. The SIR mask dictionary is labelled "bit position" but looks like bit values; verify on a real file.
3. SIR flux unit already includes the 1e-16 scaling; `FSCALE` is deprecated, but the lines catalogue header has its own `FSCALE` keyword whose role is only "scaling factor for flux unit".
4. SPE PDF-catalogue file layout is not described; per-candidate PDFs are in `SPE_PDF` (80 samples on the `SPE_PDF_ZMIN`..`SPE_PDF_ZMAX` window).
5. Copy-paste errors in the DPDD (continuum-feature descriptions that say "molecular Lick index", "TBD" SNR window) mean the descriptions of those HDUs are not reliable.
6. Slitless spectra can be contaminated by neighbours: use the `CONTAMINANTS` tables and the `QUALITY` column; blended large nearby galaxies are likely to have contaminated or truncated spectra **(inference)**.
