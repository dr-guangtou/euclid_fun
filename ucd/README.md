# UCD candidate search: Gaia + Euclid DR1 + Legacy Surveys

A staged, checked workflow to find ultra-compact dwarf (UCD) candidates anywhere in the Euclid DR1 footprint.
It is the Euclid extension of the Gaia-only project `bubbletea`. Plan and decisions:
[docs/ucd_pilot_plan.md](../docs/ucd_pilot_plan.md). Results of the first run (aggregate numbers only):
[docs/ucd_pilot_run_log.md](../docs/ucd_pilot_run_log.md).

## Idea

1. **Start from Gaia.** Gaia photometry and astrometry are the core: a UCD is a Gaia source that is not a point
   source and does not move. bubbletea's frozen selector (9 Gaia features, logistic model) removes stars, binaries
   and QSOs but keeps about 87% of background galaxies.
2. **Let Euclid separate the survivors.** At the Gaia position, Euclid VIS (0.1" pixels) tells stars, compact stellar
   systems and galaxies apart by how concentrated the light is, and gives an independent proper-motion test from the
   9 years between Gaia (2016.0) and Euclid.
3. **Use Legacy Surveys for colours.** grz colours remove red background galaxies.
4. **Compare with a control field.** Whatever survives in a field without a host sets the background.

## Stages

Each stage is one script, `uv run python -m ucd.stages.<name> [--smoke]`, reads `ucd/config/fornax_pilot.yaml`,
writes tables, QA figures and a `summary.json` with pass criteria ("gates") to
`~/data/euclid/bubbletea/runs/<run_id>/<stage>/`, and refuses to run on a failed dependency. `--smoke` runs a
5 arcmin cone in about a minute.

| Order | Script | What it does | Main checks |
|---|---|---|---|
| 1 | `stage_0_preflight` | Snapshot of bubbletea inputs with hashes; selector reproduced; services tested; control field chosen | selector scores equal bubbletea's; control field criteria |
| 2 | `stage_2_gaia` | All Gaia DR3 sources of each field (NOIRLab Data Lab), frozen selector score, motion flags | row counts equal count queries; density inside bubbletea's range |
| 3 | `stage_3_euclid` | Euclid MER entry at each Gaia position; coverage flag; per-tile epoch fit; displacement test | chance-match rate < 1%; displacement threshold validated on stars |
| 4 | `stage_4_legacy` | Legacy Surveys DR11 South entry (by Tractor's Gaia reference id, else by position) | chance-match rate < 1%; photometric offsets measured |
| 5 | `stage_1_limits` | Gaia completeness versus Euclid magnitude; stellar locus; simulated size shift; limits grid | locus in >= 5 magnitude bins; simulation consistent with catalogue |
| 6 | `stage_5_cutflow` | Nine boolean cuts, tiers A-D, galaxy-sequence information column | contamination reduction and recovery of known objects reported |
| 7 | `stage_6_statistics` | Effective area, radial profile around the host, excess over the control field | three area estimates agree; a null result passes |
| 8 | `stage_7_cutouts` | 12" Euclid and Legacy cutouts, colour composites, contact sheets, triage template | images for >= 95% of objects |
| 9 | `stage_8_report` | Local HTML report, public run log, Gaia pre-selection query | no identifiers in public files; disk budget |

The limits stage has number 1 but runs fifth, because its empirical parts need the matched tables.

## The cuts (stage 5)

| Cut | Definition | Where the number comes from |
|---|---|---|
| Gaia selector | bubbletea `point_source_logistic_model_v1`, probability >= 0.8278, 11.26 <= G <= 21.76 | frozen in bubbletea |
| No secure Gaia motion | parallax and proper motion below 5 sigma | convention |
| Euclid entry | inside catalogue coverage (an entry within 20") and an entry within the calibrated match radius | radius: largest with < 1% chance matches |
| Euclid quality | VIS-detected, not spurious, not saturated or at a border, inside the magnitude range of the stellar locus | MER flags |
| Not a moving star | not (compact and displaced since Gaia 2016.0 by more than the calibrated threshold) | threshold from stars with Gaia proper motions |
| Resolved | `mu_max - mag` above the 99% quantile of clean single stars at that magnitude | control-field stars |
| Size in range | compactness and Sersic radius not larger than a 100 pc object at the host distance | simulation with an empirical VIS PSF |
| Round | ellipticity < 0.4 | convention |
| Colour | Legacy g-r and r-z inside the box of confirmed Virgo UCDs (1-99%, padded by 0.05) | bubbletea reference outside the target |

Tiers: **A** all cuts and size up to the 95th percentile of reference UCDs; **B** all cuts, larger (up to 100 pc);
**C** exactly one of roundness or colour failed; **D** outside Euclid catalogue coverage (Gaia and Legacy only).
Known objects of the target field are never used to set a number; they only measure recovery.
Photo-z and the PHZ class probabilities are stored but not used.

## Calibration knobs

All in the stage scripts or the YAML file, each with a QA figure:
match radii (stages 3, 4); coverage radius (20"); displacement threshold and the compactness limit below which it
applies (stage 3); stellar-locus quantile (99%) and the definition of clean stars (stage 1); maximum and typical
size (stage 5); ellipticity limit; colour box and its reference sample; galaxy-sequence quantile (5%, information
only); annuli and the field-to-field term (stage 6).

## Running a new field

1. Copy `config/fornax_pilot.yaml`, set `run_id`, the target position, radius, host distance (or an angular size
   limit for a hostless field), and the control-field rules.
2. Run the stages in the order of the table, each first with `--smoke`.
3. Read `summary.json` and the figures of a stage before starting the next one, and record the result in the run log.
4. For large areas, use `config/candidate_preselection.adql` to pull only candidate-like Gaia sources.

## Rules

- Data, tables, cutouts and figures live in `~/data/euclid/bubbletea/`, never in this repository.
- This repository is public: no coordinates or identifiers of candidates or known objects in any committed file.
- bubbletea is read-only; its inputs are a hashed snapshot in `~/data/euclid/bubbletea/reference/`.
