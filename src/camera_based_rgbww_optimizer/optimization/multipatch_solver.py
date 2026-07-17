from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from typing import Any

import numpy as np

from camera_based_rgbww_optimizer.optimization.bounded_least_squares import (
    solve_box_constrained_least_squares,
)
from camera_based_rgbww_optimizer.optimization.multipatch_objective import objective_sort_key
from camera_based_rgbww_optimizer.measurement.chart_basis_validation import predict_piecewise_basis


CHANNELS = ("cw", "ww", "r", "g", "b")
GROUP_ORDER = ("neutral", "white", "training", "holdout")


def solve_lexicographic_local_step(
    command: Mapping[str, int],
    residuals: Mapping[str, Any],
    jacobians: Mapping[str, Any],
    *,
    active_channel: str,
    objective_fn: Callable[[Mapping[str, np.ndarray], Mapping[str, int]], Mapping[str, Any]],
    max_code: int = 4095,
    max_step_code: int = 768,
    damping: float = 0.05,
    channels: Sequence[str] = CHANNELS,
    group_order: Sequence[str] = GROUP_ORDER,
    objective_sort_key_fn: Callable[[Mapping[str, Any]], tuple[Any, ...]] = objective_sort_key,
) -> dict[str, Any]:
    """Propose a bounded local step and rank prefix fits lexicographically."""
    if active_channel not in channels:
        raise ValueError("active_channel must be in channels")
    if max_code <= 0 or max_step_code <= 0 or damping <= 0:
        raise ValueError("max_code, max_step_code, and damping must be positive")
    free = tuple(channel for channel in channels if channel != active_channel)
    normalized_residuals: dict[str, np.ndarray] = {}
    normalized_jacobians: dict[str, np.ndarray] = {}
    groups = tuple(str(group) for group in group_order)
    if not groups or len(set(groups)) != len(groups):
        raise ValueError("group_order must contain unique group names")
    for group in groups:
        residual = np.asarray(residuals[group], dtype="float64")
        jacobian = np.asarray(jacobians[group], dtype="float64")
        if residual.ndim != 1 or jacobian.shape != (residual.size, len(free)):
            raise ValueError(f"invalid residual/Jacobian shape for {group}")
        normalized_residuals[group] = residual
        normalized_jacobians[group] = jacobian

    current = np.asarray([int(command[channel]) / max_code for channel in free], dtype="float64")
    max_step = float(max_step_code) / float(max_code)
    lower = np.maximum(-max_step, -current)
    upper = np.minimum(max_step, 1.0 - current)
    candidates: list[dict[str, Any]] = []
    seen: set[tuple[int, ...]] = set()

    def add_candidate(delta: np.ndarray, source: str) -> None:
        for fraction in (1.0, 0.5, 0.25):
            proposed = dict(command)
            for index, channel in enumerate(free):
                proposed[channel] = min(
                    max(int(round(int(command[channel]) + float(delta[index]) * fraction * max_code)), 0),
                    max_code,
                )
            proposed[active_channel] = max_code
            key = tuple(int(proposed[channel]) for channel in channels)
            if key in seen:
                continue
            seen.add(key)
            actual_delta = np.asarray(
                [(proposed[channel] - int(command[channel])) / max_code for channel in free],
                dtype="float64",
            )
            predicted = {
                group: normalized_residuals[group] + normalized_jacobians[group] @ actual_delta
                for group in groups
            }
            objective = dict(objective_fn(predicted, proposed))
            candidates.append(
                {
                    "command": proposed,
                    "active_channel": active_channel,
                    "free_channels": list(free),
                    "delta_codes": {channel: proposed[channel] - int(command[channel]) for channel in free},
                    "predicted_residuals": {group: values.tolist() for group, values in predicted.items()},
                    "predicted_objective": objective,
                    "source": source,
                    "line_search_fraction": fraction,
                }
            )

    add_candidate(np.zeros(len(free), dtype="float64"), "current")
    for prefix_end in range(1, len(groups) + 1):
        prefix = groups[:prefix_end]
        matrix = np.vstack([normalized_jacobians[group] for group in prefix])
        target = np.concatenate([-normalized_residuals[group] for group in prefix])
        augmented_matrix = np.vstack((matrix, np.sqrt(damping) * np.eye(len(free))))
        augmented_target = np.concatenate((target, np.zeros(len(free), dtype="float64")))
        delta = solve_box_constrained_least_squares(
            augmented_matrix,
            augmented_target,
            lower,
            upper,
        )
        add_candidate(delta, f"prefix:{'+'.join(prefix)}")

    best = min(candidates, key=lambda item: objective_sort_key_fn(item["predicted_objective"]))
    return {**best, "candidate_count": len(candidates)}


def estimate_group_jacobians(
    base_residuals: Mapping[str, Any],
    probe_residuals: Mapping[str, Mapping[str, Any]],
    probe_delta_codes: Mapping[str, int],
    *,
    active_channel: str,
    max_code: int = 4095,
    channels: Sequence[str] = CHANNELS,
    group_order: Sequence[str] = GROUP_ORDER,
) -> dict[str, np.ndarray]:
    free = tuple(channel for channel in channels if channel != active_channel)
    output: dict[str, np.ndarray] = {}
    groups = tuple(str(group) for group in group_order)
    if not groups or len(set(groups)) != len(groups):
        raise ValueError("group_order must contain unique group names")
    for group in groups:
        base = np.asarray(base_residuals[group], dtype="float64")
        matrix = np.zeros((base.size, len(free)), dtype="float64")
        for index, channel in enumerate(free):
            delta = int(probe_delta_codes[channel]) / max_code
            if abs(delta) < 1e-12:
                raise ValueError(f"probe delta for {channel} must be non-zero")
            probe = np.asarray(probe_residuals[channel][group], dtype="float64")
            if probe.shape != base.shape:
                raise ValueError(f"probe residual shape mismatch for {channel}/{group}")
            matrix[:, index] = (probe - base) / delta
        output[group] = matrix
    return output


def solve_piecewise_basis_seed(
    basis: Mapping[str, Any],
    target_by_feature: Mapping[str, float],
    *,
    feature_ids: Sequence[str],
    initial_command: Mapping[str, int] | None = None,
    max_code: int = 4095,
    refinement_steps: Sequence[int] = (1024, 512, 256, 128, 64),
    channels: Sequence[str] = CHANNELS,
) -> dict[str, Any]:
    """Use the frozen P2 model only to choose a high-output starting command."""
    feature_order = list(basis["feature_order"])
    indices = [feature_order.index(feature) for feature in feature_ids]
    target = np.asarray([target_by_feature[feature] for feature in feature_ids], dtype="float64")
    floor = max(float(np.median(np.abs(target))) * 1e-6, 1e-12)
    if np.any(~np.isfinite(target)) or np.linalg.norm(target) <= 0:
        raise ValueError("basis seed target must contain finite measurable features")

    def score(command: Mapping[str, int]) -> tuple[float, float]:
        prediction = np.asarray(predict_piecewise_basis(basis, command)["values"], dtype="float64")[indices]
        denominator = float(prediction @ prediction)
        scale = 0.0 if denominator <= 0 else max(0.0, float(prediction @ target) / denominator)
        relative = (scale * prediction - target) / np.maximum(np.abs(target), floor)
        return float(np.sqrt(np.mean(relative * relative))), scale

    candidates: list[dict[str, Any]] = []
    for active_channel in channels:
        command = {
            channel: min(max(int((initial_command or {}).get(channel, max_code // 2)), 0), max_code)
            for channel in channels
        }
        command[active_channel] = max_code
        current_score, current_scale = score(command)
        evaluations = 1
        for step in refinement_steps:
            if int(step) <= 0:
                raise ValueError("basis seed refinement steps must be positive")
            improved = True
            while improved:
                improved = False
                best = (current_score, dict(command), current_scale)
                for channel in channels:
                    if channel == active_channel:
                        continue
                    for direction in (-1, 1):
                        trial = dict(command)
                        trial[channel] = min(max(trial[channel] + direction * int(step), 0), max_code)
                        if trial[channel] == command[channel]:
                            continue
                        trial_score, trial_scale = score(trial)
                        evaluations += 1
                        if trial_score < best[0] - 1e-12:
                            best = (trial_score, trial, trial_scale)
                if best[1] != command:
                    current_score, command, current_scale = best
                    improved = True
        candidates.append({
            "active_channel": active_channel,
            "command": command,
            "predicted_relative_rmse": current_score,
            "predicted_brightness_scale": current_scale,
            "evaluation_count": evaluations,
        })
    best = min(candidates, key=lambda item: item["predicted_relative_rmse"])
    return {"kind": "p2_piecewise_basis_seed_only", "best": best, "candidates": candidates}
