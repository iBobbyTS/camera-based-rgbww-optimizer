"""GUIDE12 offline deterministic corrections from retained GUIDE11 data.

Three read-only recomputations prescribed by CODEX_GUIDE12_IMPLEMENTATION_PROMPT:

A. W2 fresh pairing: the 49 same-candidate Ray/strip pairs that the GUIDE11
   selection skipped, with signed strip-minus-Ray errors, E against the fresh
   reference, the 9 adopted commands' historical-vs-fresh comparison, and the
   per-node command-difference rank diagnostics.
B. Native raw-rail audit: block_06 plane plateau/ceiling status for every
   retained patch-statistics file, separating definitive plateaus from
   conservative max-at-ceiling flags the historical stats can still prove.
C. W8 signed-unit rebuild: the white final report with per-component signed
   physical-unit errors, tolerances and separately-derived absolute
   normalized errors; the old artifact stays untouched.

No device, camera, network or RAW-mutating work; CR3s are only read to fetch
the per-frame rgb_xyz_matrix exactly as the GUIDE11 analyzer did.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

import numpy as np

from camera_based_rgbww_optimizer.optimization import guide12
from camera_based_rgbww_optimizer.optimization import white_calibration_common as common

BASE = Path("D:/rgbww-optimizer")
G11 = BASE / "guide11"
DAY = "20260929"

W2_ROOTS = [
    G11 / "guide11-w2" / "formal-w2-20260922",
    G11 / "guide11-w2" / "formal-w2-20260923-suffix",
]
W2_SELECTION = G11 / "guide11-w2" / "derived" / "w2-selection-20260923.json"
W1_TARGETS = G11 / "guide11-n1" / "derived" / "w1-frozen-targets-20260922.json"
FROZEN_LUT = G11 / "guide11-w3" / "frozen-lut-20260923.json"
OLD_W8 = BASE / "guide10" / "guide10-white70-w8-final" / "guide10-white70-final-artifact.json"
OLD_REPORT = G11 / "guide11-w8" / "guide11-white-final-report-20260928.json"
N1_ANALYSIS = G11 / "guide11-n1" / "derived" / "n1-combined-analysis-20260922.json"
W4_ANALYSIS = G11 / "guide11-w4" / "derived" / "w4-protocol-analysis-20260924.json"

OUT_PAIRING = G11 / "guide11-w2" / "derived" / f"w2-fresh-pairing-audit-{DAY}.json"
OUT_RAIL = G11 / "derived" / f"raw-rail-audit-{DAY}.json"
OUT_W8 = G11 / "guide11-w8" / "derived" / f"guide11-white-final-report-signed-{DAY}.json"

CAND_RE = re.compile(r"candidate(\d+)$")


def resolve_local(recorded: str) -> Path:
    """Map a recorded (possibly pre-reorg or macOS) data path to D-drive now."""
    text = str(recorded).replace("\\", "/")
    for prefix in ("/Volumes/4T/temp/rgbww-optimizer/", "/Volumes/4T/temp/rgbww-optimizer"):
        if text.startswith(prefix):
            text = "D:/rgbww-optimizer/" + text[len(prefix):].lstrip("/")
            break
    candidate = Path(text)
    if candidate.is_file():
        return candidate
    name = candidate.name
    for group in ("guide11", "guide10", "guide9", "foundations"):
        for hit in (BASE / group).rglob(name):
            if hit.is_file():
                return hit
    return candidate


def load_rows(root: Path) -> list[dict]:
    return [
        json.loads(line)
        for line in (root / "captures.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


_MATRIX_CACHE: dict[str, object] = {}


def white_point_of(root: Path, capture_id: str) -> dict[str, float]:
    stats = json.loads(
        (root / "measurements" / f"{capture_id}.patch-statistics.json").read_text(
            encoding="utf-8"
        )
    )
    block = next(p for p in stats["patches"] if p.get("index") == 6)
    planes = {
        plane: float(block["planes"][plane]["statistics"]["normalized_per_second"]["trimmed_mean"])
        for plane in ("R", "G1", "G2", "B")
    }
    g_mean = 0.5 * (planes["G1"] + planes["G2"])
    camera_neutral = [planes["R"] / g_mean, 1.0, planes["B"] / g_mean]
    raw_path = str((next(
        r for r in load_rows(root) if str(r.get("capture_id")) == capture_id
    ).get("capture") or {}).get("saved_file", ""))
    if raw_path not in _MATRIX_CACHE:
        _MATRIX_CACHE[raw_path] = common._load_rawpy_rgb_xyz_matrix(
            resolve_local(raw_path), np
        )
    estimate = common.estimate_white_point_from_camera_neutral(
        camera_neutral, _MATRIX_CACHE[raw_path]
    )
    return {
        "cct_K": float(estimate["cct_K"]),
        "duv": float(estimate["duv"]),
        "mired": 1_000_000.0 / float(estimate["cct_K"]),
    }


def part_a_fresh_pairing() -> dict:
    targets = json.loads(W1_TARGETS.read_text(encoding="utf-8"))
    target_by_key = {(n["cct"], n["gm"]): n for n in targets["nodes"]}
    selection = json.loads(W2_SELECTION.read_text(encoding="utf-8"))

    rows: dict[tuple, dict[str, dict]] = {}
    for root in W2_ROOTS:
        capture_rows = {
            str(r["capture_id"]): r for r in load_rows(root)
        }
        for cid, row in capture_rows.items():
            step = row.get("plan_step", {})
            match = CAND_RE.search(str(step.get("capture_id", cid)))
            if not match:
                continue
            key = (int(step["target_cct"]), int(step["target_gm"]), int(match.group(1)))
            is_strip = row.get("source_id") == "strip"
            step_command = step.get("command") or {}
            command = (
                {k: int(v) for k, v in step_command.items()}
                if is_strip and step_command else None
            )
            rows.setdefault(key[:2], {}).setdefault((key[2], row.get("source_id")), {
                "capture_id": cid,
                "root": root.name,
                "command": command,
                "white_point": white_point_of(root, cid),
            })

    pairs = []
    for node_key in sorted(rows):
        node = rows[node_key]
        tol = target_by_key[node_key]["tolerances"]
        frozen_target = target_by_key[node_key]["ray_target"]
        for cand_index in sorted({c for c, _ in node}):
            strip = node.get((cand_index, "strip"))
            ray = node.get((cand_index, "ray"))
            entry: dict = {
                "cct": node_key[0], "gm": node_key[1], "candidate_index": cand_index,
                "strip_capture_id": strip["capture_id"] if strip else None,
                "ray_capture_id": ray["capture_id"] if ray else None,
                "command": strip["command"] if strip else None,
            }
            if strip and ray:
                fresh = guide12.signed_white_errors(strip["white_point"], ray["white_point"], tol)
                historical = guide12.signed_white_errors(
                    strip["white_point"], frozen_target, tol
                )
                entry.update({
                    "status": "paired",
                    "strip_white_point": strip["white_point"],
                    "fresh_ray_white_point": ray["white_point"],
                    "signed_vs_fresh_ray": fresh["components"],
                    "E_vs_fresh_ray": fresh["E_normalized"],
                    "signed_vs_historical_target": historical["components"],
                    "E_vs_historical_target": historical["E_normalized"],
                })
            else:
                entry["status"] = "unpaired"
            pairs.append(entry)

    # Adopted commands: LUT nodes sourced from the W2 selection.
    lut = json.loads(FROZEN_LUT.read_text(encoding="utf-8"))
    adopted = []
    for node in lut["nodes"]:
        if not str(node.get("source", "")).startswith("w2_selected"):
            continue
        key = (int(node["cct"]), int(node["gm"]))
        matching = [
            p for p in pairs
            if (p["cct"], p["gm"]) == key and p.get("command") == node["command"]
        ]
        pair = matching[0] if matching else None
        adopted.append({
            "cct": key[0], "gm": key[1],
            "command": node["command"],
            "paired_selection_frame": pair,
            "independent_confirmation_status": "not_acquired",
        })

    # Command-difference rank diagnostics per reviewed node.
    diagnostics = []
    for node_key in sorted(rows):
        node = rows[node_key]
        commands = {}
        for (cand_index, source), obs in node.items():
            if source == "strip" and obs["command"]:
                commands.setdefault(cand_index, obs["command"])
        ordered = [commands[i] for i in sorted(commands) if i in commands]
        names = ("cw", "ww", "r", "g", "b")
        if len(ordered) < 2:
            rank, singulars, delta_rows = None, [], []
        else:
            base = np.array([float(ordered[0][n]) for n in names])
            delta_rows = [
                (np.array([float(c[n]) for n in names]) - base).tolist() for c in ordered[1:]
            ]
            matrix = np.asarray(delta_rows)
            rank = int(np.linalg.matrix_rank(matrix))
            singulars = [float(v) for v in np.linalg.svd(matrix, compute_uv=False)]
        diagnostics.append({
            "cct": node_key[0], "gm": node_key[1],
            "distinct_strip_commands": len(ordered),
            "command_delta_rank": rank,
            "command_delta_singular_values": singulars,
            "note": (
                "rank over candidate command differences vs candidate0; rank 1 means "
                "only one command direction was measured at this node"
            ),
        })

    artifact = {
        "schema": "guide12_w2_fresh_pairing_audit_v1",
        "pair_count": sum(1 for p in pairs if p["status"] == "paired"),
        "strip_frames": sum(1 for p in pairs if p.get("strip_capture_id")),
        "ray_frames": sum(1 for p in pairs if p.get("ray_capture_id")),
        "nodes": [
            {
                "cct": key[0], "gm": key[1],
                "pairs": [p for p in pairs if (p["cct"], p["gm"]) == key],
            }
            for key in sorted({(p["cct"], p["gm"]) for p in pairs})
        ],
        "adopted_commands_fresh_vs_historical": adopted,
        "command_delta_rank_diagnostics": diagnostics,
        "sign_convention": "strip_minus_reference",
        "note": (
            "Corrected GUIDE11 selection defect: Ray rows are no longer skipped. "
            "E_vs_fresh_ray uses the same-candidate same-run Ray observation; "
            "E_vs_historical_target reproduces the old (wrong-reference) gate."
        ),
        "steady_claim": False,
    }
    OUT_PAIRING.parent.mkdir(parents=True, exist_ok=True)
    OUT_PAIRING.write_text(json.dumps(artifact, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return artifact


def part_b_raw_rail_audit() -> dict:
    # Scope: the measurement roots that feed current GUIDE11/12 analyses
    # (guide11 stage roots plus the guide9 HSI/white anchors reused by C3/C4).
    # guide10-era roots are historical ledger inputs whose signed errors enter
    # reports as values, not as GUIDE12 derivative inputs; excluded here.
    audit_roots = []
    for group in ("guide11", "guide9"):
        for measurements in sorted((BASE / group).rglob("measurements")):
            if not any(measurements.glob("*.patch-statistics.json")):
                continue
            audit_roots.append(measurements.parent)
    frames = []
    summary_roots = []
    for root in audit_roots:
        root_frames = []
        for stats_path in sorted(root.joinpath("measurements").glob("*.patch-statistics.json")):
            stats = json.loads(stats_path.read_text(encoding="utf-8"))
            block = next(
                (p for p in stats["patches"] if p.get("index") == 6), None
            )
            if block is None:
                continue
            planes_out = {}
            worst = "clean"
            for plane, blk in sorted(block["planes"].items()):
                rc = blk["statistics"]["raw_code"]
                wl = float(blk["cfa"]["effective_white_level"])
                minimum, maximum, variance = (
                    float(rc["minimum"]), float(rc["maximum"]), float(rc["variance"])
                )
                plateau = minimum >= wl - 2.0 and variance == 0.0
                at_ceiling = maximum >= wl - 2.0
                status = "plateau" if plateau else ("max_at_protective_ceiling" if at_ceiling else "clean")
                planes_out[plane] = {
                    "effective_white_level": wl,
                    "raw_code_min": minimum, "raw_code_max": maximum,
                    "raw_code_variance": variance,
                    "old_clipped_fraction": blk["metrics"].get("clipped_fraction"),
                    "old_quality_status": blk["quality"]["status"],
                    "rail_status": status,
                }
                if status == "plateau":
                    worst = "plateau"
                elif status == "max_at_protective_ceiling" and worst != "plateau":
                    worst = "max_at_protective_ceiling"
            frame = {
                "root": str(root.relative_to(BASE)),
                "capture_id": stats_path.name.split(".patch-statistics.json")[0],
                "block_06_frame_class": worst,
                "planes": planes_out,
            }
            frame["old_gate_mismatch"] = (
                worst == "plateau"
                and all(p["old_quality_status"] == "accepted" for p in planes_out.values())
            )
            frames.append(frame)
            root_frames.append(frame)
        summary_roots.append({
            "root": str(root.relative_to(BASE)),
            "frames": len(root_frames),
            "plateau_frames": sum(1 for f in root_frames if f["block_06_frame_class"] == "plateau"),
            "ceiling_flagged_frames": sum(
                1 for f in root_frames if f["block_06_frame_class"] == "max_at_protective_ceiling"
            ),
        })
    artifact = {
        "schema": "guide12_raw_rail_audit_v1",
        "rail_rule": (
            "plateau = raw_code variance 0 with min >= effective_white_level - 2 DN; "
            "max_at_protective_ceiling = max >= effective_white_level - 2 DN with "
            "variance > 0. Historical patch statistics do not retain the near-rail "
            "pixel fraction, so partial contamination cannot be recomputed; the "
            "conservative ceiling flag is the strongest available statement."
        ),
        "frame_count": len(frames),
        "plateau_frame_count": sum(1 for f in frames if f["block_06_frame_class"] == "plateau"),
        "ceiling_flagged_frame_count": sum(
            1 for f in frames if f["block_06_frame_class"] == "max_at_protective_ceiling"
        ),
        "old_gate_mismatch_count": sum(1 for f in frames if f["old_gate_mismatch"]),
        "roots": summary_roots,
        "scope_note": (
            "guide11 and guide9 measurement roots (current-stage analysis inputs); "
            "guide10-era roots excluded: their W6 errors enter reports as signed "
            "historical values, not as GUIDE12 derivative inputs"
        ),
        "quantitative_ineligible_frames": [
            {"root": f["root"], "capture_id": f["capture_id"]}
            for f in frames if f["block_06_frame_class"] == "plateau"
        ],
        "frames": frames,
        "note": (
            "Read-only audit of retained patch statistics; no RAW decoded, no "
            "historical file modified. Plateau frames are excluded from GUIDE12 "
            "derivative/selection/variance inputs; their measurements and failure "
            "identity are retained here."
        ),
    }
    OUT_RAIL.parent.mkdir(parents=True, exist_ok=True)
    OUT_RAIL.write_text(json.dumps(artifact, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return artifact


def part_c_signed_w8(pairing: dict) -> dict:
    lut = json.loads(FROZEN_LUT.read_text(encoding="utf-8"))
    targets = json.loads(W1_TARGETS.read_text(encoding="utf-8"))
    target_by_key = {(n["cct"], n["gm"]): n for n in targets["nodes"]}
    w6 = json.loads(OLD_W8.read_text(encoding="utf-8"))
    w6_by_key = {(int(r["cct"]), int(r["gm"])): r for r in w6["canonical_lut"]}
    old_report = json.loads(OLD_REPORT.read_text(encoding="utf-8"))
    old_nodes = {(n["cct"], n["gm"]): n for n in old_report["nodes"]}
    adopted_by_key = {
        (a["cct"], a["gm"]): a for a in pairing["adopted_commands_fresh_vs_historical"]
    }

    nodes_out = []
    within_fresh = 0
    identity_counts: dict[str, int] = {}
    for row in lut["nodes"]:
        key = (int(row["cct"]), int(row["gm"]))
        target = target_by_key.get(key)
        tol = (target or {}).get("tolerances") or {}
        is_w2 = str(row.get("source", "")).startswith("w2_selected")
        if is_w2 and key in adopted_by_key:
            adopted_row = adopted_by_key[key]
            pair = adopted_row.get("paired_selection_frame") or {}
            evidence = {
                "identity": "w2_selection_frame_vs_same_candidate_fresh_ray",
                "independent_confirmation": "not_acquired",
                "selection_frame_vs_historical_target": pair.get("signed_vs_historical_target"),
                "E_vs_historical_target": pair.get("E_vs_historical_target"),
                "signed_vs_fresh_ray": pair.get("signed_vs_fresh_ray"),
                "E_vs_fresh_ray": pair.get("E_vs_fresh_ray"),
                "within_tolerance_vs_fresh_ray": (
                    None if pair.get("E_vs_fresh_ray") is None
                    else bool(pair["E_vs_fresh_ray"] < 1.0)
                ),
                "legacy_note": (
                    "old report stored e_gates (dimensionless absolute) in "
                    "e_cct_K/e_mired/e_duv fields; superseded by signed units here"
                ),
            }
            if evidence["within_tolerance_vs_fresh_ray"]:
                within_fresh += 1
            identity = evidence["identity"]
        elif key in w6_by_key:
            w6row = w6_by_key[key]
            components = {}
            for err_name, tol_name, unit in (
                ("cct_error_K", "cct_K", "K"),
                ("mired_error", "mired", "mired"),
                ("duv_error", "duv", "duv"),
            ):
                err = w6row.get(err_name)
                tolerance = tol.get(tol_name)
                components[tol_name] = {
                    "error_signed": None if err is None else float(err),
                    "unit": unit,
                    "tolerance": tolerance,
                    "abs_normalized_error": (
                        None if err is None or tolerance is None
                        else abs(float(err)) / float(tolerance)
                    ),
                }
            identity = "w6_single_observation"
            evidence = {
                "identity": identity,
                "signed_components": components,
                "within_tolerance_point_estimate": w6row.get("status") == "pass",
                "certification": "W6 single FAST observation; signed errors as historically computed",
            }
        else:
            identity = "no_evidence"
            evidence = {
                "identity": identity,
                "within_tolerance_point_estimate": False,
                "certification": "no measured strip observation retained for this node",
            }
        identity_counts[identity] = identity_counts.get(identity, 0) + 1
        old = old_nodes.get(key, {})
        nodes_out.append({
            "cct": key[0], "gm": key[1],
            "command": row["command"],
            "command_source": row["source"],
            "tolerances": tol,
            "error_evidence": evidence,
            "interval_evidence": old.get("interval_evidence"),
            "protocol_deviation": old.get("protocol_deviation"),
            "interpolation_applicability": old.get("interpolation_applicability"),
        })

    report = {
        "schema": "guide11_white_final_report_v2_signed_units",
        "stage": "GUIDE12-OFFLINE-CORRECTION",
        "correction_note": (
            "GUIDE12 W8 unit fix: the W2 branch previously assigned dimensionless "
            "absolute e_gates into e_cct_K/e_mired/e_duv. This rebuild stores signed "
            "physical-unit errors (strip_minus_reference), their tolerances, and "
            "separately derived abs_normalized_error. The 2026-09-28 artifact is "
            "retained read-only as the historical record."
        ),
        "source_artifacts": {
            "lut": str(FROZEN_LUT),
            "targets": str(W1_TARGETS),
            "w2_selection": str(W2_SELECTION),
            "fresh_pairing_audit": str(OUT_PAIRING),
            "w6_historical": str(OLD_W8),
            "superseded_report": str(OLD_REPORT),
        },
        "node_count": len(nodes_out),
        "identity_counts": identity_counts,
        "w2_adopted_within_tolerance_vs_fresh_ray": within_fresh,
        "sign_convention": "strip_minus_reference",
        "nodes": nodes_out,
        "steady_claim": False,
    }
    OUT_W8.parent.mkdir(parents=True, exist_ok=True)
    OUT_W8.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return report


def main() -> None:
    pairing = part_a_fresh_pairing()
    print("A pairing:", pairing["pair_count"], "pairs |",
          pairing["strip_frames"], "strip |", pairing["ray_frames"], "ray")
    for a in pairing["adopted_commands_fresh_vs_historical"]:
        pair = a.get("paired_selection_frame") or {}
        print(
            f"  {a['cct']}/{a['gm']}: E_hist={pair.get('E_vs_historical_target')}"
            f" E_fresh={pair.get('E_vs_fresh_ray')}"
        )
    ranks = [d["command_delta_rank"] for d in pairing["command_delta_rank_diagnostics"]]
    print("A ranks: nodes", len(ranks), "| rank-1 nodes:",
          sum(1 for r in ranks if r == 1), "| max rank:", max(r for r in ranks if r is not None))
    rail = part_b_raw_rail_audit()
    print("B rail:", rail["frame_count"], "frames |", rail["plateau_frame_count"],
          "plateau |", rail["ceiling_flagged_frame_count"], "ceiling-flagged |",
          rail["old_gate_mismatch_count"], "old-gate mismatches")
    report = part_c_signed_w8(pairing)
    print("C w8:", report["node_count"], "nodes |", report["identity_counts"],
          "| w2 within vs fresh:", report["w2_adopted_within_tolerance_vs_fresh_ray"])
    print("->", OUT_PAIRING)
    print("->", OUT_RAIL)
    print("->", OUT_W8)


if __name__ == "__main__":
    main()
