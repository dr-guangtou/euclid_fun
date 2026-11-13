# DR1 data model: products, files, tables, keys

> Key points
> - Three processing levels: LE1 raw frames; LE2 per-PF products (VIS, NIR, SIR, MER, PHZ, SPE) and VMPZ-ID HEALPix
>   maps; LE3 cosmology products (full DR1, 2027).
> - Imaging users mostly need **MER tiles**: a background-subtracted mosaic per band on a common 0.1"/px grid with
>   RMS, FLAG, BGMOD (subtracted sky), PSF (grid + per-object), bright-star masks and layer files; plus the
>   **MER catalogue** (photometry, morphology, cutout geometry) which is the parent of all other catalogues via
>   `object_id`.
> - Pixel units: VIS `ADU/s` (ZP 24.5), NISP `ELECTRON/s` (ZP 29.8/30.1/30.0 for Y/J/H), EXT ZP 30; catalogue fluxes
>   in microJy (ZP 23.9).
> - Details: [verified_on_archive](data_model/verified_on_archive.md) (hands-on facts),
>   [dpdd_mer](data_model/dpdd_mer.md), [dpdd_vis_nir](data_model/dpdd_vis_nir.md),
>   [dpdd_phz](data_model/dpdd_phz.md), [dpdd_spectroscopy](data_model/dpdd_spectroscopy.md),
>   [dpdd_masks_vmpz](data_model/dpdd_masks_vmpz.md), [dpdd_ext_archive](data_model/dpdd_ext_archive.md),
>   column-level TAP dump [tap/README](data_model/tap/README.md) (134 tables, 8447 columns).

## 1. Product tree

```
LE1  DpdVisRawFrame, DpdNispRawFrame                        (dr1.raw_frame, raw_detector, raw_quadrant)
LE2  VIS  DpdVisCalibratedQuadFrame  -> DET (144 quadrants x SCI/RMS/FLG), BKG, WGT, PSF, SCI-PERI json
          DpdVisStackedFrame         -> STK, WGT, PSF   (per observation; background already subtracted)
          DpdVis{Calibrated,Stacked}FrameCatalog
     NIR  DpdNirCalibratedFrame      -> CAL (16 detectors x SCI/RMS/DQ), BKG (same layout), CAL-PSF-I/M, GLOBAL-PSF-I/M
          DpdNirStackedFrame         -> STK (SCI/RMS/FLG, microJy), PSF-I, PSF-M
          DpdNir{Calibrated,Stacked}FrameCatalog
     SIR  DpdSirScienceFrame (48 ext: 16 x SCI/VAR/DQ), DpdSirCombinedSpectra (<= 1000 1-D spectra per file)
     MER  DpdMerBksMosaic            -> BGSUB-MOSAIC, RMS, FLAG, BGMOD, CATALOG-PSF, GRID-PSF, STAR-MASKS (json),
                                        DETECTOR-LAYERING, FILTER-TRANSMISSION (EXT)
          DpdMerSegmentationMap      -> SEGMAP
          DpdMerFinalCatalog         -> FINAL-CAT, FINAL-MORPH-CAT, FINAL-CUTOUTS-CAT, (deep) FINAL-DEEP-CAT
     PHZ  DpdPhzPfOutputCatalog (photo-z + PDF, galaxy/star SED), DpdPhzPfOutputForL3 (classification, physical
          parameters, NIR physical parameters, QSO parameters, star template), DpdPhzDeepOutputCatalog
     SPE  DpdSpePfOutputCatalog (redshift: classification, galaxy/QSO/star candidates, quality; models; line features)
LE3* VMPZ-ID HEALPix: bit mask, coverage, effective coverage, footprint, depth map, information maps
```

## 2. Identifiers and keys

| Key | Where | Meaning |
|---|---|---|
| `object_id` (int64) | all catalogue tables (`source_id` in `spectra_source_*`) | MER source ID; encodes the position (~3.6 mas resolution); identical across MER/PHZ/SPE/SIR. Deep visits: the same object usually gets a different ID per visit |
| `tile_index` | mosaics, catalogues | 9 digits: `102...` wide 32' tiles, `101...` deep 17' tiles, `1025...` special tiles (none in DR1) |
| `segmentation_map_id` | MER catalogue | tile index + running number; pixel value in SEGMAP |
| `mosaic_product_oid` | `dr1.mosaic_product` -> `dr1.aux_mosaic` | archive key linking a mosaic to its auxiliary files |
| `observation_id`, `patch_id` | frames, stacks | ROS observation (4 dithers) and survey patch |
| `calibrated_frame_oid` / `observation_stack_oid` | frames/stacks -> `aux_calibrated` / `aux_stacked` | archive keys |
| `basic_download_data_oid` | catalogue tables | archive-internal, links rows to the catalogue FITS files in `dr1.basic_download_data` / `dr1.mer_final_catalogue` |
| `data_set_release_part1..3` | most tables | release triplet; part 3 = version (1 = `DR1_R1`, 2 = `DR1_R2`) |

## 3. Archive table families (`dr1` schema)

| Family | Tables | Notes |
|---|---|---|
| MER mosaics | `mosaic_product`, `aux_mosaic`, `mer_segmentation_map` | select by `release_name`, `purpose`, `processing_mode` (see [03_data_access](03_data_access.md)) |
| MER catalogues | `mer_catalogue_<g>` (478 cols, only ones with coordinates), `mer_morphology_<g>` (113), `mer_cutouts_<g>` (32), `mer_catalogue_<deep>_photometry` (721) | `<g>` = `wide_survey`, `wide_mode`, `deep_survey`, `deep_mode`, `deep_visits` |
| PHZ | `phz_photo_z_<g>`, `phz_classification_<g>`, `phz_physical_parameters_<g>`, `phz_nir_physical_parameters_<g>`, `phz_qso_physical_parameters_<g>`, `phz_galaxy_sed_<g>`, `phz_star_sed_<g>`, `phz_star_template_<g>`, `phz_catalogue*` | `<g>` = `wide`, `deep_survey`, `deep_mode`, `deep_visits` |
| SPE | `spectro_z_spe_{classification,galaxy_candidates,qso_candidates,star_candidates,quality}_<g>`, `spectro_model_spe_*`, `spectro_line_features_spe_*`, `spe_catalogue` | `<g>` = `wide`, `wide_survey`, `deep`, `deep_visits`; several rows per object: use `spe_rank = 0` |
| SIR | `spectra_source[_<g>]`, `combined_spectra`, `combined_spectra_product`, `sir_science_frame`, `sir_frame_detectors` | |
| Frames | `raw_*`, `calibrated_frame`, `calibrated_detectors`, `aux_calibrated`, `observation_stack`, `aux_stacked`, `frame_catalog`, `aux_common` | |
| Masks | `vmpz_healpix_{bitmask,coverage,effective_coverage,footprint_mask,depthmap,infomap}` | HEALPix Nside 16384 (12.9"), nested |
| Bookkeeping | `data_release`, `instrument`, `observation_mode`, `provenance`, `files_table`, `column_values`, `basic_download_data`, `ivoa.obscore` | |

## 4. Units and photometric conventions

| Quantity | Unit | Conversion |
|---|---|---|
| MER VIS pixel | ADU/s | m = 24.5 - 2.5 log10(I); mu = 19.5 - 2.5 log10(I) |
| MER NISP pixel | electron/s | Y: m = 29.8 - 2.5 log10(I); J 30.1; H 30.0 (mu = ZP - 5 - 2.5 log10 I) |
| MER EXT pixel | scaled counts | ZP 30.0 |
| VIS calibrated frame | ADU (not per second) | m = ZP_frame - 2.5 log10(ADU) + 2.5 log10(EXPTIME) (DPDD; ZP ~24.57, gain ~3.48 e-/ADU in Q1) |
| NIR calibrated frame | electrons | inverse sensitivity in microJy per e-/s in the header |
| NIR stack | microJy | |
| Catalogue fluxes | microJy | m = 23.9 - 2.5 log10(F) |
| Sersic radii (morphology) | arcsec | `sersic_sersic_vis_radius` |
| `flux_radius`, `semimajor_axis`, `kron_radius` | pixels (0.1") | |
| Spectra | 1e-16 erg/s/cm^2/A (FSCALE applied) | wavelength in Angstrom, 13.4 A bins |

Extinction: `gal_ebv` (Planck) in the MER catalogue and VMPZ extinction maps. All magnitudes AB.

## 5. What is *not* there (or is empty) in DR1-Foundation

- Disk+Sersic (bulge/disc) fit columns exist but are NaN; `t_type` NaN.
- Special large-object MER tiles (prefix `1025`) were not processed.
- EXT ground-based stacks are not distributed as products (only resampled inside MER tiles).
- SHE shear catalogues, LE3 products, visibility masks, random catalogues: full DR1 (2027).
- No LSB-optimised mosaics (planned for later via Datalabs).
- No SGS software.
