from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from camera_based_rgbww_optimizer.control.all_off import ShutdownStep
from camera_based_rgbww_optimizer.optimization import measure_ray_hsi_manifold as subject


class MeasureRayHsiManifoldTests(unittest.TestCase):
    def test_plan_freezes_expected_states_and_latest_location(self):
        plan = subject.build_ray_hsi_manifold_plan(off_seconds=0, settle_seconds=0)

        self.assertEqual(len(plan["captures"]), 106)
        self.assertEqual(plan["measurement"]["base_state_count"], 73)
        self.assertEqual(plan["inputs"]["location_config"]["sha256"], "21f02328bff8b5ffcfc10c767e15cdefbf8bb883bc352eff6f0fb7ade38a8f80")
        self.assertEqual({step["source"] for step in plan["captures"]}, {"ambient", "ray"})
        self.assertTrue(all(step["strip_command"] is None for step in plan["captures"]))
        sat0_hue0 = [step for step in plan["captures"] if step["analysis_context"].get("family") == "sat0" and step["analysis_context"].get("hue") == 0]
        self.assertEqual(len(sat0_hue0), 5)
        coarse = [step for step in plan["captures"] if step["purpose"] == "hsi_coarse"]
        self.assertEqual(len(coarse), 72)
        self.assertEqual({(step["ray_state"]["hue"], step["ray_state"]["sat"]) for step in coarse}, {(hue, sat) for hue in range(0, 360, 30) for sat in (5, 20, 50, 80, 95, 100)})

    def test_fake_execution_verifies_readback_and_always_cleans_up(self):
        plan = subject.build_ray_hsi_manifold_plan(off_seconds=0, settle_seconds=0)
        events = []
        state = {}

        def strip_off():
            events.append("strip_off")
            return {"cold_white": 0, "warm_white": 0, "red": 0, "green": 0, "blue": 0}

        def ray_off():
            events.append("ray_off")
            return {"code": 0, "data": {"intensity": 0}}

        def set_hsi(hue, sat, *, intensity_percent):
            state["hsi"] = {"hue": hue, "sat": sat, "intensity": round(intensity_percent * 10)}
            events.append(("set_hsi", hue, sat))
            return {"code": 0, "data": dict(state["hsi"])}

        def get_hsi():
            return {"code": 0, "data": dict(state["hsi"])}

        def set_rgb(r, g, b, *, intensity_percent):
            state["rgb"] = {"r": r, "g": g, "b": b, "intensity": round(intensity_percent * 10)}
            events.append(("set_rgb", r, g, b))
            return {"code": 0, "data": dict(state["rgb"])}

        def get_rgb():
            return {"code": 0, "data": dict(state["rgb"])}

        cleanup_calls = []

        def cleanup():
            cleanup_calls.append(True)
            return [ShutdownStep("esphome", True), ShutdownStep("ray120c", True)]

        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir) / "run"
            output = subject.execute_ray_hsi_manifold_plan(
                plan,
                run_dir=root,
                strip_off_fn=strip_off,
                ray_set_hsi_fn=set_hsi,
                ray_get_hsi_fn=get_hsi,
                ray_set_rgb_fn=set_rgb,
                ray_get_rgb_fn=get_rgb,
                ray_off_fn=ray_off,
                capture_step_fn=lambda step: {"fake": step["capture_id"]},
                sleep_fn=lambda _seconds: None,
                cleanup_fn=cleanup,
            )

            run = json.loads((root / "run.json").read_text(encoding="utf-8"))
            captures = (root / "captures.jsonl").read_text(encoding="utf-8").splitlines()

        self.assertEqual(output, root)
        self.assertEqual(run["status"], "complete")
        self.assertEqual(run["completed_capture_count"], 106)
        self.assertEqual(len(captures), 106)
        self.assertEqual(len(cleanup_calls), 1)
        self.assertEqual(events.count("strip_off"), 106)
        self.assertGreater(events.count("ray_off"), 106)

    def test_readback_mismatch_fails_and_runs_python_cleanup(self):
        plan = subject.build_ray_hsi_manifold_plan(off_seconds=0, settle_seconds=0)
        cleanup_calls = []

        def cleanup():
            cleanup_calls.append(True)
            return [ShutdownStep("esphome", True), ShutdownStep("ray120c", True)]

        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir) / "run"
            with self.assertRaisesRegex(RuntimeError, "readback mismatch"):
                subject.execute_ray_hsi_manifold_plan(
                    plan,
                    run_dir=root,
                    strip_off_fn=lambda: {},
                    ray_set_hsi_fn=lambda *_args, **_kwargs: {"code": 0},
                    ray_get_hsi_fn=lambda: {"code": 0, "data": {"hue": 999, "sat": 0, "intensity": 1000}},
                    ray_set_rgb_fn=lambda *_args, **_kwargs: {"code": 0},
                    ray_get_rgb_fn=lambda: {"code": 0, "data": {}},
                    ray_off_fn=lambda: {"code": 0},
                    capture_step_fn=lambda step: {"fake": step["capture_id"]},
                    sleep_fn=lambda _seconds: None,
                    cleanup_fn=cleanup,
                )

            run = json.loads((root / "run.json").read_text(encoding="utf-8"))
            failure = json.loads((root / "failure.json").read_text(encoding="utf-8"))

        self.assertEqual(run["status"], "failed")
        self.assertEqual(failure["type"], "RuntimeError")
        self.assertEqual(len(cleanup_calls), 1)

    def test_shell_wrapper_has_independent_cleanup_trap(self):
        wrapper = (Path(__file__).parents[1] / "tmp" / "run-ray-hsi-manifold.zsh").read_text(encoding="utf-8")

        self.assertIn("trap cleanup EXIT", wrapper)
        self.assertIn("camera_based_rgbww_optimizer.control.all_off", wrapper)
        self.assertIn("--camera-backend remote", wrapper)
        self.assertIn("locations-20260714-211759.json", wrapper)
        self.assertIn('cd "$PROJECT_ROOT"', wrapper)


if __name__ == "__main__":
    unittest.main()
