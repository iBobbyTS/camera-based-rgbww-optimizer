# REF-P7-25-R2-B2-P7-C1-C1-C1-C1-V1-C1-V1：immutable candidate validation-only closure

**计划状态：** `WAITING_ORCHESTRATOR_ACTIVATION`

**Planner 日期：** 2026-07-31

**Reference task：** `REF-P7-25-R2-B2-P7-C1-C1-C1-C1-V1-C1-V1`

**Contract ID：**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-P7-C1-C1-C1-C1-V1-C1-V1-IMMUTABLE-CANDIDATE-VALIDATION-ONLY-CLOSURE-V1`

**Planner decision：** reviewed V1-C1 execution is
`REJECTED_PRE_GATE_LOGICAL_EXIT_PERSISTENCE_WRAPPER_FAILURE_CANDIDATE_IMMUTABLE_NON_CONSUMABLE`。Activation、candidate identities及exact two-path correction均形成；唯一Python pre-gate body的全部语义断言通过，但zsh wrapper向readonly special parameter `status`赋值，导致logical exit `0`未打印、未持久化，后续tests均为`0`。这是execution packaging defect，不是source/test语义失败。Candidate `864f08c...`冻结为immutable且non-consumable；无需再改code/test。

**当前唯一动作：** Orchestrator审核并更新FULL后，以clean HEAD
`7d8a12178372ee34428665273086497da98f9099`为direct parent创建exact activation commit。Executer不得写code/test；只对immutable candidate `864f08c...`运行exact one fresh pre-gate。Wrapper只用ordinary non-special variable `pregate_exit`捕获、打印、核对logical exit `0`，并在sole ER append中持久化exact marker；禁止`status`、`path`等special variables。Gate通过后运行fresh targeted11、focused93、compileall与unique full778；CodeGraph、implementation commit、postcommit test、retry/fallback和所有external/retained/device effects均为`0`。ER append once后停回Planner。

**唯一 Planner stop：**
`B2_P7_C1_C1_C1_C1_V1_C1_V1_IMMUTABLE_CANDIDATE_VALIDATION_ONLY_WAITING_PLANNER_REVIEW`。

**本轮新归档：**
`.agent-work/PLANS/20260731-1808-p7-retained-r3-b2-p7-outer-plain-wrapper-failure-review.md`，bytes `6804`，SHA-256
`a8e29140f643bf218a82af1018f67cec30748f65c56ca108d058883bd519f9b4`；不得覆盖早期archive。

`PLAN_MACHINE_CONTRACT={"schema":"p7_td_b_retained_r3_option_b_b2_p7_c1_c1_c1_c1_v1_c1_v1_immutable_candidate_validation_only_closure_v1","reference_task_id":"REF-P7-25-R2-B2-P7-C1-C1-C1-C1-V1-C1-V1","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-P7-C1-C1-C1-C1-V1-C1-V1-IMMUTABLE-CANDIDATE-VALIDATION-ONLY-CLOSURE-V1","execution_authorized_after_orchestrator_activation":true,"activation_commit":{"expected_parent":"7d8a12178372ee34428665273086497da98f9099","expected_subject":"chore(plan): activate p7 outer plain validation closure","expected_changed_paths":[".agent-work/FULL_PLAN_REFERENCE.md",".agent-work/PLAN.md",".agent-work/PLANS/20260731-1808-p7-retained-r3-b2-p7-outer-plain-wrapper-failure-review.md"],"clean_porcelain_required_after_activation":true},"required_full_machine_state":{"active_task_count":1,"active_task":"REF-P7-25-R2-B2-P7-C1-C1-C1-C1-V1-C1-V1","active_plan_contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-P7-C1-C1-C1-C1-V1-C1-V1-IMMUTABLE-CANDIDATE-VALIDATION-ONLY-CLOSURE-V1","retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","p5_runtime_owner_status":"ACCEPTED_COMPLETE_REPO_OWNED_CONTROLLER_RUNTIME_OWNER","p6_domain_template_owner_status":"ACCEPTED_COMPLETE_DETERMINISTIC_DOMAIN_TEMPLATE_OWNER_WITH_RUNNABLE_CONTRACT_RESIDUAL","p6_candidate_commit":"48b3979d6c0df5f488cd500597e26dc4c38877dd","p6_candidate_consumable":true,"p7_status":"REJECTED_PRE_GATE_LOGICAL_EXIT_PERSISTENCE_WRAPPER_FAILURE_CANDIDATE_IMMUTABLE_NON_CONSUMABLE","p7_candidate_commit":"864f08cc5436519a37e41d553e49ebde4a3c8bb2","p7_candidate_consumable":false,"p7_implementation_commits":0,"executer_dispatched":true,"device_authorized_by_this_file":false},"rejected_validation":{"activation_commit":"44fb7295f0f71030833476225350da01ce3c71d3","candidate_commit":"864f08cc5436519a37e41d553e49ebde4a3c8bb2","evidence_commit":"7d8a12178372ee34428665273086497da98f9099","python_gate_body_exit":0,"wrapper_exit":1,"logical_exit_persisted":false,"stable_finding":"zsh_readonly_status_assignment","targeted_invocations":0,"external_effects":0},"immutable_candidate":{"commit":"864f08cc5436519a37e41d553e49ebde4a3c8bb2","parent":"44fb7295f0f71030833476225350da01ce3c71d3","subject":"chore(p7): retain rejected outer plain nul candidate","changed_paths":["src/camera_based_rgbww_optimizer/utils/p7_retained_r3_controller_domain_template.py","tests/test_p7_retained_r3_controller_domain_template.py"],"canonical_binary_diff_sha256":"b03b1a049a407e2049f049b6f2514497e6d5bb82675f14dc750f00cc09ce6bd4","source_blob_oid":"5529ec27b3893c20995e9a8cb3a9fa5c0a87a3b5","source_bytes":19753,"source_sha256":"10969de79f5afece8018f094823efcf6f60237670ed1eeb54135f451ef0425c2","test_blob_oid":"d0f733426673aa9a57fcb1195ecea014f8c48062","test_bytes":27386,"test_sha256":"4c3b93d4a2f5967b91cb48a2dea1c0a0f8994fb687f6109830d24602bb93083e","template_bytes":11999,"template_sha256":"0369231f11bc968ebc343bac57acab236d75faf5d5d6e2b9c3d82918df19a467","replacement_bytes":1907,"replacement_sha256":"502c303e6257d8f59a4d5bbd39b0339371e210a8c10c9e8fa3fd0d2530160807","consumable_before_review":false},"exact_implementation_write_paths":[],"implementation_commit":{"count":0},"wrapper_contract":{"shell":"zsh","gate_invocations":1,"exit_capture_variable":"pregate_exit","ordinary_non_special_required":true,"required_stdout_marker":"PRE_GATE_LOGICAL_EXIT=0","marker_count":1,"logical_exit_required":0,"persist_marker_in_execution_result":true,"prohibited_assignment_targets":["status","pipestatus","path","PATH","argv","ARGC","commands","functions","options","signals","parameters"],"alternative_exit_capture_variables":0},"source_domain_contract":{"module_physical_nul_bytes":0,"outer_plain_ast_physical_nul_constants":1,"outer_plain_ast_physical_lf_constants":1,"outer_plain_ast_physical_cr_constants":1,"literal_backslash_x00_spec_text_accepted":true,"physical_nul_spec_text_rejected":true,"physical_nul_error_code_field_specific":true,"canonical_template_byte_identical":true,"canonical_template_physical_nul_bytes":0,"canonical_template_literal_backslash_x00_tokens":8,"canonical_template_literal_backslash_n_tokens":3,"exact_spec_replacement_byte_identical":true,"serializer_changes":0,"semantic_matrix_changes":0,"owner_api_dataclass_changes":0,"new_helpers":0,"fallbacks":0},"regression_contract":{"targeted_expected":11,"focused_expected":93,"full_expected":778},"execution_budgets":{"pregate_invocations":1,"targeted_invocations":1,"focused_invocations":1,"compileall_invocations":1,"full_invocations":1,"implementation_commits":0,"postcommit_targeted_invocations":0,"codegraph_sync":0,"codegraph_queries":0,"execution_result_appends":1,"retry":0,"fallback":0},"zero_budgets":{"code_writes":0,"test_writes":0,"third_code_path":0,"template_edits":0,"replacement_edits":0,"serializer_edits":0,"matrix_edits":0,"owner_api_edits":0,"new_helper":0,"generic_allowlist":0,"plan_writes_by_executer":0,"full_writes_by_executer":0,"archive_writes_by_executer":0,"debug_writes":0,"guide_writes":0,"research_writes":0,"external_controller_writes":0,"external_controller_reads":0,"external_controller_processes":0,"external_root_creates":0,"external_root_reads":0,"synthetic_integration_runs":0,"old_failed_controller_reads":0,"old_failed_root_reads":0,"old_external_evidence_reads":0,"retained_artifact_reads":0,"candidate_payload_reads":0,"git_provenance_replay":0,"real_b2_dispatch":0,"subordinate_manifest_writes":0,"actual_canonical_validator_calls":0,"eligibility_emissions":0,"retained_release_audit":0,"release_generation":0,"release_qualification":0,"release_copy":0,"release_consumption":0,"network":0,"dns":0,"environment":0,"credentials":0,"device":0,"camera":0,"ray":0,"strip":0,"cleanup":0,"capture":0,"formal":0,"public_analyzer":0,"td_c":0,"sentinel":0,"p8":0,"firmware":0,"deployment":0},"expected_duration":"under_10_minutes","visible_terminal_required":false,"planner_stop":"B2_P7_C1_C1_C1_C1_V1_C1_V1_IMMUTABLE_CANDIDATE_VALIDATION_ONLY_WAITING_PLANNER_REVIEW"}`

## 1. Activation and immutable inputs

Activation必须匹配machine row的exact parent、subject与three-path set，之后porcelain clean。FULL只允许本V1 active；必须保持retained R3 unvalidated/unconsumed、P5/P6 accepted、candidate `864f08c...` immutable/non-consumable、implementation commits `0`、device authorization false。

Activation后只读核对：

1. candidate topology、exact two-path set及canonical binary diff；
2. source/test blob、bytes与SHA-256；
3. canonical template与exact-spec replacement bytes/SHA；
4. rejected V1-C1 activation/candidate/evidence topology；
5. PLAN/FULL machine rows及new archive identity；
6. initially clean porcelain及candidate code/test bytes与HEAD完全一致。

任一不符必须在gate前fail closed。Accepted P7-C1 CodeGraph evidence继续冻结使用；本包CodeGraph sync/query exact `0/0`。不得读取old failed external controller/root/evidence、retained R3或candidate payload。

## 2. Zero-write validation-only boundary

Code与test write exact `0/0`；不得生成working diff、stage、commit、amend或改写candidate。Implementation commit exact `0`。不得修改template、replacement、serializer、semantic matrix、owner/API/dataclass、helper、fallback、doc、skill或debug。

Executer在每个validation stage后重新核对candidate source/test blob、bytes、SHA-256与clean porcelain。任何漂移、untracked path或write必须fail closed；不得尝试repair。

## 3. Exact one gate and zsh logical-exit owner

Executer运行exact one fresh fail-fast Python semantic pre-gate。唯一owning zsh wrapper必须：

1. Python body返回后立即以exact ordinary non-special variable `pregate_exit=$?`捕获logical exit；
2. exact once打印`PRE_GATE_LOGICAL_EXIT=${pregate_exit}`；
3. 立即核对值strictly等于整数`0`，nonzero则以同值fail closed；
4. 在本包唯一ER append中逐字持久化`PRE_GATE_LOGICAL_EXIT=0`并记录marker count `1`；
5. 禁止向`status`、`pipestatus`、`path`、`PATH`、`argv`、`ARGC`、`commands`、`functions`、`options`、`signals`或`parameters`赋值；禁止使用其他变量作为exit capture owner。

Wrapper不允许把pipeline exit、`tee` exit或后续命令exit误记为Python logical exit。不得通过`|| true`、subshell swallowing、重新运行Python或推断Python stdout来替代exact `$?` capture。Gate invocation、Python body与logical-exit marker各exact one。

Python pre-gate必须重新证明：

- activation/baseline/current path exact、strict UTF-8、source/test AST parse+compile、methods exact `11`；
- candidate topology/diff/identities unchanged，repository在gate前clean；
- module physical NUL bytes `0`，outer `_plain` AST physical NUL/LF/CR constants exact `1/1/1`；
- public builder physical-NUL negative返回field现有stable code；literal four-character backslash-`x00` positive可build并在runtime request保持exact text；
- template及exact-spec replacement exact baseline bytes/SHA，template physical NUL `0`、literal backslash-`x00`/backslash-`n` counts `8/3`；
- exact16 canonical semantic matrix、test03/test08、runnable lifecycle与previously accepted semantic boundaries不漂移；
- code/test writes、diff、implementation commits、external effects均为`0`。

Gate或wrapper任一失败不得运行tests。

## 4. Fresh regression sequence

仅在pre-gate marker已持久化并核对exact `0`后，按顺序exact once：

1. `PYTHONUNBUFFERED=1 .venv/bin/python -m unittest tests.test_p7_retained_r3_controller_domain_template`，exact `11/11`、exit `0`、`OK`；
2. `PYTHONUNBUFFERED=1 .venv/bin/python -m unittest tests.test_p7_retained_r3_controller_domain_template tests.test_p7_retained_r3_controller_runtime tests.test_p7_retained_r3_controller_conformance tests.test_p7_retained_r3_controller_preparation tests.test_p7_retained_r3_provenance_io tests.test_agent_work_machine_contract`，exact `93/93`、exit `0`、`OK`；
3. `.venv/bin/python -m compileall -q src tests`，exit `0`；
4. unique `PYTHONUNBUFFERED=1 .venv/bin/python -m unittest discover -s tests -p 'test_*.py'`，single unified session、exact `778/778`、exit `0`、`OK`；
5. 最终核对candidate topology、all identities、source-domain contract、clean porcelain、zero writes/commits及zero external effects；
6. 只向`.agent-work/EXECUTION_RESULT.md` EOF append exact once，记录activation、candidate/final identities、wrapper exact command boundary、logical exit marker、fresh outputs、zero budgets和residual locks，然后停在Planner review。

本包没有implementation commit或postcommit test。Retry/fallback `0/0`；任一failure不得重跑、repair、lower counts或进入后续stage。

## 5. Acceptance boundary and hard locks

Success只报告
`immutable_candidate_validation_only_pass_waiting_for_planner`。Executer不得自行将candidate标记consumable或解锁integration；只有后续independent Planner review可接受candidate。

本包不运行external controller/source/root/process或synthetic integration，不读取retained R3/candidate payload，不运行Git provenance replay、real B2、subordinate manifest、canonical validator、eligibility、retained audit或release。Network、DNS、environment、credentials、device、camera、Ray、strip、cleanup、capture、FORMAL、public analyzer、TD-C、sentinel、P8、firmware、deployment全部hard locked `0`。不需要Human授权。

维护性判断：本包只验证immutable candidate，不修改任何生产或测试owner，不新增抽象、状态或平行执行路径。

## 6. Final archive row

`ARCHIVE_IDENTITY={"path":".agent-work/PLANS/20260731-1808-p7-retained-r3-b2-p7-outer-plain-wrapper-failure-review.md","bytes":6804,"sha256":"a8e29140f643bf218a82af1018f67cec30748f65c56ca108d058883bd519f9b4"}`
