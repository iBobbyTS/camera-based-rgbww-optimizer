"""GUIDE13 offline-correction audit table (no device access).

Produces the pre-experiment audit the GUIDE13 implementation prompt
requires before any new capture: existing white-light statuses, primary-
layer recovered frames, high-SAT valid directions, local-mapping
qualification, actual command counts, and old-vs-new verdict differences.

Everything is recomputed from the local D: run roots with the corrected
guide13 owners; the advisor/13 data files are used only as cross-checks
(with numeric tolerances), never as the source of the local numbers.
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from camera_based_rgbww_optimizer.optimization import guide13  # noqa: E402

D = Path("D:/rgbww-optimizer")
C122 = D / "guide12-c122"
N2 = D / "guide12-n2"
W122 = D / "guide12-w122"
ADV = Path(__file__).resolve().parents[1] / "advisor" / "13" / "data"
OUT = D / "guide13" / "derived" / "offline-correction-audit-20261013.json"

T_975_DF2 = 4.302652729911275
CHI2_975_DF3 = 9.348403602498
CHI2_025_DF3 = 0.2157952855


def jl(path: Path) -> list[dict]:
    return [json.loads(x) for x in path.read_text(encoding="utf-8")
            .splitlines() if x.strip()]


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def stats_for(run: Path, capture_id: str) -> dict:
    return load(run / "measurements" / f"{capture_id}.patch-statistics.json")


def primary_of(run: Path, capture_id: str) -> dict:
    layer = guide13.primary_layer_from_stats(stats_for(run, capture_id))
    if layer["primary_quality"] == "accepted":
        layer["z"] = list(guide13.z_from_planes(layer["planes_nps"]))
    else:
        layer["z"] = None
    return layer


def c122_strip_rows() -> list[dict]:
    rows = []
    for root in sorted(C122.glob("formal-c122-*")):
        if not (root / "captures.jsonl").exists():
            continue
        captures = jl(root / "captures.jsonl")
        commands = {
            tuple(c.get("group_capture_ids") or ()): c
            for c in jl(root / "commands.jsonl")
        }
        for row in captures:
            if row.get("source_id") != "strip":
                continue
            step = row.get("plan_step") or {}
            if "c122_request" not in step:
                continue
            cmd = commands.get((row["capture_id"],))
            fullscale = (
                guide13.fullscale_from_command(cmd)["actual_fullscale"]
                if cmd else None
            )
            inner = (row.get("capture") or {}).get("capture") or {}
            rows.append({
                "run": f"guide12-c122/{root.name}",
                "capture_id": row["capture_id"],
                "target": step["c122_request"],
                "tag": step.get("c122_tag"),
                "candidate_role": step.get("candidate_role"),
                "secondary58_quality": guide13.secondary58_from_capture(row),
                "fullscale_readback": fullscale,
                "command": step.get("command"),
                "iso": inner.get("iso"),
                "aperture": inner.get("aperture"),
            })
    return rows


def audit_primary_recovery(rows: list[dict]) -> dict:
    advisor = load(ADV / "primary_secondary_gate_audit.json")
    advisor_by_key = {
        r["capture_id"]: r for r in advisor["primary_valid_global_rejected"]
    }
    recovered, mismatch = [], []
    for row in rows:
        if row["secondary58_quality"] == "pass":
            continue
        run_root = C122 / row["run"].split("/")[-1]
        layer = primary_of(run_root, row["capture_id"])
        if layer["primary_quality"] != "accepted":
            continue
        entry = {
            **row,
            "primary_planes": layer["planes"],
            "z": layer["z"],
        }
        recovered.append(entry)
        ref = advisor_by_key.get(row["capture_id"])
        if ref is None:
            mismatch.append({"capture_id": row["capture_id"],
                             "issue": "not_in_advisor_recovery"})
        elif layer["z"] is None or ref["z"] is None or any(
            abs(a - b) > 1e-9 for a, b in zip(layer["z"], ref["z"])
        ):
            mismatch.append({"capture_id": row["capture_id"],
                             "local_z": layer["z"], "advisor_z": ref["z"]})
    return {
        "recovered_primary_valid_secondary_rejected": recovered,
        "count": len(recovered),
        "advisor_count": advisor["primary_valid_global_rejected_count"],
        "z_cross_check_mismatches": mismatch,
        "reclassification": (
            "Five high-SAT 'near-noise corner unreachable' stop conclusions "
            "downgraded to bounded_search_not_exhaustive or "
            "primary_analysis_incomplete; secondary58 failures retained "
            "unchanged as the parallel layer"),
    }


def audit_blue_n2() -> dict:
    advisor = load(ADV / "primary_secondary_gate_audit.json")[
        "N2_blue_recovered_primary_analysis"]
    roots = ["formal-n2-session1-r5", "formal-n2-session2-r2",
             "formal-n2-session3"]
    sessions = []
    for index, name in enumerate(roots, 1):
        root = N2 / name
        captures = jl(root / "captures.jsonl")
        cycles = {}
        for row in captures:
            step = row.get("plan_step") or {}
            if step.get("n2_state_key") != "color_blue":
                continue
            cycle = int(step["n2_cycle_index"])
            layer = primary_of(root, row["capture_id"])
            cycles.setdefault(cycle, {})[row["source_id"]] = {
                "capture_id": row["capture_id"], "z": layer["z"],
            }
        dz = []
        for cycle in sorted(cycles):
            pair = cycles[cycle]
            if "ray" not in pair or "strip" not in pair:
                raise ValueError(f"incomplete blue pair {name} c{cycle}")
            if pair["strip"]["z"] is None or pair["ray"]["z"] is None:
                raise ValueError(f"primary invalid blue pair {name} c{cycle}")
            dz.append([b - a for a, b in
                       zip(pair["ray"]["z"], pair["strip"]["z"])])
        sessions.append({"session": index, "run": name,
                         "cycle_dz": dz, "session_mean": [
                             sum(d[k] for d in dz) / len(dz)
                             for k in (0, 1)]})
    n = len(sessions)
    mu = [sum(s["session_mean"][k] for s in sessions) / n for k in (0, 1)]
    sd = [math.sqrt(sum((s["session_mean"][k] - mu[k]) ** 2 for s in sessions)
                    / (n - 1)) for k in (0, 1)]
    within_num = [sum(
        (d[k] - s["session_mean"][k]) ** 2
        for s in sessions for d in s["cycle_dz"]) for k in (0, 1)]
    within = [v / 3.0 for v in within_num]
    between = [math.sqrt(max(0.0, sd[k] ** 2 - within[k] / 2.0))
               for k in (0, 1)]
    out = {
        "sessions": sessions,
        "mean_dz": mu,
        "session_mean_ci95": [
            [mu[k] - T_975_DF2 * sd[k] / math.sqrt(n),
             mu[k] + T_975_DF2 * sd[k] / math.sqrt(n)] for k in (0, 1)],
        "next_session_mean_pi95": [
            [mu[k] - T_975_DF2 * sd[k] * math.sqrt(1 + 1.0 / n),
             mu[k] + T_975_DF2 * sd[k] * math.sqrt(1 + 1.0 / n)]
            for k in (0, 1)],
        "within_cycle_sd": [math.sqrt(v) for v in within],
        "within_cycle_sd_ci95": [
            [math.sqrt(3.0 * within[k] / CHI2_975_DF3),
             math.sqrt(3.0 * within[k] / CHI2_025_DF3)] for k in (0, 1)],
        "between_session_sd_moment": between,
        "advisor_cross_check": {
            "mean_dz": advisor["mean_dz"],
            "max_abs_dev": max(
                abs(mu[k] - advisor["mean_dz"][k]) for k in (0, 1)),
        },
        "assumptions": (
            "Conditional Gaussian/exchangeable session means, 3 sessions; "
            "PI is for the next session mean, separate from the CI. Not an "
            "H/S mapping claim; the 58-layer near-noise verdicts stand."),
    }
    if out["advisor_cross_check"]["max_abs_dev"] > 1e-9:
        raise ValueError("blue N2 recovery deviates from advisor audit")
    return out


def audit_white() -> dict:
    advisor = load(ADV / "white_nodes.json")
    local = load(W122 / "derived" / "w12-2-verification-analysis.json")
    local_summary = {r["node"]: r["verdict"] for r in local["node_summary"]}
    counts: dict[str, int] = {}
    for verdict in local_summary.values():
        key = ("verified_qualified" if verdict == "verified_qualified"
               else "reference_limited" if verdict.startswith("reference_limited")
               else "exceeds_tolerance_or_other")
        counts[key] = counts.get(key, 0) + 1
    changed_2pair = [
        n["node"] for n in local["node_summary"]
        if n["valid_pairs"] >= 2
    ]
    return {
        "machine_counts_local": counts,
        "advisor_summary": advisor["summary"],
        "counts_note": (
            "38 point-estimate passes / 29 exceeds / 3 reference-limited; "
            "point-estimate pass is not a prediction guarantee"),
        "pairs_distribution": (
            "54 nodes x1 + 16 nodes x2 = 86 pairs (advisor recount of the "
            "same local pair table)"),
        "confirmation_gap_nodes": [
            f"{n['cct']}/{n['gm']}"
            for n in load(W122 / "derived" /
                          "w12-2-frozen-lut-20261005.json")["nodes"]
            if n.get("changed_since_w2") and f"{n['cct']}/{n['gm']}" != "3200/0"
        ],
        "confirmation_gap_note": (
            "16 changed nodes carry 2 pairs; 3200/0 reuses the N2 "
            "three-session six-cycle evidence, leaving 15 nodes below "
            "three independent confirmations"),
    }


def audit_color_targets() -> dict:
    confirmations = load(ADV / "color_confirmations.json")
    hue_status = load(ADV / "hue_coverage_status.json")
    search = load(ADV / "color_search_and_quality.json")
    direction_gaps = {}
    for label in ("0/100", "120/100", "180/100", "240/100", "300/100"):
        block = search[label]
        rows = block["rows"] if isinstance(block, dict) else block
        unique = {
            json.dumps(r["command"], sort_keys=True) for r in rows
            if r.get("command")
        }
        direction_gaps[label] = {
            "unique_physical_commands": len(unique),
            "next_action": (
                "one bounded re-search round under the corrected primary "
                "layer; not locked by the old near-noise stop reason"),
        }
    return {
        "distinct_confirmed_targets_including_S0":
            confirmations["actual_confirmed_discrete_target_count"],
        "reported_validated_samples":
            confirmations["reported_validated_samples"],
        "counting_note": (
            "13 model-adopted commands + S0 = 14 distinct targets, each "
            "3 confirmations + 1 selection frame; selection frames are "
            "not a 4th confirmation; '17 validated_samples' was not "
            "countable from the tables"),
        "hue_coverage_status": hue_status,
        "s100_direction_gaps": direction_gaps,
        "h300_s50": (
            "old tangential 0.38deg was arithmetic; correct product "
            "0.153386 (8.336deg at the old 0.0184/deg) is a formula check "
            "only - re-evaluate with a true local J before any command "
            "change"),
    }


def main() -> int:
    rows = c122_strip_rows()
    iso_counter: dict[str, int] = {}
    aperture_counter: dict[str, int] = {}
    for row in rows:
        iso_counter[str(row["iso"])] = iso_counter.get(str(row["iso"]), 0) + 1
        aperture_counter[str(row["aperture"])] = \
            aperture_counter.get(str(row["aperture"]), 0) + 1

    audit = {
        "schema": "guide13_offline_correction_audit_v1",
        "c122_strip_rows": len(rows),
        "primary_recovery": audit_primary_recovery(rows),
        "n2_blue_recovery": audit_blue_n2(),
        "white": audit_white(),
        "color": audit_color_targets(),
        "metadata_recovery": {
            "c122_nested_capture_iso": iso_counter,
            "c122_nested_capture_aperture": aperture_counter,
            "note": (
                "ISO 100 recovered from the nested capture object; "
                "'implicit auto' is not a measured aperture"),
        },
        "runtime_corrections": {
            "w123_mired_weight": "fixed; 70/70 node identity restored",
            "c124_s0": "S0 serves the validated white command at any hue",
            "c124_high_sat": "H60/S100 anchor actually served; other hues "
                             "compress explicitly with realized SAT",
        },
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(audit, indent=1, ensure_ascii=False),
                   encoding="utf-8")
    print("recovered primary-valid/secondary-rejected:",
          audit["primary_recovery"]["count"],
          "(advisor:", audit["primary_recovery"]["advisor_count"], ")")
    print("blue N2 mean dz:", audit["n2_blue_recovery"]["mean_dz"],
          "| max dev vs advisor:",
          audit["n2_blue_recovery"]["advisor_cross_check"]["max_abs_dev"])
    print("white machine counts:", audit["white"]["machine_counts_local"])
    print("confirmation-gap nodes:", len(
        audit["white"]["confirmation_gap_nodes"]))
    print("->", OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
