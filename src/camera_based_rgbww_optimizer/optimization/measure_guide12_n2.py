"""Execute one GUIDE12 N2 repeatability run (HSI ladder or session)."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Mapping, Sequence

from camera_based_rgbww_optimizer.control import camera_remote
from camera_based_rgbww_optimizer.optimization.guide12_n2 import (
    build_guide12_n2_hsi_ladder_plan,
    build_guide12_n2_session_plan,
)
from camera_based_rgbww_optimizer.optimization.measure_p7_thermal_diagnostics import (
    run_authorized_plan,
)
from camera_based_rgbww_optimizer.paths import PROJECT_TMP_DIR

DEFAULT_OUTPUT = PROJECT_TMP_DIR / "guide12-n2"


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Execute one GUIDE12 N2 repeatability run."
    )
    parser.add_argument(
        "--kind", choices=("hsi-ladder", "session"), required=True,
    )
    parser.add_argument("--session", type=int, default=1, choices=(1, 2, 3))
    parser.add_argument(
        "--hsi-ray-shutter-h0", default=None,
        help="ladder-frozen Ray H0/S100 shutter (e.g. 1/2000); required for kind=session",
    )
    parser.add_argument(
        "--hsi-ray-shutter-h240", default=None,
        help="ladder-frozen Ray H240/S100 shutter; required for kind=session",
    )
    parser.add_argument(
        "--predicted-raw-max", type=Path, default=None,
        help="JSON mapping N2 strip state keys to predicted raw maxima (DN); "
             "any value over the ceiling aborts the build (fail-closed)",
    )
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--run-name", required=True)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--dry-run", action="store_true")
    mode.add_argument("--execute", action="store_true")
    parser.add_argument("--allow-device-control", action="store_true")
    camera_remote.add_camera_backend_arguments(parser, default="remote")
    return parser.parse_args(argv)


def _load_mapping(path: Path | None) -> dict[str, Any]:
    if path is None:
        return {}
    return dict(json.loads(path.read_text(encoding="utf-8")))


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    predicted = _load_mapping(args.predicted_raw_max)
    if args.kind == "hsi-ladder":
        if args.hsi_ray_shutter_h0 or args.hsi_ray_shutter_h240:
            raise SystemExit(
                "GUIDE12 N2 ladder derives the HSI shutters; do not pass them"
            )
        plan = build_guide12_n2_hsi_ladder_plan()
    else:
        if not args.hsi_ray_shutter_h0 or not args.hsi_ray_shutter_h240:
            raise SystemExit(
                "GUIDE12 N2 session needs both ladder-frozen Ray HSI shutters"
            )
        plan = build_guide12_n2_session_plan(
            args.session,
            hsi_ray_shutters={
                "ray-hsi-h0-s100": args.hsi_ray_shutter_h0,
                "ray-hsi-h240-s100": args.hsi_ray_shutter_h240,
            },
            predicted_raw_max=predicted or None,
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
        raise PermissionError("GUIDE12 N2 execution requires --allow-device-control")
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
