# P7 retained-R3 Option B：M1-R1 fresh real-input manifest-only package

**计划状态：** `WAITING_ORCHESTRATOR_ACTIVATION`

**Planner 日期：** `2026-08-01`

**Reference task：** `REF-P7-25-R2-B2-M1-R1`

**Contract：**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-M1-R1-FRESH-REAL-INPUT-MANIFEST-ONLY-V1`

**当前唯一动作：** Orchestrator记录M1-I1-S1接受结论并建立fresh activation；Executer随后只运行一次由该
activation full SHA派生的pure-offline real-input manifest-only integration。它先以accepted P3 owner读取accepted C1
四件套与其机械绑定的original retained R3三件套，再组合accepted M1 builder与P5 runtime各exact1，完成immutable
physical evidence审计与single ER handoff后停止。

**唯一 Planner stop：**
`B2_M1_R1_FRESH_REAL_INPUT_MANIFEST_WAITING_PLANNER_REVIEW`。

**本轮新归档：**
`.agent-work/PLANS/20260801-0152-p7-retained-r3-b2-m1-i1-s1-synthetic-integration-acceptance-review.md`；bytes
`7124`，SHA-256 `c957274b721f73d31f5c50fbee1156a8b3a32306491af979dded8257a0424855`；不得覆盖 earlier archives。

`PLAN_MACHINE_CONTRACT={"schema":"p7_td_b_retained_r3_option_b_b2_m1_r1_fresh_real_input_manifest_only_v1","reference_task_id":"REF-P7-25-R2-B2-M1-R1","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-M1-R1-FRESH-REAL-INPUT-MANIFEST-ONLY-V1","execution_authorized_after_orchestrator_activation":true,"activation_commit":{"expected_parent":"0a7f718a8d49eb33974ce5f22f85dd8a00ea1110","expected_subject":"chore(plan): activate fresh real input manifest seal","expected_changed_paths":[".agent-work/FULL_PLAN_REFERENCE.md",".agent-work/PLAN.md",".agent-work/PLANS/20260801-0152-p7-retained-r3-b2-m1-i1-s1-synthetic-integration-acceptance-review.md"],"clean_porcelain_required_after_activation":true},"accepted_m1_owner":{"implementation_commit":"0f4c09e1b2b2afbf627f6f36d57a1a65847ab4a8","implementation_parent":"f2b38c530a6cbac5c29d761036eb3cd2a159f3b9","implementation_subject":"fix(p7): align real manifest Git ledgers","implementation_tree":"26e10d77bd3d89ca80d6bdbef3561b3bce2a4f07","implementation_paths":["src/camera_based_rgbww_optimizer/utils/p7_retained_r3_real_manifest_domain_template.py","tests/test_p7_retained_r3_real_manifest_domain_template.py"],"binary_patch_command":"git diff --binary f2b38c530a6cbac5c29d761036eb3cd2a159f3b9 0f4c09e1b2b2afbf627f6f36d57a1a65847ab4a8 -- src/camera_based_rgbww_optimizer/utils/p7_retained_r3_real_manifest_domain_template.py tests/test_p7_retained_r3_real_manifest_domain_template.py","binary_patch_bytes":5874,"binary_patch_sha256":"6b26e49359f944bceafe5129b0b81a3d5600d400eae7d3b739c2baba12d6a5ca","superseded_er_patch_sha256":"4044c62434109516e16e1fe3daad5c56d1f3ea4558f092f2976aaaec02fc94c5","source_blob":"c0238fba753fc7608df1c352f336199fb6ebc105","source_bytes":23737,"source_sha256":"350e393dcb3155c71cb416b18ad485197173b8c64d19cda510923c771a0ab25e","template_sha256":"a83804d299c747c485dda86eecd3bcb576a90bb2be3c2ae03fe77951ed404ad6","test_blob":"ef8273e14853446c31b47f1f093a18bac43c6f64","test_bytes":22897,"test_sha256":"0a3278c95a5a1ef11bec217e4ce06a123711fe2c884157e9c7e02d40b68b479c","evidence_commit":"7d35542b4b3b24081f6652a5c4f9c15879d03055","consumable_for_this_package":true,"retained_eligible":false},"accepted_p3_owner":{"module":"src/camera_based_rgbww_optimizer/utils/p7_retained_r3_provenance_io.py","input_owners":["read_existing_root","read_exact_file"],"output_owners":["create_exclusive_root","persist_canonical_json"],"git_owner":"run_read_only_git"},"accepted_p5_owner":{"implementation_commit":"37f7d0021c7a81a9d6680815bc51c305cf807a7b","source_blob":"075face6fd7453236affa303640b91eb16a42a9b","source_bytes":12320,"source_sha256":"07eaeac615ea79db45afad91ce4c82e28c1cdcb66b6119b5cdca6462d7c091d2","entrypoint":"execute_controller_runtime"},"accepted_i1_s1":{"activation_commit":"f925a2885ee2e282ece2e230cf752658ced2d273","evidence_commit":"0a7f718a8d49eb33974ce5f22f85dd8a00ea1110","result":"FRESH_M1_SYNTHETIC_INTEGRATION_QUALIFIED_NOT_RETAINED_ELIGIBLE","external_evidence_disposition":"IMMUTABLE_NO_READ_NO_REUSE_NO_MODIFY_NO_DELETE_NO_RETRY"},"required_full_machine_state":{"active_task_count":1,"active_task":"REF-P7-25-R2-B2-M1-R1","active_plan_contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-M1-R1-FRESH-REAL-INPUT-MANIFEST-ONLY-V1","retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","real_manifest_domain_owner_status":"ACCEPTED_COMPLETE_GIT_GRAMMAR_VALIDATED","m1_real_manifest_candidate_commit":"0f4c09e1b2b2afbf627f6f36d57a1a65847ab4a8","m1_real_manifest_candidate_consumable":true,"m1_synthetic_integration_status":"ACCEPTED_COMPLETE_QUALIFIED_NOT_RETAINED_ELIGIBLE","m1_real_input_manifest_status":"ACTIVE_FRESH_REAL_INPUT_MANIFEST_ONLY","existing_root_identity_owner_status":"ACCEPTED_COMPLETE_COMPOSITE_VALIDATED","executer_dispatched":true,"device_authorized_by_this_file":false},"c1_input_contract":{"root":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b2-c1-path-owner-27aacbf-20260730T1547Z","root_mode":448,"files":[["path_owner_index","path-owner-index.json",12195,"b189117fdd0a9a65ca80660245ec84b7f2f533c3e496c96e76eb48a4666feb35"],["path_owner_index_seal","path-owner-index.sha256.json",682,"867d1ffad5bd29f24dc81b24a58ce66393dd688833d3a4516fe7f45ef50875e9"],["terminal_evidence","terminal-evidence.json",13455,"c21a691272ca7466271349daa5b10236c9f36dfeb481d592e9c368a87e7a4763"],["terminal_evidence_seal","terminal-evidence.sha256.json",772,"4bfebf4ad40e8c2e65ad2470faaed184f21d39eda73c13e689b09769d280752f"]],"file_mode":384,"direct_file_set_exact":true,"index_schema":"p7_retained_r3_path_owner_index_v1","index_status":"path_owner_resolved_waiting_for_planner"},"retained_input_contract":{"root":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-lineage-release-r3/lineage-release-32b9e67-r2-20260727T2227/child-output/lineage-release-r3","root_mode":448,"files":[["current_lineage_candidate","current-lineage-candidate.json",9819,"3a2ff5a2af200c55c925b954488c5c5dd31a35a481440d17dfcdd8b68419f2e0"],["resolved_formal_plan","resolved-formal-plan.json",15137,"cf7c78b6a6cfda4055d05f5e9bbe9914161213b380dc7736ee09e257dd45eb6b"],["setup_lineage_release","setup-lineage-release.json",1567,"0bacf1878a97fcdc4436259e132e89f6e56611df6d7fb5d5a7da28f62c98ad3e"]],"file_mode":384,"paths_must_equal_c1_resolved_records":true,"semantic_validation":false,"consumption":false},"domain_spec_contract":{"builder":"build_real_manifest_domain_template","builder_calls":1,"runtime":"execute_controller_runtime","runtime_calls":1,"controller_processes":1,"generated_git_ledgers":56,"git_argv_shape":["git","show","-s","--format=%H%x00%P%x00%s","GIT_TARGETS[index % 7]"],"target_count":7,"cycles":8,"retry":0,"fallback":0},"frozen_baseline":{"release_checkpoint":"32b9e670ff3bbea0cd1505528c2ca87c2935446c","helper_v1":"9303aa22a9bd37e8ec4f23147c78c6bea84b9a2e","integration":"3e2ebed132b6d4338bfa324bfc42c3565d2eeb3c","helper_path":"src/camera_based_rgbww_optimizer/optimization/p7_retained_release_audit.py","test_path":"tests/test_p7_retained_release_audit.py","governance_manifest_sha256":"69bbbb369e776e1aa11a227ecf3432de44bc517c7eb25828094f4820df45042e","guide_sha256":"659152f6c0ae69c90c701de4e57c352d771e4f0bf75cf9410271ba0a94200e35","advisor_decision_sha256":"842cfad090549ebf6379df4551bd4f051267e4bf93014f899c5e329c57085620","advisor_attachment_sha256":"91a88e5467e13c811794c2149b6a8d5669e613c3e259d8f4091ba08c048733d6","human_governance_override":"human_owned_local_lab","helper_disposition":"retained_release_audit_prerequisite_v1_superseded_before_real_validation"},"fresh_namespace":{"base_dir":"/Volumes/4T/temp/rgbww-optimizer","prefix":"p7-td-b-retained-r3-option-b-m1-r1-<activation_short12>","source_suffix":"-source.py","output_root_suffix":"-output","source_mode":384,"output_root_mode":448,"output_artifacts":5,"output_file_mode":384,"absence_targets":2,"alternate":0},"success_contract":{"process_exit":0,"stderr_bytes":0,"stderr_sha256":"e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855","stdout_bytes":71,"stdout_sha256":"495d98f75ac38100658f317d531fe4a824b7325671d8e6697dbaec4c01ecebba","stdout_payload":{"artifact_count":5,"status":"sealed_subordinate_provenance_evidence"},"controller_git_ledgers":56,"controller_input_reads":7,"controller_output_reload_reads":5,"output_exact_file_set":["execution-result-admission.json","retained-r3-audit-provenance-manifest-v2.json","retained-r3-audit-provenance-manifest-v2.sha256.json","terminal-evidence.json","terminal-evidence.sha256.json"],"manifest_schema":"p7_retained_r3_audit_provenance_manifest_v2","manifest_status":"sealed_subordinate_provenance_evidence","admitted":true,"eligibility":false,"release_consumable":false,"success_label":"FRESH_M1_REAL_INPUT_MANIFEST_SEALED_NOT_RETAINED_ELIGIBLE"},"execution_budgets":{"real_input_manifest_runs":1,"outer_python_invocations":1,"fresh_absence_checks":2,"preacquisition_root_reads":2,"preacquisition_file_reads":7,"builder_calls":1,"runtime_calls":1,"controller_processes":1,"source_creates":1,"output_root_creates":1,"output_artifact_writes":5,"controller_git_ledgers":56,"controller_input_root_reads":7,"controller_input_file_reads":7,"controller_output_reload_reads":5,"postaudit_root_reads":2,"postaudit_input_file_reads":7,"process_table_scans":1,"execution_result_appends":1,"tests":0,"compileall":0,"codegraph_sync":0,"codegraph_queries":0,"implementation_commits":0,"retry":0,"fallback":0},"zero_budgets":{"repository_code_writes":0,"repository_test_writes":0,"plan_writes_by_executer":0,"full_writes_by_executer":0,"archive_writes_by_executer":0,"debug_writes":0,"guide_writes":0,"research_writes":0,"old_failure_evidence_reads":0,"accepted_synthetic_external_evidence_reads":0,"alternate_path_search":0,"parent_sibling_listing":0,"recursive_search":0,"input_writes":0,"retained_artifact_writes":0,"real_b2_retry":0,"actual_canonical_validator_calls":0,"canonical_validator_callbacks":0,"eligibility_emissions":0,"retained_release_audit":0,"release_generation":0,"release_qualification":0,"release_copy":0,"release_consumption":0,"network":0,"dns":0,"environment":0,"credentials":0,"device":0,"camera":0,"ray":0,"strip":0,"cleanup":0,"capture":0,"formal":0,"public_analyzer":0,"td_c":0,"sentinel":0,"p8":0,"firmware":0,"deployment":0},"authorization":{"classification":"PURE_OFFLINE_READ_ONLY_EXISTING_INPUTS_AND_NEW_EVIDENCE_OUTPUT","human_device_authorization_required":false,"advisor_scientific_decision_required":false},"expected_duration":"under_10_minutes","visible_terminal_required":false,"archive":{"path":".agent-work/PLANS/20260801-0152-p7-retained-r3-b2-m1-i1-s1-synthetic-integration-acceptance-review.md","bytes":7124,"sha256":"c957274b721f73d31f5c50fbee1156a8b3a32306491af979dded8257a0424855"},"planner_stop":"B2_M1_R1_FRESH_REAL_INPUT_MANIFEST_WAITING_PLANNER_REVIEW"}`

## 1. Fresh activation、owner gate 与 immutable prior evidence

Orchestrator必须先将M1-I1-S1 acceptance及唯一active M1-R1写入FULL，再创建activation。Expected parent exact
`0a7f718a8d49eb33974ce5f22f85dd8a00ea1110`，subject exact
`chore(plan): activate fresh real input manifest seal`，changed paths exact为FULL、PLAN与本轮新archive。Activation后
porcelain必须clean。

Executer先验证activation topology、PLAN/FULL各exact one strict machine row、required FULL subset、archive identity与accepted
M1/P3/P5 owner Git identities。M1 patch唯一authoritative口径是machine row exact command、`5874` bytes、
`6b26e493...a5ca`；旧`4044c624...94c5`只作为superseded mismatch记录，禁止使用或修复。

旧失败M1-I1 external source/root与已接受M1-I1-S1 synthetic source/root全部immutable no-read/no-stat/no-list/no-glob/
no-search/no-reuse/no-modify/no-delete/no-cleanup/no-retry。历史B2失败roots亦不得复用。Repository中的Git/ER记录可用于gate，
但不得从其中提取旧external路径后做filesystem probe。

## 2. Fresh namespace 与 exact input acquisition

令`<activation_short12>`为新activation full SHA前12位。Fresh exact targets只有：

- source：`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-m1-r1-<activation_short12>-source.py`；
- output root：同prefix加`-output`。

任何external input read或fresh write前，对fresh source/output exact2做non-following absence check，必须`2/2 absent`；禁止alternate
name/root。随后只允许读取machine row冻结的两个existing roots，禁止parent/sibling listing、recursive search、glob或另选路径。

以P3 `read_existing_root`分别exact1获取accepted C1 root与retained root 0700 identity。再以P3 `read_exact_file`按exact order
读取C1 four及retained three各exact1，expected filename/bytes/SHA/mode必须完全匹配machine row。C1 four须strict canonical JSON并验证：
index schema/status、index seal target bytes/SHA、terminal对index/index-seal identity、terminal seal对terminal identity；index解析出的
three absolute paths必须逐项等于machine row retained paths，且三record labels/order/type facts一致。不得把C1 path evidence解释为
content validation。

Retained three须strict canonical duplicate-key/non-finite-safe JSON，但本包不判断其schema science或eligibility；只冻结各自path、bytes、
SHA、device/inode/mode及shared root identity。任一C1/retained drift立即fail closed：builder/runtime/process/output root均0，不搜索、
repair、copy、regenerate、retry或fallback；仅append ER一次并停止。

## 3. Single M1 builder 与 P5 runtime/controller

用preacquisition得到的exact seven `RealManifestInputIdentity`及machine row frozen baseline构造
`RealManifestDomainTemplateSpec`。Domain内部reference/contract保持accepted M1-S1 constants；manifest activation five-item继续绑定
accepted M1 implementation `0f4c09e...`及authoritative patch `6b26e493...a5ca`，不是本轮PLAN activation。Repo root exact
`/Users/ibobby/Projects/WLED-RGBWW`，process argv exact `.venv/bin/python -`。

`build_real_manifest_domain_template(spec)` exact1；验证typed bundle、template SHA、artifact names5、lifecycle8、bound-results contract76、
generated Git family56。禁止direct source compose/patch/edit、override、second builder或parallel manifest owner。

将bundle `runtime_request`原样交`execute_controller_runtime` exact1，dependency override0。P5只可exclusive create fresh source0600，
launch exact one controller process。Controller由P3执行Git ledgers56、existing-root acquisitions7、input exact reads7、exclusive output
root1、five canonical persists及five reloads，执行exact conformance→activation→root→inputs→evaluate→terminal→terminal_seal→admission。

Runtime exception或process nonzero时保留fresh evidence，冻结first failure及actual <= budget；不得诊断重跑、补写、cleanup、修改path、
复用source或第二process。Success必须满足machine row exact exit/stderr/stdout bytes/hash/payload。

## 4. Success-only immutable physical audit

Process success后，不再执行source：

- source必须仍为original regular0600 same inode，bytes/SHA与runtime composition exact；
- 重新以P3分别获取C1/retained two root identity各exact1，并按原order读取seven files各exact1；每个完整`FileIdentity`必须与
  preacquisition byte-for-byte/data/hash/device/inode/mode/root exact，证明controller前后无替换、增长、截断或内容漂移；
- output root保持same regular0700 identity，direct sorted file set exact machine row five names；每项same-root regular0600、strict
  canonical JSON，无extra/missing/symlink；
- manifest schema/status、activation five-item、baseline twelve-item、C1 four rows、retained three rows全部与spec exact；retained rows
  仅陈述physical identity，不声明validation、audit或consumption；
- manifest seal、terminal seal分别same-root绑定target exact bytes/SHA；admission exact
  `admitted=true, eligibility=false, release_consumable=false`；
- process table只做一次owned exact-argv scan，排除outer audit自身后residual controller exact0。

该audit不是canonical validator或retained release audit。Success label只能是
`FRESH_M1_REAL_INPUT_MANIFEST_SEALED_NOT_RETAINED_ELIGIBLE`，且只解锁Planner审查；不得自行进入B3。

## 5. Evidence、budgets、failure branches 与 stop

无论success/failure，只向ER EOF append exact1后停Planner门。Append冻结activation/owner/patch supersession、prior evidence no-read、
fresh absence、C1/retained preacquisition、path binding、builder/runtime/controller counts、Git56、process stdout/stderr、source/output five
identities/seals/admission、postaudit input identities、owned process scan、ER immutable prefix、first failure与全部zero locks。

Exact budgets见machine row：outer1、real-input run1、fresh absence2、pre root2/file7、builder/runtime/process1/1/1、source/output root
create1/1、output writes5、Git56、controller root/file reads7/7、reload5、post root2/file7、process scan1、ER append1；retry/fallback0。
任何early failure只记录actual，不补跑。

Executer不得修改repository code/test/PLAN/FULL/archive/debug/GUIDE/RESEARCH，不运行tests/compileall/CodeGraph，不stage/commit
implementation。旧failure/synthetic external evidence reads、input/retained writes、alternate discovery、canonical validator/callback、eligibility、
retained audit、release generation/qualification/copy/consumption、network/DNS/environment/credentials、device/camera/Ray/strip/cleanup/capture/
FORMAL/public analyzer/TD-C/sentinel/P8/firmware/deployment全部exact0。

## 6. Authorization 与 maintainability

本包只读Human-owned local retained evidence并在fresh external root写从属evidence；不访问或控制设备，不上传固件、不部署、不改变硬件，
属于`PURE_OFFLINE_READ_ONLY_EXISTING_INPUTS_AND_NEW_EVIDENCE_OUTPUT`。按AGENTS High-Risk Device Authorization不需要Human授权，PLAN已
明确Executer不得再次询问。同样没有未决色彩或测量科学分支，不需要Advisor决定。

维护性边界：P3继续唯一physical file/Git I/O owner，M1继续唯一manifest domain owner，P5继续唯一runtime owner；本包不新增生产module、
helper、serializer、controller、validator或parallel evidence path，无需后续重构。
