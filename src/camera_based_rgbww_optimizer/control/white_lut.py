from __future__ import annotations

import argparse
import json
import math
from collections.abc import Callable, Mapping, Sequence
from pathlib import Path
from typing import Any

from camera_based_rgbww_optimizer.control import esphome
from camera_based_rgbww_optimizer.paths import PROJECT_ROOT


DEFAULT_LUT_PATH = PROJECT_ROOT / "config/white/white-lut.json"
MAX_CODE = 4095

LightFn = Callable[..., dict[str, int]]


def load_white_lut(path: str | Path) -> dict[str, Any]:
    lut_path = Path(path)
    data = json.loads(lut_path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("white LUT root must be a JSON object")
    return data


def interpolate_white_lut(
    data: Mapping[str, Any],
    cct: float,
    gm: float,
    *,
    clamp: bool = False,
) -> dict[str, Any]:
    requested_cct = _finite_float(cct, "cct")
    requested_gm = _finite_float(gm, "gm")
    points, cct_values, gm_values = _validated_grid(data)
    resolved_cct = _resolve_axis(requested_cct, cct_values, "CCT", clamp=clamp)
    resolved_gm = _resolve_axis(requested_gm, gm_values, "GM", clamp=clamp)
    low_cct, high_cct = _bounds(cct_values, resolved_cct)
    low_gm, high_gm = _bounds(gm_values, resolved_gm)
    cct_ratio = _ratio(resolved_cct, low_cct, high_cct)
    gm_ratio = _ratio(resolved_gm, low_gm, high_gm)

    low_gm_command = _lerp_commands(
        points[(low_cct, low_gm)],
        points[(low_cct, high_gm)],
        gm_ratio,
    )
    high_gm_command = _lerp_commands(
        points[(high_cct, low_gm)],
        points[(high_cct, high_gm)],
        gm_ratio,
    )
    command = _lerp_commands(low_gm_command, high_gm_command, cct_ratio)
    rounded_command = {
        channel: min(max(int(round(command[channel])), 0), MAX_CODE)
        for channel in esphome.CHANNEL_ORDER
    }
    return {
        "requested": {"cct": requested_cct, "gm": requested_gm},
        "resolved": {"cct": resolved_cct, "gm": resolved_gm},
        "clamped": resolved_cct != requested_cct or resolved_gm != requested_gm,
        "bracket": {
            "cct": [low_cct, high_cct],
            "gm": [low_gm, high_gm],
            "cct_ratio": cct_ratio,
            "gm_ratio": gm_ratio,
        },
        "command": rounded_command,
    }


def scale_command(command: Mapping[str, int], intensity_percent: float) -> dict[str, int]:
    intensity = _finite_float(intensity_percent, "intensity_percent")
    if not 0.0 <= intensity <= 100.0:
        raise ValueError("intensity_percent must be between 0 and 100")
    scale = intensity / 100.0
    return {
        channel: min(max(int(round(float(command[channel]) * scale)), 0), MAX_CODE)
        for channel in esphome.CHANNEL_ORDER
    }


def set_white_from_lut(
    *,
    lut_path: str | Path,
    cct: float,
    gm: float,
    intensity_percent: float = 100.0,
    clamp: bool = False,
    dry_run: bool = False,
    host: str = esphome.DEFAULT_HOST,
    port: int = esphome.DEFAULT_PORT,
    expected_name: str = esphome.DEFAULT_EXPECTED_NAME,
    curve_path: str | Path | None = esphome.DEFAULT_CURVE_PATH,
    light_fn: LightFn = esphome.light,
) -> dict[str, Any]:
    interpolation = interpolate_white_lut(load_white_lut(lut_path), cct, gm, clamp=clamp)
    command = scale_command(interpolation["command"], intensity_percent)
    payload = None
    if not dry_run:
        payload = light_fn(
            command["cw"],
            command["ww"],
            command["r"],
            command["g"],
            command["b"],
            host=host,
            port=port,
            expected_name=expected_name,
            curve_path=curve_path,
        )
    return {
        **interpolation,
        "lut_path": str(Path(lut_path)),
        "intensity_percent": float(intensity_percent),
        "command": command,
        "payload": payload,
        "dry_run": bool(dry_run),
    }


def _validated_grid(
    data: Mapping[str, Any],
) -> tuple[dict[tuple[float, float], dict[str, int]], list[float], list[float]]:
    targets = data.get("targets")
    if not isinstance(targets, Sequence) or isinstance(targets, (str, bytes)) or not targets:
        raise ValueError("white LUT targets must be a non-empty array")
    points: dict[tuple[float, float], dict[str, int]] = {}
    for target in targets:
        if not isinstance(target, Mapping):
            raise ValueError("white LUT target must be an object")
        key = (_finite_float(target.get("cct"), "target cct"), _finite_float(target.get("gm"), "target gm"))
        if key in points:
            raise ValueError(f"duplicate white LUT target: cct={key[0]:g}, gm={key[1]:g}")
        command = target.get("selected_command")
        if not isinstance(command, Mapping):
            raise ValueError(f"target cct={key[0]:g}, gm={key[1]:g} has no selected_command")
        resolved_command: dict[str, int] = {}
        for channel in esphome.CHANNEL_ORDER:
            value = int(command[channel])
            if not 0 <= value <= MAX_CODE:
                raise ValueError(f"channel {channel} value {value} is outside 0..{MAX_CODE}")
            resolved_command[channel] = value
        points[key] = resolved_command

    cct_values = sorted({key[0] for key in points})
    gm_values = sorted({key[1] for key in points})
    missing = [
        (cct, gm)
        for cct in cct_values
        for gm in gm_values
        if (cct, gm) not in points
    ]
    if missing:
        formatted = ", ".join(f"{cct:g}K/gm{gm:g}" for cct, gm in missing)
        raise ValueError(f"white LUT grid is incomplete; missing: {formatted}")
    return points, cct_values, gm_values


def _resolve_axis(value: float, values: Sequence[float], name: str, *, clamp: bool) -> float:
    low = float(values[0])
    high = float(values[-1])
    if low <= value <= high:
        return value
    if not clamp:
        raise ValueError(f"{name} {value:g} is outside LUT range {low:g}..{high:g}")
    return min(max(value, low), high)


def _bounds(values: Sequence[float], value: float) -> tuple[float, float]:
    if value <= values[0]:
        return float(values[0]), float(values[0])
    for high_index in range(1, len(values)):
        high = float(values[high_index])
        if value <= high:
            return float(values[high_index - 1]), high
    return float(values[-1]), float(values[-1])


def _ratio(value: float, low: float, high: float) -> float:
    if high == low:
        return 0.0
    return (value - low) / (high - low)


def _lerp_commands(
    left: Mapping[str, int | float],
    right: Mapping[str, int | float],
    ratio: float,
) -> dict[str, float]:
    return {
        channel: float(left[channel]) + ratio * (float(right[channel]) - float(left[channel]))
        for channel in esphome.CHANNEL_ORDER
    }


def _finite_float(value: Any, name: str) -> float:
    try:
        resolved = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{name} must be a finite number") from exc
    if not math.isfinite(resolved):
        raise ValueError(f"{name} must be a finite number")
    return resolved


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Set the RGBWW strip from a bilinearly interpolated white LUT.")
    parser.add_argument("cct", type=float, help="Requested CCT in kelvin.")
    parser.add_argument("gm", type=float, help="Requested raw G/M value.")
    parser.add_argument("--lut", type=Path, default=DEFAULT_LUT_PATH)
    parser.add_argument("--intensity-percent", type=float, default=100.0)
    parser.add_argument("--clamp", action="store_true", help="Clamp CCT/G-M outside the measured LUT range.")
    parser.add_argument("--dry-run", action="store_true", help="Calculate and print without controlling ESPHome.")
    parser.add_argument("--host", default=esphome.DEFAULT_HOST)
    parser.add_argument("--port", type=int, default=esphome.DEFAULT_PORT)
    parser.add_argument("--expected-name", default=esphome.DEFAULT_EXPECTED_NAME)
    parser.add_argument("--curve", type=Path, default=esphome.DEFAULT_CURVE_PATH)
    parser.add_argument("--no-curve", action="store_true", help="Disable code-duty curve correction.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    result = set_white_from_lut(
        lut_path=args.lut,
        cct=args.cct,
        gm=args.gm,
        intensity_percent=args.intensity_percent,
        clamp=args.clamp,
        dry_run=args.dry_run,
        host=args.host,
        port=args.port,
        expected_name=args.expected_name,
        curve_path=None if args.no_curve else args.curve,
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
