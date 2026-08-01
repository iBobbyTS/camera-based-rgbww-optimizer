# P7 retained-R3 Option B：B3-C1-C1 strict machine-row 自校验、测试与 synthetic replay

**计划状态：** `WAITING_ORCHESTRATOR_ACTIVATION`

**Planner 日期：** `2026-08-01`

**Reference task：** `REF-P7-25-R2-B3-C1-C1`

**Contract：**
`P7-TD-B-RETAINED-R3-OPTION-B-B3-C1-C1-STRICT-MACHINE-ROW-SELF-CHECK-TEST-SYNTHETIC-V1`

**当前唯一动作：** Orchestrator先将B3-C1裁定为execution assertion并创建B3-C1-C1 activation；Executer随后运行exact one pure-offline fresh controller。Controller必须以exact delimiter和strict duplicate-free/non-finite-safe object parser读取committed/current PLAN与FULL，禁止canonical reencode/key-order/whitespace byte-equality gate；随后依次执行真实五件套self-check、focused exact once、full exact once与brand-new synthetic exact once。任何阶段失败立即封存证据并停Planner门。

**唯一 Planner stop：**
`B3_C1_C1_STRICT_MACHINE_ROW_SELF_CHECK_TEST_SYNTHETIC_WAITING_PLANNER_REVIEW`。

**本轮新归档：**
`.agent-work/PLANS/20260801-0428-p7-retained-r3-b3-c1-canonical-gate-review.md`；bytes `4666`，SHA-256 `34f7098b5465e89a5c1f6cbdc36912e6b026c6a8860fd51e22c32df688296b24`；不得覆盖earlier archives。

`PLAN_MACHINE_CONTRACT={"schema":"p7_td_b_retained_r3_option_b_b3_c1_c1_strict_machine_row_self_check_test_synthetic_v1","reference_task_id":"REF-P7-25-R2-B3-C1-C1","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B3-C1-C1-STRICT-MACHINE-ROW-SELF-CHECK-TEST-SYNTHETIC-V1","execution_authorized_after_orchestrator_activation":true,"activation_commit":{"expected_parent":"07d83391c918b20467e310ec72ec3554adda8271","expected_subject":"chore(plan): activate strict machine-row retained verification","expected_changed_paths":[".agent-work/FULL_PLAN_REFERENCE.md",".agent-work/PLAN.md",".agent-work/PLANS/20260801-0428-p7-retained-r3-b3-c1-canonical-gate-review.md"],"clean_porcelain_required_after_activation":true},"rejected_b3_c1":{"activation":"8555f5790b66f2eac7b777cec3d70b4bd2908f8b","evidence_commit":"07d83391c918b20467e310ec72ec3554adda8271","decision":"REJECTED_EXECUTION_ASSERTION_CANONICAL_MACHINE_ROW_REENCODE_NOT_CONTRACTUAL","failure_stage":"activation machine row","failure_message":"not strict canonical JSON","manifest_self_checks":0,"focused_suites":0,"full_suites":0,"synthetic_runs":0,"parent_er":{"bytes":1290261,"sha256":"24afc1b3876bf6988d8de139b81e2b8f094f8939b788d7ac75c9e4a54fb6cc8e"},"physical_eof_suffix":{"bytes":2830,"sha256":"5abd96713ea773704253279e74c4bc7a5991a7f875044e68f13286395a12bfd9"},"evidence_er":{"bytes":1293091,"sha256":"f0bf45501ae31d700eb3d0095d01d881b2a35ae1c17717936b36ec0a95240413"}},"repository_machine_row_contract":{"plan_delimiter":"PLAN_MACHINE_CONTRACT=","full_delimiter":"FULL_PLAN_MACHINE_STATE=","wrapper":"exact_single_backtick_wrapped_line","decode":"strict_utf8","parse":"json_object_duplicate_free_nonfinite_safe","compare":"typed_semantic_fields_only","canonical_reencode":false,"sorted_key_gate":false,"whitespace_normalization":false,"raw_vs_reencoded_byte_equality":false,"json_dumps_for_acceptance":false},"accepted_b2":{"activation":"e939b639f40e3dee3d2199110ea2ae1d5e8108a4","evidence_commit":"3b9e60441062714115d9688e636891d591f3a6ef","decision":"ACCEPTED_COMPLETE_SEALED_SUBORDINATE_PROVENANCE_NOT_RETAINED_ELIGIBLE","result":"FRESH_M1_REAL_INPUT_MANIFEST_SEALED_NOT_RETAINED_ELIGIBLE"},"real_manifest":{"root":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-m1-r1-s2-s1-c1-e939b639f40e-output","root_mode":448,"files":[["execution-result-admission.json",65,"c43d97963373db7d61066de6ebb7e16e6d915281f1f30861f86e1bd6404d87e9"],["retained-r3-audit-provenance-manifest-v2.json",4651,"c3ac3bc712965e39453b32e8cde15ebc7e53dcc7e1a99f1ecb38177f65cadfaf"],["retained-r3-audit-provenance-manifest-v2.sha256.json",148,"3a5f5a4b2c7fa203cad63a90d36a0b43a0e519534cc7c202eeb9b56fcddbfbbc"],["terminal-evidence.json",52,"b438e5c7cac0ef434205c748a003596d740c155f8b0ff3fa06df5a16f4a17893"],["terminal-evidence.sha256.json",123,"d17c4836355406fba95bb2d564692a32ff4b94423ae69e4de8cfe4b542572d75"]],"file_mode":384,"schema":"p7_retained_r3_audit_provenance_manifest_v2","status":"sealed_subordinate_provenance_evidence","immutable":true},"exact_artifact_contract":{"terminal":{"exact_keys":["status"],"status":"sealed_subordinate_provenance_evidence","bytes":52,"sha256":"b438e5c7cac0ef434205c748a003596d740c155f8b0ff3fa06df5a16f4a17893"},"terminal_seal":{"exact_keys":["bytes","sha256","target"],"bytes":52,"sha256":"b438e5c7cac0ef434205c748a003596d740c155f8b0ff3fa06df5a16f4a17893","target":"terminal-evidence.json","artifact_bytes":123,"artifact_sha256":"d17c4836355406fba95bb2d564692a32ff4b94423ae69e4de8cfe4b542572d75"},"admission":{"exact_keys":["admitted","eligibility","release_consumable"],"admitted":true,"eligibility":false,"release_consumable":false,"bytes":65,"sha256":"c43d97963373db7d61066de6ebb7e16e6d915281f1f30861f86e1bd6404d87e9"},"forbidden_invented_artifact_fields":["passed"],"self_check_pass_semantics":"DERIVED_ONLY_FROM_ALL_FROZEN_CHECKS_NOT_AN_ARTIFACT_FIELD"},"source_identity":{"path":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-m1-r1-s2-s1-c1-e939b639f40e-source.py","bytes":26644,"sha256":"0889b150daae9ba6313aea9f6502e09bcf838eb70312a3595c056edb0be1b09b","mode":384},"git_recompute":{"release_checkpoint":"32b9e670ff3bbea0cd1505528c2ca87c2935446c","helper_v1":"9303aa22a9bd37e8ec4f23147c78c6bea84b9a2e","integration":"3e2ebed132b6d4338bfa324bfc42c3565d2eeb3c","m1_commit":"0f4c09e1b2b2afbf627f6f36d57a1a65847ab4a8","m1_parent":"f2b38c530a6cbac5c29d761036eb3cd2a159f3b9","m1_subject":"fix(p7): align real manifest Git ledgers","m1_paths":["src/camera_based_rgbww_optimizer/utils/p7_retained_r3_real_manifest_domain_template.py","tests/test_p7_retained_r3_real_manifest_domain_template.py"],"m1_patch_bytes":5874,"m1_patch_sha256":"6b26e49359f944bceafe5129b0b81a3d5600d400eae7d3b739c2baba12d6a5ca","seam_paths":["src/camera_based_rgbww_optimizer/optimization/p7_retained_release_audit.py","tests/test_p7_retained_release_audit.py"],"governance_manifest_path":"config/hsi/p7-governance-lineage-successor-v1.json","governance_manifest_sha256":"69bbbb369e776e1aa11a227ecf3432de44bc517c7eb25828094f4820df45042e","guide_path":"advisor/4/4.GUIDE.md","guide_sha256":"659152f6c0ae69c90c701de4e57c352d771e4f0bf75cf9410271ba0a94200e35","advisor_decision_path":"advisor/4/0.AUDIT/07-guide4-to-retained-r3-lineage-owner-decision.md","advisor_decision_sha256":"842cfad090549ebf6379df4551bd4f051267e4bf93014f899c5e329c57085620","advisor_attachment_path":"/Users/ibobby/.codex/attachments/cba7928d-712a-441e-a708-4301ee32bd66/pasted-text.txt","advisor_attachment_sha256":"91a88e5467e13c811794c2149b6a8d5669e613c3e259d8f4091ba08c048733d6"},"input_roots":{"c1":{"path":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b2-c1-path-owner-27aacbf-20260730T1547Z","mode":448,"files":[["path-owner-index.json",12195,"b189117fdd0a9a65ca80660245ec84b7f2f533c3e496c96e76eb48a4666feb35"],["path-owner-index.sha256.json",682,"867d1ffad5bd29f24dc81b24a58ce66393dd688833d3a4516fe7f45ef50875e9"],["terminal-evidence.json",13455,"c21a691272ca7466271349daa5b10236c9f36dfeb481d592e9c368a87e7a4763"],["terminal-evidence.sha256.json",772,"4bfebf4ad40e8c2e65ad2470faaed184f21d39eda73c13e689b09769d280752f"]]},"retained":{"path":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-lineage-release-r3/lineage-release-32b9e67-r2-20260727T2227/child-output/lineage-release-r3","mode":448,"files":[["current-lineage-candidate.json",9819,"3a2ff5a2af200c55c925b954488c5c5dd31a35a481440d17dfcdd8b68419f2e0"],["resolved-formal-plan.json",15137,"cf7c78b6a6cfda4055d05f5e9bbe9914161213b380dc7736ee09e257dd45eb6b"],["setup-lineage-release.json",1567,"0bacf1878a97fcdc4436259e132e89f6e56611df6d7fb5d5a7da28f62c98ad3e"]]}},"focused_test_modules":["tests.test_p7_retained_release_audit","tests.test_p7_retained_r3_provenance_io","tests.test_p7_retained_r3_controller_conformance","tests.test_p7_retained_r3_controller_preparation","tests.test_p7_retained_r3_exact_five_controller","tests.test_p7_retained_r3_controller_domain_template","tests.test_p7_retained_r3_controller_runtime","tests.test_p7_retained_r3_controller_integration","tests.test_p7_retained_r3_real_manifest_domain_template"],"full_test_command":[".venv/bin/python","-m","unittest","discover","-s","tests","-v"],"fresh_synthetic":{"base_dir":"/Volumes/4T/temp/rgbww-optimizer","root_prefix":"p7-td-b-retained-r3-option-b-b3-c1-c1-<activation_short12>-synthetic","root_mode":448,"file_mode":384,"synthetic_input_files":7,"output_artifacts":5,"controller_processes":1,"replay_reads":5,"retry":0,"fallback":0,"consumable":false,"terminal_exact_keys":["status"],"terminal_status":"sealed_subordinate_provenance_evidence","admission_exact_keys":["admitted","eligibility","release_consumable"],"admission_values":[true,false,false],"forbidden_invented_artifact_fields":["passed"]},"success_contract":{"manifest_self_check":"PASS_DERIVED_FROM_FROZEN_CHECKS","focused_exit":0,"full_exit":0,"synthetic_exit":0,"synthetic_lifecycle_check":"PASS_DERIVED_FROM_FROZEN_CHECKS","synthetic_replay_check":"PASS_DERIVED_FROM_FROZEN_CHECKS","real_retained_audit_performed":false,"canonical_eligibility_validator_called":false,"eligibility":false,"release_consumable":false,"success_label":"B3_C1_C1_STRICT_MACHINE_ROW_SELF_CHECK_TEST_SYNTHETIC_PASS_NOT_RETAINED_ELIGIBLE"},"execution_budgets":{"outer_controller_invocations":1,"repository_file_decodes":2,"repository_machine_row_extractions":2,"real_manifest_root_reads":1,"real_manifest_file_reads":5,"real_source_reads":1,"c1_root_reads":1,"c1_file_reads":4,"retained_root_identity_reads":1,"retained_physical_file_reads":3,"git_read_invocations_max":24,"governance_file_reads":4,"manifest_self_checks":1,"focused_suites":1,"full_suites":1,"synthetic_runs":1,"synthetic_controller_processes":1,"synthetic_input_writes":7,"synthetic_output_writes":5,"synthetic_replay_reads":5,"process_table_scans":1,"apply_patch_invocations":1,"execution_result_appends":1,"postappend_operations":0,"retry":0,"fallback":0},"zero_budgets":{"repository_code_writes":0,"repository_test_writes":0,"plan_writes_by_executer":0,"full_writes_by_executer":0,"archive_writes_by_executer":0,"debug_writes":0,"guide_writes":0,"research_writes":0,"real_manifest_writes":0,"real_source_writes":0,"c1_input_writes":0,"retained_artifact_writes":0,"retained_schema_validation":0,"retained_scientific_validation":0,"old_b3_evidence_reads":0,"canonical_machine_row_reencode_checks":0,"canonical_machine_row_key_order_checks":0,"canonical_machine_row_byte_equality_checks":0,"inferred_terminal_passed_field_checks":0,"actual_canonical_lineage_validator_calls":0,"canonical_validator_callbacks":0,"retained_release_audit":0,"eligibility_emissions":0,"release_generation":0,"release_qualification":0,"release_copy":0,"release_consumption":0,"network":0,"dns":0,"environment":0,"credentials":0,"device":0,"camera":0,"ray":0,"strip":0,"cleanup":0,"capture":0,"formal":0,"public_analyzer":0,"td_c":0,"sentinel":0,"p8":0,"firmware":0,"deployment":0,"implementation_commits":0},"required_full_machine_state":{"active_task_count":1,"active_task":"REF-P7-25-R2-B3-C1-C1","active_plan_contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B3-C1-C1-STRICT-MACHINE-ROW-SELF-CHECK-TEST-SYNTHETIC-V1","retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","manifest_authority":"SUBORDINATE_EVIDENCE_ONLY_CANONICAL_VALIDATOR_SOLE_ELIGIBILITY_OWNER","m1_real_input_manifest_status":"ACCEPTED_COMPLETE_SEALED_SUBORDINATE_PROVENANCE_NOT_RETAINED_ELIGIBLE","b3_status":"REJECTED_EXECUTION_ASSERTION_TERMINAL_PASSED_FIELD_NOT_CONTRACTUAL","b3_c1_status":"REJECTED_EXECUTION_ASSERTION_CANONICAL_MACHINE_ROW_REENCODE_NOT_CONTRACTUAL","b3_c1_c1_status":"ACTIVE_STRICT_MACHINE_ROW_SELF_CHECK_TEST_SYNTHETIC","executer_dispatched":true,"device_authorized_by_this_file":false},"authorization":{"classification":"PURE_OFFLINE_POSTCOMMIT_VERIFICATION_WITH_READ_ONLY_RETAINED_IDENTITIES_AND_FRESH_SYNTHETIC_EVIDENCE","human_device_authorization_required":false,"advisor_scientific_decision_required":false},"expected_duration":"under_10_minutes","visible_terminal_required":false,"archive":{"path":".agent-work/PLANS/20260801-0428-p7-retained-r3-b3-c1-canonical-gate-review.md","bytes":4666,"sha256":"34f7098b5465e89a5c1f6cbdc36912e6b026c6a8860fd51e22c32df688296b24"},"planner_stop":"B3_C1_C1_STRICT_MACHINE_ROW_SELF_CHECK_TEST_SYNTHETIC_WAITING_PLANNER_REVIEW"}`

## 1. Activation 与 repository machine-row parser

Orchestrator必须先将B3-C1标为
`REJECTED_EXECUTION_ASSERTION_CANONICAL_MACHINE_ROW_REENCODE_NOT_CONTRACTUAL`，将B3-C1-C1设为唯一active task并按machine row创建activation。Activation后porcelain必须clean。

Executer在任何external或test access前完整读取activation committed/current PLAN与FULL各一次并要求对应文件byte-identical。每个文件只允许：

1. strict UTF-8 decode；
2. 定位exact one单行、反引号包裹的`PLAN_MACHINE_CONTRACT=`或`FULL_PLAN_MACHINE_STATE=` delimiter；
3. duplicate-free、non-finite-safe JSON object parse；
4. 对parsed typed values核对PLAN contract和required FULL subset。

这里的“strict”只描述decode、唯一delimiter、object type、duplicate keys与non-finite numbers。它**不**要求machine-row原始JSON是sorted-key、compact、canonical encoding。严禁`json.dumps`/其他reencode参与acceptance，严禁sort-key gate、whitespace normalization、raw-vs-reencoded byte equality或任何canonical key-order比较。这三类actual必须为`0`。不得使用regex、generic/fallback scanner。

只允许读取machine row冻结的accepted B2 source、output root/five exact files、C1 four、retained three及Git/governance paths。真实inputs不得list父目录、glob、search、copy、normalize、repair、rewrite、delete或relocate。

## 2. Exact terminal/seal/admission self-check

使用exact one外置、一次性、纯读controller完成self-check，不新增repository owner：

1. 验证B2 source、output root与五文件的exact path/mode/bytes/SHA；五文件以strict UTF-8、duplicate-free/non-finite-safe JSON object parse，不要求canonical reencode或key order。
2. `terminal-evidence.json`只核对exact key set `status`及冻结status/bytes/SHA。
3. `terminal-evidence.sha256.json`只核对exact key set `bytes/sha256/target`，真实绑定terminal，并核对seal自身身份。
4. `execution-result-admission.json`只核对exact key set `admitted/eligibility/release_consumable`及`true/false/false`和冻结身份。
5. Manifest只核对冻结schema/status、physical identities及Git/provenance bindings。重算M1 commit/parent/subject/exact paths、before/after blobs、file SHA、authoritative exact-two-path patch、两条seam ledger与四个governance file SHA。Generic path allowlist不能作为证明。
6. C1 four与retained three各读exact once，只重算physical root/file identity、bytes/SHA。C1不重审semantic/linkage；retained只作为opaque bytes，不做schema/science/audit/callback/eligibility。

严禁要求、搜索、扫描或推导artifact中的`passed`字段。Self-check PASS只能是以上冻结检查全部完成后的内存派生outcome。Self-check失败则focused/full/synthetic均为`0`，写terminal handoff并停Planner门。

## 3. Focused 与 durable full exact once

仅self-check pass后运行focused exact once：

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

Focused nonzero立即stop，full/synthetic保持`0`。Focused pass后运行machine row冻结full discovery exact once并持久化command、exit、tests/failures/errors与stdout/stderr bytes/SHA。Full nonzero立即stop，synthetic保持`0`。Retry、rerun、selector-only补跑、parallel shard和filter fallback均为`0`。

Tests只允许既有temp/fake/synthetic fixtures；禁止把真实retained root传给audit/validator callback。若启动前有证据显示总时长超过10分钟，不启动并回Planner/Orchestrator调整owner。

## 4. Brand-new synthetic exact once 与 replay

仅full pass后，以activation short12派生machine row冻结的brand-new synthetic root；exact non-following absence gate失败即停，不换path。一次outer controller创建0700 root与七个0600 strict JSON synthetic inputs，调用accepted M1 builder exact once与P5 runtime exact once，启动exact one process并产出exact five 0600 artifacts。

Synthetic核对terminal exact key/status、terminal seal exact key与真实绑定、admission exact key及`true/false/false`、manifest exact schema/status、synthetic/nonconsumable identities、lifecycle order、Git ledger family与owned residual0。严禁invented `passed`字段。随后五件套各exact one replay read，独立strict decode、seal/hash与typed facts复算。失败保留partial fresh root，不cleanup、不retry、不换path。

成功label只能是
`B3_C1_C1_STRICT_MACHINE_ROW_SELF_CHECK_TEST_SYNTHETIC_PASS_NOT_RETAINED_ELIGIBLE`。

## 5. Evidence lifecycle、locks 与 stop

所有Git、external、test、process与audit操作必须在ER append前结束。先在内存冻结完整payload：activation、machine-row parser facts、exact artifact contract、self-check派生outcome、Git ledgers、real identities、test commands/results/log hashes、synthetic identities/derived outcomes、budget/actual、first failure、zero locks、retained status与唯一Planner stop。

唯一repository write为exact one physical-EOF `apply_patch`向`EXECUTION_RESULT.md`追加heading及single strict JSON block；append是最后side effect，之后read/status/hash/probe或second append均为`0`。本包没有implementation commit。

真实canonical lineage validator、真实retained release audit、callback、eligibility emission、release generation/qualification/copy/consumption全部为`0`。Network/DNS/`.env`/credentials、device/camera/Ray/strip/cleanup/capture/FORMAL/public analyzer/TD-C/sentinel/P8/firmware/deployment全部为`0`。

B3-C1-C1 pass只证明postcommit implementation/tests与synthetic lifecycle合格，可解锁未来B4 Planner package；retained仍为`RETAINED_UNVALIDATED_UNCONSUMED`。Pass或fail都立即停唯一Planner门。

维护性判断：本包复用P3 physical/Git owner、M1 deterministic domain owner、P5 runtime owner和既有测试入口；只修正一次性controller的machine-row验收语义，不改production schema、不新增eligibility owner或执行框架。
