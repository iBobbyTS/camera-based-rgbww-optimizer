from __future__ import annotations

import hashlib
import json
import math
import os
import stat
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from camera_based_rgbww_optimizer.optimization import p7_retained_release_audit as subject


SAFE_TEMP_BASE = Path("/Volumes/4T/temp/rgbww-optimizer")


def _canonical(value: object) -> bytes:
    return (
        json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
            allow_nan=False,
        ).encode("utf-8")
        + b"\n"
    )


def _pass_callback(*_payloads: object) -> dict[str, object]:
    return {"status": "pass", "identity": "synthetic-test"}


class RetainedReleaseAuditTests(unittest.TestCase):
    def setUp(self) -> None:
        self.assertTrue(SAFE_TEMP_BASE.is_dir())
        self.assertFalse(SAFE_TEMP_BASE.is_symlink())
        self.temporary = tempfile.TemporaryDirectory(
            prefix="p7-retained-audit-test-", dir=SAFE_TEMP_BASE
        )
        self.case = Path(self.temporary.name)
        self.base = self.case / "base"
        self.base.mkdir(mode=0o700)
        self.source = self.case / "source"
        self.source.mkdir(mode=0o700)
        self._write_valid_sources()

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def _write_valid_sources(
        self,
        *,
        candidate_mutator=None,
        resolved_mutator=None,
        release_mutator=None,
    ) -> None:
        checkpoint = "1" * 40
        resolved = {
            "schema": "p7_td_b_resolved_formal_plan_v1",
            "status": "formal_plan_resolved",
            "code_checkpoint": checkpoint,
        }
        if resolved_mutator:
            resolved_mutator(resolved)
        resolved_bytes = _canonical(resolved)
        release = {
            "schema": "p7_td_b_setup_lineage_release_v1",
            "status": "formal_plan_resolved",
            "code_checkpoint": checkpoint,
            "resolved_formal_plan": {
                "path": "resolved-formal-plan.json",
                "sha256": hashlib.sha256(resolved_bytes).hexdigest(),
            },
        }
        if release_mutator:
            release_mutator(release)
        release_bytes = _canonical(release)
        rows = [
            {
                "path": f"synthetic/path-{index:02d}.json",
                "classification": "bounded_validation_or_documentation",
            }
            for index in range(59)
        ]
        candidate = {
            "schema": "p7_td_b_current_lineage_candidate_v1",
            "status": "eligible",
            "code_checkpoint": checkpoint,
            "changed_paths": rows,
            "prohibited_paths": [],
            "resolved_formal_plan": {
                "path": "resolved-formal-plan.json",
                "sha256": hashlib.sha256(resolved_bytes).hexdigest(),
            },
            "setup_lineage_release": {
                "path": "setup-lineage-release.json",
                "sha256": hashlib.sha256(release_bytes).hexdigest(),
            },
        }
        if candidate_mutator:
            candidate_mutator(candidate)
        payloads = {
            "current-lineage-candidate.json": _canonical(candidate),
            "resolved-formal-plan.json": resolved_bytes,
            "setup-lineage-release.json": release_bytes,
        }
        for name, data in payloads.items():
            (self.source / name).write_bytes(data)

    def _run(
        self,
        *,
        family: str = "family",
        run: str = "run",
        source: Path | None = None,
        validator=_pass_callback,
        consumer=_pass_callback,
        overrides: dict[str, object] | None = None,
        accounting: dict[str, object] | None = None,
    ) -> dict[str, object]:
        return subject.run_retained_release_audit(
            trusted_base=self.base,
            family_name=family,
            run_name=run,
            source_dir=source or self.source,
            semantic_validator=validator,
            semantic_consumer=consumer,
            execution_accounting=accounting or {"fixture": "synthetic"},
            dependency_overrides=overrides,
        )

    def _assert_failure(self, **kwargs) -> subject.RetainedReleaseAuditError:
        with self.assertRaises(subject.RetainedReleaseAuditError) as raised:
            self._run(**kwargs)
        return raised.exception

    def _rewrite_canonical(self, path: Path, mutator) -> None:
        value = json.loads(path.read_text(encoding="utf-8"))
        mutator(value)
        path.write_bytes(_canonical(value))

    def test_positive_exact_lifecycle_persists_canonical_terminal_bundle(self) -> None:
        calls = {"validator": 0, "consumer": 0}

        def validator(*payloads):
            calls["validator"] += 1
            self.assertEqual(len(payloads[0]["changed_paths"]), 59)
            self.assertIsInstance(payloads[0]["changed_paths"][0], dict)
            return {"status": "pass", "owner": "validator"}

        def consumer(*payloads):
            calls["consumer"] += 1
            self.assertEqual(payloads[1]["code_checkpoint"], payloads[2]["code_checkpoint"])
            return {"status": "pass", "owner": "consumer"}

        result = self._run(validator=validator, consumer=consumer)
        root = Path(result["root"])
        self.assertEqual(result["status"], "pass")
        self.assertEqual(calls, {"validator": 1, "consumer": 1})
        self.assertEqual(stat.S_IMODE(root.parent.stat().st_mode), 0o700)
        self.assertEqual(stat.S_IMODE(root.stat().st_mode), 0o700)
        for name in (*subject.PROGRESSIVE_NAMES, subject.TERMINAL_NAME):
            path = root / name
            data = path.read_bytes()
            self.assertEqual(stat.S_IMODE(path.stat().st_mode), 0o600)
            self.assertTrue(data.endswith(b"\n"))
            self.assertEqual(_canonical(json.loads(data)), data)
        terminal = json.loads((root / subject.TERMINAL_NAME).read_bytes())
        self.assertEqual(
            [item["path"] for item in terminal["artifact_references"]],
            list(subject.PROGRESSIVE_NAMES),
        )
        self.assertNotIn(subject.TERMINAL_NAME, {
            item["path"] for item in terminal["artifact_references"]
        })
        self.assertEqual(subject._replay_terminal_bundle(root)["mismatches"], [])

    def test_missing_intermediate_parent_and_child_are_each_acquired_once(self) -> None:
        mkdir_calls: list[tuple[str, int]] = []

        def mkdir(path, mode):
            mkdir_calls.append((Path(path).name, mode))
            os.mkdir(path, mode)

        result = self._run(overrides={"mkdir": mkdir})
        self.assertEqual(result["status"], "pass")
        self.assertEqual(mkdir_calls, [("family", 0o700), ("run", 0o700)])

    def test_noncallable_dependency_or_callback_fails_before_mutation(self) -> None:
        for kwargs in (
            {"overrides": {"write_fd": None}},
            {"validator": None},
            {"consumer": None},
        ):
            with self.subTest(kwargs=sorted(kwargs)):
                self._assert_failure(family=f"family-{len(list(self.base.iterdir()))}", **kwargs)
        self.assertEqual(list(self.base.iterdir()), [])

    def test_semantic_proxy_dependencies_ignore_module_metadata(self) -> None:
        class Proxy:
            __module__ = "synthetic.proxy"

            def __init__(self, target):
                self.target = target

            def __call__(self, *args, **kwargs):
                return self.target(*args, **kwargs)

        result = self._run(
            overrides={
                "path": Proxy(Path),
                "lstat": Proxy(os.lstat),
                "mkdir": Proxy(lambda path, mode: os.mkdir(path, mode)),
                "open_fd": Proxy(os.open),
                "write_fd": Proxy(os.write),
                "fsync_fd": Proxy(os.fsync),
                "close_fd": Proxy(os.close),
                "sha256": Proxy(hashlib.sha256),
                "json_dumps": Proxy(json.dumps),
                "json_loads": Proxy(json.loads),
                "is_dir": Proxy(stat.S_ISDIR),
                "is_regular": Proxy(stat.S_ISREG),
            }
        )
        dependency = json.loads(
            (Path(result["root"]) / subject.PROGRESSIVE_NAMES[1]).read_bytes()
        )
        self.assertEqual(dependency["metadata_provenance_gates"], 0)

    def test_direct_child_names_reject_escape_without_mutation(self) -> None:
        bad_names = ("", ".", "..", "a/b", r"a\b", "/absolute")
        for index, value in enumerate(bad_names):
            with self.subTest(value=value):
                kwargs = {"family": value, "run": "run"} if index % 2 == 0 else {
                    "family": f"family-{index}",
                    "run": value,
                }
                self._assert_failure(**kwargs)
        self.assertEqual(list(self.base.iterdir()), [])

    def test_base_parent_and_child_path_attacks_fail_closed(self) -> None:
        outside = self.case / "outside"
        outside.mkdir()
        base_link = self.case / "base-link"
        base_link.symlink_to(self.base, target_is_directory=True)
        with self.assertRaises(subject.RetainedReleaseAuditError):
            subject.run_retained_release_audit(
                trusted_base=base_link,
                family_name="family-link",
                run_name="run",
                source_dir=self.source,
                semantic_validator=_pass_callback,
                semantic_consumer=_pass_callback,
            )
        (self.base / "preexisting").mkdir()
        self._assert_failure(family="preexisting")
        (self.base / "preexisting").rmdir()

        def parent_with_child_link(path, mode):
            os.mkdir(path, mode)
            (Path(path) / "run").symlink_to(outside, target_is_directory=True)

        failure = self._assert_failure(
            family="child-link", overrides={"mkdir": parent_with_child_link}
        )
        self.assertIsNone(failure.root)
        self.assertFalse((outside / subject.PROGRESSIVE_NAMES[0]).exists())

    def test_non_directory_wrong_mode_and_identity_drift_fail_closed(self) -> None:
        file_base = self.case / "file-base"
        file_base.write_text("x")
        with self.assertRaises(subject.RetainedReleaseAuditError):
            subject.run_retained_release_audit(
                trusted_base=file_base,
                family_name="family",
                run_name="run",
                source_dir=self.source,
                semantic_validator=_pass_callback,
                semantic_consumer=_pass_callback,
            )

        def wrong_mode(path, _mode):
            os.mkdir(path, 0o755)

        self._assert_failure(family="wrong-mode", overrides={"mkdir": wrong_mode})

        triggered = {"done": False}

        def drift(phase, context):
            if phase == "before_write:01-dependency-audit.json" and not triggered["done"]:
                triggered["done"] = True
                root = context["root"]
                moved = root.with_name("moved-root")
                root.rename(moved)
                root.mkdir(mode=0o700)

        failure = self._assert_failure(
            family="identity-drift", overrides={"phase_hook": drift}
        )
        self.assertIsNotNone(failure.root)
        self.assertIsNotNone(failure.seal_failure)

    def test_device_identity_drift_is_rejected(self) -> None:
        calls: dict[str, int] = {}

        class StatProxy:
            def __init__(self, actual, device):
                self.st_mode = actual.st_mode
                self.st_dev = device
                self.st_ino = actual.st_ino

        def lstat(path):
            actual = os.lstat(path)
            key = str(path)
            calls[key] = calls.get(key, 0) + 1
            if Path(path).name == "run" and calls[key] >= 2:
                return StatProxy(actual, actual.st_dev + 1)
            return actual

        failure = self._assert_failure(
            family="device-drift", overrides={"lstat": lstat}
        )
        self.assertIsNotNone(failure.root)

    def test_source_symlink_nonregular_and_mutation_fail_closed(self) -> None:
        target = self.case / "candidate-target"
        candidate = self.source / subject.SOURCE_NAMES[0]
        candidate.rename(target)
        candidate.symlink_to(target)
        self._assert_failure(family="source-link")
        candidate.unlink()
        target.rename(candidate)

        resolved = self.source / subject.SOURCE_NAMES[1]
        resolved.unlink()
        resolved.mkdir()
        self._assert_failure(family="source-directory")
        resolved.rmdir()
        self._write_valid_sources()

        def mutate(phase, _context):
            if phase == "before_source_after_snapshot":
                with (self.source / subject.SOURCE_NAMES[0]).open("ab") as handle:
                    handle.write(b" ")

        failure = self._assert_failure(
            family="source-mutation", overrides={"phase_hook": mutate}
        )
        terminal = json.loads((failure.root / subject.TERMINAL_NAME).read_bytes())
        self.assertEqual(terminal["status"], "fail")
        self.assertIn("source identity drifted", terminal["primary_failure"]["message"])

    def test_reference_hash_and_source_strict_json_tamper_fail_closed(self) -> None:
        self._write_valid_sources(
            candidate_mutator=lambda value: value["resolved_formal_plan"].update(
                sha256="0" * 64
            )
        )
        self._assert_failure(family="hash-tamper")
        malformed_cases = {
            "duplicate": b'{"schema":"x","schema":"y"}\n',
            "nan": b'{"value":NaN}\n',
            "array": b"[]\n",
            "trailing": b'{"value":1} trailing\n',
            "decode": b"\xff\n",
        }
        for index, (name, data) in enumerate(malformed_cases.items()):
            with self.subTest(name=name):
                self._write_valid_sources()
                (self.source / subject.SOURCE_NAMES[0]).write_bytes(data)
                self._assert_failure(family=f"strict-{index}")

    def test_exclusive_writer_failures_preserve_no_overwrite_contract(self) -> None:
        marker = _canonical({"preexisting": True})

        def precreate(phase, context):
            if phase == "after_root_acquisition":
                path = context["root"] / subject.PROGRESSIVE_NAMES[0]
                path.write_bytes(marker)
                path.chmod(0o600)

        failure = self._assert_failure(
            family="preexisting-output", overrides={"phase_hook": precreate}
        )
        self.assertEqual(
            (failure.root / subject.PROGRESSIVE_NAMES[0]).read_bytes(), marker
        )

        def zero_write(_fd, _data):
            return 0

        short = self._assert_failure(
            family="short-write", overrides={"write_fd": zero_write}
        )
        self.assertIsNotNone(short.root)
        self.assertIsNotNone(short.seal_failure)

        fsync_calls = {"count": 0}

        def fail_fsync(fd):
            fsync_calls["count"] += 1
            raise OSError("synthetic fsync failure")

        fsync = self._assert_failure(
            family="fsync-failure", overrides={"fsync_fd": fail_fsync}
        )
        self.assertEqual(fsync_calls["count"], 2)
        self.assertIsNotNone(fsync.primary)
        self.assertIsNotNone(fsync.seal_failure)

        def fail_close(fd):
            os.close(fd)
            raise OSError("synthetic close failure")

        close = self._assert_failure(
            family="close-failure", overrides={"close_fd": fail_close}
        )
        self.assertIsNotNone(close.seal_failure)

    def test_encode_nan_and_post_write_verification_failures_are_hard(self) -> None:
        nan_failure = self._assert_failure(
            family="nan-encode", accounting={"not_finite": math.nan}
        )
        self.assertIsInstance(nan_failure.primary, ValueError)

        corrupted = {"done": False}

        def corrupt_fsync(fd):
            os.fsync(fd)
            if not corrupted["done"]:
                corrupted["done"] = True
                os.lseek(fd, 0, os.SEEK_SET)
                os.write(fd, b"!")

        verification = self._assert_failure(
            family="verification-failure", overrides={"fsync_fd": corrupt_fsync}
        )
        self.assertIn("persisted bytes differ", str(verification.primary))

    def test_changed_path_adversarial_matrix(self) -> None:
        mutators = {
            "string-row": lambda c: c["changed_paths"].__setitem__(0, "not-a-row"),
            "not-59": lambda c: c["changed_paths"].pop(),
            "missing-key": lambda c: c["changed_paths"][0].pop("classification"),
            "extra-key": lambda c: c["changed_paths"][0].update(extra="x"),
            "empty-path": lambda c: c["changed_paths"][0].update(path=""),
            "empty-class": lambda c: c["changed_paths"][0].update(classification=""),
            "unsorted": lambda c: c["changed_paths"].reverse(),
            "duplicate": lambda c: c["changed_paths"].__setitem__(
                1, dict(c["changed_paths"][0])
            ),
            "absolute": lambda c: c["changed_paths"][0].update(path="/absolute"),
            "traversal": lambda c: c["changed_paths"][0].update(path="../escape"),
            "prohibited": lambda c: c.update(prohibited_paths=["blocked"]),
        }
        for index, (name, mutator) in enumerate(mutators.items()):
            with self.subTest(name=name):
                self._write_valid_sources(candidate_mutator=mutator)
                self._assert_failure(family=f"changed-{index}")

    def test_exact_59_dict_rows_are_never_hashed_as_rows(self) -> None:
        class UnhashableDict(dict):
            __hash__ = None

        original = subject._strict_json_load

        def wrapped(data, dependencies):
            value = original(data, dependencies)
            if "changed_paths" in value:
                value["changed_paths"] = [
                    UnhashableDict(row) for row in value["changed_paths"]
                ]
            return value

        with mock.patch.object(subject, "_strict_json_load", side_effect=wrapped):
            result = self._run(family="unhashable-dicts")
        self.assertEqual(result["status"], "pass")

    def test_artifact_schema_status_checkpoint_and_reference_matrix(self) -> None:
        cases = (
            ("candidate-schema", {"candidate_mutator": lambda v: v.update(schema="wrong")}),
            ("candidate-status", {"candidate_mutator": lambda v: v.update(status="wrong")}),
            ("candidate-extra", {"candidate_mutator": lambda v: v.update(extra=True)}),
            ("resolved-schema", {"resolved_mutator": lambda v: v.update(schema="wrong")}),
            ("resolved-status", {"resolved_mutator": lambda v: v.update(status="wrong")}),
            (
                "resolved-checkpoint",
                {"resolved_mutator": lambda v: v.update(code_checkpoint="2" * 40)},
            ),
            ("release-schema", {"release_mutator": lambda v: v.update(schema="wrong")}),
            ("release-status", {"release_mutator": lambda v: v.update(status="wrong")}),
            (
                "release-checkpoint",
                {"release_mutator": lambda v: v.update(code_checkpoint="2" * 40)},
            ),
            (
                "reference-path",
                {
                    "candidate_mutator": lambda v: v["resolved_formal_plan"].update(
                        path="wrong.json"
                    )
                },
            ),
        )
        for index, (name, kwargs) in enumerate(cases):
            with self.subTest(name=name):
                self._write_valid_sources(**kwargs)
                self._assert_failure(family=f"artifact-{index}")

    def test_callback_missing_exception_nonpass_and_exact_counts(self) -> None:
        self._assert_failure(family="callback-missing", validator=None)

        def explode(*_payloads):
            raise LookupError("synthetic callback failure")

        failure = self._assert_failure(family="callback-exception", validator=explode)
        self.assertEqual(type(failure.primary).__name__, "LookupError")
        self.assertEqual(
            json.loads((failure.root / subject.TERMINAL_NAME).read_bytes())[
                "semantic_callback_counts"
            ],
            {"validator": 0, "consumer": 0},
        )
        nonpass = self._assert_failure(
            family="callback-nonpass",
            validator=lambda *_: {"status": "fail"},
        )
        self.assertIn("non-pass", str(nonpass.primary))

        calls = {"validator": 0, "consumer": 0}

        def validator(*_):
            calls["validator"] += 1
            return {"status": "pass"}

        def consumer(*_):
            calls["consumer"] += 1
            return {"status": "pass"}

        self._run(family="callback-counts", validator=validator, consumer=consumer)
        self.assertEqual(calls, {"validator": 1, "consumer": 1})

    def test_baseexception_failure_seals_and_remains_non_success(self) -> None:
        for index, exception in enumerate((KeyboardInterrupt(), SystemExit(7))):
            with self.subTest(exception=type(exception).__name__):
                def interrupt(*_args, exception=exception):
                    raise exception

                with self.assertRaises(type(exception)) as raised:
                    self._run(family=f"baseexception-{index}", validator=interrupt)
                root = raised.exception.retained_release_root
                terminal = json.loads((root / subject.TERMINAL_NAME).read_bytes())
                self.assertEqual(terminal["status"], "fail")
                self.assertEqual(
                    terminal["primary_failure"]["type"], type(exception).__name__
                )

    def test_source_is_unchanged_on_pass_and_injected_writer_failure(self) -> None:
        before = {
            name: (self.source / name).read_bytes() for name in subject.SOURCE_NAMES
        }
        self._run(family="immutable-pass")
        self.assertEqual(
            before,
            {name: (self.source / name).read_bytes() for name in subject.SOURCE_NAMES},
        )
        calls = {"count": 0}

        def fail_second_fsync(fd):
            calls["count"] += 1
            if calls["count"] == 2:
                raise OSError("synthetic second fsync")
            os.fsync(fd)

        self._assert_failure(
            family="immutable-failure", overrides={"fsync_fd": fail_second_fsync}
        )
        self.assertEqual(
            before,
            {name: (self.source / name).read_bytes() for name in subject.SOURCE_NAMES},
        )

    def test_terminal_replay_rejects_tamper_missing_count_mismatch_and_self_reference(self) -> None:
        mutations = {
            "reference-tamper": lambda t: t["artifact_references"][0].update(
                sha256="0" * 64
            ),
            "wrong-count": lambda t: t.update(artifact_reference_count=99),
            "mismatch-array": lambda t: t["mismatch_arrays"]["artifact"].append("x"),
            "self-reference": lambda t: t["artifact_references"].append(
                {"path": subject.TERMINAL_NAME, "bytes": 1, "sha256": "0" * 64}
            ),
        }
        for index, (name, mutation) in enumerate(mutations.items()):
            with self.subTest(name=name):
                result = self._run(family=f"terminal-{index}")
                terminal = Path(result["root"]) / subject.TERMINAL_NAME
                self._rewrite_canonical(terminal, mutation)
                replay = subject._replay_terminal_bundle(terminal.parent)
                self.assertEqual(replay["status"], "fail")
                self.assertTrue(replay["mismatches"])

        result = self._run(family="terminal-missing")
        root = Path(result["root"])
        (root / subject.PROGRESSIVE_NAMES[4]).unlink()
        replay = subject._replay_terminal_bundle(root)
        self.assertEqual(replay["status"], "fail")
        self.assertTrue(any("artifact:" in item for item in replay["mismatches"]))

    def test_forbidden_external_prefix_is_not_present_in_module_or_tests(self) -> None:
        # Construct the policy sentinel so the prohibited literal itself never
        # appears in either allowed source file.
        sentinel = "/Volumes/4T/temp/" + "rgbww-optimizer/" + "p7-td-b-lineage-" + "release-r3/"
        for path in (Path(subject.__file__), Path(__file__)):
            self.assertNotIn(sentinel, path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
