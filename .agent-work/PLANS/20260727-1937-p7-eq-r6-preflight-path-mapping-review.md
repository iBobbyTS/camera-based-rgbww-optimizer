# REF-P7-23 / Fresh bounded EQ-R6 live activation after accepted C3/C3E2

**计划状态：** `executable_bounded_live_activation`

**Planner 日期：** 2026-07-27

**Reference task ID：** `REF-P7-23`

**PLAN contract ID：** `P7-TD-B-RAY-C-EXPOSURE-QUAL-R6-FRESH-LIVE-AFTER-C3E2`

**Package kind：** `bounded_live_prelaunch_and_conditional_visible_terminal_dispatch`

**Expected HEAD：** `f37517af3ae25efb41f085904fd48f037980ed04`

`PLAN_MACHINE_CONTRACT={"schema":"planner_execution_contract_v1","contract_id":"P7-TD-B-RAY-C-EXPOSURE-QUAL-R6-FRESH-LIVE-AFTER-C3E2","reference_task_id":"REF-P7-23","package_kind":"bounded_live_prelaunch_and_conditional_visible_terminal_dispatch","expected_head":"f37517af3ae25efb41f085904fd48f037980ed04","single_current_action":"run_one_fresh_production_prelaunch_validate_only_its_handoff_and_dispatch_one_visible_terminal_eq_r6_outer","orchestrator_authorization_adjudication":"human_reauthorization_not_required_under_current_agents_high_risk_boundary","human_authorization_required":false,"human_authorization_reask_required":false,"prior_human_eq_confirmation_present":true,"static_preflight_cap":1,"production_prelaunch_invocation_cap":1,"prelaunch_root_acquisition_cap":1,"handoff_validation_cap":1,"outer_dispatch_cap":1,"candidate_1_cap":1,"candidate_2_cap":1,"candidate_1_shutter":"1/2500","candidate_2_shutter":"1/3200","candidate_2_unlock":"candidate_1_clipping_only_and_candidate_terminal_cleanup_final_zero_pass","per_candidate_dwell":"A@600s+C@60/120/300/600s","real_capture_cap":8,"formal_measurement_count":0,"ambient_measurement_count":0,"retry":0,"relaunch":0,"alternative_root":0,"same_root_repair":0,"source_edits_authorized":false,"test_edits_authorized":false,"docs_edits_authorized":false,"skill_edits_authorized":false,"wrapper_edits_authorized":false,"config_edits_authorized":false,"commit_authorized":false,"camera_access":"bounded_readiness_and_eq_candidate_capture","ray_access":"bounded_readiness_candidate_light_and_cleanup","strip_access":"generation_bearing_zero_state_only","public_analyzer_authorized":false,"formal_r6_authorized":false,"release_authorized":false,"strip_stage_authorized":false,"td_c_authorized":false,"planner_stop_required":true}`

**当前唯一动作：** 在全新FAMILY中完成一个single cohesive activation transaction：

```text
one static preflight
-> production prelaunch exactly once
-> validate that exact fresh handoff within 600 seconds
-> one visible macOS Terminal outer dispatch
-> three sparse read-only liveness checks
-> terminal read-only audit or Orchestrator automation handoff
```

**唯一 Planner 停止点：** static preflight、production prelaunch、handoff validation、Terminal dispatch、
candidate lifecycle、quality、physical evidence、cleanup、final-zero或terminal seal任一步失败立即stop并回Planner；
outer在L1/L2/L3前terminal则完成最终只读审计并stop；L3后仍存活则记录三次存活证据并交Orchestrator创建
automation后stop。成功terminal也必须回Planner，不得运行public analyzer、successor release、full formal R6、
strip stage或TD-C。

## 1. Authorization adjudication and accepted predecessor

当前`AGENTS.md`只要求以下危险操作取得Human authorization：

```text
remote firmware upload / flash
remote deployment
destructive hardware changes
device operation outside active PLAN bounds
```

本包不包含上述操作。它只执行active PLAN内的bounded local-lab Ray/camera EQ-R6 acquisition、strip
generation-bearing zero verification及双cleanup；Ray/strip bounded light output和zero/off cleanup明确不要求
额外Human authorization。Human此前也已经明确确认进入同一冻结EQ-R6路线。C3/C3E2仅修复1650暴露的
runtime feature-selection与physical-return accounting defects，没有扩大实验目标、shutter、cap、dwell、
fallback条件或设备范围。

因此：

```text
REF-P7-23-H2 = SUPERSEDED_AUTHORIZATION_MISCLASSIFICATION
new Human authorization required = false
Executer may consume this PLAN without asking Human again
Advisor decision required = false
```

H2 override archive：

```text
.agent-work/PLANS/20260727-1928-p7-eq-r6-h2-authorization-override-review.md
SHA-256 d18432fb86bdf0ad0de3ef29a103ee3c5b7ddb2d254b038fe3eed9579e7c66c6
```

Accepted C3/C3E2：

```text
REF-P7-23-C3E2 = ACCEPTED
REV-EQ-R6-C3-PATH-003 = CLOSED
REV-EQ-R6-C3E1-GIT-CMD-004 = CLOSED
REV-EQ-R6-FEATURE-001 = CLOSED
REV-EQ-R6-PHYSICAL-FAILURE-002 = CLOSED
commit =
  f37517af3ae25efb41f085904fd48f037980ed04
```

Acceptance archive and evidence：

```text
.agent-work/PLANS/20260727-1807-p7-eq-r6-c3e2-acceptance-review.md
SHA-256 889db188fbcb575bfa6b72eba671d73f47e2bc22b630fb565439ef130d72c6e5
evidence root =
  /Volumes/4T/temp/rgbww-optimizer/p7-td-b-eq-r6-c3e2-offline-f37517a-20260727T1756
validation SHA-256 =
  3b136148a2571dba893447c0558d9663d08a44ceef59000bd19a1fb22c48dc3c
terminal SHA-256 =
  c50e40e2b28fb0a69aa80e0016b39c06ff79f2818440c9b890417405d1ad309a
all mismatches = []
```

The CLI field `--human-authorization P7-TD-B-RAY-C-EXPOSURE-QUAL-R6` remains part of the frozen runner/handoff
identity for compatibility and provenance. In this PLAN it records the already-confirmed bounded experiment identity;
it is not a new approval gate and must not cause an additional Human prompt.

## 2. Frozen repository and dispatch inputs

```text
REPO =
  /Users/ibobby/Projects/WLED-RGBWW
HEAD =
  f37517af3ae25efb41f085904fd48f037980ed04
HEAD parent =
  0f36671a351d537f204e8bc20849ac83e7e57c2b
HEAD subject =
  fix(p7): select eq-r6 policy features atomically
```

Frozen hashes：

```text
advisor/4/4.GUIDE.md
  659152f6c0ae69c90c701de4e57c352d771e4f0bf75cf9410271ba0a94200e35
.agents/skills/camera-based-rgbww-optimizer/SKILL.md
  c8dd57a23ad684b4f7001f342ed3413a1abf4349bc6aeb90dbee7f5158139607
src/camera_based_rgbww_optimizer/optimization/measure_p7_thermal_diagnostics.py
  a9bc77340dc43a30c0733e6ed651ea155b2250739b02a69d5abe6b6d249a3d47
src/camera_based_rgbww_optimizer/optimization/p7_thermal_diagnostics.py
  34758f854cd5b17f3f844d8f8312b31fdbda11965aa4f695a3b1421e19522dc3
tests/test_p7_td_b_r6_contract.py
  030497bddc6735a6912abb08fe40e12bd3c0b4f37d47ef9954a61a5b88a39ad4
config/hsi/p7-ray-td-b-exposure-policy-v2.json
  9e5ec953fdeedf0e73a26a3a476b7336febdbdb2c3e83819123c7b9ad4060ec2
tmp/run-p7-thermal-diagnostics.zsh
  2730d43507af14a531453978477439bb29ef93ae7dea8e0bddb6c2330e1242e5
```

Orchestrator dispatch必须提供exact dynamic handoff：

```text
LIVE_PLAN_SHA256
LIVE_FULL_SHA256
LIVE_EXECUTION_RESULT_START_SHA256
```

PLAN不能自嵌自身hash。任一dynamic hash缺失、格式错误或current path/hash不符即stop。当前FULL中的旧H2
blocked状态不授权也不否定本PLAN；Orchestrator必须在dispatch消息中明确确认其authorization override并在
Executer handoff后独立更新FULL。Executer不得修改FULL。

## 3. Fresh unique live root

```text
SAFE_PARENT =
  /Volumes/4T/temp/rgbww-optimizer
FAMILY =
  /Volumes/4T/temp/rgbww-optimizer/p7-td-b-exposure-qual-r6-f37517a-20260727T1928
PRELAUNCH =
  ${FAMILY}/prelaunch
RUN =
  ${FAMILY}/run
```

开始时FAMILY/PRELAUNCH/RUN必须absent且non-symlink。Production prelaunch是唯一FAMILY/PRELAUNCH
acquisition owner；outer是唯一RUN acquisition owner。不得预建、复用、删除、repair或改用alternative root。

以下旧family永久只读，不得作为fresh handoff input：

```text
/Volumes/4T/temp/rgbww-optimizer/p7-td-b-exposure-qual-r6-0f36671-20260727T1650
/Volumes/4T/temp/rgbww-optimizer/p7-td-b-eq-r6-c3e2-offline-f37517a-20260727T1756
```

## 4. One static preflight

只允许一次local read/hash/stat preflight：

```text
HEAD / parent / subject = §2 exact
PLAN/FULL/EXECUTION_RESULT start = Orchestrator dynamic hashes
§2 frozen source/config/wrapper hashes = exact
§1 archive/evidence hashes = exact
SAFE_PARENT = safe
new FAMILY/PRELAUNCH/RUN = absent and non-symlink
old 1650 and C3E2 evidence roots = present, read-only inputs only
repository .env = regular non-symlink if present
```

`.env`只可lstat；不得读取、打印、hash或复制。不得在static preflight做DNS、resolver、ping、HTTP、camera、
Ray、strip或cleanup probe。cap=1，失败即stop；不得修复、重试或换root。

## 5. Fresh production prelaunch exactly once

从repo root逐字运行一次：

```zsh
.venv/bin/python -m camera_based_rgbww_optimizer.optimization.measure_p7_thermal_diagnostics \
  --execute \
  --allow-device-control \
  --eq-r6-prelaunch \
  --experiment-id p7_td_b_command_switch_history_v1 \
  --source ray \
  --phase formal \
  --output-dir /Volumes/4T/temp/rgbww-optimizer/p7-td-b-exposure-qual-r6-f37517a-20260727T1928 \
  --run-name prelaunch \
  --code-checkpoint f37517af3ae25efb41f085904fd48f037980ed04 \
  --human-authorization P7-TD-B-RAY-C-EXPOSURE-QUAL-R6 \
  --camera-backend remote
```

Invocation/root-acquisition cap=`1/1`。不设置ESPHome host override，不消费旧handoff，不读取`.env`内容。
Prelaunch允许bounded camera/Ray readiness、strip zero与cleanup；不允许：

```text
capture / CR3 / NPY / TIFF = 0
nonzero strip output = 0
RUN / outer / candidate / dispatch = 0
formal / ambient measurement = 0 / 0
public analyzer / release / formal R6 / strip stage / TD-C = 0
```

PRELAUNCH exact 9：

```text
frozen-inputs.json
offline-plan.json
camera-readiness.json
ray-readiness.json
all-off-python.json
all-off-shell.json
independent-final-zero.json
prelaunch-terminal.json
prelaunch-manifest.json
```

若exit非零、artifact不全、terminal/manifest不通过或zero proof无generation，保留证据并立即stop；不得补probe、
额外cleanup、retry、第二prelaunch或same-root repair。

## 6. Exact handoff validation within 600 seconds

仅fresh prelaunch exit `0`后继续。必须在`prelaunch-terminal.json.sealed_at`后600秒内完成validation并dispatch；
超时立即stop，不能重跑prelaunch。

使用production `_eq_prelaunch_validate_root`做一次read-only validation，并独立确认：

```text
exact 9 names/order, strict JSON, modes 0700/0600, safe containment
terminal.status / manifest.status = pass / pass
manifest references = exact bytes and SHA-256
camera / Ray / Python cleanup / shell cleanup / final-zero = all pass
strip generation-bearing five-channel zero = true
Ray zero and validate_both_off = pass
capture / nonzero / dispatch counts = 0 / 0 / 0
RUN = absent and non-symlink
launch_handoff.ready_for_dispatch = true
launch_handoff.dispatch_count / outer_launch_count = 0 / 0
launch_handoff.run_root = §3 exact RUN
checkpoint / authorization label = §2 and §1 exact
outer_argv = §7 exact argv
outer_argv_sha256 =
  4f96b6d78c12ecdfbbf7cf6c40073c25bb20e4778efb981ad55172855b274589
secret material = absent
```

Hash定义：UTF-8 compact JSON array，`separators=(",",":")`、`ensure_ascii=False`、无newline。
Validation cap=`1`。任一不符立即stop；不得编辑argv、重建handoff、调用第二validator或用旧handoff替换。

## 7. Visible macOS Terminal exact single dispatch

Validated outer argv：

```text
/Users/ibobby/Projects/WLED-RGBWW/.venv/bin/python
-m
camera_based_rgbww_optimizer.optimization.measure_p7_thermal_diagnostics
--execute
--allow-device-control
--eq-r6-orchestrate
--experiment-id
p7_td_b_command_switch_history_v1
--source
ray
--phase
formal
--output-dir
/Volumes/4T/temp/rgbww-optimizer/p7-td-b-exposure-qual-r6-f37517a-20260727T1928
--run-name
run
--code-checkpoint
f37517af3ae25efb41f085904fd48f037980ed04
--human-authorization
P7-TD-B-RAY-C-EXPOSURE-QUAL-R6
--camera-backend
remote
```

在一个可见macOS Terminal tab运行exact：

```zsh
cd /Users/ibobby/Projects/WLED-RGBWW && exec /Users/ibobby/Projects/WLED-RGBWW/.venv/bin/python -m camera_based_rgbww_optimizer.optimization.measure_p7_thermal_diagnostics --execute --allow-device-control --eq-r6-orchestrate --experiment-id p7_td_b_command_switch_history_v1 --source ray --phase formal --output-dir /Volumes/4T/temp/rgbww-optimizer/p7-td-b-exposure-qual-r6-f37517a-20260727T1928 --run-name run --code-checkpoint f37517af3ae25efb41f085904fd48f037980ed04 --human-authorization P7-TD-B-RAY-C-EXPOSURE-QUAL-R6 --camera-backend remote
```

必须使用Terminal visible `do script`或等价前台tab，不得作为Codex-managed background process。
Dispatch cap=`1`；Terminal API不确定、异常或无PID也计`attempted=1`，不得重试。

记录：

```text
Terminal window/tab identifier
exact command and command SHA-256
dispatch attempted = 1
observed outer PID and exact argv if uniquely bound
RUN/live-plan first appearance
authorization basis = AGENTS bounded-operation exception plus Orchestrator adjudication
```

## 8. Frozen EQ-R6 scientific and budget contract

```text
experiment = P7-TD-B-RAY-C-EXPOSURE-QUAL-R6
runner experiment_id = p7_td_b_command_switch_history_v1
source / phase / variant = ray / formal / core
qualification formal-authorizing = false
strip = generation-bearing zero throughout
ambient / formal measurement count = 0 / 0
candidate 1 nominal shutter = 1/2500 s
candidate 2 nominal shutter = 1/3200 s
candidate count = 1, or 2 only under exact clipping-only unlock
physical CR3 cap = 4 per candidate, 8 total
retry / relaunch / alternative shutter = 0 / 0 / 0
public analyzer / successor release / formal R6 / strip / TD-C = 0
```

每个candidate exact sequence：

```text
verify strip generation-bearing five-channel zero
Ray A = H120/S100/INT100 for 600 s
A -> C = H300/S100/INT100
C capture at 60 s
C capture at 120 s
C capture at 300 s
C capture at 600 s
Ray off
Python finally all_off
shell trap all_off
independent generation-bearing final-zero
candidate terminal seal
```

资格测试不采A图、不计算TD-B history、不进入P6 compatibility。每张C capture使用formal同一measurement path，
并必须具有：

```text
58/58 frozen required features
clipped_fraction == 0.0 for every required feature
finite / near-noise / valid-pixel gates pass
MakerNote recorded exposure and nominal/recorded ratio gate pass
Ray command/readback and source isolation pass
strip generation/readback zero pass
CR3/sidecar path, bytes, SHA-256 and remote IDs complete
attempt / logical / physical-return / accepted accounting truthful
```

Candidate 1 branch：

```text
4/4 accepted
  -> qualified_1_2500; candidate 2 launch = 0

one or more capture failures, all and only required_feature_clipping,
and candidate-1 Python cleanup, shell cleanup, independent final-zero,
physical preservation and terminal seal all pass
  -> candidate 2 may launch once

low-signal / nonfinite / valid-pixel / metadata / source isolation /
readback / ownership / evidence / cleanup / final-zero / seal / runtime failure
  -> hard stop; candidate 2 launch = 0
```

Candidate 2 branch：

```text
4/4 accepted
  -> qualified_1_3200
any required failure
  -> exposure_window_unresolved or run_invalid, preserving owner classification
```

不允许`1/4000`、`1/5000`、auto exposure、weak reacquire、same-root continuation、third candidate或自动搜索。
Candidate 1 clipping后只有其terminal lifecycle完整通过才可进入candidate 2。

## 9. Progressive evidence, preservation and terminal lifecycle

Outer与每个candidate必须逐阶段atomic exclusive-write evidence，至少覆盖：

```text
frozen inputs / live plan / launch ledger
candidate dispatch and exact PID/argv/parent binding
Ray and strip command/readback chronology
capture attempted and remote request/capture IDs
physical-returns ledger
CR3 and sidecar path/type/mode/bytes/SHA-256
RAW patch statistics and 58-feature quality decision
candidate result/failure and candidate terminal seal
Python cleanup / shell cleanup / independent final-zero
outer result/failure and outer terminal seal
```

Physical-return后任何sidecar read、feature、policy、classification或later-stage failure都必须保留并记账已返回
CR3/sidecar；不得因failure payload生成阶段丢失remote IDs或把authoritative physical count重置为零。失败证据必须
progressively persisted；terminal summary不得代替逐阶段事实。

任何runtime、quality、ownership、source isolation、readback、path containment、symlink、hash、accounting、
cleanup、final-zero或seal异常：

```text
hard fail
preserve family and all returned physical evidence
retry / relaunch / repair / alternate root = 0
stop at Planner
```

## 10. Three sparse liveness checks

单candidate预期约25分钟；clipping-only fallback总计约50分钟。Outer dispatch后仅执行：

```text
L1 approximately +60 s
L2 approximately +300 s
L3 approximately +540 s
```

每次只读检查：

```text
same visible Terminal tab
same outer PID and exact argv if still running
existing RUN progressive filenames, sizes and hashes
existing launch ledger / candidate / terminal evidence
duplicate or residual owned process count
```

禁止liveness期间做额外DNS、hostname、network、device、camera、capture、Ray、strip、cleanup或public analyzer
probe。若outer在L1/L2/L3前terminal，不重启，直接进入§11。若L3后仍运行，Executer把三次liveness、PID、
latest evidence、started time和estimated completion window追加到`EXECUTION_RESULT.md`后stop；Orchestrator创建
一次稀疏automation唤醒当前task复核同一PID/root。

## 11. Terminal read-only audit and handoff

Outer terminal后，只读审计同一PID/tab/FAMILY/RUN：

```text
outer exit and terminal status
candidate launch count = 1 or conditionally 2
candidate-2 unlock proof = exact branch plus candidate-1 lifecycle pass
launch ledger PID/argv/parent binding = exact
candidate terminal seals and outer terminal seal = exact
outer result classification = owner-recorded without reinterpretation
attempted / physical-returned / accepted counts = truthful
all returned CR3/sidecar path/bytes/SHA-256/remote IDs = complete
Python cleanup / shell cleanup / independent final-zero = pass
strip generation-bearing five-channel zero and Ray zero = owner-valid
no residual or duplicate owned process
retry / relaunch / alternate root / same-root repair = 0
HEAD and §2 source/config/wrapper hashes unchanged
formal / ambient / public analyzer / release / strip / TD-C = 0
```

不得运行public analyzer、自动重拍、补probe、successor release、full formal R6、strip stage或TD-C。
Executer只向`.agent-work/EXECUTION_RESULT.md`append完整evidence paths/hashes、counters、terminal classification和
Planner decision request，然后stop；不得修改PLAN或FULL。

## 12. Planner acceptance branches

```text
A. candidate 1 4/4 accepted and all lifecycle/evidence gates pass
   -> accept REF-P7-23 as qualified_1_2500

B. candidate 1 exact clipping-only plus full terminal lifecycle pass,
   candidate 2 4/4 accepted and all lifecycle/evidence gates pass
   -> accept REF-P7-23 as qualified_1_3200

C. valid scientific/quality rejection with truthful evidence and valid cleanup/seal
   -> retain evidence; Planner selects GUIDE-defined stop branch

D. runtime/readiness/ownership/evidence/accounting/cleanup/seal failure
   -> retain evidence; Planner writes only a bounded corrective decision
```

所有分支都必须stop回Planner。本PLAN不授权retry、fresh second prelaunch、third shutter、public analyzer、
successor release、full formal R6、strip stage或TD-C。只有Planner验收EQ outcome并归档本PLAN后，才可写新的
单一下一阶段package；Orchestrator随后独立更新FULL。

## 13. 维护性判断

本PLAN不修改production/test或新增parallel owner；它复用accepted production prelaunch、handoff validator、
EQ outer/candidate runner、physical ledger及terminal lifecycle owners。C3/C3E2已为冻结58-feature selection和
physical-return failure accounting提供`634/634` full-suite及one-shot evidence，新增风险仅为一次bounded live
acquisition。无需Advisor或架构重构。

---

## 14. Planner formal review — rejected before device entry

**Review 时间：** 2026-07-27 19:37 America/Edmonton

Reviewed inputs：

```text
PLAN SHA-256 =
  ca46edcbabf72f5d6e273efcf4abb544169b6aa71faeda9a1e90dc0aaab060a7
FULL_PLAN_REFERENCE SHA-256 at dispatch =
  f1c6ee1a7ddb72d7548baf923e1e7d58ebec520d632c7b00a9cf426b6d5fe105
EXECUTION_RESULT start SHA-256 =
  4b625a1cb410f78b54cc14e045fb1956a5c51859223b5e95c207b091bf46ee09
EXECUTION_RESULT reviewed SHA-256 =
  f933149efff307cf6fe8775cef689022b108c1b6fa8a674a61a82f2624f9bc88
HEAD =
  f37517af3ae25efb41f085904fd48f037980ed04
```

Planner decision：

```text
REF-P7-23 current activation =
  REJECTED_PREDEVICE_EXECUTER_PREFLIGHT_PATH_MAPPING
scientific EQ-R6 contract = PRESERVE
accepted C3/C3E2 evidence = PRESERVE
device/live attempt consumed = false
Advisor / Human decision required = false / false
next branch =
  one bounded continuation activation with exact canonical C3E2 11/12 paths
```

Root cause：

```text
Executer mapped logical validation artifact to nonexistent:
  .../validation-summary.json
canonical path is:
  .../11-validation-summary.json

canonical terminal path is:
  .../12-terminal-summary.json
```

Canonical evidence independently confirmed：

```text
/Volumes/4T/temp/rgbww-optimizer/
  p7-td-b-eq-r6-c3e2-offline-f37517a-20260727T1756/
  11-validation-summary.json
SHA-256 =
  3b136148a2571dba893447c0558d9663d08a44ceef59000bd19a1fb22c48dc3c

/Volumes/4T/temp/rgbww-optimizer/
  p7-td-b-eq-r6-c3e2-offline-f37517a-20260727T1756/
  12-terminal-summary.json
SHA-256 =
  c50e40e2b28fb0a69aa80e0016b39c06ff79f2818440c9b890417405d1ad309a
```

The C3E2 root still contains exact 12 numbered regular JSON artifacts. The hashes above equal the accepted PLAN and
C3E2 review values; there is no evidence drift.

Execution quality and lifecycle：

```text
static preflight processes attempted = 1
static preflight transactions completed = 0
static preflight exit = 1
post-failure read-only path/hash diagnostic = 1

production prelaunch / handoff validation / outer dispatch = 0 / 0 / 0
FAMILY / PRELAUNCH / RUN acquisition = 0 / 0 / 0
candidate 1 / candidate 2 = 0 / 0
capture / CR3 / sidecar = 0 / 0 / 0
network / DNS / camera / Ray / strip / cleanup = 0
retry / relaunch / alternate root / same-root repair = 0
formal / ambient / public analyzer / release / strip / TD-C = 0
```

Reserved fresh root remains absent：

```text
/Volumes/4T/temp/rgbww-optimizer/
  p7-td-b-exposure-qual-r6-f37517a-20260727T1928
FAMILY / PRELAUNCH / RUN = absent / absent / absent
```

Acceptance criteria were not met because the only allowed static preflight process exited nonzero. The Executer
correctly stopped and did not reinterpret the failure as permission to rerun. Because no acquisition owner, device
operation, prelaunch or dispatch occurred, the same still-absent reserved root and unchanged scientific/live budgets may
be frozen in one new activation package.

Residual risks：

```text
canonical filenames must be frozen together with hashes
new static preflight cap remains 1
any future mapping ambiguity must hard-stop
visible Terminal, candidate-2 clipping-only gate, physical cap and cleanup remain unchanged
```

Exact next branch：archive this reviewed package, then write one active bounded continuation PLAN that explicitly names
`11-validation-summary.json` and `12-terminal-summary.json`; it may run one new static preflight process and, only if
successful, continue the unchanged one-shot production prelaunch/handoff/visible-Terminal transaction.
