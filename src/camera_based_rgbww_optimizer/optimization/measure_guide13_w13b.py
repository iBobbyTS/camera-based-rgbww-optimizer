"""Execute one GUIDE13 W13-B confirmation-backfill session."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Sequence

from camera_based_rgbww_optimizer.control import camera_remote
from camera_based_rgbww_optimizer.optimization.guide13_w13b import (
    build_guide13_w13b_session_plan,
)
from camera_based_rgbww_optimizer.optimization.measure_p7_thermal_diagnostics import (
    run_authorized_plan,
)
from camera_based_rgbww_optimizer.paths import PROJECT_TMP_DIR

DEFAULT_OUTPUT = PROJECT_TMP_DIR / "guide13-w13b"
DEFAULT_LUT = Path(
    "D:/rgbww-optimizer/guide13-w13a/derived/w13a-corrected-lut-v2-20261016.json")


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Execute one GUIDE13 W13-B confirmation session.")
    parser.add_argument("--lut", type=Path, default=DEFAULT_LUT)
    parser.add_argument("--session-index", type=int, default=1)
    parser.add_argument(
        "--nodes", required=True,
        help="comma-separated cct/gm list, e.g. 6500/130,20000/70",
    )
    parser.add_argument(
        "--ordinals", default="2,3",
        help="pair ordinals this session provides (default 2,3)",
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
    by_key = {f"{n['cct']}/{n['gm']}": n for n in lut["nodes"]}
    wanted = [s.strip() for s in args.nodes.split(",") if s.strip()]
    missing = [k for k in wanted if k not in by_key]
    if missing:
        raise SystemExit(f"nodes not in corrected LUT: {missing}")
    nodes = [by_key[k] for k in wanted]
    ordinals = tuple(int(x) for x in args.ordinals.split(","))
    plan = build_guide13_w13b_session_plan(
        nodes, session_index=args.session_index, pair_ordinals=ordinals)
    if args.dry_run:
        root = (args.output_dir / args.run_name).resolve()
        root.mkdir(parents=True, exist_ok=False)
        output = root / "experiment-spec.json"
        output.write_text(
            json.dumps(plan, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(output)
        return 0
    if not args.allow_device_control:
        raise PermissionError("W13-B execution requires --allow-device-control")
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
