# P7 retained-R3 Option B：B3-C1-C1-S1 Git/ER-only terminal supersession

**计划状态：** `WAITING_ORCHESTRATOR_ACTIVATION`

**Planner 日期：** `2026-08-01`

**Reference task：** `REF-P7-25-R2-B3-C1-C1-S1`

**Contract：**
`P7-TD-B-RETAINED-R3-OPTION-B-B3-C1-C1-S1-GIT-ER-ONLY-TERMINAL-SUPERSESSION-V1`

**当前唯一动作：** Orchestrator先记录B3-C1-C1 rejected状态并创建activation；Executer随后只读
committed Git objects，独立冻结B3-C1-C1的governance owner misbinding、non-EOF insertion与未授权
CodeGraph计数，最后在current `EXECUTION_RESULT.md`真实physical EOF追加exact one canonical supersession
block。成功或失败均必须append，且append为最后side effect。

**唯一 Planner stop：**
`B3_C1_C1_S1_GIT_ER_ONLY_TERMINAL_SUPERSESSION_WAITING_PLANNER_REVIEW`。

**本轮新归档：**
`.agent-work/PLANS/20260801-0444-p7-retained-r3-b3-c1-c1-governance-eof-review.md`；
bytes `5674`，SHA-256 `ad399ac02d7b6992358d7c42bcf6974125a90c6f8752749f0bb080f5bdadcebc`；不得覆盖earlier archives。

`PLAN_MACHINE_CONTRACT={"schema":"p7_td_b_retained_r3_option_b_b3_c1_c1_s1_git_er_only_terminal_supersession_v1","reference_task_id":"REF-P7-25-R2-B3-C1-C1-S1","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B3-C1-C1-S1-GIT-ER-ONLY-TERMINAL-SUPERSESSION-V1","execution_authorized_after_orchestrator_activation":true,"activation_commit":{"expected_parent":"4877fd30ea2821e71fc7497321e24a886302d93c","expected_subject":"chore(plan): activate B3 governance EOF supersession","expected_changed_paths":[".agent-work/FULL_PLAN_REFERENCE.md",".agent-work/PLAN.md",".agent-work/PLANS/20260801-0444-p7-retained-r3-b3-c1-c1-governance-eof-review.md"],"clean_porcelain_required_after_activation":true},"reviewed_b3_c1_c1":{"activation":"a9de513b94b2e6871914960c238333a979de4ecf","evidence_commit":"4877fd30ea2821e71fc7497321e24a886302d93c","decision":"REJECTED_NON_EOF_HANDOFF_UNAUTHORIZED_CODEGRAPH_AND_GOVERNANCE_IDENTITY_MISBINDING","evidence_changed_paths":[".agent-work/EXECUTION_RESULT.md"],"parent_er":{"bytes":1293091,"sha256":"f0bf45501ae31d700eb3d0095d01d881b2a35ae1c17717936b36ec0a95240413"},"insert":{"offset":2579,"bytes":8523,"sha256":"3bf15b37db7711bfeb343fbd0a89b394a9db8fc82aab06fab4dbd464d64d9412"},"preserved_old_suffix":{"bytes":1290512,"sha256":"926777941aa912f6bc08a2a32e13b65e34fc8d05fc6d675757259c7239a25d1d"},"evidence_er":{"bytes":1301614,"sha256":"6c2ccf6170aca4e1b51b1192b1be93ab0a43457063ac3675be5afb052c64128c"},"reported_physical_eof":true,"actual_physical_eof":false,"reported_append_last":true,"actual_insert_before_preserved_suffix":true,"codegraph_queries_before_controller":3,"focused_suites":0,"full_suites":0,"synthetic_runs":0},"governance_owner_correction":{"advisor_request_git_path":"advisor/4/0.AUDIT/07-guide4-to-retained-r3-lineage-owner-decision.md","advisor_request_bytes":6754,"advisor_request_sha256":"5b23cbdfe97ac71e7438f1d30461455938828029c0ba32e931a9570e0ea88a34","lineage_owner_decision_evidence_path":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-release-lineage-owner-o3-c1r3/20260728T0121/lineage-owner-decision-evidence.json","lineage_owner_decision_evidence_bytes":7066,"lineage_owner_decision_evidence_sha256":"842cfad090549ebf6379df4551bd4f051267e4bf93014f899c5e329c57085620","lineage_owner_decision_evidence_status":"advisor_decision_required","lineage_owner_decision_evidence_accepted":false,"advisor_option_b_attachment_path":"/Users/ibobby/.codex/attachments/cba7928d-712a-441e-a708-4301ee32bd66/pasted-text.txt","advisor_option_b_attachment_bytes":11146,"advisor_option_b_attachment_sha256":"91a88e5467e13c811794c2149b6a8d5669e613c3e259d8f4091ba08c048733d6","governance_manifest_sha256":"69bbbb369e776e1aa11a227ecf3432de44bc517c7eb25828094f4820df45042e","guide_sha256":"659152f6c0ae69c90c701de4e57c352d771e4f0bf75cf9410271ba0a94200e35","b2_manifest_baseline_positions":{"6":"governance_manifest_sha256","7":"guide_sha256","8":"lineage_owner_decision_evidence_sha256","9":"advisor_option_b_attachment_sha256","10":"human_governance_override","11":"helper_disposition"},"old_payload_repair":false,"old_payload_regeneration":false,"future_required_branch":"BOUNDED_PRODUCTION_AND_DEDICATED_TEST_GOVERNANCE_IDENTITY_CORRECTION"},"execution_budgets":{"git_read_invocations_max":18,"execution_result_committed_reads":2,"execution_result_appends":1,"apply_patch_invocations":1,"postappend_operations":0,"retry":0,"fallback":0},"zero_budgets":{"repository_code_reads":0,"repository_test_reads":0,"repository_code_writes":0,"repository_test_writes":0,"plan_writes_by_executer":0,"full_writes_by_executer":0,"archive_writes_by_executer":0,"debug_writes":0,"guide_reads":0,"guide_writes":0,"research_writes":0,"advisor_file_reads":0,"advisor_file_writes":0,"external_governance_evidence_reads":0,"advisor_attachment_reads":0,"real_manifest_reads":0,"real_manifest_writes":0,"real_source_reads":0,"c1_input_reads":0,"retained_artifact_reads":0,"retained_artifact_writes":0,"codegraph_queries":0,"codegraph_sync":0,"tests":0,"controller_invocations":0,"synthetic_runs":0,"actual_canonical_lineage_validator_calls":0,"canonical_validator_callbacks":0,"retained_release_audit":0,"eligibility_emissions":0,"release_generation":0,"release_qualification":0,"release_copy":0,"release_consumption":0,"network":0,"dns":0,"environment":0,"credentials":0,"device":0,"camera":0,"ray":0,"strip":0,"cleanup":0,"capture":0,"formal":0,"public_analyzer":0,"td_c":0,"sentinel":0,"p8":0,"firmware":0,"deployment":0,"implementation_commits":0},"required_full_machine_state":{"active_task_count":1,"active_task":"REF-P7-25-R2-B3-C1-C1-S1","active_plan_contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B3-C1-C1-S1-GIT-ER-ONLY-TERMINAL-SUPERSESSION-V1","retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","manifest_authority":"SUBORDINATE_EVIDENCE_ONLY_CANONICAL_VALIDATOR_SOLE_ELIGIBILITY_OWNER","b3_c1_c1_status":"REJECTED_NON_EOF_HANDOFF_UNAUTHORIZED_CODEGRAPH_AND_GOVERNANCE_IDENTITY_MISBINDING","b3_c1_c1_s1_status":"ACTIVE_GIT_ER_ONLY_TERMINAL_SUPERSESSION","executer_dispatched":true,"device_authorized_by_this_file":false},"authorization":{"classification":"PURE_OFFLINE_COMMITTED_GIT_AND_ER_ONLY_TERMINAL_SUPERSESSION","human_device_authorization_required":false,"advisor_scientific_decision_required":false},"expected_duration":"under_10_minutes","visible_terminal_required":false,"archive":{"path":".agent-work/PLANS/20260801-0444-p7-retained-r3-b3-c1-c1-governance-eof-review.md","bytes":5674,"sha256":"ad399ac02d7b6992358d7c42bcf6974125a90c6f8752749f0bb080f5bdadcebc"},"planner_stop":"B3_C1_C1_S1_GIT_ER_ONLY_TERMINAL_SUPERSESSION_WAITING_PLANNER_REVIEW"}`

## 1. Activation 与唯一数据源

Activation后porcelain必须clean。Executer只能通过read-only Git命令读取：

1. activation commit/parent/subject/exact changed paths；
2. evidence commit `4877fd...`及parent `a9de513...`；
3. `a9de513...:.agent-work/EXECUTION_RESULT.md`与
   `4877fd...:.agent-work/EXECUTION_RESULT.md` exact bytes；
4. activation committed/current PLAN与FULL的machine row typed subset。

不得读取working-tree production/test/Advisor/GUIDE、任何external governance evidence、B2 real
manifest/source、C1或retained artifact。Archive identity由activation committed PLAN冻结；不得把旧
Advisor request或external payload重新解释为可修改输入。

## 2. 必须独立重算的supersession事实

Executer必须以committed ER bytes计算longest common prefix/suffix并确认：

- parent ER `1293091` bytes / `f0bf4550...`；
- evidence ER `1301614` bytes / `6c2ccf61...`；
- insert offset `2579`，insert `8523` bytes / `3bf15b37...`；
- preserved parent suffix `1290512` bytes / `92677794...`；
- evidence commit changed path exact one ER；
- 原payload自报physical EOF/append-last，但实际插入于旧suffix之前；
- 原payload记录unauthorized `codegraph_queries_before_controller=3`；
- first failure所称Advisor file hash drift实际是PLAN/M1 provenance路径语义misbinding：`842...`
  owner是external lineage-owner decision evidence，Advisor request Git file是`5b23...`，真正Option-B
  decision attachment是`91a88...`。

最后一项只从本PLAN冻结facts重述；本包不得重新读取相应文件。若任一Git/ER重算失败，仍须生成failure
terminal supersession payload并记录first failure，不能继续其他owner。

## 3. Exact terminal payload与physical EOF

在内存冻结single strict JSON object，至少包含schema/reference/contract、activation、reviewed evidence
commit、Git ledgers、两版ER identity、prefix/insert/suffix重算、原payload三项finding、correct provenance
owner mapping、actual/budget、zero locks、retained status、outcome及唯一Planner stop。

Success outcome只能是：
`B3_C1_C1_S1_GIT_ER_ONLY_TERMINAL_SUPERSESSION_RECORDED`。

使用exact one `apply_patch`在current `EXECUTION_RESULT.md`**真实文件末尾**追加heading与single strict JSON
block。不得按同名早期heading插入；patch anchor必须使用current committed ER的exact final unique context。
Append为最后side effect，之后read/status/hash/Git/probe/second append均为`0`。本包无implementation commit。

## 4. Locks 与stop

不修改、repair或regenerate旧B3-C1-C1 payload、B2 manifest five、source、C1或retained artifacts。
Canonical validator、retained audit、eligibility、release及device/formal全部保持锁定。Supersession成功只
修复repository evidence ledger，不credit B3-C1-C1 scientific/verification pass，也不解锁B4。

成功或失败均停
`B3_C1_C1_S1_GIT_ER_ONLY_TERMINAL_SUPERSESSION_WAITING_PLANNER_REVIEW`。

维护性判断：本包只用committed Git objects纠正ER账本且不新增parser/owner；后续治理字段修正必须作为
独立production+dedicated-test package，保持immutable manifest与canonical eligibility owner不变。
