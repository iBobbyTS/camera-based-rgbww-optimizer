# REF-G4-05-RAY-R6-STAGE-GATE terminal rejected checkpoint

**计划状态：** `TERMINAL_REJECTED_G4_05_POST_CHILD_HISTORY_BYPASS_WAITING_ORCHESTRATOR`

**Executable：** `false`

**Active task count：** `0`

**Reviewed reference task：** `REF-G4-05-RAY-R6-STAGE-GATE`

**Terminal disposition：** `REJECTED_G4_05_POST_CHILD_HISTORY_NET_DIFF_BYPASS`

`PLAN_MACHINE_CONTRACT={"schema":"planner_terminal_checkpoint_v2","contract_id":"G4-RAY-R6-STAGE-GATE-OFFLINE-V1","plan_status":"TERMINAL_REJECTED_G4_05_POST_CHILD_HISTORY_BYPASS_WAITING_ORCHESTRATOR","executable":false,"active_task_count":0,"active_task":null,"reference_task_id":"REF-G4-05-RAY-R6-STAGE-GATE","reference_goal":"REF-G4-COMPLETE","terminal_disposition":"REJECTED_G4_05_POST_CHILD_HISTORY_NET_DIFF_BYPASS","planner_review_complete":true,"review_phase":"PHASE1_CLOSED_REJECTED","activation_checkpoint":"955397add65e7be0c31e8edebb0b5e397a2f31a3","activation_tree":"f23902ec26aeba0765f24bdcd5a61f6e39a14878","reviewed_plan_archive":{"path":".agent-work/archived/PLAN-20260803-1913.md","bytes":28031,"sha256":"bfda6db2cb6b589933e3a78a5eb2b170a5cfdfb7c592a27f7c910c0b0eb5022b"},"reviewed_execution_result_archive":{"path":".agent-work/archived/EXECUTION_RESULT-20260803-1913.md","bytes":14447,"sha256":"821133d9598445e19b1b8e8af78157eb08224c97c3ab469563e3b08b487388d5"},"reviewed_root":"/Volumes/4T/temp/rgbww-optimizer/g4-ray-r6-stage-gate-a6ecdb5bbfa3-20260804T004013Z","root_identity":{"device":16777244,"inode":2583482,"mode":448},"root_inventory":["launch-descriptor.json","stage-gate.json","terminal-seal.json"],"planner_public_replay_calls":0,"planner_targeted_tests":{"tests":22,"passed":22},"phase1_ready_for_controlled_code_child":false,"controlled_code_child_authorized":false,"post_child_lineage_uses_net_diff_only":true,"transient_non_orchestration_descendant_probe":{"non_orchestration_commits":2,"net_changed_paths":[],"validator_accepted":true,"attested_post_child_changed_paths":[]},"rejection_classification":"COMMITTED_SOURCE_LINEAGE_HISTORY_CONTRACT_DEFECT_NOT_HARNESS_NOT_SCIENCE_NOT_HUMAN","candidate_package_authority_false":true,"candidate_offline_evidence_only":true,"actual_code_child_checkpoint":null,"actual_code_child_tree":null,"g4_05_stage_complete":false,"g4_06_planning_unlocked":false,"g4_06_execution_authorized":false,"release_consumption_authorized":false,"device_authorized":false,"camera_authorized":false,"ray_authorized":false,"strip_authorized":false,"formal_r6_authorized":false,"formal_root_creation_authorized":false,"td_c_authorized":false,"retry_authorized":false,"corrective_suffix_allowed":false,"new_task_id_allowed":false,"executer_correction_allowed":false,"next_owner":"Orchestrator","next_action":"CLOSE_G4_05_REJECTED_NO_CONTROLLED_CODE_CHILD_NO_EXECUTER_REPAIR","future_reference_task":"REF-G4-06-RAY-R6","future_reference_status":"LOCKED","planner_stop":"ORCHESTRATOR_G4_05_TERMINAL_REASSESSMENT"}`

## Planner phase1 terminal decision

Planner拒绝本次G4-05 committed-source attestation candidate。Targeted测试、descriptor非自引用、A/C/L字段分离及scoped worktree parser均通过；唯一terminal defect是post-child lineage只验证C..L最终tree的净差异，没有验证每个descendant commit均为orchestration-only。

独立pure synthetic Git probe构造：

1. C后第一个descendant新增`src/transient-post-child.py`；
2. 第二个descendant删除该文件，恢复与C相同的source tree；
3. current HEAD=L、candidate bytes、protected sources和worktree均clean；
4. `git diff --name-only C..L`为空；
5. `validate_committed_source_attestation()`返回PASS，并把`post_child_changed_paths`证明为空。

因此一个包含两次非`.agent-work/`历史变化的lineage被误表述为orchestration-only descendant。它违反reviewed PLAN的受控后继合同；不能创建controlled code child，也不能解锁G4-06。

这是provenance/Git history attestation工程缺陷，不是21/22 harness assertion、科学问题、Human授权或设备问题。按本PLAN phase1规则，不允许再交给Executer修补。

## Accepted subordinate evidence retained

- activation A `955397add65e7be0c31e8edebb0b5e397a2f31a3` / tree
  `f23902ec26aeba0765f24bdcd5a61f6e39a14878`，parent/subject/FULL+PLAN topology exact；
- descriptor只记录A verified parent、allowed child subject/path与candidate refs，没有预填future C/L SHA/tree；
- runtime authority字段明确区分code owner C与live activation L；A不能冒充C；
- worktree parser使用porcelain `-z --untracked-files=all`，tracked/staged/untracked negative tests存在；
- Planner独立targeted `22/22` PASS；Executer记录的首次`21/22`只是期望`descriptor_shape_drift`而owner正确返回`descriptor_semantic_drift`，修订只改测试assertion，未改production owner；
- Executer记录focused `212/212`、final full `939/939`、compile/static/CodeGraph PASS；Planner没有重复full；
- 三项final candidate refs：
  - measure owner：191221 bytes / `a6b2df22d3dde950962b600456bbeef02efb445b25679fcba69d805e6e5248d3` / mode0644；
  - stage-gate owner：65029 bytes / `bcb7430f77735740ab846649dcdf458dc043ce655db6cf808702391d633aec1e` / mode0644；
  - focused tests：50348 bytes / `3a4f91cdacf367e7259336a939ddbed3e6fa43cc3afc9da09caf43a57f8a8fb8` / mode0644；
- new root仍是immutable non-authorizing offline evidence；Planner public replay calls0，未访问新root或两个旧root；
- package/device/formal/release/G4-06 authority与credit仍false/0。

这些成果可作为historical offline candidate evidence保留，但不能证明完整commit history为orchestration-only。

## Archive identities

- Reviewed PLAN：`.agent-work/archived/PLAN-20260803-1913.md`，28031 bytes，SHA-256
  `bfda6db2cb6b589933e3a78a5eb2b170a5cfdfb7c592a27f7c910c0b0eb5022b`；source body exact为26146 bytes /
  `86e2ec519c250540c5e27c49244d535f8e37242a1e0e3d1eba3f9026f9caf91b`。
- Reviewed EXECUTION_RESULT：`.agent-work/archived/EXECUTION_RESULT-20260803-1913.md`，14447 bytes，SHA-256
  `821133d9598445e19b1b8e8af78157eb08224c97c3ab469563e3b08b487388d5`；source body exact为13058 bytes /
  `067f2dfe947832e79502187d10641d8d208defb0c9773bed013a7cb4bc8e5fa4`。

两份archive均为`historical_non_executable`，不授权execution、Git child、device、release、retry或stage entry。

## Exact stop

Live PLAN现在active0且non-executable。不得创建`feat(stage-gate): accept ray r6 launch owner` controlled child；不得给Executer另一轮修补；不得生成suffix、新task、G4-06 PLAN或访问设备/formal/release。

返回Orchestrator关闭本次terminal rejected disposition并决定goal路线。Planner未修改FULL、candidate code/test或ER，未commit。
