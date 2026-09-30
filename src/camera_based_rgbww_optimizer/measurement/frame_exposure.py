"""Full-frame RENDERED-RGB exposure profiling: the first-line triage check.

GUIDE11 lesson (2026-09-26): a block-level trimmed mean reads *low* on a
saturated frame because clipped pixels drop out of the statistic, which once
turned 91-percent-saturated white frames into an "underexposed, go slower"
misdiagnosis. Any anomalous block readout must therefore be checked against a
full-frame profile before any exposure-direction conclusion is drawn.

GUIDE12 domain rule (2026-09-29): these profiles are computed on
``rawpy.postprocess`` output (camera white balance, color conversion and a
display curve applied), so their saturation fractions live in the RENDERED RGB
domain. They are an auxiliary diagnostic only; native CFA-plane rail
qualification is owned by ``measurement.raw_mosaic_patches`` and must not be
overridden by this rendered view, in either direction.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any, Mapping, Sequence


SATURATION_THRESHOLD = 65_000
SATURATED_FRAME_FRACTION = 0.25
DARK_FRAME_MEAN = 2_000


def rendered_rgb_exposure_profile(cr3_path: str | Path) -> dict[str, Any]:
    """Read one CR3 and return its full-frame rendered-RGB exposure profile.

    The profile is deliberately independent of the patch statistics chain:
    rawpy postprocess with camera white balance and no auto brightness, then
    full-frame means, percentiles, saturation fraction, and a per-channel
    structure check. ``classification`` distinguishes saturated / dark /
    normal so exposure-direction triage cannot be fooled twice.

    The numbers are in the rendered RGB postprocess domain (see module
    docstring): a ``saturated`` classification here does NOT by itself
    disqualify a native CFA plane, and a ``normal`` classification here does
    NOT certify the native planes are below the protective white rail.
    """
    import rawpy
    import numpy as np

    path = Path(cr3_path)
    with rawpy.imread(str(path)) as raw:
        rgb = raw.postprocess(use_camera_wb=True, no_auto_bright=True, output_bps=16)
    arr = np.asarray(rgb, dtype="float64").reshape(-1, 3)
    mean = arr.mean(axis=0)
    p99 = np.percentile(arr, 99, axis=0)
    saturated = (arr >= SATURATION_THRESHOLD).any(axis=1).mean()
    structure = float(np.max(mean) / max(np.min(mean), 1.0))
    if saturated >= SATURATED_FRAME_FRACTION:
        classification = "saturated"
    elif float(mean.mean()) <= DARK_FRAME_MEAN:
        classification = "dark"
    else:
        classification = "normal"
    return {
        "file": str(path),
        "domain": "rendered_rgb_postprocess",
        "classification": classification,
        "mean_per_channel": [round(float(v), 1) for v in mean],
        "p99_per_channel": [round(float(v), 1) for v in p99],
        "saturated_fraction": round(float(saturated), 4),
        "channel_structure_ratio": round(structure, 2),
        "warning": (
            "rendered-RGB domain; block trimmed means read LOW on saturated "
            "frames, and this profile cannot override native CFA rail "
            "qualification in either direction"
            if classification == "saturated" else None
        ),
    }


def frame_exposure_profile(cr3_path: str | Path) -> dict[str, Any]:
    """Deprecated GUIDE11 name for :func:`rendered_rgb_exposure_profile`."""
    return rendered_rgb_exposure_profile(cr3_path)


# Direct alias so historical callers keep the exact GUIDE11 entry point
# while all new call sites use the rendered-domain name.
frame_exposure_profile = rendered_rgb_exposure_profile


def profile_from_run_captures(
    captures_jsonl: str | Path, camera_dir: str | Path, limit: int | None = None,
) -> list[dict[str, Any]]:
    """Profile the CR3 files referenced by a run's captures ledger."""
    rows = [
        json.loads(line)
        for line in Path(captures_jsonl).read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    profiles = []
    for row in rows[: limit or len(rows)]:
        raw_value = (row.get("capture") or {}).get("saved_file")
        if not raw_value:
            continue
        profiles.append({
            "capture_id": row.get("capture_id"),
            **frame_exposure_profile(str(raw_value)),
        })
    return profiles


def main(argv: Sequence[str] | None = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(
        description="Full-frame exposure profiles for CR3 files or a run's captures."
    )
    parser.add_argument("paths", nargs="*", help="CR3 files to profile")
    parser.add_argument("--captures-jsonl", type=Path)
    parser.add_argument("--limit", type=int)
    args = parser.parse_args(argv)
    profiles: list[dict[str, Any]] = []
    if args.captures_jsonl:
        camera_dir = Path(args.captures_jsonl).parent / "camera"
        profiles = profile_from_run_captures(args.captures_jsonl, camera_dir, args.limit)
    for path in args.paths:
        profiles.append(frame_exposure_profile(path))
    print(json.dumps(profiles, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
