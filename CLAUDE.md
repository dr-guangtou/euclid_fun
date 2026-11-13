# Project rules: euclid_fun (Euclid DR1 knowledge base)

Purpose: a searchable knowledge base and working demos for using Euclid Data Release 1 (DR1)
for extragalactic science (photometry and 2-D modelling of extended, low-to-intermediate
redshift galaxies, including low-surface-brightness work).

## Storage rules (from the user, 2026-11-12)

- Downloads larger than 500 MB go to `~/data/euclid/` (DR1 demo data under `~/data/euclid/dr1_demo/`).
  Never store them in this Dropbox folder.
- Archived source documents (PDFs, mirrored web pages, extracted text) live in `~/Desktop/euclid/`.
  Only summaries, notes and code live here.
- `.venv/` is excluded from Dropbox sync via the `com.dropbox.ignored` xattr; re-apply it if the venv is recreated.

## Git and GitHub (from the user, 2026-11-13)

- Remote: `git@github.com:dr-guangtou/euclid_fun.git` (public). The initial commit went straight to `main`; from now on
  work on feature branches and merge into `main` only with the user's permission.
- Never commit data, credentials, archived source documents (papers, extracted text) or the search index
  `kb/kb_index.sqlite`, which contains that text. The built guide (`guide/site/`, single-file HTML) is generated and
  not tracked.
- Pre-commit runs Ruff from the project environment: `uv run pre-commit install` once per clone.
- The guide is public at https://dr-guangtou.github.io/euclid_fun/, built and deployed by
  `.github/workflows/pages.yml` on pushes to `main`. Write anything in `guide/src/` for a public audience.

## UCD search sub-project (from the user, 2026-11-13)

- Plan and source of truth: `docs/ucd_pilot_plan.md`; code in `ucd/`; sister project: `~/Dropbox/work/project/bubbletea`
  (read-only: never modify it; use the snapshot in `~/data/euclid/bubbletea/reference/`).
- All data, catalogues, cutouts and QA figures of this sub-project go to `~/data/euclid/bubbletea/`. Only code,
  configuration, docs and compact files stay here.
- This repository is public: never commit a table, figure or text that gives coordinates or identifiers of UCD
  candidates or of known objects with our measurements. Docs report aggregate numbers only.
- Known Fornax UCDs are for verification only; never tune a threshold on them.
- Sky-area limit for a run: 10 deg^2 until the user raises it. Gaia DR4 is not public yet (checked 2026-11-13): use DR3.

## Figures

- Publication quality, LaTeX fonts (`text.usetex=True`; a TeX install is available), PNG output.
- Use `scripts/plot_style.py` for the shared style.

## Credentials

- ESA Euclid archive credentials are the environment variables `EUCLID_USER` and `EUCLID_PASS`
  (set in `~/.zprofile`). Code reads them from the environment; never print, log or commit them.

## Conventions

- Python via `uv` only (`uv run ...`, `uv add ...`). Lint/format with `uv run ruff check` / `uv run ruff format`.
- `snake_case` everywhere; English only.
- `docs/SPEC.md` = architecture source of truth; `docs/todo.md` = task tracking; `docs/lessons.md` = mistakes and rationale.
- Knowledge base entry point: `kb/00_index.md`. Full-text search: `uv run python scripts/kb_search.py "query"`.
