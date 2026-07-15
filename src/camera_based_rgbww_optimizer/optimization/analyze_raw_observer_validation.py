from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
from typing import Any, Mapping, Sequence

from camera_based_rgbww_optimizer.measurement import raw_mosaic_patches, raw_observer_analysis, recorded_exposure


DEFAULT_OUTPUT_NAME = "analysis.json"
DEFAULT_RECORDED_OUTPUT_NAME = "analysis-recorded-exposure-v1.json"


def load_validation_reports(
    run_dir: str | Path,
    *,
    require_complete: bool = True,
    recompute_recorded_exposure: bool = False,
    exiftool_executable: str = "exiftool",
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

    ambient_capture = next(
        (
            _capture_payload(records_by_id[str(step["capture_id"])], str(step["capture_id"]))
            for step in planned
            if step.get("source") == "ambient" and str(step["capture_id"]) in records_by_id
        ),
        None,
    )
    if recompute_recorded_exposure:
        location_path = _verified_input_path(plan, "location_config")
        observer_path = _verified_input_path(plan, "raw_observer_config")
        if ambient_capture is None:
            raise ValueError("P1 recorded-exposure recomputation requires an ambient capture")
        ambient_camera = _camera_payload(ambient_capture, "ambient", require_saved_file=True)
        ambient_exposure = recorded_exposure.resolve_recorded_exposure(
            ambient_camera["saved_file"],
            str(ambient_camera["shutter_speed"]),
            executable=exiftool_executable,
        )
    else:
        location_path = None
        observer_path = None
        ambient_camera = None
        ambient_exposure = None

    reports: list[dict[str, Any]] = []
    for step in planned:
        capture_id = str(step["capture_id"])
        record = records_by_id.get(capture_id)
        if record is None:
            continue
        captured = _capture_payload(record, capture_id)
        camera = _camera_payload(captured, capture_id, require_saved_file=recompute_recorded_exposure)
        if recompute_recorded_exposure:
            exposure = recorded_exposure.resolve_recorded_exposure(
                camera["saved_file"],
                str(camera["shutter_speed"]),
                executable=exiftool_executable,
            )
            kwargs: dict[str, Any] = {
                "exposure_seconds": exposure.seconds,
                "location_config_path": location_path,
                "observer_config_path": observer_path,
            }
            if str(step["source"]) != "ambient":
                kwargs.update(
                    {
                        "ambient_raw_file": ambient_camera["saved_file"],
                        "ambient_exposure_seconds": ambient_exposure.seconds,
                    }
                )
            report = dict(raw_mosaic_patches.analyze_raw_file(camera["saved_file"], **kwargs))
            report["exposure_metadata"] = exposure.to_jsonable()
            report["ambient_exposure_metadata"] = (
                None if str(step["source"]) == "ambient" else ambient_exposure.to_jsonable()
            )
        else:
            statistics_path = captured.get("patch_statistics")
            if not isinstance(statistics_path, str) or not statistics_path:
                raise ValueError(f"capture {capture_id} has no patch_statistics path")
            report = _read_object(Path(statistics_path))
        context = report.get("analysis_context")
        merged_context = dict(context) if isinstance(context, Mapping) else {}
        merged_context.update(
            {
                "capture_id": capture_id,
                "source": str(step["source"]),
                "purpose": str(step["purpose"]),
                "repeat_index": step.get("repeat_index"),
                "exposure_factor": step.get("exposure_factor"),
                "shutter_speed": camera.get("shutter_speed"),
                "exposure_seconds": (
                    report.get("exposure_metadata", {}).get("seconds")
                    if isinstance(report.get("exposure_metadata"), Mapping)
                    else report.get("exposure_seconds")
                ),
                "exposure_source": (
                    report.get("exposure_metadata", {}).get("source")
                    if isinstance(report.get("exposure_metadata"), Mapping)
                    else "legacy_report_unspecified"
                ),
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
    recompute_recorded_exposure: bool = False,
    exiftool_executable: str = "exiftool",
) -> dict[str, Any]:
    reports = load_validation_reports(
        run_dir,
        require_complete=require_complete,
        recompute_recorded_exposure=recompute_recorded_exposure,
        exiftool_executable=exiftool_executable,
    )
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
    preflight_reports = [
        report
        for report in signal_reports
        if _context_value(report, "purpose") == "linearity_preflight"
    ]

    return {
        "schema_version": 1,
        "analysis": "raw_observer_validation_run",
        "run_dir": str(Path(run_dir)),
        "status": (
            "preflight_ready_for_manual_review"
            if preflight_reports
            else "ready_for_manual_branch_review"
        ),
        "report_count": len(reports),
        "signal_report_count": len(signal_reports),
        "normalization": {
            "mode": (
                "recomputed_from_cr3_recorded_exposure"
                if recompute_recorded_exposure
                else "stored_patch_statistics"
            ),
            "exposure_provenance": _summarize_exposure_provenance(reports),
        },
        "repeatability": repeatability,
        "linearity": linearity,
        "preflight": analyze_preflight_reports(preflight_reports),
        "green_consistency": raw_observer_analysis.analyze_green_consistency(signal_reports),
        "quality_threshold_recommendation": raw_observer_analysis.recommend_quality_thresholds(signal_reports),
        "notes": [
            "No P1 pass/fail conclusion or observer-config update is inferred automatically.",
            "Review repeatability, linearity, G1/G2 context, source isolation, and cleanup evidence against PLAN.md sections 7.4-7.7.",
        ],
    }


def analyze_preflight_reports(reports: Sequence[Mapping[str, Any]]) -> dict[str, Any] | None:
    if not reports:
        return None
    sources: dict[str, dict[str, Any]] = {}
    for source in sorted({str(_context_value(report, "source")) for report in reports}):
        group = [report for report in reports if str(_context_value(report, "source")) == source]
        clipped: list[float] = []
        near_noise: list[float] = []
        trimmed_signal: list[float] = []
        maximum_signal: list[float] = []
        missing_metrics = 0
        plane_count = 0
        for report in group:
            for patch in report.get("patches", []):
                if not isinstance(patch, Mapping) or not bool(patch.get("optimization_eligible")):
                    continue
                planes = patch.get("planes")
                if not isinstance(planes, Mapping):
                    continue
                for plane in planes.values():
                    if not isinstance(plane, Mapping):
                        continue
                    plane_count += 1
                    metrics = plane.get("metrics")
                    statistics = plane.get("statistics")
                    normalized = (
                        statistics.get("black_corrected_normalized")
                        if isinstance(statistics, Mapping)
                        else None
                    )
                    if not isinstance(metrics, Mapping) or not isinstance(normalized, Mapping):
                        missing_metrics += 1
                        continue
                    for target, value in (
                        (clipped, metrics.get("clipped_fraction")),
                        (near_noise, metrics.get("near_noise_floor_fraction")),
                        (trimmed_signal, normalized.get("trimmed_mean")),
                        (maximum_signal, normalized.get("maximum")),
                    ):
                        if isinstance(value, (int, float)):
                            target.append(float(value))
        sources[source] = {
            "report_count": len(group),
            "plane_count": plane_count,
            "missing_metrics_plane_count": missing_metrics,
            "maximum_clipped_fraction": max(clipped) if clipped else None,
            "maximum_near_noise_floor_fraction": max(near_noise) if near_noise else None,
            "maximum_black_corrected_normalized_trimmed_mean": (
                max(trimmed_signal) if trimmed_signal else None
            ),
            "maximum_black_corrected_normalized_sample": (
                max(maximum_signal) if maximum_signal else None
            ),
        }
    return {
        "analysis": "raw_observer_longest_bracket_preflight",
        "sources": sources,
        "notes": [
            "No automatic pass/fail is inferred.",
            "PLAN.md owns the clipping, noise-floor, and signal-envelope branch.",
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
    parser.add_argument("--recompute-recorded-exposure", action="store_true")
    parser.add_argument("--exiftool", default="exiftool")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    analysis = analyze_validation_run(
        args.run_dir,
        require_complete=not args.allow_incomplete,
        recompute_recorded_exposure=args.recompute_recorded_exposure,
        exiftool_executable=args.exiftool,
    )
    default_name = DEFAULT_RECORDED_OUTPUT_NAME if args.recompute_recorded_exposure else DEFAULT_OUTPUT_NAME
    output = args.output or args.run_dir / default_name
    print(write_validation_analysis(output, analysis))
    return 0


def _context_value(report: Mapping[str, Any], name: str) -> Any:
    context = report.get("analysis_context")
    return context.get(name) if isinstance(context, Mapping) else None


def _capture_payload(record: Mapping[str, Any], capture_id: str) -> Mapping[str, Any]:
    captured = record.get("capture")
    if not isinstance(captured, Mapping):
        raise ValueError(f"capture {capture_id} has no capture payload")
    return captured


def _camera_payload(
    captured: Mapping[str, Any],
    capture_id: str,
    *,
    require_saved_file: bool = False,
) -> Mapping[str, Any]:
    camera = captured.get("capture")
    if not isinstance(camera, Mapping):
        raise ValueError(f"capture {capture_id} has no camera payload")
    required = ("saved_file", "shutter_speed") if require_saved_file else ("shutter_speed",)
    for key in required:
        if not isinstance(camera.get(key), str) or not camera[key]:
            raise ValueError(f"capture {capture_id} camera payload has no {key}")
    return camera


def _verified_input_path(plan: Mapping[str, Any], name: str) -> Path:
    inputs = plan.get("inputs")
    reference = inputs.get(name) if isinstance(inputs, Mapping) else None
    if not isinstance(reference, Mapping):
        raise ValueError(f"P1 plan has no {name} input reference")
    path_value = reference.get("path")
    expected_hash = reference.get("sha256")
    if not isinstance(path_value, str) or not isinstance(expected_hash, str):
        raise ValueError(f"P1 plan {name} reference is incomplete")
    path = Path(path_value)
    actual_hash = hashlib.sha256(path.read_bytes()).hexdigest()
    if actual_hash != expected_hash:
        raise ValueError(f"P1 plan {name} hash no longer matches {path}")
    return path


def _summarize_exposure_provenance(reports: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    entries = [report.get("exposure_metadata") for report in reports]
    valid = [entry for entry in entries if isinstance(entry, Mapping)]
    sources: dict[str, int] = {}
    statuses: dict[str, int] = {}
    ratios: list[float] = []
    for entry in valid:
        source = str(entry.get("source", "unknown"))
        status = str(entry.get("status", "unknown"))
        sources[source] = sources.get(source, 0) + 1
        statuses[status] = statuses.get(status, 0) + 1
        ratio = entry.get("recorded_to_nominal_ratio")
        if isinstance(ratio, (int, float)):
            ratios.append(float(ratio))
    return {
        "report_count": len(reports),
        "metadata_report_count": len(valid),
        "missing_metadata_report_count": len(reports) - len(valid),
        "source_counts": dict(sorted(sources.items())),
        "status_counts": dict(sorted(statuses.items())),
        "recorded_to_nominal_ratio": (
            None
            if not ratios
            else {"min": min(ratios), "max": max(ratios), "max_absolute_difference_from_one": max(abs(value - 1.0) for value in ratios)}
        ),
    }


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
