import unittest

import numpy as np

import json
from pathlib import Path

from camera_based_rgbww_optimizer.measurement.chart_basis_validation import predict_piecewise_basis
from camera_based_rgbww_optimizer.optimization.multipatch_solver import (
    solve_lexicographic_local_step,
    solve_piecewise_basis_seed,
)


class MultipatchSolverTests(unittest.TestCase):
    def test_keeps_active_channel_at_max_and_respects_step_bounds(self):
        residuals = {group: np.asarray([1.0]) for group in ("neutral", "white", "training", "holdout")}
        jacobians = {group: np.asarray([[-2.0, 0.0, 0.0, 0.0]]) for group in residuals}

        def objective(predicted, _command):
            value = abs(float(predicted["neutral"][0]))
            return {"rank_key": [0, value, 0, 0, value, value, value, value, value, value, 0]}

        result = solve_lexicographic_local_step(
            {"cw": 4095, "ww": 0, "r": 0, "g": 0, "b": 0}, residuals, jacobians,
            active_channel="cw", objective_fn=objective, max_step_code=512,
        )
        self.assertEqual(result["command"]["cw"], 4095)
        self.assertLessEqual(max(abs(value) for value in result["delta_codes"].values()), 512)
        self.assertGreater(result["candidate_count"], 1)

    def test_neutral_rank_wins_over_training(self):
        residuals = {
            "neutral": np.asarray([0.1]), "white": np.asarray([0.0]),
            "training": np.asarray([1.0]), "holdout": np.asarray([1.0]),
        }
        jacobians = {
            "neutral": np.asarray([[1.0, 0.0, 0.0, 0.0]]),
            "white": np.zeros((1, 4)),
            "training": np.asarray([[-10.0, 0.0, 0.0, 0.0]]),
            "holdout": np.asarray([[-10.0, 0.0, 0.0, 0.0]]),
        }

        def objective(predicted, _command):
            neutral = abs(float(predicted["neutral"][0]))
            training = abs(float(predicted["training"][0]))
            return {"rank_key": [0 if neutral <= 0.1 else 1, neutral, 0, 0, training, training, training, training, training, training, 0]}

        result = solve_lexicographic_local_step(
            {"cw": 4095, "ww": 2048, "r": 2048, "g": 2048, "b": 2048},
            residuals, jacobians, active_channel="cw", objective_fn=objective,
        )
        self.assertLessEqual(abs(result["predicted_residuals"]["neutral"][0]), 0.1)

    def test_piecewise_basis_is_seed_only_and_keeps_a_channel_at_max(self):
        path = Path(
            "/Volumes/4T/temp/rgbww-optimizer/chart-response-basis/"
            "p2-five-channel-basis-20260716-005935/basis-analysis.json"
        )
        basis = json.loads(path.read_text(encoding="utf-8"))
        expected = {"cw": 4095, "ww": 2200, "r": 600, "g": 900, "b": 300}
        prediction = predict_piecewise_basis(basis, expected)["values"]
        target = dict(zip(basis["feature_order"], prediction))
        seed = solve_piecewise_basis_seed(
            basis,
            target,
            feature_ids=basis["feature_order"],
            initial_command={channel: 2048 for channel in ("cw", "ww", "r", "g", "b")},
            refinement_steps=(1024, 512, 256),
        )
        self.assertEqual(max(seed["best"]["command"].values()), 4095)
        self.assertLess(seed["best"]["predicted_relative_rmse"], 0.1)
        self.assertEqual(seed["kind"], "p2_piecewise_basis_seed_only")
