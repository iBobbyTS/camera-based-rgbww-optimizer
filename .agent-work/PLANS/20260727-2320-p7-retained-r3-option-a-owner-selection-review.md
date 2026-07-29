# REF-P7-25-R2-O1 / Option A ownership selection review

**Planner decision：** `STOP_SATISFIED_OPTION_A_SELECTED`

**Planner date：** 2026-07-27

**Reviewed stop contract：**
`P7-TD-B-RETAINED-R3-EVIDENCE-CONTROLLER-OWNERSHIP-REASSESSMENT-STOP`

**Reviewed reference task：** `REF-P7-25-R2-O1`

**Exact next branch：** `REF-P7-25-R2-O1-IMPLEMENTATION`

## 1. Frozen review inputs

```text
HEAD =
  32b9e670ff3bbea0cd1505528c2ca87c2935446c
parent =
  cc6dbd356dec20eca1437b6c282358c3f2a5e5c7

reviewed stop PLAN SHA-256 =
  18d0d78e83ce9869c79faee29e271f1e4db9e4214957ea20f8d572ed4a1ce311
reviewed FULL_PLAN_REFERENCE SHA-256 =
  e8e8ab66cb2e8d967fabca69647439c3795d6871f1d0f355d35c07553a128e47
reviewed EXECUTION_RESULT SHA-256 =
  c8c5326841f97511fbf5700d75713439d44cee37a91cb4c6befc3df42e35ba76
third-failure review archive SHA-256 =
  e02b169a9b8ec84d113461695b7d68f4552ce4f2973b982cf5589dc444c575ae
GUIDE SHA-256 =
  659152f6c0ae69c90c701de4e57c352d771e4f0bf75cf9410271ba0a94200e35
```

Planner verified that the Orchestrator recorded all three adjacent failures,
kept the retained release unvalidated/unconsumed, and explicitly selected：

```text
Option A =
  repo-owned retained-release audit helper
Option B =
  inactive
```

No Executer, implementation, evidence-root, retained-release, qualification,
release, validator, device or formal lifecycle was entered while the stop PLAN
was active.

## 2. Stop disposition

The prior stop's exit criteria are satisfied：

1. C1R2 rejection and the three-failure threshold are recorded in
   `FULL_PLAN_REFERENCE.md`;
2. Option A and its single ownership boundary are explicit;
3. the next package is implementation/test-only;
4. retained R3 access remains prohibited;
5. release and every device/formal route remain locked.

Decision：

```text
REF-P7-25-R2-O1 =
  STOP_SATISFIED_OPTION_A_SELECTED
REF-P7-25 =
  BLOCKED_ON_OPTION_A_IMPLEMENTATION_AND_REVIEW
retained release =
  RETAINED_UNVALIDATED_UNCONSUMED
```

## 3. Maintainability preflight

This change touches persistence, error handling and release-evidence ownership,
so a maintainability preflight is mandatory.

CodeGraph shows that：

- lineage classification and release validation already belong to
  `p7_thermal_diagnostics.py`;
- `canonical_sha256` already has a broad lineage/plan blast radius;
- the existing thermal module is a large scientific/contract owner and should
  not also absorb evidence-root acquisition, no-follow persistence and terminal
  lifecycle;
- the three failures all arose because those lifecycle responsibilities were
  split across transient launcher code.

The smallest enabling refactor is therefore one new P7-scoped module with one
public retained-audit owner and one dedicated test module. It reuses existing
lineage validators through explicit callables in a later integration package;
it does not duplicate or change scientific/release semantics.

## 4. Exact next package

The successor may edit only：

```text
src/camera_based_rgbww_optimizer/optimization/
  p7_retained_release_audit.py
tests/test_p7_retained_release_audit.py
```

It must establish one owner for：

- semantic dependency validation;
- safe two-level evidence parent/root acquisition and no-follow identity;
- exclusive canonical persistence;
- schema-aware exact-59-row changed-path audit;
- success/failure terminal sealing.

Fake filesystem and synthetic fixtures must cover the three historical
failures before any later package may read retained R3 evidence. The successor
must perform failing-first, focused/full/static/CodeGraph validation, at most
one exact-two-path commit, and one one-shot offline validation seal.

## 5. Locks and next stop

The implementation package must not read, hash, list, validate, copy, repair or
consume the current retained R3 family or any external release root. It must
not run qualification, release generation, public release validation against a
real release, device/network/`.env`, camera/Ray/strip/cleanup/capture, public
analyzer, formal R6 or TD-C.

After implementation failure or the one-shot offline terminal seal, Executer
must stop for independent Planner review. A later PLAN alone may authorize one
retained-release audit.

## 6. Decision owners

- Advisor guidance is not required: no scientific/release meaning changes.
- Human authorization is not required: this package is pure offline and
  contains no firmware, deployment, destructive hardware or out-of-plan device
  operation.

## 7. 维护性判断

Option A moves a repeatedly failing evidence lifecycle into a small,
testable, repo-owned boundary while leaving the existing lineage/scientific
owner unchanged. Dedicated adversarial tests protect the new persistence and
error-handling boundary before retained evidence can be accessed.
