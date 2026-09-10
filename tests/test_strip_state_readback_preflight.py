from __future__ import annotations

import json
import os
import shutil
import signal
import subprocess
import tempfile
import time
import unittest
from pathlib import Path
from unittest import mock

from camera_based_rgbww_optimizer.control import all_off
from camera_based_rgbww_optimizer.control import strip_state_readback_preflight as subject


class _FakeVerifiedLight:
    def __init__(self, mutations=None, failures=None):
        self.generation = 10
        self.calls = []
        self.mutations = mutations or {}
        self.failures = failures or {}

    def __call__(self, cw, ww, r, g, b, **kwargs):
        call_index = len(self.calls)
        self.calls.append(((cw, ww, r, g, b), dict(kwargs)))
        if call_index in self.failures:
            raise self.failures[call_index]
        baseline = self.generation
        self.generation += 1
        payload = {
            "red": r, "green": g, "blue": b,
            "warm_white": ww, "cold_white": cw,
        }
        evidence = {
            "schema_version": 1,
            "requested_payload": dict(payload),
            "baseline_snapshot": _snapshot(baseline, **_zero_payload()),
            "device_snapshot": _snapshot(self.generation, **payload),
            "device_state_entity": {"object_id": "rgbww_commanded_state", "key": 7},
            "device_identity": {"name": "bedroom-rgbww-strip", "mac_address": "AA:BB"},
        }
        mutation = self.mutations.get(call_index)
        if mutation is not None:
            mutation(evidence)
        return evidence


class StripStateReadbackPreflightTests(unittest.TestCase):
    def test_dry_run_freezes_five_raw_steps_without_device_calls(self):
        with (
            tempfile.TemporaryDirectory() as tempdir,
            mock.patch.object(subject.esphome, "verified_light") as verified,
            mock.patch.object(subject.all_off, "turn_everything_off") as cleanup,
        ):
            run_dir = subject.write_dry_run(output_dir=Path(tempdir), run_name="dry")
            plan = _read_json(run_dir / "plan.json")
            run = _read_json(run_dir / "run.json")

        self.assertEqual([step["step_id"] for step in plan["transitions"]], [
            "startup_zero", "low_first", "low_repeat", "main_zero", "final_zero",
        ])
        self.assertEqual(plan["transitions"][1]["arguments"], subject.LOW_ARGUMENTS)
        self.assertEqual(plan["transitions"][1], plan["transitions"][2] | {"step_id": "low_first"})
        self.assertEqual(plan["output_policy"]["maximum_physical_pwm"], 48)
        self.assertIsNone(plan["output_policy"]["curve_path"])
        self.assertEqual(run["status"], "dry_run_complete")
        self.assertFalse(run["device_calls_performed"])
        verified.assert_not_called()
        cleanup.assert_not_called()

    def test_execute_requires_consent_and_exact_named_experiment_before_calls(self):
        base = ["--execute", "--output-dir", "unused", "--run-name", "blocked"]
        with mock.patch.object(subject, "execute_preflight") as execute:
            with self.assertRaises(SystemExit):
                subject.main(base)
            with self.assertRaises(SystemExit):
                subject.main(base + ["--allow-device-control", "--named-experiment", "wrong"])
        execute.assert_not_called()

    def test_success_records_five_globally_increasing_transitions_and_cleanup(self):
        verified = _FakeVerifiedLight()
        cleanup_calls = []

        def cleanup():
            cleanup_calls.append(True)
            return _successful_shutdown()

        with tempfile.TemporaryDirectory() as tempdir:
            run_dir = subject.execute_preflight(
                output_dir=Path(tempdir), run_name="success",
                verified_light_fn=verified, cleanup_fn=cleanup,
            )
            run = _read_json(run_dir / "run.json")
            records = _read_jsonl(run_dir / "transitions.jsonl")
            plan = _read_json(run_dir / "plan.json")
            self._assert_no_secret_keys(run_dir)

        self.assertEqual(run["status"], "complete")
        self.assertEqual(run["completed_transition_count"], 5)
        self.assertEqual([record["step_id"] for record in records], [
            "startup_zero", "low_first", "low_repeat", "main_zero", "final_zero",
        ])
        generations = [record["evidence"]["device_snapshot"]["generation"] for record in records]
        self.assertEqual(generations, sorted(generations))
        self.assertEqual(len(set(generations)), 5)
        self.assertEqual(records[1]["evidence"]["requested_payload"], records[2]["evidence"]["requested_payload"])
        final_snapshot = records[-1]["evidence"]["device_snapshot"]
        self.assertEqual({key: final_snapshot[key] for key in subject.PAYLOAD_KEYS}, _zero_payload())
        self.assertEqual(len(cleanup_calls), 2)
        self.assertTrue(all(call[1]["curve_path"] is None for call in verified.calls))
        self.assertTrue(all(call[1]["expected_name"] == "bedroom-rgbww-strip" for call in verified.calls))
        self.assertEqual(plan["output_policy"]["maximum_physical_pwm"], 48)

    def test_identity_name_or_mac_drift_is_rejected(self):
        mutations = {
            1: lambda evidence: evidence["device_identity"].update(mac_address="CC:DD"),
        }
        verified = _FakeVerifiedLight(mutations=mutations)
        with tempfile.TemporaryDirectory() as tempdir, self.assertRaises(subject.PreflightRunFailed):
            run_dir = Path(tempdir) / "identity"
            try:
                subject.execute_preflight(
                    output_dir=Path(tempdir), run_name="identity",
                    verified_light_fn=verified, cleanup_fn=_successful_shutdown,
                )
            finally:
                run = _read_json(run_dir / "run.json")
                failure = _read_json(run_dir / "failure.json")
        self.assertEqual(run["failure_branch"], "D0-DEVICE/IDENTITY")
        self.assertEqual(failure["primary_failure"]["branch"], "D0-DEVICE/IDENTITY")

    def test_missing_entity_stale_generation_channel_mismatch_and_timeout_fail_closed(self):
        cases = {
            "missing_entity": ({1: lambda evidence: evidence.update(device_state_entity={})}, {}),
            "stale_generation": ({1: lambda evidence: evidence["device_snapshot"].update(generation=10)}, {}),
            "channel_mismatch": ({1: lambda evidence: evidence["device_snapshot"].update(red=999)}, {}),
            "timeout": ({}, {1: RuntimeError("timed out waiting for RGBWW device-state generation")}),
        }
        for name, (mutations, failures) in cases.items():
            with self.subTest(name=name), tempfile.TemporaryDirectory() as tempdir:
                verified = _FakeVerifiedLight(mutations=mutations, failures=failures)
                with self.assertRaises(subject.PreflightRunFailed):
                    subject.execute_preflight(
                        output_dir=Path(tempdir), run_name=name,
                        verified_light_fn=verified, cleanup_fn=_successful_shutdown,
                    )
                run = _read_json(Path(tempdir) / name / "run.json")
                transitions = _read_jsonl(Path(tempdir) / name / "transitions.jsonl")
                self.assertNotEqual(run["status"], "complete")
                self.assertTrue((Path(tempdir) / name / "failure.json").exists())
                self.assertEqual(run["cleanup"]["python_finally"], "pass")
                self.assertEqual(run["cleanup"]["final_verified_zero"], "pass")
                failed = [record for record in transitions if record["status"] == "failed"]
                self.assertEqual(len(failed), 1)
                if name != "timeout":
                    self.assertIn("evidence", failed[0])

    def test_main_step_exception_still_executes_python_cleanup(self):
        verified = _FakeVerifiedLight(failures={1: ConnectionError("link dropped")})
        cleanup_calls = []

        def cleanup():
            cleanup_calls.append(True)
            return _successful_shutdown()

        with tempfile.TemporaryDirectory() as tempdir:
            with self.assertRaises(subject.PreflightRunFailed):
                subject.execute_preflight(
                    output_dir=Path(tempdir), run_name="error",
                    verified_light_fn=verified, cleanup_fn=cleanup,
                )
            run = _read_json(Path(tempdir) / "error" / "run.json")
        self.assertEqual(len(cleanup_calls), 2)
        self.assertEqual(run["cleanup"]["python_finally"], "pass")
        self.assertEqual(run["cleanup"]["final_verified_zero"], "pass")

    def test_final_verified_zero_failure_marks_cleanup_state_unknown(self):
        verified = _FakeVerifiedLight(failures={4: RuntimeError("timed out waiting for final zero")})
        with tempfile.TemporaryDirectory() as tempdir:
            with self.assertRaises(subject.PreflightRunFailed):
                subject.execute_preflight(
                    output_dir=Path(tempdir), run_name="unknown",
                    verified_light_fn=verified, cleanup_fn=_successful_shutdown,
                )
            run_dir = Path(tempdir) / "unknown"
            run = _read_json(run_dir / "run.json")
            final_zero = _read_json(run_dir / "final-zero.json")
        self.assertEqual(run["status"], "cleanup_state_unknown")
        self.assertEqual(run["failure_branch"], "D0-CLEANUP-UNKNOWN")
        self.assertEqual(final_zero["status"], "failed")

    def test_shutdown_requires_both_steps_and_ray_intensity_zero(self):
        for steps in (
            _successful_shutdown(ray_intensity=1),
            _successful_shutdown(esphome_ok=False),
            _successful_shutdown()[:1],
        ):
            with self.subTest(steps=steps), self.assertRaises(subject.PreflightFailure):
                subject._validate_shutdown_steps([
                    step.to_jsonable() if hasattr(step, "to_jsonable") else step for step in steps
                ])

    def test_wrapper_records_atomic_exit_evidence_and_runs_cleanup_once(self):
        if os.name == "nt" or shutil.which("zsh") is None:
            self.skipTest("the historical zsh wrapper test requires a POSIX zsh runtime")
        cases = [
            ("success", None, 0, 0, 0, "complete", None),
            ("failure", None, 7, 0, 7, "child_failed", None),
            ("cleanup_failure", None, 0, 9, 70, "cleanup_failed", None),
            ("sleep", signal.SIGINT, 130, 0, 130, "signaled", "INT"),
            ("sleep", signal.SIGTERM, 143, 0, 143, "signaled", "TERM"),
        ]
        for mode, sent_signal, child_code, cleanup_code, wrapper_code, status, signal_name in cases:
            with self.subTest(mode=mode, sent_signal=sent_signal), tempfile.TemporaryDirectory() as tempdir:
                root, wrapper, call_log = _make_fake_wrapper_project(Path(tempdir))
                run_dir = root / "runs" / f"{mode}-{getattr(sent_signal, 'name', 'exit')}"
                env = os.environ.copy()
                env["FAKE_RUNNER_MODE"] = mode
                env["FAKE_CALL_LOG"] = str(call_log)
                ready_file = Path(tempdir) / "runner-ready"
                env["FAKE_READY_FILE"] = str(ready_file)
                process = subprocess.Popen(
                    ["zsh", str(wrapper), str(run_dir)], env=env,
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                    start_new_session=True,
                )
                try:
                    if sent_signal is not None:
                        deadline = time.monotonic() + 5
                        while not ready_file.exists() and time.monotonic() < deadline:
                            time.sleep(0.02)
                        self.assertTrue(ready_file.exists())
                        os.kill(process.pid, sent_signal)
                    process.wait(timeout=8)
                finally:
                    if process.poll() is None:
                        os.killpg(process.pid, signal.SIGKILL)
                        process.wait(timeout=5)
                calls = call_log.read_text(encoding="utf-8").splitlines()
                cleanup_calls = [line for line in calls if "camera_based_rgbww_optimizer.control.all_off" in line]
                self.assertEqual(len(cleanup_calls), 1)
                self.assertEqual(process.returncode, wrapper_code)
                self.assertEqual((run_dir / "child-exit-status.txt").read_text(encoding="utf-8").strip(), str(child_code))
                self.assertEqual((run_dir / "all-off-shell.exit-status.txt").read_text(encoding="utf-8").strip(), str(cleanup_code))
                result = _read_json(run_dir / "wrapper-result.json")
                self.assertEqual(result["status"], status)
                self.assertEqual(result["child_exit_code"], child_code)
                self.assertEqual(result["shell_cleanup_exit_code"], cleanup_code)
                self.assertEqual(result["wrapper_exit_code"], wrapper_code)
                self.assertEqual(result["signal"], signal_name)
                self.assertEqual(Path(result["artifacts"]["run_dir"]), run_dir.resolve())
                self.assertEqual(Path(result["artifacts"]["shell_cleanup"]), run_dir.resolve() / "all-off-shell.json")
                self.assertFalse(list(run_dir.glob(".*.tmp.*")))
                self.assertNotIn("secret", json.dumps(result).lower())
                self.assertNotIn("token", json.dumps(result).lower())
                cleanup_stdout = (run_dir / "all-off-shell.json").read_text(encoding="utf-8")
                self.assertIn('"name": "esphome"', cleanup_stdout)
                cleanup_stderr = (run_dir / "all-off-shell.stderr.log").read_text(encoding="utf-8")
                if mode == "cleanup_failure":
                    self.assertIn("fake cleanup failed", cleanup_stderr)
                else:
                    self.assertEqual(cleanup_stderr, "")

    def _assert_no_secret_keys(self, run_dir: Path):
        forbidden = ("secret", "token", "api_key", "encryption_key")

        def visit(value):
            if isinstance(value, dict):
                for key, child in value.items():
                    self.assertFalse(any(word in key.lower() for word in forbidden), key)
                    visit(child)
            elif isinstance(value, list):
                for child in value:
                    visit(child)

        for path in run_dir.glob("*.json"):
            visit(_read_json(path))
        for path in run_dir.glob("*.jsonl"):
            for row in _read_jsonl(path):
                visit(row)


def _successful_shutdown(*, ray_intensity=0, esphome_ok=True):
    return [
        all_off.ShutdownStep("esphome", esphome_ok, detail={"payload": _zero_payload()}),
        all_off.ShutdownStep("ray120c", True, detail={
            "cct": 5600, "gm": 100,
            "response": {"code": 0, "data": {"cct": 5600, "gm": 100, "intensity": ray_intensity}},
        }),
    ]


def _zero_payload():
    return {"red": 0, "green": 0, "blue": 0, "warm_white": 0, "cold_white": 0}


def _snapshot(generation, **payload):
    return {"schema_version": 1, "generation": generation, **payload}


def _read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _read_jsonl(path):
    return [json.loads(line) for line in Path(path).read_text(encoding="utf-8").splitlines()]


def _make_fake_wrapper_project(tempdir: Path):
    root = tempdir / "project"
    (root / "tmp").mkdir(parents=True)
    (root / ".venv/bin").mkdir(parents=True)
    source = Path(__file__).parents[1] / "tmp/run-strip-state-readback-preflight.zsh"
    wrapper = root / "tmp/run-strip-state-readback-preflight.zsh"
    shutil.copy2(source, wrapper)
    fake_python = root / ".venv/bin/python"
    fake_python.write_text("""#!/usr/bin/env python3
import json
import os
import signal
import sys
import time

with open(os.environ["FAKE_CALL_LOG"], "a", encoding="utf-8") as handle:
    handle.write(" ".join(sys.argv[1:]) + "\\n")
if len(sys.argv) > 1 and sys.argv[1] == "-c":
    os.execv(sys.executable, [sys.executable, *sys.argv[1:]])
if "camera_based_rgbww_optimizer.control.all_off" in sys.argv:
    print(json.dumps([{"name": "esphome", "ok": True}, {"name": "ray120c", "ok": True}]))
    if os.environ.get("FAKE_RUNNER_MODE") == "cleanup_failure":
        print("fake cleanup failed", file=sys.stderr)
        raise SystemExit(9)
    raise SystemExit(0)
mode = os.environ.get("FAKE_RUNNER_MODE", "success")
if mode in {"success", "cleanup_failure"}:
    raise SystemExit(0)
if mode == "failure":
    raise SystemExit(7)
for signum in (signal.SIGINT, signal.SIGTERM, signal.SIGHUP):
    signal.signal(signum, lambda received, _frame: sys.exit(128 + received))
open(os.environ["FAKE_READY_FILE"], "w", encoding="utf-8").write("ready\\n")
time.sleep(30)
""", encoding="utf-8")
    fake_python.chmod(0o755)
    return root, wrapper, tempdir / "calls.log"


if __name__ == "__main__":
    unittest.main()
