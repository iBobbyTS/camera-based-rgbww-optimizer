# P7 retained-R3 Option B：P1-C1-R1 exact-bytes activation correction

**计划状态：** `WAITING_ORCHESTRATOR_ACTIVATION`

**Planner 日期：** `2026-08-01`

**Reference task：** `REF-P7-25-R2-B3-C3-C4-R5-R1-C1-R2-P1-C1-R1`

**Contract：** `P7-TD-B-RETAINED-R3-OPTION-B-B3-C3-C4-R5-R1-C1-R2-P1-C1-R1-EXACT-BYTES-IMMUTABLE-EXPECTATION-CORRECTION-V1`

**当前唯一动作：** 从activation commit取得committed PLAN/FULL/archive的exact bytes并调用当前repo-owned parser，保留P1 exact two-path dirty implementation；activation gate通过后，只在dedicated test内一次bounded patch修正两处stale mutable equality expectation，再完成原P1-C1 targeted/focused/full、compileall、CodeGraph、exact two-path implementation commit和postcommit targeted合同，封存ER并停在Planner验收门。

**唯一 Planner stop：** `B3_C3_C4_R5_R1_C1_R2_P1_C1_R1_EXACT_BYTES_IMMUTABLE_EXPECTATION_CORRECTION_WAITING_PLANNER_REVIEW`。

**本轮新归档：** `.agent-work/PLANS/20260801-1212-p7-retained-r3-b3-c3-c4-r5-r1-c1-activation-bytes-review.md`；bytes `4900`，SHA-256 `b9cd03b55ff291c7025627fa841d6ef6d946ea102eb7147803b5155870b5a00f`。

`PLAN_MACHINE_CONTRACT={"schema":"p7_td_b_retained_r3_option_b_b3_c3_c4_r5_r1_c1_r2_p1_c1_r1_exact_bytes_immutable_expectation_correction_v1","reference_task_id":"REF-P7-25-R2-B3-C3-C4-R5-R1-C1-R2-P1-C1-R1","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B3-C3-C4-R5-R1-C1-R2-P1-C1-R1-EXACT-BYTES-IMMUTABLE-EXPECTATION-CORRECTION-V1","reviewed_p1_c1":{"activation":"81019ea94c266e9f69a82a3d985f6397d45041a4","evidence":"aea9ce3769dea41348d739ee92b36fa2f47889a5","decision":"REJECTED_P1_C1_EXECUTION_CREDIT_PRESERVE_EXACT_TWO_PATHS_FOR_EXACT_BYTES_SUCCESSOR","failure_phase":"ACTIVATION_MACHINE_ROW_PARSE","failure_code":"source_not_exact_bytes","repository_effects":0,"test_correction":0,"validation_suites":0,"implementation_commit":0,"retry":0,"real_self_check":0,"eligibility":false,"release_consumable":false},"activation_commit":{"expected_parent":"aea9ce3769dea41348d739ee92b36fa2f47889a5","expected_subject":"chore(plan): retry immutable parser correction with exact bytes","expected_changed_paths":[".agent-work/FULL_PLAN_REFERENCE.md",".agent-work/PLAN.md",".agent-work/PLANS/20260801-1212-p7-retained-r3-b3-c3-c4-r5-r1-c1-activation-bytes-review.md"]},"archive":{"path":".agent-work/PLANS/20260801-1212-p7-retained-r3-b3-c3-c4-r5-r1-c1-activation-bytes-review.md","bytes":4900,"sha256":"b9cd03b55ff291c7025627fa841d6ef6d946ea102eb7147803b5155870b5a00f"},"preserved_dirty":{"exact_paths":["src/camera_based_rgbww_optimizer/utils/agent_work_machine_contract.py","tests/test_agent_work_machine_contract.py"],"source":[9414,"a02a30c026fba548c81c04a277e2f235385ddb8a459c4ff2f73c91ee87c3737e","ce2200181bd2a493cfaab621daa17b89a13bdf1f"],"test":[13411,"5e5aa5831edc50d695a09cb473333450f68820cfaddedc054d8bb010314ba920","5efc93c11b37de900f67b3d1c4aa734048d035fc"],"source_patch_writes":0,"test_patch_writes":1,"implementation_expected_subject":"fix(p7): harden machine row parsing"},"exact_bytes_gate":{"plan_acquisition":"GIT_SHOW_BYTES","full_acquisition":"GIT_SHOW_BYTES","archive_acquisition":"GIT_SHOW_BYTES","parser_owner":"CURRENT_REPO_OWNED_AGENT_WORK_MACHINE_CONTRACT","forbidden_transforms":["text=True","encoding=","decode()","read_text()"],"required_full_subset_comparison":true},"correction_contract":{"production_return":"DEEP_IMMUTABLE_MAPPING_AND_TUPLE_UNCHANGED","test_only_json_semantic_adapter":true,"adapter_scope":"ASSERTION_ONLY_RECURSIVE_OBJECT_ARRAY_SCALAR_EQUIVALENCE","container_type_assertions":"REMAIN_SEPARATE_AND_STRICT","production_thaw_or_serializer":false,"custom_equality_owner":false,"source_modification":false},"validation":{"targeted":"ALL_TESTS_PASS","focused":"ALL_RELEVANT_CALLER_TESTS_PASS","full":"UNITTEST_DISCOVER_PASS","compileall":1,"codegraph_sync":1,"codegraph_post_query":1,"diff_check":1,"status_exact_two":1,"implementation_commit":1,"postcommit_targeted":1},"execution_budgets":{"committed_plan_byte_reads":1,"committed_full_byte_reads":1,"committed_archive_byte_reads":1,"machine_row_parser_calls":2,"pre_edit_status_checks":1,"pre_edit_identity_checks":1,"source_patch_writes":0,"test_patch_writes":1,"targeted_suites":1,"focused_suites":1,"full_suites":1,"compileall":1,"codegraph_sync":1,"codegraph_post_queries":1,"diff_checks":1,"status_checks":1,"implementation_commits":1,"postcommit_targeted_suites":1,"er_heading_index_reads":1,"er_complete_suffix_extractions":1,"er_apply_patch_appends":1,"postappend_operations":0,"retry":0,"fallback":0},"zero_budgets":{"new_parallel_parser_modules":0,"parser_owner_writes":0,"other_repository_source_writes":0,"other_repository_test_writes":0,"real_artifact_reads":0,"old_root_reads":0,"self_check_owner_calls":0,"canonical_validator_calls":0,"eligibility_emissions":0,"release_consumption":0,"release_copy":0,"release_generation":0,"release_qualification":0,"network":0,"device":0,"camera":0,"ray":0,"strip":0,"cleanup":0,"formal":0,"public_analyzer":0,"plan_writes_by_executer":0,"full_writes_by_executer":0,"archive_writes_by_executer":0},"required_full_machine_state":{"active_task_count":1,"active_task":"REF-P7-25-R2-B3-C3-C4-R5-R1-C1-R2-P1-C1-R1","active_plan_contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B3-C3-C4-R5-R1-C1-R2-P1-C1-R1-EXACT-BYTES-IMMUTABLE-EXPECTATION-CORRECTION-V1","retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","manifest_authority":"SUBORDINATE_EVIDENCE_ONLY_CANONICAL_VALIDATOR_SOLE_ELIGIBILITY_OWNER","machine_row_parser_owner_status":"ACTIVE_EXACT_BYTES_BOUNDED_IMMUTABLE_EXPECTATION_CORRECTION","real_execution_status":"BLOCKED_ON_P1_C1_R1_ACCEPTANCE","device_authorized_by_this_file":false},"successor_lock":"R2_SUCCESSOR_MUST_CALL_ACCEPTED_REPO_OWNED_HELPER_NO_HAND_WRITTEN_PARSER","orchestrator_commit_after_handoff":{"owner":"ORCHESTRATOR","executer_must_not_commit":true,"expected_subject":"chore(evidence): record exact-bytes immutable parser correction","expected_changed_paths":[".agent-work/EXECUTION_RESULT.md"]},"authorization":{"classification":"PURE_OFFLINE_EXACT_BYTES_ACTIVATION_TEST_CORRECTION_AND_REPOSITORY_VALIDATION","human_device_authorization_required":false,"advisor_scientific_decision_required":false},"expected_duration":"under_10_minutes","visible_terminal_required":false,"planner_stop":"B3_C3_C4_R5_R1_C1_R2_P1_C1_R1_EXACT_BYTES_IMMUTABLE_EXPECTATION_CORRECTION_WAITING_PLANNER_REVIEW"}`

## 1. Activation topology 与 exact-bytes machine-row gate

Activation必须是evidence commit `aea9ce3769dea41348d739ee92b36fa2f47889a5` direct child，subject exact `chore(plan): retry immutable parser correction with exact bytes`，changed paths exact FULL、PLAN与本轮archive。Orchestrator只提交这三个文档路径，必须保留P1现有exact two dirty implementation paths，不得把source/test误stage进activation commit。

Executer先核验HEAD topology、subject与exact changed paths。随后各一次从activation commit取得committed PLAN、FULL与archive的raw bytes：必须使用返回`bytes`的Git acquisition（例如不带`text`/`encoding`参数的`subprocess.check_output(["git","show",f"{activation}:{path}"])`），或者等价的`Path.read_bytes()`读取已由Git按identity冻结的文件；对PLAN/FULL的authoritative gate必须以activation commit中的Git bytes为准。严禁`text=True`、`encoding=`、`.decode()`、`.read_text()`或任何bytes→str→bytes往返。

把PLAN bytes直接传给当前`parse_plan_machine_contract`，FULL bytes直接传给当前`parse_full_plan_machine_state`，不得复制其内部扫描逻辑、不得搜索bare marker、不得写临时parser。比较PLAN contract、archive identity以及required FULL machine-state exact subset。archive committed bytes必须为bytes `4900`、SHA-256 `b9cd03b55ff291c7025627fa841d6ef6d946ea102eb7147803b5155870b5a00f`。任一gate失败立即封存，后续status/identity/source/test写入与validation全部`0`；同一尝试retry `0`。

Gate通过后一次`git status --short`必须exact显示以下两条且无第三条：

- ` M src/camera_based_rgbww_optimizer/utils/agent_work_machine_contract.py`
- ` M tests/test_agent_work_machine_contract.py`

随后以`Path.read_bytes()`等exact bytes方式核对preserved dirty identities：source bytes/SHA/blob `9414` / `a02a30c026fba548c81c04a277e2f235385ddb8a459c4ff2f73c91ee87c3737e` / `ce2200181bd2a493cfaab621daa17b89a13bdf1f`；test bytes/SHA/blob `13411` / `5e5aa5831edc50d695a09cb473333450f68820cfaddedc054d8bb010314ba920` / `5efc93c11b37de900f67b3d1c4aa734048d035fc`。任一不符即pre-edit hard fail；不得修正、恢复或重做P1 source/test。

## 2. Exact one test-only correction

Source当前dirty内容逐字不变，source patch/write exact `0`；`parser_owner_writes` exact `0`。唯一允许实现写入是`tests/test_agent_work_machine_contract.py`一次`apply_patch`，不得触碰第三路径。

Test patch合同沿用P1-C1，不得删减：

1. 在dedicated test内加入最小test-only recursive semantic comparison helper或等价逐层assertion。JSON object按exact keys和values比较，immutable `Mapping`与mutable expected dict视为语义对象；JSON array按exact顺序和元素比较，tuple与mutable expected list视为语义数组；scalar必须保持exact JSON value和type，bool不得被int相等掩盖。
2. 只把失败的custom-marker assertion与PLAN/FULL preserve-values assertion改用语义比较。`test_success_value_is_deeply_immutable`、type preservation、legacy-wrapper/core equality及negative matrix继续分别严格冻结container type和fail-closed行为；不得删除、skip、xfail或放宽。
3. Adapter只能位于test module且只用于assertion；不得加入production owner/public API/evidence serializer，不得thaw production返回，不得加入自定义Mapping/`__eq__`。
4. Test patch必须覆盖nested object、nested array以及bool/int/string/null scalar，不能只把expected list改成tuple。

若唯一test patch后targeted仍失败，立即停止并封存真实失败；retry/fallback为`0`，不得第二次patch source或test。

## 3. Validation、exact two-path commit 与 postcommit gate

严格依序、每项一次；任一步失败即停止，后续计数为`0`：

1. targeted：`.venv/bin/python -m unittest tests.test_agent_work_machine_contract -v`；必须全通过并记录actual count。
2. focused：`.venv/bin/python -m unittest tests.test_agent_work_machine_contract tests.test_p7_retained_r3_offline_patch_preflight tests.test_p7_retained_r3_exact_five_controller tests.test_p7_retained_r3_controller_integration -v`；必须全通过并记录actual count。
3. full：`.venv/bin/python -m unittest discover -s tests -v`；必须全通过并记录actual count。
4. compileall exact source/test；`codegraph sync`一次；post-query一次证明generic/legacy入口仍由同一production owner持有、没有parallel parser/caller authority，test-only adapter未进入production。
5. `git diff --check`通过；`git status --short`必须仍为exact source/test two paths。记录最终bytes、SHA-256与Git blob。
6. implementation commit parent必须是activation commit，subject exact `fix(p7): harden machine row parsing`，changed paths exact source/test；不得拆分或包含文档/evidence。
7. commit后targeted suite一次并全通过；不得再修改文件或追加第二个implementation commit。

本包预计低于10分钟，不用visible Terminal/automation，不访问设备。P1之前`13/15`与本轮前置失败不替代任何validation。

## 4. ER handoff、locks 与 stop

成功或任一terminal failure后，ER只允许一次结构化heading index read，定位最后level-2 section并精确读取该heading至physical EOF的完整suffix。唯一`apply_patch`必须以该完整suffix逐字作旧anchor、原样重放后紧接追加P1-C1-R1 canonical strict-JSON handoff，至少记录：activation topology、exact bytes acquisition方式与禁用转换、parser calls、FULL subset、archive identity、pre-edit status/identities、test-only correction、source/parser-owner write `0`、test write `1`、targeted/focused/full/compileall/CodeGraph/diff/status/commit/postcommit actual results、全部locks与Planner request。

ER append是Executer最后副作用；append后operations exact `0`，不得再读ER、status/hash/check或commit。Executer不得修改PLAN、FULL、archive，也不得提交ER；Orchestrator随后按machine row的exact subject/path提交ER。

P1-C1-R1验收前R2 successor锁定；验收后也只能调用accepted repo-owned helper，禁止新的external hand-written parser。real artifacts、old roots、self-check owner、canonical validator、eligibility、release、network、device、camera、Ray、strip、cleanup、formal与public analyzer全部`0`。retained R3保持`RETAINED_UNVALIDATED_UNCONSUMED`。

维护性判断：本包不改parser owner，只把activation调用恢复到其既有exact-bytes边界；原test-only correction将JSON语义和deep immutable container类型分开验证，single-owner边界不变，无需架构重构。
