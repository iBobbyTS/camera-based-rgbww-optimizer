from __future__ import annotations

import ast
from dataclasses import FrozenInstanceError, replace
import hashlib
import inspect
import unittest

from camera_based_rgbww_optimizer.utils import p7_retained_r3_controller_domain_template as subject
from camera_based_rgbww_optimizer.utils.p7_retained_r3_controller_conformance import analyze_controller_source
from camera_based_rgbww_optimizer.utils.p7_retained_r3_controller_preparation import prepare_controller_source
from camera_based_rgbww_optimizer.utils.p7_retained_r3_controller_runtime import compose_controller_source


def spec() -> subject.ControllerDomainTemplateSpec:
    repo = "/Users/ibobby/Projects/WLED-RGBWW"
    return subject.ControllerDomainTemplateSpec(
        reference_task_id="REF-P7-25-R2-B2-P6",
        contract_id="P7-TD-B-RETAINED-R3-OPTION-B-B2-P6-REPO-OWNED-DETERMINISTIC-DOMAIN-TEMPLATE-V1",
        activation_commit="94ad1c7bf7353480766418a2cffbbf3f581899be",
        activation_parent="4af057e0cd5f62d18a02cf02e088c1f293bddc4d",
        activation_subject="chore(plan): activate p6 domain template owner",
        activation_paths=(".agent-work/FULL_PLAN_REFERENCE.md", ".agent-work/PLAN.md", ".agent-work/PLANS/20260731-1549-p7-retained-r3-b2-p5-i1-domain-template-gap-review.md"),
        runtime_commit="37f7d0021c7a81a9d6680815bc51c305cf807a7b",
        runtime_parent="099d1ad833c3e73b7dc157f5786ad66bb6718f5e",
        runtime_source_blob_oid="075face6fd7453236affa303640b91eb16a42a9b",
        runtime_source_sha256="07eaeac615ea79db45afad91ce4c82e28c1cdcb66b6119b5cdca6462d7c091d2",
        runtime_test_blob_oid="a6aa7d7caf015e2eb858830dc89aaedaeb51aafa",
        runtime_test_sha256="66b1806f68f110280da519e2376de8de7d03ebe6c262af67d9ea589fd51d3782",
        source_path="/Volumes/4T/temp/rgbww-optimizer/p6/controller.py",
        output_root="/Volumes/4T/temp/rgbww-optimizer/p6/root",
        repo_root=repo, process_argv=(repo + "/.venv/bin/python", "-"),
    )


class ControllerDomainTemplateTests(unittest.TestCase):
    def test_01_identical_spec_builds_frozen_byte_exact_bundle(self):
        first = subject.build_controller_domain_template(spec())
        self.assertEqual(first, subject.build_controller_domain_template(spec()))
        self.assertEqual(first.template_sha256, hashlib.sha256(first.template_source).hexdigest())
        self.assertEqual(first.replacement_sha256, hashlib.sha256(first.replacement_statement).hexdigest())
        with self.assertRaises(FrozenInstanceError): first.expected_bound_results = 0

    def test_02_placeholder_replacement_is_unique_adjacent_and_canonical(self):
        bundle = subject.build_controller_domain_template(spec())
        prepared = prepare_controller_source(bundle.template_source, assignment_name="ACTIVATION_CONTRACT", validation_function="require_activation_contract", replacement_statement=bundle.replacement_statement)
        tree = ast.parse(prepared.source.decode("utf-8")); compile(tree, "<test>", "exec")
        assignments = [n for n in ast.walk(tree) if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "ACTIVATION_CONTRACT" for t in n.targets)]
        self.assertEqual(len(assignments), 1)
        self.assertEqual(prepared.source.count(b"ACTIVATION_CONTRACT ="), 1)
        self.assertTrue(bundle.replacement_statement.endswith(b"\n"))

    def test_03_runtime_request_inputs_are_exact_and_compose_without_effect(self):
        bundle = subject.build_controller_domain_template(spec()); request = bundle.runtime_request
        self.assertEqual((request.assignment_name, request.validation_function), ("ACTIVATION_CONTRACT", "require_activation_contract"))
        self.assertEqual(request.process_argv, (spec().repo_root + "/.venv/bin/python", "-"))
        composed = compose_controller_source(request)
        self.assertEqual(composed.source_sha256, hashlib.sha256(composed.source).hexdigest())

    def test_04_existing_analyzer_accepts_golden_eighteen_binding_report(self):
        report = analyze_controller_source(compose_controller_source(subject.build_controller_domain_template(spec()).runtime_request).source)
        self.assertEqual(report.bound_results, (
            ("activation_commit_ledger", "GitLedger"), ("activation_metadata_ledger", "GitLedger"), ("activation_paths_ledger", "GitLedger"),
            ("execution_result_admission_identity", "FileIdentity"), ("fixture_file", "FileIdentity"), ("fixture_root", "DirectoryIdentity"),
            ("fixture_span", "ByteSpan"), ("fixture_target", "SealTargetIdentity"), ("integration_qualification_identity", "FileIdentity"),
            ("root_identity", "DirectoryIdentity"), ("runtime_metadata_ledger", "GitLedger"), ("runtime_patch_ledger", "GitLedger"),
            ("runtime_paths_ledger", "GitLedger"), ("synthetic_full_identity", "FileIdentity"), ("synthetic_lineage_identity", "FileIdentity"),
            ("synthetic_plan_identity", "FileIdentity"), ("synthetic_seal_identity", "FileIdentity"), ("terminal_evidence_identity", "FileIdentity"),
        ))
        self.assertEqual((len(report.transport.effect_bindings), len(report.transport.fixture_bindings), len(report.root_reads)), (14, 4, 7))
        self.assertEqual(report.transport.effect_transport_uses, ())

    def test_05_single_physical_root_chain_and_seven_reads_have_exact_shape(self):
        report = analyze_controller_source(compose_controller_source(subject.build_controller_domain_template(spec()).runtime_request).source)
        self.assertEqual(report.transport.root_chain_compositions, (("root_chain", "root_identity", ("synthetic_plan_identity", "synthetic_full_identity", "synthetic_lineage_identity", "synthetic_seal_identity"), "root_identity"),))
        self.assertEqual(report.transport.root_chain_validations, (("root_chain", "validate_root_identity_chain"),))
        self.assertEqual({root for _name, root in report.root_reads}, {"root_identity"})

    def test_06_git6_matrix16_exact9_and_lifecycle_inventory_is_frozen(self):
        bundle = subject.build_controller_domain_template(spec()); tree = ast.parse(bundle.template_source.decode("utf-8"))
        calls = [n.func.id if isinstance(n.func, ast.Name) else n.func.attr for n in ast.walk(tree) if isinstance(n, ast.Call)]
        self.assertEqual(calls.count("run_read_only_git"), 6); self.assertEqual(calls.count("read_exact_file"), 7)
        self.assertEqual(calls.count("persist_canonical_json"), 9); self.assertEqual(calls.count("execute_controller_lifecycle"), 1)
        self.assertEqual(len(bundle.expected_artifact_names), 9); self.assertEqual(bundle.expected_lifecycle_order, ("conformance", "activation", "root", "inputs", "evaluate", "terminal", "terminal_seal", "admission"))
        matrix = next(n.value for n in ast.walk(tree) if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name) and n.targets[0].id == "semantic_matrix")
        self.assertEqual(len(matrix.elts), 16)

    def test_07_invalid_specs_and_literal_values_fail_closed_with_stable_codes(self):
        cases = (("reference_task_id", "wrong", "reference_task_mismatch"), ("activation_commit", "x", "activation_commit_invalid"), ("source_path", "relative", "source_path_invalid"), ("process_argv", ("python", "-"), "process_argv_mismatch"))
        for field, value, code in cases:
            with self.subTest(field=field), self.assertRaises(subject.ControllerDomainTemplateError) as raised:
                subject.build_controller_domain_template(replace(spec(), **{field: value}))
            self.assertEqual(raised.exception.code, code)
        with self.assertRaises(FrozenInstanceError): spec().repo_root = "/x"

    def test_08_static_owner_boundary_has_no_effect_retained_or_parallel_owner(self):
        self.assertEqual(subject.__all__, ["ControllerDomainTemplateError", "ControllerDomainTemplateSpec", "ControllerDomainTemplateBundle", "build_controller_domain_template"])
        source = inspect.getsource(subject); tree = ast.parse(source)
        calls = [n.func.id if isinstance(n.func, ast.Name) else n.func.attr for n in ast.walk(tree) if isinstance(n, ast.Call)]
        for forbidden in ("execute_controller_runtime", "analyze_controller_source", "compose_controller_source", "open", "run", "Popen"):
            self.assertNotIn(forbidden, calls)
        self.assertNotIn("retained", " ".join(n.value for n in ast.walk(tree) if isinstance(n, ast.Constant) and isinstance(n.value, str)).lower())


if __name__ == "__main__": unittest.main()
