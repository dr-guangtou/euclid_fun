# SPEC: Euclid DR1 knowledge base and demos

## Goals

1. Understand the content and data model of every product released in Euclid DR1.
2. Retrieve cutout images (VIS + NISP, plus auxiliary maps) around arbitrary coordinates.
3. Know the processing steps and known issues, with emphasis on low-surface-brightness (LSB)
   imaging: background subtraction, scattered light, ghosts, persistence, PSF wings, masks.
4. Provide a searchable knowledge base, a runnable demo, and a single-file HTML quick guide.

## Layout

| Path | Role |
|---|---|
| `kb/00_index.md` | Entry point of the knowledge base; links to every note |
| `kb/NN_*.md` | Topical syntheses (overview, data model, access, processing, PSF, LSB, known issues, ..., 14 HATS/LSDB) |
| `kb/papers/*.md` | One structured summary per A&A DR1-Foundation paper |
| `scripts/` | `fetch_sources.sh`, `fetch_arxiv_extra.sh` (archive), `extract_text.py` (text), `dump_tap_schema.py` (TAP dump), `kb_search.py` (FTS5 index + search), `build_guide.py` (builds the multi-page guide site and the single-file version from `guide/src/`), `plot_style.py` |
| `kb/data_model/` | DPDD notes, `verified_on_archive.md` (hands-on facts, authoritative), `tap/` column dump |
| `kb/expsup/`, `kb/web/` | Explanatory Supplement notes; ESA pages, memos, help pages, astroquery docs |
| `demo/` | `dr1_access.py` helpers, `targets.py`, steps `01`-`08` + `download_lsb_tiles.py` (see `demo/README.md`); `06` = IRSA HATS/LSDB check, `07` = fragment flags, `08` = footprint MOC, `09` = calibrated-frame cutouts by HTTP range reads |
| `figures/` | Publication-quality PNG figures produced by the demo |
| `guide/src/` -> `guide/site/` (+ `guide/euclid_dr1_quick_guide.html`) | HTML quick guide: page sources and shared template (`_template.html`); built site with `index.html` and one page per topic, figures in `site/figures/`; plus an all-in-one self-contained file. Page order is `page_order` in `scripts/build_guide.py`. Links written as `#id` are rewritten to the page holding that id |
| `.gitignore`, `.pre-commit-config.yaml` | Git repository (`origin` = `github.com/dr-guangtou/euclid_fun`, public). Untracked: `.venv/`, caches, data files, the search index, the built guide (`guide/site/`, single-file HTML) |
| `~/Desktop/euclid/` | Archive: PDFs, mirrored web pages, extracted plain text (not in this folder, never in git) |
| `~/data/euclid/dr1_demo/` | Downloaded DR1 data (budget about 15 GB; ~12 GB used): tiles, cutouts, catalogues, one NIR frame (`frames/`), VMPZ samples (`vmpz/`), footprint MOCs (`footprint/`) |
| `~/data/euclid/hats_cache/` | Saved LSDB/HATS query results and the HATS-derived MOC (tens of MB) |

## Search

`scripts/kb_search.py` builds an SQLite FTS5 index (`kb/kb_index.sqlite`) over:
- every markdown note in `kb/`, and
- the extracted full text of the papers and Explanatory Supplement in `~/Desktop/euclid/text/`.

Results show the source file, the section/page and a snippet.

## Demo target selection

Galaxy examples are taken from objects featured in the DR1 papers (user decision), covering
several morphological types (e.g. large spiral, early type, dwarf/LSB, edge-on, interacting/tidal,
lens), so the demo doubles as a gallery of DR1 image quality.

## Precedence of information

1. `kb/data_model/verified_on_archive.md` and `demo/` results (hands-on, release day);
2. Explanatory Supplement release notes and archive known-issue pages;
3. DPDD; 4. DR1 papers; 5. Q1 papers (only where DR1 papers defer to them).
Discrepancies are listed in `kb/11_known_issues.md`.
