from __future__ import annotations

import signal
import unittest
from unittest import mock
import copy
import json
import os
import tempfile

import numpy as np

from camera_based_rgbww_optimizer.measurement import hsi_uncertainty as subject
from camera_based_rgbww_optimizer.measurement.ray_hsi_manifold import RayHsiManifold
from tests.test_ray_hsi_manifold import synthetic_manifold


FEATURE_IDS = tuple(
    f"block_{index:02d}::{plane}"
    for index in (2, 3)
    for plane in subject.PLANES
)


class HsiUncertaintyTests(unittest.TestCase):
    def test_termination_signal_enters_keyboard_interrupt_cleanup_path(self):
        with self.assertRaisesRegex(KeyboardInterrupt, "SIGTERM"):
            subject._interrupt_on_signal(signal.SIGTERM, None)

    def test_main_sigterm_records_interrupted_run_and_python_safety(self):
        def terminate(**_kwargs):
            os.kill(os.getpid(), signal.SIGTERM)

        with tempfile.TemporaryDirectory(dir=subject.PROJECT_ROOT / "tmp") as temporary:
            evidence_dir = subject.Path(temporary) / "evidence"
            output = subject.Path(temporary) / "artifact.json"
            with mock.patch.object(subject, "generate_uncertainty_artifact", side_effect=terminate):
                with self.assertRaisesRegex(KeyboardInterrupt, "SIGTERM"):
                    subject.main([
                        "--output", str(output),
                        "--evidence-dir", str(evidence_dir),
                    ])

            run = json.loads((evidence_dir / "run.json").read_text(encoding="utf-8"))
            safety = json.loads((evidence_dir / "all-off-python.json").read_text(encoding="utf-8"))
            self.assertEqual(run["status"], "interrupted")
            self.assertIsNotNone(run["finished_at"])
            self.assertEqual(safety["status"], "safe_by_device_isolation")
            self.assertFalse(safety["sources_touched"])

    def test_real_frozen_artifact_passes_structural_validation(self):
        manifold = RayHsiManifold.load()
        artifact = json.loads(subject.DEFAULT_OUTPUT.read_text(encoding="utf-8"))

        result = subject.validate_uncertainty_artifact(
            artifact,
            expected_feature_ids=manifold.coordinate_feature_ids,
        )

        self.assertEqual(result["status"], "pass")
        self.assertTrue(all(item["passed"] for item in result["checks"]))

    def test_validation_rejects_guarded_limit_above_coverage(self):
        manifold = RayHsiManifold.load()
        artifact = json.loads(subject.DEFAULT_OUTPUT.read_text(encoding="utf-8"))
        broken = copy.deepcopy(artifact)
        calibration = broken["joint_calibration"]["nonzero_exact_node"]
        calibration["guarded_acceptance_limit"] = calibration["coverage_limit"] + 1.0

        result = subject.validate_uncertainty_artifact(
            broken,
            expected_feature_ids=manifold.coordinate_feature_ids,
        )

        self.assertEqual(result["status"], "fail")
        joint_check = next(item for item in result["checks"] if item["name"] == "joint_monte_carlo_and_guard_band")
        self.assertFalse(joint_check["passed"])

    def test_real_frozen_inputs_supply_58_features_and_separate_day_groups(self):
        manifold = RayHsiManifold.load()

        ray = subject.load_ray_repeat_groups(manifold)
        strip = subject.load_strip_repeat_groups(manifold.coordinate_feature_ids)

        self.assertEqual(len(manifold.coordinate_feature_ids), 58)
        self.assertEqual(len(ray), 12)
        self.assertEqual(len(strip), 2)
        self.assertTrue(all(len(rows) >= 2 for rows in ray.values()))
        self.assertEqual([len(rows) for rows in strip.values()], [5, 5])

    def test_regularization_is_positive_deterministic_and_plane_isotropic(self):
        base = np.linspace(0.1, 0.8, len(FEATURE_IDS))
        groups = {
            "day-a": [(base + offset).tolist() for offset in (0.0, 0.01, -0.01)],
            "day-b": [(base + offset).tolist() for offset in (0.0, 0.02, -0.02)],
        }

        first = subject.regularize_groups(groups, FEATURE_IDS)
        second = subject.regularize_groups(groups, FEATURE_IDS)

        self.assertEqual(first, second)
        diagonal = np.asarray(first["diagonal_variance"])
        self.assertTrue(np.all(diagonal > 0.0))
        for plane in subject.PLANES:
            values = [diagonal[index] for index, feature in enumerate(FEATURE_IDS) if feature.endswith(f"::{plane}")]
            self.assertEqual(len(set(values)), 1)

    def test_regularization_rejects_low_group_count(self):
        with self.assertRaisesRegex(ValueError, "at least two independent groups"):
            subject.regularize_groups({"only": [[1.0] * len(FEATURE_IDS), [1.1] * len(FEATURE_IDS)]}, FEATURE_IDS)

    def test_regularization_centers_each_natural_day_before_pooling(self):
        shape = np.linspace(0.1, 0.8, len(FEATURE_IDS))
        offsets = (-0.01, 0.0, 0.01)
        centered_days = {
            "day-a": [(shape + offset).tolist() for offset in offsets],
            "day-b": [(shape + offset).tolist() for offset in offsets],
        }
        shifted_days = {
            "day-a": centered_days["day-a"],
            "day-b": [(shape + 100.0 + offset).tolist() for offset in offsets],
        }

        centered = subject.regularize_groups(centered_days, FEATURE_IDS)
        shifted = subject.regularize_groups(shifted_days, FEATURE_IDS)

        np.testing.assert_allclose(
            centered["diagonal_variance"],
            shifted["diagonal_variance"],
            rtol=1e-10,
            atol=1e-14,
        )

    def test_interpolation_cv_separates_regular_and_high_curvature(self):
        groups = subject.build_interpolation_groups(RayHsiManifold.load())

        self.assertEqual(set(groups), {"regular", "high_curvature"})
        self.assertGreaterEqual(len(groups["regular"]), 2)
        self.assertGreaterEqual(len(groups["high_curvature"]), 2)
        self.assertNotEqual(groups["regular"], groups["high_curvature"])

    def test_target_kind_distinguishes_exact_regular_and_high_curvature(self):
        manifold = synthetic_manifold()

        self.assertEqual(subject.target_kind(manifold, 0, 0), "sat0_exact_node")
        self.assertEqual(subject.target_kind(manifold, 120, 50), "nonzero_exact_node")
        self.assertEqual(subject.target_kind(manifold, 150, 35), "nonzero_regular_interpolation")
        self.assertEqual(subject.target_kind(manifold, 345, 50), "nonzero_high_curvature_interpolation")

    def test_joint_calibration_uses_fixed_seed_and_requires_three_stable_batches(self):
        manifold = synthetic_manifold()

        def stable_outputs(_manifold, *, sample_count, **_kwargs):
            row = np.asarray([0.5, 0.75, 1.0])
            return np.tile(row, (sample_count, 1))

        with mock.patch.object(subject, "_null_outputs", side_effect=stable_outputs):
            first = subject.calibrate_joint_region(
                manifold,
                target_hue=120,
                target_sat=50,
                diagonal_variance=[1e-6] * 8,
                seed=7,
                batch_size=10,
                minimum_samples=20,
                maximum_samples=50,
                convergence_relative=0.01,
            )
            second = subject.calibrate_joint_region(
                manifold,
                target_hue=120,
                target_sat=50,
                diagonal_variance=[1e-6] * 8,
                seed=7,
                batch_size=10,
                minimum_samples=20,
                maximum_samples=50,
                convergence_relative=0.01,
            )

        self.assertEqual(first, second)
        self.assertEqual(first["monte_carlo"]["consecutive_stable_batches"], 3)
        self.assertEqual(first["monte_carlo"]["sample_count"], 40)

    def test_sat0_joint_evaluation_has_no_hue_dimension(self):
        manifold = synthetic_manifold()
        target = manifold.target_at(240, 0)

        result = subject.evaluate_joint(
            manifold,
            target.features,
            target_hue=240,
            target_sat=0,
            scales=[1.0, 1.0],
        )

        self.assertEqual(len(result["output"]), 2)
        self.assertEqual(result["output"], [0.0, 0.0])


if __name__ == "__main__":
    unittest.main()
