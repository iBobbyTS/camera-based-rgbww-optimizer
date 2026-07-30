# REF-P7-25-R2-B1A-C3E6F18：Clean-dispatch committed-helper fixed-container bootstrap prerequisite

**计划状态：** `ACTIVE_DISPATCH_READY_SINGLE_OFFLINE_BOOTSTRAP`

**Planner 日期：** `2026-07-30`

**Reference task：** `REF-P7-25-R2-B1A-C3E6F18`

**active_plan_contract_id：** `P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F18-BOOTSTRAP-PREREQUISITE`

**Reviewed parent task：** `REF-P7-25-R2-B1A-C3E6F17-C13-LINEAGE-SEAL`

**Lineage-seal review archive：** `.agent-work/PLANS/20260730-0219-p7-retained-r3-option-b-b1a-c3e6f17-c13-lineage-seal-review.md`；SHA-256 `d6d8a47a0a60e06e7a4048dd7ae729e3952075031fe82858e358cf29a87319fb`。

**Clean-dispatch repository anchor：** corrective commit 的 direct parent 必须为当前 activation HEAD `686c4d0d816d0c77fbde8653f13d9759c3b5f4be`，exact changed path 只能是 `.agent-work/PLAN.md`，commit subject 必须为 `chore(plan): bind f18 clean dispatch lineage`。corrective child SHA 不在 PLAN 中预知或冻结；Executer 必须从实际 dispatch HEAD 读取并记录。dispatch 时 staged、unstaged、untracked path 必须全部为空。

**Activation input identities：** current read-only FULL SHA-256 `2fbf160c15d865ef254c6100d013812cbdc0ccf291cc67e7f38e7b7665cd4292`。PLAN SHA 字段固定为 `null`，其 raw SHA 由 Executer 在 clean dispatch 时从唯一 PLAN buffer独立计算并写入 terminal evidence；不得建立自哈希等式。helper 的 committed blob/SHA 保持冻结。

`PLAN_MACHINE_CONTRACT={"schema":"planner_execution_contract_v2","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F18-BOOTSTRAP-PREREQUISITE","task_id":"REF-P7-25-R2-B1A-C3E6F18","parent_reference_task_id":"REF-P7-25-R2-B1A-C3E6F17-C13-LINEAGE-SEAL","package_kind":"single_offline_fixed_container_bootstrap_prerequisite","dispatch_lock":"released_by_planner_after_orchestrator_full_activation","single_current_action":"one_functions_exec_containing_one_exec_command_and_one_python_invocation_runs_preflight_bootstrap_terminal_evidence_er_append_then_stops","repository_identity":{"dispatch_head":null,"dispatch_head_runtime_evidence_required":true,"direct_parent":"686c4d0d816d0c77fbde8653f13d9759c3b5f4be","head_subject":"chore(plan): bind f18 clean dispatch lineage","head_changed_paths":[".agent-work/PLAN.md"],"seal_commit":"64c34ade850aecd8c3aefb78358c7e66fcc4de88","seal_direct_parent":"fd1fe095f59b9accf008c95eeba73fbf6e778030","seal_commit_must_be_ancestor":true,"allowed_dispatch_status":{"staged_paths":[],"unstaged_paths":[],"untracked_paths":[]}},"source_binding":{"plan_absolute_path":"/Users/ibobby/Projects/WLED-RGBWW/.agent-work/PLAN.md","full_absolute_path":"/Users/ibobby/Projects/WLED-RGBWW/.agent-work/FULL_PLAN_REFERENCE.md","plan_sha256":null,"runtime_plan_sha256_evidence_required":true,"expected_full_sha256":"2fbf160c15d865ef254c6100d013812cbdc0ccf291cc67e7f38e7b7665cd4292","raw_byte_buffer_count":2,"cross_owner_buffer_reuse":false},"machine_contract_helper":{"path":"src/camera_based_rgbww_optimizer/utils/agent_work_machine_contract.py","blob_oid":"5c581f9b502bcab1809b6a61a082a47f4150e09f","sha256":"743e2948f6c30a31fde5d072c8effa8b1365d321b303d61e9899ad18ac41825f","plan_function":"parse_plan_machine_contract","full_function":"parse_full_plan_machine_state","plan_calls":1,"full_calls":1,"manual_or_copied_scanner_calls":0,"fallback_parser_calls":0,"payload_repairs":0},"full_required_fields":{"active_task":"REF-P7-25-R2-B1A-C3E6F18","active_plan_contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F18-BOOTSTRAP-PREREQUISITE","retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","candidate_contract_orchestrator_verified":true,"executer_dispatched":false},"external_paths":{"parent":"/Volumes/4T/temp/rgbww-optimizer","container":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b1a-c3e6f18-offline","record":"/Volumes/4T/temp/rgbww-optimizer/c3e6f18-container-bootstrap.json","seal":"/Volumes/4T/temp/rgbww-optimizer/c3e6f18-container-bootstrap.seal.json","fallback":"/Volumes/4T/temp/rgbww-optimizer/c3e6f18-container-bootstrap.fallback.json","exact_allowed_new_path_count":4,"alternate_paths":0,"all_four_must_be_absent_before_first_create":true},"call_budget":{"functions_exec_calls":1,"exec_command_calls":1,"python_invocations":1,"additional_python_invocations":0,"controller_processes":0,"controller_invocations":0,"test_runner_invocations":0,"retry":0},"success_operation_budget":{"container_create_attempt":1,"container_create_succeeded":1,"record_create_attempt":1,"record_create_succeeded":1,"seal_create_attempt":1,"seal_create_succeeded":1,"fallback_create_attempt":0,"fallback_create_succeeded":0,"execution_result_append":1},"failure_operation_caps":{"container_create_attempt":1,"record_create_attempt":1,"seal_create_attempt":1,"fallback_create_attempt":1,"execution_result_append":1,"repair":0,"delete":0,"reuse":0,"rewrite":0,"alternate_path":0,"retry":0},"filesystem_contract":{"parent_existing_regular_directory_non_symlink":true,"container_create":"single_os_mkdir_mode_0700","container_identity":"absolute_path_lstat_open_directory_fd_fstat_mode_uid_gid_dev_inode_empty","record_create":"O_CREAT_O_EXCL_mode_0600","seal_create":"O_CREAT_O_EXCL_mode_0600","fallback_create":"O_CREAT_O_EXCL_mode_0600_only_after_parent_and_four_path_absence_gate","json":"deterministic_utf8_strict_duplicate_key_and_nonfinite_rejecting_reload","fsync":["container","record","seal_or_fallback","parent_after_each_create"],"preserve_on_failure":true},"evidence_contract":{"record_schema":"p7_td_b_c3e6f18_container_bootstrap_record_v1","seal_schema":"p7_td_b_c3e6f18_container_bootstrap_seal_v1","fallback_schema":"p7_td_b_c3e6f18_container_bootstrap_failure_v1","execution_result_schema":"p7_td_b_c3e6f18_container_bootstrap_terminal_v1","record_seal_fallback_raw_bytes_and_sha256":true,"first_failure_stage_and_reasons":true,"operation_counters":true,"planner_stop":true},"zero_locks":{"retained_r3_access":0,"candidate_materialization":0,"old_release_access":0,"new_release_access":0,"manifest_access":0,"consumer_access":0,"canonical_validator_calls":0,"eligibility_emissions":0,"controller_source_access":0,"clone":0,"fixture_or_canonical_content_access":0,"tests":0,"network":0,"dns":0,"env":0,"credential":0,"device":0,"camera":0,"ray":0,"strip":0,"cleanup":0,"capture":0,"public_analyzer":0,"formal":0,"td_c":0,"sentinel":0,"p8":0,"firmware":0,"deployment":0,"git_mutation":0},"execution_result_append_cap":1,"append_on_pass_or_fail":true,"planner_stop_required":true}`

## Planner activation decision

Orchestrator 已将 FULL 的唯一 machine row 激活到 C3E6F18，FULL task/contract、retained lock 与 candidate contract verification 均与上方 strict machine contract一致；Planner解除 pre-dispatch lock。唯一授权动作是建立一次 empty、sealed、fixed-container prerequisite。PASS不产生candidate、eligibility或release权限。

Executer 的首个 execution tool call必须也是本包唯一 execution tool call：一个 `functions.exec`，内部恰好一个 `exec_command`；该command恰好启动一次 repository `.venv/bin/python -c`，运行一份纯Python标准库source。不得使用Codex CLI、二级dispatcher、heredoc、另一个Python、test runner、controller或shell cleanup。命令构造失败、Python未启动或任一gate失败均不得fallback command或retry。

## Frozen source、helper与Git gate

1. 分别以两个独立 `Path.read_bytes()` buffer读取绝对PLAN与FULL；不得跨owner复用或从prose推导字段。
2. 从已提交helper import `parse_plan_machine_contract`与`parse_full_plan_machine_state`，对对应buffer各调用恰好一次。不得手写、复制、包装第二套scanner，不得alias/fallback parse或repair payload。helper返回的owner、candidate count/lines、source/raw-row/payload bytes与SHA必须完整保留。
3. PLAN对象必须逐键逐类型匹配本合同；FULL source SHA必须等于 `2fbf...4292`，FULL对象的active task/contract、retained status、verification与dispatch flag必须匹配冻结值。PLAN machine contract中的`plan_sha256`必须为JSON `null`；PLAN raw SHA只由dispatch buffer计算并记录，避免自引用。
4. 只读Git gate必须从实际dispatch HEAD证明：其direct parent恰为 `686c4d0d816d0c77fbde8653f13d9759c3b5f4be`、exact changed path仅 `.agent-work/PLAN.md`、subject恰为 `chore(plan): bind f18 clean dispatch lineage`，且HEAD中的PLAN内容与working-tree PLAN raw bytes一致；同时证明seal commit ancestry、helper blob与working file SHA完全匹配冻结值。实际child SHA只作为runtime evidence记录，不在PLAN中预知。dispatch时staged、unstaged、untracked path必须全部为空；Git mutation为0。
5. 任何source/helper/Git gate失败发生在外置path operation之前：不得检查四条外置路径，不得创建fallback，只append一次ER terminal row后停止。

## Exact four-path bootstrap

只允许接触machine contract冻结的parent与四条新路径。禁止探测、读取、删除或复用任何F14/F15/F16/F17或其他历史root/evidence。

1. 先以`lstat`证明parent是existing regular directory且non-symlink，再证明四条路径全部absent。存在、symlink或检查错误均fail closed；不得读取存在对象内容。
2. 只以一次`os.mkdir(container, mode=0o700)`创建container，禁止parents/mkdir-p。以absolute path、`lstat`及open directory fd的`fstat`冻结mode、uid、gid、dev、inode并证明empty；fsync directory fd与parent。
3. record以`O_CREAT|O_EXCL`、mode `0600`创建，写deterministic UTF-8 strict JSON、fsync file/parent、strict reload并记录raw bytes/SHA。record绑定source/helper/Git gates、四路径preflight、container identity与当时counters。
4. seal以同样exclusive/0600/deterministic/reload/fsync规则创建，绑定record bytes/SHA、再次确认的container lstat/fstat identity与emptiness、全部counter及hard locks。
5. 任一失败只能在parent与四路径absence gate已成功后尝试一次fixed fallback；fallback同样exclusive/0600/strict/reload/fsync，记录真实阶段、原因、已发生操作、保留现场及所有未发生项。若absence gate本身未通过，fallback attempt必须为0。
6. 不论PASS/FAIL，最后最多向 `.agent-work/EXECUTION_RESULT.md` append一条single-line strict JSON terminal evidence；append后立即Planner stop。ER不得改写既有内容。

## Required terminal evidence

record、seal/fallback与ER必须覆盖：schema、UTC、terminal status、first failure；task/contract；PLAN/FULL raw bytes/SHA与helper两份parse evidence；dispatch HEAD/direct parent/changed paths/status、seal ancestry、helper committed path/blob/SHA；四条exact path与pre/post identity、mode/uid/gid/dev/inode/emptiness/fsync；record/seal/fallback bytes/SHA与strict reload；全部attempt/succeeded counter；`RETAINED_UNVALIDATED_UNCONSUMED`、canonical validator `0`、eligibility `0`及全部hard locks；`planner_stop=true`。

## Acceptance、failure branch与stop

PASS仅接受“一个全新empty fixed container及其immutable record/seal prerequisite已创建”。它不授权后继controller、candidate、retained R3 audit、manifest、canonical validator、consumer、release或设备工作。Planner必须独立只读审查外置evidence、ER、identity与预算。

FAIL保留现场并停止；不得删除、修复、改路径、重跑或进入后继。工程纠偏回Orchestrator；仅真正的色彩/测量科学矛盾才回Advisor。

**Planner stop：** `C3E6F18_TERMINAL_EVIDENCE_READY_FOR_PLANNER_REVIEW`。

**维护性判断：** 本包强制复用唯一committed pure-bytes helper，filesystem bootstrap仍是单次外置执行owner；没有新增production、eligibility或release owner。
