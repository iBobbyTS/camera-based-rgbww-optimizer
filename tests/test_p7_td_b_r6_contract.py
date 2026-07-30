from __future__ import annotations

import json
import hashlib
import os
import stat
import subprocess
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from camera_based_rgbww_optimizer.optimization import (
    analyze_p7_thermal_diagnostics as analyzer,
)
from camera_based_rgbww_optimizer.optimization import (
    measure_p7_thermal_diagnostics as measure,
)
from camera_based_rgbww_optimizer.optimization import p7_thermal_diagnostics as thermal
from tests.test_p7_thermal_diagnostics import _attach_v2_capture_evidence


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

    def test_policy_finalizes_qualified_c_without_authorizing_formal(self):
        policy = thermal.load_td_b_exposure_policy_v2()
        c_state = policy["states"]["C"]
        self.assertEqual(c_state["nominal_candidates"], ["1/2500", "1/3200"])
        self.assertEqual(c_state["formal_shutter"], "1/2500")
        self.assertEqual(c_state["status"], "qualified")
        self.assertEqual(policy["exposure_qualification_status"], "qualified_1_2500")
        self.assertEqual(policy["selected_state_c_nominal_shutter"], "1/2500")
        self.assertEqual(
            policy["selected_state_c_recorded_exposure_range"],
            {
                "owner": "Canon:ExposureTime",
                "min_seconds": 0.000387549084953174,
                "max_seconds": 0.000387549084953174,
            },
        )
        forbidden_claims = {
            "formal_pass", "td_b_pass", "history_pass", "release_usable",
            "production_release_usable", "product_ready", "state_c_settled",
        }
        self.assertTrue(forbidden_claims.isdisjoint(policy))

    def test_policy_rejects_scientific_or_shutter_drift(self):
        policy = thermal.load_td_b_exposure_policy_v2()
        policy["states"]["A"]["formal_shutter"] = "1/4000"
        with self.assertRaisesRegex(ValueError, "differs"):
            thermal.validate_td_b_exposure_policy_v2(policy)

    def test_selected_policy_hash_is_the_external_file_hash(self):
        expected = hashlib.sha256(thermal.TD_B_EXPOSURE_POLICY_V2_PATH.read_bytes()).hexdigest()
        self.assertEqual(len(expected), 64)
        self.assertNotIn("selected_policy_hash", thermal.load_td_b_exposure_policy_v2())


class EqFamilyManifestTests(unittest.TestCase):
    def test_manifest_ignores_only_root_regular_ds_store(self):
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            os.chmod(root, 0o700)
            (root / "evidence.json").write_bytes(b"evidence")
            os.chmod(root / "evidence.json", 0o600)
            baseline = thermal.build_planner_eq_family_manifest(root)

            ds_store = root / ".DS_Store"
            ds_store.write_bytes(b"Finder metadata version one")
            os.chmod(ds_store, 0o644)
            with_metadata = thermal.build_planner_eq_family_manifest(root)
            ds_store.write_bytes(b"Finder metadata changed")
            after_payload_change = thermal.build_planner_eq_family_manifest(root)

            for manifest in (with_metadata, after_payload_change):
                self.assertEqual(manifest["rows"], baseline["rows"])
                self.assertEqual(
                    tuple(manifest[key] for key in (
                        "entries", "files", "directories", "symlinks", "other",
                        "payload_bytes", "sha256", "payload",
                    )),
                    tuple(baseline[key] for key in (
                        "entries", "files", "directories", "symlinks", "other",
                        "payload_bytes", "sha256", "payload",
                    )),
                )

    def test_manifest_does_not_hide_unsafe_or_nested_ds_store(self):
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            os.chmod(root, 0o700)
            (root / ".DS_Store").symlink_to(root.parent)
            with self.assertRaisesRegex(ValueError, "symlink"):
                thermal.build_planner_eq_family_manifest(root)

        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            os.chmod(root, 0o700)
            baseline = thermal.build_planner_eq_family_manifest(root)
            nested = root / "nested"
            nested.mkdir(mode=0o700)
            (nested / ".DS_Store").write_bytes(b"nested evidence")
            manifest = thermal.build_planner_eq_family_manifest(root)
            self.assertIn("nested/.DS_Store", [row["path"] for row in manifest["rows"]])
            self.assertNotEqual(manifest["sha256"], baseline["sha256"])

    def test_exact_family_manifest_matches_frozen_digest_and_qualification(self):
        manifest = thermal.build_planner_eq_family_manifest(
            thermal.TD_B_EQ_R6_ACCEPTED_ROOT,
        )
        self.assertEqual(
            (manifest["entries"], manifest["files"], manifest["directories"],
             manifest["symlinks"], manifest["other"], manifest["payload_bytes"]),
            (47, 42, 5, 0, 0, 7980),
        )
        self.assertEqual(manifest["sha256"], thermal.TD_B_EQ_R6_MANIFEST_SHA256)
        self.assertEqual(
            manifest["rows"][0],
            {"mode": "0o700", "path": "prelaunch", "type": "dir"},
        )
        self.assertNotIn("bytes", manifest["rows"][0])
        self.assertNotIn("sha256", manifest["rows"][0])
        audit = thermal.audit_td_b_eq_r6_qualification(
            thermal.TD_B_EQ_R6_ACCEPTED_ROOT,
        )
        self.assertEqual(audit["status"], "qualified_1_2500")
        self.assertEqual(audit["selected_shutter"], "1/2500")
        self.assertEqual(audit["candidate_launch_count"], 1)
        self.assertEqual(audit["candidate_2_call_count"], 0)
        self.assertEqual(
            (audit["attempted_capture_calls"], audit["physical_returned_cr3_count"],
             audit["accepted_capture_count"]),
            (4, 4, 4),
        )
        self.assertEqual(audit["feature_counts"], [58, 58, 58, 58])
        self.assertEqual(
            audit["recorded_exposure_seconds"],
            [0.000387549084953174] * 4,
        )
        self.assertEqual(audit["recorded_to_nominal_ratio"], 0.9688727123829349)

    def test_manifest_serializer_and_unsafe_types_fail_closed(self):
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            os.chmod(root, 0o700)
            (root / "z").mkdir(mode=0o700)
            (root / "a.txt").write_bytes(b"alpha")
            os.chmod(root / "a.txt", 0o600)
            manifest = thermal.build_planner_eq_family_manifest(root)
            self.assertEqual([row["path"] for row in manifest["rows"]], ["a.txt", "z"])
            self.assertEqual(manifest["rows"][0]["type"], "file")
            self.assertEqual(manifest["rows"][0]["mode"], "0o600")
            expected_payload = json.dumps(
                manifest["rows"],
                sort_keys=True,
                separators=(",", ":"),
                ensure_ascii=False,
                allow_nan=False,
            ).encode("utf-8")
            self.assertEqual(manifest["payload"], expected_payload)
            self.assertFalse(manifest["payload"].endswith(b"\n"))
            before_sha256 = manifest["sha256"]
            (root / "a.txt").write_bytes(b"changed")
            self.assertNotEqual(
                thermal.build_planner_eq_family_manifest(root)["sha256"],
                before_sha256,
            )
            (root / "escape").symlink_to(root.parent)
            with self.assertRaisesRegex(ValueError, "symlink"):
                thermal.build_planner_eq_family_manifest(root)

    def test_qualification_rejects_wrong_root_and_artifact_hash_drift(self):
        with tempfile.TemporaryDirectory() as tempdir:
            with self.assertRaisesRegex(ValueError, "exact accepted"):
                thermal.audit_td_b_eq_r6_qualification(Path(tempdir))
        drifted = dict(thermal.TD_B_EQ_R6_ARTIFACT_SHA256)
        drifted["run/outer-result.json"] = "0" * 64
        with patch.object(thermal, "TD_B_EQ_R6_ARTIFACT_SHA256", drifted):
            with self.assertRaisesRegex(ValueError, "artifact drifted"):
                thermal.audit_td_b_eq_r6_qualification(
                    thermal.TD_B_EQ_R6_ACCEPTED_ROOT,
                )

    @unittest.skipUnless(hasattr(os, "mkfifo"), "FIFO creation unavailable")
    def test_manifest_rejects_other_filesystem_types(self):
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            os.chmod(root, 0o700)
            os.mkfifo(root / "fifo")
            with self.assertRaisesRegex(ValueError, "unsupported filesystem type"):
                thermal.build_planner_eq_family_manifest(root)


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
        early = deepcopy(second[0])
        early["feature_quality"][FEATURE_IDS[0]]["valid_pixel_count"] = 1
        result = thermal.classify_td_b_eq_r6(
            [[first], [early]], required_feature_ids=FEATURE_IDS,
        )
        self.assertEqual(result["status"], "exposure_window_unresolved")
        self.assertEqual(result["candidate_2_call_count"], 1)

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


class EqR6LiveOwnerTests(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory(
            dir="/Volumes/4T/temp/rgbww-optimizer",
        )
        self.parent = Path(self.tempdir.name)

    def tearDown(self):
        self.tempdir.cleanup()

    def live_plan(self, name: str = "eq-live") -> dict:
        return thermal.activate_td_b_eq_r6_live_plan(
            thermal.build_td_b_eq_r6_plan(),
            code_checkpoint="a" * 40,
            output_root=self.parent / name,
            wrapper_path=measure.PRODUCTION_WRAPPER,
            measurement_runner_path=Path(measure.__file__),
        )

    @staticmethod
    def passing_zero():
        return {"status": "pass", "generation_bearing_zero": True}

    @staticmethod
    def passing_command():
        return {"status": "pass"}

    @staticmethod
    def passing_cleanup():
        return {"status": "pass", "steps": [{"ok": True}]}

    @staticmethod
    def passing_final_zero():
        return {
            "status": "pass",
            "strip_verified_off": True,
            "ray_verified_off": True,
        }

    def capture_factory(self, root: Path, *, clipped: bool = False, invalid: bool = False):
        def capture(request):
            result = _attach_v2_capture_evidence(
                root, request, {}, observed=float(request["requested_elapsed_s"]),
            )
            quality = accepted_capture(
                capture_id=request["capture_id"],
                clipped=clipped,
            )
            quality.update({
                "requested_elapsed_s": request["requested_elapsed_s"],
                "nominal_shutter": request["nominal_shutter"],
            })
            if invalid:
                quality["recorded_exposure"] = None
            result["quality_capture"] = quality
            return result
        return capture

    def prepare_candidate(self, live: dict, candidate_index: int) -> Path:
        outer = Path(live["output_root"])
        outer.mkdir(parents=True, exist_ok=True)
        root = outer / f"candidate-{candidate_index}"
        runtime_argv = ["--eq-r6-single-candidate", str(candidate_index)]
        measure.write_td_b_eq_r6_launch_ledger(
            live,
            candidate_index=candidate_index,
            candidate_root=root,
            outer_pid=111,
            wrapper_pid=222,
            runner_pid=333,
            argv=runtime_argv,
        )
        return root

    def run_candidate(self, live: dict, candidate_index: int, capture_fn) -> dict:
        root = self.prepare_candidate(live, candidate_index)
        result = measure.run_td_b_eq_r6_single_candidate(
            live,
            candidate_index=candidate_index,
            candidate_root=root,
            strip_zero_fn=self.passing_zero,
            ray_a_fn=self.passing_command,
            ray_c_fn=self.passing_command,
            capture_fn=capture_fn(root) if callable(capture_fn) else capture_fn,
            python_cleanup_fn=self.passing_cleanup,
            runtime_outer_pid=111,
            runtime_wrapper_pid=222,
            runtime_runner_pid=333,
            runtime_argv=["--eq-r6-single-candidate", str(candidate_index)],
            sleep_fn=lambda _seconds: None,
            monotonic_fn=lambda: 0.0,
        )
        return json.loads(result.read_text(encoding="utf-8"))

    def test_activation_is_explicit_unique_and_rejects_contract_drift(self):
        live = self.live_plan()
        self.assertTrue(live["executable"])
        self.assertEqual(live["physical_cr3_cap"], 8)
        thermal.validate_td_b_eq_r6_live_plan(live, require_fresh_root=True)
        drift = deepcopy(live)
        drift["offline_plan"]["retry"] = 1
        with self.assertRaisesRegex(ValueError, "offline contract"):
            thermal.validate_td_b_eq_r6_live_plan(drift, require_fresh_root=True)
        Path(live["output_root"]).mkdir()
        with self.assertRaisesRegex(ValueError, "not fresh"):
            thermal.validate_td_b_eq_r6_live_plan(live, require_fresh_root=True)

    def test_single_candidate_accounts_attempt_return_accept_and_stops_clipping(self):
        live = self.live_plan()
        root_holder = {}

        def factory(root):
            root_holder["root"] = root
            calls = 0

            def capture(request):
                nonlocal calls
                calls += 1
                return self.capture_factory(root, clipped=calls == 2)(request)
            return capture

        result = self.run_candidate(live, 1, factory)
        self.assertEqual(result["classification"], "clipping_only")
        self.assertEqual(
            (
                result["attempted_capture_calls"],
                result["physical_returned_cr3_count"],
                result["accepted_capture_count"],
            ),
            (2, 2, 1),
        )
        events = [
            json.loads(line)
            for line in (root_holder["root"] / "capture-results.jsonl")
            .read_text(encoding="utf-8").splitlines()
        ]
        self.assertTrue(all(item["physical_return"]["cr3_sha256"] for item in events))

    def test_nonclipping_and_python_cleanup_failure_fail_closed(self):
        live = self.live_plan("invalid")
        result = self.run_candidate(
            live, 1, lambda root: self.capture_factory(root, invalid=True),
        )
        self.assertEqual(result["classification"], "invalid")
        self.assertEqual(result["attempted_capture_calls"], 1)

        live = self.live_plan("cleanup")
        root = self.prepare_candidate(live, 1)
        with self.assertRaisesRegex(RuntimeError, "single candidate failed"):
            measure.run_td_b_eq_r6_single_candidate(
                live,
                candidate_index=1,
                candidate_root=root,
                strip_zero_fn=self.passing_zero,
                ray_a_fn=self.passing_command,
                ray_c_fn=self.passing_command,
                capture_fn=self.capture_factory(root),
                python_cleanup_fn=lambda: {"status": "fail"},
                runtime_outer_pid=111,
                runtime_wrapper_pid=222,
                runtime_runner_pid=333,
                runtime_argv=["--eq-r6-single-candidate", "1"],
                sleep_fn=lambda _seconds: None,
                monotonic_fn=lambda: 0.0,
            )
        failure = json.loads((root / "candidate-result.json").read_text(encoding="utf-8"))
        self.assertEqual(failure["status"], "failed")

    def test_physical_sidecar_failure_is_retained_before_processing(self):
        live = self.live_plan()
        root = self.prepare_candidate(live, 1)

        def capture(request):
            result = self.capture_factory(root)(request)
            Path(result["remote_metadata_path"]).unlink()
            return result

        with self.assertRaisesRegex(RuntimeError, "single candidate failed"):
            measure.run_td_b_eq_r6_single_candidate(
                live,
                candidate_index=1,
                candidate_root=root,
                strip_zero_fn=self.passing_zero,
                ray_a_fn=self.passing_command,
                ray_c_fn=self.passing_command,
                capture_fn=capture,
                python_cleanup_fn=self.passing_cleanup,
                runtime_outer_pid=111,
                runtime_wrapper_pid=222,
                runtime_runner_pid=333,
                runtime_argv=["--eq-r6-single-candidate", "1"],
                sleep_fn=lambda _seconds: None,
                monotonic_fn=lambda: 0.0,
            )
        physical = [
            json.loads(line)
            for line in (root / "physical-returns.jsonl").read_text(encoding="utf-8").splitlines()
        ]
        self.assertEqual(len(physical), 1)
        self.assertIsNotNone(physical[0]["cr3_sha256"])
        self.assertEqual(physical[0]["sidecar_validation_status"], "fail")
        self.assertFalse((root / "capture-results.jsonl").exists())
        result = json.loads((root / "candidate-result.json").read_text(encoding="utf-8"))
        self.assertEqual(result["physical_returned_cr3_count"], 1)

    def test_eq_r6_full_raw_observations_select_exact_policy_order(self):
        policy_rows = [
            {
                "feature_id": feature_id,
                "value": float(index + 1),
                "metrics": {
                    "clipped_fraction": 0.0,
                    "near_noise_floor_fraction": 0.0,
                    "valid_pixel_count": 30_000 + index,
                },
            }
            for index, feature_id in enumerate(FEATURE_IDS)
        ]
        extras = [
            {
                "feature_id": f"diagnostic::{index:02d}",
                "value": -float(index + 1),
                "metrics": {
                    "clipped_fraction": 0.0,
                    "near_noise_floor_fraction": 0.0,
                    "valid_pixel_count": 1_000 + index,
                },
            }
            for index in range(34)
        ]
        observations = [
            *extras[:17],
            *reversed(policy_rows),
            *extras[17:],
        ]

        selected = measure._select_eq_r6_policy_observations(
            observations,
            FEATURE_IDS,
        )

        self.assertEqual(len(observations), 92)
        self.assertEqual(len(selected), 58)
        self.assertEqual(
            tuple(row["feature_id"] for row in selected),
            FEATURE_IDS,
        )
        source_by_id = {row["feature_id"]: row for row in observations}
        self.assertEqual(
            selected,
            tuple(source_by_id[feature_id] for feature_id in FEATURE_IDS),
        )
        self.assertEqual(selected[0]["feature_id"], "block_03::G1")

    def test_eq_r6_feature_selection_rejects_missing_required_id(self):
        observations = [
            {"feature_id": feature_id, "value": float(index)}
            for index, feature_id in enumerate(FEATURE_IDS[:-1])
        ]

        with self.assertRaisesRegex(ValueError, "missing required"):
            measure._select_eq_r6_policy_observations(
                observations,
                FEATURE_IDS,
            )

    def test_eq_r6_feature_selection_rejects_duplicate_observation_id(self):
        observations = [
            {"feature_id": feature_id, "value": float(index)}
            for index, feature_id in enumerate(FEATURE_IDS)
        ]
        observations.append(dict(observations[0]))

        with self.assertRaisesRegex(ValueError, "duplicate"):
            measure._select_eq_r6_policy_observations(
                observations,
                FEATURE_IDS,
            )

    def test_eq_r6_post_return_feature_failure_counts_physical_atomically(self):
        live = self.live_plan("post-return-feature-failure")
        root = self.prepare_candidate(live, 1)
        observer = {}

        def capture(request):
            returned = _attach_v2_capture_evidence(
                root,
                request,
                {},
                observed=float(request["requested_elapsed_s"]),
            )
            observer["callback"](request, returned, 1)
            raise RuntimeError("synthetic post-return feature failure")

        with self.assertRaisesRegex(RuntimeError, "single candidate failed"):
            measure.run_td_b_eq_r6_single_candidate(
                live,
                candidate_index=1,
                candidate_root=root,
                strip_zero_fn=self.passing_zero,
                ray_a_fn=self.passing_command,
                ray_c_fn=self.passing_command,
                capture_fn=capture,
                python_cleanup_fn=self.passing_cleanup,
                runtime_outer_pid=111,
                runtime_wrapper_pid=222,
                runtime_runner_pid=333,
                runtime_argv=["--eq-r6-single-candidate", "1"],
                bind_physical_return_observer_fn=lambda callback: observer.__setitem__(
                    "callback",
                    callback,
                ),
                sleep_fn=lambda _seconds: None,
                monotonic_fn=lambda: 0.0,
            )

        failure = json.loads(
            (root / "candidate-failure.json").read_text(encoding="utf-8")
        )
        result = json.loads(
            (root / "candidate-result.json").read_text(encoding="utf-8")
        )
        ledger = [
            json.loads(line)
            for line in (root / "physical-returns.jsonl")
            .read_text(encoding="utf-8")
            .splitlines()
            if line
        ]
        self.assertEqual(len(ledger), 1)
        self.assertEqual(failure["physical_returned"], 1)
        self.assertEqual(result["physical_returned_cr3_count"], 1)

        invalid_ledgers = {
            "broken-symlink": None,
            "malformed-json": ("{",),
            "noncontiguous-index": (
                json.dumps({"physical_index": 2, "capture_id": "capture-1"}),
            ),
            "duplicate-capture-id": (
                json.dumps({"physical_index": 1, "capture_id": "capture-1"}),
                json.dumps({"physical_index": 2, "capture_id": "capture-1"}),
            ),
        }
        for case_name, lines in invalid_ledgers.items():
            with self.subTest(strict_ledger=case_name):
                strict_root = self.parent / f"strict-{case_name}"
                strict_root.mkdir()
                strict_ledger = strict_root / "physical-returns.jsonl"
                if lines is None:
                    strict_ledger.symlink_to(strict_root / "missing-ledger")
                else:
                    strict_ledger.write_text(
                        "\n".join(lines) + "\n",
                        encoding="utf-8",
                    )
                with self.assertRaisesRegex(
                    ValueError,
                    "physical-return ledger",
                ):
                    measure._count_eq_r6_physical_returns(strict_root)

    def test_eq_r6_sidecar_failure_counts_physical_in_failure_and_result(self):
        live = self.live_plan("sidecar-accounting")
        root = self.prepare_candidate(live, 1)

        def capture(request):
            returned = self.capture_factory(root)(request)
            Path(returned["remote_metadata_path"]).unlink()
            return returned

        with self.assertRaisesRegex(RuntimeError, "single candidate failed"):
            measure.run_td_b_eq_r6_single_candidate(
                live,
                candidate_index=1,
                candidate_root=root,
                strip_zero_fn=self.passing_zero,
                ray_a_fn=self.passing_command,
                ray_c_fn=self.passing_command,
                capture_fn=capture,
                python_cleanup_fn=self.passing_cleanup,
                runtime_outer_pid=111,
                runtime_wrapper_pid=222,
                runtime_runner_pid=333,
                runtime_argv=["--eq-r6-single-candidate", "1"],
                sleep_fn=lambda _seconds: None,
                monotonic_fn=lambda: 0.0,
            )

        failure = json.loads(
            (root / "candidate-failure.json").read_text(encoding="utf-8")
        )
        result = json.loads(
            (root / "candidate-result.json").read_text(encoding="utf-8")
        )
        ledger = [
            json.loads(line)
            for line in (root / "physical-returns.jsonl")
            .read_text(encoding="utf-8")
            .splitlines()
            if line
        ]
        self.assertEqual(len(ledger), 1)
        self.assertEqual(ledger[0]["sidecar_validation_status"], "fail")
        self.assertEqual(failure["physical_returned"], 1)
        self.assertEqual(result["physical_returned_cr3_count"], 1)

    def test_eq_r6_pre_return_failure_keeps_all_physical_counts_zero(self):
        live = self.live_plan("pre-return-accounting")
        root = self.prepare_candidate(live, 1)

        with self.assertRaisesRegex(RuntimeError, "single candidate failed"):
            measure.run_td_b_eq_r6_single_candidate(
                live,
                candidate_index=1,
                candidate_root=root,
                strip_zero_fn=lambda: {
                    "status": "fail",
                    "generation_bearing_zero": False,
                },
                ray_a_fn=self.passing_command,
                ray_c_fn=self.passing_command,
                capture_fn=lambda _request: self.fail("capture must not run"),
                python_cleanup_fn=self.passing_cleanup,
                runtime_outer_pid=111,
                runtime_wrapper_pid=222,
                runtime_runner_pid=333,
                runtime_argv=["--eq-r6-single-candidate", "1"],
                sleep_fn=lambda _seconds: None,
                monotonic_fn=lambda: 0.0,
            )

        failure = json.loads(
            (root / "candidate-failure.json").read_text(encoding="utf-8")
        )
        result = json.loads(
            (root / "candidate-result.json").read_text(encoding="utf-8")
        )
        self.assertFalse((root / "physical-returns.jsonl").exists())
        self.assertEqual(failure["physical_returned"], 0)
        self.assertEqual(result["physical_returned_cr3_count"], 0)

    def fake_wrapper_run(self, live, behavior):
        def run(command, *, check):
            self.assertFalse(check)
            candidate_index = int(command[command.index("--eq-r6-single-candidate") + 1])
            outer_pid = int(command[command.index("--eq-r6-outer-pid") + 1])
            root = Path(command[2])
            expected_child_argv = measure._eq_r6_exact_child_argv(
                live,
                candidate_index=candidate_index,
                live_plan_path=Path(live["output_root"]) / "live-plan.json",
                outer_pid=outer_pid,
            )
            measure.write_td_b_eq_r6_launch_ledger(
                live,
                candidate_index=candidate_index,
                candidate_root=root,
                outer_pid=outer_pid,
                wrapper_pid=300 + candidate_index,
                runner_pid=400 + candidate_index,
                argv=expected_child_argv,
            )
            capture = behavior(candidate_index, root)
            measure.run_td_b_eq_r6_single_candidate(
                live,
                candidate_index=candidate_index,
                candidate_root=root,
                strip_zero_fn=self.passing_zero,
                ray_a_fn=self.passing_command,
                ray_c_fn=self.passing_command,
                capture_fn=capture,
                python_cleanup_fn=self.passing_cleanup,
                runtime_outer_pid=outer_pid,
                runtime_wrapper_pid=300 + candidate_index,
                runtime_runner_pid=400 + candidate_index,
                runtime_argv=expected_child_argv,
                sleep_fn=lambda _seconds: None,
                monotonic_fn=lambda: 0.0,
            )
            (root / "all-off-shell.json").write_text(
                json.dumps([{"ok": True}]) + "\n", encoding="utf-8",
            )
            measure._write_json(root / "wrapper-result.json", {
                "schema_version": 1,
                "experiment": "p7_thermal_diagnostics_v1",
                "status": "complete",
                "run_dir": str(root.resolve()),
                "wrapper_pid": 300 + candidate_index,
                "child_pid": 400 + candidate_index,
                "child_exit_code": 0,
                "shell_cleanup_exit_code": 0,
                "wrapper_exit_code": 0,
                "signal": None,
                "started_at": "2026-07-27T00:00:00Z",
            })
            return subprocess.CompletedProcess(command, 0)
        return run

    def test_outer_pass_does_not_launch_candidate_two(self):
        live = self.live_plan()
        result_path = measure.orchestrate_td_b_eq_r6(
            live,
            run_fn=self.fake_wrapper_run(
                live, lambda _index, root: self.capture_factory(root),
            ),
            final_zero_fn=self.passing_final_zero,
            outer_pid=111,
        )
        result = json.loads(result_path.read_text(encoding="utf-8"))
        self.assertEqual(result["status"], "qualified_1_2500")
        self.assertEqual(len(result["candidate_launches"]), 1)
        self.assertFalse((Path(live["output_root"]) / "candidate-2").exists())

    def test_outer_clipping_only_launches_candidate_two_after_first_seal(self):
        live = self.live_plan()

        def behavior(index, root):
            return self.capture_factory(root, clipped=index == 1)

        result_path = measure.orchestrate_td_b_eq_r6(
            live,
            run_fn=self.fake_wrapper_run(live, behavior),
            final_zero_fn=self.passing_final_zero,
            outer_pid=111,
        )
        result = json.loads(result_path.read_text(encoding="utf-8"))
        self.assertEqual(result["status"], "qualified_1_3200")
        self.assertEqual(len(result["candidate_launches"]), 2)
        first_seal = json.loads(
            (Path(live["output_root"]) / "candidate-1" / "terminal-seal.json")
            .read_text(encoding="utf-8")
        )
        self.assertGreaterEqual(
            result["candidate_launches"][1]["launched_at"],
            first_seal["sealed_at"],
        )

    def test_outer_nonclipping_and_terminal_failure_never_launch_candidate_two(self):
        live = self.live_plan("outer-invalid")
        result_path = measure.orchestrate_td_b_eq_r6(
            live,
            run_fn=self.fake_wrapper_run(
                live, lambda _index, root: self.capture_factory(root, invalid=True),
            ),
            final_zero_fn=self.passing_final_zero,
            outer_pid=111,
        )
        result = json.loads(result_path.read_text(encoding="utf-8"))
        self.assertEqual(result["status"], "run_invalid")
        self.assertEqual(len(result["candidate_launches"]), 1)

        live = self.live_plan("outer-zero-fail")
        with self.assertRaisesRegex(RuntimeError, "terminal lifecycle"):
            measure.orchestrate_td_b_eq_r6(
                live,
                run_fn=self.fake_wrapper_run(
                    live, lambda _index, root: self.capture_factory(root, clipped=True),
                ),
                final_zero_fn=lambda: {
                    "status": "fail",
                    "strip_verified_off": False,
                    "ray_verified_off": True,
                },
                outer_pid=111,
            )
        failure = json.loads(
            (Path(live["output_root"]) / "outer-failure.json").read_text(encoding="utf-8")
        )
        self.assertEqual(len(failure["candidate_launches"]), 1)

    def test_launch_ledger_is_immutable_and_rejects_private_argv(self):
        live = self.live_plan()
        root = self.prepare_candidate(live, 1)
        with self.assertRaises(FileExistsError):
            measure.write_td_b_eq_r6_launch_ledger(
                live,
                candidate_index=1,
                candidate_root=root,
                outer_pid=111,
                wrapper_pid=222,
                runner_pid=333,
                argv=["--eq-r6-single-candidate", "1"],
            )
        live = self.live_plan("private")
        Path(live["output_root"]).mkdir()
        with self.assertRaisesRegex(ValueError, "private parameter"):
            measure.write_td_b_eq_r6_launch_ledger(
                live,
                candidate_index=1,
                candidate_root=Path(live["output_root"]) / "candidate-1",
                outer_pid=111,
                wrapper_pid=222,
                runner_pid=333,
                argv=["--token", "fabricated"],
            )

    def test_launch_ledger_tamper_rejects_before_any_adapter(self):
        live = self.live_plan()
        root = self.prepare_candidate(live, 1)
        ledger_path = root / "launch-ledger.json"
        ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
        ledger["measurement_runner"]["sha256"] = "0" * 64
        ledger_path.chmod(0o600)
        ledger_path.write_text(json.dumps(ledger) + "\n", encoding="utf-8")
        calls = []
        with self.assertRaisesRegex(PermissionError, "binding differs"):
            measure.run_td_b_eq_r6_single_candidate(
                live,
                candidate_index=1,
                candidate_root=root,
                strip_zero_fn=lambda: calls.append("strip"),
                ray_a_fn=lambda: calls.append("a"),
                ray_c_fn=lambda: calls.append("c"),
                capture_fn=lambda _request: calls.append("capture"),
                python_cleanup_fn=lambda: calls.append("cleanup"),
                runtime_outer_pid=111,
                runtime_wrapper_pid=222,
                runtime_runner_pid=333,
                runtime_argv=["--eq-r6-single-candidate", "1"],
                sleep_fn=lambda _seconds: None,
            )
        self.assertEqual(calls, [])

    def test_runtime_binding_entry_rejects_each_pid_and_argv_drift(self):
        mutations = {
            "outer_pid": lambda value: value.__setitem__("outer_pid", 112),
            "wrapper_pid": lambda value: value.__setitem__("wrapper_pid", 223),
            "runner_pid": lambda value: value.__setitem__("runner_pid", 334),
            "argv_append": lambda value: value["argv"].append("--safe"),
            "argv_duplicate": lambda value: value["argv"].append(
                value["argv"][-1]
            ),
            "argv_remove": lambda value: value["argv"].pop(),
            "argv_reorder": lambda value: value["argv"].reverse(),
            "argv_replace": lambda value: value["argv"].__setitem__(1, "2"),
        }
        for index, (name, mutate) in enumerate(mutations.items(), start=1):
            with self.subTest(case=name):
                live = self.live_plan(f"entry-drift-{index}")
                root = self.prepare_candidate(live, 1)
                ledger_path = root / "launch-ledger.json"
                ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
                mutate(ledger)
                ledger_path.chmod(0o600)
                ledger_path.write_text(
                    json.dumps(ledger) + "\n",
                    encoding="utf-8",
                )
                calls = []
                with self.assertRaisesRegex(PermissionError, "binding differs"):
                    measure.run_td_b_eq_r6_single_candidate(
                        live,
                        candidate_index=1,
                        candidate_root=root,
                        strip_zero_fn=lambda: calls.append("strip"),
                        ray_a_fn=lambda: calls.append("a"),
                        ray_c_fn=lambda: calls.append("c"),
                        capture_fn=lambda _request: calls.append("capture"),
                        python_cleanup_fn=lambda: calls.append("cleanup"),
                        runtime_outer_pid=111,
                        runtime_wrapper_pid=222,
                        runtime_runner_pid=333,
                        runtime_argv=["--eq-r6-single-candidate", "1"],
                        sleep_fn=lambda _seconds: None,
                    )
                self.assertEqual(calls, [])

    def test_runtime_binding_seal_rejects_wrapper_child_root_and_candidate_drift(self):
        cases = (
            "wrapper_pid",
            "child_pid",
            "run_dir",
            "candidate_runner_pid",
        )
        for index, name in enumerate(cases, start=1):
            with self.subTest(case=name):
                live = self.live_plan(f"seal-drift-{index}")
                base_run = self.fake_wrapper_run(
                    live,
                    lambda _candidate, root: self.capture_factory(
                        root, clipped=True,
                    ),
                )

                def run(command, *, check, case=name):
                    completed = base_run(command, check=check)
                    root = Path(command[2])
                    if case == "candidate_runner_pid":
                        path = root / "candidate-result.json"
                        value = json.loads(path.read_text(encoding="utf-8"))
                        value["runtime_binding"]["runner_pid"] += 1
                    else:
                        path = root / "wrapper-result.json"
                        value = json.loads(path.read_text(encoding="utf-8"))
                        if case == "run_dir":
                            value[case] = str(root.parent / "safe-other")
                        else:
                            value[case] += 1
                    path.write_text(json.dumps(value) + "\n", encoding="utf-8")
                    return completed

                zero_calls = []
                with self.assertRaises(
                    (PermissionError, RuntimeError),
                ):
                    measure.orchestrate_td_b_eq_r6(
                        live,
                        run_fn=run,
                        final_zero_fn=lambda: (
                            zero_calls.append("zero")
                            or self.passing_final_zero()
                        ),
                        outer_pid=111,
                    )
                outer = Path(live["output_root"])
                self.assertEqual(zero_calls, ["zero"])
                self.assertFalse((outer / "candidate-2").exists())
                self.assertTrue((outer / "outer-failure.json").is_file())
                terminal = json.loads(
                    (outer / "candidate-1-outer-terminal.json").read_text(
                        encoding="utf-8"
                    )
                )
                self.assertEqual(terminal["status"], "fail")

    def test_exact_runtime_binding_passes_entry_and_terminal_seal(self):
        live = self.live_plan("binding-pass")
        result_path = measure.orchestrate_td_b_eq_r6(
            live,
            run_fn=self.fake_wrapper_run(
                live,
                lambda _index, root: self.capture_factory(root),
            ),
            final_zero_fn=self.passing_final_zero,
            outer_pid=111,
        )
        result = json.loads(result_path.read_text(encoding="utf-8"))
        seal = json.loads(
            (Path(live["output_root"]) / "candidate-1" / "terminal-seal.json")
            .read_text(encoding="utf-8")
        )
        self.assertEqual(result["status"], "qualified_1_2500")
        self.assertEqual(seal["status"], "pass")
        self.assertEqual(seal["runtime_binding"]["outer_pid"], 111)
        self.assertEqual(seal["runtime_binding"]["wrapper_pid"], 301)
        self.assertEqual(seal["runtime_binding"]["runner_pid"], 401)
        self.assertEqual(
            seal["runtime_binding"]["argv"],
            result["candidate_launches"][0]["child_argv"],
        )

    def test_outer_final_zero_and_failure_evidence_cover_all_exit_paths(self):
        cases = (
            ("run_runtime_error", "run_runtime_error", None, RuntimeError, "primary"),
            ("run_keyboard_interrupt", "run_keyboard_interrupt", None, KeyboardInterrupt, ""),
            ("run_system_exit", "run_system_exit", None, SystemExit, ""),
            ("subprocess_nonzero", "subprocess_nonzero", None, RuntimeError, ""),
            ("missing_wrapper_result", "missing_wrapper_result", None, ValueError, ""),
            ("malformed_wrapper_result", "malformed_wrapper_result", None, json.JSONDecodeError, ""),
            ("tampered_wrapper_pid", "tampered_wrapper_pid", None, PermissionError, ""),
            ("missing_candidate_result", "missing_candidate_result", None, ValueError, ""),
            ("tampered_launch_ledger", "tampered_launch_ledger", None, PermissionError, ""),
            ("seal_reference_failure", "seal_reference_failure", None, ValueError, ""),
            ("final_zero_runtime_error", "success", RuntimeError("zero"), RuntimeError, "zero"),
            ("final_zero_keyboard_interrupt", "success", KeyboardInterrupt(), KeyboardInterrupt, ""),
            (
                "primary_and_final_zero_failure",
                "run_runtime_error",
                RuntimeError("zero"),
                RuntimeError,
                "primary",
            ),
        )
        for index, (
            name,
            run_case,
            zero_exception,
            expected_type,
            expected_message,
        ) in enumerate(cases, start=1):
            with self.subTest(case=name):
                live = self.live_plan(f"outer-failure-{index}")
                base_run = self.fake_wrapper_run(
                    live,
                    lambda _candidate, root: self.capture_factory(root),
                )

                def run(command, *, check, case=run_case):
                    if case == "run_runtime_error":
                        raise RuntimeError("primary")
                    if case == "run_keyboard_interrupt":
                        raise KeyboardInterrupt()
                    if case == "run_system_exit":
                        raise SystemExit(7)
                    completed = base_run(command, check=check)
                    root = Path(command[2])
                    if case == "subprocess_nonzero":
                        return subprocess.CompletedProcess(command, 9)
                    if case == "missing_wrapper_result":
                        (root / "wrapper-result.json").unlink()
                    elif case == "malformed_wrapper_result":
                        (root / "wrapper-result.json").write_text(
                            "{",
                            encoding="utf-8",
                        )
                    elif case == "tampered_wrapper_pid":
                        path = root / "wrapper-result.json"
                        value = json.loads(path.read_text(encoding="utf-8"))
                        value["wrapper_pid"] += 1
                        path.write_text(
                            json.dumps(value) + "\n",
                            encoding="utf-8",
                        )
                    elif case == "missing_candidate_result":
                        (root / "candidate-result.json").unlink()
                    elif case == "tampered_launch_ledger":
                        path = root / "launch-ledger.json"
                        value = json.loads(path.read_text(encoding="utf-8"))
                        value["runner_pid"] += 1
                        path.chmod(0o600)
                        path.write_text(
                            json.dumps(value) + "\n",
                            encoding="utf-8",
                        )
                    elif case == "seal_reference_failure":
                        (root / "all-off-python.json").unlink()
                    return completed

                zero_calls = []

                def final_zero(exc=zero_exception):
                    zero_calls.append("zero")
                    if exc is not None:
                        raise exc
                    return self.passing_final_zero()

                caught = None
                try:
                    measure.orchestrate_td_b_eq_r6(
                        live,
                        run_fn=run,
                        final_zero_fn=final_zero,
                        outer_pid=111,
                    )
                except BaseException as exc:
                    caught = exc
                self.assertIsNotNone(caught)
                self.assertIsInstance(caught, expected_type)
                if name == "run_system_exit":
                    self.assertEqual(caught.code, 7)
                if expected_message:
                    self.assertIn(expected_message, str(caught))
                self.assertEqual(zero_calls, ["zero"])
                outer = Path(live["output_root"])
                self.assertFalse((outer / "outer-result.json").exists())
                self.assertFalse((outer / "candidate-2").exists())
                failure = json.loads(
                    (outer / "outer-failure.json").read_text(encoding="utf-8")
                )
                terminal = json.loads(
                    (outer / "candidate-1-outer-terminal.json").read_text(
                        encoding="utf-8"
                    )
                )
                self.assertEqual(failure["status"], "failed")
                self.assertEqual(failure["candidate_2_launch_count"], 0)
                self.assertTrue(terminal["launch_attempted"])
                self.assertTrue(terminal["final_zero_attempted"])
                self.assertEqual(terminal["status"], "fail")

    def test_shell_cleanup_artifact_failure_blocks_terminal_seal_and_candidate_two(self):
        live = self.live_plan()
        base_run = self.fake_wrapper_run(
            live, lambda _index, root: self.capture_factory(root, clipped=True),
        )

        def run(command, *, check):
            completed = base_run(command, check=check)
            root = Path(command[2])
            (root / "all-off-shell.json").write_text(
                json.dumps([{"ok": False}]) + "\n", encoding="utf-8",
            )
            return completed

        with self.assertRaisesRegex(RuntimeError, "terminal lifecycle"):
            measure.orchestrate_td_b_eq_r6(
                live,
                run_fn=run,
                final_zero_fn=self.passing_final_zero,
                outer_pid=111,
            )
        failure = json.loads(
            (Path(live["output_root"]) / "outer-failure.json").read_text(encoding="utf-8")
        )
        self.assertEqual(len(failure["candidate_launches"]), 1)

    def test_cli_modes_are_isolated_from_execute_dry_run_and_release(self):
        base = [
            "--experiment-id", thermal.TD_B,
            "--source", "ray",
            "--phase", "formal",
            "--run-name", "fake",
        ]
        parsed = measure.parse_args([
            *base, "--execute", "--allow-device-control", "--eq-r6-orchestrate",
        ])
        self.assertTrue(parsed.eq_r6_orchestrate)
        with self.assertRaises(PermissionError):
            measure.main([*base, "--dry-run", "--eq-r6-single-candidate", "1"])
        with self.assertRaises(PermissionError):
            measure.main([
                *base, "--qualify-lineage-release", "--eq-r6-orchestrate",
            ])


class EqR6PrelaunchOwnerTests(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory(
            dir="/Volumes/4T/temp/rgbww-optimizer",
        )
        self.parent = Path(self.tempdir.name)

    def tearDown(self):
        self.tempdir.cleanup()

    @staticmethod
    def passing_shell():
        return subprocess.CompletedProcess(
            ["zsh"],
            0,
            stdout=json.dumps([{"ok": True}]),
            stderr="",
        )

    @staticmethod
    def passing_zero():
        return {
            "status": "pass",
            "strip_verified_off": True,
            "ray_verified_off": True,
        }

    @staticmethod
    def passing_ray():
        return {"data": {"hue": 120, "sat": 50, "intensity": 0}}

    def dependencies(self, *, backend=None):
        test_case = self
        calls = {
            "factory": 0,
            "connect": 0,
            "resolve": 0,
            "shutters": 0,
            "capture": 0,
            "ray": 0,
            "python": 0,
            "shell": 0,
            "zero": 0,
            "dispatch": 0,
        }

        class Backend:
            backend_name = "remote"
            v2_capture_capability = measure.REMOTE_V2_CAPABILITY

            def connect(self):
                calls["connect"] += 1
                return object()

            def resolve_capture_settings(self, **kwargs):
                calls["resolve"] += 1
                test_case.assertEqual(
                    kwargs,
                    {"iso": None, "aperture": None, "image_format": "RAW"},
                )
                return SimpleNamespace(
                    iso="100",
                    aperture="8",
                    image_format="RAW",
                )

            def read_shutter_current_and_choices(self, _connection):
                calls["shutters"] += 1
                return "1/2500", ["1/2000", "1/2500", "1/3200"]

            def capture_with_timing(self, **_kwargs):
                calls["capture"] += 1
                raise AssertionError("prelaunch must not capture")

        selected_backend = backend or Backend()

        def factory():
            calls["factory"] += 1
            return selected_backend

        def ray():
            calls["ray"] += 1
            return self.passing_ray()

        def python_cleanup():
            calls["python"] += 1
            return {"status": "pass"}

        def shell_cleanup():
            calls["shell"] += 1
            return self.passing_shell()

        def zero():
            calls["zero"] += 1
            return self.passing_zero()

        return calls, {
            "backend_factory": factory,
            "ray_readiness_fn": ray,
            "python_cleanup_fn": python_cleanup,
            "shell_cleanup_fn": shell_cleanup,
            "final_zero_fn": zero,
        }

    def run_owner(self, name, **overrides):
        calls, dependencies = self.dependencies()
        dependencies.update(overrides)
        family = self.parent / name
        path = measure.run_td_b_eq_r6_prelaunch(
            family_root=family,
            code_checkpoint="a" * 40,
            checkpoint_validator=lambda _checkpoint: None,
            **dependencies,
        )
        return calls, family, path

    def test_positive_prelaunch_has_exact_order_modes_counts_and_no_dispatch(self):
        calls, family, manifest_path = self.run_owner("positive")
        prelaunch = family / "prelaunch"
        self.assertEqual(manifest_path, prelaunch / "prelaunch-manifest.json")
        self.assertEqual(
            calls,
            {
                "factory": 1,
                "connect": 1,
                "resolve": 1,
                "shutters": 1,
                "capture": 0,
                "ray": 1,
                "python": 1,
                "shell": 1,
                "zero": 1,
                "dispatch": 0,
            },
        )
        parsed = measure._eq_prelaunch_validate_root(prelaunch)
        self.assertEqual(
            list(parsed),
            list(measure.EQ_R6_PRELAUNCH_ARTIFACTS),
        )
        self.assertEqual(
            stat.S_IMODE(os.lstat(prelaunch).st_mode),
            0o700,
        )
        self.assertEqual(stat.S_IMODE(os.lstat(family).st_mode), 0o700)
        self.assertTrue(
            all(
                stat.S_IMODE(os.lstat(prelaunch / name).st_mode) == 0o600
                for name in measure.EQ_R6_PRELAUNCH_ARTIFACTS
            )
        )
        terminal = parsed["prelaunch-terminal.json"]
        self.assertEqual(terminal["status"], "pass")
        handoff = terminal["launch_handoff"]
        self.assertTrue(handoff["ready_for_dispatch"])
        self.assertEqual(
            (handoff["dispatch_count"], handoff["outer_launch_count"]),
            (0, 0),
        )
        self.assertFalse((family / "run").exists())
        expected = measure._eq_prelaunch_outer_argv(
            family=family,
            run_root=family / "run",
            code_checkpoint="a" * 40,
        )
        self.assertEqual(handoff["outer_argv"], expected)
        expected_hash = hashlib.sha256(
            json.dumps(
                expected,
                separators=(",", ":"),
                ensure_ascii=False,
                allow_nan=False,
            ).encode("utf-8")
        ).hexdigest()
        self.assertEqual(handoff["outer_argv_sha256"], expected_hash)

    def test_injected_prelaunch_never_reaches_real_dependency_owners(self):
        from camera_based_rgbww_optimizer.control import (
            all_off,
            camera_remote,
            esphome,
            ray120c,
        )

        calls, dependencies = self.dependencies()
        forbidden = AssertionError("real dependency owner was reached")
        with (
            patch.object(
                camera_remote,
                "create_camera_backend",
                side_effect=forbidden,
            ),
            patch.object(
                camera_remote,
                "load_remote_camera_config",
                side_effect=forbidden,
            ),
            patch.object(
                camera_remote.request,
                "urlopen",
                side_effect=forbidden,
            ),
            patch.object(ray120c, "get_hsi", side_effect=forbidden),
            patch.object(ray120c, "set_cct", side_effect=forbidden),
            patch.object(esphome, "verified_light", side_effect=forbidden),
            patch.object(all_off, "turn_everything_off", side_effect=forbidden),
        ):
            manifest = measure.run_td_b_eq_r6_prelaunch(
                family_root=self.parent / "forbidden-real-dependencies",
                code_checkpoint="a" * 40,
                checkpoint_validator=lambda _checkpoint: None,
                **dependencies,
            )
        self.assertTrue(manifest.is_file())
        self.assertEqual(
            (
                calls["factory"],
                calls["connect"],
                calls["resolve"],
                calls["shutters"],
                calls["ray"],
                calls["python"],
                calls["shell"],
                calls["zero"],
                calls["capture"],
                calls["dispatch"],
            ),
            (1, 1, 1, 1, 1, 1, 1, 1, 0, 0),
        )

    def test_readiness_negative_matrix_seals_failure_and_runs_all_cleanups(self):
        cases = (
            "factory_exception",
            "factory_keyboard",
            "factory_system_exit",
            "connect_exception",
            "connect_keyboard",
            "connect_system_exit",
            "backend_name",
            "capability",
            "settings_missing",
            "settings_malformed",
            "settings_nonraw",
            "capture_missing",
            "shutter_missing_2500",
            "shutter_missing_3200",
            "ray_exception",
            "ray_keyboard",
            "ray_system_exit",
            "ray_missing_data",
            "ray_malformed",
        )
        for index, case in enumerate(cases, start=1):
            with self.subTest(case=case):
                calls, dependencies = self.dependencies()
                base_factory = dependencies["backend_factory"]
                backend = base_factory()
                calls["factory"] = 0
                if case.startswith("factory_"):
                    exc = {
                        "factory_exception": RuntimeError("private-sentinel"),
                        "factory_keyboard": KeyboardInterrupt(),
                        "factory_system_exit": SystemExit(7),
                    }[case]

                    def factory(exc=exc):
                        calls["factory"] += 1
                        raise exc

                    dependencies["backend_factory"] = factory
                else:
                    if case.startswith("connect_"):
                        exc = {
                            "connect_exception": RuntimeError("private"),
                            "connect_keyboard": KeyboardInterrupt(),
                            "connect_system_exit": SystemExit(8),
                        }[case]
                        backend.connect = lambda exc=exc: (
                            calls.__setitem__("connect", calls["connect"] + 1)
                            or (_ for _ in ()).throw(exc)
                        )
                    elif case == "backend_name":
                        backend.backend_name = "local"
                    elif case == "capability":
                        backend.v2_capture_capability = "legacy"
                    elif case == "settings_missing":
                        backend.resolve_capture_settings = lambda **_kwargs: {}
                    elif case == "settings_malformed":
                        backend.resolve_capture_settings = lambda **_kwargs: "bad"
                    elif case == "settings_nonraw":
                        backend.resolve_capture_settings = lambda **_kwargs: {
                            "iso": "100",
                            "aperture": "8",
                            "image_format": "JPEG",
                        }
                    elif case == "capture_missing":
                        backend.capture_with_timing = None
                    elif case == "shutter_missing_2500":
                        backend.read_shutter_current_and_choices = (
                            lambda _connection: ("1/3200", ["1/3200"])
                        )
                    elif case == "shutter_missing_3200":
                        backend.read_shutter_current_and_choices = (
                            lambda _connection: ("1/2500", ["1/2500"])
                        )

                    def factory(backend=backend):
                        calls["factory"] += 1
                        return backend

                    dependencies["backend_factory"] = factory
                if case.startswith("ray_"):
                    if case == "ray_missing_data":
                        dependencies["ray_readiness_fn"] = (
                            lambda: calls.__setitem__("ray", calls["ray"] + 1)
                            or {}
                        )
                    elif case == "ray_malformed":
                        dependencies["ray_readiness_fn"] = (
                            lambda: calls.__setitem__("ray", calls["ray"] + 1)
                            or {"data": {"hue": "bad"}}
                        )
                    else:
                        exc = {
                            "ray_exception": RuntimeError("private"),
                            "ray_keyboard": KeyboardInterrupt(),
                            "ray_system_exit": SystemExit(9),
                        }[case]
                        dependencies["ray_readiness_fn"] = (
                            lambda exc=exc: calls.__setitem__(
                                "ray", calls["ray"] + 1
                            )
                            or (_ for _ in ()).throw(exc)
                        )
                family = self.parent / f"readiness-{index}"
                caught = None
                try:
                    measure.run_td_b_eq_r6_prelaunch(
                        family_root=family,
                        code_checkpoint="a" * 40,
                        checkpoint_validator=lambda _checkpoint: None,
                        **dependencies,
                    )
                except BaseException as exc:
                    caught = exc
                self.assertIsNotNone(caught)
                parsed = measure._eq_prelaunch_validate_root(
                    family / "prelaunch"
                )
                self.assertEqual(
                    parsed["prelaunch-terminal.json"]["status"],
                    "fail",
                )
                self.assertFalse(
                    parsed["prelaunch-terminal.json"]["launch_handoff"][
                        "ready_for_dispatch"
                    ]
                )
                self.assertEqual(
                    (calls["python"], calls["shell"], calls["zero"]),
                    (1, 1, 1),
                )
                self.assertEqual(calls["capture"], 0)
                self.assertFalse((family / "run").exists())
                if case.startswith(("factory_", "connect_")) or case in {
                    "backend_name",
                    "capability",
                    "settings_missing",
                    "settings_malformed",
                    "settings_nonraw",
                    "capture_missing",
                    "shutter_missing_2500",
                    "shutter_missing_3200",
                }:
                    self.assertEqual(calls["ray"], 0)

    def test_cleanup_and_final_zero_baseexception_matrix_is_all_path(self):
        cases = (
            "python_fail",
            "python_keyboard",
            "python_system_exit",
            "shell_nonzero",
            "shell_malformed",
            "shell_exception",
            "shell_keyboard",
            "shell_system_exit",
            "zero_generation",
            "zero_strip_nonzero",
            "zero_ray_nonzero",
            "zero_validate_failure",
            "zero_exception",
            "zero_keyboard",
            "zero_system_exit",
            "primary_python",
            "primary_shell",
            "primary_zero",
            "all_three",
        )
        for index, case in enumerate(cases, start=1):
            with self.subTest(case=case):
                calls, dependencies = self.dependencies()

                def python_result():
                    calls["python"] += 1
                    if case in {"python_keyboard"}:
                        raise KeyboardInterrupt()
                    if case in {"python_system_exit"}:
                        raise SystemExit(10)
                    if case in {"python_fail", "primary_python", "all_three"}:
                        return {"status": "fail"}
                    return {"status": "pass"}

                def shell_result():
                    calls["shell"] += 1
                    if case in {"shell_exception"}:
                        raise RuntimeError("private")
                    if case in {"shell_keyboard"}:
                        raise KeyboardInterrupt()
                    if case in {"shell_system_exit"}:
                        raise SystemExit(11)
                    if case in {"shell_malformed"}:
                        return subprocess.CompletedProcess(
                            ["zsh"], 0, stdout="{", stderr=""
                        )
                    if case in {"shell_nonzero", "primary_shell", "all_three"}:
                        return subprocess.CompletedProcess(
                            ["zsh"], 3, stdout="[]", stderr="private"
                        )
                    return self.passing_shell()

                def zero_result():
                    calls["zero"] += 1
                    if case == "zero_exception":
                        raise RuntimeError("private")
                    if case == "zero_keyboard":
                        raise KeyboardInterrupt()
                    if case == "zero_system_exit":
                        raise SystemExit(12)
                    if case in {
                        "zero_generation",
                        "zero_strip_nonzero",
                        "zero_ray_nonzero",
                        "zero_validate_failure",
                        "primary_zero",
                        "all_three",
                    }:
                        return {
                            "status": "fail",
                            "strip_verified_off": False,
                            "ray_verified_off": False,
                        }
                    return self.passing_zero()

                dependencies.update(
                    {
                        "python_cleanup_fn": python_result,
                        "shell_cleanup_fn": shell_result,
                        "final_zero_fn": zero_result,
                    }
                )
                if case.startswith("primary_"):
                    dependencies["ray_readiness_fn"] = lambda: (
                        calls.__setitem__("ray", calls["ray"] + 1)
                        or (_ for _ in ()).throw(RuntimeError("primary"))
                    )
                family = self.parent / f"cleanup-{index}"
                caught = None
                try:
                    measure.run_td_b_eq_r6_prelaunch(
                        family_root=family,
                        code_checkpoint="a" * 40,
                        checkpoint_validator=lambda _checkpoint: None,
                        **dependencies,
                    )
                except BaseException as exc:
                    caught = exc
                self.assertIsNotNone(caught)
                parsed = measure._eq_prelaunch_validate_root(
                    family / "prelaunch"
                )
                terminal = parsed["prelaunch-terminal.json"]
                self.assertEqual(terminal["status"], "fail")
                self.assertFalse(
                    terminal["launch_handoff"]["ready_for_dispatch"]
                )
                self.assertEqual(
                    (calls["python"], calls["shell"], calls["zero"]),
                    (1, 1, 1),
                )
                self.assertFalse((family / "run").exists())

    def test_root_atomic_and_manifest_validation_fail_closed_matrix(self):
        calls, dependencies = self.dependencies()
        root_cases = (
            "relative",
            "escape",
            "parent_symlink",
            "family",
            "prelaunch",
            "run",
        )
        for index, case in enumerate(root_cases, start=1):
            with self.subTest(case=case):
                base = self.parent / f"root-{index}"
                family = base / "family"
                if case == "relative":
                    family = Path("relative-family")
                elif case == "escape":
                    family = self.parent / "owner" / ".." / "escaped-family"
                elif case == "parent_symlink":
                    target = self.parent / f"target-{index}"
                    target.mkdir()
                    base.symlink_to(target, target_is_directory=True)
                    family = base / "family"
                elif case == "family":
                    family.mkdir(parents=True)
                elif case == "prelaunch":
                    (family / "prelaunch").mkdir(parents=True)
                elif case == "run":
                    (family / "run").mkdir(parents=True)
                before = dict(calls)
                with self.assertRaises(
                    (ValueError, PermissionError, FileExistsError)
                ):
                    measure.run_td_b_eq_r6_prelaunch(
                        family_root=family,
                        code_checkpoint="a" * 40,
                        checkpoint_validator=lambda _checkpoint: None,
                        **dependencies,
                    )
                self.assertEqual(calls, before)

        checkpoint_family = self.parent / "checkpoint-reject"
        before = dict(calls)
        with self.assertRaises(PermissionError):
            measure.run_td_b_eq_r6_prelaunch(
                family_root=checkpoint_family,
                code_checkpoint="a" * 40,
                checkpoint_validator=lambda _checkpoint: (
                    (_ for _ in ()).throw(PermissionError("checkpoint"))
                ),
                **dependencies,
            )
        self.assertFalse(checkpoint_family.exists())
        self.assertEqual(calls, before)

        calls, family, _manifest = self.run_owner("second")
        before = dict(calls)
        with self.assertRaises(FileExistsError):
            measure.run_td_b_eq_r6_prelaunch(
                family_root=family,
                code_checkpoint="a" * 40,
                checkpoint_validator=lambda _checkpoint: None,
                **self.dependencies()[1],
            )
        self.assertEqual(calls, before)

        writer_root = self.parent / "writer"
        writer_root.mkdir(mode=0o700)
        target = writer_root / "frozen-inputs.json"
        target.write_text("{}\n", encoding="utf-8")
        with self.assertRaises(FileExistsError):
            measure._eq_prelaunch_write_json(
                writer_root, "frozen-inputs.json", {}
            )
        target.unlink()
        outside = self.parent / "outside.json"
        target.symlink_to(outside)
        with self.assertRaises(FileExistsError):
            measure._eq_prelaunch_write_json(
                writer_root, "frozen-inputs.json", {}
            )

        calls, dependencies = self.dependencies()
        write_calls = []

        def failing_writer(root, name, value):
            write_calls.append(name)
            if name == "camera-readiness.json":
                raise OSError("injected atomic failure")
            return measure._eq_prelaunch_write_json(root, name, value)

        family = self.parent / "writer-failure"
        with self.assertRaises(OSError):
            measure.run_td_b_eq_r6_prelaunch(
                family_root=family,
                code_checkpoint="a" * 40,
                checkpoint_validator=lambda _checkpoint: None,
                write_artifact_fn=failing_writer,
                **dependencies,
            )
        self.assertFalse(
            (family / "prelaunch" / "prelaunch-manifest.json").exists()
        )
        self.assertEqual(
            write_calls,
            [
                "frozen-inputs.json",
                "offline-plan.json",
                "camera-readiness.json",
            ],
        )

        mutations = (
            "manifest_hash",
            "terminal_reference",
            "extra_json",
            "malformed",
            "nonfinite",
            "wrong_mode",
        )
        for index, mutation in enumerate(mutations, start=1):
            with self.subTest(mutation=mutation):
                _calls, family, _path = self.run_owner(
                    f"manifest-drift-{index}"
                )
                prelaunch = family / "prelaunch"
                if mutation == "manifest_hash":
                    path = prelaunch / "prelaunch-manifest.json"
                    value = json.loads(path.read_text(encoding="utf-8"))
                    value["canonical_artifacts"][0]["sha256"] = "0" * 64
                    path.write_text(
                        json.dumps(value, indent=2, sort_keys=True) + "\n",
                        encoding="utf-8",
                    )
                elif mutation == "terminal_reference":
                    path = prelaunch / "prelaunch-terminal.json"
                    value = json.loads(path.read_text(encoding="utf-8"))
                    value["canonical_artifacts"][0]["bytes"] += 1
                    path.write_text(
                        json.dumps(value, indent=2, sort_keys=True) + "\n",
                        encoding="utf-8",
                    )
                elif mutation == "extra_json":
                    (prelaunch / "extra.json").write_text(
                        "{}\n", encoding="utf-8"
                    )
                elif mutation == "malformed":
                    (prelaunch / "camera-readiness.json").write_text(
                        "{", encoding="utf-8"
                    )
                elif mutation == "nonfinite":
                    (prelaunch / "camera-readiness.json").write_text(
                        '{"value": NaN}\n', encoding="utf-8"
                    )
                elif mutation == "wrong_mode":
                    (prelaunch / "camera-readiness.json").chmod(0o644)
                with self.assertRaises(
                    (PermissionError, ValueError, json.JSONDecodeError)
                ):
                    measure._eq_prelaunch_validate_root(prelaunch)

    def test_cli_handoff_and_secret_absence_matrix(self):
        exact = [
            "--experiment-id",
            thermal.TD_B,
            "--source",
            "ray",
            "--phase",
            "formal",
            "--output-dir",
            str(self.parent / "cli-family"),
            "--run-name",
            "prelaunch",
            "--execute",
            "--allow-device-control",
            "--eq-r6-prelaunch",
            "--code-checkpoint",
            "a" * 40,
            "--human-authorization",
            thermal.TD_B_EQ_R6_EXPERIMENT_ID,
            "--camera-backend",
            "remote",
        ]
        calls = []

        def fake_owner(**kwargs):
            calls.append(kwargs)
            return self.parent / "fake-manifest.json"

        self.assertEqual(
            measure.main(exact, eq_prelaunch_fn=fake_owner),
            0,
        )
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0]["family_root"], self.parent / "cli-family")
        self.assertIsNone(calls[0]["backend_factory"])

        def without_pair(values, flag):
            index = values.index(flag)
            return values[:index] + values[index + 2 :]

        reject_cases = (
            exact[: exact.index("--execute")] + exact[exact.index("--execute") + 1 :],
            [value for value in exact if value != "--allow-device-control"],
            without_pair(exact, "--code-checkpoint"),
            without_pair(exact, "--human-authorization"),
            [
                "WRONG-AUTH" if value == thermal.TD_B_EQ_R6_EXPERIMENT_ID else value
                for value in exact
            ],
            [value if value != "ray" else "strip" for value in exact],
            [value if value != "formal" else "setup" for value in exact],
            [value if value != "prelaunch" else "other" for value in exact],
            [
                "relative-family"
                if value == str(self.parent / "cli-family")
                else value
                for value in exact
            ],
            exact[:-2] + ["--camera-backend", "local"],
            exact + ["--remote-base-url", "http://safe.invalid"],
            exact + ["--remote-env-file", str(self.parent / "fake.env")],
            exact + ["--remote-timeout", "9"],
            exact + ["--setup-release", str(self.parent / "release.json")],
            exact + ["--eq-r6-orchestrate"],
            exact + ["--unknown-prelaunch-state"],
        )
        for index, argv in enumerate(reject_cases, start=1):
            with self.subTest(cli_reject=index):
                before = len(calls)
                with self.assertRaises((PermissionError, SystemExit)):
                    measure.main(argv, eq_prelaunch_fn=fake_owner)
                self.assertEqual(len(calls), before)

        camera_token = "CAMERA_TOKEN_SENTINEL_C2"
        ray_private = "RAY_PRIVATE_SENTINEL_C2"
        shell_secret = "SHELL_SECRET_SENTINEL_C2"
        calls, dependencies = self.dependencies()

        def secret_factory():
            calls["factory"] += 1
            raise RuntimeError(camera_token)

        dependencies["backend_factory"] = secret_factory
        dependencies["shell_cleanup_fn"] = lambda: (
            calls.__setitem__("shell", calls["shell"] + 1)
            or subprocess.CompletedProcess(
                ["zsh"],
                2,
                stdout=json.dumps(
                    [{"ok": False, "authorization": shell_secret}]
                ),
                stderr=f"password={ray_private}",
            )
        )
        family = self.parent / "secret"
        with self.assertRaises(RuntimeError):
            measure.run_td_b_eq_r6_prelaunch(
                family_root=family,
                code_checkpoint="a" * 40,
                checkpoint_validator=lambda _checkpoint: None,
                forbidden_secret_values=(
                    camera_token,
                    ray_private,
                    shell_secret,
                ),
                **dependencies,
            )
        payload = b"".join(
            path.read_bytes()
            for path in (family / "prelaunch").iterdir()
            if path.is_file()
        )
        self.assertNotIn(camera_token.encode(), payload)
        self.assertNotIn(ray_private.encode(), payload)
        self.assertNotIn(shell_secret.encode(), payload)
        self.assertNotIn(b'"token"', payload.lower())
        self.assertNotIn(b'"secret"', payload.lower())
        self.assertNotIn(b'"password"', payload.lower())
        self.assertFalse((family / "run").exists())

        from camera_based_rgbww_optimizer.control import ray120c

        public = ray120c.OpenAPISettings.from_env({})
        self.assertEqual(public.secret, ray120c.DEFAULT_OPENAPI_SECRET)

        fake_completed = self.passing_shell()
        with patch.object(
            measure.subprocess,
            "run",
            return_value=fake_completed,
        ) as run:
            self.assertIs(
                measure._eq_prelaunch_default_shell_cleanup(),
                fake_completed,
            )
        command = run.call_args.args[0]
        self.assertIsInstance(command, list)
        self.assertEqual(command[:2], ["zsh", "-c"])
        self.assertIn("exec", command[2])
        self.assertEqual(run.call_args.kwargs["shell"], False)
        self.assertNotIn(camera_token, json.dumps(command))
        self.assertNotIn(ray_private, json.dumps(command))


class RayR6ContractTests(unittest.TestCase):
    def test_post_eq_formal_plan_is_still_non_executable_and_exact(self):
        plan = thermal.build_td_b_r6_formal_plan()
        self.assertFalse(plan["executable"])
        self.assertEqual(plan["status"], "selected_exposure_policy_non_executable")
        self.assertEqual(plan["capture_ids"], list(thermal.TD_B_R6_CAPTURE_IDS))
        self.assertEqual(plan["state_shutters"]["C"], "1/2500")
        self.assertEqual(plan["c_policy_status"], "qualified")
        self.assertEqual(
            (plan["formal_logical"], plan["formal_physical_cap"], plan["ambient"],
             plan["setup_in_formal_root"], plan["launch"], plan["retry"]),
            (16, 16, 0, 0, 1, 0),
        )

    def test_external_c_override_and_plan_drift_fail_closed(self):
        with self.assertRaisesRegex(ValueError, "cannot override"):
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
