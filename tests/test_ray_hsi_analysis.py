from __future__ import annotations

import math
import json
import tempfile
import unittest
from pathlib import Path

import numpy as np

from camera_based_rgbww_optimizer.measurement import ray_hsi_analysis as subject
from camera_based_rgbww_optimizer.optimization import measure_ray_hsi_manifold


class RayHsiAnalysisTests(unittest.TestCase):
    def test_separable_periodic_synthetic_manifold_is_reported(self):
        analysis = subject.analyze_ray_hsi_samples(self._samples())

        self.assertEqual(analysis["sample_count"], 105)
        self.assertEqual(analysis["sat0"]["status"], "complete")
        self.assertEqual(analysis["hsi_rgb_endpoints"]["complete_count"], 6)
        candidate = analysis["affine_separability"]["candidates"]["pooled_sat0"]
        self.assertEqual(candidate["complete_point_count"], 60)
        self.assertLess(candidate["orthogonal_relative_residual"]["maximum"], 0.001)
        self.assertEqual(analysis["hue_periodicity"]["closure_edge"]["from_hue"], 330)
        self.assertFalse(analysis["decision_hints"]["automatic_gate5_selection"])
        self.assertFalse(analysis["decision_hints"]["run_invalid_for_model_selection"])

    def test_local_bend_is_visible_in_orthogonal_residual(self):
        samples = self._samples()
        for sample in samples:
            state = sample["state"]
            if sample["mode"] == "hsi" and state["hue"] == 150 and state["sat"] == 50:
                sample["features"]["f11"] += 0.8

        analysis = subject.analyze_ray_hsi_samples(samples)

        points = analysis["affine_separability"]["candidates"]["pooled_sat0"]["points"]
        point = next(item for item in points if item["hue"] == 150 and item["sat"] == 50)
        self.assertGreater(point["orthogonal_relative_residual"], 0.01)
        self.assertFalse(point["within_2x_repeatability"])

    def test_completed_run_requires_and_reports_full_native_evidence(self):
        plan = measure_ray_hsi_manifold.build_ray_hsi_manifold_plan(off_seconds=0, settle_seconds=0)
        by_id = {sample["capture_id"]: sample for sample in self._samples()}
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            camera = root / "camera"
            measurements = root / "measurements"
            camera.mkdir()
            measurements.mkdir()
            (root / "run.json").write_text(
                json.dumps({"phase": "P6", "status": "complete", "completed_capture_count": 106}),
                encoding="utf-8",
            )
            cleanup = [{"name": "esphome", "ok": True}, {"name": "ray120c", "ok": True}]
            (root / "all-off-python.json").write_text(json.dumps({"steps": cleanup}), encoding="utf-8")
            (root / "all-off-shell.json").write_text(json.dumps(cleanup), encoding="utf-8")
            records = []
            for step in plan["captures"]:
                raw = camera / f"{step['capture_id']}.cr3"
                raw.write_bytes(b"CR3")
                report_path = measurements / f"{step['capture_id']}.json"
                values = np.full(12, 0.01) if step["source"] == "ambient" else np.asarray(list(by_id[step["capture_id"]]["features"].values()))
                report_path.write_text(json.dumps(self._report(values, raw)), encoding="utf-8")
                records.append(
                    {
                        "capture_id": step["capture_id"],
                        "source": step["source"],
                        "purpose": step["purpose"],
                        "repeat_index": step["repeat_index"],
                        "analysis_context": step["analysis_context"],
                        "ray_mode": step["ray_mode"],
                        "ray_state": step["ray_state"],
                        "capture": {"capture": {"saved_file": str(raw)}, "patch_statistics": str(report_path)},
                    }
                )
            (root / "captures.jsonl").write_text("\n".join(json.dumps(record) for record in records) + "\n", encoding="utf-8")

            analysis = subject.analyze_ray_hsi_run(root)

        self.assertEqual(analysis["capture_validation"]["raw_count"], 106)
        self.assertEqual(analysis["capture_validation"]["recorded_exposure_count"], 106)
        self.assertEqual(analysis["sample_count"], 105)
        self.assertEqual(analysis["status"], "ready_for_manual_gate5_decision")

    def _samples(self):
        plan = measure_ray_hsi_manifold.build_ray_hsi_manifold_plan(off_seconds=0, settle_seconds=0)
        samples = []
        for step in plan["captures"]:
            if step["source"] == "ambient":
                continue
            state = step["ray_state"]
            repeat = int(step["repeat_index"] or 0)
            if step["ray_mode"] == "hsi":
                hue = int(state["hue"])
                sat = int(state["sat"])
                vector = self._hsi_vector(hue, sat)
            else:
                hue = int(step["analysis_context"]["matching_hue"])
                vector = 1.35 * self._hsi_vector(hue, 100)
            noise = (repeat + 1) * 1e-5 * np.asarray([(-1.0) ** index * (index + 1) for index in range(12)])
            vector = vector + noise
            samples.append(
                {
                    "capture_id": step["capture_id"],
                    "mode": step["ray_mode"],
                    "state": state,
                    "endpoint": step["analysis_context"].get("endpoint"),
                    "features": {f"f{index:02d}": float(value) for index, value in enumerate(vector)},
                    "rejected_feature_count": 0,
                }
            )
        return samples

    @staticmethod
    def _report(values: np.ndarray, raw: Path) -> dict:
        planes = ("R", "G1", "G2", "B")
        patches = []
        for patch_index in range(3):
            patch_planes = {}
            for plane_index, plane in enumerate(planes):
                value = float(values[patch_index * 4 + plane_index])
                patch_planes[plane] = {
                    "quality": {"status": "accepted"},
                    "metrics": {"valid_pixel_count": 30000, "nonfinite_fraction": 0.0, "clipped_fraction": 0.0, "near_noise_floor_fraction": 0.0},
                    "ambient_subtracted": {"trimmed_mean_per_second": value},
                }
            patches.append({"name": f"p{patch_index}", "optimization_eligible": True, "planes": patch_planes})
        return {
            "schema_version": 1,
            "measurement": "native_bayer_patch_statistics",
            "source": {"path": str(raw)},
            "exposure_metadata": {"status": "recorded"},
            "location_config": {"sha256": "location"},
            "mosaic": {"plane_order": list(planes)},
            "patches": patches,
        }

    @staticmethod
    def _hsi_vector(hue: int, sat: int) -> np.ndarray:
        phase = math.radians(hue)
        zero = np.linspace(1.0, 2.1, 12)
        endpoint = zero + np.asarray([
            0.4 * math.cos(phase + index * 0.23) + 0.35 * math.sin(phase * 2 + index * 0.11)
            for index in range(12)
        ]) + 0.8
        fraction = sat / 100.0
        return (1.0 - fraction) * zero + fraction * endpoint


if __name__ == "__main__":
    unittest.main()
