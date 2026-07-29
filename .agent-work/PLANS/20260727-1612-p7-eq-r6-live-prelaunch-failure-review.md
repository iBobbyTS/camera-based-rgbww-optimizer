# REF-P7-23 / EQ-R6 单次 live activation

**计划状态：** `executable_bounded_live_activation`

**Planner 日期：** 2026-07-27

**Reference task ID：** `REF-P7-23`

**PLAN contract ID：** `P7-TD-B-RAY-C-EXPOSURE-QUAL-R6-LIVE-ACTIVATION`

**Package kind：** `bounded_live_prelaunch_and_conditional_terminal_dispatch`

**Expected HEAD：** `0f36671a351d537f204e8bc20849ac83e7e57c2b`

`PLAN_MACHINE_CONTRACT={"schema":"planner_execution_contract_v1","contract_id":"P7-TD-B-RAY-C-EXPOSURE-QUAL-R6-LIVE-ACTIVATION","reference_task_id":"REF-P7-23","package_kind":"bounded_live_prelaunch_and_conditional_terminal_dispatch","expected_head":"0f36671a351d537f204e8bc20849ac83e7e57c2b","single_current_action":"activate_eq_r6_once_via_production_prelaunch_then_same_package_handoff_consumption_and_one_visible_terminal_dispatch","human_authorization_id":"P7-TD-B-RAY-C-EXPOSURE-QUAL-R6","human_confirmation_verified":true,"human_confirmation_reask_required":false,"human_confirmation_consumed_by_offline_corrections":false,"prelaunch_invocation_cap":1,"prelaunch_root_acquisition_cap":1,"outer_dispatch_cap":1,"candidate_1_cap":1,"candidate_2_cap":1,"candidate_2_unlock":"candidate_1_exact_clipping_only_and_pass_seal","real_capture_cap":8,"formal_measurement_count":0,"ambient_measurement_count":0,"retry":0,"relaunch":0,"alternative_root":0,"same_root_repair":0,"source_edits_authorized":false,"test_edits_authorized":false,"docs_edits_authorized":false,"skill_edits_authorized":false,"wrapper_edits_authorized":false,"config_edits_authorized":false,"commit_authorized":false,"device_access":"bounded_by_this_plan","camera_access":"bounded_readiness_and_candidate_capture","ray_access":"bounded_readiness_candidate_light_and_cleanup","strip_access":"zero_state_only","public_analyzer_authorized":false,"strip_stage_authorized":false,"td_c_authorized":false,"planner_stop_required":true}`

**当前唯一动作：** 完成一个不可拆分的EQ-R6 activation transaction：先单次运行production
`--eq-r6-prelaunch`；只在该owner以exact pass artifacts封口后，由同一active package验证并消费其
`launch_handoff`，随即在可见macOS Terminal中exact dispatch一次outer owner；完成三次稀疏liveness
后交回Orchestrator。prelaunch pass不是独立阶段完成，也不得跨PLAN保存为未来launch凭据。

**唯一 Planner 停止点：** 以下任一条件立即停止并handoff，不得重试、换root、repair、补probe或重新
dispatch：

- static preflight、production prelaunch、handoff validation或Terminal dispatch失败；
- handoff超过本PLAN规定的freshness window；
- outer在三次liveness内terminal；
- 完成三次liveness且outer仍存活（此时由Orchestrator建立automation）；
- automation后outer到达terminal并完成最终只读审计。

不得进入public analyzer、strip stage或TD-C。

## 1. Planner decision and archive

C2E2正式通过：

```text
REF-P7-23-C2E2 = ACCEPTED
REF-P7-23-C2 = ACCEPTED_THROUGH_C2E2
REV-EQ-R6-C2-001 = CLOSED
REV-EQ-R6-C2E1-001 = CLOSED
implementation commit 0f36671 = ACCEPTED_FOR_THIS_LIVE_ACTIVATION
```

Reviewed hashes：

```text
C2E2 PLAN =
  107823e5dc3810d3e1a813e970ec2ab89ffa1c0b292856baccef8ec901c79405
C2E2 EXECUTION_RESULT =
  3b5b9619537c099967003dc1844df9c0424d457d7b547a39d44e6fd87595c5cf
Orchestrator FULL =
  0d36aca2fdef762fbc9c1fa53f66b542310ad3a6b19ffc35eb61f511720b5d74
C2E2 validation =
  3cf1e52483b35438f4be6c1036ead3993e41dd288fdcea1ebbed72a8869140c2
C2E2 terminal =
  6fdf31a4992b3175f10492704c96917a32d11357045aec9310c969e63c49747e
```

Review archive：

```text
.agent-work/PLANS/20260727-1601-p7-eq-r6-c2e2-acceptance-review.md
SHA-256 03d1a30d636a2273b38263f3a727d32ae8f58782427dab9b9ab60cf116e1a51d
```

## 2. Authorization and ownership

Human已确认exact authorization：

```text
P7-TD-B-RAY-C-EXPOSURE-QUAL-R6
```

本确认覆盖本PLAN冻结的同一local-lab设备、readiness、Ray light operation、cleanup及最多两个候选的
EQ-R6 exposure qualification。Executer不得再次询问Human。

C2/C2E1/C2E2纯离线纠偏未消费该确认。production prelaunch与outer dispatch属于本次同一个activation
transaction；prelaunch不会耗尽或失效该确认。只有outer Terminal dispatch实际发生时，才记录
`human_confirmation_consumed=true`。若在dispatch前失败，则本包停止；不得据此自行再开一次package。

Ownership：

```text
production prelaunch owner =
  run_td_b_eq_r6_prelaunch
outer live owner =
  orchestrate_td_b_eq_r6
candidate wrapper owner =
  tmp/run-p7-thermal-diagnostics.zsh
candidate runner owner =
  --eq-r6-single-candidate
activation/handoff consumer =
  this Executer under this single active PLAN
Planner owns PLAN and acceptance
Orchestrator owns FULL and automation
```

Executer不得编辑PLAN/FULL。所有进度、evidence和decision request写入
`.agent-work/EXECUTION_RESULT.md`。

## 3. Frozen inputs

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

Frozen source hashes：

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

Orchestrator dispatch时另行给出exact：

```text
LIVE_PLAN_SHA256
LIVE_FULL_SHA256
LIVE_EXECUTION_RESULT_START_SHA256
```

PLAN不能自嵌自身hash；缺少或不匹配即stop。不得从history猜测。

## 4. New unique live root

本包只使用：

```text
FAMILY =
  /Volumes/4T/temp/rgbww-optimizer/p7-td-b-exposure-qual-r6-0f36671-20260727T1601
PRELAUNCH =
  ${FAMILY}/prelaunch
RUN =
  ${FAMILY}/run
```

该FAMILY是现有safe parent
`/Volumes/4T/temp/rgbww-optimizer`的direct child。此设计避免预先创建额外container owner，同时绝不复用：

```text
/Volumes/4T/temp/rgbww-optimizer/p7-td-b-exposure-qual-r6/eq-r6-93e72b8-20260727T1445
/Volumes/4T/temp/rgbww-optimizer/p7-td-b-eq-r6-c2e1-0f36671-20260727T1535
```

开始时FAMILY/PRELAUNCH/RUN必须全部absent且non-symlink。production prelaunch是唯一FAMILY和PRELAUNCH
root acquisition owner；outer是唯一RUN acquisition owner。不得预建、复用、删改、repair或换root。

## 5. Static preflight

本节仅允许一次本地read/hash/stat preflight；不得做额外DNS、ping、HTTP、camera、Ray、strip或cleanup
probe。真实readiness由production prelaunch唯一拥有。

必须确认：

```text
HEAD / parent / subject = 第3节exact值
PLAN/FULL/EXECUTION_RESULT start = Orchestrator handed-off hashes
第3节7个source hashes = exact
review archive hash = exact
C2E2 12 JSON strict，validation/terminal hashes = exact
/Volumes/4T/temp/rgbww-optimizer = directory and non-symlink
FAMILY/PRELAUNCH/RUN = absent and non-symlink
repository .env = regular non-symlink if present
```

`.env`只允许`lstat`存在性/类型，不得打印、复制、hash或记录值。Ray public default按现有owner读取；
本PLAN不新建override。

任一失败立即stop；prelaunch invocation=0，outer dispatch=0。

## 6. Production prelaunch exactly once

从repo root逐字运行一次：

```zsh
.venv/bin/python -m camera_based_rgbww_optimizer.optimization.measure_p7_thermal_diagnostics \
  --execute \
  --allow-device-control \
  --eq-r6-prelaunch \
  --experiment-id p7_td_b_command_switch_history_v1 \
  --source ray \
  --phase formal \
  --output-dir /Volumes/4T/temp/rgbww-optimizer/p7-td-b-exposure-qual-r6-0f36671-20260727T1601 \
  --run-name prelaunch \
  --code-checkpoint 0f36671a351d537f204e8bc20849ac83e7e57c2b \
  --human-authorization P7-TD-B-RAY-C-EXPOSURE-QUAL-R6 \
  --camera-backend remote
```

Invocation cap=1。不得用wrapper、alias、额外env override、retry或第二owner。

Prelaunch允许：

```text
camera remote-v2 readiness
Ray readiness/readback
strip zero/off verification
Python cleanup
shell cleanup
independent final-zero
```

Prelaunch禁止：

```text
capture / CR3 / NPY / TIFF = 0
nonzero strip output = 0
candidate / outer dispatch = 0
formal measurement = 0
public analyzer = 0
```

PRELAUNCH exact artifacts：

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

若process非零、异常、artifact不全或terminal/manifest fail：保留证据，outer dispatch=0，立即stop。

## 7. Same-package handoff validation

只有prelaunch exit 0后才能继续。Executer必须在10分钟内完成本节并dispatch；以
`prelaunch-terminal.json` sealed time为起点，超过600秒即stop，不得重跑prelaunch。

必须用production `_eq_prelaunch_validate_root`做一次read-only validation，并独立确认：

```text
PRELAUNCH exact 9 names, regular, non-symlink, contained, mode 0600
PRELAUNCH directory mode = 0700
strict JSON = 9/9
prelaunch-terminal.status = pass
prelaunch-manifest.status = pass
manifest references = exact bytes/SHA-256
cleanup and final-zero = pass; strip and Ray verified off
capture/nonzero/dispatch counts = 0
RUN = absent/non-symlink
launch_handoff.ready = true
launch_handoff.dispatch_count = 0
launch_handoff.outer_launch_count = 0
launch_handoff.run_root = exact RUN
launch_handoff.code_checkpoint = exact HEAD
launch_handoff.human_authorization = exact authorization ID
launch_handoff.outer_argv = 第8节exact argv
launch_handoff.outer_argv_sha256 =
  20ce0adc10c95a880995593cbbffd39a52ef9453d348affee0ad78471af108a8
secret material in artifacts/argv = absent
```

该hash定义为UTF-8 compact JSON array（`separators=(",",":")`，无newline）的SHA-256。

任一不符立即stop；不得手工改argv、重建handoff或补artifact。

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
/Volumes/4T/temp/rgbww-optimizer/p7-td-b-exposure-qual-r6-0f36671-20260727T1601
--run-name
run
--code-checkpoint
0f36671a351d537f204e8bc20849ac83e7e57c2b
--human-authorization
P7-TD-B-RAY-C-EXPOSURE-QUAL-R6
--camera-backend
remote
```

Executer只可把该validated argv进行standard shell quoting，并在一个可见macOS Terminal tab中运行：

```zsh
cd /Users/ibobby/Projects/WLED-RGBWW && exec /Users/ibobby/Projects/WLED-RGBWW/.venv/bin/python -m camera_based_rgbww_optimizer.optimization.measure_p7_thermal_diagnostics --execute --allow-device-control --eq-r6-orchestrate --experiment-id p7_td_b_command_switch_history_v1 --source ray --phase formal --output-dir /Volumes/4T/temp/rgbww-optimizer/p7-td-b-exposure-qual-r6-0f36671-20260727T1601 --run-name run --code-checkpoint 0f36671a351d537f204e8bc20849ac83e7e57c2b --human-authorization P7-TD-B-RAY-C-EXPOSURE-QUAL-R6 --camera-backend remote
```

必须使用macOS Terminal的visible `do script`/等价前台tab，不得作为Codex background process。
outer dispatch call cap=1。不得同时开第二tab、第二Terminal、second outer或restart。

dispatch后记录：

```text
Terminal window/tab identifier
dispatch attempted count = 1
exact command and SHA-256
observed outer PID（若可唯一绑定）
RUN/live-plan/launch-ledger first appearance
human_confirmation_consumed = true
```

若Terminal API返回不确定或失败，也按attempted=1处理；不得重试。只读检查RUN和exact argv/PID ownership，
然后stop。

## 9. Frozen scientific contract

Outer owner必须保持：

```text
experiment = p7_td_b_command_switch_history_v1
source = ray
phase = formal
variant = core
ambient captures = 0
formal measurements = 0
candidate 1 shutter = 1/2500 s
candidate 2 shutter = 1/3200 s
candidate 2 unlock = candidate 1 exact clipping_only and pass terminal seal
candidate count = 1, or 2 only under that branch
states per candidate = A@600s plus C@60s/120s/300s/600s
physical CR3 cap = 4 per candidate, 8 total
retry = 0
alternate shutter = 0
public analyzer = 0
```

每个capture都必须保留CR3/sidecar path、bytes、SHA-256、remote IDs、attempt accounting和quality
evidence。任何device/camera/Ray/strip/wrapper/cleanup/seal异常都hard fail；outer仍必须完成Python cleanup、
shell cleanup、独立final-zero和terminal evidence。

## 10. Three sparse liveness checks

预期单候选约25分钟；若clipping-only解锁第二候选，约50分钟。dispatch后只做三次稀疏只读检查：

```text
L1 = approximately +60 s
L2 = approximately +300 s
L3 = approximately +540 s
```

每次只允许：

```text
confirm same Terminal tab
confirm exact outer PID/argv if still running
inspect existing RUN progressive JSON/log filenames and hashes
inspect existing candidate launch ledger / terminal evidence
check for owned residual/duplicate processes
```

禁止设备probe、ping、HTTP、capture call、light command、cleanup call或public analyzer。

若outer在任一次检查前已terminal：不重启；直接进入第11节。若L3后仍运行，Executer向
`EXECUTION_RESULT.md`写入三次liveness、PID、latest evidence、started time和预计完成窗口，然后stop；
Orchestrator建立一次稀疏automation来唤醒本task。不得由Executer后台轮询。

## 11. Terminal read-only audit

outer terminal后，只读审计同一PID、同一Terminal tab、同一FAMILY/RUN：

```text
outer process terminal and exit observed
candidate launch count = 1 or conditionally 2
each launch ledger PID/argv/parent binding = exact
candidate terminal seal references = exact
outer candidate terminal artifacts = exact
outer result/terminal status and classification = recorded without reinterpretation
attempted captures / physical returned / accepted counts = truthful
CR3 and sidecar path/bytes/hash/remote IDs = complete
Python cleanup / shell cleanup / independent final-zero = pass
strip and Ray final zero = generation-bearing/owner-valid
no owned residual process
no retry/relaunch/alternate root
HEAD/source hashes = unchanged
```

不得运行public analyzer，不得自动进入strip stage或TD-C，不得自动重拍。

无论outer成功、scientific rejection或runtime failure，Executer都把完整evidence paths/hashes、call counts、
classification、cleanup和decision request追加到`EXECUTION_RESULT.md`，然后停在Planner验收门。

## 12. Acceptance branches

Planner terminal review后只允许以下分支：

```text
A. one candidate accepted
   -> REF-P7-23 accepted; Orchestrator更新FULL，选择下一GUIDE task

B. candidate 1 clipping_only; candidate 2 accepted
   -> REF-P7-23 accepted through bounded clipping branch

C. quality/scientific rejection with valid lifecycle and cleanup
   -> retain evidence; stop for Planner/Advisor branch decision

D. runtime/readiness/ownership/evidence/cleanup failure
   -> retain evidence; bounded corrective package only after Planner review
```

本PLAN不预授权任何retry、fresh prelaunch、third shutter、public analyzer、strip stage或TD-C。

## 13. 维护性判断

本包不改生产代码；prelaunch、outer、wrapper与candidate runner仍各自只有单一owner。把prelaunch与handoff
消费定义为同一个activation transaction，避免跨PLAN的stale handoff，同时不引入第二个设备状态机。
三次稀疏liveness和Orchestrator automation保持长跑ownership清晰；无需Advisor或架构重构。

---

## 14. Planner review（2026-07-27 16:12 MDT）

Reviewed：

```text
PLAN SHA-256 =
  581ef8857c4bb2224765d1c914d48bd324b7d264b773692f33451f6c34b6cc4f
EXECUTION_RESULT SHA-256 =
  3c51f17c9f21d6a9d7225e8ffde89181b6c6b103d3839a27ef4c09ce3135d694
Orchestrator FULL SHA-256 =
  bb2b54f9fb70bcdc2ef4dc4cc3003582b7dc6dc6cca4d7342e21f77cf82b168e
HEAD =
  0f36671a351d537f204e8bc20849ac83e7e57c2b
```

Failure evidence：

```text
FAMILY =
  /Volumes/4T/temp/rgbww-optimizer/p7-td-b-exposure-qual-r6-0f36671-20260727T1601
prelaunch terminal SHA-256 =
  f9f106652c32a506772f676175d60d317f3d5137a1891072b9ca448d1ec9bd02
prelaunch manifest SHA-256 =
  1cc926a0b0212fa2c350cf50ad8863ad5c1741b9f3bb25c9694253b273d48dd4
```

Planner independently confirmed：

```text
PRELAUNCH directory mode = 0700
exact artifacts = 9/9 strict JSON, regular non-symlink, mode 0600
terminal/manifest reference bytes and hashes = exact
static preflight / production prelaunch / root acquisition = 1/1/1
camera readiness / Ray readiness = pass/pass
Python cleanup / shell cleanup / independent final-zero = fail/fail/fail
first runtime boundary = strip .local ResolveTimeout
RUN / outer dispatch / candidate / capture / CR3 = 0/0/0/0/0
retry / extra probe / alternative root / repair = 0/0/0/0
Human confirmation consumed = false
```

Decision：

```text
REF-P7-23 = REJECTED_BRANCH_D_PRELAUNCH_REACHABILITY_FAILURE
REV-EQ-R6-LIVE-001 = OPEN
failed FAMILY = immutable and permanently non-retryable
Human confirmation = preserved and unconsumed
Advisor decision = not required
next = REF-P7-23-R1
```

Evidence is complete enough to localize the runtime boundary; a pure-offline forensic package would add no decision
value. The minimum next package is one fresh-root, zero-only production prelaunch gate. It may prove hostname/device
reachability and final-zero ownership, but cannot consume its launch handoff or dispatch EQ.
