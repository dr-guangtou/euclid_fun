# Masks, flags, coverage and exposure maps in Euclid DR1

> **Key points**
>
> - A galaxy user meets **five layers of flags**: per-pixel flags in the VIS/NIR calibrated frames, the **MER mosaic FLAG maps** (bits inherited per band, no bit-0 "INVALID" in practice), per-object `DET_QUALITY_FLAG`/`FLAG_<band>` in the catalogue, **bright-star mask polygons** (JSON), and the **VMPZ HEALPix maps** (cosmology-grade, 12.9" pixels). Only the first two and the polygons work at pixel level.
> - In a measured 2' cutout, `FLAG != 0` is useless as a mask: 52.6 % of VIS pixels carry the `OBJECTS` bit and 99.9 % of NIR-H pixels carry informational bits. Build the invalid mask from the documented component bits.
> - The VMPZ maps are **not meant for masking individual objects** (Nside 16384, effective coverage is the AND of all bands including ground data, and **nearby SGA galaxies with MAG_LEDA < 16.5 are masked on purpose**). For a target use the per-object `EFF_COV` flag only with care, otherwise check pixel-level products.
> - Exposure time and number of layers are **not** in the catalogue: get them from the per-band layer files (`EUC_MER_DETECTOR-LAYERING-*`), the MER overview FITS tables (sftp) or the EXPTIME notebook; tile-level `FILLING_FACTOR` is in the overview tables only.
> - Coverage check in practice: tile list by `fov` (not always exact), cutout of the FLAG map, layer-file exposure and number of layers, bright-star polygons within about 1-2', `FILLING_FACTOR` of the tile, and VMPZ info maps (persistence, NIR astrometric scatter, depth).

**Conventions.** Citations `(Author+26, p. N)` use the page numbers recorded in the summaries under `papers/` (first mention linked); `(DPDD)` = [dpdd_vis_nir.md](data_model/dpdd_vis_nir.md), [dpdd_masks_vmpz.md](data_model/dpdd_masks_vmpz.md), [dpdd_mer.md](data_model/dpdd_mer.md); `(TAP)` = [data_model/tap/](data_model/tap/README.md); `(verified)` = [verified_on_archive.md](data_model/verified_on_archive.md) (wins on conflicts); `(measured)` = a check run for this note on 2026-11-13 (tile 102021980 in EDF-S, containing NGC 1483, for pixel and catalogue checks; archive-wide table counts for the VMPZ tables). Companion notes: [06_catalogues_photometry_morphology.md](06_catalogues_photometry_morphology.md) (catalogue columns and flags) and [10_low_surface_brightness.md](10_low_surface_brightness.md) (sky subtraction).

---

## 1. Map of the flag and mask systems

| System | Level | Where | Bit/value definitions | Use |
|---|---|---|---|---|
| VIS `FLG` extension | pixel, per exposure quadrant | `DpdVisCalibratedQuadFrame` | documented (section 2), source page "may be out of date" | masks for re-stacking from calibrated frames |
| NIR `DQ` layer | pixel, per detector | `DpdNirCalibratedFrame` | **not in the DPDD text**; Q1 NIR paper lists them (section 3) | same |
| MER mosaic FLAG map | pixel, per band, per tile | `EUC_MER_MOSAIC-<band>-FLAG_TILE*` | inherited from VIS/NIR/EXT; measured usage in section 4 | masking cutouts of the BGSUB mosaic |
| `DET_QUALITY_FLAG`, `FLAG_<band>` | object | `dr1.mer_catalogue_*` | documented ([06](06_catalogues_photometry_morphology.md), section 7.2) | sample cleaning |
| Bright-star masks | polygon list | `EUC_MER_STAR-MASKS-<band>_TILE*.json` | polygons per Gaia star (section 6) | masking spikes, cores, blooming |
| VMPZ HEALPix maps | sky pixels (Nside 16384) | `dr1.vmpz_healpix_*` | only bit 13 (persistence) documented (section 7) | footprint, area, depth, systematics |
| Layer files, overview tables | exposure/coverage | `EUC_MER_DETECTOR-LAYERING-*`, `DR1_*_MER_public.fits` | table columns (section 8) | exposure time, layers, filling factor |

---

## 2. VIS flag map (`FLG`, also `IMAFLAGS_ISO`)

From the VIS_Flags page (`VIS_ImageTools_M/FlagMap.py`, int32); the page states that it may be out of date and `DpdVisFlagMap` is in the "missing" list, so this is the best available text ([dpdd_vis_nir.md](data_model/dpdd_vis_nir.md), section 4.1). "In INVALID" = included in the convenience flag.

| Bit | Value | Name | In INVALID | Meaning |
|---|---|---|---|---|
| 0 | 1 | INVALID | n/a | OR of the flags marked X; all odd values are unusable |
| 1 | 2 | HOT | X | hot pixel |
| 2 | 4 | COLD | X | unresponsive pixel |
| 3 | 8 | SAT | X | saturated (above the blooming threshold) |
| 4 | 16 | COSMIC | X | cosmic ray (LA Cosmic); X-rays and proton showers use it too |
| 5 | 32 | GHOST | X | optical ghost (reflection on the dichroic back face) |
| 6 | 64 | QUADEDGE | | near a quadrant edge (pixel size and non-linearity variations) |
| 7 | 128 | BAD_COLUMN | X | bad column |
| 8 | 256 | BAD_CLUSTER | X | secondary bad pixels around HOT/COLD |
| 9 | 512 | CR_REGION | X | region with too many cosmic rays (threshold 5 % per the quad-frame card, 3 % per the VIS_Flags page) |
| 12 | 4096 | OVRCOL | X | overflow column (saturated neighbour) |
| 15 | 32768 | CHARINJ | X | charge-injection line |
| 17 | 131072 | SATXTALKGHOST | X | crosstalk ghost from a saturated pixel in another quadrant of the same ROE |
| 18 | 262144 | STARSIGNAL | | pixel affected by the PSF of a Gaia star (1024 x 1024 broadband PSF scaled by magnitude, 2 ADU threshold; **misses long diffraction spikes**) |
| 21 | 2097152 | ADCMAX | X | raw value 65535 ADU |
| 22 | 4194304 | NO_DATA | X | raw value 0 (dead quadrant/CCD/ROE, transmission error) |
| 23 | 8388608 | STITCHBLOCK | | photolithographic stitch-block boundary, "documentation only, not yet used by the pipeline" |
| 24 | 16777216 | OBJECTS | | SExtractor objects check-image (any non-background signal) |

- Summing the X rows gives `INVALID_BITMASK` = 6,460,350 (derived; plus 1 for the INVALID bit itself).
- `STARSIGNAL`, `OBJECTS`, `QUADEDGE`, `STITCHBLOCK` are **not** invalid. The page also prints two flags absent from its dictionary: `SATURATEDSTAR` (bit 19, 524288) and `CTICORRECTION` (bit 20, 1048576) (DPDD). [McCracken+](papers/q1_mccracken_vis.md) (Q1) list the same bits, noting that bit 18 and bit 24 mark object pixels.
- The VIS `RMS` extension is **not masked** (invalid pixels still have values); `WGT` is zero where invalid. If more than 5 % of a quadrant is CR-flagged the whole quadrant gets `CR_REGION`, which the card recommends excluding manually. DR1 (PF 18.0) re-ran cosmic-ray detection with a stack-based method and updated the flag map and weight map but **not the VIS frame catalogue** (DPDD).
- Per-exposure VIS files are about 7 GB each and the DR1 VIS *stack* has no flag extension ([10](10_low_surface_brightness.md), sections 2 and 6).

---

## 3. NIR data-quality layer (`DETxy.DQ`)

- The DPDD says only that bit `INVALID` flags unusable pixels and that the per-bit table is an image in the original document, so **no bit values are available in the DPDD text** (DPDD gap). Per-detector header counters exist (`NBADPIXT`, `NSATPIX`, `NCRPIXS`, `NCRPIXM`, ...).
- The Q1 NIR paper (Appendix B; [q1_polenta_nir.md](papers/q1_polenta_nir.md)) tabulates the bit convention of the Q1 DPDD. It gives "bit" numbers; that the value is `2^bit` is the natural reading but is not written there. DR1 ([Polenta+26](papers/polenta.md), Table A.1, p. 17) lists the static flag names DISCONN, ZEROQE, SUPERQE, BADBASE, SAT, FLOWER, LOWQE, HOT and splits them into invalid and informational, so the DR1 naming differs slightly (SAT vs SATUR). Treat the table as Q1 convention, consistent with DR1 in the measured pattern of section 4.

| Bit | Name | Invalid? | Bit | Name | Invalid? |
|---|---|---|---|---|---|
| 0 | INVALID (convenience) | | 13 | PERSIST (persistence) | yes |
| 1 | OBMASK (on-board flags) | | 14 | PERMODFAIL (persistence calibration failed) | |
| 2 | DISCONNECTED | yes | 15 | DARKNODET (dark current not detected) | |
| 3 | ZEROQE | yes | 16 | COSMIC | yes |
| 4 | BADBASE (high/low baseline) | yes | 17 | FLATLH (flat response too low/high) | |
| 5 | LOWQE | | 18 | GHOST | yes |
| 6 | SUPERQE (QE > 110 %) | yes | 19 | SCATTER | |
| 7 | HOT | | 20 | MOVING | |
| 8 | RTN (random telegraph noise) | yes | 21 | TRANS (transients) | |
| 9 | SNOWBALL | yes | 22 | CROSSTALK | |
| 10 | SATUR | yes | 23 | FLOWER | yes |
| 11 | NLINEAR | | 24 | VIGNET | |
| 12 | NLMODFAIL | yes | | | |

- Persistence: pixels in an arc of about 1.7' radius around stars brighter than about 11 mag are flagged `PERSIST` + `INVALID`, ghosts `GHOST` + `INVALID` ([q1_polenta_nir.md](papers/q1_polenta_nir.md), p. 16; [10](10_low_surface_brightness.md), section 4). Persistence is masked, not corrected.
- **Stacked NIR frames** (`DpdNirStackedFrame`, in `dr1.observation_stack`): flag propagation is switched off, so the stack `DQ` only records zero weight; persistence and bad-pixel flags exist only in the single-dither frames ([Polenta+26](papers/polenta.md), p. 8).

---

## 4. MER mosaic FLAG maps

- **Propagation.** MER resamples every band with SWarp; the DPDD says input flags are combined with a bitwise **OR** (one flagged input pixel flags the mosaic pixel); the Q1 MER paper says the `BILINEAR_FLAGS` kernel combines flags with a bitwise **XOR** ([Romelli+26](papers/q1_romelli_mer.md), p. 5). The DR1 MER paper does not say. Bit meaning is **inherited per band**: VIS bits for the VIS mosaic, NIR DQ bits for Y/J/H, EXT bits for ground bands (EXT bit definitions are not documented in the DPDD).
- **Access.** The cutout service serves FLAG maps (and BGSUB mosaics) anonymously, but **not** RMS or BGMOD maps (HTTP 500; [verified](data_model/verified_on_archive.md)); take those as whole tiles. Table `dr1.aux_mosaic` with `stype = 'FLAG'`, joined to `dr1.mosaic_product` on `mosaic_product_oid`, gives file names (measured: 8 FLAG files for tile 102021980: VIS, NIR-Y/J/H, DECam g/r/i/z).
- **Unobserved pixels.** Mosaics are 0-filled outside the covered area ([Kuemmel+26](papers/kuemmel.md), p. 5); VMPZ treats RMS = 0 or RMS > 10,000 ADU as unobserved ([Odier+26](papers/odier.md), p. 2).

### 4.1 Measured bit usage (1' radius cutout, 1208 x 1208 px, around NGC 1483, tile 102021980)

Cutouts of the FLAG maps were taken with the cutout service and the bits counted per pixel (code not kept in the repository; single field, one tile).

| Band | Bits set (share of pixels) |
|---|---|
| VIS | 1 HOT 0.57 %, 2 COLD 0.07 %, 3 SAT 0.09 %, **4 COSMIC 14.7 %**, 6 QUADEDGE 1.7 %, 8 BAD_CLUSTER 0.17 %, 12 OVRCOL 0.02 %, 17 SATXTALKGHOST 0.03 %, 18 STARSIGNAL 0.51 %, **23 STITCHBLOCK 7.6 %**, **24 OBJECTS 52.6 %**; 38.8 % of pixels are exactly 0. **Bit 0 (INVALID) never set.** Pixels with at least one component bit of the invalid set: 15.4 % (derived with the mask of section 2) |
| NIR-H | every pixel non-zero. 1 OBMASK 16.3 %, 2 DISCONNECTED 0.2 %, 3 ZEROQE 0.34 %, 4 BADBASE 0.05 %, 5 LOWQE 0.19 %, 6 SUPERQE 0.20 %, 7 HOT 2.0 %, 10 SATUR 0.12 %, **11 NLINEAR 99.9 %**, **13 PERSIST 9.4 %**, 14 PERMODFAIL 1.3 %, **15 DARKNODET 99.7 %**, 16 COSMIC 4.9 %, 17 FLATLH 1.6 %. Bit 0 never set. Pixels with a bit of the "invalid" rows of section 3: 14.2 % (derived) |
| DECam z (EXT) | bits 0, 2, 4 only (10.6 %, 1.4 %, 17.1 %); 73.6 % zero; header `BUNIT = 'DN / pixel'`; **meaning undocumented** |

Consequences:

1. `FLAG != 0` is not a usable mask: OBJECTS (VIS) and NLINEAR/DARKNODET (NIR) are nearly everywhere. Build the mask from the invalid component bits: VIS `flag & 6460350`, NIR the "invalid" rows of section 3 (numerical mask 8,730,460, derived from the Q1 table; bit 0 excluded).
2. `INVALID` (bit 0) is not set in these mosaic maps, so one cannot test `flag & 1`.
3. `STITCHBLOCK` (bit 23) is set in DR1 mosaics for 7.6 % of the pixels, although the VIS_Flags page calls it documentation-only (discrepancy; semantics for the mosaic not known).
4. With OR propagation the share of COSMIC-flagged mosaic pixels (14.7 %) overstates the loss: the mosaic is a median of several exposures. The NIR PERSIST bit 13 is the one the VMPZ persistence map is built from (section 7.4).
5. Bits are numbered as in the single-exposure products; the pattern (bit 13 = persistence, 16 = cosmic ray) agrees with the Q1 NIR convention, but this is an inference from counts, not documentation.

---

## 5. Catalogue-level flags relevant to masking (details in [06](06_catalogues_photometry_morphology.md), section 7.2)

| Column | Bits relevant to masks |
|---|---|
| `DET_QUALITY_FLAG` | 128 = inside the VIS bright-star mask, 256 = inside the NIR bright-star mask, 512 = inside an extended-object area, 1024 = skipped by the deblender (large pixel size); 1, 2, 4, 8 = neighbours/bad pixels, blended, saturated, close to border. Bits 16, 32, 64 undocumented. Measured shares (tile 102021980): 128 in 2.0 %, 256 in 1.2 %, 512 in 5.2 % of sources |
| `FLAG_<band>` | only bits 1-4 (same meaning as the first four rows above), 22 bands |

- Bright-star-mask area in EWS tiles is 1-5 % (Galactic-latitude dependent); upper limits 2-10 % (EDF-S) and 3-15 % (EDF-N) for multi-roll deep data ([Kuemmel+26](papers/kuemmel.md), p. 6).
- Bit 512 ("extended-object area") is set for practically all entries inside a large nearby galaxy (measured, NGC 1483): see [06](06_catalogues_photometry_morphology.md), section 10. It marks a region to treat with care, not a bad detection.

---

## 6. Bright-star masks (JSON)

- **File**: `EUC_MER_STAR-MASKS-<band>_TILE<idx>_*.json` (about 2 MB for the VIS file of tile 102021980; [verified](data_model/verified_on_archive.md)); in `dr1.aux_mosaic` as `stype = 'BRIGHT_STAR_MASKS'`. Per Gaia star: RA, Dec, brightness and the mask polygon (DPDD). Key names and the polygon coordinate system were not inspected (untested).
- **What it covers.** For each Gaia star a central circle (saturated core), rectangles for the three diffraction spikes and a rectangle for the VIS blooming pattern, with sizes scaling with brightness; built per calibrated frame and unioned after projection to the mosaic; masks exist for I_E, Y_E, J_E, H_E; sources inside are flagged in `DET_QUALITY_FLAG` (bits 128 VIS, 256 NIR) ([Romelli+26](papers/q1_romelli_mer.md), p. 14; [Kuemmel+26](papers/kuemmel.md), p. 6). The area dominated by diffuse emission and spikes around bright Gaia stars is the stated target (DPDD).
- **What it does not cover.** Halo and scattered light around stars (build your own Gaia-based mask; the EXT radius relation of [Odier+26](papers/odier.md) is a guide), the VIS dichroic ghost (compact ghost about 70" from stars with G <~ 14; flagged by a flux-threshold model in the frames, not subtracted), NIR persistence arcs and internal-reflection arcs, satellite trails, cosmic rays ([10](10_low_surface_brightness.md), section 4; Odier+26 do not mention ghosts, scattered light, trails or cosmics in their mask description). The `STARSIGNAL` pixel flag (VIS) misses long diffraction spikes (DPDD). False VIS detections along diffraction spikes are possible in wide data and flagged through `DET_QUALITY_FLAG` (Kuemmel+26, p. 10).
- **EXT masks used inside VMPZ**: Gaia stars with G_RP < 14 masked by circles of radius `r*(G_RP) = -0.01972 G^3 + 0.65849 G^2 - 7.31734 G + 27.75053` (arcmin) enlarged by 20 %; bleeding trails for G_RP < 10.3 as a rectangle of half-width `r_bleed(G_RP) = 0.06158 G^4 - 1.98886 G^3 + 23.65131 G^2 - 123.78714 G + 245.65947` (units not stated, presumably arcmin), polynomial saturated at G_RP = 4 (Odier+26, pp. 3-4, Eqs. 1-2).

---

## 7. VMPZ-ID HEALPix maps

### 7.1 What exists

Only the LE3 **VMPZ-ID** pipeline ran for DR1-Foundation; the visibility mask and the random catalogue products were *not* produced ([dpdd_masks_vmpz.md](data_model/dpdd_masks_vmpz.md), section 1), although Odier+26 (p. 4) describe random catalogues per tile. Six product types ([dpdd_masks_vmpz.md](data_model/dpdd_masks_vmpz.md), section 2; [Odier+26](papers/odier.md), p. 2):

| Product | `EXTNAME` | `WEIGHT` holds | Notes |
|---|---|---|---|
| Footprint mask | `FOOTPRINT_MASK` | 1 observed, 0 not (per band) | built from MER RMS and flags; logical OR of MER pixels inside a HEALPix pixel |
| Coverage mask | `COVERAGE_MASK` | fraction in [0,1] of valid MER pixels (per band); Euclid bands also exclude bright-star polygons | **1 = fully valid** (Odier+26 text). The DPDD card contradicts itself (it also says flagged areas are 1), so use Odier+26 and check empirically |
| Effective coverage | `EFFECTIVE_COVERAGE_MASK` | fraction in [0,1], all Euclid and EXT bands combined | section 7.3; also gives the per-object flag `EFF_COV` |
| Bit mask | `BIT_MASK` | uint32: bitwise OR of the MER mosaic FLAG bits of all MER pixels in the HEALPix pixel | `BITSEL` header says which bits were selected (32 binary digits, MSB first) |
| Depth map | `DEPTH_MAP` | 5 sigma AB limit in a 2" diameter aperture: `m = -2.5 log10(RMS * 5 * sqrt(A_aper / A_pix)) + ZP` | point-source depth, **not** a surface-brightness limit |
| Information maps | `INFO_MAP` | one quantity per map, named in header keyword `INFO` | section 7.4 |

Odier+26 count 104 full-sky masks for DR1 (some redundant) built from the per-tile products.

### 7.2 File format, Nside, and archive tables

- **FITS**: primary HDU keywords only; extension 1 is a binary table with an **explicit partial-sky** index (`INDXSCHM = 'EXPLICIT'`): columns `PIXEL` (int64), `WEIGHT` (float32; uint32 for the bit mask) and `ERROR` (float32, undefined). Header keywords `PIXTYPE='HEALPIX'`, `NSIDE`, `ORDERING` (`RING` or `NESTED`), `COORDSYS` (`C`/`E`/`G`), `EXTNAME`; primary keywords include `FILTER`, `TILEID`, `BITSEL`, `NSIDE_WK` (working Nside), `DEPTHEST` (depth map), `INFO` (info map) (DPDD).
- **Nside**: the DPDD does not fix it (user parameter, recorded in `NSIDE`); Odier+26 (p. 2): **Nside = 16384, NESTED, explicit indexing, about 12.9" pixels**. Read `NSIDE`/`ORDERING`/`COORDSYS` from each file.
- **Archive tables** (measured, 2026-11-13): `dr1.vmpz_healpix_{bitmask,coverage,depthmap,footprint_mask,infomap,effective_coverage}` are **product-level file lists (26 columns: `file_path`, `file_name_list`, `tile_index_list`, `filter_name`, `version`, `release_name`, ...), not pixel tables**. The rows are **per tile**: 110,859 rows each for bitmask, coverage, depthmap and footprint (17 filters: VIS, NIR_Y/J/H, DECam g/r/i/z, HSC g/r/r2/i/i2/z, MegaCam u/r, Pan-STARRS i), 544,948 for infomap (18 distinct non-blank filter values; band-independent maps such as `HPTILE` and `HPNIRPRMS` have a blank `filter_name`), 27,390 for effective coverage (no `filter_name`). Releases: `DR1_R1` (version 1) and `DR1_R2` (version 2) for the per-band maps; effective coverage has `DR1_R2` (17,928) and `DR1_R4` (version 4; 9,462 files whose names carry `-WL` or `-CL`, meaning not documented); info maps have an extra `DR1_NIRPRMS_R3` (version 3, 8,963 files). File names look like `EUC_LE3_VMPZ-ID_HPBITMASK-<tile>_<timestamp>_0.12.fits`; info-map names carry the map type (observed: `HPBA`, `HPNOISE`, `HPTILE`, `HPPSF`, `HPNIRPRMS`). Whether the R4 effective-coverage files supersede R2 or are a different variant is **not documented**; the release notes (Archive v1.12.0, 2026-06-23) only say that multiple versions of the effective coverage are available for download. The full-sky maps of Odier+26 would have to be assembled from the per-tile files (not checked).
- **Join** (help page *Other data products*): `dr1.mosaic_product mp JOIN dr1.vmpz_healpix_bitmask v ON mp.tile_index = ANY(v.tile_index_list) AND mp.filter_name = v.filter_name WHERE mp.tile_index = <tile> AND mp.filter_name = 'VIS'` (restrict to a tile to avoid timeouts).

### 7.3 Effective coverage, footprint and what is masked on purpose

Construction (Odier+26, pp. 3-4): per band, pixels with RMS = 0 or > 10,000 ADU are unobserved; equivalent EXT bands are OR-ed into "effective bands"; the effective bands and the Euclid bands are combined with a logical **AND** (only regions observed in all bands survive); stellar polygons (central lobe and spikes) are rasterised for I_E, Y_E, J_E, H_E and circles/bleed trails for EXT stars with G_RP < 14; globular clusters and planetary nebulae (NGC/OpenNGC) are masked with their radii; **nearby galaxies of the Siena Galaxy Atlas (SGA-2020) with MAG_LEDA < 16.5 are masked with ellipses enlarged by 30 %**; the result is averaged to Nside = 16384.

- Numbers: EWS 2008.8 deg2 observed, 1642.4 deg2 (82 %) kept in the effective coverage (18.1 % lost); EDS 74.7 deg2, 81 % kept (EDF-F 13.2 to 11.8 deg2, EDF-N 28.5 to 21.1, EDF-S 33.0 to 27.9); pixels with effective coverage > 0.8 hold ~99 % of the effective area (Odier+26, pp. 6, 8). The effective area requires data in all bands, so Euclid-only users lose area where EXT is missing.
- `EFF_COV`: per-object flag in the second extension of the effective-coverage FITS file; 1 if the object **position** lies in a pixel of non-zero initial (MER-resolution) effective coverage; **ignores the object extent** (Odier+26, p. 4).
- **Caveat for this group**: because SGA galaxies with MAG_LEDA < 16.5 are masked, **bright nearby galaxies are largely excluded from the effective area by construction** (done to avoid spurious detections and shredded objects). Do not apply the effective-coverage mask or `EFF_COV` to a nearby-galaxy sample; use the footprint/coverage of the VIS band, or no VMPZ mask, and check bright-star proximity yourself (Odier+26 practical recommendations).

### 7.4 Information maps (`INFO` values) and bit meanings

Odier+26 (Table 1, p. 3) maps: `Tile` (MER tile index, int64), `SAA`, `AA`, `BA` (solar aspect, alpha and beta angles, exposure-weighted from the layer files; not per band), `Exposures` (s, per Euclid band), `Noise` (mean RMS, ADU), `PSF` (mean FWHM, arcsec; measured at bright stars only, interpolated), `Persistence` (fraction 0-1 of the pixel affected, NIR; no level information), `NIR_PRMS` (maximum RMS of NIR-stack astrometric residuals, mas, about 30" resolution), `PanStarrsArtefacts` (binary, Pan-STARRS i), `ZodiacalLight`, `GalacticExtinction` (Euclid bands, mag), `StarNumberDensity`, `StarBrightnessMean/Rms/Std` (Gaia G). The DPDD additionally lists galaxy-density and photo-z-weight maps, which may not exist in DR1.

- NIR astrometry: 0.7 % of the DR1 area has an error > 50 mas; the `NIR_PRMS` map flags it ([Aussel+26](papers/aussel.md), p. 5). Degraded Pan-STARRS regions are flagged by `PanStarrsArtefacts`.
- **Bit-mask bit meanings**: the DPDD points to the MER mosaic flag definitions and gives no table; Odier+26 states the bit meaning is in the MER data model (Kuemmel+26 does not list them). **Documented: bit 13 = persistence** (NIR PERSIST; the persistence info map is derived from it). Other bits follow the per-band MER mosaic flag convention (sections 2-4). Which bits `BITSEL` selected must be read from the header.
- Depth/PSF/noise/exposure maps are useful to quote the conditions at a target; derive surface-brightness limits from the RMS map yourself ([10](10_low_surface_brightness.md), section 5).

### 7.5 How to apply a map with healpy (snippet untested; the header values it relies on were verified, see 7.6)

```python
import numpy as np
import healpy as hp
from astropy.io import fits

with fits.open(path_to_vmpz_file) as hdul:
    header, table = hdul[1].header, hdul[1].data
nside = header["NSIDE"]
nested = header["ORDERING"].strip().upper() == "NESTED"
# DR1 files write COORDSYS = 'celestial' (verified), not the 'C' of the DPDD
assert header["COORDSYS"].strip().lower() in ("c", "celestial"), "convert RA/Dec first"

pixel_index = hp.ang2pix(nside, ra_deg, dec_deg, nest=nested, lonlat=True)
order = np.argsort(table["PIXEL"])
sorted_pixels = table["PIXEL"][order]
sorted_values = table["WEIGHT"][order]
position = np.clip(np.searchsorted(sorted_pixels, pixel_index), 0, len(sorted_pixels) - 1)
found = sorted_pixels[position] == pixel_index
value = np.where(found, sorted_values[position], np.nan)   # missing pixel = outside the footprint
# bit mask: flagged = (value.astype(np.uint32) & wanted_bits) != 0   (wanted_bits from the MER flag definition)
```

Rules: a pixel absent from the table is outside the map (not "zero depth"); for the footprint keep `WEIGHT > 0`; for a bit mask test `(WEIGHT & wanted_bits) == 0`, since several bits can be set in one pixel (DPDD, inference). Because pixels are 12.9", **sample the map over the whole extent of an extended target** (several pixels), not only at its centre; a flag in a pixel can come from a star elsewhere in that pixel ([Odier+26](papers/odier.md), p. 4: the original small masks are "smeared out" at this resolution).

---

### 7.6 Getting a DR1 footprint: what exists (verified 2026-11-13)

**There is no single survey-wide footprint, coverage or MOC file in the DR1-Foundation archive.** Every VMPZ map is
per MER tile, including the 27,390 effective-coverage files whose names carry `-WL`/`-CL` but no tile index: their
primary header still has `TILEID`. Footprint options, from exact to quick:

| Option | Resolution | Area (DR1) | Cost | How |
|---|---|---|---|---|
| VMPZ `HPFOOTPRINTMASK` per tile and band (official) | Nside 16384 (12.9"), NESTED | 0.2487 deg^2 per wide tile core (19,420 pixels, tile 102021980) | about 240 KB per file; 8 files (bands) per tile; ~9000 wide tiles | file names from `dr1.files_table` (`file_path` = `.../VMPZ_HEALPIX_FOOTPRINT_MASK/<tile>`); download with `sas-dd ... release=dr1` |
| MOC from MER tile polygons (`demo/08_dr1_footprint.py`) | order 13 (25.8") | wide 8975 tiles: **2235.4 deg^2**; deep 1368 tiles: **86.9 deg^2**; union 2273.3 deg^2 | 1 TAP query, ~20 s | `dr1.mosaic_product.stc_s` (VIS); polygons are the full 32'/17' tiles with margins, so this is an upper bound |
| MOC from the IRSA HATS partition index ([14](14_hats_lsdb_access.md)) | order 9 (6.9') | MER wide: **2095 deg^2** (1997 deg^2 keeping pixels with at least half the median source count) | one 4 MB text file | `healpix9_to_partition.txt` of the HATS catalogue; data-driven (where sources are) |
| ESASky HiPS (MOC inside) | | | | the ESA DR1 page says DR1 HiPS are in ESASky; ESASky was "temporarily unavailable" on 2026-11-13 and the CDS MocServer lists only ERO and Q1 Euclid HiPS (not checked further) |

Reference areas: EWS 2092 deg^2 observed in VIS, 1975 deg^2 VIS+NISP, ~1900 deg^2 validated
([01](01_dr1_overview.md)). Odier+26: 2008.8 deg^2 observed and 1642.4 deg^2 effective coverage (section 7.3).
The polygon and HATS MOCs are larger because edge tiles are only partly filled.

Header facts from two downloaded footprint files (tile 102021980, `DECAM_r` and `NIR_J`):
- `NSIDE = 16384`, `ORDERING = 'NESTED'`, `COORDSYS = 'celestial'` (not `'C'`), `INDXSCHM = 'EXPLICIT'`,
  `EXTNAME = 'FOOTPRINT_MASK'`, columns `PIXEL`, `WEIGHT`;
- primary header: `FILTER`, `INSTRUME`, `TILEID`, `NSIDE_WK = '16384'` (a string), and an all-zero `BITSEL`;
- `WEIGHT > 0` for 100% (DECam r) and 99.9% (NIR J) of the 19,420 pixels.

TAP pitfall: selecting the array columns `file_name_list` or `fov` (with `DISTINCT` or `LIKE`) from these tables
returns HTTP 500 ("results is null"). Use `dr1.files_table` for file names and `stc_s` for polygons.

## 8. Exposure time, number of layers and coverage fractions

### 8.1 Layer files

- `EUC_MER_DETECTOR-LAYERING-<band>_TILE*` (`stype = 'LAYERS'` in `dr1.aux_mosaic`; **VIS and NIR only**) is a table with one row per input single-epoch frame/detector or quadrant that overlaps the tile: `CALIB_IMAGE`, `EXTNAME`, `EXPTIME` (s), `POLYGON` (four RA/Dec corners; DPDD unit "rad"), `ALPHA`, `BETA`, `SAA`, `MJD-OBS` (DPDD; [Kuemmel+26](papers/kuemmel.md), p. 3). With them exposure time and number of layers `N(p) = number of polygons covering p`, `t_exp(p) = sum of t_i` can be rebuilt (Expsup 15.3.6) and the calibrated frames to re-download for a re-stack identified.
- Typical depth: most of the EWS is covered by 3 or 4 single-dither exposures ([Odier+26](papers/odier.md), p. 6). Median EWS tile exposure (Kuemmel+26, Table 5): I_E 2274 s, Y/J/H about 314 s; the VMPZ statistics are mean 2735 s and median 2421 s in I_E, about 338 and 349 s for NISP (Odier+26, Table 2); they use different statistics (tile medians versus map pixels) and are not directly comparable. Deep fields: EDF-N and EDF-S about 20-25 ks in I_E, EDF-F 4-5 ks.

### 8.2 MER overview FITS tables (`DR1_<field>_MER_public.fits`)

Tile-level metadata collected during MER validation (Expsup 15.3.1), sorted by `TILE_INDEX`, one file per field: EWS, EDF-F, EDF-N, EDF-S, COSMOS, CDFS, AEGIS, SELFCAL, F-014, ILS-WAVES-S, SSO-ECLIPTIC, EMDS-HSC-HL-3, EMDS-HSC-HL-4. Columns: `TILE_INDEX`; `RA_AVERAGE`, `DEC_AVERAGE` (mean position of detected objects, not the tile centre); `REFERENCE_TIME` (MJD, median time of all Euclid inputs); `PATCH_IDS`; **`FILLING_FACTOR`**; `MOSAIC_MASKED_FRACTION_{VIS,Y,J,H}` (= 1 - FILLING_FACTOR of that band; not available for all deep fields); `VIS_DETECTIONS`, `NIR_DETECTIONS`; `GAIA_MATCHES`; `{VIS,NIR_Y,NIR_J,NIR_H}_EXPTIME_MEAN` (s); `CREATION_DATE_YEARS`. Access: `sftp anonymous@ftp-bdt.cosmos.esa.int`, log in with an e-mail address, `cd EUC_DR1_CAL`. These are the only place where `FILLING_FACTOR` is available (not in TAP; measured/TAP check). Not downloaded here.

### 8.3 Object-specific exposure time notebook

Notebook in `github.com/esa/euclid-contributed-jupyter-notebooks` (Expsup 15.3.6): reads the BGSUB mosaic, the layer file and the MER final catalogue per tile and band (VIS, Y, J, H), builds a HEALPix coverage table (`healpix_order`, default 17, about 1.6"; nested) and writes an extended catalogue with `EXPTIME_<band>` and `NLAYER_<band>` (file `*_EXPTIME.fits`) plus optional exposure-time images on the mosaic grid and diagnostic plots. Limits: resolution set by the HEALPix order (higher orders are expensive); geometry only (defective pixels, cosmic rays, persistence not accounted for); each object takes the value of the pixel containing its **centre** (extent ignored).

### 8.4 FILLING_FACTOR and partially covered tiles

- **Definition**: fraction of the HEALPix pixels of the tile **core** area that contain detected objects, equivalent to the core-area fraction covered with VIS or NIR data (Expsup 15.3.1; [Kuemmel+26](papers/kuemmel.md), p. 5). The HEALPix order used for it is not stated. Wide-tile cores are Nside = 13 pixels, deep-tile cores Nside = 8192 ([Romelli+26](papers/q1_romelli_mer.md), pp. 3-4; Kuemmel+26, pp. 2-3).
- **Thresholds in the papers**: astrometry vs Gaia < 10 mas for `FILLING_FACTOR > 0.5` (Kuemmel+26, p. 7); 88 % of wide tiles (7803 of the released tiles, count as given in the paper) have coverage > 80 % (pp. 13, 15). Tiles with a band more than 10 % smaller than the VIS+NIR coverage: 34 (I_E), 405 (Y), 560 (J), 510 (H) (pp. 13-14); causes include solar proton showers (examples: tile 102015130, J_E with 2 instead of 4 layers; tile 102015171, Y/J/H about 50 % filled; tile 102036162, 52 % coverage at a survey border).
- **Effects in partial tiles**: zero-filled empty areas; S/N falling towards borders; Q1 CAS asymmetry biased low (fixed in DR1 by local noise); an unusually high NIR-to-VIS detection ratio signals incomplete VIS coverage (Kuemmel+26, Sect. 3.2); **SE++ Sersic fluxes that are input guesses, not fits**, and **wrong worst-PSF aperture sizes** where an EXT band covers only part of the tile ([06](06_catalogues_photometry_morphology.md), section 8).
- **Wide-like versus deep products in the EDFs**: the wide-like mosaic can be all zeros at a position inside the `fov` polygon (PGC 61126, tile 102158273); use the deep stack and always check a cutout ([verified](data_model/verified_on_archive.md)). The help page *Target appears within the mosaic footprint...* confirms that `dr1.mosaic_product.fov` is occasionally inexact.

---

## 9. Practical checklist: is my target position well covered?

1. **Tiles**: query `dr1.mosaic_product` with `INTERSECTS(CIRCLE(ra, dec, r), fov)`; separate wide (`102...`, `DATA_RELEASE`, `WIDE`), deep (`101...`, `DATA_RELEASE_DEEP`, `DEEP`) and single visits; choose the newest `creation_date` when a tile has two mosaics per band ([verified](data_model/verified_on_archive.md)). Remember the 2' tile overlap and that large targets may cross a tile edge ([06](06_catalogues_photometry_morphology.md), section 10).
2. **Does data exist at the position?** Download a cutout of each band you need (BGSUB and FLAG); check for all-zero/NaN pixels (the `fov` is not exact). A MER cone search at the position that returns sources is a second check (help page).
3. **Per-band completeness**: compare the VIS, Y, J, H (and EXT) cutouts; a band missing at the target means the catalogue photometry there is not measured (SE++ guesses). Read `FILLING_FACTOR` and `MOSAIC_MASKED_FRACTION_<band>` of the tile from the overview table (section 8.2); < 0.8 deserves a look; the < 10 mas astrometry agreement with Gaia is only quoted for `FILLING_FACTOR > 0.5`.
4. **Exposure**: read the layer file, or run the EXPTIME notebook, for exposure time and `NLAYER` at the target; compare with the EWS typical 3-4 layers; check `AA`/`BA`/`SAA` info maps if stray light is a concern.
5. **Pixel flags**: from the FLAG cutout, count the invalid component bits (sections 2-4) inside the galaxy footprint, not `FLAG != 0`; look for `PERSIST` (NIR, bit 13), `SAT`, `OVRCOL`, `SATXTALKGHOST` and ghost bits near bright stars.
6. **Bright stars**: load the `STAR-MASKS` JSON; check polygons within about 1-2' of the target, plus Gaia stars with G < 14 within about 70" (VIS ghost) and the halo of brighter ones; none of these halos are masked ([10](10_low_surface_brightness.md), section 4).
7. **Catalogue sanity**: counts of `DET_QUALITY_FLAG` bits 128/256/512 and of `SPURIOUS_PROB > 0.7` entries around the target; a cluster of spurious or `DEBLENDED_FLAG = 1` entries means a shredded galaxy or an artefact.
8. **VMPZ**: look up depth, `Noise`, `PSF` FWHM, `Persistence` and `NIR_PRMS` over the target extent (section 7.5); use the coverage/footprint of the **VIS** band, and **not** the effective coverage or `EFF_COV` for nearby bright galaxies (they are masked on purpose, section 7.3). For ground-based colours check `PanStarrsArtefacts`.
9. **Depth for LSB work**: the VMPZ depth is a 5-sigma, 2" point-source limit. Measure surface-brightness limits from the RMS map in blank apertures at your scale ([10](10_low_surface_brightness.md)).

---

## 10. Discrepancies and open items

| Topic | Statement A | Statement B | Handling |
|---|---|---|---|
| Mosaic flag combination | DPDD: bitwise OR | [Romelli+26](papers/q1_romelli_mer.md) p. 5 (Q1): XOR in `BILINEAR_FLAGS` | not resolved; the measured cutout cannot tell |
| `STITCHBLOCK` (VIS bit 23) | VIS_Flags page: documentation only, not used | measured set on 7.6 % of mosaic pixels near NGC 1483 | treat as informational; meaning in the mosaic unknown |
| `CR_REGION` threshold | quad-frame card 5 % | VIS_Flags page 3 % | both quoted |
| NIR DQ bits | DPDD: table only as an image | Q1 NIR paper Appendix B gives the table | Q1 table used, flagged as such |
| VMPZ coverage sense | DPDD card self-contradictory | Odier+26: 1 = valid | Odier+26 |
| VMPZ Nside | DPDD: user-defined | Odier+26: 16384, nested | read `NSIDE` from the file |
| VMPZ products | DPDD: random catalogue and visibility mask "not produced" | Odier+26 describe per-tile random catalogues | random catalogues not in the archive tables checked |
| EXT mosaic flag bits | not documented | measured bits 0, 2, 4 in DECam z | unknown meaning |
| Effective coverage versions | `DR1_R2` (2025) and `DR1_R4` (2026, `-WL`/`-CL`) | no documentation of the difference | check headers of the files before use |
| Exposure of the median EWS tile | Kuemmel+26 Table 5: 2274 s | Odier+26 Table 2: median 2421 s | different statistics |
