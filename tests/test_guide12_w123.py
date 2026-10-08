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


if __name__ == "__main__":
    unittest.main()
