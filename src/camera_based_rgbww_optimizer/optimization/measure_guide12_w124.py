from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any, Sequence

from camera_based_rgbww_optimizer.control import camera_remote
from camera_based_rgbww_optimizer.optimization.guide12_w124 import (
    W124_EXECUTION_ORDER,
    W124_POINTS,
    W124_RAY_FIRST,
    build_guide12_w124_point_plan,
)
from camera_based_rgbww_optimizer.optimization.measure_p7_thermal_diagnostics import (
    run_authorized_plan,
)
from camera_based_rgbww_optimizer.paths import PROJECT_TMP_DIR


DEFAULT_OUTPUT = Path("D:/rgbww-optimizer/guide12-w124")
DEFAULT_LUT = Path(
    "D:/rgbww-optimizer/guide12-w122/derived/w12-2-frozen-lut-20261005.json"
)


def _reference(path: Path) -> dict[str, Any]:
    return {"path": str(path.resolve()), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Execute one GUIDE12 W12-4 point run (one point, one protocol, two frames).")
    parser.add_argument(
        "--point", required=True,
        help="cct/gm, one of: " + ", ".join(f"{c}/{g}" for c, g in W124_POINTS))
    parser.add_argument("--protocol", choices=("fast", "long"), required=True)
    source = parser.add_mutually_exclusive_group()
    source.add_argument("--ray-first", action="store_true", default=None)
    source.add_argument("--strip-first", action="store_true", default=None)
    parser.add_argument("--frozen-lut", type=Path, default=DEFAULT_LUT)
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
    cct_s, gm_s = args.point.split("/")
    lut_doc = json.loads(args.frozen_lut.read_text(encoding="utf-8"))
    ray_first: bool | None = None
    if args.ray_first:
        ray_first = True
    elif args.strip_first:
        ray_first = False
    plan = build_guide12_w124_point_plan(
        lut_doc["nodes"], int(cct_s), int(gm_s),
        protocol=args.protocol, ray_first=ray_first,
        inputs_references={"frozen_lut": _reference(args.frozen_lut)},
    )
    if args.dry_run:
        root = (args.output_dir / args.run_name).resolve()
        root.mkdir(parents=True, exist_ok=False)
        output = root / "experiment-spec.json"
        output.write_text(json.dumps(plan, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(output)
        return 0
    if not args.allow_device_control:
        raise PermissionError("GUIDE12 W12-4 execution requires --allow-device-control")
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
