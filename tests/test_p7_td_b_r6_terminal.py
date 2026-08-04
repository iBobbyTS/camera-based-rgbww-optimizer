from __future__ import annotations

import copy
import hashlib
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest import mock

from camera_based_rgbww_optimizer.optimization import p7_td_b_r6_stage_gate as stage_gate
from camera_based_rgbww_optimizer.optimization import p7_td_b_r6_terminal as subject
from camera_based_rgbww_optimizer.optimization import p7_thermal_diagnostics as thermal
from camera_based_rgbww_optimizer.optimization.hsi_source_evidence import (
    expected_strip_payloads,
)
from camera_based_rgbww_optimizer.control import ray120c
from camera_based_rgbww_optimizer.control import camera_remote_v2


TEST_ROOT = Path("/Volumes/4T/temp/rgbww-optimizer/g4-r6-terminal-tests")


def temporary_directory():
    TEST_ROOT.mkdir(parents=True, exist_ok=True)
    return tempfile.TemporaryDirectory(dir=TEST_ROOT)


def write_json(path: Path, value) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    path.chmod(0o600)


def write_jsonl(path: Path, rows) -> None:
    path.write_text(
        "".join(json.dumps(row, sort_keys=True) + "\n" for row in rows),
        encoding="utf-8",
    )
    path.chmod(0o600)


def materialized_plan(basename: str) -> dict:
    template = stage_gate.build_runtime_plan_template()
    attestation = {
        "schema": stage_gate.COMMITTED_SOURCE_ATTESTATION_SCHEMA,
        "verified_parent_checkpoint": "1" * 40,
        "verified_parent_tree": "2" * 40,
        "code_owner_checkpoint": "3" * 40,
        "code_owner_tree": "4" * 40,
        "live_activation_checkpoint": "5" * 40,
        "live_activation_tree": "6" * 40,
        "candidate_references_sha256": "7" * 64,
        "post_child_changed_paths": [".agent-work/PLAN.md"],
        "post_child_commits": [{
            "parent_checkpoint": "3" * 40,
            "child_checkpoint": "5" * 40,
            "child_tree": "6" * 40,
            "changed_paths": [".agent-work/PLAN.md"],
        }],
    }
    activation = {
        "descriptor_sha256": "8" * 64,
        "template_sha256": stage_gate.runtime_plan_template_sha256(template),
        "committed_source_attestation": attestation,
        "formal_root_basename": basename,
    }
    plan = stage_gate._materialized_projection(template, activation)
    stage_gate.validate_materialized_runtime_plan(plan)
    return plan


def feature_ids() -> tuple[str, ...]:
    policy = json.loads(thermal.POLICY_PATH.read_text(encoding="utf-8"))
    return tuple(policy["feature_set"]["ids"])


def fixture_command_groups(plan: dict) -> list[list[dict]]:
    groups = []
    for step in plan["captures"]:
        key = thermal.timing_sequence_identity(plan["experiment_id"], step)
        previous_key = (
            None
            if not groups
            else thermal.timing_sequence_identity(
                plan["experiment_id"], groups[-1][0],
            )
        )
        if (
            groups
            and key == previous_key
            and step["requested_elapsed_s"] > groups[-1][-1]["requested_elapsed_s"]
        ):
            groups[-1].append(step)
        else:
            groups.append([step])
    return groups


def fixture_control_ledgers(plan: dict):
    groups = fixture_command_groups(plan)
    commands = [
        {
            "at": f"2026-08-04T15:00:{index:02d}Z",
            "event": "command_readback_verified",
            "source_id": group[0]["source_id"],
            "state_id": group[0]["state_id"],
            "exact_command_hash": group[0]["exact_command_hash"],
            "applied": {"data": {
                "hue": int(group[0]["command"]["hue"]),
                "sat": int(group[0]["command"]["sat"]),
                "intensity": ray120c.intensity_percent_to_raw(
                    float(group[0]["command"]["intensity_percent"]),
                ),
            }},
            "readback": {"data": {
                "hue": int(group[0]["command"]["hue"]),
                "sat": int(group[0]["command"]["sat"]),
                "intensity": ray120c.intensity_percent_to_raw(
                    float(group[0]["command"]["intensity_percent"]),
                ),
            }},
        }
        for index, group in enumerate(groups)
    ]
    gate_ids = [
        "run_start",
        *(group[-1]["isolation_gate_after"] for group in groups),
    ]
    curve = json.loads(thermal.CURVE_PATH.read_text(encoding="utf-8"))
    _raw, off_payload = expected_strip_payloads(
        {channel: 0 for channel in thermal.CHANNELS},
        curve,
    )
    gates = [
        {
            "gate_id": gate_id,
            "evidence": {
                "status": "pass",
                "gate_id": gate_id,
                "strip_verified_off": True,
                "ray_verified_off": True,
                "strip_device_evidence": {
                    "schema_version": 1,
                    "requested_payload": off_payload,
                    "baseline_snapshot": {
                        "schema_version": 1,
                        "generation": index * 2 + 1,
                        **off_payload,
                    },
                    "device_snapshot": {
                        "schema_version": 1,
                        "generation": index * 2 + 2,
                        **off_payload,
                    },
                    "device_state_entity": {
                        "object_id": "rgbww_commanded_state",
                        "key": 1,
                    },
                    "device_identity": {
                        "name": "bedroom-rgbww-strip",
                        "mac_address": "00:11:22:33:44:55",
                    },
                },
                "ray_off_command": {"code": 0},
                "ray_readback": {"data": {"intensity": 0}},
            },
            "at": f"2026-08-04T15:01:{index:02d}Z",
        }
        for index, gate_id in enumerate(gate_ids)
    ]
    run = {
        "schema": "p7_thermal_diagnostic_run_v2",
        "experiment_id": plan["experiment_id"],
        "status": "complete",
        "completed_formal": 16,
        "accepted_formal_count": 16,
        "ambient_capture_count": 0,
        "accepted_ambient_count": 0,
        "physical_returned_cr3_count": 16,
        "setup_physical_cr3_count": 0,
        "physical_cr3_count": 16,
        "cleanup": "pass",
    }
    return commands, gates, run


def fixture_rows(root: Path, plan: dict):
    ids = feature_ids()
    expected_values = {
        feature_id: float(offset + 1)
        for offset, feature_id in enumerate(ids)
    }
    patch_names = tuple(dict.fromkeys(
        feature_id.split("::", 1)[0] for feature_id in ids
    ))
    captures = []
    physical = []
    covariates = []
    for index, step in enumerate(plan["captures"], start=1):
        capture_id = step["capture_id"]
        cr3 = root / "camera" / f"{capture_id}.CR3"
        sidecar = root / "camera" / f"{capture_id}.CR3.metadata.json"
        cr3.parent.mkdir(exist_ok=True)
        cr3.write_bytes(f"raw-{capture_id}".encode())
        cache_key = thermal.shutter_cache_key_for_step(step)
        nominal = plan["frozen_shutters"][cache_key]
        seconds = 1 / int(nominal.split("/", 1)[1])
        observed = float(step["requested_elapsed_s"])
        request_ns = 1_000_000_000
        estimate_ns = request_ns + int(observed * 1_000_000_000)
        metadata = {
            "schema": "remote_capture_result_v2",
            "capture_id": f"remote-{index}",
            "request_id": f"request-{index}",
            "timing_quality": "best_effort_gphoto2",
            "formal_p7_eligibility": "unchanged_requires_later_planner_advisor_decision",
            "cr3": {
                "sha256": hashlib.sha256(cr3.read_bytes()).hexdigest(),
                "byte_count": cr3.stat().st_size,
                "content_type": "image/x-canon-cr3",
            },
            "gphoto2": {
                "driver_event_type": None,
                "event_sequence": [],
                "request_received_monotonic_ns": request_ns,
                "capture_call_started_monotonic_ns": request_ns,
                "capture_call_returned_monotonic_ns": (
                    estimate_ns + int(seconds * 1_000_000_000)
                ),
                "camera_event_observed_monotonic_ns": None,
                "file_added_observed_monotonic_ns": None,
                "download_started_monotonic_ns": estimate_ns + 20_000_000,
                "download_completed_monotonic_ns": estimate_ns + 30_000_000,
                "cr3_saved_observed_monotonic_ns": estimate_ns + 40_000_000,
                "clock_domain": "bridge_monotonic",
            },
            "recorded_exposure": {
                "seconds": seconds,
                "source": "Canon:ExposureTime",
                "status": "recorded",
            },
            "exposure_start_estimate": {
                "timestamp_monotonic_ns": estimate_ns,
                "clock_domain": "bridge_monotonic",
                "method": "gphoto_capture_return_minus_recorded_exposure",
                "status": "weak_estimate",
                "uncertainty_ms": None,
                "uncertainty_basis": "unknown",
            },
            "network_observation": {
                "request_id": f"request-{index}",
                "response_or_event_round_trip_ms": None,
                "uncertainty_ms": None,
                "uncertainty_basis": "unknown",
            },
            "bridge_utc_observation": {
                "request_received": "2026-08-04T15:00:00+00:00",
                "source": "bridge_system_clock_utc",
            },
        }
        timing = camera_remote_v2.reconstruct_best_effort_timing(
            metadata,
            local_request_started_monotonic_s=0.0,
            local_response_received_monotonic_s=max(1.0, observed + 1.0),
            local_readback_done_monotonic_s=0.0,
        )
        metadata["_local_receipt"] = {
            "parser_version": camera_remote_v2.PARSER_VERSION,
            "response_headers": {
                "content-type": "multipart/mixed; boundary=fake",
                "content-length": "1000",
                "x-capture-id": f"remote-{index}",
                "x-request-id": f"request-{index}",
                "x-capture-metadata-schema": camera_remote_v2.SCHEMA,
            },
            "multipart_body_byte_count": 1000,
            "multipart_body_sha256": "a" * 64,
            "http_attempts": 1,
            "successful_attempt_index": 1,
            "local_request_started_monotonic_s": 0.0,
            "local_response_received_monotonic_s": max(1.0, observed + 1.0),
            "received_monotonic_s": max(1.0, observed + 1.0),
            "timing_evidence": timing,
        }
        sidecar.write_text(json.dumps(metadata), encoding="utf-8")
        report_path = root / "measurements" / f"{capture_id}.patch-statistics.json"
        report_path.parent.mkdir(exist_ok=True)
        write_json(report_path, {
            "schema_version": 1,
            "measurement": "native_bayer_patch_statistics",
            "source": {"path": str(cr3)},
            "location_config": {"sha256": "synthetic-location"},
            "mosaic": {"plane_order": ["R", "G1", "G2", "B"]},
            "exposure_metadata": {
                "seconds": seconds,
                "source": "Canon:ExposureTime",
                "status": "recorded",
            },
            "analysis_context": {"capture_id": capture_id},
            "patches": [
                {
                    "name": patch_name,
                    "optimization_eligible": True,
                    "planes": {
                        plane: {
                            "quality": {"status": "accepted"},
                            "metrics": {
                                "valid_pixel_count": 30_000,
                                "nonfinite_fraction": 0.0,
                                "clipped_fraction": 0.0,
                                "near_noise_floor_fraction": 0.0,
                            },
                            "statistics": {
                                "normalized_per_second": {
                                    "trimmed_mean": expected_values.get(
                                        f"{patch_name}::{plane}", 1.0,
                                    ),
                                },
                            },
                        }
                        for plane in ("R", "G1", "G2", "B")
                    },
                }
                for patch_name in patch_names
            ],
        })
        captures.append({
            "capture_id": capture_id,
            "source_id": step["source_id"],
            "state_id": step["state_id"],
            "capture_role": step["capture_role"],
            "formal_measurement": True,
            "plan_step": dict(step),
            "timing_evidence_status": "accepted",
            "nominal_slot_s": step["requested_elapsed_s"],
            "best_effort_exposure_start_elapsed_s": timing["best_effort_elapsed_s"],
            "timing_offset_s": (
                float(timing["best_effort_elapsed_s"])
                - float(step["requested_elapsed_s"])
            ),
            "timing_estimate_method": "gphoto_capture_return_minus_recorded_exposure",
            "timing_evidence": dict(timing),
            "capture": {
                "capture": {
                    "backend": "remote",
                    "saved_file": str(cr3.resolve()),
                    "byte_count": cr3.stat().st_size,
                },
                "saved_file": str(cr3.resolve()),
                "remote_metadata_path": str(sidecar.resolve()),
                "timing_metadata": metadata,
                "timing_evidence": timing,
                "physical_capture_count": 1,
                "physical_return_receipt": {
                    "schema": thermal.PHYSICAL_RETURN_LEDGER_SCHEMA,
                    "physical_index": index,
                    "capture_id": capture_id,
                    "cr3_sha256": hashlib.sha256(cr3.read_bytes()).hexdigest(),
                    "cr3_byte_count": cr3.stat().st_size,
                    "sidecar_sha256": hashlib.sha256(sidecar.read_bytes()).hexdigest(),
                    "sidecar_byte_count": sidecar.stat().st_size,
                },
                "patch_statistics": str(report_path.resolve()),
                "r6_terminal_quality": {
                    "capture_id": capture_id,
                    "nominal_shutter": nominal,
                    "recorded_exposure": {
                        "seconds": seconds,
                        "source": "Canon:ExposureTime",
                        "status": "recorded",
                    },
                    "nominal_recorded_ratio_gate": "pass",
                    "feature_quality": {
                        feature_id: {
                            "value": float(offset + 1),
                            "clipped_fraction": 0.0,
                            "near_noise_floor_fraction": 0.0,
                            "valid_pixel_count": 30_000,
                        }
                        for offset, feature_id in enumerate(ids)
                    },
                },
            },
        })
        physical.append({
            "schema": thermal.PHYSICAL_RETURN_LEDGER_SCHEMA,
            "physical_index": index,
            "capture_id": capture_id,
            "source_id": step["source_id"],
            "state_id": step["state_id"],
            "cr3_path": str(cr3.resolve()),
            "cr3_byte_count": cr3.stat().st_size,
            "cr3_sha256": hashlib.sha256(cr3.read_bytes()).hexdigest(),
            "sidecar_path": str(sidecar.resolve()),
            "sidecar_byte_count": sidecar.stat().st_size,
            "sidecar_sha256": hashlib.sha256(sidecar.read_bytes()).hexdigest(),
            "sidecar_validation_status": "pass",
            "remote_capture_id": f"remote-{index}",
            "remote_request_id": f"request-{index}",
        })
        command = step["command"]
        covariates.append(thermal.build_covariate_record(
            source_id=step["source_id"],
            state_id=step["state_id"],
            command=command,
            sequence_index=int(capture_id.split("-", 1)[0]),
            capture_order=int(capture_id.split("-", 1)[0]),
            source_order=int(step.get("source_order", 1)),
            monotonic_timestamp_ns=index,
            wall_clock_timestamp=f"2026-08-04T15:02:{index:02d}Z",
            session_elapsed_s=float(index),
            source_on_elapsed_s=observed,
            state_on_elapsed_s=observed,
            off_duration_before_s=0.0,
            previous_state_id=None,
            previous_state_dwell_s=None,
            shutter_seconds=seconds,
            raw_black_levels=[0.0, 0.0, 0.0, 0.0],
            raw_white_level=65535.0,
            load_history={60: 1.0, 300: 1.0, 900: 1.0},
            readback={"data": {"hue": command["hue"]}},
        ))
    commands, gates, run = fixture_control_ledgers(plan)
    return captures, physical, gates, commands, covariates, run


def pass_steps():
    return [
        {"name": "esphome", "ok": True, "detail": {}, "error": None},
        {"name": "ray120c", "ok": True, "detail": {}, "error": None},
    ]


def build_terminal_root(parent: Path):
    basename = "p7-td-b-formal-r6-abcdef123456-20260804T150000Z"
    root = parent / basename
    root.mkdir(mode=0o700)
    root.chmod(0o700)
    plan = materialized_plan(basename)
    captures, physical, gates, commands, covariates, run = fixture_rows(root, plan)
    write_json(root / "plan.json", plan)
    write_json(root / "run.json", run)
    write_json(root / "all-off-python.json", {"status": "pass", "steps": pass_steps()})
    write_json(root / "all-off-shell.json", pass_steps())
    (root / "all-off-shell.stderr.log").write_bytes(b"")
    (root / "all-off-shell.stderr.log").chmod(0o600)
    (root / "all-off-shell.exit-status.txt").write_text("0\n", encoding="utf-8")
    (root / "all-off-shell.exit-status.txt").chmod(0o600)
    (root / "child-exit-status.txt").write_text("0\n", encoding="utf-8")
    (root / "child-exit-status.txt").chmod(0o600)
    write_json(root / "commands-audit.json", {
        "status": "pass", "formal_capture_count": 16, "ambient_capture_count": 0,
    })
    write_jsonl(root / "captures.jsonl", captures)
    write_jsonl(root / "physical-returns.jsonl", physical)
    write_jsonl(root / "isolation-gates.jsonl", gates)
    write_jsonl(root / "commands.jsonl", commands)
    write_jsonl(root / "thermal-covariates.jsonl", covariates)
    return root, plan, captures, physical, gates, commands, covariates, run


def drift_first_retained_timing(root: Path) -> None:
    rows = [
        json.loads(line)
        for line in (root / "captures.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    rows[0]["capture"]["timing_evidence"]["best_effort_elapsed_s"] = 999.0
    write_jsonl(root / "captures.jsonl", rows)


class TerminalOwnerTests(unittest.TestCase):
    def test_exact_wrapper_classifier_and_near_misses(self):
        exact = (
            "--experiment-id", thermal.TD_B,
            "--source", "ray",
            "--phase", "formal",
            "--stage-gate-package", "/offline/stage-gate",
            "--code-checkpoint", "a" * 40,
        )
        self.assertEqual(subject.classify_wrapper_argv(exact), "r6")
        near_misses = (
            exact[:-2],
            (*exact, "--dry-run"),
            tuple("strip" if value == "ray" else value for value in exact),
            tuple("setup" if value == "formal" else value for value in exact),
            tuple(f"{thermal.TD_B}-similar" if value == thermal.TD_B else value for value in exact),
        )
        for argv in near_misses:
            with self.subTest(argv=argv):
                self.assertEqual(subject.classify_wrapper_argv(argv), "legacy")
        with self.assertRaisesRegex(subject.TerminalEvidenceError, "wrapper_duplicate_option"):
            subject.classify_wrapper_argv((*exact, "--phase", "formal"))
        for conflict in ("--execute", "--allow-device-control", "--output-dir", "--run-name"):
            with self.subTest(conflict=conflict), self.assertRaisesRegex(
                subject.TerminalEvidenceError,
                "wrapper_owned_option_conflict",
            ):
                subject.classify_wrapper_argv((*exact, conflict, "/conflict"))

    def test_capture_projection_passes_existing_validator_and_negative_matrix(self):
        with temporary_directory() as temporary:
            root = Path(temporary) / "run"
            root.mkdir()
            plan = stage_gate.build_runtime_plan_template()
            captures, physical, gates, commands, covariates, run = fixture_rows(root, plan)
            rows = subject.build_capture_ledger_rows(
                run_root=root,
                plan=plan,
                captures=captures,
                physical_returns=physical,
                isolation_gates=gates,
                commands=commands,
                covariates=covariates,
                run=run,
                required_feature_ids=feature_ids(),
            )
            thermal.validate_td_b_r6_capture_ledger(
                rows, required_feature_ids=feature_ids(), selected_c_shutter="1/2500",
            )
            mutations = {
                "missing": lambda value: value.pop(),
                "reordered": lambda value: value.__setitem__(slice(0, 2), [value[1], value[0]]),
                "cross_root": lambda value: value[0].__setitem__("run_root", "/other"),
                "r5_origin": lambda value: value[0].__setitem__("origin", "ray_r5"),
                "wrong_shutter": lambda value: value[0].__setitem__("nominal_shutter", "1/2"),
                "quality": lambda value: value[0]["feature_quality"][feature_ids()[0]].__setitem__("clipped_fraction", 1.0),
                "physical_return": lambda value: value[0].__setitem__("physical_return_persisted_before_postprocessing", False),
            }
            for name, mutate in mutations.items():
                altered = json.loads(json.dumps(rows))
                mutate(altered)
                with self.subTest(name=name), self.assertRaises(ValueError):
                    thermal.validate_td_b_r6_capture_ledger(
                        altered,
                        required_feature_ids=feature_ids(),
                        selected_c_shutter="1/2500",
                    )

            evidence_mutations = {
                "missing_command": lambda value: value[3].pop(),
                "wrong_nonempty_readback": lambda value: value[3][0]["readback"]["data"].__setitem__("intensity", 1),
                "missing_isolation_gate": lambda value: value[2].pop(),
                "embedded_ray_not_off": lambda value: value[2][0]["evidence"]["ray_readback"]["data"].__setitem__("intensity", 1),
                "embedded_strip_drift": lambda value: value[2][0]["evidence"]["strip_device_evidence"]["device_snapshot"].__setitem__("red", 1),
                "duplicate_remote_capture": lambda value: value[1][1].__setitem__("remote_capture_id", value[1][0]["remote_capture_id"]),
                "physical_index": lambda value: value[1][0].__setitem__("physical_index", 2),
                "covariate_tamper": lambda value: value[4][0].__setitem__(
                    "exact_command_hash", "0" * 64,
                ),
                "missing_covariate": lambda value: value[4].pop(),
                "accepted_timing_payload_drift": lambda value: value[0][0]["capture"][
                    "timing_evidence"
                ].__setitem__("best_effort_elapsed_s", 999.0),
                "run_budget": lambda value: value[5].__setitem__("physical_cr3_count", 15),
            }
            for name, mutate in evidence_mutations.items():
                evidence = copy.deepcopy(
                    (captures, physical, gates, commands, covariates, run)
                )
                mutate(evidence)
                with self.subTest(evidence=name), self.assertRaises(
                    subject.TerminalEvidenceError,
                ):
                    subject.build_capture_ledger_rows(
                        run_root=root,
                        plan=plan,
                        captures=evidence[0],
                        physical_returns=evidence[1],
                        isolation_gates=evidence[2],
                        commands=evidence[3],
                        covariates=evidence[4],
                        run=evidence[5],
                        required_feature_ids=feature_ids(),
                    )

    def test_independent_final_zero_writes_pass_and_failure_evidence(self):
        for pass_zero in (True, False):
            with self.subTest(pass_zero=pass_zero), temporary_directory() as temporary:
                root = Path(temporary) / "p7-td-b-formal-r6-abcdef123456-20260804T150000Z"
                root.mkdir(mode=0o700)
                root.chmod(0o700)
                calls = []

                def validate(strip, ray, curve):
                    calls.append((strip, ray, curve))
                    if not pass_zero:
                        raise ValueError("not zero")

                dependencies = subject.IndependentZeroDependencies(
                    strip_off=lambda: {"channels": [0, 0, 0, 0, 0]},
                    ray_set_cct=lambda *_args, **_kwargs: {"code": 0},
                    ray_get_cct=lambda *_args, **_kwargs: {"data": {"intensity": 0}},
                    curve=lambda: {"curve": "fake"},
                    validate_both_off=validate,
                )
                self.assertEqual(
                    subject.run_independent_final_zero(root, dependencies=dependencies),
                    pass_zero,
                )
                record = json.loads((root / "independent-final-zero.json").read_text())
                self.assertEqual(record["status"], "pass" if pass_zero else "fail")
                self.assertEqual(len(calls), 1)
                self.assertEqual(record["retry"], 0)

    def test_terminal_finalize_writes_unique_pass_seal_and_replays_ledger_once(self):
        with temporary_directory() as temporary:
            root, _plan, _captures, _physical, _gates, _commands, _covariates, _run = (
                build_terminal_root(Path(temporary))
            )
            subject.run_independent_final_zero(
                root,
                dependencies=subject.IndependentZeroDependencies(
                    strip_off=lambda: {"channels": [0, 0, 0, 0, 0]},
                    ray_set_cct=lambda *_args, **_kwargs: {"code": 0},
                    ray_get_cct=lambda *_args, **_kwargs: {"data": {"intensity": 0}},
                    curve=lambda: {},
                    validate_both_off=lambda *_args: None,
                ),
            )
            calls = []

            def validator(rows, **kwargs):
                calls.append(tuple(row["capture_id"] for row in rows))
                thermal.validate_td_b_r6_capture_ledger(rows, **kwargs)

            self.assertTrue(subject.finalize_terminal(
                root,
                child_exit=0,
                shell_cleanup_exit=0,
                independent_zero_exit=0,
                signal_name=None,
                ledger_validator=validator,
            ))
            self.assertEqual(calls, [thermal.TD_B_R6_CAPTURE_IDS])
            audit = json.loads((root / "terminal-audit.json").read_text())
            seal = json.loads((root / "terminal-seal.json").read_text())
            self.assertTrue(audit["formal_pass"])
            self.assertEqual(seal["status"], "PASS")
            self.assertEqual(seal["formal_count"], 16)
            self.assertEqual(seal["physical_count"], 16)
            self.assertEqual(seal["analysis_call_count"], 0)
            self.assertIn("terminal-audit.json", seal["artifact_identities"])
            self.assertIn("returned-summary.json", seal["artifact_identities"])
            summary = json.loads((root / "returned-summary.json").read_text())
            self.assertEqual(summary["status"], "returned_evidence_complete")
            self.assertTrue(summary["formal_pass"])
            self.assertTrue(summary["capture_order_exact"])
            self.assertEqual(tuple(summary["capture_ids"]), thermal.TD_B_R6_CAPTURE_IDS)
            self.assertEqual(len(summary["returned"]), 16)
            self.assertEqual(summary["root"], seal["root"])
            self.assertEqual(summary["retry"], 0)
            first_capture = thermal.TD_B_R6_CAPTURE_IDS[0]
            self.assertIn(f"camera/{first_capture}.CR3", seal["artifact_identities"])
            self.assertIn(
                f"measurements/{first_capture}.patch-statistics.json",
                seal["artifact_identities"],
            )
            with self.assertRaises(Exception):
                subject.finalize_terminal(
                    root,
                    child_exit=0,
                    shell_cleanup_exit=0,
                    independent_zero_exit=0,
                    signal_name=None,
                )

    def test_terminal_finalize_hard_failures_never_write_pass(self):
        cases = {
            "python_cleanup": lambda root: write_json(
                root / "all-off-python.json", {"status": "fail", "steps": pass_steps()}
            ),
            "shell_cleanup": lambda root: (root / "all-off-shell.exit-status.txt").write_text("1\n"),
            "missing_artifact": lambda root: (root / "commands-audit.json").unlink(),
            "symlink_artifact": lambda root: (
                (root / "commands-audit.json").unlink(),
                (root / "commands-audit.json").symlink_to(root / "run.json"),
            ),
            "identity_drift": lambda root: (root / "camera" / f"{thermal.TD_B_R6_CAPTURE_IDS[0]}.CR3").write_bytes(b"drift"),
            "extra_artifact": lambda root: (root / "unexpected.txt").write_text("extra\n"),
            "extra_empty_directory": lambda root: (root / "unexpected-dir").mkdir(),
            "special_node": lambda root: os.mkfifo(root / "unexpected-fifo"),
            "timing_payload_drift": drift_first_retained_timing,
        }
        for name, mutate in cases.items():
            with self.subTest(name=name), temporary_directory() as temporary:
                root, _plan, _captures, _physical, _gates, _commands, _covariates, _run = (
                    build_terminal_root(Path(temporary))
                )
                write_json(root / "independent-final-zero.json", {
                    "schema": subject.INDEPENDENT_ZERO_SCHEMA,
                    "status": "pass",
                    "strip_verified_zero": True,
                    "ray_verified_zero": True,
                })
                mutate(root)
                self.assertFalse(subject.finalize_terminal(
                    root,
                    child_exit=0,
                    shell_cleanup_exit=0,
                    independent_zero_exit=0,
                    signal_name=None,
                ))
                seal = json.loads((root / "terminal-seal.json").read_text())
                self.assertEqual(seal["status"], "FAIL")
                self.assertFalse(seal["formal_pass"])
                self.assertEqual(seal["retry"], 0)
                self.assertEqual(seal["analysis_call_count"], 0)
                self.assertEqual(seal["inventory"]["status"], "rejected")
                summary = json.loads((root / "returned-summary.json").read_text())
                self.assertEqual(summary["status"], "partial_or_invalid")
                self.assertFalse(summary["formal_pass"])
                self.assertEqual(summary["retry"], 0)
                self.assertIn("returned-summary.json", seal["artifact_identities"])
                self.assertEqual(len(summary["capture_ids"]), 16)
                self.assertEqual(len(summary["returned"]), 16)
                if name not in {
                    "python_cleanup", "shell_cleanup", "missing_artifact",
                    "symlink_artifact",
                }:
                    self.assertEqual(seal["cleanup"]["python"], "pass")
                    self.assertEqual(seal["cleanup"]["shell"], "pass")
                    self.assertEqual(seal["cleanup"]["independent_zero"], "pass")
                if name == "missing_artifact":
                    self.assertNotIn("commands-audit.json", seal["artifact_identities"])
                    self.assertIn("plan.json", seal["artifact_identities"])
                    self.assertIn("run.json", seal["artifact_identities"])
                if name == "symlink_artifact":
                    self.assertNotIn("commands-audit.json", seal["artifact_identities"])
                    self.assertIn(
                        {"path": "commands-audit.json", "kind": "symlink"},
                        seal["inventory"]["unsafe_unbound"],
                    )
                if name == "special_node":
                    self.assertNotIn("unexpected-fifo", seal["artifact_identities"])
                    self.assertIn(
                        {"path": "unexpected-fifo", "kind": "non_regular"},
                        seal["inventory"]["unsafe_unbound"],
                    )

    def test_returned_summary_write_failure_is_attempted_once_and_nonzero(self):
        with temporary_directory() as temporary:
            root, *_rest = build_terminal_root(Path(temporary))
            write_json(root / "independent-final-zero.json", {
                "schema": subject.INDEPENDENT_ZERO_SCHEMA,
                "status": "pass",
                "strip_verified_zero": True,
                "ray_verified_zero": True,
            })
            original = subject.provenance.persist_canonical_json
            summary_attempts = []

            def persist(root_identity, child_name, value):
                if child_name == "returned-summary.json":
                    summary_attempts.append(child_name)
                    raise subject.provenance.ProvenanceIOError(
                        "returned_summary_write_failed"
                    )
                return original(root_identity, child_name, value)

            with mock.patch.object(
                subject.provenance,
                "persist_canonical_json",
                side_effect=persist,
            ):
                self.assertEqual(subject.main([
                    "finalize",
                    "--run-dir", str(root),
                    "--child-exit", "0",
                    "--shell-cleanup-exit", "0",
                    "--independent-zero-exit", "0",
                ]), 1)
            self.assertEqual(summary_attempts, ["returned-summary.json"])
            self.assertFalse((root / "returned-summary.json").exists())
            seal = json.loads((root / "terminal-seal.json").read_text())
            self.assertEqual(seal["status"], "FAIL")
            self.assertEqual(seal["error_code"], "returned_summary_write_failed")


if __name__ == "__main__":
    unittest.main()
