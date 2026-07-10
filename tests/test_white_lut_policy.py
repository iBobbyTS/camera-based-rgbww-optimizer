import unittest

from camera_based_rgbww_optimizer.optimization import measure_white_lut
from camera_based_rgbww_optimizer.optimization import white_lut_policy as policy


ENDPOINT_MATCHES = {
    "ww": {"best": {"cct": 2931, "gm": 176}},
    "cw": {"best": {"cct": 7702, "gm": 160}},
}


def build_policy(cct, gm):
    return policy.build_rgb_policy(
        target_cct=cct,
        target_gm=gm,
        endpoint_matches=ENDPOINT_MATCHES,
        cct_min=1800,
        cct_max=20000,
        gm_min=0,
        gm_max=200,
        native_penalty=0.45,
        outside_penalty=0.06,
        endpoint_penalty=0.02,
    )


class WhiteLutPolicyTests(unittest.TestCase):
    def test_native_gm_interpolates_between_measured_endpoints(self):
        self.assertEqual(
            policy.interpolate_native_gm(2931, low_cct=2931, low_gm=176, high_cct=7702, high_gm=160),
            176.0,
        )
        self.assertEqual(
            policy.interpolate_native_gm(7702, low_cct=2931, low_gm=176, high_cct=7702, high_gm=160),
            160.0,
        )
        self.assertAlmostEqual(
            policy.interpolate_native_gm(5316, low_cct=2931, low_gm=176, high_cct=7702, high_gm=160),
            168.002,
            places=3,
        )

    def test_native_white_keeps_strong_rgb_penalty(self):
        result = build_policy(2931, 176)

        self.assertEqual(result["cct_extension"]["need"], 0.0)
        self.assertEqual(result["gm_compensation"]["need"], 0.0)
        self.assertEqual(result["channel_penalties"], {"r": 0.45, "g": 0.45, "b": 0.45})

    def test_magenta_target_releases_red_and_blue_but_not_green(self):
        result = build_policy(3200, 0)

        self.assertEqual(result["gm_compensation"]["direction"], "magenta")
        self.assertAlmostEqual(result["channel_penalties"]["r"], 0.02)
        self.assertAlmostEqual(result["channel_penalties"]["b"], 0.02)
        self.assertAlmostEqual(result["channel_penalties"]["g"], 0.45)

    def test_green_target_releases_green_but_not_red_and_blue(self):
        result = build_policy(5600, 200)

        self.assertEqual(result["gm_compensation"]["direction"], "green")
        self.assertAlmostEqual(result["channel_penalties"]["g"], 0.02)
        self.assertAlmostEqual(result["channel_penalties"]["r"], 0.45)
        self.assertAlmostEqual(result["channel_penalties"]["b"], 0.45)

    def test_cct_extremes_release_the_directional_primary(self):
        warm = build_policy(1800, 176)
        cool = build_policy(20000, 160)

        self.assertEqual(warm["cct_extension"], {"direction": "warmer", "need": 1.0})
        self.assertAlmostEqual(warm["channel_penalties"]["r"], 0.02)
        self.assertAlmostEqual(warm["channel_penalties"]["b"], 0.45)
        self.assertEqual(cool["cct_extension"], {"direction": "cooler", "need": 1.0})
        self.assertAlmostEqual(cool["channel_penalties"]["b"], 0.02)
        self.assertAlmostEqual(cool["channel_penalties"]["r"], 0.45)

    def test_first_step_outside_cct_span_caps_directional_primary_at_outside_penalty(self):
        result = build_policy(2930, 176)

        self.assertEqual(result["cct_extension"]["direction"], "warmer")
        self.assertGreater(result["channel_penalties"]["r"], 0.02)
        self.assertLessEqual(result["channel_penalties"]["r"], 0.06)
        self.assertEqual(result["channel_penalties"]["g"], 0.45)

    def test_model_solver_prefers_the_lower_penalty_rgb_direction(self):
        regions = [{"name": "white", "calibration_weight": 1.0}]
        basis = {
            "cw": [0.0, 0.0, 0.0],
            "ww": [1.0, 1.0, 1.0],
            "r": [1.0, 0.0, 0.0],
            "g": [1.0, 0.0, 0.0],
            "b": [0.0, 0.0, 0.0],
        }

        solution = measure_white_lut.solve_high_output_mix(
            basis,
            [2.0, 1.0, 1.0],
            regions=regions,
            rgb_penalty=0.02,
            channel_penalties={"r": 0.02, "g": 0.45, "b": 0.45},
            endpoint_bias="ww",
            max_code=4095,
        )

        self.assertGreater(solution["command"]["r"], solution["command"]["g"])
        self.assertEqual(solution["channel_penalties"], {"r": 0.02, "g": 0.45, "b": 0.45})

    def test_outside_range_solver_can_keep_compensation_primary_at_max(self):
        regions = [{"name": "white", "calibration_weight": 1.0}]
        basis = {
            "cw": [0.0, 0.0, 0.0],
            "ww": [1.0, 1.0, 1.0],
            "r": [1.0, 0.0, 0.0],
            "g": [0.0, 1.0, 0.0],
            "b": [0.0, 0.0, 1.0],
        }

        solution = measure_white_lut.solve_high_output_mix(
            basis,
            [1.5, 0.5, 0.5],
            regions=regions,
            rgb_penalty=0.02,
            channel_penalties={"r": 0.02, "g": 0.45, "b": 0.45},
            endpoint_bias="ww",
            max_code=4095,
        )

        self.assertEqual(solution["active_channel"], "r")
        self.assertEqual(solution["command"]["r"], 4095)
        self.assertLess(solution["command"]["ww"], 4095)


if __name__ == "__main__":
    unittest.main()
