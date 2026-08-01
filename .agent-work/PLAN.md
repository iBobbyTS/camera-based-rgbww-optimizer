# P7 retained-R3 Option B：B3-C3 fresh postcommit verification

**计划状态：** `WAITING_ORCHESTRATOR_ACTIVATION`

**Planner 日期：** `2026-08-01`

**Reference task：** `REF-P7-25-R2-B3-C3`

**Contract：**
`P7-TD-B-RETAINED-R3-OPTION-B-B3-C3-FRESH-POSTCOMMIT-SELF-CHECK-TEST-SYNTHETIC-V1`

**当前唯一动作：** Orchestrator按machine contract创建exact activation；Executer随后运行exact one pure-offline
controller，严格依次完成accepted real manifest/Git identity self-check、focused exact once、durable full exact once及
brand-new synthetic terminal/replay exact once。任何失败立即停止后续阶段、保留已有证据并回到唯一Planner门。

**唯一 Planner stop：**
`B3_C3_FRESH_POSTCOMMIT_SELF_CHECK_TEST_SYNTHETIC_WAITING_PLANNER_REVIEW`。

**本轮新归档：**
`.agent-work/PLANS/20260801-0528-p7-retained-r3-b3-c3-postcommit-verification-selection.md`；
bytes `5366`，SHA-256 `7ea80f19281ecda0310573b4afd33b0b0349e1d3637d93efc50e439899a6b49b`；
不得覆盖earlier archives。

`PLAN_MACHINE_CONTRACT={"schema":"p7_td_b_retained_r3_option_b_b3_c3_fresh_postcommit_self_check_test_synthetic_v1","reference_task_id":"REF-P7-25-R2-B3-C3","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B3-C3-FRESH-POSTCOMMIT-SELF-CHECK-TEST-SYNTHETIC-V1","execution_authorized_after_orchestrator_activation":true,"activation_commit":{"expected_parent":"1f121b16502d869ed31d6b6cccc0a79d3dbdd737","expected_subject":"chore(plan): activate fresh postcommit verification","expected_changed_paths":[".agent-work/FULL_PLAN_REFERENCE.md",".agent-work/PLAN.md",".agent-work/PLANS/20260801-0528-p7-retained-r3-b3-c3-postcommit-verification-selection.md"],"clean_porcelain_required_after_activation":true},"repository_machine_row_contract":{"plan_delimiter":"PLAN_MACHINE_CONTRACT=","full_delimiter":"FULL_PLAN_MACHINE_STATE=","wrapper":"exact_single_backtick_wrapped_line","decode":"strict_utf8","parse":"json_object_duplicate_free_nonfinite_safe","compare":"typed_semantic_fields_only","canonical_reencode":false,"sorted_key_gate":false,"whitespace_normalization":false,"raw_vs_reencoded_byte_equality":false,"json_dumps_for_acceptance":false},"accepted_b2":{"activation":"e939b639f40e3dee3d2199110ea2ae1d5e8108a4","evidence_commit":"3b9e60441062714115d9688e636891d591f3a6ef","decision":"ACCEPTED_COMPLETE_SEALED_SUBORDINATE_PROVENANCE_NOT_RETAINED_ELIGIBLE","result":"FRESH_M1_REAL_INPUT_MANIFEST_SEALED_NOT_RETAINED_ELIGIBLE"},"accepted_implementation":{"commit":"e84f5b6adc7c004b388074f5e81a4d109a6541f2","parent":"8e5d4ea520fd5aa5edb41af7b574188b47596bc3","subject":"fix(p7): correct manifest governance identity","changed_paths":[".agent-work/EXECUTION_RESULT.md","src/camera_based_rgbww_optimizer/utils/p7_retained_r3_real_manifest_domain_template.py","tests/test_p7_retained_r3_real_manifest_domain_template.py"],"source_git_blob_sha256":"da8b24b9530d387befde8eda3f0ee0dcfca373e28f27a6bda3433c4f4bf5f410","test_git_blob_sha256":"193464af34c10809b91987f984a4b7ce40f924df66a472511acbd6fb5142b378","exact_two_path_binary_diff_sha256":"2685d00525d90f725ed3c73ca7adeebcf9bb5ade14c39dc4172d725fa9d741c0","serialized_baseline_length":12,"canonical_template_sha256":"a83804d299c747c485dda86eecd3bcb576a90bb2be3c2ae03fe77951ed404ad6","golden_replacement_sha256":"55c43ad338a83c11a2b2c8d2c5714a9efaf75ec4215dd30e103d540b0c6502ec","implementation_accepted":true,"original_execution_accepted":false,"budget_distinction_evidence_commit":"798e459761946f48f69d8c87c48dfaee6961becd"},"real_manifest":{"root":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-m1-r1-s2-s1-c1-e939b639f40e-output","root_mode":448,"file_mode":384,"files":[["execution-result-admission.json",65,"c43d97963373db7d61066de6ebb7e16e6d915281f1f30861f86e1bd6404d87e9"],["retained-r3-audit-provenance-manifest-v2.json",4651,"c3ac3bc712965e39453b32e8cde15ebc7e53dcc7e1a99f1ecb38177f65cadfaf"],["retained-r3-audit-provenance-manifest-v2.sha256.json",148,"3a5f5a4b2c7fa203cad63a90d36a0b43a0e519534cc7c202eeb9b56fcddbfbbc"],["terminal-evidence.json",52,"b438e5c7cac0ef434205c748a003596d740c155f8b0ff3fa06df5a16f4a17893"],["terminal-evidence.sha256.json",123,"d17c4836355406fba95bb2d564692a32ff4b94423ae69e4de8cfe4b542572d75"]],"schema":"p7_retained_r3_audit_provenance_manifest_v2","status":"sealed_subordinate_provenance_evidence","immutable":true},"exact_artifact_contract":{"manifest_seal":{"exact_keys":["bytes","sha256","target"],"bytes":4651,"sha256":"c3ac3bc712965e39453b32e8cde15ebc7e53dcc7e1a99f1ecb38177f65cadfaf","target":"retained-r3-audit-provenance-manifest-v2.json","artifact_bytes":148,"artifact_sha256":"3a5f5a4b2c7fa203cad63a90d36a0b43a0e519534cc7c202eeb9b56fcddbfbbc"},"terminal":{"exact_keys":["status"],"status":"sealed_subordinate_provenance_evidence","bytes":52,"sha256":"b438e5c7cac0ef434205c748a003596d740c155f8b0ff3fa06df5a16f4a17893"},"terminal_seal":{"exact_keys":["bytes","sha256","target"],"bytes":52,"sha256":"b438e5c7cac0ef434205c748a003596d740c155f8b0ff3fa06df5a16f4a17893","target":"terminal-evidence.json","artifact_bytes":123,"artifact_sha256":"d17c4836355406fba95bb2d564692a32ff4b94423ae69e4de8cfe4b542572d75"},"admission":{"exact_keys":["admitted","eligibility","release_consumable"],"admitted":true,"eligibility":false,"release_consumable":false,"bytes":65,"sha256":"c43d97963373db7d61066de6ebb7e16e6d915281f1f30861f86e1bd6404d87e9"},"forbidden_invented_artifact_fields":["passed"],"package_pass_semantics":"DERIVED_ONLY_FROM_ALL_FROZEN_CHECKS_NOT_AN_ARTIFACT_FIELD"},"source_identity":{"path":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-m1-r1-s2-s1-c1-e939b639f40e-source.py","bytes":26644,"sha256":"0889b150daae9ba6313aea9f6502e09bcf838eb70312a3595c056edb0be1b09b","mode":384},"manifest_git_recompute":{"release_checkpoint":"32b9e670ff3bbea0cd1505528c2ca87c2935446c","helper_v1":"9303aa22a9bd37e8ec4f23147c78c6bea84b9a2e","integration":"3e2ebed132b6d4338bfa324bfc42c3565d2eeb3c","m1_commit":"0f4c09e1b2b2afbf627f6f36d57a1a65847ab4a8","m1_parent":"f2b38c530a6cbac5c29d761036eb3cd2a159f3b9","m1_subject":"fix(p7): align real manifest Git ledgers","m1_paths":["src/camera_based_rgbww_optimizer/utils/p7_retained_r3_real_manifest_domain_template.py","tests/test_p7_retained_r3_real_manifest_domain_template.py"],"m1_patch_bytes":5874,"m1_patch_sha256":"6b26e49359f944bceafe5129b0b81a3d5600d400eae7d3b739c2baba12d6a5ca","required_recomputed_fields":["full_child_commit","full_parent_commit","tree","subject","exact_path_set","before_blob_oids","after_blob_oids","before_file_sha256","after_file_sha256","canonical_patch_sha256","seam_before_after_blobs","seam_file_sha256","seam_patch_sha256"],"trust_manifest_without_recompute":false,"generic_path_allowlist_permitted":false},"governance_identities":{"governance_manifest":["config/hsi/p7-governance-lineage-successor-v1.json","69bbbb369e776e1aa11a227ecf3432de44bc517c7eb25828094f4820df45042e"],"guide":["advisor/4/4.GUIDE.md","659152f6c0ae69c90c701de4e57c352d771e4f0bf75cf9410271ba0a94200e35"],"baseline_position_8":{"owner":"external_lineage_owner_decision_evidence","path":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-release-lineage-owner-o3-c1r3/20260728T0121/lineage-owner-decision-evidence.json","bytes":7066,"sha256":"842cfad090549ebf6379df4551bd4f051267e4bf93014f899c5e329c57085620"},"baseline_position_9":{"owner":"advisor_option_b_attachment","path":"/Users/ibobby/.codex/attachments/cba7928d-712a-441e-a708-4301ee32bd66/pasted-text.txt","bytes":11146,"sha256":"91a88e5467e13c811794c2149b6a8d5669e613c3e259d8f4091ba08c048733d6"},"advisor_request_git_document":{"path":"advisor/4/0.AUDIT/07-guide4-to-retained-r3-lineage-owner-decision.md","sha256":"5b23cbdfe97ac71e7438f1d30461455938828029c0ba32e931a9570e0ea88a34","serialized_baseline_member":false,"reads":0}},"input_roots":{"c1":{"path":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b2-c1-path-owner-27aacbf-20260730T1547Z","mode":448,"files":[["path-owner-index.json",12195,"b189117fdd0a9a65ca80660245ec84b7f2f533c3e496c96e76eb48a4666feb35"],["path-owner-index.sha256.json",682,"867d1ffad5bd29f24dc81b24a58ce66393dd688833d3a4516fe7f45ef50875e9"],["terminal-evidence.json",13455,"c21a691272ca7466271349daa5b10236c9f36dfeb481d592e9c368a87e7a4763"],["terminal-evidence.sha256.json",772,"4bfebf4ad40e8c2e65ad2470faaed184f21d39eda73c13e689b09769d280752f"]]},"retained":{"path":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-lineage-release-r3/lineage-release-32b9e67-r2-20260727T2227/child-output/lineage-release-r3","mode":448,"files":[["current-lineage-candidate.json",9819,"3a2ff5a2af200c55c925b954488c5c5dd31a35a481440d17dfcdd8b68419f2e0"],["resolved-formal-plan.json",15137,"cf7c78b6a6cfda4055d05f5e9bbe9914161213b380dc7736ee09e257dd45eb6b"],["setup-lineage-release.json",1567,"0bacf1878a97fcdc4436259e132e89f6e56611df6d7fb5d5a7da28f62c98ad3e"]],"interpretation":"OPAQUE_PHYSICAL_IDENTITY_ONLY"}},"focused_test_modules":["tests.test_p7_retained_release_audit","tests.test_p7_retained_r3_provenance_io","tests.test_p7_retained_r3_controller_conformance","tests.test_p7_retained_r3_controller_preparation","tests.test_p7_retained_r3_exact_five_controller","tests.test_p7_retained_r3_controller_domain_template","tests.test_p7_retained_r3_controller_runtime","tests.test_p7_retained_r3_controller_integration","tests.test_p7_retained_r3_real_manifest_domain_template"],"focused_expected_tests":83,"full_test_command":[".venv/bin/python","-m","unittest","discover","-s","tests","-v"],"full_expected_tests":800,"fresh_synthetic":{"base_dir":"/Volumes/4T/temp/rgbww-optimizer","root_prefix":"p7-td-b-retained-r3-option-b-b3-c3-<activation_short12>-synthetic","root_mode":448,"file_mode":384,"absence_checks":1,"synthetic_input_files":7,"output_artifacts":5,"builder_calls":1,"runtime_calls":1,"controller_processes":1,"replay_reads":5,"retry":0,"fallback":0,"consumable":false,"terminal_exact_keys":["status"],"terminal_status":"sealed_subordinate_provenance_evidence","admission_exact_keys":["admitted","eligibility","release_consumable"],"admission_values":[true,false,false],"forbidden_invented_artifact_fields":["passed"]},"real_input_read_budgets":{"real_manifest_root_reads":1,"real_manifest_file_reads":5,"real_source_reads":1,"c1_root_reads":1,"c1_file_reads":4,"retained_root_identity_reads":1,"retained_physical_file_reads":3,"governance_manifest_reads":1,"guide_reads":1,"external_lineage_owner_decision_evidence_reads":1,"advisor_option_b_attachment_reads":1,"advisor_request_git_document_reads":0,"parent_directory_lists":0,"globs":0,"searches":0,"symlink_follows":0,"real_input_writes":0},"execution_budgets":{"outer_controller_invocations":1,"repository_file_decodes":2,"repository_machine_row_extractions":2,"git_read_invocations_max":36,"manifest_self_checks":1,"focused_suites":1,"full_suites":1,"synthetic_runs":1,"synthetic_controller_processes":1,"synthetic_input_writes":7,"synthetic_output_writes":5,"synthetic_replay_reads":5,"process_table_scans":1,"execution_result_tail_reads":1,"apply_patch_invocations":1,"execution_result_appends":1,"postappend_operations":0,"retry":0,"fallback":0},"success_contract":{"manifest_self_check":"PASS_DERIVED_FROM_FROZEN_CHECKS","focused_exit":0,"focused_tests":83,"full_exit":0,"full_tests":800,"synthetic_exit":0,"synthetic_lifecycle_check":"PASS_DERIVED_FROM_FROZEN_CHECKS","synthetic_replay_check":"PASS_DERIVED_FROM_FROZEN_CHECKS","real_retained_audit_performed":false,"canonical_eligibility_validator_called":false,"eligibility_emitted":false,"release_consumable":false,"success_label":"B3_C3_FRESH_POSTCOMMIT_SELF_CHECK_TEST_SYNTHETIC_PASS_NOT_RETAINED_ELIGIBLE"},"required_full_machine_state":{"active_task_count":1,"active_task":"REF-P7-25-R2-B3-C3","active_plan_contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B3-C3-FRESH-POSTCOMMIT-SELF-CHECK-TEST-SYNTHETIC-V1","retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","manifest_authority":"SUBORDINATE_EVIDENCE_ONLY_CANONICAL_VALIDATOR_SOLE_ELIGIBILITY_OWNER","b3_c2_s1_status":"ACCEPTED_COMPLETE_EXECUTION_BUDGET_DISTINCTION_SEALED","b3_c3_status":"ACTIVE_FRESH_POSTCOMMIT_SELF_CHECK_TEST_SYNTHETIC","executer_dispatched":true,"device_authorized_by_this_file":false},"orchestrator_commit_after_handoff":{"owner":"ORCHESTRATOR","executer_must_not_commit":true,"expected_subject":"chore(evidence): record B3-C3 postcommit verification","expected_changed_paths":[".agent-work/EXECUTION_RESULT.md"]},"zero_budgets":{"repository_code_direct_reads":0,"repository_test_direct_reads":0,"repository_code_writes":0,"repository_test_writes":0,"plan_writes_by_executer":0,"full_writes_by_executer":0,"archive_writes_by_executer":0,"debug_writes":0,"advisor_request_git_document_reads":0,"guide_writes":0,"research_writes":0,"real_manifest_writes":0,"real_source_writes":0,"c1_input_writes":0,"retained_artifact_writes":0,"retained_schema_validation":0,"retained_scientific_validation":0,"old_b2_manifest_repair":0,"old_b2_manifest_regeneration":0,"old_b3_evidence_reads":0,"canonical_machine_row_reencode_checks":0,"canonical_machine_row_key_order_checks":0,"canonical_machine_row_byte_equality_checks":0,"inferred_terminal_passed_field_checks":0,"codegraph_queries":0,"codegraph_sync":0,"actual_canonical_lineage_validator_calls":0,"canonical_validator_callbacks":0,"retained_release_audit":0,"eligibility_emissions":0,"release_generation":0,"release_qualification":0,"release_copy":0,"release_consumption":0,"network":0,"dns":0,"environment":0,"credentials":0,"device":0,"camera":0,"ray":0,"strip":0,"cleanup":0,"capture":0,"formal":0,"public_analyzer":0,"td_c":0,"sentinel":0,"p8":0,"firmware":0,"deployment":0,"implementation_commits_by_executer":0},"authorization":{"classification":"PURE_OFFLINE_POSTCOMMIT_VERIFICATION_WITH_READ_ONLY_REAL_IDENTITIES_AND_FRESH_SYNTHETIC_EVIDENCE","human_device_authorization_required":false,"advisor_scientific_decision_required":false},"expected_duration":"under_10_minutes","visible_terminal_required":false,"archive":{"path":".agent-work/PLANS/20260801-0528-p7-retained-r3-b3-c3-postcommit-verification-selection.md","bytes":5366,"sha256":"7ea80f19281ecda0310573b4afd33b0b0349e1d3637d93efc50e439899a6b49b"},"planner_stop":"B3_C3_FRESH_POSTCOMMIT_SELF_CHECK_TEST_SYNTHETIC_WAITING_PLANNER_REVIEW"}`

## 1. Activation 与 repository contract

Activation必须是`1f121b16502d869ed31d6b6cccc0a79d3dbdd737`的direct child，subject及FULL、PLAN、新archive
exact three-path set以machine row为准，activation后porcelain clean。Executer在任何external/test access前完整读取
activation committed/current PLAN与FULL各一次并要求byte-identical。

Machine row只允许strict UTF-8、exact one反引号包裹delimiter、duplicate-free/non-finite-safe JSON object parse和typed
semantic compare。严禁canonical reencode、sorted-key、whitespace normalization、raw-vs-reencoded equality或
`json.dumps` acceptance gate；不得使用regex、generic或fallback scanner。

## 2. Real manifest 与 Git identity self-check

使用exact one外置、一次性、纯读controller，不新增repository owner：

1. 按exact path non-following读取B2 source、output root/five files、C1 four及retained three，核对mode、bytes、SHA；
   禁止list父目录、glob、search、copy、repair、rewrite、regenerate、delete或relocate。
2. Strict解析五件套。Manifest schema/status、manifest seal、terminal、terminal seal和admission必须符合machine row的
   exact key/value/target/bytes/SHA。不得要求、扫描、推导artifact顶层`passed`；package pass只能是全部冻结checks完成后
   的内存派生结论。
3. 从Git对象独立重算manifest绑定的child/parent/tree/subject/exact path set、before/after blob OID、before/after文件
   SHA、canonical patch SHA及两条seam ledger；同时核对release checkpoint、helper v1、integration和governance identities。
   不能只信manifest，也不能用generic path allowlist替代exact path set。
4. 单独重算accepted implementation `e84f5b6...`的parent/subject/exact three paths、source/test Git blob SHA与exact
   two-path diff，并证明activation tree中的source/test blobs与accepted implementation相同；working-tree source/test direct
   reads保持0。
5. Baseline position 8只能绑定external lineage-owner decision evidence；position 9只能绑定Advisor Option-B attachment。
   Advisor request Git document不属于serialized baseline且本包读取0次。
6. C1仅做四文件physical identity；retained仅做三文件opaque physical identity，不做schema、science、audit、callback或
   eligibility判断。Pre/post real-input identities必须相等。

任一mismatch立即进入BR-SELF-CHECK，focused/full/synthetic均为0；真实输入写入始终为0。

## 3. Focused 与 durable full exact once

仅self-check派生PASS后执行focused exact once：

```text
.venv/bin/python -m unittest -v
  tests.test_p7_retained_release_audit
  tests.test_p7_retained_r3_provenance_io
  tests.test_p7_retained_r3_controller_conformance
  tests.test_p7_retained_r3_controller_preparation
  tests.test_p7_retained_r3_exact_five_controller
  tests.test_p7_retained_r3_controller_domain_template
  tests.test_p7_retained_r3_controller_runtime
  tests.test_p7_retained_r3_controller_integration
  tests.test_p7_retained_r3_real_manifest_domain_template
```

要求exit 0、tests 83、failures/errors 0；否则进入BR-FOCUSED且full/synthetic为0。Focused pass后运行
`.venv/bin/python -m unittest discover -s tests -v` exact once，要求exit 0、tests 800、failures/errors 0；否则进入
BR-FULL且synthetic为0。两次均记录command、exit、tests/failures/errors、stdout/stderr bytes/SHA。Retry、rerun、
selector-only补跑、parallel shard、filter fallback均为0。Tests只能使用既有fake/synthetic fixtures，禁止把真实retained
root传入validator/audit callback。

既有full约3分钟，预计总时长低于10分钟，无需visible Terminal。若启动前出现可信证据表明会超过10分钟，不启动任何test，
封存BR-DURATION并回Planner/Orchestrator调整执行owner。

## 4. Brand-new synthetic terminal/replay exact once

仅full pass后使用activation short12派生的exact fresh root。先做一次non-following absence gate；present/symlink/error进入
BR-SYNTHETIC-ROOT且controller process为0，不得换path。随后一次controller创建0700 root与七个0600 synthetic inputs，
调用accepted M1 builder exact1、P5 runtime exact1、controller process exact1，并产出exact five 0600 artifacts。

Synthetic必须核对manifest schema/status及seal、terminal exact key/status及seal、admission exact keys与
`true/false/false`、synthetic/nonconsumable identities、lifecycle order、Git ledger family与owned residual0；禁止invented
`passed`字段。再对五件套各exact one replay read，独立strict parse、hash/seal和typed facts复算。失败进入
BR-SYNTHETIC并保留partial fresh root，不cleanup、不retry、不换path。成功label只能是
`B3_C3_FRESH_POSTCOMMIT_SELF_CHECK_TEST_SYNTHETIC_PASS_NOT_RETAINED_ELIGIBLE`。

## 5. Failure preservation、terminal seal 与 handoff

顺序固定为self-check→focused1→full1→synthetic1；任何BR都冻结first failure、completed-stage actuals、未执行阶段0及
全部zero locks。所有Git/external/test/process操作必须在ER append前完成。先在内存冻结activation、machine parser、
real identities、manifest/Git recompute、test结果、synthetic terminal/replay、budget/actual、first failure、retained state和
唯一Planner stop。

唯一repository write为exact one `apply_patch`，使用current ER physical EOF的exact final anchor追加heading与single strict
canonical JSON terminal block。该append必须是最后side effect；之后read/status/hash/probe/test/commit/second append均为0。
Executer不得commit；Orchestrator收到handoff后只可按machine row的ER-only subject/path commit。

B3-C3 pass只关闭postcommit/self-check/test/synthetic工程门。Canonical lineage validator、真实retained audit、eligibility
emission、release generation/qualification/copy/consumption及全部network/device/scientific路径保持0；retained仍为
`RETAINED_UNVALIDATED_UNCONSUMED`。Pass或fail均立即停Planner门，B4仍须另一个future PLAN。

本包无需Advisor科学决策或Human设备授权。

维护性判断：本包复用P3 physical/Git、M1 deterministic domain、P5 runtime及既有测试owner；一次性controller不进入
production，不新增serializer、generic allowlist、validator或平行provenance framework。
