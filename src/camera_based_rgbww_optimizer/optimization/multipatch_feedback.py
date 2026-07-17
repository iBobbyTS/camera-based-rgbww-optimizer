from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from typing import Any

import numpy as np

from camera_based_rgbww_optimizer.optimization.multipatch_objective import (
    objective_from_residual_groups,
    objective_sort_key,
)
from camera_based_rgbww_optimizer.optimization.multipatch_solver import (
    CHANNELS,
    GROUP_ORDER,
    estimate_group_jacobians,
    solve_lexicographic_local_step,
)
from camera_based_rgbww_optimizer.optimization import white_lut_feedback as white_feedback


CaptureObservationFn = Callable[..., Mapping[str, Any]]


class FeedbackMeasurementRejected(ValueError):
    def __init__(self, *, phase: str, command: Mapping[str, int], evidence: Mapping[str, Any]):
        super().__init__(f"feedback measurement rejected during {phase}")
        self.phase = str(phase)
        self.command = {str(key): int(value) for key, value in command.items()}
        self.evidence = dict(evidence)


def run_multipatch_feedback(
    *,
    initial_command: Mapping[str, int],
    active_channel: str,
    capture_observation_fn: CaptureObservationFn,
    neutral_chroma_tolerance: float,
    max_code: int = 4095,
    rounds: int = 16,
    probe_step_code: int = 256,
    max_step_code: int = 768,
    damping: float = 0.05,
    confirmations: int = 2,
    thermal_rebases: int = 2,
    acceptance_rank_key: Sequence[float] | None = None,
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
    acceptance_key = None if acceptance_rank_key is None else tuple(float(value) for value in acceptance_rank_key)

    def acceptable(objective: Mapping[str, Any]) -> bool:
        return bool(objective["feasible"]) and (
            acceptance_key is None or objective_sort_key(objective) < acceptance_key
        )

    def capture(command: Mapping[str, int], *, phase: str, settled_confirmation: bool = False) -> dict[str, Any]:
        bounded = {channel: min(max(int(command[channel]), 0), max_code) for channel in channels}
        bounded[active_channel] = max_code
        observation = dict(capture_observation_fn(bounded, phase=phase, settled_confirmation=settled_confirmation))
        if observation.get("measurement_rejected"):
            evidence = observation.get("rejection_evidence")
            if not isinstance(evidence, Mapping):
                raise ValueError("measurement_rejected feedback observation requires rejection_evidence")
            raise FeedbackMeasurementRejected(phase=phase, command=bounded, evidence=evidence)
        residuals = {group: np.asarray(observation["residuals"][group], dtype="float64") for group in GROUP_ORDER}
        objective = dict(observation.get("objective") or objective_from_residual_groups(
            residuals, neutral_chroma_tolerance=neutral_chroma_tolerance
        ))
        sample = {
            "index": len(samples), "phase": phase, "command": bounded,
            "residuals": {group: value.tolist() for group, value in residuals.items()},
            "objective": objective,
            "white_point_comparison": {
                "normalized_error": residuals["white"].tolist(),
                "goal_score": float(np.max(np.abs(residuals["white"]))),
                "absolute_cct_error_K": float(abs(residuals["white"][0])),
            },
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
                raise ValueError(f"cannot probe fixed channel {channel}")
            command[channel] += delta
            output.append(capture(command, phase=f"{prefix}-{channel}"))
            deltas[channel] = delta
        return output, deltas

    def jacobian(base: Mapping[str, Any], probe_samples: Sequence[Mapping[str, Any]], deltas: Mapping[str, int]) -> dict[str, np.ndarray]:
        by_channel = {str(sample["phase"]).rsplit("-", 1)[-1]: sample["residuals"] for sample in probe_samples}
        return estimate_group_jacobians(
            base["residuals"], by_channel, deltas,
            active_channel=active_channel, max_code=max_code, channels=channels,
        )

    def confirm(candidate: Mapping[str, Any]) -> tuple[bool, dict[str, Any]]:
        record = {"candidate_sample_index": int(candidate["index"]), "sample_indices": [], "status": "running"}
        confirmation_attempts.append(record)
        latest = dict(candidate)
        for index in range(confirmations):
            phase = f"confirm-{len(confirmation_attempts)-1}-{index}"
            try:
                latest = capture(candidate["command"], phase=phase, settled_confirmation=True)
            except FeedbackMeasurementRejected as exc:
                measurement_rejections.append({
                    "round": None,
                    "phase": exc.phase,
                    "backtrack_fraction": None,
                    "command": exc.command,
                    "evidence": exc.evidence,
                })
                record["status"] = "measurement_rejected"
                record["rejection_phase"] = phase
                return False, dict(candidate)
            record["sample_indices"].append(int(latest["index"]))
            if not acceptable(latest["objective"]):
                record["status"] = "failed"
                return False, latest
        record["status"] = "confirmed"
        return True, max(
            (samples[index] for index in record["sample_indices"]),
            key=lambda item: objective_sort_key(item["objective"]),
        )

    current = capture(initial_command, phase="initial")
    confirmed: dict[str, Any] | None = None
    matrix: dict[str, np.ndarray] | None = None
    pending_confirmation_rebase = False
    step_samples: list[dict[str, Any]] = []
    consecutive_secant_misses = 0
    rounds_completed = 0
    status = "round_limit"
    if acceptable(current["objective"]):
        ok, latest = confirm(current)
        current = latest
        if ok:
            confirmed = latest
            status = "goal_confirmed"
        else:
            pending_confirmation_rebase = True

    if confirmed is None and rounds > 0:
        perform_initial_rebase = pending_confirmation_rebase and thermal_rebases > 0
        probe_prefix = "thermal-rebase-0" if perform_initial_rebase else "probe"
        probe_samples, deltas = probes(current, probe_prefix)
        matrix = jacobian(current, probe_samples, deltas)
        step_samples = [current, *probe_samples]
        if perform_initial_rebase:
            rebase_records.append({
                "base_sample_index": int(current["index"]),
                "probe_sample_indices": [int(item["index"]) for item in probe_samples],
                "reason": "confirmation_failed",
            })
        for round_index in range(rounds):
            step = white_feedback.build_bracketed_cct_step(
                step_samples,
                current["command"],
                active_channel=active_channel,
                max_code=max_code,
                channels=channels,
            )
            if step is None:
                step = solve_lexicographic_local_step(
                    current["command"], current["residuals"], matrix,
                    active_channel=active_channel,
                    objective_fn=lambda predicted, _command: objective_from_residual_groups(
                        predicted, neutral_chroma_tolerance=neutral_chroma_tolerance
                    ),
                    max_code=max_code, max_step_code=max_step_code, damping=damping, channels=channels,
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
                except FeedbackMeasurementRejected as exc:
                    measurement_rejections.append({
                        "round": round_index,
                        "phase": exc.phase,
                        "backtrack_fraction": fraction,
                        "command": exc.command,
                        "evidence": exc.evidence,
                    })
                    continue
                break
            if candidate is None:
                status = "candidate_measurement_rejected"
                break
            step_samples.append(candidate)
            matrix = _broyden_update_groups(
                matrix, current, candidate, active_channel=active_channel,
                max_code=max_code, channels=channels,
            )
            current = candidate
            if white_feedback.bracketed_cct_prediction_missed(step, candidate):
                consecutive_secant_misses += 1
            else:
                consecutive_secant_misses = 0
            if consecutive_secant_misses >= white_feedback.SECANT_MISSES_BEFORE_THERMAL_REBASE:
                if len(rebase_records) < thermal_rebases:
                    probe_samples, deltas = probes(current, f"thermal-rebase-{len(rebase_records)}")
                    matrix = jacobian(current, probe_samples, deltas)
                    step_samples = [current, *probe_samples]
                    rebase_records.append({
                        "base_sample_index": int(current["index"]),
                        "probe_sample_indices": [int(item["index"]) for item in probe_samples],
                        "reason": "repeated_secant_prediction_miss",
                    })
                consecutive_secant_misses = 0
                continue
            if acceptable(candidate["objective"]):
                ok, latest = confirm(candidate)
                current = latest
                if ok:
                    confirmed = latest
                    status = "goal_confirmed"
                    break
                if len(rebase_records) < thermal_rebases:
                    probe_samples, deltas = probes(current, f"thermal-rebase-{len(rebase_records)}")
                    matrix = jacobian(current, probe_samples, deltas)
                    step_samples = [current, *probe_samples]
                    rebase_records.append({
                        "base_sample_index": int(current["index"]),
                        "probe_sample_indices": [int(item["index"]) for item in probe_samples],
                        "reason": "confirmation_failed",
                    })

    best = confirmed or min(samples, key=lambda item: objective_sort_key(item["objective"]))
    return {
        "kind": "multipatch_bounded_local_feedback",
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
        "acceptance_rank_key": None if acceptance_key is None else list(acceptance_key),
        "best": best,
        "samples": samples,
    }


def _broyden_update_groups(
    jacobians: Mapping[str, np.ndarray],
    previous: Mapping[str, Any],
    current: Mapping[str, Any],
    *,
    active_channel: str,
    max_code: int,
    channels: Sequence[str],
) -> dict[str, np.ndarray]:
    free = [channel for channel in channels if channel != active_channel]
    delta = np.asarray([
        (int(current["command"][channel]) - int(previous["command"][channel])) / max_code
        for channel in free
    ], dtype="float64")
    denominator = float(delta @ delta)
    if denominator < 1e-12:
        return {group: np.asarray(matrix).copy() for group, matrix in jacobians.items()}
    output = {}
    for group in GROUP_ORDER:
        matrix = np.asarray(jacobians[group], dtype="float64")
        previous_residual = np.asarray(previous["residuals"][group], dtype="float64")
        current_residual = np.asarray(current["residuals"][group], dtype="float64")
        correction = current_residual - previous_residual - matrix @ delta
        output[group] = matrix + np.outer(correction, delta) / denominator
    return output
