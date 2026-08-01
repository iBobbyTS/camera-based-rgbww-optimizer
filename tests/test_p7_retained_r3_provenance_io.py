from __future__ import annotations

import ast
from dataclasses import replace
import errno
import hashlib
import inspect
import json
import os
from pathlib import Path
import stat
import subprocess
import tempfile
from types import SimpleNamespace
import unittest
from unittest import mock

from camera_based_rgbww_optimizer.utils import p7_retained_r3_provenance_io as subject


SAFE_TEMP_BASE = Path("/Volumes/4T/temp/rgbww-optimizer")
SHA_A = "a" * 40
SHA_B = "b" * 40


class ProvenanceIOTests(unittest.TestCase):
    def setUp(self) -> None:
        self.assertTrue(SAFE_TEMP_BASE.is_dir())
        self.assertFalse(SAFE_TEMP_BASE.is_symlink())
        self.temporary = tempfile.TemporaryDirectory(
            prefix="p7-provenance-io-test-", dir=SAFE_TEMP_BASE
        )
        self.case = Path(self.temporary.name)

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def assert_code(self, code: str, function, *args, **kwargs) -> subject.ProvenanceIOError:
        with self.assertRaises(subject.ProvenanceIOError) as raised:
            function(*args, **kwargs)
        self.assertEqual(raised.exception.code, code)
        return raised.exception

    def root(self) -> subject.DirectoryIdentity:
        return subject.create_exclusive_root(self.case / "root")

    def test_exclusive_root_success_and_rejections(self):
        target = self.case / "root"
        identity = subject.create_exclusive_root(target)
        observed = os.lstat(target)
        self.assertEqual(identity, subject.DirectoryIdentity(
            str(target), observed.st_dev, observed.st_ino, 0o700
        ))
        self.assertEqual(stat.S_IMODE(observed.st_mode), 0o700)
        self.assert_code("root_exists", subject.create_exclusive_root, target)

        file_target = self.case / "file"
        file_target.write_bytes(b"x")
        self.assert_code("root_exists", subject.create_exclusive_root, file_target)
        link = self.case / "link"
        link.symlink_to(target, target_is_directory=True)
        self.assert_code("root_exists", subject.create_exclusive_root, link)
        self.assert_code("root_not_absolute", subject.create_exclusive_root, "relative")

    def test_root_identity_type_mode_and_mkdir_drift_fail_closed(self):
        target = self.case / "root"
        real_lstat = os.lstat

        def wrong_mode(path):
            value = real_lstat(path)
            return SimpleNamespace(
                st_mode=stat.S_IFDIR | 0o755, st_dev=value.st_dev,
                st_ino=value.st_ino, st_size=value.st_size,
            )

        self.assert_code(
            "root_mode_mismatch", subject.create_exclusive_root, target,
            dependencies={"lstat": wrong_mode},
        )
        other = self.case / "other"
        other.write_bytes(b"x")
        self.assert_code(
            "root_not_directory", subject.create_exclusive_root, self.case / "fake",
            dependencies={"mkdir": lambda _p, _m: None, "lstat": lambda _p: os.lstat(other)},
        )

    def test_exact_read_success_freezes_all_facts_and_validates_expectations(self):
        root = self.root()
        path = Path(root.path) / "source.json"
        data = b'{"a":1}\n'
        path.write_bytes(data)
        path.chmod(0o640)
        identity = subject.read_exact_file(
            path, expected_mode=0o640, expected_size=len(data),
            expected_sha256=hashlib.sha256(data).hexdigest(), root=root,
        )
        observed = os.lstat(path)
        self.assertEqual(identity.path, str(path))
        self.assertEqual(identity.data, data)
        self.assertEqual(identity.byte_count, len(data))
        self.assertEqual(identity.sha256, hashlib.sha256(data).hexdigest())
        self.assertEqual((identity.device, identity.inode, identity.mode),
                         (observed.st_dev, observed.st_ino, 0o640))
        self.assertEqual(identity.root, root)
        self.assert_code("file_mode_mismatch", subject.read_exact_file, path, expected_mode=0o600)
        self.assert_code("file_size_mismatch", subject.read_exact_file, path, expected_size=99)
        self.assert_code("file_hash_mismatch", subject.read_exact_file, path, expected_sha256="0" * 64)

    def test_exact_read_rejects_symlink_nonregular_and_descriptor_rebind(self):
        path = self.case / "source"
        path.write_bytes(b"abc")
        link = self.case / "link"
        link.symlink_to(path)
        self.assert_code("file_not_regular", subject.read_exact_file, link)
        directory = self.case / "dir"
        directory.mkdir()
        self.assert_code("file_not_regular", subject.read_exact_file, directory)

        real_fstat = os.fstat
        def rebound(fd):
            value = real_fstat(fd)
            return SimpleNamespace(
                st_mode=value.st_mode, st_dev=value.st_dev, st_ino=value.st_ino + 1,
                st_size=value.st_size,
            )
        self.assert_code(
            "file_identity_drift", subject.read_exact_file, path,
            dependencies={"fstat": rebound},
        )

    def test_exact_read_handles_partial_and_eintr_and_closes_once(self):
        path = self.case / "source"
        path.write_bytes(b"abcdef")
        calls = {"read": 0, "close": 0}
        def reader(fd, count):
            calls["read"] += 1
            if calls["read"] in {1, 4}:
                raise OSError(errno.EINTR, "interrupted")
            return os.read(fd, min(count, 2))
        def closer(fd):
            calls["close"] += 1
            os.close(fd)
        identity = subject.read_exact_file(
            path, dependencies={"read_fd": reader, "close_fd": closer}
        )
        self.assertEqual(identity.data, b"abcdef")
        self.assertEqual(calls["close"], 1)
        self.assertGreaterEqual(calls["read"], 5)

    def test_required_open_capabilities_and_exact_flags(self):
        root = self.root()
        source = Path(root.path) / "source"
        source.write_bytes(b"x")
        opened = []

        def opener(path, flags, mode):
            opened.append((Path(path), flags, mode))
            return os.open(path, flags, mode)

        subject.read_exact_file(source, root=root, dependencies={"open_fd": opener})
        self.assertEqual(opened, [(source, os.O_RDONLY | os.O_NOFOLLOW, 0)])
        opened.clear()
        subject.persist_canonical_json(
            root, "target.json", {"x": 1}, dependencies={"open_fd": opener}
        )
        self.assertEqual(
            opened,
            [
                (Path(root.path) / "target.json",
                 os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600),
                (Path(root.path), os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, 0),
                (Path(root.path) / "target.json", os.O_RDONLY | os.O_NOFOLLOW, 0),
            ],
        )

        for name, value in (("O_NOFOLLOW", None), ("O_NOFOLLOW", 0),
                            ("O_NOFOLLOW", "flag"), ("O_DIRECTORY", None),
                            ("O_DIRECTORY", 0), ("O_DIRECTORY", "flag")):
            with self.subTest(name=name, value=value):
                calls = mock.Mock()
                fresh_root = subject.create_exclusive_root(
                    self.case / f"cap-{name}-{type(value).__name__}-{value}"
                )
                with mock.patch.object(os, name, value, create=True):
                    if name == "O_NOFOLLOW":
                        self.assert_code(
                            f"required_open_flag_unavailable:{name}",
                            subject.read_exact_file, source,
                            dependencies={"open_fd": calls},
                        )
                    else:
                        self.assert_code(
                            f"required_open_flag_unavailable:{name}",
                            subject.persist_canonical_json, fresh_root, "x.json", {},
                            dependencies={"open_fd": calls},
                        )
                calls.assert_not_called()
                self.assertFalse((Path(fresh_root.path) / "x.json").exists())

    def test_root_bound_read_requires_exact_lexical_direct_child_pre_lstat(self):
        root = self.root()
        legal = Path(root.path) / "legal"
        legal.write_bytes(b"ok")
        self.assertEqual(subject.read_exact_file(legal, root=root).data, b"ok")
        cases = (
            self.case / "outside",
            Path(root.path) / "nested" / "x",
            str(root.path) + "/./x",
            str(root.path) + "/../x",
            str(root.path) + "//x",
            str(root.path) + "/x\\y",
            "relative",
        )
        for index, candidate in enumerate(cases):
            with self.subTest(candidate=candidate):
                seen = []

                def lstat(path):
                    seen.append(os.fspath(path))
                    return os.lstat(path)

                self.assert_code(
                    "target_not_absolute" if candidate == "relative" else "target_not_direct_child",
                    subject.read_exact_file, candidate, root=root,
                    dependencies={"lstat": lstat},
                )
                self.assertEqual(seen, [root.path])

    def test_failed_read_closes_once_and_close_failure_remains_visible(self):
        path = self.case / "source-failure"
        path.write_bytes(b"abc")
        closes = 0

        def closer(fd):
            nonlocal closes
            closes += 1
            os.close(fd)

        self.assert_code(
            "read_failed", subject.read_exact_file, path,
            dependencies={
                "read_fd": lambda _fd, _count: (_ for _ in ()).throw(OSError("read")),
                "close_fd": closer,
            },
        )
        self.assertEqual(closes, 1)

        def failed_close(fd):
            os.close(fd)
            raise OSError("close")

        error = self.assert_code(
            "close_failed", subject.read_exact_file, path,
            dependencies={
                "read_fd": lambda _fd, _count: (_ for _ in ()).throw(OSError("read")),
                "close_fd": failed_close,
            },
        )
        self.assertIsInstance(error.__cause__, subject.ProvenanceIOError)
        self.assertEqual(error.__cause__.code, "read_failed")

    def test_read_growth_truncation_fstat_drift_and_close_failure_are_visible(self):
        path = self.case / "source"
        path.write_bytes(b"abc")
        self.assert_code(
            "file_truncated", subject.read_exact_file, path,
            dependencies={"read_fd": lambda _fd, _count: b""},
        )

        real_read = os.read
        appended = False
        def growing(fd, count):
            nonlocal appended
            value = real_read(fd, count)
            if not appended:
                with path.open("ab") as stream:
                    stream.write(b"z")
                appended = True
            return value
        self.assert_code(
            "file_grew", subject.read_exact_file, path,
            dependencies={"read_fd": growing},
        )

        path.write_bytes(b"abc")
        real_fstat = os.fstat
        count = 0
        def drifting(fd):
            nonlocal count
            count += 1
            value = real_fstat(fd)
            if count == 2:
                return SimpleNamespace(st_mode=value.st_mode, st_dev=value.st_dev,
                                       st_ino=value.st_ino, st_size=value.st_size + 1)
            return value
        self.assert_code(
            "file_identity_drift", subject.read_exact_file, path,
            dependencies={"fstat": drifting},
        )
        self.assert_code(
            "close_failed", subject.read_exact_file, path,
            dependencies={"close_fd": lambda _fd: (_ for _ in ()).throw(OSError("close"))},
        )

    def test_canonical_json_success_and_detached_immutable_decode(self):
        value = {"色": [1, {"x": True}], "a": 2}
        encoded = subject.canonical_json_bytes(value)
        self.assertEqual(encoded, '{"a":2,"色":[1,{"x":true}]}\n'.encode())
        decoded = subject.decode_canonical_json(encoded)
        value["色"][1]["x"] = False
        self.assertTrue(decoded["色"][1]["x"])
        with self.assertRaises(TypeError):
            decoded["new"] = 3

    def test_canonical_json_rejects_malformed_and_noncanonical_bytes(self):
        cases = (
            (b'{"a":1,"a":2}\n', "json_duplicate_key"),
            (b'{"a":NaN}\n', "json_nonfinite"),
            (b'{"a":Infinity}\n', "json_nonfinite"),
            (b'\xef\xbb\xbf{"a":1}\n', "json_bytes_invalid"),
            (b"\xff\n", "json_decode_failed"),
            (b'{"b":2,"a":1}\n', "json_not_canonical"),
            (b'{"a": 1}\n', "json_not_canonical"),
            (b'{"a":1}', "json_terminal_lf_invalid"),
            (b'{"a":1}\n\n', "json_terminal_lf_invalid"),
            (b'{"a":1}\ntrailing', "json_terminal_lf_invalid"),
        )
        for data, code in cases:
            with self.subTest(data=data):
                self.assert_code(code, subject.decode_canonical_json, data)
        for value in ({"x": float("nan")}, {"x": float("inf")}, {"x": object()}):
            with self.subTest(value=value):
                with self.assertRaises(subject.ProvenanceIOError):
                    subject.canonical_json_bytes(value)

    def test_persist_success_partial_write_eintr_fsync_order_and_reload(self):
        root = self.root()
        calls: list[str] = []
        writes = 0
        def writer(fd, value):
            nonlocal writes
            writes += 1
            calls.append("write")
            if writes == 1:
                raise OSError(errno.EINTR, "interrupted")
            return os.write(fd, value[:2])
        def fsync(fd):
            calls.append("fsync")
            os.fsync(fd)
        def close(fd):
            calls.append("close")
            os.close(fd)
        identity = subject.persist_canonical_json(
            root, "manifest.json", {"b": 2, "a": 1},
            dependencies={"write_fd": writer, "fsync_fd": fsync, "close_fd": close},
        )
        self.assertEqual(identity.data, b'{"a":1,"b":2}\n')
        self.assertEqual(identity.mode, 0o600)
        self.assertEqual(identity.root, root)
        self.assertGreater(writes, 2)
        self.assertEqual(calls.count("fsync"), 2)
        self.assertEqual(calls.count("close"), 3)  # target, root, reload
        self.assertLess(calls.index("fsync"), calls.index("close"))

    def test_persist_rejects_unsafe_existing_and_symlink_targets_without_repair(self):
        root = self.root()
        for name in ("", ".", "..", "a/b", "/abs", "a\\b", "x\x00y"):
            with self.subTest(name=name):
                self.assert_code("unsafe_child", subject.persist_canonical_json, root, name, {})
        target = Path(root.path) / "target.json"
        target.write_bytes(b"preserve")
        self.assert_code("target_exists", subject.persist_canonical_json, root, "target.json", {})
        self.assertEqual(target.read_bytes(), b"preserve")
        target.unlink()
        source = Path(root.path) / "source"
        source.write_bytes(b"preserve")
        target.symlink_to(source)
        self.assert_code("target_exists", subject.persist_canonical_json, root, "target.json", {})
        self.assertTrue(target.is_symlink())
        self.assertEqual(source.read_bytes(), b"preserve")

    def test_persist_failures_preserve_created_target_and_fail_closed(self):
        cases = (
            ("write_no_progress", {"write_fd": lambda _fd, _value: 0}),
            ("file_fsync_failed", {"fsync_fd": lambda _fd: (_ for _ in ()).throw(OSError("fsync"))}),
            ("close_failed", {"close_fd": lambda _fd: (_ for _ in ()).throw(OSError("close"))}),
        )
        for index, (code, dependencies) in enumerate(cases):
            root = subject.create_exclusive_root(self.case / f"root-{index}")
            name = "target.json"
            self.assert_code(code, subject.persist_canonical_json, root, name, {"a": 1}, dependencies=dependencies)
            self.assertTrue((Path(root.path) / name).exists())

    def test_persist_root_identity_and_open_identity_drift_fail_closed(self):
        root = self.root()
        changed = replace(root, inode=root.inode + 1)
        self.assert_code("root_identity_drift", subject.persist_canonical_json, changed, "x.json", {})

        real_fstat = os.fstat
        first = True
        def wrong_mode(fd):
            nonlocal first
            value = real_fstat(fd)
            if first:
                first = False
                return SimpleNamespace(st_mode=stat.S_IFREG | 0o644, st_dev=value.st_dev,
                                       st_ino=value.st_ino, st_size=value.st_size)
            return value
        self.assert_code(
            "file_mode_mismatch", subject.persist_canonical_json, root, "mode.json", {},
            dependencies={"fstat": wrong_mode},
        )

    def test_target_open_and_identity_failures_preserve_physical_state(self):
        root = self.root()
        target = Path(root.path) / "open.json"
        self.assert_code(
            "target_open_failed", subject.persist_canonical_json, root, target.name, {},
            dependencies={"open_fd": lambda *_args: (_ for _ in ()).throw(OSError("open"))},
        )
        self.assertFalse(target.exists())

        for field in ("st_dev", "st_ino"):
            with self.subTest(field=field):
                branch_root = subject.create_exclusive_root(self.case / f"drift-{field}")
                branch_target = Path(branch_root.path) / "target.json"
                real_fstat = os.fstat
                count = 0

                def drifting(fd):
                    nonlocal count
                    count += 1
                    value = real_fstat(fd)
                    if count == 2:
                        values = dict(st_mode=value.st_mode, st_dev=value.st_dev,
                                      st_ino=value.st_ino, st_size=value.st_size)
                        values[field] += 1
                        return SimpleNamespace(**values)
                    return value

                self.assert_code(
                    "target_identity_drift", subject.persist_canonical_json,
                    branch_root, branch_target.name, {"a": 1},
                    dependencies={"fstat": drifting},
                )
                self.assertEqual(branch_target.read_bytes(), b'{"a":1}\n')

    def test_root_lifecycle_failures_preserve_fsynced_target(self):
        for stage in ("open", "fsync", "close"):
            with self.subTest(stage=stage):
                root = subject.create_exclusive_root(self.case / f"root-stage-{stage}")
                target = Path(root.path) / "target.json"
                opens = 0
                fsyncs = 0
                closes = 0

                def opener(path, flags, mode):
                    nonlocal opens
                    opens += 1
                    if stage == "open" and opens == 2:
                        raise OSError("root open")
                    return os.open(path, flags, mode)

                def fsyncer(fd):
                    nonlocal fsyncs
                    fsyncs += 1
                    if stage == "fsync" and fsyncs == 2:
                        raise OSError("root fsync")
                    os.fsync(fd)

                def closer(fd):
                    nonlocal closes
                    closes += 1
                    os.close(fd)
                    if stage == "close" and closes == 2:
                        raise OSError("root close")

                codes = {"open": "root_open_failed", "fsync": "root_fsync_failed",
                         "close": "close_failed"}
                self.assert_code(
                    codes[stage], subject.persist_canonical_json, root, target.name,
                    {"a": 1}, dependencies={"open_fd": opener, "fsync_fd": fsyncer,
                                                "close_fd": closer},
                )
                self.assertEqual(target.read_bytes(), b'{"a":1}\n')
                self.assertGreaterEqual(closes, 1)

    def test_reload_failures_preserve_target_without_second_write(self):
        for stage in ("lstat", "open", "read", "decode"):
            with self.subTest(stage=stage):
                root = subject.create_exclusive_root(self.case / f"reload-{stage}")
                target = Path(root.path) / "target.json"
                real_lstat = os.lstat
                opens = 0
                writes = 0

                def lstat(path):
                    if stage == "lstat" and Path(path) == target and target.exists():
                        raise OSError("reload lstat")
                    return real_lstat(path)

                def opener(path, flags, mode):
                    nonlocal opens
                    opens += 1
                    if stage == "open" and opens == 3:
                        raise OSError("reload open")
                    return os.open(path, flags, mode)

                def writer(fd, value):
                    nonlocal writes
                    writes += 1
                    return os.write(fd, value)

                dependencies = {"lstat": lstat, "open_fd": opener, "write_fd": writer}
                expected = {"lstat": "file_lstat_failed", "open": "file_open_failed",
                            "read": "read_failed", "decode": "decode_failed"}[stage]
                if stage == "read":
                    dependencies["read_fd"] = lambda _fd, _count: (
                        _ for _ in ()
                    ).throw(OSError("reload read"))
                decode = mock.patch.object(
                    subject, "decode_canonical_json",
                    side_effect=subject.ProvenanceIOError("decode_failed"),
                ) if stage == "decode" else mock.patch.object(
                    subject, "decode_canonical_json", wraps=subject.decode_canonical_json,
                )
                with decode:
                    self.assert_code(
                        expected, subject.persist_canonical_json, root, target.name,
                        {"a": 1}, dependencies=dependencies,
                    )
                self.assertEqual(target.read_bytes(), b'{"a":1}\n')
                self.assertEqual(writes, 1)

    def test_target_linkage_binds_every_field_and_is_immutable(self):
        root = self.root()
        path = Path(root.path) / "x"
        path.write_bytes(b"x")
        identity = subject.read_exact_file(path, root=root)
        self.assertIs(subject.require_same_target(identity, identity), identity)
        mutations = {
            "path": identity.path + "x", "data": b"y", "byte_count": 2,
            "sha256": "0" * 64, "device": identity.device + 1,
            "inode": identity.inode + 1, "mode": 0o600,
            "root": replace(root, inode=root.inode + 1),
        }
        for field, value in mutations.items():
            with self.subTest(field=field):
                self.assert_code(
                    "target_identity_mismatch", subject.require_same_target,
                    replace(identity, **{field: value}), identity,
                )
        with self.assertRaises((AttributeError, TypeError)):
            identity.path = "changed"

    def test_all_git_shapes_use_exact_process_contract_and_immutable_ledger(self):
        commands = (
            ("git", "rev-parse", "--verify", SHA_A + "^{commit}"),
            ("git", "show", "-s", "--format=%H%x00%P%x00%s", SHA_A),
            ("git", "diff-tree", "--no-commit-id", "--name-only", "-r", "-z", SHA_A),
            ("git", "rev-parse", SHA_A + ":src/file.py"),
            ("git", "diff", "--binary", "--full-index", "--no-ext-diff", SHA_A, SHA_B, "--", "a", "b/c"),
        )
        for index, argv in enumerate(commands):
            with self.subTest(argv=argv):
                runner = mock.Mock(return_value=SimpleNamespace(
                    returncode=index, stdout=b"out", stderr=b"err"
                ))
                ledger = subject.run_read_only_git(
                    self.case, argv, dependencies={"run_process": runner}
                )
                runner.assert_called_once_with(
                    argv, cwd=str(self.case), shell=False, stdin=subprocess.DEVNULL,
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
                )
                self.assertEqual(ledger.argv, argv)
                self.assertEqual(ledger.exit_code, index)
                self.assertEqual(ledger.stdout, b"out")
                self.assertEqual(ledger.stderr, b"err")
                self.assertEqual(ledger.stdout_sha256, hashlib.sha256(b"out").hexdigest())
                self.assertEqual(ledger.stderr_sha256, hashlib.sha256(b"err").hexdigest())
                with self.assertRaises((AttributeError, TypeError)):
                    ledger.exit_code = 99

    def test_git_grammar_rejects_every_unlisted_or_malformed_shape_before_launch(self):
        denied = (
            ("git", "status"),
            ("git", "reset", "--hard"),
            ("git", "-C", ".", "show"),
            ("git show", SHA_A),
            ("git", "rev-parse", "--verify", SHA_A.upper() + "^{commit}"),
            ("git", "rev-parse", SHA_A + ":../x"),
            ("git", "rev-parse", SHA_A + ":a//b"),
            ("git", "diff", "--binary", "--full-index", "--no-ext-diff", SHA_A, SHA_B, "--", "b", "a"),
            ("git", "diff", "--binary", "--full-index", "--no-ext-diff", SHA_A, SHA_B, "--", "a", "a"),
        )
        for argv in denied:
            with self.subTest(argv=argv):
                runner = mock.Mock()
                self.assert_code(
                    "git_command_denied", subject.run_read_only_git, self.case, argv,
                    dependencies={"run_process": runner},
                )
                runner.assert_not_called()
        self.assert_code("git_argv_invalid", subject.run_read_only_git, self.case, ["git", "status"])

    def test_git_nonzero_is_truthful_while_launch_and_result_failures_are_typed(self):
        argv = ("git", "rev-parse", "--verify", SHA_A + "^{commit}")
        runner = mock.Mock(return_value=SimpleNamespace(returncode=17, stdout=b"", stderr=b"bad"))
        ledger = subject.run_read_only_git(self.case, argv, dependencies={"run_process": runner})
        self.assertEqual((ledger.exit_code, ledger.stderr), (17, b"bad"))
        self.assert_code(
            "git_launch_failed", subject.run_read_only_git, self.case, argv,
            dependencies={"run_process": lambda *_a, **_k: (_ for _ in ()).throw(OSError("launch"))},
        )
        self.assert_code(
            "git_result_invalid", subject.run_read_only_git, self.case, argv,
            dependencies={"run_process": lambda *_a, **_k: SimpleNamespace(returncode=0, stdout="text", stderr=b"")},
        )

    def test_dependency_overrides_fail_closed_and_inputs_are_not_mutated(self):
        overrides = {"read_fd": os.read}
        path = self.case / "x"
        path.write_bytes(b"x")
        subject.read_exact_file(path, dependencies=overrides)
        self.assertEqual(overrides, {"read_fd": os.read})
        self.assert_code("unknown_dependency", subject.read_exact_file, path, dependencies={"unknown": lambda: None})
        self.assert_code("noncallable_dependency", subject.read_exact_file, path, dependencies={"read_fd": None})

    def test_existing_root_public_signature_export_and_exact_identity(self):
        signature = inspect.signature(subject.read_existing_root)
        self.assertEqual(tuple(signature.parameters), ("path", "dependencies"))
        self.assertEqual(signature.parameters["dependencies"].kind, inspect.Parameter.KEYWORD_ONLY)
        self.assertIn("read_existing_root", subject.__all__)

        calls = {name: mock.Mock() for name in (
            "mkdir", "open_fd", "fstat", "read_fd", "write_fd", "fsync_fd",
            "close_fd", "run_process",
        )}
        observed = SimpleNamespace(
            st_mode=stat.S_IFDIR | 0o700, st_dev=17, st_ino=29, st_size=0,
        )
        lstat = mock.Mock(return_value=observed)
        identity = subject.read_existing_root(
            "/evidence/root", dependencies={"lstat": lstat, **calls}
        )
        self.assertEqual(
            identity, subject.DirectoryIdentity("/evidence/root", 17, 29, 0o700)
        )
        self.assertIs(type(identity), subject.DirectoryIdentity)
        lstat.assert_called_once_with(Path("/evidence/root"))
        for capability in calls.values():
            capability.assert_not_called()

    def test_existing_root_invalid_absolute_and_canonical_matrix_pre_lstat(self):
        cases = (
            (object(), "invalid_path"),
            (b"/bytes", "invalid_path"),
            ("/root\x00tail", "invalid_path"),
            ("relative", "root_not_absolute"),
            ("//root", "root_not_canonical"),
            ("/root/", "root_not_canonical"),
            ("/root/.", "root_not_canonical"),
            ("/root/..", "root_not_canonical"),
            ("/root//child", "root_not_canonical"),
            ("/root\\child", "root_not_canonical"),
        )
        for candidate, code in cases:
            with self.subTest(candidate=candidate):
                lstat = mock.Mock()
                self.assert_code(
                    code, subject.read_existing_root, candidate,
                    dependencies={"lstat": lstat},
                )
                lstat.assert_not_called()

    def test_existing_root_lstat_type_and_mode_failures_are_exact_and_read_only(self):
        failures = (
            (FileNotFoundError("missing"), "root_lstat_failed"),
            (PermissionError("denied"), "root_lstat_failed"),
            (SimpleNamespace(st_mode=stat.S_IFLNK | 0o700, st_dev=1, st_ino=2), "root_not_directory"),
            (SimpleNamespace(st_mode=stat.S_IFREG | 0o700, st_dev=1, st_ino=2), "root_not_directory"),
            (SimpleNamespace(st_mode=stat.S_IFIFO | 0o700, st_dev=1, st_ino=2), "root_not_directory"),
            (SimpleNamespace(st_mode=stat.S_IFDIR | 0o755, st_dev=1, st_ino=2), "root_mode_mismatch"),
        )
        for index, (result, code) in enumerate(failures):
            with self.subTest(index=index, code=code):
                lstat = mock.Mock(
                    side_effect=result if isinstance(result, OSError) else None,
                    return_value=None if isinstance(result, OSError) else result,
                )
                forbidden = {name: mock.Mock() for name in (
                    "mkdir", "open_fd", "fstat", "read_fd", "write_fd",
                    "fsync_fd", "close_fd", "run_process",
                )}
                self.assert_code(
                    code, subject.read_existing_root, f"/evidence/root-{index}",
                    dependencies={"lstat": lstat, **forbidden},
                )
                lstat.assert_called_once_with(Path(f"/evidence/root-{index}"))
                for capability in forbidden.values():
                    capability.assert_not_called()

    def test_existing_root_identity_feeds_direct_read_and_fresh_drift_revalidation(self):
        target = self.case / "existing-root"
        target.mkdir(mode=0o700)
        target.chmod(0o700)
        child = target / "artifact.json"
        child.write_bytes(b'{}\n')
        child.chmod(0o600)
        identity = subject.read_existing_root(target)
        value = subject.read_exact_file(child, expected_mode=0o600, root=identity)
        self.assertEqual((value.data, value.root), (b'{}\n', identity))

        observed = os.lstat(target)
        failures = (
            (SimpleNamespace(st_mode=observed.st_mode, st_dev=observed.st_dev + 1,
                             st_ino=observed.st_ino, st_size=observed.st_size), "root_identity_drift"),
            (SimpleNamespace(st_mode=observed.st_mode, st_dev=observed.st_dev,
                             st_ino=observed.st_ino + 1, st_size=observed.st_size), "root_identity_drift"),
            (SimpleNamespace(st_mode=stat.S_IFDIR | 0o755, st_dev=observed.st_dev,
                             st_ino=observed.st_ino, st_size=observed.st_size), "root_mode_mismatch"),
            (SimpleNamespace(st_mode=stat.S_IFLNK | 0o700, st_dev=observed.st_dev,
                             st_ino=observed.st_ino, st_size=observed.st_size), "root_not_directory"),
        )
        for replacement, code in failures:
            with self.subTest(code=code, replacement=replacement):
                opened = mock.Mock()
                lstats = mock.Mock(return_value=replacement)
                self.assert_code(
                    code, subject.read_exact_file, child, root=identity,
                    dependencies={"lstat": lstats, "open_fd": opened},
                )
                lstats.assert_called_once_with(Path(identity.path))
                opened.assert_not_called()

    def test_ast_import_and_capability_guard(self):
        source_path = Path(subject.__file__)
        source = source_path.read_text(encoding="utf-8")
        tree = ast.parse(source)
        imports = {
            alias.name
            for node in ast.walk(tree) if isinstance(node, ast.Import)
            for alias in node.names
        }
        imported_from = {
            node.module or "" for node in ast.walk(tree) if isinstance(node, ast.ImportFrom)
        }
        forbidden = ("socket", "urllib", "requests", "camera", "ray120c", "esphome",
                     "p7_retained_release_audit", "controller_preparation")
        joined = "\n".join(sorted(imports | imported_from))
        for token in forbidden:
            self.assertNotIn(token, joined)
        self.assertNotIn("os.environ", source)
        self.assertNotIn("shell=True", source)
        self.assertNotIn("tempfile", source)
        self.assertNotIn("/Volumes/", source)
        self.assertNotIn("git reset", source)


if __name__ == "__main__":
    unittest.main()
