# Lessons

Record mistakes and the rationale for fixes here. Review at session start.

- 2026-11-12: zsh indirect expansion `${(P)var}` in a Bash tool command trips the safety parser;
  use `printenv NAME >/dev/null` to test whether a variable is set without printing it.
- 2026-11-12: `pre-commit` needs a git repository. Until 2026-11-13 this folder was not one, so Ruff was run by hand.
  It is now a git repository (public on GitHub), and pre-commit runs Ruff from the project environment.
- 2026-11-13: before publishing, check what the files carry, not only their names. The search index
  `kb/kb_index.sqlite` holds the full text of the archived papers, so it must stay out of the public repository even
  though it looks like a harmless build artefact.
- 2026-11-12: docs.astropy.org sits behind a Cloudflare browser check; fetch the astroquery docs source
  (`docs/esa/euclid/euclid.rst`) from GitHub instead of scraping the rendered page.
- 2026-11-12: astroquery 0.4.11 (PyPI) `Euclid.get_cutout` writes an empty file for DR1 mosaics and lacks
  `query_sia`; the git `main` build (0.4.12.dev) works. Pinned `astroquery @ git+...@main` in pyproject.
- 2026-11-12: DR1 full-file downloads must use `release=dr1` on `https://eas.esac.esa.int/sas-dd/data`
  (astroquery `get_product(..., schema='dr1')`). The default `sedm` (Q1) gives HTTP 401, even when logged in.
  The 401 error text echoes the account's name, e-mail and IP: never print or store raw server errors.
- 2026-11-12: SIA (`Euclid.query_sia`) returns no DR1 products on release day (Q1 only); use TAP on
  `dr1.mosaic_product` + `INTERSECTS(CIRCLE(...), fov)` to find tiles.
- 2026-11-12: the cutout service works for BGSUB mosaics and FLAG maps but fails (HTTP 500, "CTYPE1 not
  found") for BGMOD and RMS maps; download those as full tiles.
- 2026-11-12: SIMBAD TAP capabilities endpoint returned 404 (astroquery.simbad broken that night);
  `SkyCoord.from_name` (Sesame) still works for name resolution.
- 2026-11-13: in this shell `rm` is aliased to a trash-based `delete` function that rejects `-rf`; use `trash <dir>` (recoverable) for directories.
- 2026-11-13: a background download piped through `grep` showed no output for 30 min because of pipe buffering and
  then turned out to be hung in a TAP wait; run long jobs with `python -u` and `grep --line-buffered`, and print
  progress per file.
- 2026-11-13: a "line" hypothesis (Pa-beta of NGC 1483 explaining a spurious SPE redshift) was wrong; plotting the
  spectrum showed contamination by dispersed host light instead. Always look at the data before writing the caption.
- 2026-11-13: masking spectra with `MASK == 0` hid most of a bright galaxy's spectrum (LOW_SNR/EXT_PRB bits set over
  long ranges); hide only NOT_USE (1) and ABS_FLUX (64) and treat the others as informational.
- 2026-11-13: paper summaries can be wrong by omission (e.g. "only single-Sersic fits" while the archive has empty
  Disk+Sersic columns; PHZ class codes swapped in the TAP description): verify data-model claims against the archive.
- 2026-11-13: the user's `~/.matplotlib/matplotlibrc` enables grids; the shared style sets `axes.grid = False`.
- 2026-11-13: the built-in browser could not open local files or localhost pages unattended; `qlmanage -t -s 1400
  file.html` renders a WebKit thumbnail for a quick visual check.
- 2026-11-13: a subagent reported Legacy Surveys as "DR10.1 South only" on LSDB after listing `data.lsdb.io/hats/`;
  DR11.0 North and South are listed in the portal (`data.lsdb.io/data/catalogs.json`) and served from a SLAC host.
  When a user names a data set that "is not there", read the portal's catalogue index before concluding.
- 2026-11-13: ESA TAP returns HTTP 500 ("results is null") for queries that select array columns (`fov`,
  `file_name_list`) together with `DISTINCT`/`LIKE`/`GROUP BY`; use `stc_s` for polygons and `dr1.files_table` for
  file names. `SELECT *` on the MER catalogue also fails in astroquery (`calblock_id_list`).
- 2026-11-13: `parent_id` is a tile-local number; a family selected by `parent_id` alone in a multi-tile cone picked
  up unrelated entries. Always match on (`tile_index`, `parent_id`), and choose the host as the brightest entry near
  the target position, not the brightest in the cone.
- 2026-11-13: a background job queued a 2.4 GB VIS background file the check did not need; list sizes (or download
  the smallest representative file) before queueing several large files. `~/data/euclid/perseus_ero` (33 GB) belongs
  to the user and is not part of this project's budget.
- 2026-11-13: the mocpy WCS context draws a small all-sky map inside a large box; for publication maps sample the MOC
  on a lon/lat grid (`MOC.contains_lonlat`) and use matplotlib's Mollweide axes with x = -RA.
- 2026-11-13: data-volume estimates must state the field size and whether whole files are assumed. The first answer
  ("~280 GB VIS per target") silently assumed whole focal-plane files for a cluster-sized field; for a 1' galaxy,
  range reads of the needed CCD quadrants cut this to 0.9 GB. Check whether the server supports HTTP range requests
  before concluding that a product is too big.
- 2026-11-13: the archive's per-detector table (`dr1.calibrated_detectors`) looked like the way to locate detectors
  but is unusable (NIR only, one shared `crval`); a focal-plane model from one exposure's headers works for all.
