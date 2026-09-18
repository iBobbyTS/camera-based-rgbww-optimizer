from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any, Sequence

from camera_based_rgbww_optimizer.control import camera_remote
from camera_based_rgbww_optimizer.optimization import p7_thermal_diagnostics as thermal
from camera_based_rgbww_optimizer.optimization.guide10_white70 import (
    build_guide10_white70_recovery_suffix,
    build_guide10_white70_w5_recovery_suffix,
    build_guide10_white70_validation_plan,
    build_guide10_white70_w5_plan,
)
from camera_based_rgbww_optimizer.optimization.measure_p7_thermal_diagnostics import (
    run_authorized_plan,
)
from camera_based_rgbww_optimizer.paths import PROJECT_TMP_DIR


DEFAULT_OUTPUT = PROJECT_TMP_DIR / "guide10-white70-round1"


def _reference(path: Path) -> dict[str, Any]:
    return {"path": str(path.resolve()), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Execute GUIDE10 white70 FAST validation round 1.")
    parser.add_argument("--candidates", type=Path, required=True)
    parser.add_argument("--calibration", type=Path, default=thermal.GUIDE9_WHITE_70_CANDIDATE_PATH)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--run-name", required=True)
    parser.add_argument("--resume-run-root", type=Path)
    parser.add_argument("--w5-analysis", type=Path)
    parser.add_argument("--w5-round1-plan", type=Path)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--dry-run", action="store_true")
    mode.add_argument("--execute", action="store_true")
    parser.add_argument("--allow-device-control", action="store_true")
    camera_remote.add_camera_backend_arguments(parser, default="remote")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    if args.w5_analysis is not None or args.w5_round1_plan is not None:
        if args.w5_analysis is None or args.w5_round1_plan is None:
            raise ValueError("W5 requires --w5-analysis and --w5-round1-plan together")
        candidates = json.loads(args.candidates.read_text(encoding="utf-8"))
        calibration = json.loads(args.calibration.read_text(encoding="utf-8"))
        plan = build_guide10_white70_w5_plan(
            json.loads(args.w5_analysis.read_text(encoding="utf-8")),
            json.loads(args.w5_round1_plan.read_text(encoding="utf-8")),
            calibration,
            analysis_reference=_reference(args.w5_analysis),
            round1_reference=_reference(args.w5_round1_plan),
            calibration_reference=_reference(args.calibration),
        )
    elif args.resume_run_root is not None:
        parent_plan = json.loads((args.resume_run_root.resolve() / "experiment-spec.json").read_text(encoding="utf-8"))
        if parent_plan.get("guide_experiment_id") == "GUIDE10_WHITE70_W5_LOCAL_CORRECTION_V1":
            plan = build_guide10_white70_w5_recovery_suffix(args.resume_run_root.resolve())
        else:
            plan = build_guide10_white70_recovery_suffix(args.resume_run_root.resolve())
    else:
        candidates = json.loads(args.candidates.read_text(encoding="utf-8"))
        calibration = json.loads(args.calibration.read_text(encoding="utf-8"))
        plan = build_guide10_white70_validation_plan(
            candidates,
            calibration,
            candidate_reference=_reference(args.candidates),
            calibration_reference=_reference(args.calibration),
        )
    if args.dry_run:
        root = (args.output_dir / args.run_name).resolve()
        root.mkdir(parents=True, exist_ok=False)
        output = root / "experiment-spec.json"
        output.write_text(json.dumps(plan, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(output)
        return 0
    if not args.allow_device_control:
        raise PermissionError("GUIDE10 white70 execution requires --allow-device-control")
    backend = camera_remote.create_camera_backend(
        args.camera_backend,
        env_file=args.remote_env_file,
        base_url=args.remote_base_url,
        timeout=args.remote_timeout,
    )
    print(run_authorized_plan(plan, output_dir=args.output_dir, run_name=args.run_name, camera_backend=backend))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
