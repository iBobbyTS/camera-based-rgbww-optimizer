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
        # Candidate-tier qualified shutters: full-scale candidates keep the
        # frozen GUIDE9-class 1/400; dimmer white-based candidates get slower
        # tiers so their patches stay above the noise floor without clipping
        # block_06 (verified per capture by the quality system).
        label_shutter = {
            "fullscale_dominant": "1/400",
            "high_white_dominant": "1/8",
            "white_biased_mix": "1/8",
            "continuity_s100_anchor": "1/8",
        }
        ray_shutter = "1/6400" if sat == 50 else "1/1600"
        bracket = [
            ("ray", "ray_q_before", ray_command, ray_shutter, ray_cache),
        ] + [
            (
                "strip", f"candidate_{index}_{label}", dict(command),
                label_shutter.get(label, "1/100"),
                f"{strip_cache}-{label}",
            )
            for index, (label, command) in enumerate(candidates)
        ] + [
            ("ray", "ray_q_after", ray_command, ray_shutter, ray_cache),
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



C1B2_EXPERIMENT_ID = "GUIDE11_C1_BATCH2_V1"


def c1_strip_shutter_for_command(command: Mapping[str, int]) -> str:
    """Exposure-amount shutter tiers for C1/batch2/C4 strip commands.

    Anchored at measured points: full-scale color r4095 normal at 1/400;
    the G9 white anchor (cw4095/ww4095 plus color) also passed at 1/400, so
    mixed white+color commands tier on the conservative brightness proxy
    max(color)+max(white). Multi-channel dimmed secants saturate at 1/8 and
    take 1/125. A SINGLE active color channel is an extreme dynamic-range
    target measured on r2048 (2026-09-28, r1/r2 confirm attempts): block_06
    R sat exactly at the sensor cap at 1/8 (batch-1 passed with zero
    clipped pixels; +0.6 percent ambient tipped it over) while its B plane
    fell below the near-noise floor at 1/125. The measured in-window point
    is 1/25 (R 0.655 of scale, B five times above the failed noise level),
    a legal camera shutter. Saturated frames read LOW in block trimmed
    means, so an over-slow shutter misleads the triage twice.
    """
    channels = {name: int(command.get(name, 0)) for name in ("r", "g", "b")}
    white = max(int(command.get(name, 0)) for name in ("cw", "ww"))
    color = max(channels.values())
    if color == 0:
        return "1/400" if white > 0 else "1/8"
    active = [value for value in channels.values() if value >= 0.05 * color]
    if len(active) <= 1 and white == 0:
        return "1/25"
    brightness = color + white
    if brightness >= 2500:
        return "1/400"
    if brightness >= 1000:
        return "1/125"
    if brightness >= 400:
        return "1/30"
    return "1/8"
C1B2_AUTHORIZATION_SCHEMA = "direct_guide11_c1_batch2_v1"


def build_guide11_c1_batch2_plan(
    batch1_analysis: Mapping[str, Any],
    batch1_run_root: Path,
    *,
    inputs_references: Mapping[str, Mapping[str, Any]] | None = None,
) -> dict[str, Any]:
    """GUIDE11 C1 batch-2: measured-secant bounded search per target.

    Candidates use the same two-stage secant method as W2 applied to the
    product-layer z coordinates: batch-1 (command, z) observations at each
    target give a local sensitivity, and the bounded command step aims the
    best candidate's z at the paired Ray z. Half-steps bound the risk; every
    target keeps its measured fallback outside the batch.
    """
    import json as _json
    import math as _math

    import numpy as np

    from camera_based_rgbww_optimizer.optimization import p7_thermal_diagnostics as thermal

    def z_of_capture(capture_id: str) -> dict[str, float]:
        stats = _json.loads(
            (batch1_run_root / "measurements" / f"{capture_id}.patch-statistics.json")
            .read_text(encoding="utf-8")
        )
        block = next(p for p in stats["patches"] if p.get("index") == 6)
        p = {
            plane: float(block["planes"][plane]["statistics"]["normalized_per_second"]["trimmed_mean"])
            for plane in ("R", "G1", "G2", "B")
        }
        g = 0.5 * (p["G1"] + p["G2"])
        return {"log_R_over_G": _math.log(p["R"] / g), "log_B_over_G": _math.log(p["B"] / g)}

    rows = [
        _json.loads(line)
        for line in (batch1_run_root / "captures.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    command_by_capture = {
        str(row["capture_id"]): {
            name: int(value)
            for name, value in (row.get("plan_step", {}).get("command") or {}).items()
        }
        for row in rows
        if row.get("source_id") == "strip"
    }

    captures: list[dict[str, Any]] = []
    contracts = []
    for target in batch1_analysis.get("results", ()):
        hue, sat = int(target["hue"]), int(target["sat"])
        ray_z = target.get("ray_z_mean")
        best = target.get("best") or {}
        if not ray_z or not best.get("capture_id"):
            continue
        best_id = best["capture_id"]
        base_cmd = command_by_capture.get(best_id)
        if not base_cmd:
            continue
        base_z = z_of_capture(best_id)
        base_vec = np.array([base_z["log_R_over_G"], base_z["log_B_over_G"]])
        target_vec = np.array([ray_z["log_R_over_G"], ray_z["log_B_over_G"]])
        a_rows, b_rows = [], []
        for cand in target.get("candidates_ranked", ()):
            cid = cand.get("capture_id")
            cmd = command_by_capture.get(cid)
            if not cmd or cid == best_id:
                continue
            z = z_of_capture(cid)
            dz = np.array([z["log_R_over_G"], z["log_B_over_G"]]) - base_vec
            dc = np.array([float(cmd[n]) - float(base_cmd[n]) for n in CHANNELS])
            if not dc.any():
                continue
            a_rows.append(dc)
            b_rows.append(dz)
        proposed: list[dict[str, int]] = []
        method = "no_local_sensitivity"
        if a_rows:
            sensitivity, *_ = np.linalg.lstsq(np.asarray(a_rows), np.asarray(b_rows), rcond=None)
            step, *_ = np.linalg.lstsq(sensitivity.T, target_vec - base_vec, rcond=None)
            step = np.clip(step, -768.0, 768.0)
            base_strongest = max(int(base_cmd[name]) for name in CHANNELS)
            brightness_floor = max(1000, int(0.6 * base_strongest))
            for scale in (1.0, 0.5):
                command = {
                    name: max(0, min(4095, int(round(float(base_cmd[name]) + scale * float(step[i])))))
                    for i, name in enumerate(CHANNELS)
                }
                strongest = max(command.values())
                if strongest < brightness_floor:
                    continue  # z is a ratio; secant steps may dim a command
                    # below the measurement system's observability
                if command != base_cmd and command not in proposed:
                    proposed.append(command)
            method = "measured_z_secant_full_step"
        contracts.append({
            "hue": hue, "sat": sat, "method": method,
            "fallback_capture": best_id,
            "fallback_command": base_cmd,
            "fallback_z": base_z,
            "ray_z": ray_z,
            "commands": proposed,
        })
        ray_command = {"hue": hue, "sat": sat, "intensity_percent": 100.0}
        ray_shutter = "1/6400" if sat == 50 else "1/1600"
        ray_cache = f"ray-c1b2-h{hue}-s{sat}"
        bracket = [("ray", "ray_q_before", ray_command, ray_shutter, ray_cache)] + [
            (
                "strip", f"candidate_{i}", dict(command),
                c1_strip_shutter_for_command(command),
                f"strip-c1b2-h{hue}-s{sat}-c{i}",
            )
            for i, command in enumerate(proposed)
        ] + [("ray", "ray_q_after", ray_command, ray_shutter, ray_cache)]
        for source, role, command, shutter, cache in bracket:
            captures.append({
                "capture_id": f"{len(captures):03d}-{source}-guide11-c1b2-h{hue}-s{sat}-{role}",
                "source_id": source,
                "state_id": f"C1B2_H{hue}_S{sat}_{role.upper()}",
                "role": f"{source}_c1b2_h{hue}_s{sat}_{role}",
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
    if not captures:
        raise ValueError("GUIDE11 C1 batch2 has no fittable target")
    frozen = {str(step["exposure_cache_key"]): str(step["nominal_shutter"]) for step in captures}
    strip_count = sum(s["source_id"] == "strip" for s in captures)
    return {
        "schema": thermal.PLAN_SCHEMA_V2,
        "status": "execute_authorized",
        "experiment_id": thermal.TD_C,
        "guide_experiment_id": C1B2_EXPERIMENT_ID,
        "variant": "guide11-c1-batch2-measured-secants",
        "stage": "GUIDE11-C1-BATCH2",
        "phase": "formal",
        "source": "guide11_c1_batch1_measured_improvement",
        "created_at": thermal.datetime.now(thermal.timezone.utc).isoformat(),
        "inputs": {
            "location": thermal.file_reference(thermal.LOCATION_PATH),
            "policy": thermal.file_reference(thermal.POLICY_PATH),
            "code_duty_curve": thermal.file_reference(thermal.CURVE_PATH),
            **{k: dict(v) for k, v in (inputs_references or {}).items()},
        },
        "captures": captures,
        "capture_ids": [s["capture_id"] for s in captures],
        "timing_contract": thermal.timing_contract(2),
        "timing_resolution": "guide11_c1b2_reset600_D120",
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
            "ray_cap": len(captures) - strip_count,
            "strip_cap": strip_count,
            "formal_cap": len(captures),
            "physical_cr3_cap": len(captures),
            "ambient_cap": 0, "retry": 0,
            "per_target_command_cap": 2,
        },
        "execution_authorization": {
            "schema": C1B2_AUTHORIZATION_SCHEMA,
            "human_authorization_required": False,
            "human_authorization_verified": False,
            "device_use_granted_by": "operator_cli_allow_device_control",
            "experiment_id": C1B2_EXPERIMENT_ID,
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
            "method": "guide11_c1_batch2_measured_z_secants",
            "targets": contracts,
            "product_layer": "z distance to paired Ray z per target",
            "batch1_fallback_retained_outside_batch": True,
            "independent_reset_s": 600,
            "dwell_s": 120,
            "steady_claim": False,
        },
    }


C1_CONFIRM_EXPERIMENT_ID = "GUIDE11_C1_CONFIRM_V1"
C1_CONFIRM_AUTHORIZATION_SCHEMA = "direct_guide11_c1_confirm_v1"


def c1_confirm_completed_brackets(
    completed_run_root: Path,
) -> dict[tuple[int, int], list[str]]:
    """Map each target to its accepted capture roles in a (failed) run root.

    In this runner a captures.jsonl row is appended only after a capture's
    post-return processing succeeded (the rejected capture never appears),
    and its patch-statistics artifact exists. A target counts as complete
    only when all four bracket roles (ray_q_before, confirm_1, confirm_2,
    ray_q_after) are present. Partial targets are re-bracketed whole: a Ray
    bracket must be temporally local, so a q_before stranded hours before
    the resumed run cannot certify a fresh q_after.
    """
    import json as _json

    root = Path(completed_run_root)
    captures_path = root / "captures.jsonl"
    if not captures_path.is_file():
        return {}
    roles_by_target: dict[tuple[int, int], set[str]] = {}
    for line in captures_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = _json.loads(line)
        step = row.get("plan_step") or {}
        if "c1_hue" not in step:
            continue
        capture_id = str(row.get("capture_id"))
        if not (root / "measurements" / f"{capture_id}.patch-statistics.json").is_file():
            continue
        roles_by_target.setdefault(
            (int(step["c1_hue"]), int(step["c1_sat"])), set()
        ).add(str(step.get("role", "")).rsplit("_", 1)[-1])
    complete: dict[tuple[int, int], list[str]] = {}
    want = {"before", "1", "2", "after"}
    for key, roles in roles_by_target.items():
        if want.issubset(roles):
            complete[key] = sorted(roles)
    return complete


def build_guide11_c1_confirm_recovery_suffix(
    batch2_analysis_path: Path,
    batch1_run_root: Path,
    completed_run_roots: Sequence[Path] | Path,
    *,
    inputs_references: Mapping[str, Mapping[str, Any]] | None = None,
) -> dict[str, Any]:
    """Recovery suffix for an interrupted C1 confirm run.

    Fully completed targets (all four bracket roles accepted in ANY prior
    root of the failure chain) keep their evidence there and are skipped.
    Partial or untouched targets are re-bracketed completely in a fresh
    root; failed roots are never mutated and their observations remain
    preserved scientific record. Shutter tiers come from the corrected
    exposure-amount rule.
    """
    from camera_based_rgbww_optimizer.optimization import p7_thermal_diagnostics as thermal

    roots = [Path(completed_run_roots)] if isinstance(completed_run_roots, (str, Path)) \
        else [Path(root) for root in completed_run_roots]
    completed: dict[tuple[int, int], list[str]] = {}
    for root in roots:
        for key, roles in c1_confirm_completed_brackets(root).items():
            completed.setdefault(key, roles)
    full = build_guide11_c1_confirm_plan(
        batch2_analysis_path, batch1_run_root, inputs_references=inputs_references
    )
    remaining_contracts = [
        t for t in full["analysis_contract"]["targets"]
        if (int(t["hue"]), int(t["sat"])) not in completed
    ]
    keep_targets = {(int(t["hue"]), int(t["sat"])) for t in remaining_contracts}
    captures = [
        dict(step) for step in full["captures"]
        if (int(step["c1_hue"]), int(step["c1_sat"])) in keep_targets
    ]
    for index, step in enumerate(captures):
        _prefix, rest = step["capture_id"].split("-", 1)
        step["capture_id"] = f"{index:03d}-suffix-{rest}"
        step["session_index"] = index + 1
    frozen = {
        str(step["exposure_cache_key"]): str(step["nominal_shutter"]) for step in captures
    }
    strip_count = sum(s["source_id"] == "strip" for s in captures)
    analysis_contract = dict(full["analysis_contract"])
    analysis_contract["targets"] = remaining_contracts
    analysis_contract["method"] = "guide11_c1_best_repeat_confirmation_recovery_suffix"
    return {
        "schema": full["schema"],
        "status": full["status"],
        "experiment_id": full["experiment_id"],
        "guide_experiment_id": full["guide_experiment_id"],
        "variant": "guide11-c1-best-repeat-confirmation-recovery-suffix",
        "stage": full["stage"],
        "phase": full["phase"],
        "source": "guide11_c1_confirm_recovery_after_engineering_failure",
        "created_at": thermal.datetime.now(thermal.timezone.utc).isoformat(),
        "inputs": dict(full["inputs"]),
        "captures": captures,
        "capture_ids": [s["capture_id"] for s in captures],
        "timing_contract": full["timing_contract"],
        "timing_resolution": full["timing_resolution"],
        "cold_proxy": full["cold_proxy"],
        "cold_proxy_wait_s": full["cold_proxy_wait_s"],
        "native_raw_ambient_policy": full["native_raw_ambient_policy"],
        "exposure_setup_required": list(full["exposure_setup_required"]),
        "frozen_shutters": frozen,
        "shutter_ledger_provenance": {
            "owner": "experiment_capture_steps",
            "required_cache_keys": sorted(frozen),
            "frozen_shutters_sha256": thermal.canonical_sha256(frozen),
        },
        "budgets": {
            "ray_cap": len(captures) - strip_count,
            "strip_cap": strip_count,
            "formal_cap": len(captures),
            "physical_cr3_cap": len(captures),
            "ambient_cap": 0, "retry": 0,
            "confirmations_per_target": 2,
        },
        "execution_authorization": dict(full["execution_authorization"]),
        "camera": dict(full["camera"]),
        "analysis_contract": analysis_contract,
        "recovery": {
            "completed_run_roots": [str(root) for root in roots],
            "completed_targets_kept_in_prior_roots": [
                {"hue": hue, "sat": sat} for (hue, sat) in sorted(completed)
            ],
            "reason": (
                "captures.jsonl rows are appended only after accepted "
                "post-processing; full brackets stay in the failed root, partial "
                "brackets are re-acquired whole (temporal locality of Ray "
                "references)"
            ),
        },
    }


def build_guide11_c1_confirm_plan(
    batch2_analysis_path: Path,
    batch1_run_root: Path,
    *,
    inputs_references: Mapping[str, Mapping[str, Any]] | None = None,
) -> dict[str, Any]:
    """GUIDE11 C1 best-repeat confirmation for the eight main nodes.

    Each target's final selected command (batch-2 improvement when measured,
    otherwise its batch-1 fallback) gets two additional independent FAST
    observations inside a fresh Ray bracket, completing the three independent
    FAST observations GUIDE11 C1 requires for a final command. Shutter tiers
    follow the exposure-amount rule validated in batch-2 r6.
    """
    import json as _json

    from camera_based_rgbww_optimizer.optimization import p7_thermal_diagnostics as thermal

    batch2_analysis = _json.loads(
        Path(batch2_analysis_path).read_text(encoding="utf-8")
    )

    batch1_commands: dict[str, dict[str, int]] = {}
    for line in (Path(batch1_run_root) / "captures.jsonl").read_text(
        encoding="utf-8"
    ).splitlines():
        if not line.strip():
            continue
        row = _json.loads(line)
        if row.get("source_id") != "strip":
            continue
        command = row.get("plan_step", {}).get("command") or {}
        batch1_commands[str(row.get("capture_id"))] = {
            name: int(value) for name, value in command.items()
        }

    captures: list[dict[str, Any]] = []
    contracts = []
    for target in batch2_analysis.get("targets", ()):
        hue, sat = int(target["hue"]), int(target["sat"])
        improved = bool(target.get("improved_vs_batch1"))
        if improved:
            selected = target.get("best") or {}
            command = {
                name: int(value)
                for name, value in (selected.get("command") or {}).items()
            }
            selected_capture = selected.get("capture_id")
            selection_batch = "batch2"
            if not command or not selected_capture:
                raise ValueError(f"C1 confirm target h{hue}/s{sat} lacks its batch-2 command")
        else:
            selected_capture = (target.get("batch1_fallback") or {}).get("capture_id")
            command = batch1_commands.get(str(selected_capture) or "")
            selection_batch = "batch1_fallback"
            if not command:
                raise ValueError(
                    f"C1 confirm target h{hue}/s{sat} fallback capture "
                    f"{selected_capture!r} not found in batch-1 run root"
                )
        contracts.append({
            "hue": hue, "sat": sat,
            "selection_batch": selection_batch,
            "selected_capture_id": selected_capture,
            "selected_command": dict(command),
            "selection_z_distance_to_ray": (
                target.get("best", {}).get("z_distance_to_ray")
                if improved
                else (target.get("batch1_fallback") or {}).get("z_distance_to_ray")
            ),
            "selection_frame_is_not_independent_confirmation": True,
            "independent_confirmations_required": 2,
        })
        ray_command = {"hue": hue, "sat": sat, "intensity_percent": 100.0}
        ray_shutter = "1/6400" if sat == 50 else "1/1600"
        ray_cache = f"ray-c1c-h{hue}-s{sat}"
        strip_shutter = c1_strip_shutter_for_command(command)
        bracket = [
            ("ray", "ray_q_before", ray_command, ray_shutter, ray_cache),
            ("strip", "confirm_1", dict(command), strip_shutter, f"strip-c1c-h{hue}-s{sat}-c1"),
            ("strip", "confirm_2", dict(command), strip_shutter, f"strip-c1c-h{hue}-s{sat}-c2"),
            ("ray", "ray_q_after", ray_command, ray_shutter, ray_cache),
        ]
        for source, role, bracket_command, shutter, cache in bracket:
            captures.append({
                "capture_id": f"{len(captures):03d}-{source}-guide11-c1c-h{hue}-s{sat}-{role}",
                "source_id": source,
                "state_id": f"C1C_H{hue}_S{sat}_{role.upper()}",
                "role": f"{source}_c1c_h{hue}_s{sat}_{role}",
                "capture_role": "formal",
                "formal_measurement": True,
                "command": dict(bracket_command),
                "exact_command_hash": thermal.canonical_sha256(bracket_command),
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
    if not captures:
        raise ValueError("GUIDE11 C1 confirm has no target")
    frozen = {str(step["exposure_cache_key"]): str(step["nominal_shutter"]) for step in captures}
    strip_count = sum(s["source_id"] == "strip" for s in captures)
    return {
        "schema": thermal.PLAN_SCHEMA_V2,
        "status": "execute_authorized",
        "experiment_id": thermal.TD_C,
        "guide_experiment_id": C1_CONFIRM_EXPERIMENT_ID,
        "variant": "guide11-c1-best-repeat-confirmation",
        "stage": "GUIDE11-C1-CONFIRM",
        "phase": "formal",
        "source": "guide11_c1_batch2_selection_closeout",
        "created_at": thermal.datetime.now(thermal.timezone.utc).isoformat(),
        "inputs": {
            "location": thermal.file_reference(thermal.LOCATION_PATH),
            "policy": thermal.file_reference(thermal.POLICY_PATH),
            "code_duty_curve": thermal.file_reference(thermal.CURVE_PATH),
            "batch2_analysis": thermal.file_reference(Path(batch2_analysis_path)),
            "batch1_run_root": {"path": str(Path(batch1_run_root))},
            "batch1_captures": thermal.file_reference(
                Path(batch1_run_root) / "captures.jsonl"
            ),
            **{k: dict(v) for k, v in (inputs_references or {}).items()},
        },
        "captures": captures,
        "capture_ids": [s["capture_id"] for s in captures],
        "timing_contract": thermal.timing_contract(2),
        "timing_resolution": "guide11_c1confirm_reset600_D120",
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
            "ray_cap": len(captures) - strip_count,
            "strip_cap": strip_count,
            "formal_cap": len(captures),
            "physical_cr3_cap": len(captures),
            "ambient_cap": 0, "retry": 0,
            "confirmations_per_target": 2,
        },
        "execution_authorization": {
            "schema": C1_CONFIRM_AUTHORIZATION_SCHEMA,
            "human_authorization_required": False,
            "human_authorization_verified": False,
            "device_use_granted_by": "operator_cli_allow_device_control",
            "experiment_id": C1_CONFIRM_EXPERIMENT_ID,
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
            "method": "guide11_c1_best_repeat_confirmation",
            "targets": contracts,
            "product_layer": "z distance to paired fresh Ray z per target; selection frame counted with selection-process flag",
            "legacy_layer": "frozen 58-feature reported side by side",
            "independent_reset_s": 600,
            "dwell_s": 120,
            "steady_claim": False,
        },
    }


def fit_periodic_hue_sat_command_model(
    anchors: Sequence[Mapping[str, Any]],
    *,
    white_layer: Mapping[str, int] | None = None,
) -> dict[str, Any]:
    """Fit per-channel circular-harmonic hue models for each SAT layer.

    GUIDE11 C3: the runtime command model must be periodic in hue (0/360
    continuous) with SAT handled by layer interpolation. Each SAT layer with
    at least three distinct measured hues is fitted with circular harmonics
    of the highest order the anchor count supports (n>=5 -> order 2,
    n==3..4 -> order 1); sparser layers are anchor-only and refuse
    interpolation. SAT0 keeps exactly one white command; hue is not
    applicable there.
    """
    import numpy as np

    layers: dict[int, dict[int, dict[str, int]]] = {}
    sources: dict[int, list[str]] = {}
    for anchor in anchors:
        sat = int(anchor["sat"])
        hue = int(anchor["hue"]) % 360
        layers.setdefault(sat, {})[hue] = {
            name: int(value) for name, value in anchor["command"].items()
        }
        sources.setdefault(sat, []).append(str(anchor.get("source", "")))

    fitted: dict[str, Any] = {}
    for sat in sorted(layers):
        hues = sorted(layers[sat])
        n = len(hues)
        entry: dict[str, Any] = {
            "anchor_hues": hues,
            "anchor_commands": {str(h): layers[sat][h] for h in hues},
            "sources": sorted(set(sources[sat])),
            "anchor_only": n < 3,
        }
        if n >= 3:
            order = 2 if n >= 5 else 1
            theta = np.array([2.0 * math.pi * h / 360.0 for h in hues])
            design = [np.ones(n)]
            for k in range(1, order + 1):
                design.append(np.cos(k * theta))
                design.append(np.sin(k * theta))
            matrix = np.stack(design, axis=1)
            coefficients: dict[str, list[float]] = {}
            residuals: dict[str, float] = {}
            for channel in CHANNELS:
                values = np.array([layers[sat][h].get(channel, 0) for h in hues], dtype=float)
                solution, *_ = np.linalg.lstsq(matrix, values, rcond=None)
                coefficients[channel] = [float(v) for v in solution]
                residuals[channel] = float(np.max(np.abs(matrix @ solution - values)))
            entry.update({
                "anchor_only": False,
                "harmonic_order": order,
                "coefficients": coefficients,
                "max_anchor_residual": residuals,
            })
        fitted[str(sat)] = entry

    return {
        "schema": "guide11_periodic_hue_sat_command_model_v1",
        "channels": list(CHANNELS),
        "white_layer_sat0": (
            {name: int(value) for name, value in (white_layer or {}).items()}
            if white_layer else None
        ),
        "sat0_hue": "not_applicable",
        "layers": fitted,
        "steady_claim": False,
    }


def interpolate_hsi_command(
    model: Mapping[str, Any], hue: float, sat: float
) -> dict[str, Any]:
    """Interpolate the periodic hue x SAT command model.

    SAT0 returns the single white command (hue not applicable). Between SAT
    layers the command blends linearly in SAT at the periodic hue prediction
    of each layer. Layers marked anchor-only refuse non-anchor hues rather
    than copying a nearest hue.
    """
    import numpy as np

    hue = float(hue) % 360.0
    sat = max(0.0, min(100.0, float(sat)))
    layers = model.get("layers") or {}

    def predict(layer: Mapping[str, Any], at_hue: float) -> dict[str, float]:
        if layer.get("anchor_only"):
            raise ValueError(
                "SAT layer is anchor-only; periodic interpolation not supported"
            )
        theta = 2.0 * math.pi * at_hue / 360.0
        basis = [1.0]
        for k in range(1, int(layer["harmonic_order"]) + 1):
            basis.extend((math.cos(k * theta), math.sin(k * theta)))
        vec = np.asarray(basis)
        return {
            channel: float(np.dot(vec, np.asarray(layer["coefficients"][channel])))
            for channel in model.get("channels") or CHANNELS
        }

    if sat == 0.0:
        white = model.get("white_layer_sat0")
        if not white:
            raise ValueError("model has no SAT0 white layer")
        return {
            "command": {k: int(v) for k, v in white.items()},
            "sat_layer": "sat0_white",
            "hue_applicable": False,
            "exact_anchor": False,
            "clipped": [],
            "note": "SAT0: single white target; hue not applicable",
        }

    sats = sorted(float(key) for key in layers)
    lower = None
    upper = None
    for value in sats:
        if value <= sat:
            lower = value
        if value >= sat and upper is None:
            upper = value
    if lower is None and upper is not None and model.get("white_layer_sat0"):
        # Saturation compression below the lowest fitted layer: blend the
        # SAT0 white command toward the lowest periodic layer, hue first.
        lowest = upper
        weight = sat / lowest
        layer_cmd = predict(layers[str(int(lowest))], hue)
        white = {k: float(v) for k, v in model["white_layer_sat0"].items()}
        raw = {
            channel: white.get(channel, 0.0)
            + weight * (layer_cmd.get(channel, 0.0) - white.get(channel, 0.0))
            for channel in layer_cmd
        }
        used = f"sat0..s{int(lowest)}"
        exact_sat = False
        upper = None  # skip the bracketing path below
    if upper is not None and lower is None:
        raise ValueError(f"SAT {sat} outside fitted layer range {sats}")

    if lower is not None and upper is not None:
        if lower == upper:
            raw = predict(layers[str(int(lower))], hue)
            used = f"s{int(lower)}"
            exact_sat = True
        else:
            low_cmd = predict(layers[str(int(lower))], hue)
            high_cmd = predict(layers[str(int(upper))], hue)
            weight = (sat - lower) / (upper - lower)
            raw = {
                channel: low_cmd[channel] + weight * (high_cmd[channel] - low_cmd[channel])
                for channel in low_cmd
            }
            used = f"s{int(lower)}..s{int(upper)}"
            exact_sat = False

    command: dict[str, int] = {}
    clipped: list[str] = []
    for channel, value in raw.items():
        bound = int(round(value))
        if bound < 0:
            bound, _ = 0, clipped.append(channel)
        elif bound > 4095:
            bound, _ = 4095, clipped.append(channel)
        command[channel] = bound

    exact_anchor = False
    if exact_sat and lower is not None:
        anchor_layer = layers.get(str(int(lower)))
        if (
            anchor_layer is not None
            and int(round(hue)) in [int(h) for h in anchor_layer.get("anchor_hues", [])]
            and float(hue).is_integer()
        ):
            exact_anchor = True

    return {
        "command": command,
        "sat_layer": used,
        "hue_applicable": True,
        "exact_anchor": exact_anchor,
        "clipped": clipped,
        "requested_sat": sat,
        "equivalent_sat_note": (
            "requested SAT; measured equivalent SAT requires the C3 anchor-map "
            "inversion against paired Ray references (ambiguity flagged)"
        ),
    }


C4_EXPERIMENT_ID = "GUIDE11_C4_EXPERIENCE_HOLDOUT_V1"
C4_AUTHORIZATION_SCHEMA = "direct_guide11_c4_holdout_v1"
C4_TARGETS: tuple[tuple[int, int], ...] = (
    # Six non-main hues, one per 60-degree sector, mid SAT between the
    # fitted layers (exercises periodic interpolation + layer blending).
    (30, 75), (90, 75), (150, 75), (210, 75), (270, 75), (330, 75),
    # 0/360 continuity point.
    (350, 75),
    # High-curvature sector (b-dominant -> r+b+ww switch between H240/H300).
    (280, 50),
    # Fixed low-SAT holdout points (white-blend saturation compression).
    (90, 20), (210, 10),
)


def _c4_ray_shutter_for_sat(sat: int) -> str:
    """Ray shutter tiers anchored at measured points.

    G9 H0/S0 white used 1/16000; C1 S50 used 1/6400; C1 S100 used 1/1600.
    Low SAT is white-dominant and brightest; mid SAT interpolates the tier.
    """
    if sat <= 25:
        return "1/16000"
    if sat <= 60:
        return "1/6400"
    if sat < 100:
        return "1/3200"
    return "1/1600"


def build_guide11_c4_holdout_plan(
    command_model: Mapping[str, Any],
    *,
    targets: Sequence[tuple[int, int]] = C4_TARGETS,
    label: str = "c4",
    model_provenance: Mapping[str, Any] | None = None,
    inputs_references: Mapping[str, Mapping[str, Any]] | None = None,
) -> dict[str, Any]:
    """GUIDE11 C4 experience-holdout plan for the periodic command model.

    Ten fixed (hue, SAT) targets chosen before capture: six non-main hues
    covering the six 60-degree sectors, one 0/360 continuity point, one
    high-curvature sector point, and two fixed low-SAT points. Each target
    acquires a fresh paired Ray bracket around one strip observation of the
    model's interpolated command. Targets are frozen; no result-dependent
    substitution is permitted.

    ``label`` only affects capture/state identity strings so other GUIDE11
    packages (e.g. the C2 S25 reachability tier) can reuse this bracket
    structure without masquerading as C4 evidence; the default keeps C4 ids.
    """
    from camera_based_rgbww_optimizer.optimization import p7_thermal_diagnostics as thermal

    captures: list[dict[str, Any]] = []
    contracts = []
    for hue, sat in targets:
        resolved = interpolate_hsi_command(command_model, float(hue), float(sat))
        command = resolved["command"]
        contracts.append({
            "hue": hue, "sat": sat,
            "model_command": dict(command),
            "sat_layer_used": resolved["sat_layer"],
            "clipped_channels": list(resolved["clipped"]),
            "checks": ["hue_continuity", "sat_monotonicity", "equivalent_menu_sat_error"],
        })
        ray_command = {"hue": hue, "sat": sat, "intensity_percent": 100.0}
        ray_shutter = _c4_ray_shutter_for_sat(sat)
        ray_cache = f"ray-{label}-h{hue}-s{sat}"
        strip_shutter = c1_strip_shutter_for_command(command)
        bracket = [
            ("ray", "ray_q_before", ray_command, ray_shutter, ray_cache),
            ("strip", "model_point", dict(command), strip_shutter, f"strip-{label}-h{hue}-s{sat}"),
            ("ray", "ray_q_after", ray_command, ray_shutter, ray_cache),
        ]
        for source, role, bracket_command, shutter, cache in bracket:
            captures.append({
                "capture_id": f"{len(captures):03d}-{source}-guide11-{label}-h{hue}-s{sat}-{role}",
                "source_id": source,
                "state_id": f"{label.upper()}_H{hue}_S{sat}_{role.upper()}",
                "role": f"{source}_{label}_h{hue}_s{sat}_{role}",
                "capture_role": "formal",
                "formal_measurement": True,
                "command": dict(bracket_command),
                "exact_command_hash": thermal.canonical_sha256(bracket_command),
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
    frozen = {str(step["exposure_cache_key"]): str(step["nominal_shutter"]) for step in captures}
    strip_count = sum(s["source_id"] == "strip" for s in captures)
    return {
        "schema": thermal.PLAN_SCHEMA_V2,
        "status": "execute_authorized",
        "experiment_id": thermal.TD_C,
        "guide_experiment_id": C4_EXPERIMENT_ID,
        "variant": "guide11-c4-experience-holdout",
        "stage": "GUIDE11-C4-EXPERIENCE-HOLDOUT",
        "phase": "formal",
        "source": "guide11_c3_periodic_command_model",
        "created_at": thermal.datetime.now(thermal.timezone.utc).isoformat(),
        "inputs": {
            "location": thermal.file_reference(thermal.LOCATION_PATH),
            "policy": thermal.file_reference(thermal.POLICY_PATH),
            "code_duty_curve": thermal.file_reference(thermal.CURVE_PATH),
            **{k: dict(v) for k, v in (inputs_references or {}).items()},
        },
        "captures": captures,
        "capture_ids": [s["capture_id"] for s in captures],
        "timing_contract": thermal.timing_contract(2),
        "timing_resolution": "guide11_c4holdout_reset600_D120",
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
            "ray_cap": len(captures) - strip_count,
            "strip_cap": strip_count,
            "formal_cap": len(captures),
            "physical_cr3_cap": len(captures),
            "ambient_cap": 0, "retry": 0,
            "target_count": len(contracts),
            "local_model_corrections_allowed": 1,
        },
        "execution_authorization": {
            "schema": C4_AUTHORIZATION_SCHEMA,
            "human_authorization_required": False,
            "human_authorization_verified": False,
            "device_use_granted_by": "operator_cli_allow_device_control",
            "experiment_id": C4_EXPERIMENT_ID,
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
            "method": "guide11_c4_experience_holdout",
            "targets": contracts,
            "targets_frozen_before_capture": True,
            "model_provenance": dict(model_provenance or {}),
            "product_layer": "z + equivalent hue/SAT via local anchor-map inversion (ambiguity flagged)",
            "legacy_layer": "frozen 58-feature reported side by side",
            "one_local_model_correction_then_new_holdout": True,
            "failure_ranges_reported_separately": True,
            "independent_reset_s": 600,
            "dwell_s": 120,
            "steady_claim": False,
        },
    }


C2_S25_EXPERIMENT_ID = "GUIDE11_C2_SAT_REACHABILITY_S25_V1"
C2_S25_TARGETS: tuple[tuple[int, int], ...] = ((0, 25), (60, 25), (180, 25), (240, 25))


def build_guide11_c2_s25_plan(
    command_model: Mapping[str, Any],
    *,
    targets: Sequence[tuple[int, int]] = C2_S25_TARGETS,
    model_provenance: Mapping[str, Any] | None = None,
    inputs_references: Mapping[str, Mapping[str, Any]] | None = None,
) -> dict[str, Any]:
    """GUIDE11 C2 S25 descent-tier plan for the four main hues.

    Built only when no main-hue node is product-layer valid at S50/S100
    (C2 reachability assessment); S25 is the last descent tier and a still
    invalid outcome closes the hue's downward search without further tiers.
    Reuses the C4 bracket structure (fresh paired Ray bracket around one
    model-command strip observation) with C2 identity and analysis contract.
    """
    plan = build_guide11_c4_holdout_plan(
        command_model,
        targets=targets,
        label="c2",
        model_provenance=model_provenance,
        inputs_references=inputs_references,
    )
    plan["guide_experiment_id"] = C2_S25_EXPERIMENT_ID
    plan["variant"] = "guide11-c2-sat-reachability-s25"
    plan["stage"] = "GUIDE11-C2-SAT-REACHABILITY-S25"
    plan["analysis_contract"]["method"] = "guide11_c2_sat_reachability"
    plan["analysis_contract"]["descent_tier"] = 25
    plan["analysis_contract"]["stop_rule"] = (
        "if S25 remains outside product tolerance the hue's downward SAT "
        "search stops per GUIDE11 C2; report boundary bracket, not hardware limit"
    )
    plan["analysis_contract"]["one_local_model_correction_then_new_holdout"] = False
    for contract in plan["analysis_contract"]["targets"]:
        contract["checks"] = [
            "bracket_consistency",
            "product_layer_validity",
            "equivalent_menu_sat_error",
        ]
    return plan
