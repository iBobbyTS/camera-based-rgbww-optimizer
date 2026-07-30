# REF-P7-25-R2-B1A-C3E6F17-CORRECTIVE-3：canonical machine-row 唯一性纠偏

**计划状态：** `active_executable_offline_canonical_row_uniqueness_only`

**Planner 日期：** `2026-07-29`

**Reference task：** `REF-P7-25-R2-B1A-C3E6F17-CORRECTIVE-3`

**active_plan_contract_id：** `P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F17-CORRECTIVE-3`

**只读 FULL SHA-256：** `a676268f625091fbc2c2a3b7f388dd9b113a4ae247a376354a1e43ff1df82e99`

**Reviewed archive：** `.agent-work/PLANS/20260729-1812-p7-retained-r3-option-b-b1a-c3e6f17-corrective-2-review.md`

**Reviewed archive SHA-256：** `93c7f85a11a8d81a567598e679c2962602dcde718870412bdfb844a8cb702edd`

`PLAN_MACHINE_CONTRACT={"schema":"planner_execution_contract_v1","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F17-CORRECTIVE-3","task_id":"REF-P7-25-R2-B1A-C3E6F17-CORRECTIVE-3","parent_reference_task_id":"REF-P7-25-R2-B1A-C3E6F17-CORRECTIVE-2","package_kind":"bounded_offline_canonical_machine_row_uniqueness_and_owner_semantics_only","single_current_action":"audit_canonical_plan_and_full_machine_rows_then_append_one_execution_result_and_stop","expected_full_sha256":"a676268f625091fbc2c2a3b7f388dd9b113a4ae247a376354a1e43ff1df82e99","activation_status":"active_executable_offline_canonical_row_uniqueness_only","canonical_identity_field":"task_id","full_identity_field":"active_task","body_marker_examples_forbidden":true,"empty_payload_marker_examples_forbidden":true,"exact_plan_marker_count":1,"exact_full_marker_count_required":1,"path_before_gate":true,"artifact_operations":0,"path_operations":0,"test_execution":0,"git_mutation":0,"device_access":0,"release_access":0,"network_access":0,"env_access":0,"old_root_touch":0,"retry":0,"execution_result_append_cap":1,"append_once_on_gate_pass_or_fail":true,"planner_stop_required":true}`

## 唯一 executable action

Executer 只可在本地离线读取当前 PLAN 的 raw bytes 与 FULL 的 raw bytes，完成一次 marker 唯一性审计，并修正本 PLAN 的 owner 语义：

1. 严格提取反引号包裹的完整 machine row；PLAN 必须恰好一条，FULL 必须恰好一条。正文、标题、示例和空 payload 不得包含可被 loader 匹配的 marker 前缀；不得将其他标签当作 alias。
2. 对唯一 row 做 strict JSON 校验（object、无 duplicate key、finite 数值、类型与 required keys 正确），并确认 PLAN `task_id` 与 FULL `active_task` 显式等值；任何失败立即 terminal。
3. 仅记录 raw SHA、物理行号、marker-count、owner 语义、首次失败阶段及计数器；不得访问任何旧 root、artifact、source、controller、candidate、fixture、canonical content、tests、release、retained R3、`.env`、network 或 device。

## 证据、预算与停止

- 必须 path-before-gate：在 gate 结论前不得 `lexists`、`lstat`、mkdir、open、创建/读取路径或其他 path operation；path-operation counter 必须为 `0/0`。
- artifact/path/test/Git/device/release/network/`.env`/camera/Ray/strip 全为 `0`；禁止 bootstrap、release、eligibility、授权、fallback、retry、reuse、rewrite、alternate path 或旧 root touch。
- 无论 gate pass 或 gate fail，Executer 最多向 `.agent-work/EXECUTION_RESULT.md` append 一次结果，记录上述证据后立即 stop；不得读取旧 ER、archive 或任何旧 root 来补证。

**Planner stop：** 收到本轮单次 ER（或明确记录 gate failure 且未成功 append 的 handoff）后停止；不得进入 bootstrap、controller、R3、release、network 或 device。
