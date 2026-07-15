import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from camera_based_rgbww_optimizer.measurement import recorded_exposure
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
            "statistics": {
                "normalized_per_second": {"trimmed_mean": value * multiplier},
                "black_corrected_normalized": {
                    "trimmed_mean": 0.30 * multiplier,
                    "maximum": 0.40 * multiplier,
                },
            },
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
    def test_preflight_summary_reports_signal_clipping_and_noise_without_deciding(self):
        sample = report(1.0, ambient=True)
        sample["analysis_context"] = {"source": "ray", "purpose": "linearity_preflight"}
        sample["patches"][0]["planes"]["G1"]["metrics"]["clipped_fraction"] = 0.001
        sample["patches"][0]["planes"]["B"]["metrics"]["near_noise_floor_fraction"] = 0.02

        analysis = analyze_raw_observer_validation.analyze_preflight_reports([sample])

        ray = analysis["sources"]["ray"]
        self.assertEqual(ray["plane_count"], 4)
        self.assertEqual(ray["maximum_clipped_fraction"], 0.001)
        self.assertEqual(ray["maximum_near_noise_floor_fraction"], 0.02)
        self.assertAlmostEqual(ray["maximum_black_corrected_normalized_trimmed_mean"], 0.33)
        self.assertNotIn("decision", analysis)

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

    def test_recompute_uses_recorded_exposure_and_preserves_stored_analysis(self):
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            self._write_run(root, status="complete")
            location = root / "locations.json"
            observer = root / "observer.json"
            location.write_text("{}", encoding="utf-8")
            observer.write_text("{}", encoding="utf-8")
            plan = json.loads((root / "plan.json").read_text(encoding="utf-8"))
            plan["inputs"] = {
                "location_config": {"path": str(location), "sha256": hashlib.sha256(location.read_bytes()).hexdigest()},
                "raw_observer_config": {"path": str(observer), "sha256": hashlib.sha256(observer.read_bytes()).hexdigest()},
            }
            (root / "plan.json").write_text(json.dumps(plan), encoding="utf-8")
            records = []
            for line in (root / "captures.jsonl").read_text(encoding="utf-8").splitlines():
                record = json.loads(line)
                raw_file = root / f"{record['capture_id']}.cr3"
                raw_file.write_bytes(b"fake")
                record["capture"]["capture"]["saved_file"] = str(raw_file)
                records.append(record)
            (root / "captures.jsonl").write_text(
                "\n".join(json.dumps(record) for record in records) + "\n",
                encoding="utf-8",
            )
            (root / "analysis.json").write_text('{"legacy": true}\n', encoding="utf-8")

            def exposure(path, shutter, **_kwargs):
                nominal = recorded_exposure.parse_nominal_exposure(shutter)
                return recorded_exposure.RecordedExposure(
                    seconds=nominal * 0.9375,
                    source="Canon:ExposureTime",
                    nominal_seconds=nominal,
                    nominal_shutter_speed=shutter,
                    raw_file=Path(path),
                    status="recorded",
                    metadata_values={"Canon:ExposureTime": nominal * 0.9375},
                )

            def analyze(_path, **kwargs):
                return report(10.0, ambient="ambient_raw_file" in kwargs)

            with mock.patch.object(
                analyze_raw_observer_validation.recorded_exposure,
                "resolve_recorded_exposure",
                side_effect=exposure,
            ), mock.patch.object(
                analyze_raw_observer_validation.raw_mosaic_patches,
                "analyze_raw_file",
                side_effect=analyze,
            ):
                analysis = analyze_raw_observer_validation.analyze_validation_run(
                    root,
                    recompute_recorded_exposure=True,
                )
                output = analyze_raw_observer_validation.write_validation_analysis(
                    root / analyze_raw_observer_validation.DEFAULT_RECORDED_OUTPUT_NAME,
                    analysis,
                )

            self.assertEqual(analysis["normalization"]["mode"], "recomputed_from_cr3_recorded_exposure")
            provenance = analysis["normalization"]["exposure_provenance"]
            self.assertEqual(provenance["status_counts"], {"recorded": 9})
            self.assertAlmostEqual(
                provenance["recorded_to_nominal_ratio"]["max_absolute_difference_from_one"],
                0.0625,
            )
            self.assertEqual(json.loads((root / "analysis.json").read_text(encoding="utf-8")), {"legacy": True})
            self.assertTrue(output.is_file())

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
