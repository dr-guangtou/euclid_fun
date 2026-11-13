# Euclid DR1 knowledge base: index

Built 2026-11-12/13 (DR1-Foundation release day) for photometry and 2-D modelling of extended low-to-intermediate-z
galaxies, with emphasis on low-surface-brightness (LSB) work. Facts verified hands-on against the archive are in
[data_model/verified_on_archive.md](data_model/verified_on_archive.md) and take precedence over the documentation.

**Search everything** (KB notes + full text of all papers, DPDD, Explanatory Supplement, help pages, memos):

```bash
uv run python scripts/kb_search.py "background model" --limit 10
uv run python scripts/kb_search.py '"Sersic index" AND reliab*' --group papers
uv run python scripts/kb_search.py build        # after adding documents
```

## Start here

| If you want to ... | read |
|---|---|
| know what DR1 contains, dates, areas, depths | [01_dr1_overview](01_dr1_overview.md) |
| understand files, tables, keys, units | [02_data_model](02_data_model.md) -> [data_model/](data_model/) |
| get images/cutouts/catalogues/spectra (tested code) | [03_data_access](03_data_access.md) |
| do LSB photometry / surface-brightness profiles | **[10_low_surface_brightness](10_low_surface_brightness.md)** |
| avoid known traps | [11_known_issues](11_known_issues.md) |
| decide whether a catalogue entry near a big galaxy is real | [06 §10.1](06_catalogues_photometry_morphology.md) (measured flag performance) |
| reproduce the Nottingham ICL processing on public DR1 | [10 §6.1](10_low_surface_brightness.md) |
| get a DR1 footprint / MOC | [09 §7.6](09_masks_flags_coverage.md) |
| read only part of a big file (1' from a 7.3 GB calibrated frame, BGMOD/RMS cutouts) | [03 §5, §8](03_data_access.md), [10 §6.2](10_low_surface_brightness.md) |
| query or cross-match catalogues at scale (IRSA HATS, LSDB, Legacy Surveys DR11, Gaia, DESI, HSC) | [14_hats_lsdb_access](14_hats_lsdb_access.md) |
| pick example galaxies | [12_galaxy_examples](12_galaxy_examples.md) |

## Topical notes

| # | Note | Content |
|---|---|---|
| 01 | [DR1 overview](01_dr1_overview.md) | release stages, timeline, data sets, products, depths, versions, licence |
| 02 | [Data model](02_data_model.md) | product tree, identifiers, archive table families, units, what is missing |
| 03 | [Data access](03_data_access.md) | routes, astroquery setup, tile finding, cutouts, full files, ADQL joins, spectra, calibrated frames, bulk |
| 04 | [Imaging processing](04_imaging_processing.md) | VIS, NIR, EXT and MER pipelines, calibration, spacecraft effects |
| 05 | [PSF](05_psf.md) | all PSF products, sizes, normalisation, FWHM, wings, how to get a PSF for modelling |
| 06 | [Catalogues, photometry, morphology](06_catalogues_photometry_morphology.md) | MER catalogue groups, flux types, cookbooks, Sersic/Zoobot/CAS, flags, clean samples |
| 07 | [Photo-z and physical parameters](07_photoz_physical_parameters.md) | PHZ tables, performance at low z, selections |
| 08 | [Spectroscopy](08_spectroscopy.md) | NISP grisms, SIR spectra format, SPE redshifts, low-z limitations |
| 09 | [Masks, flags, coverage](09_masks_flags_coverage.md) | FLAG/DQ bits, star masks, VMPZ HEALPix maps, exposure-time layers |
| 10 | [Low surface brightness](10_low_surface_brightness.md) | where sky is subtracted, recovery recipes, artefacts, SB limits, ICL-team lessons, NGC 1483 test |
| 11 | [Known issues](11_known_issues.md) | consolidated list with severity and workarounds |
| 12 | [Galaxy examples](12_galaxy_examples.md) | objects from the DR1 papers with coordinates and tiles |
| 13 | [Glossary](13_glossary.md) | acronyms and jargon |
| 14 | [HATS / LSDB access](14_hats_lsdb_access.md) | IRSA HATS copy of the DR1 catalogues, comparison with ESA TAP, timings, cross-match partners (Gaia, Legacy Surveys DR10.1/DR11, DESI, HSC, WISE) |

## Source summaries

- [papers/](papers/): one structured summary per paper (template [papers/_TEMPLATE.md](papers/_TEMPLATE.md)):
  - A&A Special Issue DR1-Foundation (26): [aussel](papers/aussel.md) (overview), [tereno](papers/tereno.md) (surveys),
    [ruffenach](papers/ruffenach.md) (SGS), [mccracken](papers/mccracken.md) (VIS), [polenta](papers/polenta.md)
    (NIR), [radovich](papers/radovich.md) (NIR astrometry), [dasilva](papers/dasilva.md) (NISP PSF),
    [kubik](papers/kubik.md) (persistence), [corcho-caballero](papers/corcho-caballero.md) (EXT),
    [kuemmel](papers/kuemmel.md) (MER), [gasparetto](papers/gasparetto.md) (photometry validation),
    [odier](papers/odier.md) (masks), [hartley](papers/hartley.md) (photo-z), [enia](papers/enia.md) (physical
    properties), [dunn](papers/dunn.md) (3-D shapes), [fumana](papers/fumana.md) (SIR calibration),
    [lebrun](papers/lebrun.md) (SPE), [bergamini](papers/bergamini.md) (arcs spectroscopy),
    [gabarra](papers/gabarra.md) (emission-line maps), [schirmer-calibration](papers/schirmer-calibration.md),
    [schirmer-spacecraft](papers/schirmer-spacecraft.md), [gatto](papers/gatto.md) (LSB stellar systems),
    [lines](papers/lines.md), [holloway](papers/holloway.md), [nightingale](papers/nightingale.md),
    [nersesian](papers/nersesian.md) (ECLIPSE lens series A-D).
  - Q1 processing papers cited by the Supplement as the DR1 reference: [q1_romelli_mer](papers/q1_romelli_mer.md),
    [q1_mccracken_vis](papers/q1_mccracken_vis.md), [q1_polenta_nir](papers/q1_polenta_nir.md).
  - Euclid cluster-team ICL papers (arXiv 2610.29682-4): [q1_icl_processing_bamford](papers/q1_icl_processing_bamford.md),
    [q1_icl_halo_shapes_kolcu](papers/q1_icl_halo_shapes_kolcu.md), [q1_icl_fraction_gully](papers/q1_icl_fraction_gully.md).
- [expsup/](expsup/README.md): Explanatory Supplement (release notes!).
- [web/](web/README.md): ESA pages, DR1 memo, list of supported products, Data Space help & known issues, astroquery docs.
- [data_model/](data_model/): DPDD notes (MER, VIS/NIR, PHZ, spectroscopy, VMPZ masks, EXT/archive), TAP column dump
  ([tap/README](data_model/tap/README.md)), [verified facts](data_model/verified_on_archive.md).

## Archive of originals (not in this folder)

`~/Desktop/euclid/`: `papers/` (26 DR1 PDFs), `papers_q1/` (3), `papers_extra/` (3 ICL arXiv), `docs/` (memos),
`web/`, `expsup_mirror/`, `dpdd_mirror/`, `eds_help_mirror/`, and `text/` (plain-text extracts used by the search).
Re-create with `bash scripts/fetch_sources.sh && bash scripts/fetch_arxiv_extra.sh && uv run python -I scripts/extract_text.py`.

## Demo

`demo/` (see [demo/README.md](../demo/README.md)) and `figures/`: gallery, catalogue, spectra, LSB, fragment-flag
and footprint figures; HATS/LSDB access and cross-match check (`demo/06_hats_crossmatch.py`).
