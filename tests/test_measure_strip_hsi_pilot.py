from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from camera_based_rgbww_optimizer.control.all_off import ShutdownStep
from camera_based_rgbww_optimizer.measurement.ray_hsi_manifold import RayHsiManifold
from camera_based_rgbww_optimizer.optimization import analyze_strip_hsi_pilot
from camera_based_rgbww_optimizer.optimization import measure_strip_hsi_pilot as subject


class MeasureStripHsiPilotTests(unittest.TestCase):
    def test_plan_freezes_gate5_basis_location_and_13_targets(self):
        plan = subject.build_strip_hsi_pilot_plan()

        self.assertEqual(plan["measurement"]["phase"], "P7-pilot")
        self.assertEqual(plan["measurement"]["branch"], "full_periodic_2d_HB")
        self.assertEqual(len(plan["targets"]), 13)
        self.assertEqual(len(plan["measurement"]["coordinate_feature_ids"]), 58)
        self.assertEqual(plan["inputs"]["location_config"]["sha256"], subject.LATEST_LOCATION_SHA256)
        self.assertEqual(plan["inputs"]["basis_analysis"]["sha256"], subject.FROZEN_BASIS_SHA256)
        self.assertEqual(plan["inputs"]["ray_hsi_manifold"]["sha256"], subject.FROZEN_MANIFOLD_SHA256)
        self.assertTrue(all(max(target["seed"]["best"]["command"].values()) == 4095 for target in plan["targets"]))

    def test_fake_execution_is_strip_only_and_analyzes_all_points_faithful(self):
        plan = subject.build_strip_hsi_pilot_plan()
        manifold = RayHsiManifold.load()
        target_by_index = {target["index"]: target for target in plan["targets"]}
        light_calls = []
        ray_off_calls = []

        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir) / "run"

            def capture_step(step):
                capture_id = step["capture_id"]
                raw = root / "camera" / f"{capture_id}.cr3"
                raw.parent.mkdir(parents=True, exist_ok=True)
                raw.write_bytes(b"CR3")
                target_index = int(step["analysis_context"]["target_index"])
                if target_index < 0:
                    values = {feature: 0.01 for feature in manifold.coordinate_feature_ids}
                else:
                    target = target_by_index[target_index]
                    measured = manifold.target_at(target["hue"], target["sat"])
                    values = {feature: measured.features[feature] for feature in manifold.coordinate_feature_ids}
                report = root / "measurements" / f"{capture_id}.json"
                report.parent.mkdir(parents=True, exist_ok=True)
                report.write_text(json.dumps(_report(values, raw)), encoding="utf-8")
                return {"capture": {"saved_file": str(raw), "byte_count": 3, "camera_backend": "remote"}, "patch_statistics": str(report)}

            def strip_light(cw, ww, r, g, b):
                payload = {"cw": cw, "ww": ww, "r": r, "g": g, "b": b}
                light_calls.append(payload)
                return payload

            def ray_off():
                ray_off_calls.append(True)
                return {"code": 0, "data": {"intensity": 0}}

            output = subject.execute_strip_hsi_pilot_plan(
                plan,
                run_dir=root,
                capture_step_fn=capture_step,
                strip_light_fn=strip_light,
                ray_off_fn=ray_off,
                sleep_fn=lambda _seconds: None,
                all_off_fn=lambda: [ShutdownStep("esphome", True), ShutdownStep("ray120c", True)],
            )
            shell_cleanup = [{"name": "esphome", "ok": True}, {"name": "ray120c", "ok": True}]
            (root / "all-off-shell.json").write_text(json.dumps(shell_cleanup), encoding="utf-8")
            analysis = analyze_strip_hsi_pilot.analyze_strip_hsi_pilot(root)
            commands = [json.loads(line) for line in (root / "commands.jsonl").read_text(encoding="utf-8").splitlines()]
            captures = (root / "captures.jsonl").read_text(encoding="utf-8").splitlines()

        self.assertEqual(output, root)
        self.assertEqual(len(captures), 40)
        self.assertEqual(analysis["faithful_point_count"], 13)
        self.assertTrue(analysis["decision_hints"]["all_primary_hues_sat100_faithful"])
        self.assertEqual(analysis["decision_hints"]["next_action"], "random_holdout")
        self.assertFalse(any(item["event"] == "ray_on" for item in commands))
        self.assertEqual(len(ray_off_calls), 40)
        self.assertTrue(any(max(call.values()) == 4095 for call in light_calls))

    def test_shell_wrapper_has_double_cleanup_and_fixed_project_cwd(self):
        wrapper = (Path(__file__).parents[1] / "tmp" / "run-strip-hsi-pilot.zsh").read_text(encoding="utf-8")

        self.assertIn('cd "$PROJECT_ROOT"', wrapper)
        self.assertIn("trap cleanup EXIT", wrapper)
        self.assertIn("camera_based_rgbww_optimizer.control.all_off", wrapper)
        self.assertIn("--camera-backend remote", wrapper)


def _report(values, raw):
    grouped = {}
    for feature, value in values.items():
        patch, plane = feature.split("::")
        grouped.setdefault(patch, {})[plane] = value
    patches = []
    for patch, planes in sorted(grouped.items()):
        patches.append({
            "name": patch,
            "optimization_eligible": True,
            "planes": {
                plane: {
                    "quality": {"status": "accepted"},
                    "metrics": {"valid_pixel_count": 30000, "nonfinite_fraction": 0.0, "clipped_fraction": 0.0, "near_noise_floor_fraction": 0.0},
                    "ambient_subtracted": {"trimmed_mean_per_second": float(planes.get(plane, 0.01))},
                }
                for plane in ("R", "G1", "G2", "B")
            },
        })
    return {
        "schema_version": 1,
        "measurement": "native_bayer_patch_statistics",
        "source": {"path": str(raw)},
        "exposure_metadata": {"status": "recorded"},
        "location_config": {"sha256": subject.LATEST_LOCATION_SHA256},
        "mosaic": {"plane_order": ["R", "G1", "G2", "B"]},
        "observer_config": {"quality_thresholds": {"minimum_valid_pixels_per_plane": 29000, "maximum_nonfinite_fraction": 0.0, "maximum_clipped_fraction": 0.0, "maximum_near_noise_floor_fraction": 0.05}},
        "patches": patches,
    }


if __name__ == "__main__":
    unittest.main()
