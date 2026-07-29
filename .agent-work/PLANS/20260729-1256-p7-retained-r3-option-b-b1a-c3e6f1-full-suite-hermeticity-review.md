# REF-P7-25-R2-B1A-C3E6F1 review / exact candidate full-suite hermeticity failure

**Planner review date:** 2026-07-29

**Reviewed contract:**
`P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F1-EXACT-CANDIDATE-COMMIT-V1`

**Decision:** `rejected_full_suite_environment_dependencies`

**Next branch:** `REF-P7-25-R2-B1A-C3E6F2`

## Reviewed scope

C3E6F1 was authorized to create one fresh clean room at parent
`9303aa22a9bd37e8ec4f23147c78c6bea84b9a2e`, materialize the exact five-path
candidate bound by candidate object SHA-256
`3c5847fcbe0af85833c901f6f01058d000a3cecdc0f84e6ae331ed24e138c225`,
copy two exact ignored fixtures, run one clean-room import gate, one focused
suite and one full suite, and only after full success create one direct-child
commit plus one subordinate immutable provenance manifest.

Release audit, eligibility, release consumption, original-R3 semantic reads,
network, DNS, `.env`, device, camera, Ray, strip, cleanup, capture, analyzer,
FORMAL, firmware and deployment access were all prohibited.

## Independently verified implementation and evidence

Evidence root:

```text
/Volumes/4T/temp/rgbww-optimizer/
  p7-td-b-retained-r3-option-b-b1a-c3e6f1-offline/
  20260729T184631Z
```

The clean room remains detached at the exact parent. Its only five modified
paths are the five candidate paths. Nothing is staged.

`candidate-verification.json` proves:

- all five candidate files match their expected bytes and SHA-256 values;
- changed paths are exactly the candidate five;
- candidate edits are zero;
- `git diff --check` passed;
- the canonical binary full-index patch is 53,230 bytes with SHA-256
  `7b71f9db1ef5a56c6065a255f35b34e9ca7d625699ff31a07cfa7fadb1f75f35`.

The import identity gate resolved all three production owners inside this
exact clean room and matched their candidate hashes. The focused command ran
exactly once and passed `102/102` with zero failures and zero errors.

The full command ran exactly once:

```text
/Users/ibobby/Projects/WLED-RGBWW/.venv/bin/python \
  -m unittest discover -s tests -v
```

It ran 664 tests and returned 18 errors, zero assertion failures. The persisted
summary and stderr SHA-256 values are:

- `full-summary.json`:
  `615203f8b62dc530a63c4355698ddee6f76c929bdde4ca58edba4fb49e5699a3`
- `full.stderr`:
  `f1177579b79ff74cfab28a07db4476ab8c11b8bdfb36b79b2f62f38b924d0c06`
- `validation-summary.json`:
  `dde3c1fad1e1c0b48504941c664edfb64d37f20f24c59f0d597c45b8123838ad`
- `terminal-summary.json`:
  `8dcb29e4bf0ddd1e92c22bf0d451e2422103d3d1410de79235cdb01c1cf2313e`

The package correctly stopped before stage, commit, manifest, verifier or any
retained-R3 content read. Those counters, all release/audit/eligibility calls,
all prohibited environment/device operations and retry remain zero. Shared
HEAD remains `9303aa22a9bd37e8ec4f23147c78c6bea84b9a2e`; shared staged paths remain zero.

## Failure classification

### Exact local white-LUT fixture: 17 errors

All 17 errors are in
`tests/test_measure_raw_observer_validation.py`. Every traceback reaches
`build_raw_observer_validation_plan()`, which always records
`DEFAULT_WHITE_LUT` through `_file_reference()`. In the clean room that path is
`config/white/white-lut.json`, and `_file_reference()` correctly rejects its
absence.

Independent inspection of the shared source input proves:

- path: `/Users/ibobby/Projects/WLED-RGBWW/config/white/white-lut.json`;
- regular file, not a symlink;
- 9,272 bytes;
- SHA-256:
  `5236492c8474be4e77caf7adb7807e549c4bc83a8f373328a7293eb9861b3145`;
- strict JSON object with top-level keys `measurement_policy`, `source_runs`,
  `status`, `targets`, `version`;
- recursive key scan found no secret/token/password/credential/API-key field;
- untracked and ignored by the exact existing `config/*` rule;
- production and documentation statically name it as the default white LUT.

This is the same class as the two already approved exact ignored local inputs:
an external, noncandidate, non-Git, test-only fixture needed to reproduce the
repository's local test environment. It must be read once with no-follow and
stable-fstat evidence, validated before copying, copied exactly once only into
the fresh clean room, and excluded from changed paths, stage, commit and any
provenance manifest.

### Raw-shutter CLI test isolation: 1 error

`test_cli_execute_calls_native_runner_only_after_explicit_consent` mocks
`run_native_raw_shutter_response` but does not mock
`camera_remote.create_camera_backend`. Production `main()` constructs the
backend before calling the mocked runner, so the test reaches
`RemoteCameraBackend.from_environment()` and attempts to load a real token from
the process environment or clean-room `.env`.

The correct regression boundary is test-only dependency injection: patch
`measure_raw_shutter_response.camera_remote.create_camera_backend` to return a
fake sentinel backend, keep the existing runner mock, prove the factory is
called exactly once, prove the runner receives that same fake backend, and
retain the existing success/runner-once assertions. No token value, `.env`
copy/read, production fallback or network access is permitted.

## Planner decision

C3E6F1 is rejected as a terminal hard failure. It earns exact-candidate,
import-identity and focused-test credit, but no full-suite, commit, manifest,
audit, eligibility or release credit. The rejected root is immutable and must
not be repaired or rerun.

The failure is engineering/test-environment-owned, not color-science-owned.
No Advisor or Human authorization is required.

The successor is one fresh, bounded offline diagnostic/correction package:

1. materialize the same exact five candidate paths into a new clean room;
2. validate and copy the existing two fixtures plus the exact white-LUT fixture;
3. permit an edit to exactly
   `tests/test_measure_raw_shutter_response.py` and no production path;
4. implement only the fake-backend injection described above;
5. run one post-edit targeted suite covering both candidate suites and both
   formerly failing modules, then one full discovery;
6. stop after immutable terminal evidence, without stage, commit, manifest,
   retained-R3 reads, audit, eligibility or release consumption.

If targeted or full fails, stop with the complete new evidence. If both pass,
return to Planner for the exact Git/candidate topology decision; success does
not itself enlarge the candidate or authorize a commit.

## Residual risks

- The full suite has not yet passed in a hermetic clean room.
- The test-only correction is not yet frozen by a resulting file/patch hash.
- Whether the correction becomes a prerequisite commit or a member of a later
  exact candidate remains an Orchestrator-owned engineering decision after the
  correction is proved.
- Original retained R3 remains
  `RETAINED_UNVALIDATED_UNCONSUMED`; rollback remains
  `32b9e670ff3bbea0cd1505528c2ca87c2935446c`.

**Planner stop:** archive complete; activate only C3E6F2 after Orchestrator
reviews and synchronizes its required FULL machine state.
