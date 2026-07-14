import json
import tempfile
import unittest
from pathlib import Path

from camera_based_rgbww_optimizer.optimization import measure_raw_shutter_response


def write_lut(path: Path) -> None:
    path.write_text(
        json.dumps(
            {
                "targets": [
                    {
                        "cct": 5600,
                        "gm": 100,
                        "selected_command": {"cw": 2800, "ww": 800, "r": 200, "g": 100, "b": 400},
                    }
                ]
            }
        ),
        encoding="utf-8",
    )


class RawShutterResponseTests(unittest.TestCase):
    def test_plan_keeps_same_explicit_shutter_sequence_for_each_continuous_source_group(self):
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            plan = self._plan(root)

            self.assertEqual(len(plan["captures"]), 49)
            self.assertEqual(plan["measurement"]["frames_per_shutter_per_source"], 6)
            self.assertEqual(plan["measurement"]["anchor"]["strip_command"]["cw"], 560)
            for source in ("ray", "strip"):
                group = [item for item in plan["captures"] if item["source"] == source]
                self.assertEqual([item["shutter_speed"] for item in group], list(measure_raw_shutter_response.DEFAULT_SHUTTER_ORDER) * 3)

    def test_plan_rejects_unbalanced_shutter_order(self):
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            with self.assertRaisesRegex(ValueError, "equal number"):
                measure_raw_shutter_response.build_raw_shutter_response_plan(
                    baseline_lut_path=self._lut(root),
                    location_config_path=self._locations(root),
                    observer_config_path=self._observer(root),
                    shutter_order=("1/80", "1/60", "1/100", "1/50", "1/80"),
                )

    def test_executor_leaves_each_source_on_across_its_capture_group_and_cleans_up(self):
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            plan = self._plan(root)
            calls = []
            captured = []

            def strip(*values):
                calls.append(("strip", values))
                return {"values": values}

            def ray(cct, *, intensity, gm, **_kwargs):
                calls.append(("ray", cct, intensity, gm))
                return {"cct": cct, "intensity": intensity, "gm": gm}

            result = measure_raw_shutter_response.execute_raw_shutter_response_plan(
                plan,
                run_dir=root / "run",
                strip_light_fn=strip,
                ray_set_cct_fn=ray,
                capture_step_fn=lambda step: captured.append(step["capture_id"]) or {"raw": step["capture_id"]},
                sleep_fn=lambda _seconds: None,
            )

            self.assertEqual(len(captured), len(plan["captures"]))
            self.assertEqual(sum(1 for call in calls if call[0] == "ray" and call[2] == 10.0), 1)
            self.assertEqual(sum(1 for call in calls if call[0] == "strip" and call[1] == (560, 160, 40, 20, 80)), 1)
            self.assertEqual(json.loads((result / "run.json").read_text(encoding="utf-8"))["status"], "complete")
            cleanup = json.loads((result / "all-off-python.json").read_text(encoding="utf-8"))
            self.assertTrue(all(step["ok"] for step in cleanup["steps"]))

    def test_analysis_reports_relative_shutter_evidence_without_pass_fail(self):
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            plan = self._plan(root)
            (root / "measurements").mkdir()
            captures = []
            source_values = {
                "ray": {"1/100": 98.0, "1/80": 100.0, "1/60": 101.0, "1/50": 99.0},
                "strip": {"1/100": 99.0, "1/80": 100.0, "1/60": 94.0, "1/50": 99.0},
            }
            for step in plan["captures"]:
                if step["source"] == "ambient":
                    captures.append({"capture_id": step["capture_id"], "source": "ambient", "capture": {"raw": "ambient.cr3"}})
                    continue
                value = source_values[step["source"]][step["shutter_speed"]]
                report_path = root / "measurements" / f"{step['capture_id']}.json"
                report_path.write_text(json.dumps(_report(value)), encoding="utf-8")
                captures.append({"capture_id": step["capture_id"], "source": step["source"], "capture": {"patch_statistics": str(report_path)}})
            (root / "plan.json").write_text(json.dumps(plan), encoding="utf-8")
            (root / "run.json").write_text(json.dumps({"status": "complete"}), encoding="utf-8")
            (root / "captures.jsonl").write_text("\n".join(json.dumps(item) for item in captures) + "\n", encoding="utf-8")

            output = measure_raw_shutter_response.analyze_raw_shutter_response_run(root)
            analysis = json.loads(output.read_text(encoding="utf-8"))
            strip = analysis["sources"]["strip"]["1/60"]["relative_to_reference"]
            self.assertEqual(analysis["status"], "ready_for_manual_branch_review")
            self.assertAlmostEqual(strip["p50"], -0.06)
            self.assertNotIn("decision", analysis)

    def test_executor_failure_still_attempts_both_final_shutdowns(self):
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            plan = self._plan(root)
            calls = []

            def strip(*values):
                calls.append(("strip", values))
                return {}

            def ray(cct, *, intensity, gm, **_kwargs):
                calls.append(("ray", cct, intensity, gm))
                return {}

            with self.assertRaisesRegex(RuntimeError, "camera failed"):
                measure_raw_shutter_response.execute_raw_shutter_response_plan(
                    plan,
                    run_dir=root / "failed",
                    strip_light_fn=strip,
                    ray_set_cct_fn=ray,
                    capture_step_fn=lambda _step: (_ for _ in ()).throw(RuntimeError("camera failed")),
                    sleep_fn=lambda _seconds: None,
                )

            cleanup = json.loads((root / "failed" / "all-off-python.json").read_text(encoding="utf-8"))
            self.assertTrue(all(step["ok"] for step in cleanup["steps"]))
            self.assertEqual(calls[-2][0], "strip")
            self.assertEqual(calls[-1][0], "ray")

    def _plan(self, root: Path):
        return measure_raw_shutter_response.build_raw_shutter_response_plan(
            baseline_lut_path=self._lut(root),
            location_config_path=self._locations(root),
            observer_config_path=self._observer(root),
        )

    def _lut(self, root: Path) -> Path:
        path = root / "lut.json"
        if not path.exists():
            write_lut(path)
        return path

    def _locations(self, root: Path) -> Path:
        path = root / "locations.json"
        path.write_text("{}", encoding="utf-8")
        return path

    def _observer(self, root: Path) -> Path:
        path = root / "observer.json"
        path.write_text("{}", encoding="utf-8")
        return path


def _report(value: float) -> dict:
    return {
        "patches": [
            {
                "name": "block_02",
                "optimization_eligible": True,
                "planes": {
                    plane: {"ambient_subtracted": {"trimmed_mean_per_second": value}}
                    for plane in ("R", "G1", "G2", "B")
                },
            }
        ]
    }
