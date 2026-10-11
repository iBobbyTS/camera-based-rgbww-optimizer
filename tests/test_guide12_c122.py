"""Behavior tests for the GUIDE12 C12-2 color solving scaffolding."""
from __future__ import annotations

import unittest

from camera_based_rgbww_optimizer.optimization import guide12_c122


class Guide12C122RequestTests(unittest.TestCase):
    def test_thirteen_frozen_requests_and_shutters(self):
        self.assertEqual(len(guide12_c122.C122_REQUESTS), 13)
        self.assertIn((0, 0), guide12_c122.C122_REQUESTS)
        for hue in guide12_c122.C122_HUES:
            for sat in (50, 100):
                self.assertIn((hue, sat), guide12_c122.C122_REQUESTS)
        for request in guide12_c122.C122_REQUESTS:
            key = f"{request[0]}/{request[1]}"
            self.assertIn(key, guide12_c122.C122_RAY_SHUTTERS)
        # anchor self-checks reproduce the C12-1/W12-3 frozen values
        self.assertEqual(guide12_c122.C122_RAY_SHUTTERS["120/100"], "1/3200")
        self.assertEqual(guide12_c122.C122_RAY_SHUTTERS["300/100"], "1/1600")
        self.assertEqual(guide12_c122.C122_RAY_SHUTTERS["0/0"], "1/6400")

    def test_initial_commands_are_true_fullscale_sector_structures(self):
        for hue in guide12_c122.C122_HUES:
            for sat in (50, 100):
                command = guide12_c122.c122_initial_command(hue, sat)
                self.assertEqual(max(command.values()), 4095, (hue, sat))
                self.assertEqual(
                    sorted(command), ["b", "cw", "g", "r", "ww"])
                if sat == 50:
                    self.assertGreater(command["cw"], 0)
                    self.assertGreater(command["ww"], 0)
                else:
                    self.assertEqual(command["cw"], 0)
                    self.assertEqual(command["ww"], 0)
        seed = guide12_c122.c122_initial_command(0, 0)
        self.assertEqual(sorted(seed), ["b", "cw", "g", "r", "ww"])
        with self.assertRaises(ValueError):
            guide12_c122.c122_initial_command(90, 50)

    def test_probe_candidates_repeat_base_and_probe_free_axes(self):
        for hue in guide12_c122.C122_HUES:
            for sat in (50, 100):
                base = guide12_c122.c122_initial_command(hue, sat)
                candidates = guide12_c122.c122_probe_candidates(base)
                self.assertLessEqual(len(candidates), 4)
                self.assertEqual(candidates[0]["tag"], "u0_repeat")
                self.assertFalse(candidates[0]["new_unique_command"])
                self.assertEqual(candidates[0]["command"], base)
                probed = {c.get("probe_channel") for c in candidates[1:]}
                for channel in probed:
                    if channel is not None:
                        self.assertGreater(base[str(channel)], 0)

    def test_initial_strip_shutter_tiers_by_dominance(self):
        white_seed = guide12_c122.c122_initial_command(0, 0)
        self.assertEqual(
            guide12_c122.c122_initial_strip_shutter(white_seed), "1/100")
        for hue in guide12_c122.C122_HUES:
            rgb = guide12_c122.c122_initial_command(hue, 100)
            self.assertEqual(
                guide12_c122.c122_initial_strip_shutter(rgb), "1/400")

    def test_z_face_step_respects_face_and_box(self):
        base = guide12_c122.c122_initial_command(0, 100)  # r fullscale
        sensitivity = {
            "z_r": {"cw": 0.0, "ww": 0.0, "r": 0.0, "g": -0.5, "b": -0.9},
            "z_b": {"cw": 0.0, "ww": 0.0, "r": 0.0, "g": -0.4, "b": 0.7},
        }
        step = guide12_c122.solve_guide12_c122_face_step(
            base, {"z_r": 0.04, "z_b": 0.03}, sensitivity,
            face_channels=("cw", "ww"), sat=100,
        )
        self.assertEqual(step["face_channels"], ["cw", "ww"])
        self.assertEqual(step["command"]["cw"], 0)
        self.assertEqual(step["command"]["ww"], 0)
        self.assertEqual(step["command"]["r"], 4095)
        self.assertLessEqual(max(abs(v) for v in step["delta"].values()), 768.0)
        self.assertTrue(step["surrogate"])
        self.assertTrue(step["final_selection_requires_measured_gate"])
        self.assertLess(step["predicted_E"], 10.0)
        # unmodeled axis (red at ceiling with zero sensitivity) stays pinned
        self.assertIn("r", step["unmodeled_locked_channels"])


class Guide12C122BlockPlanTests(unittest.TestCase):
    def test_block_brackets_candidates_with_per_candidate_shutters(self):
        candidates = guide12_c122.c122_probe_candidates(
            guide12_c122.c122_initial_command(240, 100))
        plan = guide12_c122.build_guide12_c122_block_plan(
            240, 100, candidates, block_index=1)
        roles = [s["role"] for s in plan["captures"]]
        self.assertEqual(roles[0], "ray_reference")
        self.assertEqual(roles[-1], "ray_reference")
        strip = [s for s in plan["captures"] if s["source_id"] == "strip"]
        self.assertEqual(len(strip), len(candidates))
        for step in strip:
            self.assertEqual(step["requested_elapsed_s"], 120)
            self.assertEqual(step["c122_request"], "240/100")
            self.assertEqual(step["c122_block"], 1)
            self.assertTrue(step["ray_zero_required"])
        ray = [s for s in plan["captures"] if s["source_id"] == "ray"]
        for step in ray:
            self.assertEqual(
                step["command"],
                {"mode": "hsi", "hue": 240, "sat": 100, "intensity_percent": 100.0})
            self.assertEqual(step["nominal_shutter"], "1/3200")
            self.assertTrue(step["strip_zero_required"])
        ledger = plan["shutter_ledger_provenance"]
        self.assertEqual(
            sorted(plan["frozen_shutters"]), ledger["required_cache_keys"])
        self.assertEqual(
            plan["execution_authorization"]["schema"],
            guide12_c122.C122_SCHEMA)

    def test_c12_3_s25_requests_accepted_with_transferred_shutters(self):
        self.assertEqual(len(guide12_c122.C123_S25_REQUESTS), 6)
        candidates = [{
            "tag": "u0", "command": {"cw": 1575, "ww": 1575,
                                    "r": 4095, "g": 1024, "b": 1024},
            "role": "base_repeat", "new_unique_command": False,
            "face_channels": [], "strip_shutter": "1/400"}]
        plan = guide12_c122.build_guide12_c122_block_plan(
            0, 25, candidates, block_index=1)
        ray = [s for s in plan["captures"] if s["source_id"] == "ray"]
        self.assertEqual(ray[0]["nominal_shutter"], "1/4000")
        self.assertEqual(ray[0]["command"]["sat"], 25)

    def test_block_rejects_bad_requests_tags_and_candidates(self):
        candidates = guide12_c122.c122_probe_candidates(
            guide12_c122.c122_initial_command(0, 100))
        with self.assertRaises(ValueError):
            guide12_c122.build_guide12_c122_block_plan(
                90, 50, candidates, block_index=1)
        with self.assertRaises(ValueError):
            guide12_c122.build_guide12_c122_block_plan(
                0, 35, candidates, block_index=1)
        with self.assertRaises(ValueError):
            guide12_c122.build_guide12_c122_block_plan(
                0, 100, candidates + candidates, block_index=1)
        bad = [{"tag": "x", "command": {"cw": 1, "ww": 1, "r": 1, "g": 1}}]
        with self.assertRaises(ValueError):
            guide12_c122.build_guide12_c122_block_plan(
                0, 100, bad, block_index=1)
        over = [{"tag": "x", "command": {"cw": 0, "ww": 0, "r": 5000, "g": 0, "b": 0}}]
        with self.assertRaises(ValueError):
            guide12_c122.build_guide12_c122_block_plan(
                0, 100, over, block_index=1)

    def test_budgets_record_request_caps(self):
        candidates = guide12_c122.c122_probe_candidates(
            guide12_c122.c122_initial_command(60, 50))
        plan = guide12_c122.build_guide12_c122_block_plan(
            60, 50, candidates, block_index=2)
        budgets = plan["budgets"]
        self.assertEqual(
            budgets["request_unique_command_cap"],
            guide12_c122.C122_UNIQUE_COMMAND_CAP)
        self.assertEqual(
            budgets["request_unique_command_cap_expanded"],
            guide12_c122.C122_UNIQUE_COMMAND_CAP_EXPANDED)
        self.assertEqual(
            budgets["request_face_cap"], guide12_c122.C122_FACE_CAP)
        self.assertEqual(
            budgets["request_confirmations_required"],
            guide12_c122.C122_CONFIRMATIONS_REQUIRED)
        new_unique = sum(
            1 for c in candidates if c.get("new_unique_command", True))
        self.assertEqual(budgets["block_new_unique_commands"], new_unique)
        self.assertFalse(plan["analysis_contract"]["steady_claim"])


if __name__ == "__main__":
    unittest.main()
