from __future__ import annotations

import ast
from dataclasses import FrozenInstanceError, fields, replace
import hashlib
import inspect
from types import SimpleNamespace
import unittest

from camera_based_rgbww_optimizer.utils import p7_retained_r3_real_manifest_domain_template as subject
from camera_based_rgbww_optimizer.utils.p7_retained_r3_controller_conformance import (
    ControllerConformanceError,
    analyze_controller_source,
)
from camera_based_rgbww_optimizer.utils.p7_retained_r3_controller_runtime import (
    ControllerRuntimeRequest,
    compose_controller_source,
)
from camera_based_rgbww_optimizer.utils.p7_retained_r3_provenance_io import (
    DirectoryIdentity,
    FileIdentity,
    GitLedger,
    canonical_json_bytes,
)


SHA40 = "a" * 40
SHA64 = "b" * 64


def git_path(path: str, offset: int) -> subject.RealManifestGitPathIdentity:
    return subject.RealManifestGitPathIdentity(
        path, f"{offset:040x}", f"{offset + 1:040x}",
        f"{offset + 2:064x}", f"{offset + 3:064x}", f"{offset + 4:064x}",
    )


def input_identity(label: str, index: int) -> subject.RealManifestInputIdentity:
    root = f"/evidence/root-{index}"
    return subject.RealManifestInputIdentity(
        label, root + "/value.json", index + 1, f"{index + 20:064x}",
        index + 100, index + 200, 0o600,
        root, index + 100, index + 300, 0o700,
    )


def spec() -> subject.RealManifestDomainTemplateSpec:
    helper = "src/camera_based_rgbww_optimizer/utils/retained_r3_helper.py"
    test = "tests/test_retained_r3_helper.py"
    activation = subject.RealManifestCommitIdentity(
        "1" * 40, "2" * 40, "fix(p7): exact repair", (helper, test), "3" * 64,
    )
    baseline = subject.RealManifestBaselineIdentity(
        "4" * 40, "5" * 40, "6" * 40, helper, test,
        (git_path(helper, 7), git_path(test, 13)),
        "7" * 64, "8" * 64, "9" * 64, "a" * 64,
        "human_owned_local_lab", "retained_release_audit_prerequisite_v1_superseded_before_real_validation",
    )
    c1_labels = (
        "path_owner_index", "path_owner_index_seal",
        "terminal_evidence", "terminal_evidence_seal",
    )
    retained_labels = (
        "current_lineage_candidate", "resolved_formal_plan", "setup_lineage_release",
    )
    return subject.RealManifestDomainTemplateSpec(
        "REF-P7-25-R2-B2-M1-S1",
        "P7-TD-B-RETAINED-R3-OPTION-B-B2-M1-S1-REAL-MANIFEST-DOMAIN-TEMPLATE-SUCCESSOR-V1",
        activation, baseline,
        tuple(input_identity(label, index) for index, label in enumerate(c1_labels)),
        tuple(input_identity(label, index + 4) for index, label in enumerate(retained_labels)),
        "/controller/real-manifest.py", "/output/real-manifest", "/repo",
        ("/repo/.venv/bin/python", "-"),
    )


class RealManifestDomainTemplateTests(unittest.TestCase):
    def assert_code(self, code: str, value: object) -> None:
        with self.assertRaises(subject.RealManifestDomainTemplateError) as raised:
            subject.build_real_manifest_domain_template(value)  # type: ignore[arg-type]
        self.assertEqual(raised.exception.code, code)

    def test_01_exact_exports_fields_frozen_and_deep_tuple_contract(self):
        self.assertEqual(subject.__all__, [
            "RealManifestDomainTemplateError", "RealManifestGitPathIdentity",
            "RealManifestCommitIdentity", "RealManifestInputIdentity",
            "RealManifestBaselineIdentity", "RealManifestDomainTemplateSpec",
            "RealManifestDomainTemplateBundle", "build_real_manifest_domain_template",
        ])
        expected = {
            subject.RealManifestGitPathIdentity: ("repo_path", "before_blob_oid", "after_blob_oid", "before_sha256", "after_sha256", "binary_patch_sha256"),
            subject.RealManifestCommitIdentity: ("commit", "parent", "subject", "changed_paths", "full_patch_sha256"),
            subject.RealManifestInputIdentity: ("label", "path", "byte_count", "sha256", "device", "inode", "mode", "root_path", "root_device", "root_inode", "root_mode"),
            subject.RealManifestBaselineIdentity: ("release_checkpoint", "helper_v1", "integration", "helper_path", "test_path", "seam_chain", "governance_manifest_sha256", "guide_sha256", "advisor_decision_sha256", "advisor_attachment_sha256", "human_governance_override", "helper_disposition"),
            subject.RealManifestDomainTemplateSpec: ("reference_task_id", "contract_id", "activation", "baseline", "c1_inputs", "retained_inputs", "source_path", "output_root", "repo_root", "process_argv"),
            subject.RealManifestDomainTemplateBundle: ("template_source", "template_sha256", "replacement_statement", "replacement_sha256", "runtime_request", "expected_bound_results", "expected_artifact_names", "expected_lifecycle_order"),
        }
        for owner, names in expected.items():
            self.assertEqual(tuple(field.name for field in fields(owner)), names)
            self.assertTrue(owner.__dataclass_params__.frozen)
        self.assertIsInstance(spec().c1_inputs, tuple)
        self.assertIsInstance(spec().baseline.seam_chain, tuple)
        with self.assertRaises(FrozenInstanceError):
            spec().source_path = "/changed"

    def test_02_deterministic_strict_template_replacement_and_golden_hashes(self):
        first = subject.build_real_manifest_domain_template(spec())
        second = subject.build_real_manifest_domain_template(spec())
        self.assertEqual(first, second)
        self.assertEqual(first.template_sha256, hashlib.sha256(first.template_source).hexdigest())
        self.assertEqual(first.replacement_sha256, hashlib.sha256(first.replacement_statement).hexdigest())
        self.assertEqual(first.template_sha256, subject._CANONICAL_TEMPLATE_SHA256)
        self.assertEqual(first.replacement_sha256, subject._GOLDEN_REPLACEMENT_SHA256)
        text = first.template_source.decode("utf-8", errors="strict")
        self.assertIsNotNone(compile(ast.parse(text), "<golden-template>", "exec"))
        self.assertEqual(text.count("REAL_MANIFEST_CONTRACT ="), 1)
        self.assertEqual(text.count("require_real_manifest_contract(REAL_MANIFEST_CONTRACT)"), 1)

    def test_03_runtime_request_exact_binding_and_builder_has_no_effect(self):
        bundle = subject.build_real_manifest_domain_template(spec())
        self.assertIsInstance(bundle.runtime_request, ControllerRuntimeRequest)
        self.assertEqual(bundle.runtime_request.template_source, bundle.template_source)
        self.assertEqual(bundle.runtime_request.replacement_statement, bundle.replacement_statement)
        self.assertEqual(bundle.runtime_request.assignment_name, "REAL_MANIFEST_CONTRACT")
        self.assertEqual(bundle.runtime_request.validation_function, "require_real_manifest_contract")
        self.assertEqual(bundle.runtime_request.source_path, spec().source_path)
        self.assertEqual(bundle.runtime_request.process_argv, spec().process_argv)
        module_calls = {
            node.func.id if isinstance(node.func, ast.Name) else node.func.attr
            for node in ast.walk(ast.parse(inspect.getsource(subject))) if isinstance(node, ast.Call)
        }
        self.assertTrue({"open", "run", "Popen", "read_exact_file", "persist_canonical_json", "execute_controller_runtime"}.isdisjoint(module_calls))

    def test_04_invalid_spec_task_contract_and_literal_types_fail_closed(self):
        self.assert_code("invalid_spec", object())
        self.assert_code("reference_task_mismatch", replace(spec(), reference_task_id="wrong"))
        self.assert_code("contract_mismatch", replace(spec(), contract_id="wrong"))
        self.assert_code("process_argv_mismatch", replace(spec(), process_argv=("python", "-")))
        self.assert_code("source_path_invalid", replace(spec(), source_path="relative"))
        self.assert_code("repo_root_invalid", replace(spec(), repo_root="/repo/../repo"))

    def test_05_commit_blob_sha_path_byte_mode_and_root_identity_codes(self):
        self.assert_code("commit_identity_invalid", replace(spec(), activation=replace(spec().activation, commit="x")))
        bad_seam = replace(spec().baseline.seam_chain[0], before_blob_oid="x")
        self.assert_code("blob_oid_invalid", replace(spec(), baseline=replace(spec().baseline, seam_chain=(bad_seam, spec().baseline.seam_chain[1]))))
        bad_input = replace(spec().c1_inputs[0], sha256="x")
        self.assert_code("sha256_invalid", replace(spec(), c1_inputs=(bad_input,) + spec().c1_inputs[1:]))
        bad_input = replace(spec().c1_inputs[0], byte_count=0)
        self.assert_code("byte_count_invalid", replace(spec(), c1_inputs=(bad_input,) + spec().c1_inputs[1:]))
        bad_input = replace(spec().c1_inputs[0], mode=0o644)
        self.assert_code("mode_invalid", replace(spec(), c1_inputs=(bad_input,) + spec().c1_inputs[1:]))
        bad_input = replace(spec().c1_inputs[0], root_device=999)
        self.assert_code("input_identity_invalid", replace(spec(), c1_inputs=(bad_input,) + spec().c1_inputs[1:]))

    def test_06_activation_baseline_exact_typed_chain_and_no_generic_allowlist(self):
        bundle = subject.build_real_manifest_domain_template(spec())
        replacement = bundle.replacement_statement.decode("utf-8")
        for value in (spec().activation.commit, spec().activation.parent, spec().activation.full_patch_sha256, spec().baseline.release_checkpoint, spec().baseline.helper_v1, spec().baseline.integration):
            self.assertIn(value, replacement)
        for path in (spec().baseline.helper_path, spec().baseline.test_path):
            self.assertIn(path, replacement)
        self.assertNotIn("allowlist", inspect.getsource(subject).lower())
        self.assert_code("baseline_identity_invalid", replace(spec(), baseline=replace(spec().baseline, seam_chain=spec().baseline.seam_chain[:1])))

    def test_07_c1_exact_four_labels_order_children_uniqueness_and_hashes(self):
        bundle = subject.build_real_manifest_domain_template(spec())
        for identity in spec().c1_inputs:
            self.assertIn(identity.label, bundle.replacement_statement.decode())
            self.assertIn(identity.sha256, bundle.replacement_statement.decode())
        self.assert_code("c1_cardinality_mismatch", replace(spec(), c1_inputs=spec().c1_inputs[:3]))
        swapped = (spec().c1_inputs[1], spec().c1_inputs[0], *spec().c1_inputs[2:])
        self.assert_code("c1_label_mismatch", replace(spec(), c1_inputs=swapped))
        bad = replace(spec().c1_inputs[0], path="/elsewhere/value.json")
        self.assert_code("path_not_direct_child", replace(spec(), c1_inputs=(bad,) + spec().c1_inputs[1:]))
        collision = replace(spec().c1_inputs[0], label=spec().c1_inputs[1].label)
        self.assert_code("path_collision", replace(spec(), c1_inputs=(spec().c1_inputs[0], collision, *spec().c1_inputs[2:])))

    def test_08_retained_exact_three_labels_order_children_and_frozen_hashes(self):
        bundle = subject.build_real_manifest_domain_template(spec())
        for identity in spec().retained_inputs:
            self.assertIn(identity.label, bundle.replacement_statement.decode())
            self.assertIn(identity.sha256, bundle.replacement_statement.decode())
        self.assert_code("retained_cardinality_mismatch", replace(spec(), retained_inputs=spec().retained_inputs[:2]))
        swapped = (spec().retained_inputs[1], spec().retained_inputs[0], spec().retained_inputs[2])
        self.assert_code("retained_label_mismatch", replace(spec(), retained_inputs=swapped))

    def test_09_schema_status_exact_five_canonical_artifacts_and_no_authority_claim(self):
        bundle = subject.build_real_manifest_domain_template(spec())
        self.assertEqual(bundle.expected_artifact_names, (
            "retained-r3-audit-provenance-manifest-v2.json",
            "retained-r3-audit-provenance-manifest-v2.sha256.json",
            "terminal-evidence.json", "terminal-evidence.sha256.json",
            "execution-result-admission.json",
        ))
        text = compose_controller_source(bundle.runtime_request).source.decode()
        self.assertIn('"schema": "p7_retained_r3_audit_provenance_manifest_v2"', text)
        self.assertIn('"status": "sealed_subordinate_provenance_evidence"', text)
        self.assertNotIn("production_release_usable", text)
        self.assertNotIn("validator_pass", text)
        self.assertNotIn("device_authorized", text)

    def test_10_p3_owner_inventory_is_exact_seven_existing_one_created_git56_exit_code(self):
        source = compose_controller_source(subject.build_real_manifest_domain_template(spec()).runtime_request).source
        tree = ast.parse(source.decode())
        calls = [node.func.id if isinstance(node.func, ast.Name) else node.func.attr for node in ast.walk(tree) if isinstance(node, ast.Call)]
        self.assertEqual(calls.count("read_existing_root"), 7)
        self.assertEqual(calls.count("create_exclusive_root"), 1)
        self.assertEqual(calls.count("run_read_only_git"), 56)
        self.assertEqual(calls.count("persist_canonical_json"), 5)
        self.assertEqual(calls.count("read_exact_file"), 12)
        self.assertEqual(source.count(b".exit_code"), 56)
        self.assertNotIn(b".returncode", source)

    def test_11_p4_report_live_roots_reads_chain_and_effect_transport_are_exact(self):
        source = compose_controller_source(subject.build_real_manifest_domain_template(spec()).runtime_request).source
        report = analyze_controller_source(source)
        self.assertEqual(len(report.bound_results), 76)
        roots = [item for item in report.transport.effect_bindings if item[1] == "DirectoryIdentity"]
        self.assertEqual(len(roots), 8)
        self.assertEqual(len(report.root_reads), 12)
        self.assertEqual(len(report.transport.root_chain_compositions), 1)
        self.assertEqual(len(report.transport.root_chain_compositions[0][2]), 5)
        self.assertEqual(report.transport.effect_transport_uses, ())

    def test_12_lifecycle_order_primary_dominance_and_terminal_seal_blocking(self):
        self.assertEqual(subject.build_real_manifest_domain_template(spec()).expected_lifecycle_order, (
            "conformance", "activation", "root", "inputs", "evaluate",
            "terminal", "terminal_seal", "admission",
        ))
        source = compose_controller_source(subject.build_real_manifest_domain_template(spec()).runtime_request).source.decode()
        self.assertIn("retry=RETRY, fallback=FALLBACK", source)
        self.assertEqual(source.count("execute_controller_lifecycle("), 1)
        self.assertIn("if primary_failure is not None:\n            return seal", source)

    def test_13_generated_compile_fake_success_failure_and_negative_authority_surface(self):
        bundle = subject.build_real_manifest_domain_template(spec())
        source = compose_controller_source(bundle.runtime_request).source
        tree = ast.parse(source.decode("utf-8", errors="strict"))
        self.assertIsNotNone(compile(tree, "<generated>", "exec"))
        import_modules: set[str] = set()
        import_aliases: set[str] = set()
        call_tokens: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                import_modules.update(alias.name for alias in node.names)
                import_aliases.update(alias.asname or alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom):
                if node.module is not None:
                    import_modules.add(node.module)
                import_aliases.update(alias.asname or alias.name for alias in node.names)
            elif isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    call_tokens.add(node.func.id)
                elif isinstance(node.func, ast.Attribute):
                    call_tokens.add(node.func.attr)
        self.assertLessEqual(import_modules, {
            "sys",
            "camera_based_rgbww_optimizer.utils.p7_retained_r3_controller_conformance",
            "camera_based_rgbww_optimizer.utils.p7_retained_r3_provenance_io",
        })
        forbidden = {
            "canonical_validator", "emit_eligibility", "consume_release",
            "device_authorized", "camera", "ray120c", "socket", "requests",
        }
        self.assertTrue(forbidden.isdisjoint(import_modules | import_aliases | call_tokens))
        namespace: dict[str, object] = {"__name__": "fake_controller"}
        exec(source, namespace)
        stored: dict[str, FileIdentity] = {}
        root_counter = 0

        def existing(path: str) -> DirectoryIdentity:
            nonlocal root_counter
            root_counter += 1
            return DirectoryIdentity(path, 100 + root_counter, 200 + root_counter, 0o700)

        output_root = DirectoryIdentity(spec().output_root, 999, 1000, 0o700)
        def create(_path: str) -> DirectoryIdentity:
            return output_root
        def read(path: str, *, root: DirectoryIdentity, expected_size=None, expected_sha256=None, **_kwargs) -> FileIdentity:
            if path in stored:
                return stored[path]
            data = b"x" * int(expected_size or 1)
            return FileIdentity(path, data, len(data), expected_sha256 or hashlib.sha256(data).hexdigest(), root.device, root.inode + 10, 0o600, root)
        def persist(root: DirectoryIdentity, name: str, payload: object) -> FileIdentity:
            data = canonical_json_bytes(payload)
            value = FileIdentity(root.path + "/" + name, data, len(data), hashlib.sha256(data).hexdigest(), root.device, root.inode + len(stored) + 1, 0o600, output_root)
            stored[value.path] = value
            return value
        namespace.update(
            read_existing_root=existing,
            create_exclusive_root=create,
            read_exact_file=read,
            persist_canonical_json=persist,
            run_read_only_git=lambda *_args: GitLedger(("git",), "/repo", 0, b"", b"", SHA64, SHA64),
        )
        self.assertEqual(namespace["controller"]()["artifact_count"], 5)  # type: ignore[index,operator]
        current = spec()
        activation = current.activation
        baseline = current.baseline
        manifest_path = current.output_root + "/" + bundle.expected_artifact_names[0]
        self.assertEqual(stored[manifest_path].data, canonical_json_bytes({
            "schema": "p7_retained_r3_audit_provenance_manifest_v2",
            "status": "sealed_subordinate_provenance_evidence",
            "activation": [
                activation.commit, activation.parent, activation.subject,
                list(activation.changed_paths), activation.full_patch_sha256,
            ],
            "baseline": [
                baseline.release_checkpoint, baseline.helper_v1, baseline.integration,
                baseline.helper_path, baseline.test_path,
                [[
                    seam.repo_path, seam.before_blob_oid, seam.after_blob_oid,
                    seam.before_sha256, seam.after_sha256, seam.binary_patch_sha256,
                ] for seam in baseline.seam_chain],
                baseline.governance_manifest_sha256, baseline.guide_sha256,
                baseline.advisor_decision_sha256, baseline.advisor_attachment_sha256,
                baseline.human_governance_override, baseline.helper_disposition,
            ],
            "c1": [[
                item.label, item.path, item.root_path, item.byte_count, item.sha256,
                item.device, item.mode, item.inode, item.root_device,
                item.root_inode, item.root_mode,
            ] for item in current.c1_inputs],
            "retained": [[
                item.label, item.path, item.root_path, item.byte_count, item.sha256,
                item.device, item.mode, item.inode, item.root_device,
                item.root_inode, item.root_mode,
            ] for item in current.retained_inputs],
        }))
        primary = LookupError("input")
        namespace["read_existing_root"] = lambda _path: (_ for _ in ()).throw(primary)
        with self.assertRaises(LookupError) as raised:
            namespace["controller"]()  # type: ignore[index,operator]
        self.assertIs(raised.exception, primary)
        self.assertEqual(len([name for name in dir(self) if name.startswith("test_")]), 13)


if __name__ == "__main__":
    unittest.main()
