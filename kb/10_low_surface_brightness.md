# Low-surface-brightness (LSB) work with Euclid DR1

> Scope: outskirts and stellar haloes of nearby/low-z galaxies, tidal features, dwarfs, intra-cluster light (ICL),
> and any 2-D modelling whose result depends on the sky level (outer discs, Sersic n, large R_e).
> Sources: [Explanatory Supplement 15.2.2](expsup/README.md), Q1/DR1 processing papers
> ([q1_romelli_mer](papers/q1_romelli_mer.md), [q1_mccracken_vis](papers/q1_mccracken_vis.md),
> [q1_polenta_nir](papers/q1_polenta_nir.md), [mccracken](papers/mccracken.md), [polenta](papers/polenta.md),
> [kuemmel](papers/kuemmel.md)), calibration/spacecraft papers ([schirmer-spacecraft](papers/schirmer-spacecraft.md),
> [schirmer-calibration](papers/schirmer-calibration.md), [kubik](papers/kubik.md), [dasilva](papers/dasilva.md),
> [odier](papers/odier.md)), and the cluster-team ICL papers
> ([q1_icl_processing_bamford](papers/q1_icl_processing_bamford.md), [q1_icl_halo_shapes_kolcu](papers/q1_icl_halo_shapes_kolcu.md),
> [q1_icl_fraction_gully](papers/q1_icl_fraction_gully.md)) plus [gatto](papers/gatto.md) (resolved LSB dwarfs).
> Hands-on check: `demo/05_lsb_background.py` (NGC 1483, wide vs deep, BGMOD restored) -> section 7.

## 1. Bottom line

1. **The official DR1 statement** (Explanatory Supplement 15.2.2): the SGS pipeline is optimised for arcsecond-sized
   galaxies at z > 0.5; LSB features "are mostly filtered out at the MER stage". Alternative LSB-preserving products
   (from the VIS/NIR calibrated frames) are being prepared by Consortium groups and will come later via ESA Datalabs,
   **not in DR1-Foundation**.
2. **Diffuse light is removed in two places**: (i) a per-exposure background subtracted from every calibrated frame
   before stacking/mosaicking (VIS: NoiseChisel per CCD quadrant; NIR: NoiseChisel per detector in DR1), and (ii) a
   second, tile-level MER background (256-pixel = 25.6" mesh, 3-cell = 76.8" median filter) on the mosaic.
   Only (ii) is stored with the mosaic (`BGMOD`) and can be added back.
3. **Rule of thumb** (Bamford et al., Q1, confirmed qualitatively for DR1 by the Supplement):
   - objects smaller than ~10": MER `BGSUB` mosaics and catalogue photometry are fine;
   - VIS, 10" to ~1': restore the MER background (`BGSUB + BGMOD`) and fit your own local sky in a much larger
     annulus;
   - NIR above ~0.5'-1', and anything above ~1' in any band (galaxy haloes, ICL, tidal streams, large nearby galaxies):
     **rebuild from the calibrated single-exposure frames** (`DpdVisCalibratedQuadFrame`, `DpdNirCalibratedFrame`,
     with their `BKG`, `WGT`/`RMS`, `FLG`/`DQ` layers), with additive detector-level corrections and one large-scale
     sky at the end ([recipe in section 6](#6-recipe-rebuilding-lsb-safe-images-from-calibrated-frames)).
4. **Realistic limits** for single-visit (wide-survey) depth: 3 sigma in 10"x10" boxes of about 27.8 mag/arcsec^2
   (I_E) and 26.4 (Y_E, J_E, H_E); about 29 (I_E) and 27.5 (YJH) on arcmin scales after LSB-specific processing.
   Never extrapolate pixel noise with 1/sqrt(N): that is > 2 mag too optimistic.
5. **Large galaxies (> 2')**: special MER tiles for 164 526 large objects were designed but **not processed in DR1**;
   such galaxies are shredded by the deblender, may cross tile edges, and are deliberately masked in the VMPZ
   effective-coverage maps (SGA galaxies with MAG_LEDA < 16.5).

## 2. Where the sky is subtracted (and whether it can be undone)

| Stage | Product (archive table) | Algorithm and scale | Stored? | Undo? |
|---|---|---|---|---|
| VIS per exposure | `DpdVisCalibratedQuadFrame` (`dr1.calibrated_frame`, aux `BKG`) | NoiseChisel (Gnuastro 0.16) per quadrant (2066x2048 px = 3.4'x3.4'); if a quadrant has a lot of signal, re-run with looser options, else SExtractor fallback. Over-subtracts inside objects larger than one quadrant; slightly negative sky near sources in DR1 | yes, `BKG` map per exposure; `SCI` is **not** background-subtracted | yes, from calibrated frames |
| NIR per exposure, DR1 | `DpdNirCalibratedFrame` (aux `BKG`) | NoiseChisel v0.16, quantile threshold 0.3, 10x10 px tessellation (3"), Manhattan interpolation, 3-px flat kernel, per detector (2040 px = 10.2'). Tuned to protect extended light (NGC 1483 comparison, Polenta Fig. 4) | yes, `BKG` per exposure; `SCI` not subtracted | yes, from calibrated frames |
| NIR per exposure, Q1 (for comparison) | idem | SExtractor-like 64x64 px boxes (19.2"), 3x3 median filter (~58"), no source mask: "considerable over-subtraction" around bright extended galaxies | yes | yes |
| VIS/NIR stacks | `DpdVisStackedFrame`, `DpdNirStackedFrame` (`dr1.observation_stack`) | built from background-subtracted exposures (NIR stack in microJy); DR1 VIS stack has no BKG/RMS/FLG extensions any more | no | no |
| MER mosaic | `DpdMerBksMosaic` (`dr1.mosaic_product`, aux `BKG` = `EUC_MER_BGMOD-*`) | inputs: per-exposure-background-subtracted frames, SWarp BILINEAR, MEDIAN combine. Then SE++ source mask, 256x256 px cells (25.6"), 2-sigma clipping, mean or mode (2.5 median - 1.5 mean), 3-cell median filter (76.8"), spline; one pass | yes, `BGMOD` (same 19200x19200 grid, same units) | **only this step**: `BGSUB + BGMOD` |
| EXT (ground) | MER EXT mosaics (DECam, MegaCam, HSC, Pan-STARRS) | sky subtracted per exposure before stacking (SWarp mesh 256 px DECam, 128 MegaCam; HSC and PS1 native pipelines); not tested on large galaxies ([corcho-caballero](papers/corcho-caballero.md)) | no | no |

Consequences (Bamford et al. 2026, Q1): with both steps, VIS loses diffuse light on scales above ~10" and NIR above
~0.5'. Restoring BGMOD rescues VIS structures up to ~1'. In NIR the per-exposure step dominated in Q1; DR1 replaced it
by NoiseChisel (improvement acknowledged), but the authors still require dedicated processing above ~1'. MER aperture
photometry does **no local sky subtraction** because "two background subtractions have already been performed"
(Romelli), so any sky bias propagates directly into Kron, aperture and Sersic fluxes of large galaxies.

## 3. Which product for which science case

| Target / measurement | Recommended DR1 input | Notes |
|---|---|---|
| Sersic/bulge-disc fits of galaxies with R_e < ~3" (most z > 0.1 galaxies) | MER `BGSUB` cutouts + MER PSF (`GRID-PSF`/`CATALOG-PSF`) + RMS/FLAG | fit a residual sky plane; compare with catalogue `SERSIC_*` |
| Surface-brightness profiles to ~27 mag/arcsec^2 of galaxies 10"-1' (VIS) | `BGSUB + BGMOD` (full tile download; the cutout service does not serve BGMOD/RMS) | re-estimate sky in an annulus beyond ~3-5x the galaxy size; check BGMOD for a "hole" at the galaxy |
| Same in NIR | treat MER NIR profiles beyond ~0.5' as lower limits; prefer calibrated frames | NIR has persistence, 1/f stripes, detector offsets |
| Galaxies > 1', stellar haloes, tidal features, ICL, cirrus | calibrated frames + `BKG` + weights/flags, own background matching and co-addition | Bamford recipe; ~6 (NIR) / 10 (VIS) neighbouring observations for an atemporal background |
| Resolved dwarfs (Local Volume) | MER catalogue for selection (`POINT_LIKE_PROB`, colours), VIS stacks/mosaics for vetting, own PSF photometry | Gatto et al.: MER photometry weaker in crowded fields |
| Statistics over many galaxies (stacking) | MER cutouts, but forward-model the sky subtraction (inject mocks) | masks and sky scale bias outer profiles |
| Deep fields | deep tiles (`101xxxxxx`, `DR1_R1`, `DATA_RELEASE_DEEP`, mode `DEEP`): EDF-N 11 visits, EDF-S 10, EDF-F 2 | different roll angles average down detector artefacts; CDFS/COSMOS deeper still |

## 4. Instrumental and astrophysical contaminants of LSB light

| Effect | Band | Size / where | Treated in DR1? | What to do |
|---|---|---|---|---|
| Out-of-field / in-field stray light | VIS (and NIR) | VIS stray light ~10-15% of zodiacal light after the azimuth fix; depends on solar aspect angle (SAA) and azimuth angle (AA), detector region (quadrant groups C, D worst), grows ~14%/yr | removed only as part of the nominal background | attitude-matched or local background models; compare exposures from different observations |
| Zodiacal light | all | 0.09-0.15 MJy/sr near the NEP; dominant sky | smooth, subtracted | fine for small objects; large-scale gradients across a tile |
| Galactic cirrus | all | sets the arcmin-scale floor even at |b| > 30 deg: EDF-N limit 0.4 (I_E)/0.2 (H_E) mag brighter than EDF-S/F | not modelled | check Planck/IRAS dust maps; avoid or model |
| VIS dichroic ghost | VIS | compact ghost ~70" from stars with G <~ 14 (stronger for blue stars); weaker during the 2024 ice episode | flagged by a model (flux threshold), not subtracted; unmasked ghosts remain in deep data and create spurious detections | mask all stars G < 14 with a 70" offset ghost region; inspect |
| NIR ghosts and arcs | NIR | dichroic/filter ghosts flagged (DQ bit 18 GHOST); arcs of radius ~1.7' around stars brighter than ~11 mag flagged as PERSIST (bit 13) | flagged only | grow masks; avoid |
| Internal-reflection arcs | NIR | diffuse arcs (~3% of images) not modelled | no | visual inspection |
| VIS blooming / serial-register bleeding | VIS | bands from I_E ~ 10 stars | partly flagged | mask |
| NIR persistence | NIR | 5 h look-back, 2 e- threshold, masked (not corrected): ~5% of J_E pixels, >10% on some detectors; residual charge-release structure up to ~2% (5% on DET11/14/44) of the background | masked | do not use PERSIST pixels for faint outskirts; Bamford model for removal |
| NIR 1/f ("tartan") row/column stripes | NIR | exposure-to-exposure banding, ~100 px scales | no (DR2) | row/column median after masking |
| Detector/quadrant offsets, illumination residuals | both | VIS ~2% between/within quadrants, NIR ~5% additive structure applied multiplicatively | partly | additive per-detector background matching on overlaps |
| Flat-field accuracy | VIS | large-scale flat 0.08-0.14%; star-vs-galaxy colour bias up to 1-1.5% at the right FPA edge; ~0.4% monthly | partly | small for SB; matters for colour gradients |
| VIS shutter gradient | VIS | 0.8% (nominal), 4.7% (89.5 s short exposures) | not corrected until DR2 | exclude short exposures from LSB stacks |
| PSF wings | all | MER PSF stamps <= 5"; NISP PSF models only to 3" (stack) / 7" (single) with 1-2% of light beyond 7"; no scattered-light model | no | build extended PSFs from bright stars or use the ERO extended PSF (Cuillandre et al. 2025) |
| Bright-star masks | all | MER masks only saturated cores and spikes (1-5% of area) | yes (cores/spikes) | build halo masks from Gaia (r(G_RP) relation in Odier et al.) |
| Resampling noise correlation | all | MER uses BILINEAR: pixel noise underestimates large-scale noise (NIR by ~0.44 mag/arcsec^2) | n/a | measure noise in random apertures at your scale |
| Diffuse light of faint galaxies | VIS deep | EUDF depth 0.2 mag shallower than extrapolated in the deepest regions | n/a | sets a confusion floor in very deep data |

## 5. Surface-brightness limits and units

**Pixel units** (verified on DR1 files): VIS mosaics `BUNIT = ADU/s`, `MAGZERO = 24.5`; NISP mosaics
`BUNIT = ELECTRON/s`, `MAGZERO` 29.8 (Y), 30.1 (J), 30.0 (H) (the `zero_point` column of `dr1.mosaic_product`); EXT
mosaics `MAGZERO = 30`. Pixel scale 0.1". Hence, for a pixel value `I`:

    m_AB(pixel) = MAGZERO - 2.5 log10(I)
    mu [mag/arcsec^2] = MAGZERO - 2.5 log10(I) + 5 log10(0.1) = MAGZERO - 5.0 - 2.5 log10(I)
    flux [microJy/pixel] = I * 10**(-0.4 (MAGZERO - 23.9))

(Catalogue fluxes are in microJy: m = 23.9 - 2.5 log10(F).) Correct for Galactic extinction (`GAL_EBV` column; VMPZ
extinction maps) and cosmological dimming yourself.

**Published limits** (always quote the definition):

| Data | Limit | Definition | Source |
|---|---|---|---|
| Q1 EDF single visit, LSB-processed from frames | 27.8 (I_E), 26.4 (Y_E/J_E/H_E) | 3 sigma, 10"x10" boxes, random masked apertures | Bamford et al. |
| same, arcmin scales | ~29 (I_E), ~27.5 (YJH) | 3 sigma, elliptical annuli of arcmin size | Bamford et al. |
| ERO LSB reduction | 28.3 (I_E), 26.8 (H_E) | 3 sigma, 10"x10", 26" background | Cuillandre et al. 2025 via Bamford |
| combined LE2 frames without extra processing | brighter than ~26.3 (VIS), ~25.5 (NIR) at any aperture | 3 sigma | Bamford et al. |
| MER VIS, realistic dwarf profiles (r_h ~ 10") | 26-27 | injection-recovery | Urbano et al. 2026 via Bamford |
| EWS point-source depth (median) | 25.69 (I_E), 24.14 (Y_E), 24.30 (J_E), 24.29 (H_E) | 5 sigma, 2" aperture | Odier et al. / VMPZ depth maps |
| Resolved dwarfs found in DR1 | mean mu_V ~ 27-31 | from resolved stars | Gatto et al. |

Limits in our own demo field are in section 7.

## 6. Recipe: rebuilding LSB-safe images from calibrated frames

Adapted from Bamford et al. (Q1, code `nicl`: github.com/IntraClusterLight/nicl_q1). All inputs are in DR1:
`dr1.calibrated_frame` + `dr1.aux_calibrated` (VIS: `DET` 432 extensions = 144 quadrants x SCI/RMS/FLG, plus `BKG`,
`WGT`, `PSF`; NIR: `CAL` 48 extensions = 16 detectors x SCI/RMS/DQ, plus `BKG`, PSF files). A VIS calibrated frame is
~7 GB, so restrict to the observations overlapping the target plus its neighbours.

1. Use `SCI` (not sky-subtracted). Ignore the pipeline `BKG` or keep it only as a diagnostic.
2. **Atemporal background**: source-masked median over ~6 (NIR) / 10 (VIS) neighbouring observations, after coarsening
   to 51x51 (NIR) / 149x149 (VIS) px boxes; subtract per exposure, add back one scalar level.
3. **NIR tartan**: mask sources, remove a 200-px circular median, subtract masked row and column medians.
4. **NIR persistence**: model from the 9 nearest same-band exposures (second-lowest value), power-law decay
   (index ~1.0); mask where the uncertainty exceeds 20 e-.
5. Resample all detectors (SWarp LANCZOS2) to a common grid without background subtraction (distortion changes pixel
   areas by 1-2%, so the sky must already be near zero).
6. **Background matching**: least-squares additive constant per detector from all overlapping pairs (source-masked).
7. Co-add with a clipped weighted mean (not the MER median, which is noisier).
8. Only now subtract one large-scale background: box >= ~3x the target size (1 Mpc for clusters; 9' at z = 0.1),
   3x3 median filter, sources and target masked; the cutout must hold at least 3x3 boxes.
9. Masks: detect at 3 sigma over >= 5 px, deblend, grow by 50% outside the target and 25% inside; protect the target
   with an adaptive-smoothing mask; combine Y+J+H for a single NIR mask.
10. Profiles: elliptical annuli (not circular), sigma-clipped medians; AutoProf with regularised PA/ellipticity;
    errors from random blank-sky apertures at the same scale plus mock injection into the frames.

Simpler, cheaper variant for VIS and moderate sizes: download the MER tile `BGSUB` and `BGMOD`, add them, mask sources,
fit a low-order plane or large-box background beyond 3-5x the galaxy radius, and measure profiles; demonstrated in
`demo/05_lsb_background.py`.

### 6.1 Can the Nottingham ICL method (Bamford, Kolcu, Gully et al.) be reproduced with public DR1? (checked 2026-11-13)

The group is the Nottingham ICL team (N. A. Hatch, S. P. Bamford; contact `icl-group@nottingham.ac.uk`). The method
paper is Bamford et al. (arXiv:2610.29682).

**Verdict: yes for the processing. Every input is public and downloads anonymously. Their code is public but needs
adapting, and the data volume per target is large.** Checked by TAP queries and downloads:

| Input the method needs | In public DR1? | Verified detail |
|---|---|---|
| VIS calibrated quad frames (`SCI`, `RMS`, `FLG`) + `BKG` + `WGT` | yes | `dr1.calibrated_frame`: 42 092 `DpdVisCalibratedQuadFrame` (DR1_R1); `dr1.aux_calibrated`: 42 092 each of `BKG`, `WGT`, `PSF MODEL`, `QUALITY_PARAMETERS`; HTTP 200 for DET, BKG, WGT with `release=dr1`, anonymous |
| NIR calibrated frames (`SCI`, `RMS`, `DQ`) + `BKG` | yes | 66 723 (R1) + 4936 (R2) `DpdNirCalibratedFrame`; 71 659 `BKG`. One H frame of obs 2683: `CAL` 799 MB, 49 HDUs (16 detectors x SCI/RMS/DQ), `BUNIT = ELECTRON`, sky ~65 e- **still in SCI**; `BKG` 799 MB, same 49-HDU layout, NoiseChisel model ~63 e-; DQ bit 13 (PERSIST) on 4.6-5.7% of pixels; `MJD-OBS`, `EXPTIME`, `OBS_ID`, `DITHOBS` in the primary header; `ZPAB` per detector |
| NISP spectroscopic exposures (persistence sources) | yes | `dr1.sir_science_frame`: 26 581 frames (`EUC_SIR_W-SCIFRM_BKGSUB_*`, background-subtracted); 76 cover the Q1 test cluster; HTTP 200 (contents not inspected) |
| Exposure times for the persistence time sequence | yes | `dr1.calibrated_frame.start_time_mjd`, `duration`; `MJD-OBS` in the headers |
| LE1 raw frames (optional) | yes | `dr1.raw_frame`: 201 082 rows (e.g. `EUC_LE1_NISP-02683-...`); HTTP 200. Some `dr1.raw_frame` column combinations return HTTP 500 from TAP (select `file_name` first) |
| Neighbouring observations for the atemporal background | yes, within the DR1 area | Q1 test cluster MCXC J1754.6+6803: **13 observations** in DR1 (Q1 had obs 2683 only), 196 calibrated frames (65 VIS incl. short exposures, 43-44 per NIR band) |
| MER tiles + `BGMOD` (comparison) | yes | see section 7 |
| Euclid cluster catalogue (AMICO+PZWav, used by Gully+26) | **no** (LE3 clusters come with full DR1, mid-2027) | use external catalogues: eRASS1, DES/Legacy redMaPPer, SPT, ACT (Kolcu+26 used eRASS1 + DES Y3 redMaPPer) |
| Hydrangea mock clusters (validation) | not a Euclid product | not needed to reproduce the processing; inject your own mocks |

**The code:** [github.com/IntraClusterLight/nicl_q1](https://github.com/IntraClusterLight/nicl_q1) (Apache-2.0, nbdev,
last push 2026-07-28). Its README calls it a "snapshot of work in progress", with a DR1 version promised with future
papers. The scripts are `scripts/v0.7/run_pipeline_{nir,vis}.py`, `get_all_nir.py`, `create_coarse_data.py`,
`do_persistence_correction.py`, `stack_Q1.py` and `run_measure.py`, written for SLURM on the Nottingham HPC cluster
(ada).

`nicl/euclid/data_access.py` already has a "DR1" mode, but it points to the **Consortium-internal** server
(`easidr.esac.esa.int`, schema `sedm`, `environment='DR1'`). For the public archive, change:
- the server to `https://eas.esac.esa.int`;
- the table schema `sedm.` to `dr1.` (the tables `calibrated_frame`, `sir_science_frame`, `raw_frame` and
  `mosaic_product` exist with the same columns used by nicl);
- the release condition to `release_name IN ('DR1_R1', 'DR1_R2')`;
- downloads to `release=dr1`.

**Practical caveats:**
- **Volume** depends on the field size and on which corrections you apply. See section 6.2. The figure quoted
  first (10 x 4 x 7.3 GB = ~290 GB VIS, 6 x 4 x 1.6 GB = ~38 GB per NIR band) assumes whole files for a field
  that fills the focal plane, as for the 30'x30' cluster fields of Bamford+26. For a ~1' galaxy, partial reads
  bring this down to 0.9 GB (science only) to ~54 GB (full recipe).
- **Neighbour selection.** DR1 needs a selection by time and angular separation, not the Q1 observation-ID sequence
  (Bamford+26, p. 17).
- **Persistence.** The model needs the temporally preceding exposures. A previous pointing outside the released area
  (calibration blocks, unreleased fields) leaves gaps.
- **DR1 differences.** DR1 NIR backgrounds are improved (Bamford+26, p. 3), but SCI is still not background-subtracted,
  so the recipe starts from the same point. Check whether the tartan and atemporal corrections are still needed at the
  same amplitude before applying them blindly.

### 6.2 How much data for one galaxy? Partial reads of calibrated frames (measured 2026-11-13, `demo/09_frame_cutouts.py`)

**Key facts (verified):**
- The data service answers HTTP range requests (`206 Partial Content`, `Accept-Ranges: bytes`), and HEAD returns
  the exact size.
- The calibrated frames have a perfectly regular layout:
  - VIS `DET`: a 17,280-byte primary header, then 144 (SCI, RMS, FLG) triples of 3 x 16,934,400 bytes
    = 7,315,678,080 bytes in total;
  - NIR `CAL`: an 11,520-byte primary header, then 16 triples of 49,959,360 bytes = 799,361,280 bytes.
- So one CCD quadrant (VIS) or one detector (NIR) can be fetched with **one range request**. The cost is ~50 MB
  and 12-18 s (3-4 MB/s, with several seconds of latency per request).
- To know which unit holds a target, the script builds a focal-plane model once per instrument. It reads the 144
  (VIS) or 16 (NIR) SCI headers of one exposure and stores the unit corners relative to `ra`, `dec`, `pa` of
  `dr1.calibrated_frame`; then it predicts the units for any other exposure. All predicted units contained the
  target.
- `dr1.calibrated_detectors` cannot be used for this: it has NIR rows only, all detectors of a frame share one
  `crval`, `crpix1` = `crpix2`, and `observation_id` is NULL.

**Test case:** ESO 248-G006, the BCG of Abell 3112 (z = 0.075, so 1' is about 86 kpc), observation 5897 (one ROS of
4 dithers). Units covering the target:

| Region | VIS quadrants (per dither; union of indices) | NIR detectors per band (per dither; union) |
|---|---|---|
| 1'x1' (radius 0.5') | 1, 2, 2, 1 = 6 (4 distinct) | 1, 1, 1, 1 = 4 (1 distinct) |
| 9'x9' (radius 4.5'; room for 3x3 background boxes of 3') | 9, 10, 10, 10 = 39 (14 distinct) | 2, 2, 3, 4 = 11 (4 distinct) |

Measured file sizes per exposure:

| File | Size per exposure | Per unit |
|---|---|---|
| VIS `DET` | 7315.7 MB | 50.8 MB per quadrant |
| VIS `BKG`, VIS `WGT` | 2438.6 MB each | 16.9 MB per quadrant |
| NIR `CAL`, NIR `BKG`, SIR `SCIFRM_BKGSUB` | 799.3 MB each | 50.0 MB per detector |

Volumes for one galaxy in VIS + Y + J + H. These are arithmetic from the unit counts and sizes above; the times
assume the measured ~3.5 MB/s:

| Level of processing | What you fetch | Volume | Whole-file equivalent |
|---|---|---|---|
| **A. 1' science region** (own sky from a local annulus; pipeline BKG optional) | 6 VIS quadrants + 4 detectors x 3 bands | **0.90 GB** (+0.70 GB for the BKG units); **measured: 904 MB in 295 s** (16 requests) | 4 x 7.3 GB + 12 x 0.8 GB = 39 GB |
| **B. 9' field** (background matching across units and dithers, one large-scale sky on 3' boxes) | 39 VIS quadrants + 11 detectors x 3 bands | **3.6 GB**; ~20 min | same 39 GB |
| **C. full Bamford recipe** = B + atemporal background (same unit indices in 10 VIS / 6 NIR neighbouring observations x 4 dithers) + NIR persistence (4 same-band exposures either side, plus the SIR frames of the 3 observations) | C1: 10 x 4 x 14 x 50.8 MB = 28.4 GB (VIS); 6 x 4 x 4 x 50 MB = 4.8 GB per NIR band. C2: <= 1.6 GB per band + 2.4 GB SIR | **~54 GB** upper bound (43 GB of it atemporal); ~4 h at one stream | 10 x 4 x 7.3 GB + 3 x 6 x 4 x 0.8 GB = ~350 GB |

What this means for a ~1' massive galaxy:
1. **VIS.** Bamford+26 (p. 2) find the MER mosaic with BGMOD restored adequate for VIS LSB work up to about 1'. Take
   the BGSUB cutout from the cutout service. Take the BGMOD (and RMS) cutout with a **row-range read of the tile
   file**: `dr1_access.remote_rows_cutout`, about 46 MB and ~26 s for 1'. It is pixel-identical to the same region of
   the full 1.47 GB tile (checked on NGC 1483).
2. **NIR.** The per-exposure background cannot be restored from the mosaic, but `SCI` in the calibrated frames still
   contains the sky. Level A or B gives you un-subtracted NIR data for under 4 GB: co-add the dithers yourself and
   fit one large-scale sky.
3. **Full corrections.** Atemporal background, tartan and persistence matter for arcminute-scale haloes at
   <~ 27.5 mag/arcsec^2 (NIR). Most of their cost (C1) characterises the **detectors, not the target**. Compute it
   once per period and sky region (e.g. in Datalabs) and reuse it for every target observed in that period.

## 7. Hands-on: NGC 1483 (EDF-South), wide vs deep, with and without the MER background

Script `demo/05_lsb_background.py`, figure `figures/dr1_lsb_ngc1483.png`, numbers
`figures/dr1_lsb_ngc1483_limits.json`. Data: wide tile 102021980 (`DR1_R2`, one EWS visit) and EDF-South deep tile
101287204 (`DR1_R1`, 10 visits); 8'x8' regions block-averaged to 1" pixels; sources masked (1.5 sigma segmentation,
dilated); fixed ellipse (q = 0.8, PA = 160 deg); "restored" = BGSUB + BGMOD minus our own sky (sigma-clipped median in
the 3'-4' elliptical annulus).

**What the MER background did to NGC 1483 (D25 ~ 2'):**
- The BGMOD maps (panels b, c) show a **positive bump centred on the galaxy**, extending ~1.5' from the centre: the
  MER sky model absorbed galaxy light although sources were masked. Its amplitude is ~3x larger in the single-visit
  wide mosaic than in the deep stack.
- Fraction of the light removed by the MER step (panel f): negligible inside ~30", then rising to **~40% (deep I_E)
  and ~65% (wide I_E) at a semi-major axis of ~100"**, and ~55% in wide H_E at ~80". The deep H_E BGMOD has no such
  bump (restoring it slightly lowers the outskirts), so the effect varies between bands and tiles.
- Profiles (panels d, e): delivered (BGSUB) and restored profiles agree to ~1' and diverge beyond; the deep restored
  I_E profile is traced to ~29 mag/arcsec^2 at ~2'.

**Measured 3-sigma surface-brightness limits in 10"x10" boxes** (random boxes on masked sky beyond 2.5'):

| Image | BGSUB | restored | naive from pixel RMS (1/sqrt(N)) |
|---|---|---|---|
| wide I_E (1 visit) | 28.2 | 28.3 | 29.8 |
| deep I_E (10 visits) | 29.0 | 29.1 | 31.0 |
| wide H_E | 27.0 | 27.0 | 29.6 |
| deep H_E | 27.9 | 27.9 | 30.7 |

- The naive white-noise extrapolation is **1.5-2.8 mag too optimistic**, as Bamford et al. found (resampling-induced
  pixel correlations plus real large-scale structure).
- Wide-survey I_E 28.2-28.3 is consistent with (slightly deeper than) the Q1 value 27.8 of Bamford et al.; H_E 27.0
  is ~0.6 mag deeper than their 26.4 (EDF-S position, different estimator details).
- Deep vs wide gain: +0.8 mag (I_E) and +0.9 mag (H_E), i.e. less than the sqrt(10) = 1.25 mag expected for pure
  photon noise: structure on 10" scales already contributes.
- In the 3'-4' annulus the BGMOD level is slightly **negative** (|level| ~ 29-29.6 mag/arcsec^2 in I_E, ~28.5-28.7 in
  H_E): the pre-MER mosaic (after per-exposure sky subtraction) sits slightly below zero around the galaxy,
  consistent with the mild per-exposure over-subtraction near sources reported by McCracken+26; MER lifts it back.
  Azimuthal scatter of our own sky between 8 sectors: 30.5 (wide I_E) to 31.7 (deep I_E) mag/arcsec^2.

Take-away for NGC 1483-like galaxies: for profiles fainter than ~26 mag/arcsec^2 or radii beyond ~1', restore BGMOD
and re-derive the sky; the MER-delivered mosaics under-estimate the outer disc light by tens of per cent. The
per-exposure sky subtraction (not undone here) may remove more on even larger scales.

## 8. Lessons from the Euclid cluster/ICL team (transferable to galaxy haloes)

- Sky at the 1-Mpc scale, sources masked in two zones (+50% outside, +25% inside the diffuse region), profile fitter
  background fixed to zero (Kolcu, Gully).
- AutoProf elliptical isophotes with regularised ellipticity/PA, log-spaced radii (0.15 dex), shape frozen beyond the
  last reliable radius (Kolcu).
- Band choice: H_E (or summed YJH) reaches furthest at z > 0.2; I_E is better only at z < 0.2; Y_E is worst (zodiacal
  light) (Kolcu).
- Interpolate component fluxes to a common rest-frame band; band choice alone changes ICL fractions by ~15% (Gully).
- PSF-wing deconvolution changes 50-200 kpc fluxes by < 1% for clusters (Gully); for small galaxies the PSF wing
  matters more.
- Masking biases shapes: mask-defined diffuse light is more elliptical (0.43) than truly unbound light (0.24) in
  simulations: forward-model your masks (Kolcu).
- Errors from blank-sky random apertures with covariance plus mock injection into real Euclid sky (all three papers).
- Low-S/N selection effects and mis-centred BCGs can mimic redshift evolution (Gully).

## 9. Lessons from resolved LSB dwarfs (Gatto et al.)

- Selection from the MER catalogue: `POINT_LIKE_PROB > 0.05` plus an I_E-H_E / Y_E-H_E colour polygon matched to old
  RGB isochrones; vetting on VIS stacks; characterisation with own PSF-fitting photometry (MER catalogue is weaker in
  crowded fields).
- Recovery: 88% of known dwarfs, but only ~55% of faint dwarfs beyond 3.6 Mpc.
- Fifteen new or newly resolved systems from 20 kpc to 5.5 Mpc (see [12_galaxy_examples.md](12_galaxy_examples.md)).

## 10. Open items to verify for your own data

- Whether a given DR1 tile used NoiseChisel or the SExtractor fallback in a quadrant/detector containing your galaxy
  (not stored in the products; compare `BKG` maps of the calibrated frames with the galaxy footprint).
- The `BGMOD` around your target: a negative "dip" or ring indicates the MER step absorbed galaxy light.
- Whether the target lies in a tile with incomplete NIR coverage (solar-proton events; `FILLING_FACTOR`, layer files).
- Whether bright stars (G < 14) within ~2' contribute ghosts or arcs.
