import copy
import unittest

import numpy as np

from camera_based_rgbww_optimizer.measurement import chart_basis_validation


PLANES = ("R", "G1", "G2", "B")
PATCHES = ("block_18", "block_19")
FEATURES = tuple(f"{patch}::{plane}" for patch in PATCHES for plane in PLANES)
CHANNELS = chart_basis_validation.CHANNELS
LEVELS = chart_basis_validation.LEVEL_CODES


def make_basis(*, level_dependent=False):
    base = np.asarray([
        [5, 1, 1, 1, 1], [1, 5, 1, 1, 1], [1, 1, 5, 1, 1], [1, 1, 1, 5, 1],
        [1, 1, 1, 1, 5], [2, 3, 1, 4, 1], [3, 1, 4, 1, 2], [1, 4, 2, 3, 1],
    ], dtype=float)
    basis_by_level = {}
    statistics = {}
    for level in LEVELS:
        matrix = base.copy()
        if level_dependent:
            matrix[:, 2] *= 1.0 + (level - 1024) / 4095.0 * 0.1
        basis_by_level[str(level)] = {
            "matrix": matrix.tolist(),
            "cell_weights": np.ones_like(matrix).tolist(),
            "diagnostics": {"rank": 5},
        }
        statistics[str(level)] = {}
        for channel_index, channel in enumerate(CHANNELS):
            statistics[str(level)][channel] = {
                feature: {
                    "mode": "direct", "center": float(matrix[index, channel_index] * level / 4095.0),
                    "normalized_center": float(matrix[index, channel_index]), "standard_deviation": 0.001,
                }
                for index, feature in enumerate(FEATURES)
            }
    return {
        "analysis": "chart_response_basis", "status": "ready_for_manual_branch_review",
        "location_config_sha256": "location-hash", "channels": list(CHANNELS),
        "level_codes": list(LEVELS), "plane_order": list(PLANES), "feature_order": list(FEATURES),
        "feature_weights": {feature: 1.0 for feature in FEATURES},
        "basis_by_level": basis_by_level, "feature_statistics": statistics,
    }


def make_mixture_reports(basis, *, distortion_sample=None):
    reports = []
    commands = []
    for index in range(24):
        command = {channel: 0 for channel in CHANNELS}
        command[CHANNELS[index % 5]] = 512 + (index % 7) * 400
        command[CHANNELS[(index + 2) % 5]] = 256 + (index % 3) * 300
        commands.append(command)
    for state_index, command in enumerate(commands, start=1):
        prediction = chart_basis_validation.predict_piecewise_basis(basis, command)["values"]
        for repeat in range(2):
            patches = []
            value_index = 0
            for patch in PATCHES:
                planes = {}
                for plane in PLANES:
                    value = prediction[value_index] * (1.0 + (repeat * 2 - 1) * 0.0001)
                    if distortion_sample == state_index and value_index == 0:
                        value *= 1.2
                    planes[plane] = {
                        "ambient_subtracted": {"trimmed_mean_per_second": float(value)},
                        "metrics": {"valid_pixel_count": 30000, "nonfinite_fraction": 0.0, "clipped_fraction": 0.0, "near_noise_floor_fraction": 0.0},
                        "quality": {"status": "accepted"},
                    }
                    value_index += 1
                patches.append({"name": patch, "optimization_eligible": True, "planes": planes})
            reports.append({
                "schema_version": 1, "measurement": "native_bayer_patch_statistics",
                "source": {"path": f"sample-{state_index}-{repeat}.cr3"},
                "location_config": {"sha256": "location-hash"}, "mosaic": {"plane_order": list(PLANES)},
                "analysis_context": {
                    "capture_id": f"sample-{state_index}-{repeat}", "purpose": "mixture_formal",
                    "sample_id": f"sample-{state_index:02d}", "category": "synthetic",
                    "state_index": state_index, "repeat_index": repeat, "command": command,
                    "total_target_load": sum(command.values()), "active_set": [key for key, value in command.items() if value],
                    "previous_state": (
                        (None if state_index == 1 else f"sample-{state_index - 1:02d}")
                        if repeat == 0
                        else f"sample-{state_index:02d}"
                    ),
                },
                "patches": patches,
            })
    return reports


class ChartBasisValidationTests(unittest.TestCase):
    def test_piecewise_prediction_interpolates_level_dependent_column(self):
        basis = make_basis(level_dependent=True)
        low = chart_basis_validation.predict_piecewise_basis(basis, {"cw": 0, "ww": 0, "r": 1024, "g": 0, "b": 0})
        middle = chart_basis_validation.predict_piecewise_basis(basis, {"cw": 0, "ww": 0, "r": 1536, "g": 0, "b": 0})
        high = chart_basis_validation.predict_piecewise_basis(basis, {"cw": 0, "ww": 0, "r": 2048, "g": 0, "b": 0})
        normalized_middle = np.asarray(middle["values"]) / (1536 / 4095.0)
        expected = (np.asarray(low["values"]) / (1024 / 4095.0) + np.asarray(high["values"]) / (2048 / 4095.0)) / 2
        np.testing.assert_allclose(normalized_middle, expected)

    def test_exact_additive_mixtures_have_small_shape_residual(self):
        basis = make_basis(level_dependent=True)
        result = chart_basis_validation.analyze_chart_basis_validation(make_mixture_reports(basis), basis)
        self.assertEqual(result["sample_count"], 24)
        self.assertLess(result["aggregate"]["sample_shape_p95"]["max"], 1e-9)
        self.assertEqual(result["rejections"]["observation_count"], 0)
        self.assertEqual(result["samples"][0]["previous_states"], [None, "sample-01"])

    def test_systematic_feature_distortion_is_visible(self):
        basis = make_basis()
        result = chart_basis_validation.analyze_chart_basis_validation(
            make_mixture_reports(basis, distortion_sample=4), basis
        )
        sample = result["samples"][3]
        self.assertGreater(sample["absolute_shape_relative_residual"]["max"], 0.1)
        self.assertFalse(result["decision_hints"]["all_sample_sigma_p95_at_or_below_3"])

    def test_anchor_series_separates_global_scale_from_shape_drift(self):
        basis = make_basis()
        reports = make_mixture_reports(basis)
        anchor_reports = []
        for index, scale in enumerate((1.0, 0.99, 0.98, 0.97)):
            report = copy.deepcopy(reports[0])
            report["source"]["path"] = f"anchor-{index}.cr3"
            report["analysis_context"] = {
                "capture_id": f"anchor-{index}",
                "purpose": "anchor_auto_exposure" if index == 0 else "anchor_check",
            }
            for patch in report["patches"]:
                for plane in patch["planes"].values():
                    plane["ambient_subtracted"]["trimmed_mean_per_second"] *= scale
            anchor_reports.append(report)
        result = chart_basis_validation.analyze_chart_basis_validation(reports + anchor_reports, basis)
        drift = result["anchor_drift"]
        self.assertEqual(drift["status"], "complete")
        self.assertEqual(len(drift["comparisons_to_baseline"]), 3)
        self.assertAlmostEqual(drift["comparisons_to_baseline"][-1]["global_scale_to_baseline"], 0.97)
        self.assertLess(drift["comparisons_to_baseline"][-1]["absolute_shape_drift"]["max"], 1e-12)

    def test_rejects_location_mismatch(self):
        basis = make_basis()
        reports = make_mixture_reports(basis)
        changed = copy.deepcopy(reports)
        changed[0]["location_config"]["sha256"] = "wrong"
        with self.assertRaisesRegex(ValueError, r"location_config\.sha256"):
            chart_basis_validation.analyze_chart_basis_validation(changed, basis)


if __name__ == "__main__":
    unittest.main()
