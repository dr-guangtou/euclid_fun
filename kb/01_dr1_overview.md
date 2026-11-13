# Euclid DR1: what was released

> Key points
> - **DR1-Foundation** went public on **2026-11-12**: all complete raw data (LE1) to 2025-05-21 plus validated LE2
>   images, catalogues and spectra, ~1900 deg^2 of the Euclid Wide Survey (EWS) and 77 deg^2 of Deep Fields.
> - The **full DR1** (mid-2027) adds only shear catalogues and LE3 cosmology products; DR1-Foundation products are
>   **not reprocessed** then. DR2 (~3 years of survey) is planned for 2029.
> - About 1 billion catalogued objects, of which more than 900 million are galaxies (`PHZ_CLASSIFICATION = 2`); more
>   than 160 million 1-D spectra (H_E < 23.5); 1.7 PB.
> - Imaging: VIS I_E (0.1"/px, PSF FWHM ~0.16-0.21") and NISP Y_E, J_E, H_E (0.3"/px native, ~0.45-0.56" FWHM),
>   plus ground-based ugriz (UNIONS north, DES south, HSC/DECam/Pan-STARRS in deep fields) resampled onto the MER
>   tile grid. Single-visit EWS 5-sigma point-source depth ~25.7 (I_E), ~24.2-24.3 (YJH) AB.

Sources: [Aussel+26](papers/aussel.md) (overview), [Tereno+26](papers/tereno.md) (surveys), the ESA DR1 memo
EUCL-EST-ME-8-020 (`~/Desktop/euclid/docs/DR1-memo_260922.pdf`), the archive's list of supported products
EUCL-ESAC-RP-8-017 v42, ESA pages (`~/Desktop/euclid/text/web/`), [Kuemmel+26](papers/kuemmel.md),
[Odier+26](papers/odier.md).

## 1. Timeline

| Date | Event |
|---|---|
| 2023-07-01 | Launch; commissioning, then performance verification (PV) from 2023-08-01 |
| 2023-12 | Phase-diversity calibration (PDC) campaign; thermal-stabilisation periods used for EMDS, ILS, SSO science |
| 2024-02-14 | Start of the nominal survey |
| 2024-03-14 / 2024-06-08 | Decontaminations ("ice age"); VIS data 2024-03-23 to 2024-06-07 declared invalid, area partly re-observed |
| 2024-05-23 | Early Release Observations (ERO) public |
| 2025-03-19 | Quick release Q1 (one visit of each Deep Field, 63 deg^2) |
| 2025-05-21 | End of the DR1 data-taking period |
| 2026-06-24 | Q2 (Galactic bulge) public; not part of DR1 |
| **2026-11-12** | **DR1-Foundation public** (this knowledge base) |
| early 2027 | Euclid Ultra-Deep Field (EUDF, self-calibration field) planned |
| mid-2027 | Full DR1: shear catalogues, LE3 weak-lensing and clustering products, visibility mask, random catalogues |
| 2029 / early 2030s | DR2 / DR3 |

## 2. Data sets in DR1-Foundation

| Data set | Area (VIS) | Depth / visits | MER processing | Notes |
|---|---|---|---|---|
| EWS (Euclid Wide Survey) | 2092 deg^2 VIS, 1975 deg^2 VIS+NISP; ~1900 deg^2 validated with ground data | 1 ROS (4 dithers), 14% mean tile overlap | Wide (32' tiles, `102...`) | north ~500 deg^2 (UNIONS), south ~1400 deg^2 (DES) |
| EDF-North (269.733, +66.02) | 24.3 deg^2 deep | 11 visits (8 red, 3 blue grism) | Deep (17' tiles, `101...`) + wide-like per visit | no EWS under EDF-N |
| EDF-South (61.241, -48.42) | 27.8 deg^2 deep | 10 visits | Deep + wide-like | also covered by EWS |
| EDF-Fornax (52.932, -28.09) | 13.1 deg^2 | 2 visits | Deep + wide-like | contains CDFS |
| EAFs: COSMOS (150.120, +2.21), CDFS (53.118, -27.81), AEGIS (214.827, +52.82) | 4.8 deg^2 total | 27 / 34 / 18 visits | Deep + wide (AEGIS: VIS+NIR only, no EXT) | photo-z and colour-gradient calibration |
| SelfCal (268.813, +65.29) | ~2 deg^2 | 11 F-001 visits (76 dithers each) | Wide | basis of the future EUDF |
| EMDS-1..4 (PDC science) | 13-16 deg^2 each | ~1 mag deeper than EWS | VIS+NIR (EMDS-3/4); EMDS-1/2 VIS only, no MER | overlap HSC-SSP fields |
| ILS-WAVES-S (355.7, -31.2), SSO, F010, F014 | 2-38 deg^2 | wide-like | VIS+NIR | ILS chosen partly for LSB dwarf work |
| PSF fields (CALBLOCK-F-008) | 6.3 deg^2 | 100 short dithers | none | VIS only |

Sky distribution and exclusions (Tereno+26): from 2639 deg^2 scheduled EWS to 2099 deg^2 of complete LE1 and ~1900
deg^2 of validated LE2. Losses come from the ice age (147 deg^2 not re-observed in time), missing ground-based data
(302 deg^2), instrument outages, unexecuted observations, solar radiation events and **tiles crossing RA = 0 h (not
processable in DR1)**.

## 3. Products (DR1-Foundation)

Level 1 (raw): VIS and NISP raw frames for all complete observations (including calibration and PV blocks).
Housekeeping telemetry comes with full DR1.

Level 2 (per processing function; detailed data model in [02_data_model.md](02_data_model.md)):

| PF | Products | Archive tables |
|---|---|---|
| VIS | calibrated quad frames (+ background map, weight map, PSF model), stacked frames (+ weight, PSF), catalogues | `dr1.calibrated_frame`, `dr1.aux_calibrated`, `dr1.observation_stack`, `dr1.aux_stacked`, `dr1.frame_catalog` |
| NIR | calibrated frames (+ background, PSFs), stacked frames (new in DR1, microJy), catalogues | same tables |
| SIR | science frames (2-D spectrograms), combined 1-D spectra | `dr1.sir_science_frame`, `dr1.spectra_source*`, `dr1.combined_spectra*` |
| MER | background-subtracted mosaics + RMS, FLAG, BGMOD, PSFs, star masks, layer files, filter curves; segmentation maps; final catalogue (+ morphology, cutouts, deep photometry) | `dr1.mosaic_product`, `dr1.aux_mosaic`, `dr1.mer_segmentation_map`, `dr1.mer_catalogue_<group>`, `dr1.mer_morphology_<group>`, `dr1.mer_cutouts_<group>`, `dr1.mer_final_catalogue` |
| PHZ | photo-z + PDFs, classification, galaxy/star SEDs, physical parameters (galaxy, NIR-based, QSO), star templates; deep-tile catalogue | `dr1.phz_*_<group>` |
| SPE | redshifts, classification, line features, model parameters | `dr1.spectro_*_<group>` |
| VMPZ-ID (LE3 treated as LE2) | HEALPix bit mask, coverage, effective coverage, footprint, depth and information maps | `dr1.vmpz_healpix_*` |

Not in DR1-Foundation: shear (SHE) catalogues and bias parameters, LE3 science products, the visibility mask and
random catalogues (all full DR1), EXT stacked frames as separate products, special large-object MER tiles (designed
but not processed), software ("no software will be made available by the SGS").

Catalogue groups (`<group>` suffix; row counts from the archive help): `wide_survey` 888 152 165 (cosmological EWS),
`wide_mode` 58 488 372 (wide-like observations not in the EWS: SelfCal, EMDS, ecliptic, calibration fields),
`deep_survey` 51 820 952 (EDF deep stacks), `deep_mode` 4 719 299 (COSMOS, CDFS deep), `deep_visits` 252 948 682
(every individual EDF visit). PHZ/SPE/SIR use `wide`, `wide_survey`, `deep`, `deep_visits` combinations.

## 4. Depth and image quality (EWS medians)

| Band | Pixel (native -> MER) | PSF FWHM | 5-sigma depth (2" aperture) | Typical exposure |
|---|---|---|---|---|
| I_E (VIS, 550-900 nm) | 0.1" -> 0.1" | 0.203" in MER (0.14-0.16" native VIS PSF core) | 25.69 | 4 x 565 s (+2 short), MER median 2274 s |
| Y_E | 0.3" -> 0.1" | 0.488" | 24.14 | 4 x 87 s, MER median 314 s |
| J_E | 0.3" -> 0.1" | 0.514" | 24.30 | 4 x 87 s |
| H_E | 0.3" -> 0.1" | 0.559" | 24.29 | 4 x 87 s |

Deep fields: EDF-N and EDF-S I_E exposure ~20 ks per tile (about 1.2-1.3 mag deeper than EWS), COSMOS 52 ks.
Surface-brightness limits are discussed in [10_low_surface_brightness.md](10_low_surface_brightness.md).

## 5. Pipeline versions frozen for DR1 (Aussel+26)

MER 11.3.1, VIS 18.0.4, NIR 6.1.2 (see [Ruffenach+26](papers/ruffenach.md) Table E.1 for the full list).

## 6. Licence, acknowledgement, DOI

- Data released under CC BY-NC 3.0 IGO.
- Acknowledgement text (Explanatory Supplement): "This work has made use of data from the European Space Agency (ESA)
  mission Euclid (https://www.cosmos.esa.int/euclid), processed by the Euclid Consortium (https://www.euclid-ec.org/)."
- ESA DR1 DOI 10.57780/esa-d079c51 (quoted in Kuemmel+26). Cite the DR1 papers relevant to the products used and,
  for Datalabs, Navarro et al. 2024.
