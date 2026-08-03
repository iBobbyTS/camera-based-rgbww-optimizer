# REF-G4-02-PREDEVICE：terminal accepted durable oracle checkpoint

**计划状态：** `TERMINAL_ACCEPTED_WAITING_ORCHESTRATOR_FULL_UPDATE_AND_FOCUSED_COMMIT`

**Executable：** `false`

**Active task count：** `0`

**Active task：** `null`

**Reference goal：** `REF-G4-COMPLETE`

**唯一 Planner stop：** `RETURN_ORCHESTRATOR_TERMINAL_FULL_UPDATE_AND_FOCUSED_COMMIT_G4_03_PLANNING_ONLY`

`PLAN_MACHINE_CONTRACT={"schema":"planner_terminal_checkpoint_v2","contract_id":null,"plan_status":"TERMINAL_ACCEPTED_WAITING_ORCHESTRATOR_FULL_UPDATE_AND_FOCUSED_COMMIT","executable":false,"active_task_count":0,"active_task":null,"reference_task_id":"REF-G4-02-PREDEVICE","reference_goal":"REF-G4-COMPLETE","reference_task_status":"TERMINAL_ACCEPTED_DURABLE_PREDEVICE_EXACT_G4_01_RELEASE","accepted_disposition":"ACCEPTED_G4_02_DURABLE_PREDEVICE_EXACT_G4_01_RELEASE_ELIGIBLE_CONSUMABLE_UNCONSUMED","review_source_head":"79b8f03e65107e1d62f8de3b33ffb31d3413e185","review_source_tree":"a5002bdd389218af49fb7ac1629c236080da51ea","reviewed_plan_archive":{"path":".agent-work/archived/PLAN-20260803-1259.md","bytes":12554,"sha256":"6dfa02175a2d1b18da841f912b8aed0a56b59ec0ae473bdfbfff317628354f15","source_body_bytes":11598,"source_body_sha256":"82fc61ac7c15cfa8ca6aea374a916b067dccf9e96ab5c56f005c582ebd97f5c2"},"reviewed_execution_result_archive":{"path":".agent-work/archived/EXECUTION_RESULT-20260803-1259.md","bytes":7416,"sha256":"9553789352e278324f6d2a8078b19109e910286dc1f9292580322e7dc4a21ee7","source_body_bytes":6457,"source_body_sha256":"2e70137282284223f4fc842684183448989b54a05bede8d8355e6344632b2cf9"},"accepted_production_owner":{"path":"src/camera_based_rgbww_optimizer/optimization/p7_successor_predevice.py","bytes":24232,"sha256":"4c8bf96dca444b5412120534a1df5519976afc98fe4aa1aaf2b83596177ffc81"},"accepted_tests":{"path":"tests/test_p7_successor_predevice.py","bytes":29738,"sha256":"44ac81ae18ae0a8f041d53837c4c7d6c4e867cf4761c616bfb640117550d4cfa"},"validation":{"targeted":"18_of_18_pass","focused":"133_of_133_pass","full":"864_of_864_pass","full_seconds":146.475,"compileall":"pass","codegraph_sync":"pass","codegraph_explore":"pass","git_diff_check":"pass"},"durable_package":{"root":{"path":"/Volumes/4T/temp/rgbww-optimizer/g4-predevice-oracle-125158a3c1b8-20260803T181631Z","device":16777244,"inode":2495492,"mode":448},"artifacts":[{"path":"predevice-oracle-result.json","device":16777244,"inode":2495493,"mode":384,"bytes":3186,"sha256":"78fa982b7f318734afc158324b968ee71ff41b5ce7b91e27d6eabc0f60bc40d9"},{"path":"terminal-seal.json","device":16777244,"inode":2495494,"mode":384,"bytes":1114,"sha256":"39456ca3379df45cae0ca5337bf6d24d2040e6581dcd074b8ebf12d39b87e68e"}],"inventory_exact":true,"canonical_identities_verified":true,"terminal_non_circular_reference":true,"replay_schema":"g4_successor_predevice_evidence_replay_v1","replay_status":"pass"},"call_ledger":{"persist_successor_predevice_evidence":1,"evaluate_successor_predevice":1,"durable_root_create":1,"replay_successor_predevice_evidence":1,"retry":0,"alternate_root":0,"release_consumption":0},"repo_owned_name_derivation":"successor.ARTIFACT_NAMES","persisted_evidence_effective_authority":{"canonical_validator_success":false,"eligibility":false,"release_consumable":false,"release_consumption_authorized":false,"device_authorized":false,"camera_authorized":false,"ray_authorized":false,"strip_authorized":false,"capture_authorized":false,"formal_r6_authorized":false,"td_c_authorized":false},"planner_accepted_release_state":{"scope":"exact_g4_01_release_only","canonical_validator_success":true,"eligibility":true,"release_consumable":true,"release_consumption_authorized":false,"retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","device_authorized":false,"camera_authorized":false,"ray_authorized":false,"strip_authorized":false,"capture_authorized":false,"formal_r6_authorized":false,"td_c_authorized":false},"proposed_full_status_changes":{"g4_02_disposition":"ACCEPTED_G4_02_DURABLE_PREDEVICE_EXACT_G4_01_RELEASE_ELIGIBLE_CONSUMABLE_UNCONSUMED","active_task_count":0,"active_task":null,"active_plan_contract_id":null,"canonical_validator_success":true,"eligibility":true,"release_consumable":true,"release_consumption_authorized":false,"canonical_next_reference_task":"REF-G4-03-REAL-ZERO-READINESS","canonical_next_reference_status":"READY_FOR_PLANNING_ONLY_NOT_EXECUTABLE","device_authorized_by_this_file":false,"camera_authorized_by_this_file":false,"ray_authorized_by_this_file":false,"strip_authorized_by_this_file":false,"formal_r6_authorized":false,"td_c_authorized":false},"full_update_pending":true,"release_consumption":0,"retained_r3_access":0,"legacy_r2_access":0,"other_external_experiment_payload_access":0,"device_access":0,"network_access":0,"camera_access":0,"ray_access":0,"strip_access":0,"capture_access":0,"formal_r6_access":0,"td_c_access":0,"firmware_access":0,"deployment_access":0,"retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","planner_stop":"RETURN_ORCHESTRATOR_TERMINAL_FULL_UPDATE_AND_FOCUSED_COMMIT_G4_03_PLANNING_ONLY","future_reference_task":"REF-G4-03-REAL-ZERO-READINESS","future_reference_status":"READY_FOR_PLANNING_ONLY_NOT_EXECUTABLE","future_stage_locked":true}`

## 1. Planner acceptance

Planner接受`REF-G4-02-PREDEVICE` terminal disposition：

`ACCEPTED_G4_02_DURABLE_PREDEVICE_EXACT_G4_01_RELEASE_ELIGIBLE_CONSUMABLE_UNCONSUMED`

独立只读检查确认：root identity/mode、exact two inventory、两artifact device/inode/mode/bytes/SHA、canonical bytes、result closed core、
terminal对result的exact物理identity引用且不自引用、repo-owned successor artifact tuple、retry/consumption 0与persisted
effective authority全false。Planner没有再次调用evaluator、persist或replay，因此production ledger保持persist/evaluate/root/replay
1/1/1/1。

## 2. Evidence与validation

```text
root = /Volumes/4T/temp/rgbww-optimizer/g4-predevice-oracle-125158a3c1b8-20260803T181631Z
root device/inode/mode = 16777244 / 2495492 / 0700

predevice-oracle-result.json
  3186 bytes / 78fa982b7f318734afc158324b968ee71ff41b5ce7b91e27d6eabc0f60bc40d9
  device/inode/mode = 16777244 / 2495493 / 0600
terminal-seal.json
  1114 bytes / 39456ca3379df45cae0ca5337bf6d24d2040e6581dcd074b8ebf12d39b87e68e
  device/inode/mode = 16777244 / 2495494 / 0600
```

Fresh validation为18/18、133/133、864/864；compileall、CodeGraph sync/explore、diff check均PASS。Code/test identities与V2/V3
冻结值exact。Repo dirty在review前为exact 9 paths。

Reviewed evidence archives：

```text
.agent-work/archived/PLAN-20260803-1259.md
  12554 bytes / 6dfa02175a2d1b18da841f912b8aed0a56b59ec0ae473bdfbfff317628354f15
.agent-work/archived/EXECUTION_RESULT-20260803-1259.md
  7416 bytes / 9553789352e278324f6d2a8078b19109e910286dc1f9292580322e7dc4a21ee7
```

## 3. FULL status recommendation

对且仅对exact G4-01 release，fresh predevice durable oracle已经通过，因此Planner建议Orchestrator在FULL中设：

```text
REF-G4-02-PREDEVICE = terminal accepted
canonical_validator_success = true
eligibility = true
release_consumable = true
release_consumption_authorized = false
retained_r3_status = RETAINED_UNVALIDATED_UNCONSUMED
device/camera/Ray/strip/formal R6/TD-C authorization = false
```

`release_consumable=true`只表示该exact release可供后续明确PLAN消费；它不是当前消费、设备访问或formal authorization。本包
release consumption仍为0。

Orchestrator应先归档pre-rewrite FULL snapshot、删除live FULL中terminal G4-02 detail、应用上述状态并创建focused commit。
下一reference只能是`REF-G4-03-REAL-ZERO-READINESS`的`READY_FOR_PLANNING_ONLY_NOT_EXECUTABLE`；当前PLAN active0，
不得执行或编写G4-03 package。

## 4. Stop

当前stop只交给Orchestrator完成FULL terminal update和focused commit。Planner不修改FULL，不生成G4-03 executable PLAN，
不消费release，不访问设备或formal阶段。
