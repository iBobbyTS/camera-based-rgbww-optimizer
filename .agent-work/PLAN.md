# P7 retained-R3 Option B：B3-C2-S1 Git/ER-only budget supersession

**计划状态：** `WAITING_ORCHESTRATOR_ACTIVATION`

**Planner 日期：** `2026-08-01`

**Reference task：** `REF-P7-25-R2-B3-C2-S1`

**Contract：**
`P7-TD-B-RETAINED-R3-OPTION-B-B3-C2-S1-GIT-ER-ONLY-BUDGET-SUPERSESSION-V1`

**当前唯一动作：** Orchestrator先记录B3-C2 review decision并创建activation；Executer随后只使用committed Git
objects、本active PLAN/FULL machine state及本轮review archive，复核`e84f5b6...`的exact commit identity、two-path
blob/diff identity和ER physical-EOF evidence，然后在`.agent-work/EXECUTION_RESULT.md`真实physical EOF追加exact one
canonical terminal supersession block。不得修改或直接读取code/test，不得重跑任何测试或科学/设备路径。

**唯一 Planner stop：**
`B3_C2_S1_GIT_ER_ONLY_BUDGET_SUPERSESSION_WAITING_PLANNER_REVIEW`。

**本轮新归档：**
`.agent-work/PLANS/20260801-0513-p7-retained-r3-b3-c2-governance-identity-review.md`；
bytes `5672`，SHA-256 `28de01953ea65f31fa35ed37b003f8e27d2d2a4390b2c614962b35033e3faee8`；不得覆盖earlier archives。

`PLAN_MACHINE_CONTRACT={"schema":"p7_td_b_retained_r3_option_b_b3_c2_s1_git_er_only_budget_supersession_v1","reference_task_id":"REF-P7-25-R2-B3-C2-S1","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B3-C2-S1-GIT-ER-ONLY-BUDGET-SUPERSESSION-V1","execution_authorized_after_orchestrator_activation":true,"activation_commit":{"expected_parent":"e84f5b6adc7c004b388074f5e81a4d109a6541f2","expected_subject":"chore(plan): activate B3-C2 budget supersession","expected_changed_paths":[".agent-work/FULL_PLAN_REFERENCE.md",".agent-work/PLAN.md",".agent-work/PLANS/20260801-0513-p7-retained-r3-b3-c2-governance-identity-review.md"],"clean_porcelain_required_after_activation":true},"reviewed_b3_c2":{"activation":"8e5d4ea520fd5aa5edb41af7b574188b47596bc3","evidence_commit":"e84f5b6adc7c004b388074f5e81a4d109a6541f2","decision":"REJECTED_EXECUTION_BUDGET_ACCEPTED_COMMITTED_IMPLEMENTATION_PENDING_TERMINAL_SUPERSESSION","evidence_parent":"8e5d4ea520fd5aa5edb41af7b574188b47596bc3","evidence_subject":"fix(p7): correct manifest governance identity","evidence_changed_paths":[".agent-work/EXECUTION_RESULT.md","src/camera_based_rgbww_optimizer/utils/p7_retained_r3_real_manifest_domain_template.py","tests/test_p7_retained_r3_real_manifest_domain_template.py"],"source_post_sha256":"da8b24b9530d387befde8eda3f0ee0dcfca373e28f27a6bda3433c4f4bf5f410","test_post_sha256":"193464af34c10809b91987f984a4b7ce40f924df66a472511acbd6fb5142b378","two_path_binary_diff_sha256":"2685d00525d90f725ed3c73ca7adeebcf9bb5ade14c39dc4172d725fa9d741c0","parent_er":{"bytes":1309616,"sha256":"f0474fcc4b6f835d91c9483f4923b9ca50f54ce3b0fa7816ca2be32caeee7546"},"evidence_er":{"bytes":1314849,"sha256":"ff23fe99b2819bae2c90542f7ea1ddd42445553363960ac1a5e35a182ae8f33f"},"physical_eof_suffix":{"bytes":5233,"sha256":"66ec9bb4cccbc33e93ef461cf311c895e1ca9dec4afd9eb879b9ecd570470be9"},"parent_is_complete_prefix":true,"payload_strict_canonical_json":true,"historical_repository_code_reads":{"actual":2,"max":1},"historical_repository_test_reads":{"actual":2,"max":1},"implementation_candidate_accepted":true,"execution_contract_accepted":false,"executor_validation":{"targeted":13,"focused":83,"compileall":true,"full":800,"codegraph_query":1,"codegraph_sync":1,"diff_check":true},"planner_independent_validation":{"targeted":13,"focused":83}},"required_full_machine_state":{"active_task_count":1,"active_task":"REF-P7-25-R2-B3-C2-S1","active_plan_contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B3-C2-S1-GIT-ER-ONLY-BUDGET-SUPERSESSION-V1","retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","manifest_authority":"SUBORDINATE_EVIDENCE_ONLY_CANONICAL_VALIDATOR_SOLE_ELIGIBILITY_OWNER","b3_c2_status":"REJECTED_EXECUTION_BUDGET_ACCEPTED_COMMITTED_IMPLEMENTATION_PENDING_TERMINAL_SUPERSESSION","b3_c2_s1_status":"ACTIVE_GIT_ER_ONLY_BUDGET_SUPERSESSION","executer_dispatched":true,"device_authorized_by_this_file":false},"exact_write_paths":[".agent-work/EXECUTION_RESULT.md"],"git_object_contract":{"reviewed_commit":"e84f5b6adc7c004b388074f5e81a4d109a6541f2","reviewed_parent":"8e5d4ea520fd5aa5edb41af7b574188b47596bc3","reviewed_subject":"fix(p7): correct manifest governance identity","reviewed_changed_paths":[".agent-work/EXECUTION_RESULT.md","src/camera_based_rgbww_optimizer/utils/p7_retained_r3_real_manifest_domain_template.py","tests/test_p7_retained_r3_real_manifest_domain_template.py"],"source_blob_sha256":"da8b24b9530d387befde8eda3f0ee0dcfca373e28f27a6bda3433c4f4bf5f410","test_blob_sha256":"193464af34c10809b91987f984a4b7ce40f924df66a472511acbd6fb5142b378","binary_diff_sha256":"2685d00525d90f725ed3c73ca7adeebcf9bb5ade14c39dc4172d725fa9d741c0","er_parent_prefix_required":true,"old_payload_repair":false,"old_payload_regeneration":false},"execution_budgets":{"git_read_invocations_max":18,"execution_result_committed_reads":2,"source_git_blob_reads":1,"test_git_blob_reads":1,"binary_diff_reads":1,"plan_reads":1,"full_reads":1,"archive_reads":1,"execution_result_appends":1,"apply_patch_invocations_max":2,"postappend_operations":0,"implementation_commits_by_executer":0,"retry":0,"fallback":0},"success_outcome":"B3_C2_S1_EXECUTION_BUDGET_DISTINCTION_SEALED","orchestrator_commit_after_handoff":{"owner":"ORCHESTRATOR","executer_must_not_commit":true,"expected_subject":"chore(evidence): seal B3-C2 budget distinction","expected_changed_paths":[".agent-work/EXECUTION_RESULT.md"]},"zero_budgets":{"repository_code_direct_reads":0,"repository_test_direct_reads":0,"repository_code_writes":0,"repository_test_writes":0,"third_path_writes":0,"plan_writes_by_executer":0,"full_writes_by_executer":0,"archive_writes_by_executer":0,"debug_writes":0,"guide_reads":0,"guide_writes":0,"research_writes":0,"advisor_file_reads":0,"advisor_attachment_reads":0,"external_governance_evidence_reads":0,"old_b2_manifest_reads":0,"old_b2_manifest_writes":0,"old_payload_repair":0,"old_payload_regeneration":0,"real_manifest_reads":0,"real_manifest_writes":0,"c1_input_reads":0,"retained_artifact_reads":0,"retained_artifact_writes":0,"codegraph_queries":0,"codegraph_sync":0,"tests":0,"compileall":0,"controller_invocations":0,"synthetic_runs":0,"actual_canonical_lineage_validator_calls":0,"canonical_validator_callbacks":0,"retained_release_audit":0,"eligibility_emissions":0,"release_generation":0,"release_qualification":0,"release_copy":0,"release_consumption":0,"network":0,"dns":0,"environment":0,"credentials":0,"device":0,"camera":0,"ray":0,"strip":0,"cleanup":0,"capture":0,"formal":0,"public_analyzer":0,"td_c":0,"sentinel":0,"p8":0,"firmware":0,"deployment":0},"authorization":{"classification":"PURE_OFFLINE_GIT_ER_ONLY_EXECUTION_BUDGET_SUPERSESSION","human_device_authorization_required":false,"advisor_scientific_decision_required":false},"expected_duration":"under_10_minutes","visible_terminal_required":false,"archive":{"path":".agent-work/PLANS/20260801-0513-p7-retained-r3-b3-c2-governance-identity-review.md","bytes":5672,"sha256":"28de01953ea65f31fa35ed37b003f8e27d2d2a4390b2c614962b35033e3faee8"},"planner_stop":"B3_C2_S1_GIT_ER_ONLY_BUDGET_SUPERSESSION_WAITING_PLANNER_REVIEW"}`

## 1. Activation 与输入边界

Activation必须以`e84f5b6...`为parent、exact subject/path set，并在dispatch前porcelain clean。Executer只读取
activation committed PLAN/FULL各一次和review archive一次。Machine row按backtick内exact
`PLAN_MACHINE_CONTRACT=` / `FULL_PLAN_MACHINE_STATE=`前缀定位并做strict JSON decode与typed semantic subset compare；
不得增加canonical reencode、key-order或raw-byte-equality gate。

本包只复核committed Git objects。禁止直接打开working-tree source/test，禁止读取retained、C1、old B2 manifest、real
manifest、external governance evidence或Advisor attachment。PLAN中冻结的hash只用于Git-object exact compare，不授权读取其
外部原文件。

## 2. Exact Git/ER supersession

在single bounded invocation内：

1. 核对activation parent/subject/changed paths和initial clean status；
2. 核对`e84f5b6...` parent、subject与exact three changed paths；
3. 从`e84f5b6...` exact source/test Git blobs各读取一次并计算冻结SHA；
4. 计算`8e5d4ea...`至`e84f5b6...` exact two-path binary diff SHA；
5. 读取activation与evidence commit中的ER blobs各一次，证明parent ER是evidence ER完整prefix，重算bytes/SHA及physical EOF
   suffix identity，并strict decode最后canonical payload；
6. 明确保留历史actual source/test direct reads各`2`、budget各`1`，不得改写为合规；同时记录two-path implementation
   candidate accepted、original execution contract rejected。

任何identity mismatch均fail closed并记录first failure，不搜索alternate path、不读取working-tree code/test、不重试。

## 3. Handoff 与终端证据

完成全部Git-object检查后，可读取current ER tail exact once取得唯一EOF anchor，再用exact one `apply_patch`向physical EOF
追加一个heading加single canonical JSON block。Payload至少记录activation、reviewed commit identity、source/test blob与binary
diff SHA、ER parent/evidence/suffix identity、historical budget violation、accepted implementation/rejected execution distinction、
actual/budget、zero locks、outcome与唯一Planner stop。

Success outcome只能是`B3_C2_S1_EXECUTION_BUDGET_DISTINCTION_SEALED`；它不得声称原B3-C2 execution成功，不得生成
eligibility或解锁retained/release。失败必须记录first failure与已完成计数。

ER append是Executer最后side effect；其后read/status/hash/test/commit均为`0`。Executer不得commit；Orchestrator收到handoff
后按AGENTS创建exact ER-only focused commit。

## 4. Locks 与下一门

本包不重跑targeted/focused/full/compileall，不调用CodeGraph、controller、synthetic、canonical validator或retained audit。
`RETAINED_UNVALIDATED_UNCONSUMED`保持不变；canonical lineage validator仍是唯一eligibility owner；B4、release、device、
FORMAL-R6、strip、TD-C、sentinel与P8全部locked。

S1成功后也只允许Planner验收此ledger distinction；随后由Orchestrator决定fresh postcommit self-check/test/synthetic
verification包，不得直接进入real retained audit或release。

成功或失败均停
`B3_C2_S1_GIT_ER_ONLY_BUDGET_SUPERSESSION_WAITING_PLANNER_REVIEW`。

维护性判断：本包只修复evidence ledger的状态表达，不触碰production/test或科学合同；历史预算偏差保持immutable且显式，
不会引入parallel owner或额外执行框架。
