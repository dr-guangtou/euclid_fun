# Euclid DR1 DPDD: VMPZ-ID HEALPix maps (masks, coverage, depth, info maps), LE1 raw frames, SHE/SIM

**How to use this note.** Reference for the LE3 "VMPZ-ID" (photometric-redshift selection function, internal data) HEALPix products that describe survey footprint, masked area, depth and observing conditions, plus short notes on LE1 raw frames and on what SHE and SIM contribute to DR1. Sections 1-4 give the data model; section 5 explains how to apply the maps to a galaxy sample and the caveats for nearby/large galaxies; sections 6-7 cover LE1 and SHE/SIM. **(DPDD)** marks statements taken from the DPDD; **(inference)** marks my reading or suggested practice. Important: the DPDD pages do not give the Nside, the numeric bit definitions of the bit mask, or the survey-wide file names; those must be read from the actual files and the MER documentation.

**Source files** (in `~/Desktop/euclid/text/dpdd/`): `le3dpd__le3intro.md`, `le3dpd__le3index.md`, `le3dpd__id__idintro.md`, `le3dpd__id__idindex.md`, `le3dpd__id__vmpz-id__vmpz-idintro.md`, `le3dpd__id__vmpz-id__vmpz-idindex.md`, `le3dpd__id__vmpz-id__dpcards__vmpzid_healpix_{bitmask,coverage,depthmap,effectivecoverage,footprint,infomap}.md`, `le1dpd__le1intro.md`, `le1dpd__le1index.md`, `le1dpd__dpcards__le1_visrawframe.md`, `le1dpd__dpcards__le1_nisprawframe.md`, `shedpd__sheintro.md`, `simdpd__simintro.md`. Online: https://euclid.esac.esa.int/dr/dr1/dpdd/le3dpd/id/vmpz-id/vmpz-idindex.html

## 1. Context

- LE3 has 7 work packages; for **DR1-Foundation only the VMPZ-ID PF ("photometric redshift selection function", internal data) was run**, because it computes maps useful for data-quality assessment **(DPDD)**.
- VMPZ-ID outputs are triggered at the MER-tile level as (potentially weighted) MOC HEALPix maps ("stage 1"); a "stage 2" merges them into a HEALPix partial map or MOC map at a resolution given by the user in the parameter files. Products exist per tile and for the full survey **(DPDD)**.
- **Not produced for DR1-Foundation**: the photometric visibility mask (`VMPZIDHEALPixVisibility`, `VMPZIDMOCVisibility`) and the random catalogue (`VMPZIDRandomCatalog`) **(DPDD)**. The DPDD also names MOC/mangle variants (`VMPZIDMOC*`, `VMPZIDMangleCoverageMask`); only the six HEALPix products below have data-product cards.

## 2. The six HEALPix products

All are FITS files of a common layout (section 3). Each product is "per observed band/instrument (Euclid or EXT)" except the effective coverage, which combines all bands.

| Product (data product name) | `EXTNAME` | `WEIGHT` column holds | `WEIGHT` format | Schema |
|---|---|---|---|---|
| HEALPix Footprint Mask (`DpdHealpixFootprintMaskVMPZ`) | `FOOTPRINT_MASK` | footprint coverage; equivalent to applying weights > 0 on the coverage mask. Described as 0 or 1 "fraction of the pixel actually covered by the footprint" | E | `euc-le3-id-vmpz-HealpixFootprintMask.xsd` |
| HEALPix Coverage Mask (`DpdHealpixCoverageVMPZ`) | `COVERAGE_MASK` | value in [0,1]: footprint combined with excluded regions flagged in the bit mask and the RMS image from the MER mosaic | E | `...HealpixCoverageMask.xsd` |
| HEALPix Effective Coverage Mask (`DpdHealpixEffectiveCoverageVMPZ`) | `EFFECTIVE_COVERAGE_MASK` | [0,1] fraction of the pixel covered by the footprint and not in the bit mask, with Euclid and EXT bands combined in one mask | E | `...HealpixEffectiveCoverageMask.xsd` |
| HEALPix Bit Mask (`DpdHealpixBitMaskVMPZ`) | `BIT_MASK` | unsigned 32-bit value in [0, 2^32 - 1]: which flag(s) of the MER bit mask are set | J (uint32) | `...HealpixBitMask.xsd` |
| HEALPix Depth Map (`DpdHealpixDepthMapVMPZ`) | `DEPTH_MAP` | depth (limiting magnitude), 5 sigma, 2 arcsec diameter aperture | E | `...HealpixDepthMap.xsd` |
| HEALPix Information Maps (`DpdHealpixInfoMapVMPZ`) | `INFO_MAP` | the value of an instrumental or environmental parameter (which one is in primary keyword `INFO`) | E | `...HealpixInfoMap.xsd` |

Common metadata: custodian IDVMPZ, "Last Edited for DPDD Version 2.0", created by `VMPZ_Main` (`LE3_VMPZ_ID_Main`), consumed by `VMPZ_Visibility`; used by 2PCF-WL, PK-WL, 2PCF-GC, 3PCF-GC, PK-GC, DET-CL, PROF-CL, VMSP-ID and SWG-GC/WL/CL; proposed for the SAS: yes. Each product also has `SpatialCoverage` metadata (polygon envelope, for queries) and optional parameter objects (for example `BitMaskHealpixParams`).

## 3. File format (common to all six)

- **Primary HDU**: no data table; keywords only.
- **First extension**: a binary table, **partial-sky HEALPix**, with an explicit pixel index (`INDXSCHM = 'EXPLICIT'`): only pixels that exist in the survey are listed; absent pixels are not in the table.
- Table columns (3):

| Column | Format | Meaning |
|---|---|---|
| `PIXEL` | K (int64) | HEALPix pixel index |
| `WEIGHT` | E (float32), except bit mask J (uint32) | map value (see table above) |
| `ERROR` | E | "mask error value" (no further definition) |

- Extension header keywords: `PIXTYPE='HEALPIX'`; **`ORDERING` = 'RING' or 'NESTED'** (read from the file; both are allowed); **`COORDSYS` = 'C' (celestial), 'E' (ecliptic) or 'G' (galactic)**; `EXTNAME` as above; `NSIDE` (integer); `INDXSCHM='EXPLICIT'`. The DPDD does not fix Nside or ordering: the **Nside is set by the user parameter files and recorded in `NSIDE`**. Primary keyword `NSIDE_WK` is "Nside used for the mosaic frame to HEALPix" conversion (the working Nside before merging).
- **Primary-HDU keywords**: `DATE-OBS`, `DATE-END` (considered observations), `TELESCOP`, `INSTRUME`, `FILTER` (for example Euclid/VIS/VIS, or -1), `FILTLST` (index for a combination of filters if intersection of footprints), `TILEID` (MER tile, -1 if several tiles), `LISTID` (product ID for a MER list of tiles), `NSIDE_WK`, `BITSEL` (bit-mask selection applied, see below), `SOFTNAME`, `SOFTVERS`, `SOFTINST`; depth map adds `DEPTHEST` (depth estimator); info map adds `INFO`.
- `BITSEL`: combination of bits reported in the bit mask as **32 binary digits, each 0 or 1, most significant bit first** (string) **(DPDD, footprint card)**.
- Resolution: because Nside is not given, the pixel size is `sqrt(4*pi/(12*NSIDE^2))` radians (about 58.6/NSIDE degrees, for example about 1.7 arcmin at Nside 2048) **(general HEALPix relation; DPDD gives no value)**.
- File names are not given in the DPDD cards for these products.

## 4. Product details

### 4.1 Footprint mask and coverage masks

- **Footprint**: survey footprint of a band/instrument, reconstructed from the MER tiling (and for stage 1 from VIS/NIR pointing geometry or from external-survey image footprints). Pixel coverage fraction is recorded. `WEIGHT > 0` means covered.
- **Coverage mask**: footprint minus areas flagged by the bit mask and RMS-image criteria; the DPDD says it has "the same format as the survey footprint, but the flagged areas are set to 1", and also that `WEIGHT` is the "fraction of the pixel actually covered by the footprint (1: not observed/flagged regions)". These two statements about the meaning of 1 contradict each other (1 = fully usable versus 1 = flagged); **determine the sense empirically** (for example check that deep survey interior has the dominant value) before using it **(oddity in the DPDD)**.
- **Effective coverage**: single mask combining Euclid and external bands, fraction in [0,1] of the pixel covered and not masked. Its card contains a "FIX THIS LINE" placeholder for the header table, so keyword details are missing.

### 4.2 Bit mask

Contains a map for one or more flags from the **MER pixel-flag definition** (flag maps of MER mosaics for each band), one bit per set flag, in a partial HEALPix map. The selected bit(s) are recorded in `BITSEL`. **The numeric bit definitions are not in this card**; it points to the MER definition ("MER definition" link). So the semantic table of bits (saturated, star halo, etc.) must come from the MER documentation, not from VMPZ pages. Note: `TFORM2` is listed as 'E' in the keyword list but the column is `J` (uint32), a DPDD inconsistency; trust the column (uint32).

### 4.3 Depth map

Partial HEALPix map built from the MER noise RMS image, depth for a 2 arcsec diameter aperture:

m = -2.5 log10( RMS x snr_level x sqrt(area_aperture / area_pixel) ) + zero_point, with area_aperture = pi (diameter/2)^2 and snr_level = 5 (the DPDD writes "srn_level").

So `WEIGHT` is a 5-sigma limiting AB magnitude in a 2" aperture (point-source-like depth), per band **(DPDD formula; AB system is an assumption)**. `DEPTHEST` records the estimator.

### 4.4 Information maps (`INFO` field values)

Instrumental/environmental quantities per band; the table gives measurement, subtype (XML) / `INFO` (FITS) field, data source:

| Measurement | `INFO` value | Source |
|---|---|---|
| Tile index | `Tile` | MER tile |
| Solar aspect angle | `SAA` | MER background-subtracted mosaic |
| Alpha angle | `AA` | MER mosaic |
| Beta angle | `BA` | MER mosaic |
| Exposures | `Exposures` | MER mosaic |
| Noise (RMS) | `Noise` | MER mosaic |
| PSF FWHM | `PSF` | MER mosaic |
| Galactic extinction per band | `GalacticExtinction` | Planck E(B-V) (Scaramella et al. 2022) |
| Zodiacal light per band | `ZodiacalLight` | Scaramella et al. 2022 |
| Galaxy number density | `GalaxyNumberDensity` | CatRed catalogues |
| Photo-z weight | `GalaxyPhZWeight` | CatRed catalogues |
| PHZ70 mean / RMS / std | `GalaxyRelPhZSeventy{Mean,Rms,Std}` | CatRed catalogues |
| Star number density | `StarNumberDensity` | Gaia catalogues |
| Star FLUX_G mean / RMS / std | `StarBrightness{Mean,Rms,Std}` | Gaia catalogues |

The intro also lists other candidate inputs (airmass, atmospheric extinction, background level, exposure time) for external surveys, with several "TBD" entries; these may not appear in DR1-Foundation.

## 5. How to apply the maps to a galaxy sample

Recipe (inference unless stated; uses `healpy` and `astropy.io.fits`):

1. Open the map, read the extension header: `NSIDE`, `ORDERING`, `COORDSYS`. If `COORDSYS` is not 'C' convert your coordinates first (the MER catalogue RA/DEC are equatorial).
2. Compute each object's pixel: `healpy.ang2pix(nside, ra, dec, nest=(ORDERING=='NESTED'), lonlat=True)`.
3. Look up the pixel in the partial map: build a dict or use `np.searchsorted` on the sorted `PIXEL` array. **A pixel missing from the table means outside the footprint** (treat as not covered, not as zero value of a field such as depth).
4. For a sample mask: keep objects whose pixel has `WEIGHT > 0` (footprint) and/or above a chosen coverage threshold (coverage / effective coverage; for example require the fraction to be 1, or weight the objects by the fraction for clustering statistics). Check the sense of 1 vs 0 as noted in section 4.1.
5. For the bit mask: keep objects with `(WEIGHT & wanted_bits) == 0`, where `wanted_bits` come from the MER flag definition and from `BITSEL`. Several flags can be set in one pixel; the pixel is flagged if any bit of interest is set.
6. For depth, use the depth map to define a homogeneous-depth subsample (for example restrict to pixels deeper than a chosen limit) or to model completeness; use the `Exposures`, `PSF`, `Noise`, `GalacticExtinction`, `ZodiacalLight` info maps for systematics tests and to weight/regress the density field.
7. For a clustering/density analysis, the effective area is the sum of `WEIGHT x pixel_area` over the effective coverage map; do not use the footprint area. The random catalogue and visibility mask are **not** in DR1-Foundation, so generate randoms yourself from the effective-coverage map (and a depth or visibility model) **(inference)**.

### Caveats for nearby, large, extended galaxies (inference, reflecting how the maps are built)

- **Resolution mismatch**: the maps are coarse relative to arcsecond structures. Pixel sizes at typical Nside are arcminutes (about 1.7 arcmin at Nside 2048), so a nearby galaxy of tens of arcsec to several arcmin spans one to many pixels, and a mask flag in the pixel may come from a bright star or artefact elsewhere in the pixel rather than at the galaxy. Test with the actual `NSIDE`.
- **Partial pixel fractions**: coverage and effective-coverage pixels have fractional values; objects in partially covered pixels near star masks or tile edges may be wrongly kept or rejected. For nearby galaxies sample the map over the whole galaxy extent (several pixels), not only at its centre.
- **Bit mask built from MER flags**: MER flags include extended-object and star-halo masking; large galaxies themselves, or their bright companion stars, can fall in masked pixels. Do not blindly reject a nearby galaxy for a flag; check which bit is set and whether the flag comes from the galaxy (some pipelines flag bright extended sources) **(inference)**.
- **Depth map**: it is a 2 arcsec point-source-like limit (RMS-based, 5 sigma). For low-surface-brightness work it is not a surface-brightness limit; derive SB limits from the MER RMS map and your own aperture/binning instead. Pixel-averaging smooths out local depth variations around bright objects.
- **Masks are per band**: the effective coverage combines Euclid plus external bands, so it can remove area where an external survey is missing; for VIS-only LSB work use the VIS footprint/coverage maps instead.
- **DR1 sky is partial**: coverage consists of the DR1 tiles only; check the footprint before computing area.
- The DPDD says nothing about handling of masked areas created by the Milky Way, solar-system objects, or ghost features beyond "flag-based" masking; defer to MER and VIS documentation for the full flag set.

## 6. LE1 raw frames (what exists in DR1 and what they contain)

LE1 turns spacecraft telemetry into raw data products at the SOC; there is no corresponding OU. LE1 raw frames are uncalibrated detector data (ADU) with metadata; they are not what you use for photometry or morphology (use calibrated VIS/NISP frames and MER mosaics) **(inference)**. The HKTM LE1 product is not in DR1-Foundation but will ship with DR1 **(DPDD)**. The LE1 intro mentions that the pointing history (0.5 Hz) is preserved in LE1 products for jitter estimation (VIS PSF).

| Product | `DpdVisRawFrame` | `DpdNispRawFrame` |
|---|---|---|
| Custodian / creators | LE1 / LE1_VIS | LE1 / LE1 NISP Processor (consumers NIR, SIR, SOC AUX, QLA, IODA) |
| Schema | `euc-le1-VisRawFrame.xsd` | `euc-le1-NispRawFrame.xsd` |
| Layout | one MEF per exposure, **144 extensions (36 CCDs x 4 quadrants E, F, G, H)**, `EXTNAME` format "row.column-quadrant" (CCDs '1-1' to '6-6') | one MEF `le1.nispRawImage` per exposure, **2 extensions per detector (science `DETnn.SCI` plus chi2/data-quality `DETnn.CHI2`/`.DQ`), up to 32 for 16 detectors**; plus an HK raw file `le1.nispHkRaw` (per detector `DETxx.RAW`, `.ERR`, `.HIST`) and engineering-exposure files `le1.nispEngExposure` (`DETxx.ENG`, `DETxx.GROUPn.ENG`) |
| Pixel data | ADU, 16-bit unsigned integer | ADU 16-bit unsigned (science); chi2 layer 8-bit unsigned (1 bit for photometry: cosmic-ray flag; integer chi2 for spectroscopy) |
| Geometry | each quadrant has 51 serial pre-scan pixels and overscan (extension header example `OVRSCANX`=29, `OVRSCANY`=20; the prose says 20 over-scan pixels) | science pixels in a central window (xcorner, ycorner, xsize, ysize) = (3, 3, 2040, 2040); reference pixels around it |
| Key primary-header keywords | `EXPTIME`, `OBSMODE` (WIDE, DEEP, CALIBRATION), `OBSTYPE=IMAGE`, `IMG_CAT`, `IMG_T1/T2`, `DATE-OBS`, `MJD-OBS`, `PLAN_ID`, `PATCH_ID`, `OBS_ID`, `DITHOBS`, `PTGID`, `EXPNUM`, `RA`, `DEC`, `PA`, `SAA`, `ALPHA`, `BETA`, charge-injection `CI_*`, trap-pumping `TP_*`, LED/calibration unit keywords, `M2_POS` | `READMODE` (MultiAccum, UpTheRamp, FowlerSamples), `NR`/`NG`/`ND` (reads, groups, drops), `FRTIME` (default 1.45408 s), `EXPTIME`, `FWA_POS` (J, H, Y, OPEN, CLOSED, HOMECHECK), `GWA_POS` (RGS270, RGS000, RGS180, BGS000, OPEN), `GWA_TILT`, `OBSTYPE` (IMAGE, SPECTROIMAGE), pointing keywords |
| Extension keywords | `DETID`, `CCDID`, `QUADID`, `ROEID`, `PRESCANX`, `OVRSCANX/Y`, `EXPDUR1/2`, WCS (`CRVAL`, `CRPIX`, `CD`), `CMPRTSCI`, `ROETEMP`, `DETTEMP` | `DET_ID`, `SCEINDEX`, `SCA_ID`, WCS keywords, `BUNIT`, `RON_DET`, `GAIN_DET`, `CMPRTSCI`; chi2 layer `CMPRTX2` |

Notes: for VIS, `DATE-OBS` is the beginning of the instrument sequence, not the shutter opening; the shutter is fully open about 7.7 s after `DATE-OBS` (about 9.6 s before 2024-01-26 00:35 UTC) with about 0.1 s spread; exact event times are in the VIS HKTM product (EXTNAMEs VOGT5031, VOGT5032, VOGT5030, VOGT5009). Pixel (0,0) of NISP SCAs is at the upper left for detectors 11-14 and 21-24 and at the lower right for 31-34 and 41-44. The VIS CCDs on the right of the focal plane are rotated 180 degrees relative to the left, so quadrant orientation differs across the focal plane. A future LE1 release is announced to add spacecraft velocity (aberration), temperatures and a checksum.

## 7. SHE and SIM in DR1

- **SHE**: "No SHE products are distributed in the DR1-Foundation Data Release, but will be shipped with the DR1 data release" **(DPDD)**. So no shear catalogues or shape measurements from SHE are available in the Foundation release; morphology/shape information must come from the MER catalogue.
- **SIM**: "There is no products from OU-SIM distributed with the DR1-Foundation data release" **(DPDD)**. Simulated data (used internally for validation) are not part of the release.
- Related: the PHZ `FLAG_SOM_*_TOMOBIN`, bin IDs and weights are prepared for weak lensing but the matching shear catalogues are not in the Foundation release.
