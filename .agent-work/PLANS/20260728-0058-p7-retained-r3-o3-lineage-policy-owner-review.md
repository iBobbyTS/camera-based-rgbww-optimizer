# REF-P7-25-R2-O3 / Lineage-policy owner review

**Planner decision：** `REJECTED_LINEAGE_POLICY_OWNER_REQUIRED`

**Planner date：** 2026-07-28 00:58 MDT

**Reviewed reference task：** `REF-P7-25-R2-O3`

**Reviewed contract：**
`P7-TD-B-RETAINED-R3-SCHEMA-OWNER-DIAGNOSIS-AND-CORRECTION-O3`

**Exact next branch：** `REF-P7-25-R2-O3-C1`

## 1. Frozen review inputs

```text
HEAD =
  9303aa22a9bd37e8ec4f23147c78c6bea84b9a2e
reviewed PLAN SHA-256 =
  63d9725b472fbf745fb327525ae5e1cab9c5e188c5c77b56f1df1f9637024eab
reviewed EXECUTION_RESULT SHA-256 =
  5311fe08623fe2a9d8ea43ca8464ad343afefeb91b665085b21b2632752169ff
reviewed FULL_PLAN_REFERENCE SHA-256 =
  ced309e2f60f4db9ff94a42dd1b3a461832901dd9e10aa59f8d47032dd813172
GUIDE SHA-256 =
  659152f6c0ae69c90c701de4e57c352d771e4f0bf75cf9410271ba0a94200e35
```

## 2. Accepted Branch A diagnosis

The bounded diagnostic proved the retained three-artifact top-level
schema/status/key shapes match the existing public lineage owner while the
helper expected only its earlier synthetic variant.

```text
diagnostic-summary.json bytes/SHA-256 =
  9082 /
  a5141b90f42bc8753229356492d16af8839ca17492c7a2ad19500caaf923fb41
diagnostic branch = A_PROVEN_HELPER_CONTRACT_BUG
real helper/validator/consumer/replay = 0/0/0/0
source before/after identity = exact
```

The one failing-first produced the expected stale schema boundary. The
retained two-file correction then passed its dedicated focused suite `21/21`.
This proves the correction direction only; it does not accept the diff.

## 3. Rejected lineage gate

The exact five-test lineage invocation completed `4/5`. The failure was：

```text
test =
  test_post_eq_policy_lineage_classifies_only_exact_accepted_paths
expected changed-path count = 59
observed changed-path count = 61
```

The Executer stopped correctly. Compileall, durable full suite, static gates,
post-edit CodeGraph, commit, postcommit focused and synthetic evidence all
remain zero.

Retained uncommitted inputs：

```text
src/camera_based_rgbww_optimizer/optimization/
  p7_retained_release_audit.py
SHA-256 =
  48c0c57fb95c08205c3fef7b23e6df3729928352cd23e1722e8693b9f3634cf8
diff numstat = +186/-33

tests/test_p7_retained_release_audit.py
SHA-256 =
  c8d6c7c99815d823871ecfddce79eadd5d5def918affbcd7e4ce86de691d1b3f
diff numstat = +159/-0
```

They remain unstaged, uncommitted and unaccepted.

## 4. Independent root-cause proof

Git ancestry and path-set comparison prove：

```text
setup checkpoint =
  9c804abdeabbc5da18a66d0acf25a1f13128bc2d
release checkpoint =
  32b9e670ff3bbea0cd1505528c2ca87c2935446c
current HEAD =
  9303aa22a9bd37e8ec4f23147c78c6bea84b9a2e

setup -> release changed paths = 59
setup -> HEAD changed paths = 61
release checkpoint is direct parent of HEAD = true
release-only path delta = empty
HEAD-only path delta =
  src/camera_based_rgbww_optimizer/optimization/p7_retained_release_audit.py
  tests/test_p7_retained_release_audit.py
HEAD commit path set equals delta = true
```

Neither path appears in：

- `TD_B_LINEAGE_ALLOWED_PRODUCTION_PATHS`;
- `TD_B_LINEAGE_ALLOWED_VALIDATION_PATHS`;
- successor/workflow/cleanup/post-EQ exact classification owners.

The public candidate builder therefore routes both paths to
`prohibited_or_unreviewed`. The failing test's literal `59` is stale, but
changing only that assertion would still leave the candidate ineligible.

## 5. Decision and next branch

```text
REF-P7-25-R2-O3 =
  REJECTED_LINEAGE_POLICY_OWNER_REQUIRED
helper correction acceptance = 0
retained audit credit = 0
retained R3 = RETAINED_UNVALIDATED_UNCONSUMED
```

Classifying the exact helper commit requires a third production/policy owner
or a new exact commit-provenance manifest plus corresponding tests. That is a
lineage/release policy decision outside O3's two-file owner boundary; it must
not be disguised as an assertion update.

`REF-P7-25-R2-O3-C1` may only persist an independent, bounded offline ownership
proof and stop for Planner/Advisor determination. It must preserve the current
two-file diff unchanged and must not run tests, edit policy, commit or create
synthetic/real audit evidence.

## 6. Locks and residual risks

Qualification, generation, retry, repair, copy, consumption, real audit,
validator/consumer/replay, device/network/formal/public analyzer, firmware and
deployment remain zero.

Residual decision required: whether the exact helper commit and its dedicated
test should receive an exact provenance-backed lineage classification, and
which existing/new owner should carry it. Advisor guidance is required before
any policy implementation because the choice changes future release
eligibility.

## 7. 维护性判断

The helper correction remains locally coherent, but release eligibility is
owned elsewhere. Pausing prevents a test-only patch from masking two genuinely
unclassified paths and preserves a single explicit lineage-policy owner.
