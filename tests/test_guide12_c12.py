"""Behavior tests for the GUIDE12 C12-1 Ray HSI mapping plan builder."""
from __future__ import annotations

import unittest

from camera_based_rgbww_optimizer.optimization.guide12_c12 import (
    C12_1_EXISTING_COORDINATES,
    C12_1_TARGETS,
    build_guide12_c12_ray_grid_plan,
)


class Guide12C12RayGridPlanTests(unittest.TestCase):
    def test_frozen_budget_is_within_the_ray_only_cap(self):
        plan = build_guide12_c12_ray_grid_plan()
        self.assertEqual(len(plan["captures"]), 20)
        self.assertEqual(len(C12_1_TARGETS), 20)
        self.assertLessEqual(len(C12_1_TARGETS), 31)

    def test_holdout_coordinates_are_untested_and_cover_the_required_regions(self):
        holdouts = [
            (int(t["hue"]), int(t["sat"]))
            for t in C12_1_TARGETS if t["role"] == "holdout"
        ]
        self.assertEqual(len(holdouts), 12)
        for coord in holdouts:
            self.assertNotIn(coord, C12_1_EXISTING_COORDINATES, coord)
        sectors = {h // 60 for h, _ in holdouts}
        self.assertEqual(sectors, {0, 1, 2, 3, 4, 5})
        self.assertTrue(any(h < 10 for h, _ in holdouts))       # 0 side
        self.assertTrue(any(h > 350 for h, _ in holdouts))      # 360 side
        sats = {s for _, s in holdouts}
        self.assertEqual(sats, {10, 20, 50, 75})

    def test_special_qualification_and_s0_frames_are_frozen(self):
        roles = [t["role"] for t in C12_1_TARGETS]
        self.assertEqual(roles.count("special_qualification_ref"), 4)
        self.assertEqual(roles.count("s0_control"), 2)
        self.assertEqual(roles.count("s0_reference_sessionA"), 1)
        self.assertEqual(roles.count("s0_hue_consistency_diag"), 1)
        for hue in (120, 300):
            self.assertEqual(
                sum(
                    1 for t in C12_1_TARGETS
                    if t["role"] == "special_qualification_ref"
                    and int(t["hue"]) == hue
                ),
                2,
            )

    def test_every_step_is_a_ray_hsi_command_matching_its_target(self):
        plan = build_guide12_c12_ray_grid_plan()
        for step in plan["captures"]:
            self.assertEqual(step["source_id"], "ray")
            self.assertEqual(step["command"]["mode"], "hsi")
            self.assertEqual(step["command"]["intensity_percent"], 100.0)
            self.assertEqual(step["command"]["hue"], step["c12_hue"])
            self.assertEqual(step["command"]["sat"], step["c12_sat"])
            self.assertTrue(step["formal_measurement"])
            self.assertTrue(step["strip_zero_required"])
            self.assertTrue(step["exposure_cache_key"])

    def test_shutter_ledger_is_frozen_and_complete(self):
        plan = build_guide12_c12_ray_grid_plan()
        frozen = plan["frozen_shutters"]
        self.assertEqual(
            sorted(frozen),
            sorted(plan["shutter_ledger_provenance"]["required_cache_keys"]),
        )
        for step in plan["captures"]:
            self.assertEqual(frozen[step["exposure_cache_key"]], step["nominal_shutter"])
        for shutter in frozen.values():
            self.assertRegex(shutter, r"^1/\d+$")

    def test_role_filter_narrows_for_retries_and_rejects_unknown_roles(self):
        plan = build_guide12_c12_ray_grid_plan(roles=("s0_reference_sessionA",))
        self.assertEqual(len(plan["captures"]), 1)
        with self.assertRaises(ValueError):
            build_guide12_c12_ray_grid_plan(roles=("nonexistent_role",))

    def test_authorization_schema_and_budgets_are_declared(self):
        plan = build_guide12_c12_ray_grid_plan()
        self.assertEqual(
            plan["execution_authorization"]["schema"],
            "direct_guide12_c12_ray_grid_v1",
        )
        self.assertEqual(plan["budgets"]["formal_cap"], 20)
        self.assertEqual(plan["budgets"]["ambient_cap"], 0)
        self.assertEqual(plan["budgets"]["retry"], 0)
        self.assertEqual(
            plan["analysis_contract"]["budgets"],
            {"hue_deg": 0.5, "sat_pp": 0.5},
        )


if __name__ == "__main__":
    unittest.main()
