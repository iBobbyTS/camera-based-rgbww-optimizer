# P7 retained-R3 Option B：P1-C1 immutable parser test expectation correction

**计划状态：** `WAITING_ORCHESTRATOR_ACTIVATION`

**Planner 日期：** `2026-08-01`

**Reference task：** `REF-P7-25-R2-B3-C3-C4-R5-R1-C1-R2-P1-C1`

**Contract：** `P7-TD-B-RETAINED-R3-OPTION-B-B3-C3-C4-R5-R1-C1-R2-P1-C1-IMMUTABLE-EXPECTATION-CORRECTION-V1`

**当前唯一动作：** 保留P1现有exact two-path dirty implementation，只在dedicated test内一次bounded patch，把两处stale mutable dict/list equality expectation改为test-only JSON semantic comparison，同时继续独立冻结deep immutable container type；随后从targeted开始完成focused/full、compileall、CodeGraph与exact two-path implementation commit验证，封存ER并停在Planner验收门。

**唯一 Planner stop：** `B3_C3_C4_R5_R1_C1_R2_P1_C1_IMMUTABLE_EXPECTATION_CORRECTION_WAITING_PLANNER_REVIEW`。

**本轮新归档：** `.agent-work/PLANS/20260801-1204-p7-retained-r3-b3-c3-c4-r5-r1-c1-r2-p1-targeted-review.md`；bytes `5435`，SHA-256 `5730e2d986fd85b1b4d65207f126b9df4c4ca0758693e310d87d4eff23d3fab3`。

`PLAN_MACHINE_CONTRACT={"schema":"p7_td_b_retained_r3_option_b_b3_c3_c4_r5_r1_c1_r2_p1_c1_immutable_expectation_correction_v1","reference_task_id":"REF-P7-25-R2-B3-C3-C4-R5-R1-C1-R2-P1-C1","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B3-C3-C4-R5-R1-C1-R2-P1-C1-IMMUTABLE-EXPECTATION-CORRECTION-V1","reviewed_p1":{"activation":"6d2a8c24554a9235f028a85ac316c25bca1951af","evidence":"6a8ae8fcbecb311bfe53c3cc4d13773ef49956be","decision":"REJECTED_P1_COMPLETION_PRESERVE_CONTRACTUAL_IMPLEMENTATION_FOR_BOUNDED_TEST_CORRECTION","targeted_run":15,"targeted_passed":13,"targeted_failed":2,"focused":0,"full":0,"implementation_commit":0,"first_failure":"STALE_MUTABLE_NESTED_DICT_LIST_EQUALITY_EXPECTATIONS","real_self_check":0,"eligibility":false,"release_consumable":false},"activation_commit":{"expected_parent":"6a8ae8fcbecb311bfe53c3cc4d13773ef49956be","expected_subject":"chore(plan): correct immutable parser expectations","expected_changed_paths":[".agent-work/FULL_PLAN_REFERENCE.md",".agent-work/PLAN.md",".agent-work/PLANS/20260801-1204-p7-retained-r3-b3-c3-c4-r5-r1-c1-r2-p1-targeted-review.md"]},"archive":{"path":".agent-work/PLANS/20260801-1204-p7-retained-r3-b3-c3-c4-r5-r1-c1-r2-p1-targeted-review.md","bytes":5435,"sha256":"5730e2d986fd85b1b4d65207f126b9df4c4ca0758693e310d87d4eff23d3fab3"},"preserved_dirty":{"exact_paths":["src/camera_based_rgbww_optimizer/utils/agent_work_machine_contract.py","tests/test_agent_work_machine_contract.py"],"source":[9414,"a02a30c026fba548c81c04a277e2f235385ddb8a459c4ff2f73c91ee87c3737e","ce2200181bd2a493cfaab621daa17b89a13bdf1f"],"test":[13411,"5e5aa5831edc50d695a09cb473333450f68820cfaddedc054d8bb010314ba920","5efc93c11b37de900f67b3d1c4aa734048d035fc"],"source_patch_writes":0,"test_patch_writes":1,"implementation_expected_subject":"fix(p7): harden machine row parsing"},"correction_contract":{"production_return":"DEEP_IMMUTABLE_MAPPING_AND_TUPLE_UNCHANGED","test_only_json_semantic_adapter":true,"adapter_scope":"ASSERTION_ONLY_RECURSIVE_OBJECT_ARRAY_SCALAR_EQUIVALENCE","container_type_assertions":"REMAIN_SEPARATE_AND_STRICT","production_thaw_or_serializer":false,"custom_equality_owner":false,"source_modification":false},"validation":{"targeted":"ALL_TESTS_PASS","focused":"ALL_RELEVANT_CALLER_TESTS_PASS","full":"UNITTEST_DISCOVER_PASS","compileall":1,"codegraph_sync":1,"codegraph_post_query":1,"diff_check":1,"status_exact_two":1,"implementation_commit":1,"postcommit_targeted":1},"execution_budgets":{"committed_plan_reads":1,"committed_full_reads":1,"review_archive_reads":1,"pre_edit_status_checks":1,"pre_edit_identity_checks":1,"source_patch_writes":0,"test_patch_writes":1,"targeted_suites":1,"focused_suites":1,"full_suites":1,"compileall":1,"codegraph_sync":1,"codegraph_post_queries":1,"diff_checks":1,"status_checks":1,"implementation_commits":1,"postcommit_targeted_suites":1,"er_heading_index_reads":1,"er_complete_suffix_extractions":1,"er_apply_patch_appends":1,"postappend_operations":0,"retry":0,"fallback":0},"zero_budgets":{"new_parallel_parser_modules":0,"other_repository_source_writes":0,"other_repository_test_writes":0,"production_owner_writes":0,"real_artifact_reads":0,"old_root_reads":0,"self_check_owner_calls":0,"canonical_validator_calls":0,"eligibility_emissions":0,"release_consumption":0,"release_copy":0,"release_generation":0,"release_qualification":0,"network":0,"device":0,"camera":0,"ray":0,"strip":0,"cleanup":0,"formal":0,"public_analyzer":0,"plan_writes_by_executer":0,"full_writes_by_executer":0,"archive_writes_by_executer":0},"required_full_machine_state":{"active_task_count":1,"active_task":"REF-P7-25-R2-B3-C3-C4-R5-R1-C1-R2-P1-C1","active_plan_contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B3-C3-C4-R5-R1-C1-R2-P1-C1-IMMUTABLE-EXPECTATION-CORRECTION-V1","retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","manifest_authority":"SUBORDINATE_EVIDENCE_ONLY_CANONICAL_VALIDATOR_SOLE_ELIGIBILITY_OWNER","machine_row_parser_owner_status":"ACTIVE_BOUNDED_IMMUTABLE_EXPECTATION_CORRECTION","real_execution_status":"BLOCKED_ON_P1_C1_ACCEPTANCE","device_authorized_by_this_file":false},"successor_lock":"R2_SUCCESSOR_MUST_CALL_ACCEPTED_REPO_OWNED_HELPER_NO_HAND_WRITTEN_PARSER","orchestrator_commit_after_handoff":{"owner":"ORCHESTRATOR","executer_must_not_commit":true,"expected_subject":"chore(evidence): record immutable parser correction","expected_changed_paths":[".agent-work/EXECUTION_RESULT.md"]},"authorization":{"classification":"PURE_OFFLINE_TEST_CORRECTION_AND_REPOSITORY_VALIDATION","human_device_authorization_required":false,"advisor_scientific_decision_required":false},"expected_duration":"under_10_minutes","visible_terminal_required":false,"planner_stop":"B3_C3_C4_R5_R1_C1_R2_P1_C1_IMMUTABLE_EXPECTATION_CORRECTION_WAITING_PLANNER_REVIEW"}`

## 1. Activation gate 与 preserved-dirty precondition

Activation必须是evidence commit `6a8ae8fcbecb311bfe53c3cc4d13773ef49956be` direct child，subject exact `chore(plan): correct immutable parser expectations`，commit changed paths exact FULL、PLAN与本轮archive。Orchestrator必须只提交这三个Planner/Orchestrator文档路径，保留P1的两个uncommitted implementation paths；不得把它们误stage进activation commit。

Executer各读取一次committed PLAN、committed FULL与本轮review archive。使用仓库当前`agent_work_machine_contract`入口解析PLAN/FULL machine rows并核对required FULL subset；读取是纯repository validation，不接受P1实现。一次pre-edit status必须exact显示以下两条且不得有第三条：

- ` M src/camera_based_rgbww_optimizer/utils/agent_work_machine_contract.py`
- ` M tests/test_agent_work_machine_contract.py`

随后核对两路径preserved dirty identities exact：source bytes/SHA/blob `9414` / `a02a30c026fba548c81c04a277e2f235385ddb8a459c4ff2f73c91ee87c3737e` / `ce2200181bd2a493cfaab621daa17b89a13bdf1f`；test bytes/SHA/blob `13411` / `5e5aa5831edc50d695a09cb473333450f68820cfaddedc054d8bb010314ba920` / `5efc93c11b37de900f67b3d1c4aa734048d035fc`。任一不符即pre-edit hard fail，source/test写入与所有测试保持`0`。

本纠偏不得重读real artifacts、old roots、validator或release payload。P1的CodeGraph preflight和source implementation不重做；本包只修dedicated test并验证。

## 2. Exact one test patch correction

source path保持当前dirty内容逐字不变，source patch/write budget exact `0`。唯一允许写入是`tests/test_agent_work_machine_contract.py`一次`apply_patch`，不得触碰第三个path。

Test patch合同：

1. 在dedicated test内加入最小test-only recursive semantic comparison helper，或用等价的逐层assertion：JSON object按exact keys与values比较，immutable Mapping与mutable expected dict视为语义容器；JSON array按exact顺序与元素比较，tuple与mutable expected list视为语义容器；scalar必须保持exact JSON value与type，特别是bool不得被int比较掩盖。
2. 仅把失败的通用custom marker断言与PLAN/FULL preserve-values断言改为该语义比较。`test_success_value_is_deeply_immutable`、type preservation、legacy-wrapper/core equality及negative matrix必须保留，不得删除、skip、xfail或放宽。
3. Adapter只能存在于test module且只用于断言；不得加入production owner、public API或evidence serializer。不得将mappingproxy/tuple thaw后作为production返回，不得引入自定义Mapping class或`__eq__`绕过合同。
4. Test patch应明确覆盖nested object、nested array及bool/int/string/null scalar；不得仅把expected list机械改成tuple而遗漏递归mapping语义。

若一次test patch后targeted仍失败，立即停止并封存真实失败；retry/fallback为`0`，不得再patch source或test。

## 3. Validation 与 implementation commit

严格按以下顺序，每项只运行一次；任一步失败立即停止，后续计数为`0`：

1. targeted：`.venv/bin/python -m unittest tests.test_agent_work_machine_contract -v`；必须全通过并记录actual test count。
2. focused：`.venv/bin/python -m unittest tests.test_agent_work_machine_contract tests.test_p7_retained_r3_offline_patch_preflight tests.test_p7_retained_r3_exact_five_controller tests.test_p7_retained_r3_controller_integration -v`；必须全通过并记录count。
3. full：`.venv/bin/python -m unittest discover -s tests -v`；必须全通过并记录count。
4. compileall exact source/test；`codegraph sync`一次；post-query一次，证明generic与legacy入口仍在同一owner、无parallel module/caller authority，且test-only adapter未进入production。
5. `git diff --check`通过；`git status --short`必须exact two modified paths，无第三条dirty/untracked path。记录after bytes、SHA-256与Git blob。
6. implementation commit parent必须是activation commit，subject exact `fix(p7): harden machine row parsing`，changed paths exact source/test。不得拆分或添加其他path。
7. commit后targeted suite再运行一次并全通过；不得再修改文件或追加第二个implementation commit。

本包预计低于10分钟，不使用visible Terminal、automation或设备。focused/full通过才证明caller compatibility；P1之前的13/15不替代本轮任何suite。

## 4. ER handoff、locks 与 stop

实现成功或任一terminal failure后，ER只允许一次结构化heading index read，定位最后一个level-2 section；从该heading精确读取完整suffix至physical EOF。唯一`apply_patch`以完整suffix逐字作旧anchor，原样重放并紧接追加P1-C1 canonical strict-JSON handoff，至少记录：activation topology、P1 review decision、preserved before identities、test-only correction方式、source write `0`、test write `1`、targeted/focused/full/compileall/CodeGraph/diff/status/commit/postcommit结果、actual counts、所有locks及Planner request。

ER append是Executer最后一个副作用；成功后postappend operations exact `0`，不得再读ER、运行status/hash/check或commit。Executer不得修改PLAN、FULL、archive，也不得提交ER；Orchestrator随后按machine row以exact subject/path提交ER。

P1-C1验收前R2 successor锁定；验收后successor也只能调用accepted repo-owned helper，禁止新的external hand-written parser。real artifacts、old roots、real self-check owner、canonical validator、eligibility、release、network、device、camera、Ray、strip、cleanup、formal与public analyzer全部`0`。retained R3继续`RETAINED_UNVALIDATED_UNCONSUMED`。

维护性判断：纠偏只修dedicated test的语义比较，不给production owner增加compatibility/thaw层；deep immutability与JSON语义被分开验证，existing single-owner边界不变。完整focused/full仍是接受前硬门，无需架构重构。
