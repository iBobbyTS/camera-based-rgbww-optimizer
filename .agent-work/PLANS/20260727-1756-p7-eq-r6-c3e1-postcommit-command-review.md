# REF-P7-23-C3E1 / Preserve C3 implementation and finish corrected offline gates

**计划状态：** `executable_pure_offline_continuation`

**Planner 日期：** 2026-07-27

**Reference task ID：** `REF-P7-23-C3E1`

**Parent reference task：** `REF-P7-23`

**PLAN contract ID：** `P7-TD-B-EQ-R6-C3E1-CORRECTED-FOCUSED-PATH-CONTINUATION`

**Package kind：** `bounded_pure_offline_existing_worktree_test_commit_evidence_continuation`

**Expected starting HEAD：** `0f36671a351d537f204e8bc20849ac83e7e57c2b`

`PLAN_MACHINE_CONTRACT={"schema":"planner_execution_contract_v1","contract_id":"P7-TD-B-EQ-R6-C3E1-CORRECTED-FOCUSED-PATH-CONTINUATION","reference_task_id":"REF-P7-23-C3E1","parent_reference_task_id":"REF-P7-23","package_kind":"bounded_pure_offline_existing_worktree_test_commit_evidence_continuation","expected_starting_head":"0f36671a351d537f204e8bc20849ac83e7e57c2b","single_current_action":"preserve_the_existing_c3_allowlisted_worktree_then_run_the_corrected_remaining_gates_commit_once_and_seal_once","source_allowlist":["src/camera_based_rgbww_optimizer/optimization/measure_p7_thermal_diagnostics.py"],"test_allowlist":["tests/test_p7_td_b_r6_contract.py"],"preserve_existing_uncommitted_implementation":true,"failing_first_recorded_evidence_consumable":true,"failing_first_rerun_authorized":false,"commit_authorized":true,"commit_cap":1,"device_access":0,"network_access":0,"dns_access":0,"env_access":0,"camera_access":0,"ray_access":0,"strip_access":0,"cleanup_access":0,"capture_access":0,"eq_access":0,"public_analyzer_access":0,"old_1650_mutation":0,"evidence_owner_invocation_cap":1,"evidence_root_acquisition_cap":1,"retry":0,"second_evidence_generator":0,"alternative_root":0,"same_root_repair":0,"human_eq_authorization_consumed_by_1650":true,"future_live_authorized":false,"advisor_required":false,"planner_stop_required":true}`

**当前唯一动作：** 保留C3已经形成的两个allowlisted file未提交实现，不revert、不restart、不制造pre-fix
source；使用正确的tracked focused test path完成剩余offline gates、1650 read-only replay、一个exact focused
commit和一个fresh 12-artifact evidence seal。

**唯一 Planner 停止点：** 任一frozen-input、scope、test、replay、immutability、static、commit或seal门失败，
立即stop并handoff。不得在失败evidence root上repair，不得另建root或第二次调用owner。全部通过也必须停回
Planner；不得访问设备、重跑EQ、运行public analyzer或进入future live stage。

## 1. C3 review and continuation decision

```text
REF-P7-23-C3 = REJECTED_PLAN_FOCUSED_PATH_MISMATCH
REV-EQ-R6-C3-PATH-003 = OPEN
REF-P7-23-C3E1 = EXECUTABLE
implementation candidate = PRESERVE_UNCOMMITTED
failing-first = ACCEPTED_COMPLETED_EVIDENCE
```

C3 review archive：

```text
.agent-work/PLANS/20260727-1734-p7-eq-r6-c3-path-mismatch-review.md
SHA-256 727a95a92edbfa951f7da9042d5bd8fd18a7699dd3e53e67fd6aa42bed83b992
```

Active debug：

```text
.agent-work/debug/active/20260727-p7-eq-r6-feature-selection-and-failure-accounting.md
SHA-256 3ac344854e47054e22a0b2b57315cb346a9de77102b8d8bc3f836691a6708e53
```

本包只纠正C3 PLAN中不存在的focused test path：

```text
wrong and absent =
  tests/test_measure_p7_thermal_diagnostics.py
correct and tracked =
  tests/test_p7_thermal_diagnostics.py
```

这不是对implementation的重新设计，不恢复future live authority，也不需要Advisor或Human authorization。

## 2. Frozen dispatch inputs

Orchestrator dispatch必须提供exact：

```text
C3E1_PLAN_SHA256
C3E1_FULL_SHA256
C3E1_EXECUTION_RESULT_START_SHA256
```

Expected inputs：

```text
HEAD =
  0f36671a351d537f204e8bc20849ac83e7e57c2b
FULL_PLAN_REFERENCE SHA-256 at planning =
  4016d422934e153c9ccd545453a921fa54b175a0d6f7ca17d6008e4d1cfbd083
EXECUTION_RESULT SHA-256 at planning =
  fd19fefae4577c2a3c9641d46557a3c74e5a3b7b99f4d2a11b8023e277fdd211
source working-tree SHA-256 =
  e8d563f894ae0119c7e3970e940570a21fb213cb6d1e542471a55406edbee9a8
test working-tree SHA-256 =
  7bbb635eeefcbf17884f4636434bcfe029e54c1c6344d559c40c6fd6f3277468
allowlisted binary diff SHA-256 =
  c4903c3dfb4f5d6f3a9f36909f430bcbce1f6de580a63d557e3a7bfcb96cd5cd
staged changes =
  0
```

PLAN不能自嵌自身hash。Dispatch给出的PLAN/FULL/EXECUTION_RESULT hash任一不符，或HEAD、两个working-tree
file hash、allowlisted binary diff hash不符，必须stop；不得尝试恢复、重建或覆盖当前实现。

允许其它Human/Planner-owned `.agent-work/**` working-tree changes存在，但不得stage、commit、修改或删除。
若两个implementation allowlist之外存在新的production/test staged或unstaged diff，必须stop并报告。

## 3. Exact implementation scope

允许保留和必要时最小调整：

```text
src/camera_based_rgbww_optimizer/optimization/measure_p7_thermal_diagnostics.py
tests/test_p7_td_b_r6_contract.py
```

允许append-only：

```text
.agent-work/EXECUTION_RESULT.md
```

禁止修改、stage或commit：

```text
.agent-work/PLAN.md
.agent-work/FULL_PLAN_REFERENCE.md
.agent-work/debug/**
.agent-work/PLANS/**
advisor/**
docs/**
.agents/skills/**
config/**
tmp/**
firmware/**
all other src/** and tests/**
```

当前实现必须继续满足C3原始两个owner合同：

1. complete RAW observations建立strict unique ID map，只按frozen 58 policy IDs和其exact order选择；
2. missing/duplicate required ID fail closed，extra 34只忽略、不误报quality failure；
3. statistic owner保持`statistics.normalized_per_second.trimmed_mean`；
4. strict `physical-returns.jsonl` ledger recount是candidate failure/result的共同authoritative count；
5. post-return feature/sidecar failure均保留physical count，pre-return failure保持0；
6. 不增加parallel owner、fallback、schema repair、analyzer或execution framework。

如果剩余gate暴露当前实现的局部缺陷，可在exact two-file allowlist中作最小修正并重跑受影响gate；不得新增测试
method、改变frozen scientific semantics、扩大scope或另起纠偏方向。需要上述任何扩大时stop给Planner。

## 4. Recorded failing-first evidence is consumed, not rerun

C3已完成并由Planner接受：

```text
exact six pre-fix =
  Ran 6
  pass 1
  failures 2
  errors 3
positive selection / post-return accounting reproduced original symptoms
post-fix exact six =
  6/6 pass; no skips
post-fix R6 contract file =
  61/61 pass; no skips
```

Exact six methods：

```text
test_eq_r6_full_raw_observations_select_exact_policy_order
test_eq_r6_feature_selection_rejects_missing_required_id
test_eq_r6_feature_selection_rejects_duplicate_observation_id
test_eq_r6_post_return_feature_failure_counts_physical_atomically
test_eq_r6_sidecar_failure_counts_physical_in_failure_and_result
test_eq_r6_pre_return_failure_keeps_all_physical_counts_zero
```

`failing_first_rerun_authorized=false`。不得revert source、临时checkout旧source、patch制造pre-fix或复制旧代码来
重复failing-first。C3E1 evidence artifact 03必须引用C3 review archive、C3 EXECUTION_RESULT §148记录及其
dispatch hash，清楚标记`recorded_evidence_consumed=true`和`rerun=false`。

## 5. Zero-side-effect boundary

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

## 6. Corrected remaining test gates

先确认exact six名称仍exact存在且没有skip/xfail，再按以下顺序运行：

```text
1. exact six methods = 6/6
2. tests/test_p7_td_b_r6_contract.py = 61/61
3. focused files =
   tests/test_p7_td_b_r6_contract.py
   tests/test_hsi_objective.py
   tests/test_p7_thermal_diagnostics.py
   tests/test_analyze_p7_thermal_diagnostics.py
4. full unittest discover = 634/634
```

Focused suite必须无failure、error、skip或xfail。禁止引用或尝试创建
`tests/test_measure_p7_thermal_diagnostics.py`。

若full discovery因仓库已经存在的测试变化而不是本包改动不等于634，不得改PLAN期望或宣称通过；记录exact
count与来源后stop给Planner。不得把warning、skip或partial suite视为pass。

提交前还必须通过：

```text
python -m compileall \
  src/camera_based_rgbww_optimizer/optimization/measure_p7_thermal_diagnostics.py
CodeGraph sync
CodeGraph blast-radius inspection for both private owners
git diff --check
```

CodeGraph必须确认没有新增parallel owner或意外caller drift；若index同步失败或报告stale，stop并记录，不以grep
替代该门。

## 7. 1650 immutable read-only replay

Frozen family：

```text
/Volumes/4T/temp/rgbww-optimizer/p7-td-b-exposure-qual-r6-0f36671-20260727T1650
```

开始和结束都做path/type/mode/bytes/SHA-256 whole-tree manifest，必须exact相等。Planner已接受的历史manifest：

```text
entries = 38
files = 33
symlinks = 0
canonical SHA-256 =
  fc39fccfc9921600968add879c0f024100b2cd5e6d3d32de18cb962ae6dc393c
```

Replay只能调用当前private feature-selection helper与strict ledger helper，不得运行public analyzer或修改旧
artifacts。Acceptance：

```text
RAW source accepted observations = 92
selected policy observations = 58
missing = 0
extras = 34
selected order = exact frozen policy order
first selected = block_03::G1
selected values/metrics = source observation by-ID exact
old physical ledger strict count = 1
old candidate-failure remains physical 0
old candidate-result remains physical 1
old terminal seal remains physical 1
before tree = after tree exact
```

旧`0/1/1/1`证明历史缺陷且不得repair；fresh fake matrix必须证明新code的同类post-return failure为
`1/1/1/1`，pre-return为`0/0/0/0`。

## 8. Commit contract

仅在所有test、replay、immutability、compileall、CodeGraph与diff门通过后，允许一次focused commit：

```text
git add -- \
  src/camera_based_rgbww_optimizer/optimization/measure_p7_thermal_diagnostics.py \
  tests/test_p7_td_b_r6_contract.py

git commit \
  -m "fix(p7): select eq-r6 policy features atomically" \
  -m "Filter complete RAW observations to the frozen policy order and keep candidate failure physical-return counts aligned with the authoritative ledger."
```

Commit cap=1。禁止`git add -A`、amend、第二commit、push或PR。Commit必须exact two paths；不得包含PLAN、
FULL、archive、debug、EXECUTION_RESULT或evidence。

提交后重新运行：

```text
exact six = 6/6
git diff --check
git show --name-only --format=HEAD
```

任何post-commit failure必须stop；不得amend或第二commit。

## 9. One-shot evidence owner

```text
SAFE_PARENT =
  /Volumes/4T/temp/rgbww-optimizer
NEW_ROOT =
  /Volumes/4T/temp/rgbww-optimizer/p7-td-b-eq-r6-c3e1-offline-0f36671-20260727T1734
```

开始必须absent/non-symlink。只有implementation/test/replay/static/commit/post-commit全部通过后，才调用一个
one-shot owner一次：

```text
owner invocations = 1
root acquisitions = 1
retry / second generator / alternate root / same-root repair = 0
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

Artifact 03必须消费C3 recorded failing-first，不得声称C3E1 fresh reproduction。其它required：

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

失败时不得补写same root、删除root、创建alternate root或调用第二generator；只在EXECUTION_RESULT记录owner
failure。

## 10. Acceptance and handoff

向`.agent-work/EXECUTION_RESULT.md` append：

```text
dispatch hashes and frozen-state checks
whether existing implementation was preserved
recorded failing-first source and rerun=false
exact/contract/focused/full counts
corrected focused path
compileall / CodeGraph / diff results
1650 before/after manifest and replay values
commit id and exact paths
evidence root, exact 12 files, terminal and validation SHA-256
owner/root/retry counts
all zero-side-effect counters
decision request
```

全部通过后可请求：

```text
REF-P7-23-C3E1 = ACCEPTED
REV-EQ-R6-C3-PATH-003 = CLOSED
REV-EQ-R6-FEATURE-001 = CLOSED
REV-EQ-R6-PHYSICAL-FAILURE-002 = CLOSED
```

然后stop回Planner。不得推断新的live EQ、device、retry或Human authority。Planner验收C3E1后仍须单独判断
future live scientific eligibility和新的Human授权边界。

## 11. 维护性判断

本continuation不新增模块或owner，只保留现有两个private owners及其focused tests，并纠正Planner写错的
test path。风险被限制在EQ-R6 feature selection和physical failure accounting两个既有语义边界；exact、
focused、full、immutable replay与CodeGraph门覆盖剩余风险，不需要Advisor或架构重构。

## 12. Planner review — rejected for invalid postcommit Git command

**Review 时间：** 2026-07-27 17:56 America/Edmonton

**Decision：**

```text
REF-P7-23-C3E1 = REJECTED_PLAN_POSTCOMMIT_COMMAND_SYNTAX
REV-EQ-R6-C3-PATH-003 = CLOSED
REV-EQ-R6-C3E1-GIT-CMD-004 = OPEN
implementation and commit = PRESERVE
next branch = REF-P7-23-C3E2
```

本次拒绝只针对本PLAN §8的字面命令：

```text
git show --name-only --format=HEAD
```

当前Git把`HEAD`解释为pretty-format名称并返回`fatal: invalid --pretty format: HEAD`、exit 128。Executer按
PLAN停止是正确行为。独立只读`git diff-tree --no-commit-id --name-only -r HEAD`已确认commit exact two
paths，因此该命令缺陷不否定implementation、tests、replay、CodeGraph或commit。

Reviewed inputs：

```text
PLAN SHA-256 =
  255e229cd6c762f6e07db603836dd4c126a6ca7bf67690d1135d206f09a6610c
EXECUTION_RESULT SHA-256 =
  cdcb6f1c3232439a6345721c4691a0727c5c2677b6c94b399c597aa1e960580d
FULL_PLAN_REFERENCE SHA-256 =
  bd6e0499c1231ab775af1bd5ba557bee388c5cd09067a70b405be221ed41e2bc
starting HEAD =
  0f36671a351d537f204e8bc20849ac83e7e57c2b
current HEAD / accepted commit =
  f37517af3ae25efb41f085904fd48f037980ed04
```

Accepted completed evidence：

```text
recorded pre-fix failing-first = pass 1 / failures 2 / errors 3
post-fix exact six = 6/6
R6 contract file = 61/61
focused four files = 182/182
full discovery = 634/634
failures / errors / skips = 0
compileall / CodeGraph sync and blast-radius / git diff --check = pass
1650 manifest before/after =
  38 entries / 33 files / 0 symlinks
  canonical SHA-256 fc39fccfc9921600968add879c0f024100b2cd5e6d3d32de18cb962ae6dc393c
1650 helper-only replay =
  source 92 / selected 58 / missing 0 / extras 34 / exact order true
  old ledger/failure/result/seal 1/0/1/1
fresh fake accounting =
  post-return 1/1/1/1; pre-return 0/0/0/0
postcommit exact six = 6/6
postcommit git diff --check = pass
```

Accepted commit：

```text
commit =
  f37517af3ae25efb41f085904fd48f037980ed04
parent =
  0f36671a351d537f204e8bc20849ac83e7e57c2b
subject =
  fix(p7): select eq-r6 policy features atomically
body =
  Filter complete RAW observations to the frozen policy order and keep candidate failure physical-return counts aligned with the authoritative ledger.
paths =
  src/camera_based_rgbww_optimizer/optimization/measure_p7_thermal_diagnostics.py
  tests/test_p7_td_b_r6_contract.py
commit count = 1
amend / second commit = 0
```

未完成且转交C3E2：

```text
one valid exact commit-path audit
fresh 1650 before/after whole-tree manifest equality
one fresh non-circular 12-artifact evidence seal
```

C3E2不得修改source/test、重跑tests/replay/CodeGraph/compileall、amend或创建commit。它消费上述C3/C3E1
recorded evidence，只执行必要的只读postcommit audit与immutable manifest。C3E1 evidence owner/root/artifacts
均为0，旧planned root absent；network、device、capture、EQ、public analyzer及其它real side effects均为0。

Human EQ authorization仍由1650消耗完毕；future live/device authority仍为false。C3E2是pure-offline evidence
continuation，不需要Advisor或Human authorization。
