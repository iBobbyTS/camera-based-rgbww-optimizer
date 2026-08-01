# REF-P7-25-R2-B2-P7-C1-C1-C1-C1-V1-C1-V1-C1：deferred ER append immutable validation closure

**计划状态：** `WAITING_ORCHESTRATOR_ACTIVATION`

**Planner 日期：** 2026-07-31

**Reference task：** `REF-P7-25-R2-B2-P7-C1-C1-C1-C1-V1-C1-V1-C1`

**Contract ID：**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-P7-C1-C1-C1-C1-V1-C1-V1-C1-DEFERRED-ER-APPEND-IMMUTABLE-VALIDATION-CLOSURE-V1`

**Planner decision：** reviewed V1-C1-V1 execution is
`REJECTED_PRE_GATE_INITIAL_CLEAN_SELF_CONTAMINATION_CANDIDATE_IMMUTABLE_NON_CONSUMABLE`。Activation、immutable candidate与ordinary `pregate_exit` wrapper均匹配；但wrapper在gate的initial-clean断言前向ER写入header，自致dirty并产生logical exit `1`。Evidence commit `045915d...`真实持久化exact one marker；targeted及后续验证均为`0`。这不是candidate code/test失败，不得repair或regenerate candidate。

**当前唯一动作：** Orchestrator审核并更新FULL后，以clean HEAD
`045915dae74b14c9a56d6524d5573a5bdeade4d4`为direct parent创建exact activation commit。Executer只验证immutable candidate `864f08c...`，code/test write与commit exact `0`。所有execution observations先完整保存在内存；initial-clean、完整pre-gate、fresh targeted11、focused93、compileall、full778及final-clean全部terminal后，才向ER single EOF append。Gate marker必须来自真实logical exit并在该sole append逐字持久化；禁止任何pre-gate ER byte。

**唯一 Planner stop：**
`B2_P7_C1_C1_C1_C1_V1_C1_V1_C1_DEFERRED_ER_APPEND_IMMUTABLE_VALIDATION_WAITING_PLANNER_REVIEW`。

**本轮新归档：**
`.agent-work/PLANS/20260731-1819-p7-retained-r3-b2-p7-pregate-append-order-failure-review.md`，bytes `6345`，SHA-256
`5a316e29a56090715307734ca954ee7de3265666999516d86d4bdb1e358a317d`；不得覆盖早期archive。

`PLAN_MACHINE_CONTRACT={"schema":"p7_td_b_retained_r3_option_b_b2_p7_c1_c1_c1_c1_v1_c1_v1_c1_deferred_er_append_immutable_validation_closure_v1","reference_task_id":"REF-P7-25-R2-B2-P7-C1-C1-C1-C1-V1-C1-V1-C1","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-P7-C1-C1-C1-C1-V1-C1-V1-C1-DEFERRED-ER-APPEND-IMMUTABLE-VALIDATION-CLOSURE-V1","execution_authorized_after_orchestrator_activation":true,"activation_commit":{"expected_parent":"045915dae74b14c9a56d6524d5573a5bdeade4d4","expected_subject":"chore(plan): activate p7 deferred er append validation closure","expected_changed_paths":[".agent-work/FULL_PLAN_REFERENCE.md",".agent-work/PLAN.md",".agent-work/PLANS/20260731-1819-p7-retained-r3-b2-p7-pregate-append-order-failure-review.md"],"clean_porcelain_required_after_activation":true},"required_full_machine_state":{"active_task_count":1,"active_task":"REF-P7-25-R2-B2-P7-C1-C1-C1-C1-V1-C1-V1-C1","active_plan_contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-P7-C1-C1-C1-C1-V1-C1-V1-C1-DEFERRED-ER-APPEND-IMMUTABLE-VALIDATION-CLOSURE-V1","retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","p5_runtime_owner_status":"ACCEPTED_COMPLETE_REPO_OWNED_CONTROLLER_RUNTIME_OWNER","p6_domain_template_owner_status":"ACCEPTED_COMPLETE_DETERMINISTIC_DOMAIN_TEMPLATE_OWNER_WITH_RUNNABLE_CONTRACT_RESIDUAL","p6_candidate_commit":"48b3979d6c0df5f488cd500597e26dc4c38877dd","p6_candidate_consumable":true,"p7_status":"REJECTED_PRE_GATE_INITIAL_CLEAN_SELF_CONTAMINATION_CANDIDATE_IMMUTABLE_NON_CONSUMABLE","p7_candidate_commit":"864f08cc5436519a37e41d553e49ebde4a3c8bb2","p7_candidate_consumable":false,"p7_implementation_commits":0,"executer_dispatched":true,"device_authorized_by_this_file":false},"rejected_validation":{"activation_commit":"56adae01902e9fde99270bc69db9cda5ee5afe53","activation_parent":"7d8a12178372ee34428665273086497da98f9099","activation_subject":"chore(plan): activate p7 outer plain validation closure","candidate_commit":"864f08cc5436519a37e41d553e49ebde4a3c8bb2","evidence_commit":"045915dae74b14c9a56d6524d5573a5bdeade4d4","wrapper_exit_capture_variable":"pregate_exit","pre_initial_clean_er_bytes_written":true,"gate_logical_exit":1,"persisted_marker":"PRE_GATE_LOGICAL_EXIT=1","persisted_marker_count":1,"er_append_lines":7,"targeted_invocations":0,"external_effects":0},"immutable_candidate":{"commit":"864f08cc5436519a37e41d553e49ebde4a3c8bb2","parent":"44fb7295f0f71030833476225350da01ce3c71d3","subject":"chore(p7): retain rejected outer plain nul candidate","changed_paths":["src/camera_based_rgbww_optimizer/utils/p7_retained_r3_controller_domain_template.py","tests/test_p7_retained_r3_controller_domain_template.py"],"canonical_binary_diff_sha256":"b03b1a049a407e2049f049b6f2514497e6d5bb82675f14dc750f00cc09ce6bd4","source_blob_oid":"5529ec27b3893c20995e9a8cb3a9fa5c0a87a3b5","source_bytes":19753,"source_sha256":"10969de79f5afece8018f094823efcf6f60237670ed1eeb54135f451ef0425c2","test_blob_oid":"d0f733426673aa9a57fcb1195ecea014f8c48062","test_bytes":27386,"test_sha256":"4c3b93d4a2f5967b91cb48a2dea1c0a0f8994fb687f6109830d24602bb93083e","template_bytes":11999,"template_sha256":"0369231f11bc968ebc343bac57acab236d75faf5d5d6e2b9c3d82918df19a467","replacement_bytes":1907,"replacement_sha256":"502c303e6257d8f59a4d5bbd39b0339371e210a8c10c9e8fa3fd0d2530160807","consumable_before_review":false},"exact_implementation_write_paths":[],"implementation_commit":{"count":0},"evidence_order_contract":{"initial_clean_before_any_er_bytes":true,"pre_initial_clean_er_bytes":0,"pre_terminal_er_bytes":0,"in_memory_buffer_required":true,"append_descriptor_may_open_early":true,"append_descriptor_truncate_forbidden":true,"successful_er_appends":1,"successful_er_marker":"PRE_GATE_LOGICAL_EXIT=0","successful_er_marker_count":1,"failure_before_initial_clean_er_appends":0,"ordinary_exit_capture_variable":"pregate_exit","prohibited_assignment_targets":["status","pipestatus","path","PATH","argv","ARGC","commands","functions","options","signals","parameters"]},"source_domain_contract":{"module_physical_nul_bytes":0,"outer_plain_ast_physical_nul_constants":1,"outer_plain_ast_physical_lf_constants":1,"outer_plain_ast_physical_cr_constants":1,"literal_backslash_x00_spec_text_accepted":true,"physical_nul_spec_text_rejected":true,"physical_nul_error_code_field_specific":true,"canonical_template_byte_identical":true,"canonical_template_physical_nul_bytes":0,"canonical_template_literal_backslash_x00_tokens":8,"canonical_template_literal_backslash_n_tokens":3,"exact_spec_replacement_byte_identical":true,"serializer_changes":0,"semantic_matrix_changes":0,"owner_api_dataclass_changes":0,"new_helpers":0,"fallbacks":0},"regression_contract":{"targeted_expected":11,"focused_expected":93,"full_expected":778},"execution_budgets":{"pregate_invocations":1,"targeted_invocations":1,"focused_invocations":1,"compileall_invocations":1,"full_invocations":1,"implementation_commits":0,"postcommit_targeted_invocations":0,"codegraph_sync":0,"codegraph_queries":0,"successful_execution_result_appends":1,"retry":0,"fallback":0},"zero_budgets":{"code_writes":0,"test_writes":0,"third_code_path":0,"pre_initial_clean_er_bytes":0,"pre_terminal_er_bytes":0,"template_edits":0,"replacement_edits":0,"serializer_edits":0,"matrix_edits":0,"owner_api_edits":0,"new_helper":0,"generic_allowlist":0,"plan_writes_by_executer":0,"full_writes_by_executer":0,"archive_writes_by_executer":0,"debug_writes":0,"guide_writes":0,"research_writes":0,"external_controller_writes":0,"external_controller_reads":0,"external_controller_processes":0,"external_root_creates":0,"external_root_reads":0,"synthetic_integration_runs":0,"old_failed_controller_reads":0,"old_failed_root_reads":0,"old_external_evidence_reads":0,"retained_artifact_reads":0,"candidate_payload_reads":0,"git_provenance_replay":0,"real_b2_dispatch":0,"subordinate_manifest_writes":0,"actual_canonical_validator_calls":0,"eligibility_emissions":0,"retained_release_audit":0,"release_generation":0,"release_qualification":0,"release_copy":0,"release_consumption":0,"network":0,"dns":0,"environment":0,"credentials":0,"device":0,"camera":0,"ray":0,"strip":0,"cleanup":0,"capture":0,"formal":0,"public_analyzer":0,"td_c":0,"sentinel":0,"p8":0,"firmware":0,"deployment":0},"expected_duration":"under_10_minutes","visible_terminal_required":false,"planner_stop":"B2_P7_C1_C1_C1_C1_V1_C1_V1_C1_DEFERRED_ER_APPEND_IMMUTABLE_VALIDATION_WAITING_PLANNER_REVIEW"}`

## 1. Activation and immutable inputs

Activation必须匹配machine row的exact parent、subject、three-path set，随后porcelain clean。FULL仅允许本task active；必须保持retained R3 unvalidated/unconsumed、P5/P6 accepted、candidate `864f08c...` immutable/non-consumable、implementation commits `0`、device authorization false。

Activation后、任何ER byte前只读核对：

1. candidate topology、exact two-path set及canonical binary diff；
2. source/test blob、bytes与SHA-256；
3. canonical template与exact-spec replacement bytes/SHA；
4. rejected activation/candidate/evidence topology及seven-line marker；
5. PLAN/FULL machine rows及new archive identity；
6. initially clean porcelain，candidate code/test bytes与HEAD完全一致。

任一不符必须fail closed。Accepted P7-C1 CodeGraph evidence继续冻结；本包CodeGraph exact `0/0`。不得读取old failed external controller/root/evidence、retained R3或candidate payload。

## 2. Immutable validation and evidence-write ordering

Code/test write exact `0/0`；不得形成working diff、stage、commit、amend或改写candidate。不得修改template、replacement、serializer、semantic matrix、owner/API/dataclass、helper、fallback、doc、skill或debug。

所有header、marker、counts、stdout/stderr摘要、identity与terminal result必须先保存在内存。可以提前以append-only/no-truncate方式打开ER descriptor，但在initial-clean和完整validation terminal前不得写入任何byte；不得用header、blank line、placeholder或marker预占位置。Success path只允许terminal时single EOF append。

若initial-clean assertion自身失败，ER writes exact `0`，直接在subagent handoff报告并停止；不得用写ER污染被诊断状态。若initial-clean已通过但后续gate/test失败，可在terminal后single EOF append真实failure evidence；不得重跑或repair。

每个validation stage后均只读核对candidate source/test identities与clean porcelain。任何漂移、untracked path或write必须fail closed。

## 3. Exact one semantic gate and real logical-exit marker

Executer运行exact one fresh fail-fast Python semantic pre-gate。Owning zsh wrapper必须：

1. Python body返回后立即以ordinary non-special `pregate_exit=$?`捕获logical exit；
2. exact once打印`PRE_GATE_LOGICAL_EXIT=${pregate_exit}`并保存在内存buffer；
3. 立即strictly核对整数`0`，nonzero则不运行tests；
4. 禁止向`status`、`pipestatus`、`path`、`PATH`、`argv`、`ARGC`、`commands`、`functions`、`options`、`signals`或`parameters`赋值；禁止alternative exit owner；
5. 禁止用pipeline/tee/subsequent-command exit、`|| true`、subshell swallowing、rerun或stdout推断替代exact `$?`。

Python gate必须重新证明activation/current path exact、initial clean、strict UTF-8、source/test AST parse+compile、methods exact `11`；candidate topology/diff/identities unchanged；module physical NUL bytes `0`；outer `_plain` AST physical NUL/LF/CR constants `1/1/1`；public physical-NUL negative与literal escape positive；template/replacement exact baseline identities及escape counts `8/3`；exact16 canonical matrix、test03/test08、runnable lifecycle与accepted boundaries不漂移；all code/test/external effects `0`。

## 4. Fresh regression and terminal append

仅在gate logical exit exact `0`后按顺序exact once：

1. `PYTHONUNBUFFERED=1 .venv/bin/python -m unittest tests.test_p7_retained_r3_controller_domain_template`，exact `11/11`、exit `0`、`OK`；
2. `PYTHONUNBUFFERED=1 .venv/bin/python -m unittest tests.test_p7_retained_r3_controller_domain_template tests.test_p7_retained_r3_controller_runtime tests.test_p7_retained_r3_controller_conformance tests.test_p7_retained_r3_controller_preparation tests.test_p7_retained_r3_provenance_io tests.test_agent_work_machine_contract`，exact `93/93`、exit `0`、`OK`；
3. `.venv/bin/python -m compileall -q src tests`，exit `0`；
4. unique `PYTHONUNBUFFERED=1 .venv/bin/python -m unittest discover -s tests -p 'test_*.py'`，single unified session、exact `778/778`、exit `0`、`OK`；
5. 最终核对candidate topology、all identities、source-domain contract、clean porcelain、zero writes/commits及zero external effects；
6. 所有检查terminal后，向`.agent-work/EXECUTION_RESULT.md` single EOF append，逐字持久化真实`PRE_GATE_LOGICAL_EXIT=0` exact once，并记录activation/candidate/final identities、fresh outputs、write ordering与residual locks；随后立即停在Planner review。

本包implementation commit、postcommit test、CodeGraph与retry/fallback均exact `0`。任一failure不得rerun、repair、lower counts或进入后续stage。

## 5. Acceptance boundary and hard locks

Success只报告
`deferred_er_append_immutable_validation_pass_waiting_for_planner`。Executer不得将candidate标记consumable或解锁integration；只有后续independent Planner review可接受。

External controller/source/root/process、synthetic integration、retained R3/candidate payload、Git provenance replay、real B2、subordinate manifest、canonical validator、eligibility、retained audit与所有release操作均locked `0`。Network、DNS、environment、credentials、device、camera、Ray、strip、cleanup、capture、FORMAL、public analyzer、TD-C、sentinel、P8、firmware、deployment全部hard locked `0`。不需要Human授权或Advisor scientific decision。

维护性判断：本包只纠正validation evidence append时序，不修改任何生产或测试owner，不新增抽象、状态或平行执行路径。

## 6. Final archive row

`ARCHIVE_IDENTITY={"path":".agent-work/PLANS/20260731-1819-p7-retained-r3-b2-p7-pregate-append-order-failure-review.md","bytes":6345,"sha256":"5a316e29a56090715307734ca954ee7de3265666999516d86d4bdb1e358a317d"}`
