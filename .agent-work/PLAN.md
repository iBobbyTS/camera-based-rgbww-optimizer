# P7 retained-R3 Option B：M1-I1-S1 fresh synthetic integration successor

**计划状态：** `WAITING_ORCHESTRATOR_ACTIVATION`

**Planner 日期：** `2026-08-01`

**Reference task：** `REF-P7-25-R2-B2-M1-I1-S1`

**Contract：**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-M1-I1-S1-FRESH-SYNTHETIC-INTEGRATION-SUCCESSOR-V1`

**当前唯一动作：** Orchestrator记录M1-I1-C1接受结论并建立fresh activation；Executer随后只运行一次由该
activation full SHA派生的pure-offline synthetic fixture/source/root integration，组合accepted M1 builder与P5 runtime，
完成immutable physical evidence审计与single ER handoff后停止。

**唯一 Planner stop：**
`B2_M1_I1_S1_FRESH_SYNTHETIC_INTEGRATION_WAITING_PLANNER_REVIEW`。

**本轮新归档：**
`.agent-work/PLANS/20260801-0135-p7-retained-r3-b2-m1-i1-c1-git-grammar-acceptance-review.md`；bytes
`6186`，SHA-256 `d3a01adebc667447031ff1bb55f7f055c696fa74ce796d4f79f4728df2ad5764`；不得覆盖 earlier archives。

`PLAN_MACHINE_CONTRACT={"schema":"p7_td_b_retained_r3_option_b_b2_m1_i1_s1_fresh_synthetic_integration_successor_v1","reference_task_id":"REF-P7-25-R2-B2-M1-I1-S1","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-M1-I1-S1-FRESH-SYNTHETIC-INTEGRATION-SUCCESSOR-V1","execution_authorized_after_orchestrator_activation":true,"activation_commit":{"expected_parent":"7d35542b4b3b24081f6652a5c4f9c15879d03055","expected_subject":"chore(plan): activate fresh real manifest synthetic integration","expected_changed_paths":[".agent-work/FULL_PLAN_REFERENCE.md",".agent-work/PLAN.md",".agent-work/PLANS/20260801-0135-p7-retained-r3-b2-m1-i1-c1-git-grammar-acceptance-review.md"],"clean_porcelain_required_after_activation":true},"accepted_m1_owner":{"implementation_commit":"0f4c09e1b2b2afbf627f6f36d57a1a65847ab4a8","implementation_parent":"f2b38c530a6cbac5c29d761036eb3cd2a159f3b9","implementation_subject":"fix(p7): align real manifest Git ledgers","implementation_tree":"26e10d77bd3d89ca80d6bdbef3561b3bce2a4f07","implementation_paths":["src/camera_based_rgbww_optimizer/utils/p7_retained_r3_real_manifest_domain_template.py","tests/test_p7_retained_r3_real_manifest_domain_template.py"],"binary_patch_command":"git diff --binary f2b38c530a6cbac5c29d761036eb3cd2a159f3b9 0f4c09e1b2b2afbf627f6f36d57a1a65847ab4a8 -- src/camera_based_rgbww_optimizer/utils/p7_retained_r3_real_manifest_domain_template.py tests/test_p7_retained_r3_real_manifest_domain_template.py","binary_patch_bytes":5874,"binary_patch_sha256":"6b26e49359f944bceafe5129b0b81a3d5600d400eae7d3b739c2baba12d6a5ca","superseded_er_patch_sha256":"4044c62434109516e16e1fe3daad5c56d1f3ea4558f092f2976aaaec02fc94c5","patch_identity_owner":"PLANNER_INDEPENDENT_GIT_OBJECT_RECOMPUTATION","source_blob":"c0238fba753fc7608df1c352f336199fb6ebc105","source_bytes":23737,"source_sha256":"350e393dcb3155c71cb416b18ad485197173b8c64d19cda510923c771a0ab25e","template_sha256":"a83804d299c747c485dda86eecd3bcb576a90bb2be3c2ae03fe77951ed404ad6","test_blob":"ef8273e14853446c31b47f1f093a18bac43c6f64","test_bytes":22897,"test_sha256":"0a3278c95a5a1ef11bec217e4ce06a123711fe2c884157e9c7e02d40b68b479c","evidence_commit":"7d35542b4b3b24081f6652a5c4f9c15879d03055","consumable_for_this_package":true,"retained_eligible":false},"accepted_runtime_owner":{"implementation_commit":"37f7d0021c7a81a9d6680815bc51c305cf807a7b","source_blob":"075face6fd7453236affa303640b91eb16a42a9b","source_sha256":"07eaeac615ea79db45afad91ce4c82e28c1cdcb66b6119b5cdca6462d7c091d2","entrypoint":"execute_controller_runtime"},"reviewed_failure":{"activation_commit":"2f2899ac769d0ac30662b495dfbdfd06fe508282","evidence_commit":"99bc4ec1710395fc54772343fc650daf7d29e7d4","stable_code":"git_command_denied","failure_evidence_disposition":"IMMUTABLE_NO_READ_NO_REUSE_NO_MODIFY_NO_DELETE_NO_RETRY"},"required_full_machine_state":{"active_task_count":1,"active_task":"REF-P7-25-R2-B2-M1-I1-S1","active_plan_contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-M1-I1-S1-FRESH-SYNTHETIC-INTEGRATION-SUCCESSOR-V1","retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","real_manifest_domain_owner_status":"ACCEPTED_COMPLETE_GIT_GRAMMAR_VALIDATED","m1_real_manifest_candidate_commit":"0f4c09e1b2b2afbf627f6f36d57a1a65847ab4a8","m1_real_manifest_candidate_consumable":true,"m1_synthetic_integration_status":"ACTIVE_FRESH_ACTIVATION_DERIVED_SUCCESSOR","existing_root_identity_owner_status":"ACCEPTED_COMPLETE_COMPOSITE_VALIDATED","executer_dispatched":true,"device_authorized_by_this_file":false},"domain_spec_contract":{"reference_task_id":"REF-P7-25-R2-B2-M1-S1","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-M1-S1-REAL-MANIFEST-DOMAIN-TEMPLATE-SUCCESSOR-V1","builder":"build_real_manifest_domain_template","builder_calls":1,"runtime":"execute_controller_runtime","runtime_calls":1,"controller_processes":1,"generated_git_ledgers":56,"git_argv_shape":["git","show","-s","--format=%H%x00%P%x00%s","GIT_TARGETS[index % 7]"],"target_count":7,"cycles":8,"retry":0,"fallback":0},"frozen_baseline":{"activation_commit":"0f4c09e1b2b2afbf627f6f36d57a1a65847ab4a8","activation_parent":"f2b38c530a6cbac5c29d761036eb3cd2a159f3b9","activation_subject":"fix(p7): align real manifest Git ledgers","activation_changed_paths":["src/camera_based_rgbww_optimizer/utils/p7_retained_r3_real_manifest_domain_template.py","tests/test_p7_retained_r3_real_manifest_domain_template.py"],"activation_patch_sha256":"6b26e49359f944bceafe5129b0b81a3d5600d400eae7d3b739c2baba12d6a5ca","release_checkpoint":"32b9e670ff3bbea0cd1505528c2ca87c2935446c","helper_v1":"9303aa22a9bd37e8ec4f23147c78c6bea84b9a2e","integration":"3e2ebed132b6d4338bfa324bfc42c3565d2eeb3c","helper_path":"src/camera_based_rgbww_optimizer/optimization/p7_retained_release_audit.py","test_path":"tests/test_p7_retained_release_audit.py","governance_manifest_sha256":"69bbbb369e776e1aa11a227ecf3432de44bc517c7eb25828094f4820df45042e","guide_sha256":"659152f6c0ae69c90c701de4e57c352d771e4f0bf75cf9410271ba0a94200e35","advisor_decision_sha256":"842cfad090549ebf6379df4551bd4f051267e4bf93014f899c5e329c57085620","advisor_attachment_sha256":"91a88e5467e13c811794c2149b6a8d5669e613c3e259d8f4091ba08c048733d6","human_governance_override":"human_owned_local_lab","helper_disposition":"retained_release_audit_prerequisite_v1_superseded_before_real_validation"},"seam_chain":[{"repo_path":"src/camera_based_rgbww_optimizer/optimization/p7_retained_release_audit.py","before_blob_oid":"57aded4a77219d1966bb4303331ec1e4a29f2e1c","after_blob_oid":"b3daada521d3eec98ac0ac8382a8846546aaf780","before_sha256":"82713766baa2c66a2fa6e0d64796d9f1fe280ede98f41ab5c453fb32cfc63d9a","after_sha256":"48c0c57fb95c08205c3fef7b23e6df3729928352cd23e1722e8693b9f3634cf8","binary_patch_sha256":"ff3a44f6ebc539026ed6c8ac62966aab29d97f211cd5b7f7b62ef9d52c59eb2e"},{"repo_path":"tests/test_p7_retained_release_audit.py","before_blob_oid":"f55cb67be8e4a9dcee3e5e3208c8b946eb38f247","after_blob_oid":"c1ec87913783cba4cc4322729d2222986953b1f0","before_sha256":"e5df8f007745593ecbd9c5df3d5430b58c65b7fdb6fd0f1b0a00462ef7650900","after_sha256":"c8d6c7c99815d823871ecfddce79eadd5d5def918affbcd7e4ce86de691d1b3f","binary_patch_sha256":"5c900c5245b24a3cafe836e72aea705522eee8c782d5f3626cc136537042e2f4"}],"synthetic_fixture_contract":{"base_dir":"/Volumes/4T/temp/rgbww-optimizer","name_prefix":"p7-td-b-retained-r3-option-b-m1-i1-s1-<activation_short12>","source_suffix":"-source.py","output_root_suffix":"-output","input_root_suffixes":["-input-00","-input-01","-input-02","-input-03","-input-04","-input-05","-input-06"],"c1_labels":["path_owner_index","path_owner_index_seal","terminal_evidence","terminal_evidence_seal"],"retained_labels":["current_lineage_candidate","resolved_formal_plan","setup_lineage_release"],"input_payload_shape":{"label":"exact_label","synthetic":true},"input_roots":7,"input_files":7,"input_root_mode":448,"input_file_mode":384,"source_mode":384,"output_root_mode":448,"output_artifacts":5,"output_file_mode":384,"old_path_reuse":false},"success_contract":{"process_exit":0,"stderr_bytes":0,"stderr_sha256":"e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855","stdout_bytes":71,"stdout_sha256":"495d98f75ac38100658f317d531fe4a824b7325671d8e6697dbaec4c01ecebba","stdout_payload":{"artifact_count":5,"status":"sealed_subordinate_provenance_evidence"},"controller_git_ledgers":56,"controller_input_reads":7,"controller_output_reload_reads":5,"output_exact_file_set":["execution-result-admission.json","retained-r3-audit-provenance-manifest-v2.json","retained-r3-audit-provenance-manifest-v2.sha256.json","terminal-evidence.json","terminal-evidence.sha256.json"],"manifest_schema":"p7_retained_r3_audit_provenance_manifest_v2","manifest_status":"sealed_subordinate_provenance_evidence","terminal_status":"sealed_subordinate_provenance_evidence","admitted":true,"eligibility":false,"release_consumable":false,"success_label":"FRESH_M1_SYNTHETIC_INTEGRATION_QUALIFIED_NOT_RETAINED_ELIGIBLE"},"execution_budgets":{"synthetic_integration_runs":1,"outer_python_invocations":1,"builder_calls":1,"runtime_calls":1,"controller_processes":1,"source_creates":1,"input_root_creates":7,"input_artifact_writes":7,"output_root_creates":1,"output_artifact_writes":5,"controller_git_ledgers":56,"execution_result_appends":1,"tests":0,"compileall":0,"codegraph_sync":0,"codegraph_queries":0,"implementation_commits":0,"retry":0,"fallback":0},"zero_budgets":{"repository_code_writes":0,"repository_test_writes":0,"plan_writes_by_executer":0,"full_writes_by_executer":0,"archive_writes_by_executer":0,"debug_writes":0,"guide_writes":0,"research_writes":0,"old_failure_er_prefix_writes":0,"old_failed_fresh_evidence_reads":0,"old_failed_fresh_evidence_writes":0,"old_failed_fresh_evidence_deletes":0,"old_external_source_reads":0,"old_external_root_reads":0,"accepted_c1_physical_reads":0,"retained_artifact_physical_reads":0,"real_b2_dispatch":0,"actual_canonical_validator_calls":0,"canonical_validator_callbacks":0,"eligibility_emissions":0,"retained_release_audit":0,"release_generation":0,"release_qualification":0,"release_copy":0,"release_consumption":0,"network":0,"dns":0,"environment":0,"credentials":0,"device":0,"camera":0,"ray":0,"strip":0,"cleanup":0,"capture":0,"formal":0,"public_analyzer":0,"td_c":0,"sentinel":0,"p8":0,"firmware":0,"deployment":0},"expected_duration":"under_10_minutes","visible_terminal_required":false,"archive":{"path":".agent-work/PLANS/20260801-0135-p7-retained-r3-b2-m1-i1-c1-git-grammar-acceptance-review.md","bytes":6186,"sha256":"d3a01adebc667447031ff1bb55f7f055c696fa74ce796d4f79f4728df2ad5764"},"planner_stop":"B2_M1_I1_S1_FRESH_SYNTHETIC_INTEGRATION_WAITING_PLANNER_REVIEW"}`

## 1. Fresh activation 与 accepted owner gate

Orchestrator必须先把本轮acceptance与唯一active task写入FULL，再创建fresh activation。Activation parent exact
`7d35542b4b3b24081f6652a5c4f9c15879d03055`，subject exact
`chore(plan): activate fresh real manifest synthetic integration`，changed paths exact：

1. `.agent-work/FULL_PLAN_REFERENCE.md`；
2. `.agent-work/PLAN.md`；
3. `.agent-work/PLANS/20260801-0135-p7-retained-r3-b2-m1-i1-c1-git-grammar-acceptance-review.md`。

Activation后porcelain必须clean。Executer先验证activation topology、PLAN/FULL唯一strict JSON machine row、required FULL
subset与archive identity；再验证accepted M1/P5 commit、subject、path、blob、bytes、SHA-256及M1 authoritative patch command/
bytes/hash。任一不符时external path read/create、builder/runtime/process均为0，只append ER一次并停止。

ER历史patch hash `4044c624...94c5`已由Planner归类为non-authoritative evidence mismatch；唯一authoritative patch identity是
machine row的普通exact two-path `git diff --binary`命令、`5874` bytes与`6b26e493...a5ca`。Executer不得修改旧ER，也不得
重新解释、fallback或选择另一个patch口径。

## 2. Old failure immutable lock 与 fresh path derivation

旧M1-I1 activation `2f2899ac...`产生的source、seven input roots/files和未创建output root由evidence `99bc4ec...`冻结。
Executer不得读取、stat、list、glob、search、复用、修改、删除、cleanup或retry其任何external path；不得运行旧controller或复用
其source/spec/fixture identity。读取repository中的PLAN/FULL/ER Git证据不等于读取旧external root，但不得以ER路径做filesystem probe。

令`<activation_short12>`为本轮新activation full SHA前12位。fresh exact targets：

- source：`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-m1-i1-s1-<activation_short12>-source.py`；
- output root：同prefix加`-output`；
- seven input roots：同prefix依次加`-input-00`至`-input-06`；
- 每个input file为其root direct child，filename使用对应exact label加`.json`。

任何create/write前，对fresh source + output + seven inputs exact nine targets各做non-following absence check；必须全部absent。
不得搜索alternate root，也不得读取真实C1 path-owner root或retained R3 root。任一fresh target已存在立即停止，retry/fallback/
alternate exact0。

## 3. Seven synthetic fixtures 与 frozen spec

使用accepted P3 `create_exclusive_root`为seven fresh input roots各exact一次创建0700 root，再以
`persist_canonical_json`各exact一次写0600 direct child。Payload exact
`{"label":"<exact label>","synthetic":true}`，由P3 canonical owner编码。写后使用P3 root-bound exact readback冻结每项
path、bytes、SHA-256、device/inode/mode与root identity。Labels/order exact C1 four followed byretained three。

将machine row frozen baseline与seven synthetic physical identities构造`RealManifestDomainTemplateSpec`。Builder内部domain
`reference_task_id`/`contract_id`保持accepted M1-S1 constants，不因当前M1-I1-S1改写。Source/output/repo/process argv使用fresh
exact paths、repo root `/Users/ibobby/Projects/WLED-RGBWW`及其`.venv/bin/python -`。

`build_real_manifest_domain_template(spec)` exact1；验证bundle typed owner、template/replacement SHA、runtime request、artifact names
exact5、lifecycle order exact8及generated Git family exact56。不得直接compose/patch/edit generated source、增加override或第二builder。

## 4. Single P5 runtime/controller integration

将bundle `runtime_request`原样交给accepted P5 `execute_controller_runtime` exact1，dependency override0。P5应compose/analyze
accepted M1 source，O_EXCL|O_NOFOLLOW创建source exact1，launch exact一个`.venv/bin/python -` process。Controller必须成功执行
P3-eligible read-only Git ledgers exact56，target 0..6循环8次；existing-root acquisition7、synthetic input read7、exclusive output
root1、output persist/reload5与existing lifecycle exact1。

若runtime抛错或process非零，立即保留本轮fresh evidence，记录first failure与actual counts，不得诊断重跑、修改path或补齐未执行项。
Success必须满足process exit0、stderr empty及machine row exact stdout bytes/hash/payload。

## 5. Success-only immutable physical audit

Process success后，在不执行source第二次的条件下独立只读审计：

- source为原inode regular0600，bytes/SHA与runtime composition/identity exact；
- seven fresh input roots/files与controller前冻结identities逐项不变，每root exact one direct regular0600 canonical JSON file；
- output root为0700且before/after identity一致，direct file set exact machine row five names，全部regular0600、same-root、strict
  canonical JSON，无额外/缺失/symlink；
- manifest schema/status、activation five-item list、baseline twelve-item list、C1 four rows与retained three rows全部与spec exact；
  activation patch只接受`6b26e493...a5ca`，不得claim eligibility、release usability或device authorization；
- manifest/terminal sidecar分别same-root绑定target exact bytes/SHA；admission exact
  `admitted=true, eligibility=false, release_consumable=false`；
- process-table只做一次owned exact argv scan，residual process exact0。

该audit不是canonical validator或retained audit；success label只能是
`FRESH_M1_SYNTHETIC_INTEGRATION_QUALIFIED_NOT_RETAINED_ELIGIBLE`。

## 6. Evidence、budgets、failure branches 与 stop

本package不改repository code/test，不运行tests、compileall或CodeGraph，不stage/commit implementation。无论success/failure，只向
ER做一次EOF append并停Planner门。Append必须冻结activation/owner/authoritative patch identities、old-failure no-read ledger、fresh
path/absence gate、seven fixtures、spec/bundle/runtime counts、Git56、source/process/output identities/payload、owned process scan、ER
immutable prefix、first failure及全部zero budgets。

预算exact：outer Python1、synthetic integration1、builder1、runtime1、controller process1、source create1、input root create7、input
artifact write7、output root create1、output artifact write5、controller Git ledger56、ER append1；retry/fallback0。任何early failure只报告
actual <= budget，不补跑。

以下全部exact0：repository code/test/PLAN/FULL/archive/debug/GUIDE/RESEARCH write by Executer；旧failure external evidence read/
write/delete/reuse；真实C1/retained physical read；real B2；canonical validator/callback；eligibility emission；retained audit；release
generation/qualification/copy/consumption；network/DNS/environment/credentials；device/camera/Ray/strip/cleanup/capture/FORMAL/public
analyzer/TD-C/sentinel/P8/firmware/deployment。

本包是under-ten-minute pure-offline integration，不需要visible Terminal、Advisor scientific decision或Human危险设备授权。全绿也不得
自行进入M1-R1。

维护性边界：只以一次fresh external synthetic composition验证M1/P5既有owner，不增加生产module、helper、serializer、controller、
validator或parallel evidence owner；旧failure evidence保持immutable，新的activation-derived namespace避免复用与隐藏状态。
