# REF-P7-25-R2-B2-P7-C1-C1-C1-C1-V1-C1-V1-C1-C1：Markdown machine-row delimiter validation closure

**计划状态：** `WAITING_ORCHESTRATOR_ACTIVATION`

**Planner 日期：** 2026-07-31

**Reference task：** `REF-P7-25-R2-B2-P7-C1-C1-C1-C1-V1-C1-V1-C1-C1`

**Contract ID：**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-P7-C1-C1-C1-C1-V1-C1-V1-C1-C1-MARKDOWN-MACHINE-ROW-DELIMITER-VALIDATION-CLOSURE-V1`

**Planner decision：** reviewed deferred-append execution is
`REJECTED_GATE_HARNESS_MARKDOWN_MACHINE_ROW_REGEX_DEFECT_CANDIDATE_IMMUTABLE_NON_CONSUMABLE`。Activation `30aa4f2...`、candidate semantic/identity、AST/compile、`_plain`、public boundary、template/replacement、matrix/test与lifecycle prior gates均已通过；line 155的`plan_match`与`full_match`同时为`None`，因为gate期待bare marker row，而authoritative PLAN/FULL rows均为exact backtick-wrapped Markdown inline-code row。Tests与all effects为`0`。本轮无ER append/evidence commit；evidence source是same Executer terminal source-backed diagnostic，HEAD与ER保持不变。这是validation harness defect，不是candidate defect。

**当前唯一动作：** Orchestrator审核并更新FULL后，以clean HEAD
`30aa4f281f6fe2fb825ba2240cfce779fdba47e4`为direct parent创建exact activation commit。Executer只对immutable candidate `864f08c...`运行one corrected validation sequence；code/test write、implementation commit、CodeGraph、retry与external effects exact `0`。

**唯一 Planner stop：**
`B2_P7_C1_C1_C1_C1_V1_C1_V1_C1_C1_MARKDOWN_MACHINE_ROW_DELIMITER_VALIDATION_WAITING_PLANNER_REVIEW`。

**本轮新归档：**
`.agent-work/PLANS/20260731-1835-p7-retained-r3-b2-p7-markdown-machine-row-gate-failure-review.md`，bytes `6222`，SHA-256
`296b9eefb701efdf6b54cefe502881ca1b5c13e909bd4eb6058808452521da14`；不得覆盖早期archive。

`PLAN_MACHINE_CONTRACT={"schema":"p7_td_b_retained_r3_option_b_b2_p7_c1_c1_c1_c1_v1_c1_v1_c1_c1_markdown_machine_row_delimiter_validation_closure_v1","reference_task_id":"REF-P7-25-R2-B2-P7-C1-C1-C1-C1-V1-C1-V1-C1-C1","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-P7-C1-C1-C1-C1-V1-C1-V1-C1-C1-MARKDOWN-MACHINE-ROW-DELIMITER-VALIDATION-CLOSURE-V1","execution_authorized_after_orchestrator_activation":true,"activation_commit":{"expected_parent":"30aa4f281f6fe2fb825ba2240cfce779fdba47e4","expected_subject":"chore(plan): activate p7 markdown machine row validation closure","expected_changed_paths":[".agent-work/FULL_PLAN_REFERENCE.md",".agent-work/PLAN.md",".agent-work/PLANS/20260731-1835-p7-retained-r3-b2-p7-markdown-machine-row-gate-failure-review.md"],"clean_porcelain_required_after_activation":true},"required_full_machine_state":{"active_task_count":1,"active_task":"REF-P7-25-R2-B2-P7-C1-C1-C1-C1-V1-C1-V1-C1-C1","active_plan_contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-P7-C1-C1-C1-C1-V1-C1-V1-C1-C1-MARKDOWN-MACHINE-ROW-DELIMITER-VALIDATION-CLOSURE-V1","retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","p5_runtime_owner_status":"ACCEPTED_COMPLETE_REPO_OWNED_CONTROLLER_RUNTIME_OWNER","p6_domain_template_owner_status":"ACCEPTED_COMPLETE_DETERMINISTIC_DOMAIN_TEMPLATE_OWNER_WITH_RUNNABLE_CONTRACT_RESIDUAL","p6_candidate_commit":"48b3979d6c0df5f488cd500597e26dc4c38877dd","p6_candidate_consumable":true,"p7_status":"REJECTED_GATE_HARNESS_MARKDOWN_MACHINE_ROW_REGEX_DEFECT_CANDIDATE_IMMUTABLE_NON_CONSUMABLE","p7_candidate_commit":"864f08cc5436519a37e41d553e49ebde4a3c8bb2","p7_candidate_consumable":false,"p7_implementation_commits":0,"executer_dispatched":true,"device_authorized_by_this_file":false},"rejected_validation":{"activation_commit":"30aa4f281f6fe2fb825ba2240cfce779fdba47e4","activation_parent":"045915dae74b14c9a56d6524d5573a5bdeade4d4","activation_subject":"chore(plan): activate p7 deferred er append validation closure","terminal_evidence_source":"same_executer_terminal_source_backed_diagnostic","gate_line":155,"plan_match":null,"full_match":null,"candidate_prior_gates_passed":true,"targeted_invocations":0,"er_appends":0,"evidence_commits":0,"external_effects":0,"unchanged_head":"30aa4f281f6fe2fb825ba2240cfce779fdba47e4","unchanged_er_bytes":1129765,"unchanged_er_sha256":"954e378e23fd9dfc4f6bf0f50da765076db54d5c62030995207c983f674c76b3"},"immutable_candidate":{"commit":"864f08cc5436519a37e41d553e49ebde4a3c8bb2","parent":"44fb7295f0f71030833476225350da01ce3c71d3","subject":"chore(p7): retain rejected outer plain nul candidate","changed_paths":["src/camera_based_rgbww_optimizer/utils/p7_retained_r3_controller_domain_template.py","tests/test_p7_retained_r3_controller_domain_template.py"],"canonical_binary_diff_sha256":"b03b1a049a407e2049f049b6f2514497e6d5bb82675f14dc750f00cc09ce6bd4","source_blob_oid":"5529ec27b3893c20995e9a8cb3a9fa5c0a87a3b5","source_bytes":19753,"source_sha256":"10969de79f5afece8018f094823efcf6f60237670ed1eeb54135f451ef0425c2","test_blob_oid":"d0f733426673aa9a57fcb1195ecea014f8c48062","test_bytes":27386,"test_sha256":"4c3b93d4a2f5967b91cb48a2dea1c0a0f8994fb687f6109830d24602bb93083e","template_bytes":11999,"template_sha256":"0369231f11bc968ebc343bac57acab236d75faf5d5d6e2b9c3d82918df19a467","replacement_bytes":1907,"replacement_sha256":"502c303e6257d8f59a4d5bbd39b0339371e210a8c10c9e8fa3fd0d2530160807","consumable_before_review":false},"harness_correction":{"scope":"markdown_machine_row_delimiters_only","plan_marker":"PLAN_MACHINE_CONTRACT=","full_marker":"FULL_PLAN_MACHINE_STATE=","line_anchor_required":true,"opening_backtick_required":true,"one_line_json_capture_required":true,"trailing_backtick_required":true,"line_terminal_required":true,"exact_match_count_each":1,"strict_json_decode":true,"generic_parser":false,"fallback":false,"row_repair":false,"row_regeneration":false},"evidence_order_contract":{"initial_clean_before_any_er_bytes":true,"pre_initial_clean_er_bytes":0,"pre_terminal_er_bytes":0,"in_memory_buffer_required":true,"successful_er_appends":1,"successful_er_marker":"PRE_GATE_LOGICAL_EXIT=0","successful_er_marker_count":1,"failure_before_initial_clean_er_appends":0,"ordinary_exit_capture_variable":"pregate_exit"},"exact_implementation_write_paths":[],"implementation_commit":{"count":0},"regression_contract":{"targeted_expected":11,"focused_expected":93,"full_expected":778},"execution_budgets":{"pregate_invocations":1,"targeted_invocations":1,"focused_invocations":1,"compileall_invocations":1,"full_invocations":1,"implementation_commits":0,"postcommit_targeted_invocations":0,"codegraph_sync":0,"codegraph_queries":0,"successful_execution_result_appends":1,"retry":0,"fallback":0},"zero_budgets":{"code_writes":0,"test_writes":0,"third_code_path":0,"pre_initial_clean_er_bytes":0,"pre_terminal_er_bytes":0,"template_edits":0,"replacement_edits":0,"serializer_edits":0,"matrix_edits":0,"owner_api_edits":0,"new_helper":0,"generic_parser":0,"generic_allowlist":0,"plan_writes_by_executer":0,"full_writes_by_executer":0,"archive_writes_by_executer":0,"debug_writes":0,"guide_writes":0,"research_writes":0,"external_controller_writes":0,"external_controller_reads":0,"external_controller_processes":0,"external_root_creates":0,"external_root_reads":0,"synthetic_integration_runs":0,"old_failed_controller_reads":0,"old_failed_root_reads":0,"old_external_evidence_reads":0,"retained_artifact_reads":0,"candidate_payload_reads":0,"git_provenance_replay":0,"real_b2_dispatch":0,"subordinate_manifest_writes":0,"actual_canonical_validator_calls":0,"eligibility_emissions":0,"retained_release_audit":0,"release_generation":0,"release_qualification":0,"release_copy":0,"release_consumption":0,"network":0,"dns":0,"environment":0,"credentials":0,"device":0,"camera":0,"ray":0,"strip":0,"cleanup":0,"capture":0,"formal":0,"public_analyzer":0,"td_c":0,"sentinel":0,"p8":0,"firmware":0,"deployment":0},"expected_duration":"under_10_minutes","visible_terminal_required":false,"planner_stop":"B2_P7_C1_C1_C1_C1_V1_C1_V1_C1_C1_MARKDOWN_MACHINE_ROW_DELIMITER_VALIDATION_WAITING_PLANNER_REVIEW"}`

## 1. Activation and immutable inputs

Activation必须匹配machine row的exact parent、subject、three-path set并在commit后porcelain clean。FULL仅允许本task active，且必须保持retained R3 unvalidated/unconsumed、P5/P6 accepted、candidate `864f08c...` immutable/non-consumable、implementation commits `0`、device authorization false。

任何ER byte前只读核对activation topology、candidate exact two-path diff、source/test blob+bytes+SHA、template/replacement identities、PLAN/FULL machine rows、新archive identity、initial clean和candidate bytes unchanged。任一不符fail closed。不得读取old failed external controller/root/evidence、retained R3或candidate payload。

## 2. Exact Markdown machine-row delimiter correction

本包只允许修正transient Python gate中的两条regex；不得写入repository code/test或持久化harness。Exact patterns为：

```text
^`PLAN_MACHINE_CONTRACT=(\{[^\r\n]*\})`$
^`FULL_PLAN_MACHINE_STATE=(\{[^\r\n]*\})`$
```

每条必须匹配exact one row，然后只对captured JSON object strict decode。必须保留line start `^`、literal opening backtick、exact marker、one-line JSON capture、literal trailing backtick和line terminal `$`。禁止generic Markdown parser、permissive alternative、fallback、repair或regeneration；zero/multiple match均fail closed。

## 3. Delayed evidence ordering and exact gate

所有header、marker、counts、stdout/stderr摘要、identity与terminal result先保存在内存。Initial-clean和完整validation terminal前ER byte exact `0`；success仅允许terminal后single EOF append。Initial-clean失败则ER append `0`并直接handoff；later failure不得retry/repair。

Owning zsh必须在Python gate后立即用ordinary `pregate_exit=$?`捕获logical exit，exact once打印并缓存`PRE_GATE_LOGICAL_EXIT=${pregate_exit}`，nonzero不得运行tests。禁止pipeline/subsequent exit、swallow、rerun或stdout inference。

Gate除上述delimiter correction外必须重证activation/current path、strict UTF-8、candidate topology/diff/identities、AST+compile、methods exact `11`、module physical NUL `0`、outer `_plain` AST NUL/LF/CR `1/1/1`、public boundaries、template/replacement baselines与escape counts、exact16 matrix、test03/test08、runnable lifecycle、clean porcelain与all zero effects。

## 4. Fresh regression and terminal append

仅在gate logical exit `0`后按顺序exact once：

1. targeted domain-template suite exact `11/11`、exit `0`、`OK`；
2. focused six-module suite exact `93/93`、exit `0`、`OK`；
3. `.venv/bin/python -m compileall -q src tests` exit `0`；
4. unique full discovery session exact `778/778`、exit `0`、`OK`；
5. final candidate identities、source-domain contract、clean porcelain及zero effects；
6. terminal后single EOF append，逐字持久化真实`PRE_GATE_LOGICAL_EXIT=0` exact once，然后停止在Planner review。

Implementation commit、postcommit test、CodeGraph、retry/fallback exact `0`。任一failure不得rerun、repair、lower counts或进入后续stage。

## 5. Acceptance boundary and locks

Success只报告`markdown_machine_row_delimiter_validation_pass_waiting_for_planner`；Executer不得把candidate标为consumable或解锁integration。External controller/source/root/process、synthetic integration、retained R3/candidate payload、Git provenance replay、real B2、subordinate manifest、canonical validator、eligibility、retained audit、所有release操作、network/DNS/environment/credentials/device/camera/Ray/strip/cleanup/capture/FORMAL/public analyzer/TD-C/sentinel/P8/firmware/deployment全部locked `0`。无需Human授权或Advisor scientific decision。

维护性判断：本包只纠正transient validation harness的exact Markdown delimiter表达式，不修改生产/测试owner，不新增parser、helper、fallback或平行路径。

## 6. Final archive row

`ARCHIVE_IDENTITY={"path":".agent-work/PLANS/20260731-1835-p7-retained-r3-b2-p7-markdown-machine-row-gate-failure-review.md","bytes":6222,"sha256":"296b9eefb701efdf6b54cefe502881ca1b5c13e909bd4eb6058808452521da14"}`
