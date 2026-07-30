# REF-P7-25-R2-B1A-C3E6F18-CORRECTIVE-1：Repo-local import 与 terminal-evidence owner 纠偏

**计划状态：** `PLANNER_REVIEW_COMPLETE_WAITING_ORCHESTRATOR_ACTIVATION`

**Planner 日期：** `2026-07-30`

**Reference task：** `REF-P7-25-R2-B1A-C3E6F18-CORRECTIVE-1`

**active_plan_contract_id：** `P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F18-CORRECTIVE-1`

**Reviewed package archive：** `.agent-work/PLANS/20260730-0234-p7-retained-r3-option-b-b1a-c3e6f18-import-failure-review.md`；SHA-256 `732a279e908e26ad7b397b55d16e39527a0bedcffae1460245c82c8b79a31dd3`。

**Planner decision：** F18 bootstrap `REJECTED_IMPORT_OWNER_AND_TERMINAL_EVIDENCE_CONTRACT`。唯一Python进程在helper import处以`ModuleNotFoundError`终止；helper parse、Git preflight、四外置路径检查/创建、fallback、ER append均为0，所有R3/release/network/device等hard lock均为0。

`PLAN_MACHINE_CONTRACT={"schema":"planner_execution_contract_v2","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F18-CORRECTIVE-1","task_id":"REF-P7-25-R2-B1A-C3E6F18-CORRECTIVE-1","parent_reference_task_id":"REF-P7-25-R2-B1A-C3E6F18","package_kind":"single_offline_fixed_container_bootstrap_import_terminal_corrective","dispatch_lock":"waiting_orchestrator_full_activation_and_planner_rebind","single_current_action":"after_activation_one_python_process_establishes_terminal_writer_imports_committed_helper_via_frozen_repo_src_runs_all_preflight_then_bootstraps_once_and_stops","review_archive":{"path":".agent-work/PLANS/20260730-0234-p7-retained-r3-option-b-b1a-c3e6f18-import-failure-review.md","sha256":"732a279e908e26ad7b397b55d16e39527a0bedcffae1460245c82c8b79a31dd3"},"activation_binding":{"orchestrator_full_activation_required":true,"expected_full_sha256":null,"dispatch_head":null,"dispatch_parent":null,"allowed_dispatch_status":{"staged_paths":[],"unstaged_paths":[],"untracked_paths":[]}},"source_binding":{"repo_root":"/Users/ibobby/Projects/WLED-RGBWW","repo_src":"/Users/ibobby/Projects/WLED-RGBWW/src","plan_absolute_path":"/Users/ibobby/Projects/WLED-RGBWW/.agent-work/PLAN.md","full_absolute_path":"/Users/ibobby/Projects/WLED-RGBWW/.agent-work/FULL_PLAN_REFERENCE.md","execution_result_absolute_path":"/Users/ibobby/Projects/WLED-RGBWW/.agent-work/EXECUTION_RESULT.md","independent_plan_full_buffers":true},"machine_contract_helper":{"module":"camera_based_rgbww_optimizer.utils.agent_work_machine_contract","path":"src/camera_based_rgbww_optimizer/utils/agent_work_machine_contract.py","absolute_path":"/Users/ibobby/Projects/WLED-RGBWW/src/camera_based_rgbww_optimizer/utils/agent_work_machine_contract.py","blob_oid":"5c581f9b502bcab1809b6a61a082a47f4150e09f","sha256":"743e2948f6c30a31fde5d072c8effa8b1365d321b303d61e9899ad18ac41825f","import_owner":"insert_frozen_repo_src_at_sys_path_index_0_once_then_import_exact_package_module_and_verify_module_file","plan_function":"parse_plan_machine_contract","full_function":"parse_full_plan_machine_state","plan_calls":1,"full_calls":1,"manual_or_copied_scanner_calls":0,"source_loader_alias_calls":0,"fallback_parser_calls":0,"payload_repairs":0},"terminal_evidence":{"writer_owner":"stdlib_only_single_use_er_append_writer_established_before_helper_import","post_writer_ready_pass_append":1,"post_writer_ready_fail_append":1,"append_cap":1,"strict_single_line_json":true,"outer_exception_boundary":"all_stages_after_writer_ready","pre_payload_or_pre_writer_failure_evidence":"execution_tool_terminal_only_er_append_not_claimed","no_second_command":true},"external_paths":{"parent":"/Volumes/4T/temp/rgbww-optimizer","container":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b1a-c3e6f18-offline","record":"/Volumes/4T/temp/rgbww-optimizer/c3e6f18-container-bootstrap.json","seal":"/Volumes/4T/temp/rgbww-optimizer/c3e6f18-container-bootstrap.seal.json","fallback":"/Volumes/4T/temp/rgbww-optimizer/c3e6f18-container-bootstrap.fallback.json","exact_allowed_new_path_count":4,"alternate_paths":0,"all_four_must_be_absent_before_first_create":true},"preflight_order":["terminal_writer_ready","independent_plan_full_read","repo_src_insert_and_exact_module_import","helper_identity","helper_parse_once_per_owner","plan_full_contract","git_lineage_and_clean_status","parent_and_four_path_gate","bootstrap"],"call_budget":{"functions_exec_calls":1,"exec_command_calls":1,"python_invocations":1,"additional_python_invocations":0,"controller_processes":0,"controller_invocations":0,"test_runner_invocations":0,"retry":0},"success_operation_budget":{"container_create_attempt":1,"container_create_succeeded":1,"record_create_attempt":1,"record_create_succeeded":1,"seal_create_attempt":1,"seal_create_succeeded":1,"fallback_create_attempt":0,"fallback_create_succeeded":0,"execution_result_append":1},"failure_operation_caps":{"container_create_attempt":1,"record_create_attempt":1,"seal_create_attempt":1,"fallback_create_attempt":1,"execution_result_append":1,"repair":0,"delete":0,"reuse":0,"rewrite":0,"alternate_path":0,"retry":0},"zero_locks":{"retained_r3_access":0,"candidate_materialization":0,"old_release_access":0,"new_release_access":0,"manifest_access":0,"consumer_access":0,"canonical_validator_calls":0,"eligibility_emissions":0,"controller_source_access":0,"clone":0,"fixture_or_canonical_content_access":0,"tests":0,"network":0,"dns":0,"env":0,"credential":0,"device":0,"camera":0,"ray":0,"strip":0,"cleanup":0,"capture":0,"public_analyzer":0,"formal":0,"td_c":0,"sentinel":0,"p8":0,"firmware":0,"deployment":0,"git_mutation":0},"planner_stop_required":true}`

## 当前唯一动作与 activation lock

当前不得 dispatch Executer。Orchestrator须先把FULL的唯一active task/contract更新为本C1，保留`RETAINED_UNVALIDATED_UNCONSUMED`与candidate verification，再交Planner冻结更新后的FULL SHA、clean dispatch lineage和实际执行合同。FULL未激活、PLAN未rebind前，不得运行Python、import helper、检查外置路径或进入bootstrap。

## 纠偏后的唯一执行 owner

激活后的Executer仍只可使用一个`functions.exec`、一个`exec_command`和一个`.venv/bin/python -c`进程。Python source只使用标准库；不得heredoc、第二Python、dispatcher、controller、test runner、Codex CLI、shell cleanup或retry。

Python payload启动后，先建立single-use ER writer及outer terminal boundary，再执行任何helper import。随后将冻结的绝对`/Users/ibobby/Projects/WLED-RGBWW/src`恰好一次插入`sys.path[0]`，按完整模块名import committed helper，并验证模块`__file__`、Git blob及working SHA与冻结值一致。不得复制helper源码/scanner，不得用`spec_from_file_location`、source loader、editable-install猜测、alias、fallback parser或payload repair。

writer ready后的任一import/source/helper/Git/bootstrap PASS或FAIL都必须最多且恰好append一条single-line strict JSON ER terminal row，然后stop。对于Python payload根本未启动或writer尚未成功建立的failure，PLAN不再虚假保证ER append；唯一证据owner是execution tool terminal，且仍禁止第二command、fallback或retry。

## Preflight-before-path 与 fixed bootstrap

只有terminal writer、独立PLAN/FULL buffers、exact helper import/identity、helper各一次parse、激活后合同及Git clean-lineage全部通过，才可首次`lstat` parent及四条冻结路径。此前外置path check/create/fallback必须均为0。

四条路径继续复用F18冻结名称，因为本次独立review确认它们仍absent；这不是旧执行retry。通过全部preflight后，filesystem语义保持原F18合同：四路径absence gate、single `os.mkdir(0700)`、container lstat/fstat/empty/fsync、record与seal各一次`O_CREAT|O_EXCL 0600` deterministic strict JSON/reload/fsync；absence gate后发生的failure才可尝试一次fixed fallback。禁止历史root、alternate path、delete、repair、reuse或rewrite。

## Acceptance、failure branch与stop

PASS只接受“唯一fresh empty fixed container及immutable record/seal prerequisite建立成功，ER terminal row恰1”。它不授权candidate、retained R3、manifest、canonical validator、eligibility、consumer、release、network、device、FORMAL或B2。

FAIL保留现场并停止；不得补写、修复、删除、改路径、第二次probe或retry。Planner独立只读验收terminal evidence；工程失败回Orchestrator，仅真正科学矛盾才回Advisor。

**Planner stop：** `C3E6F18_CORRECTIVE_1_WAITING_ORCHESTRATOR_ACTIVATION`。

**维护性判断：** 本纠偏不新增parser或filesystem owner，只把src-layout import和terminal append边界明确归属同一个单进程payload；复杂度局部且无需生产重构。
