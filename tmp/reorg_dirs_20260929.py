"""2026-09-29 directory reorganization: move-only, no deletion.

Groups .agent-work evidence files by guide stage and D:/rgbww-optimizer
data roots by guide/p7/foundations. Writes an auditable old->new map.
VENV, D: tmp/ snapshot, legacy archive, git bundle and repo PLAN files
stay in place. Run once; every move asserts source exists and
destination is absent.
"""
from __future__ import annotations

import hashlib
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(r"C:/Users/iBobb/Projects/WLED-RGBWW")
AW = REPO / ".agent-work"
DATA = Path(r"D:/rgbww-optimizer")
MAP_OUT = DATA / "REORG-MAP-20260929.json"

# --- .agent-work: explicit per-guide lists (PLAN.md/PLAN-FULL.md and the
# already-organized archived/debug/evidence/plans dirs stay at top level).
AW_GROUPS: dict[str, list[str]] = {
    "guide4": [
        "ADVISOR_HANDOFF-20260808-RAY-R6-HISTORY-FAIL.md",
        "ADVISOR_HANDOFF-20260808-RAY-R6-HISTORY-FAIL.zip",
    ],
    "guide5": [
        "ADVISOR_HANDOFF-20260810-GUIDE5-STRIP-HISTORY.md",
        "ADVISOR_HANDOFF-20260810-GUIDE5-STRIP-HISTORY-DATA.zip",
        "ADVISOR_HANDOFF-20260810-RAY-HISTORY-COLD600.md",
        "ADVISOR_HANDOFF-20260811-GUIDE5-RAY-FAST-LONG-BRIDGE.md",
        "ADVISOR_HANDOFF-20260811-GUIDE5-RAY-FAST-LONG-BRIDGE.zip",
        "ADVISOR_HANDOFF-20260812-GUIDE5-TD-C-CORE.md",
        "ADVISOR_HANDOFF-20260812-GUIDE5-TD-C-CORE.zip",
        "ADVISOR_HANDOFF-20260813-TD-C-FAST-ENDPOINT.md",
        "ADVISOR_HANDOFF-20260813-TD-C-FAST-ENDPOINT.zip",
        "ADVISOR_HANDOFF-20260813-TD-C-FAST-ENDPOINT-v2.zip",
        "ADVISOR_HANDOFF-20260813-TD-C-V3-EXACT-CONTEXT.md",
        "ADVISOR_HANDOFF-20260813-TD-C-V3-EXACT-CONTEXT.zip",
        "GUIDE5-STRIP-HISTORY-V3-RESULT.md",
        "HUMAN_DECISION-20260810-COLD600.md",
        "HUMAN_DECISION-20260810-OP120.md",
        "EXECUTION_RESULT-20260810-OP120-ATTEMPT1.md",
        ".advisor-pack-guide5-ray-bridge-20260811",
    ],
    "guide6": [
        "ADVISOR_HANDOFF-20260814-GUIDE6-SOLVER-RETRY.md",
        "ADVISOR_HANDOFF-20260814-GUIDE6-SOLVER-RETRY.zip",
        "ADVISOR_HANDOFF-20260815-GUIDE6-S-MEASUREMENT.md",
        "ADVISOR_HANDOFF-20260815-GUIDE6-S-MEASUREMENT.zip",
        "ADVISOR_HANDOFF-20260818-GUIDE6-LCB-CONTINUATION.md",
        "ADVISOR_HANDOFF-20260818-GUIDE6-LCB-CONTINUATION.zip",
        "guide6-solver-coordinate-review-20260814.md",
    ],
    "guide7": [
        "ADVISOR_HANDOFF-20260819-GUIDE7-F2-REPEATED-DRIFT.md",
        "ADVISOR_HANDOFF-20260819-GUIDE7-F2-REPEATED-DRIFT.zip",
        "ADVISOR_HANDOFF-20260820-GUIDE7-SCALE-RELAXED-STABILITY.md",
        "ADVISOR_HANDOFF-20260820-GUIDE7-SCALE-RELAXED-STABILITY.zip",
        "analysis-v2-f2-locally-bracketed-probes-derived.json",
    ],
    "guide9": [
        "ADVISOR_HANDOFF-20260823-GUIDE9-H300-RAY-REFERENCE.md",
        "ADVISOR_HANDOFF-20260823-GUIDE9-H300-RAY-REFERENCE-v1.zip",
        "ADVISOR_HANDOFF-20260823-GUIDE9-H300-RAY-REFERENCE-v2.zip",
        "EXECUTION_RESULT.md",
    ],
    "guide11": [
        "GUIDE11-C1-RESULT-20260925.md",
        "GUIDE11-C1B2-RESULT-20260927.md",
        "GUIDE11-C1C-RESULT-20260928.md",
        "GUIDE11-C2-ASSESSMENT-20260928.md",
        "GUIDE11-C2S25-RESULT-20260928.md",
        "GUIDE11-C4-RESULT-20260928.md",
        "GUIDE11-C5-RESULT-20260928.md",
        "GUIDE11-FINAL-PACKAGE-20260929.zip",
        "GUIDE11-FINAL-PACKAGE-MANIFEST-20260929.json",
        "GUIDE11-FINAL-PACKAGE-MANIFEST-20260929.md",
        "GUIDE11-FINAL-REPORT-20260929.md",
        "GUIDE11-HUMAN-GATE-20260925-whole-second-shutter.md",
        "GUIDE11-N1-RESULT-20260922.md",
        "GUIDE11-PAUSE-20260928.md",
        "GUIDE11-W2-PAUSE-20260923.md",
        "GUIDE11-W2-RESULT-20260923.md",
        "GUIDE11-W3-RESULT-20260924.md",
        "GUIDE11-W4-RESULT-20260924.md",
        "GUIDE11-W8P6-RESULT-20260928.md",
    ],
}

# --- D:/rgbww-optimizer: prefix routing plus an explicit foundations list.
DATA_GUIDE_PREFIXES = tuple(f"guide{i}-" for i in range(4, 12))
FOUNDATIONS = [
    "cct-multipatch-pilot",
    "chart-basis-mixtures",
    "chart-response-basis",
    "cr3",
    "dry-input",
    "firmware",
    "hsi-reference-repeatability",
    "hsi-uncertainty",
    "manual-five-channel-ray-comparison-20260817",
    "manual-ray-emission-check-20260817",
    "manual-strip-emission-check-20260817",
    "raw-observer-validation",
    "raw-shutter-response",
    "ray-hsi-manifold",
    "strip-hsi-pilot",
    "strip-state-readback-preflight",
    "white-endpoints",
    "white-lut",
    "white-lut-calibration",
    "white-repeatability",
    "workflow-local-lab-context-r1",
]
DATA_KEEP_TOP = {
    ".venv-windows",
    "README.md",
    "REORG-MAP-20260929.json",
    "tmp",
    "_archive-legacy-workflow-202606-202608",
    "git-branch-archive-rejected-g4-r6-20260922.bundle",
}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def snapshot(base: Path) -> list[str]:
    return sorted(p.name for p in base.iterdir())


def move_records(base: Path, groups: dict[str, list[str]]) -> list[dict]:
    records = []
    for group, names in groups.items():
        dest_dir = base / group
        dest_dir.mkdir(exist_ok=True)
        for name in names:
            src = base / name
            dst = dest_dir / name
            if not src.exists():
                if dst.exists():
                    # already moved by an earlier interrupted run of this script
                    continue
                raise FileNotFoundError(src)
            if dst.exists():
                raise FileExistsError(dst)
            shutil.move(str(src), str(dst))
            records.append(
                {
                    "from": str(src),
                    "to": str(dst),
                    "kind": "dir" if src.is_dir() else "file",
                }
            )
    return records


def main() -> int:
    before_aw = snapshot(AW)
    before_data = snapshot(DATA)

    # Integrity anchor: hash the GUIDE11 final package zip before/after.
    pkg = AW / "GUIDE11-FINAL-PACKAGE-20260929.zip"
    pkg_hash_before = sha256_file(pkg)

    aw_records = move_records(AW, AW_GROUPS)

    # Data side: route every non-keep top-level entry by prefix or list.
    data_groups: dict[str, list[str]] = {g: [] for g in
                                         [f"guide{i}" for i in range(4, 12)]
                                         + ["p7", "foundations"]}
    leftovers = []
    for name in before_data:
        if name in DATA_KEEP_TOP:
            continue
        if name.startswith(DATA_GUIDE_PREFIXES):
            data_groups[name.split("-")[0]].append(name)
        elif name.startswith("p7-"):
            data_groups["p7"].append(name)
        elif name in FOUNDATIONS:
            data_groups["foundations"].append(name)
        else:
            leftovers.append(name)
    if leftovers:
        raise RuntimeError(f"unclassified D: top-level entries: {leftovers}")
    data_records = move_records(DATA, data_groups)

    pkg_after = AW / "guide11" / "GUIDE11-FINAL-PACKAGE-20260929.zip"
    pkg_hash_after = sha256_file(pkg_after)

    report = {
        "schema": "rgbww_reorg_map_v1",
        "date": "2026-09-29",
        "policy": "move-only; nothing deleted or modified",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "agent_work_root": str(AW),
        "agent_work_kept_top_level": [
            n for n in snapshot(AW)
            if n not in {r["to"].split("\\")[-1] for r in aw_records}
        ],
        "agent_work_moves": aw_records,
        "data_root": str(DATA),
        "data_kept_top_level": sorted(DATA_KEEP_TOP & set(before_data)),
        "data_moves": data_records,
        "integrity_checks": {
            "guide11_final_package_zip": {
                "sha256_before": pkg_hash_before,
                "sha256_after": pkg_hash_after,
                "unchanged": pkg_hash_before == pkg_hash_after,
            }
        },
        "counts": {
            "agent_work_items_moved": len(aw_records),
            "data_items_moved": len(data_records),
        },
        "note": (
            "Historical manifests and frozen scripts record pre-move absolute "
            "paths (D:/rgbww-optimizer/<name>/...). Resolve them through this "
            "map: prepend the group directory, e.g. guide11-c1 -> "
            "guide11/guide11-c1. Repo-side .agent-work moves are additionally "
            "visible as git renames."
        ),
    }
    MAP_OUT.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n",
                       encoding="utf-8")

    after_aw = snapshot(AW)
    after_data = snapshot(DATA)
    print(json.dumps({
        "agent_work_top_before": len(before_aw),
        "agent_work_top_after": len(after_aw),
        "data_top_before": len(before_data),
        "data_top_after": len(after_data),
        "moved_agent_work": len(aw_records),
        "moved_data": len(data_records),
        "package_zip_unchanged": pkg_hash_before == pkg_hash_after,
        "map": str(MAP_OUT),
        "data_top_after_names": after_data,
        "agent_work_top_after_names": after_aw,
    }, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
