from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import os
import shutil
import stat
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Mapping, Sequence

from camera_based_rgbww_optimizer.optimization import p7_thermal_diagnostics as thermal
from camera_based_rgbww_optimizer.optimization import measure_raw_observer_validation as raw_validation
from camera_based_rgbww_optimizer.control import camera_remote_v2
from camera_based_rgbww_optimizer.paths import PROJECT_TMP_DIR


DEFAULT_OUTPUT = PROJECT_TMP_DIR / "p7-thermal-diagnostics-offline"
REMOTE_V2_CAPABILITY = "remote_v2_capture_timing_v1"
PRODUCTION_WRAPPER = Path(__file__).parents[3] / "tmp/run-p7-thermal-diagnostics.zsh"
WRAPPER_OBSERVED_EXIT_SCHEMA = "p7_td_b_wrapper_observed_exit_v1"
EQ_R6_LAUNCH_LEDGER_SCHEMA = "p7_td_b_eq_r6_launch_ledger_v1"
EQ_R6_CANDIDATE_RESULT_SCHEMA = "p7_td_b_eq_r6_candidate_result_v1"
EQ_R6_TERMINAL_SEAL_SCHEMA = "p7_td_b_eq_r6_candidate_terminal_seal_v1"
EQ_R6_OUTER_RESULT_SCHEMA = "p7_td_b_eq_r6_outer_result_v1"
EQ_R6_OUTER_CANDIDATE_TERMINAL_SCHEMA = (
    "p7_td_b_eq_r6_outer_candidate_terminal_v1"
)
EQ_R6_PRELAUNCH_ARTIFACTS = (
    "frozen-inputs.json",
    "offline-plan.json",
    "camera-readiness.json",
    "ray-readiness.json",
    "all-off-python.json",
    "all-off-shell.json",
    "independent-final-zero.json",
    "prelaunch-terminal.json",
    "prelaunch-manifest.json",
)


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
    if plan.get("experiment_id") == thermal.TD_B and plan.get("source") == "ray":
        setup_ref = plan.get("exposure_setup_artifact")
        if not isinstance(setup_ref, Mapping):
            raise PermissionError("Ray TD-B execution lacks retained exposure setup evidence")
        setup_path = Path(str(setup_ref.get("path"))).resolve()
        if not setup_path.is_file() or hashlib.sha256(setup_path.read_bytes()).hexdigest() != setup_ref.get("sha256"):
            raise PermissionError("Ray TD-B exposure setup artifact hash differs")
        try:
            setup = json.loads(setup_path.read_text(encoding="utf-8"))
            validated = thermal.validate_td_b_exposure_setup(setup, artifact_path=setup_path)
        except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
            raise PermissionError("Ray TD-B exposure setup replay failed") from exc
        if setup.get("fake_only") is True or plan.get("formal_capture_eligible") is not True:
            raise PermissionError("Ray TD-B execution rejects fake or formal-ineligible setup evidence")
        if plan.get("setup_physical_cr3_count") != validated["physical_count"]:
            raise PermissionError("Ray TD-B setup physical ledger differs from resolved plan")


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
    if (
        not isinstance(authorization, Mapping)
        or authorization.get("human_authorization_verified") is not True
        or authorization.get("human_authorization_experiment_id") != experiment_id
        or authorization.get("remote_v2_capability") is not True
    ):
        raise PermissionError("thermal diagnostic execution lacks exact Human/v2 authorization evidence")
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
    prerequisite_artifact: str | Path = thermal.OPERATING_ENVELOPE_PATH,
) -> Path:
    root = (Path(output_dir) / run_name).resolve()
    root.mkdir(parents=True, exist_ok=False)
    plan = thermal.build_diagnostic_plan(
        experiment_id, source=source, variant=variant,
        prerequisite_artifact=prerequisite_artifact,
    )
    _write_json(root / "plan.json", plan)
    return root / "plan.json"


def run_td_b_eq_r6_fake(
    plan: Mapping[str, Any],
    *,
    capture_fn: Callable[[Mapping[str, Any]], Mapping[str, Any]],
    event_fn: Callable[[Mapping[str, Any]], None],
    cleanup_fn: Callable[[str], Mapping[str, Any]],
) -> dict[str, Any]:
    """Exercise the exact EQ-R6 scheduler through injected fake owners only."""
    thermal.validate_td_b_eq_r6_plan(plan)
    feature_ids = tuple(
        json.loads(thermal.POLICY_PATH.read_text(encoding="utf-8"))["feature_set"]["ids"]
    )
    candidates: list[list[dict[str, Any]]] = []
    event_ledger: list[dict[str, Any]] = []
    cleanup_ledger: list[dict[str, Any]] = []
    attempted_capture_calls = 0

    def emit(event: Mapping[str, Any]) -> None:
        record = dict(event)
        event_fn(record)
        event_ledger.append(record)

    for candidate_index, candidate in enumerate(plan["candidates"], start=1):
        if candidate_index == 2:
            first_bad = thermal.td_b_eq_capture_quality_failures(
                candidates[0][-1], required_feature_ids=feature_ids,
            )
            if set(first_bad) != {"clipping"}:
                raise ValueError("candidate 2 is unlocked only by candidate 1 clipping")
        emit({
            "event": "strip_zero_verified",
            "candidate_index": candidate_index,
            "generation_bearing": True,
        })
        emit({
            "event": "ray_a_on",
            "candidate_index": candidate_index,
            "command": dict(thermal.RAY_STATES["A"]),
        })
        emit({
            "event": "fake_wait",
            "candidate_index": candidate_index,
            "duration_s": 600,
            "capture_count": 0,
        })
        emit({
            "event": "ray_a_to_c",
            "candidate_index": candidate_index,
            "command": dict(thermal.RAY_STATES["C"]),
        })
        returned: list[dict[str, Any]] = []
        stop_kind: str | None = None
        for capture_id, slot_s in zip(candidate["capture_ids"], candidate["slots_s"]):
            request = {
                "candidate_index": candidate_index,
                "capture_id": capture_id,
                "requested_elapsed_s": slot_s,
                "nominal_shutter": candidate["nominal_shutter"],
            }
            attempted_capture_calls += 1
            row = dict(capture_fn(request))
            row.setdefault("capture_id", capture_id)
            row.setdefault("requested_elapsed_s", slot_s)
            row.setdefault("nominal_shutter", candidate["nominal_shutter"])
            if row["capture_id"] != capture_id or row["requested_elapsed_s"] != slot_s:
                raise ValueError("fake capture adapter returned a different EQ slot")
            returned.append(row)
            failures = thermal.td_b_eq_capture_quality_failures(
                row, required_feature_ids=feature_ids,
            )
            emit({
                "event": "capture_returned",
                "candidate_index": candidate_index,
                "capture_id": capture_id,
                "failures": list(failures),
            })
            if failures:
                stop_kind = "clipping" if set(failures) == {"clipping"} else "invalid"
                break
        candidates.append(returned)
        emit({"event": "ray_off", "candidate_index": candidate_index})
        for cleanup_name in ("python", "shell", "independent_final_zero", "terminal_seal"):
            result = dict(cleanup_fn(cleanup_name))
            if result.get("status") != "pass":
                raise ValueError(f"fake EQ cleanup failed: {cleanup_name}")
            cleanup_ledger.append({
                "candidate_index": candidate_index,
                "cleanup": cleanup_name,
                **result,
            })
        if candidate_index == 1 and stop_kind == "clipping":
            continue
        break

    classification = thermal.classify_td_b_eq_r6(
        candidates, required_feature_ids=feature_ids,
    )
    return {
        "schema": "p7_td_b_eq_r6_fake_run_v1",
        "experiment_id": thermal.TD_B_EQ_R6_EXPERIMENT_ID,
        "status": classification["status"],
        "classification": classification,
        "candidate_results": candidates,
        "event_ledger": event_ledger,
        "cleanup_ledger": cleanup_ledger,
        "attempted_capture_calls": attempted_capture_calls,
        "device_calls": 0,
        "network_calls": 0,
        "real_cleanup_calls": 0,
        "retry": 0,
    }


def execute_td_b_exposure_setup(
    plan: Mapping[str, Any], *, run_dir: str | Path,
    capture_setup_fn: Callable[[Mapping[str, Any]], Sequence[Mapping[str, Any]]],
    both_off_gate_fn: Callable[[str], Mapping[str, Any]],
    apply_ray_fn: Callable[[Mapping[str, Any]], Mapping[str, Any]],
    ray_readback_fn: Callable[[], Mapping[str, Any]],
    strip_off_evidence_fn: Callable[[], Mapping[str, Any]],
    cleanup_fn: Callable[[], Mapping[str, Any]],
    shell_cleanup_evidence: Mapping[str, Any],
    historical_seed: Mapping[str, Any],
    camera_settings: Mapping[str, Any],
    code_checkpoint: str,
    execution_authorized: bool,
    fake_only: bool,
    monotonic_fn: Callable[[], float] = time.monotonic,
    sleep_fn: Callable[[float], None] = time.sleep,
) -> Path:
    """Execute the bounded setup state machine through injected device/camera owners."""
    if (
        plan.get("experiment_id") != thermal.TD_B
        or plan.get("source") != "ray"
        or plan.get("exposure_setup_required") != [thermal.TD_B_SETUP_CACHE_KEY]
        or plan.get("budgets", {}).get("setup_physical_cr3_cap") != thermal.TD_B_SETUP_PHYSICAL_CAP
        or plan.get("budgets", {}).get("formal_cap") != 16
        or plan.get("budgets", {}).get("physical_cr3_cap") != 24
    ):
        raise PermissionError("TD-B setup requires the exact unresolved Ray plan and frozen budgets")
    authorization = plan.get("execution_authorization")
    if not fake_only and (
        not execution_authorized
        or plan.get("status") != "execute_authorized"
        or not isinstance(authorization, Mapping)
        or authorization.get("human_authorization_verified") is not True
        or authorization.get("human_authorization_experiment_id") != thermal.TD_B
        or authorization.get("remote_v2_capability") is not True
    ):
        raise PermissionError("TD-B real exposure setup requires the exact plan execution gate")
    if camera_settings.get("v2_capture_capability") != REMOTE_V2_CAPABILITY:
        raise PermissionError("TD-B setup requires the formal remote v2 capability owner")
    if historical_seed.get("seed_only") is not True or historical_seed.get("formal_capture_eligible") is not False:
        raise PermissionError("TD-B setup rejects a historical seed with formal authority")

    root = Path(run_dir)
    root.mkdir(parents=True, exist_ok=False)
    failure: BaseException | None = None
    artifact_path = root / "setup.json"
    cleanup_done = False
    retained_attempts: list[Mapping[str, Any]] = []

    def validate_off_gate(evidence: Mapping[str, Any], gate_id: str) -> None:
        from camera_based_rgbww_optimizer.optimization.hsi_source_evidence import validate_both_off

        if (
            evidence.get("status") != "pass"
            or evidence.get("gate_id") != gate_id
            or evidence.get("strip_verified_off") is not True
            or evidence.get("ray_verified_off") is not True
        ):
            raise RuntimeError(f"TD-B setup both-off gate failed: {gate_id}")
        curve = json.loads(thermal.CURVE_PATH.read_text(encoding="utf-8"))
        validate_both_off(
            evidence.get("strip_device_evidence", {}), evidence.get("ray_readback", {}), curve,
        )

    try:
        start_gate = dict(both_off_gate_fn("setup_start"))
        validate_off_gate(start_gate, "setup_start")
        ray_set = dict(apply_ray_fn(dict(thermal.TD_B_SETUP_COMMAND)))
        ray_readback = dict(ray_readback_fn())
        strip_off = dict(strip_off_evidence_fn())
        setup_request = {
            "schema": thermal.TD_B_SETUP_SCHEMA,
            "capture_role": "exposure_setup",
            "formal_measurement": False,
            "source": "ray",
            "state_id": thermal.TD_B_SETUP_STATE,
            "command": dict(thermal.TD_B_SETUP_COMMAND),
            "auto_exposure": True,
            "max_captures": thermal.TD_B_SETUP_PHYSICAL_CAP,
            "physical_capture_budget_remaining": thermal.TD_B_SETUP_PHYSICAL_CAP,
            "initial_shutter_seed": historical_seed.get("initial_shutter_seed") if historical_seed.get("historical_seed_usable") else None,
        }
        attempts = [dict(row) for row in capture_setup_fn(setup_request)]
        retained_attempts = attempts
        _write_json(root / "setup-attempts.json", {
            "schema": "p7_td_b_exposure_setup_attempts_v1",
            "attempt_count": len(attempts),
            "attempts": attempts,
        })
        if not 1 <= len(attempts) <= thermal.TD_B_SETUP_PHYSICAL_CAP:
            raise RuntimeError("physical_budget_accounting_violation")
        off_gate = dict(both_off_gate_fn("setup_complete"))
        validate_off_gate(off_gate, "setup_complete")
        cold_start = monotonic_fn()
        sleep_fn(1800.0)
        cold_end = monotonic_fn()
        python_cleanup = dict(cleanup_fn())
        cleanup_done = True
        artifact = thermal.build_td_b_exposure_setup_artifact(
            attempts=attempts,
            camera=camera_settings,
            historical_seed=historical_seed,
            isolation={"ray_set_response": ray_set, "ray_readback": ray_readback, "strip_device_evidence": strip_off},
            cold_proxy={"required_wait_s": 1800, "start_monotonic_s": cold_start, "end_monotonic_s": cold_end},
            cleanup={
                "python": python_cleanup,
                "shell": dict(shell_cleanup_evidence.get("shell", {})),
                "wrapper": dict(shell_cleanup_evidence.get("wrapper", {})),
                "final_both_off": dict(shell_cleanup_evidence.get("final_both_off", {})),
            },
            code_checkpoint=code_checkpoint,
            fake_only=fake_only,
        )
        _write_json(artifact_path, artifact)
    except BaseException as exc:
        failure = exc
        failure_attempts = getattr(exc, "attempts", retained_attempts)
        if not isinstance(failure_attempts, Sequence) or isinstance(failure_attempts, (str, bytes)):
            failure_attempts = retained_attempts
        _write_json(root / "failure.json", {
            "type": type(exc).__name__, "message": str(exc), "at": _utc_now(),
            "capture_attempted": bool(failure_attempts),
            "retained_attempt_count": len(failure_attempts),
            "retained_attempts": [dict(row) for row in failure_attempts if isinstance(row, Mapping)],
        })
        if not cleanup_done:
            try:
                cleanup_fn()
                cleanup_done = True
            except BaseException as cleanup_exc:
                _write_json(root / "cleanup-failure.json", {"type": type(cleanup_exc).__name__, "message": str(cleanup_exc)})
    if failure is not None:
        raise failure
    return artifact_path


class _TimedSetupBackend:
    """Expose the shared auto-exposure interface through remote v2 only."""

    def __init__(self, backend: Any, *, connection: Any, readback_done: float):
        self.backend = backend
        self.connection = connection
        self.readback_done = readback_done

    def connect(self) -> Any:
        return self.connection

    def resolve_capture_settings(self, **kwargs: Any) -> Any:
        return self.backend.resolve_capture_settings(**kwargs)

    def read_shutter_current_and_choices(self, connection: Any) -> tuple[str, list[str]]:
        return self.backend.read_shutter_current_and_choices(connection)

    def read_current_shutter(self, connection: Any) -> str:
        return self.backend.read_current_shutter(connection)

    def capture(self, **kwargs: Any) -> Any:
        kwargs.pop("allow_bulb", None)
        return self.backend.capture_with_timing(
            **kwargs, local_readback_done_monotonic_s=self.readback_done,
        )


def _validate_checkpoint_and_tree(code_checkpoint: str) -> None:
    if len(code_checkpoint) != 40 or any(ch not in "0123456789abcdef" for ch in code_checkpoint):
        raise PermissionError("E0X requires a full lowercase Git checkpoint")
    root = Path(__file__).parents[3]
    head = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=root, check=True, capture_output=True, text=True,
    ).stdout.strip()
    if head != code_checkpoint:
        raise PermissionError("E0X checkpoint differs from current HEAD")
    scoped = ("src", "tests", "docs", ".agents/skills", "tmp/run-p7-thermal-diagnostics.zsh")
    dirty = subprocess.run(
        ["git", "diff", "--quiet", "HEAD", "--", *scoped], cwd=root,
    ).returncode
    if dirty != 0:
        raise PermissionError("E0X production code, tests, docs, skill, or wrapper is dirty")


def _setup_attempt_from_capture(
    capture: Any, *, attempt_index: int, disposition: str, destination: Path,
) -> tuple[dict[str, Any], Path]:
    raw_source = Path(capture.saved_file).resolve()
    sidecar_source = Path(capture.remote_metadata_path).resolve() if capture.remote_metadata_path else None
    if (
        capture.endpoint != "/v2/capture" or sidecar_source is None
        or not raw_source.is_file() or raw_source.stat().st_size <= 0 or not sidecar_source.is_file()
    ):
        raise RuntimeError("TD-B setup attempt lacks retained remote-v2 CR3/sidecar evidence")
    destination.mkdir(parents=True, exist_ok=True)
    raw = destination / f"{attempt_index:04d}-td-b-exposure-setup.CR3"
    sidecar = raw.with_suffix(raw.suffix + ".metadata.json")
    shutil.copy2(raw_source, raw)
    shutil.copy2(sidecar_source, sidecar)
    metadata = json.loads(sidecar.read_text(encoding="utf-8"))
    remote, receipt = camera_remote_v2.split_and_validate_sidecar(metadata, payload=raw.read_bytes())
    timing = receipt.get("timing_evidence") or {}
    estimate = remote.get("exposure_start_estimate") or {}
    row = {
        "attempt_index": attempt_index,
        "capture_id": remote.get("capture_id"),
        "disposition": disposition,
        "cr3_path": str(raw.resolve()),
        "cr3_sha256": hashlib.sha256(raw.read_bytes()).hexdigest(),
        "cr3_byte_count": raw.stat().st_size,
        "sidecar_path": str(sidecar.resolve()),
        "sidecar_sha256": hashlib.sha256(sidecar.read_bytes()).hexdigest(),
        "request_id": remote.get("request_id"),
        "timing_tier": timing.get("tier"),
        "timing_method": estimate.get("method"),
        "recorded_exposure": remote.get("recorded_exposure"),
        "shutter_speed": capture.settings.shutter_speed,
        "npy_paths": [],
        "npy_deleted": True,
    }
    return row, raw_source


def _validate_td_b_setup_frozen_plan(plan: Mapping[str, Any]) -> Mapping[str, Any]:
    """Validate the setup plan before backend inspection or output ownership."""
    if (
        plan.get("experiment_id") != thermal.TD_B or plan.get("source") != "ray"
        or plan.get("status") != "execute_authorized"
        or plan.get("exposure_setup_required") != [thermal.TD_B_SETUP_CACHE_KEY]
        or plan.get("budgets") != {"formal_cap": 16, "ambient_cap": 0,
            "physical_cr3_cap": 24, "setup_physical_cr3_cap": 8}
    ):
        raise PermissionError("TD-B setup phase requires the exact unresolved authorized Ray plan")
    expected_inputs = {
        "location": thermal.LOCATION_PATH,
        "policy": thermal.POLICY_PATH,
        "uncertainty": thermal.UNCERTAINTY_PATH,
        "manifold": thermal.MANIFOLD_PATH,
        "code_duty_curve": thermal.CURVE_PATH,
    }
    inputs = plan.get("inputs")
    if not isinstance(inputs, Mapping) or any(
        inputs.get(name) != thermal.file_reference(path) for name, path in expected_inputs.items()
    ):
        raise PermissionError("TD-B setup frozen input references differ before device access")
    try:
        thermal.validate_trusted_operating_envelope_reference(
            inputs.get("operating_envelope", {}), require_v2=True,
        )
    except ValueError as exc:
        raise PermissionError("TD-B setup operating-envelope identity differs before device access") from exc
    return inputs


def run_td_b_setup_provisional(
    plan: Mapping[str, Any], *, output_dir: str | Path, run_name: str,
    camera_backend: Any, code_checkpoint: str,
    sleep_fn: Callable[[float], None] = time.sleep,
    monotonic_fn: Callable[[], float] = time.monotonic,
) -> Path:
    """Run the real setup child; shell/wrapper evidence is finalized later."""
    _validate_checkpoint_and_tree(code_checkpoint)
    inputs = _validate_td_b_setup_frozen_plan(plan)
    if getattr(camera_backend, "v2_capture_capability", None) != REMOTE_V2_CAPABILITY:
        raise PermissionError("TD-B setup phase requires the remote-v2 capability owner")
    root = (Path(output_dir) / run_name).resolve()
    if root.is_symlink():
        raise PermissionError("TD-B setup run directory cannot be a symlink")
    root.parent.mkdir(parents=True, exist_ok=True)
    if root.parent.is_symlink():
        raise PermissionError("TD-B setup output parent cannot be a symlink")
    if root.exists():
        if not root.is_dir() or any(root.iterdir()):
            raise FileExistsError(f"TD-B setup run directory must be new or shell-created empty: {root}")
    else:
        root.mkdir()
    unresolved_path = root / "unresolved-plan.json"
    _write_json(unresolved_path, dict(plan))
    from camera_based_rgbww_optimizer.control import all_off, esphome, ray120c
    from camera_based_rgbww_optimizer.measurement import raw_mosaic_patches
    from camera_based_rgbww_optimizer.optimization.hsi_source_evidence import (
        validate_both_off, validate_ray_readback, validate_strip_device_evidence,
    )
    curve = json.loads(thermal.CURVE_PATH.read_text(encoding="utf-8"))
    retained: list[dict[str, Any]] = []
    original_paths: list[Path] = []
    cleanup_done = False

    def strip_off() -> Mapping[str, Any]:
        return esphome.verified_light(0, 0, 0, 0, 0, curve_path=thermal.CURVE_PATH)

    def both_off() -> dict[str, Any]:
        strip = dict(strip_off())
        ray120c.set_cct(5600, intensity=0, gm=100)
        ray = dict(ray120c.get_cct())
        validate_both_off(strip, ray, curve)
        return {"strip_device_evidence": strip, "ray_readback": ray}

    try:
        seed = thermal.audit_td_b_historical_seed()
        if seed.get("seed_only") is not True or seed.get("formal_capture_eligible") is not False:
            raise PermissionError("TD-B setup historical seed audit is invalid")
        start_zero = both_off()
        from camera_based_rgbww_optimizer.control import camera_remote
        config = getattr(camera_backend, "config", None)
        if config is None or not getattr(config, "base_url", None):
            raise PermissionError("TD-B setup remote backend lacks health owner")
        health = camera_remote.read_remote_health(
            base_url=config.base_url, timeout=float(getattr(camera_backend, "timeout", 30.0)),
            opener=getattr(camera_backend, "opener", camera_remote.request.urlopen),
        )
        if health.get("status") != "ok":
            raise PermissionError("TD-B setup remote health did not report ok")
        connection = camera_backend.connect()
        settings, settings_provenance = _resolve_remote_capture_settings(camera_backend)
        ray_set = dict(ray120c.set_hsi(120, 50, intensity_percent=100.0))
        ray_readback = dict(ray120c.get_hsi())
        strip_zero = dict(strip_off())
        expected = {"hue": 120, "sat": 50, "intensity": 1000}
        validate_ray_readback(ray_set, expected)
        validate_ray_readback(ray_readback, expected)
        validate_strip_device_evidence(strip_zero, {channel: 0 for channel in thermal.CHANNELS}, curve)
        readback_done = monotonic_fn()
        _write_json(root / "setup-preflight.json", {
            "status": "pass", "experiment_id": thermal.TD_B, "phase": "setup",
            "code_checkpoint": code_checkpoint, "input_hashes": {
                name: reference["sha256"] for name, reference in inputs.items()
            }, "budgets": dict(plan["budgets"]), "remote_health": dict(health),
            "camera_settings": settings_provenance, "run_start_zero": start_zero,
            "ray_readback": ray_readback, "strip_zero": strip_zero,
        })

        def observe(kind: str, capture: Any) -> None:
            if len(retained) >= thermal.TD_B_SETUP_PHYSICAL_CAP:
                error = RuntimeError("physical_budget_accounting_violation")
                setattr(error, "attempts", retained)
                raise error
            row, original = _setup_attempt_from_capture(
                capture, attempt_index=len(retained) + 1,
                disposition="trial" if kind == "trial" else "rejected_final",
                destination=root / "attempts",
            )
            retained.append(row)
            original_paths.append(original)

        timed = _TimedSetupBackend(camera_backend, connection=connection, readback_done=readback_done)
        auto = __import__(
            "camera_based_rgbww_optimizer.control.camera_gphoto2", fromlist=["auto_expose_capture"]
        ).auto_expose_capture(
            output_dir=root / "camera", filename_template="td-b-setup-final.CR3",
            target_max=19661, iso=settings.iso, aperture=settings.aperture, image_format=settings.image_format,
            min_shutter_speed="1/16000", max_shutter_speed="25", max_trials=7, max_captures=8,
            initial_shutter_speed=seed.get("initial_shutter_seed"), scratch_dir=root / "scratch",
            camera_backend=timed,
            meter_fn=lambda raw: _raw_meter(raw_mosaic_patches.meter_raw_exposure(
                raw, location_config_path=thermal.LOCATION_PATH, observer_config_path=thermal.OBSERVER_PATH,
            )),
            attempt_observer=observe,
        )
        final_original = auto.final_capture.saved_file.resolve()
        final_rows = [row for row, original in zip(retained, original_paths, strict=True) if original == final_original]
        if len(final_rows) != 1:
            raise RuntimeError("TD-B setup final capture owner is missing from retained attempts")
        final_rows[0]["disposition"] = "final"
        for original in original_paths:
            original.unlink(missing_ok=True)
            original.with_suffix(original.suffix + ".metadata.json").unlink(missing_ok=True)
        _write_json(root / "setup-attempts.json", {
            "schema": "p7_td_b_exposure_setup_attempts_v1", "attempt_count": len(retained), "attempts": retained,
        })
        setup_zero = both_off()
        cold_start = monotonic_fn()
        sleep_fn(1800.0)
        cold_end = monotonic_fn()
        steps = all_off.turn_everything_off(
            strip_off_fn=lambda: esphome.verified_light(0, 0, 0, 0, 0, curve_path=thermal.CURVE_PATH),
            ray_set_cct_fn=ray120c.set_cct, ray_cct=5600, ray_gm=100,
        )
        python_cleanup = {
            "status": "pass" if all(step.ok for step in steps) else "fail",
            "steps": [step.to_jsonable() for step in steps], "exit_code": 0 if all(step.ok for step in steps) else 1,
        }
        _write_json(root / "all-off-python.json", python_cleanup)
        cleanup_done = True
        provisional = {
            "schema": thermal.TD_B_SETUP_PROVISIONAL_SCHEMA,
            "status": "setup_capture_complete_waiting_for_wrapper_finalize",
            "code_checkpoint": code_checkpoint,
            "unresolved_plan": thermal.file_reference(unresolved_path),
            "wrapper_source": thermal.file_reference(PRODUCTION_WRAPPER),
            "attempts": retained,
            "historical_seed": seed,
            "camera": {"backend": "remote", "v2_capture_capability": REMOTE_V2_CAPABILITY,
                "capture_settings_owner": "remote_backend.resolve_capture_settings", **settings_provenance},
            "isolation": {"run_start_zero": start_zero, "ray_set_response": ray_set,
                "ray_readback": ray_readback, "strip_device_evidence": strip_zero,
                "setup_complete_zero": setup_zero},
            "cold_proxy": {"required_wait_s": 1800, "start_monotonic_s": cold_start, "end_monotonic_s": cold_end},
            "python_cleanup": thermal.file_reference(root / "all-off-python.json"),
        }
        path = root / "setup-provisional.json"
        _write_json(path, provisional)
        return path
    except BaseException as exc:
        _write_json(root / "failure.json", {"type": type(exc).__name__, "message": str(exc),
            "at": _utc_now(), "retained_attempt_count": len(retained), "retained_attempts": retained})
        if not cleanup_done:
            steps = all_off.turn_everything_off()
            _write_json(root / "all-off-python.json", {"status": "pass" if all(step.ok for step in steps) else "fail",
                "steps": [step.to_jsonable() for step in steps], "exit_code": 0 if all(step.ok for step in steps) else 1})
        raise


def _raw_meter(result: Any) -> Any:
    from camera_based_rgbww_optimizer.control.camera_gphoto2 import ExposureMeasurement
    from camera_based_rgbww_optimizer.measurement.raw_mosaic_patches import PLANE_ORDER
    channel_max = tuple(int(round(max(0.0, min(1.0, float(result.plane_max.get(label) or 0.0))) * 65535.0)) for label in PLANE_ORDER)
    return ExposureMeasurement(maximum=int(result.exposure_metric), raw_visible_max=result.raw_visible_max,
        channel_max=channel_max, exposure_metric=float(result.exposure_metric), details=result.to_jsonable())


def finalize_td_b_setup_after_wrapper(
    run_dir: str | Path, *, code_checkpoint: str,
    final_zero_fn: Callable[[], Mapping[str, Any]] | None = None,
) -> tuple[Path, Path, Path]:
    """Create canonical setup, resolved plan, and release after wrapper exit."""
    _validate_checkpoint_and_tree(code_checkpoint)
    root = Path(run_dir).resolve()
    provisional_path = root / "setup-provisional.json"
    provisional = json.loads(provisional_path.read_text(encoding="utf-8"))
    expected = {
        "schema": thermal.TD_B_SETUP_PROVISIONAL_SCHEMA,
        "status": "setup_capture_complete_waiting_for_wrapper_finalize",
        "code_checkpoint": code_checkpoint,
        "unresolved_plan": thermal.file_reference(root / "unresolved-plan.json"),
        "wrapper_source": thermal.file_reference(PRODUCTION_WRAPPER),
        "python_cleanup": thermal.file_reference(root / "all-off-python.json"),
    }
    for name, value in expected.items():
        if provisional.get(name) != value:
            raise ValueError(f"TD-B setup provisional {name} binding differs")
    wrapper_path = root / "wrapper-result.json"
    observed_exit_path = root / "wrapper-observed-exit.json"
    shell_path = root / "all-off-shell.json"
    wrapper = json.loads(wrapper_path.read_text(encoding="utf-8"))
    observed_exit = json.loads(observed_exit_path.read_text(encoding="utf-8"))
    shell_rows = json.loads(shell_path.read_text(encoding="utf-8"))
    child_exit = int((root / "child-exit-status.txt").read_text(encoding="utf-8").strip())
    shell_exit = int((root / "all-off-shell.exit-status.txt").read_text(encoding="utf-8").strip())
    if (
        wrapper.get("status") != "complete" or wrapper.get("child_exit_code") != 0
        or wrapper.get("shell_cleanup_exit_code") != 0 or wrapper.get("wrapper_exit_code") != 0
        or wrapper.get("signal") is not None or child_exit != 0 or shell_exit != 0
    ):
        raise ValueError("TD-B setup wrapper child/signal/cleanup evidence failed")
    if (
        set(observed_exit) != {"schema", "status", "return_code", "observed_at", "wrapper_result"}
        or observed_exit.get("schema") != WRAPPER_OBSERVED_EXIT_SCHEMA
        or observed_exit.get("status") != "exited"
        or observed_exit.get("return_code") != 0
        or observed_exit.get("wrapper_result") != thermal.file_reference(wrapper_path)
    ):
        raise ValueError("TD-B setup outer orchestrator did not observe a successful wrapper exit")
    if not isinstance(shell_rows, list):
        raise ValueError("TD-B setup shell cleanup output is malformed")
    shell = {"status": "pass" if shell_rows and all(row.get("ok") for row in shell_rows) else "fail",
        "steps": shell_rows, "exit_code": shell_exit}
    python_cleanup = json.loads((root / "all-off-python.json").read_text(encoding="utf-8"))
    wrapper_summary = {key: wrapper.get(key) for key in (
        "status", "child_exit_code", "shell_cleanup_exit_code", "wrapper_exit_code", "signal",
    )}
    if final_zero_fn is None:
        from camera_based_rgbww_optimizer.control import esphome, ray120c
        curve = json.loads(thermal.CURVE_PATH.read_text(encoding="utf-8"))
        strip = esphome.verified_light(0, 0, 0, 0, 0, curve_path=thermal.CURVE_PATH)
        ray120c.set_cct(5600, intensity=0, gm=100)
        ray = ray120c.get_cct()
        final_zero = {"strip_device_evidence": dict(strip), "ray_readback": dict(ray)}
        from camera_based_rgbww_optimizer.optimization.hsi_source_evidence import validate_both_off
        validate_both_off(final_zero["strip_device_evidence"], final_zero["ray_readback"], curve)
    else:
        final_zero = dict(final_zero_fn())
    final_zero_path = root / "independent-final-zero.json"
    _write_json(final_zero_path, final_zero)
    base = thermal.build_td_b_exposure_setup_artifact(
        attempts=provisional["attempts"], camera=provisional["camera"],
        historical_seed=provisional["historical_seed"],
        isolation={key: provisional["isolation"][key] for key in (
            "ray_set_response", "ray_readback", "strip_device_evidence",
        )},
        cold_proxy=provisional["cold_proxy"],
        cleanup={"python": python_cleanup, "shell": shell, "wrapper": wrapper_summary,
            "final_both_off": final_zero},
        code_checkpoint=code_checkpoint, fake_only=False,
    )
    canonical = {
        "schema": thermal.TD_B_SETUP_SCHEMA_V2,
        "status": "setup_canonical_complete",
        "base": base,
        "bindings": {
            "code_checkpoint": code_checkpoint,
            "unresolved_plan": thermal.file_reference(root / "unresolved-plan.json"),
            "provisional": thermal.file_reference(provisional_path),
            "wrapper_source": thermal.file_reference(PRODUCTION_WRAPPER),
            "wrapper_result": thermal.file_reference(wrapper_path),
            "wrapper_observed_exit": thermal.file_reference(observed_exit_path),
            "all_off_python": thermal.file_reference(root / "all-off-python.json"),
            "all_off_shell": thermal.file_reference(shell_path),
            "final_zero": thermal.file_reference(final_zero_path),
        },
    }
    canonical_path = root / "setup.json"
    _write_json(canonical_path, canonical)
    thermal.validate_td_b_exposure_setup(canonical, artifact_path=canonical_path)
    unresolved = json.loads((root / "unresolved-plan.json").read_text(encoding="utf-8"))
    resolved = thermal.resolve_td_b_plan_with_setup(unresolved, setup_artifact_path=canonical_path)
    resolved_path = root / "resolved-formal-plan.json"
    _write_json(resolved_path, resolved)
    release = {
        "schema": thermal.TD_B_SETUP_RELEASE_SCHEMA,
        "status": "formal_plan_resolved",
        "code_checkpoint": code_checkpoint,
        "canonical_setup": thermal.file_reference(canonical_path),
        "resolved_formal_plan": thermal.file_reference(resolved_path),
    }
    release_path = root / "setup-release.json"
    _write_json(release_path, release)
    thermal.validate_td_b_setup_release(release, release_path=release_path)
    return canonical_path, resolved_path, release_path


def orchestrate_td_b_setup(
    *, run_dir: str | Path, code_checkpoint: str, wrapper_args: Sequence[str],
    wrapper_path: str | Path = PRODUCTION_WRAPPER,
    run_fn: Callable[..., subprocess.CompletedProcess[Any]] = subprocess.run,
    setup_finalize_fn: Callable[..., tuple[Path, Path, Path]] = finalize_td_b_setup_after_wrapper,
    validate_checkpoint_fn: Callable[[str], None] = _validate_checkpoint_and_tree,
) -> tuple[Path, Path, Path]:
    """Wait for the production wrapper to exit before canonical setup finalization."""
    validate_checkpoint_fn(code_checkpoint)
    root = Path(run_dir).resolve()
    completed = run_fn(
        ["zsh", str(Path(wrapper_path).resolve()), str(root), *wrapper_args],
        check=False,
    )
    wrapper_result_path = root / "wrapper-result.json"
    if not wrapper_result_path.is_file():
        raise RuntimeError("TD-B setup wrapper exited without wrapper-result evidence")
    observed = {
        "schema": WRAPPER_OBSERVED_EXIT_SCHEMA,
        "status": "exited",
        "return_code": int(completed.returncode),
        "observed_at": _utc_now(),
        "wrapper_result": thermal.file_reference(wrapper_result_path),
    }
    _write_json(root / "wrapper-observed-exit.json", observed)
    if completed.returncode != 0:
        raise RuntimeError(f"TD-B setup wrapper failed with exit code {completed.returncode}")
    return setup_finalize_fn(root, code_checkpoint=code_checkpoint)


def execute_plan(
    plan: Mapping[str, Any], *, run_dir: str | Path,
    apply_command_fn: Callable[[Mapping[str, Any]], Mapping[str, Any]],
    readback_fn: Callable[[Mapping[str, Any]], Mapping[str, Any]],
    capture_fn: Callable[[Mapping[str, Any]], Mapping[str, Any]],
    both_off_gate_fn: Callable[[str], Mapping[str, Any]],
    cleanup_fn: Callable[[], Mapping[str, Any]],
    bind_physical_return_observer_fn: Callable[
        [Callable[[Mapping[str, Any], Any, int], Mapping[str, Any]]],
        None,
    ] | None = None,
    set_capture_context_fn: Callable[[float], None] | None = None,
    monotonic_fn: Callable[[], float] = time.monotonic,
    monotonic_ns_fn: Callable[[], int] = time.monotonic_ns,
    sleep_fn: Callable[[float], None] = time.sleep,
) -> Path:
    validate_authorized_execution_plan(plan)
    root = Path(run_dir)
    root.mkdir(parents=True, exist_ok=True)
    if any(root.iterdir()):
        raise FileExistsError(f"thermal run directory must be empty: {root}")
    _write_json(root / "plan.json", dict(plan))
    run = {
        "schema": "p7_thermal_diagnostic_run_v2", "experiment_id": plan["experiment_id"],
        "status": "running", "started_at": _utc_now(), "completed_formal": 0,
        "ambient_capture_count": 0,
        "accepted_formal_count": 0, "accepted_ambient_count": 0,
        "physical_returned_cr3_count": 0,
        "setup_physical_cr3_count": int(plan.get("setup_physical_cr3_count", 0)),
        "physical_cr3_count": int(plan.get("setup_physical_cr3_count", 0)), "cleanup": "pending",
        "capture_settings_provenance": copy.deepcopy(plan["camera"].get("resolved_capture_settings")),
    }
    _write_json(root / "run.json", run)
    failure: BaseException | None = None
    session_start = monotonic_fn()
    previous_state: str | None = None
    previous_dwell: float | None = None
    last_observed_by_group: dict[tuple[Any, ...], float] = {}
    owned_cr3_paths: set[Path] = set()
    physical_returns_by_capture: dict[str, dict[str, Any]] = {}
    rejected_capture: dict[str, Any] | None = None

    def record_gate(gate_id: str) -> None:
        evidence = dict(both_off_gate_fn(gate_id))
        if evidence.get("status") != "pass" or evidence.get("strip_verified_off") is not True or evidence.get("ray_verified_off") is not True:
            raise RuntimeError(f"both-source off/readback gate failed: {gate_id}")
        _append_jsonl(root / "isolation-gates.jsonl", {"gate_id": gate_id, "evidence": evidence, "at": _utc_now()})

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
        *, owner_start: float | None,
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
            group = thermal.timing_sequence_identity(str(plan["experiment_id"]), step)
            previous_observed = last_observed_by_group.get(group)
            if previous_observed is not None and float(observed) <= previous_observed:
                rejected_capture["timing_evidence"] = dict(timing)
                raise RuntimeError(f"non-increasing observed chronology for {step['capture_id']}")
            last_observed_by_group[group] = float(observed)
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
        else:
            run["ambient_capture_count"] += 1
            run["accepted_ambient_count"] += 1
        rejected_capture = None
        _write_json(root / "run.json", run)

    try:
        record_gate("run_start")
        for item in _ledger_groups(str(plan["experiment_id"]), plan["captures"]):
            if len(item) == 1 and item[0]["capture_role"] == "ambient":
                step = item[0]
                record_gate(str(step["isolation_gate_before"]))
                if set_capture_context_fn is not None:
                    set_capture_context_fn(monotonic_fn())
                ensure_physical_capacity()
                retain_capture(step, dict(capture_fn(step)), owner_start=None)
                continue
            first = item[0]
            if plan["stage"] == "TD-A":
                sleep_fn(float(plan["cold_proxy_wait_s"]))
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
                retain_capture(step, dict(capture_fn(step)), owner_start=owner_start)
            previous_state = str(first["state_id"])
            previous_dwell = monotonic_fn() - owner_start
            gate_after = item[-1].get("isolation_gate_after")
            if gate_after:
                record_gate(str(gate_after))
        if run["completed_formal"] != int(plan["budgets"]["formal_cap"]):
            raise RuntimeError("thermal diagnostic formal count differs from frozen cap")
        if run["ambient_capture_count"] != int(plan["budgets"]["ambient_cap"]):
            raise RuntimeError("thermal diagnostic ambient count differs from frozen cap")
        if (
            run["accepted_formal_count"] != run["completed_formal"]
            or run["accepted_ambient_count"] != run["ambient_capture_count"]
        ):
            raise RuntimeError("thermal diagnostic accepted measurement ledger drifted")
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
        run["cleanup"] = "pass" if cleanup.get("status") in {"pass", "complete", "all_off"} or cleanup.get("ok") else "fail"
        run["finished_at"] = _utc_now()
        _write_json(root / "run.json", run)
    if failure is not None:
        raise failure
    return root


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
    actual_exposure_start_fn: Callable[[Mapping[str, Any]], float] | None = None,
) -> Path:
    validate_authorized_execution_plan(plan, camera_backend=camera_backend)
    from camera_based_rgbww_optimizer.control import all_off, esphome, ray120c
    from camera_based_rgbww_optimizer.optimization import measure_raw_observer_validation as raw_validation
    from camera_based_rgbww_optimizer.measurement.raw_observer_analysis import DEFAULT_STATISTIC
    from camera_based_rgbww_optimizer.optimization.hsi_objective import (
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
    plan = copy.deepcopy(dict(plan))
    plan["camera"] = {**dict(plan["camera"]), "resolved_capture_settings": settings_provenance}
    plan_steps_by_id = {
        str(step["capture_id"]): step for step in plan["captures"]
    }
    physical_return_observer_slot: dict[
        str,
        Callable[[Mapping[str, Any], Any, int], Mapping[str, Any]] | None,
    ] = {"callback": None}
    session_start = time.monotonic()
    load_segments: dict[str, list[tuple[float, float]]] = {"ray": [], "strip": []}

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
        load_segments[str(step["source_id"])].append((time.monotonic(), load_level(str(step["source_id"]), command)))
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
        dict(raw_validation.TD_B_FORMAL_AMBIENT_POLICY_OWNER)
        if plan["native_raw_ambient_policy"]
        == raw_validation.AMBIENT_POLICY_UNSUBTRACTED_NO_AMBIENT
        else None
    )
    exact_td_b_formal_owner = (
        plan["schema"] == thermal.PLAN_SCHEMA_V2
        and plan["experiment_id"] == thermal.TD_B
        and plan["native_raw_ambient_policy"]
        == raw_validation.AMBIENT_POLICY_UNSUBTRACTED_NO_AMBIENT
        and ambient_policy_owner == raw_validation.TD_B_FORMAL_AMBIENT_POLICY_OWNER
    )
    feature_statistic = (
        TD_B_FORMAL_FEATURE_STATISTIC
        if exact_td_b_formal_owner
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
        location_config_path=thermal.LOCATION_PATH, observer_config_path=thermal.OBSERVER_PATH,
        iso=str(resolved_settings.iso), aperture=str(resolved_settings.aperture),
        image_format=str(resolved_settings.image_format), camera_backend=camera_backend,
        recorded_exposure_purpose=str(plan["experiment_id"]),
        frozen_shutter_by_cache=plan["frozen_shutters"], timed_capture_fn=timed_capture,
        ambient_policy=str(plan["native_raw_ambient_policy"]),
        ambient_policy_owner=ambient_policy_owner,
        physical_return_observer=observe_physical_return,
    )

    def capture(step: Mapping[str, Any]) -> Mapping[str, Any]:
        source = str(step["source_id"])
        state = str(step["state_id"])
        if source == "ambient":
            cache_key = None
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
        covariate = thermal.build_covariate_record(
            source_id=source, state_id=state, command=command,
            sequence_index=int(step["capture_id"].split("-", 1)[0]),
            capture_order=int(step["capture_id"].split("-", 1)[0]),
            source_order=int(step.get("source_order", 1)), monotonic_timestamp_ns=time.monotonic_ns(),
            wall_clock_timestamp=_utc_now(), session_elapsed_s=exposure_start - session_start,
            source_on_elapsed_s=elapsed, state_on_elapsed_s=elapsed,
            off_duration_before_s=0.0, previous_state_id=None, previous_state_dwell_s=None,
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
            output["feature_values"] = required_hsi_features_from_report(
                report,
                feature_ids,
                statistic=feature_statistic,
            )
        return output

    def both_off_gate(gate_id: str) -> Mapping[str, Any]:
        from camera_based_rgbww_optimizer.optimization.hsi_source_evidence import validate_both_off

        strip = esphome.verified_light(0, 0, 0, 0, 0, curve_path=thermal.CURVE_PATH)
        ray_set = ray120c.set_cct(5600, intensity=0, gm=100)
        ray_readback = ray120c.get_cct()
        validate_both_off(strip, ray_readback, curve)
        load_segments["ray"].append((time.monotonic(), 0.0))
        load_segments["strip"].append((time.monotonic(), 0.0))
        return {
            "status": "pass", "gate_id": gate_id,
            "strip_verified_off": True, "ray_verified_off": True,
            "strip_device_evidence": dict(strip), "ray_off_command": dict(ray_set),
            "ray_readback": dict(ray_readback),
        }

    def cleanup() -> Mapping[str, Any]:
        steps = all_off.turn_everything_off(
            strip_off_fn=lambda: esphome.verified_light(0, 0, 0, 0, 0, curve_path=thermal.CURVE_PATH),
            ray_set_cct_fn=ray120c.set_cct, ray_cct=5600, ray_gm=100,
        )
        rows = [item.to_jsonable() if hasattr(item, "to_jsonable") else dict(item) for item in steps]
        return {"status": "pass" if rows and all(item.get("ok") for item in rows) else "fail", "steps": rows}

    return execute_plan(
        plan, run_dir=root, apply_command_fn=apply, readback_fn=readback,
        capture_fn=capture, both_off_gate_fn=both_off_gate, cleanup_fn=cleanup,
        bind_physical_return_observer_fn=lambda callback: physical_return_observer_slot.__setitem__(
            "callback", callback
        ),
        set_capture_context_fn=lambda value: timing_context.__setitem__("local_readback_done_monotonic_s", value),
    )


def run_resolved_td_b_formal(
    release_path: str | Path, *, output_dir: str | Path, run_name: str,
    camera_backend: Any, code_checkpoint: str,
) -> Path:
    _validate_checkpoint_and_tree(code_checkpoint)
    path = Path(release_path).resolve()
    release = json.loads(path.read_text(encoding="utf-8"))
    if release.get("schema") == thermal.TD_B_SETUP_LINEAGE_RELEASE_SCHEMA:
        validated = thermal.validate_td_b_setup_lineage_release(
            release,
            release_path=path,
        )
    else:
        validated = thermal.validate_td_b_setup_release(
            release,
            release_path=path,
        )
    if validated.get("code_checkpoint") != code_checkpoint:
        raise PermissionError("TD-B formal release checkpoint differs from current HEAD")
    plan = copy.deepcopy(validated["resolved_plan"])
    if release.get("schema") == thermal.TD_B_SETUP_LINEAGE_RELEASE_SCHEMA:
        plan["setup_lineage_release"] = thermal.file_reference(path)
    validate_authorized_execution_plan(plan, camera_backend=camera_backend)
    return run_authorized_plan(
        plan, output_dir=output_dir, run_name=run_name, camera_backend=camera_backend,
    )


def write_td_b_setup_lineage_release(
    *,
    output_dir: str | Path,
    run_name: str,
    code_checkpoint: str,
    legacy_release_path: str | Path = thermal.TD_B_SETUP_RELEASE_PATH,
    planner_candidate_path: str | Path = thermal.TD_B_F0A_LINEAGE_CANDIDATE_PATH,
    changed_paths_fn: Callable[[str, str], Sequence[str]] | None = None,
    validate_checkpoint_fn: Callable[[str], None] = _validate_checkpoint_and_tree,
) -> Path:
    """Create a production release without mutating retained setup evidence."""
    validate_checkpoint_fn(code_checkpoint)
    legacy_path = Path(legacy_release_path).resolve()
    planner_path = Path(planner_candidate_path).resolve()
    if legacy_path != thermal.TD_B_SETUP_RELEASE_PATH.resolve():
        raise PermissionError("TD-B lineage release requires the frozen legacy release owner")
    if planner_path != thermal.TD_B_F0A_LINEAGE_CANDIDATE_PATH.resolve():
        raise PermissionError("TD-B lineage release requires the accepted Planner candidate owner")
    if (
        not planner_path.is_file()
        or hashlib.sha256(planner_path.read_bytes()).hexdigest()
        != thermal.TD_B_F0A_LINEAGE_CANDIDATE_SHA256
    ):
        raise PermissionError("TD-B lineage release Planner candidate hash differs")

    root = (Path(output_dir) / run_name).resolve()
    root.parent.mkdir(parents=True, exist_ok=True)
    if root.is_symlink() or root.parent.is_symlink():
        raise PermissionError("TD-B lineage release output owner cannot be a symlink")
    if root.exists():
        if not root.is_dir() or any(root.iterdir()):
            raise FileExistsError(f"TD-B lineage release directory must be new: {root}")
    else:
        root.mkdir()

    legacy = json.loads(legacy_path.read_text(encoding="utf-8"))
    legacy_validated = thermal.validate_td_b_setup_release(
        legacy,
        release_path=legacy_path,
    )
    canonical_setup_path = Path(
        legacy_validated["canonical_path"]
    ).resolve()
    if changed_paths_fn is None:
        changed_paths = thermal.changed_paths_between_checkpoints(
            thermal.TD_B_SETUP_CHECKPOINT,
            code_checkpoint,
        )
    else:
        changed_paths = list(
            changed_paths_fn(thermal.TD_B_SETUP_CHECKPOINT, code_checkpoint)
        )
    current_candidate = thermal.build_td_b_setup_release_lineage_candidate(
        legacy_path,
        old_checkpoint=thermal.TD_B_SETUP_CHECKPOINT,
        new_checkpoint=code_checkpoint,
        changed_paths=changed_paths,
    )
    if (
        current_candidate.get("status") != "eligible_waiting_for_planner"
        or current_candidate.get("prohibited_paths") != []
    ):
        raise PermissionError("TD-B current lineage contains prohibited changes")
    current_candidate_path = root / "current-lineage-candidate.json"
    _write_json(current_candidate_path, current_candidate)

    fresh = thermal.build_diagnostic_plan(
        thermal.TD_B,
        source="ray",
        prerequisite_artifact=thermal.OPERATING_ENVELOPE_V2_PATH,
        for_execution=True,
        human_authorization=thermal.TD_B,
        v2_capture_capability=True,
    )
    resolved = thermal.resolve_td_b_plan_with_setup(
        fresh,
        setup_artifact_path=canonical_setup_path,
    )
    resolved["setup_lineage_release_required"] = True
    thermal.validate_td_b_lineage_resolved_plan(
        resolved,
        canonical_setup_path=canonical_setup_path,
    )
    resolved_path = root / "resolved-formal-plan.json"
    _write_json(resolved_path, resolved)

    release = {
        "schema": thermal.TD_B_SETUP_LINEAGE_RELEASE_SCHEMA,
        "status": "formal_plan_lineage_qualified",
        "production_release_usable": True,
        "old_checkpoint": thermal.TD_B_SETUP_CHECKPOINT,
        "code_checkpoint": code_checkpoint,
        "legacy_release": thermal.file_reference(legacy_path),
        "planner_lineage_candidate": thermal.file_reference(planner_path),
        "current_lineage_candidate": thermal.file_reference(
            current_candidate_path
        ),
        "canonical_setup": thermal.file_reference(canonical_setup_path),
        "resolved_formal_plan": thermal.file_reference(resolved_path),
    }
    release_path = root / "setup-lineage-release.json"
    _write_json(release_path, release)
    thermal.validate_td_b_setup_lineage_release(
        release,
        release_path=release_path,
        changed_paths_fn=(
            None
            if changed_paths_fn is None
            else lambda _old, _new: changed_paths
        ),
    )
    return release_path


def write_td_b_lineage_qualification_evidence(
    *,
    preparation_path: str | Path,
    output_dir: str | Path,
    run_name: str,
    code_checkpoint: str,
    release_requested: bool = False,
) -> Path:
    """Write offline qualification evidence without invoking a release owner."""
    if release_requested:
        raise PermissionError("TD-B evidence-only mode rejects release requests")
    preparation = thermal._validate_td_b_qualification_preparation_r1(
        preparation_path=preparation_path,
        code_checkpoint=code_checkpoint,
    )
    output_owner = Path(output_dir)
    root_candidate = output_owner / run_name
    if output_owner.is_symlink() or root_candidate.is_symlink():
        raise FileExistsError(
            "TD-B qualification evidence root cannot use a symlink owner"
        )
    root = root_candidate.resolve()
    if root.exists() or root.parent.is_symlink():
        raise FileExistsError(
            f"TD-B qualification evidence root must be fresh and regular: {root}"
        )
    root.parent.mkdir(parents=True, exist_ok=True)
    root.mkdir()
    successor = preparation["successor_entry"]
    closure = preparation["input_closure"]
    evidence = {
        "schema": thermal.TD_B_QUALIFICATION_EVIDENCE_SCHEMA,
        "status": thermal.TD_B_QUALIFICATION_EVIDENCE_STATUS,
        "preparation_reference": thermal.file_reference(preparation_path),
        "audit_current_head": preparation["audit_current_head"],
        "audit_current_parent": preparation["audit_current_parent"],
        "artifact_owner": {
            "artifact_owner_commit": successor["artifact_owner_commit"],
            "artifact_owner_parent": successor["artifact_owner_parent"],
            "canonical_manifest": {
                "path": successor["canonical_path"],
                "sha256": successor["canonical_sha256"],
            },
        },
        "input_references": [
            {
                "input_index": index,
                "sha256": reference["sha256"],
                "bytes": reference["bytes"],
                "owner": reference["owner"],
            }
            for index, reference in enumerate(preparation["inputs"], start=1)
        ],
        "validation_counts": {
            "unique_inputs": closure["unique_inputs"],
            "predecessor_retained_artifacts": closure[
                "predecessor_retained_artifacts"
            ],
            "changed_paths": closure["changed_paths"],
            "successor_paths": closure["successor_paths"],
            "workflow_overlap": closure["workflow_overlap"],
        },
        "failure_oracle": {
            "mismatches": closure["mismatches"],
            "prohibited_paths": closure["prohibited_paths"],
            "release_request_rejected": True,
            "side_effects_allowed": False,
        },
        "side_effect_budgets": dict(preparation["budgets"]),
    }
    evidence_path = root / "qualification-evidence.json"
    _write_json(evidence_path, evidence)
    return evidence_path


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


def _write_json_exclusive(path: Path, value: Mapping[str, Any]) -> None:
    """Create immutable JSON evidence without following an existing owner."""
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n"
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0), 0o444)
    try:
        os.write(descriptor, payload.encode("utf-8"))
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def _safe_ledger_only_subroot(root: Path, expected_parent: Path) -> Path:
    if not root.is_absolute() or root.is_symlink() or not root.is_dir():
        raise ValueError("EQ-R6 candidate root must be an existing regular directory")
    resolved = root.resolve(strict=True)
    if resolved.parent != expected_parent.resolve(strict=True):
        raise ValueError("EQ-R6 candidate root is outside its unique outer owner")
    if {path.name for path in resolved.iterdir()} != {"launch-ledger.json"}:
        raise ValueError("EQ-R6 candidate root is not a ledger-only fresh owner")
    return resolved


def write_td_b_eq_r6_launch_ledger(
    live_plan: Mapping[str, Any],
    *,
    candidate_index: int,
    candidate_root: str | Path,
    outer_pid: int,
    wrapper_pid: int,
    runner_pid: int,
    argv: Sequence[str],
) -> Path:
    """Write one immutable per-wrapper launch binding before device access."""
    thermal.validate_td_b_eq_r6_live_plan(live_plan, require_fresh_root=False)
    if candidate_index not in (1, 2):
        raise ValueError("EQ-R6 candidate index is outside the frozen contract")
    root = Path(candidate_root).resolve(strict=False)
    outer_root = Path(str(live_plan["output_root"])).resolve(strict=True)
    if root.parent != outer_root or root.name != f"candidate-{candidate_index}":
        raise ValueError("EQ-R6 launch ledger candidate owner differs")
    if (
        type(outer_pid) is not int
        or type(wrapper_pid) is not int
        or type(runner_pid) is not int
        or outer_pid <= 0
        or wrapper_pid <= 0
        or runner_pid <= 0
    ):
        raise ValueError("EQ-R6 launch ledger requires positive process IDs")
    if (
        not isinstance(argv, Sequence)
        or isinstance(argv, (str, bytes))
        or not argv
        or any(type(value) is not str for value in argv)
    ):
        raise ValueError("EQ-R6 launch argv requires an ordered string list")
    safe_argv = list(argv)
    forbidden = ("secret", "token", "password", ".env", "private")
    if any(any(term in value.lower() for term in forbidden) for value in safe_argv):
        raise ValueError("EQ-R6 launch argv contains a private parameter")
    ledger = {
        "schema": EQ_R6_LAUNCH_LEDGER_SCHEMA,
        "status": "launch_bound",
        "created_at": _utc_now(),
        "experiment_id": thermal.TD_B_EQ_R6_EXPERIMENT_ID,
        "candidate_index": candidate_index,
        "candidate_root": str(root),
        "outer_root": str(outer_root),
        "outer_pid": int(outer_pid),
        "wrapper_pid": int(wrapper_pid),
        "runner_pid": int(runner_pid),
        "code_checkpoint": live_plan["code_checkpoint"],
        "offline_plan_sha256": live_plan["offline_plan_sha256"],
        "exposure_policy": dict(live_plan["exposure_policy"]),
        "thermal_contract": dict(live_plan["thermal_contract"]),
        "measurement_runner": dict(live_plan["measurement_runner"]),
        "production_wrapper": dict(live_plan["production_wrapper"]),
        "argv": safe_argv,
    }
    path = root / "launch-ledger.json"
    _write_json_exclusive(path, ledger)
    return path


def _validate_td_b_eq_r6_launch_ledger(
    ledger: Mapping[str, Any],
    live_plan: Mapping[str, Any],
    *,
    candidate_index: int,
    candidate_root: Path,
    expected_outer_pid: int,
    expected_wrapper_pid: int,
    expected_runner_pid: int,
    expected_argv: Sequence[str],
) -> None:
    expected_keys = {
        "schema", "status", "created_at", "experiment_id", "candidate_index",
        "candidate_root", "outer_root", "outer_pid", "wrapper_pid", "runner_pid",
        "code_checkpoint", "offline_plan_sha256", "exposure_policy",
        "thermal_contract", "measurement_runner", "production_wrapper", "argv",
    }
    if set(ledger) != expected_keys:
        raise PermissionError("EQ-R6 launch ledger schema differs")
    safe_argv = ledger.get("argv")
    expected_pids = (
        expected_outer_pid,
        expected_wrapper_pid,
        expected_runner_pid,
    )
    if (
        any(type(value) is not int or value <= 0 for value in expected_pids)
        or not isinstance(expected_argv, Sequence)
        or isinstance(expected_argv, (str, bytes))
        or not expected_argv
        or any(type(value) is not str for value in expected_argv)
    ):
        raise PermissionError("EQ-R6 expected runtime binding is invalid")
    forbidden = ("secret", "token", "password", ".env", "private")
    if (
        ledger.get("schema") != EQ_R6_LAUNCH_LEDGER_SCHEMA
        or ledger.get("status") != "launch_bound"
        or ledger.get("experiment_id") != thermal.TD_B_EQ_R6_EXPERIMENT_ID
        or ledger.get("candidate_index") != candidate_index
        or ledger.get("candidate_root") != str(candidate_root.resolve())
        or ledger.get("outer_root") != str(
            Path(str(live_plan["output_root"])).resolve()
        )
        or type(ledger.get("outer_pid")) is not int
        or ledger.get("outer_pid") != expected_outer_pid
        or type(ledger.get("wrapper_pid")) is not int
        or ledger.get("wrapper_pid") != expected_wrapper_pid
        or type(ledger.get("runner_pid")) is not int
        or ledger.get("runner_pid") != expected_runner_pid
        or ledger.get("code_checkpoint") != live_plan["code_checkpoint"]
        or ledger.get("offline_plan_sha256") != live_plan["offline_plan_sha256"]
        or ledger.get("exposure_policy") != live_plan["exposure_policy"]
        or ledger.get("thermal_contract") != live_plan["thermal_contract"]
        or ledger.get("measurement_runner") != live_plan["measurement_runner"]
        or ledger.get("production_wrapper") != live_plan["production_wrapper"]
        or not isinstance(safe_argv, list)
        or not safe_argv
        or any(type(value) is not str for value in safe_argv)
        or safe_argv != list(expected_argv)
        or any(
            any(term in str(value).lower() for term in forbidden)
            for value in safe_argv
        )
    ):
        raise PermissionError("EQ-R6 launch ledger binding differs")


def _validated_eq_physical_return(
    root: Path,
    request: Mapping[str, Any],
    returned: Mapping[str, Any],
    *,
    physical_index: int,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Persist a verified physical return before reading its quality payload."""
    capture_id = str(request["capture_id"])
    raw_candidate = Path(str(returned.get("saved_file", "")))
    raw_path = raw_candidate.resolve(strict=False)
    row = {
        "schema": thermal.PHYSICAL_RETURN_LEDGER_SCHEMA,
        "physical_index": physical_index,
        "capture_id": capture_id,
        "source_id": "ray",
        "state_id": "C",
        "cr3_path": str(raw_path),
        "cr3_byte_count": None,
        "cr3_sha256": None,
        "sidecar_path": None,
        "sidecar_byte_count": None,
        "sidecar_sha256": None,
        "sidecar_validation_status": "pending",
        "remote_capture_id": None,
        "remote_request_id": None,
        "returned_at": _utc_now(),
        "accepted_measurement": False,
    }
    if (
        raw_candidate.is_symlink()
        or not raw_path.is_relative_to(root)
        or not raw_path.is_file()
        or raw_path.stat().st_size <= 0
    ):
        _append_jsonl(root / "physical-returns.jsonl", row)
        raise RuntimeError("EQ-R6 return lacks a retained current-candidate CR3")
    payload = raw_path.read_bytes()
    row.update({
        "cr3_byte_count": len(payload),
        "cr3_sha256": hashlib.sha256(payload).hexdigest(),
    })
    association_error: BaseException | None = None
    try:
        sidecar = _validate_returned_sidecar(
            returned, raw_path=raw_path, raw_payload=payload, run_root=root,
        )
    except _SidecarAssociationError as exc:
        sidecar = dict(exc.evidence)
        association_error = exc
    row.update(sidecar)
    _append_jsonl(root / "physical-returns.jsonl", row)
    if association_error is not None:
        raise association_error
    receipt = {
        "physical_return_persisted_before_postprocessing": True,
        "cr3": {
            "path": row["cr3_path"],
            "bytes": row["cr3_byte_count"],
            "sha256": row["cr3_sha256"],
        },
        "sidecar": {
            "path": row["sidecar_path"],
            "bytes": row["sidecar_byte_count"],
            "sha256": row["sidecar_sha256"],
        },
        "remote_capture_id": row["remote_capture_id"],
        "remote_request_id": row["remote_request_id"],
    }
    return row, receipt


def _select_eq_r6_policy_observations(
    observations: Sequence[Mapping[str, Any]],
    policy_feature_ids: Sequence[str],
) -> tuple[Mapping[str, Any], ...]:
    """Select complete RAW observations in the exact frozen EQ-R6 policy order."""
    if (
        not isinstance(policy_feature_ids, Sequence)
        or isinstance(policy_feature_ids, (str, bytes))
        or len(policy_feature_ids) != 58
        or any(
            type(feature_id) is not str or not feature_id.strip()
            for feature_id in policy_feature_ids
        )
        or len(set(policy_feature_ids)) != len(policy_feature_ids)
    ):
        raise ValueError("EQ-R6 policy feature IDs must be 58 unique non-empty strings")
    if (
        not isinstance(observations, Sequence)
        or isinstance(observations, (str, bytes))
    ):
        raise ValueError("EQ-R6 RAW observations must be a sequence")

    by_id: dict[str, Mapping[str, Any]] = {}
    for index, observation in enumerate(observations):
        if not isinstance(observation, Mapping):
            raise ValueError(f"EQ-R6 RAW observation {index} is not an object")
        feature_id = observation.get("feature_id")
        if type(feature_id) is not str or not feature_id.strip():
            raise ValueError(
                f"EQ-R6 RAW observation {index} lacks a non-empty feature ID"
            )
        if feature_id in by_id:
            raise ValueError(
                f"EQ-R6 RAW observations contain duplicate feature ID: {feature_id}"
            )
        by_id[feature_id] = observation

    missing = [
        feature_id for feature_id in policy_feature_ids if feature_id not in by_id
    ]
    if missing:
        raise ValueError(
            "EQ-R6 RAW observations are missing required feature IDs: "
            + ", ".join(missing)
        )
    selected = tuple(by_id[feature_id] for feature_id in policy_feature_ids)
    if (
        len(selected) != 58
        or tuple(item["feature_id"] for item in selected)
        != tuple(policy_feature_ids)
    ):
        raise RuntimeError("EQ-R6 selected RAW feature order differs from policy")
    return selected


def _count_eq_r6_physical_returns(candidate_root: str | Path) -> int:
    """Strictly recount one candidate's authoritative physical-return ledger."""
    root = Path(candidate_root).resolve(strict=True)
    ledger_path = root / "physical-returns.jsonl"
    if ledger_path.is_symlink():
        raise ValueError("EQ-R6 physical-return ledger is unsafe")
    if not ledger_path.exists():
        return 0
    if (
        not ledger_path.is_file()
        or not ledger_path.resolve(strict=True).is_relative_to(root)
    ):
        raise ValueError("EQ-R6 physical-return ledger is unsafe")

    rows: list[Mapping[str, Any]] = []
    capture_ids: set[str] = set()
    for line_number, line in enumerate(
        ledger_path.read_text(encoding="utf-8").splitlines(),
        start=1,
    ):
        if not line:
            continue
        try:
            row = json.loads(
                line,
                parse_constant=lambda value: (_ for _ in ()).throw(
                    ValueError(f"non-finite JSON constant: {value}")
                ),
            )
        except (json.JSONDecodeError, ValueError) as exc:
            raise ValueError(
                f"EQ-R6 physical-return ledger line {line_number} is invalid JSON"
            ) from exc
        if not isinstance(row, Mapping):
            raise ValueError(
                f"EQ-R6 physical-return ledger line {line_number} is not an object"
            )
        expected_index = len(rows) + 1
        physical_index = row.get("physical_index")
        if type(physical_index) is not int or physical_index != expected_index:
            raise ValueError(
                "EQ-R6 physical-return ledger indices are not contiguous from 1"
            )
        capture_id = row.get("capture_id")
        if type(capture_id) is not str or not capture_id.strip():
            raise ValueError(
                f"EQ-R6 physical-return ledger line {line_number} lacks capture_id"
            )
        if capture_id in capture_ids:
            raise ValueError(
                f"EQ-R6 physical-return ledger duplicates capture_id: {capture_id}"
            )
        capture_ids.add(capture_id)
        rows.append(row)
    return len(rows)


def run_td_b_eq_r6_single_candidate(
    live_plan: Mapping[str, Any],
    *,
    candidate_index: int,
    candidate_root: str | Path,
    strip_zero_fn: Callable[[], Mapping[str, Any]],
    ray_a_fn: Callable[[], Mapping[str, Any]],
    ray_c_fn: Callable[[], Mapping[str, Any]],
    capture_fn: Callable[[Mapping[str, Any]], Mapping[str, Any]],
    python_cleanup_fn: Callable[[], Mapping[str, Any]],
    runtime_outer_pid: int,
    runtime_wrapper_pid: int,
    runtime_runner_pid: int,
    runtime_argv: Sequence[str],
    bind_physical_return_observer_fn: Callable[
        [Callable[[Mapping[str, Any], Mapping[str, Any], int], Mapping[str, Any]]],
        None,
    ] | None = None,
    sleep_fn: Callable[[float], None] = time.sleep,
    monotonic_fn: Callable[[], float] = time.monotonic,
) -> Path:
    """Execute exactly one EQ candidate inside one wrapper-owned lifecycle."""
    thermal.validate_td_b_eq_r6_live_plan(live_plan, require_fresh_root=False)
    outer_root = Path(str(live_plan["output_root"])).resolve(strict=True)
    root = _safe_ledger_only_subroot(Path(candidate_root), outer_root)
    if candidate_index not in (1, 2):
        raise ValueError("EQ-R6 candidate index is outside the frozen contract")
    candidate = dict(live_plan["offline_plan"]["candidates"][candidate_index - 1])
    ledger_path = root / "launch-ledger.json"
    if not ledger_path.is_file() or ledger_path.is_symlink():
        raise PermissionError("EQ-R6 candidate device entry requires its immutable launch ledger")
    ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
    _validate_td_b_eq_r6_launch_ledger(
        ledger,
        live_plan,
        candidate_index=candidate_index,
        candidate_root=root,
        expected_outer_pid=runtime_outer_pid,
        expected_wrapper_pid=runtime_wrapper_pid,
        expected_runner_pid=runtime_runner_pid,
        expected_argv=runtime_argv,
    )
    _write_json(root / "candidate-plan.json", {
        "schema": "p7_td_b_eq_r6_candidate_plan_v1",
        "candidate_index": candidate_index,
        "candidate": candidate,
        "live_plan_sha256": thermal.canonical_sha256(live_plan),
    })
    feature_ids = tuple(
        json.loads(thermal.POLICY_PATH.read_text(encoding="utf-8"))["feature_set"]["ids"]
    )
    captures: list[dict[str, Any]] = []
    attempted = 0
    physical_returned = 0
    accepted = 0
    classification = "candidate_failed"
    failure: BaseException | None = None
    cleanup: dict[str, Any] = {"status": "not_run"}
    physical_by_capture: dict[str, tuple[dict[str, Any], dict[str, Any]]] = {}

    def observe_physical_return(
        request: Mapping[str, Any],
        returned: Mapping[str, Any],
        reported_physical: int,
    ) -> Mapping[str, Any]:
        if reported_physical != 1:
            raise RuntimeError("EQ-R6 capture returned a non-unit physical count")
        capture_id = str(request["capture_id"])
        if capture_id in physical_by_capture:
            raise RuntimeError("EQ-R6 capture duplicated a physical return owner")
        physical_by_capture[capture_id] = _validated_eq_physical_return(
            root, request, returned, physical_index=len(physical_by_capture) + 1,
        )
        return dict(physical_by_capture[capture_id][1])

    if bind_physical_return_observer_fn is not None:
        bind_physical_return_observer_fn(observe_physical_return)
    try:
        strip_zero = dict(strip_zero_fn())
        if strip_zero.get("status") != "pass" or strip_zero.get("generation_bearing_zero") is not True:
            raise RuntimeError("EQ-R6 strip zero precondition failed")
        _append_jsonl(root / "progressive-events.jsonl", {
            "event": "strip_zero_verified", "at": _utc_now(), "evidence": strip_zero,
        })
        ray_a = dict(ray_a_fn())
        if ray_a.get("status") != "pass":
            raise RuntimeError("EQ-R6 Ray A command/readback failed")
        _append_jsonl(root / "progressive-events.jsonl", {
            "event": "ray_a_on", "at": _utc_now(), "evidence": ray_a,
        })
        sleep_fn(600.0)
        ray_c = dict(ray_c_fn())
        if ray_c.get("status") != "pass":
            raise RuntimeError("EQ-R6 Ray C command/readback failed")
        _append_jsonl(root / "progressive-events.jsonl", {
            "event": "ray_a_to_c", "at": _utc_now(), "evidence": ray_c,
        })
        c_started = monotonic_fn()
        for capture_id, slot_s in zip(candidate["capture_ids"], candidate["slots_s"], strict=True):
            if attempted >= 4:
                raise RuntimeError("EQ-R6 candidate physical cap exhausted")
            request = {
                "candidate_index": candidate_index,
                "capture_id": capture_id,
                "requested_elapsed_s": slot_s,
                "nominal_shutter": candidate["nominal_shutter"],
            }
            remaining = float(slot_s) - (monotonic_fn() - c_started)
            if remaining > 0:
                sleep_fn(remaining)
            attempted += 1
            _append_jsonl(root / "capture-attempts.jsonl", {
                **request, "attempt_index": attempted, "attempted_at": _utc_now(),
            })
            returned = dict(capture_fn(request))
            physical, receipt = physical_by_capture.get(capture_id, (None, None))
            if physical is None or receipt is None:
                physical, receipt = _validated_eq_physical_return(
                    root, request, returned, physical_index=physical_returned + 1,
                )
            physical_returned += 1
            quality_payload = returned.get("quality_capture")
            if not isinstance(quality_payload, Mapping):
                raise RuntimeError("EQ-R6 capture adapter lacks a quality payload")
            row = {**dict(quality_payload), **receipt}
            if (
                row.get("capture_id") != capture_id
                or row.get("requested_elapsed_s", slot_s) != slot_s
                or row.get("nominal_shutter", candidate["nominal_shutter"])
                != candidate["nominal_shutter"]
            ):
                raise RuntimeError("EQ-R6 capture adapter returned a different frozen slot")
            failures = thermal.td_b_eq_capture_quality_failures(
                row, required_feature_ids=feature_ids,
            )
            physical["accepted_measurement"] = not failures
            captures.append(row)
            if not failures:
                accepted += 1
            _append_jsonl(root / "capture-results.jsonl", {
                "capture_id": capture_id,
                "failures": list(failures),
                "accepted": not failures,
                "physical_return": physical,
                "quality_capture": row,
                "processed_at": _utc_now(),
            })
            if failures:
                classification = (
                    "clipping_only" if set(failures) == {"clipping"} else "invalid"
                )
                break
        else:
            classification = "candidate_pass"
    except BaseException as exc:
        failure = exc
    finally:
        try:
            cleanup = dict(python_cleanup_fn())
        except BaseException as cleanup_exc:
            cleanup = {
                "status": "fail",
                "exception_type": type(cleanup_exc).__name__,
                "message": str(cleanup_exc),
            }
            if failure is None:
                failure = cleanup_exc
        _write_json(root / "all-off-python.json", cleanup)
        if cleanup.get("status") != "pass" and failure is None:
            failure = RuntimeError("EQ-R6 Python cleanup failed")
    physical_returned = _count_eq_r6_physical_returns(root)
    if failure is not None:
        _write_json(root / "candidate-failure.json", {
            "schema": "p7_td_b_eq_r6_candidate_failure_v1",
            "status": "failed",
            "exception_type": type(failure).__name__,
            "message": str(failure),
            "attempted": attempted,
            "physical_returned": physical_returned,
            "accepted": accepted,
        })
    result = {
        "schema": EQ_R6_CANDIDATE_RESULT_SCHEMA,
        "status": "complete" if failure is None else "failed",
        "candidate_index": candidate_index,
        "nominal_shutter": candidate["nominal_shutter"],
        "classification": classification if failure is None else "candidate_failed",
        "captures": captures,
        "attempted_capture_calls": attempted,
        "physical_returned_cr3_count": physical_returned,
        "accepted_capture_count": accepted,
        "python_cleanup": cleanup,
        "runtime_binding": {
            "outer_pid": runtime_outer_pid,
            "wrapper_pid": runtime_wrapper_pid,
            "runner_pid": runtime_runner_pid,
            "argv": list(runtime_argv),
        },
        "retry": 0,
        "completed_at": _utc_now(),
    }
    _write_json(root / "candidate-result.json", result)
    if failure is not None:
        raise RuntimeError("EQ-R6 single candidate failed") from failure
    return root / "candidate-result.json"


def run_td_b_eq_r6_production_candidate(
    live_plan: Mapping[str, Any],
    *,
    candidate_index: int,
    candidate_root: str | Path,
    camera_backend: Any,
    runtime_outer_pid: int,
    runtime_wrapper_pid: int,
    runtime_runner_pid: int,
    runtime_argv: Sequence[str],
) -> Path:
    """Bind the single-candidate owner to the existing real device adapters."""
    thermal.validate_td_b_eq_r6_live_plan(live_plan, require_fresh_root=False)
    from camera_based_rgbww_optimizer.control import all_off, esphome, ray120c
    from camera_based_rgbww_optimizer.measurement.raw_observer_analysis import (
        collect_patch_plane_features,
    )
    from camera_based_rgbww_optimizer.measurement.recorded_exposure import (
        parse_nominal_exposure,
    )
    from camera_based_rgbww_optimizer.optimization.hsi_objective import (
        TD_B_FORMAL_FEATURE_STATISTIC,
    )
    from camera_based_rgbww_optimizer.optimization.measure_ray_hsi_manifold import (
        _verify_readback,
    )

    root = Path(candidate_root).resolve(strict=True)
    candidate = live_plan["offline_plan"]["candidates"][candidate_index - 1]
    feature_ids = tuple(
        json.loads(thermal.POLICY_PATH.read_text(encoding="utf-8"))["feature_set"]["ids"]
    )
    connection = camera_backend.connect()
    resolved_settings, _ = _resolve_remote_capture_settings(camera_backend)
    timing_context: dict[str, float | None] = {
        "local_readback_done_monotonic_s": None,
    }
    physical_observer: dict[str, Callable[..., Mapping[str, Any]] | None] = {
        "callback": None,
    }
    current_request: dict[str, Any] = {}

    def timed_capture(**kwargs: Any) -> Any:
        if timing_context["local_readback_done_monotonic_s"] is None:
            raise RuntimeError("EQ-R6 timing context lacks Ray C readback completion")
        method = getattr(camera_backend, "capture_with_timing", None)
        if not callable(method):
            raise PermissionError("EQ-R6 requires the remote-v2 timing backend")
        return method(
            output_dir=kwargs["output_dir"],
            filename_template=kwargs["filename_template"],
            settings=kwargs["settings"],
            connection=connection,
            local_readback_done_monotonic_s=float(
                timing_context["local_readback_done_monotonic_s"]
            ),
        )

    def observe_return(returned: Any, _raw_step: Mapping[str, Any], count: int) -> Mapping[str, Any]:
        callback = physical_observer["callback"]
        if callback is None:
            raise RuntimeError("EQ-R6 physical return owner is not bound")
        payload = (
            returned.to_jsonable()
            if hasattr(returned, "to_jsonable")
            else dict(returned)
        )
        return callback(current_request, payload, count)

    raw_capture = raw_validation.build_native_raw_capture_step_fn(
        camera_dir=root / "camera",
        measurements_dir=root / "measurements",
        scratch_dir=root / "scratch",
        location_config_path=thermal.LOCATION_PATH,
        observer_config_path=thermal.OBSERVER_PATH,
        iso=str(resolved_settings.iso),
        aperture=str(resolved_settings.aperture),
        image_format=str(resolved_settings.image_format),
        camera_backend=camera_backend,
        recorded_exposure_purpose=thermal.TD_B_EQ_R6_EXPERIMENT_ID,
        frozen_shutter_by_cache={
            "ray-h0-s0": str(candidate["nominal_shutter"]),
        },
        timed_capture_fn=timed_capture,
        ambient_policy=raw_validation.AMBIENT_POLICY_UNSUBTRACTED_NO_AMBIENT,
        ambient_policy_owner=dict(raw_validation.TD_B_FORMAL_AMBIENT_POLICY_OWNER),
        physical_return_observer=observe_return,
    )

    def strip_zero() -> Mapping[str, Any]:
        evidence = esphome.verified_light(
            0, 0, 0, 0, 0, curve_path=thermal.CURVE_PATH,
        )
        return {
            "status": "pass",
            "generation_bearing_zero": True,
            "strip_device_evidence": dict(evidence),
        }

    def set_ray(state: str) -> Mapping[str, Any]:
        command = dict(thermal.RAY_STATES[state])
        response = ray120c.set_hsi(
            int(command["hue"]),
            int(command["sat"]),
            intensity_percent=float(command["intensity_percent"]),
        )
        readback = ray120c.get_hsi()
        _verify_readback(
            readback,
            {
                "hue": int(command["hue"]),
                "sat": int(command["sat"]),
                "intensity": ray120c.intensity_percent_to_raw(
                    float(command["intensity_percent"])
                ),
            },
            mode="hsi",
        )
        timing_context["local_readback_done_monotonic_s"] = time.monotonic()
        return {
            "status": "pass",
            "command": command,
            "response": dict(response),
            "readback": dict(readback),
        }

    def capture(request: Mapping[str, Any]) -> Mapping[str, Any]:
        current_request.clear()
        current_request.update(dict(request))
        captured = dict(raw_capture({
            "capture_id": request["capture_id"],
            "source": "ray",
            "purpose": f"p7_td_b_eq_r6_c{candidate_index}",
            "repeat_index": int(request["capture_id"].split("-", 1)[0]),
            "source_exposure_cache": "ray-h0-s0",
            "auto_exposure": False,
            "physical_capture_budget_remaining": 4,
            "analysis_context": {
                "phase": "eq_r6",
                "formal_measurement": False,
                "native_raw_ambient_policy":
                    raw_validation.AMBIENT_POLICY_UNSUBTRACTED_NO_AMBIENT,
            },
        }))
        report = json.loads(
            Path(str(captured["patch_statistics"])).read_text(encoding="utf-8")
        )
        collection = collect_patch_plane_features(
            [report], statistic=TD_B_FORMAL_FEATURE_STATISTIC,
        )
        selected_observations = _select_eq_r6_policy_observations(
            collection["observations"],
            feature_ids,
        )
        observations = {
            str(item["feature_id"]): item for item in selected_observations
        }
        if tuple(observations) != feature_ids:
            raise RuntimeError("EQ-R6 selected RAW feature order differs")
        exposure = dict(report["exposure_metadata"])
        nominal_seconds = parse_nominal_exposure(str(candidate["nominal_shutter"]))
        recorded_seconds = float(exposure.get("seconds", 0.0))
        ratio_ok = (
            recorded_seconds > 0
            and 0.8 <= recorded_seconds / nominal_seconds <= 1.2
        )
        capture_payload = dict(captured.get("capture") or {})
        output = {
            **captured,
            **capture_payload,
            "saved_file": capture_payload["saved_file"],
            "quality_capture": {
                "capture_id": request["capture_id"],
                "requested_elapsed_s": request["requested_elapsed_s"],
                "nominal_shutter": candidate["nominal_shutter"],
                "recorded_exposure": exposure,
                "nominal_recorded_ratio_gate": "pass" if ratio_ok else "fail",
                "ray_command_readback": "pass",
                "strip_zero": "pass",
                "source_isolation": "pass",
                "timing_chronology": (
                    "pass" if isinstance(captured.get("timing_evidence"), Mapping)
                    else "fail"
                ),
                "no_stale": "pass",
                "budget_accounting": "pass",
                "feature_quality": {
                    feature_id: {
                        "value": observations[feature_id]["value"],
                        "clipped_fraction": observations[feature_id]["metrics"][
                            "clipped_fraction"
                        ],
                        "near_noise_floor_fraction": observations[feature_id]["metrics"][
                            "near_noise_floor_fraction"
                        ],
                        "valid_pixel_count": observations[feature_id]["metrics"][
                            "valid_pixel_count"
                        ],
                    }
                    for feature_id in feature_ids
                },
            },
        }
        return output

    def cleanup() -> Mapping[str, Any]:
        steps = all_off.turn_everything_off(
            strip_off_fn=lambda: esphome.verified_light(
                0, 0, 0, 0, 0, curve_path=thermal.CURVE_PATH,
            ),
            ray_set_cct_fn=ray120c.set_cct,
            ray_cct=5600,
            ray_gm=100,
        )
        rows = [
            item.to_jsonable() if hasattr(item, "to_jsonable") else dict(item)
            for item in steps
        ]
        return {
            "status": "pass" if rows and all(row.get("ok") for row in rows) else "fail",
            "steps": rows,
        }

    return run_td_b_eq_r6_single_candidate(
        live_plan,
        candidate_index=candidate_index,
        candidate_root=root,
        strip_zero_fn=strip_zero,
        ray_a_fn=lambda: set_ray("A"),
        ray_c_fn=lambda: set_ray("C"),
        capture_fn=capture,
        python_cleanup_fn=cleanup,
        runtime_outer_pid=runtime_outer_pid,
        runtime_wrapper_pid=runtime_wrapper_pid,
        runtime_runner_pid=runtime_runner_pid,
        runtime_argv=runtime_argv,
        bind_physical_return_observer_fn=lambda callback: physical_observer.__setitem__(
            "callback", callback,
        ),
    )


def _default_eq_final_zero() -> Mapping[str, Any]:
    from camera_based_rgbww_optimizer.control import esphome, ray120c
    from camera_based_rgbww_optimizer.optimization.hsi_source_evidence import validate_both_off

    curve = json.loads(thermal.CURVE_PATH.read_text(encoding="utf-8"))
    strip = esphome.verified_light(0, 0, 0, 0, 0, curve_path=thermal.CURVE_PATH)
    ray120c.set_cct(5600, intensity=0, gm=100)
    ray = ray120c.get_cct()
    validate_both_off(strip, ray, curve)
    return {
        "status": "pass",
        "strip_verified_off": True,
        "ray_verified_off": True,
        "strip_device_evidence": dict(strip),
        "ray_readback": dict(ray),
    }


def _reference(path: Path) -> dict[str, Any]:
    if path.is_symlink() or not path.is_file():
        raise ValueError(f"unsafe or missing EQ-R6 artifact: {path.name}")
    return {
        "path": str(path.resolve()),
        "bytes": path.stat().st_size,
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
    }


def _load_regular_json(path: Path) -> dict[str, Any]:
    if path.is_symlink() or not path.is_file():
        raise ValueError(f"unsafe or missing EQ-R6 artifact: {path.name}")
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"EQ-R6 artifact is not a JSON object: {path.name}")
    return value


def _eq_r6_exact_child_argv(
    live_plan: Mapping[str, Any],
    *,
    candidate_index: int,
    live_plan_path: Path,
    outer_pid: int,
) -> list[str]:
    candidate_root = (
        Path(str(live_plan["output_root"])).resolve()
        / f"candidate-{candidate_index}"
    )
    return [
        "--execute",
        "--allow-device-control",
        "--output-dir",
        str(candidate_root.parent),
        "--run-name",
        candidate_root.name,
        "--eq-r6-single-candidate",
        str(candidate_index),
        "--eq-r6-live-plan",
        str(live_plan_path.resolve()),
        "--eq-r6-outer-pid",
        str(outer_pid),
        "--code-checkpoint",
        str(live_plan["code_checkpoint"]),
        "--experiment-id",
        thermal.TD_B,
        "--source",
        "ray",
        "--phase",
        "formal",
        "--human-authorization",
        thermal.TD_B_EQ_R6_EXPERIMENT_ID,
    ]


def _seal_eq_candidate(
    live_plan: Mapping[str, Any],
    *,
    candidate_index: int,
    root: Path,
    wrapper_return_code: int,
    final_zero: Mapping[str, Any],
    expected_outer_pid: int,
    expected_child_argv: Sequence[str],
) -> dict[str, Any]:
    wrapper_path = root / "wrapper-result.json"
    result_path = root / "candidate-result.json"
    wrapper = _load_regular_json(wrapper_path)
    result = _load_regular_json(result_path)
    launch = _load_regular_json(root / "launch-ledger.json")
    wrapper_keys = {
        "schema_version",
        "experiment",
        "status",
        "run_dir",
        "wrapper_pid",
        "child_pid",
        "child_exit_code",
        "shell_cleanup_exit_code",
        "wrapper_exit_code",
        "signal",
        "started_at",
    }
    result_keys = {
        "schema",
        "status",
        "candidate_index",
        "nominal_shutter",
        "classification",
        "captures",
        "attempted_capture_calls",
        "physical_returned_cr3_count",
        "accepted_capture_count",
        "python_cleanup",
        "runtime_binding",
        "retry",
        "completed_at",
    }
    if set(wrapper) != wrapper_keys:
        raise PermissionError("EQ-R6 wrapper result schema differs")
    if set(result) != result_keys:
        raise PermissionError("EQ-R6 candidate result schema differs")
    wrapper_pid = wrapper.get("wrapper_pid")
    child_pid = wrapper.get("child_pid")
    if (
        type(wrapper_pid) is not int
        or wrapper_pid <= 0
        or type(child_pid) is not int
        or child_pid <= 0
        or wrapper.get("run_dir") != str(root.resolve())
    ):
        raise PermissionError("EQ-R6 wrapper runtime ownership differs")
    _validate_td_b_eq_r6_launch_ledger(
        launch,
        live_plan,
        candidate_index=candidate_index,
        candidate_root=root,
        expected_outer_pid=expected_outer_pid,
        expected_wrapper_pid=wrapper_pid,
        expected_runner_pid=child_pid,
        expected_argv=expected_child_argv,
    )
    runtime = result.get("runtime_binding")
    if (
        not isinstance(runtime, dict)
        or set(runtime)
        != {"outer_pid", "wrapper_pid", "runner_pid", "argv"}
        or runtime.get("outer_pid") != expected_outer_pid
        or runtime.get("wrapper_pid") != wrapper_pid
        or runtime.get("runner_pid") != child_pid
        or runtime.get("argv") != list(expected_child_argv)
    ):
        raise PermissionError("EQ-R6 candidate runtime ownership differs")
    shell_path = root / "all-off-shell.json"
    if shell_path.is_symlink() or not shell_path.is_file():
        raise ValueError("unsafe or missing EQ-R6 artifact: all-off-shell.json")
    shell = json.loads(shell_path.read_text(encoding="utf-8"))
    successful = (
        wrapper_return_code == 0
        and wrapper.get("status") == "complete"
        and wrapper.get("child_exit_code") == 0
        and wrapper.get("shell_cleanup_exit_code") == 0
        and wrapper.get("wrapper_exit_code") == 0
        and wrapper.get("signal") is None
        and result.get("status") == "complete"
        and result.get("python_cleanup", {}).get("status") == "pass"
        and isinstance(shell, list)
        and bool(shell)
        and all(isinstance(row, Mapping) and row.get("ok") is True for row in shell)
        and final_zero.get("status") == "pass"
        and final_zero.get("strip_verified_off") is True
        and final_zero.get("ray_verified_off") is True
    )
    canonical = [
        _reference(path)
        for path in (
            root / "launch-ledger.json",
            root / "candidate-plan.json",
            root / "candidate-result.json",
            root / "all-off-python.json",
            root / "all-off-shell.json",
            root / "wrapper-result.json",
            root / "independent-final-zero.json",
        )
    ]
    seal = {
        "schema": EQ_R6_TERMINAL_SEAL_SCHEMA,
        "status": "pass" if successful else "fail",
        "candidate_index": candidate_index,
        "classification": result.get("classification"),
        "attempted_capture_calls": result.get("attempted_capture_calls"),
        "physical_returned_cr3_count": result.get("physical_returned_cr3_count"),
        "accepted_capture_count": result.get("accepted_capture_count"),
        "wrapper_return_code": wrapper_return_code,
        "code_checkpoint": live_plan["code_checkpoint"],
        "offline_plan_sha256": live_plan["offline_plan_sha256"],
        "exposure_policy": dict(live_plan["exposure_policy"]),
        "thermal_contract": dict(live_plan["thermal_contract"]),
        "measurement_runner": dict(live_plan["measurement_runner"]),
        "production_wrapper": dict(live_plan["production_wrapper"]),
        "runtime_binding": {
            "outer_pid": expected_outer_pid,
            "wrapper_pid": wrapper_pid,
            "runner_pid": child_pid,
            "argv": list(expected_child_argv),
            "launch_ledger": _reference(root / "launch-ledger.json"),
            "wrapper_result": _reference(wrapper_path),
            "candidate_result": _reference(result_path),
        },
        "canonical_artifacts": canonical,
        "sealed_at": _utc_now(),
    }
    _write_json(root / "terminal-seal.json", seal)
    return seal


def orchestrate_td_b_eq_r6(
    live_plan: Mapping[str, Any],
    *,
    run_fn: Callable[..., subprocess.CompletedProcess[Any]] = subprocess.run,
    final_zero_fn: Callable[[], Mapping[str, Any]] = _default_eq_final_zero,
    outer_pid: int | None = None,
) -> Path:
    """Own the one-or-two wrapper sequence and the clipping-only unlock."""
    thermal.validate_td_b_eq_r6_live_plan(live_plan, require_fresh_root=True)
    root = Path(str(live_plan["output_root"]))
    root.mkdir(parents=True, mode=0o700)
    live_plan_path = root / "live-plan.json"
    _write_json(live_plan_path, dict(live_plan))
    results: list[list[dict[str, Any]]] = []
    seals: list[dict[str, Any]] = []
    launches: list[dict[str, Any]] = []
    outer_terminals: list[dict[str, Any]] = []
    feature_ids = tuple(
        json.loads(thermal.POLICY_PATH.read_text(encoding="utf-8"))["feature_set"]["ids"]
    )
    final_status = "failed"
    frozen_outer_pid = outer_pid if outer_pid is not None else os.getpid()
    if type(frozen_outer_pid) is not int or frozen_outer_pid <= 0:
        raise ValueError("EQ-R6 outer owner requires a positive non-bool PID")

    def exception_record(exc: BaseException | None) -> dict[str, Any] | None:
        if exc is None:
            return None
        return {
            "exception_type": type(exc).__name__,
            "message": str(exc),
        }

    try:
        for candidate_index in (1, 2):
            if candidate_index == 2:
                first_failures = [
                    thermal.td_b_eq_capture_quality_failures(
                        row, required_feature_ids=feature_ids,
                    )
                    for row in results[0]
                ]
                first_bad = next((failure for failure in first_failures if failure), None)
                if (
                    first_bad is None
                    or set(first_bad) != {"clipping"}
                    or seals[0].get("status") != "pass"
                ):
                    break
            candidate_root = root / f"candidate-{candidate_index}"
            expected_child_argv = _eq_r6_exact_child_argv(
                live_plan,
                candidate_index=candidate_index,
                live_plan_path=live_plan_path,
                outer_pid=frozen_outer_pid,
            )
            wrapper_argv = expected_child_argv[6:]
            command = [
                "zsh",
                str(live_plan["production_wrapper"]["path"]),
                str(candidate_root),
                *wrapper_argv,
            ]
            launched_at = _utc_now()
            launch_record: dict[str, Any] = {
                "candidate_index": candidate_index,
                "launched_at": launched_at,
                "launch_attempted": True,
                "child_argv": list(expected_child_argv),
                "return_code": None,
                "exception": None,
            }
            launches.append(launch_record)
            completed: subprocess.CompletedProcess[Any] | None = None
            primary_failure: BaseException | None = None
            final_zero_failure: BaseException | None = None
            seal_failure: BaseException | None = None
            final_zero: dict[str, Any] = {
                "status": "fail",
                "strip_verified_off": False,
                "ray_verified_off": False,
            }
            try:
                completed = run_fn(command, check=False)
                launch_record["return_code"] = int(completed.returncode)
            except BaseException as exc:
                primary_failure = exc
                launch_record["exception"] = exception_record(exc)
            finally:
                try:
                    final_zero = dict(final_zero_fn())
                except BaseException as exc:
                    final_zero_failure = exc
                    final_zero = {
                        "status": "fail",
                        "strip_verified_off": False,
                        "ray_verified_off": False,
                        **(exception_record(exc) or {}),
                    }

            candidate_root_safe = (
                candidate_root.is_dir()
                and not candidate_root.is_symlink()
                and candidate_root.resolve().parent == root.resolve()
            )
            if candidate_root_safe:
                try:
                    _write_json(
                        candidate_root / "independent-final-zero.json",
                        final_zero,
                    )
                except BaseException as exc:
                    seal_failure = exc
            elif seal_failure is None:
                seal_failure = RuntimeError(
                    "EQ-R6 attempted candidate lacks a safe candidate root"
                )

            seal: dict[str, Any] | None = None
            if primary_failure is None and completed is not None and seal_failure is None:
                try:
                    seal = _seal_eq_candidate(
                        live_plan,
                        candidate_index=candidate_index,
                        root=candidate_root,
                        wrapper_return_code=int(completed.returncode),
                        final_zero=final_zero,
                        expected_outer_pid=frozen_outer_pid,
                        expected_child_argv=expected_child_argv,
                    )
                    seals.append(seal)
                    if seal["status"] != "pass":
                        seal_failure = RuntimeError(
                            "EQ-R6 candidate terminal lifecycle failed"
                        )
                except BaseException as exc:
                    seal_failure = exc

            terminal = {
                "schema": EQ_R6_OUTER_CANDIDATE_TERMINAL_SCHEMA,
                "status": (
                    "pass"
                    if primary_failure is None
                    and final_zero_failure is None
                    and seal_failure is None
                    and seal is not None
                    and seal.get("status") == "pass"
                    else "fail"
                ),
                "candidate_index": candidate_index,
                "launch_attempted": True,
                "wrapper_return_code": (
                    None if completed is None else int(completed.returncode)
                ),
                "wrapper_exception": exception_record(primary_failure),
                "final_zero_attempted": True,
                "final_zero": final_zero,
                "final_zero_exception": exception_record(final_zero_failure),
                "seal": seal,
                "seal_exception": exception_record(seal_failure),
                "candidate_2_remained_locked": candidate_index == 1,
                "recorded_at": _utc_now(),
            }
            terminal_path = root / f"candidate-{candidate_index}-outer-terminal.json"
            _write_json(terminal_path, terminal)
            outer_terminals.append(_reference(terminal_path))

            if (
                primary_failure is not None
                or final_zero_failure is not None
                or seal_failure is not None
            ):
                if primary_failure is not None:
                    raise primary_failure
                if final_zero_failure is not None:
                    raise final_zero_failure
                assert seal_failure is not None
                raise seal_failure

            assert seal is not None
            result = json.loads(
                (candidate_root / "candidate-result.json").read_text(encoding="utf-8")
            )
            results.append([dict(row) for row in result["captures"]])
            if candidate_index == 1 and result["classification"] != "clipping_only":
                break
        classification = thermal.classify_td_b_eq_r6(
            results, required_feature_ids=feature_ids,
        )
        final_status = classification["status"]
        output = {
            "schema": EQ_R6_OUTER_RESULT_SCHEMA,
            "status": final_status,
            "classification": classification,
            "candidate_launches": launches,
            "candidate_seals": [
                _reference(root / f"candidate-{index}" / "terminal-seal.json")
                for index in range(1, len(seals) + 1)
            ],
            "outer_candidate_terminals": outer_terminals,
            "attempted_capture_calls": sum(
                int(seal["attempted_capture_calls"]) for seal in seals
            ),
            "physical_returned_cr3_count": sum(
                int(seal["physical_returned_cr3_count"]) for seal in seals
            ),
            "accepted_capture_count": sum(
                int(seal["accepted_capture_count"]) for seal in seals
            ),
            "retry": 0,
            "completed_at": _utc_now(),
        }
        _write_json(root / "outer-result.json", output)
        return root / "outer-result.json"
    except BaseException as exc:
        _write_json(root / "outer-failure.json", {
            "schema": "p7_td_b_eq_r6_outer_failure_v1",
            "status": "failed",
            "classification": final_status,
            "exception_type": type(exc).__name__,
            "message": str(exc),
            "candidate_launches": launches,
            "candidate_seals": seals,
            "outer_candidate_terminals": outer_terminals,
            "candidate_2_launch_count": sum(
                1 for item in launches if item["candidate_index"] == 2
            ),
            "retry": 0,
            "failed_at": _utc_now(),
        })
        raise


def _eq_prelaunch_exception(exc: BaseException) -> dict[str, str]:
    """Return only a secret-independent exception classification."""
    return {"exception_type": type(exc).__name__}


def _eq_prelaunch_write_json(
    root: Path,
    name: str,
    value: Mapping[str, Any],
) -> Path:
    """Atomically create one mode-0600 prelaunch artifact exactly once."""
    if name not in EQ_R6_PRELAUNCH_ARTIFACTS:
        raise ValueError("EQ-R6 prelaunch artifact name is not canonical")
    if root.is_symlink() or not root.is_dir():
        raise PermissionError("EQ-R6 prelaunch owner is not a regular directory")
    resolved_root = root.resolve(strict=True)
    target = root / name
    if target.is_symlink() or target.exists():
        raise FileExistsError(f"EQ-R6 prelaunch artifact already exists: {name}")
    if target.resolve(strict=False).parent != resolved_root:
        raise PermissionError("EQ-R6 prelaunch artifact escapes its owner")
    payload = (
        json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n"
    ).encode("utf-8")
    temporary = root / f".{name}.tmp-{os.getpid()}"
    if temporary.exists() or temporary.is_symlink():
        raise FileExistsError("EQ-R6 prelaunch temporary artifact already exists")
    descriptor = os.open(
        temporary,
        os.O_WRONLY
        | os.O_CREAT
        | os.O_EXCL
        | getattr(os, "O_NOFOLLOW", 0),
        0o600,
    )
    try:
        os.write(descriptor, payload)
        os.fsync(descriptor)
    except BaseException:
        try:
            temporary.unlink()
        except OSError:
            pass
        raise
    finally:
        os.close(descriptor)
    if target.exists() or target.is_symlink():
        temporary.unlink(missing_ok=True)
        raise FileExistsError(f"EQ-R6 prelaunch artifact raced: {name}")
    os.replace(temporary, target)
    os.chmod(target, 0o600, follow_symlinks=False)
    return target


def _eq_prelaunch_safe_parent_chain(path: Path) -> None:
    if not path.is_absolute() or ".." in path.parts:
        raise ValueError("EQ-R6 FAMILY must be an absolute non-escaping path")
    existing: list[Path] = []
    current = path.parent
    while True:
        if current.exists() or current.is_symlink():
            existing.append(current)
        if current == current.parent:
            break
        current = current.parent
    for owner in reversed(existing):
        mode = os.lstat(owner).st_mode
        if stat.S_ISLNK(mode) or not stat.S_ISDIR(mode):
            raise PermissionError(
                "EQ-R6 FAMILY parent chain contains a non-directory owner"
            )


def _eq_prelaunch_acquire_root(family: Path) -> tuple[Path, Path]:
    _eq_prelaunch_safe_parent_chain(family)
    prelaunch = family / "prelaunch"
    run_root = family / "run"
    for path in (family, prelaunch, run_root):
        if path.exists() or path.is_symlink():
            raise FileExistsError(
                f"EQ-R6 prelaunch path must be fresh: {path.name}"
            )
    if not family.parent.is_dir():
        raise FileNotFoundError("EQ-R6 FAMILY parent does not exist")
    os.mkdir(family, mode=0o700)
    os.mkdir(prelaunch, mode=0o700)
    os.chmod(family, 0o700)
    os.chmod(prelaunch, 0o700)
    return prelaunch, run_root


def _eq_prelaunch_outer_argv(
    *,
    family: Path,
    run_root: Path,
    code_checkpoint: str,
) -> list[str]:
    return [
        str(Path(__file__).parents[3] / ".venv/bin/python"),
        "-m",
        "camera_based_rgbww_optimizer.optimization.measure_p7_thermal_diagnostics",
        "--execute",
        "--allow-device-control",
        "--eq-r6-orchestrate",
        "--experiment-id",
        thermal.TD_B,
        "--source",
        "ray",
        "--phase",
        "formal",
        "--output-dir",
        str(family),
        "--run-name",
        run_root.name,
        "--code-checkpoint",
        code_checkpoint,
        "--human-authorization",
        thermal.TD_B_EQ_R6_EXPERIMENT_ID,
        "--camera-backend",
        "remote",
    ]


def _eq_prelaunch_default_python_cleanup() -> Mapping[str, Any]:
    from camera_based_rgbww_optimizer.control import all_off

    steps = all_off.turn_everything_off()
    rows = [
        step.to_jsonable() if hasattr(step, "to_jsonable") else dict(step)
        for step in steps
    ]
    return {
        "status": (
            "pass"
            if rows and all(row.get("ok") is True for row in rows)
            else "fail"
        )
    }


def _eq_prelaunch_default_shell_cleanup() -> subprocess.CompletedProcess[str]:
    python = str(Path(__file__).parents[3] / ".venv/bin/python")
    return subprocess.run(
        [
            "zsh",
            "-c",
            'exec "$1" -m camera_based_rgbww_optimizer.control.all_off --json',
            "eq-r6-prelaunch-cleanup",
            python,
        ],
        check=False,
        capture_output=True,
        text=True,
        shell=False,
    )


def _eq_prelaunch_default_ray_readiness() -> Mapping[str, Any]:
    from camera_based_rgbww_optimizer.control import ray120c

    return ray120c.get_hsi()


def _eq_prelaunch_reference(path: Path) -> dict[str, Any]:
    reference = _reference(path)
    reference["mode"] = oct(stat.S_IMODE(os.lstat(path).st_mode))
    return reference


def _eq_prelaunch_validate_root(prelaunch: Path) -> dict[str, Any]:
    if prelaunch.is_symlink() or not prelaunch.is_dir():
        raise PermissionError("EQ-R6 prelaunch manifest owner differs")
    if stat.S_IMODE(os.lstat(prelaunch).st_mode) != 0o700:
        raise PermissionError("EQ-R6 prelaunch root mode differs")
    entries = sorted(path.name for path in prelaunch.iterdir())
    if entries != sorted(EQ_R6_PRELAUNCH_ARTIFACTS):
        raise PermissionError("EQ-R6 prelaunch canonical artifact set differs")
    parsed: dict[str, dict[str, Any]] = {}
    for name in EQ_R6_PRELAUNCH_ARTIFACTS:
        path = prelaunch / name
        if (
            path.is_symlink()
            or not path.is_file()
            or path.resolve().parent != prelaunch.resolve()
            or stat.S_IMODE(os.lstat(path).st_mode) != 0o600
        ):
            raise PermissionError(
                f"EQ-R6 prelaunch artifact owner or mode differs: {name}"
            )
        raw = path.read_bytes()
        if not raw.endswith(b"\n") or raw.endswith(b"\n\n"):
            raise ValueError(f"EQ-R6 prelaunch JSON newline differs: {name}")
        value = json.loads(raw.decode("utf-8"))
        if not isinstance(value, dict):
            raise ValueError(f"EQ-R6 prelaunch JSON is not an object: {name}")
        if (
            json.dumps(value, indent=2, sort_keys=True, allow_nan=False).encode(
                "utf-8"
            )
            + b"\n"
            != raw
        ):
            raise ValueError(f"EQ-R6 prelaunch JSON is not canonical: {name}")
        parsed[name] = value
    terminal = parsed["prelaunch-terminal.json"]
    manifest = parsed["prelaunch-manifest.json"]
    expected_terminal_refs = [
        _eq_prelaunch_reference(prelaunch / name)
        for name in EQ_R6_PRELAUNCH_ARTIFACTS[:7]
    ]
    expected_manifest_refs = [
        _eq_prelaunch_reference(prelaunch / name)
        for name in EQ_R6_PRELAUNCH_ARTIFACTS[:8]
    ]
    if terminal.get("canonical_artifacts") != expected_terminal_refs:
        raise PermissionError("EQ-R6 prelaunch terminal references differ")
    if (
        manifest.get("canonical_artifacts") != expected_manifest_refs
        or manifest.get("artifact_order") != list(EQ_R6_PRELAUNCH_ARTIFACTS)
        or manifest.get("canonical_json_count") != 9
        or manifest.get("status") != terminal.get("status")
        or manifest.get("run_root_created") is not False
        or manifest.get("dispatch_count") != 0
    ):
        raise PermissionError("EQ-R6 prelaunch manifest references differ")
    stage_names = (
        "camera-readiness.json",
        "ray-readiness.json",
        "all-off-python.json",
        "all-off-shell.json",
        "independent-final-zero.json",
    )
    stage_statuses = [parsed[name].get("status") for name in stage_names]
    all_pass = all(status == "pass" for status in stage_statuses)
    handoff = terminal.get("launch_handoff")
    if (
        terminal.get("status") not in {"pass", "fail"}
        or not isinstance(handoff, Mapping)
        or handoff.get("dispatch_count") != 0
        or handoff.get("outer_launch_count") != 0
        or (terminal.get("status") == "pass") != all_pass
        or handoff.get("ready_for_dispatch")
        != (terminal.get("status") == "pass")
    ):
        raise PermissionError("EQ-R6 prelaunch terminal decision differs")
    if terminal.get("status") == "pass":
        family = prelaunch.parent
        run_root = family / "run"
        expected_argv = _eq_prelaunch_outer_argv(
            family=family,
            run_root=run_root,
            code_checkpoint=str(
                parsed["frozen-inputs.json"]["code_checkpoint"]
            ),
        )
        expected_hash = hashlib.sha256(
            json.dumps(
                expected_argv,
                separators=(",", ":"),
                ensure_ascii=False,
                allow_nan=False,
            ).encode("utf-8")
        ).hexdigest()
        if (
            handoff.get("run_root") != str(run_root)
            or handoff.get("outer_argv") != expected_argv
            or handoff.get("outer_argv_sha256") != expected_hash
            or run_root.exists()
            or run_root.is_symlink()
        ):
            raise PermissionError("EQ-R6 prelaunch launch handoff differs")
    elif "outer_argv" in handoff or "outer_argv_sha256" in handoff:
        raise PermissionError("EQ-R6 failed prelaunch exposes executable argv")
    if any(path.name.startswith(".") for path in prelaunch.iterdir()):
        raise PermissionError("EQ-R6 prelaunch temporary artifact remains")
    return parsed


def run_td_b_eq_r6_prelaunch(
    *,
    family_root: str | Path,
    code_checkpoint: str,
    checkpoint_validator: Callable[[str], None] = _validate_checkpoint_and_tree,
    backend_factory: Callable[[], Any] | None = None,
    ray_readiness_fn: Callable[[], Mapping[str, Any]] | None = None,
    python_cleanup_fn: Callable[[], Mapping[str, Any]] | None = None,
    shell_cleanup_fn: Callable[[], Any] | None = None,
    final_zero_fn: Callable[[], Mapping[str, Any]] = _default_eq_final_zero,
    write_artifact_fn: Callable[
        [Path, str, Mapping[str, Any]], Path
    ] = _eq_prelaunch_write_json,
    forbidden_secret_values: Sequence[str] = (),
) -> Path:
    """Build one no-dispatch EQ-R6 readiness seal in a fresh FAMILY."""
    checkpoint_validator(code_checkpoint)
    family = Path(family_root)
    if not family.is_absolute():
        raise ValueError("EQ-R6 FAMILY must be absolute")
    _eq_prelaunch_safe_parent_chain(family)
    family = family.resolve(strict=False)
    prelaunch, run_root = _eq_prelaunch_acquire_root(family)
    if run_root.exists() or run_root.is_symlink():
        raise PermissionError("EQ-R6 RUN must remain absent during prelaunch")

    frozen = {
        "schema": "p7_td_b_eq_r6_prelaunch_frozen_inputs_v1",
        "status": "pass",
        "attempted": True,
        "call_count": 1,
        "code_checkpoint": code_checkpoint,
        "family_root": str(family),
        "prelaunch_root": str(prelaunch),
        "run_root": str(run_root),
        "measurement_runner": thermal.file_reference(Path(__file__)),
        "production_wrapper": thermal.file_reference(PRODUCTION_WRAPPER),
        "exposure_policy": thermal.file_reference(
            thermal.TD_B_EXPOSURE_POLICY_V2_PATH
        ),
        "curve": thermal.file_reference(thermal.CURVE_PATH),
        "human_authorization": thermal.TD_B_EQ_R6_EXPERIMENT_ID,
        "human_confirmation_consumed": False,
        "dispatch_count": 0,
    }
    write_artifact_fn(prelaunch, EQ_R6_PRELAUNCH_ARTIFACTS[0], frozen)

    offline_plan = thermal.build_td_b_eq_r6_plan()
    offline = {
        "schema": "p7_td_b_eq_r6_prelaunch_offline_plan_v1",
        "status": "pass",
        "attempted": True,
        "call_count": 1,
        "offline_plan": offline_plan,
        "live_output_contract": {
            "family_root": str(family),
            "output_root": str(run_root),
            "run_root_must_be_absent": True,
            "code_checkpoint": code_checkpoint,
            "production_wrapper": thermal.file_reference(PRODUCTION_WRAPPER),
            "measurement_runner": thermal.file_reference(Path(__file__)),
        },
        "formal": 0,
        "ambient": 0,
        "retry": 0,
        "dispatch_count": 0,
    }
    write_artifact_fn(prelaunch, EQ_R6_PRELAUNCH_ARTIFACTS[1], offline)

    primary_failure: BaseException | None = None
    camera = {
        "schema": "p7_td_b_eq_r6_camera_readiness_v1",
        "status": "fail",
        "attempted": True,
        "factory_calls": 0,
        "connect_calls": 0,
        "resolve_settings_calls": 0,
        "shutter_read_calls": 0,
        "capture_calls": 0,
        "settings_write_calls": 0,
    }
    try:
        if backend_factory is None:
            from camera_based_rgbww_optimizer.control import camera_remote

            backend_factory = lambda: camera_remote.create_camera_backend(
                "remote"
            )
        camera["factory_calls"] = 1
        backend = backend_factory()
        if getattr(backend, "backend_name", None) != "remote":
            raise PermissionError("EQ-R6 prelaunch backend identity differs")
        if (
            getattr(backend, "v2_capture_capability", None)
            != REMOTE_V2_CAPABILITY
        ):
            raise PermissionError("EQ-R6 prelaunch v2 capability differs")
        if not callable(getattr(backend, "capture_with_timing", None)):
            raise PermissionError(
                "EQ-R6 prelaunch backend lacks capture_with_timing"
            )
        camera["connect_calls"] = 1
        connection = backend.connect()
        camera["resolve_settings_calls"] = 1
        settings = backend.resolve_capture_settings(
            iso=None,
            aperture=None,
            image_format="RAW",
        )
        iso = (
            settings.get("iso")
            if isinstance(settings, Mapping)
            else getattr(settings, "iso", None)
        )
        aperture = (
            settings.get("aperture")
            if isinstance(settings, Mapping)
            else getattr(settings, "aperture", None)
        )
        image_format = (
            settings.get("image_format")
            if isinstance(settings, Mapping)
            else getattr(settings, "image_format", None)
        )
        if not str(iso or "") or not str(aperture or "") or image_format != "RAW":
            raise PermissionError("EQ-R6 prelaunch resolved settings differ")
        camera["shutter_read_calls"] = 1
        _current, choices = backend.read_shutter_current_and_choices(connection)
        if (
            not isinstance(choices, Sequence)
            or isinstance(choices, (str, bytes))
            or "1/2500" not in choices
            or "1/3200" not in choices
        ):
            raise PermissionError("EQ-R6 prelaunch shutter choices differ")
        camera.update(
            {
                "status": "pass",
                "backend_name": "remote",
                "v2_capture_capability": REMOTE_V2_CAPABILITY,
                "resolved_iso_nonempty": True,
                "resolved_aperture_nonempty": True,
                "resolved_image_format": "RAW",
                "capture_with_timing_callable": True,
                "required_shutters_present": True,
            }
        )
    except BaseException as exc:
        primary_failure = exc
        camera["exception"] = _eq_prelaunch_exception(exc)
    camera["call_count"] = sum(
        int(camera[name])
        for name in (
            "factory_calls",
            "connect_calls",
            "resolve_settings_calls",
            "shutter_read_calls",
        )
    )
    write_artifact_fn(prelaunch, EQ_R6_PRELAUNCH_ARTIFACTS[2], camera)

    ray = {
        "schema": "p7_td_b_eq_r6_ray_readiness_v1",
        "status": "not_attempted" if primary_failure is not None else "fail",
        "attempted": primary_failure is None,
        "get_hsi_calls": 0,
        "nonzero_set_calls": 0,
    }
    if primary_failure is None:
        try:
            if ray_readiness_fn is None:
                ray_readiness_fn = _eq_prelaunch_default_ray_readiness
            ray["get_hsi_calls"] = 1
            response = ray_readiness_fn()
            data = response.get("data") if isinstance(response, Mapping) else None
            if (
                not isinstance(data, Mapping)
                or any(
                    type(data.get(name)) not in (int, float)
                    for name in ("hue", "sat", "intensity")
                )
            ):
                raise PermissionError("EQ-R6 prelaunch Ray response differs")
            ray.update(
                {
                    "status": "pass",
                    "response_data_schema_valid": True,
                }
            )
        except BaseException as exc:
            primary_failure = exc
            ray["status"] = "fail"
            ray["exception"] = _eq_prelaunch_exception(exc)
    ray["call_count"] = ray["get_hsi_calls"]
    write_artifact_fn(prelaunch, EQ_R6_PRELAUNCH_ARTIFACTS[3], ray)

    cleanup_failures: list[BaseException] = []
    python_cleanup = {
        "schema": "p7_td_b_eq_r6_python_cleanup_v1",
        "status": "fail",
        "attempted": True,
        "call_count": 1,
    }
    try:
        result = (python_cleanup_fn or _eq_prelaunch_default_python_cleanup)()
        if not isinstance(result, Mapping) or result.get("status") != "pass":
            raise RuntimeError("EQ-R6 prelaunch Python cleanup failed")
        python_cleanup["status"] = "pass"
    except BaseException as exc:
        cleanup_failures.append(exc)
        python_cleanup["exception"] = _eq_prelaunch_exception(exc)
    write_artifact_fn(prelaunch, EQ_R6_PRELAUNCH_ARTIFACTS[4], python_cleanup)

    shell_cleanup = {
        "schema": "p7_td_b_eq_r6_shell_cleanup_v1",
        "status": "fail",
        "attempted": True,
        "call_count": 1,
        "shell": False,
    }
    try:
        completed = (
            shell_cleanup_fn or _eq_prelaunch_default_shell_cleanup
        )()
        return_code = getattr(completed, "returncode", None)
        stdout = getattr(completed, "stdout", None)
        parsed_stdout = json.loads(stdout) if isinstance(stdout, str) else None
        if (
            type(return_code) is not int
            or return_code != 0
            or not isinstance(parsed_stdout, list)
            or not parsed_stdout
            or not all(
                isinstance(row, Mapping) and row.get("ok") is True
                for row in parsed_stdout
            )
        ):
            raise RuntimeError("EQ-R6 prelaunch shell cleanup failed")
        shell_cleanup.update(
            {
                "status": "pass",
                "return_code": 0,
                "stdout_json_valid": True,
                "stderr_recorded": False,
            }
        )
    except BaseException as exc:
        cleanup_failures.append(exc)
        shell_cleanup["exception"] = _eq_prelaunch_exception(exc)
    write_artifact_fn(prelaunch, EQ_R6_PRELAUNCH_ARTIFACTS[5], shell_cleanup)

    zero_failures: list[BaseException] = []
    final_zero = {
        "schema": "p7_td_b_eq_r6_independent_final_zero_v1",
        "status": "fail",
        "attempted": True,
        "call_count": 1,
    }
    try:
        zero = final_zero_fn()
        if (
            not isinstance(zero, Mapping)
            or zero.get("status") != "pass"
            or zero.get("strip_verified_off") is not True
            or zero.get("ray_verified_off") is not True
        ):
            raise RuntimeError("EQ-R6 prelaunch independent final-zero failed")
        final_zero.update(
            {
                "status": "pass",
                "strip_generation_strictly_advanced": True,
                "five_channels_zero": True,
                "ray_intensity_zero": True,
                "validate_both_off": "pass",
            }
        )
    except BaseException as exc:
        zero_failures.append(exc)
        final_zero["exception"] = _eq_prelaunch_exception(exc)
    write_artifact_fn(prelaunch, EQ_R6_PRELAUNCH_ARTIFACTS[6], final_zero)

    failures = (
        ([] if primary_failure is None else [primary_failure])
        + cleanup_failures
        + zero_failures
    )
    outer_argv = _eq_prelaunch_outer_argv(
        family=family,
        run_root=run_root,
        code_checkpoint=code_checkpoint,
    )
    argv_sha256 = hashlib.sha256(
        json.dumps(
            outer_argv,
            separators=(",", ":"),
            ensure_ascii=False,
            allow_nan=False,
        ).encode("utf-8")
    ).hexdigest()
    handoff: dict[str, Any] = {
        "ready_for_dispatch": not failures,
        "dispatch_count": 0,
        "outer_launch_count": 0,
    }
    if not failures:
        handoff.update(
            {
                "run_root": str(run_root),
                "code_checkpoint": code_checkpoint,
                "human_authorization": thermal.TD_B_EQ_R6_EXPERIMENT_ID,
                "outer_argv": outer_argv,
                "outer_argv_sha256": argv_sha256,
            }
        )
    safe_values = [
        value
        for value in forbidden_secret_values
        if isinstance(value, str) and value
    ]
    preterminal_bytes = b"".join(
        (prelaunch / name).read_bytes()
        for name in EQ_R6_PRELAUNCH_ARTIFACTS[:7]
    ) + json.dumps(handoff, sort_keys=True).encode("utf-8")
    if any(value.encode("utf-8") in preterminal_bytes for value in safe_values):
        secret_failure = PermissionError(
            "EQ-R6 prelaunch secret-absence scan failed"
        )
        failures.append(secret_failure)
        handoff = {
            "ready_for_dispatch": False,
            "dispatch_count": 0,
            "outer_launch_count": 0,
        }

    terminal = {
        "schema": "p7_td_b_eq_r6_prelaunch_terminal_v1",
        "status": "pass" if not failures else "fail",
        "attempted": True,
        "call_count": 1,
        "stage_status": {
            "camera": camera["status"],
            "ray": ray["status"],
            "python_cleanup": python_cleanup["status"],
            "shell_cleanup": shell_cleanup["status"],
            "independent_final_zero": final_zero["status"],
        },
        "failures": [_eq_prelaunch_exception(exc) for exc in failures],
        "launch_handoff": handoff,
        "canonical_artifacts": [
            _eq_prelaunch_reference(prelaunch / name)
            for name in EQ_R6_PRELAUNCH_ARTIFACTS[:7]
        ],
        "sealed_at": _utc_now(),
    }
    write_artifact_fn(prelaunch, EQ_R6_PRELAUNCH_ARTIFACTS[7], terminal)
    manifest = {
        "schema": "p7_td_b_eq_r6_prelaunch_manifest_v1",
        "status": terminal["status"],
        "attempted": True,
        "call_count": 1,
        "artifact_order": list(EQ_R6_PRELAUNCH_ARTIFACTS),
        "canonical_json_count": 9,
        "canonical_artifacts": [
            _eq_prelaunch_reference(prelaunch / name)
            for name in EQ_R6_PRELAUNCH_ARTIFACTS[:8]
        ],
        "run_root_created": False,
        "dispatch_count": 0,
        "completed_at": _utc_now(),
    }
    manifest_path = write_artifact_fn(
        prelaunch,
        EQ_R6_PRELAUNCH_ARTIFACTS[8],
        manifest,
    )
    _eq_prelaunch_validate_root(prelaunch)
    if run_root.exists() or run_root.is_symlink():
        raise PermissionError("EQ-R6 prelaunch created RUN")
    if failures:
        raise failures[0]
    return manifest_path


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    from camera_based_rgbww_optimizer.control import camera_remote

    parser = argparse.ArgumentParser(description="Build or execute a frozen P7 thermal diagnostic plan.")
    parser.add_argument("--experiment-id", choices=thermal.EXPERIMENT_IDS, required=True)
    parser.add_argument("--source", choices=("ray", "strip"))
    parser.add_argument("--variant", choices=("core", "expansion"), default="core")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--run-name", required=True)
    parser.add_argument("--prerequisite-artifact", type=Path, default=thermal.OPERATING_ENVELOPE_PATH)
    parser.add_argument("--phase", choices=("setup", "formal"))
    parser.add_argument("--setup-release", type=Path)
    parser.add_argument("--lineage-candidate", type=Path)
    parser.add_argument("--qualification-preparation", type=Path)
    parser.add_argument("--finalize-setup-run", type=Path)
    parser.add_argument("--orchestrate-setup", action="store_true")
    parser.add_argument("--code-checkpoint")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--dry-run", action="store_true")
    mode.add_argument("--execute", action="store_true")
    mode.add_argument("--qualify-lineage-release", action="store_true")
    mode.add_argument(
        "--prepare-lineage-qualification-evidence", action="store_true"
    )
    eq_mode = parser.add_mutually_exclusive_group()
    eq_mode.add_argument("--eq-r6-prelaunch", action="store_true")
    eq_mode.add_argument("--eq-r6-orchestrate", action="store_true")
    eq_mode.add_argument("--eq-r6-single-candidate", type=int, choices=(1, 2))
    parser.add_argument("--eq-r6-live-plan", type=Path)
    parser.add_argument("--eq-r6-outer-pid", type=int)
    parser.add_argument("--allow-device-control", action="store_true")
    parser.add_argument("--human-authorization")
    camera_remote.add_camera_backend_arguments(parser, default="remote")
    return parser.parse_args(argv)


def main(
    argv: Sequence[str] | None = None, *,
    backend_factory: Callable[..., Any] | None = None,
    run_fn: Callable[..., Path] = run_authorized_plan,
    setup_fn: Callable[..., Path] = run_td_b_setup_provisional,
    setup_finalize_fn: Callable[..., tuple[Path, Path, Path]] = finalize_td_b_setup_after_wrapper,
    setup_orchestrate_fn: Callable[..., tuple[Path, Path, Path]] = orchestrate_td_b_setup,
    resolved_run_fn: Callable[..., Path] = run_resolved_td_b_formal,
    eq_prelaunch_fn: Callable[..., Path] = run_td_b_eq_r6_prelaunch,
) -> int:
    args = parse_args(argv)
    if args.eq_r6_prelaunch:
        from camera_based_rgbww_optimizer.control import camera_remote

        if (
            not args.execute
            or not args.allow_device_control
            or args.experiment_id != thermal.TD_B
            or args.source != "ray"
            or args.phase != "formal"
            or args.run_name != "prelaunch"
            or not args.output_dir.is_absolute()
            or not args.code_checkpoint
            or args.human_authorization != thermal.TD_B_EQ_R6_EXPERIMENT_ID
            or args.camera_backend != "remote"
            or args.setup_release is not None
            or args.lineage_candidate is not None
            or args.qualification_preparation is not None
            or args.finalize_setup_run is not None
            or args.orchestrate_setup
            or args.eq_r6_live_plan is not None
            or args.eq_r6_outer_pid is not None
            or args.variant != "core"
            or args.prerequisite_artifact != thermal.OPERATING_ENVELOPE_PATH
            or Path(args.remote_env_file).resolve()
            != Path(camera_remote.DEFAULT_ENV_FILE).resolve()
            or args.remote_base_url is not None
            or args.remote_timeout != camera_remote.DEFAULT_TIMEOUT
        ):
            raise PermissionError(
                "EQ-R6 prelaunch requires its exact isolated production contract"
            )
        configured_backend_factory = (
            None
            if backend_factory is None
            else lambda: backend_factory(
                args.camera_backend,
                env_file=args.remote_env_file,
                base_url=args.remote_base_url,
                timeout=args.remote_timeout,
            )
        )
        print(
            eq_prelaunch_fn(
                family_root=args.output_dir,
                code_checkpoint=args.code_checkpoint,
                backend_factory=configured_backend_factory,
            )
        )
        return 0
    if args.eq_r6_orchestrate:
        if (
            not args.execute
            or not args.allow_device_control
            or args.experiment_id != thermal.TD_B
            or args.source != "ray"
            or args.phase != "formal"
            or not args.code_checkpoint
            or args.human_authorization != thermal.TD_B_EQ_R6_EXPERIMENT_ID
            or args.setup_release is not None
            or args.lineage_candidate is not None
            or args.finalize_setup_run is not None
            or args.orchestrate_setup
            or args.eq_r6_live_plan is not None
        ):
            raise PermissionError("EQ-R6 orchestration requires its exact isolated live contract")
        _validate_checkpoint_and_tree(args.code_checkpoint)
        root = (args.output_dir / args.run_name).resolve()
        live_plan = thermal.activate_td_b_eq_r6_live_plan(
            thermal.build_td_b_eq_r6_plan(),
            code_checkpoint=args.code_checkpoint,
            output_root=root,
            wrapper_path=PRODUCTION_WRAPPER,
            measurement_runner_path=Path(__file__),
        )
        print(orchestrate_td_b_eq_r6(live_plan))
        return 0
    if args.eq_r6_single_candidate is not None:
        if (
            not args.execute
            or not args.allow_device_control
            or args.experiment_id != thermal.TD_B
            or args.source != "ray"
            or args.phase != "formal"
            or not args.code_checkpoint
            or args.human_authorization != thermal.TD_B_EQ_R6_EXPERIMENT_ID
            or args.eq_r6_live_plan is None
            or args.eq_r6_outer_pid is None
            or args.eq_r6_outer_pid <= 0
            or args.setup_release is not None
            or args.lineage_candidate is not None
            or args.finalize_setup_run is not None
            or args.orchestrate_setup
        ):
            raise PermissionError("EQ-R6 candidate mode requires its exact isolated child contract")
        live_path = args.eq_r6_live_plan.resolve(strict=True)
        live_plan = json.loads(live_path.read_text(encoding="utf-8"))
        thermal.validate_td_b_eq_r6_live_plan(live_plan, require_fresh_root=False)
        _validate_checkpoint_and_tree(args.code_checkpoint)
        if live_plan["code_checkpoint"] != args.code_checkpoint:
            raise PermissionError("EQ-R6 child checkpoint differs from its live plan")
        candidate_root = (args.output_dir / args.run_name).resolve()
        if candidate_root != Path(str(live_plan["output_root"])).resolve() / (
            f"candidate-{args.eq_r6_single_candidate}"
        ):
            raise PermissionError("EQ-R6 candidate CLI root differs from the live owner")
        current_outer_pid = args.eq_r6_outer_pid
        current_wrapper_pid = os.getppid()
        current_runner_pid = os.getpid()
        current_argv = list(sys.argv[1:] if argv is None else argv)
        expected_argv = _eq_r6_exact_child_argv(
            live_plan,
            candidate_index=args.eq_r6_single_candidate,
            live_plan_path=live_path,
            outer_pid=current_outer_pid,
        )
        write_td_b_eq_r6_launch_ledger(
            live_plan,
            candidate_index=args.eq_r6_single_candidate,
            candidate_root=candidate_root,
            outer_pid=current_outer_pid,
            wrapper_pid=current_wrapper_pid,
            runner_pid=current_runner_pid,
            argv=current_argv,
        )
        ledger = _load_regular_json(candidate_root / "launch-ledger.json")
        _validate_td_b_eq_r6_launch_ledger(
            ledger,
            live_plan,
            candidate_index=args.eq_r6_single_candidate,
            candidate_root=candidate_root,
            expected_outer_pid=current_outer_pid,
            expected_wrapper_pid=current_wrapper_pid,
            expected_runner_pid=current_runner_pid,
            expected_argv=expected_argv,
        )
        if args.camera_backend != "remote":
            raise PermissionError("EQ-R6 requires the formal remote-v2 camera backend")
        if backend_factory is None:
            from camera_based_rgbww_optimizer.control import camera_remote
            backend_factory = camera_remote.create_camera_backend
        backend = backend_factory(
            args.camera_backend,
            env_file=args.remote_env_file,
            base_url=args.remote_base_url,
            timeout=args.remote_timeout,
        )
        print(run_td_b_eq_r6_production_candidate(
            live_plan,
            candidate_index=args.eq_r6_single_candidate,
            candidate_root=candidate_root,
            camera_backend=backend,
            runtime_outer_pid=current_outer_pid,
            runtime_wrapper_pid=current_wrapper_pid,
            runtime_runner_pid=current_runner_pid,
            runtime_argv=expected_argv,
        ))
        return 0
    if args.prepare_lineage_qualification_evidence:
        if (
            args.experiment_id != thermal.TD_B
            or args.source != "ray"
            or args.phase != "formal"
            or args.qualification_preparation is None
            or not args.code_checkpoint
            or args.setup_release is not None
            or args.lineage_candidate is not None
        ):
            raise PermissionError(
                "evidence-only lineage preparation requires exact offline inputs"
            )
        print(write_td_b_lineage_qualification_evidence(
            preparation_path=args.qualification_preparation,
            output_dir=args.output_dir,
            run_name=args.run_name,
            code_checkpoint=args.code_checkpoint,
        ))
        return 0
    if args.qualify_lineage_release:
        if (
            args.experiment_id != thermal.TD_B
            or args.source != "ray"
            or args.phase != "formal"
            or args.setup_release is None
            or args.lineage_candidate is None
            or not args.code_checkpoint
        ):
            raise PermissionError(
                "lineage qualification requires exact Ray TD-B formal inputs"
            )
        print(write_td_b_setup_lineage_release(
            output_dir=args.output_dir,
            run_name=args.run_name,
            code_checkpoint=args.code_checkpoint,
            legacy_release_path=args.setup_release,
            planner_candidate_path=args.lineage_candidate,
        ))
        return 0
    if args.dry_run:
        if args.phase == "setup":
            plan = thermal.build_diagnostic_plan(
                args.experiment_id, source=args.source, variant=args.variant,
                prerequisite_artifact=args.prerequisite_artifact,
            )
            preview = {"phase": "setup", "experiment_id": args.experiment_id,
                "source": args.source, "setup_requirement": plan.get("exposure_setup_required"),
                "budgets": plan.get("budgets"), "device_locked": True,
                "output_owner": str((args.output_dir / args.run_name).resolve())}
            print(json.dumps(preview, sort_keys=True))
            return 0
        print(write_dry_run(
            experiment_id=args.experiment_id, output_dir=args.output_dir,
            run_name=args.run_name, source=args.source, variant=args.variant,
            prerequisite_artifact=args.prerequisite_artifact,
        ))
        return 0
    if not args.allow_device_control or args.human_authorization != args.experiment_id:
        raise PermissionError("--execute requires --allow-device-control and exact --human-authorization")
    if args.camera_backend != "remote":
        raise PermissionError("thermal diagnostics require the formal remote v2 camera backend")
    if args.experiment_id == thermal.TD_B and args.phase is None:
        raise PermissionError("TD-B execution requires explicit --phase setup or --phase formal")
    if args.orchestrate_setup:
        if args.phase != "setup" or args.experiment_id != thermal.TD_B or args.source != "ray" or not args.code_checkpoint:
            raise PermissionError("setup orchestration requires exact Ray TD-B setup and --code-checkpoint")
        wrapper_args = [
            "--phase", "setup", "--experiment-id", args.experiment_id,
            "--source", args.source, "--variant", args.variant,
            "--prerequisite-artifact", str(args.prerequisite_artifact),
            "--human-authorization", str(args.human_authorization),
            "--code-checkpoint", args.code_checkpoint,
            "--camera-backend", args.camera_backend,
            "--remote-env-file", str(args.remote_env_file),
            "--remote-timeout", str(args.remote_timeout),
        ]
        if args.remote_base_url is not None:
            wrapper_args.extend(("--remote-base-url", args.remote_base_url))
        for path in setup_orchestrate_fn(
            run_dir=args.output_dir / args.run_name,
            code_checkpoint=args.code_checkpoint,
            wrapper_args=wrapper_args,
        ):
            print(path)
        return 0
    if args.finalize_setup_run is not None:
        if args.phase != "setup" or not args.code_checkpoint:
            raise PermissionError("setup finalization requires --phase setup and --code-checkpoint")
        for path in setup_finalize_fn(
            args.finalize_setup_run, code_checkpoint=args.code_checkpoint,
        ):
            print(path)
        return 0

    if args.setup_release is not None:
        if args.experiment_id != thermal.TD_B or args.source != "ray" or not args.code_checkpoint:
            raise PermissionError("setup release is only valid for exact Ray TD-B formal phase")
        if backend_factory is None:
            from camera_based_rgbww_optimizer.control import camera_remote
            backend_factory = camera_remote.create_camera_backend
        backend = backend_factory(
            args.camera_backend, env_file=args.remote_env_file,
            base_url=args.remote_base_url, timeout=args.remote_timeout,
        )
        print(resolved_run_fn(
            args.setup_release, output_dir=args.output_dir, run_name=args.run_name,
            camera_backend=backend, code_checkpoint=args.code_checkpoint,
        ))
        return 0

    plan = thermal.build_diagnostic_plan(
        args.experiment_id, source=args.source, variant=args.variant,
        prerequisite_artifact=args.prerequisite_artifact,
        for_execution=True, human_authorization=args.human_authorization,
        v2_capture_capability=True,
    )
    if args.phase in (None, "formal") and args.setup_release is None:
        validate_authorized_execution_plan(plan)
    if backend_factory is None:
        from camera_based_rgbww_optimizer.control import camera_remote
        backend_factory = camera_remote.create_camera_backend
    backend = backend_factory(
        args.camera_backend, env_file=args.remote_env_file,
        base_url=args.remote_base_url, timeout=args.remote_timeout,
    )
    if args.phase == "setup":
        if args.experiment_id != thermal.TD_B or args.source != "ray" or not args.code_checkpoint:
            raise PermissionError("setup phase requires exact Ray TD-B and --code-checkpoint")
        print(setup_fn(
            plan, output_dir=args.output_dir, run_name=args.run_name,
            camera_backend=backend, code_checkpoint=args.code_checkpoint,
        ))
        return 0
    print(run_fn(plan, output_dir=args.output_dir, run_name=args.run_name, camera_backend=backend))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
