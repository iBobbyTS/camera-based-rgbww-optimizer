from __future__ import annotations

import hashlib
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from camera_based_rgbww_optimizer.optimization import analyze_hsi_reference_repeatability as r1
from camera_based_rgbww_optimizer.optimization import analyze_p7_thermal_diagnostics as subject
from camera_based_rgbww_optimizer.optimization import measure_p7_thermal_diagnostics as measure
from camera_based_rgbww_optimizer.optimization import p7_thermal_diagnostics as thermal
from camera_based_rgbww_optimizer.optimization.hsi_source_evidence import expected_strip_payloads
from camera_based_rgbww_optimizer.control import camera_remote_v2


FEATURE_IDS = json.loads(thermal.POLICY_PATH.read_text(encoding="utf-8"))["feature_set"]["ids"]


def _feature(seed: float = 1.0):
    return {key: seed + index * 0.001 for index, key in enumerate(FEATURE_IDS)}


class _Clock:
    def __init__(self):
        self.value = 0.0

    def monotonic(self):
        return self.value

    def sleep(self, seconds):
        self.value += seconds


def _write_json(path: Path, value):
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _write_jsonl(path: Path, rows):
    path.write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in rows), encoding="utf-8")


def _cleanup_steps():
    return [
        {"name": "esphome", "ok": True, "detail": {"payload": {}}, "error": None},
        {"name": "ray120c", "ok": True, "detail": {"response": {}}, "error": None},
    ]


def _build_formal_td_a_run(root: Path, *, source: str = "ray", settle: bool = True) -> Path:
    plan = thermal.build_diagnostic_plan(
        thermal.TD_A, source=source, for_execution=True,
        human_authorization=thermal.TD_A, v2_capture_capability=True,
    )
    plan["camera"]["resolved_capture_settings"] = {
        "owner": "remote_backend.resolve_capture_settings",
        "iso": "125",
        "aperture": "implicit auto",
        "image_format": "RAW",
    }
    clock = _Clock()
    curve = json.loads(thermal.CURVE_PATH.read_text(encoding="utf-8"))
    _raw, off_payload = expected_strip_payloads({channel: 0 for channel in thermal.CHANNELS}, curve)

    def both_off(gate_id):
        return {
            "status": "pass", "gate_id": gate_id,
            "strip_verified_off": True, "ray_verified_off": True,
            "strip_device_evidence": {
                "schema_version": 1, "requested_payload": off_payload,
                "baseline_snapshot": {"schema_version": 1, "generation": 1, **off_payload},
                "device_snapshot": {"schema_version": 1, "generation": 2, **off_payload},
                "device_state_entity": {"object_id": "rgbww_commanded_state", "key": 1},
                "device_identity": {"name": "bedroom-rgbww-strip", "mac_address": "00:11:22:33:44:55"},
            },
            "ray_readback": {"data": {"intensity": 0}},
        }

    def capture(step):
        sequence = int(step["capture_id"].split("-", 1)[0])
        saved = root / f"{step['capture_id']}.CR3"
        saved.parent.mkdir(parents=True, exist_ok=True)
        saved.write_bytes(b"raw")
        command = step["command"] or {"strip": "off", "ray": "off"}
        covariate = thermal.build_covariate_record(
            source_id=step["source_id"], state_id=step["state_id"], command=command,
            sequence_index=sequence, capture_order=sequence,
            source_order=int(step.get("source_order", 0)),
            monotonic_timestamp_ns=int(clock.value * 1_000_000_000) + sequence + 1,
            wall_clock_timestamp="2026-07-20T00:00:00Z", session_elapsed_s=clock.value,
            source_on_elapsed_s=float(step["requested_elapsed_s"] or 0),
            state_on_elapsed_s=float(step["requested_elapsed_s"] or 0),
            off_duration_before_s=1800, previous_state_id=None, previous_state_dwell_s=None,
            shutter_seconds=0.01, raw_black_levels=[512] * 4, raw_white_level=16383,
            load_history={60: 0, 300: 0, 900: 0}, readback={}, curve=curve,
        )
        output = {
            "saved_file": str(saved), "physical_capture_count": 1,
            "capture": {
                "saved_file": str(saved), "iso": "125",
                "aperture": "implicit auto", "image_format": "RAW",
            },
            "recorded_exposure": {"status": "recorded", "seconds": 0.01},
            "thermal_covariates": covariate,
        }
        requested = float(step["requested_elapsed_s"] or 1.0)
        bridge_request = 1_000_000_000
        estimate = bridge_request + int(requested * 1_000_000_000)
        metadata = {
            "schema": "remote_capture_result_v2", "capture_id": step["capture_id"], "request_id": f"request-{sequence}",
            "timing_quality": "best_effort_gphoto2", "formal_p7_eligibility": "unchanged_requires_later_planner_advisor_decision",
            "cr3": {"sha256": __import__("hashlib").sha256(b"raw").hexdigest(), "byte_count": 3, "content_type": "image/x-canon-cr3"},
            "gphoto2": {
                "driver_event_type": None, "event_sequence": [], "request_received_monotonic_ns": bridge_request,
                "capture_call_started_monotonic_ns": bridge_request + 1, "capture_call_returned_monotonic_ns": estimate + 10_000_000,
                "camera_event_observed_monotonic_ns": None, "file_added_observed_monotonic_ns": None,
                "download_started_monotonic_ns": estimate + 20_000_000, "download_completed_monotonic_ns": estimate + 30_000_000,
                "cr3_saved_observed_monotonic_ns": estimate + 40_000_000, "clock_domain": "bridge_monotonic",
            },
            "recorded_exposure": {"seconds": 0.01, "source": "Canon:ExposureTime", "status": "recorded"},
            "exposure_start_estimate": {"timestamp_monotonic_ns": estimate, "clock_domain": "bridge_monotonic", "method": "gphoto_capture_return_minus_recorded_exposure", "status": "weak_estimate", "uncertainty_ms": None, "uncertainty_basis": "unknown"},
            "network_observation": {"request_id": f"request-{sequence}", "response_or_event_round_trip_ms": None, "uncertainty_ms": None, "uncertainty_basis": "unknown"},
            "bridge_utc_observation": {"request_received": "2026-07-20T00:00:00+00:00", "source": "bridge_system_clock_utc"},
        }
        multipart_size = 1000 + sequence
        metadata["_local_receipt"] = {
            "parser_version": camera_remote_v2.PARSER_VERSION,
            "response_headers": {
                "content-type": "multipart/mixed; boundary=fake",
                "content-length": str(multipart_size),
                "x-capture-id": step["capture_id"],
                "x-request-id": f"request-{sequence}",
                "x-capture-metadata-schema": camera_remote_v2.SCHEMA,
            },
            "multipart_body_byte_count": multipart_size,
            "multipart_body_sha256": "a" * 64,
            "http_attempts": 1,
            "successful_attempt_index": 1,
            "local_request_started_monotonic_s": 0.0,
            "local_response_received_monotonic_s": 0.2,
            "received_monotonic_s": 0.2,
            "timing_evidence": camera_remote_v2.reconstruct_best_effort_timing(
                metadata, local_request_started_monotonic_s=0.0,
                local_response_received_monotonic_s=0.2,
                local_readback_done_monotonic_s=0.0,
            ),
        }
        output["timing_metadata"] = metadata
        output["timing_evidence"] = metadata["_local_receipt"]["timing_evidence"]
        output["remote_metadata_path"] = str(root / f"{step['capture_id']}.CR3.metadata.json")
        (root / f"{step['capture_id']}.CR3.metadata.json").write_text(json.dumps(metadata), encoding="utf-8")
        if step["formal_measurement"]:
            output["feature_values"] = _feature(
                1.0 if settle else float(step["requested_elapsed_s"]),
            )
        else:
            output["ambient_diagnostic"] = {
                "geometry_hash": "frozen-geometry", "black_levels": [512] * 4,
                "white_level": 16383, "black_level_tolerance_dn": 2,
            }
        return output

    measure.execute_plan(
        plan, run_dir=root, apply_command_fn=lambda _step: {}, readback_fn=lambda _step: {},
        capture_fn=capture, both_off_gate_fn=both_off,
        cleanup_fn=lambda: {"status": "pass", "steps": _cleanup_steps()},
        monotonic_fn=clock.monotonic, sleep_fn=clock.sleep,
    )
    _write_json(root / "all-off-shell.json", _cleanup_steps())
    (root / "child-exit-status.txt").write_text("0\n", encoding="utf-8")
    (root / "all-off-shell.exit-status.txt").write_text("0\n", encoding="utf-8")
    _write_json(root / "wrapper-result.json", {
        "schema_version": 1,
        "experiment": "p7_thermal_diagnostics_v1",
        "status": "complete",
        "run_dir": str(root.resolve()),
        "wrapper_pid": 1001,
        "child_pid": 1002,
        "child_exit_code": 0,
        "shell_cleanup_exit_code": 0,
        "wrapper_exit_code": 0,
        "signal": None,
        "started_at": "2026-07-20T00:00:00Z",
    })
    return root


class AnalyzeP7ThermalDiagnosticsTests(unittest.TestCase):
    def test_public_analyzer_accepts_only_runner_round_trip_and_rejects_ledger_tampering(self):
        with tempfile.TemporaryDirectory() as tempdir:
            root = _build_formal_td_a_run(Path(tempdir) / "run")
            report = subject.analyze_thermal_run(
                root, feature_ids=FEATURE_IDS, compatibility_fn=lambda _left, _right: True,
            )
            self.assertEqual(report["capture_contract"], "pass")
            self.assertEqual(report["formal_capture_count"], 12)
            self.assertEqual(report["ambient_capture_count"], 3)
            self.assertEqual(report["physical_cr3_count"], 15)

            original_run = json.loads((root / "run.json").read_text(encoding="utf-8"))
            tampered_run = {**original_run, "capture_settings_provenance": {
                **original_run["capture_settings_provenance"], "iso": "400",
            }}
            _write_json(root / "run.json", tampered_run)
            with self.assertRaisesRegex(ValueError, "capture settings provenance"):
                subject.analyze_thermal_run(root, feature_ids=FEATURE_IDS, compatibility_fn=lambda _left, _right: True)
            _write_json(root / "run.json", original_run)

            original_captures = (root / "captures.jsonl").read_text(encoding="utf-8")
            rows = [json.loads(line) for line in original_captures.splitlines()]
            cases = {
                "missing ambient": [row for row in rows if row["capture_role"] != "ambient"],
                "duplicate ambient": rows + [next(row for row in rows if row["capture_role"] == "ambient")],
                "reordered ambient": [rows[1], rows[0], *rows[2:]],
                "forged formal role": [{**row, "formal_measurement": True} if row["capture_role"] == "ambient" else row for row in rows],
            }
            for label, tampered in cases.items():
                with self.subTest(label=label):
                    _write_jsonl(root / "captures.jsonl", tampered)
                    with self.assertRaises(ValueError):
                        subject.analyze_thermal_run(root, feature_ids=FEATURE_IDS, compatibility_fn=lambda _left, _right: True)
            (root / "captures.jsonl").write_text(original_captures, encoding="utf-8")

            rows = [json.loads(line) for line in original_captures.splitlines()]
            rows[1]["timing_evidence"]["best_effort_elapsed_s"] = 1.0
            _write_jsonl(root / "captures.jsonl", rows)
            with self.assertRaisesRegex(ValueError, "independent replay"):
                subject.analyze_thermal_run(root, feature_ids=FEATURE_IDS, compatibility_fn=lambda _left, _right: True)

            _write_jsonl(root / "captures.jsonl", [json.loads(line) for line in original_captures.splitlines()])
            clean_rows = [json.loads(line) for line in original_captures.splitlines()]
            metadata_path = Path(clean_rows[1]["capture"]["remote_metadata_path"])
            metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
            metadata["exposure_start_estimate"]["timestamp_monotonic_ns"] += 1
            metadata_path.write_text(json.dumps(metadata), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "timing estimate"):
                subject.analyze_thermal_run(root, feature_ids=FEATURE_IDS, compatibility_fn=lambda _left, _right: True)

    def test_public_analyzer_replays_v2_headers_parser_attempt_and_sidecar_owner(self):
        def mutate_sidecar(label, mutation):
            with tempfile.TemporaryDirectory() as tempdir:
                root = _build_formal_td_a_run(Path(tempdir) / "run")
                rows = [json.loads(line) for line in (root / "captures.jsonl").read_text(encoding="utf-8").splitlines()]
                metadata_path = Path(rows[1]["capture"]["remote_metadata_path"])
                metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
                mutation(metadata)
                metadata_path.write_text(json.dumps(metadata), encoding="utf-8")
                with self.subTest(label=label), self.assertRaises((ValueError, camera_remote_v2.RemoteCaptureV2Error)):
                    subject.analyze_thermal_run(root, feature_ids=FEATURE_IDS, compatibility_fn=lambda _left, _right: True)

        mutate_sidecar("missing header", lambda value: value["_local_receipt"]["response_headers"].pop("content-length"))
        mutate_sidecar("header id", lambda value: value["_local_receipt"]["response_headers"].__setitem__("x-capture-id", "forged"))
        mutate_sidecar("schema header", lambda value: value["_local_receipt"]["response_headers"].__setitem__("x-capture-metadata-schema", "forged"))
        mutate_sidecar("parser", lambda value: value["_local_receipt"].__setitem__("parser_version", "forged"))
        mutate_sidecar("network id", lambda value: value["network_observation"].__setitem__("request_id", "forged"))
        mutate_sidecar("attempt index", lambda value: value["_local_receipt"].__setitem__("successful_attempt_index", 2))
        mutate_sidecar("successful start", lambda value: value["_local_receipt"].__setitem__("local_request_started_monotonic_s", -1.0))
        mutate_sidecar("unknown sensitive", lambda value: value.__setitem__("remote_camera_serial", "secret"))

        with tempfile.TemporaryDirectory() as tempdir:
            root = _build_formal_td_a_run(Path(tempdir) / "run")
            rows = [json.loads(line) for line in (root / "captures.jsonl").read_text(encoding="utf-8").splitlines()]
            rows[1]["capture"]["remote_metadata_path"] = str(Path(tempdir) / "outside.metadata.json")
            _write_jsonl(root / "captures.jsonl", rows)
            with self.assertRaisesRegex(ValueError, "outside the current run"):
                subject.analyze_thermal_run(root, feature_ids=FEATURE_IDS, compatibility_fn=lambda _left, _right: True)

    def test_public_analyzer_rejects_missing_or_forged_both_off_ledger(self):
        with tempfile.TemporaryDirectory() as tempdir:
            root = _build_formal_td_a_run(Path(tempdir) / "run")
            original = (root / "isolation-gates.jsonl").read_text(encoding="utf-8")
            rows = [json.loads(line) for line in original.splitlines()]
            _write_jsonl(root / "isolation-gates.jsonl", rows[1:])
            with self.assertRaisesRegex(ValueError, "isolation gate ledger"):
                subject.analyze_thermal_run(root, feature_ids=FEATURE_IDS, compatibility_fn=lambda _left, _right: True)
            rows[0]["evidence"]["ray_readback"]["data"]["intensity"] = 1
            _write_jsonl(root / "isolation-gates.jsonl", rows)
            with self.assertRaisesRegex(ValueError, "intensity zero"):
                subject.analyze_thermal_run(root, feature_ids=FEATURE_IDS, compatibility_fn=lambda _left, _right: True)

    def test_public_analyzer_rejects_command_owner_or_count_tampering(self):
        with tempfile.TemporaryDirectory() as tempdir:
            root = _build_formal_td_a_run(Path(tempdir) / "run")
            commands = [json.loads(line) for line in (root / "commands.jsonl").read_text(encoding="utf-8").splitlines()]
            _write_jsonl(root / "commands.jsonl", commands[:-1])
            with self.assertRaisesRegex(ValueError, "ledger count"):
                subject.analyze_thermal_run(root, feature_ids=FEATURE_IDS, compatibility_fn=lambda _left, _right: True)
            commands[0]["state_id"] = "forged"
            _write_jsonl(root / "commands.jsonl", commands)
            with self.assertRaisesRegex(ValueError, "differs from frozen plan"):
                subject.analyze_thermal_run(root, feature_ids=FEATURE_IDS, compatibility_fn=lambda _left, _right: True)

    def test_public_analyzer_replays_cleanup_and_wrapper_completion(self):
        def mutate_json(path: Path, mutation):
            value = json.loads(path.read_text(encoding="utf-8"))
            mutation(value)
            _write_json(path, value)

        cases = {
            "python cleanup": lambda root: mutate_json(
                root / "all-off-python.json", lambda value: value["steps"][0].__setitem__("ok", False),
            ),
            "shell cleanup": lambda root: mutate_json(
                root / "all-off-shell.json", lambda value: value[1].__setitem__("ok", False),
            ),
            "run cleanup": lambda root: mutate_json(
                root / "run.json", lambda value: value.__setitem__("cleanup", "fail"),
            ),
            "wrapper child": lambda root: mutate_json(
                root / "wrapper-result.json", lambda value: value.__setitem__("child_exit_code", 1),
            ),
            "wrapper cleanup": lambda root: mutate_json(
                root / "wrapper-result.json", lambda value: value.__setitem__("shell_cleanup_exit_code", 1),
            ),
            "wrapper exit": lambda root: mutate_json(
                root / "wrapper-result.json", lambda value: value.__setitem__("wrapper_exit_code", 70),
            ),
            "wrapper signal": lambda root: mutate_json(
                root / "wrapper-result.json", lambda value: value.__setitem__("signal", "TERM"),
            ),
            "wrapper schema": lambda root: mutate_json(
                root / "wrapper-result.json", lambda value: value.__setitem__("unknown", True),
            ),
            "child exit file": lambda root: (root / "child-exit-status.txt").write_text("1\n", encoding="utf-8"),
            "shell exit file": lambda root: (root / "all-off-shell.exit-status.txt").write_text("1\n", encoding="utf-8"),
            "empty cleanup": lambda root: (root / "all-off-shell.json").write_text("", encoding="utf-8"),
        }
        for label, mutation in cases.items():
            with self.subTest(label=label), tempfile.TemporaryDirectory() as tempdir:
                root = _build_formal_td_a_run(Path(tempdir) / "run")
                mutation(root)
                with self.assertRaises(ValueError):
                    subject.analyze_thermal_run(
                        root, feature_ids=FEATURE_IDS, compatibility_fn=lambda _left, _right: True,
                    )

    def test_td_a_pair_finalizer_replays_both_runs_and_writes_atomic_outputs(self):
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            ray = _build_formal_td_a_run(root / "ray", source="ray")
            strip = _build_formal_td_a_run(root / "strip", source="strip")
            output = root / "combined"
            envelope_before = hashlib.sha256(thermal.OPERATING_ENVELOPE_PATH.read_bytes()).hexdigest()
            report = subject.analyze_td_a_pair(ray, strip, output, feature_ids=FEATURE_IDS)
            envelope_after = hashlib.sha256(thermal.OPERATING_ENVELOPE_PATH.read_bytes()).hexdigest()

            self.assertEqual(report["status"], "td_a_pass")
            self.assertEqual(
                report["t_formal_provisional_s"],
                max(report["t_settle_ray_s"], report["t_settle_strip_s"]),
            )
            self.assertEqual(report["formal_capture_count"], 24)
            self.assertEqual(report["ambient_capture_count"], 6)
            self.assertLessEqual(report["physical_cr3_count"], 44)
            self.assertTrue((output / "td-a-combined-analysis.json").is_file())
            self.assertTrue((output / "EXPERIMENT_SUMMARY.md").is_file())
            self.assertEqual(list(output.glob(".*.tmp-*")), [])
            self.assertEqual(envelope_before, envelope_after)

    def test_td_a_pair_cli_writes_combined_artifacts(self):
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            ray = _build_formal_td_a_run(root / "ray", source="ray")
            strip = _build_formal_td_a_run(root / "strip", source="strip")
            output = root / "combined"
            self.assertEqual(subject.main([
                str(ray), "--feature-ids", str(thermal.POLICY_PATH),
                "--paired-run", str(strip), "--combined-output", str(output),
            ]), 0)
            self.assertTrue((output / "td-a-combined-analysis.json").is_file())
            self.assertTrue((output / "EXPERIMENT_SUMMARY.md").is_file())

    def test_td_a_pair_finalizer_preserves_legal_nonsettle(self):
        for unsettled_source in ("ray", "strip"):
            with self.subTest(source=unsettled_source), tempfile.TemporaryDirectory() as tempdir:
                root = Path(tempdir)
                ray = _build_formal_td_a_run(
                    root / "ray", source="ray", settle=unsettled_source != "ray",
                )
                strip = _build_formal_td_a_run(
                    root / "strip", source="strip", settle=unsettled_source != "strip",
                )
                report = subject.analyze_td_a_pair(
                    ray, strip, root / "combined", feature_ids=FEATURE_IDS,
                )
                self.assertEqual(report["status"], "settling_not_demonstrated_by_600")
                self.assertIsNone(report["t_formal_provisional_s"])
                self.assertIsNone(report[f"t_settle_{unsettled_source}_s"])

    def test_td_a_pair_finalizer_rejects_source_and_input_owner_mismatch(self):
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            ray_a = _build_formal_td_a_run(root / "ray-a", source="ray")
            ray_b = _build_formal_td_a_run(root / "ray-b", source="ray")
            strip = _build_formal_td_a_run(root / "strip", source="strip")
            with self.assertRaisesRegex(ValueError, "Ray first and strip second"):
                subject.analyze_td_a_pair(ray_a, ray_b, root / "duplicate", feature_ids=FEATURE_IDS)
            with self.assertRaisesRegex(ValueError, "Ray first and strip second"):
                subject.analyze_td_a_pair(strip, ray_a, root / "reversed", feature_ids=FEATURE_IDS)

        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            ray = _build_formal_td_a_run(root / "ray", source="ray")
            strip = _build_formal_td_a_run(root / "strip", source="strip")
            strip_plan = json.loads((strip / "plan.json").read_text(encoding="utf-8"))
            input_name = next(iter(strip_plan["inputs"]))
            original = Path(strip_plan["inputs"][input_name]["path"])
            alternate = root / f"alternate-{original.name}"
            shutil.copyfile(original, alternate)
            strip_plan["inputs"][input_name]["path"] = str(alternate)
            _write_json(strip / "plan.json", strip_plan)
            with self.assertRaisesRegex(ValueError, "input path/hash mismatch"):
                subject.analyze_td_a_pair(ray, strip, root / "mismatch", feature_ids=FEATURE_IDS)

    def test_td_a_pair_finalizer_rejects_capture_settings_timing_and_exposure_tampering(self):
        def mutate_capture(root: Path, mutation):
            rows = [json.loads(line) for line in (root / "captures.jsonl").read_text(encoding="utf-8").splitlines()]
            mutation(rows[0])
            _write_jsonl(root / "captures.jsonl", rows)

        cases = {
            "missing CR3": lambda root: Path(
                json.loads((root / "captures.jsonl").read_text(encoding="utf-8").splitlines()[0])["capture"]["saved_file"],
            ).unlink(),
            "settings": lambda root: mutate_capture(
                root, lambda row: row["capture"]["capture"].__setitem__("iso", "400"),
            ),
            "recorded exposure": lambda root: mutate_capture(
                root, lambda row: row["capture"]["recorded_exposure"].__setitem__("status", "missing"),
            ),
            "timing": lambda root: mutate_capture(
                root, lambda row: row["timing_evidence"].__setitem__("best_effort_elapsed_s", 999.0),
            ),
        }
        for label, mutation in cases.items():
            with self.subTest(label=label), tempfile.TemporaryDirectory() as tempdir:
                root = Path(tempdir)
                ray = _build_formal_td_a_run(root / "ray", source="ray")
                strip = _build_formal_td_a_run(root / "strip", source="strip")
                mutation(strip)
                with self.assertRaises(ValueError):
                    subject.analyze_td_a_pair(ray, strip, root / "combined", feature_ids=FEATURE_IDS)

    def test_settle_never_returns_600(self):
        stable = {str(cycle): {point: [_feature()] for point in thermal.TIMED_POINTS} for cycle in range(3)}
        result = thermal.settle_from_cycles(stable, FEATURE_IDS)
        self.assertEqual(result["t_settle_s"], 60)
        drifting = {str(cycle): {point: [_feature(float(point))] for point in thermal.TIMED_POINTS} for cycle in range(3)}
        result = thermal.settle_from_cycles(drifting, FEATURE_IDS)
        self.assertIsNone(result["t_settle_s"])
        self.assertEqual(result["status"], "settling_not_demonstrated_by_600")

    def test_incompatible_cold_cycle_centers_block_settle(self):
        cycles = {
            "1": {point: [_feature(1)] for point in thermal.TIMED_POINTS},
            "2": {point: [_feature(2)] for point in thermal.TIMED_POINTS},
            "3": {point: [_feature(1)] for point in thermal.TIMED_POINTS},
        }
        result = thermal.settle_from_cycles(cycles, FEATURE_IDS)
        self.assertIsNone(result["t_settle_s"])

    def test_return_anchor_split_reports_history_dependence(self):
        captures = []
        roles = ("initial_anchor", "return_after_D", "return_after_B", "return_after_C")
        for index, role in enumerate(roles):
            captures.append({"plan_step": {"role": role, "state_id": "A", "requested_elapsed_s": 300}, "feature_values": _feature(1 if index < 3 else 9)})
        for state in ("D", "B", "C"):
            for point in thermal.TIMED_POINTS:
                captures.append({"plan_step": {"role": "switch_curve", "state_id": state, "requested_elapsed_s": point}, "feature_values": _feature(1)})
        report = subject.analyze_td_b(captures, feature_ids=FEATURE_IDS)
        self.assertEqual(report["status"], "history_dependent_at_current_protocol")

    def test_td_c_reports_order_balanced_not_abba(self):
        plan = thermal.build_diagnostic_plan(thermal.TD_C, variant="core")
        captures = [
            {"plan_step": step, "source_id": step["source_id"], "feature_values": _feature(1 if step["source_id"] == "ray" else 2)}
            for step in plan["captures"] if step["formal_measurement"]
        ]
        ambients = [
            {"plan_step": step, "ambient_diagnostic": {"geometry_hash": "g", "black_levels": [512] * 4}}
            for step in plan["captures"] if not step["formal_measurement"]
        ]
        report = subject.analyze_td_c(
            captures, ambients=ambients, feature_ids=FEATURE_IDS,
            compatibility_fn=lambda _left, _right: True,
            p6_compare_fn=lambda _rows: {"status": "pass"},
        )
        self.assertEqual(report["status"], "td_c_core_pass_waiting_for_planner")
        self.assertEqual(report["comparison_design"], "order_balanced_paired_comparison_not_classic_abba")
        self.assertEqual(report["balanced_order_effect"]["status"], "pass")

    def test_td_c_gate_fails_on_order_center_p6_or_ambient(self):
        plan = thermal.build_diagnostic_plan(thermal.TD_C, variant="core")
        captures = [
            {"plan_step": step, "source_id": step["source_id"], "feature_values": _feature(1 if step["source_id"] == "ray" else 2)}
            for step in plan["captures"] if step["formal_measurement"]
        ]
        ambients = [
            {"plan_step": step, "ambient_diagnostic": {"geometry_hash": "g", "black_levels": [512] * 4}}
            for step in plan["captures"] if not step["formal_measurement"]
        ]
        cases = (
            (lambda _left, _right: False, lambda _rows: {"status": "pass"}, ambients, "compatibility"),
            (lambda _left, _right: True, lambda _rows: {"status": "fail"}, ambients, "p6_interpretability"),
            (lambda _left, _right: True, lambda _rows: {"status": "pass"}, [
                {**row, "ambient_diagnostic": {"geometry_hash": "changed", "black_levels": [900] * 4}}
                if index == len(ambients) - 1 else row for index, row in enumerate(ambients)
            ], "ambient_trend"),
        )
        for compatibility, p6, ambient_rows, branch in cases:
            with self.subTest(branch=branch):
                report = subject.analyze_td_c(
                    captures, ambients=ambient_rows, feature_ids=FEATURE_IDS,
                    compatibility_fn=compatibility, p6_compare_fn=p6,
                )
                self.assertEqual(report["status"], "td_c_gate_failed")
                self.assertIn(branch, report["failure_branches"])

    def test_reference_epoch_v2_preserves_legacy_false_as_not_identifiable(self):
        legacy = {
            "ray_reference": {
                "failure_branch": "R-REFERENCE-UNSTABLE", "reference_epoch_shift": False,
                "failed_states": [{"compatibility": "fail"}],
            }
        }
        epoch = r1.build_reference_epoch_v2(legacy)
        self.assertEqual(epoch["reference_stationarity"], "fail")
        self.assertEqual(epoch["reference_shift_class"], "not_identifiable")
        self.assertFalse(epoch["legacy_reference_epoch_shift"])
        self.assertNotIn("no shift", epoch["reference_shift_reason"])

    def test_retained_r1_derived_writes_new_directory_only(self):
        with tempfile.TemporaryDirectory() as tempdir:
            before = (thermal.R1_RUN / "analysis.json").read_bytes()
            epoch_path, derived_path = r1.write_reference_epoch_v2_derived(thermal.R1_RUN, tempdir)
            epoch = json.loads(epoch_path.read_text(encoding="utf-8"))
            derived = json.loads(derived_path.read_text(encoding="utf-8"))
            after = (thermal.R1_RUN / "analysis.json").read_bytes()
        self.assertEqual(before, after)
        self.assertEqual(epoch["reference_shift_class"], "not_identifiable")
        self.assertTrue(derived["derived_only"])
        self.assertFalse(derived["original_artifacts_modified"])


if __name__ == "__main__":
    unittest.main()
