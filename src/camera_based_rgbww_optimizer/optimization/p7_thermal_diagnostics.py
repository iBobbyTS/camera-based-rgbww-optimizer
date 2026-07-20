from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Mapping, Sequence

import numpy as np

from camera_based_rgbww_optimizer.measurement.hsi_policy_v2 import (
    AUDIT_THRESHOLDS,
    ordered_unit_shape,
    summarize_within_groups,
)
from camera_based_rgbww_optimizer.paths import PROJECT_ROOT


TD_A = "p7_td_a_cold_settling_v1"
TD_B = "p7_td_b_command_switch_history_v1"
TD_C = "p7_td_c_balanced_source_comparison_v1"
EXPERIMENT_IDS = (TD_A, TD_B, TD_C)
TIMED_POINTS = (60, 120, 300, 600)
SELECTABLE_SETTLE_POINTS = (60, 120, 300)
TIMING_TOLERANCE_S = {60: 2.0, 120: 2.0, 300: 5.0, 600: 5.0}
ACTUAL_EXPOSURE_START_PROVENANCE = "camera_adapter_actual_exposure_start_monotonic"
CHANNELS = ("cw", "ww", "r", "g", "b")
R1_RUN = Path(
    "/Volumes/4T/temp/rgbww-optimizer/hsi-reference-repeatability/"
    "p7-r1-20260719-091000-terminal-retry1"
)
POLICY_PATH = PROJECT_ROOT / "config/hsi/strip-hsi-policy-v2-waiting.json"
OBSERVER_PATH = PROJECT_ROOT / "config/camera/raw-observer.json"
UNCERTAINTY_PATH = PROJECT_ROOT / "config/hsi/strip-hsi-uncertainty.json"
MANIFOLD_PATH = PROJECT_ROOT / "config/hsi/ray-hsi-manifold.json"
LOCATION_PATH = PROJECT_ROOT / "config/location/locations-20260714-211759.json"
CURVE_PATH = PROJECT_ROOT / "config/channel/code-duty-curve.json"
OPERATING_ENVELOPE_PATH = PROJECT_ROOT / "config/hsi/p7-operating-envelope-v1.json"

RAY_STATES = {
    "A": {"hue": 120, "sat": 100, "intensity_percent": 100.0},
    "D": {"hue": 120, "sat": 50, "intensity_percent": 100.0},
    "B": {"hue": 0, "sat": 0, "intensity_percent": 100.0},
    "C": {"hue": 300, "sat": 100, "intensity_percent": 100.0},
}
STRIP_COMMAND_KEYS = {
    "A": "h120-s100-fullscale",
    "D": "h120-s50-fullscale",
    "B": "h0-s0-fullscale",
    "C": "h300-s100-fullscale",
}
REQUIRED_COVARIATES = (
    "monotonic_timestamp_ns", "wall_clock_timestamp", "session_elapsed_s",
    "source_id", "state_id", "exact_command_hash", "source_on_elapsed_s",
    "state_on_elapsed_s", "off_duration_before_s", "previous_state_id",
    "previous_state_dwell_s", "sequence_index", "capture_order", "source_order",
    "ambient_temperature_c", "source_surface_temperature_c", "fan_mode", "power_mode",
    "shutter_seconds", "raw_black_levels", "raw_white_level",
    "load_history_proxy_60s", "load_history_proxy_300s", "load_history_proxy_900s",
)


def canonical_sha256(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")
    ).hexdigest()


def file_reference(path: str | Path) -> dict[str, str]:
    target = Path(path)
    return {"path": str(target), "sha256": hashlib.sha256(target.read_bytes()).hexdigest()}


def load_r1_commands(run_dir: str | Path = R1_RUN) -> dict[str, dict[str, int]]:
    plan = json.loads((Path(run_dir) / "plan.json").read_text(encoding="utf-8"))
    commands = plan.get("commands")
    if not isinstance(commands, Mapping):
        raise ValueError("retained P7-R1 plan lacks its canonical command map")
    output = {
        str(name): {channel: int(command[channel]) for channel in CHANNELS}
        for name, command in commands.items()
    }
    required = set(STRIP_COMMAND_KEYS.values()) | {"h0-s0-scale-relaxed-3072"}
    if set(output) != required:
        raise ValueError("retained P7-R1 command set differs from the frozen five-command set")
    return output


def load_r1_shutters(run_dir: str | Path = R1_RUN) -> dict[str, str | None]:
    rows = [
        json.loads(line) for line in (Path(run_dir) / "captures.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    output: dict[str, str | None] = {}
    for row in rows:
        source = row.get("source")
        if source == "ray":
            state = row["plan_step"]["state"]
            key = f"ray-h{int(state['hue'])}-s{int(state['sat'])}"
        elif source == "strip":
            key = f"strip-{row['plan_step']['command_key']}"
        else:
            continue
        capture = row.get("capture") or {}
        final = (capture.get("auto_exposure_audit") or {}).get("final") or (capture.get("capture") or {})
        shutter = final.get("shutter_speed")
        if shutter:
            if key in output and output[key] != str(shutter):
                raise ValueError(f"retained P7-R1 shutter cache is inconsistent for {key}")
            output[key] = str(shutter)
    required = {
        "ray-h120-s100", "ray-h0-s0", "ray-h300-s100",
        *(f"strip-{name}" for name in STRIP_COMMAND_KEYS.values()),
    }
    if not required.issubset(output):
        raise ValueError("retained P7-R1 lacks a required source/state shutter cache")
    output.setdefault("ray-h120-s50", None)  # TD-B requires a separate non-formal setup capture.
    return output


def _command(source: str, state: str, commands: Mapping[str, Mapping[str, int]]) -> dict[str, Any]:
    if source == "ray":
        return dict(RAY_STATES[state])
    return {channel: int(commands[STRIP_COMMAND_KEYS[state]][channel]) for channel in CHANNELS}


def build_diagnostic_plan(
    experiment_id: str,
    *,
    source: str | None = None,
    variant: str = "core",
    r1_run: str | Path = R1_RUN,
    prerequisite_artifact: str | Path = OPERATING_ENVELOPE_PATH,
    for_execution: bool = False,
    human_authorization: str | None = None,
    exposure_start_capability: bool = False,
) -> dict[str, Any]:
    if experiment_id not in EXPERIMENT_IDS:
        raise ValueError(f"unsupported exact experiment id: {experiment_id}")
    if source not in {None, "ray", "strip"}:
        raise ValueError("source must be ray or strip")
    if experiment_id in {TD_A, TD_B} and source is None:
        raise ValueError("TD-A/TD-B plans are source-specific")
    if experiment_id == TD_C and source is not None:
        raise ValueError("TD-C plans own both sources")
    if experiment_id == TD_C and variant not in {"core", "expansion"}:
        raise ValueError("TD-C variant must be core or expansion")

    envelope = json.loads(Path(prerequisite_artifact).read_text(encoding="utf-8"))
    _enforce_prerequisites(experiment_id, variant, envelope, for_execution=for_execution)
    if for_execution and human_authorization != experiment_id:
        raise PermissionError(f"execution requires exact Human authorization for {experiment_id}")
    if for_execution and not exposure_start_capability:
        raise PermissionError("execution requires camera-adapter actual exposure-start provenance")

    commands = load_r1_commands(r1_run)
    shutters = load_r1_shutters(r1_run)
    inputs = {
        "r1_commands": file_reference(Path(r1_run) / "commands.jsonl"),
        "r1_plan": file_reference(Path(r1_run) / "plan.json"),
        "policy": file_reference(POLICY_PATH),
        "observer": file_reference(OBSERVER_PATH),
        "uncertainty": file_reference(UNCERTAINTY_PATH),
        "manifold": file_reference(MANIFOLD_PATH),
        "location": file_reference(LOCATION_PATH),
        "code_duty_curve": file_reference(CURVE_PATH),
        "operating_envelope": file_reference(prerequisite_artifact),
    }
    plan = {
        "schema": "p7_thermal_diagnostic_plan_v1",
        "status": "execute_authorized" if for_execution else "dry_run_complete_device_locked",
        "experiment_id": experiment_id,
        "variant": variant,
        "source": source,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "inputs": inputs,
        "camera": {
            "backend": "remote", "location": inputs["location"],
            "auto_exposure_in_timed_cycle": False,
            "actual_exposure_start_provenance_required": ACTUAL_EXPOSURE_START_PROVENANCE,
            "adapter_capability_available": bool(exposure_start_capability),
        },
        "cold_proxy": envelope["cold_proxy"],
        "cleanup": {"python_finally": "required", "shell_trap": "EXIT_INT_TERM_HUP_required"},
        "offline_contract": {"env_calls": 0, "network_calls": 0, "device_calls": 0, "all_off_calls": 0},
        "hard_locks": {
            "sentinel_v2": True, "remaining_9": True, "boundary": True,
            "holdout": True, "P8": True, "Gate_6": True,
            "cold_steady_covariance_merge": True,
        },
        "formal_capture_eligible": False,
        "frozen_shutters": shutters,
        "exposure_setup_required": sorted(key for key, value in shutters.items() if value is None),
        "capture_ledger_contract": {
            "formal_measurement": "boolean", "capture_role": ["formal", "ambient"],
            "ambient_counts_as_physical_cr3": True,
        },
        "source_isolation_contract": "independent_both_off_readback_at_run_ambient_and_transition_gates",
    }
    if experiment_id == TD_A:
        plan.update(_td_a_plan(str(source), commands))
    elif experiment_id == TD_B:
        plan.update(_td_b_plan(str(source), commands, envelope))
    else:
        plan.update(_td_c_plan(variant, commands, envelope))
    return plan


def _enforce_prerequisites(
    experiment_id: str, variant: str, envelope: Mapping[str, Any], *, for_execution: bool
) -> None:
    if not for_execution:
        return
    if experiment_id == TD_B and envelope.get("status") != "td_a_pass":
        raise PermissionError("TD-B execute plan is locked until TD-A passes")
    if experiment_id == TD_B and envelope.get("t_formal_provisional_s") not in SELECTABLE_SETTLE_POINTS:
        raise PermissionError("TD-B execute plan requires frozen t_formal_provisional_s in 60/120/300")
    if experiment_id == TD_C and envelope.get("status") not in {"td_b_pass", "td_c_core_pass_waiting_for_planner"}:
        raise PermissionError("TD-C execute plan is locked until TD-B passes")
    if experiment_id == TD_C and envelope.get("t_formal_s") not in SELECTABLE_SETTLE_POINTS:
        raise PermissionError("TD-C execute plan requires frozen t_formal_s in 60/120/300")
    if experiment_id == TD_C and variant == "expansion" and envelope.get("status") != "td_c_core_pass_waiting_for_planner":
        raise PermissionError("TD-C expansion is locked until core Planner acceptance")


def _step(
    source: str, state: str, elapsed: int | None, index: int,
    commands: Mapping[str, Mapping[str, int]], **extra: Any,
) -> dict[str, Any]:
    command = _command(source, state, commands)
    suffix = "deferred" if elapsed is None else str(elapsed)
    return {
        "capture_id": f"{index:03d}-{source}-{state.lower()}-t{suffix}",
        "source_id": source,
        "state_id": state,
        "command": command,
        "exact_command_hash": canonical_sha256(command),
        "requested_elapsed_s": elapsed,
        "timing_tolerance_s": None if elapsed is None else TIMING_TOLERANCE_S.get(elapsed, 5.0),
        "timing_status": "resolved" if elapsed is not None else "deferred",
        "formal_measurement": True,
        "capture_role": "formal",
        **extra,
    }


def _ambient_step(index: int, *, position: str, **extra: Any) -> dict[str, Any]:
    return {
        "capture_id": f"{index:03d}-ambient-{position}",
        "source_id": "ambient", "state_id": "ambient",
        "command": None, "exact_command_hash": canonical_sha256({"strip": "off", "ray": "off"}),
        "requested_elapsed_s": None, "timing_tolerance_s": None,
        "timing_status": "diagnostic_not_timed", "formal_measurement": False,
        "capture_role": "ambient", "ambient_position": position,
        **extra,
    }


def _td_a_plan(source: str, commands: Mapping[str, Mapping[str, int]]) -> dict[str, Any]:
    steps = [_ambient_step(0, position="start", isolation_gate_before="run_start_ambient_start")]
    for cycle in range(1, 4):
        for elapsed in TIMED_POINTS:
            steps.append(_step(
                source, "A", elapsed, len(steps), commands, cycle_index=cycle,
                isolation_gate_after=(f"after_cycle_{cycle}" if elapsed == 600 else None),
            ))
        if cycle == 2:
            steps.append(_ambient_step(
                len(steps), position="mid", cycle_index=cycle,
                isolation_gate_before="after_cycle_2_ambient_mid",
            ))
    steps.append(_ambient_step(
        len(steps), position="end", isolation_gate_before="after_cycle_3_ambient_end",
    ))
    return {
        "stage": "TD-A", "timing_schedule_s": list(TIMED_POINTS), "cycles": 3,
        "cold_proxy_wait_s": 1800,
        "captures": steps, "budgets": {"formal_cap": 12, "ambient_cap": 3, "physical_cr3_cap": 22},
        "continuous_command_between_timed_points": True,
        "exposure": {"source_specific_shutter_frozen_before_cycle": True, "setup_is_nonformal": True},
        "analysis_contract": {"settle_candidates_s": list(SELECTABLE_SETTLE_POINTS), "six_hundred_is_validation_only": True},
    }


def _td_b_plan(source: str, commands: Mapping[str, Mapping[str, int]], envelope: Mapping[str, Any]) -> dict[str, Any]:
    provisional = envelope.get("t_formal_provisional_s")
    schedule: list[tuple[str, int | None, str]] = [("A", 600, "initial_anchor")]
    for state in ("D", "B", "C"):
        schedule.extend((state, elapsed, "switch_curve") for elapsed in TIMED_POINTS)
        schedule.append(("A", None if provisional is None else int(provisional), f"return_after_{state}"))
    steps = []
    for index, (state, elapsed, role) in enumerate(schedule):
        next_group = None if index + 1 == len(schedule) else (schedule[index + 1][0], schedule[index + 1][2])
        current_group = (state, role)
        steps.append(_step(
            source, state, elapsed, index, commands, role=role,
            timing_status=("deferred_until_td_a" if elapsed is None else "resolved"),
            isolation_gate_after=(f"after_{role}" if next_group != current_group else None),
        ))
    return {
        "stage": "TD-B", "captures": steps,
        "budgets": {"formal_cap": 16, "ambient_cap": 0, "physical_cr3_cap": 24},
        "timing_resolution": "deferred_until_td_a" if provisional is None else "resolved",
        "continuous_command_between_timed_points": True,
        "analysis_contract": {"return_anchor_states": ["A0", "A_after_D", "A_after_B", "A_after_C"]},
        "execute_lock": "td_a_pass_required",
    }


def _td_c_plan(variant: str, commands: Mapping[str, Mapping[str, int]], envelope: Mapping[str, Any]) -> dict[str, Any]:
    if variant == "core":
        states = ("A",)
        orders = (("ray", "strip"), ("strip", "ray"), ("ray", "strip"), ("strip", "ray"))
        physical = 16
    else:
        states = ("B", "C")
        orders = (("ray", "strip"), ("strip", "ray"))
        physical = 20
    formal_value = envelope.get("t_formal_s")
    elapsed = None if formal_value is None else int(formal_value)
    steps = []
    for state in states:
        for session_index, order in enumerate(orders, start=1):
            steps.append(_ambient_step(
                len(steps), position=f"session_{session_index}_{state}_start",
                state_group=state, session_index=session_index,
                isolation_gate_before=f"session_{session_index}_{state}_start_ambient",
            ))
            for source_order, source in enumerate(order, start=1):
                steps.append(_step(
                    source, state, elapsed, len(steps), commands,
                    session_index=session_index, source_order=source_order,
                    timing_status=("deferred_until_td_b" if elapsed is None else "resolved"),
                    isolation_gate_after=f"session_{session_index}_{state}_after_{source}",
                ))
            steps.append(_ambient_step(
                len(steps), position=f"session_{session_index}_{state}_end",
                state_group=state, session_index=session_index,
                isolation_gate_before=f"session_{session_index}_{state}_end_ambient",
            ))
    return {
        "stage": "TD-C", "comparison_design": "order_balanced_paired_comparison_not_classic_abba",
        "cold_proxy_wait_s": 1800,
        "session_orders": [list(order) for order in orders], "captures": steps,
        "budgets": {"formal_cap": 8, "ambient_cap": 8, "physical_cr3_cap": physical},
        "timing_resolution": "deferred_until_td_b" if elapsed is None else "resolved",
        "execute_lock": "td_b_pass_required" if variant == "core" else "td_c_core_planner_acceptance_required",
    }


@dataclass(frozen=True)
class TimedCaptureResult:
    requested_elapsed_s: float
    actual_elapsed_s: float
    timing_error_s: float
    timing_valid: bool
    capture: Mapping[str, Any]


def run_timed_schedule(
    requested_points_s: Sequence[int],
    *,
    command_apply_fn: Callable[[], Any],
    readback_fn: Callable[[], Any],
    capture_fn: Callable[[int], Mapping[str, Any]],
    monotonic_fn: Callable[[], float],
    sleep_fn: Callable[[float], None],
) -> list[TimedCaptureResult]:
    command_apply_fn()
    readback_fn()
    owner_start = monotonic_fn()
    output = []
    for requested in requested_points_s:
        remaining = owner_start + float(requested) - monotonic_fn()
        if remaining > 0:
            sleep_fn(remaining)
        capture = dict(capture_fn(int(requested)))
        if capture.get("exposure_start_provenance") != ACTUAL_EXPOSURE_START_PROVENANCE:
            raise ValueError("timed capture lacks camera-adapter actual exposure-start provenance")
        if "exposure_start_monotonic_s" not in capture:
            raise ValueError("timed capture lacks camera-adapter actual exposure-start timestamp")
        actual = float(capture["exposure_start_monotonic_s"]) - owner_start
        error = actual - float(requested)
        tolerance = TIMING_TOLERANCE_S[int(requested)]
        output.append(TimedCaptureResult(float(requested), actual, error, abs(error) <= tolerance, capture))
    return output


def strip_duty(command: Mapping[str, int], curve: Mapping[str, Any]) -> dict[str, float]:
    points = curve.get("channels", curve)
    result: dict[str, float] = {}
    for channel in CHANNELS:
        channel_data = points[channel]
        entries = channel_data.get("measured_points", channel_data) if isinstance(channel_data, Mapping) else channel_data
        xs = np.asarray([float(item["code"] if isinstance(item, Mapping) else item[0]) for item in entries])
        ys = np.asarray([float(item.get("duty", item.get("linear", 0.0)) if isinstance(item, Mapping) else item[1]) for item in entries])
        result[channel] = float(np.interp(float(command[channel]), xs, ys))
    return result


def build_covariate_record(
    *, source_id: str, state_id: str, command: Mapping[str, Any], sequence_index: int,
    capture_order: int, source_order: int, monotonic_timestamp_ns: int,
    wall_clock_timestamp: str, session_elapsed_s: float, source_on_elapsed_s: float,
    state_on_elapsed_s: float, off_duration_before_s: float,
    previous_state_id: str | None, previous_state_dwell_s: float | None,
    shutter_seconds: float, raw_black_levels: Sequence[float], raw_white_level: float,
    load_history: Mapping[int, float], readback: Mapping[str, Any] | None = None,
    curve: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    record = {
        "monotonic_timestamp_ns": int(monotonic_timestamp_ns),
        "wall_clock_timestamp": str(wall_clock_timestamp),
        "session_elapsed_s": float(session_elapsed_s), "source_id": source_id,
        "state_id": state_id, "exact_command_hash": canonical_sha256(command),
        "source_on_elapsed_s": float(source_on_elapsed_s), "state_on_elapsed_s": float(state_on_elapsed_s),
        "off_duration_before_s": float(off_duration_before_s), "previous_state_id": previous_state_id,
        "previous_state_dwell_s": previous_state_dwell_s, "sequence_index": int(sequence_index),
        "capture_order": int(capture_order), "source_order": int(source_order),
        "ambient_temperature_c": None, "source_surface_temperature_c": None,
        "fan_mode": None, "power_mode": None, "shutter_seconds": float(shutter_seconds),
        "raw_black_levels": [float(value) for value in raw_black_levels],
        "raw_white_level": float(raw_white_level),
        "load_history_proxy_60s": float(load_history[60]),
        "load_history_proxy_300s": float(load_history[300]),
        "load_history_proxy_900s": float(load_history[900]),
    }
    if source_id == "strip":
        if curve is None:
            raise ValueError("strip covariates require the frozen code-duty curve")
        duty = strip_duty({key: int(command[key]) for key in CHANNELS}, curve)
        record.update({key: int(command[key]) for key in CHANNELS})
        record["linearized_duty"] = duty
        record["sum_duty"] = float(sum(duty.values()))
        record["rolling_integrated_sum_duty_history"] = {str(key): float(load_history[key]) for key in (60, 300, 900)}
    elif source_id == "ray":
        record["hsi_command"] = dict(command)
        record["hsi_readback"] = None if readback is None else dict(readback)
        record["rolling_int_on_history"] = {str(key): float(load_history[key]) for key in (60, 300, 900)}
        record["load_proxy_quality"] = "command_only_not_electrical_power"
    elif source_id == "ambient":
        record["ambient_diagnostic_only"] = True
        record["both_sources_verified_off"] = True
    else:
        raise ValueError("covariate source must be ray, strip, or ambient")
    validate_covariate_record(record, expected_command=command)
    return record


def validate_covariate_record(record: Mapping[str, Any], *, expected_command: Mapping[str, Any]) -> None:
    missing = [key for key in REQUIRED_COVARIATES if key not in record]
    if missing:
        raise ValueError(f"thermal covariate fields missing: {missing}")
    if record["exact_command_hash"] != canonical_sha256(expected_command):
        raise ValueError("thermal covariate command hash mismatch")
    for key in ("ambient_temperature_c", "source_surface_temperature_c"):
        value = record[key]
        if value is not None and (not isinstance(value, (int, float)) or not np.isfinite(value)):
            raise ValueError(f"invalid temperature covariate: {key}")
    if int(record["sequence_index"]) < 0 or int(record["capture_order"]) < 0:
        raise ValueError("chronology indices must be nonnegative")


def settle_from_cycles(
    cycles: Mapping[str, Mapping[int, Sequence[Mapping[str, float]]]],
    feature_ids: Sequence[str],
    *,
    compatibility_fn: Callable[[Sequence[float], Sequence[float]], bool] | None = None,
) -> dict[str, Any]:
    compatibility = compatibility_fn or (lambda left, right: bool(np.linalg.norm(np.asarray(left) - np.asarray(right)) <= 1e-9))
    normalized: dict[str, dict[int, np.ndarray]] = {}
    for cycle, rows in cycles.items():
        normalized[cycle] = {
            int(point): np.mean(np.vstack([ordered_unit_shape(row, feature_ids) for row in values]), axis=0)
            for point, values in rows.items()
        }
    for candidate in SELECTABLE_SETTLE_POINTS:
        candidate_centers = [rows[candidate] for rows in normalized.values() if candidate in rows]
        if len(candidate_centers) != len(normalized) or not _all_pairs(candidate_centers, compatibility):
            continue
        valid = True
        for rows in normalized.values():
            if any(not compatibility(rows[candidate], rows[later]) for later in TIMED_POINTS if later > candidate):
                valid = False
                break
        if valid:
            return {"status": "pass", "t_settle_s": candidate, "six_hundred_is_validation_only": True}
    return {"status": "settling_not_demonstrated_by_600", "t_settle_s": None, "six_hundred_is_validation_only": True}


def _all_pairs(values: Sequence[Sequence[float]], fn: Callable[[Sequence[float], Sequence[float]], bool]) -> bool:
    return all(fn(values[left], values[right]) for left in range(len(values)) for right in range(left + 1, len(values)))


def audit_chronology(rows: Sequence[Mapping[str, Any]]) -> None:
    if [int(row["sequence_index"]) for row in rows] != list(range(len(rows))):
        raise ValueError("thermal covariate sequence is missing, duplicated, or reordered")
    timestamps = [int(row["monotonic_timestamp_ns"]) for row in rows]
    if timestamps != sorted(timestamps) or len(timestamps) != len(set(timestamps)):
        raise ValueError("thermal covariate monotonic timestamps are not strictly increasing")


def summarize_group_audit(groups: Mapping[str, Sequence[Mapping[str, float]]], feature_ids: Sequence[str]) -> dict[str, Any]:
    summary = summarize_within_groups(groups, feature_ids)
    failures = summary["audit"]["failure_branches"]
    trend_failed = any(item.get("branch") == "trend" and float(item.get("score", 0)) > AUDIT_THRESHOLDS["trend_whitened_limit"] for item in failures)
    dominance_failed = any(item.get("branch") == "single_frame_dominance" for item in failures)
    return {"summary": summary, "trend_failed": trend_failed, "dominance_failed": dominance_failed}
