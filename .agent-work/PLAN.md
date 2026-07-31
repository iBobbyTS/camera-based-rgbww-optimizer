# REF-P7-25-R2-B2-P7-C1-C1-C1：generated-source newline escape correction

**计划状态：** `WAITING_ORCHESTRATOR_ACTIVATION`

**Planner 日期：** 2026-07-31

**Reference task：** `REF-P7-25-R2-B2-P7-C1-C1-C1`

**Contract ID：**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-P7-C1-C1-C1-GENERATED-NEWLINE-ESCAPE-CORRECTION-V1`

**Planner decision：** P7-C1-C1 candidate
`443e470dbb28a83daf7f7fa33135e03861f871b8` is
`REJECTED_PRE_GATE_GENERATED_NEWLINE_ESCAPE` and is not consumable. Five-token NUL correction已完成且physical NUL不再出现；唯一fresh
Python pre-gate在generated source line `57`以unterminated string literal失败，定位到same outer bytes template中exact三个generated-source LF
string tokens提前物化。Combined shell final `0`仅来自后续path/diff gates，不改变Python logical gate `1`。Targeted及其后验证均为`0`，所有external、retained与device effects为`0`。

**当前唯一动作：** Orchestrator审核、更新FULL，并以clean evidence HEAD
`4af21403d047139a9261e010ac1d9ccc92b77f8a`为direct parent创建exact activation commit。Activation后，Executer只修改existing
domain-template module与dedicated test exact two paths：逐项修正冻结的exact三个generated-source LF escape tokens，并增加byte+AST meaningful
regression；然后运行fresh pre-gate、targeted11、focused93、compileall、unique full778、single implementation commit与postcommit targeted11。
P7-C1已接受的pre-edit CodeGraph sync/query继续作为冻结ownership evidence，本包不得调用CodeGraph。不得运行external controller/source/root/process、synthetic integration、retained、validator、release、network或device work。

**唯一 Planner stop：**
`B2_P7_C1_C1_C1_NEWLINE_ESCAPE_CORRECTION_WAITING_PLANNER_REVIEW`。

**本轮新归档：**
`.agent-work/PLANS/20260731-1720-p7-retained-r3-b2-p7-c1-c1-newline-escape-failure-review.md`，bytes `6325`，SHA-256
`d47ce2f7915f5d306780b448e37bf3b951b6b7e4fa31ecaa2cfac904d5cb5a92`；不得覆盖早期archive。

`PLAN_MACHINE_CONTRACT={"schema":"p7_td_b_retained_r3_option_b_b2_p7_c1_c1_c1_generated_newline_escape_correction_v1","reference_task_id":"REF-P7-25-R2-B2-P7-C1-C1-C1","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-P7-C1-C1-C1-GENERATED-NEWLINE-ESCAPE-CORRECTION-V1","execution_authorized_after_orchestrator_activation":true,"activation_commit":{"expected_parent":"4af21403d047139a9261e010ac1d9ccc92b77f8a","expected_subject":"chore(plan): activate p7 c1 c1 c1 newline escape correction","expected_changed_paths":[".agent-work/FULL_PLAN_REFERENCE.md",".agent-work/PLAN.md",".agent-work/PLANS/20260731-1720-p7-retained-r3-b2-p7-c1-c1-newline-escape-failure-review.md"],"clean_porcelain_required_after_activation":true},"required_full_machine_state":{"active_task_count":1,"active_task":"REF-P7-25-R2-B2-P7-C1-C1-C1","active_plan_contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-P7-C1-C1-C1-GENERATED-NEWLINE-ESCAPE-CORRECTION-V1","retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","p5_runtime_owner_status":"ACCEPTED_COMPLETE_REPO_OWNED_CONTROLLER_RUNTIME_OWNER","p6_domain_template_owner_status":"ACCEPTED_COMPLETE_DETERMINISTIC_DOMAIN_TEMPLATE_OWNER_WITH_RUNNABLE_CONTRACT_RESIDUAL","p6_candidate_commit":"48b3979d6c0df5f488cd500597e26dc4c38877dd","p6_candidate_consumable":true,"p7_status":"REJECTED_PRE_GATE_GENERATED_NEWLINE_ESCAPE","p7_rejected_candidate_commit":"443e470dbb28a83daf7f7fa33135e03861f871b8","p7_rejected_candidate_consumable":false,"p7_implementation_commits":0,"executer_dispatched":true,"device_authorized_by_this_file":false},"rejected_candidate":{"commit":"443e470dbb28a83daf7f7fa33135e03861f871b8","parent":"ac0a7d42f744edfa314562e051b547a0dc834f75","subject":"chore(p7): retain rejected p7 c1 c1 escape candidate","changed_paths":["src/camera_based_rgbww_optimizer/utils/p7_retained_r3_controller_domain_template.py","tests/test_p7_retained_r3_controller_domain_template.py"],"canonical_binary_diff_sha256":"86ea7d5709387747e1287c000383ae375f106aa53fb9515ec0c12db5e11ef0e7","consumable":false},"baseline":{"source_path":"src/camera_based_rgbww_optimizer/utils/p7_retained_r3_controller_domain_template.py","source_blob_oid":"d445dc0f778ff6723caa891b24f75d44e76a129d","source_bytes":19756,"source_sha256":"47d1c85c00feb9c088cf02f78c0ae44a6c15ad9be417be19edda7e07f2937fb3","test_path":"tests/test_p7_retained_r3_controller_domain_template.py","test_blob_oid":"a2cb719feec0e4f27224a6fa81fe379d73f02e92","test_bytes":21413,"test_sha256":"e8da56d923e0077b37eea3d1cddf798dd4691233ab49f5ff06734c8a1820ed84"},"accepted_codegraph_preflight":{"source_contract":"P7-TD-B-RETAINED-R3-OPTION-B-B2-P7-C1-CODEGRAPH-PREFLIGHT-ORDER-CORRECTION-V1","activation_commit":"13f79754daf549deeee5b470e2e620fa70e43545","sync_invocations":1,"sync_exit":0,"query_invocations":1,"query_exit":0,"query_immediately_after_sync":true,"source_or_test_content_read_before_sync":0,"post_edit_sync_invocations":0,"post_edit_query_invocations":0,"successor_may_freeze":true},"exact_code_test_write_paths":["src/camera_based_rgbww_optimizer/utils/p7_retained_r3_controller_domain_template.py","tests/test_p7_retained_r3_controller_domain_template.py"],"exact_execution_write_paths":["src/camera_based_rgbww_optimizer/utils/p7_retained_r3_controller_domain_template.py","tests/test_p7_retained_r3_controller_domain_template.py",".agent-work/EXECUTION_RESULT.md"],"correction_contract":{"outer_template_only_escape_layer":true,"generated_lf_token_count":3,"generated_lf_tokens":["activation_commit_stdout_suffix","activation_metadata_stdout_suffix","runtime_metadata_subject_suffix"],"each_generated_lf_token_corrected_once":true,"physical_nul_bytes_in_owner_generated_source":0,"generated_runtime_nul_separator_semantics_preserved":true,"generated_runtime_lf_suffix_semantics_preserved":true,"generated_source_ast_parse_and_compile":true,"broad_replacement":false,"raw_template_conversion":false,"generic_escape_helper":false,"unrelated_backslash_changes":0,"carriage_return_token_changes":0,"nul_token_changes":0,"public_exports_unchanged":true,"public_dataclass_fields_unchanged":true,"runtime_request_owner_unchanged":true,"lifecycle_owner_unchanged":true,"provenance_owner_unchanged":true,"controller_entrypoint_count":1,"test_method_count":11,"meaningful_byte_and_ast_assertions_required":true},"runnable_contract":{"replacement_tuple_only":true,"git_ledgers":6,"root_creates":1,"synthetic_inputs":4,"semantic_matrix_cases":16,"artifact_names":9,"explicit_root_bound_reads":7,"lifecycle_order":["conformance","activation","root","inputs","evaluate","terminal","terminal_seal","admission"],"persist_before_read":true,"qualification_before_terminal":true,"terminal_before_seal":true,"seal_before_admission":true,"stdout_canonical_envelopes":1,"stderr_on_success_bytes":0,"retry":0,"fallback":0,"second_analyzer":false,"second_lifecycle":false},"regression_contract":{"pregate_expected":1,"targeted_expected":11,"focused_expected":93,"full_expected":778,"postcommit_targeted_expected":11},"implementation_commit":{"expected_parent":"ACTIVATION_COMMIT_FULL_SHA","expected_subject":"fix(p7): preserve generated newline source syntax","expected_changed_paths":["src/camera_based_rgbww_optimizer/utils/p7_retained_r3_controller_domain_template.py","tests/test_p7_retained_r3_controller_domain_template.py"]},"execution_budgets":{"pregate_invocations":1,"targeted_invocations":1,"focused_invocations":1,"compileall_invocations":1,"full_invocations":1,"codegraph_sync":0,"codegraph_queries":0,"implementation_commits":1,"postcommit_targeted_invocations":1,"execution_result_appends":1,"retry":0,"fallback":0},"zero_budgets":{"external_controller_writes":0,"external_controller_reads":0,"external_controller_processes":0,"external_root_creates":0,"external_root_reads":0,"synthetic_integration_runs":0,"old_failed_controller_reads":0,"old_failed_root_reads":0,"old_external_evidence_reads":0,"retained_artifact_reads":0,"candidate_payload_reads":0,"git_provenance_replay":0,"real_b2_dispatch":0,"subordinate_manifest_writes":0,"actual_canonical_validator_calls":0,"eligibility_emissions":0,"retained_release_audit":0,"release_generation":0,"release_qualification":0,"release_copy":0,"release_consumption":0,"network":0,"dns":0,"environment":0,"credentials":0,"device":0,"camera":0,"ray":0,"strip":0,"cleanup":0,"capture":0,"formal":0,"public_analyzer":0,"td_c":0,"sentinel":0,"p8":0,"firmware":0,"deployment":0,"plan_writes_by_executer":0,"full_writes_by_executer":0,"archive_writes_by_executer":0,"debug_writes":0,"guide_writes":0,"research_writes":0},"expected_duration":"under_10_minutes","visible_terminal_required":false,"planner_stop":"B2_P7_C1_C1_C1_NEWLINE_ESCAPE_CORRECTION_WAITING_PLANNER_REVIEW"}`

## 1. Activation and frozen identities

Activation必须匹配machine row的full parent、subject与exact three-path set，之后porcelain clean。FULL只允许P7-C1-C1-C1 active；必须明确
P7-C1-C1 rejected、candidate `443e470...` non-consumable、P6与P5 owners仍accepted、retained R3仍为
`RETAINED_UNVALIDATED_UNCONSUMED`且device authorization false。

Activation后先核对candidate/evidence topology、exact two-path baseline blob/bytes/SHA、PLAN/FULL machine rows与archive identity。P7-C1已接受的
CodeGraph preflight必须按machine row冻结：它发生在candidate source理解/编辑之前，exact sync后immediate exact query，且post-edit调用`0`。
本successor不得再运行CodeGraph sync/query，不得以新query替换、补充或重解释冻结证据。

## 2. Exact two-path, three-token correction

只允许修改machine row exact two paths，且两个路径都必须出现在implementation commit。不得新增helper/module/framework，不得修改runtime、provenance、conformance或lifecycle owners。

唯一production变更：在existing outer bytes `_CANONICAL_TEMPLATE`内，逐项、显式修正exact三个用于generated Python string literal的LF escape
token，使它们穿过outer template层后仍为generated-source escaped `\\n`语法，而不是在string literal内部提前成为physical LF：

1. activation commit `rev-parse` stdout expected suffix；
2. activation metadata stdout expected suffix；
3. runtime metadata subject/stdout expected suffix。

每个token只能改一次，不得用loop、mapping、regex或`.replace()`批处理。不得改candidate已经修正的五个NUL separator token，不得改`\r`、其他
backslash、line ending、bindings、artifact names、phase order、error codes或public contract；不得raw-template conversion、generic escape helper、fallback。
若pre-gate证明还需第四个production escape token或任何非冻结位置修改，必须fail closed并停回Planner。

Dedicated test保持exact `11` methods，并在existing regression surface增加或强化meaningful exact byte+AST assertions，至少证明：

1. template/builder/compose source physical `0x00` count exact `0`，existing five-token NUL assertions保持；
2. composed generated bytes在三个冻结位置各出现exact一次escaped LF source token，token两侧使用完整stable expression boundary而非宽泛substring/prefix；
3. 每个冻结generated string literal的AST常量在compile后语义以真实single LF结尾，并与fake Git ledger stdout的LF-delimited bytes匹配；
4. entire generated source strict UTF-8、`ast.parse`与`compile`通过；用negative specimen逐项证明任一token退回single outer escape都会导致physical-LF/string边界被拒绝；
5. assertions不得使用broad replacement、regex/path allowlist、动态从当前实现生成expected token集或只执行不验证。

其余runnable contract完全冻结：replacement tuple是唯一activation/runtime/path/budget binding；required provenance owner/signatures、Git6、root1、inputs4、matrix16、artifacts9、root reads7、eight lifecycle order、persist-before-read、single guarded entrypoint、single canonical stdout envelope、stderr empty、primary-failure dominance及retry/fallback0不漂移。

## 3. Fresh validation, commit and evidence

在exact two-path edit完成后依次exact once：

1. 一个fail-fast Python pre-gate，独立保留其logical exit；核对exact path set、`git diff --check`、test method exact11、five NUL tokens不漂移、three LF tokens exact、generated bytes、AST/compile、negative specimens及frozen runnable AST/effect-free contract。不得把多个逻辑gate串入不带`set -e`的shell后以最终命令exit代替前序结果；
2. targeted domain-template：exact `11/11`、exit `0`、`OK`；
3. focused domain-template/runtime/conformance/preparation/provenance/machine-contract六模块：exact `93/93`、exit `0`、`OK`；
4. compileall exact source/test：exit `0`；
5. unique unbuffered full suite：exact `778/778`、exit `0`、`OK`，保留唯一unified session/terminal evidence；
6. 再次核对diff、exact two paths、three-token/five-NUL identities与frozen CodeGraph evidence；不得运行CodeGraph；
7. 创建direct child exact implementation commit，subject `fix(p7): preserve generated newline source syntax`，changed paths exact two；
8. postcommit targeted exact `11/11`、exit `0`、`OK`；final porcelain除ER append前clean；
9. 向`.agent-work/EXECUTION_RESULT.md` EOF append exact once，记录activation/candidate/implementation topology、before/after blob/bytes/SHA、three-token byte+AST gate、全部validation、frozen CodeGraph evidence、zero budgets与residual risk，然后停在Planner review。

Retry/fallback `0/0`。任一失败不得补第二实现、第二commit、重跑命令、降低counts、扩大路径或修改测试追随错误实现；保留真实证据并停。

## 4. Acceptance and hard locks

Acceptance要求three-token correction exact、existing five-token NUL correction不漂移、exact two-path topology、physical NUL exact0、generated AST/compile、runtime real-LF/NUL semantics、test11、targeted11、focused93、compileall、unique full778、single implementation commit、postcommit targeted11与final porcelain通过。Success只报告
`repo_owned_runnable_domain_template_candidate_waiting_for_planner_review`；不得声称synthetic integration qualified。

External controller/source/root/process与synthetic integration exact0。Old failed evidence、retained R3/candidate payload、Git provenance replay、real B2、subordinate manifest、actual canonical validator、eligibility、retained audit、release、network、DNS、environment、credentials、device、camera、Ray、strip、cleanup、capture、FORMAL、public analyzer、TD-C、sentinel、P8、firmware、deployment全部hard locked0。本PLAN不授权P5-I1或later stage。

维护性判断：本纠偏只修deterministic template owner内已证实的exact三个generated-source LF token，并以byte+AST双回归保护两层语言边界；不新增owner、helper、状态机或parallel coordinator，维护复杂度不增加。

## 5. Final archive row

`ARCHIVE_IDENTITY={"path":".agent-work/PLANS/20260731-1720-p7-retained-r3-b2-p7-c1-c1-newline-escape-failure-review.md","bytes":6325,"sha256":"d47ce2f7915f5d306780b448e37bf3b951b6b7e4fa31ecaa2cfac904d5cb5a92"}`
