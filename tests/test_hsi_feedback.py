from __future__ import annotations

import unittest

import numpy as np

from camera_based_rgbww_optimizer.optimization.hsi_budget import HsiSolverBudgetLimits, HsiStartBudget

from camera_based_rgbww_optimizer.optimization.hsi_feedback import (
    run_hsi_feedback,
    run_hsi_feedback_multiseed,
)


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
        self.assertEqual(len(result["confirmation_attempts"][-1]["sample_indices"]), 3)
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

    def test_solver_budget_is_not_expanded_after_requested_rounds(self):
        calls = []

        def capture(command, *, phase, settled_confirmation):
            calls.append((phase, dict(command)))
            value = 2.0 + command["ww"] / 4095.0
            return {
                "residuals": {"hue": [value], "sat": [value], "shape": [value, value]},
                "objective": {
                    "feasible": False,
                    "hue_normalized": value,
                    "sat_normalized": value,
                    "orthogonal_normalized": value,
                    "shape_normalized_p90": value,
                    "shape_normalized_maximum": value,
                    "command_continuity_l1": 0.0,
                },
            }

        result = run_hsi_feedback(
            initial_command={"cw": 4095, "ww": 2000, "r": 1000, "g": 1000, "b": 1000},
            active_channel="cw",
            capture_observation_fn=capture,
            rounds=2,
        )

        self.assertEqual(result["rounds_requested"], 2)
        self.assertLessEqual(result["rounds_completed"], 2)
        self.assertFalse(result["goal_confirmed"])
        self.assertIn(result["status"], {"solver_budget_exhausted", "no_new_command"})
        self.assertFalse(any(phase.startswith("feedback-2") for phase, _command in calls))

    def test_v2_multiseed_has_strict_start_round_and_capture_bounds(self):
        calls = []

        def capture(command, *, phase, settled_confirmation):
            calls.append((phase, dict(command)))
            coordinate = [(command["ww"] - 1000) / 4095.0, (command["r"] - 1000) / 4095.0]
            rendering = [(command["g"] - 1000) / 4095.0, (command["b"] - 1000) / 4095.0]
            return {
                "residuals": {"coordinate": coordinate, "rendering": rendering},
                "objective": {
                    "kind": "ray_hsi_policy_v2_lexicographic",
                    "feasible": False,
                    "hue_defined": True,
                    "hue_error_degrees": coordinate[0],
                    "sat_error_percent": coordinate[1],
                    "coordinate_guarded_excess": float(np.linalg.norm(coordinate)),
                    "coordinate_guarded_limit": 2.5,
                    "color_rendering_residual": {"whitened_score": float(np.linalg.norm(rendering))},
                    "command_continuity_l1": 0.0,
                },
            }

        limits = HsiSolverBudgetLimits(
            feedback_attempts_per_start=1,
            confirmations_per_group=3,
            rebase_count_per_start=0,
        )
        result = run_hsi_feedback_multiseed(
            seeds=[
                {"active_channel": "cw", "command": {"cw": 4095, "ww": 2000, "r": 2000, "g": 2000, "b": 2000}},
                {"active_channel": "ww", "command": {"cw": 2000, "ww": 4095, "r": 2000, "g": 2000, "b": 2000}},
                {"active_channel": "r", "command": {"cw": 2000, "ww": 2000, "r": 4095, "g": 2000, "b": 2000}},
            ],
            capture_observation_fn=capture,
            max_starts=2,
            rounds_per_start=1,
            budget_limits=limits,
        )

        self.assertLessEqual(result["attempt_count"], 2)
        self.assertLessEqual(result["logical_observations_used"], limits.logical_per_target)
        self.assertTrue(all(item["result"]["rounds_requested"] == 1 for item in result["attempts"]))
        self.assertTrue(all(item["result"]["step_records"] for item in result["attempts"]))

    def test_first_start_exhaustion_keeps_best_valid_and_second_start_reservation(self):
        def capture(command, *, phase, settled_confirmation):
            first_face = command["cw"] == 4095
            if first_face and phase.startswith("probe-"):
                return {
                    "measurement_rejected": True,
                    "rejection_evidence": {"status": "solver_budget_exhausted", "sub_budget": "physical_cr3"},
                }
            feasible = command["ww"] == 4095
            coordinate = [0.0, 0.0] if feasible else [2.0, 2.0]
            return {
                "residuals": {"coordinate": coordinate, "rendering": [0.0, 0.0]},
                "objective": {
                    "kind": "ray_hsi_policy_v2_lexicographic", "feasible": feasible,
                    "hue_defined": True, "hue_error_degrees": coordinate[0],
                    "sat_error_percent": coordinate[1], "coordinate_guarded_limit": 1.0,
                    "coordinate_guarded_excess": max(float(np.linalg.norm(coordinate)) - 1.0, 0.0),
                    "color_rendering_residual": {"whitened_score": 0.0},
                    "command_continuity_l1": 0.0,
                },
            }

        limits = HsiSolverBudgetLimits(
            feedback_attempts_per_start=1, confirmations_per_group=3,
            rebase_count_per_start=0,
        )
        result = run_hsi_feedback_multiseed(
            seeds=[
                {"active_channel": "cw", "command": {"cw": 4095, "ww": 1000, "r": 1000, "g": 1000, "b": 1000}},
                {"active_channel": "ww", "command": {"cw": 1000, "ww": 4095, "r": 1000, "g": 1000, "b": 1000}},
            ],
            capture_observation_fn=capture,
            max_starts=2, rounds_per_start=1, budget_limits=limits,
        )
        self.assertEqual(result["attempt_count"], 2)
        self.assertIsNotNone(result["attempts"][0]["result"]["best"])
        self.assertEqual(result["attempts"][0]["result"]["status"], "solver_budget_exhausted")
        self.assertTrue(result["attempts"][1]["result"]["goal_confirmed"])
        self.assertEqual(result["selected_start_index"], 1)

    def test_confirmed_face_wins_over_lower_error_unconfirmed_face(self):
        def capture(command, *, phase, settled_confirmation):
            first_face = command["cw"] == 4095
            feasible = not first_face
            coordinate = [0.01, 0.01] if first_face else [0.5, 0.5]
            return {
                "residuals": {"coordinate": coordinate, "rendering": [0.0, 0.0]},
                "objective": {
                    "kind": "ray_hsi_policy_v2_lexicographic", "feasible": feasible,
                    "hue_defined": True, "hue_error_degrees": coordinate[0],
                    "sat_error_percent": coordinate[1], "coordinate_guarded_limit": 1.0,
                    "coordinate_guarded_excess": 0.0 if feasible else 0.01,
                    "color_rendering_residual": {"whitened_score": 0.0},
                    "command_continuity_l1": 0.0,
                },
            }

        limits = HsiSolverBudgetLimits(
            feedback_attempts_per_start=1, confirmations_per_group=3,
            rebase_count_per_start=0,
        )
        result = run_hsi_feedback_multiseed(
            seeds=[
                {"active_channel": "cw", "command": {"cw": 4095, "ww": 1000, "r": 1000, "g": 1000, "b": 1000}},
                {"active_channel": "ww", "command": {"cw": 1000, "ww": 4095, "r": 1000, "g": 1000, "b": 1000}},
            ],
            capture_observation_fn=capture,
            max_starts=2, rounds_per_start=1, budget_limits=limits,
        )
        self.assertEqual(result["status"], "goal_confirmed")
        self.assertEqual(result["selected_start_index"], 1)
        self.assertTrue(result["selected_result"]["goal_confirmed"])

    def test_confirmation_collects_full_group_after_first_gate_failure(self):
        confirmation_phases = []

        def capture(command, *, phase, settled_confirmation):
            if settled_confirmation:
                confirmation_phases.append(phase)
            feasible = phase == "initial" or (settled_confirmation and not phase.endswith("-0"))
            value = 0.0 if feasible else 2.0
            return {
                "residuals": {"coordinate": [value, value], "rendering": [0.0, 0.0]},
                "objective": {
                    "kind": "ray_hsi_policy_v2_lexicographic", "feasible": feasible,
                    "hue_defined": True, "hue_error_degrees": value,
                    "sat_error_percent": value, "coordinate_guarded_limit": 1.0,
                    "coordinate_guarded_excess": max(value - 1.0, 0.0),
                    "color_rendering_residual": {"whitened_score": 0.0},
                    "command_continuity_l1": 0.0,
                },
            }

        limits = HsiSolverBudgetLimits(
            feedback_attempts_per_start=1, confirmations_per_group=3,
            rebase_count_per_start=0,
        )
        result = run_hsi_feedback(
            initial_command={"cw": 4095, "ww": 1000, "r": 1000, "g": 1000, "b": 1000},
            active_channel="cw", capture_observation_fn=capture,
            rounds=0, confirmations=3, thermal_rebases=0,
            group_order=("coordinate", "rendering"),
            start_budget=HsiStartBudget(limits, start_index=0),
        )
        self.assertEqual(len(confirmation_phases), 6)
        self.assertEqual([item["captured_count"] for item in result["confirmation_attempts"]], [3, 3])
        self.assertTrue(all(not item["partial_group"] for item in result["confirmation_attempts"]))

    def test_never_feasible_runs_final_best_valid_confirmation_group(self):
        calls = []

        def capture(command, *, phase, settled_confirmation):
            calls.append((phase, settled_confirmation))
            return {
                "residuals": {"coordinate": [2.0, 2.0], "rendering": [0.0, 0.0]},
                "objective": {
                    "kind": "ray_hsi_policy_v2_lexicographic", "feasible": False,
                    "hue_defined": True, "hue_error_degrees": 2.0,
                    "sat_error_percent": 2.0, "coordinate_guarded_limit": 1.0,
                    "coordinate_guarded_excess": 1.0,
                    "color_rendering_residual": {"whitened_score": 0.0},
                    "command_continuity_l1": 0.0,
                },
            }

        result = run_hsi_feedback(
            initial_command={"cw": 4095, "ww": 1000, "r": 1000, "g": 1000, "b": 1000},
            active_channel="cw", capture_observation_fn=capture,
            rounds=0, confirmations=3, thermal_rebases=0,
            group_order=("coordinate", "rendering"),
        )
        self.assertEqual(result["confirmation_attempts"][0]["verification_kind"], "final_best_valid")
        self.assertEqual(result["confirmation_attempts"][0]["captured_count"], 3)
        self.assertEqual(sum(settled for _phase, settled in calls), 3)

    def test_partial_confirmation_measurement_rejection_is_retained_and_stops(self):
        settled_count = 0

        def capture(command, *, phase, settled_confirmation):
            nonlocal settled_count
            if settled_confirmation:
                settled_count += 1
                if settled_count == 2:
                    return {"measurement_rejected": True, "rejection_evidence": {"reason": "weak_signal"}}
            return {
                "residuals": {"coordinate": [0.0, 0.0], "rendering": [0.0, 0.0]},
                "objective": {
                    "kind": "ray_hsi_policy_v2_lexicographic", "feasible": True,
                    "hue_defined": True, "hue_error_degrees": 0.0,
                    "sat_error_percent": 0.0, "coordinate_guarded_limit": 1.0,
                    "coordinate_guarded_excess": 0.0,
                    "color_rendering_residual": {"whitened_score": 0.0},
                    "command_continuity_l1": 0.0,
                },
            }

        result = run_hsi_feedback(
            initial_command={"cw": 4095, "ww": 1000, "r": 1000, "g": 1000, "b": 1000},
            active_channel="cw", capture_observation_fn=capture,
            rounds=0, confirmations=3, thermal_rebases=0,
            group_order=("coordinate", "rendering"),
        )
        self.assertEqual(result["status"], "measurement_unreachable")
        self.assertEqual(len(result["confirmation_attempts"]), 1)
        self.assertEqual(result["confirmation_attempts"][0]["captured_count"], 1)
        self.assertTrue(result["confirmation_attempts"][0]["partial_group"])

    def test_n5_final_verification_collects_exactly_five(self):
        def capture(command, *, phase, settled_confirmation):
            return {
                "residuals": {"coordinate": [2.0, 2.0], "rendering": [0.0, 0.0]},
                "objective": {
                    "kind": "ray_hsi_policy_v2_lexicographic", "feasible": False,
                    "hue_defined": True, "hue_error_degrees": 2.0,
                    "sat_error_percent": 2.0, "coordinate_guarded_limit": 1.0,
                    "coordinate_guarded_excess": 1.0,
                    "color_rendering_residual": {"whitened_score": 0.0},
                    "command_continuity_l1": 0.0,
                },
            }
        result = run_hsi_feedback(
            initial_command={"cw": 4095, "ww": 1000, "r": 1000, "g": 1000, "b": 1000},
            active_channel="cw", capture_observation_fn=capture,
            rounds=0, confirmations=5, thermal_rebases=0,
            group_order=("coordinate", "rendering"),
        )
        self.assertEqual(result["confirmation_attempts"][0]["captured_count"], 5)


if __name__ == "__main__":
    unittest.main()
