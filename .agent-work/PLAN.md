# REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-7：C2 terminal required-field subset binding

**计划状态：** `WAITING_ORCHESTRATOR_ALIGNMENT_AND_FRESH_PLANNER_ACTIVATION`

**Planner 日期：** `2026-07-29`

**Reference task：** `REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-7`

**Contract ID：** `P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F19-CORRECTIVE-7-SCHEMA-SUBSET`

**唯一当前动作：** Orchestrator审查C6拒绝结论、将FULL唯一active task对齐到C7并提交review state；随后fresh
Planner只做exact SHA/lineage activation。对齐和activation完成前不得dispatch Executer。未来唯一fresh Executer仅可执行
required-field subset terminal gate；通过后只修正dedicated test的lexical-local `run`断言并运行一次fresh fail-fast chain。

**C6 review archive：**
`.agent-work/PLANS/20260729-2254-p7-retained-r3-option-b-b1a-c3e6f19-corrective-6-review.md`；
SHA-256 `cb95512ac8e7d26df43552df913aaaf22ca66a776f065a36362397156fc1a6d6`。

`PLAN_MACHINE_CONTRACT={"schema":"f19_corrective_7_schema_subset_alignment_v1","reference_task_id":"REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-7","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F19-CORRECTIVE-7-SCHEMA-SUBSET","dispatch_state":"blocked_until_orchestrator_full_alignment_and_fresh_planner_activation","single_current_action":"orchestrator_align_full_then_fresh_planner_freeze_activation_sha_before_one_executer","review_archive":{"path":".agent-work/PLANS/20260729-2254-p7-retained-r3-option-b-b1a-c3e6f19-corrective-6-review.md","sha256":"cb95512ac8e7d26df43552df913aaaf22ca66a776f065a36362397156fc1a6d6"},"required_aligned_full_state":{"active_task_count":1,"active_task":"REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-7","active_plan_contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F19-CORRECTIVE-7-SCHEMA-SUBSET","retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","candidate_machine_contract_sha256":"3c5847fcbe0af85833c901f6f01058d000a3cecdc0f84e6ae331ed24e138c225","candidate_contract_orchestrator_verified":true},"fresh_planner_activation_required":true,"machine_contract_helper":{"path":"src/camera_based_rgbww_optimizer/utils/agent_work_machine_contract.py","sha256":"743e2948f6c30a31fde5d072c8effa8b1365d321b303d61e9899ad18ac41825f","plan_api":"parse_plan_machine_contract","full_api":"parse_full_plan_machine_state","plan_api_calls":1,"full_api_calls":1,"direct_import":true,"independent_scanner_or_reparse_count":0},"field_gate_entries":12,"immutable_c2_evidence":{"root":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b1a-c3e6f19-corrective-2-offline","root_mode":"0700","artifact_mode":"0600","exact_path_set":["activation-gate.json","pre-validation.json","compileall.log","targeted_unittest.log","terminal-evidence.json"],"artifacts":{"activation-gate.json":{"bytes":3243,"sha256":"cd52abf2bcf4dd7a59052771e4fa342f69dc21dd59b7697ad5e5b89d9b53ce5c"},"pre-validation.json":{"bytes":670,"sha256":"16ec941cd276846268d930c50e31492ea3c5198e0ed473953c5b1304f6a9d9f2"},"compileall.log":{"bytes":0,"sha256":"e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"},"targeted_unittest.log":{"bytes":3108,"sha256":"60e72a1e1bddd8afa34420ed2f4d56db3d7a769879f1a75e8025208360f0bc48"},"terminal-evidence.json":{"bytes":2519,"sha256":"41294a0cf35ace7dcc3389d0323015ebaacb42a3bbf0753c3295412be003d8f6"}},"single_lstat_and_bytes_read_per_artifact":true,"terminal_bytes_reused_for_one_json_parse":true,"second_terminal_read_count":0,"repair_rewrite_regenerate_delete_count":0},"terminal_schema_subset_contract":{"top_schema":{"type":"str","value":"f19_corrective_2_terminal_evidence_v1"},"collections":{"manifest":{"path":["artifact_manifest_before_terminal"],"type":"list","exact_length":3,"record_type":"dict","selector":"path"},"validation":{"path":["validation"],"type":"list","exact_length":2,"record_type":"dict","selector":"name"}},"commands":{"compileall":{"artifact":"compileall.log","manifest_required_fields":{"path":{"type":"str","value":"compileall.log"},"bytes":{"type":"int","value":0},"sha256":{"type":"str","value":"e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"},"mode":{"type":"str","value":"0600"}},"validation_required_fields":{"name":{"type":"str","value":"compileall"},"log":{"type":"str","value":"compileall.log"},"log_bytes":{"type":"int","value":0},"log_sha256":{"type":"str","value":"e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"},"log_mode":{"type":"str","value":"0600"},"invocation_count":{"type":"int","value":1},"exit_code":{"type":"int","value":0}}},"targeted_unittest":{"artifact":"targeted_unittest.log","manifest_required_fields":{"path":{"type":"str","value":"targeted_unittest.log"},"bytes":{"type":"int","value":3108},"sha256":{"type":"str","value":"60e72a1e1bddd8afa34420ed2f4d56db3d7a769879f1a75e8025208360f0bc48"},"mode":{"type":"str","value":"0600"}},"validation_required_fields":{"name":{"type":"str","value":"targeted_unittest"},"log":{"type":"str","value":"targeted_unittest.log"},"log_bytes":{"type":"int","value":3108},"log_sha256":{"type":"str","value":"60e72a1e1bddd8afa34420ed2f4d56db3d7a769879f1a75e8025208360f0bc48"},"log_mode":{"type":"str","value":"0600"},"invocation_count":{"type":"int","value":1},"exit_code":{"type":"int","value":1}}}},"required_field_rule":"for_each_listed_field_direct_membership_then_exact_builtin_type_identity_then_exact_value","record_schema_rule":"listed_fields_are_required_subset_not_complete_record_key_set","extra_field_policy":{"must_not_reject_record_for_extra_keys":true,"must_not_enumerate_or_compare_extra_key_set":true,"must_not_read_or_infer_binding_from_extra_values":true,"observed_nonbinding_extra":{"validation":{"compileall":{"argv":"list"},"targeted_unittest":{"argv":"list"}},"manifest":{}}},"selector_exact_match_count":1,"whole_object_exact_key_set_assertion_forbidden":true,"recursive_search_shape_inference_generic_key_search_forbidden":true},"committed_baseline":{"controller_sha256":"746fd13056c326489b48ca555b21618b65c8a78f198d035e18c02f68af689726","helper_sha256":"743e2948f6c30a31fde5d072c8effa8b1365d321b303d61e9899ad18ac41825f","dedicated_test_before_sha256":"e9b51d5d83319e68d29da68a2a023ef6feb248bf6c4b3ce8d776a70e63b957e6"},"repo_edit_paths":["tests/test_p7_retained_r3_exact_five_controller.py"],"repo_preserve_paths":["src/camera_based_rgbww_optimizer/utils/p7_retained_r3_exact_five_controller.py","src/camera_based_rgbww_optimizer/utils/agent_work_machine_contract.py"],"exact_test_correction":{"lexical_owner":"execute_prepared_exact_five_controller","name_argval":"run","allowed_owner_opcodes":["STORE_FAST","LOAD_FAST"],"forbidden_opcodes":["LOAD_GLOBAL","LOAD_NAME","LOAD_ATTR","LOAD_METHOD"],"preserve_ast_and_other_boundaries":true},"fresh_evidence":{"root":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b1a-c3e6f19-corrective-7-offline","must_be_absent_at_activation":true,"exclusive_create_after_all_pre_edit_gates":true,"root_mode":"0700","artifact_mode":"0600","terminal_seal_last":true},"validation_chain":{"fail_fast":true,"ordered":["compileall","targeted_unittest","focused_unittest","full_unittest","codegraph_sync","git_diff_check"],"each_call":1,"retry":0,"fallback":0},"operation_budgets":{"helper_edits":0,"test_file_edits":1,"controller_source_edits":0,"controller_calls":0,"c3_c4_c5_c6_evidence_access":0,"candidate_access":0,"retained_r3_access":0,"validator_calls":0,"eligibility_emissions":0,"manifest_writes":0,"git_mutation":0,"release_access":0,"network_calls":0,"env_reads":0,"device_calls":0,"camera_calls":0,"ray_calls":0,"strip_calls":0,"cleanup_calls":0,"formal_calls":0,"public_analyzer_calls":0,"td_c_calls":0,"sentinel_calls":0,"p8_calls":0},"execution_result_append_cap":1,"planner_stop":"F19_CORRECTIVE_7_WAITING_PLANNER_REVIEW"}`

## C6验收结论

C6结论为`REJECTED_EXECUTION_SIDE_UNAUTHORIZED_WHOLE_RECORD_KEY_SET_ASSERTION`。执行器已证明activation、helper
`1/1`、ledger `12/12`、五项identity、collection schema、compileall两个selector均通过；但在逐字段校验前额外要求
validation record整个key set等于七个required fields，错误拒绝了合法的`argv:list`。

冻结C2 JSON中，两个validation record的唯一observed extra均为`argv:list`。它不拥有selector、log binding、identity、
invocation或exit status；whole-file bytes/SHA已绑定完整payload。C7必须仅对列出的required fields做membership、exact builtin
type和exact value检查。额外字段不得触发拒绝，也不得被枚举为第二个acceptance gate、读取内容或用于推断绑定。

## 对齐与activation硬门

当前PLAN不授权Executer。Orchestrator必须先把FULL唯一active task/contract改为C7，保留retained R3
`RETAINED_UNVALIDATED_UNCONSUMED`与candidate contract verified状态，并提交C6 review state。随后fresh Planner必须核对
实际direct parent、FULL blob/SHA、PLAN-only activation changed path与clean porcelain，将这些runtime事实写入新的可执行PLAN并由
Orchestrator创建exact PLAN-only activation commit。缺任一项即停止，不得dispatch。

## 未来唯一执行范围

Activation后，唯一fresh Executer先按committed helper完成PLAN/FULL各一次parse、12-entry owner gate和C2五项single-read
identity gate。terminal crosscheck必须复用已读bytes、strict parse一次、按exact paths/selectors/cardinality选择四个record，然后只对
listed required fields逐项校验。禁止whole-record exact key set、extra-key enumeration、recursive search、shape inference、generic
key search、二读、shadow expected map、alias/fallback或payload repair。

全部pre-edit gate通过后，只允许编辑`tests/test_p7_retained_r3_exact_five_controller.py`，将lexical-local `run`的合法
`STORE_FAST`/`LOAD_FAST`与非法global/name/attribute/method owners区分开。Controller和helper byte-exact冻结。随后在fresh C7
root依序各运行一次compileall、targeted、focused、full、CodeGraph sync和`git diff --check`；严格fail-fast，retry/fallback 0，
PASS/FAIL均append ER一次并停在Planner review。

## 持续硬锁与停止点

C3-C6 evidence、candidate、retained R3、release、canonical validator、eligibility、controller execution、网络、`.env`、设备、
相机、Ray、strip、cleanup、FORMAL-R6、public analyzer、TD-C、sentinel和P8全部锁定为0。本包为纯离线工程/provenance纠偏，
不需要Advisor科学决策或Human高危设备授权。

**当前Planner stop：** `F19_CORRECTIVE_6_REVIEWED_WAITING_ORCHESTRATOR_C7_ALIGNMENT`。
