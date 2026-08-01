# REF-P7-25-R2-B2-P7-I1-E1-C1：audit-domain validation/evidence supersession

**计划状态：** `WAITING_ORCHESTRATOR_ACTIVATION`

**Planner 日期：** `2026-07-31`

**Reference task：** `REF-P7-25-R2-B2-P7-I1-E1-C1`

**Contract ID：**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-P7-I1-E1-C1-AUDIT-DOMAIN-VALIDATION-SUPERSESSION-V1`

**审核结论来源：** E1因临时audit错误要求root artifacts重复包含process exit字段而
fail closed；旧ER、source、root与candidate均未修改，integration语义仍为provisionally
proven。本包只纠正validation owner mapping，不修改任何历史证据。

**当前唯一动作：** Orchestrator审核本PLAN、同步其独占FULL，并以当前clean HEAD
`75d6ac5326322f1503c7175c6190db6b26162e2c`为direct parent创建exact activation commit。
Activation完成且worktree clean后，Executer执行一次新的E1-C1 bounded read-only audit；
全部gate通过后，向ER做一次single EOF supersession append。不得重跑integration或把本次
调用称为原E1 retry。

**唯一 Planner stop：**
`B2_P7_I1_E1_C1_AUDIT_DOMAIN_VALIDATION_SUPERSESSION_WAITING_PLANNER_REVIEW`。

**本轮新归档：**
`.agent-work/PLANS/20260731-2033-p7-retained-r3-b2-p7-i1-e1-audit-domain-failure-review.md`；
bytes `3629`，SHA-256
`630fcc445ddf758eaaea2da731f5b5416d4529aaf8203a3c6018f09fa371e6b0`；不得覆盖earlier archives。

`PLAN_MACHINE_CONTRACT={"schema":"p7_td_b_retained_r3_option_b_b2_p7_i1_e1_c1_audit_domain_validation_supersession_v1","reference_task_id":"REF-P7-25-R2-B2-P7-I1-E1-C1","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-P7-I1-E1-C1-AUDIT-DOMAIN-VALIDATION-SUPERSESSION-V1","execution_authorized_after_orchestrator_activation":true,"activation_commit":{"expected_parent":"75d6ac5326322f1503c7175c6190db6b26162e2c","expected_subject":"chore(plan): activate p7 audit domain validation closure","expected_changed_paths":[".agent-work/FULL_PLAN_REFERENCE.md",".agent-work/PLAN.md",".agent-work/PLANS/20260731-2033-p7-retained-r3-b2-p7-i1-e1-audit-domain-failure-review.md"],"clean_porcelain_required_after_activation":true},"required_full_machine_state":{"active_task_count":1,"active_task":"REF-P7-25-R2-B2-P7-I1-E1-C1","active_plan_contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-P7-I1-E1-C1-AUDIT-DOMAIN-VALIDATION-SUPERSESSION-V1","retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","p5_runtime_owner_status":"ACCEPTED_COMPLETE_REPO_OWNED_CONTROLLER_RUNTIME_OWNER","p6_domain_template_owner_status":"ACCEPTED_COMPLETE_DETERMINISTIC_DOMAIN_TEMPLATE_OWNER_WITH_RUNNABLE_CONTRACT_RESIDUAL","p7_status":"ACCEPTED_COMPLETE_REPO_OWNED_RUNNABLE_DOMAIN_TEMPLATE_OWNER","p7_candidate_commit":"864f08cc5436519a37e41d553e49ebde4a3c8bb2","p7_candidate_consumable":true,"p7_candidate_consumable_scope":"FUTURE_PURE_OFFLINE_SYNTHETIC_INTEGRATION_INPUT_ONLY","p7_synthetic_integration_qualified":false,"p7_i1_status":"REJECTED_E1_TRANSIENT_AUDIT_DOMAIN_ASSERTION_INTEGRATION_SEMANTICS_PROVISIONALLY_PROVEN","executer_dispatched":true,"device_authorized_by_this_file":false},"frozen_integration":{"activation_commit":"c245bbc7d7b120c83dd59b2b2cc87b8f9f01dae2","activation_parent":"9d8573fd4155851adc6e71b3b0ccc50365f6f6d3","activation_subject":"chore(plan): activate p7 synthetic integration","activation_paths":[".agent-work/FULL_PLAN_REFERENCE.md",".agent-work/PLAN.md",".agent-work/PLANS/20260731-1921-p7-retained-r3-b2-p7-acceptance-route-review.md"],"evidence_commit":"6c85cdb07a115b16c3879805c0a14f37b866f0df","evidence_parent":"c245bbc7d7b120c83dd59b2b2cc87b8f9f01dae2","evidence_subject":"chore(evidence): record p7 synthetic integration","evidence_paths":[".agent-work/EXECUTION_RESULT.md"],"er_pre_bytes":1133941,"er_pre_sha256":"a60e328ae4c47abd5f56d2116b8239fcb1bb4f23c969001a3b4dde8b1e060f6f","er_evidence_bytes":1140609,"er_evidence_sha256":"85072a33ae2cf9d9074f70ec93263ce36e8ff9a25bf14ba1e1a290088cd2409f","er_added_lines":179,"er_added_bytes":6668,"historical_execution_result_append_actual":1,"historical_outer_shell_commands_final_actual":5,"superseded_snapshot_values":{"execution_result_append":0,"outer_shell_commands_cumulative":4}},"immutable_source":{"path":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-p7-i1-source-c245bbc7d7b1.py","bytes":13946,"sha256":"e66afc9b6d2a8b9092a5d051fc3260a3078cab1d60ea5ceb92baa755bca6bc0a","mode":384,"device":16777240,"inode":2253709},"immutable_root":{"path":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-p7-i1-root-c245bbc7d7b1","mode":448,"device":16777240,"inode":2253710,"artifact_count":9,"artifact_sha256":{"execution-result-admission.json":"ae37face4b811daec3d0c6762e22bb2c99b47ee47e14d2a6d218a20a3afc9908","integration-qualification.json":"1a37676bf034bc575f57570a9532d32db6395d675bb2addf0a7da4242c3768a8","integration-qualification.sha256.json":"9e80d174ad63f8adc4423d0f94c7c249d6f14e7086c678a5ba4498d981c2a257","synthetic-full.json":"b3d452931897ddca36ea73587fc00b3900925fa4d5e7144899c2f88f671d4d9d","synthetic-lineage.json":"c0d4ed42c5435ad2c4595d157c38ef7c961b08f9038c9402b1c7b96624ec987e","synthetic-plan.json":"f235229723506e28e6ea148dd2f80bcc71b4612239f1f6b0009747dd37111702","synthetic-seal.json":"7dc2d9a59478b3daa8f1ba0b506373db33a1cc00e5be4488a90f2e3ea1ac5542","terminal-evidence.json":"16503bcb3d78becd58f9fcbb0f2a67de9f529eeaabce14d9697fe7ee7c1ce937","terminal-evidence.sha256.json":"667ef7b5eb899feea579f2c9a9affa12cf490e67997cd8b46127e8e69049e8b1"}},"audit_data_owner_map":{"process_exit_stdout_stderr":"old_er.runtime_report.process","success_label":"old_er.success_label","source_identity":"filesystem_immutable_source","root_identity_and_exact9":"filesystem_immutable_root","durable_canonical_sidecar_matrix_terminal_admission":"immutable_root_exact9_payloads","activation_evidence_topology_and_eof_delta":"git_and_old_er_prefix","supersession_scope_and_historical_counts":"plan_frozen_values_crosschecked_against_old_er_and_git"},"audit_invocations":{"prior_e1_bounded_audit":1,"prior_e1_retry":0,"e1_c1_fresh_successor_bounded_audit":1,"e1_c1_retry":0,"original_e1_retry":0},"supersession":{"scope":["counts.execution_result_append","counts.outer_shell_commands_cumulative"],"old_record_immutable":true,"append_only":true,"single_append":1,"integration_rerun":0,"root_source_mutation":0},"zero_budgets":{"builder":0,"runtime":0,"controller":0,"controller_process":0,"controller_git_ledgers":0,"integration":0,"source_create":0,"root_create":0,"source_root_writes":0,"source_root_delete_repair_rename_reuse":0,"old_er_prefix_writes":0,"tests":0,"compileall":0,"codegraph_sync":0,"codegraph_query":0,"code_writes":0,"test_writes":0,"production_writes":0,"implementation_commits":0,"old_p5_i1_source_reads":0,"old_failed_root_reads":0,"old_external_evidence_reads":0,"retained_artifact_reads":0,"candidate_payload_reads":0,"real_b2_dispatch":0,"subordinate_manifest_writes":0,"canonical_validator_calls":0,"eligibility_emissions":0,"retained_release_audit":0,"release_generation":0,"release_qualification":0,"release_copy":0,"release_consumption":0,"network":0,"dns":0,"environment":0,"credentials":0,"device":0,"camera":0,"ray":0,"strip":0,"cleanup":0,"capture":0,"formal":0,"public_analyzer":0,"td_c":0,"sentinel":0,"p8":0,"firmware":0,"deployment":0,"git_stage":0,"git_commit":0},"archive":{"path":".agent-work/PLANS/20260731-2033-p7-retained-r3-b2-p7-i1-e1-audit-domain-failure-review.md","bytes":3629,"sha256":"630fcc445ddf758eaaea2da731f5b5416d4529aaf8203a3c6018f09fa371e6b0"},"expected_duration":"under_10_minutes","visible_terminal_required":false,"planner_stop":"B2_P7_I1_E1_C1_AUDIT_DOMAIN_VALIDATION_SUPERSESSION_WAITING_PLANNER_REVIEW"}`

## 1. Activation and immutable prefix gate

Activation必须满足machine row冻结的direct parent、subject与exact three paths，完成后
worktree clean。FULL必须把本reference/contract设为唯一active，保持retained状态、三个
accepted owner、P7 candidate的synthetic-input-only consumable scope，以及P7-I1尚未最终
qualified的状态。

Executer在任何external evidence read或ER append前，用canonical helper各exact once解析
PLAN/FULL唯一machine row，校验activation与FULL subset。然后验证HEAD/topology/path与旧ER
prefix exact `1140609` bytes、SHA-256
`85072a33ae2cf9d9074f70ec93263ce36e8ff9a25bf14ba1e1a290088cd2409f`。
任一不符即fail closed，ER writes `0`。

## 2. Exact audit data-owner contract

本次只允许一次新的E1-C1 bounded read-only audit。它是stable successor的唯一audit，
不是原E1 retry；`original_e1_retry=0`、`e1_c1_retry=0`。

事实只能按下列owner读取与判断：

1. `old_er.runtime_report.process`独占process argv、exit code、stdout/stderr bytes、payload与
   SHA-256。必须验证exit `0`、stderr empty和single JSON stdout envelope；禁止要求root
   artifact重复包含`exit_code`或`returncode`。
2. `old_er.success_label`独占integration success label，必须exact为
   `FRESH_SYNTHETIC_INTEGRATION_QUALIFIED_NOT_RETAINED_ELIGIBLE`。
3. Physical source独占source path/mode/bytes/hash/device/inode；用`lstat`与`O_NOFOLLOW`
   只读，regular `0600`，不得import、compile、exec或作为stdin启动。
4. Physical root与exact9 payload独占root identity、direct file set、regular `0600`、
   strict canonical JSON、artifact hashes、sidecar same-root binding、ordered matrix `16/16`、
   terminal status与admission true。Root不拥有process stdout/stderr/exit。
5. Git与old ER prefix独占activation/evidence topology、exact paths、EOF-only `179` lines /
   `6668` bytes delta、旧prefix identity。
6. Source/root audit前后physical identity、file set、bytes/hash必须完全相同。不得放宽任何
   identity/hash/canonical/sidecar/matrix/lifecycle条件。

## 3. Single append-only supersession

只有第1至2节全部通过，才允许对`.agent-work/EXECUTION_RESULT.md`做一次single EOF
append。Append前再次验证old prefix bytes/SHA，使用append/no-follow语义，禁止seek、
truncate、rewrite、repair、regenerate或修改旧record。

新增strict JSON record必须绑定activation/evidence commits、old ER before/after identities、
exact EOF delta、source/root identities与本PLAN的owner map；supersede scope只能是
`counts.execution_result_append`和`counts.outer_shell_commands_cumulative`。必须区分旧
pre-append snapshot `0`/`4`与historical final actual `1`/`5`，保持其他旧terminal fields
authoritative。只能声明本append intent为`1`；single append实际值留给Git diff与Planner
验收。所有in-memory audit observations在同一次append写完。

Append后只读确认新bytes增加、old prefix逐byte不变、section位于EOF和worktree只改ER。
不得第二次append或commit。若pre-append任一检查失败，ER write为`0`并stop。

## 4. Acceptance criteria

Planner只在以下全部成立时接受：activation/FULL/current clean；immutable source identity；
physical root exact9/canonical/hash；sidecars/matrix16/terminal/admission；process facts只从旧ER
runtime report复核；success label exact；source/root before-after identity；old Git topology与
EOF delta；old ER prefix immutable；new record exact two-field supersession；historical actual
`1`/`5`；current package single EOF append；全部rerun/retry/adjacent routes为`0`。

若接受，Planner可将P7-I1标记为synthetic integration qualified并提出下一reference route；
本PLAN不解锁retained validation、canonical validator、eligibility或release。

## 5. Hard locks and stop

Builder、runtime、controller、process、controller Git6、integration、source/root create或
mutation、tests、compileall、CodeGraph、code/test/production write、implementation commit、
old paths、retained R3/candidate payload、real B2、subordinate manifest、canonical validator、
eligibility、retained audit、全部release、network/DNS/environment/credentials、device/camera/
Ray/strip/cleanup/capture/FORMAL/public analyzer、TD-C、sentinel、P8、firmware/deployment均为
exact `0`。不需要Advisor或Human checkpoint。

无论success或failure，Executer必须停在：

`B2_P7_I1_E1_C1_AUDIT_DOMAIN_VALIDATION_SUPERSESSION_WAITING_PLANNER_REVIEW`

维护性判断：本包只修正临时audit的事实owner mapping，并以旧ER与immutable root的既有
边界做一次validation/evidence closure；不新增生产抽象或平行evidence owner。
