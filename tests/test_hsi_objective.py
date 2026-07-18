from __future__ import annotations

import unittest
import json

from camera_based_rgbww_optimizer.measurement.ray_hsi_manifold import RayHsiManifold
from camera_based_rgbww_optimizer.optimization.hsi_objective import (
    GROUP_ORDER,
    HsiRejectedFeaturesError,
    P7_RESULT_STATUSES,
    evaluate_hsi_observation,
    evaluate_hsi_observation_v2,
    hsi_objective_sort_key,
    required_hsi_features_from_report,
)
from camera_based_rgbww_optimizer.measurement import hsi_uncertainty
from camera_based_rgbww_optimizer.measurement.hsi_policy_v2 import HsiPolicyV2, build_waiting_artifact
from camera_based_rgbww_optimizer.optimization.multipatch_solver import (
    estimate_group_jacobians,
    solve_lexicographic_local_step,
)
from tests.test_ray_hsi_manifold import synthetic_manifold


class HsiObjectiveTests(unittest.TestCase):
    def setUp(self):
        self.manifold: RayHsiManifold = synthetic_manifold()
        self.uncertainty = _SyntheticUncertainty()

    def test_exact_target_is_feasible_and_displacement_reports_hue_first(self):
        exact = self.manifold.target_at(120, 50)
        displaced = self.manifold.target_at(123, 54)

        exact_result = evaluate_hsi_observation(self.manifold, exact.features, target_hue=120, target_sat=50, uncertainty_evaluator=self.uncertainty)
        displaced_result = evaluate_hsi_observation(self.manifold, displaced.features, target_hue=120, target_sat=50, uncertainty_evaluator=self.uncertainty)

        self.assertTrue(exact_result["objective"]["feasible"])
        self.assertFalse(displaced_result["objective"]["feasible"])
        self.assertAlmostEqual(displaced_result["objective"]["hue_error_degrees"], 3.0, delta=0.2)
        self.assertAlmostEqual(displaced_result["objective"]["sat_error_percent"], 4.0, delta=0.2)
        self.assertLess(hsi_objective_sort_key(exact_result["objective"]), hsi_objective_sort_key(displaced_result["objective"]))

    def test_joint_guarded_decision_is_the_only_feasibility_gate(self):
        displaced = self.manifold.target_at(180, 100)

        class JointOnlyEvaluator(_SyntheticUncertainty):
            def evaluate(self, manifold, candidate_features, *, target_hue, target_sat):
                result = super().evaluate(
                    manifold,
                    candidate_features,
                    target_hue=target_hue,
                    target_sat=target_sat,
                )
                result.update({"joint_score": 0.5, "feasible": True, "decision": "faithful"})
                return result

        result = evaluate_hsi_observation(
            self.manifold,
            displaced.features,
            target_hue=0,
            target_sat=20,
            uncertainty_evaluator=JointOnlyEvaluator(),
        )

        self.assertGreater(abs(result["objective"]["hue_normalized"]), 1.0)
        self.assertGreater(abs(result["objective"]["sat_normalized"]), 1.0)
        self.assertTrue(result["objective"]["feasible"])

    def test_p7_status_vocabulary_is_exact_and_mutually_exclusive(self):
        self.assertEqual(P7_RESULT_STATUSES, {
            "faithful",
            "unconfirmed",
            "measurement_unreachable",
            "uncertainty_unresolved",
            "solver_budget_exhausted",
            "reference_drift",
            "boundary_bracketed_at_full_scale",
        })

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

        result = evaluate_hsi_observation(self.manifold, target.features, target_hue=240, target_sat=0, uncertainty_evaluator=self.uncertainty)

        self.assertTrue(result["objective"]["feasible"])
        self.assertFalse(result["objective"]["hue_defined"])
        self.assertIsNone(result["objective"]["hue_error_degrees"])
        self.assertEqual(result["residuals"]["hue"], [0.0])

    def test_v2_separates_coordinate_observer_and_rendering_layers(self):
        manifold = RayHsiManifold.load()
        v1 = json.loads(hsi_uncertainty.DEFAULT_OUTPUT.read_text(encoding="utf-8"))
        artifact = build_waiting_artifact(
            feature_ids=manifold.coordinate_feature_ids,
            v1_artifact=v1,
            inputs={"v1": {"sha256": "frozen"}},
        )
        artifact["status"] = "offline_frozen_before_measurement"
        artifact["formal_capture_eligible"] = True
        artifact["coordinate_policy"]["formal_limits"] = {
            "nonzero_exact_node": {"component_scales": [10.0, 10.0], "guarded_limit": 1.0, "unguarded_limit": 2.0},
        }
        artifact["observer_policy"]["formal_limits"] = {
            "nonzero_exact_node": {"guarded_limit": 0.01, "unguarded_limit": 0.02},
        }
        target = manifold.target_at(120, 50)
        values = dict(target.features)
        values[manifold.coordinate_feature_ids[0]] *= 1.1
        result = evaluate_hsi_observation_v2(
            manifold, values,
            target_hue=120, target_sat=50,
            repeatability_class="mid_sat_fullscale",
            policy=HsiPolicyV2(artifact),
        )

        self.assertIn(result["objective"]["hsi_coordinate_equivalent"], {"pass", "unresolved", "fail"})
        self.assertEqual(result["objective"]["observer_equivalent"], "fail")
        self.assertTrue(result["objective"]["color_rendering_residual"]["directional_vector"])
        self.assertEqual(set(result["residuals"]), {"coordinate", "rendering"})

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


class _SyntheticUncertainty:
    def evaluate(self, manifold, candidate_features, *, target_hue, target_sat):
        coordinate = manifold.coordinate(candidate_features, target_hue=target_hue, target_sat=target_sat)
        if target_sat == 0:
            scales = [1.0, 0.01]
            output = [abs(coordinate.sat_error_percent), coordinate.orthogonal_residual]
        else:
            scales = [1.0, 1.0, 0.01]
            output = [abs(coordinate.hue_error_degrees), abs(coordinate.sat_error_percent), coordinate.orthogonal_residual]
        score = max(value / scale for value, scale in zip(output, scales))
        return {
            "artifact_sha256": "synthetic",
            "target_kind": "sat0_exact_node" if target_sat == 0 else "nonzero_exact_node",
            "coverage_limit": 1.5,
            "guarded_acceptance_limit": 1.0,
            "component_scales": scales,
            "diagonal_variance": [1e-4] * len(manifold.coordinate_feature_ids),
            "joint_score": score,
            "output": output,
            "feasible": score <= 1.0,
            "decision": "faithful" if score <= 1.0 else "outside_coverage",
        }


if __name__ == "__main__":
    unittest.main()
