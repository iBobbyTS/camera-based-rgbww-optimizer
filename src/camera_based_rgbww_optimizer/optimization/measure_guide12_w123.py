"""Execute the GUIDE12 W12-3 interpolation holdout run."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Sequence

from camera_based_rgbww_optimizer.control import camera_remote
from camera_based_rgbww_optimizer.optimization.guide12_w123 import (
    build_guide12_w123_request_plan,
)
from camera_based_rgbww_optimizer.optimization.measure_p7_thermal_diagnostics import (
    run_authorized_plan,
)
from camera_based_rgbww_optimizer.paths import PROJECT_TMP_DIR

DEFAULT_OUTPUT = PROJECT_TMP_DIR / "guide12-w123"
DEFAULT_LUT = (
    Path("D:/rgbww-optimizer/guide12-w122/derived/w12-2-frozen-lut-20261005.json")
)
DEFAULT_SHUTTERS = Path(
    "D:/rgbww-optimizer/guide12-w122/derived/w123-strip-shutters-20261008.json"
)


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Execute the GUIDE12 W12-3 interpolation holdout run."
    )
    parser.add_argument("--lut", type=Path, default=DEFAULT_LUT)
    parser.add_argument("--strip-shutters", type=Path, default=DEFAULT_SHUTTERS)
    parser.add_argument(
        "--include-s0-reference", action="store_true",
        help="prepend the S0 session-C reference frame",
    )
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--run-name", required=True)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--dry-run", action="store_true")
    mode.add_argument("--execute", action="store_true")
    parser.add_argument("--allow-device-control", action="store_true")
    camera_remote.add_camera_backend_arguments(parser, default="remote")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    lut = json.loads(args.lut.read_text(encoding="utf-8"))
    if lut.get("schema") != "guide12_w12_2_frozen_lut_v1":
        raise SystemExit("W12-3 requires the frozen W12-2 LUT schema")
    strip_shutters = json.loads(args.strip_shutters.read_text(encoding="utf-8"))
    plan = build_guide12_w123_request_plan(
        lut["nodes"], strip_shutters=strip_shutters,
        include_s0_reference=args.include_s0_reference,
    )
    if args.dry_run:
        root = (args.output_dir / args.run_name).resolve()
        root.mkdir(parents=True, exist_ok=False)
        output = root / "experiment-spec.json"
        output.write_text(
            json.dumps(plan, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
        print(output)
        return 0
    if not args.allow_device_control:
        raise PermissionError("GUIDE12 W12-3 execution requires --allow-device-control")
    backend = camera_remote.create_camera_backend(
        args.camera_backend,
        env_file=args.remote_env_file,
        base_url=args.remote_base_url,
        timeout=args.remote_timeout,
    )
    print(run_authorized_plan(
        plan, output_dir=args.output_dir, run_name=args.run_name,
        camera_backend=backend,
    ))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
