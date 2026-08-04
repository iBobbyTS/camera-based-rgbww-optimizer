# Reviewed EXECUTION_RESULT archive: REF-G4-05 committed-source attestation phase1

- archive_status: HISTORICAL_NON_EXECUTABLE_REVIEWED_REJECTED
- timestamp: 2026-08-03T19:13:58-06:00
- source_owner: Executer
- source_type: EXECUTION_RESULT
- reviewed_scope: REF-G4-05-RAY-R6-STAGE-GATE / G4-RAY-R6-STAGE-GATE-OFFLINE-V1
- activation_checkpoint: 955397add65e7be0c31e8edebb0b5e397a2f31a3
- activation_tree: f23902ec26aeba0765f24bdcd5a61f6e39a14878
- source_body_bytes: 13058
- source_body_sha256: 067f2dfe947832e79502187d10641d8d208defb0c9773bed013a7cb4bc8e5fa4
- terminal_disposition: REJECTED_G4_05_POST_CHILD_HISTORY_NET_DIFF_BYPASS
- reviewed_plan: .agent-work/archived/PLAN-20260803-1913.md
- exact_root: /Volumes/4T/temp/rgbww-optimizer/g4-ray-r6-stage-gate-a6ecdb5bbfa3-20260804T004013Z
- Planner_public_replay_calls: 0
- Planner_targeted_result: 22/22 PASS
- Planner_independent_probe: FAIL; validator accepts C..L history containing a transient src commit followed by restoration because final net changed-path set is empty
- evidence_disposition: candidate/package remain non-authorizing offline evidence; no controlled code child may be created and no G4-06/device/formal/release credit is granted
- exact_next_branch: active0 terminal return to Orchestrator with no further Executer correction or code child
- historical_non_executable: true
- execution_authorized: false
---

# REF-G4-05 committed-source attestation phase1 handoff

**状态：** `G4_05_COMMITTED_SOURCE_ATTESTATION_PHASE1_CANDIDATE`

**Reference task：** `REF-G4-05-RAY-R6-STAGE-GATE`

**Contract：** `G4-RAY-R6-STAGE-GATE-OFFLINE-V1`

**Planner stop：** `RETURN_FOR_G4_05_TWO_PHASE_COMMITTED_SOURCE_ATTESTATION_REVIEW`

本handoff只提交同一G4-05 task的一阶段candidate/code/package closed-review材料。它不宣称G4-05已accepted，不解锁G4-06 execution，也不宣称hardware/formal/quality/history/release readiness。Planner phase1若通过，只能返回`READY_FOR_ORCHESTRATOR_CONTROLLED_CODE_CHILD`；terminal disposition必须等待同一PLAN的phase2。

## Activation A与dirty ownership

- activation A：`955397add65e7be0c31e8edebb0b5e397a2f31a3`；A tree：`f23902ec26aeba0765f24bdcd5a61f6e39a14878`。
- A direct parent：`a6ecdb5bbfa3fc8dc360f52bd78f6821dfc2f22d`；parent tree：`96728c09259db1bf8412f6b746a8ff471ab364ae`。
- A subject exact：`docs(plan): activate ray r6 source attestation`；changed paths exact且仅为`.agent-work/FULL_PLAN_REFERENCE.md`与`.agent-work/PLAN.md`；branch=`main`。
- Executer首次编辑前dirty path/SHA-256 exact匹配PLAN：
  - `.agent-work/EXECUTION_RESULT.md`：`607ae8a0c226d63a6b02074fae757130628cadb5f9c56020d4e376d9ae3c0bf4`；
  - `measure_p7_thermal_diagnostics.py`：`f81925e225e749c25354d8382c94bb053390e53aaa10542e2d12f2c4a56288eb`；
  - `p7_td_b_r6_stage_gate.py`：`734b756bf1a20275a508d71cc203d2de8e4eef69cc614ba62f6fc64d4b9927ff`；
  - `test_p7_td_b_r6_stage_gate.py`：`41ec3bbe791f97af6e6437c29c36cd482f7495f5c97a309b625f4f5b52125bef`。
- GUIDE SHA-256=`659152f6c0ae69c90c701de4e57c352d771e4f0bf75cf9410271ba0a94200e35`；thermal scientific owner=`14955da5f19e9cd73532910eee295aaaf612ec9a78559c99a51d38c239c674d1`；wrapper=`2730d43507af14a531453978477439bb29ef93ae7dea8e0bddb6c2330e1242e5`，均未改。
- PLAN/FULL strict parser执行前后均active `1/1`，task/contract/canonical next exact同一G4-05；retained R3=`RETAINED_UNVALIDATED_UNCONSUMED`；release consumption/device/camera/Ray/strip/formal/TD-C/G4-06 authority均false/0。

## Single attestation owner与A/C/L角色

- 唯一owner/API：`p7_td_b_r6_stage_gate.validate_committed_source_attestation(descriptor, future_activation, *, repo_root)`，返回frozen `CommittedSourceAttestation`；没有新module、controller、corrective suffix或parallel validator。
- A只记录为`verified_parent_checkpoint/tree`，role exact=`activation_parent_not_code_owner`；A不再出现在runtime authority的`source_checkpoint/source_tree`，也不能冒充actual code source。
- C是未来Orchestrator controlled code-owner child：必须是A direct child、单parent、subject exact、三路径exact、blob/candidate identity exact。
- L是future live activation：必须等于C或是C的descendant；C..L只允许canonical `.agent-work/` paths。Runtime authority显式区分`code_owner_checkpoint/tree`与`live_activation_checkpoint/tree`。
- materializer保持pure projection：调用方必须先取得typed `CommittedSourceAttestation`，activation中的canonical attestation必须与该typed result exact一致；expected runtime SHA只在activation，不写入runtime自身。
- narrow hook顺序为stage/template → descriptor → future activation + read-only committed-source validator → focused runtime → existing authorized validator → existing `run_authorized_plan(runtime_plan, output_dir=..., run_name=..., camera_backend=...)` exact once。

### Read-only Git query surface

production validator只使用以下read-only类别：

1. `git rev-parse`：repo top-level、A/C/L commit/tree及current HEAD/tree；
2. `git rev-list --parents -n 1`：C parent count/direct parent；
3. `git show -s --format=%s`及`git show C:path`：subject/blob bytes；
4. repo-owned`thermal.changed_paths_between_checkpoints()`的`git diff --name-only`：A..C及C..L paths；
5. `git ls-tree -z C -- path`：regular blob type/mode/path；
6. `git merge-base --is-ancestor C L`：lineage；
7. `git status --porcelain=v1 -z --untracked-files=all`：tracked/staged/untracked worktree scope。

validator没有write、checkout、reset、clean、stage、commit、root I/O或external payload access。Synthetic tests只在`/Volumes/4T/temp/rgbww-optimizer`的自动回收临时目录中执行local `git init/config/add/commit/commit-tree/update-ref`以构造拓扑；network=0且主repo Git未被修改。

## Descriptor controlled-child contract

- allowed child subject exact：`feat(stage-gate): accept ray r6 launch owner`。
- direct parent exact：A；merge=false。
- changed-path set/order exact：
  1. `src/camera_based_rgbww_optimizer/optimization/measure_p7_thermal_diagnostics.py`
  2. `src/camera_based_rgbww_optimizer/optimization/p7_td_b_r6_stage_gate.py`
  3. `tests/test_p7_td_b_r6_stage_gate.py`
- final candidate refs与package descriptor exact一致：
  - measure owner：191221 bytes / SHA-256 `a6b2df22d3dde950962b600456bbeef02efb445b25679fcba69d805e6e5248d3` / mode `0644` (`420`)；
  - stage-gate owner：65029 bytes / SHA-256 `bcb7430f77735740ab846649dcdf458dc043ce655db6cf808702391d633aec1e` / mode `0644` (`420`)；
  - focused tests：50348 bytes / SHA-256 `3a4f91cdacf367e7259336a939ddbed3e6fa43cc3afc9da09caf43a57f8a8fb8` / mode `0644` (`420`)。
- descriptor只包含`child_checkpoint_recorded=false`、`child_tree_recorded=false`、`live_checkpoint_recorded=false`、`live_tree_recorded=false`布尔声明；没有C/L future SHA、tree或blob OID，不自引用、不预知future commit。
- post-child rule：C必须为L ancestor；C..L only `.agent-work/`；`.agent-work-evil/`、path traversal、absolute/backslash路径与所有其他repo paths均fail closed。

## Synthetic Git positive/negative matrix

真实local Git拓扑positive配置=`3`：

1. A → C direct child，L=C，HEAD=L，scoped clean：PASS；
2. A → C → 两个`.agent-work/`-only descendants，actual source仍C、live=L：PASS；
3. phase2形态仅`.agent-work/EXECUTION_RESULT.md`dirty：PASS。

拓扑/worktree negative配置=`18`，全部在materializer/delegate前fail closed：

- wrong subject；wrong parent；missing parent；merge/extra parent；
- child changed paths extra；descriptor paths missing/extra/reordered；
- provided C tree错误；provided L tree错误；candidate blob SHA drift；descriptor prefilled child identity；
- C非L ancestor；C..L包含`src/`；C..L包含`.agent-work-evil/`；
- current candidate tracked drift、staged drift、outside untracked path。

稳定failure code覆盖：`committed_source_subject_drift`、`committed_source_parent_drift`、`committed_source_changed_paths_drift`、`committed_source_descriptor_semantic_drift`、`committed_source_tree_drift`、`committed_source_candidate_blob_drift`、`committed_source_lineage_drift`、`committed_source_post_child_path_drift`、`committed_source_current_candidate_drift`、`committed_source_worktree_scope_drift`。

另有activation/runtime invalid matrix=`28`：missing/extra字段、bool/int、A冒充C、descriptor/template/runtime hash、C/L identity、root/bounds、launch/retry，以及runtime schema/IDs/order/state/dwell/command/shutter/budget15/17/ambient/setup/retry/strip drift，全部callback0、camera connect0。

## Accepted runtime/owner compatibility preserved

- sealed template仍为`thermal.PLAN_SCHEMA_V2`，status waiting、authority/formal eligibility false；canonical template SHA-256=`36b9e6e06663822a0e69781762e4993533db96204652b026ebe14c369f720d75`。
- exact 16 Ray captures/order、A/D/B/C commands与fixed shutters、logical/physical16、setup/ambient0、launch1/retry0、strip zero、quality/history/cleanup contracts保持canonical thermal owner；runtime required top-level key scan PASS；`cold_proxy_wait_s`仍只属于TD-A branch。
- template被existing authorized validator在connect前拒绝；reference-consistent materialized runtime通过focused及existing validator，fake-capable backend connect0。
- synthetic role-separated runtime SHA-256=`4b77c6923d21b46155911983c607d18c32d7a8678f4be01a39faf1c605e36ada`；descriptor SHA-256=`c5cf914d7cb50b910341f5d87eb4804d0511f7b6c9ad1238be9eaeba657bfcd6`。这是offline compatibility projection，不是实际G4-06 activation或formal evidence。
- patch真实`measure.run_authorized_plan`后，runtime identity与`output_dir`/`run_name`/`camera_backend` kwargs exact once；hook没有复制runner body、device command、capture loop、serializer、persistence ledger或cleanup。
- legacy authorized-plan tests继续PASS；sealed package不能自授权。`thermal.validate_td_b_r6_capture_ledger`仍是future post-capture owner，本task build/evaluate/materialize/persist/replay调用计数0。

## New immutable offline package

两个旧rejected roots access=`0`：

- `/Volumes/4T/temp/rgbww-optimizer/g4-ray-r6-stage-gate-a1db65d01cba-20260803T233631Z`
- `/Volumes/4T/temp/rgbww-optimizer/g4-ray-r6-stage-gate-724083157ae7-20260804T000832Z`

唯一新root：`/Volumes/4T/temp/rgbww-optimizer/g4-ray-r6-stage-gate-a6ecdb5bbfa3-20260804T004013Z`。

- counters：absence1、create1、persist1、internal replay1、public replay1、retry0、repair root0、alternate root0、formal root0。
- root：device `16777244` / inode `2583482` / mode `0700` (`448`)。
- inventory exact：`launch-descriptor.json`、`stage-gate.json`、`terminal-seal.json`。
- `stage-gate.json`：24195 bytes / SHA-256 `779f4be5c6efda8752f4251dcca844d6fc03d05312510f796d609e6ad28e50e0` / device `16777244` / inode `2583483` / mode `0600` (`384`)。
- `launch-descriptor.json`：10358 bytes / SHA-256 `c5cf914d7cb50b910341f5d87eb4804d0511f7b6c9ad1238be9eaeba657bfcd6` / device `16777244` / inode `2583484` / mode `0600` (`384`)。
- `terminal-seal.json`：861 bytes / SHA-256 `785eaac822f6fa182e4c41ba746bc867c69ecf821e10d0cbabf338ce9dfe5b26` / device `16777244` / inode `2583485` / mode `0600` (`384`)。
- terminal status由public replay验证为`sealed_offline_ray_r6_stage_gate_pass_waiting_planner_review`；terminal只引用前两artifact，无self-reference；package/descriptor/terminal authority与hardware/formal/quality/history/release claims全部false。
- package绑定A verified parent、allowed child contract、三项final candidate refs及post-child `.agent-work/` rule；没有C/L future SHA/tree。package persist/replay未调用Git attestation materializer、existing authorized validator、post-capture validator或device owner。

## Validation ledger

| Gate | Result |
| --- | --- |
| intake topology/dirty SHA/machine/locks | PASS |
| first targeted | 首次`21/22`：唯一负向harness期望`descriptor_shape_drift`，owner正确返回`descriptor_semantic_drift` |
| bounded harness correction | 只校正该assertion；production semantic owner未改 |
| targeted pre-package | `22/22` PASS，12.812s；后补runtime-key assertion由随后完整focused覆盖 |
| real-owner/topology probes pre-package | `7/7` PASS，7.690s |
| focused pre-package | `212/212` PASS，55.283s |
| compile/static | `.venv/bin/python -m compileall -q src tests` PASS；`zsh -n tmp/run-p7-thermal-diagnostics.zsh` PASS；no-device-import/parallel-owner scan PASS |
| package absence/persist/internal/public | PASS；exact counters/identities见上 |
| targeted post-package | `22/22` PASS，12.190s |
| real-owner/topology probes post-package | `7/7` PASS，6.824s |
| focused post-package | `212/212` PASS，51.419s |
| unique final full suite | `.venv/bin/python -m unittest discover -s tests`：`939/939` PASS，170.709s，exit0/OK |
| CodeGraph sync/query | PASS（already up to date）；descriptor → committed-source validator → runtime validator → existing validator → narrow hook → existing runner single chain |
| final machine/scope/protected/diff | PASS；active1/1 same task/contract/next；exact四项dirty；protected paths未改；`git diff --check` PASS |

完整测试中的argparse输出为预期negative-path测试；candidate full suite只运行一次。Synthetic temp Git fixtures已由`TemporaryDirectory`回收。

## Final scope与safety

Current dirty/changed paths exact：

1. `.agent-work/EXECUTION_RESULT.md`
2. `src/camera_based_rgbww_optimizer/optimization/measure_p7_thermal_diagnostics.py`
3. `src/camera_based_rgbww_optimizer/optimization/p7_td_b_r6_stage_gate.py`
4. `tests/test_p7_td_b_r6_stage_gate.py`

PLAN/FULL/archives/GUIDE/RESEARCH/config/thermal scientific owner/wrapper均未改。Executer未stage、commit、push、创建PR、reset、clean、checkout或revert。

Exact production counts：old-root access/external payload/release root/predevice/readiness/E2/retained R3/legacy corrective/device/network/app/process/listener/camera connect/Ray/strip/capture/nonzero light/release consumption/formal R6/formal root/TD-C/firmware/deployment=`0`。

唯一stop：`RETURN_FOR_G4_05_TWO_PHASE_COMMITTED_SOURCE_ATTESTATION_REVIEW`。等待Planner phase1 closed review；本handoff不得被解释为terminal acceptance或G4-06 planning/execution authorization。
