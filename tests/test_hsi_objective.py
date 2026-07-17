from __future__ import annotations

import unittest

from camera_based_rgbww_optimizer.measurement.ray_hsi_manifold import RayHsiManifold
from camera_based_rgbww_optimizer.optimization.hsi_objective import (
    GROUP_ORDER,
    HsiRejectedFeaturesError,
    evaluate_hsi_observation,
    hsi_objective_sort_key,
    required_hsi_features_from_report,
)
from camera_based_rgbww_optimizer.optimization.multipatch_solver import (
    estimate_group_jacobians,
    solve_lexicographic_local_step,
)
from tests.test_ray_hsi_manifold import synthetic_manifold


class HsiObjectiveTests(unittest.TestCase):
    def setUp(self):
        self.manifold: RayHsiManifold = synthetic_manifold()

    def test_exact_target_is_feasible_and_displacement_reports_hue_first(self):
        exact = self.manifold.target_at(120, 50)
        displaced = self.manifold.target_at(123, 54)

        exact_result = evaluate_hsi_observation(self.manifold, exact.features, target_hue=120, target_sat=50)
        displaced_result = evaluate_hsi_observation(self.manifold, displaced.features, target_hue=120, target_sat=50)

        self.assertTrue(exact_result["objective"]["feasible"])
        self.assertFalse(displaced_result["objective"]["feasible"])
        self.assertAlmostEqual(displaced_result["objective"]["hue_error_degrees"], 3.0, delta=0.2)
        self.assertAlmostEqual(displaced_result["objective"]["sat_error_percent"], 4.0, delta=0.2)
        self.assertLess(hsi_objective_sort_key(exact_result["objective"]), hsi_objective_sort_key(displaced_result["objective"]))

    def test_generic_local_solver_accepts_hsi_group_order(self):
        command = {"cw": 4095, "ww": 1500, "r": 1500, "g": 1500, "b": 1500}
        base = {"hue": [2.0], "sat": [-1.0], "shape": [0.5, -0.25]}
        probes = {
            "ww": {"hue": [1.0], "sat": [-1.0], "shape": [0.5, -0.25]},
            "r": {"hue": [2.0], "sat": [0.0], "shape": [0.5, -0.25]},
            "g": {"hue": [2.0], "sat": [-1.0], "shape": [0.0, -0.25]},
            "b": {"hue": [2.0], "sat": [-1.0], "shape": [0.5, 0.0]},
        }
        deltas = {"ww": 256, "r": 256, "g": 256, "b": 256}
        jacobians = estimate_group_jacobians(base, probes, deltas, active_channel="cw", group_order=GROUP_ORDER)

        def objective(predicted, proposed):
            return {
                "feasible": False,
                "hue_normalized": float(predicted["hue"][0]),
                "sat_normalized": float(predicted["sat"][0]),
                "orthogonal_normalized": float(abs(predicted["shape"][0])),
                "shape_normalized_p90": float(max(abs(predicted["shape"]))),
                "shape_normalized_maximum": float(max(abs(predicted["shape"]))),
                "command_continuity_l1": 0.0,
            }

        step = solve_lexicographic_local_step(
            command,
            base,
            jacobians,
            active_channel="cw",
            objective_fn=objective,
            group_order=GROUP_ORDER,
            objective_sort_key_fn=hsi_objective_sort_key,
        )

        self.assertLess(abs(step["predicted_objective"]["hue_normalized"]), 2.0)
        self.assertEqual(step["command"]["cw"], 4095)

    def test_sat0_does_not_invent_a_hue_error(self):
        target = self.manifold.target_at(240, 0)

        result = evaluate_hsi_observation(self.manifold, target.features, target_hue=240, target_sat=0)

        self.assertTrue(result["objective"]["feasible"])
        self.assertFalse(result["objective"]["hue_defined"])
        self.assertIsNone(result["objective"]["hue_error_degrees"])
        self.assertEqual(result["residuals"]["hue"], [0.0])

    def test_required_features_reject_only_frozen_weak_signal(self):
        report = {
            "schema_version": 1,
            "measurement": "native_bayer_patch_statistics",
            "source": {"path": "sample.cr3"},
            "location_config": {"sha256": "location"},
            "mosaic": {"plane_order": ["R", "G1", "G2", "B"]},
            "observer_config": {"quality_thresholds": {"minimum_valid_pixels_per_plane": 10, "maximum_nonfinite_fraction": 0.0, "maximum_clipped_fraction": 0.0, "maximum_near_noise_floor_fraction": 0.05}},
            "patches": [{
                "name": "block_01",
                "optimization_eligible": True,
                "planes": {
                    plane: {
                        "quality": {"status": "rejected" if plane == "B" else "accepted"},
                        "metrics": {"valid_pixel_count": 20, "nonfinite_fraction": 0.0, "clipped_fraction": 0.0, "near_noise_floor_fraction": 0.2 if plane == "B" else 0.0},
                        "ambient_subtracted": {"trimmed_mean_per_second": 1.0},
                    }
                    for plane in ("R", "G1", "G2", "B")
                },
            }],
        }

        with self.assertRaises(HsiRejectedFeaturesError) as raised:
            required_hsi_features_from_report(report, ["block_01::R", "block_01::B"])

        self.assertTrue(raised.exception.weak_signal_only)


if __name__ == "__main__":
    unittest.main()
