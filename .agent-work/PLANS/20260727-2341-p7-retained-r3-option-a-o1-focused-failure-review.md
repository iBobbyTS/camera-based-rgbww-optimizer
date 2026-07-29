# REF-P7-25-R2-O1 / Repo-owned retained-release audit owner focused-failure review

**Planner decision：** `REJECTED_FOCUSED_GATE_FAILED_OWNER_REPLAY_COUNT_UNVALIDATED`

**Planner date：** 2026-07-27 23:41 MDT

**Reviewed reference task：** `REF-P7-25-R2-O1`

**Reviewed contract：**
`P7-TD-B-RETAINED-R3-REPO-OWNED-AUDIT-HELPER-O1`

**Exact next branch：** `REF-P7-25-R2-O1-C1`

## 1. Frozen review inputs

```text
HEAD =
  32b9e670ff3bbea0cd1505528c2ca87c2935446c
parent =
  cc6dbd356dec20eca1437b6c282358c3f2a5e5c7
tree =
  494b24c70b8cd5c3a4e06f82de3511b3d63dd0a9
subject =
  test(p7): bind post-eq checkpoint drift injection

reviewed PLAN SHA-256 =
  aca75dc1922d67ce13145ba3d1a8a6e257ccd03f39613b0cb3ab3f9c161fb0d5
reviewed FULL_PLAN_REFERENCE SHA-256 =
  51b1d073c2d2e1dd607900be02b63c79e932f7d556c0f2de910c9bfbce738509
reviewed EXECUTION_RESULT SHA-256 =
  7bddc87a9878e7eb73f044b9c4350a1d2e2ca60473963fa2a0ad596232e54dec

Option A selection review =
  .agent-work/PLANS/
  20260727-2320-p7-retained-r3-option-a-owner-selection-review.md
Option A selection review SHA-256 =
  3f5773b67dfff33393adc64ff742e40475db1c5589bbf9539353285799c290f2
```

The exact two implementation inputs remain uncommitted and unstaged：

```text
src/camera_based_rgbww_optimizer/optimization/
  p7_retained_release_audit.py
SHA-256 =
  aec8c98cde73b5f6eb0e1f4b75fe7b563216757fa8098d6748de9eb434db4701

tests/test_p7_retained_release_audit.py
SHA-256 =
  759cc12d0e13b9cf89fec219582dfc9655df7ead1325896348deefbfe468c09a
```

The planned O1 synthetic evidence root remained absent：

```text
/Volumes/4T/temp/rgbww-optimizer/
  p7-td-b-retained-release-audit-helper-o1-offline/20260727T2320
```

No Planner review command accessed the retained/external release family.

## 2. Reviewed execution and gate quality

The initial failing-first gate was consumed exactly once and produced the
expected pre-implementation import error：

```text
failing-first attempt/completed = 1/1
tests run/pass/fail/error = 1/0/0/1
expected failure =
  ModuleNotFoundError for p7_retained_release_audit
```

The production module and dedicated test module were then added within the
exact two-path allowlist. The first implementation focused run was consumed
once：

```text
focused attempt/completed = 1/1
tests run/pass/fail/error = 20/17/3/0
result = fail
```

The Executer correctly stopped at the focused hard gate. It did not run a
second focused pass, existing-lineage tests, full suite, static checks,
post-edit CodeGraph, Git stage/commit, postcommit checks or one-shot synthetic
evidence. The reported stop therefore proves neither full validation nor an
acceptable owner.

## 3. Planner findings

### REV-R3-O1-001 — NaN rejection is correct; the assertion is interpreter-text specific

The canonical encoder used `allow_nan=False` and rejected the injected NaN
with `ValueError`. Python 3.13 rendered the error as：

```text
Out of range float values are not JSON compliant: nan
```

The test incorrectly required the literal substring `allow_nan`. This is a
test-contract defect. The correction must assert the semantic failure type and
hard-failure disposition, not an interpreter-specific message.

### REV-R3-O1-002 — permanent fsync failure has two truthful attempts, not three

With a permanently failing injected `fsync`, the owner attempted：

1. the primary progressive persistence;
2. one best-effort failure-summary persistence.

The second failure becomes the seal failure, so execution cannot reach a third
terminal write. The observed count `2` is consistent with fail-closed
behavior; the test's expected count `3` is wrong. The correction must assert
the exact two-attempt lifecycle plus preserved primary/seal failures.

### REV-R3-O1-003 — terminal replay does not validate `artifact_reference_count`

The private read-only terminal replay validates reference schemas, order,
duplicates, self-reference, artifact bytes/SHA, required progressive names,
mismatch arrays and callback counts. It does not compare the terminal's
declared `artifact_reference_count` with the actual reference-list length.

The `wrong-count` mutation was therefore accepted. This is a real fail-closed
owner defect, not a test issue. Because independent terminal replay is an
explicit O1 acceptance gate, the owner cannot be accepted until this exact
field is validated.

## 4. Decision and retained implementation disposition

```text
REF-P7-25-R2-O1 =
  REJECTED_FOCUSED_GATE_FAILED_OWNER_REPLAY_COUNT_UNVALIDATED
REF-P7-25 =
  BLOCKED_ON_OPTION_A_O1_C1_CORRECTION_AND_REVIEW
retained R3 =
  RETAINED_UNVALIDATED_UNCONSUMED
```

The two uncommitted implementation files are accepted only as retained inputs
for one bounded corrective package. The owner itself is not accepted, no
commit is accepted, and no validation/evidence credit beyond the frozen
failing-first and failed focused attempts may be inferred.

## 5. Exact corrective branch

`REF-P7-25-R2-O1-C1` may edit only the same two files and make exactly three
minimal corrections：

1. replace the NaN message-substring assertion with a semantic
   `ValueError`/hard-failure assertion;
2. correct the permanent-fsync test to require exactly two persistence
   attempts and preserved primary plus seal failure;
3. make read-only terminal replay reject any
   `artifact_reference_count != len(artifact_references)`.

The initial failing-first gate is already consumed and must not be rerun.
Pre-edit reproduction is also unnecessary and prohibited: the failed focused
run plus source inspection are the frozen regression evidence. The first test
invocation in C1 must occur only after the three minimal edits and is a
corrective focused validation, not a new failing-first or reproduction event.

If any other code/test change is required, or the focused suite exposes a new
owner defect, C1 must stop rather than broaden the repair.

## 6. Required successor validation

After the exact three corrections, C1 must run：

- the dedicated focused suite;
- the two exact existing post-EQ lineage tests;
- compileall for the two editable files;
- the complete unittest suite;
- tracked wrapper syntax, `git diff --check` and a two-file secret/path scan;
- post-edit `codegraph sync` and a fresh owner/blast-radius query.

Only after all precommit gates pass may C1 create one exact-two-path commit,
audit its path set and rerun the dedicated focused suite once postcommit.
Then one fresh synthetic exact-three-artifact/59-row owner invocation and
independent replay may create a new C1 evidence root. Any failure stops without
amend, retry, alternate root or same-root repair.

## 7. Absolute locks

C1 must not open, stat, list, hash, read, validate, copy, repair or consume the
real retained R3 family or any historical/external release root. Production
qualification, release generation/retry/repair/copy/consumption, real public
validator/consumer calls, device/network/DNS/`.env`, camera/Ray/strip,
cleanup/capture, public analyzer, predevice/Z0/E2/formal R6/TD-C, firmware,
deployment, push and PR all remain prohibited.

No Human authorization or Advisor decision is required because this is a
synthetic pure-offline correction that does not change scientific/release
meaning or perform a dangerous operation.

## 8. Residual risks

- The new owner is nearly complete but currently trusts one tamperable
  terminal count field.
- The module is large for a new owner, but the current failure does not justify
  a refactor before correctness is established.
- Retained R3 remains unavailable as authority until a later, separately
  planned real-retained audit succeeds.
- Release consumption and all device/formal work remain locked.

## 9. 维护性判断

The single-owner boundary remains preferable to the failed external-launcher
pattern. O1-C1 is deliberately limited to one owner check and two test-contract
corrections; it adds no abstraction, writer, controller or scientific rule.
The dedicated adversarial suite plus full regression and synthetic terminal
replay are the required proof before considering any later cleanup.
