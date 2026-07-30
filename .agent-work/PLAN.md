# REF-P7-25-R2-B1A-C3E6F17-CORRECTIVE-12：byte-exact scanner 纠偏

**计划状态：** `planner_corrective_waiting_orchestrator_activation`

**Planner 日期：** `2026-07-29`

**Reference task：** `REF-P7-25-R2-B1A-C3E6F17-CORRECTIVE-12`

**Parent reviewed task：** `REF-P7-25-R2-B1A-C3E6F17-CORRECTIVE-11`

**active_plan_contract_id：** `P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F17-CORRECTIVE-12`

**当前只读 FULL SHA-256：** `d089f4b604a9d0307798c4a84f3b63610e13b2364f93e5aace163cafa2a287b6`；其 owner 仍为 C11，故 C12 pre-dispatch lock 尚未解除。Orchestrator 必须先唯一激活 C12，随后 Planner 再冻结更新后的 exact FULL SHA。

**C11 review archive：** `.agent-work/PLANS/20260730-0143-p7-retained-r3-option-b-b1a-c3e6f17-corrective-11-review.md`；SHA-256 `0614be22ca09cbe807e5c32dd7ab8e0ca43e6559e2f2e501a68e2b7615e41056`。

`PLAN_MACHINE_CONTRACT={"schema":"planner_execution_contract_v1","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F17-CORRECTIVE-12","task_id":"REF-P7-25-R2-B1A-C3E6F17-CORRECTIVE-12","parent_reference_task_id":"REF-P7-25-R2-B1A-C3E6F17-CORRECTIVE-11","package_kind":"bounded_offline_byte_exact_scanner_qualification_only","single_current_action":"after_orchestrator_activation_run_one_ascii_base64_wrapped_python_qualification_then_append_execution_result_at_most_once_and_stop","dispatch_lock":"blocked_until_orchestrator_activates_c12_and_planner_refreshes_exact_full_sha","expected_full_sha256":null,"input_owner_binding":{"plan_absolute_path":"/Users/ibobby/Projects/WLED-RGBWW/.agent-work/PLAN.md","full_absolute_path":"/Users/ibobby/Projects/WLED-RGBWW/.agent-work/FULL_PLAN_REFERENCE.md","raw_byte_buffer_count":2,"plan_lines_origin":"plan_raw.splitlines_keepends_true_only","full_lines_origin":"full_raw.splitlines_keepends_true_only","cross_owner_assignment":false,"qualification_input_reads":2},"byte_exact_scanner":{"plan_marker_ascii":"`PLAN_MACHINE_CONTRACT=","full_marker_ascii":"`FULL_PLAN_MACHINE_STATE=","accepted_suffix_hex":"600a","reject_crlf":true,"reject_eof_without_lf":true,"candidate_predicate":"raw.startswith(marker) and raw.endswith(b'`\\n') and not raw.endswith(b'`\\r\\n')","json_slice":"raw[len(marker):-2]","json_loader":"json.loads_bytes_slice_must_return_dict","line_number_is_evidence_only":true,"presentation_text_is_not_candidate":true,"aliases_forbidden":true,"candidate_count":{"plan":1,"full":1}},"field_owner_contract":{"plan_fields_source":"unique_plan_object_only","full_fields_source":"unique_full_object_only","plan_zero_budget_source":"unique_plan_object.zero_budget_fields_only","compare_value_and_json_type":true},"required_subset_12":{"plan_sha":null,"full_sha":null,"plan_candidate_count":1,"full_candidate_count":1,"task_id":"REF-P7-25-R2-B1A-C3E6F17-CORRECTIVE-12","active_task":"REF-P7-25-R2-B1A-C3E6F17-CORRECTIVE-12","active_plan_contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F17-CORRECTIVE-12","retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","candidate_contract_orchestrator_verified":true,"artifact_operations":0,"path_operations":0,"execution_result_append_cap":1},"zero_budget_fields":{"artifact_operations":0,"path_operations":0,"fallback":0,"retry":0,"reuse":0,"rewrite":0,"alternate_path":0,"old_root_touch":0,"controller_access":0,"source_access":0,"test_execution":0,"git_mutation":0,"release_access":0,"network_access":0,"env_access":0,"device_access":0,"camera_access":0,"ray_access":0,"strip_access":0},"encoding_transport":{"python_source_ascii_only":true,"manual_pure_js_base64":true,"python_c_payload_count":1,"heredoc":false,"template_literal":false,"text_encoder":false,"node_buffer":false,"dispatcher":false,"fallback":false,"retry":false},"gate_before_path_operations":true,"execution_result_append_cap":1,"append_once_on_gate_pass_or_fail":true,"planner_stop_required":true}`

## 唯一 current action（C12 激活后仅离线 qualification）

当前不得 dispatch。Orchestrator 先把 FULL 的唯一 machine row、header 与状态说明激活为 C12；Planner 再只刷新本 PLAN 的 FULL SHA header、`expected_full_sha256`、`required_subset_12.full_sha` 与 dispatch lock。任何其他 role 都不得编辑 FULL。

解除 lock 后，Executer 只可用一次已经证明可启动的纯 ASCII manual-JS-base64 → 单 payload `python -c` wrapper。Python source 分别逐字节读取两个冻结绝对路径到两个独立 raw buffers，并分别调用 `splitlines(keepends=True)`；不得复用 owner、不得读 line number 代替扫描、不得使用 decode 后的模糊文本匹配。

scanner 必须逐字节执行 machine row 中冻结的 predicate：marker 自身包含起始 backtick；合法 raw line 必须 exact 以 backtick+LF 结束且不是 CRLF；JSON bytes 只能取 `raw[len(marker):-2]`。PLAN 和 FULL 必须各得到唯一 dict object。随后才可按 owner 验证 required subset 12/12 与 PLAN-owned zero budget 19/19。

## Evidence、预算与停点

- gate 前除两份冻结 input read 外，artifact/path/controller/source/test/Git/release/R3/network/`.env`/device/camera/Ray/strip 均为 `0`；fallback/retry/reuse/rewrite/alternate/old-root 也为 `0`。
- PASS/FAIL 最多 append `EXECUTION_RESULT.md` 一次，记录 raw SHA、候选 raw line hex/line/count、两个 owner object 的字段来源、12/19逐项结果、首次失败与全部 zero counters；随后立即停止。
- 若 wrapper 在 Python 启动前失败，ER append 为 `0` 并 terminal handoff；不得 fallback/retry。

**Planner stop：** 收到一次 ER 或明确 terminal handoff 后停止。C12 PASS 不授权 bootstrap、retained R3、release、eligibility、formal 或任何设备操作。
