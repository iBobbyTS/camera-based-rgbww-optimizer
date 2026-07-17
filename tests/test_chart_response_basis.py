import copy
import unittest

import numpy as np

from camera_based_rgbww_optimizer.measurement import chart_response_basis


PLANES = ("R", "G1", "G2", "B")
PATCHES = ("patch_a", "patch_b")


def make_reports(*, level_dependent=False, reject_feature=None):
    reports = []
    basis = np.asarray(
        [
            [5, 1, 1, 1, 1],
            [1, 5, 1, 1, 1],
            [1, 1, 5, 1, 1],
            [1, 1, 1, 5, 1],
            [1, 1, 1, 1, 5],
            [2, 3, 1, 4, 1],
            [3, 1, 4, 1, 2],
            [1, 4, 2, 3, 1],
        ],
        dtype=float,
    )
    for channel_index, channel in enumerate(chart_response_basis.CHANNELS):
        for code in chart_response_basis.LEVEL_CODES:
            fraction = code / 4095.0
            for repeat in range(3):
                values = basis[:, channel_index] * fraction
                if level_dependent and channel == "r" and code == 4095:
                    values = values.copy()
                    values[0] *= 1.25
                patches = []
                value_index = 0
                for patch in PATCHES:
                    planes = {}
                    for plane in PLANES:
                        feature = f"{patch}::{plane}"
                        rejected = reject_feature in {
                            (channel, code, repeat, feature),
                            (channel, None, None, feature),
                        }
                        quality = "rejected" if rejected else "accepted"
                        planes[plane] = {
                            "ambient_subtracted": {"trimmed_mean_per_second": float(values[value_index])},
                            "metrics": {
                                "valid_pixel_count": 30000,
                                "nonfinite_fraction": 0.0,
                                "clipped_fraction": 0.0,
                                "near_noise_floor_fraction": 0.0,
                            },
                            "quality": {"status": quality},
                        }
                        value_index += 1
                    patches.append({"name": patch, "optimization_eligible": True, "planes": planes})
                reports.append(
                    {
                        "schema_version": 1,
                        "measurement": "native_bayer_patch_statistics",
                        "source": {"path": f"{channel}-{code}-{repeat}.cr3"},
                        "location_config": {"sha256": "location-hash"},
                        "mosaic": {"plane_order": list(PLANES)},
                        "analysis_context": {
                            "capture_id": f"{channel}-{code}-{repeat}",
                            "purpose": "basis_formal",
                            "channel": channel,
                            "target_code": code,
                            "repeat_index": repeat,
                        },
                        "patches": patches,
                    }
                )
    return reports


class ChartResponseBasisTests(unittest.TestCase):
    def test_fits_full_rank_level_bases_and_normalizes_target_level(self):
        result = chart_response_basis.analyze_chart_response_basis(
            make_reports(), bootstrap_samples=100, random_seed=7
        )

        self.assertEqual(result["feature_count"], 8)
        self.assertEqual(result["plane_order"], list(PLANES))
        for code in chart_response_basis.LEVEL_CODES:
            diagnostics = result["basis_by_level"][str(code)]["diagnostics"]
            self.assertEqual(diagnostics["rank"], 5)
            self.assertIsNotNone(diagnostics["condition_number"])
        self.assertLess(
            max(item["relative_l2_shape_difference"] for item in result["level_shape_comparison"]),
            1e-12,
        )

    def test_reports_stable_level_dependent_shape_without_hiding_it(self):
        result = chart_response_basis.analyze_chart_response_basis(
            make_reports(level_dependent=True), bootstrap_samples=100
        )
        red = [item for item in result["level_shape_comparison"] if item["channel"] == "r"]
        self.assertGreater(max(item["relative_l2_shape_difference"] for item in red), 0.01)
        self.assertGreater(max(item["feature_count_over_3_sigma"] for item in red), 0)

    def test_rejected_observation_uses_marked_level_imputation_not_direct_center(self):
        result = chart_response_basis.analyze_chart_response_basis(
            make_reports(reject_feature=("cw", 1024, 0, "patch_a::R")),
            bootstrap_samples=100,
        )
        cell = result["feature_statistics"]["1024"]["cw"]["patch_a::R"]
        self.assertEqual(cell["mode"], "imputed_from_level")
        self.assertEqual(cell["imputed_from_level"], 2048)
        self.assertEqual(result["feature_count"], 8)
        self.assertEqual(result["rejections"]["observation_count"], 1)
        self.assertEqual(result["rejections"]["imputed_cell_count"], 1)

    def test_rejects_missing_formal_state(self):
        reports = [
            report
            for report in make_reports()
            if not (
                report["analysis_context"]["channel"] == "b"
                and report["analysis_context"]["target_code"] == 4095
            )
        ]
        with self.assertRaisesRegex(ValueError, "missing channel/level states"):
            chart_response_basis.analyze_chart_response_basis(reports, bootstrap_samples=100)

    def test_feature_with_no_accepted_level_is_censored_zero_with_zero_weight(self):
        result = chart_response_basis.analyze_chart_response_basis(
            make_reports(reject_feature=("b", None, None, "patch_a::R")),
            bootstrap_samples=100,
        )
        cell = result["feature_statistics"]["1024"]["b"]["patch_a::R"]
        feature_index = result["feature_order"].index("patch_a::R")
        channel_index = result["channels"].index("b")
        self.assertEqual(cell["mode"], "censored_zero")
        self.assertEqual(result["basis_by_level"]["1024"]["cell_weights"][feature_index][channel_index], 0.0)
        self.assertEqual(result["rejections"]["censored_zero_cell_count"], 3)

    def test_anchor_drift_separates_global_scale_from_shape(self):
        reports = make_reports()
        first = copy.deepcopy(reports[0])
        second = copy.deepcopy(reports[0])
        first["source"]["path"] = "anchor-a.cr3"
        second["source"]["path"] = "anchor-b.cr3"
        first["analysis_context"] = {"capture_id": "anchor-a", "purpose": "anchor_auto_exposure"}
        second["analysis_context"] = {"capture_id": "anchor-b", "purpose": "anchor_check"}
        for patch in second["patches"]:
            for plane in patch["planes"].values():
                plane["ambient_subtracted"]["trimmed_mean_per_second"] *= 1.1
        second["patches"][0]["planes"]["R"]["ambient_subtracted"]["trimmed_mean_per_second"] *= 1.05

        result = chart_response_basis.analyze_chart_response_basis(
            reports + [first, second], bootstrap_samples=100
        )
        self.assertEqual(result["anchor_drift"]["status"], "complete")
        self.assertAlmostEqual(result["anchor_drift"]["global_scale_right_to_left"], 1.1)
        self.assertGreater(result["anchor_drift"]["absolute_shape_drift"]["max"], 0.0)


if __name__ == "__main__":
    unittest.main()
