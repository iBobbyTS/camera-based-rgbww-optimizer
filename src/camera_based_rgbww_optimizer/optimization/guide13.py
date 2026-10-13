"""GUIDE13 shared offline-correction owners (frozen).

Scientific contract: advisor/13/13.GUIDE.md. This module owns the
corrected measurement semantics that GUIDE12 got wrong or collapsed:

- layered quality: the primary block_06 four-native-CFA-plane gate is
  separate from the 58-feature secondary layer; a frame rejected only by
  the secondary layer stays a legal primary observation, and a primary
  rejection can never be cured by deleting planes or widening gates
  (GUIDE13 section 1.2);
- primary chromaticity z = (ln(R/G), ln(B/G)) with G=(G1+G2)/2;
- the true local 2D Jacobian J = [dz/dH, dz/dS] whose two columns come
  from measured Ray responses along the H and S directions (they need
  not be orthogonal; rotating the radial direction by 90 degrees is not
  a Hue derivative - GUIDE13 section C13-A);
- interval primitives with the correct Student-t values, including the
  pre-declared two-sided Bonferroni joint-95% coefficient for three
  outputs at df=2 (7.64880394), and prediction intervals computed
  separately from mean CIs (GUIDE13 section 2.2).

No device access, no new runtime: these are the frozen analysis owners.
"""
from __future__ import annotations

import math
from typing import Any, Iterable, Mapping, Sequence

PRIMARY_BLOCK_INDEX = 6
PRIMARY_PLANES = ("R", "G1", "G2", "B")
FULLSCALE = 4095
STRIP_READBACK_CHANNELS = {
    "cw": "cold_white", "ww": "warm_white", "r": "red", "g": "green", "b": "blue",
}

# Two-sided Bonferroni t for a joint 95% region over 3 outputs (CCT,
# mired, Duv) with df=2: t(1 - 0.05/(2*3), 2). The GUIDE12-era code
# hardcoded 9.925, which is t(0.98333, 2) - the single-comparison value
# for 3 outputs, not the joint coefficient.
T_JOINT_95_DF2_THREE_OUTPUTS = 7.64880394


# ---------------------------------------------------------------- layered
# quality


def primary_layer_from_stats(stats: Mapping[str, Any]) -> dict[str, Any]:
    """Primary-layer gate from one patch-statistics document: the main
    block's four native CFA planes must each be accepted with a finite,
    positive normalized-per-second trimmed mean."""
    patches = stats.get("patches") or []
    block = next(
        (p for p in patches if p.get("index") == PRIMARY_BLOCK_INDEX), None)
    planes: dict[str, Any] = {}
    nps: dict[str, float | None] = {}
    if block is None:
        return {
            "primary_quality": "missing_block",
            "planes": {p: "missing" for p in PRIMARY_PLANES},
            "planes_nps": {p: None for p in PRIMARY_PLANES},
            "block_found": False,
        }
    for plane in PRIMARY_PLANES:
        blk = (block.get("planes") or {}).get(plane)
        if blk is None:
            planes[plane] = "missing"
            nps[plane] = None
            continue
        status = (blk.get("quality") or {}).get("status")
        raw = ((blk.get("statistics") or {}).get("normalized_per_second")
               or {}).get("trimmed_mean")
        value = float(raw) if raw is not None else None
        ok = (
            status == "accepted"
            and value is not None
            and math.isfinite(value)
            and value > 0.0
        )
        if ok:
            planes[plane] = "accepted"
        elif status == "accepted":
            planes[plane] = "invalid_value"
        else:
            planes[plane] = status or "missing_value"
        nps[plane] = value
    quality = "accepted" if all(
        planes[p] == "accepted" for p in PRIMARY_PLANES) else "rejected"
    return {
        "primary_quality": quality,
        "planes": planes,
        "planes_nps": nps,
        "block_found": True,
    }


def secondary58_from_capture(row: Mapping[str, Any]) -> str | None:
    """The legacy 58-feature global gate result as recorded at capture
    time. Reported alongside - never instead of - the primary layer."""
    return ((row.get("capture") or {}).get("direct_quality") or {}).get("status")


def fullscale_from_command(cmd: Mapping[str, Any]) -> dict[str, Any]:
    """Actual-PWM readback of one strip command ledger row: the channel
    values read back after apply and whether at least one channel sits
    at 4095 (the GUIDE13 definition of an actual fullscale output)."""
    snapshot = ((cmd.get("readback") or {}).get("device_snapshot")
                or (cmd.get("applied") or {}).get("device_snapshot") or {})
    channels = {
        ch: int(snapshot[name]) for ch, name in STRIP_READBACK_CHANNELS.items()
        if isinstance(snapshot.get(name), (int, float))
    }
    if not channels:
        return {"readback_channels": {}, "max_channel": None,
                "actual_fullscale": False}
    winner = max(channels, key=lambda ch: channels[ch])
    return {
        "readback_channels": channels,
        "max_channel": winner,
        "actual_fullscale": channels[winner] >= FULLSCALE,
    }


def z_from_planes(planes_nps: Mapping[str, float | None]) -> tuple[float, float]:
    """Primary chromaticity z=(ln(R/G), ln(B/G)), G=(G1+G2)/2."""
    g1, g2 = planes_nps["G1"], planes_nps["G2"]
    if g1 is None or g2 is None or planes_nps["R"] is None \
            or planes_nps["B"] is None:
        raise ValueError("z_from_planes requires all four primary planes")
    g = 0.5 * (g1 + g2)
    if g <= 0 or planes_nps["R"] <= 0 or planes_nps["B"] <= 0:
        raise ValueError("z_from_planes requires positive plane levels")
    return (
        math.log(planes_nps["R"] / g),
        math.log(planes_nps["B"] / g),
    )


# ------------------------------------------------------------- local 2D
# Jacobian


def local_jacobian(
    dz_over_dH: Sequence[float],
    dz_over_dS: Sequence[float],
) -> list[list[float]]:
    """J = [dz/dH, dz/dS] as 2x2 column-major rows: row index is the z
    component, column 0 the H direction, column 1 the S direction. Both
    columns must come from measured Ray responses along those menu
    directions; nothing here assumes they are orthogonal."""
    if len(dz_over_dH) != 2 or len(dz_over_dS) != 2:
        raise ValueError("local_jacobian needs 2-component columns")
    return [
        [float(dz_over_dH[0]), float(dz_over_dS[0])],
        [float(dz_over_dH[1]), float(dz_over_dS[1])],
    ]


def solve_local_delta(
    jacobian: Sequence[Sequence[float]],
    dz: Sequence[float],
    *,
    min_singular: float = 1e-9,
) -> tuple[float, float]:
    """(dH, dS) = J^-1 dz. Raises when J is (numerically) singular - a
    singular model Jacobian means the local linear map cannot be
    inverted here; it is never silently replaced by a 90-degree
    rotation."""
    (a, b), (c, d) = jacobian
    det = a * d - b * c
    if not math.isfinite(det) or abs(det) < min_singular:
        raise ValueError(
            f"local Jacobian singular (det={det}); no local inverse exists")
    dx, dy = float(dz[0]), float(dz[1])
    return ((d * dx - b * dy) / det, (-c * dx + a * dy) / det)


def local_delta_covariance(
    jacobian: Sequence[Sequence[float]],
    dz_covariance: Sequence[Sequence[float]],
    *,
    min_singular: float = 1e-9,
) -> list[list[float]]:
    """Cov(delta) = J^-1 Cov(dz) J^-T for a 2x2 dz covariance."""
    (a, b), (c, d) = jacobian
    det = a * d - b * c
    if not math.isfinite(det) or abs(det) < min_singular:
        raise ValueError(
            f"local Jacobian singular (det={det}); no local inverse exists")
    (vx, xy), (_, vy) = dz_covariance
    # J^-1 = 1/det [[d, -b], [-c, a]]
    i00, i01 = d / det, -b / det
    i10, i11 = -c / det, a / det
    # (J^-1 C J^-T)
    m00 = i00 * i00 * vx + 2 * i00 * i01 * xy + i01 * i01 * vy
    m01 = i00 * i10 * vx + (i00 * i11 + i01 * i10) * xy + i01 * i11 * vy
    m11 = i10 * i10 * vx + 2 * i10 * i11 * xy + i11 * i11 * vy
    return [[m00, m01], [m01, m11]]


# ------------------------------------------------------------- interval
# primitives


def sample_sd(values: Sequence[float]) -> float:
    n = len(values)
    if n < 2:
        raise ValueError("sample_sd needs n>=2")
    mean = sum(values) / n
    return math.sqrt(sum((v - mean) ** 2 for v in values) / (n - 1))


def mean_ci(values: Sequence[float], t_value: float) -> dict[str, float]:
    """mean +- t*s/sqrt(n) (independent-unit CI at whatever level the
    t_value declares)."""
    n = len(values)
    mean = sum(values) / n
    half = t_value * sample_sd(values) / math.sqrt(n)
    return {"mean": mean, "n": n, "low": mean - half, "high": mean + half,
            "t_value": t_value, "half_width": half}


def prediction_interval_next_mean(
    values: Sequence[float], t_value: float, future_m: int,
) -> dict[str, float]:
    """PI for the mean of the next m future observations (same
    conditions): mean +- t*s*sqrt(1/n + 1/m). Computed independently of
    mean_ci; never a relabelled CI."""
    n = len(values)
    mean = sum(values) / n
    half = t_value * sample_sd(values) * math.sqrt(1.0 / n + 1.0 / future_m)
    return {"mean": mean, "n": n, "m": future_m, "low": mean - half,
            "high": mean + half, "t_value": t_value, "half_width": half,
            "estimand": f"mean_of_next_{future_m}_observations"}


def prediction_interval_next_single(
    values: Sequence[float], t_value: float,
) -> dict[str, float]:
    """PI for one future single observation: mean +- t*s*sqrt(1+1/n)."""
    return prediction_interval_next_mean(values, t_value, 1)


def interval_self_consistent(interval: Mapping[str, float]) -> bool:
    """low <= mean <= high and the declared half-width matches the
    bounds (GUIDE13: box center, half-width and bounds must agree)."""
    low, high, mean = interval["low"], interval["high"], interval["mean"]
    half = interval.get("half_width")
    if low > mean or mean > high:
        return False
    if half is None:
        return True
    return (abs((mean - low) - half) <= 1e-9
            and abs((high - mean) - half) <= 1e-9)


def sd_confidence_interval(
    values: Sequence[float], chi2_right: float, chi2_left: float,
) -> dict[str, float]:
    """Conditional CI for the SD via the chi-square pivot:
    sqrt((n-1)s^2/chi2_right) .. sqrt((n-1)s^2/chi2_left), where
    chi2_right > chi2_left are the two chi-square quantiles at the
    declared level (e.g. chi2(0.975, df) and chi2(0.025, df))."""
    n = len(values)
    s2 = sample_sd(values) ** 2
    return {
        "sd": math.sqrt(s2), "n": n,
        "low": math.sqrt((n - 1) * s2 / chi2_right),
        "high": math.sqrt((n - 1) * s2 / chi2_left),
    }
