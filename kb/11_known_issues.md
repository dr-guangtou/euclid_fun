# Known issues, caveats and documentation discrepancies (DR1-Foundation)

Collected from the Explanatory Supplement release notes ([expsup](expsup/README.md)), the Euclid Data Space
known-issue pages ([web](web/README.md)), the DR1/Q1 papers ([papers/](papers/)), the DPDD notes
([data_model/](data_model/)) and our own tests ([verified](data_model/verified_on_archive.md), `demo/`).
Severity for extended-galaxy work: **H** high, **M** medium, **L** low.

## 1. Imaging and background

| Sev. | Issue | Impact | Workaround | Source |
|---|---|---|---|---|
| H | LSB light "mostly filtered out at the MER stage": per-exposure sky (VIS NoiseChisel per quadrant, NIR NoiseChisel per detector) + MER 25.6"/76.8" mesh | outskirts, haloes, tidal features, ICL; Kron/Sersic fluxes of large galaxies biased low | restore BGMOD (VIS, < ~1'); rebuild from calibrated frames otherwise | Expsup 15.2.2; Bamford+26; [10](10_low_surface_brightness.md) |
| H | No special tiles for 164 526 objects > 2'; large galaxies may cross tile edges | truncated galaxies, edge effects | mosaic neighbouring tiles yourself | Kuemmel+26 |
| M | VIS sky slightly over-subtracted near sources; inner over-subtraction for objects larger than a quadrant (3.4') | negative sky around bright galaxies | own sky from calibrated frames | McCracken+26, Q1 McCracken |
| M | Unmasked VIS ghosts (dichroic ghost ~70" from G <~ 14 stars) and serial-register bleeding | spurious diffuse sources/detections | mask around bright stars | McCracken+26, Schirmer+26 |
| M | NIR persistence masked, not corrected (~5% of pixels); persistence-like structure in master background; 1/f row/column striping (DR2) | NIR diffuse structure, holes in large galaxies | avoid PERSIST pixels; Bamford corrections | Polenta+26, Kubik+26 |
| M | VIS stray light 10-15% of zodiacal, attitude- and detector-dependent, +14%/yr | large-scale sky structure | local/attitude-matched backgrounds | Schirmer+26 spacecraft |
| M | VIS shutter gradient (0.8%, 4.7% for short exposures) not corrected until DR2 | low-level gradients | exclude short exposures in LSB stacks | Schirmer+26 calibration |
| M | Incomplete NIR coverage in some tiles (solar proton events); zero-filled areas | missing bands, noisy borders | check `FILLING_FACTOR`, layer files | Kuemmel+26 |
| M | Mosaic `fov` polygons larger than the data (zeros at the target), e.g. PGC 61126 in the wide mosaic of tile 102158273 | empty cutouts | check cutouts; use deep products in EDFs | EDS help; verified |
| L | Duplicate mosaic files for a few tiles in one release | ambiguity | newest `creation_date` | verified |
| L | VIS skypatches 39 (EDS) and 40 (EWS) have poor distortion models (up to 23 mas) | astrometry | check | McCracken+26 |
| L | 0.7% of the NIR area has astrometric errors > 50 mas | NIR-VIS misalignment, colours | VMPZ info map | Expsup 15.2.3, Radovich+26 |
| L | Pan-STARRS flags mishandled; degraded PS1 i photometry in places; PS1 PSF > 5" (stamp sum 0.88) | EXT photometry in the north | VMPZ map; avoid PS1 | Expsup 15.2.4, Corcho-Caballero+26 |
| L | HSC r and i in deep fields have almost no validity | use HSC r2/i2 | | Corcho-Caballero+26 |
| L | Ice-age period (2024-03-23 to 06-07) excluded; residual VIS throughput drift ~0.2 mmag/month; NISP QE drift (Y worst) | calibration epochs | | Schirmer+26 |

## 2. PSF

| Sev. | Issue | Source |
|---|---|---|
| M | MER PSF stamps not renormalised in DR1 (I_E stamp sum median ~0.958): model fluxes differ by 1/S from Q1; "not best for large extended sources" | Kuemmel+26; verified |
| M | PSF stamps are small: VIS GRID-PSF 21x21 px (2.1"), NIR catalogue PSF 45x45 px (4.5") (paper says <= 5"); NISP models cover <= 3" (stack) / 7" (single), 1-2% of light beyond 7"; no scattered-light wings | verified; [05_psf](05_psf.md), da Silva+26 |
| L | VIS PSF model too small for shear (cosmology issue); NIR brighter-fatter uncorrected | Aussel+26, da Silva+26 |

## 3. MER catalogue

| Sev. | Issue | Impact | Workaround | Source |
|---|---|---|---|---|
| H | Large nearby galaxies shredded. NGC 1483: wide = 6 pieces of one parent + 525 excess entries in 40"-100" (+58%); deep = 38 pieces + 1244 excess (+75%, out to ~140"). No column isolates fragments: `SPURIOUS_PROB > 0.7` flags 23% of them, `> 0.7` or NIR-only flags 76% but also 24% of real field sources | wrong counts, colours, morphology near big galaxies | mask the galaxy region (bit 512 / own isophote); statistical background correction; own photometry | verified (demo 07; [06 §10.1](06_catalogues_photometry_morphology.md)) |
| M | `BLENDED_PROB`, `EXTENDED_PROB`, `EXTENDED_FLAG`, `SHE_FLAG` are 100% NULL; `POINT_LIKE_PROB` NaN for NIR-only and bright (I_E < 16.5) entries | blending/extendedness cannot be selected on | `DEBLENDED_FLAG`, `PARENT_ID`, `MUMAX_MINUS_MAG` | verified (tile 102021980) |
| M | Bright-star haloes and detector artefacts are catalogued as multi-piece "galaxies" (17-entry family around a saturated star in tile 102021980) | spurious extended objects | check families with large summed area against stars/images | verified |
| L | `PARENT_ID` is a tile-local detection number | wrong families when matching across tiles | match on (`tile_index`, `parent_id`) | verified |
| H | Disk+Sersic (bulge/disc) columns present but empty; `t_type` empty | no B/D decompositions in DR1 | fit yourself | verified |
| H | `DET_QUALITY_FLAG` bit 512 (inside an extended-object area) is set on practically all fragments of large nearby galaxies: common cuts (`= 0`, `< 4`) remove the galaxy entirely | selection of nearby galaxies | use bit 512 to identify them; re-measure from mosaics | [06](06_catalogues_photometry_morphology.md) (measured) |
| M | Sersic fits in bands without data contain the initial guesses, not NaN | fake NIR/EXT Sersic values in partial tiles | helpdesk `bad_objects.py` | Expsup 15.3.3 |
| M | `FLUX_RADIUS` restricted to the segmentation area (DR1 version), biased low for extended sources | sizes | use Sersic R_e or own growth curves | Expsup 15.3.5 (Kuemmel+26 describes the intended SE++-like version) |
| M | Over-deblending in wide, under-deblending in deep | inflated fluxes for blended big galaxies (worst in A-PHOT) | `DEBLENDED_FLAG`, visual checks | Kuemmel+26, Gasparetto+26 |
| M | Sersic n pile-up at the n = 8 limit; n unreliable vs HST (scatter ~0.6); R_e scatter ~16%, q ~7% at I_E 24-24.5 | | treat n ~ 8 as failed; use I_E < 23 | Kuemmel+26, Dunn+26, verified |
| M | T-PHOT bugs (recentring sign; numpy/FITS axis swap of PSFs/kernels) | mainly point sources; PSF-fit fluxes ~0.13 mag off | prefer A-PHOT/Sersic for stars; fine for galaxies | Expsup 15.3.2 |
| L | Wrong worst-PSF assignment in partially covered tiles | noisier aperture colours | | Expsup 15.3.4 |
| L | Duplicate sources at tile borders (1e-5) | | de-duplicate by position | Expsup 15.3.7 |
| L | `SPURIOUS_FLAG` at 0.5 too aggressive | | use `SPURIOUS_PROB > 0.7` | Kuemmel+26 |
| L | Bright-star masks cover only cores/spikes (1-5% of area); no halo masks | | Gaia-based halo masks | Kuemmel+26, Odier+26 |
| L | Coordinates epoch not stored in the table (tile XML `ReferenceObservationDateTime`); `EQUINOX` meaningless | proper-motion work | | EDS help |
| L | `gaia_id` is Gaia DR3 | | | EDS help |

## 4. Photo-z, physical parameters, spectra

| Sev. | Issue | Source |
|---|---|---|
| H | PHZ reference sample (COSMOS) lacks z < 0.2 and very massive galaxies: masses biased low there; aperture-based (2FWHM) fluxes scaled to total, not total light of extended galaxies | Hartley+26, Enia+26 ([07](07_photoz_physical_parameters.md)) |
| M | North without u band: more outliers (+5 points), +20% scatter; deep-field zPDF configuration error | Hartley+26 |
| H | `phys_param_flags = 1` for 251 of 256 galaxies with I_E < 18 (tile 102021980): the usual `PHYS_PARAM_FLAGS = 0` cut removes almost all bright, nearby galaxies; `phz_flags` are decimal codes (0, 1, 10, 11, 12), not bits | [07](07_photoz_physical_parameters.md) (checked) |
| H | SPE optimised for H-alpha at 0.84 < z < 1.88: only 40-60% correct at 0.1 < z < 0.84 and < 10% at z < 0.1 (wide) | Le Brun+26 ([08](08_spectroscopy.md)) |
| H | Spectra of fragments of nearby galaxies are contaminated and can carry absurd SPE redshifts with `spe_z_prob` ~ 1 (NGC 1483 disc fragment: z = 4.59) | verified (demo 04) |
| M | Spectral `MASK` bits LOW_SNR (2) and EXT_PRB (4) cover long ranges even for bright galaxies; DPDD calls them "bit positions" but they are values | verified; DPDD |
| M | Several spectra per `object_id` (SelfCal, COSMOS repeats, CDFS in EDF-F) | EDS help |
| L | SPE incomplete in 14 edge tiles | EDS help |
| L | Quiescent galaxies and type-2 AGN can be classified as QSO by SPE | Le Brun+26 |

## 5. Archive, services and documentation

| Issue | Status / workaround | Source |
|---|---|---|
| astroquery 0.4.11 (PyPI) not DR1-ready | install from GitHub main | verified |
| `schema='sedm'` / `release=sedm` defaults -> HTTP 401 for DR1 files | use `dr1` | verified |
| SIA returns no DR1 products (release day) | ADQL on `dr1.mosaic_product.fov` | verified |
| Cutout service fails for BGMOD/RMS (`CTYPE1 not found`) | row-range read of the tile file (`dr1_access.remote_rows_cutout`: ~46 MB for 1', pixel-identical) or download full files | verified |
| `dr1.calibrated_detectors` cannot locate detectors: NIR only, one `crval` per frame, `crpix1` = `crpix2`, `observation_id` NULL | focal-plane model from one exposure's headers (`demo/09`) | verified |
| Cutout service sometimes returns HTTP 200 with a non-FITS body | retry | verified |
| Cutout headers lack `MAGZERO` | use `zero_point` column | verified |
| `phz_classification` TAP description swapped (actual: 1 star, 2 galaxy) | | verified vs DPDD |
| DPDD: MER flux unit printed as "mJy" but ZP 23.9 (microJy); `FLUX_SEGMENTATION`/`FLUX_DETECTION_TOTAL` descriptions shifted by one row; Sersic flag values printed 2028/4056 (likely 2048/4096) | trust the archive units (uJy) | [dpdd_mer](data_model/dpdd_mer.md) |
| DPDD lists stacked frames as "missing"/not described, but stacks are in the archive (`dr1.observation_stack`) | | dpdd_vis_nir vs verified |
| NULLs stored as NaN or -99 | `NULLIF(col, 'NaN')` | EDS help |
| Help-page bulk-download example uses `release=sedm` (Q1) | use `dr1` | EDS help |
| Raw server error messages echo account name/e-mail/IP | do not log them | verified |
| DR1 SIR paper (Scodeggio et al.) linked from the Supplement is not yet public (404) | | verified |
| IRSA does not list DR1 yet (2026-11-12) | ESA archive | verified |

## 6. Inconsistencies between papers (for the record)

- Q1 NIR PSFs vs Gaia: "1.75-3.5% too compact" (Romelli+25 table) vs "too large" (Kuemmel+26 text).
- VIS PSF FWHM quoted as 0.14" (McCracken+26), 0.158" (Q1), 0.16" (Dunn, Nightingale), 0.20-0.21" (MER mosaics,
  includes resampling): different processing stages.
- Decontamination dates differ slightly between papers (e.g. 2024-03-14 vs 03-12/21, 2024-06-08 vs 06-12; one typo
  "2026-06-08" in Schirmer+26 spacecraft).
- Holloway+26 quotes lens completeness 0.73/0.34 vs Lines+26 0.81/0.43.

## Added 2026-11-14 (UCD pilot)

- **A tile can have mosaics but no catalogue rows.** Example: tile 102035564 next to NGC 1399. Footprints built from
  tile polygons (including the MOCs of demo 08) are upper limits; test coverage with the catalogue itself. Details:
  [verified_on_archive.md](data_model/verified_on_archive.md).
- **No catalogue entries in the core of a giant elliptical** (about 1.5 arcmin around NGC 1399), in addition to the
  shredding of large galaxies described above.
- **Multi-table cone joins are very slow** on the Euclid TAP; fetch the catalogue by cone and the rest by id lists.
- **ESA Gaia archive rate limit** (HTTP 429) for anonymous bulk queries; use the NOIRLab Data Lab copy.
