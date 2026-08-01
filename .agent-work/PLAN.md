# P7 retained-R3 Option B：M1-I1 fresh pure-offline synthetic integration

**计划状态：** `WAITING_ORCHESTRATOR_ACTIVATION`

**Planner 日期：** `2026-08-01`

**Reference task：** `REF-P7-25-R2-B2-M1-I1`

**Contract：**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-M1-I1-FRESH-SYNTHETIC-INTEGRATION-V1`

**当前唯一动作：** Orchestrator接受 M1 composite owner并建立fresh activation；Executer随后只运行一次
activation-derived、pure-offline synthetic fixture/source/root integration，组合已接受的 M1 builder 与 P5 runtime，
完成immutable physical evidence审计与single ER handoff后停止。

**唯一 Planner stop：**
`B2_M1_I1_FRESH_SYNTHETIC_INTEGRATION_WAITING_PLANNER_REVIEW`。

**本轮新归档：**
`.agent-work/PLANS/20260801-0101-p7-retained-r3-b2-m1-s1-canonical-json-acceptance-review.md`；bytes
`9014`，SHA-256 `91f5bed95569c1d94b37c3a2f9789cd6966abdf439982417485003475310e4d3`；不得覆盖
earlier archives。

`PLAN_MACHINE_CONTRACT={"schema":"p7_td_b_retained_r3_option_b_b2_m1_i1_fresh_synthetic_integration_v1","reference_task_id":"REF-P7-25-R2-B2-M1-I1","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-M1-I1-FRESH-SYNTHETIC-INTEGRATION-V1","execution_authorized_after_orchestrator_activation":true,"activation_commit":{"expected_parent":"216946495c455c91d433c4e70b32c14b940428fa","expected_subject":"chore(plan): activate real manifest synthetic integration","expected_changed_paths":[".agent-work/FULL_PLAN_REFERENCE.md",".agent-work/PLAN.md",".agent-work/PLANS/20260801-0101-p7-retained-r3-b2-m1-s1-canonical-json-acceptance-review.md"],"clean_porcelain_required_after_activation":true},"accepted_m1_owner":{"implementation_commit":"c480c4065081eab06388a12e95fd79b37b0230e2","implementation_parent":"db4703a2e13f8314cfe529551078e60567678bf7","implementation_subject":"fix(p7): project real manifest into canonical JSON","implementation_tree":"df6ce2d1b8adcf0f5b9d30b4f9936312a37b1529","implementation_paths":["src/camera_based_rgbww_optimizer/utils/p7_retained_r3_real_manifest_domain_template.py","tests/test_p7_retained_r3_real_manifest_domain_template.py"],"binary_patch_bytes":4827,"binary_patch_sha256":"c536bf657b1ccb5021c823a12c586c45e014f713b7a367f62a7964a243967f01","source_blob":"4bf50cf69f259f212e34d9be5eacd7721ed91c41","source_bytes":23725,"source_sha256":"8016df1265a82a49b90c7bbe33ccf7621c61ac9568538f159aea4f84fca3543f","test_blob":"4036e05ed0ad92d4afc52df69b9a7cf7356c8fef","test_bytes":20374,"test_sha256":"d8bff33770aba2b002b25652e086e5f45f5ef646cc0ade97d1a7be8ea7a99fc4","evidence_commit":"216946495c455c91d433c4e70b32c14b940428fa","consumable_for_this_package":true,"retained_eligible":false},"accepted_runtime_owner":{"implementation_commit":"37f7d0021c7a81a9d6680815bc51c305cf807a7b","source_blob":"075face6fd7453236affa303640b91eb16a42a9b","source_sha256":"07eaeac615ea79db45afad91ce4c82e28c1cdcb66b6119b5cdca6462d7c091d2","entrypoint":"execute_controller_runtime"},"required_full_machine_state":{"active_task_count":1,"active_task":"REF-P7-25-R2-B2-M1-I1","active_plan_contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-M1-I1-FRESH-SYNTHETIC-INTEGRATION-V1","retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","real_manifest_domain_owner_status":"ACCEPTED_COMPLETE_CANONICAL_JSON_VALIDATED","m1_real_manifest_candidate_commit":"c480c4065081eab06388a12e95fd79b37b0230e2","m1_real_manifest_candidate_consumable":true,"m1_synthetic_integration_status":"ACTIVE_FRESH_PURE_OFFLINE","existing_root_identity_owner_status":"ACCEPTED_COMPLETE_COMPOSITE_VALIDATED","executer_dispatched":true,"device_authorized_by_this_file":false},"domain_spec_contract":{"reference_task_id":"REF-P7-25-R2-B2-M1-S1","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-M1-S1-REAL-MANIFEST-DOMAIN-TEMPLATE-SUCCESSOR-V1","builder":"build_real_manifest_domain_template","builder_calls":1,"runtime":"execute_controller_runtime","runtime_calls":1,"controller_processes":1,"retry":0,"fallback":0},"frozen_baseline":{"activation_commit":"c480c4065081eab06388a12e95fd79b37b0230e2","activation_parent":"db4703a2e13f8314cfe529551078e60567678bf7","activation_subject":"fix(p7): project real manifest into canonical JSON","activation_changed_paths":["src/camera_based_rgbww_optimizer/utils/p7_retained_r3_real_manifest_domain_template.py","tests/test_p7_retained_r3_real_manifest_domain_template.py"],"activation_patch_sha256":"c536bf657b1ccb5021c823a12c586c45e014f713b7a367f62a7964a243967f01","release_checkpoint":"32b9e670ff3bbea0cd1505528c2ca87c2935446c","helper_v1":"9303aa22a9bd37e8ec4f23147c78c6bea84b9a2e","integration":"3e2ebed132b6d4338bfa324bfc42c3565d2eeb3c","helper_path":"src/camera_based_rgbww_optimizer/optimization/p7_retained_release_audit.py","test_path":"tests/test_p7_retained_release_audit.py","governance_manifest_sha256":"69bbbb369e776e1aa11a227ecf3432de44bc517c7eb25828094f4820df45042e","guide_sha256":"659152f6c0ae69c90c701de4e57c352d771e4f0bf75cf9410271ba0a94200e35","advisor_decision_sha256":"842cfad090549ebf6379df4551bd4f051267e4bf93014f899c5e329c57085620","advisor_attachment_sha256":"91a88e5467e13c811794c2149b6a8d5669e613c3e259d8f4091ba08c048733d6","human_governance_override":"human_owned_local_lab","helper_disposition":"retained_release_audit_prerequisite_v1_superseded_before_real_validation"},"seam_chain":[{"repo_path":"src/camera_based_rgbww_optimizer/optimization/p7_retained_release_audit.py","before_blob_oid":"57aded4a77219d1966bb4303331ec1e4a29f2e1c","after_blob_oid":"b3daada521d3eec98ac0ac8382a8846546aaf780","before_sha256":"82713766baa2c66a2fa6e0d64796d9f1fe280ede98f41ab5c453fb32cfc63d9a","after_sha256":"48c0c57fb95c08205c3fef7b23e6df3729928352cd23e1722e8693b9f3634cf8","binary_patch_sha256":"ff3a44f6ebc539026ed6c8ac62966aab29d97f211cd5b7f7b62ef9d52c59eb2e"},{"repo_path":"tests/test_p7_retained_release_audit.py","before_blob_oid":"f55cb67be8e4a9dcee3e5e3208c8b946eb38f247","after_blob_oid":"c1ec87913783cba4cc4322729d2222986953b1f0","before_sha256":"e5df8f007745593ecbd9c5df3d5430b58c65b7fdb6fd0f1b0a00462ef7650900","after_sha256":"c8d6c7c99815d823871ecfddce79eadd5d5def918affbcd7e4ce86de691d1b3f","binary_patch_sha256":"5c900c5245b24a3cafe836e72aea705522eee8c782d5f3626cc136537042e2f4"}],"synthetic_fixture_contract":{"base_dir":"/Volumes/4T/temp/rgbww-optimizer","name_prefix":"p7-td-b-retained-r3-option-b-m1-i1-<activation_short12>","source_suffix":"-source.py","output_root_suffix":"-output","input_root_suffixes":["-input-00","-input-01","-input-02","-input-03","-input-04","-input-05","-input-06"],"c1_labels":["path_owner_index","path_owner_index_seal","terminal_evidence","terminal_evidence_seal"],"retained_labels":["current_lineage_candidate","resolved_formal_plan","setup_lineage_release"],"input_payload_shape":{"label":"exact_label","synthetic":true},"input_roots":7,"input_files":7,"input_root_mode":448,"input_file_mode":384,"source_mode":384,"output_root_mode":448,"output_artifacts":5,"output_file_mode":384,"old_path_reuse":false},"success_contract":{"process_exit":0,"stderr_bytes":0,"stderr_sha256":"e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855","stdout_bytes":71,"stdout_sha256":"495d98f75ac38100658f317d531fe4a824b7325671d8e6697dbaec4c01ecebba","stdout_payload":{"artifact_count":5,"status":"sealed_subordinate_provenance_evidence"},"controller_git_ledgers":56,"controller_input_reads":7,"controller_output_reload_reads":5,"output_exact_file_set":["execution-result-admission.json","retained-r3-audit-provenance-manifest-v2.json","retained-r3-audit-provenance-manifest-v2.sha256.json","terminal-evidence.json","terminal-evidence.sha256.json"],"manifest_schema":"p7_retained_r3_audit_provenance_manifest_v2","manifest_status":"sealed_subordinate_provenance_evidence","terminal_status":"sealed_subordinate_provenance_evidence","admitted":true,"eligibility":false,"release_consumable":false,"success_label":"FRESH_M1_SYNTHETIC_INTEGRATION_QUALIFIED_NOT_RETAINED_ELIGIBLE"},"execution_budgets":{"synthetic_integration_runs":1,"outer_python_invocations":1,"builder_calls":1,"runtime_calls":1,"controller_processes":1,"source_creates":1,"input_root_creates":7,"input_artifact_writes":7,"output_root_creates":1,"output_artifact_writes":5,"controller_git_ledgers":56,"execution_result_appends":1,"tests":0,"compileall":0,"codegraph_sync":0,"codegraph_queries":0,"implementation_commits":0,"retry":0,"fallback":0},"zero_budgets":{"repository_code_writes":0,"repository_test_writes":0,"plan_writes_by_executer":0,"full_writes_by_executer":0,"archive_writes_by_executer":0,"debug_writes":0,"guide_writes":0,"research_writes":0,"old_external_source_reads":0,"old_external_root_reads":0,"accepted_c1_physical_reads":0,"retained_artifact_physical_reads":0,"real_b2_dispatch":0,"actual_canonical_validator_calls":0,"canonical_validator_callbacks":0,"eligibility_emissions":0,"retained_release_audit":0,"release_generation":0,"release_qualification":0,"release_copy":0,"release_consumption":0,"network":0,"dns":0,"environment":0,"credentials":0,"device":0,"camera":0,"ray":0,"strip":0,"cleanup":0,"capture":0,"formal":0,"public_analyzer":0,"td_c":0,"sentinel":0,"p8":0,"firmware":0,"deployment":0},"expected_duration":"under_10_minutes","visible_terminal_required":false,"archive":{"path":".agent-work/PLANS/20260801-0101-p7-retained-r3-b2-m1-s1-canonical-json-acceptance-review.md","bytes":9014,"sha256":"91f5bed95569c1d94b37c3a2f9789cd6966abdf439982417485003475310e4d3"},"planner_stop":"B2_M1_I1_FRESH_SYNTHETIC_INTEGRATION_WAITING_PLANNER_REVIEW"}`

## 1. Fresh activation 与 accepted owner gate

Orchestrator必须先把本轮接受结论和唯一 active task 写入 FULL，再创建fresh activation。Activation parent必须是
current evidence HEAD `216946495c455c91d433c4e70b32c14b940428fa`，subject exact
`chore(plan): activate real manifest synthetic integration`，changed paths exact：

1. `.agent-work/FULL_PLAN_REFERENCE.md`；
2. `.agent-work/PLAN.md`；
3. `.agent-work/PLANS/20260801-0101-p7-retained-r3-b2-m1-s1-canonical-json-acceptance-review.md`。

Activation后porcelain必须clean。Executer先验证 activation topology、PLAN/FULL唯一 strict JSON machine row、required
FULL subset与archive identity；再验证 accepted M1/P5 commit、subject、path、blob、bytes、SHA-256及M1 patch。任一不符时
external path read/create、builder/runtime/process均为0，只append ER一次并停止。

Accepted M1 owner是 `c480c406...`，不是 historical rejected candidate `cddd23e...`。后者继续
non-consumable。M1 acceptance只授权本 synthetic integration；retained R3仍未验证、未消费。

## 2. Fresh path derivation 与 no-reuse gate

令 `<activation_short12>` 为本轮activation full SHA前12位。所有fresh paths必须严格从它派生：

- source：`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-m1-i1-<activation_short12>-source.py`；
- output root：同prefix加`-output`；
- seven input roots：同prefix依次加`-input-00`至`-input-06`；
- 每个input file为其root direct child，filename使用对应exact label加`.json`。

在任何create/write前，对exact nine targets（source + output + seven inputs）各做non-following absence check；必须全部
absent。不得搜索alternate root、读取/复用/修复/删除任何旧 P7-I1/M1 failure source/root，也不得读取真实 C1
path-owner root或retained R3 root。任一target已存在立即停止，retry/fallback/alternate为0。

## 3. Seven synthetic fixtures 与 frozen spec

使用accepted P3 `create_exclusive_root`为seven input roots各exact一次创建0700 root；随后以
`persist_canonical_json`各exact一次写0600 direct child。Payload exact
`{"label":"<exact label>","synthetic":true}`，由P3 canonical sorted compact UTF-8 JSON+LF owner编码；不得手写
alternate serializer。写后用P3 root-bound exact readback冻结每项path、bytes、SHA-256、device/inode/mode及root
device/inode/mode。七项labels/order必须为machine row exact C1 four followed by retained three。

将machine row frozen baseline与runtime取得的seven physical identities构造
`RealManifestDomainTemplateSpec`。Active PLAN task是M1-I1，但accepted builder内部domain spec的
`reference_task_id`/`contract_id`必须保持它已验证的 M1-S1 exact constants；不得为了本integration修改builder或伪造
新的contract。Source/output/repo/process argv使用fresh exact paths、repo root
`/Users/ibobby/Projects/WLED-RGBWW`及其`.venv/bin/python -`。

`build_real_manifest_domain_template(spec)` exact一次。必须验证bundle typed owner、template/replacement SHA、runtime request
path/argv、artifact names exact five、lifecycle order exact eight。不得直接compose/patch/edit generated source，不得增加
override或第二builder。

## 4. Single P5 runtime/controller integration

把bundle `runtime_request`原样交给 accepted P5 `execute_controller_runtime` exact一次，dependencies override为0。P5应：

1. compose/analyze accepted M1 source；
2. O_EXCL|O_NOFOLLOW写source exact一次为0600，fsync、root-bound readback；
3. launch exact一个 `.venv/bin/python -` process，并把source bytes作为stdin exact一次；
4. controller执行Git read-only ledgers exact56、existing-root acquisition exact7、input read exact7、exclusive output
   root exact1、output persist/reload exact5与existing lifecycle exact一次；
5. 无retry/fallback、second source/root/process或cleanup/delete/repair。

若runtime抛错或process非零，立即保留已产生的fresh evidence不变，记录first failure、实际phase/count、stdout/stderr/identity，
不得诊断性重跑或修改任何path。Success必须满足process exit0、stderr empty及machine row exact stdout bytes/hash/payload。

## 5. Success-only immutable physical audit

Process success后，在不执行source的条件下独立只读审计：

- source为原inode regular0600，bytes/SHA与runtime composition/identity exact；
- seven input roots/files与controller前冻结identities逐项完全不变，每个root exact one direct regular0600 file，payload
  strict canonical JSON且label/synthetic值exact；
- output root physical directory0700且before/after identity一致，direct file set exact machine row five names，全部
  regular0600、same-root、strict canonical JSON；不得出现额外/缺失/symlink；
- manifest schema/status exact；activation是ordered five-item list、baseline ordered twelve-item list with two six-item
  seam rows、C1 exact four eleven-item rows、retained exact three eleven-item rows；所有值等于spec，且manifest不得claim
  eligibility、release usability或device authorization；
- manifest/terminal sidecars分别绑定same-root target exact bytes/SHA；terminal status exact；admission exact
  `admitted=true, eligibility=false, release_consumable=false`；
- process-table只做一次owned exact argv scan，residual process exact0。

该audit不是canonical validator或retained audit；它只验证fresh synthetic integration自产生的物理evidence。成功label只能是
`FRESH_M1_SYNTHETIC_INTEGRATION_QUALIFIED_NOT_RETAINED_ELIGIBLE`。

## 6. Evidence handoff、budgets 与 failure branches

本package不改repository code/test，不运行test、compileall或CodeGraph，不stage/commit implementation。无论success/failure，
只向`.agent-work/EXECUTION_RESULT.md`做一次EOF append，然后停Planner门。Append必须冻结：activation/owner identities、
fresh path set、absence gate、seven fixture before/after、spec/bundle/runtime counts、source/process stdout/stderr、output exact-five
identities/payload、owned process scan、ER immutable prefix、first failure和全部zero budgets。

预算exact：outer Python invocation1、synthetic integration1、builder1、runtime1、controller process1、source create1、input
root create7、input artifact write7、output root create1、output artifact write5、controller Git ledger56、ER append1；retry/
fallback0。任何early failure只报告actual <= budget，不补跑未完成项。

以下全部exact0：repository code/test/PLAN/FULL/archive/debug/GUIDE/RESEARCH write by Executer；old source/root read；真实
C1/retained physical read；real B2；actual canonical validator/callback；eligibility emission；retained audit；release
generation/qualification/copy/consumption；network/DNS/environment/credentials；device/camera/Ray/strip/cleanup/capture/
FORMAL/public analyzer/TD-C/sentinel/P8/firmware/deployment。

本包是under-ten-minute pure-offline integration，不需要visible Terminal、Advisor scientific decision或Human危险设备授权。
全绿也不得自行进入M1-R1。

维护性边界：只以一次external synthetic composition验证M1/P5既有owner，不增加生产module、helper、serializer、controller、
validator或parallel evidence owner；失败evidence immutable保留，避免复用和隐藏状态。
