from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from camera_based_rgbww_optimizer.optimization import measure_p7_thermal_diagnostics as measure
from camera_based_rgbww_optimizer.optimization import p7_thermal_diagnostics as subject


class _Clock:
    def __init__(self):
        self.value = 0.0

    def monotonic(self):
        return self.value

    def sleep(self, seconds):
        self.value += seconds


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

    def test_scheduler_accepts_boundary_and_rejects_one_over(self):
        for requested, tolerance in subject.TIMING_TOLERANCE_S.items():
            for delta, valid in ((tolerance, True), (tolerance + 0.001, False)):
                with self.subTest(requested=requested, delta=delta):
                    clock = _Clock()
                    results = subject.run_timed_schedule(
                        [requested], command_apply_fn=lambda: None, readback_fn=lambda: None,
                        capture_fn=lambda _point, d=delta: {
                            "exposure_start_monotonic_s": clock.value + d,
                            "exposure_start_provenance": subject.ACTUAL_EXPOSURE_START_PROVENANCE,
                        },
                        monotonic_fn=clock.monotonic, sleep_fn=clock.sleep,
                    )
                    self.assertEqual(results[0].timing_valid, valid)

    def test_readback_completion_owns_elapsed_and_wall_clock_is_irrelevant(self):
        clock = _Clock()
        calls = []
        def readback():
            clock.value += 7
        result = subject.run_timed_schedule(
            [60, 120], command_apply_fn=lambda: calls.append("apply"), readback_fn=readback,
            capture_fn=lambda point: {
                "point": point, "exposure_start_monotonic_s": clock.value,
                "exposure_start_provenance": subject.ACTUAL_EXPOSURE_START_PROVENANCE,
            },
            monotonic_fn=clock.monotonic, sleep_fn=clock.sleep,
        )
        self.assertEqual([item.actual_elapsed_s for item in result], [60, 120])
        self.assertEqual(calls, ["apply"])

    def test_scheduler_rejects_request_start_or_missing_actual_exposure_provenance(self):
        for capture in (
            {"exposure_start_monotonic_s": 60},
            {"exposure_start_monotonic_s": 60, "exposure_start_provenance": "host_camera_request_start_monotonic"},
        ):
            with self.subTest(capture=capture), self.assertRaisesRegex(ValueError, "actual exposure-start"):
                clock = _Clock()
                subject.run_timed_schedule(
                    [60], command_apply_fn=lambda: None, readback_fn=lambda: None,
                    capture_fn=lambda _point, value=capture: value,
                    monotonic_fn=clock.monotonic, sleep_fn=clock.sleep,
                )

    def test_execute_plan_fails_before_calls_when_adapter_lacks_actual_exposure_start(self):
        calls = []
        with self.assertRaisesRegex(PermissionError, "exposure-start"):
            subject.build_diagnostic_plan(
                subject.TD_A, source="ray", for_execution=True,
                human_authorization=subject.TD_A, exposure_start_capability=False,
            )
        self.assertEqual(calls, [])

    def test_fake_td_a_execution_keeps_ambient_separate_and_counts_all_physical(self):
        plan = subject.build_diagnostic_plan(
            subject.TD_A, source="ray", for_execution=True,
            human_authorization=subject.TD_A, exposure_start_capability=True,
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
                "exposure_start_monotonic_s": clock.value,
                "exposure_start_provenance": subject.ACTUAL_EXPOSURE_START_PROVENANCE,
                "physical_capture_count": 1, "thermal_covariates": covariate,
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
            human_authorization=subject.TD_A, exposure_start_capability=True,
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

    def test_cleanup_exception_is_retained_and_marks_run_failed(self):
        plan = subject.build_diagnostic_plan(
            subject.TD_A, source="ray", for_execution=True,
            human_authorization=subject.TD_A, exposure_start_capability=True,
        )
        plan = {**plan, "captures": [], "budgets": {"formal_cap": 0, "ambient_cap": 0, "physical_cr3_cap": 0}}
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

    def test_deferred_td_b_plan_is_rejected_by_runner_before_calls(self):
        plan = subject.build_diagnostic_plan(subject.TD_B, source="strip")
        plan["status"] = "execute_authorized"
        plan["camera"]["adapter_capability_available"] = True
        calls = []
        with tempfile.TemporaryDirectory() as tempdir, self.assertRaisesRegex(PermissionError, "deferred"):
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
        with self.assertRaises(PermissionError):
            measure.main(["--experiment-id", subject.TD_A, "--source", "ray", "--run-name", "x", "--execute"])

    def test_exact_authorization_still_fails_before_backend_when_exposure_start_is_unavailable(self):
        from camera_based_rgbww_optimizer.control import camera_remote
        with mock.patch.object(camera_remote, "create_camera_backend") as backend, self.assertRaisesRegex(PermissionError, "exposure-start"):
            measure.main([
                "--experiment-id", subject.TD_A, "--source", "ray", "--run-name", "x", "--execute",
                "--allow-device-control", "--human-authorization", subject.TD_A,
            ])
        backend.assert_not_called()

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


if __name__ == "__main__":
    unittest.main()
