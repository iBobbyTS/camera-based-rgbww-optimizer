# P7 retained-R3 Option B：P1 repo-owned machine-row parser owner hardening

**计划状态：** `WAITING_ORCHESTRATOR_ACTIVATION`

**Planner 日期：** `2026-08-01`

**Reference task：** `REF-P7-25-R2-B3-C3-C4-R5-R1-C1-R2-P1`

**Contract：** `P7-TD-B-RETAINED-R3-OPTION-B-B3-C3-C4-R5-R1-C1-R2-P1-REPO-OWNED-MACHINE-ROW-PARSER-V1`

**当前唯一动作：** 在仓库既有唯一machine-row owner及其dedicated test这exact two paths内，建立接受完整text与literal marker的通用纯函数API，补齐Markdown wrapper、whole-line backtick、strict JSON object及deep immutability合同；完成focused/full validation与唯一implementation commit后封存ER handoff，停在Planner验收门。

**唯一 Planner stop：** `B3_C3_C4_R5_R1_C1_R2_P1_MACHINE_ROW_PARSER_OWNER_WAITING_PLANNER_REVIEW`。

**本轮新归档：** `.agent-work/PLANS/20260801-1153-p7-retained-r3-b3-c3-c4-r5-r1-c1-r2-review.md`；bytes `5088`，SHA-256 `3425edb05e79fb50672e0a87746e0a331b446598b73398d5e963c69f49458b38`。

`PLAN_MACHINE_CONTRACT={"schema":"p7_td_b_retained_r3_option_b_b3_c3_c4_r5_r1_c1_r2_p1_repo_owned_machine_row_parser_v1","reference_task_id":"REF-P7-25-R2-B3-C3-C4-R5-R1-C1-R2-P1","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B3-C3-C4-R5-R1-C1-R2-P1-REPO-OWNED-MACHINE-ROW-PARSER-V1","reviewed_r2":{"activation":"5b0d7259c1c6a1211f8981ea0d41ac0832a7e7c6","evidence":"89099740bc0b4fa8babc3be233a5f53ab3d697b2","decision":"REJECTED_R2_ACCEPTED_COMPLETE_PHYSICAL_EOF_ZERO_EFFECT_HANDOFF","first_failure":"FULL_PLAN_MACHINE_STATE_EXACT_BOUNDARY_NOT_UNIQUE","source_writes":0,"test_writes":0,"tests":0,"real_self_check":0,"eligibility":false,"release_consumable":false},"activation_commit":{"expected_parent":"89099740bc0b4fa8babc3be233a5f53ab3d697b2","expected_subject":"chore(plan): harden machine row parser owner","expected_changed_paths":[".agent-work/FULL_PLAN_REFERENCE.md",".agent-work/PLAN.md",".agent-work/PLANS/20260801-1153-p7-retained-r3-b3-c3-c4-r5-r1-c1-r2-review.md"]},"archive":{"path":".agent-work/PLANS/20260801-1153-p7-retained-r3-b3-c3-c4-r5-r1-c1-r2-review.md","bytes":5088,"sha256":"3425edb05e79fb50672e0a87746e0a331b446598b73398d5e963c69f49458b38"},"implementation":{"exact_paths":["src/camera_based_rgbww_optimizer/utils/agent_work_machine_contract.py","tests/test_agent_work_machine_contract.py"],"before":[["src/camera_based_rgbww_optimizer/utils/agent_work_machine_contract.py",7230,"743e2948f6c30a31fde5d072c8effa8b1365d321b303d61e9899ad18ac41825f","5c581f9b502bcab1809b6a61a082a47f4150e09f"],["tests/test_agent_work_machine_contract.py",9820,"32c0d47cfcdfa49ecad2a4976f401021f0ff1bef947eab705a8c89836b2f5a19","c9589947e876920f0cbd2fe7e113592e3cd390e1"]],"owner_disposition":"EXTEND_EXISTING_SINGLE_OWNER_NOT_PARALLEL_NEW_MODULE","public_generic_api":"parse_machine_row","input":"COMPLETE_TEXT_AND_LITERAL_MARKER","output":"DEEP_IMMUTABLE_MAPPING","filesystem_io":false,"runner_authority":false,"validator_authority":false,"eligibility_authority":false,"release_authority":false,"writer":false,"expected_subject":"fix(p7): harden machine row parsing"},"parser_contract":{"valid_row":"EXACT_OPENING_BACKTICK_PLUS_LITERAL_MARKER_PLUS_STRICT_JSON_OBJECT_PLUS_FINAL_CLOSING_BACKTICK_PLUS_LF","candidate_count":1,"whole_line_backticks":2,"duplicate_keys":"REJECT","nonfinite":"REJECT","top_level":"OBJECT_ONLY","nested_mapping":"MAPPING_PROXY","arrays":"TUPLE","legacy_plan_full_entrypoints":"PRESERVE_AND_DELEGATE_TO_SINGLE_CORE","reject":["bare","unwrapped","multiline","missing","duplicate","trailing","extra_backticks","crlf","eof_without_lf","invalid_utf8_or_text","malformed_json","duplicate_keys","nonfinite","non_object"]},"validation":{"codegraph_preflight":1,"targeted":"ALL_TESTS_PASS","focused":"ALL_RELEVANT_CALLER_TESTS_PASS","full":"UNITTEST_DISCOVER_PASS","compileall":1,"codegraph_sync":1,"codegraph_post_query":1,"diff_check":1,"status_exact_two":1,"implementation_commit":1,"postcommit_targeted":1},"execution_budgets":{"committed_plan_reads":1,"committed_full_reads":1,"accepted_archive_reads":1,"pre_edit_status_checks":1,"codegraph_preflight_queries":1,"source_patch_writes":1,"test_patch_writes":1,"targeted_suites":1,"focused_suites":1,"full_suites":1,"compileall":1,"codegraph_sync":1,"codegraph_post_queries":1,"diff_checks":1,"status_checks":1,"implementation_commits":1,"postcommit_targeted_suites":1,"er_heading_index_reads":1,"er_complete_suffix_extractions":1,"er_apply_patch_appends":1,"postappend_operations":0,"retry":0,"fallback":0},"zero_budgets":{"new_parallel_parser_modules":0,"other_repository_source_writes":0,"other_repository_test_writes":0,"real_artifact_reads":0,"old_root_reads":0,"self_check_owner_calls":0,"canonical_validator_calls":0,"eligibility_emissions":0,"release_consumption":0,"release_copy":0,"release_generation":0,"release_qualification":0,"network":0,"device":0,"camera":0,"ray":0,"strip":0,"cleanup":0,"formal":0,"public_analyzer":0,"plan_writes_by_executer":0,"full_writes_by_executer":0,"archive_writes_by_executer":0},"required_full_machine_state":{"active_task_count":1,"active_task":"REF-P7-25-R2-B3-C3-C4-R5-R1-C1-R2-P1","active_plan_contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B3-C3-C4-R5-R1-C1-R2-P1-REPO-OWNED-MACHINE-ROW-PARSER-V1","retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","manifest_authority":"SUBORDINATE_EVIDENCE_ONLY_CANONICAL_VALIDATOR_SOLE_ELIGIBILITY_OWNER","machine_row_parser_owner_status":"ACTIVE_REPO_OWNED_PURE_FUNCTION_HARDENING","real_execution_status":"BLOCKED_ON_P1_ACCEPTANCE","device_authorized_by_this_file":false},"successor_lock":"R2_SUCCESSOR_MUST_CALL_ACCEPTED_REPO_OWNED_HELPER_NO_HAND_WRITTEN_PARSER","orchestrator_commit_after_handoff":{"owner":"ORCHESTRATOR","executer_must_not_commit":true,"expected_subject":"chore(evidence): record machine row parser owner","expected_changed_paths":[".agent-work/EXECUTION_RESULT.md"]},"authorization":{"classification":"PURE_OFFLINE_REPOSITORY_IMPLEMENTATION_AND_TESTING","human_device_authorization_required":false,"advisor_scientific_decision_required":false},"expected_duration":"under_10_minutes","visible_terminal_required":false,"planner_stop":"B3_C3_C4_R5_R1_C1_R2_P1_MACHINE_ROW_PARSER_OWNER_WAITING_PLANNER_REVIEW"}`

## 1. Activation gate 与维护性边界

Activation必须是`89099740bc0b4fa8babc3be233a5f53ab3d697b2` direct child，subject exact `chore(plan): harden machine row parser owner`，changed paths exact FULL、PLAN与本轮archive。committed PLAN、FULL、archive各读取一次；使用仓库当前accepted入口提取PLAN/FULL machine rows并核对required FULL subset。一次pre-edit `git status --short`必须为空；任一dirty/untracked path即在edit前hard fail。

先运行一次CodeGraph preflight，范围仅限：现有`agent_work_machine_contract` owner、dedicated test、两个public wrapper及其直接caller/test blast radius。该查询用于确认单一owner边界，不得搜索或读取real artifacts、old roots、validator或release payload。

维护性预检已冻结：仓库已有`agent_work_machine_contract.py`及`test_agent_work_machine_contract.py`，所以本包只能强化这exact two existing paths。禁止新增第二个machine-row module、compatibility wrapper、writer、runner或parallel authority；现有PLAN/FULL专用入口必须复用同一内部parse core。

## 2. Exact two-path pure parser implementation

唯一source path：`src/camera_based_rgbww_optimizer/utils/agent_work_machine_contract.py`。唯一test path：`tests/test_agent_work_machine_contract.py`。activation identities必须与machine row一致；source和test各至多一次`apply_patch`，不得触碰其他path。

实现合同：

1. 新增并export通用纯函数`parse_machine_row`，接受完整exact text和literal marker，例如`FULL_PLAN_MACHINE_STATE=`或`PLAN_MACHINE_CONTRACT=`；marker本身不得包含opening/closing backtick、CR/LF或空值。若保留bytes adapter，只能位于同一owner内且不得产生第二套语法。
2. 唯一合法candidate必须是一个完整独立line：exact opening backtick、紧接literal marker、紧接strict JSON object、final closing backtick、最后exact LF。whole line内backtick数量必须exact `2`。
3. complete text内符合该wrapped literal marker的candidate必须exact `1`。bare marker、无wrapper、indent/prefix、missing、duplicate、multiline payload、closing backtick后trailing字符、extra backticks、CRLF、EOF without LF全部fail closed。
4. inner JSON必须UTF-8/Unicode-valid strict object；任意深度duplicate key、`NaN`/`Infinity`/`-Infinity`、malformed JSON与top-level non-object全部fail closed。不得coerce bool/int/string/null类型。
5. 成功返回值必须deep immutable：object每一层为`MappingProxyType`或等价read-only `Mapping`，array每一层为tuple，scalar保持exact JSON类型。调用方不得能通过nested mutation改变结果。
6. `parse_plan_machine_contract`与`parse_full_plan_machine_state`兼容入口保留，并委派同一个core；`ParsedMachineContract.value`同步收紧为deep immutable Mapping。既有evidence identity与fail-closed error code应保持或作最小、测试覆盖的兼容扩展。
7. owner只能import纯解析/immutability所需stdlib，或复用P3严格decode primitive；不得filesystem I/O、`pathlib`/`os`、subprocess/runner、environment、writer、canonical validator callback、eligibility、release或device authority。

Dedicated tests必须验证：valid PLAN/FULL/custom marker；nested mapping/list不可变；legacy wrappers与generic core结果一致；candidate唯一性；bare/unwrapped/indented/prefixed/multiline/duplicate/trailing/extra-backtick/CRLF/no-LF拒绝；invalid type/marker/UTF-8；malformed/duplicate/nonfinite/non-object拒绝；bool/int exact type不coerce；public surface与no-I/O/no-authority边界。不得修改现有caller以绕过owner。

## 3. Validation 与 implementation commit

顺序严格且每项只运行一次：

1. targeted：`.venv/bin/python -m unittest tests.test_agent_work_machine_contract -v`；全通过并记录实际test count。
2. focused：`.venv/bin/python -m unittest tests.test_agent_work_machine_contract tests.test_p7_retained_r3_offline_patch_preflight tests.test_p7_retained_r3_exact_five_controller tests.test_p7_retained_r3_controller_integration -v`；全通过。
3. full：`.venv/bin/python -m unittest discover -s tests -v`；全通过。
4. compileall exact two paths；`codegraph sync`一次；post-query一次，证明generic与legacy入口同一owner且无新parallel caller path。
5. `git diff --check`通过，`git status --short`必须exact two modified paths，无其他dirty/untracked path。
6. implementation commit parent必须是activation，subject exact `fix(p7): harden machine row parsing`，changed paths exact two。commit后targeted suite再运行一次并全通过。

任一步失败立即停止，后续计数保持`0`；retry/fallback均`0`。不得因test failure修改第三个path、降低合同或跳过full suite。本包预计低于10分钟，不使用visible Terminal/automation流程。

## 4. ER handoff、locks 与 stop

实现或任一失败terminal后，ER只允许一次结构化heading index读，定位最后一个level-2 section；再从该heading精确读取完整suffix至physical EOF。唯一`apply_patch`以完整suffix逐字作旧anchor，原样重放并紧接追加P1 canonical strict-JSON handoff，记录activation、R2 review、preflight、before/after identities、API/export、negative matrix、targeted/focused/full/compileall/CodeGraph/diff/commit结果、所有locks与Planner request。

ER append是Executer最后一个副作用；成功后postappend operations exact`0`，不得再读ER、运行status/hash/check或commit。Executer不得修改PLAN、FULL或archive，也不得提交ER；Orchestrator随后按machine row以exact subject/path提交ER。

P1验收前，任何R2 successor不得运行；验收后也只能调用accepted repo-owned helper，禁止新的external hand-written parser。real artifacts、old roots、real self-check owner、canonical validator、eligibility、release、network、device、camera、Ray、strip、cleanup、formal与public analyzer全部`0`。retained R3继续`RETAINED_UNVALIDATED_UNCONSUMED`。

维护性判断：本包把反复退化的Markdown machine-row语法集中到既有单一owner，并用dedicated negative matrix冻结error boundary；exact two-path修改不引入I/O、runner或eligibility authority，后续R2 successor只能消费已验收helper，无需额外架构重构。
