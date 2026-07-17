import json
import tempfile
import unittest
from pathlib import Path

import numpy as np

from camera_based_rgbww_optimizer.optimization import analyze_cct_multipatch_pilot
from camera_based_rgbww_optimizer.optimization.multipatch_objective import objective_from_residual_groups


def write_json(path, value):
    path.write_text(json.dumps(value), encoding="utf-8")


class AnalyzeCctMultipatchPilotTests(unittest.TestCase):
    def _run(self, root, *, unreachable=False):
        root = Path(root)
        write_json(root / "run.json", {
            "phase": "P4", "status": "complete", "completed_target_count": 12,
        })
        cleanup = {"steps": [{"name": "esphome", "ok": True}, {"name": "ray120c", "ok": True}]}
        write_json(root / "all-off-python.json", cleanup)
        write_json(root / "all-off-shell.json", cleanup["steps"])
        raw = root / "capture.cr3"
        raw.write_bytes(b"raw")
        measurement = root / "capture.json"
        write_json(measurement, {"exposure_metadata": {"status": "recorded"}})
        capture = {
            "capture_id": "capture", "capture": {
                "capture": {"saved_file": str(raw)}, "patch_statistics": str(measurement),
            },
        }
        (root / "captures.jsonl").write_text(json.dumps(capture) + "\n", encoding="utf-8")

        rows = []
        for cct in (1800, 3200, 5600, 20000):
            for gm in (0, 100, 200):
                baseline = [self._sample(0.10 + offset, 0.20 + offset) for offset in (-0.001, 0.0, 0.001)]
                candidate = [self._sample(0.04, 0.10), self._sample(0.041, 0.101)]
                command = {"cw": 4095, "ww": 2048, "r": 256, "g": 128, "b": 64}
                rows.append({
                    "status": "complete",
                    "target": {"cct_K": cct, "gm_raw": gm, "baseline_command": command},
                    "neutral_chroma_tolerance": 0.01,
                    "baseline": baseline,
                    "feedback": {
                        "goal_confirmed": True, "status": "goal_confirmed",
                        "selected_command": command,
                        "confirmation_attempts": [{"status": "confirmed", "sample_indices": [0, 1]}],
                        "samples": [
                            {"index": index, **sample} for index, sample in enumerate(candidate)
                        ],
                    },
                    "final_verification": [],
                })
        if unreachable:
            target = rows[1]["target"]
            rows[1] = {
                "status": "measurement_unreachable",
                "target": target,
                "stage": "ray_reference",
                "reason": "weak_signal_after_max_validated_exposure",
                "validated_exposure_envelope": [1.0, 1.25],
                "evidence": {
                    "source": "ray",
                    "purpose": "ray_target",
                    "capture_ids": ["normal", "reacquire"],
                    "exposure_factors": [1.0, 1.25],
                    "rejected_features": [{"feature_id": "block_02::B"}],
                },
            }
        (root / "target-results.jsonl").write_text(
            "".join(json.dumps(row) + "\n" for row in rows), encoding="utf-8"
        )

    def _sample(self, color_error, white_error):
        residuals = {
            "neutral": [0.001], "white": [white_error, 0.0],
            "training": [color_error, color_error * 0.8],
            "holdout": [color_error * 1.1, color_error * 0.9],
        }
        objective = objective_from_residual_groups(
            {key: np.asarray(value) for key, value in residuals.items()},
            neutral_chroma_tolerance=0.01,
        )
        return {"residuals": residuals, "objective": objective}

    def test_analyzer_builds_gate3_evidence_without_selecting_branch(self):
        with tempfile.TemporaryDirectory() as tempdir:
            self._run(tempdir)
            analysis = analyze_cct_multipatch_pilot.analyze_cct_multipatch_pilot(tempdir)
        self.assertEqual(analysis["point_count"], 12)
        self.assertTrue(analysis["decision_hints"]["c_a_evidence_complete"])
        self.assertFalse(analysis["decision_hints"]["automatic_gate3_selection"])
        self.assertEqual(analysis["capture_validation"]["recorded_exposure_count"], 1)
        self.assertEqual(analysis["aggregate"]["command_continuity"]["edge_count"], 17)

    def test_analyzer_rejects_missing_shell_cleanup(self):
        with tempfile.TemporaryDirectory() as tempdir:
            self._run(tempdir)
            (Path(tempdir) / "all-off-shell.json").unlink()
            with self.assertRaises(FileNotFoundError):
                analyze_cct_multipatch_pilot.analyze_cct_multipatch_pilot(tempdir)

    def test_analyzer_keeps_unreachable_point_and_disables_c_a(self):
        with tempfile.TemporaryDirectory() as tempdir:
            self._run(tempdir, unreachable=True)
            analysis = analyze_cct_multipatch_pilot.analyze_cct_multipatch_pilot(tempdir)
        self.assertEqual(analysis["point_count"], 12)
        self.assertEqual(analysis["evaluable_point_count"], 11)
        self.assertEqual(analysis["measurement_unreachable_point_count"], 1)
        self.assertFalse(analysis["decision_hints"]["c_a_evidence_complete"])
        self.assertEqual(analysis["decision_hints"]["measurement_unreachable_points"], ["1800K-gm100"])
        self.assertTrue(analysis["decision_hints"]["measurement_unreachable_extreme_cct_only"])
        self.assertEqual(analysis["aggregate"]["command_continuity"]["edge_count"], 14)
        self.assertEqual(analysis["aggregate"]["command_continuity"]["omitted_edge_count"], 3)


if __name__ == "__main__":
    unittest.main()
