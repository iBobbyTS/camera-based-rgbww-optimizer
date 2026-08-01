from __future__ import annotations

from dataclasses import FrozenInstanceError
import hashlib
import json
from pathlib import Path
import unittest
from unittest import mock

from camera_based_rgbww_optimizer.utils import p7_retained_r3_offline_patch_preflight as subject
from camera_based_rgbww_optimizer.utils import p7_retained_r3_provenance_io as provenance


SHA_A = "a" * 40
SHA_B = "b" * 40
EMPTY_SHA = hashlib.sha256(b"").hexdigest()
PATHS = ("src/owner.py", "tests/test_owner.py")


def row(prefix: str, value: object) -> bytes:
    return ("`" + prefix + json.dumps(value, separators=(",", ":")) + "`\n").encode()


def valid_inputs(required: dict | None = None) -> tuple[bytes, bytes]:
    required = required if required is not None else {"active": "R1", "enabled": True}
    plan = {"schema": "plan-v1", "required_full_machine_state": required}
    full = {"schema": "full-v1", "active": "R1", "enabled": True, "extra": 7}
    return row("PLAN_MACHINE_CONTRACT=", plan), row("FULL_PLAN_MACHINE_STATE=", full)


def spec(**changes) -> subject.CanonicalPatchDiagnosticSpec:
    values = dict(
        repo="/repo",
        parent_sha=SHA_A,
        child_sha=SHA_B,
        paths=PATHS,
        expected_exit_code=0,
        expected_stdout_bytes=3,
        expected_stdout_sha256=hashlib.sha256(b"out").hexdigest(),
        expected_stderr_bytes=0,
        expected_stderr_sha256=EMPTY_SHA,
    )
    values.update(changes)
    return subject.CanonicalPatchDiagnosticSpec(**values)


def ledger(item: subject.CanonicalPatchDiagnosticSpec, *, exit_code=0, stdout=b"out", stderr=b""):
    argv = (
        "git", "diff", "--binary", "--full-index", "--no-ext-diff",
        item.parent_sha, item.child_sha, "--", *item.paths,
    )
    return provenance.GitLedger(
        argv, item.repo, exit_code, stdout, stderr,
        hashlib.sha256(stdout).hexdigest(), hashlib.sha256(stderr).hexdigest(),
    )


class OfflinePatchPreflightTests(unittest.TestCase):
    def assert_code(self, code, function, *args, **kwargs):
        with self.assertRaises(subject.OfflinePatchPreflightError) as caught:
            function(*args, **kwargs)
        self.assertEqual(caught.exception.code, code)

    def run_valid(self, item=None, **ledger_changes):
        item = item or spec()
        runner = mock.Mock(return_value=ledger(item, **ledger_changes))
        plan, full = valid_inputs()
        result = subject.run_offline_patch_preflight(
            plan, full, item, dependencies={"run_git": runner}
        )
        return result, runner

    def test_exports_signatures_and_frozen_fields(self):
        self.assertEqual(subject.__all__, [
            "OfflinePatchPreflightError", "MachineRowPreflightResult",
            "CanonicalPatchDiagnosticSpec", "OfflinePatchPreflightResult",
            "run_offline_patch_preflight",
        ])
        item = spec()
        result, _runner = self.run_valid(item)
        for value in (item, result.machine_rows, result):
            with self.assertRaises((FrozenInstanceError, AttributeError, TypeError)):
                value.marker = True
        with self.assertRaises(TypeError):
            result.machine_rows.plan_contract["schema"] = "changed"

    def test_valid_plan_full_subset_and_exact_git_invocation(self):
        result, runner = self.run_valid()
        expected_argv = (
            "git", "diff", "--binary", "--full-index", "--no-ext-diff",
            SHA_A, SHA_B, "--", *PATHS,
        )
        runner.assert_called_once_with("/repo", expected_argv)
        self.assertEqual(result.observed_argv, expected_argv)
        self.assertEqual(result.classification, "CANONICAL_PATCH_EXACT_MATCH")
        self.assertEqual(result.machine_rows.required_full_state["active"], "R1")

    def test_embedded_backticks_are_payload_data_not_scanned(self):
        required = {"note": "left `inner` right"}
        plan = row("PLAN_MACHINE_CONTRACT=", {
            "schema": "plan-v1", "required_full_machine_state": required,
        })
        full = row("FULL_PLAN_MACHINE_STATE=", {"schema": "full-v1", **required})
        item = spec()
        runner = mock.Mock(return_value=ledger(item))
        result = subject.run_offline_patch_preflight(
            plan, full, item, dependencies={"run_git": runner}
        )
        self.assertEqual(result.machine_rows.required_full_state["note"], required["note"])
        runner.assert_called_once()

    def test_bytes_utf8_cr_and_row_count_fail_before_git(self):
        plan, full = valid_inputs()
        cases = (
            ("invalid_plan_bytes", "text", full),
            ("invalid_full_bytes", plan, bytearray(full)),
            ("machine_row_utf8_invalid", b"\xff", full),
            ("machine_row_cr_invalid", plan + b"\r\n", full),
            ("plan_row_count_invalid", b"plain\n", full),
            ("full_row_count_invalid", plan, full + full),
        )
        for code, candidate_plan, candidate_full in cases:
            with self.subTest(code=code):
                runner = mock.Mock()
                self.assert_code(
                    code, subject.run_offline_patch_preflight,
                    candidate_plan, candidate_full, spec(), dependencies={"run_git": runner},
                )
                runner.assert_not_called()

    def test_duplicate_nonfinite_and_malformed_json_fail_before_git(self):
        _plan, full = valid_inputs()
        candidates = (
            ("machine_row_duplicate_key", b'`PLAN_MACHINE_CONTRACT={"required_full_machine_state":{},"x":1,"x":2}`\n'),
            ("machine_row_nonfinite", b'`PLAN_MACHINE_CONTRACT={"required_full_machine_state":{},"x":NaN}`\n'),
            ("machine_row_json_invalid", b'`PLAN_MACHINE_CONTRACT={broken}`\n'),
        )
        for code, candidate in candidates:
            with self.subTest(code=code):
                runner = mock.Mock()
                self.assert_code(
                    code, subject.run_offline_patch_preflight,
                    candidate, full, spec(), dependencies={"run_git": runner},
                )
                runner.assert_not_called()

    def test_missing_or_mismatched_full_subset_is_type_exact_and_git_zero(self):
        cases = (
            ({"missing": 1}, {"schema": "full-v1"}, "required_full_subset_mismatch"),
            ({"value": 1}, {"schema": "full-v1", "value": True}, "required_full_subset_mismatch"),
            (None, {"schema": "full-v1"}, "required_full_state_invalid"),
        )
        for required, full_value, code in cases:
            with self.subTest(code=code):
                plan_value = {"schema": "plan-v1"}
                if required is not None:
                    plan_value["required_full_machine_state"] = required
                runner = mock.Mock()
                self.assert_code(
                    code, subject.run_offline_patch_preflight,
                    row("PLAN_MACHINE_CONTRACT=", plan_value),
                    row("FULL_PLAN_MACHINE_STATE=", full_value), spec(),
                    dependencies={"run_git": runner},
                )
                runner.assert_not_called()

    def test_spec_hash_expectation_and_argv_fail_closed(self):
        plan, full = valid_inputs()
        cases = (
            ("diagnostic_spec_invalid", object()),
            ("diagnostic_spec_invalid", spec(repo="relative")),
            ("patch_argv_invalid", spec(parent_sha="A" * 40)),
            ("patch_argv_invalid", spec(paths=("b", "a"))),
            ("patch_expectation_invalid", spec(expected_stdout_bytes=-1)),
            ("patch_expectation_invalid", spec(expected_stdout_sha256="0")),
        )
        for code, item in cases:
            with self.subTest(code=code):
                runner = mock.Mock()
                self.assert_code(
                    code, subject.run_offline_patch_preflight,
                    plan, full, item, dependencies={"run_git": runner},
                )
                runner.assert_not_called()

    def test_exact_match_and_output_mismatch_classifications(self):
        exact, exact_runner = self.run_valid()
        mismatch, mismatch_runner = self.run_valid(stdout=b"different")
        self.assertEqual(exact.classification, "CANONICAL_PATCH_EXACT_MATCH")
        self.assertEqual(mismatch.classification, "CANONICAL_PATCH_OUTPUT_MISMATCH")
        exact_runner.assert_called_once()
        mismatch_runner.assert_called_once()

    def test_git_failure_and_invalid_result_are_fail_closed(self):
        failed, runner = self.run_valid(exit_code=9, stderr=b"git failed")
        self.assertEqual(failed.classification, "CANONICAL_PATCH_GIT_FAILURE")
        runner.assert_called_once()
        plan, full = valid_inputs()
        invalid = mock.Mock(return_value=object())
        self.assert_code(
            "git_result_invalid", subject.run_offline_patch_preflight,
            plan, full, spec(), dependencies={"run_git": invalid},
        )
        invalid.assert_called_once()

    def test_report_is_canonical_and_owner_performs_no_io(self):
        result, runner = self.run_valid()
        self.assertEqual(
            result.report_bytes,
            provenance.canonical_json_bytes(json.loads(result.report_bytes)),
        )
        payload = json.loads(result.report_bytes)
        self.assertEqual(payload["diagnostic"]["classification"], result.classification)
        self.assertTrue(result.report_bytes.endswith(b"\n"))
        runner.assert_called_once()
        with mock.patch.object(Path, "write_bytes") as write_bytes, mock.patch.object(
            Path, "mkdir"
        ) as mkdir:
            self.run_valid()
        write_bytes.assert_not_called()
        mkdir.assert_not_called()


if __name__ == "__main__":
    unittest.main()
