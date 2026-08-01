# P7 retained-R3 Option B：M1-R1-S2-S1 strict-machine-row fresh successor

**计划状态：** `WAITING_ORCHESTRATOR_ACTIVATION`

**Planner 日期：** `2026-08-01`

**Reference task：** `REF-P7-25-R2-B2-M1-R1-S2-S1`

**Contract：**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-M1-R1-S2-S1-FRESH-REAL-INPUT-STRICT-MACHINE-ROW-NO-CANONICAL-ORDER-V1`

**当前唯一动作：** Orchestrator先记录S2非合同machine-row gate rejection并创建activation；Executer随后仅运行一次从activation full SHA
派生的brand-new S2-S1 real-input manifest-only integration。Repository gate只证明PLAN/FULL各exact one strict duplicate-free object machine row并核对
冻结required FULL subset；禁止整行canonical re-encode、sorted-key equality或任何key-order assertion。C1 four只做exact physical identity与canonical
JSON decode，retained three只做exact physical identity plus strict JSON。最终完整partial-or-success payload必须预先冻结，并以physical EOF single
append作为最后side effect。

**唯一 Planner stop：**
`B2_M1_R1_S2_S1_FRESH_REAL_INPUT_STRICT_MACHINE_ROW_WAITING_PLANNER_REVIEW`。

**本轮新归档：**
`.agent-work/PLANS/20260801-0328-p7-retained-r3-b2-m1-r1-s2-machine-row-gate-review.md`；bytes `6143`，SHA-256
`0f8e19c537d5e1756de8be4ebcc939e4693adf888b43360fe569b16e87a405ce`；不得覆盖earlier archives。

`PLAN_MACHINE_CONTRACT={"schema":"p7_td_b_retained_r3_option_b_b2_m1_r1_s2_s1_fresh_real_input_strict_machine_row_no_canonical_order_v1","reference_task_id":"REF-P7-25-R2-B2-M1-R1-S2-S1","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-M1-R1-S2-S1-FRESH-REAL-INPUT-STRICT-MACHINE-ROW-NO-CANONICAL-ORDER-V1","execution_authorized_after_orchestrator_activation":true,"activation_commit":{"expected_parent":"82e5a13319642ccf6a584c6bd535094d6ac53a9a","expected_subject":"chore(plan): activate strict-machine-row real input successor","expected_changed_paths":[".agent-work/FULL_PLAN_REFERENCE.md",".agent-work/PLAN.md",".agent-work/PLANS/20260801-0328-p7-retained-r3-b2-m1-r1-s2-machine-row-gate-review.md"],"clean_porcelain_required_after_activation":true},"rejected_s2":{"activation":"df56622d8ed2963e2cdd76610592c9a55651c1df","evidence_commit":"82e5a13319642ccf6a584c6bd535094d6ac53a9a","result":"REJECTED_EXECUTION_ASSERTION_MACHINE_ROW_CANONICAL_ORDER_NOT_CONTRACTUAL","external_acquisition":0,"builder_runtime_controller":0,"parent_er":{"bytes":1252674,"sha256":"3203d390d2e0c43da03f40603e651c3bd967f83b2dc0af97950818c678076e3e"},"evidence_er":{"bytes":1258401,"sha256":"681a5d12f7a5b53c4aa3269475cc009b51893320a1f3a3d41d41175ece3764f9"},"physical_eof_suffix":{"bytes":5727,"sha256":"45eb34ef341f5040ec908292279f45dca07184fa591b633b55ec0718bf5a7dfb"},"production_repair_required":false,"test_repair_required":false,"supersession_required":false},"repository_machine_row_contract":{"row_count_each":1,"strict_utf8_json":true,"object_root":true,"duplicate_keys_rejected":true,"required_full_subset_exact":true,"canonical_reencode":false,"sorted_key_equality":false,"top_level_key_order_frozen":false,"nested_key_order_frozen":false,"generic_canonical_byte_gate":false},"accepted_c1_review":{"archive":".agent-work/PLANS/20260730-1000-p7-retained-r3-option-b-b2-c1-path-owner-index-review.md","semantic_owner":"ACCEPTED_C1_INDEPENDENT_REVIEW","runtime_semantic_revalidation":false,"runtime_linkage_revalidation":false,"unversioned_terminal_selectors":0},"accepted_m1_owner":{"implementation_commit":"0f4c09e1b2b2afbf627f6f36d57a1a65847ab4a8","implementation_parent":"f2b38c530a6cbac5c29d761036eb3cd2a159f3b9","implementation_subject":"fix(p7): align real manifest Git ledgers","implementation_paths":["src/camera_based_rgbww_optimizer/utils/p7_retained_r3_real_manifest_domain_template.py","tests/test_p7_retained_r3_real_manifest_domain_template.py"],"binary_patch_bytes":5874,"binary_patch_sha256":"6b26e49359f944bceafe5129b0b81a3d5600d400eae7d3b739c2baba12d6a5ca","source_blob":"c0238fba753fc7608df1c352f336199fb6ebc105","source_bytes":23737,"source_sha256":"350e393dcb3155c71cb416b18ad485197173b8c64d19cda510923c771a0ab25e","template_sha256":"a83804d299c747c485dda86eecd3bcb576a90bb2be3c2ae03fe77951ed404ad6","test_blob":"ef8273e14853446c31b47f1f093a18bac43c6f64","test_bytes":22897,"test_sha256":"0a3278c95a5a1ef11bec217e4ce06a123711fe2c884157e9c7e02d40b68b479c","consumable_for_this_package":true,"retained_eligible":false},"accepted_p3_owner":{"module":"src/camera_based_rgbww_optimizer/utils/p7_retained_r3_provenance_io.py","input_owners":["read_existing_root","read_exact_file"],"canonical_decoder":"decode_canonical_json","output_owners":["create_exclusive_root","persist_canonical_json"],"git_owner":"run_read_only_git"},"strict_retained_owner":{"module":"src/camera_based_rgbww_optimizer/optimization/p7_retained_release_audit.py","decoder":"_strict_json_load","dependencies":"_default_dependencies","requirements":["utf8","object_root","duplicate_keys_rejected","nonfinite_rejected"],"canonical_reencode":false,"schema_validation":false,"scientific_validation":false,"eligibility":false,"release_consumable":false},"accepted_p5_owner":{"implementation_commit":"37f7d0021c7a81a9d6680815bc51c305cf807a7b","source_blob":"075face6fd7453236affa303640b91eb16a42a9b","source_bytes":12320,"source_sha256":"07eaeac615ea79db45afad91ce4c82e28c1cdcb66b6119b5cdca6462d7c091d2","entrypoint":"execute_controller_runtime"},"required_full_machine_state":{"active_task_count":1,"active_task":"REF-P7-25-R2-B2-M1-R1-S2-S1","active_plan_contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-M1-R1-S2-S1-FRESH-REAL-INPUT-STRICT-MACHINE-ROW-NO-CANONICAL-ORDER-V1","retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","real_manifest_domain_owner_status":"ACCEPTED_COMPLETE_GIT_GRAMMAR_VALIDATED","m1_real_manifest_candidate_commit":"0f4c09e1b2b2afbf627f6f36d57a1a65847ab4a8","m1_real_manifest_candidate_consumable":true,"m1_synthetic_integration_status":"ACCEPTED_COMPLETE_QUALIFIED_NOT_RETAINED_ELIGIBLE","m1_real_input_manifest_status":"ACTIVE_FRESH_STRICT_MACHINE_ROW_NO_CANONICAL_ORDER_SUCCESSOR","m1_real_input_supersession_status":"REJECTED_EXECUTION_ASSERTION_MACHINE_ROW_CANONICAL_ORDER_NOT_CONTRACTUAL","existing_root_identity_owner_status":"ACCEPTED_COMPLETE_COMPOSITE_VALIDATED","executer_dispatched":true,"device_authorized_by_this_file":false},"c1_input_contract":{"root":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b2-c1-path-owner-27aacbf-20260730T1547Z","root_mode":448,"files":[["path_owner_index","path-owner-index.json",12195,"b189117fdd0a9a65ca80660245ec84b7f2f533c3e496c96e76eb48a4666feb35"],["path_owner_index_seal","path-owner-index.sha256.json",682,"867d1ffad5bd29f24dc81b24a58ce66393dd688833d3a4516fe7f45ef50875e9"],["terminal_evidence","terminal-evidence.json",13455,"c21a691272ca7466271349daa5b10236c9f36dfeb481d592e9c368a87e7a4763"],["terminal_evidence_seal","terminal-evidence.sha256.json",772,"4bfebf4ad40e8c2e65ad2470faaed184f21d39eda73c13e689b09769d280752f"]],"file_mode":384,"json_acceptance":"CANONICAL_EXACT_REENCODE_ONLY","semantic_acceptance_owner":"ACCEPTED_C1_REVIEW","runtime_schema_field_checks":false,"runtime_linkage_field_checks":false,"runtime_path_extraction":false},"retained_input_contract":{"root":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-lineage-release-r3/lineage-release-32b9e67-r2-20260727T2227/child-output/lineage-release-r3","root_mode":448,"files":[["current_lineage_candidate","current-lineage-candidate.json",9819,"3a2ff5a2af200c55c925b954488c5c5dd31a35a481440d17dfcdd8b68419f2e0"],["resolved_formal_plan","resolved-formal-plan.json",15137,"cf7c78b6a6cfda4055d05f5e9bbe9914161213b380dc7736ee09e257dd45eb6b"],["setup_lineage_release","setup-lineage-release.json",1567,"0bacf1878a97fcdc4436259e132e89f6e56611df6d7fb5d5a7da28f62c98ad3e"]],"file_mode":384,"json_acceptance":"STRICT_JSON_NO_CANONICAL_REENCODE","semantic_validation":false,"consumption":false},"identity_ledger_contract":{"successful_reads_preserved_immediately":true,"ordered_partial_ledger_on_failure":true,"raw_data_must_remain_in_memory":true,"invented_or_reconstructed_rows":false},"domain_spec_contract":{"builder":"build_real_manifest_domain_template","builder_calls":1,"runtime":"execute_controller_runtime","runtime_calls":1,"controller_processes":1,"generated_git_ledgers":56,"git_argv_shape":["git","show","-s","--format=%H%x00%P%x00%s","GIT_TARGETS[index % 7]"],"target_count":7,"cycles":8,"retry":0,"fallback":0},"fresh_namespace":{"base_dir":"/Volumes/4T/temp/rgbww-optimizer","prefix":"p7-td-b-retained-r3-option-b-m1-r1-s2-s1-<activation_short12>","source_suffix":"-source.py","output_root_suffix":"-output","source_mode":384,"output_root_mode":448,"output_artifacts":5,"output_file_mode":384,"preflight_absence_targets":2,"postappend_probes":0,"alternate":0},"success_contract":{"process_exit":0,"stderr_bytes":0,"stdout_bytes":71,"controller_git_ledgers":56,"controller_input_reads":7,"controller_output_reload_reads":5,"output_exact_file_set":["execution-result-admission.json","retained-r3-audit-provenance-manifest-v2.json","retained-r3-audit-provenance-manifest-v2.sha256.json","terminal-evidence.json","terminal-evidence.sha256.json"],"manifest_schema":"p7_retained_r3_audit_provenance_manifest_v2","manifest_status":"sealed_subordinate_provenance_evidence","admitted":true,"eligibility":false,"release_consumable":false,"success_label":"FRESH_M1_REAL_INPUT_MANIFEST_SEALED_NOT_RETAINED_ELIGIBLE"},"execution_result_append_contract":{"heading":"## REF-P7-25-R2-B2-M1-R1-S2-S1 Executer handoff","schema":"p7_td_b_retained_r3_option_b_b2_m1_r1_s2_s1_execution_result_v1","strict_canonical_one_line_json":true,"physical_eof":true,"current_final_anchor_heading":"## REF-P7-25-R2-B2-M1-R1-S2 Executer handoff","full_unique_final_block_context_required":true,"apply_patch_invocations":1,"execution_result_appends":1,"append_is_last_side_effect":true,"postappend_operations":0},"execution_budgets":{"real_input_manifest_runs":1,"outer_python_invocations":1,"fresh_absence_checks":2,"preacquisition_root_reads":2,"preacquisition_file_reads":7,"c1_canonical_decodes":4,"c1_semantic_field_selectors":0,"c1_linkage_revalidations":0,"unversioned_terminal_selectors":0,"retained_strict_decodes":3,"builder_calls":1,"runtime_calls":1,"controller_processes":1,"source_creates":1,"output_root_creates":1,"output_artifact_writes":5,"controller_git_ledgers":56,"controller_input_root_reads":7,"controller_input_file_reads":7,"controller_output_reload_reads":5,"postaudit_source_reads":1,"postaudit_root_reads":3,"postaudit_input_file_reads":7,"postaudit_output_file_reads":5,"process_table_scans":1,"apply_patch_invocations":1,"execution_result_appends":1,"postappend_operations":0,"tests":0,"compileall":0,"codegraph_sync":0,"codegraph_queries":0,"implementation_commits":0,"retry":0,"fallback":0},"zero_budgets":{"repository_code_writes":0,"repository_test_writes":0,"plan_writes_by_executer":0,"full_writes_by_executer":0,"archive_writes_by_executer":0,"debug_writes":0,"guide_writes":0,"research_writes":0,"old_m1_r1_external_reads":0,"old_s1_external_reads":0,"old_s2_external_reads":0,"accepted_synthetic_external_evidence_reads":0,"alternate_path_search":0,"parent_sibling_listing":0,"recursive_search":0,"input_writes":0,"retained_artifact_writes":0,"retained_canonical_reencode":0,"retained_schema_validation":0,"retained_scientific_validation":0,"actual_canonical_validator_calls":0,"canonical_validator_callbacks":0,"eligibility_emissions":0,"retained_release_audit":0,"release_generation":0,"release_qualification":0,"release_copy":0,"release_consumption":0,"network":0,"dns":0,"environment":0,"credentials":0,"device":0,"camera":0,"ray":0,"strip":0,"cleanup":0,"capture":0,"formal":0,"public_analyzer":0,"td_c":0,"sentinel":0,"p8":0,"firmware":0,"deployment":0},"authorization":{"classification":"PURE_OFFLINE_READ_ONLY_EXISTING_INPUTS_AND_NEW_EVIDENCE_OUTPUT","human_device_authorization_required":false,"advisor_scientific_decision_required":false},"expected_duration":"under_10_minutes","visible_terminal_required":false,"archive":{"path":".agent-work/PLANS/20260801-0328-p7-retained-r3-b2-m1-r1-s2-machine-row-gate-review.md","bytes":6143,"sha256":"0f8e19c537d5e1756de8be4ebcc939e4693adf888b43360fe569b16e87a405ce"},"planner_stop":"B2_M1_R1_S2_S1_FRESH_REAL_INPUT_STRICT_MACHINE_ROW_WAITING_PLANNER_REVIEW"}`

## 1. Activation 与 strict-machine-row gate

Orchestrator必须先把S2 rejection与唯一active S2-S1写入FULL并创建activation。Expected parent exact
`82e5a13319642ccf6a584c6bd535094d6ac53a9a`，subject exact
`chore(plan): activate strict-machine-row real input successor`，changed paths exact为FULL、PLAN与本轮new archive。Activation后porcelain必须clean。

Executer验证activation topology、PLAN/FULL each exact one machine row。每行只需strict UTF-8 JSON、object root、duplicate-key rejection，并核对
machine row冻结的required FULL subset与archive/M1/P3/P5 identities。禁止对完整PLAN/FULL machine row做canonical encoder/re-encode、sorted-key byte
equality、top-level/nested key-order冻结、generic canonical-byte assertion或名为`machine_row_not_canonical`的gate。此限制只作用于repository machine
rows，不削弱C1 input、output artifacts或最终ER payload各自明确的canonical合同。

任何external access前，在内存建立append-safe payload与ordered counters/identity ledgers。Failure也必须保留activation、owner、budget/actual、first
failure、partial identities、selector-zero assertions与hard locks；不得等全部成功后才建立。

## 2. Fresh S2-S1 namespace 与 exact-two absence gate

令`<activation_short12>`为activation full SHA前12位。Fresh targets exact two：

- source：`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-m1-r1-s2-s1-<activation_short12>-source.py`；
- output root：同prefix加`-output`。

对exact two各一次non-following `lstat`；必须`2/2 absent`。任一present、symlink、error或budget drift立即fail closed。禁止alternate、parent/
sibling listing、glob、recursive search或复用任何S2、S1、M1-R1、synthetic、failure namespace。ER append后不得再probe。

## 3. Exact inputs 与 selector-free JSON boundaries

只读取machine row冻结的C1与retained两个root。以P3 `read_existing_root`各exact1取得0700 exact identity；每次成功立即append到ordered ledger。
按machine row order以P3 `read_exact_file`读取C1 four再retained three；每次成功后、任何decode或下一read前，立即保存完整FileIdentity及raw data。
Failure handoff保留所有ordered partial rows，不得clear、truncate、reconstruct或发明identity。

C1 four各exact一次调用P3 `decode_canonical_json`，只证明冻结bytes可canonical strict object decode。C1 semantic/schema/linkage/path binding承接accepted
C1 review；不得读取或断言`planner_stop`、`c1_terminal_link`、status、schema、resolved path或任何未版本化字段。Generic selector、fallback、whole-object
search与字符串扫描同样禁止。

Retained three各exact一次调用production `_strict_json_load(data, _default_dependencies())`，只证明strict UTF-8 object、duplicate-key reject、
non-finite reject。禁止canonical encoder/re-encode、P3 canonical decoder、schema/science解释、eligibility或release consumption；不得修改、normalize、
copy、repair或regenerate retained bytes。

任一root/file/decode failure立即停止后续external acquisition，冻结first failure与partial ledgers并转sole ER append；builder/runtime/process/output
create保持0，retry/fallback0。

## 4. Single accepted M1/P5 execution

使用preacquisition exact seven identities构造accepted `RealManifestDomainTemplateSpec`；绑定accepted M1 commit `0f4c09e...`与authoritative patch
`6b26e493...a5ca`。Builder `build_real_manifest_domain_template` exact1，验证typed bundle、template SHA、artifact names5、lifecycle8、bound-results76与
Git family56；direct source patch/override/second builder0。

Bundle runtime request原样交P5 `execute_controller_runtime` exact1，dependency override0。它只可exclusive create fresh source0600并launch exact one
`.venv/bin/python -` controller。Controller执行Git ledgers56、input root/file reads7/7、exclusive output root0700 exact1、canonical output
persists5/reloads5与one lifecycle；retry/fallback/second process0。Exception/nonzero保留fresh evidence，不cleanup、不改path、不诊断重跑。

## 5. Pre-append terminal audit

仅process success时，在ER append前完成：

1. source same inode/mode0600，bytes/SHA与runtime composition exact；
2. C1/retained roots each reread exact1，seven files按原order each reread exact1；每次成功立即append post identity并与pre完整identity/data相同；
3. output root reread exact1，direct sorted set exact five；output files each reread exact1并立即append identity，same-root regular0600 canonical JSON；
4. manifest/seals/terminal/admission与spec exact；retained rows只陈述physical identity；admission exact `true/false/false`；
5. owned exact-argv process scan exact1，排除outer process后residual0。

任一postaudit failure保留全部已完成ledgers与actual counts。Success label只能是
`FRESH_M1_REAL_INPUT_MANIFEST_SEALED_NOT_RETAINED_ELIGIBLE`，不能解释为validator、retained audit、eligibility或release result。

## 6. Physical-EOF ER lifecycle

所有external、process、audit和repository/Git prefix reads必须在ER append前完成。先在内存冻结final payload：result/first failure、完整budget/actual、
ordered identities、source/output/process/Git ledgers、machine-row gate assertions、selector zeros、old namespace immutable dispositions、hard locks、
`execution_result_appends=1`、`apply_patch_invocations=1`、postappend operations `0`及唯一Planner stop。

唯一write使用exact one `apply_patch`。必须从activation committed/current worktree ER取得physical EOF完整唯一S2 block，从heading
`## REF-P7-25-R2-B2-M1-R1-S2 Executer handoff`经其完整one-line JSON及closing fence到final LF，证明current worktree ER与activation committed ER
byte-identical且该完整block exact once并位于EOF。Patch用完整block作context，只在其后加入空行、S2-S1 heading、single fenced one-line strict
canonical JSON及final LF；禁止generic fence、短JSON尾或重复heading context。

Successful apply-patch是本包最后side effect。之后Git/status/diff/hash、repository或ER read、external read/stat/list/search/probe、process scan及second
append全部0。Apply-patch no-write failure立即stop；retry/fallback/second append0。

## 7. Locks、authorization 与 stop

Budgets以machine row为准，early failure只报告actual、不补跑。Repository code/test/PLAN/FULL/archive/debug/GUIDE/RESEARCH writes0；tests、compileall、
CodeGraph、implementation commit0。Old S2及其他old namespace operations0；input/retained writes0；C1 semantic/linkage selectors0；retained canonical
reencode/schema/science0；validator/callback/eligibility、retained audit、release generation/qualification/copy/consumption0；network/DNS/environment/
credentials、device/camera/Ray/strip/cleanup/capture/FORMAL/public analyzer/TD-C/sentinel/P8/firmware/deployment0。

本包是`PURE_OFFLINE_READ_ONLY_EXISTING_INPUTS_AND_NEW_EVIDENCE_OUTPUT`，无需Human device授权或Advisor科学决定。Sole append或safe no-write stop后
立即停Planner门；不得进入validator、release、device或later stage。

维护性判断：继续复用P3 physical/canonical owner、historical strict decoder、M1 domain owner与P5 runtime owner；repository machine row准入明确为
strict decode + frozen subset，避免执行脚本耦合JSON key order，不新增production helper、serializer、validator、controller或parallel evidence framework。
