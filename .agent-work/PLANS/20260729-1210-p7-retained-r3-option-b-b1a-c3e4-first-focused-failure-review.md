# REF-P7-25-R2-B1A-C3E4 / First real focused failure review

**Planner 日期：** 2026-07-29

**Reviewed contract：**
`P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E4-PATCH-ARGV-STATUS-V1`

**Decision：**
`REJECTED_FIRST_REAL_FOCUSED_FAILURE_REQUIRES_BOUNDED_ENGINEERING_DIAGNOSTIC`

## 1. Frozen evidence

```text
root = /Volumes/4T/temp/rgbww-optimizer/
  p7-td-b-retained-r3-option-b-b1a-c3e4-offline/20260729T180615Z
focused-unittest-summary.json SHA-256 =
  99f4ccfca0a09bad4da64f07dd9553a6b0fc54f99dc697f3d1e1d20723508ba2
focused-unittest.stdout SHA-256 =
  60a99296cd05148e61f81c360fe8fb1aa67ccb17228015fa6b728da41fe860ab
focused-unittest.stderr SHA-256 =
  d48afe3d563289f82907c159f05dd40904ecc2ec7448770a5670ebcc96efafff
import-identity-summary.json SHA-256 =
  5452bf9b235acd704bb3e6c6545d670622f4865a90e1a7abb3c2ab5ea76b904e
validation-summary.json SHA-256 =
  a45be1eae0bddbb1751ba8570333d90e18446a5af968243fb67fea6fbdc0c571
terminal-summary.json SHA-256 =
  210ca3ac516bbab479eb4a588d7bdebc31ef6e6d41c85d21ece6751d14371920
EXECUTION_RESULT.md §58 SHA-256 =
  bc7633d6388e587c4586ec01c879a7799e9befab2722d03577f2a25545626b24
reviewed PLAN SHA-256 =
  aa1b891daffd40e0060c6669c9ba3c61a821ffd009a172c70a62b51ebbe0bf2b
HEAD = 9303aa22a9bd37e8ec4f23147c78c6bea84b9a2e
staged paths = 0
```

Runtime、row-policy、FULL 12-key subset、candidate load、source evidence-before-compare、materialization、canonical full-index patch、
clone aggregate status与cleanroom import identity全部通过。Candidate edit0。Full/stage/commit/manifest/R3 reads均0；所有network/
device/formal锁定面调用为0。

## 2. Focused result classification

Focused unittest首次真实运行102 tests，结果为3 failures、66 errors。

66 errors主要来自clean clone缺少两个shared worktree中存在但Git未跟踪且被`config/*`忽略的local inputs：

```text
config/location/locations-20260714-211759.json
  bytes = 14769
  SHA-256 = 21f02328bff8b5ffcfc10c767e15cdefbf8bb883bc352eff6f0fb7ade38a8f80
config/channel/code-duty-curve.json
  bytes = 24058
  SHA-256 = 0b03ce50bda13112c95d64d1f5974991514067bbd9f48e920214654c122ff911
```

它们不是candidate repository paths；不能因测试缺失而盲目并入candidate、Git或最终commit。Fresh successor必须先把其身份、
strict JSON、stable read、无symlink、用途与敏感字段风险验证为exact external fixture inputs，且只复制到fresh diagnostic root。

三个failures为：

1. `test_p6_historical_seed_is_rebuilt_as_seed_only`：`historical_seed_usable`实际false；
2. `test_p6_historical_seed_tampering_falls_back_without_seed`：baseline同样false；
3. `test_subordinate_manifest_positive_and_fail_closed_matrix`：synthetic `git checkout --detach`成功，但Git正常把
   `HEAD is now at ...`写到stderr，test helper错误要求stderr为空。

第三项是明确test defect：synthetic checkout只能断言exit success与checkout后的exact HEAD，不得要求stderr为空。前两项尚不能
判为candidate defect；必须持久化audit reason与source identities，区分外部historical evidence漂移、环境缺失与deterministic code defect。

## 3. Successor branch

下一包是fresh-root bounded engineering diagnostic/correction，不是C3E4 retry，也不直接恢复B1A commit流程。它必须：

- 先验证并seal上述两个exact external fixture inputs，安全通过后才只复制到fresh root；不得加入candidate/stage/commit；
- 在补fixture后的fresh candidate cleanroom隔离复现exact three failures；
- 在`tests/test_p7_thermal_diagnostics.py`修正synthetic checkout assertion为exit/HEAD contract；
- 对两条historical seed failure记录完整root cause；仅当证明是candidate deterministic code defect时，才可在显式
  `p7_thermal_diagnostics.py`加对应test的二路径allowlist内纠偏；环境/evidence问题则不改production并停Planner；
- correction后只运行exact three targeted tests一次，再运行fresh focused一次；full/commit/manifest/R3均0；
- 若出现科学阈值或解释选择才停Advisor，否则仍由Planner/Orchestrator处理。

建议FULL将C3E4记录为首次真实focused hard-fail，programmatically激活diagnostic successor；candidate、checkpoint、release与
`RETAINED_UNVALIDATED_UNCONSUMED`不变。
