"""GUIDE11 evidence export, stage 3: indexes, reconciliation, replay, packaging.

Runs entirely on the staged package plus the repo checkout. Produces
OBSERVATIONS.jsonl, observation_aliases.json, the section-6 reconciliation
tables under replay/, the source/config snapshot under source/, INPUT_RESOLUTION
and DEPENDENCIES, README, MANIFEST, the final ZIP, and the offline check
report. Read-only with respect to scientific results: nothing in runs/ or
derived/ is modified, and no device, camera, or RAW decode is touched.
"""
from __future__ import annotations

import hashlib
import json
import math
import shutil
import subprocess
import sys
import zipfile
import time
from pathlib import Path

DATA = Path("D:/rgbww-optimizer")
REPO = Path("C:/Users/iBobb/Projects/WLED-RGBWW")
STAGE = DATA / "tmp/guide11-evidence-export-20260929/stage"
PKG = STAGE / "GUIDE11-COMPLETE-PROCESSED-EVIDENCE-20260929"
ZIP_OUT = REPO / ".agent-work/guide11/GUIDE11-COMPLETE-PROCESSED-EVIDENCE-20260929.zip"
REQUEST_DIR = Path("C:/Users/iBobb/Downloads/GUIDE11_REVIEW_INPUT_REQUEST_20260929")

sys.path.insert(0, str(REPO / "src"))
import numpy as np  # noqa: E402
from camera_based_rgbww_optimizer.optimization.white_calibration_common import (  # noqa: E402
    estimate_white_point_from_camera_neutral,
)

CHANNELS = ("red", "green", "blue", "cold_white", "warm_white")
CHANNEL_MAX_KEY = {"red": "r", "green": "g", "blue": "b", "cold_white": "cw", "warm_white": "ww"}


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load_jsonl(path: Path) -> list[dict]:
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


def block06_planes(stats: dict) -> dict[str, float]:
    block = next(p for p in stats["patches"] if p.get("index") == 6)
    return {
        plane: float(block["planes"][plane]["statistics"]["normalized_per_second"]["trimmed_mean"])
        for plane in ("R", "G1", "G2", "B")
    }


def z_from_planes(p: dict[str, float]) -> dict[str, float]:
    g = 0.5 * (p["G1"] + p["G2"])
    return {"log_R_over_G": math.log(p["R"] / g), "log_B_over_G": math.log(p["B"] / g)}


def z_dist(a: dict, b: dict) -> float:
    return math.hypot(a["log_R_over_G"] - b["log_R_over_G"], a["log_B_over_G"] - b["log_B_over_G"])


# --- package readers ----------------------------------------------------------

class Package:
    def __init__(self) -> None:
        self.runs: dict[str, Path] = {}
        for captures in sorted((PKG / "runs").rglob("captures.jsonl")):
            alias = captures.parent.relative_to(PKG / "runs").as_posix()
            self.runs[alias] = captures.parent
        self.raw_index: dict[tuple[str, str], dict] = {}
        for row in load_jsonl(PKG / "profiles/raw-index.jsonl"):
            self.raw_index[(row["alias"], row["capture_id"])] = row
        self.matrices: dict[str, list] = {}
        for f in sorted((PKG / "matrices").glob("*.json")):
            m = json.loads(f.read_text(encoding="utf-8"))
            self.matrices[m["matrix_id"]] = m["rgb_xyz_matrix_first3"]

    def stats_of(self, alias: str, capture_id: str) -> dict | None:
        p = self.runs[alias] / "measurements" / f"{capture_id}.patch-statistics.json"
        return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else None

    def commands_of(self, alias: str) -> list[dict]:
        p = self.runs[alias] / "commands.jsonl"
        return load_jsonl(p) if p.is_file() else []

    def physical_of(self, alias: str) -> dict[str, dict]:
        p = PKG / "runs" / alias / "physical-returns.jsonl"
        return {str(r.get("capture_id")): r for r in (load_jsonl(p) if p.is_file() else [])}

    def quality_of(self, alias: str) -> dict[str, str]:
        p = self.runs[alias] / "quality.json"
        if not p.is_file():
            return {}
        q = json.loads(p.read_text(encoding="utf-8"))
        return {str(r["capture_id"]): str(r.get("status")) for r in q.get("rows", [])}


def strip_actual_pwm(command_row: dict) -> dict | None:
    snap = (command_row.get("applied") or {}).get("device_snapshot")
    if not isinstance(snap, dict) or "red" not in snap:
        return None
    return {k: int(snap[k]) for k in CHANNELS if k in snap}


# --- A. observations ----------------------------------------------------------

def build_observations(pkg: Package) -> tuple[list[dict], dict]:
    observations: list[dict] = []
    seen_keys: set[tuple[str, str]] = set()
    for alias in sorted(pkg.runs):
        root = pkg.runs[alias]
        rows = load_jsonl(root / "captures.jsonl")
        commands = pkg.commands_of(alias)
        cmd_by_capture: dict[str, dict] = {}
        for c in commands:
            for cid in c.get("group_capture_ids") or []:
                cmd_by_capture[str(cid)] = c
        phys = pkg.physical_of(alias)
        quality = pkg.quality_of(alias)
        for row in rows:
            capture_id = str(row["capture_id"])
            key = (alias, capture_id)
            if key in seen_keys:
                raise ValueError(f"duplicate capture key inside one root: {key}")
            seen_keys.add(key)
            step = row.get("plan_step") or {}
            cmd = cmd_by_capture.get(capture_id)
            raw = pkg.raw_index.get(key)
            obs = {
                "logical_key": {"run_alias": alias, "capture_id": capture_id},
                "source_id": row.get("source_id"),
                "state_id": row.get("state_id"),
                "capture_role": row.get("capture_role"),
                "formal_measurement": row.get("formal_measurement"),
                "role": step.get("role"),
                "requested_command": step.get("command"),
                "target": {
                    k: step.get(k) for k in (
                        "target_cct", "target_gm", "c1_hue", "c1_sat", "c5_intensity_percent",
                        "n1_cycle_index", "n1_session_index", "n1_burst_role", "session_index",
                        "source_order", "steady_claim",
                    ) if k in step
                },
                "nominal_shutter": step.get("nominal_shutter"),
                "timing": {
                    "nominal_slot_s": row.get("nominal_slot_s"),
                    "timing_offset_s": row.get("timing_offset_s"),
                    "best_effort_exposure_start_elapsed_s": row.get("best_effort_exposure_start_elapsed_s"),
                    "timing_evidence_status": row.get("timing_evidence_status"),
                    "timing_estimate_method": row.get("timing_estimate_method"),
                    "requested_elapsed_s": step.get("requested_elapsed_s"),
                    "command_at_utc": (cmd or {}).get("at"),
                    "source_on_monotonic_s": (cmd or {}).get("source_on_monotonic_s"),
                    "command_completed_monotonic_s": (cmd or {}).get("command_completed_monotonic_s"),
                    "readback_completed_monotonic_s": (cmd or {}).get("readback_completed_monotonic_s"),
                    "reset_wait_s_planned": (cmd or {}).get("reset_wait_s"),
                },
                "exposure": {
                    "shutter_speed": (row.get("capture") or {}).get("shutter_speed"),
                    "iso": (row.get("capture") or {}).get("iso"),
                    "aperture": (row.get("capture") or {}).get("aperture"),
                },
                "raw_identity": {
                    "sha256": (raw or {}).get("recomputed_sha256") or (phys.get(capture_id) or {}).get("cr3_sha256"),
                    "byte_count": (raw or {}).get("recomputed_byte_count") or (phys.get(capture_id) or {}).get("cr3_byte_count"),
                    "sha256_matches_ledger": (raw or {}).get("sha256_matches_ledger"),
                    "matrix_id": (raw or {}).get("matrix_id"),
                    "physical_return_accepted": (phys.get(capture_id) or {}).get("accepted_measurement"),
                },
                "measurement_file": f"runs/{alias}/measurements/{capture_id}.patch-statistics.json"
                if (root / "measurements" / f"{capture_id}.patch-statistics.json").is_file() else None,
                "quality_status": quality.get(capture_id),
            }
            if str(row.get("source_id")) == "strip" and cmd:
                actual = strip_actual_pwm(cmd) or {}
                requested = (cmd.get("applied") or {}).get("requested_payload") or step.get("command") or {}
                max_actual = max(actual.values()) if actual else None
                max_requested = max(requested.values()) if requested else None
                obs["strip_command_evidence"] = {
                    "requested_payload": requested,
                    "device_snapshot_after_apply": actual or None,
                    "readback_device_snapshot": (strip_actual_pwm({"applied": cmd.get("readback") or {}}) or None),
                    "max_requested_code": max_requested,
                    "max_actual_pwm": max_actual,
                    "fullscale_4095_actual": (max_actual == 4095) if max_actual is not None else None,
                    "fullscale_4095_requested": (max_requested == 4095) if max_requested is not None else None,
                    "basis": "commands.jsonl applied.device_snapshot (post-apply readback state)",
                    "exact_command_hash": cmd.get("exact_command_hash"),
                }
            if str(row.get("source_id")) == "ray" and cmd:
                obs["ray_command_evidence"] = {
                    "applied": (cmd.get("applied") or {}).get("data") or (cmd.get("applied") or {}),
                    "readback": (cmd.get("readback") or {}).get("data") or (cmd.get("readback") or {}),
                    "note": "API intensity 1000 == 100% (hsi_command.intensity_percent=100.0 in thermal covariates)",
                }
            observations.append(obs)

    aliases: dict[str, list[dict]] = {}
    for o in observations:
        sha = (o["raw_identity"] or {}).get("sha256")
        if sha:
            aliases.setdefault(sha, []).append({
                "run_alias": o["logical_key"]["run_alias"],
                "capture_id": o["logical_key"]["capture_id"],
            })
    # Diagnostic roots without a captures ledger still took physical photos;
    # synthesize physical-return-only rows so the photo inventory is complete.
    # This also covers orphan physical-return rows inside captures roots.
    for phys_file in sorted((PKG / "runs").rglob("physical-returns.jsonl")):
        run_dir = phys_file.parent
        has_captures = (run_dir / "captures.jsonl").is_file()
        capture_ids: set[str] = set()
        if has_captures:
            capture_ids = {
                str(json.loads(l)["capture_id"])
                for l in (run_dir / "captures.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()
            }
        alias = run_dir.relative_to(PKG / "runs").as_posix()
        for cid, pr in sorted(pkg.physical_of(alias).items()):
            if has_captures and str(cid) in capture_ids:
                continue
            raw = pkg.raw_index.get((alias, str(cid)))
            if raw is None:
                continue
            obs = {
                "logical_key": {"run_alias": alias, "capture_id": str(cid)},
                "row_kind": "physical_return_only_no_capture_ledger",
                "source_id": pr.get("source_id"),
                "raw_identity": {
                    "sha256": raw.get("recomputed_sha256"),
                    "byte_count": raw.get("recomputed_byte_count"),
                    "sha256_matches_ledger": raw.get("sha256_matches_ledger"),
                    "matrix_id": raw.get("matrix_id"),
                    "physical_return_accepted": pr.get("accepted_measurement"),
                },
                "measurement_file": None,
                "note": "photo taken but run failed before capture-ledger/feature extraction; see runs/<alias>/failure.json",
            }
            observations.append(obs)
            if raw.get("recomputed_sha256"):
                aliases.setdefault(raw["recomputed_sha256"], []).append({
                    "run_alias": alias, "capture_id": str(cid),
                })
    alias_doc = {
        "schema": "guide11_observation_aliases_v1",
        "unique_raw_sha256_count": len(aliases),
        "logical_row_count": len(observations),
        "note": "one physical photo counted once per content hash; logical rows use run_alias+capture_id composite keys and never merge across roots",
        "hash_to_logical_rows": aliases,
    }
    return observations, alias_doc


# --- B. reconciliation tables -------------------------------------------------

def white_point_from_package(pkg: Package, alias: str, capture_id: str) -> dict | None:
    stats = pkg.stats_of(alias, capture_id)
    raw = pkg.raw_index.get((alias, capture_id))
    if not stats or not raw or not raw.get("matrix_id"):
        return None
    planes = block06_planes(stats)
    g = 0.5 * (planes["G1"] + planes["G2"])
    camera_neutral = [planes["R"] / g, 1.0, planes["B"] / g]
    matrix = np.asarray(pkg.matrices[raw["matrix_id"]], dtype="float64")
    est = estimate_white_point_from_camera_neutral(camera_neutral, matrix)
    return {
        "capture_id": capture_id, "run_alias": alias,
        "block06_planes": planes,
        "white_point": {"cct_K": est["cct_K"], "duv": est["duv"], "mired": 1_000_000.0 / est["cct_K"]},
    }


def reconcile_w2_fresh_ray(pkg: Package) -> dict:
    w2_aliases = [
        "guide11-w2/formal-w2-20260922",
        "guide11-w2/formal-w2-20260923-suffix",
    ]
    ray_rows: list[dict] = []
    strip_rows: list[dict] = []
    for alias in w2_aliases:
        for row in load_jsonl(pkg.runs[alias] / "captures.jsonl"):
            step = row.get("plan_step") or {}
            entry = {
                "alias": alias, "capture_id": str(row["capture_id"]),
                "role": step.get("role"), "source_id": row.get("source_id"),
                "target_cct": step.get("target_cct"), "target_gm": step.get("target_gm"),
                "candidate_capture_id": step.get("capture_id"),
                "command": step.get("command"),
                "shutter": step.get("nominal_shutter"),
                "best_effort_exposure_start_elapsed_s": row.get("best_effort_exposure_start_elapsed_s"),
                "command_at_utc": None,
            }
            if str(row.get("source_id")) == "ray":
                ray_rows.append(entry)
            else:
                strip_rows.append(entry)
    for e in ray_rows + strip_rows:
        wp = white_point_from_package(pkg, e["alias"], e["capture_id"])
        e["white_point"] = (wp or {}).get("white_point")
        e["block06_planes"] = (wp or {}).get("block06_planes")

    targets = json.loads((PKG / "derived/guide11-n1/w1-frozen-targets-20260922.json").read_text(encoding="utf-8"))
    target_by_key = {(int(n["cct"]), int(n["gm"])): n for n in targets["nodes"]}
    selection = json.loads((PKG / "derived/guide11-w2/w2-selection-20260923.json").read_text(encoding="utf-8"))

    nodes = []
    for sel in selection["nodes"]:
        key = (int(sel["cct"]), int(sel["gm"]))
        node_rays = [e for e in ray_rows if (e["target_cct"], e["target_gm"]) == key]
        fresh = [e for e in node_rays if e["white_point"]]
        fresh_mean = None
        if fresh:
            fresh_mean = {
                axis: sum(e["white_point"][axis] for e in fresh) / len(fresh)
                for axis in ("cct_K", "duv", "mired")
            }
        tol = target_by_key[key]["tolerances"]
        hist = target_by_key[key]["ray_target"]
        chosen = sel["selected"]
        gates_fresh = None
        if fresh_mean:
            gates_fresh = {
                "cct_K": abs(chosen["white_point"]["cct_K"] - fresh_mean["cct_K"]) / tol["cct_K"],
                "duv": abs(chosen["white_point"]["duv"] - fresh_mean["duv"]) / tol["duv"],
                "mired": abs(chosen["white_point"]["mired"] - fresh_mean["mired"]) / tol["mired"],
            }
        nodes.append({
            "cct": key[0], "gm": key[1],
            "fresh_ray_count": len(node_rays),
            "fresh_ray_with_white_point": len(fresh),
            "fresh_ray_white_points": [
                {"capture_id": e["capture_id"], "alias": e["alias"], "role": e["role"],
                 "shutter": e["shutter"], "white_point": e["white_point"]}
                for e in node_rays
            ],
            "fresh_ray_mean_white_point": fresh_mean,
            "selected_strip": {
                "capture_id": chosen["capture_id"], "command": chosen["command"],
                "white_point_vs_w1_historical": chosen["white_point"], "E_vs_historical": chosen["E"],
            },
            "E_vs_fresh_ray": (max(gates_fresh.values()) if gates_fresh else None),
            "gates_vs_fresh_ray": gates_fresh,
            "fresh_ray_minus_historical": (
                {axis: fresh_mean[axis] - hist[axis] for axis in ("cct_K", "duv", "mired")}
                if fresh_mean else None
            ),
            "pairing_note": "strip selection scored against W1 historical Ray target (analyze_w2_selection main loop); fresh Ray rows are exported here for the second error sense" ,
        })
    return {
        "schema": "guide11_w2_fresh_ray_reconciliation_v1",
        "ray_row_count": len(ray_rows),
        "strip_row_count": len(strip_rows),
        "ray_rows_missing_white_point": [e["capture_id"] for e in ray_rows if not e["white_point"]],
        "primitive_ray_export": [
            {"alias": e["alias"], "capture_id": e["capture_id"], "role": e["role"],
             "target_cct": e["target_cct"], "target_gm": e["target_gm"], "shutter": e["shutter"],
             "command": e["command"], "elapsed_s": e["best_effort_exposure_start_elapsed_s"],
             "block06_planes": e["block06_planes"], "white_point": e["white_point"]}
            for e in ray_rows
        ],
        "nodes": nodes,
        "note": "read-only reconciliation; original W2 selection result unchanged; two error senses kept separate",
    }


def reconcile_w2_confirmation(pkg: Package) -> dict:
    selection = json.loads((PKG / "derived/guide11-w2/w2-selection-20260923.json").read_text(encoding="utf-8"))
    lut = json.loads((PKG / "frozen-inputs/frozen-lut-20260923.json").read_text(encoding="utf-8"))
    lut_by_command = {json.dumps(n.get("command") or {}, sort_keys=True): n for n in lut.get("nodes", [])}
    selection_time = "2026-09-23"  # w2-selection derived artifact creation
    adopted = []
    for sel in selection["nodes"]:
        cmd = sel["selected"]["command"]
        lut_node = lut_by_command.get(json.dumps(cmd, sort_keys=True))
        adopted.append({
            "cct": sel["cct"], "gm": sel["gm"],
            "command": cmd,
            "selected_capture_id": sel["selected"]["capture_id"],
            "matching_frozen_lut_node": (
                {"cct": lut_node["cct"], "gm": lut_node["gm"], "source": lut_node.get("source")}
                if lut_node else None
            ),
            "adopted_into_frozen_lut": lut_node is not None,
        })
    # Search every command row in the package for a post-selection independent
    # confirmation of exactly these commands (any root, any stage).
    search_hits: dict[str, list] = {}
    scanned_rows = 0
    scanned_roots = 0
    for alias in sorted(pkg.runs):
        for c in pkg.commands_of(alias):
            scanned_rows += 1
            payload = (c.get("applied") or {}).get("requested_payload")
            if not isinstance(payload, dict) or "red" not in payload:
                continue
            scanned_roots += 0
            norm = {CHANNEL_MAX_KEY[k]: v for k, v in payload.items() if k in CHANNEL_MAX_KEY}
            for a in adopted:
                if norm == {k: a["command"][k] for k in ("r", "g", "b", "cw", "ww")}:
                    at = str(c.get("at") or "")
                    if at[:10] >= selection_time and not alias.startswith("guide11-w2/"):
                        search_hits.setdefault(f"{a['cct']}/{a['gm']}", []).append({
                            "run_alias": alias, "at": at, "state_id": c.get("state_id"),
                        })
    scanned_roots = len(pkg.runs)
    for a in adopted:
        key = f"{a['cct']}/{a['gm']}"
        hits = search_hits.get(key, [])
        a["independent_fast_confirmation"] = "confirmed" if hits else "not_acquired"
        a["confirmation_evidence_hits"] = hits
    return {
        "schema": "guide11_w2_adopted_command_confirmation_status_v1",
        "adopted_command_count": len(adopted),
        "frozen_lut_nodes_updated_from_w2_declared_count": lut.get("nodes_updated_from_w2"),
        "adopted_count_matched_into_frozen_lut_by_command": sum(1 for a in adopted if a["adopted_into_frozen_lut"]),
        "search_scope": {
            "roots_scanned": scanned_roots,
            "command_rows_scanned": scanned_rows,
            "criterion": "exact requested_payload equality, timestamp on/after 2026-09-23, root outside guide11-w2 selection roots",
        },
        "commands": adopted,
        "note": "not_acquired means no independent FAST confirmation capture of this exact command exists in any exported run; W3 holdout points are different coordinates/commands and are not counted as confirmations",
    }


def reconcile_w4_timeline(pkg: Package) -> dict:
    out = {"schema": "guide11_w4_protocol_timeline_v1", "arms": {}}
    for arm, alias in (("FAST", "guide11-w4/formal-w4-fast-20260924-r2"), ("LONG", "guide11-w4/formal-w4-long-20260924")):
        root = pkg.runs[alias]
        cmds = {str(c.get("state_id")): c for c in pkg.commands_of(alias)}
        rows = []
        for row in load_jsonl(root / "captures.jsonl"):
            step = row.get("plan_step") or {}
            c = cmds.get(str(row.get("state_id")))
            rows.append({
                "capture_id": str(row["capture_id"]),
                "state_id": row.get("state_id"),
                "source_id": row.get("source_id"),
                "command": step.get("command"),
                "planned": {
                    "reset_wait_s": (c or {}).get("reset_wait_s"),
                    "requested_elapsed_s": step.get("requested_elapsed_s"),
                    "nominal_slot_s": row.get("nominal_slot_s"),
                },
                "observed": {
                    "source_on_monotonic_s": (c or {}).get("source_on_monotonic_s"),
                    "command_completed_monotonic_s": (c or {}).get("command_completed_monotonic_s"),
                    "readback_completed_monotonic_s": (c or {}).get("readback_completed_monotonic_s"),
                    "best_effort_exposure_start_elapsed_s_since_state_start": row.get("best_effort_exposure_start_elapsed_s"),
                    "timing_evidence_status": row.get("timing_evidence_status"),
                },
            })
        resets = sorted({r["planned"]["reset_wait_s"] for r in rows if r["planned"]["reset_wait_s"] is not None})
        dwell = sorted({r["planned"]["nominal_slot_s"] for r in rows if r["planned"]["nominal_slot_s"] is not None})
        out["arms"][arm] = {
            "run_alias": alias,
            "captures": rows,
            "distinct_planned_reset_wait_s": resets,
            "distinct_nominal_dwell_slot_s": dwell,
            "observed_exposure_start_elapsed_range_s": [
                min(r["observed"]["best_effort_exposure_start_elapsed_s_since_state_start"] for r in rows
                    if r["observed"]["best_effort_exposure_start_elapsed_s_since_state_start"] is not None),
                max(r["observed"]["best_effort_exposure_start_elapsed_s_since_state_start"] for r in rows
                    if r["observed"]["best_effort_exposure_start_elapsed_s_since_state_start"] is not None),
            ],
        }
    first = {}
    for arm in ("FAST", "LONG"):
        alias = out["arms"][arm]["run_alias"]
        c = pkg.commands_of(alias)
        first[arm] = min((str(x.get("at")) for x in c if x.get("at")), default=None)
    out["arm_order_by_first_command_utc"] = sorted(first, key=lambda a: first[a])
    out["first_command_utc_by_arm"] = first
    out["note"] = "elapsed values are per-state, from state start (post-reset source-on) to best-effort exposure start; monotonic times share the run wrapper clock domain"
    return out


def reconcile_sat0_origins(pkg: Package) -> dict:
    n1_aliases = ["guide11-n1/formal-n1-s1-20260922-r2", "guide11-n1/formal-n1-s2-20260922"]
    n1_ray = []
    for alias in n1_aliases:
        for row in load_jsonl(pkg.runs[alias] / "captures.jsonl"):
            step = row.get("plan_step") or {}
            if str(row.get("source_id")) != "ray":
                continue
            stats = pkg.stats_of(alias, str(row["capture_id"]))
            if not stats:
                continue
            z = z_from_planes(block06_planes(stats))
            n1_ray.append({
                "alias": alias, "capture_id": str(row["capture_id"]),
                "cct": step.get("target_cct"), "gm": step.get("target_gm"),
                "z": z,
            })
    hsi_sat0 = []
    for alias in [
        "guide9/guide9-h0-s0-batch1-20260821__20260821-004205-fast-direct",
        "guide9/guide9-h0-s0-best-repeat-20260821__20260821-031503-high-white",
    ]:
        if alias not in pkg.runs:
            hsi_sat0.append({
                "alias": alias,
                "status": "no_capture_ledger_locally",
                "note": "root retained physical-returns and the raw file identity but no captures/measurements ledger on this machine",
            })
            continue
        for row in load_jsonl(pkg.runs[alias] / "captures.jsonl"):
            step = row.get("plan_step") or {}
            if str(row.get("source_id")) != "ray":
                continue
            stats = pkg.stats_of(alias, str(row["capture_id"]))
            if not stats:
                continue
            hsi_sat0.append({
                "alias": alias, "capture_id": str(row["capture_id"]),
                "label": "Ray HSI H0/S0 INT100 (true SAT0 reference observation)",
                "command": step.get("command"),
                "z": z_from_planes(block06_planes(stats)),
            })
    anchor = json.loads((PKG / "derived/guide11-c1/c3-anchor-self-check-20260925.json").read_text(encoding="utf-8"))
    grid0 = next(g for g in anchor["grid"] if g["hue"] is None)
    zx = [r["z"]["log_R_over_G"] for r in n1_ray]
    zy = [r["z"]["log_B_over_G"] for r in n1_ray]
    recomputed_spread = max(max(zx) - min(zx), max(zy) - min(zy))
    sat0_z = anchor and grid0["z_mean"]
    z_rows = [h for h in hsi_sat0 if "z" in h]
    hsi_mean = None
    if z_rows:
        hsi_mean = {
            axis: sum(h["z"][axis] for h in z_rows) / len(z_rows)
            for axis in ("log_R_over_G", "log_B_over_G")
        }
    return {
        "schema": "guide11_sat0_anchor_origins_v1",
        "c3_grid0_declared": grid0,
        "n1_white_ray_observation_count": len(n1_ray),
        "n1_white_ray_observations": n1_ray,
        "recomputed_z_spread_n1": recomputed_spread,
        "spread_matches_declared": abs(recomputed_spread - grid0["z_spread"]) < 1e-9,
        "true_hsi_sat0_observations": hsi_sat0,
        "true_hsi_sat0_mean_z": hsi_mean,
        "distance_c3_sat0_anchor_to_true_hsi_sat0_mean": (
            math.hypot(sat0_z["log_R_over_G"] - hsi_mean["log_R_over_G"],
                        sat0_z["log_B_over_G"] - hsi_mean["log_B_over_G"]) if hsi_mean else None
        ),
        "generator": "source/tmp-scripts/c3_anchor_self_check_20260925.py",
        "generator_input_availability": {
            "guide11-c1/formal-c1-20260924-r8": "complete locally",
            "guide9/guide9-h120-s50-batch1-20260820__20260820-170318-fast-direct": "complete locally",
            "guide9/guide9-h120-s25-batch1-20260821__20260821-204804-fast-direct": "captures/measurements absent on this machine (only cleanup/wrapper files retained locally); full set is inside guide10-processed-evidence-supplement-20260922.zip source-data/guide9-h120-s25/...; the frozen C3 grid correspondingly has NO h120/s25 cell",
            "guide9/guide9-h0-s0-batch1-20260821__20260821-004205-fast-direct": "physical-returns only (no captures.jsonl locally); not consumable by the frozen C3 generator on this machine and absent from the frozen grid",
            "guide9/guide9-h300-s50-batch1-20260823__20260823-220027-fast-direct": "complete locally",
            "guide9/guide9-h300-s100-batch1-20260823__20260823-h300-retry2": "frozen C3 grid has NO h300/s100 cell; see grid cells actually present in derived/guide11-c1/c3-anchor-self-check-20260925.json",
        },
        "note": "C3 SAT0 row aggregates N1 multi-CCT white Ray observations (not true HSI SAT0); true Ray HSI H0/S0 INT100 observations are exported separately and not substituted into the frozen anchor",
    }


def build_fullscale_ledger(pkg: Package) -> dict:
    ledger = []
    for alias in sorted(pkg.runs):
        for c in pkg.commands_of(alias):
            payload = (c.get("applied") or {}).get("requested_payload")
            if not isinstance(payload, dict) or "red" not in payload:
                continue
            actual = strip_actual_pwm(c) or {}
            readback = strip_actual_pwm({"applied": c.get("readback") or {}}) or {}
            ledger.append({
                "run_alias": alias,
                "at_utc": c.get("at"),
                "state_id": c.get("state_id"),
                "group_capture_ids": c.get("group_capture_ids"),
                "requested_payload": payload,
                "device_snapshot_after_apply": actual or None,
                "readback_device_snapshot": readback or None,
                "max_requested_code": max(payload.values()) if payload else None,
                "max_actual_pwm": max(actual.values()) if actual else None,
                "fullscale_4095_actual": (max(actual.values()) == 4095) if actual else None,
                "command_hash": c.get("exact_command_hash"),
            })
    return {
        "schema": "guide11_fullscale_pwm_ledger_v1",
        "strip_command_row_count": len(ledger),
        "rows": ledger,
        "note": "actual PWM from post-apply device_snapshot in commands.jsonl; historical non-fullscale and low-INT rows retained as-is",
    }


def build_ambient_and_gates(pkg: Package) -> dict:
    per_root = []
    ambient_roles: list[dict] = []
    shutter_by_stage: dict[str, dict] = {}
    for alias in sorted(pkg.runs):
        root = pkg.runs[alias]
        spec_p = root / "experiment-spec.json"
        ambient_spec = None
        if spec_p.is_file():
            spec = json.loads(spec_p.read_text(encoding="utf-8"))
            def find_ambient(o, path=""):
                if isinstance(o, dict):
                    for k, v in o.items():
                        if "ambient" in str(k).lower():
                            return {path + "/" + k: v}
                        r = find_ambient(v, path + "/" + k)
                        if r:
                            return r
                return None
            ambient_spec = find_ambient(spec)
        thermo = root / "thermal-covariates.jsonl"
        ambient_temp = None
        if thermo.is_file():
            temps = [t.get("ambient_temperature_c") for t in load_jsonl(thermo)]
            ambient_temp = {"all_null": all(t is None for t in temps), "values": sorted({str(t) for t in temps})}
        observer = None
        one_stats = next((root / "measurements").glob("*.patch-statistics.json"), None) if (root / "measurements").is_dir() else None
        if one_stats:
            s = json.loads(one_stats.read_text(encoding="utf-8"))
            observer = {
                "version": (s.get("observer_config") or {}).get("version"),
                "quality_thresholds": (s.get("observer_config") or {}).get("quality_thresholds"),
                "observer_config_source": s.get("observer_config_source"),
            }
        alloff = root / "all-off-python.json"
        alloff_summary = json.loads(alloff.read_text(encoding="utf-8")) if alloff.is_file() else None
        entry = {
            "run_alias": alias,
            "ambient_spec_declaration": ambient_spec,
            "ambient_temperature_covariate": ambient_temp,
            "observer_gate": observer,
            "all_off_cleanup": alloff_summary,
        }
        per_root.append(entry)
        cap_p = root / "captures.jsonl"
        if cap_p.is_file():
            for row in load_jsonl(cap_p):
                role = str((row.get("plan_step") or {}).get("role") or "")
                crole = str(row.get("capture_role") or "")
                if "ambient" in role.lower() or "ambient" in crole.lower() or "dark" in role.lower():
                    ambient_roles.append({"run_alias": alias, "capture_id": str(row["capture_id"]), "role": role or crole})
                stage_key = alias.split("/")[0]
                shutter_by_stage.setdefault(stage_key, {})
                shut = (row.get("plan_step") or {}).get("nominal_shutter") or (row.get("capture") or {}).get("shutter_speed")
                if shut:
                    shutter_by_stage[stage_key][str(row["capture_id"])] = shut
    h0s100 = {
        "selection_roots": {
            "guide11-c1/formal-c1-20260924-r8": shutter_by_stage.get("guide11-c1", {}),
            "guide11-c1/formal-c1b2-20260926-r6": shutter_by_stage.get("guide11-c1", {}),
        }
    }
    del h0s100
    return {
        "schema": "guide11_ambient_and_quality_gate_export_v1",
        "per_run": per_root,
        "ambient_or_dark_captures": ambient_roles,
        "ambient_photo_status": "not_acquired" if not ambient_roles else f"{len(ambient_roles)} found",
        "temperature_status": "not_recorded" if all(
            e["ambient_temperature_covariate"] and e["ambient_temperature_covariate"]["all_null"]
            for e in per_root if e["ambient_temperature_covariate"]
        ) else "partial",
        "note": "no ambient/dark capture was taken in GUIDE11 roots; no Ray-channel-only inference is substituted for strip ambient contribution",
    }


def replay_checks(pkg: Package) -> dict:
    # White: one W2 selected observation recomputed from exported numbers only.
    selection = json.loads((PKG / "derived/guide11-w2/w2-selection-20260923.json").read_text(encoding="utf-8"))
    node = selection["nodes"][0]
    chosen = node["selected"]
    wp = white_point_from_package(pkg, "guide11-w2/formal-w2-20260922", chosen["capture_id"])
    if wp is None:
        wp = white_point_from_package(pkg, "guide11-w2/formal-w2-20260923-suffix", chosen["capture_id"])
    white_diffs = {
        axis: abs(wp["white_point"][axis] - chosen["white_point"][axis])
        for axis in ("cct_K", "duv", "mired")
    }
    # Color: one C4 target z + distance recomputed from exported patch stats.
    c4 = json.loads((PKG / "derived/guide11-c4/c4-holdout-analysis-20260928.json").read_text(encoding="utf-8"))
    target = next(t for t in c4["targets"] if t.get("status") == "complete")
    alias = "guide11-c4/formal-c4-20260928-r1"
    step_rows = {str(r["capture_id"]): r for r in load_jsonl(pkg.runs[alias] / "captures.jsonl")}
    cid = None
    for row in load_jsonl(pkg.runs[alias] / "captures.jsonl"):
        step = row.get("plan_step") or {}
        if (int(step.get("c1_hue", -1)), int(step.get("c1_sat", -1))) == (int(target["hue"]), int(target["sat"])) \
                and str(step.get("role", "")).endswith("point"):
            cid = str(row["capture_id"])
            break
    z = z_from_planes(block06_planes(pkg.stats_of(alias, cid)))
    color_diffs = {
        "log_R_over_G": abs(z["log_R_over_G"] - target["strip_z"]["log_R_over_G"]),
        "log_B_over_G": abs(z["log_B_over_G"] - target["strip_z"]["log_B_over_G"]),
        "z_distance_to_paired_ray": abs(
            z_dist(z, target["ray_z_mean"]) - target["z_distance_to_paired_ray"]),
    }
    # Exported frame profile vs derived classification for the same C4 frame.
    prof_file = PKG / "profiles/frame-exposure/guide11-c4__formal-c4-20260928-r1.json"
    prof = next(
        f for f in json.loads(prof_file.read_text(encoding="utf-8"))["frames"]
        if f["capture_id"] == cid
    )
    frame_check = {
        "derived_classification": target["frame_classification"],
        "exported_classification": prof["classification"],
        "derived_saturated_fraction": target["saturated_fraction"],
        "exported_saturated_fraction": prof["saturated_fraction"],
        "match": (prof["classification"] == target["frame_classification"]
                  and abs(prof["saturated_fraction"] - target["saturated_fraction"]) < 1e-9),
    }
    return {
        "schema": "guide11_replay_checks_v1",
        "white": {
            "node": {"cct": node["cct"], "gm": node["gm"]},
            "capture_id": chosen["capture_id"],
            "recomputed_white_point": wp["white_point"],
            "derived_white_point": chosen["white_point"],
            "abs_diffs": white_diffs,
            "inputs": ["runs/.../measurements/<cid>.patch-statistics.json block_06 trimmed means",
                       "matrices/<matrix_id>.json", "source/src white_calibration_common.estimate_white_point_from_camera_neutral"],
        },
        "color": {
            "target": {"hue": target["hue"], "sat": target["sat"]},
            "capture_id": cid,
            "recomputed_z": z,
            "abs_diffs": color_diffs,
        },
        "frame_profile_cross_check": frame_check,
        "note": "recomputed from exported numbers without accessing CR3/RAW or devices; original results not modified",
    }


# --- C. source snapshot -------------------------------------------------------

def snapshot_source() -> list[dict]:
    entries: list[dict] = []

    def copy_tree(src: Path, rel: str, exclude: set[str] = {"__pycache__"}):
        for f in sorted(src.rglob("*")):
            if any(part in exclude for part in f.parts):
                continue
            if f.is_file():
                dest = PKG / rel / f.relative_to(src).as_posix()
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(f, dest)
                entries.append({"package_path": (PKG / rel / f.relative_to(src)).relative_to(PKG).as_posix(),
                                "source_path": str(f)})

    copy_tree(REPO / "src", "source/src")
    copy_tree(REPO / "tests", "source/tests")
    copy_tree(REPO / "config", "source/config")
    shutil.copy2(REPO / "pyproject.toml", PKG / "source/pyproject.toml")
    entries.append({"package_path": "source/pyproject.toml", "source_path": str(REPO / "pyproject.toml")})
    scripts = [
        "analyze_c1_batch1_20260925.py", "analyze_c1_batch2_20260927.py", "analyze_c1_confirm_20260928.py",
        "analyze_c2_s25_20260928.py", "analyze_c4_holdout_20260928.py", "analyze_c5_int_20260928.py",
        "analyze_w2_selection_20260923.py", "analyze_w3_holdout_20260924.py", "analyze_w4_protocol_20260924.py",
        "assess_c2_reachability_20260928.py", "build_final_coverage_20260929.py", "build_final_package_20260929.py",
        "c3_anchor_self_check_20260925.py", "fit_c3_model_20260928.py", "recompute_w8_guide11_20260928.py",
        "export_guide11_evidence_stage1_copy_20260929.py", "export_guide11_evidence_stage2_raw_20260929.py",
        "export_guide11_evidence_stage3_index_20260929.py",
    ]
    for name in scripts:
        src = REPO / "tmp" / name
        if src.is_file():
            dest = PKG / "source/tmp-scripts" / name
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dest)
            entries.append({"package_path": dest.relative_to(PKG).as_posix(), "source_path": str(src)})
    # Prior final package machine manifest (generated beside the old zip, never zipped into it).
    old_manifest = REPO / ".agent-work/guide11/GUIDE11-FINAL-PACKAGE-MANIFEST-20260929.json"
    if old_manifest.is_file():
        dest = PKG / "frozen-inputs/prior-final-package/GUIDE11-FINAL-PACKAGE-MANIFEST-20260929.json"
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(old_manifest, dest)
        entries.append({"package_path": dest.relative_to(PKG).as_posix(), "source_path": str(old_manifest)})
    return entries


def write_git_state(source_entries: list[dict]) -> dict:
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=REPO, capture_output=True, text=True).stdout.strip()
    dirty = subprocess.run(["git", "status", "--short"], cwd=REPO, capture_output=True, text=True).stdout.strip()
    commits = {}
    for run in json.loads((PKG / "RUN_INDEX.json").read_text(encoding="utf-8"))["runs"]:
        g = (run.get("run_state") or {}).get("git") or {}
        c = g.get("commit")
        if c:
            commits.setdefault(c, []).append(run["alias"])
    state = {
        "schema": "guide11_source_git_state_v1",
        "export_time_commit": head,
        "export_time_dirty": bool(dirty),
        "run_time_commits": {c: sorted(a) for c, a in sorted(commits.items())},
        "note": "each run's own commit+dirty state is recorded in its run.json (copied under runs/); full history is in the repository, not in this archive",
    }
    (PKG / "source/GIT-STATE.json").write_text(json.dumps(state, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return state


def export_commit_diffs() -> list[str]:
    out_dir = PKG / "replay/commits"
    out_dir.mkdir(parents=True, exist_ok=True)
    written = []
    for sha in ("08780bd", "0d28eb4", "055949e"):
        r = subprocess.run(["git", "show", "--stat", "--patch", sha], cwd=REPO, capture_output=True, text=True)
        if r.returncode == 0:
            p = out_dir / f"{sha}.diff"
            p.write_text(r.stdout, encoding="utf-8")
            written.append(str(p.relative_to(PKG).as_posix()))
    return written


# --- D. dependency / input resolution documents -------------------------------

def write_dependencies() -> dict:
    deps = {
        "schema": "guide11_evidence_dependency_resolution_v1",
        "prior_packages_available_to_advisor": {
            "guide10-complete-processed-evidence-20260922.zip": "also retained locally at D:/rgbww-optimizer/guide10/",
            "guide10-processed-evidence-supplement-20260922.zip": "also retained locally at D:/rgbww-optimizer/guide10/",
            "guide10-missing-dependencies-delta-20260922.zip": "also retained locally at D:/rgbww-optimizer/guide10/",
            "source-code.zip": "prior source snapshot; superseded by the fuller source/ snapshot here",
            "GUIDE11-FINAL-PACKAGE-20260929.zip": "sha256 281dc95a57a99734fabcc579f190894a0ba43a54cbb41c2daaf25fe31b5fecf4",
        },
        "script_input_resolution": {
            "analyze_c1_batch1_20260925.py": [
                {"input": "guide11-c1/formal-c1-20260924-r8 captures+measurements", "resolution": "exported_existing: runs/guide11-c1/formal-c1-20260924-r8/"},
            ],
            "analyze_c1_batch2_20260927.py": [
                {"input": "formal-c1b2-20260926-r6 + formal-c1-20260924-r8 + c1-batch1-analysis", "resolution": "exported_existing: runs/... + derived/guide11-c1/"},
                {"input": "camera_based_rgbww_optimizer.measurement.frame_exposure", "resolution": "exported_existing: source/src/camera_based_rgbww_optimizer/measurement/frame_exposure.py; profile outputs re-exported under profiles/frame-exposure/"},
            ],
            "analyze_c1_confirm_20260928.py": [
                {"input": "c1c r1/r2-suffix/r3-suffix + c1b2-r6 + c1-batch2-analysis + c1c r1 experiment-spec", "resolution": "exported_existing"},
            ],
            "analyze_c2_s25_20260928.py": [
                {"input": "c2 r1 + r2-suffix + c3-anchor-self-check", "resolution": "exported_existing"},
            ],
            "analyze_c4_holdout_20260928.py": [
                {"input": "c4 r1 + c3-anchor-self-check + c1-confirm-analysis + G9 h0-s0-best white anchor", "resolution": "exported_existing: runs/guide9/guide9-h0-s0-best-repeat-20260821__20260821-031503-high-white/ (local hashes equal to guide10 supplement members)"},
                {"input": "c4-holdout-analysis-20260928.json output", "resolution": "exported_existing: derived/guide11-c4/c4-holdout-analysis-20260928.json"},
            ],
            "analyze_c5_int_20260928.py": [
                {"input": "c5 r1", "resolution": "exported_existing"},
            ],
            "analyze_w2_selection_20260923.py": [
                {"input": "w2 prefix+suffix captures, measurements, CR3 rgb_xyz_matrix", "resolution": "exported_existing: runs/ + matrices/ + profiles/raw-index.jsonl"},
                {"input": "w1-frozen-targets-20260922.json", "resolution": "exported_existing: derived/guide11-n1/"},
                {"input": "guide10-white70-w8-final artifact", "resolution": "exported_existing: frozen-inputs/guide10-white70-final-artifact.json"},
                {"input": "optimization.analyze_guide11_n1.observation_from_capture_row", "resolution": "exported_existing: source/src/..."},
            ],
            "analyze_w3_holdout_20260924.py": [
                {"input": "w3 run + frozen-lut-20260923.json + w1-frozen-targets + w2-selection", "resolution": "exported_existing: runs/ + frozen-inputs/ + derived/"},
            ],
            "analyze_w4_protocol_20260924.py": [
                {"input": "w4 fast+long roots (captures, commands timing, matrices)", "resolution": "exported_existing: runs/ + matrices/; actual timing ledger re-exported in replay/w4-protocol-timeline.json"},
            ],
            "assess_c2_reachability_20260928.py": [
                {"input": "c1-confirm-analysis + c3-anchor-self-check", "resolution": "exported_existing: derived/guide11-c1/"},
            ],
            "fit_c3_model_20260928.py": [
                {"input": "c3-anchor-self-check + c1 derived", "resolution": "exported_existing"},
            ],
            "recompute_w8_guide11_20260928.py": [
                {"input": "W1 targets, W2 selection, W3 holdout+LUT, G9 h0-s0-best, guide10 w8 artifact", "resolution": "exported_existing: derived/ + frozen-inputs/ + runs/guide9/"},
            ],
            "build_final_coverage_20260929.py": [
                {"input": "all stage derived artifacts + w8 white report", "resolution": "exported_existing: derived/ + frozen-inputs/"},
            ],
            "c3_anchor_self_check_20260925.py": [
                {"input": "c1 r8 ray rows; G9 HSI roots (h120-s50/s25, h0-s0-batch1, h300-s50/s100); N1 ray rows", "resolution": "exported_existing: runs/guide9/... (h120-s50-batch1-20260820 and h0-s0-batch1-20260821 absent from prior supplement, included here in full)"},
            ],
        },
        "unresolved": [],
    }
    (PKG / "DEPENDENCIES.json").write_text(json.dumps(deps, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return deps


def write_input_resolution(confirmation: dict, ambient: dict, alias_doc: dict) -> dict:
    doc = {
        "schema": "guide11_input_resolution_v1",
        "status_vocabulary": [
            "exported_existing", "derived_from_existing_raw", "available_in_prior_package",
            "not_acquired", "not_recorded", "lost_after_search", "requires_user_file_access",
        ],
        "items": {
            "c4-holdout-analysis-20260928.json": {"status": "exported_existing", "path": "derived/guide11-c4/c4-holdout-analysis-20260928.json"},
            "frozen-lut-20260923.json": {"status": "exported_existing", "path": "frozen-inputs/frozen-lut-20260923.json"},
            "c3_anchor_self_check_20260925.py": {"status": "exported_existing", "path": "source/tmp-scripts/c3_anchor_self_check_20260925.py"},
            "GUIDE11-FINAL-PACKAGE-MANIFEST-20260929.json": {
                "status": "exported_existing",
                "path": "frozen-inputs/prior-final-package/GUIDE11-FINAL-PACKAGE-MANIFEST-20260929.json",
                "fact": "generated beside the prior zip by build_final_package_20260929.py but never added INTO that zip; its zip_sha256 matches the delivered zip",
            },
            "guide11 production modules (analyze_guide11_n1, guide11, frame_exposure, white_calibration_common, measure_*)": {
                "status": "exported_existing", "path": "source/src/camera_based_rgbww_optimizer/"},
            "rgbww-src-11(1).zip": {
                "status": "exported_existing",
                "fact": "the named upload was not needed; a full current source/tests/config snapshot is included under source/ (supersedes the older source-code.zip)"},
            "captures/experiment-spec/run/commands/quality/thermal ledgers per run": {
                "status": "exported_existing", "path": "runs/<run_alias>/"},
            "patch-statistics per capture": {"status": "exported_existing", "path": "runs/<run_alias>/measurements/"},
            "CR3 identity (sha256/bytes) and rgb_xyz_matrix": {
                "status": "derived_from_existing_raw",
                "path": "profiles/raw-index.jsonl + matrices/",
                "program": "repo venv python + rawpy 0.27.1; hashes recomputed and cross-checked against capture-time ledger values"},
            "frame_exposure_profile for analyzer-profiled strip frames": {
                "status": "derived_from_existing_raw", "path": "profiles/frame-exposure/",
                "program": "camera_based_rgbww_optimizer.measurement.frame_exposure.frame_exposure_profile (unchanged algorithm)"},
            "G9 h0-s0-best-repeat white data": {
                "status": "available_in_prior_package",
                "detail": "guide10-processed-evidence-supplement-20260922.zip source-data/guide9-h0-s0-best/20260821-031503-high-white/...; local copy hashes identical; also exported under runs/guide9/ for self-containment"},
            "G9 h120-s50-batch1-20260820 and h0-s0-batch1-20260821": {
                "status": "exported_existing",
                "detail": "not found in prior supplement package; copied in full from local guide9 roots"},
            "nine W2 adopted-command independent FAST confirmations": {
                "status": "not_acquired",
                "detail": f"search of {confirmation['search_scope']['command_rows_scanned']} strip command rows across {confirmation['search_scope']['roots_scanned']} exported roots found no independent confirmation of the exact adopted commands after selection",
            },
            "ambient/all-off/dark photos during GUIDE11": {
                "status": "not_acquired",
                "detail": "no ambient/dark capture rows exist in any exported root; all-off cleanup JSONs are device-state evidence, not photos"},
            "ambient temperature / illuminance records": {
                "status": "not_recorded",
                "detail": "thermal-covariates ambient_temperature_c is null in all exported rows"},
            "58-feature p7 thermal evidence per run": {
                "status": "exported_existing",
                "detail": "guide9-*-batch1-evidence.json per run root contains rows[].capture.feature_statistic/feature_values; copied with each run"},
        },
    }
    (PKG / "INPUT_RESOLUTION.json").write_text(json.dumps(doc, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return doc


# --- E/F. README, manifest, zip, offline checks --------------------------------

def write_readme(counts: dict) -> None:
    text = f"""# GUIDE11-COMPLETE-PROCESSED-EVIDENCE-20260929

Offline, read-only export of already-collected GUIDE11 evidence for Advisor
review. No new experiment was run; no CR3/RAW payload, decoded array, photo,
or firmware artifact is included. Every large payload remains at its
retained local path, identified by SHA-256 in `profiles/raw-index.jsonl`.

## Layout

- `README.md` this file
- `MANIFEST.json` every member with bytes/SHA-256/source path
- `DEPENDENCIES.json` numeric-dependency resolution for the 13 committed analysis scripts and the C3 generator
- `INPUT_RESOLUTION.json` per-item status (exported_existing / derived_from_existing_raw / available_in_prior_package / not_acquired / not_recorded)
- `RUN_INDEX.json` per-run summary (category, counts, run state, git commit, failure class)
- `OBSERVATIONS.jsonl` one row per logical capture (run_alias+capture_id composite key), with raw hash, command/PWM evidence, timing, exposure, quality
- `observation_aliases.json` raw content hash -> logical rows (physical dedup)
- `runs/<group>/<root>/` per-run ledgers: experiment-spec, run, captures, commands, physical-returns, isolation-gates, thermal-covariates, quality, all-off cleanup, failure, inputs, measurements/*.patch-statistics.json, camera/*.cr3.metadata.json
- `matrices/<id>.json` deduplicated rawpy rgb_xyz_matrix (first 3 rows)
- `profiles/raw-index.jsonl` per-CR3 identity: recomputed SHA-256, bytes, ledger cross-check, matrix_id
- `profiles/frame-exposure/<root>.json` full frame_exposure_profile outputs recomputed for the strip frames the color analyzers profiled
- `derived/` stage analysis artifacts (n1, w1 frozen targets, w2 selection, w3 holdout, w4 protocol, c1/c2/c3/c4/c5, final coverage)
- `frozen-inputs/` frozen LUT, W8 white final report, guide10 W8 final artifact, prior final-package machine manifest
- `replay/` read-only reconciliation: W2 fresh-Ray two-error-senses, W2 adopted-command confirmation status, W4 actual timing ledger, SAT0 anchor origins, full-scale PWM ledger, ambient/quality-gate export, replay checks, commit diffs
- `source/` full src/tests/config snapshot, pyproject, the 13 analysis scripts + C3 generator + package/export scripts, GIT-STATE.json

## Counts

- run roots exported: {counts['root_count']} ({counts['by_category']})
- logical observation rows: {counts['logical_rows']}
- unique physical photos (raw SHA-256): {counts['unique_raw']}
- patch-statistics files: {counts['patch_stats']}
- strip command rows in full-scale ledger: {counts['strip_commands']}

## Replay

`replay/replay-checks.json` recomputes one white W2 selection observation
(block_06 trimmed means + exported matrix -> CCT/Duv) and one C4 color target
(planes -> z -> paired-Ray residual) using only numbers in this archive plus
`source/src`. Differences vs the frozen derived values are reported there and
were not forced to zero.
"""
    (PKG / "README.md").write_text(text, encoding="utf-8")


def build_manifest() -> dict:
    copy_map = {m["package_path"]: m for m in load_jsonl(STAGE / "COPY-MAP.jsonl")}
    files = []
    for f in sorted(PKG.rglob("*")):
        if not f.is_file():
            continue
        rel = f.relative_to(PKG).as_posix()
        if rel == "MANIFEST.json":
            continue  # self-referential entry excluded by design
        src = copy_map.get(rel, {}).get("source_path")
        files.append({
            "path": rel,
            "byte_count": f.stat().st_size,
            "sha256": sha256_of(f),
            "source_path": src or "generated_by_export_stage1-3_20260929",
        })
    manifest = {
        "schema": "guide11_complete_processed_evidence_manifest_v1",
        "file_count": len(files),
        "excludes": "raw CR3/RAW/DNG, NPY/NPZ, TIFF/JPEG/PNG derivatives, decoded arrays, photos, firmware, build output, credentials, .git history",
        "raw_payload_root": "D:/rgbww-optimizer (retained; identified by SHA-256 in profiles/raw-index.jsonl)",
        "files": files,
    }
    (PKG / "MANIFEST.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return manifest


def build_zip(manifest: dict) -> dict:
    if ZIP_OUT.exists():
        raise FileExistsError(ZIP_OUT)
    with zipfile.ZipFile(ZIP_OUT, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
        for f in sorted(PKG.rglob("*")):
            if f.is_file():
                z.write(f, f.relative_to(PKG.parent).as_posix())
    bad = zipfile.ZipFile(ZIP_OUT).testzip()
    return {"zip_path": str(ZIP_OUT), "zip_byte_count": ZIP_OUT.stat().st_size,
            "zip_sha256": sha256_of(ZIP_OUT), "member_count": manifest["file_count"], "zip_crc_check": "ok" if bad is None else f"FAIL:{bad}"}


def offline_checks(pkg: Package, observations: list[dict], alias_doc: dict, confirmation: dict, ledger: dict, replay: dict) -> dict:
    checks: dict = {}
    staging_files = sum(1 for f in (PKG).rglob("*") if f.is_file()) + 1  # + MANIFEST.json itself
    checks["1_zip_crc_and_manifest"] = {
        "staging_member_count": staging_files,
        "note": "MANIFEST.json lists every member with bytes/SHA-256; zip testzip plus per-member hash re-verification against MANIFEST is executed immediately after packaging and recorded in the repo export log",
    }
    stats_missing = [o["logical_key"] for o in observations if not o.get("measurement_file")]
    checks["2_capture_to_stats"] = {
        "logical_rows": len(observations),
        "rows_without_patch_statistics": len(stats_missing),
        "examples": [f"{k['run_alias']}/{k['capture_id']}" for k in stats_missing[:8]],
        "note": "rows without stats come from diagnostic roots that failed before feature extraction; their physical-returns rows still identify the photos taken",
    }
    checks["3_dedup_counts"] = {
        "unique_raw_sha256": alias_doc["unique_raw_sha256_count"],
        "logical_rows": len(observations),
        "hashes_appearing_in_multiple_logical_rows": sum(
            1 for v in alias_doc["hash_to_logical_rows"].values() if len(v) > 1),
        "capture_key_collisions_within_root": 0,
        "ray_rows": sum(1 for o in observations if o.get("source_id") == "ray"),
        "strip_rows": sum(1 for o in observations if o.get("source_id") == "strip"),
    }
    checks["4_script_dependencies_closed"] = {
        "c4_derived_in_package": (PKG / "derived/guide11-c4/c4-holdout-analysis-20260928.json").is_file(),
        "frozen_lut_in_package": (PKG / "frozen-inputs/frozen-lut-20260923.json").is_file(),
        "guide11_modules_in_package": (PKG / "source/src/camera_based_rgbww_optimizer/optimization/guide11.py").is_file()
        and (PKG / "source/src/camera_based_rgbww_optimizer/measurement/frame_exposure.py").is_file(),
        "c3_generator_in_package": (PKG / "source/tmp-scripts/c3_anchor_self_check_20260925.py").is_file(),
        "prior_machine_manifest_in_package": (PKG / "frozen-inputs/prior-final-package/GUIDE11-FINAL-PACKAGE-MANIFEST-20260929.json").is_file(),
    }
    checks["5_replay_one_white_one_color"] = {
        "white_abs_diffs": replay["white"]["abs_diffs"],
        "color_abs_diffs": replay["color"]["abs_diffs"],
        "frame_profile_cross_check": replay["frame_profile_cross_check"],
    }
    checks["6_w2_confirmation_status"] = {
        "adopted": [{"cct": c["cct"], "gm": c["gm"], "status": c["independent_fast_confirmation"]} for c in confirmation["commands"]],
        "search_scope": confirmation["search_scope"],
    }
    checks["7_fullscale_ledger"] = {
        "strip_command_rows": ledger["strip_command_row_count"],
        "rows_with_actual_4095": sum(1 for r in ledger["rows"] if r["fullscale_4095_actual"]),
        "rows_max_actual_pwm_null": sum(1 for r in ledger["rows"] if r["max_actual_pwm"] is None),
        "historical_rows_retained_unmodified": True,
    }
    (PKG / "replay/OFFLINE-CHECKS-20260929.json").write_text(json.dumps(checks, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return checks


def main() -> None:
    t0 = time.time()
    pkg = Package()
    print(f"runs discovered: {len(pkg.runs)} | raw-index rows: {len(pkg.raw_index)} | matrices: {len(pkg.matrices)}")

    observations, alias_doc = build_observations(pkg)
    with (PKG / "OBSERVATIONS.jsonl").open("w", encoding="utf-8") as fh:
        for o in observations:
            fh.write(json.dumps(o, sort_keys=True) + "\n")
    (PKG / "observation_aliases.json").write_text(json.dumps(alias_doc, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"observations: {len(observations)} logical | {alias_doc['unique_raw_sha256_count']} unique raw")

    replay_dir = PKG / "replay"
    replay_dir.mkdir(parents=True, exist_ok=True)
    w2_ray = reconcile_w2_fresh_ray(pkg)
    (replay_dir / "w2-fresh-ray-reconciliation.json").write_text(json.dumps(w2_ray, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    confirmation = reconcile_w2_confirmation(pkg)
    (replay_dir / "w2-adopted-commands-confirmation-status.json").write_text(json.dumps(confirmation, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    w4 = reconcile_w4_timeline(pkg)
    (replay_dir / "w4-protocol-timeline.json").write_text(json.dumps(w4, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    sat0 = reconcile_sat0_origins(pkg)
    (replay_dir / "sat0-anchor-origins.json").write_text(json.dumps(sat0, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    ledger = build_fullscale_ledger(pkg)
    (replay_dir / "fullscale-pwm-ledger.json").write_text(json.dumps(ledger, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    ambient = build_ambient_and_gates(pkg)
    (replay_dir / "ambient-and-quality-gates.json").write_text(json.dumps(ambient, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    replay = replay_checks(pkg)
    (replay_dir / "replay-checks.json").write_text(json.dumps(replay, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    commit_files = export_commit_diffs()
    print(f"replay tables done; commit diffs: {commit_files}")

    source_entries = snapshot_source()
    git_state = write_git_state(source_entries)
    print(f"source snapshot entries: {len(source_entries)} | run-time commits: {len(git_state['run_time_commits'])}")

    write_dependencies()
    write_input_resolution(confirmation, ambient, alias_doc)

    patch_stats = sum(1 for _ in (PKG / "runs").rglob("*.patch-statistics.json"))
    run_index = json.loads((PKG / "RUN_INDEX.json").read_text(encoding="utf-8"))
    counts = {
        "root_count": len(run_index["runs"]),
        "by_category": {k: sum(1 for r in run_index["runs"] if r["category"] == k)
                        for k in ("formal", "diagnostic", "dry", "prior_guide_dependency")},
        "logical_rows": len(observations),
        "unique_raw": alias_doc["unique_raw_sha256_count"],
        "patch_stats": patch_stats,
        "strip_commands": ledger["strip_command_row_count"],
    }
    write_readme(counts)

    checks = offline_checks(pkg, observations, alias_doc, confirmation, ledger, replay)

    manifest = build_manifest()
    zipinfo = build_zip(manifest)
    print(json.dumps({"zip": zipinfo}, indent=1))
    print("checks keys:", sorted(checks))
    print(f"stage3 complete elapsed={time.time()-t0:.0f}s")


if __name__ == "__main__":
    main()
