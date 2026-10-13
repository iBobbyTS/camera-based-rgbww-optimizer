"""Behavior tests for the GUIDE13 offline-correction owners.

Every expected value below is derived independently (hand arithmetic,
closed-form Student-t inversion for df=2, or frozen advisor audit
numbers) - never by calling the function under test.
"""
from __future__ import annotations

import math
import unittest

from camera_based_rgbww_optimizer.optimization import guide13


class LayeredQualityTests(unittest.TestCase):
    @staticmethod
    def _stats(plane_status: dict[str, str], nps: float = 100.0) -> dict:
        return {
            "patches": [
                {"index": 6, "planes": {
                    plane: {
                        "quality": {"status": status},
                        "statistics": {"normalized_per_second": {
                            "trimmed_mean": nps}},
                    } for plane, status in plane_status.items()
                }},
            ],
        }

    def test_primary_valid_but_secondary58_failed_frame_is_legal_primary(self):
        # the GUIDE13 recovery class: block_06 four planes accepted while
        # the 58-feature global gate said near_noise_only (C12-2's 10
        # deep-color candidates)
        stats = self._stats({p: "accepted" for p in guide13.PRIMARY_PLANES})
        row = {"capture": {"direct_quality": {"status": "near_noise_only"}}}
        layered = guide13.primary_layer_from_stats(stats)
        self.assertEqual(layered["primary_quality"], "accepted")
        self.assertEqual(
            guide13.secondary58_from_capture(row), "near_noise_only")

    def test_primary_real_failure_is_not_cured_by_secondary_pass(self):
        # opposite counterexample: one main-block plane genuinely
        # rejected - the frame stays a primary rejection even if the
        # global gate had passed it
        stats = self._stats({
            "R": "accepted", "G1": "accepted", "G2": "accepted",
            "B": "rejected",
        })
        row = {"capture": {"direct_quality": {"status": "pass"}}}
        layered = guide13.primary_layer_from_stats(stats)
        self.assertEqual(layered["primary_quality"], "rejected")
        self.assertEqual(layered["planes"]["B"], "rejected")
        self.assertEqual(guide13.secondary58_from_capture(row), "pass")

    def test_nonfinite_or_zero_plane_level_rejects_primary(self):
        stats = {
            "patches": [{"index": 6, "planes": {
                "R": {"quality": {"status": "accepted"},
                      "statistics": {"normalized_per_second": {
                          "trimmed_mean": 0.0}}},
                "G1": {"quality": {"status": "accepted"},
                       "statistics": {"normalized_per_second": {
                           "trimmed_mean": 10.0}}},
                "G2": {"quality": {"status": "accepted"},
                       "statistics": {"normalized_per_second": {
                           "trimmed_mean": 10.0}}},
                "B": {"quality": {"status": "accepted"},
                      "statistics": {"normalized_per_second": {
                          "trimmed_mean": 10.0}}},
            }}],
        }
        self.assertEqual(
            guide13.primary_layer_from_stats(stats)["primary_quality"],
            "rejected")

    def test_z_from_planes_definitions(self):
        z = guide13.z_from_planes(
            {"R": 1000.0, "G1": 1000.0, "G2": 1000.0, "B": 1000.0})
        self.assertEqual(z, (0.0, 0.0))
        z = guide13.z_from_planes(
            {"R": 2000.0, "G1": 1000.0, "G2": 1000.0, "B": 500.0})
        self.assertAlmostEqual(z[0], math.log(2.0), places=12)
        self.assertAlmostEqual(z[1], math.log(0.5), places=12)
        # G is the average of the two green planes
        z = guide13.z_from_planes(
            {"R": 1500.0, "G1": 1000.0, "G2": 2000.0, "B": 1500.0})
        self.assertAlmostEqual(z[0], 0.0, places=12)
        self.assertAlmostEqual(z[1], 0.0, places=12)

    def test_fullscale_from_command_readback(self):
        cmd = {"readback": {"device_snapshot": {
            "cold_white": 100, "warm_white": 200, "red": 4095,
            "green": 50, "blue": 0}}}
        out = guide13.fullscale_from_command(cmd)
        self.assertTrue(out["actual_fullscale"])
        self.assertEqual(out["max_channel"], "r")
        cmd2 = {"readback": {"device_snapshot": {
            "cold_white": 4000, "warm_white": 200, "red": 3000,
            "green": 50, "blue": 0}}}
        self.assertFalse(guide13.fullscale_from_command(cmd2)["actual_fullscale"])
        self.assertFalse(
            guide13.fullscale_from_command({"readback": {}})["actual_fullscale"])


class LocalJacobianTests(unittest.TestCase):
    def test_non_orthogonal_columns_solved_by_matrix_inverse(self):
        # J columns (H direction (1.0, 0.3), S direction (0.2, 1.0)) are
        # clearly non-orthogonal; hand-solved J^-1 dz for dz=(0.5, 0.5):
        # det = 1*1 - 0.2*0.3 = 0.94
        # dH = (1*0.5 - 0.2*0.5)/0.94 = 0.425531914893617
        # dS = (-0.3*0.5 + 1*0.5)/0.94 = 0.372340425531915
        j = guide13.local_jacobian((1.0, 0.3), (0.2, 1.0))
        dH, dS = guide13.solve_local_delta(j, (0.5, 0.5))
        self.assertAlmostEqual(dH, 0.425531914893617, places=12)
        self.assertAlmostEqual(dS, 0.372340425531915, places=12)
        # the 90-degree-rotation pseudo-tangent gives a materially wrong
        # SAT answer for this dz: dz lies exactly along the radial, so
        # the rotation estimate says zero SAT error while the true
        # inverse says 0.372
        n = math.hypot(0.5, 0.5)
        rx, ry = 0.5 / n, 0.5 / n
        tx, ty = -ry, rx
        pseudo_sat = tx * 0.5 + ty * 0.5
        self.assertAlmostEqual(pseudo_sat, 0.0, places=12)
        self.assertGreater(abs(pseudo_sat - dS), 0.3)

    def test_singular_jacobian_raises_never_rotates(self):
        j = guide13.local_jacobian((1.0, 2.0), (2.0, 4.0))  # parallel columns
        with self.assertRaises(ValueError):
            guide13.solve_local_delta(j, (0.1, 0.1))
        with self.assertRaises(ValueError):
            guide13.local_delta_covariance(j, [[1.0, 0.0], [0.0, 1.0]])

    def test_delta_covariance_propagation_matches_hand_computation(self):
        # J = [[2, 0], [0, 1]] (diagonal): J^-1 = diag(0.5, 1); with
        # Cov(dz)=diag(4, 9) the delta covariance is diag(1, 9)
        j = guide13.local_jacobian((2.0, 0.0), (0.0, 1.0))
        cov = guide13.local_delta_covariance(j, [[4.0, 0.0], [0.0, 9.0]])
        self.assertAlmostEqual(cov[0][0], 1.0, places=12)
        self.assertAlmostEqual(cov[1][1], 9.0, places=12)
        self.assertAlmostEqual(cov[0][1], 0.0, places=12)

    def test_h300_s50_old_tangential_arithmetic_counterexample(self):
        # GUIDE13 C13-A / RESEARCH section 5: the original report claimed
        # tangential ~0.007 for H300/S50. Independent arithmetic from the
        # frozen numbers (dz, radial) gives 0.153386 (8.336 deg at the
        # report's own 0.0184/deg). The counterexample must keep firing.
        dz = (-0.114069, 0.104696)
        radial = (0.772, 0.639)
        n = math.hypot(*radial)
        tangent = (-radial[1] / n, radial[0] / n)
        tangential = tangent[0] * dz[0] + tangent[1] * dz[1]
        self.assertAlmostEqual(tangential, 0.153386, places=5)
        self.assertAlmostEqual(abs(tangential) / 0.0184, 8.336, places=2)
        self.assertGreater(abs(tangential), 0.15)  # not the old 0.007


class IntervalPrimitiveTests(unittest.TestCase):
    def test_joint_bonferroni_t_df2_independently_derived(self):
        # closed-form Student-t(df=2) quantile inversion:
        # F(t) = 1/2 + t/(2*sqrt(t^2+2))  =>  t = sqrt(8q^2/(1-4q^2)),
        # q = p - 1/2 with p = 1 - 0.05/(2*3) for a joint 95% over
        # three outputs
        p = 1.0 - 0.05 / 6.0
        q = p - 0.5
        expected_t = math.sqrt(8.0 * q * q / (1.0 - 4.0 * q * q))
        self.assertAlmostEqual(
            guide13.T_JOINT_95_DF2_THREE_OUTPUTS, expected_t, places=6)
        self.assertNotEqual(guide13.T_JOINT_95_DF2_THREE_OUTPUTS, 9.925)

    def test_mean_ci_and_pi_computed_separately_and_self_consistent(self):
        values = [1.0, 2.0, 3.0]  # mean 2, sd 1, n 3
        t = 4.303  # t(0.95, df=2), independent
        ci = guide13.mean_ci(values, t)
        self.assertAlmostEqual(ci["mean"], 2.0, places=12)
        self.assertAlmostEqual(ci["half_width"], 4.303 / math.sqrt(3),
                               places=12)
        pi = guide13.prediction_interval_next_single(values, t)
        self.assertAlmostEqual(
            pi["half_width"], 4.303 * math.sqrt(1 + 1.0 / 3.0), places=12)
        self.assertGreater(pi["half_width"], ci["half_width"])
        self.assertTrue(guide13.interval_self_consistent(ci))
        self.assertTrue(guide13.interval_self_consistent(pi))
        self.assertEqual(pi["estimand"], "mean_of_next_1_observations")

    def test_next_session_mean_pi_uses_one_over_n_plus_one_over_m(self):
        # NIST prediction-limit form for the mean of m future values:
        # mean +- t*s*sqrt(1/n + 1/m); with values [1,2,3], m=2:
        # half = 4.303*sqrt(1/3 + 1/2) = 4.303*sqrt(5/6)
        values = [1.0, 2.0, 3.0]
        pi = guide13.prediction_interval_next_mean(values, 4.303, 2)
        self.assertAlmostEqual(
            pi["half_width"], 4.303 * math.sqrt(1.0 / 3.0 + 1.0 / 2.0),
            places=12)
        self.assertEqual(pi["estimand"], "mean_of_next_2_observations")

    def test_sd_confidence_interval_chi_square_pivot(self):
        values = [1.0, 2.0, 3.0]  # s = 1, n = 3, df = 2
        # chi2(0.975, 2) = 7.37776 (right/large), chi2(0.025, 2) = 0.05063562
        out = guide13.sd_confidence_interval(values, 7.37776, 0.05063562)
        self.assertAlmostEqual(out["sd"], 1.0, places=12)
        self.assertAlmostEqual(out["low"], math.sqrt(2.0 / 7.37776),
                               places=9)
        self.assertAlmostEqual(out["high"], math.sqrt(2.0 / 0.05063562),
                               places=5)
        self.assertLess(out["low"], out["high"])


if __name__ == "__main__":
    unittest.main()
