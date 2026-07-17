import unittest

import numpy as np

from camera_based_rgbww_optimizer.optimization.bounded_least_squares import (
    solve_box_constrained_least_squares,
)


class BoundedLeastSquaresTests(unittest.TestCase):
    def test_finds_interior_solution(self):
        result = solve_box_constrained_least_squares(np.eye(2), [0.25, 0.75], [0, 0], [1, 1])
        np.testing.assert_allclose(result, [0.25, 0.75])

    def test_uses_active_bound_instead_of_post_solve_clipping(self):
        matrix = np.asarray([[1.0, 1.0], [0.0, 1.0]])
        result = solve_box_constrained_least_squares(matrix, [2.0, 0.2], [0, 0], [1, 1])
        np.testing.assert_allclose(result, [1.0, 0.6])

    def test_rejects_invalid_bounds(self):
        with self.assertRaisesRegex(ValueError, "must not exceed"):
            solve_box_constrained_least_squares([[1.0]], [1.0], [2.0], [1.0])
