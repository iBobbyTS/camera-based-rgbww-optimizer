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


def rebuild_probe_contracts(plan: Mapping[str, Any]) -> list[dict[str, Any]]:
    source_contracts = list(plan["analysis_contract"]["target_contracts"])
    if not source_contracts:
        return []
    steps_by_target: dict[tuple[int, int], list[Mapping[str, Any]]] = {}
    for step in plan["captures"]:
        key = (int(step["target_cct"]), int(step["target_gm"]))
        steps_by_target.setdefault(key, []).append(step)
    rebuilt = []
    for source_contract in source_contracts:
        contract = copy.deepcopy(dict(source_contract))
        key = (int(contract["cct"]), int(contract["gm"]))
        steps = steps_by_target.get(key, [])
        base_steps = [step for step in steps if step["role"] == "strip_base"]
        probe_steps = [step for step in steps if str(step["role"]).startswith("strip_probe_")]
        active = str(contract["active_channel"])
        expected_channels = set(thermal.CHANNELS) - {active}
        if len(base_steps) != 1 or len(probe_steps) != 4:
            raise ValueError("GUIDE9 recovery plan lacks one base and four probe steps per target")
        base = {channel: int(base_steps[0]["command"][channel]) for channel in thermal.CHANNELS}
        if base != {channel: int(contract["base_command"][channel]) for channel in thermal.CHANNELS}:
            raise ValueError("GUIDE9 recovery probe base differs from its target contract")
        probes = []
        observed_channels = set()
        for step in probe_steps:
            channel = str(step["role"]).removeprefix("strip_probe_")
            if channel not in expected_channels or channel in observed_channels:
                raise ValueError("GUIDE9 recovery probe channels differ from the four free channels")
            command = {name: int(step["command"][name]) for name in thermal.CHANNELS}
            changed = {name for name in thermal.CHANNELS if command[name] != base[name]}
            delta = command[channel] - base[channel]
            if changed != {channel} or delta not in {-256, 256}:
                raise ValueError("GUIDE9 recovery probe command is not one bounded channel step")
            probes.append({"channel": channel, "delta_code": delta, "command": command})
            observed_channels.add(channel)
        if observed_channels != expected_channels:
            raise ValueError("GUIDE9 recovery probe set does not cover the four free channels")
        contract["probes"] = probes
        contract["probe_step_abs"] = 256
        rebuilt.append(contract)
    return rebuilt


def build_candidate_plan(
    parent_root: str | Path, analysis: str | Path, *, data_root: str | Path,
) -> dict[str, Any]:
    parent_path = Path(parent_root).resolve()
    analysis_path = Path(analysis).resolve()
    plan = _load_json(parent_path / "experiment-spec.json")
    report = _load_json(analysis_path)
    recovery = report.get("recovery_evidence") or {}
    if report.get("status") != "candidates_preregistered":
        raise ValueError("GUIDE9 candidate execution requires a preregistered probe analysis")
    if (
        recovery.get("rejected_dark_capture_included") is not False
        or recovery.get("diagnostic_captures_included") is not False
    ):
        raise ValueError("GUIDE9 candidate analysis includes prohibited recovery observations")
    if report.get("global_model_refit") is not False or report.get("default_lut_installation") is not False:
        raise ValueError("GUIDE9 candidate analysis changed a locked global artifact")

    source_contracts = {
        (int(row["cct"]), int(row["gm"])): row
        for row in plan["analysis_contract"]["target_contracts"]
    }
    nodes = {
        (int(row["cct"]), int(row["gm"])): row for row in report["nodes"]
    }
    if (
        len(nodes) != int(report.get("node_count", -1))
        or set(nodes) != set(source_contracts)
        or int(recovery.get("combined_capture_count", -1)) != int(report.get("capture_count", -2))
    ):
        raise ValueError("GUIDE9 candidate analysis differs from the frozen target or capture set")

    steps_by_target: dict[tuple[int, int], list[Mapping[str, Any]]] = {}
    for step in plan["captures"]:
        key = (int(step["target_cct"]), int(step["target_gm"]))
        steps_by_target.setdefault(key, []).append(step)
    contracts = []
    captures = []
    for target_index, key in enumerate(sorted(source_contracts)):
        source_contract = source_contracts[key]
        node = nodes[key]
        command = {
            channel: int(node["candidate"]["command"][channel]) for channel in thermal.CHANNELS
        }
        if set(node["candidate"]["command"]) != set(thermal.CHANNELS) or any(
            value < 0 or value > 4095 for value in command.values()
        ):
            raise ValueError("GUIDE9 candidate command is outside the five-channel bounds")
        active = str(source_contract["active_channel"])
        if command[active] != int(source_contract["base_command"][active]):
            raise ValueError("GUIDE9 candidate changed the frozen full-scale active channel")
        contract = copy.deepcopy(dict(source_contract))
        contract.update({
            "target_index": target_index,
            "strip_command": command,
            "source_order": ["ray", "strip"],
            "candidate_owner": "recovered_19_node_current_session_local_probe_jacobian",
        })
        contracts.append(contract)

        source_steps = steps_by_target.get(key, [])
        ray_steps = [step for step in source_steps if step["role"] == "ray_reference"]
        strip_steps = [step for step in source_steps if step["role"] == "strip_base"]
        if len(ray_steps) != 1 or len(strip_steps) != 1:
            raise ValueError("GUIDE9 candidate plan lacks one Ray/base template per target")
        for source, template in (("ray", ray_steps[0]), ("strip", strip_steps[0])):
            index = len(captures)
            step = copy.deepcopy(dict(template))
            step.update({
                "capture_id": (
                    f"{index:03d}-{source}-guide9-white70-local-probe-candidate-"
                    f"cct{key[0]}-gm{key[1]}"
                ),
                "role": "ray_reference" if source == "ray" else "strip_candidate",
                "session_index": index + 1,
                "source_order": 1 if source == "ray" else 2,
            })
            if source == "strip":
                step["command"] = command
                step["exact_command_hash"] = thermal.canonical_sha256(command)
            captures.append(step)

    frozen_shutters = {
        str(step["exposure_cache_key"]): str(step["nominal_shutter"]) for step in captures
    }
    plan.update({
        "guide_experiment_id": thermal.GUIDE9_WHITE_LOCAL_JAC_EXPERIMENT_ID,
        "variant": thermal.GUIDE9_WHITE_LOCAL_JAC_VARIANT,
        "stage": "GUIDE9-WHITE70-LOCAL-PROBE-CANDIDATES",
        "captures": captures,
        "capture_ids": [step["capture_id"] for step in captures],
        "frozen_shutters": frozen_shutters,
        "shutter_ledger_provenance": {
            "owner": "experiment_capture_steps",
            "required_cache_keys": sorted(frozen_shutters),
            "frozen_shutters_sha256": _canonical_sha256(frozen_shutters),
        },
        "budgets": {
            "ray_cap": len(contracts), "strip_cap": len(contracts),
            "formal_cap": len(captures), "physical_cr3_cap": len(captures),
            "ambient_cap": 0, "retry": 0,
        },
        "inputs": _current_input_references(plan, Path(data_root).resolve()),
        "execution_authorization": {
            **plan["execution_authorization"],
            "schema": "direct_guide9_white_local_jacobian_v1",
            "experiment_id": thermal.GUIDE9_WHITE_LOCAL_JAC_EXPERIMENT_ID,
            "human_authorization_experiment_id": None,
        },
        "analysis_contract": {
            **plan["analysis_contract"],
            "method": "white70_recovered_local_probe_candidates",
            "target_contracts": contracts,
            "parent_analysis": {
                "path": str(analysis_path),
                "sha256": hashlib.sha256(analysis_path.read_bytes()).hexdigest(),
            },
            "pass_next": "GUIDE9_WHITE70_LOCAL_NODE_CORRECTION_CONTINUE",
            "failure_next": "GUIDE9_WHITE70_LOCAL_PROBE_REASSESSMENT",
            "global_model_refit": False,
        },
        "candidate_contract": {
            "schema": "guide9_white70_recovered_local_probe_candidates_v1",
            "node_count": len(contracts), "capture_count": len(captures),
            "parent_root": str(parent_path), "paired_validation": True,
            "global_model_refit": False, "default_lut_installation": False,
        },
    })
    measure.validate_authorized_execution_plan(plan)
    return plan


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
        combined, target_contracts=rebuild_probe_contracts(retained["plan"]),
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
    for name in ("inspect-candidates", "run-candidates"):
        candidate_parser = commands.add_parser(name)
        candidate_parser.add_argument("--parent-root", type=Path, required=True)
        candidate_parser.add_argument("--analysis", type=Path, required=True)
        candidate_parser.add_argument("--data-root", type=Path, required=True)
        if name == "run-candidates":
            candidate_parser.add_argument("--output-dir", type=Path, required=True)
            candidate_parser.add_argument("--run-name", required=True)
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
    if args.command in {"inspect-candidates", "run-candidates"}:
        plan = build_candidate_plan(args.parent_root, args.analysis, data_root=args.data_root)
        if args.command == "inspect-candidates":
            print(json.dumps({
                "status": "ready", "stage": plan["stage"],
                "node_count": plan["candidate_contract"]["node_count"],
                "capture_count": plan["candidate_contract"]["capture_count"],
                "parent_analysis": plan["analysis_contract"]["parent_analysis"],
            }, indent=2))
            return 0
        backend = camera_remote.create_camera_backend("remote")
        print(measure.run_authorized_plan(
            plan, output_dir=args.output_dir, run_name=args.run_name, camera_backend=backend,
        ))
        return 0
    print(combine_and_analyze(args.parent_root, args.suffix_root, output=args.output))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
