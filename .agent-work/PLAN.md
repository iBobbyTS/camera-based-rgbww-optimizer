# REF-G4-03-ZERO-READINESS：terminal cleanup-contract failure checkpoint

**计划状态：** `TERMINAL_REJECTED_OVERALL_PASS_WAITING_ORCHESTRATOR_APP_LIFECYCLE_REASSESSMENT`

**Executable：** `false`

**Active task count：** `0`

**Active task：** `null`

**Reference goal：** `REF-G4-COMPLETE`

**唯一 Planner stop：** `RETURN_ORCHESTRATOR_APP_LIFECYCLE_CONTRACT_REASSESSMENT`

`PLAN_MACHINE_CONTRACT={"schema":"planner_terminal_checkpoint_v2","contract_id":null,"plan_status":"TERMINAL_REJECTED_OVERALL_PASS_WAITING_ORCHESTRATOR_APP_LIFECYCLE_REASSESSMENT","executable":false,"active_task_count":0,"active_task":null,"reference_task_id":"REF-G4-03-ZERO-READINESS","reference_goal":"REF-G4-COMPLETE","reference_task_status":"READINESS_ROOT_ACCEPTED_PASS_OVERALL_TASK_NOT_ACCEPTED","terminal_disposition":"REJECTED_G4_03_PASS_APP_GRACEFUL_QUIT_EXIT_MISMATCH_DESPITE_RESIDUAL_ZERO","review_source_head":"663c873e79708c91c4f788144ef2987d880e7a37","reviewed_plan_archive":{"path":".agent-work/archived/PLAN-20260803-1415.md","bytes":11371,"sha256":"8fdc95371fa21eb7a6a486cd9c145a76becae474aacd9159c66464a0689ad188","source_body_bytes":10251,"source_body_sha256":"8359238500b313c5f4b68ba6afe1b8e31132f9fae356a96cb0f58a36b35de472"},"reviewed_execution_result_archive":{"path":".agent-work/archived/EXECUTION_RESULT-20260803-1415.md","bytes":10449,"sha256":"0f05a0b25394ddde5f499d2e906e51d5d4a546f54bfcd6b10cbe906101835602","source_body_bytes":9377,"source_body_sha256":"9df3bf1601ae8d13819841188a16f474367d1efdcb907f48f8d23dfd8c3fd287"},"readiness_root":{"path":"/Volumes/4T/temp/rgbww-optimizer/g4-zero-readiness-d957a89a84d3-20260803T200550Z","device":16777244,"inode":2506552,"mode":448,"inventory_count":14,"terminal_status":"sealed_pass_waiting_planner_review","terminal_sha256":"c6fc7b2a14cfce2474e1a1369721ebbdf660aa60baccb4caf237873a1af2a39d","terminal_artifact_refs":13,"terminal_self_reference":false,"readiness_evidence_accepted":true},"call_ledger":{"strip_verified_zero":3,"strip_shell_zero":1,"strip_nonzero":0,"ray_set_zero":4,"ray_get_cct":2,"ray_get_node_config":1,"ray_nonzero":0,"camera_health_get":1,"camera_config_get":1,"camera_capture":0,"camera_config_write":0,"source_isolation_validation":2,"release_consumption":0,"formal_r6":0,"td_c":0,"retry":0,"alternate_root":0},"final_zero":{"strip":true,"ray":true,"strip_generations":[2,3,5]},"app_lifecycle":{"preexisting":false,"launch_count":1,"owned_pid":79395,"listener_owner_exact":true,"graceful_quit_count":1,"graceful_quit_exit":1,"graceful_quit_error":-128,"graceful_quit_status":"USER_CANCELED_NOT_SUCCESS","owned_pid_at_0s":true,"owned_pid_absent_from_1s_through_15s":true,"force_kill_count":0,"alternate_quit_count":0,"service_variant_count":0,"endpoint_variant_count":0},"final_residual":{"exact_app_process":0,"listener":0,"owned_process":0,"scratch":0,"readiness_helper_process":0,"automation":0},"g4_03_pass":false,"g4_04_unlocked":false,"future_reference_task":"REF-G4-03-ZERO-READINESS","future_reference_status":"WAITING_ORCHESTRATOR_APP_LIFECYCLE_CONTRACT_REASSESSMENT_NOT_EXECUTABLE","repair_plan_generated":false,"human_governance_gate":false,"advisor_scientific_gate":false,"g4_01_reopen":false,"g4_01_status":"ACCEPTED_NOT_REOPENED","planner_stop":"RETURN_ORCHESTRATOR_APP_LIFECYCLE_CONTRACT_REASSESSMENT"}`

## Planner decision

Readiness evidence自身接受：activation exact；fresh root 14项、0700/0600、canonical bytes、13项terminal引用与hash、
non-self-reference均通过；call ledger exact；strip/Ray final zero、camera health/config和两次source isolation通过；
capture/nonzero/config-write/consumption/formal/TD-C、retry、alternate root与variant均为0。

但整体G4-03 PASS被拒绝。PLAN §6明确要求本轮owned app同时满足“graceful quit成功”与“owned residual为0”。
Exact bundle-id AppleScript只调用一次，但exit为1且返回-128 `User canceled`；这不是成功。Owned PID从1秒起消失、
最终app/listener/owned/scratch residual均为0，只满足第二个必要条件，不能覆盖第一个失败条件。

Terminal disposition：

`REJECTED_G4_03_PASS_APP_GRACEFUL_QUIT_EXIT_MISMATCH_DESPITE_RESIDUAL_ZERO`

这是普通app-lifecycle/attestation工程合同问题，不是科学问题或Human授权问题。Planner不生成repair PLAN，不重试、
不访问设备/网络，不修改FULL。Orchestrator应将FULL收为active0、G4-04继续locked，并独立决定后续app lifecycle
success contract；不得把本次readiness root丢弃或重跑来改写证据。

G4-01仍为accepted，不重开。

## Stop

停止于`RETURN_ORCHESTRATOR_APP_LIFECYCLE_CONTRACT_REASSESSMENT`。本checkpoint不授权G4-04、service/app操作、
readiness retry、release consumption、capture、formal或TD-C。
