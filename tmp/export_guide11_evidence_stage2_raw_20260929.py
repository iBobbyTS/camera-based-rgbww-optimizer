"""GUIDE11 evidence export, stage 2: read-only small numeric extraction from existing CR3s.

For every CR3 referenced by the exported run ledgers: recompute SHA-256
(verify against the recorded value), extract the rawpy rgb_xyz_matrix
(first 3 rows, exactly as white_calibration_common.load_rawpy_rgb_xyz_matrix
returns it), dedupe matrices by content hash into matrices/, and recompute
frame_exposure_profile for the strip frames the GUIDE11 color analyzers
actually profiled. No new capture, no device access; CR3 bytes are only
read. Resume-tolerant via raw-index.jsonl append log.
"""
from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path

DATA = Path("D:/rgbww-optimizer")
REPO = Path("C:/Users/iBobb/Projects/WLED-RGBWW")
STAGE = DATA / "tmp/guide11-evidence-export-20260929/stage"
PKG = STAGE / "GUIDE11-COMPLETE-PROCESSED-EVIDENCE-20260929"
PROGRESS = STAGE / "stage2-progress.log"

import sys
sys.path.insert(0, str(REPO / "src"))

from camera_based_rgbww_optimizer.measurement.frame_exposure import (  # noqa: E402
    frame_exposure_profile,
)
from camera_based_rgbww_optimizer.optimization.white_calibration_common import (  # noqa: E402
    load_rawpy_rgb_xyz_matrix,
)

GROUPS = ("guide11", "guide9", "guide10", "foundations")


def resolve_path(old: str) -> Path:
    p = Path(old)
    if p.exists():
        return p
    # Mac-era data root prefix -> current Windows data root.
    old_s = str(old)
    if old_s.startswith("/Volumes/4T/temp/rgbww-optimizer/"):
        p = Path("D:/rgbww-optimizer") / old_s[len("/Volumes/4T/temp/rgbww-optimizer/"):]
        if p.exists():
            return p
    # Post-reorg layout: D:/rgbww-optimizer/<group>/<first-component>/...
    try:
        first = p.relative_to(DATA).parts[0]
        rest = p.relative_to(DATA / first)
    except Exception:
        return p
    for g in GROUPS:
        cand = DATA / g / first / rest
        if cand.exists():
            return cand
    return p


def log(msg: str) -> None:
    line = f"[{time.strftime('%H:%M:%S')}] {msg}"
    print(line, flush=True)
    with PROGRESS.open("a", encoding="utf-8") as fh:
        fh.write(line + "\n")


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def matrix_id_for(matrix, matrix_cache: dict) -> str:
    import numpy as np
    content = json.dumps(np.asarray(matrix).tolist())
    mid = hashlib.sha256(content.encode()).hexdigest()[:16]
    if mid not in matrix_cache:
        dest = PKG / "matrices" / f"{mid}.json"
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(json.dumps({
            "matrix_id": mid,
            "shape": [3, 3],
            "rgb_xyz_matrix_first3": np.asarray(matrix).tolist(),
            "dedup_note": "raw.rgb_xyz_matrix[:3] via white_calibration_common.load_rawpy_rgb_xyz_matrix",
        }, indent=2) + "\n", encoding="utf-8")
        matrix_cache[mid] = True
    return mid


def iter_cr3_refs() -> list[dict]:
    """One entry per referenced CR3: alias, capture_id, old path, recorded sha."""
    refs: dict[tuple[str, str], dict] = {}

    def add(alias: str, capture_id: str, old_path: str, recorded_sha: str | None, recorded_bytes: int | None, role: str):
        key = (alias, capture_id)
        if key in refs:
            refs[key]["roles"].append(role)
            return
        refs[key] = {
            "alias": alias, "capture_id": capture_id, "old_path": old_path,
            "recorded_sha256": recorded_sha, "recorded_byte_count": recorded_bytes,
            "roles": [role],
        }

    for captures in sorted((PKG / "runs").rglob("captures.jsonl")):
        alias = captures.parent.relative_to(PKG / "runs").as_posix()
        for line in captures.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            row = json.loads(line)
            cap = row.get("capture") or {}
            sf = cap.get("saved_file")
            if sf:
                add(alias, str(row["capture_id"]), sf, cap.get("sha256"), cap.get("byte_count"), "captures")
    for phys in sorted((PKG / "runs").rglob("physical-returns.jsonl")):
        alias = phys.parent.relative_to(PKG / "runs").as_posix()
        for line in phys.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            row = json.loads(line)
            cid = row.get("capture_id")
            cp = row.get("cr3_path")
            if cid and cp:
                add(alias, str(cid), cp, row.get("cr3_sha256"), row.get("cr3_byte_count"), "physical_returns")
    return list(refs.values())


def profile_frame_set() -> set[tuple[str, str]]:
    """Replicate the analyzer profiling scope: strip rows in the color roots."""
    scope: set[tuple[str, str]] = {}
    roots = [
        "guide11-c1/formal-c1b2-20260926-r6",
        "guide11-c1/formal-c1c-20260928-r1",
        "guide11-c1/formal-c1c-20260928-r2-suffix",
        "guide11-c1/formal-c1c-20260928-r3-suffix",
        "guide11-c2/formal-c2s25-20260928-r1",
        "guide11-c2/formal-c2s25-20260928-r2-suffix",
        "guide11-c4/formal-c4-20260928-r1",
        "guide11-c5/formal-c5-20260928-r1",
    ]
    for alias in roots:
        captures = PKG / "runs" / alias / "captures.jsonl"
        if not captures.is_file():
            continue
        for line in captures.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            row = json.loads(line)
            if str(row.get("source_id")) != "strip":
                continue
            sf = (row.get("capture") or {}).get("saved_file")
            if sf:
                scope[(alias, str(row["capture_id"]))] = sf
    return scope


def main() -> None:
    t0 = time.time()
    refs = iter_cr3_refs()
    log(f"CR3 references collected: {len(refs)}")

    done: set[tuple[str, str]] = set()
    index_path = PKG / "profiles" / "raw-index.jsonl"
    index_path.parent.mkdir(parents=True, exist_ok=True)
    if index_path.exists():
        for line in index_path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                r = json.loads(line)
                done.add((r["alias"], r["capture_id"]))
    matrix_cache: dict[str, bool] = {}
    for f in (PKG / "matrices").glob("*.json") if (PKG / "matrices").is_dir() else []:
        matrix_cache[f.stem] = True

    import numpy as np
    mismatch = 0
    missing = 0
    n_new = 0
    with index_path.open("a", encoding="utf-8") as out:
        for ref in refs:
            key = (ref["alias"], ref["capture_id"])
            if key in done:
                continue
            real = resolve_path(ref["old_path"])
            if not real.exists():
                missing += 1
                out.write(json.dumps({
                    **ref, "resolved_path": str(real), "status": "file_missing_after_reorg_search",
                }, sort_keys=True) + "\n")
                log(f"MISSING {ref['alias']}/{ref['capture_id']}")
                continue
            sha = sha256_of(real)
            sha_ok = (ref["recorded_sha256"] is None) or (sha == ref["recorded_sha256"])
            if not sha_ok:
                mismatch += 1
            try:
                matrix = load_rawpy_rgb_xyz_matrix(real, np)
                mid = matrix_id_for(matrix, matrix_cache)
            except Exception as exc:
                mid = None
                log(f"MATRIX-FAIL {ref['capture_id']}: {exc}")
            bytes_ok = (ref["recorded_byte_count"] is None) or (real.stat().st_size == ref["recorded_byte_count"])
            out.write(json.dumps({
                **ref,
                "resolved_path": str(real),
                "recomputed_sha256": sha,
                "recomputed_byte_count": real.stat().st_size,
                "sha256_matches_ledger": sha_ok,
                "byte_count_matches_ledger": bytes_ok,
                "matrix_id": mid,
                "status": "ok",
            }, sort_keys=True) + "\n")
            n_new += 1
            if n_new % 25 == 0:
                log(f"hashed+matrix {n_new}/{len(refs)} elapsed={time.time()-t0:.0f}s")
    log(f"raw identity pass done: new={n_new} missing={missing} sha_mismatch={mismatch} elapsed={time.time()-t0:.0f}s")

    # Frame exposure profiles for the analyzer-profiled strip frames.
    scope = profile_frame_set()
    log(f"frame exposure profile scope: {len(scope)} strip frames")
    profiles_by_root: dict[str, dict] = {}
    pdir = PKG / "profiles" / "frame-exposure"
    pdir.mkdir(parents=True, exist_ok=True)
    for alias in sorted({a for a, _ in scope}):
        outfile = pdir / (alias.replace("/", "__") + ".json")
        if outfile.exists():
            log(f"profile file already exists, skipping root {alias}")
            continue
        rows = []
        for (a, cid), old_path in sorted(scope.items()):
            if a != alias:
                continue
            real = resolve_path(old_path)
            prof = frame_exposure_profile(str(real))
            rows.append({
                "alias": alias, "capture_id": cid,
                "raw_sha256_source": old_path,
                **prof,
            })
            log(f"profiled {cid} -> {prof['classification']} sat={prof['saturated_fraction']}")
        outfile.write_text(json.dumps({
            "schema": "guide11_frame_exposure_profile_export_v1",
            "source_module": "camera_based_rgbww_optimizer.measurement.frame_exposure.frame_exposure_profile",
            "algorithm_version": "as-of-export git tree (see source/)",
            "root_alias": alias,
            "frames": rows,
        }, indent=2) + "\n", encoding="utf-8")
    log(f"stage2 complete elapsed={time.time()-t0:.0f}s")


if __name__ == "__main__":
    main()
