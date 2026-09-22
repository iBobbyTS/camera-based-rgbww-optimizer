from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any, Sequence

from camera_based_rgbww_optimizer.control import camera_remote
from camera_based_rgbww_optimizer.optimization import p7_thermal_diagnostics as thermal
from camera_based_rgbww_optimizer.optimization.guide11 import (
    build_guide11_n1_session_plan,
)
from camera_based_rgbww_optimizer.optimization.measure_p7_thermal_diagnostics import (
    run_authorized_plan,
)
from camera_based_rgbww_optimizer.paths import PROJECT_TMP_DIR


DEFAULT_OUTPUT = PROJECT_TMP_DIR / "guide11-n1"


def _reference(path: Path) -> dict[str, Any]:
    return {"path": str(path.resolve()), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Execute one GUIDE11 N1 white repeatability session.")
    parser.add_argument("--lut", type=Path, required=True, help="GUIDE10 W8 canonical LUT JSON (70 nodes with commands)")
    parser.add_argument("--w6-plan", type=Path, required=True, help="W6 final validation plan carrying frozen shutters")
    parser.add_argument("--session", type=int, choices=(1, 2), required=True)
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
    lut_document = json.loads(args.lut.read_text(encoding="utf-8"))
    lut = lut_document.get("canonical_lut")
    if not isinstance(lut, list) or len(lut) != 70:
        raise ValueError("GUIDE11 N1 requires the 70-node canonical LUT")
    w6_plan = json.loads(args.w6_plan.read_text(encoding="utf-8"))
    frozen_shutters = {
        str(key): str(value)
        for key, value in w6_plan.get("frozen_shutters", {}).items()
    }
    plan = build_guide11_n1_session_plan(
        lut, frozen_shutters, session_index=args.session, cycle_index=args.session,
    )
    plan["inputs"].update({
        "canonical_lut": _reference(args.lut),
        "w6_plan": _reference(args.w6_plan),
    })
    if args.dry_run:
        root = (args.output_dir / args.run_name).resolve()
        root.mkdir(parents=True, exist_ok=False)
        output = root / "experiment-spec.json"
        output.write_text(json.dumps(plan, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(output)
        return 0
    if not args.allow_device_control:
        raise PermissionError("GUIDE11 N1 execution requires --allow-device-control")
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
