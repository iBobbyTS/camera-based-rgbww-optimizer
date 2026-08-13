import hashlib
import json
import tempfile
import unittest
from types import SimpleNamespace
from camera_based_rgbww_optimizer.measurement.recorded_exposure import parse_nominal_exposure
from pathlib import Path
from unittest.mock import patch

from camera_based_rgbww_optimizer.optimization import p7_thermal_diagnostics as thermal
from camera_based_rgbww_optimizer.optimization import measure_p7_thermal_diagnostics as measure
from camera_based_rgbww_optimizer.optimization import analyze_p7_thermal_diagnostics as analyze


class DirectR6Tests(unittest.TestCase):
    def _write_r6_vector_evidence(self, root):
        feature_ids = tuple(
            json.loads(thermal.POLICY_PATH.read_text())["feature_set"]["ids"]
        )
        captures = []
        covariates = []
        anchor_offset = {
            "initial_anchor": 0.0,
            "return_after_D": 0.01,
            "return_after_B": 0.02,
            "return_after_C": 0.03,
        }
        for index, step in enumerate(thermal.build_ray_r6_spec()["captures"]):
            values = {feature_id: 1.0 for feature_id in feature_ids}
            if step["role"] in anchor_offset:
                values[feature_ids[0]] += anchor_offset[step["role"]]
            covariate = {
                "sequence_index": index,
                "session_elapsed_s": float(600 + index * 600),
                "source_on_elapsed_s": float(600 + index * 599),
                "previous_state_dwell_s": None,
                "previous_state_id": {
                    "return_after_D": "D",
                    "return_after_B": "B",
                    "return_after_C": "C",
                }.get(step["role"]),
            }
            covariates.append(covariate)
            captures.append({
                "capture_id": step["capture_id"],
                "plan_step": step,
                "capture": {
                    "feature_values": values,
                    "thermal_covariates": covariate,
                },
            })
        (root / "captures.jsonl").write_text(
            "".join(json.dumps(row) + "\n" for row in captures)
        )
        (root / "thermal-covariates.jsonl").write_text(
            "".join(json.dumps(row) + "\n" for row in covariates)
        )
        (root / "quality.json").write_text(json.dumps({
            "status": "pass", "capture_count": 16,
        }))
        (root / analyze.POST_FIX_REVALIDATION_FILE).write_text(json.dumps({
            "status": "pass", "original_child_exit": 1,
            "original_failure_preserved": True,
        }))
        slope = {feature_id: 0.0 for feature_id in feature_ids}
        slope[feature_ids[0]] = 1.0
        (root / "analysis.json").write_text(json.dumps({
            "status": "history_dependent_at_operational_dwell_600",
            "formal_pass": False,
            "return_anchor_history": "fail",
            "operational_endpoint_600_valid": False,
            "chronology_by_state": {
                state: {"direction": {"slope_by_feature": slope}}
                for state in ("D", "B", "C")
            },
        }))
        return feature_ids

    def _execute_fake_protocol(
        self, plan, root, *, observed_elapsed_fn=None, feature_values_fn=None,
    ):
        feature_ids = tuple(json.loads(thermal.POLICY_PATH.read_text())["feature_set"]["ids"])
        curve = json.loads(thermal.CURVE_PATH.read_text())

        def capture(step):
            index = int(step["capture_id"].split("-", 1)[0])
            raw = root / f"{step['capture_id']}.cr3"
            raw.parent.mkdir(parents=True, exist_ok=True)
            raw.write_bytes(f"fake-{index}".encode())
            sidecar = raw.with_suffix(raw.suffix + ".metadata.json")
            sidecar.write_text("{}")
            observed_elapsed = (
                float(index + 1)
                if observed_elapsed_fn is None
                else float(observed_elapsed_fn(step, index))
            )
            timing = {
                "tier": "tier_b", "status": "accepted_best_effort_anchor",
                "provenance": thermal.TIMING_CONTRACT_V2["provenance"],
                "best_effort_elapsed_s": observed_elapsed,
            }
            command = step["command"] or {"strip": "off", "ray": "off"}
            covariates = thermal.build_covariate_record(
                source_id=step["source_id"], state_id=step["state_id"], command=command,
                sequence_index=index, capture_order=index,
                source_order=int(step.get("source_order", 1)),
                monotonic_timestamp_ns=index + 1,
                wall_clock_timestamp="2026-08-07T00:00:00+00:00",
                session_elapsed_s=float(index), source_on_elapsed_s=1.0,
                state_on_elapsed_s=1.0, off_duration_before_s=0.0,
                previous_state_id=None, previous_state_dwell_s=None,
                shutter_seconds=1 / 5000, raw_black_levels=(0, 0, 0, 0),
                raw_white_level=65535,
                load_history={60: 0.0, 300: 0.0, 900: 0.0},
                readback={"status": "pass"},
                curve=curve if step["source_id"] == "strip" else None,
            )
            output = {
                "capture_id": step["capture_id"], "saved_file": str(raw),
                "remote_metadata_path": str(sidecar), "physical_capture_count": 1,
                "timing_evidence": timing, "thermal_covariates": covariates,
                "recorded_exposure": {
                    "source": "Canon:ExposureTime", "status": "recorded",
                    "seconds": parse_nominal_exposure(
                        plan["frozen_shutters"].get(
                            thermal.shutter_cache_key_for_step(step), "1/5000"
                        )
                    ),
                },
            }
            if step["formal_measurement"]:
                output["feature_values"] = (
                    feature_values_fn(step)
                    if feature_values_fn is not None
                    else {feature_id: 1.0 for feature_id in feature_ids}
                )
                output["direct_quality"] = {
                    "status": "pass", "feature_count": len(feature_ids),
                }
            else:
                output["ambient_diagnostic"] = {
                    "geometry_hash": "fake", "black_levels": [0, 0, 0, 0],
                    "white_level": 65535, "black_level_tolerance_dn": 1,
                }
            if step["source_id"] == "ray":
                output["strip_zero_before_capture"] = {
                    "requested_payload": {
                        "red": 0, "green": 0, "blue": 0,
                        "warm_white": 0, "cold_white": 0,
                    },
                    "device_snapshot": {
                        "red": 0, "green": 0, "blue": 0,
                        "warm_white": 0, "cold_white": 0,
                    },
                }
            elif plan["execution_authorization"]["schema"] in {
                "direct_strip_history_session_v1",
                "direct_td_c_fast_endpoint_holdout_v1",
            }:
                output["ray_zero_before_capture"] = {
                    "response": {"data": {"intensity": 0}},
                }
            return output

        def fake_sidecar(payload, *, raw_path, raw_payload=None, run_root):
            sidecar = Path(str(payload["remote_metadata_path"]))
            return {
                "sidecar_path": str(sidecar.resolve()),
                "sidecar_byte_count": sidecar.stat().st_size,
                "sidecar_sha256": hashlib.sha256(sidecar.read_bytes()).hexdigest(),
                "sidecar_validation_status": "pass",
                "remote_capture_id": f"remote-{payload['capture_id']}",
                "remote_request_id": f"request-{payload['capture_id']}",
                "remote_metadata": {
                    "capture_id": f"remote-{payload['capture_id']}",
                    "request_id": f"request-{payload['capture_id']}",
                    "exposure_start_estimate": {
                        "method": "gphoto_event_minus_recorded_exposure",
                    },
                },
                "receipt": {"timing_evidence": payload["timing_evidence"]},
            }

        def gate(_gate_id):
            return {
                "status": "pass", "strip_verified_off": True,
                "ray_verified_off": True, "ray_off_command": {"status": "pass"},
            }

        def source_isolation(_gate_id):
            if plan["execution_authorization"]["schema"] == "direct_strip_history_session_v1":
                return {
                    "status": "pass", "source_verified_zero": True,
                    "source_verified": "ray", "strip_verified_off": False,
                    "ray_verified_off": True, "ray_off_command": {"status": "pass"},
                }
            return {
                "status": "pass", "strip_verified_off": True,
                "source_verified_zero": True, "ray_off_command": None,
            }

        direct_ray_continuous = plan["execution_authorization"]["schema"] in {
            "direct_ray_r6_authority_v1",
            "direct_ray_history_session_v1",
            "direct_strip_history_session_v1",
            "direct_ray_fast_long_bridge_session_v1",
        }

        with patch.object(measure, "_validate_returned_sidecar", side_effect=fake_sidecar):
            return measure.execute_plan(
                plan, run_dir=root,
                apply_command_fn=lambda step: {"status": "pass"},
                readback_fn=lambda step: {"status": "pass"},
                capture_fn=capture, both_off_gate_fn=gate,
                source_isolation_check_fn=(
                    source_isolation if direct_ray_continuous else None
                ),
                cleanup_fn=lambda: {"status": "pass", "steps": [{"ok": True}]},
                runtime_capture_settings_provenance=plan["camera"]["resolved_capture_settings"],
                runtime_git_provenance={"commit": "0" * 40, "dirty": False, "dirty_entries": []},
                post_capture_validator_fn=(
                    measure.validate_direct_ray_history_session_post_capture
                    if plan["execution_authorization"]["schema"]
                    == "direct_ray_history_session_v1"
                    else measure.validate_direct_strip_history_session_post_capture
                    if plan["execution_authorization"]["schema"]
                    == "direct_strip_history_session_v1"
                    else measure.validate_direct_ray_fast_long_bridge_session_post_capture
                    if plan["execution_authorization"]["schema"]
                    == "direct_ray_fast_long_bridge_session_v1"
                    else measure.validate_direct_protocol_post_capture
                ),
                sleep_fn=lambda _seconds: None,
            )

    def test_exact_sequence_and_contract(self):
        spec = thermal.build_ray_r6_spec()
        self.assertEqual(spec["capture_ids"], list(thermal.TD_B_R6_CAPTURE_IDS))
        self.assertEqual(len(spec["captures"]), 16)
        self.assertEqual({r["nominal_shutter"] for r in spec["captures"]}, {"1/5000", "1/6400", "1/8000", "1/2500"})
        self.assertTrue(all(r["exposure_mode"] == "fixed" and not r["weak_reacquire"] for r in spec["captures"]))
        groups = measure._ledger_groups(thermal.TD_B, spec["captures"])
        self.assertEqual([group[0]["state_id"] for group in groups], ["A", "D", "A", "B", "A", "C", "A"])

    def test_ray_history_spec_is_exact_balanced_and_device_locked(self):
        experiment = thermal.build_ray_history_experiment_spec()
        self.assertEqual(experiment["status"], "device_locked")
        self.assertEqual(experiment["formal_capture_count"], 21)
        self.assertEqual(experiment["orders"], [["D", "B", "C"], ["C", "D", "B"], ["B", "C", "D"]])
        self.assertEqual(sum(len(session["captures"]) for session in experiment["sessions"]), 21)
        for session_index, session in enumerate(experiment["sessions"], start=1):
            self.assertEqual(session["status"], "device_locked")
            self.assertEqual({step["requested_elapsed_s"] for step in session["captures"]}, {120})
            self.assertTrue(all(step["capture_id"].endswith("-t120") for step in session["captures"]))
            self.assertEqual(session["analysis_contract"]["operational_dwell_s"], 120)
            self.assertEqual(
                session["analysis_contract"]["session_cold_proxy_s"],
                thermal.RAY_HISTORY_SESSION_COLD_PROXY_S,
            )
            self.assertEqual(session["analysis_contract"]["session_cold_proxy_thermal_error"], "human_accepted")
            self.assertEqual(session["analysis_contract"]["thermal_error"], "human_accepted")
            self.assertFalse(session["analysis_contract"]["steady_claim"])
            self.assertIn("human_dwell_policy", session["inputs"])
            self.assertEqual([step["state_id"] for step in session["captures"]][::2], ["A", "A", "A", "A"])
            returns = [step for step in session["captures"] if step["role"] == "return_anchor"]
            self.assertEqual(
                [(step["sequence_position"], step["immediate_predecessor_state"]) for step in returns],
                list(enumerate(session["session_order"], start=1)),
            )
            authorized = thermal.build_ray_history_session_spec(
                session_index, device_control_enabled=True,
                session_start_condition=thermal.RAY_HISTORY_SESSION_START_CONDITION,
            )
            self.assertEqual(authorized["status"], "execute_authorized")
            self.assertTrue(authorized["execution_authorization"]["bounded_device_scope"])
            self.assertFalse(authorized["execution_authorization"]["human_authorization_required"])
        with self.assertRaisesRegex(ValueError, "600 s cold-proxy"):
            thermal.build_ray_history_session_spec(
                1,
                device_control_enabled=True,
                session_start_condition=(
                    "Ray and strip continuously off for at least 3600 s after prior high load; "
                    "both-source zero readback passes at run start"
                ),
            )

    def test_ray_history_cli_requires_bounded_scope_and_one_session(self):
        called = {}

        def runner(plan, **_kwargs):
            called["plan"] = plan
            return Path("/fake/session")

        base = [
            "--experiment-id", thermal.RAY_HISTORY_3X3_EXPERIMENT_ID,
            "--source", "ray", "--variant", "core", "--phase", "formal",
            "--run-name", "session-2", "--execute", "--allow-device-control",
            "--direct-ray-history-3x3", "--session-index", "2",
            "--session-start-condition", thermal.RAY_HISTORY_SESSION_START_CONDITION,
        ]
        with self.assertRaises(PermissionError):
            measure.main(base[:-2], run_fn=runner, backend_factory=lambda: object())
        self.assertEqual(
            measure.main(base, run_fn=runner, backend_factory=lambda: object()), 0,
        )
        self.assertEqual(called["plan"]["session_index"], 2)
        self.assertEqual(called["plan"]["session_order"], ["C", "D", "B"])

    def test_strip_history_cli_does_not_require_prior_analysis(self):
        called = {}

        def runner(plan, **_kwargs):
            called["plan"] = plan
            return Path("/fake/strip-session")

        base = [
            "--experiment-id", "p7_td_b_command_switch_history_v1",
            "--source", "strip", "--variant", "history", "--phase", "formal",
            "--run-name", "strip-session-1", "--execute", "--allow-device-control",
            "--direct-strip-history-3x3", "--session-index", "1",
            "--session-start-condition", thermal.RAY_HISTORY_SESSION_START_CONDITION,
        ]
        self.assertEqual(
            measure.main(base, run_fn=runner, backend_factory=lambda: object()), 0,
        )
        self.assertEqual(called["plan"]["session_index"], 1)
        self.assertEqual(called["plan"]["source"], "strip")

    def test_ray_fast_long_bridge_specs_keep_exact_pair_order_and_envelopes(self):
        expected = (
            ("C", "FAST", 600, 120),
            ("C", "LONG", 1800, 600),
            ("B", "LONG", 1800, 600),
            ("B", "FAST", 600, 120),
        )
        prerequisite = {
            "path": "/fake/analysis-v3.json",
            "sha256": "a" * 64,
            "kind": "ray-fast-long-bridge",
            "status": "pass",
        }
        with tempfile.TemporaryDirectory() as tmp:
            for mini_session_index, (state, protocol, reset_s, dwell_s) in enumerate(
                expected, start=1,
            ):
                condition = thermal.ray_fast_long_bridge_start_condition(
                    state=state, protocol=protocol, reset_s=reset_s,
                )
                plan = thermal.build_ray_fast_long_bridge_session_spec(
                    mini_session_index,
                    device_control_enabled=True,
                    session_start_condition=condition,
                    scientific_prerequisite=prerequisite,
                )
                self.assertEqual(
                    (plan["bridge_state"], plan["bridge_protocol"], plan["reset_s"]),
                    (state, protocol, reset_s),
                )
                self.assertEqual(
                    [step["state_id"] for step in plan["captures"]], ["A", state, "A"],
                )
                self.assertEqual(
                    {step["requested_elapsed_s"] for step in plan["captures"]}, {dwell_s},
                )
                self.assertEqual(plan["budgets"]["formal_cap"], 3)
                self.assertFalse(
                    plan["execution_authorization"]["human_authorization_required"],
                )
                run = self._execute_fake_protocol(
                    plan, Path(tmp) / f"bridge-{mini_session_index}",
                )
                quality = json.loads((run / "quality.json").read_text())
                self.assertEqual(
                    quality["schema"], "guide5_ray_fast_long_bridge_session_quality_v1",
                )
                self.assertEqual(quality["capture_count"], 3)

    def test_ray_fast_long_bridge_cli_requires_accepted_v3(self):
        called = {}

        def runner(plan, **_kwargs):
            called["plan"] = plan
            return Path("/fake/bridge")

        with tempfile.TemporaryDirectory() as tmp:
            prerequisite = Path(tmp) / "analysis-v3.json"
            prerequisite.write_text(json.dumps({
                "schema": "guide5_strip_history_order_balanced_analysis_v3",
                "status": "accepted_advisor_corrected_classification",
                "advisor_decision": "OPTION_3_CORRECT_THE_COMMON_CONTRAST",
                "guide5_parent_branch": "S-A",
                "classification": (
                    "common_warm_reentry_shift_with_session_block_heterogeneity"
                ),
                "locks": {"ray_fast_long_bridge": False, "combined_td_b": True},
            }))
            condition = thermal.ray_fast_long_bridge_start_condition(
                state="C", protocol="FAST", reset_s=600,
            )
            base = [
                "--experiment-id", thermal.RAY_FAST_LONG_BRIDGE_EXPERIMENT_ID,
                "--source", "ray", "--variant", "core", "--phase", "formal",
                "--run-name", "bridge-m1", "--execute", "--allow-device-control",
                "--direct-ray-fast-long-bridge", "--bridge-mini-session", "1",
                "--session-start-condition", condition,
                "--prerequisite-analysis", str(prerequisite),
            ]
            self.assertEqual(
                measure.main(base, run_fn=runner, backend_factory=lambda: object()), 0,
            )
            self.assertEqual(called["plan"]["bridge_state"], "C")
            self.assertEqual(called["plan"]["bridge_protocol"], "FAST")
            self.assertEqual(
                called["plan"]["scientific_prerequisite"]["status"], "pass",
            )
            invalid = json.loads(prerequisite.read_text())
            invalid["classification"] = "underpowered_or_unclassified"
            prerequisite.write_text(json.dumps(invalid))
            with self.assertRaisesRegex(ValueError, "required scientific pass"):
                measure.main(base, run_fn=runner, backend_factory=lambda: object())

    def test_ray_fast_long_bridge_analyzer_uses_four_holdout_mini_sessions(self):
        feature_ids = tuple(
            json.loads(thermal.POLICY_PATH.read_text())["feature_set"]["ids"]
        )
        prerequisite = {
            "path": "/fake/analysis-v3.json",
            "sha256": "b" * 64,
            "kind": "ray-fast-long-bridge",
            "status": "pass",
        }
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "bridge"
            for mini_session_index, (state, protocol, reset_s, _dwell_s) in enumerate(
                thermal.RAY_FAST_LONG_BRIDGE_MINI_SESSIONS, start=1,
            ):
                plan = thermal.build_ray_fast_long_bridge_session_spec(
                    mini_session_index,
                    device_control_enabled=True,
                    session_start_condition=thermal.ray_fast_long_bridge_start_condition(
                        state=state, protocol=protocol, reset_s=reset_s,
                    ),
                    scientific_prerequisite=prerequisite,
                )

                def feature_values(step, *, index=mini_session_index):
                    values = {feature_id: 1.0 for feature_id in feature_ids}
                    if index == 2 and step["role"] == "return_anchor":
                        values[feature_ids[0]] = 3.0
                    return values

                run = self._execute_fake_protocol(
                    plan,
                    root / f"mini-session-{mini_session_index}",
                    feature_values_fn=feature_values,
                )
                (run / "all-off-shell.json").write_text(json.dumps([{"ok": True}]))
                (run / "all-off-shell.exit-status.txt").write_text("0\n")
                (run / "wrapper-result.json").write_text(json.dumps({
                    "status": "complete", "child_exit_code": 0,
                    "shell_cleanup_exit_code": 0, "wrapper_exit_code": 0,
                    "signal": None,
                }))

            report = analyze.analyze_ray_fast_long_bridge(
                root, feature_ids=feature_ids,
            )
            self.assertEqual(
                report["schema"], "guide5_ray_fast_long_bridge_analysis_v1",
            )
            self.assertEqual(report["capture_count"], 12)
            self.assertEqual(report["long_session_count"], 2)
            self.assertEqual(
                report["classification"],
                "state_dependent_protocol_bias_detected",
            )
            self.assertEqual(
                report["state_dependent_bias_compatibility"]["return_delta"]["decision"],
                "detected",
            )
            self.assertTrue(report["locks"]["combined_td_b"])
            output = root / "bridge-analysis.json"
            self.assertEqual(analyze.main([
                str(root),
                "--feature-ids", str(thermal.POLICY_PATH),
                "--ray-fast-long-bridge-analysis",
                "--ray-fast-long-bridge-analysis-output", str(output),
            ]), 0)
            self.assertEqual(
                json.loads(output.read_text())["classification"],
                "state_dependent_protocol_bias_detected",
            )
            output.write_text(json.dumps(report))
            refined = analyze.analyze_ray_fast_long_bridge_v2(
                root,
                feature_ids=feature_ids,
                legacy_analysis_artifact=output,
            )
            self.assertEqual(
                refined["schema"], "guide5_ray_fast_long_bridge_analysis_v2",
            )
            self.assertIn(
                "Q_local_anchor_protocol_difference", refined["states"]["C"],
            )
            self.assertIn(
                "A_reentry_displacement_protocol_difference",
                refined["states"]["B"],
            )
            self.assertFalse(refined["measurement_contract"]["fast_long_pooling"])

    def test_combined_fast_history_uses_local_returns_and_does_not_gate_state_terms(self):
        feature_ids = tuple(
            json.loads(thermal.POLICY_PATH.read_text())["feature_set"]["ids"]
        )
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ray_root = root / "ray-history"
            strip_root = root / "strip-history"
            for source, history_root, builder in (
                ("ray", ray_root, thermal.build_ray_history_session_spec),
                ("strip", strip_root, thermal.build_strip_history_session_spec),
            ):
                for session_index in (1, 2, 3):
                    plan = builder(
                        session_index,
                        device_control_enabled=True,
                        session_start_condition=thermal.RAY_HISTORY_SESSION_START_CONDITION,
                    )

                    def feature_values(step, *, source_name=source):
                        values = {feature_id: 1.0 for feature_id in feature_ids}
                        if step["role"] not in {"initial_anchor", "return_anchor"}:
                            values[feature_ids[0]] = 2.0 if source_name == "ray" else 3.0
                        return values

                    run = self._execute_fake_protocol(
                        plan, history_root / f"session-{session_index}",
                        feature_values_fn=feature_values,
                    )
                    (run / "all-off-shell.json").write_text(json.dumps([{"ok": True}]))
                    (run / "all-off-shell.exit-status.txt").write_text("0\n")
                    (run / "wrapper-result.json").write_text(json.dumps({
                        "status": "complete", "child_exit_code": 0,
                        "shell_cleanup_exit_code": 0, "wrapper_exit_code": 0,
                        "signal": None,
                    }))
            bridge_v2 = root / "bridge-v2.json"
            bridge_v2.write_text(json.dumps({
                "schema": "guide5_ray_fast_long_bridge_analysis_v2",
                "status": "accepted_advisor_refined_holdout",
            }))
            strip_v3 = root / "strip-v3.json"
            strip_v3.write_text(json.dumps({
                "schema": "guide5_strip_history_order_balanced_analysis_v3",
                "classification": "common_warm_reentry_shift_with_session_block_heterogeneity",
            }))
            ray_history_analysis = root / "ray-history-v2.json"
            ray_history_analysis.write_text(json.dumps({
                "schema": "guide4_ray_history_order_balanced_analysis_v2",
                "classification": "common_warm_reentry_shift",
            }))
            combined = analyze.analyze_combined_fast_history_coordinate(
                ray_root, strip_root,
                feature_ids=feature_ids,
                ray_history_analysis_artifact=ray_history_analysis,
                ray_analysis_artifact=bridge_v2,
                strip_analysis_artifact=strip_v3,
            )
            self.assertEqual(combined["status"], "canonical_pass")
            self.assertEqual(combined["experiment_id"], "combined_td_b")
            self.assertEqual(combined["source_capture_count"], 42)
            self.assertEqual(combined["long_input_count"], 0)
            self.assertEqual(combined["gate"]["session"], "pass")
            self.assertEqual(
                set(combined["model"]["state_terms_not_gated_at_zero"]),
                {"B_minus_D", "C_minus_D", "C_minus_B"},
            )
            self.assertFalse(combined["locks"]["td_c_core"])

    def test_direct_main_uses_injected_runner(self):
        called = {}
        def runner(plan, **kwargs):
            called["plan"] = plan
            return Path("/fake/run")
        rc = measure.main(["--experiment-id", thermal.TD_B, "--source", "ray", "--phase", "formal", "--variant", "core", "--run-name", "x", "--execute", "--allow-device-control", "--human-authorization", thermal.TD_B_R6_EXPERIMENT_ID, "--direct-r6"], run_fn=runner, backend_factory=lambda: object())
        self.assertEqual(rc, 0)
        self.assertEqual(called["plan"]["capture_ids"], list(thermal.TD_B_R6_CAPTURE_IDS))
        with self.assertRaises(PermissionError):
            measure.main(
                ["--experiment-id", thermal.TD_B, "--source", "ray", "--phase", "formal", "--run-name", "x", "--execute", "--human-authorization", thermal.TD_B_R6_EXPERIMENT_ID, "--direct-r6"],
                run_fn=runner, backend_factory=lambda: object(),
            )

    def test_analyzer_rejects_direct_tamper(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            spec = thermal.build_ray_r6_spec(); spec["capture_ids"][0] = "tampered"
            (root / "experiment-spec.json").write_text(__import__("json").dumps(spec))
            (root / "run.json").write_text(__import__("json").dumps({"status": "complete", "experiment_id": thermal.TD_B}))
            with self.assertRaises(ValueError):
                analyze.analyze_thermal_run(root, feature_ids=())

    def test_execute_plan_uses_real_scheduler_with_fake_callbacks(self):
        spec = thermal.build_ray_r6_spec()
        calls = []
        feature_ids = tuple(json.loads(thermal.POLICY_PATH.read_text())["feature_set"]["ids"])
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "run"
            sidecar_result_by_capture = {}

            def apply(step):
                calls.append(("apply", step["capture_id"])); return {"status": "pass", "exact_command_hash": "fake", "source_on_elapsed_s": 0, "state_on_elapsed_s": 0}

            def readback(step):
                calls.append(("readback", step["capture_id"])); return {"status": "pass", "strip_verified_off": True, "ray_verified_off": True}

            def capture(step):
                index = int(step["sequence_index"])
                calls.append(("capture", step["capture_id"]))
                raw = root / (step["capture_id"] + ".cr3")
                raw.parent.mkdir(parents=True, exist_ok=True)
                raw.write_bytes((f"fake-cr3-{index}\n").encode())
                sidecar = raw.with_suffix(raw.suffix + ".metadata.json")
                sidecar.write_text("{}")
                timing = {
                    "tier": "tier_b", "status": "accepted_best_effort_anchor",
                    "provenance": thermal.TIMING_CONTRACT_V2["provenance"],
                    "best_effort_elapsed_s": float(index + 1),
                }
                command = step["command"]
                covariates = thermal.build_covariate_record(
                    source_id="ray", state_id=step["state_id"], command=command,
                    sequence_index=index, capture_order=index, source_order=1,
                    monotonic_timestamp_ns=index + 1,
                    wall_clock_timestamp="2026-08-07T00:00:00+00:00",
                    session_elapsed_s=float(index), source_on_elapsed_s=1.0,
                    state_on_elapsed_s=1.0, off_duration_before_s=0.0,
                    previous_state_id=None, previous_state_dwell_s=None,
                    shutter_seconds={"A": 1 / 5000, "D": 1 / 6400, "B": 1 / 8000, "C": 1 / 2500}[step["state_id"]],
                    raw_black_levels=(0, 0, 0, 0), raw_white_level=65535,
                    load_history={60: 0.0, 300: 0.0, 900: 0.0},
                    readback={"status": "pass"},
                )
                return {
                    "capture_id": step["capture_id"], "saved_file": str(raw),
                    "remote_metadata_path": str(sidecar), "physical_capture_count": 1,
                    "capture": {
                        "iso": "100", "aperture": "implicit auto",
                        "image_format": "RAW",
                    },
                    "timing_evidence": timing, "thermal_covariates": covariates,
                    "feature_values": {feature_id: 1.0 for feature_id in feature_ids},
                    "direct_quality": {
                        "status": "pass", "feature_count": len(feature_ids),
                    },
                    "recorded_exposure": {
                        "source": "Canon:ExposureTime", "status": "recorded",
                        "seconds": 0.97 * {"A": 1 / 5000, "D": 1 / 6400, "B": 1 / 8000, "C": 1 / 2500}[step["state_id"]],
                    },
                    "strip_zero_before_capture": {
                        "requested_payload": {
                            "red": 0, "green": 0, "blue": 0,
                            "warm_white": 0, "cold_white": 0,
                        },
                        "device_snapshot": {
                            "red": 0, "green": 0, "blue": 0,
                            "warm_white": 0, "cold_white": 0,
                        },
                    },
                }

            def gate(g):
                calls.append(("ray_off", g))
                return {
                    "status": "pass", "strip_verified_off": True,
                    "ray_verified_off": True, "ray_off_command": {"status": "pass"},
                }
            def source_isolation(g):
                calls.append(("strip_zero", g))
                return {
                    "status": "pass", "strip_verified_off": True,
                    "ray_off_command": None,
                }
            def cleanup():
                calls.append(("ray_off", "cleanup")); return {"status": "pass", "steps": [{"ok": True}]}

            def fake_sidecar(payload, *, raw_path, raw_payload=None, run_root):
                sidecar = Path(str(payload["remote_metadata_path"]))
                sidecar_result_by_capture[str(payload["capture_id"])] = True
                return {
                    "sidecar_path": str(sidecar.resolve()), "sidecar_byte_count": sidecar.stat().st_size,
                    "sidecar_sha256": hashlib.sha256(sidecar.read_bytes()).hexdigest(),
                    "sidecar_validation_status": "pass",
                    "remote_capture_id": f"remote-{payload['capture_id']}",
                    "remote_request_id": f"request-{payload['capture_id']}",
                    "remote_metadata": {
                        "capture_id": f"remote-{payload['capture_id']}",
                        "request_id": f"request-{payload['capture_id']}",
                        "exposure_start_estimate": {"method": "gphoto_event_minus_recorded_exposure"},
                    },
                    "receipt": {"timing_evidence": payload["timing_evidence"]},
                }

            with patch.object(measure, "_validate_returned_sidecar", side_effect=fake_sidecar):
                path = measure.execute_plan(
                    spec, run_dir=root, apply_command_fn=apply, readback_fn=readback,
                    capture_fn=capture, both_off_gate_fn=gate,
                    source_isolation_check_fn=source_isolation, cleanup_fn=cleanup,
                    runtime_capture_settings_provenance=spec["camera"]["resolved_capture_settings"],
                    runtime_git_provenance={"commit": "0" * 40, "dirty": False, "dirty_entries": []},
                    post_capture_validator_fn=measure.validate_direct_ray_r6_post_capture,
                    sleep_fn=lambda _: None,
                )
            self.assertTrue(path.is_dir())
            self.assertEqual(sum(1 for c in calls if c[0] == "capture"), 16)
            ray_off_indices = [index for index, call in enumerate(calls) if call[0] == "ray_off"]
            first_ray_on = next(index for index, call in enumerate(calls) if call[0] == "apply")
            self.assertEqual(len(ray_off_indices), 2)
            self.assertLess(ray_off_indices[0], first_ray_on)
            self.assertEqual(ray_off_indices[-1], len(calls) - 1)
            self.assertFalse(any(call[0] == "ray_off" for call in calls[first_ray_on:ray_off_indices[-1]]))
            self.assertEqual(len((root / "physical-returns.jsonl").read_text().splitlines()), 16)
            self.assertEqual(len((root / "captures.jsonl").read_text().splitlines()), 16)
            self.assertEqual(len(sidecar_result_by_capture), 16)
            covariates = [
                json.loads(line)
                for line in (root / "thermal-covariates.jsonl").read_text().splitlines()
                if line.strip()
            ]
            self.assertEqual(covariates[0]["previous_state_id"], None)
            self.assertEqual(covariates[5]["previous_state_id"], "D")
            self.assertEqual(covariates[6]["previous_state_id"], "A")
            self.assertTrue(all(float(row["previous_state_dwell_s"]) >= 0 for row in covariates[1:]))
            (root / "all-off-shell.json").write_text(json.dumps([{"ok": True}]))
            (root / "all-off-shell.exit-status.txt").write_text("0\n")
            (root / "wrapper-result.json").write_text(json.dumps({
                "status": "complete", "child_exit_code": 0,
                "shell_cleanup_exit_code": 0, "wrapper_exit_code": 0, "signal": None,
            }))
            report = analyze.analyze_thermal_run(root, feature_ids=feature_ids)
            self.assertEqual(report["direct_artifact_validation"], "pass")
            self.assertTrue(report["formal_pass"])
            history = report["return_anchor_history_compatibility"]
            self.assertEqual(history["anchor_order"], ["A0", "A_after_D", "A_after_B", "A_after_C"])
            self.assertEqual(history["pair_count"], 6)
            self.assertTrue(all(row["decision"] == "pass" for row in history["pairwise"]))
            self.assertEqual(set(report["chronology_by_state"]), {"B", "C", "D"})
            for chronology in report["chronology_by_state"].values():
                self.assertEqual(chronology["elapsed_s"], [60, 120, 300, 600])
                self.assertIn("score", chronology["trend"])
                self.assertIn("maximum_single_frame_variance_fraction", chronology["dominance"])
                self.assertEqual(
                    set(chronology["direction"]["slope_by_feature"]), set(feature_ids),
                )

            run_path = root / "run.json"
            run_payload = json.loads(run_path.read_text())
            run_payload["status"] = "failed"
            run_payload["capture_settings_provenance"]["aperture"] = "implicit auto"
            run_path.write_text(json.dumps(run_payload))
            (root / "failure.json").write_text(json.dumps({
                "type": "ValueError",
                "message": analyze.LEGACY_EXPOSURE_FAILURE_MESSAGE,
                "at": "2026-08-08T00:00:00+00:00",
            }))
            (root / "wrapper-result.json").write_text(json.dumps({
                "status": "child_failed", "child_exit_code": 1,
                "shell_cleanup_exit_code": 0, "wrapper_exit_code": 1,
                "signal": None,
            }))
            (root / "commands-audit.json").unlink()
            original_names = (
                "experiment-spec.json", "input-checkpoint.json", "run.json",
                "failure.json", "wrapper-result.json", "all-off-python.json",
                "all-off-shell.json", "all-off-shell.exit-status.txt",
            )
            original_hashes = {
                name: hashlib.sha256((root / name).read_bytes()).hexdigest()
                for name in original_names
            }
            original_quality_hash = hashlib.sha256(
                (root / "quality.json").read_bytes()
            ).hexdigest()
            with self.assertRaisesRegex(ValueError, "completed exact experiment"):
                analyze.analyze_thermal_run(root, feature_ids=feature_ids)

            captures_path = root / "captures.jsonl"
            original_capture_lines = captures_path.read_text().splitlines()
            tampered_capture = json.loads(original_capture_lines[0])
            tampered_capture["capture"]["recorded_exposure"]["seconds"] = 1 / 6400
            captures_path.write_text(
                "\n".join([json.dumps(tampered_capture), *original_capture_lines[1:]]) + "\n"
            )
            with self.assertRaisesRegex(ValueError, "different shutter setting"):
                analyze.revalidate_direct_ray_r6_exposure_failure(
                    root, feature_ids=feature_ids, validator_commit="1" * 40,
                )
            captures_path.write_text("\n".join(original_capture_lines) + "\n")

            cleanup_path = root / "all-off-python.json"
            original_cleanup = cleanup_path.read_bytes()
            cleanup_path.write_text(json.dumps({"status": "fail", "steps": []}))
            with self.assertRaisesRegex(ValueError, "Python cleanup"):
                analyze.revalidate_direct_ray_r6_exposure_failure(
                    root, feature_ids=feature_ids, validator_commit="1" * 40,
                )
            cleanup_path.write_bytes(original_cleanup)

            self.assertEqual(analyze.main([
                str(root), "--feature-ids", str(thermal.POLICY_PATH),
                "--revalidate-exposure-failure", "--validator-commit", "1" * 40,
            ]), 0)
            revalidation = json.loads(
                (root / analyze.POST_FIX_REVALIDATION_FILE).read_text()
            )
            self.assertEqual(revalidation["status"], "pass")
            self.assertEqual(revalidation["original_child_exit"], 1)
            self.assertTrue(revalidation["original_failure_preserved"])
            self.assertEqual(
                hashlib.sha256((root / "quality.json").read_bytes()).hexdigest(),
                original_quality_hash,
            )
            self.assertEqual(
                original_hashes,
                {
                    name: hashlib.sha256((root / name).read_bytes()).hexdigest()
                    for name in original_names
                },
            )
            derived_audit = json.loads((root / "commands-audit.json").read_text())
            self.assertTrue(derived_audit["derived_after_original_child_failure"])
            revalidated_report = json.loads((root / "analysis.json").read_text())
            self.assertTrue(revalidated_report["formal_pass"])
            self.assertEqual(
                revalidated_report["engineering_revalidation"]["status"], "pass",
            )
            self.assertEqual(
                revalidated_report["capture_settings_reconciliation"]["status"],
                "accepted_uniform_implicit_aperture",
            )
            self.assertEqual(
                revalidated_report["return_anchor_history_compatibility"]["pair_count"], 6,
            )
            retained_revalidation_hash = hashlib.sha256(
                (root / analyze.POST_FIX_REVALIDATION_FILE).read_bytes()
            ).hexdigest()
            self.assertEqual(analyze.main([
                str(root), "--feature-ids", str(thermal.POLICY_PATH),
                "--revalidate-exposure-failure", "--validator-commit", "1" * 40,
            ]), 0)
            self.assertEqual(
                hashlib.sha256(
                    (root / analyze.POST_FIX_REVALIDATION_FILE).read_bytes()
                ).hexdigest(),
                retained_revalidation_hash,
            )

            tampered_capture = json.loads(original_capture_lines[0])
            tampered_capture["capture"]["recorded_exposure"]["seconds"] = 1.0
            tampered_capture_lines = [json.dumps(tampered_capture), *original_capture_lines[1:]]
            captures_path.write_text("\n".join(tampered_capture_lines) + "\n")
            with self.assertRaises(ValueError):
                analyze.analyze_thermal_run(
                    root, feature_ids=feature_ids, post_fix_revalidation=True,
                )
            captures_path.write_text("\n".join(original_capture_lines) + "\n")
            location_copy = root / "inputs/location.json"
            original_location = location_copy.read_bytes()
            location_copy.write_bytes(original_location + b"\n")
            with self.assertRaises(ValueError):
                analyze.analyze_thermal_run(
                    root, feature_ids=feature_ids, post_fix_revalidation=True,
                )
            location_copy.write_bytes(original_location)
            (root / "quality.json").unlink()
            with self.assertRaises(ValueError):
                analyze.analyze_thermal_run(
                    root, feature_ids=feature_ids, post_fix_revalidation=True,
                )
            self.assertEqual(report["capture_count"], 16)

    def test_r6_history_failure_names_each_incompatible_anchor_pair(self):
        feature_ids = tuple(
            json.loads(thermal.POLICY_PATH.read_text())["feature_set"]["ids"]
        )
        rows = []
        for step in thermal.build_ray_r6_spec()["captures"]:
            values = {feature_id: 1.0 for feature_id in feature_ids}
            if step["role"] == "return_after_C":
                values[feature_ids[0]] = 2.0
            rows.append({
                "capture_id": step["capture_id"],
                "plan_step": step,
                "feature_values": values,
                "engineering_quality_status": "pass",
                "origin": "ray_r6",
                "run_root": "/same/root",
            })

        report = analyze.analyze_td_b(
            rows,
            feature_ids=feature_ids,
            compatibility_fn=lambda left, right: all(
                abs(float(a) - float(b)) < 1e-12 for a, b in zip(left, right)
            ),
            r6_operational_contract=True,
        )

        self.assertFalse(report["formal_pass"])
        self.assertEqual(report["status"], "history_dependent_at_operational_dwell_600")
        failed = {
            (row["left"], row["right"])
            for row in report["return_anchor_history_compatibility"]["pairwise"]
            if row["decision"] == "fail"
        }
        self.assertEqual(
            failed,
            {
                ("A0", "A_after_C"),
                ("A_after_D", "A_after_C"),
                ("A_after_B", "A_after_C"),
            },
        )

    def test_r6_vector_reanalysis_freezes_rank1_direction_without_reclassifying(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            feature_ids = self._write_r6_vector_evidence(root)

            report = analyze.analyze_r6_anchor_vectors(
                root, feature_ids=feature_ids, source_bundle_sha256="a" * 64,
                source_bundle_member="bundle/run",
                analyzer_commit="b" * 40,
            )

            self.assertEqual(report["status"], "rank1_drift_hypothesis_supported")
            self.assertGreater(report["pca"]["explained_variance_ratio"][0], 0.99)
            self.assertGreater(
                report["classical_mds"]["positive_explained_variance_ratio"][0],
                0.99,
            )
            self.assertTrue(all(
                row["cosine"] > 0.99
                for row in report["difference_vector_cosines"]
            ))
            projections = [
                row["projection_on_r6_drift_direction"]
                for row in report["anchor_projections"]
            ]
            self.assertEqual(projections, sorted(projections))
            interpretation = report["scientific_interpretation"]
            self.assertFalse(interpretation["r6_formal_pass"])
            self.assertFalse(interpretation["r6_reclassification_allowed"])
            self.assertEqual(interpretation["c_specific_carryover"], "unproven")
            self.assertEqual(interpretation["strip_combined_td_c"], "locked")
            self.assertFalse(report["input_identity"]["evidence_dir_is_authority"])
            self.assertEqual(report["input_identity"]["source_bundle_member"], "bundle/run")
            self.assertEqual(report["input_identity"]["analyzer_commit"], "b" * 40)

    def test_r6_vector_reanalysis_rejects_reclassified_input(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            feature_ids = self._write_r6_vector_evidence(root)
            analysis_path = root / "analysis.json"
            payload = json.loads(analysis_path.read_text())
            payload["formal_pass"] = True
            analysis_path.write_text(json.dumps(payload))

            with self.assertRaisesRegex(ValueError, "history-negative"):
                analyze.analyze_r6_anchor_vectors(root, feature_ids=feature_ids)

    def test_r6_vector_reanalysis_uses_corrected_dwell_ledger_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            feature_ids = self._write_r6_vector_evidence(root)
            ledger_path = root / "thermal-covariates.jsonl"
            rows = [json.loads(line) for line in ledger_path.read_text().splitlines()]
            rows[5]["previous_state_dwell_s"] = 600.0
            ledger_path.write_text("".join(json.dumps(row) + "\n" for row in rows))

            report = analyze.analyze_r6_anchor_vectors(root, feature_ids=feature_ids)

            reconciliation = report["covariate_reconciliation"]
            self.assertEqual(reconciliation["difference_count"], 1)
            self.assertEqual(reconciliation["differences"][0]["sequence_index"], 5)
            self.assertEqual(reconciliation["canonical_owner"], "thermal-covariates.jsonl")

    def test_runtime_owner_keeps_ray_on_between_first_state_and_cleanup(self):
        spec = thermal.build_ray_r6_spec()
        events = []

        class FakeBackend:
            backend_name = "remote"
            v2_capture_capability = measure.REMOTE_V2_CAPABILITY

            def connect(self):
                return object()

            def resolve_capture_settings(self, **_kwargs):
                return SimpleNamespace(iso="100", aperture="f/4", image_format="RAW")

            def capture_with_timing(self, **_kwargs):
                raise AssertionError("sequence wiring test must not capture")

        def fake_execute(plan, **kwargs):
            kwargs["both_off_gate_fn"]("run_start")
            for group in measure._ledger_groups(thermal.TD_B, plan["captures"]):
                step = group[0]
                kwargs["apply_command_fn"](step)
                kwargs["readback_fn"](step)
                kwargs["source_isolation_check_fn"](str(group[-1]["isolation_gate_after"]))
            kwargs["cleanup_fn"]()
            return Path("/fake/ray-r6")

        zero = {
            "requested_payload": {
                "red": 0, "green": 0, "blue": 0,
                "warm_white": 0, "cold_white": 0,
            },
            "device_snapshot": {
                "red": 0, "green": 0, "blue": 0,
                "warm_white": 0, "cold_white": 0,
            },
        }

        def set_hsi(hue, sat, *, intensity_percent):
            events.append(("ray_on", hue, sat, intensity_percent))
            return {"status": "pass"}

        def set_cct(*_args, **_kwargs):
            events.append(("ray_off",))
            return {"status": "pass"}

        with (
            patch.object(measure, "execute_plan", side_effect=fake_execute),
            patch("camera_based_rgbww_optimizer.optimization.measure_raw_observer_validation.build_native_raw_capture_step_fn", return_value=lambda _step: None),
            patch("camera_based_rgbww_optimizer.control.esphome.verified_light", return_value=zero),
            patch("camera_based_rgbww_optimizer.control.ray120c.set_hsi", side_effect=set_hsi),
            patch("camera_based_rgbww_optimizer.control.ray120c.get_hsi", return_value={"data": {"hue": 0, "sat": 0, "intensity": 255}}),
            patch("camera_based_rgbww_optimizer.control.ray120c.set_cct", side_effect=set_cct),
            patch("camera_based_rgbww_optimizer.control.ray120c.get_cct", return_value={"data": {"cct": 5600, "gm": 100, "intensity": 0}}),
            patch("camera_based_rgbww_optimizer.optimization.measure_ray_hsi_manifold._verify_readback"),
            patch("camera_based_rgbww_optimizer.optimization.hsi_source_evidence.validate_both_off"),
            patch("camera_based_rgbww_optimizer.control.all_off.turn_everything_off", side_effect=lambda **_kwargs: (events.append(("ray_off",)) or [{"name": "all_off", "ok": True}])),
        ):
            measure.run_authorized_plan(
                spec, output_dir=Path("/fake"), run_name="ray-r6",
                camera_backend=FakeBackend(),
            )

        self.assertEqual([event[0] for event in events], ["ray_off", *(["ray_on"] * 7), "ray_off"])
        self.assertEqual(
            [(event[1], event[2]) for event in events if event[0] == "ray_on"],
            [(120, 100), (120, 50), (120, 100), (0, 0), (120, 100), (300, 100), (120, 100)],
        )

    def test_runtime_owner_routes_strip_commands_to_esphome_not_ray_hsi(self):
        spec = thermal.build_strip_history_session_spec(
            1,
            device_control_enabled=True,
            session_start_condition=thermal.RAY_HISTORY_SESSION_START_CONDITION,
        )
        events = []

        class FakeBackend:
            backend_name = "remote"
            v2_capture_capability = measure.REMOTE_V2_CAPABILITY

            def connect(self):
                return object()

            def resolve_capture_settings(self, **_kwargs):
                return SimpleNamespace(iso="100", aperture="f/4", image_format="RAW")

            def capture_with_timing(self, **_kwargs):
                raise AssertionError("strip routing test must not capture")

        def fake_execute(_plan, **kwargs):
            kwargs["both_off_gate_fn"]("run_start")
            for step in _plan["captures"]:
                kwargs["apply_command_fn"](step)
                kwargs["readback_fn"](step)
                kwargs["source_isolation_check_fn"](step["isolation_gate_after"])
            kwargs["cleanup_fn"]()
            return Path("/fake/strip-history")

        zero = {
            "requested_payload": {
                "red": 0, "green": 0, "blue": 0,
                "warm_white": 0, "cold_white": 0,
            },
            "device_snapshot": {
                "red": 0, "green": 0, "blue": 0,
                "warm_white": 0, "cold_white": 0,
            },
        }

        def verified_light(*channels, **_kwargs):
            events.append(("strip", channels))
            return zero

        with (
            patch.object(measure, "execute_plan", side_effect=fake_execute),
            patch("camera_based_rgbww_optimizer.optimization.measure_raw_observer_validation.build_native_raw_capture_step_fn", return_value=lambda _step: None),
            patch("camera_based_rgbww_optimizer.control.esphome.verified_light", side_effect=verified_light),
            patch("camera_based_rgbww_optimizer.control.ray120c.set_hsi", side_effect=AssertionError("strip command reached Ray HSI")),
            patch("camera_based_rgbww_optimizer.control.ray120c.set_cct", return_value={"status": "pass"}),
            patch("camera_based_rgbww_optimizer.control.ray120c.get_cct", return_value={"data": {"cct": 5600, "gm": 100, "intensity": 0}}),
            patch("camera_based_rgbww_optimizer.optimization.hsi_source_evidence.validate_both_off"),
            patch("camera_based_rgbww_optimizer.control.all_off.turn_everything_off", return_value=[{"name": "all_off", "ok": True}]),
        ):
            measure.run_authorized_plan(
                spec, output_dir=Path("/fake"), run_name="strip-history",
                camera_backend=FakeBackend(),
            )

        self.assertEqual(len([event for event in events if event[0] == "strip"]), 1 + 7)
        self.assertTrue(all(len(event[1]) == 5 for event in events if event[0] == "strip"))

    def test_downstream_direct_specs_use_scientific_prerequisites(self):
        strip = thermal.build_direct_plan(thermal.TD_B, source="strip")
        td_c = thermal.build_direct_plan(thermal.TD_C)
        self.assertEqual(strip["execution_authorization"]["schema"], "direct_strip_td_b_authority_v1")
        self.assertEqual(td_c["execution_authorization"]["schema"], "direct_td_c_core_authority_v1")
        self.assertEqual(strip["timing_resolution"], "direct_operational_600")
        self.assertEqual(td_c["timing_resolution"], "guide5_reset600_D120_A120")
        self.assertEqual(
            td_c["native_raw_ambient_policy"],
            "unsubtracted_no_ambient",
        )
        self.assertEqual(td_c["budgets"], {
            "formal_cap": 8, "ambient_cap": 0, "physical_cr3_cap": 8,
        })
        self.assertEqual(td_c["session_orders"], [
            ["ray", "strip"], ["strip", "ray"],
            ["ray", "strip"], ["strip", "ray"],
        ])
        self.assertTrue(all(
            step["warm_precondition"]["state_id"] == "D"
            and step["warm_precondition"]["reset_s"] == 600
            and step["warm_precondition"]["dwell_s"] == 120
            and step["requested_elapsed_s"] == 120
            for step in td_c["captures"]
        ))
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            invalid = root / "ray-analysis.json"
            invalid.write_text(json.dumps({"experiment_id": thermal.TD_B, "formal_pass": False}))
            with self.assertRaises(ValueError):
                measure.validate_scientific_prerequisite(invalid, kind="strip-td-b")
            valid = root / "ray-analysis-pass.json"
            valid.write_text(json.dumps({
                "experiment_id": thermal.TD_B,
                "formal_pass": True,
                "return_anchor_history_effect": "pass",
            }))
            evidence = measure.validate_scientific_prerequisite(valid, kind="strip-td-b")
            self.assertEqual(evidence["status"], "pass")
            self.assertEqual(len(evidence["sha256"]), 64)
            combined = root / "combined.json"
            combined.write_text(json.dumps({
                "schema": "p7_combined_fast_history_coordinate_v1",
                "status": "canonical_pass",
                "classification": "fast_local_anchor_coordinate_compatible_for_paired_source_comparison",
                "experiment_id": "combined_td_b",
                "long_input_count": 0,
                "gate": {
                    "evidence_identity": "pass", "no_pooling": "pass",
                    "session": "pass", "position": "pass",
                    "additive_residual": "pass",
                },
                "locks": {"td_c_core": False, "td_c_expansion": True},
            }))
            self.assertEqual(
                measure.validate_scientific_prerequisite(
                    combined, kind="td-c-core",
                )["status"],
                "pass",
            )

    def test_ray_history_sessions_use_real_scheduler_and_classify_no_reproduction(self):
        feature_ids = tuple(
            json.loads(thermal.POLICY_PATH.read_text())["feature_set"]["ids"]
        )
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "history"
            root.mkdir()
            for session_index in (1, 2, 3):
                plan = thermal.build_ray_history_session_spec(
                    session_index, device_control_enabled=True,
                    session_start_condition=thermal.RAY_HISTORY_SESSION_START_CONDITION,
                )
                run = self._execute_fake_protocol(
                    plan, root / f"session-{session_index}",
                )
                self.assertEqual(len((run / "captures.jsonl").read_text().splitlines()), 7)
                gates = [
                    json.loads(line)
                    for line in (run / "isolation-gates.jsonl").read_text().splitlines()
                ]
                self.assertEqual(gates[0]["gate_kind"], "both_off")
                self.assertTrue(all(
                    row["gate_kind"] == "strip_zero_only" for row in gates[1:]
                ))
                self.assertTrue(all(
                    row["evidence"].get("ray_off_command") is None for row in gates[1:]
                ))
                (run / "all-off-shell.json").write_text(json.dumps([{"ok": True}]))
                (run / "all-off-shell.exit-status.txt").write_text("0\n")
                (run / "wrapper-result.json").write_text(json.dumps({
                    "status": "complete", "child_exit_code": 0,
                    "shell_cleanup_exit_code": 0, "wrapper_exit_code": 0,
                    "signal": None,
                }))
            direction = {feature_id: 0.0 for feature_id in feature_ids}
            direction[feature_ids[0]] = 1.0
            drift = root / "r6-vector.json"
            drift.write_text(json.dumps({
                "r6_drift_direction": {
                    "values_by_feature": direction, "sha256": "a" * 64,
                },
                "common_whitening": {
                    "feature_ids": list(feature_ids),
                    "diagonal_variance": analyze._same_state_pair_variance(
                        source="ray", state="A",
                    ).tolist(),
                },
                "scientific_interpretation": {
                    "r6_formal_pass": False,
                    "r6_reclassification_allowed": False,
                },
            }))
            report = analyze.analyze_ray_history_experiment(
                root, feature_ids=feature_ids, r6_vector_artifact=drift,
            )
            self.assertEqual(report["classification"], "R6-not-reproduced")
            self.assertFalse(report["r6_frames_pooled"])
            self.assertEqual(report["model"]["observation_count"], 9)
            self.assertEqual(report["model"]["residual_degrees_of_freedom"], 2)
            self.assertTrue(all(report["locks"].values()))
            derived = analyze.analyze_ray_history_experiment_v2(
                root, feature_ids=feature_ids, r6_vector_artifact=drift,
            )
            self.assertEqual(derived["schema"], "guide4_ray_history_order_balanced_analysis_v2")
            self.assertEqual(derived["classification"], "no_history_effect_detected")
            self.assertEqual(
                derived["legacy_classification"], "R6-not-reproduced",
            )
            self.assertFalse(derived["diagnostics"]["common_warm_reentry_detected"])
            self.assertFalse(derived["diagnostics"]["nonlinear_interaction_demonstrated"])

            captures_path = root / "session-1" / "captures.jsonl"
            original = captures_path.read_text()
            rows = [json.loads(line) for line in original.splitlines()]
            rows[0]["capture"]["strip_zero_before_capture"]["device_snapshot"]["red"] = 1
            captures_path.write_text("".join(json.dumps(row) + "\n" for row in rows))
            with self.assertRaisesRegex(ValueError, "strip-zero"):
                analyze.analyze_ray_history_experiment(
                    root, feature_ids=feature_ids, r6_vector_artifact=drift,
                )
            captures_path.write_text(original)

    def test_strip_history_session_reuses_scheduler_and_requires_ray_zero(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "strip-history"
            for session_index in (1, 2, 3):
                plan = thermal.build_strip_history_session_spec(
                    session_index,
                    device_control_enabled=True,
                    session_start_condition=thermal.RAY_HISTORY_SESSION_START_CONDITION,
                )
                self.assertEqual(plan["source"], "strip")
                self.assertFalse(plan["execution_authorization"]["human_authorization_required"])
                self.assertEqual([step["source_id"] for step in plan["captures"]], ["strip"] * 7)
                run = self._execute_fake_protocol(plan, root / f"session-{session_index}")
                (run / "all-off-shell.json").write_text(json.dumps([{"ok": True}]))
                (run / "all-off-shell.exit-status.txt").write_text("0\n")
                (run / "wrapper-result.json").write_text(json.dumps({
                    "status": "complete", "child_exit_code": 0,
                    "shell_cleanup_exit_code": 0, "wrapper_exit_code": 0,
                    "signal": None,
                }))
                rows = [json.loads(line) for line in (run / "captures.jsonl").read_text().splitlines()]
                self.assertEqual(len(rows), 7)
                self.assertTrue(all(
                    row["capture"].get("ray_zero_before_capture", {}).get("response", {}).get("data", {}).get("intensity") == 0
                    for row in rows
                ))
                gates = [json.loads(line) for line in (run / "isolation-gates.jsonl").read_text().splitlines()]
                self.assertTrue(any(gate["gate_kind"] == "strip_zero_only" for gate in gates))
            report = analyze.analyze_ray_history_experiment_v2(
                root,
                feature_ids=tuple(json.loads(thermal.POLICY_PATH.read_text())["feature_set"]["ids"]),
                r6_vector_artifact=None,
                source="strip",
            )
            self.assertEqual(report["experiment_id"], thermal.STRIP_HISTORY_3X3_EXPERIMENT_ID)
            self.assertEqual(report["classification"], "no_history_effect_detected")
            self.assertEqual(report["r6_rank1_direction_transfer"], "not_applicable")

    def test_strip_history_v3_uses_balanced_common_and_reports_session_contrasts(self):
        feature_ids = tuple(
            json.loads(thermal.POLICY_PATH.read_text())["feature_set"]["ids"]
        )
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "strip-history"
            for session_index in (1, 2, 3):
                plan = thermal.build_strip_history_session_spec(
                    session_index,
                    device_control_enabled=True,
                    session_start_condition=thermal.RAY_HISTORY_SESSION_START_CONDITION,
                )

                def feature_values(step, *, session=session_index):
                    values = {feature_id: 1.0 for feature_id in feature_ids}
                    if step["role"] == "return_anchor":
                        values[feature_ids[0]] = 2.0 if session < 3 else 3.0
                    return values

                run = self._execute_fake_protocol(
                    plan,
                    root / f"session-{session_index}",
                    feature_values_fn=feature_values,
                )
                (run / "all-off-shell.json").write_text(json.dumps([{"ok": True}]))
                (run / "all-off-shell.exit-status.txt").write_text("0\n")
                (run / "wrapper-result.json").write_text(json.dumps({
                    "status": "complete", "child_exit_code": 0,
                    "shell_cleanup_exit_code": 0, "wrapper_exit_code": 0,
                    "signal": None,
                }))

            legacy = analyze.analyze_ray_history_experiment_v2(
                root,
                feature_ids=feature_ids,
                r6_vector_artifact=None,
                source="strip",
            )
            legacy_path = root / "analysis-v2.json"
            legacy_path.write_text(json.dumps(legacy))
            report = analyze.analyze_strip_history_experiment_v3(
                root,
                feature_ids=feature_ids,
                legacy_analysis_artifact=legacy_path,
            )

            self.assertEqual(
                report["schema"], "guide5_strip_history_order_balanced_analysis_v3",
            )
            self.assertEqual(
                report["status"], "accepted_advisor_corrected_classification",
            )
            self.assertEqual(report["guide5_parent_branch"], "S-A")
            self.assertEqual(
                report["classification"],
                "common_warm_reentry_shift_with_session_block_heterogeneity",
            )
            self.assertAlmostEqual(
                report["balanced_common_variance_scalar_relative_to_one_delta"],
                2 / 9,
            )
            self.assertEqual(
                report["incorrect_legacy_common_estimand"],
                "treatment_coded_baseline_cell_intercept",
            )
            self.assertEqual(len(report["raw_return_deltas"]), 9)
            self.assertTrue(
                report["diagnostics"]["balanced_common_warm_reentry_detected"],
            )
            self.assertNotIn("common_warm_reentry_detected", report["diagnostics"])
            self.assertEqual(
                report["session_contrasts"]["session3_minus_session2"]["decision"],
                "detected",
            )
            self.assertFalse(report["locks"]["ray_fast_long_bridge"])
            self.assertTrue(report["locks"]["combined_td_b"])

    def test_equal_dwell_repeated_state_visits_do_not_share_observed_chronology(self):
        plan = thermal.build_ray_history_session_spec(
            1,
            device_control_enabled=True,
            session_start_condition=thermal.RAY_HISTORY_SESSION_START_CONDITION,
        )
        observed_by_index = (130.0, 126.0, 127.0, 126.5, 125.0, 126.25, 124.5)
        with tempfile.TemporaryDirectory() as tmp:
            run = self._execute_fake_protocol(
                plan,
                Path(tmp) / "history",
                observed_elapsed_fn=lambda _step, index: observed_by_index[index],
            )
            rows = [
                json.loads(line)
                for line in (run / "captures.jsonl").read_text().splitlines()
            ]
            self.assertEqual(len(rows), 7)
            self.assertEqual(
                [row["best_effort_exposure_start_elapsed_s"] for row in rows],
                list(observed_by_index),
            )

    def test_multi_timepoint_group_still_requires_increasing_observed_chronology(self):
        plan = thermal.build_ray_r6_spec()

        def observed_elapsed(step, index):
            if step["capture_id"] == "001-ray-d-t60":
                return 61.0
            if step["capture_id"] == "002-ray-d-t120":
                return 60.0
            return float(index + 100)

        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(
                RuntimeError,
                "non-increasing observed chronology for 002-ray-d-t120",
            ):
                self._execute_fake_protocol(
                    plan,
                    Path(tmp) / "r6",
                    observed_elapsed_fn=observed_elapsed,
                )

    def test_strip_and_td_c_use_the_real_scheduler_with_fake_callbacks(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for name, plan in (
                ("strip", thermal.build_direct_plan(thermal.TD_B, source="strip")),
                ("td-c", thermal.build_direct_plan(thermal.TD_C)),
            ):
                prerequisite = root / f"{name}-analysis.json"
                prerequisite.write_text(json.dumps({
                    "experiment_id": thermal.TD_B if name == "strip" else "combined_td_b",
                    "formal_pass": name == "strip",
                    "return_anchor_history_effect": "pass",
                    "status": "combined_td_b_pass" if name == "td-c" else "pass",
                }))
                plan["scientific_prerequisite"] = {
                    "path": str(prerequisite.resolve()),
                    "sha256": hashlib.sha256(prerequisite.read_bytes()).hexdigest(),
                    "kind": name,
                    "status": "pass",
                }
                run = self._execute_fake_protocol(plan, root / name)
                self.assertTrue(run.is_dir())
                captures = (run / "captures.jsonl").read_text().splitlines()
                self.assertEqual(len(captures), len(plan["captures"]))
                quality = json.loads((run / "quality.json").read_text())
                self.assertEqual(quality["capture_count"], plan["budgets"]["formal_cap"])
                (run / "all-off-shell.json").write_text(json.dumps([{"ok": True}]))
                (run / "all-off-shell.exit-status.txt").write_text("0\n")
                (run / "wrapper-result.json").write_text(json.dumps({
                    "status": "complete", "child_exit_code": 0,
                    "shell_cleanup_exit_code": 0, "wrapper_exit_code": 0, "signal": None,
                }))
                if name == "td-c":
                    run_payload = json.loads((run / "run.json").read_text())
                    run_payload["capture_settings_provenance"]["aperture"] = "implicit auto"
                    (run / "run.json").write_text(json.dumps(run_payload))
                    capture_rows = [
                        json.loads(line)
                        for line in (run / "captures.jsonl").read_text().splitlines()
                    ]
                    for row in capture_rows:
                        row["capture"]["capture"] = {
                            "iso": "100",
                            "aperture": "implicit auto",
                            "image_format": "RAW",
                        }
                    (run / "captures.jsonl").write_text(
                        "".join(json.dumps(row) + "\n" for row in capture_rows)
                    )
                report = analyze.analyze_thermal_run(
                    run,
                    feature_ids=tuple(json.loads(thermal.POLICY_PATH.read_text())["feature_set"]["ids"]),
                    compatibility_fn=lambda _left, _right: True,
                )
                self.assertEqual(report["direct_artifact_validation"], "pass")
                if name == "td-c":
                    self.assertEqual(
                        report["capture_settings_reconciliation"]["status"],
                        "accepted_uniform_implicit_aperture",
                    )
                    commands = [
                        json.loads(line)
                        for line in (run / "commands.jsonl").read_text().splitlines()
                    ]
                    self.assertEqual(
                        len([row for row in commands if row["event"] == "warm_precondition_command_readback_verified"]),
                        8,
                    )
                    self.assertEqual(report["warm_precondition"], "reset600_then_D120_then_A120")
                    self.assertTrue(report["td_c_expansion_locked"])

    def test_td_c_core_corrected_contrasts_match_advisor_estimands(self):
        root = Path(
            "/Volumes/4T/temp/rgbww-optimizer/"
            "guide5-td-c-core-20260812-151638-noambient-fix"
        )
        if not root.is_dir():
            self.skipTest("retained accepted TD-C core root is unavailable")
        feature_ids = tuple(
            json.loads(thermal.POLICY_PATH.read_text())["feature_set"]["ids"]
        )
        legacy_bytes = (root / "analysis.json").read_bytes()
        with patch.object(
            analyze,
            "calibrate_direct_limits",
            side_effect=AssertionError("difference-center helper must not be used"),
        ):
            report = analyze.analyze_td_c_core_contrasts_v2_1(
                root,
                feature_ids=feature_ids,
                legacy_analysis_artifact=root / "analysis.json",
            )
        self.assertEqual((root / "analysis.json").read_bytes(), legacy_bytes)
        self.assertEqual(report["status"], "canonical_pass")
        self.assertEqual(
            report["refined_status"],
            "stable_order_invariant_nonzero_warm_A_cross_source_offset_established",
        )
        self.assertAlmostEqual(
            report["ray_center_pairwise"]["maximum_score"], 4.7728227800, places=9,
        )
        self.assertAlmostEqual(
            report["strip_center_pairwise"]["maximum_score"], 5.3379311421, places=9,
        )
        self.assertAlmostEqual(
            report["paired_offset_pairwise"]["maximum_score"], 5.7765306838, places=9,
        )
        self.assertAlmostEqual(
            report["source_order_contrast"]["score"], 3.2538875744, places=9,
        )
        self.assertEqual(report["source_order_contrast"]["decision"], "pass")
        self.assertEqual(
            report["absolute_offset"]["zero_compatibility"],
            "fail_expected_pre_solver",
        )
        self.assertFalse(report["absolute_offset"]["hard_gate"])
        self.assertFalse(report["absolute_offset"]["warm_A_cross_source_match"])
        self.assertTrue(report["measurement_contract"]["source_level_monte_carlo"])
        self.assertFalse(
            report["measurement_contract"]["difference_vector_used_as_unit_center"],
        )
        self.assertFalse(report["locks"]["fast_B_C_endpoint_holdout"])
        self.assertTrue(report["locks"]["legacy_td_c_expansion"])
        self.assertTrue(report["locks"]["solver_sentinel_and_later"])
        self.assertLess(report["absolute_offset"]["guarded_limit"], 20.0)

    def test_td_c_core_corrected_cli_writes_once_without_mutating_legacy(self):
        source = Path(
            "/Volumes/4T/temp/rgbww-optimizer/"
            "guide5-td-c-core-20260812-151638-noambient-fix"
        )
        if not source.is_dir():
            self.skipTest("retained accepted TD-C core root is unavailable")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "td-c-core"
            root.mkdir()
            for name in ("analysis.json", "captures.jsonl"):
                (root / name).write_bytes((source / name).read_bytes())
            legacy_bytes = (root / "analysis.json").read_bytes()
            output = root / "analysis-v2.1-td-c-core-contrasts-derived.json"
            argv = [
                str(root),
                "--feature-ids", str(thermal.POLICY_PATH),
                "--td-c-core-contrasts-v2-1",
                "--legacy-td-c-core-analysis-artifact", str(root / "analysis.json"),
                "--td-c-core-contrasts-output", str(output),
            ]
            self.assertEqual(analyze.main(argv), 0)
            self.assertTrue(output.is_file())
            self.assertEqual(json.loads(output.read_text())["status"], "canonical_pass")
            self.assertEqual((root / "analysis.json").read_bytes(), legacy_bytes)
            derived_bytes = output.read_bytes()
            with self.assertRaisesRegex(FileExistsError, "immutable"):
                analyze.main(argv)
            self.assertEqual(output.read_bytes(), derived_bytes)
            self.assertEqual((root / "analysis.json").read_bytes(), legacy_bytes)

    def test_td_c_fast_endpoint_plan_runs_exact_b_c_direct_protocol(self):
        plan = thermal.build_direct_plan(
            thermal.TD_C, variant=thermal.TD_C_FAST_ENDPOINT_HOLDOUT_VARIANT,
        )
        self.assertEqual(
            plan["guide_experiment_id"],
            thermal.TD_C_FAST_ENDPOINT_HOLDOUT_EXPERIMENT_ID,
        )
        self.assertEqual(plan["budgets"], {
            "formal_cap": 8, "ambient_cap": 0, "physical_cr3_cap": 8,
            "setup_physical_cr3_cap": 0, "retry": 0,
        })
        self.assertEqual(plan["session_states"], ["B", "C", "B", "C"])
        self.assertEqual(plan["session_orders"], [
            ["ray", "strip"], ["strip", "ray"],
            ["strip", "ray"], ["ray", "strip"],
        ])
        self.assertEqual(plan["frozen_shutters"], {
            "ray-h0-s0": "1/8000", "ray-h300-s100": "1/2500",
            "strip-h0-s0-fullscale": "1/500",
            "strip-h300-s100-fullscale": "1/125",
        })
        self.assertTrue(all(
            [row["state_id"] for row in step["warm_precondition_sequence"]]
            == ["D", "A"]
            and all(row["dwell_s"] == 120 for row in step["warm_precondition_sequence"])
            and step["requested_elapsed_s"] == 120
            for step in plan["captures"]
        ))
        with tempfile.TemporaryDirectory() as tmp:
            run = self._execute_fake_protocol(plan, Path(tmp) / "endpoint")
            rows = [json.loads(line) for line in (run / "captures.jsonl").read_text().splitlines()]
            self.assertEqual(len(rows), 8)
            self.assertTrue(all(
                isinstance(row["capture"].get("strip_zero_before_capture"), dict)
                if row["source_id"] == "ray"
                else isinstance(row["capture"].get("ray_zero_before_capture"), dict)
                for row in rows
            ))
            commands = [json.loads(line) for line in (run / "commands.jsonl").read_text().splitlines()]
            self.assertEqual(
                len([row for row in commands if row["event"] == "warm_precondition_command_readback_verified"]),
                16,
            )
            report = analyze.analyze_td_c_fast_endpoint_holdout(
                run,
                feature_ids=tuple(json.loads(thermal.POLICY_PATH.read_text())["feature_set"]["ids"]),
                core_contrast_artifact=thermal.TD_C_CORE_CONTRAST_ARTIFACT,
                combined_artifact=thermal.COMBINED_FAST_HISTORY_ARTIFACT,
            )
            self.assertEqual(report["capture_count"], 8)
            self.assertEqual(set(report["states"]), {"B", "C"})
            for state in report["states"].values():
                self.assertEqual(
                    state["independent_synthesis_agreement"]["hard_gate"], True,
                )
                self.assertEqual(
                    state["residual_covariance"],
                    "new_endpoint_mean+(core_A_absolute_mean)+(combined_local_state_mean)",
                )
                self.assertFalse(state["pre_solver_offset_zero_gated"])
            self.assertTrue(report["locks"]["legacy_td_c_expansion"])
            self.assertTrue(report["locks"]["solver_sentinel_and_later"])
            captures_path = run / "captures.jsonl"
            rows[-1]["capture"]["ray_zero_before_capture"] = {
                "response": {"data": {"intensity": 1}},
            }
            captures_path.write_text("".join(json.dumps(row) + "\n" for row in rows))
            with self.assertRaisesRegex(ValueError, "Ray-zero"):
                measure.validate_direct_protocol_post_capture(run, plan, None)

    def test_td_c_endpoint_decomposition_is_immutable_and_keeps_locks(self):
        root = Path("/Volumes/4T/temp/rgbww-optimizer/guide5-td-c-fast-endpoint-holdout-20260813-073328")
        artifact = root / "analysis-v2-residual-decomposition-derived-v2.json"
        if not artifact.is_file():
            self.skipTest("retained endpoint decomposition is unavailable")
        report = json.loads(artifact.read_text())
        self.assertEqual(report["schema"], "guide5_td_c_fast_endpoint_residual_decomposition_v1")
        self.assertEqual(report["status"], "offline_derived_no_parent_refit")
        self.assertEqual(report["classification"], "absolute_composition_rejected_endpoint_observations_retained")
        self.assertIn("B_minus_C_synthesis_residual", report["scores"])
        self.assertIn("A_after_B_minus_A_after_D", report["vectors"])
        self.assertIn("A_after_C_minus_A_after_D", report["vectors"])
        self.assertFalse(report["covariance"]["refit_endpoint_data"])
        self.assertTrue(report["locks"]["C_validation"])
        self.assertTrue(report["locks"]["solver_sentinel_and_later"])

    def test_td_c_fast_anchor_direction_b_is_plan_only_and_exact_12_capture(self):
        plan = thermal.build_direct_plan(
            thermal.TD_C, variant=thermal.TD_C_FAST_ANCHOR_DIRECTION_B_VARIANT,
        )
        self.assertEqual(plan["status"], "deferred_diagnostic_only")
        self.assertFalse(plan["formal_capture_eligible"])
        self.assertEqual(plan["guide_experiment_id"], thermal.TD_C_FAST_ANCHOR_DIRECTION_B_EXPERIMENT_ID)
        self.assertEqual(plan["budgets"]["formal_cap"], 12)
        self.assertEqual(plan["session_orders"], [["ray", "strip"], ["strip", "ray"]])
        self.assertEqual([step["state_id"] for step in plan["captures"]], ["A", "B", "A", "A", "B", "A", "A", "B", "A", "A", "B", "A"])
        self.assertTrue(plan["hard_locks"]["C_validation"])

    def test_td_c_endpoint_exact_context_v3_excludes_r6_and_serializes_mc_terms(self):
        root = Path("/Volumes/4T/temp/rgbww-optimizer/guide5-td-c-fast-endpoint-holdout-20260813-073328")
        artifact = root / "analysis-v3-exact-context-anchor-decomposition-v1.json"
        if not artifact.is_file():
            self.skipTest("retained v3 decomposition is unavailable")
        report = json.loads(artifact.read_text())
        self.assertEqual(report["schema"], "guide5_td_c_fast_endpoint_exact_context_decomposition_v3")
        self.assertEqual(report["r6_input_count"], 0)
        self.assertEqual(report["status"], "offline_derived_no_parent_refit")
        self.assertIn("B_exact_pre_synthesis_residual", report["contrasts"])
        self.assertIn("B_exact_post_synthesis_residual", report["contrasts"])
        self.assertIn("B_anchor_direction", report["contrasts"])
        self.assertIn("B_minus_C_synthesis_residual", report["contrasts"])
        self.assertLess(report["identity_error"], 0.01)
        for contrast in report["contrasts"].values():
            self.assertFalse(contrast["monte_carlo"]["difference_center_used"])
            self.assertTrue(contrast["primitive_terms"])

    def test_td_c_endpoint_exact_context_v4_has_sign_corrected_scores_and_exact_identity(self):
        root = Path("/Volumes/4T/temp/rgbww-optimizer/guide5-td-c-fast-endpoint-holdout-20260813-073328")
        artifact = root / "v4-corrected/analysis-v4-exact-context-sign-corrected-derived.json"
        if not artifact.is_file():
            self.skipTest("retained v4 decomposition is unavailable")
        report = json.loads(artifact.read_text())
        self.assertEqual(report["schema"], "guide5_td_c_fast_endpoint_exact_context_decomposition_v4")
        self.assertEqual(
            report["classification"],
            "B_local_coordinate_transfer_unresolved_with_anchor_direction_compatible",
        )
        self.assertLessEqual(report["identity_max_abs"], 1e-12)
        self.assertLessEqual(report["identity_l2"], 1e-12)
        self.assertEqual(report["coefficient_identity_nonzero_terms"], {})
        expected = {
            "B_exact_pre_synthesis_residual": (24.341350574998774, "fail"),
            "B_exact_post_synthesis_residual": (24.37011085295253, "fail"),
            "B_anchor_direction": (2.8927944104915984, "pass"),
            "B_minus_C_synthesis_residual": (21.57223112462142, "fail"),
        }
        for name, (score, decision) in expected.items():
            self.assertAlmostEqual(report["contrasts"][name]["score"], score, delta=1e-9)
            self.assertEqual(report["contrasts"][name]["decision"], decision)
        self.assertEqual(report["locks"]["B_prepost_experiments"], "deferred_diagnostic_only")
        self.assertFalse(report["locks"]["direct_target_local_sentinel"])

    def test_guide6_h120_s100_target_local_plan_is_human_pending_and_no_synthesis(self):
        plan = thermal.build_direct_plan(
            thermal.TD_C,
            variant=thermal.GUIDE6_DIRECT_TARGET_LOCAL_H120_S100_VARIANT,
        )
        self.assertEqual(plan["status"], "execute_authorized")
        self.assertTrue(plan["formal_capture_eligible"])
        self.assertFalse(plan["execution_authorization"]["human_authorization_required"])
        self.assertEqual(plan["guide_experiment_id"], thermal.GUIDE6_DIRECT_TARGET_LOCAL_H120_S100_EXPERIMENT_ID)
        self.assertFalse(plan["analysis_contract"]["cross_experiment_absolute_synthesis"])
        self.assertEqual([step["role"] for step in plan["captures"]], [
            "ray_precondition", "ray_precondition", "ray_q_before",
            "strip_precondition", "strip_precondition", "strip_candidate",
            "ray_postcondition", "ray_postcondition", "ray_q_after",
        ])


if __name__ == "__main__":
    unittest.main()
