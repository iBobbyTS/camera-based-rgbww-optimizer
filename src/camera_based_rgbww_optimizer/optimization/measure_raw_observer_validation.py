from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Sequence

from camera_based_rgbww_optimizer.control import white_lut as white_lut_control
from camera_based_rgbww_optimizer.paths import PROJECT_ROOT, PROJECT_TMP_DIR


DEFAULT_OUTPUT_ROOT = PROJECT_TMP_DIR / "raw-observer-validation"
DEFAULT_LOCATION_CONFIG = PROJECT_ROOT / "config" / "location" / "locations-20260709-012045.json"
DEFAULT_OBSERVER_CONFIG = PROJECT_ROOT / "config" / "camera" / "raw-observer.json"
DEFAULT_ANCHOR_CCT = 5600
DEFAULT_ANCHOR_GM = 100
DEFAULT_RAY_INTENSITY_PERCENT = 100.0
DEFAULT_PAIRED_REPEATS = 5
DEFAULT_LINEARITY_FACTORS = (0.5, 1.0, 2.0)
DEFAULT_LINEARITY_REPEATS = 3
DEFAULT_OFF_SECONDS = 1.0
DEFAULT_SETTLE_SECONDS = 60.0


def build_raw_observer_validation_plan(
    *,
    baseline_lut_path: str | Path,
    location_config_path: str | Path,
    observer_config_path: str | Path,
    anchor_cct: int = DEFAULT_ANCHOR_CCT,
    anchor_gm: int = DEFAULT_ANCHOR_GM,
    ray_intensity_percent: float = DEFAULT_RAY_INTENSITY_PERCENT,
    paired_repeats: int = DEFAULT_PAIRED_REPEATS,
    linearity_factors: Sequence[float] = DEFAULT_LINEARITY_FACTORS,
    linearity_repeats: int = DEFAULT_LINEARITY_REPEATS,
    off_seconds: float = DEFAULT_OFF_SECONDS,
    settle_seconds: float = DEFAULT_SETTLE_SECONDS,
    include_flat_field: bool = False,
) -> dict[str, Any]:
    """Build the P1 capture order without connecting to camera or lights."""

    if paired_repeats < 1:
        raise ValueError("paired_repeats must be at least 1")
    if linearity_repeats < 1:
        raise ValueError("linearity_repeats must be at least 1")
    factors = _validate_linearity_factors(linearity_factors)
    if off_seconds < 0 or settle_seconds < 0:
        raise ValueError("off_seconds and settle_seconds must be non-negative")
    if not 0.0 <= float(ray_intensity_percent) <= 100.0:
        raise ValueError("ray_intensity_percent must be between 0 and 100")

    lut_path = Path(baseline_lut_path)
    interpolation = white_lut_control.interpolate_white_lut(
        white_lut_control.load_white_lut(lut_path),
        anchor_cct,
        anchor_gm,
        clamp=False,
    )
    strip_command = {channel: int(value) for channel, value in interpolation["command"].items()}
    captures: list[dict[str, Any]] = []

    def add_capture(
        *,
        source: str,
        purpose: str,
        repeat_index: int | None = None,
        exposure_factor: float | None = None,
        source_cache: str | None = None,
    ) -> None:
        index = len(captures)
        captures.append(
            {
                "capture_id": f"{index:04d}-{source}-{purpose}",
                "index": index,
                "source": source,
                "purpose": purpose,
                "repeat_index": repeat_index,
                "exposure_factor": exposure_factor,
                "source_exposure_cache": source_cache,
                "off_seconds_before": float(off_seconds),
                "settle_seconds": float(settle_seconds),
                "ray": (
                    None
                    if source not in {"ray", "flat_field_ray"}
                    else {"cct": int(anchor_cct), "gm": int(anchor_gm), "intensity_percent": float(ray_intensity_percent)}
                ),
                "strip_command": strip_command if source == "strip" else None,
                "other_source_must_be_off": True,
            }
        )

    add_capture(source="ambient", purpose="ambient")
    add_capture(source="ray", purpose="baseline_auto_exposure", source_cache="ray")
    add_capture(source="strip", purpose="baseline_auto_exposure", source_cache="strip")

    for repeat_index in range(paired_repeats):
        source_order = ("ray", "strip") if repeat_index % 2 == 0 else ("strip", "ray")
        for source in source_order:
            add_capture(
                source=source,
                purpose="paired_repeat",
                repeat_index=repeat_index,
                source_cache=source,
            )

    for repeat_index in range(linearity_repeats):
        ordered_factors = factors if repeat_index % 2 == 0 else tuple(reversed(factors))
        for factor_index, factor in enumerate(ordered_factors):
            source_order = ("ray", "strip") if (repeat_index + factor_index) % 2 == 0 else ("strip", "ray")
            for source in source_order:
                add_capture(
                    source=source,
                    purpose="linearity_bracket",
                    repeat_index=repeat_index,
                    exposure_factor=factor,
                    source_cache=source,
                )

    flat_field = {"status": "not_requested"}
    if include_flat_field:
        add_capture(source="flat_field_ray", purpose="flat_field", source_cache="ray")
        flat_field = {"status": "planned", "capture_id": captures[-1]["capture_id"]}

    return {
        "schema_version": 1,
        "status": "planned",
        "measurement": {
            "kind": "camera_based_rgbww_optimizer_raw_observer_validation",
            "anchor": {
                "cct": int(anchor_cct),
                "gm": int(anchor_gm),
                "ray_intensity_percent": float(ray_intensity_percent),
                "strip_command": strip_command,
            },
            "paired_repeats": int(paired_repeats),
            "linearity_factors": list(factors),
            "linearity_repeats": int(linearity_repeats),
            "flat_field": flat_field,
            "source_isolation": "every capture requires the other source to be off",
        },
        "inputs": {
            "baseline_lut": _file_reference(lut_path),
            "location_config": _file_reference(Path(location_config_path)),
            "raw_observer_config": _file_reference(Path(observer_config_path)),
        },
        "captures": captures,
        "cleanup": {
            "python": "required_on_normal_exit_exception_and_keyboard_interrupt",
            "shell": "required_via_wrapper_trap",
            "strip_and_ray": "must_both_be_attempted_even_if_one_shutdown_fails",
        },
    }


def write_raw_observer_validation_dry_run(
    *,
    output_root: str | Path,
    run_name: str | None,
    **plan_kwargs: Any,
) -> Path:
    """Write exactly the immutable dry-run plan and perform no device I/O."""

    run_dir = Path(output_root) / (run_name or datetime.now().strftime("%Y%m%d-%H%M%S"))
    run_dir.mkdir(parents=True, exist_ok=False)
    plan = build_raw_observer_validation_plan(**plan_kwargs)
    plan["status"] = "dry_run"
    plan["created_at"] = datetime.now(timezone.utc).isoformat()
    plan["run_dir"] = str(run_dir)
    output = run_dir / "plan.json"
    _write_json(output, plan)
    return output


def parse_linearity_factors(value: str) -> tuple[float, ...]:
    return _validate_linearity_factors(tuple(float(item.strip()) for item in value.split(",") if item.strip()))


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build the immutable dry-run plan for native Bayer raw observer validation."
    )
    parser.add_argument("--baseline-lut", required=True, type=Path)
    parser.add_argument("--location-config", type=Path, default=DEFAULT_LOCATION_CONFIG)
    parser.add_argument("--raw-observer-config", type=Path, default=DEFAULT_OBSERVER_CONFIG)
    parser.add_argument("--anchor-cct", type=int, default=DEFAULT_ANCHOR_CCT)
    parser.add_argument("--anchor-gm", type=int, default=DEFAULT_ANCHOR_GM)
    parser.add_argument("--ray-intensity-percent", type=float, default=DEFAULT_RAY_INTENSITY_PERCENT)
    parser.add_argument("--paired-repeats", type=int, default=DEFAULT_PAIRED_REPEATS)
    parser.add_argument("--linearity-factors", type=parse_linearity_factors, default=DEFAULT_LINEARITY_FACTORS)
    parser.add_argument("--linearity-repeats", type=int, default=DEFAULT_LINEARITY_REPEATS)
    parser.add_argument("--off-seconds", type=float, default=DEFAULT_OFF_SECONDS)
    parser.add_argument("--settle-seconds", type=float, default=DEFAULT_SETTLE_SECONDS)
    parser.add_argument("--include-flat-field", action="store_true")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_ROOT)
    parser.add_argument("--run-name")
    parser.add_argument("--dry-run", action="store_true", required=True)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    output = write_raw_observer_validation_dry_run(
        output_root=args.output_dir,
        run_name=args.run_name,
        baseline_lut_path=args.baseline_lut,
        location_config_path=args.location_config,
        observer_config_path=args.raw_observer_config,
        anchor_cct=args.anchor_cct,
        anchor_gm=args.anchor_gm,
        ray_intensity_percent=args.ray_intensity_percent,
        paired_repeats=args.paired_repeats,
        linearity_factors=args.linearity_factors,
        linearity_repeats=args.linearity_repeats,
        off_seconds=args.off_seconds,
        settle_seconds=args.settle_seconds,
        include_flat_field=args.include_flat_field,
    )
    print(output)
    return 0


def _validate_linearity_factors(values: Sequence[float]) -> tuple[float, ...]:
    factors = tuple(float(value) for value in values)
    if len(factors) < 2 or any(value <= 0 for value in factors) or len(set(factors)) != len(factors):
        raise ValueError("linearity_factors must contain at least two unique positive values")
    if 1.0 not in factors:
        raise ValueError("linearity_factors must include 1.0")
    return factors


def _file_reference(path: Path) -> dict[str, str]:
    if not path.is_file():
        raise ValueError(f"required input file does not exist: {path}")
    return {"path": str(path), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


def _write_json(path: Path, data: Mapping[str, Any]) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
