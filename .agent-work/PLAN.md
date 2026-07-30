# REF-P7-25-R2-B1A-C3E6F17-CORRECTIVE-4：调用层封装最小纠偏

**计划状态：** `active_planner_corrective_only`

**Planner 日期：** `2026-07-29`

**Reference task：** `REF-P7-25-R2-B1A-C3E6F17-CORRECTIVE-4`

**Parent reviewed task：** `REF-P7-25-R2-B1A-C3E6F17-CORRECTIVE-3`

**active_plan_contract_id：** `P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F17-CORRECTIVE-4`

**只读 FULL SHA-256：** `359e12bdd766a2360a5349dd90dd49119acf2ac800401dcba81e6a41df756c49`

`PLAN_MACHINE_CONTRACT={"schema":"planner_execution_contract_v1","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F17-CORRECTIVE-4","task_id":"REF-P7-25-R2-B1A-C3E6F17-CORRECTIVE-4","parent_reference_task_id":"REF-P7-25-R2-B1A-C3E6F17-CORRECTIVE-3","package_kind":"bounded_offline_invocation_layer_wrapper_only","single_current_action":"direct_exec_command_start_one_python_stdlib_script_then_append_one_execution_result_and_stop","expected_full_sha256":"359e12bdd766a2360a5349dd90dd49119acf2ac800401dcba81e6a41df756c49","full_owner_field":"active_task","canonical_identity_field":"task_id","full_identity_binding":"must_equal","body_marker_examples_forbidden":true,"empty_payload_marker_examples_forbidden":true,"exact_plan_marker_count":1,"exact_full_marker_count_required":1,"gate_before_path_operations":true,"artifact_operations":0,"path_operations":0,"fallback":0,"retry":0,"reuse":0,"rewrite":0,"alternate_path":0,"old_root_touch":0,"controller_access":0,"source_access":0,"test_execution":0,"git_mutation":0,"release_access":0,"network_access":0,"env_access":0,"device_access":0,"camera_access":0,"ray_access":0,"strip_access":0,"execution_result_append_cap":1,"append_once_on_gate_pass_or_fail":true,"planner_stop_required":true}`

## 唯一 executable action（Orchestrator 同步 FULL 后才可 dispatch）

Executer 只能通过一次 direct `exec_command` 启动一个 Python 标准库脚本。调用层使用简单 argv/环境传递与普通脚本文件或安全的单层 heredoc；不得在 JavaScript 字符串中嵌套复杂 heredoc、反斜杠转义、模板插值或二级 dispatcher。Python 不得启动子进程、Codex CLI 或其他 dispatcher。

脚本启动后仅读取当前 PLAN raw bytes、FULL raw bytes 及其唯一 machine rows，执行 C3 的 canonical marker 唯一性、strict JSON、required-subset 与 owner-binding audit；不得读取代码、测试、archive、旧 ER、controller、source、candidate、fixture、canonical content、release、retained R3、`.env` 或任何外部路径。

## 证据、预算与停止

- marker/strict-JSON/owner gate 必须先于一切 `lexists`、`lstat`、mkdir、open、artifact 或其他 path operation；gate 结论前 path counter 必须为 `0/0`。
- artifact/path/test/Git/device/release/network/`.env`/camera/Ray/strip 全为 `0`；禁止 fallback、retry、reuse、rewrite、alternate path、bootstrap、controller、source、package、release 或二级 dispatcher。
- 无论 PASS 或 FAIL，Executer 最多向 `.agent-work/EXECUTION_RESULT.md` append 一次，记录 raw SHA、marker 行号/count、owner-binding、首次失败阶段、全部 zero counters 与 terminal 状态；append 后立即 stop，不得追加核验或执行后继工作。

**Planner stop：** 收到一次 ER 或明确的调用层 terminal handoff 后停止；不得把 PASS 解释为 bootstrap、release、R3、正式实验或设备授权。
