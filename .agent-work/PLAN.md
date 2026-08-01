# P7 retained-R3 Option B：B3 postcommit 自校验、测试与 synthetic replay

**计划状态：** `WAITING_ORCHESTRATOR_ACTIVATION`

**Planner 日期：** `2026-08-01`

**Reference task：** `REF-P7-25-R2-B3`

**Contract：**
`P7-TD-B-RETAINED-R3-OPTION-B-B3-POSTCOMMIT-SELF-CHECK-TEST-SYNTHETIC-V1`

**当前唯一动作：** Orchestrator先把S2-S1-C1接受为sealed subordinate provenance并创建B3 activation；Executer随后只运行一次pure-offline B3 controller，严格顺序完成真实B2 manifest独立自校验、postcommit focused suite、durable full suite与一个brand-new synthetic terminal/replay。任何阶段失败立即封存证据并停；不得调用真实canonical lineage validator、不得执行retained audit或emit eligibility。

**唯一 Planner stop：**
`B3_POSTCOMMIT_SELF_CHECK_TEST_SYNTHETIC_WAITING_PLANNER_REVIEW`。

**本轮新归档：**
`.agent-work/PLANS/20260801-0402-p7-retained-r3-b2-m1-r1-s2-s1-c1-sealed-manifest-review.md`；bytes `5882`，SHA-256 `f67cdaa95bc6294dbf1f8127d14b92e7fab5e1f41fcd377c8c037e7f8a489ebc`；不得覆盖earlier archives。

`PLAN_MACHINE_CONTRACT={"schema":"p7_td_b_retained_r3_option_b_b3_postcommit_self_check_test_synthetic_v1","reference_task_id":"REF-P7-25-R2-B3","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B3-POSTCOMMIT-SELF-CHECK-TEST-SYNTHETIC-V1","execution_authorized_after_orchestrator_activation":true,"activation_commit":{"expected_parent":"3b9e60441062714115d9688e636891d591f3a6ef","expected_subject":"chore(plan): activate retained manifest postcommit verification","expected_changed_paths":[".agent-work/FULL_PLAN_REFERENCE.md",".agent-work/PLAN.md",".agent-work/PLANS/20260801-0402-p7-retained-r3-b2-m1-r1-s2-s1-c1-sealed-manifest-review.md"],"clean_porcelain_required_after_activation":true},"accepted_b2":{"activation":"e939b639f40e3dee3d2199110ea2ae1d5e8108a4","evidence_commit":"3b9e60441062714115d9688e636891d591f3a6ef","decision":"ACCEPTED_COMPLETE_SEALED_SUBORDINATE_PROVENANCE_NOT_RETAINED_ELIGIBLE","result":"FRESH_M1_REAL_INPUT_MANIFEST_SEALED_NOT_RETAINED_ELIGIBLE","parent_er":{"bytes":1266264,"sha256":"ddd34c672984309c954d19e5028327ce936f7f0182283121000a22cbb8d3763a"},"physical_eof_suffix":{"bytes":21212,"sha256":"ea998ba6c72aecf9e1038fe02412e35d41e12250501770867936af68532053ba"},"evidence_er":{"bytes":1287476,"sha256":"42057a760eabee310927b438f62ae2b8d84975c75c74bfa8bcf5e9b71eff069a"},"all_success_budgets_match":true,"pre_post_input_identities_equal":true,"terminal_passed":true,"admitted":true,"eligibility":false,"release_consumable":false},"real_manifest":{"root":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-m1-r1-s2-s1-c1-e939b639f40e-output","root_mode":448,"files":[["execution-result-admission.json",65,"c43d97963373db7d61066de6ebb7e16e6d915281f1f30861f86e1bd6404d87e9"],["retained-r3-audit-provenance-manifest-v2.json",4651,"c3ac3bc712965e39453b32e8cde15ebc7e53dcc7e1a99f1ecb38177f65cadfaf"],["retained-r3-audit-provenance-manifest-v2.sha256.json",148,"3a5f5a4b2c7fa203cad63a90d36a0b43a0e519534cc7c202eeb9b56fcddbfbbc"],["terminal-evidence.json",52,"b438e5c7cac0ef434205c748a003596d740c155f8b0ff3fa06df5a16f4a17893"],["terminal-evidence.sha256.json",123,"d17c4836355406fba95bb2d564692a32ff4b94423ae69e4de8cfe4b542572d75"]],"file_mode":384,"schema":"p7_retained_r3_audit_provenance_manifest_v2","status":"sealed_subordinate_provenance_evidence","immutable":true},"source_identity":{"path":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-m1-r1-s2-s1-c1-e939b639f40e-source.py","bytes":26644,"sha256":"0889b150daae9ba6313aea9f6502e09bcf838eb70312a3595c056edb0be1b09b","mode":384},"git_recompute":{"release_checkpoint":"32b9e670ff3bbea0cd1505528c2ca87c2935446c","helper_v1":"9303aa22a9bd37e8ec4f23147c78c6bea84b9a2e","integration":"3e2ebed132b6d4338bfa324bfc42c3565d2eeb3c","m1_commit":"0f4c09e1b2b2afbf627f6f36d57a1a65847ab4a8","m1_parent":"f2b38c530a6cbac5c29d761036eb3cd2a159f3b9","m1_subject":"fix(p7): align real manifest Git ledgers","m1_paths":["src/camera_based_rgbww_optimizer/utils/p7_retained_r3_real_manifest_domain_template.py","tests/test_p7_retained_r3_real_manifest_domain_template.py"],"m1_patch_bytes":5874,"m1_patch_sha256":"6b26e49359f944bceafe5129b0b81a3d5600d400eae7d3b739c2baba12d6a5ca","seam_paths":["src/camera_based_rgbww_optimizer/optimization/p7_retained_release_audit.py","tests/test_p7_retained_release_audit.py"],"governance_manifest_path":"config/hsi/p7-governance-lineage-successor-v1.json","governance_manifest_sha256":"69bbbb369e776e1aa11a227ecf3432de44bc517c7eb25828094f4820df45042e","guide_path":"advisor/4/4.GUIDE.md","guide_sha256":"659152f6c0ae69c90c701de4e57c352d771e4f0bf75cf9410271ba0a94200e35","advisor_decision_path":"advisor/4/0.AUDIT/07-guide4-to-retained-r3-lineage-owner-decision.md","advisor_decision_sha256":"842cfad090549ebf6379df4551bd4f051267e4bf93014f899c5e329c57085620","advisor_attachment_path":"/Users/ibobby/.codex/attachments/cba7928d-712a-441e-a708-4301ee32bd66/pasted-text.txt","advisor_attachment_sha256":"91a88e5467e13c811794c2149b6a8d5669e613c3e259d8f4091ba08c048733d6"},"input_roots":{"c1":{"path":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b2-c1-path-owner-27aacbf-20260730T1547Z","mode":448,"files":[["path-owner-index.json",12195,"b189117fdd0a9a65ca80660245ec84b7f2f533c3e496c96e76eb48a4666feb35"],["path-owner-index.sha256.json",682,"867d1ffad5bd29f24dc81b24a58ce66393dd688833d3a4516fe7f45ef50875e9"],["terminal-evidence.json",13455,"c21a691272ca7466271349daa5b10236c9f36dfeb481d592e9c368a87e7a4763"],["terminal-evidence.sha256.json",772,"4bfebf4ad40e8c2e65ad2470faaed184f21d39eda73c13e689b09769d280752f"]]},"retained":{"path":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-lineage-release-r3/lineage-release-32b9e67-r2-20260727T2227/child-output/lineage-release-r3","mode":448,"files":[["current-lineage-candidate.json",9819,"3a2ff5a2af200c55c925b954488c5c5dd31a35a481440d17dfcdd8b68419f2e0"],["resolved-formal-plan.json",15137,"cf7c78b6a6cfda4055d05f5e9bbe9914161213b380dc7736ee09e257dd45eb6b"],["setup-lineage-release.json",1567,"0bacf1878a97fcdc4436259e132e89f6e56611df6d7fb5d5a7da28f62c98ad3e"]]}},"focused_test_modules":["tests.test_p7_retained_release_audit","tests.test_p7_retained_r3_provenance_io","tests.test_p7_retained_r3_controller_conformance","tests.test_p7_retained_r3_controller_preparation","tests.test_p7_retained_r3_exact_five_controller","tests.test_p7_retained_r3_controller_domain_template","tests.test_p7_retained_r3_controller_runtime","tests.test_p7_retained_r3_controller_integration","tests.test_p7_retained_r3_real_manifest_domain_template"],"full_test_command":[".venv/bin/python","-m","unittest","discover","-s","tests","-v"],"fresh_synthetic":{"base_dir":"/Volumes/4T/temp/rgbww-optimizer","root_prefix":"p7-td-b-retained-r3-option-b-b3-<activation_short12>-synthetic","root_mode":448,"file_mode":384,"synthetic_input_files":7,"output_artifacts":5,"controller_processes":1,"replay_reads":5,"retry":0,"fallback":0,"consumable":false},"success_contract":{"manifest_self_check":"PASS","focused_exit":0,"full_exit":0,"synthetic_exit":0,"synthetic_terminal_passed":true,"synthetic_replay_passed":true,"real_retained_audit_performed":false,"canonical_eligibility_validator_called":false,"eligibility":false,"release_consumable":false,"success_label":"B3_POSTCOMMIT_SELF_CHECK_TEST_SYNTHETIC_PASS_NOT_RETAINED_ELIGIBLE"},"execution_budgets":{"outer_controller_invocations":1,"repository_file_decodes":2,"repository_machine_row_extractions":2,"real_manifest_root_reads":1,"real_manifest_file_reads":5,"real_source_reads":1,"c1_root_reads":1,"c1_file_reads":4,"retained_root_identity_reads":1,"retained_physical_file_reads":3,"git_read_invocations_max":24,"governance_file_reads":4,"manifest_self_checks":1,"focused_suites":1,"full_suites":1,"synthetic_runs":1,"synthetic_controller_processes":1,"synthetic_input_writes":7,"synthetic_output_writes":5,"synthetic_replay_reads":5,"process_table_scans":1,"apply_patch_invocations":1,"execution_result_appends":1,"postappend_operations":0,"retry":0,"fallback":0},"zero_budgets":{"repository_code_writes":0,"repository_test_writes":0,"plan_writes_by_executer":0,"full_writes_by_executer":0,"archive_writes_by_executer":0,"debug_writes":0,"guide_writes":0,"research_writes":0,"real_manifest_writes":0,"real_source_writes":0,"c1_input_writes":0,"retained_artifact_writes":0,"retained_schema_validation":0,"retained_scientific_validation":0,"actual_canonical_lineage_validator_calls":0,"canonical_validator_callbacks":0,"retained_release_audit":0,"eligibility_emissions":0,"release_generation":0,"release_qualification":0,"release_copy":0,"release_consumption":0,"network":0,"dns":0,"environment":0,"credentials":0,"device":0,"camera":0,"ray":0,"strip":0,"cleanup":0,"capture":0,"formal":0,"public_analyzer":0,"td_c":0,"sentinel":0,"p8":0,"firmware":0,"deployment":0,"implementation_commits":0},"required_full_machine_state":{"active_task_count":1,"active_task":"REF-P7-25-R2-B3","active_plan_contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B3-POSTCOMMIT-SELF-CHECK-TEST-SYNTHETIC-V1","retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","manifest_authority":"SUBORDINATE_EVIDENCE_ONLY_CANONICAL_VALIDATOR_SOLE_ELIGIBILITY_OWNER","m1_real_input_manifest_status":"ACCEPTED_COMPLETE_SEALED_SUBORDINATE_PROVENANCE_NOT_RETAINED_ELIGIBLE","b3_status":"ACTIVE_POSTCOMMIT_SELF_CHECK_TEST_SYNTHETIC","executer_dispatched":true,"device_authorized_by_this_file":false},"authorization":{"classification":"PURE_OFFLINE_POSTCOMMIT_VERIFICATION_WITH_READ_ONLY_RETAINED_IDENTITIES_AND_FRESH_SYNTHETIC_EVIDENCE","human_device_authorization_required":false,"advisor_scientific_decision_required":false},"expected_duration":"under_10_minutes","visible_terminal_required":false,"archive":{"path":".agent-work/PLANS/20260801-0402-p7-retained-r3-b2-m1-r1-s2-s1-c1-sealed-manifest-review.md","bytes":5882,"sha256":"f67cdaa95bc6294dbf1f8127d14b92e7fab5e1f41fcd377c8c037e7f8a489ebc"},"planner_stop":"B3_POSTCOMMIT_SELF_CHECK_TEST_SYNTHETIC_WAITING_PLANNER_REVIEW"}`

## 1. Activation 与 immutable inputs

Orchestrator必须先把S2-S1-C1标为
`ACCEPTED_COMPLETE_SEALED_SUBORDINATE_PROVENANCE_NOT_RETAINED_ELIGIBLE`，将B3设为唯一active task，并创建activation。Expected parent、subject与exact three changed paths以machine row为准；activation后porcelain必须clean。

Executer在任何external或test access前完整读取activation committed/current PLAN与FULL各一次并要求byte-identical；以strict UTF-8、exact backtick-wrapped machine row、duplicate-free/non-finite-safe JSON object parse取得合同并核对required FULL subset。不得使用regex/generic/fallback scanner或canonical key-order gate。

真实B2 source、output root/five artifacts、C1 four与retained three均为immutable input。只允许按machine row exact paths non-following读取；不得list父目录、glob、search、copy、normalize、repair、rewrite、delete或relocate。每个成功read立即记录root/file完整identity与bytes/SHA；失败立即停止后续阶段。

## 2. Independent subordinate-manifest self-check

使用一个外置、一次性、纯读controller完成self-check，不新增repository owner：

1. 验证B2 source及output root/five exact files的路径、mode、bytes、SHA；五文件strict duplicate-free canonical JSON，两个seal分别重算target bytes/SHA，terminal/status/admission exact，admission只能是`true/false/false`。
2. 从Git重新计算manifest绑定的M1 commit/parent/subject/exact paths、before/after blob、文件SHA与authoritative exact-two-path patch；重新确认release checkpoint、helper v1及integration full SHA存在且关系与manifest冻结值一致。
3. 对两条seam path分别从manifest指定的before/after Git对象重新计算blob OID、bytes/SHA与per-path patch SHA；重算exact governance manifest、GUIDE、Advisor decision record和attachment SHA。不得把任何generic path allowlist当作证明。
4. 读取C1 four和retained three各一次，只重算physical root/file identity、bytes与SHA并与manifest行逐项相等。C1不做semantic/linkage重审；retained三件套只作为opaque physical bytes，不做schema、science、audit、candidate/release callback或eligibility判断。
5. Manifest schema/status必须exact；不得信任manifest自身声称的eligibility，不得把self-check命名或解释为canonical lineage validation。

Self-check失败则focused/full/synthetic保持0，写terminal evidence后停Planner门。真实manifest/source/input不得产生任何write。

## 3. Postcommit focused 与 durable full

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

测试只能使用其既有temp/fake/synthetic fixtures；禁止把真实retained root传入任何audit/validator callback。Focused nonzero立即stop，full/synthetic0。

Focused pass后运行machine row冻结的full discovery exact once，持久化command、exit、tests/failures/errors及stdout/stderr bytes/SHA。Full nonzero立即stop，synthetic0。Retry、rerun、selector-only补跑、parallel shard与test filter fallback均为0。预计full沿用既有约3分钟，因此无需visible Terminal；若启动前有证据显示总时长会超过10分钟，必须不启动并回Planner/Orchestrator调整执行owner。

## 4. Fresh synthetic terminal/replay

仅full pass后，以activation short12派生machine row的brand-new synthetic root；对exact root做一次non-following absence gate，present/symlink/error均fail closed。一次outer controller创建0700 root与七个0600 strict canonical synthetic input files，构造与真实B2相同结构但明确标记synthetic/nonconsumable的C1 four与retained three identities，调用accepted M1 builder exact1与P5 runtime exact1，启动exact one controller process并产出exact five 0600 artifacts。

Synthetic terminal必须证明schema/status、seal、lifecycle order、Git ledger family、admission `true/false/false`、owned residual0。随后对五件套各exact one replay read，独立strict decode、seal/hash与typed facts复算，证明replay deterministic。不得使用任何旧synthetic root/evidence，不得读取真实B2 source/output以外的旧failure namespace，不得把synthetic pass解释成retained eligibility。

Synthetic任一失败保留partial fresh root，不cleanup、不retry、不换path。成功label只能是
`B3_POSTCOMMIT_SELF_CHECK_TEST_SYNTHETIC_PASS_NOT_RETAINED_ELIGIBLE`。

## 5. Evidence lifecycle、locks 与 stop

所有Git、external、test、process与audit操作必须在ER append前结束。先在内存冻结完整payload：activation、self-check facts、Git ledgers、real input identities、test commands/results/log hashes、synthetic root/input/output/terminal/replay identities、budget/actual、first failure、zero locks、retained status与唯一Planner stop。唯一repository write为exact one physical-EOF `apply_patch`向`EXECUTION_RESULT.md`追加一个heading及single strict canonical JSON block；append是最后side effect，之后任何read/status/hash/probe或second append均为0。

本包没有implementation commit。真实canonical lineage validator、真实retained release audit、callback、eligibility emission、release generation/qualification/copy/consumption均为0。Network/DNS/`.env`/credentials、device/camera/Ray/strip/cleanup/capture/FORMAL/public analyzer/TD-C/sentinel/P8/firmware/deployment均为0。Unit tests中的isolated fake/synthetic call coverage不能对真实retained input执行，也不能被计作真实validator/audit。

B3 pass只证明postcommit implementation/tests与synthetic lifecycle合格，并解锁未来B4 Planner package；retained state仍为`RETAINED_UNVALIDATED_UNCONSUMED`。B4首次真实audit、canonical validator唯一eligibility判定、release与设备阶段全部锁定。Pass或fail都立即停Planner门。

维护性判断：B3复用既有P3 physical/Git owner、M1 deterministic domain owner、P5 runtime owner及现有测试入口；一次性self-check controller只编排已冻结事实，不进入生产代码，不新增eligibility owner或并行执行框架。
