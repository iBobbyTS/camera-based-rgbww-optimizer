# REF-P7-25-R2-O1-C1 / Full-suite terminal-evidence review

**Planner decision：** `REJECTED_FULL_SUITE_TERMINAL_EVIDENCE_UNPROVEN`

**Planner date：** 2026-07-27 23:53 MDT

**Reviewed reference task：** `REF-P7-25-R2-O1-C1`

**Reviewed contract：**
`P7-TD-B-RETAINED-R3-REPO-OWNED-AUDIT-HELPER-O1-C1`

**Exact next branch：** `REF-P7-25-R2-O1-C1R1`

## 1. Frozen review inputs

```text
HEAD =
  32b9e670ff3bbea0cd1505528c2ca87c2935446c
reviewed PLAN SHA-256 =
  4f2cc83baae1f7a73c081aaff317fab0b00dc2cc8a446271df160554c45f1857
reviewed FULL_PLAN_REFERENCE SHA-256 =
  d9ffe80725eae74779568a27fa1d4f7a315b1e0988103be9e60b2732e163d7c4
reviewed EXECUTION_RESULT SHA-256 =
  d443fe052fdfead060ad8db4f33e00f5cd92857c14ba50adaf9e8ac6bfe00f61
GUIDE SHA-256 =
  659152f6c0ae69c90c701de4e57c352d771e4f0bf75cf9410271ba0a94200e35
predecessor O1 review SHA-256 =
  f6d01102cdc0516961d45ae9c0170f9e6f9d37fe3e50e20d8d8aa257b2aa19da
```

No Planner review command opened, listed, statted, hashed or otherwise accessed
the real retained/external release family.

## 2. Exact retained implementation state

The O1-C1 implementation remains uncommitted and unstaged at the same starting
HEAD. Reverse-diff reconstruction recorded by the Executer matches both frozen
O1 inputs.

```text
production path =
  src/camera_based_rgbww_optimizer/optimization/
  p7_retained_release_audit.py
frozen O1 SHA-256 =
  aec8c98cde73b5f6eb0e1f4b75fe7b563216757fa8098d6748de9eb434db4701
corrected SHA-256 =
  82713766baa2c66a2fa6e0d64796d9f1fe280ede98f41ab5c453fb32cfc63d9a

test path =
  tests/test_p7_retained_release_audit.py
frozen O1 SHA-256 =
  759cc12d0e13b9cf89fec219582dfc9655df7ead1325896348deefbfe468c09a
corrected SHA-256 =
  e5df8f007745593ecbd9c5df3d5430b58c65b7fdb6fd0f1b0a00462ef7650900
```

The retained diff contains exactly the three authorized corrections：

1. independent terminal replay rejects a declared
   `artifact_reference_count` unequal to `len(artifact_references)`;
2. the NaN test requires a preserved `ValueError` hard failure without
   interpreter-specific text;
3. the permanent-fsync test requires exactly two attempts and both primary
   and seal failures.

No additional production/test edit is accepted or authorized.

## 3. Accepted completed gates

The following O1-C1 gates completed once and passed：

```text
corrective focused = 1/1, 20/20 pass
exact existing lineage tests = 1/1, 2/2 pass
compileall = 1/1 pass
```

The predecessor failing-first and predecessor failed focused run remain
historical consumed gates. None of these commands may be rerun in the
continuation package.

## 4. Full-suite terminal-evidence defect

The full-suite command was invoked exactly once under original PID `38992`.
Its output exceeded the tool yield window, and the invocation owner retained
neither a resumable session identifier nor a durable log/status pair.

The PID later exited naturally. That proves only that the process is no longer
running. It does not prove：

- the process exit code;
- the terminal unittest summary;
- test count, failure count or successful completion.

Therefore：

```text
full-suite attempted = 1/1
full-suite process later absent = true
durable exit code = missing
durable terminal summary = missing
full-suite disposition = indeterminate
```

The missing terminal evidence must not be inferred, reconstructed from partial
output, or relabelled as a pass.

## 5. Decision

```text
REF-P7-25-R2-O1-C1 =
  REJECTED_FULL_SUITE_TERMINAL_EVIDENCE_UNPROVEN
REF-P7-25 =
  BLOCKED_ON_OPTION_A_O1_C1R1_DURABLE_FULL_CAPTURE
retained R3 =
  RETAINED_UNVALIDATED_UNCONSUMED
```

The exact three corrections and the three completed gates may be retained as
frozen continuation inputs. No commit, full-suite pass, static/CodeGraph pass
or synthetic evidence credit exists.

## 6. Exact continuation branch

`REF-P7-25-R2-O1-C1R1` is a bounded evidence-lifecycle continuation, not a new
repair package. It must：

1. freeze the current two corrected file hashes and permit no additional
   production/test edit;
2. not rerun focused, exact-lineage or compileall;
3. consume one fresh full-suite invocation using a durable logfile plus an
   atomically persisted exit/status record owned by a minimal external
   controller;
4. treat any missing status, nonzero exit, absent unittest terminal summary or
   controller/seal failure as a hard stop with no retry;
5. only after a proven full-suite pass, run the remaining wrapper, diff,
   secret/path and fresh CodeGraph gates;
6. only after all precommit gates pass, create the previously authorized
   exact-two-path commit, run the one postcommit focused gate, and invoke the
   one fresh synthetic owner bundle plus independent replay.

The durable-capture mechanism may live only in a fresh disposable validation
root under `/Volumes/4T/temp/rgbww-optimizer`; it may not change repository
source, tests, config, docs, skills or wrappers.

## 7. Absolute locks and residual risks

The real retained R3 family and all external release roots remain prohibited:
no open/stat/list/hash/read/write/copy/repair/validation/consumption. Production
qualification, release generation/retry/repair/copy/consumption, real
validator/consumer calls, network/DNS/`.env`, device/camera/Ray/strip,
cleanup/capture, CR3/NPY/nonzero output, predevice/Z0/E2/public analyzer,
formal R6/TD-C, firmware, deployment, push and PR remain locked at zero.

Residual risks：

- the full regression result is still unproven until the continuation produces
  both durable exit and terminal summary evidence;
- the new owner is not accepted and the retained R3 cannot be treated as
  validated or consumable;
- the large lifecycle module remains intentionally unchanged until correctness
  is established.

No Human authorization or Advisor decision is required: the next branch is
pure-offline validation and does not change scientific or release meaning.

## 8. 维护性判断

The three corrections stay inside the single repo-owned lifecycle/replay
boundary. The continuation adds no repository abstraction or parallel owner;
it only makes the full-suite result recoverable before the existing static,
commit and synthetic-evidence gates may proceed.
