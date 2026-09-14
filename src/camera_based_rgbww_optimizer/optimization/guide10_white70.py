from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
from typing import Any, Mapping, Sequence


CHANNELS = ("cw", "ww", "r", "g", "b")


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _active_face(command: Mapping[str, Any]) -> tuple[str, ...]:
    return tuple(name for name in CHANNELS if int(command[name]) >= 4095)


def _distance(a: tuple[float, float], b: tuple[float, float], spans: tuple[float, float]) -> float:
    dm = (a[0] - b[0]) / spans[0]
    dg = (a[1] - b[1]) / spans[1]
    return math.hypot(dm, dg)


def build_guide10_white70_candidates(
    baseline: Mapping[str, Any],
    evidence: Sequence[tuple[str, Mapping[str, Any]]],
    confirmation: Mapping[str, Any],
) -> dict[str, Any]:
    baseline_nodes = {(int(row["cct"]), int(row["gm"])): row for row in baseline["nodes"]}
    if len(baseline_nodes) != 70:
        raise ValueError("GUIDE10 white70 requires exactly 70 baseline nodes")

    observations: dict[tuple[int, int], list[dict[str, Any]]] = {key: [] for key in baseline_nodes}
    for order, (source, analysis) in enumerate(evidence):
        for row in analysis.get("nodes", ()):
            key = (int(row["cct"]), int(row["gm"]))
            if key in observations:
                observations[key].append({"order": order, "source": source, "row": row})

    confirm_key = (1800, 100)
    confirm_observation = confirmation["confirmation_observations"][0]
    observations[confirm_key].append({
        "order": len(evidence),
        "source": str(confirmation.get("run_root", "GUIDE10 confirmation")),
        "row": {
            "cct": 1800,
            "gm": 100,
            "status": "pass",
            "strip_command": confirmation["selected_command"],
            "gates": confirm_observation["gates"],
            "cct_error_K": confirm_observation["cct_error_K"],
            "mired_error": confirm_observation["mired_error"],
            "duv_error": confirm_observation["duv_error"],
        },
    })

    canonical = []
    for key, base in sorted(baseline_nodes.items()):
        candidates = observations[key]
        passing = [item for item in candidates if item["row"].get("status") == "pass"]
        selected = max(passing or candidates, key=lambda item: item["order"]) if candidates else None
        row = selected["row"] if selected else base
        command = {name: int(row["strip_command"][name]) for name in CHANNELS}
        status = "strict_equivalent" if row.get("status") == "pass" else "stable_best"
        canonical.append({
            "cct": key[0],
            "gm": key[1],
            "status": status,
            "command": command,
            "active_face": list(_active_face(command)),
            "errors": {
                "cct_K": float(row["cct_error_K"]),
                "mired": float(row["mired_error"]),
                "duv": float(row["duv_error"]),
            },
            "source": selected["source"] if selected else "baseline",
        })

    anchor_rows = []
    for row in canonical:
        key = (row["cct"], row["gm"])
        base_command = baseline_nodes[key]["strip_command"]
        if row["status"] == "strict_equivalent":
            anchor_rows.append({
                "coordinate": (1_000_000.0 / row["cct"], float(row["gm"])),
                "face": tuple(row["active_face"]),
                "delta": {name: row["command"][name] - int(base_command[name]) for name in CHANNELS},
            })

    mired_values = [1_000_000.0 / key[0] for key in baseline_nodes]
    gm_values = [float(key[1]) for key in baseline_nodes]
    spans = (max(mired_values) - min(mired_values), max(gm_values) - min(gm_values))
    output_nodes = []
    for row in canonical:
        key = (row["cct"], row["gm"])
        if row["status"] == "strict_equivalent":
            output_nodes.append({**row, "candidate_command": dict(row["command"]), "field_action": "retain_strict"})
            continue
        point = (1_000_000.0 / row["cct"], float(row["gm"]))
        same_face = [anchor for anchor in anchor_rows if anchor["face"] == tuple(row["active_face"])]
        bounded = same_face and (
            min(a["coordinate"][0] for a in same_face) <= point[0] <= max(a["coordinate"][0] for a in same_face)
            and min(a["coordinate"][1] for a in same_face) <= point[1] <= max(a["coordinate"][1] for a in same_face)
        )
        if not bounded:
            output_nodes.append({**row, "candidate_command": dict(row["command"]), "field_action": "retain_no_bounded_anchor"})
            continue
        nearest = sorted(same_face, key=lambda a: _distance(a["coordinate"], point, spans))[:4]
        distances = [_distance(a["coordinate"], point, spans) for a in nearest]
        weights = [1.0 / max(value, 1e-9) for value in distances]
        candidate = {}
        for name in CHANNELS:
            delta = sum(weight * anchor["delta"][name] for weight, anchor in zip(weights, nearest)) / sum(weights)
            candidate[name] = max(0, min(4095, int(round(row["command"][name] + delta))))
        output_nodes.append({**row, "candidate_command": candidate, "field_action": "same_face_bounded_idw"})

    return {
        "schema": "guide10_white70_canonical_and_correction_field_v1",
        "status": "candidate_generation_complete",
        "node_count": len(output_nodes),
        "strict_equivalent_count": sum(row["status"] == "strict_equivalent" for row in output_nodes),
        "stable_best_count": sum(row["status"] == "stable_best" for row in output_nodes),
        "field_adjusted_count": sum(row["field_action"] == "same_face_bounded_idw" for row in output_nodes),
        "model": "inverse-distance weighted low-order field in target mired x GM, piecewise by active face",
        "extrapolation": "prohibited; canonical command retained outside same-face anchor bounds",
        "role": "candidate_generation_only_requires_direct_validation",
        "nodes": output_nodes,
        "next": "GUIDE10_WHITE70_FAST_VALIDATION_ROUND1",
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build GUIDE10 canonical white70 and one-time correction-field candidates.")
    parser.add_argument("--baseline", type=Path, required=True)
    parser.add_argument("--evidence", type=Path, action="append", default=[])
    parser.add_argument("--confirmation", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    baseline = json.loads(args.baseline.read_text(encoding="utf-8"))
    evidence = [(str(path.resolve()), json.loads(path.read_text(encoding="utf-8"))) for path in args.evidence]
    confirmation = json.loads(args.confirmation.read_text(encoding="utf-8"))
    result = build_guide10_white70_candidates(baseline, evidence, confirmation)
    result["inputs"] = {
        "baseline": {"path": str(args.baseline.resolve()), "sha256": _sha256(args.baseline)},
        "evidence": [{"path": str(path.resolve()), "sha256": _sha256(path)} for path in args.evidence],
        "confirmation": {"path": str(args.confirmation.resolve()), "sha256": _sha256(args.confirmation)},
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({key: result[key] for key in ("status", "node_count", "strict_equivalent_count", "stable_best_count", "field_adjusted_count", "next")}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
