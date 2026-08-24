import hashlib
import json
import shutil
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
        applied_steps=None, diagnostic_status_fn=None,
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
            if step["formal_measurement"] or plan["execution_authorization"]["schema"] in {
                "direct_guide8_ray_emission_exposure_v1",
                "direct_guide6_strip_exposure_qualification_v1",
                "direct_guide9_scale_age_discrimination_v1",
            }:
                output["feature_values"] = (
                    feature_values_fn(step)
                    if feature_values_fn is not None
                    else {feature_id: 1.0 for feature_id in feature_ids}
                )
                output["direct_quality"] = {
                    "status": (
                        diagnostic_status_fn(step)
                        if diagnostic_status_fn is not None else "pass"
                    ),
                    "feature_count": len(feature_ids),
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
            elif plan["execution_authorization"]["schema"] in (
                measure.GUIDE9_CANDIDATE_BATCH_SCHEMAS
                | measure.GUIDE9_BEST_REPEAT_SCHEMAS
            ) or plan["execution_authorization"]["schema"] in {
                "direct_strip_history_session_v1",
                "direct_td_c_fast_endpoint_holdout_v1",
                "direct_guide6_target_local_h120_s100_v1",
                "direct_guide7_f2_alternate_face_v1",
                "direct_guide7_f2_short_endpoint_v1",
                "direct_guide7_f2_scale3072_stability_v1",
                "direct_guide7_f2_scale2048_stability_v1",
                "direct_guide6_strip_exposure_qualification_v1",
                "direct_guide9_scale_age_discrimination_v1",
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
            if plan["execution_authorization"]["schema"] in (
                measure.GUIDE9_CANDIDATE_BATCH_SCHEMAS
                | measure.GUIDE9_BEST_REPEAT_SCHEMAS
            ) or plan["execution_authorization"]["schema"] in {
                "direct_strip_history_session_v1",
                "direct_guide6_strip_exposure_qualification_v1",
            }:
                return {
                    "status": "pass", "source_verified_zero": True,
                    "source_verified": "ray", "strip_verified_off": True,
                    "ray_verified_off": True,
                    "ray_off_command": {"status": "pass", "data": {"intensity": 0}},
                }
            return {
                "status": "pass", "strip_verified_off": True,
                "source_verified_zero": True, "ray_off_command": None,
            }

        direct_ray_continuous = (
            plan["execution_authorization"]["schema"]
            in measure.GUIDE9_CANDIDATE_BATCH_SCHEMAS
            | measure.GUIDE9_BEST_REPEAT_SCHEMAS
        ) or plan["execution_authorization"]["schema"] in {
            "direct_ray_r6_authority_v1",
            "direct_ray_history_session_v1",
            "direct_strip_history_session_v1",
            "direct_ray_fast_long_bridge_session_v1",
            "direct_guide6_target_local_h120_s100_v1",
            "direct_guide7_f2_alternate_face_v1",
            "direct_guide7_f2_short_endpoint_v1",
            "direct_guide7_f2_scale3072_stability_v1",
            "direct_guide7_f2_scale2048_stability_v1",
            "direct_guide8_ray_emission_exposure_v1",
            "direct_guide6_strip_exposure_qualification_v1",
            "direct_guide9_scale_age_discrimination_v1",
        }

        with patch.object(measure, "_validate_returned_sidecar", side_effect=fake_sidecar):
            return measure.execute_plan(
                plan, run_dir=root,
                apply_command_fn=lambda step: (
                    applied_steps.append(dict(step)) if applied_steps is not None else None
                ) or {"status": "pass"},
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
                    if plan["execution_authorization"]["schema"] not in {
                        "direct_guide8_ray_emission_exposure_v1",
                        "direct_guide6_strip_exposure_qualification_v1",
                    }
                    else measure.validate_direct_guide8_post_capture
                    if plan["execution_authorization"]["schema"]
                    == "direct_guide8_ray_emission_exposure_v1"
                    else measure.validate_direct_guide6_strip_exposure_post_capture
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
                raise AssertionError("runtime wiring test must not capture")

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

    def test_run_authorized_plan_routes_guide6_source_isolation_and_cleanup(self):
        spec = thermal.build_direct_plan(
            thermal.TD_C,
            variant=thermal.GUIDE6_DIRECT_TARGET_LOCAL_H120_S100_VARIANT,
        )
        routed = {}

        class FakeBackend:
            backend_name = "remote"
            v2_capture_capability = measure.REMOTE_V2_CAPABILITY

            def connect(self):
                return object()

            def resolve_capture_settings(self, **_kwargs):
                return SimpleNamespace(iso="100", aperture="f/4", image_format="RAW")

            def capture_with_timing(self, **_kwargs):
                raise AssertionError("routing test must not capture")

        def fake_execute(_plan, **kwargs):
            routed.update(kwargs)
            isolation = kwargs["source_isolation_check_fn"]("guide6-strip")
            self.assertTrue(isolation["source_verified_zero"])
            self.assertEqual(isolation["source_verified"], "ray")
            self.assertEqual(kwargs["cleanup_fn"]()["status"], "pass")
            return Path("/fake/guide6")

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
        with (
            patch.object(measure, "execute_plan", side_effect=fake_execute),
            patch("camera_based_rgbww_optimizer.optimization.measure_raw_observer_validation.build_native_raw_capture_step_fn", return_value=lambda _step: None),
            patch("camera_based_rgbww_optimizer.control.esphome.verified_light", return_value=zero),
            patch("camera_based_rgbww_optimizer.control.ray120c.set_cct", return_value={"status": "pass"}),
            patch("camera_based_rgbww_optimizer.control.ray120c.get_cct", return_value={"data": {"cct": 5600, "gm": 100, "intensity": 0}}),
            patch("camera_based_rgbww_optimizer.control.all_off.turn_everything_off", return_value=[{"name": "all_off", "ok": True}]),
        ):
            result = measure.run_authorized_plan(
                spec, output_dir=Path("/fake"), run_name="guide6",
                camera_backend=FakeBackend(),
            )
        self.assertEqual(result, Path("/fake/guide6"))
        self.assertIsNotNone(routed["source_isolation_check_fn"])

    def test_run_authorized_plan_guide8_uses_checkpointed_location(self):
        spec = thermal.build_direct_plan(
            thermal.TD_C, variant=thermal.GUIDE8_RAY_EMISSION_EXPOSURE_VARIANT,
        )
        captured_builder_kwargs = {}

        class FakeBackend:
            backend_name = "remote"
            v2_capture_capability = measure.REMOTE_V2_CAPABILITY

            def connect(self):
                return object()

            def resolve_capture_settings(self, **_kwargs):
                return SimpleNamespace(iso="100", aperture="f/4", image_format="RAW")

            def capture_with_timing(self, **_kwargs):
                raise AssertionError("routing test must not capture")

        def fake_builder(**kwargs):
            captured_builder_kwargs.update(kwargs)
            return lambda _step: None

        with (
            patch.object(measure, "execute_plan", return_value=Path("/fake/guide8")),
            patch.object(
                measure.raw_validation, "build_native_raw_capture_step_fn",
                side_effect=fake_builder,
            ),
        ):
            result = measure.run_authorized_plan(
                spec, output_dir=Path("/fake"), run_name="guide8",
                camera_backend=FakeBackend(),
            )

        self.assertEqual(result, Path("/fake/guide8"))
        self.assertEqual(
            captured_builder_kwargs["location_config_path"],
            Path("/fake/guide8/inputs/location.json"),
        )
        self.assertNotEqual(
            captured_builder_kwargs["location_config_path"], thermal.LOCATION_PATH,
        )

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

    def test_guide6_h120_s100_target_local_plan_is_exact_and_no_synthesis(self):
        plan = thermal.build_direct_plan(
            thermal.TD_C,
            variant=thermal.GUIDE6_DIRECT_TARGET_LOCAL_H120_S100_VARIANT,
        )
        self.assertEqual(plan["status"], "execute_authorized")
        self.assertTrue(plan["formal_capture_eligible"])
        self.assertFalse(plan["execution_authorization"]["human_authorization_required"])
        self.assertEqual(plan["guide_experiment_id"], thermal.GUIDE6_DIRECT_TARGET_LOCAL_H120_S100_EXPERIMENT_ID)
        self.assertEqual(plan["frozen_shutters"]["strip-h120-s100-fullscale"], "1/400")
        self.assertEqual(plan["analysis_contract"]["strip_guard_nominal_shutter"], "1/320")
        self.assertFalse(plan["analysis_contract"]["strip_guard_reacquire_allowed"])
        self.assertEqual(
            plan["inputs"]["strip_exposure_policy"]["sha256"],
            hashlib.sha256(thermal.GUIDE6_STRIP_EXPOSURE_POLICY_PATH.read_bytes()).hexdigest(),
        )
        self.assertFalse(plan["analysis_contract"]["cross_experiment_absolute_synthesis"])
        self.assertEqual([step["role"] for step in plan["captures"]], [
            "ray_q_before", "strip_base", "strip_probe_cw", "strip_probe_ww",
            "strip_base_anchor_after_probe_2", "strip_probe_r", "strip_probe_b",
            "strip_base_anchor_after_probe_4", "ray_q_after",
        ])
        contract = plan["local_controllability_contract"]
        self.assertEqual(contract["base_command"], {"cw": 518, "ww": 0, "r": 0, "g": 4095, "b": 0})
        self.assertEqual(contract["probes"], {
            "cw": {"cw": 774, "ww": 0, "r": 0, "g": 4095, "b": 0},
            "ww": {"cw": 518, "ww": 256, "r": 0, "g": 4095, "b": 0},
            "r": {"cw": 518, "ww": 0, "r": 256, "g": 4095, "b": 0},
            "b": {"cw": 518, "ww": 0, "r": 0, "g": 4095, "b": 256},
        })
        self.assertEqual(plan["budgets"], {
            "ray_cap": 2, "strip_cap": 14, "formal_cap": 16,
            "physical_cr3_cap": 16, "ambient_cap": 0, "retry": 0,
            "confirmation_reserved": 3,
        })
        self.assertEqual(contract["backtrack_factors"], [1.0, 0.5, 0.25])
        self.assertEqual(contract["maximum_absolute_step"], 768)
        self.assertEqual(contract["maximum_model_rebases"], 1)
        self.assertEqual(contract["rebase_extra_probes"], 0)

    def test_guide6_lc_b_continuation_is_centered_and_single_generation(self):
        plan = thermal.build_direct_plan(
            thermal.TD_C,
            variant=(
                thermal.GUIDE6_DIRECT_TARGET_LOCAL_H120_S100_CONTINUATION_VARIANT
            ),
        )
        contract = plan["local_controllability_contract"]
        self.assertEqual(plan["guide_experiment_id"], (
            thermal.GUIDE6_DIRECT_TARGET_LOCAL_H120_S100_CONTINUATION_EXPERIMENT_ID
        ))
        self.assertEqual(
            plan["execution_authorization"]["schema"],
            "direct_guide6_target_local_h120_s100_v1",
        )
        self.assertTrue(plan["execution_authorization"]["bounded_device_scope"])
        self.assertEqual(
            plan["execution_authorization"]["experiment_id"],
            thermal.GUIDE6_DIRECT_TARGET_LOCAL_H120_S100_CONTINUATION_EXPERIMENT_ID,
        )
        self.assertEqual(contract["continuation_generation"], 1)
        self.assertEqual(contract["base_command"], {
            "cw": 0, "ww": 0, "r": 377, "g": 4095, "b": 107,
        })
        self.assertEqual(contract["probes"], {
            "cw": {"cw": 256, "ww": 0, "r": 377, "g": 4095, "b": 107},
            "ww": {"cw": 0, "ww": 256, "r": 377, "g": 4095, "b": 107},
            "r": {"cw": 0, "ww": 0, "r": 633, "g": 4095, "b": 107},
            "b": {"cw": 0, "ww": 0, "r": 377, "g": 4095, "b": 363},
        })
        self.assertIn("lc_b_continuation", plan["inputs"])
        self.assertEqual(plan["frozen_shutters"]["strip-h120-s100-fullscale"], "1/400")

    def test_guide7_f2_plan_and_nonfaithful_repeats_use_selected_cw_face(self):
        import numpy as np
        plan = thermal.build_direct_plan(thermal.TD_C, variant=thermal.GUIDE7_F2_VARIANT)
        contract = plan["local_controllability_contract"]
        self.assertEqual(plan["guide_experiment_id"], thermal.GUIDE7_F2_EXPERIMENT_ID)
        self.assertEqual(contract["active_channel"], "cw")
        self.assertEqual(contract["free_channels"], ["ww", "r", "g", "b"])
        self.assertEqual(contract["base_command"], {
            "cw": 4095, "ww": 0, "r": 0, "g": 3839, "b": 0,
        })
        self.assertEqual(contract["repeat_best_nonfaithful_count"], 3)
        measure._validate_execution_shutter_ledger(plan)
        feature_ids = tuple(f"f{index}" for index in range(58))
        base = contract["base_command"]
        free = contract["free_channels"]
        roles = []
        def fake_measure(step):
            roles.append(step["role"])
            vector = np.zeros(58)
            if step["source_id"] == "strip":
                vector[0] = 100.0
                for index, channel in enumerate(free, start=1):
                    vector[index] = 1.0 - (int(step["command"][channel]) - base[channel]) / 256.0
                self.assertEqual(step["command"]["cw"], 4095)
            return {"_vector": vector, "direct_quality": {"status": "pass", "feature_count": 58}, "feature_values": {name: 1.0 for name in feature_ids}}
        with (
            patch.object(measure, "_guide6_feature_vector", side_effect=lambda c, _: np.asarray(c["_vector"])),
            patch.object(measure, "_guide6_variances", return_value=(np.ones(58), np.ones(58))),
            patch.object(measure, "calibrate_direct_limits", return_value={"guarded_limit": 0.05, "statistic": "synthetic"}),
        ):
            result = measure.run_guide6_local_controllability_protocol(
                plan, measure_fn=fake_measure, feature_ids=feature_ids,
                source_isolation_fn=lambda _source: {"status": "pass", "source_verified_zero": True},
                cleanup_fn=lambda: {"status": "pass"},
            )
        self.assertEqual(result["lc_branch"], "LC-B")
        self.assertEqual(roles[-4:], ["strip_repeat_1", "strip_repeat_2", "strip_repeat_3", "ray_q_after"])
        self.assertLessEqual(result["counts"]["total"], 16)
        self.assertTrue(result["guide7_f2"])
        self.assertEqual(result["active_face"], "cw")

    def test_guide7_f2_repeats_base_when_solver_has_no_unique_candidate(self):
        import numpy as np
        plan = thermal.build_direct_plan(thermal.TD_C, variant=thermal.GUIDE7_F2_VARIANT)
        feature_ids = tuple(f"f{index}" for index in range(58))
        roles = []
        commands = []
        def fake_measure(step):
            roles.append(step["role"])
            commands.append(dict(step["command"]))
            vector = np.zeros(58)
            if step["source_id"] == "strip":
                vector[0] = 100.0
            return {"_vector": vector, "direct_quality": {"status": "pass", "feature_count": 58}, "feature_values": {name: 1.0 for name in feature_ids}}
        with (
            patch.object(measure, "_guide6_feature_vector", side_effect=lambda c, _: np.asarray(c["_vector"])),
            patch.object(measure, "_guide6_variances", return_value=(np.ones(58), np.ones(58))),
            patch.object(measure, "calibrate_direct_limits", return_value={"guarded_limit": 0.05, "statistic": "synthetic"}),
            patch.object(measure, "solve_box_constrained_least_squares", return_value=np.zeros(4)),
        ):
            result = measure.run_guide6_local_controllability_protocol(
                plan, measure_fn=fake_measure, feature_ids=feature_ids,
                source_isolation_fn=lambda _source: {"status": "pass", "source_verified_zero": True},
                cleanup_fn=lambda: {"status": "pass"},
            )
        self.assertEqual(result["candidates"], [])
        self.assertEqual(roles[-4:], ["strip_repeat_1", "strip_repeat_2", "strip_repeat_3", "ray_q_after"])
        base = plan["local_controllability_contract"]["base_command"]
        self.assertEqual(commands[-4:-1], [base, base, base])
        self.assertEqual(result["lc_branch"], "LC-C")

    def test_guide7_scale3072_plan_is_stability_first_and_bounded(self):
        plan = thermal.build_direct_plan(
            thermal.TD_C,
            variant=thermal.GUIDE7_F2_SCALE3072_STABILITY_VARIANT,
        )
        self.assertEqual(
            plan["guide_experiment_id"],
            thermal.GUIDE7_F2_SCALE3072_STABILITY_EXPERIMENT_ID,
        )
        self.assertEqual(plan["budgets"], {
            "ray_cap": 2, "strip_cap": 3, "formal_cap": 5,
            "physical_cr3_cap": 5, "ambient_cap": 0, "retry": 0,
        })
        self.assertEqual(
            [step["role"] for step in plan["captures"]],
            [
                "ray_q_before", "scale3072_repeat_1", "scale3072_repeat_2",
                "scale3072_repeat_3", "ray_q_after",
            ],
        )
        strip = [step for step in plan["captures"] if step["source_id"] == "strip"]
        self.assertTrue(all(step["command"] == {
            "cw": 3072, "ww": 0, "r": 0, "g": 3072, "b": 0,
        } for step in strip))
        self.assertTrue(plan["hard_locks"]["probes_until_stability_pass"])
        self.assertTrue(plan["hard_locks"]["solver_until_stability_pass"])
        self.assertFalse(plan["analysis_contract"]["cross_experiment_absolute_synthesis"])
        measure.validate_authorized_execution_plan(plan)

    def test_guide7_scale3072_fake_vertical_slice_and_analyzer(self):
        plan = thermal.build_direct_plan(
            thermal.TD_C,
            variant=thermal.GUIDE7_F2_SCALE3072_STABILITY_VARIANT,
        )
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "scale3072"
            self._execute_fake_protocol(plan, root)
            self.assertEqual(
                len((root / "captures.jsonl").read_text().splitlines()), 5,
            )
            evidence = json.loads(
                (root / "scale3072-stability-evidence.json").read_text()
            )
            self.assertEqual(evidence["capture_count"], 5)
            self.assertFalse((root / "local-controllability.json").exists())
            feature_ids = tuple(
                json.loads(thermal.POLICY_PATH.read_text())["feature_set"]["ids"]
            )
            report = analyze.analyze_thermal_run(root, feature_ids=feature_ids)
            self.assertEqual(report["branch"], "R-FAITHFUL")
            self.assertEqual(report["probes_executed"], 0)
            self.assertEqual(report["solver_candidates_executed"], 0)
            self.assertEqual(report["next"], "H120/S50")
            self.assertEqual(report["gamut_inference"], "prohibited")

    def test_guide7_scale2048_plan_remains_stability_first(self):
        plan = thermal.build_direct_plan(
            thermal.TD_C,
            variant=thermal.GUIDE7_F2_SCALE2048_STABILITY_VARIANT,
        )
        self.assertEqual(plan["budgets"]["formal_cap"], 5)
        self.assertEqual(plan["analysis_contract"]["max_code"], 2048)
        self.assertTrue(all(
            step["command"] == {"cw": 2048, "ww": 0, "r": 0, "g": 2048, "b": 0}
            for step in plan["captures"] if step["source_id"] == "strip"
        ))
        self.assertTrue(plan["hard_locks"]["probes_until_stability_pass"])
        self.assertTrue(plan["hard_locks"]["solver_until_stability_pass"])
        measure.validate_authorized_execution_plan(plan)

    def test_guide9_scale_age_plan_freezes_independent_cycles_without_pooling(self):
        plan = thermal.build_direct_plan(
            thermal.TD_C, variant=thermal.GUIDE9_H120_S100_SCALE_AGE_VARIANT,
        )
        self.assertEqual(plan["guide_experiment_id"], thermal.GUIDE9_H120_S100_SCALE_AGE_EXPERIMENT_ID)
        self.assertEqual(plan["budgets"]["formal_cap"], 10)
        self.assertEqual(plan["analysis_contract"]["cycle_order"], [4095, 2048, 2048, 4095])
        self.assertTrue(plan["analysis_contract"]["no_pool_fast_long"])
        self.assertEqual(
            [step["role"] for step in plan["captures"]],
            ["ray_q_before", "scale4095_cycle1_fast120", "scale4095_cycle1_long600",
             "scale2048_cycle2_fast120", "scale2048_cycle2_long600",
             "scale2048_cycle3_fast120", "scale2048_cycle3_long600",
             "scale4095_cycle4_fast120", "scale4095_cycle4_long600", "ray_q_after"],
        )
        measure.validate_authorized_execution_plan(plan)

    def test_guide9_analyzer_does_not_use_legacy_td_c_grouping(self):
        plan = thermal.build_direct_plan(
            thermal.TD_C, variant=thermal.GUIDE9_H120_S100_SCALE_AGE_VARIANT,
        )
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "guide9"
            self._execute_fake_protocol(plan, root)
            feature_ids = tuple(
                json.loads(thermal.POLICY_PATH.read_text())["feature_set"]["ids"]
            )
            report = analyze.analyze_thermal_run(root, feature_ids=feature_ids)
            self.assertEqual(report["schema"], analyze.GUIDE9_ANALYSIS_SCHEMA)
            self.assertEqual(report["next"], "H120/S50")

    def _run_fake_guide6_protocol(
        self, residual_scale=1.0, *, irreducible=0.0, abort_role=None,
        cleanup_sink=None,
    ):
        import numpy as np

        plan = thermal.build_direct_plan(
            thermal.TD_C,
            variant=thermal.GUIDE6_DIRECT_TARGET_LOCAL_H120_S100_VARIANT,
        )
        feature_ids = tuple(f"f{index}" for index in range(58))
        roles = []
        isolation = []
        cleanup = [] if cleanup_sink is None else cleanup_sink

        def fake_vector(capture, _feature_ids):
            return np.asarray(capture["_vector"], dtype=float)

        def fake_measure(step):
            roles.append(step["role"])
            if step["role"] == abort_role:
                raise RuntimeError("synthetic abort")
            vector = np.zeros(58)
            if step["source_id"] == "strip":
                command = step["command"]
                vector[:4] = residual_scale * np.asarray([
                    1.0 + (command["cw"] - 518) / 256.0,
                    1.0 - command["ww"] / 256.0,
                    1.0 - command["r"] / 256.0,
                    1.0 - command["b"] / 256.0,
                ])
                vector[4] = irreducible
            return {
                "_vector": vector,
                "direct_quality": {"status": "pass", "feature_count": 58},
                "feature_values": {name: 1.0 for name in feature_ids},
            }

        with (
            patch.object(measure, "_guide6_feature_vector", side_effect=fake_vector),
            patch.object(measure, "_guide6_variances", return_value=(np.ones(58), np.ones(58))),
            patch.object(measure, "calibrate_direct_limits", return_value={
                "guarded_limit": 0.05, "statistic": "synthetic",
            }),
        ):
            result = measure.run_guide6_local_controllability_protocol(
                plan,
                measure_fn=fake_measure,
                feature_ids=feature_ids,
                source_isolation_fn=lambda source: (
                    isolation.append(source)
                    or {"status": "pass", "source_verified_zero": True}
                ),
                cleanup_fn=lambda: cleanup.append("off") or {"status": "pass"},
            )
        return result, roles, isolation, cleanup

    def test_guide6_fake_backend_exact_sequence_reserves_confirmations_and_passes(self):
        result, roles, isolation, cleanup = self._run_fake_guide6_protocol()
        self.assertEqual(roles[:8], [
            "ray_q_before", "strip_base", "strip_probe_cw", "strip_probe_ww",
            "strip_base_anchor_after_probe_2", "strip_probe_r", "strip_probe_b",
            "strip_base_anchor_after_probe_4",
        ])
        self.assertEqual(roles[-4:], [
            "strip_confirmation_1", "strip_confirmation_2", "strip_confirmation_3",
            "ray_q_after",
        ])
        self.assertEqual(result["lc_branch"], "LC-A")
        self.assertGreaterEqual(len(result["candidates"]), 1)
        self.assertLessEqual(len(result["candidates"]), 4)
        self.assertEqual(len(result["confirmations"]), 3)
        self.assertEqual(result["counts"]["ray"], 2)
        self.assertLessEqual(result["counts"]["strip"], 14)
        self.assertLessEqual(result["counts"]["total"], 16)
        self.assertEqual(result["counts"]["ambient"], 0)
        self.assertEqual(result["counts"]["in_root_retry"], 0)
        self.assertEqual(result["model_rebase_extra_probe_count"], 0)
        self.assertFalse(result["terminal_multi_start_solver_unresolved"])
        self.assertEqual(result["gamut_inference"], "prohibited")
        self.assertEqual(len(isolation), result["counts"]["total"])
        self.assertEqual(cleanup, ["off"])

    def test_guide6_fake_backend_improvement_stays_within_candidate_budget(self):
        result, roles, _isolation, cleanup = self._run_fake_guide6_protocol(
            4.0, irreducible=0.5,
        )
        self.assertEqual(result["lc_branch"], "LC-B")
        self.assertGreaterEqual(len(result["candidates"]), 1)
        self.assertLessEqual(len(result["candidates"]), 4)
        self.assertEqual(result["confirmations"], [])
        self.assertLessEqual(result["counts"]["strip"], 11)
        self.assertFalse(result["terminal_multi_start_solver_unresolved"])
        self.assertEqual(roles[-1], "ray_q_after")
        self.assertEqual(cleanup, ["off"])

    def test_guide6_fake_backend_abort_always_cleans_up(self):
        cleanup = []
        with self.assertRaisesRegex(RuntimeError, "synthetic abort"):
            self._run_fake_guide6_protocol(
                abort_role="strip_probe_ww", cleanup_sink=cleanup,
            )
        self.assertEqual(cleanup, ["off"])

    def test_guide6_execute_plan_routes_live_scheduler_to_adaptive_owner_and_cleanup(self):
        plan = thermal.build_direct_plan(
            thermal.TD_C,
            variant=thermal.GUIDE6_DIRECT_TARGET_LOCAL_H120_S100_VARIANT,
        )
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "guide6"
            path = self._execute_fake_protocol(plan, root)
            self.assertEqual(path, root)
            evidence = json.loads((root / "local-controllability.json").read_text())
            self.assertEqual(evidence["counts"], {
                "ray": 2, "strip": 7, "total": 9,
                "ambient": 0, "in_root_retry": 0,
            })
            self.assertEqual(
                [step["role"] for step in evidence["measured_steps"]],
                [
                    "ray_q_before", "strip_base", "strip_probe_cw", "strip_probe_ww",
                    "strip_base_anchor_after_probe_2", "strip_probe_r", "strip_probe_b",
                    "strip_base_anchor_after_probe_4", "ray_q_after",
                ],
            )
            runtime_plan = json.loads((root / "adaptive-execution-plan.json").read_text())
            self.assertEqual(runtime_plan["budgets"]["formal_cap"], 9)
            self.assertEqual(len((root / "captures.jsonl").read_text().splitlines()), 9)
            self.assertEqual(len((root / "physical-returns.jsonl").read_text().splitlines()), 9)
            self.assertEqual(json.loads((root / "all-off-python.json").read_text())["status"], "pass")
            self.assertEqual(json.loads((root / "run.json").read_text())["cleanup"], "pass")
            feature_ids = tuple(json.loads(thermal.POLICY_PATH.read_text())["feature_set"]["ids"])
            report = analyze.analyze_thermal_run(root, feature_ids=feature_ids)
            self.assertEqual(report["guide6_branch"], "LC-D")
            self.assertFalse(report["terminal_multi_start_solver_unresolved"])
            self.assertFalse((root / "wrapper-result.json").exists())

    def test_guide6_analyzer_frozen_lc_table_never_claims_gamut_or_terminal(self):
        import numpy as np

        fixed = [
            "ray_q_before", "strip_base", "strip_probe_cw", "strip_probe_ww",
            "strip_base_anchor_after_probe_2", "strip_probe_r", "strip_probe_b",
            "strip_base_anchor_after_probe_4", "ray_q_after",
        ]

        def rows(*, candidate=None, confirmations=False, repeats=False):
            values = {role: [0.0, 0.0] for role in fixed}
            values["strip_base"] = [1.0, 0.0]
            output = [
                {"plan_step": {"role": role}, "feature_values": {
                    "f0": vector[0], "f1": vector[1],
                }}
                for role, vector in values.items()
            ]
            if candidate is not None:
                output.append({
                    "plan_step": {"role": "strip_solver_candidate_1"},
                    "feature_values": {"f0": candidate[0], "f1": candidate[1]},
                })
            if confirmations:
                output.extend({
                    "plan_step": {"role": f"strip_confirmation_{index}"},
                    "feature_values": {"f0": 0.0, "f1": 0.0},
                } for index in range(1, 4))
            if repeats:
                output.extend({
                    "plan_step": {"role": f"strip_repeat_{index}"},
                    "feature_values": {"f0": 0.5, "f1": 0.0},
                } for index in range(1, 4))
            return output

        evidence = {
            "schema": "guide6_h120_s100_direct_local_controllability_evidence_v1",
            "gamut_inference": "prohibited",
            "terminal_multi_start_solver_unresolved": False,
            "jacobian": {"effective_rank": 4},
            "measured_steps": [{}] * 9,
        }

        def compatibility(_left, _right, *, source, **_kwargs):
            return {"decision": "pass", "source": source}

        with (
            patch.object(analyze, "_unit", side_effect=lambda value, ids: np.asarray([
                value[ids[0]], value[ids[1]],
            ])),
            patch.object(analyze, "_same_state_variance", return_value=np.ones(2)),
            patch.object(analyze, "calibrate_direct_limits", return_value={
                "guarded_limit": 0.1, "statistic": "synthetic",
            }),
            patch.object(analyze, "direct_whitened_norm", side_effect=lambda value, variance: float(np.linalg.norm(value))),
            patch.object(analyze, "frozen_same_state_compatibility_diagnostic", side_effect=compatibility),
        ):
            cases = (
                ("LC-A", rows(candidate=[0.0, 0.0], confirmations=True), evidence),
                ("LC-B", rows(candidate=[0.5, 0.0]), evidence),
                ("LC-C", rows(), evidence),
                ("LC-D", rows(), {**evidence, "jacobian": {"effective_rank": 0}}),
            )
            for expected, captures, artifact in cases:
                with self.subTest(expected=expected):
                    report = analyze.analyze_guide6_local_controllability(
                        captures, feature_ids=("f0", "f1"),
                        protocol_evidence=artifact,
                    )
                    self.assertEqual(report["guide6_branch"], expected)
                    self.assertEqual(report["gamut_inference"], "prohibited")
                    self.assertFalse(report["terminal_multi_start_solver_unresolved"])
                    self.assertNotEqual(report["classification"], "multi_start_solver_unresolved")
            continuation = analyze.analyze_guide6_local_controllability(
                rows(candidate=[0.5, 0.0]), feature_ids=("f0", "f1"),
                protocol_evidence={**evidence, "continuation_generation": 1},
            )
            self.assertEqual(continuation["guide6_branch"], "LC-B")
            self.assertEqual(
                continuation["next"],
                "ADVISOR_GATE_REQUIRED_after_centered_continuation",
            )
            f2 = analyze.analyze_guide6_local_controllability(
                rows(candidate=[0.5, 0.0], repeats=True), feature_ids=("f0", "f1"),
                protocol_evidence={
                    **evidence, "guide7_f2": True, "active_face": "cw",
                    "measured_steps": [
                        {"role": role} for role in (
                            "ray_q_before", "strip_base", "strip_probe_cw",
                            "strip_probe_ww", "strip_probe_r", "strip_probe_b",
                            "strip_base_anchor_after_probe_2",
                            "strip_base_anchor_after_probe_4", "ray_q_after",
                        )
                    ],
                },
            )
            self.assertEqual(f2["classification"], "H120_S100_stable_nonfaithful_after_two_fullscale_faces")
            self.assertTrue(f2["best_nonfaithful_repeat_stable"])
            self.assertEqual(f2["next"], "GUIDE7_H120_S100_MAX_CODE_3072_DIAGNOSTIC")

    def test_guide6_target_local_analyzer_uses_ray_bracket_and_local_contrast(self):
        feature_ids = tuple(json.loads(thermal.POLICY_PATH.read_text())["feature_set"]["ids"])
        vector = {feature_id: 1.0 for feature_id in feature_ids}
        strip_vector = dict(vector)
        strip_vector[feature_ids[0]] += 1e-6
        strip_zero = {
            "requested_payload": {key: 0 for key in ("red", "green", "blue", "warm_white", "cold_white")},
            "device_snapshot": {key: 0 for key in ("red", "green", "blue", "warm_white", "cold_white")},
        }
        captures = [
            {"plan_step": {"role": "ray_q_before", "source_id": "ray"},
             "feature_values": dict(vector), "strip_zero_before_capture": strip_zero},
            {"plan_step": {"role": "ray_q_after", "source_id": "ray"},
             "feature_values": dict(vector), "strip_zero_before_capture": strip_zero},
            {"plan_step": {"role": "strip_candidate", "source_id": "strip"},
             "feature_values": strip_vector,
             "ray_zero_before_capture": {"response": {"data": {"intensity": 0}}}},
        ]
        report = analyze.analyze_td_c_direct_target_local(
            captures, feature_ids=feature_ids,
        )
        self.assertEqual(report["guide6_branch"], "S-PASS")
        self.assertTrue(report["measurement_valid"])
        self.assertTrue(report["faithful"])
        self.assertFalse(report["cross_experiment_absolute_synthesis"])
        self.assertFalse(report["steady_claim"])

    def test_guide6_seed_negative_rejects_missing_ray_zero_evidence(self):
        retained = Path(
            "/Volumes/4T/temp/rgbww-optimizer/guide6-direct-target-local-h120-s100-20260813"
        )
        source_roots = (
            retained / "20260814-075000-qualified-strip-1over1600-reference-repeat",
            retained / "20260814-080000-qualified-strip-1over1600-solver-repeat",
        )
        if not all((root / "analysis.json").is_file() for root in source_roots):
            self.skipTest("retained GUIDE6 seed roots are unavailable")
        legacy_before = tuple((root / "analysis.json").read_bytes() for root in source_roots)
        with tempfile.TemporaryDirectory() as temporary:
            temporary_path = Path(temporary)
            roots = (temporary_path / "root1", temporary_path / "root2")
            for source, root in zip(source_roots, roots):
                root.mkdir()
                shutil.copy2(source / "analysis.json", root / "analysis.json")
                shutil.copy2(source / "captures.jsonl", root / "captures.jsonl")
            output = temporary_path / "analysis-v2-guide6-seed-negative-derived.json"
            self.assertEqual(analyze.main([
                str(roots[0]),
                "--guide6-seed-negative-root2", str(roots[1]),
                "--guide6-seed-negative-output", str(output),
            ]), 0)
            report = json.loads(output.read_text())
            self.assertEqual(report["classification"], "historical_cross_source_contaminated")
            self.assertFalse(report["scientific_input_allowed"])
            self.assertFalse(report["legacy_conclusion_allowed"])
            self.assertEqual(report["solver_attempt_count"], 0)
            self.assertEqual(report["distinct_strip_candidate_count"], 1)
            self.assertEqual(report["probe_count"], 0)
            self.assertEqual(report["solver_generated_candidate_count"], 0)
            self.assertEqual(report["exact_command_hash"], analyze.GUIDE6_SEED_COMMAND_HASH)
            self.assertEqual(
                [item["ray_zero_before_capture"] for item in report["roots"]],
                ["missing_or_nonzero", "missing_or_nonzero"],
            )
            output_before = output.read_bytes()
            with self.assertRaises(FileExistsError):
                analyze.main([
                    str(roots[0]),
                    "--guide6-seed-negative-root2", str(roots[1]),
                    "--guide6-seed-negative-output", str(output),
                ])
            self.assertEqual(output.read_bytes(), output_before)
            self.assertEqual((roots[0] / "analysis.json").read_bytes(), legacy_before[0])
            self.assertEqual((roots[1] / "analysis.json").read_bytes(), legacy_before[1])

    def test_guide6_local_analyzer_rejects_strip_without_ray_zero(self):
        feature_ids = tuple(json.loads(thermal.POLICY_PATH.read_text())["feature_set"]["ids"])
        vector = {feature_id: 1.0 for feature_id in feature_ids}
        protocol = {
            "schema": "guide6_h120_s100_direct_local_controllability_evidence_v1",
            "gamut_inference": "prohibited",
            "terminal_multi_start_solver_unresolved": False,
            "jacobian": {"effective_rank": 1},
            "measured_steps": [{}] * 9,
        }
        roles = (
            "ray_q_before", "ray_q_after", "strip_base", "strip_probe_cw",
            "strip_probe_ww", "strip_probe_r", "strip_probe_b",
            "strip_base_anchor_after_probe_2", "strip_base_anchor_after_probe_4",
        )
        rows = []
        for role in roles:
            source = "ray" if role.startswith("ray_") else "strip"
            capture = {
                "feature_values": vector,
                "strip_zero_before_capture": {
                    "requested_payload": {key: 0 for key in ("red", "green", "blue", "warm_white", "cold_white")},
                    "device_snapshot": {key: 0 for key in ("red", "green", "blue", "warm_white", "cold_white")},
                },
            } if source == "ray" else {"feature_values": vector}
            rows.append({"plan_step": {"role": role, "source_id": source}, "capture": capture})
        with self.assertRaisesRegex(ValueError, "lacks verified Ray-zero evidence"):
            analyze.analyze_guide6_local_controllability(
                rows, feature_ids=feature_ids, protocol_evidence=protocol,
            )

    def _run_fake_guide8(self, ladder_statuses, *, evaluator=True):
        spec = thermal.build_direct_plan(
            thermal.TD_C, variant=thermal.GUIDE8_RAY_EMISSION_EXPOSURE_VARIANT,
        )
        feature_ids = tuple(json.loads(thermal.POLICY_PATH.read_text())["feature_set"]["ids"])
        measured = []
        cleanup = []

        def capture(step):
            measured.append(step)
            phase = step["diagnostic_phase"]
            status = (
                "pass" if phase == "control" else
                "near_noise_only" if phase == "dark" else
                ladder_statuses.get(step["nominal_shutter"], "near_noise_only")
            )
            return {
                "direct_quality": {"status": status, "feature_count": 58},
                "feature_values": {feature_id: 1.0 for feature_id in feature_ids},
                "recorded_exposure": {"seconds": float(parse_nominal_exposure(step["nominal_shutter"]))},
            }
        result = measure.run_guide8_emission_exposure_protocol(
            spec, measure_fn=capture, feature_ids=feature_ids,
            pair_evaluator_fn=lambda _fast, _slow: {"status": "pass" if evaluator else "fail"},
            cleanup_fn=lambda: cleanup.append(True) or {"status": "pass"},
        )
        return result, measured, cleanup

    def test_guide8_spec_freezes_control_dark_ladder_and_caps(self):
        spec = thermal.build_direct_plan(
            thermal.TD_C, variant=thermal.GUIDE8_RAY_EMISSION_EXPOSURE_VARIANT,
        )
        self.assertEqual(spec["guide_experiment_id"], thermal.GUIDE8_RAY_EMISSION_EXPOSURE_EXPERIMENT_ID)
        self.assertEqual(spec["budgets"]["formal_cap"], 0)
        self.assertEqual(spec["budgets"]["physical_cr3_cap"], 16)
        self.assertEqual(spec["captures"][0]["nominal_shutter"], "1/2500")
        self.assertEqual(spec["captures"][1]["nominal_shutter"], "1/250")
        self.assertEqual(tuple(step["nominal_shutter"] for step in spec["captures"][2:]), thermal.GUIDE8_RAY_EMISSION_EXPOSURE_LADDER)
        self.assertEqual([item["dwell_s"] for item in spec["captures"][0]["warm_precondition_sequence"]], [120, 120])
        self.assertEqual([item["state_id"] for item in spec["captures"][2]["warm_precondition_sequence"]], ["D", "A", "Q"])
        self.assertTrue(all(not step["warm_precondition_sequence"] for step in spec["captures"][3:]))

    def test_guide8_control_and_dark_stop_before_ladder_and_cleanup(self):
        spec = thermal.build_direct_plan(thermal.TD_C, variant=thermal.GUIDE8_RAY_EMISSION_EXPOSURE_VARIANT)
        feature_ids = tuple(json.loads(thermal.POLICY_PATH.read_text())["feature_set"]["ids"])
        for failed_phase, expected_branch, expected_count in (("control", "E-A", 1), ("dark", "E-B", 2)):
            seen = []
            def capture(step, failed_phase=failed_phase):
                seen.append(step)
                status = "clipping" if step["diagnostic_phase"] == failed_phase else ("near_noise_only" if step["diagnostic_phase"] == "dark" else "pass")
                return {"direct_quality": {"status": status, "feature_count": 58},
                        "feature_values": {feature_id: 1.0 for feature_id in feature_ids},
                        "recorded_exposure": {"seconds": float(parse_nominal_exposure(step["nominal_shutter"]))}}
            cleaned = []
            result = measure.run_guide8_emission_exposure_protocol(
                spec, measure_fn=capture, feature_ids=feature_ids,
                pair_evaluator_fn=lambda *_: True,
                cleanup_fn=lambda: cleaned.append(True) or {"status": "pass"},
            )
            self.assertEqual(result["branch"], expected_branch)
            self.assertEqual(len(seen), expected_count)
            self.assertEqual(cleaned, [True])

    def test_guide8_near_noise_continues_and_valid_pair_stops_early(self):
        result, measured, cleanup = self._run_fake_guide8({
            "1/5000": "near_noise_only", "1/4000": "pass", "1/3200": "pass",
        })
        self.assertEqual(result["branch"], "E-D")
        self.assertEqual(result["selected_nominal_shutter"], "1/4000")
        self.assertEqual(result["guard_nominal_shutter"], "1/3200")
        self.assertEqual(len(measured), 5)
        self.assertEqual(cleanup, [True])

    def test_guide8_ratio_above_1_25_cannot_form_pair(self):
        evaluated = []
        spec = thermal.build_direct_plan(thermal.TD_C, variant=thermal.GUIDE8_RAY_EMISSION_EXPOSURE_VARIANT)
        feature_ids = tuple(json.loads(thermal.POLICY_PATH.read_text())["feature_set"]["ids"])
        valid = {"1/3200", "1/2500", "1/2000"}
        def capture(step):
            status = "pass" if step["diagnostic_phase"] == "control" or step["nominal_shutter"] in valid else "near_noise_only"
            return {"direct_quality": {"status": status, "feature_count": 58}, "feature_values": {feature_id: 1.0 for feature_id in feature_ids}, "recorded_exposure": {"seconds": float(parse_nominal_exposure(step["nominal_shutter"]))}}
        result = measure.run_guide8_emission_exposure_protocol(
            spec, measure_fn=capture, feature_ids=feature_ids,
            pair_evaluator_fn=lambda a, b: evaluated.append((a, b)) or {"status": "pass"},
        )
        self.assertEqual(result["selected_nominal_shutter"], "1/2500")
        self.assertEqual(len(evaluated), 1)

    def test_guide8_clipping_nonfinite_and_shape_failure_stop(self):
        result, measured, _ = self._run_fake_guide8({"1/5000": "near_noise_only", "1/4000": "clipping"})
        self.assertEqual(result["branch"], "E-E")
        self.assertEqual(len(measured), 4)
        for status in ("clipping", "nonfinite"):
            cleaned = []
            spec = thermal.build_direct_plan(thermal.TD_C, variant=thermal.GUIDE8_RAY_EMISSION_EXPOSURE_VARIANT)
            feature_ids = tuple(json.loads(thermal.POLICY_PATH.read_text())["feature_set"]["ids"])
            def capture(step, status=status):
                if step["diagnostic_phase"] == "control":
                    current = "pass"
                elif step["diagnostic_phase"] == "dark":
                    current = "near_noise_only"
                else:
                    current = status
                return {
                    "direct_quality": {"status": current, "feature_count": 58},
                    "feature_values": {feature_id: 1.0 for feature_id in feature_ids},
                    "recorded_exposure": {"seconds": float(parse_nominal_exposure(step["nominal_shutter"]))},
                }
            with self.assertRaisesRegex(RuntimeError, "non-scientific quality/evidence failure"):
                measure.run_guide8_emission_exposure_protocol(
                    spec, measure_fn=capture, feature_ids=feature_ids,
                    pair_evaluator_fn=lambda *_: True,
                    cleanup_fn=lambda: cleaned.append(True) or {"status": "pass"},
                )
            self.assertEqual(cleaned, [True])
        result, measured, _ = self._run_fake_guide8({"1/5000": "pass", "1/4000": "pass"}, evaluator=False)
        self.assertEqual(result["branch"], "E-G")
        self.assertEqual(len(measured), 4)

    def test_guide8_near_noise_to_cap_is_e_f(self):
        result, measured, cleanup = self._run_fake_guide8({})
        self.assertEqual(result["branch"], "E-F")
        self.assertEqual(len(measured), 16)
        self.assertEqual(cleanup, [True])

    def test_guide6_strip_exposure_plan_and_early_stop(self):
        plan = thermal.build_direct_plan(
            thermal.TD_C,
            variant=thermal.GUIDE6_STRIP_EXPOSURE_QUALIFICATION_VARIANT,
        )
        self.assertEqual(
            [step["nominal_shutter"] for step in plan["captures"]],
            list(thermal.GUIDE6_STRIP_EXPOSURE_QUALIFICATION_LADDER),
        )
        self.assertEqual(plan["budgets"]["formal_cap"], 0)
        self.assertEqual(plan["budgets"]["physical_cr3_cap"], 9)
        self.assertFalse(plan["solver_probe_allowed"])
        feature_ids = tuple(json.loads(thermal.POLICY_PATH.read_text())["feature_set"]["ids"])
        seen = []
        def capture(step):
            seen.append(step["nominal_shutter"])
            status = "pass" if step["nominal_shutter"] in {"1/1000", "1/800"} else "near_noise_only"
            return {
                "direct_quality": {"status": status, "feature_count": 58},
                "feature_values": {feature_id: 1.0 for feature_id in feature_ids},
                "recorded_exposure": {"seconds": float(parse_nominal_exposure(step["nominal_shutter"]))},
                "ray_zero_before_capture": {"response": {"data": {"intensity": 0}}},
            }
        result = measure.run_guide6_strip_exposure_qualification_protocol(
            plan, measure_fn=capture, feature_ids=feature_ids,
            pair_evaluator_fn=lambda *_: {"status": "pass"},
        )
        self.assertEqual(result["classification"], "strip_exposure_window_qualified")
        self.assertEqual(result["selected_nominal_shutter"], "1/1000")
        self.assertEqual(result["guard_nominal_shutter"], "1/800")
        self.assertEqual(seen, ["1/1600", "1/1250", "1/1000", "1/800"])

    def test_guide6_strip_exposure_stops_on_non_near_noise_and_caps_to_advisor(self):
        plan = thermal.build_direct_plan(
            thermal.TD_C,
            variant=thermal.GUIDE6_STRIP_EXPOSURE_QUALIFICATION_VARIANT,
        )
        feature_ids = tuple(json.loads(thermal.POLICY_PATH.read_text())["feature_set"]["ids"])
        def capture_with(status):
            return lambda step: {
                "direct_quality": {"status": status, "feature_count": 0, "failures": [status]},
                "recorded_exposure": {"seconds": float(parse_nominal_exposure(step["nominal_shutter"]))},
                "ray_zero_before_capture": {"response": {"data": {"intensity": 0}}},
            }
        with self.assertRaisesRegex(RuntimeError, "quality/evidence failure"):
            measure.run_guide6_strip_exposure_qualification_protocol(
                plan, measure_fn=capture_with("clipping"), feature_ids=feature_ids,
                pair_evaluator_fn=lambda *_: True,
            )
        result = measure.run_guide6_strip_exposure_qualification_protocol(
            plan, measure_fn=capture_with("near_noise_only"), feature_ids=feature_ids,
            pair_evaluator_fn=lambda *_: True,
        )
        self.assertEqual(result["classification"], "no_legal_strip_exposure_window")
        self.assertEqual(result["next_gate"], "ADVISOR_GATE_REQUIRED")
        self.assertEqual(result["physical_capture_count"], 9)

    def test_guide6_strip_exposure_execute_plan_retains_ray_zero_and_validates(self):
        plan = thermal.build_direct_plan(
            thermal.TD_C,
            variant=thermal.GUIDE6_STRIP_EXPOSURE_QUALIFICATION_VARIANT,
        )
        with tempfile.TemporaryDirectory() as temporary, patch.object(
            analyze, "evaluate_guide8_pair_captures", return_value={"status": "pass"},
        ):
            root = Path(temporary) / "strip-exposure"
            self._execute_fake_protocol(
                plan, root,
                diagnostic_status_fn=lambda step: (
                    "pass" if step["nominal_shutter"] in {"1/1000", "1/800"}
                    else "near_noise_only"
                ),
            )
            rows = [json.loads(line) for line in (root / "captures.jsonl").read_text().splitlines()]
            quality = json.loads((root / "quality.json").read_text())
        self.assertEqual(len(rows), 4)
        self.assertTrue(all(
            row["capture"]["ray_zero_before_capture"]["response"]["data"]["intensity"] == 0
            for row in rows
        ))
        self.assertEqual(quality["classification"], "strip_exposure_window_qualified")

    def test_guide8_execute_plan_keeps_q_on_until_final_cleanup(self):
        plan = thermal.build_direct_plan(
            thermal.TD_C, variant=thermal.GUIDE8_RAY_EMISSION_EXPOSURE_VARIANT,
        )
        applied = []
        with tempfile.TemporaryDirectory() as temporary, patch.object(
            analyze, "evaluate_guide8_pair_captures", return_value={"status": "pass"},
        ):
            root = Path(temporary) / "guide8"
            self._execute_fake_protocol(
                plan, root, applied_steps=applied,
                diagnostic_status_fn=lambda step: (
                    "near_noise_only" if step["diagnostic_phase"] == "dark" else "pass"
                ),
            )
            run = json.loads((root / "run.json").read_text())
            evidence = json.loads((root / "guide8-emission-exposure.json").read_text())
        self.assertEqual(run["cleanup"], "pass")
        self.assertEqual(evidence["branch"], "E-C")
        q_index = next(index for index, step in enumerate(applied) if step["state_id"] == "Q")
        self.assertTrue(all(float(step["command"]["intensity_percent"]) > 0 for step in applied[q_index:]))
        self.assertEqual([step["state_id"] for step in applied[:3]], ["D", "A", "C"])
        self.assertEqual([step["state_id"] for step in applied[3:6]], ["D", "A", "Q"])

    def test_guide8_execute_plan_validates_one_frame_e_a_prefix(self):
        plan = thermal.build_direct_plan(
            thermal.TD_C, variant=thermal.GUIDE8_RAY_EMISSION_EXPOSURE_VARIANT,
        )
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "guide8-e-a"
            self._execute_fake_protocol(
                plan, root,
                diagnostic_status_fn=lambda step: "clipping" if step["diagnostic_phase"] == "control" else "near_noise_only",
            )
            evidence = json.loads((root / "guide8-emission-exposure.json").read_text())
            quality = json.loads((root / "quality.json").read_text())
        self.assertEqual(evidence["branch"], "E-A")
        self.assertEqual(evidence["physical_capture_count"], 1)
        self.assertEqual(quality["capture_count"], 1)

    def test_guide8_policy_is_hashed_and_overwrite_fails_closed(self):
        report = {
            "schema": analyze.GUIDE8_ANALYSIS_SCHEMA, "branch": "E-D",
            "selected_nominal_shutter": "1/4000", "guard_nominal_shutter": "1/3200",
            "selected_recorded_exposure_seconds": 1 / 4000,
            "guard_recorded_exposure_seconds": 1 / 3200,
            "observer_hash": "a" * 64, "feature_hash": "b" * 64,
            "quality_policy_hash": "c" * 64, "invariance_evaluator_hash": "d" * 64,
            "accepted_boundary_artifact_hash": "e" * 64,
            "repeatability_evidence_hash": "f" * 64,
            "derived_from_root": "/fake/guide8", "historical_1over5000_pooling": False,
            "pooling_semantics": "old_and_new_target_centers_must_not_be_pooled",
        }
        with tempfile.TemporaryDirectory() as temporary, patch.object(
            analyze, "analyze_guide8_emission_exposure", return_value=report,
        ):
            root = Path(temporary)
            analysis_path = root / "analysis-derived.json"
            policy_path = root / "policy-v2.json"
            written_analysis, written_policy = analyze.write_guide8_analysis_and_policy(
                root, analysis_output=analysis_path, policy_output=policy_path,
            )
            policy = json.loads(policy_path.read_text())
            self.assertEqual(written_analysis, analysis_path.resolve())
            self.assertEqual(written_policy, policy_path.resolve())
            self.assertEqual(policy["derived_analysis_sha256"], hashlib.sha256(analysis_path.read_bytes()).hexdigest())
            self.assertEqual(policy["repeatability_evidence_hash"], "f" * 64)
            before = (analysis_path.read_bytes(), policy_path.read_bytes())
            with self.assertRaises(FileExistsError):
                analyze.write_guide8_analysis_and_policy(
                    root, analysis_output=analysis_path, policy_output=policy_path,
                )
            self.assertEqual((analysis_path.read_bytes(), policy_path.read_bytes()), before)

    def test_guide8_repeatability_identity_matches_accepted_boundary(self):
        reports = analyze._guide8_repeatability_reports()
        boundary = json.loads(thermal.GUIDE8_P1_ACCEPTED_BOUNDARY_ARTIFACT.read_text())
        from camera_based_rgbww_optimizer.measurement import raw_response_candidate
        self.assertEqual(
            raw_response_candidate._reports_sha256(reports),
            boundary["repeatability_input_sha256"],
        )

    def test_guide8_pair_evaluator_uses_exact_58_features_and_identity_model(self):
        from camera_based_rgbww_optimizer.optimization import analyze_raw_observer_validation
        reports = analyze_raw_observer_validation.load_validation_reports(
            thermal.GUIDE8_P1_REPEATABILITY_RUN
        )
        pair = {}
        for report in reports:
            context = report.get("analysis_context", {})
            if (
                context.get("source") == "ray"
                and context.get("purpose") == "linearity_bracket"
                and context.get("exposure_factor") in {1.0, 1.5}
            ):
                pair.setdefault(context["exposure_factor"], report)
        result = analyze.evaluate_guide8_pair_captures(
            {"patch_statistics_report": pair[1.0]},
            {"patch_statistics_report": pair[1.5]},
        )
        sigma = result["evaluation"]["summary"]["shape_residual_repeatability_sigma_non_reference"]
        self.assertEqual(result["identity_response"], {"a": 0.0, "b": 0.0})
        self.assertEqual(sigma["count"], 58)
        self.assertLessEqual(sigma["max"], 3.0)

    def test_guide9_h300_s100_batch1_is_bounded_and_source_isolated(self):
        plan = thermal.build_direct_plan(
            thermal.TD_C, variant=thermal.GUIDE9_H300_S100_BATCH1_VARIANT,
        )
        self.assertEqual(plan["guide_experiment_id"], thermal.GUIDE9_H300_S100_BATCH1_EXPERIMENT_ID)
        self.assertEqual(len(plan["captures"]), 6)
        self.assertEqual(plan["budgets"]["physical_cr3_cap"], 6)
        self.assertEqual(plan["target"], {"hue": 300, "sat": 100, "intensity": 100})
        self.assertEqual(plan["frozen_shutters"], {"ray-h300-s100": "1/2500", "strip-h300-s100": "1/125"})
        self.assertEqual(plan["captures"][1]["command"], {"cw": 406, "ww": 0, "r": 4095, "g": 0, "b": 1541})
        self.assertTrue(all(step["strip_zero_required"] for step in plan["captures"] if step["source_id"] == "ray"))
        self.assertTrue(all(step["ray_zero_required"] for step in plan["captures"] if step["source_id"] == "strip"))

    def test_guide9_h300_s50_batch1_uses_frozen_p2_faces_and_source_isolation(self):
        plan = thermal.build_direct_plan(
            thermal.TD_C, variant=thermal.GUIDE9_H300_S50_BATCH1_VARIANT,
        )
        self.assertEqual(plan["guide_experiment_id"], thermal.GUIDE9_H300_S50_BATCH1_EXPERIMENT_ID)
        self.assertEqual(plan["target"], {"hue": 300, "sat": 50, "intensity": 100})
        self.assertEqual(plan["budgets"]["physical_cr3_cap"], 6)
        self.assertEqual(
            plan["frozen_shutters"],
            {"ray-h300-s50": "1/4000", "strip-h300-s50": "1/400"},
        )
        self.assertEqual(
            [step["role"] for step in plan["captures"][1:5]],
            ["p2_best_ww", "p2_r_face", "p2_cw_face", "p2_b_face"],
        )
        self.assertEqual(
            plan["captures"][1]["command"],
            {"cw": 192, "ww": 4095, "r": 2495, "g": 0, "b": 2559},
        )
        self.assertTrue(all(
            step["strip_zero_required"] for step in plan["captures"]
            if step["source_id"] == "ray"
        ))
        self.assertTrue(all(
            step["ray_zero_required"] for step in plan["captures"]
            if step["source_id"] == "strip"
        ))
        measure.validate_authorized_execution_plan(plan)
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "guide9-h300-s50"
            self._execute_fake_protocol(plan, root)
            feature_ids = tuple(
                json.loads(thermal.POLICY_PATH.read_text())["feature_set"]["ids"]
            )
            report = analyze.analyze_thermal_run(root, feature_ids=feature_ids)
            self.assertEqual(report["schema"], "guide9_h300_s50_batch1_analysis_v1")
            self.assertEqual(report["classification"], "H300_S50_batch1_candidate_selected")
            self.assertEqual(report["next"], "GUIDE9_H300_S50_BEST_REPEAT_V1")

    def test_guide9_h300_s50_best_repeat_is_bounded_and_analyzable(self):
        plan = thermal.build_direct_plan(
            thermal.TD_C, variant=thermal.GUIDE9_H300_S50_BEST_REPEAT_VARIANT,
        )
        self.assertEqual(plan["guide_experiment_id"], thermal.GUIDE9_H300_S50_BEST_REPEAT_EXPERIMENT_ID)
        self.assertEqual(plan["target"], {"hue": 300, "sat": 50, "intensity": 100})
        self.assertEqual(plan["budgets"]["physical_cr3_cap"], 4)
        self.assertEqual(
            plan["analysis_contract"]["best_command"],
            {"cw": 192, "ww": 4095, "r": 2495, "g": 0, "b": 2559},
        )
        self.assertEqual(
            plan["frozen_shutters"],
            {"ray-h300-s50": "1/4000", "strip-h300-s50": "1/400"},
        )
        measure.validate_authorized_execution_plan(plan)
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "guide9-h300-s50-best"
            self._execute_fake_protocol(plan, root)
            feature_ids = tuple(
                json.loads(thermal.POLICY_PATH.read_text())["feature_set"]["ids"]
            )
            report = analyze.analyze_thermal_run(root, feature_ids=feature_ids)
            self.assertEqual(report["schema"], "guide9_h300_s50_best_repeat_analysis_v1")
            self.assertEqual(report["classification"], "H300_S50_faithful")
            self.assertEqual(report["next"], "H300_ROUTE_COMPLETE")

    def test_guide9_h300_s50_best_repeat_runtime_wires_source_isolation(self):
        plan = thermal.build_direct_plan(
            thermal.TD_C, variant=thermal.GUIDE9_H300_S50_BEST_REPEAT_VARIANT,
        )
        routed = {}

        class FakeBackend:
            backend_name = "remote"
            v2_capture_capability = measure.REMOTE_V2_CAPABILITY

            def connect(self):
                return object()

            def resolve_capture_settings(self, **_kwargs):
                return SimpleNamespace(iso="100", aperture="f/4", image_format="RAW")

            def capture_with_timing(self, **_kwargs):
                raise AssertionError("runtime wiring test must not capture")

        def fake_execute(_plan, **kwargs):
            routed.update(kwargs)
            return Path("/fake/guide9-h300-s50-best")

        with (
            patch.object(measure, "execute_plan", side_effect=fake_execute),
            patch(
                "camera_based_rgbww_optimizer.optimization.measure_raw_observer_validation.build_native_raw_capture_step_fn",
                return_value=lambda _step: None,
            ),
        ):
            result = measure.run_authorized_plan(
                plan, output_dir=Path("/fake"), run_name="guide9-h300-s50-best",
                camera_backend=FakeBackend(),
            )

        self.assertEqual(result, Path("/fake/guide9-h300-s50-best"))
        self.assertTrue(callable(routed["source_isolation_check_fn"]))
        self.assertTrue(callable(routed["post_capture_validator_fn"]))

    def test_guide9_white12_is_balanced_bounded_and_analyzable(self):
        plan = thermal.build_direct_plan(
            thermal.TD_C, variant=thermal.GUIDE9_WHITE12_VARIANT,
        )
        self.assertEqual(plan["guide_experiment_id"], thermal.GUIDE9_WHITE12_EXPERIMENT_ID)
        self.assertEqual(plan["budgets"], {
            "ray_cap": 12, "strip_cap": 12, "formal_cap": 24,
            "physical_cr3_cap": 24, "ambient_cap": 0, "retry": 0,
        })
        self.assertEqual(len(plan["captures"]), 24)
        self.assertEqual(
            [row["source_order"] for row in plan["analysis_contract"]["target_contracts"]],
            [["ray", "strip"], ["strip", "ray"]] * 6,
        )
        self.assertTrue(all(
            step["requested_elapsed_s"] == 120 and step["steady_claim"] is False
            for step in plan["captures"]
        ))
        self.assertTrue(all(
            step["strip_zero_required"] for step in plan["captures"]
            if step["source_id"] == "ray"
        ))
        self.assertTrue(all(
            step["ray_zero_required"] for step in plan["captures"]
            if step["source_id"] == "strip"
        ))
        measure.validate_authorized_execution_plan(plan)

        feature_ids = tuple(json.loads(thermal.POLICY_PATH.read_text())["feature_set"]["ids"])
        rows = [
            {"plan_step": step, "feature_values": {name: 1.0 for name in feature_ids}}
            for step in plan["captures"]
        ]
        def observation(row):
            source = row["plan_step"]["source_id"]
            base = float(row["plan_step"]["target_cct"])
            cct = base + (0.5 if source == "strip" else 0.0)
            return {
                "white_patch_normalized_per_second": {"R": 1.0, "G1": 1.0, "G2": 1.0, "B": 1.0},
                "neutral_log_chroma": {"log_R_over_G": 0.0, "log_B_over_G": 0.0, "G1_minus_G2_over_mean_G": 0.0},
                "white_point": {"cct_K": cct, "duv": 0.0, "xy": [0.3, 0.3], "uv1960": [0.2, 0.3], "approx_XYZ": [1.0, 1.0, 1.0]},
            }
        report = analyze.analyze_guide9_white12(
            rows, feature_ids=feature_ids,
            target_contracts=plan["analysis_contract"]["target_contracts"],
            observation_fn=observation,
        )
        self.assertEqual(report["classification"], "white_representative_12_pass")
        self.assertEqual(report["passed_node_count"], 12)
        self.assertEqual(report["next"], "GUIDE9_WHITE_FAST_DIRECT_70_V1")

    def test_guide9_white12_runtime_uses_cct_owner_and_isolation(self):
        plan = thermal.build_direct_plan(
            thermal.TD_C, variant=thermal.GUIDE9_WHITE12_VARIANT,
        )
        routed = {}

        class FakeBackend:
            backend_name = "remote"
            v2_capture_capability = measure.REMOTE_V2_CAPABILITY

            def connect(self):
                return object()

            def resolve_capture_settings(self, **_kwargs):
                return SimpleNamespace(iso="100", aperture="f/4", image_format="RAW")

            def capture_with_timing(self, **_kwargs):
                raise AssertionError("runtime wiring test must not capture")

        def fake_execute(_plan, **kwargs):
            ray_step = next(step for step in _plan["captures"] if step["source_id"] == "ray")
            routed["applied"] = kwargs["apply_command_fn"](ray_step)
            routed["readback"] = kwargs["readback_fn"](ray_step)
            routed["source_isolation"] = kwargs["source_isolation_check_fn"]
            return Path("/fake/guide9-white12")

        with (
            patch.object(measure, "execute_plan", side_effect=fake_execute),
            patch(
                "camera_based_rgbww_optimizer.optimization.measure_raw_observer_validation.build_native_raw_capture_step_fn",
                return_value=lambda _step: None,
            ),
            patch(
                "camera_based_rgbww_optimizer.control.ray120c.set_cct",
                return_value={"data": {"cct": 1800, "gm": 0, "intensity": 1000}},
            ) as set_cct,
            patch(
                "camera_based_rgbww_optimizer.control.ray120c.get_cct",
                return_value={"data": {"cct": 1800, "gm": 0, "intensity": 1000}},
            ),
        ):
            result = measure.run_authorized_plan(
                plan, output_dir=Path("/fake"), run_name="guide9-white12",
                camera_backend=FakeBackend(),
            )

        self.assertEqual(result, Path("/fake/guide9-white12"))
        set_cct.assert_called_once_with(1800, gm=0, intensity_percent=100.0)
        self.assertEqual(routed["readback"]["data"]["cct"], 1800)
        self.assertTrue(callable(routed["source_isolation"]))

    def test_guide9_white_local_jacobian_candidates_are_bounded(self):
        plan = thermal.build_direct_plan(
            thermal.TD_C, variant=thermal.GUIDE9_WHITE_LOCAL_JAC_VARIANT,
        )
        self.assertEqual(plan["guide_experiment_id"], thermal.GUIDE9_WHITE_LOCAL_JAC_EXPERIMENT_ID)
        self.assertEqual(plan["budgets"], {
            "ray_cap": 5, "strip_cap": 5, "formal_cap": 10,
            "physical_cr3_cap": 10, "ambient_cap": 0, "retry": 0,
        })
        self.assertEqual(
            [(row["cct"], row["gm"]) for row in plan["analysis_contract"]["target_contracts"]],
            [(3200, 100), (3200, 200), (5600, 100), (20000, 100), (20000, 200)],
        )
        self.assertEqual(
            plan["analysis_contract"]["target_contracts"][0]["strip_command"],
            {"cw": 2271, "ww": 506, "r": 4095, "g": 1939, "b": 56},
        )
        self.assertEqual(len(plan["captures"]), 10)
        self.assertTrue(all(
            step["strip_zero_required"] if step["source_id"] == "ray"
            else step["ray_zero_required"]
            for step in plan["captures"]
        ))
        measure.validate_authorized_execution_plan(plan)

    def test_guide9_white_local_confirm2_is_two_exact_pairs(self):
        plan = thermal.build_direct_plan(
            thermal.TD_C, variant=thermal.GUIDE9_WHITE_LOCAL_CONFIRM2_VARIANT,
        )
        self.assertEqual(plan["guide_experiment_id"], thermal.GUIDE9_WHITE_LOCAL_CONFIRM2_EXPERIMENT_ID)
        self.assertEqual(plan["budgets"]["physical_cr3_cap"], 4)
        self.assertEqual(
            [(row["cct"], row["gm"], row["strip_command"])
             for row in plan["analysis_contract"]["target_contracts"]],
            [
                (3200, 200, {"cw": 756, "ww": 440, "r": 4095, "g": 2431, "b": 32}),
                (20000, 200, {"cw": 4095, "ww": 114, "r": 400, "g": 3792, "b": 3067}),
            ],
        )
        self.assertEqual(len(plan["captures"]), 4)
        measure.validate_authorized_execution_plan(plan)

    def test_guide9_white_local_probes_are_six_bounded_blocks(self):
        plan = thermal.build_direct_plan(
            thermal.TD_C, variant=thermal.GUIDE9_WHITE_LOCAL_PROBES_VARIANT,
        )
        self.assertEqual(plan["guide_experiment_id"], thermal.GUIDE9_WHITE_LOCAL_PROBES_EXPERIMENT_ID)
        self.assertEqual(plan["budgets"], {
            "ray_cap": 6, "strip_cap": 30, "formal_cap": 36,
            "physical_cr3_cap": 36, "ambient_cap": 0, "retry": 0,
        })
        self.assertEqual(len(plan["analysis_contract"]["target_contracts"]), 6)
        self.assertEqual(len(plan["captures"]), 36)
        for contract in plan["analysis_contract"]["target_contracts"]:
            self.assertEqual(len(contract["probes"]), 4)
            self.assertEqual(contract["base_command"][contract["active_channel"]], 4095)
            self.assertEqual(
                {probe["channel"] for probe in contract["probes"]},
                set(thermal.CHANNELS) - {contract["active_channel"]},
            )
        measure.validate_authorized_execution_plan(plan)

        rows = [{"plan_step": step} for step in plan["captures"]]
        def observation(row):
            step = row["plan_step"]
            target = float(step["target_cct"])
            role = str(step["role"])
            if role == "ray_reference":
                cct, duv = target, 0.0
            elif role == "strip_base":
                cct, duv = target - 20.0, 0.001
            else:
                index = sorted(
                    role_name for role_name in {
                        value["role"] for value in plan["captures"]
                        if value["target_cct"] == step["target_cct"]
                        and value["target_gm"] == step["target_gm"]
                        and value["role"].startswith("strip_probe_")
                    }
                ).index(role)
                cct, duv = target - 15.0 + index * 5.0, 0.0008 - index * 0.0002
            return {
                "white_patch_normalized_per_second": {"R": 1.0, "G1": 1.0, "G2": 1.0, "B": 1.0},
                "neutral_log_chroma": {"log_R_over_G": 0.0, "log_B_over_G": 0.0, "G1_minus_G2_over_mean_G": 0.0},
                "white_point": {"cct_K": cct, "duv": duv},
            }
        report = analyze.analyze_guide9_white_local_probes(
            rows, target_contracts=plan["analysis_contract"]["target_contracts"],
            observation_fn=observation,
        )
        self.assertEqual(report["status"], "candidates_preregistered")
        self.assertEqual(report["node_count"], 6)
        self.assertEqual(report["next"], "GUIDE9_WHITE12_LOCAL_PROBE_CANDIDATES")

    def test_guide9_h300_reference_diagnostic_is_order_balanced_and_bounded(self):
        plan = thermal.build_direct_plan(
            thermal.TD_C, variant=thermal.GUIDE9_H300_REFERENCE_DIAG_VARIANT,
        )
        self.assertEqual(
            plan["guide_experiment_id"], thermal.GUIDE9_H300_REFERENCE_DIAG_EXPERIMENT_ID,
        )
        self.assertEqual(
            [step["role"] for step in plan["captures"]],
            ["control_1", "h300_1", "h300_2", "control_2"],
        )
        self.assertEqual([step["session_index"] for step in plan["captures"]], [1, 1, 2, 2])
        self.assertEqual(
            [step["nominal_shutter"] for step in plan["captures"]],
            ["1/16000", "1/2500", "1/2500", "1/16000"],
        )
        self.assertEqual(
            plan["budgets"],
            {"formal_cap": 0, "ambient_cap": 0, "diagnostic_cap": 4,
             "diagnostic_dark_cap": 0, "physical_cr3_cap": 4,
             "setup_physical_cr3_cap": 0, "retry": 0},
        )
        self.assertFalse(plan["analysis_contract"]["root1_strip_pooling"])

    def test_guide9_h300_reference_runtime_wires_source_isolation(self):
        plan = thermal.build_direct_plan(
            thermal.TD_C, variant=thermal.GUIDE9_H300_REFERENCE_DIAG_VARIANT,
        )
        routed = {}

        class FakeBackend:
            backend_name = "remote"
            v2_capture_capability = measure.REMOTE_V2_CAPABILITY

            def connect(self):
                return object()

            def resolve_capture_settings(self, **_kwargs):
                return SimpleNamespace(iso="100", aperture="f/4", image_format="RAW")

            def capture_with_timing(self, **_kwargs):
                raise AssertionError("runtime wiring test must not capture")

        def fake_execute(_plan, **kwargs):
            routed["source_isolation"] = kwargs["source_isolation_check_fn"]
            routed["validator"] = kwargs["post_capture_validator_fn"]
            return Path("/fake/guide9-h300-reference")

        with (
            patch.object(measure, "execute_plan", side_effect=fake_execute),
            patch(
                "camera_based_rgbww_optimizer.optimization.measure_raw_observer_validation.build_native_raw_capture_step_fn",
                return_value=lambda _step: None,
            ),
        ):
            result = measure.run_authorized_plan(
                plan, output_dir=Path("/fake"), run_name="guide9-h300-reference",
                camera_backend=FakeBackend(),
            )

        self.assertEqual(result, Path("/fake/guide9-h300-reference"))
        self.assertTrue(callable(routed["source_isolation"]))
        self.assertTrue(callable(routed["validator"]))

    def test_guide9_h300_reference_diagnostic_classifies_all_branches(self):
        plan = thermal.build_direct_plan(
            thermal.TD_C, variant=thermal.GUIDE9_H300_REFERENCE_DIAG_VARIANT,
        )
        feature_ids = tuple(json.loads(thermal.POLICY_PATH.read_text())["feature_set"]["ids"])

        def run(status_by_role, pair_pass=True):
            def capture(step):
                status = status_by_role.get(step["role"], "pass")
                result = {
                    "direct_quality": {"status": status, "feature_count": 58},
                    "recorded_exposure": {
                        "seconds": float(parse_nominal_exposure(step["nominal_shutter"]))
                    },
                }
                if status == "pass":
                    result["feature_values"] = {feature_id: 1.0 for feature_id in feature_ids}
                return result
            return measure.run_guide9_h300_reference_diagnostic_protocol(
                plan, measure_fn=capture, feature_ids=feature_ids,
                pair_evaluator_fn=lambda *_: {"status": "pass" if pair_pass else "fail"},
            )

        self.assertEqual(run({})["branch"], "R-A")
        self.assertEqual(run({"h300_1": "near_noise_only", "h300_2": "near_noise_only"})["branch"], "R-B")
        self.assertEqual(run({"h300_1": "near_noise_only"})["branch"], "R-C")
        self.assertEqual(run({}, pair_pass=False)["branch"], "R-C")
        self.assertEqual(run({"control_2": "near_noise_only"})["branch"], "R-D")

    def test_guide9_h300_reference_validator_requires_capture_bound_state_evidence(self):
        plan = thermal.build_direct_plan(
            thermal.TD_C, variant=thermal.GUIDE9_H300_REFERENCE_DIAG_VARIANT,
        )
        zero = {
            "requested_payload": {key: 0 for key in ("red", "green", "blue", "warm_white", "cold_white")},
            "device_snapshot": {key: 0 for key in ("red", "green", "blue", "warm_white", "cold_white")},
        }
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            captures = []
            states = []
            for step in plan["captures"]:
                state = {
                    "schema": "guide9_h300_reference_capture_state_v1",
                    "captured_at": "2026-08-23T00:00:00+00:00",
                    "capture_id": step["capture_id"], "session_index": step["session_index"],
                    "exact_command_hash": step["exact_command_hash"],
                    "expected_command": step["command"], "set_response": {"status": "pass"},
                    "immediate_readback": {"data": {"intensity": 255}},
                    "post_capture_readback": {"data": {"intensity": 255}},
                    "strip_zero_before_capture": zero,
                }
                states.append(state)
                captures.append({
                    "capture_id": step["capture_id"], "plan_step": step,
                    "capture": {"ray_state_evidence": state,
                                "direct_quality": {"status": "near_noise_only"}},
                })
            (root / "captures.jsonl").write_text(
                "".join(json.dumps(row) + "\n" for row in captures)
            )
            (root / "physical-returns.jsonl").write_text(
                "".join(json.dumps({"capture_id": step["capture_id"]}) + "\n" for step in plan["captures"])
            )
            (root / "ray-state-evidence.jsonl").write_text(
                "".join(json.dumps(row) + "\n" for row in states)
            )
            (root / "guide9-h300-reference-diagnostic.json").write_text(json.dumps({
                "schema": "guide9_h300_reference_emission_path_diagnostic_evidence_v1",
                "branch": "R-B", "classification": "H300_S100_reference_emission_path_unresolved",
                "physical_capture_count": 4, "formal_capture_count": 0,
                "root1_strip_pooling": False,
            }))
            quality = measure.validate_direct_guide9_h300_reference_post_capture(root, plan, None)
            self.assertEqual(quality["state_evidence_count"], 4)
            (root / "ray-state-evidence.jsonl").write_text(
                "".join(json.dumps(row) + "\n" for row in states[:-1])
            )
            with self.assertRaisesRegex(ValueError, "ledger order differs"):
                measure.validate_direct_guide9_h300_reference_post_capture(root, plan, None)


if __name__ == "__main__":
    unittest.main()
