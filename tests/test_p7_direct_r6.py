import hashlib
import json
import tempfile
import unittest
from camera_based_rgbww_optimizer.measurement.recorded_exposure import parse_nominal_exposure
from pathlib import Path
from unittest.mock import patch

from camera_based_rgbww_optimizer.optimization import p7_thermal_diagnostics as thermal
from camera_based_rgbww_optimizer.optimization import measure_p7_thermal_diagnostics as measure
from camera_based_rgbww_optimizer.optimization import analyze_p7_thermal_diagnostics as analyze


class DirectR6Tests(unittest.TestCase):
    def _execute_fake_protocol(self, plan, root):
        feature_ids = tuple(json.loads(thermal.POLICY_PATH.read_text())["feature_set"]["ids"])
        curve = json.loads(thermal.CURVE_PATH.read_text())

        def capture(step):
            index = int(step["capture_id"].split("-", 1)[0])
            raw = root / f"{step['capture_id']}.cr3"
            raw.parent.mkdir(parents=True, exist_ok=True)
            raw.write_bytes(f"fake-{index}".encode())
            sidecar = raw.with_suffix(raw.suffix + ".metadata.json")
            sidecar.write_text("{}")
            timing = {
                "tier": "tier_b", "status": "accepted_best_effort_anchor",
                "provenance": thermal.TIMING_CONTRACT_V2["provenance"],
                "best_effort_elapsed_s": float(index + 1),
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
                output["feature_values"] = {feature_id: 1.0 for feature_id in feature_ids}
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
                        "cw": 0, "ww": 0, "r": 0, "g": 0, "b": 0,
                    },
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
                "ray_verified_off": True,
            }

        with patch.object(measure, "_validate_returned_sidecar", side_effect=fake_sidecar):
            return measure.execute_plan(
                plan, run_dir=root,
                apply_command_fn=lambda step: {"status": "pass"},
                readback_fn=lambda step: {"status": "pass"},
                capture_fn=capture, both_off_gate_fn=gate,
                cleanup_fn=lambda: {"status": "pass", "steps": [{"ok": True}]},
                runtime_capture_settings_provenance=plan["camera"]["resolved_capture_settings"],
                post_capture_validator_fn=measure.validate_direct_protocol_post_capture,
                sleep_fn=lambda _seconds: None,
            )

    def test_exact_sequence_and_contract(self):
        spec = thermal.build_ray_r6_spec()
        self.assertEqual(spec["capture_ids"], list(thermal.TD_B_R6_CAPTURE_IDS))
        self.assertEqual(len(spec["captures"]), 16)
        self.assertEqual({r["nominal_shutter"] for r in spec["captures"]}, {"1/5000", "1/6400", "1/8000", "1/2500"})
        self.assertTrue(all(r["exposure_mode"] == "fixed" and not r["weak_reacquire"] for r in spec["captures"]))

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
                    "timing_evidence": timing, "thermal_covariates": covariates,
                    "feature_values": {feature_id: 1.0 for feature_id in feature_ids},
                    "direct_quality": {
                        "status": "pass", "feature_count": len(feature_ids),
                    },
                    "recorded_exposure": {
                        "source": "Canon:ExposureTime", "status": "recorded",
                        "seconds": {"A": 1 / 5000, "D": 1 / 6400, "B": 1 / 8000, "C": 1 / 2500}[step["state_id"]],
                    },
                    "strip_zero_before_capture": {
                        "requested_payload": {
                            "red": 0, "green": 0, "blue": 0,
                            "warm_white": 0, "cold_white": 0,
                        },
                        "device_snapshot": {
                            "cw": 0, "ww": 0, "r": 0, "g": 0, "b": 0,
                        },
                    },
                }

            def gate(g): return {"status": "pass", "strip_verified_off": True, "ray_verified_off": True}
            def cleanup():
                calls.append(("cleanup",)); return {"status": "pass", "steps": [{"ok": True}]}

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
                    capture_fn=capture, both_off_gate_fn=gate, cleanup_fn=cleanup,
                    runtime_capture_settings_provenance=spec["camera"]["resolved_capture_settings"],
                    post_capture_validator_fn=measure.validate_direct_ray_r6_post_capture,
                    sleep_fn=lambda _: None,
                )
            self.assertTrue(path.is_dir())
            self.assertEqual(sum(1 for c in calls if c[0] == "capture"), 16)
            self.assertTrue(any(c[0] == "cleanup" for c in calls))
            self.assertEqual(len((root / "physical-returns.jsonl").read_text().splitlines()), 16)
            self.assertEqual(len((root / "captures.jsonl").read_text().splitlines()), 16)
            self.assertEqual(len(sidecar_result_by_capture), 16)
            (root / "all-off-shell.json").write_text(json.dumps([{"ok": True}]))
            (root / "all-off-shell.exit-status.txt").write_text("0\n")
            (root / "wrapper-result.json").write_text(json.dumps({
                "status": "complete", "child_exit_code": 0,
                "shell_cleanup_exit_code": 0, "wrapper_exit_code": 0, "signal": None,
            }))
            report = analyze.analyze_thermal_run(root, feature_ids=feature_ids)
            self.assertEqual(report["direct_artifact_validation"], "pass")
            self.assertTrue(report["formal_pass"])

            captures_path = root / "captures.jsonl"
            original_capture_lines = captures_path.read_text().splitlines()
            tampered_capture = json.loads(original_capture_lines[0])
            tampered_capture["capture"]["recorded_exposure"]["seconds"] = 1.0
            tampered_capture_lines = [json.dumps(tampered_capture), *original_capture_lines[1:]]
            captures_path.write_text("\n".join(tampered_capture_lines) + "\n")
            with self.assertRaises(ValueError):
                analyze.analyze_thermal_run(root, feature_ids=feature_ids)
            captures_path.write_text("\n".join(original_capture_lines) + "\n")
            (root / "quality.json").unlink()
            with self.assertRaises(ValueError):
                analyze.analyze_thermal_run(root, feature_ids=feature_ids)
            self.assertEqual(report["capture_count"], 16)

    def test_downstream_direct_specs_use_scientific_prerequisites(self):
        strip = thermal.build_direct_plan(thermal.TD_B, source="strip")
        td_c = thermal.build_direct_plan(thermal.TD_C)
        self.assertEqual(strip["execution_authorization"]["schema"], "direct_strip_td_b_authority_v1")
        self.assertEqual(td_c["execution_authorization"]["schema"], "direct_td_c_core_authority_v1")
        self.assertEqual(strip["timing_resolution"], "direct_operational_600")
        self.assertEqual(td_c["timing_resolution"], "direct_operational_600")
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
                report = analyze.analyze_thermal_run(
                    run,
                    feature_ids=tuple(json.loads(thermal.POLICY_PATH.read_text())["feature_set"]["ids"]),
                    compatibility_fn=lambda _left, _right: True,
                )
                self.assertEqual(report["direct_artifact_validation"], "pass")


if __name__ == "__main__":
    unittest.main()
