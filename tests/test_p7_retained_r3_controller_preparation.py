import ast
import hashlib
import json
from pathlib import Path
import unittest

from camera_based_rgbww_optimizer.utils import (
    p7_retained_r3_controller_preparation as subject,
)


SHA = "1" * 64


def source(body: str) -> bytes:
    return ("def controller():\n" + body).encode("utf-8")


def target(**changes):
    values = {
        "path": "root/terminal.json",
        "byte_count": 123,
        "sha256": SHA,
        "device": 7,
        "inode": 11,
    }
    values.update(changes)
    return subject.SealTargetIdentity(**values)


def terminal(identity=None, *, status="PASS", **changes):
    identity = identity or target()
    payload = {
        "schema": "terminal-v1",
        "status": status,
        "target": dict(identity.as_mapping()),
    }
    payload.update(changes)
    return subject.canonical_terminal_bytes(payload)


class ControllerPreparationTests(unittest.TestCase):
    def test_direct_nested_and_double_nested_ownership(self):
        cases = (
            "    payload = {'a': 1}\n    require_payload(payload)\n",
            "    if True:\n        payload = {'a': 1}\n        require_payload(payload)\n",
            "    if True:\n        for _ in (1,):\n            payload = {'a': 1}\n            require_payload(payload)\n",
        )
        for value in cases:
            with self.subTest(value=value):
                pair = subject.locate_owned_statement_pair(
                    source(value),
                    assignment_name="payload",
                    validation_function="require_payload",
                )
                self.assertEqual(pair.function_name, "controller")
                self.assertLess(pair.assignment_span.end, pair.validation_span.start)

    def test_owner_and_cardinality_ambiguities_fail_closed(self):
        cases = {
            "cross_function": b"def one():\n    payload = 1\ndef two():\n    require_payload(payload)\n",
            "async": b"async def controller():\n    payload = 1\n    require_payload(payload)\n",
            "zero_owner": b"payload = 1\nrequire_payload(payload)\n",
            "zero_match": b"def controller():\n    other = 1\n    require_payload(other)\n",
            "multiple": b"def controller():\n    payload = 1\n    require_payload(payload)\n    payload = 2\n    require_payload(payload)\n",
        }
        for name, value in cases.items():
            with self.subTest(name=name), self.assertRaises(subject.ControllerPreparationError):
                subject.locate_owned_statement_pair(
                    value,
                    assignment_name="payload",
                    validation_function="require_payload",
                )

        lambda_tree = ast.parse("owner = lambda: payload")
        edges = subject._parent_edges(lambda_tree)
        name = next(node for node in ast.walk(lambda_tree) if isinstance(node, ast.Name) and node.id == "payload")
        with self.assertRaises(subject.ControllerPreparationError) as raised:
            subject._regular_function_owner(name, edges)
        self.assertEqual(raised.exception.code, "alternate_function_owner")

    def test_regular_function_nested_in_regular_function_is_ambiguous(self):
        value = b"""\
def outer():
    def inner():
        if True:
            payload = 1
            require_payload(payload)
"""
        with self.assertRaises(subject.ControllerPreparationError) as raised:
            subject.locate_owned_statement_pair(
                value,
                assignment_name="payload",
                validation_function="require_payload",
            )
        self.assertEqual(raised.exception.code, "function_owner_ambiguous")

    def test_same_list_adjacency_is_required(self):
        invalid = (
            "    payload = 1\n    marker = 2\n    require_payload(payload)\n",
            "    if True:\n        payload = 1\n    require_payload(payload)\n",
        )
        for body in invalid:
            with self.subTest(body=body), self.assertRaises(subject.ControllerPreparationError):
                subject.locate_owned_statement_pair(
                    source(body),
                    assignment_name="payload",
                    validation_function="require_payload",
                )

    def test_same_line_and_utf8_byte_offsets_select_exact_statement(self):
        value = "def controller():\n    if '色': payload = 1; require_payload(payload)\n".encode()
        pair = subject.locate_owned_statement_pair(
            value,
            assignment_name="payload",
            validation_function="require_payload",
        )
        self.assertEqual(value[pair.assignment_span.start:pair.assignment_span.end], b"payload = 1")
        self.assertEqual(
            value[pair.validation_span.start:pair.validation_span.end],
            b"require_payload(payload)",
        )

    def test_span_boundaries_and_order_are_deterministic(self):
        value = b"x = 1\ny = 2\n"
        replacements = (
            subject.SourceReplacement(subject.ByteSpan(6, 11), b"y = 4"),
            subject.SourceReplacement(subject.ByteSpan(0, 5), b"x = 3"),
        )
        self.assertEqual(subject.replace_byte_spans(value, replacements), b"x = 3\ny = 4\n")

    def test_invalid_replacement_spans_fail_closed(self):
        value = b"x = 1\n"
        cases = (
            (),
            (subject.SourceReplacement(subject.ByteSpan(2, 2), b"x"),),
            (subject.SourceReplacement(subject.ByteSpan(4, 2), b"x"),),
            (subject.SourceReplacement(subject.ByteSpan(0, 99), b"x"),),
            (
                subject.SourceReplacement(subject.ByteSpan(0, 4), b"x"),
                subject.SourceReplacement(subject.ByteSpan(3, 5), b"y"),
            ),
        )
        for replacements in cases:
            with self.subTest(replacements=replacements), self.assertRaises(subject.ControllerPreparationError):
                subject.replace_byte_spans(value, replacements)

    def test_malformed_replacements_fail_with_stable_error_before_sorting(self):
        malformed_sets = (
            (object(),),
            (None,),
            (
                subject.SourceReplacement(subject.ByteSpan(0, 1), b"x"),
                {"span": subject.ByteSpan(2, 3), "replacement": b"y"},
            ),
            None,
        )
        for replacements in malformed_sets:
            with self.subTest(replacements=replacements):
                with self.assertRaises(subject.ControllerPreparationError) as raised:
                    subject.replace_byte_spans(b"x = 1\n", replacements)
                self.assertEqual(raised.exception.code, "invalid_replacement")

    def test_prepared_source_is_deterministic_parseable_and_compilable(self):
        value = source("    payload = {'old': 1}\n    require_payload(payload)\n")
        kwargs = {
            "assignment_name": "payload",
            "validation_function": "require_payload",
            "replacement_statement": b"payload = {'new': 2}",
        }
        first = subject.prepare_controller_source(value, **kwargs)
        second = subject.prepare_controller_source(value, **kwargs)
        self.assertEqual(first, second)
        self.assertEqual(first.source_sha256, hashlib.sha256(first.source).hexdigest())
        tree = ast.parse(first.source.decode())
        self.assertIsNotNone(compile(tree, "<test>", "exec"))
        self.assertIn(b"payload = {'new': 2}", first.source)

    def test_invalid_prepared_source_is_never_returned(self):
        value = source("    payload = 1\n    require_payload(payload)\n")
        with self.assertRaises(subject.ControllerPreparationError) as raised:
            subject.prepare_controller_source(
                value,
                assignment_name="payload",
                validation_function="require_payload",
                replacement_statement=b"payload = (",
            )
        self.assertEqual(raised.exception.code, "prepared_source_invalid")

    def test_canonical_terminal_success_has_exactly_one_lf(self):
        data = terminal()
        self.assertTrue(data.endswith(b"}\n"))
        self.assertFalse(data.endswith(b"\n\n"))
        gate = subject.validate_terminal_seal(data, target())
        self.assertEqual(gate.payload["status"], "PASS")

    def test_terminal_encoding_and_line_ending_rejections(self):
        canonical = terminal()
        cases = (
            canonical[:-1],
            canonical + b"\n",
            canonical[:-1] + b"\r\n",
            canonical[:-2] + b"\\n\"}\n",
            b"\xff\n",
            b'{"schema":"terminal-v1",\n"status":"PASS"}\n',
        )
        for data in cases:
            with self.subTest(data=data), self.assertRaises(subject.ControllerPreparationError):
                subject.validate_terminal_seal(data, target())

    def test_duplicate_nonfinite_and_noncanonical_json_rejected(self):
        identity = json.dumps(dict(target().as_mapping()), separators=(",", ":"), sort_keys=True)
        cases = (
            ('{"schema":"terminal-v1","schema":"terminal-v1","status":"PASS","target":' + identity + '}\n').encode(),
            ('{"schema":"terminal-v1","status":NaN,"target":' + identity + '}\n').encode(),
            ('{"schema": "terminal-v1", "status": "PASS", "target": ' + identity + '}\n').encode(),
            ('{"status":"PASS","schema":"terminal-v1","target":' + identity + '}\n').encode(),
        )
        for data in cases:
            with self.subTest(data=data), self.assertRaises(subject.ControllerPreparationError):
                subject.validate_terminal_seal(data, target())

    def test_every_target_identity_field_is_bound(self):
        changes = {
            "path": "other",
            "byte_count": 124,
            "sha256": "2" * 64,
            "device": 8,
            "inode": 12,
        }
        for field, value in changes.items():
            payload = json.loads(terminal().decode())
            key = "bytes" if field == "byte_count" else field
            payload["target"][key] = value
            data = subject.canonical_terminal_bytes(payload)
            with self.subTest(field=field), self.assertRaises(subject.ControllerPreparationError):
                subject.validate_terminal_seal(data, target())
        payload = json.loads(terminal().decode())
        del payload["target"]["inode"]
        with self.assertRaises(subject.ControllerPreparationError):
            subject.validate_terminal_seal(subject.canonical_terminal_bytes(payload), target())

    def test_target_schema_and_runtime_types_are_exact(self):
        substitutions = {
            "bytes_bool": ("bytes", True),
            "bytes_float": ("bytes", 123.0),
            "bytes_string": ("bytes", "123"),
            "device_float": ("device", 7.0),
            "inode_float": ("inode", 11.0),
            "path_number": ("path", 1),
            "sha_number": ("sha256", 1),
        }
        for name, (key, value) in substitutions.items():
            payload = json.loads(terminal().decode())
            payload["target"][key] = value
            with self.subTest(name=name):
                with self.assertRaises(subject.ControllerPreparationError) as raised:
                    subject.validate_terminal_seal(
                        subject.canonical_terminal_bytes(payload), target()
                    )
                self.assertEqual(raised.exception.code, "terminal_target_mismatch")

        payload = json.loads(terminal().decode())
        payload["target"]["extra"] = "not-allowed"
        with self.assertRaises(subject.ControllerPreparationError) as raised:
            subject.validate_terminal_seal(
                subject.canonical_terminal_bytes(payload), target()
            )
        self.assertEqual(raised.exception.code, "terminal_target_mismatch")

    def test_validated_gate_payload_is_recursively_immutable_and_detached(self):
        payload = json.loads(terminal().decode())
        payload["details"] = {"attempts": [{"name": "one"}], "counts": [1, 2]}
        data = subject.canonical_terminal_bytes(payload)
        identity = target()
        gate = subject.validate_terminal_seal(data, identity)

        payload["details"]["attempts"][0]["name"] = "caller-mutated"
        self.assertEqual(gate.payload["details"]["attempts"][0]["name"], "one")
        self.assertIsInstance(gate.payload["details"]["attempts"], tuple)
        with self.assertRaises(TypeError):
            gate.payload["status"] = "MUTATED"
        with self.assertRaises(TypeError):
            gate.payload["details"]["attempts"][0]["name"] = "MUTATED"
        with self.assertRaises(AttributeError):
            gate.payload["details"]["counts"].append(3)
        with self.assertRaises(AttributeError):
            gate.target.path = "other"
        self.assertEqual(dict(gate.target.as_mapping()), dict(identity.as_mapping()))

    def test_success_and_failure_terminal_both_dominate_er_callback(self):
        calls = []
        for status in ("PASS", "FAIL"):
            result = subject.validate_and_emit_execution_result(
                terminal(status=status),
                target(),
                lambda gate: calls.append(gate.payload["status"]) or "written",
            )
            self.assertEqual(result, "written")
        self.assertEqual(calls, ["PASS", "FAIL"])

    def test_invalid_seal_and_callback_setup_leave_er_count_zero(self):
        calls = []
        invalid = (
            terminal()[:-1],
            terminal(target(path="other")),
        )
        for data in invalid:
            with self.subTest(data=data), self.assertRaises(subject.ControllerPreparationError):
                subject.validate_and_emit_execution_result(
                    data, target(), lambda gate: calls.append(gate)
                )
        with self.assertRaises(subject.ControllerPreparationError):
            subject.validate_and_emit_execution_result(terminal()[:-1], target(), None)
        self.assertEqual(calls, [])

    def test_primary_error_and_callback_result_semantics_are_preserved(self):
        primary = RuntimeError("primary")
        calls = []
        with self.assertRaises(RuntimeError) as raised:
            subject.validate_and_emit_execution_result(
                terminal(status="FAIL"),
                target(),
                lambda gate: calls.append(gate) or "cannot-convert-to-success",
                primary_error=primary,
            )
        self.assertIs(raised.exception, primary)
        self.assertEqual(len(calls), 1)

        with self.assertRaises(RuntimeError) as raised:
            subject.validate_and_emit_execution_result(
                terminal(status="FAIL"),
                target(),
                lambda gate: (_ for _ in ()).throw(ValueError("er")),
                primary_error=primary,
            )
        self.assertIs(raised.exception, primary)

    def test_seal_gate_cannot_be_constructed_normally(self):
        gate_type = type(subject.validate_terminal_seal(terminal(), target()))
        with self.assertRaises(subject.ControllerPreparationError):
            gate_type(object(), {}, target())

    def test_static_source_has_no_io_forbidden_imports_or_large_nested_program(self):
        source_text = Path(subject.__file__).read_text(encoding="utf-8")
        tree = ast.parse(source_text)
        imported = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module is not None:
                imported.add(node.module.split(".")[0])
        self.assertFalse(imported & {
            "os", "pathlib", "subprocess", "socket", "requests", "camera",
            "measurement", "release", "git",
        })
        prohibited = {
            "open", "read", "write", "read_text", "read_bytes", "write_text",
            "write_bytes", "stat", "rename", "replace", "fsync", "unlink",
            "mkdir", "system", "run", "Popen",
        }
        name_calls = {
            node.func.id for node in ast.walk(tree)
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
        }
        attr_calls = {
            node.func.attr for node in ast.walk(tree)
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
        }
        self.assertFalse(name_calls & prohibited)
        self.assertFalse(attr_calls & prohibited)
        long_literals = [
            node.value for node in ast.walk(tree)
            if isinstance(node, ast.Constant) and isinstance(node.value, (str, bytes))
            and len(node.value) > 1000
        ]
        self.assertEqual(long_literals, [])


if __name__ == "__main__":
    unittest.main()
