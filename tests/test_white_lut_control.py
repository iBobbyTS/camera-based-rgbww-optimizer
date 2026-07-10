import json
import tempfile
import unittest
from pathlib import Path

from camera_based_rgbww_optimizer.control import white_lut


def lut_data():
    targets = []
    for cct, cct_offset in ((2000, 0), (4000, 1000)):
        for gm, gm_offset in ((0, 0), (200, 200)):
            targets.append({
                "cct": cct,
                "gm": gm,
                "selected_command": {
                    "cw": 4095,
                    "ww": cct_offset,
                    "r": gm_offset,
                    "g": cct_offset + gm_offset,
                    "b": 0,
                },
            })
    return {"version": 1, "status": "complete", "targets": targets}


class WhiteLutControlTests(unittest.TestCase):
    def test_exact_grid_point_returns_measured_command(self):
        result = white_lut.interpolate_white_lut(lut_data(), 2000, 200)

        self.assertEqual(
            result["command"],
            {"cw": 4095, "ww": 0, "r": 200, "g": 200, "b": 0},
        )
        self.assertFalse(result["clamped"])

    def test_bilinear_interpolation_uses_both_cct_and_gm_axes(self):
        result = white_lut.interpolate_white_lut(lut_data(), 3000, 100)

        self.assertEqual(
            result["command"],
            {"cw": 4095, "ww": 500, "r": 100, "g": 600, "b": 0},
        )
        self.assertEqual(result["bracket"]["cct_ratio"], 0.5)
        self.assertEqual(result["bracket"]["gm_ratio"], 0.5)

    def test_out_of_range_values_require_explicit_clamp(self):
        with self.assertRaisesRegex(ValueError, "outside LUT range"):
            white_lut.interpolate_white_lut(lut_data(), 1800, 100)

        result = white_lut.interpolate_white_lut(lut_data(), 1800, 300, clamp=True)

        self.assertEqual(result["resolved"], {"cct": 2000.0, "gm": 200.0})
        self.assertTrue(result["clamped"])

    def test_incomplete_grid_is_rejected(self):
        data = lut_data()
        data["targets"].pop()

        with self.assertRaisesRegex(ValueError, "grid is incomplete"):
            white_lut.interpolate_white_lut(data, 3000, 100)

    def test_set_white_scales_linear_command_before_calling_esphome(self):
        calls = []

        def fake_light(cw, ww, r, g, b, **kwargs):
            calls.append({"cw": cw, "ww": ww, "r": r, "g": g, "b": b, **kwargs})
            return {"cold_white": cw, "warm_white": ww, "red": r, "green": g, "blue": b}

        with tempfile.TemporaryDirectory() as tmpdir:
            lut_path = Path(tmpdir) / "white-lut.json"
            lut_path.write_text(json.dumps(lut_data()), encoding="utf-8")
            result = white_lut.set_white_from_lut(
                lut_path=lut_path,
                cct=3000,
                gm=100,
                intensity_percent=50,
                host="strip.local",
                port=6053,
                expected_name="strip",
                curve_path=None,
                light_fn=fake_light,
            )

        self.assertEqual(result["command"], {"cw": 2048, "ww": 250, "r": 50, "g": 300, "b": 0})
        self.assertEqual(calls[0]["cw"], 2048)
        self.assertEqual(calls[0]["host"], "strip.local")
        self.assertFalse(result["dry_run"])

    def test_dry_run_does_not_call_esphome(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            lut_path = Path(tmpdir) / "white-lut.json"
            lut_path.write_text(json.dumps(lut_data()), encoding="utf-8")
            result = white_lut.set_white_from_lut(
                lut_path=lut_path,
                cct=3000,
                gm=100,
                dry_run=True,
                light_fn=lambda *args, **kwargs: self.fail("light_fn should not be called"),
            )

        self.assertIsNone(result["payload"])
        self.assertTrue(result["dry_run"])


if __name__ == "__main__":
    unittest.main()
