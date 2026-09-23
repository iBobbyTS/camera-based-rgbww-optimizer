from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any, Sequence

from camera_based_rgbww_optimizer.control import camera_remote
from camera_based_rgbww_optimizer.optimization import p7_thermal_diagnostics as thermal
from camera_based_rgbww_optimizer.optimization.guide11 import (
    build_guide11_w2_candidate_rows,
    build_guide11_w2_plan,
    build_guide11_w2_recovery_suffix,
)
from camera_based_rgbww_optimizer.optimization.measure_p7_thermal_diagnostics import (
    run_authorized_plan,
)
from camera_based_rgbww_optimizer.paths import PROJECT_TMP_DIR


DEFAULT_OUTPUT = PROJECT_TMP_DIR / "guide11-w2"


def _reference(path: Path) -> dict[str, Any]:
    return {"path": str(path.resolve()), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Execute the GUIDE11 W2 bounded white correction.")
    parser.add_argument("--frozen-targets", type=Path)
    parser.add_argument("--w6-status", type=Path,
                        help="W8 canonical LUT (per-node frozen commands and status) or a W6 analysis")
    parser.add_argument("--w6-plan", type=Path)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--run-name", required=True)
    parser.add_argument("--resume-run-root", type=Path)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--dry-run", action="store_true")
    mode.add_argument("--execute", action="store_true")
    parser.add_argument("--allow-device-control", action="store_true")
    camera_remote.add_camera_backend_arguments(parser, default="remote")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    if args.resume_run_root is not None:
        if not (args.frozen_targets and args.w6_status and args.w6_plan):
            raise ValueError("--resume-run-root requires --frozen-targets/--w6-status/--w6-plan")
        plan = build_guide11_w2_recovery_suffix(args.resume_run_root.resolve())
        plan["inputs"].update({
            "frozen_targets": _reference(args.frozen_targets),
            "w6_status": _reference(args.w6_status),
            "w6_plan": _reference(args.w6_plan),
            "resumed_from": {
                "path": str(args.resume_run_root.resolve()),
                "pause_evidence_sha256": plan["recovery"]["pause_evidence_sha256"],
            },
        })
        return _dispatch(plan, args)
    targets = json.loads(args.frozen_targets.read_text(encoding="utf-8"))
    candidate_rows = build_guide11_w2_candidate_rows(targets, args.w6_status)
    with_commands = [row for row in candidate_rows if row["commands"]]
    if not with_commands:
        raise ValueError("GUIDE11 W2 has no node with feasible measured-direction candidates")
    w6_plan = json.loads(args.w6_plan.read_text(encoding="utf-8"))
    plan = build_guide11_w2_plan(
        with_commands, w6_plan,
        inputs_references={
            "frozen_targets": _reference(args.frozen_targets),
            "w6_status": _reference(args.w6_status),
            "w6_plan": _reference(args.w6_plan),
        },
    )
    return _dispatch(plan, args)


def _dispatch(plan: dict, args: argparse.Namespace) -> int:
    if args.dry_run:
        root = (args.output_dir / args.run_name).resolve()
        root.mkdir(parents=True, exist_ok=False)
        output = root / "experiment-spec.json"
        output.write_text(json.dumps(plan, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(output)
        return 0
    if not args.allow_device_control:
        raise PermissionError("GUIDE11 W2 execution requires --allow-device-control")
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
