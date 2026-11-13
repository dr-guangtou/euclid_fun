# Euclid DR1 DPDD: VIS calibrated quad frames and NIR calibrated frames (+ catalogues)

**How to use this note.** Reference for the single-exposure Level-2 products that feed MER: `DpdVisCalibratedQuadFrame`, `DpdVisCalibratedFrameCatalog`, `DpdNirCalibratedFrame`, `DpdNirCalibratedFrameCatalog`. Section 1 summarises what a user needs to redo background subtraction and coaddition for LSB work; sections 2 and 3 are product-by-product references; section 4 collects the flag bit tables; section 5 states which stacked frames have (no) DPDD cards. **[derived]** marks my own arithmetic; **[DPDD gap]** marks missing or inconsistent information.

**Sources** (in `~/Desktop/euclid/text/dpdd/`): `visdpd__visintro.md`, `visdpd__visindex.md`, `visdpd__dpcards__vis_calibratedquadframe.md`, `visdpd__dpcards__vis_calibratedframecatalog.md`, `download__VIS_Flags.txt` (a PDF text dump, dated 2024-04-10, itself says it may be out of date), `nirdpd__nirintro.md`, `nirdpd__nirindex.md`, `nirdpd__dpcards__nir_calibratedframe.md`, `nirdpd__dpcards__nir_calibratedframecatalog.md`; plus `missing__missing-index.md` and `sasdataproducts.md` for availability.

---

## 1. Quick answer: what you need to re-do background subtraction and coadd (LSB)

| Need | VIS (per exposure) | NIR (per exposure) |
|---|---|---|
| Science pixels, **not** background subtracted, native pixel scale, optical distortion still present | `SCI` extensions in `EUC_VIS_SWL_DET-...` | `DETxy.SCI` in the NIR science MEF |
| Background model that the pipeline estimated (so you can add it back / compare) | `EUC_VIS_SWL_BKG-...` (NoiseChisel; fallbacks NC2, HISTMODE) | `Data.BackgroundStorage` MEF (same 49-HDU layout as the science file) |
| Noise | `RMS` extension (absolute std-dev, not masked) | `DETxy.RMS` |
| Weights for SWarp-type coadd | `EUC_VIS_SWL_WGT-...` (small-scale flat/PRNU, invalid = 0) | not provided separately (use `RMS`; **[DPDD gap]**) |
| Pixel mask | `FLG` extension (`INVALID` = bit 0; see 4.1) | `DETxy.DQ` (bit table is only in an image, see 4.2) |
| Photometric scale | header `MAGZEROP`, `EXPTIME`, `GAIN`, `APERCORR`, `FLXSCALE` | header `ZPAB`, `PHOTFNU`, `PHRELDT`, `PHRELOB`, `PHRELEX`, `EXPTIME` |
| Astrometry | per-quadrant header WCS with `PV1_*`/`PV2_*` distortion polynomial (+ `CD` matrix, `CRVAL`, `CRPIX`) | per-detector header WCS with `PV` terms, `CD` matrix |
| PSF | VIS PSF FITS file (PSF part of VisPSFModel) | `PsfFITSFile` (PSF image) + `.psf` PSFEx model |

Also needed in practice: the MER **layers table** (which frames, exposure times, footprints went into each tile; see `dpdd_mer.md` §1.3) to know which quad frames to download for a tile; and the fact that the **MER mosaic cannot be un-subtracted** (VIS and NIR backgrounds were removed before MER coaddition and are not propagated).

Both VIS and NIR science images are **not** background-subtracted: this is what makes them suitable starting points for an LSB-oriented re-reduction. The VIS card warns that its NoiseChisel background for large objects "can be not optimal" (so large galaxies may have been partly absorbed into the background map; it is not stated whether objects are masked). No NoiseChisel or NIR background-estimation parameters are given in the DPDD.

DR1 production version: VIS PF 18.0 (RR2 / DR1 version; Q1 used PF 17.0). The cards describe the product at that version.

---

## 2. VIS: `DpdVisCalibratedQuadFrame`

### 2.1 What is delivered

One product per exposure with **3 FITS files** (+ a PSF file), all gzip-compressed, pixels at native scale, same size in every extension, **32-bit floating point**:

| File | Name pattern | Content |
|---|---|---|
| Calibrated exposure | `EUC_VIS_SWL_DET-[ObsId]-[Dither]-[exposure]-0000000__[YYYYMMDDThhmmss.s]Z.fits.gz` | MEF with 3 extensions per quadrant: SCI, RMS, FLG. 144 quadrants (36 CCDs x 4) -> **432 extensions** (+ primary) |
| Weight map | `EUC_VIS_SWL_WGT-[ObsId]-[Dither]-[exposure]-0000000__[YYYYMMDDThhmmss.s]Z.fits.gz` | weight per quadrant extension |
| Background map | `EUC_VIS_SWL_BKG-[ObsId]-[Dither]-[exposure]-0000000__[YYYYMMDDThhmmss.s]Z.fits.gz` | background per quadrant extension |
| PSF | (name not given) | PSF part of `VisPSFModel` |

The date in the name is the production date. An `.xml` follows each FITS file with quality metrics (see VisAnalysisResults, not distributed). `SAS` serves each of these FITS files (`sasdataproducts.md`).

`EXTNAME` convention (exposure file): `<detector id>.SCI`, `<detector id>.RMS`, `<detector id>.FLG`, with detector id per the VIS FPA ICD (EUCL-SAP-ICD-6-001), CCD numbering `1-1` ... `6-6`, quadrant `E,F,G,H`. Header keywords `DETID` (0-35), `CCDID` (e.g. `1-1`), `QUADID` (E/F/G/H), `ROEID` (1-12).

### 2.2 Units, gain, exposure time, zero point (critical)

- **Pixel unit is ADU for all products** (SCI, RMS, BKG). To get electrons multiply by `GAIN` (e-/ADU, per-extension header). `BUNIT` is in the header (DPDD says it can be "electrons" or "adu"; the text says ADU).
- **Not divided by exposure time**: the conversion given in the card is

```
m_AB   = -2.5 log10(ADU) + Zp + 2.5 log10(t_exp)
S_mJy  = 10^((23.9 - m_AB)/2.5)
```
  with `Zp` = header `MAGZEROP` and `t_exp` = header `EXPTIME`. The DPDD labels the flux `S_mJy`, but the constant 23.9 is the **micro**-Jansky zero point (AB = 23.9 - 2.5 log10(uJy)); the label is almost certainly a typo for uJy **[derived]**. (This is the same convention as the MER catalogue, 23.9 for uJy.)
- "No flux scaling is applied" to SCI; the photometric solution is only recorded in the header: `MAGZEROP` (zero point), `PHOT_ERR` (self-calibration photometric error), `PHOTIRMS` (self-calibration mag dispersion RMS), `APERCORR` (self-cal aperture correction `MAG_50pix - MAG_13pix`), `APCORRMS` (RMS of that), `FLXSCALE` (flux scaling for stacked exposure; i.e. what a stack would apply).
- **Contrast with MER mosaics**: VIS mosaics are stated to be in **ADU/sec** with `MAGZERO` (no exposure-time term), so exposure time has been divided out in the mosaic.
- Gain: `GAIN` (per extension), `GAINCORR` = ref_gain/cal_gain, read-out noise `RDNOISE`, saturation `SATLEVEL` (e-) and `SATURATE` (ADU; the VIS_Flags page quotes 192000 e- and 61935 ADU as an example).
- Exposure time: `EXPTIME` ("commanded integration time in seconds, e.g. 565", also in the primary header and BKG primary); `EXPDUR1`, `EXPDUR2` in extension headers.

### 2.3 Layers

- **SCI**: calibrated pixel data per quadrant, instrumental signatures corrected, astrometric (PV projection computed with WCSFITS using the FPA `DpdVisDistortionModel`) and photometric solutions in the header; **images are not resampled** and **not background subtracted**; pointing = centre of VIS FPA.
- **RMS**: absolute standard deviation per pixel, computed as the quadratic sum of the signal (background + objects in the science image) and the read-out noise. It is "the one to use for photometry". It is **not flagged/masked**: invalid pixels still have values.
- **FLG**: per-pixel bit flags (section 4.1). `INVALID` = flag value 1; **all odd flag values mean unusable pixel**. If more than 5% of a quadrant's pixels are cosmic-ray flagged, the whole quadrant is flagged `CR_REGION` (512), which is *not* part of `INVALID`; the card recommends manually excluding such quadrants. (The VIS_Flags page quotes the CR-per-pixel threshold as 3%: **[DPDD gap]**, 5% vs 3%.) Keyword `COSMICPC` = percentage of COSMIC-flagged pixels in the extension (since PF 15.0).
- **Weight map**: "small-scale flat" reflecting PRNU; all invalid pixels have weight 0; it is the input to SWarp for `VisStackedFrame`.
- **Background map**: computed with **NoiseChisel**; captures straylight and many features; "for large object the background calculation can be not optimal". Fallbacks when NoiseChisel crashes: type recorded in `VisAnalysisResults` as `NC1` (NoiseChisel method 1), `NC2` (method 2), `HISTMODE` (mode of the image). Per-extension keywords `BKG_MED` (CCD background median) and `BKG_MAD` (MAD) are given **in MJy/sr** (so those header values are in different units from the ADU pixels). BKG primary header carries `MAGZEROP`, `PHOT_ERR`, `PHOTIRMS`, `APERCORR`, `APCORRMS`, `EXPTIME`.

### 2.4 Header keywords (grouped)

Primary header of the exposure (selection; ~200 keys): file/structure `SIMPLE, BITPIX, NAXIS, EXTEND, FITS_DEF, FITS_VER`; identity `OBS_ID, DITHOBS, PTGID, EXPNUM, TOTEXP, FIELDID, PATCH_ID, CALBLKID, CALBLKVR`; observation `OBSMODE, OBSTYPE, IMG_CAT, IMG_T1, IMG_T2, INSTRUME, TELESCOP, SEQID, DATE-OBS, DATE-END, MJD-OBS, TIMESYS, EXPTIME, BUNIT`; pointing `RA, DEC, PA` (reconstructed), `ELAT, ELONG, POS, ALPHA, BETA, SAA` (commanded attitude and solar angles), `FOV_LAT1-4`, `FOV_LON1-4` (the DPDD labels LAT as RA and LON as Dec) ; spacecraft `POS_X/Y/Z, VEL_X/Y/Z`; instrument state `INSTRMOD, COMPALGO, COMPPARA, NOMCHAIN, VSTART, VEND, ROECFGID, RSU*, TP_STAT, CUSTATUS, CI_STAT, IDLTIME`; per-ROE/CCD temperatures `VS1T2020 ... VSCT2050`; calibration `MAGZEROP, PHOT_ERR, PHOTIRMS, APERCORR, APCORRMS, FLXSCALE, REFCAT, FPAMODEL, N_CCD`; `BIASSEC`.

Extension header (per quadrant): `XTENSION, BITPIX, NAXIS1/2, EXTNAME, DETID, CCDID, QUADID, ROEID, ROECTV, BUNIT, PRESCANX, OVRSCANX, OVRSCANY, EXPDUR1/2, CMPRTSCI, GAIN, RDNOISE, SATLEVEL, SATURATE, GAINCORR, LSFCORR` (large-scale flat corrected), bias level/noise `BIAS_LVL, BIAS_RON, BIAS_TOP/BTM/LFT/RGT` (and per-quadrant `BIASLVLE..H`, `BIASRONE..H` in the BKG file), `COSMICPC`, astrometry `WCSAXES, CTYPE1/2, CUNIT1/2, CRVAL1/2, CRPIX1/2, CD1_1..CD2_2, PV1_0..PV1_10, PV2_0..PV2_10, RADESYS, STDCRMS, NUMBRMS, AVGRESID`, pointing `RA, DEC, PA, RA_COMM, DEC_COMM, PA_COMM, PTG_RECD` (false if the pointing could not be reconstructed and the commanded one was used; then `AutomatedValidationStatus` is INVALID), plus the same photometric keywords as the primary (`MAGZEROP...`). The weight-map and BKG-map extensions repeat the geometric/astrometric keywords. BKG extensions also have `CCD_RA`, `CCD_DEC`, `BKG_MED`, `BKG_MAD`.

Quadrant pixel dimensions and VIS pixel scale are not stated in the card (only via `NAXIS1/2`, `CD`).

### 2.5 Changes by PF version (as listed)

- 14.0: product replaces `DpdVisCalibratedFrame` (now deprecated and in the missing list); flag definitions changed; noise-map contents updated; quadrants with too many CRs invalidated; PSF statistics added.
- 15.0: flag definitions changed; CR-heavy quadrants no longer invalidated; keyword `COSMICPC` added; if pointing reconstruction fails the commanded pointing is used (`PTG_RECD` false, product marked INVALID).
- 17.0: no major change (Q1).
- 18.0 (DR1): new cosmic-ray detection using a stack-based method; only flag map and weight map are updated after this detection, **not the catalogue**; NoiseChisel parameters adjusted (values not given).

---

## 3. VIS catalogue: `DpdVisCalibratedFrameCatalog`

- FITS "LDAC" catalogues from **SExtractor**, one per exposure: `EUC_VIS_SWL_CAT-[ObsId]-[Dither]-[exposure]-0000000__[YYYYMMDDThhmmss.s]Z.fits.gz`. Two tables: `LDAC_IMHEAD` (1 column, original image header and SExtractor parameters) and `LDAC_OBJECTS` (84 columns, listed below).
- Apertures: **7, 13, 26, 50 px**. `APERCORR = mean(MAG_APER_50 - MAG_APER_13)` (stored in the header); recommended magnitude: `mag = MAG_APER_13 + APERCORR`.
- Raw vs calibrated: `MAG_[...]_RAW` instrumental (no zero point), `FLUX_[...]` raw counts, `MAG_[...]` calibrated, `FLUX_[...]_CAL` calibrated **uJy**. Since PF 17.0 `MAG_AUTO` and `MAG_APER[0-3]` are calibrated; raw ones are `MAG_AUTO_RAW`, `MAG_APER_RAW[0-3]`; calibrated flux columns `FLUX_AUTO_CAL`, `FLUX_APER_CAL` (+ `FLUXERR_*_CAL`). PF 18.0: new Gaia-VIS conversion (table `BP-RP_G-VIS_GAIA_DR3_sim-obs-combined_function.fits`, MDB `SpaceSegment.Instrument.VIS.GaiaVISColorTransformation`) and new model-fitting columns.
- VisPSFModel is used to fit `SPREAD_MODEL`; the spread model is used with Gaia for the zero point and data selection.
- **User cases**: stars `abs(SPREAD_MODEL) < 0.003` (can also pick up cosmic rays; add a magnitude and `FLUX_RADIUS` cut; require `FLAGS = 0` to avoid saturated stars). Valid pixels only: `IMAFLAGS_ISO != VIS_FLAG[INVALID]`, equivalent to `IMAFLAGS_ISO % 2 == 0`.

**Columns (84 in LDAC_OBJECTS, name: unit)**
- Flags: `FLAGS`, `FLAGS_WIN`, `FLAGS_MODEL` (SExtractor flags), `IMAFLAGS_ISO` (OR of flag-map bits under the isophote; see `VisFlagMap`), `NIMAFLAGS_ISO` (number of flagged pixels).
- Star/galaxy: `SPREAD_MODEL`.
- Fluxes (counts; **not calibrated**): `FLUX_AUTO`, `FLUXERR_AUTO`, `FLUX_APER`, `FLUXERR_APER`, `FLUX_MODEL`, `FLUXERR_MODEL`. Calibrated uJy: `FLUX_AUTO_CAL`, `FLUXERR_AUTO_CAL`, `FLUX_APER_CAL`, `FLUXERR_APER_CAL`.
- Magnitudes (mag): `MAG_AUTO`, `MAGERR_AUTO`, `MAG_AUTO_RAW`, `MAG_APER`, `MAGERR_APER`, `MAG_APER_RAW`, `MAG_PSF`, `MAGERR_PSF`, `MAG_MODEL`, `MAGERR_MODEL`.
- Size: `FLUX_RADIUS` (listed unit "Count", really pixels per its description "fraction-of-light radii (pixels)"), `FWHM_IMAGE` (px), `A_WORLD`, `B_WORLD` (deg), `THETA_WORLD`, `THETA_J2000`, `AWIN_WORLD`, `BWIN_WORLD`, `THETAWIN_WORLD`, `ELLIPTICITY` (1 - B/A), `ELONGATION` (A/B).
- Positions: `NUMBER`, `X_IMAGE`, `Y_IMAGE`, `XWIN_IMAGE`, `YWIN_IMAGE`, `XPSF_IMAGE`, `YPSF_IMAGE`, `XMODEL_IMAGE`, `YMODEL_IMAGE` (pix); `X_WORLD`, `Y_WORLD`, `XWIN_WORLD`, `YWIN_WORLD`, `XPSF_WORLD`, `YPSF_WORLD`, `XMODEL_WORLD`, `YMODEL_WORLD`, `ALPHA_J2000`, `DELTA_J2000`, `ALPHAPSF_J2000`, `DELTAPSF_J2000`, `ALPHAWIN_J2000`, `DELTAWIN_J2000` (deg); error ellipses `ERRA/B/THETA_WORLD`, `ERR*PSF_WORLD`, `ERR*WIN_WORLD`, `ERRX2_WORLD`, `ERRY2_WORLD`, `ERRX2WIN_WORLD`, `ERRY2WIN_WORLD`, `ERR*WIN_IMAGE`.
- Surface brightness (mag arcsec^-2): `MU_THRESHOLD`, `MU_MAX` (brightest pixel), `MU_MAX_MODEL`, `MU_EFF_MODEL`, `MU_MEAN_MODEL`, and for Sersic R^(1/n) spheroid and exponential disk models `MU_{MAX,EFF,MEAN}_{SPHEROID,DISK}` (all "above the background").
- Model fitting (SExtractor Model): `VECTOR_MODEL`, `VECTOR_MODELERR`, `MATRIX_MODELERR`, `CHI2_MODEL`, `NITER_MODEL`, `ELLIP1MODEL_{IMAGE,WORLD}`, `ELLIP2MODEL_*`, `ELLIP1ERRMODEL_*`, `ELLIP2ERRMODEL_*`, `ELLIPCORRMODEL_*`.
- Other: `BACKGROUND` (count, background at the centroid), `SNR_WIN`, `SNR` (`FLUX_APER/FLUXERR_APER` in the 50-px aperture). Note `ERRAPSF_WORLD` and `ERRBPSF_WORLD` are listed in pixel units (inconsistent with the other `_WORLD` columns).

---

## 4. Flag bit definitions

### 4.1 VIS flag map (`FLG` extension; `IMAFLAGS_ISO`)

From the VIS_Flags page (VIS_ImageTools_M/FlagMap.py, int32 values; "Invalid" = included in `INVALID`). The page says it may be out of date; `DpdVisFlagMap` is in the missing list, so this is the best available text.

| Bit | Hex | Value | Name | Part of INVALID | Meaning |
|---|---|---|---|---|---|
| 0 | 0x00000001 | 1 | INVALID | n/a | convenience flag = OR of the flags marked X; all odd values are unusable pixels |
| 1 | 0x00000002 | 2 | HOT | X | hot pixel (master flat > 1.15; master dark > 0.01 e-/s, or whole column with >= 200 hot pixels) |
| 2 | 0x00000004 | 4 | COLD | X | unresponsive pixel (master flat < 0.85) |
| 3 | 0x00000008 | 8 | SAT | X | saturated: above the blooming threshold (`SATLEVEL`/`SATURATE` in header) |
| 4 | 0x00000010 | 16 | COSMIC | X | cosmic ray (LA Cosmic); X-rays and proton showers use the same flag |
| 5 | 0x00000020 | 32 | GHOST | X | optical ghost (reflection on the dichroic back face) |
| 6 | 0x00000040 | 64 | QUADEDGE | | near quadrant edge; pixel-size and non-linear response variations |
| 7 | 0x00000080 | 128 | BAD_COLUMN | X | part of a bad column |
| 8 | 0x00000100 | 256 | BAD_CLUSTER | X | secondary bad pixel in a cluster of neighbours of HOT/COLD |
| 9 | 0x00000200 | 512 | CR_REGION | X | region with too high a cosmic-ray per pixel ratio (threshold 3% per that page; 5% per the quad-frame card) |
| 12 | 0x00001000 | 4096 | OVRCOL | X | overflow column: neighbour in same column saturated |
| 15 | 0x00008000 | 32768 | CHARINJ | X | charge-injection line |
| 17 | 0x00020000 | 131072 | SATXTALKGHOST | X | crosstalk ghost from a saturated pixel in another quadrant of the same ROE |
| 18 | 0x00040000 | 262144 | STARSIGNAL | | pixel affected by the PSF of a Gaia star (1024x1024 broadband PSF scaled by magnitude, 2 ADU threshold; misses long diffraction spikes) |
| 21 | 0x00200000 | 2097152 | ADCMAX | X | raw value 65535 ADU |
| 22 | 0x00400000 | 4194304 | NO_DATA | X | raw value 0 (transmission error, dead quadrant/CCD/ROE) |
| 23 | 0x00800000 | 8388608 | STITCHBLOCK | | photolithographic stitch-block boundary, possibly non-nominal pixel size (documentation only, not yet used by the pipeline) |
| 24 | 0x01000000 | 16777216 | OBJECTS | | SExtractor objects check-image (any non-background signal) |

`INVALID_BITMASK` = OR of HOT, COLD, SAT, COSMIC, GHOST, BAD_COLUMN, BAD_CLUSTER, CR_REGION, OVRCOL, CHARINJ, SATXTALKGHOST, ADCMAX, NO_DATA. Inconsistency in the same page: the sample print-out lists two more flags, `SATURATEDSTAR` (bit 19, 524288) and `CTICORRECTION` (bit 20, 1048576), which are absent from the dictionary and the table above.

Important for LSB and extended objects: `STARSIGNAL` and `OBJECTS` are **not** in `INVALID`; `QUADEDGE` and `STITCHBLOCK` are not either. MER mosaic flag images OR these bits together, so after MER a "flag != 0" cut is not the same as "INVALID".

### 4.2 NIR data-quality layer (`DETxy.DQ`)

`int32` bit mask; first bit `INVALID` flags pixels not to be used (set by any task that finds a critical feature: bad pixels, cosmic-ray hits, saturated pixels). **The per-bit table exists only as an image (Fig. 19) and a wiki reference, so no bit values are available in the converted text [DPDD gap].** Per-detector keywords count flagged pixels: `NBADPIXT` (bad pixels), `NREJNL` (high-noise pixels not corrected for non-linearity), `NSATPIX` (saturated), `NDFILL` (high-noise pixels filled with dark values), `NCRPIXS` (CR pixels in single-frame rejection), `NCRPIXM` (multi-frame rejection). Cosmic-ray algorithm keywords `CRSNGALG`, `CRMULALG`. Bad-pixel/persistence/saturation calibration files: `BPIXCAL`, `SATCAL`, `NLCAL`, `PERSMAKS`, `THRESH`, `NTHRESH`, `MDARKCAL`, `FLTCORR`, `FLTCAL`.

### 4.3 SExtractor `FLAGS` in the NIR and VIS catalogues
Standard SExtractor extraction flags (integer, not tabulated in the DPDD).

---

## 5. NIR: `DpdNirCalibratedFrame`

### 5.1 Files and layout

Four referenced files (`Data.*Storage`):
1. `DataStorage`: scientific MEF, `FitsFormat` id `nir.calibratedScienceFrame` (`FITS_DEF`, `FITS_VER` = 0.4). **49 HDUs**: primary header + 3 per detector x 16 detectors. Detector id `xy` in the NISP detector assembly grid (11, 12, ..., 44). `EXTNAME` = `DETxy.SCI`, `DETxy.RMS`, `DETxy.DQ`.
2. `BackgroundStorage`: MEF with the same structure, containing the estimated background (made by the NIR_BackgroundEstimation task).
3. `PsfStorage`: `PsfModelFile` (PSFEx `.psf`) and `PsfFITSFile` (PSF image, single extension, may include wavelength and focal-plane dependence); MER uses the image. PSF estimated from all input images.
4. `PsfSingleStorage` (optional): same structure, PSF per single dither.

File-name patterns are **not given** in the NIR cards [DPDD gap]. Each file has its own `QualityParams` section (`ScienceQualityParams`, `BackgroundQualityParams`, `PsfQualityParams`, `PsfSingleQualityParams`); background statistics are quoted "in Myr/sr" (typo for MJy/sr) although the pixels are in electrons.

| HDU | Format | Unit | Content |
|---|---|---|---|
| PRIMARY | | | pointing and pipeline keywords |
| `DETxy.SCI` | float32 | electron | science data, **background not subtracted** |
| `DETxy.RMS` | float32 | electron | noise, derived from the internal variance layer (initialised by NIR_Init following eq. 12 of Kubik 2016, then updated by calibration contributions) |
| `DETxy.DQ` | int32 | | data-quality bit mask |

- **Detector size 2040 x 2040 px**: the 4-pixel border of reference pixels is removed (**[derived]** raw 2048 x 2048).
- "Pixel values are still in native units (electrons)": **not** divided by exposure time. Relative and absolute calibration factors (to micro-Jy) and AB/Vega zero points are in the header.
- Pixel scale: header `PIXSCALE` (arcsec, from MDB); value not given in the card.

### 5.2 Photometric keywords (what you need to put NIR on a flux scale)

Per-detector `SCI` header: `ZPAB` (zero point for AB mag) and `ZPABE` (error), `ZPVEGA`, `ZPVEGAE`, `PHRELDT` and `PHRELDTE` (relative-calibration correction for the detector and its uncertainty), `GAIN` ("e- to ADU conversion factor, e.g. 1.5"), `RPIX_PRC` (reference-pixel processing mode), `DARKFILL` (e-).

Primary header: `PHOTFNU` (inverse sensitivity, **micro-Jy s / e-**) and `PHOTFNUE`; `PHRELOB`/`PHRELOBE` (relative calibration for the observation), `PHRELEX`/`PHRELEXE` (relative calibration), `QPRELEX`/`QPRELEXE` (relative photometric offset among dithers: quality parameter), `CAL_VER`, `WAVE_CAL`, `WAVELEN` (central wavelength, micron), `WAVEHPBW` (half-power bandwidth, micron); `EXPTIME` (effective integration time, s), `ELAPTIME`, `READMODE`, `NR`, `NG`, `ND`, `FRTIME` (default 1.41 s).

**[DPDD gap]**: the card does not give the formula that combines these keywords (e.g. whether `ZPAB` applies to e-/s or to e-, whether `PHRELDT`/`PHRELOB` have already been applied). From the unit of `PHOTFNU` it follows that `F_uJy = PHOTFNU * (electrons / EXPTIME)` **[derived, unverified]**; check on a bright star against the NIR catalogue and MER `MAGZERO` before relying on it.

Other primary keywords: identification `OBS_ID, DITHOBS, PTGID, EXPNUM, TOTEXP, PATCH_ID, CALBLKID, CALBLKVR, FILTER` (e.g. `NIR_J`), `FWA_POS` (J, H, Y, OPEN, CLOSED), `GWA_POS`, `OBSMODE, OBSTYPE, IMG_CAT, IMG_T1, IMG_T2`, `DATE-OBS, UTC-OBS, MJD-OBS`, `RA, DEC, PA, RADESYS`; astrometric diagnostics `ASTRIOFF, ASTRIORA, ASTRIODE, ASTRDEN, ASTRREF, ASTRREFD, ASTRNREF, ASTRNM, ASTRM2R, ASTRNMF, ASTRD2R, ASTRELL, WASTRELL, ERRASTR` (true = dither should be removed), `REFCAT` (Gaia).

`SCI` extension header WCS: `CRVAL1/2, CRPIX1/2, CTYPE1/2, CUNIT1/2, CD1_1..CD2_2`, `PV1_*`, `PV2_*` (distortion; PV1_3/PV2_3 omitted), `ASTIRMS1/2` (internal astrometric RMS), `ASTRRMS1/2` (vs reference), `RADESYS`, `BUNIT`, `DET_ID`.

### 5.3 Stacking / background considerations (NIR)
- Background is estimated per frame by the NIR_BackgroundEstimation task and delivered as a separate MEF; method/parameters not documented.
- Because SCI is not background-subtracted, a user can subtract, scale, or re-estimate it. The NIR background statistics are in MJy/sr per detector in the QualityParams.
- MER's mosaicking then subtracts the NIR background models before coaddition (see `dpdd_mer.md`).

---

## 6. NIR catalogue: `DpdNirCalibratedFrameCatalog`

- FITS file linked from `Data.DataStorage`; primary header + **16 table extensions** (one per detector, named `DETxy.SCI`; the DPDD notes the table sits in these extensions).
- Extraction by NIR_Catalog_Extraction with SExtractor: three photometries: `MagAper` (fixed aperture "6 pixel size"), `MagAuto`, `MagPSF`. `MAG_APER` and friends are 5-element vectors (FITS `5E`), which is at odds with "6 pixels" aperture; aperture diameters not listed.
- Primary header: `FITS_DEF` = nir.calCatalog, `FITS_VER` 0.6, `ID_CATA`, `RA_PNT, DEC_PNT, PA_PNT, EXPTIME, TELESCOP, FILTER, INSTRUME, OBSMODE, DATE-OBS, UTC-OBS, MJD-OBS, OBS_ID, DITHOBS, PTGID, EXPNUM, TOTEXP, PHOT_CAL` (photometrically calibrated?), `DET_SIG` (detection threshold), and Gaia-comparison statistics by colour class: `NSOU_{BRI,BLU,GRE,RED}`, `MED_{BRI,BLU,GRE,RED}`, `ERR_{BRI,BLU,GRE,RED}`.
- **Columns (stated 44)**: `OBJECT_ID` (MER tool), `XWIN_IMAGE, YWIN_IMAGE` (pix), `XWIN_WORLD, YWIN_WORLD`, `ALPHA_J2000, DELTA_J2000` (deg), `MAG_APER[5], MAGERR_APER[5], FLUX_APER[5], FLUXERR_APER[5]`, `MAG_AUTO, MAGERR_AUTO, FLUX_AUTO, FLUXERR_AUTO` (flux in counts), `AWIN_WORLD, BWIN_WORLD, THETAWIN_WORLD, ERRAWIN_WORLD, ERRBWIN_WORLD, ERRTHETAWIN_WORLD`, `KRON_RADIUS` (listed unit deg; really dimensionless), `ELLIPTICITY`, `CLASS_STAR`, `SPREAD_MODEL`, `FWHM_IMAGE` (px), `FLUX_RADIUS` (listed unit "count"; really pixels), `BACKGROUND` (ADU), `THRESHOLD`, `XPSF_IMAGE, YPSF_IMAGE, XPSF_WORLD, YPSF_WORLD, ALPHAPSF_J2000, DELTAPSF_J2000, MAG_PSF, MAGERR_PSF, FLUX_PSF, FLUXERR_PSF, ERRAPSF_IMAGE, ERRBPSF_IMAGE, ERRTHETAPSF_IMAGE, CHI2_PSF`, `FLAGS` (SExtractor extraction flags).
- Quality parameters (XML): `ObjectCount`, statistics for `MagAper`, `MagAuto`, `MagPSF`, and `Bright` / `Faint` error statistics.
- Because fluxes are in counts and magnitudes are calibrated, use `MAG_*` with `PHOT_CAL = True`.

---

## 7. Stacked frames and other products: DPDD cards? (answer from `missing__missing-index.md`)

The "missing" list states these products are declared in data model DM 10.1.4 but **not documented** in DPDD v2.0 because they are not published in DR1-Foundation.

| Product | DPDD card? | Status |
|---|---|---|
| `DpdVisStackedFrame`, `DpdVisStackedFrameCatalog` | **no** | listed as missing and as "Not distributed in DR1-Foundation" in `visintro` |
| `DpdNirStackedFrame`, `DpdNirStackedFrameCatalog` | **no** | listed as missing; "Not distributed" in `nirintro` |
| EXT stacked / single-epoch frames (`DpdExtStackedFrame`, `DpdExtSingleEpochFrame`, `DpdExtDesStackedFrame`, ...) | **no** | missing |
| `DpdVisCalibratedFrame` | no (deprecated since PF 14) | missing |
| `DpdVisFlagMap` | no (the quad card still refers to it) | missing; use `download__VIS_Flags.txt` |
| `DpdVisPSFModel` (listed as `DpdPSFModel` under VIS in the missing list), `DpdVisZeroPoint` | no | not distributed; only the PSF FITS file attached to the quad frame is served |
| `DpdVisStarMask`, `DpdVisGhostCatalogue`, `DpdVisDiffractionSpikesFocus`, `DpdVisAnalysisResults` | no | missing / not distributed |
| VIS and NIR calibration products (master bias/dark/flat, large flat, CTI, BFE, gain, non-linearity, persistence, distortion, abs/rel photometric calibration, bad-pixel masks, etc.) | no | missing / not distributed |
| `DpdNirTransientCatalog`, `DpdNirGhostModel`, `DpdNirSuperFlatFrame`, `DpdNirConfigurationSet` | no | missing |

Consequences: stacking in DR1-Foundation is done by MER (mosaics), not by VIS or NIR; for LSB re-stacking use the quad frames, their weight/background/PSF files, and (for NIR) the calibrated frames; large-scale flats and master calibrations are not available.

Related: `visindex.md` and `nirindex.md` contain only tables of contents; `visintro` PF table: PF 13.0 2023-07-01 (PV phase), 14.0 2024-02-14 (survey start), 15.0 2024-05-24 (reprocessing 1), 17.0 2024-09-23 (DM 10, Q1), 18.0 2025-01-20 (RR2 / DR1).
