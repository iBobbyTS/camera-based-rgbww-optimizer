from __future__ import annotations

import argparse
import copy
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
import time
from typing import Any, Callable, Mapping, Sequence

from camera_based_rgbww_optimizer.control import all_off, camera_gphoto2, camera_remote, esphome, ray120c
from camera_based_rgbww_optimizer.measurement.hsi_uncertainty import DEFAULT_P6_RUN
from camera_based_rgbww_optimizer.optimization import measure_raw_observer_validation as raw_validation
from camera_based_rgbww_optimizer.optimization.hsi_objective import (
    HsiRejectedFeaturesError,
    required_hsi_features_from_report,
)
from camera_based_rgbww_optimizer.optimization.measure_ray_hsi_manifold import _verify_readback

from camera_based_rgbww_optimizer.measurement.hsi_policy_v2 import (
    HsiPolicyV2,
    WAITING_STATUS,
)
from camera_based_rgbww_optimizer.measurement.ray_hsi_manifold import RayHsiManifold
from camera_based_rgbww_optimizer.paths import PROJECT_ROOT, PROJECT_TMP_DIR


EXPERIMENT_NAME = "p7_targeted_reference_repeatability_v2"
DEFAULT_SENTINEL_RUN = Path(
    "/Volumes/4T/temp/rgbww-optimizer/strip-hsi-pilot/"
    "p7-sentinel-4-20260717-223108-retry2"
)
DEFAULT_POLICY = PROJECT_ROOT / "config" / "hsi" / "strip-hsi-policy-v2-waiting.json"
DEFAULT_MANIFOLD = PROJECT_ROOT / "config" / "hsi" / "ray-hsi-manifold.json"
DEFAULT_LOCATION = PROJECT_ROOT / "config" / "location" / "locations-20260714-211759.json"
DEFAULT_OBSERVER = PROJECT_ROOT / "config" / "camera" / "raw-observer.json"
DEFAULT_CURVE = esphome.DEFAULT_CURVE_PATH
DEFAULT_OUTPUT = PROJECT_TMP_DIR / "hsi-reference-repeatability-offline"
RAY_STATES = ((0, 0), (120, 100), (300, 100))
STRIP_KEYS = (
    "h0-s0-fullscale", "h120-s100-fullscale", "h120-s50-fullscale",
    "h300-s100-fullscale", "h0-s0-scale-relaxed-3072",
)


def build_targeted_reference_repeatability_plan(
    *,
    sentinel_run: str | Path = DEFAULT_SENTINEL_RUN,
    policy_path: str | Path = DEFAULT_POLICY,
    manifold_path: str | Path = DEFAULT_MANIFOLD,
    location_path: str | Path = DEFAULT_LOCATION,
    observer_path: str | Path = DEFAULT_OBSERVER,
    target_max: int = 19661,
    min_shutter_speed: str = "1/16000",
    max_shutter_speed: str = "25",
    auto_exposure_max_trials: int = 12,
    curve_path: str | Path = DEFAULT_CURVE,
    p6_run: str | Path = DEFAULT_P6_RUN,
    named_experiment_authorization: str | None = None,
) -> dict[str, Any]:
    root = Path(sentinel_run)
    policy = HsiPolicyV2.load(policy_path)
    if policy.artifact.get("status") != WAITING_STATUS or policy.formal_capture_eligible:
        raise ValueError("P7-R1 draft requires the P7-R0 waiting policy, not a capture-ready artifact")
    manifold = RayHsiManifold.load(manifold_path)
    if policy.artifact["feature_set"]["ids"] != list(manifold.coordinate_feature_ids):
        raise ValueError("P7-R1 policy/manifold feature order mismatch")
    run = _load_json(root / "run.json")
    if run.get("status") != "complete" or run.get("target_set") != "sentinel":
        raise ValueError("P7-R1 draft requires the completed frozen sentinel diagnostic")
    rows = _load_jsonl(root / "target-results.jsonl")
    commands = _extract_commands(rows)
    captures: list[dict[str, Any]] = []

    def add_ambient(position: str) -> None:
        captures.append({
            "capture_id": f"{len(captures):04d}-ambient-{position}",
            "source": "ambient", "formal_measurement": False,
            "position": position, "sources_required_off": ["strip", "ray"],
        })

    def add_ray(block: str, order: Sequence[tuple[int, int]]) -> None:
        for repeat_index, (hue, sat) in enumerate(order):
            captures.append({
                "capture_id": f"{len(captures):04d}-ray-{block.lower()}-h{hue}-s{sat}-r{repeat_index // 3}",
                "source": "ray", "formal_measurement": True, "block": block,
                "repeat_index": repeat_index // 3, "state": {"hue": hue, "sat": sat, "intensity_percent": 100.0},
                "exposure_cache_key": f"ray-h{hue}-s{sat}",
                "settling": {"off_seconds": 1.0, "on_seconds": 60.0, "independent_off_on": True},
                "source_isolation": {"strip": "all_zero", "ray": "exact_hsi_readback"},
            })

    def add_strip(block: str, order: Sequence[str]) -> None:
        seen: dict[str, int] = {}
        for key in order:
            repeat_index = seen.get(key, 0)
            seen[key] = repeat_index + 1
            captures.append({
                "capture_id": f"{len(captures):04d}-strip-{block.lower()}-{key}-r{repeat_index}",
                "source": "strip", "formal_measurement": True, "block": block,
                "repeat_index": repeat_index, "command_key": key,
                "command": commands[key], "exposure_cache_key": f"strip-{key}",
                "settling": {"off_seconds": 1.0, "on_seconds": 60.0, "independent_off_on": True},
                "source_isolation": {"ray": "intensity_zero", "strip": "exact_five_channel_readback"},
            })

    add_ambient("start")
    add_ray("A", _balanced_ray_order(reverse=False))
    add_strip("A", _balanced_strip_order(reverse=False))
    add_strip("B", _balanced_strip_order(reverse=True))
    add_ray("B", _balanced_ray_order(reverse=True))
    add_ambient("end")
    formal_ray = sum(item["source"] == "ray" and item["formal_measurement"] for item in captures)
    formal_strip = sum(item["source"] == "strip" and item["formal_measurement"] for item in captures)
    if formal_ray != 30 or formal_strip != 50 or len(captures) != 82:
        raise AssertionError("P7-R1 frozen 30+50 plan construction drift")
    return {
        "schema_version": 2,
        "status": "dry_run_draft_requires_planner_acceptance_and_named_authorization",
        "experiment": EXPERIMENT_NAME,
        "authorization": (
            {"status": "named_experiment_authorized", "experiment": EXPERIMENT_NAME}
            if named_experiment_authorization == EXPERIMENT_NAME
            else {"status": "not_authorized_for_execution", "experiment": None}
        ),
        "formal_capture_eligible": False,
        "created_at": _utc_now(),
        "inputs": {
            "sentinel_run_json": _file_reference(root / "run.json"),
            "sentinel_plan_json": _file_reference(root / "plan.json"),
            "sentinel_target_results": _file_reference(root / "target-results.jsonl"),
            "policy_v2_waiting": _file_reference(Path(policy_path)),
            "ray_hsi_manifold": _file_reference(Path(manifold_path)),
            "location_config": _file_reference(Path(location_path)),
            "raw_observer_config": _file_reference(Path(observer_path)),
            "code_duty_curve": _file_reference(Path(curve_path)),
            "p6_run_json": _file_reference(Path(p6_run) / "run.json"),
            "p6_captures": _file_reference(Path(p6_run) / "captures.jsonl"),
        },
        "measurement": {
            "formal_ray_count": formal_ray,
            "formal_strip_count": formal_strip,
            "formal_total": formal_ray + formal_strip,
            "ambient_count": 2,
            "planned_capture_count_excluding_auto_exposure_trials": len(captures),
            "sequence": ["start_ambient", "ray_A", "strip_A", "strip_B", "ray_B", "end_ambient"],
            "camera_backend": "remote",
            "location_mode": "latest_frozen",
            "recorded_exposure_required": True,
            "retain_npy": False,
            "auto_exposure": {
                "target_max": int(target_max), "minimum_shutter": min_shutter_speed,
                "maximum_shutter": max_shutter_speed, "maximum_trials_per_cache_miss": int(auto_exposure_max_trials),
                "cache_policy": "per exact Ray state and per exact strip command; B restores A cache",
            },
            "physical_capture_audit": {
                "unique_autoexposure_cache_misses": 8,
                "maximum_physical_per_cache_miss": int(auto_exposure_max_trials),
                "maximum_autoexposure_physical_cr3": 8 * int(auto_exposure_max_trials),
                "maximum_extra_physical_cr3": 8 * (int(auto_exposure_max_trials) - 1),
                "maximum_weak_signal_reacquire_cr3": 80,
                "maximum_total_physical_cr3": len(captures) + 8 * (int(auto_exposure_max_trials) - 1) + 80,
                "expected_physical_cr3_range": [len(captures), len(captures) + 8 * (int(auto_exposure_max_trials) - 1)],
                "absolute_cap_status": "proposed_not_frozen",
                "maximum_60_second_settling_events": formal_ray + formal_strip + 80,
                "maximum_60_second_settling_seconds": 60 * (formal_ray + formal_strip + 80),
            },
        },
        "commands": commands,
        "captures": captures,
        "cleanup": {
            "python": "required_all_off_strip_and_ray",
            "shell": "required_independent_trap_all_off_strip_and_ray",
        },
        "offline_contract": {
            "env_loaded": False, "network_calls": 0, "camera_calls": 0,
            "ray_calls": 0, "esphome_calls": 0, "all_off_calls": 0,
        },
        "execution_contract": {
            "named_experiment": EXPERIMENT_NAME,
            "authorized": named_experiment_authorization == EXPERIMENT_NAME,
            "remote_only": True,
            "formal_measurement_count_exact": 80,
            "planned_logical_capture_count_exact": 82,
            "candidate_status": "calibrated_waiting_for_planner",
            "candidate_formal_capture_eligible": False,
        },
        "locked_next_steps": ["execute", "new_sentinel", "remaining_9", "boundary", "holdout", "P8"],
    }


def write_dry_run(
    *, output_root: str | Path = DEFAULT_OUTPUT, run_name: str | None = None,
    **kwargs: Any,
) -> Path:
    root = Path(output_root) / (run_name or datetime.now().strftime("p7-r1-draft-%Y%m%d-%H%M%S"))
    root.mkdir(parents=True, exist_ok=False)
    plan = build_targeted_reference_repeatability_plan(**kwargs)
    output = root / "plan.json"
    output.write_text(json.dumps(plan, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8")
    return output


def execute_targeted_reference_repeatability_plan(
    plan: Mapping[str, Any], *, run_dir: str | Path,
    capture_step_fn: Callable[[Mapping[str, Any]], Mapping[str, Any]],
    strip_light_fn: Callable[..., Mapping[str, Any]],
    ray_off_fn: Callable[[], Mapping[str, Any]],
    ray_set_hsi_fn: Callable[..., Mapping[str, Any]],
    ray_get_hsi_fn: Callable[[], Mapping[str, Any]],
    sleep_fn: Callable[[float], None] = time.sleep,
    all_off_fn: Callable[..., Sequence[all_off.ShutdownStep]] = all_off.turn_everything_off,
    provenance_fn: Callable[[], Mapping[str, Any]] | None = None,
) -> Path:
    plan_data = copy.deepcopy(dict(plan))
    contract = plan_data.get("execution_contract", {})
    if plan_data.get("experiment") != EXPERIMENT_NAME or not contract.get("authorized"):
        raise ValueError("P7-R1 execution requires exact named-experiment authorization")
    if plan_data.get("measurement", {}).get("camera_backend") != "remote":
        raise ValueError("P7-R1 execution is remote-camera-only")
    if len(plan_data.get("captures", [])) != 82:
        raise ValueError("P7-R1 execution requires the exact 82-capture logical plan")
    _verify_input_hashes(plan_data["inputs"])
    policy = HsiPolicyV2.load(plan_data["inputs"]["policy_v2_waiting"]["path"])
    if policy.artifact["status"] != WAITING_STATUS or policy.formal_capture_eligible:
        raise ValueError("P7-R1 calibration must start from the formal-ineligible waiting policy")
    feature_ids = tuple(policy.artifact["feature_set"]["ids"])
    curve = _load_json(Path(plan_data["inputs"]["code_duty_curve"]["path"]))
    root = Path(run_dir)
    root.mkdir(parents=True, exist_ok=True)
    if any(root.iterdir()):
        raise FileExistsError(f"run directory must be empty: {root}")
    _write_json(root / "plan.json", plan_data)
    run = {
        "schema_version": 2,
        "experiment": EXPERIMENT_NAME,
        "status": "running",
        "started_at": _utc_now(),
        "finished_at": None,
        "logical_captures_completed": 0,
        "formal_captures_completed": 0,
        "physical_cr3_count": 0,
        "base_physical_cr3_count": 0,
        "auto_exposure_physical_cr3_count": 0,
        "auto_exposure_cache_miss_count": 0,
        "weak_signal_reacquire_count": 0,
        "weak_signal_reacquire_physical_cr3_count": 0,
        "inputs": plan_data["inputs"],
        "provenance": {"status": "pending" if provenance_fn else "not_collected"},
    }
    _write_json(root / "run.json", run)
    exposure_ready: set[str] = set()
    failure: BaseException | None = None

    def both_off(capture_id: str) -> None:
        strip = strip_light_fn(0, 0, 0, 0, 0)
        ray = ray_off_fn()
        _append_jsonl(root / "commands.jsonl", {
            "at": _utc_now(), "event": "both_off", "capture_id": capture_id,
            "strip_response": dict(strip), "ray_response": dict(ray),
        })

    def acquire(step: Mapping[str, Any]) -> dict[str, Any]:
        capture_id = str(step["capture_id"])
        base_attempt_id = f"{capture_id}-base"
        source = str(step["source"])
        audit = plan_data["measurement"]["physical_capture_audit"]
        maximum_physical = int(audit["maximum_total_physical_cr3"])
        maximum_auto = int(audit["maximum_autoexposure_physical_cr3"])
        maximum_weak = int(audit["maximum_weak_signal_reacquire_cr3"])
        both_off(base_attempt_id)
        settling = step.get("settling") or {"off_seconds": 1.0, "on_seconds": 0.0}
        sleep_fn(float(settling.get("off_seconds", 1.0)))
        readback = None
        if source == "ray":
            state = step["state"]
            set_response = ray_set_hsi_fn(
                int(state["hue"]), int(state["sat"]),
                intensity_percent=float(state["intensity_percent"]),
            )
            readback = ray_get_hsi_fn()
            expected = {
                "hue": int(state["hue"]), "sat": int(state["sat"]),
                "intensity": ray120c.intensity_percent_to_raw(float(state["intensity_percent"])),
            }
            _verify_readback(readback, expected, mode="hsi")
            _append_jsonl(root / "commands.jsonl", {
                "at": _utc_now(), "event": "ray_on_readback_verified", "capture_id": base_attempt_id,
                "expected": expected, "set_response": dict(set_response), "readback": dict(readback),
            })
        elif source == "strip":
            command = {channel: int(step["command"][channel]) for channel in ("cw", "ww", "r", "g", "b")}
            response = strip_light_fn(*(command[channel] for channel in ("cw", "ww", "r", "g", "b")))
            expected = esphome._build_payload(*(command[channel] for channel in ("cw", "ww", "r", "g", "b")), curve=curve)
            if dict(response) not in (command, expected):
                raise RuntimeError(f"strip command response mismatch for {capture_id}")
            readback = dict(response)
            _append_jsonl(root / "commands.jsonl", {
                "at": _utc_now(), "event": "strip_on_readback_verified", "capture_id": base_attempt_id,
                "requested_command": command, "expected_response": expected,
                "response": dict(response), "response_verified": True,
            })
        sleep_fn(float(settling.get("on_seconds", 0.0)))
        cache_key = step.get("exposure_cache_key")
        auto_exposure = source != "ambient" and cache_key not in exposure_ready
        remaining_global = maximum_physical - int(run["physical_cr3_count"])
        remaining_auto = maximum_auto - int(run["auto_exposure_physical_cr3_count"])
        adapter_remaining = min(remaining_global, remaining_auto) if auto_exposure else remaining_global
        if adapter_remaining < 1:
            raise RuntimeError("P7-R1 physical CR3 budget exhausted before base capture")
        capture_step = {
            **dict(step),
            "capture_id": base_attempt_id,
            "index": int(str(capture_id).split("-", 1)[0]),
            "purpose": f"reference_repeatability_{source}",
            "repeat_index": step.get("repeat_index"),
            "source_exposure_cache": cache_key,
            "auto_exposure": auto_exposure,
            "physical_capture_budget_remaining": adapter_remaining,
            "exposure_factor": None,
            "other_source_must_be_off": True,
            "ray": step.get("state") if source == "ray" else None,
            "strip_command": step.get("command") if source == "strip" else None,
            "analysis_context": {"phase": "P7-R1", "formal_measurement": bool(step.get("formal_measurement"))},
        }
        try:
            capture = dict(capture_step_fn(capture_step))
            if cache_key is not None:
                exposure_ready.add(str(cache_key))
        finally:
            both_off(base_attempt_id)
        physical = int(capture.get("physical_capture_count", 1))
        if physical < 1 or physical > adapter_remaining:
            raise RuntimeError("P7-R1 capture adapter returned invalid physical count")
        run["physical_cr3_count"] += physical
        run["base_physical_cr3_count"] += physical
        if auto_exposure:
            run["auto_exposure_physical_cr3_count"] += physical
            run["auto_exposure_cache_miss_count"] += 1
        report = _load_json(Path(capture["patch_statistics"]))
        features = None
        attempts = [{
            "logical_capture_id": capture_id,
            "attempt_capture_id": base_attempt_id,
            "attempt_kind": "base",
            "source": source,
            "selected_for_formal": False,
            "readback": readback,
            "capture": capture,
            "physical_capture_count": physical,
            "auto_exposure": auto_exposure,
            "auto_exposure_audit": capture.get("auto_exposure_audit"),
            "settling": dict(settling),
            "quality_rejection": None,
        }]
        try:
            if source != "ambient":
                features = required_hsi_features_from_report(report, feature_ids)
        except HsiRejectedFeaturesError as exc:
            if source == "ambient" or not exc.weak_signal_only:
                raise
            attempts[0]["quality_rejection"] = {
                "weak_signal_only": bool(exc.weak_signal_only),
                "rejected_features": copy.deepcopy(exc.rejected),
            }
            reacquire_id = f"{capture_id}-weak-signal-reacquire"
            if int(run["physical_cr3_count"]) >= maximum_physical or int(run["weak_signal_reacquire_physical_cr3_count"]) >= maximum_weak:
                raise RuntimeError("P7-R1 physical CR3 budget exhausted before weak reacquire")
            reacquire_step = {
                **capture_step,
                "capture_id": reacquire_id,
                "purpose": f"reference_repeatability_{source}_weak_signal_reacquire",
                "auto_exposure": False,
                "exposure_factor": 1.25,
                "formal_measurement": False,
                "reacquire_of": capture_id,
                "physical_capture_budget_remaining": 1,
            }
            both_off(reacquire_id)
            sleep_fn(float(settling.get("off_seconds", 1.0)))
            if source == "ray":
                state = step["state"]
                set_response = ray_set_hsi_fn(
                    int(state["hue"]), int(state["sat"]),
                    intensity_percent=float(state["intensity_percent"]),
                )
                reacquire_readback = ray_get_hsi_fn()
                expected = {
                    "hue": int(state["hue"]), "sat": int(state["sat"]),
                    "intensity": ray120c.intensity_percent_to_raw(float(state["intensity_percent"])),
                }
                _verify_readback(reacquire_readback, expected, mode="hsi")
                _append_jsonl(root / "commands.jsonl", {
                    "at": _utc_now(), "event": "ray_reacquire_on_readback_verified",
                    "capture_id": reacquire_id, "expected": expected,
                    "set_response": dict(set_response), "readback": dict(reacquire_readback),
                })
            else:
                command = {channel: int(step["command"][channel]) for channel in ("cw", "ww", "r", "g", "b")}
                response = strip_light_fn(*(command[channel] for channel in ("cw", "ww", "r", "g", "b")))
                expected = esphome._build_payload(*(command[channel] for channel in ("cw", "ww", "r", "g", "b")), curve=curve)
                if dict(response) not in (command, expected):
                    raise RuntimeError(f"strip reacquire response mismatch for {capture_id}")
                _append_jsonl(root / "commands.jsonl", {
                    "at": _utc_now(), "event": "strip_reacquire_on_readback_verified",
                    "capture_id": reacquire_id, "requested_command": command,
                    "expected_response": expected, "response": dict(response), "response_verified": True,
                })
            sleep_fn(float(settling.get("on_seconds", 0.0)))
            try:
                reacquired = dict(capture_step_fn(reacquire_step))
            finally:
                both_off(reacquire_id)
            reacquired_physical = int(reacquired.get("physical_capture_count", 1))
            if reacquired_physical != 1:
                raise RuntimeError("P7-R1 weak reacquire must consume exactly one physical CR3")
            run["physical_cr3_count"] += reacquired_physical
            run["weak_signal_reacquire_count"] += 1
            run["weak_signal_reacquire_physical_cr3_count"] += reacquired_physical
            report = _load_json(Path(reacquired["patch_statistics"]))
            features = required_hsi_features_from_report(report, feature_ids)
            capture = reacquired
            readback = reacquire_readback if source == "ray" else dict(response)
            attempts.append({
                "logical_capture_id": capture_id,
                "attempt_capture_id": reacquire_id,
                "attempt_kind": "weak_signal_reacquire",
                "source": source,
                "selected_for_formal": True,
                "readback": readback,
                "capture": reacquired,
                "physical_capture_count": reacquired_physical,
                "auto_exposure": False,
                "auto_exposure_audit": None,
                "settling": dict(settling),
                "quality_rejection": None,
            })
        else:
            attempts[0]["selected_for_formal"] = True
        if run["physical_cr3_count"] > maximum_physical:
            raise AssertionError("P7-R1 pre-call physical cap invariant failed")
        for attempt in attempts:
            _append_jsonl(root / "capture-attempts.jsonl", attempt)
        selected_attempt = next(item for item in attempts if item["selected_for_formal"])
        record = {
            "capture_id": capture_id,
            "source": source,
            "formal_measurement": bool(step.get("formal_measurement")),
            "plan_step": dict(step),
            "readback": readback,
            "capture": capture,
            "feature_values": features,
            "attempt_capture_ids": [item["attempt_capture_id"] for item in attempts],
            "selected_attempt_capture_id": selected_attempt["attempt_capture_id"],
        }
        _append_jsonl(root / "captures.jsonl", record)
        return record

    try:
        if provenance_fn is not None:
            provenance = provenance_fn()
            if not isinstance(provenance, Mapping):
                raise TypeError("P7-R1 provenance collector must return a mapping")
            run["provenance"] = dict(provenance)
        for step in plan_data["captures"]:
            acquire(step)
            run["logical_captures_completed"] += 1
            if step.get("formal_measurement"):
                run["formal_captures_completed"] += 1
            _write_json(root / "run.json", run)
    except BaseException as exc:
        failure = exc
        run["status"] = "interrupted" if isinstance(exc, KeyboardInterrupt) else "failed"
        _write_json(root / "failure.json", {"at": _utc_now(), "type": type(exc).__name__, "message": str(exc)})
    finally:
        cleanup = {"at": _utc_now(), "steps": [step.to_jsonable() for step in all_off_fn()]}
        _write_json(root / "all-off-python.json", cleanup)
        if run["status"] == "running":
            run["status"] = "complete" if (
                run["logical_captures_completed"] == 82
                and run["formal_captures_completed"] == 80
                and all(item["ok"] for item in cleanup["steps"])
            ) else "failed"
        run["finished_at"] = _utc_now()
        _write_json(root / "run.json", run)
    if failure is not None:
        raise failure
    if run["status"] != "complete":
        raise RuntimeError("P7-R1 did not complete the exact plan with successful Python cleanup")
    return root


def run_targeted_reference_repeatability(
    plan: Mapping[str, Any], *, output_root: str | Path, run_name: str | None,
    curve_path: str | Path, camera_backend: camera_gphoto2.CameraBackend,
) -> Path:
    root = Path(output_root) / (run_name or datetime.now().strftime("p7-r1-%Y%m%d-%H%M%S"))
    capture_step = raw_validation.build_native_raw_capture_step_fn(
        camera_dir=root / "camera", measurements_dir=root / "measurements",
        scratch_dir=root / "scratch",
        location_config_path=plan["inputs"]["location_config"]["path"],
        observer_config_path=plan["inputs"]["raw_observer_config"]["path"],
        target_max=int(plan["measurement"]["auto_exposure"]["target_max"]),
        min_shutter_speed=str(plan["measurement"]["auto_exposure"]["minimum_shutter"]),
        max_shutter_speed=str(plan["measurement"]["auto_exposure"]["maximum_shutter"]),
        max_trials=int(plan["measurement"]["auto_exposure"]["maximum_trials_per_cache_miss"]),
        max_captures=int(plan["measurement"]["auto_exposure"]["maximum_trials_per_cache_miss"]),
        camera_backend=camera_backend,
        recorded_exposure_purpose="P7-R1",
    )
    return execute_targeted_reference_repeatability_plan(
        plan, run_dir=root, capture_step_fn=capture_step,
        strip_light_fn=lambda cw, ww, r, g, b: esphome.light(cw, ww, r, g, b, curve_path=curve_path),
        ray_off_fn=lambda: ray120c.set_cct(5600, intensity=0, gm=100),
        ray_set_hsi_fn=ray120c.set_hsi, ray_get_hsi_fn=ray120c.get_hsi,
        provenance_fn=lambda: raw_validation.collect_native_raw_observer_provenance(
            curve_path=curve_path, camera_backend=camera_backend, backend_name="remote",
        ),
    )


def _extract_commands(rows: Sequence[Mapping[str, Any]]) -> dict[str, dict[str, int]]:
    by_target = {(int(row["target"]["hue"]), int(row["target"]["sat"])): row for row in rows}
    mapping = {
        "h0-s0-fullscale": ((0, 0), None),
        "h120-s100-fullscale": ((120, 100), None),
        "h120-s50-fullscale": ((120, 50), None),
        "h300-s100-fullscale": ((300, 100), None),
        "h0-s0-scale-relaxed-3072": ((0, 0), 3072),
    }
    output = {}
    for name, (key, diagnostic_max) in mapping.items():
        row = by_target[key]
        if diagnostic_max is None:
            command = row["selected_command"]
        else:
            matches = [item for item in row.get("scale_relaxed_diagnostics", []) if int(item.get("max_code", -1)) == diagnostic_max]
            if len(matches) != 1 or not matches[0].get("selected_command"):
                raise ValueError(f"sentinel lacks exact diagnostic command for {name}")
            command = matches[0]["selected_command"]
        normalized = {channel: int(command[channel]) for channel in ("cw", "ww", "r", "g", "b")}
        expected_max = 4095 if diagnostic_max is None else diagnostic_max
        if max(normalized.values()) != expected_max:
            raise ValueError(f"sentinel command {name} violates frozen max-code policy")
        output[name] = normalized
    return output


def _balanced_ray_order(*, reverse: bool) -> list[tuple[int, int]]:
    states = list(reversed(RAY_STATES)) if reverse else list(RAY_STATES)
    return [states[(index + shift) % len(states)] for shift in range(5) for index in range(len(states))]


def _balanced_strip_order(*, reverse: bool) -> list[str]:
    states = list(reversed(STRIP_KEYS)) if reverse else list(STRIP_KEYS)
    return [states[(index + shift) % len(states)] for shift in range(5) for index in range(len(states))]


def _file_reference(path: Path) -> dict[str, str]:
    return {"path": str(path), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


def _verify_input_hashes(inputs: Mapping[str, Any]) -> None:
    for reference in inputs.values():
        path = Path(reference["path"])
        if hashlib.sha256(path.read_bytes()).hexdigest() != reference["sha256"]:
            raise ValueError(f"P7-R1 input hash drift for {path}")


def _write_json(path: Path, value: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8")


def _append_jsonl(path: Path, value: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(value, sort_keys=True, allow_nan=False) + "\n")


def _load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build the offline-only P7-R1 named-experiment draft.")
    parser.add_argument("--sentinel-run", type=Path, default=DEFAULT_SENTINEL_RUN)
    parser.add_argument("--policy-v2", type=Path, default=DEFAULT_POLICY)
    parser.add_argument("--manifold", type=Path, default=DEFAULT_MANIFOLD)
    parser.add_argument("--location", type=Path, default=DEFAULT_LOCATION)
    parser.add_argument("--observer", type=Path, default=DEFAULT_OBSERVER)
    parser.add_argument("--curve", type=Path, default=DEFAULT_CURVE)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--run-name")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--dry-run", action="store_true")
    mode.add_argument("--execute", action="store_true")
    parser.add_argument("--allow-high-output", action="store_true")
    parser.add_argument("--named-experiment")
    camera_remote.add_camera_backend_arguments(parser, default="remote")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    kwargs = {
        "sentinel_run": args.sentinel_run, "policy_path": args.policy_v2,
        "manifold_path": args.manifold, "location_path": args.location,
        "observer_path": args.observer, "curve_path": args.curve,
        "named_experiment_authorization": args.named_experiment,
    }
    if args.dry_run:
        print(write_dry_run(output_root=args.output_dir, run_name=args.run_name, **kwargs))
        return 0
    if not args.allow_high_output or args.named_experiment != EXPERIMENT_NAME:
        raise ValueError(f"--execute requires --allow-high-output --named-experiment {EXPERIMENT_NAME}")
    backend = camera_remote.create_camera_backend(
        args.camera_backend, env_file=args.remote_env_file,
        base_url=args.remote_base_url, timeout=args.remote_timeout,
    )
    plan = build_targeted_reference_repeatability_plan(**kwargs)
    print(run_targeted_reference_repeatability(
        plan, output_root=args.output_dir, run_name=args.run_name,
        curve_path=args.curve, camera_backend=backend,
    ))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
