"""Run bookkeeping: configuration, stage folders, summaries with gate verdicts, and the run log."""

import datetime
import hashlib
import json
from pathlib import Path

import numpy as np
import yaml

repository_root = Path(__file__).resolve().parents[2]
default_config_path = repository_root / "ucd" / "config" / "fornax_pilot.yaml"


def load_config(path: Path = default_config_path) -> dict:
    return yaml.safe_load(Path(path).read_text())


def expand(path: str) -> Path:
    return Path(path).expanduser()


def data_root(config: dict) -> Path:
    return expand(config["data_root"])


def reference_dir(config: dict) -> Path:
    return data_root(config) / "reference"


def run_dir(config: dict) -> Path:
    return data_root(config) / "runs" / config["run_id"]


def stage_dir(config: dict, stage_name: str, *, smoke: bool = False) -> Path:
    """Folder of one stage; smoke-test products go to a sibling folder so they never mix with real ones."""
    folder = run_dir(config) / (f"{stage_name}_smoke" if smoke else stage_name)
    for child in ("tables", "figures"):
        (folder / child).mkdir(parents=True, exist_ok=True)
    return folder


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def gate(name: str, criterion: str, measured, passed: bool, *, fatal: bool = True) -> dict:
    """One pass criterion. A failed non-fatal gate marks the stage 'degraded' instead of 'fail'."""
    return {"name": name, "criterion": criterion, "measured": measured, "passed": bool(passed), "fatal": fatal}


def json_safe(value):
    if isinstance(value, dict):
        return {str(key): json_safe(item) for key, item in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [json_safe(item) for item in value]
    if isinstance(value, np.generic):
        value = value.item()
    if isinstance(value, float) and not np.isfinite(value):
        return None
    if isinstance(value, Path):
        return str(value)
    return value


def write_summary(
    config: dict, stage_name: str, metrics: dict, gates: list[dict], *, smoke: bool = False, notes: list[str] = ()
) -> dict:
    failed = [item for item in gates if not item["passed"]]
    if any(item["fatal"] for item in failed):
        verdict = "fail"
    elif failed:
        verdict = "degraded"
    else:
        verdict = "pass"
    summary = {
        "stage": stage_name,
        "run_id": config["run_id"],
        "smoke_test": smoke,
        "written_utc": datetime.datetime.now(datetime.UTC).isoformat(timespec="seconds"),
        "verdict": verdict,
        "gates": gates,
        "metrics": metrics,
        "notes": list(notes),
    }
    path = stage_dir(config, stage_name, smoke=smoke) / "summary.json"
    path.write_text(json.dumps(json_safe(summary), indent=2))
    print(f"[{stage_name}{' smoke' if smoke else ''}] verdict: {verdict}")
    for item in gates:
        mark = "PASS" if item["passed"] else ("FAIL" if item["fatal"] else "WARN")
        print(f"  {mark}  {item['name']}: {item['measured']}  (criterion: {item['criterion']})")
    return summary


def read_summary(config: dict, stage_name: str) -> dict:
    return json.loads((run_dir(config) / stage_name / "summary.json").read_text())


def require_stages(config: dict, stage_names: list[str]) -> dict[str, dict]:
    """Summaries of the stages this one depends on; refuses to continue on a failed or missing dependency."""
    summaries = {}
    for name in stage_names:
        path = run_dir(config) / name / "summary.json"
        if not path.exists():
            raise RuntimeError(f"dependency {name} has not been run")
        summaries[name] = json.loads(path.read_text())
        if summaries[name]["verdict"] == "fail":
            raise RuntimeError(f"dependency {name} failed its gate; fix it before running this stage")
    return summaries


def load_fields(config: dict) -> dict:
    """Field definitions fixed by stage 0 (target from the configuration, control chosen there)."""
    return json.loads((run_dir(config) / "stage_0_preflight" / "tables" / "fields.json").read_text())


def smoke_fields(config: dict, fields: dict) -> dict:
    """Same field centres with the small smoke-test radius."""
    radius = config["smoke_test"]["radius_deg"]
    return {name: {**field, "radius_deg": radius} for name, field in fields.items()}


def append_log(config: dict, text: str) -> None:
    path = run_dir(config) / "run_log.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    with open(path, "a") as handle:
        handle.write(f"\n<!-- {stamp} -->\n{text.rstrip()}\n")
