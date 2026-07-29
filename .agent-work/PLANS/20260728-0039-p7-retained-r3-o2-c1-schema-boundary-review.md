# REF-P7-25-R2-O2-C1 / Real retained schema-boundary review

**Planner decision：** `REJECTED_HELPER_SCHEMA_BOUNDARY_BEFORE_PUBLIC_VALIDATION`

**Planner date：** 2026-07-28 00:39 MDT

**Reviewed reference task：** `REF-P7-25-R2-O2-C1`

**Reviewed contract：**
`P7-TD-B-RETAINED-R3-REAL-READ-ONLY-AUDIT-O2-C1-MACHINE-STATE-BINDING`

**Exact next branch：** `REF-P7-25-R2-O3`

## 1. Frozen review inputs

```text
HEAD =
  9303aa22a9bd37e8ec4f23147c78c6bea84b9a2e
reviewed PLAN SHA-256 =
  90d2c8ebec938f05025a76fc27d75d812dcdd942e8611473218a87f72891a077
reviewed EXECUTION_RESULT SHA-256 =
  8c9ae0b7c7f55c72338ae9bc0cfd4c517bb5dc51314c58ecd8bc78b797d2fbb0
reviewed FULL_PLAN_REFERENCE SHA-256 =
  cba2ab0a0b47e5531af2a569e1075ed0fb882d47e780077fa778486aba877340
GUIDE SHA-256 =
  659152f6c0ae69c90c701de4e57c352d771e4f0bf75cf9410271ba0a94200e35
```

## 2. Accepted failure facts

The unique FULL machine-state contract and every non-FULL hash gate passed.
The frozen source root contained exactly the three expected regular,
non-symlink files with exact bytes/SHA. Full before/after root and file
identity snapshots matched.

The helper acquired one fresh parent/root and stopped in its internal
schema/status audit before either semantic callback：

```text
helper invocation = 1
parent/root acquisition = 1/1
primary failure =
  ValueError: artifact schema or status differs
public lineage validator = 0
fake consumer = 0
independent replay = 0
retry/repair/copy/alternate root = 0/0/0/0
```

Truthful terminal evidence：

```text
evidence root =
  /Volumes/4T/temp/rgbww-optimizer/
  p7-td-b-retained-release-r3-audit-o2-c1-offline/20260728T0028
09-terminal-summary.json bytes/SHA-256 =
  883 /
  60547cf020a6decfce6daf028df3724d84058a2fa03a65abad231164fe159474
terminal status = fail
terminal references = 4/4 exact
primary/seal failure = ValueError / null
callback counts = 0/0
mismatch arrays = all empty
```

## 3. Decision

```text
REF-P7-25-R2-O2-C1 =
  REJECTED_HELPER_SCHEMA_BOUNDARY_BEFORE_PUBLIC_VALIDATION
retained audit credit = 0
retained R3 = RETAINED_UNVALIDATED_UNCONSUMED
```

The evidence proves the failure boundary, not its owner. No Planner acceptance
may infer that the retained artifacts violate the authoritative public
lineage contract, or that the helper is wrong, until their exact top-level
schema/status/key sets are compared offline.

## 4. Exact next branch

`REF-P7-25-R2-O3` first performs one read-only schema-owner diagnosis against
the exact retained three artifacts, the existing public lineage owner and the
helper schema audit. It must not invoke the real helper audit, validator,
consumer or replay and must not create a real-audit root.

Only if that comparison proves the retained artifacts match the authoritative
public contract and the helper is stale may O3：

1. add one minimal real-schema-shaped failing test without copying production
   artifacts or secrets;
2. edit only the existing helper and its dedicated test;
3. make the smallest fail-closed compatibility correction;
4. run bounded focused/lineage/full/static/CodeGraph gates, one exact-two-path
   commit, postcommit focused and one fresh synthetic owner bundle.

If the retained artifacts violate the public owner or scientific meaning is
ambiguous, O3 must stop for Advisor guidance without editing.

## 5. Locks and residual risks

Qualification, generation, retry, repair, copy, consumption, real retained
audit, real validator/consumer/replay, device/network/formal/public analyzer,
firmware and deployment remain zero. The failed O2-C1 root is immutable and
must never be reused.

No Human authorization is required. Advisor is required only if the diagnostic
finds authoritative-contract failure or scientific ambiguity.

## 6. 维护性判断

The next branch preserves the single helper/public-validator ownership split:
first identify which contract is stale, then permit a two-file correction only
for a proven helper bug. No parallel owner or broad schema fallback is allowed.
