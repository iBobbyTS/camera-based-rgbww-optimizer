"""Behavior tests for the GUIDE12 C12-4 runtime model + holdout plan."""
from __future__ import annotations

import unittest

from camera_based_rgbww_optimizer.optimization import guide12_c124


class Guide12C124ModelTests(unittest.TestCase):
    def test_adopted_commands_are_true_fullscale(self):
        for key, command in guide12_c124.C124_ADOPTED.items():
            self.assertEqual(max(command.values()), 4095, key)
            self.assertEqual(sorted(command), ["b", "cw", "g", "r", "ww"], key)

    def test_model_always_fullscale_and_periodic_at_anchors(self):
        for hue, sat in guide12_c124.C124_HOLDOUTS:
            out = guide12_c124.c124_model_command(hue, sat)
            self.assertEqual(max(out["command"].values()), 4095, (hue, sat))
        # periodicity: hue 0 and hue 360 are the same model output
        a = guide12_c124.c124_model_command(0, 50)
        b = guide12_c124.c124_model_command(360, 50)
        self.assertEqual(a["command"], b["command"])
        # anchor requests reproduce the adopted commands verbatim
        for hue in guide12_c124.C124_HUE_ANCHORS:
            out = guide12_c124.c124_model_command(hue, 25)
            self.assertEqual(
                out["command"], guide12_c124.C124_ADOPTED[f"{hue}/25"], hue)

    def test_sat_monotonic_by_construction_and_compression_recorded(self):
        out25 = guide12_c124.c124_model_command(45, 25)
        out50 = guide12_c124.c124_model_command(45, 50)
        self.assertNotEqual(out25["command"], out50["command"])
        interior = guide12_c124.c124_model_command(75, 35)
        self.assertIn("compressed", interior["sat_note"])
        self.assertIn(
            "NOT claimed as the original request being reproduced",
            interior["compressed_sat_note"])
        clamped = guide12_c124.c124_model_command(45, 10)
        floor = guide12_c124.c124_model_command(45, 25)
        self.assertEqual(clamped["command"], floor["command"])  # clamp to 25


class Guide12C124PlanTests(unittest.TestCase):
    def test_plan_is_30_frames_with_sandwiches(self):
        plan = guide12_c124.build_guide12_c124_holdout_plan()
        self.assertEqual(len(plan["captures"]), 30)
        self.assertEqual(
            plan["budgets"]["formal_cap"], 30)
        self.assertEqual(
            plan["budgets"]["repair_rounds_cap"], 1)
        self.assertEqual(plan["budgets"]["repair_frames_cap"], 18)
        for index in range(0, 30, 3):
            triple = plan["captures"][index:index + 3]
            self.assertEqual(
                [s["source_id"] for s in triple], ["ray", "strip", "ray"])
            self.assertEqual(
                [s["c124_position"] for s in triple],
                ["raybefore", "strip", "rayafter"])
            strip = triple[1]
            self.assertEqual(
                strip["command"],
                guide12_c124.c124_model_command(
                    *next(iter([r for r in guide12_c124.C124_HOLDOUTS
                                if f"{r[0]}/{r[1]}" == strip["c124_request"]]))
                )["command"])
            self.assertTrue(strip["ray_zero_required"])
            self.assertTrue(triple[0]["strip_zero_required"])
        self.assertEqual(
            plan["execution_authorization"]["schema"],
            guide12_c124.C124_SCHEMA)
        ledger = plan["shutter_ledger_provenance"]
        self.assertEqual(
            sorted(plan["frozen_shutters"]), ledger["required_cache_keys"])

    def test_holdouts_cover_required_structure(self):
        reqs = set(guide12_c124.C124_HOLDOUTS)
        self.assertEqual(len(reqs), 10)
        hues = {h for h, _ in reqs}
        for sector in (0, 60, 120, 180, 240, 300):
            self.assertTrue(any(abs(h - sector) <= 30 for h in hues), sector)
        self.assertIn((2, 25), reqs)     # periodic neighbor
        self.assertIn((358, 25), reqs)   # periodic neighbor
        self.assertIn((75, 35), reqs)    # fixed low-SAT interior
        self.assertIn((255, 40), reqs)   # fixed low-SAT interior
        for key in (f"{h}/{s}" for h, s in reqs):
            self.assertIn(key, guide12_c124.C124_RAY_SHUTTERS)


if __name__ == "__main__":
    unittest.main()
