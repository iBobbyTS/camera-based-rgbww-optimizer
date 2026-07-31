from __future__ import annotations

import ast
from dataclasses import FrozenInstanceError, replace
import errno
import hashlib
import inspect
import os
from pathlib import Path
import stat
import subprocess
import tempfile
from types import SimpleNamespace
import unittest

from camera_based_rgbww_optimizer.utils import p7_retained_r3_controller_runtime as subject
from camera_based_rgbww_optimizer.utils.p7_retained_r3_controller_conformance import (
    ControllerConformanceError,
    ControllerConformanceReport,
    analyze_controller_source,
)
from camera_based_rgbww_optimizer.utils.p7_retained_r3_provenance_io import FileIdentity


SAFE_TEMP_BASE = Path("/Volumes/4T/temp/rgbww-optimizer")


def template(*, reflection: bool = False, returncode: bool = False) -> bytes:
    access = "getattr(ledger, 'exit_code')" if reflection else (
        "ledger.returncode" if returncode else "ledger.exit_code"
    )
    return f"""\
def require_payload(value):
    assert value

def controller():
    payload = {{'old': 1}}
    require_payload(payload)
    ledger = GitLedger(argv=('git', 'status'), cwd='/repo', exit_code=0, stdout=b'', stderr=b'', stdout_sha256='{'0' * 64}', stderr_sha256='{'0' * 64}')
    assert {access} == 0
""".encode()


class ControllerRuntimeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.assertTrue(SAFE_TEMP_BASE.is_dir())
        self.temporary = tempfile.TemporaryDirectory(prefix="p7-runtime-test-", dir=SAFE_TEMP_BASE)
        self.case = Path(self.temporary.name)

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def request(self, *, name: str = "controller.py", source: bytes | None = None):
        return subject.ControllerRuntimeRequest(
            template_source=source or template(),
            assignment_name="payload",
            validation_function="require_payload",
            replacement_statement=b"payload = {'new': 2}",
            source_path=str(self.case / name),
            process_argv=("python3", "-"),
        )

    def assert_code(self, code: str, function, *args, **kwargs):
        with self.assertRaises(subject.ControllerRuntimeError) as raised:
            function(*args, **kwargs)
        self.assertEqual(raised.exception.code, code)

    def test_01_identical_immutable_request_composes_deterministic_valid_source_and_report(self):
        request = self.request()
        first = subject.compose_controller_source(request)
        second = subject.compose_controller_source(request)
        self.assertEqual(first, second)
        self.assertEqual(first.source_sha256, hashlib.sha256(first.source).hexdigest())
        self.assertEqual(first.byte_count, len(first.source))
        text = first.source.decode("utf-8", errors="strict")
        tree = ast.parse(text)
        self.assertIsNotNone(compile(tree, "<runtime-test>", "exec"))
        self.assertIn("payload = {'new': 2}", text)
        with self.assertRaises(FrozenInstanceError):
            first.source_path = "/changed"

    def test_02_existing_analyzer_rejects_reflection_before_every_effect(self):
        counters = {"analyze": 0, "open": 0, "read": 0, "run": 0}

        def analyze(data):
            counters["analyze"] += 1
            return analyze_controller_source(data)

        def forbidden(name):
            def invoke(*_args, **_kwargs):
                counters[name] += 1
                raise AssertionError(name)
            return invoke

        self.assert_code(
            "source_conformance_failed",
            subject.execute_controller_runtime,
            self.request(source=template(reflection=True)),
            dependencies={
                "analyze_source": analyze,
                "open_fd": forbidden("open"),
                "read_source": forbidden("read"),
                "run_process": forbidden("run"),
            },
        )
        self.assertEqual(counters, {"analyze": 1, "open": 0, "read": 0, "run": 0})

    def test_03_writer_proves_flags_partial_eintr_fsync_order_identity_and_readback(self):
        request = self.request()
        events = []
        writes = 0

        def opener(path, flags, mode):
            events.append(("open", Path(path), flags, mode))
            return os.open(path, flags, mode)

        def writer(fd, data):
            nonlocal writes
            writes += 1
            if writes == 1:
                raise OSError(errno.EINTR, "interrupted")
            events.append(("write", len(data)))
            return os.write(fd, data[:7])

        def syncer(fd):
            events.append(("fsync", stat.S_ISDIR(os.fstat(fd).st_mode)))
            os.fsync(fd)

        def closer(fd):
            events.append(("close", stat.S_ISDIR(os.fstat(fd).st_mode)))
            os.close(fd)

        processes = []

        def run(argv, **kwargs):
            processes.append((argv, kwargs))
            return subprocess.CompletedProcess(argv, 0, b"ok", b"")

        result = subject.execute_controller_runtime(
            request,
            dependencies={"open_fd": opener, "write_fd": writer, "fsync_fd": syncer,
                          "close_fd": closer, "run_process": run},
        )
        expected_flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW
        self.assertEqual(events[0], ("open", Path(request.source_path), expected_flags, 0o600))
        file_fsync = events.index(("fsync", False))
        file_close = events.index(("close", False))
        parent_open = next(i for i, item in enumerate(events) if item[0] == "open" and item[1] == self.case)
        parent_fsync = events.index(("fsync", True))
        self.assertLess(file_fsync, file_close)
        self.assertLess(file_close, parent_open)
        self.assertLess(parent_open, parent_fsync)
        self.assertGreater(writes, 2)
        observed = os.lstat(request.source_path)
        self.assertEqual(stat.S_IMODE(observed.st_mode), 0o600)
        self.assertEqual(result.source_identity.data, result.composition.source)
        self.assertEqual(result.source_identity.sha256, result.composition.source_sha256)
        self.assertEqual(len(processes), 1)

    def test_04_writer_failure_matrix_is_fail_closed_without_launch_rewrite_delete_or_repair(self):
        launch = []
        existing = self.case / "existing.py"
        existing.write_bytes(b"preserve")
        link = self.case / "link.py"
        link.symlink_to(existing)

        cases = [
            ("existing", self.request(name="existing.py"), {}, "source_open_failed"),
            ("symlink", self.request(name="link.py"), {}, "source_open_failed"),
            ("no_progress", self.request(name="zero.py"), {"write_fd": lambda _fd, _data: 0}, "source_write_no_progress"),
            ("file_fsync", self.request(name="file-fsync.py"), {"fsync_fd": lambda _fd: (_ for _ in ()).throw(OSError("fsync"))}, "source_file_fsync_failed"),
        ]
        for name, request, changes, code in cases:
            with self.subTest(name=name):
                self.assert_code(
                    code, subject.execute_controller_runtime, request,
                    dependencies={**changes, "run_process": lambda *_a, **_k: launch.append(name)},
                )

        parent_target = self.request(name="parent-fsync.py")
        fsync_calls = 0

        def parent_fsync(fd):
            nonlocal fsync_calls
            fsync_calls += 1
            if stat.S_ISDIR(os.fstat(fd).st_mode):
                raise OSError("parent fsync")
            os.fsync(fd)

        self.assert_code(
            "parent_fsync_failed", subject.execute_controller_runtime, parent_target,
            dependencies={"fsync_fd": parent_fsync, "run_process": lambda *_a, **_k: launch.append("parent")},
        )

        drift_target = self.request(name="drift.py")

        def drift_read(path, **_kwargs):
            value = os.lstat(path)
            data = Path(path).read_bytes()
            return FileIdentity(str(path), data + b"x", len(data) + 1,
                                hashlib.sha256(data + b"x").hexdigest(),
                                value.st_dev, value.st_ino, 0o600)

        self.assert_code(
            "source_identity_drift", subject.execute_controller_runtime, drift_target,
            dependencies={"read_source": drift_read, "run_process": lambda *_a, **_k: launch.append("drift")},
        )
        self.assertEqual(existing.read_bytes(), b"preserve")
        self.assertTrue(link.is_symlink())
        self.assertEqual(launch, [])

    def test_05_launcher_uses_verified_bytes_once_and_freezes_truthful_result(self):
        calls = []

        def run(argv, **kwargs):
            calls.append((argv, kwargs))
            return subprocess.CompletedProcess(argv, 7, b"stdout", b"stderr")

        result = subject.execute_controller_runtime(self.request(), dependencies={"run_process": run})
        self.assertEqual(len(calls), 1)
        argv, kwargs = calls[0]
        self.assertEqual(argv, ("python3", "-"))
        self.assertEqual(kwargs["input"], result.source_identity.data)
        self.assertNotIn("stdin", kwargs)
        self.assertIs(kwargs["shell"], False)
        self.assertIs(kwargs["check"], False)
        self.assertEqual((result.process.exit_code, result.process.stdout, result.process.stderr),
                         (7, b"stdout", b"stderr"))
        with self.assertRaises(FrozenInstanceError):
            result.process.exit_code = 0

        for name, callback, code in (
            ("invalid", lambda *_a, **_k: SimpleNamespace(returncode="0", stdout=b"", stderr=b""), "controller_result_invalid"),
            ("exception", lambda *_a, **_k: (_ for _ in ()).throw(OSError("launch")), "controller_launch_failed"),
        ):
            with self.subTest(name=name):
                request = self.request(name=f"{name}.py")
                attempts = []

                def once(*args, _callback=callback, **kwargs):
                    attempts.append(1)
                    return _callback(*args, **kwargs)

                self.assert_code(code, subject.execute_controller_runtime, request,
                                 dependencies={"run_process": once})
                self.assertEqual(attempts, [1])

    def test_06_token_contract_existing_analyzer_is_single_owner_and_static_boundary_is_narrow(self):
        calls = []

        def analyze(data):
            calls.append(data)
            return analyze_controller_source(data)

        result = subject.execute_controller_runtime(
            self.request(), dependencies={"analyze_source": analyze,
                                          "run_process": lambda argv, **_kwargs: subprocess.CompletedProcess(argv, 0, b"", b"")},
        )
        self.assertEqual(len(calls), 1)
        self.assertIn(("ledger", "exit_code"), result.conformance.attribute_uses)

        for source, code in ((template(returncode=True), "git_returncode_rejected"),
                             (template(reflection=True), "reflection_rejected")):
            with self.subTest(code=code), self.assertRaises(ControllerConformanceError) as raised:
                analyze_controller_source(subject.compose_controller_source(self.request(name=f"{code}.py", source=source)).source)
            self.assertEqual(raised.exception.code, code)

        source_text = inspect.getsource(subject)
        tree = ast.parse(source_text)
        imported = {
            alias.name for node in tree.body if isinstance(node, (ast.Import, ast.ImportFrom))
            for alias in node.names
        }
        self.assertNotIn("re", imported)
        self.assertNotIn("json", imported)
        self.assertNotIn("socket", imported)
        self.assertNotIn("requests", imported)
        self.assertEqual(source_text.count("analyze_controller_source"), 2)
        self.assertNotIn("execute_controller_lifecycle", source_text)
        self.assertNotIn("canonical_validator", source_text)
        self.assertNotIn("retained_artifact", source_text)


if __name__ == "__main__":
    unittest.main()
