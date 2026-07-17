from __future__ import annotations

import argparse
import hashlib
import json
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any


EXPECTED_TARGET_COUNT = 13
PRIMARY_HUES = (0, 60, 120, 180, 240, 300)


def analyze_strip_hsi_pilot(run_dir: str | Path) -> dict[str, Any]:
    root = Path(run_dir)
    run = _load_json(root / "run.json")
    if run.get("phase") != "P7-pilot" or run.get("status") != "complete":
        raise ValueError("P7 pilot analysis requires a completed P7-pilot run")
    if int(run.get("completed_target_count", -1)) != EXPECTED_TARGET_COUNT:
        raise ValueError("P7 pilot analysis requires 13 completed targets")
    if (root / "failure.json").exists():
        raise ValueError("P7 pilot run contains failure.json")
    python_cleanup = _load_json_value(root / "all-off-python.json")
    shell_cleanup = _load_json_value(root / "all-off-shell.json")
    if not _cleanup_ok(python_cleanup) or not _cleanup_ok(shell_cleanup):
        raise ValueError("P7 pilot requires successful Python and shell cleanup")
    if list(root.rglob("*.npy")):
        raise ValueError("P7 pilot must not retain .npy files")

    captures = _load_jsonl(root / "captures.jsonl")
    capture_validation = _validate_captures(captures)
    rows = _load_jsonl(root / "target-results.jsonl")
    if len(rows) != EXPECTED_TARGET_COUNT:
        raise ValueError(f"P7 target-results must contain 13 rows, found {len(rows)}")
    by_target = {}
    for row in rows:
        target = row["target"]
        key = (int(target["hue"]), int(target["sat"]))
        if key in by_target:
            raise ValueError(f"duplicate P7 target row: {key}")
        by_target[key] = row
    expected = {(0, 0)} | {(hue, sat) for hue in PRIMARY_HUES for sat in (50, 100)}
    if set(by_target) != expected:
        raise ValueError("P7 target grid is incomplete or contains unexpected points")

    points = [_point_summary(by_target[key]) for key in sorted(by_target)]
    hue_branches = []
    targeted_search = []
    for hue in PRIMARY_HUES:
        sat50 = by_target[(hue, 50)]
        sat100 = by_target[(hue, 100)]
        faithful50 = _faithful(sat50)
        faithful100 = _faithful(sat100)
        if faithful100:
            branch = "full_range_faithful"
            bracket = [100, 100]
        elif faithful50:
            branch = "boundary_bracket_50_100"
            bracket = [50, 100]
            targeted_search.append({"hue": hue, "lower_faithful_sat": 50, "upper_unconfirmed_sat": 100})
        else:
            branch = "boundary_below_50_or_hue_unreachable"
            bracket = [0, 50]
            targeted_search.append({"hue": hue, "lower_faithful_sat": 0, "upper_unconfirmed_sat": 50})
        hue_branches.append({"hue": hue, "sat50_faithful": faithful50, "sat100_faithful": faithful100, "branch": branch, "initial_boundary_bracket": bracket})

    unavailable = [point for point in points if point["status"] == "measurement_unreachable"]
    faithful = [point for point in points if point["gamut_status"] == "faithful"]
    return {
        "schema_version": 1,
        "analysis": "strip_hsi_pilot_gate6_preflight",
        "status": "ready_for_p7_branch_review",
        "run_dir": str(root),
        "run_json_sha256": _sha256(root / "run.json"),
        "capture_validation": capture_validation,
        "cleanup": {"python": python_cleanup, "shell": shell_cleanup},
        "point_count": len(points),
        "faithful_point_count": len(faithful),
        "measurement_unreachable_point_count": len(unavailable),
        "points": points,
        "hue_branches": hue_branches,
        "targeted_boundary_search": targeted_search,
        "decision_hints": {
            "automatic_gate6_selection": False,
            "pilot_complete_for_all_hues": not unavailable,
            "all_primary_hues_sat50_faithful": all(item["sat50_faithful"] for item in hue_branches),
            "all_primary_hues_sat100_faithful": all(item["sat100_faithful"] for item in hue_branches),
            "next_action": "targeted_s_exact_max_search" if targeted_search and not unavailable else ("random_holdout" if not targeted_search else "repair_measurement"),
        },
        "notes": [
            "Unconfirmed is not equivalent to physically unreachable; it only means the settled pilot gate was not proven.",
            "Exact gamut boundaries require targeted search inside each reported bracket.",
            "This analyzer does not freeze Gate-6 or install a runtime LUT.",
        ],
    }


def _point_summary(row: Mapping[str, Any]) -> dict[str, Any]:
    target = row["target"]
    if row.get("status") == "measurement_unreachable":
        return {"hue": int(target["hue"]), "sat": int(target["sat"]), "status": "measurement_unreachable", "gamut_status": "unconfirmed", "stage": row.get("stage")}
    feedback = row["feedback"]
    best = feedback["best"]["objective"]
    return {
        "hue": int(target["hue"]),
        "sat": int(target["sat"]),
        "status": "complete",
        "gamut_status": row["gamut_status"],
        "goal_confirmed": bool(feedback["goal_confirmed"]),
        "selected_command": row["selected_command"],
        "active_channel": feedback["active_channel"],
        "hue_error_degrees": best.get("hue_error_degrees"),
        "sat_error_percent": best.get("sat_error_percent"),
        "orthogonal_residual": best.get("orthogonal_residual"),
        "rounds_completed": int(feedback["rounds_completed"]),
        "settled_evidence_count": sum(len(item.get("sample_indices", [])) for item in feedback["confirmation_attempts"]) + len(row.get("final_verification", [])),
    }


def _faithful(row: Mapping[str, Any]) -> bool:
    return row.get("status") == "complete" and row.get("gamut_status") == "faithful"


def _validate_captures(captures: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    raw_count = 0
    recorded_count = 0
    measurement_count = 0
    for record in captures:
        capture = record.get("capture", {})
        raw_path = Path(str(capture.get("capture", {}).get("saved_file", "")))
        if not raw_path.is_file() or raw_path.stat().st_size <= 0:
            raise ValueError(f"missing or empty CR3 for {record.get('capture_id')}")
        raw_count += 1
        report_path = Path(str(capture.get("patch_statistics", "")))
        if not report_path.is_file():
            raise ValueError(f"missing measurement report for {record.get('capture_id')}")
        measurement_count += 1
        report = _load_json(report_path)
        if report.get("exposure_metadata", {}).get("status") != "recorded":
            raise ValueError(f"capture {record.get('capture_id')} lacks recorded exposure")
        recorded_count += 1
    return {"capture_count": len(captures), "raw_count": raw_count, "measurement_count": measurement_count, "recorded_exposure_count": recorded_count, "npy_count": 0}


def _cleanup_ok(value: Any) -> bool:
    steps = value.get("steps") if isinstance(value, Mapping) else value
    return isinstance(steps, list) and len(steps) == 2 and all(isinstance(step, Mapping) and step.get("ok") is True for step in steps)


def _load_json(path: Path) -> dict[str, Any]:
    value = _load_json_value(path)
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value


def _load_json_value(path: Path) -> Any:
    if not path.is_file():
        raise ValueError(f"missing required file: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.is_file():
        raise ValueError(f"missing required file: {path}")
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_strip_hsi_pilot_analysis(output: str | Path, analysis: Mapping[str, Any]) -> Path:
    path = Path(output)
    path.write_text(json.dumps(analysis, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8")
    return path


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Analyze a completed P7 strip HSI pilot.")
    parser.add_argument("run_dir", type=Path)
    parser.add_argument("--output", type=Path)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    analysis = analyze_strip_hsi_pilot(args.run_dir)
    print(write_strip_hsi_pilot_analysis(args.output or args.run_dir / "strip-hsi-pilot-analysis.json", analysis))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
