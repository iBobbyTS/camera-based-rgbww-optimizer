# Archive metadata

- archive_status: `HISTORICAL_NON_EXECUTABLE_REVIEWED_REJECTED_PRE_ROOT_CALLER_TRANSCRIPTION`
- archived_at: `2026-08-03T12:49:56-06:00`
- source_owner: `Executer`
- source_type: `EXECUTION_RESULT`
- reviewed_scope: `REF-G4-02-PREDEVICE / zero-edit validation and first durable call input`
- source_checkpoint: `79b8f03e65107e1d62f8de3b33ffb31d3413e185`
- original_body_bytes: `5901`
- original_body_sha256: `bea5eb5e277942834a48a1811b736d4287039b8c5f4477a0aa07665cc897c8e6`
- terminal_disposition: `REJECTED_PRE_ROOT_THIN_CALLER_NAME_TRANSCRIPTION_PRODUCTION_AND_VALIDATION_ACCEPTED`
- reviewed_plan_pointer: `.agent-work/archived/PLAN-20260803-1249.md`
- exact_next_stop: `SAME_REF_G4_02_REPO_OWNED_ARTIFACT_NAME_DERIVATION_SINGLE_PACKAGE_ATTEMPT`
- historical_non_executable: `true`

该archive不授权execution、durable root、release consumption、device、formal、retry、stage entry、budget或commit。下方逐字节
保留reviewed ER body。

---

# REF-G4-02-PREDEVICE：durable offline oracle V2 execution handoff

**状态：** `STOPPED_PRE_ROOT_INPUT_CONTRACT_FAILURE_WAITING_PLANNER_REVIEW`

**PLAN contract：** `G4-PREDEVICE-DURABLE-OFFLINE-ORACLE-ZERO-EDIT-VALIDATION-CONTINUATION-V2`

**Reference task：** `REF-G4-02-PREDEVICE`

**Planner stop：** `RETURN_FOR_G4_02_DURABLE_OFFLINE_ORACLE_REVIEW`

## 1. 结论

V2 的全部 fresh pre-real gates 通过，冻结的 production/test bytes 与 SHA-256 未漂移。随后唯一一次
production persist owner 调用在创建 durable root 之前 fail-closed：

```text
camera_based_rgbww_optimizer.optimization.p7_successor_predevice.SuccessorPredeviceError:
artifact_expectation_invalid
```

失败发生在 `persist_successor_predevice_evidence()` 内部 evaluator 的 `_validate_expectation()`；尚未调用
`read_existing_root`，尚未读取 successor release payload，尚未创建 durable root。依 single-call、zero-edit、
no-retry contract，Executer没有修正参数、没有再次调用 persist owner、没有调用 replay owner，也没有编辑
production/test。

建议 failure classification：

`REAL_CALL_INPUT_ARTIFACT_NAME_TRANSCRIPTION_DRIFT_PRE_ROOT`

这不是 canonical validator、release、设备或科学实验失败；是否允许下一包修正 exact caller input 由 Planner/
Orchestrator 判断。

## 2. V2 intake

- PLAN/FULL machine parser：PASS。
- PLAN/FULL active task：`REF-G4-02-PREDEVICE`，count `1/1`。
- PLAN/FULL contract：
  `G4-PREDEVICE-DURABLE-OFFLINE-ORACLE-ZERO-EDIT-VALIDATION-CONTINUATION-V2`。
- dirty path set：与冻结的 7 paths exact 一致。
- durable root pre-call：`os.path.lexists(...) = false`。
- archive identities：

```text
.agent-work/archived/PLAN-20260803-1236.md
  17892 bytes / 78a2c599ad31f36e2370064c40d2374538d2efd8f76d448512f61813b2428612
  body: 16889 bytes / 791f6ffb92ba61a7241b726042aa4e50568a3cce9d4ca8f555d41d5e0443cc82
.agent-work/archived/EXECUTION_RESULT-20260803-1236.md
  6522 bytes / 91c6d83f36aa8d0606a34e98be13de066aea7afd9cc1d6ec24f137f182ce6275
  body: 5516 bytes / 04e1278aea64ab75202484116687e2e11fa1b6d0d921a263fd3440172987adc2
```

## 3. 冻结 code/test identity

执行前与所有 pre-real gates 通过后均为：

```text
src/camera_based_rgbww_optimizer/optimization/p7_successor_predevice.py
  24232 bytes
  4c8bf96dca444b5412120534a1df5519976afc98fe4aa1aaf2b83596177ffc81
tests/test_p7_successor_predevice.py
  29738 bytes
  44ac81ae18ae0a8f041d53837c4c7d6c4e867cf4761c616bfb640117550d4cfa
```

本 V2 code/test edit count：`0`。

## 4. Fresh validation ledger

按 PLAN 顺序执行：

1. targeted：`18/18 PASS`，exit `0`。
2. focused（predevice + successor lineage + retained provenance I/O + TD-B R6 contract）：
   `133/133 PASS`，exit `0`。
3. full suite：`864/864 PASS`，`146.475s`，exit `0`。
4. `python -m compileall -q src tests`：exit `0`。
5. `codegraph sync`：exit `0`，`Synced 2 changed files`。
6. `codegraph explore "p7_successor_predevice durable persistence replay ownership call paths"`：
   exit `0`；确认 durable owner 继续组合 repo-owned provenance root/persist/read/inventory/same-target
   owners，没有平行 filesystem/serialization owner。
7. `git diff --check`：exit `0`。

## 5. 唯一 real-owner 调用与精确失败

Frozen output root：

```text
/Volumes/4T/temp/rgbww-optimizer/g4-predevice-oracle-125158a3c1b8-20260803T181631Z
```

调用计数：

```text
persist_successor_predevice_evidence calls = 1
evaluate_successor_predevice entries = 1
successor release root reads = 0
durable root creation calls = 0
durable artifact persist calls = 0
replay_successor_predevice_evidence calls = 0
release consumption = 0
device/camera/Ray/strip/capture/formal/TD-C calls = 0
```

传入的 artifact names：

```text
frozen-inputs.json
ray-r6-plan.json
lineage-descriptor.json
validation-summary.json
terminal-seal.json
```

repo-owned `p7_successor_lineage.ARTIFACT_NAMES`：

```text
frozen-inputs.json
r6-formal-plan.json
release-descriptor.json
validation-summary.json
terminal-seal.json
```

因此 exact tuple guard 在任何 root read/create 之前拒绝第二、第三项名称漂移。异常 traceback 的最终 owner
链为：

```text
persist_successor_predevice_evidence
  -> evaluate_successor_predevice
    -> _validate_expectation
      -> SuccessorPredeviceError("artifact_expectation_invalid")
```

## 6. Post-failure seal

只读 existence 检查：

```text
DURABLE_ROOT_LEXISTS=0
```

所以没有不完整 root、result、terminal seal 或需要修复/清理的 payload。Executer未遍历 EQ root，未读取
external experiment payload，未访问 retained R3，未执行设备、网络、相机、Ray、灯带、release
consumption、formal R6 或 TD-C。

## 7. Authority ledger

```text
canonical_validator_success = false
eligibility = false
release_consumable = false
release_consumption_authorized = false
retained_r3_status = RETAINED_UNVALIDATED_UNCONSUMED
device_authorized = false
camera_authorized = false
ray_authorized = false
strip_authorized = false
capture_authorized = false
formal_r6_authorized = false
td_c_authorized = false
```

没有 durable package，因此没有 proposal state 可供 Planner 接受。所有 effective authority 保持 false。

## 8. Planner decision request

请 Planner 对以下问题作唯一 review：

1. 接受 V2 pre-real validation 与 frozen code/test identities；
2. 将本次失败归类为 pre-root thin-caller artifact-name transcription drift，而不是 production defect；
3. 决定是否归档本 PLAN 并返回一个只修正 exact input names、仍保持 code/test zero-edit、fresh-root、
   single-call/no-retry 的 bounded continuation；
4. 不得在本 handoff 上授予 eligibility、release consumption、设备或 formal 权限。

Executer已到达唯一 Planner stop，不会自行重试或创建后继 task。
