import unittest

import numpy as np

from camera_based_rgbww_optimizer.optimization import white_lut_feedback as feedback


class WhiteLutFeedbackTests(unittest.TestCase):
    def test_white_point_metrics_uses_requested_goal_tolerances(self):
        metrics = feedback.white_point_metrics(
            {"cct_K": 5006.0, "duv": 0.003},
            {"cct_K": 5000.0, "duv": -0.002},
            cct_tolerance_K=10.0,
            duv_tolerance=0.01,
        )

        self.assertEqual(metrics["normalized_error"], [0.6, 0.5])
        self.assertEqual(metrics["goal_score"], 0.6)
        self.assertTrue(metrics["within_goal"])

    def test_probe_commands_keep_active_channel_at_max_and_probe_each_free_channel(self):
        command = {"cw": 4095, "ww": 0, "r": 100, "g": 4000, "b": 2048}

        probes = feedback.build_probe_commands(
            command,
            active_channel="cw",
            probe_step_code=256,
            max_code=4095,
        )

        self.assertEqual([probe["channel"] for probe in probes], ["ww", "r", "g", "b"])
        for probe in probes:
            self.assertEqual(probe["command"]["cw"], 4095)
            changed = [
                channel
                for channel in feedback.DEFAULT_CHANNELS
                if probe["command"][channel] != command[channel]
            ]
            self.assertEqual(changed, [probe["channel"]])
            self.assertTrue(all(0 <= value <= 4095 for value in probe["command"].values()))

    def test_estimated_jacobian_and_damped_step_reduce_linear_white_point_error(self):
        channels = feedback.DEFAULT_CHANNELS
        active = "cw"
        max_code = 4095
        target = {"cct_K": 5000.0, "duv": 0.0}
        desired = {"cw": 4095, "ww": 1500, "r": 400, "g": 1200, "b": 300}
        initial = {"cw": 4095, "ww": 700, "r": 400, "g": 400, "b": 300}

        def observe(command):
            ww_error = command["ww"] - desired["ww"]
            g_error = command["g"] - desired["g"]
            return {
                "cct_K": target["cct_K"] + ww_error * 0.2 + g_error * 0.01,
                "duv": target["duv"] + ww_error * 0.000001 + g_error * 0.00002,
            }

        probes = []
        for probe in feedback.build_probe_commands(
            initial,
            active_channel=active,
            probe_step_code=256,
            max_code=max_code,
            channels=channels,
        ):
            probes.append({
                "probe_channel": probe["channel"],
                "probe_delta_code": probe["delta_code"],
                "white_point": observe(probe["command"]),
            })
        jacobian = feedback.estimate_jacobian(
            observe(initial),
            probes,
            target_white_point=target,
            active_channel=active,
            cct_tolerance_K=10.0,
            duv_tolerance=0.01,
            max_code=max_code,
            channels=channels,
        )
        step = feedback.solve_damped_step(
            initial,
            observe(initial),
            target,
            jacobian,
            active_channel=active,
            cct_tolerance_K=10.0,
            duv_tolerance=0.01,
            max_code=max_code,
            max_step_code=1024,
            damping=0.001,
            rgb_penalty=0.45,
            channels=channels,
        )

        before = feedback.white_point_metrics(
            observe(initial), target, cct_tolerance_K=10.0, duv_tolerance=0.01
        )
        after = feedback.white_point_metrics(
            observe(step["command"]), target, cct_tolerance_K=10.0, duv_tolerance=0.01
        )
        self.assertLess(after["goal_score"], before["goal_score"])
        self.assertEqual(step["command"][active], max_code)

    def test_broyden_update_satisfies_latest_secant_observation(self):
        previous_command = {"cw": 4095, "ww": 1000, "r": 0, "g": 500, "b": 0}
        next_command = {"cw": 4095, "ww": 1200, "r": 0, "g": 700, "b": 0}
        previous_white = {"cct_K": 4800.0, "duv": -0.01}
        next_white = {"cct_K": 4950.0, "duv": -0.002}
        target = {"cct_K": 5000.0, "duv": 0.0}
        jacobian = np.zeros((2, 4), dtype="float64")

        updated = feedback.broyden_update(
            jacobian,
            previous_command,
            next_command,
            previous_white,
            next_white,
            target,
            active_channel="cw",
            cct_tolerance_K=10.0,
            duv_tolerance=0.01,
            max_code=4095,
        )

        delta = np.asarray([
            (next_command[channel] - previous_command[channel]) / 4095.0
            for channel in ("ww", "r", "g", "b")
        ])
        observed_delta = np.asarray([15.0, 0.8])
        np.testing.assert_allclose(updated @ delta, observed_delta, atol=1e-12)

    def test_damped_step_prefers_rgb_channel_with_lower_directional_penalty(self):
        command = {"cw": 4095, "ww": 0, "r": 0, "g": 0, "b": 0}
        jacobian = np.asarray([
            [0.0, 10.0, 10.0, 0.0],
            [0.0, 5.0, 5.0, 0.0],
        ])

        step = feedback.solve_damped_step(
            command,
            {"cct_K": 4900.0, "duv": -0.01},
            {"cct_K": 5000.0, "duv": 0.0},
            jacobian,
            active_channel="cw",
            cct_tolerance_K=10.0,
            duv_tolerance=0.01,
            max_code=4095,
            max_step_code=1024,
            damping=0.05,
            rgb_penalty=0.02,
            channel_penalties={"r": 0.02, "g": 0.45, "b": 0.45},
        )

        self.assertGreater(step["delta_codes"]["r"], step["delta_codes"]["g"])

    def test_bracketed_cct_step_interpolates_between_measured_samples(self):
        initial_command = {"cw": 4095, "ww": 0, "r": 0, "g": 0, "b": 1024}
        probe_command = {**initial_command, "r": 256}
        samples = [
            {
                "index": 0,
                "command": initial_command,
                "white_point_comparison": {
                    "normalized_error": [2.5, 0.05],
                    "goal_score": 2.5,
                },
            },
            {
                "index": 1,
                "command": probe_command,
                "white_point_comparison": {
                    "normalized_error": [-5.0, 0.08],
                    "goal_score": 5.0,
                },
            },
        ]

        step = feedback.build_bracketed_cct_step(
            samples,
            initial_command,
            active_channel="cw",
            max_code=4095,
        )

        self.assertIsNotNone(step)
        self.assertEqual(step["kind"], "bracketed_cct_secant")
        self.assertEqual(step["command"], {**initial_command, "r": 85})
        self.assertEqual(step["source_sample_indices"], [0, 1])
        self.assertAlmostEqual(step["predicted_normalized_error"][0], 0.0)
        self.assertLess(step["predicted_goal_score"], 1.0)

    def test_bracketed_cct_step_rejects_unbracketed_samples(self):
        command = {"cw": 4095, "ww": 0, "r": 0, "g": 0, "b": 1024}
        samples = [
            {
                "index": index,
                "command": {**command, "r": index * 256},
                "white_point_comparison": {
                    "normalized_error": [error, 0.05],
                    "goal_score": error,
                },
            }
            for index, error in enumerate((2.5, 1.5))
        ]

        step = feedback.build_bracketed_cct_step(
            samples,
            command,
            active_channel="cw",
            max_code=4095,
        )

        self.assertIsNone(step)


if __name__ == "__main__":
    unittest.main()
