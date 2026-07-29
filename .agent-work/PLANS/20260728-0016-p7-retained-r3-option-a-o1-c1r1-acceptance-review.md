# REF-P7-25-R2-O1-C1R1 / Durable full capture and synthetic owner acceptance review

**Planner decision：** `ACCEPTED_OPTION_A_OWNER_PREREQUISITE_COMPLETE`

**Planner date：** 2026-07-28 00:16 MDT

**Reviewed reference task：** `REF-P7-25-R2-O1-C1R1`

**Reviewed contract：**
`P7-TD-B-RETAINED-R3-REPO-OWNED-AUDIT-HELPER-O1-C1R1-DURABLE-FULL-CAPTURE`

**Exact next branch：** `REF-P7-25-R2-O2`

## 1. Frozen review inputs

```text
reviewed starting HEAD =
  32b9e670ff3bbea0cd1505528c2ca87c2935446c
accepted current HEAD =
  9303aa22a9bd37e8ec4f23147c78c6bea84b9a2e
reviewed PLAN SHA-256 =
  a96188a13ddfb84f2da4a2623ceb0cf26cf2e78398b068e4efd69cfdb1b6b2cf
reviewed EXECUTION_RESULT SHA-256 =
  6ca52c3b1f7aeb72a39a02809c97d1e11d03af4fe696cbe016bb6c33f272c36f
reviewed FULL_PLAN_REFERENCE SHA-256 =
  7408b4764b9f165588e484efaec427ad4d39e19ed38b8ab3eb9569eda4636a74
GUIDE SHA-256 =
  659152f6c0ae69c90c701de4e57c352d771e4f0bf75cf9410271ba0a94200e35
predecessor C1 review SHA-256 =
  49b1ed4a97009662b78bab9452d52d9ce5ef0cb5df438248e1363c77a393b3e9
```

The Planner did not rerun any test, invoke a device/network path, or access the
real retained R3 release family during review.

## 2. Exact commit and implementation identity

The accepted commit is：

```text
commit =
  9303aa22a9bd37e8ec4f23147c78c6bea84b9a2e
parent =
  32b9e670ff3bbea0cd1505528c2ca87c2935446c
tree =
  c67473c6c8b4fbf799f9e74cd71f89493e18ce4d
subject =
  fix(p7): validate retained release terminal counts
path count = 2
```

Exact paths and accepted current bytes：

```text
src/camera_based_rgbww_optimizer/optimization/
  p7_retained_release_audit.py
SHA-256 =
  82713766baa2c66a2fa6e0d64796d9f1fe280ede98f41ab5c453fb32cfc63d9a

tests/test_p7_retained_release_audit.py
SHA-256 =
  e5df8f007745593ecbd9c5df3d5430b58c65b7fdb6fd0f1b0a00462ef7650900
```

The commit contains exactly the retained O1 owner plus the three C1
corrections: terminal reference-count equality, semantic NaN assertion and
truthful two-attempt permanent-fsync assertion. No amend, second commit, push
or PR occurred.

## 3. Accepted test and static evidence

Frozen predecessor gates：

```text
C1 corrective focused = 20/20 pass
C1 exact lineage = 2/2 pass
C1 compileall = pass
C1R1 reruns before commit = 0/0/0
```

The C1R1 durable full-suite artifacts are：

```text
validation root =
  /Volumes/4T/temp/rgbww-optimizer/
  p7-td-b-retained-release-audit-helper-o1-c1r1-validation/20260727T2353

controller SHA-256 =
  6893d8100a10fda025747655a5148886e9350dabd6314f2d991a4b386fd2dab5
full-suite.log bytes / SHA-256 =
  133736 /
  f02951bcbdfc1dca5106874942bb730c88592e83863ac4816bb04b1b270607fa
full-suite-terminal.json bytes / SHA-256 =
  789 /
  0fdc9d3bc1b6e277abc616476b3395ccc21d0204f35a23fe8a4d159d604c205e
final-read-only-audit-summary.json bytes / SHA-256 =
  2988 /
  962b6517259a143179cd5cce715ad8e76ec407f1a1da74ca33032662818ee612
```

Independent Planner replay proved：

```text
exact argv = .venv/bin/python -m unittest discover -s tests -v
child exit = 0
unique terminal summary = Ran 661 tests in 153.070s
final disposition = OK
FAILED summaries = 0
controller/seal errors = null/null
partial artifacts = 0
controller/child residual process = 0/0
```

The remaining precommit gates passed once: `git diff --check`, syntax for 18
tracked wrappers, secret/path scan, exact-three-change audit and fresh
CodeGraph sync/query with no stale re-query. The exact postcommit focused suite
passed `20/20`.

## 4. Accepted synthetic lifecycle proof

Synthetic evidence root：

```text
/Volumes/4T/temp/rgbww-optimizer/
p7-td-b-retained-release-audit-helper-o1-c1-offline/20260727T2341
```

Canonical summaries：

```text
08-validation-summary.json bytes / SHA-256 =
  2278 /
  9b9ba4f8751fd23f86749e5f697155ee4131bc778d48544d419cd242303e9522
09-terminal-summary.json bytes / SHA-256 =
  1461 /
  58d646dea248054ee79228a95c919d9737dc166ca5d5d6da9235b3ba38104f
```

Independent Planner verification proved：

```text
source artifacts = 3
changed-path rows = 59 ordered dict rows
owner invocation = 1
validator/consumer calls = 1/1
progressive artifacts = 9
terminal artifact references = 9/9 exact bytes and SHA
source before/after manifests = byte-identical
source file bytes/SHA/device/inode = unchanged
artifact/callback/identity/schema/side-effect mismatches = all empty
primary/seal failure = null/null
independent replay = pass
```

The synthetic source root has exactly three regular non-symlink files; the
evidence root has exactly ten regular non-symlink files. No `.partial` residue
or parallel lifecycle owner remains.

## 5. Boundary verification

The final read-only audit and execution handoff agree on exact zero counts：

```text
real retained release access = 0
external release root access = 0
qualification/generation/retry/repair/copy/consumption = 0/0/0/0/0/0
real validator/consumer = 0/0
network/DNS/.env = 0/0/0
device/camera/Ray/strip/cleanup/capture = 0/0/0/0/0/0
CR3/NPY/nonzero light = 0/0/0
predevice/Z0/E2/public analyzer/formal R6/TD-C = 0/0/0/0/0/0
firmware/deployment/push/PR = 0/0/0/0
```

Staged paths are empty, production/test scope is clean at the accepted commit,
and unrelated dirty worktree entries remain preserved.

## 6. Decision and exact next branch

```text
REF-P7-25-R2-O1-C1R1 =
  ACCEPTED_OPTION_A_OWNER_PREREQUISITE_COMPLETE
REF-P7-25-R2-O1 =
  ACCEPTED_REPO_OWNED_AUDIT_HELPER_READY_FOR_REAL_RETAINED_AUDIT
REF-P7-25 =
  BLOCKED_ON_ONE_REAL_RETAINED_R3_READ_ONLY_AUDIT
retained R3 =
  RETAINED_UNVALIDATED_UNCONSUMED
```

This acceptance proves the repo-owned acquisition/persistence/schema-audit/
callback/terminal/replay lifecycle against adversarial tests and a fresh
synthetic fixture. It does not claim that the frozen retained R3 production
shape passes the helper or public lineage semantics.

The exact next branch `REF-P7-25-R2-O2` must use the accepted helper once on the
frozen real retained R3 three-artifact source. It must call the existing public
lineage validator and a non-executing fake consumer at most once each, preserve
durable progressive/terminal evidence, independently replay the terminal and
prove source immutability.

## 7. Residual risks and locks

- Real retained R3 schema and semantic compatibility remain unproven until O2.
- A helper schema rejection or callback failure in O2 is a valid fail-closed
  result and must not be repaired, retried, copied or relabelled in that package.
- Retained R3 remains unavailable for consumption, release authority, device
  entry or formal execution.
- Qualification, generation, repair, copy and consumption remain locked.

No Human authorization or Advisor decision is required for O2 because it is a
strictly read-only offline audit with fresh audit-evidence writes only.

## 8. 维护性判断

The accepted helper centralizes one high-risk filesystem lifecycle and keeps
scientific meaning callback-owned. Its 661-test full regression, dedicated
20-test adversarial suite and one-shot synthetic terminal replay provide the
required prerequisite proof. The next package adds no implementation or
abstraction; it tests the remaining real-shape boundary directly.
