from __future__ import annotations

import hashlib
import json
import os
import shutil
import signal
import subprocess
import tempfile
import time
import unittest
from pathlib import Path
from unittest import mock

from camera_based_rgbww_optimizer.optimization import measure_p7_thermal_diagnostics as measure
from camera_based_rgbww_optimizer.optimization import p7_thermal_diagnostics as subject
from camera_based_rgbww_optimizer.optimization import analyze_p7_thermal_diagnostics as thermal_analyzer
from camera_based_rgbww_optimizer.optimization.hsi_objective import (
    HsiRejectedFeaturesError,
    TD_B_FORMAL_FEATURE_STATISTIC,
)
from camera_based_rgbww_optimizer.control import camera_gphoto2, camera_remote_v2


W0_TEMP_ROOT = Path("/Volumes/4T/temp/rgbww-optimizer/p7-td-a-w0-offline/test-runtime")
C2_TEMP_ROOT = Path("/Volumes/4T/temp/rgbww-optimizer/p7-td-b-r1-c2-offline/test-runtime")
C1_FAILED_RUN = Path(
    "/Volumes/4T/temp/rgbww-optimizer/p7-td-b-formal-ray-r1-20260723-182500"
)
C1_CR3_SHA256 = "0778e98d46d05e6bf13e218b79ee644178629076e4d9e6d8a1545fcb54a03889"
C1_SIDECAR_SHA256 = "93d0e64f612ab591da717d99af25dc5606a98148729e1988cc43f667375b4e68"


def _allowed_lineage_changed_paths_fixture() -> tuple[str, ...]:
    """Return a small test-only fixture from the production allowlist owners."""

    production = subject.TD_B_LINEAGE_ALLOWED_PRODUCTION_PATHS
    validation = subject.TD_B_LINEAGE_ALLOWED_VALIDATION_PATHS
    selected = {
        ".agent-work/PLAN.md",
        next(path for path in production if path.endswith("hsi_objective.py")),
        next(path for path in production if path.endswith("measure_raw_observer_validation.py")),
        next(path for path in validation if path.endswith("test_hsi_objective.py")),
        next(path for path in validation if path.endswith("test_p7_thermal_diagnostics.py")),
        next(path for path in validation if path == "docs/README.md"),
    }
    return tuple(sorted(selected))


def _c3_native_raw_report(feature_ids, *, ambient_policy, phase):
    required = set(feature_ids)
    patches = []
    feature_index = 0
    for block_index in range(1, 25):
        patch_name = f"block_{block_index:02d}"
        planes = {}
        for plane in ("R", "G1", "G2", "B"):
            feature_id = f"{patch_name}::{plane}"
            feature_index += 1
            planes[plane] = {
                "quality": {"status": "accepted"},
                "metrics": {
                    "valid_pixel_count": 30_000,
                    "nonfinite_fraction": 0.0,
                    "clipped_fraction": 0.0,
                    "near_noise_floor_fraction": 0.0,
                },
                "statistics": {
                    "normalized_per_second": {
                        "trimmed_mean": float(feature_index),
                    },
                },
            }
            if feature_id not in required:
                planes[plane]["ambient_subtracted"] = {
                    "trimmed_mean_per_second": float(feature_index) + 1000.0,
                }
        patches.append({
            "name": patch_name,
            "optimization_eligible": True,
            "planes": planes,
        })
    return {
        "schema_version": 1,
        "measurement": "native_bayer_patch_statistics",
        "source": {"path": "synthetic.cr3"},
        "location_config": {"sha256": "synthetic-location"},
        "mosaic": {"plane_order": ["R", "G1", "G2", "B"]},
        "observer_config": {
            "quality_thresholds": {
                "minimum_valid_pixels_per_plane": 29_000,
                "maximum_nonfinite_fraction": 0.0,
                "maximum_clipped_fraction": 0.0,
                "maximum_near_noise_floor_fraction": 0.05,
            },
        },
        "exposure_metadata": {"seconds": 0.001},
        "raw_metadata": {
            "black_level_per_channel": [512, 512, 512, 512],
            "white_level": 16383,
            "black_level_metadata_tolerance_dn": 8,
        },
        "analysis_context": {
            "native_raw_ambient_policy": ambient_policy,
            "ambient_subtraction_applied": (
                ambient_policy == subject.AMBIENT_POLICY_REQUIRE_PRECEDING
            ),
            "phase": phase,
            "formal_measurement": True,
        },
        "patches": patches,
    }


class _Clock:
    def __init__(self):
        self.value = 0.0

    def monotonic(self):
        return self.value

    def sleep(self, seconds):
        self.value += seconds


def _minimal_covariate(step):
    command = step["command"]
    return subject.build_covariate_record(
        source_id=step["source_id"], state_id=step["state_id"], command=command,
        sequence_index=0, capture_order=0, source_order=0, monotonic_timestamp_ns=1,
        wall_clock_timestamp="2026-07-21T00:00:00Z", session_elapsed_s=0,
        source_on_elapsed_s=0, state_on_elapsed_s=0, off_duration_before_s=0,
        previous_state_id=None, previous_state_dwell_s=None, shutter_seconds=0.01,
        raw_black_levels=[512] * 4, raw_white_level=16383,
        load_history={60: 0, 300: 0, 900: 0}, readback={},
        curve=json.loads(subject.CURVE_PATH.read_text(encoding="utf-8")) if step["source_id"] == "strip" else None,
    )


def _attach_v2_capture_evidence(root, step, result, *, observed=None, tier="tier_b", method=None):
    sequence = int(step["capture_id"].split("-", 1)[0])
    raw = Path(root) / f"{step['capture_id']}.CR3"
    raw.parent.mkdir(parents=True, exist_ok=True)
    raw.write_bytes(f"raw-{step['capture_id']}".encode())
    request_ns = 1_000_000_000
    if observed is None:
        observed = float(step.get("requested_elapsed_s") or 1.0)
    status = {"tier_a": "estimated_not_absolute", "tier_b": "weak_estimate", "tier_c": "unavailable"}[tier]
    if method is None and tier != "tier_c":
        method = "gphoto_capture_return_minus_recorded_exposure"
    estimate_ns = None if tier == "tier_c" else request_ns + int(float(observed) * 1_000_000_000)
    capture_done_ns = request_ns + 10_000_000 if estimate_ns is None else estimate_ns + 10_000_000
    metadata = {
        "schema": "remote_capture_result_v2", "capture_id": step["capture_id"],
        "request_id": f"request-{sequence}", "timing_quality": "best_effort_gphoto2",
        "formal_p7_eligibility": "unchanged_requires_later_planner_advisor_decision",
        "cr3": {"sha256": hashlib.sha256(raw.read_bytes()).hexdigest(), "byte_count": raw.stat().st_size, "content_type": "image/x-canon-cr3"},
        "gphoto2": {"driver_event_type": None, "event_sequence": [], "request_received_monotonic_ns": request_ns,
            "capture_call_started_monotonic_ns": request_ns, "capture_call_returned_monotonic_ns": capture_done_ns,
            "camera_event_observed_monotonic_ns": None, "file_added_observed_monotonic_ns": None,
            "download_started_monotonic_ns": capture_done_ns + 10_000_000, "download_completed_monotonic_ns": capture_done_ns + 20_000_000,
            "cr3_saved_observed_monotonic_ns": capture_done_ns + 30_000_000, "clock_domain": "bridge_monotonic"},
        "recorded_exposure": {"seconds": 0.01, "source": "Canon:ExposureTime", "status": "recorded"},
        "exposure_start_estimate": {"timestamp_monotonic_ns": estimate_ns, "clock_domain": "bridge_monotonic", "method": method,
            "status": status, "uncertainty_ms": None, "uncertainty_basis": "unknown"},
        "network_observation": {"request_id": f"request-{sequence}", "response_or_event_round_trip_ms": None, "uncertainty_ms": None, "uncertainty_basis": "unknown"},
        "bridge_utc_observation": {"request_received": "2026-07-21T00:00:00+00:00", "source": "bridge_system_clock_utc"},
    }
    # Keep capture-return arithmetic exact for the recognized Tier B method.
    if method == "gphoto_capture_return_minus_recorded_exposure" and estimate_ns is not None:
        metadata["gphoto2"]["capture_call_returned_monotonic_ns"] = estimate_ns + 10_000_000
    elif method == "gphoto_event_minus_recorded_exposure" and estimate_ns is not None:
        metadata["gphoto2"]["file_added_observed_monotonic_ns"] = estimate_ns + 10_000_000
    timing = camera_remote_v2.reconstruct_best_effort_timing(
        metadata, local_request_started_monotonic_s=0.0,
        local_response_received_monotonic_s=max(1.0, float(observed) + 1.0),
        local_readback_done_monotonic_s=0.0,
    )
    metadata["_local_receipt"] = {
        "parser_version": camera_remote_v2.PARSER_VERSION,
        "response_headers": {"content-type": "multipart/mixed; boundary=fake", "content-length": "1000",
            "x-capture-id": step["capture_id"], "x-request-id": f"request-{sequence}",
            "x-capture-metadata-schema": camera_remote_v2.SCHEMA},
        "multipart_body_byte_count": 1000, "multipart_body_sha256": "a" * 64,
        "http_attempts": 1, "successful_attempt_index": 1,
        "local_request_started_monotonic_s": 0.0,
        "local_response_received_monotonic_s": max(1.0, float(observed) + 1.0),
        "received_monotonic_s": max(1.0, float(observed) + 1.0),
        "timing_evidence": timing,
    }
    sidecar = raw.with_suffix(raw.suffix + ".metadata.json")
    sidecar.write_text(json.dumps(metadata), encoding="utf-8")
    result.update({"saved_file": str(raw), "remote_metadata_path": str(sidecar),
                   "timing_metadata": metadata, "timing_evidence": timing,
                   "physical_capture_count": 1})
    return result


def _fake_td_b_setup(root: Path, *, count: int = 1, fake_only: bool = True):
    root.mkdir(parents=True, exist_ok=True)
    attempts = []
    for index in range(1, count + 1):
        step = {"capture_id": f"{index:04d}-td-b-exposure-setup", "requested_elapsed_s": 1}
        result = _attach_v2_capture_evidence(root, step, {}, observed=1.0)
        raw = Path(result["saved_file"])
        sidecar = Path(result["remote_metadata_path"])
        metadata = json.loads(sidecar.read_text(encoding="utf-8"))
        attempts.append({
            "attempt_index": index,
            "capture_id": step["capture_id"],
            "disposition": "final" if index == count else "trial",
            "cr3_path": str(raw.resolve()),
            "cr3_sha256": hashlib.sha256(raw.read_bytes()).hexdigest(),
            "cr3_byte_count": raw.stat().st_size,
            "sidecar_path": str(sidecar.resolve()),
            "sidecar_sha256": hashlib.sha256(sidecar.read_bytes()).hexdigest(),
            "request_id": metadata["request_id"],
            "timing_tier": result["timing_evidence"]["tier"],
            "timing_method": metadata["exposure_start_estimate"]["method"],
            "recorded_exposure": metadata["recorded_exposure"],
            "shutter_speed": "1/100",
            "npy_paths": [],
            "npy_deleted": True,
        })
    curve = json.loads(subject.CURVE_PATH.read_text(encoding="utf-8"))
    from camera_based_rgbww_optimizer.optimization.hsi_source_evidence import expected_strip_payloads
    _raw, off_payload = expected_strip_payloads({channel: 0 for channel in subject.CHANNELS}, curve)
    return {
        "schema": subject.TD_B_SETUP_SCHEMA,
        "experiment_id": subject.TD_B,
        "source": "ray",
        "state_id": subject.TD_B_SETUP_STATE,
        "command": dict(subject.TD_B_SETUP_COMMAND),
        "command_sha256": subject.canonical_sha256(dict(subject.TD_B_SETUP_COMMAND)),
        "capture_role": "exposure_setup",
        "formal_measurement": False,
        "counts_as_physical": True,
        "enters_58_feature_fit": False,
        "enters_repeatability_covariance": False,
        "enters_td_b_history_aggregate": False,
        "setup_method": "bounded_remote_v2_auto_exposure",
        "historical_seed": subject.audit_td_b_historical_seed(),
        "camera": {"backend": "remote", "v2_capture_capability": measure.REMOTE_V2_CAPABILITY,
            "capture_settings_owner": "remote_backend.resolve_capture_settings", "iso": "100",
            "aperture": "implicit auto", "image_format": "RAW"},
        "attempts": attempts,
        "final_capture_id": attempts[-1]["capture_id"],
        "resolved_shutter_speed": "1/100",
        "setup_physical_cr3_count": count,
        "setup_physical_cr3_cap": subject.TD_B_SETUP_PHYSICAL_CAP,
        "input_hashes": {"location": subject.file_reference(subject.LOCATION_PATH)["sha256"],
            "policy": subject.file_reference(subject.POLICY_PATH)["sha256"],
            "operating_envelope": subject.file_reference(subject.OPERATING_ENVELOPE_V2_PATH)["sha256"]},
        "code_checkpoint": "fake-offline",
        "isolation": {"ray_set_response": {"data": {"hue": 120, "sat": 50, "intensity": 1000}},
            "ray_readback": {"data": {"hue": 120, "sat": 50, "intensity": 1000}},
            "strip_device_evidence": {"schema_version": 1, "requested_payload": off_payload,
                "baseline_snapshot": {"schema_version": 1, "generation": 1, **off_payload},
                "device_snapshot": {"schema_version": 1, "generation": 2, **off_payload},
                "device_state_entity": {"object_id": "rgbww_commanded_state", "key": 1},
                "device_identity": {"name": "bedroom-rgbww-strip", "mac_address": "00:11:22:33:44:55"}}},
        "cold_proxy": {"required_wait_s": 1800, "start_monotonic_s": 10.0, "end_monotonic_s": 1810.0},
        "cleanup": _fake_td_b_setup_cleanup(off_payload),
        "failure": None,
        "fake_only": fake_only,
    }


def _fake_td_b_setup_cleanup(off_payload):
    steps = [
        {"name": "esphome", "ok": True, "detail": {"payload": off_payload}, "error": None},
        {"name": "ray120c", "ok": True, "detail": {"response": {"data": {"intensity": 0}}}, "error": None},
    ]
    strip = {"schema_version": 1, "requested_payload": off_payload,
        "baseline_snapshot": {"schema_version": 1, "generation": 2, **off_payload},
        "device_snapshot": {"schema_version": 1, "generation": 3, **off_payload},
        "device_state_entity": {"object_id": "rgbww_commanded_state", "key": 1},
        "device_identity": {"name": "bedroom-rgbww-strip", "mac_address": "00:11:22:33:44:55"}}
    return {
        "python": {"status": "pass", "steps": steps, "exit_code": 0},
        "shell": {"status": "pass", "steps": steps, "exit_code": 0},
        "wrapper": {"status": "complete", "child_exit_code": 0, "shell_cleanup_exit_code": 0,
            "wrapper_exit_code": 0, "signal": None},
        "final_both_off": {"strip_device_evidence": strip, "ray_readback": {"data": {"intensity": 0}}},
    }


def _build_p6_seed_fixture(root: Path):
    source = subject.P6_SETUP_SEED_RUN
    captures = [json.loads(line) for line in (source / "captures.jsonl").read_text().splitlines()]
    row = next(item for item in captures if item.get("capture_id") == subject.P6_SETUP_SEED_CAPTURE_ID)
    commands = [json.loads(line) for line in (source / "commands.jsonl").read_text().splitlines()]
    command = next(item for item in commands if item.get("capture_id") == subject.P6_SETUP_SEED_CAPTURE_ID and item.get("event") == "ray_on_readback_verified")
    root.mkdir(parents=True, exist_ok=True)
    raw_source = Path(row["capture"]["capture"]["saved_file"])
    raw = root / raw_source.name
    try:
        os.link(raw_source, raw)
    except OSError:
        shutil.copyfile(raw_source, raw)
    report_source = Path(row["capture"]["patch_statistics"])
    report = json.loads(report_source.read_text(encoding="utf-8"))
    report["exposure_metadata"]["raw_file"] = str(raw.resolve())
    report_path = root / report_source.name
    report_path.write_text(json.dumps(report), encoding="utf-8")
    row["capture"]["capture"]["saved_file"] = str(raw.resolve())
    row["capture"]["patch_statistics"] = str(report_path.resolve())
    (root / "captures.jsonl").write_text(json.dumps(row) + "\n", encoding="utf-8")
    (root / "commands.jsonl").write_text(json.dumps(command) + "\n", encoding="utf-8")
    return row, command, report, report_path


class P7ThermalDiagnosticsTests(unittest.TestCase):
    def test_td_b_trusted_prerequisite_spellings_are_canonical_and_cwd_independent(self):
        scratch_root = Path("/Volumes/4T/temp/rgbww-optimizer/p7-td-b-path-r1-offline/test-runtime")
        scratch_root.mkdir(parents=True, exist_ok=True)
        previous_cwd = Path.cwd()
        try:
            os.chdir(scratch_root)
            plans = [
                subject.build_diagnostic_plan(
                    subject.TD_B, source="ray", prerequisite_artifact=spelling,
                )
                for spelling in (
                    "config/hsi/p7-operating-envelope-v2.json",
                    "./config/hsi/p7-operating-envelope-v2.json",
                    subject.OPERATING_ENVELOPE_V2_PATH,
                )
            ]
        finally:
            os.chdir(previous_cwd)

        references = [plan["inputs"]["operating_envelope"] for plan in plans]
        self.assertEqual(references[0], references[1])
        self.assertEqual(references[1], references[2])
        self.assertEqual(references[0], {
            "path": str(subject.OPERATING_ENVELOPE_V2_PATH.resolve()),
            "sha256": subject.OPERATING_ENVELOPE_V2_SHA256,
        })

    def test_td_b_trusted_prerequisite_rejects_non_owner_paths_before_json_read(self):
        scratch_root = Path("/Volumes/4T/temp/rgbww-optimizer/p7-td-b-path-r1-offline/test-runtime")
        scratch_root.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=scratch_root) as tempdir:
            root = Path(tempdir)
            same_hash_copy = root / "same-hash.json"
            shutil.copyfile(subject.OPERATING_ENVELOPE_V2_PATH, same_hash_copy)
            symlink = root / "trusted-link.json"
            symlink.symlink_to(subject.OPERATING_ENVELOPE_V2_PATH)
            cases = {
                "traversal": "config/hsi/../hsi/p7-operating-envelope-v2.json",
                "outside": same_hash_copy,
                "missing": root / "missing.json",
                "directory": root,
                "symlink": symlink,
            }
            for label, path in cases.items():
                with self.subTest(label=label), self.assertRaises(ValueError):
                    subject.build_diagnostic_plan(
                        subject.TD_B, source="ray", prerequisite_artifact=path,
                    )

        reference = subject.file_reference(subject.OPERATING_ENVELOPE_V2_PATH)
        with self.assertRaisesRegex(ValueError, "hash"):
            subject.validate_trusted_operating_envelope_reference(
                {**reference, "sha256": "0" * 64}, require_v2=True,
            )
        with self.assertRaisesRegex(ValueError, "trusted repository owner"):
            subject.validate_trusted_operating_envelope_reference(
                subject.file_reference(subject.OPERATING_ENVELOPE_PATH), require_v2=True,
            )

    def test_td_b_relative_cli_plan_reaches_setup_fake_backend_boundary(self):
        scratch_root = Path("/Volumes/4T/temp/rgbww-optimizer/p7-td-b-path-r1-offline/test-runtime")
        scratch_root.mkdir(parents=True, exist_ok=True)
        observed = {"factory": 0, "setup": 0, "replay": None}

        class FakeBackend:
            v2_capture_capability = measure.REMOTE_V2_CAPABILITY

        def factory(*_args, **_kwargs):
            observed["factory"] += 1
            return FakeBackend()

        def setup(plan, **kwargs):
            observed["setup"] += 1
            self.assertEqual(plan["inputs"]["operating_envelope"], {
                "path": str(subject.OPERATING_ENVELOPE_V2_PATH.resolve()),
                "sha256": subject.OPERATING_ENVELOPE_V2_SHA256,
            })
            measure._validate_td_b_setup_frozen_plan(plan)
            root = Path(kwargs["output_dir"]) / kwargs["run_name"]
            artifact = _fake_td_b_setup(root, count=2)
            artifact_path = root / "setup.json"
            artifact_path.write_text(json.dumps(artifact), encoding="utf-8")
            observed["replay"] = thermal_analyzer.analyze_td_b_setup_resolution(
                plan, setup_artifact_path=artifact_path,
            )
            (root / "plan.json").write_text(json.dumps(plan, indent=2) + "\n", encoding="utf-8")
            (root / "public-replay.json").write_text(
                json.dumps(observed["replay"], indent=2) + "\n", encoding="utf-8",
            )
            evidence_root = os.environ.get("P7_PATH_R1_EVIDENCE_DIR")
            if evidence_root:
                shutil.copytree(root, Path(evidence_root) / "fake-production-roundtrip")
            return artifact_path

        with tempfile.TemporaryDirectory(dir=scratch_root) as tempdir:
            output = Path(tempdir) / "relative-cli"
            self.assertEqual(measure.main([
                    "--experiment-id", subject.TD_B, "--source", "ray",
                    "--run-name", output.name, "--output-dir", str(output.parent),
                    "--prerequisite-artifact", "config/hsi/p7-operating-envelope-v2.json",
                    "--execute", "--allow-device-control", "--human-authorization", subject.TD_B,
                    "--phase", "setup", "--code-checkpoint", "a" * 40,
                ], backend_factory=factory, setup_fn=setup), 0)
        self.assertEqual(observed["factory"], 1)
        self.assertEqual(observed["setup"], 1)
        self.assertEqual(observed["replay"]["status"], "offline_fake_replay_pass")
        self.assertEqual(observed["replay"]["setup_physical_cr3_count"], 2)

    def test_td_b_setup_tampered_envelope_rejects_before_backend_or_output_owner(self):
        scratch_root = Path("/Volumes/4T/temp/rgbww-optimizer/p7-td-b-path-r1-offline/test-runtime")
        scratch_root.mkdir(parents=True, exist_ok=True)
        plan = subject.build_diagnostic_plan(
            subject.TD_B, source="ray",
            prerequisite_artifact="config/hsi/p7-operating-envelope-v2.json",
            for_execution=True, human_authorization=subject.TD_B, v2_capture_capability=True,
        )

        class UntouchableBackend:
            @property
            def v2_capture_capability(self):
                raise AssertionError("tampered plan touched backend capability")

        cases = {
            "path": {**plan["inputs"]["operating_envelope"],
                     "path": str(scratch_root / "same-hash-copy.json")},
            "hash": {**plan["inputs"]["operating_envelope"], "sha256": "0" * 64},
        }
        shutil.copyfile(
            subject.OPERATING_ENVELOPE_V2_PATH, scratch_root / "same-hash-copy.json",
        )
        for label, reference in cases.items():
            tampered = json.loads(json.dumps(plan))
            tampered["inputs"]["operating_envelope"] = reference
            output = scratch_root / f"tampered-{label}-must-not-exist"
            if output.exists():
                self.fail(f"test output owner unexpectedly exists: {output}")
            with self.subTest(label=label), mock.patch.object(
                measure, "_validate_checkpoint_and_tree",
            ), self.assertRaisesRegex(PermissionError, "identity"):
                measure.run_td_b_setup_provisional(
                    tampered, output_dir=output.parent, run_name=output.name,
                    camera_backend=UntouchableBackend(), code_checkpoint="a" * 40,
                )
            self.assertFalse(output.exists())

    def test_p6_historical_seed_is_rebuilt_as_seed_only(self):
        audit = subject.audit_td_b_historical_seed()
        self.assertTrue(audit["historical_seed_usable"])
        self.assertTrue(audit["seed_only"])
        self.assertFalse(audit["formal_capture_eligible"])
        self.assertEqual(audit["initial_shutter_seed"], "1/6400")
        self.assertEqual(audit["evidence"]["feature_count"], 58)
        self.assertEqual(audit["evidence"]["remote_endpoint"], "/v1/capture")
        self.assertEqual(audit["evidence"]["quality"]["status"], "rejected")

    def test_p6_historical_seed_tampering_falls_back_without_seed(self):
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            row, command, report, report_path = _build_p6_seed_fixture(root)
            self.assertTrue(subject.audit_td_b_historical_seed(root)["historical_seed_usable"])
            mutations = {
                "command": lambda: command["expected"].update(sat=49),
                "capture_hash": lambda: row["capture"]["capture"].update(sha256="0" * 64),
                "location": lambda: report["location_config"].update(sha256="0" * 64),
                "recorded_exposure": lambda: report["exposure_metadata"].update(status="fallback_nominal"),
                "raw_owner": lambda: report["exposure_metadata"].update(raw_file=str(root / "other.CR3")),
            }
            for name, mutate in mutations.items():
                with self.subTest(name=name):
                    clean_row, clean_command, clean_report, clean_report_path = _build_p6_seed_fixture(root / name)
                    row, command, report, report_path = clean_row, clean_command, clean_report, clean_report_path
                    mutate()
                    (root / name / "captures.jsonl").write_text(json.dumps(row) + "\n", encoding="utf-8")
                    (root / name / "commands.jsonl").write_text(json.dumps(command) + "\n", encoding="utf-8")
                    report_path.write_text(json.dumps(report), encoding="utf-8")
                    audit = subject.audit_td_b_historical_seed(root / name)
                    self.assertFalse(audit["historical_seed_usable"])
                    self.assertIsNone(audit["initial_shutter_seed"])
                    self.assertTrue(audit["seed_only"])

    def test_td_b_setup_round_trip_resolves_only_ray_shutter(self):
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            artifact = _fake_td_b_setup(root / "setup", count=8)
            artifact_path = root / "setup" / "setup.json"
            artifact_path.write_text(json.dumps(artifact), encoding="utf-8")
            validated = subject.validate_td_b_exposure_setup(artifact, artifact_path=artifact_path)
            self.assertEqual(validated["physical_count"], 8)
            plan = subject.build_diagnostic_plan(
                subject.TD_B, source="ray", prerequisite_artifact=subject.OPERATING_ENVELOPE_V2_PATH,
            )
            resolved = subject.resolve_td_b_plan_with_setup(plan, setup_artifact_path=artifact_path)
            self.assertEqual(resolved["frozen_shutters"]["ray-h120-s50"], "1/100")
            self.assertEqual(resolved["exposure_setup_required"], [])
            self.assertEqual(resolved["setup_physical_cr3_count"], 8)
            self.assertFalse(resolved["formal_capture_eligible"])
            self.assertEqual(resolved["status"], "fake_resolved_device_locked")
            replay = subject.replay_td_b_setup_resolution(plan, setup_artifact_path=artifact_path)
            self.assertEqual(replay["status"], "offline_fake_replay_pass")
            self.assertEqual(replay["formal_capture_count"], 16)
            self.assertEqual(replay["setup_physical_cr3_count"], 8)
            self.assertTrue(replay["setup_excluded_from_58_feature_fit"])
            self.assertEqual(
                thermal_analyzer.analyze_td_b_setup_resolution(plan, setup_artifact_path=artifact_path),
                replay,
            )

    def test_td_b_setup_injected_state_machine_accounts_attempts_and_cold_wait(self):
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            plan = subject.build_diagnostic_plan(
                subject.TD_B, source="ray", prerequisite_artifact=subject.OPERATING_ENVELOPE_V2_PATH,
            )
            fake = _fake_td_b_setup(root / "evidence", count=2)
            clock = _Clock()
            cleanup_calls = []
            final_off = fake["cleanup"]["final_both_off"]
            artifact_path = measure.execute_td_b_exposure_setup(
                plan, run_dir=root / "run",
                capture_setup_fn=lambda request: (
                    self.assertEqual(request["max_captures"], 8) or fake["attempts"]
                ),
                both_off_gate_fn=lambda gate: {"status": "pass", "gate_id": gate,
                    "strip_verified_off": True, "ray_verified_off": True,
                    "strip_device_evidence": final_off["strip_device_evidence"],
                    "ray_readback": final_off["ray_readback"]},
                apply_ray_fn=lambda _command: fake["isolation"]["ray_set_response"],
                ray_readback_fn=lambda: fake["isolation"]["ray_readback"],
                strip_off_evidence_fn=lambda: fake["isolation"]["strip_device_evidence"],
                cleanup_fn=lambda: cleanup_calls.append("cleanup") or fake["cleanup"]["python"],
                shell_cleanup_evidence={key: fake["cleanup"][key] for key in ("shell", "wrapper", "final_both_off")},
                historical_seed=fake["historical_seed"], camera_settings=fake["camera"],
                code_checkpoint="fake-offline", execution_authorized=False, fake_only=True,
                monotonic_fn=clock.monotonic, sleep_fn=clock.sleep,
            )
            artifact = json.loads(artifact_path.read_text(encoding="utf-8"))
            self.assertEqual(artifact["setup_physical_cr3_count"], 2)
            self.assertEqual(artifact["cold_proxy"]["end_monotonic_s"], 1800.0)
            self.assertEqual(cleanup_calls, ["cleanup"])

    def test_td_b_setup_state_machine_rejects_ninth_attempt_and_cleans_up(self):
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            plan = subject.build_diagnostic_plan(
                subject.TD_B, source="ray", prerequisite_artifact=subject.OPERATING_ENVELOPE_V2_PATH,
            )
            fake = _fake_td_b_setup(root / "evidence", count=9)
            cleanup_calls = []
            final_off = fake["cleanup"]["final_both_off"]
            with self.assertRaisesRegex(RuntimeError, "physical_budget_accounting_violation"):
                measure.execute_td_b_exposure_setup(
                    plan, run_dir=root / "run", capture_setup_fn=lambda _request: fake["attempts"],
                    both_off_gate_fn=lambda gate: {"status": "pass", "gate_id": gate,
                        "strip_verified_off": True, "ray_verified_off": True,
                        "strip_device_evidence": final_off["strip_device_evidence"],
                        "ray_readback": final_off["ray_readback"]},
                    apply_ray_fn=lambda _command: fake["isolation"]["ray_set_response"],
                    ray_readback_fn=lambda: fake["isolation"]["ray_readback"],
                    strip_off_evidence_fn=lambda: fake["isolation"]["strip_device_evidence"],
                    cleanup_fn=lambda: cleanup_calls.append("cleanup") or fake["cleanup"]["python"],
                    shell_cleanup_evidence={key: fake["cleanup"][key] for key in ("shell", "wrapper", "final_both_off")},
                    historical_seed=fake["historical_seed"],
                    camera_settings=fake["camera"], code_checkpoint="fake", execution_authorized=False,
                    fake_only=True, sleep_fn=lambda _seconds: None,
                )
            self.assertEqual(cleanup_calls, ["cleanup"])
            self.assertTrue((root / "run" / "failure.json").is_file())
            failure = json.loads((root / "run" / "failure.json").read_text(encoding="utf-8"))
            self.assertTrue(failure["capture_attempted"])
            self.assertEqual(failure["retained_attempt_count"], 9)
            self.assertEqual(len(failure["retained_attempts"]), 9)

    def test_td_b_real_setup_rejects_caller_boolean_without_exact_plan_gate_before_calls(self):
        plan = subject.build_diagnostic_plan(
            subject.TD_B, source="ray", prerequisite_artifact=subject.OPERATING_ENVELOPE_V2_PATH,
        )
        calls = []
        with tempfile.TemporaryDirectory() as tempdir, self.assertRaisesRegex(PermissionError, "exact plan"):
            measure.execute_td_b_exposure_setup(
                plan, run_dir=Path(tempdir) / "run",
                capture_setup_fn=lambda _request: calls.append("capture") or [],
                both_off_gate_fn=lambda _gate: calls.append("off") or {},
                apply_ray_fn=lambda _command: calls.append("ray") or {}, ray_readback_fn=lambda: {},
                strip_off_evidence_fn=lambda: {}, cleanup_fn=lambda: calls.append("cleanup") or {},
                shell_cleanup_evidence={}, historical_seed=subject.audit_td_b_historical_seed(),
                camera_settings={"v2_capture_capability": measure.REMOTE_V2_CAPABILITY},
                code_checkpoint="a" * 40, execution_authorized=True, fake_only=False,
            )
        self.assertEqual(calls, [])

    def test_td_b_setup_replays_both_off_before_ray_command(self):
        plan = subject.build_diagnostic_plan(
            subject.TD_B, source="ray", prerequisite_artifact=subject.OPERATING_ENVELOPE_V2_PATH,
        )
        calls = []
        with tempfile.TemporaryDirectory() as tempdir, self.assertRaises(ValueError):
            measure.execute_td_b_exposure_setup(
                plan, run_dir=Path(tempdir) / "run", capture_setup_fn=lambda _request: [],
                both_off_gate_fn=lambda gate: {"status": "pass", "gate_id": gate,
                    "strip_verified_off": True, "ray_verified_off": True,
                    "strip_device_evidence": {}, "ray_readback": {}},
                apply_ray_fn=lambda _command: calls.append("ray") or {}, ray_readback_fn=lambda: {},
                strip_off_evidence_fn=lambda: {}, cleanup_fn=lambda: calls.append("cleanup") or {"status": "pass"},
                shell_cleanup_evidence={}, historical_seed=subject.audit_td_b_historical_seed(),
                camera_settings={"v2_capture_capability": measure.REMOTE_V2_CAPABILITY},
                code_checkpoint="fake", execution_authorized=False, fake_only=True,
            )
        self.assertEqual(calls, ["cleanup"])

    def test_td_b_setup_rejects_budget_hash_owner_and_cold_proxy_tampering(self):
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir) / "setup"
            clean = _fake_td_b_setup(root, count=1)
            path = root / "setup.json"
            path.write_text(json.dumps(clean), encoding="utf-8")
            mutations = []
            changed = json.loads(json.dumps(clean)); changed["setup_physical_cr3_count"] = 9; mutations.append(changed)
            changed = json.loads(json.dumps(clean)); changed["attempts"][0]["cr3_sha256"] = "0" * 64; mutations.append(changed)
            changed = json.loads(json.dumps(clean)); changed["attempts"][0]["request_id"] = "wrong"; mutations.append(changed)
            changed = json.loads(json.dumps(clean)); changed["cold_proxy"]["end_monotonic_s"] = 1809.0; mutations.append(changed)
            changed = json.loads(json.dumps(clean)); changed["attempts"][0]["npy_paths"] = ["trial.npy"]; mutations.append(changed)
            changed = json.loads(json.dumps(clean)); changed["historical_seed"]["capture_id"] = "stale"; mutations.append(changed)
            changed = json.loads(json.dumps(clean)); changed["command"]["sat"] = 49; mutations.append(changed)
            changed = json.loads(json.dumps(clean)); changed["source"] = "strip"; mutations.append(changed)
            changed = json.loads(json.dumps(clean)); changed["isolation"]["ray_readback"]["data"]["sat"] = 49; mutations.append(changed)
            changed = json.loads(json.dumps(clean)); changed["isolation"]["strip_device_evidence"]["device_snapshot"]["generation"] = 1; mutations.append(changed)
            changed = json.loads(json.dumps(clean)); changed["cleanup"]["wrapper"]["child_exit_code"] = 1; mutations.append(changed)
            changed = json.loads(json.dumps(clean)); changed["cleanup"]["wrapper"]["signal"] = "TERM"; mutations.append(changed)
            changed = json.loads(json.dumps(clean)); changed["cleanup"]["shell"]["exit_code"] = 70; mutations.append(changed)
            changed = json.loads(json.dumps(clean)); changed["cleanup"]["python"]["steps"][0]["ok"] = False; mutations.append(changed)
            for artifact in mutations:
                with self.subTest(artifact=artifact):
                    with self.assertRaises(ValueError):
                        subject.validate_td_b_exposure_setup(artifact, artifact_path=path)

    def test_td_b_setup_ninth_physical_capture_is_rejected(self):
        with tempfile.TemporaryDirectory() as tempdir:
            artifact = _fake_td_b_setup(Path(tempdir) / "setup", count=9)
            with self.assertRaisesRegex(ValueError, "1..8"):
                subject.validate_td_b_exposure_setup(artifact)

    def test_td_a_plan_freezes_exact_command_schedule_and_caps(self):
        plan = subject.build_diagnostic_plan(subject.TD_A, source="strip")
        self.assertEqual(plan["experiment_id"], subject.TD_A)
        self.assertEqual(plan["timing_schedule_s"], [60, 120, 300, 600])
        self.assertEqual(plan["budgets"], {"formal_cap": 12, "ambient_cap": 3, "physical_cr3_cap": 22})
        self.assertEqual([step["ambient_position"] for step in plan["captures"] if step["capture_role"] == "ambient"], ["start", "mid", "end"])
        formal = [step for step in plan["captures"] if step["formal_measurement"]]
        self.assertEqual(len(formal), 12)
        self.assertEqual(formal[0]["command"], {"cw": 518, "ww": 0, "r": 0, "g": 4095, "b": 0})
        self.assertTrue(all(step["exact_command_hash"] == subject.canonical_sha256(step["command"]) for step in formal))
        self.assertTrue(all(plan["hard_locks"].values()))
        self.assertEqual(plan["offline_contract"], {"env_calls": 0, "network_calls": 0, "device_calls": 0, "all_off_calls": 0})
        self.assertEqual(plan["schema"], subject.PLAN_SCHEMA_V2)
        self.assertEqual(plan["timing_contract"]["name"], "best_effort_gphoto2_observed_elapsed_v2")
        self.assertFalse(plan["timing_contract"]["absolute_exposure_start"])

    def test_timing_contract_plan_mutation_cannot_pollute_shared_owner(self):
        first = subject.build_diagnostic_plan(subject.TD_A, source="ray")
        first["timing_contract"]["accepted_tiers"].append("tier_c")
        second = subject.build_diagnostic_plan(subject.TD_A, source="ray")
        self.assertEqual(second["timing_contract"], subject.timing_contract(2))
        self.assertEqual(subject.TIMING_CONTRACT_V2["accepted_tiers"], ("tier_a", "tier_b"))
        self.assertEqual(subject.ACCEPTED_TIMING_TIERS, frozenset({"tier_a", "tier_b"}))

    def test_experiment_aware_timing_sequence_identity(self):
        self.assertNotEqual(
            subject.timing_sequence_identity(subject.TD_A, {"formal_measurement": True, "source_id": "ray", "state_id": "A", "cycle_index": 1}),
            subject.timing_sequence_identity(subject.TD_A, {"formal_measurement": True, "source_id": "ray", "state_id": "A", "cycle_index": 2}),
        )
        self.assertNotEqual(
            subject.timing_sequence_identity(subject.TD_B, {"formal_measurement": True, "source_id": "ray", "state_id": "A", "role": "initial_anchor"}),
            subject.timing_sequence_identity(subject.TD_B, {"formal_measurement": True, "source_id": "ray", "state_id": "A", "role": "return_after_D"}),
        )
        self.assertNotEqual(
            subject.timing_sequence_identity(subject.TD_C, {"formal_measurement": True, "source_id": "ray", "state_id": "A", "session_index": 1}),
            subject.timing_sequence_identity(subject.TD_C, {"formal_measurement": True, "source_id": "ray", "state_id": "A", "session_index": 2}),
        )
        with self.assertRaisesRegex(ValueError, "session identity"):
            subject.timing_sequence_identity(subject.TD_C, {"formal_measurement": True, "source_id": "ray", "state_id": "A"})

    def test_td_c_runner_accepts_observed_elapsed_reset_across_sessions(self):
        plan = subject.build_diagnostic_plan(subject.TD_C)
        ray_steps = [step for step in plan["captures"] if step["formal_measurement"] and step["source_id"] == "ray"][:2]
        for step in ray_steps:
            step["requested_elapsed_s"] = 60
            step["timing_status"] = "resolved"
            step["timing_acceptance"] = "observed_elapsed_record_only"
        shutter = {"ray-h120-s100": "1/5000"}
        plan.update({
            "status": "execute_authorized",
            "captures": ray_steps,
            "budgets": {"formal_cap": 2, "ambient_cap": 0, "physical_cr3_cap": 2},
            "frozen_shutters": shutter, "exposure_setup_required": [],
            "execution_authorization": {"human_authorization_experiment_id": subject.TD_C,
                "human_authorization_verified": True, "remote_v2_capability": True},
            "camera": {**plan["camera"], "v2_capture_timing_capability_available": True},
            "shutter_ledger_provenance": {"owner": "experiment_capture_steps",
                "required_cache_keys": ["ray-h120-s100"],
                "frozen_shutters_sha256": subject.canonical_sha256(shutter)},
        })
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir) / "run"
            def capture(step):
                return _attach_v2_capture_evidence(
                    root, step, {"thermal_covariates": _minimal_covariate(step)}, observed=64.4,
                )
            measure.execute_plan(
                plan, run_dir=root, apply_command_fn=lambda _step: {}, readback_fn=lambda _step: {},
                capture_fn=capture,
                both_off_gate_fn=lambda _gate: {"status": "pass", "strip_verified_off": True, "ray_verified_off": True},
                cleanup_fn=lambda: {"status": "pass"}, monotonic_fn=lambda: 0, sleep_fn=lambda _seconds: None,
            )
            run = json.loads((root / "run.json").read_text())
            self.assertEqual(run["status"], "complete")
            self.assertEqual(run["physical_cr3_count"], 2)

    def test_shutter_ledgers_are_scoped_to_exact_experiment_and_source(self):
        expected = {
            (subject.TD_A, "ray"): ({"ray-h120-s100": "1/5000"}, []),
            (subject.TD_A, "strip"): ({"strip-h120-s100-fullscale": "1/320"}, []),
            (subject.TD_B, "ray"): ({
                "ray-h0-s0": "1/8000",
                "ray-h120-s100": "1/5000",
                "ray-h120-s50": None,
                "ray-h300-s100": "1/2000",
            }, ["ray-h120-s50"]),
            (subject.TD_B, "strip"): ({
                "strip-h0-s0-fullscale": "1/500",
                "strip-h120-s100-fullscale": "1/320",
                "strip-h120-s50-fullscale": "1/400",
                "strip-h300-s100-fullscale": "1/125",
            }, []),
        }
        for (experiment, source), (shutters, setup) in expected.items():
            with self.subTest(experiment=experiment, source=source):
                first = subject.build_diagnostic_plan(experiment, source=source)
                second = subject.build_diagnostic_plan(experiment, source=source)
                self.assertEqual(first["frozen_shutters"], shutters)
                self.assertEqual(first["exposure_setup_required"], setup)
                self.assertEqual(first["shutter_ledger_provenance"], second["shutter_ledger_provenance"])
                self.assertEqual(
                    first["shutter_ledger_provenance"]["frozen_shutters_sha256"],
                    subject.canonical_sha256(shutters),
                )
                self.assertEqual(set(shutters), set(subject.required_shutter_cache_keys(first["captures"])))
        self.assertNotIn("ray-h120-s50", subject.build_diagnostic_plan(subject.TD_A, source="ray")["frozen_shutters"])
        self.assertNotIn("ray-h120-s50", subject.build_diagnostic_plan(subject.TD_A, source="strip")["frozen_shutters"])

    def test_td_b_and_c_dry_plans_exist_but_execute_stays_locked(self):
        td_b = subject.build_diagnostic_plan(subject.TD_B, source="ray")
        self.assertEqual(len(td_b["captures"]), 16)
        deferred = [step for step in td_b["captures"] if str(step.get("role", "")).startswith("return_after_")]
        self.assertTrue(deferred)
        self.assertTrue(all(step["requested_elapsed_s"] is None and step["timing_status"] == "deferred_until_td_a" for step in deferred))
        self.assertEqual(sum(bool(step.get("isolation_gate_after")) for step in td_b["captures"]), 7)
        core = subject.build_diagnostic_plan(subject.TD_C, variant="core")
        expansion = subject.build_diagnostic_plan(subject.TD_C, variant="expansion")
        self.assertEqual(core["session_orders"], [["ray", "strip"], ["strip", "ray"], ["ray", "strip"], ["strip", "ray"]])
        self.assertEqual(core["comparison_design"], "order_balanced_paired_comparison_not_classic_abba")
        self.assertEqual(core["budgets"], {"formal_cap": 8, "ambient_cap": 8, "physical_cr3_cap": 16})
        self.assertEqual(len(core["captures"]), 16)
        self.assertEqual(sum(step["formal_measurement"] for step in core["captures"]), 8)
        self.assertEqual(sum(step["capture_role"] == "ambient" for step in core["captures"]), 8)
        self.assertTrue(all(step["requested_elapsed_s"] is None for step in core["captures"] if step["formal_measurement"]))
        self.assertEqual(len(expansion["captures"]), 16)
        with self.assertRaisesRegex(PermissionError, "TD-B"):
            subject.build_diagnostic_plan(subject.TD_B, source="ray", for_execution=True, human_authorization=subject.TD_B)
        with self.assertRaisesRegex(PermissionError, "TD-C"):
            subject.build_diagnostic_plan(subject.TD_C, for_execution=True, human_authorization=subject.TD_C)

    def test_td_b_v2_developer_dwell_plan_is_resolved_without_measured_settle(self):
        plan = subject.build_diagnostic_plan(
            subject.TD_B, source="strip",
            prerequisite_artifact=subject.OPERATING_ENVELOPE_V2_PATH,
        )
        self.assertEqual(len(plan["captures"]), 16)
        self.assertEqual(plan["timing_resolution"], "developer_override_resolved")
        self.assertEqual(plan["operational_dwell"], {
            "source": "developer_human_override", "seconds": 600,
            "scientifically_settled": False, "measured_t_formal_provisional_s": None,
        })
        self.assertTrue(all(step["requested_elapsed_s"] is not None for step in plan["captures"]))
        self.assertEqual(
            [step["requested_elapsed_s"] for step in plan["captures"]],
            [600, 60, 120, 300, 600, 600, 60, 120, 300, 600, 600, 60, 120, 300, 600, 600],
        )

    def test_developer_dwell_envelope_rejects_tampered_decision_contract(self):
        envelope = json.loads(subject.OPERATING_ENVELOPE_V2_PATH.read_text(encoding="utf-8"))
        cases = (
            ("owner", {"decision_owner": "Planner"}),
            ("dwell", {"developer_selected_operational_dwell_s": 300}),
            ("measured", {"t_formal_provisional_s": 600}),
            ("status", {"status": "td_a_pass"}),
            ("audit", {"decision_audit": {"path": "advisor/4/0.AUDIT/03-human-decision-no-extension.md", "sha256": "0" * 64}}),
        )
        for label, changes in cases:
            with self.subTest(label=label), self.assertRaises(ValueError):
                subject.validate_operating_envelope({**envelope, **changes})

    def test_legacy_v1_envelope_cannot_be_claimed_as_v2(self):
        envelope = json.loads(subject.OPERATING_ENVELOPE_PATH.read_text(encoding="utf-8"))
        self.assertEqual(subject.validate_operating_envelope(envelope)["mode"], "legacy_v1")
        with self.assertRaisesRegex(ValueError, "explicit v2"):
            subject.validate_operating_envelope(envelope, require_v2=True)

    def test_td_b_plan_provenance_mismatch_is_rejected(self):
        envelope = json.loads(subject.OPERATING_ENVELOPE_V2_PATH.read_text(encoding="utf-8"))
        plan = subject.build_diagnostic_plan(
            subject.TD_B, source="strip",
            prerequisite_artifact=subject.OPERATING_ENVELOPE_V2_PATH,
        )
        subject.validate_td_b_operational_dwell_plan(plan, envelope)
        plan["operational_dwell"]["seconds"] = 300
        with self.assertRaisesRegex(ValueError, "provenance"):
            subject.validate_td_b_operational_dwell_plan(plan, envelope)

    def test_scheduler_accepts_large_finite_best_effort_offset(self):
        clock = _Clock()
        results = subject.run_timed_schedule(
            [60], command_apply_fn=lambda: None, readback_fn=lambda: None,
            capture_fn=lambda _point: {"timing_evidence": {
                "tier": "tier_b", "status": "accepted_best_effort_anchor",
                "provenance": subject.TIMING_CONTRACT_V2["provenance"],
                "best_effort_elapsed_s": 64.40580299403518,
            }}, monotonic_fn=clock.monotonic, sleep_fn=clock.sleep,
        )
        self.assertEqual(results[0].nominal_slot_s, 60)
        self.assertAlmostEqual(results[0].best_effort_exposure_start_elapsed_s, 64.40580299403518)
        self.assertAlmostEqual(results[0].timing_offset_s, 4.40580299403518)
        self.assertEqual(results[0].timing_evidence_status, "accepted")

    def test_readback_completion_owns_elapsed_and_wall_clock_is_irrelevant(self):
        clock = _Clock()
        calls = []
        def readback():
            clock.value += 7
        result = subject.run_timed_schedule(
            [60, 120], command_apply_fn=lambda: calls.append("apply"), readback_fn=readback,
            capture_fn=lambda point: {"point": point, "timing_evidence": {
                "tier": "tier_b", "status": "accepted_best_effort_anchor",
                "provenance": subject.TIMING_CONTRACT_V2["provenance"],
                "best_effort_elapsed_s": float(point),
            }},
            monotonic_fn=clock.monotonic, sleep_fn=clock.sleep,
        )
        self.assertEqual([item.best_effort_exposure_start_elapsed_s for item in result], [60, 120])
        self.assertEqual(calls, ["apply"])

    def test_scheduler_rejects_request_start_or_missing_actual_exposure_provenance(self):
        for capture in (
            {"exposure_start_monotonic_s": 60},
            {"exposure_start_monotonic_s": 60, "exposure_start_provenance": "host_camera_request_start_monotonic"},
        ):
            with self.subTest(capture=capture), self.assertRaisesRegex(ValueError, "best-effort timing"):
                clock = _Clock()
                subject.run_timed_schedule(
                    [60], command_apply_fn=lambda: None, readback_fn=lambda: None,
                    capture_fn=lambda _point, value=capture: value,
                    monotonic_fn=clock.monotonic, sleep_fn=clock.sleep,
                )

    def test_best_effort_timing_boundaries_are_exposed_without_actual_provenance(self):
        plan = subject.build_diagnostic_plan(
            subject.TD_A, source="ray", for_execution=True,
            human_authorization=subject.TD_A, v2_capture_capability=True,
        )
        self.assertTrue(plan["camera"]["v2_capture_timing_capability_available"])
        self.assertFalse(plan["camera"]["actual_exposure_start_provenance_required"])

    def test_execute_plan_fails_before_calls_when_adapter_lacks_actual_exposure_start(self):
        calls = []
        with self.assertRaisesRegex(PermissionError, "v2 capture timing"):
            subject.build_diagnostic_plan(
                subject.TD_A, source="ray", for_execution=True,
                human_authorization=subject.TD_A, exposure_start_capability=False,
            )
        self.assertEqual(calls, [])

    def test_legacy_exposure_capability_cannot_impersonate_remote_v2(self):
        with self.assertRaisesRegex(PermissionError, "remote v2"):
            subject.build_diagnostic_plan(
                subject.TD_A, source="ray", for_execution=True,
                human_authorization=subject.TD_A, exposure_start_capability=True,
            )

    def test_fake_td_a_execution_keeps_ambient_separate_and_counts_all_physical(self):
        plan = subject.build_diagnostic_plan(
            subject.TD_A, source="ray", for_execution=True,
            human_authorization=subject.TD_A, v2_capture_capability=True,
        )
        clock = _Clock()
        gates = []

        def capture(step):
            command = step["command"] or {"strip": "off", "ray": "off"}
            covariate = subject.build_covariate_record(
                source_id=step["source_id"], state_id=step["state_id"], command=command,
                sequence_index=int(step["capture_id"].split("-", 1)[0]),
                capture_order=int(step["capture_id"].split("-", 1)[0]), source_order=int(step.get("source_order", 0)),
                monotonic_timestamp_ns=int(clock.value * 1_000_000_000) + int(step["capture_id"].split("-", 1)[0]),
                wall_clock_timestamp="2026-07-20T00:00:00Z", session_elapsed_s=clock.value,
                source_on_elapsed_s=float(step["requested_elapsed_s"] or 0),
                state_on_elapsed_s=float(step["requested_elapsed_s"] or 0), off_duration_before_s=1800,
                previous_state_id=None, previous_state_dwell_s=None, shutter_seconds=0.01,
                raw_black_levels=[512] * 4, raw_white_level=16383,
                load_history={60: 0, 300: 0, 900: 0}, readback={},
            )
            result = {"thermal_covariates": covariate}
            requested = float(step["requested_elapsed_s"] or 1.0)
            if step["capture_role"] == "ambient":
                result["ambient_diagnostic"] = {"geometry_hash": "g", "black_levels": [512] * 4}
            return _attach_v2_capture_evidence(root, step, result, observed=requested)

        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir) / "run"
            measure.execute_plan(
                plan, run_dir=root, apply_command_fn=lambda _step: {}, readback_fn=lambda _step: {},
                capture_fn=capture,
                both_off_gate_fn=lambda gate_id: gates.append(gate_id) or {
                    "status": "pass", "strip_verified_off": True, "ray_verified_off": True,
                },
                cleanup_fn=lambda: {"status": "pass"},
                monotonic_fn=clock.monotonic, monotonic_ns_fn=lambda: int(clock.value * 1e9), sleep_fn=clock.sleep,
            )
            run = json.loads((root / "run.json").read_text(encoding="utf-8"))
            captures = [json.loads(line) for line in (root / "captures.jsonl").read_text(encoding="utf-8").splitlines()]
        self.assertEqual(run["completed_formal"], 12)
        self.assertEqual(run["ambient_capture_count"], 3)
        self.assertEqual(run["physical_cr3_count"], 15)
        self.assertEqual([row["capture_role"] for row in captures].count("ambient"), 3)
        self.assertIn("run_start", gates)
        self.assertIn("after_cycle_2_ambient_mid", gates)

    def test_isolation_gate_failure_stops_before_capture(self):
        plan = subject.build_diagnostic_plan(
            subject.TD_A, source="ray", for_execution=True,
            human_authorization=subject.TD_A, v2_capture_capability=True,
        )
        captures = []
        with tempfile.TemporaryDirectory() as tempdir, self.assertRaisesRegex(RuntimeError, "both-source"):
            measure.execute_plan(
                plan, run_dir=Path(tempdir) / "run", apply_command_fn=lambda _step: {}, readback_fn=lambda _step: {},
                capture_fn=lambda step: captures.append(step) or {},
                both_off_gate_fn=lambda _gate: {"status": "pass", "strip_verified_off": True, "ray_verified_off": False},
                cleanup_fn=lambda: {"status": "pass"}, monotonic_fn=lambda: 0, sleep_fn=lambda _seconds: None,
            )
        self.assertEqual(captures, [])

    def test_formal_tier_c_timing_fails_closed_before_capture_ledger(self):
        plan = subject.build_diagnostic_plan(
            subject.TD_A, source="ray", for_execution=True,
            human_authorization=subject.TD_A, v2_capture_capability=True,
        )
        def tier_c_capture(step):
            result = {
                "physical_capture_count": 1,
                "thermal_covariates": {
                    "monotonic_timestamp_ns": 1, "wall_clock_timestamp": "x", "session_elapsed_s": 0,
                    "source_id": step["source_id"], "state_id": step["state_id"],
                    "exact_command_hash": subject.canonical_sha256(step["command"] or {"strip": "off", "ray": "off"}),
                    "source_on_elapsed_s": 0, "state_on_elapsed_s": 0, "off_duration_before_s": 0,
                    "previous_state_id": None, "previous_state_dwell_s": None, "sequence_index": 0,
                    "capture_order": 0, "source_order": 0, "ambient_temperature_c": None,
                    "source_surface_temperature_c": None, "fan_mode": None, "power_mode": None,
                    "shutter_seconds": 0.01, "raw_black_levels": [512] * 4, "raw_white_level": 16383,
                    "load_history_proxy_60s": 0, "load_history_proxy_300s": 0, "load_history_proxy_900s": 0,
                },
            }
            if step["capture_role"] == "ambient":
                result["ambient_diagnostic"] = {"geometry_hash": "g", "black_levels": [512] * 4}
            return _attach_v2_capture_evidence(root, step, result, tier="tier_c")
        with tempfile.TemporaryDirectory() as tempdir, self.assertRaisesRegex(RuntimeError, "Tier A/B"):
            root = Path(tempdir) / "run"
            measure.execute_plan(
                plan, run_dir=root, apply_command_fn=lambda _step: {}, readback_fn=lambda _step: {},
                capture_fn=tier_c_capture,
                both_off_gate_fn=lambda _gate: {"status": "pass", "strip_verified_off": True, "ray_verified_off": True},
                cleanup_fn=lambda: {"status": "pass"}, monotonic_fn=lambda: 0, sleep_fn=lambda _seconds: None,
            )

    def test_cleanup_exception_is_retained_and_marks_run_failed(self):
        plan = subject.build_diagnostic_plan(
            subject.TD_A, source="ray", for_execution=True,
            human_authorization=subject.TD_A, v2_capture_capability=True,
        )
        plan = {
            **plan,
            "captures": [],
            "budgets": {"formal_cap": 0, "ambient_cap": 0, "physical_cr3_cap": 0},
            "frozen_shutters": {},
            "exposure_setup_required": [],
            "shutter_ledger_provenance": {
                "owner": "experiment_capture_steps",
                "required_cache_keys": [],
                "frozen_shutters_sha256": subject.canonical_sha256({}),
            },
        }
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir) / "run"
            with self.assertRaisesRegex(RuntimeError, "cleanup failed"):
                measure.execute_plan(
                    plan, run_dir=root, apply_command_fn=lambda _step: {}, readback_fn=lambda _step: {},
                    capture_fn=lambda _step: {},
                    both_off_gate_fn=lambda _gate: {"status": "pass", "strip_verified_off": True, "ray_verified_off": True},
                    cleanup_fn=lambda: (_ for _ in ()).throw(RuntimeError("cleanup failed")),
                monotonic_fn=lambda: 0, sleep_fn=lambda _seconds: None,
            )
            run = json.loads((root / "run.json").read_text(encoding="utf-8"))
            cleanup = json.loads((root / "all-off-python.json").read_text(encoding="utf-8"))
            self.assertEqual(run["status"], "failed")
            self.assertEqual(run["cleanup"], "fail")
            self.assertEqual(cleanup["message"], "cleanup failed")

    def test_rejected_post_capture_timing_retains_physical_ledger_and_failure_evidence(self):
        plan = subject.build_diagnostic_plan(
            subject.TD_A, source="ray", for_execution=True,
            human_authorization=subject.TD_A, v2_capture_capability=True,
        )
        def capture(step):
            root = current_root[0]
            result = {"thermal_covariates": _minimal_covariate(step)}
            return _attach_v2_capture_evidence(root, step, result, observed=64.4)
        current_root = [None]
        with tempfile.TemporaryDirectory() as tempdir, self.assertRaisesRegex(RuntimeError, "non-increasing"):
            root = Path(tempdir) / "run"
            current_root[0] = root
            # Reuse a two-point schedule to exercise a retained CR3 followed by chronology rejection.
            plan = {**plan, "captures": [plan["captures"][1], plan["captures"][2]],
                    "budgets": {"formal_cap": 2, "ambient_cap": 0, "physical_cr3_cap": 22},
                    "frozen_shutters": {"ray-h120-s100": "1/5000"}, "exposure_setup_required": [],
                    "shutter_ledger_provenance": {"owner": "experiment_capture_steps",
                        "required_cache_keys": ["ray-h120-s100"],
                        "frozen_shutters_sha256": subject.canonical_sha256({"ray-h120-s100": "1/5000"})}}
            measure.execute_plan(
                plan, run_dir=root, apply_command_fn=lambda _step: {}, readback_fn=lambda _step: {},
                capture_fn=capture,
                both_off_gate_fn=lambda _gate: {"status": "pass", "strip_verified_off": True, "ray_verified_off": True},
                cleanup_fn=lambda: {"status": "pass"}, monotonic_fn=lambda: 0, sleep_fn=lambda _seconds: None,
            )
            run = json.loads((root / "run.json").read_text(encoding="utf-8"))
            failure = json.loads((root / "failure.json").read_text(encoding="utf-8"))
            self.assertEqual(run["physical_cr3_count"], 2)
            self.assertEqual(failure["rejected_capture"]["current_physical_cr3_count"], 2)
            self.assertNotEqual(
                Path(json.loads((root / "captures.jsonl").read_text().splitlines()[0])["capture"]["saved_file"]),
                Path(failure["rejected_capture"]["cr3_path"]),
            )

    def test_physical_ledger_requires_unique_nonempty_owned_cr3_before_counting(self):
        def minimal_plan(count=1):
            plan = subject.build_diagnostic_plan(
                subject.TD_A, source="ray", for_execution=True,
                human_authorization=subject.TD_A, v2_capture_capability=True,
            )
            steps = plan["captures"][1:1 + count]
            return {**plan, "captures": steps,
                    "budgets": {"formal_cap": count, "ambient_cap": 0, "physical_cr3_cap": 22},
                    "frozen_shutters": {"ray-h120-s100": "1/5000"}, "exposure_setup_required": [],
                    "shutter_ledger_provenance": {"owner": "experiment_capture_steps",
                        "required_cache_keys": ["ray-h120-s100"],
                        "frozen_shutters_sha256": subject.canonical_sha256({"ray-h120-s100": "1/5000"})}}

        def execute(root, plan, capture):
            return measure.execute_plan(
                plan, run_dir=root, apply_command_fn=lambda _step: {}, readback_fn=lambda _step: {},
                capture_fn=capture,
                both_off_gate_fn=lambda _gate: {"status": "pass", "strip_verified_off": True, "ray_verified_off": True},
                cleanup_fn=lambda: {"status": "pass"}, monotonic_fn=lambda: 0, sleep_fn=lambda _seconds: None,
            )

        cases = ("missing", "empty", "outside", "symlink_escape")
        for case in cases:
            with self.subTest(case=case), tempfile.TemporaryDirectory() as tempdir:
                root = Path(tempdir) / "run"
                def capture(step, case=case):
                    result = {"physical_capture_count": 1, "thermal_covariates": _minimal_covariate(step)}
                    if case != "missing":
                        raw = (root / "empty.CR3") if case == "empty" else (root.parent / "outside.CR3")
                        raw.parent.mkdir(parents=True, exist_ok=True)
                        raw.write_bytes(b"" if case == "empty" else b"raw")
                        if case == "symlink_escape":
                            link = root / "escape.CR3"
                            link.symlink_to(raw)
                            raw = link
                        result["saved_file"] = str(raw)
                    return result
                with self.assertRaisesRegex(RuntimeError, "retained nonempty current-run CR3"):
                    execute(root, minimal_plan(), capture)
                run = json.loads((root / "run.json").read_text())
                failure = json.loads((root / "failure.json").read_text())
                self.assertEqual(run["physical_cr3_count"], 0)
                self.assertIsNone(failure["rejected_capture"]["cr3_sha256"])

        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir) / "run"
            def missing_sidecar(step):
                result = _attach_v2_capture_evidence(
                    root, step, {"thermal_covariates": _minimal_covariate(step)},
                    observed=float(step["requested_elapsed_s"]),
                )
                Path(result["remote_metadata_path"]).unlink()
                return result
            with self.assertRaisesRegex(RuntimeError, "sidecar owner"):
                execute(root, minimal_plan(), missing_sidecar)
            run = json.loads((root / "run.json").read_text())
            failure = json.loads((root / "failure.json").read_text())
            self.assertEqual(run["physical_cr3_count"], 1)
            self.assertIsNotNone(failure["rejected_capture"]["cr3_sha256"])
            self.assertIsNone(failure["rejected_capture"]["sidecar_sha256"])

        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir) / "run"
            first_result = {}
            def duplicate(step):
                if not first_result:
                    first_result.update(_attach_v2_capture_evidence(
                        root, step, {"thermal_covariates": _minimal_covariate(step)}, observed=64.4,
                    ))
                    return dict(first_result)
                reused = dict(first_result)
                reused["thermal_covariates"] = _minimal_covariate(step)
                return reused
            with self.assertRaisesRegex(RuntimeError, "reused a CR3"):
                execute(root, minimal_plan(2), duplicate)
            run = json.loads((root / "run.json").read_text())
            self.assertEqual(run["physical_cr3_count"], 1)
            self.assertEqual(len(list(root.glob("*.CR3"))), 1)

    def test_v1_production_plan_is_rejected_before_backend_connect(self):
        plan = subject.build_diagnostic_plan(subject.TD_A, source="ray")
        plan["schema"] = subject.PLAN_SCHEMA_V1
        with self.assertRaisesRegex(PermissionError, "schema v2"):
            measure.validate_authorized_execution_plan(plan)

    def test_deferred_td_b_plan_is_rejected_by_runner_before_calls(self):
        plan = subject.build_diagnostic_plan(subject.TD_B, source="strip")
        plan["status"] = "execute_authorized"
        plan["camera"]["adapter_capability_available"] = True
        plan["camera"]["v2_capture_timing_capability_available"] = True
        plan["execution_authorization"] = {
            "human_authorization_experiment_id": subject.TD_B,
            "human_authorization_verified": True,
            "remote_v2_capability": True,
        }
        calls = []
        with tempfile.TemporaryDirectory() as tempdir, self.assertRaisesRegex(PermissionError, "observed-elapsed|deferred"):
            measure.execute_plan(
                plan, run_dir=Path(tempdir) / "run",
                apply_command_fn=lambda step: calls.append(step) or {}, readback_fn=lambda _step: {},
                capture_fn=lambda _step: {}, both_off_gate_fn=lambda _gate: {},
                cleanup_fn=lambda: {"status": "pass"},
            )
        self.assertEqual(calls, [])

    def test_covariates_recompute_strip_duty_and_reject_command_tampering(self):
        command = {"cw": 518, "ww": 0, "r": 0, "g": 4095, "b": 0}
        curve = json.loads(subject.CURVE_PATH.read_text(encoding="utf-8"))
        row = subject.build_covariate_record(
            source_id="strip", state_id="A", command=command, sequence_index=0,
            capture_order=0, source_order=1, monotonic_timestamp_ns=1,
            wall_clock_timestamp="2026-07-20T00:00:00Z", session_elapsed_s=60,
            source_on_elapsed_s=60, state_on_elapsed_s=60, off_duration_before_s=1800,
            previous_state_id=None, previous_state_dwell_s=None, shutter_seconds=0.01,
            raw_black_levels=[512] * 4, raw_white_level=16383,
            load_history={60: 1, 300: 2, 900: 3}, curve=curve,
        )
        self.assertAlmostEqual(row["sum_duty"], sum(row["linearized_duty"].values()))
        self.assertIsNone(row["ambient_temperature_c"])
        with self.assertRaisesRegex(ValueError, "command hash"):
            subject.validate_covariate_record({**row, "exact_command_hash": "bad"}, expected_command=command)

    def test_dry_run_never_constructs_device_owner_or_cleanup(self):
        with tempfile.TemporaryDirectory() as tempdir, mock.patch.object(measure, "execute_plan") as execute:
            path = measure.write_dry_run(
                experiment_id=subject.TD_A, source="ray", output_dir=tempdir, run_name="td-a-ray-dry",
            )
            plan = json.loads(path.read_text(encoding="utf-8"))
        execute.assert_not_called()
        self.assertEqual(plan["status"], "dry_run_complete_device_locked")
        self.assertEqual(plan["offline_contract"]["device_calls"], 0)

    def test_td_b_v2_dry_run_accepts_explicit_prerequisite_artifact(self):
        with tempfile.TemporaryDirectory() as tempdir:
            path = measure.write_dry_run(
                experiment_id=subject.TD_B, source="strip", output_dir=tempdir,
                run_name="td-b-strip-v2-dry", prerequisite_artifact=subject.OPERATING_ENVELOPE_V2_PATH,
            )
            plan = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(plan["inputs"]["operating_envelope"]["sha256"],
                         subject.file_reference(subject.OPERATING_ENVELOPE_V2_PATH)["sha256"])
        self.assertEqual(plan["timing_resolution"], "developer_override_resolved")
        self.assertEqual(plan["exposure_setup_required"], [])

    def test_execute_cli_fails_before_adapter_binding_without_exact_authorization(self):
        constructs = []
        with self.assertRaises(PermissionError):
            measure.main(
                ["--experiment-id", subject.TD_A, "--source", "ray", "--run-name", "x", "--execute"],
                backend_factory=lambda *args, **kwargs: constructs.append((args, kwargs)),
            )
        self.assertEqual(constructs, [])

    def test_exact_authorized_cli_binds_v2_capability_and_enters_injected_runner(self):
        calls = []

        class FakeBackend:
            backend_name = "remote"
            v2_capture_capability = measure.REMOTE_V2_CAPABILITY

            def connect(self):
                raise AssertionError("fake CLI runner must own whether connect occurs")

            def capture_with_timing(self, **_kwargs):
                raise AssertionError("fake CLI runner does not capture")

        result = measure.main([
                "--experiment-id", subject.TD_A, "--source", "ray", "--run-name", "x", "--execute",
                "--allow-device-control", "--human-authorization", subject.TD_A,
            ], backend_factory=lambda *_args, **_kwargs: FakeBackend(),
            run_fn=lambda plan, **kwargs: calls.append((plan, kwargs)) or Path("fake-run"))
        self.assertEqual(result, 0)
        self.assertEqual(len(calls), 1)
        self.assertTrue(calls[0][0]["camera"]["v2_capture_timing_capability_available"])

    def test_td_b_phase_cli_dispatches_setup_and_disk_release_explicitly(self):
        calls = []

        class FakeBackend:
            backend_name = "remote"
            v2_capture_capability = measure.REMOTE_V2_CAPABILITY

        common = [
            "--experiment-id", subject.TD_B, "--source", "ray", "--run-name", "x",
            "--prerequisite-artifact", str(subject.OPERATING_ENVELOPE_V2_PATH),
            "--execute", "--allow-device-control", "--human-authorization", subject.TD_B,
            "--code-checkpoint", "a" * 40,
        ]
        self.assertEqual(measure.main(
            [*common, "--phase", "setup"],
            backend_factory=lambda *_args, **_kwargs: FakeBackend(),
            setup_fn=lambda plan, **kwargs: calls.append(("setup", plan, kwargs)) or Path("provisional"),
        ), 0)
        release = Path("/Volumes/4T/temp/rgbww-optimizer/fake-release.json")
        self.assertEqual(measure.main(
            [*common, "--phase", "formal", "--setup-release", str(release)],
            backend_factory=lambda *_args, **_kwargs: FakeBackend(),
            resolved_run_fn=lambda path, **kwargs: calls.append(("formal", path, kwargs)) or Path("formal"),
        ), 0)
        self.assertEqual([row[0] for row in calls], ["setup", "formal"])
        self.assertEqual(calls[1][1], release)

    def test_td_b_execute_requires_explicit_phase_before_backend_construction(self):
        constructs = []
        with self.assertRaisesRegex(PermissionError, "explicit --phase"):
            measure.main([
                "--experiment-id", subject.TD_B, "--source", "ray", "--run-name", "x",
                "--prerequisite-artifact", str(subject.OPERATING_ENVELOPE_V2_PATH),
                "--execute", "--allow-device-control", "--human-authorization", subject.TD_B,
                "--code-checkpoint", "a" * 40,
            ], backend_factory=lambda *args, **kwargs: constructs.append((args, kwargs)))
        self.assertEqual(constructs, [])

    def test_td_b_setup_orchestration_dispatches_before_backend_construction(self):
        constructs = []
        calls = []
        result = measure.main([
            "--experiment-id", subject.TD_B, "--source", "ray", "--run-name", "setup",
            "--prerequisite-artifact", str(subject.OPERATING_ENVELOPE_V2_PATH),
            "--execute", "--allow-device-control", "--human-authorization", subject.TD_B,
            "--phase", "setup", "--orchestrate-setup", "--code-checkpoint", "a" * 40,
        ], backend_factory=lambda *args, **kwargs: constructs.append((args, kwargs)),
            setup_orchestrate_fn=lambda **kwargs: calls.append(kwargs) or (
                Path("canonical"), Path("resolved"), Path("release"),
            ))
        self.assertEqual(result, 0)
        self.assertEqual(constructs, [])
        self.assertEqual(len(calls), 1)
        self.assertIn("--phase", calls[0]["wrapper_args"])
        self.assertIn("setup", calls[0]["wrapper_args"])

    def test_td_b_setup_post_wrapper_finalizer_binds_release_and_rejects_tamper(self):
        with tempfile.TemporaryDirectory() as tempdir:
            root = (Path(tempdir) / "setup-run").resolve()
            root.mkdir()
            plan = subject.build_diagnostic_plan(
                subject.TD_B, source="ray", prerequisite_artifact=subject.OPERATING_ENVELOPE_V2_PATH,
                for_execution=True, human_authorization=subject.TD_B, v2_capture_capability=True,
            )
            fake = _fake_td_b_setup(root / "evidence", count=2, fake_only=False)
            fake["code_checkpoint"] = "a" * 40
            (root / "unresolved-plan.json").write_text(json.dumps(plan), encoding="utf-8")
            (root / "all-off-python.json").write_text(json.dumps(fake["cleanup"]["python"]), encoding="utf-8")
            (root / "all-off-shell.json").write_text(json.dumps(fake["cleanup"]["shell"]["steps"]), encoding="utf-8")
            (root / "child-exit-status.txt").write_text("0\n", encoding="utf-8")
            (root / "all-off-shell.exit-status.txt").write_text("0\n", encoding="utf-8")
            wrapper = {
                "schema_version": 1, "experiment": "p7_thermal_diagnostics_v1", "status": "complete",
                "run_dir": str(root), "wrapper_pid": 1, "child_pid": 2, "child_exit_code": 0,
                "shell_cleanup_exit_code": 0, "wrapper_exit_code": 0, "signal": None,
                "started_at": "2026-07-22T00:00:00Z",
            }
            (root / "wrapper-result.json").write_text(json.dumps(wrapper), encoding="utf-8")
            (root / "wrapper-observed-exit.json").write_text(json.dumps({
                "schema": measure.WRAPPER_OBSERVED_EXIT_SCHEMA,
                "status": "exited", "return_code": 0, "observed_at": "2026-07-22T00:00:00Z",
                "wrapper_result": subject.file_reference(root / "wrapper-result.json"),
            }), encoding="utf-8")
            provisional = {
                "schema": subject.TD_B_SETUP_PROVISIONAL_SCHEMA,
                "status": "setup_capture_complete_waiting_for_wrapper_finalize",
                "code_checkpoint": "a" * 40,
                "unresolved_plan": subject.file_reference(root / "unresolved-plan.json"),
                "wrapper_source": subject.file_reference(measure.PRODUCTION_WRAPPER),
                "attempts": fake["attempts"], "historical_seed": fake["historical_seed"],
                "camera": fake["camera"],
                "isolation": {"run_start_zero": fake["cleanup"]["final_both_off"],
                    **fake["isolation"], "setup_complete_zero": fake["cleanup"]["final_both_off"]},
                "cold_proxy": fake["cold_proxy"],
                "python_cleanup": subject.file_reference(root / "all-off-python.json"),
            }
            (root / "setup-provisional.json").write_text(json.dumps(provisional), encoding="utf-8")
            with mock.patch.object(measure, "_validate_checkpoint_and_tree"):
                canonical, resolved, release = measure.finalize_td_b_setup_after_wrapper(
                    root, code_checkpoint="a" * 40,
                    final_zero_fn=lambda: fake["cleanup"]["final_both_off"],
                )
            validated = subject.validate_td_b_setup_release(
                json.loads(release.read_text(encoding="utf-8")), release_path=release,
            )
            self.assertEqual(validated["physical_count"], 2)
            self.assertTrue(validated["resolved_plan"]["formal_capture_eligible"])
            self.assertEqual(validated["resolved_plan"]["setup_physical_cr3_count"], 2)
            self.assertTrue(canonical.is_file())
            self.assertTrue(resolved.is_file())
            evidence_root = os.environ.get("P7_TD_B_E0X_EVIDENCE_DIR")
            if evidence_root:
                shutil.copytree(root, Path(evidence_root) / "setup-roundtrip")
            with (root / "wrapper-result.json").open("a", encoding="utf-8") as handle:
                handle.write(" ")
            with self.assertRaisesRegex(ValueError, "wrapper_result hash"):
                subject.validate_td_b_exposure_setup(
                    json.loads(canonical.read_text(encoding="utf-8")), artifact_path=canonical,
                )

    def test_run_authorized_plan_rejects_before_connect_filesystem_or_cleanup(self):
        class FakeBackend:
            backend_name = "remote"
            v2_capture_capability = measure.REMOTE_V2_CAPABILITY

            def __init__(self):
                self.connect_calls = 0

            def connect(self):
                self.connect_calls += 1
                return object()

            def resolve_capture_settings(self, **_kwargs):
                return camera_gphoto2.CaptureSettings(iso="125", aperture="implicit auto", image_format="RAW")

            def capture_with_timing(self, **_kwargs):
                raise AssertionError("capture must not run")

        authorized = subject.build_diagnostic_plan(
            subject.TD_A, source="ray", for_execution=True,
            human_authorization=subject.TD_A, v2_capture_capability=True,
        )
        dry_run = subject.build_diagnostic_plan(subject.TD_A, source="ray")
        first_formal_index = next(
            index for index, step in enumerate(authorized["captures"]) if step.get("formal_measurement")
        )
        deferred_captures = [dict(step) for step in authorized["captures"]]
        deferred_captures[first_formal_index]["requested_elapsed_s"] = None
        cases = {
            "dry-run": dry_run,
            "wrong experiment": {**authorized, "experiment_id": "forged"},
            "forged status": {**authorized, "status": "ready"},
            "missing v2": {**authorized, "camera": {**authorized["camera"], "v2_capture_timing_capability_available": False}},
            "deferred": {**authorized, "captures": deferred_captures},
        }
        for label, plan in cases.items():
            backend = FakeBackend()
            with self.subTest(label=label), tempfile.TemporaryDirectory() as tempdir:
                output = Path(tempdir) / "must-not-exist"
                with self.assertRaises(PermissionError):
                    measure.run_authorized_plan(plan, output_dir=output, run_name="run", camera_backend=backend)
                self.assertFalse(output.exists())
            self.assertEqual(backend.connect_calls, 0)

        local_backend = FakeBackend()
        local_backend.backend_name = "local"
        with tempfile.TemporaryDirectory() as tempdir, self.assertRaisesRegex(PermissionError, "formal remote v2"):
            measure.run_authorized_plan(
                authorized, output_dir=Path(tempdir) / "must-not-exist", run_name="run",
                camera_backend=local_backend,
            )
        self.assertEqual(local_backend.connect_calls, 0)

    def test_authorized_runner_rejects_shutter_drift_before_backend_connect(self):
        class FakeBackend:
            backend_name = "remote"
            v2_capture_capability = measure.REMOTE_V2_CAPABILITY

            def __init__(self):
                self.connect_calls = 0

            def connect(self):
                self.connect_calls += 1
                return object()

            def resolve_capture_settings(self, **_kwargs):
                raise AssertionError("invalid shutter plan must fail before settings resolution")

            def capture_with_timing(self, **_kwargs):
                raise AssertionError("invalid shutter plan must not capture")

        base = subject.build_diagnostic_plan(
            subject.TD_A, source="ray", for_execution=True,
            human_authorization=subject.TD_A, v2_capture_capability=True,
        )
        missing = {
            **base,
            "frozen_shutters": {"ray-h120-s100": None},
            "exposure_setup_required": ["ray-h120-s100"],
        }
        missing["shutter_ledger_provenance"] = {
            **base["shutter_ledger_provenance"],
            "frozen_shutters_sha256": subject.canonical_sha256(missing["frozen_shutters"]),
        }
        contaminated = {
            **base,
            "frozen_shutters": {**base["frozen_shutters"], "ray-h120-s50": "1/1000"},
        }
        for label, plan in (("missing", missing), ("contaminated", contaminated)):
            backend = FakeBackend()
            with self.subTest(label=label), self.assertRaises(PermissionError):
                measure.run_authorized_plan(
                    plan,
                    output_dir=Path("/Volumes/4T/temp/rgbww-optimizer/p7-r0d-negative"),
                    run_name=label,
                    camera_backend=backend,
                )
            self.assertEqual(backend.connect_calls, 0)

    def test_authorized_runner_resolves_once_and_binds_non_null_settings_to_ambient_and_formal(self):
        for source, formal_shutter in (("ray", "1/5000"), ("strip", "1/320")):
            captured_settings = []
            executed_plans = []
            raw_steps = []

            class FakeCaptureComplete(Exception):
                pass

            class FakeBackend:
                backend_name = "remote"
                v2_capture_capability = measure.REMOTE_V2_CAPABILITY

                def __init__(self):
                    self.connect_calls = 0
                    self.resolve_calls = 0

                def connect(self):
                    self.connect_calls += 1
                    return camera_gphoto2.CameraConnection("fake-remote", "fake://camera")

                def resolve_capture_settings(self, **kwargs):
                    self.resolve_calls += 1
                    self.asserted_request = kwargs
                    return camera_gphoto2.CaptureSettings(
                        iso="125", aperture="implicit auto", shutter_speed="1/100", image_format="RAW"
                    )

                def capture_with_timing(self, **kwargs):
                    captured_settings.append(kwargs["settings"])
                    return object()

            backend = FakeBackend()
            plan = subject.build_diagnostic_plan(
                subject.TD_A, source=source, for_execution=True,
                human_authorization=subject.TD_A, v2_capture_capability=True,
            )

            def adapter_builder(**kwargs):
                def adapter(step):
                    raw_steps.append(dict(step))
                    cache_key = step.get("source_exposure_cache")
                    shutter = "30" if step["source"] == "ambient" else kwargs["frozen_shutter_by_cache"][cache_key]
                    kwargs["timed_capture_fn"](
                        output_dir=kwargs["camera_dir"], filename_template="fake.cr3",
                        settings=camera_gphoto2.CaptureSettings(
                            iso=kwargs["iso"], aperture=kwargs["aperture"],
                            shutter_speed=shutter, image_format=kwargs["image_format"],
                        ),
                    )
                    raise FakeCaptureComplete
                return adapter

            def fake_execute(resolved_plan, **kwargs):
                executed_plans.append(resolved_plan)
                kwargs["set_capture_context_fn"](100.0)
                ambient = next(step for step in resolved_plan["captures"] if step["capture_role"] == "ambient")
                formal = next(step for step in resolved_plan["captures"] if step["formal_measurement"])
                for step in (ambient, formal):
                    try:
                        kwargs["capture_fn"](step)
                    except FakeCaptureComplete:
                        pass
                return Path("fake-run")

            with self.subTest(source=source), mock.patch(
                "camera_based_rgbww_optimizer.optimization.measure_raw_observer_validation.build_native_raw_capture_step_fn",
                side_effect=adapter_builder,
            ), mock.patch.object(measure, "execute_plan", side_effect=fake_execute):
                result = measure.run_authorized_plan(
                    plan,
                    output_dir=Path("/Volumes/4T/temp/rgbww-optimizer/p7-r0d-binding"),
                    run_name=source,
                    camera_backend=backend,
                )
            self.assertEqual(result, Path("fake-run"))
            self.assertEqual(backend.connect_calls, 1)
            self.assertEqual(backend.resolve_calls, 1)
            self.assertEqual(backend.asserted_request, {"iso": None, "aperture": None, "image_format": "RAW"})
            self.assertEqual([item.shutter_speed for item in captured_settings], ["30", formal_shutter])
            self.assertTrue(all(item.iso == "125" for item in captured_settings))
            self.assertTrue(all(item.aperture == "implicit auto" for item in captured_settings))
            self.assertTrue(all(item.image_format == "RAW" for item in captured_settings))
            self.assertNotIn(None, [item.iso for item in captured_settings] + [item.aperture for item in captured_settings])
            self.assertTrue(all(step["auto_exposure"] is False for step in raw_steps))
            self.assertIsNone(raw_steps[0]["source_exposure_cache"])
            self.assertEqual(raw_steps[1]["source_exposure_cache"], next(iter(plan["frozen_shutters"])))
            self.assertEqual(executed_plans[0]["camera"]["resolved_capture_settings"], {
                "owner": "remote_backend.resolve_capture_settings",
                "iso": "125", "aperture": "implicit auto", "image_format": "RAW",
            })

    def test_td_b_authorized_runner_binds_exact_no_ambient_owner(self):
        observed = {}

        class StopAfterBinding(Exception):
            pass

        class FakeBackend:
            backend_name = "remote"
            v2_capture_capability = measure.REMOTE_V2_CAPABILITY

            def connect(self):
                return camera_gphoto2.CameraConnection("fake-remote", "offline")

            def resolve_capture_settings(self, **_kwargs):
                return camera_gphoto2.CaptureSettings(
                    iso="100",
                    aperture="implicit auto",
                    shutter_speed="1/100",
                    image_format="RAW",
                )

            def capture_with_timing(self, **_kwargs):
                raise AssertionError("offline binding test must not reach camera capture")

        plan = subject.build_diagnostic_plan(
            subject.TD_B,
            source="strip",
            prerequisite_artifact=subject.OPERATING_ENVELOPE_V2_PATH,
            for_execution=True,
            human_authorization=subject.TD_B,
            v2_capture_capability=True,
        )

        def adapter_builder(**kwargs):
            observed["builder"] = kwargs

            def adapter(step):
                observed["raw_step"] = dict(step)
                raise StopAfterBinding

            return adapter

        def fake_execute(resolved_plan, **kwargs):
            observed["resolved_plan"] = resolved_plan
            self.assertFalse(any(
                step["capture_role"] == "ambient"
                for step in resolved_plan["captures"]
            ))
            try:
                kwargs["capture_fn"](resolved_plan["captures"][0])
            except StopAfterBinding:
                pass
            return Path("fake-td-b")

        with mock.patch(
            "camera_based_rgbww_optimizer.optimization."
            "measure_raw_observer_validation.build_native_raw_capture_step_fn",
            side_effect=adapter_builder,
        ), mock.patch.object(measure, "execute_plan", side_effect=fake_execute):
            result = measure.run_authorized_plan(
                plan,
                output_dir=Path(
                    "/Volumes/4T/temp/rgbww-optimizer/p7-td-b-f0a-offline/"
                    "fake-production-roundtrip"
                ),
                run_name="strip",
                camera_backend=FakeBackend(),
            )

        self.assertEqual(result, Path("fake-td-b"))
        self.assertEqual(
            observed["builder"]["ambient_policy"],
            subject.AMBIENT_POLICY_UNSUBTRACTED_NO_AMBIENT,
        )
        self.assertEqual(
            observed["builder"]["ambient_policy_owner"],
            measure.raw_validation.TD_B_FORMAL_AMBIENT_POLICY_OWNER,
        )
        self.assertEqual(
            observed["raw_step"]["analysis_context"]["native_raw_ambient_policy"],
            subject.AMBIENT_POLICY_UNSUBTRACTED_NO_AMBIENT,
        )

    def test_production_runner_uses_no_ambient_statistic_only_for_exact_td_b_owner(self):
        feature_ids = json.loads(
            subject.POLICY_PATH.read_text(encoding="utf-8")
        )["feature_set"]["ids"]

        class FakeBackend:
            backend_name = "remote"
            v2_capture_capability = measure.REMOTE_V2_CAPABILITY

            def connect(self):
                return camera_gphoto2.CameraConnection("fake-remote", "offline")

            def resolve_capture_settings(self, **_kwargs):
                return camera_gphoto2.CaptureSettings(
                    iso="100",
                    aperture="implicit auto",
                    shutter_speed="1/100",
                    image_format="RAW",
                )

            def capture_with_timing(self, **_kwargs):
                raise AssertionError("fake RAW adapter owns the offline capture")

        def run(plan, root, *, mutate_context=None):
            observed = {}

            def adapter_builder(**kwargs):
                def adapter(step):
                    report_path = kwargs["measurements_dir"] / (
                        f"{step['capture_id']}.patch-statistics.json"
                    )
                    report_path.parent.mkdir(parents=True, exist_ok=True)
                    report = _c3_native_raw_report(
                        feature_ids,
                        ambient_policy=kwargs["ambient_policy"],
                        phase=plan["stage"],
                    )
                    if mutate_context is not None:
                        mutate_context(report["analysis_context"])
                    report_path.write_text(
                        json.dumps(report),
                        encoding="utf-8",
                    )
                    raw_path = kwargs["camera_dir"] / f"{step['capture_id']}.CR3"
                    raw_path.parent.mkdir(parents=True, exist_ok=True)
                    raw_path.write_bytes(b"synthetic-c3")
                    return {
                        "capture": {"saved_file": str(raw_path)},
                        "saved_file": str(raw_path),
                        "patch_statistics": str(report_path),
                        "timing_metadata": {},
                        "timing_evidence": {
                            "best_effort_elapsed_s": 600.0,
                            "local_readback_done_monotonic_s": 0.0,
                        },
                    }

                return adapter

            def fake_execute(resolved_plan, **kwargs):
                formal = next(
                    step for step in resolved_plan["captures"]
                    if step["formal_measurement"]
                )
                kwargs["set_capture_context_fn"](0.0)
                observed["capture"] = kwargs["capture_fn"](formal)
                return root

            with mock.patch(
                "camera_based_rgbww_optimizer.optimization."
                "measure_raw_observer_validation.build_native_raw_capture_step_fn",
                side_effect=adapter_builder,
            ), mock.patch.object(measure, "execute_plan", side_effect=fake_execute):
                result = measure.run_authorized_plan(
                    plan,
                    output_dir=root.parent,
                    run_name=root.name,
                    camera_backend=FakeBackend(),
                )
            self.assertEqual(result, root)
            return observed["capture"]

        with _w0_temporary_directory() as tempdir:
            root = Path(tempdir)
            td_b = subject.build_diagnostic_plan(
                subject.TD_B,
                source="strip",
                prerequisite_artifact=subject.OPERATING_ENVELOPE_V2_PATH,
                for_execution=True,
                human_authorization=subject.TD_B,
                v2_capture_capability=True,
            )
            captured = run(td_b, root / "td-b")
            self.assertEqual(captured["feature_statistic"], TD_B_FORMAL_FEATURE_STATISTIC)
            self.assertEqual(len(captured["feature_values"]), 58)
            self.assertEqual(list(captured["feature_values"]), feature_ids)

            for label, mutation in (
                (
                    "ambient-subtraction",
                    lambda context: context.__setitem__(
                        "ambient_subtraction_applied", True
                    ),
                ),
                (
                    "phase",
                    lambda context: context.__setitem__("phase", "TD-A"),
                ),
            ):
                with self.subTest(report_context=label), self.assertRaisesRegex(
                    RuntimeError,
                    "report context",
                ):
                    run(
                        td_b,
                        root / f"td-b-{label}",
                        mutate_context=mutation,
                    )

            td_a = subject.build_diagnostic_plan(
                subject.TD_A,
                source="ray",
                for_execution=True,
                human_authorization=subject.TD_A,
                v2_capture_capability=True,
            )
            with self.assertRaises(HsiRejectedFeaturesError) as raised:
                run(td_a, root / "td-a")
            self.assertEqual(len(raised.exception.rejected), 58)
            self.assertTrue(all(
                item["status"] == "missing_statistic"
                for item in raised.exception.rejected
            ))
            self.assertFalse(raised.exception.weak_signal_only)

            mismatched = subject.build_diagnostic_plan(
                subject.TD_B,
                source="strip",
                prerequisite_artifact=subject.OPERATING_ENVELOPE_V2_PATH,
                for_execution=True,
                human_authorization=subject.TD_B,
                v2_capture_capability=True,
            )
            mismatched["native_raw_ambient_policy"] = (
                subject.AMBIENT_POLICY_REQUIRE_PRECEDING
            )
            with self.assertRaisesRegex(PermissionError, "ambient policy"):
                run(mismatched, root / "mismatched")

    def test_authorized_runner_settings_failure_is_before_run_directory_and_lights(self):
        class FakeBackend:
            backend_name = "remote"
            v2_capture_capability = measure.REMOTE_V2_CAPABILITY

            def __init__(self, value):
                self.value = value
                self.connect_calls = 0
                self.resolve_calls = 0

            def connect(self):
                self.connect_calls += 1
                return object()

            def resolve_capture_settings(self, **_kwargs):
                self.resolve_calls += 1
                if isinstance(self.value, BaseException):
                    raise self.value
                return self.value

            def capture_with_timing(self, **_kwargs):
                raise AssertionError("invalid settings must not capture")

        plan = subject.build_diagnostic_plan(
            subject.TD_A, source="ray", for_execution=True,
            human_authorization=subject.TD_A, v2_capture_capability=True,
        )
        invalid = {
            "resolver_error": RuntimeError("invalid remote choice"),
            "null_iso": camera_gphoto2.CaptureSettings(iso=None, aperture="implicit auto", image_format="RAW"),
            "empty_aperture": camera_gphoto2.CaptureSettings(iso="125", aperture="", image_format="RAW"),
            "non_raw": camera_gphoto2.CaptureSettings(iso="125", aperture="implicit auto", image_format="JPEG"),
        }
        for label, value in invalid.items():
            backend = FakeBackend(value)
            output = Path("/Volumes/4T/temp/rgbww-optimizer/p7-r0d-settings-negative") / label
            self.assertFalse(output.exists())
            with self.subTest(label=label), self.assertRaises((PermissionError, RuntimeError)):
                measure.run_authorized_plan(
                    plan, output_dir=output.parent, run_name=output.name, camera_backend=backend,
                )
            self.assertEqual(backend.connect_calls, 1)
            self.assertEqual(backend.resolve_calls, 1)
            self.assertFalse(output.exists())

    def test_operating_envelope_has_no_prefilled_settle(self):
        artifact = json.loads(subject.OPERATING_ENVELOPE_PATH.read_text(encoding="utf-8"))
        self.assertEqual(artifact["status"], "offline_schema_only")
        for key in ("t_settle_ray_s", "t_settle_strip_s", "t_formal_provisional_s", "t_formal_s"):
            self.assertIsNone(artifact[key])
        self.assertEqual(artifact["merge_cold_and_steady_covariance"], "prohibited")

    def test_wrapper_has_independent_cleanup_and_atomic_exit_evidence(self):
        wrapper = (Path(__file__).parents[1] / "tmp/run-p7-thermal-diagnostics.zsh").read_text(encoding="utf-8")
        self.assertIn("trap on_exit EXIT", wrapper)
        self.assertIn("on_signal INT 2", wrapper)
        self.assertIn("on_signal TERM 15", wrapper)
        self.assertIn("on_signal HUP 1", wrapper)
        self.assertIn("camera_based_rgbww_optimizer.control.all_off --json", wrapper)
        self.assertIn("wrapper-result.json", wrapper)
        self.assertIn("child-exit-status.txt", wrapper)
        self.assertIn("cleanup_once", wrapper)

    def test_production_wrapper_real_zsh_runtime_round_trip(self):
        cases = (
            ("success", None, 0, 0, 0, "complete", None),
            ("child_failure", None, 7, 0, 7, "child_failed", None),
            ("cleanup_failure", None, 0, 9, 70, "cleanup_failed", None),
            ("signal_wait", signal.SIGINT, 130, 0, 130, "signaled", "INT"),
            ("signal_wait", signal.SIGTERM, 143, 0, 143, "signaled", "TERM"),
            ("signal_wait", signal.SIGHUP, 129, 0, 129, "signaled", "HUP"),
        )
        for mode, sent_signal, child_code, cleanup_code, wrapper_code, result_status, signal_name in cases:
            with self.subTest(mode=mode, signal=signal_name), _w0_temporary_directory() as tempdir:
                root, wrapper, call_log, source_hash = _make_fake_thermal_wrapper_project(Path(tempdir))
                copied_hash = hashlib.sha256(wrapper.read_bytes()).hexdigest()
                self.assertEqual(copied_hash, source_hash)
                self.assertEqual(
                    wrapper.read_bytes(),
                    (Path(__file__).parents[1] / "tmp/run-p7-thermal-diagnostics.zsh").read_bytes(),
                )
                run_dir = root / "runs" / f"{mode}-{signal_name or 'exit'}"
                state_path = run_dir.parent / f"{run_dir.name}.wrapper-state.json"
                runner_log = run_dir.parent / f"{run_dir.name}.runner.log"
                wrapper_log = run_dir.parent / f"{run_dir.name}.wrapper.log"
                ready_file = Path(tempdir) / "runner-ready"
                env = os.environ.copy()
                env.update({
                    "FAKE_RUNNER_MODE": mode,
                    "FAKE_CALL_LOG": str(call_log),
                    "FAKE_READY_FILE": str(ready_file),
                })
                process = subprocess.Popen(
                    ["zsh", str(wrapper), str(run_dir)],
                    env=env,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    start_new_session=True,
                )
                child_pid = None
                try:
                    if sent_signal is not None:
                        deadline = time.monotonic() + 8
                        while time.monotonic() < deadline:
                            if ready_file.exists() and state_path.exists():
                                running_state = _read_json(state_path)
                                if running_state.get("status") == "running":
                                    break
                            time.sleep(0.02)
                        else:
                            self.fail("fake thermal wrapper did not reach running state")
                        self.assertEqual(running_state["status"], "running")
                        self.assertEqual(running_state["wrapper_pid"], process.pid)
                        child_pid = running_state["child_pid"]
                        os.kill(process.pid, sent_signal)
                    process.wait(timeout=12)
                finally:
                    if process.poll() is None:
                        os.killpg(process.pid, signal.SIGKILL)
                        process.wait(timeout=5)

                calls = call_log.read_text(encoding="utf-8").splitlines()
                runner_calls = [line for line in calls if "measure_p7_thermal_diagnostics" in line]
                cleanup_calls = [line for line in calls if "camera_based_rgbww_optimizer.control.all_off" in line]
                self.assertEqual(len(runner_calls), 1)
                self.assertEqual(len(cleanup_calls), 1)
                self.assertIn("--execute --allow-device-control", runner_calls[0])
                self.assertEqual(process.returncode, wrapper_code)
                self.assertEqual(
                    (run_dir / "child-exit-status.txt").read_text(encoding="utf-8").strip(),
                    str(child_code),
                )
                self.assertEqual(
                    (run_dir / "all-off-shell.exit-status.txt").read_text(encoding="utf-8").strip(),
                    str(cleanup_code),
                )

                expected_keys = {
                    "schema_version", "experiment", "status", "run_dir", "wrapper_pid",
                    "child_pid", "child_exit_code", "shell_cleanup_exit_code",
                    "wrapper_exit_code", "signal", "started_at",
                }
                result = _read_json(run_dir / "wrapper-result.json")
                state = _read_json(state_path)
                self.assertEqual(set(result), expected_keys)
                self.assertEqual(set(state), expected_keys)
                self.assertEqual(result["status"], result_status)
                self.assertEqual(result["experiment"], "p7_thermal_diagnostics_v1")
                self.assertEqual(Path(result["run_dir"]), run_dir.resolve())
                self.assertEqual(result["wrapper_pid"], process.pid)
                self.assertEqual(result["child_exit_code"], child_code)
                self.assertEqual(result["shell_cleanup_exit_code"], cleanup_code)
                self.assertEqual(result["wrapper_exit_code"], wrapper_code)
                self.assertEqual(result["signal"], signal_name)
                self.assertEqual(state["status"], "finished")
                self.assertEqual(state["wrapper_pid"], process.pid)
                self.assertEqual(state["child_pid"], result["child_pid"])
                self.assertEqual(state["wrapper_exit_code"], wrapper_code)
                self.assertEqual(Path(state["run_dir"]), run_dir.resolve())
                self.assertTrue(runner_log.is_file())
                self.assertTrue(wrapper_log.is_file())
                self.assertEqual(list(run_dir.glob(".*.tmp.*")), [])
                self.assertEqual(list(run_dir.parent.glob(".*.tmp.*")), [])
                retained_text = "\n".join(
                    path.read_text(encoding="utf-8", errors="replace")
                    for path in (*run_dir.glob("*"), state_path, runner_log, wrapper_log)
                    if path.is_file()
                ).lower()
                for forbidden in ("secret", "token", "api_key", ".env"):
                    self.assertNotIn(forbidden, retained_text)
                cleanup_stdout = (run_dir / "all-off-shell.json").read_text(encoding="utf-8")
                self.assertIn('"name": "esphome"', cleanup_stdout)
                cleanup_stderr = (run_dir / "all-off-shell.stderr.log").read_text(encoding="utf-8")
                if mode == "cleanup_failure":
                    self.assertIn("fake cleanup failed", cleanup_stderr)
                else:
                    self.assertEqual(cleanup_stderr, "")
                child_pid = result["child_pid"]
                with self.assertRaises(ProcessLookupError):
                    os.kill(child_pid, 0)
                retained_root = os.environ.get("P7_W0_RUNTIME_EVIDENCE_DIR")
                if retained_root:
                    case_name = f"{mode}-{signal_name or 'exit'}"
                    target = Path(retained_root) / case_name
                    target.mkdir(parents=True, exist_ok=False)
                    shutil.copytree(root, target / "project")
                    shutil.copy2(call_log, target / "calls.log")
                    (target / "case-summary.json").write_text(
                        json.dumps({
                            "case": case_name,
                            "child_exit_code": child_code,
                            "shell_cleanup_exit_code": cleanup_code,
                            "wrapper_exit_code": wrapper_code,
                            "status": result_status,
                            "signal": signal_name,
                            "runner_call_count": len(runner_calls),
                            "cleanup_call_count": len(cleanup_calls),
                            "residual_process": False,
                            "production_wrapper_sha256": source_hash,
                        }, indent=2, sort_keys=True) + "\n",
                        encoding="utf-8",
                    )

    def test_setup_wrapper_records_exit_without_predicting_post_exit_finalization(self):
        for mode, expected_exit in (("success", 0), ("child_failure", 7), ("cleanup_failure", 70)):
            with self.subTest(mode=mode), _w0_temporary_directory() as tempdir:
                root, wrapper, call_log, _source_hash = _make_fake_thermal_wrapper_project(Path(tempdir))
                run_dir = root / "runs" / mode
                env = os.environ.copy()
                env.update({"FAKE_RUNNER_MODE": mode, "FAKE_CALL_LOG": str(call_log),
                    "FAKE_READY_FILE": str(Path(tempdir) / "ready")})
                process = subprocess.run(
                    ["zsh", str(wrapper), str(run_dir), "--phase", "setup",
                        "--experiment-id", subject.TD_B, "--source", "ray", "--code-checkpoint", "a" * 40],
                    env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=15,
                )
                calls = call_log.read_text(encoding="utf-8").splitlines()
                runner_calls = [line for line in calls if "measure_p7_thermal_diagnostics" in line]
                cleanup_calls = [line for line in calls if "camera_based_rgbww_optimizer.control.all_off" in line]
                self.assertEqual(len(runner_calls), 1)
                self.assertEqual(len(cleanup_calls), 1)
                finalize_calls = [line for line in calls if "--finalize-setup-run" in line]
                self.assertEqual(finalize_calls, [])
                self.assertEqual(process.returncode, expected_exit)

    def test_setup_outer_orchestrator_finalizes_only_after_real_wrapper_exit(self):
        for mode, expected_exit in (("success", 0), ("child_failure", 7), ("cleanup_failure", 70)):
            with self.subTest(mode=mode), _w0_temporary_directory() as tempdir:
                root, wrapper, call_log, _source_hash = _make_fake_thermal_wrapper_project(Path(tempdir))
                run_dir = root / "runs" / mode
                env = os.environ.copy()
                env.update({"FAKE_RUNNER_MODE": mode, "FAKE_CALL_LOG": str(call_log),
                    "FAKE_READY_FILE": str(Path(tempdir) / "ready")})
                finalized = []

                def fake_finalize(observed_root, *, code_checkpoint):
                    wrapper_result = _read_json(Path(observed_root) / "wrapper-result.json")
                    with self.assertRaises(ProcessLookupError):
                        os.kill(wrapper_result["wrapper_pid"], 0)
                    observed = _read_json(Path(observed_root) / "wrapper-observed-exit.json")
                    self.assertEqual(observed["return_code"], 0)
                    finalized.append((Path(observed_root), code_checkpoint))
                    return tuple(Path(observed_root) / name for name in ("setup.json", "resolved.json", "release.json"))

                with mock.patch.dict(os.environ, env, clear=False):
                    kwargs = {
                        "run_dir": run_dir, "code_checkpoint": "a" * 40,
                        "wrapper_args": ["--phase", "setup", "--experiment-id", subject.TD_B,
                            "--source", "ray", "--code-checkpoint", "a" * 40],
                        "wrapper_path": wrapper, "setup_finalize_fn": fake_finalize,
                        "validate_checkpoint_fn": lambda _checkpoint: None,
                    }
                    if mode == "success":
                        result = measure.orchestrate_td_b_setup(**kwargs)
                        self.assertEqual(result[-1], run_dir.resolve() / "release.json")
                    else:
                        with self.assertRaisesRegex(RuntimeError, f"exit code {expected_exit}"):
                            measure.orchestrate_td_b_setup(**kwargs)
                self.assertEqual(len(finalized), 1 if mode == "success" else 0)
                self.assertEqual(_read_json(run_dir / "wrapper-observed-exit.json")["return_code"], expected_exit)
                evidence_root = os.environ.get("P7_TD_B_E0X_EVIDENCE_DIR")
                if evidence_root and mode == "success":
                    shutil.copytree(root, Path(evidence_root) / "wrapper-roundtrip")
                    shutil.copy2(call_log, Path(evidence_root) / "wrapper-calls.log")

    def test_thermal_wrapper_locals_avoid_zsh_readonly_special_parameters(self):
        wrapper = (Path(__file__).parents[1] / "tmp/run-p7-thermal-diagnostics.zsh").read_text(encoding="utf-8")
        local_names = set()
        for line in wrapper.splitlines():
            stripped = line.strip()
            if not stripped.startswith("local "):
                continue
            for declaration in stripped.removeprefix("local ").split():
                local_names.add(declaration.split("=", 1)[0])
        readonly_special = {
            "status", "pipestatus", "signals", "argv", "ARGC", "RANDOM", "SECONDS",
            "LINENO", "ZSH_SUBSHELL", "ZSH_EVAL_CONTEXT", "ZSH_ARGZERO", "ZSH_PATCHLEVEL",
            "functions", "commands", "modules", "options", "parameters", "dirstack",
            "funcstack", "functrace", "funcsourcetrace", "funcfiletrace", "history",
        }
        self.assertTrue(local_names)
        self.assertEqual(local_names & readonly_special, set())

    def test_td_b_v2_owns_the_only_no_ambient_plan_policy(self):
        td_b_ray = subject.build_diagnostic_plan(subject.TD_B, source="ray")
        td_b_strip = subject.build_diagnostic_plan(subject.TD_B, source="strip")
        for plan in (td_b_ray, td_b_strip):
            self.assertEqual(
                plan["native_raw_ambient_policy"],
                subject.AMBIENT_POLICY_UNSUBTRACTED_NO_AMBIENT,
            )
            self.assertEqual(plan["budgets"]["ambient_cap"], 0)
            self.assertFalse(any(
                step["capture_role"] == "ambient" for step in plan["captures"]
            ))
        for experiment, source in ((subject.TD_A, "ray"), (subject.TD_C, None)):
            plan = subject.build_diagnostic_plan(experiment, source=source)
            self.assertEqual(
                plan["native_raw_ambient_policy"],
                subject.AMBIENT_POLICY_REQUIRE_PRECEDING,
            )

        authorized = subject.build_diagnostic_plan(
            subject.TD_A,
            source="ray",
            for_execution=True,
            human_authorization=subject.TD_A,
            v2_capture_capability=True,
        )
        authorized["native_raw_ambient_policy"] = (
            subject.AMBIENT_POLICY_UNSUBTRACTED_NO_AMBIENT
        )
        with self.assertRaisesRegex(PermissionError, "ambient policy"):
            measure.validate_authorized_execution_plan(authorized)

    def test_physical_return_is_persisted_before_post_return_processing_failure(self):
        plan = subject.build_diagnostic_plan(
            subject.TD_A,
            source="ray",
            for_execution=True,
            human_authorization=subject.TD_A,
            v2_capture_capability=True,
        )
        plan = {
            **plan,
            "captures": [plan["captures"][1]],
            "budgets": {
                "formal_cap": 1,
                "ambient_cap": 0,
                "physical_cr3_cap": 22,
            },
            "frozen_shutters": {"ray-h120-s100": "1/5000"},
            "exposure_setup_required": [],
            "shutter_ledger_provenance": {
                "owner": "experiment_capture_steps",
                "required_cache_keys": ["ray-h120-s100"],
                "frozen_shutters_sha256": subject.canonical_sha256(
                    {"ray-h120-s100": "1/5000"}
                ),
            },
        }
        with _w0_temporary_directory() as tempdir:
            root = Path(tempdir) / "run"
            observer = {}

            def bind(callback):
                observer["callback"] = callback

            def capture(step):
                result = _attach_v2_capture_evidence(
                    root,
                    step,
                    {},
                    observed=float(step["requested_elapsed_s"]),
                )
                observer["callback"](step, result, 1)
                raise HsiRejectedFeaturesError(
                    [{"feature_id": "block_01::R", "status": "rejected"}],
                    weak_signal_only=True,
                )

            with self.assertRaisesRegex(
                HsiRejectedFeaturesError,
                "required HSI observer features were rejected",
            ):
                measure.execute_plan(
                    plan,
                    run_dir=root,
                    apply_command_fn=lambda _step: {},
                    readback_fn=lambda _step: {},
                    capture_fn=capture,
                    both_off_gate_fn=lambda _gate: {
                        "status": "pass",
                        "strip_verified_off": True,
                        "ray_verified_off": True,
                    },
                    cleanup_fn=lambda: {"status": "pass"},
                    bind_physical_return_observer_fn=bind,
                    monotonic_fn=lambda: 0,
                    sleep_fn=lambda _seconds: None,
                )
            run = _read_json(root / "run.json")
            failure = _read_json(root / "failure.json")
            physical = [
                json.loads(line)
                for line in (root / "physical-returns.jsonl").read_text().splitlines()
            ]
            captures = (
                (root / "captures.jsonl").read_text().splitlines()
                if (root / "captures.jsonl").exists()
                else []
            )
            self.assertEqual(run["physical_returned_cr3_count"], 1)
            self.assertEqual(run["accepted_formal_count"], 0)
            self.assertEqual(len(physical), 1)
            self.assertEqual(captures, [])
            self.assertEqual(
                failure["rejected_capture"]["rejection_stage"],
                "post_return_processing",
            )
            sidecar = Path(failure["rejected_capture"]["sidecar_path"])
            self.assertEqual(
                failure["rejected_capture"]["sidecar_byte_count"],
                sidecar.stat().st_size,
            )
            self.assertEqual(
                failure["rejected_capture"]["sidecar_sha256"],
                hashlib.sha256(sidecar.read_bytes()).hexdigest(),
            )
            self.assertEqual(
                failure["rejected_capture"]["sidecar_validation_status"],
                "pass",
            )
            self.assertEqual(physical[0]["sidecar_path"], str(sidecar.resolve()))
            self.assertEqual(physical[0]["sidecar_validation_status"], "pass")
            self.assertEqual(
                failure["rejected_capture"]["remote_capture_id"],
                physical[0]["remote_capture_id"],
            )
            self.assertEqual(
                failure["rejected_capture"]["remote_request_id"],
                physical[0]["remote_request_id"],
            )

    def test_physical_return_sidecar_association_fails_closed_after_counting_cr3(self):
        def minimal_plan():
            plan = subject.build_diagnostic_plan(
                subject.TD_A,
                source="ray",
                for_execution=True,
                human_authorization=subject.TD_A,
                v2_capture_capability=True,
            )
            return {
                **plan,
                "captures": [plan["captures"][1]],
                "budgets": {
                    "formal_cap": 1,
                    "ambient_cap": 0,
                    "physical_cr3_cap": 22,
                },
                "frozen_shutters": {"ray-h120-s100": "1/5000"},
                "exposure_setup_required": [],
                "shutter_ledger_provenance": {
                    "owner": "experiment_capture_steps",
                    "required_cache_keys": ["ray-h120-s100"],
                    "frozen_shutters_sha256": subject.canonical_sha256(
                        {"ray-h120-s100": "1/5000"}
                    ),
                },
            }

        def mutate(case, root, result):
            sidecar = Path(result["remote_metadata_path"])
            if case == "missing":
                sidecar.unlink()
            elif case == "empty":
                sidecar.write_bytes(b"")
            elif case == "outside":
                outside = root.parent / sidecar.name
                sidecar.replace(outside)
                result["remote_metadata_path"] = str(outside)
            elif case == "symlink":
                target = root / "retained-sidecar.json"
                sidecar.replace(target)
                sidecar.symlink_to(target)
            elif case == "same_name_mismatch":
                other = root / "other.metadata.json"
                shutil.copy2(sidecar, other)
                result["remote_metadata_path"] = str(other)
            else:
                metadata = json.loads(sidecar.read_text(encoding="utf-8"))
                if case == "hash":
                    metadata["cr3"]["sha256"] = "0" * 64
                elif case == "id":
                    metadata["capture_id"] = "forged"
                elif case == "metadata":
                    metadata["unexpected_secret"] = "forged"
                sidecar.write_text(json.dumps(metadata), encoding="utf-8")

        for case in (
            "missing",
            "empty",
            "outside",
            "symlink",
            "same_name_mismatch",
            "hash",
            "id",
            "metadata",
        ):
            with self.subTest(case=case), _w0_temporary_directory() as tempdir:
                root = Path(tempdir) / "run"
                observer = {}

                def bind(callback):
                    observer["callback"] = callback

                def capture(step):
                    result = _attach_v2_capture_evidence(
                        root,
                        step,
                        {},
                        observed=float(step["requested_elapsed_s"]),
                    )
                    mutate(case, root, result)
                    observer["callback"](step, result, 1)
                    self.fail("invalid sidecar association must fail in physical return")

                with self.assertRaisesRegex(
                    RuntimeError,
                    "sidecar owner|invalid CR3 sidecar evidence|timing metadata",
                ):
                    measure.execute_plan(
                        minimal_plan(),
                        run_dir=root,
                        apply_command_fn=lambda _step: {},
                        readback_fn=lambda _step: {},
                        capture_fn=capture,
                        both_off_gate_fn=lambda _gate: {
                            "status": "pass",
                            "strip_verified_off": True,
                            "ray_verified_off": True,
                        },
                        cleanup_fn=lambda: {"status": "pass"},
                        bind_physical_return_observer_fn=bind,
                        monotonic_fn=lambda: 0,
                        sleep_fn=lambda _seconds: None,
                    )
                run = _read_json(root / "run.json")
                failure = _read_json(root / "failure.json")
                physical = [
                    json.loads(line)
                    for line in (root / "physical-returns.jsonl")
                    .read_text(encoding="utf-8")
                    .splitlines()
                ]
                self.assertEqual(run["physical_returned_cr3_count"], 1)
                self.assertEqual(run["accepted_formal_count"], 0)
                self.assertEqual(len(physical), 1)
                self.assertTrue(Path(physical[0]["cr3_path"]).is_file())
                self.assertEqual(
                    failure["rejected_capture"]["rejection_stage"],
                    "sidecar_association",
                )
                self.assertEqual(
                    failure["rejected_capture"]["sidecar_validation_status"],
                    "fail",
                )

    def test_post_stat_sidecar_io_failures_preserve_one_physical_owner(self):
        plan = subject.build_diagnostic_plan(
            subject.TD_A,
            source="ray",
            for_execution=True,
            human_authorization=subject.TD_A,
            v2_capture_capability=True,
        )
        plan = {
            **plan,
            "captures": [plan["captures"][1]],
            "budgets": {
                "formal_cap": 1,
                "ambient_cap": 0,
                "physical_cr3_cap": 22,
            },
            "frozen_shutters": {"ray-h120-s100": "1/5000"},
            "exposure_setup_required": [],
            "shutter_ledger_provenance": {
                "owner": "experiment_capture_steps",
                "required_cache_keys": ["ray-h120-s100"],
                "frozen_shutters_sha256": subject.canonical_sha256(
                    {"ray-h120-s100": "1/5000"}
                ),
            },
        }
        original_read_bytes = Path.read_bytes

        for case in ("read_oserror", "removed_after_stat", "replaced_after_stat"):
            with self.subTest(case=case), _w0_temporary_directory() as tempdir:
                root = Path(tempdir) / "run"
                observer = {}

                def bind(callback):
                    observer["callback"] = callback

                def capture(step):
                    result = _attach_v2_capture_evidence(
                        root,
                        step,
                        {},
                        observed=float(step["requested_elapsed_s"]),
                    )
                    sidecar = Path(result["remote_metadata_path"]).resolve()

                    def fail_after_stat(path):
                        if path.resolve() != sidecar:
                            return original_read_bytes(path)
                        if case == "removed_after_stat":
                            path.unlink()
                            return original_read_bytes(path)
                        if case == "replaced_after_stat":
                            path.unlink()
                            path.mkdir()
                            return original_read_bytes(path)
                        raise OSError("synthetic post-stat sidecar read failure")

                    with mock.patch.object(Path, "read_bytes", new=fail_after_stat):
                        observer["callback"](step, result, 1)
                    self.fail("post-stat sidecar I/O failure must reject the capture")

                with self.assertRaisesRegex(
                    RuntimeError,
                    "sidecar owner|sidecar evidence",
                ):
                    measure.execute_plan(
                        plan,
                        run_dir=root,
                        apply_command_fn=lambda _step: {},
                        readback_fn=lambda _step: {},
                        capture_fn=capture,
                        both_off_gate_fn=lambda _gate: {
                            "status": "pass",
                            "strip_verified_off": True,
                            "ray_verified_off": True,
                        },
                        cleanup_fn=lambda: {"status": "pass"},
                        bind_physical_return_observer_fn=bind,
                        monotonic_fn=lambda: 0,
                        sleep_fn=lambda _seconds: None,
                    )
                run = _read_json(root / "run.json")
                failure = _read_json(root / "failure.json")
                physical = [
                    json.loads(line)
                    for line in (root / "physical-returns.jsonl")
                    .read_text(encoding="utf-8")
                    .splitlines()
                ]
                accepted = (
                    (root / "captures.jsonl").read_text(encoding="utf-8").splitlines()
                    if (root / "captures.jsonl").exists()
                    else []
                )
                self.assertEqual(run["physical_returned_cr3_count"], 1)
                self.assertEqual(run["physical_cr3_count"], 1)
                self.assertEqual(run["accepted_formal_count"], 0)
                self.assertEqual(len(physical), 1)
                self.assertEqual(len({row["capture_id"] for row in physical}), 1)
                self.assertTrue(Path(physical[0]["cr3_path"]).is_file())
                self.assertIsNotNone(physical[0]["cr3_sha256"])
                self.assertEqual(accepted, [])
                self.assertEqual(
                    failure["rejected_capture"]["rejection_stage"],
                    "sidecar_association",
                )
                self.assertEqual(
                    failure["rejected_capture"]["cr3_sha256"],
                    physical[0]["cr3_sha256"],
                )
                self.assertEqual(_read_json(root / "all-off-python.json")["status"], "pass")

    def test_adapter_drift_preserves_sidecar_verified_remote_ids(self):
        plan = subject.build_diagnostic_plan(
            subject.TD_A,
            source="ray",
            for_execution=True,
            human_authorization=subject.TD_A,
            v2_capture_capability=True,
        )
        plan = {
            **plan,
            "captures": [plan["captures"][1]],
            "budgets": {
                "formal_cap": 1,
                "ambient_cap": 0,
                "physical_cr3_cap": 22,
            },
            "frozen_shutters": {"ray-h120-s100": "1/5000"},
            "exposure_setup_required": [],
            "shutter_ledger_provenance": {
                "owner": "experiment_capture_steps",
                "required_cache_keys": ["ray-h120-s100"],
                "frozen_shutters_sha256": subject.canonical_sha256(
                    {"ray-h120-s100": "1/5000"}
                ),
            },
        }

        for case in ("timing_metadata", "timing_evidence"):
            with self.subTest(case=case), _w0_temporary_directory() as tempdir:
                root = Path(tempdir) / "run"
                observer = {}
                expected_ids = {}

                def bind(callback):
                    observer["callback"] = callback

                def capture(step):
                    result = _attach_v2_capture_evidence(
                        root,
                        step,
                        {},
                        observed=float(step["requested_elapsed_s"]),
                    )
                    sidecar = json.loads(
                        Path(result["remote_metadata_path"]).read_text(encoding="utf-8")
                    )
                    expected_ids.update({
                        "capture_id": sidecar["capture_id"],
                        "request_id": sidecar["request_id"],
                    })
                    if case == "timing_metadata":
                        result["timing_metadata"] = {
                            **result["timing_metadata"],
                            "capture_id": "adapter-forged",
                        }
                    else:
                        result["timing_evidence"] = {
                            **result["timing_evidence"],
                            "best_effort_elapsed_s": 999.0,
                        }
                    observer["callback"](step, result, 1)
                    self.fail("adapter drift must reject the physical return")

                with self.assertRaisesRegex(
                    RuntimeError,
                    "timing metadata differs|timing evidence differs",
                ):
                    measure.execute_plan(
                        plan,
                        run_dir=root,
                        apply_command_fn=lambda _step: {},
                        readback_fn=lambda _step: {},
                        capture_fn=capture,
                        both_off_gate_fn=lambda _gate: {
                            "status": "pass",
                            "strip_verified_off": True,
                            "ray_verified_off": True,
                        },
                        cleanup_fn=lambda: {"status": "pass"},
                        bind_physical_return_observer_fn=bind,
                        monotonic_fn=lambda: 0,
                        sleep_fn=lambda _seconds: None,
                    )
                run = _read_json(root / "run.json")
                failure = _read_json(root / "failure.json")
                physical = [
                    json.loads(line)
                    for line in (root / "physical-returns.jsonl")
                    .read_text(encoding="utf-8")
                    .splitlines()
                ]
                accepted = (
                    (root / "captures.jsonl").read_text(encoding="utf-8").splitlines()
                    if (root / "captures.jsonl").exists()
                    else []
                )
                self.assertEqual(run["physical_returned_cr3_count"], 1)
                self.assertEqual(run["accepted_formal_count"], 0)
                self.assertEqual(len(physical), 1)
                self.assertEqual(len({row["capture_id"] for row in physical}), 1)
                self.assertEqual(accepted, [])
                self.assertEqual(
                    physical[0]["remote_capture_id"], expected_ids["capture_id"]
                )
                self.assertEqual(
                    physical[0]["remote_request_id"], expected_ids["request_id"]
                )
                self.assertEqual(
                    failure["rejected_capture"]["remote_capture_id"],
                    expected_ids["capture_id"],
                )
                self.assertEqual(
                    failure["rejected_capture"]["remote_request_id"],
                    expected_ids["request_id"],
                )
                self.assertIsNotNone(physical[0]["sidecar_sha256"])
                self.assertEqual(physical[0]["sidecar_validation_status"], "pass")
                self.assertEqual(
                    failure["rejected_capture"]["sidecar_validation_status"],
                    "pass",
                )
                self.assertEqual(_read_json(root / "all-off-python.json")["status"], "pass")

    def test_failed_r1_run_replays_read_only_with_low_signal_and_cleanup_evidence(self):
        C2_TEMP_ROOT.mkdir(parents=True, exist_ok=True)
        before = {
            str(path.relative_to(C1_FAILED_RUN)): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in sorted(C1_FAILED_RUN.rglob("*"))
            if path.is_file()
        }
        with tempfile.TemporaryDirectory(dir=C2_TEMP_ROOT) as tempdir:
            output = Path(tempdir) / "audit"
            artifact_path = measure.audit_post_return_failure(
                C1_FAILED_RUN,
                output,
                expected_cr3_sha256=C1_CR3_SHA256,
                expected_sidecar_sha256=C1_SIDECAR_SHA256,
            )
            artifact = _read_json(artifact_path)
            self.assertEqual(artifact["status"], "pass")
            self.assertTrue(artifact["forensic_only"])
            self.assertFalse(artifact["accepted_formal"])
            self.assertFalse(artifact["reusable_capture"])
            self.assertEqual(artifact["physical"], {
                "setup": 2,
                "returned": 1,
                "total": 3,
                "accepted_formal": 0,
            })
            self.assertEqual(artifact["recorded_exposure"]["source"], "Canon:ExposureTime")
            self.assertEqual(artifact["timing_evidence"]["tier"], "tier_b")
            self.assertEqual(len(artifact["rejected_planes"]), 6)
            self.assertTrue(all(
                row["failures"] == ["near_noise_floor_fraction_exceeded"]
                for row in artifact["rejected_planes"]
            ))
            self.assertEqual(artifact["cleanup"], "pass")
            self.assertEqual(artifact["independent_final_zero"], "pass")
            self.assertEqual(artifact["immutable_input_file_count"], len(before))
            self.assertEqual(artifact["immutable_input_sha256"], before)
            self.assertTrue(any(name.endswith(".cr3") for name in before))
            self.assertTrue(any(name.endswith(".cr3.metadata.json") for name in before))
            self.assertTrue(any(name.endswith(".patch-statistics.json") for name in before))
        after = {
            str(path.relative_to(C1_FAILED_RUN)): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in sorted(C1_FAILED_RUN.rglob("*"))
            if path.is_file()
        }
        self.assertEqual(after, before)

    def test_setup_release_lineage_candidate_is_planner_only_and_fail_closed(self):
        release = Path(
            "/Volumes/4T/temp/rgbww-optimizer/p7-thermal-diagnostics/"
            "p7-td-b-canon-r2-setup-20260723-042002/setup-release.json"
        )
        candidate = subject.build_td_b_setup_release_lineage_candidate(
            release,
            old_checkpoint=subject.TD_B_SETUP_CHECKPOINT,
            new_checkpoint="b" * 40,
            changed_paths=[
                ".agent-work/PLAN.md",
                "src/camera_based_rgbww_optimizer/optimization/hsi_objective.py",
                "src/camera_based_rgbww_optimizer/optimization/"
                "measure_raw_observer_validation.py",
                "tests/test_hsi_objective.py",
                "tests/test_p7_thermal_diagnostics.py",
                "docs/README.md",
            ],
        )
        self.assertEqual(candidate["status"], "eligible_waiting_for_planner")
        self.assertFalse(candidate["production_release_usable"])
        self.assertTrue(candidate["planner_acceptance_required"])

        ineligible = subject.build_td_b_setup_release_lineage_candidate(
            release,
            old_checkpoint=subject.TD_B_SETUP_CHECKPOINT,
            new_checkpoint="c" * 40,
            changed_paths=["src/camera_based_rgbww_optimizer/control/unreviewed.py"],
        )
        self.assertEqual(ineligible["status"], "ineligible_requires_new_setup")
        self.assertEqual(
            ineligible["prohibited_paths"],
            ["src/camera_based_rgbww_optimizer/control/unreviewed.py"],
        )
        with _w0_temporary_directory() as tempdir:
            candidate_path = Path(tempdir) / "lineage-candidate.json"
            candidate_path.write_text(json.dumps(candidate), encoding="utf-8")
            backend = mock.Mock()
            with mock.patch.object(measure, "_validate_checkpoint_and_tree"):
                with self.assertRaisesRegex(ValueError, "release schema"):
                    measure.run_resolved_td_b_formal(
                        candidate_path,
                        output_dir=Path(tempdir) / "runs",
                        run_name="must-not-run",
                        camera_backend=backend,
                        code_checkpoint="b" * 40,
                    )
            backend.connect.assert_not_called()

    def test_lineage_release_rebuilds_current_plan_and_reaches_formal_runner(self):
        checkpoint = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=Path(__file__).parents[1],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        with _w0_temporary_directory() as tempdir:
            release_path = measure.write_td_b_setup_lineage_release(
                output_dir=tempdir,
                run_name="lineage-release",
                code_checkpoint=checkpoint,
                validate_checkpoint_fn=lambda _checkpoint: None,
                changed_paths_fn=lambda _old, _new: _allowed_lineage_changed_paths_fixture(),
            )
            release = _read_json(release_path)
            validated = subject.validate_td_b_setup_lineage_release(
                release,
                release_path=release_path,
                changed_paths_fn=lambda _old, _new: _allowed_lineage_changed_paths_fixture(),
            )
            resolved = validated["resolved_plan"]
            self.assertTrue(release["production_release_usable"])
            self.assertEqual(release["code_checkpoint"], checkpoint)
            self.assertEqual(resolved["native_raw_ambient_policy"], "unsubtracted_no_ambient")
            self.assertEqual(resolved["budgets"]["formal_cap"], 16)
            self.assertEqual(resolved["budgets"]["ambient_cap"], 0)
            self.assertEqual(resolved["setup_physical_cr3_count"], 2)
            self.assertEqual(len(resolved["captures"]), 16)
            self.assertTrue(all(row["capture_role"] == "formal" for row in resolved["captures"]))

            sentinel = Path(tempdir) / "formal-run"
            backend = mock.Mock()
            backend.backend_name = "remote"
            backend.v2_capture_capability = measure.REMOTE_V2_CAPABILITY
            backend.connect = mock.Mock()
            backend.resolve_capture_settings = mock.Mock()
            backend.capture_with_timing = mock.Mock()
            lineage_validator = subject.validate_td_b_setup_lineage_release

            def validate_with_fixture(release, *, release_path):
                return lineage_validator(
                    release,
                    release_path=release_path,
                    changed_paths_fn=lambda _old, _new: _allowed_lineage_changed_paths_fixture(),
                )

            with mock.patch.object(measure, "_validate_checkpoint_and_tree"), mock.patch.object(
                measure,
                "run_authorized_plan",
                return_value=sentinel,
            ) as run_mock, mock.patch.object(
                subject,
                "validate_td_b_setup_lineage_release",
                side_effect=validate_with_fixture,
            ):
                result = measure.run_resolved_td_b_formal(
                    release_path,
                    output_dir=Path(tempdir) / "runs",
                    run_name="ray",
                    camera_backend=backend,
                    code_checkpoint=checkpoint,
                )
            self.assertEqual(result, sentinel)
            run_mock.assert_called_once()
            self.assertEqual(
                run_mock.call_args.args[0]["native_raw_ambient_policy"],
                "unsubtracted_no_ambient",
            )

    def test_lineage_release_rejects_candidate_and_resolved_plan_tampering(self):
        checkpoint = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=Path(__file__).parents[1],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        with _w0_temporary_directory() as tempdir:
            release_path = measure.write_td_b_setup_lineage_release(
                output_dir=tempdir,
                run_name="lineage-release",
                code_checkpoint=checkpoint,
                validate_checkpoint_fn=lambda _checkpoint: None,
                changed_paths_fn=lambda _old, _new: _allowed_lineage_changed_paths_fixture(),
            )
            release = _read_json(release_path)
            candidate_path = Path(release["current_lineage_candidate"]["path"])
            candidate = _read_json(candidate_path)
            candidate["new_checkpoint"] = "f" * 40
            candidate_path.write_text(json.dumps(candidate), encoding="utf-8")
            release["current_lineage_candidate"] = subject.file_reference(candidate_path)
            release_path.write_text(json.dumps(release), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "current lineage candidate"):
                subject.validate_td_b_setup_lineage_release(
                    release,
                    release_path=release_path,
                    changed_paths_fn=lambda _old, _new: _allowed_lineage_changed_paths_fixture(),
                )

        with _w0_temporary_directory() as tempdir:
            release_path = measure.write_td_b_setup_lineage_release(
                output_dir=tempdir,
                run_name="lineage-release",
                code_checkpoint=checkpoint,
                validate_checkpoint_fn=lambda _checkpoint: None,
                changed_paths_fn=lambda _old, _new: _allowed_lineage_changed_paths_fixture(),
            )
            release = _read_json(release_path)
            resolved_path = Path(release["resolved_formal_plan"]["path"])
            resolved = _read_json(resolved_path)
            resolved["budgets"]["ambient_cap"] = 1
            resolved_path.write_text(json.dumps(resolved), encoding="utf-8")
            release["resolved_formal_plan"] = subject.file_reference(resolved_path)
            release_path.write_text(json.dumps(release), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "resolved plan"):
                subject.validate_td_b_setup_lineage_release(
                    release,
                    release_path=release_path,
                    changed_paths_fn=lambda _old, _new: _allowed_lineage_changed_paths_fixture(),
                )

        with _w0_temporary_directory() as tempdir:
            release_path = measure.write_td_b_setup_lineage_release(
                output_dir=tempdir,
                run_name="lineage-release",
                code_checkpoint=checkpoint,
                validate_checkpoint_fn=lambda _checkpoint: None,
                changed_paths_fn=lambda _old, _new: _allowed_lineage_changed_paths_fixture(),
            )
            symlink = Path(tempdir) / "release-link.json"
            symlink.symlink_to(release_path)
            with self.assertRaisesRegex(ValueError, "symlink"):
                subject.validate_td_b_setup_lineage_release(
                    _read_json(release_path),
                    release_path=symlink,
                    changed_paths_fn=lambda _old, _new: _allowed_lineage_changed_paths_fixture(),
                )

        with _w0_temporary_directory() as tempdir:
            with self.assertRaisesRegex(PermissionError, "prohibited"):
                measure.write_td_b_setup_lineage_release(
                    output_dir=tempdir,
                    run_name="lineage-release",
                    code_checkpoint=checkpoint,
                    validate_checkpoint_fn=lambda _checkpoint: None,
                    changed_paths_fn=lambda _old, _new: [
                        "src/camera_based_rgbww_optimizer/control/unreviewed.py"
                    ],
                )

    def test_current_head_lineage_accepts_exact_human_policy_freeze(self):
        checkpoint = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=Path(__file__).parents[1],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        changed_paths = subject.changed_paths_between_checkpoints(
            subject.TD_B_SETUP_CHECKPOINT,
            checkpoint,
        )
        candidate = subject.build_td_b_setup_release_lineage_candidate(
            subject.TD_B_SETUP_RELEASE_PATH,
            old_checkpoint=subject.TD_B_SETUP_CHECKPOINT,
            new_checkpoint=checkpoint,
            changed_paths=changed_paths,
        )
        self.assertEqual(changed_paths, sorted(changed_paths))
        prohibited = set(candidate["prohibited_paths"])
        classifications = {
            row["path"]: row["classification"]
            for row in candidate["changed_paths"]
        }
        self.assertNotIn("AGENTS.md", prohibited)
        self.assertEqual(
            classifications["AGENTS.md"],
            "bounded_validation_or_documentation",
        )
        self.assertEqual(
            classifications[".agent-work/FULL_PLAN_REFERENCE.md"],
            "planner_or_execution_audit_only",
        )
        self.assertNotIn(".agent-work/FULL_PLAN_REFERENCE.md", prohibited)
        for path, classification in subject.TD_B_WORKFLOW_PATH_CLASSIFICATIONS.items():
            self.assertNotIn(path, prohibited)
            self.assertEqual(
                classifications[path],
                subject.TD_B_PUBLIC_DEFAULT_SUCCESSOR_CLASSIFICATIONS.get(
                    path, classification,
                ),
            )
        for path, classification in (
            subject.TD_B_PUBLIC_DEFAULT_SUCCESSOR_CLASSIFICATIONS.items()
        ):
            self.assertNotIn(path, prohibited)
            self.assertEqual(classifications[path], classification)
        for path, classification in subject.TD_B_CLEANUP_TEST_PROVENANCE_CLASSIFICATIONS.items():
            self.assertNotIn(path, prohibited)
            self.assertEqual(classifications[path], classification)
        self.assertEqual(candidate["new_checkpoint"], checkpoint)
        workflow_only = subject.build_td_b_setup_release_lineage_candidate(
            subject.TD_B_SETUP_RELEASE_PATH,
            old_checkpoint=subject.TD_B_SETUP_CHECKPOINT,
            new_checkpoint=checkpoint,
            changed_paths=list(subject.TD_B_WORKFLOW_PATH_CLASSIFICATIONS),
        )
        self.assertEqual(workflow_only["status"], "eligible_waiting_for_planner")
        self.assertEqual(workflow_only["prohibited_paths"], [])

    def test_post_eq_policy_lineage_classifies_only_exact_accepted_paths(self):
        checkpoint = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=Path(__file__).parents[1],
            check=True, capture_output=True, text=True,
        ).stdout.strip()
        expected = {
            "config/hsi/p7-ray-td-b-exposure-policy-v2.json":
                "accepted_post_eq_exposure_policy_contract",
            "tests/test_p7_td_b_r6_contract.py":
                "accepted_post_eq_exposure_policy_validation",
        }
        candidate = subject.build_td_b_setup_release_lineage_candidate(
            subject.TD_B_SETUP_RELEASE_PATH,
            old_checkpoint=subject.TD_B_SETUP_CHECKPOINT,
            new_checkpoint=checkpoint,
            changed_paths=sorted(expected),
        )
        self.assertEqual(
            {row["path"]: row["classification"] for row in candidate["changed_paths"]},
            expected,
        )
        self.assertEqual(candidate["status"], "eligible_waiting_for_planner")
        self.assertEqual(candidate["prohibited_paths"], [])

        changed_paths = subject.changed_paths_between_checkpoints(
            subject.TD_B_SETUP_CHECKPOINT,
            checkpoint,
        )
        full_candidate = subject.build_td_b_setup_release_lineage_candidate(
            subject.TD_B_SETUP_RELEASE_PATH,
            old_checkpoint=subject.TD_B_SETUP_CHECKPOINT,
            new_checkpoint=checkpoint,
            changed_paths=changed_paths,
        )
        self.assertEqual(len(changed_paths), 59)
        self.assertEqual(full_candidate["status"], "eligible_waiting_for_planner")
        self.assertEqual(full_candidate["prohibited_paths"], [])
        self.assertEqual(dict(subject.TD_B_POST_EQ_POLICY_CLASSIFICATIONS), expected)
        self.assertEqual(
            dict(subject._validate_td_b_post_eq_policy_lineage(
                new_checkpoint=checkpoint,
            )),
            expected,
        )
        for path, expected_sha256 in subject.TD_B_POST_EQ_POLICY_BLOB_SHA256.items():
            accepted = subprocess.run(
                ["git", "show", f"{subject.TD_B_POST_EQ_POLICY_COMMIT}:{path}"],
                cwd=Path(__file__).parents[1], check=True, capture_output=True,
            ).stdout
            self.assertEqual(hashlib.sha256(accepted).hexdigest(), expected_sha256)
            if path in expected:
                self.assertEqual(
                    (Path(__file__).parents[1] / path).read_bytes(),
                    accepted,
                )

    def test_post_eq_policy_lineage_fails_closed_without_widening(self):
        root = Path(__file__).parents[1]
        checkpoint = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=root,
            check=True, capture_output=True, text=True,
        ).stdout.strip()
        neighboring = [
            "config/hsi/p7-ray-td-b-exposure-policy-v3.json",
            "tests/test_p7_td_b_r7_contract.py",
            "src/camera_based_rgbww_optimizer/control/unreviewed.py",
        ]
        candidate = subject.build_td_b_setup_release_lineage_candidate(
            subject.TD_B_SETUP_RELEASE_PATH,
            old_checkpoint=subject.TD_B_SETUP_CHECKPOINT,
            new_checkpoint=checkpoint,
            changed_paths=neighboring,
        )
        self.assertEqual(candidate["prohibited_paths"], neighboring)
        self.assertTrue(all(
            row["classification"] == "prohibited_or_unreviewed"
            for row in candidate["changed_paths"]
        ))
        self.assertFalse(
            set(subject.TD_B_POST_EQ_POLICY_CLASSIFICATIONS)
            & set(subject.TD_B_LINEAGE_ALLOWED_PRODUCTION_PATHS)
        )
        self.assertFalse(
            set(subject.TD_B_POST_EQ_POLICY_CLASSIFICATIONS)
            & set(subject.TD_B_LINEAGE_ALLOWED_VALIDATION_PATHS)
        )

        with self.assertRaisesRegex(ValueError, "ancestry differs"):
            subject._validate_td_b_post_eq_policy_lineage(
                new_checkpoint=subject.TD_B_POST_EQ_POLICY_PARENT,
            )
        for name, replacement, message in (
            ("TD_B_POST_EQ_POLICY_PARENT", "0" * 40, "parent differs"),
            ("TD_B_POST_EQ_POLICY_SUBJECT", "wrong", "subject differs"),
            ("TD_B_POST_EQ_POLICY_PATHS_SHA256", "0" * 64, "path set differs"),
        ):
            with self.subTest(name=name), mock.patch.object(subject, name, replacement):
                with self.assertRaisesRegex(ValueError, message):
                    subject._validate_td_b_post_eq_policy_lineage(
                        new_checkpoint=checkpoint,
                    )

        accepted_path = next(iter(subject.TD_B_POST_EQ_POLICY_BLOB_SHA256))
        changed_hashes = dict(subject.TD_B_POST_EQ_POLICY_BLOB_SHA256)
        changed_hashes[accepted_path] = "0" * 64
        with mock.patch.object(
            subject,
            "TD_B_POST_EQ_POLICY_BLOB_SHA256",
            changed_hashes,
        ):
            with self.assertRaisesRegex(ValueError, "accepted blob differs"):
                subject._validate_td_b_post_eq_policy_lineage(
                    new_checkpoint=checkpoint,
                )

        mapped_path = next(iter(subject.TD_B_POST_EQ_POLICY_CLASSIFICATIONS))
        original_run = subprocess.run
        mapped_show_calls = 0
        target_show = ["git", "show", f"{checkpoint}:{mapped_path}"]

        def drift_checkpoint(command, *args, **kwargs):
            nonlocal mapped_show_calls
            if command == target_show:
                mapped_show_calls += 1
                return subprocess.CompletedProcess(command, 0, stdout=b"drift")
            return original_run(command, *args, **kwargs)

        with mock.patch.object(subject.subprocess, "run", side_effect=drift_checkpoint):
            with self.assertRaisesRegex(ValueError, "checkpoint blob differs"):
                subject._validate_td_b_post_eq_policy_lineage(
                    new_checkpoint=checkpoint,
                )
        self.assertEqual(mapped_show_calls, 1)

        mapped_owner = (root / mapped_path).resolve()
        original_read_bytes = Path.read_bytes

        def drift_working(path):
            if path.resolve() == mapped_owner:
                return b"drift"
            return original_read_bytes(path)

        with mock.patch.object(Path, "read_bytes", drift_working):
            with self.assertRaisesRegex(ValueError, "working owner differs"):
                subject._validate_td_b_post_eq_policy_lineage(
                    new_checkpoint=checkpoint,
                )
        original_is_symlink = Path.is_symlink

        def mapped_symlink(path):
            return path.resolve() == mapped_owner or original_is_symlink(path)

        with mock.patch.object(Path, "is_symlink", mapped_symlink):
            with self.assertRaisesRegex(ValueError, "working owner differs"):
                subject._validate_td_b_post_eq_policy_lineage(
                    new_checkpoint=checkpoint,
                )
        original_is_file = Path.is_file

        def mapped_missing(path):
            return False if path.resolve() == mapped_owner else original_is_file(path)

        with mock.patch.object(Path, "is_file", mapped_missing):
            with self.assertRaisesRegex(ValueError, "working owner differs"):
                subject._validate_td_b_post_eq_policy_lineage(
                    new_checkpoint=checkpoint,
                )
        with self.assertRaisesRegex(ValueError, "duplicates"):
            subject.build_td_b_setup_release_lineage_candidate(
                subject.TD_B_SETUP_RELEASE_PATH,
                old_checkpoint=subject.TD_B_SETUP_CHECKPOINT,
                new_checkpoint=checkpoint,
                changed_paths=[mapped_path, mapped_path],
            )
        with self.assertRaisesRegex(ValueError, "repository-relative"):
            subject.build_td_b_setup_release_lineage_candidate(
                subject.TD_B_SETUP_RELEASE_PATH,
                old_checkpoint=subject.TD_B_SETUP_CHECKPOINT,
                new_checkpoint=checkpoint,
                changed_paths=["../outside.py"],
            )

    def test_public_default_successor_lineage_layers_historical_and_current_owners(self):
        checkpoint = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=Path(__file__).parents[1],
            check=True, capture_output=True, text=True,
        ).stdout.strip()
        successor = subject._validate_td_b_public_default_successor_lineage(
            new_checkpoint=checkpoint,
        )
        historical = subject._validate_td_b_workflow_path_lineage(
            new_checkpoint=checkpoint,
        )
        overlap = set(successor).intersection(historical)
        self.assertEqual(overlap, {
            "docs/local-lab-connection-boundary.md",
            "src/camera_based_rgbww_optimizer/control/ray120c.py",
            "tests/test_all_off.py",
            "tests/test_project_context_docs.py",
            "tests/test_ray120c.py",
        })
        self.assertEqual(
            successor["src/camera_based_rgbww_optimizer/control/ray120c.py"],
            "human_directed_public_shared_protocol_default_boundary",
        )

        unchanged = "docs/engineering/p7-td-b-contract-history.md"
        original_run = subprocess.run

        def drift_checkpoint(command, *args, **kwargs):
            if command == ["git", "show", f"{checkpoint}:{unchanged}"]:
                return subprocess.CompletedProcess(command, 0, stdout=b"drift")
            return original_run(command, *args, **kwargs)

        with mock.patch.object(subject.subprocess, "run", side_effect=drift_checkpoint):
            with self.assertRaisesRegex(ValueError, f"hash or diff differs: {unchanged}"):
                subject._validate_td_b_workflow_path_lineage(
                    new_checkpoint=checkpoint,
                )

    def test_governance_lineage_successor_accepts_exact_authorized_history_and_preserves_canonical_owner(self):
        root = Path(__file__).parents[1]
        checkpoint = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=root, check=True,
            capture_output=True, text=True,
        ).stdout.strip()
        canonical = subject.TD_B_GOVERNANCE_LINEAGE_SUCCESSOR_PATH.read_bytes()
        manifest = json.loads(canonical)
        self.assertEqual(
            canonical,
            json.dumps(
                manifest, sort_keys=True, separators=(",", ":"), allow_nan=False,
            ).encode("utf-8") + b"\n",
        )
        self.assertEqual(
            set(manifest["changed_path_ledger"]), {"argv", "count", "lf_sha256"},
        )
        self.assertEqual(manifest["changed_path_ledger"]["count"], 181)
        self.assertEqual(
            manifest["changed_path_ledger"]["argv"],
            [
                "git", "diff", "--name-only",
                subject.TD_B_GOVERNANCE_LINEAGE_SUCCESSOR_PARENT,
                subject.TD_B_GOVERNANCE_LINEAGE_SUCCESSOR_COMMIT,
            ],
        )
        classifications = subject._validate_td_b_governance_lineage_successor(
            new_checkpoint=checkpoint,
        )
        self.assertEqual(dict(classifications), {
            ".agents/skills/camera-based-rgbww-optimizer/SKILL.md":
                "bounded_validation_or_documentation",
            "AGENTS.md": "bounded_validation_or_documentation",
        })
        self.assertFalse(
            {"eligibility", "eligible", "release", "production_release_usable"}
            .intersection(classifications)
        )
        subject._validate_td_b_agents_policy_lineage(
            old_checkpoint=subject.TD_B_SETUP_CHECKPOINT,
            new_checkpoint=checkpoint,
        )
        subject._validate_td_b_public_default_successor_lineage(
            new_checkpoint=checkpoint,
        )
        candidate = subject.build_td_b_setup_release_lineage_candidate(
            subject.TD_B_SETUP_RELEASE_PATH,
            old_checkpoint=subject.TD_B_SETUP_CHECKPOINT,
            new_checkpoint=checkpoint,
            changed_paths=list(classifications),
        )
        self.assertEqual(candidate["status"], "eligible_waiting_for_planner")
        self.assertFalse(candidate["production_release_usable"])
        self.assertTrue(candidate["planner_acceptance_required"])
        self.assertNotIn("eligibility", classifications)

    def test_governance_lineage_successor_fails_closed_on_exact_drift_without_widening(self):
        root = Path(__file__).parents[1]
        checkpoint = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=root, check=True,
            capture_output=True, text=True,
        ).stdout.strip()
        canonical = subject.TD_B_GOVERNANCE_LINEAGE_SUCCESSOR_PATH.read_bytes()

        with _w0_temporary_directory() as tempdir:
            temp = Path(tempdir)
            copied = temp / "governance-successor.json"
            copied.write_bytes(canonical)

            def canonical_bytes(value):
                return json.dumps(
                    value, sort_keys=True, separators=(",", ":"), allow_nan=False,
                ).encode("utf-8") + b"\n"

            def reject_bytes(label, payload, message=None):
                changed = temp / f"{label}.json"
                changed.write_bytes(payload)
                expected = hashlib.sha256(payload).hexdigest()
                assertion = (
                    self.assertRaisesRegex(ValueError, message)
                    if message else self.assertRaises(ValueError)
                )
                with assertion:
                    subject._validate_td_b_governance_lineage_successor(
                        new_checkpoint=checkpoint,
                        manifest_path=changed,
                        require_canonical_manifest_owner=False,
                        expected_manifest_sha256=expected,
                    )

            def reject_mutation(label, mutate, message=None):
                value = json.loads(canonical)
                mutate(value)
                reject_bytes(label, canonical_bytes(value), message)

            with self.assertRaisesRegex(ValueError, "owner differs"):
                subject._validate_td_b_governance_lineage_successor(
                    new_checkpoint=checkpoint, manifest_path=copied,
                )
            subject._validate_td_b_governance_lineage_successor(
                new_checkpoint=checkpoint, manifest_path=copied,
                require_canonical_manifest_owner=False,
            )
            tampered = canonical[:-2] + b"0\n"
            changed = temp / "whole-file-hash.json"
            changed.write_bytes(tampered)
            with self.assertRaisesRegex(ValueError, "hash differs"):
                subject._validate_td_b_governance_lineage_successor(
                    new_checkpoint=checkpoint, manifest_path=changed,
                    require_canonical_manifest_owner=False,
                )
            missing = temp / "missing.json"
            with self.assertRaisesRegex(ValueError, "missing"):
                subject._validate_td_b_governance_lineage_successor(
                    new_checkpoint=checkpoint, manifest_path=missing,
                    require_canonical_manifest_owner=False,
                )
            directory = temp / "directory.json"
            directory.mkdir()
            with self.assertRaisesRegex(ValueError, "non-regular"):
                subject._validate_td_b_governance_lineage_successor(
                    new_checkpoint=checkpoint, manifest_path=directory,
                    require_canonical_manifest_owner=False,
                )
            link = temp / "link.json"
            link.symlink_to(copied)
            with self.assertRaisesRegex(ValueError, "symlink"):
                subject._validate_td_b_governance_lineage_successor(
                    new_checkpoint=checkpoint, manifest_path=link,
                    require_canonical_manifest_owner=False,
                )

            reject_bytes("malformed", b"{", "JSON differs")
            reject_bytes(
                "duplicate-key",
                canonical.replace(b'"count":181', b'"count":181,"count":181'),
                "JSON differs",
            )
            reject_bytes(
                "non-finite", canonical.replace(b'"count":181', b'"count":NaN'),
                "JSON differs",
            )

            top_level_cases = (
                ("top-missing", lambda v: v.pop("rollback")),
                ("top-extra", lambda v: v.__setitem__("unexpected", 0)),
                ("schema", lambda v: v.__setitem__("schema", "wrong")),
                ("status", lambda v: v.__setitem__("status", "wrong")),
                ("owner", lambda v: v.__setitem__("owner", "wrong")),
                ("scope", lambda v: v.__setitem__("scope", "broader")),
                ("eligibility-owner", lambda v: v.__setitem__("eligibility_owner", "other")),
                ("commit", lambda v: v.__setitem__("commit", "0" * 40)),
                ("parent", lambda v: v.__setitem__("parent_commit", "0" * 40)),
                ("selected-count-field", lambda v: v.__setitem__("selected_path_count", 3)),
                ("combined-diff", lambda v: v.__setitem__("selected_binary_diff_sha256", "0" * 64)),
                ("rollback", lambda v: v.__setitem__("rollback", "broader")),
                ("top-extra-paths", lambda v: v.__setitem__("extra_paths", ["OTHER"])),
            )
            ledger_cases = (
                ("ledger-missing", lambda v: v["changed_path_ledger"].pop("argv")),
                ("ledger-extra", lambda v: v["changed_path_ledger"].__setitem__("extra", 0)),
                ("ledger-argv", lambda v: v["changed_path_ledger"]["argv"].append("OTHER")),
                ("ledger-count", lambda v: v["changed_path_ledger"].__setitem__("count", 180)),
                ("ledger-count-bool", lambda v: v["changed_path_ledger"].__setitem__("count", True)),
                ("ledger-hash", lambda v: v["changed_path_ledger"].__setitem__("lf_sha256", "0" * 64)),
            )
            for label, mutate in (*top_level_cases, *ledger_cases):
                with self.subTest(case=label):
                    reject_mutation(label, mutate)

            selected_cases = (
                ("selected-missing", lambda v: v["selected_paths"].pop()),
                ("selected-extra", lambda v: v["selected_paths"].append(dict(v["selected_paths"][0]))),
                ("selected-order", lambda v: v["selected_paths"].reverse()),
                ("selected-duplicate", lambda v: v["selected_paths"][1].__setitem__("path", v["selected_paths"][0]["path"])),
                ("selected-third-path", lambda v: v["selected_paths"][1].__setitem__("path", "OTHER")),
                ("entry-missing-key", lambda v: v["selected_paths"][0].pop("scope")),
                ("entry-extra-key", lambda v: v["selected_paths"][0].__setitem__("unexpected", 0)),
                ("entry-classification", lambda v: v["selected_paths"][0].__setitem__("classification", "broader")),
                ("entry-scope", lambda v: v["selected_paths"][0].__setitem__("scope", "broader")),
                ("before-blob", lambda v: v["selected_paths"][0].__setitem__("before_blob_oid", "0" * 40)),
                ("after-blob", lambda v: v["selected_paths"][0].__setitem__("after_blob_oid", "0" * 40)),
                ("before-sha", lambda v: v["selected_paths"][0].__setitem__("before_sha256", "0" * 64)),
                ("after-sha", lambda v: v["selected_paths"][0].__setitem__("after_sha256", "0" * 64)),
                ("single-diff", lambda v: v["selected_paths"][0].__setitem__("binary_diff_sha256", "0" * 64)),
                ("entry-rollback", lambda v: v["selected_paths"][0].__setitem__("rollback", "broader")),
                ("entry-extra-paths", lambda v: v["selected_paths"][0].__setitem__("extra_paths", ["OTHER"])),
            )
            counter_cases = (
                ("counter-missing", lambda v: v["operation_counters"].pop("camera_calls")),
                ("counter-extra", lambda v: v["operation_counters"].__setitem__("other", 0)),
                ("counter-nonzero", lambda v: v["operation_counters"].__setitem__("camera_calls", 1)),
                ("counter-bool", lambda v: v["operation_counters"].__setitem__("camera_calls", False)),
                ("counter-type", lambda v: v["operation_counters"].__setitem__("camera_calls", "0")),
            )
            for label, mutate in (*selected_cases, *counter_cases):
                with self.subTest(case=label):
                    reject_mutation(label, mutate)

            for label, value in (
                ("invalid-checkpoint", "not-a-checkpoint"),
                ("abbreviated-checkpoint", checkpoint[:12]),
                ("non-descendant", subject.TD_B_GOVERNANCE_LINEAGE_SUCCESSOR_PARENT),
            ):
                with self.subTest(case=label), self.assertRaises(ValueError):
                    subject._validate_td_b_governance_lineage_successor(
                        new_checkpoint=value,
                    )
            with mock.patch.object(
                subject.subprocess, "run",
                side_effect=subprocess.CalledProcessError(1, ["git"]),
            ):
                with self.assertRaisesRegex(ValueError, "Git owner differs"):
                    subject._validate_td_b_governance_lineage_successor(
                        new_checkpoint=checkpoint,
                    )

            original_run = subprocess.run

            def reject_git_drift(label, matches, output, message):
                def drift(command, *args, **kwargs):
                    if matches(command):
                        emitted = (
                            output.decode("utf-8")
                            if kwargs.get("text") and isinstance(output, bytes)
                            else output
                        )
                        return subprocess.CompletedProcess(command, 0, stdout=emitted)
                    return original_run(command, *args, **kwargs)

                with self.subTest(case=label), mock.patch.object(
                    subject.subprocess, "run", side_effect=drift,
                ):
                    with self.assertRaisesRegex(ValueError, message):
                        subject._validate_td_b_governance_lineage_successor(
                            new_checkpoint=checkpoint,
                        )

            selected_path = ".agents/skills/camera-based-rgbww-optimizer/SKILL.md"
            reject_git_drift(
                "historical-parent",
                lambda c: c == ["git", "rev-parse", f"{subject.TD_B_GOVERNANCE_LINEAGE_SUCCESSOR_COMMIT}^"],
                ("0" * 40 + "\n").encode(), "historical owner differs",
            )
            reject_git_drift(
                "ledger-bytes",
                lambda c: c[:3] == ["git", "diff", "--name-only"],
                b"drift\n", "historical owner differs",
            )
            reject_git_drift(
                "before-blob-recompute",
                lambda c: c == ["git", "rev-parse", f"{subject.TD_B_GOVERNANCE_LINEAGE_SUCCESSOR_PARENT}:{selected_path}"],
                ("0" * 40 + "\n").encode(), "path identity differs",
            )
            reject_git_drift(
                "after-blob-recompute",
                lambda c: c == ["git", "rev-parse", f"{subject.TD_B_GOVERNANCE_LINEAGE_SUCCESSOR_COMMIT}:{selected_path}"],
                ("0" * 40 + "\n").encode(), "path identity differs",
            )
            reject_git_drift(
                "before-bytes-recompute",
                lambda c: c == ["git", "show", f"{subject.TD_B_GOVERNANCE_LINEAGE_SUCCESSOR_PARENT}:{selected_path}"],
                b"drift", "path identity differs",
            )
            reject_git_drift(
                "after-bytes-recompute",
                lambda c: c == ["git", "show", f"{subject.TD_B_GOVERNANCE_LINEAGE_SUCCESSOR_COMMIT}:{selected_path}"],
                b"drift", "path identity differs",
            )
            reject_git_drift(
                "checkpoint-bytes",
                lambda c: c == ["git", "show", f"{checkpoint}:{selected_path}"],
                b"drift", "path identity differs",
            )
            reject_git_drift(
                "single-binary-diff",
                lambda c: c[-1:] == [selected_path] and c[:3] == ["git", "diff", "--binary"],
                b"drift", "path identity differs",
            )
            reject_git_drift(
                "combined-binary-diff",
                lambda c: c[:3] == ["git", "diff", "--binary"] and len(c) == 8,
                b"drift", "combined diff differs",
            )

            working_path = root / ".agents/skills/camera-based-rgbww-optimizer/SKILL.md"
            original_read_bytes = Path.read_bytes

            def drift_working(path):
                if path.resolve() == working_path.resolve():
                    return b"drift"
                return original_read_bytes(path)

            with mock.patch.object(Path, "read_bytes", drift_working):
                with self.assertRaisesRegex(ValueError, "path identity differs"):
                    subject._validate_td_b_governance_lineage_successor(
                        new_checkpoint=checkpoint,
                    )

            # Both old immutable payloads must reject before the subordinate
            # validator runs; no new hash can serve as a fallback.
            with mock.patch.object(
                subject, "TD_B_PUBLIC_DEFAULT_SUCCESSOR_MANIFEST_SHA256", "0" * 64,
            ), mock.patch.object(
                subject, "_validate_td_b_governance_lineage_successor",
            ) as subordinate:
                with self.assertRaisesRegex(ValueError, "manifest hash differs"):
                    subject._validate_td_b_public_default_successor_lineage(
                        new_checkpoint=checkpoint,
                    )
                subordinate.assert_not_called()
            with mock.patch.object(
                subject, "TD_B_AGENTS_POLICY_FREEZE_SHA256", "0" * 64,
            ), mock.patch.object(
                subject, "_validate_td_b_governance_lineage_successor",
            ) as subordinate:
                with self.assertRaisesRegex(ValueError, "freeze hash differs"):
                    subject._validate_td_b_agents_policy_lineage(
                        old_checkpoint=subject.TD_B_SETUP_CHECKPOINT,
                        new_checkpoint=checkpoint,
                    )
                subordinate.assert_not_called()

    def test_public_default_successor_manifest_fails_closed_on_exact_drift(self):
        checkpoint = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=Path(__file__).parents[1],
            check=True, capture_output=True, text=True,
        ).stdout.strip()
        canonical = subject.TD_B_PUBLIC_DEFAULT_SUCCESSOR_MANIFEST_PATH.read_bytes()

        with _w0_temporary_directory() as tempdir:
            root = Path(tempdir)
            copied = root / "successor-workflow-manifest.json"
            copied.write_bytes(canonical)
            with self.assertRaisesRegex(ValueError, "owner differs"):
                subject._validate_td_b_public_default_successor_lineage(
                    new_checkpoint=checkpoint,
                    manifest_path=copied,
                )
            subject._validate_td_b_public_default_successor_lineage(
                new_checkpoint=checkpoint,
                manifest_path=copied,
                require_canonical_manifest_owner=False,
            )

            def assert_semantic_rejection(label, mutate, message):
                value = json.loads(canonical)
                mutate(value)
                changed = root / f"{label}.json"
                changed.write_text(json.dumps(value, sort_keys=True), encoding="utf-8")
                changed_sha = hashlib.sha256(changed.read_bytes()).hexdigest()
                with mock.patch.object(
                    subject,
                    "TD_B_PUBLIC_DEFAULT_SUCCESSOR_MANIFEST_SHA256",
                    changed_sha,
                ):
                    with self.assertRaisesRegex(ValueError, message):
                        subject._validate_td_b_public_default_successor_lineage(
                            new_checkpoint=checkpoint,
                            manifest_path=changed,
                            require_canonical_manifest_owner=False,
                        )

            contract_cases = (
                ("schema", lambda value: value.__setitem__("schema", "wrong")),
                ("parent", lambda value: value.__setitem__("parent_commit", "0" * 40)),
                ("commit", lambda value: value.__setitem__("commit", "0" * 40)),
                ("provenance", lambda value: value.__setitem__("human_provenance", "missing")),
                ("extra", lambda value: value.__setitem__("extra_paths", ["OTHER"])),
            )
            for label, mutate in contract_cases:
                with self.subTest(label=label):
                    assert_semantic_rejection(label, mutate, "contract differs")

            entry_cases = (
                ("missing-path", lambda value: value["entries"].pop(), "entry count"),
                ("extra-path", lambda value: value["entries"].append(
                    dict(value["entries"][0], path="OTHER"),
                ), "entry count"),
                ("duplicate-path", lambda value: value["entries"][1].__setitem__(
                    "path", value["entries"][0]["path"],
                ), "duplicate paths"),
                ("wrong-path", lambda value: value["entries"][0].__setitem__(
                    "path", "OTHER",
                ), "exact path set"),
                ("old-hash", lambda value: value["entries"][0].__setitem__(
                    "old_blob_sha256", "0" * 64,
                ), "hash or diff differs"),
                ("current-hash", lambda value: value["entries"][0].__setitem__(
                    "current_blob_sha256", "0" * 64,
                ), "hash or diff differs"),
                ("diff-hash", lambda value: value["entries"][0].__setitem__(
                    "diff_sha256", "0" * 64,
                ), "hash or diff differs"),
                ("classification", lambda value: value["entries"][0].__setitem__(
                    "classification", "broader",
                ), "contract differs"),
                ("scope", lambda value: value["entries"][0].__setitem__(
                    "scope", "broader",
                ), "contract differs"),
                ("human-decision", lambda value: value["entries"][0].__setitem__(
                    "human_decision", "missing",
                ), "contract differs"),
                ("entry-provenance", lambda value: value["entries"][0].__setitem__(
                    "provenance", "missing",
                ), "contract differs"),
                ("rollback", lambda value: value["entries"][0].__setitem__(
                    "rollback", "broader",
                ), "contract differs"),
            )
            for label, mutate, message in entry_cases:
                with self.subTest(label=label):
                    assert_semantic_rejection(label, mutate, message)

            missing = root / "missing.json"
            with self.assertRaisesRegex(ValueError, "missing"):
                subject._validate_td_b_public_default_successor_lineage(
                    new_checkpoint=checkpoint,
                    manifest_path=missing,
                    require_canonical_manifest_owner=False,
                )
            non_regular = root / "manifest-directory"
            non_regular.mkdir()
            with self.assertRaisesRegex(ValueError, "missing"):
                subject._validate_td_b_public_default_successor_lineage(
                    new_checkpoint=checkpoint,
                    manifest_path=non_regular,
                    require_canonical_manifest_owner=False,
                )
            symlink = root / "manifest-link.json"
            symlink.symlink_to(copied)
            with self.assertRaisesRegex(ValueError, "symlink"):
                subject._validate_td_b_public_default_successor_lineage(
                    new_checkpoint=checkpoint,
                    manifest_path=symlink,
                    require_canonical_manifest_owner=False,
                )
            with self.assertRaisesRegex(ValueError, "ancestry differs"):
                subject._validate_td_b_public_default_successor_lineage(
                    new_checkpoint=subject.TD_B_PUBLIC_DEFAULT_SUCCESSOR_PARENT,
                )

            target = (
                Path(__file__).parents[1]
                / "src/camera_based_rgbww_optimizer/control/ray120c.py"
            ).resolve()
            original_read_bytes = Path.read_bytes

            def tampered_read_bytes(path):
                if path.resolve() == target:
                    return b"tampered working tree"
                return original_read_bytes(path)

            with mock.patch.object(Path, "read_bytes", tampered_read_bytes):
                with self.assertRaisesRegex(ValueError, "hash or diff differs"):
                    subject._validate_td_b_public_default_successor_lineage(
                        new_checkpoint=checkpoint,
                    )

            predecessor = json.loads(subject.TD_B_WORKFLOW_PATH_MANIFEST_PATH.read_bytes())
            predecessor["entries"][0]["current_blob_sha256"] = "0" * 64
            predecessor_path = root / "predecessor-drift.json"
            predecessor_path.write_text(
                json.dumps(predecessor, sort_keys=True), encoding="utf-8",
            )
            predecessor_sha = hashlib.sha256(predecessor_path.read_bytes()).hexdigest()
            with mock.patch.object(
                subject, "TD_B_WORKFLOW_PATH_MANIFEST_SHA256", predecessor_sha,
            ):
                with self.assertRaisesRegex(ValueError, "hash or diff differs"):
                    subject._validate_td_b_workflow_path_lineage(
                        new_checkpoint=checkpoint,
                        manifest_path=predecessor_path,
                        require_canonical_manifest_owner=False,
                    )

            missing_overlap = json.loads(canonical)
            missing_overlap["entries"] = [
                entry for entry in missing_overlap["entries"]
                if entry["path"] != "tests/test_ray120c.py"
            ]
            overlap_path = root / "missing-overlap.json"
            overlap_path.write_text(
                json.dumps(missing_overlap, sort_keys=True), encoding="utf-8",
            )
            overlap_sha = hashlib.sha256(overlap_path.read_bytes()).hexdigest()
            with mock.patch.object(
                subject, "TD_B_PUBLIC_DEFAULT_SUCCESSOR_MANIFEST_SHA256", overlap_sha,
            ):
                with self.assertRaisesRegex(ValueError, "entry count differs"):
                    subject._validate_td_b_workflow_path_lineage(
                        new_checkpoint=checkpoint,
                        successor_manifest_path=overlap_path,
                        require_canonical_successor_owner=False,
                    )

    def test_cleanup_test_provenance_manifest_rejects_exact_drift(self):
        checkpoint = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=Path(__file__).parents[1],
            check=True, capture_output=True, text=True,
        ).stdout.strip()
        canonical = subject.TD_B_CLEANUP_TEST_PROVENANCE_MANIFEST_PATH.read_bytes()
        with _w0_temporary_directory() as tempdir:
            root = Path(tempdir)
            copied = root / "cleanup-test-provenance-manifest.json"
            copied.write_bytes(canonical)
            with self.assertRaisesRegex(ValueError, "owner differs"):
                subject._validate_td_b_cleanup_test_provenance(
                    new_checkpoint=checkpoint,
                    manifest_path=copied,
                )
            subject._validate_td_b_cleanup_test_provenance(
                new_checkpoint=checkpoint,
                manifest_path=copied,
                require_canonical_manifest_owner=False,
            )
            for label, mutate in (
                ("bytes", lambda value: value["entries"][0].__setitem__(
                    "current_blob_sha256", "0" * 64,
                )),
                ("scope", lambda value: value["entries"][0].__setitem__(
                    "scope", "broader",
                )),
                ("path", lambda value: value["entries"][0].__setitem__(
                    "path", "tests/OTHER.py",
                )),
                ("extra", lambda value: value.__setitem__(
                    "extra_paths", ["tests/OTHER.py"],
                )),
            ):
                with self.subTest(label=label):
                    value = json.loads(canonical)
                    mutate(value)
                    changed = root / f"{label}.json"
                    changed.write_text(json.dumps(value), encoding="utf-8")
                    with self.assertRaisesRegex(ValueError, "hash differs"):
                        subject._validate_td_b_cleanup_test_provenance(
                            new_checkpoint=checkpoint,
                            manifest_path=changed,
                            require_canonical_manifest_owner=False,
                        )
            symlink = root / "manifest-link.json"
            symlink.symlink_to(copied)
            with self.assertRaisesRegex(ValueError, "symlink"):
                subject._validate_td_b_cleanup_test_provenance(
                    new_checkpoint=checkpoint,
                    manifest_path=symlink,
                    require_canonical_manifest_owner=False,
                )

    def test_workflow_path_manifest_rejects_owner_hash_and_provenance_drift(self):
        checkpoint = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=Path(__file__).parents[1],
            check=True, capture_output=True, text=True,
        ).stdout.strip()
        canonical = subject.TD_B_WORKFLOW_PATH_MANIFEST_PATH.read_bytes()
        with _w0_temporary_directory() as tempdir:
            root = Path(tempdir)
            copied = root / "workflow-path-manifest.json"
            copied.write_bytes(canonical)
            with self.assertRaisesRegex(ValueError, "owner differs"):
                subject._validate_td_b_workflow_path_lineage(
                    new_checkpoint=checkpoint,
                    manifest_path=copied,
                )
            subject._validate_td_b_workflow_path_lineage(
                new_checkpoint=checkpoint,
                manifest_path=copied,
                require_canonical_manifest_owner=False,
            )
            for label, mutate in (
                ("wrong-current", lambda value: value["entries"][0].__setitem__(
                    "current_blob_sha256", "0" * 64,
                )),
                ("wrong-diff", lambda value: value["entries"][0].__setitem__(
                    "diff_sha256", "0" * 64,
                )),
                ("extra-path", lambda value: value.__setitem__("extra_paths", ["OTHER.md"])),
                ("missing-provenance", lambda value: value.pop("human_provenance")),
                ("wrong-path", lambda value: value["entries"][0].__setitem__(
                    "path", "docs/engineering/OTHER.md",
                )),
            ):
                with self.subTest(label=label):
                    value = json.loads(canonical)
                    mutate(value)
                    changed = root / f"{label}.json"
                    changed.write_text(json.dumps(value), encoding="utf-8")
                    with self.assertRaisesRegex(ValueError, "hash differs"):
                        subject._validate_td_b_workflow_path_lineage(
                            new_checkpoint=checkpoint,
                            manifest_path=changed,
                            require_canonical_manifest_owner=False,
                        )
            missing = root / "missing.json"
            with self.assertRaisesRegex(ValueError, "missing"):
                subject._validate_td_b_workflow_path_lineage(
                    new_checkpoint=checkpoint,
                    manifest_path=missing,
                    require_canonical_manifest_owner=False,
                )
            symlink = root / "manifest-link.json"
            symlink.symlink_to(copied)
            with self.assertRaisesRegex(ValueError, "symlink"):
                subject._validate_td_b_workflow_path_lineage(
                    new_checkpoint=checkpoint,
                    manifest_path=symlink,
                    require_canonical_manifest_owner=False,
                )

    def test_agents_policy_lineage_rejects_wrong_bytes_owner_and_provenance(self):
        checkpoint = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=Path(__file__).parents[1],
            check=True, capture_output=True, text=True,
        ).stdout.strip()
        canonical = subject.TD_B_AGENTS_POLICY_FREEZE_PATH.read_bytes()
        with _w0_temporary_directory() as tempdir:
            root = Path(tempdir)
            copied = root / "policy-freeze.json"
            copied.write_bytes(canonical)
            with self.assertRaisesRegex(ValueError, "owner differs"):
                subject._validate_td_b_agents_policy_lineage(
                    old_checkpoint=subject.TD_B_SETUP_CHECKPOINT,
                    new_checkpoint=checkpoint,
                    policy_freeze_path=copied,
                )

            subject._validate_td_b_agents_policy_lineage(
                old_checkpoint=subject.TD_B_SETUP_CHECKPOINT,
                new_checkpoint=checkpoint,
                policy_freeze_path=copied,
                require_canonical_policy_owner=False,
            )
            for label, mutate in (
                ("wrong-hash", lambda value: value.__setitem__("current_blob_sha256", "0" * 64)),
                ("extra-path", lambda value: value.__setitem__("extra_paths", ["OTHER.md"])),
                ("missing-provenance", lambda value: value.pop("provenance")),
                ("wrong-scope", lambda value: value.__setitem__("scope", "broader")),
            ):
                with self.subTest(label=label):
                    value = json.loads(canonical)
                    mutate(value)
                    changed = root / f"{label}.json"
                    changed.write_text(json.dumps(value), encoding="utf-8")
                    with self.assertRaisesRegex(ValueError, "hash differs"):
                        subject._validate_td_b_agents_policy_lineage(
                            old_checkpoint=subject.TD_B_SETUP_CHECKPOINT,
                            new_checkpoint=checkpoint,
                            policy_freeze_path=changed,
                            require_canonical_policy_owner=False,
                        )
            missing = root / "missing.json"
            with self.assertRaisesRegex(ValueError, "missing"):
                subject._validate_td_b_agents_policy_lineage(
                    old_checkpoint=subject.TD_B_SETUP_CHECKPOINT,
                    new_checkpoint=checkpoint,
                    policy_freeze_path=missing,
                    require_canonical_policy_owner=False,
                )
            symlink = root / "policy-link.json"
            symlink.symlink_to(copied)
            with self.assertRaisesRegex(ValueError, "symlink"):
                subject._validate_td_b_agents_policy_lineage(
                    old_checkpoint=subject.TD_B_SETUP_CHECKPOINT,
                    new_checkpoint=checkpoint,
                    policy_freeze_path=symlink,
                    require_canonical_policy_owner=False,
                )

        candidate = subject.build_td_b_setup_release_lineage_candidate(
            subject.TD_B_SETUP_RELEASE_PATH,
            old_checkpoint=subject.TD_B_SETUP_CHECKPOINT,
            new_checkpoint=checkpoint,
            changed_paths=["ANOTHER_POLICY.md"],
        )
        self.assertEqual(candidate["prohibited_paths"], ["ANOTHER_POLICY.md"])

    def test_qualification_evidence_adapter_is_release_isolated(self):
        with _w0_temporary_directory() as tempdir:
            output = measure.write_td_b_lineage_qualification_evidence(
                preparation_path=subject.TD_B_QUALIFICATION_PREPARATION_R1_PATH,
                output_dir=Path(tempdir) / "direct",
                run_name="evidence",
                code_checkpoint=subject.TD_B_QUALIFICATION_AUDIT_CHECKPOINT,
            )
            evidence = _read_json(output)
            self.assertEqual(set(evidence), {
                "schema", "status", "preparation_reference",
                "audit_current_head", "audit_current_parent", "artifact_owner",
                "input_references", "validation_counts", "failure_oracle",
                "side_effect_budgets",
            })
            self.assertEqual(
                evidence["schema"], subject.TD_B_QUALIFICATION_EVIDENCE_SCHEMA,
            )
            self.assertEqual(
                evidence["status"], subject.TD_B_QUALIFICATION_EVIDENCE_STATUS,
            )
            self.assertEqual(len(evidence["input_references"]), 17)
            self.assertTrue(all(
                set(reference) == {"input_index", "sha256", "bytes", "owner"}
                for reference in evidence["input_references"]
            ))
            self.assertTrue(all(
                value == 0 for value in evidence["side_effect_budgets"].values()
            ))
            serialized = json.dumps(evidence, sort_keys=True)
            for forbidden in (
                "production_release_usable", "setup-lineage-release.json",
                "resolved_formal_plan", "device_authorization", "consumer_claim",
                '"readiness"',
            ):
                self.assertNotIn(forbidden, serialized)

        with _w0_temporary_directory() as tempdir:
            backend_factory = mock.Mock()
            run_fn = mock.Mock()
            setup_fn = mock.Mock()
            resolved_run_fn = mock.Mock()
            with mock.patch.object(
                measure, "write_td_b_setup_lineage_release",
            ) as release_writer, mock.patch.object(
                measure.thermal, "build_diagnostic_plan",
            ) as formal_plan_owner:
                result = measure.main(
                    [
                        "--experiment-id", subject.TD_B,
                        "--source", "ray",
                        "--phase", "formal",
                        "--output-dir", str(Path(tempdir) / "cli"),
                        "--run-name", "evidence",
                        "--qualification-preparation",
                        str(subject.TD_B_QUALIFICATION_PREPARATION_R1_PATH),
                        "--code-checkpoint",
                        subject.TD_B_QUALIFICATION_AUDIT_CHECKPOINT,
                        "--prepare-lineage-qualification-evidence",
                    ],
                    backend_factory=backend_factory,
                    run_fn=run_fn,
                    setup_fn=setup_fn,
                    resolved_run_fn=resolved_run_fn,
                )
            self.assertEqual(result, 0)
            release_writer.assert_not_called()
            formal_plan_owner.assert_not_called()
            backend_factory.assert_not_called()
            run_fn.assert_not_called()
            setup_fn.assert_not_called()
            resolved_run_fn.assert_not_called()

    def test_qualification_evidence_adapter_rejects_preparation_drift(self):
        canonical_path = subject.TD_B_QUALIFICATION_PREPARATION_R1_PATH
        canonical_bytes = canonical_path.read_bytes()
        canonical = json.loads(canonical_bytes)

        with _w0_temporary_directory() as tempdir:
            root = Path(tempdir)
            copied = root / "copied-r1.json"
            copied.write_bytes(canonical_bytes)
            copied.chmod(0o600)
            with self.assertRaisesRegex(ValueError, "owner differs"):
                subject._validate_td_b_qualification_preparation_r1(
                    preparation_path=copied,
                    code_checkpoint=subject.TD_B_QUALIFICATION_AUDIT_CHECKPOINT,
                )
            subject._validate_td_b_qualification_preparation_r1(
                preparation_path=copied,
                code_checkpoint=subject.TD_B_QUALIFICATION_AUDIT_CHECKPOINT,
                require_canonical_owner=False,
                expected_payload_sha256=hashlib.sha256(canonical_bytes).hexdigest(),
                expected_payload_bytes=len(canonical_bytes),
            )

            cases = (
                ("schema", lambda value: value.__setitem__("schema", "p7_c3_v1")),
                ("status", lambda value: value.__setitem__("status", "release_usable")),
                ("head", lambda value: value.__setitem__("audit_current_head", "0" * 40)),
                ("parent", lambda value: value.__setitem__("audit_current_parent", "0" * 40)),
                ("owner-commit", lambda value: value["successor_entry"].__setitem__(
                    "artifact_owner_commit", "0" * 40,
                )),
                ("owner-parent", lambda value: value["successor_entry"].__setitem__(
                    "artifact_owner_parent", "0" * 40,
                )),
                ("ambiguous", lambda value: value["successor_entry"].__setitem__(
                    "commit", subject.TD_B_QUALIFICATION_AUDIT_CHECKPOINT,
                )),
                ("missing", lambda value: value["inputs"].pop()),
                ("extra", lambda value: value["inputs"].append(
                    dict(value["inputs"][0], path="/other"),
                )),
                ("duplicate", lambda value: value["inputs"].append(
                    dict(value["inputs"][0]),
                )),
                ("provenance", lambda value: value["successor_entry"].__setitem__(
                    "provenance", "wrong",
                )),
                ("rollback", lambda value: value["successor_entry"].__setitem__(
                    "rollback_entries", 6,
                )),
                ("mismatch", lambda value: value["input_closure"].__setitem__(
                    "mismatches", ["drift"],
                )),
                ("prohibited", lambda value: value["input_closure"].__setitem__(
                    "prohibited_paths", ["OTHER"],
                )),
                ("qualification-budget", lambda value: value["budgets"].__setitem__(
                    "qualification", 1,
                )),
                ("release-budget", lambda value: value["budgets"].__setitem__(
                    "release_generation", 1,
                )),
                ("live-budget", lambda value: value["budgets"].__setitem__(
                    "live", 1,
                )),
                ("usable", lambda value: value.__setitem__(
                    "production_release_usable", True,
                )),
                ("readiness", lambda value: value.__setitem__("readiness", True)),
            )
            for label, mutate in cases:
                with self.subTest(label=label):
                    value = json.loads(canonical_bytes)
                    mutate(value)
                    changed = root / f"{label}.json"
                    changed.write_text(
                        json.dumps(value, indent=2, sort_keys=True) + "\n",
                        encoding="utf-8",
                    )
                    changed.chmod(0o600)
                    payload = changed.read_bytes()
                    with self.assertRaises(ValueError):
                        subject._validate_td_b_qualification_preparation_r1(
                            preparation_path=changed,
                            code_checkpoint=subject.TD_B_QUALIFICATION_AUDIT_CHECKPOINT,
                            require_canonical_owner=False,
                            expected_payload_sha256=hashlib.sha256(payload).hexdigest(),
                            expected_payload_bytes=len(payload),
                        )

            old_c3 = root / "old-c3.json"
            old_c3.write_bytes(Path(
                "/Volumes/4T/temp/rgbww-optimizer/"
                "p7-td-b-ray-public-default-lineage-c3-offline-preparation/"
                "20260726T092247Z/qualification-preparation.json"
            ).read_bytes())
            old_c3.chmod(0o600)
            old_payload = old_c3.read_bytes()
            with self.assertRaisesRegex(ValueError, "schema/status"):
                subject._validate_td_b_qualification_preparation_r1(
                    preparation_path=old_c3,
                    code_checkpoint=subject.TD_B_QUALIFICATION_AUDIT_CHECKPOINT,
                    require_canonical_owner=False,
                    expected_payload_sha256=hashlib.sha256(old_payload).hexdigest(),
                    expected_payload_bytes=len(old_payload),
                )

            wrong_mode = root / "wrong-mode.json"
            wrong_mode.write_bytes(canonical_bytes)
            wrong_mode.chmod(0o644)
            with self.assertRaisesRegex(ValueError, "mode differs"):
                subject._validate_td_b_qualification_preparation_r1(
                    preparation_path=wrong_mode,
                    code_checkpoint=subject.TD_B_QUALIFICATION_AUDIT_CHECKPOINT,
                    require_canonical_owner=False,
                )
            symlink = root / "link.json"
            symlink.symlink_to(copied)
            with self.assertRaisesRegex(ValueError, "symlink"):
                subject._validate_td_b_qualification_preparation_r1(
                    preparation_path=symlink,
                    code_checkpoint=subject.TD_B_QUALIFICATION_AUDIT_CHECKPOINT,
                    require_canonical_owner=False,
                )
            directory = root / "directory"
            directory.mkdir()
            with self.assertRaisesRegex(ValueError, "non-regular"):
                subject._validate_td_b_qualification_preparation_r1(
                    preparation_path=directory,
                    code_checkpoint=subject.TD_B_QUALIFICATION_AUDIT_CHECKPOINT,
                    require_canonical_owner=False,
                )
            with self.assertRaisesRegex(PermissionError, "rejects release"):
                measure.write_td_b_lineage_qualification_evidence(
                    preparation_path=canonical_path,
                    output_dir=root,
                    run_name="release-request",
                    code_checkpoint=subject.TD_B_QUALIFICATION_AUDIT_CHECKPOINT,
                    release_requested=True,
                )
            with self.assertRaises(SystemExit):
                measure.parse_args([
                    "--experiment-id", subject.TD_B,
                    "--source", "ray",
                    "--run-name", "conflict",
                    "--prepare-lineage-qualification-evidence",
                    "--qualify-lineage-release",
                ])
            with self.assertRaisesRegex(PermissionError, "exact offline inputs"):
                measure.main([
                    "--experiment-id", subject.TD_B,
                    "--source", "ray",
                    "--phase", "formal",
                    "--output-dir", str(root),
                    "--run-name", "incomplete",
                    "--prepare-lineage-qualification-evidence",
                ])
            self.assertFalse((root / "incomplete").exists())
            existing = root / "existing"
            existing.mkdir()
            with self.assertRaisesRegex(FileExistsError, "must be fresh"):
                measure.write_td_b_lineage_qualification_evidence(
                    preparation_path=canonical_path,
                    output_dir=root,
                    run_name="existing",
                    code_checkpoint=subject.TD_B_QUALIFICATION_AUDIT_CHECKPOINT,
                )
            symlink_output = root / "symlink-output"
            symlink_output.symlink_to(root, target_is_directory=True)
            with self.assertRaisesRegex(FileExistsError, "symlink owner"):
                measure.write_td_b_lineage_qualification_evidence(
                    preparation_path=canonical_path,
                    output_dir=symlink_output,
                    run_name="evidence",
                    code_checkpoint=subject.TD_B_QUALIFICATION_AUDIT_CHECKPOINT,
                )

    def test_lineage_qualification_cli_never_constructs_backend(self):
        backend_factory = mock.Mock()
        release = Path("/offline/setup-lineage-release.json")
        with mock.patch.object(
            measure,
            "write_td_b_setup_lineage_release",
            return_value=release,
        ) as writer:
            result = measure.main(
                [
                    "--experiment-id", subject.TD_B,
                    "--source", "ray",
                    "--phase", "formal",
                    "--output-dir", "/offline",
                    "--run-name", "lineage",
                    "--setup-release", str(subject.TD_B_SETUP_RELEASE_PATH),
                    "--lineage-candidate", str(subject.TD_B_F0A_LINEAGE_CANDIDATE_PATH),
                    "--code-checkpoint", "a" * 40,
                    "--qualify-lineage-release",
                ],
                backend_factory=backend_factory,
            )
        self.assertEqual(result, 0)
        writer.assert_called_once()
        backend_factory.assert_not_called()

    def test_lineage_formal_cli_dispatches_before_unresolved_td_b_plan_gate(self):
        checkpoint = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=Path(__file__).parents[1],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        backend = mock.Mock()
        backend_factory = mock.Mock(return_value=backend)
        resolved_run = mock.Mock(return_value=Path("/offline/formal-run"))
        with mock.patch.object(
            measure.thermal,
            "build_diagnostic_plan",
            side_effect=AssertionError("formal lineage dispatch built an unresolved plan"),
        ):
            result = measure.main(
                [
                    "--experiment-id", subject.TD_B,
                    "--source", "ray",
                    "--phase", "formal",
                    "--output-dir", "/offline",
                    "--run-name", "ray",
                    "--setup-release", "/offline/setup-lineage-release.json",
                    "--code-checkpoint", checkpoint,
                    "--human-authorization", subject.TD_B,
                    "--camera-backend", "remote",
                    "--allow-device-control",
                    "--execute",
                ],
                backend_factory=backend_factory,
                resolved_run_fn=resolved_run,
            )
        self.assertEqual(result, 0)
        backend_factory.assert_called_once()
        resolved_run.assert_called_once()


def _w0_temporary_directory():
    W0_TEMP_ROOT.mkdir(parents=True, exist_ok=True)
    return tempfile.TemporaryDirectory(dir=W0_TEMP_ROOT)


def _read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def _make_fake_thermal_wrapper_project(tempdir: Path):
    root = tempdir / "project"
    (root / "tmp").mkdir(parents=True)
    (root / ".venv/bin").mkdir(parents=True)
    source = Path(__file__).parents[1] / "tmp/run-p7-thermal-diagnostics.zsh"
    wrapper = root / "tmp/run-p7-thermal-diagnostics.zsh"
    source_bytes = source.read_bytes()
    shutil.copy2(source, wrapper)
    fake_python = root / ".venv/bin/python"
    fake_python.write_text("""#!/usr/bin/env python3
import json
import os
import signal
import sys
import time

with open(os.environ["FAKE_CALL_LOG"], "a", encoding="utf-8") as handle:
    handle.write(" ".join(sys.argv[1:]) + "\\n")
if len(sys.argv) > 1 and sys.argv[1] == "-c":
    os.execv(sys.executable, [sys.executable, *sys.argv[1:]])
if "camera_based_rgbww_optimizer.control.all_off" in sys.argv:
    print(json.dumps([
        {"name": "esphome", "ok": True, "detail": {}, "error": None},
        {"name": "ray120c", "ok": True, "detail": {}, "error": None},
    ]))
    if os.environ.get("FAKE_RUNNER_MODE") == "cleanup_failure":
        print("fake cleanup failed", file=sys.stderr)
        raise SystemExit(9)
    raise SystemExit(0)
mode = os.environ.get("FAKE_RUNNER_MODE", "success")
if mode in {"success", "cleanup_failure"}:
    raise SystemExit(0)
if mode == "child_failure":
    raise SystemExit(7)
for signum in (signal.SIGINT, signal.SIGTERM, signal.SIGHUP):
    signal.signal(signum, lambda received, _frame: sys.exit(128 + received))
with open(os.environ["FAKE_READY_FILE"], "w", encoding="utf-8") as handle:
    handle.write("ready\\n")
time.sleep(30)
""", encoding="utf-8")
    fake_python.chmod(0o755)
    return root, wrapper, tempdir / "calls.log", hashlib.sha256(source_bytes).hexdigest()


if __name__ == "__main__":
    unittest.main()
