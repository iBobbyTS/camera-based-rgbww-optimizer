from __future__ import annotations

from typing import Any, Callable, Mapping, Sequence

import numpy as np

from camera_based_rgbww_optimizer.optimization.hsi_objective import (
    GROUP_ORDER,
    hsi_objective_sort_key,
)
from camera_based_rgbww_optimizer.optimization.hsi_budget import (
    HsiSolverBudgetLimits,
    HsiStartBudget,
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


class HsiLogicalBudgetExhausted(RuntimeError):
    def __init__(self, *, evidence: Mapping[str, Any], result: Mapping[str, Any]):
        super().__init__("HSI logical observation budget exhausted")
        self.evidence = dict(evidence)
        self.result = dict(result)


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
    confirmations: int = 3,
    thermal_rebases: int = 2,
    channels: Sequence[str] = CHANNELS,
    group_order: Sequence[str] = GROUP_ORDER,
    prediction_error_rebase_threshold: float = 2.0,
    jacobian_condition_limit: float = 1e8,
    consecutive_prediction_misses_for_rebase: int = 2,
    start_budget: HsiStartBudget | None = None,
) -> dict[str, Any]:
    if rounds < 0 or confirmations < 1 or thermal_rebases < 0:
        raise ValueError("rounds/rebases must be non-negative and confirmations at least one")
    if active_channel not in channels:
        raise ValueError("active_channel must be in channels")
    samples: list[dict[str, Any]] = []
    confirmation_attempts: list[dict[str, Any]] = []
    rebase_records: list[dict[str, Any]] = []
    measurement_rejections: list[dict[str, Any]] = []
    step_records: list[dict[str, Any]] = []
    prediction_misses = 0
    confirmation_measurement_unreachable = False
    groups = tuple(str(value) for value in group_order)
    if not groups or len(set(groups)) != len(groups):
        raise ValueError("group_order must contain unique group names")

    def snapshot(*, phase: str) -> dict[str, Any]:
        best = min(samples, key=lambda item: hsi_objective_sort_key(item["objective"])) if samples else None
        return {
            "kind": "hsi_bounded_local_feedback",
            "status": "solver_budget_exhausted",
            "active_channel": active_channel,
            "initial_command": dict(initial_command),
            "selected_command": dict(initial_command if best is None else best["command"]),
            "goal_confirmed": False,
            "rounds_requested": rounds,
            "rounds_completed": len(step_records),
            "confirmation_attempts": confirmation_attempts,
            "thermal_rebases": rebase_records,
            "measurement_rejections": measurement_rejections,
            "step_records": step_records,
            "group_order": list(groups),
            "best": best,
            "samples": samples,
            "budget": None if start_budget is None else start_budget.to_jsonable(),
            "exhaustion_phase": phase,
        }

    def require_budget(ok: bool, *, phase: str) -> None:
        if not ok:
            evidence = {"status": "solver_budget_exhausted", "phase": phase}
            if start_budget is not None:
                evidence.update(start_budget.exhaustion or {})
            raise HsiLogicalBudgetExhausted(evidence=evidence, result=snapshot(phase=phase))

    def capture(command: Mapping[str, int], *, phase: str, settled_confirmation: bool = False) -> dict[str, Any]:
        if start_budget is not None:
            require_budget(start_budget.consume(phase=phase), phase=phase)
        bounded = {channel: min(max(int(command[channel]), 0), max_code) for channel in channels}
        bounded[active_channel] = max_code
        observation = dict(capture_observation_fn(bounded, phase=phase, settled_confirmation=settled_confirmation))
        if observation.get("measurement_rejected"):
            evidence = observation.get("rejection_evidence")
            if not isinstance(evidence, Mapping):
                raise ValueError("measurement_rejected HSI observation requires rejection_evidence")
            if evidence.get("status") == "solver_budget_exhausted":
                raise HsiLogicalBudgetExhausted(evidence=evidence, result=snapshot(phase=phase))
            raise HsiMeasurementRejected(phase=phase, command=bounded, evidence=evidence)
        residuals = {group: np.asarray(observation["residuals"][group], dtype=float) for group in groups}
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
        if start_budget is not None:
            require_budget(
                start_budget.reserve_probe_group(phase=prefix, rebase="rebase" in prefix),
                phase=prefix,
            )
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
            group_order=groups,
        )

    def confirm(candidate: Mapping[str, Any], *, verification_kind: str = "solver_candidate") -> tuple[bool, dict[str, Any]]:
        nonlocal confirmation_measurement_unreachable
        if start_budget is not None:
            require_budget(
                start_budget.reserve_confirmation_group(phase=f"confirm-{len(confirmation_attempts)}"),
                phase=f"confirm-{len(confirmation_attempts)}",
            )
        record = {
            "candidate_sample_index": int(candidate["index"]),
            "candidate_command": dict(candidate["command"]),
            "verification_kind": verification_kind,
            "expected_capture_count": int(confirmations),
            "sample_indices": [],
            "status": "running",
        }
        confirmation_attempts.append(record)
        latest = dict(candidate)
        for index in range(confirmations):
            phase = f"confirm-{len(confirmation_attempts)-1}-{index}"
            try:
                latest = capture(candidate["command"], phase=phase, settled_confirmation=True)
            except HsiMeasurementRejected as exc:
                _record_rejection(measurement_rejections, exc, round_index=None, fraction=None)
                confirmation_measurement_unreachable = True
                record.update({
                    "status": "measurement_rejected",
                    "rejection_phase": phase,
                    "captured_count": len(record["sample_indices"]),
                    "partial_group": True,
                })
                return False, dict(candidate)
            except HsiLogicalBudgetExhausted:
                record.update({
                    "status": "solver_budget_exhausted",
                    "rejection_phase": phase,
                    "captured_count": len(record["sample_indices"]),
                    "partial_group": True,
                })
                raise
            record["sample_indices"].append(int(latest["index"]))
        group_samples = [samples[index] for index in record["sample_indices"]]
        group_passed = all(bool(item["objective"]["feasible"]) for item in group_samples)
        record.update({
            "status": "confirmed" if group_passed else "failed",
            "captured_count": len(group_samples),
            "partial_group": False,
            "feasible_capture_count": sum(bool(item["objective"]["feasible"]) for item in group_samples),
        })
        return group_passed, max(
            group_samples,
            key=lambda item: hsi_objective_sort_key(item["objective"]),
        )

    current = capture(initial_command, phase="initial")
    confirmed: dict[str, Any] | None = None
    rounds_completed = 0
    status = "solver_budget_exhausted"
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
                objective_fn=lambda predicted, command: _predicted_objective(
                    predicted,
                    command,
                    group_order=groups,
                    coordinate_guarded_limit=current["objective"].get("coordinate_guarded_limit"),
                ),
                max_code=max_code,
                max_step_code=max_step_code,
                damping=damping,
                channels=channels,
                group_order=groups,
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
            predicted_residuals = {
                group: np.asarray(step["predicted_residuals"][group], dtype=float) for group in groups
            }
            prediction_error, prediction_error_by_group = _normalized_prediction_error(
                candidate["residuals"], predicted_residuals,
                group_order=groups,
                coordinate_guarded_limit=current["objective"].get("coordinate_guarded_limit"),
            )
            condition = _jacobian_condition(matrix, groups)
            step_records.append({
                "round": round_index,
                "source": step["source"],
                "predicted_residuals": {group: value.tolist() for group, value in predicted_residuals.items()},
                "actual_residuals": {group: list(candidate["residuals"][group]) for group in groups},
                "prediction_error_rms": prediction_error,
                "prediction_error_normalized_by_group": prediction_error_by_group,
                "prediction_error_space": "v2_guarded_coordinate_and_whitened_rendering" if groups == ("coordinate", "rendering") else "v1_normalized_groups",
                "jacobian_condition": condition,
                "command": dict(candidate["command"]),
            })
            prediction_misses = prediction_misses + 1 if (
                prediction_error > prediction_error_rebase_threshold or condition > jacobian_condition_limit
            ) else 0
            matrix = _broyden_update(
                matrix, current, candidate, active_channel=active_channel,
                max_code=max_code, channels=channels, group_order=groups,
            )
            current = candidate
            if (
                prediction_misses >= consecutive_prediction_misses_for_rebase
                and len(rebase_records) < thermal_rebases
            ):
                probe_samples, deltas = probes(current, f"prediction-rebase-{len(rebase_records)}")
                matrix = jacobian(current, probe_samples, deltas)
                rebase_records.append({
                    "base_sample_index": int(current["index"]),
                    "probe_sample_indices": [int(item["index"]) for item in probe_samples],
                    "reason": "prediction_error" if condition <= jacobian_condition_limit else "jacobian_condition",
                    "prediction_error_rms": prediction_error,
                    "jacobian_condition": condition,
                })
                prediction_misses = 0
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

    if (
        confirmed is None
        and samples
        and not confirmation_measurement_unreachable
        and (
            start_budget is None
            or start_budget.confirmation_groups_started < start_budget.limits.confirmation_groups_per_start
        )
    ):
        best_valid = min(samples, key=lambda item: hsi_objective_sort_key(item["objective"]))
        ok, verified = confirm(best_valid, verification_kind="final_best_valid")
        if ok:
            confirmed = verified
            status = "goal_confirmed"
        elif status not in {"solver_budget_exhausted", "measurement_unreachable"}:
            status = "unconfirmed"

    if confirmation_measurement_unreachable:
        status = "measurement_unreachable"
    elif any(
        item.get("evidence", {}).get("status") == "solver_budget_exhausted"
        for item in measurement_rejections
    ):
        status = "solver_budget_exhausted"
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
        "step_records": step_records,
        "group_order": list(groups),
        "prediction_rebase_policy": {
            "prediction_error_rms_limit": float(prediction_error_rebase_threshold),
            "jacobian_condition_limit": float(jacobian_condition_limit),
            "consecutive_misses": int(consecutive_prediction_misses_for_rebase),
        },
        "best": best,
        "samples": samples,
        "budget": None if start_budget is None else start_budget.to_jsonable(),
    }


def _predicted_objective(
    predicted: Mapping[str, np.ndarray], command: Mapping[str, int],
    *, group_order: Sequence[str] = GROUP_ORDER,
    coordinate_guarded_limit: float | None = None,
) -> dict[str, Any]:
    if tuple(group_order) == ("coordinate", "rendering"):
        coordinate = np.asarray(predicted["coordinate"], dtype=float)
        rendering = np.asarray(predicted["rendering"], dtype=float)
        if coordinate_guarded_limit is None or not np.isfinite(coordinate_guarded_limit) or coordinate_guarded_limit <= 0.0:
            raise ValueError("v2 predicted objective requires the frozen target-specific guarded limit")
        coordinate_norm = float(np.linalg.norm(coordinate))
        coordinate_excess = max(coordinate_norm / float(coordinate_guarded_limit) - 1.0, 0.0)
        rendering_norm = float(np.linalg.norm(rendering))
        return {
            "kind": "ray_hsi_policy_v2_lexicographic",
            "feasible": coordinate_norm <= float(coordinate_guarded_limit),
            "hue_defined": coordinate.size > 1,
            "hue_error_degrees": 0.0 if coordinate.size <= 1 else float(coordinate[0]),
            "sat_error_percent": float(coordinate[-1]),
            "coordinate_guarded_limit": float(coordinate_guarded_limit),
            "coordinate_guarded_excess": coordinate_excess,
            "color_rendering_residual": {"whitened_score": rendering_norm},
            "command_continuity_l1": 0.0,
            "predicted_command": dict(command),
        }
    shape = np.asarray(predicted["shape"], dtype=float)
    hue = float(predicted["hue"][0])
    sat = float(predicted["sat"][0])
    orthogonal = float(np.linalg.norm(shape))
    joint_score = max(abs(hue), abs(sat), orthogonal)
    return {
        "feasible": abs(hue) <= 1.0 and abs(sat) <= 1.0 and orthogonal <= 1.0,
        "hue_defined": True,
        "hue_normalized": hue,
        "sat_normalized": sat,
        "orthogonal_normalized": orthogonal,
        "joint_score": joint_score,
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
    group_order: Sequence[str] = GROUP_ORDER,
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
    for group in group_order:
        matrix = np.asarray(jacobians[group], dtype=float)
        observed = np.asarray(current["residuals"][group], dtype=float) - np.asarray(previous["residuals"][group], dtype=float)
        output[group] = matrix + np.outer(observed - matrix @ delta, delta) / denominator
    return output


def _jacobian_condition(
    jacobians: Mapping[str, np.ndarray], group_order: Sequence[str]
) -> float:
    matrix = np.vstack([np.asarray(jacobians[group], dtype=float) for group in group_order])
    return float(np.linalg.cond(matrix))


def run_hsi_feedback_multiseed(
    *,
    seeds: Sequence[Mapping[str, Any]],
    capture_observation_fn: CaptureObservationFn,
    max_starts: int,
    rounds_per_start: int,
    budget_limits: HsiSolverBudgetLimits,
    group_order: Sequence[str] = ("coordinate", "rendering"),
    **feedback_kwargs: Any,
) -> dict[str, Any]:
    if max_starts < 1 or rounds_per_start < 0:
        raise ValueError("bounded multi-seed limits must be positive")
    if max_starts != budget_limits.max_starts or rounds_per_start != budget_limits.feedback_attempts_per_start:
        raise ValueError("multi-seed runtime limits must equal the declared Planner budget")
    selected = list(seeds[:max_starts])
    if not selected or len({str(item["active_channel"]) for item in selected}) != len(selected):
        raise ValueError("bounded multi-seed requires distinct active-channel faces")
    attempts = []

    for start_index, seed in enumerate(selected):
        start_budget = HsiStartBudget(budget_limits, start_index=start_index)
        try:
            result = run_hsi_feedback(
                initial_command=seed["command"],
                active_channel=str(seed["active_channel"]),
                capture_observation_fn=capture_observation_fn,
                rounds=rounds_per_start,
                confirmations=budget_limits.confirmations_per_group,
                thermal_rebases=budget_limits.rebase_count_per_start,
                group_order=group_order,
                start_budget=start_budget,
                **feedback_kwargs,
            )
        except HsiLogicalBudgetExhausted as exc:
            result = dict(exc.result)
            result["budget_exhaustion"] = dict(exc.evidence)
        except HsiMeasurementRejected as exc:
            exhausted = exc.evidence.get("status") == "solver_budget_exhausted"
            result = {
                "kind": "hsi_bounded_local_feedback",
                "status": "solver_budget_exhausted" if exhausted else "measurement_unreachable",
                "active_channel": str(seed["active_channel"]),
                "initial_command": dict(seed["command"]),
                "selected_command": dict(seed["command"]),
                "goal_confirmed": False,
                "rounds_requested": rounds_per_start,
                "rounds_completed": 0,
                "confirmation_attempts": [],
                "thermal_rebases": [],
                "measurement_rejections": [{
                    "phase": exc.phase, "command": exc.command, "evidence": exc.evidence,
                }],
                "step_records": [],
                "group_order": list(group_order),
                "best": None,
                "samples": [],
                "budget": start_budget.to_jsonable(),
                "budget_exhaustion": dict(exc.evidence) if exhausted else None,
            }
        attempts.append({"start_index": start_index, "seed": dict(seed), "result": result})
        if result["goal_confirmed"]:
            break
    confirmed_attempts = [item for item in attempts if item["result"].get("goal_confirmed")]
    valid_attempts = [item for item in attempts if item["result"].get("best") is not None]
    selection_pool = confirmed_attempts or valid_attempts
    best_attempt = min(
        selection_pool or attempts,
        key=lambda item: hsi_objective_sort_key(item["result"]["best"]["objective"]),
    ) if selection_pool else attempts[0]
    logical_used = sum(int(item["result"].get("budget", {}).get("logical_observations_used", 0)) for item in attempts)
    exhausted = any(item["result"].get("status") == "solver_budget_exhausted" for item in attempts)
    all_unreachable = all(item["result"].get("status") == "measurement_unreachable" for item in attempts)
    overall_status = (
        "goal_confirmed" if confirmed_attempts
        else "solver_budget_exhausted" if exhausted
        else "measurement_unreachable" if all_unreachable
        else "unconfirmed"
    )
    return {
        "kind": "hsi_bounded_multiseed_feedback_v2",
        "max_starts": int(max_starts),
        "rounds_per_start": int(rounds_per_start),
        "status": overall_status,
        "budget_declaration": budget_limits.to_jsonable(),
        "logical_observations_used": logical_used,
        "attempt_count": len(attempts),
        "attempts": attempts,
        "selected_start_index": int(best_attempt["start_index"]),
        "selected_result": best_attempt["result"],
        "best_valid_sample": best_attempt["result"].get("best"),
    }


def _normalized_prediction_error(
    actual: Mapping[str, Sequence[float]], predicted: Mapping[str, np.ndarray],
    *, group_order: Sequence[str], coordinate_guarded_limit: float | None,
) -> tuple[float, dict[str, float]]:
    by_group: dict[str, float] = {}
    for group in group_order:
        delta = np.asarray(actual[group], dtype=float) - np.asarray(predicted[group], dtype=float)
        if group == "coordinate" and tuple(group_order) == ("coordinate", "rendering"):
            if coordinate_guarded_limit is None or coordinate_guarded_limit <= 0.0:
                raise ValueError("v2 prediction error requires coordinate guarded limit")
            delta = delta / float(coordinate_guarded_limit)
        by_group[group] = float(np.sqrt(np.mean(delta * delta)))
    return float(np.sqrt(sum(value * value for value in by_group.values()))), by_group


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
