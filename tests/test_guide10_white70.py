import unittest
import json
import tempfile
from pathlib import Path

from camera_based_rgbww_optimizer.optimization.guide10_white70 import (
    build_guide10_white70_candidates,
    build_guide10_white70_recovery_suffix,
    build_guide10_white70_validation_plan,
    build_guide10_white70_w5_plan,
)


class Guide10White70Tests(unittest.TestCase):
    def _inputs(self):
        nodes = []
        for cct in range(1000, 24000, 1000):
            for gm in (0, 100, 200):
                nodes.append({
                    "cct": cct,
                    "gm": gm,
                    "status": "fail",
                    "strip_command": {"cw": 0, "ww": 0, "r": 4095, "g": 100, "b": 0},
                    "cct_error_K": 30,
                    "mired_error": 2,
                    "duv_error": 0.001,
                })
        nodes = nodes[:69]
        nodes.append({**nodes[0], "cct": 1800, "gm": 100})
        baseline = {"nodes": nodes}
        pass_row = {**nodes[1], "status": "pass", "strip_command": {"cw": 0, "ww": 0, "r": 4095, "g": 110, "b": 0}, "cct_error_K": 1, "mired_error": 0.1, "duv_error": 0.0001}
        confirmation = {
            "run_root": "confirmation",
            "selected_command": {"cw": 0, "ww": 0, "r": 4095, "g": 1197, "b": 0},
            "confirmation_observations": [{"gates": {"cct": True, "mired": True, "duv": True}, "cct_error_K": 1, "mired_error": 0.2, "duv_error": 0.0001}],
        }
        return baseline, pass_row, confirmation

    def test_latest_pass_wins_and_field_does_not_cross_active_faces(self):
        baseline, pass_row, confirmation = self._inputs()
        result = build_guide10_white70_candidates(baseline, [("pass", {"nodes": [pass_row]})], confirmation)
        self.assertEqual(result["node_count"], 70)
        selected = next(row for row in result["nodes"] if row["cct"] == 1800 and row["gm"] == 100)
        self.assertEqual(selected["candidate_command"]["g"], 1197)
        self.assertEqual(selected["field_action"], "retain_strict")
        self.assertTrue(all(row["active_face"] == ["r"] for row in result["nodes"]))

    def test_validation_plan_covers_exact_grid_with_balanced_sources(self):
        baseline, pass_row, confirmation = self._inputs()
        candidates = build_guide10_white70_candidates(
            baseline, [("pass", {"nodes": [pass_row]})], confirmation,
        )
        calibration = {"targets": []}
        for row in candidates["nodes"]:
            calibration["targets"].append({
                "cct": row["cct"],
                "gm": row["gm"],
                "ray": {"auto_exposure": {"final": {"shutter_speed": "1/1600"}}},
                "feedback_optimizer": {"best": {"capture": {"shutter_speed": "1/50"}}},
                "feedback_goal": {
                    "resolved_cct_tolerance_K": 25,
                    "cct_tolerance_mired": 1,
                    "duv_tolerance": 0.0005,
                },
            })
        plan = build_guide10_white70_validation_plan(
            candidates,
            calibration,
            candidate_reference={"path": "candidate", "sha256": "a"},
            calibration_reference={"path": "calibration", "sha256": "b"},
        )
        self.assertEqual(len(plan["captures"]), 140)
        self.assertEqual(plan["budgets"]["physical_cr3_cap"], 140)
        self.assertEqual(plan["execution_authorization"]["schema"], "direct_guide10_white70_round1_v1")
        self.assertEqual(plan["captures"][0]["source_id"], "ray")
        self.assertEqual(plan["captures"][2]["source_id"], "strip")
        selected = next(
            row for row in plan["analysis_contract"]["target_contracts"]
            if row["cct"] == 1800 and row["gm"] == 100
        )
        self.assertEqual(selected["strip_command"]["g"], 1197)

    def test_recovery_suffix_requires_exact_complete_node_prefix(self):
        baseline, pass_row, confirmation = self._inputs()
        candidates = build_guide10_white70_candidates(baseline, [("pass", {"nodes": [pass_row]})], confirmation)
        calibration = {"targets": [{
            "cct": row["cct"], "gm": row["gm"],
            "ray": {"auto_exposure": {"final": {"shutter_speed": "1/1600"}}},
            "feedback_optimizer": {"best": {"capture": {"shutter_speed": "1/50"}}},
            "feedback_goal": {"resolved_cct_tolerance_K": 25, "cct_tolerance_mired": 1, "duv_tolerance": 0.0005},
        } for row in candidates["nodes"]]}
        plan = build_guide10_white70_validation_plan(candidates, calibration, candidate_reference={}, calibration_reference={})
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "experiment-spec.json").write_text(json.dumps(plan))
            (root / "run.json").write_text(json.dumps({"status": "interrupted", "interruption_reason": "user_requested_pause", "cleanup": "pass", "completed_formal": 2}))
            (root / "pause-evidence.json").write_text(json.dumps({"status": "pass", "rgbww_zero_readback": {"blue": 0, "green": 0, "cold_white": 0, "red": 0, "warm_white": 0}, "ray_zero_readback": {"intensity": 0}}))
            capture_rows, return_rows = [], []
            for step in plan["captures"][:2]:
                raw = root / f"{step['capture_id']}.cr3"
                raw.write_bytes(b"raw")
                receipt = {"cr3_sha256": "hash", "cr3_byte_count": 3}
                capture_rows.append({"capture_id": step["capture_id"], "capture": {"physical_return_receipt": receipt}})
                return_rows.append({"capture_id": step["capture_id"], "cr3_sha256": "hash", "cr3_byte_count": 3, "cr3_path": str(raw)})
            (root / "captures.jsonl").write_text("".join(json.dumps(row) + "\n" for row in capture_rows))
            (root / "physical-returns.jsonl").write_text("".join(json.dumps(row) + "\n" for row in return_rows))
            suffix = build_guide10_white70_recovery_suffix(root)
            self.assertEqual(len(suffix["captures"]), 138)
            self.assertEqual(suffix["recovery"]["completed_prefix_count"], 2)
            self.assertEqual(suffix["budgets"]["formal_cap"], 138)

    def test_w5_preserves_source_specific_shutters_when_round1_order_is_strip_first(self):
        baseline, pass_row, confirmation = self._inputs()
        candidates = build_guide10_white70_candidates(baseline, [("pass", {"nodes": [pass_row]})], confirmation)
        calibration = {"targets": [{
            "cct": row["cct"], "gm": row["gm"],
            "ray": {"auto_exposure": {"final": {"shutter_speed": "1/1600"}}},
            "feedback_optimizer": {
                "active_channel": "r", "final_jacobian": None,
                "best": {"capture": {"shutter_speed": "1/50"}},
            },
            "feedback_goal": {"resolved_cct_tolerance_K": 25, "cct_tolerance_mired": 1, "duv_tolerance": 0.0005},
        } for row in candidates["nodes"]]}
        round1 = build_guide10_white70_validation_plan(candidates, calibration, candidate_reference={}, calibration_reference={})
        node = candidates["nodes"][1]
        failed = {
            "node_count": 70,
            "nodes": [{
                "cct": node["cct"], "gm": node["gm"], "status": "fail",
                "strip_command": node["candidate_command"],
                "mired_error": 2.0, "duv_error": 0.0,
                "limits": {"cct_K": 25, "mired": 1, "duv": 0.0005},
                "ray": {"white_point": {"cct_K": 1800, "duv": 0.0}},
                "strip": {"white_point": {"cct_K": 1794, "duv": 0.0}},
            }],
        }
        w5 = build_guide10_white70_w5_plan(
            failed, round1, calibration,
            analysis_reference={}, round1_reference={}, calibration_reference={},
        )
        first_ray, first_strip = w5["captures"][:2]
        self.assertEqual((first_ray["source_id"], first_ray["nominal_shutter"]), ("ray", "1/1600"))
        self.assertEqual((first_strip["source_id"], first_strip["nominal_shutter"]), ("strip", "1/50"))
        self.assertEqual(first_strip["exposure_cache_key"], f"strip-white-{node['cct']}-gm{node['gm']}")


if __name__ == "__main__":
    unittest.main()
