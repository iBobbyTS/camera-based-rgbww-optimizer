# REF-P7-23-R2 / post-H1 zero-only recovery gate

**计划状态：** `executable_bounded_zero_only_recovery`

**Planner 日期：** 2026-07-27

**Reference task ID：** `REF-P7-23-R2`

**Parent reference task：** `REF-P7-23`

**PLAN contract ID：** `P7-TD-B-EQ-R6-POST-H1-ZERO-RECOVERY-R2`

**Package kind：** `bounded_real_zero_only_production_prelaunch`

**Expected HEAD：** `0f36671a351d537f204e8bc20849ac83e7e57c2b`

`PLAN_MACHINE_CONTRACT={"schema":"planner_execution_contract_v1","contract_id":"P7-TD-B-EQ-R6-POST-H1-ZERO-RECOVERY-R2","reference_task_id":"REF-P7-23-R2","parent_reference_task_id":"REF-P7-23","package_kind":"bounded_real_zero_only_production_prelaunch","expected_head":"0f36671a351d537f204e8bc20849ac83e7e57c2b","single_current_action":"run_one_fresh_root_production_prelaunch_as_post_h1_zero_only_recovery_then_stop","human_action_required":false,"human_reauthorization_required":false,"human_eq_confirmation_preserved":true,"human_eq_confirmation_consumed":false,"static_preflight_cap":1,"production_prelaunch_invocation_cap":1,"root_acquisition_cap":1,"retry":0,"extra_resolver_probe":0,"extra_device_probe":0,"extra_cleanup_owner":0,"outer_dispatch_cap":0,"candidate_cap":0,"real_capture_cap":0,"formal_measurement_count":0,"ambient_measurement_count":0,"nonzero_strip_output_cap":0,"eq_launch_authorized":false,"launch_handoff_consumption_authorized":false,"source_edits_authorized":false,"test_edits_authorized":false,"docs_edits_authorized":false,"skill_edits_authorized":false,"wrapper_edits_authorized":false,"config_edits_authorized":false,"commit_authorized":false,"camera_access":"readiness_only","ray_access":"readiness_and_zero_only","strip_access":"zero_and_generation_readback_only","public_analyzer_authorized":false,"strip_stage_authorized":false,"td_c_authorized":false,"planner_stop_required":true}`

**当前唯一动作：** H1已证明project `.venv` same-stack resolver返回non-empty rows；现在在全新FAMILY中只
运行一次production `--eq-r6-prelaunch`，取得strip generation-bearing zero及完整cleanup/final-zero seal，
然后无论pass/fail都停回Planner。

**唯一 Planner 停止点：** static preflight或production owner任一步失败立即停止；production prelaunch
pass也立即停止。不得消费launch handoff、创建RUN、启动Terminal/outer、capture或进入EQ。

## 1. H1 acceptance

```text
REF-P7-23-H1 = ACCEPTED_CORE_ENVIRONMENT_FACT
same-stack async_resolve_host returned non-empty rows = proven
H1 formatter TypeError = Planner command bug after resolver return
Human repeat probe = not required
REV-EQ-R6-LIVE-001 = READY_FOR_ZERO_ONLY_RECOVERY_GATE
```

H1 review archive：

```text
.agent-work/PLANS/20260727-1642-p7-eq-r6-human-resolver-checkpoint-review.md
SHA-256 ef33c26359647db168c1a866e451ad68e0d68757af0032dc445c6ada0dbe81cb
```

Persistent debug note：

```text
.agent-work/debug/active/20260725-p7-td-b-e2-r1-hostname-and-progressive-evidence.md
SHA-256 e0e412f4cf4e16243db5dbb0d70091d8119b96bb6de76e79db807bc470495bf1
```

H1只恢复了当前same-stack resolution事实，没有证明strip generation-bearing zero。因此本包不直接恢复
live EQ。

## 2. Authorization

本包仅允许readiness与zero/off：

```text
camera readiness
Ray readiness/readback at zero
strip zero/off plus generation-bearing state readback
Python cleanup
shell cleanup
independent final-zero
```

这些操作依AGENTS不需要新的Human授权。Executer不得再询问Human。

CLI仍传入existing provenance：

```text
P7-TD-B-RAY-C-EXPOSURE-QUAL-R6
```

它不在本包授权EQ，也不会被本zero-only gate消费：

```text
human_eq_confirmation_preserved = true
human_eq_confirmation_consumed = false
```

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

Orchestrator正式dispatch时给出：

```text
R2_PLAN_SHA256
R2_FULL_SHA256
R2_EXECUTION_RESULT_START_SHA256
```

缺一或current path/hash不符立即stop；Executer不得推导或补值。

## 4. Fresh unique root

```text
SAFE_PARENT =
  /Volumes/4T/temp/rgbww-optimizer
FAMILY =
  /Volumes/4T/temp/rgbww-optimizer/p7-td-b-eq-r6-zero-recovery-0f36671-20260727T1642
PRELAUNCH =
  ${FAMILY}/prelaunch
RUN =
  ${FAMILY}/run
```

开始时FAMILY/PRELAUNCH/RUN必须absent且non-symlink；SAFE_PARENT必须是existing safe directory。
Production prelaunch是唯一FAMILY/PRELAUNCH owner。

旧FAMILY：

```text
/Volumes/4T/temp/rgbww-optimizer/p7-td-b-exposure-qual-r6-0f36671-20260727T1601
/Volumes/4T/temp/rgbww-optimizer/p7-td-b-eq-r6-zero-reachability-0f36671-20260727T1612
```

必须只读且before/after terminal/manifest hashes不变。不得复用、repair、删除或写入。

## 5. One local static preflight

只允许一次read/hash/stat preflight：

```text
HEAD / parent / subject = exact
PLAN/FULL/EXECUTION_RESULT start = Orchestrator handoff hashes
第3节source hashes = exact
H1 archive/debug hashes = exact
旧1601与1612 terminal/manifest hashes = exact
旧RUN = absent
SAFE_PARENT = safe
new FAMILY/PRELAUNCH/RUN = absent/non-symlink
repository .env = regular non-symlink if present
```

不得读取/打印/hash `.env`内容。Static preflight不得做DNS、resolver、ping、HTTP、camera、Ray、strip或cleanup
call。cap=1；失败即stop。

## 6. One production recovery owner

Static preflight通过后，从repo root逐字运行一次：

```zsh
.venv/bin/python -m camera_based_rgbww_optimizer.optimization.measure_p7_thermal_diagnostics \
  --execute \
  --allow-device-control \
  --eq-r6-prelaunch \
  --experiment-id p7_td_b_command_switch_history_v1 \
  --source ray \
  --phase formal \
  --output-dir /Volumes/4T/temp/rgbww-optimizer/p7-td-b-eq-r6-zero-recovery-0f36671-20260727T1642 \
  --run-name prelaunch \
  --code-checkpoint 0f36671a351d537f204e8bc20849ac83e7e57c2b \
  --human-authorization P7-TD-B-RAY-C-EXPOSURE-QUAL-R6 \
  --camera-backend remote
```

不设置`CAMERA_BASED_RGBWW_OPTIMIZER_ESPHOME_HOST` override；本包使用H1已验证恢复的
`bedroom-rgbww-strip.local` production path。

Exact caps：

```text
static preflight = 1
production owner = 1
root acquisition = 1
camera readiness = 1 owner sequence
Ray readiness = 1
Python cleanup = 1
shell cleanup = 1
independent final-zero = 1
extra resolver/ping/HTTP/device probe = 0
extra cleanup = 0
retry/relaunch/alternate root/repair = 0
```

## 7. Zero-only execution boundary

允许：

```text
camera remote-v2 readiness/config read
Ray readiness and zero/off cleanup
strip zero/off only
strip exact expected name/state object and generation-bearing readback
```

必须保持：

```text
capture / CR3 / NPY / TIFF = 0
formal / ambient measurement = 0 / 0
nonzero strip output = 0
RUN / Terminal / outer dispatch = 0 / 0 / 0
candidate 1 / candidate 2 = 0 / 0
public analyzer / strip stage / TD-C = 0 / 0 / 0
firmware / deployment / destructive operation = 0
source/test/docs/skill/wrapper/config edit = 0
commit = 0
```

## 8. Exact evidence and pass criteria

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

Required：

```text
PRELAUNCH mode = 0700
files mode = 0600
regular non-symlink and contained
strict sorted JSON and exact count/order
terminal first-7 references = exact
manifest first-8 references = exact
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
strip_verified_off = true
strip evidence has expected name bedroom-rgbww-strip
strip evidence has state object rgbww_commanded_state
strip evidence has generation-bearing all-zero readback
ray_verified_off = true
terminal.status = pass
manifest.status = pass
```

任何failure都必须all-path attempt并seal fail；不得补probe、补cleanup、repair或retry。

## 9. Both branches stop

### Pass

```text
REF-P7-23-R2 = READY_FOR_PLANNER_REVIEW_ZERO_RECOVERY_PROVED
REV-EQ-R6-LIVE-001 = may be reconsidered only by next Planner review
launch_handoff = non-authorizing evidence only
Human EQ confirmation = preserved/unconsumed
```

立即stop。不得验证/消费handoff、创建RUN、打开Terminal或dispatch EQ。

### Fail

```text
REF-P7-23-R2 = REJECTED_WITH_FRESH_POST_H1_FAILURE_EVIDENCE
```

立即stop。不得自动第四次attempt、IP fallback、extra probe或code correction。

## 10. Post-terminal audit

Owner退出后只允许一次filesystem/process read-only audit：

```text
strict JSON = 9/9
names/order/modes/containment = exact
terminal/manifest refs = exact
stage attempt/call/status = truthful
RUN/dispatch/candidate/capture/CR3/nonzero = 0
retry/extra probe/extra cleanup = 0
old 1601/1612 evidence unchanged
HEAD/source hashes unchanged
owned residual processes = 0
Human confirmation consumed = false
```

不得通过network/device call完成audit。Executer追加完整evidence与Planner decision request到
`.agent-work/EXECUTION_RESULT.md`，不修改PLAN/FULL。

## 11. 维护性判断

H1 formatter bug仅影响Human命令输出，不触及production code。R2继续复用唯一production prelaunch owner，
把恢复验证限制为zero-only generation-bearing evidence；不新增resolver fallback、硬编码IP或平行cleanup owner。
无需Human再次操作、无需Advisor或架构重构。

---

## 12. Planner review（2026-07-27 16:50 MDT）

Reviewed：

```text
PLAN SHA-256 =
  a88137e02948f031732742d5e0c68d838f0a9d1fb02caf539b4f6679d697699f
EXECUTION_RESULT SHA-256 =
  7154b3a72911c362e03696b22a0a08945c8986751f856e12bf49a88b81732cda
Orchestrator FULL SHA-256 =
  297127a46c06dca52d9e755fcd3a81d1ac4348f7a475bb83ebf5bf5b910e4667
HEAD =
  0f36671a351d537f204e8bc20849ac83e7e57c2b
```

Evidence：

```text
FAMILY =
  /Volumes/4T/temp/rgbww-optimizer/p7-td-b-eq-r6-zero-recovery-0f36671-20260727T1642
terminal SHA-256 =
  808056f62ef9af114736e2263cdb2996e4c6c908b757913e7fec8b310d27bf6c
manifest SHA-256 =
  3353fa3dd3cda4ea6706ccf42aaf47ff75e5c692aadd58505ded105ebe25eefa
```

Planner independently confirmed：

```text
exact artifacts = 9/9 strict JSON, mode 0600, PRELAUNCH mode 0700
terminal/manifest refs = exact
static / production / root acquisition = 1/1/1
camera / Ray / Python / shell / final-zero = pass/pass/pass/pass/pass
strip generation strictly advanced and five channels zero
Ray intensity zero and validate_both_off pass
host override / extra resolver / retry = 0/0/0
RUN / dispatch / capture / nonzero / EQ = 0/0/0/0/0
handoff consumed = false
Human EQ confirmation consumed = false
```

Decision：

```text
REF-P7-23-R2 = ACCEPTED_ZERO_RECOVERY_PROVED
REV-EQ-R6-LIVE-001 = CLOSED
hostname debug record = RESOLVED
R2 launch handoff = permanently non-authorizing and non-consumable across PLAN
Human EQ confirmation = valid, preserved and unconsumed
Advisor decision = not required
next = REF-P7-23
```

The next live activation must acquire a new unique FAMILY and repeat production prelaunch inside the same active PLAN.
Only that fresh handoff may be validated within 600 seconds and consumed by one visible-Terminal outer dispatch.
