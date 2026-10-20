"""D1 (GUIDE13 evidence completion 20261020): per-frame matrix extraction.

Offline, read-only over the 626 GUIDE13 CR3 payloads:
- re-hash every CR3 (sha256 + byte count + local timestamp) and compare with
  the recorded hash in the original package RAW_INDEX (hash_match is separate
  from not_rehashed; recorded hashes are never renamed),
- extract the actual rgb_xyz_matrix slice used by the white-point chain
  (raw.rgb_xyz_matrix[:3] == 3x3, per
  white_calibration_common.load_rawpy_rgb_xyz_matrix), dedupe by content and
  write matrices/<matrix_id>.json once per distinct content,
- emit RAW_INDEX_COMPLETE.jsonl with campaign/run/capture_id identity, capture
  and physical-return record hashes, sidecar reference, matrix_id, rawpy
  version, and the ISO/aperture distinction (plan vs bridge vs RAW EXIF),
- never fabricate: missing paths, unreadable files and missing EXIF are
  recorded as such with the search scope.

No device, camera or network access.
"""
from __future__ import annotations

import hashlib
import json
import sys
import time
from datetime import datetime
from pathlib import Path

import numpy as np
import rawpy

D = Path("D:/rgbww-optimizer")
WORK = D / "guide13" / "completion-20261020"
RAW_INDEX = WORK / "original-RAW_INDEX.jsonl"
OUT_ROWS = WORK / "RAW_INDEX_COMPLETE.jsonl"
OUT_MAT_DIR = WORK / "matrices"
SUMMARY = WORK / "d1-summary.json"
PROGRESS = WORK / "d1-progress.json"

OLD_GUIDE12_MATRIX_3X3 = [
    [0.9538999795913696, -0.27950000762939453, -0.12240000069141388],
    [-0.41749998927116394, 1.1998000144958496, 0.24580000340938568],
    [-0.04650000110268593, 0.17550000548362732, 0.6047999858856201],
]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def canonical_json(obj) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"))


def matrix_id_of(slice_3x3) -> str:
    return "mtx_" + hashlib.sha256(
        canonical_json([[float(v) for v in row] for row in slice_3x3]).encode("utf-8")
    ).hexdigest()[:16]


def line_hash(text_line: str) -> str:
    return hashlib.sha256(text_line.strip().encode("utf-8")).hexdigest()


def load_ledger_hashes(root: Path) -> tuple[dict[str, str], dict[str, dict]]:
    """capture_id -> line hash for captures.jsonl and physical-returns rows."""
    cap: dict[str, str] = {}
    pr: dict[str, dict] = {}
    f = root / "captures.jsonl"
    if f.exists():
        for line in f.read_text(encoding="utf-8").splitlines():
            if line.strip():
                row = json.loads(line)
                cid = str(row.get("plan_step", {}).get("capture_id", row.get("capture_id")))
                cap[cid] = line_hash(line)
    f = root / "physical-returns.jsonl"
    if f.exists():
        for line in f.read_text(encoding="utf-8").splitlines():
            if line.strip():
                row = json.loads(line)
                pr[str(row.get("capture_id"))] = {
                    "record_sha256": line_hash(line),
                    "cr3_path": row.get("cr3_path"),
                    "cr3_sha256": row.get("cr3_sha256"),
                    "cr3_byte_count": row.get("cr3_byte_count"),
                }
    return cap, pr


def main() -> int:
    OUT_MAT_DIR.mkdir(parents=True, exist_ok=True)
    rows = [
        json.loads(l) for l in RAW_INDEX.read_text(encoding="utf-8").splitlines() if l.strip()
    ]
    ledger_cache: dict[str, tuple[dict, dict]] = {}
    matrices: dict[str, dict] = {}
    out = OUT_ROWS.open("w", encoding="utf-8")
    stats = {
        "frames_total": len(rows), "hash_match": 0, "hash_mismatch": 0,
        "path_missing": 0, "read_error": 0, "distinct_matrices": 0,
        "matrix_shape_counts": {}, "matches_old_guide12_matrix_frames": 0,
    }
    t0 = time.time()
    for i, row in enumerate(rows):
        campaign, run, cid = row["campaign"], row["run"], str(row["capture_id"])
        root = D / campaign / run
        key = f"{campaign}/{run}"
        if key not in ledger_cache:
            ledger_cache[key] = load_ledger_hashes(root)
        cap_hashes, pr_rows = ledger_cache[key]

        path = Path(row["cr3_path"])
        located = "recorded_path"
        if not path.exists():
            cands = sorted((root / "camera").glob(f"{cid}-*.cr3"))
            if len(cands) == 1:
                path, located = cands[0], "relocated_by_capture_id_glob"
            else:
                stats["path_missing"] += 1
                out.write(json.dumps({
                    "campaign": campaign, "run": run, "capture_id": cid,
                    "status": "raw_not_located",
                    "search_scope": [row["cr3_path"], str(root / "camera")],
                    "recorded_cr3_sha256": row.get("cr3_sha256"),
                    "recorded_cr3_byte_count": row.get("cr3_byte_count"),
                    "sidecar_sha256_reference": row.get("sidecar_sha256"),
                }, sort_keys=True) + "\n")
                continue
        entry: dict = {
            "campaign": campaign, "run": run, "capture_id": cid,
            "status": "ok",
            "current_path": str(path),
            "path_located_by": located,
            "byte_count": path.stat().st_size,
            "recorded_cr3_sha256": row.get("cr3_sha256"),
            "recorded_cr3_byte_count": row.get("cr3_byte_count"),
            "recorded_identity_source": "GUIDE13-COMPLETE-PROCESSED-EVIDENCE-20261019.zip RAW_INDEX.jsonl",
            "sidecar_reference": {
                "sha256": row.get("sidecar_sha256"),
                "member": f"runs/{campaign}/{run}/camera/",
                "available_in_original_package": True,
            },
            "capture_record_sha256": cap_hashes.get(cid),
            "physical_return_record_sha256": pr_rows.get(cid, {}).get("record_sha256"),
        }
        try:
            rehash_start = datetime.now().isoformat(timespec="seconds")
            entry["rehash_sha256"] = sha256_file(path)
            entry["rehash_time_local"] = rehash_start
            entry["hash_match"] = entry["rehash_sha256"] == row.get("cr3_sha256")
            stats["hash_match" if entry["hash_match"] else "hash_mismatch"] += 1
        except OSError as exc:
            stats["read_error"] += 1
            entry.update({"status": "rehash_failed", "error": str(exc)})
            out.write(json.dumps(entry, sort_keys=True) + "\n")
            continue
        try:
            with rawpy.imread(str(path)) as raw:
                full = np.asarray(raw.rgb_xyz_matrix, dtype="float64")
            shape = "x".join(str(v) for v in full.shape)
            stats["matrix_shape_counts"][shape] = stats["matrix_shape_counts"].get(shape, 0) + 1
            used = full[:3, :3] if full.shape[1] >= 3 else full[:3]
            used_list = [[float(v) for v in r] for r in used]
            mid = matrix_id_of(used_list)
            entry["matrix"] = {
                "matrix_id": mid,
                "used_slice": "raw.rgb_xyz_matrix[:3, :3]",
                "raw_shape": list(full.shape),
                "rawpy_version": rawpy.__version__,
                "matches_old_guide12_matrix": used_list == OLD_GUIDE12_MATRIX_3X3,
            }
            if used_list == OLD_GUIDE12_MATRIX_3X3:
                stats["matches_old_guide12_matrix_frames"] += 1
            if mid not in matrices:
                blob = {
                    "schema": "guide13_completion_matrix_v1",
                    "matrix_id": mid,
                    "matrix_3x3": used_list,
                    "raw_full_matrix": [[float(v) for v in r] for r in full],
                    "raw_shape": list(full.shape),
                    "used_slice": "raw.rgb_xyz_matrix[:3, :3]",
                    "extraction": {
                        "library": "rawpy", "rawpy_version": rawpy.__version__,
                        "numpy_version": np.__version__,
                        "extracted_at_local": datetime.now().isoformat(timespec="seconds"),
                        "identity": "reanalysis/export (GUIDE13 evidence completion 20261020)",
                    },
                    "frame_count": 0,
                    "first_seen": {"campaign": campaign, "run": run, "capture_id": cid},
                    "matches_old_guide12_matrix": used_list == OLD_GUIDE12_MATRIX_3X3,
                }
                matrices[mid] = blob
                (OUT_MAT_DIR / f"{mid}.json").write_text(
                    json.dumps(blob, indent=1, sort_keys=True) + "\n", encoding="utf-8")
                stats["distinct_matrices"] += 1
            matrices[mid]["frame_count"] += 1
            entry["iso_aperture"] = {
                "plan": "implicit_auto (exposure-auto per plan step; no numeric ISO/aperture planned)",
                "bridge_return": "shutter seconds recorded in sidecar recorded_exposure; ISO/aperture not_recorded_in_sidecar",
                "raw_exif": "not_extracted_no_tool (no EXIF parser in frozen environment; no new acquisition permitted)",
            }
        except Exception as exc:  # matrix extraction failure must not lose the hash row
            entry["matrix"] = {"status": "extraction_failed", "error": repr(exc)[:300]}
        out.write(json.dumps(entry, sort_keys=True) + "\n")
        if (i + 1) % 25 == 0 or i + 1 == len(rows):
            PROGRESS.write_text(json.dumps({
                "done": i + 1, "total": len(rows),
                "elapsed_s": round(time.time() - t0, 1),
                "eta_s": round((time.time() - t0) / (i + 1) * (len(rows) - i - 1), 1),
                **{k: v for k, v in stats.items() if k != "matrix_shape_counts"},
            }), encoding="utf-8")
            print(f"[{i+1}/{len(rows)}] elapsed={time.time()-t0:.0f}s", flush=True)
    out.close()
    for mid, blob in matrices.items():
        (OUT_MAT_DIR / f"{mid}.json").write_text(
            json.dumps(blob, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    summary = {
        "schema": "guide13_completion_d1_summary_v1",
        "identity": "reanalysis/export (GUIDE13 evidence completion 20261020)",
        "generated_at_local": datetime.now().isoformat(timespec="seconds"),
        **stats,
        "matrix_usage_counts": {mid: blob["frame_count"] for mid, blob in matrices.items()},
        "elapsed_s": round(time.time() - t0, 1),
        "rawpy_version": rawpy.__version__,
        "numpy_version": np.__version__,
    }
    SUMMARY.write_text(json.dumps(summary, indent=1, sort_keys=True), encoding="utf-8")
    print(json.dumps({k: v for k, v in summary.items() if k != "matrix_usage_counts"}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
