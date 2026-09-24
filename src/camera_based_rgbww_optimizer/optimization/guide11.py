"""GUIDE11 shared white-control interpolation and N1 repeatability planning.

GUIDE11 corrections implemented here:

* One shared ``mired x GM`` piecewise-bilinear command interpolation that the
  runtime controller path and validation/holdout plans must both call. Nearest
  node copying is only a labelled diagnostic, never the runtime model.
* N1 (``11.GUIDE.md`` section 3.2): six fixed white states, two independent
  FAST paired cycles split across two operating sessions, balanced source
  order, and optional same-dwell burst captures that never add a reset.
"""

from __future__ import annotations

import copy
import math
from pathlib import Path
from typing import Any, Mapping, Sequence


CHANNELS = ("cw", "ww", "r", "g", "b")

N1_POINTS: tuple[tuple[int, int], ...] = (
    (1800, 100),
    (2300, 200),
    (3200, 0),
    (5600, 100),
    (14000, 0),
    (20000, 100),
)
N1_BURST_POINTS: tuple[tuple[int, int], ...] = (
    (1800, 100),
    (5600, 100),
    (20000, 100),
)
N1_BURST_EXTRA_CAPTURES = 2
N1_BURST_STEP_S = 5.0

GUIDE11_N1_EXPERIMENT_ID = "GUIDE11_N1_WHITE_REPEATABLILITY_V1"
GUIDE11_N1_VARIANT = "guide11-n1-white-repeatability"
N1_AUTHORIZATION_SCHEMA = "direct_guide11_n1_repeatability_v1"


def _mired(cct: int) -> float:
    return 1_000_000.0 / float(cct)


def _lut_rows(lut: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for row in lut:
        command = {name: int(row["command"][name]) for name in CHANNELS}
        rows.append({
            "cct": int(row["cct"]),
            "gm": int(row["gm"]),
            "mired": _mired(int(row["cct"])),
            "command": command,
        })
    if not rows:
        raise ValueError("GUIDE11 interpolation requires a non-empty LUT")
    if len({(row["cct"], row["gm"]) for row in rows}) != len(rows):
        raise ValueError("GUIDE11 interpolation requires unique LUT nodes")
    return rows


def _channel_value(
    cct_rows: dict[float, list[dict[str, Any]]],
    gm_columns: Sequence[float],
    mired: float,
    gm: float,
    channel: str,
) -> float:
    mired_keys = sorted(cct_rows)
    if mired <= mired_keys[0]:
        m_lo = m_hi = mired_keys[0]
    elif mired >= mired_keys[-1]:
        m_lo = m_hi = mired_keys[-1]
    else:
        m_lo = max(key for key in mired_keys if key <= mired)
        m_hi = min(key for key in mired_keys if key >= mired)
    if gm <= gm_columns[0]:
        g_lo = g_hi = gm_columns[0]
    elif gm >= gm_columns[-1]:
        g_lo = g_hi = gm_columns[-1]
    else:
        g_lo = max(key for key in gm_columns if key <= gm)
        g_hi = min(key for key in gm_columns if key >= gm)

    def at(m_key: float, g_key: float) -> float:
        candidates = [
            row for row in cct_rows[m_key]
            if abs(row["gm"] - g_key) < 1e-9
        ]
        if not candidates:
            nearest = min(cct_rows[m_key], key=lambda row: abs(row["gm"] - g_key))
            raise ValueError(
                f"GUIDE11 interpolation grid lacks GM {g_key} at mired {m_key}; "
                f"nearest stored GM is {nearest['gm']}"
            )
        return float(candidates[0]["command"][channel])

    if m_lo == m_hi and g_lo == g_hi:
        return at(m_lo, g_lo)
    if m_lo == m_hi:
        frac_g = (gm - g_lo) / (g_hi - g_lo)
        return at(m_lo, g_lo) * (1.0 - frac_g) + at(m_lo, g_hi) * frac_g
    if g_lo == g_hi:
        frac_m = (mired - m_lo) / (m_hi - m_lo)
        return at(m_lo, g_lo) * (1.0 - frac_m) + at(m_hi, g_lo) * frac_m
    frac_m = (mired - m_lo) / (m_hi - m_lo)
    frac_g = (gm - g_lo) / (g_hi - g_lo)
    c00 = at(m_lo, g_lo)
    c01 = at(m_lo, g_hi)
    c10 = at(m_hi, g_lo)
    c11 = at(m_hi, g_hi)
    return (
        c00 * (1.0 - frac_m) * (1.0 - frac_g)
        + c01 * (1.0 - frac_m) * frac_g
        + c10 * frac_m * (1.0 - frac_g)
        + c11 * frac_m * frac_g
    )


def interpolate_white_command(
    lut: Sequence[Mapping[str, Any]], cct: int, gm: int,
) -> dict[str, Any]:
    """Shared runtime white command model: bilinear in mired x GM, clamped.

    This is the single interpolation owner for GUIDE11. The runtime
    controller, validation plans, and holdout plans must all route through
    this function so a request resolves to one identical command everywhere.
    Requests outside the LUT hull clamp to the hull edge; the response always
    reports whether the request was an exact stored node.
    """
    rows = _lut_rows(lut)
    gm_columns = sorted({float(row["gm"]) for row in rows})
    cct_rows: dict[float, list[dict[str, Any]]] = {}
    for row in rows:
        cct_rows.setdefault(row["mired"], []).append(row)
    mired = _mired(cct)
    gm_value = float(gm)
    hull_m = (min(cct_rows), max(cct_rows))
    hull_g = (gm_columns[0], gm_columns[-1])
    exact_node = any(
        row["cct"] == int(cct) and row["gm"] == int(gm) for row in rows
    )
    command = {}
    for channel in CHANNELS:
        value = _channel_value(cct_rows, gm_columns, mired, gm_value, channel)
        command[channel] = max(0, min(4095, int(round(value))))
    clamped = (
        not hull_m[0] - 1e-9 <= mired <= hull_m[1] + 1e-9
        or not hull_g[0] - 1e-9 <= gm_value <= hull_g[1] + 1e-9
    )
    return {
        "model": "guide11_mired_gm_bilinear_clamped_v1",
        "request": {"cct": int(cct), "gm": int(gm), "mired": mired},
        "command": command,
        "exact_node": exact_node,
        "clamped_to_hull": clamped,
        "nearest_node_command": None if exact_node else _nearest_node_command(rows, cct, gm),
    }


def _nearest_node_command(
    rows: Sequence[dict[str, Any]], cct: int, gm: int,
) -> dict[str, int]:
    mired = _mired(cct)
    nearest = min(
        rows,
        key=lambda row: abs(row["mired"] - mired) / max(mired, 1.0)
        + abs(row["gm"] - float(gm)) / 200.0,
    )
    return dict(nearest["command"])


def build_guide11_n1_session_plan(
    lut: Sequence[Mapping[str, Any]],
    frozen_shutters: Mapping[str, str],
    *,
    session_index: int,
    cycle_index: int,
) -> dict[str, Any]:
    """Build one N1 operating-session plan (one FAST paired cycle per point).

    Session 1 carries the bursts; session 2 is plain paired cycles so the six
    states span at least two operating periods with balanced Ray/strip order.
    """
    if session_index not in (1, 2) or cycle_index not in (1, 2):
        raise ValueError("GUIDE11 N1 defines exactly two sessions/cycles")
    import hashlib
    import json
    from datetime import datetime, timezone

    from camera_based_rgbww_optimizer.optimization import p7_thermal_diagnostics as thermal

    rows = _lut_rows(lut)
    shutters = dict(frozen_shutters)

    def nearest_shutter(source: str, cct: int, gm: int) -> str:
        mired = _mired(cct)
        nearest = min(
            rows,
            key=lambda row: abs(row["mired"] - mired) / max(mired, 1.0)
            + abs(row["gm"] - float(gm)) / 200.0,
        )
        key = f"{source}-white-{nearest['cct']}-gm{nearest['gm']}"
        if key not in shutters:
            raise ValueError(f"GUIDE11 N1 lacks a qualified {source} shutter for {key}")
        return str(shutters[key])

    captures: list[dict[str, Any]] = []
    commands_audit: list[dict[str, Any]] = []
    session_plan_shutters: dict[str, str] = {}
    for point_index, (cct, gm) in enumerate(N1_POINTS):
        resolved = interpolate_white_command(lut, cct, gm)
        strip_command = resolved["command"]
        ray_command = {"mode": "cct", "cct": cct, "gm": gm, "intensity_percent": 100.0}
        commands_audit.append({
            "cct": cct,
            "gm": gm,
            "command_source": "w6_node_exact" if resolved["exact_node"] else "guide11_bilinear_interpolation",
            "exact_node": resolved["exact_node"],
            "clamped_to_hull": resolved["clamped_to_hull"],
            "strip_command": strip_command,
        })
        ray_first = (point_index + cycle_index) % 2 == 0
        order = ("ray", "strip") if ray_first else ("strip", "ray")
        burst_here = session_index == 1 and (cct, gm) in N1_BURST_POINTS
        for source_index, source in enumerate(order, start=1):
            command = ray_command if source == "ray" else dict(strip_command)
            shutter = nearest_shutter(source, cct, gm)
            cache_key = f"{source}-n1-cct{cct}-gm{gm}"
            session_plan_shutters[cache_key] = shutter
            base = {
                "capture_role": "formal",
                "formal_measurement": True,
                "command": command,
                "exact_command_hash": thermal.canonical_sha256(command),
                "requested_elapsed_s": 120,
                "nominal_shutter": shutter,
                "exposure_cache_key": cache_key,
                "timing_acceptance": "observed_elapsed_record_only",
                "strip_zero_required": source == "ray",
                "ray_zero_required": source == "strip",
                "session_index": point_index * 2 + source_index,
                "source_order": source_index,
                "target_cct": cct,
                "target_gm": gm,
                "steady_claim": False,
                "source_id": source,
                "state_id": f"N1_C{cycle_index}_CCT{cct}_GM{gm}_{source.upper()}",
                "role": f"{source}_n1_cct{cct}_gm{gm}_cycle{cycle_index}",
                "n1_cycle_index": cycle_index,
                "n1_session_index": session_index,
            }
            elapsed_list = [120]
            if burst_here:
                elapsed_list.extend(
                    120 + N1_BURST_STEP_S * (extra + 1)
                    for extra in range(N1_BURST_EXTRA_CAPTURES)
                )
            for elapsed_index, elapsed in enumerate(elapsed_list):
                step = dict(base)
                step["requested_elapsed_s"] = elapsed
                burst_role = (
                    "burst_main" if burst_here and elapsed_index == 0
                    else f"burst_extra_{elapsed_index}" if burst_here
                    else "paired_cycle_main"
                )
                step["n1_burst_role"] = burst_role
                step["capture_id"] = (
                    f"{len(captures):03d}-{source}-guide11-n1-s{session_index}"
                    f"-cct{cct}-gm{gm}-c{cycle_index}"
                    + (f"-b{elapsed_index}" if burst_here else "")
                )
                captures.append(step)
    budget_cr3 = len(captures)
    plan = {
        "schema": thermal.PLAN_SCHEMA_V2,
        "status": "execute_authorized",
        "experiment_id": thermal.TD_C,
        "guide_experiment_id": GUIDE11_N1_EXPERIMENT_ID,
        "variant": GUIDE11_N1_VARIANT,
        "stage": f"GUIDE11-N1-SESSION-{session_index}",
        "phase": "formal",
        "source": "guide11_n1_repeatability",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "inputs": {
            "location": thermal.file_reference(thermal.LOCATION_PATH),
            "policy": thermal.file_reference(thermal.POLICY_PATH),
            "code_duty_curve": thermal.file_reference(thermal.CURVE_PATH),
        },
        "captures": captures,
        "capture_ids": [row["capture_id"] for row in captures],
        "timing_contract": thermal.timing_contract(2),
        "timing_resolution": "guide11_n1_reset600_D120",
        "cold_proxy": 600,
        "cold_proxy_wait_s": 600,
        "native_raw_ambient_policy": thermal.AMBIENT_POLICY_UNSUBTRACTED_NO_AMBIENT,
        "exposure_setup_required": [],
        "frozen_shutters": session_plan_shutters,
        "shutter_ledger_provenance": {
            "owner": "experiment_capture_steps",
            "required_cache_keys": sorted(session_plan_shutters),
            "frozen_shutters_sha256": thermal.canonical_sha256(session_plan_shutters),
        },
        "budgets": {
            "ray_cap": sum(row["source_id"] == "ray" for row in captures),
            "strip_cap": sum(row["source_id"] == "strip" for row in captures),
            "formal_cap": budget_cr3,
            "physical_cr3_cap": budget_cr3,
            "ambient_cap": 0,
            "retry": 0,
        },
        "execution_authorization": {
            "schema": N1_AUTHORIZATION_SCHEMA,
            "human_authorization_required": False,
            "human_authorization_verified": False,
            "device_use_granted_by": "operator_cli_allow_device_control",
            "experiment_id": GUIDE11_N1_EXPERIMENT_ID,
            "bounded_device_scope": True,
            "remote_v2_capability": True,
        },
        "camera": {
            "backend": "remote",
            "v2_capture_timing_capability_available": True,
            "v2_capture_capability": "remote_v2_capture_timing_v1",
            "resolved_capture_settings": {
                "owner": "remote_backend.resolve_capture_settings",
                "iso": "100",
                "aperture": "f/4",
                "image_format": "RAW",
            },
        },
        "analysis_contract": {
            "method": "guide11_n1_white_repeatability",
            "points": [{"cct": cct, "gm": gm} for cct, gm in N1_POINTS],
            "burst_points": [{"cct": cct, "gm": gm} for cct, gm in N1_BURST_POINTS],
            "session_index": session_index,
            "cycle_index": cycle_index,
            "commands_audit": commands_audit,
            "independent_reset_s": 600,
            "dwell_s": 120,
            "interpolation_model": "guide11_mired_gm_bilinear_clamped_v1",
            "steady_claim": False,
        },
    }
    return plan


def rejoin_thermal_covariates_by_physical_identity(
    observations_path: Path,
    output_path: Path,
) -> dict[str, Any]:
    """Rebuild the thermal join of an OBSERVATIONS-style index by identity.

    GUIDE11 correction: the packaged index joined ``thermal_covariates`` by
    ``state_id``, so paired Ray/strip observations sharing one state crossed
    sources (W6: 70/140 rows mismatched). The corrected join chain is
    physical: observation ``cr3_sha256`` -> the root's
    ``physical-returns.jsonl`` (capture_id plus the CR3's original run root
    via ``cr3_path``) -> that root's ``captures.jsonl`` row order -> the same
    row in ``thermal-covariates.jsonl``. Originals are never modified; the
    corrected index is a derived artifact.
    """
    import json
    from pathlib import Path as _Path

    rows = [
        json.loads(line)
        for line in _Path(observations_path).read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    ledger_cache: dict[str, dict[str, Any]] = {}

    def load_ledger(root_value: str) -> dict[str, Any]:
        if root_value in ledger_cache:
            return ledger_cache[root_value]
        root = Path(root_value)
        phys_path = root / "physical-returns.jsonl"
        ledger = {"phys_by_sha": {}, "phys_by_capture": {}, "cov": [], "cap_index": {}}
        if phys_path.is_file():
            for line in phys_path.read_text(encoding="utf-8").splitlines():
                if not line.strip():
                    continue
                row = json.loads(line)
                ledger["phys_by_sha"][str(row.get("cr3_sha256"))] = row
                ledger["phys_by_capture"][str(row.get("capture_id"))] = row
        cov_path = root / "thermal-covariates.jsonl"
        if cov_path.is_file():
            ledger["cov"] = [
                json.loads(line)
                for line in cov_path.read_text(encoding="utf-8").splitlines()
                if line.strip()
            ]
        caps_path = root / "captures.jsonl"
        if caps_path.is_file():
            for index, line in enumerate(caps_path.read_text(encoding="utf-8").splitlines()):
                if line.strip():
                    cap = json.loads(line)
                    ledger["cap_index"][str(cap.get("capture_id"))] = index
        ledger_cache[root_value] = ledger
        return ledger

    def resolve_covariate(row: Mapping[str, Any]) -> tuple[dict[str, Any] | None, dict[str, Any]]:
        identity = row.get("physical_identity") or {}
        sha = str(identity.get("cr3_sha256", ""))
        root_value = str(row.get("root", ""))
        capture_id = str(row.get("capture_id", ""))
        chain: list[str] = []
        for probe_root in (root_value,):
            ledger = load_ledger(probe_root)
            phys = ledger["phys_by_sha"].get(sha) or ledger["phys_by_capture"].get(capture_id)
            if phys is None:
                continue
            origin = None
            cr3_path = str(phys.get("cr3_path", ""))
            if cr3_path:
                origin = str(Path(cr3_path).parent.parent)
            for cov_root_value in (probe_root, origin) if origin else (probe_root,):
                cov_ledger = load_ledger(cov_root_value)
                index = cov_ledger["cap_index"].get(str(phys.get("capture_id")))
                if index is not None and index < len(cov_ledger["cov"]):
                    chain = [probe_root, str(phys.get("capture_id")), cov_root_value]
                    return cov_ledger["cov"][index], {
                        "status": "rejoined_by_physical_identity",
                        "chain": chain,
                    }
        return None, {
            "status": "unresolved",
            "reason": "no physical covariate row reachable from cr3 identity",
        }

    corrected = 0
    unresolved = 0
    for row in rows:
        match, join = resolve_covariate(row)
        if match is None:
            unresolved += 1
        else:
            old = row.get("thermal_covariates") or {}
            old_source = old.get("source_id") or old.get("source")
            if old_source != match.get("source_id") or old != match:
                corrected += 1
            row["thermal_covariates"] = match
            join["previous_source_id"] = old_source
            join["joined_source_id"] = match.get("source_id")
        row["thermal_covariates_join"] = join
    report = {
        "schema": "guide11_thermal_covariates_rejoin_v1",
        "source_index": str(Path(observations_path).resolve()),
        "row_count": len(rows),
        "corrected_rows": corrected,
        "unresolved_rows": unresolved,
        "join_chain": "cr3_sha256 -> physical-returns -> origin run root -> capture row order",
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    newline = "\n"
    output_path.write_text(
        "".join(json.dumps(row, sort_keys=True) + newline for row in rows),
        encoding="utf-8",
    )
    return report


def build_w7_long_mislabel_reclassification(
    run_root: Path, output_path: Path,
) -> dict[str, Any]:
    """Immutable derived reclassification of the mislabelled W7 'LONG' run.

    The GUIDE10 W7 'long' plan inherited reset600/D120 execution through the
    GUIDE9 branch while carrying LONG labels: its twelve photos are FAST
    (600/120) observations. Originals stay untouched; this derived artifact
    records, per capture, the effective protocol actually executed and the
    corrected scientific label for every downstream consumer.
    """
    import json

    root = Path(run_root)
    plan = json.loads((root / "experiment-spec.json").read_text(encoding="utf-8"))
    captures = [
        json.loads(line)
        for line in (root / "captures.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    reset_s = float(plan.get("cold_proxy_wait_s", -1))
    dwell_values = sorted({float(step.get("requested_elapsed_s", -1)) for step in plan.get("captures", ())})
    effective = "FAST_reset600_D120" if (reset_s == 600 and dwell_values == [120]) else (
        "LONG_reset1800_D600" if (reset_s == 1800 and dwell_values == [600]) else f"UNVERIFIED_reset{reset_s:g}_D{dwell_values}"
    )
    rows = []
    for capture in captures:
        step = capture.get("plan_step", {})
        rows.append({
            "capture_id": capture.get("capture_id"),
            "state_id": capture.get("state_id"),
            "source_id": capture.get("source_id"),
            "original_label": "W7_LONG",
            "effective_protocol": effective,
            "reclassified_scientific_label": "FAST_appended_derived",
            "usable_as_true_long": False,
            "independent_source_observation_retained": True,
            "plan_timing_resolution": plan.get("timing_resolution"),
            "plan_cold_proxy_wait_s": reset_s,
            "plan_dwell_values_s": dwell_values,
        })
    artifact = {
        "schema": "guide11_w7_long_derived_reclassification_v1",
        "run_root": str(root.resolve()),
        "effective_protocol": effective,
        "capture_count": len(rows),
        "note": (
            "Derived classification only; original run files are immutable. "
            "The 1800/GM100 pair crossed a long pause and must not be treated "
            "as an ordinary short-dwell pairing."
        ),
        "captures": rows,
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(artifact, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return artifact


def build_guide11_w1_frozen_targets(
    rejoined_observations_path: Path,
    w6_plan: Mapping[str, Any],
    output_path: Path,
) -> dict[str, Any]:
    """Freeze the GUIDE11 W1 white targets, tolerances, and response evidence.

    Targets come from the W6 Ray observations joined by physical identity;
    tolerances come from the frozen W6 validation contracts. The navigation
    objective is the full-tolerance ``E(u)`` of ``11.GUIDE.md`` section 4/W1.
    Same-node strip commands observed at more than one code (W5 candidate
    batches) are listed as measured secant evidence; no historical Jacobian is
    promoted to a derivative truth.
    """
    import json

    rows = [
        json.loads(line)
        for line in Path(rejoined_observations_path).read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    contracts = {
        (int(x["cct"]), int(x["gm"])): x
        for x in w6_plan.get("analysis_contract", {}).get("target_contracts", ())
    }
    ray_by_key: dict[tuple[int, int], dict[str, Any]] = {}
    measured_pairs: dict[tuple[int, int], list[dict[str, Any]]] = {}
    for row in rows:
        capture_id = str(row.get("capture_id", ""))
        source = str(row.get("source_id", ""))
        plan_step = row.get("plan_step") or {}
        key = (int(plan_step.get("target_cct", 0) or row.get("target", {}).get("cct", 0)),
               int(plan_step.get("target_gm", 0) or row.get("target", {}).get("gm", 0)))
        white = (row.get("white_observation") or {}).get("white_point") or {}
        command = row.get("command") or {}
        if not white or not command:
            continue
        if "w6" in capture_id and source == "ray" and key not in ray_by_key:
            ray_by_key[key] = {
                "cct_K": float(white["cct_K"]),
                "duv": float(white["duv"]),
                "mired": 1_000_000.0 / float(white["cct_K"]),
                "capture_id": capture_id,
            }
        if "w5" in capture_id and source == "strip":
            channel_command = {
                name: int(command.get(name, 0)) for name in CHANNELS
            }
            measured_pairs.setdefault(key, []).append({
                "capture_id": capture_id,
                "command": channel_command,
                "strip_white_point": {
                    "cct_K": float(white["cct_K"]),
                    "duv": float(white["duv"]),
                    "mired": 1_000_000.0 / float(white["cct_K"]),
                },
            })
    nodes = []
    missing_targets = []
    for key in sorted(contracts):
        contract = contracts[key]
        ray = ray_by_key.get(key)
        if ray is None:
            missing_targets.append(key)
            continue
        pairs = measured_pairs.get(key, [])
        unique_commands = {tuple(sorted(p["command"].items())) for p in pairs}
        nodes.append({
            "cct": key[0],
            "gm": key[1],
            "ray_target": ray,
            "tolerances": {
                "cct_K": float(contract["resolved_cct_tolerance_K"]),
                "mired": float(contract["cct_tolerance_mired"]),
                "duv": float(contract["duv_tolerance"]),
            },
            "navigation_objective": "E(u)=max(|e_K|/tau_K, |e_mired|/tau_mired, |e_Duv|/tau_Duv)",
            "measured_secant_evidence": {
                "observation_count": len(pairs),
                "unique_command_count": len(unique_commands),
                "usable_for_local_response": len(unique_commands) >= 2,
                "observations": pairs,
            },
        })
    artifact = {
        "schema": "guide11_w1_frozen_targets_v1",
        "node_count": len(nodes),
        "missing_ray_targets": [list(key) for key in missing_targets],
        "objective": "guide11_full_tolerance_E_max",
        "mired_cct_relation": "same white-point chromaticity, never independent noises",
        "nodes": nodes,
        "steady_claim": False,
    }
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    Path(output_path).write_text(
        json.dumps(artifact, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return artifact


W2_PER_NODE_COMMAND_CAP = 3
W2_CLOSED_POINTS = ((1800, 100),)


def _w6_node_status_rows(w6_analysis_path: Path) -> dict[tuple[int, int], dict[str, Any]]:
    import json

    analysis = json.loads(Path(w6_analysis_path).read_text(encoding="utf-8"))
    if isinstance(analysis.get("canonical_lut"), list):
        # The W8 final artifact carries the same per-node frozen commands and
        # status labels; normalize to the analysis-node shape.
        analysis = {
            "nodes": [
                {**row, "strip_command": row.get("command", {})}
                for row in analysis["canonical_lut"]
            ]
        }
    return {
        (int(row["cct"]), int(row["gm"])): row
        for row in analysis.get("nodes", ())
    }


def build_guide11_w2_candidate_rows(
    frozen_targets: Mapping[str, Any],
    w6_analysis_path: Path,
) -> list[dict[str, Any]]:
    """GUIDE11 W2 bounded-correction candidates from measured evidence only.

    Open nodes are W6 non-passing nodes excluding the permanently closed
    1800/100 point. Candidates come from the measured secant evidence frozen
    in W1 (>=2 distinct same-node commands with paired Ray-referenced
    observations): a full-tolerance E(u) best observation is kept as the
    measured fallback, a local secant step toward the frozen target is the
    correction candidate, and a half step bounds the risk. Nodes without
    measured direction evidence carry no fabricated candidates here.
    """
    import json

    rows_by_key = _w6_node_status_rows(w6_analysis_path)
    candidates_out = []
    for node in frozen_targets.get("nodes", ()):
        key = (int(node["cct"]), int(node["gm"]))
        if key in W2_CLOSED_POINTS:
            continue
        w6_row = rows_by_key.get(key)
        if w6_row is None or w6_row.get("status") == "pass":
            continue
        tolerances = node["tolerances"]
        target = node["ray_target"]
        evidence = node.get("measured_secant_evidence", {})
        observations = evidence.get("observations", ())
        commands = [obs["command"] for obs in observations]
        unique = {tuple(sorted(c.items())) for c in commands}
        row: dict[str, Any] = {
            "cct": key[0], "gm": key[1],
            "w6_status": w6_row.get("status"),
            "tolerances": tolerances,
            "objective": "guide11_full_tolerance_E_max",
        }
        if not unique:
            row.update({
                "method": "no_measured_direction_evidence",
                "commands": [],
                "fallback_command": dict(w6_row.get("strip_command", {})),
            })
            candidates_out.append(row)
            continue

        def eu_of(obs: Mapping[str, Any]) -> float:
            wp = obs["strip_white_point"]
            e_k = (wp["cct_K"] - target["cct_K"]) / tolerances["cct_K"]
            e_m = (wp["mired"] - target["mired"]) / tolerances["mired"]
            e_d = (wp["duv"] - target["duv"]) / tolerances["duv"]
            return max(abs(e_k), abs(e_m), abs(e_d))

        ranked = sorted(observations, key=eu_of)
        best = ranked[0]
        row["fallback_command"] = dict(best["command"])
        row["fallback_eu"] = eu_of(best)
        if len(unique) < 2:
            row.update({
                "method": "single_measured_command_no_direction",
                "commands": [],
            })
            candidates_out.append(row)
            continue
        # Measured local response: least squares over paired observations of
        # E-component error differences vs command differences, using the two
        # E-dominant axes of the best observation.
        import numpy as np

        names = list(CHANNELS)
        base_cmd = np.array([float(best["command"][n]) for n in names])
        target_vec = np.array([
            target["cct_K"] / tolerances["cct_K"],
            target["mired"] / tolerances["mired"],
            target["duv"] / tolerances["duv"],
        ])
        a_rows, b_rows = [], []
        base_residual = None
        for obs in observations:
            cmd = np.array([float(obs["command"][n]) for n in names])
            wp = obs["strip_white_point"]
            err_vec = np.array([
                wp["cct_K"] / tolerances["cct_K"],
                wp["mired"] / tolerances["mired"],
                wp["duv"] / tolerances["duv"],
            ])
            residual = err_vec - target_vec
            if np.allclose(cmd, base_cmd):
                base_residual = residual
                continue
            a_rows.append(cmd - base_cmd)
            b_rows.append(residual)
        if len(a_rows) >= 1 and base_residual is not None:
            sensitivity, *_ = np.linalg.lstsq(
                np.asarray(a_rows), np.asarray(b_rows), rcond=None
            )
            # Two-stage secant: measured sensitivity maps command deltas to
            # normalized error deltas; solve for the bounded command step that
            # cancels the best observation's residual as the smooth surrogate
            # for the max-form E(u).
            step, *_ = np.linalg.lstsq(sensitivity.T, -base_residual, rcond=None)
            max_step = 768.0
            step = np.clip(step, -max_step, max_step)
            proposed = {}
            for full, half in ((1.0, "correction"), (0.5, "half_step")):
                command = {
                    name: max(0, min(4095, int(round(float(base_cmd[i]) + full * float(step[i])))))
                    for i, name in enumerate(names)
                }
                if command != dict(best["command"]):
                    proposed[half] = command
            row.update({
                "method": "measured_secant_full_tolerance_step",
                "commands": list(proposed.values())[: W2_PER_NODE_COMMAND_CAP - 1],
            })
        else:
            row.update({
                "method": "single_measured_command_no_direction",
                "commands": [],
            })
        candidates_out.append(row)
    return candidates_out


W2_EXPERIMENT_ID = "GUIDE11_W2_BOUNDED_CORRECTION_V1"
W2_VARIANT = "guide11-w2-bounded-correction"
W2_AUTHORIZATION_SCHEMA = "direct_guide11_w2_bounded_correction_v1"


def build_guide11_w2_plan(
    candidate_rows: Sequence[Mapping[str, Any]],
    w6_plan: Mapping[str, Any],
    *,
    inputs_references: Mapping[str, Mapping[str, Any]] | None = None,
) -> dict[str, Any]:
    """Assemble the GUIDE11 W2 bounded-correction execution plan.

    One paired FAST Ray/strip capture per proposed command; the measured
    fallback command stays outside this batch (W6 evidence already covers
    it). Node order follows the frozen grid; source order alternates.
    """
    import copy

    from camera_based_rgbww_optimizer.optimization import p7_thermal_diagnostics as thermal

    templates: dict[tuple[int, int], dict[str, Mapping[str, Any]]] = {}
    for step in w6_plan.get("captures", ()):
        key = (int(step["target_cct"]), int(step["target_gm"]))
        templates.setdefault(key, {})[str(step["source_id"])] = step
    captures: list[dict[str, Any]] = []
    contracts: list[dict[str, Any]] = []
    for node_index, row in enumerate(
        sorted(candidate_rows, key=lambda r: (int(r["cct"]), int(r["gm"])))
    ):
        key = (int(row["cct"]), int(row["gm"]))
        node_templates = templates.get(key)
        if not node_templates or set(node_templates) != {"ray", "strip"}:
            raise ValueError(f"GUIDE11 W2 lacks frozen templates for {key}")
        ray_first = node_index % 2 == 0
        order = ("ray", "strip") if ray_first else ("strip", "ray")
        contracts.append({
            "target_index": node_index,
            "cct": key[0], "gm": key[1],
            "method": row["method"],
            "candidate_commands": [dict(c) for c in row["commands"]],
            "fallback_command": dict(row.get("fallback_command", {})),
            "tolerances": dict(row["tolerances"]),
        })
        for candidate_index, command in enumerate(row["commands"]):
            for source_index, source in enumerate(order, start=1):
                template = node_templates[source]
                step = copy.deepcopy(template)
                step.update({
                    "capture_id": (
                        f"{len(captures):03d}-{source}-guide11-w2-cct{key[0]}"
                        f"-gm{key[1]}-candidate{candidate_index}"
                    ),
                    "state_id": f"CCT{key[0]}_GM{key[1]}_W2_C{candidate_index}_{source.upper()}",
                    "role": "ray_reference" if source == "ray" else "strip_candidate",
                    "capture_role": "formal",
                    "formal_measurement": True,
                    "session_index": len(captures) + 1,
                    "source_order": source_index,
                    "requested_elapsed_s": 120,
                })
                if source == "strip":
                    step["command"] = dict(command)
                    step["exact_command_hash"] = thermal.canonical_sha256(command)
                captures.append(step)
    frozen = {str(step["exposure_cache_key"]): str(step["nominal_shutter"]) for step in captures}
    plan: dict[str, Any] = {
        "schema": thermal.PLAN_SCHEMA_V2,
        "status": "execute_authorized",
        "experiment_id": thermal.TD_C,
        "guide_experiment_id": W2_EXPERIMENT_ID,
        "variant": W2_VARIANT,
        "stage": "GUIDE11-W2-BOUNDED-CORRECTION",
        "phase": "formal",
        "source": "guide11_w1_frozen_targets_measured_secants",
        "created_at": thermal.datetime.now(thermal.timezone.utc).isoformat(),
        "inputs": {
            "location": thermal.file_reference(thermal.LOCATION_PATH),
            "policy": thermal.file_reference(thermal.POLICY_PATH),
            "code_duty_curve": thermal.file_reference(thermal.CURVE_PATH),
            **{k: dict(v) for k, v in (inputs_references or {}).items()},
        },
        "captures": captures,
        "capture_ids": [step["capture_id"] for step in captures],
        "timing_contract": thermal.timing_contract(2),
        "timing_resolution": "guide11_w2_reset600_D120",
        "cold_proxy": 600,
        "cold_proxy_wait_s": 600,
        "native_raw_ambient_policy": thermal.AMBIENT_POLICY_UNSUBTRACTED_NO_AMBIENT,
        "exposure_setup_required": [],
        "frozen_shutters": frozen,
        "shutter_ledger_provenance": {
            "owner": "experiment_capture_steps",
            "required_cache_keys": sorted(frozen),
            "frozen_shutters_sha256": thermal.canonical_sha256(frozen),
        },
        "budgets": {
            "ray_cap": sum(s["source_id"] == "ray" for s in captures),
            "strip_cap": sum(s["source_id"] == "strip" for s in captures),
            "formal_cap": len(captures),
            "physical_cr3_cap": len(captures),
            "ambient_cap": 0,
            "retry": 0,
        },
        "execution_authorization": {
            "schema": W2_AUTHORIZATION_SCHEMA,
            "human_authorization_required": False,
            "human_authorization_verified": False,
            "device_use_granted_by": "operator_cli_allow_device_control",
            "experiment_id": W2_EXPERIMENT_ID,
            "bounded_device_scope": True,
            "remote_v2_capability": True,
        },
        "camera": {
            "backend": "remote",
            "v2_capture_timing_capability_available": True,
            "v2_capture_capability": "remote_v2_capture_timing_v1",
            "resolved_capture_settings": {
                "owner": "remote_backend.resolve_capture_settings",
                "iso": "100", "aperture": "f/4", "image_format": "RAW",
            },
        },
        "analysis_contract": {
            "method": "guide11_w2_bounded_correction_measured_secants",
            "node_count": len(candidate_rows),
            "nodes_with_candidates": sum(1 for r in candidate_rows if r["commands"]),
            "target_contracts": contracts,
            "independent_reset_s": 600,
            "dwell_s": 120,
            "per_node_command_cap": W2_PER_NODE_COMMAND_CAP,
            "closed_points": [list(p) for p in W2_CLOSED_POINTS],
            "objective": "guide11_full_tolerance_E_max",
            "fallback_policy": "measured W6/W5 best command retained outside this batch",
            "global_model_refit": False,
            "steady_claim": False,
        },
    }
    return plan


def build_guide11_w2_recovery_suffix(interrupted_root: Path) -> dict[str, Any]:
    """Recover a paused GUIDE11 W2 run as an immutable suffix plan.

    The completed prefix is validated against the pause evidence (ledger
    agreement, capture order, physical CR3 presence, evidence hashes) and is
    never mutated; only the remaining suffix captures are re-executed in a
    fresh run.
    """
    import hashlib
    import json

    from camera_based_rgbww_optimizer.optimization import p7_thermal_diagnostics as thermal

    root = Path(interrupted_root)
    run = json.loads((root / "run.json").read_text(encoding="utf-8"))
    pause = json.loads((root / "pause-evidence.json").read_text(encoding="utf-8"))
    plan_path = root / "experiment-spec.json"
    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    if plan.get("guide_experiment_id") != W2_EXPERIMENT_ID:
        raise ValueError("GUIDE11 W2 recovery requires the frozen W2 plan")
    if run.get("status") != "interrupted" or not str(run.get("interruption_reason", "")).startswith("user_requested_pause"):
        raise ValueError("GUIDE11 W2 recovery requires an explicitly paused run")
    if run.get("cleanup") not in {"pass", "pass_external_verified"} or pause.get("status") != "pass":
        raise ValueError("GUIDE11 W2 recovery requires verified pause cleanup evidence")
    expected_zero = {"blue": 0, "green": 0, "cold_white": 0, "red": 0, "warm_white": 0}
    cleanup_block = pause.get("external_cleanup") if isinstance(pause.get("external_cleanup"), dict) else {}
    rgbww_zero = pause.get("rgbww_zero_readback") or cleanup_block.get("rgbww_zero_readback")
    ray_zero = pause.get("ray_zero_readback") or cleanup_block.get("ray_zero_readback")
    if rgbww_zero != expected_zero or int((ray_zero or {}).get("intensity", -1)) != 0:
        raise ValueError("GUIDE11 W2 recovery requires exact both-device zero readback")
    captures = [
        json.loads(line)
        for line in (root / "captures.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    returns = [
        json.loads(line)
        for line in (root / "physical-returns.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    if len(captures) != len(returns) or len(captures) != int(run.get("completed_formal", -1)):
        raise ValueError("GUIDE11 W2 recovery ledgers disagree on the completed prefix")
    expected = list(plan.get("captures", ()))
    if not captures or len(captures) >= len(expected):
        raise ValueError("GUIDE11 W2 recovery requires a non-empty incomplete prefix")
    for index, (capture, returned, step) in enumerate(zip(captures, returns, expected)):
        if str(capture.get("capture_id")) != str(step["capture_id"]) or str(returned.get("capture_id")) != str(step["capture_id"]):
            raise ValueError(f"GUIDE11 W2 recovery prefix diverges at index {index}")
        raw = Path(str(returned.get("cr3_path", "")))
        if not raw.is_file() or raw.stat().st_size != int(returned.get("cr3_byte_count", -1)):
            raise ValueError(f"GUIDE11 W2 recovery RAW artifact missing at index {index}")

    def _sha(path: Path) -> str:
        return hashlib.sha256(path.read_bytes()).hexdigest()

    if pause.get("evidence_hashes", {}).get("captures_jsonl") != _sha(root / "captures.jsonl"):
        raise ValueError("GUIDE11 W2 recovery captures ledger hash drifted")
    if pause.get("evidence_hashes", {}).get("physical_returns_jsonl") != _sha(root / "physical-returns.jsonl"):
        raise ValueError("GUIDE11 W2 recovery physical-returns ledger hash drifted")
    suffix = json.loads(json.dumps(plan))
    suffix["captures"] = expected[len(captures):]
    suffix["capture_ids"] = [str(step["capture_id"]) for step in suffix["captures"]]
    required = sorted({str(step["exposure_cache_key"]) for step in suffix["captures"]})
    suffix["frozen_shutters"] = {
        key: value for key, value in plan["frozen_shutters"].items() if key in required
    }
    suffix["shutter_ledger_provenance"] = {
        "owner": "experiment_capture_steps",
        "required_cache_keys": required,
        "frozen_shutters_sha256": thermal.canonical_sha256(suffix["frozen_shutters"]),
    }
    suffix["budgets"].update(
        ray_cap=sum(s["source_id"] == "ray" for s in suffix["captures"]),
        strip_cap=sum(s["source_id"] == "strip" for s in suffix["captures"]),
        formal_cap=len(suffix["captures"]),
        physical_cr3_cap=len(suffix["captures"]),
    )
    suffix["stage"] = "GUIDE11-W2-BOUNDED-CORRECTION-RECOVERY-SUFFIX"
    suffix["variant"] = f"{W2_VARIANT}-recovery-suffix"
    suffix["recovery"] = {
        "schema": "guide11_w2_recovery_suffix_v1",
        "parent_root": str(root.resolve()),
        "completed_prefix_count": len(captures),
        "remaining_suffix_count": len(suffix["captures"]),
        "parent_plan_sha256": _sha(plan_path),
        "pause_evidence_sha256": _sha(root / "pause-evidence.json"),
        "parent_captures_sha256": _sha(root / "captures.jsonl"),
        "parent_physical_returns_sha256": _sha(root / "physical-returns.jsonl"),
    }
    suffix["analysis_contract"] = {
        **dict(suffix["analysis_contract"]),
        "recovery_parent_prefix_count": len(captures),
    }
    return suffix


W3_EXPERIMENT_ID = "GUIDE11_W3_INTERPOLATION_HOLDOUT_V2"
W3_VARIANT = "guide11-w3-interpolation-holdout"
W3_AUTHORIZATION_SCHEMA = "direct_guide11_w3_interpolation_holdout_v2"
# Twenty fixed non-node holdout requests: the old GUIDE10 W7 lattice with
# four mid-band points moved onto the N1-confirmed difficult regions
# (3200 K and 14000 K neighbourhoods) per GUIDE11 W3 stratification.
W3_POINTS: tuple[tuple[int, int], ...] = (
    (1800, 35), (1800, 165), (1900, 100), (2150, 35), (2150, 165),
    (2500, 35), (2500, 165), (3000, 100), (3200, 35), (3200, 165),
    (4100, 100), (4750, 35), (4750, 165), (5300, 100), (6100, 35),
    (6100, 165), (7250, 100), (9000, 35), (14000, 35), (17000, 100),
)


def build_guide11_w3_holdout_plan(
    frozen_lut: Sequence[Mapping[str, Any]],
    w6_plan: Mapping[str, Any],
    *,
    inputs_references: Mapping[str, Mapping[str, Any]] | None = None,
) -> dict[str, Any]:
    """GUIDE11 W3 holdout: interpolated commands for twenty fixed non-nodes.

    Commands come exclusively from the shared
    ``guide11_mired_gm_bilinear_clamped_v1`` interpolation owner over the
    frozen post-W2 LUT, so controller and validation share one model. Each
    request records the contributing knots' nearest-node command as the
    diagnostic baseline; node residual and interpolation increment are
    separable in the analysis.
    """
    import copy

    from camera_based_rgbww_optimizer.optimization import p7_thermal_diagnostics as thermal

    templates: dict[tuple[int, int], dict[str, Mapping[str, Any]]] = {}
    for step in w6_plan.get("captures", ()):
        key = (int(step["target_cct"]), int(step["target_gm"]))
        templates.setdefault(key, {})[str(step["source_id"])] = step

    def nearest_template_key(cct: int, gm: int) -> tuple[int, int]:
        rows = [(int(n["cct"]), int(n["gm"])) for n in frozen_lut]
        return min(
            rows,
            key=lambda key: abs(1_000_000.0 / key[0] - 1_000_000.0 / cct) / (1_000_000.0 / cct)
            + abs(key[1] - gm) / 200.0,
        )

    def nearest_shutter(source: str, cct: int, gm: int) -> str:
        rows = [(int(n["cct"]), int(n["gm"])) for n in frozen_lut]
        nearest = min(
            rows,
            key=lambda key: abs(1_000_000.0 / key[0] - 1_000_000.0 / cct) / (1_000_000.0 / cct)
            + abs(key[1] - gm) / 200.0,
        )
        key = f"{source}-white-{nearest[0]}-gm{nearest[1]}"
        shutters = dict(w6_plan.get("frozen_shutters", {}))
        if key not in shutters:
            raise ValueError(f"GUIDE11 W3 lacks a qualified {source} shutter for {key}")
        return str(shutters[key])

    captures: list[dict[str, Any]] = []
    audit: list[dict[str, Any]] = []
    for point_index, (cct, gm) in enumerate(W3_POINTS):
        resolved = interpolate_white_command(frozen_lut, cct, gm)
        strip_command = resolved["command"]
        ray_command = {"mode": "cct", "cct": cct, "gm": gm, "intensity_percent": 100.0}
        audit.append({
            "cct": cct, "gm": gm,
            "exact_node": resolved["exact_node"],
            "clamped_to_hull": resolved["clamped_to_hull"],
            "interpolated_command": strip_command,
            "nearest_node_command": resolved["nearest_node_command"],
        })
        nearest_key = nearest_template_key(cct, gm)
        node_templates = templates[nearest_key]
        ray_first = point_index % 2 == 0
        order = ("ray", "strip") if ray_first else ("strip", "ray")
        for source_index, source in enumerate(order, start=1):
            template = node_templates[source]
            step = copy.deepcopy(template)
            cache_key = f"{source}-w3-cct{cct}-gm{gm}"
            step.update({
                "capture_id": f"{len(captures):03d}-{source}-guide11-w3-cct{cct}-gm{gm}",
                "state_id": f"W3_CCT{cct}_GM{gm}_{source.upper()}",
                "role": "ray_reference" if source == "ray" else "strip_holdout",
                "capture_role": "formal",
                "formal_measurement": True,
                "session_index": len(captures) + 1,
                "source_order": source_index,
                "target_cct": cct,
                "target_gm": gm,
                "requested_elapsed_s": 120,
                "nominal_shutter": nearest_shutter(source, cct, gm),
                "exposure_cache_key": cache_key,
            })
            if source == "ray":
                step["command"] = ray_command
                step["exact_command_hash"] = thermal.canonical_sha256(ray_command)
            else:
                step["command"] = dict(strip_command)
                step["exact_command_hash"] = thermal.canonical_sha256(strip_command)
            captures.append(step)
    frozen = {str(step["exposure_cache_key"]): str(step["nominal_shutter"]) for step in captures}
    return {
        "schema": thermal.PLAN_SCHEMA_V2,
        "status": "execute_authorized",
        "experiment_id": thermal.TD_C,
        "guide_experiment_id": W3_EXPERIMENT_ID,
        "variant": W3_VARIANT,
        "stage": "GUIDE11-W3-INTERPOLATION-HOLDOUT",
        "phase": "formal",
        "source": "guide11_w3_frozen_lut_interpolation",
        "created_at": thermal.datetime.now(thermal.timezone.utc).isoformat(),
        "inputs": {
            "location": thermal.file_reference(thermal.LOCATION_PATH),
            "policy": thermal.file_reference(thermal.POLICY_PATH),
            "code_duty_curve": thermal.file_reference(thermal.CURVE_PATH),
            **{k: dict(v) for k, v in (inputs_references or {}).items()},
        },
        "captures": captures,
        "capture_ids": [step["capture_id"] for step in captures],
        "timing_contract": thermal.timing_contract(2),
        "timing_resolution": "guide11_w3_reset600_D120",
        "cold_proxy": 600,
        "cold_proxy_wait_s": 600,
        "native_raw_ambient_policy": thermal.AMBIENT_POLICY_UNSUBTRACTED_NO_AMBIENT,
        "exposure_setup_required": [],
        "frozen_shutters": frozen,
        "shutter_ledger_provenance": {
            "owner": "experiment_capture_steps",
            "required_cache_keys": sorted(frozen),
            "frozen_shutters_sha256": thermal.canonical_sha256(frozen),
        },
        "budgets": {
            "ray_cap": 20, "strip_cap": 20, "formal_cap": 40,
            "physical_cr3_cap": 40, "ambient_cap": 0, "retry": 0,
        },
        "execution_authorization": {
            "schema": W3_AUTHORIZATION_SCHEMA,
            "human_authorization_required": False,
            "human_authorization_verified": False,
            "device_use_granted_by": "operator_cli_allow_device_control",
            "experiment_id": W3_EXPERIMENT_ID,
            "bounded_device_scope": True,
            "remote_v2_capability": True,
        },
        "camera": {
            "backend": "remote",
            "v2_capture_timing_capability_available": True,
            "v2_capture_capability": "remote_v2_capture_timing_v1",
            "resolved_capture_settings": {
                "owner": "remote_backend.resolve_capture_settings",
                "iso": "100", "aperture": "f/4", "image_format": "RAW",
            },
        },
        "analysis_contract": {
            "method": "guide11_w3_interpolation_holdout",
            "holdout_count": 20,
            "points": [{"cct": c, "gm": g} for c, g in W3_POINTS],
            "requests_audit": audit,
            "interpolation_model": "guide11_mired_gm_bilinear_clamped_v1",
            "reporting": "node-residual and interpolation-increment reported separately",
            "one_local_knot_correction_allowed": True,
            "max_new_knots": 6,
            "independent_reset_s": 600,
            "dwell_s": 120,
            "global_model_refit": False,
            "steady_claim": False,
        },
    }


W4_EXPERIMENT_ID = "GUIDE11_W4_PROTOCOL_FAST_LONG_V1"
W4_POINTS: tuple[tuple[int, int], ...] = ((1800, 100), (3200, 100), (5600, 100), (20000, 100))


def build_guide11_w4_protocol_plan(
    frozen_lut: Sequence[Mapping[str, Any]],
    w6_plan: Mapping[str, Any],
    *,
    protocol: str,
    inputs_references: Mapping[str, Mapping[str, Any]] | None = None,
) -> dict[str, Any]:
    """GUIDE11 W4 FAST or true-LONG protocol pair at four fixed points.

    One plan carries exactly one protocol so the timing-label contract stays
    exact: FAST runs reset600/D120; LONG runs a true reset1800/D600. Each
    point gets one paired Ray/strip observation under the same frozen node
    command; source order alternates and reverses between the two protocol
    runs. The analysis forms Delta_protocol = (strip-Ray)_LONG -
    (strip-Ray)_FAST across the paired runs.
    """
    import copy

    from camera_based_rgbww_optimizer.optimization import p7_thermal_diagnostics as thermal

    if protocol not in {"fast", "long"}:
        raise ValueError("GUIDE11 W4 protocol must be 'fast' or 'long'")
    templates: dict[tuple[int, int], dict[str, Mapping[str, Any]]] = {}
    for step in w6_plan.get("captures", ()):
        key = (int(step["target_cct"]), int(step["target_gm"]))
        templates.setdefault(key, {})[str(step["source_id"])] = step
    lut_by_key = {(int(n["cct"]), int(n["gm"])): n for n in frozen_lut}
    captures: list[dict[str, Any]] = []
    for point_index, (cct, gm) in enumerate(W4_POINTS):
        key = (cct, gm)
        node = lut_by_key[key]
        strip_command = {name: int(node["command"][name]) for name in CHANNELS}
        ray_command = {"mode": "cct", "cct": cct, "gm": gm, "intensity_percent": 100.0}
        node_templates = templates[key]
        ray_first = point_index % 2 == 0
        order = ("ray", "strip") if ray_first else ("strip", "ray")
        for source_index, source in enumerate(order, start=1):
            template = node_templates[source]
            step = copy.deepcopy(template)
            step.update({
                "capture_id": f"{len(captures):03d}-{source}-guide11-w4-{protocol}-cct{cct}-gm{gm}",
                "state_id": f"W4_{protocol.upper()}_CCT{cct}_GM{gm}_{source.upper()}",
                "role": f"{source}_w4_{protocol}",
                "capture_role": "formal",
                "formal_measurement": True,
                "session_index": len(captures) + 1,
                "source_order": source_index,
                "target_cct": cct,
                "target_gm": gm,
                "requested_elapsed_s": 120 if protocol == "fast" else 600,
                "w4_protocol": protocol,
            })
            if source == "ray":
                step["command"] = ray_command
                step["exact_command_hash"] = thermal.canonical_sha256(ray_command)
            else:
                step["command"] = strip_command
                step["exact_command_hash"] = thermal.canonical_sha256(strip_command)
            captures.append(step)
    frozen = {str(step["exposure_cache_key"]): str(step["nominal_shutter"]) for step in captures}
    return {
        "schema": thermal.PLAN_SCHEMA_V2,
        "status": "execute_authorized",
        "experiment_id": thermal.TD_C,
        "guide_experiment_id": W4_EXPERIMENT_ID,
        "variant": f"guide11-w4-protocol-{protocol}",
        "stage": f"GUIDE11-W4-PROTOCOL-{protocol.upper()}",
        "phase": "formal",
        "source": "guide11_w4_protocol_validation",
        "created_at": thermal.datetime.now(thermal.timezone.utc).isoformat(),
        "inputs": {
            "location": thermal.file_reference(thermal.LOCATION_PATH),
            "policy": thermal.file_reference(thermal.POLICY_PATH),
            "code_duty_curve": thermal.file_reference(thermal.CURVE_PATH),
            **{k: dict(v) for k, v in (inputs_references or {}).items()},
        },
        "captures": captures,
        "capture_ids": [step["capture_id"] for step in captures],
        "timing_contract": thermal.timing_contract(2),
        "timing_resolution": (
            "guide11_w4fast_reset600_D120" if protocol == "fast"
            else "guide11_w4long_reset1800_D600"
        ),
        "cold_proxy": 600 if protocol == "fast" else 1800,
        "cold_proxy_wait_s": 600 if protocol == "fast" else 1800,
        "native_raw_ambient_policy": thermal.AMBIENT_POLICY_UNSUBTRACTED_NO_AMBIENT,
        "exposure_setup_required": [],
        "frozen_shutters": frozen,
        "shutter_ledger_provenance": {
            "owner": "experiment_capture_steps",
            "required_cache_keys": sorted(frozen),
            "frozen_shutters_sha256": thermal.canonical_sha256(frozen),
        },
        "budgets": {
            "ray_cap": 4, "strip_cap": 4, "formal_cap": 8,
            "physical_cr3_cap": 8, "ambient_cap": 0, "retry": 0,
        },
        "execution_authorization": {
            "schema": f"direct_guide11_w4_{protocol}_v1",
            "human_authorization_required": False,
            "human_authorization_verified": False,
            "device_use_granted_by": "operator_cli_allow_device_control",
            "experiment_id": W4_EXPERIMENT_ID,
            "bounded_device_scope": True,
            "remote_v2_capability": True,
        },
        "camera": {
            "backend": "remote",
            "v2_capture_timing_capability_available": True,
            "v2_capture_capability": "remote_v2_capture_timing_v1",
            "resolved_capture_settings": {
                "owner": "remote_backend.resolve_capture_settings",
                "iso": "100", "aperture": "f/4", "image_format": "RAW",
            },
        },
        "analysis_contract": {
            "method": "guide11_w4_protocol_difference_in_differences",
            "protocol": protocol,
            "points": [{"cct": c, "gm": g} for c, g in W4_POINTS],
            "primary_quantity": "Delta_protocol=(strip-Ray)_LONG-(strip-Ray)_FAST",
            "components_reported_separately": ["Ray_LONG-FAST", "strip_LONG-FAST"],
            "order_note": "FAST run executes first; reversed-order pairing is an optional <=8-frame append only if conclusions would change adoption",
            "independent_reset_s": 600 if protocol == "fast" else 1800,
            "dwell_s": 120 if protocol == "fast" else 600,
            "steady_claim": False,
            "thermal_causal_claim": False,
        },
    }


C1_EXPERIMENT_ID = "GUIDE11_C1_HSI_MAIN_NODES_V1"
C1_TARGETS: tuple[tuple[int, int], ...] = (
    (0, 50), (0, 100), (60, 50), (60, 100),
    (180, 50), (180, 100), (240, 50), (240, 100),
)


def _c1_sector_candidates(hue: int, sat: int) -> list[tuple[str, dict[str, int]]]:
    """Four structurally diverse candidates for a C1 main node.

    Structure follows the frozen GUIDE9 HSI batch pattern (distinct active
    faces / channel dominances, no directionality claim), with the dominant
    channels rotated by hue sector. SAT enters through the white-channel
    floor: S50 keeps half the white base of S100.
    """
    sat_scale = sat / 100.0
    white = int(round(2100 * (1.0 - sat_scale) + 1050 * sat_scale * 0.0))
    white_s50 = 1050
    base_white = white_s50 if sat == 50 else 0
    full = 4095
    half = 2048
    quarter = 1024
    if hue == 0:
        dominant = ("r",)
        secondary = {"g": quarter, "b": quarter}
    elif hue == 60:
        dominant = ("r", "g")
        secondary = {"b": quarter}
    elif hue == 180:
        dominant = ("g", "b")
        secondary = {"r": quarter}
    else:  # 240
        dominant = ("b",)
        secondary = {"r": quarter, "g": half}
    pure = {name: 0 for name in CHANNELS}
    for name in dominant:
        pure[name] = full
    for name, value in secondary.items():
        pure[name] = max(pure[name], value)
    candidates: list[tuple[str, dict[str, int]]] = [
        ("fullscale_dominant", pure),
        ("high_white_dominant", {
            **{name: 0 for name in CHANNELS},
            "cw": base_white, "ww": base_white,
            **{name: (half if name in dominant else 0) for name in CHANNELS[2:]},
            **{name: (half if name in dominant else 0) for name in CHANNELS[:2]},
        }),
        ("white_biased_mix", {
            **{name: 0 for name in CHANNELS},
            "cw": max(base_white, 1500), "ww": max(base_white, 1500),
            **{name: (int(full * sat_scale) if name in dominant else int(quarter * sat_scale)) for name in ("r", "g", "b")},
        }),
        ("continuity_s100_anchor", {
            **{name: 0 for name in CHANNELS},
            **{name: (full if name in dominant else 0) for name in ("r", "g", "b")},
        }),
    ]
    # Drop empty/degenerate entries and keep four distinct commands.
    seen: set[tuple] = set()
    unique: list[tuple[str, dict[str, int]]] = []
    for label, command in candidates:
        key = tuple(sorted(command.items()))
        if key not in seen and any(command.values()):
            seen.add(key)
            unique.append((label, {k: max(0, min(4095, v)) for k, v in command.items()}))
    if len(unique) < 2:
        raise ValueError(f"C1 candidates degenerate for hue {hue}")
    return unique[:4]




def build_guide11_c1_batch_plan(
    *,
    inputs_references: Mapping[str, Mapping[str, Any]] | None = None,
) -> dict[str, Any]:
    """GUIDE11 C1 batch-1 plan: eight remaining HSI main nodes.

    Each target carries one paired Ray reference bracket (q_before/q_after,
    locally acquired per GUIDE11 C1) around its structurally diverse strip
    candidates; per-command independent FAST resets; product-layer z
    chromaticity and legacy 58-feature are reported side by side in analysis.
    """
    from camera_based_rgbww_optimizer.optimization import p7_thermal_diagnostics as thermal

    captures: list[dict[str, Any]] = []
    target_contracts = []
    for target_index, (hue, sat) in enumerate(C1_TARGETS):
        ray_command = {"hue": hue, "sat": sat, "intensity_percent": 100.0}
        candidates = _c1_sector_candidates(hue, sat)
        target_contracts.append({
            "target_index": target_index, "hue": hue, "sat": sat,
            "candidate_labels": [label for label, _ in candidates],
            "candidates": [dict(cmd) for _, cmd in candidates],
        })
        ray_cache = f"ray-c1-h{hue}-s{sat}"
        strip_cache = f"strip-c1-h{hue}-s{sat}"
        bracket = [
            ("ray", "ray_q_before", ray_command, "1/6400", ray_cache),
        ] + [
            ("strip", f"candidate_{index}_{label}", dict(command), "1/400", strip_cache)
            for index, (label, command) in enumerate(candidates)
        ] + [
            ("ray", "ray_q_after", ray_command, "1/6400", ray_cache),
        ]
        for source, role, command, shutter, cache in bracket:
            captures.append({
                "capture_id": f"{len(captures):03d}-{source}-guide11-c1-h{hue}-s{sat}-{role}",
                "source_id": source,
                "state_id": f"C1_H{hue}_S{sat}_{role.upper()}",
                "role": f"{source}_c1_h{hue}_s{sat}_{role}",
                "capture_role": "formal",
                "formal_measurement": True,
                "command": dict(command),
                "exact_command_hash": thermal.canonical_sha256(command),
                "requested_elapsed_s": 120,
                "nominal_shutter": shutter,
                "exposure_cache_key": cache,
                "timing_acceptance": "observed_elapsed_record_only",
                "strip_zero_required": source == "ray",
                "ray_zero_required": source == "strip",
                "session_index": len(captures) + 1,
                "source_order": 1 if source == "ray" else 2,
                "target_cct": None,
                "target_gm": None,
                "c1_hue": hue,
                "c1_sat": sat,
                "steady_claim": False,
            })
    frozen: dict[str, str] = {}
    for step in captures:
        frozen[str(step["exposure_cache_key"])] = str(step["nominal_shutter"])
    return {
        "schema": thermal.PLAN_SCHEMA_V2,
        "status": "execute_authorized",
        "experiment_id": thermal.TD_C,
        "guide_experiment_id": C1_EXPERIMENT_ID,
        "variant": "guide11-c1-hsi-main-nodes",
        "stage": "GUIDE11-C1-HSI-MAIN-NODES",
        "phase": "formal",
        "source": "guide11_c1_remaining_main_nodes",
        "created_at": thermal.datetime.now(thermal.timezone.utc).isoformat(),
        "inputs": {
            "location": thermal.file_reference(thermal.LOCATION_PATH),
            "policy": thermal.file_reference(thermal.POLICY_PATH),
            "code_duty_curve": thermal.file_reference(thermal.CURVE_PATH),
            **{k: dict(v) for k, v in (inputs_references or {}).items()},
        },
        "captures": captures,
        "capture_ids": [step["capture_id"] for step in captures],
        "timing_contract": thermal.timing_contract(2),
        "timing_resolution": "guide11_c1_reset600_D120",
        "cold_proxy": 600,
        "cold_proxy_wait_s": 600,
        "native_raw_ambient_policy": thermal.AMBIENT_POLICY_UNSUBTRACTED_NO_AMBIENT,
        "exposure_setup_required": [],
        "frozen_shutters": frozen,
        "shutter_ledger_provenance": {
            "owner": "experiment_capture_steps",
            "required_cache_keys": sorted(frozen),
            "frozen_shutters_sha256": thermal.canonical_sha256(frozen),
        },
        "budgets": {
            "ray_cap": 16, "strip_cap": 32, "formal_cap": 48,
            "physical_cr3_cap": 48, "ambient_cap": 0, "retry": 0,
            "candidate_batches": 1, "unique_commands_per_target_cap": 4,
        },
        "execution_authorization": {
            "schema": "direct_guide11_c1_hsi_main_nodes_v1",
            "human_authorization_required": False,
            "human_authorization_verified": False,
            "device_use_granted_by": "operator_cli_allow_device_control",
            "experiment_id": C1_EXPERIMENT_ID,
            "bounded_device_scope": True,
            "remote_v2_capability": True,
        },
        "camera": {
            "backend": "remote",
            "v2_capture_timing_capability_available": True,
            "v2_capture_capability": "remote_v2_capture_timing_v1",
            "resolved_capture_settings": {
                "owner": "remote_backend.resolve_capture_settings",
                "iso": "100", "aperture": "f/4", "image_format": "RAW",
            },
        },
        "analysis_contract": {
            "method": "guide11_c1_main_node_batch1",
            "targets": target_contracts,
            "product_layer": "z=[log(R/Gmean), log(B/Gmean)] from paired Ray reference per target",
            "legacy_layer": "frozen 58-feature reported side by side; product pass never mapped to strict pass",
            "sat0_hue_gate": "not_applicable",
            "batch1_command_cap": 4,
            "batch2_entry": "only with measured improvement",
            "closed_routes_not_reopened": ["H120/S100", "H300/S100"],
            "independent_reset_s": 600,
            "dwell_s": 120,
            "best_requires_independent_confirmation": True,
            "steady_claim": False,
        },
    }
