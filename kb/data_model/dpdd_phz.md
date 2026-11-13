# Euclid DR1 DPDD: PHZ (photometric redshift) data products

**How to use this note.** This is a condensed data-model reference for the PHZ processing function (PF) as described in the DR1 Data Product Description Document (DPDD). Use it to look up which PHZ file holds which column, what the units/flag codes mean, and how to join to the MER catalogue. Statements marked **(DPDD)** come directly from the DPDD pages; statements marked **(inference)** are my reading or a suggested practice and are not stated in the DPDD. The DPDD itself says some items are "TBD" or are internally inconsistent; those are called out in the "Gaps and oddities" section. Column lists for unit-less columns: the DPDD gives "NA" as unit for nearly every non-flux column.

**Source files** (all in `~/Desktop/euclid/text/dpdd/`): `phzdpd__phzintro.md`, `phzdpd__phzindex.md`, `phzdpd__dpcards__phz_phzpfoutputcatalog.md`, `phzdpd__dpcards__phz_phzpfoutputforl3.md`, `phzdpd__dpcards__phz_phzdeepoutputcatalog.md`, `phzdpd__dpcards__phz_classificationinput.md`, `phzdpd__dpcards__phz_modelcomponents.md`, `phzdpd__dpcards__phz_referencesample.md`, `phzdpd__dpcards__phz_specdbinput.md`. Online: https://euclid.esac.esa.int/dr/dr1/dpdd/phzdpd/phzindex.html

## 1. Overview and product map

- PHZ takes the **MER Final Catalog** (photometry + morphology) as main input and produces, per MER tile: photo-z PDFs and point estimates, classification (star/galaxy/QSO/globular cluster), unified fluxes, star and galaxy SEDs, physical parameters, and tomographic-bin assignments **(DPDD)**.
- Per-tile outputs are split over several FITS files "to simplify retrieval and use by L3 PFs" **(DPDD)**. All have an `OBJECT_ID` column (FITS `K`, int64) "as set by MER": this is the join key.
- Not distributed with DR1-Foundation: `DpdPhzAnalysisResult` (validation report), `PHZBinMeanRedshift`, `PHZCoAddedPDZBiasMap` (these will exist for DR1 proper) **(DPDD)**.

| DPDD product (data product name) | Role | Files (name pattern `EUC_PHZ_<X>__<timestamp>Z_00.00.fits.gz`) |
|---|---|---|
| **PHZ PF output catalog for WL** (`DpdPhzPfOutputCatalog`) | Main photo-z product, used by SHE and LE3 | `PHZCAT` (2 HDUs), `STARSED`, `GALAXYSED` |
| **PHZ PF output catalog for LE3** (`DpdPhzPfOutputForL3`) | Classification, physical parameters, AGN/QSO/NIR parameters, GC list, star templates | `CLASSCAT`, `PHYSPARAM`, `PHYSPARAMQAGN`, `PHYSPARAMQSO`, `PHYSPARAMNIR`, `GLOBULARCLUSTERCAT`, `STARCLASS` |
| **PHZ PF output catalog for Deep tiles** (`DpdPhzDeepOutputCatalog`) | Same photo-z table as WL for Deep fields, plus sampled physical parameters (binary files) and star SED catalog | `PHZCAT`, sampled physical-parameter binary files, `STARSED` |
| Classification Training Sample (`DpdClassificationInput`) | Input (training sample for classification); built outside the pipeline | FITS table; columns "mainly following MER catalog"; the DPDD does not list them |
| Phosphoros model-grid configuration (`DpdModelComponents`) | Input config | not described beyond metadata |
| Reference Sample (`DpdReferenceSample`) | Input to NNPZ (PDZ / physical-parameter / SED reference objects) | `.npy` index, SED, PDZ, sampling files plus a photometry FITS |
| Spec-z input (`DpdSpecDbInput`) | Input to the SomSpecZ pipeline (spec-z database in MER-like columns) | FITS, 383 columns |

Schema files are `euc-phz-<Name>.xsd` in the ST_DataModel repo (version 10.1.4 cited for the WL product). Catalog formats follow "phz.* version 0.9" descriptions.

## 2. PHZ output for WL: `DpdPhzPfOutputCatalog`

Created by the PHZ Catalog Merger, which merges NNPZ (PDF/SED), PDF Statistics and Classification outputs **(DPDD)**.

### 2.1 `EUC_PHZ_PHZCAT` : 2 table HDUs

- **HDU "PhotoZ Catalog"** (name as written in the DPDD, with a space): 41 columns, one row per object of the tile.
- **HDU `ZERO_POINT`**: header keyword `ZP_CORRECTION_STATUS` = `Computed` (diagnostic only) or `Applied` (correction applied to photometry before analysis). Table with 2 columns: `FILTER` (25A) and `CORRECTION` (E, multiplicative factor). Zero points come from Gaia stars in the tile **(DPDD)**.

### 2.2 PhotoZ Catalog columns (41)

| Column group | Column | Format | Meaning |
|---|---|---|---|
| Key | `OBJECT_ID` | K | MER object ID |
| PDF | `PHZ_PDF` | 601E | PDF values on z = 0 to 6, step 0.01 (601 samples) |
| Point estimate | `PHZ_MEDIAN` | E | median of the PDF |
| Intervals | `PHZ_70_INT`, `PHZ_90_INT`, `PHZ_95_INT` | 2E | smallest PDF interval (lower, upper) holding 70/90/95 percent of the probability |
| Modes | `PHZ_MODE_1` | E | first mode of the PDF |
| | `PHZ_MODE_1_AREA` | E | total area of the first mode |
| | `PHZ_MODE_2` | E | redshift of the global maximum a posteriori solution (name is misleading; see oddities) |
| | `PHZ_MODE_2_AREA` | E | "Not used" |
| Bias map | `BIAS_ID` | J | identifier to look up the bias-correction shift in the bias-correction map |
| Tomography | `TOM_BIN_ID` | J | tomographic bin, equipopulated bins |
| | `ALT_TOM_BIN_ID` | J | alternate tomographic bin, equidistant bins |
| | `POS_TOM_BIN_ID` | J | photometric-clustering tomographic bin, equipopulated |
| | `FLAG_SOM_TOMOBIN`, `FLAG_SOM_ALT_TOMOBIN`, `FLAG_SOM_POS_TOMOBIN` | J | 1 if the SOM-cell x tomographic-bin combination can be calibrated, 0 if not |
| Photometric setup | `PHOTOMETRIC_SYSTEM` | J | encodes the band configuration (also number of missing columns) |
| Classification | `PHZ_CLASSIFICATION` | J | bit-coded class (section 5) |
| Weights | `IE_CUTS_WEIGHTS` | 4E | probability of being a usable source for VIS magnitude cuts [20.25, 21.25, 22.25, 24.5] |
| | `PHZ_WEIGHT` | E | probability of being a usable source at VIS mag = 23.5 |
| Flags | `PHZ_FLAGS` | J | processing flags (section 6) |
| Unified fluxes | `FLUX_{U,G,R,I,Z}_EXT_DECAM_UNIF`, `FLUX_VIS_UNIF`, `FLUX_{Y,J,H}_UNIF` | E, uJy | flux "recomputed after correction from galactic extinction and filter shifts" |
| Unified flux errors | `FLUXERR_*_UNIF` for the same 9 bands | E, uJy | errors on the above |
| Fit quality | `BEST_CHI2` | E | chi2 of the best-fit model or of the closest neighbour |

The 9 unified bands: DECam u, g, r, i, z (external), Euclid VIS, NISP Y, J, H.

### 2.3 `EUC_PHZ_STARSED` and `EUC_PHZ_GALAXYSED` (120 columns each, identical layout)

- `OBJECT_ID`.
- `FLUX_4500_4600` ... `FLUX_9900_10000`: flux in 55 top-hat bands of 100 Angstrom between 4500 and 10000 A, unit uJy (E). Matching `FLUXERR_<lo>_<hi>` columns.
- `PHZ_FLAGS` (64-bit K): 0 = OK, 1 = no close neighbour (the DPDD writes "I").
- `PHZ_GAL_PROB`, `GALAXY_THRESHOLD`, `PHZ_STAR_PROB`, `STAR_THRESHOLD`, `PHZ_QSO_PROB`, `QSO_THRESHOLD`, `PHZ_GLOB_CL_PROB`, `GLOBC_THRESHOLD` (E).
- The Star SED catalog holds SEDs for objects identified as stars; the Galaxy SED catalog holds SEDs for objects identified as galaxies. Presumably the SED is the best-fitting/neighbour-averaged template integrated in these bins **(inference)**.

## 3. PHZ output for LE3: `DpdPhzPfOutputForL3`

Created by the PHZ Catalog Merger from Phosphoros, NNPZ, PDF Statistics and Classification outputs. Used by LE3 **(DPDD)**.

### 3.1 `EUC_PHZ_CLASSCAT`: classification catalog (13 columns)

| Column | Format | Meaning |
|---|---|---|
| `OBJECT_ID` | K | MER ID |
| `CONFIGURATION` | J | photometric band configuration code (same concept as `PHOTOMETRIC_SYSTEM` in PHZCAT) |
| `PHZ_STAR_PROB`, `PHZ_GAL_PROB`, `PHZ_QSO_PROB`, `PHZ_GLOB_CL_PROB` | E | class probabilities (star, galaxy, QSO, globular cluster) |
| `PHZ_CLASSIFICATION` | J | bit-coded accepted class (section 5) |
| `VIS_DET` | K | copied from MER: 1 = detected on VIS image, 0 = detected on the NIR stack |
| `MISSING_BAND` | 255A | names of missing photometries |
| `STAR_THRESHOLD`, `GALAXY_THRESHOLD`, `QSO_THRESHOLD`, `GLOBC_THRESHOLD` | E | probability above which the object is accepted as that class |

### 3.2 `EUC_PHZ_PHYSPARAM`: physical parameters (galaxies; 93 columns)

Structure: 6 bookkeeping columns, 28 parameters x 3 columns each (84), plus 3 integer codes.

Bookkeeping: `OBJECT_ID` (K); `PHYS_PARAM_FLAGS` (J; "64 bit integer containing flags (TBD)"); `PHZ_PDF_NN_ID` (30J, neighbour IDs in the reference sample); `PHZ_PDF_NN_WEIGHT` (30E); `PHZ_PDF_NN_SCALE` (30E); `QUALITY_FLAG` (J).

Per parameter `X`, three columns: `PHZ_PP_MEDIAN_X` (E), `PHZ_PP_MODE_X` (E), `PHZ_PP_68_X` (2E, lower and upper bound of the 68 percent interval of the PDF). The 28 parameters:

| Suffix `X` | Meaning (as stated) |
|---|---|
| `REDSHIFT` | redshift from the physical-parameter PDF |
| `STELLARMASS` | log10(stellar mass / Msun) |
| `SFR` | log10(SFR / (Msun/yr)) |
| `MASSFORMED` | log10(mass formed / Msun), mass formed = integral of the SFR |
| `STELLARMETALLICITY` | stellar metallicity |
| `SFHAGE`, `SFHTIMESCALE` | star-formation-history age and timescale |
| `AV` | V-band dust attenuation |
| `DUSTLAWHEIGHT`, `DUSTLAWSLOPE`, `DUSTLAWWIDTH` | dust-law shape parameters |
| `SCALING` | absolute scaling of the template in solar luminosities |
| `AGNEBV`, `AGNLBOL`, `AGNLUMFRAC` | AGN E(B-V), bolometric luminosity, luminosity fraction |
| `MFUV`, `MNUV`, `MU`, `MB`, `MV`, `MR`, `MI`, `MZ`, `MVIS`, `MY`, `MJ`, `MH`, `MKs` | absolute magnitudes in FUV, NUV, U, B, V, R, I, Z, VIS, Y, J, H, Ks (the DPDD does not state the magnitude system or rest/observed convention) |

Final 3 columns: `GALAXYCLASS` (K), `SFHTYPE` (K), `IMF` (K): integer codes; the DPDD gives no code table.

All unit fields are "NA" in the DPDD table; the physical units are only in the descriptions (log10 Msun, log10 Msun/yr).

### 3.3 `EUC_PHZ_PHYSPARAMQAGN`: AGN physical parameters (6 columns)

`OBJECT_ID` (K), `PHYS_PARAM_FLAGS` (K), `PHZ_PDF_NN_ID` (100E), `PHZ_PDF_NN_WEIGHT` (100E), `PHZ_PDF_NN_SCALE` (100E), `QUALITY_FLAG` (E). It holds neighbour lists only (100 neighbours); the AGN parameter values are not tabulated here.

### 3.4 `EUC_PHZ_PHYSPARAMQSO` (QSO, 55 columns) and `EUC_PHZ_PHYSPARAMNIR` (NIR-based, 16 columns)

These Phosphoros-style template-fit tables share a column pattern (the DPDD prints 15 columns for QSO, though it states 55; see oddities):

| Column | Format | Meaning |
|---|---|---|
| `OBJECT_ID` | K | MER ID |
| `Z-1D-PDF` | 121D (QSO), 681D (NIR) | redshift PDF; binning is in the HDU header |
| `region-Index` | K | region of the template grid containing the best model |
| `SED`, `SED-Index` | 16A, K | best-fit SED name and index |
| `ReddeningCurve`, `ReddeningCurve-Index` | 16A, K | best-fit reddening curve |
| `E(B-V)`, `E(B-V)-Index` | D, K | best-fit E(B-V) |
| `Z`, `Z-Index` | D, K | best-fit redshift |
| `Scale` | D | scale of the best-fit model |
| `Posterior-Log`, `Likelihood-Log` | D | log posterior / log likelihood |
| `1DPDF-Peak-Z` | D | peak of the 1-D redshift PDF |
| `HIGH_Z_PROB` (NIR table only) | D | probability to be above z = 6 |

### 3.5 `EUC_PHZ_GLOBULARCLUSTERCAT` (3 columns)

`OBJECT_ID` (K), `RIGHT_ASCENSION` (K as written; decimal degrees, SExtractor ALPHA_J2000), `DECLINATION` (E; decimal degrees). The K format for RA is probably a typo in the DPDD **(inference)**.

### 3.6 `EUC_PHZ_STARCLASS`: star template fits (56 columns stated, 16 printed)

Same Phosphoros-style columns as the QSO table (`region-Index`, `SED`, `SED-Index`, `ReddeningCurve`, `E(B-V)`, `Z`, `Scale`, `Posterior-Log`, `Likelihood-Log`) plus stellar parameters `FEH` (Fe/H), `LOGG` (log g), `TEFF` (K), all D. The DPDD description of `region-Index` is a copy of the `OBJECT_ID` text (a copy-paste error).

## 4. Deep-tile product: `DpdPhzDeepOutputCatalog`

Created by the PHZ Deep pipeline. The photo-z table has the same 41 columns as the WL `PHZCAT` (section 2.2). It adds "Sampled Physical Parameters" as a set of binary files containing samplings of the physical parameters (no column description), and a Star SED catalog `EUC_PHZ_STARSED` (not tabulated on this page; same pattern as section 2.3).

## 5. Classification codes

`PHZ_CLASSIFICATION` is an integer flag, documented as "[|]1 if accepted as star, [|]2 if accepted as a galaxy, [|]4 if accepted as a QSO, [|]8 if accepted as a globular cluster" (the bracketed pipe looks like a bitwise OR sign lost in conversion).

| Bit value | Class | Accepted when |
|---|---|---|
| 1 | star | `PHZ_STAR_PROB` above `STAR_THRESHOLD` |
| 2 | galaxy | `PHZ_GAL_PROB` above `GALAXY_THRESHOLD` |
| 4 | QSO | `PHZ_QSO_PROB` above `QSO_THRESHOLD` |
| 8 | globular cluster | `PHZ_GLOB_CL_PROB` above `GLOBC_THRESHOLD` |

The threshold relation is stated in the threshold column descriptions. Because the codes are powers of two and described as OR-ed flags, a source can carry several classes, for example 6 = galaxy + QSO **(inference)**. Select galaxies with `(PHZ_CLASSIFICATION & 2) != 0`; to exclude composites also require `(PHZ_CLASSIFICATION & (1|4|8)) == 0` **(inference)**. Probabilities and thresholds are given per object, so you can re-threshold yourself.

## 6. Flags

| Flag column | Product | Documented values |
|---|---|---|
| `PHZ_FLAGS` (J) | PHZCAT | "0 => OK, 1 => NNPZ flag: no close neighbor, 10 not VIS detected, 11 missing band, 12 too faint" |
| `PHZ_FLAGS` (K, 64-bit) | STARSED / GALAXYSED | 0 = OK, 1 = no close neighbour |
| `PHYS_PARAM_FLAGS` | PHYSPARAM, PHYSPARAMQAGN | "TBD"; no definition |
| `QUALITY_FLAG` | PHYSPARAM, PHYSPARAMQAGN | no definition |
| `FLAG_SOM_*_TOMOBIN` | PHZCAT | 1 = calibratable SOM-cell/bin combination, 0 = not |
| `VIS_DET` | CLASSCAT | 1 = VIS-detected, 0 = NIR-stack-detected |

Ambiguity: the PHZCAT list "1, 10, 11, 12" mixes what look like bit positions with a value; it is not stated whether 10, 11, 12 are decimal values or bit positions (2^10 etc.). Test empirically on real data before relying on this (the value distribution will show it).

## 7. Joining to MER, selections

- **Join key**: `OBJECT_ID` (int64, FITS `K`), identical to the MER Final Catalog `OBJECT_ID`. PHZ outputs are produced per MER tile, so also keep the tile ID from the file name / MER side when merging tile-wise. All PHZ tables in one tile use the same key, so PHZCAT, CLASSCAT, PHYSPARAM, SED tables join one-to-one on `OBJECT_ID` (some tables may only contain subsets, e.g. QSO or star tables; do a left join) **(inference)**.
- Duplicates across overlapping tiles: the DPDD does not say how objects in tile overlaps are de-duplicated; check MER documentation **(not in the PHZ pages)**.
- **Suggested selection for a galaxy sample** (inference, not DPDD-prescribed): `PHZ_CLASSIFICATION & 2`; `PHZ_FLAGS == 0` (or inspect the values 10/11/12 as "not VIS detected / missing band / too faint"); weight by `PHZ_WEIGHT` or the `IE_CUTS_WEIGHTS` entry closest to your VIS magnitude limit when emulating the weak-lensing selection; use `PHZ_90_INT` width as a per-object photo-z quality indicator; use `BEST_CHI2` to reject poor template fits; for tomographic work require the relevant `FLAG_SOM_*_TOMOBIN == 1`.
- For low-z work use `PHZ_MEDIAN` (point estimate) or the full `PHZ_PDF`; `PHZ_MODE_1` is the dominant peak.
- For physical parameters (stellar mass, SFR) use `PHZ_PP_MEDIAN_STELLARMASS` etc. from `PHYSPARAM`, join on `OBJECT_ID`; note that these come from a neighbour-based PDF (`PHZ_PDF_NN_*`) built on a reference sample, not a per-object SED fit **(inference from column design)**.

## 8. Input and calibration products (for provenance)

- **Reference Sample** (`DpdReferenceSample`): field gives the sample type: `PHZ` (reference with PDZ information), `PP` (physical-parameter information), `GAL_SED`, `STAR_SED`. Up to five file types: an **Index** numpy array (`.npy`) linking each reference object to its records (e.g. `pdz_file`, `pdz_offset`); **SED data files** `sed_data_XX.bin` (`.npy`, each SED an (N,2) array of wavelength and value, files of about 1 GB); **PDZ data files** `pdz_data_XX.bin` (shape (N records, M redshift samples)); **sampling files** `pp_data_XX.bin` (shape (N objects, M samples), structured dtype holds parameter names); and a **Photometry** FITS file whose first HDU has `EXTNAME=NNPZ_PHOTOMETRY` and keyword `PHOTYPE` in {Photons, F_nu, F_nu_uJy, F_lambda, MAG_AB}; first column `ID` (int64), other columns float32 with optional `_ERR` columns; further HDUs hold filter transmissions (wavelength in Angstrom, transmission 0 to 1) named after the band.
- **Spec-z input** (`DpdSpecDbInput`, 383 columns, "mainly following MER catalog"): `OBJECT_ID`, `RIGHT_ASCENSION`, `DECLINATION`; fluxes and errors in uJy for VIS, Y, J, H, NIR stack, and external bands (DECam ugriz, LSST ugriz, Megacam u r, JPCam g, PanSTARRS i z, HSC g z) in 1-4 FWHM apertures on PSF-matched images (`FLUX_<band>_<n>FWHM_APER`), TPHOT template-fitting fluxes (`*_TEMPLFIT`, `FLUX_VIS_TO_<band>_TEMPLFIT`), `FLUX_VIS_PSF`, segmentation/total fluxes, Sersic and Disk+Sersic model fluxes (`*_SERSIC`, `*_DISK_SERSIC`), `AVG_TRANS_WAVE_<band>` (Angstrom), `GAL_EBV`, `GAL_EBV_ERR`, `GAL_SPEC_Z`, `GAL_SPEC_Z_ERR`, and weights (`NO_WEIGHT`, `PHZ_WEIGHT`, `IE_CUTS_WEIGHTS`, and shear-method weights KSB, LENS_MC, MOMENTS_ML, REGAUSS, METACAL, GENERIC). This is an internal training input; it is useful mainly as a map of which MER column families exist. The flux-error descriptions for `FLUX_SEGMENTATION`/`FLUX_DETECTION_TOTAL` are shuffled in the DPDD table.
- **Classification Training Sample** and **Model Components**: only metadata given.

## 9. Gaps and oddities in the DPDD (verify on real files)

1. `PHZ_MODE_2` is described as "redshift of the global maximum a posteriori solution", not a second mode; `PHZ_MODE_2_AREA` is "Not used".
2. No explicit recommended cuts, no PDF sampling for `Z-1D-PDF` (see HDU header), no tomographic-bin edges, no definition of `PHOTOMETRIC_SYSTEM`/`CONFIGURATION` codes, no `QUALITY_FLAG`/`PHYS_PARAM_FLAGS` definitions, no code table for `GALAXYCLASS`, `SFHTYPE`, `IMF`.
3. Table sizes disagree with printed columns for `PHYSPARAMQSO` (55 stated, 15 printed) and `STARCLASS` (56 stated, 16 printed); the DPDD listing is truncated.
4. Absolute-magnitude and metallicity columns carry no unit in the table.
5. Unified fluxes are corrected for Galactic extinction and filter shifts; this differs from the MER fluxes, so do not mix the two in colours without care **(inference)**.
