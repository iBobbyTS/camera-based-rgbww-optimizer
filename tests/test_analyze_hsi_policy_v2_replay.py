from __future__ import annotations

import unittest

from camera_based_rgbww_optimizer.optimization import analyze_hsi_policy_v2_replay as subject


class AnalyzeHsiPolicyV2ReplayTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result = subject.analyze_v2_replay(synthetic_samples=1000)

    def test_v1_replay_is_byte_identical_and_not_reclassified(self):
        self.assertTrue(self.result["v1_replay"]["byte_identical"])
        self.assertEqual(self.result["v1_replay"]["faithful_point_count"], 0)
        self.assertFalse(self.result["v1_replay"]["formal_gate6_eligibility"])

    def test_v2_replay_is_diagnostic_holdout_only(self):
        self.assertEqual(self.result["v2_synthetic_coverage"]["status"], "pass_synthetic_only_not_formal_limits")
        self.assertEqual(len(self.result["old_sentinel_holdout_replay"]), 5)
        self.assertTrue(all(not item["gate6_eligibility"] for item in self.result["old_sentinel_holdout_replay"]))
        self.assertFalse(self.result["formal_acceptance_calibration_from_sentinel"])

    def test_replay_retains_directional_residual_and_all_seed_faces(self):
        fullscale = [item for item in self.result["old_sentinel_holdout_replay"] if item["target"]["max_code"] == 4095]
        self.assertTrue(all(len(item["basis_seed_faces"]) == 5 for item in fullscale))
        self.assertTrue(all(item["color_rendering_residual_retained"] for item in fullscale))
        self.assertTrue(any(item["recorded_trace_replay"]["steps"] for item in fullscale))
        self.assertTrue(all(item["proposed_multiseed_state_machine_replay"]["state_machine_driven"] for item in fullscale))
        self.assertTrue(any(
            item["proposed_multiseed_state_machine_replay"]["status"] == "trace_support_missing"
            for item in fullscale
        ))

    def test_solver_proposal_is_strictly_bounded_and_requires_planner_freeze(self):
        solver = self.result["solver_architecture"]
        self.assertEqual(solver["proposed_max_distinct_face_starts"], 2)
        self.assertEqual(solver["proposed_rounds_per_start"], 8)
        self.assertEqual(solver["ordinary_hard_caps"], {"logical_observations": 54, "physical_cr3": 67})
        self.assertEqual(solver["n5_hard_caps"], {"logical_observations": 62, "physical_cr3": 75})
        self.assertTrue(solver["planner_freeze_required_before_capture"])


if __name__ == "__main__":
    unittest.main()
