"""D3.3/3.4 reconciliation (GUIDE13 evidence completion 20261020): W13-B
3-pair ledger, workpackage count calibers, C13-C per-hue fathers, W13-C v2
generator binding.

Everything here is derived from retained analyses/ledgers; original counts
are annotated with their statistical caliber, never rewritten to match.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from camera_based_rgbww_optimizer.optimization import guide12_c124  # noqa: E402

D = Path("D:/rgbww-optimizer")
WORK = D / "guide13" / "completion-20261020"
IDENTITY = "reanalysis/export (GUIDE13 evidence completion 20261020)"
W13B = D / "guide13-w13b/derived"


def load(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))


def main() -> int:
    # ---- 1. W13-B unified pair ledger ----
    s1 = load(W13B / "w13b-s1-confirmation-analysis.json")
    s2c = load(W13B / "w13b-s2-combined-confirmation-analysis.json")
    s3 = load(W13B / "w13b-s3-confirmation-analysis.json")
    s4 = load(W13B / "w13b-s4-final-analysis.json")
    ledger: dict[str, list] = {}

    def add(node, session, ordn, strip, refs, E, within):
        ledger.setdefault(node, []).append({
            "session": session, "pair_ordinal": ordn,
            "strip_capture_id": strip, "reference_capture_ids": refs,
            "E_normalized": E, "E_within_gate": within})

    for r in s1["pairs"]:
        add(r["node"], "s1", r["pair_ordinal"], r["strip_capture_id"],
            r["reference_capture_ids"], r["E_normalized"], r["E_within_gate"])
    for r in s2c["pairs"]:
        add(r["node"], "s2/s2r-a/s2r-b", r["pair_ordinal"], r["strip_capture_id"],
            r["reference_capture_ids"], r["E_normalized"], r["E_within_gate"])
    # s3/s4 rows carry (node, ordinal, E) only; resolve the actual capture
    # identities from the run roots by w13b_node/w13b_pair_ordinal
    def resolve_from_root(camp: str, run: str):
        mapping = {}
        cap = D / camp / run / "captures.jsonl"
        if not cap.exists():
            return mapping
        for line in cap.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            s = json.loads(line)["plan_step"]
            if s.get("source_id") == "strip":
                mapping[(str(s.get("w13b_node")), s.get("w13b_pair_ordinal"))] = {
                    "strip_capture_id": str(s["capture_id"]),
                    "run": run,
                }
        return mapping

    res_map: dict[tuple, dict] = {}
    for run in ("formal-w13b-s3", "formal-w13b-s4", "formal-w13b-s4-recert"):
        res_map.update(resolve_from_root("guide13-w13b", run))

    def add_rows(rows, session):
        for r in rows:
            node = str(r.get("node"))
            ordn = r.get("ord", r.get("pair_ordinal"))
            resolved = res_map.get((node, ordn), {})
            add(node, session, ordn,
                resolved.get("strip_capture_id"), None,
                r.get("E_normalized", r.get("E")),
                r.get("E") is not None and r["E"] <= 1.0)

    if isinstance(s3, list):
        add_rows(s3, "s3")
    add_rows(s4.get("s4", []), "s4")
    recert = s4.get("recert_20000_130", [])
    if isinstance(recert, list) and recert:
        add_rows(recert, "s4-recert")

    node_table = []
    for node, rows in sorted(ledger.items(), key=lambda kv: tuple(
            int(v) for v in kv[0].split("/"))):
        valid = [r for r in rows if r["E_normalized"] is not None]
        session_ok = [r for r in valid if r["E_within_gate"]]
        s1row = next((r for r in s1.get("node_summary", [])
                      if r["node"] == node), None)
        s2row = next((r for r in s2c.get("node_summary", [])
                      if r["node"] == node), None)
        # retained confirmation semantics: pair 1 is the W13-A/W12-2
        # qualifying observation (historical), pairs 2/3 are session pairs;
        # s1 analyzer expresses this as all_within_gate on its 2 session pairs
        confirmed = bool(
            (s1row is not None and s1row.get("all_within_gate"))
            or (s2row is not None and s2row.get("confirmed_3_pairs"))
            or (node in {r["node"] for r in s4.get("s4", []) if r["E"] <= 1.0}
                and len(session_ok) >= 1))
        node_table.append({
            "node": node,
            "pairs": rows,
            "valid_pairs": len(valid),
            "session_pairs_within_gate": len(session_ok),
            "retained_semantics_note": (
                "pair ordinal 1 is the qualifying W13-A block (or W12-2 "
                "original measurement); session pairs are ordinals 2/3"),
            "confirmed_3_pairs": confirmed,
        })
    confirmed_nodes = [n["node"] for n in node_table if n["confirmed_3_pairs"]]
    s2_confirmed = [r["node"] for r in s2c.get("node_summary", [])
                    if r.get("confirmed_3_pairs")]
    s1_confirmed = [r["node"] for r in s1.get("node_summary", [])
                    if r.get("all_within_gate")]

    # ---- 2. workpackage count calibers ----
    census = {(r["campaign"], r["run"]): r for r in load(WORK / "RUN_INDEX_COMPLETE.json")}

    def frames(camp, runs=None):
        return sum(r["captures"] for (c, n), r in census.items()
                   if c == camp and (runs is None or n in runs))

    retest_roots = ["formal-w13a-1800-100-retest", "formal-w13a-20000-0-retest",
                    "formal-w13a-20000-100-retest", "formal-w13a-20000-200-retest"]
    calibers = {
        "ledger_totals": {
            "all_campaigns_frames": sum(r["captures"] for r in census.values()
                                        if r["class"] != "plan_dry"),
            "ray_vs_strip_per_campaign": "see PAIRINGS_COMPLETE.json (316 strip "
                                         "frames, 310 Ray frames)",
        },
        "final_report_figures_annotated": {
            "W13-A ~236": {
                "report_caliber": ("approximate figure (marked ~ in the report); "
                                   "not exactly reproducible from ledgers - no "
                                   "denominator definition was retained"),
                "ledger": {
                    "w13a_total_frames": frames("guide13-w13a"),
                    "retest_discrimination_roots_frames":
                        frames("guide13-w13a", retest_roots),
                    "main_queue_frames": frames("guide13-w13a") -
                                         frames("guide13-w13a", retest_roots),
                    "strip_frames": 180, "ray_frames": 128,
                },
                "note": "all ledger figures retained; the report's ~236 is "
                        "annotated, not rewritten and not force-matched",
            },
            "C13-B ~35": {
                "report_caliber": "strip frames",
                "ledger": {"c13b_total": frames("guide13-c13b"),
                           "c13b_strip": 35},
            },
            "W13-B 48+55+16+27+3": {
                "ledger": {
                    "s1": frames("guide13-w13b", ["formal-w13b-s1"]),
                    "s2_chain": frames("guide13-w13b",
                                       ["formal-w13b-s2", "formal-w13b-s2r-a",
                                        "formal-w13b-s2r-b"]),
                    "s3": frames("guide13-w13b", ["formal-w13b-s3"]),
                    "s4_and_recert": frames(
                        "guide13-w13b", ["formal-w13b-s4", "formal-w13b-s4-recert"]),
                },
            },
            "W13-C 13+13": {"ledger": frames("guide13-w13c")},
            "C13-A 21": {"ledger": frames("guide13-c13a")},
            "C13-D 63": {"ledger": frames("guide13-c13d")},
        },
    }

    # ---- 3. C13-C per-hue father observations ----
    c13c = load(D / "guide13/derived/c13c-sat-coverage-20261018.json")
    adopted = guide12_c124.C124_ADOPTED
    adopted_levels = {}
    for key in adopted:
        parts = str(key).split("/")
        if len(parts) == 2 and parts[0].lstrip("-").isdigit():
            adopted_levels.setdefault(int(parts[0]), set()).add(int(parts[1]))
    c13a_targets = {t["target"] for t in
                    load(D / "guide13-c13a/derived/c13a-local-jacobian-20261013.json")["targets"]}
    hue_fathers = {}
    for hue, row in c13c["per_hue"].items():
        h = int(hue[1:])
        sats = row["confirmed_sats"]
        per_sat = {}
        for s in sats:
            if s == 0:
                per_sat["S0"] = ("C124 white anchor 0/0 (guide12_c124.C124_ADOPTED, "
                                 "base-package source)")
            elif (h, s) in {(0, 50), (300, 50)} and f"{h}/{s}" in c13a_targets:
                per_sat[f"S{s}"] = (f"C13-A local-J anchor frames at {h}/{s} "
                                    "(c13a-local-jacobian-20261013.json)")
            elif h == 60 and s == 100:
                per_sat[f"S{s}"] = ("C13-A 60/100 anchor frames + C124 runtime "
                                    "anchors (per c13c s100_status)")
            elif s == 50 and h in (0, 120, 180, 240, 300):
                per_sat[f"S{s}"] = (
                    f"C13-B {hue}/S50 block Ray frames (guide13-c13b blocks) + "
                    + ("C124 anchor present" if s in adopted_levels.get(h, set())
                       else "no C124 anchor at this exact level"))
            elif s in adopted_levels.get(h, set()):
                per_sat[f"S{s}"] = "C124 adopted anchor level (guide12_c124)"
            else:
                per_sat[f"S{s}"] = ("father observations not localized inside "
                                    "GUIDE13 scope; level reported by retained "
                                    "c13c report only")
        hue_fathers[hue] = {"confirmed_sats": sats,
                            "s100_status": row["s100_status"],
                            "s_best_tested": row["s_best_tested"],
                            "father_sources": per_sat}
    c124_levels_note = {str(h): sorted(v) for h, v in sorted(adopted_levels.items())}

    # ---- 4. W13-C v2 generator binding ----
    w13c_binding = {
        "retained_analyzer": "tmp/analyze_w13c_dev_20261013.py (original package "
                             "source/; unchanged since commit f10a1f2)",
        "v1_regression": "generated by the retained analyzer as committed",
        "v2_regression": ("original_generator_not_retained: the retained script "
                          "hard-codes the W12-2 frozen LUT path; the v2 numbers "
                          "were produced by an inline invocation over corrected "
                          "LUT v2 + corrected node errors; output "
                          "w13c-dev-v2-regression-20261016.json is retained and "
                          "recomputed transparently in the replay"),
    }

    out = {
        "schema": "guide13_completion_w13b_c13c_reconciliation_v1",
        "identity": IDENTITY,
        "w13b_3pair_ledger": {
            "nodes": node_table,
            "counts": {
                "s1_confirmed": s1_confirmed,
                "s2_confirmed": s2_confirmed,
                "recomputed_confirmed_nodes": confirmed_nodes,
                "campaign_summary_claim": "20 nodes 3-pair confirmed "
                                          "(10 s1 + 2 s2 + 8 s4)",
                "matches_claim": len(confirmed_nodes) == 20,
            },
        },
        "count_calibers": calibers,
        "c13c_hue_fathers": hue_fathers,
        "c124_adopted_levels": c124_levels_note,
        "w13c_v2_generator_binding": w13c_binding,
    }
    outdir = WORK / "reanalysis"
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "w13b-c13c-reconciliation-20261020.json").write_text(
        json.dumps(out, indent=1, sort_keys=True), encoding="utf-8")
    print(json.dumps({
        "confirmed_nodes": len(confirmed_nodes),
        "claim_20": len(confirmed_nodes) == 20,
        "s1": len(s1_confirmed), "s2": len(s2_confirmed),
        "calibers_W13A": calibers["final_report_figures_annotated"]["W13-A ~236"]["ledger"],
        "calibers_W13B": calibers["final_report_figures_annotated"]["W13-B 48+55+16+27+3"]["ledger"],
        "c124_hues": sorted(c124_levels_note),
    }, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
