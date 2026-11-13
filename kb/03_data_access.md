# Accessing Euclid DR1 data (tested recipes)

> Key points
> - Everything public is reachable **anonymously**: TAP/ADQL for catalogues and metadata, the cutout service for
>   mosaic cutouts, the data service for full files (`release=dr1`). Logging in (ESA Cosmos account) only adds longer
>   query time-outs, a persistent user space and table upload/sharing.
> - Use **astroquery from GitHub `main`** (0.4.12.dev); the PyPI 0.4.11 `get_cutout` writes empty files for DR1 and has
>   no `query_sia`. Pass `schema='dr1'` to `get_product` and `get_spectrum`.
> - On release day the **SIA service indexed only Q1**: find DR1 tiles with ADQL on `dr1.mosaic_product`
>   (`INTERSECTS(CIRCLE(ra, dec, r), fov) = 1`) and pick the right mosaic family (wide / deep / deep-visit).
> - Cutouts work for BGSUB mosaics and FLAG maps only; BGMOD (background model), RMS and PSF files must be downloaded
>   whole (1.47 GB per wide-tile layer, 0.42 GB per deep-tile layer).
> - All snippets below were run on 2026-11-12/13; the full working code is in `demo/dr1_access.py` and `demo/0*.py`.

See also: [verified_on_archive](data_model/verified_on_archive.md) (facts), [02_data_model](02_data_model.md)
(products), [11_known_issues](11_known_issues.md).

## 1. Access routes

| Route | What | Auth | Notes |
|---|---|---|---|
| Euclid Data Space portal https://euclid.dataspace.esa.int | web GUI: search, ADQL form, shopping basket, "Download All" curl scripts | optional | the help pages are JavaScript; raw HTML under `/public-eds-help/*.html` (archived in `~/Desktop/euclid/eds_help_mirror`) |
| TAP+ `https://eas.esac.esa.int/tap-server/tap` | ADQL on all `dr1.*` tables (sync <= 2000 rows; async up to 2 h / 3 M rows) | optional | `astroquery.esa.euclid.Euclid`, pyvo, TOPCAT |
| Cutout service `https://eas.esac.esa.int/sas-cutout/cutout` | server-side cutouts of MER BGSUB mosaics and FLAG maps (radius <= 0.5 deg) | none | `filepath=<file_path>/<file_name>&POS=CIRCLE,ra,dec,r_deg` |
| Data service `https://eas.esac.esa.int/sas-dd/data` | any full product file | none | `file_name=<name>&release=dr1&RETRIEVAL_TYPE=FILE`; spectra via DataLink (`get_spectrum`) |
| SIA v2 (`Euclid.query_sia`) | image discovery | none | returned Q1 only on DR1 day |
| ESASky (via Data Space) | HiPS colour images, catalogue overlays | none | quick look; coloured-HiPS caveats in the help pages |
| ESA Datalabs | JupyterLab next to the data: `/data/euclid_idr1/DR1/R2/...` (`datalabs_path` column), 32 GB RAM, 2 cores, 100 GB personal space, `euclid-tools` kernel (astroquery, photutils, SEP, SWarp, SExtractor, ...) | Cosmos account + approval (moderated beta, invitation code) | best for working on full tiles or calibrated frames (1.7 PB DR1 on disk) without downloading |
| sftp `anonymous@ftp-bdt.cosmos.esa.int`, `cd EUC_DR1_CAL` | DR1 calibration data repository incl. MER overview FITS tables per field (`DR1_EWS_MER_public.fits`, ...) | e-mail as password | Explanatory Supplement 15.3.1 |
| IRSA / ENSCI (IPAC) | Euclid Q1, Q2, ERO and **DR1**: 57 DR1 catalogues as HATS Parquet in `s3://nasa-irsa-euclid-dr1/contributed/dr1/hats/...` (README dated 2026-11-07; identical to the ESA DR1_R2 wide catalogue), plus IRSA DR1 tutorials (MER images, MER catalogue, PHZ, SPE, 1-D spectra, cloud access; updated 2026-11-11/12; services they use not checked here) | none (anonymous S3) | survey-scale catalogue work and cross-matching with LSDB: [14](14_hats_lsdb_access.md) |
| Helpdesk https://support.cosmos.esa.int/euclid | questions, bug reports, request the "bad MER Sersic" cleaning script | Cosmos account | |

## 2. Setup

```bash
uv add "astroquery @ git+https://github.com/astropy/astroquery.git@main"   # tested commit 74b6cd23
uv add astropy photutils matplotlib requests
```

Credentials (optional) are read from the environment (`EUCLID_USER`, `EUCLID_PASS`):

```python
import os
from astroquery.esa.euclid import Euclid
Euclid.login(user=os.environ["EUCLID_USER"], password=os.environ["EUCLID_PASS"])   # TAP, data, cutout, SIA
...
Euclid.logout()
```

Do not print raw HTTP error bodies from the data service: they echo the account name, e-mail and IP address.

## 3. Find the MER tile(s) covering a position

Mosaic families (`dr1.mosaic_product`): wide survey = `release_name='DR1_R2' AND purpose='DATA_RELEASE' AND
processing_mode='WIDE'` (32' tiles, index `102...`); deep stacks = `release_name='DR1_R1' AND
purpose='DATA_RELEASE_DEEP' AND processing_mode='DEEP'` (17' tiles, `101...`); single deep-field visits =
`purpose='DATA_RELEASE_DEEP' AND processing_mode='WIDE'`.

```python
from astroquery.esa.euclid import Euclid
ra, dec = 58.19837, -47.47752   # NGC 1483
adql = f"""
SELECT mosaic_product_oid, tile_index, filter_name, file_name, file_path, zero_point, creation_date, ra, dec
FROM dr1.mosaic_product
WHERE INTERSECTS(CIRCLE({ra}, {dec}, 0.0001), fov) = 1
  AND instrument_name IN ('VIS', 'NISP')
  AND release_name = 'DR1_R2' AND purpose = 'DATA_RELEASE' AND processing_mode = 'WIDE'
ORDER BY tile_index, filter_name, creation_date DESC"""
mosaics = Euclid.launch_job_async(adql).get_results()
```

Then (i) keep the newest `creation_date` per (tile, band) (a few tiles have duplicates), (ii) if several tiles
overlap, take the one whose centre (`ra`, `dec`) is closest so the target is far from the edge, (iii) check the
cutout for zeros: in the Deep Fields the wide-survey mosaic can be empty although `fov` contains the target (use the
deep stack there). For EXT bands use `instrument_name IN ('DECAM', 'MEGACAM', 'HSC', 'GPC')`.

## 4. Cutouts

```python
import requests
row = mosaics[0]
params = {"filepath": f"{row['file_path']}/{row['file_name']}",           # /data/euclid/repository_dr1/DR1/R2/MER/...
          "POS": f"CIRCLE,{ra},{dec},{1.0 / 60}"}                         # half-size 1 arcmin -> 1201 x 1201 px
response = requests.get("https://eas.esac.esa.int/sas-cutout/cutout", params=params, timeout=600)
assert response.content.startswith(b"SIMPLE")                             # retry if not (happens under load)
open("ngc1483_vis.fits", "wb").write(response.content)
```

or, with astroquery main: `Euclid.get_cutout(file_path=f"{file_path}/{file_name}", coordinate=coord,
radius=1 * u.arcmin, output_file="cutout.fits")`.

The cutout is a square of side 2 x radius, single primary HDU, float32, `BUNIT` `ADU/s` (VIS) or `ELECTRON/s`
(NISP), WCS with CD matrix, plus a few propagated keywords; **`MAGZERO` is not in the cutout header**: take
`zero_point` from the table (VIS 24.5, Y 29.8, J 30.1, H 30.0, EXT 30.0). FLAG cutouts: request the FLAG file listed
in `dr1.aux_mosaic`. Timing: 2-20 s for 1' (minutes when the service is busy).

## 5. Auxiliary MER files and full downloads

```python
aux = Euclid.launch_job_async(
    f"SELECT stype, file_name FROM dr1.aux_mosaic WHERE mosaic_product_oid = {row['mosaic_product_oid']}"
).get_results()            # stype: RMS, FLAG, BKG (=BGMOD), PSF (=CATALOG-PSF), GRID_PSF, BRIGHT_STAR_MASKS, LAYERS, FILTER_TRANSMISSION

# full file, anonymous (stream to disk; 1.47 GB took ~230 s):
url = "https://eas.esac.esa.int/sas-dd/data"
with requests.get(url, params={"file_name": name, "release": "dr1", "RETRIEVAL_TYPE": "FILE"}, stream=True) as r:
    with open(name, "wb") as f:
        for chunk in r.iter_content(8 << 20):
            f.write(chunk)
# or: Euclid.get_product(file_name=name, schema="dr1", output_file=name)   (schema='sedm' -> HTTP 401)
```

Sizes: wide-tile layers 1.47 GB each (BGSUB, BGMOD, RMS, FLAG, GRID-PSF), CATALOG-PSF 0.7-2 GB, star-mask JSON
~2 MB; deep-tile layers 0.42 GB. Read big mosaics with `fits.open(path, memmap=True)` and `Cutout2D`.

**Partial reads (verified 2026-11-13).** The data service answers HTTP range requests (206), so a region of a
single-image file can be read without the whole file. `dr1_access.remote_rows_cutout(file_name, coord, half_size)`
reads the header, then fetches only the image rows around the target in one request. For BGMOD and RMS, which the
cutout service rejects, a 1' cutout is ~46 MB in ~26 s instead of 1.47 GB in ~230 s, and is pixel-identical. Keep the
number of requests low: each costs several seconds of latency.
Bright-star mask JSON: `{"0": {"RA", "DEC", "mag", "gaia_id", "polygon": [[ra, dec], ...]}, ...}`.

## 6. Catalogue queries

MER tables with coordinates are `dr1.mer_catalogue_<group>` (`wide_survey`, `wide_mode`, `deep_survey`, `deep_mode`,
`deep_visits`); morphology, PHZ and SPE tables join on `object_id`.

```sql
-- cone search + morphology + photo-z + class + stellar mass (tested; a whole tile, ~20k rows, took ~10 min)
SELECT m.object_id, m.right_ascension, m.declination, m.flux_detection_total, m.flux_vis_sersic,
       m.point_like_prob, m.spurious_prob, m.det_quality_flag, m.deblended_flag,
       mo.sersic_sersic_vis_radius, mo.sersic_sersic_vis_index, mo.sersic_sersic_vis_axis_ratio, mo.sersic_visnir_flags,
       p.phz_median, p.phz_flags, c.phz_classification, pp.phz_pp_median_stellarmass
FROM dr1.mer_catalogue_wide_survey AS m
JOIN dr1.mer_morphology_wide_survey AS mo ON mo.object_id = m.object_id
JOIN dr1.phz_photo_z_wide AS p ON p.object_id = m.object_id
JOIN dr1.phz_classification_wide AS c ON c.object_id = m.object_id
LEFT OUTER JOIN dr1.phz_physical_parameters_wide AS pp ON pp.object_id = m.object_id
WHERE 1 = CONTAINS(POINT(m.right_ascension, m.declination), CIRCLE(58.198, -47.478, 0.05))
  AND m.vis_det = 1 AND m.flux_detection_total > 0.912        -- I_E < 24 (23.9 - 2.5 log10 F)
```

- Galaxies: `phz_classification = 2` (bit 2; 1 = star). The TAP column description has these swapped.
- Prefer `CONTAINS(POINT(...), CIRCLE(...))` or `DISTANCE(...) < r`; `query_object` uses the deprecated BOX.
- Nulls can be NaN or -99: use `NULLIF(col, 'NaN')`.
- Whole tile: `WHERE m.tile_index = 102021980`. Whole-survey queries need async jobs (login gives longer time-outs).
- Full catalogue FITS files per tile: `dr1.basic_download_data` / `dr1.mer_final_catalogue` (`file_name_list`).

## 7. Spectra

```python
from astropy.table import Table
Euclid.get_spectrum(ids="-582334178474562017", schema="dr1", retrieval_type="SPECTRA_RGS",
                    output_file="spec.fits")          # writes 'SPECTRA_RGS-dr1 <id>.fits' next to it
spectrum = Table.read("SPECTRA_RGS-dr1 -582334178474562017.fits", hdu=1, unit_parse_strict="silent")
# columns WAVELENGTH [A], SIGNAL [1e-16 erg/s/cm2/A], MASK, QUALITY, VAR [1e-32 ...], NDITH; 531 bins of 13.4 A, 1.19-1.90 um
```

Which sources have spectra: `dr1.spectra_source_<wide|deep|deep_visits>` (`source_id` = MER `object_id`,
`file_name`, `hdu_index`); redshifts in `dr1.spectro_z_spe_galaxy_candidates_<group>` (use `spe_rank = 0`).
`Euclid.get_datalinks(ids=...)` lists available products. Spectra exist for MER objects with H_E < 23.5.

## 8. Calibrated single-exposure frames (for LSB re-processing)

```sql
SELECT cf.calibrated_frame_oid, cf.observation_id, cf.instrument_name, cf.filter_name, cf.file_name, cf.file_path,
       cf.start_time, cf.pa
FROM dr1.calibrated_frame AS cf
WHERE INTERSECTS(CIRCLE(58.198, -47.478, 0.05), cf.fov) = 1
-- auxiliary files (BKG, WGT, PSF, ...): dr1.aux_calibrated ON calibrated_frame_id = calibrated_frame_oid
```

A VIS calibrated quad frame is 7.3 GB (432 extensions = 144 quadrants x SCI/RMS/FLG); a NIR frame 0.8 GB (48
extensions). **You do not need whole files for a small target.** The layout is regular, so
`demo/09_frame_cutouts.py` fetches only the quadrants or detectors covering the target (one ~50 MB range request
each) and cuts the region out with the unit's WCS. For a 1' galaxy (VIS + Y + J + H, 4 dithers) this is 0.9 GB instead
of 39 GB ([10 §6.2](10_low_surface_brightness.md)). The query above uses `fov`; `demo/09` selects frames whose centre
(`ra`, `dec`) lies within 0.6 deg of the target and uses `pa` for the focal-plane model. Prefer ESA Datalabs for
full-field work (whole focal planes, atemporal backgrounds).
Stacks: `dr1.observation_stack` + `dr1.aux_stacked`.

## 9. Bulk downloads

- GUI: select rows -> "Download All" -> cURL script.
- Script: list `file_name`s via ADQL (`dr1.mosaic_product`, `dr1.aux_mosaic`, `dr1.calibrated_frame`,
  `dr1.basic_download_data`), then one `curl -o <name> 'https://eas.esac.esa.int/sas-dd/data?file_name=<name>&release=dr1&RETRIEVAL_TYPE=FILE'`
  per file (the help page shows `release=sedm`, valid for Q1 only).
- Throughput observed: ~6.5 MB/s per stream; plan ~4 min per 1.47 GB tile layer.

## 10. Practical gotchas (all hit on release day)

1. astroquery PyPI 0.4.11 is not DR1-ready (empty cutouts, no SIA, `sedm` defaults).
2. `release=sedm`/`schema='sedm'` defaults give HTTP 401 for DR1 files: use `dr1`.
3. SIA has no DR1 yet; use ADQL on `fov`.
4. Footprint polygons can be larger than the data (zeros in cutouts), especially in Deep Fields.
5. Duplicated mosaics for a few tiles: take the newest.
6. The cutout service can answer HTTP 200 with a non-FITS body under load: check the `SIMPLE` header and retry.
7. Cutout headers lack `MAGZERO`: use the table `zero_point`.
8. The archive help's query examples use `catalogue.*`/`q1.*` names in places; DR1 tables live in `dr1.*`.
9. Several catalogue column descriptions are wrong or missing (e.g. `phz_classification`); check
   [11_known_issues](11_known_issues.md).
