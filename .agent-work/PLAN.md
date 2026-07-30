# REF-P7-25-R2-B1A-C3E6F17-CORRECTIVE-6：canonical-row scanner 与冻结对象纠偏

**计划状态：** `active_planner_corrective_only`

**Planner 日期：** `2026-07-29`

**Reference task：** `REF-P7-25-R2-B1A-C3E6F17-CORRECTIVE-6`

**Parent reviewed task：** `REF-P7-25-R2-B1A-C3E6F17-CORRECTIVE-5`

**active_plan_contract_id：** `P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F17-CORRECTIVE-6`

**只读 FULL SHA-256（Orchestrator 同步前冻结值）：** `95cd9a2aebb10006128c5999f8ca52d9ad517a430fcc414ea7450789928e12b6`

**C5 review archive：** `.agent-work/PLANS/20260729-1840-p7-retained-r3-option-b-b1a-c3e6f17-corrective-5-review.md`；SHA-256 `4fb5e0649e35efe2f1603de928c923795f3fb99aca78ceb94145b9c1308a28ce`。

`PLAN_MACHINE_CONTRACT={"schema":"planner_execution_contract_v1","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F17-CORRECTIVE-6","task_id":"REF-P7-25-R2-B1A-C3E6F17-CORRECTIVE-6","parent_reference_task_id":"REF-P7-25-R2-B1A-C3E6F17-CORRECTIVE-5","package_kind":"bounded_offline_contract_qualification_only","single_current_action":"direct_exec_command_start_one_python_stdlib_script_then_append_one_execution_result_and_stop","expected_full_sha256":"95cd9a2aebb10006128c5999f8ca52d9ad517a430fcc414ea7450789928e12b6","canonical_wrapper":{"physical_line_start":true,"single_line":true,"backtick_wrap_exactly_once":true,"exact_json_object":true,"plan_prefix":"PLAN_MACHINE_CONTRACT=","full_prefix":"FULL_PLAN_MACHINE_STATE=","candidate_count":{"plan":1,"full":1},"ignore_noncanonical_text":true},"required_subset_12":{"plan_sha":"0a0620853ad6003027bcbe66ded8765a36c3898b900b4584ecdbed93697040f7","full_sha":"95cd9a2aebb10006128c5999f8ca52d9ad517a430fcc414ea7450789928e12b6","plan_candidate_count":1,"full_candidate_count":1,"task_id":"REF-P7-25-R2-B1A-C3E6F17-CORRECTIVE-6","active_task":"REF-P7-25-R2-B1A-C3E6F17-CORRECTIVE-6","active_plan_contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F17-CORRECTIVE-6","retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","candidate_contract_orchestrator_verified":true,"artifact_operations":0,"path_operations":0,"execution_result_append_cap":1},"zero_budget":{"artifact_operations":0,"path_operations":0,"fallback":0,"retry":0,"reuse":0,"rewrite":0,"alternate_path":0,"old_root_touch":0,"controller_access":0,"source_access":0,"test_execution":0,"git_mutation":0,"release_access":0,"network_access":0,"env_access":0,"device_access":0,"camera_access":0,"ray_access":0,"strip_access":0},"gate_before_path_operations":true,"execution_result_append_cap":1,"append_once_on_gate_pass_or_fail":true,"planner_stop_required":true}`

## 唯一 executable action（Orchestrator 同步 FULL 后才可 dispatch）

Executer 只能通过一次 direct `exec_command` 启动一个 Python 标准库脚本；不得嵌套复杂 heredoc、二级 dispatcher、子进程、Codex CLI 或其他启动器。scanner 只把同时满足“物理行首、单行、两端各一个反引号、前缀后为 exact JSON object、无尾随字符”的 canonical row 计数；正文自然语言、JSON/schema 描述、示例及其中的 marker 字符串一律不计数。脚本只读当前 PLAN/FULL raw bytes 及 canonical rows，逐字节计算 frozen SHA，并按 machine contract 执行唯一性、wrapper、required-subset、contract-exact、owner-binding 与 zero-budget audit。

Executer 不得读取代码、测试、archive、旧 ER、controller、source、candidate、fixture、canonical content、release、retained R3、`.env` 或任何外部路径；不得自创字段、别名、键值、谓词、补偿映射或通过条件。`required_subset_12` 与 `zero_budget` 均以上方 machine row 中唯一 JSON object 为唯一输入，必须逐键、逐值、逐类型比较；不得从自然语言推断、合并、展开或替换字段。

## 证据、预算与停止

- marker/strict-JSON/required-subset/owner gate 必须先于一切 `lexists`、`lstat`、mkdir、open、artifact 或其他 path operation；gate 结论前 path counter 必须为 `0/0`。
- artifact/path/test/Git/device/release/network/`.env`/camera/Ray/strip 全为 `0`；fallback/retry/reuse/rewrite/alternate/old-root/controller/source 全为 `0`，并与唯一 `zero_budget` object 完全相等。
- 无论 PASS 或 FAIL，Executer 最多向 `.agent-work/EXECUTION_RESULT.md` append 一次，记录两份 raw SHA、candidate lines/count、12 项逐键结果、wrapper/contract/owner/zero-budget ledger、首次失败阶段、全部 zero counters 与 terminal 状态；append 后立即 stop。

**Planner stop：** 收到一次 ER 或明确的 terminal handoff 后停止。PASS 仅表示离线 contract qualification，不是 bootstrap、release、R3、正式实验或设备授权。
