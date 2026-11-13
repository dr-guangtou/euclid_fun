"""Stage 8: synthesis. Local HTML report, public (aggregate-only) run log, and a Gaia pre-selection query.

Usage: uv run python -m ucd.stages.stage_8_report
Products: runs/<run_id>/report/index.html (local, with figures), docs/ucd_pilot_run_log.md (aggregate only),
          ucd/config/candidate_preselection.adql, stage_8_report/tables/final_candidates_<field>.csv, summary.json
"""

import html
import json
import re

import numpy as np
import pandas as pd

from ucd.lib import run_state

stage_name = "stage_8_report"
stage_order = [
    ("stage_0_preflight", "Stage 0: preflight"),
    ("stage_2_gaia", "Stage 2: Gaia retrieval and frozen selector"),
    ("stage_3_euclid", "Stage 3: Euclid cross-match and displacement"),
    ("stage_4_legacy", "Stage 4: Legacy Surveys DR11 South"),
    ("stage_1_limits", "Stage 1: detection and resolution limits"),
    ("stage_5_cutflow", "Stage 5: cut flow and tiers"),
    ("stage_6_statistics", "Stage 6: spatial statistics"),
    ("stage_7_cutouts", "Stage 7: cutouts and visual triage"),
]
retention_target = 0.995


def preselection_query(config: dict, tables: dict) -> tuple[str, dict]:
    """Simple ADQL pre-filter that keeps (almost) every selector-passed source while dropping most stars."""
    combined = pd.concat(tables.values(), ignore_index=True)
    passed = combined["selector_selected"] & combined["selector_in_valid_g_range"]
    no_motion = ~(
        (combined["parallax_significance"] > 5)
        | ((combined["pmra"] / combined["pmra_error"]) ** 2 + (combined["pmdec"] / combined["pmdec_error"]) ** 2 > 50)
    )
    significance = combined["astrometric_excess_noise_sig"]
    threshold = float(np.floor(significance[passed & no_motion].quantile(1 - retention_target) * 10) / 10)
    prefilter = (
        no_motion
        & (significance > threshold)
        & combined["phot_g_mean_mag"].between(11.26291847229004, 21.75798797607422)
    )
    known = combined["known_state"] == "confirmed"
    statistics = {
        "excess_noise_significance_threshold": threshold,
        "all_sources": len(combined),
        "kept_by_prefilter": int(prefilter.sum()),
        "reduction_factor": float(len(combined) / max(prefilter.sum(), 1)),
        "selector_passed": int(passed.sum()),
        "selector_passed_kept": int((passed & prefilter).sum()),
        "selector_passed_retention": float((passed & prefilter).sum() / passed.sum()),
        "tier_a_or_b": int(combined["tier"].isin(["A", "B"]).sum()),
        "tier_a_or_b_kept": int((combined["tier"].isin(["A", "B"]) & prefilter).sum()),
        "known_confirmed_selector_passed": int((known & passed).sum()),
        "known_confirmed_selector_passed_kept": int((known & passed & prefilter).sum()),
        "status": "derived from the two pilot fields; validate on an independent field before relying on it",
    }
    settings = config["gaia"]
    query = f"""-- Gaia pre-selection of UCD-like sources (pilot: {config["run_id"]}).
-- In the two pilot fields it keeps {statistics["kept_by_prefilter"]} of {statistics["all_sources"]} Gaia sources,
-- {statistics["tier_a_or_b_kept"]} of {statistics["tier_a_or_b"]} tier A or B candidates and {statistics["selector_passed_retention"]:.1%} of all sources that pass
-- bubbletea's frozen selector (the rest have Gaia motions above 5 sigma). Apply the frozen selector to the result. Replace the cone by the region of interest. Syntax: {settings["cone_syntax"]} ({settings["tap_url"]}).
SELECT *
FROM {settings["table"]}
WHERE 't' = Q3C_RADIAL_QUERY(ra, dec, <ra_deg>, <dec_deg>, <radius_deg>)
  AND phot_g_mean_mag BETWEEN 11.26291847229004 AND 21.75798797607422
  AND astrometric_excess_noise_sig > {threshold}
  AND (parallax IS NULL OR parallax < 5 * parallax_error)
  AND (pmra IS NULL
       OR (pmra * pmra) / (pmra_error * pmra_error) + (pmdec * pmdec) / (pmdec_error * pmdec_error) < 50)
"""
    return query, statistics


def merge_triage(config: dict, tables: dict, folder) -> dict:
    """Attach the visual notes (if present) to the candidate tables; notes never change tiers."""
    stage_7 = run_state.run_dir(config) / "stage_7_cutouts" / "tables"
    triage_path = stage_7 / "visual_triage.csv"
    counts = {}
    triage = pd.read_csv(triage_path) if triage_path.exists() else None
    for name, frame in tables.items():
        candidates = frame[frame["tier"] != ""].copy()
        if triage is not None:
            notes = triage[triage["field"] == name][["source_id", "visual_flag", "visual_note"]].drop_duplicates(
                "source_id"
            )
            candidates = candidates.merge(notes, on="source_id", how="left")
            counts[name] = (
                candidates.loc[candidates["tier"].isin(["A", "B"]), "visual_flag"]
                .fillna("not inspected")
                .value_counts()
                .to_dict()
            )
        candidates.sort_values(["tier", "euclid_ie_mag"]).to_csv(
            folder / "tables" / f"final_candidates_{name}.csv", index=False
        )
    return {"triage_file_present": triage is not None, "visual_flags_tier_a_b": counts}


def public_run_log(config: dict) -> str:
    """Run log without object-level blocks (fenced tables are local only)."""
    text = (run_state.run_dir(config) / "run_log.md").read_text()
    text = re.sub(r"\n[^\n]*\(object-level, local log only\):\n\n```.*?```\n", "\n", text, flags=re.S)
    text = re.sub(r"```.*?```", "(object-level block removed from the public copy)", text, flags=re.S)
    text = re.sub(r"\n<!-- [0-9: -]+ -->\n", "\n", text)
    header = (
        "<!-- Generated by ucd/stages/stage_8_report.py from the local run log. Aggregate numbers only: no coordinates\n"
        "     or identifiers of candidates or known objects (public repository). -->\n\n"
    )
    return header + text.strip() + "\n"


def flatten(value, prefix: str = "", depth: int = 0) -> list[tuple[str, str]]:
    rows = []
    if isinstance(value, dict) and depth < 2:
        for key, item in value.items():
            rows += flatten(item, f"{prefix}{key}" if not prefix else f"{prefix} / {key}", depth + 1)
    else:
        text = json.dumps(value) if not isinstance(value, str) else value
        rows.append((prefix, text if len(text) < 600 else text[:600] + " ..."))
    return rows


def build_html(config: dict, summaries: dict, extra: dict) -> str:
    run = run_state.run_dir(config)
    parts = [
        "<!doctype html><html lang='en'><head><meta charset='utf-8'>",
        f"<title>UCD pilot report: {html.escape(config['run_id'])}</title>",
        "<style>body{font:15px/1.5 -apple-system,Helvetica,Arial,sans-serif;margin:0 auto;max-width:1100px;padding:24px;"
        "color:#1a1a1a;background:#fafafa}h1{font-size:26px}h2{margin-top:44px;border-bottom:2px solid #ddd;padding-bottom:4px}"
        "table{border-collapse:collapse;margin:10px 0;font-size:13px}td,th{border:1px solid #ccc;padding:4px 8px;"
        "vertical-align:top;text-align:left}th{background:#eee}.pass{color:#0a7a3d;font-weight:600}.fail{color:#b3261e;"
        "font-weight:600}.degraded{color:#a15c00;font-weight:600}img{max-width:100%;border:1px solid #ddd;margin:8px 0;"
        "background:#fff}code{background:#eee;padding:1px 4px;border-radius:3px}details{margin:8px 0}"
        ".note{background:#fff8e1;border-left:4px solid #e0a800;padding:8px 12px;margin:12px 0}</style></head><body>",
        f"<h1>UCD candidate search pilot: {html.escape(config['run_id'])}</h1>",
        "<p class='note'>Local report. It contains object-level figures and must not be published "
        "(the repository and its website are public).</p>",
        "<table><tr><th>Stage</th><th>Verdict</th><th>Gates passed</th></tr>",
    ]
    for stage, title in stage_order:
        summary = summaries.get(stage)
        if summary is None:
            parts.append(f"<tr><td>{title}</td><td class='fail'>not run</td><td></td></tr>")
            continue
        passed = sum(gate["passed"] for gate in summary["gates"])
        parts.append(
            f"<tr><td><a href='#{stage}'>{title}</a></td><td class='{summary['verdict']}'>{summary['verdict']}</td>"
            f"<td>{passed} / {len(summary['gates'])}</td></tr>"
        )
    parts.append("</table>")
    parts.append("<h2>Gaia pre-selection for future runs</h2><table>")
    for key, value in extra["preselection"].items():
        parts.append(f"<tr><td>{html.escape(key)}</td><td>{html.escape(str(value))}</td></tr>")
    parts.append("</table>")
    for stage, title in stage_order:
        summary = summaries.get(stage)
        if summary is None:
            continue
        parts.append(f"<h2 id='{stage}'>{title} <span class='{summary['verdict']}'>({summary['verdict']})</span></h2>")
        parts.append("<table><tr><th>Gate</th><th>Criterion</th><th>Measured</th><th></th></tr>")
        for gate in summary["gates"]:
            mark = "pass" if gate["passed"] else ("fail" if gate["fatal"] else "degraded")
            measured = html.escape(json.dumps(gate["measured"]))
            measured = measured if len(measured) < 700 else measured[:700] + " ..."
            parts.append(
                f"<tr><td>{html.escape(gate['name'])}</td><td>{html.escape(gate['criterion'])}</td>"
                f"<td><code>{measured}</code></td><td class='{mark}'>{mark}</td></tr>"
            )
        parts.append("</table><details><summary>Metrics</summary><table>")
        for key, value in flatten(summary["metrics"]):
            parts.append(f"<tr><td>{html.escape(key)}</td><td><code>{html.escape(value)}</code></td></tr>")
        parts.append("</table></details>")
        for figure in sorted((run / stage / "figures").glob("*.png")):
            parts.append(
                f"<p><b>{html.escape(figure.stem)}</b><br><img src='../{stage}/figures/{figure.name}' loading='lazy'></p>"
            )
    log = html.escape((run / "run_log.md").read_text())
    parts.append(f"<h2>Run log</h2><pre style='white-space:pre-wrap;font-size:12.5px'>{log}</pre></body></html>")
    return "\n".join(parts)


def main() -> None:
    config = run_state.load_config()
    run = run_state.run_dir(config)
    folder = run_state.stage_dir(config, stage_name)
    summaries = {}
    for stage, _ in stage_order:
        path = run / stage / "summary.json"
        if path.exists():
            summaries[stage] = json.loads(path.read_text())
    stage_5 = run / "stage_5_cutflow" / "tables"
    tables = {name: pd.read_parquet(stage_5 / f"master_{name}.parquet") for name in ("fornax", "control")}
    query, statistics = preselection_query(config, tables)
    (run_state.repository_root / "ucd" / "config" / "candidate_preselection.adql").write_text(query)
    triage = merge_triage(config, tables, folder)

    report_dir = run / "report"
    report_dir.mkdir(exist_ok=True)
    report_path = report_dir / "index.html"
    report_path.write_text(build_html(config, summaries, {"preselection": statistics}))
    public_path = run_state.repository_root / "docs" / "ucd_pilot_run_log.md"
    public_path.write_text(public_run_log(config))
    leaked = bool(re.search(r"canonical_[0-9a-f]{8}|\b\d{18,19}\b", public_path.read_text()))

    size_gigabytes = sum(path.stat().st_size for path in run_state.data_root(config).rglob("*") if path.is_file()) / 1e9
    verdicts = {stage: summaries[stage]["verdict"] if stage in summaries else "not run" for stage, _ in stage_order}
    metrics = {
        "verdicts": verdicts,
        "preselection": statistics,
        "triage": triage,
        "report": str(report_path),
        "public_run_log": str(public_path),
        "disk_use_gigabytes": size_gigabytes,
    }
    gates = [
        run_state.gate("all_stages_have_verdicts", "every stage has a summary with a verdict", verdicts,
                       all(value != "not run" for value in verdicts.values())),
        run_state.gate("no_failed_stage", "no stage ends with a failed gate", verdicts,
                       all(value != "fail" for value in verdicts.values()), fatal=False),
        run_state.gate("report_written", "local HTML report written", str(report_path), report_path.exists()),
        run_state.gate("public_log_has_no_identifiers", "no object identifiers in the public run log", not leaked, not leaked),
        run_state.gate("disk_budget", f"data folder below {config['budgets']['maximum_disk_gigabytes']} GB",
                       round(size_gigabytes, 2), size_gigabytes < config["budgets"]["maximum_disk_gigabytes"]),
    ]  # fmt: skip
    run_state.write_summary(config, stage_name, metrics, gates)


if __name__ == "__main__":
    main()
