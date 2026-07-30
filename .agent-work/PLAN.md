# REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-8：validation log single-owner corrective

**计划状态：** `ACTIVE_EXECUTABLE_WAITING_ONE_FRESH_EXECUTER_AFTER_ORCHESTRATOR_ACTIVATION_COMMIT`

**Planner 日期：** `2026-07-30`

**Reference task：** `REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-8`

**Contract ID：** `P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F19-CORRECTIVE-8-LOG-OWNER`

**唯一当前动作：** Orchestrator 以本 PLAN 冻结的 exact subject 创建唯一 PLAN-only activation commit；随后唯一
fresh Executer 复用已接受的 C7 pre-gates 与已提交 source/test bytes，在 fresh C8 root 中以每个 validation log
唯一 exclusive-open fd 直接承接 child stdout/stderr，运行一次完整 fail-fast validation chain，最后 seal terminal 并
append 一条显式 supersede C7 ER 错记的结果。不得重跑 C7 pre-gates、读取 C2-C7 其他 payload 或修改 repo 文件。

**C7 review archive：**
`.agent-work/PLANS/20260729-2310-p7-retained-r3-option-b-b1a-c3e6f19-corrective-7-review.md`；
SHA-256 `6a7a2bc3467c5b63b634578b5a14252efffa4557f32d9ff65fbeb420dcf0a424`。

`PLAN_MACHINE_CONTRACT={"schema":"f19_corrective_8_validation_log_single_owner_activation_v1","reference_task_id":"REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-8","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F19-CORRECTIVE-8-LOG-OWNER","dispatch_state":"dispatchable_one_fresh_executer_after_orchestrator_exact_activation_commit","single_current_action":"preserve_committed_baseline_then_run_one_fresh_single_fd_fail_fast_validation_chain_and_supersede_c7_er_discrepancy","review_archive":{"path":".agent-work/PLANS/20260729-2310-p7-retained-r3-option-b-b1a-c3e6f19-corrective-7-review.md","sha256":"6a7a2bc3467c5b63b634578b5a14252efffa4557f32d9ff65fbeb420dcf0a424"},"activation_commit":{"required_direct_parent":"2d817465dbd0974d2cc455f7b99be79f1e62bab4","pre_activation_current_head":"2d817465dbd0974d2cc455f7b99be79f1e62bab4","pre_activation_porcelain_clean":true,"exact_changed_paths":[".agent-work/PLAN.md"],"exact_plan_path":"/Users/ibobby/Projects/WLED-RGBWW/.agent-work/PLAN.md","exact_subject":"chore(plan): activate f19 validation log owner correction","actual_child_owner":"runtime_git_rev_parse_HEAD_full_sha_after_orchestrator_activation_commit","actual_child_requirements":{"full_40_char":true,"not_equal_parent":true,"direct_parent_equals_required_direct_parent":true,"subject_equals_exact_subject":true,"changed_paths_equal_exact_changed_paths":true,"clean_porcelain":true},"committed_plan":{"path":".agent-work/PLAN.md","absolute_path":"/Users/ibobby/Projects/WLED-RGBWW/.agent-work/PLAN.md","blob_owner":"runtime_git_rev_parse_HEAD_colon_exact_plan_path","sha256_owner":"runtime_sha256_of_committed_plan_blob","worktree_must_equal_committed_blob":true},"self_referential_expected_child_blob_or_plan_sha_forbidden":true},"frozen_full":{"path":".agent-work/FULL_PLAN_REFERENCE.md","absolute_path":"/Users/ibobby/Projects/WLED-RGBWW/.agent-work/FULL_PLAN_REFERENCE.md","blob_oid":"df4c29410baff06858abcbac511da999b9c7ce82","sha256":"613c62174f1c01f2ec37064acb0b2832aee1ab98516a34816b8622b00d59fffd"},"required_aligned_full_state":{"active_task_count":1,"active_task":"REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-8","active_plan_contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F19-CORRECTIVE-8-LOG-OWNER","repair_v2_status":"B1A_C3E6F19_CORRECTIVE_7_REJECTED_LOG_NOCLOBBER_REOPEN_CORRECTIVE_8_ACTIVE","retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","candidate_machine_contract_sha256":"3c5847fcbe0af85833c901f6f01058d000a3cecdc0f84e6ae331ed24e138c225","candidate_contract_orchestrator_verified":true,"executer_dispatched":false},"machine_contract_helper":{"path":"src/camera_based_rgbww_optimizer/utils/agent_work_machine_contract.py","blob_oid":"5c581f9b502bcab1809b6a61a082a47f4150e09f","bytes":7230,"sha256":"743e2948f6c30a31fde5d072c8effa8b1365d321b303d61e9899ad18ac41825f","plan_api":"parse_plan_machine_contract","full_api":"parse_full_plan_machine_state","plan_api_calls":1,"full_api_calls":1,"direct_import_from_committed_helper":true,"independent_scanner_alias_fallback_inference_or_payload_repair_count":0},"committed_baseline":{"controller":{"path":"src/camera_based_rgbww_optimizer/utils/p7_retained_r3_exact_five_controller.py","blob_oid":"45097745bcc48aa1312b06fc07c6c910a4529325","bytes":13477,"sha256":"746fd13056c326489b48ca555b21618b65c8a78f198d035e18c02f68af689726","preserve_byte_exact":true},"helper":{"path":"src/camera_based_rgbww_optimizer/utils/agent_work_machine_contract.py","blob_oid":"5c581f9b502bcab1809b6a61a082a47f4150e09f","bytes":7230,"sha256":"743e2948f6c30a31fde5d072c8effa8b1365d321b303d61e9899ad18ac41825f","preserve_byte_exact":true},"dedicated_test":{"path":"tests/test_p7_retained_r3_exact_five_controller.py","blob_oid":"f871951645af6ef6fb51e49cda09dad43eb90b2b","bytes":15835,"sha256":"19858a64fb760c112783b176822e7dabf72dce1b0cf9fb21e3a4738b83cebc3d","preserve_byte_exact":true}},"accepted_c7_prerequisites":{"source":"immutable_c7_terminal_and_planner_review","activation_helper_gate":true,"field_owner_ledger":"12/12","immutable_c2_identity_gate":"5/5","terminal_required_field_subset_crosscheck":true,"test_edit_semantics":"accepted_and_committed_preserve_current_bytes","must_not_rerun_or_rederive":true},"immutable_c7_terminal":{"path":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b1a-c3e6f19-corrective-7-offline/terminal-evidence.json","bytes":3977,"sha256":"85f1895d48297d71d351f323e7024523cd68ccebfd88e84c8ed8acc2184e4369","mode":"0600","regular_non_symlink":true,"read_only":true,"payload_read_cap":1,"other_c7_artifact_access":0},"c7_execution_result_discrepancy":{"old_append_read_required":false,"field":"identities.dedicated_test_after_sha256","recorded_in_old_er":"48b0cb295538481998a79896db4fc53d8e4fa12f807a04b67620e54946eb2c38","authoritative_c7_terminal_and_current_committed_bytes":"19858a64fb760c112783b176822e7dabf72dce1b0cf9fb21e3a4738b83cebc3d","old_terminal_or_er_rewrite_forbidden":true,"fresh_terminal_must_record_supersession":true,"fresh_er_append_must_record_supersession":true,"supersession_identity_must_include_c7_terminal_path_bytes_sha_mode":true},"fresh_evidence":{"root":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b1a-c3e6f19-corrective-8-offline","planner_observed_absent_before_activation":true,"must_be_absent_at_activation":true,"exclusive_create_once":true,"root_mode":"0700","artifact_mode":"0600","json_artifacts":["activation-gate.json","pre-validation.json","terminal-evidence.json"],"validation_logs":["compileall.log","targeted_unittest.log","focused_unittest.log","full_unittest.log","codegraph-sync.log","git-diff-check.log"],"artifact_requirements":{"regular":true,"non_symlink":true,"exclusive_create":true,"strict_json_when_json":true,"terminal_sealed_last":true},"fail_fast_unstarted_logs_must_be_absent":true,"old_c7_root_reuse_mutation_or_retry":false},"validation_log_owner":{"open_timing":"immediately_before_each_authorized_child_only","exclusive_open_once_per_started_log":true,"open_flags":["O_WRONLY","O_CREAT","O_EXCL","O_NOFOLLOW"],"open_mode":"0600","fstat_regular_non_symlink_required":true,"child_launch":{"argv_direct_no_shell":true,"shell":false,"stdout":"same_exclusive_open_fd","stderr":"same_exclusive_open_fd","path_reopen_count":0,"shell_redirection_count":0,"second_fd_for_same_log_count":0},"after_child":{"fsync_same_fd":true,"close_same_fd":true,"digest_only_after_close":true},"fail_closed_on_create_fstat_fd_launch_wait_fsync_close_or_digest_error":true},"validation_chain":{"fail_fast":true,"ordered":["compileall","targeted_unittest","focused_unittest","full_unittest","codegraph_sync","git_diff_check"],"commands":{"compileall":{"env":{"PYTHONDONTWRITEBYTECODE":"1"},"argv":[".venv/bin/python","-m","compileall","-q","src/camera_based_rgbww_optimizer/utils/p7_retained_r3_exact_five_controller.py","tests/test_p7_retained_r3_exact_five_controller.py"],"log":"compileall.log","invocation_cap":1},"targeted_unittest":{"env":{"PYTHONDONTWRITEBYTECODE":"1"},"argv":[".venv/bin/python","-m","unittest","-v","tests.test_p7_retained_r3_exact_five_controller"],"log":"targeted_unittest.log","invocation_cap":1},"focused_unittest":{"env":{"PYTHONDONTWRITEBYTECODE":"1"},"argv":[".venv/bin/python","-m","unittest","-v","tests.test_agent_work_machine_contract","tests.test_p7_retained_r3_exact_five_controller","tests.test_p7_retained_release_audit"],"log":"focused_unittest.log","invocation_cap":1},"full_unittest":{"env":{"PYTHONDONTWRITEBYTECODE":"1"},"argv":[".venv/bin/python","-m","unittest","discover","-s","tests","-v"],"log":"full_unittest.log","invocation_cap":1},"codegraph_sync":{"env":{},"argv":["codegraph","sync"],"log":"codegraph-sync.log","invocation_cap":1},"git_diff_check":{"env":{},"argv":["git","diff","--check"],"log":"git-diff-check.log","invocation_cap":1}},"each_invocation_cap":1,"retry":0,"fallback":0},"repo_edits":{"controller":0,"helper":0,"dedicated_test":0,"other":0,"pre_er_changed_paths":[],"post_er_changed_paths":[".agent-work/EXECUTION_RESULT.md"],"execution_result_append_excluded_from_repo_edit_budget":true},"operation_budgets":{"controller_calls":0,"c2_evidence_access":0,"c3_evidence_access":0,"c4_evidence_access":0,"c5_evidence_access":0,"c6_evidence_access":0,"candidate_path_probes":0,"candidate_payload_reads":0,"retained_r3_path_probes":0,"retained_r3_reads":0,"canonical_validator_calls":0,"eligibility_emissions":0,"manifest_writes":0,"commits":0,"stages":0,"release_path_probes":0,"release_calls":0,"network_calls":0,"env_reads":0,"device_calls":0,"camera_calls":0,"ray_calls":0,"strip_calls":0,"cleanup_calls":0,"formal_calls":0,"public_analyzer_calls":0,"td_c_calls":0,"sentinel_calls":0,"p8_calls":0},"execution_result_append_cap":1,"execution_result_contract":{"append_on_pass_or_fail":true,"append_only":true,"required_fields":["activation","full_and_baseline_identities","accepted_c7_prerequisites","c7_discrepancy_supersession","commands","validation_log_fd_ledger","fresh_evidence","repo_diff","zero_locks","retained_r3_status","planner_stop"],"terminal_external_json_required_after_root_creation":true,"terminal_external_json_strict":true,"terminal_external_json_mode":"0600","terminal_external_json_seal_last":true,"terminal_and_er_supersession_values_must_match":true},"retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","terminal_required_on_pass_or_fail_after_root_creation":true,"planner_stop":"F19_CORRECTIVE_8_TERMINAL_WAITING_PLANNER"}`

## Activation lineage 与执行前硬门

本 PLAN 仅在 Orchestrator 以 exact subject `chore(plan): activate f19 validation log owner correction` 创建唯一
PLAN-only activation commit 后可执行。Direct parent 必须为
`2d817465dbd0974d2cc455f7b99be79f1e62bab4`，changed paths 必须精确等于 `.agent-work/PLAN.md`。
Child、committed PLAN blob 与 PLAN SHA 只由 commit 后 runtime Git/bytes 取得；禁止把 activation child、PLAN blob 或
PLAN SHA 写回本 PLAN 形成 self-reference。执行时必须验证 runtime child 为 full SHA、direct parent/subject/path exact、
worktree clean，absolute PLAN bytes 等于 committed blob。

FULL 冻结为 blob `df4c29410baff06858abcbac511da999b9c7ce82`、SHA-256
`613c62174f1c01f2ec37064acb0b2832aee1ab98516a34816b8622b00d59fffd`。Executer 只可从已提交 helper 对 committed
PLAN/FULL 各 parse 一次，逐项验证 active task/contract、candidate identity/verified flag、retained status 与 dispatch flag；
禁止独立 scanner、alias、fallback、payload repair、candidate payload read 或 cross-owner borrowing。

## 已接受 C7 prerequisites 与 immutable discrepancy

C7 terminal/review 已接受 activation/helper gate、12/12 field-owner ledger、5/5 immutable C2 identities、required-field
subset crosscheck 及 test edit 语义。C8 不得重新读取或重算 C2-C6 evidence，也不得重复 test edit。Controller、helper、
dedicated test 必须分别保持 committed SHA-256 `746fd1…9726`、`743e29…825f`、`19858a…bc3d`。

C7 terminal 唯一允许读取一次的旧证据是上述 frozen path，identity 为 `3977` bytes、mode `0600`、SHA-256
`85f1895d48297d71d351f323e7024523cd68ccebfd88e84c8ed8acc2184e4369`。旧 ER 将 dedicated-test after SHA 错记为
`48b0cb…2c38`，而 C7 terminal 与 committed bytes 均证明 `19858a…bc3d`。旧 terminal/ER 不得改写；C8 terminal 与
唯一新 ER append 必须逐字段记录错误值、正确值及 C7 terminal identity，明确该 append supersedes 旧错记。

## C8 single-fd validation execution

Fresh C8 root 已由 Planner 观察为 absent。Activation/pre-validation gate 通过后只可 exclusive-create 一次 root `0700`。
每项 command 仅在即将启动时 exclusive-open 对应 log 一次，mode `0600`；child 的 stdout 与 stderr 直接绑定同一已打开
fd，`shell=false`。禁止先建文件后按路径重开，禁止 shell `>`/`>>`，禁止同一 log 第二 fd。Child terminal 后必须对同一
fd fsync、close，再从路径读取一次并计算 bytes/SHA；任一 create/fstat/fd/launch/wait/fsync/close/digest 错误 fail closed。

按 machine contract 中 exact argv 顺序各最多运行一次 compileall、targeted、focused、full、CodeGraph sync、
`git diff --check`。任一 nonzero 立即停止，未启动 command 的 log 必须 absent；retry/fallback 为 `0`。执行期间 repo
implementation changed paths 在 ER append 前必须为空，不得编辑 controller/helper/test 或任何其他 repo 文件；最后唯一允许的
worktree change 是 append-only `.agent-work/EXECUTION_RESULT.md`。

PASS 或 FAIL 均在 root 创建后最后 exclusive-seal strict `terminal-evidence.json`，记录 activation、FULL/baseline identity、
accepted C7 gate、discrepancy supersession、每个 log 的 single-fd ledger、command counts/exits、artifact manifest、repo diff、
zero locks 与 Planner stop；随后只可向 `.agent-work/EXECUTION_RESULT.md` append 一条同值 superseding record。

## 持续硬锁与停止点

C2-C6 evidence、C7 其他 artifacts、candidate、retained R3、release、canonical validator、eligibility、manifest、network、
`.env`、device、camera、Ray、strip、cleanup、FORMAL-R6、public analyzer、TD-C、sentinel 与 P8 全部锁定为 `0`。
Retained R3 保持 `RETAINED_UNVALIDATED_UNCONSUMED`。这是纯离线 evidence-lifecycle 纠偏，不需要 Advisor 科学判断或
Human 高危设备授权。

Executer 完成或任一失败后必须停止在 `F19_CORRECTIVE_8_TERMINAL_WAITING_PLANNER`；不得 retry、fallback、另建 root、
stage、commit、执行真实 controller、进入 B2 或任何后续阶段。
