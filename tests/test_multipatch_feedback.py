import unittest

import numpy as np

from camera_based_rgbww_optimizer.optimization.multipatch_feedback import run_multipatch_feedback


class MultipatchFeedbackTests(unittest.TestCase):
    def test_linear_synthetic_feedback_converges_and_confirms(self):
        calls = []

        def capture(command, *, phase, settled_confirmation):
            calls.append((phase, settled_confirmation, dict(command)))
            x = (command["ww"] - 2048) / 4095
            y = (command["r"] - 1024) / 4095
            return {
                "residuals": {
                    "neutral": np.asarray([x]),
                    "white": np.asarray([y, 0.0]),
                    "training": np.asarray([x + y]),
                    "holdout": np.asarray([x - y]),
                }
            }

        result = run_multipatch_feedback(
            initial_command={"cw": 4095, "ww": 1000, "r": 2000, "g": 0, "b": 0},
            active_channel="cw", capture_observation_fn=capture,
            neutral_chroma_tolerance=0.01, rounds=8, probe_step_code=256,
            max_step_code=2048, confirmations=2,
        )
        self.assertTrue(result["goal_confirmed"])
        self.assertEqual(result["selected_command"]["cw"], 4095)
        self.assertEqual(len(result["confirmation_attempts"][-1]["sample_indices"]), 2)
        self.assertTrue(all(settled for phase, settled, _ in calls if phase.startswith("confirm")))

    def test_failed_confirmation_rebuilds_jacobian(self):
        confirmation_count = 0

        def capture(command, *, phase, settled_confirmation):
            nonlocal confirmation_count
            value = 0.0
            if settled_confirmation and confirmation_count == 0:
                value = 0.2
                confirmation_count += 1
            return {
                "residuals": {
                    "neutral": np.asarray([value]), "white": np.asarray([0.0, 0.0]),
                    "training": np.asarray([0.0]), "holdout": np.asarray([0.0]),
                }
            }

        result = run_multipatch_feedback(
            initial_command={"cw": 4095, "ww": 1000, "r": 1000, "g": 1000, "b": 1000},
            active_channel="cw", capture_observation_fn=capture,
            neutral_chroma_tolerance=0.01, rounds=1, confirmations=2, thermal_rebases=1,
        )
        self.assertTrue(result["goal_confirmed"])
        self.assertEqual(result["confirmation_attempts"][0]["status"], "failed")
        self.assertEqual(len(result["thermal_rebases"]), 1)

    def test_unmeasurable_feedback_step_backtracks_without_polluting_samples(self):
        calls = []

        def capture(command, *, phase, settled_confirmation):
            calls.append((phase, dict(command)))
            if phase.startswith("feedback-") and command["ww"] < 700:
                return {
                    "measurement_rejected": True,
                    "rejection_evidence": {"rejected_features": [{"feature_id": "block_12::R"}]},
                }
            value = command["ww"] / 4095
            return {
                "residuals": {
                    "neutral": np.asarray([value]),
                    "white": np.asarray([0.0, 0.0]),
                    "training": np.asarray([value]),
                    "holdout": np.asarray([value]),
                }
            }

        result = run_multipatch_feedback(
            initial_command={"cw": 4095, "ww": 1000, "r": 1000, "g": 1000, "b": 1000},
            active_channel="cw", capture_observation_fn=capture,
            neutral_chroma_tolerance=0.001, rounds=2, probe_step_code=256,
            max_step_code=2048, confirmations=2,
        )
        self.assertTrue(result["measurement_rejections"])
        self.assertTrue(any("backtrack" in phase for phase, _command in calls))
        self.assertTrue(all(sample["command"]["ww"] >= 700 for sample in result["samples"]))
        self.assertTrue(all(item["evidence"]["rejected_features"] for item in result["measurement_rejections"]))

    def test_unmeasurable_confirmation_is_a_failed_confirmation_not_an_abort(self):
        def capture(command, *, phase, settled_confirmation):
            if settled_confirmation:
                return {
                    "measurement_rejected": True,
                    "rejection_evidence": {"rejected_features": [{"feature_id": "block_12::R"}]},
                }
            return {
                "residuals": {
                    "neutral": np.asarray([0.0]),
                    "white": np.asarray([0.0, 0.0]),
                    "training": np.asarray([0.0]),
                    "holdout": np.asarray([0.0]),
                }
            }

        result = run_multipatch_feedback(
            initial_command={"cw": 4095, "ww": 1000, "r": 1000, "g": 1000, "b": 1000},
            active_channel="cw", capture_observation_fn=capture,
            neutral_chroma_tolerance=0.01, rounds=0, confirmations=2,
        )
        self.assertFalse(result["goal_confirmed"])
        self.assertEqual(result["confirmation_attempts"][0]["status"], "measurement_rejected")
        self.assertEqual(result["measurement_rejections"][0]["phase"], "confirm-0-0")
        self.assertEqual(len(result["samples"]), 1)
