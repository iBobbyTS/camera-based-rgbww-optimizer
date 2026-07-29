# REF-P7-25-C2E1 Planner Review / Full-discovery invocation hard stop

**Review time:** 2026-07-27 22:13 MDT

**Reference task:** `REF-P7-25-C2E1`

**Reviewed contract:** `P7-TD-B-POST-EQ-LINEAGE-PATH-CLASSIFICATION-C2E1`

**Decision:** `REJECTED_FULL_DISCOVERY_INVOCATION`

## 1. Frozen review inputs

```text
HEAD =
  cc6dbd356dec20eca1437b6c282358c3f2a5e5c7
parent =
  161094ffa2bf1f84ed1fc787e708e8c3463f10db
tree =
  2d64be148c7c0033ab19a06424c54b92064ea76f
subject =
  fix(p7): classify accepted post-eq lineage paths
PLAN SHA-256 =
  43e6f87b82595091d5c85380c67997243a1fe196bf10ba23fd14d3e49aa000e3
FULL_PLAN_REFERENCE SHA-256 =
  cc0190e862e8149d8eafe6ef160c326ec2aa53fd5804fbfd0f76acfe451e528a
EXECUTION_RESULT SHA-256 =
  885d71e5b7c2d560c513289d950b6a80189635f302db276312e054c86b8b2dd0
reviewed EXECUTION_RESULT section =
  §159
```

The Planner independently confirmed the retained worktree change is exactly one unstaged test path:

```text
tests/test_p7_thermal_diagnostics.py
diffstat = 4 insertions / 3 deletions
binary diff SHA-256 =
  b69ce4e60a82b23e214daa5dc5fed2fe982c3c03f49a15103f6044a7fddebb58
working file SHA-256 =
  7ccc64a1f3182a0860b01dcc159f5b2ef505193fae9d2add41cbc161b49e5c7a
```

The production/config owners remained byte-identical:

```text
src/camera_based_rgbww_optimizer/optimization/p7_thermal_diagnostics.py =
  61033c79e51a046ecce4f26b06bc2b10427350b10733967e72b109e506f835d9
config/hsi/p7-ray-td-b-exposure-policy-v2.json =
  c9080d18571f617cb7d323ade843ff9c86bf92e3795d23e3999e26d413968681
tests/test_p7_td_b_r6_contract.py =
  10374ec2366fc8cbe928953690defc31c83dc5c04da192f599f59591ec196f23
```

## 2. Reviewed execution and validation quality

The package correctly completed and recorded:

```text
failing-first = 2 run / 0 errors / 1 expected failure
corrected focused = 2/2 pass
lineage/candidate/release-selection = 13/13 pass
affected suites = 145/145 pass
git diff --check = pass
target checkpoint command independently returned b"drift"
drift injection assertion = exactly 1
production/config edits = 0/0
```

The retained correction is narrow and matches the C2E1 design: it binds the mock to the exact target-checkpoint
`git show` command, returns drift independently of the accepted-commit identity, delegates all other subprocess calls
to the original implementation, and proves the injection fired once.

The next command was invoked as:

```text
.venv/bin/python -m unittest discover -v
exit = 5
tests run = 0
output = NO TESTS RAN
```

This omitted the repository's established discovery root. The required full command is:

```text
.venv/bin/python -m unittest discover -s tests -v
```

Although the observed result is an invocation error rather than a code-test failure, C2E1 explicitly required any
full-discovery failure to stop without rerunning that gate. The Executer complied with the hard stop: it did not
rerun, commit, acquire evidence, amend production, or enter release/device/later-stage work.

## 3. Planner findings

```text
REV-C2E1-001 = accepted finding
class = execution-contract / validation invocation
cause = missing "-s tests" discovery root
scientific or production defect = no evidence
retained test diff disposition = reviewable but not accepted under C2E1
```

The package is not acceptable because:

1. the required full validation did not run;
2. C2E1's own stop contract forbids correcting that invocation inside the failed package;
3. no commit, postcommit gate, or one-shot evidence seal exists;
4. therefore the production correction checkpoint remains unaccepted and R3 release remains locked.

No Advisor or Human decision is needed. This is a bounded pure-offline validation-continuation decision.

## 4. Decision and retained evidence

```text
REF-P7-25-C2E1 = REJECTED_FULL_DISCOVERY_INVOCATION
HEAD cc6dbd3 = retained_not_accepted
test-only worktree diff = retained_uncommitted_reviewed_input
C2E1 evidence root = absent
commit/amend/retry = 0/0/0
release generation/consumption = 0/0
device/network/formal = 0/0/0
```

The failing-first, corrected focused, lineage/candidate/release-selection, affected-suite, and `git diff --check`
results are final evidence of C2E1. They must not be repeated by the continuation merely to erase the hard stop.

## 5. Exact next branch

Create `REF-P7-25-C2E2` under contract
`P7-TD-B-POST-EQ-LINEAGE-PATH-CLASSIFICATION-C2E2`.

The continuation must:

1. require the exact retained one-path diff and hashes above;
2. permit no additional test or production edit;
3. consume the already-reviewed C2E1 checks without rerunning them;
4. begin executable validation at:

   ```text
   .venv/bin/python -m unittest discover -s tests -v
   ```

5. if full/static/CodeGraph checks pass, create exactly one test-only commit;
6. run the exact postcommit focused gate once;
7. acquire and seal one new C2E2 evidence root once;
8. stop for Planner review with release/device/network/formal routes still locked.

If the retained diff identity, HEAD, production bytes, immutable roots, or prior evidence differ, the continuation
must stop rather than repair, edit, reset, or reconstruct them.

## 6. Residual risks

- Full discovery, compileall, static scans, and CodeGraph final exploration remain unexecuted.
- The retained test diff is not committed and must be consumed only after exact identity verification.
- Postcommit focused validation and canonical evidence do not yet exist.
- The R3 release candidate must not be generated or consumed until a later Planner acceptance.

## 7. Maintainability judgment

The retained change is confined to one test-owned subprocess seam; production lineage ownership and exact provenance
gates are unchanged. The next package needs validation and evidence continuation only, with no refactor or new
abstraction.
