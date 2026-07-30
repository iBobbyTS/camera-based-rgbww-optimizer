# REF-P7-25-R2-B1A-C3E6F17-CORRECTIVE-5：required-subset/contract/zero-budget 纠偏

**计划状态：** `active_planner_corrective_only`

**Planner 日期：** `2026-07-29`

**Reference task：** `REF-P7-25-R2-B1A-C3E6F17-CORRECTIVE-5`

**Parent reviewed task：** `REF-P7-25-R2-B1A-C3E6F17-CORRECTIVE-4`

**active_plan_contract_id：** `P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F17-CORRECTIVE-5`

**只读 FULL SHA-256（Orchestrator 同步前冻结值）：** `95cd9a2aebb10006128c5999f8ca52d9ad517a430fcc414ea7450789928e12b6`

`PLAN_MACHINE_CONTRACT={"schema":"planner_execution_contract_v1","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F17-CORRECTIVE-5","task_id":"REF-P7-25-R2-B1A-C3E6F17-CORRECTIVE-5","parent_reference_task_id":"REF-P7-25-R2-B1A-C3E6F17-CORRECTIVE-4","package_kind":"bounded_offline_contract_qualification_only","single_current_action":"direct_exec_command_start_one_python_stdlib_script_then_append_one_execution_result_and_stop","expected_full_sha256":"95cd9a2aebb10006128c5999f8ca52d9ad517a430fcc414ea7450789928e12b6","canonical_wrapper":{"physical_line":"single_line_wrapped_in_one_backtick_at_each_end","plan_prefix":"PLAN_MACHINE_CONTRACT\\u003d","full_prefix":"FULL_PLAN_MACHINE_STATE\\u003d","candidate_count":{"plan":1,"full":1},"body_prefix_occurrences":0,"empty_payload_occurrences":0,"line_start_required":true,"line_end_required":true},"required_subset_12":{"plan_sha":"fb95192a98dd805e2d5e5ed35a1f14d9648cd79ee904279eaf22208681dfa5c3","full_sha":"95cd9a2aebb10006128c5999f8ca52d9ad517a430fcc414ea7450789928e12b6","plan_candidate_count":1,"full_candidate_count":1,"task_id":"REF-P7-25-R2-B1A-C3E6F17-CORRECTIVE-5","active_task":"REF-P7-25-R2-B1A-C3E6F17-CORRECTIVE-5","active_plan_contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F17-CORRECTIVE-5","retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","candidate_contract_orchestrator_verified":true,"artifact_operations":0,"path_operations":0,"execution_result_append_cap":1},"zero_budget_fields":["artifact_operations","path_operations","fallback","retry","reuse","rewrite","alternate_path","old_root_touch","controller_access","source_access","test_execution","git_mutation","release_access","network_access","env_access","device_access","camera_access","ray_access","strip_access"],"zero_budget_value":0,"contract_exact":{"json_canonicalization":"RFC8785-like sorted keys with compact separators","required_subset_exact":true,"unknown_contract_keys_forbidden":true,"unknown_predicates_forbidden":true,"full_active_task_must_equal_task_id":true,"full_active_plan_contract_must_equal_contract_id":true},"gate_before_path_operations":true,"artifact_operations":0,"path_operations":0,"fallback":0,"retry":0,"reuse":0,"rewrite":0,"alternate_path":0,"old_root_touch":0,"controller_access":0,"source_access":0,"test_execution":0,"git_mutation":0,"release_access":0,"network_access":0,"env_access":0,"device_access":0,"camera_access":0,"ray_access":0,"strip_access":0,"execution_result_append_cap":1,"append_once_on_gate_pass_or_fail":true,"planner_stop_required":true}`

## 唯一 executable action（Orchestrator 同步 FULL 后才可 dispatch）

Executer 只能通过一次 direct `exec_command` 启动一个 Python 标准库脚本；不得嵌套复杂 heredoc、二级 dispatcher、子进程、Codex CLI 或其他启动器。脚本只读当前 PLAN/FULL raw bytes 及其唯一 machine rows，逐字节计算 frozen SHA，并按 machine contract 执行唯一性、wrapper、required-subset、contract-exact、owner-binding 与 zero-budget audit。

Executer 不得读取代码、测试、archive、旧 ER、controller、source、candidate、fixture、canonical content、release、retained R3、`.env` 或任何外部路径；不得自创字段、别名、键值、谓词、补偿映射或通过条件。required-subset 只能使用上方冻结的 12 个键值，zero-budget 只能使用上方冻结字段集合。

## 证据、预算与停止

- marker/strict-JSON/required-subset/owner gate 必须先于一切 `lexists`、`lstat`、mkdir、open、artifact 或其他 path operation；gate 结论前 path counter 必须为 `0/0`。
- artifact/path/test/Git/device/release/network/`.env`/camera/Ray/strip 全为 `0`；fallback/retry/reuse/rewrite/alternate/old-root/controller/source 全为 `0`。
- 无论 PASS 或 FAIL，Executer 最多向 `.agent-work/EXECUTION_RESULT.md` append 一次，记录两份 raw SHA、candidate lines/count、12 项逐键结果、wrapper/contract/owner/zero-budget ledger、首次失败阶段、全部 zero counters 与 terminal 状态；append 后立即 stop。

**Planner stop：** 收到一次 ER 或明确的 terminal handoff 后停止。PASS 仅表示离线 contract qualification，不是 bootstrap、release、R3、正式实验或设备授权。
