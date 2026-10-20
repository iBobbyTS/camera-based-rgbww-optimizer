"""D3.3 reanalysis (GUIDE13 evidence completion 20261020): corrected LUT v2
rebuild and the 70-node white reference table.

The generator that produced w13a-corrected-lut-v2-20261016.json was an
inline computation (only the output JSON was committed, 486ac49) ->
original_generator_not_retained. This script rebuilds the LUT from retained
inputs following the replacement rule documented in the file's own
replacement_note, diffs the rebuild against the retained v2 node by node,
and emits the 70-node white reference table (final command, changed flag,
W13-A status class, supporting evidence pointer, W13-B confirmation status
where measured). Differences, if any, are preserved, never reconciled away.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

D = Path("D:/rgbww-optimizer")
WORK = D / "guide13" / "completion-20261020"
IDENTITY = "reanalysis (GUIDE13 evidence completion 20261020)"
V1 = D / "guide12-w122/derived/w12-2-frozen-lut-20261005.json"
V2 = D / "guide13-w13a/derived/w13a-corrected-lut-v2-20261016.json"
SUMMARY = D / "guide13-w13a/derived/w13a-campaign-summary-20261016.json"
NS_DIR = D / "guide13-w13a/derived"
W13B_DIR = D / "guide13-w13b/derived"


def key(node: dict) -> str:
    return f"{node['cct']}/{node['gm']}"


def main() -> int:
    v1 = json.loads(V1.read_text(encoding="utf-8"))
    v2 = json.loads(V2.read_text(encoding="utf-8"))
    summary = json.loads(SUMMARY.read_text(encoding="utf-8"))
    node_states = {}
    for p in sorted(NS_DIR.glob("w13a-node-state-*.json")):
        ns = json.loads(p.read_text(encoding="utf-8"))
        node_states[ns["node"]] = {**ns, "_file": p.name}

    new_cmd_nodes = list(summary["qualified_new_command"])
    requal_nodes = list(summary["qualified_original_command"])

    # rebuild per documented rule
    rebuilt_nodes = []
    diffs = []
    for node in v1["nodes"]:
        k = key(node)
        out = dict(node)
        out.pop("w13a_update", None)
        if k in new_cmd_nodes:
            ns = node_states.get(k)
            if ns is None or "best_command" not in ns:
                diffs.append({"node": k, "issue": "node state missing best_command"})
            else:
                out["command"] = dict(ns["best_command"])
                out["w13a_update"] = "w13a_new_command"
        elif k in requal_nodes:
            out["w13a_update"] = "original_command_session_qualified"
        elif k == "1800/100":
            pass  # closure point: retained v2 leaves it unlabeled
        rebuilt_nodes.append(out)

    v2_by_key = {key(n): n for n in v2["nodes"]}
    for out in rebuilt_nodes:
        k = key(out)
        kept = v2_by_key.get(k)
        if kept is None:
            diffs.append({"node": k, "issue": "missing in retained v2"})
            continue
        if out.get("command") != kept.get("command"):
            diffs.append({"node": k, "issue": "command differs",
                          "rebuilt": out.get("command"), "retained": kept.get("command")})
        if out.get("w13a_update") != kept.get("w13a_update"):
            diffs.append({"node": k, "issue": "w13a_update label differs",
                          "rebuilt": out.get("w13a_update"),
                          "retained": kept.get("w13a_update")})
    extra = [k for k in v2_by_key if k not in {key(n) for n in rebuilt_nodes}]
    replaced_in_retained = sum(1 for n in v2["nodes"] if n.get("w13a_update"))

    # W13-B confirmation status map (from retained analyses)
    confirm_map: dict[str, dict] = {}
    s1 = json.loads((W13B_DIR / "w13b-s1-confirmation-analysis.json").read_text(encoding="utf-8"))
    for row in s1.get("node_summary", []):
        confirm_map[row["node"]] = {"s1": row}
    s2c = json.loads((W13B_DIR / "w13b-s2-combined-confirmation-analysis.json").read_text(encoding="utf-8"))
    for row in s2c.get("node_summary", []):
        confirm_map.setdefault(row["node"], {})[
            "s2_confirmed_3_pairs"] = row.get("confirmed_3_pairs")
    s4 = json.loads((W13B_DIR / "w13b-s4-final-analysis.json").read_text(encoding="utf-8"))
    for row in s4.get("s4", []):
        confirm_map.setdefault(row["node"], {})["s4_E_ord3"] = row.get("E")

    def w13b_status(k: str) -> str:
        e = confirm_map.get(k)
        if not e:
            return "not_measured_in_w13b"
        if e.get("s2_confirmed_3_pairs") is True:
            return "3_pair_confirmed_s2"
        s1r = e.get("s1")
        if s1r is not None:
            base = "s1_confirmed" if s1r.get("confirmed_3_pairs") else "s1_pairs"
            s4e = e.get("s4_E_ord3")
            if s4e is not None:
                return base + ("+s4_within" if s4e <= 1.0 else "+s4_exceeds")
            return base
        s4e = e.get("s4_E_ord3")
        return f"s4_only_E={s4e}" if s4e is not None else "partial"

    # 70-node white reference table
    table = []
    for kept in v2["nodes"]:
        k = key(kept)
        changed = bool(kept.get("w13a_update"))
        table.append({
            "node": k,
            "final_command": kept.get("command"),
            "changed_in_v2": changed,
            "w13a_update_label": kept.get("w13a_update"),
            "w13a_status_class": (
                "qualified_new_command" if k in new_cmd_nodes
                else "qualified_original_command" if k in requal_nodes
                else "closure_point" if k == "1800/100"
                else "reference_limited" if k == "20000/130"
                else "unchanged_from_w12_2"),
            "evidence_pointer": (
                f"results/guide13-w13a/{node_states[k]['_file']}"
                if k in node_states else
                "GUIDE12 base package w12-2-frozen-lut-20261005.json (original "
                "W12-2 evidence, unchanged this campaign)"),
            "w13b_cross_session_status": w13b_status(k),
            "ci_pi": "not_calculated for the adopted command this campaign "
                     "(W13-B pair errors are reported as E/signed values; no "
                     "CI/PI was installed on the LUT commands)",
        })

    out = {
        "schema": "guide13_completion_lut_v2_rebuild_v1",
        "identity": IDENTITY,
        "provenance": {
            "original_generator": "original_generator_not_retained "
                                  "(inline at commit 486ac49; output committed, "
                                  "script not)",
            "rebuild_rule": v2.get("replacement_note"),
            "inputs": {
                "v1_lut": str(V1), "campaign_summary": str(SUMMARY),
                "node_state_files": len(node_states)},
        },
        "rebuild_result": {
            "nodes": len(rebuilt_nodes),
            "command_or_label_diffs_vs_retained": diffs,
            "extra_nodes_in_retained": extra,
            "retained_nodes_replaced_label_count": replaced_in_retained,
            "expected_replaced": v2.get("nodes_replaced"),
            "verdict": (
                "rebuilt identical to retained v2 (commands and w13a_update "
                "labels)" if not diffs and not extra
                and replaced_in_retained == v2.get("nodes_replaced")
                else "differences preserved above"),
        },
        "white_node_reference_table_70": table,
    }
    outdir = WORK / "reanalysis"
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "w13a-corrected-lut-v2-rebuild-20261020.json").write_text(
        json.dumps(out, indent=1, sort_keys=True), encoding="utf-8")
    print(json.dumps({
        "diffs": len(diffs), "extra": extra,
        "replaced_retained": replaced_in_retained,
        "expected": v2.get("nodes_replaced"),
        "verdict": out["rebuild_result"]["verdict"],
    }, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
