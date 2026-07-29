# REF-P7-25-C2 / Post-EQ lineage path classification review

**Planner decision：** `REJECTED_POSTCOMMIT_FOCUSED_TEST`

**Review time：** 2026-07-27 22:04 MDT

**Reviewed contract：** `P7-TD-B-POST-EQ-LINEAGE-PATH-CLASSIFICATION-C2`

**Reviewed PLAN SHA-256：**
`9d7c58aeee42bad00e6b3084b7e65bf3aec5087bcbaff753ccaeaf8a4ba472b6`

**Reviewed EXECUTION_RESULT SHA-256：**
`5d4e5cfdf4251431071b16efeff3d60290b4103424b125882e1c8ad102e8134c`

**Reviewed handoff：** `.agent-work/EXECUTION_RESULT.md` §159

## 1. Reviewed scope and method

Planner independently compared §159 with the active PLAN, inspected the exact correction commit and its two-path
diff, and verified the reported current Git checkpoint:

```text
HEAD =
  cc6dbd356dec20eca1437b6c282358c3f2a5e5c7
parent =
  161094ffa2bf1f84ed1fc787e708e8c3463f10db
tree =
  2d64be148c7c0033ab19a06424c54b92064ea76f
subject =
  fix(p7): classify accepted post-eq lineage paths
changed paths exact =
  src/camera_based_rgbww_optimizer/optimization/p7_thermal_diagnostics.py
  tests/test_p7_thermal_diagnostics.py
```

The review did not rerun tests, mutate production/test files, acquire evidence, qualify or generate a release, access
devices/network, or run the public analyzer/formal route.

## 2. Accepted implementation evidence

The implementation remained inside the existing lineage candidate owner:

```text
exact new classifications =
  config/hsi/p7-ray-td-b-exposure-policy-v2.json
    -> accepted_post_eq_exposure_policy_contract
  tests/test_p7_td_b_r6_contract.py
    -> accepted_post_eq_exposure_policy_validation
accepted commit / parent / subject / exact path set = frozen
accepted blobs = frozen exact three paths
target/live equality = exact two mapped paths
generic production/validation allowlist additions = 0
prefix/suffix/glob matching = 0
```

The exact config and R6 contract test remain absent from the correction diff and retain their accepted SHA-256:

```text
config policy =
  c9080d18571f617cb7d323ade843ff9c86bf92e3795d23e3999e26d413968681
R6 contract test =
  10374ec2366fc8cbe928953690defc31c83dc5c04da192f599f59591ec196f23
```

Recorded precommit validation quality:

```text
failing-first = 1 run / 0 errors / 1 expected failure
new focused = 2/2 pass
lineage/candidate/release selection = 13/13 pass
affected suites = 145/145 pass
full unittest discovery = 641 tests / exit 0
compileall / git diff --check = pass / pass
secret / generic allowlist / allowlist mutation scans = pass
CodeGraph sync and focused owner/call-path exploration = pass
```

These results support retaining commit `cc6dbd3`; they do not override the mandatory postcommit gate.

## 3. Rejection finding

The sole required postcommit focused run was:

```text
run / errors / failures = 2 / 0 / 1
exit = 1
positive exact-classification test = pass
negative test =
  test_post_eq_policy_lineage_fails_closed_without_widening
failure =
  AssertionError: ValueError not raised
expected regex =
  checkpoint blob differs
```

The failure is reproducible from the committed test seam: `drift_checkpoint` injects drift only on the second
occurrence of `git show <checkpoint>:<mapped_path>`. Before the correction commit, accepted commit and current
checkpoint were the same, so that command occurred twice. After the commit, accepted commit remains `161094f` while
current checkpoint is `cc6dbd3`; the target-checkpoint command occurs once and the mock never injects drift.

This is a test-owned pre/postcommit identity assumption. It does not establish a production helper defect, but the
PLAN explicitly made any postcommit focused failure a hard stop. Therefore:

```text
REF-P7-25-C2 = REJECTED_POSTCOMMIT_FOCUSED_TEST
changed-path correction checkpoint = retained_not_accepted
R3 release generation = locked
```

The original C2 evidence root remained absent, and controller source build/SHA/compile/exec/acquisition were all zero.
No evidence artifact can be accepted for C2.

## 4. Safety and accounting

Accepted zero boundaries:

```text
release qualification/generation/validation/consumption = 0/0/0/0
release retry/second release = 0/0
device/network/DNS/hostname/.env = 0/0/0/0/0
camera/Ray/strip/all_off/cleanup/capture = 0/0/0/0/0/0
CR3/NPY/nonzero output = 0/0/0
public analyzer/predevice/Z0/E2/formal R6/TD-C = 0/0/0/0/0/0
firmware/deployment = 0/0
amend/push/second commit = 0/0/0
residual owned process = 0
```

Old C1 roots remained immutable with the exact before/after manifests reported in §159.

## 5. Residual risk and exact next branch

Residual risk is limited to the negative test not actually exercising checkpoint-blob drift when accepted commit and
current checkpoint differ. The next package must:

1. keep `cc6dbd3` and its production implementation unchanged;
2. reproduce the current focused failure before editing;
3. edit only `tests/test_p7_thermal_diagnostics.py`;
4. make checkpoint drift injection match the exact target-checkpoint command independently of accepted-commit calls;
5. prove the mock fired exactly once and that the real helper raises `checkpoint blob differs`;
6. rerun focused, affected, full and static validation;
7. create at most one new test-only commit, never amend `cc6dbd3`;
8. acquire one fresh offline evidence root once, seal it once, and stop;
9. keep release, device, network, analyzer, formal and later-stage work locked.

No Advisor or Human decision is required. This is a bounded pure-offline test-seam and evidence correction.

## 6. Maintainability

The retained production mapping has one existing lineage owner and explicit ancestry/blob gates. The correction should
stay local to one test mock and add no production abstraction. Follow-up refactoring is not warranted.
