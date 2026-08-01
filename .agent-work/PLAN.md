# P7 retained-R3 Option B：B3-C3-C4-R1 repo-owned offline patch preflight owner

**计划状态：** `WAITING_ORCHESTRATOR_ACTIVATION`

**Planner 日期：** `2026-08-01`

**Reference task：** `REF-P7-25-R2-B3-C3-C4-R1`

**Contract：**
`P7-TD-B-RETAINED-R3-OPTION-B-B3-C3-C4-R1-OFFLINE-PATCH-PREFLIGHT-OWNER-V1`

**当前唯一动作：** 新增一个repo-owned、pure-offline PLAN/FULL machine-row preflight + canonical patch diagnostic owner及其dedicated tests；本包只实现、
测试并提交owner，不运行真实diagnostic。后续另起PLAN调用accepted stable entry。

**唯一 Planner stop：**
`B3_C3_C4_R1_OFFLINE_PATCH_PREFLIGHT_OWNER_WAITING_PLANNER_REVIEW`。

**本轮新归档：** `.agent-work/PLANS/20260801-0806-p7-retained-r3-b3-c3-c4-c2-incomplete-full-preflight-review.md`；bytes
`5123`，SHA-256 `57dd1e043c073fa98b8c89d739e1202eb1255bf5b5627b9232ada2bbf2b032c0`。

`PLAN_MACHINE_CONTRACT={"schema":"p7_td_b_retained_r3_option_b_b3_c3_c4_r1_offline_patch_preflight_owner_v1","reference_task_id":"REF-P7-25-R2-B3-C3-C4-R1","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B3-C3-C4-R1-OFFLINE-PATCH-PREFLIGHT-OWNER-V1","execution_authorized_after_orchestrator_activation":true,"reviewed_c2":{"activation":"aa87fad66463fcb50da92c22e0b45460f5a8ab20","evidence_commit":"9e865683b718d1954582bc6ca17489d4582572a4","decision":"REJECTED_PHASE1_FALSE_SUCCESS_PLAN_ONLY_FULL_AND_REQUIRED_SUBSET_OMITTED","phase1_plan_parse_successes":1,"phase1_full_parse_attempts":0,"required_full_subset_exact_performed":false,"phase2_invocations":0,"root_creates":0,"canonical_git_diff_invocations":0,"retry":0,"fallback":0},"activation_commit":{"expected_parent":"9e865683b718d1954582bc6ca17489d4582572a4","expected_subject":"chore(plan): activate offline patch preflight owner","expected_changed_paths":[".agent-work/FULL_PLAN_REFERENCE.md",".agent-work/PLAN.md",".agent-work/PLANS/20260801-0806-p7-retained-r3-b3-c3-c4-c2-incomplete-full-preflight-review.md"],"clean_porcelain_required_after_activation":true},"implementation_commit":{"expected_parent_source":"current_activation_head_runtime","expected_subject":"feat(p7): own offline patch preflight diagnostic","expected_changed_paths":["src/camera_based_rgbww_optimizer/utils/p7_retained_r3_offline_patch_preflight.py","tests/test_p7_retained_r3_offline_patch_preflight.py"],"single_commit":true,"clean_porcelain_required_after_commit":true},"exact_write_paths":["src/camera_based_rgbww_optimizer/utils/p7_retained_r3_offline_patch_preflight.py","tests/test_p7_retained_r3_offline_patch_preflight.py"],"owner_contract":{"module":"camera_based_rgbww_optimizer.utils.p7_retained_r3_offline_patch_preflight","exports":["OfflinePatchPreflightError","MachineRowPreflightResult","CanonicalPatchDiagnosticSpec","OfflinePatchPreflightResult","run_offline_patch_preflight"],"entrypoint":"run_offline_patch_preflight","inputs":["plan_bytes","full_bytes","diagnostic_spec"],"dependencies":["run_git"],"default_run_git":"p7_retained_r3_provenance_io.run_read_only_git","canonical_report_encoder":"p7_retained_r3_provenance_io.canonical_json_bytes","frozen_dataclasses":true,"pure_offline":true,"filesystem_writes":0,"external_root_operations":0,"network_device_capability":false,"validator_eligibility_authority":false},"machine_row_contract":{"plan_inner_prefix":"PLAN_MACHINE_CONTRACT=","full_inner_prefix":"FULL_PLAN_MACHINE_STATE=","boundary_algorithm":["len(row) >= 2","row[0] == '`'","row[-1] == '`'","inner = row[1:-1]","inner.startswith(expected_prefix)","payload = inner[len(expected_prefix):]"],"row_count_each":1,"internal_backtick_scans":0,"strip":false,"regex":false,"duplicate_keys_rejected":true,"nonfinite_rejected":true,"required_full_subset_exact":true,"git_calls_before_preflight_success":0},"patch_contract":{"helper_compatible_argv_prefix":["git","diff","--binary","--full-index","--no-ext-diff"],"parent_child_sha40":true,"separator":"--","paths_utf8_sorted_unique":true,"git_invocations":1,"shell":false,"classification_exact_match":"CANONICAL_PATCH_EXACT_MATCH","classification_output_mismatch":"CANONICAL_PATCH_OUTPUT_MISMATCH","classification_git_failure":"CANONICAL_PATCH_GIT_FAILURE","canonical_report_bytes":true,"persist":false},"stable_error_codes":["invalid_plan_bytes","invalid_full_bytes","machine_row_utf8_invalid","machine_row_cr_invalid","plan_row_count_invalid","full_row_count_invalid","machine_row_json_invalid","machine_row_duplicate_key","machine_row_nonfinite","required_full_state_invalid","required_full_subset_mismatch","diagnostic_spec_invalid","patch_argv_invalid","patch_expectation_invalid","git_result_invalid"],"test_contract":{"new_test_methods":10,"targeted_command":".venv/bin/python -m unittest tests.test_p7_retained_r3_offline_patch_preflight","targeted_expected":10,"focused_command":".venv/bin/python -m unittest tests.test_p7_retained_r3_provenance_io tests.test_p7_retained_r3_offline_patch_preflight","focused_expected":38,"compileall_command":".venv/bin/python -m compileall -q src tests","full_command":"PYTHONUNBUFFERED=1 .venv/bin/python -m unittest discover -s tests -p 'test_*.py'","full_baseline":800,"full_expected":810,"postcommit_targeted_expected":10},"codegraph_contract":{"pre_edit_sync":1,"pre_edit_query":1,"post_edit_sync":1,"post_edit_query":1,"sync_before_query":true,"query_before_source_test_read_or_edit":true},"execution_budgets":{"implementation_commits":1,"execution_result_appends":1,"test_invocations":4,"compileall_invocations":1,"codegraph_sync":2,"codegraph_queries":2,"retry":0,"fallback":0},"required_full_machine_state":{"active_task_count":1,"active_task":"REF-P7-25-R2-B3-C3-C4-R1","active_plan_contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B3-C3-C4-R1-OFFLINE-PATCH-PREFLIGHT-OWNER-V1","retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","manifest_authority":"SUBORDINATE_EVIDENCE_ONLY_CANONICAL_VALIDATOR_SOLE_ELIGIBILITY_OWNER","b3_c3_c4_status":"ACTIVE_OFFLINE_PATCH_PREFLIGHT_OWNER_IMPLEMENTATION","offline_patch_preflight_owner_status":"ACTIVE_IMPLEMENTATION","executer_dispatched":true,"device_authorized_by_this_file":false},"zero_budgets":{"third_code_test_path_writes":0,"p3_edits":0,"other_production_test_writes":0,"real_git_diagnostic_invocations":0,"external_root_operations":0,"failed_root_reads":0,"real_manifest_reads":0,"c1_input_reads":0,"retained_artifact_reads":0,"remaining_manifest_self_checks":0,"synthetic_runs":0,"actual_canonical_validator_calls":0,"canonical_validator_callbacks":0,"retained_release_audit":0,"eligibility_emissions":0,"release_generation":0,"release_qualification":0,"release_copy":0,"release_consumption":0,"network":0,"dns":0,"environment":0,"credentials":0,"device":0,"camera":0,"ray":0,"strip":0,"cleanup":0,"capture":0,"formal":0,"public_analyzer":0,"td_c":0,"sentinel":0,"p8":0,"firmware":0,"deployment":0,"plan_writes_by_executer":0,"full_writes_by_executer":0,"archive_writes_by_executer":0,"guide_writes":0,"research_writes":0},"expected_duration":"under_10_minutes","visible_terminal_required":false,"archive":{"path":".agent-work/PLANS/20260801-0806-p7-retained-r3-b3-c3-c4-c2-incomplete-full-preflight-review.md","bytes":5123,"sha256":"57dd1e043c073fa98b8c89d739e1202eb1255bf5b5627b9232ada2bbf2b032c0"},"planner_stop":"B3_C3_C4_R1_OFFLINE_PATCH_PREFLIGHT_OWNER_WAITING_PLANNER_REVIEW"}`

## 1. Activation与scope

Activation必须是`9e865683b718d1954582bc6ca17489d4582572a4`的direct child，subject/path set与machine row exact、porcelain clean。
Pre-edit CodeGraph sync/query必须先于source/test read/edit，确认P3 `canonical_json_bytes`与`run_read_only_git` contracts、new paths absent及baseline tests
P3=28/full=800；不符即edits/tests/commit0并single ER。

Exact write paths仅：

- `src/camera_based_rgbww_optimizer/utils/p7_retained_r3_offline_patch_preflight.py`；
- `tests/test_p7_retained_r3_offline_patch_preflight.py`。

不得编辑P3/P4/P5、real-manifest owner、FULL/GUIDE或增加CLI/controller/root framework。

## 2. Small owner API与reuse boundary

实现machine row冻结的5项exports与frozen dataclasses。`run_offline_patch_preflight(plan_bytes, full_bytes, diagnostic_spec, *,
dependencies=None)`必须先完整解析PLAN与FULL、验证required subset，再调用`run_git` exact一次；preflight任何failure时Git calls0。

Parser严格使用固定首尾索引、`row[1:-1]`与inner prefix；内部backtick不扫描。Strict UTF-8、无CR、row count1/1、duplicate/nonfinite rejection及
required FULL exact subset全部属于同一owner，不允许caller跳过FULL。

Patch argv必须是P3 `run_read_only_git`已allowlist的
`git diff --binary --full-index --no-ext-diff <parent> <child> -- <sorted unique paths>`；旧one-off缺flag argv不进入owner。Default runner直接复用
`run_read_only_git`，report bytes直接复用`canonical_json_bytes`；不得复制generic Git runner或canonical serializer。Owner只返回immutable typed result与
canonical report bytes，不persist、不建root、无external/device/validator/eligibility能力。

## 3. Dedicated tests与validation

Dedicated exact10 methods覆盖：exports/frozen fields；valid PLAN+FULL/subset；embedded backticks不扫描；UTF-8/CR/row count；duplicate/nonfinite；missing或
mismatched FULL subset且Git0；spec/hash/argv fail closed；exact Git match；output mismatch/Git failure；canonical report/no-I/O并验证run_git exact once。

验证顺序各exact一次：targeted10、focused38、compileall、full810、post-edit CodeGraph sync/query、`git diff --check`、exact two-path commit
`feat(p7): own offline patch preflight diagnostic`、postcommit targeted10。任一失败立即停，不retry/fallback/second commit；single ER EOF append记录topology、
API、tests、CodeGraph、blobs/patch与locks。

## 4. Locks

本实现包真实Git diagnostic、external roots/failed roots、real manifest/C1/retained、remaining checks/synthetic、validator/audit/eligibility/release、network/device/
science/firmware/deployment全部0。Retained R3保持`RETAINED_UNVALIDATED_UNCONSUMED`。无Advisor或Human授权需求。

维护性判断：两路径owner将重复失败的parser+diagnostic收敛为单一typed、专测边界，并复用P3 canonical JSON/Git helpers；接受后下一包只调用稳定入口。
