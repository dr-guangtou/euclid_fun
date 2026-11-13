# Plan: UCD candidate search with Gaia + Euclid DR1 + Legacy Surveys (Fornax pilot)

Status: **plan approved in interview on 2026-11-13; run not started.** This file is the source of truth for the
overnight run. After any interruption or context loss, read this file and the run log first
(`~/data/euclid/bubbletea/runs/<run_id>/run_log.md`), then continue with the first stage that has no passed gate.

## 1. Motivation and scope

Ultra-compact dwarfs (UCDs) are known almost only around a few nearby clusters and massive galaxies. The sister
project `bubbletea` (Gaia DR3 only) can reject stars, binaries and QSOs, but its frozen selector still keeps about 87%
of background galaxies. Euclid VIS (0.1" pixels) can separate marginally resolved UCDs from both stars and galaxies,
and gives YJH photometry, Sersic fits and photo-z; Legacy Surveys add grz.

Goal of the first run: **establish a standard, repeatable workflow** (motivation, procedure, checks, QA, output
structure) on one field with a known UCD population. Scientific results are welcome but not required. The workflow
must later run on any region of Euclid DR1 + Gaia.

Out of scope tonight: anything larger than 10 deg^2 in total; Euclid-only (no Gaia) candidates; spectroscopy;
re-training any selector.

## 2. Facts checked on 2026-11-13 (before planning)

| Fact | Result |
|---|---|
| Fornax cluster core (NGC 1399, RA 54.6211, Dec -35.4507, ~20 Mpc) | In the DR1 **wide** survey (VIS + Y, J, H mosaics; tiles 102034972, 102034973 at the centre). It is **not** a deep field: "Euclid Deep Field Fornax" is at RA 52.93, Dec -28.09 (CDFS), 7.5 deg away |
| DR1 coverage of the 1 deg radius field | 94% (tile-polygon MOC) |
| Euclid MER wide entries within 1 deg | 1,067,008 (count query: 8 s) |
| Gaia DR3 sources within 1 deg / within 1.78 deg | 11,358 (6,842 with G > 19) / 35,505 |
| Gaia DR4 | Not in the ESA archive (schemas: gaiadr1, gaiadr2, gaiaedr3, gaiadr3, gaiafpr). The run uses DR3; code keeps the release as a parameter |
| Other DR1 hosts with known or plausible UCDs | NGC 1316 (Fornax A), NGC 1365, Dorado group (NGC 1549/1553/1566), NGC 1291, NGC 1433 (wide); NGC 1483 (deep). Virgo, Coma, Hydra I, Centaurus, Cen A, Sombrero are **not** in DR1 |
| Known Fornax objects in bubbletea (within 3 deg) | 166 confirmed, 44 candidates (Saifollahi et al. 2021 "BEST"), 547 rejected, 14 uncertain; 59 of the confirmed + candidate have Gaia DR3 ids |
| Known UCD properties (bubbletea, confirmed) | r_h 6.9 / 15.1 / 37.3 pc (5 / 50 / 95%; n = 426); M_V -12.1 / -10.4 / -9.1 (n = 428) |
| Angular scale at 20 Mpc | 10 pc = 0.10" (one VIS pixel); 100 pc = 1.0" |
| bubbletea frozen selector | `point_source_logistic_model_v1`, 9 Gaia features, threshold 0.8277833628791744, valid for 11.26 <= G <= 21.76; sealed test: 21/23 UCDs kept, 0/287 binaries, 1/88 QSOs, 87% of SDSS galaxies kept. Random-field density of selected sources 340-490 per deg^2 |
| MER catalogue helpers | `gaia_id` (Gaia DR3, 0.3" epoch-propagated match), `point_like_prob`, `mumax_minus_mag`, Sersic radius, `phz_glob_cl_prob`, DECam g, r, i, z aperture fluxes |

## 3. Decisions from the interview (2026-11-13)

| Topic | Decision |
|---|---|
| Fields | 1 deg radius around NGC 1399 (3.14 deg^2) plus an equal-area control field in the wide survey, a few degrees away, without bright galaxies. About 6.3 deg^2 in total (limit: 10 deg^2) |
| Gaia step | Pull all Gaia DR3 sources in both fields; score with bubbletea's frozen v1 selector (unchanged). Simple Voggel et al. 2020 style cuts are computed alongside for comparison only |
| Known Fornax objects | **Verification only.** No threshold is ever set or adjusted using them. Every miss is reported and explained |
| UCD definition for the limits | r_h >= 10 pc and M_V <= -10; grid r_h 3-100 pc, M_V -8 to -14, distance 3-50 Mpc. Hostless candidates are described in observed units |
| grz photometry | Legacy Surveys **DR11 South** (SLAC LSDB server) is the standard. MER DECam fluxes and a DR10 subset are QA comparisons |
| Public repository | Git holds **code, configuration, docs and aggregate numbers only**. No table with coordinates of candidates or of known objects, no cutouts, no QA figures |
| bubbletea dependency | One-time snapshot into `~/data/euclid/bubbletea/reference/` with SHA-256 hashes and bubbletea's commit id. Code reads only the snapshot. bubbletea is never modified |
| Visual vetting | Claude looks at every final cutout and records a note and a flag in a separate column. Notes never remove or re-rank an object |
| Git during the run | One commit per finished stage on `ucd-search-pilot`, pushed. No merge into `main`, no pull request, nothing on the website |
| Failed stage | Up to two documented fix-and-retry attempts; then continue only with independent stages and mark later products provisional. Pass criteria are never loosened |

## 4. Layout

Code and docs (this repository, branch `ucd-search-pilot`):

```
ucd/
  README.md                 workflow description (motivation, procedure, checks, outputs)
  config/fornax_pilot.yaml  fields, radii, releases, cross-match radii, cut definitions, paths
  lib/                      shared modules: gaia_access, selector, euclid_catalogue, legacy_access,
                            crossmatch, limits, statistics, cutouts, qa_plots, run_state
  stages/stage_0_preflight.py ... stage_8_report.py   one script per stage
docs/ucd_pilot_plan.md      this plan
docs/ucd_pilot_run_log.md   aggregate-only copy of the run log (gates, counts, lessons), updated per stage
```

Data, figures and tables (outside git, all under `~/data/euclid/bubbletea/`):

```
reference/                  bubbletea snapshot + manifest.json (hashes, commit id)
runs/<run_id>/
  run_log.md                full log: what ran, checks, problems, lessons (includes object-level detail)
  stage_N_<name>/
    tables/                 Parquet/CSV products
    figures/                QA figures (PNG, LaTeX fonts, scripts/plot_style.py)
    summary.json            metrics, gate verdicts (pass / fail / degraded), inputs with hashes, timings
  report/index.html         local HTML report of the whole run
```

Budgets: sky area <= 10 deg^2; disk <= 10 GB; no new stage starts more than 9 h after the run begins.

## 5. How the autopilot runs

1. Every stage script is first run on a **5 arcmin smoke cone** (under one minute), then on the full fields.
2. Every stage writes `summary.json` with measured metrics and a verdict per gate criterion.
3. Before the next stage starts, Claude (a) reads the previous `summary.json`, (b) opens and inspects the QA figures,
   (c) appends "result, problems, lessons, consequences for the next stage" to the run log, (d) updates
   `docs/todo.md` and `docs/lessons.md`, (e) commits and pushes. The next stage reads the previous stage's products
   and verdicts through `run_state`, and refuses to run on a failed dependency.
4. Long downloads run in the background; the session is kept awake. State lives on disk, so a restart resumes at the
   first stage without a passed gate.
5. Failure handling follows the "diagnose, retry, then degrade" decision above.

## 6. Stages

Each stage lists its goal, method, QA figures and gate (pass criteria). Numbers in gates are either structural
(must hold) or measured and reported; no gate depends on recovering a wanted science result.

### Stage 0: preflight and setup

- **Goal:** everything the night needs exists and works.
- **Method:** create the layout; snapshot bubbletea assets (frozen selector JSON + joblib, Fornax reference tables
  incl. Saifollahi et al. 2021 A1/A5/A6, canonical catalogue, host register, Gaia and Legacy cross-matches, M60
  scored sources for the regression test, background-field densities); re-implement the selector from its JSON
  coefficients; test services (ESA Gaia TAP, Euclid TAP, SLAC LSDB DR11 South, Legacy and Euclid cutouts); choose the
  control field (wide survey, full coverage, |b| within 5 deg of Fornax's -53.6 deg, more than 4 deg from NGC 1399,
  away from Fornax A and the Eridanus group, no galaxy brighter than a set limit, similar Gaia density).
- **QA figure:** field map (DR1 tiles, both fields, known Fornax objects, bright galaxies, bright stars).
- **Gate:** selector scores reproduce bubbletea's stored M60 scores to 1e-6; every service answers a small query;
  the control field meets all criteria; snapshot hashes recorded.

### Stage 1: resolution and detection limits

- **Goal:** know, for Gaia and for Euclid, which (r_h, M_V, distance) can be detected and recognised as non-point-like.
- **Method:**
  1. Population: r_h and M_V distributions of confirmed UCDs from the snapshot (non-Fornax and Fornax shown apart).
  2. Detection: Gaia completeness versus Euclid I_E, measured in the control field (fraction of clean compact MER
     sources with a Gaia counterpart); Euclid and Legacy depths from the catalogues.
  3. Euclid resolution, empirical: locus and scatter of secure Gaia stars (significant parallax or proper motion) in
     `mumax_minus_mag`, Sersic radius and `point_like_prob` versus magnitude; "resolved" = beyond a stated quantile
     of the stellar locus.
  4. Euclid resolution, simulated: King and Sersic profiles convolved with an empirical VIS PSF (stacked stars),
     with wide-survey noise; smallest r_h distinguishable from a star versus magnitude.
  5. Gaia resolution, empirical: excess noise and BP/RP excess versus angular size for reference UCDs **outside
     Fornax** (hosts with distances).
- **QA figures:** r_h versus M_V with lines of constant angular size and apparent magnitude at 5, 10, 20, 30, 50 Mpc;
  Gaia completeness curve; stellar locus with the resolved threshold; simulated recovered size versus input; summary
  "discovery space" for Gaia alone, Euclid alone and both.
- **Gate:** stellar-locus scatter measured in at least 5 magnitude bins; simulation returns unresolved for point
  sources (false-resolved rate reported, expected at the chosen quantile); limits table written for the full grid.

### Stage 2: Gaia retrieval and scoring

- **Goal:** complete Gaia DR3 tables for both fields with the frozen selector score.
- **Method:** count first, then retrieve all sources (19 selector columns plus quality columns); score; add Voggel
  2020 style flags and parallax / proper-motion significance (with covariance).
- **QA figures:** colour-magnitude diagrams; feature distributions (all, selected, known UCDs); sky maps of selected
  sources; selected density versus bubbletea's random-field range.
- **Gate:** row count equals the count query; unique `source_id`; control-field selected density inside bubbletea's
  95% range for its latitude band (else flagged, not fatal); recovery of known Gaia-matched Fornax objects reported.
  Note: the selector's training set includes Fornax objects, so this recovery is a consistency check, not a test.

### Stage 3: Euclid MER cross-match

- **Goal:** Euclid photometry, sizes, shapes, flags, classification and photo-z for every Gaia source.
- **Method:** pull MER wide catalogue + morphology + PHZ rows around the Gaia positions; match by position after
  propagating Gaia (epoch 2016.0) to the tile epoch, and compare with MER's own `gaia_id`; calibrate the match radius
  with displaced-position controls; keep all in-radius candidates and an ambiguity flag; resolve tile-overlap
  duplicates; record coverage, saturation, `spurious_flag`, `det_quality_flag`, shredding (`parent_id`).
- **QA figures:** separation histogram with the random-offset control; match fraction versus G; G versus I_E;
  compactness diagrams (`mumax_minus_mag` and Sersic radius versus magnitude) with stars, galaxies and known UCDs.
- **Gate:** false-match rate from offsets below 1% at the adopted radius; agreement between the positional match and
  `gaia_id` reported (disagreements listed); G - I_E versus colour consistent between the two fields.

### Stage 4: Legacy Surveys DR11 South cross-match

- **Goal:** grz (+W1, W2) photometry and Tractor morphology.
- **Method:** LSDB cross-match on the SLAC server; type, shape, fluxes with inverse variances, mask bits, fracflux;
  same radius calibration and ambiguity bookkeeping as Stage 3.
- **QA figures:** separation histogram; g - r versus r - z with the stellar locus; DR11 versus MER DECam fluxes;
  DR11 versus DR10 for a subset.
- **Gate:** false-match rate below 1%; photometric offsets between DR11 and MER DECam fluxes measured per band.
  If the service fails after retries, later stages run on Gaia + Euclid and are marked provisional.

### Stage 5: contaminant rejection and candidate tiers

- **Goal:** a transparent cut flow from all Gaia sources to promising candidates.
- **Method:** every criterion is a boolean column; nothing is deleted. Criteria come from Stage 1 limits, from the
  control field, and from reference UCDs **outside Fornax**:
  1. Gaia: frozen selector score; no significant parallax or proper motion.
  2. Euclid quality: covered, not spurious, not saturated, not a shredded fragment of a large galaxy.
  3. Euclid size: resolved beyond the stellar locus, and smaller than the angular size of a 100 pc object at the
     host distance (for hostless fields: stated in arcsec).
  4. Shape: round and compact (ellipticity, Sersic fit quality).
  5. Colour: within the old-stellar-population locus in grz and I_E, Y, J, H defined from non-Fornax reference UCDs.
  6. Information only, never a veto tonight: `phz_glob_cl_prob` and the other PHZ probabilities, photo-z, Tractor
     type, Gaia galaxy/QSO candidate membership.
  Tiers A / B / C from the number and strength of criteria met.
- **QA figures:** cut-flow bars for Fornax and control; size-magnitude and colour-colour diagrams of survivors with
  known objects; recovery of known objects after each cut.
- **Gate:** contamination reduction measured (control-field survivors per deg^2 after each cut); recovery of known
  objects reported per cut with every miss explained in the run log; the control-field survivor list doubles as the
  first "middle of nowhere" search.

### Stage 6: spatial distribution and background statistics

- **Goal:** is there an excess of candidates around NGC 1399, and how significant?
- **Method:** effective area from the coverage MOC and masks (random-point test); radial surface-density profile
  around NGC 1399 per tier; background from the control field with Poisson (Garwood) intervals and a field-to-field
  term (control field split into cells; bubbletea's measured factor ~1.18); excess and significance per annulus and
  in total; 2-D map with the cluster galaxies.
- **QA figures:** radial profile with background band; 2-D density map; cumulative excess.
- **Gate:** random-point area test passes (recovered area within 1% of the MOC area); profile and significance
  written with uncertainties. A null result passes.

### Stage 7: cutouts, colour composites, visual triage

- **Goal:** look at the objects.
- **Method:** small Euclid VIS, Y, J, H cutouts and Legacy DR11 grz cutouts; colour composites; contact sheets for
  (a) known Fornax UCDs, (b) top new candidates, (c) control-field survivors; Claude's note and flag per object in a
  separate column.
- **QA figures:** the three contact sheets; one annotated example per visual class.
- **Gate:** cutouts for at least 95% of the listed objects (failures listed); triage file written.

### Stage 8: synthesis

- **Goal:** a workflow others can repeat and improve.
- **Method:** local HTML report; `ucd/README.md` with the standard workflow; aggregate results, limits and the list
  of calibration knobs in the docs; a single ADQL pre-selection for future runs that pulls only candidate-like Gaia
  sources (derived from tonight's cut flow, to be validated next); recommended next fields (Fornax A, Dorado,
  NGC 1291 / NGC 1433 for the disc-galaxy case); review section in `docs/todo.md`; lessons.
- **Gate:** every stage has a verdict; the report opens; final commit pushed.

## 7. Risks seen in advance

- Only about a third of the known Fornax objects have Gaia ids, so a Gaia-seeded search cannot recover the rest;
  recovery is always reported for "in Gaia" and "all" separately.
- Many known UCDs at 20 Mpc are at or below one VIS pixel in r_h; Euclid may resolve only the larger ones. Stage 1
  measures this instead of assuming it.
- Photo-z cannot confirm a z ~ 0.005 object; it can only flag background galaxies, and bright-compact sources often
  get poor photo-z.
- Gaia (2016.0) and Euclid (about 2024.6) epochs differ by ~8.6 yr; stars with proper motion shift, UCDs do not.
- MER shreds large galaxies and the sky near NGC 1399 is crowded; fragments can mimic compact sources.
- Legacy DR11 identifiers differ from DR10, and bubbletea saw dark DR11 cutout layers; cutouts fall back to DR10.
- Cluster environment: the 1 deg field lies inside the virial radius, so the control field, not an outer annulus,
  sets the background.
