import json
import tempfile
import unittest
from pathlib import Path

from camera_based_rgbww_optimizer.measurement import raw_observer_analysis


def make_plane(value, *, ambient=True, clipped=0.0, near_noise=0.0, valid_pixels=1024):
    plane = {
        "metrics": {
            "valid_pixel_count": valid_pixels,
            "nonfinite_fraction": 0.0,
            "clipped_fraction": clipped,
            "near_noise_floor_fraction": near_noise,
        },
        "quality": {"status": "pending_thresholds"},
        "statistics": {"normalized_per_second": {"trimmed_mean": value}},
    }
    if ambient:
        plane["ambient_subtracted"] = {"trimmed_mean_per_second": value}
    return plane


def make_report(
    report_id,
    *,
    values=None,
    ambient=True,
    location_hash="location-a",
    context=None,
    clipped=0.0,
    near_noise=0.0,
):
    values = {"R": 10.0, "G1": 11.0, "G2": 10.0, "B": 9.0} if values is None else values
    return {
        "schema_version": 1,
        "measurement": "native_bayer_patch_statistics",
        "source": {"path": f"{report_id}.cr3"},
        "location_config": {"sha256": location_hash},
        "mosaic": {"plane_order": ["R", "G1", "G2", "B"]},
        "analysis_context": context or {},
        "patches": [
            {
                "name": "neutral_01",
                "optimization_eligible": True,
                "planes": {
                    name: make_plane(value, ambient=ambient, clipped=clipped, near_noise=near_noise)
                    for name, value in values.items()
                },
            }
        ],
    }


class RawObserverCollectionTests(unittest.TestCase):
    def test_default_statistic_requires_ambient_subtraction_without_fallback(self):
        collection = raw_observer_analysis.collect_patch_plane_features(
            [make_report("ambient"), make_report("missing", ambient=False)]
        )

        self.assertEqual(collection["statistic"], "ambient_subtracted.trimmed_mean_per_second")
        self.assertEqual(collection["included_observation_count"], 4)
        self.assertEqual(collection["missing_statistic_count"], 4)
        self.assertEqual(
            {item["status"] for item in collection["observations"]},
            {"included", "missing_statistic"},
        )

    def test_rejects_different_location_hashes(self):
        with self.assertRaisesRegex(ValueError, "location_config.sha256"):
            raw_observer_analysis.collect_patch_plane_features(
                [make_report("one"), make_report("two", location_hash="location-b")]
            )

    def test_rejects_inconsistent_cfa_plane_set(self):
        incomplete = make_report("incomplete")
        del incomplete["patches"][0]["planes"]["B"]

        with self.assertRaisesRegex(ValueError, "expected CFA planes"):
            raw_observer_analysis.collect_patch_plane_features([make_report("complete"), incomplete])


class RawObserverRepeatabilityTests(unittest.TestCase):
    def test_repeatability_reports_feature_and_global_distributions(self):
        reports = [
            make_report("one", values={"R": 10.0, "G1": 11.0, "G2": 10.0, "B": 9.0}),
            make_report("two", values={"R": 11.0, "G1": 11.0, "G2": 10.0, "B": 9.0}),
            make_report("three", values={"R": 12.0, "G1": 11.0, "G2": 10.0, "B": 9.0}),
        ]

        analysis = raw_observer_analysis.analyze_repeatability(reports)

        red = analysis["features"]["neutral_01::R"]
        self.assertEqual(red["count"], 3)
        self.assertAlmostEqual(red["mean"], 11.0)
        self.assertAlmostEqual(red["median"], 11.0)
        self.assertAlmostEqual(red["mad"], 1.0)
        self.assertAlmostEqual(red["standard_deviation"], 1.0)
        self.assertGreater(analysis["summary"]["p95_range"]["max"], 0.0)

    def test_repeatability_retains_outlier_in_distribution(self):
        reports = [
            make_report("one"),
            make_report("two"),
            make_report("outlier", values={"R": 30.0, "G1": 11.0, "G2": 10.0, "B": 9.0}),
        ]

        analysis = raw_observer_analysis.analyze_repeatability(reports)

        self.assertGreater(analysis["features"]["neutral_01::R"]["p95_range"], 10.0)


class RawObserverLinearityTests(unittest.TestCase):
    def test_linearity_uses_repeatability_scale_and_detects_monotonic_drift(self):
        repeatability = raw_observer_analysis.analyze_repeatability(
            [make_report("repeat-a"), make_report("repeat-b", values={"R": 11.0, "G1": 12.0, "G2": 11.0, "B": 10.0})]
        )
        groups = {
            0.5: [make_report("half", values={"R": 8.0, "G1": 8.0, "G2": 8.0, "B": 8.0})],
            1.0: [make_report("one", values={"R": 10.0, "G1": 10.0, "G2": 10.0, "B": 10.0})],
            2.0: [make_report("two", values={"R": 12.0, "G1": 12.0, "G2": 12.0, "B": 12.0})],
        }

        analysis = raw_observer_analysis.analyze_exposure_linearity(groups, repeatability)

        red = analysis["features"]["neutral_01::R"]
        self.assertEqual(red["status"], "complete")
        self.assertEqual(red["reference_factor"], 1.0)
        self.assertEqual(red["monotonic_drift"], "increasing")
        self.assertGreater(red["centers"][0]["residual_repeatability_sigma"], 0.0)

    def test_linearity_reports_flat_normalized_response_without_drift(self):
        groups = {
            0.5: [make_report("half")],
            1.0: [make_report("one")],
            2.0: [make_report("two")],
        }

        analysis = raw_observer_analysis.analyze_exposure_linearity(groups)

        red = analysis["features"]["neutral_01::R"]
        self.assertAlmostEqual(red["slope_per_log_exposure_factor"], 0.0)
        self.assertEqual(red["monotonic_drift"], "none")
        self.assertTrue(all(item["relative_residual"] == 0.0 for item in red["centers"]))
        self.assertTrue(all(item["shape_relative_residual"] == 0.0 for item in red["centers"]))

    def test_linearity_separates_global_exposure_scale_from_feature_shape(self):
        groups = {
            0.5: [
                make_report(
                    "half",
                    values={"R": 8.0, "G1": 16.0, "G2": 24.0, "B": 32.0},
                    context={"exposure_seconds": 1.0},
                )
            ],
            1.0: [
                make_report(
                    "one",
                    values={"R": 10.0, "G1": 20.0, "G2": 30.0, "B": 40.0},
                    context={"exposure_seconds": 1.0},
                )
            ],
        }

        analysis = raw_observer_analysis.analyze_exposure_linearity(groups)

        half_scale = analysis["global_exposure_scale_by_factor"][0]
        self.assertEqual(half_scale["factor"], 0.5)
        self.assertAlmostEqual(half_scale["scale_to_reference"], 0.8)
        self.assertAlmostEqual(half_scale["relative_residual"], -0.2)
        self.assertAlmostEqual(
            analysis["summary"]["absolute_relative_residual"]["p95"],
            0.2,
        )
        self.assertAlmostEqual(
            analysis["summary"]["absolute_shape_relative_residual"]["max"],
            0.0,
        )
        self.assertAlmostEqual(
            analysis["summary"]["absolute_relative_residual_non_reference"]["p95"],
            0.2,
        )
        self.assertAlmostEqual(
            analysis["features"]["neutral_01::R"]["centers"][0]["normalized_signal_fraction"],
            8.0,
        )

    def test_linearity_keeps_a_short_exposure_only_deviation_visible(self):
        groups = {
            0.5: [make_report("half", values={"R": 8.0, "G1": 8.0, "G2": 8.0, "B": 8.0})],
            1.0: [make_report("one")],
            2.0: [make_report("two")],
        }

        analysis = raw_observer_analysis.analyze_exposure_linearity(groups)

        centers = analysis["features"]["neutral_01::R"]["centers"]
        self.assertAlmostEqual(centers[0]["relative_residual"], -0.2)
        self.assertEqual(centers[1]["relative_residual"], 0.0)
        self.assertEqual(centers[2]["relative_residual"], 0.0)

    def test_linearity_rejects_mismatched_group_geometry(self):
        with self.assertRaisesRegex(ValueError, "location_config_sha256"):
            raw_observer_analysis.analyze_exposure_linearity(
                {0.5: [make_report("half")], 1.0: [make_report("one", location_hash="different")]}
            )

    def test_linearity_rejects_mismatched_patch_signature(self):
        changed = make_report("changed")
        changed["patches"][0]["name"] = "different_neutral"

        with self.assertRaisesRegex(ValueError, "patch_signature"):
            raw_observer_analysis.analyze_exposure_linearity(
                {0.5: [make_report("half")], 1.0: [changed]}
            )


class RawObserverGreenTests(unittest.TestCase):
    def test_green_analysis_preserves_context_and_ratio(self):
        analysis = raw_observer_analysis.analyze_green_consistency(
            [
                make_report(
                    "one",
                    values={"R": 1.0, "G1": 11.0, "G2": 10.0, "B": 1.0},
                    context={"source": "ray", "exposure_factor": 1.0},
                ),
                make_report(
                    "two",
                    values={"R": 1.0, "G1": 12.1, "G2": 11.0, "B": 1.0},
                    context={"source": "strip", "exposure_factor": 2.0},
                ),
            ]
        )

        first = analysis["observations"][0]
        self.assertEqual(first["analysis_context"]["source"], "ray")
        self.assertAlmostEqual(first["g1_to_g2_ratio"], 1.1)
        self.assertAlmostEqual(analysis["patches"]["neutral_01"]["ratio"]["median"], 1.1)

    def test_green_analysis_retains_source_dependent_ratio_change(self):
        analysis = raw_observer_analysis.analyze_green_consistency(
            [
                make_report(
                    "ray",
                    values={"R": 1.0, "G1": 11.0, "G2": 10.0, "B": 1.0},
                    context={"source": "ray"},
                ),
                make_report(
                    "strip",
                    values={"R": 1.0, "G1": 12.0, "G2": 10.0, "B": 1.0},
                    context={"source": "strip"},
                ),
            ]
        )

        self.assertGreater(analysis["patches"]["neutral_01"]["ratio"]["p95_range"], 0.05)

    def test_zero_signal_stays_json_safe_and_does_not_invent_green_ratio(self):
        zero = make_report("zero", values={"R": 0.0, "G1": 0.0, "G2": 0.0, "B": 0.0})
        analysis = raw_observer_analysis.analyze_green_consistency([zero])

        self.assertIsNone(analysis["observations"][0]["g1_to_g2_ratio"])
        self.assertIsNone(analysis["patches"]["neutral_01"]["ratio"]["median"])
        json.dumps(analysis, allow_nan=False)


class RawObserverQualityRecommendationTests(unittest.TestCase):
    def test_recommendation_requires_explicit_selection_then_uses_selected_evidence(self):
        reports = [
            make_report("one", clipped=0.01, near_noise=0.02),
            make_report("two", clipped=0.03, near_noise=0.04),
        ]

        pending = raw_observer_analysis.recommend_quality_thresholds(reports)
        recommendation = raw_observer_analysis.recommend_quality_thresholds(
            reports,
            accepted_report_ids=["one.cr3", "two.cr3"],
        )

        self.assertEqual(pending["status"], "requires_explicit_accepted_report_ids")
        self.assertEqual(recommendation["status"], "candidate_only")
        self.assertAlmostEqual(recommendation["candidate_quality_thresholds"]["maximum_clipped_fraction"], 0.03)
        self.assertAlmostEqual(
            recommendation["candidate_quality_thresholds"]["maximum_near_noise_floor_fraction"], 0.04
        )

    def test_json_writer_rejects_nonfinite_values(self):
        with tempfile.TemporaryDirectory() as tempdir:
            output = Path(tempdir) / "analysis.json"
            with self.assertRaises(ValueError):
                raw_observer_analysis.write_analysis_json(output, {"bad": float("nan")})
            raw_observer_analysis.write_analysis_json(output, {"ok": True})
            self.assertEqual(json.loads(output.read_text(encoding="utf-8")), {"ok": True})


if __name__ == "__main__":
    unittest.main()
