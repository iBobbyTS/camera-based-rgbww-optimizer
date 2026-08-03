from __future__ import annotations

import ast
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from camera_based_rgbww_optimizer.optimization import p7_successor_zero_readiness as subject
from camera_based_rgbww_optimizer.utils import p7_retained_r3_provenance_io as provenance


class _FakeStrip:
    def __init__(self, *, failures: set[int] | None = None) -> None:
        self.calls: list[tuple[tuple[object, ...], dict[str, object]]] = []
        self.generation = 20
        self.failures = failures or set()

    def __call__(self, *values: object, **kwargs: object) -> dict[str, object]:
        index = len(self.calls)
        self.calls.append((values, dict(kwargs)))
        if index in self.failures:
            raise ConnectionError("fake strip failure")
        baseline = self.generation
        self.generation += 1
        return {
            "schema_version": 1,
            "requested_payload": dict(subject.ZERO_PAYLOAD),
            "baseline_snapshot": _snapshot(baseline),
            "device_snapshot": _snapshot(self.generation),
            "device_state_entity": {"object_id": "rgbww_commanded_state", "key": 7},
            "device_identity": {"name": subject.EXPECTED_STRIP_NAME, "mac_address": "AA:BB"},
        }


class _FakeRay:
    def __init__(self, *, failures: set[str] | None = None) -> None:
        self.failures = failures or set()
        self.set_calls: list[tuple[tuple[object, ...], dict[str, object]]] = []
        self.get_calls: list[dict[str, object]] = []
        self.node_calls: list[dict[str, object]] = []

    def set(self, *args: object, **kwargs: object) -> dict[str, object]:
        self.set_calls.append((args, dict(kwargs)))
        if "set" in self.failures:
            raise ConnectionError("fake ray set failure")
        return _ray_response()

    def get(self, **kwargs: object) -> dict[str, object]:
        self.get_calls.append(dict(kwargs))
        if "get" in self.failures:
            raise ConnectionError("fake ray get failure")
        return _ray_response()

    def node(self, **kwargs: object) -> dict[str, object]:
        self.node_calls.append(dict(kwargs))
        if "node" in self.failures:
            raise ConnectionError("fake node failure")
        return {"code": 0, "data": {"node_id": subject.EXPECTED_RAY_NODE}}


class SuccessorZeroReadinessTests(unittest.TestCase):
    def test_success_is_exact_canonical_non_authorizing_package(self) -> None:
        strip = _FakeStrip()
        ray = _FakeRay()
        deps = _dependencies(strip, ray)
        with tempfile.TemporaryDirectory() as tempdir, self._runtime(Path(tempdir)):
            root_path = Path(tempdir) / "success"
            root = subject.execute_zero_readiness(root_path, dependencies=deps)
            self.assertEqual(provenance.list_exact_regular_children(root), tuple(sorted(subject.INITIAL_ARTIFACTS)))
            scratches = _scratch_files(root_path, shell_exit=0)
            result = subject.finalize_zero_readiness(
                root_path,
                runner_log_source=scratches[0],
                wrapper_log_source=scratches[1],
                shell_json_source=scratches[2],
                shell_stderr_source=scratches[3],
                child_exit_status=0,
                shell_exit_status=0,
                wrapper_status="complete",
                wrapper_exit_status=0,
                signal_name=None,
                dependencies=deps,
            )
            self.assertEqual(result, 0)
            self.assertEqual(provenance.list_exact_regular_children(root), subject.FINAL_INVENTORY)
            terminal = _read_json(root_path / subject.TERMINAL_NAME)
            wrapper = _read_json(root_path / "wrapper-result.json")
            for path in root_path.iterdir():
                self.assertEqual(path.stat().st_mode & 0o777, 0o600)
                data = path.read_bytes()
                self.assertEqual(data, provenance.canonical_json_bytes(json.loads(data)))
                self.assertNotIn("secret", data.decode("utf-8").lower())
                self.assertNotIn("token", data.decode("utf-8").lower())
            self.assertEqual(terminal["status"], "sealed_pass_waiting_planner_review")
            self.assertFalse(terminal["terminal_self_reference"])
            self.assertEqual(terminal["artifact_count_before_terminal"], 13)
            self.assertNotIn(subject.TERMINAL_NAME, {item["path"] for item in terminal["artifacts"]})
            self.assertEqual(wrapper["call_ledger"]["strip_verified_zero"], 3)
            self.assertEqual(wrapper["call_ledger"]["strip_shell_zero"], 1)
            self.assertEqual(wrapper["call_ledger"]["ray_set_zero"], 4)
            self.assertEqual(wrapper["call_ledger"]["ray_get_cct"], 2)
            self.assertEqual(wrapper["call_ledger"]["source_isolation_validation"], 2)
            self.assertEqual(wrapper["capture_calls"], 0)
            self.assertEqual(wrapper["nonzero_calls"], 0)
            self.assertEqual(wrapper["release_consumption"], 0)
            self.assertEqual(len(strip.calls), 3)
            self.assertEqual(len(ray.set_calls), 3)
            self.assertEqual(len(ray.get_calls), 2)
            self.assertEqual(len(ray.node_calls), 1)
            _remove_scratches(scratches)

    def test_main_failure_retains_fail_seal_and_runs_all_cleanup_layers(self) -> None:
        strip = _FakeStrip()
        ray = _FakeRay()

        def camera_failure() -> dict[str, object]:
            raise ConnectionError("fake camera failure")

        deps = _dependencies(strip, ray, camera_probe=camera_failure)
        with tempfile.TemporaryDirectory() as tempdir, self._runtime(Path(tempdir)):
            root_path = Path(tempdir) / "main-fail"
            with self.assertRaisesRegex(subject.ZeroReadinessError, "main_readiness_failed"):
                subject.execute_zero_readiness(root_path, dependencies=deps)
            python_finally = _read_json(root_path / "python-finally-zero.json")
            self.assertEqual(python_finally["status"], "pass")
            self.assertEqual(python_finally["primary"]["phase"], "main_readiness")
            scratches = _scratch_files(root_path, shell_exit=0)
            code = subject.finalize_zero_readiness(
                root_path,
                runner_log_source=scratches[0], wrapper_log_source=scratches[1],
                shell_json_source=scratches[2], shell_stderr_source=scratches[3],
                child_exit_status=20, shell_exit_status=0,
                wrapper_status="child_failed", wrapper_exit_status=20,
                signal_name=None, dependencies=deps,
            )
            self.assertEqual(code, 20)
            self.assertEqual(_read_json(root_path / subject.TERMINAL_NAME)["status"], "sealed_fail_waiting_planner_review")
            self.assertEqual(len(strip.calls), 3)
            self.assertEqual(len(ray.set_calls), 3)
            _remove_scratches(scratches)

    def test_python_finally_failure_is_visible_and_not_retried(self) -> None:
        strip = _FakeStrip(failures={1})
        ray = _FakeRay()
        with tempfile.TemporaryDirectory() as tempdir, self._runtime(Path(tempdir)):
            root_path = Path(tempdir) / "finally-fail"
            with self.assertRaisesRegex(subject.ZeroReadinessError, "python_finally_zero_failed"):
                subject.execute_zero_readiness(root_path, dependencies=_dependencies(strip, ray))
            record = _read_json(root_path / "python-finally-zero.json")
            self.assertEqual(record["status"], "fail")
            self.assertEqual(record["failures"][0]["phase"], "python_finally_strip_zero")
            self.assertEqual(len(strip.calls), 2)
            self.assertEqual(len(ray.set_calls), 2)

    def test_shell_cleanup_and_signal_status_preserve_priority(self) -> None:
        for name, child, shell, status, wrapper_exit, signal_name in (
            ("shell", 0, 9, "shell_cleanup_failed", 70, None),
            ("signal", 130, 0, "signaled", 130, "INT"),
        ):
            with self.subTest(name=name), tempfile.TemporaryDirectory() as tempdir, self._runtime(Path(tempdir)):
                root_path = Path(tempdir) / name
                initial_deps = _dependencies(_FakeStrip(), _FakeRay())
                subject.execute_zero_readiness(root_path, dependencies=initial_deps)
                scratches = _scratch_files(root_path, shell_exit=shell)
                code = subject.finalize_zero_readiness(
                    root_path,
                    runner_log_source=scratches[0], wrapper_log_source=scratches[1],
                    shell_json_source=scratches[2], shell_stderr_source=scratches[3],
                    child_exit_status=child, shell_exit_status=shell,
                    wrapper_status=status, wrapper_exit_status=wrapper_exit,
                    signal_name=signal_name,
                    dependencies=_dependencies(_FakeStrip(), _FakeRay()),
                )
                self.assertEqual(code, wrapper_exit)
                wrapper = _read_json(root_path / "wrapper-result.json")
                self.assertEqual(wrapper["status"], status)
                self.assertEqual(wrapper["wrapper_exit_status"], wrapper_exit)
                self.assertEqual(wrapper["signal"], signal_name)
                self.assertEqual(_read_json(root_path / subject.TERMINAL_NAME)["status"], "sealed_fail_waiting_planner_review")
                _remove_scratches(scratches)

    def test_independent_final_zero_failure_changes_only_success_exit(self) -> None:
        with tempfile.TemporaryDirectory() as tempdir, self._runtime(Path(tempdir)):
            root_path = Path(tempdir) / "independent-fail"
            subject.execute_zero_readiness(root_path, dependencies=_dependencies(_FakeStrip(), _FakeRay()))
            scratches = _scratch_files(root_path, shell_exit=0)
            code = subject.finalize_zero_readiness(
                root_path,
                runner_log_source=scratches[0], wrapper_log_source=scratches[1],
                shell_json_source=scratches[2], shell_stderr_source=scratches[3],
                child_exit_status=0, shell_exit_status=0,
                wrapper_status="complete", wrapper_exit_status=0, signal_name=None,
                dependencies=_dependencies(_FakeStrip(failures={0}), _FakeRay()),
            )
            self.assertEqual(code, 71)
            wrapper = _read_json(root_path / "wrapper-result.json")
            self.assertEqual(wrapper["status"], "independent_final_zero_failed")
            self.assertEqual(_read_json(root_path / "independent-final-zero.json")["status"], "fail")
            _remove_scratches(scratches)

    def test_preexisting_or_nonabsolute_root_rejects_before_calls(self) -> None:
        strip = _FakeStrip()
        ray = _FakeRay()
        with tempfile.TemporaryDirectory() as tempdir, self._runtime(Path(tempdir)):
            existing = Path(tempdir) / "existing"
            existing.mkdir(mode=0o700)
            with self.assertRaises(provenance.ProvenanceIOError):
                subject.execute_zero_readiness(existing, dependencies=_dependencies(strip, ray))
            with self.assertRaisesRegex(subject.ZeroReadinessError, "root_scope_invalid"):
                subject.execute_zero_readiness("relative", dependencies=_dependencies(strip, ray))
        self.assertEqual(strip.calls, [])
        self.assertEqual(ray.set_calls, [])

    def test_owner_has_no_parallel_io_capture_or_nonzero_semantics(self) -> None:
        path = Path(subject.__file__)
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source)
        imports = {
            alias.name
            for node in ast.walk(tree)
            if isinstance(node, (ast.Import, ast.ImportFrom))
            for alias in node.names
        }
        self.assertFalse({"json", "os", "stat", "subprocess", "urllib", "socket"} & imports)
        self.assertNotIn("capture_remote_image(", source)
        self.assertNotIn("capture_with_timing(", source)
        self.assertNotIn("write_text(", source)
        self.assertNotIn("write_bytes(", source)
        self.assertNotIn("open(", source)
        self.assertEqual(subject.__all__, [
            "ZeroReadinessError", "execute_zero_readiness", "finalize_zero_readiness", "main",
        ])

    def test_wrapper_has_foreground_owner_traps_and_sibling_scratch_only(self) -> None:
        wrapper = Path(__file__).parents[1] / "tmp/run-g4-zero-readiness.zsh"
        source = wrapper.read_text(encoding="utf-8")
        self.assertIn("trap on_exit EXIT", source)
        self.assertIn("trap 'on_signal INT 2' INT", source)
        self.assertIn("camera_based_rgbww_optimizer.control.all_off", source)
        self.assertIn("--finalize-only", source)
        self.assertIn("rm -f -- \"$RUNNER_SCRATCH\"", source)
        self.assertNotIn("mkdir", source)
        self.assertNotIn(" &\n", source)
        self.assertNotIn(">\"$OUTPUT_ROOT", source)

    def _runtime(self, parent: Path):
        settings = subject.ray120c.OpenAPISettings(
            url=subject.EXPECTED_RAY_URL,
            node_id=subject.EXPECTED_RAY_NODE,
            client_id=subject.EXPECTED_RAY_CLIENT,
            timeout=subject.RAY_TIMEOUT,
        )
        return _PatchGroup(
            mock.patch.object(subject, "EXPECTED_ROOT_PARENT", parent),
            mock.patch.object(subject.ray120c.OpenAPISettings, "from_env", return_value=settings),
        )


class _PatchGroup:
    def __init__(self, *patchers: mock._patch) -> None:
        self.patchers = patchers

    def __enter__(self):
        for patcher in self.patchers:
            patcher.start()
        return self

    def __exit__(self, exc_type, exc, tb):
        for patcher in reversed(self.patchers):
            patcher.stop()


def _dependencies(
    strip: _FakeStrip,
    ray: _FakeRay,
    *,
    camera_probe=None,
) -> subject._RuntimeDependencies:
    return subject._RuntimeDependencies(
        strip_zero=strip,
        ray_set_zero=ray.set,
        ray_get_cct=ray.get,
        ray_get_node=ray.node,
        camera_probe=camera_probe or _camera_probe,
    )


def _camera_probe() -> dict[str, object]:
    return {
        "health_status": "ok",
        "health_keys": ["status"],
        "backend": "remote",
        "model": subject.EXPECTED_CAMERA_MODEL,
        "base_url": subject.EXPECTED_CAMERA_BASE_URL,
        "capability": subject.EXPECTED_CAMERA_CAPABILITY,
        "capture_with_timing_callable": True,
        "config": {
            "iso_current": "100",
            "iso_choice_count": 2,
            "aperture_current": "2.8",
            "aperture_choice_count": 2,
            "shutter_current": "1/2500",
            "shutter_choice_count": 2,
            "image_format": "RAW",
        },
    }


def _snapshot(generation: int) -> dict[str, int]:
    return {"schema_version": 1, "generation": generation, **subject.ZERO_PAYLOAD}


def _ray_response() -> dict[str, object]:
    return {"code": 0, "data": {"cct": 5600, "gm": 100, "intensity": 0}}


def _shell_steps(ok: bool) -> list[dict[str, object]]:
    return [
        {"name": "esphome", "ok": ok, "detail": {"payload": dict(subject.ZERO_PAYLOAD)}, "error": None},
        {
            "name": "ray120c",
            "ok": ok,
            "detail": {"cct": 5600, "gm": 100, "response": _ray_response()},
            "error": None,
        },
    ]


def _scratch_files(root: Path, *, shell_exit: int) -> tuple[Path, Path, Path, Path]:
    paths = tuple(
        root.parent / f".{root.name}.{kind}.scratch"
        for kind in ("runner", "wrapper", "shell-json", "shell-stderr")
    )
    payloads = (
        b"runner complete\n",
        b"wrapper cleanup complete\n",
        json.dumps(_shell_steps(shell_exit == 0), sort_keys=True).encode("utf-8") + b"\n",
        b"" if shell_exit == 0 else b"fake cleanup failure\n",
    )
    for path, payload in zip(paths, payloads, strict=True):
        path.write_bytes(payload)
        path.chmod(0o600)
    return paths


def _remove_scratches(paths: tuple[Path, ...]) -> None:
    for path in paths:
        path.unlink()


def _read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
