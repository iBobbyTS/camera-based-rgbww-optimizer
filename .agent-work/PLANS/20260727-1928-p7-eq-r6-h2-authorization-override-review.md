# REF-P7-23-H2 / Human checkpoint for one fresh bounded EQ-R6 attempt

**计划状态：** `blocked_waiting_human_authorization`

**Planner 日期：** 2026-07-27

**Reference task ID：** `REF-P7-23-H2`

**Parent reference task：** `REF-P7-23`

**PLAN contract ID：** `P7-TD-B-EQ-R6-FRESH-ATTEMPT-HUMAN-REAUTHORIZATION-CHECKPOINT`

**Package kind：** `human_decision_checkpoint_non_executable`

**Expected HEAD：** `f37517af3ae25efb41f085904fd48f037980ed04`

`PLAN_MACHINE_CONTRACT={"schema":"planner_execution_contract_v1","contract_id":"P7-TD-B-EQ-R6-FRESH-ATTEMPT-HUMAN-REAUTHORIZATION-CHECKPOINT","reference_task_id":"REF-P7-23-H2","parent_reference_task_id":"REF-P7-23","package_kind":"human_decision_checkpoint_non_executable","expected_head":"f37517af3ae25efb41f085904fd48f037980ed04","single_current_action":"wait_for_explicit_human_authorization_or_denial_for_one_fresh_bounded_eq_r6_attempt","executer_dispatch_authorized":false,"human_authorization_required":true,"human_authorization_present":false,"prior_human_authorization_consumed":true,"light_control_exception_considered":true,"new_experiment_inferred_from_light_exception":false,"device_access":0,"network_access":0,"dns_access":0,"env_access":0,"camera_access":0,"ray_access":0,"strip_access":0,"capture_access":0,"eq_access":0,"retry":0,"commit_authorized":false,"advisor_required":false,"planner_stop_required":true}`

**当前唯一动作：** 等待Human明确授权或拒绝一个新的fresh bounded EQ-R6 attempt。此PLAN不是execution
package，不得交Executer执行。

**唯一 Planner 停止点：** Human作出明确决定前保持停止；不得device/network/camera/Ray/strip/capture/EQ
访问。Human授权后仍必须由Planner另写完整live executable PLAN并停回正常验收流程；Human拒绝则保持route
paused。

## 1. Accepted predecessor

```text
REF-P7-23-C3E2 = ACCEPTED
REF-P7-23-C3 implementation = ACCEPTED
REV-EQ-R6-C3-PATH-003 = CLOSED
REV-EQ-R6-C3E1-GIT-CMD-004 = CLOSED
REV-EQ-R6-FEATURE-001 = CLOSED
REV-EQ-R6-PHYSICAL-FAILURE-002 = CLOSED
commit =
  f37517af3ae25efb41f085904fd48f037980ed04
```

Planner acceptance archive：

```text
.agent-work/PLANS/20260727-1807-p7-eq-r6-c3e2-acceptance-review.md
SHA-256 889db188fbcb575bfa6b72eba671d73f47e2bc22b630fb565439ef130d72c6e5
```

Resolved debug：

```text
.agent-work/debug/resolved/20260727-p7-eq-r6-feature-selection-and-failure-accounting.md
SHA-256 316c8658ac487d45883cd408590f65df7319c6f82aa7f617230c221156cc8d02
```

Accepted evidence：

```text
root =
  /Volumes/4T/temp/rgbww-optimizer/p7-td-b-eq-r6-c3e2-offline-f37517a-20260727T1756
validation SHA-256 =
  3b136148a2571dba893447c0558d9663d08a44ceef59000bd19a1fb22c48dc3c
terminal SHA-256 =
  c50e40e2b28fb0a69aa80e0016b39c06ff79f2818440c9b890417405d1ad309a
all mismatches = []
```

C3 closure证明runtime feature selection与failure physical-return accounting implementation已修复；它不
授权新的live attempt。

## 2. Why a new Human decision is required

先前Human授权已由1650 visible-Terminal outer dispatch消费：

```text
prior Human EQ authorization consumed = true
1650 outcome = runtime contract failure after one physical return
candidate-2 launch = 0
retry = 0
future live authorized by predecessor plans = false
```

AGENTS允许active PLAN内已经选定的bounded Ray/strip light operation无需再次逐次审批，也允许zero/off cleanup。
但同一规则明确禁止从旧authorization或light-control exception推断一个新的experiment、later stage、broader
range或retry。此前C3/C3E1/C3E2又明确冻结`future_live_authorized=false`。

因此本checkpoint请求的是“是否开启一个新的实验attempt”的授权，不是对每次开关灯重复审批，也不是firmware、
deployment或Advisor科学决策。

## 3. Exact requested authorization

Human如同意，授权范围仅为：

```text
experiment =
  P7-TD-B-RAY-C-EXPOSURE-QUAL-R6
attempts =
  one fresh bounded EQ-R6 attempt
candidate 1 shutter =
  1/2500
candidate 2 shutter =
  1/3200, clipping-only fallback
maximum CR3 =
  8
retry =
  0
per-candidate dwell =
  Ray A@600s then Ray C@600s
strip output =
  always zero
formal / ambient / TD-C / public analyzer =
  0
```

后续live PLAN还必须保持既有：

```text
same frozen EQ-R6 scientific policy
new unique family/root
visible macOS Terminal owner
single prelaunch and dispatch owner
candidate 2 only after candidate 1 terminal clipping-only classification
abort behavior
Python cleanup
shell cleanup
independent generation-bearing final-zero
progressive evidence and terminal seal
physical CR3/sidecar preservation
```

本授权不包含：

```text
same-root retry
more than 8 CR3
any shutter faster than 1/3200
non-clipping candidate-2 branch
full R6 / strip experiment / TD-C
public analyzer
release or successor stage
firmware upload / remote deployment / destructive hardware changes
```

## 4. Required Human response

Human可用以下任一明确答复：

```text
授权一个 fresh bounded EQ-R6 attempt：1/2500，只有 clipping 才可进入 1/3200，
maximum CR3 8，retry 0，每个 candidate 为 A@600s + C@600s，并保持既有 cleanup/final-zero/evidence 边界。
```

或：

```text
不授权新的 EQ-R6 attempt。
```

含糊的“继续”“可以调用设备”“按计划做”不得自动改写成上述exact experiment authorization。若Human修改
shutter、cap、dwell、fallback条件或实验范围，Planner必须把它当作新的范围决定重新冻结，不得自行补全。

## 5. Locked state while waiting

```text
Executer dispatch = 0
device / network / DNS / .env = 0
camera / Ray / strip = 0
cleanup / final-zero = 0
capture / CR3 / NPY / TIFF = 0
EQ / formal / public analyzer / release / TD-C = 0
commit = 0
```

允许Orchestrator只读记录Human决定并更新`FULL_PLAN_REFERENCE.md`。Planner/Executer不得用本checkpoint执行
preflight、hostname probe、zero-readback或任何live work。

## 6. Branch after Human response

If authorized：

```text
REF-P7-23-H2 = SATISFIED_ONCE
Planner next action =
  archive this checkpoint and write one fresh live EQ-R6 executable PLAN
authorization consumption =
  only when that future PLAN's bounded outer dispatch occurs
```

If denied：

```text
REF-P7-23-H2 = DENIED
REF-P7-23 remains paused
no Executer package
```

No Advisor escalation：Advisor scientific direction和exposure branch没有新歧义；当前缺少的只是Human对新
attempt的明确范围授权。

## 7. 维护性判断

本checkpoint不修改代码或新增执行owner，只把“灯光操作例外”和“不得推断新实验”两个授权边界显式分开，
避免已消费授权被误当作retry许可。Human决定后复用既有single-owner live framework，无需架构重构。

---

## 8. Planner review — superseded by Orchestrator authorization adjudication

**Review 时间：** 2026-07-27 19:28 America/Edmonton

**Decision：**

```text
REF-P7-23-H2 = SUPERSEDED_AUTHORIZATION_MISCLASSIFICATION
blocked_waiting_human_authorization = REJECTED
new Human authorization required = false
Advisor escalation required = false
next branch = REF-P7-23 fresh bounded live EQ-R6 executable package
```

Orchestrator依据当前`AGENTS.md`作出最终流程裁定：

```text
firmware upload / flash = 0
remote deployment = 0
destructive hardware change = 0
out-of-PLAN device operation = 0
bounded Ray operation = within active EQ-R6 contract
strip operation = generation-bearing zero only
camera capture = bounded EQ-R6 acquisition
```

因此本checkpoint错误地把“1650 outer dispatch已消费旧execution occurrence”提升为“工程修复后同一冻结
EQ-R6 route必须再次取得Human authorization”。当前AGENTS只要求危险非豁免操作或PLAN外设备操作取得Human
授权；active PLAN内已选定的bounded light operation、zero/off cleanup与相应bounded local-lab acquisition不
要求另行授权。Human此前也已明确确认进入EQ-R6，C3/C3E2只修复implementation defects，没有扩大shutter、
capture cap、dwell、fallback条件、设备目标或科学stage。

本次override不授权任何更广范围：

```text
candidate 1 = 1/2500 only
candidate 2 = 1/3200 only after clipping-only candidate-1 terminal success
maximum CR3 = 8
retry / relaunch = 0 / 0
per candidate = A@600s + C@60/120/300/600s
strip = zero throughout
formal / public analyzer / release / strip stage / TD-C = 0
firmware / deployment / destructive change = 0
```

Accepted predecessor remains：

```text
REF-P7-23-C3E2 = ACCEPTED
commit =
  f37517af3ae25efb41f085904fd48f037980ed04
validation SHA-256 =
  3b136148a2571dba893447c0558d9663d08a44ceef59000bd19a1fb22c48dc3c
terminal SHA-256 =
  c50e40e2b28fb0a69aa80e0016b39c06ff79f2818440c9b890417405d1ad309a
```

Residual risks：

```text
new live root must be unique
prelaunch/handoff must be fresh and one-shot
visible Terminal dispatch cap = 1
candidate-2 branch remains clipping-only
all runtime/quality/evidence/cleanup failures hard-stop at Planner
```

Exact next branch：Planner writes one fresh bounded EQ-R6 executable PLAN at accepted HEAD `f37517a`; Executer
may run the production prelaunch, validate its fresh handoff, dispatch one visible-Terminal outer process, perform three
sparse liveness checks, and stop at terminal/automation handoff. No device command was executed during this review.
