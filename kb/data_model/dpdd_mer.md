# Euclid DR1 DPDD: MER products (mosaics, segmentation map, final catalogue)

**How to use this note.** Data-model reference for the MER (Merging) Processing Function products in Euclid DR1-Foundation (DPDD v2.0, data model DM 10.1.4). Use section 1 to open a mosaic correctly (units, zero point, WCS), section 2 for the MER background step (what is, and mostly is not, documented), section 4 to look up catalogue columns and flag bits, and section 5 for the cookbook recommendations. Statements marked **[derived]** are my own arithmetic, not in the DPDD. Statements marked **[DPDD gap]** mean the DPDD is silent or internally inconsistent; verify against a real file header.

**Sources** (all in `~/Desktop/euclid/text/dpdd/`): `merdpd__merintro.md`, `merdpd__merindex.md`, `merdpd__dpcards__mer_bksmosaic.md`, `merdpd__dpcards__mer_finalcatalog.md`, `merdpd__dpcards__mer_segmentationmap.md`, `merdpd__merphotometrycookbook.md`, `merdpd__mermorphologycookbook.md`; context from `sasdataproducts.md`, `missing__missing-index.md`.

---

## 0. What MER does and which MER products exist in DR1

MER takes VIS calibrated quad frames, NIR calibrated frames and EXT stacked frames overlapping a MER tile, mosaics them, runs a residual background subtraction, detects sources on a VIS detection mosaic and on a NIR-stack detection mosaic (VIS has priority), deblends, merges the two lists, propagates PSFs, then measures: Kron total flux (detection mosaic), aperture photometry (A-PHOT) and template-fitting photometry (T-PHOT) in all bands, PSF-fitting photometry (VIS), CAS and ML morphology (VIS-detected sources), and finally a SourceXtractor++ Sersic fit in all bands.

| Product | DPD name | In SAS (DR1) | Notes |
|---|---|---|---|
| Background-subtracted mosaic (+ auxiliary files) | `DpdMerBksMosaic` | yes | one per band per tile |
| Segmentation map | `DpdMerSegmentationMap` | yes | VIS+NIR combined |
| Final catalogue (main, morphology, cutouts, deep) | `DpdMerFinalCatalog` | yes | |
| Detection mosaic | `DpdMerDetectionMosaic` | **no** | "not distributed in DR1-Foundation" |
| Tile definition, MER tile list | `DpdMerTile`, `DpdMerTileList` | no | tile geometry only via mosaic WCS/footprint |
| PSF stamp collection, PSF transformation kernel | `DpdMerPsfStampCollection`, `DpdMerPsfTransformationKernel` | no | the PSF stamps in the mosaic PSF file are the only PSF product |
| Un-merged / single-band / object catalogues | `DpdMerSingleBandCatalog`, `DpdMerObjectCatalog`, `DpdMerCrossMatchedCatalog`, `DpdMerMorphologyCatalog`, `DpdMerMosaic` | no | morphology table is shipped inside `DpdMerFinalCatalog` |
| Config / ML models / DQC limits / analysis & validation | `DpdMerConfigurationSet`, `DpdMerMachineLearningModels`, `DpdMerDqcStaticFlagLimits`, `DpdMerAnalysisResult`, `DpdMerExtendedAnalysisResult`, `DpdMerValidation*`, `DpdMerTrueUniverse*Catalog` | no | so the actual MER background parameters (MERConfigurationSet) are not public |

Every product has four XML-level elements: `Header` (sys:genericHeader), `Data`, `QualityFlags` (dqc:...), `Parameters` (ppr:genericKeyValueParameters). The science data live in FITS files linked from `Data`.

---

## 1. `DpdMerBksMosaic`: background-subtracted mosaic and auxiliary layers

### 1.1 Geometry and conventions

- **Pixel scale**: 0.1 arcsec x 0.1 arcsec, identical for **all** bands (the DPDD says MER mosaics share the pixel scale and FoV; EXT frames are rebinned to it; native VIS and NISP pixel scales are not stated in the MER cards).
- **Field of view**: same for all bands, built from the MER tile *outer* spatial footprint. "Typically" 32' x 32' for WIDE tiles and 17' x 17' for DEEP tiles. **[derived]** this is about 19200 x 19200 px (WIDE) and about 10200 x 10200 px (DEEP); the DPDD gives no NAXIS values.
- **Catalogue vs mosaic**: the final catalogue contains only sources in the tile *core* area (no duplicates across neighbouring tiles), so sources near a mosaic edge are in the neighbour tile's catalogue.
- **WCS** (image, RMS, flag, filter-transmission, background files): linear CD matrix keywords `CD1_1, CD1_2, CD2_1, CD2_2`, `CRPIX1/2`, `CRVAL1/2`, `CTYPE1/2`, `CUNIT1/2`, `RADESYS`, `EQUINOX`. These are SWarp-written headers. Resampling-related keywords recorded: `CENTERT1/2` (CENTER_TYPE), `PSCALET1/2` (PIXELSCALE_TYPE), `RESAMPT1/2` (RESAMPLING_TYPE), `COMBINET` (COMBINE_TYPE). The DPDD does not give their values (projection type, resampling kernel, combine type), so check the header. Segmentation map uses a *different* WCS style (see 3).
- **Data type / HDU names**: the DPDD lists only a `PRIMARY` header per file and gives `BITPIX` as a generic "array data type". Data type and HDU/EXTNAME layout are **[DPDD gap]**; the mosaic image, RMS and flag maps are described as single-image files whose keywords are all in the PRIMARY header (so the image is presumably in the primary HDU). The PSF and layer files additionally have table/image extensions (below).
- **Per-band naming**: `[filter_name]` follows the `Filter` element, e.g. `VIS`, `NIR_Y`, `NIR_J`, `NIR_H`, `DECAM_g`, `LSST_u`. `Instrument` is VIS/NIR/DECAM, telescope Euclid/NOAO/LSST.
- Other product-level metadata: `ZeroPoint`, `ImgSpatialFootprint`, `TileIndex`, `PatchIdList`, `ObservationIdList`, `CalblockIdList`, `CalblockVariantList`, `ProcessingMode` (WIDE/DEEP), `ReferenceObservationDateTime` (reference epoch for Gaia proper-motion correction), `FirstObservationDateTime`, `LastObservationDateTime`.

### 1.2 Pixel units and conversion to AB magnitude (critical)

DPDD statement for the image and RMS maps: units depend on provenance:

| Band origin | Pixel unit stated by DPDD |
|---|---|
| VIS | **ADU/sec** |
| NIR | **electrons** (no "per second" stated) |
| EXT | arbitrary units |

"In all cases, image units can be translated to physical units using the mosaic Zero Point":

```
m_AB = -2.5 * log10(image_value) + ZeroPoint          (DPDD eq. 9)
```

- The zero point is in the image-file (and RMS-file) PRIMARY header as **`MAGZERO`** ("AB zeropoint", double). `MAGZERO` is *not* listed in the flag, background, PSF, filter-transmission or layers file headers.
- No `BUNIT`, `EXPTIME`, `GAIN`, or `PHOTFNU`-style keyword is listed for mosaics. So everything needed is `MAGZERO` plus the unit convention above. **[DPDD gap]**: the NIR "electrons" statement is odd given the same formula applies; treat the (VIS: ADU/s, NIR: e-, EXT: arbitrary) statement as unverified until checked against one real file, e.g. by comparing `10**((23.9-MAGZERO)/2.5) * pixel_sum_in_aperture` with the catalogue `FLUX_<band>_nFWHM_APER` (uJy) for an isolated star.
- Catalogue fluxes are in uJy with fixed ZP **23.9** (see 5.4): `m_AB = -2.5 log10(F_uJy) + 23.9`. So the implied pixel-to-uJy factor is `10**((23.9 - MAGZERO)/2.5)` **[derived]**.
- **Surface brightness** is not described in the mosaic card. **[derived]** with 0.1" pixels (0.01 arcsec^2): `mu [mag/arcsec^2] = MAGZERO - 2.5 log10(pixel_value) + 2.5 log10(0.01) = MAGZERO - 2.5 log10(pixel_value) - 5.0`.
- RMS map: same units as the image. VIS and NIR RMS include a Poisson-noise contribution (can be significant for bright sources); **EXT RMS currently does not include Poisson noise**.
- Flag map: integer bit mask; MER propagates input flags with a bitwise **OR** (one flagged input pixel flags the mosaic pixel). Bit meanings differ per band because they are inherited from VIS, NIR, or EXT definitions (see `dpdd_vis_nir.md` for VIS and NIR bits; EXT flag definitions are not documented in DR1 DPDD).

### 1.3 Files in the product

All names begin with the stated prefix (the DPDD only promises "always start with"; the suffix, e.g. date/extension, is not given). `TILE[tile index]` is the MER tile index.

| Element | File name prefix | Content | HDUs / structure documented |
|---|---|---|---|
| `DataStorage` | `EUC_MER_BGSUB-MOSAIC-[filter_name]_TILE[tile index]` | background-subtracted science mosaic | PRIMARY header (SWarp + MAGZERO + FILTER + provenance keywords) |
| `RmsStorage` | `EUC_MER_MOSAIC-[filter_name]-RMS_TILE[tile index]` | propagated 1-sigma noise map | PRIMARY header, includes MAGZERO |
| `FlagStorage` | `EUC_MER_MOSAIC-[filter_name]-FLAG_TILE[tile index]` | OR-propagated input bit flags | PRIMARY header, `EXTEND` present |
| `PsfModelStorage` | `EUC_MER_CATALOG-PSF-[filter_name]_TILE[tile index]` | propagated PSF stamps, one per (most) catalogue sources | PRIMARY (no data keywords of note) + **image extension** (all stamps on a regular grid; header keyword `STMPSIZE` = stamp size in px) + **table extension** (7 columns, below) |
| `FilterTransmissionStorage` | `EUC_MER_FILTER-TRANSMISSION-[filter_name]_TILE[tile index]` | per-pixel average filter-transmission wavelength | PRIMARY header, CD matrix, FILTER |
| `LayersStorage` | `EUC_MER_DETECTOR-LAYERING-[filter_name]_TILE[tile index]` | which input VIS/NIR images contributed (Euclid bands only) | table, 8 columns (below) |
| `BrightStarMasksStorage` | `EUC_MER_STAR-MASKS-[filter_name]_TILE[tile index]` | bright-star masks (JSON) | per Gaia star: RA, Dec, brightness, polygon |
| `BackgroundStorage` | `EUC_MER_BGMOD-[filter_name]_TILE[tile index]` | **MER-step** background model that was subtracted | PRIMARY header, CD matrix, FILTER (no MAGZERO) |

Other keywords present in image/RMS headers: `FILTER`, `DATASETR` (pipeline data-set release), `PIPDEFID`, `PPLANID`, `PPOID`, `PSWNAME`, `PSWREL`, and SWarp provenance `AUTHOR`, `DATE`, `ORIGIN`, `SOFTAUTH`, `SOFTDATE`, `SOFTINST`, `SOFTNAME`, `SOFTVERS`.

There is **no file called `GRID_PSF`** in the DPDD. The closest object is the PSF FITS file above (stamps on a regular grid in an image extension plus a coordinate table).

**PSF stamp table (7 columns)**

| Column | Meaning | Unit |
|---|---|---|
| `x_center`, `y_center` | stamp-centre pixel position inside the PSF image extension | pix |
| `x`, `y` | stamp pixel coordinate on the associated mosaic | pix |
| `RA`, `Dec` | stamp sky position | deg |
| `FWHM` | Gaussian-fit FWHM of the stamp | arcsec |

Stamp size and oversampling are not in the DPDD except that `STMPSIZE` exists in the image-extension header (**[DPDD gap]**: its value, and the PSF image-extension keyword list, which the card leaves empty).

**Layers (detector layering) table (8 columns)**

| Column | Meaning | Unit / format |
|---|---|---|
| `CALIB_IMAGE` | calibrated input file name | 80A |
| `EXTNAME` | extension (detector/quadrant) name of that input | 15A |
| `EXPTIME` | exposure time | s, 1E |
| `POLYGON` | detector or quadrant spatial polygon | rad, 8D |
| `ALPHA`, `BETA` | alpha / beta solar angles | 1E |
| `SAA` | solar aspect angle | 1E |
| `MJD-OBS` | instrument sequence start | d, 1E |

Use it to rebuild exposure-time / coverage maps and to find which quad frames to re-fetch for a custom re-stack.

**Bright-star masks.** The areas around bright Gaia stars dominated by diffuse emission and diffraction spikes. Sources inside are marked in catalogue `DET_QUALITY_FLAG` (bit values 128 for the VIS mask and 256 for the NIR mask).

### 1.4 Quality parameters (XML, not in FITS)

Image: Mean, Median, StDev, Min, Max, MaskedPixelFraction, CoverageFraction. Background map: Mean, Median, StDev, Min, Max.

---

## 2. MER background subtraction (LSB-critical)

### 2.1 What the DPDD says (complete list)

1. **Two stages of background removal precede the MER mosaic**:
   - Before coaddition, the **background models computed in the VIS and NIR pipelines are subtracted** from the input frames (VIS: NoiseChisel-based map, NIR: NIR_BackgroundEstimation task; see `dpdd_vis_nir.md`). These models "are not propagated by the MER pipeline and **cannot be added again** to the MER mosaics".
   - **EXT stacked frames are already background-subtracted**; MER only rebins them to 0.1".
2. **MER then applies a second background-subtraction step** on each mosaic, "to remove any remaining background" / "any remaining residual background". The model of this second step is delivered as the `EUC_MER_BGMOD-...` file, and **has been subtracted** from the `EUC_MER_BGSUB-MOSAIC-...` image. The background-map quality parameters (mean/median/StDev/min/max) are stored.
3. Detection happens after this step; `MU_MAX` in the catalogue is "peak surface brightness above the background".

### 2.2 Algorithm parameters: **not documented in the DPDD**

The DPDD gives **no** mesh/box size, filter size, mask treatment, sigma-clipping, interpolation scheme, object masking, scale of the background model, nor the name of the software that does the MER background estimate. These sit in `MERConfigurationSet`, which is not distributed in DR1-Foundation. Neither "mesh", "BACK_SIZE" nor "filter size" appear anywhere in the input pages (only "background" in the sense above). For LSB work this has to come from the Euclid MER paper(s) and the Q1/DR1 release documentation, not from the DPDD.

### 2.3 Consequences for LSB / extended-galaxy analysis (from the above)

- The only background model you can recover from MER products is the MER-step residual map (`BGMOD`). The earlier VIS/NIR-pipeline backgrounds are gone from the mosaics.
- To control background yourself, start from the quad/calibrated frames (VIS SCI is *not* background subtracted; NIR SCI is *not* background subtracted) together with their background maps and weight/RMS/flag layers; the layering table tells you which frames cover a tile. See `dpdd_vis_nir.md`.
- Nothing in the DPDD says that large galaxies are masked during the MER background estimate, so over-subtraction around large extended objects cannot be ruled out from this document. (VIS card itself warns its NoiseChisel background "for large object ... can be not optimal".)

---

## 3. `DpdMerSegmentationMap`

- File: `EUC_MER_FINAL-SEGMAP_TILE[tile index]`. Pixel value = object id of the source owning that pixel (0 = no source: the quality parameter `NonZeroFraction` is the fraction of pixels > 0).
- **ID link**: `SEGMENTATION_MAP_ID = TILE_INDEX * 10^6 + SOURCE_DETECTION_ID` (eq. 12); this equals the catalogue column `SEGMENTATION_MAP_ID`. Sources outside the tile core area have `SEGMENTATION_MAP_ID = -1`. `TILE_INDEX = floor(SEGMENTATION_MAP_ID / 1e6)`.
- Combination of two segmentation maps (VIS detection mosaic and NIR-stack detection mosaic, produced by parallel detection and deblending). **VIS has priority**: pixels of a VIS source are never modified; where a NIR-only source overlaps a VIS source, the overlap is removed from the NIR-only source (so SHE shear measurements are not biased by NIR-only sources).
- PRIMARY header keywords listed: `BITPIX`, `NAXIS`, `NAXIS1/2`, `WCSAXES`, `CDELT1/2` (deg), `PC1_1`, `PC2_2`, `LATPOLE`, `LONPOLE`, `MJDREF`, and `NIR_OFF` = offset of the NIR-detected source IDs. **Note the WCS convention here is `CDELT` + `PC` (astropy-written), unlike the `CD`-matrix convention of the mosaics.** Data type not stated.
- Product metadata: `FilterList`, `WCS`, `ImgSpatialFootprint`, `TileIndex`, `PatchIdList`, `ObservationIdList`, `CalblockIdList` (optional), `CalblockVariantList`, `ProcessingMode`.
- Useful for LSB/extended work: reuse the segmentation footprint to mask neighbours or to replicate MER photometry. Segmented area is also what bounds the Sersic fitting box (see 5.3).

---

## 4. `DpdMerFinalCatalog`: catalogue structure and column reference

### 4.1 Files

| Element | File prefix | Rows keyed on | Columns |
|---|---|---|---|
| `DataStorage` (main) | `EUC_MER_FINAL-CAT_TILE[tile index]` | `OBJECT_ID` | 470 |
| `MorphologyCatalogStorage` | `EUC_MER_FINAL-MORPH-CAT_TILE[tile index]` | `OBJECT_ID` | 106 |
| `CutoutsCatalogStorage` | `EUC_MER_FINAL-CUTOUTS-CAT_TILE[tile index]` | `OBJECT_ID` | 25 |
| `DeepFieldPhotometryCatalogStorage` (DEEP tiles only) | `EUC_MER_FINAL-DEEP-PHOTO-CAT_TILE[tile index]` | `OBJECT_ID` | 713 |

All tables share `OBJECT_ID`. The main file also carries a `TILE_INDEX` header keyword. Format codes: K int64, J int32, I int16, E float32, D float64.

**Identifiers.**
`OBJECT_ID = sign(Dec) * ( int(RA*1e7) * 1e9 + int(|Dec|*1e7) )` (eq. 10): negative for southern sources. The same source usually gets a different `OBJECT_ID` in different data releases (the position changes slightly).

**Product-level elements**: `SpatialCoverage`, `SpectralCoverage` (filters list), `TileIndex`, `PatchIdList`, `ObservationIdList`, `CalblockIdList`, `CalblockVariantList`, `ProcessingMode`, `ReferenceObservationDateTime`, `FirstObservationDateTime`, `LastObservationDateTime`.

**Quality parameters (XML)**: ObjectCount, ObjectDensity (objects per mosaic pixel), PointLikeFraction, NirOnlyFraction, CoverageFraction, and for VIS and NIR J: Min/Max/Median flux and flux error, NoFluxFraction, SatObjectFraction.

### 4.2 Band-token patterns used in the main catalogue

`<band>` in column names takes these values in the **main** catalogue:

- Euclid: `VIS`, `Y`, `J`, `H` (NISP bands carry no instrument suffix). `NIR_STACK` (the NIR-stack detection image) exists only for `FLUX*_nFWHM_APER` and `FLAG_`.
- EXT (17 bands): `U_EXT_DECAM`, `G_EXT_DECAM`, `R_EXT_DECAM`, `I_EXT_DECAM`, `Z_EXT_DECAM`; `U_EXT_LSST`, `G_EXT_LSST`, `R_EXT_LSST`, `I_EXT_LSST`, `Z_EXT_LSST`; `U_EXT_MEGACAM`, `R_EXT_MEGACAM`; `G_EXT_JPCAM`; `I_EXT_PANSTARRS`, `Z_EXT_PANSTARRS`; `G_EXT_HSC`, `Z_EXT_HSC`.
- `<n>` = 1,2,3,4 (aperture diameter in units of the FWHM).

Rule: every `FLUX_*` has a matching `FLUXERR_*` (same suffix). All fluxes and flux errors are in **uJy**, float32. Column descriptions in the DPDD for `FLUX_SEGMENTATION`, `FLUXERR_SEGMENTATION`, `FLUX_DETECTION_TOTAL`, `FLUXERR_DETECTION_TOTAL` are **shifted by one row** in the published table (e.g. `FLUX_DETECTION_TOTAL` is described as "total flux error (Kron aperture)"). The photometry cookbook is unambiguous: `FLUX_DETECTION_TOTAL` is the Kron flux, `FLUX_SEGMENTATION` the segmented-pixel flux; the errors follow.

### 4.3 Main catalogue (`FINAL-CAT`) by group

**Identifiers, positions, provenance**

| Column | Meaning | Unit |
|---|---|---|
| `OBJECT_ID` | Euclid unique source id (formula above) | K |
| `RIGHT_ASCENSION`, `DECLINATION` | barycentre (SExtractor ALPHA_J2000 / DELTA_J2000) | deg |
| `RIGHT_ASCENSION_PSF_FITTING`, `DECLINATION_PSF_FITTING` | position from the PSF-fitting method | deg |
| `TILE_INDEX` | tile of the source | |
| `SEGMENTATION_MAP_ID` | id in the segmentation map; -1 outside tile core | |
| `VIS_DET` | 1 = detected on the VIS detection mosaic, 0 = NIR-stack only | I |
| `GAIA_ID`, `GAIA_MATCH_QUALITY` | associated Gaia source and quality of match | |
| `GAL_EBV`, `GAL_EBV_ERR` | Galactic E(B-V) at the source (Planck map) and error | mag |

**Photometry** (all uJy)

| Pattern | Meaning | Bands |
|---|---|---|
| `FLUX_DETECTION_TOTAL`, `FLUXERR_DETECTION_TOTAL` | Kron (SExtractor FLUX_AUTO-like) total flux in the detection mosaic (VIS for `VIS_DET=1`, NIR-stack for `VIS_DET=0`; the NIR-stack flux is non-physical) | detection band |
| `FLUX_SEGMENTATION`, `FLUXERR_SEGMENTATION` | flux summed in the segmented pixels (SExtractor FLUX_ISO-like) | detection band |
| `FLUX_<band>_<n>FWHM_APER`, `FLUXERR_<band>_<n>FWHM_APER` | A-PHOT circular-aperture flux, diameter n x FWHM of the worst-resolution band PSF, measured on PSF-matched images, per source (PSF varies over the FoV) | VIS, Y, J, H, NIR_STACK + 17 EXT (22 bands x 4 = 88 columns each for FLUX, FLUXERR) |
| `FWHM` | FWHM in arcsec used to size the A-PHOT apertures for that source | arcsec |
| `FLUX_<band>_TEMPLFIT`, `FLUXERR_<band>_TEMPLFIT` | T-PHOT template-fitting flux (VIS image as high-res template) | Y, J, H + 17 EXT (20) |
| `FLUX_VIS_TO_<band>_TEMPLFIT`, `FLUXERR_VIS_TO_<band>_TEMPLFIT` | T-PHOT flux of the VIS image degraded to the resolution of `<band>`; to be paired with `FLUX_<band>_TEMPLFIT` for colours | same 20 bands |
| `FLUX_VIS_PSF`, `FLUXERR_VIS_PSF` | PSF-fitting flux, VIS only | VIS |
| `FLUX_<band>_SERSIC`, `FLUXERR_<band>_SERSIC` | total flux from the single-Sersic model fit (SourceXtractor++) | VIS, Y, J, H + 17 EXT (21) |
| `FLUX_<band>_DISK_SERSIC`, `FLUXERR_<band>_DISK_SERSIC` | flux from the Disk+Sersic (two-component) fit | 21 bands |
| `SERSIC_FRACT_<band>_DISK_SERSIC`, `..._ERR` | Sersic fraction in that band for the two-component fit | 21 bands |
| `AVG_TRANS_WAVE_<band>` | average filter-transmission wavelength (Angstrom) | VIS, Y, J, H + 17 EXT (no NIR_STACK) |

**Per-band pixel flags**: `FLAG_<band>` (int32): "object flag keeping track of the flagged pixels in the `<band>` flag image" for 22 bands (VIS, Y, J, H, NIR_STACK, 17 EXT). Bit values: see 4.5.

**Detection / quality / star-galaxy / deblending**

| Column | Meaning |
|---|---|
| `DET_QUALITY_FLAG` | detection-step flag; non-zero = `MAG_STARGAL_SEP` (and by extension the Kron flux) may be corrupted; bit table in 4.5 |
| `DEBLENDED_FLAG` | object was originally blended with another |
| `PARENT_ID`, `PARENT_VISNIR` | id of the parent source of a deblended object (both with the same description in the DPDD) |
| `BLENDED_PROB` | probability of being blended with another source |
| `POINT_LIKE_FLAG` | 1 for VIS detections with `DET_QUALITY_FLAG==0` and `POINT_LIKE_PROB` above threshold, else NaN |
| `POINT_LIKE_PROB` | probability in [0,1] of being point-like (from a "star probability cube" in the MDB); NaN for NIR-only sources |
| `EXTENDED_FLAG`, `EXTENDED_PROB` | extended-source flag and probability |
| `SPURIOUS_FLAG`, `SPURIOUS_PROB` | spurious-source flag and probability |
| `MAG_STARGAL_SEP` | magnitude used to compute `POINT_LIKE_PROB` (mag) |
| `MUMAX_MINUS_MAG` | `MU_MAX - MAG_STARGAL_SEP`, valid also for NIR-only sources (use this for them) |
| `SHE_FLAG` | objects SHE may want to remove (e.g. bright stars) |
| `VARIABLE_FLAG`, `BINARY_FLAG` | variability flag, potential binary stars |

Bit assignments for `SHE_FLAG`, `VARIABLE_FLAG`, `BINARY_FLAG`, `EXTENDED_FLAG`, `SPURIOUS_FLAG`, `DEBLENDED_FLAG`, `POINT_LIKE_FLAG`, `VIS_DET` are **not documented** (treat as boolean/0-1 unless proven otherwise).

**Shape on the detection image**

| Column | Meaning | Unit |
|---|---|---|
| `MU_MAX` | peak surface brightness above the background in the detection band | mag/arcsec^2 |
| `SEGMENTATION_AREA` | isophotal area above the analysis threshold | pix |
| `SEMIMAJOR_AXIS`, `_ERR` | semi-major axis (= SExtractor A_IMAGE / SourceXtractor++ ellipse_a) | pix |
| `POSITION_ANGLE`, `_ERR` | CCW, NE-SW convention, range [-90, 90] | deg |
| `ELLIPTICITY`, `_ERR` | stretch of the object from minor/major axes | |
| `KRON_RADIUS`, `_ERR` | major semi-axis of the elliptical Kron aperture used for `FLUX_DETECTION_TOTAL` | pix |

Note: there is **no `MAG_AUTO` column** in the final catalogue (the morphology cookbook text refers to `MAG_AUTO` conceptually; the column is `MAG_STARGAL_SEP`). There is also no semi-minor-axis column in the main catalogue (it is in the cutouts table); derive from `SEMIMAJOR_AXIS` and `ELLIPTICITY`.

### 4.4 Morphology catalogue (`FINAL-MORPH-CAT`, 106 columns)

| Group | Columns | Meaning / unit |
|---|---|---|
| Size | `FLUX_RADIUS`, `_ERR` | half-light radius, SExtractor-like (pix) |
| CAS+Gini+M20 (VIS-detected sources, Conselice 2003, Lotz et al. 2004), each with `_ERR` | `CONCENTRATION` (log of ratio of circular radii enclosing 80% and 20% of total flux), `ASYMMETRY` (180-deg rotation residual), `SMOOTHNESS` (clumpiness; image smoothed with a box of width 0.25 rp then subtracted), `GINI` (Lorenz-curve inequality of pixel values), `MOMENT_20` (normalised second moment of the brightest 20% of pixels) | dimensionless |
| Single Sersic, VIS+NIR joint fit | `SERSIC_VISNIR_REDUCED_CHI2`, `_ITERATIONS`, `_FLAGS` (int64), `_DURATION` (s); `SERSIC_SERSIC_VIS_RADIUS` (arcsec), `SERSIC_SERSIC_VIS_AXIS_RATIO`, `SERSIC_SERSIC_VIS_INDEX`; same trio with `NIR` instead of `VIS`; each parameter has `_ERR`; `SERSIC_ANGLE`, `_ERR` (deg, CCW NE-SW, [-90,90]) | the radius is described only as "Sersic radius" (presumably effective radius; not stated) |
| Single Sersic, EXT fit (VIS-derived shape held fixed, fluxes only) | `SERSIC_EXT_REDUCED_CHI2`, `_ITERATIONS`, `_FLAGS`, `_DURATION` | |
| Disk+Sersic fit | `DISK_SERSIC_REDUCED_CHI2`, `_ITERATIONS`, `_FLAGS`, `_DURATION`; Sersic component: `DISK_SERSIC_SERSIC_RADIUS` (arcsec), `_AXIS_RATIO`, `_INDEX`; disk component: `DISK_SERSIC_DISK_RADIUS` (arcsec), `_DISK_AXIS_RATIO`; `DISK_SERSIC_ANGLE`; each with `_ERR` | |
| Zoobot (Galaxy-Zoo-like) Dirichlet concentrations | `BAR_{NO,STRONG,WEAK}`, `BULGE_SIZE_{DOMINANT,LARGE,MODERATE,SMALL,NONE}`, `CLUMP_COUNT_{ANY,ABOVE}_THRESHOLD`, `CLUMP_COUNT_UNUSUAL_{ANY,ABOVE}_THRESHOLD` (integer counts), `DISK_EDGE_ON_{NO,YES}`, `EDGE_ON_BULGE_{BOXY,NONE,ROUNDED}`, `LOPSIDED_{NO,YES}`, `HAS_SPIRAL_ARMS_{NO,YES}`, `HOW_ROUNDED_{CIGAR_SHAPED,COMPLETELY,IN_BETWEEN}`, `MERGING_{MAJOR_DISTURBANCE,MERGER,MINOR_DISTURBANCE,NONE}`, `SMOOTH_OR_FEATURED_{ARTIFACT_STAR_ZOOM,FEATURED_OR_DISK,SMOOTH}`, `SPIRAL_ARM_COUNT_{1,2,3,4,CANT_TELL,MORE_THAN_4}`, `SPIRAL_WINDING_{LOOSE,MEDIUM,TIGHT}`, `DWARF_{YES,NO}` (dwarf = visually a "smudge"), `PECULIAR_{YES,NO}`, `RING_{YES,NO}`, `AGN_{YES,NO}` (central PSF-like bright spot) | answer / sum over answers of the same question = expected fraction of volunteers |
| Other ML | `ETG_OR_LTG` (early vs late type), `T_TYPE` (regression), both from Dominguez Sanchez 2022; `MAJOR_MERGER` (+`_UNCERTAINTY`), `MAJOR_MERGER_STAGE` (int), `MAJOR_MERGER_STAGE_PROBABILITY`, `MAJOR_MERGER_STAGE_UNCERTAINTY` | |

Zoobot and merger columns are only filled for galaxies with VIS < 20.5 mag **or** `SEGMENTATION_AREA` > 1200 pixels (roughly 2% of MER sources).

### 4.5 Flag bit definitions (everything documented)

**`DET_QUALITY_FLAG`** (photometry cookbook; "Bit set" is 1-based, "Integer" = value to test with `&`):

| Bit set | Value | Meaning |
|---|---|---|
| 1 | 1 | contaminated by close neighbours or has bad pixels |
| 2 | 2 | blended with another source (consistent with `PARENT_ID != -1`) |
| 3 | 4 | saturated |
| 4 | 8 | close to a border |
| 5-7 | 16, 32, 64 | not documented |
| 8 | 128 | within the VIS bright-star mask |
| 9 | 256 | within the NIR bright-star mask |
| 10 | 512 | within an extended-object area |
| 11 | 1024 | skipped by the deblending algorithm because of its large pixel size |

**`FLAG_<band>`** (single-band flags; only bits 1-4, same definitions as the first four rows above: 1 contaminated/bad pixels, 2 blended, 4 saturated, 8 close to border). Note `DET_QUALITY_FLAG` carries more information than `FLAG_<band>`.

**`SERSIC_VISNIR_FLAGS`, `SERSIC_EXT_FLAGS`** (and presumably `DISK_SERSIC_FLAGS`, whose bits are not separately documented): combined SourceXtractor++ and Levmar stop-reason bits. Cookbook "Bit set" here is **0-based**:

| Bit | Value | Meaning |
|---|---|---|
| 0 | 1 | error flag (from levmar) |
| 1 | 2 | size correction (manual resizing of fitting box) |
| 2 | 4 | outside the measurement frame (no fit run) |
| 3 | 8 | insufficient data (no fit run) |
| 4 | 16 | some/all model parameters could not be fitted |
| 5 | 32 | fit done on a downsampled image (max size exceeded) |
| 6 | 64 | small gradient |
| 7 | 128 | small step |
| 8 | 256 | maximum iterations |
| 9 | 512 | singular matrix (raises error flag) |
| 10 | 1024 | no further error reduction possible |
| 11 | "2028" | small residual |
| 12 | "4056" | invalid (NaN/Inf) model values (raises error flag) |

The values "2028" and "4056" are printed exactly so in the DPDD; they are almost certainly typos for 2048 and 4096 (bits 11, 12) **[derived]**.

**Mosaic flag-image bits** (inherited from VIS / NIR / EXT) and `POINT_LIKE_FLAG` rule: see `dpdd_vis_nir.md` and 5.2.

### 4.6 Cutouts catalogue (`FINAL-CUTOUTS-CAT`, 25 columns)

`OBJECT_ID`, `RIGHT_ASCENSION`, `DECLINATION` (deg); `CORNER_{0..3}_{RA,DEC}` (corners of the source cutout: 0 lower-right, 1 lower-left, 2 upper-left, 3 upper-right); `DBL_CORNER_{0..3}_{RA,DEC}` (same for the deblending region); `SEMIMAJOR_AXIS`, `SEMIMINOR_AXIS` (deg, from "Asterism"); `POSITION_ANGLE` (deg); `PARENT_ID`, `PARENT_VISNIR`; `FLUX_DETECTION_TOTAL` (uJy; description mis-printed as an error). Note `SEMIMAJOR_AXIS` is in **deg** here but in **pixels** in the main catalogue.

### 4.7 DEEP-field photometry catalogue (`FINAL-DEEP-PHOTO-CAT`, 713 columns)

Only for DEEP tiles. `OBJECT_ID` plus the same per-band families as the main catalogue, for 36 additional EXT bands not in the main file: Subaru intermediate bands `IA427, IA445, IA464, IA484, IA505, IA527, IA550, IA574, IA598, IA624, IA651, IA679, IA709, IA738, IA767, IA797, IA827, IA856` (`_EXT_SUBARU`); `USTAR_EXT_MEGACAM`, `UPRIME_EXT_MEGACAM`; HSC `R, R2, I, I2, Y`; VISTA `H, J, Y, KS`; UKIRT `J, H, K`; IRAC `CH1, CH2`; GALEX `FUV, NUV`. Families: `FLUX[ERR]_<band>_<n>FWHM_APER`, `FLUX[ERR]_<band>_TEMPLFIT`, `FLUX[ERR]_VIS_TO_<band>_TEMPLFIT`, `FLUX[ERR]_<band>_SERSIC`, `FLUX[ERR]_<band>_DISK_SERSIC`, `SERSIC_FRACT_<band>_DISK_SERSIC[_ERR]`, `FLAG_<band>`, `AVG_TRANS_WAVE_<band>`. (Counts differ slightly from a naive 36 x 20 because a few families are absent for some bands.)

---

## 5. Cookbook recommendations (paraphrased)

### 5.1 Which flux for what

- **Reference total flux**: `FLUX_DETECTION_TOTAL` (Kron aperture on the detection mosaic; like SExtractor FLUX_AUTO). Check `DET_QUALITY_FLAG` to judge its reliability.
- `FLUX_SEGMENTATION`: flux in segmented pixels (FLUX_ISO analogue).
- `FLUX_<band>_nFWHM_APER`: fixed circular apertures (n = 1..4 FWHM of the worst-resolution band) on PSF-matched images, source by source; use for **colours**.
- `FLUX_<band>_TEMPLFIT` and `FLUX_VIS_TO_<band>_TEMPLFIT`: T-PHOT; the second exists only to form template-fitting colours.
- `FLUX_<band>_SERSIC`: single-Sersic model fluxes, also usable as total fluxes (and colours between model totals).
- `FLUX_VIS_PSF`: PSF fitting on VIS, for point sources.
- Uncertainties are in matching `FLUXERR_*` columns. All fluxes are uJy.

### 5.2 Colours

1. Aperture: `H - g = -2.5 log10( FLUX_H_nFWHM_APER / FLUX_G_EXT_DECAM_nFWHM_APER )` (same n; PSF-matched).
2. Template fitting: `H - VIS = -2.5 log10( FLUX_H_TEMPLFIT / FLUX_VIS_TO_H_TEMPLFIT )`.
3. Model fitting: `g - J = -2.5 log10( FLUX_G_..._SERSIC / FLUX_J_SERSIC )`.

### 5.3 Total fluxes in non-detection bands

- Aperture-colour scaling: `F_H,tot = FLUX_DETECTION_TOTAL * FLUX_H_nFWHM_APER / FLUX_VIS_nFWHM_APER` if `VIS_DET = 1`; with `FLUX_NIR_STACK_nFWHM_APER` in the denominator if `VIS_DET = 0`.
- Template-fitting scaling: `F_H,tot = FLUX_DETECTION_TOTAL * FLUX_H_TEMPLFIT / FLUX_VIS_TO_H_TEMPLFIT`.
- Alternatively `FLUX_<band>_TEMPLFIT` can be used directly as a total flux, "especially for EXT bands", or `FLUX_<band>_SERSIC` as a model total.

### 5.4 Magnitudes

`m_AB = -2.5 log10(flux_uJy) + 23.9` in all bands. (This is a different convention from the mosaic pixels, which use `MAGZERO`.)

### 5.5 Aperture corrections

The cookbook gives no aperture-correction recipe for the 1-4 FWHM apertures; the only route to "total" is the colour-scaling of `FLUX_DETECTION_TOTAL` above, or Sersic fluxes. (The VIS single-exposure catalogues do define `APERCORR`; see `dpdd_vis_nir.md`.)

### 5.6 Morphology caveats and star/galaxy selection

- Detection-band shape (`SEMIMAJOR_AXIS`, `POSITION_ANGLE`, `ELLIPTICITY`) is from the light distribution inside the segmentation area on the VIS or NIR-stack detection mosaic; equivalent to SExtractor A/B/THETA_IMAGE (or ellipse_a/b/theta of SourceXtractor++). **[derived]** Shapes measured inside the segmentation area are limited by the detection threshold, so they will not follow faint outskirts.
- **Sersic fitting**: SourceXtractor++ in no-detection mode (positions and fitting areas supplied by MER). Iterative: first a Sersic fit to combined VIS + NIR (Y/J/H); then, with VIS-derived shape parameters held constant, fluxes are fitted in each EXT band. Validated on COSMOS. Processing limits that matter for **large/extended galaxies**:
  - objects whose segmentation implies a fitting area above 300 x 300 px have their fitting box reduced to **50 x 50 px** (to save time on saturated stars); a modification was later introduced, based on Q1 data, to exempt large galaxies from the shrinking, with a parameter combination chosen to select them;
  - all objects deblended from one parent are fitted jointly, with at most **150 objects per group**.
  Inspect `SERSIC_*_FLAGS` (bits 1 "size correction", 32 "downsampled", 4/8 "no fit run").
- **Star/galaxy**: VIS-detected objects only. Point-like estimator uses `MU_MAX - MAG_AUTO` as a proxy of SPREAD_MODEL (catalogue columns `MUMAX_MINUS_MAG`, `MAG_STARGAL_SEP`); biased toward **high purity, low completeness**. Rule of thumb for stars: VIS AB < 17 (even if saturated) plus anything with `POINT_LIKE_PROB` > 0.96; `POINT_LIKE_FLAG` = (`POINT_LIKE_PROB` > 0.96) AND (`DET_QUALITY_FLAG` = 0). For a more complete star sample, add PHZ colour/SED information.
- Zoobot: convert Dirichlet concentrations to fractions by dividing by the sum over the answers of the question (e.g. `SMOOTH_OR_FEATURED_SMOOTH` / (smooth + featured_or_disk + artifact_star_zoom)). Only ~2% of sources have them.
- Sources flagged by `DET_QUALITY_FLAG` bit 512 (extended-object area) or bits 128/256 (bright-star masks) sit in regions where photometry is less reliable.

---

## 6. Gotchas and DPDD inconsistencies collected here

1. Mosaic units: VIS ADU/s, NIR electrons, EXT arbitrary; zero point in `MAGZERO`; whereas VIS single exposures are plain ADU (not per second) with an exposure-time term.
2. MER background algorithm parameters are absent from the DPDD; VIS/NIR backgrounds cannot be restored in MER mosaics.
3. `FLUX_SEGMENTATION` / `FLUX_DETECTION_TOTAL` (and `FLUXERR_*`) descriptions are rotated by one row in the published table.
4. `DET_QUALITY_FLAG` bits 5-7 undocumented; Sersic flag values printed as 2028 and 4056.
5. Different "bit set" indexing (1-based for detection flags, 0-based for Sersic flags).
6. Segmentation map uses CDELT/PC WCS, mosaics use CD matrix.
7. `SEMIMAJOR_AXIS` unit differs between main (pix) and cutouts (deg) tables; the `SEMIMINOR_AXIS` exists only in the cutouts table.
8. No MAG_AUTO column; no per-source Kron or Petrosian magnitude other than `FLUX_DETECTION_TOTAL`; no surface-brightness profile columns other than `MU_MAX`.
9. `PARENT_ID` and `PARENT_VISNIR` carry identical descriptions.
