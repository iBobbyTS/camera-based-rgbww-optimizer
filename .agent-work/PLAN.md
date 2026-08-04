# REF-G4-05-RAY-R6-STAGE-GATE terminal rejected checkpoint

**计划状态：** `TERMINAL_REJECTED_G4_05_WAITING_ORCHESTRATOR_PROVENANCE_REASSESSMENT`

**Executable：** `false`

**Active task count：** `0`

**Reviewed reference task：** `REF-G4-05-RAY-R6-STAGE-GATE`

**Terminal disposition：** `REJECTED_G4_05_COMMITTED_SOURCE_ATTESTATION_UNREACHABLE`

`PLAN_MACHINE_CONTRACT={"schema":"planner_terminal_checkpoint_v2","contract_id":"G4-RAY-R6-STAGE-GATE-OFFLINE-V1","plan_status":"TERMINAL_REJECTED_G4_05_WAITING_ORCHESTRATOR_PROVENANCE_REASSESSMENT","executable":false,"active_task_count":0,"active_task":null,"reference_task_id":"REF-G4-05-RAY-R6-STAGE-GATE","reference_goal":"REF-G4-COMPLETE","terminal_disposition":"REJECTED_G4_05_COMMITTED_SOURCE_ATTESTATION_UNREACHABLE","planner_review_complete":true,"activation_checkpoint":"2eb5b68e43340fbf96e94b9fb2d2b2a7df684d8d","activation_tree":"67b56594da1743271e2c361396281abd475c3ce0","reviewed_plan_archive":{"path":".agent-work/archived/PLAN-20260803-1835.md","bytes":25430,"sha256":"19db80ff5148613311b697dbd0d2123ba87888d03cbdb38fb2db8181afd99c0f"},"reviewed_execution_result_archive":{"path":".agent-work/archived/EXECUTION_RESULT-20260803-1835.md","bytes":14578,"sha256":"9aedae947d6f62c074500f18c66a5f59e57f45ba50cf9e2e6424ccab44271893"},"reviewed_root":"/Volumes/4T/temp/rgbww-optimizer/g4-ray-r6-stage-gate-724083157ae7-20260804T000832Z","root_identity":{"device":16777244,"inode":2558810,"mode":448},"root_inventory":["launch-descriptor.json","stage-gate.json","terminal-seal.json"],"planner_public_replay_calls":1,"planner_public_replay_pass":true,"planner_targeted_tests":{"tests":18,"passed":18},"runtime_required_key_scan_pass":true,"runtime_template_authority_false_pass":true,"real_delegate_signature_compatible":true,"real_delegate_contract_validator_pass":true,"legacy_authority_branch_preserved":true,"post_capture_validator_calls":0,"descriptor_source_checkpoint":"2eb5b68e43340fbf96e94b9fb2d2b2a7df684d8d","descriptor_source_tree":"67b56594da1743271e2c361396281abd475c3ce0","candidate_owner_present_in_descriptor_commit":false,"future_activation_requires_descriptor_source_identity":true,"committed_source_attestation_reachable":false,"rejection_classification":"PROVENANCE_AUTHORITY_CONTRACT_DEFECT_NOT_SCIENCE_NOT_HUMAN","accepted_launch_seam":false,"g4_05_stage_complete":false,"g4_06_planning_unlocked":false,"g4_06_execution_authorized":false,"release_consumption_authorized":false,"device_authorized":false,"camera_authorized":false,"ray_authorized":false,"strip_authorized":false,"formal_r6_authorized":false,"formal_root_creation_authorized":false,"td_c_authorized":false,"retry_authorized":false,"corrective_suffix_allowed":false,"new_task_id_allowed":false,"next_owner":"Orchestrator","next_action":"CLOSE_G4_05_REJECTED_AND_REASSESS_COMMITTED_SOURCE_AUTHORITY_NO_SUFFIX_NO_NEW_TASK","future_reference_task":"REF-G4-06-RAY-R6","future_reference_status":"LOCKED","planner_stop":"ORCHESTRATOR_G4_05_PROVENANCE_REASSESSMENT_NO_SUFFIX"}`

## Planner terminal decision

Planner拒绝本次G4-05 acceptance candidate。真实delegate shape已经收敛，拒绝点是未来PLAN-bound authority的committed-source attestation不可达：

- durable descriptor与唯一公开replay固定记录activation checkpoint/tree为
  `2eb5b68e43340fbf96e94b9fb2d2b2a7df684d8d` / `67b56594da1743271e2c361396281abd475c3ce0`；
- focused owner `p7_td_b_r6_stage_gate.py`与其测试在该commit中不存在，measure owner的新authority branch也尚未提交；因此该checkpoint/tree不能代表本候选的production source；
- `validate_future_activation()`又要求future activation的`source_checkpoint/source_tree`与descriptor exact相等；materialized runtime authority原样携带这两个值；
- Planner acceptance后所需focused code/test commit必然是`2eb5b68...`的后继并产生不同tree。现有合同因此无法同时绑定immutable descriptor与实际committed owner HEAD/tree，违反reviewed PLAN第3节的exact authority要求；
- 当前synthetic tests把activation identity固定为`2eb5b68...`，只证明pre-code identity可自洽，没有覆盖“focused commit后future activation绑定实际source commit”的必要路径。

这是provenance/authority工程合同缺陷，不是科学分支、Human授权、设备状态或测试运行失败。不得把它上升给Human/Advisor，也不得以offline测试通过或package replay通过替代committed-source binding。

## Accepted subordinate evidence retained

- new root唯一公开replay PASS：root device `16777244` / inode `2558810` / mode `0700`；inventory exact为
  `launch-descriptor.json`、`stage-gate.json`、`terminal-seal.json`；artifact identity与Executer handoff一致；
- package与descriptor authority全部false，claims仍为offline engineering evidence only；没有hardware/formal/quality/history/release credit；
- template为canonical `PLAN_SCHEMA_V2`，exact 16 captures、Ray-only、strip-zero、fixed shutters、budget16/setup0/ambient0/launch1/retry0；
- existing authorized validator在connect前拒绝non-authorizing template，并接受synthetic materialized runtime；legacy Human-authority branch未被替换；
- narrow hook的真实owner签名、三个keyword-only kwargs与delegate exact-once已被测试覆盖；无效activation/runtime在delegate前fail closed；
- Planner独立targeted `18/18` PASS；AST required-key scan确认materialized template包含`run_authorized_plan`与TD-B `execute_plan`实际读取的全部top-level keys；`cold_proxy_wait_s`仅在TD-A分支读取，不构成本task runtime-shape gap；
- post-capture ledger validator在G4-05调用计数为0；新root仍为immutable、non-authorizing offline candidate evidence。

这些成果可保留，但不能建立可用的committed-source launch authority，也不解锁G4-06 planning/execution。

## Archive identities

- Reviewed PLAN：`.agent-work/archived/PLAN-20260803-1835.md`，25430 bytes，SHA-256
  `19db80ff5148613311b697dbd0d2123ba87888d03cbdb38fb2db8181afd99c0f`；source body exact为23652 bytes /
  `c17d6a8893830f99399e3b94b4e7a43b6302ee3278c94979c24dac9bdc79ec80`。
- Reviewed EXECUTION_RESULT：`.agent-work/archived/EXECUTION_RESULT-20260803-1835.md`，14578 bytes，SHA-256
  `9aedae947d6f62c074500f18c66a5f59e57f45ba50cf9e2e6424ccab44271893`；source body exact为12867 bytes /
  `607ae8a0c226d63a6b02074fae757130628cadb5f9c56020d4e376d9ae3c0bf4`。

两份archive均为`historical_non_executable`，不授权execution、device、release、retry、stage entry、budget或commit。

## Exact stop

Live PLAN现在active0且non-executable。`REF-G4-06-RAY-R6`的planning与execution均保持locked；不得生成G4-06 PLAN、执行formal、创建formal root、消费release或访问设备。

返回Orchestrator关闭本次G4-05 rejected disposition并重新评估committed-source authority seam。不得创建corrective suffix、新task ID、alternate root或继续Executer修补循环；本Planner review不修改FULL、不commit。
