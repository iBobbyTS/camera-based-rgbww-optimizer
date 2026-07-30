# REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-5：exact C2 evidence-identity binding

**计划状态：** `WAITING_ORCHESTRATOR_ALIGNMENT_AND_FRESH_PLANNER_ACTIVATION`

**Planner 日期：** `2026-07-29`

**Reference task：** `REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-5`

**Contract ID：** `P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F19-CORRECTIVE-5-EVIDENCE-IDENTITY`

**唯一当前动作：** Orchestrator先验收C4 review、把FULL唯一active task对齐至C5并提交；随后由新的Planner只对
committed FULL/PLAN identity和activation lineage做一次激活审查。激活前不得派发Executer。激活通过后，唯一Executer
必须从helper parsed PLAN value取得C2五artifact的唯一expected identity，完成pre-edit gate；不得在执行源手抄或影子冻结
任何expected digest。全部gate通过后只修改dedicated test的lexical-local `run` `STORE_FAST`/`LOAD_FAST`精确断言，并在
唯一fresh C5 root运行一次完整fail-fast validation chain。不得执行controller、读取C3/candidate/retained R3/release，或进入B2。

**C4 review archive：**
`.agent-work/PLANS/20260729-2218-p7-retained-r3-option-b-b1a-c3e6f19-corrective-4-review.md`；
SHA-256 `59e24e783eb59463ba048da5a11bb9d18473a5df6af1cc542331df63e82fa8b6`。

`PLAN_MACHINE_CONTRACT={"schema":"f19_corrective_5_evidence_identity_draft_v1","reference_task_id":"REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-5","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F19-CORRECTIVE-5-EVIDENCE-IDENTITY","dispatch_state":"waiting_orchestrator_alignment_and_fresh_planner_activation","single_current_action":"parsed_plan_owned_c2_identity_gate_then_test_only_local_run_correction_then_one_fail_fast_validation_chain","review_archive":{"path":".agent-work/PLANS/20260729-2218-p7-retained-r3-option-b-b1a-c3e6f19-corrective-4-review.md","sha256":"59e24e783eb59463ba048da5a11bb9d18473a5df6af1cc542331df63e82fa8b6"},"activation_requirements":{"orchestrator_full_alignment_required":true,"fresh_planner_activation_required":true,"activation_commit_exact_changed_paths":[".agent-work/PLAN.md"],"activation_commit_exact_subject":"chore(plan): activate f19 c2 evidence identity correction","actual_child_owner":"runtime_git_rev_parse_HEAD_full_sha_after_activation_commit","direct_parent_owner":"runtime_orchestrator_alignment_commit","clean_porcelain_required":true,"committed_plan_blob_owner":"runtime_git_rev_parse_HEAD_colon_plan_path","committed_plan_sha256_owner":"runtime_sha256_of_committed_plan_blob","worktree_plan_must_equal_committed_blob":true,"self_referential_child_or_plan_sha_freeze_forbidden":true},"required_aligned_full_state":{"active_task_count":1,"active_task":"REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-5","active_plan_contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F19-CORRECTIVE-5-EVIDENCE-IDENTITY","retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","candidate_machine_contract_sha256":"3c5847fcbe0af85833c901f6f01058d000a3cecdc0f84e6ae331ed24e138c225","candidate_contract_orchestrator_verified":true},"machine_contract_helper":{"path":"src/camera_based_rgbww_optimizer/utils/agent_work_machine_contract.py","blob_oid":"5c581f9b502bcab1809b6a61a082a47f4150e09f","sha256":"743e2948f6c30a31fde5d072c8effa8b1365d321b303d61e9899ad18ac41825f","plan_api":"parse_plan_machine_contract","full_api":"parse_full_plan_machine_state","plan_api_calls":1,"full_api_calls":1,"direct_import_from_committed_helper":true,"execution_source_machine_marker_literal_count":0,"independent_scanner_alias_fallback_inference_or_payload_repair_count":0},"field_gate_requirements":{"entries":12,"exact_key_membership_before_index":true,"exact_builtin_type_identity":true,"exact_value_compare_after_type":true,"plan_expected_owner":"PLAN.value_only","full_actual_owner":"FULL.value_top_level_only","unlisted_key_alias_get_default_fallback_inference_cross_owner_forbidden":true,"candidate_payload_recompute_or_read_forbidden":true},"immutable_c2_evidence":{"root":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b1a-c3e6f19-corrective-2-offline","root_mode":"0700","artifact_count":5,"artifact_mode":"0600","artifacts":{"activation-gate.json":{"bytes":3243,"sha256":"cd52abf2bcf4dd7a59052771e4fa342f69dc21dd59b7697ad5e5b89d9b53ce5c","source":"c2_execution_result_artifact_map_and_current_bytes"},"pre-validation.json":{"bytes":670,"sha256":"16ec941cd276846268d930c50e31492ea3c5198e0ed473953c5b1304f6a9d9f2","source":"c2_terminal_manifest_and_execution_result"},"compileall.log":{"bytes":0,"sha256":"e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855","source":"c2_terminal_manifest_validation_record_and_execution_result"},"targeted_unittest.log":{"bytes":3108,"sha256":"60e72a1e1bddd8afa34420ed2f4d56db3d7a769879f1a75e8025208360f0bc48","source":"c2_terminal_manifest_validation_record_and_execution_result"},"terminal-evidence.json":{"bytes":2519,"sha256":"41294a0cf35ace7dcc3389d0323015ebaacb42a3bbf0753c3295412be003d8f6","source":"c2_execution_result_artifact_map_and_current_bytes"}},"expected_identity_owner":"PLAN.value.immutable_c2_evidence.artifacts[artifact_name]_single_lookup_only","expected_digest_shadow_literal_or_alias_count":0,"actual_identity_owner":"lstat_plus_single_file_bytes_sha256","actual_expected_record_required":true,"regular_non_symlink_required":true,"exact_path_set_required":true,"preserve_before_after_byte_exact":true,"repair_rewrite_regenerate_delete_count":0},"c4_failure_correction":{"planner_frozen_compileall_sha256_was_correct":true,"c4_failure_detail_transcribed_sha256":"e3b0c44298fc1c149afbf4d8996fb92427ae41e4649b934ca495991b7852b855","transcription_error":"single_character_substitution_c_to_d","execution_source_expected_digest_literal_count":0,"use_parsed_plan_identity_map_only":true},"committed_baseline":{"controller":{"path":"src/camera_based_rgbww_optimizer/utils/p7_retained_r3_exact_five_controller.py","blob_oid":"45097745bcc48aa1312b06fc07c6c910a4529325","sha256":"746fd13056c326489b48ca555b21618b65c8a78f198d035e18c02f68af689726","preserve_byte_exact":true},"dedicated_test":{"path":"tests/test_p7_retained_r3_exact_five_controller.py","blob_oid":"3cff60484e70db003409268f3365d7275dd53ab5","sha256":"e9b51d5d83319e68d29da68a2a023ef6feb248bf6c4b3ce8d776a70e63b957e6"}},"repo_edit_paths":["tests/test_p7_retained_r3_exact_five_controller.py"],"repo_preserve_paths":["src/camera_based_rgbww_optimizer/utils/p7_retained_r3_exact_five_controller.py","src/camera_based_rgbww_optimizer/utils/agent_work_machine_contract.py"],"exact_test_correction":{"lexical_owner":"execute_prepared_exact_five_controller","name_argval":"run","allowed_owner_opcodes":[["execute_prepared_exact_five_controller","STORE_FAST"],["execute_prepared_exact_five_controller","LOAD_FAST"]],"forbidden_opcodes":["LOAD_GLOBAL","LOAD_NAME","LOAD_ATTR","LOAD_METHOD"],"other_owner_or_opcode_allowed":false,"preserve_ast_lexical_owner_proof":true,"preserve_forbidden_import_direct_io_attribute_method_and_eligibility_boundaries":true,"generic_allowlist_string_absence_production_rename_or_regression_removal_forbidden":true},"fresh_evidence_root":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b1a-c3e6f19-corrective-5-offline","fresh_evidence_root_absent_at_activation":true,"fresh_evidence_root_exclusive_create_mode":"0700","fresh_artifacts":["activation-gate.json","pre-validation.json","compileall.log","targeted_unittest.log","focused_unittest.log","full_unittest.log","codegraph-sync.log","git-diff-check.log","terminal-evidence.json"],"fresh_artifact_requirements":{"regular":true,"non_symlink":true,"exclusive_create":true,"mode":"0600","json_strict_when_json":true,"terminal_seal_immutable":true},"validation_chain":{"fail_fast":true,"ordered":["compileall","targeted_unittest","focused_unittest","full_unittest","codegraph_sync","git_diff_check"],"compileall":1,"targeted_unittest":1,"focused_unittest":1,"full_unittest":1,"codegraph_sync":1,"git_diff_check":1,"retry":0,"fallback":0},"operation_budgets":{"helper_edits":0,"test_file_edits":1,"controller_source_edits":0,"controller_calls":0,"c3_evidence_access":0,"candidate_path_probes":0,"candidate_payload_reads":0,"retained_r3_path_probes":0,"retained_r3_reads":0,"canonical_validator_calls":0,"eligibility_emissions":0,"manifest_writes":0,"commits":0,"stages":0,"release_path_probes":0,"release_calls":0,"network_calls":0,"env_reads":0,"device_calls":0,"camera_calls":0,"ray_calls":0,"strip_calls":0,"cleanup_calls":0,"formal_calls":0,"public_analyzer_calls":0,"td_c_calls":0,"sentinel_calls":0,"p8_calls":0},"execution_result_append_cap":1,"terminal_required_on_pass_or_fail":true,"planner_stop":"F19_CORRECTIVE_5_TERMINAL_WAITING_PLANNER"}`

## 激活前硬门

本PLAN当前不是执行授权。Orchestrator必须先把FULL active task/contract与
`required_aligned_full_state`完全对齐并提交；新的Planner随后冻结committed FULL SHA、activation direct parent、committed
PLAN blob/SHA，并把dispatch state改为唯一Executer可执行。任何字段不一致均停止，不得以本draft派发。

激活Planner必须保留12-entry exact field ledger的逐字段owner/path/type/value验证：PLAN-owned字段只从PLAN parsed value取，
FULL-owned字段只从FULL parsed top-level value取。helper PLAN/FULL调用各一次；禁止独立scanner、marker literal、alias、fallback、
`.get()`降级、cross-owner borrowing或candidate payload重算。

## C2 evidence identity唯一owner

Executer在任何repo edit、fresh root创建或测试前，只能读取冻结C2 root。对五个exact artifact逐一执行：

1. `expected = parsed_plan.value["immutable_c2_evidence"]["artifacts"][name]`，每个name只取一次；
2. 验证root `0700`、exact path set、regular/non-symlink、artifact `0600`、exact bytes、SHA-256；
3. actual与expected bytes/SHA都写入pre-edit ledger；
4. 交叉核验C2 `terminal-evidence.json`内compileall/targeted manifest与validation record；
5. 五项全部通过后再继续。

执行源不得出现第二份expected digest literal、手抄digest字典、digest alias、fallback或repair。特别是
`compileall.log`的expected必须来自parsed PLAN map，真实identity为0 bytes及
`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。任一失败立即单次ER append并停止；
不得修改、重写、重建、删除或替换旧C2 evidence，不得访问C3 evidence。

## 唯一允许实现

Pre-edit gate全绿后，只允许编辑`tests/test_p7_retained_r3_exact_five_controller.py`：在AST已证明lexical owner为
`execute_prepared_exact_five_controller`的前提下，`run`只允许该owner的`STORE_FAST`与`LOAD_FAST`；同名的
`LOAD_GLOBAL`、`LOAD_NAME`、`LOAD_ATTR`、`LOAD_METHOD`及其他owner/opcode仍拒绝。不得改controller/helper，不得删除回归、
改名production符号或加入generic allowlist。

## Fresh validation与证据

实现完成后才可exclusive-create frozen C5 root并依序恰好运行一次：compileall、targeted unittest、focused unittest、full
unittest、CodeGraph sync、git diff check。严格fail-fast，retry/fallback均0。每阶段artifact为exclusive regular non-symlink
`0600`，terminal JSON最后seal。PASS/FAIL均只append一次ER，记录activation lineage、helper/field ledger、C2五项
actual/expected identity及before/after不变、C3 access0、controller/test before/after、exact diff、fresh manifest、command
count/exit及全部zero budgets。

## 锁与停止点

controller执行、candidate/retained R3/release、canonical validator、eligibility、manifest、network、`.env`、device、camera、
Ray、strip、cleanup、FORMAL、public analyzer、TD-C、sentinel与P8全部为0。本包不需要Advisor或Human授权。

Executer完成或任一失败后停止在`F19_CORRECTIVE_5_TERMINAL_WAITING_PLANNER`；不得自动重试、另建root、提交、进入B2或后续阶段。
