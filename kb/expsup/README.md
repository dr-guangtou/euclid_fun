# Euclid Explanatory Supplement, DR1-Foundation (documentation release 1)

Online: https://euclid.esac.esa.int/dr/dr1/expsup/ (LaTeXML HTML; "updated regularly in the coming weeks").
Local mirror: `~/Desktop/euclid/expsup_mirror/`; plain text: `~/Desktop/euclid/text/expsup/*.md` (76 pages, ~11.5k words).

## What it is

A thin user guide: most chapters are one-paragraph pointers to the DR1 (and Q1) papers and to DPDD product cards.
The substantive, user-facing content is in **Chapter 15 (Release notes)**, Chapter 16 (Science Archive) and
Chapter 17 (ESA Datalabs). Several sections are still "TBI" (PDC science data).

## Structure and pointers

| Chapter | Content | Points to |
|---|---|---|
| 1-4 | mission, VIS, NISP, surveys (EWS, EDS, PDC, calibration observations) | Euclid I (arXiv:2405.13491), [Tereno+26](../papers/tereno.md), [Schirmer+26 calibration](../papers/schirmer-calibration.md) |
| 5 | processing overview | [Aussel+26](../papers/aussel.md) |
| 6 | VIS: calibrated quad frames, calibrated catalogue | Q1 McCracken ([q1_mccracken_vis](../papers/q1_mccracken_vis.md)) + DR1 [McCracken+26](../papers/mccracken.md) |
| 7 | NIR: calibrated frames + catalogue | Q1 Polenta ([q1_polenta_nir](../papers/q1_polenta_nir.md)), DR1 [Polenta+26](../papers/polenta.md), [Radovich+26](../papers/radovich.md), [da Silva+26](../papers/dasilva.md), [Kubik+26](../papers/kubik.md) |
| 8 | EXT: "No EXT product is distributed with DR1-Foundation" (stacks are only used inside MER) | [Corcho-Caballero+26](../papers/corcho-caballero.md) |
| 9 | MER: BGSUB mosaic, final catalogue, segmentation map; Photometry and Morphology Cookbooks (in the DPDD) | Q1 Romelli ([q1_romelli_mer](../papers/q1_romelli_mer.md)), DR1 [Kuemmel+26](../papers/kuemmel.md), [Gasparetto+26](../papers/gasparetto.md) |
| 10 | PHZ: WL, LE3 and deep-tile output catalogues | Q1 Tucci et al., [Hartley+26](../papers/hartley.md), [Enia+26](../papers/enia.md) |
| 11 | SIR: science frames, combined spectra | Q1 Copin et al., DR1 Scodeggio et al. (`dr1/scodeggio.pdf`, **not yet public**: 404 on 2026-11-12), [Fumana+26](../papers/fumana.md) |
| 12 | SPE: output catalogue | Q1 Le Brun et al., DR1 [Le Brun+26](../papers/lebrun.md) |
| 13 | VMPZ-ID HEALPix maps | [Odier+26](../papers/odier.md) |
| 14 | calibration products | [Schirmer+26](../papers/schirmer-calibration.md) |
| 15 | **Release notes**: content, known issues, MER release notes | below |
| 16 | Science Archive System / Euclid Data Space | [../03_data_access.md](../03_data_access.md) |
| 17 | ESA Datalabs | [../03_data_access.md](../03_data_access.md) |
| Appendix | credit and citation | acknowledgement sentence (see [../01_dr1_overview.md](../01_dr1_overview.md)) |

## Chapter 15: release notes (essential)

**15.2 Known issues and limitations** ("data processing is not yet fully mature")
- 15.2.1 Slitless spectroscopy: heading only (no text yet).
- **15.2.2 Low-surface-brightness features**: SGS optimised for z > 0.5, arcsecond-sized galaxies; VIS and NIR PFs try
  to preserve LSB features but they are "mostly filtered out at the MER stage when the stacks are being built".
  Consortium groups (ICL, local galaxies, cirrus) are building alternative products from the calibrated frames, to be
  served later via Datalabs, not in time for DR1-Foundation. -> [../10_low_surface_brightness.md](../10_low_surface_brightness.md)
- 15.2.3 NIR astrometry: 0.7% of the DR1 area has errors > 50 mas; a VMPZ-ID HEALPix information map traces it.
- 15.2.4 EXT Pan-STARRS: wrong handling of Pan-STARRS flags by the SGS degraded photometry in some areas; VMPZ-ID map.

**15.3 MER release notes**
- 15.3.1 Overview FITS tables per field (EWS, EDF-F/N/S, COSMOS, CDFS, AEGIS, SELFCAL, F-014, ILS, SSO, HSC3, HSC4):
  `TILE_INDEX, RA/DEC_AVERAGE, REFERENCE_TIME, PATCH_IDS, FILLING_FACTOR, MOSAIC_MASKED_FRACTION_<band>,
  VIS/NIR_DETECTIONS, GAIA_MATCHES, <band>_EXPTIME_MEAN, CREATION_DATE_YEARS`; via sftp
  `anonymous@ftp-bdt.cosmos.esa.int`, folder `EUC_DR1_CAL`.
- 15.3.2 Two T-PHOT bugs (recentring correction applied in the wrong direction for PSF fitting; numpy-vs-FITS row/column
  inversion of PSFs/kernels for all template fitting). Minor for galaxies, significant for point sources; fixed after DR1.
- 15.3.3 Bad SE++ Sersic fits where a band has no data: the catalogue contains the initial guesses instead of NaN.
  A cleaning program (`bad_objects.py --tiles <TILE_ID>`) is available from the helpdesk (subject "Bad MER catalog
  Sersic fitting results"); it NaNs `FLUX_<band>_SERSIC`, `FLUXERR_<band>_SERSIC`, the `SERSIC*` morphology columns and
  EXT Sersic fluxes when the flux is NaN, the error is 0/NaN, log10(error) is outside [-5, 5], or the Sersic flux equals
  the detection flux to 1e-6.
- 15.3.4 Wrong "worst-resolution PSF" assignment in partially covered tiles (e.g. tile 10183462, HSC-r): larger
  apertures and noisier A-PHOT colours for affected sources; fixed post-DR1.
- 15.3.5 `FLUX_RADIUS` computed only inside the segmentation area (not like SExtractor/SE++): biased low for extended
  sources; fixed post-DR1.
- 15.3.6 Notebook (github.com/esa/euclid-contributed-jupyter-notebooks) computing per-object exposure time and
  number of layers from the MER `LAYERS` files (HEALPix order 17, ~1.6"), optionally as exposure-time images.
- 15.3.7 Duplicate sources at tile borders (rate 1e-5), because inner-area membership was decided per parent cluster.
