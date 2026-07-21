from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Mapping, Sequence

from camera_based_rgbww_optimizer.optimization import p7_thermal_diagnostics as thermal
from camera_based_rgbww_optimizer.control import camera_remote_v2
from camera_based_rgbww_optimizer.paths import PROJECT_TMP_DIR


DEFAULT_OUTPUT = PROJECT_TMP_DIR / "p7-thermal-diagnostics-offline"
REMOTE_V2_CAPABILITY = "remote_v2_capture_timing_v1"


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
) -> Path:
    root = Path(output_dir) / run_name
    root.mkdir(parents=True, exist_ok=False)
    plan = thermal.build_diagnostic_plan(experiment_id, source=source, variant=variant)
    _write_json(root / "plan.json", plan)
    return root / "plan.json"


def execute_plan(
    plan: Mapping[str, Any], *, run_dir: str | Path,
    apply_command_fn: Callable[[Mapping[str, Any]], Mapping[str, Any]],
    readback_fn: Callable[[Mapping[str, Any]], Mapping[str, Any]],
    capture_fn: Callable[[Mapping[str, Any]], Mapping[str, Any]],
    both_off_gate_fn: Callable[[str], Mapping[str, Any]],
    cleanup_fn: Callable[[], Mapping[str, Any]],
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
        "ambient_capture_count": 0, "physical_cr3_count": 0, "cleanup": "pending",
        "capture_settings_provenance": copy.deepcopy(plan["camera"].get("resolved_capture_settings")),
    }
    _write_json(root / "run.json", run)
    failure: BaseException | None = None
    session_start = monotonic_fn()
    previous_state: str | None = None
    previous_dwell: float | None = None
    last_observed_by_group: dict[tuple[Any, ...], float] = {}
    owned_cr3_paths: set[Path] = set()
    rejected_capture: dict[str, Any] | None = None

    def record_gate(gate_id: str) -> None:
        evidence = dict(both_off_gate_fn(gate_id))
        if evidence.get("status") != "pass" or evidence.get("strip_verified_off") is not True or evidence.get("ray_verified_off") is not True:
            raise RuntimeError(f"both-source off/readback gate failed: {gate_id}")
        _append_jsonl(root / "isolation-gates.jsonl", {"gate_id": gate_id, "evidence": evidence, "at": _utc_now()})

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
        sidecar_value = capture.get("remote_metadata_path")
        sidecar_candidate = Path(str(sidecar_value)) if sidecar_value else None
        sidecar_path = sidecar_candidate.resolve() if sidecar_candidate is not None else None
        rejected_capture = {
            "capture_id": step["capture_id"],
            "rejection_stage": "adapter_retained_cr3_validation",
            "reported_physical_capture_count": reported_physical,
            "cr3_path": None if raw_path is None else str(raw_path),
            "cr3_sha256": None,
            "sidecar_path": None if sidecar_path is None else str(sidecar_path),
            "sidecar_sha256": None,
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
        owned_cr3_paths.add(raw_path)
        rejected_capture["cr3_sha256"] = hashlib.sha256(raw_path.read_bytes()).hexdigest()
        run["physical_cr3_count"] += 1
        if run["physical_cr3_count"] > int(plan["budgets"]["physical_cr3_cap"]):
            raise RuntimeError("thermal diagnostic physical CR3 cap exceeded")
        _write_json(root / "run.json", run)
        if reported_physical != 1:
            rejected_capture["rejection_stage"] = "reported_physical_count_mismatch"
            raise RuntimeError("thermal capture reported physical count differs from one retained CR3")
        rejected_capture["rejection_stage"] = "sidecar_and_timing_validation"
        if (
            sidecar_path is None
            or not sidecar_path.is_relative_to(run_root)
            or sidecar_candidate is None
            or sidecar_candidate.is_symlink()
            or not sidecar_path.is_file()
            or sidecar_path.stat().st_size <= 0
            or sidecar_path != raw_path.with_suffix(raw_path.suffix + ".metadata.json")
        ):
            raise RuntimeError("capture adapter lacks the retained CR3 sidecar owner")
        rejected_capture["sidecar_sha256"] = hashlib.sha256(sidecar_path.read_bytes()).hexdigest()
        try:
            sidecar = json.loads(sidecar_path.read_text(encoding="utf-8"))
            remote_metadata, receipt = camera_remote_v2.split_and_validate_sidecar(
                sidecar, payload=raw_path.read_bytes(),
            )
        except (OSError, UnicodeError, json.JSONDecodeError, camera_remote_v2.RemoteCaptureV2Error) as exc:
            raise RuntimeError("capture adapter retained invalid CR3 sidecar evidence") from exc
        if capture.get("timing_metadata") != sidecar:
            raise RuntimeError("capture adapter timing metadata differs from retained sidecar")
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
        else:
            run["ambient_capture_count"] += 1
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
    from camera_based_rgbww_optimizer.optimization.hsi_objective import required_hsi_features_from_report
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

    raw_capture = raw_validation.build_native_raw_capture_step_fn(
        camera_dir=root / "camera", measurements_dir=root / "measurements", scratch_dir=root / "scratch",
        location_config_path=thermal.LOCATION_PATH, observer_config_path=thermal.OBSERVER_PATH,
        iso=str(resolved_settings.iso), aperture=str(resolved_settings.aperture),
        image_format=str(resolved_settings.image_format), camera_backend=camera_backend,
        recorded_exposure_purpose=str(plan["experiment_id"]),
        frozen_shutter_by_cache=plan["frozen_shutters"], timed_capture_fn=timed_capture,
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
            "analysis_context": {"phase": plan["stage"], "formal_measurement": bool(step["formal_measurement"])},
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
            output["feature_values"] = required_hsi_features_from_report(report, feature_ids)
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

    parser = argparse.ArgumentParser(description="Build or execute a frozen P7 thermal diagnostic plan.")
    parser.add_argument("--experiment-id", choices=thermal.EXPERIMENT_IDS, required=True)
    parser.add_argument("--source", choices=("ray", "strip"))
    parser.add_argument("--variant", choices=("core", "expansion"), default="core")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--run-name", required=True)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--dry-run", action="store_true")
    mode.add_argument("--execute", action="store_true")
    parser.add_argument("--allow-device-control", action="store_true")
    parser.add_argument("--human-authorization")
    camera_remote.add_camera_backend_arguments(parser, default="remote")
    return parser.parse_args(argv)


def main(
    argv: Sequence[str] | None = None, *,
    backend_factory: Callable[..., Any] | None = None,
    run_fn: Callable[..., Path] = run_authorized_plan,
) -> int:
    args = parse_args(argv)
    if args.dry_run:
        print(write_dry_run(
            experiment_id=args.experiment_id, output_dir=args.output_dir,
            run_name=args.run_name, source=args.source, variant=args.variant,
        ))
        return 0
    if not args.allow_device_control or args.human_authorization != args.experiment_id:
        raise PermissionError("--execute requires --allow-device-control and exact --human-authorization")
    if args.camera_backend != "remote":
        raise PermissionError("thermal diagnostics require the formal remote v2 camera backend")

    plan = thermal.build_diagnostic_plan(
        args.experiment_id, source=args.source, variant=args.variant,
        for_execution=True, human_authorization=args.human_authorization,
        v2_capture_capability=True,
    )
    validate_authorized_execution_plan(plan)
    if backend_factory is None:
        from camera_based_rgbww_optimizer.control import camera_remote
        backend_factory = camera_remote.create_camera_backend
    backend = backend_factory(
        args.camera_backend, env_file=args.remote_env_file,
        base_url=args.remote_base_url, timeout=args.remote_timeout,
    )
    print(run_fn(plan, output_dir=args.output_dir, run_name=args.run_name, camera_backend=backend))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
