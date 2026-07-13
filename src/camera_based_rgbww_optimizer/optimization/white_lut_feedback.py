from __future__ import annotations

import time
from collections.abc import Mapping, Sequence
from itertools import product
from pathlib import Path
from typing import Any, Callable

import numpy as np

from camera_based_rgbww_optimizer.control import camera_gphoto2
from camera_based_rgbww_optimizer.optimization import white_calibration_common as common


DEFAULT_CHANNELS = ("cw", "ww", "r", "g", "b")
SECANT_MISSES_BEFORE_THERMAL_REBASE = 2
SECANT_MISS_SCORE_RATIO = 2.0
SECANT_MISS_SCORE_SLACK = 0.5

LightFn = Callable[..., dict[str, int]]
AutoExposeFn = Callable[..., camera_gphoto2.AutoExposureResult]
CaptureFn = Callable[..., camera_gphoto2.CaptureResult]
DecoderFn = Callable[..., camera_gphoto2.DecodeResult]
WhitePointEstimatorFn = Callable[[camera_gphoto2.CaptureResult, Sequence[dict[str, Any]]], dict[str, Any]]


def resolve_cct_tolerance_K(
    target_cct_K: float,
    *,
    minimum_tolerance_K: float,
    tolerance_mired: float,
) -> float:
    if target_cct_K <= 0:
        raise ValueError("target_cct_K must be positive")
    if minimum_tolerance_K <= 0:
        raise ValueError("minimum_tolerance_K must be positive")
    if tolerance_mired <= 0:
        raise ValueError("tolerance_mired must be positive")
    mired_equivalent_K = float(target_cct_K) ** 2 * float(tolerance_mired) / 1_000_000.0
    return max(float(minimum_tolerance_K), mired_equivalent_K)


def white_point_metrics(
    candidate: Mapping[str, Any],
    target: Mapping[str, Any],
    *,
    cct_tolerance_K: float,
    duv_tolerance: float,
) -> dict[str, Any]:
    if cct_tolerance_K <= 0:
        raise ValueError("cct_tolerance_K must be positive")
    if duv_tolerance <= 0:
        raise ValueError("duv_tolerance must be positive")
    cct_error = float(candidate["cct_K"]) - float(target["cct_K"])
    duv_error = float(candidate["duv"]) - float(target["duv"])
    normalized_error = [cct_error / float(cct_tolerance_K), duv_error / float(duv_tolerance)]
    return {
        "cct_error_K": cct_error,
        "duv_error": duv_error,
        "absolute_cct_error_K": abs(cct_error),
        "absolute_duv_error": abs(duv_error),
        "normalized_error": normalized_error,
        "goal_score": max(abs(normalized_error[0]), abs(normalized_error[1])),
        "within_goal": abs(cct_error) < float(cct_tolerance_K) and abs(duv_error) < float(duv_tolerance),
    }


def free_channels(channels: Sequence[str], active_channel: str) -> tuple[str, ...]:
    if active_channel not in channels:
        raise ValueError(f"active channel {active_channel!r} is not in the channel list")
    return tuple(channel for channel in channels if channel != active_channel)


def resolve_channel_penalties(
    *,
    rgb_penalty: float,
    channel_penalties: Mapping[str, float] | None,
) -> dict[str, float]:
    resolved = {
        channel: float(rgb_penalty if channel_penalties is None else channel_penalties.get(channel, rgb_penalty))
        for channel in ("r", "g", "b")
    }
    for channel, value in resolved.items():
        if value < 0:
            raise ValueError(f"RGB penalty must be non-negative for channel {channel}")
    return resolved


def build_probe_commands(
    command: Mapping[str, int],
    *,
    active_channel: str,
    probe_step_code: int,
    max_code: int,
    channels: Sequence[str] = DEFAULT_CHANNELS,
) -> list[dict[str, Any]]:
    if probe_step_code <= 0:
        raise ValueError("probe_step_code must be positive")
    if max_code <= 0:
        raise ValueError("max_code must be positive")
    probes: list[dict[str, Any]] = []
    for channel in free_channels(channels, active_channel):
        value = min(max(int(command[channel]), 0), int(max_code))
        room_up = int(max_code) - value
        room_down = value
        if room_up <= 0 and room_down <= 0:
            continue
        if room_up >= room_down:
            delta = min(int(probe_step_code), room_up)
        else:
            delta = -min(int(probe_step_code), room_down)
        if delta == 0:
            continue
        probe_command = {name: min(max(int(command[name]), 0), int(max_code)) for name in channels}
        probe_command[active_channel] = int(max_code)
        probe_command[channel] = value + delta
        probes.append({
            "channel": channel,
            "delta_code": int(delta),
            "command": probe_command,
        })
    return probes


def estimate_jacobian(
    base_white_point: Mapping[str, Any],
    probe_samples: Sequence[Mapping[str, Any]],
    *,
    target_white_point: Mapping[str, Any],
    active_channel: str,
    cct_tolerance_K: float,
    duv_tolerance: float,
    max_code: int,
    channels: Sequence[str] = DEFAULT_CHANNELS,
) -> np.ndarray:
    free = free_channels(channels, active_channel)
    base_error = np.asarray(
        white_point_metrics(
            base_white_point,
            target_white_point,
            cct_tolerance_K=cct_tolerance_K,
            duv_tolerance=duv_tolerance,
        )["normalized_error"],
        dtype="float64",
    )
    jacobian = np.zeros((2, len(free)), dtype="float64")
    by_channel = {str(sample["probe_channel"]): sample for sample in probe_samples}
    for index, channel in enumerate(free):
        sample = by_channel.get(channel)
        if sample is None:
            continue
        delta_weight = float(sample["probe_delta_code"]) / float(max_code)
        if abs(delta_weight) < 1e-12:
            continue
        probe_error = np.asarray(
            white_point_metrics(
                sample["white_point"],
                target_white_point,
                cct_tolerance_K=cct_tolerance_K,
                duv_tolerance=duv_tolerance,
            )["normalized_error"],
            dtype="float64",
        )
        jacobian[:, index] = (probe_error - base_error) / delta_weight
    return jacobian


def _solve_box_constrained_least_squares(
    matrix: Any,
    target: Any,
    lower_bounds: Any,
    upper_bounds: Any,
) -> np.ndarray:
    """Solve a small bounded least-squares problem by enumerating active bounds."""
    coefficients = np.asarray(matrix, dtype="float64")
    desired = np.asarray(target, dtype="float64")
    lower = np.asarray(lower_bounds, dtype="float64")
    upper = np.asarray(upper_bounds, dtype="float64")
    if coefficients.ndim != 2:
        raise ValueError("least-squares matrix must be two-dimensional")
    variable_count = coefficients.shape[1]
    if desired.shape != (coefficients.shape[0],):
        raise ValueError("least-squares target shape does not match the matrix")
    if lower.shape != (variable_count,) or upper.shape != (variable_count,):
        raise ValueError("least-squares bounds shape does not match the matrix")
    if np.any(lower > upper):
        raise ValueError("least-squares lower bounds must not exceed upper bounds")

    best: np.ndarray | None = None
    best_objective = float("inf")
    tolerance = 1e-12
    # There are only four free RGBWW channels, so all 3^4 active sets are cheap.
    for states in product((-1, 0, 1), repeat=variable_count):
        candidate = np.zeros(variable_count, dtype="float64")
        fixed_indices = [index for index, state in enumerate(states) if state != 0]
        free_indices = [index for index, state in enumerate(states) if state == 0]
        for index in fixed_indices:
            candidate[index] = lower[index] if states[index] < 0 else upper[index]

        adjusted_target = desired
        if fixed_indices:
            adjusted_target = desired - coefficients[:, fixed_indices] @ candidate[fixed_indices]
        if free_indices:
            free_solution = np.linalg.lstsq(
                coefficients[:, free_indices],
                adjusted_target,
                rcond=None,
            )[0]
            free_lower = lower[free_indices]
            free_upper = upper[free_indices]
            if np.any(free_solution < free_lower - tolerance) or np.any(
                free_solution > free_upper + tolerance
            ):
                continue
            candidate[free_indices] = np.clip(free_solution, free_lower, free_upper)

        residual = coefficients @ candidate - desired
        objective = float(residual @ residual)
        if objective < best_objective:
            best = candidate
            best_objective = objective

    if best is None:
        raise RuntimeError("bounded least-squares solver did not find a feasible solution")
    return best


def solve_damped_step(
    command: Mapping[str, int],
    white_point: Mapping[str, Any],
    target_white_point: Mapping[str, Any],
    jacobian: Any,
    *,
    active_channel: str,
    cct_tolerance_K: float,
    duv_tolerance: float,
    max_code: int,
    max_step_code: int,
    damping: float,
    rgb_penalty: float,
    channel_penalties: Mapping[str, float] | None = None,
    channels: Sequence[str] = DEFAULT_CHANNELS,
) -> dict[str, Any]:
    if max_step_code <= 0:
        raise ValueError("max_step_code must be positive")
    if damping <= 0:
        raise ValueError("damping must be positive")
    free = free_channels(channels, active_channel)
    matrix = np.asarray(jacobian, dtype="float64")
    if matrix.shape != (2, len(free)):
        raise ValueError(f"jacobian shape must be (2, {len(free)})")
    residual = np.asarray(
        white_point_metrics(
            white_point,
            target_white_point,
            cct_tolerance_K=cct_tolerance_K,
            duv_tolerance=duv_tolerance,
        )["normalized_error"],
        dtype="float64",
    )
    resolved_penalties = resolve_channel_penalties(
        rgb_penalty=rgb_penalty,
        channel_penalties=channel_penalties,
    )
    regularization = np.asarray([
        1.0 + 4.0 * resolved_penalties[channel]
        if channel in {"r", "g", "b"}
        else 1.0
        for channel in free
    ], dtype="float64")
    max_step_weight = float(max_step_code) / float(max_code)
    current_weights = np.asarray(
        [float(command[channel]) / float(max_code) for channel in free],
        dtype="float64",
    )
    lower_bounds = np.maximum(-max_step_weight, -current_weights)
    upper_bounds = np.minimum(max_step_weight, 1.0 - current_weights)
    augmented_matrix = np.vstack((
        matrix,
        np.sqrt(float(damping)) * np.diag(regularization),
    ))
    augmented_target = np.concatenate((-residual, np.zeros(len(free), dtype="float64")))
    delta_weight = _solve_box_constrained_least_squares(
        augmented_matrix,
        augmented_target,
        lower_bounds,
        upper_bounds,
    )

    next_command = {channel: min(max(int(command[channel]), 0), int(max_code)) for channel in channels}
    actual_delta_weight = np.zeros(len(free), dtype="float64")
    delta_codes: dict[str, int] = {}
    for index, channel in enumerate(free):
        proposed = int(round(float(command[channel]) + float(delta_weight[index]) * float(max_code)))
        bounded = min(max(proposed, 0), int(max_code))
        next_command[channel] = bounded
        delta_codes[channel] = bounded - int(command[channel])
        actual_delta_weight[index] = float(delta_codes[channel]) / float(max_code)
    next_command[active_channel] = int(max_code)
    predicted_error = residual + matrix @ actual_delta_weight
    return {
        "command": next_command,
        "delta_codes": delta_codes,
        "delta_weights": actual_delta_weight.tolist(),
        "predicted_normalized_error": predicted_error.tolist(),
        "free_channels": list(free),
    }


def broyden_update(
    jacobian: Any,
    previous_command: Mapping[str, int],
    next_command: Mapping[str, int],
    previous_white_point: Mapping[str, Any],
    next_white_point: Mapping[str, Any],
    target_white_point: Mapping[str, Any],
    *,
    active_channel: str,
    cct_tolerance_K: float,
    duv_tolerance: float,
    max_code: int,
    channels: Sequence[str] = DEFAULT_CHANNELS,
) -> np.ndarray:
    free = free_channels(channels, active_channel)
    matrix = np.asarray(jacobian, dtype="float64")
    delta_weight = np.asarray(
        [(float(next_command[channel]) - float(previous_command[channel])) / float(max_code) for channel in free],
        dtype="float64",
    )
    denominator = float(delta_weight @ delta_weight)
    if denominator < 1e-12:
        return matrix.copy()
    previous_error = np.asarray(
        white_point_metrics(
            previous_white_point,
            target_white_point,
            cct_tolerance_K=cct_tolerance_K,
            duv_tolerance=duv_tolerance,
        )["normalized_error"],
        dtype="float64",
    )
    next_error = np.asarray(
        white_point_metrics(
            next_white_point,
            target_white_point,
            cct_tolerance_K=cct_tolerance_K,
            duv_tolerance=duv_tolerance,
        )["normalized_error"],
        dtype="float64",
    )
    correction = next_error - previous_error - matrix @ delta_weight
    return matrix + np.outer(correction, delta_weight) / denominator


def sample_sort_key(sample: Mapping[str, Any]) -> tuple[float, float, float]:
    comparison = sample["white_point_comparison"]
    vector_comparison = sample.get("comparison_to_ray_weighted", {})
    return (
        float(comparison["goal_score"]),
        float(vector_comparison.get("relative_rmse", float("inf"))),
        float(comparison["absolute_cct_error_K"]),
    )


def build_bracketed_cct_step(
    samples: Sequence[Mapping[str, Any]],
    current_command: Mapping[str, int],
    *,
    active_channel: str,
    max_code: int,
    channels: Sequence[str] = DEFAULT_CHANNELS,
) -> dict[str, Any] | None:
    """Interpolate between measured commands that straddle the target CCT."""
    if max_code <= 0:
        raise ValueError("max_code must be positive")
    free = free_channels(channels, active_channel)
    sampled_commands = {
        tuple(int(sample["command"][channel]) for channel in channels)
        for sample in samples
    }
    best_observed_score = min(
        float(sample["white_point_comparison"]["goal_score"])
        for sample in samples
    )
    candidates: list[tuple[float, int, dict[str, Any]]] = []
    for left_index, left in enumerate(samples):
        left_error = np.asarray(
            left["white_point_comparison"]["normalized_error"],
            dtype="float64",
        )
        for right_index in range(left_index + 1, len(samples)):
            right = samples[right_index]
            right_error = np.asarray(
                right["white_point_comparison"]["normalized_error"],
                dtype="float64",
            )
            if float(left_error[0]) * float(right_error[0]) >= 0:
                continue
            alpha = -float(left_error[0]) / float(right_error[0] - left_error[0])
            if not 0.0 < alpha < 1.0:
                continue
            predicted_error = left_error + alpha * (right_error - left_error)
            predicted_score = float(np.max(np.abs(predicted_error)))
            if abs(float(predicted_error[1])) >= 1.0 or predicted_score >= best_observed_score:
                continue

            command = {
                channel: min(
                    max(
                        int(
                            round(
                                float(left["command"][channel])
                                + alpha
                                * (
                                    float(right["command"][channel])
                                    - float(left["command"][channel])
                                )
                            )
                        ),
                        0,
                    ),
                    int(max_code),
                )
                for channel in channels
            }
            command[active_channel] = int(max_code)
            command_key = tuple(command[channel] for channel in channels)
            if command_key in sampled_commands:
                continue

            delta_codes = {
                channel: int(command[channel]) - int(current_command[channel])
                for channel in free
            }
            movement = sum(abs(value) for value in delta_codes.values())
            candidates.append(
                (
                    predicted_score,
                    movement,
                    {
                        "kind": "bracketed_cct_secant",
                        "command": command,
                        "delta_codes": delta_codes,
                        "delta_weights": [
                            float(delta_codes[channel]) / float(max_code)
                            for channel in free
                        ],
                        "predicted_normalized_error": predicted_error.tolist(),
                        "predicted_goal_score": predicted_score,
                        "free_channels": list(free),
                        "source_sample_indices": [int(left["index"]), int(right["index"])],
                        "interpolation_fraction": alpha,
                    },
                )
            )
    if not candidates:
        return None
    return min(candidates, key=lambda item: (item[0], item[1]))[2]


def bracketed_cct_prediction_missed(
    step: Mapping[str, Any],
    sample: Mapping[str, Any],
) -> bool:
    """Return whether a secant prediction was materially invalidated by measurement."""
    if step.get("kind") != "bracketed_cct_secant":
        return False
    predicted_score = float(step["predicted_goal_score"])
    actual_score = float(sample["white_point_comparison"]["goal_score"])
    return (
        actual_score >= 1.0
        and actual_score > predicted_score * SECANT_MISS_SCORE_RATIO
        and actual_score - predicted_score > SECANT_MISS_SCORE_SLACK
    )


def run_feedback_optimization(
    *,
    target: dict[str, int],
    target_vector: Any,
    target_white_point: dict[str, Any],
    initial_solution: dict[str, Any],
    rgb_penalty: float,
    channel_penalties: Mapping[str, float] | None = None,
    regions: Sequence[dict[str, Any]],
    camera_dir: Path,
    decode_dir: Path,
    scratch_dir: Path,
    initial_shutter_speed: str,
    iso: str,
    aperture: str,
    image_format: str,
    min_shutter_speed: str,
    max_shutter_speed: str,
    max_trials: int,
    max_captures: int,
    decode_formats: Sequence[str],
    metering_regions: Sequence[dict[str, Any]] | None,
    settle_seconds: float,
    target_max: int,
    low_signal_ratio: float,
    high_signal_ratio: float,
    max_code: int,
    feedback_rounds: int,
    feedback_probe_step: int,
    feedback_max_step: int,
    feedback_damping: float,
    feedback_cct_tolerance_K: float,
    feedback_duv_tolerance: float,
    light_fn: LightFn,
    auto_expose_fn: AutoExposeFn,
    capture_fn: CaptureFn,
    decoder_fn: DecoderFn,
    white_point_estimator_fn: WhitePointEstimatorFn,
    feedback_confirmations: int = 2,
    feedback_confirmation_settle_seconds: float = 60.0,
    feedback_confirmation_off_seconds: float = 1.0,
    feedback_thermal_rebases: int = 2,
    progress_fn: Callable[[dict[str, Any]], None] | None = None,
) -> dict[str, Any]:
    if feedback_confirmations < 1:
        raise ValueError("feedback_confirmations must be at least 1")
    if feedback_confirmation_settle_seconds < 0:
        raise ValueError("feedback_confirmation_settle_seconds must be non-negative")
    if feedback_confirmation_off_seconds < 0:
        raise ValueError("feedback_confirmation_off_seconds must be non-negative")
    if feedback_thermal_rebases < 0:
        raise ValueError("feedback_thermal_rebases must be non-negative")
    samples: list[dict[str, Any]] = []
    confirmation_attempts: list[dict[str, Any]] = []
    thermal_rebases: list[dict[str, Any]] = []
    confirmed_best: dict[str, Any] | None = None
    active_channel = str(initial_solution["active_channel"])
    initial_command = {channel: int(initial_solution["command"][channel]) for channel in common.DEFAULT_CHANNELS}
    resolved_channel_penalties = resolve_channel_penalties(
        rgb_penalty=rgb_penalty,
        channel_penalties=channel_penalties,
    )
    restart = initial_solution.get("feedback_restart", {})
    attempt_index = int(restart.get("attempt", 0))
    current_max_step = int(feedback_max_step)
    current_shutter_speed = str(initial_shutter_speed)
    jacobian = None
    initial_jacobian = None
    rounds_completed = 0
    consecutive_secant_prediction_misses = 0
    stop_reason = "feedback_disabled" if feedback_rounds == 0 else "round_limit"

    def progress(status: str) -> None:
        if progress_fn is None:
            return
        best = min(samples, key=sample_sort_key) if samples else None
        progress_fn({
            "kind": "constrained_white_point_jacobian_broyden",
            "status": status,
            "active_channel": active_channel,
            "initial_command": initial_command,
            "channel_penalties": resolved_channel_penalties,
            "goal_confirmed": confirmed_best is not None,
            "confirmation_attempts": confirmation_attempts,
            "thermal_rebases": thermal_rebases,
            "best": best,
            "samples": samples,
        })

    def capture_sample(
        command: dict[str, int],
        *,
        phase: str,
        round_index: int | None = None,
        probe_channel: str | None = None,
        probe_delta_code: int | None = None,
        confirmation_of_sample_index: int | None = None,
        settle_seconds_override: float | None = None,
        step: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        nonlocal current_shutter_speed
        sample_index = len(samples)
        bounded_command = {
            channel: min(max(int(command[channel]), 0), int(max_code))
            for channel in common.DEFAULT_CHANNELS
        }
        bounded_command[active_channel] = int(max_code)
        payload = light_fn(
            bounded_command["cw"],
            bounded_command["ww"],
            bounded_command["r"],
            bounded_command["g"],
            bounded_command["b"],
        )
        active_settle_seconds = settle_seconds if settle_seconds_override is None else settle_seconds_override
        time.sleep(max(0.0, active_settle_seconds))
        filename_template = (
            f"target-rgbww-{target['index']:02d}-{target['cct']}K-gm{target['gm']}-"
            f"attempt{attempt_index:02d}-{sample_index:02d}-{phase}.%C"
        )
        auto_exposure = None
        if sample_index == 0:
            auto_exposure = common.capture_auto_exposed(
                auto_expose_fn=auto_expose_fn,
                camera_dir=camera_dir,
                decode_dir=decode_dir,
                scratch_dir=scratch_dir,
                filename_template=filename_template,
                target_max=target_max,
                iso=iso,
                aperture=aperture,
                image_format=image_format,
                min_shutter_speed=min_shutter_speed,
                max_shutter_speed=max_shutter_speed,
                max_trials=max_trials,
                max_captures=max_captures,
                decode_formats=decode_formats,
                metering_regions=metering_regions,
                initial_shutter_speed=current_shutter_speed,
            )
            rgbww_capture = auto_exposure.final_capture
            current_shutter_speed = rgbww_capture.settings.shutter_speed
        else:
            rgbww_capture = common.capture_fixed(
                capture_fn=capture_fn,
                decoder_fn=decoder_fn,
                camera_dir=camera_dir,
                decode_dir=decode_dir,
                filename_template=filename_template,
                iso=iso,
                aperture=aperture,
                image_format=image_format,
                shutter_speed=current_shutter_speed,
                decode_formats=decode_formats,
                metering_regions=metering_regions,
            )
        try:
            capture_json = rgbww_capture.to_jsonable()
            auto_exposure_json = auto_exposure.to_jsonable() if auto_exposure is not None else None
            rgbww_seconds, rgbww_vector, rgbww_regions = common.measure_capture_regions(rgbww_capture, regions)
            measured_comparison = common.compare_vectors(
                common.weighted_vector(rgbww_vector, regions),
                common.weighted_vector(target_vector, regions),
            )
            white_point = white_point_estimator_fn(rgbww_capture, regions)
            white_point_comparison = white_point_metrics(
                white_point,
                target_white_point,
                cct_tolerance_K=feedback_cct_tolerance_K,
                duv_tolerance=feedback_duv_tolerance,
            )
            exposure_warning = common.exposure_warning(
                rgbww_capture,
                target_max=target_max,
                low_signal_ratio=low_signal_ratio,
                high_signal_ratio=high_signal_ratio,
            )
        finally:
            removed_npy_files = common.remove_capture_npy_outputs(rgbww_capture)
        sample = {
            "index": sample_index,
            "phase": phase,
            "round": round_index,
            "command": bounded_command,
            "max_channel_value": max(bounded_command.values()),
            "payload": payload,
            "capture": capture_json,
            "auto_exposure": auto_exposure_json,
            "removed_npy_files": [str(path) for path in removed_npy_files],
            "shutter_seconds": rgbww_seconds,
            "vector_norm": common.vector_norm(rgbww_vector),
            "comparison_to_ray_weighted": measured_comparison,
            "white_point": white_point,
            "white_point_comparison": white_point_comparison,
            "exposure_warning": exposure_warning,
            "regions": rgbww_regions,
        }
        if probe_channel is not None:
            sample["probe_channel"] = probe_channel
            sample["probe_delta_code"] = int(probe_delta_code or 0)
        if confirmation_of_sample_index is not None:
            sample["confirmation_of_sample_index"] = int(confirmation_of_sample_index)
        if step is not None:
            sample["step"] = step
        samples.append(sample)
        print(
            f"  feedback {sample_index}: {phase} "
            f"cct_error={white_point_comparison['cct_error_K']:.2f}K "
            f"duv_error={white_point_comparison['duv_error']:.6f} "
            f"goal={white_point_comparison['goal_score']:.3f}"
        )
        if exposure_warning:
            print(f"  exposure warning: {exposure_warning['kind']}")
        progress("sampling")
        return sample

    def confirm_candidate(candidate: dict[str, Any]) -> tuple[bool, dict[str, Any]]:
        nonlocal confirmed_best
        attempt_index = len(confirmation_attempts)
        attempt = {
            "index": attempt_index,
            "candidate_sample_index": int(candidate["index"]),
            "command": dict(candidate["command"]),
            "required": int(feedback_confirmations),
            "sample_indices": [],
            "status": "running",
        }
        confirmation_attempts.append(attempt)
        confirmations = []
        for confirmation_index in range(feedback_confirmations):
            light_fn(0, 0, 0, 0, 0)
            time.sleep(feedback_confirmation_off_seconds)
            confirmation = capture_sample(
                candidate["command"],
                phase=f"confirm-{attempt_index}-{confirmation_index}",
                confirmation_of_sample_index=int(candidate["index"]),
                settle_seconds_override=feedback_confirmation_settle_seconds,
            )
            confirmations.append(confirmation)
            attempt["sample_indices"].append(int(confirmation["index"]))
            if not confirmation["white_point_comparison"]["within_goal"]:
                attempt["status"] = "failed"
                attempt["failed_sample_index"] = int(confirmation["index"])
                progress("confirmation_failed")
                return False, confirmation

        attempt["status"] = "confirmed"
        confirmed_best = max(confirmations, key=sample_sort_key)
        attempt["confirmed_sample_index"] = int(confirmed_best["index"])
        progress("goal_confirmed")
        return True, confirmed_best

    def capture_probe_set(base: dict[str, Any], *, phase_prefix: str) -> list[dict[str, Any]]:
        probe_samples = []
        for probe in build_probe_commands(
            base["command"],
            active_channel=active_channel,
            probe_step_code=feedback_probe_step,
            max_code=max_code,
            channels=common.DEFAULT_CHANNELS,
        ):
            sample = capture_sample(
                probe["command"],
                phase=f"{phase_prefix}-{probe['channel']}",
                probe_channel=str(probe["channel"]),
                probe_delta_code=int(probe["delta_code"]),
            )
            probe_samples.append(sample)
        return probe_samples

    def estimate_probe_jacobian(base: dict[str, Any], probes: list[dict[str, Any]]) -> Any:
        return estimate_jacobian(
            base["white_point"],
            probes,
            target_white_point=target_white_point,
            active_channel=active_channel,
            cct_tolerance_K=feedback_cct_tolerance_K,
            duv_tolerance=feedback_duv_tolerance,
            max_code=max_code,
            channels=common.DEFAULT_CHANNELS,
        )

    def thermal_rebase(
        base: dict[str, Any],
        *,
        reason: str,
    ) -> tuple[Any, list[dict[str, Any]]] | None:
        nonlocal current_max_step
        if len(thermal_rebases) >= feedback_thermal_rebases:
            return None
        rebase_index = len(thermal_rebases)
        probes = capture_probe_set(base, phase_prefix=f"thermal-rebase-{rebase_index}-probe")
        rebased_jacobian = estimate_probe_jacobian(base, probes)
        record = {
            "index": rebase_index,
            "reason": reason,
            "base_sample_index": int(base["index"]),
            "probe_sample_indices": [int(sample["index"]) for sample in probes],
        }
        thermal_rebases.append(record)
        current_max_step = int(feedback_max_step)
        progress("thermal_rebased")
        return rebased_jacobian, [base, *probes]

    initial = capture_sample(initial_command, phase="initial")
    current = initial
    if initial["white_point_comparison"]["within_goal"]:
        confirmed, current = confirm_candidate(initial)
        if confirmed:
            stop_reason = "goal_confirmed"

    if feedback_rounds > 0 and confirmed_best is None:
        probe_base = current if current["command"] == initial["command"] else initial
        probe_samples = capture_probe_set(probe_base, phase_prefix="probe")
        jacobian = estimate_probe_jacobian(probe_base, probe_samples)
        initial_jacobian = jacobian.copy()
        step_samples = [probe_base, *probe_samples]
        observed_best = min(step_samples, key=sample_sort_key)
        if observed_best["white_point_comparison"]["within_goal"]:
            confirmed, current = confirm_candidate(observed_best)
            if confirmed:
                stop_reason = "goal_confirmed"
            else:
                rebased = thermal_rebase(current, reason="confirmation_failed")
                if rebased is not None:
                    jacobian, step_samples = rebased

        if confirmed_best is None:
            for round_index in range(feedback_rounds):
                step = build_bracketed_cct_step(
                    step_samples,
                    current["command"],
                    active_channel=active_channel,
                    max_code=max_code,
                    channels=common.DEFAULT_CHANNELS,
                )
                if step is None:
                    step = solve_damped_step(
                        current["command"],
                        current["white_point"],
                        target_white_point,
                        jacobian,
                        active_channel=active_channel,
                        cct_tolerance_K=feedback_cct_tolerance_K,
                        duv_tolerance=feedback_duv_tolerance,
                        max_code=max_code,
                        max_step_code=current_max_step,
                        damping=feedback_damping,
                        rgb_penalty=rgb_penalty,
                        channel_penalties=resolved_channel_penalties,
                        channels=common.DEFAULT_CHANNELS,
                    )
                if step["command"] == current["command"]:
                    stop_reason = "no_new_command"
                    break
                phase = f"feedback-{round_index}"
                if step.get("kind") == "bracketed_cct_secant":
                    phase += "-secant-cct"
                candidate = capture_sample(
                    step["command"],
                    phase=phase,
                    round_index=round_index,
                    step=step,
                )
                rounds_completed += 1
                step_samples.append(candidate)
                jacobian = broyden_update(
                    jacobian,
                    current["command"],
                    candidate["command"],
                    current["white_point"],
                    candidate["white_point"],
                    target_white_point,
                    active_channel=active_channel,
                    cct_tolerance_K=feedback_cct_tolerance_K,
                    duv_tolerance=feedback_duv_tolerance,
                    max_code=max_code,
                    channels=common.DEFAULT_CHANNELS,
                )
                if sample_sort_key(candidate) >= sample_sort_key(current):
                    current_max_step = max(int(feedback_probe_step), current_max_step // 2)
                current = candidate
                if bracketed_cct_prediction_missed(step, candidate):
                    consecutive_secant_prediction_misses += 1
                else:
                    consecutive_secant_prediction_misses = 0
                if (
                    consecutive_secant_prediction_misses
                    >= SECANT_MISSES_BEFORE_THERMAL_REBASE
                ):
                    rebased = thermal_rebase(
                        current,
                        reason="repeated_secant_prediction_miss",
                    )
                    consecutive_secant_prediction_misses = 0
                    if rebased is not None:
                        jacobian, step_samples = rebased
                        continue
                if candidate["white_point_comparison"]["within_goal"]:
                    confirmed, current = confirm_candidate(candidate)
                    if confirmed:
                        stop_reason = "goal_confirmed"
                        break
                    rebased = thermal_rebase(current, reason="confirmation_failed")
                    if rebased is not None:
                        jacobian, step_samples = rebased
                        consecutive_secant_prediction_misses = 0
                    else:
                        step_samples.append(current)

    observed_best = min(samples, key=sample_sort_key)
    best = confirmed_best or observed_best
    if confirmed_best is None and observed_best["white_point_comparison"]["within_goal"]:
        if stop_reason == "feedback_disabled":
            stop_reason = "goal_confirmation_failed"
    result = {
        "kind": "constrained_white_point_jacobian_broyden",
        "status": stop_reason,
        "active_channel": active_channel,
        "attempt": attempt_index,
        "initial_command": initial_command,
        "initial_shutter_speed": str(initial_shutter_speed),
        "final_shutter_speed": current_shutter_speed,
        "channel_penalties": resolved_channel_penalties,
        "selected_command": best["command"],
        "rounds_requested": int(feedback_rounds),
        "rounds_completed": int(rounds_completed),
        "probe_step_code": int(feedback_probe_step),
        "final_max_step_code": int(current_max_step),
        "damping": float(feedback_damping),
        "cct_tolerance_K": float(feedback_cct_tolerance_K),
        "duv_tolerance": float(feedback_duv_tolerance),
        "confirmations_requested": int(feedback_confirmations),
        "confirmation_settle_seconds": float(feedback_confirmation_settle_seconds),
        "confirmation_off_seconds": float(feedback_confirmation_off_seconds),
        "thermal_rebases_requested": int(feedback_thermal_rebases),
        "goal_confirmed": confirmed_best is not None,
        "confirmation_attempts": confirmation_attempts,
        "thermal_rebases": thermal_rebases,
        "initial_jacobian": initial_jacobian.tolist() if initial_jacobian is not None else None,
        "final_jacobian": jacobian.tolist() if jacobian is not None else None,
        "best": best,
        "samples": samples,
    }
    if progress_fn is not None:
        progress_fn(result)
    return result
