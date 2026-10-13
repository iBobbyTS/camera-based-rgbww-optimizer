"""GUIDE12 evidence-completion incremental packager (offline export only).

Builds GUIDE12-EVIDENCE-COMPLETION-<date>.zip per the Advisor input request
GUIDE12_REVIEW_INPUT_REQUEST_20261012/CODEX_GUIDE12_EVIDENCE_COMPLETION_PROMPT.md:

- original per-run small ledgers for every run root (captures.jsonl with the
  FULL plan_step/capture objects, physical-returns.jsonl, commands.jsonl,
  spec/plan, run/quality, isolation/thermal ledgers, failure/recovery notes,
  inputs/, camera sidecars) — including the batch-1 roots, the N2 emission
  diagnostics, the zero-capture failed roots and campaign launch logs;
- complete rebuilt indexes (RUN_INDEX_COMPLETE / OBSERVATIONS_COMPLETE /
  RAW_INDEX_COMPLETE / PAIRINGS) fixing the base package's projection losses
  and the null RAW_INDEX (physical-returns use top-level cr3_* fields);
- per-frame rgb_xyz_matrix extracted offline from every retained RAW,
  deduplicated by content hash, referenced per frame via matrix_id;
- source closure: every camera_based_rgbww_optimizer module in the import
  closure of the packaged analyzers/measure entries, at its package path,
  plus the export scripts and frozen config inputs;
- retained derived analysis inputs (w12/c122 candidate-proposal chains and
  every campaign derived file not already byte-identical in the base zip);
- honest MISSING_OR_UNIDENTIFIABLE / DEPENDENCY_STATUS records.

No device, camera or network access. Raw CR3 payloads stay on
D:/rgbww-optimizer, referenced by hash.
"""
from __future__ import annotations

import hashlib
import json
import shutil
import sys
import zipfile
from datetime import datetime
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
WORK = REPO / ".agent-work" / "guide12"
DATA = Path("D:/rgbww-optimizer")
SCAN = WORK / "completion-workspace/raw-scan.json"
BASE_ZIP = WORK / "GUIDE12-COMPLETE-PROCESSED-EVIDENCE-20261012.zip"
BASE_INDEX = WORK / "base-manifest-index.json"
DATE = datetime.now().strftime("%Y%m%d")
OUT_ZIP = WORK / f"GUIDE12-EVIDENCE-COMPLETION-{DATE}.zip"
STAGE = WORK / "completion-workspace/stage"

CAMPAIGNS = [
    "guide12-batch1", "guide12-n2", "guide12-c12", "guide12-w12",
    "guide12-w122", "guide12-w123", "guide12-w124", "guide12-c122",
    "guide12-c124",
]
PKG_ROOT = REPO / "src/camera_based_rgbww_optimizer"

# import closure computed 2026-10-12 from the base-packaged analyzers plus
# every measure_guide12_* entry (ast walk incl. from-import names); the 16
# base-packaged members are re-included at package paths for importability.
CLOSURE_SEEDS = [
    "optimization/guide12.py", "optimization/guide12_n2.py",
    "optimization/guide12_c12.py", "optimization/guide12_w123.py",
    "optimization/guide12_w124.py", "optimization/guide12_c122.py",
    "optimization/guide12_c124.py",
    "optimization/measure_p7_thermal_diagnostics.py",
    "control/__init__.py", "control/all_off.py", "control/camera_gphoto2.py",
    "control/camera_remote.py", "control/camera_remote_v2.py",
    "control/esphome.py", "control/local_lab_context.py",
    "control/ray120c.py", "control/white_lut.py",
    "measurement/__init__.py", "measurement/hsi_policy_v2.py",
    "measurement/hsi_uncertainty.py", "measurement/raw_mosaic_patches.py",
    "measurement/raw_observer_analysis.py",
    "measurement/raw_response_candidate.py",
    "measurement/ray_hsi_manifold.py", "measurement/recorded_exposure.py",
    "optimization/__init__.py",
    "optimization/analyze_hsi_reference_repeatability.py",
    "optimization/analyze_p7_thermal_diagnostics.py",
    "optimization/analyze_raw_observer_validation.py",
    "optimization/bounded_least_squares.py", "optimization/hsi_objective.py",
    "optimization/hsi_source_evidence.py",
    "optimization/measure_channel_response.py",
    "optimization/measure_guide12_batch1.py",
    "optimization/measure_guide12_c12.py",
    "optimization/measure_guide12_c122.py",
    "optimization/measure_guide12_c124.py",
    "optimization/measure_guide12_n2.py",
    "optimization/measure_guide12_w12.py",
    "optimization/measure_guide12_w122.py",
    "optimization/measure_guide12_w123.py",
    "optimization/measure_guide12_w124.py",
    "optimization/measure_hsi_reference_repeatability.py",
    "optimization/measure_raw_observer_validation.py",
    "optimization/measure_ray_hsi_manifold.py",
    "optimization/p7_thermal_diagnostics.py",
    "optimization/white_calibration_common.py",
    "optimization/white_lut_feedback.py",
    "paths.py", "utils/__init__.py", "utils/location_regions.py",
    "__init__.py",
]

BASE_PACKAGED_SOURCE_FLAT = {  # base member name -> package-relative path
    "source/guide12.py": "optimization/guide12.py",
    "source/guide12_n2.py": "optimization/guide12_n2.py",
    "source/guide12_c12.py": "optimization/guide12_c12.py",
    "source/guide12_w123.py": "optimization/guide12_w123.py",
    "source/guide12_w124.py": "optimization/guide12_w124.py",
    "source/guide12_c122.py": "optimization/guide12_c122.py",
    "source/guide12_c124.py": "optimization/guide12_c124.py",
    "source/measure_p7_thermal_diagnostics.py":
        "optimization/measure_p7_thermal_diagnostics.py",
}

TMP_ANALYZERS = [
    REPO / "tmp/analyze_b1_exposure_20260930.py",
    REPO / "tmp/scan_guide12_completion_raw_20261012.py",
    REPO / "tmp/build_guide12_completion_package_20261012.py",
]


def sha_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def sha_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 22), b""):
            h.update(chunk)
    return h.hexdigest()


def read_jsonl(p: Path) -> list[dict]:
    if not p.exists():
        return []
    return [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]


def w(stage_rel: str, data: str) -> None:
    target = STAGE / stage_rel
    target.parent.mkdir(parents=True, exist_ok=True)
    with open(target, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(data)


def copy_in(src: Path, stage_rel: str, copy_map: list[dict]) -> None:
    target = STAGE / stage_rel
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, target)
    copy_map.append({
        "member": stage_rel, "source": str(src),
        "byte_count": src.stat().st_size, "sha256": sha_file(target),
    })


def main() -> int:
    if STAGE.exists():
        shutil.rmtree(STAGE)
    STAGE.mkdir(parents=True)

    base_index = json.loads(BASE_INDEX.read_text(encoding="utf-8"))
    base_shas = set(base_index.values())
    scan = json.loads(SCAN.read_text(encoding="utf-8"))
    scan_by_sha: dict[str, dict] = {}
    scan_by_path: dict[str, dict] = {}
    for rec in scan:
        scan_by_sha.setdefault(rec["recomputed_sha256"], rec)
        scan_by_path[rec["path"].replace("\\", "/")] = rec

    # unique matrices by content hash
    matrices: dict[str, dict] = {}
    for rec in scan:
        if rec.get("matrix_read") != "ok":
            continue
        canon = json.dumps(rec["rgb_xyz_matrix_first3"], separators=(",", ":"))
        mid = "mtx_" + hashlib.sha256(canon.encode()).hexdigest()[:16]
        m = matrices.setdefault(mid, {
            "matrix_id": mid, "matrix": rec["rgb_xyz_matrix_first3"],
            "referenced_frame_count": 0,
        })
        m["referenced_frame_count"] += 1
        rec["matrix_id"] = mid

    copy_map: list[dict] = []
    run_index_complete: list[dict] = []
    observations: list[dict] = []
    raw_index: list[dict] = []
    pairings: dict[str, dict] = {}
    missing: list[dict] = []
    stats_vs_phys_gaps: list[dict] = []
    thermal_temperature = {"rows": 0, "ambient_non_null": 0,
                           "surface_non_null": 0}
    base_run_index = None
    with zipfile.ZipFile(BASE_ZIP) as z:
        base_run_index = json.loads(z.read("RUN_INDEX.json"))
    base_alias_set = {r["run_alias"] for r in base_run_index}

    for campaign in CAMPAIGNS:
        croot = DATA / campaign
        # ---------- campaign-level loose files (launch logs, notes) ----------
        for p in sorted(croot.glob("*")):
            if p.is_file() and p.suffix in (".log", ".json", ".md"):
                copy_in(p, f"runs/{campaign}/_campaign/{p.name}", copy_map)

        # ---------- run roots ----------
        for root in sorted(croot.iterdir()):
            if not root.is_dir() or root.name == "derived":
                continue
            alias = f"{campaign}/{root.name}"
            klass = ("diagnostic" if root.name.startswith("diag-")
                     else "dry_plan" if root.name.startswith("dry-")
                     else "formal")
            cap_rows = read_jsonl(root / "captures.jsonl")
            phys_rows = read_jsonl(root / "physical-returns.jsonl")
            ms_files = sorted((root / "measurements").glob("*.patch-statistics.json")
                              ) if (root / "measurements").exists() else []
            runj = {}
            if (root / "run.json").exists():
                runj = json.loads((root / "run.json").read_text(encoding="utf-8"))
            in_base = alias in base_alias_set

            # --- observations: full rows preserved ---
            for row in cap_rows:
                observations.append({"run_alias": alias,
                                     "ledger": "captures.jsonl", **row})
            # recover rejected frames documented only in failure.json
            failure = None
            if (root / "failure.json").exists():
                failure = json.loads(
                    (root / "failure.json").read_text(encoding="utf-8"))
                rc = failure.get("rejected_capture") or {}
                cid = str(rc.get("capture_id") or "")
                if cid and cid not in {str(r.get("capture_id")) for r in cap_rows}:
                    observations.append({
                        "run_alias": alias, "ledger": "failure.json",
                        "capture_id": cid,
                        "recovered_rejected_capture": True,
                        "rejection_message": failure.get("message"),
                        "plan_step": None,
                        "note": ("capture rejected before the captures ledger "
                                 "was written; identity recovered from "
                                 "failure.json, NOT promoted to accepted"),
                        "cr3_sha256": rc.get("cr3_sha256"),
                        "cr3_byte_count": rc.get("cr3_byte_count"),
                    })

            # --- raw index rows: acquisition + stats + offline recompute ---
            hash_mismatch: list[dict] = []
            for pr in phys_rows:
                acq_sha = str(pr.get("cr3_sha256") or "")
                rec = scan_by_sha.get(acq_sha) or scan_by_path.get(
                    str(pr.get("cr3_path") or "").replace("\\", "/"))
                cid = str(pr.get("capture_id"))
                stats = root / "measurements" / f"{cid}.patch-statistics.json"
                stats_source = None
                stats_file_sha = None
                if stats.exists():
                    stats_file_sha = sha_file(stats)
                    try:
                        stats_source = (json.loads(
                            stats.read_text(encoding="utf-8")).get("source") or {})
                    except Exception:
                        stats_source = {}
                recomputed = rec["recomputed_sha256"] if rec else None
                if acq_sha and recomputed and acq_sha != recomputed:
                    hash_mismatch.append({
                        "run_alias": alias, "capture_id": cid,
                        "acquisition_sha256": acq_sha,
                        "recomputed_sha256": recomputed})
                if (stats_source.get("sha256") and acq_sha
                        and stats_source["sha256"] != acq_sha):
                    hash_mismatch.append({
                        "run_alias": alias, "capture_id": cid,
                        "acquisition_sha256": acq_sha,
                        "stats_source_sha256": stats_source["sha256"]})
                raw_index.append({
                    "run_alias": alias, "capture_id": cid,
                    "physical_index": pr.get("physical_index"),
                    "returned_at": pr.get("returned_at"),
                    "remote_capture_id": pr.get("remote_capture_id"),
                    "remote_request_id": pr.get("remote_request_id"),
                    "acquisition": {
                        "cr3_path": pr.get("cr3_path"),
                        "cr3_sha256": acq_sha,
                        "cr3_byte_count": pr.get("cr3_byte_count"),
                        "sidecar_path": pr.get("sidecar_path"),
                        "sidecar_sha256": pr.get("sidecar_sha256"),
                        "sidecar_byte_count": pr.get("sidecar_byte_count"),
                        "sidecar_validation_status":
                            pr.get("sidecar_validation_status"),
                        "accepted_measurement": pr.get("accepted_measurement"),
                    },
                    "stats_source": {
                        "sha256": stats_source.get("sha256"),
                        "path": stats_source.get("path"),
                        "stats_file_sha256": stats_file_sha,
                    },
                    "offline_recheck": (
                        {"path": rec["path"],
                         "byte_count": rec["byte_count"],
                         "recomputed_sha256": recomputed,
                         "readable": True,
                         "matrix_id": rec.get("matrix_id")}
                        if rec else
                        {"readable": False,
                         "status": "not_located_after_search"}),
                    "note": ("raw payload retained on D:/rgbww-optimizer; "
                             "not packaged"),
                })
                if not stats.exists():
                    stats_vs_phys_gaps.append({
                        "run_alias": alias, "capture_id": cid,
                        "status": "physical_return_without_patch_statistics"})
            if hash_mismatch:
                missing.append({
                    "item": f"raw hash chain mismatches in {alias}",
                    "status": "hash_mismatch",
                    "details": hash_mismatch,
                })
            # diagnostic payloads without physical-return ledgers
            if klass == "diagnostic":
                for p in sorted(root.iterdir()):
                    is_payload = (p.suffix == ".cr3" or
                                  (p.suffix == "" and "{{counter}}" in p.name))
                    if not (p.is_file() and is_payload):
                        continue
                    rec = scan_by_path.get(str(p).replace("\\", "/"))
                    receipt = None
                    for rj in sorted(root.glob("*.json")):
                        try:
                            d = json.loads(rj.read_text(encoding="utf-8"))
                        except Exception:
                            continue
                        if d.get("sha256") == (rec or {}).get("recomputed_sha256"):
                            receipt = {"receipt_file": rj.name,
                                       "recorded_sha256": d.get("sha256"),
                                       "recorded_byte_count": d.get("byte_count"),
                                       "iso": d.get("iso"),
                                       "shutter_speed": d.get("shutter_speed"),
                                       "aperture": d.get("aperture")}
                    raw_index.append({
                        "run_alias": alias, "capture_id": p.name,
                        "physical_index": None,
                        "diagnostic_payload": True,
                        "receipt": receipt,
                        "offline_recheck": (
                            {"path": rec["path"], "byte_count": rec["byte_count"],
                             "recomputed_sha256": rec["recomputed_sha256"],
                             "readable": True,
                             "matrix_id": rec.get("matrix_id")} if rec else
                            {"readable": False}),
                        "note": ("diagnostic emission/precheck capture; "
                                 "excluded from fullscale product samples"),
                    })

            # --- pairings: strip frames vs nearest ray frames in plan order ---
            ray_rows = [(i, r) for i, r in enumerate(cap_rows)
                        if str(r.get("plan_step", {}).get("source_id")) == "ray"]
            strip_pair_rows = []
            for i, row in enumerate(cap_rows):
                step = row.get("plan_step", {})
                if str(step.get("source_id")) != "strip":
                    continue
                before = next((r for j, r in reversed(ray_rows) if j < i), None)
                after = next((r for j, r in ray_rows if j > i), None)
                strip_pair_rows.append({
                    "capture_id": str(row.get("capture_id")),
                    "plan_index": i,
                    "candidate_tag": step.get("candidate_tag"),
                    "c122_tag": step.get("c122_tag"),
                    "w122_node": step.get("w122_node"),
                    "n2_state_key": step.get("n2_state_key"),
                    "n2_cycle_index": step.get("n2_cycle_index"),
                    "ray_before": (str(before["capture_id"])
                                   + f" (intensity "
                                   f"{before['plan_step'].get('command', {}).get('intensity_percent')})"
                                   ) if before else None,
                    "ray_after": (str(after["capture_id"])
                                  + f" (intensity "
                                  f"{after['plan_step'].get('command', {}).get('intensity_percent')})"
                                  ) if after else None,
                })
            if strip_pair_rows:
                pairings[alias] = {
                    "plan_frame_count": len(cap_rows),
                    "source_order": [str(r.get("plan_step", {}).get("source_id"))
                                     for r in cap_rows],
                    "strip_frames": strip_pair_rows,
                }

            # --- thermal covariate honesty stats ---
            for tc in read_jsonl(root / "thermal-covariates.jsonl"):
                thermal_temperature["rows"] += 1
                if tc.get("ambient_temperature_c") is not None:
                    thermal_temperature["ambient_non_null"] += 1
                if tc.get("source_surface_temperature_c") is not None:
                    thermal_temperature["surface_non_null"] += 1

            # --- run index entry ---
            run_index_complete.append({
                "run_alias": alias, "class": klass,
                "status": runj.get("status"),
                "started_at": runj.get("started_at"),
                "finished_at": runj.get("finished_at"),
                "git": runj.get("git"),
                "captures_ledger_rows": len(cap_rows),
                "patch_statistics": len(ms_files),
                "physical_returns": len(phys_rows),
                "cleanup": runj.get("cleanup"),
                "experiment": runj.get("schema"),
                "in_base_package": in_base,
                "source_root": str(root),
                "failure": (failure or {}).get("message") if failure else None,
            })

            # --- copy original small files (never RAW payloads) ---
            def is_payload(p: Path) -> bool:
                return (p.suffix in (".cr3", ".npy", ".CR3")
                        or (p.suffix == "" and "{{counter}}" in p.name))
            for p in sorted(root.iterdir()):
                if not p.is_file() or is_payload(p):
                    continue
                copy_in(p, f"runs/{alias}/{p.name}", copy_map)
            for sub in ("inputs", "camera"):
                sdir = root / sub
                if sdir.exists():
                    for p in sorted(sdir.iterdir()):
                        if p.is_file() and not is_payload(p):
                            copy_in(p, f"runs/{alias}/{sub}/{p.name}", copy_map)
            # measurements only for roots the base package lacks
            if not in_base and ms_files:
                for p in ms_files:
                    copy_in(p, f"measurements/{alias}/{p.name}", copy_map)

        # ---------- retained derived analysis inputs ----------
        der = croot / "derived"
        if der.exists():
            for p in sorted(der.rglob("*")):
                if p.is_file():
                    sha = sha_file(p)
                    member = f"results/original/{campaign}-derived/{p.name}"
                    if sha in base_shas:
                        continue
                    copy_in(p, member, copy_map)

    # ---------- source closure at package paths ----------
    dep_status: dict[str, dict] = {}
    for rel in CLOSURE_SEEDS:
        src = PKG_ROOT / rel
        member = f"source/src/camera_based_rgbww_optimizer/{rel}"
        sha = sha_file(src)
        flat = next((k for k, v in BASE_PACKAGED_SOURCE_FLAT.items()
                     if v == rel), None)
        already = None
        if flat and base_index.get(flat) == sha:
            already = {"already_in_base_package": {"member": flat, "sha256": sha,
                                                   "relationship": "byte-identical; re-included at package path for import closure"}}
        copy_in(src, member, copy_map)
        dep_status[f"source/{rel}"] = {
            "status": "exported_existing",
            "sha256": sha,
            **(already or {}),
        }
    for p in TMP_ANALYZERS:
        if p.exists():
            copy_in(p, f"scripts/{p.name}", copy_map)
    validator = REPO / "tmp/validate_guide12_completion_20261012.py"
    if validator.exists():
        copy_in(validator, "replay/validate_completion_package.py", copy_map)
    copy_in(REPO / "pyproject.toml", "source/pyproject.toml", copy_map)

    # ---------- config inputs ----------
    for p in sorted((REPO / "config").rglob("*")):
        if p.is_file():
            copy_in(p, f"config/{p.relative_to(REPO / 'config').as_posix()}",
                    copy_map)

    # ---------- matrices / raw-small ----------
    for mid, m in sorted(matrices.items()):
        w(f"matrices/{mid}.json", json.dumps({
            "schema": "guide12_rgb_xyz_matrix_v1",
            "matrix_id": mid,
            "matrix_3x3": m["matrix"],
            "source": ("rawpy.imread(raw).rgb_xyz_matrix[:3], offline re-read "
                       f"of every retained RAW on {DATE} "
                       "(tmp/scan_guide12_completion_raw_20261012.py)"),
            "frames_referencing": m["referenced_frame_count"],
        }, indent=1) + "\n")
        copy_map.append({
            "member": f"matrices/{mid}.json", "source": "generated",
            "sha256": sha_bytes((STAGE / f"matrices/{mid}.json").read_bytes()),
        })
    raw_small_dir = STAGE / "raw-small"
    raw_small_dir.mkdir(parents=True, exist_ok=True)
    by_sha_frames: dict[str, list[dict]] = {}
    for row in raw_index:
        acq = row.get("acquisition") or {}
        sha = (acq.get("cr3_sha256")
               or (row.get("offline_recheck") or {}).get("recomputed_sha256"))
        if not sha:
            continue
        by_sha_frames.setdefault(sha, []).append(row)
    for sha, rows in sorted(by_sha_frames.items()):
        first = rows[0]
        info = {
            "schema": "guide12_raw_small_identity_v1",
            "raw_sha256": sha,
            "hash_sources": {
                "acquisition_ledger": bool((first.get("acquisition") or {})
                                           .get("cr3_sha256")),
                "patch_statistics": ((first.get("stats_source") or {})
                                     .get("sha256")) is not None,
                "offline_recompute": (first.get("offline_recheck") or {})
                .get("readable") is True,
            },
            "byte_count": ((first.get("offline_recheck") or {})
                           .get("byte_count")
                           or (first.get("acquisition") or {}).get("cr3_byte_count")),
            "retained_path": (first.get("offline_recheck") or {}).get("path"),
            "sidecar": (first.get("acquisition") or {}).get("sidecar_sha256"),
            "matrix_id": (first.get("offline_recheck") or {}).get("matrix_id"),
            "frames": [{"run_alias": r["run_alias"],
                        "capture_id": r["capture_id"],
                        "diagnostic_payload": r.get("diagnostic_payload", False)}
                       for r in rows],
        }
        fp = raw_small_dir / f"{sha}.json"
        fp.write_text(json.dumps(info, indent=1, ensure_ascii=False) + "\n",
                      encoding="utf-8")
        copy_map.append({"member": f"raw-small/{sha}.json", "source": "generated",
                         "sha256": sha_bytes(fp.read_bytes())})

    # ---------- root index files ----------
    w("OBSERVATIONS_COMPLETE.jsonl",
      "\n".join(json.dumps(o, ensure_ascii=False) for o in observations) + "\n")
    w("RAW_INDEX_COMPLETE.jsonl",
      "\n".join(json.dumps(r, ensure_ascii=False) for r in raw_index) + "\n")
    w("RUN_INDEX_COMPLETE.json", json.dumps(run_index_complete, indent=1,
                                            ensure_ascii=False))
    w("PAIRINGS.json", json.dumps(pairings, indent=1, ensure_ascii=False))

    base_zip_sha = sha_file(BASE_ZIP)
    w("BASE_PACKAGE_REFERENCE.json", json.dumps({
        "base_zip": {
            "name": BASE_ZIP.name, "sha256": base_zip_sha,
            "byte_count": BASE_ZIP.stat().st_size,
            "manifest_members": len(base_index),
        },
        "relationship": ("incremental supplement; the base zip remains the "
                         "primary processed-evidence package and is not "
                         "modified or replaced"),
        "cross_reference_rule": ("members already present byte-identically in "
                                 "the base zip are not re-exported; DEPENDENCY_STATUS "
                                 "records the base member and sha"),
    }, indent=1))
    w("COPY_MAP.json", json.dumps(copy_map, indent=1, ensure_ascii=False))

    # ---------- missing / unidentifiable ----------
    missing.extend([
        {
            "item": "ambient_temperature_c in thermal-covariates.jsonl",
            "status": "not_recorded",
            "evidence": (f"{thermal_temperature['rows']} rows retained; "
                         f"ambient_temperature_c non-null in "
                         f"{thermal_temperature['ambient_non_null']}, "
                         f"source_surface_temperature_c non-null in "
                         f"{thermal_temperature['surface_non_null']}"),
            "note": "temperature covariates were not recorded by the harness; "
                    "not reconstructed from wait times",
        },
        {
            "item": "per-frame ISO/aperture in formal-run ledgers",
            "status": "not_recorded",
            "evidence": ("bridge sidecars record exposure timing and receipt "
                         "identity only; ISO/aperture appear only in the "
                         "standalone diagnostic capture receipts (iso=100, "
                         "aperture=implicit auto, e.g. runs/guide12-n2/"
                         "diag-ray-emission-20261003/a-capture.json)"),
        },
        {
            "item": "guide12-w123/diag-ray-precheck and "
                    "guide12-c122/diag-ray-precheck sidecar JSONs",
            "status": "not_recorded",
            "evidence": ("each directory retains only the CR3 payload; "
                         "identity provided by offline hash in "
                         "RAW_INDEX_COMPLETE (kind cr3, no receipt)"),
        },
        {
            "item": "three zero-capture stub run roots deleted after orphan-"
                    "process incidents during C12-2/3 (S0 block 5, H240/S50 "
                    "block 4, H0/S25 write+launch)",
            "status": "deleted_zero_capture_no_data",
            "evidence": ("GUIDE12-C122-RESULT-20261009.md §methodology note "
                         "records the third incident and the solo-background-"
                         "command discipline; the stub roots had zero captures "
                         "and no physical returns when deleted"),
        },
        {
            "item": "in-session C12-2/3 two-point interpolation arithmetic "
                    "(exact keystroke-level generator)",
            "status": "original_generator_not_retained",
            "evidence": ("retained evidence: derived/c122-*-candidates.json "
                         "(measured dz per candidate), derived/c122-next-*.json "
                         "(best command/dz, budget ledger), result-doc gate "
                         "tables, and the frozen formulas in the base package "
                         "(source/analyze_c12_2_block_20261009.py, "
                         "source/analyze_c12_4_20261012.py hue_basis); the "
                         "ad-hoc arithmetic executed in the operator session "
                         "was not captured as a script and is not "
                         "re-implemented here"),
        },
    ])
    if stats_vs_phys_gaps:
        missing.extend(stats_vs_phys_gaps)
    w("MISSING_OR_UNIDENTIFIABLE.json", json.dumps(missing, indent=1,
                                                   ensure_ascii=False))

    dep_extra = {
        "batch1_roots_and_derived": {
            "status": "exported_existing",
            "members": ["runs/guide12-batch1/...",
                        "measurements/guide12-batch1/...",
                        "results/original/guide12-batch1-derived/..."],
        },
        "rgb_xyz_matrix_per_frame": {
            "status": "export_derived_from_existing_raw_or_ledgers",
            "method": ("offline rawpy re-read of all 1076 retained RAW "
                       "payloads; unique matrices by content hash: "
                       f"{len(matrices)}; every frame references matrix_id in "
                       "RAW_INDEX_COMPLETE.jsonl"),
        },
        "raw_index_nulls": {
            "status": "export_derived_from_existing_raw_or_ledgers",
            "method": ("physical-returns.jsonl top-level cr3_*/sidecar_* "
                       "fields joined with the offline hash/matrix sweep; "
                       "three hash sources kept distinct (acquisition, "
                       "patch-statistics source, offline recompute)"),
        },
        "original_per_frame_ledgers": {
            "status": "exported_existing",
            "method": ("runs/<alias>/ holds the original bytes: captures.jsonl "
                       "(full plan_step/capture objects), physical-returns, "
                       "commands, spec/plan, run/quality, isolation, thermal, "
                       "failure/recovery, inputs/, camera sidecars, launch logs"),
        },
        "source_import_closure": {
            "status": "exported_existing",
            "method": ("ast import closure (incl. from-import names) over the "
                       "base-packaged analyzers and every measure_guide12_* "
                       "entry; 50 package files at package paths under "
                       "source/src/camera_based_rgbww_optimizer/"),
        },
        "observer_config": {
            "status": "exported_existing",
            "members": ["config/camera/raw-observer.json"],
        },
        "w12_c122_derived_analysis_inputs": {
            "status": "exported_existing",
            "members": ["results/original/guide12-w12-derived/",
                        "results/original/guide12-c122-derived/"],
        },
        "n2_emission_diagnostics": {
            "status": "exported_existing",
            "members": ["runs/guide12-n2/diag-ray-emission-20261003/",
                        "runs/guide12-n2/diag-ray-precheck-20261003b/",
                        "runs/guide12-n2/diag-ray-precheck-20261004/"],
        },
    }
    w("DEPENDENCY_STATUS.json", json.dumps({
        "per_source_module": dep_status, "per_dependency": dep_extra,
    }, indent=1, ensure_ascii=False))

    readme = f"""# GUIDE12-EVIDENCE-COMPLETION-{DATE}

Incremental offline export answering the Advisor input request
GUIDE12_REVIEW_INPUT_REQUEST_20261012. It supplements, and must be read
with, the base package GUIDE12-COMPLETE-PROCESSED-EVIDENCE-20261012.zip
(sha256 {base_zip_sha}); nothing in the base package is superseded.

Contents:
- runs/<campaign>/<root>/... — original per-run small ledgers (full
  captures.jsonl rows preserving plan_step/capture objects incl. n2_*,
  candidate_*, timing and isolation fields), failure/recovery notes,
  inputs/, camera sidecars, plus campaign launch logs and the batch-1,
  diagnostic and zero-capture roots the base packager skipped.
- measurements/ — patch statistics only for roots absent from the base
  package (batch-1: 16 frames; formal-n2-hsi-ladder-h240-r3: 1 rejected
  frame).
- matrices/ + raw-small/ — the single content-unique rgb_xyz_matrix used
  by the white-point chain (verified per-frame across 1076 RAWs) and
  per-RAW identity records with three distinct hash sources.
- OBSERVATIONS_COMPLETE.jsonl / RAW_INDEX_COMPLETE.jsonl /
  RUN_INDEX_COMPLETE.json / PAIRINGS.json — rebuilt indexes; the two
  base-package observations that existed only in measurements are
  restored as rejected captures from failure.json without promotion.
- source/src/camera_based_rgbww_optimizer/... — full import closure
  (50 modules incl. white_calibration_common, bounded_least_squares,
  p7_thermal_diagnostics, measure_raw_observer_validation, control and
  measurement layers, all measure_guide12_* entries); scripts/ holds the
  export scripts; config/ holds the frozen config inputs.
- results/original/<campaign>-derived/ — retained derived analysis
  inputs (w12/c122 candidate-proposal chains, evidence files) not
  byte-identical in the base package.
- MISSING_OR_UNIDENTIFIABLE.json / DEPENDENCY_STATUS.json — true states;
  no reconstruction of unrecorded data.
- replay/ — offline validation recomputing W12-2/N2/W12-4/colour/batch-1
  numbers from the base + completion packages only.

Raw CR3 payloads remain on D:/rgbww-optimizer (hash-referenced). No
device, camera or network access occurred during this export.
"""
    w("README.md", readme)

    # ---------- zip ----------
    manifest: list[dict] = []
    with zipfile.ZipFile(OUT_ZIP, "w", zipfile.ZIP_DEFLATED) as z:
        for p in sorted(STAGE.rglob("*")):
            if p.is_file():
                arc = p.relative_to(STAGE).as_posix()
                z.write(p, arc)
                manifest.append({"path": arc,
                                 "byte_count": p.stat().st_size,
                                 "sha256": sha_file(p)})
        man = {
            "schema": "guide12_evidence_completion_manifest_v1",
            "date": DATE,
            "file_count": len(manifest),
            "base_package_sha256": base_zip_sha,
            "excludes": ("raw CR3/RAW/DNG payloads, NPY, decoded arrays, "
                         "credentials, caches"),
            "files": manifest,
        }
        z.writestr("MANIFEST.json", json.dumps(man, indent=1))

    bad = None
    with zipfile.ZipFile(OUT_ZIP) as z:
        bad = z.testzip()
    zip_sha = sha_file(OUT_ZIP)
    (WORK / f"GUIDE12-EVIDENCE-COMPLETION-{DATE}-MANIFEST.json").write_text(
        json.dumps({"zip": str(OUT_ZIP), "zip_sha256": zip_sha,
                    "zip_byte_count": OUT_ZIP.stat().st_size,
                    "file_count": len(manifest)}, indent=1) + "\n",
        encoding="utf-8")
    n_runs = len(run_index_complete)
    print(f"zip: {OUT_ZIP.name} {OUT_ZIP.stat().st_size} bytes | files: "
          f"{len(manifest)} | integrity: {'FAIL:' + str(bad) if bad else 'ok'}")
    print(f"zip sha256: {zip_sha}")
    print(f"runs indexed: {n_runs} (base had {len(base_run_index)}) | "
          f"observations: {len(observations)} | raw rows: {len(raw_index)} | "
          f"pairing groups: {len(pairings)} | matrices: {len(matrices)}")
    print(f"phys-without-stats gaps: {len(stats_vs_phys_gaps)} | "
          f"copied files: {len(copy_map)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
