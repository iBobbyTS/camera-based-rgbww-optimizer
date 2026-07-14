import json
import tempfile
import unittest
from pathlib import Path

from camera_based_rgbww_optimizer.optimization import analyze_raw_observer_validation


def report(value: float, *, ambient: bool) -> dict:
    planes = {}
    for name, multiplier in (("R", 1.0), ("G1", 1.1), ("G2", 1.0), ("B", 0.9)):
        plane = {
            "metrics": {
                "valid_pixel_count": 100,
                "nonfinite_fraction": 0.0,
                "clipped_fraction": 0.0,
                "near_noise_floor_fraction": 0.0,
            },
            "quality": {"status": "pending_thresholds"},
            "statistics": {"normalized_per_second": {"trimmed_mean": value * multiplier}},
        }
        if ambient:
            plane["ambient_subtracted"] = {"trimmed_mean_per_second": value * multiplier}
        planes[name] = plane
    return {
        "schema_version": 1,
        "measurement": "native_bayer_patch_statistics",
        "source": {"path": "sample.cr3"},
        "location_config": {"sha256": "same-location"},
        "mosaic": {"plane_order": ["R", "G1", "G2", "B"]},
        "patches": [{"name": "neutral_01", "optimization_eligible": True, "planes": planes}],
    }


class AnalyzeRawObserverValidationTests(unittest.TestCase):
    def test_analyze_completed_run_groups_repeatability_linearity_and_context(self):
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            self._write_run(root, status="complete")

            analysis = analyze_raw_observer_validation.analyze_validation_run(root)
            output = analyze_raw_observer_validation.write_validation_analysis(root / "analysis.json", analysis)

            self.assertEqual(analysis["status"], "ready_for_manual_branch_review")
            self.assertEqual(analysis["report_count"], 9)
            self.assertEqual(analysis["signal_report_count"], 8)
            self.assertEqual(analysis["repeatability"]["ray"]["summary"]["feature_count"], 4)
            self.assertEqual(analysis["linearity"]["strip"]["factors"], [0.5, 1.0])
            green_contexts = [
                item["analysis_context"]
                for item in analysis["green_consistency"]["observations"]
                if item["status"] == "included"
            ]
            self.assertEqual({context["source"] for context in green_contexts}, {"ray", "strip"})
            self.assertEqual(analysis["quality_threshold_recommendation"]["status"], "requires_explicit_accepted_report_ids")
            self.assertTrue(output.is_file())

    def test_completed_analysis_rejects_incomplete_run_without_explicit_override(self):
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            self._write_run(root, status="running")

            with self.assertRaisesRegex(ValueError, "not complete"):
                analyze_raw_observer_validation.analyze_validation_run(root)

            analysis = analyze_raw_observer_validation.analyze_validation_run(root, require_complete=False)
            self.assertEqual(analysis["report_count"], 9)

    def _write_run(self, root: Path, *, status: str) -> None:
        measurements = root / "measurements"
        measurements.mkdir()
        captures = [
            {"capture_id": "ambient", "source": "ambient", "purpose": "ambient", "repeat_index": None, "exposure_factor": None},
            {"capture_id": "ray-r0", "source": "ray", "purpose": "paired_repeat", "repeat_index": 0, "exposure_factor": None},
            {"capture_id": "ray-r1", "source": "ray", "purpose": "paired_repeat", "repeat_index": 1, "exposure_factor": None},
            {"capture_id": "strip-r0", "source": "strip", "purpose": "paired_repeat", "repeat_index": 0, "exposure_factor": None},
            {"capture_id": "strip-r1", "source": "strip", "purpose": "paired_repeat", "repeat_index": 1, "exposure_factor": None},
            {"capture_id": "ray-half", "source": "ray", "purpose": "linearity_bracket", "repeat_index": 0, "exposure_factor": 0.5},
            {"capture_id": "ray-one", "source": "ray", "purpose": "linearity_bracket", "repeat_index": 0, "exposure_factor": 1.0},
            {"capture_id": "strip-half", "source": "strip", "purpose": "linearity_bracket", "repeat_index": 0, "exposure_factor": 0.5},
            {"capture_id": "strip-one", "source": "strip", "purpose": "linearity_bracket", "repeat_index": 0, "exposure_factor": 1.0},
        ]
        (root / "run.json").write_text(json.dumps({"status": status}), encoding="utf-8")
        (root / "plan.json").write_text(json.dumps({"captures": captures}), encoding="utf-8")
        lines = []
        for index, capture in enumerate(captures):
            path = measurements / f"{capture['capture_id']}.json"
            path.write_text(json.dumps(report(10.0 + index, ambient=capture["source"] != "ambient")), encoding="utf-8")
            lines.append(
                json.dumps(
                    {
                        "capture_id": capture["capture_id"],
                        "capture": {"patch_statistics": str(path), "capture": {"shutter_speed": "1/125"}},
                    }
                )
            )
        (root / "captures.jsonl").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    unittest.main()
