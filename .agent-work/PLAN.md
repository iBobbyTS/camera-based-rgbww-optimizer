# REF-G4-02-PREDEVICE：durable offline oracle package

**计划状态：** `EXECUTABLE_PENDING_ORCHESTRATOR_ACTIVATION_DURABLE_OFFLINE_ORACLE`

**Executable：** `true`（仅在Orchestrator对齐FULL并提交§2 activation child后生效）

**Active task count：** `1`

**Active task：** `REF-G4-02-PREDEVICE`

**Reference goal：** `REF-G4-COMPLETE`

**唯一 Planner stop：** `RETURN_FOR_G4_02_DURABLE_OFFLINE_ORACLE_REVIEW`

`PLAN_MACHINE_CONTRACT={"schema":"planner_execution_contract_v2","contract_id":"G4-PREDEVICE-DURABLE-OFFLINE-ORACLE-V1","plan_status":"EXECUTABLE_PENDING_ORCHESTRATOR_ACTIVATION_DURABLE_OFFLINE_ORACLE","executable":true,"active_task_count":1,"active_task":"REF-G4-02-PREDEVICE","reference_task_id":"REF-G4-02-PREDEVICE","reference_goal":"REF-G4-COMPLETE","reference_task_status":"ACTIVE_AFTER_ORCHESTRATOR_ACTIVATION_DURABLE_OFFLINE_ORACLE","activation_state":"DRAFT_WAITING_ORCHESTRATOR_FULL_ALIGNMENT_AND_FOCUSED_COMMIT","activation_commit":{"expected_parent":"125158a3c1b8fa36a3a377290d90ebd53e46ec8a","expected_parent_tree":"ff738d440240de1a18989360e211939f8401887d","expected_subject":"docs(plan): activate g4 durable predevice oracle","expected_changed_paths":[".agent-work/EXECUTION_RESULT.md",".agent-work/FULL_PLAN_REFERENCE.md",".agent-work/PLAN.md",".agent-work/archived/EXECUTION_RESULT-20260803-1217.md",".agent-work/archived/PLAN-20260803-1217.md"],"child_sha_recorded_in_plan":false},"reviewed_plan_archive":{"path":".agent-work/archived/PLAN-20260803-1217.md","bytes":6858,"sha256":"bf6bcb8010406a578774e9f8bced707ff0116a56cca84de693742e89e413f4ca","source_body_bytes":5953,"source_body_sha256":"bc74180c41a514694b426712ee765f9432a6a099a7fcfd32dc3705ca9988e1b8"},"reviewed_execution_result_archive":{"path":".agent-work/archived/EXECUTION_RESULT-20260803-1217.md","bytes":3450,"sha256":"1cd0a9ee081c16bdecf88250602edfdae1d0bdbc9b3dc634129b143b7ab8fb9c","source_body_bytes":2542,"source_body_sha256":"8585991d5297a0972480a73a2ad1e7d62b7f37dc82004cf2f994796f1f433c65"},"accepted_owner":{"path":"src/camera_based_rgbww_optimizer/optimization/p7_successor_predevice.py","bytes":12066,"sha256":"0d6c529934b59a2faedf802bdd1e872a8c18085d055c4bfb1604e49032885be1"},"accepted_tests":{"path":"tests/test_p7_successor_predevice.py","bytes":19429,"sha256":"eb90e55026a1c4bd927c80ab80f198346eb23ac97122eb52dabf914f99c1c509"},"single_current_action":"extend_the_accepted_predevice_owner_with_minimal_repo_owned_durable_persist_and_replay_then_generate_and_validate_one_exact_offline_package","executor_repo_write_paths":["src/camera_based_rgbww_optimizer/optimization/p7_successor_predevice.py","tests/test_p7_successor_predevice.py",".agent-work/EXECUTION_RESULT.md"],"durable_root":"/Volumes/4T/temp/rgbww-optimizer/g4-predevice-oracle-125158a3c1b8-20260803T181631Z","durable_root_preflight":"ABSENT_AT_PLANNER_2026_08_03T18_16_31Z","durable_root_mode":448,"durable_artifacts":[{"name":"predevice-oracle-result.json","mode":384},{"name":"terminal-seal.json","mode":384}],"release_bundle":{"path":"/Volumes/4T/temp/rgbww-optimizer/g4-successor-lineage-779c7d9572d9-20260803T172055Z/release","device":16777244,"inode":2478933,"mode":448,"artifacts":[["frozen-inputs.json",5047,"8a81a906d2a94903a365f54b33c224a8ec99ce8d519ae2317cdc213c6e0264f8"],["r6-formal-plan.json",899,"dea5f979950909d5b3e8fd93c3a76e4fd18c0242158eade7967c4c62ec72cc3b"],["release-descriptor.json",2024,"6843ef5007b9ebe3bfef1f7c8c1864ed0b86b3000d3d72caa8f08f67ce3bb452"],["validation-summary.json",432,"07e831616c303e68f9bf863a722b8b640c3726556f47143db8299083f941cc07"],["terminal-seal.json",808,"d9d7b784a4ec910d7c7740bc560ed87f2b99ab1744c19df42097d5683b668850"]]},"release_source":{"head":"779c7d9572d991f82076c892ec8198a059bbe44e","checkpoint":"779c7d9572d991f82076c892ec8198a059bbe44e","tree":"1ead5268917612d1232543b1a7eca28788f3980c"},"policy":{"path":"/Users/ibobby/Projects/WLED-RGBWW/config/hsi/p7-ray-td-b-exposure-policy-v2.json","bytes":4065,"sha256":"c9080d18571f617cb7d323ade843ff9c86bf92e3795d23e3999e26d413968681"},"eq_reference":{"root":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-exposure-qual-r6-f37517a-20260727T1928","manifest_bytes":7980,"manifest_sha256":"41136d0d1530163668e111b7a9213bb1b9df330d8a168b451c752e3e5dca28e9","status":"qualified_1_2500","selected_shutter":"1/2500","root_traversal_allowed":false},"evaluate_successor_predevice_invocation_cap":1,"durable_root_creation_cap":1,"independent_package_replay_cap":1,"retry":0,"alternate_root_count":0,"release_consumption":0,"retained_r3_access":0,"legacy_r2_access":0,"other_external_experiment_payload_access":0,"device_access":0,"network_access":0,"camera_access":0,"ray_access":0,"strip_access":0,"capture_access":0,"formal_r6_access":0,"td_c_access":0,"firmware_access":0,"deployment_access":0,"plan_edits_by_executer":0,"full_edits_by_executer":0,"archive_edits_by_executer":0,"guide_edits":0,"research_edits":0,"commit_by_executer":0,"canonical_validator_success":false,"eligibility":false,"release_consumable":false,"release_consumption_authorized":false,"retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","device_authorized":false,"camera_authorized":false,"ray_authorized":false,"strip_authorized":false,"capture_authorized":false,"formal_r6_authorized":false,"td_c_authorized":false,"success_candidate_proposal_allowed":true,"planner_stop":"RETURN_FOR_G4_02_DURABLE_OFFLINE_ORACLE_REVIEW","future_reference_task":"REF-G4-03-REAL-ZERO-READINESS","future_stage_locked":true}`

## 1. 唯一动作与credit边界

本包仍是同一flat task `REF-G4-02-PREDEVICE`，只完成fresh predevice oracle的durable offline package。不得创建task suffix，
不得恢复旧P7 corrective、retained R3或R2 release。成功只产生待Planner/Orchestrator审查的candidate proposal；在review与
focused checkpoint前，effective canonical validator success、eligibility、release consumable及consumption authorization继续
全部false，不释放G4-03、设备或formal阶段。

Executer repo write scope exact：

```text
src/camera_based_rgbww_optimizer/optimization/p7_successor_predevice.py
tests/test_p7_successor_predevice.py
.agent-work/EXECUTION_RESULT.md
```

External write scope exact为§5一个fresh root；不得写bundle、EQ root、retained/R2/其他external payload。PLAN/FULL/archives/
GUIDE/RESEARCH均只读。

## 2. Activation与intake

Orchestrator必须先把FULL active contract对齐本PLAN并创建唯一docs-only activation child：

```text
parent = 125158a3c1b8fa36a3a377290d90ebd53e46ec8a
parent tree = ff738d440240de1a18989360e211939f8401887d
subject = docs(plan): activate g4 durable predevice oracle
changed paths exact =
  .agent-work/EXECUTION_RESULT.md
  .agent-work/FULL_PLAN_REFERENCE.md
  .agent-work/PLAN.md
  .agent-work/archived/EXECUTION_RESULT-20260803-1217.md
  .agent-work/archived/PLAN-20260803-1217.md
```

Executer开始前必须证明：branch main；HEAD是上述parent的direct child；subject/path set exact；worktree clean；PLAN/FULL
repo-owned parser均为contract `G4-PREDEVICE-DURABLE-OFFLINE-ORACLE-V1`、active count 1、task exact；archive
bytes/SHA/body identities exact；accepted owner/test identities exact。任一drift立即stop，不得reset/clean/stash。

再次以纯existence check证明§5 root不存在；若已存在立即stop，既不读取其payload也不换root。

## 3. Maintainability与owner收敛

CodeGraph已确认：

- accepted `p7_successor_predevice.py`是successor/provenance/thermal的small composition owner；
- provenance已有exclusive 0700 root、canonical 0600 persist/fsync/reload、exact inventory/read与same-target identity owners；
- accepted module尚无durable package/replay entry point。

因此只允许在同一accepted module加入最小durable persistence/replay seam及必要closed-schema guard；不得修改
`measure_p7_thermal_diagnostics.py`、`p7_thermal_diagnostics.py`、`analyze_p7_thermal_diagnostics.py`，不得复制
filesystem、canonical JSON、successor validator或thermal semantics，不得新增CLI、external controller、adapter或第二个module。

允许的production行为只有：

1. `persist_successor_predevice_evidence(...)`（名称可作最小一致调整）内部调用
   `evaluate_successor_predevice` exact once；
2. 委托provenance `create_exclusive_root`、`persist_canonical_json`写§5 exact artifacts；
3. `replay_successor_predevice_evidence(...)`委托provenance root/inventory/exact-read/decode/same-target，复用同一result
   closed-schema guard，验证terminal对result identity的exact非循环引用；
4. 返回root/result/seal frozen identities及replay status，不赋予effective authority。

薄调用点只可构造PLAN冻结的dataclass/expectation并各调用production persist/replay一次。它不得产生JSON bytes、拼装
evidence/seal mapping、实现validation、直接open/write/mkdir或成为持久化semantic owner。

## 4. Frozen input bundle

Read-only bundle exact：

```text
path = /Volumes/4T/temp/rgbww-optimizer/g4-successor-lineage-779c7d9572d9-20260803T172055Z/release
device/inode/mode = 16777244 / 2478933 / 0700
source HEAD/checkpoint = 779c7d9572d991f82076c892ec8198a059bbe44e
source tree = 1ead5268917612d1232543b1a7eca28788f3980c
```

| artifact | bytes | SHA-256 |
| --- | ---: | --- |
| `frozen-inputs.json` | 5047 | `8a81a906d2a94903a365f54b33c224a8ec99ce8d519ae2317cdc213c6e0264f8` |
| `r6-formal-plan.json` | 899 | `dea5f979950909d5b3e8fd93c3a76e4fd18c0242158eade7967c4c62ec72cc3b` |
| `release-descriptor.json` | 2024 | `6843ef5007b9ebe3bfef1f7c8c1864ed0b86b3000d3d72caa8f08f67ce3bb452` |
| `validation-summary.json` | 432 | `07e831616c303e68f9bf863a722b8b640c3726556f47143db8299083f941cc07` |
| `terminal-seal.json` | 808 | `d9d7b784a4ec910d7c7740bc560ed87f2b99ab1744c19df42097d5683b668850` |

```text
policy path = /Users/ibobby/Projects/WLED-RGBWW/config/hsi/p7-ray-td-b-exposure-policy-v2.json
policy bytes/SHA = 4065 / c9080d18571f617cb7d323ade843ff9c86bf92e3795d23e3999e26d413968681
EQ root reference = /Volumes/4T/temp/rgbww-optimizer/p7-td-b-exposure-qual-r6-f37517a-20260727T1928
EQ manifest bytes/SHA = 7980 / 41136d0d1530163668e111b7a9213bb1b9df330d8a168b451c752e3e5dca28e9
EQ status/shutter = qualified_1_2500 / 1/2500
```

Oracle不得遍历EQ root；不得访问retained R3、R2、其他release或其他external experiment payload。

## 5. Fresh durable root与artifact contract

Planner于`2026-08-03T18:16:31Z`只读确认下列exact root不存在：

```text
/Volumes/4T/temp/rgbww-optimizer/g4-predevice-oracle-125158a3c1b8-20260803T181631Z
```

Production owner只可创建该root exact once、mode 0700；parent不得创建、chmod或修复。成功inventory exact为两个regular、
non-symlink、0600 canonical JSON direct children，UTF-8 sort order：

```text
predevice-oracle-result.json
terminal-seal.json
```

`predevice-oracle-result.json`保存`evaluate_successor_predevice`返回的closed result，不得由runner改写。必须保留
public/final/strict/lineage pass、call counts 1/1/1、五artifact identities、release/source/policy/EQ/R6/operational/locks、
candidate proposal与effective authority。

`terminal-seal.json` schema exact `g4_successor_predevice_terminal_seal_v1`；success status exact
`sealed_pass_non_authorizing_waiting_planner_review`。它必须以path/bytes/SHA/device/inode/mode exact引用result artifact，
包含root identity、evaluate/persist/replay call accounting、retry 0、release consumption 0、retained status及全部false
effective authority；不得自引用，不得包含G4-03/device/formal authorization。

Independent replay exact once必须重新绑定root/inventory、两文件identity/mode/bytes/SHA/canonical bytes，验证result closed
schema、terminal引用与authority，再返回`g4_successor_predevice_evidence_replay_v1 / pass / artifact_count=2`。

## 6. Failure evidence、cleanup与zero policy

`evaluate_successor_predevice`最多调用1次，durable root最多创建1次，independent replay最多1次，retry=0，alternate root=0。

- owner validation在root创建前失败：不创建root，写ER并stop；
- root create失败或pre-exists：不修复、不读取、不换root，写ER并stop；
- root已创建后的任何failure：保留已写证据，不删除、不覆写；production owner仅可best-effort写
  `terminal-seal.json` exact once，status `sealed_fail_non_authorizing`，记录failed phase/primary code/result identity或null；
- failure seal自身失败：同时保留primary与seal failure，立即stop；
- provenance owner负责descriptor close、file/root fsync和reload；不得新增temp sidecar、rename repair或shell cleanup删除；
- 无论pass/fail，release bundle与所有输入只读，release consumption保持0，全部device/formal access为0。

一旦真实root创建动作开始，任何failure都直接返回Planner，不允许在本execution修代码、重跑、换root或创建corrective suffix。

## 7. Tests与pre-real gates

在真实root调用前，更新meaningful tests，至少覆盖：

1. success path evaluator exact once、root exact once、result/seal persist各一次、replay exact once；
2. two-artifact inventory、0700/0600、canonical encoding、terminal non-circular exact reference；
3. existing proposal/effective authority separation保持；
4. evaluator failure发生在root创建前且zero root；
5. pre-existing root、root identity drift、result persist failure、terminal persist failure、inventory/identity/hash/canonical drift fail closed；
6. post-root primary failure会attempt failure seal once并保留root；seal failure不隐藏primary；
7. replay不调用evaluator、不消费release、不fallback或换owner/root；
8. AST/import guard继续证明无handwritten JSON/filesystem/process/device owner及无CLI；
9. old corrective/retained markers、source/policy/EQ/R6/operational/locks negative matrix继续pass。

Synthetic roots只允许test-owned `TemporaryDirectory(dir="/Volumes/4T/temp/rgbww-optimizer")`并自动清理；不得读取历史payload。

按顺序执行并记录fresh exact counts/exits：

```text
.venv/bin/python -m unittest tests.test_p7_successor_predevice -v
.venv/bin/python -m unittest tests.test_p7_successor_predevice tests.test_p7_successor_lineage tests.test_p7_retained_r3_provenance_io tests.test_p7_td_b_r6_contract -v
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python -m compileall -q src tests
codegraph sync
codegraph explore "p7_successor_predevice durable persistence replay ownership call paths"
git diff --check
```

CodeGraph sync后再次确认只有accepted module拥有predevice result/seal/replay语义；provenance仍唯一拥有bytes/fsync/identity。
所有pre-real gates通过后才可运行§5真实single-call package。

## 8. Real invocation与acceptance candidate

薄调用点以§4 exact `PredeviceExpectation`和§5 root调用production persist owner once，再以owner返回的frozen identities调用
production replay once。不得手工读取/生成/修补artifact，不得进行第二次evaluator或alternate validation。

Success必须同时证明：

```text
evaluate_successor_predevice invocation = 1
public/final/strict counts = 1/1/1
durable root identity/mode = exact / 0700
artifact inventory = exact two / both 0600
result and seal canonical identity replay = pass
retry / alternate root / release consumption = 0 / 0 / 0
retained R3 = RETAINED_UNVALIDATED_UNCONSUMED
effective authority = all false
```

ER必须记录root device/inode/mode、两个artifact bytes/SHA/device/inode/mode、package/replay closed result、code/test post-change
bytes/SHA、all test counts、git diff classification及zero ledger。成功候选只可建议：

```text
canonical_validator_success = true
eligibility = true
release_consumable = true
release_consumption_authorized = false
scope = exact_g4_01_release_only_waiting_planner_and_orchestrator
```

该建议不是live authority；Planner review前FULL不得变true。G4-03仍locked。

## 9. Handoff与stop

最终repo dirty set必须exact为§1三个Executer paths；external writes必须exact为§5 root。不得stage/commit/amend/push，不得编辑
PLAN/FULL/archives/GUIDE/RESEARCH。唯一stop为`RETURN_FOR_G4_02_DURABLE_OFFLINE_ORACLE_REVIEW`。

若任何失败涉及科学合同、source contract、history、quality或无法保持single owner，记录exact evidence并stop给Planner/
Orchestrator；不得自行改变GUIDE、冻结input、root或stage route。

## 10. 维护性判断

这是对335-line accepted composition owner的最小持久化扩展，不触及三个巨型P7模块。Persistence/serialization继续委托
provenance single source of truth，successor/thermal语义继续由原owners负责；新增测试覆盖failure seal、identity replay和
authority边界。禁止CLI及平行controller，避免恢复旧失控模式。
