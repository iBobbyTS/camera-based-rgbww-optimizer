from __future__ import annotations

import argparse
import itertools
import json
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Sequence

from camera_based_rgbww_optimizer.control import camera_gphoto2, camera_remote, esphome, ray120c
from camera_based_rgbww_optimizer.control import white_lut as white_lut_control
from camera_based_rgbww_optimizer.optimization import measure_channel_response
from camera_based_rgbww_optimizer.optimization.bounded_least_squares import (
    solve_box_constrained_least_squares,
)
from camera_based_rgbww_optimizer.optimization import white_calibration_common as common
from camera_based_rgbww_optimizer.optimization import white_lut_feedback as feedback
from camera_based_rgbww_optimizer.optimization import white_lut_policy as policy
from camera_based_rgbww_optimizer.paths import PROJECT_ROOT, PROJECT_TMP_DIR
from camera_based_rgbww_optimizer.utils import location_regions


DEFAULT_OUTPUT_ROOT = PROJECT_TMP_DIR / "white-lut-calibration"
DEFAULT_LOCATION_CONFIG = PROJECT_ROOT / "config" / "location" / "locations-20260714-211759.json"
DEFAULT_CHANNEL_RESPONSE = PROJECT_TMP_DIR / "channel-response" / "merged" / "channel-code-duty-response-merged.json"
DEFAULT_ENDPOINT_CALIBRATION = PROJECT_ROOT / "config" / "white" / "white-endpoints.json"
DEFAULT_TARGET_CCTS = (1800, 3200, 5600, 20000)
DEFAULT_TARGET_GM_VALUES = (0, 100, 200)
DEFAULT_INSIDE_RGB_PENALTY = 0.45
DEFAULT_OUTSIDE_RGB_PENALTY = 0.06
DEFAULT_ENDPOINT_RGB_PENALTY = 0.02
DEFAULT_MAX_CODE = 4095
DEFAULT_SAFE_CODE_LIMIT = 1024
DEFAULT_SETTLE_SECONDS = 1.0
DEFAULT_COARSE_LEVELS = (0.0, 0.25, 0.5, 0.75, 1.0)
DEFAULT_REFINEMENT_STEPS = (0.125, 0.0625, 0.03125, 0.015625)
DEFAULT_LOW_SIGNAL_RATIO = 0.1
DEFAULT_HIGH_SIGNAL_RATIO = 1.0
DEFAULT_RAY_INTENSITY_PERCENT = 100.0
DEFAULT_FEEDBACK_ROUNDS = 16
DEFAULT_FEEDBACK_PROBE_STEP = 256
DEFAULT_FEEDBACK_MAX_STEP = 768
DEFAULT_FEEDBACK_DAMPING = 0.05
DEFAULT_FEEDBACK_CONFIRMATIONS = 2
DEFAULT_FEEDBACK_CONFIRMATION_SETTLE_SECONDS = 60.0
DEFAULT_FEEDBACK_CONFIRMATION_OFF_SECONDS = 1.0
DEFAULT_FEEDBACK_THERMAL_REBASES = 2
DEFAULT_FEEDBACK_CCT_TOLERANCE_K = 25.0
DEFAULT_FEEDBACK_CCT_TOLERANCE_MIRED = 1.0
DEFAULT_FEEDBACK_DUV_TOLERANCE = 0.0005
DEFAULT_INITIAL_LUT_LOCAL_SCORE_LIMIT = 4.0

LightFn = Callable[..., dict[str, int]]
RaySetCctFn = Callable[..., dict[str, Any]]
AutoExposeFn = Callable[..., camera_gphoto2.AutoExposureResult]
CaptureFn = Callable[..., camera_gphoto2.CaptureResult]
DecoderFn = Callable[..., camera_gphoto2.DecodeResult]
WhitePointEstimatorFn = Callable[[camera_gphoto2.CaptureResult, Sequence[dict[str, Any]]], dict[str, Any]]


def seed_solution_from_lut(
    solution: dict[str, Any],
    lut_data: dict[str, Any],
    *,
    cct: int,
    gm: int,
    max_code: int,
) -> dict[str, Any]:
    interpolation = white_lut_control.interpolate_white_lut(lut_data, cct, gm)
    command = {channel: int(interpolation["command"][channel]) for channel in common.DEFAULT_CHANNELS}
    active_channels = [channel for channel in common.DEFAULT_CHANNELS if command[channel] == int(max_code)]
    if not active_channels:
        raise ValueError(f"initial LUT seed {cct}K/gm{gm} has no channel at max_code={max_code}")
    model_active = str(solution["active_channel"])
    active_channel = model_active if model_active in active_channels else active_channels[0]
    prior_target = next(
        (
            target
            for target in lut_data.get("targets", [])
            if int(target.get("cct", -1)) == int(cct) and int(target.get("gm", -1)) == int(gm)
        ),
        None,
    )
    prior_comparison = None
    if isinstance(prior_target, dict):
        prior_comparison = prior_target.get("feedback_optimizer", {}).get("best", {}).get("white_point_comparison")
    return {
        **solution,
        "model_command": dict(solution["command"]),
        "model_active_channel": model_active,
        "command": command,
        "active_channel": active_channel,
        "initial_lut_seed": {
            "requested": interpolation["requested"],
            "bracket": interpolation["bracket"],
            "prior_white_point_comparison": prior_comparison,
        },
    }


def feedback_restart_solutions(solution: dict[str, Any], *, max_code: int) -> list[dict[str, Any]]:
    candidates = [{
        "active_channel": str(solution["active_channel"]),
        "command": dict(solution["command"]),
        "source": "primary",
    }]
    candidates.extend(solution.get("alternative_initial_solutions", []))
    for channel in (solution.get("endpoint_bias"), solution.get("model_active_channel")):
        if channel in common.DEFAULT_CHANNELS:
            command = dict(solution["command"])
            command[str(channel)] = int(max_code)
            candidates.append({
                "active_channel": str(channel),
                "command": command,
                "source": "active_channel_restart",
            })

    attempts = []
    seen = set()
    for candidate in candidates:
        active_channel = str(candidate["active_channel"])
        command = {channel: int(candidate["command"][channel]) for channel in common.DEFAULT_CHANNELS}
        command[active_channel] = int(max_code)
        key = (active_channel, *(command[channel] for channel in common.DEFAULT_CHANNELS))
        if key in seen:
            continue
        seen.add(key)
        attempt_index = len(attempts)
        attempts.append({
            **solution,
            "command": command,
            "active_channel": active_channel,
            "feedback_restart": {
                "attempt": attempt_index,
                "active_channel": active_channel,
                "source": str(candidate.get("source", "unknown")),
            },
        })
    return attempts


def feedback_attempt_sort_key(attempt: dict[str, Any]) -> tuple[float, ...]:
    return (
        0.0 if attempt["goal_confirmed"] else 1.0,
        *feedback.sample_sort_key(attempt["best"]),
    )


def solve_white_point_mix(
    basis_vectors: dict[str, Any],
    target_white_point: dict[str, Any],
    *,
    regions: Sequence[dict[str, Any]],
    max_code: int,
    channels: Sequence[str] = common.DEFAULT_CHANNELS,
) -> dict[str, Any]:
    np = common.import_numpy()
    white_region = common.select_white_point_region(regions)
    white_index = next(index for index, region in enumerate(regions) if region["name"] == white_region["name"])
    white_slice = slice(white_index * 3, white_index * 3 + 3)
    matrix = np.column_stack([np.asarray(basis_vectors[channel][white_slice], dtype="float64") for channel in channels])
    matrix_scale = float(np.max(matrix))
    if matrix_scale <= 0:
        raise ValueError("white-point channel basis has no measurable signal")
    normalized_matrix = matrix / matrix_scale
    target = np.asarray(target_white_point["camera_neutral_g1"], dtype="float64")[:3]
    target_norm = float(np.linalg.norm(target))
    if target_norm <= 0:
        raise ValueError("target white point has no measurable camera neutral")
    target_direction = target / target_norm

    candidates = []
    for active_index, active_channel in enumerate(channels):
        free_indices = [index for index in range(len(channels)) if index != active_index]
        coefficients = np.column_stack((normalized_matrix[:, free_indices], -target_direction))
        desired = -normalized_matrix[:, active_index]
        solution = solve_box_constrained_least_squares(
            coefficients,
            desired,
            np.asarray([0.0] * len(free_indices) + [0.0]),
            np.asarray([1.0] * len(free_indices) + [10.0]),
        )
        weights = np.zeros(len(channels), dtype="float64")
        weights[active_index] = 1.0
        weights[free_indices] = solution[: len(free_indices)]
        predicted_rgb = matrix @ weights
        predicted_direction = predicted_rgb / np.linalg.norm(predicted_rgb)
        direction_residual = float(np.linalg.norm(predicted_direction - target_direction))
        if float(predicted_rgb[1]) <= 0:
            continue
        predicted_neutral = predicted_rgb / float(predicted_rgb[1])
        predicted_white_point = common.estimate_white_point_from_camera_neutral(
            predicted_neutral,
            target_white_point["rawpy_rgb_xyz_matrix_first3"],
            np_module=np,
        )
        candidates.append({
            "active_channel": str(active_channel),
            "weights": {channel: float(weights[index]) for index, channel in enumerate(channels)},
            "command": {
                channel: int(round(float(weights[index]) * float(max_code)))
                for index, channel in enumerate(channels)
            },
            "camera_rgb_direction_residual": direction_residual,
            "predicted_white_point": predicted_white_point,
        })
    best = min(candidates, key=lambda candidate: candidate["camera_rgb_direction_residual"])
    best["command"][best["active_channel"]] = int(max_code)
    return {"kind": "white_patch_linear_camera_rgb_cone", "best": best, "candidates": candidates}


def load_endpoint_calibration(path: Path) -> dict[str, Any]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if data.get("measurement", {}).get("kind") != "camera_based_rgbww_optimizer_white_endpoint_ray_match":
        raise ValueError(f"unsupported endpoint calibration kind in {path}")
    matches = data.get("ray_endpoint_matches", {})
    if "cw" not in matches or "ww" not in matches:
        raise ValueError(f"endpoint calibration must contain cw and ww matches: {path}")
    white_range = data.get("white_range")
    if not isinstance(white_range, dict):
        raise ValueError(f"endpoint calibration must contain white_range: {path}")
    return data


def solve_high_output_mix(
    basis_vectors: dict[str, Any],
    target_vector: Any,
    *,
    regions: Sequence[dict[str, Any]],
    rgb_penalty: float,
    channel_penalties: dict[str, float] | None = None,
    endpoint_bias: str | None,
    channels: Sequence[str] = common.DEFAULT_CHANNELS,
    max_code: int = DEFAULT_MAX_CODE,
    coarse_levels: Sequence[float] = DEFAULT_COARSE_LEVELS,
    refinement_steps: Sequence[float] = DEFAULT_REFINEMENT_STEPS,
) -> dict[str, Any]:
    np = common.import_numpy()
    matrix = np.column_stack([common.weighted_vector(basis_vectors[channel], regions) for channel in channels])
    target = common.weighted_vector(target_vector, regions)
    if target.size != matrix.shape[0]:
        raise ValueError(f"target vector length {target.size} does not match basis length {matrix.shape[0]}")
    if common.vector_norm(target) <= 0:
        raise ValueError("target vector has no measurable signal")

    best_weights: Any | None = None
    best_score: float | None = None
    best_comparison: dict[str, float] | None = None
    best_active_index: int | None = None
    resolved_channel_penalties = _resolve_channel_penalties(
        channels,
        rgb_penalty=rgb_penalty,
        channel_penalties=channel_penalties,
    )
    for active_index in _active_channel_indices(
        channels,
        endpoint_bias,
        channel_penalties=resolved_channel_penalties,
    ):
        for weights in _coarse_weight_vectors(len(channels), active_index, coarse_levels):
            refined = _refine_weights(
                matrix,
                target,
                weights,
                active_index,
                channels=channels,
                rgb_penalty=rgb_penalty,
                channel_penalties=channel_penalties,
                refinement_steps=refinement_steps,
            )
            comparison = common.compare_vectors(matrix @ refined, target)
            penalty_cost = _rgb_penalty_cost(
                refined,
                channels,
                rgb_penalty=rgb_penalty,
                channel_penalties=channel_penalties,
            )
            score = comparison["relative_rmse"] + penalty_cost
            if best_score is None or score < best_score:
                best_weights = refined
                best_score = score
                best_comparison = comparison
                best_active_index = active_index

    if best_weights is None or best_comparison is None or best_score is None or best_active_index is None:
        raise RuntimeError("could not solve high-output RGBWW mix")

    command = {
        channel: int(round(float(weight) * max_code))
        for channel, weight in zip(channels, best_weights)
    }
    active_channel = str(channels[best_active_index])
    command[active_channel] = int(max_code)
    rgb_fraction = _rgb_fraction(best_weights, channels)
    weights = {channel: float(best_weights[index]) for index, channel in enumerate(channels)}
    return {
        "command": command,
        "weights": weights,
        "active_channel": active_channel,
        "comparison": best_comparison,
        "score": float(best_score),
        "rgb_fraction": rgb_fraction,
        "rgb_penalty": float(rgb_penalty),
        "channel_penalties": resolved_channel_penalties,
        "rgb_penalty_cost": _rgb_penalty_cost(
            best_weights,
            channels,
            rgb_penalty=rgb_penalty,
            channel_penalties=channel_penalties,
        ),
        "endpoint_bias": endpoint_bias,
        "predicted_vector_norm": common.vector_norm(matrix @ best_weights),
        "target_vector_norm": common.vector_norm(target),
    }


def run_white_lut_calibration(
    *,
    output_root: Path,
    run_name: str | None,
    endpoint_calibration: Path,
    location_config: Path,
    channel_response: Path,
    target_ccts: Sequence[int],
    target_gm_values: Sequence[int],
    neutral_roles: Sequence[str],
    color_weight: float,
    inside_rgb_penalty: float,
    outside_rgb_penalty: float,
    endpoint_rgb_penalty: float,
    max_code: int,
    safe_code_limit: int,
    allow_high_output: bool,
    dry_run: bool,
    settle_seconds: float,
    ray_intensity_percent: float,
    target_max: int,
    iso: str | None,
    aperture: str | None,
    image_format: str,
    min_shutter_speed: str,
    max_shutter_speed: str,
    max_trials: int,
    max_captures: int,
    decode_formats: Sequence[str],
    block_indices: str | tuple[int, ...],
    auto_exposure_metering_mode: str,
    auto_exposure_metering_location_config: Path | None,
    initial_lut: Path | None = None,
    output_json: Path | None = None,
    low_signal_ratio: float = DEFAULT_LOW_SIGNAL_RATIO,
    high_signal_ratio: float = DEFAULT_HIGH_SIGNAL_RATIO,
    leave_ray_on: bool = False,
    feedback_rounds: int = DEFAULT_FEEDBACK_ROUNDS,
    feedback_probe_step: int = DEFAULT_FEEDBACK_PROBE_STEP,
    feedback_max_step: int = DEFAULT_FEEDBACK_MAX_STEP,
    feedback_damping: float = DEFAULT_FEEDBACK_DAMPING,
    feedback_confirmations: int = DEFAULT_FEEDBACK_CONFIRMATIONS,
    feedback_confirmation_settle_seconds: float = DEFAULT_FEEDBACK_CONFIRMATION_SETTLE_SECONDS,
    feedback_confirmation_off_seconds: float = DEFAULT_FEEDBACK_CONFIRMATION_OFF_SECONDS,
    feedback_thermal_rebases: int = DEFAULT_FEEDBACK_THERMAL_REBASES,
    feedback_cct_tolerance_K: float = DEFAULT_FEEDBACK_CCT_TOLERANCE_K,
    feedback_cct_tolerance_mired: float = DEFAULT_FEEDBACK_CCT_TOLERANCE_MIRED,
    feedback_duv_tolerance: float = DEFAULT_FEEDBACK_DUV_TOLERANCE,
    light_fn: LightFn = esphome.light,
    ray_set_cct_fn: RaySetCctFn = ray120c.set_cct,
    auto_expose_fn: AutoExposeFn = camera_gphoto2.auto_expose_capture,
    capture_fn: CaptureFn = camera_gphoto2.capture_image,
    decoder_fn: DecoderFn = camera_gphoto2.decode_raw_image,
    white_point_estimator_fn: WhitePointEstimatorFn = common.estimate_capture_white_point,
    camera_backend: camera_gphoto2.CameraBackend | None = None,
    camera_backend_name: str = "local",
) -> Path:
    common.validate_high_output_plan(
        max_code=max_code,
        safe_code_limit=safe_code_limit,
        allow_high_output=allow_high_output,
        dry_run=dry_run,
        operation="white LUT calibration",
    )
    if camera_backend is not None:
        unbound_auto_expose = auto_expose_fn
        auto_expose_fn = lambda **kwargs: unbound_auto_expose(camera_backend=camera_backend, **kwargs)
        capture_fn = lambda **kwargs: camera_remote.capture_with_backend(
            camera_backend,
            output_dir=kwargs["output_dir"],
            filename_template=kwargs["filename_template"],
            settings=kwargs["settings"],
        )
    if feedback_rounds < 0:
        raise ValueError("feedback_rounds must be non-negative")
    if feedback_probe_step <= 0:
        raise ValueError("feedback_probe_step must be positive")
    if feedback_max_step <= 0:
        raise ValueError("feedback_max_step must be positive")
    if feedback_damping <= 0:
        raise ValueError("feedback_damping must be positive")
    if feedback_confirmations < 1:
        raise ValueError("feedback_confirmations must be at least 1")
    if feedback_confirmation_settle_seconds < 0:
        raise ValueError("feedback_confirmation_settle_seconds must be non-negative")
    if feedback_confirmation_off_seconds < 0:
        raise ValueError("feedback_confirmation_off_seconds must be non-negative")
    if feedback_thermal_rebases < 0:
        raise ValueError("feedback_thermal_rebases must be non-negative")
    if feedback_cct_tolerance_K <= 0:
        raise ValueError("feedback_cct_tolerance_K must be positive")
    if feedback_cct_tolerance_mired <= 0:
        raise ValueError("feedback_cct_tolerance_mired must be positive")
    if feedback_duv_tolerance <= 0:
        raise ValueError("feedback_duv_tolerance must be positive")
    if not target_ccts:
        raise ValueError("at least one target CCT is required")
    if not target_gm_values:
        raise ValueError("at least one target G/M value is required")
    for cct in target_ccts:
        if not ray120c.CCT_MIN <= int(cct) <= ray120c.CCT_MAX:
            raise ValueError(f"target CCT must be in [{ray120c.CCT_MIN}, {ray120c.CCT_MAX}]: {cct}")
    for gm in target_gm_values:
        if not ray120c.GM_MIN <= int(gm) <= ray120c.GM_MAX:
            raise ValueError(f"target G/M must be in [{ray120c.GM_MIN}, {ray120c.GM_MAX}]: {gm}")
    endpoint_data = load_endpoint_calibration(endpoint_calibration)
    initial_lut_data = white_lut_control.load_white_lut(initial_lut) if initial_lut is not None else None
    endpoint_matches = endpoint_data["ray_endpoint_matches"]
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = output_root / (run_name or timestamp)
    if output_json is None:
        output_json = run_dir / "white-lut-calibration.json"
    else:
        output_json = Path(output_json)
        run_dir = output_json.parent
    camera_dir = run_dir / "camera"
    decode_dir = run_dir / "decoded"
    scratch_dir = run_dir / "scratch"
    run_dir.mkdir(parents=True, exist_ok=True)

    regions = common.load_weighted_location_regions(
        location_config,
        block_indices,
        neutral_roles=neutral_roles,
        color_weight=color_weight,
    )
    metering_config, metering_regions = common.resolve_metering_regions(
        auto_exposure_metering_mode=auto_exposure_metering_mode,
        location_config=location_config,
        auto_exposure_metering_location_config=auto_exposure_metering_location_config,
    )
    basis = common.load_channel_basis(channel_response, regions, max_code=max_code)
    target_plan = []
    for target in common.build_target_grid(target_ccts, target_gm_values):
        target_plan.append({
            **target,
            "rgb_policy": policy.build_rgb_policy(
                target_cct=int(target["cct"]),
                target_gm=int(target["gm"]),
                endpoint_matches=endpoint_matches,
                cct_min=ray120c.CCT_MIN,
                cct_max=ray120c.CCT_MAX,
                gm_min=ray120c.GM_MIN,
                gm_max=ray120c.GM_MAX,
                native_penalty=inside_rgb_penalty,
                outside_penalty=outside_rgb_penalty,
                endpoint_penalty=endpoint_rgb_penalty,
            ),
        })
    result: dict[str, Any] = {
        "version": 1,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "run_dir": str(run_dir),
        "status": "planned" if dry_run else "running",
        "measurement": {
            "kind": "camera_based_rgbww_optimizer_white_lut_from_endpoint_calibration",
            "target_ccts": [int(value) for value in target_ccts],
            "target_gm_values": [int(value) for value in target_gm_values],
            "endpoint_calibration": str(endpoint_calibration),
            "endpoint_calibration_created_at": endpoint_data.get("created_at"),
            "white_range": endpoint_data["white_range"],
            "ray_intensity_percent": float(ray_intensity_percent),
            "max_code": int(max_code),
            "high_output_constraint": "max(cw, ww, r, g, b) == max_code for every RGBWW candidate",
            "allow_high_output": bool(allow_high_output),
            "settle_seconds": float(settle_seconds),
            "location_config": str(location_config),
            "regions": location_regions.jsonable_regions(regions),
            "neutral_roles": list(neutral_roles),
            "color_weight": float(color_weight),
            "inside_rgb_penalty": float(inside_rgb_penalty),
            "outside_rgb_penalty": float(outside_rgb_penalty),
            "endpoint_rgb_penalty": float(endpoint_rgb_penalty),
            "rgb_penalty_policy": {
                "kind": "native_gm_and_cct_extension_directional_rgb_penalty",
                "native_penalty": float(inside_rgb_penalty),
                "outside_cct_direction_cap": float(outside_rgb_penalty),
                "full_compensation_penalty": float(endpoint_rgb_penalty),
            },
            "feedback": {
                "kind": "constrained_white_point_jacobian_broyden",
                "rounds": int(feedback_rounds),
                "probe_step_code": int(feedback_probe_step),
                "max_step_code": int(feedback_max_step),
                "damping": float(feedback_damping),
                "confirmations": int(feedback_confirmations),
                "confirmation_settle_seconds": float(feedback_confirmation_settle_seconds),
                "confirmation_off_seconds": float(feedback_confirmation_off_seconds),
                "thermal_rebases": int(feedback_thermal_rebases),
                "cct_tolerance_K": float(feedback_cct_tolerance_K),
                "cct_tolerance_K_semantics": "minimum; raised at high CCT to the requested mired equivalent",
                "cct_tolerance_mired": float(feedback_cct_tolerance_mired),
                "duv_tolerance": float(feedback_duv_tolerance),
            },
            "decoded_npy_retention": "delete_after_measurement",
            "channel_response": str(channel_response),
            "initial_lut": str(initial_lut) if initial_lut is not None else None,
            "channel_response_kind": basis["kind"],
            "channel_response_sources": basis["source_measurements"],
            "notes": [
                "CW/WW endpoint CCT/G-M range is read from an independent white endpoint measurement JSON.",
                "Neutral patches are primary; color patches are auxiliary with lower weight.",
                "RGB penalties are directional per channel and relax according to CCT extension plus distance from the endpoint-interpolated native G/M.",
                "The code-duty curve is applied by the ESPHome control layer; stored commands are desired linear channel codes.",
                "The channel basis produces an initial command; camera-observed CCT/Duv feedback then refines it with a constrained Jacobian/Broyden loop.",
                "Use each target's selected_command as the final LUT value; solver.command is the model-only initial candidate.",
            ],
        },
        "camera": {
            "backend": camera_backend_name,
            "target_max": int(target_max),
            "iso": str(iso),
            "aperture": str(aperture),
            "image_format": str(image_format),
            "min_shutter_speed": str(min_shutter_speed),
            "max_shutter_speed": str(max_shutter_speed),
            "max_trials": int(max_trials),
            "max_captures": int(max_captures),
            "decode_formats": list(decode_formats),
            "scratch_dir": str(scratch_dir),
            "auto_exposure_metering": {
                "mode": auto_exposure_metering_mode,
                "location_config": str(metering_config) if metering_config is not None else None,
                "regions": location_regions.jsonable_regions(metering_regions) if metering_regions is not None else None,
            },
            "exposure_cache": {
                "initial_shutter_speed": camera_gphoto2.DEFAULT_SHUTTER_SPEED,
                "ray_final_shutter_speed": camera_gphoto2.DEFAULT_SHUTTER_SPEED,
                "strip_final_shutter_speed": camera_gphoto2.DEFAULT_SHUTTER_SPEED,
            },
        },
        "target_plan": target_plan,
        "ray_endpoint_matches": endpoint_matches,
        "white_range": endpoint_data["white_range"],
        "targets": [],
    }
    common.write_json(output_json, result)
    if dry_run:
        result["status"] = "dry_run"
        common.write_json(output_json, result)
        return output_json

    last_ray_target: dict[str, int] | None = None
    ray_shutter_speed = camera_gphoto2.DEFAULT_SHUTTER_SPEED
    strip_shutter_speed = camera_gphoto2.DEFAULT_SHUTTER_SPEED
    try:
        for target in target_plan:
            print(f"target {target['index'] + 1}/{len(target_plan)}: Ray {target['cct']}K gm={target['gm']} at {ray_intensity_percent:g}%")
            light_fn(0, 0, 0, 0, 0)
            last_ray_target = {"cct": int(target["cct"]), "gm": int(target["gm"])}
            ray_response = ray_set_cct_fn(
                target["cct"],
                intensity_percent=ray_intensity_percent,
                gm=target["gm"],
            )
            time.sleep(max(0.0, settle_seconds))
            ray_initial_shutter_speed = ray_shutter_speed
            ray_capture = common.capture_auto_exposed(
                auto_expose_fn=auto_expose_fn,
                camera_dir=camera_dir,
                decode_dir=decode_dir,
                scratch_dir=scratch_dir,
                filename_template=f"target-ray-{target['index']:02d}-{target['cct']}K-gm{target['gm']}.%C",
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
                initial_shutter_speed=ray_shutter_speed,
            )
            ray_shutter_speed = ray_capture.final_capture.settings.shutter_speed
            result["camera"]["exposure_cache"]["ray_final_shutter_speed"] = ray_shutter_speed
            print(f"  ray exposure: start={ray_initial_shutter_speed} final={ray_shutter_speed}")
            try:
                ray_auto_exposure_json = ray_capture.to_jsonable()
                ray_off_response = ray_set_cct_fn(
                    target["cct"],
                    intensity=0,
                    gm=target["gm"],
                )
                ray_seconds, target_vector, ray_regions = common.measure_auto_exposure_regions(ray_capture, regions)
                target_white_point = white_point_estimator_fn(ray_capture.final_capture, regions)
            finally:
                removed_ray_npy_files = common.remove_capture_npy_outputs(ray_capture.final_capture)
            resolved_cct_tolerance_K = feedback.resolve_cct_tolerance_K(
                float(target_white_point["cct_K"]),
                minimum_tolerance_K=feedback_cct_tolerance_K,
                tolerance_mired=feedback_cct_tolerance_mired,
            )
            range_class = common.classify_target_range(
                target["cct"],
                cw_match=endpoint_matches["cw"],
                ww_match=endpoint_matches["ww"],
            )
            endpoint_bias = _endpoint_bias_for_range(range_class, matches=endpoint_matches)
            rgb_policy = target["rgb_policy"]
            rgb_penalty = float(rgb_policy["effective_rgb_penalty"])
            channel_penalties = {
                channel: float(value)
                for channel, value in rgb_policy["channel_penalties"].items()
            }
            solution = solve_high_output_mix(
                basis["vectors"],
                target_vector,
                regions=regions,
                rgb_penalty=rgb_penalty,
                channel_penalties=channel_penalties,
                endpoint_bias=endpoint_bias,
                max_code=max_code,
            )
            if initial_lut_data is not None:
                solution = seed_solution_from_lut(
                    solution,
                    initial_lut_data,
                    cct=int(target["cct"]),
                    gm=int(target["gm"]),
                    max_code=max_code,
                )
            if "camera_neutral_g1" in target_white_point and "rawpy_rgb_xyz_matrix_first3" in target_white_point:
                white_point_solution = solve_white_point_mix(
                    basis["vectors"],
                    target_white_point,
                    regions=regions,
                    max_code=max_code,
                )
                prior_command = dict(solution["command"])
                prior_active_channel = str(solution["active_channel"])
                prior_comparison = solution.get("initial_lut_seed", {}).get("prior_white_point_comparison")
                prior_score = float("inf")
                if isinstance(prior_comparison, dict):
                    prior_score = max(
                        abs(float(prior_comparison["cct_error_K"])) / float(resolved_cct_tolerance_K),
                        abs(float(prior_comparison["duv_error"])) / float(feedback_duv_tolerance),
                    )
                predicted = white_point_solution["best"]["predicted_white_point"]
                model_score = feedback.white_point_metrics(
                    predicted,
                    target_white_point,
                    cct_tolerance_K=resolved_cct_tolerance_K,
                    duv_tolerance=feedback_duv_tolerance,
                )["goal_score"]
                model_initial = {
                    "active_channel": str(white_point_solution["best"]["active_channel"]),
                    "command": dict(white_point_solution["best"]["command"]),
                    "source": "white_point_model",
                }
                prior_initial = {
                    "active_channel": prior_active_channel,
                    "command": prior_command,
                    "source": "initial_lut",
                }
                use_prior_local_start = prior_score <= DEFAULT_INITIAL_LUT_LOCAL_SCORE_LIMIT
                primary, alternative = (
                    (prior_initial, model_initial)
                    if use_prior_local_start
                    else (model_initial, prior_initial)
                )
                solution = {
                    **solution,
                    "pre_white_point_command": prior_command,
                    "pre_white_point_active_channel": prior_active_channel,
                    "command": dict(primary["command"]),
                    "active_channel": str(primary["active_channel"]),
                    "initial_solution_scores": {
                        "initial_lut": prior_score,
                        "white_point_model": float(model_score),
                        "initial_lut_local_score_limit": DEFAULT_INITIAL_LUT_LOCAL_SCORE_LIMIT,
                        "selected": str(primary["source"]),
                    },
                    "alternative_initial_solutions": [alternative],
                    "white_point_solution": white_point_solution,
                }
            command = solution["command"]
            print(
                f"  {range_class['mode']} rgb_penalty="
                f"r:{channel_penalties['r']:.3f}/g:{channel_penalties['g']:.3f}/b:{channel_penalties['b']:.3f} "
                f"command: cw={command['cw']} ww={command['ww']} r={command['r']} g={command['g']} b={command['b']}"
            )
            target_result = {
                **target,
                "status": "optimizing",
                "range_classification": range_class,
                "ray": {
                    "set_response": ray_response,
                    "off_response": ray_off_response,
                    "initial_shutter_speed": ray_initial_shutter_speed,
                    "auto_exposure": ray_auto_exposure_json,
                    "removed_npy_files": [str(path) for path in removed_ray_npy_files],
                    "shutter_seconds": ray_seconds,
                    "vector_norm": common.vector_norm(target_vector),
                    "white_point": target_white_point,
                    "regions": ray_regions,
                },
                "solver": {
                    **solution,
                    "max_channel_value": max(command.values()),
                },
                "feedback_optimizer": {"status": "pending", "samples": []},
                "feedback_goal": {
                    "minimum_cct_tolerance_K": float(feedback_cct_tolerance_K),
                    "cct_tolerance_mired": float(feedback_cct_tolerance_mired),
                    "resolved_cct_tolerance_K": float(resolved_cct_tolerance_K),
                    "duv_tolerance": float(feedback_duv_tolerance),
                },
            }
            result["targets"].append(target_result)
            common.write_json(output_json, result)

            def persist_feedback(progress: dict[str, Any]) -> None:
                target_result["feedback_optimizer"] = progress
                common.write_json(output_json, result)

            feedback_attempts = []
            for attempt_solution in feedback_restart_solutions(solution, max_code=max_code):
                feedback_result = feedback.run_feedback_optimization(
                    target=target,
                    target_vector=target_vector,
                    target_white_point=target_white_point,
                    initial_solution=attempt_solution,
                    rgb_penalty=rgb_penalty,
                    channel_penalties=channel_penalties,
                    regions=regions,
                    camera_dir=camera_dir,
                    decode_dir=decode_dir,
                    scratch_dir=scratch_dir,
                    initial_shutter_speed=strip_shutter_speed,
                    iso=iso,
                    aperture=aperture,
                    image_format=image_format,
                    min_shutter_speed=min_shutter_speed,
                    max_shutter_speed=max_shutter_speed,
                    max_trials=max_trials,
                    max_captures=max_captures,
                    decode_formats=decode_formats,
                    metering_regions=metering_regions,
                    settle_seconds=settle_seconds,
                    target_max=target_max,
                    low_signal_ratio=low_signal_ratio,
                    high_signal_ratio=high_signal_ratio,
                    max_code=max_code,
                    feedback_rounds=feedback_rounds,
                    feedback_probe_step=feedback_probe_step,
                    feedback_max_step=feedback_max_step,
                    feedback_damping=feedback_damping,
                    feedback_confirmations=feedback_confirmations,
                    feedback_confirmation_settle_seconds=feedback_confirmation_settle_seconds,
                    feedback_confirmation_off_seconds=feedback_confirmation_off_seconds,
                    feedback_thermal_rebases=feedback_thermal_rebases,
                    feedback_cct_tolerance_K=resolved_cct_tolerance_K,
                    feedback_duv_tolerance=feedback_duv_tolerance,
                    light_fn=light_fn,
                    auto_expose_fn=auto_expose_fn,
                    capture_fn=capture_fn,
                    decoder_fn=decoder_fn,
                    white_point_estimator_fn=white_point_estimator_fn,
                    progress_fn=persist_feedback,
                )
                feedback_result["restart"] = attempt_solution["feedback_restart"]
                feedback_attempts.append(feedback_result)
                strip_shutter_speed = str(feedback_result["final_shutter_speed"])
                if feedback_result["goal_confirmed"]:
                    break
            feedback_result = min(
                feedback_attempts,
                key=feedback_attempt_sort_key,
            )
            strip_shutter_speed = str(feedback_result["final_shutter_speed"])
            result["camera"]["exposure_cache"]["strip_final_shutter_speed"] = strip_shutter_speed
            print(
                f"  strip exposure: start={feedback_result['initial_shutter_speed']} "
                f"final={strip_shutter_speed}"
            )
            within_goal = bool(feedback_result["goal_confirmed"])
            target_result["status"] = "complete" if within_goal else "unmet_goal"
            target_result["feedback_optimizer"] = feedback_result
            if len(feedback_attempts) > 1:
                target_result["feedback_attempts"] = feedback_attempts
            target_result["selected_command"] = feedback_result["best"]["command"]
            target_result["rgbww"] = feedback_result["best"]
            common.write_json(output_json, result)

        result["status"] = (
            "complete"
            if all(target_result["status"] == "complete" for target_result in result["targets"])
            else "complete_with_unmet_targets"
        )
        common.write_json(output_json, result)
        return output_json
    except Exception as exc:
        result["status"] = "error"
        result["error"] = f"{type(exc).__name__}: {exc}"
        common.write_json(output_json, result)
        raise
    finally:
        try:
            light_fn(0, 0, 0, 0, 0)
        except Exception:
            pass
        if last_ray_target is not None:
            try:
                if leave_ray_on:
                    ray_set_cct_fn(
                        last_ray_target["cct"],
                        intensity_percent=ray_intensity_percent,
                        gm=last_ray_target["gm"],
                    )
                else:
                    ray_set_cct_fn(last_ray_target["cct"], intensity=0, gm=last_ray_target["gm"])
            except Exception:
                pass



def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Measure a small CCT/G-M white calibration LUT using a prior WW/CW endpoint calibration JSON."
    )
    parser.add_argument("--endpoint-calibration", type=Path, default=DEFAULT_ENDPOINT_CALIBRATION)
    parser.add_argument("--target-ccts", "--ccts", type=common.parse_int_values, default=DEFAULT_TARGET_CCTS)
    parser.add_argument("--target-gm-values", "--gm-values", type=common.parse_int_values, default=DEFAULT_TARGET_GM_VALUES)
    parser.add_argument("--location-config", type=Path, default=DEFAULT_LOCATION_CONFIG)
    parser.add_argument("--channel-response", type=Path, default=DEFAULT_CHANNEL_RESPONSE)
    parser.add_argument("--initial-lut", type=Path)
    parser.add_argument("--block-indices", type=measure_channel_response.parse_block_indices, default="all")
    parser.add_argument("--neutral-roles", type=common.parse_roles, default=common.DEFAULT_NEUTRAL_ROLES)
    parser.add_argument("--color-weight", type=float, default=common.DEFAULT_COLOR_WEIGHT)
    parser.add_argument(
        "--native-rgb-penalty",
        "--inside-rgb-penalty",
        dest="inside_rgb_penalty",
        type=float,
        default=DEFAULT_INSIDE_RGB_PENALTY,
    )
    parser.add_argument(
        "--cct-outside-rgb-penalty",
        "--outside-rgb-penalty",
        dest="outside_rgb_penalty",
        type=float,
        default=DEFAULT_OUTSIDE_RGB_PENALTY,
    )
    parser.add_argument(
        "--full-compensation-rgb-penalty",
        "--endpoint-rgb-penalty",
        dest="endpoint_rgb_penalty",
        type=float,
        default=DEFAULT_ENDPOINT_RGB_PENALTY,
    )
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_ROOT)
    parser.add_argument("--run-name")
    parser.add_argument("--output-json", type=Path)
    parser.add_argument("--max-code", type=int, default=DEFAULT_MAX_CODE)
    parser.add_argument("--safe-code-limit", type=int, default=DEFAULT_SAFE_CODE_LIMIT)
    parser.add_argument("--allow-high-output", action="store_true")
    parser.add_argument("--settle-seconds", type=float, default=DEFAULT_SETTLE_SECONDS)
    parser.add_argument("--ray-intensity-percent", type=float, default=DEFAULT_RAY_INTENSITY_PERCENT)
    parser.add_argument("--target-max", type=int, default=camera_gphoto2.DEFAULT_AUTO_EXPOSURE_MAX)
    parser.add_argument("--iso")
    parser.add_argument("--aperture")
    parser.add_argument("--image-format", default=camera_gphoto2.DEFAULT_IMAGE_FORMAT)
    parser.add_argument("--min-shutter-speed", default=camera_gphoto2.DEFAULT_MIN_SHUTTER_SPEED)
    parser.add_argument("--max-shutter-speed", default=camera_gphoto2.DEFAULT_MAX_SHUTTER_SPEED)
    parser.add_argument("--max-trials", type=int, default=camera_gphoto2.DEFAULT_AUTO_EXPOSURE_MAX_TRIALS)
    parser.add_argument("--max-captures", type=int, default=camera_gphoto2.DEFAULT_AUTO_EXPOSURE_MAX_CAPTURES)
    parser.add_argument("--decode-format", dest="decode_formats", action="append")
    parser.add_argument(
        "--auto-exposure-metering-mode",
        choices=(camera_gphoto2.METERING_MODE_FULL, camera_gphoto2.METERING_MODE_LOCATION),
        default=camera_gphoto2.METERING_MODE_LOCATION,
    )
    parser.add_argument("--auto-exposure-metering-location-config", type=Path)
    parser.add_argument("--low-signal-ratio", type=float, default=DEFAULT_LOW_SIGNAL_RATIO)
    parser.add_argument("--high-signal-ratio", type=float, default=DEFAULT_HIGH_SIGNAL_RATIO)
    parser.add_argument("--feedback-rounds", type=int, default=DEFAULT_FEEDBACK_ROUNDS)
    parser.add_argument("--feedback-probe-step", type=int, default=DEFAULT_FEEDBACK_PROBE_STEP)
    parser.add_argument("--feedback-max-step", type=int, default=DEFAULT_FEEDBACK_MAX_STEP)
    parser.add_argument("--feedback-damping", type=float, default=DEFAULT_FEEDBACK_DAMPING)
    parser.add_argument("--feedback-confirmations", type=int, default=DEFAULT_FEEDBACK_CONFIRMATIONS)
    parser.add_argument(
        "--feedback-confirmation-settle-seconds",
        type=float,
        default=DEFAULT_FEEDBACK_CONFIRMATION_SETTLE_SECONDS,
    )
    parser.add_argument(
        "--feedback-confirmation-off-seconds",
        type=float,
        default=DEFAULT_FEEDBACK_CONFIRMATION_OFF_SECONDS,
    )
    parser.add_argument("--feedback-thermal-rebases", type=int, default=DEFAULT_FEEDBACK_THERMAL_REBASES)
    parser.add_argument(
        "--feedback-cct-tolerance-k",
        "--feedback-cct-tolerance-K",
        dest="feedback_cct_tolerance_K",
        type=float,
        default=DEFAULT_FEEDBACK_CCT_TOLERANCE_K,
    )
    parser.add_argument(
        "--feedback-cct-tolerance-mired",
        type=float,
        default=DEFAULT_FEEDBACK_CCT_TOLERANCE_MIRED,
    )
    parser.add_argument("--feedback-duv-tolerance", type=float, default=DEFAULT_FEEDBACK_DUV_TOLERANCE)
    parser.add_argument("--leave-ray-on", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    camera_remote.add_camera_backend_arguments(parser, default="remote")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    backend = None
    if not args.dry_run:
        backend = camera_remote.create_camera_backend(
            args.camera_backend,
            env_file=args.remote_env_file,
            base_url=args.remote_base_url,
            timeout=args.remote_timeout,
        )
    output_json = run_white_lut_calibration(
        output_root=args.output_dir,
        run_name=args.run_name,
        endpoint_calibration=args.endpoint_calibration,
        location_config=args.location_config,
        channel_response=args.channel_response,
        target_ccts=args.target_ccts,
        target_gm_values=args.target_gm_values,
        neutral_roles=args.neutral_roles,
        color_weight=args.color_weight,
        inside_rgb_penalty=args.inside_rgb_penalty,
        outside_rgb_penalty=args.outside_rgb_penalty,
        endpoint_rgb_penalty=args.endpoint_rgb_penalty,
        max_code=args.max_code,
        safe_code_limit=args.safe_code_limit,
        allow_high_output=args.allow_high_output,
        dry_run=args.dry_run,
        settle_seconds=args.settle_seconds,
        ray_intensity_percent=args.ray_intensity_percent,
        target_max=args.target_max,
        iso=args.iso,
        aperture=args.aperture,
        image_format=args.image_format,
        min_shutter_speed=args.min_shutter_speed,
        max_shutter_speed=args.max_shutter_speed,
        max_trials=args.max_trials,
        max_captures=args.max_captures,
        decode_formats=tuple(args.decode_formats or measure_channel_response.DEFAULT_DECODE_FORMATS),
        block_indices=args.block_indices,
        auto_exposure_metering_mode=args.auto_exposure_metering_mode,
        auto_exposure_metering_location_config=args.auto_exposure_metering_location_config,
        initial_lut=args.initial_lut,
        output_json=args.output_json,
        low_signal_ratio=args.low_signal_ratio,
        high_signal_ratio=args.high_signal_ratio,
        feedback_rounds=args.feedback_rounds,
        feedback_probe_step=args.feedback_probe_step,
        feedback_max_step=args.feedback_max_step,
        feedback_damping=args.feedback_damping,
        feedback_confirmations=args.feedback_confirmations,
        feedback_confirmation_settle_seconds=args.feedback_confirmation_settle_seconds,
        feedback_confirmation_off_seconds=args.feedback_confirmation_off_seconds,
        feedback_thermal_rebases=args.feedback_thermal_rebases,
        feedback_cct_tolerance_K=args.feedback_cct_tolerance_K,
        feedback_cct_tolerance_mired=args.feedback_cct_tolerance_mired,
        feedback_duv_tolerance=args.feedback_duv_tolerance,
        leave_ray_on=args.leave_ray_on,
        camera_backend=backend,
        camera_backend_name=args.camera_backend,
    )
    print(output_json)
    data = json.loads(output_json.read_text(encoding="utf-8"))
    return 0 if data.get("status") in {"complete", "dry_run"} else 2


def _active_channel_indices(
    channels: Sequence[str],
    endpoint_bias: str | None,
    *,
    channel_penalties: dict[str, float] | None = None,
) -> list[int]:
    if endpoint_bias in channels and channel_penalties:
        highest_penalty = max(channel_penalties.values())
        compensation_channels = [
            channel
            for channel in ("r", "g", "b")
            if channel in channels and channel_penalties.get(channel, highest_penalty) < highest_penalty
        ]
        return [channels.index(channel) for channel in (*compensation_channels, endpoint_bias)]
    if endpoint_bias in channels:
        return [channels.index(endpoint_bias)]
    return list(range(len(channels)))


def _coarse_weight_vectors(channel_count: int, active_index: int, levels: Sequence[float]) -> list[Any]:
    np = common.import_numpy()
    vectors = []
    for values in itertools.product(levels, repeat=channel_count - 1):
        weights = np.zeros(channel_count, dtype="float64")
        weights[active_index] = 1.0
        value_iter = iter(values)
        for index in range(channel_count):
            if index == active_index:
                continue
            weights[index] = min(max(float(next(value_iter)), 0.0), 1.0)
        vectors.append(weights)
    return vectors


def _refine_weights(
    matrix: Any,
    target: Any,
    weights: Any,
    active_index: int,
    *,
    channels: Sequence[str],
    rgb_penalty: float,
    channel_penalties: dict[str, float] | None,
    refinement_steps: Sequence[float],
) -> Any:
    np = common.import_numpy()
    current = np.array(weights, dtype="float64")
    best_score = _solver_score(
        matrix,
        target,
        current,
        channels=channels,
        rgb_penalty=rgb_penalty,
        channel_penalties=channel_penalties,
    )
    for step in refinement_steps:
        improved = True
        while improved:
            improved = False
            for index in range(current.size):
                if index == active_index:
                    continue
                for delta in (-float(step), float(step)):
                    candidate = np.array(current, dtype="float64")
                    candidate[index] = min(max(candidate[index] + delta, 0.0), 1.0)
                    score = _solver_score(
                        matrix,
                        target,
                        candidate,
                        channels=channels,
                        rgb_penalty=rgb_penalty,
                        channel_penalties=channel_penalties,
                    )
                    if score + 1e-12 < best_score:
                        current = candidate
                        best_score = score
                        improved = True
    current[active_index] = 1.0
    return current


def _solver_score(
    matrix: Any,
    target: Any,
    weights: Any,
    *,
    channels: Sequence[str],
    rgb_penalty: float,
    channel_penalties: dict[str, float] | None = None,
) -> float:
    comparison = common.compare_vectors(matrix @ weights, target)
    return float(comparison["relative_rmse"]) + _rgb_penalty_cost(
        weights,
        channels,
        rgb_penalty=rgb_penalty,
        channel_penalties=channel_penalties,
    )


def _rgb_fraction(weights: Any, channels: Sequence[str]) -> float:
    total = sum(float(value) for value in weights)
    if total <= 0:
        return 0.0
    rgb = sum(float(weights[index]) for index, channel in enumerate(channels) if channel in {"r", "g", "b"})
    return float(rgb / total)


def _resolve_channel_penalties(
    channels: Sequence[str],
    *,
    rgb_penalty: float,
    channel_penalties: dict[str, float] | None,
) -> dict[str, float]:
    resolved: dict[str, float] = {}
    for channel in channels:
        if channel not in {"r", "g", "b"}:
            continue
        value = float(rgb_penalty if channel_penalties is None else channel_penalties.get(channel, rgb_penalty))
        if value < 0:
            raise ValueError(f"RGB penalty must be non-negative for channel {channel}")
        resolved[channel] = value
    return resolved


def _rgb_penalty_cost(
    weights: Any,
    channels: Sequence[str],
    *,
    rgb_penalty: float,
    channel_penalties: dict[str, float] | None,
) -> float:
    total = sum(float(value) for value in weights)
    if total <= 0:
        return 0.0
    resolved = _resolve_channel_penalties(
        channels,
        rgb_penalty=rgb_penalty,
        channel_penalties=channel_penalties,
    )
    return float(
        sum(
            resolved[channel] * float(weights[index])
            for index, channel in enumerate(channels)
            if channel in resolved
        )
        / total
    )


def _endpoint_bias_for_range(range_class: dict[str, Any], *, matches: dict[str, dict[str, Any]]) -> str | None:
    if range_class["inside"]:
        return None
    cct = range_class["low_cct"] if range_class["mode"].startswith("below") else range_class["high_cct"]
    distances = {
        channel: abs(int(match["best"]["cct"]) - int(cct))
        for channel, match in matches.items()
    }
    return min(distances, key=distances.get)


if __name__ == "__main__":
    raise SystemExit(main())
