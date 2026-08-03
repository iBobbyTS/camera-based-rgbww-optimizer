# Archive metadata

- archive_status: `HISTORICAL_NON_EXECUTABLE_REVIEWED_REJECTED_G4_04_E2_OPEN_RESULT_REPLAY_CONTRACT_EVIDENCE`
- archived_at: `2026-08-03T15:14:34-06:00`
- source_owner: `Executer`
- source_type: `EXECUTION_RESULT`
- reviewed_scope: `REF-G4-04-E2 / offline owner, tests, package identities and replay claim`
- source_checkpoint: `cda4f63b3428dc7c1e77510cebd7cb68a4a10a47`
- original_body_bytes: `7488`
- original_body_sha256: `0d5638d6c97e5f6cd3a7bfa6b807148ab477d757ec3070edf1cc55db1d43d6fc`
- terminal_disposition: `REJECTED_G4_04_E2_ACCEPTANCE_OPEN_RESULT_PERSISTENCE_AND_REPLAY_CONTRACT`
- reviewed_plan_pointer: `.agent-work/archived/PLAN-20260803-1514.md`
- exact_next_stop: `RETURN_ORCHESTRATOR_BOUNDED_SAME_REFERENCE_OFFLINE_RESULT_REPLAY_CLOSURE`
- historical_non_executable: `true`

该archive保留Executer的test/check与two-artifact package identity声明，但不接受其PASS结论。Planner未读取package root；
recorded identity不能弥补repo-owned replay的open-result绕过。本archive不授权root repair、alternate root、G4-05/06、device、
release、formal、retry、commit或后继PLAN。下方逐字节保留reviewed EXECUTION_RESULT body。

---

# REF-G4-04-E2：Executer handoff

**候选状态：** `G4_04_E2_ACCEPTANCE_CANDIDATE_OFFLINE_PREFORMAL_CONTRACT_PASS`

**PLAN contract：** `G4-E2-PREFORMAL-OFFLINE-INTEGRATION-V1`

**Reference task：** `REF-G4-04-E2`

**Planner stop：** `RETURN_FOR_G4_04_E2_PREFORMAL_GATE_REVIEW`

本handoff只报告offline engineering candidate；不宣称formal PASS、hardware ready、release consumed、G4-05 execution
authorization或G4-06 unlock。等待Planner独立review。

## 1. Activation topology与intake

- activation HEAD：`cda4f63b3428dc7c1e77510cebd7cb68a4a10a47`
- direct parent：`4995f7d65141ce8a4086d74f9add21c5b44d593d`
- activation tree：`37efc5893457a04705b07da51550d52ae2c3dfe6`
- subject：`docs(plan): activate g4 e2 preformal gate`
- exact activation changed paths：
  - `.agent-work/EXECUTION_RESULT.md`
  - `.agent-work/FULL_PLAN_REFERENCE.md`
  - `.agent-work/PLAN.md`
- branch：`main`
- intake时worktree clean；PLAN/FULL strict parser均为active task `REF-G4-04-E2`、active count `1`，canonical next一致；
  G4-05 execution false，G4-06 locked。
- exact E2 root在执行前不存在。
- 未读取任何G4-01/02/03 external root或payload；仅消费PLAN machine row中冻结的reference ledger。

## 2. Changed source/test identity

| Path | Before | After bytes | After SHA-256 |
|---|---:|---:|---|
| `src/camera_based_rgbww_optimizer/optimization/p7_successor_e2.py` | absent | 24222 | `20bd2ca3fe1bbf2931b7f2605c307ed00fe8c0848734e68edbe35600ba8c4fed` |
| `tests/test_p7_successor_e2.py` | absent | 16170 | `354f61e34ba714895f0fcd2b0ac50ef654ed8f685174f6ef76a1719d08c3ec1d` |

既有production owners、tests、config、wrapper、GUIDE/RESEARCH、PLAN/FULL及archives未由Executer修改。

## 3. Frozen prerequisite reference ledger

- source checkpoint/tree：
  `4995f7d65141ce8a4086d74f9add21c5b44d593d` /
  `da458ce4a81344397354a8535e8a38cef5d59375`
- GUIDE：`advisor/4/4.GUIDE.md`, bytes `22702`, SHA-256
  `659152f6c0ae69c90c701de4e57c352d771e4f0bf75cf9410271ba0a94200e35`
- exposure policy：`config/hsi/p7-ray-td-b-exposure-policy-v2.json`, bytes `4065`, SHA-256
  `c9080d18571f617cb7d323ade843ff9c86bf92e3795d23e3999e26d413968681`, status `qualified_1_2500`
- G4-01 accepted/unconsumed reference：five exact artifacts
  `frozen-inputs.json` 5047/`8a81a906...e0264f8`,
  `r6-formal-plan.json` 899/`dea5f979...72cc3b`,
  `release-descriptor.json` 2024/`6843ef50...bb452`,
  `validation-summary.json` 432/`07e83161...1cc07`,
  `terminal-seal.json` 808/`d9d7b784...68850`；validator success/eligible/consumable均true，consumption authorization false。
- G4-02 accepted reference：
  `predevice-oracle-result.json` 3186/`78fa982b...40d9`,
  `terminal-seal.json` 1114/`39456ca3...68e`。
- G4-03 accepted reference：terminal 2936/`c6fc7b2a...a39d`；review PLAN/ER archive、owner/test/wrapper exact identities按PLAN冻结；
  classification `REQUEST_TRANSPORT_AMBIGUOUS_EFFECT_CONFIRMED_CLEAN`，transport success false，exit `1`，error `-128`，residual `0`。
- protected formal plan/runner/analyzer/lineage/predevice/provenance/wrapper的七项identity均逐项冻结并由input exact equality保护。
- retained R3：`RETAINED_UNVALIDATED_UNCONSUMED`；release consumption、device、formal R6、TD-C authority均false。

省略号只用于本段的人类可读摘要；repo-owned frozen input中保存了PLAN machine row的完整64位SHA、bytes、顺序和路径，测试逐类篡改
name/bytes/SHA/order/count并验证fail closed。

## 4. Existing owner调用与contract结果

- `build_td_b_r6_formal_plan`：每次evaluator恰好调用 `1` 次。
- `validate_td_b_r6_formal_plan`：每次evaluator恰好调用 `1` 次。
- `td_b_r6_machine_status`：每次evaluator恰好调用 `1` 次。
- 唯一durable evaluation：`1` 次；root creation：`1` 次；persist package：`1` 次；independent replay：`1` 次。
- formal plan保持non-executable Ray-only `000..015`；A/D/B/C shutter为
  `1/5000`、`1/6400`、`1/8000`、`1/2500`；logical/physical `16/16`；ambient/setup `0/0`；launch/retry `1/0`；
  pooling prohibited；failure contract为accepted hard-failed formal attempt、formal false、strip call `0`、retry `0`。
- machine status保持600秒selected transient、steady未证明；strip/TD-C/sentinel/P8 locks不变。
- result为deep immutable canonical-JSON projection，status仅为
  `offline_preformal_contract_pass_waiting_planner_review`，所有execution/formal/hardware/release/downstream authority均false/0。

## 5. Tests与checks

| Check | Invocation | Result |
|---|---:|---|
| targeted `tests.test_p7_successor_e2` | 1/2 cap | `13/13 PASS`，首次通过，无bounded correction |
| focused successor/lineage/predevice/zero-readiness/R6/thermal/provenance | 1/1 cap | `245/245 PASS` |
| full `unittest discover -s tests` | 1/1 cap | `892/892 PASS` in 159.653s |
| `compileall -q src tests` | 1/1 cap | PASS |
| `zsh -n tmp/run-p7-thermal-diagnostics.zsh` | 1/1 cap | PASS |
| `git diff --check` before package | 1 | PASS |
| repo-owned source scan | 1 | PASS，2 paths，0 findings，0 private/env/network/symlink issue |
| `codegraph sync` | 1/1 cap | PASS，2 added files / 92 nodes |
| CodeGraph ownership query | 1 | PASS；新owner组合existing thermal/provenance owners；无device/network/process/controller边 |

Negative cases覆盖：全部prerequisite identity mutation，source/policy/protected identity drift，transport/effect drift，formal plan各字段、
machine envelope/locks、invalid/bool-as-int/mutable/open/duplicate/nonabsolute，non-executable runner在fake backend connect/config/capture前拒绝，
result/terminal persist failure单一fail seal，inventory drift与AST boundary。

## 6. Durable E2 package

- root：`/Volumes/4T/temp/rgbww-optimizer/g4-e2-preformal-4995f7d65141-20260803T204648Z`
- root identity：device `16777244`, inode `2516637`, mode `0700`
- `preformal-gate-result.json`：device `16777244`, inode `2516638`, mode `0600`, bytes `5880`, SHA-256
  `4352e9b007d443922a7612acfbbe1015d1312ccc09f203a969abe3d816b5284e`
- `terminal-seal.json`：device `16777244`, inode `2516639`, mode `0600`, bytes `473`, external SHA-256
  `1a79f3fd16fe85bd663e301d9abfb6faacff9651bfd9ed027fc04084173e805f`
- inventory：exactly `preformal-gate-result.json`, `terminal-seal.json`
- terminal：non-self-referential，artifact count before terminal `1`，retry `0`，alternate root `0`
- replay：schema `g4_e2_preformal_replay_v1`，status `pass`，execution authorized false；result/terminal identities exact。

## 7. Prohibited access/count ledger

`release_root_access=0`, `release_consumption=0`, `predevice_root_access=0`, `readiness_root_access=0`,
`retained_r3_access=0`, `legacy_r2_access=0`, `deep_corrective_access=0`, `other_external_payload_access=0`,
`device_access=0`, `network_access=0`, `app_access=0`, `process_access=0`, `listener_access=0`, `camera_access=0`,
`ray_access=0`, `strip_access=0`, `capture_access=0`, `nonzero_light=0`, `formal_r6_access=0`, `formal_root_creation=0`,
`td_c_access=0`, `firmware_access=0`, `deployment_access=0`, `config_write_calls=0`, `formal_capture_count=0`,
`physical_capture_count=0`, `commit_by_executer=0`, `stage_by_executer=0`, `new_task_ids=0`, `corrective_suffixes=0`。

## 8. Planner decision request

请Planner按active PLAN独立验收并先归档reviewed PLAN/ER。Executer停止于
`RETURN_FOR_G4_04_E2_PREFORMAL_GATE_REVIEW`。本handoff不授权执行或生成G4-05/G4-06 PLAN。
