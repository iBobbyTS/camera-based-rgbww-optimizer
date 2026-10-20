"""D3.1 reanalysis (GUIDE13 evidence completion 20261020): C13-D low-SAT gate.

The retained generator (tmp/analyze_c13d_holdout_20261019.py, in the original
package) outputs per-request direct dz, Ray before/after drift and track
groupings only. The dH/dS inversions and the "10/10 within +-2deg/+-2pp"
count in c13d-verdict-20261019.json were computed inline at verdict time and
that generator was NOT retained. This script transparently recomputes the
H/S inversion from retained inputs (C13-D run frames + C13-A local Jacobians
+ guide13.solve_local_delta), enumerates the exact request IDs, marks every
cross-anchor Jacobian transfer as transfer_validation_not_performed, and
compares the recomputed numbers against the verdict text without altering it.
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
ROOTS = [D / "guide13-c13d/formal-c13d-holdout",
         D / "guide13-c13d/formal-c13d-holdout-tail"]
J_FILE = D / "guide13-c13a/derived/c13a-local-jacobian-20261013.json"
VERDICT_EXPECTED = {
    "H60/S10": (-1.54, -0.93), "H60/S20": (-0.63, -0.60), "H60/S37": (1.06, 0.90),
    "H75-family S10": (1.89, 0.12), "H75-family S20": (0.68, -0.36),
}
# anchor mapping used by the original verdict (per its own text)
ORIGINAL_ANCHOR = {60: "60/100", 75: "0/50", 1: "0/50", 359: "0/50"}
# transfer policy honesty: also compute H300 with its measured 300/50 J,
# which the original verdict did NOT use despite the J existing
EXTENDED_ANCHOR = {**ORIGINAL_ANCHOR, 300: "300/50", 120: None, 135: None,
                   255: None, 195: None, 315: None}
GATE = (2.0, 2.0)


def z_of(root: Path, capture_id: str):
    stats = json.loads(
        (root / "measurements" / f"{capture_id}.patch-statistics.json")
        .read_text(encoding="utf-8"))
    layer = guide13.primary_layer_from_stats(stats)
    if layer["primary_quality"] != "accepted":
        return None, layer["primary_quality"]
    return guide13.z_from_planes(layer["planes_nps"]), "accepted"


def main() -> int:
    jac = {t["target"]: guide13.local_jacobian(
        t["J_columns"]["dz_per_deg_H"], t["J_columns"]["dz_per_pp_S"])
        for t in json.loads(J_FILE.read_text(encoding="utf-8"))["targets"]}

    by_req: dict[str, dict[str, list]] = {}
    frames = 0
    for root in ROOTS:
        rows = [json.loads(l) for l in
                (root / "captures.jsonl").read_text(encoding="utf-8").splitlines()
                if l.strip()]
        frames += len(rows)
        for row in rows:
            s = row["plan_step"]
            req = str(s["c13d_request"])
            slot = "ref" if str(s["c13d_position"]).startswith("ray") else "strip"
            z, q = z_of(root, str(s["capture_id"]))
            by_req.setdefault(req, {}).setdefault(slot, []).append({
                "capture_id": str(s["capture_id"]), "z": z, "quality": q,
                "realized_sat": s.get("c13d_realized_sat"),
                "sat_status": s.get("c13d_sat_status"),
                "root": root.name})

    points = []
    for req in sorted(by_req, key=lambda k: tuple(int(x) for x in k.split("/"))):
        hue_s, sat_s = req.split("/")
        hue, sat = int(hue_s), int(sat_s)
        g = by_req[req]
        refs = [r for r in g.get("ref", []) if r["z"] is not None]
        strips = [r for r in g.get("strip", []) if r["z"] is not None]
        entry = {
            "request": req, "refs": refs, "strip": strips[0] if strips else None,
            "anchor_used_by_original_verdict": ORIGINAL_ANCHOR.get(hue),
            "anchor_available_but_unused": (
                "300/50" if hue == 300 and "300/50" in jac else None),
        }
        if not refs or not strips:
            entry["status"] = "incomplete_or_primary_invalid"
            points.append(entry)
            continue
        ray = [sum(r["z"][i] for r in refs) / len(refs) for i in (0, 1)]
        dz = [strips[0]["z"][i] - ray[i] for i in (0, 1)]
        entry.update({
            "status": "measured",
            "dz": dz,
            "worst_abs_dz": max(abs(v) for v in dz),
            "realized_sat": strips[0]["realized_sat"],
            "sat_status_label": strips[0]["sat_status"],
        })
        anchor = EXTENDED_ANCHOR.get(hue)
        if anchor and anchor in jac:
            dh, ds = guide13.solve_local_delta(jac[anchor], dz)
            entry["hs_inversion"] = {
                "anchor": anchor,
                "dH_deg": round(dh, 4), "dS_pp": round(ds, 4),
                "formula": "(dH,dS) = J^-1 dz (guide13.solve_local_delta, "
                           "explicit 2x2 inverse; J from "
                           "c13a-local-jacobian-20261013.json)",
                "transfer_validation": "transfer_validation_not_performed",
                "transfer_note": (
                    f"J measured at anchor {anchor} applied at request {req}; "
                    "no retained experiment validates this cross-SAT/cross-hue "
                    "transfer; flagged, not silently accepted"),
                "within_gate": abs(dh) <= GATE[0] and abs(ds) <= GATE[1],
                "used_by_original_verdict": ORIGINAL_ANCHOR.get(hue) == anchor,
            }
        else:
            entry["hs_inversion"] = {
                "status": "not_evaluable_no_measured_j",
                "note": "no C13-A local J for this hue family; original "
                        "verdict reported direct dz only (correctly)",
            }
        points.append(entry)

    # low-SAT sets
    low_sat = [p for p in points if p.get("status") == "measured"
               and int(p["request"].split("/")[1]) <= 37]
    original_set = [p for p in low_sat
                    if p.get("hs_inversion", {}).get("used_by_original_verdict")]
    extended_set = [p for p in low_sat if "dH_deg" in p.get("hs_inversion", {})]

    def gate_summary(items):
        return {
            "count": len(items),
            "request_ids": [p["request"] for p in items],
            "within_gate": sum(1 for p in items
                               if p["hs_inversion"].get("within_gate")),
            "per_point": [
                {"request": p["request"],
                 "dH_deg": p["hs_inversion"].get("dH_deg"),
                 "dS_pp": p["hs_inversion"].get("dS_pp"),
                 "within": p["hs_inversion"].get("within_gate")}
                for p in items],
        }

    # numeric comparison with the verdict text (never edited)
    comparison = []
    for key, (edh, eds) in VERDICT_EXPECTED.items():
        req = (key.replace("H60/S", "60/").replace("H75-family S", "75/"))
        match = next((p for p in points if p["request"] == req
                      and "dH_deg" in p.get("hs_inversion", {})), None)
        if match is None:
            comparison.append({"verdict_claim": key, "status": "no_recomputed_point"})
            continue
        h = match["hs_inversion"]
        comparison.append({
            "verdict_claim": key,
            "verdict_dH_dS": [edh, eds],
            "recomputed_dH_dS": [h["dH_deg"], h["dS_pp"]],
            "abs_diff": [round(abs(h["dH_deg"] - edh), 4),
                         round(abs(h["dS_pp"] - eds), 4)],
        })

    out = {
        "schema": "guide13_completion_c13d_lowsat_reanalysis_v1",
        "identity": IDENTITY,
        "provenance_verdicts": {
            "direct_dz_per_request": "retained generator "
                                     "tmp/analyze_c13d_holdout_20261019.py",
            "hs_inversion_and_10_of_10_count": "original_generator_not_retained "
                                               "(computed inline at verdict time; "
                                               "recomputed here from retained inputs)",
            "ci_pi_jacobian_covariance": "not_calculated (neither original "
                                         "verdict nor this reanalysis installs "
                                         "an uncertainty model post hoc)",
            "h300_anchor_note": "C13-A measured a 300/50 J; the original "
                                "verdict did not use it for the H300 track "
                                "(direct dz only). This reanalysis reports it "
                                "as an extended, clearly-flagged variant.",
        },
        "gate": {"dH_deg": GATE[0], "dS_pp": GATE[1]},
        "frames_checked": frames,
        "requests_total": len(points),
        "low_sat_points_all": [p["request"] for p in low_sat],
        "sets": {
            "original_verdict_j_usage": gate_summary(original_set),
            "extended_all_js_incl_h300": gate_summary(extended_set),
            "low_sat_without_any_j": [p["request"] for p in low_sat
                                      if "dH_deg" not in p.get("hs_inversion", {})],
        },
        "verdict_text_numeric_comparison": comparison,
        "per_request_points": points,
    }
    outdir = WORK / "reanalysis"
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "c13d-low-sat-gate-reanalysis-20261020.json").write_text(
        json.dumps(out, indent=1, sort_keys=True), encoding="utf-8")
    print(json.dumps({
        "requests": len(points), "low_sat": len(low_sat),
        "original_set": gate_summary(original_set)["within_gate"],
        "of": gate_summary(original_set)["count"],
        "extended_set": gate_summary(extended_set)["within_gate"],
        "of_ext": gate_summary(extended_set)["count"],
        "no_j_low_sat": out["sets"]["low_sat_without_any_j"],
    }, indent=1))
    for c in comparison:
        print(c)
    return 0


if __name__ == "__main__":
    sys.exit(main())
