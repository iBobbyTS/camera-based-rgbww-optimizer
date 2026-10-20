"""D3.2 reanalysis (GUIDE13 evidence completion 20261020): C13-B provenance.

Recomputes, from retained run frames and the C13-A Jacobians:
- the H/S estimate behind the H0/S50 qualification (node state reports
  dH=0.41deg dS=-1.05pp for cw132/ww1968/r4095/g180/b480): formula
  (dH,dS) = J(0/50)^-1 * dz_best via guide13.solve_local_delta,
- per-block measured dz for H300/S50 and H0/S50 (J-theory direction
  conclusions) with the candidate tags/commands from the retained
  candidates JSONs,
- source-level Ray bracket z values for the reference_drifted S100 targets
  (H0/H120/H300) as recorded in this campaign's own blocks,
- every physical observation of the H0/S50 qualified command across all
  local GUIDE12/GUIDE13 run roots, with roles (development selection vs
  confirmation).

Node states, candidates JSONs and the campaign summary are compared against,
never overwritten. Inline computations whose generator was not retained are
marked as such.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from camera_based_rgbww_optimizer.optimization import guide13  # noqa: E402

D = Path("D:/rgbww-optimizer")
WORK = D / "guide13" / "completion-20261020"
IDENTITY = "reanalysis (GUIDE13 evidence completion 20261020)"
C13B = D / "guide13-c13b"
J_FILE = D / "guide13-c13a/derived/c13a-local-jacobian-20261013.json"
QUALIFIED_CMD = {"cw": 132, "ww": 1968, "r": 4095, "g": 180, "b": 480}
SEARCH_CAMPAIGNS = sorted(
    p.name for p in D.iterdir()
    if p.is_dir() and (p.name.startswith("guide13")
                       or p.name.startswith("guide12")))


def z_of(root: Path, capture_id: str):
    stats = json.loads(
        (root / "measurements" / f"{capture_id}.patch-statistics.json")
        .read_text(encoding="utf-8"))
    layer = guide13.primary_layer_from_stats(stats)
    if layer["primary_quality"] != "accepted":
        return None, layer["primary_quality"]
    return guide13.z_from_planes(layer["planes_nps"]), "accepted"


def block_frames(root: Path) -> dict:
    """tag -> {z, quality, command} for one C13-B block root."""
    out: dict[str, dict] = {}
    for line in (root / "captures.jsonl").read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        s = json.loads(line)["plan_step"]
        cid = str(s["capture_id"])
        tag = ("ray_before" if s.get("ray_reference_position") == "raybefore"
               else "ray_after" if s.get("ray_reference_position") == "rayafter"
               else str(s.get("candidate_tag")))
        z, q = z_of(root, cid)
        out[tag] = {"capture_id": cid, "z": z, "quality": q,
                    "command": s.get("command")}
    return out


def main() -> int:
    jac_src = json.loads(J_FILE.read_text(encoding="utf-8"))
    jac = {t["target"]: guide13.local_jacobian(
        t["J_columns"]["dz_per_deg_H"], t["J_columns"]["dz_per_pp_S"])
        for t in jac_src["targets"]}

    report: dict = {
        "schema": "guide13_completion_c13b_reanalysis_v1",
        "identity": IDENTITY,
        "provenance_verdicts": {
            "block_analyses": "original block-analysis outputs for C13-B were "
                              "not retained as files (analyzer "
                              "tmp/analyze_w12_block_20260930.py is retained; "
                              "its C13-B invocations were inline) -> "
                              "original_generator_not_retained; measured dz "
                              "recomputed here from retained frames",
            "hs_estimates": "node-state hs_estimate values recomputed via "
                            "guide13.solve_local_delta(J_anchor, dz_best)",
            "ci_pi": "not_calculated (no uncertainty model installed post hoc)",
        },
        "blocks": {},
        "hs_recomputation": {},
        "reference_drifted_source_values": {},
        "qualified_command_observations": [],
    }

    blocks = sorted(p for p in C13B.iterdir()
                    if p.is_dir() and (p / "captures.jsonl").exists())
    ray_z_by_block: dict[str, dict] = {}
    for root in blocks:
        frames = block_frames(root)
        report["blocks"][root.name] = frames
        rb = frames.get("ray_before", {}).get("z")
        ra = frames.get("ray_after", {}).get("z")
        if rb and ra:
            ray_mean = [(rb[i] + ra[i]) / 2 for i in (0, 1)]
            ray_z_by_block[root.name] = {
                "ray_before": rb, "ray_after": ra, "ray_mean": ray_mean}
            for tag, f in frames.items():
                if tag.startswith("ray_") or f["z"] is None:
                    continue
                f["dz_vs_ray_mean"] = [f["z"][i] - ray_mean[i] for i in (0, 1)]

    # H/S recomputation for the two S50 targets with Js
    for node, anchor, node_file in (
            ("H0/S50", "0/50", "c13b-node-state-h0-s50.json"),
            ("H300/S50", "300/50", "c13b-node-state-h300-s50.json")):
        ns = json.loads((C13B / "derived" / node_file).read_text(encoding="utf-8"))
        dz_best = ns.get("best_dz")
        entry = {"node": node, "anchor": anchor,
                 "node_state_best_dz": dz_best,
                 "node_state_hs_estimate": ns.get("hs_estimate")}
        if dz_best:
            dh, ds = guide13.solve_local_delta(jac[anchor], dz_best)
            entry["recomputed_hs"] = {
                "dH_deg": round(dh, 4), "dS_pp": round(ds, 4),
                "formula": "(dH,dS)=J^-1 dz, J from "
                           "c13a-local-jacobian-20261013.json target " + anchor,
            }
            est = ns.get("hs_estimate") or {}
            entry["matches_node_state"] = (
                abs(round(dh, 2) - float(est.get("dH_deg", dh))) <= 0.01
                and abs(round(ds, 2) - float(est.get("dS_pp", ds))) <= 0.01)
        # locate the best command's measured frame in blocks
        best_cmd = ns.get("best_command")
        found = []
        for bname, frames in report["blocks"].items():
            for tag, f in frames.items():
                if f.get("command") == best_cmd and f["z"] is not None:
                    found.append({"block": bname, "tag": tag,
                                  "capture_id": f["capture_id"],
                                  "dz_vs_ray_mean": f.get("dz_vs_ray_mean")})
        entry["best_command_measured_frames"] = found
        report["hs_recomputation"][node] = entry

    # reference_drifted targets: source-level Ray values + candidate offsets
    for node, blocks_for in (
            ("H0/S100", ["formal-c13b-h0-s100-b1"]),
            ("H120/S100", ["formal-c13b-h120-s100-b1", "formal-c13b-h120-s100-b2",
                           "formal-c13b-h120-s100-b3"]),
            ("H300/S100", ["formal-c13b-h300-s100-b1"])):
        per_block = {}
        for b in blocks_for:
            frames = report["blocks"].get(b, {})
            ray = ray_z_by_block.get(b, {})
            per_block[b] = {
                "ray": ray,
                "candidate_dz": {t: f.get("dz_vs_ray_mean")
                                 for t, f in frames.items()
                                 if not t.startswith("ray_") and f.get("z")},
            }
        report["reference_drifted_source_values"][node] = {
            "comparison_as_recorded": (
                "node states record candidate offsets vs this campaign's own "
                "Ray bracket means (z_b +1.2-1.6 at H0/S100; z_r -0.6/-0.8 at "
                "H300/S100); the across-session baseline implied by "
                "'reference_drifted' is the C124/N2-era anchor expectation, "
                "not a retained same-session numeric baseline"),
            "per_block": per_block,
        }

    # every physical observation of the qualified H0/S50 command
    obs = []
    for camp in SEARCH_CAMPAIGNS:
        cdir = D / camp
        if not cdir.exists():
            continue
        for root in sorted(cdir.iterdir()):
            cap = root / "captures.jsonl"
            if not (root.is_dir() and cap.exists()):
                continue
            for line in cap.read_text(encoding="utf-8").splitlines():
                if not line.strip():
                    continue
                row = json.loads(line)
                s = row["plan_step"]
                if s.get("command") == QUALIFIED_CMD:
                    obs.append({
                        "campaign": camp, "run": root.name,
                        "capture_id": str(s["capture_id"]),
                        "source": s.get("source_id"),
                        "tag": s.get("candidate_tag"),
                        "role": "development_selection_frame",
                    })
    confirmed = [o for o in obs if "w13b" in o["campaign"]]
    report["qualified_command_observations"] = obs
    report["qualified_command_confirmation_status"] = (
        "not_acquired (no independent confirmation run observed this exact "
        "command; every retained observation is a C13-B development selection "
        "frame; the node state itself queues 3 confirmations)"
        if not confirmed else
        {"status": "confirmations_present", "observations": confirmed})

    outdir = WORK / "reanalysis"
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "c13b-hs-drift-reanalysis-20261020.json").write_text(
        json.dumps(report, indent=1, sort_keys=True), encoding="utf-8")
    print(json.dumps({
        "blocks": len(report["blocks"]),
        "hs": {k: {"recomputed": v.get("recomputed_hs"),
                   "matches": v.get("matches_node_state"),
                   "frames": len(v.get("best_command_measured_frames", []))}
               for k, v in report["hs_recomputation"].items()},
        "qualified_cmd_observations": len(obs),
        "confirmation": report["qualified_command_confirmation_status"]
        if isinstance(report["qualified_command_confirmation_status"], str)
        else "confirmations_present",
    }, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
