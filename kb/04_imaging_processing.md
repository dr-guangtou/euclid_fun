# From raw frames to MER mosaics (Euclid DR1-Foundation imaging)

> **Key points**
> - Imaging comes from VIS (I_E, 0.1"/px, 36 CCDs) and NISP (Y_E, J_E, H_E, 0.3"/px, 16 H2RG), observed together in a 4-dither Reference Observing Sequence (ROS); ground-based EXT bands (DECam, MegaCam, HSC, Pan-STARRS) are added at the MER stage. MER resamples everything onto a 0.1"/px tile grid.
> - Sky is subtracted **twice** before you see a `BGSUB` mosaic (per exposure in VIS/NIR, then a 256-px-mesh MER step); only the second can be undone (`BGSUB + BGMOD`). LSB details: [10_low_surface_brightness.md](10_low_surface_brightness.md).
> - Frozen pipeline versions: VIS 18.0.4, NIR 6.1.2, MER 11.3.1, EXT 0.12.9. Persistence is masked (not corrected), CTI and the VIS shutter gradient are not corrected, VIS ghosts are flagged only partly, and 3 months of VIS "ice age" data are excluded.
> - Accuracy: astrometry ~10 mas (NIR) / few mas per source (VIS); VIS relative photometry ~0.01 mag per source; MER photometry vs Gaia is limited by the PSF normalisation (I_E offset ~-0.02 mag, NIR -0.04 to -0.13 mag depending on method).
> - For extended galaxies (R_e up to a few arcsec): use `BGSUB` mosaics + MER PSF ([05_psf.md](05_psf.md)); above ~10" restore `BGMOD` or rebuild from calibrated frames.

Authoritative hands-on facts (file structure, units, zero points, archive tables) are in
[data_model/verified_on_archive.md](data_model/verified_on_archive.md); they override the papers and the DPDD.

## 1. Instruments, bands and the reference observing sequence

| Item | VIS (I_E) | NISP-P (Y_E, J_E, H_E) | Source |
|---|---|---|---|
| Detectors | 36 CCDs, 4132 x 4096 px, 12 um pixels, 4 quadrants each = 144 quadrants | 16 H2RG, 2048 x 2048 px, 0.57 deg2 FoV | [McCracken+26](papers/mccracken.md) p. 1; [Radovich+26](papers/radovich.md) p. 1 |
| Native pixel scale | 0.100" at FPA centre, varies 1.5% (0.0991-0.1007") across the FPA | ~0.3" (0.296-0.299") | McCracken+26 p. 1; [Schirmer+26a](papers/schirmer-calibration.md) p. 23 |
| Passband | single broad band (wavelength range not given in the local summaries) | Y_E 950-1212, J_E 1168-1567, H_E 1522-2021 nm | [Kubik+26](papers/kubik.md) p. 2 (NISP); VIS range not given in the local summaries |
| Median PSF FWHM (EWS) | ~0.14" (SExtractor `FWHM_IMAGE` on stars, single frames) | 0.35 / 0.35 / 0.37" (single dither, PSFEx models) | McCracken+26 p. 9; [da Silva+26](papers/dasilva.md) Table 1. The MER-mosaic values are larger (see [05_psf.md](05_psf.md)) |
| Resolution requirement | FWHM < 0.18" | r_EE50 < 0.4", r_EE80 < 0.7" | McCracken+26 p. 9; da Silva+26 p. 2 |
| Detector gaps | 4 x 9 CCD layout; gap sizes not documented in the summaries | 4 x 4 layout; gap sizes not documented in the summaries | |

Reference observing sequence ([Tereno+26](papers/tereno.md) p. 2-3; [Schirmer+26a](papers/schirmer-calibration.md) p. 4):

| Item | Value |
|---|---|
| Dithers | 4, S pattern; dither slew 70 s; minimum dither (eigenslew) 73"; **no sub-pixel dithers possible** |
| VIS exposures | 4 nominal (565-566 s commanded; effective shutter-open 560.5 s) + 2 short (95 s; effective 89.5 s) at the first two dithers. Stack depth per pixel ~2422 s (Q1 value) |
| NISP photometric exposures | per dither one each in Y_E, J_E, H_E; MACC(4,16,4), 112.0 s total, 87.2 s integration (Kubik+26 p. 2) |
| NISP spectroscopy | 574 s per dither in parallel with the VIS exposure (not used for imaging) |
| Dither duration | 996 s (first three), 1006 s (fourth); ROS 4204 s excluding slews; ~19 ROS/day |
| Common VIS + NISP FoV | 0.525 deg2; tile of the survey tessellation 0.551 deg2; mean tile overlap 14% after the stray-light-driven attitude constraints (Tereno+26 p. 4) |
| Median MER wide tile exposure | I_E 2274 s, Y_E/J_E/H_E ~314 s (Kuemmel Table 5; [Kuemmel+26](papers/kuemmel.md) p. 15) |
| Deep fields | EDF-N 11 visits, EDF-S 10, EDF-F 2; each pass is one EWS-depth visit ([Aussel+26](papers/aussel.md) p. 3) |

Because of dithering and detector gaps the number of exposures ("layers") and total exposure time vary within a tile; the
`DETECTOR-LAYERING` file and the notebook in the Explanatory Supplement (15.3.6) give them per position (Kuemmel+26 p. 3).
Depth also differs from field to field: DR1 EDF depth is only 28% (N), 22% (S), 4% (F) of the final one (Tereno+26 p. 11).

## 2. VIS processing (VIS PF 18.0.4)

Algorithms are essentially those of Q1 ([McCracken+26 Q1](papers/q1_mccracken_vis.md)); the DR1 paper adds validation
(McCracken+26 p. 1, 2).

| Step | What is done | Remaining issue |
|---|---|---|
| Pixel level | saturation/bad-pixel flags, crosstalk (corrections below 4e-5 skipped), bias, non-linearity (2-4% at high signal), cosmic rays (LACosmic, second pass on the stack in DR1), brighter-fatter correction (11 x 11 kernel), PRNU small-scale flat, gain equalisation (3.48 e-/ADU in Q1) (McCracken+26 p. 2; Q1 p. 4-8) | **CTI not corrected** (modelled loss ~3e-4, shift 2e-3 px for a bright star far from the register, Q1 p. 6) |
| BFE / non-linearity check | nominal-minus-short comparison shows no residual BFE or non-linearity; small constant offsets consistent with an uncorrected shutter effect (McCracken+26 p. 9-10) | |
| Flats | PRNU from LED flats; **large-scale flat (LSF)** from ~15 000 self-calibration stars over 76 dithers; one LSF from five visits in DR1; accuracy 0.08-0.14% per quadrant for stars (Schirmer+26a p. 10-11) | LSF is built from stars (achromatic): up to 1-1.5% stellar-vs-galaxy colour bias at the right FPA edge; ~0.4% monthly variation; 0.8% (nominal) and **4.7% (short exposures)** shutter gradient mixed into the LSF, removed only in DR2 (Schirmer+26a p. 11-12) |
| Cosmic rays | main reason for frame rejection; a quadrant with >5% CR pixels is flagged `CR_REGION` (Q1 p. 6; [dpdd_vis_nir.md](data_model/dpdd_vis_nir.md) notes a 3% vs 5% inconsistency) | |
| Ghosts | dichroic ghost modelled from in-flight data and flagged by a flux threshold into the flag map; **not subtracted**. Offset 70" from stars with G <~ 14, stronger for blue stars ([Schirmer+26b](papers/schirmer-spacecraft.md) p. 11-12) | unmasked ghosts remain in deep data and produce spurious detections (McCracken+26 p. 11) |
| Serial bleeding | bands from I_E ~ 10 stars; readout-node persistence smears along the serial direction | not fixed in DR1 (McCracken+26 p. 11) |
| Background | NoiseChisel per quadrant, **supplied as a separate `BKG` map, not subtracted from `SCI`**; the stack is built from background-subtracted exposures (McCracken+26 p. 2) | over-subtracts inside objects larger than a quadrant; slightly negative sky near sources |
| Astrometry | Gaia DR3 WCS per quadrant (PV distortion) | see section 7 |
| Photometric calibration | zero point from Gaia stars (Gaia G, BP, RP to I_E transformation, App. A); 13-px aperture with `APERCORR` = 0.0655 mag to the 50-px aperture; time-variable ZP model (two linear segments, constant after the 8 June 2024 decontamination) fitted to self-cal visits (McCracken+26 p. 2-3) | the papers describe both per-exposure Gaia ZPs (Q1) and the time model (DR1); which one is in the delivered `MAGZEROP` is not stated in the summaries |

Products (McCracken+26 p. 2-3; [dpdd_vis_nir.md](data_model/dpdd_vis_nir.md)):

- `DpdVisCalibratedQuadFrame`: 3 FITS files per exposure: `DET` (432 extensions = 144 quadrants x SCI, RMS, FLG), `WGT`, `BKG`, plus a `PSF` file (new in DR1). **Units: ADU, not divided by exposure time**; `m_AB = -2.5 log10(ADU) + MAGZEROP + 2.5 log10(EXPTIME)`. Not resampled, not background-subtracted. Size ~7 GB per frame (10_ file).
- `DpdVisStackedFrame` (`STK`, `WGT`, `PSF`): 4 long + 2 short exposures, original 0.1" pixel scale. In DR1 the background extension is gone and RMS/FLG extensions were removed (McCracken+26 p. 3). **Availability**: the DPDD summaries ([dpdd_ext_archive.md](data_model/dpdd_ext_archive.md)) list VIS and NIR stacks as "not distributed", but the verified archive shows 6367 VIS and 15 165 + 1167 NIR stacked frames in `dr1.observation_stack`, and the archive help page says stacked data are available: **trust the archive** (verified_on_archive.md; EDS help page "Images", section Stacked frames).
- `DpdVisCalibratedFrameCatalog`: single-frame SExtractor catalogues (apertures 7, 13, 26, 50 px; `MAG_MODEL` unreliable, see section 9).
- Quality: 37 875 of 42 092 frames pass DQC; the 4217 flagged ones are still delivered (McCracken+26 p. 3).
- Flag bits (Q1 p. 20): 0 INVALID, 1 HOT, 2 COLD, 3 SAT, 4 COSMIC, 5 GHOST, 7 BAD_COLUMN, 8 BAD_CLUSTER, 9 CR_REGION, 15 CHARINJ, 17 SATXTALKGHOST, 18 STARSIGNAL, 22 NO_DATA.

## 3. NIR processing (NIR PF 6.1.2)

Reference: [Polenta+26](papers/polenta.md) (DR1) and [Polenta+26 Q1](papers/q1_polenta_nir.md).

| Step | What is done | Remaining issue |
|---|---|---|
| Bad pixels | master mask: 239 878 INVALID pixels (~0.4% of the focal plane); flower pixels masked with 4 neighbours (Polenta+26 p. 2) | |
| Non-linearity | 4th-degree polynomial per pixel, recalibrated with PV-018 and F-008 data (p. 2) | |
| Flat / PRNU | filter-dependent master flats from LED B, C, D exposures; **one static set in DR1**; PRNU stability 0.26-0.36%; ~0.1-0.5% boundary haloes and compact features of unknown origin (p. 4, App. B) | large-scale flat from sources is imperfect |
| Persistence | in-flight power-law model, **5 h look-back**, masked above 2 e- (photometric) / 30 e- (spectroscopic), plus a Hough-transform streak step; flags PERSIST + INVALID; **masked, not corrected** (p. 2-3; Kubik+26 p. 11-12) | ~5% of J_E pixels masked on average, >10% in some detectors in high solar activity; model underpredicts first-exposure persistence from sources by 2.5-3.5x; self-persistence of bright galaxy cores (Kubik+26 p. 12-14) |
| 1/f noise | not removed | horizontal stripes visible after sky subtraction; DR2 (Polenta+26 p. 5, 11) |
| Background | NoiseChisel 0.16, quantile 0.3, 10 x 10 px tessellation, 3-px kernel, per detector; supplied as `BackgroundStorage`, **not subtracted from the calibrated frame** (p. 5) | per-detector estimate, no focal-plane-scale uniformity; background in persistence "high regions" up to 2% (5% in DET11/14/44) of a ~100 e- sky (Kubik+26 p. 9-10) |
| Astrometry | SCAMP vs Gaia DR3, cubic polynomial per detector and dither ([Radovich+26](papers/radovich.md) p. 2-3) | DET13/DET14 degraded by persistence masking (3% of area >30 mas) |
| Photometric calibration | step-wise inverse sensitivity tracking throughput, absolute scale from white dwarf WDJ175318.65+644502.15 (CALSPEC) (p. 8-10) | single WD, single epoch; no calibration data Nov 2023-Mar 2024; ice drift only to first order |
| Resampling for stacks | SWarp C++, Lanczos-2, weighted combination of background-subtracted dithers (p. 7) | stack DQ carries only zero weight: persistence/bad-pixel flags are lost (p. 8) |
| Catalogues | SExtractor, detection threshold lowered 5 to 2; apertures of radius 0.6, 0.9, 1.5, 2.25, 3.0" (4, 6, 10, 15, 20 px) (p. 6) | no aperture correction applied (p. 19) |

Products (Polenta+26 p. 7, 19; [dpdd_vis_nir.md](data_model/dpdd_vis_nir.md)):

- `DpdNirCalibratedFrame`: MEF with 16 detectors x (SCI, RMS, DQ) = 48 extensions + primary (`CAL` file); `BKG` file with the same layout; PSF files `CAL-PSF-I/M` (per dither, `PsfSingleStorage`) and `GLOBAL-PSF-I/M` (`PsfStorage`, from the self-cal field) ([05_psf.md](05_psf.md)). **Units: electrons** (`SCI`), background statistics quoted in MJy/sr in quality parameters.
- `DpdNirStackedFrame` (new in DR1; `STK`, `PSF-I`, `PSF-M`): one SCI HDU for the whole stack + RMS + DQ, 4 dithers per ROS; **units microJy**; background already subtracted (no `BKG`).
- DQ bits: 0 INVALID; informational DISCONN, ZEROQE, SUPERQE, BADBASE, SAT, FLOWER, LOWQE, HOT; transient PERSIST, PERMODFAIL; GHOST (bit 18) and arcs flagged as PERSIST (bit 13) per the 10_ file.
- Arcs from bright stars (internal reflections, ~3% of images) are not masked (Polenta+26 p. 11).

## 4. EXT (ground-based) data

[Corcho-Caballero+26](papers/corcho-caballero.md): ~2500 deg2, 50 292 stacked frames (42 354 wide, 7938 deep), 10 322 EWS MER tiles.

| Region | Bands | Notes |
|---|---|---|
| EWS-South (~70% of tiles) | DECam g, r, i, z (mostly DES + archival) | the only part reduced from raw data by OU-EXT; sky by SWarp, mesh 256 px |
| EWS-North (~30%) | MegaCam u, r (CFHT/MegaPipe); HSC g (WHIGS), z (WISHES); Pan-STARRS i | arrive already reduced; MegaCam sky mesh 128 px; HSC and Pan-STARRS keep native sky subtraction |
| EDF-N, EDF-F, COSMOS | HSC g, r, r2, i, i2, z (H2O/SSP) (+ DECam in EDF-F, COSMOS) | use **r2 and i2, not r and i**: HSC-r/i fail validation in most deep tiles (EDF-N r 0/127, i 0/77 valid) |
| EDF-S | DECam g, r, i, z at EWS depth | |

- Reprocessing: per-filter delta zero-point, stacks scaled to ZP = 30 (3.631 nJy/ADU), SWarp **Lanczos-3** resampling to the MER tile grid at the **native pixel scale of each survey**, weighted mean, no pixel rejection, flags propagated by OR (Corcho-Caballero+26 p. 5). MER then rebins them to 0.1"/px with a bilinear kernel (Romelli+26 p. 5; [Romelli+26 Q1 MER](papers/q1_romelli_mer.md)).
- Depth (EWS, 10 sigma, 2" aperture, background-only noise): g/r/i/z = 24.8/24.3/24.0/23.0; 78%/96%/98%/20% of northern tiles meet the requirement; tile-to-tile scatter 0.1-0.3 mag (p. 6-7). Deep fields are 1-2 mag deeper (EDF-S is at EWS depth).
- Photometric stability: >95% of EWS-South stacks within 10 mmag; north 55-85% with 20-30 mmag tails (MegaCam-r, HSC-g, HSC-z) (p. 9).
- **No PSF homogenisation** in EXT: each band keeps its seeing; only per-band PSF models are co-added at source positions (p. 6, 14). The MER aperture photometry matches PSFs per object to the worst band (`FWHM` column, usually an EXT band) ([Kuemmel+26](papers/kuemmel.md) p. 4). Explanatory Supplement 15.3.4: in a few partially covered tiles the worst PSF was wrongly assigned from a band absent at the source position (more noise in the aperture fluxes).
- DR1 caveats: (i) **Pan-STARRS** stacks have artefacts not in the input masks (SGS flag-handling error), a bad-calibration patch was removed, and a VMPZ-ID information map flags affected areas (p. 13; Explanatory Supplement 15.2.4; [Odier+26](papers/odier.md)); (ii) a DECam stripe at RA ~ 5 deg is invalid (software bug) and tiles crossing RA = 0 h are not processed ([Tereno+26](papers/tereno.md) p. 9-10); (iii) only background RMS is propagated: **no Poisson noise of sources**, so chi2 fits on bright galaxies underestimate errors (p. 14); (iv) passband effective-wavelength variations not corrected; (v) tiles with |offset| > 50 mmag or > 3 NMAD are flagged (1-1.5% EWS; up to 20% deep) (p. 12); (vi) SExtractor-style sky mesh (128-256 px = 13-26") is smaller than large galaxies, so outskirts can be over-subtracted (not tested in the paper).
- Ground-based pixels exist in DR1 only as MER mosaics (already sky-subtracted, 0.1"/px), never as individual frames ([dpdd_ext_archive.md](data_model/dpdd_ext_archive.md)).

## 5. MER: tiles, mosaics, detection, photometry

Details: [Kuemmel+26](papers/kuemmel.md) (DR1 changes) and [Romelli+26](papers/q1_romelli_mer.md) (Q1 base).

**Tiling.** Wide tiles are 32' x 32' (19 200 x 19 200 px at 0.1"), centres 30' apart (2' overlap), prefix `102`; **deep tiles** (new) 17' x 17' (~10 200 px), centres 15' apart, prefix `101`; special-object tiles (`1025...`, galaxies > 2', 164 526 objects) were defined but **not processed in DR1** (Kuemmel+26 p. 2-3). Q1 enlarged ("breathing") wide tiles around large galaxies; the example is tile 102158273 with PGC 61126 (Romelli+26 p. 5), whose wide mosaic is nevertheless all zeros at the target in DR1 (verified_on_archive.md). Families of mosaics in `dr1.mosaic_product`: wide (8975 VIS tiles), deep stacks (EDFs), and single wide-depth visits of the deep fields; pick the most recent file if two exist (verified_on_archive.md).

**Mosaicking.** All VIS (nominal + short) and NIR calibrated frames of a tile, **after subtracting their own per-exposure backgrounds**, are co-added with `CT_SWarp`: **BILINEAR** resampling, **MEDIAN** combine, RMS-based weights (Romelli+26 p. 5; confirmed `COMBINET = MEDIAN`, `SOFTNAME = CT_SWarp` in the DR1 headers). Consequences: ~15% extra PSF broadening versus Lanczos-3, correlated noise between pixels, a co-add zero point equal to the median input ZP rounded to 0.1 (Romelli+26 p. 5, 8). Flags are combined with OR (DPDD) although the Q1 paper mentions XOR in a new bilinear-flags kernel (Romelli+26 p. 5): check the flag map near your target.

**Background (brief).** After mosaicking, one source-masked pass (256 x 256 px cells, 2-sigma clipping, mode or mean, 3-cell median filter, spline) is subtracted and stored as `BGMOD`; no local sky subtraction is applied in the photometry (Romelli+26 p. 5-9). The DR1 MER paper does not repeat this; assume it is unchanged. Full discussion and recipes: [10_low_surface_brightness.md](10_low_surface_brightness.md).

**Detection and deblending.** SExtractor++ independently on the VIS mosaic and on a Y+J+H stack; Gaussian segmentation filter FWHM 2.4 px (VIS) / 5.0 px (NIR), per-pixel S/N threshold 0.9 / 0.4, minimum area 10 px, core threshold 1.3 / 0.55 (core area 10 px); same parameters for wide and deep. ASTErIsM-based deblending (DBSCAN + modified DENCLUE) run separately in VIS and NIR, then merged with VIS objects taking priority (Kuemmel+26 p. 4; Romelli+26 p. 6-8). Known: over-deblending in wide, under-deblending in deep; large nearby galaxies are shredded (NGC 1483 example in verified_on_archive.md); `SPURIOUS_PROB` > 0.7 recommended (Kuemmel+26 p. 6).

**Photometry and morphology (brief).** Kron total flux in the detection band (`FLUX_DETECTION_TOTAL`), PSF-matched aperture fluxes (A-PHOT, 1-4 x FWHM of the worst PSF), template fitting (T-PHOT), VIS-only PSF fitting, and 2-D single-Sersic fits in all bands (SE++ 1.0.2, n_max raised from 5.5 to 8.0); CAS (noise now measured locally), `FLUX_RADIUS` (new), Zoobot (IE < 21 or segmentation area > 700 px) (Kuemmel+26 p. 4-6). The bulge+disc ("disk_sersic") columns exist but are empty in DR1 (verified_on_archive.md). Column-level guide: [06_catalogues_photometry_morphology.md](06_catalogues_photometry_morphology.md). Release-note bugs to be aware of (Explanatory Supplement 15.3): T-PHOT/PSF-fitting bugs (wrong re-centring direction; row/column inversion in the PSF homogenisation), `FLUX_RADIUS` limited to the segmentation area in DR1, Sersic outputs equal to the input guess in tiles with missing band coverage (a cleaning script is provided), duplicate sources at tile borders (~1e-5).

**PSF propagation.** Input VIS/NIR/EXT PSFs are propagated to the mosaic grid by running SWarp on zero images with PSF stamps injected at source positions; DR1 stamps are **not renormalised** (S ~ 0.96 in I_E, ~0.985 in NIR). Full treatment: [05_psf.md](05_psf.md).

## 6. Spacecraft and calibration effects on image quality

Source: [Schirmer+26b](papers/schirmer-spacecraft.md) unless stated.

| Effect | Size | Treatment in DR1 |
|---|---|---|
| Solar stray light in VIS | 10-15% of the zodiacal level after the azimuth-angle fix; 3-12 x 10^-3 e-/s per quadrant group; grows ~14%/yr; depends on SAA/AA and quadrant group (C, D worst) (p. 4-6) | only part of the nominal background |
| Zodiacal light | ~0.09-0.15 MJy/sr near the NEP (Fig. 20); models need scale factors 1.13-1.20 (p. 18-19) | smooth, subtracted with the sky |
| Out-of-field stray light | pre-launch predictions overestimated 4 (H_E) to 27 (I_E) times (p. 18) | none |
| **Ice contamination of VIS (FoM3)** | throughput loss up to 0.6 mag with a strong FPA gradient between the 14 Mar and 8 Jun 2024 decontaminations; VIS data of 23 Mar-7 Jun 2024 declared invalid (Tereno+26 p. 8-9); ~300 deg2 lost (p. 28), 838 tiles re-observed | **excluded from DR1**; the dates differ slightly between papers (heating start versus end) |
| VIS throughput drift since June 2024 | ~0.2 mmag/month (red 0.5%, blue 1.0% in 2.5 yr) (p. 13, 26) | time-dependent ZP |
| NISP ice | ~10 nm/month; QE fringes, strongest in Y_E (uncalibrated at DR2 peak: Y_E 0.08-0.12 mag, J_E 0.03-0.06, H_E 0.01-0.03) (Schirmer+26a p. 13-14) | monthly relative calibration only to first order |
| Defocus / PSF | defocus 0.32-0.56 um, follows SAA with 21-46 h response; step response t90 ~66-85 h (p. 7-9) | PSF may be less representative after a large attitude change |
| Jitter and shutter kick | RPE sigma 8.4/4.7 mas; shutter kick up to 12 mas (p. 20-21) | negligible |
| VIS shutter | 2.74 s motion; 4 s exposure-time difference across the FPA; 0.8% (nominal) and 4.7% (short) zero-point gradient (Schirmer+26a p. 11-12) | **not corrected** (DR2) |
| Dichroic ghost, serial bleeding, NISP arcs | see sections 2 and 3 | flagged only |
| Solar X-ray patterns, meteoroid hits | X-ray patterns in ~2% of data; strongest meteoroid impact doubled sources by 1.3" and deposited ~15 000 e-/px in NISP (p. 6, 24-25) | affected exposures flagged invalid |

## 7. Astrometric accuracy

| Quantity | Value | Source |
|---|---|---|
| VIS vs Gaia, per source (18.5 < I_E < 19.8) | internal/external dispersion 3.4/5.6 mas; quadrant mean residual RMS 0.41 mas; <3 mas mean residual for 99.8% of frames | McCracken+26 p. 5 |
| VIS distortion | 4' requirement met (RMS gradient 7e-7 vs 3e-5), but edge ellipticity between adjacent quadrant fits exceeds 3e-5 below 22" | McCracken+26 p. 4-7 |
| VIS chromatic shift | red-minus-blue centroid shift up to a few mas, mostly along the FPA x axis | McCracken+26 p. 7 |
| NIR vs Gaia | mean ~10 mas, offsets <2 mas, <20 mas for 99% of dithers (Y_E ~15, H_E ~10 mas in stacks) | [Radovich+26](papers/radovich.md) p. 3, 6 |
| NIR tail | RMS >30 / 60 / 90 mas over 3% / 0.3% / 0.1% of the area (persistence masking, DET13/14); the Explanatory Supplement quotes 0.7% of area >50 mas; Schirmer+26a gives 0.70/0.23/0.14% above 0.05/0.08/0.1" and affected patches 1'-3' wide | Radovich+26 p. 9; Schirmer+26a p. 12-13 |
| MER mosaics vs Gaia | offsets <10 mas for tiles with `FILLING_FACTOR` > 0.5 | Kuemmel+26 p. 7 |
| Skypatches 39 and 40 | VIS processed with an inappropriate distortion model (median largest quadrant residual 23 mas in skypatch 40) | McCracken+26 p. 3, 11 |

VIS-NIR co-registration is therefore far below one NIR pixel almost everywhere; re-register locally inside the NIR astrometric tail
(VMPZ-ID information map, [Odier+26](papers/odier.md)).

## 8. Photometric accuracy and stability

| Quantity | Value | Source |
|---|---|---|
| VIS relative, quadrant / source level (internal, external) | 0.76/1.4 mmag; 11/25 mmag; mean offset to Gaia +3.8 mmag | McCracken+26 p. 8 |
| VIS requirement | 1% relative, 5% absolute | McCracken+26 p. 8 |
| NIR repeatability | 0.9% for sources brighter than 19 mag (requirement 1.5%); time stability ~2 mmag RMS except Nov 2023-Mar 2024; spatial residuals <= 0.01 mag | Polenta+26 p. 8-9 |
| NIR aperture photometry vs Gaia | within 2%, 3%, 5% (Y_E, J_E, H_E) | da Silva+26 p. 10 |
| MER A-PHOT vs Gaia | I_E offset about -0.02 +- 0.004 mag; NIR -0.036 to -0.126 mag by method (T-PHOT bug, PSF fitting ~-0.13); scatter ~0.015 | Kuemmel+26 p. 8 |
| MER relative error (NMAD, Gaia stars) | I_E 15, Y_E 35, J_E 40, H_E 47 mmag; DECam griz 27/22/21/26; HSC-g 33, HSC-z 29; PS-i 20; MegaCam-u 97, -r 26 | Kuemmel+26 p. 9 |
| Source injection | recovered within 5% | Kuemmel+26 p. 8 |
| Wide vs deep (same tile) | offsets <= ~0.01 mag; Sersic R_e within 1%, n within a few % (IE < 23.5) | Kuemmel+26 p. 12 |
| PSF normalisation | the I_E stamp normalisation (~1% NMAD tile to tile) limits DR1 absolute photometry; I_E-based colours cancel it | Kuemmel+26 p. 10 |
| Extended galaxies | MER fluxes of extended COSMOS galaxies are slightly high versus COSMOS2025 (all methods); T-PHOT best in NIR | Kuemmel+26 p. 8; [Gasparetto+26](papers/gasparetto.md) |

Zero points and units of the DR1 mosaics (header `MAGZERO`): I_E 24.5 (ADU/s), Y_E 29.8, J_E 30.1, H_E 30.0 (electron/s), EXT 30.0; catalogue fluxes in microJy (verified_on_archive.md). Single-exposure VIS frames are in ADU with `MAGZEROP` ~24.57 (Q1) and NIR frames in electrons.

Depths (5 sigma, 2" aperture, median EWS; Odier+26 via the 10_ file): I_E 25.69, Y_E 24.14, J_E 24.30, H_E 24.29. Schirmer+26a quotes 25.0 for NISP with a 2 x FWHM aperture: different definitions. Quote any depth with its definition; sky-noise depths do not equal surface-brightness limits.

## 9. Other known imaging issues (DR1)

- `MAG_MODEL` (VIS single-frame PSF fitting) is unreliable: inconsistent PSF normalisation between quadrants (McCracken+26 p. 11). Prefer aperture fluxes.
- Missing coverage: 34 (I_E), 405 (Y_E), 560 (J_E), 510 (H_E) tiles have >10% less coverage than VIS+NIR; tile 102015130 J_E has two layers instead of four; caused by solar proton showers (Kuemmel+26 p. 13-14). Always inspect cutouts for zeros/NaNs (verified_on_archive.md).
- Bright-star masks cover 1-5% of EWS tile area (saturated cores and spikes only; no halos) (Kuemmel+26 p. 6).

## 10. Pipeline versions frozen for DR1

EXT 0.12.9; VIS 18.0.4; NIR 6.1.2; MER 11.3.1; SIR 6.0.2; LE3-ID-VMPZ 1.6.4/1.6.5; SPE 25.0.1; PHZ 2.16.13; SHE 9.12.2 ([Ruffenach+26](papers/ruffenach.md) p. 24; [Aussel+26](papers/aussel.md) p. 4). Q1 used VIS PF 17.0 (dpdd_vis_nir.md). The DR1-Foundation products "will not be re-released" in 2027 (Aussel+26 p. 1, 4); the VIS PSF model underestimating the PSF size delayed shear to June 2027 (p. 4). Record these versions in any paper.

## Implications for extended-galaxy photometry and 2-D modelling

1. **Choose the input by size.** R_e below a few arcsec (and objects < ~10"): the `BGSUB` mosaic with RMS, FLAG and the MER PSF is adequate; fit your own constant or plane for residual sky. 10"-1': add `BGMOD` back and fit a large-annulus sky. Larger: rebuild from calibrated frames. Sky bias shows up as biased n and R_e and truncated outer discs ([10_low_surface_brightness.md](10_low_surface_brightness.md); [Bamford+26](papers/q1_icl_processing_bamford.md)).
2. **Pixels are correlated and PSF is broadened by the mosaic.** Bilinear + median co-addition widens the PSF by ~15% beyond a Lanczos-3 co-add and correlates noise: use the MER-propagated PSF (not the single-frame VIS PSF) when fitting a mosaic, and estimate noise empirically in random apertures at your scale. The `RMS` map is a per-pixel value.
3. **Which PSF normalisation?** DR1 stamps are not renormalised (I_E sum ~0.96): a model convolved with the stamp as delivered loses ~4% of the flux; correct Sersic fluxes by `S` (Kuemmel+26 p. 10) or renormalise the stamp yourself and decide consciously.
4. **Fluxes.** For total fluxes of extended galaxies use Sersic or `FLUX_DETECTION_TOTAL` (Kron), not 1-4 FWHM apertures (aperture colours); Kron is truncated in the outskirts of large galaxies. Colours: aperture or T-PHOT fluxes on PSF-matched cutouts, or your own PSF-matched fits across bands. Remember the 1-1.5% focal-plane-position colour bias in I_E for red extended sources (LSF built from stars) and the 4.7% shutter gradient of short exposures (avoid them for LSB).
5. **NIR specifics.** 0.3" pixels undersample the PSF; combine with I_E for structure. Persistence masks can cut across a bright galaxy, residual 1/f stripes and persistence-like background patterns exist at ~1-5% of a ~100 e- sky; the stack DQ has lost the persistence flags, so check single-dither DQ. J_E suffers most.
6. **Tile geometry and shredding.** Galaxies above ~2' may sit on tile borders (special tiles were not run) and are shredded in the catalogue: mosaic neighbouring tiles yourself and ignore catalogue segmentation for the target. In EDFs check the deep stack (`101...`) when the wide mosaic is empty.
7. **Masks.** Mask ghosts (70" from stars with G < 14), diffraction spikes, serial-bleeding bands and bright-star halos yourself; the MER masks cover cores and spikes only.
8. **Field choice.** Single-visit wide data are shallow for LSB; deep fields and auxiliary fields add depth but have their own artefacts (roll-angle patterns, HSC r/i issues). Check VMPZ-ID depth/PSF maps and `FILLING_FACTOR`.
9. **Reproducibility.** Single-Sersic MER fits are reliable to I_E ~ 23 in R_e and q, but n should not be trusted individually; use bulge-disc fits of your own ([Dunn+26](papers/dunn.md); Kuemmel+26 p. 12).

## What to cite

| For | Cite |
|---|---|
| DR1 overview and data release | Aussel+26 ([aussel.md](papers/aussel.md)), Ruffenach+26 (processing, versions), Tereno+26 (survey, ROS) |
| VIS processing | McCracken+26 (DR1) and McCracken+26 (Q1) |
| NIR processing, astrometry, persistence, PSF | Polenta+26, Radovich+26, Kubik+26, da Silva+26 |
| EXT data | Corcho-Caballero+26 |
| MER mosaics, catalogue | Kuemmel+26 (DR1), Romelli+26 (Q1 base) |
| Calibration and spacecraft | Schirmer+26a (calibration strategy), Schirmer+26b (spacecraft) |
| Masks and survey maps | Odier+26 |
| LSB processing | Bamford+26 (Q1 ICL processing) and the Explanatory Supplement 15.2.2 |
| Archive data | ESA DOI 10.57780/esa-d079c51 (given in Kuemmel+26 p. 14-16), plus the PF versions of section 10 |

## Source conflicts found while writing

- Q1 NIR propagated PSFs: Romelli+26 (Q1) p. 9 (Table 2) says they were 1.75-3.5% **more compact** than Gaia stars (0.475 vs 0.492" in Y_E); Kuemmel+26 p. 4 says the Q1 NIR FWHM values were 1.75-3.5% **larger**. The Q1 table numbers favour "more compact".
- VIS and NIR stacks: [dpdd_ext_archive.md](data_model/dpdd_ext_archive.md) says not distributed; the archive tables and help page say available ([verified_on_archive.md](data_model/verified_on_archive.md)).
- `FLUX_RADIUS`: Kuemmel+26 p. 4-5 describes an SE-like measurement within 6 a_M; Explanatory Supplement 15.3.5 says the DR1 version was limited to the segmentation area.
- T-PHOT bug: Kuemmel+26 p. 8 mentions one bug mostly affecting bright point sources; Explanatory Supplement 15.3.2 lists two bugs, one affecting all template-fitting runs (minor for galaxies).
- Decontamination dates: 14 Mar / 8 Jun 2024 (Schirmer+26b) versus 12 Mar / 6 Jun (Q1 VIS) and 12-21 Mar / ended 12 Jun (Tereno+26): different events (start of heating, end of recalibration).
- VIS PSF FWHM: 0.14" (stars, single frames, McCracken+26), ~0.158" (Q1 PSFEx model), 0.20-0.21" (MER mosaic stamps, Kuemmel+26 p. 14): different definitions and stages, not an inconsistency (see [05_psf.md](05_psf.md)).
