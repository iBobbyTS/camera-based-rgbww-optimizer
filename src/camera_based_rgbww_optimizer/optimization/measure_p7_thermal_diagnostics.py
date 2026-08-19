from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import os
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Mapping, Sequence

import numpy as np

from camera_based_rgbww_optimizer.measurement.hsi_policy_v2 import (
    calibrate_direct_limits,
    ordered_unit_shape,
)
from camera_based_rgbww_optimizer.optimization import p7_thermal_diagnostics as thermal
from camera_based_rgbww_optimizer.optimization import measure_raw_observer_validation as raw_validation
from camera_based_rgbww_optimizer.optimization.bounded_least_squares import (
    solve_box_constrained_least_squares,
)
from camera_based_rgbww_optimizer.control import camera_remote_v2, esphome
from camera_based_rgbww_optimizer.paths import PROJECT_ROOT, PROJECT_TMP_DIR


DEFAULT_OUTPUT = PROJECT_TMP_DIR / "p7-thermal-diagnostics-offline"
REMOTE_V2_CAPABILITY = "remote_v2_capture_timing_v1"
class _SidecarAssociationError(RuntimeError):
    def __init__(self, message: str, *, evidence: Mapping[str, Any]):
        super().__init__(message)
        self.evidence = dict(evidence)


def _validate_returned_sidecar(
    capture_payload: Mapping[str, Any],
    *,
    raw_path: Path,
    raw_payload: bytes | None = None,
    run_root: Path,
) -> dict[str, Any]:
    sidecar_value = capture_payload.get("remote_metadata_path")
    sidecar_candidate = Path(str(sidecar_value)) if sidecar_value else None
    evidence = {
        "sidecar_path": None,
        "sidecar_byte_count": None,
        "sidecar_sha256": None,
        "sidecar_validation_status": "fail",
        "remote_capture_id": None,
        "remote_request_id": None,
    }
    try:
        sidecar_path = (
            sidecar_candidate.resolve() if sidecar_candidate is not None else None
        )
        evidence["sidecar_path"] = (
            None if sidecar_path is None else str(sidecar_path)
        )
        invalid_owner = (
            sidecar_path is None
            or not sidecar_path.is_relative_to(run_root)
            or sidecar_candidate is None
            or sidecar_candidate.is_symlink()
            or not sidecar_path.is_file()
            or sidecar_path.stat().st_size <= 0
            or sidecar_path
            != raw_path.with_suffix(raw_path.suffix + ".metadata.json")
        )
    except OSError as exc:
        raise _SidecarAssociationError(
            "capture adapter could not inspect retained CR3 sidecar evidence",
            evidence=evidence,
        ) from exc
    if invalid_owner:
        raise _SidecarAssociationError(
            "capture adapter lacks the retained CR3 sidecar owner",
            evidence=evidence,
        )
    try:
        sidecar_bytes = sidecar_path.read_bytes()
    except OSError as exc:
        raise _SidecarAssociationError(
            "capture adapter could not read retained CR3 sidecar evidence",
            evidence=evidence,
        ) from exc
    evidence.update({
        "sidecar_byte_count": len(sidecar_bytes),
        "sidecar_sha256": hashlib.sha256(sidecar_bytes).hexdigest(),
    })
    try:
        sidecar = json.loads(sidecar_bytes.decode("utf-8"))
        if raw_payload is None:
            raw_payload = raw_path.read_bytes()
        remote_metadata, receipt = camera_remote_v2.split_and_validate_sidecar(
            sidecar,
            payload=raw_payload,
        )
    except (
        OSError,
        UnicodeError,
        json.JSONDecodeError,
        camera_remote_v2.RemoteCaptureV2Error,
    ) as exc:
        raise _SidecarAssociationError(
            "capture adapter retained invalid CR3 sidecar evidence",
            evidence=evidence,
        ) from exc
    evidence.update({
        "sidecar_validation_status": "pass",
        "remote_capture_id": remote_metadata.get("capture_id"),
        "remote_request_id": remote_metadata.get("request_id"),
    })
    if capture_payload.get("timing_metadata") != sidecar:
        raise _SidecarAssociationError(
            "capture adapter timing metadata differs from retained sidecar",
            evidence=evidence,
        )
    if capture_payload.get("timing_evidence") != receipt.get("timing_evidence"):
        raise _SidecarAssociationError(
            "capture adapter timing evidence differs from retained sidecar",
            evidence=evidence,
        )
    return {
        **evidence,
        "remote_metadata": remote_metadata,
        "receipt": receipt,
    }


def _validate_execution_shutter_ledger(plan: Mapping[str, Any]) -> None:
    captures = plan.get("captures")
    frozen = plan.get("frozen_shutters")
    if not isinstance(captures, Sequence) or isinstance(captures, (str, bytes)):
        raise PermissionError("thermal diagnostic execution lacks a capture ledger")
    if not isinstance(frozen, Mapping):
        raise PermissionError("thermal diagnostic execution lacks a frozen shutter ledger")
    try:
        required = thermal.required_shutter_cache_keys(captures)
    except (TypeError, ValueError) as exc:
        raise PermissionError("thermal diagnostic execution has an invalid shutter owner") from exc
    if set(frozen) != set(required):
        raise PermissionError("thermal diagnostic frozen shutters differ from experiment capture steps")
    unresolved = sorted(
        key for key in required
        if not isinstance(frozen.get(key), str) or not str(frozen[key]).strip()
    )
    if plan.get("exposure_setup_required") != unresolved:
        raise PermissionError("thermal diagnostic exposure setup ledger is inconsistent")
    provenance = plan.get("shutter_ledger_provenance")
    if (
        not isinstance(provenance, Mapping)
        or provenance.get("owner") != "experiment_capture_steps"
        or provenance.get("required_cache_keys") != list(required)
        or provenance.get("frozen_shutters_sha256") != thermal.canonical_sha256(dict(frozen))
    ):
        raise PermissionError("thermal diagnostic shutter provenance is inconsistent")
    if unresolved:
        raise PermissionError(f"thermal diagnostic execution has unresolved shutter setup: {unresolved}")
def _resolve_remote_capture_settings(camera_backend: Any) -> tuple[Any, dict[str, str]]:
    resolver = getattr(camera_backend, "resolve_capture_settings", None)
    if not callable(resolver):
        raise PermissionError("remote v2 backend lacks capture settings resolution")
    resolved = resolver(iso=None, aperture=None, image_format="RAW")
    values = {
        "iso": getattr(resolved, "iso", None),
        "aperture": getattr(resolved, "aperture", None),
        "image_format": getattr(resolved, "image_format", None),
    }
    if any(not isinstance(value, str) or not value.strip() for value in values.values()):
        raise PermissionError("remote capture settings must be non-empty strings")
    if values["image_format"] != "RAW":
        raise PermissionError("remote capture settings must resolve exact RAW image format")
    provenance = {
        "owner": "remote_backend.resolve_capture_settings",
        "iso": values["iso"],
        "aperture": values["aperture"],
        "image_format": values["image_format"],
    }
    return resolved, provenance


def validate_authorized_execution_plan(
    plan: Mapping[str, Any], *, camera_backend: Any | None = None,
) -> None:
    if plan.get("schema") != thermal.PLAN_SCHEMA_V2:
        raise PermissionError("thermal diagnostic production execution requires plan schema v2")
    if plan.get("timing_contract") != thermal.timing_contract(2):
        raise PermissionError("thermal diagnostic execution timing contract differs from frozen v2")
    expected_ambient_policy = thermal.expected_native_raw_ambient_policy(
        str(plan.get("experiment_id")),
        plan_schema=str(plan.get("schema")),
    )
    if plan.get("native_raw_ambient_policy") != expected_ambient_policy:
        raise PermissionError("thermal diagnostic native RAW ambient policy differs")
    ambient_steps = [
        step for step in plan.get("captures", [])
        if step.get("capture_role") == "ambient" or step.get("source_id") == "ambient"
    ]
    if expected_ambient_policy == raw_validation.AMBIENT_POLICY_UNSUBTRACTED_NO_AMBIENT:
        if ambient_steps or plan.get("budgets", {}).get("ambient_cap") != 0:
            raise PermissionError("TD-B unsubtracted_no_ambient plan contains ambient evidence")
    for step in plan.get("captures", []):
        if "timing_tolerance_s" in step or "actual_elapsed_s" in step:
            raise PermissionError("thermal diagnostic v2 plan contains legacy timing fields")
        if step.get("formal_measurement") and step.get("timing_acceptance") != "observed_elapsed_record_only":
            raise PermissionError("thermal diagnostic v2 plan lacks observed-elapsed acceptance semantics")
    experiment_id = plan.get("experiment_id")
    if plan.get("status") != "execute_authorized" or experiment_id not in thermal.EXPERIMENT_IDS:
        raise PermissionError("thermal diagnostic execution requires an exact authorized plan")
    authorization = plan.get("execution_authorization")
    expected_authorization_experiment = (
        plan.get("guide_experiment_id") or experiment_id
    )
    direct_ray_history = (
        isinstance(authorization, Mapping)
        and authorization.get("schema") == "direct_ray_history_session_v1"
    )
    direct_strip_history = (
        isinstance(authorization, Mapping)
        and authorization.get("schema") == "direct_strip_history_session_v1"
    )
    direct_ray_fast_long_bridge = (
        isinstance(authorization, Mapping)
        and authorization.get("schema")
        == "direct_ray_fast_long_bridge_session_v1"
    )
    direct_td_c_fast_endpoint = (
        isinstance(authorization, Mapping)
        and authorization.get("schema") == "direct_td_c_fast_endpoint_holdout_v1"
    )
    direct_guide6_target_local = (
        isinstance(authorization, Mapping)
        and authorization.get("schema") == "direct_guide6_target_local_h120_s100_v1"
    )
    direct_guide7_f2 = (
        isinstance(authorization, Mapping)
        and authorization.get("schema") == "direct_guide7_f2_alternate_face_v1"
    )
    direct_guide8_emission_exposure = (
        isinstance(authorization, Mapping)
        and authorization.get("schema") == "direct_guide8_ray_emission_exposure_v1"
    )
    direct_guide6_strip_exposure = (
        isinstance(authorization, Mapping)
        and authorization.get("schema") == "direct_guide6_strip_exposure_qualification_v1"
    )
    if (
        direct_ray_history or direct_strip_history
        or direct_ray_fast_long_bridge or direct_td_c_fast_endpoint
        or direct_guide6_target_local or direct_guide7_f2 or direct_guide8_emission_exposure
        or direct_guide6_strip_exposure
    ):
        valid_execution_scope = (
            authorization.get("bounded_device_scope") is True
            and authorization.get("human_authorization_required") is False
            and authorization.get("experiment_id") == expected_authorization_experiment
            and authorization.get("remote_v2_capability") is True
        )
    else:
        valid_execution_scope = (
            isinstance(authorization, Mapping)
            and str(authorization.get("schema", "")).startswith("direct_")
            and authorization.get("human_authorization_verified") is True
            and authorization.get("human_authorization_experiment_id")
            == expected_authorization_experiment
            and authorization.get("remote_v2_capability") is True
        )
    if not valid_execution_scope:
        raise PermissionError("thermal diagnostic execution lacks its exact bounded/v2 scope")
    if (
        not isinstance(authorization, Mapping)
        or not str(authorization.get("schema", "")).startswith("direct_")
    ):
        raise PermissionError("thermal diagnostic execution lacks a direct execution scope")
    camera = plan.get("camera")
    if (
        not isinstance(camera, Mapping)
        or camera.get("backend") != "remote"
        or camera.get("v2_capture_timing_capability_available") is not True
    ):
        raise PermissionError("thermal diagnostic execution requires remote v2 capture timing capability")
    if any(step.get("formal_measurement") and step.get("requested_elapsed_s") is None for step in plan.get("captures", [])):
        raise PermissionError("thermal diagnostic execution rejects unresolved deferred timing")
    _validate_execution_shutter_ledger(plan)
    if camera_backend is not None:
        if (
            getattr(camera_backend, "backend_name", None) != "remote"
            or getattr(camera_backend, "v2_capture_capability", None) != REMOTE_V2_CAPABILITY
            or not callable(getattr(camera_backend, "connect", None))
            or not callable(getattr(camera_backend, "resolve_capture_settings", None))
            or not callable(getattr(camera_backend, "capture_with_timing", None))
        ):
            raise PermissionError("thermal diagnostic execution requires the formal remote v2 backend owner")


def write_dry_run(
    *, experiment_id: str, output_dir: str | Path = DEFAULT_OUTPUT,
    run_name: str, source: str | None = None, variant: str = "core",
) -> Path:
    root = (Path(output_dir) / run_name).resolve()
    root.mkdir(parents=True, exist_ok=False)
    plan = thermal.build_direct_plan(experiment_id, source=source, variant=variant)
    _write_json(root / "experiment-spec.json", plan)
    return root / "experiment-spec.json"


def _runtime_git_provenance() -> dict[str, Any]:
    commit = subprocess.run(
        ("git", "rev-parse", "HEAD"), cwd=PROJECT_ROOT, check=True,
        capture_output=True, text=True, timeout=30,
    ).stdout.strip()
    dirty_output = subprocess.run(
        ("git", "status", "--porcelain"), cwd=PROJECT_ROOT, check=True,
        capture_output=True, text=True, timeout=30,
    ).stdout
    return {
        "commit": commit,
        "dirty": bool(dirty_output.strip()),
        "dirty_entries": dirty_output.splitlines(),
    }


def _guide6_feature_vector(
    capture: Mapping[str, Any], feature_ids: Sequence[str],
) -> np.ndarray:
    quality = capture.get("direct_quality")
    values = capture.get("feature_values")
    if (
        not isinstance(quality, Mapping)
        or quality.get("status") != "pass"
        or not isinstance(values, Mapping)
        or set(values) != set(feature_ids)
    ):
        raise ValueError("GUIDE6 measurement lacks an accepted frozen feature vector")
    numeric = {name: float(values[name]) for name in feature_ids}
    if any(not math.isfinite(value) for value in numeric.values()):
        raise ValueError("GUIDE6 measurement contains a non-finite feature value")
    return ordered_unit_shape(numeric, feature_ids)


def _guide6_variances(feature_count: int) -> tuple[np.ndarray, np.ndarray]:
    policy = json.loads(thermal.POLICY_PATH.read_text(encoding="utf-8"))
    ray = np.asarray(
        policy["reference_policy"]["ray_within_state_diagonal_variance"],
        dtype=float,
    )
    strip = np.asarray(
        policy["repeatability_policy"]["classes"]["sat100_fullscale"]
        ["p1_floor_diagonal_variance"],
        dtype=float,
    )
    if ray.shape != (feature_count,) or strip.shape != (feature_count,):
        raise ValueError("GUIDE6 frozen covariance differs from the feature identity")
    if np.any(~np.isfinite(ray)) or np.any(~np.isfinite(strip)) or np.any(ray <= 0) or np.any(strip <= 0):
        raise ValueError("GUIDE6 frozen covariance is not positive and finite")
    return ray, strip


def _guide6_protocol_step(
    plan: Mapping[str, Any], *, capture_id: str, source: str, role: str,
    command: Mapping[str, Any],
) -> dict[str, Any]:
    shutter = "ray-h120-s100" if source == "ray" else "strip-h120-s100-fullscale"
    return {
        "capture_id": capture_id,
        "source_id": source,
        "state_id": "A",
        "target": "H120/S100/INT100",
        "role": role,
        "session_index": 1,
        "formal_measurement": True,
        "capture_role": "formal",
        "command": {key: value for key, value in command.items()},
        "exact_command_hash": thermal.canonical_sha256(command),
        "requested_elapsed_s": 120,
        "nominal_shutter": plan["frozen_shutters"][shutter],
        "timing_acceptance": "observed_elapsed_record_only",
        "strip_zero_required": source == "ray",
        "ray_zero_required": source == "strip",
        "steady_claim": False,
    }


def _run_guide6_local_controllability_protocol_core(
    plan: Mapping[str, Any], *,
    measure_fn: Callable[[Mapping[str, Any]], Mapping[str, Any]],
    feature_ids: Sequence[str],
    source_isolation_fn: Callable[[str], Mapping[str, Any]] | None,
) -> dict[str, Any]:
    """Run the protocol-specific adaptive command owner against one measurement seam.

    The caller owns D/A/tested-command dwell, source isolation, physical-return
    accounting and finally cleanup. This function owns only the frozen measurement
    sequence and the command adaptation derived from accepted current-root features.
    """
    contract = plan.get("local_controllability_contract")
    if (
        not isinstance(contract, Mapping)
        or contract.get("schema")
        != "guide6_h120_s100_direct_local_controllability_v1"
    ):
        raise ValueError("GUIDE6 local-controllability contract is missing")
    free = tuple(str(value) for value in contract["free_channels"])
    active_channel = str(contract["active_channel"])
    if active_channel not in thermal.CHANNELS or active_channel in free or len(free) != 4:
        raise ValueError("direct local-controllability active/free channel contract is invalid")
    base_command = {key: int(value) for key, value in contract["base_command"].items()}
    fixed_steps = {str(step["role"]): step for step in plan["captures"]}
    measured: list[dict[str, Any]] = []

    def measure(step: Mapping[str, Any]) -> tuple[dict[str, Any], np.ndarray]:
        if source_isolation_fn is not None:
            isolation = dict(source_isolation_fn(str(step["source_id"])))
            if isolation.get("status") != "pass" or isolation.get("source_verified_zero") is not True:
                raise RuntimeError("GUIDE6 source-isolation gate did not pass")
        capture = dict(measure_fn(step))
        vector = _guide6_feature_vector(capture, feature_ids)
        measured.append({"step": dict(step), "capture": capture, "unit_shape": vector})
        return capture, vector

    _, ray_before = measure(fixed_steps["ray_q_before"])
    _, base = measure(fixed_steps["strip_base"])
    probes: list[np.ndarray] = []
    anchor_vectors: list[np.ndarray] = []
    for probe_number, channel in enumerate(free, start=1):
        _, probe = measure(fixed_steps[f"strip_probe_{channel}"])
        probes.append(probe)
        if probe_number in (2, 4):
            _, anchor = measure(
                fixed_steps[f"strip_base_anchor_after_probe_{probe_number}"]
            )
            anchor_vectors.append(anchor)

    ray_variance, strip_variance = _guide6_variances(len(feature_ids))
    contrast_variance = strip_variance + ray_variance / 2.0
    whitening = np.sqrt(contrast_variance)
    def direct_limits(center: np.ndarray, variance: np.ndarray) -> Mapping[str, Any]:
        calibration_center = center
        if float(np.linalg.norm(calibration_center)) <= 1e-15:
            calibration_center = np.ones_like(calibration_center)
        return calibrate_direct_limits(
            calibration_center, variance, samples=1000,
        )
    base_residual = (base - ray_before) / whitening
    probe_matrix = np.column_stack([
        ((probe - ray_before) / whitening - base_residual)
        / float(contract["probe_step_linearized_code"])
        for probe in probes
    ])
    singular_values = np.linalg.svd(probe_matrix, compute_uv=False)
    effective_rank = int(np.linalg.matrix_rank(probe_matrix))
    condition = (
        None
        if not len(singular_values) or singular_values[-1] <= 0
        else float(singular_values[0] / singular_values[-1])
    )
    limits = direct_limits(base - ray_before, contrast_variance)
    guarded_limit = float(limits["guarded_limit"])
    base_score = float(np.linalg.norm(base_residual))
    anchor_diagnostics = []
    drift_pass = True
    for index, anchor in enumerate(anchor_vectors, start=1):
        anchor_score = float(np.linalg.norm((anchor - base) / np.sqrt(2.0 * strip_variance)))
        anchor_limit = float(direct_limits(
            anchor - base, 2.0 * strip_variance,
        )["guarded_limit"])
        passed = anchor_score <= anchor_limit
        drift_pass = drift_pass and passed
        anchor_diagnostics.append({
            "anchor_number": index,
            "score": anchor_score,
            "guarded_limit": anchor_limit,
            "decision": "pass" if passed else "fail",
        })

    candidates: list[dict[str, Any]] = []
    confirmations: list[dict[str, Any]] = []
    best_score = base_score
    best_command = dict(base_command)
    best_residual = base_residual.copy()
    model_center = np.asarray([base_command[channel] for channel in free], dtype=float)
    model_residual = base_residual.copy()
    jacobian = probe_matrix.copy()
    jacobian_version = 1
    rebase_count = 0
    passing_command: dict[str, int] | None = None
    used_hashes = {thermal.canonical_sha256(base_command)}
    backtracks = tuple(float(value) for value in contract["backtrack_factors"])
    maximum_candidates = int(contract["maximum_feedback_candidates"])

    while drift_pass and len(candidates) < maximum_candidates and passing_command is None:
        lower = np.maximum(-float(contract["maximum_absolute_step"]), -model_center)
        upper = np.minimum(
            float(contract["maximum_absolute_step"]), 4095.0 - model_center,
        )
        regularization = 1e-6
        matrix = np.vstack([jacobian, math.sqrt(regularization) * np.eye(len(free))])
        target = np.concatenate([-model_residual, np.zeros(len(free))])
        full_delta = solve_box_constrained_least_squares(matrix, target, lower, upper)
        measured_this_model = False
        for factor in backtracks:
            if len(candidates) >= maximum_candidates:
                break
            candidate_values = np.rint(model_center + factor * full_delta).astype(int)
            candidate_values = np.clip(candidate_values, 0, 4095)
            command = dict(base_command)
            for index, channel in enumerate(free):
                command[channel] = int(candidate_values[index])
            command[active_channel] = int(contract["active_value"])
            command_hash = thermal.canonical_sha256(command)
            if command_hash in used_hashes:
                continue
            used_hashes.add(command_hash)
            actual_delta = candidate_values.astype(float) - model_center
            predicted_residual = model_residual + jacobian @ actual_delta
            predicted_score = float(np.linalg.norm(predicted_residual))
            step = _guide6_protocol_step(
                plan,
                capture_id=f"{100 + len(candidates):03d}-strip-h120-s100-solver-candidate",
                source="strip",
                role=f"strip_solver_candidate_{len(candidates) + 1}",
                command=command,
            )
            _, candidate_vector = measure(step)
            residual = (candidate_vector - ray_before) / whitening
            score = float(np.linalg.norm(residual))
            predicted_reduction = float(model_residual @ model_residual - predicted_residual @ predicted_residual)
            actual_reduction = float(model_residual @ model_residual - residual @ residual)
            trust_ratio = (
                actual_reduction / predicted_reduction
                if predicted_reduction > 0.0 else None
            )
            candidates.append({
                "candidate_number": len(candidates) + 1,
                "exact_command": command,
                "exact_command_hash": command_hash,
                "predicted_residual_vector": predicted_residual.tolist(),
                "predicted_direct_score": predicted_score,
                "measured_residual_vector": residual.tolist(),
                "measured_direct_score": score,
                "predicted_reduction": predicted_reduction,
                "actual_reduction": actual_reduction,
                "trust_ratio": trust_ratio,
                "active_bounds": [
                    channel for index, channel in enumerate(free)
                    if candidate_values[index] in (0, 4095)
                ] + [active_channel],
                "backtrack_factor": factor,
                "jacobian_version": jacobian_version,
            })
            measured_this_model = True
            if score < best_score:
                best_score = score
                best_command = command
                best_residual = residual.copy()
            if score <= guarded_limit:
                passing_command = command
                break
            if rebase_count == 0 and float(actual_delta @ actual_delta) > 0.0:
                correction = residual - model_residual - jacobian @ actual_delta
                jacobian = jacobian + np.outer(correction, actual_delta) / float(actual_delta @ actual_delta)
                model_center = candidate_values.astype(float)
                model_residual = residual
                jacobian_version += 1
                rebase_count = 1
                break
        if not measured_this_model or rebase_count == 0:
            break
        if rebase_count == 1 and candidates[-1]["jacobian_version"] == jacobian_version:
            break

    if passing_command is not None:
        for index in range(1, int(contract["confirmation_count"]) + 1):
            step = _guide6_protocol_step(
                plan,
                capture_id=f"{200 + index:03d}-strip-h120-s100-confirmation",
                source="strip",
                role=f"strip_confirmation_{index}",
                command=passing_command,
            )
            _, vector = measure(step)
            residual = (vector - ray_before) / whitening
            confirmations.append({
                "confirmation_number": index,
                "exact_command_hash": thermal.canonical_sha256(passing_command),
                "measured_residual_vector": residual.tolist(),
                "measured_direct_score": float(np.linalg.norm(residual)),
            })
    elif int(contract.get("repeat_best_nonfaithful_count", 0)):
        for index in range(1, int(contract["repeat_best_nonfaithful_count"]) + 1):
            step = _guide6_protocol_step(
                plan,
                capture_id=f"{300 + index:03d}-strip-h120-s100-best-repeat",
                source="strip", role=f"strip_repeat_{index}", command=best_command,
            )
            _, vector = measure(step)
            residual = (vector - ray_before) / whitening
            confirmations.append({
                "confirmation_number": index,
                "role": f"strip_repeat_{index}",
                "exact_command_hash": thermal.canonical_sha256(best_command),
                "measured_residual_vector": residual.tolist(),
                "measured_direct_score": float(np.linalg.norm(residual)),
            })

    _, ray_after = measure(fixed_steps["ray_q_after"])
    ray_bracket_score = float(np.linalg.norm((ray_after - ray_before) / np.sqrt(2.0 * ray_variance)))
    ray_bracket_limit = float(direct_limits(
        ray_after - ray_before, 2.0 * ray_variance,
    )["guarded_limit"])
    ray_bracket_pass = ray_bracket_score <= ray_bracket_limit
    if not ray_bracket_pass or not drift_pass:
        classification = "target_block_reference_invalid"
        lc_branch = "LC-E"
    elif passing_command is not None and len(confirmations) == 3:
        classification = "H120_S100_direct_local_solver_pass"
        lc_branch = "LC-A"
    elif best_score < base_score:
        classification = "H120_S100_local_controllable_but_not_yet_faithful"
        lc_branch = "LC-B"
    else:
        classification = "G_active_neighborhood_inadequate"
        lc_branch = "LC-C"
    strip_count = sum(item["step"]["source_id"] == "strip" for item in measured)
    ray_count = sum(item["step"]["source_id"] == "ray" for item in measured)
    if strip_count > 14 or ray_count != 2 or len(measured) > 16:
        raise RuntimeError("GUIDE6 adaptive protocol exceeded its frozen capture budget")
    return {
        "schema": "guide6_h120_s100_direct_local_controllability_evidence_v1",
        "continuation_generation": int(contract.get("continuation_generation", 0)),
        "guide7_f2": plan.get("variant") == thermal.GUIDE7_F2_VARIANT,
        "active_face": str(contract["active_channel"]),
        "classification": classification,
        "lc_branch": lc_branch,
        "gamut_inference": "prohibited",
        "terminal_multi_start_solver_unresolved": False,
        "feature_count": len(feature_ids),
        "navigation_coordinate": "direct_whitened_58_feature_residual",
        "base": {"exact_command": base_command, "direct_score": base_score},
        "jacobian": {
            "matrix": probe_matrix.tolist(),
            "singular_values": singular_values.tolist(),
            "effective_rank": effective_rank,
            "condition": condition,
            "probe_step": int(contract["probe_step_linearized_code"]),
        },
        "base_anchors": anchor_diagnostics,
        "ray_bracket": {
            "score": ray_bracket_score, "guarded_limit": ray_bracket_limit,
            "decision": "pass" if ray_bracket_pass else "fail",
        },
        "direct_guarded_limit": guarded_limit,
        "candidates": candidates,
        "best": {"exact_command": best_command, "direct_score": best_score,
                 "residual_vector": best_residual.tolist()},
        "model_rebase_count": rebase_count,
        "model_rebase_extra_probe_count": 0,
        "confirmations": confirmations,
        "counts": {
            "ray": ray_count, "strip": strip_count, "total": len(measured),
            "ambient": 0, "in_root_retry": 0,
        },
        "measured_steps": [item["step"] for item in measured],
    }


def run_guide6_local_controllability_protocol(
    plan: Mapping[str, Any], *,
    measure_fn: Callable[[Mapping[str, Any]], Mapping[str, Any]],
    feature_ids: Sequence[str],
    source_isolation_fn: Callable[[str], Mapping[str, Any]] | None = None,
    cleanup_fn: Callable[[], Mapping[str, Any]] | None = None,
) -> dict[str, Any]:
    """Execute the bounded adaptive core and always perform its supplied cleanup."""
    failure: BaseException | None = None
    try:
        return _run_guide6_local_controllability_protocol_core(
            plan,
            measure_fn=measure_fn,
            feature_ids=feature_ids,
            source_isolation_fn=source_isolation_fn,
        )
    except BaseException as exc:
        failure = exc
        raise
    finally:
        if cleanup_fn is not None:
            cleanup = dict(cleanup_fn())
            cleanup_pass = cleanup.get("status") in {"pass", "complete", "all_off"} or cleanup.get("ok") is True
            if not cleanup_pass and failure is None:
                raise RuntimeError("GUIDE6 protocol cleanup did not pass")


def _guide8_quality_class(capture: Mapping[str, Any], *, feature_count: int) -> str:
    quality = capture.get("direct_quality")
    if not isinstance(quality, Mapping):
        return "evidence_failure"
    status = str(quality.get("status", ""))
    failures = quality.get("failures", ())
    failure_set = {str(item) for item in failures} if isinstance(failures, Sequence) and not isinstance(failures, (str, bytes)) else set()
    if status == "pass":
        values = capture.get("feature_values")
        recorded = capture.get("recorded_exposure")
        if (
            quality.get("feature_count") != feature_count
            or not isinstance(values, Mapping)
            or len(values) != feature_count
            or any(not isinstance(value, (int, float)) or not math.isfinite(float(value)) for value in values.values())
            or not isinstance(recorded, Mapping)
        ):
            return "evidence_failure"
        return "pass"
    if status == "near_noise_only" or failure_set == {"near_noise"}:
        return "near_noise_only"
    if status in {"clipping", "nonfinite", "unexpected_bright", "shape_failure"}:
        return status
    if "clipping" in failure_set:
        return "clipping"
    if "nonfinite" in failure_set:
        return "nonfinite"
    return "unexpected_quality_failure"


def _nominal_exposure_ratio(faster: str, slower: str) -> float:
    from camera_based_rgbww_optimizer.measurement.recorded_exposure import parse_nominal_exposure

    fast_s = float(parse_nominal_exposure(faster))
    slow_s = float(parse_nominal_exposure(slower))
    if fast_s <= 0 or slow_s <= 0 or slow_s < fast_s:
        raise ValueError("GUIDE8 shutter ladder is not ordered fast-to-slow")
    return slow_s / fast_s


def run_guide8_emission_exposure_protocol(
    plan: Mapping[str, Any], *,
    measure_fn: Callable[[Mapping[str, Any]], Mapping[str, Any]],
    feature_ids: Sequence[str],
    pair_evaluator_fn: Callable[[Mapping[str, Any], Mapping[str, Any]], Mapping[str, Any] | bool],
    cleanup_fn: Callable[[], Mapping[str, Any]] | None = None,
) -> dict[str, Any]:
    """Run GUIDE8 early-stop semantics over the exact predeclared diagnostic steps."""
    if (
        plan.get("guide_experiment_id") != thermal.GUIDE8_RAY_EMISSION_EXPOSURE_EXPERIMENT_ID
        or (plan.get("execution_authorization") or {}).get("schema")
        != "direct_guide8_ray_emission_exposure_v1"
    ):
        raise ValueError("GUIDE8 emission/exposure protocol requires its exact direct spec")
    if len(feature_ids) != 58:
        raise ValueError("GUIDE8 requires the frozen 58-feature observer")
    steps = list(plan.get("captures", ()))
    if len(steps) != 16 or [str(step.get("nominal_shutter")) for step in steps[2:]] != list(thermal.GUIDE8_RAY_EMISSION_EXPOSURE_LADDER):
        raise ValueError("GUIDE8 capture ladder differs from the frozen 16-frame cap")
    measured: list[dict[str, Any]] = []
    result: dict[str, Any] | None = None
    failure: BaseException | None = None
    try:
        control = dict(measure_fn(steps[0]))
        measured.append({"step": dict(steps[0]), "capture": control})
        if _guide8_quality_class(control, feature_count=58) != "pass":
            result = {"branch": "E-A", "classification": "Ray_or_optical_path_unverified"}
        else:
            dark = dict(measure_fn(steps[1]))
            measured.append({"step": dict(steps[1]), "capture": dark})
            dark_class = _guide8_quality_class(dark, feature_count=58)
            if dark_class == "pass" or dark_class in {"clipping", "unexpected_bright"}:
                result = {"branch": "E-B", "classification": "environment_or_optical_leak_unresolved"}
            elif dark_class not in {"near_noise_only"}:
                result = {"branch": "E-B", "classification": "environment_or_optical_leak_unresolved"}
        previous_valid: tuple[Mapping[str, Any], Mapping[str, Any]] | None = None
        saw_near_noise = False
        if result is None:
            for step in steps[2:]:
                capture = dict(measure_fn(step))
                measured.append({"step": dict(step), "capture": capture})
                quality_class = _guide8_quality_class(capture, feature_count=58)
                if quality_class == "near_noise_only":
                    saw_near_noise = True
                    previous_valid = None
                    continue
                if quality_class != "pass":
                    if quality_class == "clipping" and saw_near_noise:
                        result = {
                            "branch": "E-E",
                            "classification": "no_single_exposure_window_under_frozen_observer",
                            "stop_reason": quality_class,
                        }
                        break
                    raise RuntimeError(
                        "GUIDE8 ladder stopped on non-scientific quality/evidence failure: "
                        f"{quality_class}"
                    )
                if previous_valid is not None:
                    previous_step, previous_capture = previous_valid
                    ratio = _nominal_exposure_ratio(
                        str(previous_step["nominal_shutter"]), str(step["nominal_shutter"]),
                    )
                    if ratio <= float(plan["analysis_contract"]["maximum_exposure_ratio"]):
                        evaluation_value = pair_evaluator_fn(previous_capture, capture)
                        evaluation = (
                            {"status": "pass" if evaluation_value else "fail"}
                            if isinstance(evaluation_value, bool) else dict(evaluation_value)
                        )
                        shape_pass = evaluation.get("status") == "pass" or evaluation.get("pass") is True
                        if not shape_pass:
                            result = {"branch": "E-G", "classification": "exposure_response_not_invariant_for_current_state", "pair_evaluation": evaluation}
                            break
                        selected = str(previous_step["nominal_shutter"])
                        result = {
                            "branch": "E-C" if selected == "1/5000" else "E-D",
                            "classification": "historical_shutter_requalified" if selected == "1/5000" else "state_specific_exposure_window_shift",
                            "selected_nominal_shutter": selected,
                            "guard_nominal_shutter": str(step["nominal_shutter"]),
                            "nominal_exposure_ratio": ratio,
                            "pair_evaluation": evaluation,
                        }
                        break
                previous_valid = (step, capture)
            if result is None:
                result = {"branch": "E-F", "classification": "H120_S100_reference_emission_not_established"}
        return {
            "schema": "guide8_ray_emission_exposure_evidence_v1",
            **result, "measured": measured, "physical_capture_count": len(measured),
            "formal_capture_count": 0,
        }
    except BaseException as exc:
        failure = exc
        raise
    finally:
        if cleanup_fn is not None:
            cleanup = dict(cleanup_fn())
            cleanup_pass = cleanup.get("status") in {"pass", "complete", "all_off"} or cleanup.get("ok") is True
            if not cleanup_pass and failure is None:
                raise RuntimeError("GUIDE8 protocol cleanup did not pass")


def run_guide6_strip_exposure_qualification_protocol(
    plan: Mapping[str, Any], *,
    measure_fn: Callable[[Mapping[str, Any]], Mapping[str, Any]],
    feature_ids: Sequence[str],
    pair_evaluator_fn: Callable[[Mapping[str, Any], Mapping[str, Any]], Mapping[str, Any] | bool],
    cleanup_fn: Callable[[], Mapping[str, Any]] | None = None,
) -> dict[str, Any]:
    """Run the bounded strip-only S-MEASUREMENT shutter ladder."""
    if (
        plan.get("guide_experiment_id")
        != thermal.GUIDE6_STRIP_EXPOSURE_QUALIFICATION_EXPERIMENT_ID
        or (plan.get("execution_authorization") or {}).get("schema")
        != "direct_guide6_strip_exposure_qualification_v1"
    ):
        raise ValueError("GUIDE6 strip exposure qualification requires its exact direct spec")
    if len(feature_ids) != 58:
        raise ValueError("GUIDE6 strip exposure qualification requires 58 frozen features")
    steps = list(plan.get("captures", ()))
    if [str(step.get("nominal_shutter")) for step in steps] != list(
        thermal.GUIDE6_STRIP_EXPOSURE_QUALIFICATION_LADDER
    ):
        raise ValueError("GUIDE6 strip exposure ladder differs from its frozen contract")
    measured: list[dict[str, Any]] = []
    failure: BaseException | None = None
    try:
        previous_valid: tuple[Mapping[str, Any], Mapping[str, Any]] | None = None
        result: dict[str, Any] | None = None
        for step in steps:
            capture = dict(measure_fn(step))
            measured.append({"step": dict(step), "capture": capture})
            quality_class = _guide8_quality_class(capture, feature_count=58)
            if quality_class == "near_noise_only":
                previous_valid = None
                continue
            if quality_class != "pass":
                raise RuntimeError(
                    "GUIDE6 strip exposure qualification stopped on quality/evidence failure: "
                    f"{quality_class}"
                )
            if previous_valid is not None:
                previous_step, previous_capture = previous_valid
                evaluation_value = pair_evaluator_fn(previous_capture, capture)
                evaluation = (
                    {"status": "pass" if evaluation_value else "fail"}
                    if isinstance(evaluation_value, bool) else dict(evaluation_value)
                )
                if not (
                    evaluation.get("status") == "pass"
                    or evaluation.get("pass") is True
                ):
                    raise RuntimeError(
                        "GUIDE6 strip exposure qualification shape compatibility failed"
                    )
                result = {
                    "classification": "strip_exposure_window_qualified",
                    "selected_nominal_shutter": str(previous_step["nominal_shutter"]),
                    "guard_nominal_shutter": str(step["nominal_shutter"]),
                    "pair_evaluation": evaluation,
                }
                break
            previous_valid = (step, capture)
        if result is None:
            result = {
                "classification": "no_legal_strip_exposure_window",
                "next_gate": "ADVISOR_GATE_REQUIRED",
            }
        return {
            "schema": "guide6_strip_exposure_qualification_evidence_v1",
            **result,
            "measured": measured,
            "physical_capture_count": len(measured),
            "formal_capture_count": 0,
            "solver_probe_count": 0,
        }
    except BaseException as exc:
        failure = exc
        raise
    finally:
        if cleanup_fn is not None:
            cleanup = dict(cleanup_fn())
            cleanup_pass = cleanup.get("status") in {"pass", "complete", "all_off"} or cleanup.get("ok") is True
            if not cleanup_pass and failure is None:
                raise RuntimeError("GUIDE6 strip exposure qualification cleanup did not pass")


def _write_reproducibility_checkpoint(
    root: Path, plan: Mapping[str, Any], git_provenance: Mapping[str, Any],
) -> dict[str, Any]:
    inputs = plan.get("inputs")
    if not isinstance(inputs, Mapping):
        raise PermissionError("direct thermal execution lacks reproducible input references")
    checkpoint_inputs: dict[str, Any] = {}
    for name, destination in (
        ("location", "inputs/location.json"),
        ("code_duty_curve", "inputs/code-duty-curve.json"),
    ):
        reference = inputs.get(name)
        if not isinstance(reference, Mapping) or not isinstance(reference.get("path"), str):
            raise PermissionError(f"direct thermal execution lacks {name} input reference")
        source = Path(reference["path"]).resolve()
        if source.is_symlink() or not source.is_file():
            raise PermissionError(f"direct thermal execution cannot read {name} input")
        payload = source.read_bytes()
        digest = hashlib.sha256(payload).hexdigest()
        if reference.get("sha256") != digest:
            raise PermissionError(f"direct thermal execution {name} input hash drifted")
        target = root / destination
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(payload)
        checkpoint_inputs[name] = {
            "source_path": str(source),
            "run_path": destination,
            "sha256": digest,
            "byte_count": len(payload),
        }
    checkpoint = {
        "schema": "p7_direct_reproducibility_checkpoint_v1",
        "git": dict(git_provenance),
        "inputs": checkpoint_inputs,
    }
    _write_json(root / "input-checkpoint.json", checkpoint)
    return checkpoint


def execute_plan(
    plan: Mapping[str, Any], *, run_dir: str | Path,
    apply_command_fn: Callable[[Mapping[str, Any]], Mapping[str, Any]],
    readback_fn: Callable[[Mapping[str, Any]], Mapping[str, Any]],
    capture_fn: Callable[[Mapping[str, Any]], Mapping[str, Any]],
    both_off_gate_fn: Callable[[str], Mapping[str, Any]],
    cleanup_fn: Callable[[], Mapping[str, Any]],
    source_isolation_check_fn: Callable[[str], Mapping[str, Any]] | None = None,
    runtime_capture_settings_provenance: Mapping[str, Any] | None = None,
    runtime_git_provenance: Mapping[str, Any] | None = None,
    post_capture_validator_fn: Callable[
        [Path, Mapping[str, Any], Mapping[str, Any] | None], Any
    ] | None = None,
    bind_physical_return_observer_fn: Callable[
        [Callable[[Mapping[str, Any], Any, int], Mapping[str, Any]]],
        None,
    ] | None = None,
    set_capture_context_fn: Callable[[float], None] | None = None,
    monotonic_fn: Callable[[], float] = time.monotonic,
    sleep_fn: Callable[[float], None] = time.sleep,
) -> Path:
    validate_authorized_execution_plan(plan)
    direct_execution = (
        isinstance(plan.get("execution_authorization"), Mapping)
        and str(plan["execution_authorization"].get("schema", "")).startswith("direct_")
    )
    if direct_execution and post_capture_validator_fn is None:
        raise PermissionError("direct thermal execution requires its post-capture validator")
    direct_ray_continuous = (
        isinstance(plan.get("execution_authorization"), Mapping)
        and plan["execution_authorization"].get("schema") in {
            "direct_ray_r6_authority_v1", "direct_ray_history_session_v1",
            "direct_ray_fast_long_bridge_session_v1",
        }
    )
    direct_strip_history = (
        isinstance(plan.get("execution_authorization"), Mapping)
        and plan["execution_authorization"].get("schema")
        == "direct_strip_history_session_v1"
    )
    direct_td_c_fast_endpoint = (
        isinstance(plan.get("execution_authorization"), Mapping)
        and plan["execution_authorization"].get("schema")
        == "direct_td_c_fast_endpoint_holdout_v1"
    )
    direct_guide6_target_local = (
        isinstance(plan.get("execution_authorization"), Mapping)
        and plan["execution_authorization"].get("schema")
        == "direct_guide6_target_local_h120_s100_v1"
    )
    direct_guide7_f2 = (
        isinstance(plan.get("execution_authorization"), Mapping)
        and plan["execution_authorization"].get("schema")
        == "direct_guide7_f2_alternate_face_v1"
    )
    direct_f2_short = (
        isinstance(plan.get("execution_authorization"), Mapping)
        and plan["execution_authorization"].get("schema")
        == "direct_guide7_f2_short_endpoint_v1"
    )
    direct_guide8_emission_exposure = (
        isinstance(plan.get("execution_authorization"), Mapping)
        and plan["execution_authorization"].get("schema")
        == "direct_guide8_ray_emission_exposure_v1"
    )
    direct_guide6_strip_exposure = (
        isinstance(plan.get("execution_authorization"), Mapping)
        and plan["execution_authorization"].get("schema")
        == "direct_guide6_strip_exposure_qualification_v1"
    )
    if (
        direct_ray_continuous or direct_guide6_target_local or direct_guide7_f2 or direct_f2_short
        or direct_guide8_emission_exposure or direct_guide6_strip_exposure
    ) and source_isolation_check_fn is None:
        raise PermissionError("direct adaptive execution requires its source-isolation check")
    git_provenance = copy.deepcopy(
        runtime_git_provenance if runtime_git_provenance is not None else _runtime_git_provenance()
    )
    if direct_execution and git_provenance.get("dirty") is not False:
        raise PermissionError("direct thermal execution requires a clean Git checkpoint")
    capture_settings_provenance = copy.deepcopy(
        runtime_capture_settings_provenance
        if runtime_capture_settings_provenance is not None
        else plan["camera"].get("resolved_capture_settings")
    )
    if direct_execution and (
        not isinstance(capture_settings_provenance, Mapping)
        or set(capture_settings_provenance) != {"owner", "iso", "aperture", "image_format"}
        or capture_settings_provenance.get("owner")
        != "remote_backend.resolve_capture_settings"
        or any(
            not isinstance(capture_settings_provenance.get(key), str)
            or not capture_settings_provenance[key].strip()
            for key in ("iso", "aperture", "image_format")
        )
        or capture_settings_provenance.get("image_format") != "RAW"
    ):
        raise PermissionError("Ray R6 execution requires explicit resolved capture settings")
    root = Path(run_dir)
    root.mkdir(parents=True, exist_ok=True)
    if any(root.iterdir()):
        raise FileExistsError(f"thermal run directory must be empty: {root}")
    _write_json(root / "experiment-spec.json", dict(plan))
    reproducibility_checkpoint = (
        _write_reproducibility_checkpoint(root, plan, git_provenance)
        if direct_execution else None
    )
    run = {
        "schema": "p7_thermal_diagnostic_run_v2", "experiment_id": plan["experiment_id"],
        "status": "running", "started_at": _utc_now(), "completed_formal": 0,
        "ambient_capture_count": 0,
        "accepted_formal_count": 0, "accepted_ambient_count": 0,
        "diagnostic_capture_count": 0, "accepted_diagnostic_count": 0,
        "physical_returned_cr3_count": 0,
        "setup_physical_cr3_count": int(plan.get("setup_physical_cr3_count", 0)),
        "physical_cr3_count": int(plan.get("setup_physical_cr3_count", 0)), "cleanup": "pending",
        "capture_settings_provenance": capture_settings_provenance,
        "git": git_provenance,
        "reproducibility_checkpoint": (
            None if reproducibility_checkpoint is None else "input-checkpoint.json"
        ),
    }
    _write_json(root / "run.json", run)
    failure: BaseException | None = None
    session_start = monotonic_fn()
    previous_state: str | None = None
    previous_dwell: float | None = None
    last_observed_by_group: dict[int, float] = {}
    owned_cr3_paths: set[Path] = set()
    physical_returns_by_capture: dict[str, dict[str, Any]] = {}
    rejected_capture: dict[str, Any] | None = None
    expected_formal_count = int(plan["budgets"]["formal_cap"])

    def record_gate(gate_id: str) -> None:
        evidence = dict(both_off_gate_fn(gate_id))
        if evidence.get("status") != "pass" or evidence.get("strip_verified_off") is not True or evidence.get("ray_verified_off") is not True:
            raise RuntimeError(f"both-source off/readback gate failed: {gate_id}")
        _append_jsonl(root / "isolation-gates.jsonl", {
            "gate_id": gate_id, "gate_kind": "both_off", "evidence": evidence, "at": _utc_now(),
        })

    def record_source_isolation_gate(gate_id: str) -> None:
        if source_isolation_check_fn is None:
            raise RuntimeError("strip-only source isolation owner is not bound")
        evidence = dict(source_isolation_check_fn(gate_id))
        legacy_zero = (
            evidence.get("strip_verified_off") is True
            and evidence.get("ray_off_command") is None
        )
        if evidence.get("status") != "pass" or not (
            evidence.get("source_verified_zero") is True or legacy_zero
        ):
            raise RuntimeError(f"strip-only source isolation check failed: {gate_id}")
        _append_jsonl(root / "isolation-gates.jsonl", {
            "gate_id": gate_id, "gate_kind": "strip_zero_only", "evidence": evidence, "at": _utc_now(),
        })

    def ensure_physical_capacity() -> None:
        if run["physical_cr3_count"] >= int(plan["budgets"]["physical_cr3_cap"]):
            raise RuntimeError("thermal diagnostic physical CR3 cap exhausted before camera request")

    def record_physical_return(
        step: Mapping[str, Any],
        returned: Any,
        reported_physical: int,
    ) -> Mapping[str, Any]:
        nonlocal rejected_capture
        if type(reported_physical) is not int:
            raise RuntimeError("capture adapter physical count must be a non-bool integer")
        capture_payload = (
            returned.to_jsonable()
            if hasattr(returned, "to_jsonable")
            else dict(returned)
            if isinstance(returned, Mapping)
            else {}
        )
        raw_path_value = capture_payload.get("saved_file")
        raw_candidate = Path(str(raw_path_value)) if raw_path_value else None
        raw_path = raw_candidate.resolve() if raw_candidate is not None else None
        rejected_capture = {
            "capture_id": step["capture_id"],
            "rejection_stage": "physical_return_validation",
            "reported_physical_capture_count": reported_physical,
            "cr3_path": None if raw_path is None else str(raw_path),
            "cr3_sha256": None,
            "cr3_byte_count": None,
            "sidecar_path": None,
            "sidecar_byte_count": None,
            "sidecar_sha256": None,
            "sidecar_validation_status": "pending",
            "remote_capture_id": None,
            "remote_request_id": None,
        }
        run_root = root.resolve()
        if (
            raw_path is None
            or not raw_path.is_relative_to(run_root)
            or raw_candidate is None
            or raw_candidate.is_symlink()
            or not raw_path.is_file()
            or raw_path.stat().st_size <= 0
        ):
            raise RuntimeError("capture adapter lacks a unique retained nonempty current-run CR3")
        if raw_path in owned_cr3_paths:
            raise RuntimeError("capture adapter reused a CR3 already owned by another capture")
        if str(step["capture_id"]) in physical_returns_by_capture:
            raise RuntimeError("capture adapter duplicated a physical return owner")
        if reported_physical != 1:
            raise RuntimeError("thermal capture reported physical count differs from one retained CR3")
        ensure_physical_capacity()
        raw_payload = raw_path.read_bytes()
        sha256 = hashlib.sha256(raw_payload).hexdigest()
        byte_count = len(raw_payload)
        association_error: RuntimeError | None = None
        if capture_payload.get("byte_count") not in {None, byte_count} or capture_payload.get(
            "sha256"
        ) not in {None, sha256}:
            association_error = RuntimeError(
                "capture adapter CR3 digest differs from retained physical return"
            )
        try:
            sidecar_result = _validate_returned_sidecar(
                capture_payload,
                raw_path=raw_path,
                raw_payload=raw_payload,
                run_root=run_root,
            )
        except _SidecarAssociationError as exc:
            sidecar_evidence = dict(exc.evidence)
            if association_error is None:
                association_error = exc
        else:
            sidecar_evidence = {
                key: sidecar_result[key]
                for key in (
                    "sidecar_path",
                    "sidecar_byte_count",
                    "sidecar_sha256",
                    "sidecar_validation_status",
                    "remote_capture_id",
                    "remote_request_id",
                )
            }

        remote_capture_id = sidecar_evidence["remote_capture_id"]
        remote_request_id = sidecar_evidence["remote_request_id"]
        row = {
            "schema": thermal.PHYSICAL_RETURN_LEDGER_SCHEMA,
            "physical_index": run["physical_returned_cr3_count"] + 1,
            "capture_id": str(step["capture_id"]),
            "source_id": str(step["source_id"]),
            "state_id": str(step["state_id"]),
            "cr3_path": str(raw_path),
            "cr3_byte_count": byte_count,
            "cr3_sha256": sha256,
            **sidecar_evidence,
            "remote_capture_id": remote_capture_id,
            "remote_request_id": remote_request_id,
            "returned_at": _utc_now(),
            "accepted_measurement": False,
        }
        owned_cr3_paths.add(raw_path)
        physical_returns_by_capture[str(step["capture_id"])] = row
        _append_jsonl(root / "physical-returns.jsonl", row)
        run["physical_returned_cr3_count"] += 1
        run["physical_cr3_count"] = (
            run["setup_physical_cr3_count"] + run["physical_returned_cr3_count"]
        )
        rejected_capture.update({
            "rejection_stage": "post_return_processing",
            "cr3_sha256": sha256,
            "cr3_byte_count": byte_count,
            **sidecar_evidence,
            "remote_capture_id": remote_capture_id,
            "remote_request_id": remote_request_id,
        })
        _write_json(root / "run.json", run)
        if association_error is not None:
            rejected_capture["rejection_stage"] = "sidecar_association"
            raise association_error
        return {
            "schema": thermal.PHYSICAL_RETURN_LEDGER_SCHEMA,
            "physical_index": row["physical_index"],
            "capture_id": row["capture_id"],
            "cr3_sha256": sha256,
            "cr3_byte_count": byte_count,
            "sidecar_sha256": sidecar_evidence["sidecar_sha256"],
            "sidecar_byte_count": sidecar_evidence["sidecar_byte_count"],
        }

    if bind_physical_return_observer_fn is not None:
        bind_physical_return_observer_fn(record_physical_return)

    def retain_capture(
        step: Mapping[str, Any], capture: Mapping[str, Any],
        *, owner_start: float | None, chronology_group_index: int,
    ) -> None:
        nonlocal rejected_capture
        reported_physical = capture.get("physical_capture_count")
        if type(reported_physical) is not int:
            raise RuntimeError("capture adapter physical count must be a non-bool integer")
        raw_path_value = capture.get("saved_file") or (capture.get("capture") or {}).get("saved_file")
        raw_candidate = Path(str(raw_path_value)) if raw_path_value else None
        raw_path = raw_candidate.resolve() if raw_candidate is not None else None
        receipt = capture.get("physical_return_receipt")
        retained = physical_returns_by_capture.get(str(step["capture_id"]))
        if retained is None:
            receipt = record_physical_return(step, capture, reported_physical)
            retained = physical_returns_by_capture[str(step["capture_id"])]
        expected_receipt = {
            "schema": thermal.PHYSICAL_RETURN_LEDGER_SCHEMA,
            "physical_index": retained["physical_index"],
            "capture_id": retained["capture_id"],
            "cr3_sha256": retained["cr3_sha256"],
            "cr3_byte_count": retained["cr3_byte_count"],
            "sidecar_sha256": retained["sidecar_sha256"],
            "sidecar_byte_count": retained["sidecar_byte_count"],
        }
        if receipt != expected_receipt:
            raise RuntimeError("capture adapter physical return receipt differs from retained ledger")
        run_root = root.resolve()
        if raw_path != Path(retained["cr3_path"]).resolve():
            raise RuntimeError("capture adapter CR3 owner differs from physical return ledger")
        rejected_capture = {
            **rejected_capture,
            "rejection_stage": "sidecar_and_timing_validation",
            "sidecar_path": retained.get("sidecar_path"),
        }
        try:
            sidecar_result = _validate_returned_sidecar(
                capture,
                raw_path=raw_path,
                run_root=run_root,
            )
        except _SidecarAssociationError as exc:
            rejected_capture.update(exc.evidence)
            raise
        if any(
            sidecar_result[key] != retained.get(key)
            for key in (
                "sidecar_path",
                "sidecar_byte_count",
                "sidecar_sha256",
                "sidecar_validation_status",
            )
        ):
            raise RuntimeError("capture adapter sidecar owner differs from physical return ledger")
        rejected_capture.update({
            "sidecar_byte_count": retained["sidecar_byte_count"],
            "sidecar_sha256": retained["sidecar_sha256"],
            "sidecar_validation_status": "pass",
        })
        remote_metadata = sidecar_result["remote_metadata"]
        receipt = sidecar_result["receipt"]
        if (
            remote_metadata.get("capture_id") != retained.get("remote_capture_id")
            or remote_metadata.get("request_id") != retained.get("remote_request_id")
        ):
            raise RuntimeError("capture adapter sidecar IDs differ from physical return ledger")
        receipt_timing = receipt.get("timing_evidence")
        if not isinstance(receipt_timing, Mapping) or capture.get("timing_evidence") != receipt_timing:
            raise RuntimeError("capture adapter timing evidence differs from retained sidecar")
        estimate = remote_metadata.get("exposure_start_estimate")
        method = estimate.get("method") if isinstance(estimate, Mapping) else None
        if receipt_timing.get("tier") in thermal.ACCEPTED_TIMING_TIERS and method not in {
            "gphoto_event_minus_recorded_exposure",
            "gphoto_capture_return_minus_recorded_exposure",
        }:
            raise RuntimeError("capture adapter timing estimate lacks a recognized method")

        timing = capture.get("timing_evidence")
        if not isinstance(timing, Mapping):
            raise RuntimeError("capture lacks remote v2 timing evidence")
        if timing.get("provenance") != thermal.TIMING_CONTRACT_V2["provenance"]:
            raise RuntimeError("capture has unsupported timing provenance")
        observed = timing.get("best_effort_elapsed_s") if step["formal_measurement"] else None
        if step["formal_measurement"] and (
            timing.get("tier") not in thermal.ACCEPTED_TIMING_TIERS
            or timing.get("status") != "accepted_best_effort_anchor"
            or isinstance(observed, bool)
            or not isinstance(observed, (int, float))
            or not math.isfinite(float(observed))
            or float(observed) < 0
        ):
            rejected_capture["timing_evidence"] = dict(timing)
            raise RuntimeError(f"formal capture lacks accepted Tier A/B timing: {step['capture_id']}")
        nominal = step.get("requested_elapsed_s")
        offset = None if nominal is None or observed is None else float(observed) - float(nominal)
        if step["formal_measurement"]:
            previous_observed = last_observed_by_group.get(chronology_group_index)
            if previous_observed is not None and float(observed) <= previous_observed:
                rejected_capture["timing_evidence"] = dict(timing)
                raise RuntimeError(f"non-increasing observed chronology for {step['capture_id']}")
            last_observed_by_group[chronology_group_index] = float(observed)
        record = {
            "capture_id": step["capture_id"], "source_id": step["source_id"],
            "state_id": step["state_id"], "capture_role": step["capture_role"],
            "formal_measurement": bool(step["formal_measurement"]), "plan_step": dict(step),
            "nominal_slot_s": nominal,
            "best_effort_exposure_start_elapsed_s": observed,
            "timing_offset_s": offset,
            "timing_evidence_status": "accepted" if step["formal_measurement"] else "diagnostic_not_timed",
            "timing_estimate_method": method if step["formal_measurement"] else None,
            "capture": dict(capture),
            "timing_evidence": dict(timing),
        }
        if step["capture_role"] == "ambient" and not isinstance(capture.get("ambient_diagnostic"), Mapping):
            raise RuntimeError("ambient capture lacks ambient_diagnostic payload")
        covariate = dict(capture.get("thermal_covariates", {}))
        if not covariate:
            raise RuntimeError("capture adapter must retain complete thermal covariates")
        covariate["previous_state_id"] = previous_state
        covariate["previous_state_dwell_s"] = previous_dwell
        expected_command = step["command"] or {"strip": "off", "ray": "off"}
        thermal.validate_covariate_record(covariate, expected_command=expected_command)
        _append_jsonl(root / "captures.jsonl", record)
        _append_jsonl(root / "thermal-covariates.jsonl", covariate)
        if step["formal_measurement"]:
            run["completed_formal"] += 1
            run["accepted_formal_count"] += 1
        elif step["capture_role"] == "ambient":
            run["ambient_capture_count"] += 1
            run["accepted_ambient_count"] += 1
        else:
            run["diagnostic_capture_count"] += 1
            run["accepted_diagnostic_count"] += 1
        rejected_capture = None
        _write_json(root / "run.json", run)

    try:
        record_gate("run_start")
        if direct_guide6_strip_exposure:
            feature_ids = tuple(
                json.loads(thermal.POLICY_PATH.read_text(encoding="utf-8"))["feature_set"]["ids"]
            )
            chronology_index = 0
            started = False

            def strip_exposure_apply_and_wait(step: Mapping[str, Any], *, dwell_s: float) -> None:
                applied = dict(apply_command_fn(step))
                readback = dict(readback_fn(step))
                _append_jsonl(root / "commands.jsonl", {
                    "at": _utc_now(),
                    "event": "guide6_strip_exposure_command_readback_verified",
                    "source_id": "strip", "state_id": step["state_id"],
                    "exact_command_hash": step["exact_command_hash"],
                    "dwell_s": dwell_s, "applied": applied, "readback": readback,
                })
                if dwell_s:
                    sleep_fn(dwell_s)

            def strip_exposure_measure(step: Mapping[str, Any]) -> Mapping[str, Any]:
                nonlocal chronology_index, previous_state, previous_dwell, started
                record_source_isolation_gate(
                    f"guide6-strip-exposure-before-{chronology_index:02d}"
                )
                if not started:
                    record_gate("guide6-strip-exposure-reset600")
                    sleep_fn(float(plan["cold_proxy_wait_s"]))
                    for index, precondition in enumerate(step["warm_precondition_sequence"], 1):
                        strip_exposure_apply_and_wait(
                            {**dict(step),
                             "capture_id": f"guide6-strip-exposure-pre-{index}",
                             **dict(precondition)},
                            dwell_s=float(precondition["dwell_s"]),
                        )
                    started = True
                owner_start = monotonic_fn()
                if set_capture_context_fn is not None:
                    set_capture_context_fn(owner_start)
                ensure_physical_capacity()
                captured = dict(capture_fn(step))
                retain_capture(
                    step, captured, owner_start=owner_start,
                    chronology_group_index=chronology_index,
                )
                chronology_index += 1
                previous_state = str(step["state_id"])
                previous_dwell = monotonic_fn() - owner_start
                return captured

            from camera_based_rgbww_optimizer.optimization import analyze_p7_thermal_diagnostics as exposure_analyze
            protocol_evidence = run_guide6_strip_exposure_qualification_protocol(
                plan, measure_fn=strip_exposure_measure, feature_ids=feature_ids,
                pair_evaluator_fn=exposure_analyze.evaluate_guide8_pair_captures,
            )
            _write_json(root / "guide6-strip-exposure-qualification.json", protocol_evidence)
            runtime_plan = copy.deepcopy(dict(plan))
            runtime_plan["captures"] = [dict(item["step"]) for item in protocol_evidence["measured"]]
            runtime_plan["capture_ids"] = [str(step["capture_id"]) for step in runtime_plan["captures"]]
            _write_json(root / "adaptive-execution-plan.json", runtime_plan)
        elif direct_guide8_emission_exposure:
            feature_ids = tuple(
                json.loads(thermal.POLICY_PATH.read_text(encoding="utf-8"))["feature_set"]["ids"]
            )
            chronology_index = 0
            guide8_started = {"control": False, "dark": False, "ladder": False}

            def guide8_apply_and_wait(step: Mapping[str, Any], *, dwell_s: float) -> None:
                applied = dict(apply_command_fn(step))
                readback = dict(readback_fn(step))
                _append_jsonl(root / "commands.jsonl", {
                    "at": _utc_now(), "event": "guide8_command_readback_verified",
                    "source_id": step["source_id"], "state_id": step["state_id"],
                    "exact_command_hash": step["exact_command_hash"],
                    "dwell_s": dwell_s, "applied": applied, "readback": readback,
                })
                if dwell_s:
                    sleep_fn(dwell_s)

            def guide8_measure(step: Mapping[str, Any]) -> Mapping[str, Any]:
                nonlocal chronology_index, previous_state, previous_dwell
                phase = str(step["diagnostic_phase"])
                if phase == "control" and not guide8_started["control"]:
                    record_gate("guide8-control-reset600")
                    sleep_fn(600.0)
                    for index, precondition in enumerate(step["warm_precondition_sequence"], 1):
                        guide8_apply_and_wait({**dict(step), "capture_id": f"guide8-control-pre-{index}", **dict(precondition)}, dwell_s=float(precondition["dwell_s"]))
                    guide8_apply_and_wait(step, dwell_s=120.0)
                    guide8_started["control"] = True
                elif phase == "dark" and not guide8_started["dark"]:
                    record_gate("guide8-dark-reset600")
                    sleep_fn(600.0)
                    guide8_started["dark"] = True
                elif phase == "ladder" and not guide8_started["ladder"]:
                    for index, precondition in enumerate(step["warm_precondition_sequence"], 1):
                        guide8_apply_and_wait({**dict(step), "capture_id": f"guide8-ladder-pre-{index}", **dict(precondition)}, dwell_s=float(precondition["dwell_s"]))
                    guide8_started["ladder"] = True
                owner_start = monotonic_fn()
                if set_capture_context_fn is not None:
                    set_capture_context_fn(owner_start)
                ensure_physical_capacity()
                captured = dict(capture_fn(step))
                retain_capture(step, captured, owner_start=owner_start, chronology_group_index=chronology_index)
                chronology_index += 1
                previous_state = str(step["state_id"])
                previous_dwell = monotonic_fn() - owner_start
                return captured

            from camera_based_rgbww_optimizer.optimization import analyze_p7_thermal_diagnostics as guide8_analyze
            protocol_evidence = run_guide8_emission_exposure_protocol(
                plan, measure_fn=guide8_measure, feature_ids=feature_ids,
                pair_evaluator_fn=guide8_analyze.evaluate_guide8_pair_captures,
            )
            _write_json(root / "guide8-emission-exposure.json", protocol_evidence)
            runtime_plan = copy.deepcopy(dict(plan))
            runtime_plan["captures"] = [dict(item["step"]) for item in protocol_evidence["measured"]]
            runtime_plan["capture_ids"] = [str(step["capture_id"]) for step in runtime_plan["captures"]]
            _write_json(root / "adaptive-execution-plan.json", runtime_plan)
        elif direct_f2_short:
            feature_ids = tuple(json.loads(thermal.POLICY_PATH.read_text())["feature_set"]["ids"])
            rows = []
            commands = thermal.load_r1_commands()
            for step in plan["captures"]:
                source = str(step["source_id"])
                if source == "ray" or step["role"] in {"base_1", "candidate_2", "candidate_3"}:
                    sleep_fn(600.0)
                for state, command in (("D", thermal._command(source, "D", commands)), ("A", thermal._command(source, "A", commands)), ("tested", step["command"])):
                    pre = {**dict(step), "capture_id": f"pre-{state}-{step['capture_id']}", "state_id": state, "command": command, "exact_command_hash": thermal.canonical_sha256(command)}
                    apply_command_fn(pre); readback_fn(pre); sleep_fn(120.0)
                owner_start = monotonic_fn(); set_capture_context_fn(owner_start)
                captured = dict(capture_fn(step)); retain_capture(step, captured, owner_start=owner_start, chronology_group_index=len(rows)); rows.append({"step": dict(step), "capture": captured})
            _write_json(root / "short-endpoint-evidence.json", {"schema": "guide7_f2_short_endpoint_evidence_v1", "rows": rows, "capture_count": len(rows)})
            runtime_plan = copy.deepcopy(dict(plan)); runtime_plan["captures"] = [x["step"] for x in rows]; _write_json(root / "adaptive-execution-plan.json", runtime_plan)
        elif direct_guide6_target_local or direct_guide7_f2:
            feature_ids = tuple(
                json.loads(thermal.POLICY_PATH.read_text(encoding="utf-8"))
                ["feature_set"]["ids"]
            )
            commands = thermal.load_r1_commands()
            chronology_index = 0

            def guide6_source_isolation(source: str) -> Mapping[str, Any]:
                record_source_isolation_gate(
                    f"guide6-before-{run['completed_formal']:02d}-{source}"
                )
                return {"status": "pass", "source_verified_zero": True}

            def guide6_measure(step: Mapping[str, Any]) -> Mapping[str, Any]:
                nonlocal chronology_index, previous_state, previous_dwell
                role = str(step["role"])
                if role in {
                    "ray_q_before", "strip_base", "ray_q_after",
                }:
                    sleep_fn(float(plan["cold_proxy_wait_s"]))
                source = str(step["source_id"])
                for precondition_index, state in enumerate(("D", "A"), start=1):
                    command = thermal._command(source, state, commands)
                    precondition_step = {
                        **dict(step),
                        "capture_id": f"precondition-{precondition_index}-{step['capture_id']}",
                        "state_id": state,
                        "command": command,
                        "exact_command_hash": thermal.canonical_sha256(command),
                    }
                    applied = dict(apply_command_fn(precondition_step))
                    readback = dict(readback_fn(precondition_step))
                    _append_jsonl(root / "commands.jsonl", {
                        "at": _utc_now(),
                        "event": "guide6_precondition_command_readback_verified",
                        "source_id": source, "state_id": state,
                        "capture": False, "dwell_s": 120,
                        "exact_command_hash": precondition_step["exact_command_hash"],
                        "applied": applied, "readback": readback,
                    })
                    sleep_fn(120.0)
                applied = dict(apply_command_fn(step))
                readback = dict(readback_fn(step))
                _append_jsonl(root / "commands.jsonl", {
                    "at": _utc_now(), "event": "guide6_tested_command_readback_verified",
                    "source_id": source, "state_id": step["state_id"],
                    "exact_command_hash": step["exact_command_hash"],
                    "applied": applied, "readback": readback,
                })
                owner_start = monotonic_fn()
                if set_capture_context_fn is not None:
                    set_capture_context_fn(owner_start)
                sleep_fn(float(step["requested_elapsed_s"]))
                ensure_physical_capacity()
                captured = dict(capture_fn(step))
                retain_capture(
                    step, captured, owner_start=owner_start,
                    chronology_group_index=chronology_index,
                )
                chronology_index += 1
                previous_state = str(step["state_id"])
                previous_dwell = monotonic_fn() - owner_start
                return captured

            protocol_evidence = run_guide6_local_controllability_protocol(
                plan,
                measure_fn=guide6_measure,
                feature_ids=feature_ids,
                source_isolation_fn=guide6_source_isolation,
            )
            _write_json(root / "local-controllability.json", protocol_evidence)
            expected_formal_count = int(protocol_evidence["counts"]["total"])
            runtime_plan = copy.deepcopy(dict(plan))
            runtime_plan["captures"] = protocol_evidence["measured_steps"]
            runtime_plan["capture_ids"] = [
                str(step["capture_id"]) for step in protocol_evidence["measured_steps"]
            ]
            runtime_plan["budgets"] = {
                **dict(plan["budgets"]), "formal_cap": expected_formal_count,
            }
            _write_json(root / "adaptive-execution-plan.json", runtime_plan)
        else:
            runtime_plan = plan
        for chronology_group_index, item in ([] if (
            direct_guide6_target_local or direct_guide7_f2 or direct_f2_short or direct_guide8_emission_exposure
            or direct_guide6_strip_exposure
        ) else enumerate(
            _ledger_groups(str(plan["experiment_id"]), plan["captures"])
        )):
            if len(item) == 1 and item[0]["capture_role"] == "ambient":
                step = item[0]
                record_gate(str(step["isolation_gate_before"]))
                if set_capture_context_fn is not None:
                    set_capture_context_fn(monotonic_fn())
                ensure_physical_capacity()
                retain_capture(
                    step,
                    dict(capture_fn(step)),
                    owner_start=None,
                    chronology_group_index=chronology_group_index,
                )
                continue
            first = item[0]
            if plan["stage"] == "TD-A":
                sleep_fn(float(plan["cold_proxy_wait_s"]))
            warm_precondition = first.get("warm_precondition")
            warm_precondition_sequence = first.get("warm_precondition_sequence")
            if isinstance(warm_precondition, Mapping):
                preconditions = [warm_precondition]
            elif isinstance(warm_precondition_sequence, list) and warm_precondition_sequence:
                preconditions = warm_precondition_sequence
            else:
                preconditions = []
            if preconditions:
                record_gate(str(first["isolation_gate_before"]))
                sleep_fn(float(plan["cold_proxy_wait_s"]))
                for precondition_index, precondition in enumerate(preconditions, start=1):
                    precondition_step = {
                        **dict(first),
                        "capture_id": (
                            f"precondition-{precondition_index}-{first['capture_id']}"
                        ),
                        "state_id": str(precondition["state_id"]),
                        "command": dict(precondition["command"]),
                        "exact_command_hash": str(precondition["exact_command_hash"]),
                    }
                    precondition_applied = dict(apply_command_fn(precondition_step))
                    precondition_readback = dict(readback_fn(precondition_step))
                    _append_jsonl(root / "commands.jsonl", {
                        "at": _utc_now(),
                        "event": "warm_precondition_command_readback_verified",
                        "precondition_index": precondition_index,
                        "source_id": precondition_step["source_id"],
                        "state_id": precondition_step["state_id"],
                        "exact_command_hash": precondition_step["exact_command_hash"],
                        "dwell_s": precondition["dwell_s"],
                        "capture": False,
                        "applied": precondition_applied,
                        "readback": precondition_readback,
                    })
                    sleep_fn(float(precondition["dwell_s"]))
            applied = dict(apply_command_fn(first))
            readback = dict(readback_fn(first))
            _append_jsonl(root / "commands.jsonl", {
                "at": _utc_now(), "event": "command_readback_verified",
                "source_id": first["source_id"], "state_id": first["state_id"],
                "exact_command_hash": first["exact_command_hash"],
                "applied": applied, "readback": readback,
            })
            owner_start = monotonic_fn()
            if set_capture_context_fn is not None:
                set_capture_context_fn(owner_start)
            for step in item:
                remaining = owner_start + float(step["requested_elapsed_s"]) - monotonic_fn()
                if remaining > 0:
                    sleep_fn(remaining)
                ensure_physical_capacity()
                retain_capture(
                    step,
                    dict(capture_fn(step)),
                    owner_start=owner_start,
                    chronology_group_index=chronology_group_index,
                )
            previous_state = str(first["state_id"])
            previous_dwell = monotonic_fn() - owner_start
            gate_after = item[-1].get("isolation_gate_after")
            if gate_after:
                if direct_ray_continuous or direct_strip_history:
                    record_source_isolation_gate(str(gate_after))
                else:
                    record_gate(str(gate_after))
        if run["completed_formal"] != expected_formal_count:
            raise RuntimeError("thermal diagnostic formal count differs from frozen cap")
        if run["ambient_capture_count"] != int(plan["budgets"]["ambient_cap"]):
            raise RuntimeError("thermal diagnostic ambient count differs from frozen cap")
        if run["diagnostic_capture_count"] > int(plan["budgets"].get("diagnostic_cap", 0)):
            raise RuntimeError("thermal diagnostic count exceeds frozen cap")
        if (
            run["accepted_formal_count"] != run["completed_formal"]
            or run["accepted_ambient_count"] != run["ambient_capture_count"]
            or run["accepted_diagnostic_count"] != run["diagnostic_capture_count"]
        ):
            raise RuntimeError("thermal diagnostic accepted measurement ledger drifted")
        if direct_execution:
            assert post_capture_validator_fn is not None
            post_capture_validator_fn(root, runtime_plan, capture_settings_provenance)
        _write_json(root / "commands-audit.json", {
            "status": "pass", "formal_capture_count": run["completed_formal"],
            "ambient_capture_count": run["ambient_capture_count"],
        })
        run["status"] = "complete"
    except BaseException as exc:
        failure = exc
        run["status"] = "failed"
        failure_payload = {"type": type(exc).__name__, "message": str(exc), "at": _utc_now()}
        if rejected_capture is not None:
            failure_payload["rejected_capture"] = {**rejected_capture, "current_physical_cr3_count": run["physical_cr3_count"]}
        _write_json(root / "failure.json", failure_payload)
    finally:
        try:
            cleanup = dict(cleanup_fn())
        except BaseException as exc:
            cleanup = {"status": "fail", "type": type(exc).__name__, "message": str(exc)}
            if failure is None:
                failure = exc
                run["status"] = "failed"
                _write_json(root / "failure.json", {"type": type(exc).__name__, "message": str(exc), "at": _utc_now()})
        _write_json(root / "all-off-python.json", cleanup)
        cleanup_pass = bool(
            cleanup.get("status") in {"pass", "complete", "all_off"}
            or cleanup.get("ok")
        )
        run["cleanup"] = "pass" if cleanup_pass else "fail"
        if direct_execution and not cleanup_pass and failure is None:
            failure = RuntimeError("direct thermal Python cleanup did not pass")
            run["status"] = "failed"
            _write_json(root / "failure.json", {
                "type": type(failure).__name__,
                "message": str(failure),
                "at": _utc_now(),
            })
        elif failure is None:
            run["status"] = "complete"
        run["finished_at"] = _utc_now()
        _write_json(root / "run.json", run)
    if failure is not None:
        raise failure
    return root


def validate_direct_ray_r6_post_capture(
    run_root: str | Path,
    plan: Mapping[str, Any],
    runtime_evidence: Mapping[str, Any] | None,
) -> dict[str, Any]:
    """Validate the direct runner's own ledgers before analysis.

    This validator only reads the current run, its direct spec and scientific
    input policy.
    """
    root = Path(run_root).resolve()
    expected = thermal.build_ray_r6_spec()
    if plan.get("capture_ids") != expected["capture_ids"] or plan.get("frozen_shutters") != expected["frozen_shutters"]:
        raise ValueError("direct Ray R6 specification drifted before quality validation")
    def load_jsonl(path: Path) -> list[dict[str, Any]]:
        return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]

    captures = load_jsonl(root / "captures.jsonl")
    physical = load_jsonl(root / "physical-returns.jsonl")
    if [row.get("capture_id") for row in captures] != expected["capture_ids"]:
        raise ValueError("direct Ray R6 accepted capture order differs from spec")
    if [row.get("capture_id") for row in physical] != expected["capture_ids"]:
        raise ValueError("direct Ray R6 physical return order differs from spec")
    if len(captures) != 16 or len(physical) != 16:
        raise ValueError("direct Ray R6 requires exactly 16 physical and accepted captures")
    feature_ids = tuple(json.loads(thermal.POLICY_PATH.read_text(encoding="utf-8"))["feature_set"]["ids"])
    from camera_based_rgbww_optimizer.measurement.recorded_exposure import (
        validate_recorded_exposure_setting,
    )

    quality_rows: list[dict[str, Any]] = []
    physical_by_id = {str(row["capture_id"]): row for row in physical}
    for row in captures:
        step = row.get("plan_step")
        capture = row.get("capture")
        if not isinstance(step, Mapping) or not isinstance(capture, Mapping):
            raise ValueError("direct Ray R6 capture row lacks plan/capture owner")
        if str(row.get("run_root", str(root))) != str(root):
            raise ValueError("direct Ray R6 capture crosses run roots")
        values = capture.get("feature_values")
        if not isinstance(values, Mapping) or tuple(values) != feature_ids:
            raise ValueError("direct Ray R6 capture lacks the frozen feature vector")
        if any(not isinstance(value, (int, float)) or not math.isfinite(float(value)) for value in values.values()):
            raise ValueError("direct Ray R6 capture contains non-finite feature values")
        direct_quality = capture.get("direct_quality")
        if (
            not isinstance(direct_quality, Mapping)
            or direct_quality.get("status") != "pass"
            or direct_quality.get("feature_count") != len(feature_ids)
        ):
            raise ValueError("direct Ray R6 capture lacks accepted RAW feature quality")
        recorded = capture.get("recorded_exposure")
        if not isinstance(recorded, Mapping):
            raise ValueError("direct Ray R6 capture lacks recorded Canon exposure evidence")
        strip_zero = capture.get("strip_zero_before_capture")
        requested_zero = strip_zero.get("requested_payload") if isinstance(strip_zero, Mapping) else None
        observed_zero = strip_zero.get("device_snapshot") if isinstance(strip_zero, Mapping) else None
        if (
            not isinstance(requested_zero, Mapping)
            or any(int(value) != 0 for value in requested_zero.values())
            or not isinstance(observed_zero, Mapping)
            or any(int(observed_zero.get(key, -1)) != 0 for key in esphome.PAYLOAD_CHANNELS)
        ):
            raise ValueError("direct Ray R6 capture lacks verified strip-zero evidence")
        validate_recorded_exposure_setting(recorded, str(step["nominal_shutter"]))
        physical_row = physical_by_id.get(str(row["capture_id"]))
        if physical_row is None or physical_row.get("cr3_byte_count", 0) <= 0 or not physical_row.get("cr3_sha256"):
            raise ValueError("direct Ray R6 physical CR3 evidence is incomplete")
        quality_rows.append({"capture_id": str(row["capture_id"]), "status": "pass", "feature_count": len(feature_ids)})
    quality = {
        "schema": "p7_direct_ray_r6_quality_v1",
        "status": "pass",
        "experiment_id": thermal.TD_B,
        "capture_count": len(quality_rows),
        "rows": quality_rows,
    }
    quality_path = root / "quality.json"
    if quality_path.exists():
        retained_quality = json.loads(quality_path.read_text(encoding="utf-8"))
        if retained_quality != quality:
            raise ValueError("retained direct Ray R6 quality artifact differs from revalidation")
    else:
        _write_json(quality_path, quality)
    return quality


def validate_direct_guide8_post_capture(
    run_root: str | Path,
    plan: Mapping[str, Any],
    runtime_evidence: Mapping[str, Any] | None,
) -> dict[str, Any]:
    root = Path(run_root).resolve()
    canonical = thermal.build_direct_plan(
        thermal.TD_C, variant=thermal.GUIDE8_RAY_EMISSION_EXPOSURE_VARIANT,
    )
    captures = _load_jsonl_file(root / "captures.jsonl")
    physical = _load_jsonl_file(root / "physical-returns.jsonl")
    expected_prefix = canonical["capture_ids"][:len(captures)]
    capture_ids = [str(row.get("capture_id")) for row in captures]
    if capture_ids != expected_prefix or [str(row.get("capture_id")) for row in physical] != expected_prefix:
        raise ValueError("GUIDE8 early-stop capture/physical ledger is not a canonical prefix")
    if not 1 <= len(captures) <= 16 or len(physical) != len(captures):
        raise ValueError("GUIDE8 physical evidence violates its 1..16 bounded prefix")
    for row, expected_step in zip(captures, canonical["captures"]):
        if row.get("plan_step") != expected_step:
            raise ValueError("GUIDE8 retained plan step differs from its canonical owner")
        capture = row.get("capture")
        if not isinstance(capture, Mapping):
            raise ValueError("GUIDE8 capture evidence is missing")
        strip_zero = capture.get("strip_zero_before_capture")
        requested = strip_zero.get("requested_payload") if isinstance(strip_zero, Mapping) else None
        observed = strip_zero.get("device_snapshot") if isinstance(strip_zero, Mapping) else None
        if (
            not isinstance(requested, Mapping)
            or any(int(value) != 0 for value in requested.values())
            or not isinstance(observed, Mapping)
            or any(int(observed.get(key, -1)) != 0 for key in esphome.PAYLOAD_CHANNELS)
        ):
            raise ValueError("GUIDE8 capture lacks verified strip-zero evidence")
    evidence = _load_json_file(root / "guide8-emission-exposure.json")
    if int(evidence.get("physical_capture_count", -1)) != len(captures):
        raise ValueError("GUIDE8 adaptive evidence count differs from physical ledger")
    if len(captures) == 1 and evidence.get("branch") != "E-A":
        raise ValueError("GUIDE8 one-frame prefix is valid only for E-A control failure")
    quality = {
        "schema": "guide8_ray_emission_exposure_quality_v1",
        "status": "pass", "capture_count": len(captures),
        "branch": evidence.get("branch"), "formal_capture_count": 0,
    }
    _write_json(root / "quality.json", quality)
    return quality


def validate_direct_guide6_strip_exposure_post_capture(
    run_root: str | Path,
    plan: Mapping[str, Any],
    runtime_evidence: Mapping[str, Any] | None,
) -> dict[str, Any]:
    """Validate a canonical early-stop prefix and capture-level Ray-zero evidence."""
    root = Path(run_root).resolve()
    canonical = thermal.build_direct_plan(
        thermal.TD_C,
        variant=thermal.GUIDE6_STRIP_EXPOSURE_QUALIFICATION_VARIANT,
    )
    captures = _load_jsonl_file(root / "captures.jsonl")
    physical = _load_jsonl_file(root / "physical-returns.jsonl")
    expected_prefix = canonical["capture_ids"][:len(captures)]
    if (
        [str(row.get("capture_id")) for row in captures] != expected_prefix
        or [str(row.get("capture_id")) for row in physical] != expected_prefix
        or not 1 <= len(captures) <= len(canonical["captures"])
    ):
        raise ValueError("GUIDE6 strip exposure evidence is not a canonical prefix")
    for row, expected_step in zip(captures, canonical["captures"]):
        if row.get("plan_step") != expected_step:
            raise ValueError("GUIDE6 strip exposure plan step drifted")
        capture = row.get("capture")
        ray_zero = capture.get("ray_zero_before_capture") if isinstance(capture, Mapping) else None
        ray_data = (
            ray_zero.get("data")
            or ((ray_zero.get("response") or {}).get("data"))
            if isinstance(ray_zero, Mapping) else None
        )
        if not isinstance(ray_data, Mapping) or int(ray_data.get("intensity", -1)) != 0:
            raise ValueError("GUIDE6 strip exposure capture lacks verified Ray-zero evidence")
    evidence = _load_json_file(root / "guide6-strip-exposure-qualification.json")
    if (
        evidence.get("schema") != "guide6_strip_exposure_qualification_evidence_v1"
        or int(evidence.get("physical_capture_count", -1)) != len(captures)
        or int(evidence.get("formal_capture_count", -1)) != 0
        or int(evidence.get("solver_probe_count", -1)) != 0
    ):
        raise ValueError("GUIDE6 strip exposure evidence contract differs")
    quality = {
        "schema": "guide6_strip_exposure_qualification_quality_v1",
        "status": "pass",
        "capture_count": len(captures),
        "formal_capture_count": 0,
        "classification": evidence.get("classification"),
    }
    _write_json(root / "quality.json", quality)
    return quality


def _load_jsonl_file(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def _load_json_file(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value


def validate_direct_ray_history_session_post_capture(
    run_root: str | Path,
    plan: Mapping[str, Any],
    runtime_evidence: Mapping[str, Any] | None,
) -> dict[str, Any]:
    """Validate one exact seven-frame order-balanced session."""
    root = Path(run_root).resolve()
    session_index = plan.get("session_index")
    if type(session_index) is not int:
        raise ValueError("Ray history session lacks an integer session index")
    expected = thermal.build_ray_history_session_spec(
        session_index, device_control_enabled=True,
        session_start_condition=plan.get("session_start_condition"),
    )
    immutable_fields = (
        "guide_experiment_id", "session_order", "capture_ids", "frozen_shutters",
        "budgets", "analysis_contract",
    )
    if any(plan.get(key) != expected.get(key) for key in immutable_fields):
        raise ValueError("direct Ray history session specification drifted")
    quality = validate_direct_protocol_post_capture(root, plan, runtime_evidence)
    captures = [
        json.loads(line)
        for line in (root / "captures.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    if len(captures) != 7:
        raise ValueError("direct Ray history session requires exactly seven captures")
    return_anchors = [
        row for row in captures
        if (row.get("plan_step") or {}).get("role") == "return_anchor"
    ]
    if [
        (row["plan_step"].get("sequence_position"), row["plan_step"].get("immediate_predecessor_state"))
        for row in return_anchors
    ] != list(enumerate(expected["session_order"], start=1)):
        raise ValueError("direct Ray history return anchors differ from the balanced design")
    quality = {
        **quality,
        "schema": "guide4_ray_history_session_quality_v1",
        "guide_experiment_id": thermal.RAY_HISTORY_3X3_EXPERIMENT_ID,
        "session_index": session_index,
        "session_order": expected["session_order"],
    }
    _write_json(root / "quality.json", quality)
    return quality


def validate_direct_strip_history_session_post_capture(
    run_root: str | Path,
    plan: Mapping[str, Any],
    runtime_evidence: Mapping[str, Any] | None,
) -> dict[str, Any]:
    """Validate one exact GUIDE5 strip-only seven-capture session."""
    root = Path(run_root).resolve()
    session_index = plan.get("session_index")
    if type(session_index) is not int:
        raise ValueError("strip history session lacks an integer session index")
    expected = thermal.build_strip_history_session_spec(
        session_index, device_control_enabled=True,
        session_start_condition=plan.get("session_start_condition"),
    )
    immutable_fields = (
        "guide_experiment_id", "session_order", "capture_ids", "frozen_shutters",
        "budgets", "analysis_contract", "execution_authorization",
    )
    if any(plan.get(key) != expected.get(key) for key in immutable_fields):
        raise ValueError("direct strip history session specification drifted")
    quality = validate_direct_protocol_post_capture(root, plan, runtime_evidence)
    captures = [
        json.loads(line) for line in (root / "captures.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    if len(captures) != 7:
        raise ValueError("direct strip history session requires exactly seven captures")
    returns = [row for row in captures if (row.get("plan_step") or {}).get("role") == "return_anchor"]
    if [
        (row["plan_step"].get("sequence_position"), row["plan_step"].get("immediate_predecessor_state"))
        for row in returns
    ] != list(enumerate(expected["session_order"], start=1)):
        raise ValueError("direct strip history return anchors differ from the balanced design")
    for row in captures:
        evidence = (row.get("capture") or {}).get("ray_zero_before_capture")
        if not isinstance(evidence, Mapping):
            raise ValueError("strip history capture lacks Ray-zero evidence")
    quality = {
        **quality,
        "schema": "guide5_strip_history_session_quality_v1",
        "guide_experiment_id": thermal.STRIP_HISTORY_3X3_EXPERIMENT_ID,
        "session_index": session_index,
        "session_order": expected["session_order"],
    }
    _write_json(root / "quality.json", quality)
    return quality


def validate_direct_ray_fast_long_bridge_session_post_capture(
    run_root: str | Path,
    plan: Mapping[str, Any],
    runtime_evidence: Mapping[str, Any] | None,
) -> dict[str, Any]:
    """Validate one exact three-capture GUIDE5 fast/long bridge mini-session."""
    root = Path(run_root).resolve()
    mini_session_index = plan.get("mini_session_index")
    if type(mini_session_index) is not int:
        raise ValueError("Ray fast/long bridge lacks an integer mini-session index")
    prerequisite = plan.get("scientific_prerequisite")
    expected = thermal.build_ray_fast_long_bridge_session_spec(
        mini_session_index,
        device_control_enabled=True,
        session_start_condition=plan.get("session_start_condition"),
        scientific_prerequisite=(
            prerequisite if isinstance(prerequisite, Mapping) else None
        ),
    )
    immutable_fields = (
        "guide_experiment_id", "bridge_state", "bridge_protocol", "reset_s",
        "operational_dwell_s", "capture_ids", "frozen_shutters", "budgets",
        "analysis_contract", "execution_authorization", "scientific_prerequisite",
    )
    if any(plan.get(key) != expected.get(key) for key in immutable_fields):
        raise ValueError("direct Ray fast/long bridge specification drifted")
    quality = validate_direct_protocol_post_capture(root, plan, runtime_evidence)
    captures = [
        json.loads(line)
        for line in (root / "captures.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    if len(captures) != 3 or [
        (row.get("plan_step") or {}).get("role") for row in captures
    ] != ["initial_anchor", "bridge_state", "return_anchor"]:
        raise ValueError("direct Ray fast/long bridge requires exact A/Q/A captures")
    quality = {
        **quality,
        "schema": "guide5_ray_fast_long_bridge_session_quality_v1",
        "guide_experiment_id": thermal.RAY_FAST_LONG_BRIDGE_EXPERIMENT_ID,
        "mini_session_index": mini_session_index,
        "bridge_state": expected["bridge_state"],
        "bridge_protocol": expected["bridge_protocol"],
        "reset_s": expected["reset_s"],
        "operational_dwell_s": expected["operational_dwell_s"],
    }
    _write_json(root / "quality.json", quality)
    return quality


def validate_direct_protocol_post_capture(
    run_root: str | Path,
    plan: Mapping[str, Any],
    runtime_evidence: Mapping[str, Any] | None,
) -> dict[str, Any]:
    """Validate direct strip/TD-C output from the same real scheduler."""
    root = Path(run_root).resolve()
    expected_ids = [str(step["capture_id"]) for step in plan["captures"]]
    captures = [
        json.loads(line) for line in (root / "captures.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    physical = [
        json.loads(line) for line in (root / "physical-returns.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    if [str(row.get("capture_id")) for row in captures] != expected_ids:
        raise ValueError("direct protocol capture order differs from its spec")
    if [str(row.get("capture_id")) for row in physical] != expected_ids:
        raise ValueError("direct protocol physical order differs from its spec")
    formal_count = sum(bool(row.get("formal_measurement")) for row in captures)
    if formal_count != int(plan["budgets"]["formal_cap"]):
        raise ValueError("direct protocol formal count differs from its spec")
    physical_by_id = {str(row["capture_id"]): row for row in physical}
    rows = []
    for row in captures:
        capture = row.get("capture")
        step = row.get("plan_step")
        if not isinstance(capture, Mapping) or not isinstance(step, Mapping):
            raise ValueError("direct protocol capture lacks spec/capture artifacts")
        if str(row.get("run_root", str(root))) != str(root):
            raise ValueError("direct protocol artifact crossed its run root")
        values = capture.get("feature_values")
        if row.get("formal_measurement") and (
            not isinstance(values, Mapping)
            or any(
                not isinstance(value, (int, float)) or not math.isfinite(float(value))
                for value in values.values()
            )
        ):
            raise ValueError("direct protocol feature artifact is missing or non-finite")
        if row.get("formal_measurement"):
            direct_quality = capture.get("direct_quality")
            if (
                not isinstance(direct_quality, Mapping)
                or direct_quality.get("status") != "pass"
                or direct_quality.get("feature_count") != len(values)
            ):
                raise ValueError("direct protocol capture lacks accepted RAW feature quality")
        if row.get("source_id") == "ray":
            strip_zero = capture.get("strip_zero_before_capture")
            requested = strip_zero.get("requested_payload") if isinstance(strip_zero, Mapping) else None
            observed = strip_zero.get("device_snapshot") if isinstance(strip_zero, Mapping) else None
            if (
                not isinstance(requested, Mapping)
                or any(int(value) != 0 for value in requested.values())
                or not isinstance(observed, Mapping)
                or any(int(observed.get(key, -1)) != 0 for key in esphome.PAYLOAD_CHANNELS)
            ):
                raise ValueError("direct Ray capture lacks verified strip-zero evidence")
        elif (
            (plan.get("execution_authorization") or {}).get("schema")
            in {
                "direct_strip_history_session_v1",
                "direct_td_c_fast_endpoint_holdout_v1",
                "direct_guide6_target_local_h120_s100_v1",
                "direct_guide7_f2_alternate_face_v1",
                "direct_guide7_f2_short_endpoint_v1",
            }
        ):
            ray_zero = capture.get("ray_zero_before_capture")
            ray_data = (
                ray_zero.get("data")
                or ((ray_zero.get("response") or {}).get("data"))
                if isinstance(ray_zero, Mapping) else None
            )
            if not isinstance(ray_data, Mapping) or int(ray_data.get("intensity", -1)) != 0:
                raise ValueError("direct strip capture lacks Ray-zero evidence")
        physical_row = physical_by_id.get(str(row["capture_id"]))
        if physical_row is None or int(physical_row.get("cr3_byte_count", 0)) <= 0:
            raise ValueError("direct protocol physical CR3 artifact is missing")
        if row.get("formal_measurement"):
            rows.append({"capture_id": str(row["capture_id"]), "status": "pass"})
    quality = {
        "schema": "p7_direct_protocol_quality_v1",
        "status": "pass",
        "experiment_id": plan["experiment_id"],
        "capture_count": len(rows),
        "rows": rows,
    }
    _write_json(root / "quality.json", quality)
    return quality


def validate_scientific_prerequisite(path: str | Path, *, kind: str) -> dict[str, Any]:
    """Validate only a prior scientific result and its content hash."""
    target = Path(path).resolve()
    if target.is_symlink() or not target.is_file():
        raise ValueError("scientific prerequisite must be a regular file")
    value = json.loads(target.read_text(encoding="utf-8"))
    if not isinstance(value, Mapping):
        raise ValueError("scientific prerequisite must be a JSON object")
    if kind == "strip-td-b":
        valid = (
            value.get("experiment_id") == thermal.TD_B
            and value.get("formal_pass") is True
            and value.get("return_anchor_history_effect") == "pass"
        )
    elif kind == "td-c-core":
        valid = (
            value.get("schema") == "p7_combined_fast_history_coordinate_v1"
            and value.get("status") == "canonical_pass"
            and value.get("classification")
            == "fast_local_anchor_coordinate_compatible_for_paired_source_comparison"
            and value.get("experiment_id") == "combined_td_b"
            and value.get("long_input_count") == 0
            and value.get("gate") == {
                "evidence_identity": "pass", "no_pooling": "pass",
                "session": "pass", "position": "pass",
                "additive_residual": "pass",
            }
            and value.get("locks", {}).get("td_c_core") is False
            and value.get("locks", {}).get("td_c_expansion") is True
        )
    elif kind == "td-c-fast-endpoint-holdout":
        valid = (
            value.get("schema") == "guide5_td_c_core_contrasts_v2_1"
            and value.get("status") == "canonical_pass"
            and value.get("refined_status")
            == "stable_order_invariant_nonzero_warm_A_cross_source_offset_established"
            and value.get("locks", {}).get("fast_B_C_endpoint_holdout") is False
            and value.get("locks", {}).get("legacy_td_c_expansion") is True
            and value.get("locks", {}).get("solver_sentinel_and_later") is True
        )
    elif kind == "ray-fast-long-bridge":
        valid = (
            value.get("schema") == "guide5_strip_history_order_balanced_analysis_v3"
            and value.get("status") == "accepted_advisor_corrected_classification"
            and value.get("advisor_decision") == "OPTION_3_CORRECT_THE_COMMON_CONTRAST"
            and value.get("guide5_parent_branch") == "S-A"
            and value.get("classification")
            == "common_warm_reentry_shift_with_session_block_heterogeneity"
            and value.get("locks", {}).get("ray_fast_long_bridge") is False
            and value.get("locks", {}).get("combined_td_b") is True
        )
    else:
        raise ValueError(f"unknown scientific prerequisite kind: {kind}")
    if not valid:
        raise ValueError(f"{kind} prerequisite does not declare the required scientific pass")
    return {
        "path": str(target),
        "sha256": hashlib.sha256(target.read_bytes()).hexdigest(),
        "kind": kind,
        "status": "pass",
    }


def audit_post_return_failure(
    run_dir: str | Path,
    output_dir: str | Path,
    *,
    expected_cr3_sha256: str,
    expected_sidecar_sha256: str,
) -> Path:
    """Create a read-only audit of one failed post-return thermal capture."""
    root = Path(run_dir).resolve()
    output = Path(output_dir).resolve()
    if output.is_relative_to(root):
        raise ValueError("post-return audit output must be outside the failed run")
    if output.exists():
        raise FileExistsError(f"post-return audit output already exists: {output}")

    evidence_names = (
        "plan.json",
        "run.json",
        "failure.json",
        "physical-returns.jsonl",
        "all-off-python.json",
        "all-off-shell.json",
        "all-off-shell.exit-status.txt",
        "independent-final-zero.json",
    )
    evidence_paths = {name: root / name for name in evidence_names}
    if any(not path.is_file() or path.is_symlink() for path in evidence_paths.values()):
        raise ValueError("post-return audit lacks immutable run evidence")
    retained_paths = {
        str(path.relative_to(root)): path
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }
    if not retained_paths or any(path.is_symlink() for path in retained_paths.values()):
        raise ValueError("post-return audit retained file set is invalid")
    before = {
        name: hashlib.sha256(path.read_bytes()).hexdigest()
        for name, path in retained_paths.items()
    }

    plan = json.loads(evidence_paths["plan.json"].read_text(encoding="utf-8"))
    run = json.loads(evidence_paths["run.json"].read_text(encoding="utf-8"))
    failure = json.loads(evidence_paths["failure.json"].read_text(encoding="utf-8"))
    physical_rows = [
        json.loads(line)
        for line in evidence_paths["physical-returns.jsonl"]
        .read_text(encoding="utf-8")
        .splitlines()
        if line.strip()
    ]
    rejected = failure.get("rejected_capture")
    if (
        plan.get("experiment_id") != thermal.TD_B
        or plan.get("source") != "ray"
        or run.get("status") != "failed"
        or run.get("accepted_formal_count") != 0
        or run.get("completed_formal") != 0
        or run.get("physical_returned_cr3_count") != 1
        or run.get("physical_cr3_count")
        != run.get("setup_physical_cr3_count", 0) + 1
        or failure.get("type") != "HsiRejectedFeaturesError"
        or not isinstance(rejected, Mapping)
        or rejected.get("rejection_stage") != "post_return_processing"
        or len(physical_rows) != 1
    ):
        raise ValueError("post-return failed-run status or physical ledger differs")

    physical = physical_rows[0]
    raw_candidate = Path(str(physical.get("cr3_path")))
    raw = raw_candidate.resolve()
    sidecar = raw.with_suffix(raw.suffix + ".metadata.json")
    if (
        raw_candidate.is_symlink()
        or sidecar.is_symlink()
        or not raw.is_relative_to(root)
        or not sidecar.is_relative_to(root)
        or not raw.is_file()
        or raw.stat().st_size <= 0
        or not sidecar.is_file()
        or sidecar.stat().st_size <= 0
        or rejected.get("capture_id") != physical.get("capture_id")
        or Path(str(rejected.get("cr3_path"))).resolve() != raw
        or rejected.get("cr3_byte_count") != raw.stat().st_size
        or rejected.get("cr3_sha256") != expected_cr3_sha256
        or physical.get("cr3_byte_count") != raw.stat().st_size
        or physical.get("cr3_sha256") != expected_cr3_sha256
        or hashlib.sha256(raw.read_bytes()).hexdigest() != expected_cr3_sha256
        or hashlib.sha256(sidecar.read_bytes()).hexdigest()
        != expected_sidecar_sha256
    ):
        raise ValueError("post-return CR3/sidecar owner or hash differs")

    try:
        sidecar_payload = json.loads(sidecar.read_text(encoding="utf-8"))
        remote, receipt = camera_remote_v2.split_and_validate_sidecar(
            sidecar_payload,
            payload=raw.read_bytes(),
        )
    except (
        OSError,
        UnicodeError,
        json.JSONDecodeError,
        camera_remote_v2.RemoteCaptureV2Error,
    ) as exc:
        raise ValueError("post-return sidecar replay failed") from exc
    recorded = remote.get("recorded_exposure")
    timing = receipt.get("timing_evidence")
    if (
        remote.get("capture_id") != physical.get("remote_capture_id")
        or remote.get("request_id") != physical.get("remote_request_id")
        or not isinstance(recorded, Mapping)
        or recorded.get("status") != "recorded"
        or recorded.get("source") != "Canon:ExposureTime"
        or isinstance(recorded.get("seconds"), bool)
        or not isinstance(recorded.get("seconds"), (int, float))
        or float(recorded["seconds"]) <= 0
        or not isinstance(timing, Mapping)
        or timing.get("tier") != "tier_b"
        or timing.get("status") != "accepted_best_effort_anchor"
    ):
        raise ValueError("post-return capture/request/exposure/timing association differs")

    reports = list((root / "measurements").glob("*.patch-statistics.json"))
    if len(reports) != 1 or reports[0].is_symlink():
        raise ValueError("post-return audit requires one retained patch report")
    report = json.loads(reports[0].read_text(encoding="utf-8"))
    rejected_planes = []
    for patch in report.get("patches", []):
        for plane, plane_payload in (patch.get("planes") or {}).items():
            quality = plane_payload.get("quality") or {}
            if quality.get("status") == "rejected":
                rejected_planes.append({
                    "patch": patch.get("patch_id") or patch.get("name"),
                    "plane": plane,
                    "failures": list(quality.get("failures") or []),
                })
    if (
        report.get("quality", {}).get("status") != "rejected"
        or not rejected_planes
        or any(
            set(item["failures"]) != {"near_noise_floor_fraction_exceeded"}
            for item in rejected_planes
        )
    ):
        raise ValueError("post-return retained report is not the frozen low-signal rejection")

    python_cleanup = json.loads(
        evidence_paths["all-off-python.json"].read_text(encoding="utf-8")
    )
    shell_cleanup = json.loads(
        evidence_paths["all-off-shell.json"].read_text(encoding="utf-8")
    )
    final_zero = json.loads(
        evidence_paths["independent-final-zero.json"].read_text(encoding="utf-8")
    )
    zero_channels = {"cold_white", "warm_white", "red", "green", "blue"}
    strip_snapshot = (
        final_zero.get("strip_device_evidence", {}).get("device_snapshot", {})
    )
    if (
        python_cleanup.get("status") != "pass"
        or not python_cleanup.get("steps")
        or not all(step.get("ok") is True for step in python_cleanup["steps"])
        or not isinstance(shell_cleanup, list)
        or not shell_cleanup
        or not all(step.get("ok") is True for step in shell_cleanup)
        or evidence_paths["all-off-shell.exit-status.txt"]
        .read_text(encoding="utf-8")
        .strip()
        != "0"
        or final_zero.get("status") != "pass"
        or final_zero.get("ray_readback", {}).get("data", {}).get("intensity") != 0
        or any(strip_snapshot.get(channel) != 0 for channel in zero_channels)
        or list(root.rglob("*.npy"))
    ):
        raise ValueError("post-return cleanup, final-zero, or NPY evidence differs")

    retained_after = {
        str(path.relative_to(root)): path
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }
    after = {
        name: hashlib.sha256(path.read_bytes()).hexdigest()
        for name, path in retained_after.items()
    }
    if after != before:
        raise RuntimeError("post-return audit mutated the failed run")
    output.mkdir(parents=True, exist_ok=False)
    artifact = {
        "schema": "p7_td_b_post_return_failure_audit_v1",
        "status": "pass",
        "forensic_only": True,
        "accepted_formal": False,
        "reusable_capture": False,
        "failed_run": str(root),
        "immutable_input_file_count": len(before),
        "immutable_input_sha256": before,
        "physical": {
            "setup": run.get("setup_physical_cr3_count"),
            "returned": run.get("physical_returned_cr3_count"),
            "total": run.get("physical_cr3_count"),
            "accepted_formal": run.get("accepted_formal_count"),
        },
        "cr3": {
            "path": str(raw),
            "byte_count": raw.stat().st_size,
            "sha256": expected_cr3_sha256,
        },
        "sidecar": {
            "path": str(sidecar),
            "byte_count": sidecar.stat().st_size,
            "sha256": expected_sidecar_sha256,
        },
        "capture_id": remote["capture_id"],
        "request_id": remote["request_id"],
        "recorded_exposure": dict(recorded),
        "timing_evidence": dict(timing),
        "failure_type": failure["type"],
        "rejected_planes": rejected_planes,
        "cleanup": "pass",
        "independent_final_zero": "pass",
        "retained_npy_count": 0,
    }
    artifact_path = output / "post-return-failure-audit.json"
    _write_json(artifact_path, artifact)
    return artifact_path


def _ledger_groups(
    experiment_id: str, captures: Sequence[Mapping[str, Any]],
) -> list[list[Mapping[str, Any]]]:
    groups: list[list[Mapping[str, Any]]] = []
    for step in captures:
        if step["capture_role"] == "ambient":
            groups.append([step])
            continue
        key = thermal.timing_sequence_identity(experiment_id, step)
        previous = groups[-1][0] if groups and groups[-1][0]["capture_role"] == "formal" else None
        previous_key = (
            None if previous is None
            else thermal.timing_sequence_identity(experiment_id, previous)
        )
        if groups and previous is not None and key == previous_key and float(step["requested_elapsed_s"]) > float(groups[-1][-1]["requested_elapsed_s"]):
            groups[-1].append(step)
        else:
            groups.append([step])
    return groups


def run_authorized_plan(
    plan: Mapping[str, Any], *, output_dir: str | Path, run_name: str,
    camera_backend: Any,
) -> Path:
    validate_authorized_execution_plan(plan, camera_backend=camera_backend)
    from camera_based_rgbww_optimizer.control import all_off, esphome, ray120c
    from camera_based_rgbww_optimizer.optimization import measure_raw_observer_validation as raw_validation
    from camera_based_rgbww_optimizer.measurement.raw_observer_analysis import DEFAULT_STATISTIC
    from camera_based_rgbww_optimizer.optimization.hsi_objective import (
        HsiRejectedFeaturesError,
        TD_B_FORMAL_FEATURE_STATISTIC,
        required_hsi_features_from_report,
    )
    from camera_based_rgbww_optimizer.optimization.measure_ray_hsi_manifold import _verify_readback

    root = Path(output_dir) / run_name
    policy = json.loads(thermal.POLICY_PATH.read_text(encoding="utf-8"))
    feature_ids = tuple(policy["feature_set"]["ids"])
    curve = json.loads(thermal.CURVE_PATH.read_text(encoding="utf-8"))
    applied: dict[str, Mapping[str, Any]] = {}
    readbacks: dict[str, Mapping[str, Any]] = {}
    timing_context: dict[str, float | None] = {"local_readback_done_monotonic_s": None}
    timing_connection = camera_backend.connect()
    resolved_settings, settings_provenance = _resolve_remote_capture_settings(camera_backend)
    plan_steps_by_id = {
        str(step["capture_id"]): step for step in plan["captures"]
    }
    direct_ray_continuous = (
        isinstance(plan.get("execution_authorization"), Mapping)
        and plan["execution_authorization"].get("schema") in {
            "direct_ray_r6_authority_v1", "direct_ray_history_session_v1",
            "direct_ray_fast_long_bridge_session_v1",
        }
    )
    direct_strip_history = (
        isinstance(plan.get("execution_authorization"), Mapping)
        and plan["execution_authorization"].get("schema")
        == "direct_strip_history_session_v1"
    )
    direct_td_c_fast_endpoint = (
        isinstance(plan.get("execution_authorization"), Mapping)
        and plan["execution_authorization"].get("schema")
        == "direct_td_c_fast_endpoint_holdout_v1"
    )
    direct_guide6_target_local = (
        isinstance(plan.get("execution_authorization"), Mapping)
        and plan["execution_authorization"].get("schema")
        == "direct_guide6_target_local_h120_s100_v1"
    )
    direct_guide7_f2 = (
        isinstance(plan.get("execution_authorization"), Mapping)
        and plan["execution_authorization"].get("schema")
        == "direct_guide7_f2_alternate_face_v1"
    )
    direct_f2_short = (
        isinstance(plan.get("execution_authorization"), Mapping)
        and plan["execution_authorization"].get("schema")
        == "direct_guide7_f2_short_endpoint_v1"
    )
    direct_guide8_emission_exposure = (
        isinstance(plan.get("execution_authorization"), Mapping)
        and plan["execution_authorization"].get("schema")
        == "direct_guide8_ray_emission_exposure_v1"
    )
    direct_guide6_strip_exposure = (
        isinstance(plan.get("execution_authorization"), Mapping)
        and plan["execution_authorization"].get("schema")
        == "direct_guide6_strip_exposure_qualification_v1"
    )
    direct_protocol = (
        isinstance(plan.get("execution_authorization"), Mapping)
        and str(plan["execution_authorization"].get("schema", "")).startswith("direct_")
    )
    physical_return_observer_slot: dict[
        str,
        Callable[[Mapping[str, Any], Any, int], Mapping[str, Any]] | None,
    ] = {"callback": None}
    session_start = time.monotonic()
    load_segments: dict[str, list[tuple[float, float]]] = {"ray": [], "strip": []}
    thermal_context: dict[str, Any] = {
        "ray_started_monotonic_s": None,
        "ray_off_since_monotonic_s": None,
        "state_id": None,
        "state_started_monotonic_s": None,
        "previous_state_id": None,
        "previous_state_dwell_s": None,
    }

    def load_level(source: str, command: Mapping[str, Any]) -> float:
        if source == "strip":
            return float(sum(thermal.strip_duty(command, curve).values()))
        return float(command["intensity_percent"]) / 100.0

    def integrated_history(source: str, now: float, window: int) -> float:
        start = now - float(window)
        segments = load_segments[source]
        total = 0.0
        for index, (segment_start, level) in enumerate(segments):
            segment_end = segments[index + 1][0] if index + 1 < len(segments) else now
            total += level * max(0.0, min(now, segment_end) - max(start, segment_start))
        return total

    def apply(step: Mapping[str, Any]) -> Mapping[str, Any]:
        command = step["command"]
        applied_at = time.monotonic()
        if step["source_id"] == "ray":
            response = ray120c.set_hsi(
                int(command["hue"]), int(command["sat"]),
                intensity_percent=float(command["intensity_percent"]),
            )
        else:
            response = esphome.verified_light(
                *(int(command[channel]) for channel in thermal.CHANNELS),
                curve_path=thermal.CURVE_PATH,
            )
        if step["source_id"] == "ray":
            prior_state = thermal_context["state_id"]
            prior_started = thermal_context["state_started_monotonic_s"]
            thermal_context["previous_state_id"] = prior_state
            thermal_context["previous_state_dwell_s"] = (
                None if prior_started is None else max(0.0, applied_at - float(prior_started))
            )
            thermal_context["state_id"] = str(step["state_id"])
            thermal_context["state_started_monotonic_s"] = applied_at
            if thermal_context["ray_started_monotonic_s"] is None:
                thermal_context["ray_started_monotonic_s"] = applied_at
            else:
                thermal_context["ray_off_since_monotonic_s"] = None
        load_segments[str(step["source_id"])].append((applied_at, load_level(str(step["source_id"]), command)))
        applied[str(step["capture_id"])] = dict(response)
        return response

    def readback(step: Mapping[str, Any]) -> Mapping[str, Any]:
        if step["source_id"] == "ray":
            command = step["command"]
            value = ray120c.get_hsi()
            _verify_readback(value, {
                "hue": int(command["hue"]), "sat": int(command["sat"]),
                "intensity": ray120c.intensity_percent_to_raw(float(command["intensity_percent"])),
            }, mode="hsi")
        else:
            value = applied[str(step["capture_id"])]
        readbacks[f"{step['source_id']}:{step['state_id']}"] = dict(value)
        return value

    def timed_capture(**kwargs: Any) -> camera_gphoto2.CaptureResult:
        if timing_context["local_readback_done_monotonic_s"] is None:
            raise RuntimeError("P7 timing context is missing command/readback completion")
        method = getattr(camera_backend, "capture_with_timing", None)
        if not callable(method):
            raise PermissionError("remote camera adapter lacks capture_with_timing")
        return method(
            output_dir=kwargs["output_dir"], filename_template=kwargs["filename_template"],
            settings=kwargs["settings"], connection=timing_connection,
            local_readback_done_monotonic_s=float(timing_context["local_readback_done_monotonic_s"]),
        )

    ambient_policy_owner = (
        {
            "experiment_id": str(plan["experiment_id"]),
            "phase": "formal",
            "plan_schema": str(plan["schema"]),
        }
        if plan["native_raw_ambient_policy"]
        == raw_validation.AMBIENT_POLICY_UNSUBTRACTED_NO_AMBIENT
        else None
    )
    exact_p7_formal_owner = (
        plan["schema"] == thermal.PLAN_SCHEMA_V2
        and plan["experiment_id"] in {thermal.TD_B, thermal.TD_C}
        and plan["native_raw_ambient_policy"]
        == raw_validation.AMBIENT_POLICY_UNSUBTRACTED_NO_AMBIENT
        and ambient_policy_owner
        in raw_validation.UNSUBTRACTED_FORMAL_AMBIENT_POLICY_OWNERS
    )
    feature_statistic = (
        TD_B_FORMAL_FEATURE_STATISTIC
        if exact_p7_formal_owner
        else DEFAULT_STATISTIC
    )

    def observe_physical_return(
        returned: camera_gphoto2.CaptureResult,
        raw_step: Mapping[str, Any],
        physical_count: int,
    ) -> Mapping[str, Any]:
        callback = physical_return_observer_slot["callback"]
        if callback is None:
            raise RuntimeError("thermal physical return ledger owner is not bound")
        step = plan_steps_by_id.get(str(raw_step.get("capture_id")))
        if step is None:
            raise RuntimeError("thermal physical return lacks a frozen plan owner")
        return callback(step, returned, physical_count)

    raw_capture = raw_validation.build_native_raw_capture_step_fn(
        camera_dir=root / "camera", measurements_dir=root / "measurements", scratch_dir=root / "scratch",
        location_config_path=(
            root / "inputs/location.json"
            if (
                direct_ray_continuous or direct_f2_short or direct_guide8_emission_exposure
                or direct_guide6_strip_exposure
            )
            else thermal.LOCATION_PATH
        ), observer_config_path=thermal.OBSERVER_PATH,
        iso=str(resolved_settings.iso), aperture=str(resolved_settings.aperture),
        image_format=str(resolved_settings.image_format), camera_backend=camera_backend,
        recorded_exposure_purpose=str(plan["experiment_id"]),
        frozen_shutter_by_cache=plan["frozen_shutters"], timed_capture_fn=timed_capture,
        ambient_policy=str(plan["native_raw_ambient_policy"]),
        ambient_policy_owner=ambient_policy_owner,
        physical_return_observer=observe_physical_return,
    )

    def capture(step: Mapping[str, Any]) -> Mapping[str, Any]:
        plan_steps_by_id[str(step["capture_id"])] = step
        source = str(step["source_id"])
        state = str(step["state_id"])
        strip_zero_evidence = None
        ray_zero_evidence = None
        if source == "ray":
            strip_zero_evidence = esphome.verified_light(
                0, 0, 0, 0, 0, curve_path=thermal.CURVE_PATH,
            )
        elif (
            direct_strip_history or direct_td_c_fast_endpoint
            or direct_guide6_target_local or direct_guide7_f2 or direct_f2_short or direct_guide6_strip_exposure
        ):
            ray_zero_evidence = ray120c.set_cct(5600, intensity=0, gm=100)
            ray_readback = ray120c.get_cct()
            intensity = (
                ray_readback.get("data")
                or ((ray_readback.get("response") or {}).get("data"))
                or {}
            ).get("intensity")
            if int(intensity) != 0:
                raise RuntimeError("strip capture lacks Ray-zero readback")
        if source == "ambient":
            cache_key = None
        elif isinstance(step.get("exposure_cache_key"), str):
            cache_key = str(step["exposure_cache_key"])
        elif source == "ray":
            command = step["command"]
            cache_key = f"ray-h{int(command['hue'])}-s{int(command['sat'])}"
        else:
            cache_key = f"strip-{thermal.STRIP_COMMAND_KEYS[state]}"
        raw_step = {
            "capture_id": step["capture_id"], "source": source,
            "purpose": f"p7_thermal_{plan['stage'].lower()}_{source}_{state}",
            "repeat_index": step.get("cycle_index", step.get("session_index", 0)),
            "source_exposure_cache": cache_key, "auto_exposure": False,
            "physical_capture_budget_remaining": int(plan["budgets"]["physical_cr3_cap"]),
            "analysis_context": {
                "phase": plan["stage"],
                "formal_measurement": bool(step["formal_measurement"]),
                "native_raw_ambient_policy": plan["native_raw_ambient_policy"],
            },
        }
        captured_result = raw_capture(raw_step)
        if not isinstance(captured_result, Mapping):
            raise RuntimeError("timed RAW capture adapter returned malformed result")
        report = json.loads(Path(captured_result["patch_statistics"]).read_text(encoding="utf-8"))
        exposure = report["exposure_metadata"]
        if direct_guide8_emission_exposure or direct_f2_short or direct_guide6_strip_exposure:
            from camera_based_rgbww_optimizer.measurement.recorded_exposure import (
                validate_recorded_exposure_setting,
            )
            validate_recorded_exposure_setting(exposure, str(step["nominal_shutter"]))
        raw_metadata = report["raw_metadata"]
        timing = captured_result.get("timing_evidence")
        if not isinstance(timing, Mapping):
            raise RuntimeError("timed RAW capture lacks v2 timing evidence")
        elapsed = float(timing["best_effort_elapsed_s"] or 0.0)
        exposure_start = float(timing["local_readback_done_monotonic_s"]) + elapsed
        load = {window: 0.0 for window in (60, 300, 900)} if source == "ambient" else {
            window: integrated_history(source, exposure_start, window) for window in (60, 300, 900)
        }
        command = step["command"] or {"strip": "off", "ray": "off"}
        covariate_timestamp = exposure_start
        state_started = thermal_context["state_started_monotonic_s"]
        ray_started = thermal_context["ray_started_monotonic_s"]
        ray_off_since = thermal_context["ray_off_since_monotonic_s"]
        covariate = thermal.build_covariate_record(
            source_id=source, state_id=state, command=command,
            sequence_index=int(step["capture_id"].split("-", 1)[0]),
            capture_order=int(step["capture_id"].split("-", 1)[0]),
            source_order=int(step.get("source_order", 1)), monotonic_timestamp_ns=time.monotonic_ns(),
            wall_clock_timestamp=_utc_now(), session_elapsed_s=covariate_timestamp - session_start,
            source_on_elapsed_s=(
                0.0 if ray_started is None else max(0.0, covariate_timestamp - float(ray_started))
            ) if source in {"ray", "strip"} else 0.0,
            state_on_elapsed_s=(
                0.0 if state_started is None else max(0.0, covariate_timestamp - float(state_started))
            ),
            off_duration_before_s=(
                0.0 if ray_off_since is None else max(0.0, covariate_timestamp - float(ray_off_since))
            ) if source in {"ray", "strip"} else 0.0,
            previous_state_id=thermal_context["previous_state_id"],
            previous_state_dwell_s=thermal_context["previous_state_dwell_s"],
            shutter_seconds=float(exposure["seconds"]),
            raw_black_levels=raw_metadata["black_level_per_channel"],
            raw_white_level=float(raw_metadata["white_level"]), load_history=load,
            readback=readbacks.get(f"{source}:{state}"), curve=curve if source == "strip" else None,
        )
        output = {
            **captured_result, "saved_file": captured_result["capture"]["saved_file"],
            "recorded_exposure": exposure,
            "timing_evidence": dict(timing),
            "timing_metadata": dict(captured_result.get("timing_metadata") or {}),
            "thermal_covariates": covariate,
            "strip_zero_before_capture": strip_zero_evidence,
            "ray_zero_before_capture": ray_zero_evidence,
        }
        if source == "ambient":
            output["ambient_diagnostic"] = {
                "geometry_hash": report["location_config"]["sha256"],
                "black_levels": raw_metadata["black_level_per_channel"],
                "white_level": raw_metadata["white_level"],
                "black_level_tolerance_dn": raw_metadata["black_level_metadata_tolerance_dn"],
            }
        else:
            context = report.get("analysis_context")
            expected_ambient_subtraction = (
                plan["native_raw_ambient_policy"]
                == raw_validation.AMBIENT_POLICY_REQUIRE_PRECEDING
            )
            if (
                not isinstance(context, Mapping)
                or context.get("native_raw_ambient_policy")
                != plan["native_raw_ambient_policy"]
                or context.get("ambient_subtraction_applied")
                is not expected_ambient_subtraction
                or context.get("phase") != plan["stage"]
                or context.get("formal_measurement")
                is not bool(step["formal_measurement"])
            ):
                raise RuntimeError(
                    "thermal RAW feature report context differs from the frozen plan"
                )
            output["feature_statistic"] = feature_statistic
            output["ambient_policy_owner"] = (
                None if ambient_policy_owner is None else dict(ambient_policy_owner)
            )
            try:
                output["feature_values"] = required_hsi_features_from_report(
                    report, feature_ids, statistic=feature_statistic,
                )
            except HsiRejectedFeaturesError as exc:
                if not (direct_guide8_emission_exposure or direct_guide6_strip_exposure):
                    raise
                failure_names = set()
                for item in exc.rejected:
                    metrics = item.get("metrics") or {}
                    if float(metrics.get("nonfinite_fraction", 0.0)) > 0:
                        failure_names.add("nonfinite")
                    if float(metrics.get("clipped_fraction", 0.0)) > 0:
                        failure_names.add("clipping")
                    if float(metrics.get("near_noise_floor_fraction", 0.0)) > 0:
                        failure_names.add("near_noise")
                output["direct_quality"] = {
                    "status": "near_noise_only" if exc.weak_signal_only else "rejected",
                    "feature_count": 0, "required_feature_count": len(feature_ids),
                    "failures": sorted(failure_names),
                    "recorded_exposure_owner": "Canon:ExposureTime",
                }
            else:
                output["direct_quality"] = {
                    "status": "pass", "feature_count": len(feature_ids),
                    "recorded_exposure_owner": "Canon:ExposureTime",
                }
        return output

    def both_off_gate(gate_id: str) -> Mapping[str, Any]:
        from camera_based_rgbww_optimizer.optimization.hsi_source_evidence import validate_both_off

        strip = esphome.verified_light(0, 0, 0, 0, 0, curve_path=thermal.CURVE_PATH)
        ray_set = ray120c.set_cct(5600, intensity=0, gm=100)
        ray_readback = ray120c.get_cct()
        validate_both_off(strip, ray_readback, curve)
        off_at = time.monotonic()
        load_segments["ray"].append((off_at, 0.0))
        load_segments["strip"].append((off_at, 0.0))
        thermal_context["ray_off_since_monotonic_s"] = off_at
        return {
            "status": "pass", "gate_id": gate_id,
            "strip_verified_off": True, "ray_verified_off": True,
            "strip_device_evidence": dict(strip), "ray_off_command": dict(ray_set),
            "ray_readback": dict(ray_readback),
        }

    def source_isolation_check(gate_id: str) -> Mapping[str, Any]:
        if direct_strip_history or direct_guide6_target_local or direct_guide7_f2 or direct_f2_short or direct_guide6_strip_exposure:
            ray_set = ray120c.set_cct(5600, intensity=0, gm=100)
            ray_readback = ray120c.get_cct()
            intensity = (
                ray_readback.get("data")
                or ((ray_readback.get("response") or {}).get("data"))
                or {}
            ).get("intensity")
            if int(intensity) != 0:
                raise RuntimeError(f"Ray did not remain zero at source-isolation gate: {gate_id}")
            return {
                "status": "pass", "gate_id": gate_id,
                "source_verified_zero": True, "source_verified": "ray",
                "strip_verified_off": False, "ray_verified_off": True,
                "ray_off_command": dict(ray_set), "ray_readback": dict(ray_readback),
            }
        strip = esphome.verified_light(0, 0, 0, 0, 0, curve_path=thermal.CURVE_PATH)
        snapshot = strip.get("device_snapshot", {})
        if any(int(snapshot.get(key, -1)) != 0 for key in esphome.PAYLOAD_CHANNELS):
            raise RuntimeError(f"strip did not remain zero at source-isolation gate: {gate_id}")
        load_segments["strip"].append((time.monotonic(), 0.0))
        return {
            "status": "pass", "gate_id": gate_id,
            "source_verified_zero": True, "strip_verified_off": True, "ray_off_command": None,
            "strip_device_evidence": dict(strip),
        }

    def cleanup() -> Mapping[str, Any]:
        steps = all_off.turn_everything_off(
            strip_off_fn=lambda: esphome.verified_light(0, 0, 0, 0, 0, curve_path=thermal.CURVE_PATH),
            ray_set_cct_fn=ray120c.set_cct, ray_cct=5600, ray_gm=100,
        )
        rows = [item.to_jsonable() if hasattr(item, "to_jsonable") else dict(item) for item in steps]
        return {"status": "pass" if rows and all(item.get("ok") for item in rows) else "fail", "steps": rows}

    def validate_direct_post_capture(
        run_root: Path,
        frozen_plan: Mapping[str, Any],
        runtime_evidence: Mapping[str, Any] | None,
    ) -> Any:
        schema = (frozen_plan.get("execution_authorization") or {}).get("schema")
        if schema == "direct_guide6_strip_exposure_qualification_v1":
            return validate_direct_guide6_strip_exposure_post_capture(
                run_root, frozen_plan, runtime_evidence,
            )
        if schema == "direct_guide8_ray_emission_exposure_v1":
            return validate_direct_guide8_post_capture(run_root, frozen_plan, runtime_evidence)
        if schema == "direct_ray_r6_authority_v1":
            return validate_direct_ray_r6_post_capture(run_root, frozen_plan, runtime_evidence)
        if schema == "direct_ray_history_session_v1":
            return validate_direct_ray_history_session_post_capture(
                run_root, frozen_plan, runtime_evidence,
            )
        if schema == "direct_strip_history_session_v1":
            return validate_direct_strip_history_session_post_capture(
                run_root, frozen_plan, runtime_evidence,
            )
        if schema == "direct_ray_fast_long_bridge_session_v1":
            return validate_direct_ray_fast_long_bridge_session_post_capture(
                run_root, frozen_plan, runtime_evidence,
            )
        return validate_direct_protocol_post_capture(run_root, frozen_plan, runtime_evidence)

    return execute_plan(
        plan, run_dir=root, apply_command_fn=apply, readback_fn=readback,
        capture_fn=capture, both_off_gate_fn=both_off_gate,
        source_isolation_check_fn=(
            source_isolation_check
            if (
                direct_ray_continuous or direct_strip_history
                or direct_guide6_target_local or direct_guide7_f2 or direct_f2_short or direct_guide8_emission_exposure
                or direct_guide6_strip_exposure
            )
            else None
        ),
        cleanup_fn=cleanup,
        runtime_capture_settings_provenance=settings_provenance,
        post_capture_validator_fn=(validate_direct_post_capture if direct_protocol else None),
        bind_physical_return_observer_fn=lambda callback: physical_return_observer_slot.__setitem__(
            "callback", callback
        ),
        set_capture_context_fn=lambda value: timing_context.__setitem__("local_readback_done_monotonic_s", value),
    )


def _write_json(path: Path, value: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8")
    temporary.replace(path)


def _append_jsonl(path: Path, value: Mapping[str, Any]) -> None:
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(value, sort_keys=True, allow_nan=False) + "\n")
        handle.flush()


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    from camera_based_rgbww_optimizer.control import camera_remote
    parser = argparse.ArgumentParser(description="Execute direct P7 thermal diagnostic protocols.")
    parser.add_argument(
        "--experiment-id",
        choices=(
            *thermal.EXPERIMENT_IDS,
            thermal.RAY_HISTORY_3X3_EXPERIMENT_ID,
            thermal.RAY_FAST_LONG_BRIDGE_EXPERIMENT_ID,
            thermal.GUIDE8_RAY_EMISSION_EXPOSURE_EXPERIMENT_ID,
            thermal.GUIDE6_STRIP_EXPOSURE_QUALIFICATION_EXPERIMENT_ID,
        ),
        required=True,
    )
    parser.add_argument("--source", choices=("ray", "strip"))
    parser.add_argument(
        "--variant",
        choices=("core", "expansion", "history", thermal.TD_C_FAST_ENDPOINT_HOLDOUT_VARIANT, thermal.GUIDE6_DIRECT_TARGET_LOCAL_H120_S100_VARIANT, thermal.GUIDE6_DIRECT_TARGET_LOCAL_H120_S100_CONTINUATION_VARIANT, thermal.GUIDE7_F2_VARIANT, thermal.GUIDE7_F2_SHORT_ENDPOINT_VARIANT, thermal.GUIDE8_RAY_EMISSION_EXPOSURE_VARIANT, thermal.GUIDE6_STRIP_EXPOSURE_QUALIFICATION_VARIANT),
        default="core",
    )
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--run-name", required=True)
    parser.add_argument("--phase", choices=("formal", "diagnostic"), default="formal")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--dry-run", action="store_true")
    mode.add_argument("--execute", action="store_true")
    direct = parser.add_mutually_exclusive_group(required=True)
    direct.add_argument("--direct-r6", action="store_true", help="execute direct Ray R6 path")
    direct.add_argument(
        "--direct-ray-history-3x3", action="store_true",
        help="prepare or execute one session of the three-session Ray history experiment",
    )
    direct.add_argument(
        "--direct-strip-history-3x3", action="store_true",
        help="prepare or execute one session of the GUIDE5 strip history experiment",
    )
    direct.add_argument(
        "--direct-ray-fast-long-bridge", action="store_true",
        help="prepare or execute one GUIDE5 Ray fast/long bridge mini-session",
    )
    direct.add_argument("--direct-strip-td-b", action="store_true", help="execute direct strip TD-B path")
    direct.add_argument("--direct-td-c-core", action="store_true", help="execute direct TD-C core path")
    direct.add_argument(
        "--direct-td-c-fast-endpoint-holdout", action="store_true",
        help="execute the GUIDE5 FAST B/C endpoint holdout",
    )
    direct.add_argument(
        "--direct-guide6-h120-s100", action="store_true",
        help="execute the GUIDE6 direct target-local H120/S100 block",
    )
    direct.add_argument(
        "--direct-guide8-emission-exposure", action="store_true",
        help="execute the GUIDE8 Ray H120/S100 emission/exposure diagnostic",
    )
    direct.add_argument(
        "--direct-guide6-strip-exposure-qualification", action="store_true",
        help="execute the GUIDE6 strip-only S-MEASUREMENT exposure qualification",
    )
    parser.add_argument("--prerequisite-analysis", type=Path)
    parser.add_argument("--human-authorization")
    parser.add_argument("--session-index", type=int, choices=(1, 2, 3))
    parser.add_argument("--bridge-mini-session", type=int, choices=(1, 2, 3, 4))
    parser.add_argument("--session-start-condition")
    parser.add_argument("--allow-device-control", action="store_true")
    camera_remote.add_camera_backend_arguments(parser, default="remote")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None, *, backend_factory: Callable[..., Any] | None = None,
         run_fn: Callable[..., Path] = run_authorized_plan) -> int:
    args = parse_args(argv)
    direct_kind = (
        "ray-r6" if args.direct_r6 else
        "ray-history-3x3" if args.direct_ray_history_3x3 else
        "strip-history-3x3" if args.direct_strip_history_3x3 else
        "ray-fast-long-bridge" if args.direct_ray_fast_long_bridge else
        "strip-td-b" if args.direct_strip_td_b else
        "td-c-fast-endpoint-holdout" if args.direct_td_c_fast_endpoint_holdout else
        "guide6-h120-s100" if args.direct_guide6_h120_s100 else
        "guide8-emission-exposure" if args.direct_guide8_emission_exposure else
        "guide6-strip-exposure-qualification" if args.direct_guide6_strip_exposure_qualification else
        "td-c-core"
    )
    expected_scope = {
        "ray-r6": (thermal.TD_B, "ray", "core"),
        "ray-history-3x3": (thermal.RAY_HISTORY_3X3_EXPERIMENT_ID, "ray", "core"),
        "strip-history-3x3": (thermal.TD_B, "strip", "history"),
        "ray-fast-long-bridge": (
            thermal.RAY_FAST_LONG_BRIDGE_EXPERIMENT_ID, "ray", "core",
        ),
        "strip-td-b": (thermal.TD_B, "strip", "core"),
        "td-c-core": (thermal.TD_C, None, "core"),
        "td-c-fast-endpoint-holdout": (
            thermal.TD_C, None, thermal.TD_C_FAST_ENDPOINT_HOLDOUT_VARIANT,
        ),
        "guide6-h120-s100": (thermal.TD_C, None, args.variant),
        "guide8-emission-exposure": (
            thermal.GUIDE8_RAY_EMISSION_EXPOSURE_EXPERIMENT_ID,
            "ray", thermal.GUIDE8_RAY_EMISSION_EXPOSURE_VARIANT,
        ),
        "guide6-strip-exposure-qualification": (
            thermal.GUIDE6_STRIP_EXPOSURE_QUALIFICATION_EXPERIMENT_ID,
            "strip", thermal.GUIDE6_STRIP_EXPOSURE_QUALIFICATION_VARIANT,
        ),
    }[direct_kind]
    expected_phase = (
        "diagnostic"
        if direct_kind in {"guide8-emission-exposure", "guide6-strip-exposure-qualification"}
        else "formal"
    )
    if (args.experiment_id, args.source, args.variant) != expected_scope or args.phase != expected_phase:
        raise PermissionError(f"{direct_kind} arguments do not match its direct protocol scope")
    if direct_kind == "guide6-h120-s100" and args.variant not in {
        thermal.GUIDE6_DIRECT_TARGET_LOCAL_H120_S100_VARIANT,
        thermal.GUIDE6_DIRECT_TARGET_LOCAL_H120_S100_CONTINUATION_VARIANT,
        thermal.GUIDE7_F2_VARIANT,
        thermal.GUIDE7_F2_SHORT_ENDPOINT_VARIANT,
    }:
        raise PermissionError("GUIDE6 target-local direct path requires a frozen variant")
    if args.dry_run:
        if direct_kind == "ray-history-3x3":
            if args.session_index is not None:
                raise PermissionError("Ray history dry-run describes all three sessions")
            root = (Path(args.output_dir) / args.run_name).resolve()
            root.mkdir(parents=True, exist_ok=False)
            output = root / "experiment-spec.json"
            _write_json(output, thermal.build_ray_history_experiment_spec())
            print(output)
            return 0
        if direct_kind == "strip-history-3x3":
            if args.session_index is not None:
                raise PermissionError("strip history dry-run describes one selected session only")
            root = (Path(args.output_dir) / args.run_name).resolve()
            root.mkdir(parents=True, exist_ok=False)
            output = root / "experiment-spec.json"
            _write_json(output, thermal.build_strip_history_session_spec(1))
            print(output)
            return 0
        if direct_kind == "ray-fast-long-bridge":
            if args.bridge_mini_session is None:
                raise PermissionError("bridge dry-run requires --bridge-mini-session")
            root = (Path(args.output_dir) / args.run_name).resolve()
            root.mkdir(parents=True, exist_ok=False)
            output = root / "experiment-spec.json"
            _write_json(
                output,
                thermal.build_ray_fast_long_bridge_session_spec(
                    args.bridge_mini_session,
                ),
            )
            print(output)
            return 0
        if direct_kind in {"guide8-emission-exposure", "guide6-strip-exposure-qualification"}:
            root = (Path(args.output_dir) / args.run_name).resolve()
            root.mkdir(parents=True, exist_ok=False)
            output = root / "experiment-spec.json"
            variant = (
                thermal.GUIDE8_RAY_EMISSION_EXPOSURE_VARIANT
                if direct_kind == "guide8-emission-exposure"
                else thermal.GUIDE6_STRIP_EXPOSURE_QUALIFICATION_VARIANT
            )
            _write_json(output, thermal.build_direct_plan(thermal.TD_C, variant=variant))
            print(output)
            return 0
        output = write_dry_run(
            experiment_id=args.experiment_id, output_dir=args.output_dir,
            run_name=args.run_name, source=args.source, variant=args.variant,
        )
        print(output)
        return 0
    if not (args.execute and args.allow_device_control):
        raise PermissionError(f"{direct_kind} requires --execute and --allow-device-control")
    prerequisite = None
    plan = None
    if direct_kind in {"ray-history-3x3", "strip-history-3x3"}:
        if args.session_index is None:
            raise PermissionError("history execution requires one exact --session-index")
        if not isinstance(args.session_start_condition, str) or not args.session_start_condition.strip():
            raise PermissionError("Ray history execution requires the observed independent session start condition")
        builder = (
            thermal.build_ray_history_session_spec
            if direct_kind == "ray-history-3x3"
            else thermal.build_strip_history_session_spec
        )
        plan = builder(
            args.session_index, device_control_enabled=True,
            session_start_condition=args.session_start_condition,
        )
    elif direct_kind == "ray-fast-long-bridge":
        if args.bridge_mini_session is None:
            raise PermissionError("bridge execution requires --bridge-mini-session")
        if not isinstance(args.session_start_condition, str) or not args.session_start_condition.strip():
            raise PermissionError("bridge execution requires its observed reset start condition")
        if args.prerequisite_analysis is None:
            raise PermissionError("bridge execution requires accepted strip analyzer-v3")
        prerequisite = validate_scientific_prerequisite(
            args.prerequisite_analysis, kind="ray-fast-long-bridge",
        )
        plan = thermal.build_ray_fast_long_bridge_session_spec(
            args.bridge_mini_session,
            device_control_enabled=True,
            session_start_condition=args.session_start_condition,
            scientific_prerequisite=prerequisite,
        )
    elif direct_kind == "td-c-fast-endpoint-holdout":
        if args.prerequisite_analysis is None:
            raise PermissionError("FAST endpoint holdout requires corrected TD-C core analysis")
        prerequisite = validate_scientific_prerequisite(
            args.prerequisite_analysis, kind="td-c-fast-endpoint-holdout",
        )
        plan = thermal.build_direct_plan(
            thermal.TD_C, variant=thermal.TD_C_FAST_ENDPOINT_HOLDOUT_VARIANT,
        )
    if direct_kind == "ray-r6" and args.human_authorization != thermal.TD_B_R6_EXPERIMENT_ID:
        raise PermissionError("Ray R6 requires the exact Human experiment authorization token")
    if direct_kind == "guide6-h120-s100":
        plan = thermal.build_direct_plan(
            thermal.TD_C,
            variant=args.variant,
        )
    if direct_kind == "guide8-emission-exposure":
        plan = thermal.build_direct_plan(
            thermal.TD_C, variant=thermal.GUIDE8_RAY_EMISSION_EXPOSURE_VARIANT,
        )
    if direct_kind == "guide6-strip-exposure-qualification":
        plan = thermal.build_direct_plan(
            thermal.TD_C,
            variant=thermal.GUIDE6_STRIP_EXPOSURE_QUALIFICATION_VARIANT,
        )
    if direct_kind not in {
        "ray-r6", "ray-history-3x3", "strip-history-3x3",
        "ray-fast-long-bridge", "td-c-fast-endpoint-holdout", "guide6-h120-s100",
        "guide8-emission-exposure",
        "guide6-strip-exposure-qualification",
    }:
        if args.prerequisite_analysis is None:
            raise PermissionError(f"{direct_kind} requires a prior scientific analysis artifact")
        prerequisite = validate_scientific_prerequisite(args.prerequisite_analysis, kind=direct_kind)
    elif direct_kind == "ray-r6":
        prerequisite = None
    if plan is None:
        plan = thermal.build_direct_plan(args.experiment_id, source=args.source, variant=args.variant)
    if prerequisite is not None:
        plan["scientific_prerequisite"] = prerequisite
    if backend_factory is None:
        from camera_based_rgbww_optimizer.control import camera_remote
        backend_factory = camera_remote.create_camera_backend
    try:
        backend = backend_factory(args.camera_backend, env_file=args.remote_env_file,
                                  base_url=args.remote_base_url, timeout=args.remote_timeout)
    except TypeError:
        backend = backend_factory()
    print(run_fn(plan, output_dir=args.output_dir, run_name=args.run_name, camera_backend=backend))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
