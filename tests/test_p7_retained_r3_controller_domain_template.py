from __future__ import annotations

import ast
from dataclasses import FrozenInstanceError, replace
import hashlib
import inspect
import unittest

from camera_based_rgbww_optimizer.utils import p7_retained_r3_controller_domain_template as subject
from camera_based_rgbww_optimizer.utils.p7_retained_r3_controller_conformance import (
    analyze_controller_source,
    execute_controller_lifecycle,
)
from camera_based_rgbww_optimizer.utils.p7_retained_r3_controller_preparation import prepare_controller_source
from camera_based_rgbww_optimizer.utils.p7_retained_r3_provenance_io import (
    DirectoryIdentity,
    FileIdentity,
    GitLedger,
    canonical_json_bytes,
    decode_canonical_json,
)
from camera_based_rgbww_optimizer.utils.p7_retained_r3_controller_runtime import (
    ControllerRuntimeRequest,
    compose_controller_source,
)


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
        self.assertTrue(bundle.replacement_statement.startswith(b"ACTIVATION_CONTRACT ="))
        self.assertFalse(bundle.replacement_statement.startswith((b" ", b"\t")))
        self.assertTrue(bundle.replacement_statement.endswith(b"\n"))
        self.assertFalse(bundle.replacement_statement.endswith(b"\n\n"))

    def test_03_runtime_request_inputs_are_exact_and_compose_without_effect(self):
        bundle = subject.build_controller_domain_template(spec()); request = bundle.runtime_request
        self.assertEqual((request.assignment_name, request.validation_function), ("ACTIVATION_CONTRACT", "require_activation_contract"))
        self.assertEqual(request.process_argv, (spec().repo_root + "/.venv/bin/python", "-"))
        composed = compose_controller_source(request)
        self.assertEqual(composed.source_sha256, hashlib.sha256(composed.source).hexdigest())
        self.assertEqual(bundle.template_source.count(b"\x00"), 0)
        self.assertEqual(composed.source.count(b"\x00"), 0)
        self.assertIn(
            b'ACTIVATION_COMMIT + "\\x00" + ACTIVATION_PARENT + "\\x00" + ACTIVATION_SUBJECT',
            composed.source,
        )
        self.assertIn(b'"\\x00".join(ACTIVATION_PATHS) + "\\x00"', composed.source)
        self.assertIn(b'"\\x00".join(RUNTIME_PATHS) + "\\x00"', composed.source)

        activation_commit_boundary = b'activation_commit_ledger.stdout == (ACTIVATION_COMMIT + "\\n").encode("utf-8")'
        activation_metadata_boundary = b'activation_metadata_ledger.stdout == (ACTIVATION_COMMIT + "\\x00" + ACTIVATION_PARENT + "\\x00" + ACTIVATION_SUBJECT + "\\n").encode("utf-8")'
        runtime_metadata_boundary = b'runtime_metadata_ledger.stdout == (RUNTIME_COMMIT + "\\x00" + RUNTIME_PARENT + "\\x00feat(p7): own retained controller runtime\\n").encode("utf-8")'
        self.assertEqual(composed.source.count(activation_commit_boundary), 1)
        self.assertEqual(composed.source.count(activation_metadata_boundary), 1)
        self.assertEqual(composed.source.count(runtime_metadata_boundary), 1)

        generated_tree = ast.parse(composed.source.decode("utf-8", errors="strict"))
        compile(generated_tree, "<generated-newline-regression>", "exec")
        phase_assignments = {
            node.targets[0].slice.value: node.value
            for node in ast.walk(generated_tree)
            if isinstance(node, ast.Assign)
            and len(node.targets) == 1
            and isinstance(node.targets[0], ast.Subscript)
            and isinstance(node.targets[0].value, ast.Name)
            and node.targets[0].value.id == "phase_state"
            and isinstance(node.targets[0].slice, ast.Constant)
        }
        self.assertEqual(
            [node.value for node in ast.walk(phase_assignments["activation_commit"]) if isinstance(node, ast.Constant) and node.value == "\n"],
            ["\n"],
        )
        self.assertEqual(
            [node.value for node in ast.walk(phase_assignments["activation_metadata"]) if isinstance(node, ast.Constant) and node.value == "\n"],
            ["\n"],
        )
        self.assertEqual(
            [node.value for node in ast.walk(phase_assignments["runtime_metadata"]) if isinstance(node, ast.Constant) and isinstance(node.value, str) and node.value.endswith("\n")],
            ["\x00feat(p7): own retained controller runtime\n"],
        )

        commit_offset = composed.source.index(activation_commit_boundary)
        broken_commit = composed.source[:commit_offset] + activation_commit_boundary.replace(b'"\\n"', b'"\n"', 1) + composed.source[commit_offset + len(activation_commit_boundary):]
        with self.assertRaises(SyntaxError):
            ast.parse(broken_commit.decode("utf-8", errors="strict"))

        activation_offset = composed.source.index(activation_metadata_boundary)
        broken_activation = composed.source[:activation_offset] + activation_metadata_boundary.replace(b'"\\n"', b'"\n"', 1) + composed.source[activation_offset + len(activation_metadata_boundary):]
        with self.assertRaises(SyntaxError):
            ast.parse(broken_activation.decode("utf-8", errors="strict"))

        runtime_offset = composed.source.index(runtime_metadata_boundary)
        broken_runtime = composed.source[:runtime_offset] + runtime_metadata_boundary.replace(b' runtime\\n"', b' runtime\n"', 1) + composed.source[runtime_offset + len(runtime_metadata_boundary):]
        with self.assertRaises(SyntaxError):
            ast.parse(broken_runtime.decode("utf-8", errors="strict"))

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
        matrix_names = {
            "activation_commit", "activation_metadata", "activation_paths",
            "runtime_metadata", "runtime_paths", "runtime_patch", "plan_same_root",
            "full_same_root", "lineage_same_root", "seal_same_root",
            "qualification_nonempty", "terminal_nonempty", "admission_nonempty",
            "fixture_root_mode", "fixture_file_hash", "fixture_span_exact",
        }
        self.assertEqual({n.value for n in ast.walk(matrix) if isinstance(n, ast.Constant) and n.value in matrix_names}, matrix_names)

    def test_07_invalid_specs_and_literal_values_fail_closed_with_stable_codes(self):
        cases = (("reference_task_id", "wrong", "reference_task_mismatch"), ("activation_commit", "x", "activation_commit_invalid"), ("source_path", "relative", "source_path_invalid"), ("process_argv", ("python", "-"), "process_argv_mismatch"))
        for field, value, code in cases:
            with self.subTest(field=field), self.assertRaises(subject.ControllerDomainTemplateError) as raised:
                subject.build_controller_domain_template(replace(spec(), **{field: value}))
            self.assertEqual(raised.exception.code, code)
        with self.assertRaises(subject.ControllerDomainTemplateError) as raised:
            subject.build_controller_domain_template(replace(spec(), source_path=spec().source_path + "\x00"))
        self.assertEqual(raised.exception.code, "source_path_invalid")
        literal_escape_path = spec().source_path + "\\x00"
        literal_escape_bundle = subject.build_controller_domain_template(replace(spec(), source_path=literal_escape_path))
        self.assertEqual(literal_escape_bundle.runtime_request.source_path, literal_escape_path)
        with self.assertRaises(FrozenInstanceError): spec().repo_root = "/x"

    def test_08_static_owner_boundary_has_no_effect_retained_or_parallel_owner(self):
        self.assertEqual(subject.__all__, ["ControllerDomainTemplateError", "ControllerDomainTemplateSpec", "ControllerDomainTemplateBundle", "build_controller_domain_template"])
        def inventory(source_text, *, allowed_imports, allowed_calls, payload_fields=()):
            tree = ast.parse(source_text)
            imports = set()
            calls = set()
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    imports.update(alias.name for alias in node.names)
                elif isinstance(node, ast.ImportFrom):
                    imports.add(node.module or "")
                elif isinstance(node, ast.Call):
                    if isinstance(node.func, ast.Name):
                        calls.add(node.func.id)
                    elif isinstance(node.func, ast.Attribute):
                        calls.add(node.func.attr)
            forbidden_payload_fields = {
                "retained_artifacts", "candidate_payload", "eligibility",
                "release_payload", "device_payload",
            }
            return {
                *("unexpected_import:" + name for name in imports - set(allowed_imports)),
                *("unexpected_call:" + name for name in calls - set(allowed_calls)),
                *("forbidden_payload:" + name for name in set(payload_fields) & forbidden_payload_fields),
            }

        module_source = inspect.getsource(subject)
        module_tree = ast.parse(module_source)
        module_imports = {
            "__future__", "ast", "dataclasses", "hashlib", "pathlib", "re",
            "camera_based_rgbww_optimizer.utils.p7_retained_r3_controller_runtime",
        }
        module_calls = {
            node.func.id if isinstance(node.func, ast.Name) else node.func.attr
            for node in ast.walk(module_tree)
            if isinstance(node, ast.Call)
        }
        forbidden_module_calls = {
            "execute_controller_runtime", "analyze_controller_source", "compose_controller_source",
            "read_exact_file", "run_read_only_git", "persist_canonical_json",
            "validate_retained_artifacts", "validate_canonical_lineage", "emit_eligibility",
            "consume_release", "open", "run", "Popen", "socket", "urlopen",
        }
        self.assertEqual(inventory(module_source, allowed_imports=module_imports, allowed_calls=module_calls), set())
        self.assertTrue(forbidden_module_calls.isdisjoint(module_calls))

        public_payload_fields = {
            *subject.ControllerDomainTemplateSpec.__dataclass_fields__,
            *subject.ControllerDomainTemplateBundle.__dataclass_fields__,
            *ControllerRuntimeRequest.__dataclass_fields__,
        }
        self.assertTrue({"retained_artifacts", "candidate_payload", "eligibility", "release_payload", "device_payload"}.isdisjoint(public_payload_fields))

        generated = compose_controller_source(subject.build_controller_domain_template(spec()).runtime_request).source.decode("utf-8")
        generated_imports = {
            "sys",
            "camera_based_rgbww_optimizer.utils.p7_retained_r3_controller_conformance",
            "camera_based_rgbww_optimizer.utils.p7_retained_r3_controller_preparation",
            "camera_based_rgbww_optimizer.utils.p7_retained_r3_provenance_io",
        }
        generated_calls = {
            "ByteSpan", "DirectoryIdentity", "FileIdentity", "LifecycleCallbacks",
            "LifecycleRequirements", "PersistRootIdentity", "RootIdentityChain", "RuntimeError", "SealTargetIdentity",
            "_main", "all", "any", "canonical_json_bytes", "contract_value", "controller",
            "create_exclusive_root", "encode", "execute_controller_lifecycle", "len",
            "persist_canonical_json", "read_exact_file", "require_activation_contract",
            "run_read_only_git", "join", "startswith", "tuple", "type",
            "validate_root_identity_chain", "write",
        }
        self.assertEqual(inventory(generated, allowed_imports=generated_imports, allowed_calls=generated_calls), set())
        generated_tree = ast.parse(generated)
        generated_call_names = [
            node.func.id if isinstance(node.func, ast.Name) else node.func.attr
            for node in ast.walk(generated_tree)
            if isinstance(node, ast.Call)
        ]
        self.assertEqual(generated_call_names.count("any"), 1)
        self.assertEqual(generated_call_names.count("join"), 2)
        self.assertEqual(generated.count("any(type(item) is not tuple or len(item) != 2 or type(item[0]) is not str for item in value)"), 1)
        self.assertEqual(generated.count('"\\x00".join(ACTIVATION_PATHS)'), 1)
        self.assertEqual(generated.count('"\\x00".join(RUNTIME_PATHS)'), 1)

        self.assertIn("retained", subject.__doc__.lower())
        self.assertIn(
            "unexpected_import:camera_based_rgbww_optimizer.utils.p7_retained_r3_canonical_validator",
            inventory(
                "from camera_based_rgbww_optimizer.utils.p7_retained_r3_canonical_validator import validate\n",
                allowed_imports=generated_imports,
                allowed_calls=generated_calls,
            ),
        )
        self.assertIn(
            "unexpected_call:emit_eligibility",
            inventory("emit_eligibility()\n", allowed_imports=set(), allowed_calls=set()),
        )
        self.assertIn(
            "forbidden_payload:retained_artifacts",
            inventory("value = 1\n", allowed_imports=set(), allowed_calls=set(), payload_fields={"retained_artifacts"}),
        )
        self.assertIn(
            "unexpected_call:analyze_controller_source",
            inventory(generated + "\nanalyze_controller_source(b'x')\n", allowed_imports=generated_imports, allowed_calls=generated_calls),
        )

    def test_09_composed_runtime_names_bind_and_guarded_entrypoint_calls_controller_once(self):
        source = compose_controller_source(subject.build_controller_domain_template(spec()).runtime_request).source
        tree = ast.parse(source.decode("utf-8")); compile(tree, "<generated>", "exec")
        namespace = {"__name__": "import_only"}
        exec(compile(tree, "<generated>", "exec"), namespace)
        self.assertTrue(callable(namespace["controller"]))
        bindings = {
            target.id
            for node in ast.walk(tree)
            if isinstance(node, ast.Assign)
            for target in node.targets
            if isinstance(target, ast.Name)
        }
        self.assertTrue({"REPO_ROOT", "ACTIVATION_COMMIT", "RUNTIME_COMMIT", "RUNTIME_PARENT", "RUNTIME_PATHS", "OUTPUT_ROOT"}.issubset(bindings))
        controller_calls = [node for node in ast.walk(tree) if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "controller"]
        self.assertEqual(len(controller_calls), 1)
        guard = next(node for node in tree.body if isinstance(node, ast.If))
        self.assertEqual(ast.unparse(guard.test), "__name__ == '__main__'")
        self.assertEqual(len(guard.body), 1)

    def _fake_owner_harness(self, *, fail_root=False):
        bundle = subject.build_controller_domain_template(spec())
        source = compose_controller_source(bundle.runtime_request).source
        namespace = {"__name__": "import_only"}
        exec(compile(source, "<generated>", "exec"), namespace)
        calls = []
        lifecycle_orders = []
        files = {}
        persisted_values = {}
        root_identity = DirectoryIdentity(path=spec().output_root, device=17, inode=23, mode=0o700)
        sentinel = RuntimeError("pre_root_failure")

        def git_stdout(argv):
            if argv[:3] == ("git", "rev-parse", "--verify"):
                return (spec().activation_commit + "\n").encode("utf-8")
            if argv[:4] == ("git", "show", "-s", "--format=%H%x00%P%x00%s"):
                if argv[4] == spec().activation_commit:
                    return (spec().activation_commit + "\x00" + spec().activation_parent + "\x00" + spec().activation_subject + "\n").encode("utf-8")
                return (spec().runtime_commit + "\x00" + spec().runtime_parent + "\x00feat(p7): own retained controller runtime\n").encode("utf-8")
            if argv[:6] == ("git", "diff-tree", "--no-commit-id", "--name-only", "-r", "-z"):
                paths = spec().activation_paths if argv[6] == spec().activation_commit else (
                    "src/camera_based_rgbww_optimizer/utils/p7_retained_r3_controller_runtime.py",
                    "tests/test_p7_retained_r3_controller_runtime.py",
                )
                return ("\x00".join(paths) + "\x00").encode("utf-8")
            return b"diff --git a/runtime.py b/runtime.py\n"

        def fake_git(repo, argv):
            self.assertEqual(repo, spec().repo_root)
            calls.append(("git", argv))
            stdout = git_stdout(argv)
            return GitLedger(argv=argv, cwd=repo, exit_code=0, stdout=stdout, stderr=b"", stdout_sha256=hashlib.sha256(stdout).hexdigest(), stderr_sha256=hashlib.sha256(b"").hexdigest())

        def fake_create(path):
            self.assertEqual(path, spec().output_root)
            calls.append(("root", path))
            if fail_root:
                raise sentinel
            return root_identity

        def fake_persist(root, child_name, value):
            self.assertEqual(root, root_identity)
            calls.append(("persist", child_name, root))
            payload = canonical_json_bytes(value)
            identity = FileIdentity(path=root.path + "/" + child_name, data=payload, byte_count=len(payload), sha256=hashlib.sha256(payload).hexdigest(), device=root.device, inode=100 + len(files), mode=0o600, root=root)
            self.assertNotIn(identity.path, files)
            files[identity.path] = identity
            persisted_values[child_name] = value
            return identity

        def fake_read(path, *, root):
            self.assertIs(root, root_identity)
            calls.append(("read", path.rsplit("/", 1)[-1], root))
            return files[path]

        def tracked_lifecycle(callbacks, requirements):
            result = execute_controller_lifecycle(callbacks, requirements)
            lifecycle_orders.append(result.order)
            return result

        class Buffer:
            def __init__(self): self.data = b""
            def write(self, payload): self.data += payload; return len(payload)
        class Stdout:
            def __init__(self): self.buffer = Buffer()
        class Sys:
            def __init__(self): self.stdout = Stdout()

        fake_sys = Sys()
        namespace.update(
            run_read_only_git=fake_git,
            create_exclusive_root=fake_create,
            persist_canonical_json=fake_persist,
            read_exact_file=fake_read,
            execute_controller_lifecycle=tracked_lifecycle,
            sys=fake_sys,
        )
        return namespace, calls, lifecycle_orders, fake_sys, sentinel, persisted_values

    def test_10_in_memory_owner_harness_proves_persist_read_order_and_success_envelope(self):
        namespace, calls, lifecycle_orders, fake_sys, _sentinel, persisted_values = self._fake_owner_harness()
        self.assertEqual(calls, [])
        namespace["_main"]()
        self.assertEqual(lifecycle_orders, [("conformance", "activation", "root", "inputs", "evaluate", "terminal", "terminal_seal", "admission")])
        self.assertEqual(fake_sys.stdout.buffer.data, canonical_json_bytes({"artifact_count": 9, "status": "repo_owned_runnable_domain_template_candidate_waiting_for_planner_review"}))
        self.assertEqual([entry[0] for entry in calls[:7]], ["git"] * 6 + ["root"])
        persisted = [entry[1] for entry in calls if entry[0] == "persist"]
        read = [entry[1] for entry in calls if entry[0] == "read"]
        self.assertEqual(persisted, list(subject.build_controller_domain_template(spec()).expected_artifact_names))
        self.assertEqual(read, ["synthetic-plan.json", "synthetic-full.json", "synthetic-lineage.json", "synthetic-seal.json", "integration-qualification.json", "terminal-evidence.json", "execution-result-admission.json"])
        for name in read:
            self.assertLess(next(index for index, entry in enumerate(calls) if entry[:2] == ("persist", name)), next(index for index, entry in enumerate(calls) if entry[:2] == ("read", name)))
        self.assertTrue(all(entry[-1].path == spec().output_root for entry in calls if entry[0] in {"persist", "read"}))
        expected_matrix = [
            [name, True]
            for name in (
                "activation_commit", "activation_metadata", "activation_paths",
                "runtime_metadata", "runtime_paths", "runtime_patch",
                "plan_same_root", "full_same_root", "lineage_same_root",
                "seal_same_root", "fixture_root_mode", "fixture_file_hash",
                "fixture_span_exact", "qualification_nonempty",
                "terminal_nonempty", "admission_nonempty",
            )
        ]
        matrix = persisted_values["integration-qualification.json"]["matrix"]
        self.assertIs(type(matrix), list)
        self.assertEqual(len(matrix), 16)
        self.assertTrue(all(type(entry) is list and len(entry) == 2 for entry in matrix))
        self.assertEqual(matrix, expected_matrix)
        qualification_payload = canonical_json_bytes({"matrix": matrix})
        decoded = decode_canonical_json(qualification_payload)
        self.assertEqual(decoded["matrix"], tuple(tuple(entry) for entry in expected_matrix))
        self.assertEqual(canonical_json_bytes({"matrix": matrix}), qualification_payload)
        immutable_matrix = tuple(tuple(entry) for entry in expected_matrix)
        self.assertEqual(
            canonical_json_bytes({"matrix": immutable_matrix}),
            qualification_payload,
        )

    def test_11_pre_root_failure_remains_primary_and_terminal_does_not_touch_missing_root(self):
        namespace, calls, lifecycle_orders, _fake_sys, sentinel, _persisted_values = self._fake_owner_harness(fail_root=True)
        with self.assertRaises(RuntimeError) as raised:
            namespace["controller"]()
        self.assertIs(raised.exception, sentinel)
        self.assertEqual(lifecycle_orders, [])
        self.assertEqual([entry[0] for entry in calls], ["git"] * 6 + ["root"])


if __name__ == "__main__": unittest.main()
