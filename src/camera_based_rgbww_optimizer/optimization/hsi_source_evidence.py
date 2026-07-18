from __future__ import annotations

import json
from collections.abc import Mapping, Sequence
from typing import Any

from camera_based_rgbww_optimizer.control import esphome, ray120c


CHANNELS = ("cw", "ww", "r", "g", "b")


def expected_ray_state(step: Mapping[str, Any]) -> dict[str, int]:
    state = step.get("state") or step.get("ray_state") or step.get("ray")
    if not isinstance(state, Mapping):
        raise ValueError("Ray plan step lacks frozen state")
    intensity = state.get("intensity_percent", state.get("intensity"))
    if intensity is None:
        raise ValueError("Ray plan step lacks frozen intensity")
    return {
        "hue": int(state["hue"]),
        "sat": int(state["sat"]),
        "intensity": ray120c.intensity_percent_to_raw(float(intensity)),
    }


def validate_ray_readback(response: Mapping[str, Any], expected: Mapping[str, Any]) -> None:
    data = response.get("data")
    if not isinstance(data, Mapping):
        raise ValueError("Ray response lacks explicit data readback")
    actual = {name: int(data.get(name, -1)) for name in ("hue", "sat", "intensity")}
    wanted = {name: int(expected[name]) for name in ("hue", "sat", "intensity")}
    if actual != wanted:
        raise ValueError(f"Ray readback differs from frozen plan: {actual} != {wanted}")


def validate_ray_off(response: Mapping[str, Any]) -> None:
    data = response.get("data")
    if not isinstance(data, Mapping) or int(data.get("intensity", -1)) != 0:
        raise ValueError("Ray off response does not explicitly prove intensity zero")


def expected_strip_payloads(
    command: Mapping[str, Any], curve: Mapping[str, Any],
) -> tuple[dict[str, int], dict[str, Any]]:
    raw = {channel: int(command[channel]) for channel in CHANNELS}
    payload = esphome._build_payload(*(raw[channel] for channel in CHANNELS), curve=curve)
    return raw, payload


def validate_strip_device_evidence(
    evidence: Mapping[str, Any], command: Mapping[str, Any], curve: Mapping[str, Any],
) -> Mapping[str, Any]:
    _raw, payload = expected_strip_payloads(command, curve)
    required = {
        "schema_version", "requested_payload", "baseline_snapshot",
        "device_snapshot", "device_state_entity", "device_identity",
    }
    if set(evidence) != required or int(evidence.get("schema_version", -1)) != 1:
        raise ValueError("strip evidence is not an independent device-state schema")
    if evidence.get("requested_payload") != payload:
        raise ValueError("strip requested payload differs from frozen command/curve payload")
    baseline = evidence.get("baseline_snapshot")
    observed = evidence.get("device_snapshot")
    if not isinstance(baseline, Mapping) or not isinstance(observed, Mapping):
        raise ValueError("strip evidence lacks baseline/device snapshots")
    try:
        baseline_snapshot = esphome.RgbwwDeviceSnapshot.parse(json.dumps(dict(baseline), sort_keys=True))
        observed_snapshot = esphome.RgbwwDeviceSnapshot.parse(json.dumps(dict(observed), sort_keys=True))
    except (TypeError, ValueError) as exc:
        raise ValueError("strip evidence contains an invalid device-state snapshot") from exc
    if observed_snapshot.generation <= baseline_snapshot.generation:
        raise ValueError("strip device-state generation did not strictly increase")
    actual = observed_snapshot.payload()
    if actual != payload:
        raise ValueError("strip device snapshot differs from frozen command/curve payload")
    entity = evidence.get("device_state_entity")
    if (
        not isinstance(entity, Mapping)
        or set(entity) != {"object_id", "key"}
        or entity.get("object_id") != esphome.STATE_OBJECT_ID
        or not isinstance(entity.get("key"), int)
    ):
        raise ValueError("strip evidence lacks the frozen device-state entity")
    identity = evidence.get("device_identity")
    if (
        not isinstance(identity, Mapping)
        or set(identity) != {"name", "mac_address"}
        or not str(identity.get("name"))
        or not str(identity.get("mac_address"))
    ):
        raise ValueError("strip evidence lacks device identity")
    return observed_snapshot.to_jsonable()


def validate_both_off(
    strip_evidence: Mapping[str, Any], ray_response: Mapping[str, Any],
    curve: Mapping[str, Any],
) -> None:
    validate_strip_device_evidence(strip_evidence, {channel: 0 for channel in CHANNELS}, curve)
    validate_ray_off(ray_response)


def validate_attempt_event_grammar(
    events: Sequence[Mapping[str, Any]], *, source: str,
    plan_step: Mapping[str, Any], curve: Mapping[str, Any],
    attempt_kind: str = "base",
) -> Mapping[str, Any] | None:
    names = [str(item.get("event")) for item in events]
    on_event = {
        ("ray", "base"): "ray_on_readback_verified",
        ("ray", "weak_signal_reacquire"): "ray_reacquire_on_readback_verified",
        ("strip", "base"): "strip_on_readback_verified",
        ("strip", "weak_signal_reacquire"): "strip_reacquire_on_readback_verified",
    }.get((source, attempt_kind))
    expected_names = ["both_off", "both_off"] if source == "ambient" else ["both_off", on_event, "both_off"]
    if names != expected_names:
        raise ValueError(f"source isolation command evidence grammar mismatch: {names} != {expected_names}")
    validate_both_off(events[0].get("strip_device_evidence", {}), events[0].get("ray_response", {}), curve)
    validate_both_off(events[-1].get("strip_device_evidence", {}), events[-1].get("ray_response", {}), curve)
    if source == "ambient":
        return None
    on = events[1]
    if source == "ray":
        expected = expected_ray_state(plan_step)
        validate_ray_readback(on.get("readback", {}), expected)
        if on.get("expected") != expected:
            raise ValueError("Ray command expected state differs from frozen plan")
    else:
        command = plan_step.get("command")
        if not isinstance(command, Mapping):
            raise ValueError("strip plan step lacks frozen command")
        validate_strip_device_evidence(on.get("device_evidence", {}), command, curve)
        if on.get("requested_command") != {channel: int(command[channel]) for channel in CHANNELS}:
            raise ValueError("strip requested command differs from frozen plan")
    return on


def recompute_physical_count(attempt: Mapping[str, Any]) -> int:
    if not attempt.get("auto_exposure"):
        if int(attempt.get("physical_capture_count", -1)) != 1:
            raise ValueError("fixed capture must consume exactly one physical CR3")
        return 1
    audit = attempt.get("auto_exposure_audit")
    if not isinstance(audit, Mapping):
        raise ValueError("auto-exposure capture lacks detailed audit")
    trials = audit.get("trials")
    rejected = audit.get("rejected_finals")
    if not isinstance(trials, list) or not isinstance(rejected, list) or not isinstance(audit.get("final"), Mapping):
        raise ValueError("auto-exposure audit lacks trials/final/rejected_finals structure")
    recomputed = len(trials) + 1 + len(rejected)
    if int(audit.get("capture_count", -1)) != recomputed:
        raise ValueError("auto-exposure capture_count differs from retained audit structure")
    if int(attempt.get("physical_capture_count", -1)) != recomputed:
        raise ValueError("attempt physical count differs from retained auto-exposure audit")
    return recomputed
