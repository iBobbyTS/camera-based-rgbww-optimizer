from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Sequence

from camera_based_rgbww_optimizer.control import camera_remote
from camera_based_rgbww_optimizer.optimization.guide11 import (
    build_guide11_c1_confirm_plan,
    build_guide11_c1_confirm_recovery_suffix,
)
from camera_based_rgbww_optimizer.optimization.measure_p7_thermal_diagnostics import (
    run_authorized_plan,
)
from camera_based_rgbww_optimizer.paths import PROJECT_TMP_DIR


DEFAULT_OUTPUT = PROJECT_TMP_DIR / "guide11-c1"


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Execute the GUIDE11 C1 best-repeat confirmation batch."
    )
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--run-name", required=True)
    parser.add_argument("--batch2-analysis", type=Path, required=True)
    parser.add_argument("--batch1-run-root", type=Path, required=True)
    parser.add_argument(
        "--resume-from",
        type=Path,
        default=None,
        help="Failed run root whose fully completed targets are kept; "
        "partial/untouched targets are re-bracketed in this run.",
    )
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--dry-run", action="store_true")
    mode.add_argument("--execute", action="store_true")
    parser.add_argument("--allow-device-control", action="store_true")
    camera_remote.add_camera_backend_arguments(parser, default="remote")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    if args.resume_from is not None:
        plan = build_guide11_c1_confirm_recovery_suffix(
            args.batch2_analysis, args.batch1_run_root, args.resume_from
        )
    else:
        plan = build_guide11_c1_confirm_plan(args.batch2_analysis, args.batch1_run_root)
    if args.dry_run:
        root = (args.output_dir / args.run_name).resolve()
        root.mkdir(parents=True, exist_ok=False)
        output = root / "experiment-spec.json"
        output.write_text(json.dumps(plan, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(output)
        return 0
    if not args.allow_device_control:
        raise PermissionError("GUIDE11 C1 confirm execution requires --allow-device-control")
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
