"""D2 (GUIDE13 evidence completion 20261020): run small-file export + indexes.

Offline, read-only over local GUIDE13 campaign directories:
- copy the small run files the original package builder's whitelist missed
  (input-checkpoint.json, thermal-covariates.jsonl) for all 88 capture roots,
  the 46 dry-run plan roots' experiment-spec.json, launch logs, pre-run
  checklists and campaign result notes,
- RUN_INDEX_COMPLETE.json: full census (formal / interrupted-partial /
  plan-dry) with git binding, UTC boundaries and original-package coverage,
- INTERRUPTIONS.json: W13-B s2 -> s2r-a -> s2r-b and C13-D main -> tail
  narratives from ledger evidence (UTC gaps, covered requests, clock domains),
- PAIRINGS_COMPLETE.json: the strip-vs-Ray pairing actually used, per
  campaign, with cross-root / pause-crossing flags,
- PRIMARY_SECONDARY_QUALITY.jsonl: per-frame primary / secondary58 /
  fullscale layers with commanded vs applied+readback PWM and the frozen
  code-duty conversion identity.

New files carry an explicit reanalysis/export identity; original results are
never overwritten.
"""
from __future__ import annotations

import hashlib
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from camera_based_rgbww_optimizer.optimization import guide13  # noqa: E402
from camera_based_rgbww_optimizer.optimization import (  # noqa: E402
    p7_thermal_diagnostics as thermal,
)

D = Path("D:/rgbww-optimizer")
REPO = Path(__file__).resolve().parents[1]
WORK = D / "guide13" / "completion-20261020"
IDENTITY = "reanalysis/export (GUIDE13 evidence completion 20261020)"
CAMPAIGNS = ["guide13-w13a", "guide13-w13b", "guide13-w13c",
             "guide13-c13a", "guide13-c13b", "guide13-c13d"]
RUN_CLASSES = {
    "formal-w13b-s2": "formal_partial_interrupted",
    "formal-c13d-holdout": "formal_partial_interrupted",
}


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def jsonl(path: Path) -> list[dict]:
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines()
            if l.strip()]


def main() -> int:
    curve_path = REPO / "config/channel/code-duty-curve.json"
    curve_sha = sha256_file(curve_path)
    curve = json.loads(curve_path.read_text(encoding="utf-8"))

    pkg_runs = {(r["campaign"], r["run"]) for r in json.loads(
        (WORK / "original-RUN_INDEX.json").read_text(encoding="utf-8"))}

    run_index: list[dict] = []
    copied = 0
    for camp in CAMPAIGNS:
        cdir = D / camp
        # --- per-root small files ---
        for entry in sorted(cdir.iterdir()):
            if not entry.is_dir() or entry.name == "derived":
                continue
            is_plan = (entry / "captures.jsonl").exists() is False
            rel = f"runs/{camp}/{entry.name}"
            for name in (("input-checkpoint.json", "thermal-covariates.jsonl")
                         if not is_plan else ("experiment-spec.json",)):
                src = entry / name
                if src.exists():
                    dst = WORK / rel / name
                    dst.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(src, dst)
                    copied += 1
            caps = jsonl(entry / "captures.jsonl") if not is_plan else []
            prs = jsonl(entry / "physical-returns.jsonl") if not is_plan else []
            status = None
            if (entry / "run.json").exists():
                status = json.loads(
                    (entry / "run.json").read_text(encoding="utf-8")).get("status")
            commit = None
            ckpt = entry / "input-checkpoint.json"
            if ckpt.exists():
                commit = json.loads(
                    ckpt.read_text(encoding="utf-8")).get("git", {}).get("commit")
            times = sorted(str(p.get("returned_at")) for p in prs if p.get("returned_at"))
            run_index.append({
                "campaign": camp, "run": entry.name,
                "class": ("plan_dry" if is_plan
                          else RUN_CLASSES.get(entry.name, "formal")),
                "captures": len(caps), "physical_returns": len(prs),
                "run_json_status": status,
                "git_commit_at_launch": commit,
                "first_return_utc": times[0] if times else None,
                "last_return_utc": times[-1] if times else None,
                "in_original_package": (camp, entry.name) in pkg_runs,
                "new_files_exported": (
                    ["input-checkpoint.json", "thermal-covariates.jsonl"]
                    if not is_plan else ["experiment-spec.json"]),
            })
        # --- campaign meta siblings (launch logs, checklists, result notes) ---
        meta = WORK / f"runs/{camp}/_meta"
        meta.mkdir(parents=True, exist_ok=True)
        for p in sorted(cdir.iterdir()):
            if p.is_file() and (p.suffix in (".log", ".md")
                                or p.name.endswith(".json")) and p.name != "REORG-MAP-20260929.json":
                shutil.copy2(p, meta / p.name)
                copied += 1

    (WORK / "RUN_INDEX_COMPLETE.json").write_text(
        json.dumps(run_index, indent=1, sort_keys=True), encoding="utf-8")
    summary_counts = {
        "roots_total": len(run_index),
        "formal": sum(1 for r in run_index if r["class"] == "formal"),
        "formal_partial_interrupted": sum(
            1 for r in run_index if r["class"] == "formal_partial_interrupted"),
        "plan_dry": sum(1 for r in run_index if r["class"] == "plan_dry"),
        "in_original_package": sum(1 for r in run_index if r["in_original_package"]),
        "files_copied": copied,
    }
    print("run index:", json.dumps(summary_counts))

    # ---------------- interruption narratives ----------------
    def root_timeline(camp: str, run: str) -> dict:
        root = D / camp / run
        caps = jsonl(root / "captures.jsonl")
        prs = jsonl(root / "physical-returns.jsonl")
        pr_by_cid = {str(p["capture_id"]): p for p in prs}
        reqs = {}
        for row in caps:
            s = row["plan_step"]
            req = (s.get("w13b_node") or s.get("c13d_request")
                   or s.get("candidate_tag") or s.get("state_id"))
            reqs.setdefault(str(req), []).append({
                "capture_id": str(s["capture_id"]),
                "source": s.get("source_id"),
                "role": s.get("role") or s.get("ray_reference_position") or "",
                "returned_at": pr_by_cid.get(str(s["capture_id"]), {}).get("returned_at"),
            })
        times = sorted(str(p["returned_at"]) for p in prs if p.get("returned_at"))
        return {
            "campaign": camp, "run": run,
            "captures": len(caps), "physical_returns": len(prs),
            "run_json_status": json.loads(
                (root / "run.json").read_text(encoding="utf-8")).get("status"),
            "requests_covered": {k: v for k, v in sorted(reqs.items())},
            "first_return_utc": times[0] if times else None,
            "last_return_utc": times[-1] if times else None,
        }

    def utc_gap(a: str | None, b: str | None) -> float | None:
        if not a or not b:
            return None
        ta = datetime.fromisoformat(a).timestamp()
        tb = datetime.fromisoformat(b).timestamp()
        return round(tb - ta, 1)

    w13b_chain = [root_timeline("guide13-w13b", r) for r in
                  ("formal-w13b-s2", "formal-w13b-s2r-a", "formal-w13b-s2r-b",
                   "formal-w13b-s3")]
    c13d_chain = [root_timeline("guide13-c13d", r) for r in
                  ("formal-c13d-holdout", "formal-c13d-holdout-tail")]
    for chain in (w13b_chain, c13d_chain):
        for i in range(1, len(chain)):
            chain[i]["utc_gap_from_previous_root_s"] = utc_gap(
                chain[i - 1]["last_return_utc"], chain[i]["first_return_utc"])
    interruptions = {
        "schema": "guide13_completion_interruptions_v1",
        "identity": IDENTITY,
        "w13b_s2_pause_resume": {
            "chain": w13b_chain,
            "pause_record": {
                "file": ".agent-work/guide13/pause-note-20261017.json "
                        "(git 0e71f6c, also in original package "
                        "results/guide13-w13b/pause-note-20261017.json)",
            },
            "clock_domains": (
                "physical-returns returned_at is bridge UTC (isoformat); "
                "thermal-covariates monotonic_timestamp_ns and captures "
                "source_on_monotonic_s are per-process monotonic clocks and are "
                "NOT valid absolute time across processes/roots; cross-root "
                "ordering and gaps in this file use returned_at UTC only"),
            "resume_semantics": (
                "s2 preserved as partial root (7 physical returns, run.json "
                "status=running retained as historical identity); s2r-a and "
                "s2r-b are fresh roots; the s2-combined analyzer "
                "(tmp/analyze_w13b_s2_combined_20261018.py, in original "
                "package) defines which frames each confirmation used"),
        },
        "c13d_main_tail": {
            "chain": c13d_chain,
            "pause_record": {
                "file": ".agent-work/guide13/pause-note-20261019.json "
                        "(git 914da9d, also in original package "
                        "results/guide13-c13d/pause-note-20261019.json)",
            },
            "clock_domains": "same rule as W13-B above",
            "resume_semantics": (
                "main root preserved at 56/63 frames (status=running retained); "
                "tail root re-ran the 7 remaining requests only; each request's "
                "Ray sandwich lives wholly inside the root that measured its "
                "strip frame (no request spans both roots)"),
        },
    }
    (WORK / "INTERRUPTIONS.json").write_text(
        json.dumps(interruptions, indent=1, sort_keys=True), encoding="utf-8")
    print("interruptions:",
          json.dumps({c["run"]: [c["captures"], c.get("utc_gap_from_previous_root_s")]
                      for chain in (w13b_chain, c13d_chain) for c in chain}))

    # ---------------- pairings ----------------
    pairings: list[dict] = []
    for camp in CAMPAIGNS:
        for r in run_index:
            if r["campaign"] != camp or r["class"] == "plan_dry":
                continue
            root = D / camp / r["run"]
            caps = jsonl(root / "captures.jsonl")
            steps = [row["plan_step"] for row in caps]
            if camp in ("guide13-w13a", "guide13-c13b"):
                before = next((s for s in steps
                               if s.get("ray_reference_position") == "raybefore"), None)
                after = next((s for s in steps
                              if s.get("ray_reference_position") == "rayafter"), None)
                for s in steps:
                    if s.get("source_id") == "strip":
                        pairings.append({
                            "campaign": camp, "run": r["run"],
                            "capture_id": str(s["capture_id"]),
                            "role": str(s.get("candidate_tag")),
                            "reference_capture_ids": [
                                str(before["capture_id"]) if before else None,
                                str(after["capture_id"]) if after else None],
                            "pairing_rule": "block ray_before/ray_after per-component mean",
                            "weights": [0.5, 0.5],
                            "cross_root": False, "pause_crossing": False,
                            "analysis_owner": "tmp/analyze_w12_block_20260930.py "
                                              "(reused, in original package source/)",
                        })
            elif camp == "guide13-w13b":
                by_node: dict[str, dict] = {}
                for s in steps:
                    key = f"{s.get('w13b_node')}/p{s.get('w13b_pair_ordinal')}"
                    by_node.setdefault(key, {})[str(s.get("source_id"))] = s
                for key, pair in sorted(by_node.items()):
                    ray, strip = pair.get("ray"), pair.get("strip")
                    if ray and strip:
                        pairings.append({
                            "campaign": camp, "run": r["run"],
                            "capture_id": str(strip["capture_id"]),
                            "role": f"{key} strip confirmation",
                            "reference_capture_ids": [str(ray["capture_id"])],
                            "pairing_rule": "adjacent same-node same-ordinal Ray frame",
                            "weights": [1.0],
                            "cross_root": False,
                            "pause_crossing": r["class"] == "formal_partial_interrupted",
                            "analysis_owner": "tmp/analyze_w13b_s1_20261017.py / "
                                              "tmp/analyze_w13b_s2_combined_20261018.py",
                        })
            elif camp == "guide13-w13c":
                seq = list(steps)
                for i, s in enumerate(seq):
                    if s.get("source_id") == "strip":
                        prev = seq[i - 1] if i > 0 else None
                        nxt = seq[i + 1] if i + 1 < len(seq) else None
                        refs = []
                        if prev and prev.get("source_id") == "ray":
                            refs.append(str(prev["capture_id"]))
                        if nxt and nxt.get("source_id") == "ray":
                            refs.append(str(nxt["capture_id"]))
                        pairings.append({
                            "campaign": camp, "run": r["run"],
                            "capture_id": str(s["capture_id"]),
                            "role": str(s.get("state_id", ""))[:60],
                            "reference_capture_ids": refs,
                            "pairing_rule": ("bracket mean when before/after sandwich "
                                             "present, else adjacent Ray frame"),
                            "weights": [1.0 / len(refs)] * len(refs) if refs else [],
                            "cross_root": False, "pause_crossing": False,
                            "analysis_owner": "tmp/analyze_w13c_dev_20261013.py",
                        })
            elif camp == "guide13-c13d":
                by_req: dict[str, dict] = {}
                for s in steps:
                    by_req.setdefault(str(s.get("c13d_request")), {})[
                        str(s.get("c13d_position"))] = s
                for req, group in sorted(by_req.items()):
                    strip = group.get("strip")
                    if not strip:
                        continue
                    refs = [str(g["capture_id"]) for pos, g in sorted(group.items())
                            if pos.startswith("ray")]
                    pairings.append({
                        "campaign": camp, "run": r["run"],
                        "capture_id": str(strip["capture_id"]),
                        "role": f"c13d {req}",
                        "reference_capture_ids": refs,
                        "pairing_rule": "per-request Ray sandwich mean (bracket)",
                        "weights": [1.0 / len(refs)] * len(refs) if refs else [],
                        "cross_root": False,
                        "pause_crossing": r["run"] == "formal-c13d-holdout",
                        "analysis_owner": "tmp/analyze_c13d_holdout_20261019.py",
                    })
    (WORK / "PAIRINGS_COMPLETE.json").write_text(
        json.dumps(pairings, indent=1, sort_keys=True), encoding="utf-8")
    print("pairings rows:", len(pairings))

    # ---------------- layered quality + actual PWM ----------------
    out = (WORK / "PRIMARY_SECONDARY_QUALITY.jsonl").open("w", encoding="utf-8")
    counts = {"frames": 0, "primary_accepted": 0, "secondary58_rejected": 0,
              "fullscale_rows": 0}
    for camp in CAMPAIGNS:
        for r in run_index:
            if r["campaign"] != camp or r["class"] == "plan_dry":
                continue
            root = D / camp / r["run"]
            caps = jsonl(root / "captures.jsonl")
            cmds = {c.get("exact_command_hash"): c
                    for c in jsonl(root / "commands.jsonl")}
            for row in caps:
                s = row["plan_step"]
                cid = str(s["capture_id"])
                stats_path = root / "measurements" / f"{cid}.patch-statistics.json"
                primary = None
                if stats_path.exists():
                    primary = guide13.primary_layer_from_stats(
                        json.loads(stats_path.read_text(encoding="utf-8")))
                secondary = guide13.secondary58_from_capture(row)
                fullscale = None
                cmd_row = cmds.get(s.get("exact_command_hash"))
                if cmd_row is not None and s.get("source_id") == "strip":
                    try:
                        fullscale = guide13.fullscale_from_command(cmd_row)
                    except Exception as exc:
                        fullscale = {"status": "error", "error": repr(exc)[:200]}
                duty = None
                if s.get("source_id") == "strip" and isinstance(s.get("command"), dict):
                    duty = {k: round(float(v), 6) for k, v in
                            thermal.strip_duty(dict(s["command"]), curve).items()}
                counts["frames"] += 1
                if primary and primary.get("primary_quality") == "accepted":
                    counts["primary_accepted"] += 1
                if secondary is not None:
                    counts["secondary58_rejected"] += 1
                if fullscale is not None:
                    counts["fullscale_rows"] += 1
                out.write(json.dumps({
                    "campaign": camp, "run": r["run"], "capture_id": cid,
                    "source": s.get("source_id"),
                    "identity": IDENTITY,
                    "primary_layer": primary,
                    "secondary58_gate": secondary,
                    "fullscale_layer": fullscale,
                    "commanded_pwm": s.get("command"),
                    "command_ledger": ({
                        "applied": cmd_row.get("applied"),
                        "readback": cmd_row.get("readback"),
                        "at_utc": cmd_row.get("at"),
                    } if cmd_row is not None else None),
                    "code_duty_conversion": ({
                        "curve_sha256": curve_sha,
                        "curve_path": "config/channel/code-duty-curve.json",
                        "strip_duty": duty,
                    } if duty is not None else None),
                }, sort_keys=True, default=str) + "\n")
    out.close()
    print("quality rows:", json.dumps(counts))
    print("code-duty curve sha:", curve_sha)
    return 0


if __name__ == "__main__":
    sys.exit(main())
