"""Behavior tests for the GUIDE13 W13-C dev-regression plan."""
from __future__ import annotations

import json
import unittest
from pathlib import Path

from camera_based_rgbww_optimizer.optimization import guide13_w13c

LUT = json.loads(Path(
    "D:/rgbww-optimizer/guide12-w122/derived/w12-2-frozen-lut-20261005.json"
).read_text(encoding="utf-8"))["nodes"]
BRIGHTNESS = json.loads(Path(
    "D:/rgbww-optimizer/guide12-w122/derived/w122-node-strip-brightness.json"
).read_text(encoding="utf-8"))

# Advisor corrected counterfactuals (independent expected commands).
ADVISOR_CORRECTED = {
    "1850/50": {"cw": 72, "ww": 2095, "r": 4095, "g": 728, "b": 26},
    "2400/50": {"cw": 279, "ww": 3045, "r": 4095, "g": 1350, "b": 362},
    "17500/30": None,  # not published; asserted via the corrected function
}


class W13CPlanTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.plan = guide13_w13c.build_guide13_w13c_dev_plan(
            LUT, brightness=BRIGHTNESS)

    def test_frame_structure_and_cold_sandwich(self):
        self.assertEqual(len(self.plan["captures"]), 13)
        by_request: dict[str, list[str]] = {}
        for step in self.plan["captures"]:
            by_request.setdefault(step["w13c_request"], []).append(
                step["w13c_step"])
        self.assertEqual(len(by_request), 6)
        for request, steps in by_request.items():
            cold = int(request.split("/")[0]) >= guide13_w13c.W13C_COLD_CCT
            expected = (["raybefore", "strip", "rayafter"] if cold
                        else ["ray", "strip"])
            self.assertEqual(steps, expected, request)

    def test_strip_commands_are_the_corrected_advisor_candidates(self):
        commands = self.plan["analysis_contract"]["corrected_commands"]
        self.assertEqual(
            commands["1850/50"], ADVISOR_CORRECTED["1850/50"])
        self.assertEqual(
            commands["2400/50"], ADVISOR_CORRECTED["2400/50"])
        for key, command in commands.items():
            self.assertEqual(max(command.values()), 4095, key)

    def test_corrected_brightness_prediction_keeps_exposure_ceiling(self):
        for cct, gm in guide13_w13c.W13C_REQUESTS:
            sel = guide13_w13c.select_strip_shutter(LUT, BRIGHTNESS, cct, gm)
            self.assertLessEqual(
                sel["pred_max"], guide13_w13c.W13C_BRIGHTNESS_CEILING_DN,
                (cct, gm))
            # one third stop slower would exceed the ceiling (slowest rule)
            denom = int(sel["shutter"].split("/")[1])
            slower = max(
                d for d in guide13_w13c.W13C_SHUTTER_LADDER if d < denom)
            self.assertGreater(
                sel["dn_per_1over"] / slower,
                guide13_w13c.W13C_BRIGHTNESS_CEILING_DN, (cct, gm))

    def test_corrected_weights_reproduce_node_brightness_at_nodes(self):
        for node in LUT[::17]:  # sample across the grid
            key = f"{node['cct']}/{node['gm']}"
            pred = guide13_w13c.predict_strip_max_dn(
                LUT, BRIGHTNESS, int(node["cct"]), int(node["gm"]))
            self.assertAlmostEqual(
                pred, float(BRIGHTNESS[key]["dn_per_1over"]), places=6, msg=key)

    def test_plan_ledger_and_budgets_are_frozen(self):
        frozen = self.plan["frozen_shutters"]
        self.assertEqual(
            sorted(frozen),
            sorted(self.plan["shutter_ledger_provenance"]
                   ["required_cache_keys"]))
        for step in self.plan["captures"]:
            self.assertEqual(
                frozen[step["exposure_cache_key"]], step["nominal_shutter"])
            if step["source_id"] == "strip":
                self.assertEqual(
                    step["command"], step["w13c_corrected_command"])
        self.assertEqual(self.plan["budgets"]["formal_cap"], 13)
        self.assertEqual(self.plan["budgets"]["retry"], 0)
        self.assertEqual(
            self.plan["execution_authorization"]["schema"],
            guide13_w13c.W13C_AUTHORIZATION_SCHEMA,
        )
        self.assertIn("NOT independent holdouts",
                      self.plan["analysis_contract"]["role"])


if __name__ == "__main__":
    unittest.main()
