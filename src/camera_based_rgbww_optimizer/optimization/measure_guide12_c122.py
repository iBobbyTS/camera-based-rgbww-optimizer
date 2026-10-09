from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any, Sequence

from camera_based_rgbww_optimizer.control import camera_remote
from camera_based_rgbww_optimizer.optimization.guide12_c122 import (
    build_guide12_c122_block_plan,
    c122_probe_candidates,
    c122_initial_command,
)
from camera_based_rgbww_optimizer.optimization.measure_p7_thermal_diagnostics import (
    run_authorized_plan,
)

DEFAULT_OUTPUT = Path("D:/rgbww-optimizer/guide12-c122")


def _reference(path: Path) -> dict[str, Any]:
    return {"path": str(path.resolve()), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Execute one GUIDE12 C12-2 color solving block (Ray bracket + strip candidates).")
    parser.add_argument("--hue", type=int, required=True)
    parser.add_argument("--sat", type=int, required=True)
    parser.add_argument("--block-index", type=int, required=True)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--candidates-json", type=Path,
                        help="explicit block candidates (list of {tag, command, role, "
                             "new_unique_command, face_channels, strip_shutter})")
    source.add_argument("--initial", action="store_true",
                        help="frozen initial probe block from the sector-dominant seed")
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
    if args.candidates_json is not None:
        candidates = json.loads(args.candidates_json.read_text(encoding="utf-8"))
    else:
        candidates = c122_probe_candidates(c122_initial_command(args.hue, args.sat))
    plan = build_guide12_c122_block_plan(
        args.hue, args.sat, candidates, block_index=args.block_index,
        inputs_references={"candidates": _reference(args.candidates_json)}
        if args.candidates_json is not None else None,
    )
    if args.dry_run:
        root = (args.output_dir / args.run_name).resolve()
        root.mkdir(parents=True, exist_ok=False)
        output = root / "experiment-spec.json"
        output.write_text(json.dumps(plan, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(output)
        return 0
    if not args.allow_device_control:
        raise PermissionError("GUIDE12 C12-2 execution requires --allow-device-control")
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
