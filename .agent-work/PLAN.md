# P7 retained-R3 Option B：R5-C1 synthetic contract/lifecycle gate

**计划状态：** `WAITING_ORCHESTRATOR_ACTIVATION`

**Planner 日期：** `2026-08-01`

**Reference task：** `REF-P7-25-R2-B3-C3-C4-R5-C1`

**Contract：** `P7-TD-B-RETAINED-R3-OPTION-B-B3-C3-C4-R5-C1-SYNTHETIC-CONTRACT-LIFECYCLE-V1`

**当前唯一动作：** 用一个fresh source和两个fresh synthetic roots验证一次性controller的JSON-native adapter与pre-contract failure lifecycle；不读取R4 preparation、manifest、C1、retained或任何真实输入，不运行Git或self-check owner。

**唯一 Planner stop：** `B3_C3_C4_R5_C1_SYNTHETIC_CONTRACT_LIFECYCLE_WAITING_PLANNER_REVIEW`。

**本轮新归档：** `.agent-work/PLANS/20260801-1021-p7-retained-r3-b3-c3-c4-r5-precontract-failure-review.md`；bytes `4481`，SHA-256 `3ca78bce69fd085f6a2d07e3485ef69f7a82bb701d6cc18c10315c549857f399`。

`PLAN_MACHINE_CONTRACT={"schema":"p7_td_b_retained_r3_option_b_b3_c3_c4_r5_c1_synthetic_contract_lifecycle_v1","reference_task_id":"REF-P7-25-R2-B3-C3-C4-R5-C1","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B3-C3-C4-R5-C1-SYNTHETIC-CONTRACT-LIFECYCLE-V1","rejected_r5":{"activation":"e40ce0dfed03dca4d7b71650907b895a07925311","evidence":"766408d6ad3bac646a19078fdb0ad04aab8b85b7","decision":"REJECTED_PRECONTRACT_JSON_BOUNDARY_AND_FAILURE_LIFECYCLE_GAP","failure_phase":"contract_write","failure_code":"json_unsupported_value","source":["/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b3-real-self-check-r5-e40ce0dfed03-source.py",13352,"0d285fbe1dd2ddf40b3b979c41b1f304b9ebb6fec108c9d1616240518b55e936",16777240,2273267,384],"root":["/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b3-real-self-check-r5-e40ce0dfed03",16777240,2273270,448],"root_inventory":[],"reuse_forbidden":true},"activation_commit":{"expected_parent":"766408d6ad3bac646a19078fdb0ad04aab8b85b7","expected_subject":"chore(plan): test self-check lifecycle","expected_changed_paths":[".agent-work/FULL_PLAN_REFERENCE.md",".agent-work/PLAN.md",".agent-work/PLANS/20260801-1021-p7-retained-r3-b3-c3-c4-r5-precontract-failure-review.md"]},"runtime":{"source_path_template":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b3-real-self-check-r5-c1-<activation_short12>-source.py","golden_root_template":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b3-real-self-check-r5-c1-<activation_short12>-golden","failure_root_template":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b3-real-self-check-r5-c1-<activation_short12>-failure","source_mode":384,"root_mode":448,"golden_files":["00-execution-contract.json","00-execution-contract.sha256.json","99-terminal-summary.json","99-terminal-summary.sha256.json"],"failure_files":["99-terminal-summary.json","99-terminal-summary.sha256.json"]},"adapter":{"owner":"ONE_OFF_CONTROLLER_LOCAL","mapping_input":"collections.abc.Mapping","mapping_output":"plain_dict","sequence_inputs":["tuple","list"],"sequence_output":"plain_list","allowed_scalar_concrete_types":["NoneType","bool","int","str"],"string_keys_only":true,"unsupported_code":"json_native_unsupported","production_module_changes":0},"synthetic_cases":[{"name":"golden","contract_input":"nested MappingProxyType + tuple/list + exact allowed scalars","expected_contract_writes":2,"expected_terminal_status":"synthetic_contract_lifecycle_pass","expected_inventory_count":4},{"name":"precontract_failure","contract_input":"nested unsupported object inside frozen MappingProxyType/tuple","expected_failure_code":"json_native_unsupported","expected_contract_writes":0,"expected_terminal_status":"synthetic_precontract_failure_sealed","expected_inventory_count":2}],"execution_budgets":{"committed_plan_reads":1,"committed_full_reads":1,"accepted_archive_reads":1,"old_failure_source_reads":0,"old_failure_root_reads":0,"source_absence_checks":1,"golden_root_absence_checks":1,"failure_root_absence_checks":1,"source_writes":1,"source_compile_checks":1,"source_invocations":1,"fresh_root_creations":2,"native_conversion_golden":1,"native_conversion_injected_failure":1,"golden_contract_writes":2,"failure_contract_writes":0,"golden_terminal_writes":2,"failure_terminal_writes":2,"canonical_reloads":6,"seal_checks":3,"source_identity_postchecks":1,"root_inventory_checks":2,"process_table_scans":1,"execution_result_tail_reads":1,"execution_result_apply_patch_appends":1,"execution_result_appends":1,"postappend_operations":0,"retry":0,"fallback":0},"zero_budgets":{"preparation_root_reads":0,"preparation_file_reads":0,"manifest_root_reads":0,"manifest_file_reads":0,"c1_root_reads":0,"c1_file_reads":0,"retained_root_reads":0,"retained_file_reads":0,"git_processes":0,"required_argv_checks":0,"self_check_owner_calls":0,"owner_git_ledgers":0,"input_artifact_writes":0,"repository_code_writes":0,"repository_test_writes":0,"implementation_commits":0,"canonical_validator_calls":0,"eligibility_emissions":0,"release_consumption":0,"network":0,"device":0,"camera":0,"ray":0,"strip":0,"cleanup":0,"formal":0,"public_analyzer":0,"plan_writes_by_executer":0,"full_writes_by_executer":0,"archive_writes_by_executer":0},"required_full_machine_state":{"active_task_count":1,"active_task":"REF-P7-25-R2-B3-C3-C4-R5-C1","active_plan_contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B3-C3-C4-R5-C1-SYNTHETIC-CONTRACT-LIFECYCLE-V1","retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","manifest_authority":"SUBORDINATE_EVIDENCE_ONLY_CANONICAL_VALIDATOR_SOLE_ELIGIBILITY_OWNER","real_execution_status":"BLOCKED_ON_C1_ACCEPTANCE","device_authorized_by_this_file":false},"orchestrator_commit_after_handoff":{"owner":"ORCHESTRATOR","executer_must_not_commit":true,"expected_subject":"chore(evidence): record self-check lifecycle test","expected_changed_paths":[".agent-work/EXECUTION_RESULT.md"]},"authorization":{"classification":"PURE_OFFLINE_SYNTHETIC_CONTROLLER_LIFECYCLE","human_device_authorization_required":false,"advisor_scientific_decision_required":false},"expected_duration":"under_10_minutes","visible_terminal_required":false,"archive":{"path":".agent-work/PLANS/20260801-1021-p7-retained-r3-b3-c3-c4-r5-precontract-failure-review.md","bytes":4481,"sha256":"3ca78bce69fd085f6a2d07e3485ef69f7a82bb701d6cc18c10315c549857f399"},"planner_stop":"B3_C3_C4_R5_C1_SYNTHETIC_CONTRACT_LIFECYCLE_WAITING_PLANNER_REVIEW"}`

## 1. Activation与fresh-only gate

Activation必须是evidence `766408d...`direct child，subject/path set exact；committed PLAN/FULL和本archive各读取一次并匹配machine contract。source/golden root/failure root使用activation SHA前12位，三者各absence check一次；任一存在即hard fail，不得删除、改名或复用。

旧R5 source与empty root只作为归档中的冻结identity存在。本包对两者path stat/read/list/write均0，也不得从它们提取或重建常量。

只一次`apply_patch`创建mode `0600` standalone source。imports仅允许stdlib `collections.abc.Mapping`、`types.MappingProxyType`及现有P3 `create_exclusive_root`、`persist_canonical_json`、`decode_canonical_json`、`canonical_json_bytes`；不得导入real self-check/domain template、Git/process、validator、release或设备模块。

## 2. Local JSON-native adapter

controller-local `_json_native(value)`必须递归：

- 任意`Mapping`仅接受concrete `str` keys，输出fresh plain `dict`并递归values；duplicate不可能通过mapping object，输出后仍由P3 canonical owner验证。
- concrete tuple/list均输出fresh plain `list`并保持length/order。
- 只允许`None`及concrete `bool/int/str`；注意bool在int前按concrete type处理，禁止float、bytes、set、dataclass、Path及任意其他object。
- unsupported值抛stable local `SyntheticLifecycleError("json_native_unsupported")`；不得fallback到`repr`、stringify、generic serializer或修改P3。

source compile一次后只运行一次；内部按golden再failure顺序完成两个case。

## 3. Golden case

用P3创建fresh golden root。构造至少三层nested `MappingProxyType` + tuple/list contract fixture，覆盖nested mapping、tuple within list、list within tuple及全部allowed scalar types。fixture必须包含`execution_authorized=false`、`eligibility=false`、`release_consumable=false`。

primary lifecycle的`try`必须在native conversion之前开始，并包含：conversion → `00-execution-contract.json` persist → seal persist → strict decode/re-encode/seal equality。随后写JSON-native success `99-terminal-summary.json`及seal。inventory exact machine row四文件、全部0600；terminal status exact `synthetic_contract_lifecycle_pass`，记录adapter coverage和actual counters。

任何golden exception都不得继续failure case或伪装成expected failure；保留root后outer nonzero停止。

## 4. Injected pre-contract failure case

golden完整通过后创建fresh failure root。构造nested frozen fixture，在contract深层唯一插入`object()`；禁止调用P3 writer前移除或替换该值。

primary `try`必须同样在conversion之前开始，并覆盖conversion、contract persist与seal。expected `_json_native` failure被同一lifecycle捕获后：

- contract与contract seal writes必须0；
- 写完全JSON-native的`99-terminal-summary.json`及seal，status `synthetic_precontract_failure_sealed`，first failure type/code exact，eligibility/release/device locks false/0；
- failure terminal与seal自身失败时outer必须nonzero并同时保留primary与seal failure；
- terminal pair成功后把expected injected failure视为case pass，但不得宣称real execution。

failure root inventory exact two 0600 files。不得在此case读取golden artifacts作为输入。

## 5. Independent audit与handoff

controller返回0后独立只读检查source pre/post identity、两个0700 roots、inventories、六个0600 files、strict decode/canonical re-encode及三个seals；golden contract decoded value必须与`_json_native` expected fixture语义exact，failure root不得存在contract文件。process scan一次owned0。

ER tail只读一次，一次`apply_patch`追加physical EOF heading + strict duplicate-free canonical JSON，记录activation/source、两root/files、case results、adapter coverage、actual budgets、locks、first failure与Planner stop。append最后，postappend operations0；Executer不得commit或改plan files。

C1成功只证明controller transport/lifecycle可安全重试；真实R5仍需Planner接受C1后另写fresh source/root执行包。canonical validator、eligibility、release consumption、network/device/camera/Ray/strip/formal/public analyzer全部保持锁定。

维护性判断：adapter严格局限于一次性external controller并由两个行为case覆盖，不修改P3或production owner；无需新增共享helper或架构重构。
