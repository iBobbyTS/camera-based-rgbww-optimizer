"""Behavior tests for the GUIDE12 W12-2 verification plan builder."""
from __future__ import annotations

import json
import unittest
from pathlib import Path

from camera_based_rgbww_optimizer.optimization import guide12

LUT = json.loads(Path(
    "D:/rgbww-optimizer/guide12-w122/derived/w12-2-frozen-lut-20261005.json"
).read_text(encoding="utf-8"))


class Guide12W122VerificationPlanTests(unittest.TestCase):
    def test_six_batches_cover_the_frozen_lut_exactly_once(self):
        seen: set[tuple[int, int]] = set()
        for batch in guide12.W122_BATCHES:
            plan = guide12.build_guide12_w122_verification_plan(
                LUT["nodes"], batch,
            )
            batch_nodes = {
                tuple(int(x) for x in step["w122_node"].split("/"))
                for step in plan["captures"] if "w122_node" in step
            }
            self.assertFalse(seen & batch_nodes, f"node in two batches: {batch}")
            seen |= batch_nodes
        self.assertEqual(len(seen), 70)

    def test_batch_frame_counts_match_the_frozen_campaign(self):
        counts = {}
        for batch, expected in (
            ("warm", 38), ("mid", 38), ("high", 34),
            ("veryhigh", 36), ("cold14k", 18), ("cold20k", 21),
        ):
            plan = guide12.build_guide12_w122_verification_plan(
                LUT["nodes"], batch,
                include_s0_reference=(batch == "warm"),
            )
            counts[batch] = len(plan["captures"])
            self.assertEqual(len(plan["captures"]), expected + (1 if batch == "warm" else 0))
        self.assertEqual(sum(counts.values()), 186)

    def test_every_node_is_a_source_pair_with_ray_before_strip(self):
        plan = guide12.build_guide12_w122_verification_plan(LUT["nodes"], "warm")
        by_node: dict[str, list[str]] = {}
        for step in plan["captures"]:
            if "w122_node" in step:
                by_node.setdefault(
                    f"{step['w122_node']}_r{step['w122_repeat']}", []
                ).append(f"{step['w122_step']}:{step['source_id']}")
        for group, steps in by_node.items():
            if "cold" in group:
                continue
            self.assertEqual(steps, ["ray:ray", "strip:strip"], group)

    def test_cold_nodes_sandwich_strip_between_ray_references(self):
        plan = guide12.build_guide12_w122_verification_plan(LUT["nodes"], "cold20k")
        by_group: dict[str, list[str]] = {}
        for step in plan["captures"]:
            by_group.setdefault(
                f"{step['w122_node']}_r{step['w122_repeat']}", []
            ).append(step["w122_step"])
        for group, steps in by_group.items():
            if group.startswith("20000"):
                self.assertEqual(steps, ["raybefore", "strip", "rayafter"], group)

    def test_strip_commands_are_verbatim_from_the_frozen_lut(self):
        lut_by_node = {
            f"{n['cct']}/{n['gm']}": n["command"] for n in LUT["nodes"]
        }
        plan = guide12.build_guide12_w122_verification_plan(LUT["nodes"], "mid")
        for step in plan["captures"]:
            if step["source_id"] != "strip":
                continue
            expected = lut_by_node[step["w122_node"]]
            self.assertEqual(step["command"], expected, step["w122_node"])

    def test_changed_nodes_get_two_independent_repeats(self):
        plan = guide12.build_guide12_w122_verification_plan(LUT["nodes"], "mid")
        repeats: dict[str, set[int]] = {}
        for step in plan["captures"]:
            if "w122_node" in step:
                repeats.setdefault(step["w122_node"], set()).add(step["w122_repeat"])
        changed = [n for n in LUT["nodes"] if n["verification_class"] == "needs_two_pairs"]
        for node in changed:
            key = f"{node['cct']}/{node['gm']}"
            if key in repeats:
                self.assertEqual(repeats[key], {1, 2}, key)

    def test_shutter_ledger_and_authorization(self):
        plan = guide12.build_guide12_w122_verification_plan(LUT["nodes"], "cold20k")
        frozen = plan["frozen_shutters"]
        self.assertEqual(
            sorted(frozen),
            sorted(plan["shutter_ledger_provenance"]["required_cache_keys"]),
        )
        for step in plan["captures"]:
            self.assertEqual(frozen[step["exposure_cache_key"]], step["nominal_shutter"])
        self.assertEqual(
            plan["execution_authorization"]["schema"],
            "direct_guide12_w122_verification_v1",
        )
        self.assertEqual(plan["budgets"]["ambient_cap"], 0)

    def test_unknown_batch_rejected(self):
        with self.assertRaises(ValueError):
            guide12.build_guide12_w122_verification_plan(LUT["nodes"], "nonexistent")


if __name__ == "__main__":
    unittest.main()
