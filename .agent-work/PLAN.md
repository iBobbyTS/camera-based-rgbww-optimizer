# P7 retained-R3 Option B：M1-R1-S1 fresh real-input strict-retained successor

**计划状态：** `WAITING_ORCHESTRATOR_ACTIVATION`

**Planner 日期：** `2026-08-01`

**Reference task：** `REF-P7-25-R2-B2-M1-R1-S1`

**Contract：**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-M1-R1-S1-FRESH-REAL-INPUT-STRICT-RETAINED-V1`

**当前唯一动作：** Orchestrator先记录M1-R1-C1 acceptance并创建activation；Executer随后只运行一次由activation full SHA派生的new-namespace
real-input manifest-only integration。C1 four保持canonical JSON；retained three只接受exact physical identity plus strict JSON，禁止canonical
re-encode。执行必须完整保存每次成功读取的identity与partial failure ledger，并以预先冻结的single ER payload作为最后一个side effect。

**唯一 Planner stop：**
`B2_M1_R1_S1_FRESH_REAL_INPUT_STRICT_RETAINED_WAITING_PLANNER_REVIEW`。

**本轮新归档：**
`.agent-work/PLANS/20260801-0219-p7-retained-r3-b2-m1-r1-c1-supersession-acceptance-review.md`；bytes
`6368`，SHA-256 `85bf0ef3ad5cab14ef3d85ed33eeda58f68f997566f10ec2f710d41184ab3f88`；不得覆盖earlier archives。

`PLAN_MACHINE_CONTRACT={"schema":"p7_td_b_retained_r3_option_b_b2_m1_r1_s1_fresh_real_input_strict_retained_v1","reference_task_id":"REF-P7-25-R2-B2-M1-R1-S1","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-M1-R1-S1-FRESH-REAL-INPUT-STRICT-RETAINED-V1","execution_authorized_after_orchestrator_activation":true,"activation_commit":{"expected_parent":"cb59091d67683ae0b31f3790bf8e110f610791ef","expected_subject":"chore(plan): activate strict retained real input successor","expected_changed_paths":[".agent-work/FULL_PLAN_REFERENCE.md",".agent-work/PLAN.md",".agent-work/PLANS/20260801-0219-p7-retained-r3-b2-m1-r1-c1-supersession-acceptance-review.md"],"clean_porcelain_required_after_activation":true},"accepted_supersession":{"activation":"7373e0cc18b74f06859d53f8a21810b339422792","evidence_commit":"cb59091d67683ae0b31f3790bf8e110f610791ef","evidence_er_blob":"edc2229b4e6e24f63340cb0a4909747f70193c9e","evidence_er_bytes":1234268,"evidence_er_sha256":"232e1dc4ced7a072adccd8e6e95dd46ca1d2b2ff3a580150db96c5c582fbdbb1","result":"ACCEPTED_COMPLETE_GIT_ER_ONLY_SUPERSESSION","original_record_immutable":true,"missing_identity_rows_recovered":false,"old_namespace_consumable":false},"accepted_m1_owner":{"implementation_commit":"0f4c09e1b2b2afbf627f6f36d57a1a65847ab4a8","implementation_parent":"f2b38c530a6cbac5c29d761036eb3cd2a159f3b9","implementation_subject":"fix(p7): align real manifest Git ledgers","implementation_paths":["src/camera_based_rgbww_optimizer/utils/p7_retained_r3_real_manifest_domain_template.py","tests/test_p7_retained_r3_real_manifest_domain_template.py"],"binary_patch_bytes":5874,"binary_patch_sha256":"6b26e49359f944bceafe5129b0b81a3d5600d400eae7d3b739c2baba12d6a5ca","source_blob":"c0238fba753fc7608df1c352f336199fb6ebc105","source_bytes":23737,"source_sha256":"350e393dcb3155c71cb416b18ad485197173b8c64d19cda510923c771a0ab25e","template_sha256":"a83804d299c747c485dda86eecd3bcb576a90bb2be3c2ae03fe77951ed404ad6","test_blob":"ef8273e14853446c31b47f1f093a18bac43c6f64","test_bytes":22897,"test_sha256":"0a3278c95a5a1ef11bec217e4ce06a123711fe2c884157e9c7e02d40b68b479c","consumable_for_this_package":true,"retained_eligible":false},"accepted_p3_owner":{"module":"src/camera_based_rgbww_optimizer/utils/p7_retained_r3_provenance_io.py","input_owners":["read_existing_root","read_exact_file"],"canonical_decoder":"decode_canonical_json","output_owners":["create_exclusive_root","persist_canonical_json"],"git_owner":"run_read_only_git"},"strict_retained_owner":{"module":"src/camera_based_rgbww_optimizer/optimization/p7_retained_release_audit.py","decoder":"_strict_json_load","dependencies":"_default_dependencies","requirements":["utf8","object_root","duplicate_keys_rejected","nonfinite_rejected"],"canonical_reencode":false,"schema_validation":false,"scientific_validation":false,"eligibility":false,"release_consumable":false},"accepted_p5_owner":{"implementation_commit":"37f7d0021c7a81a9d6680815bc51c305cf807a7b","source_blob":"075face6fd7453236affa303640b91eb16a42a9b","source_bytes":12320,"source_sha256":"07eaeac615ea79db45afad91ce4c82e28c1cdcb66b6119b5cdca6462d7c091d2","entrypoint":"execute_controller_runtime"},"required_full_machine_state":{"active_task_count":1,"active_task":"REF-P7-25-R2-B2-M1-R1-S1","active_plan_contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-M1-R1-S1-FRESH-REAL-INPUT-STRICT-RETAINED-V1","retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","real_manifest_domain_owner_status":"ACCEPTED_COMPLETE_GIT_GRAMMAR_VALIDATED","m1_real_manifest_candidate_commit":"0f4c09e1b2b2afbf627f6f36d57a1a65847ab4a8","m1_real_manifest_candidate_consumable":true,"m1_synthetic_integration_status":"ACCEPTED_COMPLETE_QUALIFIED_NOT_RETAINED_ELIGIBLE","m1_real_input_manifest_status":"ACTIVE_FRESH_STRICT_RETAINED_SUCCESSOR","m1_real_input_supersession_status":"ACCEPTED_COMPLETE_GIT_ER_ONLY","existing_root_identity_owner_status":"ACCEPTED_COMPLETE_COMPOSITE_VALIDATED","executer_dispatched":true,"device_authorized_by_this_file":false},"c1_input_contract":{"root":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b2-c1-path-owner-27aacbf-20260730T1547Z","root_mode":448,"files":[["path_owner_index","path-owner-index.json",12195,"b189117fdd0a9a65ca80660245ec84b7f2f533c3e496c96e76eb48a4666feb35"],["path_owner_index_seal","path-owner-index.sha256.json",682,"867d1ffad5bd29f24dc81b24a58ce66393dd688833d3a4516fe7f45ef50875e9"],["terminal_evidence","terminal-evidence.json",13455,"c21a691272ca7466271349daa5b10236c9f36dfeb481d592e9c368a87e7a4763"],["terminal_evidence_seal","terminal-evidence.sha256.json",772,"4bfebf4ad40e8c2e65ad2470faaed184f21d39eda73c13e689b09769d280752f"]],"file_mode":384,"json_acceptance":"CANONICAL_EXACT_REENCODE","direct_file_set_exact":true,"index_schema":"p7_retained_r3_path_owner_index_v1","index_status":"path_owner_resolved_waiting_for_planner"},"retained_input_contract":{"root":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-lineage-release-r3/lineage-release-32b9e67-r2-20260727T2227/child-output/lineage-release-r3","root_mode":448,"files":[["current_lineage_candidate","current-lineage-candidate.json",9819,"3a2ff5a2af200c55c925b954488c5c5dd31a35a481440d17dfcdd8b68419f2e0"],["resolved_formal_plan","resolved-formal-plan.json",15137,"cf7c78b6a6cfda4055d05f5e9bbe9914161213b380dc7736ee09e257dd45eb6b"],["setup_lineage_release","setup-lineage-release.json",1567,"0bacf1878a97fcdc4436259e132e89f6e56611df6d7fb5d5a7da28f62c98ad3e"]],"file_mode":384,"json_acceptance":"STRICT_JSON_NO_CANONICAL_REENCODE","paths_must_equal_c1_resolved_records":true,"semantic_validation":false,"consumption":false},"identity_ledger_contract":{"successful_root_reads_preserved_immediately":true,"successful_file_reads_preserved_immediately":true,"file_identity_fields":["path","data","byte_count","sha256","device","inode","mode","root"],"directory_identity_fields":["path","device","inode","mode"],"ordered_partial_ledger_on_failure":true,"raw_data_must_remain_in_memory":true,"er_json_identity_projection_fields":["label","path","byte_count","sha256","device","inode","mode","root_path","root_device","root_inode","root_mode"],"invented_or_reconstructed_rows":false},"domain_spec_contract":{"builder":"build_real_manifest_domain_template","builder_calls":1,"runtime":"execute_controller_runtime","runtime_calls":1,"controller_processes":1,"generated_git_ledgers":56,"git_argv_shape":["git","show","-s","--format=%H%x00%P%x00%s","GIT_TARGETS[index % 7]"],"target_count":7,"cycles":8,"retry":0,"fallback":0},"fresh_namespace":{"base_dir":"/Volumes/4T/temp/rgbww-optimizer","prefix":"p7-td-b-retained-r3-option-b-m1-r1-s1-<activation_short12>","source_suffix":"-source.py","output_root_suffix":"-output","source_mode":384,"output_root_mode":448,"output_artifacts":5,"output_file_mode":384,"preflight_absence_targets":2,"postappend_probes":0,"alternate":0},"success_contract":{"process_exit":0,"stderr_bytes":0,"stderr_sha256":"e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855","stdout_bytes":71,"stdout_sha256":"495d98f75ac38100658f317d531fe4a824b7325671d8e6697dbaec4c01ecebba","stdout_payload":{"artifact_count":5,"status":"sealed_subordinate_provenance_evidence"},"controller_git_ledgers":56,"controller_input_reads":7,"controller_output_reload_reads":5,"output_exact_file_set":["execution-result-admission.json","retained-r3-audit-provenance-manifest-v2.json","retained-r3-audit-provenance-manifest-v2.sha256.json","terminal-evidence.json","terminal-evidence.sha256.json"],"manifest_schema":"p7_retained_r3_audit_provenance_manifest_v2","manifest_status":"sealed_subordinate_provenance_evidence","admitted":true,"eligibility":false,"release_consumable":false,"success_label":"FRESH_M1_REAL_INPUT_MANIFEST_SEALED_NOT_RETAINED_ELIGIBLE"},"execution_budgets":{"real_input_manifest_runs":1,"outer_python_invocations":1,"fresh_absence_checks":2,"preacquisition_root_reads":2,"preacquisition_file_reads":7,"c1_canonical_decodes":4,"retained_strict_decodes":3,"builder_calls":1,"runtime_calls":1,"controller_processes":1,"source_creates":1,"output_root_creates":1,"output_artifact_writes":5,"controller_git_ledgers":56,"controller_input_root_reads":7,"controller_input_file_reads":7,"controller_output_reload_reads":5,"postaudit_source_reads":1,"postaudit_root_reads":3,"postaudit_input_file_reads":7,"postaudit_output_file_reads":5,"process_table_scans":1,"execution_result_appends":1,"postappend_operations":0,"tests":0,"compileall":0,"codegraph_sync":0,"codegraph_queries":0,"implementation_commits":0,"retry":0,"fallback":0},"zero_budgets":{"repository_code_writes":0,"repository_test_writes":0,"plan_writes_by_executer":0,"full_writes_by_executer":0,"archive_writes_by_executer":0,"debug_writes":0,"guide_writes":0,"research_writes":0,"old_m1_r1_external_reads":0,"accepted_synthetic_external_evidence_reads":0,"alternate_path_search":0,"parent_sibling_listing":0,"recursive_search":0,"input_writes":0,"retained_artifact_writes":0,"retained_canonical_reencode":0,"retained_schema_validation":0,"retained_scientific_validation":0,"real_b2_retry":0,"actual_canonical_validator_calls":0,"canonical_validator_callbacks":0,"eligibility_emissions":0,"retained_release_audit":0,"release_generation":0,"release_qualification":0,"release_copy":0,"release_consumption":0,"network":0,"dns":0,"environment":0,"credentials":0,"device":0,"camera":0,"ray":0,"strip":0,"cleanup":0,"capture":0,"formal":0,"public_analyzer":0,"td_c":0,"sentinel":0,"p8":0,"firmware":0,"deployment":0},"authorization":{"classification":"PURE_OFFLINE_READ_ONLY_EXISTING_INPUTS_AND_NEW_EVIDENCE_OUTPUT","human_device_authorization_required":false,"advisor_scientific_decision_required":false},"expected_duration":"under_10_minutes","visible_terminal_required":false,"archive":{"path":".agent-work/PLANS/20260801-0219-p7-retained-r3-b2-m1-r1-c1-supersession-acceptance-review.md","bytes":6368,"sha256":"85bf0ef3ad5cab14ef3d85ed33eeda58f68f997566f10ec2f710d41184ab3f88"},"planner_stop":"B2_M1_R1_S1_FRESH_REAL_INPUT_STRICT_RETAINED_WAITING_PLANNER_REVIEW"}`

## 1. Activation 与 immutable prior gates

Orchestrator必须先把C1 acceptance及唯一active M1-R1-S1写入FULL，并创建activation。Expected parent exact
`cb59091d67683ae0b31f3790bf8e110f610791ef`，subject exact
`chore(plan): activate strict retained real input successor`，changed paths exact为FULL、PLAN与本轮new archive。Activation后porcelain必须clean。

Executer先验证activation topology、PLAN/FULL各exact one strict machine row、required FULL subset、archive identity与accepted M1/P3/P5 Git
identities。M1 patch authoritative identity是`5874` bytes / `6b26e493...a5ca`。C1 supersession commit与ER identity必须exact匹配，旧M1-R1
record仍immutable且旧fresh namespace保持no-read/no-stat/no-list/no-glob/no-search/no-reuse/no-modify/no-delete。

任何external access前，Executer必须在内存建立append-safe evidence payload与ordered counters/identity ledgers。最终ER schema exact
`p7_td_b_retained_r3_option_b_b2_m1_r1_s1_execution_result_v1`，heading exact
`## REF-P7-25-R2-B2-M1-R1-S1 Executer handoff`。Payload从开始即保留activation、owner、budget、actual、first failure、partial identities与hard
locks；不得等七件全部成功后才创建identity数组。

## 2. Fresh namespace 与 exact2 probe budget

令`<activation_short12>`为activation full SHA前12位。Fresh targets exact two：

- source：`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-m1-r1-s1-<activation_short12>-source.py`；
- output root：同prefix加`-output`。

对这两个exact path各做一次non-following `lstat` absence probe；budget/actual必须同时记入payload。必须`2/2 absent`才可继续。任何present、
symlink、error或budget drift立即fail closed。禁止alternate、parent/sibling listing、glob、recursive search或reuse任一old namespace。该exact2是本包
全部fresh absence/presence probe budget；之后包括ER append后不得再次probe fresh path。

## 3. Exact input acquisition 与 dual JSON acceptance

只允许读取machine row冻结的C1与retained两个existing roots。以P3 `read_existing_root`各exact1取得0700 exact
`DirectoryIdentity`，每次owner成功返回后立即append完整root identity到ordered in-memory ledger。

按machine row order以P3 `read_exact_file`读取C1 four再retained three。每次成功返回后，必须在执行任何JSON decode或下一read前将完整
`FileIdentity(path,data,byte_count,sha256,device,inode,mode,root)` append到ordered in-memory ledger；不得只在全部七次成功后批量赋值。失败
handoff必须保留此前全部root/file identities，禁止clear、truncate、reconstruct或发明rows。ER JSON projection必须逐项保留label、path、bytes、
SHA、device/inode/mode与root path/device/inode/mode；raw `data`保持在内存供decode/after-comparison，不直接序列化。

C1 four各exact一次调用P3 `decode_canonical_json`，并验证index schema/status、index seal target bytes/SHA、terminal对index/index-seal identity、
terminal seal对terminal identity；index解析出的three absolute paths必须逐项等于machine row retained paths，且labels/order/type exact。

Retained three各exact一次调用production `p7_retained_release_audit._strict_json_load(data, _default_dependencies())`。该owner只证明strict
UTF-8 JSON object、duplicate-key rejected、non-finite rejected。严禁调用canonical encoder/re-encode比较、`decode_canonical_json`、schema audit、
scientific interpretation、eligibility或release consumption；不得修改、normalize、copy、repair或regenerate retained bytes。

任一root/file/JSON/linkage failure立即停止所有external acquisition，冻结first failure与当前actual/partial identity ledger，跳至sole ER append；
builder/runtime/process/output create保持0，retry/fallback0。

## 4. Single accepted M1/P5 execution

用preacquisition的exact seven identities构造accepted `RealManifestDomainTemplateSpec`；manifest activation/baseline继续绑定accepted M1 commit
`0f4c09e...`与authoritative patch `6b26e493...a5ca`。Builder `build_real_manifest_domain_template` exact1，验证typed bundle、template SHA、
artifact names5、lifecycle8、bound-results76与Git family56；direct source patch/override/second builder0。

将bundle runtime request原样交P5 `execute_controller_runtime` exact1，dependency override0。它只可exclusive create fresh source0600并launch
exact one `.venv/bin/python -` controller。Controller执行Git ledgers56、input root/file reads7/7、exclusive output root0700 exact1、canonical output
persists5/reloads5与one lifecycle；retry/fallback/second process0。Exception/nonzero保留已创建fresh evidence，不cleanup、不改path、不诊断重跑。

## 5. Pre-append terminal audit 与完整identity preservation

仅process success时，在ER append前完成最后审计：

1. source same inode/mode0600，bytes/SHA与runtime composition exact；
2. C1/retained roots each reread exact1，seven files按原order each reread exact1；每次成功return立即append post identity ledger，并与pre完整
   FileIdentity/data byte-for-byte相同；identity/data equality承接predecode结论，不重复JSON decode；
3. output root reread exact1，direct sorted set exact five；output files each reread exact1并立即append完整identity，均same-root regular0600 canonical
   JSON，无extra/missing/symlink；
4. manifest/seals/terminal/admission与spec exact；retained rows只陈述physical identity，不声明schema/science/eligibility；admission exact
   `true/false/false`；
5. owned exact-argv process scan exact1，排除outer process后residual0。

任一postaudit failure仍保留所有已完成pre/post/output identities与actual counts。成功label只能是
`FRESH_M1_REAL_INPUT_MANIFEST_SEALED_NOT_RETAINED_ELIGIBLE`，不能解释为canonical validator、retained audit、eligibility或release result。

## 6. ER lifecycle、single append 与 absolute postappend lock

所有external、process、audit和repository/Git prefix reads必须在ER append前完成。先在内存冻结final payload：

- `execution_result_appends=1`，不是0；
- fresh probes budget/actual、每项operation budget/actual与first failure；
- ordered pre/post/output identity ledgers，包括failure时partial rows；
- exact source/output artifacts/process/Git ledgers与all zero locks；
- old M1-R1 namespace immutable disposition；
- Planner stop exact `B2_M1_R1_S1_FRESH_REAL_INPUT_STRICT_RETAINED_WAITING_PLANNER_REVIEW`。

然后使用exact one `apply_patch`向ER EOF appendheading + single fenced one-line strict canonical JSON block。成功append是本包最后一个tool/file/external
side effect；append之后Git status/diff/hash、repository read、external read/stat/list/glob/search/probe、process scan与任何第二append全部exact0。
Orchestrator在后续evidence commit中负责独立prefix/diff审查。

若首次`apply_patch`被拒绝且no-write，它不是append，不得计作append1；retry/fallback为0，Executer必须停止且不得第二次尝试。不得先写
placeholder/counter0/temporary record再修正。

## 7. Locks、authorization 与 stop

Budgets以machine row为准；任何early failure只报告actual，不补跑。Repository code/test/PLAN/FULL/archive/debug/GUIDE/RESEARCH writes0；tests、
compileall、CodeGraph query/sync、implementation commit0。Old M1-R1/synthetic external evidence access0；input/retained writes0；retained canonical
reencode/schema/science0；canonical validator/callback/eligibility、retained audit、release generation/qualification/copy/consumption0；network/DNS/
environment/credentials、device/camera/Ray/strip/cleanup/capture/FORMAL/public analyzer/TD-C/sentinel/P8/firmware/deployment0。

本包是`PURE_OFFLINE_READ_ONLY_EXISTING_INPUTS_AND_NEW_EVIDENCE_OUTPUT`，不需要Human device授权或Advisor科学决定。Sole append后立即停Planner门，
不得进入validator、release、device或later stage。

维护性边界：继续复用P3 physical/canonical owner、historical strict decoder、M1 domain owner与P5 runtime owner；不新增production helper、
serializer、validator、controller或parallel evidence framework，无需架构重构。
