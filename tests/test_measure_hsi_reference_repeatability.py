from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from camera_based_rgbww_optimizer.control import all_off, camera_remote, esphome, ray120c
from camera_based_rgbww_optimizer.control.all_off import ShutdownStep
from camera_based_rgbww_optimizer.measurement.ray_hsi_manifold import RayHsiManifold
from camera_based_rgbww_optimizer.optimization import measure_hsi_reference_repeatability as subject
from camera_based_rgbww_optimizer.optimization import analyze_hsi_reference_repeatability as analyzer


class MeasureHsiReferenceRepeatabilityTests(unittest.TestCase):
    def test_dry_run_has_exact_30_ray_50_strip_and_never_touches_devices(self):
        with tempfile.TemporaryDirectory(dir=subject.PROJECT_TMP_DIR) as tempdir:
            with (
                mock.patch.object(camera_remote, "create_camera_backend") as camera,
                mock.patch.object(esphome, "light") as strip,
                mock.patch.object(ray120c, "set_hsi") as ray,
                mock.patch.object(all_off, "turn_everything_off") as shutdown,
            ):
                result = subject.main([
                    "--dry-run", "--output-dir", tempdir, "--run-name", "draft",
                ])
            plan = json.loads((Path(tempdir) / "draft" / "plan.json").read_text(encoding="utf-8"))

        self.assertEqual(result, 0)
        self.assertEqual(plan["experiment"], subject.EXPERIMENT_NAME)
        self.assertEqual(plan["measurement"]["formal_ray_count"], 30)
        self.assertEqual(plan["measurement"]["formal_strip_count"], 50)
        self.assertEqual(plan["measurement"]["ambient_count"], 2)
        self.assertEqual(len(plan["captures"]), 82)
        self.assertFalse(plan["formal_capture_eligible"])
        self.assertEqual(plan["authorization"]["status"], "not_authorized_for_execution")
        self.assertEqual(plan["offline_contract"]["network_calls"], 0)
        camera.assert_not_called()
        strip.assert_not_called()
        ray.assert_not_called()
        shutdown.assert_not_called()

    def test_sequence_keeps_ray_blocks_apart_and_balances_repeats(self):
        plan = subject.build_targeted_reference_repeatability_plan()
        formal = [item for item in plan["captures"] if item["formal_measurement"]]
        sources_blocks = []
        for item in formal:
            pair = (item["source"], item["block"])
            if not sources_blocks or sources_blocks[-1] != pair:
                sources_blocks.append(pair)
        self.assertEqual(sources_blocks, [("ray", "A"), ("strip", "A"), ("strip", "B"), ("ray", "B")])
        for block in ("A", "B"):
            ray = [item for item in formal if item["source"] == "ray" and item["block"] == block]
            strip = [item for item in formal if item["source"] == "strip" and item["block"] == block]
            self.assertEqual({(item["state"]["hue"], item["state"]["sat"]): sum(
                other["state"] == item["state"] for other in ray
            ) for item in ray}, {(0, 0): 5, (120, 100): 5, (300, 100): 5})
            self.assertTrue(all(sum(other["command_key"] == key for other in strip) == 5 for key in subject.STRIP_KEYS))

    def test_commands_are_exactly_extracted_from_frozen_sentinel(self):
        plan = subject.build_targeted_reference_repeatability_plan()
        self.assertEqual(max(plan["commands"]["h0-s0-scale-relaxed-3072"].values()), 3072)
        for key in subject.STRIP_KEYS[:-1]:
            self.assertEqual(max(plan["commands"][key].values()), 4095)

    def test_fake_backend_executes_exact_82_and_python_cleanup(self):
        plan = subject.build_targeted_reference_repeatability_plan(
            named_experiment_authorization=subject.EXPERIMENT_NAME,
        )
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir) / "run"
            output = _execute_fake(plan, root)
            run = json.loads((root / "run.json").read_text(encoding="utf-8"))
            captures = (root / "captures.jsonl").read_text(encoding="utf-8").splitlines()
            cleanup = json.loads((root / "all-off-python.json").read_text(encoding="utf-8"))
        self.assertEqual(output, root)
        self.assertEqual(len(captures), 82)
        self.assertEqual(run["logical_captures_completed"], 82)
        self.assertEqual(run["formal_captures_completed"], 80)
        self.assertEqual(run["physical_cr3_count"], 82)
        self.assertTrue(all(item["ok"] for item in cleanup["steps"]))

    def test_fake_backend_failure_preserves_evidence_and_python_cleanup(self):
        plan = subject.build_targeted_reference_repeatability_plan(
            named_experiment_authorization=subject.EXPERIMENT_NAME,
        )
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir) / "run"
            with self.assertRaisesRegex(RuntimeError, "injected capture failure"):
                _execute_fake(plan, root, fail_at=5)
            run = json.loads((root / "run.json").read_text(encoding="utf-8"))
            failure = json.loads((root / "failure.json").read_text(encoding="utf-8"))
            cleanup = json.loads((root / "all-off-python.json").read_text(encoding="utf-8"))
        self.assertEqual(run["status"], "failed")
        self.assertEqual(failure["type"], "RuntimeError")
        self.assertTrue(all(item["ok"] for item in cleanup["steps"]))

    def test_python_and_shell_cleanup_fail_closed(self):
        plan = subject.build_targeted_reference_repeatability_plan(
            named_experiment_authorization=subject.EXPERIMENT_NAME,
        )
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir) / "python"
            with self.assertRaisesRegex(RuntimeError, "successful Python cleanup"):
                _execute_fake(plan, root, cleanup_ok=False)
            run = json.loads((root / "run.json").read_text(encoding="utf-8"))
            self.assertEqual(run["status"], "failed")

            root2 = Path(tempdir) / "shell"
            _execute_fake(plan, root2)
            (root2 / "all-off-shell.json").write_text(json.dumps([
                {"name": "esphome", "ok": True}, {"name": "ray120c", "ok": False},
            ]), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "Python and shell cleanup"):
                analyzer.analyze_reference_repeatability_run(root2, monte_carlo_samples=1000, bootstrap_replicates=100)

    def test_shell_wrapper_has_independent_trap_cleanup(self):
        wrapper = (Path(__file__).parents[1] / "tmp" / "run-hsi-reference-repeatability.zsh").read_text(encoding="utf-8")
        self.assertIn("trap cleanup EXIT", wrapper)
        self.assertIn("camera_based_rgbww_optimizer.control.all_off", wrapper)
        self.assertIn("p7_targeted_reference_repeatability_v2", wrapper)

    def test_analyzer_finalizer_writes_only_formal_ineligible_candidate(self):
        plan = subject.build_targeted_reference_repeatability_plan(
            named_experiment_authorization=subject.EXPERIMENT_NAME,
        )
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir) / "run"
            _execute_fake(plan, root)
            (root / "all-off-shell.json").write_text(json.dumps([
                {"name": "esphome", "ok": True}, {"name": "ray120c", "ok": True},
            ]), encoding="utf-8")
            report_path, candidate_path = analyzer.finalize_reference_repeatability_run(
                root, monte_carlo_samples=1000, bootstrap_replicates=100, seed=11,
            )
            report = json.loads(report_path.read_text(encoding="utf-8"))
            candidate = json.loads(candidate_path.read_text(encoding="utf-8"))
        self.assertEqual(report["status"], "calibrated_waiting_for_planner")
        self.assertFalse(report["formal_capture_eligible"])
        self.assertFalse(candidate["formal_capture_eligible"])
        self.assertTrue(candidate["planner_freeze_required"])
        self.assertIn("empirical_coverage", next(iter(report["synthetic_joint_coverage"]["regions"].values())))

    def test_weak_reacquire_retains_both_attempts_and_recomputes_physical_evidence(self):
        plan = subject.build_targeted_reference_repeatability_plan(
            named_experiment_authorization=subject.EXPERIMENT_NAME,
        )
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir) / "run"
            _execute_fake(plan, root, weak_at=1)
            (root / "all-off-shell.json").write_text(json.dumps([
                {"name": "esphome", "ok": True}, {"name": "ray120c", "ok": True},
            ]), encoding="utf-8")
            report = analyzer.analyze_reference_repeatability_run(
                root, monte_carlo_samples=1000, bootstrap_replicates=100, seed=11,
            )
            attempts = [json.loads(line) for line in (root / "capture-attempts.jsonl").read_text(encoding="utf-8").splitlines()]
            logical = [json.loads(line) for line in (root / "captures.jsonl").read_text(encoding="utf-8").splitlines()]
        weak_attempts = [item for item in attempts if item["logical_capture_id"] == logical[1]["capture_id"]]
        self.assertEqual([item["attempt_kind"] for item in weak_attempts], ["base", "weak_signal_reacquire"])
        self.assertIsNotNone(weak_attempts[0]["quality_rejection"])
        self.assertFalse(weak_attempts[0]["selected_for_formal"])
        self.assertTrue(weak_attempts[1]["selected_for_formal"])
        self.assertEqual(report["capture_audit"]["physical_cr3_count"], 83)
        self.assertEqual(report["capture_audit"]["weak_signal_reacquire_count"], 1)
        self.assertTrue(report["capture_audit"]["commands_jsonl_audited"])

    def test_reacquire_readback_mismatch_fails_and_python_cleanup_runs(self):
        plan = subject.build_targeted_reference_repeatability_plan(
            named_experiment_authorization=subject.EXPERIMENT_NAME,
        )
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir) / "run"
            with self.assertRaises(Exception):
                _execute_fake(plan, root, weak_at=1, mismatch_reacquire=True)
            cleanup = json.loads((root / "all-off-python.json").read_text(encoding="utf-8"))
        self.assertTrue(all(item["ok"] for item in cleanup["steps"]))

    def test_auto_exposure_one_over_is_prechecked_before_adapter_call(self):
        plan = subject.build_targeted_reference_repeatability_plan(
            named_experiment_authorization=subject.EXPERIMENT_NAME,
        )
        plan["measurement"]["physical_capture_audit"]["maximum_autoexposure_physical_cr3"] = 0
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir) / "run"
            with self.assertRaisesRegex(RuntimeError, "before base capture"):
                _execute_fake(plan, root)
            run = json.loads((root / "run.json").read_text(encoding="utf-8"))
        self.assertEqual(run["logical_captures_completed"], 1)
        self.assertEqual(run["physical_cr3_count"], 1)
        self.assertEqual(run["auto_exposure_cache_miss_count"], 0)

    def test_analyzer_rejects_counter_and_command_tampering(self):
        plan = subject.build_targeted_reference_repeatability_plan(
            named_experiment_authorization=subject.EXPERIMENT_NAME,
        )
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir) / "counter"
            _execute_fake(plan, root)
            (root / "all-off-shell.json").write_text(json.dumps([
                {"name": "esphome", "ok": True}, {"name": "ray120c", "ok": True},
            ]), encoding="utf-8")
            run = json.loads((root / "run.json").read_text(encoding="utf-8"))
            run["physical_cr3_count"] += 1
            (root / "run.json").write_text(json.dumps(run), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "counter mismatch"):
                analyzer.analyze_reference_repeatability_run(root, monte_carlo_samples=1000, bootstrap_replicates=100)

            root2 = Path(tempdir) / "commands"
            _execute_fake(plan, root2)
            (root2 / "all-off-shell.json").write_text((root / "all-off-shell.json").read_text(encoding="utf-8"), encoding="utf-8")
            commands = [json.loads(line) for line in (root2 / "commands.jsonl").read_text(encoding="utf-8").splitlines()]
            commands.pop(1)
            (root2 / "commands.jsonl").write_text("\n".join(json.dumps(item) for item in commands) + "\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "command evidence|readback mismatch"):
                analyzer.analyze_reference_repeatability_run(root2, monte_carlo_samples=1000, bootstrap_replicates=100)

    def test_finalizer_branch_matrix_is_deterministic_and_never_implies_formal_eligibility(self):
        cases = {
            "R-PASS": ({"failure_branch": None, "reference_epoch_shift": False}, {"failure_branch": None, "classes_above_p1_floor": []}, {"failure_branch": None}),
            "R-REFERENCE-EPOCH": ({"failure_branch": None, "reference_epoch_shift": True}, {"failure_branch": None, "classes_above_p1_floor": []}, {"failure_branch": None}),
            "R-REFERENCE-UNSTABLE": ({"failure_branch": "R-REFERENCE-UNSTABLE", "reference_epoch_shift": False}, {"failure_branch": None, "classes_above_p1_floor": []}, {"failure_branch": None}),
            "R-STRIP-CLASS-HIGH": ({"failure_branch": None, "reference_epoch_shift": False}, {"failure_branch": None, "classes_above_p1_floor": ["sat100_fullscale"]}, {"failure_branch": None}),
            "uncertainty_unresolved": ({"failure_branch": None, "reference_epoch_shift": False}, {"failure_branch": "uncertainty_unresolved", "classes_above_p1_floor": []}, {"failure_branch": None}),
        }
        for expected, (ray, strip, joint) in cases.items():
            branch = analyzer.select_reference_repeatability_branch(
                ray_analysis=ray, strip_analysis=strip, joint_report=joint,
            )
            self.assertEqual(branch, expected)

    def test_strip_ab_block_shift_is_reported_separately_from_within_block_noise(self):
        manifold = RayHsiManifold.load()
        policy = analyzer.HsiPolicyV2.load(subject.DEFAULT_POLICY)
        states = {
            "h0-s0-fullscale": (0, 0),
            "h120-s100-fullscale": (120, 100),
            "h120-s50-fullscale": (120, 50),
            "h300-s100-fullscale": (300, 100),
            "h0-s0-scale-relaxed-3072": (0, 0),
        }
        current = {}
        for key, state in states.items():
            center = dict(manifold.target_at(*state).features)
            current[key] = {"A": [dict(center) for _ in range(5)], "B": [dict(center) for _ in range(5)]}
        shifted_feature = manifold.coordinate_feature_ids[0]
        for row in current["h120-s50-fullscale"]["B"]:
            row[shifted_feature] *= 1.5
        report, _components = analyzer._analyze_strip(
            current, policy=policy, feature_ids=manifold.coordinate_feature_ids,
            seed=11, monte_carlo_samples=1000,
        )
        failure = next(item for item in report["failed_commands"] if item["command"] == "h120-s50-fullscale")
        self.assertEqual(failure["audit_status"], "pass")
        self.assertEqual(failure["block_center_shift"], "fail")


def _execute_fake(
    plan, root: Path, *, fail_at: int | None = None,
    weak_at: int | None = None, mismatch_reacquire: bool = False,
    cleanup_ok: bool = True,
):
    manifold = RayHsiManifold.load()
    ray_state = {}
    ray_set_calls = 0
    force_readback_mismatch = False

    def capture_step(step):
        if fail_at is not None and int(step["index"]) == fail_at:
            raise RuntimeError("injected capture failure")
        capture_id = step["capture_id"]
        raw = root / "camera" / f"{capture_id}.cr3"
        raw.parent.mkdir(parents=True, exist_ok=True)
        raw.write_bytes(b"CR3")
        if step["source"] == "ray":
            target = manifold.target_at(step["ray"]["hue"], step["ray"]["sat"])
        elif step["source"] == "strip":
            key = next(key for key, command in plan["commands"].items() if command == step["strip_command"])
            state = {
                "h0-s0-fullscale": (0, 0), "h120-s100-fullscale": (120, 100),
                "h120-s50-fullscale": (120, 50), "h300-s100-fullscale": (300, 100),
                "h0-s0-scale-relaxed-3072": (0, 0),
            }[key]
            target = manifold.target_at(*state)
        else:
            target = manifold.target_at(0, 0)
        values = {feature: target.features[feature] for feature in manifold.coordinate_feature_ids}
        report = root / "measurements" / f"{capture_id}.json"
        report.parent.mkdir(parents=True, exist_ok=True)
        report_value = _report(values, raw)
        if weak_at is not None and int(step["index"]) == weak_at and step["capture_id"].endswith("-base"):
            plane = report_value["patches"][0]["planes"]["G1"]
            plane["quality"]["status"] = "rejected"
            plane["metrics"]["near_noise_floor_fraction"] = 0.1
        report.write_text(json.dumps(report_value), encoding="utf-8")
        return {
            "capture": {"saved_file": str(raw), "byte_count": 3, "camera_backend": "remote"},
            "patch_statistics": str(report), "physical_capture_count": 1,
            "auto_exposure_audit": ({"capture_count": 1} if step.get("auto_exposure") else None),
        }

    def strip_light(cw, ww, r, g, b):
        return {"cw": cw, "ww": ww, "r": r, "g": g, "b": b}

    def ray_set_hsi(hue, sat, *, intensity_percent):
        nonlocal ray_set_calls, force_readback_mismatch
        ray_set_calls += 1
        force_readback_mismatch = mismatch_reacquire and ray_set_calls == 2
        ray_state.update({"hue": hue, "sat": sat, "intensity": int(intensity_percent * 10)})
        return {"code": 0, "data": dict(ray_state)}

    def ray_get_hsi():
        state = dict(ray_state)
        if force_readback_mismatch:
            state["hue"] = (int(state["hue"]) + 1) % 360
        return {"code": 0, "data": state}

    return subject.execute_targeted_reference_repeatability_plan(
        plan, run_dir=root, capture_step_fn=capture_step,
        strip_light_fn=strip_light,
        ray_off_fn=lambda: {"code": 0, "data": {"intensity": 0}},
        ray_set_hsi_fn=ray_set_hsi,
        ray_get_hsi_fn=ray_get_hsi,
        sleep_fn=lambda _seconds: None,
        all_off_fn=lambda: [ShutdownStep("esphome", cleanup_ok), ShutdownStep("ray120c", True)],
    )


def _report(values, raw):
    grouped = {}
    for feature, value in values.items():
        patch, plane = feature.split("::")
        grouped.setdefault(patch, {})[plane] = value
    return {
        "schema_version": 1,
        "measurement": "native_bayer_patch_statistics",
        "source": {"path": str(raw)},
        "exposure_metadata": {"status": "recorded"},
        "location_config": {"sha256": "21f02328bff8b5ffcfc10c767e15cdefbf8bb883bc352eff6f0fb7ade38a8f80"},
        "mosaic": {"plane_order": ["R", "G1", "G2", "B"]},
        "observer_config": {"quality_thresholds": {"minimum_valid_pixels_per_plane": 29000, "maximum_nonfinite_fraction": 0.0, "maximum_clipped_fraction": 0.0, "maximum_near_noise_floor_fraction": 0.05}},
        "patches": [{
            "name": patch, "optimization_eligible": True,
            "planes": {
                plane: {
                    "quality": {"status": "accepted"},
                    "metrics": {"valid_pixel_count": 30000, "nonfinite_fraction": 0.0, "clipped_fraction": 0.0, "near_noise_floor_fraction": 0.0},
                    "ambient_subtracted": {"trimmed_mean_per_second": float(planes.get(plane, 0.01))},
                } for plane in ("R", "G1", "G2", "B")
            },
        } for patch, planes in sorted(grouped.items())],
    }


if __name__ == "__main__":
    unittest.main()
