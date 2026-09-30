from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any, Mapping, Sequence

from camera_based_rgbww_optimizer.control import camera_remote
from camera_based_rgbww_optimizer.optimization import p7_thermal_diagnostics as thermal
from camera_based_rgbww_optimizer.optimization.guide12 import (
    W12_EXPERIMENT_ID,
    build_guide12_w12_block_plan,
    build_guide12_w12_open_queue,
    guide12_w12_probe_candidates,
)
from camera_based_rgbww_optimizer.optimization.measure_p7_thermal_diagnostics import (
    run_authorized_plan,
)
from camera_based_rgbww_optimizer.paths import PROJECT_TMP_DIR


DEFAULT_OUTPUT = PROJECT_TMP_DIR / "guide12-w12"


def _reference(path: Path) -> dict[str, Any]:
    return {"path": str(path.resolve()), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


def _shutter_seconds(shutter: str | None) -> float:
    if shutter is None:
        return 0.01
    numerator, _, denominator = shutter.partition("/")
    value = float(numerator) / float(denominator) if denominator else float(numerator)
    if value <= 0:
        raise ValueError(f"invalid strip shutter: {shutter}")
    return value


def _duty_sum(command: Mapping[str, int]) -> float:
    curve = json.loads(thermal.CURVE_PATH.read_text(encoding="utf-8"))
    return float(sum(thermal.strip_duty(dict(command), curve).values()))


def _w2_raw_max_and_seconds(w2_root: Path, capture_id: str) -> tuple[float, float]:
    stats = json.loads(
        (w2_root / "measurements" / f"{capture_id}.patch-statistics.json").read_text(
            encoding="utf-8"
        )
    )
    block = next(p for p in stats["patches"] if p.get("index") == 6)
    raw_max = max(
        float(block["planes"][plane]["statistics"]["raw_code"]["maximum"])
        for plane in ("R", "G1", "G2", "B")
    )
    return raw_max, float(stats["exposure_metadata"]["seconds"])


def predicted_raw_max_at_block_shutter(
    w2_root: Path,
    base_capture_id: str,
    base_command: Mapping[str, int],
    candidates: Sequence[Mapping[str, Any]],
    *,
    shutter_seconds: float = 0.01,
) -> dict[str, float]:
    """Duty-scaled exposure pre-check at the frozen block shutter.

    The W2 frame of the base command supplies the measured raw-code maximum
    at its recorded shutter; candidate predictions scale by the shutter ratio
    and the duty-sum ratio. This is a safety pre-check only — the in-run
    near-white-rail quality gate stays the measurement owner.
    """
    w2_max, w2_seconds = _w2_raw_max_and_seconds(w2_root, base_capture_id)
    base_duty = _duty_sum(base_command)
    predictions: dict[str, float] = {}
    for candidate in candidates:
        duty = _duty_sum(candidate["command"])
        predictions[str(candidate["tag"])] = (
            w2_max * (shutter_seconds / w2_seconds) * (duty / base_duty)
        )
    return predictions


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Execute one GUIDE12 W12-1 fullscale-face local block."
    )
    parser.add_argument("--fresh-pairing", type=Path, required=True)
    parser.add_argument("--w2-root", type=Path, required=True)
    parser.add_argument("--cct", type=int, required=True)
    parser.add_argument("--gm", type=int, required=True)
    parser.add_argument("--block-index", type=int, default=1)
    parser.add_argument(
        "--strip-shutter", default=None,
        help="node-level strip shutter override (e.g. 1/125) when the offline"
             " exposure pre-check trips the raw-max ceiling at the 1/100 anchor",
    )
    parser.add_argument(
        "--candidates-json", type=Path,
        help="step-block candidates (list of {tag, command, role, new_unique_command});"
             " default builds the frozen probe block for the node",
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
    pairing = json.loads(args.fresh_pairing.read_text(encoding="utf-8"))
    queue = build_guide12_w12_open_queue(pairing)
    node = next(
        (
            row for row in queue["nodes"]
            if row["cct"] == args.cct and row["gm"] == args.gm
        ),
        None,
    )
    if node is None:
        raise SystemExit(
            f"node {args.cct}/{args.gm} is not in the frozen W12-1 open queue"
        )
    if args.candidates_json is not None:
        candidates = json.loads(args.candidates_json.read_text(encoding="utf-8"))
    else:
        candidates = guide12_w12_probe_candidates(node["base_command"])
    shutter_seconds = _shutter_seconds(args.strip_shutter)
    predictions = predicted_raw_max_at_block_shutter(
        args.w2_root, str(node["base_capture_id"]), node["base_command"], candidates,
        shutter_seconds=shutter_seconds,
    )
    block = build_guide12_w12_block_plan(
        node, candidates,
        block_index=args.block_index,
        inputs_references={
            "fresh_pairing": _reference(args.fresh_pairing),
            "w2_root": {"path": str(args.w2_root.resolve())},
        },
        predicted_raw_max=predictions,
        strip_shutter=args.strip_shutter,
        command_budget={
            "unique_command_cap": queue["unique_command_cap"],
            "unique_command_expanded_cap": queue["unique_command_expanded_cap"],
            "new_unique_commands_in_block": sum(
                1 for c in candidates if c.get("new_unique_command", True)
            ),
        },
    )
    if args.dry_run:
        root = (args.output_dir / args.run_name).resolve()
        root.mkdir(parents=True, exist_ok=False)
        output = root / "experiment-spec.json"
        output.write_text(
            json.dumps(block, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
        print(output)
        return 0
    if not args.allow_device_control:
        raise PermissionError("GUIDE12 W12 execution requires --allow-device-control")
    backend = camera_remote.create_camera_backend(
        args.camera_backend,
        env_file=args.remote_env_file,
        base_url=args.remote_base_url,
        timeout=args.remote_timeout,
    )
    print(run_authorized_plan(
        block, output_dir=args.output_dir, run_name=args.run_name,
        camera_backend=backend,
    ))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
