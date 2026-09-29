"""GUIDE11 complete processed evidence export, stage 1: move nothing, copy small ledgers.

Offline, read-only over D:/rgbww-optimizer and the repo. Copies per-run
ledger JSON/JSONL, patch-statistics, CR3 sidecar metadata, inputs, launch
logs, derived artifacts, and frozen inputs into the staging tree for
GUIDE11-COMPLETE-PROCESSED-EVIDENCE-20260929.zip. Raw CR3 payloads are
never copied. Writes RUN_INDEX.json and COPY-MAP.jsonl for later stages.
"""
from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

DATA = Path("D:/rgbww-optimizer")
REPO = Path("C:/Users/iBobb/Projects/WLED-RGBWW")
STAGE = DATA / "tmp/guide11-evidence-export-20260929/stage"
PKG = STAGE / "GUIDE11-COMPLETE-PROCESSED-EVIDENCE-20260929"

MAX_TOP_LEVEL_BYTES = 8 * 1024 * 1024  # per single ledger/log file


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


# --- root inventory -----------------------------------------------------------

def classify(name: str) -> str:
    if name.startswith("formal-"):
        return "formal"
    if name.startswith("diag-"):
        return "diagnostic"
    if name.startswith("dry") or name.startswith("dryrun"):
        return "dry"
    return "other"


def collect_roots() -> list[dict]:
    roots: list[dict] = []
    for stage_dir in sorted((DATA / "guide11").iterdir()):
        if not stage_dir.is_dir():
            continue
        for child in sorted(stage_dir.iterdir()):
            if child.is_dir() and classify(child.name) in {"formal", "diagnostic", "dry"}:
                roots.append({
                    "stage_group": stage_dir.name,
                    "name": child.name,
                    "category": classify(child.name),
                    "source": child,
                    "alias": f"{stage_dir.name}/{child.name}",
                })
    g9_dependencies = [
        ("guide9-h120-s50-batch1-20260820/20260820-170318-fast-direct", "c3_anchor_hsi_reference"),
        ("guide9-h120-s25-batch1-20260821/20260821-204804-fast-direct", "c3_anchor_hsi_reference"),
        ("guide9-h0-s0-batch1-20260821/20260821-004205-fast-direct", "true_ray_hsi_sat0_int100"),
        ("guide9-h300-s50-batch1-20260823/20260823-220027-fast-direct", "c3_anchor_hsi_reference"),
        ("guide9-h300-s100-batch1-20260823/20260823-h300-retry2", "c3_anchor_hsi_reference"),
        ("guide9-h0-s0-best-repeat-20260821/20260821-031503-high-white", "true_ray_hsi_sat0_int100_and_c4_white_anchor"),
    ]
    for rel, why in g9_dependencies:
        src = DATA / "guide9" / rel
        if not src.is_dir():
            raise FileNotFoundError(src)
        roots.append({
            "stage_group": "guide9",
            "name": rel.replace("/", "__"),
            "category": "prior_guide_dependency",
            "source": src,
            "alias": f"guide9/{rel.replace('/', '__')}",
            "dependency_reason": why,
        })
    return roots


# --- copy helpers -------------------------------------------------------------

copy_map: list[dict] = []


def copy_file(src: Path, rel_dest: str) -> None:
    dest = PKG / rel_dest
    if dest.exists():
        raise FileExistsError(dest)
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dest)
    copy_map.append({
        "package_path": rel_dest,
        "source_path": str(src),
        "byte_count": src.stat().st_size,
    })


def copy_root_ledgers(root: dict) -> dict:
    src = root["source"]
    alias = root["alias"]
    counts = {"ledger_files": 0, "measurements": 0, "sidecars": 0, "input_files": 0}
    for f in sorted(src.iterdir()):
        if not f.is_file():
            continue
        if f.suffix.lower() in {".json", ".jsonl", ".txt", ".log"} and f.stat().st_size <= MAX_TOP_LEVEL_BYTES:
            copy_file(f, f"runs/{alias}/{f.name}")
            counts["ledger_files"] += 1
    meas = src / "measurements"
    if meas.is_dir():
        for f in sorted(meas.glob("*.patch-statistics.json")):
            copy_file(f, f"runs/{alias}/measurements/{f.name}")
            counts["measurements"] += 1
    cam = src / "camera"
    if cam.is_dir():
        for f in sorted(cam.glob("*.cr3.metadata.json")):
            copy_file(f, f"runs/{alias}/camera/{f.name}")
            counts["sidecars"] += 1
    inputs = src / "inputs"
    if inputs.is_dir():
        for f in sorted(inputs.rglob("*")):
            if f.is_file() and f.stat().st_size <= MAX_TOP_LEVEL_BYTES:
                copy_file(f, f"runs/{alias}/inputs/{f.relative_to(inputs).as_posix()}")
                counts["input_files"] += 1
    return counts


def summarize_run(root: dict, counts: dict) -> dict:
    src = root["source"]
    entry = {
        "alias": root["alias"],
        "category": root["category"],
        "source_path": str(src),
        **counts,
    }
    if root.get("dependency_reason"):
        entry["dependency_reason"] = root["dependency_reason"]
    run_json = src / "run.json"
    if run_json.is_file():
        r = json.loads(run_json.read_text(encoding="utf-8"))
        entry["run_state"] = {
            k: r.get(k) for k in (
                "experiment_id", "status", "cleanup", "completed_formal",
                "physical_cr3_count", "physical_returned_cr3_count",
                "accepted_formal_count", "finished_at",
            ) if k in r
        }
        entry["run_state"]["git"] = r.get("git")
    failure = src / "failure.json"
    if failure.is_file():
        try:
            fj = json.loads(failure.read_text(encoding="utf-8"))
            entry["failure"] = {k: fj.get(k) for k in ("classification", "error", "stage", "reason") if k in fj} or {"keys": sorted(fj)[:8]}
        except Exception:
            entry["failure"] = {"unparseable": True}
    captures = src / "captures.jsonl"
    if captures.is_file():
        rows = [json.loads(l) for l in captures.read_text(encoding="utf-8").splitlines() if l.strip()]
        by_source: dict[str, int] = {}
        by_role: dict[str, int] = {}
        for row in rows:
            s = str(row.get("source_id"))
            by_source[s] = by_source.get(s, 0) + 1
            role = str((row.get("plan_step") or {}).get("role") or row.get("capture_role") or "?")
            by_role[role] = by_role.get(role, 0) + 1
        entry["capture_count"] = len(rows)
        entry["captures_by_source"] = by_source
        entry["captures_by_role"] = by_role
    phys = src / "physical-returns.jsonl"
    if phys.is_file():
        entry["physical_return_rows"] = sum(1 for l in phys.read_text(encoding="utf-8").splitlines() if l.strip())
    return entry


def main() -> None:
    if PKG.exists():
        raise SystemExit(f"staging dir already exists: {PKG}")
    PKG.mkdir(parents=True)

    roots = collect_roots()
    run_index = {"schema": "guide11_evidence_run_index_v1", "runs": []}
    for root in roots:
        counts = copy_root_ledgers(root)
        run_index["runs"].append(summarize_run(root, counts))

    # Group-level launch logs, resume/preflight records inside guide11 groups.
    extras = 0
    for stage_dir in sorted((DATA / "guide11").iterdir()):
        if not stage_dir.is_dir():
            continue
        for f in sorted(stage_dir.glob("*launch*.log")):
            if f.stat().st_size <= MAX_TOP_LEVEL_BYTES:
                copy_file(f, f"runs/{stage_dir.name}/_launch-logs/{f.name}")
                extras += 1
        for f in sorted(stage_dir.glob("*.json")):
            copy_file(f, f"runs/{stage_dir.name}/{f.name}")
            extras += 1

    # Derived artifacts (analysis outputs) and frozen inputs.
    derived_copies = {
        DATA / "guide11/guide11-c1/derived": "derived/guide11-c1",
        DATA / "guide11/guide11-c2/derived": "derived/guide11-c2",
        DATA / "guide11/guide11-c4/derived": "derived/guide11-c4",
        DATA / "guide11/guide11-c5/derived": "derived/guide11-c5",
        DATA / "guide11/guide11-n1/derived": "derived/guide11-n1",
        DATA / "guide11/guide11-w2/derived": "derived/guide11-w2",
        DATA / "guide11/guide11-w3/derived": "derived/guide11-w3",
        DATA / "guide11/guide11-w4/derived": "derived/guide11-w4",
    }
    for src_dir, rel in derived_copies.items():
        for f in sorted(src_dir.glob("*.json*")):
            copy_file(f, f"{rel}/{f.name}")
    frozen_inputs = {
        DATA / "guide11/guide11-w3/frozen-lut-20260923.json": "frozen-inputs/frozen-lut-20260923.json",
        DATA / "guide11/guide11-w8/guide11-white-final-report-20260928.json": "frozen-inputs/guide11-white-final-report-20260928.json",
        DATA / "guide10/guide10-white70-w8-final/guide10-white70-final-artifact.json": "frozen-inputs/guide10-white70-final-artifact.json",
    }
    for src_f, rel in frozen_inputs.items():
        copy_file(src_f, rel)

    run_index["root_count"] = len(run_index["runs"])
    run_index["extra_group_files"] = extras
    (PKG / "RUN_INDEX.json").write_text(json.dumps(run_index, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    with (STAGE / "COPY-MAP.jsonl").open("w", encoding="utf-8") as fh:
        for item in copy_map:
            fh.write(json.dumps(item, sort_keys=True) + "\n")

    total_bytes = sum(i["byte_count"] for i in copy_map)
    print(f"roots: {len(run_index['runs'])} | copied files: {len(copy_map)} | {total_bytes/1e6:.1f} MB | extras: {extras}")
    by_cat: dict[str, int] = {}
    for r in run_index["runs"]:
        by_cat[r["category"]] = by_cat.get(r["category"], 0) + 1
    print("by category:", by_cat)
    print("staging:", PKG)


if __name__ == "__main__":
    main()
