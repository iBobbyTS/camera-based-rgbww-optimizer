# REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-6：exact C2 terminal evidence-schema binding

**计划状态：** `WAITING_ORCHESTRATOR_ALIGNMENT_AND_FRESH_PLANNER_ACTIVATION_NOT_EXECUTABLE`

**Planner 日期：** `2026-07-29`

**Reference task：** `REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-6`

**Contract ID：** `P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F19-CORRECTIVE-6-TERMINAL-SCHEMA`

**唯一当前动作：** Orchestrator先验收C5 rejection并将FULL唯一active task对齐至C6、整理并提交review state；随后fresh
Planner仅做alignment/activation review，冻结activation lineage与committed PLAN/FULL identities。此文件当前不授权
Executer。激活后的唯一fresh Executer只可按下述exact JSON path/cardinality完成C2 terminal schema crosscheck，之后执行
同一个dedicated-test-only lexical-local `run`修正和一次fresh fail-fast validation chain。

**C5 review archive：**
`.agent-work/PLANS/20260729-2236-p7-retained-r3-option-b-b1a-c3e6f19-corrective-5-review.md`；
SHA-256 `0137e2b36afce2a8120947fe140d9878ce0ccb9eb25c99784f543b6dbcf8c335`。

`PLAN_MACHINE_CONTRACT={"schema":"f19_corrective_6_terminal_schema_waiting_alignment_v1","reference_task_id":"REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-6","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F19-CORRECTIVE-6-TERMINAL-SCHEMA","dispatch_state":"not_executable_waiting_orchestrator_full_alignment_and_fresh_planner_activation","single_current_action":"align_then_activate_exact_c2_terminal_json_schema_gate_before_test_only_correction","review_archive":{"path":".agent-work/PLANS/20260729-2236-p7-retained-r3-option-b-b1a-c3e6f19-corrective-5-review.md","sha256":"0137e2b36afce2a8120947fe140d9878ce0ccb9eb25c99784f543b6dbcf8c335"},"required_future_full_state":{"active_task_count":1,"active_task":"REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-6","active_plan_contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F19-CORRECTIVE-6-TERMINAL-SCHEMA","retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","candidate_machine_contract_sha256":"3c5847fcbe0af85833c901f6f01058d000a3cecdc0f84e6ae331ed24e138c225","candidate_contract_orchestrator_verified":true},"machine_contract_helper":{"path":"src/camera_based_rgbww_optimizer/utils/agent_work_machine_contract.py","blob_oid":"5c581f9b502bcab1809b6a61a082a47f4150e09f","sha256":"743e2948f6c30a31fde5d072c8effa8b1365d321b303d61e9899ad18ac41825f","plan_api":"parse_plan_machine_contract","full_api":"parse_full_plan_machine_state","plan_api_calls":1,"full_api_calls":1,"direct_import_from_committed_helper":true,"independent_scanner_alias_fallback_inference_or_payload_repair_count":0},"immutable_c2_evidence":{"root":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b1a-c3e6f19-corrective-2-offline","root_mode":"0700","artifact_count":5,"artifact_mode":"0600","artifacts":{"activation-gate.json":{"bytes":3243,"sha256":"cd52abf2bcf4dd7a59052771e4fa342f69dc21dd59b7697ad5e5b89d9b53ce5c"},"pre-validation.json":{"bytes":670,"sha256":"16ec941cd276846268d930c50e31492ea3c5198e0ed473953c5b1304f6a9d9f2"},"compileall.log":{"bytes":0,"sha256":"e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"},"targeted_unittest.log":{"bytes":3108,"sha256":"60e72a1e1bddd8afa34420ed2f4d56db3d7a769879f1a75e8025208360f0bc48"},"terminal-evidence.json":{"bytes":2519,"sha256":"41294a0cf35ace7dcc3389d0323015ebaacb42a3bbf0753c3295412be003d8f6"}},"expected_owner":"PLAN.value.immutable_c2_evidence.artifacts[name]","actual_owner":"single_lstat_plus_single_bytes_read_per_artifact","preserve_before_after_byte_exact":true},"terminal_schema_contract":{"artifact":"terminal-evidence.json","parse_owner":"same_bytes_already_read_for_terminal_artifact_actual_identity","json_parse_count":1,"second_artifact_bytes_read_count":0,"top_schema":{"json_path":["schema"],"type":"str","value":"f19_corrective_2_terminal_evidence_v1"},"manifest_collection":{"json_path":["artifact_manifest_before_terminal"],"type":"list","exact_length":3},"validation_collection":{"json_path":["validation"],"type":"list","exact_length":2},"records":[{"command":"compileall","artifact_name":"compileall.log","manifest":{"collection_json_path":["artifact_manifest_before_terminal"],"selector_field":"path","selector_value":"compileall.log","exact_match_count":1,"identity_fields":{"bytes":0,"sha256":"e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855","mode":"0600"}},"validation":{"collection_json_path":["validation"],"selector_field":"name","selector_value":"compileall","exact_match_count":1,"binding_fields":{"log":"compileall.log","log_bytes":0,"log_sha256":"e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855","log_mode":"0600","invocation_count":1,"exit_code":0}}},{"command":"targeted_unittest","artifact_name":"targeted_unittest.log","manifest":{"collection_json_path":["artifact_manifest_before_terminal"],"selector_field":"path","selector_value":"targeted_unittest.log","exact_match_count":1,"identity_fields":{"bytes":3108,"sha256":"60e72a1e1bddd8afa34420ed2f4d56db3d7a769879f1a75e8025208360f0bc48","mode":"0600"}},"validation":{"collection_json_path":["validation"],"selector_field":"name","selector_value":"targeted_unittest","exact_match_count":1,"binding_fields":{"log":"targeted_unittest.log","log_bytes":3108,"log_sha256":"60e72a1e1bddd8afa34420ed2f4d56db3d7a769879f1a75e8025208360f0bc48","log_mode":"0600","invocation_count":1,"exit_code":1}}}],"comparison_rule":"each_path_specific_identity_must_equal_single_parsed_plan_expected_and_already_computed_actual_identity","forbidden":{"recursive_occurrence_counting":true,"duplicate_shape_inference":true,"generic_key_search":true,"complete_identity_location_count_inference":true,"field_name_homogenization":true,"second_terminal_file_read":true,"shadow_expected_identity":true}},"committed_baseline":{"controller":{"path":"src/camera_based_rgbww_optimizer/utils/p7_retained_r3_exact_five_controller.py","blob_oid":"45097745bcc48aa1312b06fc07c6c910a4529325","sha256":"746fd13056c326489b48ca555b21618b65c8a78f198d035e18c02f68af689726","preserve_byte_exact":true},"dedicated_test":{"path":"tests/test_p7_retained_r3_exact_five_controller.py","blob_oid":"3cff60484e70db003409268f3365d7275dd53ab5","sha256":"e9b51d5d83319e68d29da68a2a023ef6feb248bf6c4b3ce8d776a70e63b957e6"}},"repo_edit_paths":["tests/test_p7_retained_r3_exact_five_controller.py"],"repo_preserve_paths":["src/camera_based_rgbww_optimizer/utils/p7_retained_r3_exact_five_controller.py","src/camera_based_rgbww_optimizer/utils/agent_work_machine_contract.py"],"exact_test_correction":{"lexical_owner":"execute_prepared_exact_five_controller","name_argval":"run","allowed_owner_opcodes":[["execute_prepared_exact_five_controller","STORE_FAST"],["execute_prepared_exact_five_controller","LOAD_FAST"]],"forbidden_opcodes":["LOAD_GLOBAL","LOAD_NAME","LOAD_ATTR","LOAD_METHOD"],"other_owner_or_opcode_allowed":false,"preserve_ast_lexical_owner_proof":true,"preserve_forbidden_import_direct_io_attribute_method_and_eligibility_boundaries":true,"generic_allowlist_string_absence_production_rename_or_regression_removal_forbidden":true},"fresh_evidence_root":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b1a-c3e6f19-corrective-6-offline","fresh_root_create_after_all_pre_edit_gates_only":true,"fresh_root_mode":"0700","fresh_artifact_mode":"0600","validation_chain":{"fail_fast":true,"ordered":["compileall","targeted_unittest","focused_unittest","full_unittest","codegraph_sync","git_diff_check"],"each_calls":1,"retry":0,"fallback":0},"operation_budgets":{"helper_edits":0,"test_file_edits":1,"controller_source_edits":0,"controller_calls":0,"c3_evidence_access":0,"c4_evidence_access":0,"c5_evidence_access":0,"candidate_path_probes":0,"candidate_payload_reads":0,"retained_r3_path_probes":0,"retained_r3_reads":0,"canonical_validator_calls":0,"eligibility_emissions":0,"manifest_writes":0,"commits":0,"stages":0,"release_path_probes":0,"release_calls":0,"network_calls":0,"env_reads":0,"device_calls":0,"camera_calls":0,"ray_calls":0,"strip_calls":0,"cleanup_calls":0,"formal_calls":0,"public_analyzer_calls":0,"td_c_calls":0,"sentinel_calls":0,"p8_calls":0},"execution_result_append_cap":1,"terminal_required_on_pass_or_fail":true,"planner_stop":"F19_CORRECTIVE_6_TERMINAL_WAITING_PLANNER","activation_pending":{"orchestrator_full_alignment_required":true,"fresh_planner_activation_required":true,"activation_lineage_and_committed_plan_full_identity_not_yet_frozen":true}}`

## Planner review结论与activation前硬门

C5不得验收为完成：它没有进入test-only correction或任何validation command。但C5已充分证明helper `1/1`、field
ledger `12/12`、C2五项expected/actual identity全部通过，且所有implementation、fresh-root、test、controller与外部锁为0。
C5的失败来自runner额外加入的“完整bytes/SHA shape必须递归出现两次”假设；这不是PLAN要求，也不符合C2两个合法视图的
异构字段名。

当前PLAN只描述C6下一包，不授权执行。Orchestrator必须先将FULL唯一active task与contract对齐到C6并提交；fresh Planner
随后核对新HEAD、parent、exact changed paths、committed PLAN/FULL bytes、clean worktree、helper identity与C6 root absence，重写
本PLAN为`ACTIVE_EXECUTABLE_WAITING_ONE_FRESH_EXECUTER`后才可dispatch。禁止Orchestrator直接把本waiting版本解释为授权。

## Exact terminal schema gate

激活后的Executer须先通过committed helper对PLAN/FULL各parse一次和exact field-owner ledger，再从parsed PLAN唯一取得C2
五artifact expected identities。每个artifact只允许一次`lstat`和一次bytes read；`terminal-evidence.json`的JSON解析必须复用
这次已读bytes，不得二读。

Crosscheck只能按machine contract冻结的exact路径进行：

1. `artifact_manifest_before_terminal`必须是长度3的list；按`path`分别选择`compileall.log`和
   `targeted_unittest.log`，各恰好1项，只读`bytes`、`sha256`、`mode`；
2. `validation`必须是长度2的list；按`name`分别选择`compileall`和`targeted_unittest`，各恰好1项，只读
   `log`、`log_bytes`、`log_sha256`、`log_mode`、`invocation_count`、`exit_code`；
3. 每个视图的path-specific值分别与同一parsed-PLAN expected identity和已计算actual identity比较。

禁止递归occurrence counting、以相同字段shape推断重复次数、generic key search、完整identity location计数、字段名同构化、
第二次terminal bytes read、shadow expected map、alias/fallback或旧payload repair。任何gate失败单次append ER后停止，repo edit、
fresh root与validation保持0。

## 唯一实现、验证、锁与停止点

全部pre-edit gate通过后，仅可编辑`tests/test_p7_retained_r3_exact_five_controller.py`，使AST已证明的lexical owner
`execute_prepared_exact_five_controller`中`run`只允许`STORE_FAST`和`LOAD_FAST`；仍拒绝其他owner/opcode及
`LOAD_GLOBAL`、`LOAD_NAME`、`LOAD_ATTR`、`LOAD_METHOD`。Controller/helper保持byte-exact，不得弱化其他安全回归。

之后才可exclusive-create C6 root，按顺序各运行一次compileall、targeted、focused、full unittest、CodeGraph sync与
`git diff --check`。严格fail-fast，retry/fallback 0；PASS/FAIL均只append ER一次并terminal seal。Executer不得stage/commit。

C3/C4/C5 evidence、controller执行、candidate/retained R3/release、canonical validator、eligibility、manifest、network、
`.env`、device、camera、Ray、strip、cleanup、FORMAL、public analyzer、TD-C、sentinel与P8全部锁定为0。本包是纯
engineering/provenance纠偏，不需要Advisor或Human授权。

Planner stop：`F19_CORRECTIVE_6_WAITING_ORCHESTRATOR_ALIGNMENT_AND_FRESH_PLANNER_ACTIVATION`。
