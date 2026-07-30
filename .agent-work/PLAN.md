# REF-P7-25-R2-B1A-C3E6F17-CORRECTIVE-2：canonical task identity / marker gate 纠偏

**计划状态：** `active_executable_limited_input_contract_binding_corrective_only`

**Planner 日期：** `2026-07-29`

**Reference task：** `REF-P7-25-R2-B1A-C3E6F17-CORRECTIVE-2`

**active_plan_contract_id：** `P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F17-CORRECTIVE-2`

**只读 FULL SHA-256：** `a676268f625091fbc2c2a3b7f388dd9b113a4ae247a376354a1e43ff1df82e99`

**Reviewed archive：** `.agent-work/PLANS/20260730-0008-p7-retained-r3-option-b-b1a-c3e6f17-corrective-1-review.md`

**Reviewed archive SHA-256：** `66b8fe140aefad4db93fe9c394ddcb02106a7727482e668b3bafabbaefea5edb`

`PLAN_MACHINE_CONTRACT={"schema":"planner_execution_contract_v1","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F17-CORRECTIVE-2","task_id":"REF-P7-25-R2-B1A-C3E6F17-CORRECTIVE-2","parent_reference_task_id":"REF-P7-25-R2-B1A-C3E6F17-CORRECTIVE-1","package_kind":"bounded_offline_marker_and_limited_input_qualification_only","single_current_action":"perform_one_offline_inline_code_marker_and_strict_json_gate_qualification_then_append_one_execution_result_and_stop","expected_full_sha256":"a676268f625091fbc2c2a3b7f388dd9b113a4ae247a376354a1e43ff1df82e99","required_full_subset_fields":12,"required_full_subset_status":"must_be_exactly_12_of_12","activation_status":"active_executable_limited_input_contract_binding_corrective_only","plan_marker":"PLAN_MACHINE_CONTRACT=","full_marker":"FULL_PLAN_MACHINE_STATE=","canonical_task_field":"task_id","full_task_binding":"active_task_must_equal_task_id","reference_task_alias_forbidden":"reference_task_id","inline_code_required":true,"exact_marker_count":1,"marker_alias_forbidden":"PLAN_MACHINE_STATE=","gate_failure_terminal_before_any_path_operation":true,"allowed_input_scope":["current_plan_raw_bytes","full_unique_machine_row_and_f17_section","shared_git_metadata"],"forbidden_input_scope":["execution_result","archives","controller","source","candidate","fixture","canonical_content","tests","retained_r3","release","network","env","device"],"artifact_operations":0,"path_operations":0,"fallback":0,"retry":0,"reuse":0,"rewrite":0,"alternate_path":0,"production_code":0,"test_execution":0,"git_mutation":0,"device_access":0,"release_access":0,"network_access":0,"execution_result_append_cap":1,"old_f17_root_touch":0,"old_f17_root_retry":0,"planner_stop_required":true}`

## 唯一 executable action

Executer 只能进行一次本地、离线、无副作用的 qualification，并只读取上述允许的 raw inputs：

1. 对当前 PLAN raw bytes 解析 inline-code 行：必须恰好一条反引号包裹、内容前缀为 `PLAN_MACHINE_CONTRACT=`，提取 marker 后至结束反引号前的 JSON bytes；canonical identity 只能读取 `task_id`，缺失或出现 `reference_task_id` alias 即 reject。
2. 对 FULL 唯一 machine row 解析 inline-code 行：必须恰好一条反引号包裹、内容前缀为 `FULL_PLAN_MACHINE_STATE=`，不得把 `PLAN_MACHINE_STATE=` 当 alias；校验 required subset 恰为 12/12，且 `active_task` 必须显式等于 PLAN `task_id`、contract 与 `RETAINED_UNVALIDATED_UNCONSUMED` 与本计划一致。
3. 两个 loader 均拒绝零/多 marker、缺失或错位反引号、malformed/duplicate-key/non-finite JSON、非 object、错误类型或 required-key mismatch，并记录 rejection ledger。
4. 任一 gate failure 必须在任何 `lexists`、`lstat`、mkdir、open 或其他 path operation 前 terminal；预算为 `0`，path-operation counter 必须保持 `0/0`。不得触碰、检查、创建、删除、修复、复用或重试旧 F17 root，也不得创建任何新路径或 artifact。

## 证据、停止与禁止项

结果必须记录 PLAN/FULL raw input SHA、marker extraction 与 strict-JSON rejection case ledger、首次失败阶段、预算 `0`、`0/0` path-operation counter，以及不触碰旧 F17 root 的声明；不得通过再次检查旧路径证明该声明。Executer 仅可向 `.agent-work/EXECUTION_RESULT.md` append 一次结果，随后立即停止（one ER append then stop）。

本包禁止读取 ER、archive、controller/source、candidate、fixture、canonical content、tests、retained R3、release、network、`.env` 或 device；禁止 production/controller/test/Git mutation、fallback、retry、reuse、rewrite、alternate path、bootstrap、release、eligibility、授权或任何设备操作。不得重试旧 F17 root。

**Planner stop：** 纠偏结果返回后立即停止；下一轮先归档本包并依据证据决定 REJECT，或另立 fresh-root bootstrap 计划。本包不进入 bootstrap、controller、R3、release、network 或 device。
