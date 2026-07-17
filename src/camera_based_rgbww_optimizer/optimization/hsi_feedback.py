from __future__ import annotations

from typing import Any, Callable, Mapping, Sequence

import numpy as np

from camera_based_rgbww_optimizer.optimization.hsi_objective import (
    GROUP_ORDER,
    hsi_objective_sort_key,
)
from camera_based_rgbww_optimizer.optimization.multipatch_solver import (
    estimate_group_jacobians,
    solve_lexicographic_local_step,
)


CHANNELS = ("cw", "ww", "r", "g", "b")
CaptureObservationFn = Callable[..., Mapping[str, Any]]


class HsiMeasurementRejected(ValueError):
    def __init__(self, *, phase: str, command: Mapping[str, int], evidence: Mapping[str, Any]):
        super().__init__(f"HSI feedback measurement rejected during {phase}")
        self.phase = str(phase)
        self.command = {str(key): int(value) for key, value in command.items()}
        self.evidence = dict(evidence)


def run_hsi_feedback(
    *,
    initial_command: Mapping[str, int],
    active_channel: str,
    capture_observation_fn: CaptureObservationFn,
    max_code: int = 4095,
    rounds: int = 12,
    probe_step_code: int = 256,
    max_step_code: int = 768,
    damping: float = 0.05,
    confirmations: int = 2,
    thermal_rebases: int = 2,
    channels: Sequence[str] = CHANNELS,
) -> dict[str, Any]:
    if rounds < 0 or confirmations < 1 or thermal_rebases < 0:
        raise ValueError("rounds/rebases must be non-negative and confirmations at least one")
    if active_channel not in channels:
        raise ValueError("active_channel must be in channels")
    samples: list[dict[str, Any]] = []
    confirmation_attempts: list[dict[str, Any]] = []
    rebase_records: list[dict[str, Any]] = []
    measurement_rejections: list[dict[str, Any]] = []

    def capture(command: Mapping[str, int], *, phase: str, settled_confirmation: bool = False) -> dict[str, Any]:
        bounded = {channel: min(max(int(command[channel]), 0), max_code) for channel in channels}
        bounded[active_channel] = max_code
        observation = dict(capture_observation_fn(bounded, phase=phase, settled_confirmation=settled_confirmation))
        if observation.get("measurement_rejected"):
            evidence = observation.get("rejection_evidence")
            if not isinstance(evidence, Mapping):
                raise ValueError("measurement_rejected HSI observation requires rejection_evidence")
            raise HsiMeasurementRejected(phase=phase, command=bounded, evidence=evidence)
        residuals = {group: np.asarray(observation["residuals"][group], dtype=float) for group in GROUP_ORDER}
        objective = dict(observation["objective"])
        sample = {
            "index": len(samples),
            "phase": phase,
            "command": bounded,
            "residuals": {group: values.tolist() for group, values in residuals.items()},
            "objective": objective,
            "observation": {key: value for key, value in observation.items() if key not in {"residuals", "objective"}},
        }
        samples.append(sample)
        return sample

    def probes(base: Mapping[str, Any], prefix: str) -> tuple[list[dict[str, Any]], dict[str, int]]:
        output = []
        deltas = {}
        for channel in channels:
            if channel == active_channel:
                continue
            command = dict(base["command"])
            room_up = max_code - command[channel]
            room_down = command[channel]
            delta = min(probe_step_code, room_up) if room_up >= room_down else -min(probe_step_code, room_down)
            if delta == 0:
                raise ValueError(f"cannot probe fixed HSI channel {channel}")
            command[channel] += delta
            output.append(capture(command, phase=f"{prefix}-{channel}"))
            deltas[channel] = delta
        return output, deltas

    def jacobian(base: Mapping[str, Any], probe_samples: Sequence[Mapping[str, Any]], deltas: Mapping[str, int]) -> dict[str, np.ndarray]:
        by_channel = {str(sample["phase"]).rsplit("-", 1)[-1]: sample["residuals"] for sample in probe_samples}
        return estimate_group_jacobians(
            base["residuals"],
            by_channel,
            deltas,
            active_channel=active_channel,
            max_code=max_code,
            channels=channels,
            group_order=GROUP_ORDER,
        )

    def confirm(candidate: Mapping[str, Any]) -> tuple[bool, dict[str, Any]]:
        record = {"candidate_sample_index": int(candidate["index"]), "sample_indices": [], "status": "running"}
        confirmation_attempts.append(record)
        latest = dict(candidate)
        for index in range(confirmations):
            phase = f"confirm-{len(confirmation_attempts)-1}-{index}"
            try:
                latest = capture(candidate["command"], phase=phase, settled_confirmation=True)
            except HsiMeasurementRejected as exc:
                _record_rejection(measurement_rejections, exc, round_index=None, fraction=None)
                record.update({"status": "measurement_rejected", "rejection_phase": phase})
                return False, dict(candidate)
            record["sample_indices"].append(int(latest["index"]))
            if not bool(latest["objective"]["feasible"]):
                record["status"] = "failed"
                return False, latest
        record["status"] = "confirmed"
        return True, max(
            (samples[index] for index in record["sample_indices"]),
            key=lambda item: hsi_objective_sort_key(item["objective"]),
        )

    current = capture(initial_command, phase="initial")
    confirmed: dict[str, Any] | None = None
    rounds_completed = 0
    status = "round_limit"
    pending_rebase = False
    if bool(current["objective"]["feasible"]):
        ok, current = confirm(current)
        if ok:
            confirmed = current
            status = "goal_confirmed"
        else:
            pending_rebase = True

    matrix: dict[str, np.ndarray] | None = None
    if confirmed is None and rounds > 0:
        prefix = "thermal-rebase-0" if pending_rebase and thermal_rebases else "probe"
        probe_samples, deltas = probes(current, prefix)
        matrix = jacobian(current, probe_samples, deltas)
        if prefix.startswith("thermal-rebase"):
            rebase_records.append({
                "base_sample_index": int(current["index"]),
                "probe_sample_indices": [int(item["index"]) for item in probe_samples],
                "reason": "confirmation_failed",
            })
        for round_index in range(rounds):
            step = solve_lexicographic_local_step(
                current["command"],
                current["residuals"],
                matrix,
                active_channel=active_channel,
                objective_fn=_predicted_objective,
                max_code=max_code,
                max_step_code=max_step_code,
                damping=damping,
                channels=channels,
                group_order=GROUP_ORDER,
                objective_sort_key_fn=hsi_objective_sort_key,
            )
            if step["command"] == current["command"]:
                status = "no_new_command"
                break
            rounds_completed += 1
            candidate = None
            for fraction in (1.0, 0.5, 0.25):
                command = {
                    channel: int(round(
                        int(current["command"][channel])
                        + fraction * (int(step["command"][channel]) - int(current["command"][channel]))
                    ))
                    for channel in channels
                }
                command[active_channel] = max_code
                if command == current["command"]:
                    continue
                phase = f"feedback-{round_index}" if fraction == 1.0 else f"feedback-{round_index}-backtrack-{fraction:g}"
                try:
                    candidate = capture(command, phase=phase)
                except HsiMeasurementRejected as exc:
                    _record_rejection(measurement_rejections, exc, round_index=round_index, fraction=fraction)
                    continue
                break
            if candidate is None:
                status = "candidate_measurement_rejected"
                break
            matrix = _broyden_update(matrix, current, candidate, active_channel=active_channel, max_code=max_code, channels=channels)
            current = candidate
            if bool(candidate["objective"]["feasible"]):
                ok, current = confirm(candidate)
                if ok:
                    confirmed = current
                    status = "goal_confirmed"
                    break
                if len(rebase_records) < thermal_rebases:
                    probe_samples, deltas = probes(current, f"thermal-rebase-{len(rebase_records)}")
                    matrix = jacobian(current, probe_samples, deltas)
                    rebase_records.append({
                        "base_sample_index": int(current["index"]),
                        "probe_sample_indices": [int(item["index"]) for item in probe_samples],
                        "reason": "confirmation_failed",
                    })

    best = confirmed or min(samples, key=lambda item: hsi_objective_sort_key(item["objective"]))
    return {
        "kind": "hsi_bounded_local_feedback",
        "status": status,
        "active_channel": active_channel,
        "initial_command": dict(initial_command),
        "selected_command": dict(best["command"]),
        "goal_confirmed": confirmed is not None,
        "rounds_requested": rounds,
        "rounds_completed": rounds_completed,
        "confirmation_attempts": confirmation_attempts,
        "thermal_rebases": rebase_records,
        "measurement_rejections": measurement_rejections,
        "best": best,
        "samples": samples,
    }


def _predicted_objective(predicted: Mapping[str, np.ndarray], command: Mapping[str, int]) -> dict[str, Any]:
    shape = np.asarray(predicted["shape"], dtype=float)
    hue = float(predicted["hue"][0])
    sat = float(predicted["sat"][0])
    orthogonal = float(np.linalg.norm(shape))
    return {
        "feasible": abs(hue) <= 1.0 and abs(sat) <= 1.0 and orthogonal <= 1.0,
        "hue_normalized": hue,
        "sat_normalized": sat,
        "orthogonal_normalized": orthogonal,
        "shape_normalized_p90": float(np.quantile(np.abs(shape), 0.9)),
        "shape_normalized_maximum": float(np.max(np.abs(shape))),
        "command_continuity_l1": 0.0,
        "predicted_command": dict(command),
    }


def _broyden_update(
    jacobians: Mapping[str, np.ndarray],
    previous: Mapping[str, Any],
    current: Mapping[str, Any],
    *,
    active_channel: str,
    max_code: int,
    channels: Sequence[str],
) -> dict[str, np.ndarray]:
    free = tuple(channel for channel in channels if channel != active_channel)
    delta = np.asarray(
        [(int(current["command"][channel]) - int(previous["command"][channel])) / max_code for channel in free],
        dtype=float,
    )
    denominator = float(delta @ delta)
    if denominator <= 1e-12:
        return {group: np.asarray(matrix, dtype=float).copy() for group, matrix in jacobians.items()}
    output = {}
    for group in GROUP_ORDER:
        matrix = np.asarray(jacobians[group], dtype=float)
        observed = np.asarray(current["residuals"][group], dtype=float) - np.asarray(previous["residuals"][group], dtype=float)
        output[group] = matrix + np.outer(observed - matrix @ delta, delta) / denominator
    return output


def _record_rejection(
    output: list[dict[str, Any]],
    exc: HsiMeasurementRejected,
    *,
    round_index: int | None,
    fraction: float | None,
) -> None:
    output.append({
        "round": round_index,
        "phase": exc.phase,
        "backtrack_fraction": fraction,
        "command": exc.command,
        "evidence": exc.evidence,
    })
