# REF-P7-23 / fresh EQ-R6 live activation after R2 recovery

**计划状态：** `executable_bounded_live_activation`

**Planner 日期：** 2026-07-27

**Reference task ID：** `REF-P7-23`

**PLAN contract ID：** `P7-TD-B-RAY-C-EXPOSURE-QUAL-R6-LIVE-ACTIVATION-AFTER-R2`

**Package kind：** `bounded_live_prelaunch_and_conditional_visible_terminal_dispatch`

**Expected HEAD：** `0f36671a351d537f204e8bc20849ac83e7e57c2b`

`PLAN_MACHINE_CONTRACT={"schema":"planner_execution_contract_v1","contract_id":"P7-TD-B-RAY-C-EXPOSURE-QUAL-R6-LIVE-ACTIVATION-AFTER-R2","reference_task_id":"REF-P7-23","package_kind":"bounded_live_prelaunch_and_conditional_visible_terminal_dispatch","expected_head":"0f36671a351d537f204e8bc20849ac83e7e57c2b","single_current_action":"run_fresh_production_prelaunch_then_validate_and_consume_only_its_handoff_within_600_seconds_for_one_visible_terminal_outer_dispatch","human_authorization_id":"P7-TD-B-RAY-C-EXPOSURE-QUAL-R6","human_confirmation_verified":true,"human_confirmation_reask_required":false,"human_confirmation_consumed":false,"static_preflight_cap":1,"production_prelaunch_invocation_cap":1,"prelaunch_root_acquisition_cap":1,"outer_dispatch_cap":1,"candidate_1_cap":1,"candidate_2_cap":1,"candidate_2_unlock":"candidate_1_exact_clipping_only_and_pass_seal","real_capture_cap":8,"formal_measurement_count":0,"ambient_measurement_count":0,"retry":0,"relaunch":0,"alternative_root":0,"same_root_repair":0,"prior_handoff_consumption_authorized":false,"source_edits_authorized":false,"test_edits_authorized":false,"docs_edits_authorized":false,"skill_edits_authorized":false,"wrapper_edits_authorized":false,"config_edits_authorized":false,"commit_authorized":false,"camera_access":"bounded_readiness_and_candidate_capture","ray_access":"bounded_readiness_candidate_light_and_cleanup","strip_access":"zero_state_only","public_analyzer_authorized":false,"strip_stage_authorized":false,"td_c_authorized":false,"planner_stop_required":true}`

**当前唯一动作：** 在全新FAMILY完成一个single cohesive activation transaction：

```text
production prelaunch exactly once
-> exact handoff validation within 600 s
-> visible macOS Terminal outer dispatch exactly once
-> three sparse liveness checks
-> Orchestrator automation or terminal Planner review
```

**唯一 Planner 停止点：** preflight、prelaunch、handoff validation或Terminal dispatch任一步失败立即stop；
outer在三次liveness内terminal则进入最终只读审计并stop；L3后仍存活则交Orchestrator automation并stop。
成功terminal也必须停回Planner，不得运行public analyzer或进入strip/TD-C。

## 1. R2 acceptance and non-reuse

```text
REF-P7-23-R2 = ACCEPTED_ZERO_RECOVERY_PROVED
REV-EQ-R6-LIVE-001 = CLOSED
Human EQ confirmation = valid, preserved and unconsumed
```

R2 evidence：

```text
FAMILY =
  /Volumes/4T/temp/rgbww-optimizer/p7-td-b-eq-r6-zero-recovery-0f36671-20260727T1642
terminal SHA-256 =
  808056f62ef9af114736e2263cdb2996e4c6c908b757913e7fec8b310d27bf6c
manifest SHA-256 =
  3353fa3dd3cda4ea6706ccf42aaf47ff75e5c692aadd58505ded105ebe25eefa
```

Review archive：

```text
.agent-work/PLANS/20260727-1650-p7-eq-r6-zero-recovery-r2-acceptance-review.md
SHA-256 982fd36a038452ea3381e79be28866e4b6834e48c8850f2d2760e60e86526631
```

Resolved debug：

```text
.agent-work/debug/resolved/20260725-p7-td-b-e2-r1-hostname-and-progressive-evidence.md
SHA-256 709e08aba350c233464b3b4fc58cebc0edb08c88e191f37a13e02f73a61b7387
```

R2 handoff永久是non-authorizing evidence。不得验证freshness、消费其argv或创建其RUN。

## 2. Human authorization

Human exact confirmation：

```text
P7-TD-B-RAY-C-EXPOSURE-QUAL-R6
```

它覆盖本PLAN冻结的local-lab readiness、Ray bounded light operation、cleanup及最多两个EQ-R6 exposure
qualification candidates。Executer不得再次询问Human。

R2 zero-only gate未消费确认。本包production prelaunch也不会单独耗尽确认；只有第8节outer Terminal
dispatch实际发生时记录：

```text
human_confirmation_consumed = true
```

若dispatch前失败，仍记录unconsumed；但不得据此自动重开package。

## 3. Frozen repository state

```text
REPO =
  /Users/ibobby/Projects/WLED-RGBWW
HEAD =
  0f36671a351d537f204e8bc20849ac83e7e57c2b
HEAD parent =
  93e72b833c2ebefb6cdcfe05dd996a9ae4fc97e8
HEAD subject =
  fix(p7): add eq-r6 prelaunch owner
```

Frozen hashes：

```text
advisor/4/4.GUIDE.md
  659152f6c0ae69c90c701de4e57c352d771e4f0bf75cf9410271ba0a94200e35
.agents/skills/camera-based-rgbww-optimizer/SKILL.md
  c8dd57a23ad684b4f7001f342ed3413a1abf4349bc6aeb90dbee7f5158139607
src/camera_based_rgbww_optimizer/optimization/measure_p7_thermal_diagnostics.py
  b58fb6c314dcf3ad17241690ffa66cd1b0bb01776321d438af2dd318a79f2ccb
src/camera_based_rgbww_optimizer/optimization/p7_thermal_diagnostics.py
  34758f854cd5b17f3f844d8f8312b31fdbda11965aa4f695a3b1421e19522dc3
tests/test_p7_td_b_r6_contract.py
  240c30d894c911a82a0c46193672900e470454c299e6d53f12386a003b201dff
config/hsi/p7-ray-td-b-exposure-policy-v2.json
  9e5ec953fdeedf0e73a26a3a476b7336febdbdb2c3e83819123c7b9ad4060ec2
tmp/run-p7-thermal-diagnostics.zsh
  2730d43507af14a531453978477439bb29ef93ae7dea8e0bddb6c2330e1242e5
```

Orchestrator dispatch时必须给出exact dynamic handoff：

```text
LIVE_PLAN_SHA256
LIVE_FULL_SHA256
LIVE_EXECUTION_RESULT_START_SHA256
```

PLAN不能自嵌自身hash。缺一、格式错误或current path/hash不符即stop。

## 4. Fresh unique live root

```text
SAFE_PARENT =
  /Volumes/4T/temp/rgbww-optimizer
FAMILY =
  /Volumes/4T/temp/rgbww-optimizer/p7-td-b-exposure-qual-r6-0f36671-20260727T1650
PRELAUNCH =
  ${FAMILY}/prelaunch
RUN =
  ${FAMILY}/run
```

开始时FAMILY/PRELAUNCH/RUN必须absent且non-symlink。Production prelaunch是唯一FAMILY/PRELAUNCH
acquisition owner；outer是唯一RUN acquisition owner。不得预建、复用、删除、repair或换root。

R2及两个旧失败FAMILY全部只读，不得跨PLAN消费handoff：

```text
/Volumes/4T/temp/rgbww-optimizer/p7-td-b-eq-r6-zero-recovery-0f36671-20260727T1642
/Volumes/4T/temp/rgbww-optimizer/p7-td-b-exposure-qual-r6-0f36671-20260727T1601
/Volumes/4T/temp/rgbww-optimizer/p7-td-b-eq-r6-zero-reachability-0f36671-20260727T1612
```

## 5. One static preflight

只允许一次local read/hash/stat preflight：

```text
HEAD / parent / subject = exact
PLAN/FULL/EXECUTION_RESULT start = Orchestrator dynamic hashes
第3节source hashes = exact
R2 archive/debug/terminal/manifest hashes = exact
R2 RUN = absent
SAFE_PARENT = safe
new FAMILY/PRELAUNCH/RUN = absent/non-symlink
repository .env = regular non-symlink if present
```

`.env`只可lstat，不得读取、打印、hash或复制。不得在本preflight做DNS、resolver、ping、HTTP、camera、Ray、
strip或cleanup probe。cap=1，失败即stop。

## 6. Fresh production prelaunch once

从repo root逐字运行一次：

```zsh
.venv/bin/python -m camera_based_rgbww_optimizer.optimization.measure_p7_thermal_diagnostics \
  --execute \
  --allow-device-control \
  --eq-r6-prelaunch \
  --experiment-id p7_td_b_command_switch_history_v1 \
  --source ray \
  --phase formal \
  --output-dir /Volumes/4T/temp/rgbww-optimizer/p7-td-b-exposure-qual-r6-0f36671-20260727T1650 \
  --run-name prelaunch \
  --code-checkpoint 0f36671a351d537f204e8bc20849ac83e7e57c2b \
  --human-authorization P7-TD-B-RAY-C-EXPOSURE-QUAL-R6 \
  --camera-backend remote
```

Invocation/root acquisition cap=1。不设置ESPHome host override，不使用R2 artifacts作为input。

Prelaunch允许readiness/zero/cleanup，不允许：

```text
capture / CR3 / NPY / TIFF = 0
nonzero strip output = 0
RUN / outer / candidate / dispatch = 0
formal measurement = 0
public analyzer = 0
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

若exit非零、artifact不全或terminal/manifest fail，保留证据并立即stop；不得补probe、cleanup或retry。

## 7. Exact handoff validation within 600 seconds

只有fresh prelaunch exit0后继续。必须在`prelaunch-terminal.json.sealed_at`后600秒内完成validation并
dispatch；超时立即stop，不能重跑prelaunch。

使用production `_eq_prelaunch_validate_root`做read-only validation，并独立确认：

```text
exact 9 names/order, strict JSON, modes 0700/0600, safe containment
terminal.status / manifest.status = pass/pass
manifest references = exact bytes/SHA-256
camera/Ray/Python/shell/final-zero = all pass
strip generation-bearing five-channel zero = true
Ray zero and validate_both_off = pass
capture/nonzero/dispatch counts = 0
RUN = absent/non-symlink
launch_handoff.ready_for_dispatch = true
launch_handoff.dispatch_count / outer_launch_count = 0/0
launch_handoff.run_root = exact new RUN
checkpoint / authorization = exact
outer_argv = 第8节exact argv
outer_argv_sha256 =
  0009b21f2cebc0b73bec750e4fc1234405b701fe8ee723c52b0d58ae31153b89
secret material = absent
```

Hash定义：UTF-8 compact JSON array，`separators=(",",":")`、`ensure_ascii=False`、无newline。

任一不符立即stop。不得编辑argv、重建handoff或使用R2 handoff替换。

## 8. Visible Terminal exact single dispatch

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
/Volumes/4T/temp/rgbww-optimizer/p7-td-b-exposure-qual-r6-0f36671-20260727T1650
--run-name
run
--code-checkpoint
0f36671a351d537f204e8bc20849ac83e7e57c2b
--human-authorization
P7-TD-B-RAY-C-EXPOSURE-QUAL-R6
--camera-backend
remote
```

在一个可见macOS Terminal tab运行exact：

```zsh
cd /Users/ibobby/Projects/WLED-RGBWW && exec /Users/ibobby/Projects/WLED-RGBWW/.venv/bin/python -m camera_based_rgbww_optimizer.optimization.measure_p7_thermal_diagnostics --execute --allow-device-control --eq-r6-orchestrate --experiment-id p7_td_b_command_switch_history_v1 --source ray --phase formal --output-dir /Volumes/4T/temp/rgbww-optimizer/p7-td-b-exposure-qual-r6-0f36671-20260727T1650 --run-name run --code-checkpoint 0f36671a351d537f204e8bc20849ac83e7e57c2b --human-authorization P7-TD-B-RAY-C-EXPOSURE-QUAL-R6 --camera-backend remote
```

必须使用Terminal visible `do script`/等价前台tab，不得作为Codex background process。dispatch call cap=1；
Terminal API不确定/失败也计attempted=1，不得重试。

记录：

```text
Terminal window/tab identifier
exact command and SHA-256
dispatch attempted = 1
observed outer PID and exact argv if uniquely bound
RUN/live-plan first appearance
human_confirmation_consumed = true
```

## 9. Frozen scientific contract

```text
experiment = p7_td_b_command_switch_history_v1
source / phase / variant = ray / formal / core
ambient/formal measurement count = 0/0
candidate 1 shutter = 1/2500 s
candidate 2 shutter = 1/3200 s
candidate 2 unlock = candidate 1 exact clipping_only plus pass seal
candidate count = 1, or 2 only under unlock
states per candidate = A@600s plus C@60/120/300/600s
physical CR3 cap = 4 per candidate, 8 total
retry / alternate shutter / public analyzer = 0/0/0
```

每个capture保留CR3/sidecar path、bytes、SHA-256、remote IDs、attempt accounting与quality evidence。
任何runtime/quality/ownership/cleanup/seal异常hard fail；outer仍执行Python/shell cleanup、independent final-zero
和terminal seal。

## 10. Three sparse liveness checks

预期单候选约25分钟；clipping branch约50分钟。dispatch后只做：

```text
L1 approximately +60 s
L2 approximately +300 s
L3 approximately +540 s
```

每次只读：

```text
same Terminal tab
exact outer PID/argv if running
existing RUN progressive filenames/hashes
existing launch ledger/terminal evidence
duplicate or residual owned process
```

不得做device/network probe、capture call、light/cleanup command或public analyzer。

若outer在L1/L2/L3前terminal，不重启，直接第11节。若L3后仍运行，Executer把three liveness、PID、latest
evidence、started time和estimated completion写入EXECUTION_RESULT后stop；Orchestrator创建稀疏automation。

## 11. Terminal read-only audit

outer terminal后，只读审计同一PID/tab/FAMILY/RUN：

```text
outer exit and terminal status
candidate launch count = 1 or conditionally 2
launch ledger PID/argv/parent binding = exact
candidate terminal seals and outer candidate terminals = exact
outer result classification = recorded without reinterpretation
attempted/physical-returned/accepted counts = truthful
CR3/sidecar path/bytes/hash/remote IDs = complete
Python/shell/independent final-zero = pass
strip and Ray final zero = owner-valid
no residual/duplicate process
no retry/relaunch/alternate root
HEAD/source hashes unchanged
```

不得运行public analyzer、自动重拍、strip stage或TD-C。Executer把完整evidence与Planner decision request
追加到EXECUTION_RESULT并stop。

## 12. Acceptance branches

```text
A. candidate 1 accepted
   -> accept REF-P7-23

B. candidate 1 clipping_only and candidate 2 accepted
   -> accept bounded clipping branch

C. scientific/quality rejection with valid lifecycle/cleanup
   -> retain evidence; Planner decides Advisor branch

D. runtime/readiness/ownership/evidence/cleanup failure
   -> retain evidence; Planner-only corrective decision
```

本PLAN不授权retry、fresh prelaunch、third shutter、public analyzer、strip stage或TD-C。

## 13. 维护性判断

R2已验证network/zero recovery并关闭debug note；live package继续复用production prelaunch、outer、wrapper和
candidate runner的单一ownership。Fresh root与600秒handoff窗口避免跨PLAN/stale consumption，visible Terminal
及三次稀疏liveness符合长跑约束；无需Human重授权、Advisor或架构重构。

---

## 14. Planner review（2026-07-27 17:21 MDT）

Reviewed：

```text
PLAN SHA-256 =
  58e2256a9fe5609e2ca33a32b3977f7d6c3dce8bf8848441266fca264a2c25f8
EXECUTION_RESULT SHA-256 =
  3dcc8ce090308940c3f2aeb6da65053eb7bc6df9089760793bf87b3b30edac81
Orchestrator FULL SHA-256 =
  dd2fa75cc49ad10791e373654ea646cf452e14f20e6712d3b4efb5bfe2c44ff0
HEAD =
  0f36671a351d537f204e8bc20849ac83e7e57c2b
```

Terminal facts：

```text
FAMILY =
  /Volumes/4T/temp/rgbww-optimizer/p7-td-b-exposure-qual-r6-0f36671-20260727T1650
outer PID = 61224 terminal
owned residual process = 0
dispatch / candidate-1 / candidate-2 / retry = 1/1/0/0
capture attempted / physical returned / accepted = 1/1/0
formal / ambient / public analyzer = 0/0/0
```

The RAW report is quality accepted:

```text
optimization patches = 23
accepted observations = 92
rejected observations = 0
frozen policy IDs = 58
missing = 0
extra non-policy = 34
```

The runner compared all 92 insertion-ordered observations directly with the 58-ID policy tuple. This is a runtime
feature-selection owner defect, not clipping and not a scientific rejection. Candidate 2 correctly remained locked.

Physical evidence and cleanup：

```text
CR3 bytes / SHA-256 =
  15001300 /
  281ec241bf92ac9f0da9f5f3539f9b76e08c1bbdcaf99cba60328cee1746e2fa
sidecar bytes / SHA-256 =
  4722 /
  1f270c4e50aee2f751e10bcaf0da7a14c07efcb9d59e6511faf9589e16998a86
remote capture/request IDs = complete
Python/shell/final-zero = pass/pass/pass
```

Progressive accounting gap：

```text
candidate-failure physical_returned = 0
candidate-result / terminal-seal / physical ledger = 1/1/1
```

Decision：

```text
REF-P7-23 = REJECTED_BRANCH_D_RUNTIME_FEATURE_SELECTION_CONTRACT
REV-EQ-R6-FEATURE-001 = OPEN
REV-EQ-R6-PHYSICAL-FAILURE-002 = OPEN
1650 FAMILY = immutable, no retry/repair/analyzer
Human EQ authorization = consumed by 1650 outer dispatch
future live authorization = not inferred
Advisor decision = not required for offline correction
next = REF-P7-23-C3
```

The initial L1 front-tab misreport was corrected by L2/L3 OS tty ownership and never entered the launch ledger; it is
not a separate production defect. The only next action is a pure-offline code/test/evidence correction.
