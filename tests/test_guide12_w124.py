"""Behavior tests for the GUIDE12 W12-4 LONG order re-verification."""
from __future__ import annotations

import json
import unittest
from pathlib import Path

from camera_based_rgbww_optimizer.optimization import guide12_w124

LUT = json.loads(Path(
    "D:/rgbww-optimizer/guide12-w122/derived/w12-2-frozen-lut-20261005.json"
).read_text(encoding="utf-8"))["nodes"]
LUT_BY_KEY = {(int(n["cct"]), int(n["gm"])): n for n in LUT}


class Guide12W124PlanTests(unittest.TestCase):
    def test_each_point_protocol_pair_builds_two_frames_with_exact_timing(self):
        for cct, gm in guide12_w124.W124_POINTS:
            for protocol in guide12_w124.W124_PROTOCOLS:
                plan = guide12_w124.build_guide12_w124_point_plan(
                    LUT, cct, gm, protocol=protocol)
                self.assertEqual(len(plan["captures"]), 2, (cct, gm, protocol))
                timing = guide12_w124.W124_TIMING[protocol]
                self.assertEqual(
                    plan["cold_proxy_wait_s"], timing["reset_s"])
                self.assertEqual(
                    plan["timing_resolution"], timing["resolution"])
                for step in plan["captures"]:
                    self.assertEqual(
                        step["requested_elapsed_s"], timing["dwell_s"])
                    self.assertEqual(step["w124_protocol"], protocol)
                    self.assertEqual(step["w124_point"], f"{cct}/{gm}")
                self.assertEqual(
                    plan["execution_authorization"]["schema"],
                    f"direct_guide12_w124_{protocol}_v1")

    def test_commands_verbatim_from_frozen_lut_and_ray_cct(self):
        for cct, gm in guide12_w124.W124_POINTS:
            node = LUT_BY_KEY[(cct, gm)]
            for protocol in guide12_w124.W124_PROTOCOLS:
                plan = guide12_w124.build_guide12_w124_point_plan(
                    LUT, cct, gm, protocol=protocol)
                by_source = {s["source_id"]: s for s in plan["captures"]}
                self.assertEqual(
                    by_source["strip"]["command"],
                    {ch: int(node["command"][ch]) for ch in guide12_w124.CHANNELS})
                self.assertEqual(
                    by_source["ray"]["command"],
                    {"cct": cct, "gm": gm, "intensity_percent": 100.0, "mode": "cct"})

    def test_shutters_verbatim_from_frozen_table_and_ledger(self):
        for cct, gm in guide12_w124.W124_POINTS:
            key = f"{cct}/{gm}"
            for protocol in guide12_w124.W124_PROTOCOLS:
                plan = guide12_w124.build_guide12_w124_point_plan(
                    LUT, cct, gm, protocol=protocol)
                for step in plan["captures"]:
                    self.assertEqual(
                        step["nominal_shutter"],
                        guide12_w124.W124_FROZEN_SHUTTERS[key][step["source_id"]])
                ledger = plan["shutter_ledger_provenance"]
                self.assertEqual(
                    sorted(plan["frozen_shutters"]), ledger["required_cache_keys"])
                for cache, shutter in plan["frozen_shutters"].items():
                    self.assertEqual(
                        plan["frozen_shutters"][cache], shutter)
                    self.assertIn(("ray" if "-ray-" in cache else "strip"), cache)

    def test_campaign_order_satisfies_guide_requirements(self):
        order = guide12_w124.W124_EXECUTION_ORDER
        self.assertEqual(len(order), 8)
        self.assertEqual(len(set(order)), 8)
        pos = {run: i for i, run in enumerate(order)}
        # LONG precedes FAST for the two largest GUIDE11 deviations
        self.assertLess(pos[("3200/100", "long")], pos[("3200/100", "fast")])
        self.assertLess(pos[("20000/100", "long")], pos[("20000/100", "fast")])
        # FAST precedes LONG for the other two (balanced order structure)
        self.assertLess(pos[("1800/100", "fast")], pos[("1800/100", "long")])
        self.assertLess(pos[("5600/100", "fast")], pos[("5600/100", "long")])
        # both protocols appear in each half of the campaign (no period alias)
        protocols_first_half = [q for _, q in order[:4]]
        self.assertEqual(protocols_first_half.count("long"), 2)
        self.assertEqual(protocols_first_half.count("fast"), 2)
        # source order four/four and flipped within each point
        ray_first = guide12_w124.W124_RAY_FIRST
        self.assertEqual(sum(ray_first.values()), 4)
        for point, _ in order:
            pair = [ray_first[(point, q)] for q in ("fast", "long")]
            self.assertEqual(len(set(pair)), 2, point)
        # campaign frame budget within the GUIDE cap
        self.assertEqual(
            guide12_w124.CAMPAIGN_CORE_FRAMES, len(order) * 2)
        self.assertLessEqual(
            guide12_w124.CAMPAIGN_CORE_FRAMES, guide12_w124.CAMPAIGN_FRAME_CAP)

    def test_source_order_flag_controls_frame_order(self):
        plan = guide12_w124.build_guide12_w124_point_plan(
            LUT, 3200, 100, protocol="long", ray_first=True)
        self.assertEqual(
            [s["source_id"] for s in plan["captures"]], ["ray", "strip"])
        plan = guide12_w124.build_guide12_w124_point_plan(
            LUT, 3200, 100, protocol="long", ray_first=False)
        self.assertEqual(
            [s["source_id"] for s in plan["captures"]], ["strip", "ray"])
        # default comes from the frozen campaign table
        default = guide12_w124.build_guide12_w124_point_plan(
            LUT, 3200, 100, protocol="long")
        expected = (
            ["ray", "strip"] if guide12_w124.W124_RAY_FIRST[("3200/100", "long")]
            else ["strip", "ray"])
        self.assertEqual(
            [s["source_id"] for s in default["captures"]], expected)

    def test_unknown_point_or_protocol_fails_closed(self):
        with self.assertRaises(ValueError):
            guide12_w124.build_guide12_w124_point_plan(
                LUT, 2700, 100, protocol="fast")
        with self.assertRaises(ValueError):
            guide12_w124.build_guide12_w124_point_plan(
                LUT, 3200, 70, protocol="fast")
        with self.assertRaises(ValueError):
            guide12_w124.build_guide12_w124_point_plan(
                LUT, 3200, 100, protocol="medium")

    def test_budgets_and_authorization_are_bounded(self):
        plan = guide12_w124.build_guide12_w124_point_plan(
            LUT, 20000, 100, protocol="long")
        budgets = plan["budgets"]
        self.assertEqual(budgets["formal_cap"], 2)
        self.assertEqual(budgets["physical_cr3_cap"], 2)
        self.assertEqual(budgets["retry"], 0)
        auth = plan["execution_authorization"]
        self.assertFalse(auth["human_authorization_required"])
        self.assertEqual(
            auth["experiment_id"], guide12_w124.W124_EXPERIMENT_ID)
        contract = plan["analysis_contract"]
        self.assertEqual(
            contract["primary_quantity"], "(strip-Ray)_LONG-(strip-Ray)_FAST")
        self.assertFalse(contract["steady_claim"])
        self.assertFalse(contract["thermal_causal_claim"])
        self.assertEqual(
            contract["campaign_execution_order"],
            [f"{p}:{q}" for p, q in guide12_w124.W124_EXECUTION_ORDER])


if __name__ == "__main__":
    unittest.main()
