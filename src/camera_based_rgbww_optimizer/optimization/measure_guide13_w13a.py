"""Execute one GUIDE13 W13-A white-node correction block."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any, Mapping, Sequence

from camera_based_rgbww_optimizer.control import camera_remote
from camera_based_rgbww_optimizer.optimization import p7_thermal_diagnostics as thermal
from camera_based_rgbww_optimizer.optimization.guide13_w13a import (
    build_guide13_w13a_block_plan,
    w13a_first_block_candidates,
)
from camera_based_rgbww_optimizer.optimization.measure_guide12_w12 import (
    _shutter_seconds,
    predicted_raw_max_at_block_shutter,
)
from camera_based_rgbww_optimizer.optimization.measure_p7_thermal_diagnostics import (
    run_authorized_plan,
)
from camera_based_rgbww_optimizer.paths import PROJECT_TMP_DIR

DEFAULT_OUTPUT = PROJECT_TMP_DIR / "guide13-w13a"
DEFAULT_QUEUE = Path(
    "D:/rgbww-optimizer/guide13/derived/w13a-open-queue-20261013.json")
DEFAULT_VERIFICATION = Path(
    "D:/rgbww-optimizer/guide12-w122/derived/"
    "w12-2-verification-analysis.json")
W122_ROOT = Path("D:/rgbww-optimizer/guide12-w122")


def _reference(path: Path) -> dict[str, Any]:
    return {"path": str(path.resolve()),
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


def _base_capture_for_node(verification: Mapping[str, Any],
                           node: str) -> dict[str, Any]:
    """The strip step of the node's best W12-2 pair supplies the exposure
    pre-check base frame (its run root holds the patch statistics)."""
    best = None
    for pair in verification.get("node_pairs", ()):
        if pair.get("node") != node:
            continue
        strip = (pair.get("steps") or {}).get("strip") or {}
        if strip.get("quality") not in ("pass", "near_noise_only"):
            continue
        if pair.get("E_normalized") is None:
            continue
        if best is None or pair["E_normalized"] < best[0]:
            best = (pair["E_normalized"], strip)
    if best is None:
        raise SystemExit(f"no valid W12-2 base pair for node {node}")
    strip = best[1]
    return {"run": strip["run"], "capture_id": strip["capture_id"]}


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Execute one GUIDE13 W13-A node-correction block.")
    parser.add_argument("--queue", type=Path, default=DEFAULT_QUEUE)
    parser.add_argument("--verification", type=Path,
                        default=DEFAULT_VERIFICATION)
    parser.add_argument("--node", required=True, help="cct/gm, e.g. 6500/130")
    parser.add_argument("--block-index", type=int, default=1)
    parser.add_argument(
        "--candidates-json", type=Path,
        help="list of {tag, command, role, new_unique_command}; default "
             "builds the frozen W12-1 probe block for the node's base",
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
    queue = json.loads(args.queue.read_text(encoding="utf-8"))
    row = next((r for r in queue["nodes"] if r["node"] == args.node), None)
    if row is None:
        raise SystemExit(f"node {args.node} is not in the W13-A open queue")
    verification = json.loads(
        args.verification.read_text(encoding="utf-8"))
    base = _base_capture_for_node(verification, args.node)
    candidates = (
        json.loads(args.candidates_json.read_text(encoding="utf-8"))
        if args.candidates_json is not None
        else w13a_first_block_candidates(row)
    )
    from camera_based_rgbww_optimizer.optimization.guide13_w13a import (
        w13a_strip_shutter,
    )
    cct, gm = (int(x) for x in args.node.split("/"))
    shutter = w13a_strip_shutter(cct, gm)
    predictions = predicted_raw_max_at_block_shutter(
        W122_ROOT / base["run"], base["capture_id"],
        row["command"], candidates,
        shutter_seconds=_shutter_seconds(shutter),
    )
    plan = build_guide13_w13a_block_plan(
        row, candidates,
        block_index=args.block_index,
        inputs_references={
            "w13a_open_queue": _reference(args.queue),
            "w12_2_verification": _reference(args.verification),
            "w12_2_base_frame": {
                "run": base["run"], "capture_id": base["capture_id"],
                "path": str(
                    W122_ROOT / base["run"] / "measurements"
                    / f"{base['capture_id']}.patch-statistics.json"),
            },
        },
        predicted_raw_max=predictions,
        command_budget={
            "unique_command_cap": 8,
            "unique_command_expanded_cap": 12,
            "new_unique_commands_in_block": sum(
                1 for c in candidates if c.get("new_unique_command", True)),
        },
    )
    if args.dry_run:
        root = (args.output_dir / args.run_name).resolve()
        root.mkdir(parents=True, exist_ok=False)
        output = root / "experiment-spec.json"
        output.write_text(
            json.dumps(plan, indent=2, sort_keys=True) + "\n",
            encoding="utf-8")
        print(output)
        return 0
    if not args.allow_device_control:
        raise PermissionError("W13-A execution requires --allow-device-control")
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
