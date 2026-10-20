"""Section-6 packager (GUIDE13 evidence completion 20261020).

--stage : assemble staging-zip/ (all increment members except replay/ and
          VALIDATION.json, which the replay step adds), including the
          locally-derived equivalents of the request's attachment indexes
          and the MISSING register.
--zip   : after replay, write the final zip, external MANIFEST (no self-hash
          inside), external VALIDATION (with post-build CRC + roundtrip),
          and print the SHA-256.

Exclusion rules (deliberate, same policy as the original package): no CR3/
RAW payloads, no NPY, no decoded arrays, no caches, no credentials, no
re-zipped base packages (referenced by SHA-256 only).
"""
from __future__ import annotations

import hashlib
import json
import shutil
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path

D = Path("D:/rgbww-optimizer")
WORK = D / "guide13" / "completion-20261020"
STAGING = WORK / "staging-zip"
PKG13 = D / "guide13/package/GUIDE13-COMPLETE-PROCESSED-EVIDENCE-20261019.zip"
REPO = Path(__file__).resolve().parents[1]
DATE = "20261020"
ZIP_PATH = D / "guide13" / "package" / f"GUIDE13-EVIDENCE-COMPLETION-{DATE}.zip"
IDENTITY = "reanalysis/export (GUIDE13 evidence completion 20261020)"
EXCLUDE_SUFFIXES = (".cr3", ".npy", ".npz", ".zip")
BASE_PACKAGES = {
    "GUIDE13-COMPLETE-PROCESSED-EVIDENCE-20261019.zip": {
        "sha256": "919ef2ad47dd1b919190526fefc4fb570a7e743c13b9672684ba885e49fe3ab3",
        "bytes": 26045475, "members": 2158,
        "local_path": str(PKG13), "role": "original GUIDE13 package"},
    "GUIDE12-COMPLETE-PROCESSED-EVIDENCE-20261012.zip": {
        "sha256": "3ed20b169cb2cc60470702a05c0e0bfb96f38aa24010b7948e664d271f53d500",
        "bytes": 37300305, "members": 1115,
        "local_path": "C:/Users/iBobb/Projects/WLED-RGBWW/.agent-work/guide12/"
                      "GUIDE12-COMPLETE-PROCESSED-EVIDENCE-20261012.zip",
        "role": "base package"},
    "GUIDE12-EVIDENCE-COMPLETION-20261012.zip": {
        "sha256": "85a61c4ee3a46c28f5922804dcd3f69590c82069477f1f9ad8924627cb52b4bc",
        "bytes": 15417622, "members": 4999,
        "local_path": "C:/Users/iBobb/Projects/WLED-RGBWW/.agent-work/guide12/"
                      "GUIDE12-EVIDENCE-COMPLETION-20261012.zip",
        "role": "base package"},
}
BUILDERS = [
    "tmp/build_guide13_package_20261019.py",
    "tmp/d1_extract_matrices_20261020.py",
    "tmp/d2_collect_run_smallfiles_20261020.py",
    "tmp/d4_bind_sources_20261020.py",
    "tmp/reanalysis_c13d_low_sat_gate_20261020.py",
    "tmp/reanalysis_c13b_hs_drift_20261020.py",
    "tmp/rebuild_w13a_lut_v2_20261020.py",
    "tmp/reconcile_w13b_c13c_20261020.py",
    "tmp/replay_guide13_completion_20261020.py",
    "tmp/build_guide13_completion_package_20261020.py",
]


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def jsonl(p: Path) -> list[dict]:
    return [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines()
            if l.strip()]


def collect_tree(src: Path, dst: Path):
    if not src.exists():
        return 0
    n = 0
    for p in sorted(src.rglob("*")):
        if p.is_file() and p.suffix.lower() not in EXCLUDE_SUFFIXES:
            rel = p.relative_to(src)
            (dst / rel).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(p, dst / rel)
            n += 1
    return n


def stage() -> int:
    if STAGING.exists():
        shutil.rmtree(STAGING)
    STAGING.mkdir(parents=True)

    # top-level documents
    (STAGING / "BASE_PACKAGES.json").write_text(
        json.dumps(BASE_PACKAGES, indent=1, sort_keys=True), encoding="utf-8")
    (STAGING / "README.md").write_text(
        "# GUIDE13 evidence completion increment 20261020\n\n"
        "Offline-only increment over the original GUIDE13 package: per-frame\n"
        "matrix extraction and CR3 re-hash (626/626 match, single matrix\n"
        "mtx_d7f573d010a0e041 verified per frame), missing run small files\n"
        "(input-checkpoint.json, thermal-covariates.jsonl) for all 88 capture\n"
        "roots plus 46 plan-dry roots and launch/meta logs, interruption\n"
        "narratives (W13-B s2 chain, C13-D main/tail), complete pairings,\n"
        "layered quality with actual PWM readback, source version binding for\n"
        "the 88 runs (39 modules; versions absent from every package copied\n"
        "under source/), provenance reanalysis for the C13-D low-SAT gate,\n"
        "C13-B H/S estimates, corrected LUT v2 (rebuilt identical), W13-B\n"
        "3-pair ledger and C13-C fathers, and a self-contained replay.\n\n"
        "Nothing here re-runs a device, camera or network call; original\n"
        "results are never overwritten. Terminal states for items that cannot\n"
        "be recovered are recorded in MISSING_OR_UNIDENTIFIABLE.json.\n\n"
        "Exclusions: CR3/RAW payloads, NPY, decoded arrays, caches,\n"
        "credentials, re-copied base packages (SHA references only).\n",
        encoding="utf-8")

    # D1/D2/D4 outputs
    for name in ("RAW_INDEX_COMPLETE.jsonl", "RUN_INDEX_COMPLETE.json",
                 "PAIRINGS_COMPLETE.json", "PRIMARY_SECONDARY_QUALITY.jsonl",
                 "INTERRUPTIONS.json", "DEPENDENCY_STATUS.json"):
        shutil.copy2(WORK / name, STAGING / name)
    collect_tree(WORK / "matrices", STAGING / "matrices")
    collect_tree(WORK / "runs", STAGING / "runs")
    collect_tree(WORK / "source", STAGING / "source")
    collect_tree(WORK / "reanalysis", STAGING / "reanalysis")

    # builders + exclusion rules travel with the package
    for rel in BUILDERS:
        p = REPO / rel
        if p.exists():
            dst = STAGING / "source" / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(p, dst)

    # advisor-attachment equivalents (locally derived; originals not on disk)
    rec = STAGING / "reconciliation"
    rec.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(PKG13) as zf:
        members = []
        for info in zf.infolist():
            if not info.is_dir():
                data = zf.read(info.filename)
                members.append({"path": info.filename,
                                "byte_count": len(data),
                                "sha256": sha256_bytes(data)})
        (rec / "GUIDE13_MEMBER_INDEX.jsonl").write_text(
            "\n".join(json.dumps(m, sort_keys=True) for m in members) + "\n",
            encoding="utf-8")
        (rec / "RUN_INDEX_RECEIVED.json").write_bytes(zf.read("RUN_INDEX.json"))
        pkg_raw = jsonl_workaround = [json.loads(l) for l in
                                      zf.read("RAW_INDEX.jsonl").decode().splitlines()
                                      if l.strip()]
    raw_complete = jsonl(WORK / "RAW_INDEX_COMPLETE.jsonl")
    by_key = {(r["campaign"], r["run"], str(r["capture_id"])): r
              for r in raw_complete}
    frame_checks = {
        "schema": "guide13_completion_frame_identity_v1",
        "identity": IDENTITY,
        "derivation": "cross-check of original package RAW_INDEX vs the D1 "
                      "re-hash walk over local CR3 payloads",
        "frames": len(pkg_raw),
        "cr3_hash_match": sum(1 for r in raw_complete if r.get("hash_match")),
        "sidecar_sha_referenced": sum(
            1 for r in pkg_raw if r.get("sidecar_sha256")),
        "capture_record_hash_present": sum(
            1 for r in raw_complete if r.get("capture_record_sha256")),
        "physical_return_record_hash_present": sum(
            1 for r in raw_complete if r.get("physical_return_record_sha256")),
        "matrix_ids": sorted({r.get("matrix", {}).get("matrix_id")
                              for r in raw_complete}),
        "mismatches": [f"{r['campaign']}/{r['run']}/{r['capture_id']}"
                       for r in raw_complete if not r.get("hash_match")],
        "note": "advisor-side three-way capture/physical/statistics identity "
                "was verified on the received package; this file adds the "
                "local CR3 byte re-hash result per frame",
    }
    (rec / "FRAME_IDENTITY_CHECKS.json").write_text(
        json.dumps(frame_checks, indent=1, sort_keys=True), encoding="utf-8")

    # resolved hashed inputs across all 134 specs
    resolved: dict[str, dict] = {}
    run_idx = json.loads((WORK / "RUN_INDEX_COMPLETE.json").read_text(encoding="utf-8"))
    for r in run_idx:
        spec = D / r["campaign"] / r["run"] / "experiment-spec.json"
        if not spec.exists():
            continue
        doc = json.loads(spec.read_text(encoding="utf-8"))

        def walk(o):
            if isinstance(o, dict):
                if "sha256" in o and "path" in o:
                    key = str(o["path"])
                    resolved.setdefault(key, {
                        "sha256": str(o["sha256"]),
                        "referenced_by": [],
                        "byte_count": o.get("byte_count")})
                    resolved[key]["referenced_by"].append(
                        f"{r['campaign']}/{r['run']}")
                for v in o.values():
                    walk(v)
            elif isinstance(o, list):
                for v in o:
                    walk(v)
        walk(doc)
    for key, entry in resolved.items():
        p = Path(key)
        entry["exists_locally"] = p.exists()
        entry["local_sha_matches"] = (p.exists() and p.is_file()
                                      and sha256_file(p) == entry["sha256"])
        entry["referenced_by_count"] = len(entry["referenced_by"])
        entry["referenced_by"] = entry["referenced_by"][:3] + (
            ["..."] if len(entry["referenced_by"]) > 3 else [])
    (rec / "RESOLVED_HASHED_INPUTS.json").write_text(
        json.dumps({"schema": "guide13_completion_resolved_inputs_v1",
                    "identity": IDENTITY,
                    "distinct_inputs": len(resolved),
                    "inputs": resolved}, indent=1, sort_keys=True),
        encoding="utf-8")

    dep = json.loads((WORK / "DEPENDENCY_STATUS.json").read_text(encoding="utf-8"))
    cands = {rel: {
        "single_version_across_all_runs": v["single_version_across_all_runs"],
        "current_worktree_sha256": v["current_worktree_sha256"],
        "byte_identical_members": next(
            (c["byte_identical_members"] for c in v["used_by_run_commits"].values()
             if c.get("byte_identical_members")), []),
        "versions_added_to_increment": v.get("versions_added_to_increment", []),
    } for rel, v in dep["modules"].items()}
    (rec / "SOURCE_DEPENDENCY_CANDIDATES.json").write_text(
        json.dumps({"schema": "guide13_completion_source_candidates_v1",
                    "identity": IDENTITY,
                    "derivation": "transitive import closure of the original "
                                  "package source files plus the named direct "
                                  "dependencies; versions resolved per run "
                                  "commit via git",
                    "modules": cands}, indent=1, sort_keys=True),
        encoding="utf-8")

    missing = {
        "schema": "guide13_completion_missing_v1",
        "identity": IDENTITY,
        "items": {
            "failure.json/wrapper-result.json/all-off-shell.json": {
                "state": "not_created_by_runtime",
                "evidence": "searched all 134 local GUIDE13 roots; the GUIDE13 "
                            "runner writes all-off-python.json and "
                            "isolation-gates.jsonl but never these three file "
                            "types (they belong to the foundations-era wrapper "
                            "runs); the two interrupted roots' cleanup evidence "
                            "is the manual all_off recorded in pause-note "
                            "commit messages 0e71f6c/914da9d"},
            "iso_aperture_numeric": {
                "state": "not_recorded",
                "evidence": "plan exposure is implicit-auto; bridge sidecars "
                            "record shutter seconds only; no EXIF parser in the "
                            "frozen environment and no new acquisition "
                            "permitted"},
            "historical_temperature_power_supply": {
                "state": "not_recorded",
                "evidence": "unchanged from prior terminal states; thermal-"
                            "covariates.jsonl now exported provides load-history "
                            "proxies per frame, never converted to temperature"},
            "c13d_verdict_hs_inversion_generator": {
                "state": "original_generator_not_retained",
                "evidence": "recomputed in reanalysis/c13d-low-sat-gate-"
                            "reanalysis-20261020.json; 5 verdict values "
                            "reproduce, 10/10 membership does not"},
            "w13a_corrected_lut_v2_generator": {
                "state": "original_generator_not_retained",
                "evidence": "rebuilt identical 70/70 in reanalysis/w13a-"
                            "corrected-lut-v2-rebuild-20261020.json"},
            "w13c_v2_regression_invocation": {
                "state": "original_generator_not_retained",
                "evidence": "retained analyzer hard-codes the v1 LUT; v2 output "
                            "retained and command identity checked in replay"},
            "c13b_block_analysis_outputs": {
                "state": "original_generator_not_retained",
                "evidence": "analyzer retained, invocations inline; measured dz "
                            "recomputed in reanalysis/c13b-hs-drift-"
                            "reanalysis-20261020.json"},
            "request_attachment_index_files": {
                "state": "lost_after_documented_search",
                "evidence": "GUIDE13_MEMBER_INDEX.jsonl / RUN_INDEX_RECEIVED / "
                            "FRAME_IDENTITY_CHECKS / RESOLVED_HASHED_INPUTS / "
                            "SOURCE_DEPENDENCY_CANDIDATES were not found on this "
                            "machine (searched project, Downloads, D:); locally "
                            "derived equivalents provided under reconciliation/"},
            "h0_s50_command_confirmations": {
                "state": "not_acquired",
                "evidence": "exactly one physical observation of the qualified "
                            "command exists (development selection frame "
                            "formal-c13b-h0-s50-b3); the node state itself "
                            "queues 3 confirmations"},
            "w13a_report_236_frame_denominator": {
                "state": "not_recorded",
                "evidence": "report figure is approximate; ledger facts "
                            "(308/296/180) recorded with calibers in "
                            "reconciliation; report not rewritten"},
            "w13c_20_new_holdouts": {
                "state": "deferred_by_protocol",
                "evidence": "unchanged from original package terminal state"},
            "raw_cr3_payloads": {
                "state": "excluded_by_policy",
                "evidence": "referenced by hash; all 626 locally re-hashed "
                            "with 100% match (RAW_INDEX_COMPLETE.jsonl)"},
        },
    }
    (STAGING / "MISSING_OR_UNIDENTIFIABLE.json").write_text(
        json.dumps(missing, indent=1, sort_keys=True), encoding="utf-8")

    # MANIFEST without self-hash (zip not built yet)
    members = []
    for p in sorted(STAGING.rglob("*")):
        if p.is_file():
            data = p.read_bytes()
            members.append({"path": p.relative_to(STAGING).as_posix(),
                            "byte_count": len(data),
                            "sha256": sha256_bytes(data)})
    (STAGING / "MANIFEST.json").write_text(
        json.dumps({"schema": "guide13_completion_manifest_v1",
                    "identity": IDENTITY,
                    "generated_at_local": datetime.now(timezone.utc).isoformat(),
                    "note": "member index of this increment; the zip-level "
                            "SHA-256 lives in the external manifest beside the "
                            "zip (this file cannot contain its own container "
                            "hash)",
                    "members": members}, indent=1, sort_keys=True),
        encoding="utf-8")
    print(f"staged members (pre-replay): {len(members)}")
    return 0


def build_zip() -> int:
    replay_report = STAGING / "replay/replay-report-20261020.json"
    if not replay_report.exists():
        raise SystemExit("replay report missing; run the replay first")
    if not (STAGING / "VALIDATION.json").exists():
        raise SystemExit("VALIDATION.json missing; run write_validation first")
    # refresh member manifest so replay/ and VALIDATION.json are included
    members = []
    for p in sorted(STAGING.rglob("*")):
        if p.is_file():
            data = p.read_bytes()
            members.append({"path": p.relative_to(STAGING).as_posix(),
                            "byte_count": len(data),
                            "sha256": sha256_bytes(data)})
    (STAGING / "MANIFEST.json").write_text(
        json.dumps({"schema": "guide13_completion_manifest_v1",
                    "identity": IDENTITY,
                    "generated_at_local": datetime.now(timezone.utc).isoformat(),
                    "note": "member index of this increment; the zip-level "
                            "SHA-256 lives in the external manifest beside the "
                            "zip (this file cannot contain its own container "
                            "hash)",
                    "members": members}, indent=1, sort_keys=True),
        encoding="utf-8")
    with zipfile.ZipFile(ZIP_PATH, "w", zipfile.ZIP_DEFLATED) as zf:
        for p in sorted(STAGING.rglob("*")):
            if p.is_file():
                zf.write(p, p.relative_to(STAGING).as_posix())
    zip_sha = sha256_file(ZIP_PATH)
    # CRC + roundtrip
    with zipfile.ZipFile(ZIP_PATH) as zf:
        bad = zf.testzip()
        names = zf.namelist()
        sample = json.loads(zf.read("replay/replay-report-20261020.json"))
    manifest = {
        "schema": "guide13_completion_package_manifest_v1",
        "created_at_local": datetime.now(timezone.utc).isoformat(),
        "zip": {"path": str(ZIP_PATH), "byte_count": ZIP_PATH.stat().st_size,
                "sha256": zip_sha, "members": len(names)},
        "crc_test": "PASS" if bad is None else f"FAIL: {bad}",
        "roundtrip_replay_report_read": bool(sample),
        "base_packages": BASE_PACKAGES,
        "companion_files": [
            "GUIDE13-EVIDENCE-COMPLETION-20261020-MANIFEST.json (this file)",
            "GUIDE13-EVIDENCE-COMPLETION-20261020-VALIDATION.json",
            "GUIDE13-EVIDENCE-COMPLETION-20261020-EXPORT-RESULT.md",
        ],
    }
    (ZIP_PATH.parent / f"GUIDE13-EVIDENCE-COMPLETION-{DATE}-MANIFEST.json").write_text(
        json.dumps(manifest, indent=1, sort_keys=True), encoding="utf-8")
    print(json.dumps({"zip": str(ZIP_PATH), "bytes": ZIP_PATH.stat().st_size,
                      "sha256": zip_sha, "members": len(names),
                      "crc": manifest["crc_test"]}))
    return 0


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--stage":
        sys.exit(stage())
    if len(sys.argv) > 1 and sys.argv[1] == "--zip":
        sys.exit(build_zip())
    print("usage: build_guide13_completion_package_20261020.py --stage|--zip")
    sys.exit(2)
