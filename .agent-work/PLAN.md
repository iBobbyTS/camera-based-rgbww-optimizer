# REF-G4-03-ZERO-READINESS：terminal accepted sealed-fail checkpoint

**计划状态：** `TERMINAL_ACCEPTED_SEALED_FAIL_WAITING_ORCHESTRATOR_FULL_UPDATE_AND_FOCUSED_COMMIT`

**Executable：** `false`

**Active task count：** `0`

**Active task：** `null`

**Reference goal：** `REF-G4-COMPLETE`

**唯一 Planner stop：** `RETURN_ORCHESTRATOR_FAIL_CLOSED_FULL_UPDATE_AND_FOCUSED_COMMIT`

`PLAN_MACHINE_CONTRACT={"schema":"planner_terminal_checkpoint_v2","contract_id":null,"plan_status":"TERMINAL_ACCEPTED_SEALED_FAIL_WAITING_ORCHESTRATOR_FULL_UPDATE_AND_FOCUSED_COMMIT","executable":false,"active_task_count":0,"active_task":null,"reference_task_id":"REF-G4-03-ZERO-READINESS","reference_goal":"REF-G4-COMPLETE","reference_task_status":"TERMINAL_ACCEPTED_SEALED_FAIL_NOT_READINESS_PASS","accepted_disposition":"ACCEPTED_G4_03_SEALED_FAIL_RAY_CONTROLLER_UNREACHABLE_FINAL_ZERO_UNPROVEN","review_source_head":"e64cdaf309ac623f978e1c8aa08988707aa0c344","review_source_tree":"fc6df2d0a394f6996d8f365122f6bb476fa56973","reviewed_plan_archive":{"path":".agent-work/archived/PLAN-20260803-1357.md","bytes":12684,"sha256":"adb4a85e99bb1bc95bd945186bc3018ac28da0fdab75cdda38ae0985ded56eff","source_body_bytes":11648,"source_body_sha256":"5374c5d54b34a9b79765857174e2fff2c91bb7fabb079e9a275b4a7d028e6432"},"reviewed_execution_result_archive":{"path":".agent-work/archived/EXECUTION_RESULT-20260803-1357.md","bytes":11416,"sha256":"5a9231805a661ee97980feb703316bf6f2857e5fc77d7bfec26c1d1e32bd5961","source_body_bytes":10375,"source_body_sha256":"110285565248da6e0fd0b9e200d88454ba156413a357afaaaa55763d8392b753"},"accepted_owner_candidate":{"path":"src/camera_based_rgbww_optimizer/optimization/p7_successor_zero_readiness.py","bytes":28288,"sha256":"fea119e6a49825cf5858732c5a27dd0187020b70bc6fa5d6e8e2b3c428dacc8c"},"accepted_tests":{"path":"tests/test_p7_successor_zero_readiness.py","bytes":16311,"sha256":"5e2efcbab079b46ca18e874ee5d684a73586517b58560d793d4bff6fc060a6b7"},"accepted_wrapper":{"path":"tmp/run-g4-zero-readiness.zsh","bytes":2969,"sha256":"13c61af94a8c3e326447fe59103db074b9c707d8670120e10c82d974c09ab62a"},"validation":{"executor_targeted":"8_of_8_pass","executor_focused":"245_of_245_pass","executor_full":"872_of_872_pass","planner_targeted":"8_of_8_pass","planner_relevant_subset":"139_of_139_pass","planner_full":"872_of_872_pass","planner_full_seconds":156.187,"compileall":"pass","wrapper_syntax":"pass","git_diff_check":"pass","codegraph_sync":"pass"},"sealed_root":{"path":"/Volumes/4T/temp/rgbww-optimizer/g4-zero-readiness-5d05cc14286a-20260803T191648Z","device":16777244,"inode":2501768,"mode":448,"inventory_count":14,"terminal_seal_sha256":"cc11b85ec69c94a44b6a0dcc4b46e001387938d1fc6765b284c56523b09be4a6","terminal_status":"sealed_fail_waiting_planner_review","terminal_self_reference":false,"referenced_artifacts":13},"failure":{"classification":"RAY_CONTROLLER_LISTENER_UNREACHABLE","endpoint":"ws://127.0.0.1:33782","main":"ConnectionRefusedError","python_finally":"ConnectionRefusedError","shell_cleanup":"ConnectionRefusedError","independent_final_zero":"ConnectionRefusedError","strip_generations":[2,3,5],"strip_final_zero_proven":true,"ray_final_zero_proven":false,"camera_reached":false},"call_ledger":{"strip_verified_zero":3,"strip_shell_zero":1,"strip_nonzero":0,"ray_set_zero":4,"ray_get_cct":0,"ray_get_node_config":0,"ray_nonzero":0,"camera_health_get":0,"camera_config_get":0,"camera_capture":0,"camera_config_write":0,"source_isolation_validation":0,"release_consumption":0,"formal_r6":0,"td_c":0,"retry":0,"alternate_root":0},"residual":{"owned_processes":0,"scratch_files":0,"automation":0},"g4_03_pass":false,"g4_04_unlocked":false,"future_reference_task":"REF-G4-03-ZERO-READINESS","future_reference_status":"WAITING_ORCHESTRATOR_ENVIRONMENT_RECOVERY_DECISION_NOT_EXECUTABLE","required_environment_fact":"EXACT_RAY_LISTENER_OWNER_AND_RESTORED_REACHABILITY_AT_WS_127_0_0_1_33782","human_governance_gate":false,"advisor_scientific_gate":false,"g4_01_reopen":false,"g4_01_contract_correction":"ALREADY_ACCEPTED_AT_2e8eeb59_DO_NOT_REOPEN","repair_plan_generated":false,"planner_stop":"RETURN_ORCHESTRATOR_FAIL_CLOSED_FULL_UPDATE_AND_FOCUSED_COMMIT"}`

## Planner terminal decision

Planner接受本次G4-03 evidence disposition：

`ACCEPTED_G4_03_SEALED_FAIL_RAY_CONTROLLER_UNREACHABLE_FINAL_ZERO_UNPROVEN`

接受的是完整、可追溯、fail-closed的失败证据以及正确执行失败路径的owner/test/wrapper candidate；不是G4-03 readiness
PASS。14项inventory、root/artifact modes、repo-owned canonical decode、terminal前13项物理identity/hash引用、非自引用terminal
均exact。Strip三次generation-bearing zero为2/3/5且五通道全零；Ray在main、Python finally、shell cleanup、
independent final-zero均因exact localhost listener连接拒绝，最终zero不可证明。Camera、capture、nonzero、
release consumption、formal与TD-C均为0；retry/alternate root、scratch、owned process与automation均为0。

离线验证记录为8/8、245/245、872/872；Planner独立复验targeted 8/8、相关子集139/139及full 872/872。
因此owner正确封存失败，但G4-04必须保持locked。

当前缺失的是exact Ray controller listener的owner与已恢复可达性这一工程/环境事实，不是Advisor科学问题，也不是Human高危授权事实。
当前PLAN冻结retry、alternate root和service recovery，所以本checkpoint本身不允许启动service或再次运行；Orchestrator应先更新FULL
为active0 fail-closed状态、审查并提交accepted owner/test/wrapper与review archives，再决定如何在既有exact bounds内取得环境恢复事实。
如果未来重新执行，必须由新的单任务PLAN授权fresh root；本轮不生成repair PLAN。

G4-01的error-priority/reachability contract已在`2e8eeb59`修正并accepted；当前tree/FULL已将G4-01和G4-02作为accepted
prerequisite，本决定不重开、复制或降级G4-01。

## Stop

Planner停止于`RETURN_ORCHESTRATOR_FAIL_CLOSED_FULL_UPDATE_AND_FOCUSED_COMMIT`。不修改FULL，不要求Human/Advisor作为治理门，
不授权service启动、device retry、G4-04、capture、release consumption、formal或TD-C。
