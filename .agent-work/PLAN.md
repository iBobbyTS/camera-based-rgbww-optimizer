# REF-P7-25-R2-B2-P4-C1-C1：activation provenance disposition Planner stop

**计划状态：** `PLANNER_STOP_WAITING_ORCHESTRATOR_GIT_PROVENANCE_DECISION`

**Planner 日期：** `2026-07-31`

**Reference task：** `REF-P7-25-R2-B2-P4-C1-C1`

**Contract ID：**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-P4-C1-C1-ACTIVATION-PROVENANCE-DISPOSITION-STOP-V1`

**当前唯一动作：** Orchestrator 独立审核 P4-C1 的 activation subject / ER provenance 失配，更新
`.agent-work/FULL_PLAN_REFERENCE.md`，并向 Planner 回交一个不改写已提交历史的 bounded disposition。

**唯一 Planner stop：**
`B2_P4_C1_C1_WAITING_ORCHESTRATOR_GIT_PROVENANCE_DECISION`。

**本轮新归档：**
`.agent-work/PLANS/20260731-1326-p7-retained-r3-b2-p4-c1-transport-domain-owner-correction-review.md`，
bytes `21675`，SHA-256 `d4c82e8479668db8bfce750e2f851bf8486db24f2c2c510ae56d00735e5997fd`。

`PLAN_MACHINE_CONTRACT={"schema":"p7_td_b_retained_r3_option_b_b2_p4_c1_c1_activation_provenance_disposition_stop_v1","reference_task_id":"REF-P7-25-R2-B2-P4-C1-C1","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-P4-C1-C1-ACTIVATION-PROVENANCE-DISPOSITION-STOP-V1","execution_authorized":false,"executer_dispatch_allowed":false,"planner_stop":true,"blocking_findings":["activation_subject_mismatch","execution_result_activation_subject_misstatement"],"actual_activation_commit":"48adfd669dc8d49fe11c983a4ca36e928bef6c22","actual_activation_parent":"781e410c43774c20da9f00e8c9e0f5bfd27b1f66","expected_activation_subject":"chore(plan): activate p4 transport domain owner correction","actual_activation_subject":"chore(plan): activate p4 transport domain correction","implementation_commit":"0ec12f2de91b84f4379d64437170fa53c3ae4a28","evidence_commit":"bd9d205cf7a4385d202666f87d225739e57c970c","required_owner":"Orchestrator","history_rewrite_allowed":false,"retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","zero_budgets":{"code_writes":0,"test_writes":0,"execution_result_writes":0,"external_controller_writes":0,"external_controller_reads":0,"external_root_creates":0,"external_root_reads":0,"synthetic_integration_runs":0,"retained_artifact_reads":0,"real_b2_dispatch":0,"actual_canonical_validator_calls":0,"eligibility_emissions":0,"release_operations":0,"network":0,"dns":0,"environment":0,"credentials":0,"device":0,"camera":0,"ray":0,"strip":0,"cleanup":0,"capture":0,"formal":0,"public_analyzer":0,"td_c":0,"sentinel":0,"p8":0,"firmware":0,"deployment":0}}`

## Planner finding

Active P4-C1 PLAN 把 activation subject 冻结为
`chore(plan): activate p4 transport domain owner correction`，但 commit
`48adfd669dc8d49fe11c983a4ca36e928bef6c22` 的真实 subject 是
`chore(plan): activate p4 transport domain correction`。Executer ER 又将真实 subject 记录成预期值。这是
strict activation hard gate 和 evidence truthfulness 的双重不匹配，因此 P4-C1 按原合同被拒绝。

Implementation `0ec12f2...` 的 exact two-path scope、final blob/SHA、20 methods 以及 ER 记录的
targeted `20/20`、focused `76/76`、full `761/761` + `OK`、compileall、CodeGraph 和 postcommit
targeted `20/20` 均未发现其他阻断项；但这些不能自动豁免过去的 exact activation gate。

## Orchestrator decision boundary

Orchestrator 必须选定一个不 amend、rebase、cherry-pick、reset 或其他改写历史的 disposition。Planner
建议最小路线是 validation-only successor：绑定真实 activation/implementation/evidence commit 和最终两文件身份，
如实追加 supersession evidence，不改code/test，不重写旧 ER，不运行external integration。Orchestrator 也可以选择
更严格的新 implementation lineage，但必须先明确新 parent/scope/验证证据与旧实现的 disposition。

## Hard locks

在 Orchestrator 回交并由 Planner 写出新 active executable package 前，Executer 不得被派遣。code/test/ER 写入、
external controller/source/root、synthetic integration、retained R3/candidate、Git provenance replay、real B2、subordinate manifest、
canonical validator、eligibility、retained audit、release、network/DNS/environment/credentials、device/camera/Ray/strip/cleanup/
capture/FORMAL/public analyzer/TD-C/sentinel/P8/firmware/deployment 全部锁 `0`。

维护性判断：当前问题只是 Git/ER provenance 不一致，不要为此增加新 analyzer、transport owner 或执行框架。
