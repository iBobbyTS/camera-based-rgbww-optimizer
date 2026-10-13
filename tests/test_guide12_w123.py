"""Behavior tests for the GUIDE12 W12-3 runtime interpolation."""
from __future__ import annotations

import json
import unittest
from pathlib import Path

from camera_based_rgbww_optimizer.optimization import guide12_w123

LUT = json.loads(Path(
    "D:/rgbww-optimizer/guide12-w122/derived/w12-2-frozen-lut-20261005.json"
).read_text(encoding="utf-8"))["nodes"]
SHUTTERS = json.loads(Path(
    "D:/rgbww-optimizer/guide12-w122/derived/w123-strip-shutters-20261008.json"
).read_text(encoding="utf-8"))


class Guide12W123InterpolationTests(unittest.TestCase):
    def test_interpolation_is_always_actual_fullscale(self):
        for cct, gm in guide12_w123.W123_REQUESTS:
            result = guide12_w123.interpolate_fullscale_command(LUT, cct, gm)
            self.assertEqual(max(result["command"].values()), 4095, (cct, gm))
            self.assertEqual(
                min(result["command"].values()) >= 0, True, (cct, gm))

    def test_requests_are_non_node_and_cover_required_structure(self):
        node_coords = {(int(n["cct"]), int(n["gm"])) for n in LUT}
        for cct, gm in guide12_w123.W123_REQUESTS:
            self.assertNotIn((cct, gm), node_coords)
        ccts = {cct for cct, _ in guide12_w123.W123_REQUESTS}
        gms = {gm for _, gm in guide12_w123.W123_REQUESTS}
        self.assertTrue(any(c < 3200 for c in ccts))          # warm span
        self.assertTrue(any(c > 14000 for c in ccts))         # cold span
        self.assertTrue(any(g < 100 for g in gms))            # GM one side
        self.assertTrue(any(g > 100 for g in gms))            # GM other side
        self.assertIn((5350, 105), guide12_w123.W123_REQUESTS)  # ~5300/100
        self.assertIn((6050, 160), guide12_w123.W123_REQUESTS)  # ~6100/165

    def test_out_of_grid_requests_fail_closed(self):
        with self.assertRaises(ValueError):
            guide12_w123.interpolate_fullscale_command(LUT, 1000, 100)
        with self.assertRaises(ValueError):
            guide12_w123.interpolate_fullscale_command(LUT, 5000, 250)

    def test_face_switching_is_observed_across_requests(self):
        faces = {
            guide12_w123.interpolate_fullscale_command(LUT, c, g)["winning_channel"]
            for c, g in guide12_w123.W123_REQUESTS
        }
        self.assertGreaterEqual(len(faces), 3, faces)

    def test_plan_frame_counts_and_cold_sandwich(self):
        plan = guide12_w123.build_guide12_w123_request_plan(
            LUT, strip_shutters=SHUTTERS, include_s0_reference=True,
        )
        self.assertEqual(len(plan["captures"]), 43)
        by_request: dict[str, list[str]] = {}
        for step in plan["captures"]:
            if "w123_request" in step:
                by_request.setdefault(step["w123_request"], []).append(
                    step["w123_step"])
        for request, steps in by_request.items():
            cct = int(request.split("/")[0])
            if cct >= guide12_w123.W123_COLD_CCT:
                self.assertEqual(steps, ["raybefore", "strip", "rayafter"], request)
            else:
                self.assertEqual(steps, ["ray", "strip"], request)
        self.assertEqual(
            plan["execution_authorization"]["schema"],
            "direct_guide12_w123_interpolation_v1",
        )

    def test_shutter_ledger_complete_and_commands_frozen_in_plan(self):
        plan = guide12_w123.build_guide12_w123_request_plan(
            LUT, strip_shutters=SHUTTERS,
        )
        frozen = plan["frozen_shutters"]
        self.assertEqual(
            sorted(frozen),
            sorted(plan["shutter_ledger_provenance"]["required_cache_keys"]),
        )
        for step in plan["captures"]:
            self.assertEqual(frozen[step["exposure_cache_key"]], step["nominal_shutter"])
        for command in plan["analysis_contract"]["interpolated_commands"].values():
            self.assertEqual(max(command.values()), 4095)


class Guide13MiredWeightCorrectionTests(unittest.TestCase):
    """GUIDE13 §W13-C: the T0 (lower cct / higher mired) corner must carry
    weight a=(m-m1)/(m0-m1). Expected values below are written out
    independently (advisor audit numbers and hand arithmetic), never by
    calling the function under test."""

    def test_all_70_nodes_reproduce_their_frozen_command_exactly(self):
        for node in LUT:
            result = guide12_w123.interpolate_fullscale_command(
                LUT, int(node["cct"]), int(node["gm"]))
            self.assertEqual(
                result["command"], {k: int(v) for k, v in node["command"].items()},
                (node["cct"], node["gm"]),
            )

    def test_warm_node_identity_after_correction(self):
        # 1800/100 must be its own command, not the 2000-node mix the
        # pre-GUIDE13 function returned (advisor interpolation_audit).
        result = guide12_w123.interpolate_fullscale_command(LUT, 1800, 100)
        self.assertEqual(
            result["command"],
            {"cw": 0, "ww": 0, "r": 4095, "g": 1197, "b": 0},
        )

    def test_two_sided_bracket_matches_independent_bilinear_arithmetic(self):
        # request 2100/100 sits between T0=2000 (m0=500) and T1=2300
        # (m1=1e6/2300); a=(m-m1)/(m0-m1) weights the LOWER cct node.
        cmd2000 = {"cw": 79.0, "ww": 51.0, "r": 4095.0, "g": 1435.0, "b": 1.0}
        cmd2300 = {"cw": 0.0, "ww": 4095.0, "r": 2015.0, "g": 371.0, "b": 0.0}
        a = (1e6 / 2100 - 1e6 / 2300) / (1e6 / 2000 - 1e6 / 2300)
        raw = {ch: a * cmd2000[ch] + (1 - a) * cmd2300[ch] for ch in cmd2000}
        peak = max(raw.values())
        expected = {
            ch: max(0, min(4095, int(raw[ch] * 4095 / peak + 0.5)))
            for ch in raw
        }
        result = guide12_w123.interpolate_fullscale_command(LUT, 2100, 100)
        self.assertEqual(result["command"], expected)
        self.assertEqual(expected["r"], 4095)  # winner projected, not clipped

    def test_constant_grid_returns_the_constant_command(self):
        const = {"cw": 1000, "ww": 2000, "r": 4095, "g": 500, "b": 300}
        nodes = [
            {"cct": c, "gm": g, "command": dict(const)}
            for c in (3000, 4000) for g in (0, 70, 100, 130, 200)
        ]
        for cct, gm in ((3200, 40), (3000, 100), (4000, 0), (3500, 170)):
            result = guide12_w123.interpolate_fullscale_command(nodes, cct, gm)
            self.assertEqual(result["command"], const, (cct, gm))

    def test_weight_moves_continuously_toward_the_nearer_node(self):
        near = guide12_w123.interpolate_fullscale_command(LUT, 2001, 100)["command"]
        far = guide12_w123.interpolate_fullscale_command(LUT, 2299, 100)["command"]
        node2000 = {k: int(v) for k, v in next(
            n for n in LUT if n["cct"] == 2000 and n["gm"] == 100)["command"].items()}
        node2300 = {k: int(v) for k, v in next(
            n for n in LUT if n["cct"] == 2300 and n["gm"] == 100)["command"].items()}
        d_near = sum(abs(near[ch] - node2000[ch]) for ch in node2000)
        d_far = sum(abs(far[ch] - node2000[ch]) for ch in node2000)
        self.assertLess(d_near, d_far)
        self.assertLess(
            sum(abs(far[ch] - node2300[ch]) for ch in node2300),
            sum(abs(near[ch] - node2300[ch]) for ch in node2300),
        )

    def test_advisor_corrected_candidates_are_reproduced(self):
        # Frozen advisor counterfactuals (independent expected values).
        for request, expected in (
            ((1850, 50), {"cw": 72, "ww": 2095, "r": 4095, "g": 728, "b": 26}),
            ((2100, 170), {"cw": 0, "ww": 1495, "r": 4095, "g": 1398, "b": 0}),
            ((2400, 50), {"cw": 279, "ww": 3045, "r": 4095, "g": 1350, "b": 362}),
        ):
            result = guide12_w123.interpolate_fullscale_command(LUT, *request)
            self.assertEqual(result["command"], expected, request)


if __name__ == "__main__":
    unittest.main()
