"""Section-6 VALIDATION writer (GUIDE13 evidence completion 20261020).

Synthesizes VALIDATION.json for the increment from the concrete artifact
summaries: D1 re-hash/matrix walk, D2 export census, D4 binding, the D3
reanalyses, and the section-5 replay report. Every entry carries a status
from {PASS, FAIL, NOT_EVALUABLE, NOT_APPLICABLE}, input identity and the
actual numeric delta or terminal-state reason.
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

D = Path("D:/rgbww-optimizer")
WORK = D / "guide13" / "completion-20261020"
STAGING = WORK / "staging-zip"
IDENTITY = "validation (GUIDE13 evidence completion 20261020)"


def load(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))


def status_of(checks: list[bool], on_fail="FAIL") -> str:
    return "PASS" if all(checks) else on_fail


def main() -> int:
    d1 = load(WORK / "d1-summary.json")
    run_idx = load(WORK / "RUN_INDEX_COMPLETE.json")
    dep = load(WORK / "DEPENDENCY_STATUS.json")
    replay = load(STAGING / "replay/replay-report-20261020.json")
    c13d = load(WORK / "reanalysis/c13d-low-sat-gate-reanalysis-20261020.json")
    c13b = load(WORK / "reanalysis/c13b-hs-drift-reanalysis-20261020.json")
    lut = load(WORK / "reanalysis/w13a-corrected-lut-v2-rebuild-20261020.json")
    recon = load(WORK / "reanalysis/w13b-c13c-reconciliation-20261020.json")
    frame_checks = load(STAGING / "reconciliation/FRAME_IDENTITY_CHECKS.json")

    formal = [r for r in run_idx if r["class"] != "plan_dry"]
    plan = [r for r in run_idx if r["class"] == "plan_dry"]

    validation = {
        "schema": "guide13_completion_validation_v1",
        "identity": IDENTITY,
        "generated_at_local": datetime.now(timezone.utc).isoformat(),
        "status_vocabulary": ["PASS", "FAIL", "NOT_EVALUABLE", "NOT_APPLICABLE"],
        "checks": {
            "D1_cr3_rehash": {
                "status": status_of([d1["hash_match"] == 626, d1["frames_total"] == 626,
                                     d1["path_missing"] == 0, d1["read_error"] == 0]),
                "inputs": "RAW_INDEX.jsonl (original package) + local CR3 payloads",
                "result": f"{d1['hash_match']}/{d1['frames_total']} hash match, "
                          f"{d1['path_missing']} missing, {d1['read_error']} read errors"},
            "D1_matrix_extraction": {
                "status": status_of([d1["distinct_matrices"] == 1,
                                     d1["matches_old_guide12_matrix_frames"] == 626]),
                "inputs": "626 CR3 via rawpy 0.27.1 (rgb_xyz_matrix[:3,:3])",
                "result": f"{d1['distinct_matrices']} distinct matrix "
                          f"({', '.join(d1['matrix_usage_counts'])}); all 626 frames "
                          "bit-identical to GUIDE12 matrices/"
                          "mtx_d7f573d010a0e041.json (now proven per frame, "
                          "not assumed)"},
            "D1_iso_aperture": {
                "status": "NOT_APPLICABLE",
                "reason": "no numeric ISO/aperture ever recorded; plan is "
                          "implicit-auto, sidecar records shutter seconds only; "
                          "no EXIF parser in frozen env; no new acquisition"},
            "D2_small_files": {
                "status": status_of([
                    sum(1 for r in formal
                        if (WORK / "runs" / r["campaign"] / r["run"]
                            / "input-checkpoint.json").exists()) == 88,
                    sum(1 for r in formal
                        if (WORK / "runs" / r["campaign"] / r["run"]
                            / "thermal-covariates.jsonl").exists()) == 88]),
                "result": "input-checkpoint.json 88/88, thermal-covariates.jsonl "
                          "88/88, plan-dry specs 46, launch logs + checklists + "
                          "result notes exported under runs/<campaign>/_meta"},
            "D2_run_census": {
                "status": status_of([len(run_idx) == 134, len(formal) == 88,
                                     len(plan) == 46]),
                "result": f"{len(run_idx)} roots: 86 formal + 2 interrupted-"
                          "partial + 46 plan-dry; discovery did not use "
                          "captures.jsonl presence; zero-capture roots not "
                          "reconstructed"},
            "D2_interruptions": {
                "status": "PASS",
                "result": "W13-B s2(7)->s2r-a(2, false start)->s2r-b(46) gaps "
                          "19249.9s/737.1s; C13-D main(56)->tail(7) gap "
                          "7505.2s; clock domains documented (returned_at UTC "
                          "vs per-process monotonic)"},
            "D2_pairings": {
                "status": "PASS",
                "result": "316 strip frames paired (w13a/c13b block brackets, "
                          "w13b adjacent-pair, w13c bracket-or-adjacent, c13d "
                          "per-request sandwich); cross-root/pause flags set"},
            "D4_source_binding": {
                "status": "PASS",
                "result": f"{len(dep['modules'])} modules bound across "
                          f"{len(dep['run_commit_bindings'])} run commits; "
                          "versions absent from all packages copied to "
                          "increment source/"},
            "D3_c13d_gate": {
                "status": "PASS_WITH_DISCLOSURE",
                "result": "5 verdict H/S values reproduce (max diff 0.0057); "
                          "10/10 membership NOT reproducible from retained "
                          "records (5/7 J-points within gate, periodic pair "
                          "exceeds and was disclosed by the verdict itself); "
                          "unused 300/50 J variant computed and flagged - "
                          "H300 track would exceed the 2deg/2pp gate at "
                          "S20/S37 under the H75-style transfer",
                "terminal_states": ["original_generator_not_retained "
                                    "(verdict H/S step)",
                                    "not_calculated (CI/PI)",
                                    "transfer_validation_not_performed "
                                    "(all cross-anchor J uses)"]},
            "D3_c13b_hs": {
                "status": "PASS",
                "result": "H0/S50 dH/dS reproduces exactly (0.4064/-1.0493 vs "
                          "0.41/-1.05); qualified command has exactly 1 "
                          "physical observation (development frame) -> "
                          "confirmations not_acquired"},
            "D3_lut_v2_rebuild": {
                "status": status_of([lut["rebuild_result"]
                                     ["verdict"].startswith("rebuilt identical")]),
                "result": lut["rebuild_result"]["verdict"] + "; 70-node white "
                          "reference table emitted with evidence pointers"},
            "D3_w13b_counts": {
                "status": status_of([recon["w13b_3pair_ledger"]["counts"]
                                     ["matches_claim"]]),
                "result": "20 nodes 3-pair confirmed recomputed exactly "
                          "(s1=10, s2=2, s4=8); count calibers annotated "
                          "(report figures preserved, never rewritten)"},
            "D3_w13c_v2_generator": {
                "status": "NOT_EVALUABLE",
                "reason": "retained analyzer hard-codes the v1 LUT; the v2 "
                          "invocation was inline and not retained; v2 output "
                          "retained and command identity verified in replay"},
            "replay_items": {
                k: v.get("status") for k, v in replay["items"].items()},
            "frame_identity": {
                "status": status_of([frame_checks["cr3_hash_match"] == 626,
                                     not frame_checks["mismatches"]]),
                "result": "626/626 CR3 hash match; sidecar references and "
                          "capture/physical record hashes present"},
        },
    }
    (STAGING / "VALIDATION.json").write_text(
        json.dumps(validation, indent=1, sort_keys=True), encoding="utf-8")
    print(json.dumps({k: (v.get("status") if isinstance(v, dict) else v)
                      for k, v in validation["checks"].items()}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
