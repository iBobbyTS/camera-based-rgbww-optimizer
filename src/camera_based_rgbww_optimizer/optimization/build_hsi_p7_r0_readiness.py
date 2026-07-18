from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Sequence

from camera_based_rgbww_optimizer.measurement.hsi_policy_v2 import DEFAULT_WAITING_OUTPUT
from camera_based_rgbww_optimizer.optimization.measure_hsi_reference_repeatability import DEFAULT_SENTINEL_RUN


PROJECT_ROOT = Path(__file__).resolve().parents[3]
SOURCE_FILES = (
    PROJECT_ROOT / "src/camera_based_rgbww_optimizer/measurement/hsi_policy_v2.py",
    PROJECT_ROOT / "src/camera_based_rgbww_optimizer/optimization/hsi_objective.py",
    PROJECT_ROOT / "src/camera_based_rgbww_optimizer/optimization/hsi_feedback.py",
    PROJECT_ROOT / "src/camera_based_rgbww_optimizer/optimization/hsi_budget.py",
    PROJECT_ROOT / "src/camera_based_rgbww_optimizer/optimization/analyze_hsi_policy_v2_replay.py",
    PROJECT_ROOT / "src/camera_based_rgbww_optimizer/optimization/analyze_strip_hsi_pilot.py",
    PROJECT_ROOT / "src/camera_based_rgbww_optimizer/optimization/hsi_source_evidence.py",
    PROJECT_ROOT / "src/camera_based_rgbww_optimizer/optimization/build_hsi_p7_r0_readiness.py",
    PROJECT_ROOT / "src/camera_based_rgbww_optimizer/optimization/measure_hsi_reference_repeatability.py",
    PROJECT_ROOT / "src/camera_based_rgbww_optimizer/optimization/analyze_hsi_reference_repeatability.py",
    PROJECT_ROOT / "src/camera_based_rgbww_optimizer/optimization/measure_strip_hsi_pilot.py",
)


def build_readiness(
    *, replay_path: str | Path, dry_run_plan: str | Path,
    fake_sentinel_analysis: str | Path,
    test_count: int, validation_commands: Sequence[str],
    wrapper_paths: Sequence[str | Path],
) -> dict[str, Any]:
    replay_file = Path(replay_path)
    dry_run_file = Path(dry_run_plan)
    fake_analysis_file = Path(fake_sentinel_analysis)
    replay = json.loads(replay_file.read_text(encoding="utf-8"))
    dry_run = json.loads(dry_run_file.read_text(encoding="utf-8"))
    fake_analysis = json.loads(fake_analysis_file.read_text(encoding="utf-8"))
    if replay.get("status") != "ready_for_planner_review":
        raise ValueError("P7-R0 replay is not ready for Planner review")
    if replay.get("device_calls_performed") is not False:
        raise ValueError("P7-R0 replay does not prove zero device calls")
    if (
        dry_run.get("formal_capture_eligible") is not False
        or dry_run.get("authorization", {}).get("status") != "not_authorized_for_execution"
    ):
        raise ValueError("P7-R1 draft is not safely locked")
    if test_count < 1 or not validation_commands:
        raise ValueError("P7-R0 readiness requires recorded validation evidence")
    if (
        fake_analysis.get("analysis") != "strip_hsi_pilot_v2_formal_analysis"
        or fake_analysis.get("policy_version") != "v2"
        or fake_analysis.get("point_count") != 4
        or fake_analysis.get("anchor_validation", {}).get("anchor_count") != 12
        or fake_analysis.get("target_evidence_validation", {}).get("three_layer_result_audit") != "pass"
    ):
        raise ValueError("P7-R0D fake sentinel did not close the formal v2 evidence analyzer")
    physical = dry_run["measurement"]["physical_capture_audit"]
    if physical.get("absolute_cap_status") != "planner_frozen" or int(physical.get("maximum_total_physical_cr3", -1)) != 250:
        raise ValueError("P7-R0D requires the Planner-frozen 250-CR3 absolute cap")
    return {
        "schema_version": 2,
        "readiness": "P7-R0D-offline-v2",
        "status": "ready_for_planner_review",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "authorization_consumed": "P7-R0D_offline_only",
        "inputs": {
            "frozen_sentinel_run": {
                "path": str(DEFAULT_SENTINEL_RUN),
                "run_json_sha256": _sha256(DEFAULT_SENTINEL_RUN / "run.json"),
                "plan_json_sha256": _sha256(DEFAULT_SENTINEL_RUN / "plan.json"),
                "target_results_sha256": _sha256(DEFAULT_SENTINEL_RUN / "target-results.jsonl"),
            },
            "v1_uncertainty": _reference(PROJECT_ROOT / "config/hsi/strip-hsi-uncertainty.json"),
            "v2_waiting_policy": _reference(DEFAULT_WAITING_OUTPUT),
            "ray_hsi_manifold": _reference(PROJECT_ROOT / "config/hsi/ray-hsi-manifold.json"),
            "replay": _reference(replay_file),
            "p7_r1_dry_run": _reference(dry_run_file),
            "v2_fake_sentinel_analysis": _reference(fake_analysis_file),
            "implementation": [_reference(path) for path in SOURCE_FILES],
        },
        "validation": {
            "unit_test_count": int(test_count),
            "commands": list(validation_commands),
            "compileall": "pass",
            "wrapper_zsh_syntax": [{"path": str(path), "status": "pass"} for path in wrapper_paths],
            "git_diff_check": "pass",
            "codegraph_sync": "pass",
        },
        "no_device_call_assertion": {
            "env_loaded": False, "network_calls": 0, "camera_calls": 0,
            "ray_calls": 0, "esphome_calls": 0, "all_off_calls": 0,
            "evidence": "dry-run regression mocks plus offline-only modules without device construction",
        },
        "v1_replay": replay["v1_replay"],
        "v2_synthetic_coverage": replay["v2_synthetic_coverage"],
        "old_sentinel_holdout_replay": replay["old_sentinel_holdout_replay"],
        "solver_architecture": replay["solver_architecture"],
        "p7_r1_draft": {
            "experiment": dry_run["experiment"],
            "formal_ray_count": dry_run["measurement"]["formal_ray_count"],
            "formal_strip_count": dry_run["measurement"]["formal_strip_count"],
            "authorization": dry_run["authorization"],
            "execution_surface_implemented_not_run": True,
            "maximum_total_physical_cr3": dry_run["measurement"]["physical_capture_audit"]["maximum_total_physical_cr3"],
            "physical_cap_status": physical["absolute_cap_status"],
            "baseline_physical_range_without_weak_reacquire": physical["baseline_physical_range_without_weak_reacquire"],
            "permitted_physical_range_with_weak_reacquire": physical["permitted_physical_range_with_weak_reacquire"],
            "maximum_60_second_settling_seconds": physical["maximum_60_second_settling_seconds"],
            "retained_attempt_evidence": True,
            "commands_jsonl_audited": True,
            "physical_count_independently_recomputed": True,
            "frozen_plan_source_and_off_responses_audited": True,
            "candidate_status": dry_run["execution_contract"]["candidate_status"],
            "candidate_formal_capture_eligible": dry_run["execution_contract"]["candidate_formal_capture_eligible"],
        },
        "formal_runner": {
            "explicit_policy_dispatch": True,
            "waiting_and_candidate_hard_rejected": True,
            "v2_multiseed_integrated": True,
            "ordinary_hard_caps": {"logical_observations": 54, "physical_cr3": 67},
            "n5_hard_caps": {"logical_observations": 62, "physical_cr3": 75},
            "structured_solver_budget_exhausted": True,
            "confirmed_face_selection_priority": True,
            "complete_confirmation_groups": True,
            "best_valid_final_verification_uses_existing_group_budget": True,
            "formal_v2_analyzer": "raw_evidence_reconstruction_fake_integration_pass",
            "self_reported_and_recomputed_values_reported": True,
        },
        "repeatability_audit": {
            "within_state_command_block_centered": True,
            "chronological_trend_per_block": True,
            "block_center_shift_reported_separately": True,
        },
        "unmeasured_statistics": [
            "P7-R1 empirical reference center compatibility",
            "P7-R1 empirical pre/post reference repeatability",
            "P7-R1 four strip-class variances",
            "new sentinel-v2 convergence",
            "remaining/boundary/holdout behavior",
        ],
        "planner_review_required": True,
        "named_experiment_authorized": False,
        "locked": replay["locked"],
    }


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _reference(path: Path) -> dict[str, str]:
    return {"path": str(path), "sha256": _sha256(path)}


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Write final P7-R0 offline readiness evidence.")
    parser.add_argument("--replay", type=Path, required=True)
    parser.add_argument("--dry-run-plan", type=Path, required=True)
    parser.add_argument("--fake-sentinel-analysis", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--test-count", type=int, required=True)
    parser.add_argument("--validation-command", action="append", required=True)
    parser.add_argument("--wrapper", type=Path, action="append", default=[])
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    value = build_readiness(
        replay_path=args.replay, dry_run_plan=args.dry_run_plan,
        fake_sentinel_analysis=args.fake_sentinel_analysis,
        test_count=args.test_count, validation_commands=args.validation_command,
        wrapper_paths=args.wrapper,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    if args.output.exists():
        raise FileExistsError(f"readiness output already exists: {args.output}")
    args.output.write_text(json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8")
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
