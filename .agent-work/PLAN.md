# P7 retained-R3 Option B：R5-C1-R1 synthetic writer-failure lifecycle

**计划状态：** `WAITING_ORCHESTRATOR_ACTIVATION`

**Planner 日期：** `2026-08-01`

**Reference task：** `REF-P7-25-R2-B3-C3-C4-R5-C1-R1`

**Contract：** `P7-TD-B-RETAINED-R3-OPTION-B-B3-C3-C4-R5-C1-R1-SYNTHETIC-WRITER-FAILURE-LIFECYCLE-V1`

**当前唯一动作：** 用fresh source、fresh golden root和fresh injected-writer-failure root证明conversion、P3 contract persist与seal位于同一primary lifecycle，且P3 writer在pre-write阶段失败时仍生成exact sealed failure terminal；不读取任何旧root或真实输入。

**唯一 Planner stop：** `B3_C3_C4_R5_C1_R1_SYNTHETIC_WRITER_FAILURE_LIFECYCLE_WAITING_PLANNER_REVIEW`。

**本轮新归档：** `.agent-work/PLANS/20260801-1029-p7-retained-r3-b3-c3-c4-r5-c1-lifecycle-review.md`；bytes `4384`，SHA-256 `7a4e90278d87a02219cefa32b8bc9555b554923cd9ec2d8fd605f454f642ee5c`。

`PLAN_MACHINE_CONTRACT={"schema":"p7_td_b_retained_r3_option_b_b3_c3_c4_r5_c1_r1_synthetic_writer_failure_lifecycle_v1","reference_task_id":"REF-P7-25-R2-B3-C3-C4-R5-C1-R1","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B3-C3-C4-R5-C1-R1-SYNTHETIC-WRITER-FAILURE-LIFECYCLE-V1","rejected_c1":{"activation":"fc97ac1f4cd057768530222b614524719594c2ee","evidence":"bf5b237f4d45c3dac4bebe5626e59ef39f6a39c1","decision":"REJECTED_PARTIAL_LIFECYCLE_COVERAGE_CONTRACT_WRITER_NOT_IN_INJECTED_PRIMARY_PATH","accepted_semantics":["JSON_NATIVE_MAPPING_TO_DICT","JSON_NATIVE_TUPLE_LIST_TO_LIST","CONCRETE_SCALAR_ALLOWLIST","GOLDEN_CONTRACT_WRITER_PASS","CONVERSION_FAILURE_TERMINAL_SEALED"],"reuse_forbidden":true},"activation_commit":{"expected_parent":"bf5b237f4d45c3dac4bebe5626e59ef39f6a39c1","expected_subject":"chore(plan): test writer failure lifecycle","expected_changed_paths":[".agent-work/FULL_PLAN_REFERENCE.md",".agent-work/PLAN.md",".agent-work/PLANS/20260801-1029-p7-retained-r3-b3-c3-c4-r5-c1-lifecycle-review.md"]},"runtime":{"source_path_template":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b3-real-self-check-r5-c1-r1-<activation_short12>-source.py","golden_root_template":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b3-real-self-check-r5-c1-r1-<activation_short12>-golden","writer_failure_root_template":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b3-real-self-check-r5-c1-r1-<activation_short12>-writer-failure","source_mode":384,"root_mode":448,"golden_files":["00-execution-contract.json","00-execution-contract.sha256.json","99-terminal-summary.json","99-terminal-summary.sha256.json"],"writer_failure_files":["99-terminal-summary.json","99-terminal-summary.sha256.json"],"allowed_imports":["__future__","collections.abc.Mapping","sys","types.MappingProxyType","camera_based_rgbww_optimizer.utils.p7_retained_r3_provenance_io"]},"adapter":{"mapping_output":"plain_dict","sequence_output":"plain_list","allowed_scalar_concrete_types":["NoneType","bool","int","str"],"unsupported_code":"json_native_unsupported","local_only":true},"injection":{"surface":"persist_canonical_json.dependencies.open_fd","callable":"deny_contract_open","behavior":"raise OSError before target creation","expected_p3_error_type":"ProvenanceIOError","expected_p3_error_code":"target_open_failed","injected_open_calls":1,"contract_target_created":false,"terminal_writer_dependencies":"DEFAULT_UNINJECTED"},"execution_budgets":{"committed_plan_reads":1,"committed_full_reads":1,"accepted_archive_reads":1,"old_c1_source_reads":0,"old_c1_root_reads":0,"old_r5_source_reads":0,"old_r5_root_reads":0,"source_absence_checks":1,"golden_root_absence_checks":1,"writer_failure_root_absence_checks":1,"source_writes":1,"source_compile_checks":1,"source_invocations":1,"fresh_root_creations":2,"native_conversion_golden":1,"native_conversion_writer_failure":1,"golden_contract_writer_invocations":1,"golden_contract_writes":2,"injected_contract_writer_invocations":1,"injected_open_calls":1,"writer_failure_contract_writes":0,"golden_terminal_writes":2,"writer_failure_terminal_writes":2,"canonical_reloads":6,"seal_checks":3,"source_identity_postchecks":1,"root_inventory_checks":2,"process_table_scans":1,"execution_result_tail_reads":1,"execution_result_apply_patch_appends":1,"execution_result_appends":1,"postappend_operations":0,"retry":0,"fallback":0},"zero_budgets":{"preparation_reads":0,"manifest_reads":0,"c1_reads":0,"retained_reads":0,"git_processes":0,"required_argv_checks":0,"self_check_owner_calls":0,"owner_git_ledgers":0,"input_artifact_writes":0,"repository_code_writes":0,"repository_test_writes":0,"implementation_commits":0,"canonical_validator_calls":0,"eligibility_emissions":0,"release_consumption":0,"network":0,"device":0,"camera":0,"ray":0,"strip":0,"cleanup":0,"formal":0,"public_analyzer":0,"plan_writes_by_executer":0,"full_writes_by_executer":0,"archive_writes_by_executer":0},"required_full_machine_state":{"active_task_count":1,"active_task":"REF-P7-25-R2-B3-C3-C4-R5-C1-R1","active_plan_contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B3-C3-C4-R5-C1-R1-SYNTHETIC-WRITER-FAILURE-LIFECYCLE-V1","retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","real_execution_status":"BLOCKED_ON_C1_R1_ACCEPTANCE","device_authorized_by_this_file":false},"orchestrator_commit_after_handoff":{"owner":"ORCHESTRATOR","executer_must_not_commit":true,"expected_subject":"chore(evidence): record writer failure lifecycle","expected_changed_paths":[".agent-work/EXECUTION_RESULT.md"]},"authorization":{"classification":"PURE_OFFLINE_SYNTHETIC_P3_WRITER_FAILURE_LIFECYCLE","human_device_authorization_required":false,"advisor_scientific_decision_required":false},"expected_duration":"under_10_minutes","visible_terminal_required":false,"archive":{"path":".agent-work/PLANS/20260801-1029-p7-retained-r3-b3-c3-c4-r5-c1-lifecycle-review.md","bytes":4384,"sha256":"7a4e90278d87a02219cefa32b8bc9555b554923cd9ec2d8fd605f454f642ee5c"},"planner_stop":"B3_C3_C4_R5_C1_R1_SYNTHETIC_WRITER_FAILURE_LIFECYCLE_WAITING_PLANNER_REVIEW"}`

## 1. Activation与fresh-only scope

Activation必须是`bf5b237...`direct child，subject/path set exact；committed PLAN/FULL和本archive各读取一次并匹配。source、golden root、writer-failure root以activation SHA前12位派生并各absence check一次；任一存在即hard fail。

旧C1 source/roots、旧R5 source/empty root及R4/真实roots的path stat/read/list/write全部0；不得复用、删除、repair或从其重建fixture。

一次`apply_patch`创建0600 source。imports只能是machine row allowlist；`sys`仅用于stdout。不得导入process/Git/self-check/domain/validator/release/device模块。

## 2. Shared adapter与golden case

复用C1已验证的local `_json_native`精确语义：Mapping/string keys→fresh dict，tuple/list→fresh list，只允许concrete None/bool/int/str，其余stable `json_native_unsupported`。不得添加fallback/stringify或修改P3。

创建0700 golden root；primary broad `try`必须从conversion前开始并顺序包含：native conversion、default P3 contract persist、contract seal persist、strict decode/re-encode/seal check、success terminal及seal。nested frozen fixture覆盖mapping/tuple/list/scalars和eligibility/release false。成功inventory exact4个0600 files，status `synthetic_contract_lifecycle_pass`。

golden任一失败立即outer nonzero，writer-failure case不运行。

## 3. P3 writer pre-write injected failure

golden通过后创建0700 writer-failure root。fixture必须完全可由adapter转换，不含unsupported object。定义局部`deny_contract_open(*args, **kwargs)`：计数exact1并直接`raise OSError("synthetic_contract_open_denied")`，不得调用真实open。

primary broad `try`必须在conversion之前开始，代码路径中顺序实际存在并覆盖：

1. `_json_native(fixture)`成功；
2. `persist_canonical_json(root,"00-execution-contract.json",native,dependencies={"open_fd":deny_contract_open})`被调用一次；
3. contract seal persist语句位于同一try中，仅因step2 hard fail而不可达。

捕获actual primary后必须exact验证type `ProvenanceIOError`、code `target_open_failed`、injected open calls1；其他type/code也必须写terminal但case最终nonzero。

failure terminal必须使用default、uninjected P3 writer写`99-terminal-summary.json`及seal，记录primary type/code、injected counts、contract writer invocations1、contract writes0及所有locks。terminal/seal失败时outer nonzero并保留primary+seal failure。expected primary且terminal pair成功才视为case pass。root不得包含contract或seal，inventory exact2个0600 terminal files，status `synthetic_writer_failure_sealed`。

## 4. Independent audit与handoff

controller返回0后独立只读验证source pre/post identity、两个0700 roots、inventories、六个0600 files、strict canonical re-encode和三seals；golden contract语义exact；writer-failure root contract targets均absent；terminal counters/type/code exact。process scan一次owned0。

ER tail只读一次，一次`apply_patch`追加physical EOF heading和strict duplicate-free canonical JSON，记录activation/source、两case identities/results、injection事实、budgets/locks、first failure与Planner stop。append最后，postappend operations0；Executer不得commit或改plan files。

成功仅关闭writer failure lifecycle测试缺口；真实R5仍需Planner接受后使用全新source/root。validator、eligibility、release consumption、network/device/camera/Ray/strip/formal/public analyzer持续0。

维护性判断：R1使用P3现有dependency injection在一次性source中覆盖真实writer错误面，不修改production owner或新增抽象。
