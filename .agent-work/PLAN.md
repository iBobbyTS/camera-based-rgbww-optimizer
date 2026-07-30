# REF-P7-25-R2-B1A-C3E6F17-CORRECTIVE-9：direct command quoting 纠偏

**计划状态：** `active_planner_corrective_only`

**Planner 日期：** `2026-07-29`

**Reference task：** `REF-P7-25-R2-B1A-C3E6F17-CORRECTIVE-9`

**Parent reviewed task：** `REF-P7-25-R2-B1A-C3E6F17-CORRECTIVE-8`

**active_plan_contract_id：** `P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F17-CORRECTIVE-9`

**只读 FULL SHA-256：** `b569f511a9d49881ae13b791d275f723bdb26e5062971fda50bbbcc939a7a7b8`

**C8 review archive：** `.agent-work/PLANS/20260730-0125-p7-retained-r3-option-b-b1a-c3e6f17-corrective-8-review.md`；SHA-256 `c10aa54dddadc8acddfbda64bbefe1d8f6bff1a231f3eda391d3b358af22d146`。

`PLAN_MACHINE_CONTRACT={"schema":"planner_execution_contract_v1","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F17-CORRECTIVE-9","task_id":"REF-P7-25-R2-B1A-C3E6F17-CORRECTIVE-9","parent_reference_task_id":"REF-P7-25-R2-B1A-C3E6F17-CORRECTIVE-8","package_kind":"bounded_offline_contract_qualification_only","single_current_action":"one_shell_safe_direct_python_command_then_at_most_one_execution_result_append_and_stop","expected_full_sha256":"b569f511a9d49881ae13b791d275f723bdb26e5062971fda50bbbcc939a7a7b8","canonical_wrapper":{"physical_line_start":true,"single_line":true,"backtick_wrap_exactly_once":true,"exact_json_object":true,"no_trailing_characters":true,"terminal_newline_policy":"exactly_one_lf_required; eof_terminal_line_rejected; crlf_rejected","plan_prefix":"PLAN_MACHINE_CONTRACT=","full_prefix":"FULL_PLAN_MACHINE_STATE=","candidate_count":{"plan":1,"full":1},"ignore_noncanonical_text":true,"marker_extraction_algorithm":"for each raw line including LF: require startswith one backtick; require exactly one terminal LF; reject no-LF EOF terminal lines and CRLF; strip exactly one LF; require endswith one backtick; inner=without outer backticks; require exact path prefix; json_slice=inner[len(prefix):]; json.loads(json_slice) must be object; accept only this row","candidate_line_expectation":{"plan":17,"full":21}},"required_subset_12":{"plan_sha":null,"full_sha":"b569f511a9d49881ae13b791d275f723bdb26e5062971fda50bbbcc939a7a7b8","plan_candidate_count":1,"full_candidate_count":1,"task_id":"REF-P7-25-R2-B1A-C3E6F17-CORRECTIVE-9","active_task":"REF-P7-25-R2-B1A-C3E6F17-CORRECTIVE-9","active_plan_contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F17-CORRECTIVE-9","retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","candidate_contract_orchestrator_verified":true,"artifact_operations":0,"path_operations":0,"execution_result_append_cap":1},"zero_budget_fields":{"artifact_operations":0,"path_operations":0,"fallback":0,"retry":0,"reuse":0,"rewrite":0,"alternate_path":0,"old_root_touch":0,"controller_access":0,"source_access":0,"test_execution":0,"git_mutation":0,"release_access":0,"network_access":0,"env_access":0,"device_access":0,"camera_access":0,"ray_access":0,"strip_access":0},"gate_before_path_operations":true,"execution_result_append_cap":1,"append_once_on_gate_pass_or_fail":true,"planner_stop_required":true}`

## 唯一 executable action（仅离线 contract qualification）

Executer 只能执行一次无 shell 引号风险的 direct Python 标准库命令；不得 heredoc、嵌套引号、反引号、shell eval、二级 dispatcher、子进程、Codex CLI 或其他启动器。推荐由 agent 在启动前把 qualification script 的 UTF-8 bytes 做 `base64.b64encode`、ASCII 解码，得到只含 shell-safe 字符的单一 payload 参数；命令只使用固定的简单解码 wrapper 与该 payload，不把脚本正文放入 shell 引号。若 agent 内生成 payload，算法必须是：`payload = base64.b64encode(script.encode("utf-8")).decode("ascii")`；不得调用额外工具。也可直接调用已存在的只读标准库 entrypoint，但不得使用 heredoc 或复杂转义。

该脚本必须逐字节读取当前 PLAN/FULL；严格按 machine row 中冻结的 `terminal_newline_policy` 与 `marker_extraction_algorithm` 提取唯一 PLAN line 17 与 FULL line 21，逐字节计算 frozen SHA，并按唯一 JSON objects 执行 candidate、wrapper、required-subset、contract-exact、owner-binding 与 zero-budget audit。不得自行放宽 EOF terminal line 或把 missing-LF 解释为 PASS。

Executer 不得读取代码、测试、archive、旧 ER、controller、source、candidate、fixture、canonical content、release、retained R3、`.env` 或任何外部路径；不得自创 scanner、字段、别名、键值、谓词、补偿映射或通过条件。`required_subset_12` 与 `zero_budget_fields` 必须以上方 machine row 中唯一 JSON object 为唯一输入，逐键、逐值、逐类型比较；`required_subset_12.plan_sha=null` 是明确 self-hash 排除哨兵，PLAN SHA 只报告、不作 gate 比较；不得从自然语言推断、合并、展开或替换字段。

## 证据、预算与停止

- marker/strict-JSON/required-subset/owner gate 必须先于一切 `lexists`、`lstat`、mkdir、open、artifact 或其他 path operation；gate 结论前 path counter 必须为 `0/0`。
- artifact/path/test/Git/device/release/network/`.env`/camera/Ray/strip 全为 `0`；fallback/retry/reuse/rewrite/alternate/old-root/controller/source 全为 `0`，并与唯一 `zero_budget_fields` object 完全相等。
- 无论 PASS 或 FAIL，Executer 最多向 `.agent-work/EXECUTION_RESULT.md` append 一次，记录两份 raw SHA、candidate lines/count、12 项逐键结果、wrapper/contract/owner/zero-budget ledger、首次失败阶段、全部 zero counters 与 terminal 状态；append 后立即 stop。

**Planner stop：** 收到一次 ER 或明确 terminal handoff 后停止。PASS 仅表示离线 contract qualification，不是 bootstrap、release、R3、正式实验或设备授权。
