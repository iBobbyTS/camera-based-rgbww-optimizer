from __future__ import annotations

import hashlib
import json
import math
import subprocess
from copy import deepcopy
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Mapping, Sequence
from types import MappingProxyType

import numpy as np

from camera_based_rgbww_optimizer.measurement.hsi_policy_v2 import (
    AUDIT_THRESHOLDS,
    ordered_unit_shape,
    summarize_within_groups,
)
from camera_based_rgbww_optimizer.optimization.measure_raw_observer_validation import (
    AMBIENT_POLICY_REQUIRE_PRECEDING,
    AMBIENT_POLICY_UNSUBTRACTED_NO_AMBIENT,
)
from camera_based_rgbww_optimizer.paths import PROJECT_ROOT


TD_A = "p7_td_a_cold_settling_v1"
TD_B = "p7_td_b_command_switch_history_v1"
TD_C = "p7_td_c_balanced_source_comparison_v1"
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
OPERATING_ENVELOPE_PATH = PROJECT_ROOT / "config/hsi/p7-operating-envelope-v1.json"
OPERATING_ENVELOPE_V2_PATH = PROJECT_ROOT / "config/hsi/p7-operating-envelope-v2.json"
OPERATING_ENVELOPE_V2_SHA256 = "7012f254e5fa5182dd51b72624f64ce03645fd3d8b7227ab9144f5c7767cfc16"
OPERATING_ENVELOPE_V2_SCHEMA = "p7_operating_envelope_v2"
DEVELOPER_OPERATIONAL_DWELL_S = 600
DEVELOPER_DWELL_DECISION_AUDIT = PROJECT_ROOT / "advisor/4/0.AUDIT/03-human-decision-no-extension.md"
DEVELOPER_DWELL_DECISION_AUDIT_SHA256 = "c917c54473aa3c5cc4da9098ddeb81fb109fe9a4186fb71e994c447c63d0454a"
TD_B_SETUP_SCHEMA = "p7_td_b_exposure_setup_v1"
TD_B_SETUP_SCHEMA_V2 = "p7_td_b_exposure_setup_v2"
TD_B_SETUP_PROVISIONAL_SCHEMA = "p7_td_b_exposure_setup_provisional_v1"
TD_B_SETUP_RELEASE_SCHEMA = "p7_td_b_exposure_setup_release_v1"
TD_B_SETUP_RELEASE_LINEAGE_CANDIDATE_SCHEMA = (
    "p7_td_b_setup_release_lineage_candidate_v1"
)
TD_B_SETUP_LINEAGE_RELEASE_SCHEMA = "p7_td_b_setup_lineage_release_v2"
TD_B_SETUP_CHECKPOINT = "9c804abdeabbc5da18a66d0acf25a1f13128bc2d"
TD_B_F0A_CHECKPOINT = "8b80c87939ee9aed31ce0dfaa08a5a936bdc56cb"
TD_B_SETUP_RELEASE_PATH = Path(
    "/Volumes/4T/temp/rgbww-optimizer/p7-thermal-diagnostics/"
    "p7-td-b-canon-r2-setup-20260723-042002/setup-release.json"
)
TD_B_F0A_LINEAGE_CANDIDATE_PATH = Path(
    "/Volumes/4T/temp/rgbww-optimizer/p7-td-b-f0a-offline/"
    "p7-td-b-f0a-20260723-100606/setup-release-lineage-candidate.json"
)
TD_B_F0A_LINEAGE_CANDIDATE_SHA256 = (
    "6d74f2b0fa563147bad00d8c9a89985d3b5de97034288cdd242f10b1d52dc2f1"
)
TD_B_AGENTS_POLICY_FREEZE_PATH = Path(
    "/Volumes/4T/temp/rgbww-optimizer/p7-td-b-lineage-policy-freeze-c1/"
    "20260726T230000Z/policy-freeze.json"
)
TD_B_AGENTS_POLICY_FREEZE_SHA256 = (
    "833b4229986dbe1e551cc4da36d2eeaeb7b55c6ae0bab34e887e7ee63cfe746b"
)
TD_B_AGENTS_CURRENT_SHA256 = (
    "a035e6955ea113100031bf411f30abad3b84a9dd260fde848f1b1cfbd194c8a5"
)
TD_B_AGENTS_PREVIOUS_SHA256 = (
    "f4a4a9edffb563c0ea7709382b53eed919c4a5528c69ffa9878a4c32348ee99b"
)
TD_B_AGENTS_DIFF_SHA256 = (
    "96785b5569cf420440666912944a471baad1d2d0a39743990eee5714c0f60918"
)
TD_B_AGENTS_POLICY_SCOPE = (
    "workflow roles plus Human authorization boundary; release/off/on exceptions; "
    "no scientific or device-contract changes"
)
TD_B_AGENTS_HUMAN_DECISION = (
    "explicit instruction to clarify only remote firmware and comparable dangerous "
    "operations require Human authorization; release and light on/off do not"
)
TD_B_LINEAGE_ALLOWED_PRODUCTION_PATHS = frozenset({
    "src/camera_based_rgbww_optimizer/optimization/hsi_objective.py",
    "src/camera_based_rgbww_optimizer/optimization/measure_raw_observer_validation.py",
    "src/camera_based_rgbww_optimizer/optimization/p7_thermal_diagnostics.py",
    "src/camera_based_rgbww_optimizer/optimization/measure_p7_thermal_diagnostics.py",
    "src/camera_based_rgbww_optimizer/optimization/analyze_p7_thermal_diagnostics.py",
})
TD_B_LINEAGE_ALLOWED_VALIDATION_PATHS = frozenset({
    "tests/test_hsi_objective.py",
    "tests/test_measure_raw_observer_validation.py",
    "tests/test_p7_thermal_diagnostics.py",
    "tests/test_analyze_p7_thermal_diagnostics.py",
    "docs/README.md",
    ".agents/skills/camera-based-rgbww-optimizer/SKILL.md",
})
TD_B_SETUP_STATE = "H120_S50_INT100"
TD_B_SETUP_CACHE_KEY = "ray-h120-s50"
TD_B_SETUP_COMMAND = MappingProxyType({"hue": 120, "sat": 50, "intensity_percent": 100.0})
TD_B_SETUP_PHYSICAL_CAP = 8
P6_SETUP_SEED_RUN = Path(
    "/Volumes/4T/temp/rgbww-optimizer/ray-hsi-manifold/"
    "p6-ray-hsi-remote-20260717-0403-retry1"
)
P6_SETUP_SEED_CAPTURE_ID = "0047-ray-hsi_coarse"
PHYSICAL_RETURN_LEDGER_SCHEMA = "p7_thermal_physical_return_v1"

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


def expected_native_raw_ambient_policy(
    experiment_id: str,
    *,
    plan_schema: str,
    phase: str = "formal",
) -> str:
    if (
        experiment_id == TD_B
        and plan_schema == PLAN_SCHEMA_V2
        and phase == "formal"
    ):
        return AMBIENT_POLICY_UNSUBTRACTED_NO_AMBIENT
    return AMBIENT_POLICY_REQUIRE_PRECEDING


def file_reference(path: str | Path) -> dict[str, str]:
    target = Path(path)
    return {"path": str(target), "sha256": hashlib.sha256(target.read_bytes()).hexdigest()}


def resolve_trusted_operating_envelope(
    path: str | Path, *, require_v2: bool = False,
) -> dict[str, Any]:
    """Resolve the repo-owned operating envelope without trusting caller path spelling."""
    requested = Path(path)
    if ".." in requested.parts:
        raise ValueError("operating envelope path traversal is prohibited")

    project_root = PROJECT_ROOT.resolve()
    candidate = requested if requested.is_absolute() else PROJECT_ROOT / requested
    if not candidate.is_relative_to(project_root):
        raise ValueError("operating envelope path is outside the project")

    current = project_root
    for part in candidate.relative_to(project_root).parts:
        current = current / part
        if current.is_symlink():
            raise ValueError("operating envelope path cannot contain a symlink")
    if not candidate.exists():
        raise ValueError("operating envelope artifact is missing")
    if not candidate.is_file():
        raise ValueError("operating envelope artifact is not a regular file")

    canonical = candidate.resolve(strict=True)
    expected_v1 = OPERATING_ENVELOPE_PATH.resolve(strict=True)
    expected_v2 = OPERATING_ENVELOPE_V2_PATH.resolve(strict=True)
    allowed = {expected_v2} if require_v2 else {expected_v1, expected_v2}
    if canonical not in allowed:
        raise ValueError("operating envelope path differs from the trusted repository owner")

    sha256 = hashlib.sha256(canonical.read_bytes()).hexdigest()
    if canonical == expected_v2 and sha256 != OPERATING_ENVELOPE_V2_SHA256:
        raise ValueError("operating envelope frozen hash drift")
    try:
        envelope = json.loads(canonical.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ValueError("operating envelope artifact is not valid JSON") from exc
    if not isinstance(envelope, dict):
        raise ValueError("operating envelope artifact must be a JSON object")
    mode = validate_operating_envelope(
        envelope, artifact_path=canonical, require_v2=require_v2,
    )
    return {
        "path": canonical,
        "reference": {"path": str(canonical), "sha256": sha256},
        "envelope": envelope,
        "mode": mode,
    }


def validate_trusted_operating_envelope_reference(
    reference: Mapping[str, Any], *, require_v2: bool = False,
) -> dict[str, Any]:
    """Replay a plan reference against the trusted path owner and retained hash."""
    if not isinstance(reference, Mapping) or set(reference) != {"path", "sha256"}:
        raise ValueError("operating envelope reference schema differs")
    resolved = resolve_trusted_operating_envelope(
        str(reference["path"]), require_v2=require_v2,
    )
    if reference.get("sha256") != resolved["reference"]["sha256"]:
        raise ValueError("operating envelope reference hash differs")
    return resolved


def validate_operating_envelope(
    envelope: Mapping[str, Any], *, artifact_path: str | Path | None = None,
    require_v2: bool = False,
) -> dict[str, Any]:
    """Validate the sole v1/v2 operating-envelope trust boundary."""
    schema = envelope.get("schema")
    if schema == "p7_operating_envelope_v1":
        if require_v2:
            raise ValueError("TD-B developer dwell requires the explicit v2 operating envelope")
        return {"mode": "legacy_v1", "operational_dwell_s": None, "scientifically_settled": False}
    if schema != OPERATING_ENVELOPE_V2_SCHEMA:
        raise ValueError("unsupported P7 operating envelope schema")
    required_nulls = ("t_settle_ray_s", "t_settle_strip_s", "t_formal_provisional_s", "t_formal_s")
    if any(envelope.get(field) is not None for field in required_nulls):
        raise ValueError("developer dwell envelope must keep all measured settle fields null")
    if (
        envelope.get("status") != "td_a_developer_dwell_override"
        or envelope.get("decision_owner") != "Developer/Human"
        or envelope.get("planner_inference") is not False
        or envelope.get("thermal_extension_900_1200") != "rejected"
        or envelope.get("developer_selected_operational_dwell_s") != DEVELOPER_OPERATIONAL_DWELL_S
        or envelope.get("operational_dwell_claim") != "selected_time_limit_not_proven_steady"
    ):
        raise ValueError("developer dwell decision metadata is invalid")
    if envelope.get("td_a_status") != {
        "ray": "settling_not_demonstrated_by_600",
        "strip": "settling_not_demonstrated_by_600",
    }:
        raise ValueError("developer dwell envelope rewrites the retained TD-A result")
    audit = envelope.get("decision_audit")
    if not isinstance(audit, Mapping) or set(audit) != {"path", "sha256"}:
        raise ValueError("developer dwell decision audit reference is missing")
    audit_path = Path(str(audit["path"]))
    if not audit_path.is_absolute():
        audit_path = PROJECT_ROOT / audit_path
    audit_path = audit_path.resolve()
    if not audit_path.is_relative_to(PROJECT_ROOT.resolve()) or not audit_path.is_file():
        raise ValueError("developer dwell decision audit path is outside the project")
    if audit_path != DEVELOPER_DWELL_DECISION_AUDIT.resolve():
        raise ValueError("developer dwell decision audit path differs from the frozen artifact")
    audit_sha256 = hashlib.sha256(audit_path.read_bytes()).hexdigest()
    if audit_sha256 != DEVELOPER_DWELL_DECISION_AUDIT_SHA256 or audit.get("sha256") != audit_sha256:
        raise ValueError("developer dwell decision audit hash drift")
    if artifact_path is not None:
        path = Path(artifact_path).resolve()
        if not path.is_file():
            raise ValueError("operating envelope artifact is missing")
    return {
        "mode": "developer_human_override",
        "operational_dwell_s": DEVELOPER_OPERATIONAL_DWELL_S,
        "scientifically_settled": False,
        "decision_owner": "Developer/Human",
        "decision_audit_sha256": audit_sha256,
    }


def td_b_operational_dwell_metadata(envelope: Mapping[str, Any]) -> dict[str, Any]:
    mode = validate_operating_envelope(envelope)
    return {
        "source": mode["mode"],
        "seconds": mode["operational_dwell_s"],
        "scientifically_settled": mode["scientifically_settled"],
        "measured_t_formal_provisional_s": envelope.get("t_formal_provisional_s"),
    }


def validate_td_b_operational_dwell_plan(
    plan: Mapping[str, Any], envelope: Mapping[str, Any],
) -> dict[str, Any]:
    expected = td_b_operational_dwell_metadata(envelope)
    if plan.get("operational_dwell") != expected:
        raise ValueError("TD-B developer dwell provenance differs from frozen operating envelope")
    return expected


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


def audit_td_b_historical_seed(
    run_dir: str | Path = P6_SETUP_SEED_RUN,
    *, capture_id: str = P6_SETUP_SEED_CAPTURE_ID,
) -> dict[str, Any]:
    """Rebuild the legacy P6 shutter seed decision from retained evidence."""
    root = Path(run_dir).resolve()
    reasons: list[str] = []
    evidence: dict[str, Any] = {}
    try:
        captures = [
            json.loads(line) for line in (root / "captures.jsonl").read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        commands = [
            json.loads(line) for line in (root / "commands.jsonl").read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        rows = [row for row in captures if row.get("capture_id") == capture_id]
        command_rows = [
            row for row in commands
            if row.get("capture_id") == capture_id and row.get("event") == "ray_on_readback_verified"
        ]
        if len(rows) != 1 or len(command_rows) != 1:
            raise ValueError("P6 seed capture/command owner is missing or duplicated")
        row, command_row = rows[0], command_rows[0]
        expected_raw = {"hue": 120, "sat": 50, "intensity": 1000}
        if command_row.get("expected") != expected_raw:
            reasons.append("command_mismatch")
        for owner in ("set_response", "readback"):
            if (command_row.get(owner) or {}).get("data") != expected_raw:
                reasons.append(f"{owner}_mismatch")
        ray_state = row.get("ray_state")
        if ray_state != dict(TD_B_SETUP_COMMAND):
            reasons.append("capture_state_mismatch")
        capture = (row.get("capture") or {}).get("capture") or {}
        raw_value = capture.get("saved_file")
        raw = Path(str(raw_value)).resolve() if raw_value else None
        if raw is None or not raw.is_relative_to(root) or not raw.is_file() or raw.stat().st_size <= 0:
            reasons.append("cr3_missing_or_outside_run")
            raw_sha = None
            raw_bytes = None
        else:
            raw_sha = hashlib.sha256(raw.read_bytes()).hexdigest()
            raw_bytes = raw.stat().st_size
            if capture.get("sha256") != raw_sha or capture.get("byte_count") != raw_bytes:
                reasons.append("cr3_hash_or_byte_count_mismatch")
        report_value = (row.get("capture") or {}).get("patch_statistics")
        report_path = Path(str(report_value)).resolve() if report_value else None
        if report_path is None or not report_path.is_relative_to(root) or not report_path.is_file():
            reasons.append("patch_statistics_missing_or_outside_run")
            report = {}
        else:
            report = json.loads(report_path.read_text(encoding="utf-8"))
        exposure = report.get("exposure_metadata") or {}
        if exposure.get("status") != "recorded" or not exposure.get("seconds"):
            reasons.append("recorded_exposure_missing")
        if raw is not None and Path(str(exposure.get("raw_file"))).resolve() != raw:
            reasons.append("recorded_exposure_raw_owner_mismatch")
        if capture.get("shutter_speed") != "1/6400" or exposure.get("nominal_shutter_speed") != "1/6400":
            reasons.append("shutter_mismatch")
        if capture.get("iso") != "100" or capture.get("aperture") != "implicit auto" or capture.get("image_format") != "RAW":
            reasons.append("capture_settings_mismatch")
        expected_location = file_reference(LOCATION_PATH)["sha256"]
        if (report.get("location_config") or {}).get("sha256") != expected_location:
            reasons.append("location_mismatch")
        feature_ids = json.loads(POLICY_PATH.read_text(encoding="utf-8"))["feature_set"]["ids"]
        from camera_based_rgbww_optimizer.optimization.hsi_objective import required_hsi_features_from_report
        features = required_hsi_features_from_report(report, feature_ids) if report else {}
        if set(features) != set(feature_ids):
            reasons.append("required_58_features_missing")
        if capture.get("remote_endpoint") != "/v1/capture":
            reasons.append("legacy_endpoint_mismatch")
        evidence = {
            "capture_path": None if raw is None else str(raw),
            "capture_sha256": raw_sha,
            "capture_byte_count": raw_bytes,
            "patch_statistics_path": None if report_path is None else str(report_path),
            "recorded_exposure": exposure,
            "location_sha256": (report.get("location_config") or {}).get("sha256"),
            "feature_count": len(features),
            "quality": (row.get("capture") or {}).get("quality"),
            "remote_endpoint": capture.get("remote_endpoint"),
            "command_scale_mapping": "ray_raw_intensity_1000_equals_intensity_percent_100",
            "v2_sidecar_present": False,
        }
    except (OSError, UnicodeError, json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
        reasons.append(f"audit_error:{type(exc).__name__}:{exc}")
    return {
        "schema": "p7_td_b_historical_seed_audit_v1",
        "run_dir": str(root),
        "capture_id": capture_id,
        "historical_seed_usable": not reasons,
        "seed_only": True,
        "formal_capture_eligible": False,
        "initial_shutter_seed": "1/6400" if not reasons else None,
        "reasons": reasons,
        "evidence": evidence,
    }


def validate_td_b_exposure_setup(
    artifact: Mapping[str, Any], *, artifact_path: str | Path | None = None,
) -> dict[str, Any]:
    """Validate one retained non-formal Ray exposure setup and its physical ledger."""
    if artifact.get("schema") == TD_B_SETUP_SCHEMA_V2:
        return validate_td_b_exposure_setup_v2(artifact, artifact_path=artifact_path)
    from camera_based_rgbww_optimizer.control import camera_remote_v2

    required_keys = {
        "schema", "experiment_id", "source", "state_id", "command", "command_sha256",
        "capture_role", "formal_measurement", "counts_as_physical", "enters_58_feature_fit",
        "enters_repeatability_covariance", "enters_td_b_history_aggregate", "setup_method",
        "historical_seed", "camera", "attempts", "final_capture_id", "resolved_shutter_speed",
        "setup_physical_cr3_count", "setup_physical_cr3_cap", "input_hashes", "code_checkpoint",
        "isolation", "cold_proxy", "cleanup", "failure", "fake_only",
    }
    if set(artifact) != required_keys:
        raise ValueError("TD-B setup artifact schema keys differ from frozen contract")
    expected_command = dict(TD_B_SETUP_COMMAND)
    if (
        artifact.get("schema") != TD_B_SETUP_SCHEMA
        or artifact.get("experiment_id") != TD_B
        or artifact.get("source") != "ray"
        or artifact.get("state_id") != TD_B_SETUP_STATE
        or artifact.get("command") != expected_command
        or artifact.get("command_sha256") != canonical_sha256(expected_command)
        or artifact.get("capture_role") != "exposure_setup"
        or artifact.get("formal_measurement") is not False
        or artifact.get("counts_as_physical") is not True
        or artifact.get("enters_58_feature_fit") is not False
        or artifact.get("enters_repeatability_covariance") is not False
        or artifact.get("enters_td_b_history_aggregate") is not False
        or artifact.get("setup_method") != "bounded_remote_v2_auto_exposure"
        or artifact.get("failure") is not None
    ):
        raise ValueError("TD-B setup artifact identity or role is invalid")
    seed = artifact.get("historical_seed")
    if (
        not isinstance(seed, Mapping)
        or set(seed) != {
            "schema", "run_dir", "capture_id", "historical_seed_usable", "seed_only",
            "formal_capture_eligible", "initial_shutter_seed", "reasons", "evidence",
        }
        or seed.get("schema") != "p7_td_b_historical_seed_audit_v1"
        or seed.get("seed_only") is not True
        or seed.get("formal_capture_eligible") is not False
        or not isinstance(seed.get("reasons"), list)
        or not isinstance(seed.get("evidence"), Mapping)
    ):
        raise ValueError("TD-B setup historical seed contract is invalid")
    if seed.get("historical_seed_usable") is True:
        if (
            Path(str(seed.get("run_dir"))).resolve() != P6_SETUP_SEED_RUN.resolve()
            or seed.get("capture_id") != P6_SETUP_SEED_CAPTURE_ID
            or seed.get("initial_shutter_seed") != "1/6400"
            or seed.get("reasons") != []
            or not seed["evidence"].get("capture_sha256")
            or seed["evidence"].get("remote_endpoint") != "/v1/capture"
            or seed["evidence"].get("feature_count") != 58
        ):
            raise ValueError("TD-B setup historical seed is stale or differs from frozen P6 evidence")
    elif seed.get("historical_seed_usable") is not False or seed.get("initial_shutter_seed") is not None or not seed.get("reasons"):
        raise ValueError("TD-B setup no-seed fallback is not deterministic")
    camera = artifact.get("camera")
    if (
        not isinstance(camera, Mapping)
        or camera.get("backend") != "remote"
        or camera.get("v2_capture_capability") != "remote_v2_capture_timing_v1"
        or camera.get("capture_settings_owner") != "remote_backend.resolve_capture_settings"
        or any(not isinstance(camera.get(key), str) or not camera[key].strip() for key in ("iso", "aperture", "image_format"))
        or camera.get("image_format") != "RAW"
    ):
        raise ValueError("TD-B setup camera capability/settings provenance is invalid")
    attempts = artifact.get("attempts")
    count = artifact.get("setup_physical_cr3_count")
    if (
        not isinstance(attempts, list) or not attempts
        or type(count) is not int or count != len(attempts)
        or not 1 <= count <= TD_B_SETUP_PHYSICAL_CAP
        or artifact.get("setup_physical_cr3_cap") != TD_B_SETUP_PHYSICAL_CAP
    ):
        raise ValueError("TD-B setup physical ledger is outside the frozen 1..8 budget")
    artifact_root = None if artifact_path is None else Path(artifact_path).resolve().parent
    owned_ids: set[str] = set()
    owned_paths: set[Path] = set()
    final_rows: list[Mapping[str, Any]] = []
    for index, attempt in enumerate(attempts, start=1):
        if not isinstance(attempt, Mapping) or set(attempt) != {
            "attempt_index", "capture_id", "disposition", "cr3_path", "cr3_sha256", "cr3_byte_count",
            "sidecar_path", "sidecar_sha256", "request_id", "timing_tier", "timing_method",
            "recorded_exposure", "shutter_speed", "npy_paths", "npy_deleted",
        }:
            raise ValueError("TD-B setup attempt schema differs from frozen contract")
        capture_id = attempt.get("capture_id")
        if attempt.get("attempt_index") != index or not isinstance(capture_id, str) or not capture_id or capture_id in owned_ids:
            raise ValueError("TD-B setup attempt owner is duplicated or reordered")
        owned_ids.add(capture_id)
        raw_candidate = Path(str(attempt.get("cr3_path")))
        raw = raw_candidate.resolve()
        sidecar_candidate = Path(str(attempt.get("sidecar_path")))
        sidecar = sidecar_candidate.resolve()
        if (
            artifact_root is not None and (not raw.is_relative_to(artifact_root) or not sidecar.is_relative_to(artifact_root))
        ) or raw_candidate.is_symlink() or sidecar_candidate.is_symlink() or raw in owned_paths or sidecar in owned_paths:
            raise ValueError("TD-B setup evidence owner is outside artifact root or duplicated")
        owned_paths.update((raw, sidecar))
        if not raw.is_file() or raw.stat().st_size <= 0 or not sidecar.is_file() or sidecar.stat().st_size <= 0:
            raise ValueError("TD-B setup evidence file is missing or empty")
        payload = raw.read_bytes()
        if hashlib.sha256(payload).hexdigest() != attempt.get("cr3_sha256") or len(payload) != attempt.get("cr3_byte_count"):
            raise ValueError("TD-B setup CR3 hash or byte count mismatch")
        if hashlib.sha256(sidecar.read_bytes()).hexdigest() != attempt.get("sidecar_sha256"):
            raise ValueError("TD-B setup sidecar hash mismatch")
        try:
            metadata = json.loads(sidecar.read_text(encoding="utf-8"))
            remote, receipt = camera_remote_v2.split_and_validate_sidecar(metadata, payload=payload)
        except (OSError, UnicodeError, json.JSONDecodeError, camera_remote_v2.RemoteCaptureV2Error) as exc:
            raise ValueError("TD-B setup sidecar replay failed") from exc
        if (
            remote.get("capture_id") != capture_id
            or remote.get("request_id") != attempt.get("request_id")
            or (remote.get("recorded_exposure") or {}) != attempt.get("recorded_exposure")
            or (remote.get("recorded_exposure") or {}).get("status") != "recorded"
            or (receipt.get("timing_evidence") or {}).get("tier") != attempt.get("timing_tier")
            or (remote.get("exposure_start_estimate") or {}).get("method") != attempt.get("timing_method")
            or attempt.get("timing_tier") not in ACCEPTED_TIMING_TIERS
        ):
            raise ValueError("TD-B setup metadata ID/exposure/timing association mismatch")
        from camera_based_rgbww_optimizer.measurement.recorded_exposure import parse_nominal_exposure
        try:
            nominal_seconds = parse_nominal_exposure(str(attempt.get("shutter_speed")))
        except (TypeError, ValueError, ZeroDivisionError) as exc:
            raise ValueError("TD-B setup shutter speed is invalid") from exc
        recorded_seconds = float((remote.get("recorded_exposure") or {}).get("seconds", 0.0))
        if recorded_seconds <= 0 or not 0.8 <= recorded_seconds / nominal_seconds <= 1.2:
            raise ValueError("TD-B setup shutter differs materially from recorded exposure")
        if attempt.get("npy_paths") != [] or attempt.get("npy_deleted") is not True:
            raise ValueError("TD-B setup attempt retained NPY evidence")
        if attempt.get("disposition") == "final":
            final_rows.append(attempt)
        elif attempt.get("disposition") not in {"trial", "rejected_final"}:
            raise ValueError("TD-B setup attempt disposition is invalid")
    if len(final_rows) != 1 or artifact.get("final_capture_id") != final_rows[0].get("capture_id"):
        raise ValueError("TD-B setup final capture owner is missing or ambiguous")
    final = final_rows[0]
    if not isinstance(artifact.get("resolved_shutter_speed"), str) or not artifact["resolved_shutter_speed"].strip() or artifact["resolved_shutter_speed"] != final.get("shutter_speed"):
        raise ValueError("TD-B setup resolved shutter is empty or differs from final capture")
    isolation = artifact.get("isolation")
    if not isinstance(isolation, Mapping) or set(isolation) != {
        "ray_set_response", "ray_readback", "strip_device_evidence",
    }:
        raise ValueError("TD-B setup source isolation evidence is invalid")
    from camera_based_rgbww_optimizer.optimization.hsi_source_evidence import (
        validate_ray_readback,
        validate_strip_device_evidence,
    )
    expected_ray = {"hue": 120, "sat": 50, "intensity": 1000}
    validate_ray_readback(isolation["ray_set_response"], expected_ray)
    validate_ray_readback(isolation["ray_readback"], expected_ray)
    curve = json.loads(CURVE_PATH.read_text(encoding="utf-8"))
    validate_strip_device_evidence(
        isolation["strip_device_evidence"], {channel: 0 for channel in CHANNELS}, curve,
    )
    cold = artifact.get("cold_proxy")
    if not isinstance(cold, Mapping) or cold.get("required_wait_s") != 1800:
        raise ValueError("TD-B setup cold proxy contract is missing")
    start, end = cold.get("start_monotonic_s"), cold.get("end_monotonic_s")
    if any(isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(float(value)) for value in (start, end)) or float(end) - float(start) < 1800:
        raise ValueError("TD-B setup cold proxy wait is shortened or clock-reversed")
    validate_td_b_setup_cleanup(artifact.get("cleanup"))
    inputs = artifact.get("input_hashes")
    if not isinstance(inputs, Mapping) or any(
        key not in inputs or inputs[key] != file_reference(path)["sha256"]
        for key, path in {"location": LOCATION_PATH, "policy": POLICY_PATH, "operating_envelope": OPERATING_ENVELOPE_V2_PATH}.items()
    ):
        raise ValueError("TD-B setup frozen input hashes differ")
    return {"physical_count": count, "resolved_shutter_speed": artifact["resolved_shutter_speed"], "final_capture_id": final["capture_id"]}


def validate_td_b_exposure_setup_v2(
    artifact: Mapping[str, Any], *, artifact_path: str | Path | None = None,
) -> dict[str, Any]:
    required = {"schema", "status", "base", "bindings"}
    if set(artifact) != required or artifact.get("status") != "setup_canonical_complete":
        raise ValueError("TD-B setup v2 canonical schema or status differs")
    base = artifact.get("base")
    bindings = artifact.get("bindings")
    if not isinstance(base, Mapping) or not isinstance(bindings, Mapping):
        raise ValueError("TD-B setup v2 canonical payload is incomplete")
    if base.get("schema") != TD_B_SETUP_SCHEMA or base.get("fake_only") is not False:
        raise ValueError("TD-B setup v2 requires a non-fake v1 measurement ledger")
    expected_binding_keys = {
        "code_checkpoint", "unresolved_plan", "provisional", "wrapper_source",
        "wrapper_result", "wrapper_observed_exit", "all_off_python", "all_off_shell", "final_zero",
    }
    if set(bindings) != expected_binding_keys:
        raise ValueError("TD-B setup v2 binding schema differs")
    checkpoint = bindings.get("code_checkpoint")
    if (
        not isinstance(checkpoint, str) or len(checkpoint) != 40
        or any(ch not in "0123456789abcdef" for ch in checkpoint)
        or base.get("code_checkpoint") != checkpoint
    ):
        raise ValueError("TD-B setup v2 checkpoint binding differs")
    root = None if artifact_path is None else Path(artifact_path).resolve().parent
    for name in expected_binding_keys - {"code_checkpoint"}:
        reference = bindings.get(name)
        if not isinstance(reference, Mapping) or set(reference) != {"path", "sha256"}:
            raise ValueError(f"TD-B setup v2 {name} reference schema differs")
        path = Path(str(reference.get("path"))).resolve()
        if root is not None and name != "wrapper_source" and not path.is_relative_to(root):
            raise ValueError(f"TD-B setup v2 {name} path owner differs")
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != reference.get("sha256"):
            raise ValueError(f"TD-B setup v2 {name} hash differs")
    result = validate_td_b_exposure_setup(base, artifact_path=artifact_path)
    return {**result, "schema": TD_B_SETUP_SCHEMA_V2, "code_checkpoint": checkpoint}


def validate_td_b_setup_release(
    release: Mapping[str, Any], *, release_path: str | Path,
) -> dict[str, Any]:
    path = Path(release_path).resolve()
    required = {"schema", "status", "code_checkpoint", "canonical_setup", "resolved_formal_plan"}
    if set(release) != required or release.get("schema") != TD_B_SETUP_RELEASE_SCHEMA or release.get("status") != "formal_plan_resolved":
        raise ValueError("TD-B setup release schema or status differs")
    checkpoint = release.get("code_checkpoint")
    for name in ("canonical_setup", "resolved_formal_plan"):
        reference = release.get(name)
        if not isinstance(reference, Mapping) or set(reference) != {"path", "sha256"}:
            raise ValueError("TD-B setup release reference schema differs")
        target = Path(str(reference.get("path"))).resolve()
        if target.parent != path.parent or not target.is_file() or hashlib.sha256(target.read_bytes()).hexdigest() != reference.get("sha256"):
            raise ValueError(f"TD-B setup release {name} owner or hash differs")
    canonical_path = Path(str(release["canonical_setup"]["path"])).resolve()
    canonical = json.loads(canonical_path.read_text(encoding="utf-8"))
    validated = validate_td_b_exposure_setup(canonical, artifact_path=canonical_path)
    if checkpoint != validated.get("code_checkpoint"):
        raise ValueError("TD-B setup release checkpoint differs from canonical")
    resolved_path = Path(str(release["resolved_formal_plan"]["path"])).resolve()
    resolved = json.loads(resolved_path.read_text(encoding="utf-8"))
    if resolved.get("exposure_setup_artifact") != file_reference(canonical_path):
        raise ValueError("TD-B setup release resolved plan differs from canonical")
    return {**validated, "resolved_plan": resolved, "canonical_path": str(canonical_path)}


def changed_paths_between_checkpoints(
    old_checkpoint: str,
    new_checkpoint: str,
    *,
    project_root: str | Path = PROJECT_ROOT,
) -> list[str]:
    """Return the exact repository paths changed between two full checkpoints."""
    for value in (old_checkpoint, new_checkpoint):
        if (
            len(value) != 40
            or any(character not in "0123456789abcdef" for character in value)
        ):
            raise ValueError("TD-B lineage requires full lowercase Git checkpoints")
    completed = subprocess.run(
        ["git", "diff", "--name-only", f"{old_checkpoint}..{new_checkpoint}"],
        cwd=Path(project_root),
        check=True,
        capture_output=True,
        text=True,
    )
    paths = [line.strip() for line in completed.stdout.splitlines() if line.strip()]
    if len(paths) != len(set(paths)):
        raise ValueError("TD-B lineage changed-path ledger contains duplicates")
    return paths


def _validate_td_b_agents_policy_lineage(
    *,
    old_checkpoint: str,
    new_checkpoint: str,
    project_root: str | Path = PROJECT_ROOT,
    policy_freeze_path: str | Path = TD_B_AGENTS_POLICY_FREEZE_PATH,
    require_canonical_policy_owner: bool = True,
) -> None:
    """Validate the one Human-policy AGENTS.md lineage exception fail-closed."""
    root = Path(project_root).resolve()
    policy_requested = Path(policy_freeze_path)
    if policy_requested.is_symlink():
        raise ValueError("TD-B AGENTS policy freeze cannot be a symlink")
    policy_path = policy_requested.resolve()
    if require_canonical_policy_owner and policy_path != TD_B_AGENTS_POLICY_FREEZE_PATH.resolve():
        raise ValueError("TD-B AGENTS policy freeze owner differs")
    if not policy_path.is_file():
        raise ValueError("TD-B AGENTS policy freeze is missing")
    policy_bytes = policy_path.read_bytes()
    if hashlib.sha256(policy_bytes).hexdigest() != TD_B_AGENTS_POLICY_FREEZE_SHA256:
        raise ValueError("TD-B AGENTS policy freeze hash differs")
    policy = json.loads(policy_bytes)
    required = {
        "schema", "status", "path", "classification", "current_blob_sha256",
        "expected_current", "previous_blob_sha256", "scope", "human_decision",
        "rollback", "provenance", "diff_sha256", "extra_paths",
        "qualification_runs", "release_generation", "replay_runs",
        "candidate_builds", "device_calls", "network_calls", "formal_calls",
        "git_mutations",
    }
    if (
        set(policy) != required
        or policy.get("schema") != "p7_td_b_lineage_policy_freeze_c1"
        or policy.get("status") != "pass"
        or policy.get("path") != "AGENTS.md"
        or policy.get("classification") != "bounded_validation_or_documentation"
        or policy.get("current_blob_sha256") != TD_B_AGENTS_CURRENT_SHA256
        or policy.get("expected_current") != TD_B_AGENTS_CURRENT_SHA256
        or policy.get("previous_blob_sha256") != TD_B_AGENTS_PREVIOUS_SHA256
        or policy.get("diff_sha256") != TD_B_AGENTS_DIFF_SHA256
        or policy.get("scope") != TD_B_AGENTS_POLICY_SCOPE
        or policy.get("human_decision") != TD_B_AGENTS_HUMAN_DECISION
        or policy.get("extra_paths") != []
        or not isinstance(policy.get("rollback"), str)
        or not policy["rollback"].startswith("restore previous AGENTS.md blob hash")
        or not isinstance(policy.get("provenance"), str)
        or "Human instruction recorded in task history" not in policy["provenance"]
        or any(policy.get(name) != 0 for name in (
            "qualification_runs", "release_generation", "replay_runs",
            "candidate_builds", "device_calls", "network_calls", "formal_calls",
            "git_mutations",
        ))
    ):
        raise ValueError("TD-B AGENTS policy freeze contract differs")
    agents_path = root / "AGENTS.md"
    if agents_path.is_symlink() or not agents_path.is_file():
        raise ValueError("TD-B AGENTS policy owner differs")
    if hashlib.sha256(agents_path.read_bytes()).hexdigest() != TD_B_AGENTS_CURRENT_SHA256:
        raise ValueError("TD-B AGENTS current bytes differ")
    previous = subprocess.run(
        ["git", "show", f"{old_checkpoint}:AGENTS.md"], cwd=root, check=True,
        capture_output=True,
    ).stdout
    current = subprocess.run(
        ["git", "show", f"{new_checkpoint}:AGENTS.md"], cwd=root, check=True,
        capture_output=True,
    ).stdout
    diff = subprocess.run(
        ["git", "diff", old_checkpoint, new_checkpoint, "--", "AGENTS.md"],
        cwd=root, check=True, capture_output=True,
    ).stdout
    if hashlib.sha256(previous).hexdigest() != TD_B_AGENTS_PREVIOUS_SHA256:
        raise ValueError("TD-B AGENTS previous bytes differ")
    if hashlib.sha256(current).hexdigest() != TD_B_AGENTS_CURRENT_SHA256:
        raise ValueError("TD-B AGENTS checkpoint bytes differ")
    if hashlib.sha256(diff).hexdigest() != TD_B_AGENTS_DIFF_SHA256:
        raise ValueError("TD-B AGENTS diff scope differs")


def build_td_b_setup_release_lineage_candidate(
    release_path: str | Path,
    *,
    old_checkpoint: str,
    new_checkpoint: str,
    changed_paths: Sequence[str],
) -> dict[str, Any]:
    """Build a Planner-only candidate; this never upgrades a production release."""
    if old_checkpoint != TD_B_SETUP_CHECKPOINT:
        raise ValueError("TD-B lineage old checkpoint differs from frozen setup owner")
    if (
        len(new_checkpoint) != 40
        or any(character not in "0123456789abcdef" for character in new_checkpoint)
        or new_checkpoint == old_checkpoint
    ):
        raise ValueError("TD-B lineage new checkpoint is invalid")
    path = Path(release_path).resolve()
    release = json.loads(path.read_text(encoding="utf-8"))
    validated = validate_td_b_setup_release(release, release_path=path)
    if (
        release.get("code_checkpoint") != old_checkpoint
        or validated.get("code_checkpoint") != old_checkpoint
    ):
        raise ValueError("TD-B lineage release is not bound to the frozen setup checkpoint")

    classifications: list[dict[str, str]] = []
    prohibited: list[str] = []
    if not changed_paths:
        raise ValueError("TD-B lineage changed-path ledger must not be empty")
    for raw_path in changed_paths:
        changed_path = str(raw_path).strip()
        if not changed_path or changed_path.startswith("/") or ".." in Path(changed_path).parts:
            raise ValueError("TD-B lineage changed path is not repository-relative")
        if changed_path == "AGENTS.md":
            _validate_td_b_agents_policy_lineage(
                old_checkpoint=old_checkpoint,
                new_checkpoint=new_checkpoint,
            )
            classification = "bounded_validation_or_documentation"
        elif changed_path in TD_B_LINEAGE_ALLOWED_PRODUCTION_PATHS:
            classification = "ambient_and_physical_ledger_contract"
        elif changed_path in TD_B_LINEAGE_ALLOWED_VALIDATION_PATHS:
            classification = "bounded_validation_or_documentation"
        elif changed_path.startswith(".agent-work/"):
            classification = "planner_or_execution_audit_only"
        else:
            classification = "prohibited_or_unreviewed"
            prohibited.append(changed_path)
        classifications.append({"path": changed_path, "classification": classification})
    if len(classifications) != len({item["path"] for item in classifications}):
        raise ValueError("TD-B lineage changed-path ledger contains duplicates")

    eligible = not prohibited
    return {
        "schema": TD_B_SETUP_RELEASE_LINEAGE_CANDIDATE_SCHEMA,
        "status": (
            "eligible_waiting_for_planner"
            if eligible
            else "ineligible_requires_new_setup"
        ),
        "old_checkpoint": old_checkpoint,
        "new_checkpoint": new_checkpoint,
        "release_reference": file_reference(path),
        "canonical_setup_reference": dict(release["canonical_setup"]),
        "resolved_formal_plan_reference": dict(release["resolved_formal_plan"]),
        "changed_paths": classifications,
        "prohibited_paths": prohibited,
        "canonical_setup_replay": "pass",
        "production_release_usable": False,
        "planner_acceptance_required": True,
    }


def _validate_td_b_planner_lineage_candidate(
    candidate: Mapping[str, Any],
    *,
    candidate_path: str | Path,
    legacy_release_path: str | Path,
) -> None:
    path = Path(candidate_path).resolve()
    legacy_path = Path(legacy_release_path).resolve()
    if (
        path != TD_B_F0A_LINEAGE_CANDIDATE_PATH.resolve()
        or not path.is_file()
        or hashlib.sha256(path.read_bytes()).hexdigest()
        != TD_B_F0A_LINEAGE_CANDIDATE_SHA256
    ):
        raise ValueError("TD-B Planner lineage candidate owner or hash differs")
    required = {
        "schema", "status", "old_checkpoint", "new_checkpoint",
        "release_reference", "canonical_setup_reference",
        "resolved_formal_plan_reference", "changed_paths", "prohibited_paths",
        "canonical_setup_replay", "production_release_usable",
        "planner_acceptance_required",
    }
    if (
        set(candidate) != required
        or candidate.get("schema") != TD_B_SETUP_RELEASE_LINEAGE_CANDIDATE_SCHEMA
        or candidate.get("status") != "eligible_waiting_for_planner"
        or candidate.get("old_checkpoint") != TD_B_SETUP_CHECKPOINT
        or candidate.get("new_checkpoint") != TD_B_F0A_CHECKPOINT
        or candidate.get("release_reference") != file_reference(legacy_path)
        or candidate.get("canonical_setup_replay") != "pass"
        or candidate.get("production_release_usable") is not False
        or candidate.get("planner_acceptance_required") is not True
        or candidate.get("prohibited_paths") != []
    ):
        raise ValueError("TD-B Planner lineage candidate contract differs")
    changed = candidate.get("changed_paths")
    if (
        not isinstance(changed, list)
        or not changed
        or any(
            not isinstance(item, Mapping)
            or set(item) != {"path", "classification"}
            for item in changed
        )
    ):
        raise ValueError("TD-B Planner lineage changed-path evidence differs")


def _normalize_td_b_resolved_plan(plan: Mapping[str, Any]) -> dict[str, Any]:
    normalized = deepcopy(dict(plan))
    normalized.pop("created_at", None)
    return normalized


def validate_td_b_lineage_resolved_plan(
    plan: Mapping[str, Any],
    *,
    canonical_setup_path: str | Path,
) -> None:
    setup_path = Path(canonical_setup_path).resolve()
    expected = build_diagnostic_plan(
        TD_B,
        source="ray",
        prerequisite_artifact=OPERATING_ENVELOPE_V2_PATH,
        for_execution=True,
        human_authorization=TD_B,
        v2_capture_capability=True,
    )
    expected = resolve_td_b_plan_with_setup(
        expected,
        setup_artifact_path=setup_path,
    )
    expected["setup_lineage_release_required"] = True
    if _normalize_td_b_resolved_plan(plan) != _normalize_td_b_resolved_plan(expected):
        raise ValueError("TD-B lineage resolved plan differs from current frozen plan")
    captures = plan.get("captures")
    budgets = plan.get("budgets")
    if (
        not isinstance(captures, list)
        or len(captures) != 16
        or any(step.get("capture_role") != "formal" for step in captures)
        or any(step.get("source_id") != "ray" for step in captures)
        or plan.get("native_raw_ambient_policy")
        != AMBIENT_POLICY_UNSUBTRACTED_NO_AMBIENT
        or not isinstance(budgets, Mapping)
        or budgets.get("formal_cap") != 16
        or budgets.get("ambient_cap") != 0
        or budgets.get("physical_cr3_cap") != 24
        or plan.get("setup_physical_cr3_count") != 2
        or plan.get("formal_capture_eligible") is not True
        or plan.get("setup_lineage_release_required") is not True
    ):
        raise ValueError("TD-B lineage resolved plan protocol differs")


def validate_td_b_setup_lineage_release(
    release: Mapping[str, Any],
    *,
    release_path: str | Path,
    changed_paths_fn: Callable[[str, str], Sequence[str]] | None = None,
) -> dict[str, Any]:
    requested_path = Path(release_path)
    if requested_path.is_symlink():
        raise ValueError("TD-B setup lineage release cannot be a symlink")
    path = requested_path.resolve()
    required = {
        "schema", "status", "production_release_usable",
        "old_checkpoint", "code_checkpoint", "legacy_release",
        "planner_lineage_candidate", "current_lineage_candidate",
        "canonical_setup", "resolved_formal_plan",
    }
    if (
        set(release) != required
        or release.get("schema") != TD_B_SETUP_LINEAGE_RELEASE_SCHEMA
        or release.get("status") != "formal_plan_lineage_qualified"
        or release.get("production_release_usable") is not True
        or release.get("old_checkpoint") != TD_B_SETUP_CHECKPOINT
    ):
        raise ValueError("TD-B setup lineage release schema or status differs")
    checkpoint = release.get("code_checkpoint")
    if (
        not isinstance(checkpoint, str)
        or len(checkpoint) != 40
        or any(character not in "0123456789abcdef" for character in checkpoint)
        or checkpoint in {TD_B_SETUP_CHECKPOINT, TD_B_F0A_CHECKPOINT}
    ):
        raise ValueError("TD-B setup lineage release checkpoint differs")

    references: dict[str, Path] = {}
    for name in (
        "legacy_release", "planner_lineage_candidate",
        "current_lineage_candidate", "canonical_setup", "resolved_formal_plan",
    ):
        reference = release.get(name)
        if not isinstance(reference, Mapping) or set(reference) != {"path", "sha256"}:
            raise ValueError(f"TD-B setup lineage release {name} reference differs")
        target = Path(str(reference.get("path"))).resolve()
        if (
            not target.is_file()
            or target.is_symlink()
            or hashlib.sha256(target.read_bytes()).hexdigest()
            != reference.get("sha256")
        ):
            raise ValueError(f"TD-B setup lineage release {name} owner or hash differs")
        references[name] = target
    if (
        references["legacy_release"] != TD_B_SETUP_RELEASE_PATH.resolve()
        or references["planner_lineage_candidate"]
        != TD_B_F0A_LINEAGE_CANDIDATE_PATH.resolve()
        or references["current_lineage_candidate"].parent != path.parent
        or references["resolved_formal_plan"].parent != path.parent
    ):
        raise ValueError("TD-B setup lineage release path ownership differs")

    legacy = json.loads(references["legacy_release"].read_text(encoding="utf-8"))
    legacy_validated = validate_td_b_setup_release(
        legacy,
        release_path=references["legacy_release"],
    )
    if legacy_validated.get("code_checkpoint") != TD_B_SETUP_CHECKPOINT:
        raise ValueError("TD-B setup lineage legacy checkpoint differs")
    if references["canonical_setup"] != Path(
        legacy_validated["canonical_path"]
    ).resolve():
        raise ValueError("TD-B setup lineage canonical setup differs")

    planner_candidate = json.loads(
        references["planner_lineage_candidate"].read_text(encoding="utf-8")
    )
    _validate_td_b_planner_lineage_candidate(
        planner_candidate,
        candidate_path=references["planner_lineage_candidate"],
        legacy_release_path=references["legacy_release"],
    )
    current_candidate = json.loads(
        references["current_lineage_candidate"].read_text(encoding="utf-8")
    )
    if changed_paths_fn is None:
        changed_paths = changed_paths_between_checkpoints(
            TD_B_SETUP_CHECKPOINT,
            checkpoint,
        )
    else:
        changed_paths = list(
            changed_paths_fn(TD_B_SETUP_CHECKPOINT, checkpoint)
        )
    expected_candidate = build_td_b_setup_release_lineage_candidate(
        references["legacy_release"],
        old_checkpoint=TD_B_SETUP_CHECKPOINT,
        new_checkpoint=checkpoint,
        changed_paths=changed_paths,
    )
    if (
        current_candidate != expected_candidate
        or current_candidate.get("status") != "eligible_waiting_for_planner"
        or current_candidate.get("production_release_usable") is not False
        or current_candidate.get("prohibited_paths") != []
    ):
        raise ValueError("TD-B setup current lineage candidate differs")

    resolved = json.loads(
        references["resolved_formal_plan"].read_text(encoding="utf-8")
    )
    validate_td_b_lineage_resolved_plan(
        resolved,
        canonical_setup_path=references["canonical_setup"],
    )
    return {
        **legacy_validated,
        "schema": TD_B_SETUP_LINEAGE_RELEASE_SCHEMA,
        "code_checkpoint": checkpoint,
        "resolved_plan": resolved,
        "lineage_release_path": str(path),
    }


def validate_td_b_setup_cleanup(value: Any) -> None:
    if not isinstance(value, Mapping) or set(value) != {"python", "shell", "wrapper", "final_both_off"}:
        raise ValueError("TD-B setup cleanup evidence is incomplete")
    for owner in ("python", "shell"):
        row = value.get(owner)
        if not isinstance(row, Mapping) or set(row) != {"status", "steps", "exit_code"}:
            raise ValueError(f"TD-B setup {owner} cleanup schema differs")
        if row.get("status") != "pass" or row.get("exit_code") != 0:
            raise ValueError(f"TD-B setup {owner} cleanup failed")
        steps = row.get("steps")
        if not isinstance(steps, list) or len(steps) != 2:
            raise ValueError(f"TD-B setup {owner} cleanup lacks two shutdown owners")
        by_name = {step.get("name"): step for step in steps if isinstance(step, Mapping)}
        if set(by_name) != {"esphome", "ray120c"} or any(
            set(step) != {"name", "ok", "detail", "error"} or step.get("ok") is not True or step.get("error") is not None
            for step in by_name.values()
        ):
            raise ValueError(f"TD-B setup {owner} cleanup step evidence is invalid")
    wrapper = value.get("wrapper")
    if not isinstance(wrapper, Mapping) or set(wrapper) != {
        "status", "child_exit_code", "shell_cleanup_exit_code", "wrapper_exit_code", "signal",
    }:
        raise ValueError("TD-B setup wrapper cleanup schema differs")
    if (
        wrapper.get("status") != "complete"
        or wrapper.get("child_exit_code") != 0
        or wrapper.get("shell_cleanup_exit_code") != 0
        or wrapper.get("wrapper_exit_code") != 0
        or wrapper.get("signal") is not None
    ):
        raise ValueError("TD-B setup wrapper child/signal/cleanup evidence failed")
    final = value.get("final_both_off")
    if not isinstance(final, Mapping) or set(final) != {"strip_device_evidence", "ray_readback"}:
        raise ValueError("TD-B setup final both-off evidence is incomplete")
    from camera_based_rgbww_optimizer.optimization.hsi_source_evidence import validate_both_off
    curve = json.loads(CURVE_PATH.read_text(encoding="utf-8"))
    validate_both_off(final["strip_device_evidence"], final["ray_readback"], curve)


def build_td_b_exposure_setup_artifact(
    *, attempts: Sequence[Mapping[str, Any]], camera: Mapping[str, Any],
    historical_seed: Mapping[str, Any], isolation: Mapping[str, Any],
    cold_proxy: Mapping[str, Any], cleanup: Mapping[str, Any],
    code_checkpoint: str, fake_only: bool,
) -> dict[str, Any]:
    """Produce the canonical setup artifact from adapter-owned attempt evidence."""
    rows = [deepcopy(dict(row)) for row in attempts]
    final = [row for row in rows if row.get("disposition") == "final"]
    artifact = {
        "schema": TD_B_SETUP_SCHEMA,
        "experiment_id": TD_B,
        "source": "ray",
        "state_id": TD_B_SETUP_STATE,
        "command": dict(TD_B_SETUP_COMMAND),
        "command_sha256": canonical_sha256(dict(TD_B_SETUP_COMMAND)),
        "capture_role": "exposure_setup",
        "formal_measurement": False,
        "counts_as_physical": True,
        "enters_58_feature_fit": False,
        "enters_repeatability_covariance": False,
        "enters_td_b_history_aggregate": False,
        "setup_method": "bounded_remote_v2_auto_exposure",
        "historical_seed": deepcopy(dict(historical_seed)),
        "camera": deepcopy(dict(camera)),
        "attempts": rows,
        "final_capture_id": final[0].get("capture_id") if len(final) == 1 else None,
        "resolved_shutter_speed": final[0].get("shutter_speed") if len(final) == 1 else None,
        "setup_physical_cr3_count": len(rows),
        "setup_physical_cr3_cap": TD_B_SETUP_PHYSICAL_CAP,
        "input_hashes": {
            "location": file_reference(LOCATION_PATH)["sha256"],
            "policy": file_reference(POLICY_PATH)["sha256"],
            "operating_envelope": file_reference(OPERATING_ENVELOPE_V2_PATH)["sha256"],
        },
        "code_checkpoint": code_checkpoint,
        "isolation": deepcopy(dict(isolation)),
        "cold_proxy": deepcopy(dict(cold_proxy)),
        "cleanup": deepcopy(dict(cleanup)),
        "failure": None,
        "fake_only": bool(fake_only),
    }
    validate_td_b_exposure_setup(artifact)
    return artifact


def resolve_td_b_plan_with_setup(
    plan: Mapping[str, Any], *, setup_artifact_path: str | Path,
) -> dict[str, Any]:
    if plan.get("experiment_id") != TD_B or plan.get("source") != "ray":
        raise ValueError("TD-B exposure setup can only resolve the Ray TD-B plan")
    path = Path(setup_artifact_path).resolve()
    artifact = json.loads(path.read_text(encoding="utf-8"))
    validated = validate_td_b_exposure_setup(artifact, artifact_path=path)
    fake_only = artifact.get("fake_only") is True
    if artifact.get("schema") == TD_B_SETUP_SCHEMA_V2:
        fake_only = False
    if not fake_only:
        checkpoint = validated.get("code_checkpoint", artifact.get("code_checkpoint"))
        if not isinstance(checkpoint, str) or len(checkpoint) != 40 or any(ch not in "0123456789abcdef" for ch in checkpoint):
            raise ValueError("TD-B retained setup lacks a full lowercase Git checkpoint")
    resolved = deepcopy(dict(plan))
    if resolved.get("frozen_shutters", {}).get(TD_B_SETUP_CACHE_KEY) is not None or TD_B_SETUP_CACHE_KEY not in resolved.get("exposure_setup_required", []):
        raise ValueError("TD-B Ray plan does not own the unresolved setup shutter")
    resolved["frozen_shutters"][TD_B_SETUP_CACHE_KEY] = validated["resolved_shutter_speed"]
    resolved["exposure_setup_required"] = []
    resolved["shutter_ledger_provenance"]["frozen_shutters_sha256"] = canonical_sha256(resolved["frozen_shutters"])
    resolved["exposure_setup_artifact"] = file_reference(path)
    resolved["setup_physical_cr3_count"] = validated["physical_count"]
    resolved["formal_capture_eligible"] = not fake_only
    resolved["status"] = "fake_resolved_device_locked" if fake_only else resolved["status"]
    return resolved


def replay_td_b_setup_resolution(
    plan: Mapping[str, Any], *, setup_artifact_path: str | Path,
) -> dict[str, Any]:
    """Public offline replay for both fake fixtures and future retained setup evidence."""
    inputs = plan.get("inputs")
    if not isinstance(inputs, Mapping):
        raise ValueError("TD-B setup replay lacks frozen inputs")
    validate_trusted_operating_envelope_reference(
        inputs.get("operating_envelope", {}), require_v2=True,
    )
    resolved = resolve_td_b_plan_with_setup(plan, setup_artifact_path=setup_artifact_path)
    path = Path(setup_artifact_path).resolve()
    artifact = json.loads(path.read_text(encoding="utf-8"))
    validated = validate_td_b_exposure_setup(artifact, artifact_path=path)
    if resolved.get("exposure_setup_required") or not resolved["frozen_shutters"].get(TD_B_SETUP_CACHE_KEY):
        raise ValueError("TD-B setup replay did not resolve the formal shutter ledger")
    return {
        "schema": "p7_td_b_exposure_setup_replay_v1",
        "status": "offline_fake_replay_pass" if artifact.get("fake_only") else "retained_setup_replay_pass",
        "formal_capture_eligible": bool(resolved.get("formal_capture_eligible")),
        "fake_only": bool(artifact.get("fake_only")),
        "setup_artifact": file_reference(path),
        "resolved_plan_sha256": canonical_sha256(resolved),
        "setup_physical_cr3_count": validated["physical_count"],
        "formal_capture_count": int(resolved["budgets"]["formal_cap"]),
        "physical_cr3_cap": int(resolved["budgets"]["physical_cr3_cap"]),
        "setup_excluded_from_formal_statistics": True,
        "setup_excluded_from_58_feature_fit": True,
        "setup_excluded_from_repeatability_covariance": True,
        "setup_excluded_from_td_b_history_aggregate": True,
    }


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

    prerequisite = resolve_trusted_operating_envelope(prerequisite_artifact)
    envelope = prerequisite["envelope"]
    _enforce_prerequisites(experiment_id, variant, envelope, for_execution=for_execution)
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
        "operating_envelope": prerequisite["reference"],
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
        "cold_proxy": envelope["cold_proxy"],
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


def _enforce_prerequisites(
    experiment_id: str, variant: str, envelope: Mapping[str, Any], *, for_execution: bool
) -> None:
    if not for_execution:
        return
    if experiment_id == TD_B:
        mode = validate_operating_envelope(envelope, require_v2=False)
        if mode["mode"] == "developer_human_override":
            return
        if envelope.get("status") != "td_a_pass":
            raise PermissionError("TD-B execute plan is locked until TD-A passes")
        if envelope.get("t_formal_provisional_s") not in SELECTABLE_SETTLE_POINTS:
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
    envelope_mode = validate_operating_envelope(envelope)
    override = envelope_mode["mode"] == "developer_human_override"
    provisional = envelope_mode["operational_dwell_s"] if override else envelope.get("t_formal_provisional_s")
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
        "operational_dwell": td_b_operational_dwell_metadata(envelope),
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
