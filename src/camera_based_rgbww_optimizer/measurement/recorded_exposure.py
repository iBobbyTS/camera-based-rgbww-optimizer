from __future__ import annotations

import json
import math
import subprocess
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any, Callable, Mapping, Sequence


ExiftoolRunner = Callable[[Sequence[str]], subprocess.CompletedProcess[str]]

CANON_EXPOSURE_KEYS = ("Canon:ExposureTime", "MakerNotes:ExposureTime")
STANDARD_EXPOSURE_KEYS = ("ExifIFD:ExposureTime", "EXIF:ExposureTime")


@dataclass(frozen=True)
class RecordedExposure:
    seconds: float
    source: str
    nominal_seconds: float
    nominal_shutter_speed: str
    raw_file: Path
    status: str
    metadata_values: Mapping[str, float | None]
    diagnostic: str | None = None

    def to_jsonable(self) -> dict[str, Any]:
        return {
            "seconds": self.seconds,
            "source": self.source,
            "status": self.status,
            "nominal_seconds": self.nominal_seconds,
            "nominal_shutter_speed": self.nominal_shutter_speed,
            "recorded_to_nominal_ratio": self.seconds / self.nominal_seconds,
            "raw_file": str(self.raw_file),
            "metadata_values": dict(self.metadata_values),
            "diagnostic": self.diagnostic,
        }


def resolve_recorded_exposure(
    raw_file: str | Path,
    nominal_shutter_speed: str,
    *,
    executable: str = "exiftool",
    runner: ExiftoolRunner | None = None,
) -> RecordedExposure:
    """Resolve physical exposure duration with explicit provenance.

    Canon CR3 files can report a MakerNote duration that differs materially from
    the display shutter stored in standard EXIF. The MakerNote value therefore
    owns measurement normalization when present. A nominal fallback is retained
    for degraded tooling, but its status makes it unsuitable for P1 acceptance.
    """

    path = Path(raw_file)
    nominal = parse_nominal_exposure(nominal_shutter_speed)
    command = (
        executable,
        "-j",
        "-G1",
        "-n",
        "-Canon:ExposureTime",
        "-EXIF:ExposureTime",
        str(path),
    )
    try:
        completed = (
            runner(command)
            if runner is not None
            else subprocess.run(command, check=False, capture_output=True, text=True, timeout=30)
        )
    except (OSError, subprocess.SubprocessError) as exc:
        return _nominal_fallback(path, nominal_shutter_speed, nominal, f"{type(exc).__name__}: {exc}")

    if completed.returncode != 0:
        diagnostic = completed.stderr.strip() or completed.stdout.strip() or f"exiftool exited {completed.returncode}"
        return _nominal_fallback(path, nominal_shutter_speed, nominal, diagnostic)

    try:
        payload = json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        return _nominal_fallback(path, nominal_shutter_speed, nominal, f"invalid exiftool JSON: {exc}")
    if not isinstance(payload, list) or len(payload) != 1 or not isinstance(payload[0], Mapping):
        return _nominal_fallback(path, nominal_shutter_speed, nominal, "exiftool did not return one metadata object")

    metadata = payload[0]
    values = {
        key: _positive_finite_float(metadata.get(key))
        for key in (*CANON_EXPOSURE_KEYS, *STANDARD_EXPOSURE_KEYS)
        if key in metadata
    }
    for key in CANON_EXPOSURE_KEYS:
        value = values.get(key)
        if value is not None:
            return _recorded(path, nominal_shutter_speed, nominal, value, key, values)
    for key in STANDARD_EXPOSURE_KEYS:
        value = values.get(key)
        if value is not None:
            return _recorded(path, nominal_shutter_speed, nominal, value, key, values)
    return _nominal_fallback(
        path,
        nominal_shutter_speed,
        nominal,
        "CR3 contains no positive Canon or standard EXIF ExposureTime",
        metadata_values=values,
    )


def parse_nominal_exposure(value: str) -> float:
    normalized = value.strip().lower()
    if normalized == "bulb":
        raise ValueError("bulb exposure cannot be normalized without recorded metadata")
    try:
        seconds = float(Fraction(normalized))
    except (ValueError, ZeroDivisionError) as exc:
        raise ValueError(f"unsupported nominal shutter speed: {value}") from exc
    if not math.isfinite(seconds) or seconds <= 0:
        raise ValueError("nominal shutter speed must be positive and finite")
    return seconds


def require_recorded(exposure: RecordedExposure, *, purpose: str) -> RecordedExposure:
    if exposure.status != "recorded":
        raise RuntimeError(
            f"recorded CR3 exposure metadata is required for {purpose}: {exposure.raw_file} "
            f"({exposure.diagnostic or exposure.source})"
        )
    return exposure


def _recorded(
    path: Path,
    nominal_shutter_speed: str,
    nominal: float,
    seconds: float,
    source: str,
    values: Mapping[str, float | None],
) -> RecordedExposure:
    return RecordedExposure(
        seconds=seconds,
        source=source,
        nominal_seconds=nominal,
        nominal_shutter_speed=nominal_shutter_speed,
        raw_file=path,
        status="recorded",
        metadata_values=values,
    )


def _nominal_fallback(
    path: Path,
    nominal_shutter_speed: str,
    nominal: float,
    diagnostic: str,
    *,
    metadata_values: Mapping[str, float | None] | None = None,
) -> RecordedExposure:
    return RecordedExposure(
        seconds=nominal,
        source="nominal_shutter_speed",
        nominal_seconds=nominal,
        nominal_shutter_speed=nominal_shutter_speed,
        raw_file=path,
        status="fallback_nominal",
        metadata_values={} if metadata_values is None else metadata_values,
        diagnostic=diagnostic,
    )


def _positive_finite_float(value: Any) -> float | None:
    try:
        result = float(value)
    except (TypeError, ValueError):
        return None
    return result if math.isfinite(result) and result > 0 else None
