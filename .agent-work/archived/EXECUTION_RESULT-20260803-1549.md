# Archive metadata

- archive_status: `HISTORICAL_NON_EXECUTABLE_REVIEWED_REJECTED_G4_04_E2_CANONICAL_OWNER_INJECTION_BYPASS_EVIDENCE`
- archived_at: `2026-08-03T15:49:36-06:00`
- source_owner: `Executer`
- source_type: `EXECUTION_RESULT`
- reviewed_scope: `REF-G4-04-E2 / bounded result-replay closure candidate and validation ledger`
- source_checkpoint: `68b645c9228450bb51cca3fbbf5f0917d4ff4ab9`
- original_body_bytes: `8209`
- original_body_sha256: `14f7273ffa0fb83737eb282567daf7fcdf8b08bd3156d17140c167e5739f4895`
- terminal_disposition: `REJECTED_G4_04_E2_CANONICAL_THERMAL_OWNER_INJECTION_BYPASS`
- reviewed_plan_pointer: `.agent-work/archived/PLAN-20260803-1549.md`
- exact_next_stop: `RETURN_ORCHESTRATOR_G4_04_CANONICAL_THERMAL_OWNER_SEAM_REASSESSMENT`
- historical_non_executable: `true`

Planner复核保留Executer的21/21、253/253、900/900、compile/static/source-scan/CodeGraph证据以及唯一test-seam correction记录，但这些证据未覆盖调用者同时注入伪canonical owners的public persist/replay seam。独立无I/O探针得到`FORGED_CANONICAL_OWNER_BYPASS=PROVEN`、`create=1`；因此handoff的acceptance candidate claim被拒绝。

本archive不授权执行、设备、release、formal、root、retry、corrective suffix、G4-05/06或commit。下方逐字节保留reviewed EXECUTION_RESULT body。

---

# REF-G4-04-E2：bounded result/replay closure Executer handoff

**候选状态：** `G4_04_E2_BOUNDED_RESULT_REPLAY_CLOSURE_ACCEPTANCE_CANDIDATE`

**PLAN contract：** `G4-E2-BOUNDED-RESULT-REPLAY-CLOSURE-V1`

**Reference task：** `REF-G4-04-E2`

**唯一 Planner stop：** `RETURN_FOR_G4_04_E2_BOUNDED_RESULT_REPLAY_CLOSURE_REVIEW`

本handoff只提出offline code/test contract closure候选；不宣称hardware ready、formal pass、release consumed、G4-05 execution
authorization或G4-06 unlock。本轮没有production evaluation/persist/replay，也没有创建或读取durable E2 root。

## 1. Activation intake

- activation HEAD：`68b645c9228450bb51cca3fbbf5f0917d4ff4ab9`
- direct parent：`f385288e2a465350d9d66801578b7bdc5e211122`
- activation tree：`0342076e7460153890e0ee0d9e1f989f73451208`
- parent tree：`ebcf5a67b563e6684e7f40b7cb23da625768613d`
- subject：`docs(plan): activate bounded e2 replay closure`
- exact activation changed paths：
  - `.agent-work/EXECUTION_RESULT.md`
  - `.agent-work/FULL_PLAN_REFERENCE.md`
  - `.agent-work/PLAN.md`
- branch：`main`；intake worktree clean。
- PLAN/FULL repo-owned strict parser：PASS；active count `1/1`，active task均为`REF-G4-04-E2`，canonical next singleton
  `REF-G4-04-E2`。
- GUIDE、rejected candidate source/test、thermal owner及review archives的bytes/SHA均与PLAN machine row exact一致。
- retained R3仍为`RETAINED_UNVALIDATED_UNCONSUMED`；release consumption、device、formal R6、TD-C、G4-05/06 authority均false/0。
- 已拒E2 package仅作为machine-row historical identity；未访问其root或payload。

## 2. Source/test identities

| Path | Before bytes / SHA-256 | After bytes / SHA-256 |
|---|---|---|
| `src/camera_based_rgbww_optimizer/optimization/p7_successor_e2.py` | `24222` / `20bd2ca3fe1bbf2931b7f2605c307ed00fe8c0848734e68edbe35600ba8c4fed` | `26151` / `ffbe04250a43e3c1329bc8cfce6ec60d7eb814070603e1f350f58e7b669e904a` |
| `tests/test_p7_successor_e2.py` | `16170` / `354f61e34ba714895f0fcd2b0ac50ef654ed8f685174f6ef76a1719d08c3ec1d` | `26715` / `15f6fdcd94165d1ab570d8ae75a1e5e53dda83e17ffe8e0262afb35e255c97f7` |

未修改PLAN/FULL/archives、GUIDE/RESEARCH、config、wrapper、三大P7模块或其他production/test文件。

## 3. Shared closed validation ownership

- 唯一shared semantic owner：`_validate_result_contract`。
- `evaluate_e2_preformal_gate`在return前调用shared validator，并复用本次已取得的thermal plan/status，保持builder、validator、status
  owner每次各一次调用。
- `persist_e2_package`在任何root create或persist之前调用同一validator；forged/open result证明create/persist调用均为0。
- `replay_e2_package`在inventory/regular-file/canonical decode后调用同一validator，再调用closed terminal validator；result与terminal
  任一语义或identity不匹配均不返回PASS。
- result top-level、reference ledger、formal plan、machine status、guards、authority全为closed exact shape；nested scalar严格按type/value比对，
  bool不可由int替代，list/tuple按长度与顺序严格比对；canonical encode/decode projection再次exact验证。
- reference ledger由唯一`E2Input` projection产生，完整覆盖source checkpoint/tree、GUIDE/policy、G4-01/02/03 artifacts与历史字段、
  protected-source顺序及全部identity。
- formal plan只通过`thermal.build_td_b_r6_formal_plan`与`thermal.validate_td_b_r6_formal_plan`取得/验证；decoded plan与builder
  JSON-native输出exact相等。E2 owner已删除完整formal plan、capture IDs、experiment ID与shutter/budget/failure literal副本。
- machine status只以`thermal.td_b_r6_machine_status` JSON-native输出为exact truth；E2 owner已删除本地envelope/lock/R6字面合同。
- filesystem、exclusive create、canonical JSON、regular-file identity与inventory继续只委托既有provenance owner。
- success terminal为closed exact shape；result name/device/inode/mode/bytes/SHA逐项绑定刚读取的regular-file identity；authority nested
  keys/type/value exact，self-reference false、retry/alternate root均0。

## 4. Negative/tamper coverage

- result top-level逐项missing及extra；guards empty/missing/extra/false/truthy-int；authority每一bool/zero字段的missing、extra、type/value drift。
- reference ledger各section、G4-01/02/03 artifact name/bytes/SHA/order/count、G4-03 transport/effect及protected-source tamper。
- formal plan missing/extra/field/capture order/shutter/budget/failure-contract tamper；machine status envelope/locks/R6/extra tamper。
- terminal top-level及authority missing/extra/type/value；result identity name/device/inode/mode/bytes/SHA drift。
- synchronized forgery：先持久化open/forged result，再按其新bytes/SHA构造匹配terminal reference；replay仍在shared semantic validator
  fail closed，未产生PASS。
- accepted evaluator result仍在测试专用ephemeral package完成canonical bytes、0700/0600 mode、exact inventory、terminal binding、deep
  immutable replay round-trip；测试结束后TemporaryDirectory root不存在。
- result/terminal persist-failure single fail seal与inventory drift既有assertions保留。

## 5. Fresh validation ledger

| Stage | Invocation | Result |
|---|---:|---|
| targeted first | 1/2 | `21 tests`, `12 failures`，同一test-seam mismatch，见下述bounded correction |
| targeted second | 2/2 | `21/21 PASS` in 0.255s |
| focused successor lineage/predevice/zero-readiness/E2/R6/thermal/provenance | 1/1 | `253/253 PASS` in 40.913s |
| full `unittest discover -s tests` | 1/1 | `900/900 PASS` in 158.347s |
| `compileall -q src tests` | 1/1 | PASS |
| `zsh -n tmp/run-p7-thermal-diagnostics.zsh` | 1/1 | PASS |
| repo-owned baseline-aware source scan | 1/1 | PASS；exact 2 paths；findings/private/env/network/symlink/unsafe path均0 |
| `git diff --check` | 1 | PASS |
| changed/protected path invariant | 1 | PASS；仅source/test/ER允许路径，protected trees相对activation HEAD未变 |
| `codegraph sync` | 1/1 | PASS，index already up to date |
| CodeGraph ownership query | 1 | PASS；shared validator为单一owner，thermal/provenance边明确，无device/network/process/controller边 |
| final PLAN/FULL machine parser | 1 | PASS；active `1/1` / `REF-G4-04-E2`，canonical next不变 |

Source scan activation baselines：source
`20bd2ca3fe1bbf2931b7f2605c307ed00fe8c0848734e68edbe35600ba8c4fed`；tests
`354f61e34ba714895f0fcd2b0ac50ef654ed8f685174f6ef76a1719d08c3ec1d`。扫描没有读取任何external payload。

### 唯一 bounded correction

Targeted首轮12个failure属于同一test-seam mismatch：旧测试把注入的machine-status fake同时作为owner truth传入evaluator，又期待它相对
自身被拒绝；这与新PLAN允许evaluator复用已取得existing-owner值冲突。唯一correction只把该测试改为对accepted result中的machine-status
tamper调用shared validator并相对真实thermal owner拒绝；production source未因该失败修改。第二次targeted通过；correction预算已用尽。

## 6. Root、authority与access ledger

- `production_evaluation=0`, `production_persist=0`, `production_replay=0`
- `new_durable_e2_root=0`, `formal_root_creation=0`, `experiment_root_creation=0`
- `test_ephemeral_root_residual=0`
- `existing_rejected_e2_root_access=0`, `external_payload_access=0`, `release_root_access=0`, `predevice_root_access=0`,
  `readiness_root_access=0`, `retained_r3_access=0`, `legacy_r2_access=0`, `deep_corrective_access=0`
- `device_access=0`, `network_access=0`, `app_access=0`, `process_access=0`, `listener_access=0`, `camera_access=0`,
  `ray_access=0`, `strip_access=0`, `capture_access=0`, `nonzero_light=0`
- `release_consumption=0`, `formal_r6_access=0`, `td_c_access=0`, `firmware_access=0`, `deployment_access=0`
- `g4_05_execution_authorized=false`, `g4_06_unlocked=false`
- `commit_by_executer=0`, `stage_by_executer=0`, `new_task_ids=0`, `corrective_suffixes=0`

## 7. Planner decision request

请Planner独立review并先归档reviewed PLAN/ER。Executer停止于
`RETURN_FOR_G4_04_E2_BOUNDED_RESULT_REPLAY_CLOSURE_REVIEW`；本handoff不授权执行或生成G4-05/G4-06 PLAN。
