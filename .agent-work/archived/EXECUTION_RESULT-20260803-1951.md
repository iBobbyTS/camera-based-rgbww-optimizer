# Reviewed EXECUTION_RESULT archive: REF-G4-05 per-commit lineage history closure

- archive_status: HISTORICAL_NON_EXECUTABLE_REVIEWED_ACCEPTED
- timestamp: 2026-08-03T19:51:26-06:00
- source_owner: Executer
- source_type: EXECUTION_RESULT
- reviewed_scope: REF-G4-05-RAY-R6-STAGE-GATE / G4-RAY-R6-STAGE-GATE-OFFLINE-V1
- activation_checkpoint: 860b27359ab54a1c8c4b4a4737331e169e53cb38
- activation_tree: c4c9f0129beba2f13b663f9d392abab986e37484
- controlled_code_child: d813cba24f49ca8ae8b54004f7ec20592ee979ab
- controlled_code_child_tree: e5a940cb068ab1aec0d462edf8ea9f3b907eb1fe
- source_body_bytes: 12622
- source_body_sha256: fb4c677af69df9ed9bfa70173ea285560159172baa904c475d76ebe18f07e6e4
- terminal_disposition: ACCEPTED_G4_05_PER_COMMIT_SOURCE_ATTESTED_LAUNCH_GATE_G4_06_PLANNING_UNLOCKED_EXECUTION_FALSE
- reviewed_plan: .agent-work/archived/PLAN-20260803-1951.md
- exact_root: /Volumes/4T/temp/rgbww-optimizer/g4-ray-r6-stage-gate-70fec61ef830-20260804T012240Z
- phase1_Planner_targeted: 25/25 PASS
- phase1_Planner_descriptor_identity: PASS; deterministic SHA 637e11654d81edaa1d8884d43d6aab2d02ea7997fc892169bd4278b29f7ebfd2
- phase2_Planner_attestation: PASS; actual C/tree and live C/tree exact, ordered ledger empty
- phase2_Planner_blob_identity: PASS
- inherited_phase1_full: 942/942 PASS; not rerun
- Planner_public_replay_calls: 0
- evidence_disposition: accepted offline committed-source launch gate; package remains non-authorizing and unconsumed
- next_branch: G4-06 planning unlocked only; execution/device/formal/release/TD-C remain false
- historical_non_executable: true
- execution_authorized: false
---

# REF-G4-05 per-commit lineage history phase1 handoff

**状态：** `G4_05_PER_COMMIT_HISTORY_PHASE1_CANDIDATE`

**Reference task：** `REF-G4-05-RAY-R6-STAGE-GATE`

**Contract：** `G4-RAY-R6-STAGE-GATE-OFFLINE-V1`

**Planner stop：** `RETURN_FOR_G4_05_TWO_PHASE_PER_COMMIT_HISTORY_REVIEW`

本handoff只提交同一G4-05 task的per-commit history phase1 candidate。它不宣称G4-05 accepted、G4-06 unlocked、hardware ready、formal pass、quality/history pass或release consumable。Planner phase1若通过，只能返回`READY_FOR_ORCHESTRATOR_CONTROLLED_CODE_CHILD`；terminal disposition等待同一PLAN phase2。

## Activation A与intake

- activation A=`860b27359ab54a1c8c4b4a4737331e169e53cb38`；tree=`c4c9f0129beba2f13b663f9d392abab986e37484`。
- A direct parent=`70fec61ef8304c0d882ae02cb06a5e2bc0baa74b`；parent tree=`19452f7c0145b4bd99b8548051a7f00bb182125a`。
- A subject exact=`docs(plan): activate ray r6 lineage history closure`；changed paths exact且仅为：
  1. `.agent-work/FULL_PLAN_REFERENCE.md`
  2. `.agent-work/PLAN.md`
  3. `.agent-work/debug/INDEX.md`
  4. `.agent-work/debug/active/20260803-g4-05-committed-source-lineage-history.md`
- branch=`main`；activation commit未包含ER或candidate code/tests。
- Executer首次编辑前dirty path/SHA-256 exact：
  - `.agent-work/EXECUTION_RESULT.md`：`067f2dfe947832e79502187d10641d8d208defb0c9773bed013a7cb4bc8e5fa4`；
  - measure owner：`a6b2df22d3dde950962b600456bbeef02efb445b25679fcba69d805e6e5248d3`；
  - stage-gate owner：`bcb7430f77735740ab846649dcdf458dc043ce655db6cf808702391d633aec1e`；
  - focused tests：`3a4f91cdacf367e7259336a939ddbed3e6fa43cc3afc9da09caf43a57f8a8fb8`。
- GUIDE SHA=`659152f6c0ae69c90c701de4e57c352d771e4f0bf75cf9410271ba0a94200e35`；thermal scientific owner=`14955da5f19e9cd73532910eee295aaaf612ec9a78559c99a51d38c239c674d1`；wrapper=`2730d43507af14a531453978477439bb29ef93ae7dea8e0bddb6c2330e1242e5`，全部未改。
- PLAN/FULL strict parser执行前后active `1/1`，task/contract/canonical next exact同一G4-05；retained R3仍`RETAINED_UNVALIDATED_UNCONSUMED`；device/network/camera/Ray/strip/capture/formal/release/TD-C/G4-06 authority均false/0。

## Per-commit owner与bounded traversal

唯一owner仍为`p7_td_b_r6_stage_gate.validate_committed_source_attestation()`；没有新module、controller、schema family、task ID或corrective suffix。修改只发生在该focused owner及其private helpers：

1. 先保持原A/C identity、C direct parent/subject/三路径/blob/current candidate、C ancestor L、HEAD=L/tree检查；
2. L==C时产生empty ordered ledger并PASS；
3. L!=C时从L向C读取`git rev-list --parents -n 1 <child>`，每行必须exact为`child parent`两个checkpoint；merge、root-before-C、malformed/nonlinear parent row立即拒绝；
4. `visited` set从L开始，任何重复parent/cycle立即拒绝；verified C-ancestor-L与逐parent终止条件共同形成有限边界；
5. 每个adjacent `parent -> child`单独调用repo-owned`thermal.changed_paths_between_checkpoints(parent, child, project_root=root)`；不再用C..L endpoint net diff；
6. 每个adjacent path先过`_canonical_git_path()`，再要求exact `.agent-work/` prefix；`.agent-work-evil/`与所有其他path fail closed；
7. reverse traversal完成后翻转为C→L canonical ordered `post_child_commits` ledger；`post_child_changed_paths`只由该ledger按行、按path顺序flatten，不能再代表endpoint净diff；
8. source refs、current files与porcelain tracked/staged/untracked scope检查仍在history之后执行，ledger不能替代current identity。

### Canonical ledger shape

`post_child_commits`是ordered JSON list；每行exact keys：

- `parent_checkpoint`
- `child_checkpoint`
- `child_tree`
- `changed_paths`

Activation与runtime authority同时exact绑定该ledger、flattened paths、A/C/L identities及candidate-reference digest。Pure materializer要求typed `CommittedSourceAttestation`与activation canonical value一致；缺失、extra、reordered或伪造ledger均在delegate前拒绝。Descriptor只冻结：

- `linear_direct_child_required=true`
- `merge_commit_allowed=false`
- `nonlinear_history_allowed=false`
- `per_commit_adjacent_paths_required=true`
- `changed_path_prefix=.agent-work/`

Descriptor没有future C/L checkpoint/tree或future ledger。

### Read-only Git categories

production validator只使用：`rev-parse`、`rev-list --parents -n 1`、`show -s --format=%s`、`show C:path`、`ls-tree -z`、`merge-base --is-ancestor`、repo-owned adjacent `diff --name-only`、`status --porcelain=v1 -z --untracked-files=all`。没有Git mutation、shell string、checkout/reset/clean/stage/commit、network、root I/O或external payload。

Stable fail-closed codes新增/保留：

- `committed_source_post_child_non_linear_history`
- `committed_source_post_child_history_cycle`
- `committed_source_post_child_tree_invalid`
- `committed_source_post_child_query_failed`
- `committed_source_post_child_path_drift`
- `committed_source_post_child_ledger_shape_drift`
- `committed_source_post_child_ledger_drift`
- existing parent/subject/tree/blob/lineage/current-worktree codes保持。

## Synthetic topology evidence

所有synthetic repos均位于`/Volumes/4T/temp/rgbww-optimizer`自动回收临时目录；只在fixture内local init/config/commit/commit-tree/update-ref，network0，主repo Git未变。

Positive配置=`3`：

1. L=C：empty `post_child_commits`与empty flattened paths PASS；
2. C→L1→L2：两个`.agent-work/` direct children PASS；ledger exact按C→L排列，逐行parent/child/tree/adjacent path已断言；
3. L2状态仅`.agent-work/EXECUTION_RESULT.md`dirty：PASS。

1913/history exact rejection matrix：

- add `src/transient-post-child.py`，下一commit delete，final L tree exact恢复C tree：FAIL；
- 同样add/delete restored-tree覆盖`tests/`、`config/`、GUIDE、wrapper及`.agent-work-evil/`：全部FAIL；
- C后merge，merge tree exact等于first-parent/C tree：FAIL；
- merge side branch含source drift、merge tree仍恢复C tree：FAIL；
- 一个adjacent commit同时含`.agent-work/`与`src/`：FAIL。

既有wrong/missing/merge parent、wrong subject、changed path missing/extra/reordered、C/L tree、blob、non-descendant、post-child source/prefix、tracked/staged/untracked scope矩阵继续PASS。总计per-commit新增negative配置=`9`；既有topology negative=`18`继续PASS。Activation/runtime invalid matrix扩展为`31`，加入missing/forged runtime/activation `post_child_commits`；全部callback0、camera connect0。

## Frozen owners preserved

- `measure_p7_thermal_diagnostics.py`本包bytes与semantic完全未变：191221 bytes / SHA `a6b2df22d3dde950962b600456bbeef02efb445b25679fcba69d805e6e5248d3` / mode0644。
- template仍为non-authorizing`thermal.PLAN_SCHEMA_V2`；exact 16 Ray captures、strip zero、ambient/setup0、A/D/B/C shutters、logical/physical16、launch1、retry0及quality/history/cleanup contract保持。
- template SHA=`36b9e6e06663822a0e69781762e4993533db96204652b026ebe14c369f720d75`；existing authorized validator拒绝template/connect0；materialized runtime通过focused/existing validators/connect0。
- synthetic L=C runtime SHA=`01a903296cd37040d77b0a46c6666c4ea1b39ebac72c4cacd0fa974b626c9959`；descriptor SHA=`637e11654d81edaa1d8884d43d6aab2d02ea7997fc892169bd4278b29f7ebfd2`。这只是offline compatibility projection，不是G4-06 activation或formal evidence。
- narrow hook仍将runtime及exact `output_dir`/`run_name`/`camera_backend` kwargs交给existing `run_authorized_plan` exactly once；invalid paths callback0；legacy branch与runtime required keys继续PASS。
- `thermal.validate_td_b_r6_capture_ledger`仍是future post-capture owner；G4-05 build/evaluate/materialize/persist/replay调用0。Stage owner无device/control imports，未复制runner/capture/serializer/persistence/cleanup。

## Fresh immutable package

三个旧rejected roots access=`0`：

- `/Volumes/4T/temp/rgbww-optimizer/g4-ray-r6-stage-gate-a1db65d01cba-20260803T233631Z`
- `/Volumes/4T/temp/rgbww-optimizer/g4-ray-r6-stage-gate-724083157ae7-20260804T000832Z`
- `/Volumes/4T/temp/rgbww-optimizer/g4-ray-r6-stage-gate-a6ecdb5bbfa3-20260804T004013Z`

唯一新root=`/Volumes/4T/temp/rgbww-optimizer/g4-ray-r6-stage-gate-70fec61ef830-20260804T012240Z`。

- counters：absence1、create1、persist1、internal replay1、public replay1、retry0、repair0、alternate0、formal root0。
- root：device `16777244` / inode `2633068` / mode0700 (`448`)。
- inventory exact：`launch-descriptor.json`、`stage-gate.json`、`terminal-seal.json`。
- `stage-gate.json`：24195 bytes / SHA `8cef08f1af00eef981e86c2b2dd19ccb2a01c25ff01b1a3a246737858a652c54` / device `16777244` / inode `2633069` / mode0600 (`384`)。
- `launch-descriptor.json`：10499 bytes / SHA `637e11654d81edaa1d8884d43d6aab2d02ea7997fc892169bd4278b29f7ebfd2` / device `16777244` / inode `2633070` / mode0600 (`384`)。
- `terminal-seal.json`：861 bytes / SHA `27ab69edb05f3ac621c562c8f26c7dd68a5c3bb3ab0fbace52e4ecfb9aff0dfd` / device `16777244` / inode `2633071` / mode0600 (`384`)。
- terminal status=`sealed_offline_ray_r6_stage_gate_pass_waiting_planner_review`；terminal只引用前两artifact，不self-reference；package/descriptor/terminal authority与hardware/formal/quality/history/release claims全部false。
- package绑定A verified parent、allowed exact C child、final candidate refs和per-commit linear rule；没有C/L future identities。Public replay后未再次访问该root。

## Final candidate identities

- measure owner：191221 bytes / SHA `a6b2df22d3dde950962b600456bbeef02efb445b25679fcba69d805e6e5248d3` / mode0644 (`420`)；与PLAN initial exact相同。
- stage-gate owner：68797 bytes / SHA `d0be07db79fb1b5b2973d0b8f7775088b7cf2760f887c55bfbbd1c9b213db217` / mode0644 (`420`)。
- focused tests：57456 bytes / SHA `7edb812433df42632efa0935fa0e3abefd39ed399471096d5a3d6ebd47c64d0d` / mode0644 (`420`)。

三项与package descriptor candidate refs exact一致。

## Validation ledger

| Gate | Result |
| --- | --- |
| activation/dirty SHA/machine/locks | PASS |
| 1913 restored-tree + merge + mixed + ordered positive专项 | `4/4` test methods PASS，5.436s |
| first targeted | `24/25`；唯一error为test `LIVE_ROOT`仍是上一PLAN路径，正确返回`output_root_drift` |
| bounded fixture correction | 只更新A/tree/root constants；production owner未因此修改 |
| targeted pre-package | `25/25` PASS，18.613s |
| real-owner/per-commit pre-package | `9/9` PASS，11.712s |
| focused pre-package | `215/215` PASS，59.953s |
| compile/static | compileall PASS；wrapper `zsh -n` PASS；measure SHA frozen；endpoint-only authority0；device imports0 |
| absence/persist/internal/public | PASS；exact counters/identities见上 |
| targeted post-package | `25/25` PASS，17.375s |
| real-owner/per-commit post-package | `9/9` PASS，11.509s |
| focused post-package | `215/215` PASS，60.814s |
| unique fresh full suite | `.venv/bin/python -m unittest discover -s tests`：`942/942` PASS，177.722s，exit0/OK |
| CodeGraph sync/query | PASS；direct-parent traversal → adjacent diff/path ledger → source/worktree/candidate → activation/runtime → existing validator/hook/runner |
| final diff/machine/scope | PASS；PLAN/FULL active1/1 same task/contract/next；exact四项dirty；protected paths未改；`git diff --check` PASS |

Full输出中的argparse errors是预期negative-path测试。Fresh full只运行一次；package只public replay一次。

## Scope与safety

Current dirty paths exact：

1. `.agent-work/EXECUTION_RESULT.md`
2. `src/camera_based_rgbww_optimizer/optimization/measure_p7_thermal_diagnostics.py`
3. `src/camera_based_rgbww_optimizer/optimization/p7_td_b_r6_stage_gate.py`
4. `tests/test_p7_td_b_r6_stage_gate.py`

仅ER、stage owner、tests由本包改写；measure是冻结classified candidate，bytes未变。PLAN/FULL/debug/archives/GUIDE/RESEARCH/config/thermal owner/wrapper均未改。Executer未stage、commit、push、PR、reset、clean、checkout或revert。

Exact production counts：三个旧root/external payload/release root/predevice/readiness/E2/retained R3/legacy corrective/device/network/app/process/listener/camera connect/Ray/strip/capture/nonzero light/release consumption/formal R6/formal root/TD-C/firmware/deployment=`0`。

唯一stop=`RETURN_FOR_G4_05_TWO_PHASE_PER_COMMIT_HISTORY_REVIEW`。等待Planner phase1 closed review；本handoff不得被解释为terminal acceptance或G4-06 planning/execution authorization。
