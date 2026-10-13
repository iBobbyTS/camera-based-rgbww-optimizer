"""Behavior tests for the GUIDE13 W13-A node-correction adapter."""
from __future__ import annotations

import json
import unittest
from pathlib import Path

from camera_based_rgbww_optimizer.optimization import guide13_w13a

QUEUE = json.loads(Path(
    "D:/rgbww-optimizer/guide13/derived/w13a-open-queue-20261013.json"
).read_text(encoding="utf-8"))


class W13AAdapterTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.row_6500_130 = next(
            r for r in QUEUE["nodes"] if r["node"] == "6500/130")
        cls.row_20000_70 = next(
            r for r in QUEUE["nodes"] if r["node"] == "20000/70")

    def test_node_adapter_maps_queue_row_to_block_node_shape(self):
        node = guide13_w13a.w13a_node_from_queue_row(self.row_6500_130)
        self.assertEqual((node["cct"], node["gm"]), (6500, 130))
        # 6500/130 = (cw4095, ww0, r3, g165, b0): cold_white face
        self.assertEqual(node["face_channels"], ["cold_white"])
        self.assertEqual(node["base_command"]["cw"], 4095)
        self.assertEqual(node["E_vs_fresh_ray"], self.row_6500_130["E_max"])

    def test_first_block_is_base_repeat_plus_three_probes(self):
        candidates = guide13_w13a.w13a_first_block_candidates(
            self.row_6500_130)
        self.assertEqual(candidates[0]["tag"], "u0_repeat")
        self.assertFalse(candidates[0]["new_unique_command"])
        probes = [c for c in candidates[1:]]
        self.assertEqual(len(probes), 3)
        self.assertTrue(all(c["new_unique_command"] for c in probes))
        # the face channel (cold_white) is never probed; all codes legal
        for c in probes:
            self.assertNotEqual(c["tag"], "probe_cw")
            self.assertLessEqual(
                max(c["command"].values()), 4095, c["tag"])
            self.assertGreaterEqual(min(c["command"].values()), 0, c["tag"])

    def test_block_plan_carries_guide13_identity_and_w12_contract(self):
        candidates = guide13_w13a.w13a_first_block_candidates(
            self.row_6500_130)
        plan = guide13_w13a.build_guide13_w13a_block_plan(
            self.row_6500_130, candidates, block_index=1)
        self.assertEqual(
            plan["guide_experiment_id"],
            guide13_w13a.W13A_EXPERIMENT_ID)
        self.assertEqual(
            plan["execution_authorization"]["experiment_id"],
            guide13_w13a.W13A_EXPERIMENT_ID)
        self.assertEqual(
            plan["execution_authorization"]["schema"],
            "direct_guide12_w12_fullscale_bounded_v1")
        # W12-1 block structure: ray before + 4 strip + ray after
        self.assertEqual(len(plan["captures"]), 6)
        self.assertEqual(
            [s["source_id"] for s in plan["captures"]],
            ["ray", "strip", "strip", "strip", "strip", "ray"])
        self.assertEqual(
            plan["analysis_contract"]["method"],
            "guide13_w13_a_bounded_node_correction_block")

    def test_bright_family_gets_frozen_shutter_override(self):
        self.assertEqual(
            guide13_w13a.w13a_strip_shutter(20000, 70), "1/125")
        self.assertIsNone(guide13_w13a.w13a_strip_shutter(6500, 130))

    def test_queue_rules_frozen(self):
        self.assertEqual(QUEUE["rules"]["active_node_cap"], 30)
        self.assertEqual(
            QUEUE["rules"]["new_unique_commands_per_node"], 8)
        self.assertEqual(len(QUEUE["nodes"]), 32)


if __name__ == "__main__":
    unittest.main()
