"""Behavior tests for the GUIDE13 C13-A local-Jacobian plan."""
from __future__ import annotations

import unittest

from camera_based_rgbww_optimizer.optimization import guide13_c13a


class C13APlanTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.plan = guide13_c13a.build_guide13_c13a_plan()

    def test_three_targets_seven_frames_each(self):
        self.assertEqual(len(self.plan["captures"]), 21)
        by_target: dict[str, list[str]] = {}
        for step in self.plan["captures"]:
            by_target.setdefault(step["c13a_target"], []).append(
                step["c13a_role"])
        self.assertEqual(
            set(by_target),
            {"0/50", "300/50", "60/100"})
        for target, roles in by_target.items():
            self.assertEqual(roles, [
                "center_before", "neighbor", "neighbor", "neighbor",
                "neighbor", "holdout", "center_after"], target)

    def test_neighborhood_coordinates_match_guide13(self):
        expected = {
            "0/50": [(358, 50), (2, 50), (0, 48), (0, 52), (1, 51)],
            "300/50": [(298, 50), (302, 50), (300, 48), (300, 52), (301, 51)],
            # S100 uses S98/S96 (SAT cannot exceed 100) and (H+1, S99)
            "60/100": [(58, 100), (62, 100), (60, 98), (60, 96), (61, 99)],
        }
        for target, coords in expected.items():
            steps = [s for s in self.plan["captures"]
                     if s["c13a_target"] == target]
            got = [int(s["command"]["hue"]) * 1000 + int(s["command"]["sat"])
                   for s in steps if s["c13a_role"] in ("neighbor", "holdout")]
            want = [h * 1000 + sat for h, sat in coords]
            self.assertEqual(got, want, target)

    def test_all_frames_are_ray_hsi_with_strip_isolation(self):
        for step in self.plan["captures"]:
            self.assertEqual(step["source_id"], "ray")
            self.assertEqual(step["command"]["mode"], "hsi")
            self.assertEqual(step["command"]["intensity_percent"], 100.0)
            self.assertTrue(step["strip_zero_required"])
            self.assertFalse(step.get("ray_zero_required", False))
            # validator contract fields
            self.assertEqual(step["c12_hue"], step["command"]["hue"])
            self.assertEqual(step["c12_sat"], step["command"]["sat"])
            self.assertIn(0 <= int(step["c12_hue"]) < 360, (True,))
            self.assertIn(int(step["c12_sat"]), range(0, 101))

    def test_hue_wraps_periodically_at_h0(self):
        hues = [int(s["command"]["hue"]) for s in self.plan["captures"]
                if s["c13a_target"] == "0/50"]
        self.assertIn(358, hues)   # H-2 wraps below 0
        self.assertIn(2, hues)

    def test_ledger_budget_and_authorization(self):
        frozen = self.plan["frozen_shutters"]
        self.assertEqual(
            sorted(frozen),
            sorted(self.plan["shutter_ledger_provenance"]
                   ["required_cache_keys"]))
        for step in self.plan["captures"]:
            self.assertEqual(
                frozen[step["exposure_cache_key"]], step["nominal_shutter"])
        self.assertEqual(self.plan["budgets"]["formal_cap"], 21)
        self.assertEqual(self.plan["budgets"]["retry"], 0)
        self.assertEqual(
            self.plan["execution_authorization"]["schema"],
            "direct_guide12_c12_ray_grid_v1")
        self.assertEqual(
            self.plan["execution_authorization"]["experiment_id"],
            guide13_c13a.C13A_EXPERIMENT_ID)
        self.assertIn("NOT assumed orthogonal",
                      self.plan["analysis_contract"]["jacobian_rule"])


if __name__ == "__main__":
    unittest.main()
