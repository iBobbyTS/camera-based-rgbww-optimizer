"""Full-frame exposure profiling: the first-line check for exposure triage.

GUIDE11 lesson (2026-09-26): a block-level trimmed mean reads *low* on a
saturated frame because clipped pixels drop out of the statistic, which once
turned 91-percent-saturated white frames into an "underexposed, go slower"
misdiagnosis. Any anomalous block readout must therefore be checked against
a full-frame profile before any exposure-direction conclusion is drawn.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any, Mapping, Sequence


SATURATION_THRESHOLD = 65_000
SATURATED_FRAME_FRACTION = 0.25
DARK_FRAME_MEAN = 2_000


def frame_exposure_profile(cr3_path: str | Path) -> dict[str, Any]:
    """Read one CR3 and return its full-frame exposure profile.

    The profile is deliberately independent of the patch statistics chain:
    rawpy postprocess with camera white balance and no auto brightness, then
    full-frame means, percentiles, saturation fraction, and a per-channel
    structure check. ``classification`` distinguishes saturated / dark /
    normal so exposure-direction triage cannot be fooled twice.
    """
    import rawpy
    import numpy as np

    path = Path(cr3_path)
    with rawpy.imread(str(path)) as raw:
        rgb = raw.postprocess(use_camera_wb=True, no_auto_bright=True, output_bps=16)
    arr = np.asarray(rgb, dtype=np.float64).reshape(-1, 3)
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
        "classification": classification,
        "mean_per_channel": [round(float(v), 1) for v in mean],
        "p99_per_channel": [round(float(v), 1) for v in p99],
        "saturated_fraction": round(float(saturated), 4),
        "channel_structure_ratio": round(structure, 2),
        "warning": (
            "block trimmed means read LOW on saturated frames; never infer "
            "exposure direction from block statistics alone"
            if classification == "saturated" else None
        ),
    }


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
