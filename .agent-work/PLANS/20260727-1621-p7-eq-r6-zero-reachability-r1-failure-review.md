# REF-P7-23-R1 / zero-only hostname reachability gate

**计划状态：** `executable_bounded_zero_only_device_gate`

**Planner 日期：** 2026-07-27

**Reference task ID：** `REF-P7-23-R1`

**Parent reference task：** `REF-P7-23`

**PLAN contract ID：** `P7-TD-B-EQ-R6-ZERO-ONLY-REACHABILITY-R1`

**Package kind：** `bounded_real_zero_only_prelaunch_gate`

**Expected HEAD：** `0f36671a351d537f204e8bc20849ac83e7e57c2b`

`PLAN_MACHINE_CONTRACT={"schema":"planner_execution_contract_v1","contract_id":"P7-TD-B-EQ-R6-ZERO-ONLY-REACHABILITY-R1","reference_task_id":"REF-P7-23-R1","parent_reference_task_id":"REF-P7-23","package_kind":"bounded_real_zero_only_prelaunch_gate","expected_head":"0f36671a351d537f204e8bc20849ac83e7e57c2b","single_current_action":"run_one_fresh_root_production_prelaunch_as_zero_only_reachability_gate_then_stop","human_reauthorization_required":false,"human_eq_confirmation_preserved":true,"human_eq_confirmation_consumed":false,"static_preflight_cap":1,"production_prelaunch_invocation_cap":1,"root_acquisition_cap":1,"retry":0,"extra_hostname_probe":0,"extra_device_probe":0,"extra_cleanup_owner":0,"outer_dispatch_cap":0,"candidate_cap":0,"real_capture_cap":0,"formal_measurement_count":0,"ambient_measurement_count":0,"nonzero_strip_output_cap":0,"eq_launch_authorized":false,"launch_handoff_consumption_authorized":false,"source_edits_authorized":false,"test_edits_authorized":false,"docs_edits_authorized":false,"skill_edits_authorized":false,"wrapper_edits_authorized":false,"config_edits_authorized":false,"commit_authorized":false,"camera_access":"readiness_only","ray_access":"readiness_and_zero_only","strip_access":"zero_and_generation_readback_only","public_analyzer_authorized":false,"strip_stage_authorized":false,"td_c_authorized":false,"planner_stop_required":true}`

**当前唯一动作：** 在一个全新direct-child FAMILY中，单次运行现有production
`--eq-r6-prelaunch` owner，将其严格限定为zero-only hostname/device reachability gate；无论pass或fail，
exact 9 artifacts封口后立即交回Planner。

**唯一 Planner 停止点：** static preflight或production prelaunch任一步失败立即停止；若prelaunch成功，
也必须停止。不得验证或消费launch handoff、创建RUN、打开Terminal、dispatch outer、capture或进入EQ。

## 1. Prior live review

Live activation branch D：

```text
REF-P7-23 = REJECTED_BRANCH_D_PRELAUNCH_REACHABILITY_FAILURE
REV-EQ-R6-LIVE-001 = OPEN
```

Reviewed failure：

```text
failed FAMILY =
  /Volumes/4T/temp/rgbww-optimizer/p7-td-b-exposure-qual-r6-0f36671-20260727T1601
prelaunch terminal SHA-256 =
  f9f106652c32a506772f676175d60d317f3d5137a1891072b9ca448d1ec9bd02
prelaunch manifest SHA-256 =
  1cc926a0b0212fa2c350cf50ad8863ad5c1741b9f3bb25c9694253b273d48dd4
failure =
  strip .local ResolveTimeout; cleanup/final-zero proof unavailable
RUN / dispatch / capture / CR3 =
  0 / 0 / 0 / 0
```

Review archive：

```text
.agent-work/PLANS/20260727-1612-p7-eq-r6-live-prelaunch-failure-review.md
SHA-256 5da3dd47364dd3c1a639cd1a560076a4526b3d38910df21104f3c3c33731a696
```

本轮不需要pure-offline forensic：旧FAMILY已有9/9 strict JSON、exact terminal/manifest refs、truthful stage
failures和zero dispatch/capture accounting。不得修改、repair、重跑或在旧FAMILY补证据。

## 2. Human authorization boundary

本包仅包含：

```text
read-only camera/Ray readiness
strip zero/off command and generation-bearing readback
Python cleanup
shell cleanup
independent final-zero
```

依AGENTS规定，这些readiness与zero/off操作不需要新的Human授权。Executer不得询问Human。

CLI中仍传入：

```text
P7-TD-B-RAY-C-EXPOSURE-QUAL-R6
```

它只是production prelaunch schema冻结的provenance值，不在本zero-only包中授权EQ或表示Human确认已消费。
本包结束时必须仍记录：

```text
human_eq_confirmation_preserved = true
human_eq_confirmation_consumed = false
```

## 3. Frozen source and transition

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

Orchestrator dispatch时必须给Executer exact：

```text
R1_PLAN_SHA256
R1_FULL_SHA256
R1_EXECUTION_RESULT_START_SHA256
```

PLAN不能自嵌自身hash。缺一、格式错误或当前path/hash不符即stop，不得从旧handoff推导。

## 4. Fresh unique root

只允许：

```text
FAMILY =
  /Volumes/4T/temp/rgbww-optimizer/p7-td-b-eq-r6-zero-reachability-0f36671-20260727T1612
PRELAUNCH =
  ${FAMILY}/prelaunch
RUN =
  ${FAMILY}/run
SAFE_PARENT =
  /Volumes/4T/temp/rgbww-optimizer
```

开始时FAMILY/PRELAUNCH/RUN必须absent且non-symlink。SAFE_PARENT必须是existing directory、
non-symlink。production prelaunch是唯一FAMILY/PRELAUNCH acquisition owner。

禁止：

```text
reuse failed 1601 FAMILY
precreate FAMILY or PRELAUNCH
alternative root
same-root repair
delete and retry
RUN creation
```

## 5. One static preflight

只允许运行一次local read/hash/stat preflight，确认：

```text
HEAD / parent / subject = exact
PLAN/FULL/EXECUTION_RESULT start hashes = Orchestrator handoff
第3节source hashes = exact
review archive hash = exact
failed 1601 PRELAUNCH remains exact 9 JSON
failed terminal/manifest hashes = exact
failed RUN remains absent
SAFE_PARENT is safe
new FAMILY/PRELAUNCH/RUN absent
repository .env is regular non-symlink if present
```

`.env`只可`lstat`，不得读取、打印、hash、复制或序列化。

本static preflight不得调用：

```text
DNS / ping / HTTP / hostname resolution
camera / Ray / strip
all_off / cleanup / final-zero
```

preflight cap=1。任一失败立即stop；不得改path后再试。

## 6. One production zero-only owner

Static preflight通过后，从repo root逐字运行一次：

```zsh
.venv/bin/python -m camera_based_rgbww_optimizer.optimization.measure_p7_thermal_diagnostics \
  --execute \
  --allow-device-control \
  --eq-r6-prelaunch \
  --experiment-id p7_td_b_command_switch_history_v1 \
  --source ray \
  --phase formal \
  --output-dir /Volumes/4T/temp/rgbww-optimizer/p7-td-b-eq-r6-zero-reachability-0f36671-20260727T1612 \
  --run-name prelaunch \
  --code-checkpoint 0f36671a351d537f204e8bc20849ac83e7e57c2b \
  --human-authorization P7-TD-B-RAY-C-EXPOSURE-QUAL-R6 \
  --camera-backend remote
```

这是唯一real owner invocation，也是唯一hostname/device attempt owner。虽然production entrypoint名为
prelaunch，本PLAN将其pass handoff明确降格为non-authorizing evidence。

Exact caps：

```text
static preflight = 1
production prelaunch invocation = 1
FAMILY/PRELAUNCH root acquisition = 1
camera readiness owner = 1
Ray readiness owner = 1
Python cleanup owner = 1
shell cleanup owner = 1
independent final-zero owner = 1
extra DNS/ping/HTTP probe = 0
extra device probe = 0
extra cleanup/final-zero = 0
retry/relaunch/alternative root/repair = 0/0/0/0
```

## 7. Zero-only boundary

本包允许的device effects只有：

```text
camera readiness/config/capability read
Ray readiness/readback and zero/off cleanup
strip zero/off only
generation-bearing strip zero readback
```

必须保持：

```text
capture / CR3 / NPY / TIFF = 0
formal / ambient measurement = 0 / 0
nonzero strip output = 0
EQ outer dispatch / Terminal / RUN = 0 / 0 / 0
candidate 1 / candidate 2 = 0 / 0
public analyzer / strip stage / TD-C = 0 / 0 / 0
firmware / deployment / destructive operation = 0
source/test/docs/skill/wrapper/config edit = 0
commit = 0
```

Executer不得在production owner前后另跑`ping`、`dig`、`curl`、ESPhome CLI、all_off或任何“确认一下”
命令。production owner本身就是唯一reachability与zero-proof attempt。

## 8. Exact progressive and terminal evidence

PRELAUNCH必须最终包含exact 9：

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

Required：

```text
PRELAUNCH mode = 0700
files mode = 0600
regular non-symlink, resolved within PRELAUNCH
strict sorted JSON, allow_nan=false, single trailing newline
exact names/order/count = 9
terminal references first 7 artifacts by exact path/bytes/hash/mode
manifest references first 8 artifacts by exact path/bytes/hash/mode
tmp artifacts = 0
call_count = 1
dispatch_count = 0
run_root_created = false
```

Pass requires：

```text
camera readiness = pass
Ray readiness = pass
Python cleanup = pass
shell cleanup = pass
independent final-zero = pass
strip_verified_off = true with generation-bearing evidence
ray_verified_off = true
terminal.status = pass
manifest.status = pass
```

Failure仍必须尽可能完成all-path cleanup与terminal/manifest fail seal。任何failure后不得补probe、补cleanup、
repair artifacts或重跑。

## 9. Mandatory stop on both branches

### Pass

若exact zero-only gate通过：

```text
REF-P7-23-R1 = READY_FOR_PLANNER_REVIEW_ZERO_REACHABILITY_PROVED
REV-EQ-R6-LIVE-001 remains open until a later activation succeeds
launch_handoff = evidence only, non-authorizing, not consumed
Human EQ confirmation = preserved and unconsumed
```

必须停止。不得做handoff freshness validation、不得启动Terminal、不得创建RUN或dispatch EQ。后续是否开
fresh live activation由Planner在新PLAN中决定。

### Fail

若任一readiness、cleanup、final-zero、artifact或owner boundary失败：

```text
REF-P7-23-R1 = REJECTED_WITH_EXACT_FAILURE_EVIDENCE
```

保留FAMILY并停止。不得retry、换root、补device probe或自动进入offline correction。Planner根据证据决定
网络环境等待、实现纠偏或新的bounded package。

## 10. Post-terminal read-only audit

Owner退出后只允许一次filesystem/process read-only audit：

```text
strict JSON = 9/9
names/order/modes/containment = exact
terminal/manifest references = exact
stage attempts/call counts/statuses = truthful
RUN/dispatch/candidate/capture/CR3/nonzero = 0
retry/extra probe/extra cleanup = 0
failed 1601 FAMILY unchanged
HEAD/source hashes unchanged
owned residual processes = 0
Human confirmation consumed = false
```

不得通过device/network call完成audit。

Executer向`.agent-work/EXECUTION_RESULT.md`追加exact command、exit、root、artifact bytes/hashes、stage
attempt/status/exception type、side-effect accounting、post-terminal audit及Planner decision request。
不得修改PLAN/FULL。

## 11. 维护性判断

本包不新增代码或并行device owner；复用已经回归覆盖并能all-path seal的production prelaunch owner，
仅把其权限收窄为zero-only gate。失败证据已闭合，因此跳过无价值的offline forensic；无需Advisor或Human
action，也无需架构重构。

---

## 12. Planner review（2026-07-27 16:21 MDT）

Reviewed：

```text
PLAN SHA-256 =
  81632215c0d7c964ac14667c8188acd3cb8722e055840734e40a861adb48e98e
EXECUTION_RESULT SHA-256 =
  39e13202a4cb83d646337077cff493a93d4c17a6b741082eddec30e211fa2e67
Orchestrator FULL SHA-256 =
  68b7dcd32f496964272dec31cf92967c18cf8d72452851c0f683eeb37428db06
HEAD =
  0f36671a351d537f204e8bc20849ac83e7e57c2b
```

R1 evidence：

```text
FAMILY =
  /Volumes/4T/temp/rgbww-optimizer/p7-td-b-eq-r6-zero-reachability-0f36671-20260727T1612
prelaunch terminal SHA-256 =
  e20c438678f4b959cdf73c484856c504d1b8063dec28f095a1f8ad90aa710525
prelaunch manifest SHA-256 =
  4d30c04f42fa957e25ba640fabbd99e32536ddfcf8981579e0e3fccf18a7ab65
```

Planner independently confirmed：

```text
exact artifacts = 9/9 strict JSON, mode 0600, PRELAUNCH mode 0700
terminal/manifest references = exact
static preflight / production owner / root acquisition = 1/1/1
camera/Ray readiness = pass/pass
strip .local resolution = ResolveTimeout
Python cleanup / shell cleanup / independent final-zero = fail/fail/fail
RUN / residual / capture / dispatch / EQ = 0/0/0/0/0
extra probes / retry / repair / alternate root = 0/0/0/0
failed 1601 evidence = unchanged
Human EQ confirmation consumed = false
```

Decision：

```text
REF-P7-23-R1 = REJECTED_REPEATED_HOSTNAME_RESOLUTION_FAILURE
REV-EQ-R6-LIVE-001 = BLOCKED_ON_HUMAN_ENVIRONMENT_CHECKPOINT
fresh device attempt count in this failure family = 2
third attempt = not authorized
pure-offline code correction = not selected
Advisor decision = not required
next = REF-P7-23-H1
```

The code already exposes `CAMERA_BASED_RGBWW_OPTIMIZER_ESPHOME_HOST` and keeps
`expected_name=bedroom-rgbww-strip`; an explicit address does not require a new owner or code change. The missing fact
is a current, Human-owned address source or same-stack mDNS proof. Historical ping output is insufficient, and the
Planner will not freeze `192.168.0.74` merely because it appeared in that historical output.
