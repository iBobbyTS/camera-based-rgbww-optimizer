import unittest

from camera_based_rgbww_optimizer.optimization.guide10_white70 import build_guide10_white70_candidates


class Guide10White70Tests(unittest.TestCase):
    def test_latest_pass_wins_and_field_does_not_cross_active_faces(self):
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
        result = build_guide10_white70_candidates(baseline, [("pass", {"nodes": [pass_row]})], confirmation)
        self.assertEqual(result["node_count"], 70)
        selected = next(row for row in result["nodes"] if row["cct"] == 1800 and row["gm"] == 100)
        self.assertEqual(selected["candidate_command"]["g"], 1197)
        self.assertEqual(selected["field_action"], "retain_strict")
        self.assertTrue(all(row["active_face"] == ["r"] for row in result["nodes"]))


if __name__ == "__main__":
    unittest.main()
