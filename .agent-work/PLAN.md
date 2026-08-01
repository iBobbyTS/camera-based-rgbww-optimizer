# P7 retained-R3 Option B：R3 typed real self-check owner implementation

**计划状态：** `WAITING_ORCHESTRATOR_ACTIVATION`

**Planner 日期：** `2026-08-01`

**Reference task：** `REF-P7-25-R2-B3-C3-C4-R3`

**Contract：** `P7-TD-B-RETAINED-R3-OPTION-B-B3-C3-C4-R3-TYPED-REAL-SELF-CHECK-OWNER-V1`

**当前唯一动作：** 新增一个repo-owned typed real-manifest self-check owner及其dedicated tests；只用synthetic typed fixtures验证in-memory contract，不读取或执行任何retained real artifact。

**唯一 Planner stop：** `B3_C3_C4_R3_TYPED_REAL_SELF_CHECK_OWNER_WAITING_PLANNER_REVIEW`。

**本轮新归档：** `.agent-work/PLANS/20260801-0853-p7-retained-r3-b3-c3-c4-r2-c1-real-owner-gap-review.md`；bytes `3777`，SHA-256 `c8f66fd96f7d4e4b722d1fee71724f20110643697489bd2c6a3c02d42eb8ae24`。

`PLAN_MACHINE_CONTRACT={"schema":"p7_td_b_retained_r3_option_b_b3_c3_c4_r3_typed_real_self_check_owner_v1","reference_task_id":"REF-P7-25-R2-B3-C3-C4-R3","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B3-C3-C4-R3-TYPED-REAL-SELF-CHECK-OWNER-V1","reviewed_r2_c1":{"activation":"3e26adc176b25c81810039751ab4061e768fc873","evidence":"329e501645bdeb58aae43087d09fb094ebbd2be2","decision":"REJECTED_PRE_EFFECT_REAL_SELF_CHECK_OWNER_AND_DURABLE_OUTPUT_CONTRACT_INCOMPLETE","all_effect_classes_zero":true,"b3_credit":false},"activation_commit":{"expected_parent":"329e501645bdeb58aae43087d09fb094ebbd2be2","expected_subject":"chore(plan): activate typed real self-check owner","expected_changed_paths":[".agent-work/FULL_PLAN_REFERENCE.md",".agent-work/PLAN.md",".agent-work/PLANS/20260801-0853-p7-retained-r3-b3-c3-c4-r2-c1-real-owner-gap-review.md"],"clean_porcelain_required_after_activation":true},"exact_changed_paths":["src/camera_based_rgbww_optimizer/utils/p7_retained_r3_real_manifest_self_check.py","tests/test_p7_retained_r3_real_manifest_self_check.py"],"public_api":["RealManifestSelfCheckError","RealManifestGitFileBytes","RealManifestSelfCheckSpec","RealManifestSelfCheckReport","required_real_manifest_git_argv","run_real_manifest_self_check"],"required_reuse":["p7_retained_r3_provenance_io.FileIdentity","p7_retained_r3_provenance_io.GitLedger","p7_retained_r3_provenance_io.canonical_json_bytes","p7_retained_r3_provenance_io.decode_canonical_json","p7_retained_r3_provenance_io.run_read_only_git","p7_retained_r3_real_manifest_domain_template.RealManifestGitPathIdentity","p7_retained_r3_real_manifest_domain_template.RealManifestCommitIdentity","p7_retained_r3_real_manifest_domain_template.RealManifestInputIdentity","p7_retained_r3_real_manifest_domain_template.RealManifestBaselineIdentity"],"test_contract":{"targeted":{"module":"tests.test_p7_retained_r3_real_manifest_self_check","expected_tests":12,"invocations":1},"focused":{"modules":["tests.test_p7_retained_r3_provenance_io","tests.test_p7_retained_r3_real_manifest_domain_template","tests.test_p7_retained_r3_real_manifest_self_check"],"expected_tests":53,"invocations":1},"full":{"command":[".venv/bin/python","-m","unittest","discover","-s","tests","-v"],"expected_tests":822,"invocations":1},"postcommit_targeted":{"expected_tests":12,"invocations":1}},"implementation_commit":{"expected_parent_activation":true,"expected_subject":"feat(p7): own real manifest self-check","expected_changed_paths":["src/camera_based_rgbww_optimizer/utils/p7_retained_r3_real_manifest_self_check.py","tests/test_p7_retained_r3_real_manifest_self_check.py"]},"execution_budgets":{"codegraph_pre_queries":1,"source_writes":1,"test_writes":1,"targeted_suites":1,"focused_suites":1,"full_suites":1,"compileall":1,"codegraph_sync":1,"codegraph_post_queries":1,"implementation_commits":1,"postcommit_targeted_suites":1,"process_table_scans":1,"execution_result_tail_reads":1,"execution_result_apply_patch_appends":1,"execution_result_appends":1,"postappend_operations":0,"retry":0,"fallback":0},"zero_budgets":{"old_one_off_contract_reads":0,"real_artifact_reads":0,"retained_artifact_reads":0,"c1_artifact_reads":0,"external_root_reads":0,"external_root_writes":0,"durable_log_writes":0,"filesystem_owner_additions":0,"process_runner_additions":0,"validator_additions":0,"validator_calls":0,"eligibility_emissions":0,"release_consumption":0,"network":0,"device":0,"camera":0,"ray":0,"strip":0,"formal":0,"public_analyzer":0,"plan_writes_by_executer":0,"full_writes_by_executer":0,"archive_writes_by_executer":0},"required_full_machine_state":{"active_task_count":1,"active_task":"REF-P7-25-R2-B3-C3-C4-R3","active_plan_contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B3-C3-C4-R3-TYPED-REAL-SELF-CHECK-OWNER-V1","retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","manifest_authority":"SUBORDINATE_EVIDENCE_ONLY_CANONICAL_VALIDATOR_SOLE_ELIGIBILITY_OWNER","real_self_check_owner_status":"ACTIVE_IMPLEMENTATION","real_execution_status":"BLOCKED_ON_R3_ACCEPTANCE","synthetic_remainder_status":"BLOCKED","executer_dispatched":true,"device_authorized_by_this_file":false},"orchestrator_commit_after_handoff":{"owner":"ORCHESTRATOR","executer_must_not_commit":true,"expected_subject":"chore(evidence): record typed real self-check owner","expected_changed_paths":[".agent-work/EXECUTION_RESULT.md"]},"authorization":{"classification":"PURE_OFFLINE_ENABLING_REFACTOR","human_device_authorization_required":false,"advisor_scientific_decision_required":false},"expected_duration":"under_10_minutes","visible_terminal_required":false,"archive":{"path":".agent-work/PLANS/20260801-0853-p7-retained-r3-b3-c3-c4-r2-c1-real-owner-gap-review.md","bytes":3777,"sha256":"c8f66fd96f7d4e4b722d1fee71724f20110643697489bd2c6a3c02d42eb8ae24"},"planner_stop":"B3_C3_C4_R3_TYPED_REAL_SELF_CHECK_OWNER_WAITING_PLANNER_REVIEW"}`

## 1. Exact two-path owner

只新增：

- `src/camera_based_rgbww_optimizer/utils/p7_retained_r3_real_manifest_self_check.py`
- `tests/test_p7_retained_r3_real_manifest_self_check.py`

不得修改P3/P5/P6/P7/M1、validator、runner、docs、skill或plan files。实现前CodeGraph确认上述新路径仍不存在并核对复用API；不得读取`23ab2d8`或旧one-off controller sections。

Owner API冻结为machine row中的六个export。所有dataclass必须`frozen=True`，error暴露stable `code`。`RealManifestGitFileBytes`只携带`commit/repo_path/data`，owner用bytes严格重算SHA-256及Git blob OID并与typed seam identity及Git ledger绑定。`RealManifestSelfCheckSpec`只接收：reference/contract、absolute repo root、五个按role排序的P3 `FileIdentity`、typed activation/baseline/C1 four/retained three，以及exact Git file bytes。不得接收generic selector、path allowlist、chat constants或untyped mapping contract。

## 2. Single semantic ownership

Owner内部唯一冻结五个basename/role和exact JSON key/path/type：

1. manifest：exact keys `schema/status/activation/baseline/c1/retained`；schema/status exact；其余值与typed spec逐字段、逐位置一致；
2. manifest seal：exact keys `bytes/sha256/target`并绑定manifest `FileIdentity`；
3. terminal：exact key `status`与exact success status；
4. terminal seal：exact keys `bytes/sha256/target`并绑定terminal identity；
5. admission：exact keys `admitted/eligibility/release_consumable`，类型严格bool，值exact `true/false/false`。

五个artifact须mode `0600`、distinct path、同一root identity、basename exact、canonical JSON exact re-encode。未知/缺失/重复key、bool/int混淆、noncanonical bytes、root/path/size/hash drift均stable fail closed。

`required_real_manifest_git_argv(spec)`是ordered Git command的唯一owner：只由typed activation/baseline/seam fields生成P3 allowlisted argv，覆盖commit verify、commit metadata、changed-path set、before/after blob OID、activation full binary patch及两个seam path的binary patch；paths必须exact sorted unique。`run_real_manifest_self_check`必须逐条调用注入或默认的P3 `run_read_only_git`，验证`GitLedger.argv/cwd/exit/stderr/stdout`与expected facts；任何少、余、乱序或mismatch fail closed。不得新增subprocess wrapper或第二Git authority。

成功只返回`RealManifestSelfCheckReport`及由`canonical_json_bytes`生成的canonical report bytes/SHA。Report schema/status、artifact facts、typed manifest facts、ordered argv/result digests、blob/file/patch recompute facts全部确定性；明确`eligibility=false`、`release_consumable=false`、`authority=subordinate_self_check_only`。Owner不创建root、不读写文件、不persist full log、不调用validator，也不决定retained eligibility。

## 3. Dedicated regression contract

Dedicated exact12覆盖：golden success及determinism；exports/frozen types；五role/path/type map；canonical/duplicate/unknown/type drift；seal/terminal/admission mismatch；root/mode/path/hash drift；Git argv exact order；Git exit/stderr/stdout/argv/cwd mismatch；blob bytes SHA/Git OID与seam mismatch；generic mapping/extra ledger拒绝；所有negative cases验证first error code且后续Git calls为0。

验证顺序：targeted12 → focused53（P3 28 + M1 13 + new 12）→ full822（baseline810 + new12）→ compileall exact two source paths → CodeGraph sync/post-query → exact commit → postcommit targeted12。任一步失败立即停，后续0，retry/fallback0。

## 4. Handoff与locks

Terminal前process scan1且不kill/cleanup。只在physical EOF用一次`apply_patch`追加ER，记录activation/implementation topology、exact two-path blob/file/patch identities、API、test counts、CodeGraph、all zero budgets与下一建议；append后operations0。Executer不得改PLAN/FULL/archive或提交evidence。

R3接受后才可规划独立real execution package；后者分别运行owner、focused83、durable full810，并由launcher拥有durable output path/mode/write/seal/terminal identity。R3本身不给B3、validator、eligibility、release或synthetic credit。

维护性判断：以单一typed owner替换不断扩写的one-off sections；复用P3/M1边界，I/O、durable persistence与eligibility仍由原owner分别负责，exact two-path与12个行为测试限制复杂度。
