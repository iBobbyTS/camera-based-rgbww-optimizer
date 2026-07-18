from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

import numpy as np

from camera_based_rgbww_optimizer.measurement import hsi_policy_v2 as subject
from camera_based_rgbww_optimizer.measurement import hsi_uncertainty
from camera_based_rgbww_optimizer.measurement.ray_hsi_manifold import RayHsiManifold


class HsiPolicyV2Tests(unittest.TestCase):
    def setUp(self):
        self.manifold = RayHsiManifold.load()
        self.features = self.manifold.coordinate_feature_ids
        self.variance = [1e-4] * len(self.features)

    def test_sat100_uses_signed_unclipped_one_sided_tangent(self):
        target = self.manifold.target_at(120, 100)
        below = self.manifold.target_at(120, 95)
        target_unit = subject.ordered_unit_shape(target.features, self.features)
        below_unit = subject.ordered_unit_shape(below.features, self.features)
        beyond = target_unit + (target_unit - below_unit)
        result = subject.local_tangent_evaluate(
            self.manifold,
            dict(zip(self.features, beyond, strict=True)),
            target_hue=120,
            target_sat=100,
            diagonal_variance=self.variance,
        )

        self.assertEqual(result["status"], "evaluated")
        self.assertGreater(result["sat_error_percent"], 0.0)
        self.assertTrue(result["signed_unclipped"])
        self.assertEqual(
            result["tangent_provenance"]["sat"]["kind"],
            "one_sided_endpoint_signed_unclipped",
        )

    def test_degenerate_required_scale_hard_fails_without_floor(self):
        with self.assertRaisesRegex(ValueError, "unidentifiable"):
            subject.calibrate_component_scales([[0.0, 1.0], [0.0, -1.0]])

    def test_sat0_never_has_hue_gate(self):
        target = self.manifold.target_at(240, 0)
        result = subject.local_tangent_evaluate(
            self.manifold, target.features,
            target_hue=240, target_sat=0,
            diagonal_variance=self.variance,
        )
        self.assertFalse(result["hue_defined"])
        self.assertNotIn("hue_error_degrees", result)
        self.assertIsNone(result["tangent_provenance"]["hue"])

    def test_hue_zero_and_360_use_identical_periodic_tangent(self):
        target = self.manifold.target_at(0, 50)
        zero = subject.local_tangent_evaluate(
            self.manifold, target.features,
            target_hue=0, target_sat=50,
            diagonal_variance=self.variance,
        )
        wrapped = subject.local_tangent_evaluate(
            self.manifold, target.features,
            target_hue=360, target_sat=50,
            diagonal_variance=self.variance,
        )
        self.assertEqual(zero["tangent_provenance"], wrapped["tangent_provenance"])
        self.assertAlmostEqual(zero["hue_error_degrees"], wrapped["hue_error_degrees"])

    def test_mean_difference_covariance_scales_each_block_by_one_over_n(self):
        left = [4.0] * len(self.features)
        right = [6.0] * len(self.features)
        covariance = subject.mean_difference_covariance(
            left, 2, right, 3, self.features,
        )
        np.testing.assert_allclose(covariance, np.full(len(self.features), 4.0))

    def test_reference_evaluator_excludes_strip_and_preserves_center_shift(self):
        center = np.linspace(0.1, 0.8, len(self.features))
        shifted = center.copy()
        shifted[0] += 0.2
        result = subject.evaluate_reference_difference(
            center, shifted,
            left_variance=self.variance, left_count=5,
            right_variance=self.variance, right_count=5,
            feature_ids=self.features,
            guarded_limit=1.0, unguarded_limit=2.0,
            statistic="reference_center_compatibility",
        )
        self.assertEqual(result["decision"], "fail")
        self.assertTrue(result["reference_drift"])
        self.assertFalse(result["strip_covariance_included"])

    def test_within_block_covariance_centers_each_block_and_keeps_center_shift_separate(self):
        base = self.manifold.target_at(120, 50).features
        first = []
        shifted = []
        for offset in (-1e-4, 0.0, 1e-4):
            sample = {key: value + offset for key, value in base.items()}
            first.append(sample)
            shifted.append({key: value + 10.0 for key, value in sample.items()})
        left = subject.summarize_within_block(first, self.features)
        right = subject.summarize_within_block(shifted, self.features)
        self.assertTrue(left["centered_within_block"])
        self.assertFalse(left["cross_session_shift_absorbed"])
        self.assertNotEqual(left["center"], right["center"])
        self.assertTrue(all(value > 0.0 for value in left["diagonal_variance"]))
        self.assertTrue(all(value > 0.0 for value in right["diagonal_variance"]))

    def test_reference_pass_unresolved_and_fail_are_distinct(self):
        self.assertEqual(subject.classify_region(0.9, guarded_limit=1, unguarded_limit=2), "pass")
        self.assertEqual(subject.classify_region(1.5, guarded_limit=1, unguarded_limit=2), "unresolved")
        self.assertEqual(subject.classify_region(2.1, guarded_limit=1, unguarded_limit=2), "fail")

    def test_direct_pairwise_spread_supports_n3_n5_and_four_routes(self):
        center = self.manifold.target_at(120, 50).features
        for count in (3, 5):
            for class_name in subject.REPEATABILITY_CLASSES:
                result = subject.evaluate_confirmation_spread(
                    [center] * count,
                    feature_ids=self.features,
                    class_name=class_name,
                    class_variance=self.variance,
                    limit=None,
                )
                self.assertEqual(result["confirmation_count"], count)
                self.assertEqual(result["group_maximum_score"], 0.0)
                self.assertEqual(result["decision"], subject.WAITING_STATUS)

    def test_p1_floor_can_only_be_kept_or_increased_per_plane(self):
        lower = [5e-5] * len(self.features)
        higher = [2e-4] * len(self.features)
        result = subject.conservative_class_variance(self.variance, lower, self.features)
        np.testing.assert_allclose(result, self.variance)
        result = subject.conservative_class_variance(self.variance, higher, self.features)
        np.testing.assert_allclose(result, higher)

    def test_coordinate_and_observer_layers_can_diverge_without_losing_residual(self):
        target = self.manifold.target_at(120, 50)
        target_unit = subject.ordered_unit_shape(target.features, self.features)
        tangent_result = subject.local_tangent_evaluate(
            self.manifold, target.features,
            target_hue=120, target_sat=50,
            diagonal_variance=self.variance,
        )
        orthogonal = np.asarray(tangent_result["directional_orthogonal_residual"])
        self.assertEqual(float(np.linalg.norm(orthogonal)), 0.0)

        candidate = target_unit.copy()
        candidate[0] += 0.1
        result = subject.local_tangent_evaluate(
            self.manifold,
            dict(zip(self.features, candidate, strict=True)),
            target_hue=120, target_sat=50,
            diagonal_variance=self.variance,
        )
        self.assertIn("hue_error_degrees", result)
        self.assertGreater(result["observer_whitened_score"], 0.0)
        self.assertGreater(result["color_rendering_residual"]["raw_l2"], 0.0)
        self.assertTrue(result["color_rendering_residual"]["directional_vector"])

    def test_waiting_artifact_cannot_be_used_for_formal_capture(self):
        real_manifold = RayHsiManifold.load()
        v1 = json.loads(hsi_uncertainty.DEFAULT_OUTPUT.read_text(encoding="utf-8"))
        artifact = subject.build_waiting_artifact(
            feature_ids=real_manifold.coordinate_feature_ids,
            v1_artifact=v1,
            inputs={"v1": {"sha256": "frozen"}},
        )
        self.assertEqual(artifact["status"], subject.WAITING_STATUS)
        self.assertFalse(artifact["formal_capture_eligible"])
        self.assertIsNone(artifact["repeatability_policy"]["classes"]["sat100_fullscale"]["limits"]["3"])
        with tempfile.TemporaryDirectory() as tempdir:
            path = subject.write_policy_v2(Path(tempdir) / "policy.json", artifact)
            self.assertFalse(subject.HsiPolicyV2.load(path).formal_capture_eligible)

    def test_local_tangent_condition_limit_fails_closed(self):
        target = self.manifold.target_at(120, 50)
        result = subject.local_tangent_evaluate(
            self.manifold, target.features,
            target_hue=120, target_sat=50,
            diagonal_variance=self.variance,
            condition_limit=1.0,
        )
        self.assertEqual(result["status"], "uncertainty_unresolved")

    def test_joint_coordinate_reference_and_observer_coverage_are_reported_separately(self):
        report = subject.calibrate_joint_regions(
            self.manifold,
            target_hue=120,
            target_sat=100,
            diagonal_variance=self.variance,
            seed=7,
            samples=3000,
            bootstrap_replicates=100,
        )
        self.assertEqual(report["status"], "pass")
        self.assertEqual(len(report["component_scales"]), 2)
        self.assertIn("coordinate_unguarded", report["empirical_coverage"])
        self.assertIn("observer_unguarded", report["empirical_coverage"])
        self.assertTrue(report["noise_components_counted_once"])
        self.assertLessEqual(
            report["coordinate_region"]["guarded_limit"],
            report["coordinate_region"]["unguarded_limit"],
        )

    def test_robust_group_audit_freezes_nonfinite_shortage_and_outlier_branches(self):
        base = subject.ordered_unit_shape(self.manifold.target_at(120, 50).features, self.features)
        good = {
            "A": [(base + index * 1e-6).tolist() for index in range(5)],
            "B": [(base - index * 1e-6).tolist() for index in range(5)],
        }
        passed = subject.audit_repeatability_groups(good, self.features)
        self.assertIn("thresholds", passed)
        broken = {"A": [list(row) for row in good["A"][:2]], "B": [list(row) for row in good["B"][:2]]}
        broken["B"][0][0] = float("nan")
        failed = subject.audit_repeatability_groups(broken, self.features)
        branches = {item["branch"] for item in failed["failure_branches"]}
        self.assertEqual(failed["status"], "uncertainty_unresolved")
        self.assertIn("nonfinite_feature", branches)
        self.assertIn("effective_sample_shortage", branches)
        branch_cases = {
            "trend": {"trend_whitened_limit": 0.0, "bimodal_gap_sigma_limit": 1e9, "maximum_single_frame_variance_fraction": 1.0},
            "bimodal": {"trend_whitened_limit": 1e9, "bimodal_gap_sigma_limit": 0.0, "maximum_single_frame_variance_fraction": 1.0},
            "single_outlier_dominates_variance": {"trend_whitened_limit": 1e9, "bimodal_gap_sigma_limit": 1e9, "maximum_single_frame_variance_fraction": 0.0},
        }
        for expected, overrides in branch_cases.items():
            thresholds = {**subject.AUDIT_THRESHOLDS, **overrides}
            result = subject.audit_repeatability_groups(good, self.features, thresholds=thresholds)
            self.assertIn(expected, {item["branch"] for item in result["failure_branches"]})

    def test_distinct_stable_command_centers_do_not_create_false_trend(self):
        first = subject.ordered_unit_shape(self.manifold.target_at(120, 100).features, self.features)
        second = subject.ordered_unit_shape(self.manifold.target_at(300, 100).features, self.features)
        offsets = (-1e-5, 1e-5, 0.0, 1e-5, -1e-5)
        groups = {
            "h120-s100:A": [(first + offset).tolist() for offset in offsets],
            "h300-s100:A": [(second + offset).tolist() for offset in offsets],
        }
        result = subject.audit_repeatability_groups(groups, self.features)
        self.assertEqual(result["status"], "pass")
        self.assertLess(result["metrics"]["trend_whitened_score"], subject.AUDIT_THRESHOLDS["trend_whitened_limit"])
        self.assertEqual(result["residual_semantics"], "chronological_within_state_command_block_centered")

    def test_real_within_command_trend_bimodality_and_single_dominance_hit_frozen_thresholds(self):
        base = subject.ordered_unit_shape(self.manifold.target_at(120, 50).features, self.features)
        groups = {
            "command:A": [(base + value * 1e-4).tolist() for value in (0.0, 0.001, -0.001, 0.002, 10.0)],
            "command:B": [(base + value * 1e-4).tolist() for value in (0.0, 0.001, -0.001, 0.002, -0.002)],
        }
        result = subject.audit_repeatability_groups(groups, self.features)
        branches = {item["branch"] for item in result["failure_branches"]}
        self.assertEqual(result["status"], "uncertainty_unresolved")
        self.assertTrue({"trend", "bimodal", "single_outlier_dominates_variance"}.issubset(branches))

    def test_bootstrap_instability_fails_closed(self):
        region = subject._bootstrap_guarded_region(
            np.asarray([0.0] * 999 + [100.0]),
            rng=np.random.default_rng(3),
            replicates=100,
            maximum_relative_span=0.01,
        )
        self.assertEqual(region["status"], "uncertainty_unresolved")


if __name__ == "__main__":
    unittest.main()
