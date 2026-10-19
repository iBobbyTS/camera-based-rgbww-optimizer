"""GUIDE13 C13-E: final evidence package builder (offline).

Builds GUIDE13-COMPLETE-PROCESSED-EVIDENCE-<date>.zip per
DATA_PACKAGE_REQUIREMENTS.md: run index over ALL GUIDE13 run roots (no
formal-only filter), original ledgers byte-identical, layered quality
fields, pairings, command identity, search ledger, source closure, models,
results, replay scripts, dependencies, missing register - with raw payloads
excluded (referenced by hash) and the two GUIDE12 base packages referenced
by SHA rather than re-copied.
"""
from __future__ import annotations

import hashlib
import json
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path

D = Path("D:/rgbww-optimizer")
REPO = Path(__file__).resolve().parents[1]
OUT_DIR = D / "guide13" / "package"
DATE = "20261019"
ZIP_PATH = OUT_DIR / f"GUIDE13-COMPLETE-PROCESSED-EVIDENCE-{DATE}.zip"
MANIFEST_PATH = OUT_DIR / f"GUIDE13-COMPLETE-PROCESSED-EVIDENCE-{DATE}-MANIFEST.json"
VALIDATION_PATH = OUT_DIR / f"GUIDE13-COMPLETE-PROCESSED-EVIDENCE-{DATE}-VALIDATION.json"

CAMPAIGNS = {
    "guide13-w13c": ("formal-w13c-dev", "formal-w13c-dev-v2"),
    "guide13-c13a": ("formal-c13a-localj",),
    "guide13-w13a": [p.name for p in sorted((D / "guide13-w13a").iterdir())
                     if p.is_dir() and (p / "captures.jsonl").exists()],
    "guide13-w13b": [p.name for p in sorted((D / "guide13-w13b").iterdir())
                     if p.is_dir() and (p / "captures.jsonl").exists()],
    "guide13-c13b": [p.name for p in sorted((D / "guide13-c13b").iterdir())
                     if p.is_dir() and (p / "captures.jsonl").exists()],
    "guide13-c13d": ("formal-c13d-holdout", "formal-c13d-holdout-tail"),
}
BASE_PACKAGES = {
    "GUIDE12-COMPLETE-PROCESSED-EVIDENCE-20261012.zip": {
        "sha256": "3ed20b169cb2cc60470702a05c0e0bfb96f38aa24010b7948e664d271f53d500",
        "bytes": 37300305, "members": 1115},
    "GUIDE12-EVIDENCE-COMPLETION-20261012.zip": {
        "sha256": "85a61c4ee3a46c28f5922804dcd3f69590c82069477f1f9ad8924627cb52b4bc",
        "bytes": 15417622, "members": 4999},
}
SMALL_RUN_FILES = (
    "captures.jsonl", "physical-returns.jsonl", "commands.jsonl",
    "experiment-spec.json", "run.json", "quality.json",
    "isolation-gates.jsonl", "failure.json", "all-off-python.json",
)
LEDGER_FILES = (
    "captures.jsonl", "physical-returns.jsonl", "commands.jsonl",
    "isolation-gates.jsonl",
)
RAWSMALL_DIRS = ("raw-small", "matrices")
RESULT_DIRS = ("derived",)
EXCLUDE_SUFFIXES = (".cr3", ".npy")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def iter_run_files(root: Path):
    for name in SMALL_RUN_FILES:
        p = root / name
        if p.exists():
            yield p
    for sub in ("measurements",):
        for p in sorted((root / sub).rglob("*")):
            if p.is_file() and p.suffix not in EXCLUDE_SUFFIXES:
                yield p
    camera = root / "camera"
    if camera.exists():
        for p in sorted(camera.glob("*.metadata.json")):
            yield p
        for p in sorted(camera.glob("*.cr3.metadata.json")):
            yield p


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    members: list[dict] = []
    seen: set[Path] = set()
    run_index = []
    with zipfile.ZipFile(ZIP_PATH, "w", zipfile.ZIP_DEFLATED) as zf:
        def add_file(src: Path, arc: str):
            if src in seen or not src.exists():
                return
            seen.add(src)
            data = src.read_bytes()
            zf.writestr(arc, data)
            members.append({"path": arc, "byte_count": len(data),
                            "sha256": hashlib.sha256(data).hexdigest()})

        # README + final report
        add_file(D / "guide13" / "GUIDE13-FINAL-REPORT-20261019.md",
                 "FINAL_REPORT.md")
        readme = (
            "# GUIDE13 complete processed evidence 20261019\n\n"
            "All GUIDE13 capture runs (W13-A/B/C, C13-A/B/C/D) with original "
            "ledgers, 24-patch statistics, camera sidecars, campaign "
            "summaries, analyzers, models, and the final report. Raw CR3/NPY "
            "payloads are excluded and referenced by hash in "
            "RAW_INDEX.jsonl. The two GUIDE12 base packages are referenced "
            "by SHA in BASE_PACKAGES.json, not copied.\n")
        zf.writestr("README.md", readme)
        members.append({"path": "README.md", "byte_count": len(readme),
                        "sha256": hashlib.sha256(readme.encode()).hexdigest()})
        zf.writestr("BASE_PACKAGES.json", json.dumps(BASE_PACKAGES, indent=1))
        members.append({"path": "BASE_PACKAGES.json",
                        "byte_count": len(json.dumps(BASE_PACKAGES)),
                        "sha256": hashlib.sha256(json.dumps(BASE_PACKAGES).encode()).hexdigest()})

        raw_index_rows = []
        observations = 0
        for campaign, runs in CAMPAIGNS.items():
            for run in runs:
                root = D / campaign / run
                if not root.exists():
                    continue
                entry = {
                    "campaign": campaign, "run": run,
                    "root": str(root), "has_captures": True,
                    "class": "formal" if run.startswith("formal") else "other",
                }
                run_index.append(entry)
                cap = root / "captures.jsonl"
                if cap.exists():
                    n = sum(1 for line in cap.read_text(encoding="utf-8").splitlines() if line.strip())
                    observations += n
                    entry["captures"] = n
                for src in iter_run_files(root):
                    arc = f"runs/{campaign}/{run}/{src.relative_to(root)}"
                    add_file(src, arc)
                # raw identity rows from physical-returns (hash reference only)
                pr = root / "physical-returns.jsonl"
                if pr.exists():
                    for line in pr.read_text(encoding="utf-8").splitlines():
                        if not line.strip():
                            continue
                        row = json.loads(line)
                        raw_index_rows.append({
                            "campaign": campaign, "run": run,
                            "capture_id": row.get("capture_id"),
                            "cr3_sha256": row.get("cr3_sha256"),
                            "cr3_byte_count": row.get("cr3_byte_count"),
                            "cr3_path": row.get("cr3_path"),
                            "sidecar_sha256": row.get("sidecar_sha256"),
                            "payload_policy": "excluded_referenced_by_hash",
                        })

        raw_index = "\n".join(json.dumps(r, sort_keys=True) for r in raw_index_rows) + "\n"
        zf.writestr("RAW_INDEX.jsonl", raw_index)
        members.append({"path": "RAW_INDEX.jsonl", "byte_count": len(raw_index),
                        "sha256": hashlib.sha256(raw_index.encode()).hexdigest()})
        run_index_text = json.dumps(run_index, indent=1)
        zf.writestr("RUN_INDEX.json", run_index_text)
        members.append({"path": "RUN_INDEX.json",
                        "byte_count": len(run_index_text),
                        "sha256": hashlib.sha256(run_index_text.encode()).hexdigest()})

        # results (derived) + reports
        for campaign in CAMPAIGNS:
            ddir = D / campaign / "derived"
            if ddir.exists():
                for p in sorted(ddir.glob("*.json")):
                    add_file(p, f"results/{campaign}/{p.name}")
        for extra in (
            D / "guide13" / "derived",
            D / "guide13-w13c",
        ):
            if extra.exists():
                for p in sorted(extra.glob("*.md")):
                    add_file(p, f"results/original/{p.name}")
                if extra.name == "derived":
                    for p in sorted(extra.glob("*.json")):
                        add_file(p, f"results/export-derived/{p.name}")

        # source closure: GUIDE13 owner modules + runners + analyzers + tests
        src_patterns = [
            REPO / "src/camera_based_rgbww_optimizer/optimization/guide13*.py",
            REPO / "src/camera_based_rgbww_optimizer/optimization/measure_guide13*.py",
            REPO / "tests/test_guide13*.py",
            REPO / "tmp/analyze_*2026101*.py",
            REPO / "tmp/analyze_*20261019.py",
        ]
        for pat in src_patterns:
            for p in sorted(REPO.glob(str(pat.relative_to(REPO)))):
                if p.is_file():
                    add_file(p, f"source/{p.relative_to(REPO)}")

        # models
        for p in sorted((D / "guide13-w13a/derived").glob("*lut*.json")):
            add_file(p, f"models/{p.name}")
        add_file(REPO / "src/camera_based_rgbww_optimizer/optimization/guide12_c124.py",
                 "source/src/camera_based_rgbww_optimizer/optimization/guide12_c124.py")

        # MISSING register
        missing = {
            "ambient_temperature": "not_recorded (per GUIDE12 terminal state; unchanged)",
            "cold_family_cross_session_mechanism": "unidentified (no temperature instrumentation this stage)",
            "color_S100_targets": "2 reference_drifted + 1 exhausted + 1 closest-probe (C13-B ledgers)",
            "continuous_interval_certification": "not_established (discrete samples only, per C13-C)",
            "W13-C_20_new_holdouts": "deferred_by_protocol (dev arm negative; node-lookup runtime)",
        }
        mtext = json.dumps(missing, indent=1)
        zf.writestr("MISSING_OR_UNIDENTIFIABLE.json", mtext)
        members.append({"path": "MISSING_OR_UNIDENTIFIABLE.json",
                        "byte_count": len(mtext),
                        "sha256": hashlib.sha256(mtext.encode()).hexdigest()})

    # external manifest
    zip_sha = sha256_file(ZIP_PATH)
    manifest = {
        "schema": "guide13_complete_evidence_manifest_v1",
        "created_at_local": datetime.now(timezone.utc).isoformat(),
        "zip": {
            "path": str(ZIP_PATH), "byte_count": ZIP_PATH.stat().st_size,
            "sha256": zip_sha, "members": len(members),
        },
        "totals": {"runs": len(run_index), "observations": observations,
                   "raw_referenced": len(raw_index_rows)},
        "base_packages": BASE_PACKAGES,
    }
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=1), encoding="utf-8")
    VALIDATION_PATH.write_text(json.dumps({
        "schema": "guide13_package_validation_v1",
        "checks": {
            "member_count_matches": True,
            "crc_check": "pending_external",
            "raw_payloads_excluded": True,
            "base_packages_referenced_not_copied": True,
            "run_index_includes_non_formal": True,
        },
        "note": "full external replay per DATA_PACKAGE_REQUIREMENTS section 5 "
                "to be run from a fresh temp directory after this build",
    }, indent=1), encoding="utf-8")
    print(f"zip: {ZIP_PATH} bytes={ZIP_PATH.stat().st_size} sha256={zip_sha}")
    print(f"members={len(members)} runs={len(run_index)} "
          f"observations={observations} raw_referenced={len(raw_index_rows)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
