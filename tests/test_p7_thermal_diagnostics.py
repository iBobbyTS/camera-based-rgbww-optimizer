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
from camera_based_rgbww_optimizer.control import camera_gphoto2, camera_remote_v2


W0_TEMP_ROOT = Path("/Volumes/4T/temp/rgbww-optimizer/p7-td-a-w0-offline/test-runtime")


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


class P7ThermalDiagnosticsTests(unittest.TestCase):
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
            result = {
                "physical_capture_count": 1, "thermal_covariates": covariate,
            }
            requested = float(step["requested_elapsed_s"] or 1.0)
            result["timing_evidence"] = {
                "provenance": camera_remote_v2.TIMING_PROVENANCE,
                "timing_contract": camera_remote_v2.TIMING_CONTRACT,
                "tier": "tier_b", "status": "accepted_best_effort_anchor",
                "local_request_started_monotonic_s": 0.0,
                "local_response_received_monotonic_s": requested + 0.2,
                "local_round_trip_s": requested + 0.2,
                "local_readback_done_monotonic_s": 0.0,
                "bridge_relative_delay_s": requested,
                "best_effort_elapsed_s": requested,
                "network_assumption": "wired_lan_latency_negligible_developer_decision",
                "absolute_exposure_start": False,
            }
            if step["capture_role"] == "ambient":
                result["ambient_diagnostic"] = {"geometry_hash": "g", "black_levels": [512] * 4}
            return result

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
                "timing_evidence": {
                    "provenance": "best_effort_gphoto2_exposure_start_estimate",
                    "tier": "tier_c", "status": "timing_evidence_unavailable",
                    "best_effort_elapsed_s": None,
                },
            }
            if step["capture_role"] == "ambient":
                result["ambient_diagnostic"] = {"geometry_hash": "g", "black_levels": [512] * 4}
            return result
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
            raw = root / "rejected.CR3"
            raw.write_bytes(b"cr3")
            result = {"saved_file": str(raw), "physical_capture_count": 1,
                      "thermal_covariates": _minimal_covariate(step),
                      "timing_evidence": {
                          "provenance": subject.TIMING_CONTRACT_V2["provenance"],
                          "tier": "tier_b", "status": "accepted_best_effort_anchor",
                          "best_effort_elapsed_s": 64.4,
                      }}
            return result
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
