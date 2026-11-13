# TODO: overnight run 2026-11-12/13

- [x] Environment check, setup questions (no git; galaxy examples from DR1 papers; 15 GB data budget; local HTML only)
- [x] uv project, project CLAUDE.md, SPEC, lessons
- [x] Archive: 26 A&A DR1 PDFs, 3 Q1 processing papers, 3 ICL arXiv papers, DR1 memo + product list, ESA pages,
      astroquery docs (rst), Explanatory Supplement mirror, DPDD mirror, Data Space help mirror -> `~/Desktop/euclid`
- [x] Text extraction (`scripts/extract_text.py`) -> `~/Desktop/euclid/text`
- [x] 32 structured paper summaries (`kb/papers/`), DPDD notes (`kb/data_model/`), TAP schema dump (134 tables)
- [x] Hands-on data access: TAP, mosaic families, cutouts, full files, spectra, astroquery versions ->
      `kb/data_model/verified_on_archive.md`
- [x] Topical syntheses `kb/01`-`13`, index `kb/00_index.md`, expsup and web notes
- [x] Full-text search `scripts/kb_search.py` (SQLite FTS5, 3412 chunks / 423 files)
- [x] Demo (`demo/`): cutouts + gallery of 8 paper galaxies, catalogue join, spectra, NGC 1483 LSB test (10 GB data)
- [x] HTML quick guide `guide/euclid_dr1_quick_guide.html` (self-contained, 1.8 MB; `scripts/build_guide.py`)

## Follow-ups (not done)

- [ ] Re-check in a few weeks: SIA coverage of DR1, astroquery release > 0.4.11, Explanatory Supplement updates,
      DR1 SIR paper (Scodeggio et al.) publication, IRSA DR1 availability, EUDF (early 2027).
- [ ] LSB pipeline from calibrated frames (Bamford recipe / nicl) on one nearby galaxy, ideally in ESA Datalabs
      (VIS calibrated frames are ~7 GB each).
- [ ] Own bulge/disc decompositions (DR1 Disk+Sersic columns are empty) with the GRID-PSF stamps; compare with
      catalogue single-Sersic fits.
- [ ] Extended PSF wings (ERO PSF of Cuillandre et al. 2025 or bright-star stacks) for halo work.
- [ ] Ask the helpdesk for the "Bad MER catalog Sersic fitting results" cleaning script.

## Review

- **Outcome**: all deliverables produced: archive (~380 MB) in `~/Desktop/euclid`, KB with 13 topical notes + 32
  paper summaries + data-model notes + search, four publication-style figures, demo scripts, HTML guide.
- **Main findings** (for the group): (1) MER mosaics remove LSB light; BGMOD restores only the MER step: in NGC 1483
  it removed ~40-65% of the I_E light at ~100" (measured); (2) 3-sigma 10"x10" limits: I_E 28.2 (wide) / 29.0
  (deep), H_E 27.0 / 27.9; naive pixel extrapolation 1.5-2.8 mag too optimistic; (3) large galaxies are shredded and
  flagged with DET_QUALITY_FLAG bit 512; their fragments get absurd SPE redshifts; (4) DR1 Disk+Sersic columns are
  empty; (5) access needs astroquery main + `schema/release = dr1`; SIA had no DR1 on release day.
- **What went wrong / lessons**: see `docs/lessons.md` (astroquery version, `sedm` 401, Cloudflare docs, cutout
  retries, SIMBAD outage, `rm` alias, pipe buffering hiding a hung download, an initial wrong Pa-beta interpretation
  corrected by looking at the data).
- **Verification status**: all code in `demo/` and `scripts/` was run; snippets in the KB marked "untested" were not.
  Agent-written notes (04-09, 13) were spot-checked against the verified facts, not line-by-line.

# TODO: follow-up session 2026-11-13 (user questions + HATS/LSDB)

- [x] Q1: which MER columns indicate whether an entry is real (measured on NGC 1483, wide + deep; `demo/07`)
- [x] Q2: can the Nottingham ICL method be reproduced with public DR1 (inputs checked on the archive; nicl code read)
- [x] Q3: official DR1 footprint (VMPZ per-tile HEALPix verified; MOC from tile polygons `demo/08`; HATS MOC)
- [x] IRSA HATS / LSDB route studied and verified (`demo/06`, `kb/14`), incl. Legacy Surveys DR11 (SLAC server)
- [x] KB, guide, verified facts, lessons updated; search index rebuilt

## Follow-ups (not done)

- [ ] Adapt `nicl` data access to the public archive (server, `dr1.` schema, `release=dr1`) and run the NIR part on one
      nearby galaxy in ESA Datalabs (inputs ~38 GB per NIR band).
- [ ] Open Legacy Surveys DR11 North and cross-match a northern EWS tile; check HSC PDR3 cross-match in an EMDS/HSC field.
- [ ] Re-check ESASky DR1 HiPS (MOC file) and CDS VizieR HATS (unWISE/CatWISE) when the services respond.
- [ ] Stack the fragment analysis over more large galaxies (one tile gave only NGC 1483).

## Review

- **Outcome**: three questions answered with measurements; new KB note 14, sections 06 §10.1, 09 §7.6, 10 §6.1;
  demos 06-08 with two new figures; ~1.6 GB extra data (one NIR frame + background).
- **Main findings**: no catalogue column isolates fragments (best simple cut flags 76% of the excess but 24% of real
  sources; `blended_prob`/`extended_prob` empty); the ICL processing is reproducible from public DR1 inputs, but the
  code targets the internal archive and the volume needs Datalabs; DR1 has no survey-wide footprint file (VMPZ per
  tile; tile MOC 2235 + 87 deg^2); IRSA HATS = ESA DR1_R2, slower for small cones, DR11 via SLAC.
- **Lessons**: subagent missed DR11 (portal index vs directory listing); TAP 500 on array columns; tile-local
  `parent_id`.

# TODO: follow-up 2026-11-13 (data volume for one galaxy; multi-page guide)

- [x] Range reads on the data service verified; regular frame layouts measured; `demo/09_frame_cutouts.py`
- [x] Volumes for a 1' galaxy (Abell 3112 BCG): A 0.9 GB, B 3.6 GB, C ~54 GB vs 39-350 GB whole files (`kb/10` §6.2)
- [x] `remote_rows_cutout` for BGMOD/RMS (pixel-identical to the full tile)
- [x] Guide split into `guide/site/` (index + 8 pages) built from `guide/src/`; single-file version kept

## Review

- The earlier "~280 GB per target" assumed whole files for a cluster-sized field; now stated explicitly, with
  measured per-galaxy numbers. Not done: parallel range requests (aggregate throughput unknown), atemporal-model
  computation itself, SIR frame contents.

# TODO: version control (2026-11-13)

- [x] `.gitignore` (Python, caches, data files, search index, built guide, Dropbox/macOS files)
- [x] README rewritten for GitHub readers
- [x] Pre-commit with Ruff from the project environment plus basic file checks
- [x] `git init -b main`, `origin` = `git@github.com:dr-guangtou/euclid_fun.git`, initial commit pushed

## Review

- The repository is public. The scan found no credentials, e-mail addresses or archive error text in tracked files.
  `kb/kb_index.sqlite` is excluded because it holds the full text of the archived papers.
- Licence: MIT for code and notes (`LICENSE`, branch `add-mit-license`); figures made from Euclid data follow
  ESA's CC BY-NC 3.0 IGO.
- Open: decide whether to publish the guide with GitHub Pages, which would need a build step because `guide/site/` is
  not tracked.

# TODO: publish the guide on GitHub Pages (2026-11-13)

- [x] `.github/workflows/pages.yml`: build with Pillow only, deploy `guide/site/` (actions: checkout v7, setup-uv v7,
      configure-pages v6, upload-pages-artifact v5, deploy-pages v5; latest major tags checked on GitHub)
- [x] `build_guide.py` links `<code>path</code>` mentions of repository files to GitHub (12 links, all HTTP 200)
- [x] Clean-copy build of tracked files only: 9 pages, 6 figures, 1.8 MB in 2 s; no broken relative links
- [ ] User: Settings -> Pages -> Source = "GitHub Actions"; then merge `add-github-pages` into `main`
- [ ] Check the first workflow run and the live site
- [ ] Optional: a "what we did" page built from the todo reviews and lessons

## Review

- Not verified yet: the workflow itself (it has not run on GitHub; Pages must be enabled first).

# TODO: UCD search pilot, Fornax (2026-11-13; plan in docs/ucd_pilot_plan.md)

- [x] Study bubbletea (method, assets, lessons); check Gaia DR4 (not public), DR1 coverage of UCD hosts
- [x] Interview: fields, Gaia step, verification rule, UCD definition, grz source, public-data rule, git, failures
- [x] Plan written; branch `ucd-search-pilot`
- [x] Stage 0: preflight, bubbletea snapshot, selector regression test, control field
- [x] Stage 1: resolution and detection limits (Gaia, Euclid)
- [x] Stage 2: Gaia retrieval and frozen-selector scoring
- [x] Stage 3: Euclid MER cross-match
- [x] Stage 4: Legacy Surveys DR11 South cross-match
- [x] Stage 5: contaminant rejection, cut flow, tiers
- [x] Stage 6: spatial distribution and background statistics
- [x] Stage 7: cutouts, colour composites, visual triage notes
- [x] Stage 8: report, workflow README, candidate-only ADQL, review section

## Review (run `fornax_pilot_20261113`, finished 2026-11-14)

- **Outcome:** all nine stages have a passing verdict (stages 3 and 4 on their first retry; the limits stage was
  re-run once with a cleaner star sample). Workflow description: `ucd/README.md`; aggregate results and lessons:
  `docs/ucd_pilot_run_log.md`; local report and all products: `~/data/euclid/bubbletea/runs/fornax_pilot_20261113/`.
- **Numbers:** control field 478 -> 5.5 candidates per deg^2 (tier A); 38 of the 40 known Fornax UCDs with Gaia and
  Euclid data recovered in tier A; 61 tier A objects within 16' of NGC 1399 against 1.2 expected; 26 tier A objects
  not in the literature catalogue, 14 of them clean compact on the cutouts.
- **Deviations from the plan:** listed in `docs/ucd_pilot_plan.md` section 8.
- **Lessons:** `docs/lessons.md` (2026-11-14 entries) and `kb/data_model/verified_on_archive.md`.

## Follow-ups (not started)

- [ ] Decide whether the galaxy-sequence envelope becomes a cut (information column in the first run)
- [ ] Own size measurement on VIS cutouts at the Gaia position (PSF-convolved King or Sersic fit); needed in the
      catalogue hole, in the core of NGC 1399 and for nucleated dwarfs
- [ ] Euclid colour criterion from a reference sample outside the target field
- [ ] Second and third control fields for the field-to-field term
- [ ] Validate `ucd/config/candidate_preselection.adql` on an independent field
- [ ] Disc-galaxy field (NGC 1291 or NGC 1433) and group fields (Fornax A, Dorado)
- [ ] Gaia excess noise versus angular size for Virgo objects (only a positional join so far); Gaia's upper size limit
- [ ] Inspect the remaining contact sheets (known sheet 2, other known tier A, control tiers B and C)
- [ ] Demo 08 and kb/09: note that tile-polygon MOCs overestimate coverage; build a catalogue-based coverage map
