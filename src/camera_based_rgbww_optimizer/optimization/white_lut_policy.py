from __future__ import annotations

from collections.abc import Mapping
from typing import Any


RGB_CHANNELS = ("r", "g", "b")


def build_rgb_policy(
    *,
    target_cct: int,
    target_gm: int,
    endpoint_matches: Mapping[str, Mapping[str, Any]],
    cct_min: int,
    cct_max: int,
    gm_min: int,
    gm_max: int,
    native_penalty: float,
    outside_penalty: float,
    endpoint_penalty: float,
) -> dict[str, Any]:
    _validate_penalties(native_penalty, outside_penalty, endpoint_penalty)
    low_cct, low_gm, high_cct, high_gm = _endpoint_span(endpoint_matches)
    native_gm = interpolate_native_gm(
        target_cct,
        low_cct=low_cct,
        low_gm=low_gm,
        high_cct=high_cct,
        high_gm=high_gm,
    )
    cct_need, cct_direction = _cct_extension_need(
        target_cct,
        low_cct=low_cct,
        high_cct=high_cct,
        cct_min=cct_min,
        cct_max=cct_max,
    )
    gm_need, gm_direction = _gm_compensation_need(
        target_gm,
        native_gm=native_gm,
        gm_min=gm_min,
        gm_max=gm_max,
    )

    channel_needs = {channel: 0.0 for channel in RGB_CHANNELS}
    if gm_direction == "magenta":
        channel_needs["r"] = gm_need
        channel_needs["b"] = gm_need
    elif gm_direction == "green":
        channel_needs["g"] = gm_need
    if cct_direction == "warmer":
        channel_needs["r"] = max(channel_needs["r"], cct_need)
    elif cct_direction == "cooler":
        channel_needs["b"] = max(channel_needs["b"], cct_need)

    channel_penalties = {
        channel: _penalty_for_need(
            need,
            native_penalty=native_penalty,
            endpoint_penalty=endpoint_penalty,
        )
        for channel, need in channel_needs.items()
    }
    if cct_need > 0:
        cct_channel = "r" if cct_direction == "warmer" else "b"
        cct_cap = endpoint_penalty + (outside_penalty - endpoint_penalty) * (1.0 - cct_need)
        channel_penalties[cct_channel] = min(channel_penalties[cct_channel], cct_cap)

    combined_need = max(cct_need, gm_need)
    return {
        "kind": "native_gm_and_cct_extension_directional_rgb_penalty",
        "target_cct": int(target_cct),
        "target_gm": int(target_gm),
        "endpoint_span": {
            "low_cct": int(low_cct),
            "low_gm": float(low_gm),
            "high_cct": int(high_cct),
            "high_gm": float(high_gm),
        },
        "native_gm": float(native_gm),
        "cct_extension": {
            "direction": cct_direction,
            "need": float(cct_need),
        },
        "gm_compensation": {
            "direction": gm_direction,
            "need": float(gm_need),
        },
        "combined_rgb_need": float(combined_need),
        "channel_needs": channel_needs,
        "channel_penalties": channel_penalties,
        "effective_rgb_penalty": min(channel_penalties.values()),
        "native_penalty": float(native_penalty),
        "outside_penalty": float(outside_penalty),
        "endpoint_penalty": float(endpoint_penalty),
    }


def interpolate_native_gm(
    cct: int,
    *,
    low_cct: int,
    low_gm: float,
    high_cct: int,
    high_gm: float,
) -> float:
    if high_cct <= low_cct:
        raise ValueError("high_cct must be greater than low_cct")
    if int(cct) <= int(low_cct):
        return float(low_gm)
    if int(cct) >= int(high_cct):
        return float(high_gm)
    ratio = (float(cct) - float(low_cct)) / (float(high_cct) - float(low_cct))
    return float(low_gm) + ratio * (float(high_gm) - float(low_gm))


def _endpoint_span(
    endpoint_matches: Mapping[str, Mapping[str, Any]],
) -> tuple[int, float, int, float]:
    points = []
    for channel in ("ww", "cw"):
        if channel not in endpoint_matches:
            raise ValueError(f"missing endpoint match: {channel}")
        best = endpoint_matches[channel].get("best", {})
        points.append((int(best["cct"]), float(best["gm"])))
    points.sort(key=lambda point: point[0])
    if points[0][0] == points[1][0]:
        raise ValueError("endpoint CCT values must be distinct")
    return points[0][0], points[0][1], points[1][0], points[1][1]


def _cct_extension_need(
    target_cct: int,
    *,
    low_cct: int,
    high_cct: int,
    cct_min: int,
    cct_max: int,
) -> tuple[float, str]:
    if not cct_min < low_cct < high_cct < cct_max:
        raise ValueError("endpoint CCT span must be strictly inside the supported CCT range")
    if target_cct < low_cct:
        need = (float(low_cct) - float(target_cct)) / (float(low_cct) - float(cct_min))
        return _clamp01(need), "warmer"
    if target_cct > high_cct:
        need = (float(target_cct) - float(high_cct)) / (float(cct_max) - float(high_cct))
        return _clamp01(need), "cooler"
    return 0.0, "inside"


def _gm_compensation_need(
    target_gm: int,
    *,
    native_gm: float,
    gm_min: int,
    gm_max: int,
) -> tuple[float, str]:
    if not gm_min < native_gm < gm_max:
        raise ValueError("native_gm must be strictly inside the supported G/M range")
    if float(target_gm) < native_gm:
        need = (native_gm - float(target_gm)) / (native_gm - float(gm_min))
        return _clamp01(need), "magenta"
    if float(target_gm) > native_gm:
        need = (float(target_gm) - native_gm) / (float(gm_max) - native_gm)
        return _clamp01(need), "green"
    return 0.0, "native"


def _penalty_for_need(need: float, *, native_penalty: float, endpoint_penalty: float) -> float:
    remaining = 1.0 - _clamp01(need)
    return float(endpoint_penalty) + (float(native_penalty) - float(endpoint_penalty)) * remaining * remaining


def _validate_penalties(native_penalty: float, outside_penalty: float, endpoint_penalty: float) -> None:
    if endpoint_penalty < 0:
        raise ValueError("endpoint_penalty must be non-negative")
    if not endpoint_penalty <= outside_penalty <= native_penalty:
        raise ValueError("penalties must satisfy endpoint <= outside <= native")


def _clamp01(value: float) -> float:
    return min(max(float(value), 0.0), 1.0)
