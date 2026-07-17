import json
import tempfile
import unittest
from pathlib import Path

import numpy as np

from camera_based_rgbww_optimizer.measurement import raw_mosaic_patches


def make_config(
    *,
    minimum_pixels=1,
    maximum_clipped_fraction=1.0,
    maximum_near_noise_floor_fraction=1.0,
    maximum_nonfinite_fraction=0.0,
    combine_green=True,
):
    return {
        "version": 1,
        "statistics": {
            "trim_fraction": 0.1,
            "noise_floor_margin_normalized": 0.005,
            "clipping_margin_normalized": 0.0,
            "combine_green": combine_green,
        },
        "quality_thresholds": {
            "minimum_valid_pixels_per_plane": minimum_pixels,
            "maximum_nonfinite_fraction": maximum_nonfinite_fraction,
            "maximum_clipped_fraction": maximum_clipped_fraction,
            "maximum_near_noise_floor_fraction": maximum_near_noise_floor_fraction,
        },
        "raw_metadata": {"minimum_camera_white_to_global_ratio": 0.5},
        "patch_policy": {"diagnostic_only_roles": ["black", "ambient_check"]},
    }


def make_frame(
    mosaic,
    *,
    pattern=((0, 1), (3, 2)),
    color_desc="RGBG",
    black_levels=(0, 0, 0, 0),
    white_level=1000,
    camera_white_levels=None,
):
    return raw_mosaic_patches.RawMosaicFrame(
        source_file=Path("synthetic.raw"),
        mosaic=np.asarray(mosaic),
        raw_pattern=np.asarray(pattern),
        color_desc=color_desc,
        black_levels=tuple(black_levels),
        white_level=float(white_level),
        camera_white_levels=(
            None if camera_white_levels is None else tuple(float(value) for value in camera_white_levels)
        ),
        metadata={"kind": "synthetic"},
    )


def full_region(name="patch"):
    return {"type": "full", "name": name}


def analyze(frame, *, exposure=1.0, regions=None, config=None):
    return raw_mosaic_patches.analyze_mosaic_patches(
        frame,
        regions=regions or [full_region()],
        exposure_seconds=exposure,
        observer_config=config or make_config(),
    )


class RawMosaicCfaTests(unittest.TestCase):
    def test_recovers_implausible_black_metadata_from_optical_margins(self):
        raw_image = np.full((48, 48), 512, dtype="uint16")
        raw_image[8:, 8:] = 3000

        levels, metadata = raw_mosaic_patches._resolve_black_levels(
            reported_black_levels=(0, 44, 124, 90),
            raw_image=raw_image,
            raw_pattern=np.asarray(((0, 1), (3, 2))),
            top_margin=8,
            left_margin=8,
            white_level=16383,
        )

        self.assertEqual(levels, (512.0, 512.0, 512.0, 512.0))
        self.assertEqual(metadata["black_level_per_channel_reported"], [0.0, 44.0, 124.0, 90.0])
        self.assertEqual(metadata["black_level_source_per_channel"], ["optical_black_margin_fallback"] * 4)

    def test_keeps_black_metadata_when_optical_margins_agree(self):
        raw_image = np.full((48, 48), 512, dtype="uint16")
        raw_image[8:, 8:] = 3000

        levels, metadata = raw_mosaic_patches._resolve_black_levels(
            reported_black_levels=(512, 512, 512, 512),
            raw_image=raw_image,
            raw_pattern=np.asarray(((0, 1), (3, 2))),
            top_margin=8,
            left_margin=8,
            white_level=16383,
        )

        self.assertEqual(levels, (512.0, 512.0, 512.0, 512.0))
        self.assertEqual(metadata["black_level_source_per_channel"], ["metadata"] * 4)

    def test_does_not_treat_saturated_optical_margins_as_black(self):
        raw_image = np.full((48, 48), 16383, dtype="uint16")

        levels, metadata = raw_mosaic_patches._resolve_black_levels(
            reported_black_levels=(0, 32, 96, 64),
            raw_image=raw_image,
            raw_pattern=np.asarray(((0, 1), (3, 2))),
            top_margin=8,
            left_margin=8,
            white_level=16383,
        )

        self.assertEqual(levels, (0.0, 32.0, 96.0, 64.0))
        self.assertEqual(metadata["optical_black_level_per_channel"], [16383.0] * 4)
        self.assertEqual(metadata["black_level_source_per_channel"], ["metadata"] * 4)

    def test_resolves_all_standard_bayer_patterns(self):
        patterns = {
            "RGGB": ((0, 1), (3, 2)),
            "BGGR": ((2, 1), (3, 0)),
            "GRBG": ((1, 0), (2, 3)),
            "GBRG": ((1, 2), (0, 3)),
        }
        for expected, pattern in patterns.items():
            with self.subTest(pattern=expected):
                frame = make_frame(np.ones((4, 4)), pattern=pattern)
                descriptors = raw_mosaic_patches.describe_cfa_planes(
                    frame,
                    minimum_camera_white_to_global_ratio=0.5,
                )
                labels = descriptors[0]["pattern_labels"]
                color_codes = "".join(label[0] for row in labels for label in row)

                self.assertEqual(color_codes, expected)
                self.assertEqual([item["label"] for item in descriptors], ["R", "G1", "G2", "B"])

    def test_supports_repeated_green_color_index(self):
        frame = make_frame(
            np.ones((4, 4)),
            pattern=((0, 1), (1, 2)),
            color_desc="RGB",
            black_levels=(0, 0, 0),
        )

        descriptors = raw_mosaic_patches.describe_cfa_planes(
            frame,
            minimum_camera_white_to_global_ratio=0.5,
        )

        self.assertEqual(descriptors[1]["color_index"], 1)
        self.assertEqual(descriptors[2]["color_index"], 1)
        self.assertEqual(descriptors[1]["label"], "G1")
        self.assertEqual(descriptors[2]["label"], "G2")

    def test_applies_per_color_black_levels(self):
        frame = make_frame(
            [[550, 600], [700, 650]],
            black_levels=(100, 200, 300, 400),
            white_level=1000,
        )

        report = analyze(frame)

        for label in raw_mosaic_patches.PLANE_ORDER:
            value = report["patches"][0]["planes"][label]["statistics"][
                "black_corrected_normalized"
            ]["median"]
            self.assertAlmostEqual(value, 0.5)

    def test_falls_back_from_implausible_camera_white_levels(self):
        frame = make_frame(
            np.full((4, 4), 500),
            white_level=1000,
            camera_white_levels=(100, 100, 100, 100),
        )

        descriptors = raw_mosaic_patches.describe_cfa_planes(
            frame,
            minimum_camera_white_to_global_ratio=0.5,
        )

        self.assertTrue(
            all(item["effective_white_level_source"] == "global_white_level_fallback" for item in descriptors)
        )
        self.assertTrue(all(item["effective_white_level"] == 1000 for item in descriptors))


class RawMosaicRegionTests(unittest.TestCase):
    def test_odd_roi_preserves_global_cfa_parity(self):
        frame = make_frame(np.full((5, 5), 500))
        region = {"type": "roi", "name": "odd", "x": 1, "y": 0, "width": 3, "height": 5}

        report = analyze(frame, regions=[region])
        counts = {
            label: report["patches"][0]["planes"][label]["metrics"]["selected_pixel_count"]
            for label in raw_mosaic_patches.PLANE_ORDER
        }

        self.assertEqual(counts, {"R": 3, "G1": 6, "G2": 2, "B": 4})

    def test_rejects_roi_and_polygon_outside_mosaic(self):
        frame = make_frame(np.full((4, 4), 500))
        bad_regions = [
            {"type": "roi", "name": "roi", "x": 3, "y": 0, "width": 2, "height": 1},
            {
                "type": "polygon",
                "name": "polygon",
                "points": [(0.0, 0.0), (5.0, 0.0), (5.0, 1.0), (0.0, 1.0)],
            },
        ]
        for region in bad_regions:
            with self.subTest(region=region["type"]), self.assertRaisesRegex(ValueError, "bounds"):
                analyze(frame, regions=[region])

    def test_maps_location_coordinates_to_visible_mosaic(self):
        regions = [
            {
                "type": "polygon",
                "name": "block_01",
                "points": [(2.0, 2.0), (8.0, 2.0), (8.0, 8.0), (2.0, 8.0)],
            }
        ]

        mapped = raw_mosaic_patches.map_regions_to_mosaic(
            regions,
            source_size=(10, 10),
            target_shape=(5, 5),
        )

        self.assertEqual(mapped[0]["points"], [(1.0, 1.0), (4.0, 1.0), (4.0, 4.0), (1.0, 4.0)])

    def test_empty_cfa_planes_are_reported_without_nan(self):
        frame = make_frame([[np.nan, 100], [100, 100]])
        region = {"type": "roi", "name": "single", "x": 0, "y": 0, "width": 1, "height": 1}

        report = analyze(frame, regions=[region])

        red = report["patches"][0]["planes"]["R"]
        green = report["patches"][0]["planes"]["G1"]
        self.assertEqual(red["metrics"]["selected_pixel_count"], 1)
        self.assertEqual(red["metrics"]["valid_pixel_count"], 0)
        self.assertIsNone(red["statistics"]["normalized_per_second"]["median"])
        self.assertEqual(green["metrics"]["selected_pixel_count"], 0)
        self.assertEqual(green["quality"]["status"], "rejected")
        json.dumps(report, allow_nan=False)


class RawMosaicStatisticsTests(unittest.TestCase):
    def test_native_exposure_meter_normalizes_patch_plane_max_to_16bit_scale(self):
        meter = raw_mosaic_patches.meter_mosaic_exposure(
            make_frame(np.full((4, 4), 500)),
            regions=[full_region()],
            observer_config=make_config(),
        )

        self.assertEqual(meter.exposure_metric, 32768)
        self.assertEqual(meter.raw_visible_max, 500)
        self.assertEqual(meter.plane_max, {"R": 0.5, "G1": 0.5, "G2": 0.5, "B": 0.5})
        self.assertEqual(meter.clipped_fraction, 0.0)
        self.assertEqual(meter.low_signal_fraction, 0.0)
        self.assertEqual(meter.quality_status, "accepted")
        json.dumps(meter.to_jsonable(), allow_nan=False)

    def test_native_exposure_meter_aggregates_clipping_and_low_signal_by_valid_pixels(self):
        mosaic = np.array([[1000, 500], [0, 500]])
        meter = raw_mosaic_patches.meter_mosaic_exposure(
            make_frame(mosaic),
            regions=[full_region()],
            observer_config=make_config(maximum_clipped_fraction=0.0),
        )

        self.assertEqual(meter.exposure_metric, 65535)
        self.assertAlmostEqual(meter.clipped_fraction, 0.25)
        self.assertAlmostEqual(meter.low_signal_fraction, 0.25)
        self.assertEqual(meter.quality_status, "rejected")

    def test_exposure_normalization_matches_synthetic_linear_signal(self):
        half_second = analyze(make_frame(np.full((4, 4), 100)), exposure=0.5)
        one_second = analyze(make_frame(np.full((4, 4), 200)), exposure=1.0)

        for label in raw_mosaic_patches.PLANE_ORDER:
            half_value = half_second["patches"][0]["planes"][label]["statistics"][
                "normalized_per_second"
            ]["trimmed_mean"]
            full_value = one_second["patches"][0]["planes"][label]["statistics"][
                "normalized_per_second"
            ]["trimmed_mean"]
            self.assertAlmostEqual(half_value, 0.2)
            self.assertAlmostEqual(half_value, full_value)

    def test_ambient_is_normalized_before_subtraction(self):
        signal = analyze(make_frame(np.full((4, 4), 300)), exposure=0.5)
        ambient = analyze(make_frame(np.full((4, 4), 100)), exposure=1.0)

        result = raw_mosaic_patches.apply_ambient_subtraction(signal, ambient)

        for label in raw_mosaic_patches.PLANE_ORDER:
            value = result["patches"][0]["planes"][label]["ambient_subtracted"][
                "trimmed_mean_per_second"
            ]
            self.assertAlmostEqual(value, 0.5)

    def test_combines_g1_and_g2_after_exposure_normalization(self):
        mosaic = np.array([[300, 200], [400, 300]])

        report = analyze(make_frame(mosaic))

        combined = report["patches"][0]["combined_green"]
        self.assertAlmostEqual(combined["normalized_per_second"]["trimmed_mean"], 0.3)
        self.assertAlmostEqual(combined["g1_to_g2_trimmed_mean_ratio"], 0.5)

    def test_single_plane_clipping_does_not_mark_other_planes(self):
        mosaic = np.full((4, 4), 500)
        mosaic[0::2, 0::2] = 1000
        config = make_config(maximum_clipped_fraction=0.0)

        report = analyze(make_frame(mosaic), config=config)

        planes = report["patches"][0]["planes"]
        self.assertEqual(planes["R"]["quality"]["status"], "rejected")
        self.assertIn("clipped_fraction_exceeded", planes["R"]["quality"]["failures"])
        self.assertEqual(planes["G1"]["quality"]["status"], "accepted")
        self.assertEqual(planes["G2"]["quality"]["status"], "accepted")
        self.assertEqual(planes["B"]["quality"]["status"], "accepted")

    def test_default_config_applies_validated_quality_gates(self):
        config = raw_mosaic_patches.load_observer_config()

        report = analyze(make_frame(np.full((400, 400), 500)), config=config)

        self.assertEqual(report["quality"]["status"], "accepted")
        self.assertTrue(report["quality"]["accepted_for_optimization"])
        self.assertNotIn("combined_green", report["patches"][0])

    def test_black_role_is_diagnostic_only(self):
        region = {
            "type": "full",
            "name": "black",
            "patch": {"roles": ["neutral", "black", "ambient_check"]},
        }
        config = make_config(maximum_near_noise_floor_fraction=0.0)

        report = analyze(make_frame(np.zeros((4, 4))), regions=[region], config=config)

        self.assertFalse(report["patches"][0]["optimization_eligible"])
        self.assertEqual(report["patches"][0]["quality_status"], "diagnostic_only")
        self.assertEqual(report["quality"]["optimization_patch_count"], 0)
        self.assertEqual(report["quality"]["status"], "no_optimization_patches")
        self.assertFalse(report["quality"]["accepted_for_optimization"])


class RawMosaicCliTests(unittest.TestCase):
    def test_parse_exposure_accepts_fraction(self):
        self.assertAlmostEqual(raw_mosaic_patches.parse_exposure_seconds("1/125"), 0.008)

    def test_write_report_rejects_non_json_numbers(self):
        with tempfile.TemporaryDirectory(dir=raw_mosaic_patches.PROJECT_ROOT / "tmp") as temp_dir:
            path = Path(temp_dir) / "report.json"
            with self.assertRaises(ValueError):
                raw_mosaic_patches.write_report(path, {"bad": float("nan")})


if __name__ == "__main__":
    unittest.main()
