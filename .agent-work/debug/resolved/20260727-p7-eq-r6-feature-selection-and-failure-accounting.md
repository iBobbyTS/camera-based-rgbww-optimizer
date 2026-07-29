# P7 EQ-R6 feature selection 与 failure physical accounting

**状态：** active / pure-offline correction required before any future live retry

## Frozen failure

```text
FAMILY =
  /Volumes/4T/temp/rgbww-optimizer/p7-td-b-exposure-qual-r6-0f36671-20260727T1650
classification =
  runtime_contract_failure_feature_selection_order_owner
candidate-2 launch = 0
retry = 0
Human EQ authorization = consumed
```

RAW report quality本身accepted：

```text
optimization patches = 23
accepted observations = 92
rejected = 0
frozen policy IDs = 58
missing policy IDs = 0
extra non-policy IDs = 34
```

Production candidate capture owner把全部92 observations insertion order直接与58 policy tuple比较，未先筛选/
重排，因此抛`EQ-R6 RAW report feature order differs`。

## Physical accounting gap

```text
candidate-failure.json physical_returned = 0
candidate-result.json physical_returned_cr3_count = 1
terminal-seal.json physical_returned_cr3_count = 1
physical-returns.jsonl rows = 1
```

`candidate-failure.json`在except中先写，physical ledger authoritative recount在finally之后才发生。

## Root-cause hypothesis

两个根因都在：

```text
src/camera_based_rgbww_optimizer/optimization/measure_p7_thermal_diagnostics.py
```

最小修复：

1. 单一EQ-R6 feature-selection helper从完整observations建立唯一ID map，拒绝required duplicate/missing，
   忽略non-policy extras，并严格按frozen policy IDs返回58项；
2. 单一strict physical-ledger count helper在candidate-failure与candidate-result写入前共同使用，保证physical
   return已落盘后任何postprocessing failure都得到同一计数。

## Verification surface

- synthetic 92 -> exact frozen 58 and policy order；
- missing/duplicate required feature fail closed；
- physical return后feature/order或sidecar failure：failure/result/seal/ledger count一致；
- pre-return failure保持0；
- immutable 1650 RAW report read-only replay得到92 source observations、58 selected、0 missing、34 extra；
- 1650 whole-tree manifest before/after exact相等；
- network/device/.env/capture/EQ/public analyzer = 0。

## 2026-07-27 17:34 Planner review：C3 path mismatch

C3未通过Planner验收，唯一拒绝原因是active PLAN §8引用了不存在的
`tests/test_measure_p7_thermal_diagnostics.py`；仓库实际tracked path为
`tests/test_p7_thermal_diagnostics.py`。这属于PLAN路径缺陷，不是当前implementation candidate缺陷。

已接受为完成且不得重跑：

```text
failing-first exact six = Ran 6; pass 1; failures 2; errors 3
post-fix exact six = 6/6
post-fix R6 contract file = 61/61
```

冻结当前continuation state：

```text
HEAD = 0f36671a351d537f204e8bc20849ac83e7e57c2b
source SHA-256 =
  e8d563f894ae0119c7e3970e940570a21fb213cb6d1e542471a55406edbee9a8
test SHA-256 =
  7bbb635eeefcbf17884f4636434bcfe029e54c1c6344d559c40c6fd6f3277468
allowlisted binary diff SHA-256 =
  c4903c3dfb4f5d6f3a9f36909f430bcbce1f6de580a63d557e3a7bfcb96cd5cd
old 1650 manifest SHA-256 =
  fc39fccfc9921600968add879c0f024100b2cd5e6d3d32de18cb962ae6dc393c
```

继续路径是`REF-P7-23-C3E1`：保留现有未提交实现，只用正确focused path完成剩余tests、full suite、
static/CodeGraph、immutable replay、single commit与one-shot evidence seal。不得revert/restart、不得制造
pre-fix source重跑failing-first、不得访问设备或网络。

## 2026-07-27 17:56 Planner review：C3E1 postcommit command

C3E1的implementation、exact/focused/full tests、1650 replay、CodeGraph、static checks和single commit均已
通过。唯一阻塞是PLAN字面命令`git show --name-only --format=HEAD`；当前Git把`HEAD`解释为pretty-format
名称并exit 128。这是PLAN命令语法缺陷，不是commit scope缺陷。

冻结accepted commit：

```text
commit = f37517af3ae25efb41f085904fd48f037980ed04
parent = 0f36671a351d537f204e8bc20849ac83e7e57c2b
subject = fix(p7): select eq-r6 policy features atomically
paths =
  src/camera_based_rgbww_optimizer/optimization/measure_p7_thermal_diagnostics.py
  tests/test_p7_td_b_r6_contract.py
```

独立只读`git diff-tree --no-commit-id --name-only -r HEAD`确认exact two paths。C3E1未amend、未创建第二
commit，evidence owner/root/artifacts均为0，planned root absent，real side effects为0。

继续路径是`REF-P7-23-C3E2`：保留HEAD和commit，不作源码或测试编辑，不重跑tests/replay/CodeGraph/
compileall，只用冻结的有效`git diff-tree`命令完成exact path audit，fresh读取1650 before/after manifest，
然后调用one-shot owner生成exact 12 JSON evidence。future live/device authority保持false。

## 2026-07-27 18:07 Planner final disposition

```text
REF-P7-23-C3E2 = ACCEPTED
REF-P7-23-C3 implementation = ACCEPTED
REV-EQ-R6-C3-PATH-003 = CLOSED
REV-EQ-R6-C3E1-GIT-CMD-004 = CLOSED
REV-EQ-R6-FEATURE-001 = CLOSED
REV-EQ-R6-PHYSICAL-FAILURE-002 = CLOSED
commit = f37517af3ae25efb41f085904fd48f037980ed04
```

Exact-12 evidence及Planner独立审计闭合：

```text
validation SHA-256 =
  3b136148a2571dba893447c0558d9663d08a44ceef59000bd19a1fb22c48dc3c
terminal SHA-256 =
  c50e40e2b28fb0a69aa80e0016b39c06ff79f2818440c9b890417405d1ad309a
1650 before/after canonical SHA-256 =
  fc39fccfc9921600968add879c0f024100b2cd5e6d3d32de18cb962ae6dc393c
mismatches = []
real side effects = 0
```

Feature selection与failure physical accounting根因均已修复并由exact/focused/full、immutable replay、
fake accounting、single-caller CodeGraph和sealed evidence覆盖。调试记录移至resolved。

下一路线不是自动live retry：1650已消耗先前Human EQ authorization，所有后续PLAN均明确
`future live authorized=false`。必须先取得Human对一个fresh bounded EQ-R6 attempt的明确授权，再由Planner
另写live executable PLAN。Advisor科学分支没有新歧义，无需Advisor介入。
