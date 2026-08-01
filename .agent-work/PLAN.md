# P7 retained-R3 Option B：P1-C1-R1-C1 distinct evidence-owner test correction

**计划状态：** `WAITING_ORCHESTRATOR_ACTIVATION`

**Planner 日期：** `2026-08-01`

**Reference task：** `REF-P7-25-R2-B3-C3-C4-R5-R1-C1-R2-P1-C1-R1-C1`

**Contract：** `P7-TD-B-RETAINED-R3-OPTION-B-B3-C3-C4-R5-R1-C1-R2-P1-C1-R1-C1-EVIDENCE-OWNER-TEST-CORRECTION-V1`

**当前唯一动作：** 保留现有exact two-path dirty implementation；activation gate通过后，仅在dedicated test内一次bounded patch，把generic `PLAN_MACHINE_CONTRACT` owner与legacy `PLAN` owner分别冻结并比较其余exact evidence fields，然后完成targeted/focused/full、compileall、CodeGraph、exact two-path implementation commit和postcommit targeted合同，封存ER并停在Planner验收门。

**唯一 Planner stop：** `B3_C3_C4_R5_R1_C1_R2_P1_C1_R1_C1_EVIDENCE_OWNER_TEST_CORRECTION_WAITING_PLANNER_REVIEW`。

**本轮新归档：** `.agent-work/PLANS/20260801-1220-p7-retained-r3-b3-c3-c4-r5-r1-c1-r2-p1-c1-r1-targeted-review.md`；bytes `5811`，SHA-256 `a35b9af4fbb394656a432010945d7799cd754359bf8757082101adf00a2a48fa`。

`PLAN_MACHINE_CONTRACT={"schema":"p7_td_b_retained_r3_option_b_b3_c3_c4_r5_r1_c1_r2_p1_c1_r1_c1_evidence_owner_test_correction_v1","reference_task_id":"REF-P7-25-R2-B3-C3-C4-R5-R1-C1-R2-P1-C1-R1-C1","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B3-C3-C4-R5-R1-C1-R2-P1-C1-R1-C1-EVIDENCE-OWNER-TEST-CORRECTION-V1","reviewed_p1_c1_r1":{"activation":"1dcde91f4eefd449e7f9739f590ff2f5789f0a57","evidence":"4b512ecb3b5caf34c25decb45f967f466c3b8909","decision":"REJECTED_P1_C1_R1_COMPLETION_ACCEPTED_PHYSICAL_EOF_HANDOFF_DIRECT_TEST_ONLY_SUCCESSOR","targeted_tests":15,"targeted_failures":1,"failure":"GENERIC_AND_LEGACY_EVIDENCE_OWNER_EXPECTED_EQUAL_INCORRECTLY","er_heading_reads_actual":2,"er_heading_reads_budget":1,"physical_eof_handoff_valid":true,"supersession_required":false,"implementation_commit":0,"retry":0,"real_self_check":0,"eligibility":false,"release_consumable":false},"activation_commit":{"expected_parent":"4b512ecb3b5caf34c25decb45f967f466c3b8909","expected_subject":"chore(plan): correct parser evidence owner expectation","expected_changed_paths":[".agent-work/FULL_PLAN_REFERENCE.md",".agent-work/PLAN.md",".agent-work/PLANS/20260801-1220-p7-retained-r3-b3-c3-c4-r5-r1-c1-r2-p1-c1-r1-targeted-review.md"]},"archive":{"path":".agent-work/PLANS/20260801-1220-p7-retained-r3-b3-c3-c4-r5-r1-c1-r2-p1-c1-r1-targeted-review.md","bytes":5811,"sha256":"a35b9af4fbb394656a432010945d7799cd754359bf8757082101adf00a2a48fa"},"preserved_dirty":{"exact_paths":["src/camera_based_rgbww_optimizer/utils/agent_work_machine_contract.py","tests/test_agent_work_machine_contract.py"],"source":[9414,"a02a30c026fba548c81c04a277e2f235385ddb8a459c4ff2f73c91ee87c3737e","ce2200181bd2a493cfaab621daa17b89a13bdf1f"],"test":[14278,"a0d2a2298790e236fd6a58f393a62b25e44b487512077a3aeb4fb59fc333be2a","fce0395317f4ec1b2d75d918890eadf6694a3abf"],"source_patch_writes":0,"test_patch_writes":1,"implementation_expected_subject":"fix(p7): harden machine row parsing"},"correction_contract":{"generic_owner":"PLAN_MACHINE_CONTRACT","legacy_plan_owner":"PLAN","owner_values_intentionally_distinct":true,"remaining_evidence_fields_exact_equal":true,"production_return":"DEEP_IMMUTABLE_MAPPING_AND_TUPLE_UNCHANGED","existing_json_semantic_adapter_preserved":true,"container_type_assertions":"REMAIN_SEPARATE_AND_STRICT","source_modification":false,"production_thaw_or_serializer":false,"custom_equality_owner":false},"validation":{"targeted":"ALL_TESTS_PASS","focused":"ALL_RELEVANT_CALLER_TESTS_PASS","full":"UNITTEST_DISCOVER_PASS","compileall":1,"codegraph_sync":1,"codegraph_post_query":1,"diff_check":1,"status_exact_two":1,"implementation_commit":1,"postcommit_targeted":1},"execution_budgets":{"committed_plan_byte_reads":1,"committed_full_byte_reads":1,"committed_archive_byte_reads":1,"machine_row_parser_calls":2,"pre_edit_status_checks":1,"pre_edit_identity_checks":1,"source_patch_writes":0,"test_patch_writes":1,"targeted_suites":1,"focused_suites":1,"full_suites":1,"compileall":1,"codegraph_sync":1,"codegraph_post_queries":1,"diff_checks":1,"status_checks":1,"implementation_commits":1,"postcommit_targeted_suites":1,"er_heading_index_reads":1,"er_complete_suffix_extractions":1,"er_apply_patch_appends":1,"postappend_operations":0,"retry":0,"fallback":0},"zero_budgets":{"new_parallel_parser_modules":0,"parser_owner_writes":0,"other_repository_source_writes":0,"other_repository_test_writes":0,"real_artifact_reads":0,"old_root_reads":0,"self_check_owner_calls":0,"canonical_validator_calls":0,"eligibility_emissions":0,"release_consumption":0,"release_copy":0,"release_generation":0,"release_qualification":0,"network":0,"device":0,"camera":0,"ray":0,"strip":0,"cleanup":0,"formal":0,"public_analyzer":0,"plan_writes_by_executer":0,"full_writes_by_executer":0,"archive_writes_by_executer":0},"required_full_machine_state":{"active_task_count":1,"active_task":"REF-P7-25-R2-B3-C3-C4-R5-R1-C1-R2-P1-C1-R1-C1","active_plan_contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B3-C3-C4-R5-R1-C1-R2-P1-C1-R1-C1-EVIDENCE-OWNER-TEST-CORRECTION-V1","retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","manifest_authority":"SUBORDINATE_EVIDENCE_ONLY_CANONICAL_VALIDATOR_SOLE_ELIGIBILITY_OWNER","machine_row_parser_owner_status":"ACTIVE_DISTINCT_EVIDENCE_OWNER_TEST_CORRECTION","real_execution_status":"BLOCKED_ON_P1_C1_R1_C1_ACCEPTANCE","device_authorized_by_this_file":false},"successor_lock":"R2_SUCCESSOR_MUST_CALL_ACCEPTED_REPO_OWNED_HELPER_NO_HAND_WRITTEN_PARSER","orchestrator_commit_after_handoff":{"owner":"ORCHESTRATOR","executer_must_not_commit":true,"expected_subject":"chore(evidence): record parser evidence owner correction","expected_changed_paths":[".agent-work/EXECUTION_RESULT.md"]},"authorization":{"classification":"PURE_OFFLINE_TEST_ONLY_EVIDENCE_OWNER_CORRECTION_AND_REPOSITORY_VALIDATION","human_device_authorization_required":false,"advisor_scientific_decision_required":false},"expected_duration":"under_10_minutes","visible_terminal_required":false,"planner_stop":"B3_C3_C4_R5_R1_C1_R2_P1_C1_R1_C1_EVIDENCE_OWNER_TEST_CORRECTION_WAITING_PLANNER_REVIEW"}`

## 1. Activation topology、machine-row gate 与 preserved dirty identity

Activation必须是evidence commit `4b512ecb3b5caf34c25decb45f967f466c3b8909` direct child，subject exact `chore(plan): correct parser evidence owner expectation`，changed paths exact FULL、PLAN与本轮archive。Orchestrator只提交这三个文档路径，必须保留exact two dirty implementation paths，不得把source/test误stage进activation commit。

Executer先核验HEAD topology、subject与exact changed paths；随后各一次从activation commit取得committed PLAN、FULL与archive raw bytes。PLAN/FULL分别调用当前repo-owned `parse_plan_machine_contract`/`parse_full_plan_machine_state`，不得复制扫描逻辑或解码成text。比较PLAN contract、archive identity与required FULL exact subset。任一gate失败立即封存，后续status/identity/test写入与validation全部`0`；retry `0`。

Gate通过后一次`git status --short`必须exact只有source/test两条。核对source bytes/SHA/blob `9414` / `a02a30c026fba548c81c04a277e2f235385ddb8a459c4ff2f73c91ee87c3737e` / `ce2200181bd2a493cfaab621daa17b89a13bdf1f`；test bytes/SHA/blob `14278` / `a0d2a2298790e236fd6a58f393a62b25e44b487512077a3aeb4fb59fc333be2a` / `fce0395317f4ec1b2d75d918890eadf6694a3abf`。任一不符即hard fail，不得恢复或重做。

## 2. Exact one test-only correction

Source与parser owner write exact `0`。唯一实现写入是`tests/test_agent_work_machine_contract.py`一次`apply_patch`：在`test_generic_parser_supports_custom_marker_and_legacy_wrappers_delegate`中保留generic/legacy value equality，分别断言`generic.evidence.owner == "PLAN_MACHINE_CONTRACT"`与`legacy.evidence.owner == "PLAN"`；将两份`to_mapping()`复制为test-local mutable dict、各自移除并验证owner后，对所有剩余字段作exact equality。不得忽略其他field，不得改变production owner、generic owner derivation或legacy wrapper owner。

保留现有recursive JSON semantic adapter、nested object/array/scalar覆盖、deep immutable container/mutation assertions及全部negative matrix；不得删除、skip、xfail或放宽。若唯一test patch后targeted仍失败，立即停止并封存；不得第二次patch。

## 3. Validation、exact two-path commit 与 postcommit gate

严格依序且每项一次，任一步失败即停止：

1. targeted：`.venv/bin/python -m unittest tests.test_agent_work_machine_contract -v`，必须全通过。
2. focused：`.venv/bin/python -m unittest tests.test_agent_work_machine_contract tests.test_p7_retained_r3_offline_patch_preflight tests.test_p7_retained_r3_exact_five_controller tests.test_p7_retained_r3_controller_integration -v`，必须全通过。
3. full：`.venv/bin/python -m unittest discover -s tests -v`，必须全通过。
4. compileall exact source/test；`codegraph sync`一次；post-query一次证明generic/legacy入口仍同属single production owner且test adapter未进入production。
5. `git diff --check`通过；status仍exact source/test two paths；记录最终bytes、SHA-256与blob。
6. implementation commit parent必须是activation commit，subject exact `fix(p7): harden machine row parsing`，changed paths exact source/test。
7. commit后targeted suite一次并全通过；不得再改文件或追加第二实现commit。

本包预计低于10分钟，不用visible Terminal/automation，不访问设备。

## 4. ER handoff、locks 与 stop

成功或terminal failure后，ER只允许一次结构化heading index read，精确读取最后level-2 heading至physical EOF完整suffix；唯一`apply_patch`逐字重放suffix后追加canonical strict-JSON handoff。至少记录activation、machine-row gates、dirty identities、distinct owner correction、source/parser writes `0`、test write `1`、全部validation actuals、commit、locks与Planner request。

ER append必须是Executer最后副作用，postappend operations `0`；Executer不得提交ER。Orchestrator随后按machine row exact subject/path提交ER。

P1-C1-R1-C1验收前R2 successor锁定；验收后也只能调用accepted repo-owned helper。real artifacts、old roots、self-check owner、canonical validator、eligibility、release、network、device、camera、Ray、strip、cleanup、formal与public analyzer全部`0`；retained R3保持`RETAINED_UNVALIDATED_UNCONSUMED`。

维护性判断：本包只更正dedicated test对generic/legacy evidence owner的错误期望，production single-owner、deep immutability与wrapper边界不变，无需架构重构。
