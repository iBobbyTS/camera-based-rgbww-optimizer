# REF-P7-23-C3 / EQ-R6 feature selection and failure accounting correction

**计划状态：** `executable_pure_offline_code_test_evidence`

**Planner 日期：** 2026-07-27

**Reference task ID：** `REF-P7-23-C3`

**Parent reference task：** `REF-P7-23`

**PLAN contract ID：** `P7-TD-B-EQ-R6-FEATURE-SELECTION-PHYSICAL-ACCOUNTING-C3`

**Package kind：** `bounded_pure_offline_code_test_commit_evidence`

**Expected starting HEAD：** `0f36671a351d537f204e8bc20849ac83e7e57c2b`

`PLAN_MACHINE_CONTRACT={"schema":"planner_execution_contract_v1","contract_id":"P7-TD-B-EQ-R6-FEATURE-SELECTION-PHYSICAL-ACCOUNTING-C3","reference_task_id":"REF-P7-23-C3","parent_reference_task_id":"REF-P7-23","package_kind":"bounded_pure_offline_code_test_commit_evidence","expected_starting_head":"0f36671a351d537f204e8bc20849ac83e7e57c2b","single_current_action":"repair_one_eq_r6_policy_feature_selection_owner_and_one_authoritative_physical_failure_count_owner_then_test_commit_and_seal_once","source_allowlist":["src/camera_based_rgbww_optimizer/optimization/measure_p7_thermal_diagnostics.py"],"test_allowlist":["tests/test_p7_td_b_r6_contract.py"],"commit_authorized":true,"commit_cap":1,"device_access":0,"network_access":0,"dns_access":0,"env_access":0,"camera_access":0,"ray_access":0,"strip_access":0,"cleanup_access":0,"capture_access":0,"eq_access":0,"public_analyzer_access":0,"old_1650_mutation":0,"evidence_owner_invocation_cap":1,"evidence_root_acquisition_cap":1,"retry":0,"second_evidence_generator":0,"alternative_root":0,"same_root_repair":0,"human_eq_authorization_consumed_by_1650":true,"future_live_authorized":false,"advisor_required":false,"planner_stop_required":true}`

**当前唯一动作：** 只在两个allowlisted tracked files中完成一个bounded correction：

```text
complete RAW observations
-> unique ID map
-> select frozen 58 IDs
-> emit exact policy order

physical-return ledger
-> one strict authoritative recount
-> candidate-failure and candidate-result use identical count
```

随后完成failing-first tests、fresh regression、1650 read-only replay、一个focused commit和一个non-circular
12-artifact evidence seal。

**唯一 Planner 停止点：** 任一reproduction、test、replay、immutability、commit scope或evidence seal失败立即
stop并handoff；不得修好后在同root补写或第二次生成。全部通过也必须停回Planner，不得设备访问、重试1650、
运行public analyzer或写live PLAN。

## 1. Live review decision

```text
REF-P7-23 = REJECTED_BRANCH_D_RUNTIME_FEATURE_SELECTION_CONTRACT
REV-EQ-R6-FEATURE-001 = OPEN
REV-EQ-R6-PHYSICAL-FAILURE-002 = OPEN
1650 FAMILY = immutable
Human EQ authorization = consumed
future live authorization = not inferred
```

Review archive：

```text
.agent-work/PLANS/20260727-1721-p7-eq-r6-live-1650-runtime-contract-failure-review.md
SHA-256 868d6d17d53235d1224918173d5fb3a18df0f2af412fd43420c6d4dd02c62432
```

Active debug：

```text
.agent-work/debug/active/20260727-p7-eq-r6-feature-selection-and-failure-accounting.md
SHA-256 647698a5f65cc3e61024abab02dcedcd293f7e9c77f0c360868e1e723145a16c
```

本包是ordinary offline code correction，不需要Advisor或Human authorization。它不恢复future live authority。

## 2. Exact scope and allowlist

允许tracked edits：

```text
src/camera_based_rgbww_optimizer/optimization/measure_p7_thermal_diagnostics.py
tests/test_p7_td_b_r6_contract.py
```

允许untracked/external writes：

```text
/Volumes/4T/temp/rgbww-optimizer/p7-td-b-eq-r6-c3-offline-0f36671-20260727T1721
.agent-work/EXECUTION_RESULT.md append-only handoff
```

禁止修改或stage：

```text
.agent-work/PLAN.md
.agent-work/FULL_PLAN_REFERENCE.md
.agent-work/debug/**
.agent-work/PLANS/**
advisor/**
GUIDE / RESEARCH
docs/**
.agents/skills/**
config/**
tmp/**
firmware/**
all other src/** and tests/**
```

禁止新增parallel analyzer、feature policy、device owner、wrapper或execution framework。

## 3. Frozen inputs

```text
starting HEAD =
  0f36671a351d537f204e8bc20849ac83e7e57c2b
source pre-edit SHA-256 =
  b58fb6c314dcf3ad17241690ffa66cd1b0bb01776321d438af2dd318a79f2ccb
test pre-edit SHA-256 =
  240c30d894c911a82a0c46193672900e470454c299e6d53f12386a003b201dff
policy SHA-256 =
  9e5ec953fdeedf0e73a26a3a476b7336febdbdb2c3e83819123c7b9ad4060ec2
```

Orchestrator dispatch时必须给出exact：

```text
C3_PLAN_SHA256
C3_FULL_SHA256
C3_EXECUTION_RESULT_START_SHA256
```

缺一或current path/hash不符立即stop。PLAN不能自嵌自身hash。

1650 immutable inputs：

```text
FAMILY =
  /Volumes/4T/temp/rgbww-optimizer/p7-td-b-exposure-qual-r6-0f36671-20260727T1650
RAW report =
  FAMILY/run/candidate-1/measurements/000-ray-c2500-t60.patch-statistics.json
RAW report SHA-256 =
  c45d5838c391ff9a2347da260f406eda8284fdb6cbec929050feed9cfe205acd
candidate-failure SHA-256 =
  81518238cb79f3ed1357181734e0ad083c5013af57459626365f47d3bf235348
candidate-result SHA-256 =
  40c3bf9f6db9ca382581748eeffa5d58f2c913be80a446f65ab0d4e848803947
terminal-seal SHA-256 =
  40784653669303d5d8ced882bffc11871c1183f28690150572896c6050698021
physical-returns JSONL SHA-256 =
  f77ab60bb920335ad912a806c35da12401979567625714ffa63cf6fac69497c4
CR3 SHA-256 =
  281ec241bf92ac9f0da9f5f3539f9b76e08c1bbdcaf99cba60328cee1746e2fa
sidecar SHA-256 =
  1f270c4e50aee2f751e10bcaf0da7a14c07efcb9d59e6511faf9589e16998a86
```

开始与结束都必须对1650 whole tree做path/type/mode/bytes/SHA-256 manifest；exact相等。

## 4. Zero-side-effect boundary

整个package必须保持：

```text
network / DNS / hostname / .env read = 0
real backend / device / camera / Ray / strip = 0
real all_off / cleanup / final-zero = 0
capture / CR3 creation / NPY / TIFF = 0
Terminal / outer / wrapper / EQ / retry = 0
public analyzer / release / strip stage / TD-C = 0
firmware / deployment = 0
old 1650 writes = 0
```

测试只能使用fake/injected adapters和external scratch。任何real dependency call必须tripwire fail。

## 5. Defect A — single policy feature-selection owner

Owner location：

```text
run_td_b_eq_r6_production_candidate.capture
```

在同一source file内增加一个private helper；不得改`hsi_objective.py`、policy或RAW collector。

Helper contract：

1. 输入完整`collection["observations"]`与frozen policy IDs；
2. policy IDs必须non-empty、string、unique；
3. 每个observation必须有唯一non-empty `feature_id`；任何duplicate都fail closed，不得dict-last-win；
4. 建立by-ID map后，只选择policy IDs；
5. missing required IDs必须列出并fail closed；
6. non-policy extras允许存在并被忽略；
7. 返回值必须严格按policy IDs顺序；
8. selected count必须恰好58，order tuple与policy tuple byte-for-byte相等；
9. downstream `feature_quality`只从selected map构建；
10. 不改变statistic owner：
   `statistics.normalized_per_second.trimmed_mean`；
11. 不改变quality/clipping/low-signal分类阈值。

1650 replay acceptance：

```text
source accepted observations = 92
selected policy observations = 58
missing = 0
extras = 34
selected order = exact frozen policy order
first selected = block_03::G1
all selected values/metrics equal source observation by ID
```

不得把extra34标为quality failure，也不得允许missing/duplicate。

## 6. Defect B — authoritative physical failure count

在同一source file内增加一个private strict ledger-count helper：

```text
input = candidate root
authority = physical-returns.jsonl
no file = 0
regular non-symlink and contained
every non-empty line = strict JSON object
physical_index = exact contiguous 1..N
duplicate capture_id/physical_index = fail closed
return = N
```

Restructure candidate failure ownership：

1. `except`只保留primary failure，不立即写stale `candidate-failure.json`；
2. `finally`完成现有Python cleanup，保持original failure precedence；
3. cleanup后调用strict ledger-count helper一次，得到authoritative physical count；
4. 若failure非空，exclusive/atomic写一次candidate-failure，使用authoritative count；
5. candidate-result使用同一authoritative count；
6. failure/result/terminal seal/physical ledger必须一致；
7. sidecar validation failure仍保留已返回CR3并计为physical return；
8. pre-return failure保持0；
9. 不回写、不repair candidate-failure，不增加第二failure owner。

保持existing field names/schema，除非测试证明schema必须最小扩展；任何扩展需在handoff明确请求Planner审查，
不得自行扩大。

## 7. Failing-first regression tests

在test allowlist中新增exact六个meaningful methods：

```text
test_eq_r6_full_raw_observations_select_exact_policy_order
test_eq_r6_feature_selection_rejects_missing_required_id
test_eq_r6_feature_selection_rejects_duplicate_observation_id
test_eq_r6_post_return_feature_failure_counts_physical_atomically
test_eq_r6_sidecar_failure_counts_physical_in_failure_and_result
test_eq_r6_pre_return_failure_keeps_all_physical_counts_zero
```

执行顺序：

1. 写tests；
2. 对pre-fix source运行exact六个tests；
3. 至少A positive与post-return accounting test必须按原始症状fail；
4. 记录完整failure摘要；
5. 才可改source；
6. 改source后六个必须`6/6` pass，无skip。

Tests必须断言真实values/order/counts，不得只执行代码。

## 8. Fresh regression contract

修复后运行：

```text
exact new methods = 6/6
tests/test_p7_td_b_r6_contract.py = 61/61
focused EQ/RAW/thermal suite = no failures, no skips
full unittest discover = 634/634
python -m compileall =
  src/camera_based_rgbww_optimizer/optimization/measure_p7_thermal_diagnostics.py
CodeGraph sync and blast-radius inspection
git diff --check
```

Focused suite至少包含：

```text
tests/test_p7_td_b_r6_contract.py
tests/test_hsi_objective.py
tests/test_measure_p7_thermal_diagnostics.py
tests/test_analyze_p7_thermal_diagnostics.py
```

若baseline discovery因仓库已有新增测试而不是`634`，不得偷偷改期望；记录before/after exact count并请求
Planner判断。任何new skip、xfail或warning-as-pass不可接受。

## 9. 1650 read-only replay

不得运行public analyzer。只调用新private feature-selection helper和strict ledger helper：

```text
RAW collection statistic = frozen no-ambient statistic
source observations = 92
selected = 58
missing = 0
extras = 34
order/hash = policy exact
selected values/metrics = source by-ID exact
old physical ledger strict count = 1
old candidate-failure remains 0
old result/seal remain 1/1
```

最后三行证明old defect而不是repair old artifacts。New fake regression必须证明新code对同类post-return failure生成
`1/1/1/1`。

Replay before/after whole-tree manifest必须exact相等；不得touch atime作为acceptance input。

## 10. Commit contract

所有tests/replay/diff/CodeGraph通过后，允许一个focused commit：

```text
git add -- \
  src/camera_based_rgbww_optimizer/optimization/measure_p7_thermal_diagnostics.py \
  tests/test_p7_td_b_r6_contract.py

git commit \
  -m "fix(p7): select eq-r6 policy features atomically" \
  -m "Filter complete RAW observations to the frozen policy order and keep candidate failure physical-return counts aligned with the authoritative ledger."
```

Commit cap=1；禁止`git add -A`、amend、第二commit、push或PR。Commit必须exact two paths，无PLAN/FULL/debug/
archive/evidence。提交后重新运行exact six tests和`git diff --check`。

## 11. One-shot evidence owner

```text
SAFE_PARENT =
  /Volumes/4T/temp/rgbww-optimizer
NEW_ROOT =
  /Volumes/4T/temp/rgbww-optimizer/p7-td-b-eq-r6-c3-offline-0f36671-20260727T1721
```

开始必须absent/non-symlink。所有implementation/test/replay成功且commit完成后，只调用一个one-shot owner一次：

```text
owner invocations = 1
root acquisitions = 1
retry / second generator / alternate root / repair = 0
```

Exact 12 JSON：

```text
01-frozen-inputs.json
02-1650-tree-before.json
03-failing-first-reproduction.json
04-implementation-and-commit.json
05-targeted-tests.json
06-regression-tests.json
07-feature-selection-replay.json
08-physical-accounting-matrix.json
09-codegraph-and-static-audit.json
10-1650-tree-after.json
11-validation-summary.json
12-terminal-summary.json
```

Required：

```text
root mode 0700; files mode 0600
regular non-symlink, contained
strict sorted JSON, allow_nan=false, single trailing newline
atomic exclusive write, tmp count0
exact order/count12
02/10 whole-tree manifest exact equal
11 references 01..10 by path/bytes/SHA-256, no self hash
12 references 01..11, no self hash
mismatch arrays = []
real side effects = 0
```

失败时不得补写same root；只在EXECUTION_RESULT记录owner failure。

## 12. Acceptance and stop

通过后可请求：

```text
REF-P7-23-C3 = ACCEPTED
REV-EQ-R6-FEATURE-001 = CLOSED
REV-EQ-R6-PHYSICAL-FAILURE-002 = CLOSED
```

但不得推断future live retry authority。Planner验收C3后必须单独判断：

```text
new live package scientific eligibility
consumed Human EQ authorization是否需要重新确认
fresh root / prelaunch / dispatch bounds
```

向EXECUTION_RESULT追加commit、test counts、evidence paths/hashes、1650 immutability与decision request，然后stop。

## 13. 维护性判断

修复限定在现有production runner与其focused tests。Feature selection和physical ledger count各有一个private
single owner，消除silent dict overwrite、92/58 scope confusion和failure/result时序漂移；不修改policy、
analyzer、RAW collector、device owner或wrapper。六个failing-first tests、full suite和1650 immutable replay
覆盖本次两个根因，无需Advisor或架构重构。

## 14. Planner review — rejected for plan path mismatch

**Review 时间：** 2026-07-27 17:34 America/Edmonton

**Decision：**

```text
REF-P7-23-C3 = REJECTED_PLAN_FOCUSED_PATH_MISMATCH
REV-EQ-R6-C3-PATH-003 = OPEN
implementation candidate = PRESERVE_UNCOMMITTED
next branch = REF-P7-23-C3E1
```

本次拒绝只针对本PLAN §8把实际tracked test
`tests/test_p7_thermal_diagnostics.py`误写为不存在的
`tests/test_measure_p7_thermal_diagnostics.py`。Executer已经按字面合同运行focused suite并得到
`ModuleNotFoundError`，因此不能把C3报为accepted。该失败不否定两个allowlisted files中的当前实现，也不授权
revert、restart或重做已经完成的failing-first阶段。

Reviewed inputs：

```text
PLAN SHA-256 =
  60540f224db4356d03e4131b3f88618ea49ad528e98a9ce624bb1942436df9a5
EXECUTION_RESULT SHA-256 =
  fd19fefae4577c2a3c9641d46557a3c74e5a3b7b99f4d2a11b8023e277fdd211
FULL_PLAN_REFERENCE SHA-256 =
  4016d422934e153c9ccd545453a921fa54b175a0d6f7ca17d6008e4d1cfbd083
starting/current HEAD =
  0f36671a351d537f204e8bc20849ac83e7e57c2b
```

Accepted completed evidence：

```text
failing-first exact six =
  Ran 6; pass 1; failures 2; errors 3
post-fix exact six =
  6/6 pass
post-fix tests/test_p7_td_b_r6_contract.py =
  61/61 pass
old 1650 whole-tree manifest =
  38 entries; 33 files; 0 symlinks
  SHA-256 fc39fccfc9921600968add879c0f024100b2cd5e6d3d32de18cb962ae6dc393c
real side effects =
  0
```

The failing-first result is accepted as a completed, non-repeatable stage. It may be consumed by C3E1; because the source
is already modified and reverting user/Executer work is prohibited, C3E1 must not rerun failing-first against a
manufactured pre-fix state.

Frozen continuation state：

```text
source working-tree SHA-256 =
  e8d563f894ae0119c7e3970e940570a21fb213cb6d1e542471a55406edbee9a8
test working-tree SHA-256 =
  7bbb635eeefcbf17884f4636434bcfe029e54c1c6344d559c40c6fd6f3277468
allowlisted binary diff SHA-256 =
  c4903c3dfb4f5d6f3a9f36909f430bcbce1f6de580a63d557e3a7bfcb96cd5cd
staged changes =
  0
old planned evidence root =
  absent
commit =
  not created
```

未完成且转交C3E1：

```text
corrected focused suite
full unittest discovery
compileall / CodeGraph / diff checks
1650 immutable replay and after-manifest
one exact focused commit
one fresh non-circular evidence seal
```

Human EQ authorization仍由1650消耗完毕；future live/device authority仍为false。C3E1只是一项pure-offline
continuation，不扩大source/test scope、设备权限、网络权限、commit cap或evidence-owner cap。
