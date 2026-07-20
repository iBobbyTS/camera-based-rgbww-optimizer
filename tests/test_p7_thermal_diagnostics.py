from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from camera_based_rgbww_optimizer.optimization import measure_p7_thermal_diagnostics as measure
from camera_based_rgbww_optimizer.optimization import p7_thermal_diagnostics as subject
from camera_based_rgbww_optimizer.control import camera_gphoto2, camera_remote_v2


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
        self.assertEqual(plan["timing_contract"]["name"], "best_effort_gphoto2_v1")
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

    def test_best_effort_timing_boundaries_are_exposed_without_actual_provenance(self):
        self.assertEqual(subject.TIMING_TOLERANCE_S[60], 2.0)
        self.assertEqual(subject.TIMING_TOLERANCE_S[120], 2.0)
        self.assertEqual(subject.TIMING_TOLERANCE_S[300], 5.0)
        self.assertEqual(subject.TIMING_TOLERANCE_S[600], 5.0)
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


if __name__ == "__main__":
    unittest.main()
