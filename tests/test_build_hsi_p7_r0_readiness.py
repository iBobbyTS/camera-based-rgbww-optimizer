from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from camera_based_rgbww_optimizer.optimization import build_hsi_p7_r0_readiness as subject


class BuildHsiP7R0ReadinessTests(unittest.TestCase):
    def test_final_readiness_reports_guarded_physical_precheck_without_success_roundtrip(self):
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            sentinel = root / "sentinel"
            sentinel.mkdir()
            for name in ("run.json", "plan.json", "target-results.jsonl"):
                (sentinel / name).write_text("{}\n", encoding="utf-8")
            source = root / "source.py"
            source.write_text("# frozen test source\n", encoding="utf-8")
            waiting = root / "waiting.json"
            waiting.write_text("{}\n", encoding="utf-8")
            replay = root / "replay.json"
            replay.write_text(json.dumps({
                "status": "ready_for_planner_review",
                "device_calls_performed": False,
                "v1_replay": {},
                "v2_synthetic_coverage": {},
                "old_sentinel_holdout_replay": {},
                "solver_architecture": {},
                "locked": ["P7-R1"],
            }), encoding="utf-8")
            dry_run = root / "dry-run.json"
            dry_run.write_text(json.dumps({
                "formal_capture_eligible": False,
                "authorization": {"status": "not_authorized_for_execution"},
                "experiment": "p7_targeted_reference_repeatability_v2",
                "measurement": {
                    "formal_ray_count": 30,
                    "formal_strip_count": 50,
                    "physical_capture_audit": {
                        "absolute_cap_status": "planner_frozen",
                        "maximum_total_physical_cr3": 250,
                        "baseline_physical_range_without_weak_reacquire": "82..170",
                        "permitted_physical_range_with_weak_reacquire": "82..250",
                        "maximum_60_second_settling_seconds": 9600,
                    },
                },
                "execution_contract": {
                    "candidate_status": "calibrated_waiting_for_planner",
                    "candidate_formal_capture_eligible": False,
                },
            }), encoding="utf-8")
            fake_analysis = root / "analysis.json"
            fake_analysis.write_text(json.dumps({
                "analysis": "strip_hsi_pilot_v2_formal_analysis",
                "policy_version": "v2",
                "point_count": 4,
                "anchor_validation": {"anchor_count": 12},
                "target_evidence_validation": {
                    "three_layer_result_audit": "pass",
                    "objective_replay_audit": "pass",
                    "capture_owner_audit": "pass",
                },
            }), encoding="utf-8")

            with (
                mock.patch.object(subject, "DEFAULT_SENTINEL_RUN", sentinel),
                mock.patch.object(subject, "DEFAULT_WAITING_OUTPUT", waiting),
                mock.patch.object(subject, "SOURCE_FILES", (source,)),
            ):
                readiness = subject.build_readiness(
                    replay_path=replay,
                    dry_run_plan=dry_run,
                    fake_sentinel_analysis=fake_analysis,
                    test_count=1,
                    validation_commands=["unit: pass"],
                    wrapper_paths=["tmp/run-strip-hsi-pilot.zsh"],
                )

        self.assertEqual(readiness["schema_version"], 3)
        self.assertEqual(readiness["readiness"], "P7-R0K-offline-final-v9")
        contract = readiness["exhaustibility_matrix"]["physical.pre_capture_denial"]
        self.assertEqual(contract["classification"], "guarded_unreachable")
        self.assertEqual(contract["formal_status"], "not_emitted")
        evidence = readiness["production_roundtrip"]["physical_pre_capture_denial"]
        self.assertFalse(evidence["production_success_roundtrip"])
        self.assertEqual(evidence["runner_canonicalizer_rejection"], "pass")
        self.assertEqual(evidence["public_analyzer_rejection"], "pass")
        self.assertEqual(
            readiness["exhaustibility_path_evidence"]["physical.pre_capture_denial"]["evidence_type"],
            "n3_n5_producer_unreachability_plus_runner_and_public_analyzer_rejection",
        )


if __name__ == "__main__":
    unittest.main()
