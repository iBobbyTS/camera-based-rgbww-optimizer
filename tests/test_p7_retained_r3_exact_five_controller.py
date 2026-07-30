import ast
from dataclasses import replace
import dis
import inspect
import json
from pathlib import Path
import unittest

from camera_based_rgbww_optimizer.utils.agent_work_machine_contract import (
    FULL_PLAN_MACHINE_MARKER,
    PLAN_MACHINE_MARKER,
    parse_full_plan_machine_state,
    parse_plan_machine_contract,
)
from camera_based_rgbww_optimizer.utils import p7_retained_r3_exact_five_controller as subject


SHA = "1" * 64
RECORD_SHA = "2" * 64
SEAL_SHA = "3" * 64
PARENT = "4" * 40
OID = "5" * 40
TASK = "REF-P7-25-R2-B1A-C3E6F19"
CONTRACT = "P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F19-CONTROLLER-PREPARATION"


def machine_row(marker, value):
    return marker + json.dumps(value, sort_keys=True, separators=(",", ":")).encode() + b"`\n"


def entries(count=5):
    return tuple(
        subject.ExactFiveCandidateEntry(f"candidate/{index}.txt", SHA, OID)
        for index in range(count)
    )


def request(**changes):
    value = subject.ExactFiveControllerRequest(
        reference_task_id=TASK,
        contract_id=CONTRACT,
        entries=entries(),
        expected_parent=PARENT,
        expected_subject="feat(scope): exact five",
        candidate_identity_sha256=SHA,
        bootstrap_record_sha256=RECORD_SHA,
        bootstrap_seal_sha256=SEAL_SHA,
        import_static_argv=("python", "-m", "compileall"),
        targeted_test_argv=("python", "-m", "unittest", "targeted"),
        focused_test_argv=("python", "-m", "unittest", "focused"),
        full_test_argv=("python", "-m", "unittest", "discover"),
        subordinate_manifest_schema="subordinate-manifest-v1",
    )
    return replace(value, **changes) if changes else value


def parsed(req=None, *, plan_changes=None, full_changes=None):
    req = req or request()
    plan_value = {
        "reference_task_id": req.reference_task_id,
        "contract_id": req.contract_id,
        "activation_commit": {
            "expected_parent": req.expected_parent,
            "expected_subject": req.expected_subject,
        },
        "candidate_contract": {
            "identity_sha256": req.candidate_identity_sha256,
            "exact_entry_count": 5,
        },
        "accepted_bootstrap": {
            "record_sha256": req.bootstrap_record_sha256,
            "seal_sha256": req.bootstrap_seal_sha256,
        },
    }
    full_value = {
        "active_task_count": 1,
        "active_task": req.reference_task_id,
        "active_plan_contract_id": req.contract_id,
        "retained_r3_status": "RETAINED_UNVALIDATED_UNCONSUMED",
        "candidate_machine_contract_sha256": req.candidate_identity_sha256,
        "candidate_contract_orchestrator_verified": True,
    }
    if plan_changes:
        plan_value.update(plan_changes)
    if full_changes:
        full_value.update(full_changes)
    return (
        parse_plan_machine_contract(machine_row(PLAN_MACHINE_MARKER, plan_value)),
        parse_full_plan_machine_state(machine_row(FULL_PLAN_MACHINE_MARKER, full_value)),
    )


class FakeCallbacks:
    def __init__(self, fail_phase=None, raise_phase=None, missing_phase=None):
        self.calls = []
        self.terminals = []
        self.fail_phase = fail_phase
        self.raise_phase = raise_phase
        values = {}
        for phase in (
            "acquire", "materialize_one_entry", "import_static_gate", "targeted_gate",
            "focused_gate", "full_gate", "single_commit", "subordinate_manifest_seal",
            "canonical_validator", "terminal_seal",
        ):
            values[phase] = None if phase == missing_phase else self._callback(phase)
        self.callbacks = subject.ExactFiveControllerCallbacks(**values)

    def _callback(self, phase):
        def callback(argument):
            self.calls.append(phase)
            if phase == "terminal_seal":
                self.terminals.append(argument)
            if self.raise_phase == phase:
                raise RuntimeError("synthetic")
            return self.fail_phase != phase
        return callback


class ExactFiveControllerTests(unittest.TestCase):
    def prepare(self, req=None, **parsed_changes):
        req = req or request()
        plan, full = parsed(req, **parsed_changes)
        return subject.prepare_exact_five_controller(req, plan, full)

    def test_valid_prepare_is_pure_and_full_sequence_is_exact(self):
        fake = FakeCallbacks()
        prepared = self.prepare()
        self.assertEqual(fake.calls, [])
        terminal = subject.execute_prepared_exact_five_controller(prepared, fake.callbacks)
        self.assertEqual(
            fake.calls,
            ["acquire"] + ["materialize_one_entry"] * 5 + [
                "import_static_gate", "targeted_gate", "focused_gate", "full_gate",
                "single_commit", "subordinate_manifest_seal", "canonical_validator",
                "terminal_seal",
            ],
        )
        self.assertEqual(terminal["status"], "PASS")
        self.assertIsNone(terminal["failed_phase"])
        self.assertEqual(terminal["callback_counts"]["materialize_one_entry"], 5)
        for phase in ("targeted_gate", "focused_gate", "full_gate", "single_commit",
                      "subordinate_manifest_seal", "canonical_validator", "terminal_seal"):
            self.assertEqual(terminal["callback_counts"][phase], 1)
        self.assertEqual(len({entry.repo_path for entry in prepared.request.entries}), 5)

    def test_exact_five_count_duplicate_and_order_fail_closed(self):
        for bad_entries, code in (
            (entries(4), "entry_count_not_five"),
            (entries(6), "entry_count_not_five"),
            ((entries()[0],) * 5, "duplicate_entry_path"),
            (tuple(reversed(entries())), "entries_not_utf8_sorted"),
        ):
            with self.subTest(code=code):
                with self.assertRaises(subject.ExactFiveControllerError) as raised:
                    request(entries=bad_entries)
                self.assertEqual(raised.exception.code, code)

    def test_path_sha_and_oid_validation_fail_closed(self):
        invalid_paths = ("", "/abs", ".", "..", "a/../b", "a\\b", "a/*.py", "a/[x]")
        for path in invalid_paths:
            with self.subTest(path=path):
                with self.assertRaises(subject.ExactFiveControllerError):
                    subject.ExactFiveCandidateEntry(path, SHA, OID)
        for bad_sha in ("A" * 64, "1" * 63, "g" * 64):
            with self.subTest(sha=bad_sha):
                with self.assertRaises(subject.ExactFiveControllerError):
                    subject.ExactFiveCandidateEntry("a", bad_sha, OID)
        for bad_oid in ("A" * 40, "5" * 39, "g" * 40):
            with self.subTest(oid=bad_oid):
                with self.assertRaises(subject.ExactFiveControllerError):
                    subject.ExactFiveCandidateEntry("a", SHA, bad_oid)

    def test_plan_and_full_drift_rejected_before_callbacks(self):
        cases = (
            ("plan_task", {"plan_changes": {"reference_task_id": "drift"}}),
            ("plan_contract", {"plan_changes": {"contract_id": "drift"}}),
            ("full_task", {"full_changes": {"active_task": "drift"}}),
            ("full_contract", {"full_changes": {"active_plan_contract_id": "drift"}}),
            ("candidate", {"full_changes": {"candidate_machine_contract_sha256": "9" * 64}}),
            ("retained", {"full_changes": {"retained_r3_status": "drift"}}),
            ("verified", {"full_changes": {"candidate_contract_orchestrator_verified": False}}),
        )
        for name, changes in cases:
            with self.subTest(name=name):
                fake = FakeCallbacks()
                with self.assertRaises(subject.ExactFiveControllerError):
                    self.prepare(**changes)
                self.assertEqual(fake.calls, [])

    def test_each_execution_phase_exception_and_non_pass_seals_once_and_stops(self):
        phases = (
            "acquire", "materialize_one_entry", "import_static_gate", "targeted_gate",
            "focused_gate", "full_gate", "single_commit", "subordinate_manifest_seal",
            "canonical_validator",
        )
        for phase in phases:
            for mode in ("fail", "raise"):
                with self.subTest(phase=phase, mode=mode):
                    fake = FakeCallbacks(
                        fail_phase=phase if mode == "fail" else None,
                        raise_phase=phase if mode == "raise" else None,
                    )
                    with self.assertRaises(subject.ExactFiveControllerError) as raised:
                        subject.execute_prepared_exact_five_controller(
                            self.prepare(), fake.callbacks
                        )
                    self.assertEqual(raised.exception.phase, phase)
                    self.assertEqual(fake.calls.count("terminal_seal"), 1)
                    self.assertEqual(fake.calls[-1], "terminal_seal")
                    self.assertEqual(fake.terminals[0]["status"], "FAIL")
                    self.assertEqual(fake.terminals[0]["failed_phase"], phase)

    def test_missing_canonical_validator_is_not_success(self):
        fake = FakeCallbacks(missing_phase="canonical_validator")
        with self.assertRaises(subject.ExactFiveControllerError) as raised:
            subject.execute_prepared_exact_five_controller(self.prepare(), fake.callbacks)
        self.assertEqual(raised.exception.phase, "canonical_validator")
        self.assertEqual(fake.calls.count("terminal_seal"), 1)
        self.assertNotIn("canonical_validator", fake.calls)

    def test_terminal_failure_is_attempted_once(self):
        for mode in ("fail", "raise"):
            fake = FakeCallbacks(
                fail_phase="terminal_seal" if mode == "fail" else None,
                raise_phase="terminal_seal" if mode == "raise" else None,
            )
            with self.subTest(mode=mode):
                with self.assertRaises(subject.ExactFiveControllerError) as raised:
                    subject.execute_prepared_exact_five_controller(self.prepare(), fake.callbacks)
                self.assertEqual(raised.exception.phase, "terminal_seal")
                self.assertEqual(fake.calls.count("terminal_seal"), 1)

    def test_callback_protocol_has_no_forbidden_members(self):
        fields = set(subject.ExactFiveControllerCallbacks.__dataclass_fields__)
        self.assertEqual(
            fields,
            {"acquire", "materialize_one_entry", "import_static_gate", "targeted_gate",
             "focused_gate", "full_gate", "single_commit", "subordinate_manifest_seal",
             "canonical_validator", "terminal_seal"},
        )
        self.assertFalse({name for name in fields if any(token in name for token in (
            "consumer", "eligibility", "network", "device", "release"
        ))})

    def test_static_source_and_bytecode_have_no_direct_io_or_forbidden_imports(self):
        source_text = Path(subject.__file__).read_text(encoding="utf-8")
        tree = ast.parse(source_text)
        imported = {
            alias.name.split(".")[0]
            for node in ast.walk(tree)
            if isinstance(node, (ast.Import, ast.ImportFrom))
            for alias in node.names
        }
        self.assertFalse(imported & {
            "os", "pathlib", "subprocess", "socket", "requests", "camera", "measurement",
            "release", "git",
        })
        prohibited_calls = {"open", "read_text", "read_bytes", "write_text", "write_bytes",
                            "unlink", "mkdir", "system", "run", "Popen"}
        name_calls = {
            node.func.id
            for node in ast.walk(tree)
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
        }
        attribute_calls = {
            node.func.attr
            for node in ast.walk(tree)
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
        }
        self.assertFalse(name_calls & (prohibited_calls - {"run"}))
        self.assertFalse(attribute_calls & prohibited_calls)

        execute = next(
            node for node in tree.body
            if isinstance(node, ast.FunctionDef)
            and node.name == "execute_prepared_exact_five_controller"
        )
        nested_run_definitions = [
            node for node in execute.body
            if isinstance(node, ast.FunctionDef) and node.name == "run"
        ]
        self.assertEqual(
            [node for node in ast.walk(tree)
             if isinstance(node, ast.FunctionDef) and node.name == "run"],
            nested_run_definitions,
        )
        self.assertEqual(len(nested_run_definitions), 1)
        parents = {
            child: node
            for node in ast.walk(tree)
            for child in ast.iter_child_nodes(node)
        }
        run_calls = [
            node for node in ast.walk(tree)
            if isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "run"
        ]
        self.assertTrue(run_calls)
        for call in run_calls:
            owner = parents[call]
            while not isinstance(owner, (ast.FunctionDef, ast.AsyncFunctionDef)):
                owner = parents[owner]
            self.assertIs(owner, execute)

        def code_objects(code):
            yield code
            for constant in code.co_consts:
                if inspect.iscode(constant):
                    yield from code_objects(constant)

        instructions = [
            (code.co_name, instruction)
            for value in vars(subject).values()
            if inspect.isfunction(value)
            for code in code_objects(value.__code__)
            for instruction in dis.get_instructions(code)
        ]
        global_or_name_loads = {
            instruction.argval
            for _owner, instruction in instructions
            if instruction.opname in {"LOAD_GLOBAL", "LOAD_NAME"}
        }
        attribute_or_method_loads = {
            instruction.argval
            for _owner, instruction in instructions
            if instruction.opname in {"LOAD_ATTR", "LOAD_METHOD"}
        }
        self.assertFalse(global_or_name_loads & prohibited_calls)
        self.assertFalse(attribute_or_method_loads & prohibited_calls)
        run_loads = [
            (owner, instruction.opname)
            for owner, instruction in instructions
            if instruction.argval == "run"
        ]
        self.assertTrue(run_loads)
        self.assertEqual(
            set(run_loads),
            {
                ("execute_prepared_exact_five_controller", "STORE_FAST"),
                ("execute_prepared_exact_five_controller", "LOAD_FAST"),
            },
        )

    def test_success_terminal_follows_validator_and_owns_no_authorization(self):
        fake = FakeCallbacks()
        terminal = subject.execute_prepared_exact_five_controller(self.prepare(), fake.callbacks)
        self.assertLess(fake.calls.index("canonical_validator"), fake.calls.index("terminal_seal"))
        serialized = json.dumps(
            {"status": terminal["status"], "failed_phase": terminal["failed_phase"],
             "callback_results": dict(terminal["callback_results"]),
             "callback_counts": dict(terminal["callback_counts"])},
            sort_keys=True,
        )
        self.assertNotIn("eligibility", serialized)
        self.assertNotIn("production_release_usable", serialized)

    def test_public_exports_are_exact(self):
        self.assertEqual(
            set(subject.__all__),
            {"ExactFiveControllerError", "ExactFiveCandidateEntry", "ExactFiveControllerRequest",
             "ExactFiveControllerCallbacks", "PreparedExactFiveController",
             "prepare_exact_five_controller", "execute_prepared_exact_five_controller"},
        )


if __name__ == "__main__":
    unittest.main()
