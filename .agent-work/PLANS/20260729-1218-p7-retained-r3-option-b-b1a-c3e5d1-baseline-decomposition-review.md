# REF-P7-25-R2-B1A-C3E5D1 / Baseline decomposition review

**Planner 日期：** 2026-07-29

**Reviewed contract：**
`P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E5D1-FOCUSED-DIAGNOSTIC-V1`

**Decision：**
`ACCEPTED_FAIL_CLOSED_BASELINE_DECOMPOSITION_TEST_ONLY_SUCCESSOR`

## 1. Frozen evidence

```text
root = /Volumes/4T/temp/rgbww-optimizer/
  p7-td-b-retained-r3-option-b-b1a-c3e5d1-offline/20260729T181621Z
baseline-exact3-summary.json SHA-256 =
  35e6c2374a24374bc6c7c097cc645fcacaafa194fd89bc7128f118d7870e7846
validation-summary.json SHA-256 =
  48f95da555990eb7e57f9b0beeccba391c67a4c77a62d317587c7e219f70ce31
terminal-summary.json SHA-256 =
  ea6b775ca4903e7070e4f1eca9027903c85e9e49ceb8da8e063d20635692a779
EXECUTION_RESULT.md §59 SHA-256 =
  e00fcf7c6c9b9ef32968ae28d73a91140010b7804d93bd32a37e9ee574f794a7
reviewed PLAN SHA-256 =
  edbc02baffcff0ab18b0b5bcdad86780c64dddd5949af56f6222be936db614d1
HEAD = 9303aa22a9bd37e8ec4f23147c78c6bea84b9a2e
staged paths = 0
```

Candidate五路径、full-index patch、两个external fixture source/copy gates均pass。Fixtures strict JSON、stable、无symlink、无forbidden
keys、exact hashes且只存在fresh root；candidate/stage/commit均0。

## 2. Baseline result

Exact-three实际结果：Ran 3、2 pass、1 failure、0 errors。

```text
PASS test_p6_historical_seed_is_rebuilt_as_seed_only
PASS test_p6_historical_seed_tampering_falls_back_without_seed
FAIL test_subordinate_manifest_positive_and_fail_closed_matrix
```

唯一failure仍是synthetic `git checkout --detach`成功后Git正常在stderr输出`HEAD is now at ...`，而helper错误要求stderr为空。
因此C3E5D1按“必须exact三fail才edit”的合同正确no-edit stop。它同时消除了historical candidate defect假设：补齐exact local fixtures后，
两条historical tests均pass，不再需要production诊断或allowlist。

## 3. Fresh successor

下一包必须冻结baseline expected outcome为上述2 pass + 1 named fail，使用fresh root与同一两个exact external fixtures。只允许编辑
`tests/test_p7_thermal_diagnostics.py`：Git subprocess仍以`check=True`/exit0 fail closed；不再断言stderr为空；checkout后以
`git rev-parse HEAD`断言full exact HEAD等于requested commit。Production edits与historical allowlist均为0。

修正后exact-three运行一次并须3/3 pass；随后focused运行一次并须pass。Full、stage、commit、manifest、R3 reads、real audit、
eligibility与release均0。无Advisor/Human gate。

建议FULL把C3E5D1记录为accepted fail-closed decomposition，并激活test-only successor；candidate SHA、checkpoint、release与
`RETAINED_UNVALIDATED_UNCONSUMED`保持不变。
