from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, replace
from typing import Any, Callable

from camera_based_rgbww_optimizer.control import esphome, ray120c


DEFAULT_RAY_OFF_CCT = 5600
DEFAULT_RAY_OFF_GM = 100

StripOffFn = Callable[[], dict[str, int]]
RayGetCctFn = Callable[..., dict[str, Any]]
RaySetCctFn = Callable[..., dict[str, Any]]


@dataclass(frozen=True)
class ShutdownStep:
    name: str
    ok: bool
    detail: dict[str, Any] | None = None
    error: str | None = None

    def to_jsonable(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "ok": self.ok,
            "detail": self.detail,
            "error": self.error,
        }


def turn_everything_off(
    *,
    strip: bool = True,
    ray: bool = True,
    ray_cct: int | None = None,
    ray_gm: int | None = None,
    ray_timeout: float | None = None,
    strip_off_fn: StripOffFn | None = None,
    ray_get_cct_fn: RayGetCctFn = ray120c.get_cct,
    ray_set_cct_fn: RaySetCctFn = ray120c.set_cct,
) -> list[ShutdownStep]:
    steps: list[ShutdownStep] = []
    if strip:
        steps.append(_turn_strip_off(strip_off_fn or _default_strip_off))
    if ray:
        steps.append(_turn_ray_off(ray_get_cct_fn, ray_set_cct_fn, cct=ray_cct, gm=ray_gm, timeout=ray_timeout))
    return steps


def _default_strip_off() -> dict[str, int]:
    return esphome.light(0, 0, 0, 0, 0)


def _turn_strip_off(strip_off_fn: StripOffFn) -> ShutdownStep:
    try:
        payload = strip_off_fn()
    except Exception as exc:
        return ShutdownStep("esphome", False, error=f"{type(exc).__name__}: {exc}")
    return ShutdownStep("esphome", True, detail={"payload": payload})


def _turn_ray_off(
    ray_get_cct_fn: RayGetCctFn,
    ray_set_cct_fn: RaySetCctFn,
    *,
    cct: int | None,
    gm: int | None,
    timeout: float | None,
) -> ShutdownStep:
    resolved_cct = DEFAULT_RAY_OFF_CCT if cct is None else int(cct)
    resolved_gm = DEFAULT_RAY_OFF_GM if gm is None else int(gm)
    current_error: str | None = None
    settings = _ray_settings(timeout)
    if cct is None or gm is None:
        try:
            current = ray_get_cct_fn(settings=settings)
            data = current.get("data", {})
            if cct is None:
                current_cct = int(data.get("cct", resolved_cct))
                if ray120c.CCT_MIN <= current_cct <= ray120c.CCT_MAX:
                    resolved_cct = current_cct
                else:
                    current_error = f"invalid current CCT {current_cct}; using fallback {resolved_cct}"
            if gm is None:
                current_gm = int(data.get("gm", resolved_gm))
                if ray120c.GM_MIN <= current_gm <= ray120c.GM_MAX:
                    resolved_gm = current_gm
                else:
                    current_error = f"invalid current G/M {current_gm}; using fallback {resolved_gm}"
        except Exception as exc:
            current_error = f"{type(exc).__name__}: {exc}"

    try:
        response = ray_set_cct_fn(resolved_cct, intensity=0, gm=resolved_gm, settings=settings)
    except Exception as exc:
        detail = {"cct": resolved_cct, "gm": resolved_gm}
        if current_error is not None:
            detail["current_read_error"] = current_error
        return ShutdownStep("ray120c", False, detail=detail, error=f"{type(exc).__name__}: {exc}")

    detail = {"cct": resolved_cct, "gm": resolved_gm, "response": response}
    if current_error is not None:
        detail["current_read_error"] = current_error
    return ShutdownStep("ray120c", True, detail=detail)


def _ray_settings(timeout: float | None) -> ray120c.OpenAPISettings:
    settings = ray120c.OpenAPISettings.from_env()
    if timeout is None:
        return settings
    return replace(settings, timeout=float(timeout))


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Turn off the ESPHome RGBWW strip and Ray120c reference light.")
    parser.add_argument("--skip-strip", action="store_true", help="Do not call the ESPHome all_off action.")
    parser.add_argument("--skip-ray", action="store_true", help="Do not set the Ray120c intensity to 0.")
    parser.add_argument("--ray-cct", type=int, help="Fallback Ray120c CCT used for the off command.")
    parser.add_argument("--ray-gm", type=int, help="Fallback Ray120c GM used for the off command.")
    parser.add_argument("--ray-timeout", type=float, help="Ray120c OpenAPI timeout in seconds.")
    parser.add_argument("--json", action="store_true", help="Print machine-readable shutdown results.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    steps = turn_everything_off(
        strip=not args.skip_strip,
        ray=not args.skip_ray,
        ray_cct=args.ray_cct,
        ray_gm=args.ray_gm,
        ray_timeout=args.ray_timeout,
    )
    if args.json:
        print(json.dumps([step.to_jsonable() for step in steps], indent=2, sort_keys=True))
    else:
        for step in steps:
            if step.ok:
                print(f"{step.name}: off")
            else:
                print(f"{step.name}: failed: {step.error}", file=sys.stderr)
    return 0 if all(step.ok for step in steps) else 1


if __name__ == "__main__":
    raise SystemExit(main())
