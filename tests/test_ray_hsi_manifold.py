from __future__ import annotations

import math
import unittest

import numpy as np

from camera_based_rgbww_optimizer.measurement.ray_hsi_manifold import RayHsiManifold


class RayHsiManifoldTests(unittest.TestCase):
    def test_periodic_bilinear_target_wraps_hue(self):
        manifold = self._manifold()

        negative = manifold.target_at(-15, 50)
        wrapped = manifold.target_at(345, 50)

        self.assertEqual(negative.features, wrapped.features)
        self.assertEqual(negative.interpolation["hue_nodes"], [330, 0])
        self.assertAlmostEqual(negative.interpolation["hue_fraction"], 0.5)

    def test_coordinate_recovers_local_hue_and_sat_displacement(self):
        manifold = self._manifold()
        candidate = manifold.target_at(121.5, 52.0)

        coordinate = manifold.coordinate(candidate.features, target_hue=120, target_sat=50)

        self.assertAlmostEqual(coordinate.hue_error_degrees, 1.5, delta=0.12)
        self.assertAlmostEqual(coordinate.sat_error_percent, 2.0, delta=0.12)
        self.assertLess(coordinate.orthogonal_residual, 0.001)
        self.assertGreater(coordinate.hue_three_sigma_degrees, 0)
        self.assertGreater(coordinate.sat_three_sigma_percent, 0)

    def test_frozen_real_manifold_loads_and_reports_exact_node(self):
        manifold = RayHsiManifold.load()

        target = manifold.target_at(30, 80)
        coordinate = manifold.coordinate(target.features, target_hue=30, target_sat=80)

        self.assertGreaterEqual(len(target.features), 60)
        self.assertAlmostEqual(coordinate.hue_error_degrees, 0.0, places=6)
        self.assertAlmostEqual(coordinate.sat_error_percent, 0.0, places=6)
        self.assertLess(coordinate.shape_residual, 1e-12)

    @staticmethod
    def _manifold() -> RayHsiManifold:
        return synthetic_manifold()


def synthetic_manifold() -> RayHsiManifold:
    features = [f"f{index}" for index in range(8)]
    zero = np.linspace(1.0, 1.7, len(features))
    zero /= np.linalg.norm(zero)
    nodes = {}
    for hue in range(0, 360, 30):
        phase = math.radians(hue)
        endpoint = zero + np.asarray([
            0.35 * math.cos(phase + index * 0.2) + 0.2 * math.sin(phase + index * 0.1)
            for index in range(len(features))
        ])
        for sat in (5, 20, 50, 80, 95, 100):
            fraction = sat / 100.0
            vector = (1.0 - fraction) * zero + fraction * endpoint
            nodes[(hue, sat)] = {feature: float(vector[index]) for index, feature in enumerate(features)}
    return RayHsiManifold(
        config={"status": "synthetic"},
        nodes=nodes,
        zero_direction={feature: float(zero[index]) for index, feature in enumerate(features)},
        zero_scales={hue: 1.0 for hue in (0, 60, 120, 180, 240, 300)},
        repeatability_three_sigma=0.001,
    )


if __name__ == "__main__":
    unittest.main()
