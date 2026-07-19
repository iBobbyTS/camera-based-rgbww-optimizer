from __future__ import annotations

import argparse
import json
import os
import signal
import sys
from collections.abc import Callable, Mapping, Sequence
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from camera_based_rgbww_optimizer.control import all_off, esphome


EXPERIMENT_ID = "p7_strip_state_readback_preflight"
PHASE = "P7-D0"
STATE_TIMEOUT_SECONDS = 5.0
EXPECTED_DEVICE_NAME = esphome.DEFAULT_EXPECTED_NAME
ZERO_ARGUMENTS = {"cw": 0, "ww": 0, "r": 0, "g": 0, "b": 0}
LOW_ARGUMENTS = {"cw": 8, "ww": 16, "r": 24, "g": 32, "b": 48}
PAYLOAD_KEYS = ("red", "green", "blue", "warm_white", "cold_white")
TRANSITION_STEPS = (
    ("startup_zero", ZERO_ARGUMENTS),
    ("low_first", LOW_ARGUMENTS),
    ("low_repeat", LOW_ARGUMENTS),
    ("main_zero", ZERO_ARGUMENTS),
    ("final_zero", ZERO_ARGUMENTS),
)

VerifiedLightFn = Callable[..., Mapping[str, Any]]
CleanupFn = Callable[[], Sequence[Any]]


class PreflightFailure(RuntimeError):
    def __init__(self, branch: str, message: str):
        super().__init__(message)
        self.branch = branch


class PreflightRunFailed(RuntimeError):
    pass


def build_plan() -> dict[str, Any]:
    transitions = []
    for step_id, arguments in TRANSITION_STEPS:
        transitions.append({
            "step_id": step_id,
            "argument_order": ["cw", "ww", "r", "g", "b"],
            "arguments": dict(arguments),
            "expected_device_payload": _payload_for(arguments),
            "curve_path": None,
        })
    return {
        "schema_version": 1,
        "experiment": EXPERIMENT_ID,
        "phase": PHASE,
        "device": {
            "expected_name": EXPECTED_DEVICE_NAME,
            "state_entity_object_id": esphome.STATE_OBJECT_ID,
            "identity_policy": "exact_name_and_stable_nonempty_mac",
        },
        "output_policy": {
            "mode": "raw_pwm_calibration_bypass",
            "maximum_physical_pwm": max(LOW_ARGUMENTS.values()),
            "curve_path": None,
            "arbitrary_channel_cli_parameters": False,
        },
        "state_timeout_seconds": STATE_TIMEOUT_SECONDS,
        "transitions": transitions,
        "cleanup": {
            "preflight_all_off": True,
            "python_finally_all_off": True,
            "final_verified_zero_after_python_all_off": True,
            "shell_exit_int_term_hup_all_off": True,
            "ray_required_intensity": 0,
        },
        "prohibited": {
            "camera_calls": True,
            "cr3_outputs": True,
            "npy_outputs": True,
            "env_file_reads": True,
            "firmware_compile_or_upload": True,
            "p7_r1": True,
        },
    }


def write_dry_run(*, output_dir: Path, run_name: str) -> Path:
    run_dir = _prepare_run_dir(output_dir, run_name)
    plan = build_plan()
    _write_json_atomic(run_dir / "plan.json", plan)
    _write_json_atomic(run_dir / "run.json", {
        "schema_version": 1,
        "experiment": EXPERIMENT_ID,
        "phase": PHASE,
        "run_name": run_name,
        "status": "dry_run_complete",
        "device_calls_performed": False,
        "camera_calls_performed": False,
        "completed_transition_count": 0,
        "failure_branch": None,
    })
    return run_dir


def execute_preflight(
    *,
    output_dir: Path,
    run_name: str,
    verified_light_fn: VerifiedLightFn = esphome.verified_light,
    cleanup_fn: CleanupFn = all_off.turn_everything_off,
) -> Path:
    run_dir = _prepare_run_dir(output_dir, run_name)
    plan = build_plan()
    _write_json_atomic(run_dir / "plan.json", plan)
    started_at = _now()
    run: dict[str, Any] = {
        "schema_version": 1,
        "experiment": EXPERIMENT_ID,
        "phase": PHASE,
        "run_name": run_name,
        "status": "running",
        "started_at": started_at,
        "finished_at": None,
        "process_id": os.getpid(),
        "completed_transition_count": 0,
        "first_generation": None,
        "last_generation": None,
        "device_identity": None,
        "failure_branch": None,
        "cleanup": {
            "preflight": "pending",
            "python_finally": "pending",
            "final_verified_zero": "pending",
            "shell_trap": "external_pending",
        },
        "device_calls_performed": True,
        "camera_calls_performed": False,
    }
    _write_json_atomic(run_dir / "run.json", run)

    previous_generation: int | None = None
    stable_identity: dict[str, str] | None = None
    completed = 0
    first_generation: int | None = None
    primary_failure: dict[str, str] | None = None
    cleanup_failure: dict[str, str] | None = None

    try:
        preflight_steps = _serialize_shutdown_steps(cleanup_fn())
        _write_json_atomic(run_dir / "preflight-all-off.json", preflight_steps)
        _validate_shutdown_steps(preflight_steps)
        run["cleanup"]["preflight"] = "pass"

        for step_id, arguments in TRANSITION_STEPS[:-1]:
            record, stable_identity, previous_generation = _perform_transition(
                step_id=step_id,
                arguments=arguments,
                verified_light_fn=verified_light_fn,
                stable_identity=stable_identity,
                previous_generation=previous_generation,
                record_path=run_dir / "transitions.jsonl",
            )
            completed += 1
            if first_generation is None:
                first_generation = previous_generation
    except BaseException as exc:
        failure = _as_preflight_failure(exc)
        primary_failure = _failure_record(failure)
    finally:
        try:
            python_steps = _serialize_shutdown_steps(cleanup_fn())
            _write_json_atomic(run_dir / "all-off-python.json", python_steps)
            _validate_shutdown_steps(python_steps)
            run["cleanup"]["python_finally"] = "pass"
        except BaseException as exc:
            cleanup_failure = _failure_record(PreflightFailure(
                "D0-CLEANUP-UNKNOWN", f"Python all-off failed validation: {type(exc).__name__}: {exc}",
            ))
            run["cleanup"]["python_finally"] = "fail"

        try:
            record, stable_identity, previous_generation = _perform_transition(
                step_id="final_zero",
                arguments=ZERO_ARGUMENTS,
                verified_light_fn=verified_light_fn,
                stable_identity=stable_identity,
                previous_generation=previous_generation,
                record_path=run_dir / "transitions.jsonl",
            )
            _write_json_atomic(run_dir / "final-zero.json", record)
            run["cleanup"]["final_verified_zero"] = "pass"
            completed += 1
            if first_generation is None:
                first_generation = previous_generation
        except BaseException as exc:
            final_failure = PreflightFailure(
                "D0-CLEANUP-UNKNOWN", f"Final verified zero failed: {type(exc).__name__}: {exc}",
            )
            _write_json_atomic(run_dir / "final-zero.json", {
                "schema_version": 1,
                "step_id": "final_zero",
                "status": "failed",
                "error": _failure_record(final_failure),
                "recorded_at": _now(),
            })
            cleanup_failure = _failure_record(final_failure)
            run["cleanup"]["final_verified_zero"] = "fail"

    if cleanup_failure is not None:
        status = "cleanup_state_unknown"
        failure_branch = "D0-CLEANUP-UNKNOWN"
    elif primary_failure is not None:
        status = "failed"
        failure_branch = primary_failure["branch"]
    else:
        status = "complete"
        failure_branch = None

    run.update({
        "status": status,
        "finished_at": _now(),
        "completed_transition_count": completed,
        "first_generation": first_generation,
        "last_generation": previous_generation,
        "device_identity": stable_identity,
        "failure_branch": failure_branch,
    })
    _write_json_atomic(run_dir / "run.json", run)
    if failure_branch is not None:
        failure_artifact = {
            "schema_version": 1,
            "experiment": EXPERIMENT_ID,
            "branch": failure_branch,
            "primary_failure": primary_failure,
            "cleanup_failure": cleanup_failure,
            "recorded_at": _now(),
        }
        _write_json_atomic(run_dir / "failure.json", failure_artifact)
        raise PreflightRunFailed(f"{failure_branch}: retained failure evidence in {run_dir}")
    return run_dir


def _perform_transition(
    *,
    step_id: str,
    arguments: Mapping[str, int],
    verified_light_fn: VerifiedLightFn,
    stable_identity: dict[str, str] | None,
    previous_generation: int | None,
    record_path: Path,
) -> tuple[dict[str, Any], dict[str, str], int]:
    try:
        evidence = dict(verified_light_fn(
            arguments["cw"], arguments["ww"], arguments["r"], arguments["g"], arguments["b"],
            curve_path=None,
            expected_name=EXPECTED_DEVICE_NAME,
            state_timeout=STATE_TIMEOUT_SECONDS,
        ))
    except BaseException as exc:
        failure = _classify_device_exception(exc)
        _append_jsonl(record_path, {
            "schema_version": 1,
            "step_id": step_id,
            "status": "failed",
            "arguments": dict(arguments),
            "curve_path": None,
            "expected_device_payload": _payload_for(arguments),
            "error": _failure_record(failure),
            "recorded_at": _now(),
        })
        raise failure from exc
    record = {
        "schema_version": 1,
        "step_id": step_id,
        "arguments": dict(arguments),
        "curve_path": None,
        "evidence": evidence,
        "recorded_at": _now(),
    }
    try:
        identity, generation = _validate_transition_evidence(
            evidence,
            step_id=step_id,
            expected_payload=_payload_for(arguments),
            stable_identity=stable_identity,
            previous_generation=previous_generation,
        )
    except PreflightFailure as exc:
        record["status"] = "failed"
        record["error"] = _failure_record(exc)
        _append_jsonl(record_path, record)
        raise
    record["status"] = "pass"
    _append_jsonl(record_path, record)
    return record, identity, generation


def _validate_transition_evidence(
    evidence: Mapping[str, Any],
    *,
    step_id: str,
    expected_payload: Mapping[str, int],
    stable_identity: dict[str, str] | None,
    previous_generation: int | None,
) -> tuple[dict[str, str], int]:
    if evidence.get("schema_version") != 1:
        raise PreflightFailure("D0-READBACK", f"{step_id} has unsupported verified-light schema")
    entity = evidence.get("device_state_entity")
    if not isinstance(entity, Mapping) or entity.get("object_id") != esphome.STATE_OBJECT_ID:
        raise PreflightFailure("D0-FIRMWARE-MISSING", f"{step_id} lacks the frozen device-state entity")
    identity_raw = evidence.get("device_identity")
    if not isinstance(identity_raw, Mapping):
        raise PreflightFailure("D0-DEVICE/IDENTITY", f"{step_id} lacks device identity")
    identity = {
        "name": str(identity_raw.get("name", "")),
        "mac_address": str(identity_raw.get("mac_address", "")),
    }
    if identity["name"] != EXPECTED_DEVICE_NAME or not identity["mac_address"]:
        raise PreflightFailure("D0-DEVICE/IDENTITY", f"{step_id} device identity is not exact/nonempty")
    if stable_identity is not None and identity != stable_identity:
        raise PreflightFailure("D0-DEVICE/IDENTITY", f"{step_id} device identity drifted")

    requested = evidence.get("requested_payload")
    baseline = evidence.get("baseline_snapshot")
    observed = evidence.get("device_snapshot")
    if requested != dict(expected_payload):
        raise PreflightFailure("D0-READBACK", f"{step_id} requested payload drifted")
    if not isinstance(baseline, Mapping) or not isinstance(observed, Mapping):
        raise PreflightFailure("D0-READBACK", f"{step_id} lacks baseline/device snapshots")
    if baseline.get("schema_version") != 1 or observed.get("schema_version") != 1:
        raise PreflightFailure("D0-READBACK", f"{step_id} snapshot schema drifted")
    try:
        baseline_generation = int(baseline["generation"])
        generation = int(observed["generation"])
    except (KeyError, TypeError, ValueError) as exc:
        raise PreflightFailure("D0-READBACK", f"{step_id} has invalid generation evidence") from exc
    if generation <= baseline_generation:
        raise PreflightFailure("D0-READBACK", f"{step_id} generation did not exceed its baseline")
    if previous_generation is not None and generation <= previous_generation:
        raise PreflightFailure("D0-READBACK", f"{step_id} generation did not increase globally")
    observed_payload = {key: observed.get(key) for key in PAYLOAD_KEYS}
    if observed_payload != dict(expected_payload):
        raise PreflightFailure("D0-READBACK", f"{step_id} observed payload drifted")
    if step_id in {"startup_zero", "main_zero", "final_zero"} and any(observed_payload.values()):
        raise PreflightFailure("D0-READBACK", f"{step_id} did not verify all-zero output")
    return identity, generation


def _validate_shutdown_steps(steps: Sequence[Mapping[str, Any]]) -> None:
    if len(steps) != 2 or [step.get("name") for step in steps] != ["esphome", "ray120c"]:
        raise PreflightFailure("D0-CLEANUP-UNKNOWN", "all-off did not report both frozen shutdown steps")
    if any(step.get("ok") is not True for step in steps):
        raise PreflightFailure("D0-CLEANUP-UNKNOWN", "one or more all-off steps failed")
    ray_detail = steps[1].get("detail")
    response = ray_detail.get("response") if isinstance(ray_detail, Mapping) else None
    data = response.get("data") if isinstance(response, Mapping) else None
    try:
        intensity = int(data.get("intensity")) if isinstance(data, Mapping) else None
    except (TypeError, ValueError):
        intensity = None
    if intensity != 0:
        raise PreflightFailure("D0-CLEANUP-UNKNOWN", "Ray all-off response did not verify intensity 0")


def _serialize_shutdown_steps(steps: Sequence[Any]) -> list[dict[str, Any]]:
    result = []
    for step in steps:
        if hasattr(step, "to_jsonable"):
            result.append(dict(step.to_jsonable()))
        elif isinstance(step, Mapping):
            result.append(dict(step))
        else:
            raise TypeError("all-off returned an unsupported shutdown step")
    return result


def _classify_device_exception(exc: BaseException) -> PreflightFailure:
    message = str(exc)
    lowered = message.lower()
    if "missing or duplicated" in lowered or "services are incomplete" in lowered:
        return PreflightFailure("D0-FIRMWARE-MISSING", f"{type(exc).__name__}: {message}")
    if "timed out" in lowered or "timeout" in lowered:
        return PreflightFailure("D0-DEVICE/IDENTITY", f"{type(exc).__name__}: {message}")
    return PreflightFailure("D0-DEVICE/IDENTITY", f"{type(exc).__name__}: {message}")


def _as_preflight_failure(exc: BaseException) -> PreflightFailure:
    if isinstance(exc, PreflightFailure):
        return exc
    return PreflightFailure("D0-CODE", f"{type(exc).__name__}: {exc}")


def _failure_record(exc: PreflightFailure) -> dict[str, str]:
    return {"branch": exc.branch, "type": type(exc).__name__, "message": str(exc)}


def _payload_for(arguments: Mapping[str, int]) -> dict[str, int]:
    return {
        "red": int(arguments["r"]),
        "green": int(arguments["g"]),
        "blue": int(arguments["b"]),
        "warm_white": int(arguments["ww"]),
        "cold_white": int(arguments["cw"]),
    }


def _prepare_run_dir(output_dir: Path, run_name: str) -> Path:
    if not run_name or Path(run_name).name != run_name or run_name in {".", ".."}:
        raise ValueError("run name must be one non-empty path component")
    run_dir = Path(output_dir) / run_name
    if run_dir.exists() and any(run_dir.iterdir()):
        raise FileExistsError(f"run directory is not empty: {run_dir}")
    run_dir.mkdir(parents=True, exist_ok=True)
    return run_dir


def _write_json_atomic(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp-{os.getpid()}")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8")
    os.replace(temporary, path)


def _append_jsonl(path: Path, value: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(value, sort_keys=True, allow_nan=False) + "\n")
        handle.flush()
        os.fsync(handle.fileno())


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Verify generation-bearing RGBWW device-state readback at bounded raw PWM.")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--dry-run", action="store_true")
    mode.add_argument("--execute", action="store_true")
    parser.add_argument("--allow-device-control", action="store_true")
    parser.add_argument("--named-experiment")
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--run-name", required=True)
    args = parser.parse_args(argv)
    if args.execute:
        if not args.allow_device_control:
            parser.error("--execute requires --allow-device-control")
        if args.named_experiment != EXPERIMENT_ID:
            parser.error(f"--execute requires --named-experiment {EXPERIMENT_ID}")
    return args


def _install_interrupt_handlers() -> dict[int, Any]:
    previous: dict[int, Any] = {}

    def interrupt(signum: int, _frame: Any) -> None:
        raise InterruptedError(f"received {signal.Signals(signum).name}")

    for signum in (signal.SIGINT, signal.SIGTERM, signal.SIGHUP):
        previous[signum] = signal.getsignal(signum)
        signal.signal(signum, interrupt)
    return previous


def _restore_interrupt_handlers(previous: Mapping[int, Any]) -> None:
    for signum, handler in previous.items():
        signal.signal(signum, handler)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        if args.dry_run:
            run_dir = write_dry_run(output_dir=args.output_dir, run_name=args.run_name)
        else:
            previous = _install_interrupt_handlers()
            try:
                run_dir = execute_preflight(output_dir=args.output_dir, run_name=args.run_name)
            finally:
                _restore_interrupt_handlers(previous)
    except Exception as exc:
        print(f"strip_state_readback_preflight: {exc}", file=sys.stderr)
        return 1
    print(run_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
