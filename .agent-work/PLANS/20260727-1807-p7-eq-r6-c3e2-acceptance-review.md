# REF-P7-23-C3E2 / Preserve accepted commit and seal corrected offline evidence

**计划状态：** `executable_pure_offline_postcommit_evidence_continuation`

**Planner 日期：** 2026-07-27

**Reference task ID：** `REF-P7-23-C3E2`

**Parent reference task：** `REF-P7-23`

**PLAN contract ID：** `P7-TD-B-EQ-R6-C3E2-VALID-COMMIT-AUDIT-EVIDENCE-SEAL`

**Package kind：** `bounded_pure_offline_read_only_postcommit_audit_and_one_shot_evidence`

**Expected starting HEAD：** `f37517af3ae25efb41f085904fd48f037980ed04`

`PLAN_MACHINE_CONTRACT={"schema":"planner_execution_contract_v1","contract_id":"P7-TD-B-EQ-R6-C3E2-VALID-COMMIT-AUDIT-EVIDENCE-SEAL","reference_task_id":"REF-P7-23-C3E2","parent_reference_task_id":"REF-P7-23","package_kind":"bounded_pure_offline_read_only_postcommit_audit_and_one_shot_evidence","expected_starting_head":"f37517af3ae25efb41f085904fd48f037980ed04","single_current_action":"preserve_the_accepted_commit_run_one_valid_exact_scope_audit_and_seal_the_recorded_c3_evidence_once","source_edits":0,"test_edits":0,"tests_rerun":0,"replay_rerun":0,"codegraph_rerun":0,"compileall_rerun":0,"git_diff_check_rerun":0,"commit_authorized":false,"commit_cap":0,"amend":0,"device_access":0,"network_access":0,"dns_access":0,"env_access":0,"camera_access":0,"ray_access":0,"strip_access":0,"cleanup_access":0,"capture_access":0,"eq_access":0,"public_analyzer_access":0,"old_1650_mutation":0,"evidence_owner_invocation_cap":1,"evidence_root_acquisition_cap":1,"retry":0,"second_evidence_generator":0,"alternative_root":0,"same_root_repair":0,"human_eq_authorization_consumed_by_1650":true,"future_live_authorized":false,"advisor_required":false,"planner_stop_required":true}`

**当前唯一动作：** 保留accepted commit `f37517a`，不编辑source/test、不重跑tests或replay、不创建commit；
执行一个冻结的有效commit-path审计，并在同一个one-shot owner内fresh读取1650 before/after manifest、消费
C3/C3E1 recorded evidence、生成exact 12 JSON seal。

**唯一 Planner 停止点：** 任一frozen-input、commit identity/scope、1650 immutability、artifact结构或seal门失败
立即stop并handoff；不得amend、第二commit、repair same root、另建root或第二次调用owner。全部通过也必须停回
Planner；不得访问设备、运行tests/EQ/public analyzer或进入future live stage。

## 1. C3E1 review and C3E2 decision

```text
REF-P7-23-C3E1 = REJECTED_PLAN_POSTCOMMIT_COMMAND_SYNTAX
REV-EQ-R6-C3-PATH-003 = CLOSED
REV-EQ-R6-C3E1-GIT-CMD-004 = OPEN
REF-P7-23-C3E2 = EXECUTABLE
implementation and commit = PRESERVE
recorded validation = CONSUMABLE
```

C3E1 review archive：

```text
.agent-work/PLANS/20260727-1756-p7-eq-r6-c3e1-postcommit-command-review.md
SHA-256 ca2d9575cd3578484bba39bfc4c1a12c2982dd52d8bd17ea7b192c227b81cff9
```

Active debug：

```text
.agent-work/debug/active/20260727-p7-eq-r6-feature-selection-and-failure-accounting.md
SHA-256 84f3cadc07ffd73f994db1b2d034a5aa3c994bb35a2bd614616345036d106cc4
```

Invalid C3E1 command：

```text
git show --name-only --format=HEAD
exit = 128
fatal: invalid --pretty format: HEAD
```

Valid C3E2 command：

```text
git diff-tree --no-commit-id --name-only -r \
  f37517af3ae25efb41f085904fd48f037980ed04 --
```

Exact expected stdout，按行有序：

```text
src/camera_based_rgbww_optimizer/optimization/measure_p7_thermal_diagnostics.py
tests/test_p7_td_b_r6_contract.py
```

Expected stdout SHA-256（两行均以LF结尾）：

```text
e6997c871942e11a2031af8adf3153adab3ae77b8a6902cfc8f7b5706d411f4e
```

本包只修正Planner命令，不改变implementation或scientific contract，不恢复future live authority，也不需要
Advisor或Human authorization。

## 2. Frozen dispatch and repository state

Orchestrator dispatch必须提供exact：

```text
C3E2_PLAN_SHA256
C3E2_FULL_SHA256
C3E2_EXECUTION_RESULT_START_SHA256
```

Expected：

```text
HEAD / accepted commit =
  f37517af3ae25efb41f085904fd48f037980ed04
parent =
  0f36671a351d537f204e8bc20849ac83e7e57c2b
commit tree =
  a729ce65d0eb2cfc0f37cdc1d547e98f1ebcaaa4
FULL_PLAN_REFERENCE SHA-256 at planning =
  bd6e0499c1231ab775af1bd5ba557bee388c5cd09067a70b405be221ed41e2bc
EXECUTION_RESULT SHA-256 at planning =
  cdcb6f1c3232439a6345721c4691a0727c5c2677b6c94b399c597aa1e960580d
staged changes =
  0
```

PLAN不能自嵌自身hash。Dispatch的PLAN/FULL/EXECUTION_RESULT hash任一不符，或HEAD、parent、tree、staged
state不符，必须stop；不得checkout、reset、revert、amend、恢复或重建。

Frozen commit files：

```text
src/camera_based_rgbww_optimizer/optimization/measure_p7_thermal_diagnostics.py
  Git blob 839dfdd88f22970a2c77b88564ae016af3e76012
  SHA-256 a9bc77340dc43a30c0733e6ed651ea155b2250739b02a69d5abe6b6d249a3d47
tests/test_p7_td_b_r6_contract.py
  Git blob 86fcdb0663655e7a1a9a42955b1563f37b9a79f8
  SHA-256 030497bddc6735a6912abb08fe40e12bd3c0b4f37d47ef9954a61a5b88a39ad4
```

两文件相对HEAD必须无working-tree diff。允许其它Human/Planner-owned `.agent-work/**`与`advisor/**`
working-tree state存在，但不得修改、stage、commit或删除。任何production/test diff、任何staged change或第二
commit必须stop。

## 3. Absolute no-edit and no-rerun boundary

```text
source edits = 0
test edits = 0
PLAN / FULL / archive / debug edits = 0
commit / amend / cherry-pick / merge / rebase = 0
tests rerun = 0
failing-first rerun = 0
helper replay rerun = 0
fake accounting rerun = 0
compileall rerun = 0
CodeGraph sync/query rerun = 0
git diff --check rerun = 0
public analyzer = 0
```

C3/C3E1完成的所有validation均按§4消费。C3E2不得为了“加强证据”重复它们。唯一新的Git scope command是
§5冻结的valid `git diff-tree`，执行cap=1。

## 4. Recorded evidence accepted for consumption

来源：

```text
C3 review archive =
  .agent-work/PLANS/20260727-1734-p7-eq-r6-c3-path-mismatch-review.md
  SHA-256 727a95a92edbfa951f7da9042d5bd8fd18a7699dd3e53e67fd6aa42bed83b992
C3E1 review archive =
  .agent-work/PLANS/20260727-1756-p7-eq-r6-c3e1-postcommit-command-review.md
  SHA-256 ca2d9575cd3578484bba39bfc4c1a12c2982dd52d8bd17ea7b192c227b81cff9
EXECUTION_RESULT §148 and §149 current SHA-256 =
  cdcb6f1c3232439a6345721c4691a0727c5c2677b6c94b399c597aa1e960580d
```

Accepted recorded results：

```text
pre-fix exact six = pass 1 / failures 2 / errors 3; rerun false
post-fix exact six = 6/6
R6 contract = 61/61
focused four files = 182/182
full discovery = 634/634
failures / errors / skips = 0
compileall = pass
CodeGraph sync / blast radius = pass
private owner callers = 1 / 1
parallel owner / caller drift = 0 / 0
git diff --check = pass
postcommit exact six = 6/6
postcommit git diff --check = pass
1650 source/selected/missing/extras = 92/58/0/34
selected order and values exact = true
old ledger/failure/result/seal = 1/0/1/1
fresh post-return matrix = 1/1/1/1
fresh pre-return matrix = 0/0/0/0
```

Evidence artifacts必须标记上述项目为`recorded_evidence_consumed=true`，列出来源archive/section/hash，并对
每项标记`rerun_in_c3e2=false`。不得将它们描述为C3E2 fresh test/replay结果。

## 5. Single valid postcommit audit

在one-shot evidence owner内部执行exact一次：

```text
git diff-tree --no-commit-id --name-only -r \
  f37517af3ae25efb41f085904fd48f037980ed04 --
```

必须满足：

```text
exit = 0
stderr = empty
stdout exact two ordered lines
stdout SHA-256 =
  e6997c871942e11a2031af8adf3153adab3ae77b8a6902cfc8f7b5706d411f4e
path set = exact frozen two paths
command invocations = 1
```

同一owner还必须只读验证：

```text
HEAD = frozen commit
HEAD^ = frozen parent
HEAD^{tree} = frozen tree
subject/body = §6 exact
two blobs and file SHA-256 = §2 exact
two files clean relative to HEAD
staged changes = 0
```

不得运行invalid C3E1 command，也不得使用替代第三条path-enumeration command。任何mismatch立即使owner
hard-fail；不得修改Git状态。

## 6. Frozen commit metadata

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
commit count in C3/C3E1/C3E2 family = 1
```

`commit_authorized=false`、`commit_cap=0`。No amend、second commit、tag、push或PR。

## 7. Zero-side-effect boundary

整个package必须保持：

```text
network / DNS / hostname / .env read = 0
real backend / device / camera / Ray / strip = 0
real all_off / cleanup / final-zero = 0
capture / CR3 creation / NPY / TIFF = 0
Terminal / outer / wrapper / EQ / retry = 0
public analyzer / release / formal / strip stage / TD-C = 0
firmware / deployment = 0
old 1650 writes = 0
```

只允许本地只读Git/filesystem审计与唯一evidence root写入。

## 8. Fresh 1650 immutable manifest

Frozen family：

```text
/Volumes/4T/temp/rgbww-optimizer/p7-td-b-exposure-qual-r6-0f36671-20260727T1650
```

在同一个one-shot owner内：

1. evidence root acquisition前计算fresh before path/type/mode/bytes/SHA-256 whole-tree manifest；
2. 执行§5只读commit audit；
3. 不运行helper replay或public analyzer；
4. 计算fresh after whole-tree manifest；
5. before/after必须byte-exact相等，并与历史canonical summary一致：

```text
entries = 38
files = 33
symlinks = 0
canonical SHA-256 =
  fc39fccfc9921600968add879c0f024100b2cd5e6d3d32de18cb962ae6dc393c
```

不得写old family、修复旧artifact或以atime作为acceptance input。

## 9. One-shot evidence owner

```text
SAFE_PARENT =
  /Volumes/4T/temp/rgbww-optimizer
C3E1 OLD ROOT =
  /Volumes/4T/temp/rgbww-optimizer/p7-td-b-eq-r6-c3e1-offline-0f36671-20260727T1734
  expected absent
NEW ROOT =
  /Volumes/4T/temp/rgbww-optimizer/p7-td-b-eq-r6-c3e2-offline-f37517a-20260727T1756
  expected absent and non-symlink
```

Preflight通过后只调用一个owner一次；owner负责§5、§8和全部artifact：

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

Semantics：

```text
01 = dispatch, repository, commit, roots and zero-boundary facts
02 / 10 = C3E2 fresh immutable manifests
03 = C3 recorded failing-first; consumed, rerun false
04 = C3E1 implementation/commit plus C3E2 valid commit audit
05 = recorded exact-six and R6 results; rerun false
06 = recorded focused/full/postcommit results; rerun false
07 = recorded 1650 helper replay; rerun false
08 = recorded fake accounting and old 1650 accounting; rerun false
09 = recorded compileall/CodeGraph/diff plus C3E2 no-rerun counters
11 = references 01..10
12 = references 01..11 and terminal counters
```

Required：

```text
root mode 0700; files mode 0600
regular non-symlink, contained under SAFE_PARENT
strict sorted JSON, allow_nan=false, single trailing newline
atomic exclusive write; tmp count 0
exact order/count 12
02/10 whole-tree manifest exact equal
11 references 01..10 by path/bytes/SHA-256; no self hash
12 references 01..11 by path/bytes/SHA-256; no self hash
all mismatch arrays = []
recorded/fresh provenance explicit
real side effects = 0
```

失败时不得补写same root、删除root、创建alternate root或调用第二generator；只在EXECUTION_RESULT记录owner
failure。

## 10. Acceptance and handoff

向`.agent-work/EXECUTION_RESULT.md` append：

```text
dispatch hashes and frozen repository/commit checks
valid diff-tree exact command, invocation count, exit/stdout/stderr/hash
explicit source/test edits 0, tests/replay/static reruns 0, commits 0
recorded evidence sources and rerun=false
fresh 1650 before/after manifest equality
evidence root and exact 12 files
validation/terminal SHA-256 and mismatch arrays
owner/root/retry/repair counts
all zero-side-effect counters
decision request
```

全部通过后可请求：

```text
REF-P7-23-C3E2 = ACCEPTED
REV-EQ-R6-C3E1-GIT-CMD-004 = CLOSED
REV-EQ-R6-FEATURE-001 = CLOSED
REV-EQ-R6-PHYSICAL-FAILURE-002 = CLOSED
```

然后stop回Planner。不得推断新的live EQ、device、retry或Human authority。Planner验收C3E2后仍须单独判断
future live scientific eligibility和新的Human授权边界。

## 11. 维护性判断

C3E2不修改production/test，也不新增owner；它只以一个有效Git命令替换PLAN的无效只读门，并将已完成验证
以明确recorded provenance封装为one-shot evidence。复杂度局限于证据索引，不需要Advisor或架构重构。

## 12. Planner formal review — accepted

**Review 时间：** 2026-07-27 18:07 America/Edmonton

**Decision：**

```text
REF-P7-23-C3E2 = ACCEPTED
REF-P7-23-C3 implementation = ACCEPTED
REV-EQ-R6-C3-PATH-003 = CLOSED
REV-EQ-R6-C3E1-GIT-CMD-004 = CLOSED
REV-EQ-R6-FEATURE-001 = CLOSED
REV-EQ-R6-PHYSICAL-FAILURE-002 = CLOSED
commit f37517a = ACCEPTED
future live authorization = NOT PRESENT
next branch = HUMAN_EQ_R6_REAUTHORIZATION_CHECKPOINT
```

Reviewed inputs：

```text
PLAN SHA-256 =
  11f610712ced9aeba7918117cb87de0aae202eb6a47b504012f3aeb0d7338cd0
EXECUTION_RESULT SHA-256 =
  4b625a1cb410f78b54cc14e045fb1956a5c51859223b5e95c207b091bf46ee09
FULL_PLAN_REFERENCE SHA-256 =
  fdb8b6ac21248067b463fe627a10dae005eea37ea70807eb4fd0db282b03f0ff
HEAD =
  f37517af3ae25efb41f085904fd48f037980ed04
```

Accepted commit：

```text
commit =
  f37517af3ae25efb41f085904fd48f037980ed04
parent =
  0f36671a351d537f204e8bc20849ac83e7e57c2b
tree =
  a729ce65d0eb2cfc0f37cdc1d547e98f1ebcaaa4
paths =
  src/camera_based_rgbww_optimizer/optimization/measure_p7_thermal_diagnostics.py
  tests/test_p7_td_b_r6_contract.py
```

Accepted validation：

```text
recorded failing-first = pass 1 / failures 2 / errors 3
post-fix exact six = 6/6
R6 contract = 61/61
focused = 182/182
full discovery = 634/634
postcommit exact six = 6/6
compileall / CodeGraph / git diff check = pass
1650 replay = source 92 / selected 58 / missing 0 / extras 34 / exact order
old accounting = ledger/failure/result/seal 1/0/1/1
new post-return accounting = 1/1/1/1
new pre-return accounting = 0/0/0/0
```

Planner independent exact-12 audit：

```text
root =
  /Volumes/4T/temp/rgbww-optimizer/p7-td-b-eq-r6-c3e2-offline-f37517a-20260727T1756
root mode = 0700
files = exact 12; all regular non-symlink; mode 0600
strict JSON / canonical sorted serialization / trailing newline = pass
validation references 01..10 = exact bytes/SHA-256
terminal references 01..11 = exact bytes/SHA-256
self references = 0
validation SHA-256 =
  3b136148a2571dba893447c0558d9663d08a44ceef59000bd19a1fb22c48dc3c
terminal SHA-256 =
  c50e40e2b28fb0a69aa80e0016b39c06ff79f2818440c9b890417405d1ad309a
all mismatch arrays = []
```

Fresh commit audit exact：

```text
command invocations = 1
exit = 0
stderr = empty
paths = exact two
stdout SHA-256 =
  e6997c871942e11a2031af8adf3153adab3ae77b8a6902cfc8f7b5706d411f4e
```

1650 immutable：

```text
entries = 38
files = 33
symlinks = 0
before/after = exact equal
canonical SHA-256 =
  fc39fccfc9921600968add879c0f024100b2cd5e6d3d32de18cb962ae6dc393c
old writes = 0
```

Lifecycle与side effects：

```text
owner/root = 1/1
retry / repair / second generator / alternate root = 0
source/test edits = 0
tests/replay/static reruns = 0
commit/amend = 0
network / DNS / .env / device / camera / Ray / strip = 0
cleanup / capture / EQ / analyzer / release / formal / firmware / deployment = 0
```

### Authorization adjudication

AGENTS的light-control exception意味着：一旦active PLAN合法选择了bounded light operation，Ray/strip开关和
bounded light output本身不要求另行逐次授权。但它不允许从旧release、旧authorization或已失败实验推断一个
新的实验。C3、C3E1、C3E2及其前序PLAN均明确冻结：

```text
Human EQ authorization consumed by 1650 = true
future live authorized = false
```

因此Planner不能仅凭light-control exception自行把下一次fresh EQ-R6 retry写成executable package。下一步必须
先取得Human对“一个新的、fresh、bounded EQ-R6 attempt”的明确授权；这不是Advisor科学决策，且不涉及firmware、
deployment或范围扩展。

Human checkpoint应只请求：

```text
one fresh bounded EQ-R6 attempt
primary shutter = 1/2500
clipping-only fallback shutter = 1/3200
logical candidate cap = 8
retry = 0
dwell = A@600s + C@600s
same frozen EQ-R6 scientific policy and cleanup/final-zero contract
```

在Human明确授权前，device/network/camera/Ray/strip/capture/EQ均保持locked，Executer不得dispatch。Human授权
后，Planner仍须另写一个完整live executable PLAN；本checkpoint本身不执行实验。

No Advisor escalation：C3已修复并验证Advisor既定scientific branch中的runtime contract，没有出现新的
scientific ambiguity。
