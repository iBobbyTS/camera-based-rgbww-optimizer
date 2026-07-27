from __future__ import annotations

import json
import hashlib
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path

from camera_based_rgbww_optimizer.optimization import (
    analyze_p7_thermal_diagnostics as analyzer,
)
from camera_based_rgbww_optimizer.optimization import (
    measure_p7_thermal_diagnostics as measure,
)
from camera_based_rgbww_optimizer.optimization import p7_thermal_diagnostics as thermal


FEATURE_IDS = tuple(
    json.loads(thermal.POLICY_PATH.read_text(encoding="utf-8"))["feature_set"]["ids"]
)


def accepted_capture(*, capture_id: str = "capture", clipped: bool = False) -> dict:
    return {
        "capture_id": capture_id,
        "physical_return_persisted_before_postprocessing": True,
        "cr3": {"path": f"/synthetic/{capture_id}.cr3", "bytes": 100, "sha256": "a" * 64},
        "sidecar": {
            "path": f"/synthetic/{capture_id}.cr3.metadata.json",
            "bytes": 50,
            "sha256": "b" * 64,
        },
        "remote_capture_id": f"capture-{capture_id}",
        "remote_request_id": f"request-{capture_id}",
        "recorded_exposure": {
            "seconds": 1 / 2500,
            "source": "Canon:ExposureTime",
            "status": "recorded",
        },
        "nominal_recorded_ratio_gate": "pass",
        "ray_command_readback": "pass",
        "strip_zero": "pass",
        "source_isolation": "pass",
        "timing_chronology": "pass",
        "no_stale": "pass",
        "budget_accounting": "pass",
        "feature_quality": {
            feature_id: {
                "value": float(index + 1),
                "clipped_fraction": 0.01 if clipped and index == 0 else 0.0,
                "near_noise_floor_fraction": 0.0,
                "valid_pixel_count": 30_000,
            }
            for index, feature_id in enumerate(FEATURE_IDS)
        },
    }


def r6_analyzer_rows() -> list[dict]:
    state_by_index = {
        0: ("A", "initial_anchor", 600),
        5: ("A", "return_after_D", 600),
        10: ("A", "return_after_B", 600),
        15: ("A", "return_after_C", 600),
    }
    rows = []
    for index, capture_id in enumerate(thermal.TD_B_R6_CAPTURE_IDS):
        if index in state_by_index:
            state, role, elapsed = state_by_index[index]
        elif 1 <= index <= 4:
            state, role, elapsed = "D", "measurement", thermal.TIMED_POINTS[index - 1]
        elif 6 <= index <= 9:
            state, role, elapsed = "B", "measurement", thermal.TIMED_POINTS[index - 6]
        else:
            state, role, elapsed = "C", "measurement", thermal.TIMED_POINTS[index - 11]
        rows.append({
            "capture_id": capture_id,
            "origin": "ray_r6",
            "run_root": "/synthetic/ray-r6",
            "engineering_quality_status": "pass",
            "plan_step": {
                "source_id": "ray",
                "state_id": state,
                "role": role,
                "requested_elapsed_s": elapsed,
            },
            "feature_values": {
                feature_id: float(feature_index + 1)
                for feature_index, feature_id in enumerate(FEATURE_IDS)
            },
        })
    return rows


class ExposurePolicyV2Tests(unittest.TestCase):
    def test_policy_binds_exact_r5_and_frozen_science(self):
        policy = thermal.load_td_b_exposure_policy_v2()
        self.assertEqual(policy["supersedes"], thermal.TD_B_R5_SHUTTERS_SHA256)
        self.assertEqual(policy["superseded_plan"]["sha256"], thermal.TD_B_R5_PLAN_SHA256)
        self.assertEqual(policy["provenance"]["feature_count"], 58)
        self.assertEqual(policy["provenance"]["feature_ids_sha256"], thermal.TD_B_FEATURE_IDS_SHA256)
        self.assertEqual(
            [policy["states"][state]["formal_shutter"] for state in ("A", "D", "B")],
            ["1/5000", "1/6400", "1/8000"],
        )

    def test_policy_keeps_c_pending_with_only_two_candidates(self):
        c_state = thermal.load_td_b_exposure_policy_v2()["states"]["C"]
        self.assertEqual(c_state["nominal_candidates"], ["1/2500", "1/3200"])
        self.assertIsNone(c_state["formal_shutter"])
        self.assertEqual(c_state["status"], "pending_qualification")

    def test_policy_rejects_scientific_or_shutter_drift(self):
        policy = thermal.load_td_b_exposure_policy_v2()
        policy["states"]["A"]["formal_shutter"] = "1/4000"
        with self.assertRaisesRegex(ValueError, "differs"):
            thermal.validate_td_b_exposure_policy_v2(policy)


class R5DiagnosticTests(unittest.TestCase):
    def test_r5_diagnostic_is_non_authorizing_and_exactly_classified(self):
        report = analyzer.build_r5_partial_diagnostic()
        self.assertFalse(report["formal_authorizing"])
        self.assertFalse(report["formal_pass"])
        self.assertEqual(report["retained_11_use"], "diagnostic_only")
        self.assertEqual(report["failure_class"], thermal.TD_B_R5_FAILURE_CLASS)
        self.assertNotIn("low_signal", report["failure_class"])

    def test_r5_diagnostic_prohibits_011_and_missing_slots_from_inference(self):
        report = analyzer.build_r5_partial_diagnostic()
        self.assertEqual(report["missing_slots"], ["011", "012", "013", "014", "015"])
        self.assertEqual(report["r5_capture_011_quality"], "invalid")
        self.assertTrue(all(
            value == "not_evaluated"
            for value in report["formal_analysis_fields"].values()
        ))
        self.assertFalse(report["old_new_pooling_allowed"])

    def test_r5_manifest_is_stable_and_rejects_other_root(self):
        first = analyzer.r5_formal_tree_manifest()
        second = analyzer.r5_formal_tree_manifest()
        self.assertEqual(first, second)
        with self.assertRaisesRegex(ValueError, "exact retained"):
            analyzer.r5_formal_tree_manifest(thermal.PROJECT_ROOT)


class EqR6ContractTests(unittest.TestCase):
    def test_plan_fixes_budgets_ids_and_a_to_c_precondition(self):
        plan = thermal.build_td_b_eq_r6_plan()
        self.assertEqual(
            (plan["formal"], plan["ambient"], plan["retry"], plan["candidate_count_cap"],
             plan["candidate_physical"], plan["setup_physical_cap"]),
            (0, 0, 0, 2, 4, 8),
        )
        self.assertEqual(
            tuple(plan["candidates"][0]["capture_ids"]),
            thermal.TD_B_EQ_CAPTURE_IDS[0],
        )
        self.assertEqual(plan["candidates"][0]["precondition"]["ray_a_dwell_s"], 600)
        self.assertEqual(plan["candidates"][0]["precondition"]["ray_a_capture_count"], 0)

    def test_required_feature_clipping_is_a_hard_failure(self):
        failures = thermal.td_b_eq_capture_quality_failures(
            accepted_capture(clipped=True), required_feature_ids=FEATURE_IDS,
        )
        self.assertEqual(failures, ("clipping",))

    def test_required_feature_order_cannot_change(self):
        row = accepted_capture()
        row["feature_quality"] = dict(reversed(tuple(row["feature_quality"].items())))
        self.assertIn(
            "required_58_features",
            thermal.td_b_eq_capture_quality_failures(
                row, required_feature_ids=FEATURE_IDS,
            ),
        )
        with self.assertRaisesRegex(ValueError, "exact ordered"):
            thermal.td_b_eq_capture_quality_failures(
                accepted_capture(), required_feature_ids=tuple(reversed(FEATURE_IDS)),
            )

    def test_candidate_one_four_of_four_qualifies_without_candidate_two(self):
        rows = [[accepted_capture(capture_id=value) for value in thermal.TD_B_EQ_CAPTURE_IDS[0]]]
        result = thermal.classify_td_b_eq_r6(rows, required_feature_ids=FEATURE_IDS)
        self.assertEqual(result["status"], "qualified_1_2500")
        self.assertEqual(result["candidate_2_call_count"], 0)

    def test_only_clipping_unlocks_candidate_two(self):
        first = accepted_capture(clipped=True)
        second = [accepted_capture(capture_id=value) for value in thermal.TD_B_EQ_CAPTURE_IDS[1]]
        result = thermal.classify_td_b_eq_r6([[first], second], required_feature_ids=FEATURE_IDS)
        self.assertEqual(result["status"], "qualified_1_3200")
        nonclipping = accepted_capture()
        nonclipping["feature_quality"][FEATURE_IDS[0]]["near_noise_floor_fraction"] = 0.2
        with self.assertRaisesRegex(ValueError, "prohibits candidate 2"):
            thermal.classify_td_b_eq_r6([[nonclipping], second], required_feature_ids=FEATURE_IDS)

    def test_candidate_two_failure_is_unresolved(self):
        first = accepted_capture(clipped=True)
        second = [accepted_capture(capture_id=value) for value in thermal.TD_B_EQ_CAPTURE_IDS[1]]
        second[-1]["feature_quality"][FEATURE_IDS[0]]["valid_pixel_count"] = 1
        result = thermal.classify_td_b_eq_r6([[first], second], required_feature_ids=FEATURE_IDS)
        self.assertEqual(result["status"], "exposure_window_unresolved")

    def test_fake_scheduler_records_wait_cleanup_attempts_and_zero_real_calls(self):
        plan = thermal.build_td_b_eq_r6_plan()
        events = []

        def capture(request):
            return accepted_capture(
                capture_id=request["capture_id"],
                clipped=request["candidate_index"] == 1,
            )

        report = measure.run_td_b_eq_r6_fake(
            plan,
            capture_fn=capture,
            event_fn=events.append,
            cleanup_fn=lambda _name: {"status": "pass"},
        )
        self.assertEqual(report["status"], "qualified_1_3200")
        self.assertEqual(report["attempted_capture_calls"], 5)
        self.assertEqual(len(report["cleanup_ledger"]), 8)
        self.assertIn(
            {"event": "fake_wait", "candidate_index": 1, "duration_s": 600, "capture_count": 0},
            events,
        )
        self.assertEqual(
            (report["device_calls"], report["network_calls"], report["real_cleanup_calls"], report["retry"]),
            (0, 0, 0, 0),
        )

    def test_fake_scheduler_stops_nonclipping_without_candidate_two(self):
        def capture(request):
            row = accepted_capture(capture_id=request["capture_id"])
            row["recorded_exposure"] = None
            return row

        report = measure.run_td_b_eq_r6_fake(
            thermal.build_td_b_eq_r6_plan(),
            capture_fn=capture,
            event_fn=lambda _event: None,
            cleanup_fn=lambda _name: {"status": "pass"},
        )
        self.assertEqual(report["status"], "run_invalid")
        self.assertEqual(report["attempted_capture_calls"], 1)
        self.assertEqual(report["classification"]["candidate_2_call_count"], 0)

    def test_fake_scheduler_cleanup_failure_hard_stops(self):
        with self.assertRaisesRegex(ValueError, "cleanup failed"):
            measure.run_td_b_eq_r6_fake(
                thermal.build_td_b_eq_r6_plan(),
                capture_fn=lambda request: accepted_capture(capture_id=request["capture_id"]),
                event_fn=lambda _event: None,
                cleanup_fn=lambda name: {"status": "fail" if name == "shell" else "pass"},
            )


class RayR6ContractTests(unittest.TestCase):
    def test_pre_eq_formal_plan_is_non_executable_and_exact(self):
        plan = thermal.build_td_b_r6_formal_plan()
        self.assertFalse(plan["executable"])
        self.assertEqual(plan["status"], "pending_exposure_policy_non_executable")
        self.assertEqual(plan["capture_ids"], list(thermal.TD_B_R6_CAPTURE_IDS))
        self.assertIsNone(plan["state_shutters"]["C"])
        self.assertEqual(
            (plan["formal_logical"], plan["formal_physical_cap"], plan["ambient"],
             plan["setup_in_formal_root"], plan["launch"], plan["retry"]),
            (16, 16, 0, 0, 1, 0),
        )

    def test_pre_eq_c_materialization_and_plan_drift_fail_closed(self):
        with self.assertRaisesRegex(ValueError, "cannot finalize"):
            thermal.build_td_b_r6_formal_plan(selected_c_shutter="1/2500")
        plan = thermal.build_td_b_r6_formal_plan()
        plan["retry"] = 1
        with self.assertRaisesRegex(ValueError, "differs"):
            thermal.validate_td_b_r6_formal_plan(plan)

    def test_formal_ledger_rejects_order_pooling_and_invalid_quality(self):
        rows = []
        policy = thermal.load_td_b_exposure_policy_v2()
        for capture_id in thermal.TD_B_R6_CAPTURE_IDS:
            row = accepted_capture(capture_id=capture_id)
            if "-ray-a" in capture_id:
                state = "A"
            elif "-ray-d-" in capture_id:
                state = "D"
            elif "-ray-b-" in capture_id:
                state = "B"
            else:
                state = "C"
            shutter = (
                "1/2500" if state == "C" else policy["states"][state]["formal_shutter"]
            )
            row.update({
                "origin": "ray_r6",
                "run_root": "/synthetic/r6",
                "state_id": state,
                "nominal_shutter": shutter,
                "exposure_mode": "fixed",
                "weak_reacquire": False,
                "mid_run_shutter_change": False,
            })
            rows.append(row)
        thermal.validate_td_b_r6_capture_ledger(
            rows, required_feature_ids=FEATURE_IDS, selected_c_shutter="1/2500",
        )
        reordered = deepcopy(rows)
        reordered[0], reordered[1] = reordered[1], reordered[0]
        with self.assertRaisesRegex(ValueError, "order"):
            thermal.validate_td_b_r6_capture_ledger(
                reordered, required_feature_ids=FEATURE_IDS, selected_c_shutter="1/2500",
            )
        pooled = deepcopy(rows)
        pooled[-1]["origin"] = "r5"
        with self.assertRaisesRegex(ValueError, "pooling"):
            thermal.validate_td_b_r6_capture_ledger(
                pooled, required_feature_ids=FEATURE_IDS, selected_c_shutter="1/2500",
            )
        auto = deepcopy(rows)
        auto[1]["exposure_mode"] = "auto"
        with self.assertRaisesRegex(ValueError, "shutter contract"):
            thermal.validate_td_b_r6_capture_ledger(
                auto, required_feature_ids=FEATURE_IDS, selected_c_shutter="1/2500",
            )

    def test_r6_analyzer_requires_complete_exact_accepted_sequence(self):
        rows = r6_analyzer_rows()
        report = analyzer.analyze_td_b(
            rows,
            feature_ids=FEATURE_IDS,
            compatibility_fn=lambda _left, _right: True,
            r6_operational_contract=True,
        )
        self.assertTrue(report["formal_pass"])
        self.assertEqual(report["return_anchor_history"], "pass")
        self.assertEqual(report["steady_status"], "not_demonstrated")
        self.assertEqual(report["claim"], "selected_fixed_time_transient_not_proven_steady")
        self.assertTrue(report["operational_endpoint_600_valid"])
        with self.assertRaisesRegex(ValueError, "16/16"):
            analyzer.analyze_td_b(
                rows[:-1],
                feature_ids=FEATURE_IDS,
                compatibility_fn=lambda _left, _right: True,
                r6_operational_contract=True,
            )

    def test_r6_analyzer_history_failure_blocks_operational_endpoint(self):
        report = analyzer.analyze_td_b(
            r6_analyzer_rows(),
            feature_ids=FEATURE_IDS,
            compatibility_fn=lambda _left, _right: False,
            r6_operational_contract=True,
        )
        self.assertFalse(report["formal_pass"])
        self.assertEqual(report["return_anchor_history"], "fail")
        self.assertFalse(report["operational_endpoint_600_valid"])

    def test_machine_status_preserves_downstream_locks(self):
        status = thermal.td_b_r6_machine_status()
        self.assertEqual(status["r5"]["retained_11_use"], "diagnostic_only")
        self.assertEqual(status["exposure_qualification"]["physical_cap"], 8)
        self.assertEqual(status["ray_r6"]["formal_planned"], 16)
        self.assertEqual(status["ray_r6"]["formal_accepted"], 0)
        self.assertEqual(status["locks"]["strip"], "blocked_until_ray_r6_pass")
        self.assertEqual(status["locks"]["td_c"], "blocked_until_combined_td_b_pass")
        self.assertTrue(status["locks"]["sentinel"])
        self.assertTrue(status["locks"]["p8"])

    def test_failure_contract_keeps_strip_and_retry_zero(self):
        failure = thermal.build_td_b_r6_formal_plan()["failure_contract"]
        self.assertEqual(failure["classification"], "accepted_hard_failed_formal_attempt")
        self.assertFalse(failure["formal_pass"])
        self.assertEqual(failure["strip_call_count"], 0)
        self.assertEqual(failure["retry"], 0)


class PreEqC1EvidenceContractTests(unittest.TestCase):
    ALLOWED = ("src/owner.py",)

    def scan(self, current: str, baseline: str = "") -> dict:
        baseline_hash = hashlib.sha256(baseline.encode("utf-8")).hexdigest()
        return thermal.scan_td_b_r6_offline_sources(
            {"src/owner.py": current},
            baseline_sources={"src/owner.py": baseline},
            expected_baseline_sha256={"src/owner.py": baseline_hash},
            allowed_paths=self.ALLOWED,
            allowed_absolute_roots=(
                thermal.PROJECT_ROOT,
                "/Volumes/4T/temp/rgbww-optimizer",
                "/synthetic",
            ),
        )

    def test_exact_baseline_identifier_is_classified_not_ignored(self):
        source = f'OVERRIDE = "{thermal.TD_B_R6_PRIVATE_OVERRIDE_IDENTIFIER}"\n'
        result = self.scan(source, source)
        self.assertEqual(result["status"], "pass")
        self.assertEqual(result["findings"], [])
        self.assertEqual(
            result["baseline_identifier_classifications"][0]["classification"],
            "known_identifier_not_secret_value",
        )
        self.assertEqual(result["baseline_identifier_classifications"][0]["occurrences"], 1)

    def test_new_identifier_occurrence_or_new_path_fails(self):
        baseline = f'OVERRIDE = "{thermal.TD_B_R6_PRIVATE_OVERRIDE_IDENTIFIER}"\n'
        added = baseline + f'SECOND = "{thermal.TD_B_R6_PRIVATE_OVERRIDE_IDENTIFIER}"\n'
        self.assertEqual(self.scan(added, baseline)["status"], "fail")
        result = thermal.scan_td_b_r6_offline_sources(
            {"src/new.py": baseline},
            baseline_sources={},
            expected_baseline_sha256={},
            allowed_paths=("src/new.py",),
            allowed_absolute_roots=(thermal.PROJECT_ROOT,),
        )
        self.assertEqual(result["status"], "fail")

    def test_baseline_hash_drift_fails_identifier_classification(self):
        baseline = f'OVERRIDE = "{thermal.TD_B_R6_PRIVATE_OVERRIDE_IDENTIFIER}"\n'
        result = thermal.scan_td_b_r6_offline_sources(
            {"src/owner.py": baseline},
            baseline_sources={"src/owner.py": baseline},
            expected_baseline_sha256={"src/owner.py": "0" * 64},
            allowed_paths=self.ALLOWED,
            allowed_absolute_roots=(thermal.PROJECT_ROOT,),
        )
        self.assertEqual(result["status"], "fail")

    def test_literal_private_value_is_redacted_and_fails(self):
        private_fixture = "fabricated-" + "private-value-123"
        private_label = "api_" + "key"
        result = self.scan(f'{private_label} = "{private_fixture}"\n')
        self.assertEqual(result["status"], "fail")
        finding = result["findings"][0]
        self.assertEqual(finding["kind"], "literal_credential_or_private_value")
        self.assertNotIn("fabricated", json.dumps(finding))
        self.assertRegex(finding["redacted_sha256"], r"^[0-9a-f]{64}$")

    def test_environment_read_and_serialization_fail(self):
        env_read = "os." + 'getenv("SOME_NAME")'
        result = self.scan(f"value = {env_read}\n")
        self.assertEqual(result["status"], "fail")
        self.assertIn(
            "environment_value_read_or_serialization",
            {item["kind"] for item in result["findings"]},
        )

    def test_new_network_target_fails_without_echoing_target(self):
        target = "http://" + "new-target" + ".local/api"
        result = self.scan(f'endpoint = "{target}"\n')
        self.assertEqual(result["status"], "fail")
        finding = next(item for item in result["findings"] if item["kind"] == "network_target")
        self.assertNotIn("new-target", json.dumps(finding))

    def test_outside_path_symlink_and_unlisted_path_fail(self):
        outside_path = "/" + "private/outside/result.json"
        outside = self.scan(f'path = "{outside_path}"\n')
        self.assertEqual(outside["status"], "fail")
        symlink = thermal.scan_td_b_r6_offline_sources(
            {"src/owner.py": ""},
            baseline_sources={"src/owner.py": ""},
            expected_baseline_sha256={
                "src/owner.py": hashlib.sha256(b"").hexdigest(),
            },
            allowed_paths=self.ALLOWED,
            allowed_absolute_roots=(thermal.PROJECT_ROOT,),
            symlink_paths=("src/owner.py",),
        )
        self.assertEqual(symlink["status"], "fail")
        unlisted = thermal.scan_td_b_r6_offline_sources(
            {"src/unlisted.py": ""},
            baseline_sources={},
            expected_baseline_sha256={},
            allowed_paths=self.ALLOWED,
            allowed_absolute_roots=(thermal.PROJECT_ROOT,),
        )
        self.assertEqual(unlisted["status"], "fail")

    @staticmethod
    def references(root: Path) -> list[dict]:
        references = []
        for name in thermal.TD_B_R6_PRE_EQ_PRE_SUMMARY_ARTIFACTS:
            path = root / name
            references.append({
                "path": str(path),
                "bytes": path.stat().st_size,
                "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            })
        return references

    @staticmethod
    def write_payloads(root: Path) -> None:
        for name in thermal.TD_B_R6_PRE_EQ_PRE_SUMMARY_ARTIFACTS:
            (root / name).write_text(
                json.dumps({"name": name, "status": "pass"}) + "\n",
                encoding="utf-8",
            )

    def build_package(self, root: Path, *, child_status: str = "pass") -> tuple[dict, dict, str]:
        self.write_payloads(root)
        validation = thermal.build_td_b_r6_pre_eq_validation_summary(
            self.references(root),
            case_results=({"case": "integrated", "status": child_status},),
        )
        validation_path = root / "validation-summary.json"
        validation_path.write_text(json.dumps(validation, sort_keys=True) + "\n", encoding="utf-8")
        validation_ref = {
            "path": str(validation_path),
            "bytes": validation_path.stat().st_size,
            "sha256": hashlib.sha256(validation_path.read_bytes()).hexdigest(),
        }
        terminal = thermal.build_td_b_r6_pre_eq_terminal_summary(
            validation_ref,
            validation_status=validation["status"],
        )
        terminal_path = root / "terminal-summary.json"
        terminal_path.write_text(json.dumps(terminal, sort_keys=True) + "\n", encoding="utf-8")
        terminal_hash = hashlib.sha256(terminal_path.read_bytes()).hexdigest()
        return validation, terminal, terminal_hash

    def test_summary_and_terminal_use_distinct_11_12_13_phase_counts(self):
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            validation, terminal, terminal_hash = self.build_package(root)
            self.assertEqual(validation["indexed_preterminal_count"], 11)
            self.assertEqual(len(validation["artifacts"]), 11)
            self.assertEqual(terminal["canonical_root_json_count"], 13)
            self.assertEqual(terminal["validation_summary_count"], 1)
            self.assertEqual(terminal["terminal_self_count"], 1)
            self.assertNotIn("sha256", terminal["terminal_self"])
            seal = thermal.validate_td_b_r6_pre_eq_terminal_seal(
                root, external_terminal_sha256=terminal_hash,
            )
            self.assertEqual(seal["status"], "pass", seal)
            self.assertEqual(seal["canonical_root_json_count"], 13)

    def test_child_failure_propagates_to_validation_terminal_and_handoff(self):
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            validation, terminal, _ = self.build_package(root, child_status="fail")
            self.assertEqual(validation["status"], "fail")
            self.assertEqual(terminal["status"], "fail")
            handoff = {
                "validation_status": "fail",
                "indexed_preterminal_count": 11,
                "terminal_status": "fail",
                "canonical_root_json_count": 13,
                "first_sentence_kind": "failure",
            }
            self.assertEqual(
                thermal.validate_td_b_r6_pre_eq_handoff(
                    validation, terminal, handoff,
                )["status"],
                "pass",
            )

    def test_handoff_cannot_claim_pass_or_hide_failure(self):
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            validation, terminal, _ = self.build_package(root, child_status="fail")
            result = thermal.validate_td_b_r6_pre_eq_handoff(
                validation,
                terminal,
                {
                    "validation_status": "pass",
                    "indexed_preterminal_count": 11,
                    "terminal_status": "pass",
                    "canonical_root_json_count": 13,
                    "first_sentence_kind": "success",
                },
            )
            self.assertEqual(result["status"], "fail")
            self.assertIn("first_sentence_kind", result["mismatches"])

    def test_terminal_seal_rejects_missing_extra_stale_hash_and_external_hash(self):
        for mutation in ("missing", "extra", "stale", "external"):
            with self.subTest(mutation=mutation), tempfile.TemporaryDirectory() as tempdir:
                root = Path(tempdir)
                _, _, terminal_hash = self.build_package(root)
                if mutation == "missing":
                    (root / thermal.TD_B_R6_PRE_EQ_PRE_SUMMARY_ARTIFACTS[0]).unlink()
                elif mutation == "extra":
                    (root / "extra.json").write_text("{}\n", encoding="utf-8")
                elif mutation == "stale":
                    (root / thermal.TD_B_R6_PRE_EQ_PRE_SUMMARY_ARTIFACTS[0]).write_text(
                        '{"mutated":true}\n', encoding="utf-8",
                    )
                else:
                    terminal_hash = "0" * 64
                seal = thermal.validate_td_b_r6_pre_eq_terminal_seal(
                    root, external_terminal_sha256=terminal_hash,
                )
                self.assertEqual(seal["status"], "fail")

    def test_summary_rejects_duplicate_or_incomplete_reference_index(self):
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            self.write_payloads(root)
            references = self.references(root)
            for invalid in (references[:-1], [references[0], *references[1:-1], references[0]]):
                summary = thermal.build_td_b_r6_pre_eq_validation_summary(
                    invalid,
                    case_results=({"case": "children", "status": "pass"},),
                )
                self.assertEqual(summary["status"], "fail")


if __name__ == "__main__":
    unittest.main()
