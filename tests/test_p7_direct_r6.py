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
                        "red": 0, "green": 0, "blue": 0,
                        "warm_white": 0, "cold_white": 0,
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
                "ray_verified_off": True, "ray_off_command": {"status": "pass"},
            }

        with patch.object(measure, "_validate_returned_sidecar", side_effect=fake_sidecar):
            return measure.execute_plan(
                plan, run_dir=root,
                apply_command_fn=lambda step: {"status": "pass"},
                readback_fn=lambda step: {"status": "pass"},
                capture_fn=capture, both_off_gate_fn=gate,
                cleanup_fn=lambda: {"status": "pass", "steps": [{"ok": True}]},
                runtime_capture_settings_provenance=plan["camera"]["resolved_capture_settings"],
                runtime_git_provenance={"commit": "0" * 40, "dirty": False, "dirty_entries": []},
                post_capture_validator_fn=measure.validate_direct_protocol_post_capture,
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

            captures_path = root / "captures.jsonl"
            original_capture_lines = captures_path.read_text().splitlines()
            tampered_capture = json.loads(original_capture_lines[0])
            tampered_capture["capture"]["recorded_exposure"]["seconds"] = 1.0
            tampered_capture_lines = [json.dumps(tampered_capture), *original_capture_lines[1:]]
            captures_path.write_text("\n".join(tampered_capture_lines) + "\n")
            with self.assertRaises(ValueError):
                analyze.analyze_thermal_run(root, feature_ids=feature_ids)
            captures_path.write_text("\n".join(original_capture_lines) + "\n")
            location_copy = root / "inputs/location.json"
            original_location = location_copy.read_bytes()
            location_copy.write_bytes(original_location + b"\n")
            with self.assertRaises(ValueError):
                analyze.analyze_thermal_run(root, feature_ids=feature_ids)
            location_copy.write_bytes(original_location)
            (root / "quality.json").unlink()
            with self.assertRaises(ValueError):
                analyze.analyze_thermal_run(root, feature_ids=feature_ids)
            self.assertEqual(report["capture_count"], 16)

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
