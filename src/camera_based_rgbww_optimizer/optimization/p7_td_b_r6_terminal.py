"""Single owner for Ray R6 formal terminal evidence.

This module deliberately does not own acquisition, scientific interpretation,
or release decisions.  It projects the existing capture records into the
repo-owned R6 ledger validator, performs one independent final-zero check, and
seals one terminal success or accepted hard-failure result.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import re
import stat
from typing import Any, Callable, Mapping, Sequence

from camera_based_rgbww_optimizer.control import all_off, esphome, ray120c
from camera_based_rgbww_optimizer.measurement.raw_observer_analysis import (
    collect_patch_plane_features,
)
from camera_based_rgbww_optimizer.measurement.recorded_exposure import (
    parse_nominal_exposure,
)
from camera_based_rgbww_optimizer.optimization import p7_thermal_diagnostics as thermal
from camera_based_rgbww_optimizer.optimization.hsi_objective import (
    TD_B_FORMAL_FEATURE_STATISTIC,
)
from camera_based_rgbww_optimizer.utils import p7_retained_r3_provenance_io as provenance


TASK_ID = "REF-G4-06-RAY-R6"
CONTRACT_ID = "G4-RAY-R6-FORMAL-TERMINAL-EVIDENCE-ENGINEERING-V1"
INDEPENDENT_ZERO_SCHEMA = "p7_td_b_r6_independent_final_zero_v1"
TERMINAL_AUDIT_SCHEMA = "p7_td_b_r6_terminal_audit_v1"
TERMINAL_SEAL_SCHEMA = "p7_td_b_r6_terminal_seal_v1"
RETURNED_SUMMARY_SCHEMA = "p7_td_b_r6_returned_summary_v1"
PLAN_AUTHORITY_SCHEMA = "p7_td_b_r6_plan_bound_authority_v1"
FORMAL_ROOT_RE = re.compile(
    r"p7-td-b-formal-r6-[0-9a-f]{12}-[0-9]{8}T[0-9]{6}Z\Z"
)
_SHA256_RE = re.compile(r"[0-9a-f]{64}\Z")

REQUIRED_SUCCESS_FILES = (
    "all-off-python.json",
    "all-off-shell.exit-status.txt",
    "all-off-shell.json",
    "all-off-shell.stderr.log",
    "captures.jsonl",
    "child-exit-status.txt",
    "commands-audit.json",
    "commands.jsonl",
    "independent-final-zero.json",
    "isolation-gates.jsonl",
    "physical-returns.jsonl",
    "plan.json",
    "run.json",
    "thermal-covariates.jsonl",
)


class TerminalEvidenceError(RuntimeError):
    """Stable fail-closed terminal evidence error."""

    def __init__(self, code: str) -> None:
        self.code = code
        super().__init__(code)


@dataclass(frozen=True)
class IndependentZeroDependencies:
    strip_off: Callable[[], Mapping[str, Any]]
    ray_set_cct: Callable[..., Mapping[str, Any]]
    ray_get_cct: Callable[..., Mapping[str, Any]]
    curve: Callable[[], Mapping[str, Any]]
    validate_both_off: Callable[[Mapping[str, Any], Mapping[str, Any], Mapping[str, Any]], None]


def _default_zero_dependencies() -> IndependentZeroDependencies:
    from camera_based_rgbww_optimizer.optimization.hsi_source_evidence import (
        validate_both_off,
    )

    return IndependentZeroDependencies(
        strip_off=lambda: esphome.verified_light(
            0, 0, 0, 0, 0, curve_path=thermal.CURVE_PATH,
        ),
        ray_set_cct=ray120c.set_cct,
        ray_get_cct=ray120c.get_cct,
        curve=lambda: json.loads(thermal.CURVE_PATH.read_text(encoding="utf-8")),
        validate_both_off=validate_both_off,
    )


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _require(condition: bool, code: str) -> None:
    if not condition:
        raise TerminalEvidenceError(code)


def classify_wrapper_argv(argv: Sequence[str]) -> str:
    """Return ``r6`` only for the exact parsed formal stage-gate invocation."""

    values: dict[str, str] = {}
    flags: set[str] = set()
    value_options = {
        "--experiment-id", "--source", "--phase", "--stage-gate-package",
        "--code-checkpoint",
    }
    disqualifying = {
        "--dry-run", "--orchestrate-setup", "--finalize-setup-run",
        "--eq-r6-prelaunch", "--eq-r6-orchestrate", "--eq-r6-single-candidate",
        "--prepare-lineage-qualification-evidence", "--qualify-lineage-release",
    }
    wrapper_owned = {"--execute", "--allow-device-control", "--output-dir", "--run-name"}
    items = tuple(str(value) for value in argv)
    index = 0
    while index < len(items):
        token = items[index]
        if token in wrapper_owned:
            raise TerminalEvidenceError("wrapper_owned_option_conflict")
        if token in value_options:
            if token in values:
                raise TerminalEvidenceError("wrapper_duplicate_option")
            if index + 1 >= len(items) or items[index + 1].startswith("--"):
                raise TerminalEvidenceError("wrapper_missing_option_value")
            values[token] = items[index + 1]
            index += 2
            continue
        if token in disqualifying:
            flags.add(token)
        index += 1
    exact = (
        not flags
        and values.get("--experiment-id") == thermal.TD_B
        and values.get("--source") == "ray"
        and values.get("--phase") == "formal"
        and bool(values.get("--stage-gate-package"))
        and bool(values.get("--code-checkpoint"))
    )
    return "r6" if exact else "legacy"


def is_r6_materialized_plan(plan: Mapping[str, Any]) -> bool:
    authority = plan.get("execution_authorization")
    return (
        isinstance(authority, Mapping)
        and authority.get("schema") == PLAN_AUTHORITY_SCHEMA
        and authority.get("execution_authorized") is True
        and plan.get("experiment_id") == thermal.TD_B
        and plan.get("guide_experiment_id") == thermal.TD_B_R6_EXPERIMENT_ID
        and plan.get("source") == "ray"
        and tuple(str(row.get("capture_id")) for row in plan.get("captures", ()))
        == thermal.TD_B_R6_CAPTURE_IDS
    )


def project_quality_capture(
    report: Mapping[str, Any],
    *,
    capture_id: str,
    required_feature_ids: Sequence[str],
    nominal_shutter: str,
) -> dict[str, Any]:
    """Project existing RAW observer evidence without owning quality policy."""

    required = tuple(str(value) for value in required_feature_ids)
    collection = collect_patch_plane_features(
        [report], statistic=TD_B_FORMAL_FEATURE_STATISTIC,
    )
    by_id = {
        str(item["feature_id"]): item for item in collection["observations"]
    }
    observations = {
        feature_id: by_id[feature_id]
        for feature_id in required
        if feature_id in by_id
    }
    _require(tuple(observations) == required, "quality_feature_order_drift")
    exposure = report.get("exposure_metadata")
    _require(isinstance(exposure, Mapping), "recorded_exposure_missing")
    nominal_seconds = parse_nominal_exposure(nominal_shutter)
    recorded_seconds = float(exposure.get("seconds", math.nan))
    ratio_pass = (
        math.isfinite(recorded_seconds)
        and recorded_seconds > 0
        and 0.8 <= recorded_seconds / nominal_seconds <= 1.2
    )
    return {
        "capture_id": capture_id,
        "nominal_shutter": nominal_shutter,
        "recorded_exposure": dict(exposure),
        "nominal_recorded_ratio_gate": "pass" if ratio_pass else "fail",
        "feature_quality": {
            feature_id: {
                "value": observations[feature_id].get("value"),
                "clipped_fraction": observations[feature_id]["metrics"]["clipped_fraction"],
                "near_noise_floor_fraction": observations[feature_id]["metrics"][
                    "near_noise_floor_fraction"
                ],
                "valid_pixel_count": observations[feature_id]["metrics"][
                    "valid_pixel_count"
                ],
            }
            for feature_id in required
        },
    }


def _strict_json_bytes(data: bytes) -> Any:
    try:
        return provenance.json_native_value(provenance.decode_strict_json_bytes(data))
    except provenance.ProvenanceIOError as exc:
        raise TerminalEvidenceError(f"json_invalid:{exc.code}") from exc


def _parse_jsonl_bytes(payload: bytes) -> list[dict[str, Any]]:
    _require(payload.endswith(b"\n") and not payload.endswith(b"\n\n"), "jsonl_lf_invalid")
    rows = []
    for line in payload.splitlines():
        value = _strict_json_bytes(line)
        _require(isinstance(value, dict), "jsonl_row_not_object")
        rows.append(value)
    return rows


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    try:
        return _parse_jsonl_bytes(path.read_bytes())
    except OSError as exc:
        raise TerminalEvidenceError("jsonl_read_failed") from exc


def _required_feature_ids() -> tuple[str, ...]:
    policy = json.loads(thermal.POLICY_PATH.read_text(encoding="utf-8"))
    return tuple(str(value) for value in policy["feature_set"]["ids"])


def _validate_retained_capture_file(
    value: str,
    *,
    root: Path,
    expected_bytes: object,
    expected_sha256: object,
) -> None:
    candidate = Path(value)
    try:
        resolved = candidate.resolve(strict=True)
        owned = (
            candidate.is_absolute()
            and not candidate.is_symlink()
            and resolved.is_relative_to(root)
            and resolved.is_file()
            and not any(parent.is_symlink() for parent in resolved.parents if parent != root.parent)
        )
        payload = resolved.read_bytes() if owned else b""
    except OSError as exc:
        raise TerminalEvidenceError("capture_file_read_failed") from exc
    _require(
        owned
        and type(expected_bytes) is int
        and expected_bytes > 0
        and len(payload) == expected_bytes
        and type(expected_sha256) is str
        and _SHA256_RE.fullmatch(expected_sha256) is not None
        and hashlib.sha256(payload).hexdigest() == expected_sha256,
        "capture_file_identity_drift",
    )


def _expected_command_groups(
    plan: Mapping[str, Any],
) -> tuple[tuple[Mapping[str, Any], ...], ...]:
    groups: list[list[Mapping[str, Any]]] = []
    experiment_id = str(plan.get("experiment_id"))
    for step in plan.get("captures", ()):
        _require(isinstance(step, Mapping), "plan_capture_invalid")
        _require(step.get("capture_role") == "formal", "r6_ambient_capture_invalid")
        key = thermal.timing_sequence_identity(experiment_id, step)
        previous = groups[-1][0] if groups else None
        previous_key = (
            None
            if previous is None
            else thermal.timing_sequence_identity(experiment_id, previous)
        )
        if (
            groups
            and key == previous_key
            and float(step["requested_elapsed_s"])
            > float(groups[-1][-1]["requested_elapsed_s"])
        ):
            groups[-1].append(step)
        else:
            groups.append([step])
    return tuple(tuple(group) for group in groups)


def _validate_command_and_isolation_ledgers(
    *,
    plan: Mapping[str, Any],
    commands: Sequence[Mapping[str, Any]],
    isolation_gates: Sequence[Mapping[str, Any]],
) -> None:
    from camera_based_rgbww_optimizer.optimization.hsi_source_evidence import (
        validate_both_off,
        validate_ray_readback,
    )

    groups = _expected_command_groups(plan)
    _require(len(commands) == len(groups), "command_ledger_count_drift")
    for row, group in zip(commands, groups, strict=True):
        first = group[0]
        _require(
            set(row) == {
                "at", "event", "source_id", "state_id", "exact_command_hash",
                "applied", "readback",
            }
            and row.get("event") == "command_readback_verified"
            and row.get("source_id") == first.get("source_id")
            and row.get("state_id") == first.get("state_id")
            and row.get("exact_command_hash") == first.get("exact_command_hash")
            and isinstance(row.get("at"), str)
            and bool(row.get("at"))
            and isinstance(row.get("applied"), Mapping)
            and bool(row.get("applied"))
            and isinstance(row.get("readback"), Mapping)
            and bool(row.get("readback")),
            "command_readback_ledger_drift",
        )
        command = first.get("command")
        _require(isinstance(command, Mapping), "ray_command_missing")
        try:
            expected_readback = {
                "hue": int(command["hue"]),
                "sat": int(command["sat"]),
                "intensity": ray120c.intensity_percent_to_raw(
                    float(command["intensity_percent"]),
                ),
            }
            validate_ray_readback(row["applied"], expected_readback)
            validate_ray_readback(row["readback"], expected_readback)
        except (KeyError, TypeError, ValueError) as exc:
            raise TerminalEvidenceError("ray_command_readback_drift") from exc
    expected_gate_ids = (
        "run_start",
        *(str(group[-1]["isolation_gate_after"]) for group in groups),
    )
    _require(
        tuple(str(row.get("gate_id")) for row in isolation_gates)
        == expected_gate_ids,
        "isolation_gate_order_drift",
    )
    try:
        curve = json.loads(thermal.CURVE_PATH.read_text(encoding="utf-8"))
    except (OSError, TypeError, ValueError) as exc:
        raise TerminalEvidenceError("isolation_curve_invalid") from exc
    for row in isolation_gates:
        evidence = row.get("evidence")
        _require(
            set(row) == {"gate_id", "evidence", "at"}
            and isinstance(row.get("at"), str)
            and bool(row.get("at"))
            and isinstance(evidence, Mapping)
            and evidence.get("status") == "pass"
            and evidence.get("gate_id") == row.get("gate_id")
            and evidence.get("strip_verified_off") is True
            and evidence.get("ray_verified_off") is True,
            "isolation_gate_evidence_drift",
        )
        _require(
            isinstance(evidence.get("ray_off_command"), Mapping)
            and bool(evidence.get("ray_off_command"))
            and isinstance(evidence.get("strip_device_evidence"), Mapping)
            and isinstance(evidence.get("ray_readback"), Mapping),
            "isolation_embedded_evidence_missing",
        )
        try:
            validate_both_off(
                evidence["strip_device_evidence"],
                evidence["ray_readback"],
                curve,
            )
        except (OSError, TypeError, ValueError) as exc:
            raise TerminalEvidenceError("isolation_embedded_evidence_drift") from exc


def build_capture_ledger_rows(
    *,
    run_root: str | Path,
    plan: Mapping[str, Any],
    captures: Sequence[Mapping[str, Any]],
    physical_returns: Sequence[Mapping[str, Any]],
    isolation_gates: Sequence[Mapping[str, Any]],
    commands: Sequence[Mapping[str, Any]],
    covariates: Sequence[Mapping[str, Any]],
    run: Mapping[str, Any],
    required_feature_ids: Sequence[str],
) -> list[dict[str, Any]]:
    """Project retained acquisition records into the existing R6 validator."""

    root = Path(run_root).resolve()
    plan_steps = tuple(plan.get("captures", ()))
    _require(
        tuple(str(row.get("capture_id")) for row in plan_steps)
        == thermal.TD_B_R6_CAPTURE_IDS,
        "plan_capture_order_drift",
    )
    _require(
        len(captures) == 16
        and len(physical_returns) == 16
        and len(covariates) == 16,
        "capture_count_drift",
    )
    _validate_command_and_isolation_ledgers(
        plan=plan,
        commands=commands,
        isolation_gates=isolation_gates,
    )
    budgets = plan.get("budgets")
    _require(
        isinstance(budgets, Mapping)
        and isinstance(run, Mapping)
        and budgets.get("formal_cap") == 16
        and budgets.get("ambient_cap") == 0
        and budgets.get("physical_cr3_cap") == 16
        and run.get("schema") == "p7_thermal_diagnostic_run_v2"
        and run.get("experiment_id") == plan.get("experiment_id")
        and run.get("status") in {"running", "complete"}
        and run.get("completed_formal") == 16
        and run.get("accepted_formal_count") == 16
        and run.get("ambient_capture_count") == 0
        and run.get("accepted_ambient_count") == 0
        and run.get("physical_returned_cr3_count") == 16
        and run.get("setup_physical_cr3_count") == 0
        and run.get("physical_cr3_count") == 16,
        "run_budget_accounting_drift",
    )
    physical_by_id = {
        str(row.get("capture_id")): row for row in physical_returns
    }
    _require(len(physical_by_id) == 16, "physical_capture_identity_drift")
    frozen = plan.get("frozen_shutters")
    _require(isinstance(frozen, Mapping), "frozen_shutter_missing")
    cr3_paths: set[str] = set()
    sidecar_paths: set[str] = set()
    remote_capture_ids: set[str] = set()
    remote_request_ids: set[str] = set()
    timing_by_group: dict[tuple[Any, ...], float] = {}
    output: list[dict[str, Any]] = []
    from camera_based_rgbww_optimizer.optimization import (
        measure_p7_thermal_diagnostics as measure,
    )
    for index, (step, retained, covariate) in enumerate(
        zip(plan_steps, captures, covariates, strict=True)
    ):
        capture_id = str(step["capture_id"])
        _require(str(retained.get("capture_id")) == capture_id, "capture_order_drift")
        physical = physical_by_id.get(capture_id)
        _require(isinstance(physical, Mapping), "physical_return_missing")
        capture = retained.get("capture")
        _require(isinstance(capture, Mapping), "capture_payload_missing")
        quality = capture.get("r6_terminal_quality")
        _require(isinstance(quality, Mapping), "quality_projection_missing")
        _require(
            retained.get("source_id") == step.get("source_id")
            and retained.get("state_id") == step.get("state_id")
            and retained.get("capture_role") == step.get("capture_role")
            and retained.get("formal_measurement") is True
            and provenance.json_native_value(retained.get("plan_step"))
            == provenance.json_native_value(step)
            and physical.get("source_id") == step.get("source_id")
            and physical.get("state_id") == step.get("state_id")
            and int(physical.get("physical_index", 0)) == index + 1,
            "capture_physical_plan_identity_drift",
        )
        expected_command = step.get("command") or {"strip": "off", "ray": "off"}
        try:
            thermal.validate_covariate_record(
                covariate,
                expected_command=expected_command,
            )
        except (TypeError, ValueError) as exc:
            raise TerminalEvidenceError("covariate_contract_drift") from exc
        _require(
            covariate.get("source_id") == step.get("source_id")
            and covariate.get("state_id") == step.get("state_id")
            and covariate.get("exact_command_hash") == step.get("exact_command_hash")
            and int(covariate.get("sequence_index", -1))
            == int(str(step["capture_id"]).split("-", 1)[0])
            and int(covariate.get("capture_order", -1))
            == int(str(step["capture_id"]).split("-", 1)[0])
            and int(covariate.get("source_order", -1))
            == int(step.get("source_order", 1)),
            "covariate_plan_identity_drift",
        )
        cache_key = thermal.shutter_cache_key_for_step(step)
        nominal = frozen.get(cache_key) if cache_key is not None else None
        _require(type(nominal) is str and quality.get("nominal_shutter") == nominal,
                 "nominal_shutter_drift")
        cr3_path = str(physical.get("cr3_path", ""))
        sidecar_path = str(physical.get("sidecar_path", ""))
        remote_capture_id = physical.get("remote_capture_id")
        remote_request_id = physical.get("remote_request_id")
        _require(
            bool(cr3_path) and bool(sidecar_path)
            and Path(cr3_path).resolve().is_relative_to(root)
            and Path(sidecar_path).resolve().is_relative_to(root)
            and cr3_path == str(Path(cr3_path).resolve())
            and sidecar_path == str(Path(sidecar_path).resolve()),
            "capture_path_cross_root",
        )
        _require(
            cr3_path not in cr3_paths
            and sidecar_path not in sidecar_paths
            and type(remote_capture_id) is str
            and bool(remote_capture_id)
            and remote_capture_id not in remote_capture_ids
            and type(remote_request_id) is str
            and bool(remote_request_id)
            and remote_request_id not in remote_request_ids,
            "stale_or_duplicate_capture_identity",
        )
        cr3_paths.add(cr3_path)
        sidecar_paths.add(sidecar_path)
        remote_capture_ids.add(remote_capture_id)
        remote_request_ids.add(remote_request_id)
        _validate_retained_capture_file(
            cr3_path,
            root=root,
            expected_bytes=physical.get("cr3_byte_count"),
            expected_sha256=physical.get("cr3_sha256"),
        )
        _validate_retained_capture_file(
            sidecar_path,
            root=root,
            expected_bytes=physical.get("sidecar_byte_count"),
            expected_sha256=physical.get("sidecar_sha256"),
        )
        nested_capture = capture.get("capture")
        expected_receipt = {
            "schema": thermal.PHYSICAL_RETURN_LEDGER_SCHEMA,
            "physical_index": physical.get("physical_index"),
            "capture_id": physical.get("capture_id"),
            "cr3_sha256": physical.get("cr3_sha256"),
            "cr3_byte_count": physical.get("cr3_byte_count"),
            "sidecar_sha256": physical.get("sidecar_sha256"),
            "sidecar_byte_count": physical.get("sidecar_byte_count"),
        }
        _require(
            physical.get("schema") == thermal.PHYSICAL_RETURN_LEDGER_SCHEMA
            and isinstance(nested_capture, Mapping)
            and capture.get("saved_file") == cr3_path
            and nested_capture.get("saved_file") == cr3_path
            and nested_capture.get("byte_count") == physical.get("cr3_byte_count")
            and capture.get("remote_metadata_path") == sidecar_path
            and capture.get("physical_return_receipt") == expected_receipt,
            "capture_payload_physical_identity_drift",
        )
        try:
            sidecar_result = measure._validate_returned_sidecar(
                capture,
                raw_path=Path(cr3_path),
                run_root=root,
            )
        except (OSError, TypeError, ValueError, RuntimeError) as exc:
            raise TerminalEvidenceError("capture_sidecar_association_drift") from exc
        _require(
            all(
                sidecar_result.get(key) == physical.get(key)
                for key in (
                    "sidecar_path", "sidecar_byte_count", "sidecar_sha256",
                    "sidecar_validation_status", "remote_capture_id",
                    "remote_request_id",
                )
            ),
            "capture_sidecar_physical_identity_drift",
        )
        timing = capture.get("timing_evidence")
        remote_metadata = sidecar_result.get("remote_metadata")
        estimate = (
            remote_metadata.get("exposure_start_estimate")
            if isinstance(remote_metadata, Mapping)
            else None
        )
        observed = timing.get("best_effort_elapsed_s") if isinstance(timing, Mapping) else None
        method = estimate.get("method") if isinstance(estimate, Mapping) else None
        requested = float(step["requested_elapsed_s"])
        _require(
            isinstance(timing, Mapping)
            and timing.get("tier") in thermal.ACCEPTED_TIMING_TIERS
            and timing.get("status") == "accepted_best_effort_anchor"
            and timing.get("provenance") == thermal.TIMING_CONTRACT_V2["provenance"]
            and not isinstance(observed, bool)
            and isinstance(observed, (int, float))
            and math.isfinite(float(observed))
            and float(observed) >= 0
            and method in {
                "gphoto_event_minus_recorded_exposure",
                "gphoto_capture_return_minus_recorded_exposure",
            }
            and retained.get("timing_evidence_status") == "accepted"
            and retained.get("nominal_slot_s") == step.get("requested_elapsed_s")
            and retained.get("best_effort_exposure_start_elapsed_s") == observed
            and retained.get("timing_offset_s") == float(observed) - requested
            and retained.get("timing_estimate_method") == method,
            "capture_timing_contract_drift",
        )
        group = thermal.timing_sequence_identity(str(plan["experiment_id"]), step)
        prior_observed = timing_by_group.get(group)
        _require(
            prior_observed is None or float(observed) > prior_observed,
            "capture_timing_chronology_drift",
        )
        timing_by_group[group] = float(observed)
        output.append({
            "capture_id": capture_id,
            "run_root": str(root),
            "origin": "ray_r6",
            "state_id": str(step["state_id"]),
            "nominal_shutter": nominal,
            "exposure_mode": step.get("exposure_mode"),
            "weak_reacquire": step.get("weak_reacquire"),
            "mid_run_shutter_change": step.get("mid_run_shutter_change"),
            "physical_return_persisted_before_postprocessing": (
                int(physical.get("physical_index", 0)) == index + 1
                and physical.get("sidecar_validation_status") == "pass"
            ),
            "cr3": {
                "path": cr3_path,
                "bytes": physical.get("cr3_byte_count"),
                "sha256": physical.get("cr3_sha256"),
            },
            "sidecar": {
                "path": sidecar_path,
                "bytes": physical.get("sidecar_byte_count"),
                "sha256": physical.get("sidecar_sha256"),
            },
            "remote_capture_id": remote_capture_id,
            "remote_request_id": remote_request_id,
            "recorded_exposure": quality.get("recorded_exposure"),
            "nominal_recorded_ratio_gate": quality.get("nominal_recorded_ratio_gate"),
            "ray_command_readback": "pass",
            "strip_zero": "pass",
            "source_isolation": "pass",
            "timing_chronology": (
                "pass" if retained.get("timing_evidence_status") == "accepted" else "fail"
            ),
            "no_stale": "pass",
            "budget_accounting": "pass",
            "feature_quality": quality.get("feature_quality"),
        })
    try:
        thermal.audit_chronology(covariates)
    except (TypeError, ValueError) as exc:
        raise TerminalEvidenceError("covariate_chronology_drift") from exc
    return output


def validate_post_capture_ledger(
    run_root: str | Path,
    plan: Mapping[str, Any],
    *,
    required_feature_ids: Sequence[str] | None = None,
    validator: Callable[..., None] = thermal.validate_td_b_r6_capture_ledger,
) -> list[dict[str, Any]]:
    root = Path(run_root).resolve()
    rows = build_capture_ledger_rows(
        run_root=root,
        plan=plan,
        captures=_read_jsonl(root / "captures.jsonl"),
        physical_returns=_read_jsonl(root / "physical-returns.jsonl"),
        isolation_gates=_read_jsonl(root / "isolation-gates.jsonl"),
        commands=_read_jsonl(root / "commands.jsonl"),
        covariates=_read_jsonl(root / "thermal-covariates.jsonl"),
        run=_strict_json_bytes((root / "run.json").read_bytes()),
        required_feature_ids=required_feature_ids or _required_feature_ids(),
    )
    validator(
        rows,
        required_feature_ids=required_feature_ids or _required_feature_ids(),
        selected_c_shutter="1/2500",
    )
    return rows


def run_independent_final_zero(
    run_root: str | Path,
    *,
    dependencies: IndependentZeroDependencies | None = None,
) -> bool:
    """Perform one both-off/readback pass and persist success or failure."""

    root = provenance.read_existing_root(run_root)
    deps = dependencies or _default_zero_dependencies()
    record: dict[str, Any] = {
        "schema": INDEPENDENT_ZERO_SCHEMA,
        "status": "fail",
        "task": TASK_ID,
        "contract": CONTRACT_ID,
        "strip_nonzero_calls": 0,
        "ray_nonzero_calls": 0,
        "retry": 0,
        "steps": [],
        "completed_at": _utc_now(),
    }
    passed = False
    try:
        steps = all_off.turn_everything_off(
            strip_off_fn=deps.strip_off,
            ray_get_cct_fn=deps.ray_get_cct,
            ray_set_cct_fn=deps.ray_set_cct,
            ray_cct=5600,
            ray_gm=100,
        )
        rows = [step.to_jsonable() for step in steps]
        record["steps"] = rows
        _require(
            len(rows) == 2 and all(row.get("ok") is True for row in rows),
            "independent_all_off_failed",
        )
        strip = rows[0].get("detail", {}).get("payload")
        ray = deps.ray_get_cct()
        _require(isinstance(strip, Mapping) and isinstance(ray, Mapping),
                 "independent_readback_missing")
        deps.validate_both_off(strip, ray, deps.curve())
        record.update({
            "status": "pass",
            "strip_verified_zero": True,
            "ray_verified_zero": True,
            "ray_readback": dict(ray),
        })
        passed = True
    except BaseException as exc:
        record["failure"] = {
            "type": type(exc).__name__,
            "code": getattr(exc, "code", "independent_final_zero_failed"),
            "message": str(exc),
        }
    provenance.persist_canonical_json(root, "independent-final-zero.json", record)
    return passed


def _read_bound_file(root: provenance.DirectoryIdentity, name: str) -> provenance.FileIdentity:
    return provenance.read_exact_file(Path(root.path) / name, root=root)


def _identity(
    value: provenance.FileIdentity,
    *,
    relative_path: str | None = None,
) -> dict[str, Any]:
    return {
        "path": relative_path or Path(value.path).name,
        "bytes": value.byte_count,
        "sha256": value.sha256,
        "device": value.device,
        "inode": value.inode,
        "mode": value.mode,
    }


def _read_retained_artifact(
    path_value: object,
    *,
    root: provenance.DirectoryIdentity,
    expected_bytes: object | None = None,
    expected_sha256: object | None = None,
) -> tuple[str, provenance.FileIdentity]:
    _require(type(path_value) is str and bool(path_value), "artifact_path_missing")
    candidate = Path(path_value)
    root_path = Path(root.path)
    try:
        resolved = candidate.resolve(strict=True)
    except OSError as exc:
        raise TerminalEvidenceError("artifact_resolve_failed") from exc
    _require(
        candidate.is_absolute()
        and not candidate.is_symlink()
        and resolved.is_relative_to(root_path)
        and resolved.is_file()
        and not any(
            parent.is_symlink()
            for parent in resolved.parents
            if parent != root_path.parent
        ),
        "artifact_owner_invalid",
    )
    relative = resolved.relative_to(root_path).as_posix()
    identity = provenance.read_exact_file(
        resolved,
        expected_size=(expected_bytes if type(expected_bytes) is int else None),
        expected_sha256=(expected_sha256 if type(expected_sha256) is str else None),
    )
    _require(provenance.read_existing_root(root.path) == root, "root_identity_drift")
    return relative, identity


def _collect_safe_existing_artifacts(
    root: provenance.DirectoryIdentity,
) -> tuple[dict[str, Any], list[dict[str, str]], set[str]]:
    root_path = Path(root.path)
    artifacts: dict[str, Any] = {}
    unsafe: list[dict[str, str]] = []
    directories: set[str] = set()
    for candidate in root_path.rglob("*"):
        relative = candidate.relative_to(root_path).as_posix()
        try:
            value = candidate.lstat()
        except OSError:
            unsafe.append({"path": relative, "kind": "lstat_failed"})
            continue
        if stat.S_ISLNK(value.st_mode):
            unsafe.append({"path": relative, "kind": "symlink"})
            continue
        if stat.S_ISDIR(value.st_mode):
            directories.add(relative)
            continue
        if not stat.S_ISREG(value.st_mode):
            unsafe.append({"path": relative, "kind": "non_regular"})
            continue
        try:
            identity = provenance.read_exact_file(candidate)
        except provenance.ProvenanceIOError as exc:
            unsafe.append({"path": relative, "kind": exc.code})
            continue
        artifacts[relative] = _identity(identity, relative_path=relative)
    _require(provenance.read_existing_root(root.path) == root, "root_identity_drift")
    return artifacts, unsafe, directories


def _validate_closed_inventory(
    *,
    expected_paths: set[str],
    artifacts: Mapping[str, Any],
    unsafe: Sequence[Mapping[str, str]],
    directories: set[str],
) -> None:
    expected_directories = {
        parent.as_posix()
        for name in expected_paths
        for parent in Path(name).parents
        if parent.as_posix() != "."
    }
    _require(not unsafe, "unsafe_artifact_inventory")
    _require(set(artifacts) == expected_paths, "retained_artifact_inventory_drift")
    _require(directories == expected_directories, "retained_directory_inventory_drift")


def _best_effort_jsonl(
    root: provenance.DirectoryIdentity,
    name: str,
) -> list[Mapping[str, Any]]:
    try:
        return _parse_jsonl_bytes(_read_bound_file(root, name).data)
    except BaseException:
        return []


def _returned_summary(
    *,
    root: provenance.DirectoryIdentity,
    passed: bool,
    captures: Sequence[Mapping[str, Any]],
    physical_returns: Sequence[Mapping[str, Any]],
    counts: Mapping[str, int],
    error_code: str | None,
) -> dict[str, Any]:
    capture_ids = [str(row.get("capture_id", "")) for row in captures]
    returned = []
    for row in physical_returns:
        returned.append({
            "capture_id": row.get("capture_id"),
            "physical_index": row.get("physical_index"),
            "cr3": {
                "path": row.get("cr3_path"),
                "bytes": row.get("cr3_byte_count"),
                "sha256": row.get("cr3_sha256"),
            },
            "sidecar": {
                "path": row.get("sidecar_path"),
                "bytes": row.get("sidecar_byte_count"),
                "sha256": row.get("sidecar_sha256"),
            },
            "remote_capture_id": row.get("remote_capture_id"),
            "remote_request_id": row.get("remote_request_id"),
        })
    return {
        "schema": RETURNED_SUMMARY_SCHEMA,
        "status": "returned_evidence_complete" if passed else "partial_or_invalid",
        "formal_pass": passed,
        "task": TASK_ID,
        "contract": CONTRACT_ID,
        "root": {
            "path": root.path,
            "device": root.device,
            "inode": root.inode,
            "mode": root.mode,
        },
        "capture_ids": capture_ids,
        "expected_capture_ids": list(thermal.TD_B_R6_CAPTURE_IDS),
        "capture_order_exact": tuple(capture_ids) == thermal.TD_B_R6_CAPTURE_IDS,
        "counts": dict(counts),
        "returned": returned,
        "retry": 0,
        "error_code": error_code,
    }


def _read_bound_json(root: provenance.DirectoryIdentity, name: str) -> tuple[dict[str, Any], provenance.FileIdentity]:
    identity = _read_bound_file(root, name)
    value = _strict_json_bytes(identity.data)
    _require(isinstance(value, dict), f"{name}:not_object")
    return value, identity


def finalize_terminal(
    run_root: str | Path,
    *,
    child_exit: int,
    shell_cleanup_exit: int,
    independent_zero_exit: int,
    signal_name: str | None,
    ledger_validator: Callable[..., None] = thermal.validate_td_b_r6_capture_ledger,
) -> bool:
    """Replay one formal root and write one terminal audit plus terminal seal."""

    root = provenance.read_existing_root(run_root)
    _require(FORMAL_ROOT_RE.fullmatch(Path(root.path).name) is not None,
             "formal_root_basename_invalid")
    artifacts, unsafe_inventory, observed_directories = (
        _collect_safe_existing_artifacts(root)
    )
    failed_phase = "terminal_replay"
    error_code: str | None = None
    passed = False
    summary_written = False
    summary_attempted = False
    captures: list[Mapping[str, Any]] = []
    physical_returns: list[Mapping[str, Any]] = []
    counts = {"formal": 0, "physical": 0, "setup": 0, "ambient": 0}
    cleanup_status = {
        "python": "unknown",
        "shell": "unknown",
        "shell_exit": shell_cleanup_exit,
        "independent_zero": "unknown",
        "independent_zero_exit": independent_zero_exit,
    }
    try:
        files = {name: _read_bound_file(root, name) for name in REQUIRED_SUCCESS_FILES}
        artifacts.update({name: _identity(value) for name, value in files.items()})
        plan = _strict_json_bytes(files["plan.json"].data)
        run = _strict_json_bytes(files["run.json"].data)
        python_cleanup = _strict_json_bytes(files["all-off-python.json"].data)
        shell_cleanup = _strict_json_bytes(files["all-off-shell.json"].data)
        independent = _strict_json_bytes(files["independent-final-zero.json"].data)
        commands_audit = _strict_json_bytes(files["commands-audit.json"].data)
        python_cleanup_pass = (
            isinstance(python_cleanup, dict)
            and python_cleanup.get("status") == "pass"
            and isinstance(python_cleanup.get("steps"), list)
            and len(python_cleanup["steps"]) == 2
            and all(step.get("ok") is True for step in python_cleanup["steps"])
        )
        shell_cleanup_pass = (
            shell_cleanup_exit == 0
            and files["all-off-shell.exit-status.txt"].data == b"0\n"
            and isinstance(shell_cleanup, list)
            and len(shell_cleanup) == 2
            and all(step.get("ok") is True for step in shell_cleanup)
        )
        independent_zero_pass = (
            independent_zero_exit == 0
            and isinstance(independent, dict)
            and independent.get("status") == "pass"
            and independent.get("strip_verified_zero") is True
            and independent.get("ray_verified_zero") is True
        )
        cleanup_status.update({
            "python": "pass" if python_cleanup_pass else "fail",
            "shell": "pass" if shell_cleanup_pass else "fail",
            "independent_zero": "pass" if independent_zero_pass else "fail",
        })
        _require(isinstance(plan, dict) and is_r6_materialized_plan(plan),
                 "materialized_plan_invalid")
        from camera_based_rgbww_optimizer.optimization import p7_td_b_r6_stage_gate
        p7_td_b_r6_stage_gate.validate_materialized_runtime_plan(plan)
        _require(isinstance(run, dict), "run_invalid")
        counts = {
            "formal": int(run.get("completed_formal", 0)),
            "physical": int(run.get("physical_returned_cr3_count", 0)),
            "setup": int(run.get("setup_physical_cr3_count", 0)),
            "ambient": int(run.get("ambient_capture_count", 0)),
        }
        _require(
            run.get("status") == "complete"
            and counts == {"formal": 16, "physical": 16, "setup": 0, "ambient": 0},
            "run_counts_or_status_invalid",
        )
        _require(
            isinstance(commands_audit, dict)
            and commands_audit.get("status") == "pass"
            and commands_audit.get("formal_capture_count") == 16
            and commands_audit.get("ambient_capture_count") == 0,
            "commands_audit_invalid",
        )
        _require(python_cleanup_pass, "python_cleanup_invalid")
        _require(shell_cleanup_pass, "shell_cleanup_invalid")
        _require(independent_zero_pass, "independent_zero_invalid")
        _require(
            child_exit == 0
            and signal_name is None
            and files["child-exit-status.txt"].data == b"0\n",
            "child_or_signal_invalid",
        )
        required_feature_ids = _required_feature_ids()
        captures = _parse_jsonl_bytes(files["captures.jsonl"].data)
        physical_returns = _parse_jsonl_bytes(files["physical-returns.jsonl"].data)
        isolation_gates = _parse_jsonl_bytes(files["isolation-gates.jsonl"].data)
        covariates = _parse_jsonl_bytes(files["thermal-covariates.jsonl"].data)
        commands = _parse_jsonl_bytes(files["commands.jsonl"].data)
        _require(len(covariates) == 16 and bool(commands), "measurement_ledger_count_invalid")
        rows = build_capture_ledger_rows(
            run_root=root.path,
            plan=plan,
            captures=captures,
            physical_returns=physical_returns,
            isolation_gates=isolation_gates,
            commands=commands,
            covariates=covariates,
            run=run,
            required_feature_ids=required_feature_ids,
        )
        ledger_validator(
            rows,
            required_feature_ids=required_feature_ids,
            selected_c_shutter="1/2500",
        )
        expected_paths = set(REQUIRED_SUCCESS_FILES)
        for retained, row in zip(captures, rows, strict=True):
            for kind in ("cr3", "sidecar"):
                relative, identity = _read_retained_artifact(
                    row[kind]["path"],
                    root=root,
                    expected_bytes=row[kind]["bytes"],
                    expected_sha256=row[kind]["sha256"],
                )
                _require(relative not in expected_paths, "artifact_path_duplicate")
                expected_paths.add(relative)
                artifacts[relative] = _identity(identity, relative_path=relative)
            capture = retained.get("capture")
            _require(isinstance(capture, Mapping), "capture_payload_missing")
            relative, report_identity = _read_retained_artifact(
                capture.get("patch_statistics"),
                root=root,
            )
            _require(relative not in expected_paths, "artifact_path_duplicate")
            report = _strict_json_bytes(report_identity.data)
            _require(isinstance(report, Mapping), "measurement_report_invalid")
            projected = project_quality_capture(
                report,
                capture_id=str(retained["capture_id"]),
                required_feature_ids=required_feature_ids,
                nominal_shutter=str(row["nominal_shutter"]),
            )
            _require(
                provenance.json_native_value(capture.get("r6_terminal_quality"))
                == provenance.json_native_value(projected),
                "quality_projection_report_drift",
            )
            expected_paths.add(relative)
            artifacts[relative] = _identity(
                report_identity,
                relative_path=relative,
            )
        _validate_closed_inventory(
            expected_paths=expected_paths,
            artifacts=artifacts,
            unsafe=unsafe_inventory,
            directories=observed_directories,
        )
        summary_attempted = True
        summary_identity = provenance.persist_canonical_json(
            root,
            "returned-summary.json",
            _returned_summary(
                root=root,
                passed=True,
                captures=captures,
                physical_returns=physical_returns,
                counts=counts,
                error_code=None,
            ),
        )
        summary_written = True
        expected_paths.add("returned-summary.json")
        artifacts["returned-summary.json"] = _identity(summary_identity)
        _validate_closed_inventory(
            expected_paths=expected_paths,
            artifacts=artifacts,
            unsafe=unsafe_inventory,
            directories=observed_directories,
        )
        passed = True
        failed_phase = "none"
    except BaseException as exc:
        error_code = str(getattr(exc, "code", type(exc).__name__))

    if not summary_written and not summary_attempted:
        if not captures:
            captures = _best_effort_jsonl(root, "captures.jsonl")
        if not physical_returns:
            physical_returns = _best_effort_jsonl(root, "physical-returns.jsonl")
        try:
            partial_run = _strict_json_bytes(_read_bound_file(root, "run.json").data)
            if isinstance(partial_run, Mapping):
                counts = {
                    "formal": int(partial_run.get("completed_formal", 0)),
                    "physical": int(partial_run.get("physical_returned_cr3_count", 0)),
                    "setup": int(partial_run.get("setup_physical_cr3_count", 0)),
                    "ambient": int(partial_run.get("ambient_capture_count", 0)),
                }
        except BaseException:
            pass
        summary_attempted = True
        summary_identity = provenance.persist_canonical_json(
            root,
            "returned-summary.json",
            _returned_summary(
                root=root,
                passed=False,
                captures=captures,
                physical_returns=physical_returns,
                counts=counts,
                error_code=error_code,
            ),
        )
        artifacts["returned-summary.json"] = _identity(summary_identity)

    status = "pass" if passed else "accepted_hard_failed_formal_attempt"
    audit = {
        "schema": TERMINAL_AUDIT_SCHEMA,
        "status": status,
        "formal_pass": passed,
        "task": TASK_ID,
        "contract": CONTRACT_ID,
        "root": {
            "path": root.path, "device": root.device, "inode": root.inode,
            "mode": root.mode,
        },
        "counts": counts,
        "retry": 0,
        "alternate_root": 0,
        "launch": 1,
        "strip_call_count": 0,
        "analysis_call_count": 0,
        "cleanup": cleanup_status,
        "inventory": {
            "status": "pass" if passed else "rejected",
            "safe_bound_count": len(artifacts),
            "unsafe_unbound": unsafe_inventory,
            "observed_directories": sorted(observed_directories),
        },
        "child_exit": child_exit,
        "signal": signal_name,
        "failed_phase": failed_phase,
        "error_code": error_code,
        "artifacts": artifacts,
        "completed_at": _utc_now(),
    }
    audit_identity = provenance.persist_canonical_json(
        root, "terminal-audit.json", audit,
    )
    seal = {
        "schema": TERMINAL_SEAL_SCHEMA,
        "status": "PASS" if passed else "FAIL",
        "formal_pass": passed,
        "task": TASK_ID,
        "contract": CONTRACT_ID,
        "root": audit["root"],
        "formal_count": counts["formal"],
        "physical_count": counts["physical"],
        "setup_count": counts["setup"],
        "ambient_count": counts["ambient"],
        "retry": 0,
        "alternate_root": 0,
        "launch": 1,
        "strip_call_count": 0,
        "analysis_call_count": 0,
        "cleanup": audit["cleanup"],
        "inventory": audit["inventory"],
        "failed_phase": failed_phase,
        "error_code": error_code,
        "artifact_identities": {
            **artifacts,
            "terminal-audit.json": _identity(audit_identity),
        },
    }
    provenance.persist_canonical_json(root, "terminal-seal.json", seal)
    return passed


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Ray R6 formal terminal evidence owner")
    subparsers = parser.add_subparsers(dest="command", required=True)
    classify = subparsers.add_parser("classify-wrapper")
    classify.add_argument("runner_argv", nargs=argparse.REMAINDER)
    zero = subparsers.add_parser("independent-final-zero")
    zero.add_argument("--run-dir", required=True)
    finalize = subparsers.add_parser("finalize")
    finalize.add_argument("--run-dir", required=True)
    finalize.add_argument("--child-exit", required=True, type=int)
    finalize.add_argument("--shell-cleanup-exit", required=True, type=int)
    finalize.add_argument("--independent-zero-exit", required=True, type=int)
    finalize.add_argument("--signal", default="")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        if args.command == "classify-wrapper":
            values = tuple(args.runner_argv)
            if values[:1] == ("--",):
                values = values[1:]
            print(classify_wrapper_argv(values))
            return 0
        if args.command == "independent-final-zero":
            return 0 if run_independent_final_zero(args.run_dir) else 1
        return 0 if finalize_terminal(
            args.run_dir,
            child_exit=args.child_exit,
            shell_cleanup_exit=args.shell_cleanup_exit,
            independent_zero_exit=args.independent_zero_exit,
            signal_name=args.signal or None,
        ) else 1
    except (TerminalEvidenceError, provenance.ProvenanceIOError, ValueError) as exc:
        print(str(exc))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
