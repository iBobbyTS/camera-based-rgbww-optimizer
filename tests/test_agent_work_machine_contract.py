import hashlib
import inspect
import json
from collections.abc import Mapping
from pathlib import Path
from types import MappingProxyType
import unittest

from camera_based_rgbww_optimizer.utils import agent_work_machine_contract as subject


def row(marker: bytes, payload: bytes, ending: bytes = b"`\n") -> bytes:
    return marker + payload + ending


class AgentWorkMachineContractTests(unittest.TestCase):
    def assert_json_semantically_equal(self, actual, expected):
        if isinstance(expected, dict):
            self.assertIsInstance(actual, Mapping)
            self.assertEqual(set(actual), set(expected))
            for key, expected_value in expected.items():
                self.assert_json_semantically_equal(actual[key], expected_value)
            return
        if isinstance(expected, list):
            self.assertIsInstance(actual, tuple)
            self.assertEqual(len(actual), len(expected))
            for actual_value, expected_value in zip(actual, expected, strict=True):
                self.assert_json_semantically_equal(actual_value, expected_value)
            return
        self.assertIs(type(actual), type(expected))
        self.assertEqual(actual, expected)

    def assert_error(self, code, parser, source):
        with self.assertRaises(subject.MachineContractValidationError) as raised:
            parser(source)
        self.assertEqual(raised.exception.code, code)
        self.assertEqual(
            raised.exception.evidence["schema"],
            "agent_work_machine_contract_scan_evidence_v1",
        )
        json.dumps(raised.exception.evidence, sort_keys=True, allow_nan=False)
        return raised.exception.evidence

    def test_valid_plan_and_full_rows_preserve_values_and_replay_evidence(self):
        cases = (
            (
                "PLAN",
                subject.PLAN_MACHINE_MARKER,
                subject.parse_plan_machine_contract,
                b'{"nested":{"enabled":true,"items":[1,null,"x"]}}',
            ),
            (
                "FULL",
                subject.FULL_PLAN_MACHINE_MARKER,
                subject.parse_full_plan_machine_state,
                b'{"active_task":"C13","verified":false}',
            ),
        )
        for owner, marker, parser, payload in cases:
            with self.subTest(owner=owner):
                raw_row = row(marker, payload)
                source = b"heading\n" + raw_row + b"tail\n"
                parsed = parser(source)
                self.assert_json_semantically_equal(parsed.value, json.loads(payload))
                evidence = parsed.evidence
                self.assertEqual(evidence.owner, owner)
                self.assertEqual(evidence.marker_ascii, marker.decode("ascii"))
                self.assertEqual(evidence.source_bytes, len(source))
                self.assertEqual(evidence.source_sha256, hashlib.sha256(source).hexdigest())
                self.assertEqual(evidence.candidate_count, 1)
                self.assertEqual(evidence.candidate_lines, (2,))
                self.assertEqual(evidence.line_number, 2)
                self.assertEqual(evidence.raw_row_bytes, len(raw_row))
                self.assertEqual(evidence.raw_row_sha256, hashlib.sha256(raw_row).hexdigest())
                self.assertEqual(evidence.payload_bytes, len(payload))
                self.assertEqual(evidence.payload_sha256, hashlib.sha256(payload).hexdigest())
                self.assertEqual(evidence.line_ending, "LF")
                self.assertEqual(evidence.schema, "agent_work_machine_contract_scan_evidence_v1")
                self.assertEqual(json.loads(json.dumps(evidence.to_mapping())), evidence.to_mapping())

    def test_generic_parser_supports_custom_marker_and_legacy_wrappers_delegate(self):
        payload = b'{"nested":{"items":[true,2]}}'
        custom = subject.parse_machine_row(
            b"heading\n`CUSTOM_MACHINE_ROW=" + payload + b"`\ntail\n",
            b"CUSTOM_MACHINE_ROW=",
        )
        self.assert_json_semantically_equal(
            custom.value,
            {"nested": {"items": [True, 2]}},
        )
        self.assertEqual(custom.evidence.owner, "CUSTOM_MACHINE_ROW")

        plan_source = row(subject.PLAN_MACHINE_MARKER, payload)
        generic = subject.parse_machine_row(plan_source, subject.PLAN_MACHINE_MARKER[1:])
        legacy = subject.parse_plan_machine_contract(plan_source)
        self.assertEqual(generic.value, legacy.value)
        self.assertEqual(generic.evidence.owner, "PLAN_MACHINE_CONTRACT")
        self.assertEqual(legacy.evidence.owner, "PLAN")
        generic_evidence = generic.evidence.to_mapping()
        legacy_evidence = legacy.evidence.to_mapping()
        self.assertEqual(generic_evidence.pop("owner"), "PLAN_MACHINE_CONTRACT")
        self.assertEqual(legacy_evidence.pop("owner"), "PLAN")
        self.assertEqual(generic_evidence, legacy_evidence)

    def test_success_value_is_deeply_immutable(self):
        parsed = subject.parse_machine_row(
            b'`CUSTOM={"nested":{"items":[{"enabled":true}]}}`\n',
            b"CUSTOM=",
        )
        self.assertIsInstance(parsed.value, MappingProxyType)
        self.assertIsInstance(parsed.value["nested"], MappingProxyType)
        self.assertIsInstance(parsed.value["nested"]["items"], tuple)
        self.assertIsInstance(parsed.value["nested"]["items"][0], MappingProxyType)
        with self.assertRaises(TypeError):
            parsed.value["new"] = True
        with self.assertRaises(TypeError):
            parsed.value["nested"]["new"] = True
        with self.assertRaises(AttributeError):
            parsed.value["nested"]["items"].append(False)

    def test_plan_and_full_owners_are_separate(self):
        plan = row(subject.PLAN_MACHINE_MARKER, b'{"owner":"plan"}')
        full = row(subject.FULL_PLAN_MACHINE_MARKER, b'{"owner":"full"}')
        source = plan + full
        self.assertEqual(subject.parse_plan_machine_contract(source).value["owner"], "plan")
        self.assertEqual(subject.parse_full_plan_machine_state(source).value["owner"], "full")
        plan_evidence = self.assert_error(
            "candidate_count_not_one", subject.parse_plan_machine_contract, full,
        )
        full_evidence = self.assert_error(
            "candidate_count_not_one", subject.parse_full_plan_machine_state, plan,
        )
        self.assertEqual(plan_evidence["candidate_count"], 0)
        self.assertEqual(full_evidence["candidate_count"], 0)

    def test_line_endings_and_suffixes_fail_closed(self):
        marker = subject.PLAN_MACHINE_MARKER
        malformed = {
            "crlf": row(marker, b"{}", b"`\r\n"),
            "eof_without_lf": row(marker, b"{}", b"`"),
            "space_after_backtick": row(marker, b"{}", b"` \n"),
        }
        for name, source in malformed.items():
            with self.subTest(name=name):
                self.assert_error(
                    "invalid_line_ending_or_suffix",
                    subject.parse_plan_machine_contract,
                    source,
                )
        self.assert_error(
            "invalid_backtick_count",
            subject.parse_plan_machine_contract,
            row(marker, b"{}", b"``\n"),
        )

    def test_multiline_trailing_and_extra_backticks_fail_closed(self):
        marker = b"CUSTOM="
        malformed = (
            ("invalid_line_ending_or_suffix", b'`CUSTOM={"x":\n1}`\n'),
            ("invalid_line_ending_or_suffix", b'`CUSTOM={"x":1}` trailing\n'),
            ("invalid_backtick_count", b'`CUSTOM={"x":"`"}`\n'),
        )
        for code, source in malformed:
            with self.subTest(code=code, source=source):
                self.assert_error(
                    code,
                    lambda value: subject.parse_machine_row(value, marker),
                    source,
                )

    def test_wrong_or_indented_prefix_is_not_a_candidate(self):
        for source in (
            b"PLAN_MACHINE_CONTRACT={}`\n",
            b" `PLAN_MACHINE_CONTRACT={}`\n",
            b"prefix `PLAN_MACHINE_CONTRACT={}`\n",
        ):
            evidence = self.assert_error(
                "candidate_count_not_one", subject.parse_plan_machine_contract, source,
            )
            self.assertEqual(evidence["candidate_lines"], [])

    def test_duplicate_candidates_report_all_one_based_lines(self):
        valid = row(subject.PLAN_MACHINE_MARKER, b"{}")
        evidence = self.assert_error(
            "candidate_count_not_one",
            subject.parse_plan_machine_contract,
            b"intro\n" + valid + b"middle\n" + valid,
        )
        self.assertEqual(evidence["candidate_count"], 2)
        self.assertEqual(evidence["candidate_lines"], [2, 4])

    def test_invalid_utf8_and_malformed_json_fail_closed(self):
        self.assert_error(
            "invalid_utf8",
            subject.parse_plan_machine_contract,
            row(subject.PLAN_MACHINE_MARKER, b'{"x":"\xff"}'),
        )
        for payload in (b"{", b'{"x":}', b'{"x":1} trailing'):
            with self.subTest(payload=payload):
                self.assert_error(
                    "malformed_json",
                    subject.parse_plan_machine_contract,
                    row(subject.PLAN_MACHINE_MARKER, payload),
                )

    def test_top_level_non_objects_fail_closed(self):
        for payload in (b"[]", b'"text"', b"1", b"true", b"false", b"null"):
            with self.subTest(payload=payload):
                self.assert_error(
                    "top_level_not_object",
                    subject.parse_plan_machine_contract,
                    row(subject.PLAN_MACHINE_MARKER, payload),
                )

    def test_duplicate_keys_at_any_depth_and_nonfinite_constants_fail_closed(self):
        for payload in (b'{"x":1,"x":2}', b'{"outer":{"x":1,"x":2}}'):
            with self.subTest(payload=payload):
                self.assert_error(
                    "duplicate_json_key",
                    subject.parse_plan_machine_contract,
                    row(subject.PLAN_MACHINE_MARKER, payload),
                )
        for constant in (b"NaN", b"Infinity", b"-Infinity"):
            with self.subTest(constant=constant):
                self.assert_error(
                    "nonfinite_json_constant",
                    subject.parse_plan_machine_contract,
                    row(subject.PLAN_MACHINE_MARKER, b'{"value":' + constant + b"}"),
                )

    def test_json_values_and_types_are_not_coerced(self):
        payload = (
            b'{"true":true,"false":false,"zero":0,"one":1,"text":"1",'
            b'"none":null,"items":[false,0],"nested":{"value":true}}'
        )
        value = subject.parse_plan_machine_contract(
            row(subject.PLAN_MACHINE_MARKER, payload),
        ).value
        expected_types = {
            "true": bool,
            "false": bool,
            "zero": int,
            "one": int,
            "text": str,
            "none": type(None),
            "items": tuple,
            "nested": MappingProxyType,
        }
        self.assertEqual({key: type(item) for key, item in value.items()}, expected_types)
        self.assertIs(value["true"], True)
        self.assertIs(value["false"], False)
        self.assertEqual(value["zero"], 0)
        self.assertEqual(value["one"], 1)
        self.assertIs(type(value["zero"]), int)
        self.assertIs(type(value["one"]), int)
        self.assertIs(type(value["items"][0]), bool)
        self.assertIs(type(value["items"][1]), int)

    def test_generic_parser_rejects_invalid_source_and_literal_markers(self):
        self.assert_error(
            "source_not_exact_bytes",
            lambda source: subject.parse_machine_row(source, b"CUSTOM="),
            "not bytes",
        )
        for marker in ("CUSTOM=", bytearray(b"CUSTOM="), memoryview(b"CUSTOM=")):
            with self.subTest(marker_type=type(marker).__name__):
                self.assert_error(
                    "marker_not_exact_bytes",
                    lambda _source, marker=marker: subject.parse_machine_row(b"", marker),
                    b"",
                )
        for marker in (b"", b"`CUSTOM=", b"CUSTOM=`", b"CUSTOM=\r", b"CUSTOM=\n", b"\xff"):
            with self.subTest(marker=marker):
                self.assert_error(
                    "invalid_literal_marker",
                    lambda _source, marker=marker: subject.parse_machine_row(b"", marker),
                    b"",
                )

    def test_non_exact_bytes_and_error_evidence_are_stable(self):
        for source in ("bytes", bytearray(b"bytes"), memoryview(b"bytes")):
            with self.subTest(source_type=type(source).__name__):
                evidence = self.assert_error(
                    "source_not_exact_bytes", subject.parse_plan_machine_contract, source,
                )
                self.assertEqual(evidence["owner"], "PLAN")
                self.assertIsNone(evidence["source_bytes"])
                self.assertIsNone(evidence["source_sha256"])

    def test_public_surface_is_validation_only(self):
        expected = {
            "PLAN_MACHINE_MARKER",
            "FULL_PLAN_MACHINE_MARKER",
            "MachineContractValidationError",
            "MachineContractEvidence",
            "ParsedMachineContract",
            "parse_machine_row",
            "parse_plan_machine_contract",
            "parse_full_plan_machine_state",
        }
        self.assertEqual(set(subject.__all__), expected)
        self.assertEqual(
            tuple(inspect.signature(subject.parse_machine_row).parameters),
            ("complete_text", "literal_marker"),
        )
        for parser in (
            subject.parse_plan_machine_contract,
            subject.parse_full_plan_machine_state,
        ):
            self.assertEqual(tuple(inspect.signature(parser).parameters), ("source",))

        source = Path(subject.__file__).read_text(encoding="utf-8")
        prohibited = (
            "pathlib",
            "import os",
            "subprocess",
            "open(",
            "getenv",
            "candidate_eligible",
            "production_release_usable",
            "canonical validator",
            "retained_release",
            "repair_callback",
            "validator_callback",
            "eligibility_callback",
        )
        self.assertFalse({token for token in prohibited if token in source})
        self.assertIsInstance(
            subject.parse_machine_row(b"`CUSTOM={}`\n", b"CUSTOM=").value,
            Mapping,
        )


if __name__ == "__main__":
    unittest.main()
