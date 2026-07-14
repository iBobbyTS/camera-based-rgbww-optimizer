from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path
from typing import Any, Mapping, Sequence

from camera_based_rgbww_optimizer.measurement import raw_observer_analysis


DEFAULT_OUTPUT_NAME = "analysis.json"


def load_validation_reports(
    run_dir: str | Path,
    *,
    require_complete: bool = True,
) -> list[dict[str, Any]]:
    """Load P1 reports and restore immutable capture provenance into each report."""

    root = Path(run_dir)
    run = _read_object(root / "run.json")
    plan = _read_object(root / "plan.json")
    if require_complete and run.get("status") != "complete":
        raise ValueError(f"P1 run is not complete: {run.get('status')}")
    planned = plan.get("captures")
    if not isinstance(planned, list) or not planned:
        raise ValueError("P1 plan has no captures")
    records = _read_jsonl(root / "captures.jsonl")
    records_by_id = {str(record.get("capture_id")): record for record in records}
    if len(records_by_id) != len(records):
        raise ValueError("P1 captures.jsonl contains duplicate capture_id values")
    missing = [str(step.get("capture_id")) for step in planned if str(step.get("capture_id")) not in records_by_id]
    if missing and require_complete:
        raise ValueError(f"P1 run is missing capture records: {missing}")

    reports: list[dict[str, Any]] = []
    for step in planned:
        capture_id = str(step["capture_id"])
        record = records_by_id.get(capture_id)
        if record is None:
            continue
        captured = record.get("capture")
        if not isinstance(captured, Mapping):
            raise ValueError(f"capture {capture_id} has no capture payload")
        statistics_path = captured.get("patch_statistics")
        if not isinstance(statistics_path, str) or not statistics_path:
            raise ValueError(f"capture {capture_id} has no patch_statistics path")
        report = _read_object(Path(statistics_path))
        context = report.get("analysis_context")
        merged_context = dict(context) if isinstance(context, Mapping) else {}
        camera = captured.get("capture")
        merged_context.update(
            {
                "capture_id": capture_id,
                "source": str(step["source"]),
                "purpose": str(step["purpose"]),
                "repeat_index": step.get("repeat_index"),
                "exposure_factor": step.get("exposure_factor"),
                "shutter_speed": camera.get("shutter_speed") if isinstance(camera, Mapping) else None,
            }
        )
        report["analysis_context"] = merged_context
        reports.append(report)
    if not reports:
        raise ValueError("P1 run has no readable patch-statistics reports")
    return reports


def analyze_validation_run(
    run_dir: str | Path,
    *,
    require_complete: bool = True,
) -> dict[str, Any]:
    reports = load_validation_reports(run_dir, require_complete=require_complete)
    signal_reports = [report for report in reports if _context_value(report, "source") != "ambient"]
    paired_by_source = {
        source: [
            report
            for report in signal_reports
            if _context_value(report, "source") == source
            and _context_value(report, "purpose") == "paired_repeat"
        ]
        for source in ("ray", "strip")
    }
    repeatability = {
        source: raw_observer_analysis.analyze_repeatability(group)
        for source, group in paired_by_source.items()
        if group
    }
    linearity: dict[str, Any] = {}
    for source in ("ray", "strip"):
        groups: dict[float, list[dict[str, Any]]] = {}
        for report in signal_reports:
            if _context_value(report, "source") != source or _context_value(report, "purpose") != "linearity_bracket":
                continue
            factor = _context_value(report, "exposure_factor")
            if factor is None:
                raise ValueError(f"linearity capture for {source} has no exposure_factor")
            groups.setdefault(float(factor), []).append(report)
        if len(groups) >= 2:
            linearity[source] = raw_observer_analysis.analyze_exposure_linearity(
                groups,
                repeatability.get(source),
            )

    return {
        "schema_version": 1,
        "analysis": "raw_observer_validation_run",
        "run_dir": str(Path(run_dir)),
        "status": "ready_for_manual_branch_review",
        "report_count": len(reports),
        "signal_report_count": len(signal_reports),
        "repeatability": repeatability,
        "linearity": linearity,
        "green_consistency": raw_observer_analysis.analyze_green_consistency(signal_reports),
        "quality_threshold_recommendation": raw_observer_analysis.recommend_quality_thresholds(signal_reports),
        "notes": [
            "No P1 pass/fail conclusion or observer-config update is inferred automatically.",
            "Review repeatability, linearity, G1/G2 context, source isolation, and cleanup evidence against PLAN.md sections 7.4-7.7.",
        ],
    }


def write_validation_analysis(path: str | Path, analysis: Mapping[str, Any]) -> Path:
    output = Path(path)
    output.write_text(json.dumps(analysis, ensure_ascii=False, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8")
    return output


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Analyze a completed native Bayer P1 validation run.")
    parser.add_argument("run_dir", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--allow-incomplete", action="store_true")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    analysis = analyze_validation_run(args.run_dir, require_complete=not args.allow_incomplete)
    output = args.output or args.run_dir / DEFAULT_OUTPUT_NAME
    print(write_validation_analysis(output, analysis))
    return 0


def _context_value(report: Mapping[str, Any], name: str) -> Any:
    context = report.get("analysis_context")
    return context.get(name) if isinstance(context, Mapping) else None


def _read_object(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"expected JSON object: {path}")
    return copy.deepcopy(data)


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.is_file():
        raise ValueError(f"missing JSONL file: {path}")
    values: list[dict[str, Any]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        value = json.loads(line)
        if not isinstance(value, dict):
            raise ValueError(f"expected JSON object at {path}:{line_number}")
        values.append(value)
    return values


if __name__ == "__main__":
    raise SystemExit(main())
