import unittest

from camera_based_rgbww_optimizer.optimization import p7_thermal_diagnostics as thermal


class Guide10WhiteMicrobracketTests(unittest.TestCase):
    def test_plan_is_frozen_to_preregistered_five_capture_bracket(self):
        plan = thermal.build_direct_plan(
            thermal.TD_C,
            variant=thermal.GUIDE10_WHITE_1800_GM100_MICROBRACKET_VARIANT,
        )
        self.assertEqual(
            [step["role"] for step in plan["captures"]],
            [
                "ray_reference_before",
                "strip_g1197",
                "strip_g1204",
                "strip_g1200",
                "ray_reference_after",
            ],
        )
        self.assertEqual(
            [step["command"]["g"] for step in plan["captures"] if step["source_id"] == "strip"],
            [1197, 1204, 1200],
        )
        self.assertEqual(plan["budgets"]["ray_cap"], 2)
        self.assertEqual(plan["budgets"]["strip_cap"], 3)
        self.assertEqual(plan["budgets"]["formal_cap"], 5)
        self.assertEqual(plan["analysis_contract"]["max_unique_g_codes"], 5)


if __name__ == "__main__":
    unittest.main()
