from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any, Sequence

from camera_based_rgbww_optimizer.control import camera_remote
from camera_based_rgbww_optimizer.optimization.guide12_c124 import (
    C124_ADOPTED,
    build_guide12_c124_holdout_plan,
)
from camera_based_rgbww_optimizer.optimization.measure_p7_thermal_diagnostics import (
    run_authorized_plan,
)

DEFAULT_OUTPUT = Path("D:/rgbww-optimizer/guide12-c124")


def _reference(path: Path) -> dict[str, Any]:
    return {"path": str(path.resolve()), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Execute the GUIDE12 C12-4 runtime-model holdout run (30 frames).")
    parser.add_argument("--ray-shutter", action="append", default=[],
                        help="hue/sat=SHUTTER override, repeatable")
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
    overrides = {}
    for item in args.ray_shutter:
        key, shutter = item.split("=")
        overrides[key] = shutter
    # freeze the adopted-command table next to the run for provenance
    derived = args.output_dir / "derived"
    derived.mkdir(parents=True, exist_ok=True)
    adopted_path = derived / "c124-adopted-20261012.json"
    adopted_path.write_text(json.dumps(C124_ADOPTED, indent=1, sort_keys=True),
                            encoding="utf-8")
    plan = build_guide12_c124_holdout_plan(
        ray_shutter_overrides=overrides,
        inputs_references={"adopted_table": _reference(adopted_path)},
    )
    if args.dry_run:
        root = (args.output_dir / args.run_name).resolve()
        root.mkdir(parents=True, exist_ok=False)
        output = root / "experiment-spec.json"
        output.write_text(json.dumps(plan, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(output)
        return 0
    if not args.allow_device_control:
        raise PermissionError("GUIDE12 C12-4 execution requires --allow-device-control")
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
