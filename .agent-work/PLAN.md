# REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-8：validation log single-owner corrective

**计划状态：** `WAITING_ORCHESTRATOR_ALIGNMENT_AND_PLANNER_ACTIVATION_NOT_EXECUTABLE`

**Planner 日期：** `2026-07-29`

**Reference task：** `REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-8`

**Contract ID：** `P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F19-CORRECTIVE-8-LOG-OWNER`

**唯一当前动作：** Orchestrator验收C7 review并将FULL对齐至C8；随后由fresh Planner冻结activation lineage、
aligned FULL identity与唯一fresh C8 root，才可放行一个fresh Executer。当前PLAN不授权执行、测试、root创建、
旧root retry、代码修改、设备访问、release消费或validator调用。

**C7 review archive：**
`.agent-work/PLANS/20260729-2310-p7-retained-r3-option-b-b1a-c3e6f19-corrective-7-review.md`；
SHA-256 `6a7a2bc3467c5b63b634578b5a14252efffa4557f32d9ff65fbeb420dcf0a424`。

`PLAN_MACHINE_CONTRACT={"schema":"f19_corrective_8_validation_log_owner_alignment_v1","reference_task_id":"REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-8","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F19-CORRECTIVE-8-LOG-OWNER","dispatch_state":"not_dispatchable_waiting_orchestrator_full_alignment_and_fresh_planner_activation","single_current_action":"align_then_freeze_single_fd_validation_log_owner_for_one_fresh_chain","review_archive":{"path":".agent-work/PLANS/20260729-2310-p7-retained-r3-option-b-b1a-c3e6f19-corrective-7-review.md","sha256":"6a7a2bc3467c5b63b634578b5a14252efffa4557f32d9ff65fbeb420dcf0a424"},"accepted_prerequisites":{"activation_helper_field_schema_and_c2_identity_gates":"passed_in_c7_terminal","test_edit_semantics":"accepted_preserve_current_bytes","controller_sha256":"746fd13056c326489b48ca555b21618b65c8a78f198d035e18c02f68af689726","helper_sha256":"743e2948f6c30a31fde5d072c8effa8b1365d321b303d61e9899ad18ac41825f","dedicated_test_sha256":"19858a64fb760c112783b176822e7dabf72dce1b0cf9fb21e3a4738b83cebc3d"},"immutable_c7_terminal":{"path":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b1a-c3e6f19-corrective-7-offline/terminal-evidence.json","bytes":3977,"sha256":"85f1895d48297d71d351f323e7024523cd68ccebfd88e84c8ed8acc2184e4369","mode":"0600","read_only":true},"c7_execution_result_discrepancy":{"field":"identities.dedicated_test_after_sha256","recorded_in_old_er":"48b0cb295538481998a79896db4fc53d8e4fa12f807a04b67620e54946eb2c38","authoritative_terminal_and_current_bytes":"19858a64fb760c112783b176822e7dabf72dce1b0cf9fb21e3a4738b83cebc3d","old_terminal_or_er_rewrite_forbidden":true,"next_er_append_must_supersede":true},"next_activation_must_freeze":{"aligned_full_identity":true,"runtime_activation_lineage":true,"fresh_root":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b1a-c3e6f19-corrective-8-offline","fresh_root_absent_before_execution":true,"fresh_root_exclusive_create":true,"root_mode":"0700","artifact_mode":"0600"},"validation_log_owner":{"exclusive_open_once_per_log":true,"same_existing_fd_owns_child_stdout_and_stderr":true,"path_reopen_after_exclusive_create":false,"shell_path_redirection_after_exclusive_create":false,"close_and_fsync_before_digest":true,"fail_closed_on_create_fd_or_launch_error":true},"validation_chain":{"ordered":["compileall","targeted_unittest","focused_unittest","full_unittest","codegraph_sync","git_diff_check"],"fail_fast":true,"each_invocation_cap":1,"retry":0,"fallback":0},"repo_edits":{"test":0,"controller":0,"helper":0,"other":0},"fresh_evidence":{"terminal_sealed_last":true,"append_only_superseding_execution_result_required_on_pass_or_fail":true,"old_c7_root_reuse_or_mutation":false},"zero_locks":{"c3_evidence_access":0,"c4_evidence_access":0,"c5_evidence_access":0,"c6_evidence_access":0,"candidate_path_probes":0,"candidate_payload_reads":0,"retained_r3_path_probes":0,"retained_r3_reads":0,"canonical_validator_calls":0,"eligibility_emissions":0,"manifest_writes":0,"release_path_probes":0,"release_calls":0,"network_calls":0,"env_reads":0,"device_calls":0,"camera_calls":0,"ray_calls":0,"strip_calls":0,"cleanup_calls":0,"formal_calls":0,"public_analyzer_calls":0,"td_c_calls":0,"sentinel_calls":0,"p8_calls":0},"retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","planner_stop":"F19_CORRECTIVE_8_WAITING_ORCHESTRATOR_ALIGNMENT_AND_PLANNER_ACTIVATION"}`

## C7 验收结论

C7的activation/helper、12-entry owner ledger、C2 identity及terminal required-field subset gate均通过。
唯一test diff语义正确并保留；controller/helper byte-exact。C7因validation日志先exclusive-create、后被zsh
`noclobber`拒绝按路径重开而停止，compileall实际进程调用为`0`，后续命令均为`0`，retry/fallback为`0`。

C7 terminal与当前test bytes均证明after SHA为
`19858a64fb760c112783b176822e7dabf72dce1b0cf9fb21e3a4738b83cebc3d`；旧ER误记为`48b0…2c38`。
旧terminal与旧ER不可改写，C8必须在新terminal和新ER append中显式supersede该字段。

## C8 activation后唯一允许的执行语义

每个validation log必须由同一owner以exclusive方式只打开一次，mode为`0600`；child的stdout/stderr直接绑定
该已打开fd，不得再次以路径重开，不得在exclusive-create后使用shell `>`/`>>`。child结束后先flush/fsync/close，
再读取并计算bytes/SHA。任一create、fd、launch或seal错误均fail closed。

当前test bytes、controller与helper必须byte-exact保持。C8不得编辑任何repo文件。只允许在fresh C8 root依序各运行
一次compileall、targeted、focused、full、CodeGraph sync与`git diff --check`；fail-fast，retry/fallback为`0`。
PASS或FAIL均最后seal strict terminal JSON，并向ER追加唯一superseding record；不得复用、重试或改写C7 root。

## 持续硬锁与停止点

C3-C6、candidate、retained R3、release、canonical validator、eligibility、network、`.env`、设备、相机、Ray、
strip、cleanup、formal、public analyzer、TD-C、sentinel及P8保持`0`。Retained R3保持
`RETAINED_UNVALIDATED_UNCONSUMED`。这是离线证据生命周期纠偏，不需要Advisor科学判断或Human高风险授权。

**Planner stop：** `F19_CORRECTIVE_8_WAITING_ORCHESTRATOR_ALIGNMENT_AND_PLANNER_ACTIVATION`。
