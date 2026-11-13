# Euclid DR1 demo

Runnable end-to-end examples (tested 2026-11-12/13). Data go to `~/data/euclid/dr1_demo/` (~12 GB in total, of which
~9.5 GB are the full tiles for step 5 and 1.6 GB one NIR calibrated frame + background used to check the ICL inputs).
HATS query results go to `~/data/euclid/hats_cache/`. Figures go to `../figures/`.

```bash
uv run python demo/01_get_cutouts.py        # tiles + VIS/Y/J/H (+FLAG) cutouts for 8 galaxies from the DR1 papers
uv run python demo/02_gallery.py            # figures/dr1_gallery.png
uv run python demo/03_catalog_demo.py       # MER + morphology + PHZ join; figures/dr1_catalog_demo.png
uv run python demo/04_spectra.py            # NISP 1-D spectra; figures/dr1_spectra_demo.png
uv run python demo/download_lsb_tiles.py    # full BGSUB/BGMOD tiles for NGC 1483 (wide + EDF-S deep), ~9.5 GB
uv run python demo/05_lsb_background.py     # LSB analysis; figures/dr1_lsb_ngc1483.png + _limits.json
uv run python demo/06_hats_crossmatch.py    # IRSA HATS vs ESA TAP, LSDB cross-matches, HATS footprint (~13 min)
uv run python demo/07_fragment_flags.py     # which catalogue columns flag fragments; figures/dr1_fragment_flags.png
uv run python demo/08_dr1_footprint.py      # DR1 footprint MOCs from tile polygons; figures/dr1_footprint.png
uv run python demo/09_frame_cutouts.py      # 1' region of every calibrated exposure (VIS+YJH) via range reads (~5 min)
```

| File | Purpose |
|---|---|
| `dr1_access.py` | helper library: ADQL runner with retries, tile finding (mosaic families, de-duplication), cutouts with retries, full-file streaming (`release=dr1`), unit conversions, MER cone search |
| `targets.py` | the 8 gallery targets (from the DR1 papers), cutout sizes, mosaic family per target, LSB target and tiles |
| `01_get_cutouts.py` | per target: TAP query -> closest tile -> cutouts in 4 bands + VIS FLAG -> `metadata.json` |
| `02_gallery.py` | colour composites (R = H_E, G = (Y_E+J_E)/2, B = I_E; arcsinh stretch; NIR channels median-filtered against hot pixels) |
| `03_catalog_demo.py` | (a) MER entries around NGC 1483 (shredding), (b) Sersic R_e vs n, (c) photo-z vs I_E, (d) stellar mass vs photo-z |
| `04_spectra.py` | `Euclid.get_spectrum(schema='dr1')`; a z = 0.149 galaxy and a contaminated NGC 1483 disc fragment with a spurious z = 4.59 |
| `download_lsb_tiles.py` | full-tile downloads listed in `~/data/euclid/dr1_demo/tiles/lsb_manifest.json` |
| `05_lsb_background.py` | BGSUB vs BGSUB+BGMOD, own sky, elliptical profiles, 3-sigma 10"x10" limits vs naive pixel extrapolation |
| `06_hats_crossmatch.py` | IRSA HATS (S3) cone vs ESA TAP (rows, ids, values, timing); cross-match with Gaia DR3, Legacy Surveys DR10.1 and DR11 South; joins with morphology/PHZ; 30' cone throughput; MOC from the HATS partition index |
| `07_fragment_flags.py` | entry density around NGC 1483 (wide and deep) vs field; fraction of the fragment excess vs of field sources flagged by `spurious_prob`, `spurious_flag`, NIR-only, `deblended_flag` |
| `08_dr1_footprint.py` | MOCs (order 13) of the wide and deep VIS tile polygons, areas, all-sky map |
| `09_frame_cutouts.py` | partial reads of calibrated frames: focal-plane model (cached in `frames/focal_plane_model_*.json`), units covering a target, one range request per CCD quadrant / NIR detector, per-exposure cutouts with their own WCS; `figures/dr1_frame_cutouts.json` lists units, bytes and times |

## Results in one paragraph

- All 8 targets have DR1 data; PGC 61126 needs the EDF-N deep tile because the wide-survey mosaic is empty there.
- NGC 1483 (D ~ 2') is split into 6 large MER entries (one `parent_id`) plus 525 excess entries at 40"-100" in the wide
  catalogue (deep: 38 pieces + 1244); no column isolates them (`spurious_prob > 0.7` or NIR-only flags 76% of the excess
  but also 24% of field sources). Fragments can have absurd SPE redshifts (z = 4.59, `spe_z_prob` ~ 1) because their
  spectra are contaminated by the host's light.
- The MER background model (BGMOD) contains a positive bump on NGC 1483: the MER sky step removed ~40% (deep) to ~65%
  (wide) of the I_E light at a semi-major axis of ~100".
- 3-sigma limits in 10"x10" boxes: I_E 28.2 (wide) / 29.0 (deep); H_E 27.0 / 27.9 mag/arcsec^2. Naive extrapolation of
  the pixel RMS is 1.5-2.8 mag too optimistic.
- DR1 Disk+Sersic columns are empty; Zoobot morphology exists for bright galaxies; `phz_classification` 2 = galaxy.
- IRSA's HATS copy of the MER wide catalogue is identical to the ESA DR1_R2 table; for single small cones the ESA TAP is
  ~3-6x faster; HATS is for survey-scale work and cross-matching (Gaia, Legacy Surveys DR10.1/DR11, DESI, HSC, WISE).
- DR1 footprint: no survey-wide file in the archive; tile-polygon MOC 2235 deg^2 (wide) + 87 deg^2 (deep).
- Calibrated frames do not have to be downloaded whole: the data service answers HTTP range requests. A 1' region of
  all 4 dithers in VIS+Y+J+H is ~0.9 GB instead of 39 GB (demo 09); a 1' BGMOD/RMS cutout is one ~46 MB request
  (`dr1_access.remote_rows_cutout`, pixel-identical to the full tile).
