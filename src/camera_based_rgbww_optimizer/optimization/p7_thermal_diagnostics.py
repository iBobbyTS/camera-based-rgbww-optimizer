from __future__ import annotations

import hashlib
import json
import math
from copy import deepcopy
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Mapping, Sequence
from types import MappingProxyType

import numpy as np

from camera_based_rgbww_optimizer.measurement.hsi_policy_v2 import (
    AUDIT_THRESHOLDS, ordered_unit_shape, summarize_within_groups,
)
from camera_based_rgbww_optimizer.optimization.measure_raw_observer_validation import (
    AMBIENT_POLICY_REQUIRE_PRECEDING, AMBIENT_POLICY_UNSUBTRACTED_NO_AMBIENT,
)
from camera_based_rgbww_optimizer.paths import PROJECT_ROOT

TD_A = "p7_td_a_cold_settling_v1"
TD_B = "p7_td_b_command_switch_history_v1"
TD_C = "p7_td_c_balanced_source_comparison_v1"
TD_C_FAST_ENDPOINT_HOLDOUT_EXPERIMENT_ID = (
    "GUIDE5_TD_C_FAST_ENDPOINT_HOLDOUT_B_C_V1"
)
TD_C_FAST_ENDPOINT_HOLDOUT_VARIANT = "fast-endpoint-holdout-b-c"
TD_C_FAST_ANCHOR_DIRECTION_B_EXPERIMENT_ID = "GUIDE5_TD_C_FAST_ANCHOR_DIRECTION_B_V1"
TD_C_FAST_ANCHOR_DIRECTION_B_VARIANT = "fast-anchor-direction-b"
GUIDE6_DIRECT_TARGET_LOCAL_H120_S100_EXPERIMENT_ID = "GUIDE6-DIRECT-TARGET-LOCAL-H120-S100-V1"
GUIDE6_DIRECT_TARGET_LOCAL_H120_S100_VARIANT = "guide6-direct-target-local-h120-s100"
EXPERIMENT_IDS = (TD_A, TD_B, TD_C)
TIMED_POINTS = (60, 120, 300, 600)
SELECTABLE_SETTLE_POINTS = (60, 120, 300)
PLAN_SCHEMA_V1 = "p7_thermal_diagnostic_plan_v1"
PLAN_SCHEMA_V2 = "p7_thermal_diagnostic_plan_v2"
ANALYSIS_SCHEMA_V2 = "p7_thermal_diagnostic_analysis_v2"
_TIMING_CONTRACT_V1_TEMPLATE = {
    "name": "best_effort_gphoto2_v1",
    "decision_owner": "Developer/Human",
    "network_assumption": "wired_lan_latency_negligible_developer_decision",
    "accepted_tiers": ["tier_a", "tier_b"],
    "absolute_exposure_start_required": False,
    "absolute_exposure_start": False,
    "provenance": "best_effort_gphoto2_exposure_start_estimate",
}
_TIMING_CONTRACT_V2_TEMPLATE = {
    "name": "best_effort_gphoto2_observed_elapsed_v2",
    "decision_owner": "Developer/Human",
    "network_assumption": "wired_lan_latency_negligible_developer_decision",
    "accepted_tiers": ["tier_a", "tier_b"],
    "absolute_exposure_start_required": False,
    "absolute_exposure_start": False,
    "provenance": "best_effort_gphoto2_exposure_start_estimate",
    "nominal_slot_semantics": "scheduler_target_only",
    "acceptance_basis": "evidence_integrity_not_nominal_proximity",
    "nominal_offset_gate": "none_developer_decision",
}
ACCEPTED_TIMING_TIERS = frozenset(("tier_a", "tier_b"))
TIMING_CONTRACT_V1 = MappingProxyType({
    **_TIMING_CONTRACT_V1_TEMPLATE,
    "accepted_tiers": tuple(_TIMING_CONTRACT_V1_TEMPLATE["accepted_tiers"]),
})
TIMING_CONTRACT_V2 = MappingProxyType({
    **_TIMING_CONTRACT_V2_TEMPLATE,
    "accepted_tiers": tuple(_TIMING_CONTRACT_V2_TEMPLATE["accepted_tiers"]),
})
def timing_contract(version: int) -> dict[str, Any]:
    if version == 1:
        return deepcopy(_TIMING_CONTRACT_V1_TEMPLATE)
    if version == 2:
        return deepcopy(_TIMING_CONTRACT_V2_TEMPLATE)
    raise ValueError(f"unsupported thermal timing contract version: {version}")

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
TD_B_EXPOSURE_POLICY_V2_PATH = PROJECT_ROOT / "config/hsi/p7-ray-td-b-exposure-policy-v2.json"
RAY_HISTORY_DWELL_POLICY_PATH = PROJECT_ROOT / "config/hsi/p7-human-dwell-policy-v1.json"
TD_B_EXPOSURE_POLICY_V2_SCHEMA = "p7_ray_td_b_exposure_policy_v2"
TD_B_R6_EXPERIMENT_ID = "P7-TD-B-RAY-OP600-EXPOSURE-GUARDED-FORMAL-R6"
RAY_HISTORY_3X3_EXPERIMENT_ID = "GUIDE4-RAY-HISTORY-ORDER-BALANCED-3X3-OP120-COLD600-V3"
STRIP_HISTORY_3X3_EXPERIMENT_ID = "GUIDE5-STRIP-HISTORY-ORDER-BALANCED-3X3-OP120-RESET600-V1"
RAY_FAST_LONG_BRIDGE_EXPERIMENT_ID = (
    "GUIDE5-RAY-FAST-LONG-BRIDGE-OP120-OP600-RESET600-RESET1800-V1"
)
RAY_FAST_TARGET_PATH = PROJECT_ROOT / "config/hsi/ray-fast-op120-targets-v1.json"
TD_C_CORE_CONTRAST_ARTIFACT = Path(
    "/Volumes/4T/temp/rgbww-optimizer/guide5-td-c-core-20260812-151638-noambient-fix/"
    "analysis-v2.1-td-c-core-contrasts-derived.json"
)
COMBINED_FAST_HISTORY_ARTIFACT = Path(
    "/Volumes/4T/temp/rgbww-optimizer/guide5-ray-fast-long-bridge-20260810-194802/"
    "p7-combined-fast-history-coordinate-v1.json"
)
RAY_FAST_LONG_BRIDGE_MINI_SESSIONS = (
    ("C", "FAST", 600, 120),
    ("C", "LONG", 1800, 600),
    ("B", "LONG", 1800, 600),
    ("B", "FAST", 600, 120),
)
RAY_HISTORY_3X3_SESSION_ORDERS = (("D", "B", "C"), ("C", "D", "B"), ("B", "C", "D"))
RAY_HISTORY_OPERATIONAL_DWELL_S = 120
RAY_HISTORY_SESSION_COLD_PROXY_S = 600
RAY_HISTORY_SESSION_START_CONDITION = (
    "Ray and strip continuously off for at least 600 s after prior high load; "
    "both-source zero readback passes at run start"
)
TD_B_R5_PLAN_SHA256 = "94da09f240e2d0ca84ce545c52748522dfbaa9a674bf96ffcef5c8e74473ba9f"
TD_B_R5_SHUTTERS_SHA256 = "b49dd52ebc1eabc8ae6ae0e3713884e5e939428d0682e6d7234eea8c17626e71"
TD_B_FEATURE_IDS_SHA256 = "4a37bf13a1dcfa6b652bd4ce6a7793aa8ac0344c293d1a7fc73ff7fad763ab86"
TD_B_R5_FAILURE_CLASS = (
    "state_specific_exposure_policy_failure_with_required_feature_observer_saturation"
)
TD_B_EQ_CANDIDATES = ("1/2500", "1/3200")
TD_B_R6_CAPTURE_IDS = (
    "000-ray-a0-t600",
    "001-ray-d-t60", "002-ray-d-t120", "003-ray-d-t300", "004-ray-d-t600",
    "005-ray-a-after-d-t600",
    "006-ray-b-t60", "007-ray-b-t120", "008-ray-b-t300", "009-ray-b-t600",
    "010-ray-a-after-b-t600",
    "011-ray-c-t60", "012-ray-c-t120", "013-ray-c-t300", "014-ray-c-t600",
    "015-ray-a-after-c-t600",
)
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
PHYSICAL_RETURN_LEDGER_SCHEMA = "p7_thermal_physical_return_v1"
def canonical_sha256(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")
    ).hexdigest()

def expected_native_raw_ambient_policy(
    experiment_id: str,
    *,
    plan_schema: str,
    phase: str = "formal",
) -> str:
    if (
        experiment_id in {TD_B, TD_C}
        and plan_schema == PLAN_SCHEMA_V2
        and phase == "formal"
    ):
        return AMBIENT_POLICY_UNSUBTRACTED_NO_AMBIENT
    if experiment_id == TD_C and plan_schema == PLAN_SCHEMA_V2 and phase == "formal":
        return AMBIENT_POLICY_UNSUBTRACTED_NO_AMBIENT
    return AMBIENT_POLICY_REQUIRE_PRECEDING

def file_reference(path: str | Path) -> dict[str, str]:
    target = Path(path)
    return {"path": str(target), "sha256": hashlib.sha256(target.read_bytes()).hexdigest()}

def load_td_b_exposure_policy_v2(
    path: str | Path = TD_B_EXPOSURE_POLICY_V2_PATH,
) -> dict[str, Any]:
    """Load and validate the single versioned R6 exposure-policy owner."""
    target = Path(path)
    if target.resolve(strict=True) != TD_B_EXPOSURE_POLICY_V2_PATH.resolve(strict=True):
        raise ValueError("TD-B exposure policy must use the repository-owned v2 artifact")
    policy = json.loads(target.read_text(encoding="utf-8"))
    if policy.get("schema") != TD_B_EXPOSURE_POLICY_V2_SCHEMA:
        raise ValueError("unsupported TD-B exposure policy schema")
    if policy.get("supersedes") != TD_B_R5_SHUTTERS_SHA256:
        raise ValueError("TD-B exposure policy does not supersede the exact R5 shutter ledger")
    superseded = policy.get("superseded_plan")
    if not isinstance(superseded, Mapping) or superseded.get("sha256") != TD_B_R5_PLAN_SHA256:
        raise ValueError("TD-B exposure policy lacks exact R5 plan provenance")
    if policy.get("iso") != 100 or policy.get("aperture") != "implicit_auto":
        raise ValueError("TD-B exposure policy camera settings drifted")
    if policy.get("actual_exposure_owner") != "Canon:ExposureTime":
        raise ValueError("TD-B recorded exposure owner drifted")
    states = policy.get("states")
    expected = {"A": "1/5000", "D": "1/6400", "B": "1/8000"}
    if not isinstance(states, Mapping) or any(
        not isinstance(states.get(state), Mapping)
        or states[state].get("formal_shutter") != shutter
        or states[state].get("source") != "exact_r5_frozen_plan"
        for state, shutter in expected.items()
    ):
        raise ValueError("TD-B A/D/B shutters differ from exact R5 provenance")
    c_state = states.get("C")
    if (
        not isinstance(c_state, Mapping)
        or c_state.get("status") != "qualified"
        or tuple(c_state.get("nominal_candidates", ())) != TD_B_EQ_CANDIDATES
        or c_state.get("formal_shutter") != "1/2500"
    ):
        raise ValueError("TD-B C exposure differs from exact accepted EQ qualification")
    if (
        policy.get("r5_failure_class") != TD_B_R5_FAILURE_CLASS
        or policy.get("exposure_qualification_status") != "qualified_1_2500"
        or policy.get("selected_state_c_nominal_shutter") != "1/2500"
        or policy.get("selected_state_c_recorded_exposure_range") != {
            "owner": "Canon:ExposureTime",
            "min_seconds": 0.000387549084953174,
            "max_seconds": 0.000387549084953174,
        }
    ):
        raise ValueError("TD-B selected C exposure qualification drifted")
    prohibited_claims = {
        "formal_pass", "td_b_pass", "history_pass", "release_usable",
        "production_release_usable", "product_ready", "state_c_settled",
    }
    if prohibited_claims.intersection(policy):
        raise ValueError("TD-B exposure policy contains a prohibited downstream claim")
    if policy.get("old_new_frame_combination") != "prohibited":
        raise ValueError("TD-B exposure policy must prohibit old/new pooling")
    return policy

def validate_td_b_exposure_policy_v2(policy: Mapping[str, Any]) -> None:
    """Validate an in-memory policy without permitting a compatibility variant."""
    owner = load_td_b_exposure_policy_v2()
    if dict(policy) != owner:
        raise ValueError("in-memory TD-B exposure policy differs from the repository owner")

def td_b_eq_capture_quality_failures(
    capture: Mapping[str, Any],
    *,
    required_feature_ids: Sequence[str],
) -> tuple[str, ...]:
    """Apply the frozen 58-feature and engineering gates to one EQ return."""
    required = tuple(str(value) for value in required_feature_ids)
    if len(required) != 58 or canonical_sha256(list(required)) != TD_B_FEATURE_IDS_SHA256:
        raise ValueError("EQ-R6 requires the exact ordered 58-feature owner")
    failures: list[str] = []
    if capture.get("physical_return_persisted_before_postprocessing") is not True:
        failures.append("physical_return_evidence")
    for evidence_name in ("cr3", "sidecar"):
        evidence = capture.get(evidence_name)
        if (
            not isinstance(evidence, Mapping)
            or not isinstance(evidence.get("path"), str)
            or not evidence.get("path")
            or int(evidence.get("bytes", 0)) <= 0
            or not isinstance(evidence.get("sha256"), str)
            or len(evidence.get("sha256", "")) != 64
        ):
            failures.append(f"{evidence_name}_evidence")
    if not capture.get("remote_capture_id") or not capture.get("remote_request_id"):
        failures.append("remote_ids")
    recorded = capture.get("recorded_exposure")
    if (
        not isinstance(recorded, Mapping)
        or recorded.get("source") != "Canon:ExposureTime"
        or recorded.get("status") != "recorded"
        or not math.isfinite(float(recorded.get("seconds", math.nan)))
    ):
        failures.append("recorded_exposure")
    if capture.get("nominal_recorded_ratio_gate") != "pass":
        failures.append("nominal_recorded_ratio")
    for gate in (
        "ray_command_readback", "strip_zero", "source_isolation",
        "timing_chronology", "no_stale", "budget_accounting",
    ):
        if capture.get(gate) != "pass":
            failures.append(gate)
    quality = capture.get("feature_quality")
    if not isinstance(quality, Mapping) or tuple(quality) != required:
        failures.append("required_58_features")
        return tuple(failures)
    for feature_id in required:
        row = quality[feature_id]
        if not isinstance(row, Mapping):
            failures.append("required_58_features")
            continue
        value = row.get("value")
        if value is None or not math.isfinite(float(value)):
            failures.append("nonfinite")
        if float(row.get("clipped_fraction", math.inf)) != 0.0:
            failures.append("clipping")
        if float(row.get("near_noise_floor_fraction", math.inf)) > 0.05:
            failures.append("near_noise")
        if int(row.get("valid_pixel_count", -1)) < 29000:
            failures.append("valid_pixel")
    return tuple(sorted(set(failures)))

def classify_td_b_eq_r6(
    candidate_results: Sequence[Sequence[Mapping[str, Any]]],
    *,
    required_feature_ids: Sequence[str],
) -> dict[str, Any]:
    """Classify the exact two-candidate gate, including the sole C2 unlock."""
    if not candidate_results or len(candidate_results) > 2:
        raise ValueError("EQ-R6 requires one or at most two candidate result ledgers")
    first_failures = [
        td_b_eq_capture_quality_failures(row, required_feature_ids=required_feature_ids)
        for row in candidate_results[0]
    ]
    if not first_failures or len(first_failures) > 4:
        raise ValueError("candidate 1 must contain one to four returned slots")
    first_bad = next((item for item in first_failures if item), None)
    if first_bad is None:
        if len(first_failures) != 4 or len(candidate_results) != 1:
            raise ValueError("qualified candidate 1 requires 4/4 and zero candidate 2 calls")
        return {"status": "qualified_1_2500", "selected_shutter": "1/2500", "candidate_2_call_count": 0}
    if set(first_bad) != {"clipping"}:
        if len(candidate_results) != 1:
            raise ValueError("non-clipping candidate 1 failure prohibits candidate 2")
        return {"status": "run_invalid", "selected_shutter": None, "candidate_2_call_count": 0}
    if first_failures.index(first_bad) != len(first_failures) - 1:
        raise ValueError("candidate 1 continued after its first clipping failure")
    if len(candidate_results) != 2:
        return {"status": "candidate_2_required", "selected_shutter": None, "candidate_2_call_count": 0}
    second_failures = [
        td_b_eq_capture_quality_failures(row, required_feature_ids=required_feature_ids)
        for row in candidate_results[1]
    ]
    if not second_failures or len(second_failures) > 4:
        raise ValueError("candidate 2 requires one to four returned slots")
    second_bad = next((item for item in second_failures if item), None)
    if second_bad is not None:
        if second_failures.index(second_bad) != len(second_failures) - 1:
            raise ValueError("candidate 2 continued after its first failure")
        return {
            "status": "exposure_window_unresolved",
            "selected_shutter": None,
            "candidate_2_call_count": len(second_failures),
        }
    if len(second_failures) != 4:
        raise ValueError("qualified candidate 2 requires exactly four returned slots")
    return {"status": "qualified_1_3200", "selected_shutter": "1/3200", "candidate_2_call_count": 4}

def build_ray_r6_spec(policy: Mapping[str, Any] | None = None) -> dict[str, Any]:
    """Build the executable, direct Ray R6 acquisition specification.

    This is deliberately self-contained: the canonical capture sequence and
    frozen shutters are owned by this spec rather than by an external
    orchestration artifact.
    """
    exposure = dict(policy or load_td_b_exposure_policy_v2())
    validate_td_b_exposure_policy_v2(exposure)
    shutters = {state: exposure["states"][state]["formal_shutter"] for state in ("A", "D", "B", "C")}
    sequence = (
        ("A", "000-ray-a0-t600", 600, "initial_anchor"),
        ("D", "001-ray-d-t60", 60, "switch_curve"),
        ("D", "002-ray-d-t120", 120, "switch_curve"),
        ("D", "003-ray-d-t300", 300, "switch_curve"),
        ("D", "004-ray-d-t600", 600, "switch_curve"),
        ("A", "005-ray-a-after-d-t600", 600, "return_after_D"),
        ("B", "006-ray-b-t60", 60, "switch_curve"),
        ("B", "007-ray-b-t120", 120, "switch_curve"),
        ("B", "008-ray-b-t300", 300, "switch_curve"),
        ("B", "009-ray-b-t600", 600, "switch_curve"),
        ("A", "010-ray-a-after-b-t600", 600, "return_after_B"),
        ("C", "011-ray-c-t60", 60, "switch_curve"),
        ("C", "012-ray-c-t120", 120, "switch_curve"),
        ("C", "013-ray-c-t300", 300, "switch_curve"),
        ("C", "014-ray-c-t600", 600, "switch_curve"),
        ("A", "015-ray-a-after-c-t600", 600, "return_after_C"),
    )
    captures = []
    for index, (state, capture_id, elapsed, role) in enumerate(sequence):
        command = dict(RAY_STATES[state])
        gate_after = {
            0: "after_initial_anchor", 4: "after_switch_D", 5: "after_return_D",
            9: "after_switch_B", 10: "after_return_B", 14: "after_switch_C",
            15: "after_return_C",
        }.get(index)
        captures.append({
            "capture_id": capture_id, "sequence_index": index,
            "capture_role": "formal", "formal_measurement": True,
            "source_id": "ray", "state_id": state,
            "role": role, "command": command,
            "exact_command_hash": canonical_sha256(command),
            "nominal_shutter": shutters[state],
            "exposure_mode": "fixed", "weak_reacquire": False,
            "mid_run_shutter_change": False, "requested_elapsed_s": elapsed,
            "timing_acceptance": "observed_elapsed_record_only",
            "strip_zero_required": True, "ambient_cap": 0,
            "isolation_gate_after": gate_after,
        })
    frozen = {shutter_cache_key_for_step(row): shutters[row["state_id"]] for row in captures}
    frozen = {key: frozen[key] for key in sorted(frozen)}
    return {
        "schema": PLAN_SCHEMA_V2, "status": "execute_authorized",
        "experiment_id": TD_B, "guide_experiment_id": TD_B_R6_EXPERIMENT_ID, "stage": "TD-B",
        "source": "ray", "variant": "core", "phase": "formal",
        "inputs": {
            "location": file_reference(LOCATION_PATH),
            "policy": file_reference(POLICY_PATH),
            "uncertainty": file_reference(UNCERTAINTY_PATH),
            "manifold": file_reference(MANIFOLD_PATH),
            "code_duty_curve": file_reference(CURVE_PATH),
        },
        "strip": "zero_throughout", "ambient": 0,
        "source_isolation_contract": "strip_zero_between_states_ray_continuous_until_final_cleanup",
        "continuous_ray_state_order": ["A", "D", "A", "B", "A", "C", "A"],
        "native_raw_ambient_policy": AMBIENT_POLICY_UNSUBTRACTED_NO_AMBIENT,
        "timing_contract": timing_contract(2), "captures": captures,
        "capture_ids": [row["capture_id"] for row in captures],
        "frozen_shutters": frozen,
        "exposure_setup_required": [],
        "shutter_ledger_provenance": {"owner": "experiment_capture_steps",
            "required_cache_keys": list(frozen),
            "frozen_shutters_sha256": canonical_sha256(frozen)},
        "budgets": {"formal_cap": 16, "ambient_cap": 0, "physical_cr3_cap": 16,
                    "setup_physical_cr3_cap": 0},
        "camera": {"backend": "remote", "v2_capture_timing_capability_available": True,
                   "v2_capture_capability": "remote_v2_capture_timing_v1",
                   "resolved_capture_settings": {"owner": "remote_backend.resolve_capture_settings",
                       "iso": "100", "aperture": "f/4", "image_format": "RAW"}},
        "execution_authorization": {"schema": "direct_ray_r6_authority_v1",
            "human_authorization_verified": True,
            "human_authorization_experiment_id": TD_B_R6_EXPERIMENT_ID,
            "remote_v2_capability": True},
        "cleanup": {"python_finally": "required", "shell_trap": "EXIT_INT_TERM_HUP_required"},
        "analysis_contract": {
            "feature_ids": "frozen_policy_feature_set",
            "quality_artifact": "quality.json",
            "history_semantics": "analyze_td_b_r6_operational_contract",
            "old_new_frame_combination": "prohibited",
        },
    }


def build_ray_history_session_spec(
    session_index: int,
    *,
    policy: Mapping[str, Any] | None = None,
    device_control_enabled: bool = False,
    session_start_condition: str | None = None,
) -> dict[str, Any]:
    """Build one self-contained seven-capture order-balanced Ray session.

    Each returned plan is consumed by the existing direct measurement runner.
    The three sessions are independent runs; R6 contributes no frames or fit data.
    """
    if session_index not in (1, 2, 3):
        raise ValueError("Ray history session index must be 1, 2, or 3")
    if device_control_enabled and session_start_condition != RAY_HISTORY_SESSION_START_CONDITION:
        raise ValueError("Ray history device session requires the frozen 600 s cold-proxy condition")
    exposure = dict(policy or load_td_b_exposure_policy_v2())
    validate_td_b_exposure_policy_v2(exposure)
    dwell_policy = json.loads(RAY_HISTORY_DWELL_POLICY_PATH.read_text(encoding="utf-8"))
    if (
        dwell_policy.get("schema") != "p7_human_operational_dwell_policy_v1"
        or dwell_policy.get("status") != "active"
        or dwell_policy.get("decision_owner") != "Human"
        or dwell_policy.get("operational_dwell_s") != RAY_HISTORY_OPERATIONAL_DWELL_S
        or dwell_policy.get("thermal_error")
        != "explicitly_accepted_to_reduce_time_and_power"
        or dwell_policy.get("session_cold_proxy_s") != RAY_HISTORY_SESSION_COLD_PROXY_S
        or dwell_policy.get("session_cold_proxy_changed") is not True
        or dwell_policy.get("session_cold_proxy_supersedes_s") != 3600
        or dwell_policy.get("settled_or_steady_claim_allowed") is not False
    ):
        raise ValueError("Ray history Human dwell/cold-proxy policy differs from the frozen Human decision")
    shutters = {
        state: exposure["states"][state]["formal_shutter"]
        for state in ("A", "D", "B", "C")
    }
    order = RAY_HISTORY_3X3_SESSION_ORDERS[session_index - 1]
    sequence: list[tuple[str, str, str, int, str | None]] = [
        ("A", "initial_anchor", "A0", 0, None),
    ]
    for position, predecessor in enumerate(order, start=1):
        sequence.extend((
            (predecessor, "predecessor", predecessor, position, None),
            ("A", "return_anchor", f"A_after_{predecessor}", position, predecessor),
        ))
    captures: list[dict[str, Any]] = []
    for sequence_index, (state, role, anchor_label, position, immediate_predecessor) in enumerate(sequence):
        capture_id = (
            f"{sequence_index:03d}-s{session_index}-ray-"
            f"{anchor_label.lower()}-t{RAY_HISTORY_OPERATIONAL_DWELL_S}"
        )
        command = dict(RAY_STATES[state])
        captures.append({
            "capture_id": capture_id,
            "sequence_index": sequence_index,
            "capture_role": "formal",
            "formal_measurement": True,
            "source_id": "ray",
            "state_id": state,
            "role": role,
            "anchor_label": anchor_label,
            "session_index": session_index,
            "sequence_position": position,
            "immediate_predecessor_state": immediate_predecessor,
            "command": command,
            "exact_command_hash": canonical_sha256(command),
            "nominal_shutter": shutters[state],
            "exposure_mode": "fixed",
            "weak_reacquire": False,
            "mid_run_shutter_change": False,
            "requested_elapsed_s": RAY_HISTORY_OPERATIONAL_DWELL_S,
            "timing_acceptance": "observed_elapsed_record_only",
            "strip_zero_required": True,
            "ambient_cap": 0,
            "isolation_gate_after": f"s{session_index}-{anchor_label}-strip-zero",
        })
    frozen = {
        shutter_cache_key_for_step(row): shutters[row["state_id"]]
        for row in captures
    }
    frozen = {key: frozen[key] for key in sorted(frozen)}
    return {
        "schema": PLAN_SCHEMA_V2,
        "status": "execute_authorized" if device_control_enabled else "device_locked",
        "experiment_id": TD_B,
        "guide_experiment_id": RAY_HISTORY_3X3_EXPERIMENT_ID,
        "stage": "TD-B",
        "source": "ray",
        "variant": "history-identification",
        "phase": "formal",
        "session_index": session_index,
        "session_order": list(order),
        "session_start_condition": (
            None if session_start_condition is None else session_start_condition.strip()
        ),
        "inputs": {
            "location": file_reference(LOCATION_PATH),
            "policy": file_reference(POLICY_PATH),
            "uncertainty": file_reference(UNCERTAINTY_PATH),
            "manifold": file_reference(MANIFOLD_PATH),
            "code_duty_curve": file_reference(CURVE_PATH),
            "human_dwell_policy": file_reference(RAY_HISTORY_DWELL_POLICY_PATH),
        },
        "strip": "zero_throughout",
        "ambient": 0,
        "source_isolation_contract": "strip_zero_between_states_ray_continuous_until_final_cleanup",
        "continuous_ray_state_order": [row["state_id"] for row in captures],
        "native_raw_ambient_policy": AMBIENT_POLICY_UNSUBTRACTED_NO_AMBIENT,
        "timing_contract": timing_contract(2),
        "captures": captures,
        "capture_ids": [row["capture_id"] for row in captures],
        "frozen_shutters": frozen,
        "exposure_setup_required": [],
        "shutter_ledger_provenance": {
            "owner": "experiment_capture_steps",
            "required_cache_keys": list(frozen),
            "frozen_shutters_sha256": canonical_sha256(frozen),
        },
        "budgets": {
            "formal_cap": 7, "ambient_cap": 0, "physical_cr3_cap": 7,
            "setup_physical_cr3_cap": 0,
        },
        "camera": {
            "backend": "remote", "v2_capture_timing_capability_available": True,
            "v2_capture_capability": "remote_v2_capture_timing_v1",
            "resolved_capture_settings": {
                "owner": "remote_backend.resolve_capture_settings",
                "iso": "100", "aperture": "f/4", "image_format": "RAW",
            },
        },
        "execution_authorization": {
            "schema": "direct_ray_history_session_v1",
            "bounded_device_scope": device_control_enabled,
            "human_authorization_required": False,
            "experiment_id": RAY_HISTORY_3X3_EXPERIMENT_ID,
            "remote_v2_capability": True,
        },
        "cleanup": {
            "python_finally": "required", "shell_trap": "EXIT_INT_TERM_HUP_required",
        },
        "analysis_contract": {
            "response": "session_A_return_minus_session_A0",
            "model": "session_plus_sequence_position_plus_immediate_predecessor",
            "operational_dwell_s": RAY_HISTORY_OPERATIONAL_DWELL_S,
            "session_cold_proxy_s": RAY_HISTORY_SESSION_COLD_PROXY_S,
            "session_cold_proxy_thermal_error": "human_accepted",
            "thermal_error": "human_accepted",
            "steady_claim": False,
            "r6_frame_pooling": False,
            "r6_use": "frozen_drift_direction_only",
        },
    }


def build_ray_history_experiment_spec(
    *, device_control_enabled: bool = False,
    session_start_conditions: Sequence[str] | None = None,
) -> dict[str, Any]:
    """Build the exact three-session, 21-capture scientific experiment."""
    if device_control_enabled and (
        session_start_conditions is None or len(session_start_conditions) != 3
    ):
        raise ValueError("Ray history device experiment requires three session start conditions")
    sessions = [
        build_ray_history_session_spec(
            index,
            device_control_enabled=device_control_enabled,
            session_start_condition=(
                None if session_start_conditions is None
                else session_start_conditions[index - 1]
            ),
        )
        for index in (1, 2, 3)
    ]
    return {
        "schema": "guide4_ray_history_order_balanced_3x3_v1",
        "experiment_id": RAY_HISTORY_3X3_EXPERIMENT_ID,
        "status": "execute_authorized" if device_control_enabled else "device_locked",
        "orders": [list(order) for order in RAY_HISTORY_3X3_SESSION_ORDERS],
        "session_count": 3,
        "formal_capture_count": 21,
        "session_launch_count": 3,
        "retry_count": 0,
        "r6_frame_pooling": False,
        "sessions": sessions,
    }


def build_strip_history_session_spec(
    session_index: int,
    *,
    device_control_enabled: bool = False,
    session_start_condition: str | None = None,
) -> dict[str, Any]:
    """Build the GUIDE5 strip-only counterpart using the same seven-step scheduler."""
    plan = build_ray_history_session_spec(
        session_index, device_control_enabled=device_control_enabled,
        session_start_condition=session_start_condition,
    )
    commands = load_r1_commands()
    shutters = load_r1_shutters()
    state_shutters = {
        state: shutters[f"strip-{STRIP_COMMAND_KEYS[state]}"]
        for state in ("A", "D", "B", "C")
    }
    for step in plan["captures"]:
        state = str(step["state_id"])
        step["capture_id"] = step["capture_id"].replace("-ray-", "-strip-")
        step["source_id"] = "strip"
        step["command"] = _command("strip", state, commands)
        step["exact_command_hash"] = canonical_sha256(step["command"])
        step["nominal_shutter"] = state_shutters[state]
        step["strip_zero_required"] = False
        step["ray_zero_required"] = True
        step["isolation_gate_after"] = (
            f"s{session_index}-{step['anchor_label']}-ray-zero"
        )
    frozen = {
        shutter_cache_key_for_step(step): state_shutters[str(step["state_id"])]
        for step in plan["captures"]
    }
    frozen = {key: frozen[key] for key in sorted(frozen)}
    plan.update({
        "experiment_id": TD_B,
        "guide_experiment_id": STRIP_HISTORY_3X3_EXPERIMENT_ID,
        "source": "strip",
        "variant": "history-identification",
        "strip": "continuous_command_sequence",
        "ray": "zero_throughout",
        "source_isolation_contract": "ray_zero_between_states_strip_continuous_until_final_cleanup",
        "continuous_ray_state_order": [],
        "frozen_shutters": frozen,
        "execution_authorization": {
            "schema": "direct_strip_history_session_v1",
            "bounded_device_scope": device_control_enabled,
            "human_authorization_required": False,
            "experiment_id": STRIP_HISTORY_3X3_EXPERIMENT_ID,
            "remote_v2_capability": True,
        },
        "analysis_contract": {
            "response": "session_A_return_minus_session_A0",
            "model": "common_reentry_plus_session_plus_sequence_position_plus_immediate_predecessor",
            "operational_dwell_s": RAY_HISTORY_OPERATIONAL_DWELL_S,
            "session_cold_proxy_s": RAY_HISTORY_SESSION_COLD_PROXY_S,
            "session_cold_proxy_thermal_error": "human_accepted",
            "thermal_error": "human_accepted",
            "steady_claim": False,
            "r6_frame_pooling": False,
            "r6_use": "none",
        },
    })
    plan["capture_ids"] = [step["capture_id"] for step in plan["captures"]]
    plan["shutter_ledger_provenance"] = {
        "owner": "experiment_capture_steps",
        "required_cache_keys": list(frozen),
        "frozen_shutters_sha256": canonical_sha256(frozen),
    }
    return plan


def ray_fast_long_bridge_start_condition(
    *, state: str, protocol: str, reset_s: int,
) -> str:
    return (
        f"Ray and strip continuously off for at least {reset_s} s before the "
        f"GUIDE5 {state} {protocol} mini-session; both-source zero readback "
        "passes at run start"
    )


def build_ray_fast_long_bridge_session_spec(
    mini_session_index: int,
    *,
    device_control_enabled: bool = False,
    session_start_condition: str | None = None,
    scientific_prerequisite: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Build one direct A/Q/A mini-session for the GUIDE5 thermal bridge."""
    if mini_session_index not in range(1, 5):
        raise ValueError("Ray fast/long bridge mini-session index must be 1..4")
    state, protocol, reset_s, dwell_s = RAY_FAST_LONG_BRIDGE_MINI_SESSIONS[
        mini_session_index - 1
    ]
    required_start = ray_fast_long_bridge_start_condition(
        state=state, protocol=protocol, reset_s=reset_s,
    )
    if device_control_enabled and session_start_condition != required_start:
        raise ValueError("Ray fast/long bridge session start condition differs")
    if device_control_enabled and (
        not isinstance(scientific_prerequisite, Mapping)
        or scientific_prerequisite.get("kind") != "ray-fast-long-bridge"
        or scientific_prerequisite.get("status") != "pass"
    ):
        raise ValueError("Ray fast/long bridge requires accepted strip analyzer-v3")

    exposure = load_td_b_exposure_policy_v2()
    validate_td_b_exposure_policy_v2(exposure)
    state_shutters = {
        item: exposure["states"][item]["formal_shutter"]
        for item in ("A", state)
    }
    sequence = (
        ("A", "initial_anchor", "A0"),
        (state, "bridge_state", state),
        ("A", "return_anchor", f"A_after_{state}"),
    )
    captures = []
    for sequence_index, (capture_state, role, anchor_label) in enumerate(sequence):
        command = dict(RAY_STATES[capture_state])
        captures.append({
            "capture_id": (
                f"{sequence_index:03d}-bridge-m{mini_session_index}-"
                f"{state.lower()}-{protocol.lower()}-{anchor_label.lower()}-t{dwell_s}"
            ),
            "sequence_index": sequence_index,
            "capture_role": "formal",
            "formal_measurement": True,
            "source_id": "ray",
            "state_id": capture_state,
            "role": role,
            "anchor_label": anchor_label,
            "bridge_state": state,
            "bridge_protocol": protocol,
            "mini_session_index": mini_session_index,
            "command": command,
            "exact_command_hash": canonical_sha256(command),
            "nominal_shutter": state_shutters[capture_state],
            "exposure_mode": "fixed",
            "weak_reacquire": False,
            "mid_run_shutter_change": False,
            "requested_elapsed_s": dwell_s,
            "timing_acceptance": "observed_elapsed_record_only",
            "strip_zero_required": True,
            "ambient_cap": 0,
            "isolation_gate_after": (
                f"bridge-m{mini_session_index}-{anchor_label}-strip-zero"
            ),
        })
    frozen = {
        shutter_cache_key_for_step(step): state_shutters[str(step["state_id"])]
        for step in captures
    }
    frozen = {key: frozen[key] for key in sorted(frozen)}
    return {
        "schema": PLAN_SCHEMA_V2,
        "status": "execute_authorized" if device_control_enabled else "device_locked",
        "experiment_id": TD_B,
        "guide_experiment_id": RAY_FAST_LONG_BRIDGE_EXPERIMENT_ID,
        "stage": "TD-B",
        "source": "ray",
        "variant": "fast-long-thermal-bridge",
        "phase": "formal",
        "mini_session_index": mini_session_index,
        "bridge_state": state,
        "bridge_protocol": protocol,
        "reset_s": reset_s,
        "operational_dwell_s": dwell_s,
        "session_start_condition": session_start_condition,
        "scientific_prerequisite": (
            None if scientific_prerequisite is None else dict(scientific_prerequisite)
        ),
        "inputs": {
            "location": file_reference(LOCATION_PATH),
            "policy": file_reference(POLICY_PATH),
            "uncertainty": file_reference(UNCERTAINTY_PATH),
            "manifold": file_reference(MANIFOLD_PATH),
            "code_duty_curve": file_reference(CURVE_PATH),
            "fast_targets": file_reference(RAY_FAST_TARGET_PATH),
        },
        "strip": "zero_throughout",
        "ambient": 0,
        "source_isolation_contract": (
            "strip_zero_between_states_ray_continuous_until_final_cleanup"
        ),
        "continuous_ray_state_order": [step["state_id"] for step in captures],
        "native_raw_ambient_policy": AMBIENT_POLICY_UNSUBTRACTED_NO_AMBIENT,
        "timing_contract": timing_contract(2),
        "captures": captures,
        "capture_ids": [step["capture_id"] for step in captures],
        "frozen_shutters": frozen,
        "exposure_setup_required": [],
        "shutter_ledger_provenance": {
            "owner": "experiment_capture_steps",
            "required_cache_keys": list(frozen),
            "frozen_shutters_sha256": canonical_sha256(frozen),
        },
        "budgets": {
            "formal_cap": 3, "ambient_cap": 0, "physical_cr3_cap": 3,
            "setup_physical_cr3_cap": 0,
        },
        "camera": {
            "backend": "remote", "v2_capture_timing_capability_available": True,
            "v2_capture_capability": "remote_v2_capture_timing_v1",
            "resolved_capture_settings": {
                "owner": "remote_backend.resolve_capture_settings",
                "iso": "100", "aperture": "f/4", "image_format": "RAW",
            },
        },
        "execution_authorization": {
            "schema": "direct_ray_fast_long_bridge_session_v1",
            "bounded_device_scope": device_control_enabled,
            "human_authorization_required": False,
            "experiment_id": RAY_FAST_LONG_BRIDGE_EXPERIMENT_ID,
            "remote_v2_capability": True,
        },
        "cleanup": {
            "python_finally": "required",
            "shell_trap": "EXIT_INT_TERM_HUP_required",
        },
        "analysis_contract": {
            "response": "matched_fast_vs_long_Q_and_local_A_return",
            "fast_envelope": "op120_reset600",
            "long_envelope": "op600_reset1800_holdout",
            "long_data_fit_input": False,
            "covariance_change_allowed": False,
            "steady_claim": False,
        },
    }


def build_direct_plan(
    experiment_id: str,
    *,
    source: str | None = None,
    variant: str = "core",
) -> dict[str, Any]:
    """Build one of the three protocol-specific direct execution specs.

    The spec is the reproducibility boundary.  It contains frozen input
    references and capture steps, but no release, lineage, stage-gate, Git or
    plan-parser authority.
    """
    if experiment_id == TD_B and source == "ray" and variant == "core":
        return build_ray_r6_spec()
    if experiment_id not in {TD_B, TD_C}:
        raise ValueError("direct execution supports Ray/strip TD-B and TD-C core")
    if experiment_id == TD_B and source != "strip":
        raise ValueError("strip TD-B direct execution requires source=strip")
    if experiment_id == TD_C and source is not None:
        raise ValueError("TD-C direct execution owns both sources")
    if experiment_id == TD_C and variant == TD_C_FAST_ENDPOINT_HOLDOUT_VARIANT:
        plan = _build_td_c_fast_endpoint_holdout_plan()
    elif experiment_id == TD_C and variant == TD_C_FAST_ANCHOR_DIRECTION_B_VARIANT:
        plan = _build_td_c_fast_anchor_direction_b_plan()
    elif experiment_id == TD_C and variant == GUIDE6_DIRECT_TARGET_LOCAL_H120_S100_VARIANT:
        plan = _build_guide6_direct_target_local_h120_s100_plan()
    else:
        if experiment_id == TD_C and variant != "core":
            raise ValueError("TD-C direct execution supports core or frozen GUIDE5 variants")
        plan = build_diagnostic_plan(experiment_id, source=source, variant=variant)
    for step in plan["captures"]:
        if step.get("formal_measurement") and step.get("requested_elapsed_s") is None:
            step["requested_elapsed_s"] = 600
            step["timing_status"] = "resolved"
            step["timing_acceptance"] = "observed_elapsed_record_only"
    plan["timing_resolution"] = (
        "guide5_reset600_D120_A120_Q120"
        if variant in {TD_C_FAST_ENDPOINT_HOLDOUT_VARIANT, TD_C_FAST_ANCHOR_DIRECTION_B_VARIANT}
        else "guide5_reset600_D120_A120"
        if experiment_id == TD_C
        else "direct_operational_600"
    )
    plan.update({
        "status": (
            "execute_authorized"
            if variant == GUIDE6_DIRECT_TARGET_LOCAL_H120_S100_VARIANT
            else "deferred_diagnostic_only"
            if variant == TD_C_FAST_ANCHOR_DIRECTION_B_VARIANT
            else "execute_authorized"
        ),
        "phase": "formal",
        "execution_authorization": {
            "schema": (
                "direct_td_c_fast_endpoint_holdout_v1"
                if variant == TD_C_FAST_ENDPOINT_HOLDOUT_VARIANT
                else "direct_guide6_target_local_h120_s100_v1"
                if variant == GUIDE6_DIRECT_TARGET_LOCAL_H120_S100_VARIANT
                else "direct_td_c_fast_anchor_direction_b_v1"
                if variant == TD_C_FAST_ANCHOR_DIRECTION_B_VARIANT
                else f"direct_{'strip_td_b' if experiment_id == TD_B else 'td_c_core'}_authority_v1"
            ),
            "human_authorization_verified": variant not in {TD_C_FAST_ENDPOINT_HOLDOUT_VARIANT, TD_C_FAST_ANCHOR_DIRECTION_B_VARIANT, GUIDE6_DIRECT_TARGET_LOCAL_H120_S100_VARIANT},
            "human_authorization_experiment_id": (
                None if variant in {TD_C_FAST_ENDPOINT_HOLDOUT_VARIANT, TD_C_FAST_ANCHOR_DIRECTION_B_VARIANT, GUIDE6_DIRECT_TARGET_LOCAL_H120_S100_VARIANT} else experiment_id
            ),
            "bounded_device_scope": variant in {TD_C_FAST_ENDPOINT_HOLDOUT_VARIANT, TD_C_FAST_ANCHOR_DIRECTION_B_VARIANT, GUIDE6_DIRECT_TARGET_LOCAL_H120_S100_VARIANT},
            "human_authorization_required": False,
            "experiment_id": (
                TD_C_FAST_ENDPOINT_HOLDOUT_EXPERIMENT_ID
                if variant == TD_C_FAST_ENDPOINT_HOLDOUT_VARIANT else
                GUIDE6_DIRECT_TARGET_LOCAL_H120_S100_EXPERIMENT_ID
                if variant == GUIDE6_DIRECT_TARGET_LOCAL_H120_S100_VARIANT else
                TD_C_FAST_ANCHOR_DIRECTION_B_EXPERIMENT_ID
                if variant == TD_C_FAST_ANCHOR_DIRECTION_B_VARIANT else experiment_id
            ),
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
    })
    return plan


def _build_td_c_fast_endpoint_holdout_plan() -> dict[str, Any]:
    commands = load_r1_commands()
    shutters = load_r1_shutters()
    sessions = (
        ("B", ("ray", "strip")),
        ("C", ("strip", "ray")),
        ("B", ("strip", "ray")),
        ("C", ("ray", "strip")),
    )
    captures = []
    for session_index, (state, order) in enumerate(sessions, start=1):
        for source_order, source in enumerate(order, start=1):
            precondition = []
            for precondition_state in ("D", "A"):
                command = _command(source, precondition_state, commands)
                precondition.append({
                    "state_id": precondition_state,
                    "command": command,
                    "exact_command_hash": canonical_sha256(command),
                    "dwell_s": 120,
                    "capture": False,
                })
            step = _step(
                source, state, 120, len(captures), commands,
                session_index=session_index,
                source_order=source_order,
                session_state=state,
                endpoint_role="direct_absolute_endpoint_holdout",
                warm_precondition_sequence=precondition,
                isolation_gate_before=f"session_{session_index}_{source}_reset600",
                isolation_gate_after=f"session_{session_index}_{state}_after_{source}",
            )
            captures.append(step)
    required = required_shutter_cache_keys(captures)
    endpoint_shutters = {
        "ray-h0-s0": "1/8000",
        "ray-h300-s100": "1/2500",
        "strip-h0-s0-fullscale": "1/500",
        "strip-h300-s100-fullscale": "1/125",
    }
    frozen = {key: endpoint_shutters.get(key) for key in required}
    inputs = {
        "location": file_reference(LOCATION_PATH),
        "policy": file_reference(POLICY_PATH),
        "uncertainty": file_reference(UNCERTAINTY_PATH),
        "manifold": file_reference(MANIFOLD_PATH),
        "code_duty_curve": file_reference(CURVE_PATH),
        "fast_targets": file_reference(RAY_FAST_TARGET_PATH),
        "td_c_core_contrasts": file_reference(TD_C_CORE_CONTRAST_ARTIFACT),
        "combined_fast_history": file_reference(COMBINED_FAST_HISTORY_ARTIFACT),
    }
    return {
        "schema": PLAN_SCHEMA_V2,
        "status": "execute_authorized",
        "experiment_id": TD_C,
        "guide_experiment_id": TD_C_FAST_ENDPOINT_HOLDOUT_EXPERIMENT_ID,
        "variant": TD_C_FAST_ENDPOINT_HOLDOUT_VARIANT,
        "source": None,
        "stage": "TD-C",
        "phase": "formal",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "inputs": inputs,
        "camera": {
            "backend": "remote",
            "v2_capture_timing_capability_available": True,
            "v2_capture_capability": "remote_v2_capture_timing_v1",
            "resolved_capture_settings": {
                "owner": "remote_backend.resolve_capture_settings",
                "iso": "100", "aperture": "f/4", "image_format": "RAW",
            },
        },
        "timing_contract": timing_contract(2),
        "cold_proxy": 600,
        "cold_proxy_wait_s": 600,
        "session_orders": [list(order) for _state, order in sessions],
        "session_states": [state for state, _order in sessions],
        "captures": captures,
        "capture_ids": [step["capture_id"] for step in captures],
        "frozen_shutters": frozen,
        "exposure_setup_required": [key for key, value in frozen.items() if value is None],
        "shutter_ledger_provenance": {
            "owner": "experiment_capture_steps",
            "required_cache_keys": list(required),
            "frozen_shutters_sha256": canonical_sha256(frozen),
        },
        "native_raw_ambient_policy": AMBIENT_POLICY_UNSUBTRACTED_NO_AMBIENT,
        "source_isolation_contract": "both_off_reset_before_each_source_observation",
        "budgets": {
            "formal_cap": 8, "ambient_cap": 0, "physical_cr3_cap": 8,
            "setup_physical_cr3_cap": 0, "retry": 0,
        },
        "cleanup": {
            "python_finally": "required", "shell_trap": "EXIT_INT_TERM_HUP_required",
        },
        "analysis_contract": {
            "paired_offset_repeatability_by_state": ["B", "C"],
            "independent_synthesis_holdout": True,
            "zero_offset_gate": False,
            "steady_claim": False,
            "new_endpoint_refit_allowed": False,
        },
        "hard_locks": {
            "legacy_td_c_expansion": True,
            "solver_sentinel": True,
            "remaining_9": True, "boundary": True, "holdout": True,
            "Gate_6": True, "P8": True,
        },
        "formal_capture_eligible": True,
    }


def _build_td_c_fast_anchor_direction_b_plan() -> dict[str, Any]:
    commands = load_r1_commands()
    shutters = {
        "ray-h0-s0": "1/8000", "strip-h0-s0-fullscale": "1/500",
        "ray-h120-s50": "1/6400", "strip-h120-s50-fullscale": "1/250",
        "ray-h120-s100": "1/5000", "strip-h120-s100-fullscale": "1/160",
    }
    sessions = (("ray", "strip"), ("strip", "ray"))
    states = ("B", "B")
    captures = []
    for session_index, order in enumerate(sessions, 1):
        for source_order, source in enumerate(order, 1):
            preconditions = []
            for state in ("D", "A"):
                command = _command(source, state, commands)
                preconditions.append({
                    "state_id": state, "command": command,
                    "exact_command_hash": canonical_sha256(command),
                    "dwell_s": 120, "capture": False,
                })
            for state, role in (("A", "pre"), ("B", "q"), ("A", "post")):
                step = _step(
                    source, state, 120, len(captures), commands,
                    session_index=session_index, source_order=source_order,
                    session_state="B", endpoint_role=f"anchor_direction_{role}",
                    warm_precondition_sequence=preconditions if role == "pre" else [],
                    isolation_gate_before=f"session_{session_index}_{source}_{role}_reset600",
                    isolation_gate_after=f"session_{session_index}_{state}_{source}_{role}_after",
                )
                captures.append(step)
    return {
        "schema": PLAN_SCHEMA_V2, "status": "deferred_diagnostic_only",
        "experiment_id": TD_C, "guide_experiment_id": TD_C_FAST_ANCHOR_DIRECTION_B_EXPERIMENT_ID,
        "variant": TD_C_FAST_ANCHOR_DIRECTION_B_VARIANT, "source": None,
        "stage": "TD-C", "phase": "formal", "created_at": datetime.now(timezone.utc).isoformat(),
        "inputs": {"location": file_reference(LOCATION_PATH), "policy": file_reference(POLICY_PATH),
                   "uncertainty": file_reference(UNCERTAINTY_PATH), "manifold": file_reference(MANIFOLD_PATH),
                   "code_duty_curve": file_reference(CURVE_PATH)},
        "camera": {"backend": "remote", "v2_capture_timing_capability_available": True,
                   "v2_capture_capability": "remote_v2_capture_timing_v1",
                   "resolved_capture_settings": {"owner": "remote_backend.resolve_capture_settings", "iso": "100", "aperture": "f/4", "image_format": "RAW"}},
        "timing_contract": timing_contract(2), "cold_proxy": 600, "cold_proxy_wait_s": 600,
        "native_raw_ambient_policy": AMBIENT_POLICY_UNSUBTRACTED_NO_AMBIENT,
        "session_orders": [list(order) for order in sessions], "session_states": list(states),
        "captures": captures, "capture_ids": [step["capture_id"] for step in captures],
        "frozen_shutters": {key: value for key, value in shutters.items()},
        "exposure_setup_required": [],
        "shutter_ledger_provenance": {"owner": "guide5_anchor_direction_b_frozen", "frozen_shutters_sha256": canonical_sha256(shutters)},
        "native_raw_ambient_policy": AMBIENT_POLICY_UNSUBTRACTED_NO_AMBIENT,
        "source_isolation_contract": "both_off_reset_before_each_source_observation",
        "budgets": {"formal_cap": 12, "ambient_cap": 0, "physical_cr3_cap": 12, "setup_physical_cr3_cap": 0, "retry": 0},
        "cleanup": {"python_finally": "required", "shell_trap": "EXIT_INT_TERM_HUP_required"},
        "analysis_contract": {"route_role": "deferred_diagnostic_only",
                               "absolute_synthesis_input_allowed": False,
                               "a_pre_paired_consistency": True, "b_paired_consistency": True,
                               "a_post_paired_consistency": True, "a_post_minus_a_pre_direction": True,
                               "independent_pre_anchor_transfer": True, "zero_offset_gate": False},
        "hard_locks": {"C_validation": True, "solver_sentinel": True, "later_stages": True},
        "formal_capture_eligible": False,
    }


def _build_guide6_direct_target_local_h120_s100_plan() -> dict[str, Any]:
    """Plan-only first direct target-local H120/S100 block.

    The block is intentionally not formal-eligible until Human authorizes it.
    Ray before/after brackets and the strip candidate share the same target
    block; no cross-experiment absolute synthesis is part of this plan.
    """
    commands = load_r1_commands()
    # Use the next shorter bounded strip exposure for this saturated target
    # block. The prior attempts progressively reduced clipping; 1/640 is the
    # next camera-supported diagnosis without changing the frozen observer or
    # quality gates.
    shutters = {
        "ray": "1/5000", "strip": "1/640",
    }
    captures = []
    def add(source: str, state: str, role: str, index: int, session: int = 1) -> None:
        command = _command(source, state, commands)
        captures.append({
            "capture_id": f"{index:03d}-{source}-h120-s100-{role}",
            "source_id": source, "state_id": state, "target": "H120/S100/INT100",
            "role": role, "session_index": session, "formal_measurement": True,
            "capture_role": "formal",
            "command": command, "exact_command_hash": canonical_sha256(command),
            "requested_elapsed_s": 120, "nominal_shutter": shutters[source],
            "timing_acceptance": "observed_elapsed_record_only",
            "strip_zero_required": source == "ray", "ray_zero_required": source == "strip",
            "steady_claim": False,
        })
    add("ray", "D", "ray_precondition", 0)
    add("ray", "A", "ray_precondition", 1)
    add("ray", "A", "ray_q_before", 2)
    add("strip", "D", "strip_precondition", 3)
    add("strip", "A", "strip_precondition", 4)
    add("strip", "A", "strip_candidate", 5)
    add("ray", "D", "ray_postcondition", 6)
    add("ray", "A", "ray_postcondition", 7)
    add("ray", "A", "ray_q_after", 8)
    frozen = {
        "ray-h120-s50": shutters["ray"],
        "ray-h120-s100": shutters["ray"],
        "strip-h120-s50-fullscale": shutters["strip"],
        "strip-h120-s100-fullscale": shutters["strip"],
    }
    return {
        "schema": PLAN_SCHEMA_V2,
        "status": "execute_authorized",
        "experiment_id": TD_C,
        "guide_experiment_id": GUIDE6_DIRECT_TARGET_LOCAL_H120_S100_EXPERIMENT_ID,
        "variant": GUIDE6_DIRECT_TARGET_LOCAL_H120_S100_VARIANT,
        "stage": "GUIDE6-HSI-INT100-S1", "phase": "formal", "source": "target_local_pair",
        "inputs": {
            "location": file_reference(LOCATION_PATH),
            "code_duty_curve": file_reference(CURVE_PATH),
            "policy": file_reference(POLICY_PATH),
            "uncertainty": file_reference(UNCERTAINTY_PATH),
        },
        "target": {"hue": 120, "sat": 100, "intensity": 100, "label": "H120/S100"},
        "captures": captures,
        "capture_ids": [row["capture_id"] for row in captures],
        "session_orders": [["ray", "strip", "ray"]],
        "timing_contract": timing_contract(2), "cold_proxy": 600, "cold_proxy_wait_s": 600,
        "native_raw_ambient_policy": AMBIENT_POLICY_UNSUBTRACTED_NO_AMBIENT,
        "budgets": {"formal_cap": 9, "physical_cr3_cap": 9, "ambient_cap": 0, "retry": 0},
        "frozen_shutters": frozen,
        "exposure_setup_required": [],
        "shutter_ledger_provenance": {
            "owner": "experiment_capture_steps",
            "required_cache_keys": list(sorted(frozen)),
            "frozen_shutters_sha256": canonical_sha256(frozen),
        },
        "formal_capture_eligible": True,
        "execution_authorization": {
            "schema": "direct_guide6_target_local_h120_s100_v1",
            "human_authorization_required": False,
            "human_authorization_verified": True,
            "human_authorization_experiment_id": GUIDE6_DIRECT_TARGET_LOCAL_H120_S100_EXPERIMENT_ID,
            "bounded_device_scope": True,
            "remote_v2_capability": True,
        },
        "analysis_contract": {
            "method": "direct_target_local_ray_vs_strip",
            "cross_experiment_absolute_synthesis": False,
            "ray_before_after_bracket": True,
            "strip_base_drift_control": True,
            "steady_claim": False,
        },
        "hard_locks": {"legacy_absolute_synthesis": True, "B_prepost": "deferred_diagnostic_only", "solver_sentinel": True, "P8": True},
    }

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

def shutter_cache_key_for_step(step: Mapping[str, Any]) -> str | None:
    source = str(step.get("source_id"))
    if source == "ambient":
        return None
    state = str(step.get("state_id"))
    command = step.get("command")
    if not isinstance(command, Mapping):
        raise ValueError("formal thermal capture lacks a command for its shutter cache")
    if source == "ray":
        try:
            return f"ray-h{int(command['hue'])}-s{int(command['sat'])}"
        except (KeyError, TypeError, ValueError) as exc:
            raise ValueError("Ray thermal capture lacks a valid HSI shutter owner") from exc
    if source == "strip":
        if state not in STRIP_COMMAND_KEYS:
            raise ValueError(f"strip thermal capture has unknown state: {state}")
        return f"strip-{STRIP_COMMAND_KEYS[state]}"
    raise ValueError(f"thermal capture has unknown source: {source}")

def required_shutter_cache_keys(captures: Sequence[Mapping[str, Any]]) -> tuple[str, ...]:
    return tuple(sorted({
        key
        for step in captures
        if (key := shutter_cache_key_for_step(step)) is not None
    }))

def build_diagnostic_plan(
    experiment_id: str,
    *,
    source: str | None = None,
    variant: str = "core",
    r1_run: str | Path = R1_RUN,
    prerequisite_artifact: str | Path | None = None,
    for_execution: bool = False,
    human_authorization: str | None = None,
    exposure_start_capability: bool = False,
    v2_capture_capability: bool = False,
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

    envelope = {}
    if for_execution and human_authorization != experiment_id:
        raise PermissionError(f"execution requires exact Human authorization for {experiment_id}")
    timing_capability = bool(v2_capture_capability)
    if for_execution and not timing_capability:
        raise PermissionError("execution requires remote v2 capture timing capability")

    commands = load_r1_commands(r1_run)
    retained_shutters = load_r1_shutters(r1_run)
    if experiment_id == TD_A:
        stage_plan = _td_a_plan(str(source), commands)
    elif experiment_id == TD_B:
        stage_plan = _td_b_plan(str(source), commands, envelope)
    else:
        stage_plan = _td_c_plan(variant, commands, envelope)
    required_shutters = required_shutter_cache_keys(stage_plan["captures"])
    frozen_shutters = {key: retained_shutters.get(key) for key in required_shutters}
    inputs = {
        "r1_commands": file_reference(Path(r1_run) / "commands.jsonl"),
        "r1_plan": file_reference(Path(r1_run) / "plan.json"),
        "policy": file_reference(POLICY_PATH),
        "observer": file_reference(OBSERVER_PATH),
        "uncertainty": file_reference(UNCERTAINTY_PATH),
        "manifold": file_reference(MANIFOLD_PATH),
        "location": file_reference(LOCATION_PATH),
        "code_duty_curve": file_reference(CURVE_PATH),
    }
    plan = {
        "schema": PLAN_SCHEMA_V2,
        "status": "execute_authorized" if for_execution else "dry_run_complete_device_locked",
        "experiment_id": experiment_id,
        "variant": variant,
        "source": source,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "inputs": inputs,
        "camera": {
            "backend": "remote", "location": inputs["location"],
            "auto_exposure_in_timed_cycle": False,
            "actual_exposure_start_provenance_required": False,
            "adapter_capability_available": timing_capability,
            "v2_capture_timing_capability_available": timing_capability,
            "legacy_exposure_start_capability_deprecated_dry_run_only": bool(exposure_start_capability),
        },
        "execution_authorization": {
            "human_authorization_experiment_id": experiment_id if for_execution else None,
            "human_authorization_verified": bool(for_execution and human_authorization == experiment_id),
            "remote_v2_capability": timing_capability,
        },
        "timing_contract": timing_contract(2),
        "cold_proxy": 1800,
        "cleanup": {"python_finally": "required", "shell_trap": "EXIT_INT_TERM_HUP_required"},
        "offline_contract": {"env_calls": 0, "network_calls": 0, "device_calls": 0, "all_off_calls": 0},
        "hard_locks": {
            "sentinel_v2": True, "remaining_9": True, "boundary": True,
            "holdout": True, "P8": True, "Gate_6": True,
            "cold_steady_covariance_merge": True,
        },
        "formal_capture_eligible": False,
        "frozen_shutters": frozen_shutters,
        "exposure_setup_required": sorted(key for key, value in frozen_shutters.items() if value is None),
        "shutter_ledger_provenance": {
            "owner": "experiment_capture_steps",
            "required_cache_keys": list(required_shutters),
            "frozen_shutters_sha256": canonical_sha256(frozen_shutters),
        },
        "capture_ledger_contract": {
            "formal_measurement": "boolean", "capture_role": ["formal", "ambient"],
            "ambient_counts_as_physical_cr3": True,
            "physical_return_ledger_schema": PHYSICAL_RETURN_LEDGER_SCHEMA,
            "physical_return_precedes_measurement_acceptance": True,
        },
        "native_raw_ambient_policy": expected_native_raw_ambient_policy(
            experiment_id,
            plan_schema=PLAN_SCHEMA_V2,
        ),
        "source_isolation_contract": "independent_both_off_readback_at_run_ambient_and_transition_gates",
    }
    plan.update(stage_plan)
    return plan

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
        "timing_acceptance": "observed_elapsed_record_only" if elapsed is not None else None,
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
        "requested_elapsed_s": None, "timing_acceptance": None,
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
    override = False
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
        "budgets": {"formal_cap": 16, "ambient_cap": 0, "setup_physical_cr3_cap": 8, "physical_cr3_cap": 24},
        "timing_resolution": "developer_override_resolved" if override else ("deferred_until_td_a" if provisional is None else "resolved"),
        "continuous_command_between_timed_points": True,
        "analysis_contract": {"return_anchor_states": ["A0", "A_after_D", "A_after_B", "A_after_C"]},
        "execute_lock": "developer_override_requires_new_bounded_plan" if override else "td_a_pass_required",
    }

def _td_c_plan(variant: str, commands: Mapping[str, Mapping[str, int]], envelope: Mapping[str, Any]) -> dict[str, Any]:
    if variant == "core":
        states = ("A",)
        orders = (("ray", "strip"), ("strip", "ray"), ("ray", "strip"), ("strip", "ray"))
        physical = 8
    else:
        states = ("B", "C")
        orders = (("ray", "strip"), ("strip", "ray"))
        physical = 20
    formal_value = envelope.get("t_formal_s")
    elapsed = None if formal_value is None else int(formal_value)
    steps = []
    for state in states:
        for session_index, order in enumerate(orders, start=1):
            for source_order, source in enumerate(order, start=1):
                steps.append(_step(
                    source, state, 120 if variant == "core" else elapsed, len(steps), commands,
                    session_index=session_index, source_order=source_order,
                    timing_status=(
                        "resolved_guide5_warm_anchor"
                        if variant == "core"
                        else ("deferred_until_td_b" if elapsed is None else "resolved")
                    ),
                    warm_precondition=(
                        {
                            "reset_s": 600,
                            "state_id": "D",
                            "command": _command(source, "D", commands),
                            "exact_command_hash": canonical_sha256(_command(source, "D", commands)),
                            "dwell_s": 120,
                            "capture": False,
                            "steady_claim": False,
                        }
                        if variant == "core" else None
                    ),
                    isolation_gate_before=f"session_{session_index}_{source}_reset600",
                    isolation_gate_after=f"session_{session_index}_{state}_after_{source}",
                ))
    return {
        "stage": "TD-C", "comparison_design": "order_balanced_paired_comparison_not_classic_abba",
        "cold_proxy_wait_s": 600 if variant == "core" else 1800,
        "session_orders": [list(order) for order in orders], "captures": steps,
        "budgets": {
            "formal_cap": 8, "ambient_cap": 0 if variant == "core" else 4,
            "physical_cr3_cap": physical,
        },
        "timing_resolution": (
            "guide5_reset600_D120_A120"
            if variant == "core" else ("deferred_until_td_b" if elapsed is None else "resolved")
        ),
        "analysis_contract": {
            "warm_anchor": "reset600_then_D120_then_A120",
            "formal_capture_count": 8,
            "within_session_strip_ray_difference": True,
            "source_order_effect": True,
            "absolute_warm_A_cross_source_anchor": True,
            "steady_claim": False,
            "td_c_expansion": "locked",
        } if variant == "core" else {},
        "execute_lock": "td_b_pass_required" if variant == "core" else "td_c_core_planner_acceptance_required",
    }

class TimedCaptureResult:
    nominal_slot_s: float
    best_effort_exposure_start_elapsed_s: float
    timing_offset_s: float
    timing_evidence_status: str
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
        timing = capture.get("timing_evidence")
        if not isinstance(timing, Mapping):
            raise ValueError("timed capture lacks best-effort timing evidence")
        observed = timing.get("best_effort_elapsed_s")
        if (
            timing.get("tier") not in ACCEPTED_TIMING_TIERS
            or timing.get("status") != "accepted_best_effort_anchor"
            or timing.get("provenance") != TIMING_CONTRACT_V2["provenance"]
            or isinstance(observed, bool)
            or not isinstance(observed, (int, float))
            or not math.isfinite(float(observed))
            or float(observed) < 0
        ):
            raise ValueError("timed capture lacks accepted best-effort observed elapsed evidence")
        offset = float(observed) - float(requested)
        output.append(TimedCaptureResult(
            float(requested), float(observed), offset, "accepted", capture,
        ))
    return output

def timing_sequence_identity(experiment_id: str, step: Mapping[str, Any]) -> tuple[Any, ...]:
    if not step.get("formal_measurement"):
        raise ValueError("timing sequence identity requires a formal capture step")
    source = step.get("source_id")
    state = step.get("state_id")
    if not isinstance(source, str) or not source or not isinstance(state, str) or not state:
        raise ValueError("thermal timing sequence lacks source/state identity")
    if experiment_id == TD_A:
        cycle = step.get("cycle_index")
        if type(cycle) is not int or cycle <= 0:
            raise ValueError("TD-A timing sequence lacks cycle identity")
        return (experiment_id, source, state, cycle)
    if experiment_id == TD_B:
        role = step.get("role")
        if not isinstance(role, str) or not role:
            raise ValueError("TD-B timing sequence lacks switch/return role identity")
        return (experiment_id, source, state, role)
    if experiment_id == TD_C:
        session = step.get("session_index")
        if type(session) is not int or session <= 0:
            raise ValueError("TD-C timing sequence lacks session identity")
        return (experiment_id, source, state, session)
    raise ValueError(f"unsupported thermal experiment identity: {experiment_id}")

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
