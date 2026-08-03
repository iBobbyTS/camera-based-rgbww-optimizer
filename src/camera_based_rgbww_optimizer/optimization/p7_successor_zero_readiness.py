"""Guide 4 bounded zero/readiness composition.

This module owns only chronology, validation composition, and durable evidence.
Device protocols, zero semantics, camera transport, shutdown, and canonical JSON
I/O remain owned by their existing repository modules.
"""

from __future__ import annotations

import argparse
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType
from typing import Any

from camera_based_rgbww_optimizer.control import all_off, camera_remote, esphome, ray120c
from camera_based_rgbww_optimizer.optimization import hsi_source_evidence
from camera_based_rgbww_optimizer.paths import PROJECT_ROOT
from camera_based_rgbww_optimizer.utils import p7_retained_r3_provenance_io as provenance


__all__ = [
    "AppLifecycleObservation",
    "ZeroReadinessError",
    "classify_app_lifecycle_observation",
    "execute_zero_readiness",
    "finalize_zero_readiness",
    "main",
]


SCHEMA = "g4_successor_zero_readiness_v1"
EXPECTED_ROOT_PARENT = Path("/Volumes/4T/temp/rgbww-optimizer")
EXPECTED_STRIP_NAME = "bedroom-rgbww-strip"
EXPECTED_STRIP_HOST = "bedroom-rgbww-strip.local"
EXPECTED_STRIP_PORT = 6053
EXPECTED_CAMERA_BASE_URL = "http://ibobby-rpi-4.local:8088"
EXPECTED_CAMERA_MODEL = "Canon EOS R6 Mark III via r6-camera-bridge"
EXPECTED_CAMERA_CAPABILITY = "remote_v2_capture_timing_v1"
EXPECTED_RAY_URL = "ws://127.0.0.1:33782"
EXPECTED_RAY_NODE = "40165-560387"
EXPECTED_RAY_CLIENT = 1
RAY_CCT = 5600
RAY_GM = 100
RAY_INTENSITY = 0
RAY_TIMEOUT = 3.0
CAMERA_TIMEOUT = 10.0
STRIP_TIMEOUT = 5.0
CURVE_PATH = PROJECT_ROOT / "config/channel/code-duty-curve.json"
ZERO_COMMAND = {"cw": 0, "ww": 0, "r": 0, "g": 0, "b": 0}
ZERO_PAYLOAD = {
    "red": 0,
    "green": 0,
    "blue": 0,
    "warm_white": 0,
    "cold_white": 0,
}
INITIAL_ARTIFACTS = (
    "frozen-inputs.json",
    "strip-readiness.json",
    "ray-readiness.json",
    "camera-readiness.json",
    "source-isolation.json",
    "python-finally-zero.json",
)
FINALIZE_ARTIFACTS = (
    "all-off-shell.json",
    "all-off-shell.stderr.log",
    "all-off-shell.exit-status.txt",
    "independent-final-zero.json",
    "runner.log",
    "wrapper.log",
    "wrapper-result.json",
)
TERMINAL_NAME = "terminal-seal.json"
FINAL_INVENTORY = tuple(sorted((*INITIAL_ARTIFACTS, *FINALIZE_ARTIFACTS, TERMINAL_NAME)))
FORBIDDEN_EVIDENCE_WORDS = ("secret", "token", "api_key", "encryption_key")
APP_LIFECYCLE_OBSERVATION_SCHEMA = "g4_app_lifecycle_observation_v1"
APP_LIFECYCLE_CLASSIFICATION_SCHEMA = "g4_app_lifecycle_classification_v1"
EXPECTED_APP_BUNDLE = "/Applications/amaran Desktop.app"
EXPECTED_APP_BUNDLE_ID = "com.sidus.amaran-desktop"
EXPECTED_APP_EXECUTABLE = "/Applications/amaran Desktop.app/Contents/MacOS/amaran Desktop"
APP_LIFECYCLE_POLL_SECONDS = (0, 1, 2, 4, 8, 15)


class ZeroReadinessError(RuntimeError):
    def __init__(self, code: str) -> None:
        self.code = code
        super().__init__(code)


@dataclass(frozen=True)
class AppLifecycleObservation:
    """One immutable, caller-supplied observation with no live inspection."""

    schema: str
    app_bundle: str
    app_bundle_id: str
    app_executable: str
    owned_pid: int
    app_preexisting: bool
    graceful_request_count: int
    request_transport_exit: int
    request_error_code: int | None
    force_request_count: int
    alternate_request_count: int
    poll_elapsed_seconds: tuple[int, ...]
    owned_pid_present: tuple[bool, ...]
    final_app_residual_count: int
    final_listener_residual_count: int
    final_owned_residual_count: int
    final_scratch_residual_count: int
    service_variant_count: int
    endpoint_variant_count: int

    def to_jsonable(self) -> dict[str, Any]:
        return {
            "schema": self.schema,
            "app_bundle": self.app_bundle,
            "app_bundle_id": self.app_bundle_id,
            "app_executable": self.app_executable,
            "owned_pid": self.owned_pid,
            "app_preexisting": self.app_preexisting,
            "graceful_request_count": self.graceful_request_count,
            "request_transport_exit": self.request_transport_exit,
            "request_error_code": self.request_error_code,
            "force_request_count": self.force_request_count,
            "alternate_request_count": self.alternate_request_count,
            "poll_elapsed_seconds": list(self.poll_elapsed_seconds),
            "owned_pid_present": list(self.owned_pid_present),
            "final_app_residual_count": self.final_app_residual_count,
            "final_listener_residual_count": self.final_listener_residual_count,
            "final_owned_residual_count": self.final_owned_residual_count,
            "final_scratch_residual_count": self.final_scratch_residual_count,
            "service_variant_count": self.service_variant_count,
            "endpoint_variant_count": self.endpoint_variant_count,
        }


def _validate_app_lifecycle_observation(value: AppLifecycleObservation) -> None:
    _require(type(value) is AppLifecycleObservation, "app_lifecycle_observation_type_invalid")
    string_fields = (value.schema, value.app_bundle, value.app_bundle_id, value.app_executable)
    integer_fields = (
        value.owned_pid,
        value.graceful_request_count,
        value.request_transport_exit,
        value.force_request_count,
        value.alternate_request_count,
        value.final_app_residual_count,
        value.final_listener_residual_count,
        value.final_owned_residual_count,
        value.final_scratch_residual_count,
        value.service_variant_count,
        value.endpoint_variant_count,
    )
    _require(all(type(item) is str for item in string_fields), "app_lifecycle_observation_string_invalid")
    _require(all(type(item) is int for item in integer_fields), "app_lifecycle_observation_integer_invalid")
    _require(type(value.app_preexisting) is bool, "app_lifecycle_observation_boolean_invalid")
    _require(
        value.request_error_code is None or type(value.request_error_code) is int,
        "app_lifecycle_observation_error_invalid",
    )
    _require(
        type(value.poll_elapsed_seconds) is tuple
        and all(type(item) is int for item in value.poll_elapsed_seconds),
        "app_lifecycle_observation_poll_schedule_invalid",
    )
    _require(
        type(value.owned_pid_present) is tuple
        and all(type(item) is bool for item in value.owned_pid_present),
        "app_lifecycle_observation_presence_invalid",
    )


def classify_app_lifecycle_observation(
    observation: AppLifecycleObservation,
) -> Mapping[str, Any]:
    """Classify frozen facts without inspecting an app, process, or listener."""

    _validate_app_lifecycle_observation(observation)
    presence = observation.owned_pid_present
    post_zero = presence[1:]
    disappearance_index = next((index for index, present in enumerate(post_zero) if not present), None)
    disappeared = disappearance_index is not None
    remained_absent = disappeared and not any(post_zero[disappearance_index:])
    transport_consistent = (
        (observation.request_transport_exit == 0 and observation.request_error_code is None)
        or (observation.request_transport_exit != 0 and type(observation.request_error_code) is int)
    )
    guards = {
        "schema_exact": observation.schema == APP_LIFECYCLE_OBSERVATION_SCHEMA,
        "app_bundle_exact": observation.app_bundle == EXPECTED_APP_BUNDLE,
        "app_bundle_id_exact": observation.app_bundle_id == EXPECTED_APP_BUNDLE_ID,
        "app_executable_exact": observation.app_executable == EXPECTED_APP_EXECUTABLE,
        "owned_pid_positive": observation.owned_pid > 0,
        "non_preexisting": observation.app_preexisting is False,
        "graceful_request_exactly_once": observation.graceful_request_count == 1,
        "transport_exit_error_consistent": transport_consistent,
        "force_request_zero": observation.force_request_count == 0,
        "alternate_request_zero": observation.alternate_request_count == 0,
        "service_variant_zero": observation.service_variant_count == 0,
        "endpoint_variant_zero": observation.endpoint_variant_count == 0,
        "poll_schedule_exact": observation.poll_elapsed_seconds == APP_LIFECYCLE_POLL_SECONDS,
        "poll_presence_count_exact": len(presence) == len(APP_LIFECYCLE_POLL_SECONDS),
        "owned_present_at_zero": len(presence) > 0 and presence[0] is True,
        "disappeared_within_bounded_grace": disappeared,
        "remained_absent_after_disappearance": remained_absent,
        "final_app_residual_zero": observation.final_app_residual_count == 0,
        "final_listener_residual_zero": observation.final_listener_residual_count == 0,
        "final_owned_residual_zero": observation.final_owned_residual_count == 0,
        "final_scratch_residual_zero": observation.final_scratch_residual_count == 0,
    }
    transport_success = observation.request_transport_exit == 0 and observation.request_error_code is None
    all_clean = all(guards.values())
    if observation.app_preexisting:
        classification = "NON_OWNED_NOT_APPLICABLE"
        final_effect_status = "not_applicable"
    elif all_clean and transport_success:
        classification = "REQUEST_CONFIRMED_EFFECT_CONFIRMED_CLEAN"
        final_effect_status = "confirmed_clean"
    elif all_clean:
        classification = "REQUEST_TRANSPORT_AMBIGUOUS_EFFECT_CONFIRMED_CLEAN"
        final_effect_status = "confirmed_clean"
    else:
        classification = "APP_LIFECYCLE_FAIL_CLOSED"
        final_effect_status = "not_confirmed"
    request_transport_status = "success" if transport_success else "ambiguous_failure"
    if not transport_consistent:
        request_transport_status = "invalid"
    return MappingProxyType({
        "schema": APP_LIFECYCLE_CLASSIFICATION_SCHEMA,
        "classification": classification,
        "request_transport_status": request_transport_status,
        "request_transport_success": transport_success,
        "final_effect_status": final_effect_status,
        "request_transport_exit": observation.request_transport_exit,
        "request_error_code": observation.request_error_code,
        "guards": MappingProxyType(guards),
    })


@dataclass(frozen=True)
class _RuntimeDependencies:
    strip_zero: Callable[..., Mapping[str, Any]] = esphome.verified_light
    ray_set_zero: Callable[..., Mapping[str, Any]] = ray120c.set_cct
    ray_get_cct: Callable[..., Mapping[str, Any]] = ray120c.get_cct
    ray_get_node: Callable[..., Mapping[str, Any]] = ray120c.get_node_config
    camera_probe: Callable[[], Mapping[str, Any]] | None = None
    validate_both_off: Callable[..., None] = hsi_source_evidence.validate_both_off


def _require(condition: bool, code: str) -> None:
    if not condition:
        raise ZeroReadinessError(code)


def _failure(phase: str, error: BaseException) -> dict[str, str]:
    code = getattr(error, "code", None)
    return {
        "phase": phase,
        "code": code if type(code) is str and code else type(error).__name__,
    }


def _ensure_secret_absence(value: Any) -> None:
    if isinstance(value, Mapping):
        for key, child in value.items():
            lowered = str(key).lower()
            _require(not any(word in lowered for word in FORBIDDEN_EVIDENCE_WORDS), "secret_key_in_evidence")
            _ensure_secret_absence(child)
    elif isinstance(value, (list, tuple)):
        for child in value:
            _ensure_secret_absence(child)


def _persist(
    root: provenance.DirectoryIdentity,
    name: str,
    value: Any,
) -> provenance.FileIdentity:
    _ensure_secret_absence(value)
    return provenance.persist_canonical_json(root, name, value)


def _curve() -> Mapping[str, Any]:
    identity = provenance.read_exact_file(CURVE_PATH)
    value = provenance.decode_strict_json_bytes(identity.data)
    _require(isinstance(value, Mapping), "curve_not_object")
    return value


def _ray_settings() -> ray120c.OpenAPISettings:
    settings = ray120c.OpenAPISettings.from_env()
    _require(
        settings.url == EXPECTED_RAY_URL
        and settings.node_id == EXPECTED_RAY_NODE
        and settings.client_id == EXPECTED_RAY_CLIENT,
        "ray_runtime_identity_drift",
    )
    return ray120c.OpenAPISettings(
        secret=settings.secret,
        url=EXPECTED_RAY_URL,
        node_id=EXPECTED_RAY_NODE,
        client_id=EXPECTED_RAY_CLIENT,
        timeout=RAY_TIMEOUT,
    )


def _strip_zero_call(deps: _RuntimeDependencies) -> Mapping[str, Any]:
    return deps.strip_zero(
        0,
        0,
        0,
        0,
        0,
        host=EXPECTED_STRIP_HOST,
        port=EXPECTED_STRIP_PORT,
        expected_name=EXPECTED_STRIP_NAME,
        curve_path=CURVE_PATH,
        state_timeout=STRIP_TIMEOUT,
    )


def _ray_set_call(deps: _RuntimeDependencies, settings: ray120c.OpenAPISettings) -> Mapping[str, Any]:
    return deps.ray_set_zero(RAY_CCT, intensity=RAY_INTENSITY, gm=RAY_GM, settings=settings)


def _validate_ray_zero(value: Mapping[str, Any], code: str) -> dict[str, int]:
    hsi_source_evidence.validate_ray_off(value)
    data = value.get("data")
    _require(isinstance(data, Mapping), code)
    actual = {name: int(data.get(name, -1)) for name in ("cct", "gm", "intensity")}
    _require(actual == {"cct": RAY_CCT, "gm": RAY_GM, "intensity": RAY_INTENSITY}, code)
    return actual


def _validate_strip_zero(
    evidence: Mapping[str, Any],
    curve: Mapping[str, Any],
    *,
    previous_generation: int | None,
    stable_identity: Mapping[str, str] | None,
) -> tuple[dict[str, str], int]:
    snapshot = hsi_source_evidence.validate_strip_device_evidence(evidence, ZERO_COMMAND, curve)
    identity_raw = evidence.get("device_identity")
    _require(isinstance(identity_raw, Mapping), "strip_identity_missing")
    identity = {
        "name": str(identity_raw.get("name", "")),
        "mac_address": str(identity_raw.get("mac_address", "")),
    }
    _require(identity["name"] == EXPECTED_STRIP_NAME and bool(identity["mac_address"]), "strip_identity_drift")
    _require(stable_identity is None or dict(stable_identity) == identity, "strip_identity_drift")
    generation = int(snapshot["generation"])
    _require(previous_generation is None or generation > previous_generation, "strip_generation_not_global")
    _require({key: int(snapshot[key]) for key in ZERO_PAYLOAD} == ZERO_PAYLOAD, "strip_not_zero")
    return identity, generation


def _default_camera_probe() -> Mapping[str, Any]:
    health = camera_remote.read_remote_health(
        base_url=EXPECTED_CAMERA_BASE_URL,
        timeout=CAMERA_TIMEOUT,
    )
    _require(health.get("status") == "ok", "camera_health_not_ok")
    config = camera_remote.load_remote_camera_config(base_url=EXPECTED_CAMERA_BASE_URL)
    backend = camera_remote.RemoteCameraBackend(
        config=config,
        timeout=CAMERA_TIMEOUT,
        busy_retries=0,
    )
    connection = backend.connect()
    settings = backend._load_settings()
    _require(
        connection.model == EXPECTED_CAMERA_MODEL
        and connection.port == EXPECTED_CAMERA_BASE_URL
        and backend.backend_name == "remote"
        and backend.v2_capture_capability == EXPECTED_CAMERA_CAPABILITY
        and callable(getattr(backend, "capture_with_timing", None)),
        "camera_identity_or_capability_drift",
    )
    return {
        "health_status": "ok",
        "health_keys": sorted(str(key) for key in health),
        "backend": backend.backend_name,
        "model": connection.model,
        "base_url": connection.port,
        "capability": backend.v2_capture_capability,
        "capture_with_timing_callable": True,
        "config": {
            "iso_current": settings.iso.current,
            "iso_choice_count": len(settings.iso.choices),
            "aperture_current": settings.aperture.current,
            "aperture_choice_count": len(settings.aperture.choices),
            "shutter_current": settings.shutter_speed.current,
            "shutter_choice_count": len(settings.shutter_speed.choices),
            "image_format": settings.image_format,
        },
    }


def _frozen_inputs(output_root: str) -> dict[str, Any]:
    return {
        "schema": SCHEMA,
        "status": "frozen",
        "sequence": 1,
        "root": {"path": output_root, "mode": 0o700, "fresh": True},
        "strip": {
            "host": EXPECTED_STRIP_HOST,
            "port": EXPECTED_STRIP_PORT,
            "expected_name": EXPECTED_STRIP_NAME,
            "state_entity": esphome.STATE_OBJECT_ID,
            "state_timeout_s": STRIP_TIMEOUT,
            "command": dict(ZERO_COMMAND),
            "nonzero_calls": 0,
        },
        "ray": {
            "url": EXPECTED_RAY_URL,
            "node": EXPECTED_RAY_NODE,
            "client": EXPECTED_RAY_CLIENT,
            "timeout_s": RAY_TIMEOUT,
            "command": {"cct": RAY_CCT, "gm": RAY_GM, "intensity": RAY_INTENSITY},
            "nonzero_calls": 0,
        },
        "camera": {
            "base_url": EXPECTED_CAMERA_BASE_URL,
            "model": EXPECTED_CAMERA_MODEL,
            "capability": EXPECTED_CAMERA_CAPABILITY,
            "timeout_s": CAMERA_TIMEOUT,
            "busy_retry": 0,
            "capture_calls": 0,
            "config_write_calls": 0,
        },
        "authority": {
            "release_consumption": 0,
            "formal_r6": 0,
            "td_c": 0,
            "firmware": 0,
            "deployment": 0,
        },
    }


def execute_zero_readiness(
    output_root: str | Path,
    *,
    dependencies: _RuntimeDependencies | None = None,
) -> provenance.DirectoryIdentity:
    deps = dependencies or _RuntimeDependencies()
    root_path = Path(output_root)
    _require(root_path.is_absolute() and root_path.parent == EXPECTED_ROOT_PARENT, "root_scope_invalid")
    root = provenance.create_exclusive_root(str(root_path))
    _persist(root, INITIAL_ARTIFACTS[0], _frozen_inputs(root.path))

    curve = _curve()
    ray_settings = _ray_settings()
    ledger = {
        "strip_verified_zero": 0,
        "ray_set_zero": 0,
        "ray_get_cct": 0,
        "ray_get_node_config": 0,
        "camera_health_get": 0,
        "camera_config_get": 0,
        "camera_capture": 0,
        "camera_config_write": 0,
        "source_isolation_validation": 0,
        "strip_nonzero": 0,
        "ray_nonzero": 0,
        "release_consumption": 0,
        "formal_r6": 0,
        "td_c": 0,
    }
    records: dict[str, dict[str, Any]] = {
        "strip": {"schema": SCHEMA, "status": "skipped", "sequence": 2},
        "ray": {"schema": SCHEMA, "status": "skipped", "sequence": 3},
        "camera": {"schema": SCHEMA, "status": "skipped", "sequence": 4},
        "isolation": {"schema": SCHEMA, "status": "skipped", "sequence": 5},
    }
    primary: dict[str, str] | None = None
    stable_identity: dict[str, str] | None = None
    previous_generation: int | None = None
    main_strip: Mapping[str, Any] | None = None
    main_ray_readback: Mapping[str, Any] | None = None
    try:
        try:
            ledger["strip_verified_zero"] += 1
            main_strip = _strip_zero_call(deps)
            stable_identity, previous_generation = _validate_strip_zero(
                main_strip,
                curve,
                previous_generation=previous_generation,
                stable_identity=stable_identity,
            )
            records["strip"] = {
                "schema": SCHEMA,
                "status": "pass",
                "sequence": 2,
                "device_identity": stable_identity,
                "generation": previous_generation,
                "evidence": dict(main_strip),
            }

            ledger["ray_set_zero"] += 1
            ray_set = _ray_set_call(deps, ray_settings)
            _validate_ray_zero(ray_set, "ray_set_not_zero")
            ledger["ray_get_cct"] += 1
            main_ray_readback = deps.ray_get_cct(settings=ray_settings)
            ray_state = _validate_ray_zero(main_ray_readback, "ray_readback_not_zero")
            ledger["ray_get_node_config"] += 1
            node = deps.ray_get_node(settings=ray_settings)
            _require(node.get("code") in (None, 0) and isinstance(node.get("data"), Mapping), "ray_node_config_invalid")
            records["ray"] = {
                "schema": SCHEMA,
                "status": "pass",
                "sequence": 3,
                "request_identity": {
                    "url": ray_settings.url,
                    "node": ray_settings.node_id,
                    "client": ray_settings.client_id,
                },
                "state": ray_state,
                "node_config": {
                    "code": node.get("code"),
                    "data_keys": sorted(str(key) for key in node["data"]),
                },
            }

            probe = deps.camera_probe or _default_camera_probe
            ledger["camera_health_get"] += 1
            ledger["camera_config_get"] += 1
            camera = dict(probe())
            _require(
                camera.get("health_status") == "ok"
                and camera.get("model") == EXPECTED_CAMERA_MODEL
                and camera.get("base_url") == EXPECTED_CAMERA_BASE_URL
                and camera.get("capability") == EXPECTED_CAMERA_CAPABILITY
                and camera.get("capture_with_timing_callable") is True,
                "camera_probe_invalid",
            )
            records["camera"] = {
                "schema": SCHEMA,
                "status": "pass",
                "sequence": 4,
                **camera,
                "capture_calls": 0,
                "config_write_calls": 0,
                "busy_retry": 0,
            }

            ledger["source_isolation_validation"] += 1
            deps.validate_both_off(main_strip, main_ray_readback, curve)
            records["isolation"] = {
                "schema": SCHEMA,
                "status": "pass",
                "sequence": 5,
                "validation": "repo_owned_validate_both_off",
                "strip_generation": previous_generation,
                "ray_intensity": 0,
            }
        except BaseException as error:
            primary = _failure("main_readiness", error)
            for record in records.values():
                if record["status"] == "skipped":
                    record["failure"] = dict(primary)

        for name, key in zip(INITIAL_ARTIFACTS[1:5], ("strip", "ray", "camera", "isolation"), strict=True):
            _persist(root, name, records[key])
    finally:
        cleanup_failures: list[dict[str, str]] = []
        cleanup_strip: dict[str, Any] | None = None
        cleanup_ray: dict[str, Any] | None = None
        try:
            ledger["strip_verified_zero"] += 1
            value = _strip_zero_call(deps)
            stable_identity, previous_generation = _validate_strip_zero(
                value,
                curve,
                previous_generation=previous_generation,
                stable_identity=stable_identity,
            )
            cleanup_strip = {
                "status": "pass",
                "generation": previous_generation,
                "device_identity": stable_identity,
                "evidence": dict(value),
            }
        except BaseException as error:
            cleanup_failures.append(_failure("python_finally_strip_zero", error))
            cleanup_strip = {"status": "fail", "failure": cleanup_failures[-1]}
        try:
            ledger["ray_set_zero"] += 1
            value = _ray_set_call(deps, ray_settings)
            cleanup_ray = {"status": "pass", "state": _validate_ray_zero(value, "python_finally_ray_not_zero")}
        except BaseException as error:
            cleanup_failures.append(_failure("python_finally_ray_zero", error))
            cleanup_ray = {"status": "fail", "failure": cleanup_failures[-1]}
        _persist(
            root,
            INITIAL_ARTIFACTS[5],
            {
                "schema": SCHEMA,
                "status": "pass" if not cleanup_failures else "fail",
                "sequence": 6,
                "strip": cleanup_strip,
                "ray": cleanup_ray,
                "failures": cleanup_failures,
                "primary": primary,
                "call_ledger": ledger,
            },
        )

    if primary is not None:
        raise ZeroReadinessError("main_readiness_failed")
    if cleanup_failures:
        raise ZeroReadinessError("python_finally_zero_failed")
    return root


def _read_scratch(path: str | Path, *, root: provenance.DirectoryIdentity) -> bytes:
    target = Path(path)
    root_path = Path(root.path)
    _require(
        target.is_absolute()
        and target.parent == root_path.parent
        and target.name.startswith(f".{root_path.name}.")
        and target.name.endswith(".scratch"),
        "scratch_scope_invalid",
    )
    identity = provenance.read_exact_file(target, expected_mode=0o600)
    _require(identity.byte_count <= 1024 * 1024, "scratch_too_large")
    return identity.data


def _artifact_reference(identity: provenance.FileIdentity) -> dict[str, Any]:
    return {
        "path": Path(identity.path).name,
        "device": identity.device,
        "inode": identity.inode,
        "mode": identity.mode,
        "bytes": identity.byte_count,
        "sha256": identity.sha256,
    }


def _read_initial(
    root: provenance.DirectoryIdentity,
) -> tuple[list[provenance.FileIdentity], Mapping[str, Any]]:
    _require(tuple(provenance.list_exact_regular_children(root)) == tuple(sorted(INITIAL_ARTIFACTS)), "initial_inventory_drift")
    identities = [
        provenance.read_exact_file(Path(root.path) / name, expected_mode=0o600, root=root)
        for name in INITIAL_ARTIFACTS
    ]
    python_value = provenance.decode_canonical_json(identities[-1].data)
    _require(isinstance(python_value, Mapping), "python_finally_not_object")
    return identities, python_value


def _validate_shell_cleanup(value: Any, exit_status: int) -> dict[str, Any]:
    _require(isinstance(value, list) and len(value) == 2, "shell_cleanup_schema_invalid")
    rows = [dict(item) for item in value if isinstance(item, Mapping)]
    _require(len(rows) == 2 and [item.get("name") for item in rows] == ["esphome", "ray120c"], "shell_cleanup_schema_invalid")
    if exit_status == 0:
        _require(all(item.get("ok") is True for item in rows), "shell_cleanup_false_success")
        strip_detail = rows[0].get("detail")
        ray_detail = rows[1].get("detail")
        _require(isinstance(strip_detail, Mapping) and strip_detail.get("payload") == ZERO_PAYLOAD, "shell_strip_not_zero")
        _require(isinstance(ray_detail, Mapping), "shell_ray_not_zero")
        _validate_ray_zero(ray_detail.get("response", {}), "shell_ray_not_zero")
    return {"schema": SCHEMA, "status": "pass" if exit_status == 0 else "fail", "steps": rows}


def finalize_zero_readiness(
    output_root: str | Path,
    *,
    runner_log_source: str | Path,
    wrapper_log_source: str | Path,
    shell_json_source: str | Path,
    shell_stderr_source: str | Path,
    child_exit_status: int,
    shell_exit_status: int,
    wrapper_status: str,
    wrapper_exit_status: int,
    signal_name: str | None,
    dependencies: _RuntimeDependencies | None = None,
) -> int:
    deps = dependencies or _RuntimeDependencies()
    root = provenance.read_existing_root(str(Path(output_root)))
    initial, python_value = _read_initial(root)
    runner_bytes = _read_scratch(runner_log_source, root=root)
    wrapper_bytes = _read_scratch(wrapper_log_source, root=root)
    shell_bytes = _read_scratch(shell_json_source, root=root)
    shell_stderr = _read_scratch(shell_stderr_source, root=root)
    try:
        shell_value = provenance.json_native_value(
            provenance.decode_strict_json_bytes(shell_bytes)
        )
    except provenance.ProvenanceIOError as error:
        raise ZeroReadinessError("shell_cleanup_json_invalid") from error
    shell_record = _validate_shell_cleanup(shell_value, int(shell_exit_status))
    added: list[provenance.FileIdentity] = []
    added.append(_persist(root, FINALIZE_ARTIFACTS[0], shell_record))
    added.append(_persist(root, FINALIZE_ARTIFACTS[1], {"schema": SCHEMA, "text": shell_stderr.decode("utf-8", errors="replace")}))
    added.append(_persist(root, FINALIZE_ARTIFACTS[2], int(shell_exit_status)))

    ledger = dict(python_value.get("call_ledger", {}))
    ledger["strip_shell_zero"] = 1
    ledger["ray_set_zero"] = int(ledger.get("ray_set_zero", 0)) + 1
    stable_identity = None
    previous_generation = None
    strip_value = python_value.get("strip")
    if isinstance(strip_value, Mapping) and strip_value.get("status") == "pass":
        stable_identity = strip_value.get("device_identity")
        previous_generation = int(strip_value["generation"])
    curve = _curve()
    ray_settings = _ray_settings()
    independent_failures: list[dict[str, str]] = []
    independent_strip: dict[str, Any] | None = None
    independent_ray: dict[str, Any] | None = None
    try:
        ledger["strip_verified_zero"] = int(ledger.get("strip_verified_zero", 0)) + 1
        value = _strip_zero_call(deps)
        identity, generation = _validate_strip_zero(
            value,
            curve,
            previous_generation=previous_generation,
            stable_identity=stable_identity if isinstance(stable_identity, Mapping) else None,
        )
        independent_strip = {"status": "pass", "generation": generation, "device_identity": identity, "evidence": dict(value)}
    except BaseException as error:
        independent_failures.append(_failure("independent_strip_zero", error))
        independent_strip = {"status": "fail", "failure": independent_failures[-1]}
    try:
        ledger["ray_set_zero"] = int(ledger.get("ray_set_zero", 0)) + 1
        set_value = _ray_set_call(deps, ray_settings)
        _validate_ray_zero(set_value, "independent_ray_set_not_zero")
        ledger["ray_get_cct"] = int(ledger.get("ray_get_cct", 0)) + 1
        readback = deps.ray_get_cct(settings=ray_settings)
        independent_ray = {"status": "pass", "state": _validate_ray_zero(readback, "independent_ray_readback_not_zero")}
        if independent_strip is not None and independent_strip.get("status") == "pass":
            ledger["source_isolation_validation"] = int(ledger.get("source_isolation_validation", 0)) + 1
            deps.validate_both_off(independent_strip["evidence"], readback, curve)
    except BaseException as error:
        independent_failures.append(_failure("independent_ray_or_isolation", error))
        independent_ray = {"status": "fail", "failure": independent_failures[-1]}
    independent = {
        "schema": SCHEMA,
        "status": "pass" if not independent_failures else "fail",
        "sequence": 10,
        "strip": independent_strip,
        "ray": independent_ray,
        "failures": independent_failures,
        "call_ledger": ledger,
    }
    added.append(_persist(root, FINALIZE_ARTIFACTS[3], independent))
    added.append(_persist(root, FINALIZE_ARTIFACTS[4], {"schema": SCHEMA, "text": runner_bytes.decode("utf-8", errors="replace")}))
    added.append(_persist(root, FINALIZE_ARTIFACTS[5], {"schema": SCHEMA, "text": wrapper_bytes.decode("utf-8", errors="replace")}))

    effective_exit = int(wrapper_exit_status)
    effective_status = wrapper_status
    if independent_failures and effective_exit == 0:
        effective_exit = 71
        effective_status = "independent_final_zero_failed"
    wrapper_result = {
        "schema": SCHEMA,
        "status": effective_status,
        "child_exit_status": int(child_exit_status),
        "shell_cleanup_exit_status": int(shell_exit_status),
        "wrapper_exit_status": effective_exit,
        "signal": signal_name,
        "call_ledger": ledger,
        "capture_calls": 0,
        "nonzero_calls": 0,
        "config_write_calls": 0,
        "release_consumption": 0,
        "formal_r6": 0,
        "td_c": 0,
    }
    added.append(_persist(root, FINALIZE_ARTIFACTS[6], wrapper_result))
    preterminal = [*initial, *added]
    expected_preterminal = tuple(sorted((*INITIAL_ARTIFACTS, *FINALIZE_ARTIFACTS)))
    _require(tuple(provenance.list_exact_regular_children(root)) == expected_preterminal, "preterminal_inventory_drift")
    pass_status = (
        effective_exit == 0
        and int(child_exit_status) == 0
        and int(shell_exit_status) == 0
        and python_value.get("status") == "pass"
        and not independent_failures
    )
    terminal = {
        "schema": SCHEMA,
        "status": "sealed_pass_waiting_planner_review" if pass_status else "sealed_fail_waiting_planner_review",
        "root": {"path": root.path, "device": root.device, "inode": root.inode, "mode": root.mode},
        "artifacts": [_artifact_reference(identity) for identity in preterminal],
        "artifact_count_before_terminal": len(preterminal),
        "terminal_self_reference": False,
        "wrapper_exit_status": effective_exit,
        "retry": 0,
        "alternate_root": 0,
        "release_consumption": 0,
        "capture_calls": 0,
        "nonzero_calls": 0,
        "config_write_calls": 0,
        "formal_r6": 0,
        "td_c": 0,
        "call_ledger": ledger,
    }
    terminal_identity = _persist(root, TERMINAL_NAME, terminal)
    _require(tuple(provenance.list_exact_regular_children(root)) == FINAL_INVENTORY, "terminal_inventory_drift")
    _require(Path(terminal_identity.path).name not in {row["path"] for row in terminal["artifacts"]}, "terminal_self_reference")
    return effective_exit


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Guide 4 bounded zero/readiness owner")
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--execute", action="store_true")
    modes.add_argument("--finalize-only", action="store_true")
    parser.add_argument("--allow-device-control", action="store_true")
    parser.add_argument("--output-root", required=True)
    parser.add_argument("--runner-log-source")
    parser.add_argument("--wrapper-log-source")
    parser.add_argument("--shell-json-source")
    parser.add_argument("--shell-stderr-source")
    parser.add_argument("--child-exit-status", type=int)
    parser.add_argument("--shell-exit-status", type=int)
    parser.add_argument("--wrapper-status")
    parser.add_argument("--wrapper-exit-status", type=int)
    parser.add_argument("--signal-name")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    if not args.allow_device_control:
        raise SystemExit("--allow-device-control is required")
    try:
        if args.execute:
            execute_zero_readiness(args.output_root)
            return 0
        required = (
            args.runner_log_source,
            args.wrapper_log_source,
            args.shell_json_source,
            args.shell_stderr_source,
            args.child_exit_status,
            args.shell_exit_status,
            args.wrapper_status,
            args.wrapper_exit_status,
        )
        if any(value is None for value in required):
            raise ZeroReadinessError("finalize_arguments_missing")
        return finalize_zero_readiness(
            args.output_root,
            runner_log_source=args.runner_log_source,
            wrapper_log_source=args.wrapper_log_source,
            shell_json_source=args.shell_json_source,
            shell_stderr_source=args.shell_stderr_source,
            child_exit_status=args.child_exit_status,
            shell_exit_status=args.shell_exit_status,
            wrapper_status=args.wrapper_status,
            wrapper_exit_status=args.wrapper_exit_status,
            signal_name=args.signal_name,
        )
    except ZeroReadinessError as error:
        print(error.code)
        return 20


if __name__ == "__main__":
    raise SystemExit(main())
