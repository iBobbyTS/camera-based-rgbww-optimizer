# REF-P7-25-R2-B1A-C3E5D2 / Focused lineage owner review

**Planner 日期：** 2026-07-29

**Reviewed contract：**
`P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E5D2-CHECKOUT-TEST-ONLY-V1`

**Decision：**
`REJECTED_CHECKOUT_FIX_ACCEPTED_FOCUSED_LINEAGE_TEST_AMBIENT_HEAD_DEFECT`

## 1. Frozen evidence

```text
root = /Volumes/4T/temp/rgbww-optimizer/
  p7-td-b-retained-r3-option-b-b1a-c3e5d2-offline/20260729T182407Z
baseline-summary.json SHA-256 =
  733b62dd546273d47a4ef0d367cf8c52ef2f5abf5db9bf14eeb33672f7c7a60d
test-only-edit.json SHA-256 =
  bdc0a71b36947ca31b5b4cc8da7f1e03f38d09c311cb77aec318a885dba54d21
post-exact3-summary.json SHA-256 =
  0342ebad1a5939acd6e2610d52e666728e62aecaca55f843360f8de23112441e
focused-summary-recovered.json SHA-256 =
  1e96bfd665bdff5083eecd1661aa0e932d23b40c744d145a48ee10134ccf4781
validation-summary.json SHA-256 =
  42adc53045f10830ddb8879ba402b7482dd775aaf0dfd51f14c76972024abd8d
terminal-summary.json SHA-256 =
  44673a30d9153bbb43b621d4b006f1a41e135515c1e2f0eb12b1823debc9d628
EXECUTION_RESULT.md §60 SHA-256 =
  ce737cd2cafe992f58b9e32a6abf723bb9ccaef5703b764a73469425b2769e4c
reviewed PLAN SHA-256 =
  2ae48a2dbec894bdd6b3a096bdb0078769c99cfc65c8e7a4b2f3163a44997d3c
HEAD = 9303aa22a9bd37e8ec4f23147c78c6bea84b9a2e
staged paths = 0
```

Baseline exact 2-pass/1-fail匹配；checkout test-only edit从
`a126c60d97d0cb19eb96ce1665da357e69cdad2650a68a89ed129f93d25d9da7`变为
`2887abf4bca70b76ef82ca78f9e28dcee8371e6bf6ab4e203926bb36ca8749e5`，minimal diff SHA
`d5616a397a4eb26c3ce962bf0aaae9fb288c3d4e647d6e04bf14f84b89939c21`。Post exact-three 3/3 pass。

Focused真实运行102 tests、1 failure、0 errors；recovered summary只封已有完整raw evidence，test rerun0。Production edits、full、stage、
commit、manifest和R3 reads均0。

## 2. Independent lineage diagnosis

唯一failure：
`P7ThermalDiagnosticsTests.test_post_eq_policy_lineage_classifies_only_exact_accepted_paths`。

该test使用cleanroom ambient `git rev-parse HEAD`作为`new_checkpoint`，再硬编码`len(changed_paths) == 59`。当前ambient HEAD
`9303aa22...`相对setup checkpoint的changed paths为61；现有production owner明确冻结：

```text
TD_B_SETUP_CHECKPOINT = 9c804abdeabbc5da18a66d0acf25a1f13128bc2d
TD_B_POST_EQ_POLICY_COMMIT = 161094ffa2bf1f84ed1fc787e708e8c3463f10db
git diff --name-only <setup> <post-eq commit> count = 59
git diff --name-only <setup> <ambient HEAD> count = 61
```

故59不是当前ambient HEAD的有效断言。Test应绑定已存在的explicit post-EQ checkpoint owner，并以该checkpoint计算的exact path set作为
path-set owner，而不是另写数量常量。Checkout修正已由targeted pass验证，必须保留。

## 3. Fresh successor

下一包继续test-only。Fresh root先重建base candidate和exact external fixtures，再以C3E5D2 retained test source exact hash
`2887abf4...49e5`保留checkout修正。Edit前必须证明existing owner唯一：setup owner、post-EQ commit owner、其Git identity与两者间exact
path set；若不唯一立即停止。

只允许同一`tests/test_p7_thermal_diagnostics.py`修正lineage test：new checkpoint取existing explicit post-EQ constant，path set从explicit
old/new checkpoint计算；断言candidate实际path set与该explicit intended set一致，删除ambient HEAD与hardcoded count。不得硬编码59/61、
不得改production或放宽prohibited/classification/hash检查。

Post targeted必须覆盖checkout manifest test与lineage test，恰好一次；通过后focused恰好一次。Full、stage、commit、manifest、R3、
production edit均0。无Advisor/Human gate。

建议FULL记录C3E5D2 checkout fix accepted、focused lineage test failure，并激活fresh test-only successor；candidate base、checkpoint、release与
`RETAINED_UNVALIDATED_UNCONSUMED`保持不变。
