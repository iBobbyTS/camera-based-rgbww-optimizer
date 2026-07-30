# REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-9：governance lineage successor alignment gate

**计划状态：** `PLANNER_STOP_WAITING_ORCHESTRATOR_EXACT_PROVENANCE_ALIGNMENT`

**Planner 日期：** `2026-07-29`

**Reference task：** `REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-9`（proposed；等待 Orchestrator 写入 FULL）

**Contract ID：** `P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F19-CORRECTIVE-9-GOVERNANCE-LINEAGE`

**唯一当前动作：** Orchestrator 审查 C8 full-suite 的两个治理文件 lineage drift，选择并冻结一个最小、精确、
append-only 的 successor provenance owner、repository/artifact path scope 与 Git topology；更新
`.agent-work/FULL_PLAN_REFERENCE.md` 后再交 Planner 写 exact executable corrective。当前 PLAN 不授权 Executer、
文件修改、测试重跑、外置 evidence 访问或任何设备/validator/release 操作。

**C8 review archive：**
`.agent-work/PLANS/20260729-2332-p7-retained-r3-option-b-b1a-c3e6f19-corrective-8-review.md`；
SHA-256 `2a7891b73aa452ccde97a710a93f5b0ecbb2d669ab2056725bf819869c517b5b`。

`PLAN_MACHINE_CONTRACT={"schema":"f19_corrective_9_governance_lineage_alignment_gate_v1","reference_task_id":"REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-9","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F19-CORRECTIVE-9-GOVERNANCE-LINEAGE","dispatch_state":"not_dispatchable_waiting_orchestrator_full_alignment_and_exact_scope","single_current_action":"orchestrator_freezes_exact_append_only_successor_provenance_owner_scope_and_git_topology","review_archive":{"path":".agent-work/PLANS/20260729-2332-p7-retained-r3-option-b-b1a-c3e6f19-corrective-8-review.md","sha256":"2a7891b73aa452ccde97a710a93f5b0ecbb2d669ab2056725bf819869c517b5b"},"c8_verdict":"REJECTED_FULL_SUITE_AMBIENT_GOVERNANCE_LINEAGE_DRIFT","accepted_c8_prerequisites":{"activation_lineage":true,"single_fd_log_ledger":"4/4","compileall_exit":0,"targeted_tests":"11/11","focused_tests":"43/43","c7_supersession":true,"repo_pre_er_diff_empty":true,"f19_committed_bytes_unchanged":true,"retry":0,"fallback":0},"full_suite":{"tests":684,"seconds":124.790,"exit_code":1,"failures":1,"errors":9,"later_command_invocations":0,"log_path":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b1a-c3e6f19-corrective-8-offline/full_unittest.log","log_bytes":150463,"log_sha256":"289bb7275acfd7e3d4016cdff767999c53ef1b62565999a0e00bde5e087e9c2e"},"root_cause":{"classification":"repository_ambient_known_governance_lineage_drift_not_f19_regression_fixture_environment_or_command_error","governance_commit":"3e2ebed","agents":{"frozen_sha256":"a035e6955ea113100031bf411f30abad3b84a9dd260fde848f1b1cfbd194c8a5","current_sha256":"604b10bedeac6c9285f6448f94323521bf021a58275cce84d64163e16a2f07a0","failure_count":1},"project_skill":{"historical_successor_commit":"e7ccdda672b7d5902d81627ff98268160ff141cd","frozen_sha256":"c8dd57a23ad684b4f7001f342ed3413a1abf4349bc6aeb90dbee7f5158139607","current_sha256":"3a77c8a0f7b02b0c8b15d31b625273e88a0ee38fca5bb739dbdaaacb40dfe81e","failure_count":9}},"orchestrator_alignment_requirements":{"preserve_historical_payloads_immutable":true,"no_old_manifest_or_policy_freeze_rewrite":true,"new_owner_must_bind_exact_current_governance_bytes":true,"new_owner_must_bind_exact_before_after_blob_oids_and_patch_identity":true,"generic_allowlist_forbidden":true,"canonical_lineage_validators_remain_fail_closed":true,"exact_changed_paths_and_commit_topology_required":true,"fresh_full_suite_required_after_correction":true},"current_operation_budgets":{"executer_dispatch":0,"repo_edits":0,"test_invocations":0,"git_mutations":0,"external_evidence_reads":0,"candidate_path_probes":0,"candidate_payload_reads":0,"retained_r3_path_probes":0,"retained_r3_reads":0,"canonical_validator_calls":0,"eligibility_emissions":0,"manifest_writes":0,"release_path_probes":0,"release_calls":0,"network_calls":0,"env_reads":0,"device_calls":0,"camera_calls":0,"ray_calls":0,"strip_calls":0,"cleanup_calls":0,"formal_calls":0,"public_analyzer_calls":0,"td_c_calls":0,"sentinel_calls":0,"p8_calls":0},"retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","advisor_required":false,"human_authorization_required":false,"planner_stop":"F19_CORRECTIVE_9_WAITING_ORCHESTRATOR_PROVENANCE_ALIGNMENT"}`

## C8 验收结论

C8 的 activation、single-fd evidence lifecycle、C7 supersession、repo pre-ER clean state 与 F19 committed bytes
均验收。compileall、targeted `11/11`、focused `43/43` 通过；但完整套件运行 684 项后为
`failures=1, errors=9`，因此 C8 整体拒绝，不得以 focused green 放行 F19。

十个失败全部由旧 exact lineage freeze 与后来 Human/Orchestrator 治理变更不一致触发：一个是当前
`AGENTS.md` bytes 与 frozen hash 不同，九个是当前项目 skill bytes/diff 与 e7ccdda historical successor 不同。
`3e2ebed` 改了这两个治理文件而未改 F19 controller/helper/test；没有 fixture、环境、依赖、discovery 或命令错误。

## Orchestrator alignment contract

下一个 executable corrective 必须保留既有 AGENTS policy freeze 与 e7ccdda public-default successor payload
只读不变；不得用更新旧 hash、重写旧 manifest、宽泛 path allowlist 或跳过 validator 来消除失败。Orchestrator 应冻结
一个新的 subordinate successor layer，精确绑定合法治理变更的 before/after blob OID、commit/parent、exact path set、
canonical patch SHA-256、当前 bytes 与 rollback，并规定 production validator/test/artifact 的最小 changed paths。

Orchestrator alignment 后，Planner 必须重写本 PLAN 为唯一 fresh corrective package，给出 exact activation lineage、
fresh evidence root、编辑预算、targeted/focused/full validation chain 与 fail-fast terminal contract。未经这一步不得派发
Executer，也不得接受 full-suite nonzero。

## 持续硬锁与停止点

Candidate、retained R3、canonical retained validator、eligibility、release、network、`.env`、device、camera、Ray、strip、
cleanup、FORMAL-R6、public analyzer、TD-C、sentinel 与 P8 全部锁定。Retained R3 保持
`RETAINED_UNVALIDATED_UNCONSUMED`。

这是纯工程 provenance/Git ownership 问题，不需要 Advisor 科学判断或 Human 高危设备授权。

**Planner stop：** `F19_CORRECTIVE_9_WAITING_ORCHESTRATOR_PROVENANCE_ALIGNMENT`。
