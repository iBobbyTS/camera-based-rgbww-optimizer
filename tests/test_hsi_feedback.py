from __future__ import annotations

import unittest

import numpy as np

from camera_based_rgbww_optimizer.optimization.hsi_feedback import run_hsi_feedback


CHANNELS = ("cw", "ww", "r", "g", "b")


class HsiFeedbackTests(unittest.TestCase):
    def test_linear_feedback_converges_and_confirms(self):
        target = np.asarray([0.4, 0.6, 0.2, 0.8])
        calls = []

        def capture(command, *, phase, settled_confirmation):
            calls.append((phase, settled_confirmation, dict(command)))
            values = np.asarray([command[channel] / 4095.0 for channel in ("ww", "r", "g", "b")])
            residual = values - target
            hue = float(residual[0])
            sat = float(residual[1])
            shape = residual[2:]
            normalized_shape = shape / 0.04
            return {
                "residuals": {"hue": [hue / 0.03], "sat": [sat / 0.03], "shape": normalized_shape.tolist()},
                "objective": {
                    "feasible": abs(hue) < 0.03 and abs(sat) < 0.03 and np.linalg.norm(shape) < 0.04,
                    "hue_normalized": hue / 0.03,
                    "sat_normalized": sat / 0.03,
                    "orthogonal_normalized": float(np.linalg.norm(normalized_shape)),
                    "shape_normalized_p90": float(np.max(np.abs(normalized_shape))),
                    "shape_normalized_maximum": float(np.max(np.abs(normalized_shape))),
                    "command_continuity_l1": 0.0,
                },
            }

        result = run_hsi_feedback(
            initial_command={"cw": 4095, "ww": 3000, "r": 500, "g": 3000, "b": 500},
            active_channel="cw",
            capture_observation_fn=capture,
            rounds=12,
            probe_step_code=256,
            max_step_code=1024,
            damping=0.001,
        )

        self.assertTrue(result["goal_confirmed"])
        self.assertEqual(result["status"], "goal_confirmed")
        self.assertEqual(len(result["confirmation_attempts"][-1]["sample_indices"]), 2)
        self.assertTrue(any(settled for _phase, settled, _command in calls))
        self.assertEqual(result["selected_command"]["cw"], 4095)

    def test_rejected_candidate_backtracks_without_adding_sample(self):
        rejected = []

        def capture(command, *, phase, settled_confirmation):
            if phase.startswith("feedback") and "backtrack" not in phase:
                rejected.append(phase)
                return {"measurement_rejected": True, "rejection_evidence": {"weak": True}}
            value = (command["ww"] - 1800) / 1000.0
            return {
                "residuals": {"hue": [value], "sat": [value], "shape": [value, value]},
                "objective": {
                    "feasible": abs(value) < 0.05,
                    "hue_normalized": value,
                    "sat_normalized": value,
                    "orthogonal_normalized": abs(value),
                    "shape_normalized_p90": abs(value),
                    "shape_normalized_maximum": abs(value),
                    "command_continuity_l1": 0.0,
                },
            }

        result = run_hsi_feedback(
            initial_command={"cw": 4095, "ww": 3000, "r": 1000, "g": 1000, "b": 1000},
            active_channel="cw",
            capture_observation_fn=capture,
            rounds=2,
        )

        self.assertTrue(rejected)
        self.assertTrue(result["measurement_rejections"])
        self.assertFalse(any(sample["phase"] in rejected for sample in result["samples"]))


if __name__ == "__main__":
    unittest.main()
