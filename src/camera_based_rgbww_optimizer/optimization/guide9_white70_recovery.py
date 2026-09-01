from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
from typing import Any, Mapping, Sequence

from camera_based_rgbww_optimizer.control import camera_remote
from camera_based_rgbww_optimizer.optimization import analyze_p7_thermal_diagnostics as analyze
from camera_based_rgbww_optimizer.optimization import measure_p7_thermal_diagnostics as measure
from camera_based_rgbww_optimizer.optimization import p7_thermal_diagnostics as thermal


RECOVERY_SCHEMA = "guide9_white70_no_jacobian_probe_suffix_v1"


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def _write_json(path: Path, value: Mapping[str, Any]) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8")


def _canonical_sha256(value: Mapping[str, Any]) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def validate_prefix(parent_root: str | Path) -> dict[str, Any]:
    root = Path(parent_root).resolve()
    plan = _load_json(root / "experiment-spec.json")
    run = _load_json(root / "run.json")
    captures = _load_jsonl(root / "captures.jsonl")
    physical = _load_jsonl(root / "physical-returns.jsonl")
    expected_ids = [str(value) for value in plan["capture_ids"]]
    capture_ids = [str(row["capture_id"]) for row in captures]
    physical_ids = [str(row["capture_id"]) for row in physical]
    prefix = expected_ids[: len(captures)]
    if capture_ids != prefix or physical_ids != prefix:
        raise ValueError("GUIDE9 recovery ledgers are not the exact frozen-plan prefix")
    if len(captures) != len(physical):
        raise ValueError("GUIDE9 recovery capture and physical ledgers differ in length")
    if len(captures) >= len(expected_ids):
        raise ValueError("GUIDE9 recovery parent has no missing suffix")
    if int(run.get("accepted_formal_count", -1)) != len(captures):
        raise ValueError("GUIDE9 recovery accepted count differs from the retained prefix")
    if run.get("cleanup") != "pass":
        raise ValueError("GUIDE9 recovery parent cleanup did not pass")
    cleanup = _load_json(root / "all-off-python.json")
    if cleanup.get("status") != "pass" or any(not step.get("ok") for step in cleanup.get("steps", ())):
        raise ValueError("GUIDE9 recovery parent lacks passing zero-state cleanup")
    for row in captures:
        capture = row["capture"]
        source = capture.get("capture") or {}
        raw_path = root / "camera" / Path(str(capture["saved_file"])).name
        if not raw_path.is_file() or raw_path.stat().st_size != int(source["byte_count"]):
            raise ValueError(f"GUIDE9 recovery RAW identity differs: {raw_path.name}")
        report_path = root / "measurements" / Path(str(capture["patch_statistics"])).name
        if not report_path.is_file():
            raise ValueError(f"GUIDE9 recovery measurement is missing: {report_path.name}")
    return {
        "root": root,
        "plan": plan,
        "captures": captures,
        "physical": physical,
        "prefix_count": len(captures),
        "total_count": len(expected_ids),
        "remaining_count": len(expected_ids) - len(captures),
        "first_missing_capture_id": expected_ids[len(captures)],
    }


def _current_input_references(plan: Mapping[str, Any], data_root: Path) -> dict[str, Any]:
    references = copy.deepcopy(dict(plan["inputs"]))
    current_paths = {
        "location": thermal.LOCATION_PATH,
        "code_duty_curve": thermal.CURVE_PATH,
        "policy": thermal.POLICY_PATH,
        "uncertainty": thermal.UNCERTAINTY_PATH,
    }
    for name, path in current_paths.items():
        if name in references:
            references[name] = thermal.file_reference(path)
    if "white_70_candidate" in references:
        candidate = data_root / "white-lut-calibration/14x5-off-cycle-refined-v2-20260713/white-lut-calibration.json"
        if not candidate.is_file():
            raise FileNotFoundError(f"GUIDE9 white-70 candidate is missing: {candidate}")
        references["white_70_candidate"] = thermal.file_reference(candidate)
    return references


def build_suffix_plan(parent_root: str | Path, *, data_root: str | Path) -> dict[str, Any]:
    retained = validate_prefix(parent_root)
    plan = copy.deepcopy(retained["plan"])
    prefix_count = int(retained["prefix_count"])
    suffix = list(plan["captures"])[prefix_count:]
    plan["captures"] = suffix
    plan["capture_ids"] = [str(step["capture_id"]) for step in suffix]
    plan["budgets"] = {
        "ray_cap": sum(step["source_id"] == "ray" for step in suffix),
        "strip_cap": sum(step["source_id"] == "strip" for step in suffix),
        "formal_cap": len(suffix),
        "physical_cr3_cap": len(suffix),
        "ambient_cap": 0,
        "retry": 0,
    }
    plan["frozen_shutters"] = {
        str(step["exposure_cache_key"]): str(step["nominal_shutter"])
        for step in suffix
    }
    plan["shutter_ledger_provenance"] = {
        "owner": "experiment_capture_steps",
        "required_cache_keys": sorted(plan["frozen_shutters"]),
        "frozen_shutters_sha256": _canonical_sha256(plan["frozen_shutters"]),
    }
    plan["inputs"] = _current_input_references(plan, Path(data_root).resolve())
    plan["recovery_contract"] = {
        "schema": RECOVERY_SCHEMA,
        "parent_root": str(retained["root"]),
        "parent_capture_count": prefix_count,
        "parent_last_capture_id": retained["captures"][-1]["capture_id"],
        "first_missing_capture_id": retained["first_missing_capture_id"],
        "suffix_capture_count": len(suffix),
        "combined_capture_count": int(retained["total_count"]),
        "duplicate_capture_count": 0,
        "global_model_refit": False,
    }
    measure.validate_authorized_execution_plan(plan)
    return plan


def _portable_capture(row: Mapping[str, Any], root: Path) -> dict[str, Any]:
    value = copy.deepcopy(dict(row))
    capture = value["capture"]
    capture["saved_file"] = str(root / "camera" / Path(str(capture["saved_file"])).name)
    capture["patch_statistics"] = str(root / "measurements" / Path(str(capture["patch_statistics"])).name)
    nested = capture.get("capture")
    if isinstance(nested, dict):
        nested["saved_file"] = capture["saved_file"]
        if isinstance(nested.get("remote_metadata_path"), str):
            nested["remote_metadata_path"] = str(root / "camera" / Path(nested["remote_metadata_path"]).name)
    return value


def combine_and_analyze(parent_root: str | Path, suffix_root: str | Path, *, output: str | Path) -> Path:
    retained = validate_prefix(parent_root)
    suffix_path = Path(suffix_root).resolve()
    suffix_run = _load_json(suffix_path / "run.json")
    if suffix_run.get("status") != "complete" or suffix_run.get("cleanup") != "pass":
        raise ValueError("GUIDE9 recovery suffix is not complete with passing cleanup")
    suffix_plan = _load_json(suffix_path / "experiment-spec.json")
    suffix_rows = _load_jsonl(suffix_path / "captures.jsonl")
    expected_suffix = retained["plan"]["capture_ids"][retained["prefix_count"] :]
    if [row["capture_id"] for row in suffix_rows] != expected_suffix:
        raise ValueError("GUIDE9 recovery suffix differs from the frozen missing capture IDs")
    if suffix_plan.get("recovery_contract", {}).get("schema") != RECOVERY_SCHEMA:
        raise ValueError("GUIDE9 recovery suffix lacks its recovery contract")
    combined = [
        *(_portable_capture(row, retained["root"]) for row in retained["captures"]),
        *(_portable_capture(row, suffix_path) for row in suffix_rows),
    ]
    if [row["capture_id"] for row in combined] != retained["plan"]["capture_ids"]:
        raise ValueError("GUIDE9 recovery combined evidence is not the exact frozen plan")
    report = analyze.analyze_guide9_white_local_probes(
        combined, target_contracts=retained["plan"]["analysis_contract"]["target_contracts"],
    )
    report["recovery_evidence"] = {
        "schema": RECOVERY_SCHEMA,
        "parent_root": str(retained["root"]),
        "suffix_root": str(suffix_path),
        "parent_capture_count": retained["prefix_count"],
        "suffix_capture_count": len(suffix_rows),
        "combined_capture_count": len(combined),
        "duplicate_capture_count": 0,
        "rejected_dark_capture_included": False,
        "diagnostic_captures_included": False,
    }
    output_path = Path(output).resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    _write_json(output_path, report)
    return output_path


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Recover the interrupted GUIDE9 white70 probe batch.")
    commands = parser.add_subparsers(dest="command", required=True)
    inspect_parser = commands.add_parser("inspect")
    inspect_parser.add_argument("--parent-root", type=Path, required=True)
    run_parser = commands.add_parser("run-suffix")
    run_parser.add_argument("--parent-root", type=Path, required=True)
    run_parser.add_argument("--data-root", type=Path, required=True)
    run_parser.add_argument("--output-dir", type=Path, required=True)
    run_parser.add_argument("--run-name", required=True)
    combine_parser = commands.add_parser("combine-analyze")
    combine_parser.add_argument("--parent-root", type=Path, required=True)
    combine_parser.add_argument("--suffix-root", type=Path, required=True)
    combine_parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    if args.command == "inspect":
        result = validate_prefix(args.parent_root)
        summary = {key: str(value) if isinstance(value, Path) else value for key, value in result.items() if key not in {"plan", "captures", "physical"}}
        print(json.dumps(summary, indent=2))
        return 0
    if args.command == "run-suffix":
        plan = build_suffix_plan(args.parent_root, data_root=args.data_root)
        backend = camera_remote.create_camera_backend("remote")
        print(measure.run_authorized_plan(plan, output_dir=args.output_dir, run_name=args.run_name, camera_backend=backend))
        return 0
    print(combine_and_analyze(args.parent_root, args.suffix_root, output=args.output))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
