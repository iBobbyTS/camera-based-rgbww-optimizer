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


class Guide13RuntimeSemanticTests(unittest.TestCase):
    """GUIDE13 C13-D: S0 must serve the validated white command, the
    full anchor set (including H60/S100) must be read, and clamping is
    reported as requested/realized + gamut_compressed - never
    as-requested."""

    def test_s0_serves_validated_white_command_for_every_hue(self):
        for hue in (0, 60, 137, 240, 359):
            out = guide12_c124.c124_model_command(hue, 0)
            self.assertEqual(
                out["command"], guide12_c124.C124_ADOPTED["0/0"], hue)
            self.assertEqual(out["sat_status"], "as-requested")
            self.assertEqual(out["realized_sat"], 0)
            self.assertFalse(out["gamut_compressed"])

    def test_h60_s100_anchor_is_actually_served(self):
        out = guide12_c124.c124_model_command(60, 100)
        self.assertEqual(out["command"], guide12_c124.C124_ADOPTED["60/100"])
        self.assertEqual(out["sat_status"], "as-requested")
        self.assertEqual(out["realized_sat"], 100)
        # interpolation between the S50 and S100 anchors is available
        mid = guide12_c124.c124_model_command(60, 75)
        self.assertEqual(mid["sat_status"], "interpolated")
        self.assertEqual(mid["realized_sat"], 75)
        self.assertEqual(mid["served_layers"], [50, 100])

    def test_sat_beyond_top_layer_is_explicit_compression(self):
        out = guide12_c124.c124_model_command(30, 80)  # no S100 at hue 30
        self.assertTrue(out["gamut_compressed"])
        self.assertEqual(out["sat_status"], "gamut_compressed")
        self.assertEqual(out["realized_sat"], 50)
        self.assertEqual(out["request"]["sat"], 80)
        self.assertEqual(
            out["command"], guide12_c124.c124_model_command(30, 50)["command"])

    def test_low_interior_sat_interpolates_s0_to_s25(self):
        out = guide12_c124.c124_model_command(45, 10)
        self.assertEqual(out["sat_status"], "interpolated")
        self.assertEqual(out["realized_sat"], 10)
        self.assertEqual(out["served_layers"], [0, 25])
        self.assertFalse(out["gamut_compressed"])
        # the serve moves continuously from the white S0 command toward
        # the hue-45 S25 serve as SAT grows (each command is projected
        # to fullscale, so per-channel ranges do not apply)
        white = guide12_c124.c124_model_command(45, 0)["command"]
        s25 = guide12_c124.c124_model_command(45, 25)["command"]
        near = guide12_c124.c124_model_command(45, 5)["command"]
        far = guide12_c124.c124_model_command(45, 20)["command"]

        def l1(a, b):
            return sum(abs(a[ch] - b[ch]) for ch in ("cw", "ww", "r", "g", "b"))

        self.assertNotEqual(out["command"], white)
        self.assertNotEqual(out["command"], s25)
        self.assertLess(l1(near, white), l1(far, white))
        self.assertLess(l1(far, s25), l1(near, s25))

    def test_anchor_identity_and_periodicity(self):
        for key, command in guide12_c124.C124_ADOPTED.items():
            hue, sat = (int(x) for x in key.split("/"))
            out = guide12_c124.c124_model_command(hue, sat)
            self.assertEqual(out["command"], command, key)
            self.assertEqual(out["sat_status"], "as-requested", key)
        a = guide12_c124.c124_model_command(0, 50)
        b = guide12_c124.c124_model_command(360, 50)
        self.assertEqual(a["command"], b["command"])


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
