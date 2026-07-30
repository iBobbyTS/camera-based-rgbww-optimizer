"""Synthetic integration qualification for the retained-R3 controller owners."""

from __future__ import annotations

from dataclasses import fields
import hashlib
import json
from types import FunctionType, ModuleType
import unittest

from camera_based_rgbww_optimizer.utils.agent_work_machine_contract import (
    FULL_PLAN_MACHINE_MARKER,
    PLAN_MACHINE_MARKER,
    parse_full_plan_machine_state,
    parse_plan_machine_contract,
)
from camera_based_rgbww_optimizer.utils import (
    p7_retained_r3_controller_preparation as preparation,
)
from camera_based_rgbww_optimizer.utils import (
    p7_retained_r3_exact_five_controller as lifecycle,
)


SHA = "1" * 64
RECORD_SHA = "2" * 64
SEAL_SHA = "3" * 64
PARENT = "4" * 40
OID = "5" * 40
TASK = "REF-SYNTHETIC-INTEGRATION"
CONTRACT = "SYNTHETIC-INTEGRATION-V1"


def _machine_row(marker: bytes, value: dict[str, object]) -> bytes:
    return marker + json.dumps(value, sort_keys=True, separators=(",", ":")).encode() + b"`\n"


def _request() -> lifecycle.ExactFiveControllerRequest:
    entries = tuple(
        lifecycle.ExactFiveCandidateEntry(f"candidate/{index}.txt", SHA, OID)
        for index in range(5)
    )
    return lifecycle.ExactFiveControllerRequest(
        reference_task_id=TASK,
        contract_id=CONTRACT,
        entries=entries,
        expected_parent=PARENT,
        expected_subject="test(p7): synthetic integration",
        candidate_identity_sha256=SHA,
        bootstrap_record_sha256=RECORD_SHA,
        bootstrap_seal_sha256=SEAL_SHA,
        import_static_argv=("python", "-m", "compileall"),
        targeted_test_argv=("python", "-m", "unittest", "targeted"),
        focused_test_argv=("python", "-m", "unittest", "focused"),
        full_test_argv=("python", "-m", "unittest", "discover"),
        subordinate_manifest_schema="synthetic-subordinate-v1",
    )


def _prepared_lifecycle() -> lifecycle.PreparedExactFiveController:
    request = _request()
    plan = {
        "reference_task_id": TASK,
        "contract_id": CONTRACT,
        "activation_commit": {
            "expected_parent": PARENT,
            "expected_subject": request.expected_subject,
        },
        "candidate_contract": {"identity_sha256": SHA, "exact_entry_count": 5},
        "accepted_bootstrap": {
            "record_sha256": RECORD_SHA,
            "seal_sha256": SEAL_SHA,
        },
    }
    full = {
        "active_task_count": 1,
        "active_task": TASK,
        "active_plan_contract_id": CONTRACT,
        "retained_r3_status": "RETAINED_UNVALIDATED_UNCONSUMED",
        "candidate_machine_contract_sha256": SHA,
        "candidate_contract_orchestrator_verified": True,
    }
    return lifecycle.prepare_exact_five_controller(
        request,
        parse_plan_machine_contract(_machine_row(PLAN_MACHINE_MARKER, plan)),
        parse_full_plan_machine_state(_machine_row(FULL_PLAN_MACHINE_MARKER, full)),
    )


def _prepared_source() -> preparation.PreparedControllerSource:
    source = b"""\
def controller():
    payload = {"mode": "old"}
    require_payload(payload)
"""
    return preparation.prepare_controller_source(
        source,
        assignment_name="payload",
        validation_function="require_payload",
        replacement_statement=b'payload = {"mode": "prepared"}',
    )


class _CompositionHarness:
    def __init__(
        self,
        prepared_source: preparation.PreparedControllerSource,
        *,
        fail_phase: str | None = None,
        tamper: tuple[str, object] | None = None,
    ) -> None:
        self.prepared_source = prepared_source
        self.fail_phase = fail_phase
        self.tamper = tamper
        self.order: list[str] = []
        self.terminals: list[object] = []
        self.er_gates: list[object] = []
        self.synthetic_validator_calls = 0
        self.actual_validator_calls = 0

    def _pass(self, phase: str):
        def callback(_argument: object) -> bool:
            self.order.append(phase)
            if phase == "acquire":
                self.assert_prepared_source()
            return phase != self.fail_phase

        return callback

    def assert_prepared_source(self) -> None:
        if hashlib.sha256(self.prepared_source.source).hexdigest() != self.prepared_source.source_sha256:
            raise AssertionError("prepared source identity drift")
        if b'payload = {"mode": "prepared"}' not in self.prepared_source.source:
            raise AssertionError("prepared source was not consumed")

    def synthetic_validator(self, _request: object) -> bool:
        self.order.append("canonical_validator")
        self.synthetic_validator_calls += 1
        return True

    def emit_er(self, gate: object) -> bool:
        self.order.append("execution_result")
        self.er_gates.append(gate)
        return True

    def terminal_seal(self, terminal: object) -> bool:
        self.order.append("terminal_seal")
        self.terminals.append(terminal)
        target = preparation.SealTargetIdentity(
            path="synthetic/terminal.json",
            byte_count=321,
            sha256="6" * 64,
            device=7,
            inode=11,
        )
        serialized_target = dict(target.as_mapping())
        if self.tamper is not None:
            key, value = self.tamper
            serialized_target[key] = value
        terminal_payload = {
            "schema": "synthetic-controller-terminal-v1",
            "status": terminal["status"],
            "failed_phase": terminal["failed_phase"],
            "callback_counts": dict(terminal["callback_counts"]),
            "prepared_source_sha256": self.prepared_source.source_sha256,
            "target": serialized_target,
        }
        terminal_bytes = preparation.canonical_terminal_bytes(terminal_payload)
        admitted = preparation.validate_and_emit_execution_result(
            terminal_bytes,
            target,
            self.emit_er,
        )
        return admitted is True

    def callbacks(self) -> lifecycle.ExactFiveControllerCallbacks:
        return lifecycle.ExactFiveControllerCallbacks(
            acquire=self._pass("acquire"),
            materialize_one_entry=self._pass("materialize_one_entry"),
            import_static_gate=self._pass("import_static_gate"),
            targeted_gate=self._pass("targeted_gate"),
            focused_gate=self._pass("focused_gate"),
            full_gate=self._pass("full_gate"),
            single_commit=self._pass("single_commit"),
            subordinate_manifest_seal=self._pass("subordinate_manifest_seal"),
            canonical_validator=self.synthetic_validator,
            terminal_seal=self.terminal_seal,
        )


class RetainedR3ControllerIntegrationTests(unittest.TestCase):
    def test_success_composes_preparation_lifecycle_seal_and_er_gate(self):
        source = _prepared_source()
        harness = _CompositionHarness(source)

        terminal = lifecycle.execute_prepared_exact_five_controller(
            _prepared_lifecycle(), harness.callbacks()
        )

        expected = ["acquire"] + ["materialize_one_entry"] * 5 + [
            "import_static_gate",
            "targeted_gate",
            "focused_gate",
            "full_gate",
            "single_commit",
            "subordinate_manifest_seal",
            "canonical_validator",
            "terminal_seal",
            "execution_result",
        ]
        self.assertEqual(harness.order, expected)
        self.assertEqual(terminal["status"], "PASS")
        self.assertEqual(terminal["callback_counts"]["materialize_one_entry"], 5)
        self.assertEqual(harness.synthetic_validator_calls, 1)
        self.assertEqual(harness.actual_validator_calls, 0)
        self.assertEqual(len(harness.terminals), 1)
        self.assertEqual(len(harness.er_gates), 1)
        gate = harness.er_gates[0]
        self.assertEqual(gate.payload["prepared_source_sha256"], source.source_sha256)
        self.assertEqual(dict(gate.target.as_mapping()), gate.payload["target"])
        with self.assertRaises(TypeError):
            gate.payload["status"] = "MUTATED"

    def test_preparation_failure_prevents_every_lifecycle_callback(self):
        malformed = b"""\
def controller():
    payload = 1
    require_payload(payload)
    payload = 2
    require_payload(payload)
"""
        harness = _CompositionHarness.__new__(_CompositionHarness)
        callback_counts = {field.name: 0 for field in fields(lifecycle.ExactFiveControllerCallbacks)}

        with self.assertRaises(preparation.ControllerPreparationError):
            preparation.prepare_controller_source(
                malformed,
                assignment_name="payload",
                validation_function="require_payload",
                replacement_statement=b"payload = 3",
            )

        self.assertEqual(callback_counts, {name: 0 for name in callback_counts})
        self.assertFalse(hasattr(harness, "terminals"))
        self.assertFalse(hasattr(harness, "er_gates"))

    def test_lifecycle_failure_seals_once_and_admits_failure_er_without_eligibility(self):
        harness = _CompositionHarness(_prepared_source(), fail_phase="focused_gate")

        with self.assertRaises(lifecycle.ExactFiveControllerError) as raised:
            lifecycle.execute_prepared_exact_five_controller(
                _prepared_lifecycle(), harness.callbacks()
            )

        self.assertEqual(raised.exception.phase, "focused_gate")
        self.assertEqual(harness.order[-2:], ["terminal_seal", "execution_result"])
        self.assertNotIn("full_gate", harness.order)
        self.assertNotIn("single_commit", harness.order)
        self.assertEqual(len(harness.terminals), 1)
        self.assertEqual(len(harness.er_gates), 1)
        self.assertEqual(harness.er_gates[0].payload["status"], "FAIL")
        self.assertEqual(harness.er_gates[0].payload["failed_phase"], "focused_gate")
        self.assertNotIn("eligibility", harness.er_gates[0].payload)
        self.assertEqual(harness.synthetic_validator_calls, 0)
        self.assertEqual(harness.actual_validator_calls, 0)

    def test_target_value_or_type_tamper_fails_before_er_without_fallback(self):
        for tamper in (("path", "synthetic/other.json"), ("bytes", True)):
            with self.subTest(tamper=tamper):
                harness = _CompositionHarness(_prepared_source(), tamper=tamper)
                with self.assertRaises(lifecycle.ExactFiveControllerError) as raised:
                    lifecycle.execute_prepared_exact_five_controller(
                        _prepared_lifecycle(), harness.callbacks()
                    )
                self.assertEqual(raised.exception.phase, "terminal_seal")
                self.assertEqual(harness.order.count("terminal_seal"), 1)
                self.assertEqual(harness.order.count("execution_result"), 0)
                self.assertEqual(harness.er_gates, [])

    def test_static_ownership_boundary_has_no_real_validator_or_io_surface(self):
        imported_modules = {
            value.__name__
            for value in globals().values()
            if isinstance(value, ModuleType)
        }
        self.assertEqual(
            {name for name in imported_modules if name.startswith("camera_based_rgbww_optimizer")},
            {
                "camera_based_rgbww_optimizer.utils.p7_retained_r3_controller_preparation",
                "camera_based_rgbww_optimizer.utils.p7_retained_r3_exact_five_controller",
            },
        )
        forbidden_module_tokens = (
            "canonical_validator",
            "release",
            "consumer",
            ".camera",
            "ray120c",
            "esphome",
        )
        self.assertFalse(
            any(token in name for name in imported_modules for token in forbidden_module_tokens)
        )

        prohibited_calls = {
            "open",
            "read_text",
            "read_bytes",
            "write_text",
            "write_bytes",
            "getenv",
            "system",
            "run",
            "Popen",
            "socket",
            "connect",
        }

        def code_objects(code):
            yield code
            for constant in code.co_consts:
                if isinstance(constant, type(code)):
                    yield from code_objects(constant)

        loaded_names = {
            name
            for value in globals().values()
            if isinstance(value, FunctionType)
            for code in code_objects(value.__code__)
            for name in code.co_names
        }
        self.assertFalse(loaded_names & prohibited_calls)
        self.assertEqual(
            set(lifecycle.ExactFiveControllerCallbacks.__dataclass_fields__),
            {
                "acquire",
                "materialize_one_entry",
                "import_static_gate",
                "targeted_gate",
                "focused_gate",
                "full_gate",
                "single_commit",
                "subordinate_manifest_seal",
                "canonical_validator",
                "terminal_seal",
            },
        )


if __name__ == "__main__":
    unittest.main()
