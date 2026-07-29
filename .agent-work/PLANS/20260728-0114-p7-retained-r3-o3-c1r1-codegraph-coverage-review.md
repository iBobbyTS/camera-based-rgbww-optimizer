# REF-P7-25-R2-O3-C1R1 / CodeGraph coverage-gate review

**Planner decision：** `REJECTED_INCOMPLETE_CODEGRAPH_VERBATIM_COVERAGE`

**Planner date：** 2026-07-28 01:14 MDT

**Reviewed reference task：** `REF-P7-25-R2-O3-C1R1`

**Reviewed contract：**
`P7-TD-B-RETAINED-R3-HELPER-COMMIT-LINEAGE-OWNER-O3-C1R1-TARGETED-CODEGRAPH`

**Exact next branch：** `REF-P7-25-R2-O3-C1R2`

## 1. Frozen review inputs

```text
HEAD =
  9303aa22a9bd37e8ec4f23147c78c6bea84b9a2e
reviewed PLAN SHA-256 =
  84fccb28ec08185dbf1387f281fe39af5d0a52b5f536c35c2c055060996b9ecf
reviewed EXECUTION_RESULT SHA-256 =
  69d8942e95b0c98da37238bf570ccbffb49da7c289658267ec95b94d79a1d8b7
reviewed FULL_PLAN_REFERENCE SHA-256 =
  31093d1cf8d173cdfc8e9aaa75bd2923f56b120120b4c55dd687acd24cd66158
GUIDE SHA-256 =
  659152f6c0ae69c90c701de4e57c352d771e4f0bf75cf9410271ba0a94200e35
public owner SHA-256 =
  61033c79e51a046ecce4f26b06bc2b10427350b10733967e72b109e506f835d9
```

The unique 21-field machine state, HEAD, staged-empty state, frozen hashes and
both absent roots passed before the one query. The §169 Git proof was carried
without rerun.

## 2. Accepted CodeGraph response facts

The sole query correctly targeted
`src/camera_based_rgbww_optimizer/optimization/p7_thermal_diagnostics.py`.
The target was current/on-disk and had no stale or pending-index warning.

```text
query count / retry / sync = 1 / 0 / 0
response bytes = 15590
response SHA-256 =
  59101ae59527fd0711a5aadeea6afac4f65780f2beb23dcb3f4176c564a4f059
target-path match = true
target stale = false
```

The response supplied verbatim line-numbered source for：

- `TD_B_PUBLIC_DEFAULT_SUCCESSOR_CLASSIFICATIONS`;
- `TD_B_POST_EQ_POLICY_CLASSIFICATIONS`;
- `TD_B_LINEAGE_ALLOWED_PRODUCTION_PATHS`;
- `TD_B_LINEAGE_ALLOWED_VALIDATION_PATHS`.

Those target/freshness and covered-symbol facts may be carried into C1R2. The
query must not be repeated.

## 3. Rejected completeness gate

The response omitted required verbatim line-numbered source for：

- `build_td_b_setup_release_lineage_candidate`;
- `TD_B_WORKFLOW_PATH_CLASSIFICATIONS`;
- `TD_B_CLEANUP_TEST_PROVENANCE_CLASSIFICATIONS`;
- the candidate branch through `prohibited_or_unreviewed` and
  `eligible = not prohibited`.

It also returned unrelated test source and recommended another query. The PLAN
explicitly prohibited a second query. The Executer correctly stopped with
evidence root/seal at zero and did not substitute Git, grep or raw source.

Therefore exact absence from all owners, candidate fallthrough and
count-only-fix ineligibility remain unproven as a complete combined owner
conclusion. C1R1 cannot be accepted.

## 4. Evidence and operation disposition

```text
C1R1 evidence root/seal = 0
repository or implementation edits = 0
tests / compileall / CodeGraph sync = 0 / 0 / 0
Git ancestry/path proof rerun = 0
stage / commit / amend / push / PR = 0
helper / validator / consumer / replay / synthetic owner / real audit = 0
retained source or payload reads = 0
qualification / generation / retry / repair / copy / consumption = 0
network / DNS / .env / device / camera / Ray / strip / cleanup / capture = 0
CR3 / NPY / nonzero / predevice / Z0 / E2 / analyzer / formal / TD-C = 0
firmware / deployment = 0
```

The helper and test diffs remain byte-identical, unstaged, uncommitted and
unaccepted. Retained R3 remains `RETAINED_UNVALIDATED_UNCONSUMED`.

## 5. Decision and next branch

```text
REF-P7-25-R2-O3-C1R1 =
  REJECTED_INCOMPLETE_CODEGRAPH_VERBATIM_COVERAGE
helper correction acceptance = 0
retained audit credit = 0
```

CodeGraph was used first and explicitly did not cover the specific required
details. Under the repository CodeGraph rule, C1R2 may carry the verified
response and use only the narrowest raw-source ranges from the exact frozen
target file for the three missing symbols and classification branch. It may
not requery/sync CodeGraph, read the whole file, search other files, or broaden
into implementation analysis.

Successful combined proof may seal a fresh Advisor-decision evidence root, but
still stops at Planner and Advisor. It does not accept or commit the diff,
choose a lineage owner, or unlock retained audit.

## 6. 维护性判断

The next package completes a source-evidence gap without introducing a second
policy implementation or widening source inspection beyond the designated
owner.
