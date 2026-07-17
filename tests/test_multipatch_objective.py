import unittest

from camera_based_rgbww_optimizer.optimization.multipatch_objective import (
    build_residual_groups,
    evaluate_multipatch_objective,
    observation_from_raw_report,
    RejectedOptimizationFeaturesError,
    objective_sort_key,
    repeatability_neutral_tolerance,
    validate_feature_split,
)


def features(blocks):
    return [f"block_{block:02d}::{plane}" for block in blocks for plane in ("R", "G1", "G2", "B")]


class MultipatchObjectiveTests(unittest.TestCase):
    def _report(self):
        patches = []
        for block in range(1, 25):
            patches.append({
                "name": f"block_{block:02d}",
                "optimization_eligible": block != 1,
                "planes": {
                    plane: {
                        "ambient_subtracted": {"trimmed_mean_per_second": float(block + index + 1)},
                        "quality": {"status": "accepted"},
                        "metrics": {
                            "valid_pixel_count": 30000, "nonfinite_fraction": 0.0,
                            "clipped_fraction": 0.0, "near_noise_floor_fraction": 0.0,
                        },
                    }
                    for index, plane in enumerate(("R", "G1", "G2", "B"))
                },
            })
        return {
            "schema_version": 1,
            "measurement": "native_bayer_patch_statistics",
            "source": {"path": "capture.cr3"},
            "location_config": {"sha256": "location"},
            "mosaic": {"plane_order": ["R", "G1", "G2", "B"]},
            "analysis_context": {},
            "observer_config": {
                "quality_thresholds": {
                    "minimum_valid_pixels_per_plane": 29000,
                    "maximum_nonfinite_fraction": 0.0,
                    "maximum_clipped_fraction": 0.0,
                    "maximum_near_noise_floor_fraction": 0.05,
                }
            },
            "patches": patches,
        }

    def test_split_requires_disjoint_complete_four_plane_blocks(self):
        split = validate_feature_split(
            features([2, 7, 8]), neutral_blocks=[2], training_blocks=[7], holdout_blocks=[8]
        )
        self.assertEqual(len(split["neutral"]), 4)
        with self.assertRaisesRegex(ValueError, "disjoint"):
            validate_feature_split(features([2, 7]), neutral_blocks=[2], training_blocks=[2], holdout_blocks=[7])

    def test_lexicographic_hard_gate_cannot_be_bought_by_color_improvement(self):
        split = {"neutral": features([2]), "training": features([7]), "holdout": features([8])}
        target = {feature: 1.0 for feature in features([2, 7, 8])}
        feasible = dict(target)
        feasible.update({feature: 1.2 for feature in features([7, 8])})
        infeasible = dict(target)
        infeasible["block_02::R"] = 1.2
        white = {"goal_score": 0.5, "within_goal": True}
        first = evaluate_multipatch_objective(
            feasible, target, feature_split=split, neutral_blocks=[2], neutral_chroma_tolerance=0.05,
            white_point_comparison=white,
        )
        second = evaluate_multipatch_objective(
            infeasible, target, feature_split=split, neutral_blocks=[2], neutral_chroma_tolerance=0.05,
            white_point_comparison=white,
        )
        self.assertTrue(first["feasible"])
        self.assertFalse(second["feasible"])
        self.assertLess(objective_sort_key(first), objective_sort_key(second))

    def test_global_scale_removes_brightness_difference(self):
        split = {"neutral": features([2]), "training": features([7]), "holdout": features([8])}
        target = {feature: float(index + 1) for index, feature in enumerate(features([2, 7, 8]))}
        candidate = {feature: value * 0.5 for feature, value in target.items()}
        objective = evaluate_multipatch_objective(
            candidate, target, feature_split=split, neutral_blocks=[2], neutral_chroma_tolerance=0.01,
            white_point_comparison={"goal_score": 0.1, "within_goal": True},
        )
        self.assertAlmostEqual(objective["global_brightness_scale"], 2.0)
        self.assertAlmostEqual(objective["training"]["maximum"], 0.0)

    def test_native_report_observation_uses_four_planes_and_white_block(self):
        observation = observation_from_raw_report(
            self._report(), raw_file="capture.cr3", matrix_loader=lambda _path: __import__("numpy").eye(3)
        )
        self.assertEqual(len(observation["feature_values"]), 92)
        self.assertEqual(observation["white_point"]["block"], 6)
        self.assertEqual(observation["plane_order"], ["R", "G1", "G2", "B"])

    def test_native_report_marks_only_near_noise_rejection_as_reacquirable(self):
        report = self._report()
        plane = report["patches"][23]["planes"]["B"]
        plane["quality"]["status"] = "rejected"
        plane["metrics"]["near_noise_floor_fraction"] = 0.071
        with self.assertRaises(RejectedOptimizationFeaturesError) as caught:
            observation_from_raw_report(
                report, raw_file="capture.cr3", matrix_loader=lambda _path: __import__("numpy").eye(3)
            )
        self.assertTrue(caught.exception.weak_signal_only)
        self.assertEqual(caught.exception.rejected[0]["feature_id"], "block_24::B")

    def test_residual_groups_and_repeatability_tolerance_are_explicit(self):
        target = observation_from_raw_report(
            self._report(), raw_file="target.cr3", matrix_loader=lambda _path: __import__("numpy").eye(3)
        )
        candidate = {
            **target,
            "feature_values": {key: value * 0.9 for key, value in target["feature_values"].items()},
        }
        split = validate_feature_split(
            list(target["feature_values"]), neutral_blocks=[2, 3, 4, 5, 6],
            training_blocks=[7, 9, 10, 12, 13, 15, 16, 18, 19, 21, 23],
            holdout_blocks=[8, 11, 14, 17, 20, 22, 24],
        )
        residuals = build_residual_groups(
            candidate, target, feature_split=split, neutral_blocks=[2, 3, 4, 5, 6],
            cct_tolerance_K=25, duv_tolerance=0.0005,
        )
        self.assertEqual(residuals["neutral"].shape, (20,))
        self.assertEqual(residuals["white"].shape, (2,))
        self.assertEqual(residuals["training"].shape, (44,))
        self.assertEqual(residuals["holdout"].shape, (28,))
        tolerance = repeatability_neutral_tolerance(
            [target, candidate], neutral_blocks=[2, 3, 4, 5, 6], absolute_floor=0.002,
        )
        self.assertEqual(tolerance, 0.002)
