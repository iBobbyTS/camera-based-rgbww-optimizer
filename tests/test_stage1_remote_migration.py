import hashlib
import json
import unittest
from pathlib import Path

from camera_based_rgbww_optimizer.measurement import raw_mosaic_patches
from camera_based_rgbww_optimizer.optimization import (
    measure_channel_response,
    measure_raw_observer_validation,
    measure_raw_shutter_response,
    measure_white_endpoints,
    measure_white_lut,
)


class Stage1RemoteMigrationTests(unittest.TestCase):
    EXPECTED_NAME = "locations-20260714-211759.json"
    EXPECTED_SHA256 = "21f02328bff8b5ffcfc10c767e15cdefbf8bb883bc352eff6f0fb7ade38a8f80"

    def test_every_formal_runner_defaults_to_latest_location(self):
        defaults = (
            raw_mosaic_patches.DEFAULT_LOCATION_CONFIG,
            measure_raw_observer_validation.DEFAULT_LOCATION_CONFIG,
            measure_raw_shutter_response.DEFAULT_LOCATION_CONFIG,
            measure_white_endpoints.DEFAULT_LOCATION_CONFIG,
            measure_white_lut.DEFAULT_LOCATION_CONFIG,
            measure_channel_response.DEFAULT_AUTO_EXPOSURE_METERING_LOCATION_CONFIG,
        )
        self.assertTrue(all(Path(path).name == self.EXPECTED_NAME for path in defaults))

    def test_latest_location_geometry_and_hash_are_frozen(self):
        path = measure_raw_observer_validation.DEFAULT_LOCATION_CONFIG
        payload = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), self.EXPECTED_SHA256)
        self.assertEqual(payload["image"], {"width": 4320, "height": 2880})
        self.assertEqual(payload["chart"]["orientation_degrees"], 180)
        self.assertEqual(len(payload["blocks"]), 24)


if __name__ == "__main__":
    unittest.main()
