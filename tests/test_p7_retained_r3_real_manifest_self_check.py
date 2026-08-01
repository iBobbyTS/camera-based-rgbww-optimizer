from __future__ import annotations

from dataclasses import FrozenInstanceError, replace
import hashlib
import json
from pathlib import Path
from types import MappingProxyType, SimpleNamespace
import unittest
from unittest import mock

from camera_based_rgbww_optimizer.utils import p7_retained_r3_real_manifest_self_check as subject
from camera_based_rgbww_optimizer.utils.p7_retained_r3_provenance_io import (
    DirectoryIdentity,
    FileIdentity,
    GitLedger,
    canonical_json_bytes,
    decode_canonical_json,
)
from camera_based_rgbww_optimizer.utils.p7_retained_r3_real_manifest_domain_template import (
    RealManifestBaselineIdentity,
    RealManifestCommitIdentity,
    RealManifestGitPathIdentity,
    RealManifestInputIdentity,
)


COMMITS = tuple(character * 40 for character in "abcde")
FULL_PATCH = b"full patch\n"
SEAM_PATCHES = (b"helper seam\n", b"test seam\n")
ACTIVATION_PATHS = ("src/owner.py", "tests/test_owner.py")
SEAM_PATHS = ("src/seam.py", "tests/test_seam.py")


def blob(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\x00" + data).hexdigest()


def json_native(value):
    if isinstance(value, dict):
        return {key: json_native(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [json_native(item) for item in value]
    return value


def input_identity(label: str, index: int) -> RealManifestInputIdentity:
    data = f"input-{label}".encode()
    return RealManifestInputIdentity(
        label, f"/inputs/root/{label}.json", len(data), hashlib.sha256(data).hexdigest(),
        11, 100 + index, 0o600, "/inputs/root", 11, 50, 0o700,
    )


def fixture_spec() -> subject.RealManifestSelfCheckSpec:
    files = {
        (COMMITS[0], ACTIVATION_PATHS[0]): b"parent owner",
        (COMMITS[1], ACTIVATION_PATHS[0]): b"child owner",
        (COMMITS[0], ACTIVATION_PATHS[1]): b"parent test",
        (COMMITS[1], ACTIVATION_PATHS[1]): b"child test",
        (COMMITS[2], SEAM_PATHS[0]): b"release helper",
        (COMMITS[3], SEAM_PATHS[0]): b"v1 helper",
        (COMMITS[3], SEAM_PATHS[1]): b"v1 test",
        (COMMITS[4], SEAM_PATHS[1]): b"integration test",
    }
    seams = (
        RealManifestGitPathIdentity(
            SEAM_PATHS[0], blob(files[(COMMITS[2], SEAM_PATHS[0])]),
            blob(files[(COMMITS[3], SEAM_PATHS[0])]),
            hashlib.sha256(files[(COMMITS[2], SEAM_PATHS[0])]).hexdigest(),
            hashlib.sha256(files[(COMMITS[3], SEAM_PATHS[0])]).hexdigest(),
            hashlib.sha256(SEAM_PATCHES[0]).hexdigest(),
        ),
        RealManifestGitPathIdentity(
            SEAM_PATHS[1], blob(files[(COMMITS[3], SEAM_PATHS[1])]),
            blob(files[(COMMITS[4], SEAM_PATHS[1])]),
            hashlib.sha256(files[(COMMITS[3], SEAM_PATHS[1])]).hexdigest(),
            hashlib.sha256(files[(COMMITS[4], SEAM_PATHS[1])]).hexdigest(),
            hashlib.sha256(SEAM_PATCHES[1]).hexdigest(),
        ),
    )
    activation = RealManifestCommitIdentity(
        COMMITS[1], COMMITS[0], "feat(p7): fixture", ACTIVATION_PATHS,
        hashlib.sha256(FULL_PATCH).hexdigest(),
    )
    baseline = RealManifestBaselineIdentity(
        COMMITS[2], COMMITS[3], COMMITS[4], SEAM_PATHS[0], SEAM_PATHS[1], seams,
        "1" * 64, "2" * 64, "3" * 64, "4" * 64,
        "human override", "superseded before validation",
    )
    c1 = tuple(input_identity(label, index) for index, label in enumerate((
        "path_owner_index", "path_owner_index_seal",
        "terminal_evidence", "terminal_evidence_seal",
    )))
    retained = tuple(input_identity(label, index + 4) for index, label in enumerate((
        "current_lineage_candidate", "resolved_formal_plan", "setup_lineage_release",
    )))
    activation_row = (
        activation.commit, activation.parent, activation.subject,
        activation.changed_paths, activation.full_patch_sha256,
    )
    baseline_row = (
        baseline.release_checkpoint, baseline.helper_v1, baseline.integration,
        baseline.helper_path, baseline.test_path,
        tuple((item.repo_path, item.before_blob_oid, item.after_blob_oid,
               item.before_sha256, item.after_sha256, item.binary_patch_sha256)
              for item in baseline.seam_chain),
        baseline.governance_manifest_sha256, baseline.guide_sha256,
        baseline.lineage_owner_decision_evidence_sha256,
        baseline.advisor_attachment_sha256, baseline.human_governance_override,
        baseline.helper_disposition,
    )
    def row(item):
        return (item.label, item.path, item.root_path, item.byte_count, item.sha256,
                item.device, item.mode, item.inode, item.root_device,
                item.root_inode, item.root_mode)
    payloads = (
        {
            "schema": "p7_retained_r3_audit_provenance_manifest_v2",
            "status": "sealed_subordinate_provenance_evidence",
            "activation": json_native(activation_row),
            "baseline": json_native(baseline_row),
            "c1": [json_native(row(item)) for item in c1],
            "retained": [json_native(row(item)) for item in retained],
        },
        None,
        {"status": "sealed_subordinate_provenance_evidence"},
        None,
        {"admitted": True, "eligibility": False, "release_consumable": False},
    )
    root = DirectoryIdentity("/evidence/root", 71, 81, 0o700)
    names = (
        "retained-r3-audit-provenance-manifest-v2.json",
        "retained-r3-audit-provenance-manifest-v2.sha256.json",
        "terminal-evidence.json", "terminal-evidence.sha256.json",
        "execution-result-admission.json",
    )
    values = [canonical_json_bytes(payloads[0])]
    values.append(canonical_json_bytes({
        "bytes": len(values[0]), "sha256": hashlib.sha256(values[0]).hexdigest(),
        "target": names[0],
    }))
    values.append(canonical_json_bytes(payloads[2]))
    values.append(canonical_json_bytes({
        "bytes": len(values[2]), "sha256": hashlib.sha256(values[2]).hexdigest(),
        "target": names[2],
    }))
    values.append(canonical_json_bytes(payloads[4]))
    artifacts = tuple(
        FileIdentity(
            root.path + "/" + name, data, len(data), hashlib.sha256(data).hexdigest(),
            root.device, 200 + index, 0o600, root,
        )
        for index, (name, data) in enumerate(zip(names, values, strict=True))
    )
    git_files = tuple(
        subject.RealManifestGitFileBytes(commit, path, data)
        for (commit, path), data in sorted(files.items())
    )
    return subject.RealManifestSelfCheckSpec(
        "REF-FIXTURE", "CONTRACT-FIXTURE", "/repo", artifacts,
        activation, baseline, c1, retained, git_files,
    )


def fake_stdout(argv: tuple[str, ...], spec: subject.RealManifestSelfCheckSpec) -> bytes:
    file_map = {(item.commit, item.repo_path): item.data for item in spec.git_file_bytes}
    if argv[:3] == ("git", "rev-parse", "--verify"):
        return argv[3][:-9].encode() + b"\n"
    if argv[:4] == ("git", "show", "-s", "--format=%H%x00%P%x00%s"):
        return (spec.activation.commit.encode() + b"\x00" + spec.activation.parent.encode()
                + b"\x00" + spec.activation.subject.encode() + b"\n")
    if argv[:6] == ("git", "diff-tree", "--no-commit-id", "--name-only", "-r", "-z"):
        return b"\x00".join(path.encode() for path in spec.activation.changed_paths) + b"\x00"
    if argv[:2] == ("git", "rev-parse"):
        commit, path = argv[2].split(":", 1)
        return blob(file_map[(commit, path)]).encode() + b"\n"
    pair = argv[5:7]
    if pair == (spec.activation.parent, spec.activation.commit):
        return FULL_PATCH
    if pair == (spec.baseline.release_checkpoint, spec.baseline.helper_v1):
        return SEAM_PATCHES[0]
    return SEAM_PATCHES[1]


class Runner:
    def __init__(self, spec, mutate=None):
        self.spec = spec
        self.calls = []
        self.mutate = mutate

    def __call__(self, repo, argv):
        self.calls.append((repo, argv))
        value = GitLedger(
            argv, repo, 0, fake_stdout(argv, self.spec), b"",
            hashlib.sha256(fake_stdout(argv, self.spec)).hexdigest(),
            hashlib.sha256(b"").hexdigest(),
        )
        return self.mutate(value, len(self.calls)) if self.mutate else value


class RealManifestSelfCheckTests(unittest.TestCase):
    def assert_code(self, code, spec, runner=None):
        runner = runner or mock.Mock()
        with self.assertRaises(subject.RealManifestSelfCheckError) as caught:
            subject.run_real_manifest_self_check(
                spec, dependencies={"run_git": runner}
            )
        self.assertEqual(caught.exception.code, code)
        return runner

    def test_01_exports_and_all_public_dataclasses_are_frozen(self):
        self.assertEqual(subject.__all__, [
            "RealManifestSelfCheckError", "RealManifestGitFileBytes",
            "RealManifestSelfCheckSpec", "RealManifestSelfCheckReport",
            "required_real_manifest_git_argv", "run_real_manifest_self_check",
        ])
        spec = fixture_spec()
        runner = Runner(spec)
        report = subject.run_real_manifest_self_check(spec, dependencies={"run_git": runner})
        self.assertEqual(len(runner.calls), 18)
        self.assertEqual(len(report.git_ledger_facts), 18)
        for item in (spec.git_file_bytes[0], spec, report):
            with self.assertRaises((FrozenInstanceError, AttributeError, TypeError)):
                item.marker = True

    def test_02_golden_success_is_deterministic_and_subordinate_only(self):
        spec = fixture_spec()
        first = subject.run_real_manifest_self_check(spec, dependencies={"run_git": Runner(spec)})
        second = subject.run_real_manifest_self_check(spec, dependencies={"run_git": Runner(spec)})
        self.assertEqual(first, second)
        self.assertEqual(first.status, "real_manifest_self_check_pass")
        self.assertFalse(first.eligibility)
        self.assertFalse(first.release_consumable)
        self.assertEqual(first.authority, "subordinate_self_check_only")
        self.assertEqual(first.canonical_report_sha256, hashlib.sha256(first.canonical_report_bytes).hexdigest())
        decoded = json.loads(first.canonical_report_bytes)
        self.assertEqual(first.canonical_report_bytes, canonical_json_bytes(decoded))
        self.assertIsInstance(decoded, dict)
        frozen = decode_canonical_json(canonical_json_bytes({"rows": [1]}))
        self.assertIsInstance(frozen["rows"], tuple)
        self.assertTrue(subject._exact(frozen, {"rows": [1]}))
        self.assertTrue(subject._exact(MappingProxyType({"rows": (1,)}), {"rows": [1]}))
        self.assertFalse(subject._exact({"value": 1}, {"value": True}))

    def test_03_five_role_order_path_and_type_map_are_exact(self):
        spec = fixture_spec()
        for artifacts in (
            spec.artifacts[:4],
            (spec.artifacts[1], spec.artifacts[0], *spec.artifacts[2:]),
            (object(), *spec.artifacts[1:]),
        ):
            runner = self.assert_code(
                "artifact_contract_invalid" if len(artifacts) != 5 else
                "artifact_path_invalid" if type(artifacts[0]) is FileIdentity else
                "artifact_identity_invalid",
                replace(spec, artifacts=artifacts),
            )
            runner.assert_not_called()

    def test_04_canonical_duplicate_unknown_and_type_drift_fail_before_git(self):
        spec = fixture_spec()
        manifest = spec.artifacts[0]
        bad_values = (
            b'{"schema":"x","schema":"y"}\n',
            canonical_json_bytes({**json.loads(manifest.data), "unknown": 1}),
            canonical_json_bytes({**json.loads(manifest.data), "status": 1}),
            manifest.data[:-1] + b" \n",
        )
        for data in bad_values:
            with self.subTest(data=data[:20]):
                bad = replace(manifest, data=data, byte_count=len(data), sha256=hashlib.sha256(data).hexdigest())
                runner = self.assert_code(
                    "artifact_json_invalid" if data in (bad_values[0], bad_values[3]) else "manifest_contract_mismatch",
                    replace(spec, artifacts=(bad, *spec.artifacts[1:])),
                )
                runner.assert_not_called()

    def test_05_seal_terminal_and_admission_contracts_are_exact(self):
        spec = fixture_spec()
        cases = (
            (1, {"bytes": 1, "sha256": "0" * 64, "target": "wrong"}, "seal_contract_mismatch"),
            (2, {"status": "failed"}, "terminal_contract_mismatch"),
            (3, {"bytes": 1, "sha256": "0" * 64, "target": "wrong"}, "seal_contract_mismatch"),
            (4, {"admitted": 1, "eligibility": False, "release_consumable": False}, "admission_contract_mismatch"),
        )
        for index, payload, code in cases:
            with self.subTest(index=index):
                data = canonical_json_bytes(payload)
                artifact = replace(spec.artifacts[index], data=data, byte_count=len(data), sha256=hashlib.sha256(data).hexdigest())
                values = list(spec.artifacts)
                values[index] = artifact
                runner = self.assert_code(code, replace(spec, artifacts=tuple(values)))
                runner.assert_not_called()

    def test_06_root_mode_path_size_and_hash_drift_fail_before_git(self):
        spec = fixture_spec()
        item = spec.artifacts[0]
        other_root = replace(item.root, inode=item.root.inode + 1)
        cases = (
            (replace(item, root=other_root), "artifact_root_mismatch"),
            (replace(item, mode=0o644), "artifact_identity_invalid"),
            (replace(item, path="/evidence/root/wrong.json"), "artifact_path_invalid"),
            (replace(item, byte_count=item.byte_count + 1), "artifact_identity_invalid"),
            (replace(item, sha256="0" * 64), "artifact_identity_invalid"),
        )
        for changed, code in cases:
            values = (changed, *spec.artifacts[1:])
            runner = self.assert_code(code, replace(spec, artifacts=values))
            runner.assert_not_called()
        invalid_root = replace(item.root, path="relative", mode=0o755)
        values = tuple(replace(value, root=invalid_root) for value in spec.artifacts)
        runner = self.assert_code("artifact_root_mismatch", replace(spec, artifacts=values))
        runner.assert_not_called()
        alias = replace(spec.artifacts[1], inode=spec.artifacts[0].inode)
        runner = self.assert_code(
            "artifact_identity_invalid",
            replace(spec, artifacts=(spec.artifacts[0], alias, *spec.artifacts[2:])),
        )
        runner.assert_not_called()

    def test_07_required_git_argv_has_exact_allowlisted_order(self):
        spec = fixture_spec()
        argv = subject.required_real_manifest_git_argv(spec)
        self.assertEqual(len(argv), 18)
        self.assertEqual(argv[:5], tuple(
            ("git", "rev-parse", "--verify", commit + "^{commit}")
            for commit in (spec.activation.commit, spec.activation.parent,
                           spec.baseline.release_checkpoint, spec.baseline.helper_v1,
                           spec.baseline.integration)
        ))
        self.assertEqual(argv[5], ("git", "show", "-s", "--format=%H%x00%P%x00%s", spec.activation.commit))
        self.assertEqual(argv[6], ("git", "diff-tree", "--no-commit-id", "--name-only", "-r", "-z", spec.activation.commit))
        self.assertEqual(argv[-1], ("git", "diff", "--binary", "--full-index", "--no-ext-diff",
                                         spec.baseline.helper_v1, spec.baseline.integration, "--", spec.baseline.test_path))

    def test_08_git_exit_stderr_stdout_argv_and_cwd_mismatch_fail_closed(self):
        spec = fixture_spec()
        changes = (
            lambda value: replace(value, exit_code=1),
            lambda value: replace(value, stderr=b"bad", stderr_sha256=hashlib.sha256(b"bad").hexdigest()),
            lambda value: replace(value, stdout=b"bad", stdout_sha256=hashlib.sha256(b"bad").hexdigest()),
            lambda value: replace(value, argv=("git", "status")),
            lambda value: replace(value, cwd="/other"),
        )
        for index, change in enumerate(changes):
            runner = Runner(spec, lambda value, count, change=change: change(value) if count == 1 else value)
            self.assert_code(
                "git_command_failed" if index < 2 else "git_stdout_mismatch" if index == 2 else "git_ledger_invalid",
                spec, runner,
            )
            self.assertEqual(len(runner.calls), 1)
        def swap_tree(value, count):
            if count != 7:
                return value
            stdout = b"\x00".join(
                path.encode() for path in reversed(spec.activation.changed_paths)
            ) + b"\x00"
            return replace(
                value,
                stdout=stdout,
                stdout_sha256=hashlib.sha256(stdout).hexdigest(),
            )
        runner = Runner(spec, swap_tree)
        self.assert_code("git_stdout_mismatch", spec, runner)
        self.assertEqual(len(runner.calls), 7)

    def test_09_blob_bytes_sha_oid_and_seam_mismatch_are_pre_git(self):
        spec = fixture_spec()
        seam_index = next(
            index for index, item in enumerate(spec.git_file_bytes)
            if (item.commit, item.repo_path) == (COMMITS[2], SEAM_PATHS[0])
        )
        first = spec.git_file_bytes[seam_index]
        bad_data = replace(first, data=first.data + b"drift")
        files = list(spec.git_file_bytes)
        files[seam_index] = bad_data
        runner = self.assert_code(
            "seam_identity_mismatch",
            replace(spec, git_file_bytes=tuple(files)),
        )
        runner.assert_not_called()
        seam = replace(spec.baseline.seam_chain[0], before_blob_oid="0" * 40)
        baseline = replace(spec.baseline, seam_chain=(seam, spec.baseline.seam_chain[1]))
        with self.assertRaises(subject.RealManifestSelfCheckError) as caught:
            subject.required_real_manifest_git_argv(replace(spec, baseline=baseline))
        self.assertEqual(caught.exception.code, "seam_identity_mismatch")
        collision_seam = replace(
            spec.baseline.seam_chain[0], repo_path=spec.activation.changed_paths[0]
        )
        collision_baseline = replace(
            spec.baseline,
            release_checkpoint=spec.activation.parent,
            helper_path=spec.activation.changed_paths[0],
            seam_chain=(collision_seam, spec.baseline.seam_chain[1]),
        )
        with self.assertRaises(subject.RealManifestSelfCheckError) as caught:
            subject.required_real_manifest_git_argv(
                replace(spec, baseline=collision_baseline)
            )
        self.assertEqual(caught.exception.code, "git_file_set_collision")

    def test_10_generic_mapping_extra_ledger_and_dependency_shapes_reject(self):
        spec = fixture_spec()
        runner = mock.Mock()
        with self.assertRaises(subject.RealManifestSelfCheckError) as caught:
            subject.run_real_manifest_self_check(spec, dependencies={"run_git": runner, "extra": runner})
        self.assertEqual(caught.exception.code, "git_dependency_invalid")
        runner.assert_not_called()
        bad_runner = mock.Mock(return_value=(GitLedger, GitLedger))
        self.assert_code("git_ledger_invalid", spec, bad_runner)
        bad_runner.assert_called_once()

    def test_11_invalid_typed_spec_and_file_set_stop_before_any_git(self):
        spec = fixture_spec()
        cases = (
            (object(), "invalid_spec"),
            (replace(spec, repo_root="relative"), "repo_root_invalid"),
            (replace(spec, artifacts=list(spec.artifacts)), "artifact_contract_invalid"),
            (replace(spec, c1_inputs=spec.c1_inputs[:3]), "typed_identity_invalid"),
            (replace(spec, c1_inputs=tuple(reversed(spec.c1_inputs))), "typed_identity_invalid"),
            (replace(spec, retained_inputs=tuple(reversed(spec.retained_inputs))), "typed_identity_invalid"),
            (replace(spec, activation=replace(spec.activation, parent=spec.activation.commit)), "typed_identity_invalid"),
            (replace(spec, git_file_bytes=spec.git_file_bytes[:-1]), "git_file_set_mismatch"),
        )
        for candidate, code in cases:
            runner = self.assert_code(code, candidate)
            runner.assert_not_called()

    def test_12_canonical_report_is_deterministic_and_owner_has_no_io_authority(self):
        spec = fixture_spec()
        runner = Runner(spec)
        with mock.patch.object(Path, "write_bytes") as write_bytes, mock.patch.object(
            Path, "mkdir"
        ) as mkdir:
            report = subject.run_real_manifest_self_check(spec, dependencies={"run_git": runner})
        write_bytes.assert_not_called()
        mkdir.assert_not_called()
        payload = json.loads(report.canonical_report_bytes)
        self.assertEqual(payload["authority"], "subordinate_self_check_only")
        self.assertIs(payload["eligibility"], False)
        self.assertIs(payload["release_consumable"], False)
        self.assertEqual(report.canonical_report_bytes, canonical_json_bytes(payload))
        self.assertEqual(len(runner.calls), len(report.ordered_git_argv))
        self.assertEqual(len(payload["git"]["ledger_facts"]), 18)
        for ledger, fact in zip(runner.calls, payload["git"]["ledger_facts"], strict=True):
            repo, argv = ledger
            self.assertEqual(fact["argv"], list(argv))
            self.assertEqual(fact["cwd"], repo)
            self.assertEqual(fact["exit_code"], 0)
            self.assertEqual(fact["stderr_sha256"], hashlib.sha256(b"").hexdigest())
        self.assertEqual(
            report.git_ledger_facts,
            tuple(
                (
                    tuple(fact["argv"]), fact["cwd"], fact["exit_code"],
                    fact["stdout_sha256"], fact["stderr_sha256"],
                )
                for fact in payload["git"]["ledger_facts"]
            ),
        )


if __name__ == "__main__":
    unittest.main()
