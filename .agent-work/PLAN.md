# REF-P7-25-R2-B2-P7-I1-E1：synthetic integration terminal-count evidence supersession

**计划状态：** `WAITING_ORCHESTRATOR_ACTIVATION`

**Planner 日期：** `2026-07-31`

**Reference task：** `REF-P7-25-R2-B2-P7-I1-E1`

**Contract ID：**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-P7-I1-E1-TERMINAL-COUNT-EVIDENCE-SUPERSESSION-V1`

**当前唯一动作：** Orchestrator审核本PLAN、同步其独占FULL，并以当前clean HEAD
`6c85cdb07a115b16c3879805c0a14f37b866f0df`为direct parent创建exact activation
commit。Activation完成且worktree clean后，Executer只读重验immutable P7-I1 source、
root、activation/evidence commit和ER prefix，然后向ER做一次append-only supersession：
只纠正旧terminal record的两个历史累计计数，不修改任何旧byte，不重跑integration。

**唯一 Planner stop：**
`B2_P7_I1_E1_TERMINAL_COUNT_EVIDENCE_SUPERSESSION_WAITING_PLANNER_REVIEW`。

**本轮新归档：**
`.agent-work/PLANS/20260731-2023-p7-retained-r3-b2-p7-i1-synthetic-integration-review.md`；bytes
`8853`，SHA-256
`9a67735eba56f801998b8390add9eb69647df36f787a4f6331c586a12bad277f`；不得覆盖earlier archives。

`PLAN_MACHINE_CONTRACT={"schema":"p7_td_b_retained_r3_option_b_b2_p7_i1_e1_terminal_count_evidence_supersession_v1","reference_task_id":"REF-P7-25-R2-B2-P7-I1-E1","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-P7-I1-E1-TERMINAL-COUNT-EVIDENCE-SUPERSESSION-V1","execution_authorized_after_orchestrator_activation":true,"activation_commit":{"expected_parent":"6c85cdb07a115b16c3879805c0a14f37b866f0df","expected_subject":"chore(plan): activate p7 synthetic evidence supersession","expected_changed_paths":[".agent-work/FULL_PLAN_REFERENCE.md",".agent-work/PLAN.md",".agent-work/PLANS/20260731-2023-p7-retained-r3-b2-p7-i1-synthetic-integration-review.md"],"clean_porcelain_required_after_activation":true},"required_full_machine_state":{"active_task_count":1,"active_task":"REF-P7-25-R2-B2-P7-I1-E1","active_plan_contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-P7-I1-E1-TERMINAL-COUNT-EVIDENCE-SUPERSESSION-V1","retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","p5_runtime_owner_status":"ACCEPTED_COMPLETE_REPO_OWNED_CONTROLLER_RUNTIME_OWNER","p6_domain_template_owner_status":"ACCEPTED_COMPLETE_DETERMINISTIC_DOMAIN_TEMPLATE_OWNER_WITH_RUNNABLE_CONTRACT_RESIDUAL","p7_status":"ACCEPTED_COMPLETE_REPO_OWNED_RUNNABLE_DOMAIN_TEMPLATE_OWNER","p7_candidate_commit":"864f08cc5436519a37e41d553e49ebde4a3c8bb2","p7_candidate_consumable":true,"p7_candidate_consumable_scope":"FUTURE_PURE_OFFLINE_SYNTHETIC_INTEGRATION_INPUT_ONLY","p7_synthetic_integration_qualified":false,"p7_i1_status":"REJECTED_TERMINAL_COUNT_SNAPSHOT_INCONSISTENCY_INTEGRATION_SEMANTICS_PROVISIONALLY_PROVEN","executer_dispatched":true,"device_authorized_by_this_file":false},"frozen_integration":{"activation_commit":"c245bbc7d7b120c83dd59b2b2cc87b8f9f01dae2","activation_parent":"9d8573fd4155851adc6e71b3b0ccc50365f6f6d3","activation_subject":"chore(plan): activate p7 synthetic integration","activation_paths":[".agent-work/FULL_PLAN_REFERENCE.md",".agent-work/PLAN.md",".agent-work/PLANS/20260731-1921-p7-retained-r3-b2-p7-acceptance-route-review.md"],"evidence_commit":"6c85cdb07a115b16c3879805c0a14f37b866f0df","evidence_parent":"c245bbc7d7b120c83dd59b2b2cc87b8f9f01dae2","evidence_subject":"chore(evidence): record p7 synthetic integration","evidence_paths":[".agent-work/EXECUTION_RESULT.md"],"er_pre_bytes":1133941,"er_pre_sha256":"a60e328ae4c47abd5f56d2116b8239fcb1bb4f23c969001a3b4dde8b1e060f6f","er_evidence_bytes":1140609,"er_evidence_sha256":"85072a33ae2cf9d9074f70ec93263ce36e8ff9a25bf14ba1e1a290088cd2409f","er_added_lines":179,"er_added_bytes":6668,"historical_execution_result_append_actual":1,"historical_outer_shell_commands_final_actual":5,"superseded_snapshot_values":{"execution_result_append":0,"outer_shell_commands_cumulative":4}},"immutable_source":{"path":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-p7-i1-source-c245bbc7d7b1.py","bytes":13946,"sha256":"e66afc9b6d2a8b9092a5d051fc3260a3078cab1d60ea5ceb92baa755bca6bc0a","mode":384,"device":16777240,"inode":2253709},"immutable_root":{"path":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-p7-i1-root-c245bbc7d7b1","mode":448,"device":16777240,"inode":2253710,"artifact_count":9,"artifact_sha256":{"execution-result-admission.json":"ae37face4b811daec3d0c6762e22bb2c99b47ee47e14d2a6d218a20a3afc9908","integration-qualification.json":"1a37676bf034bc575f57570a9532d32db6395d675bb2addf0a7da4242c3768a8","integration-qualification.sha256.json":"9e80d174ad63f8adc4423d0f94c7c249d6f14e7086c678a5ba4498d981c2a257","synthetic-full.json":"b3d452931897ddca36ea73587fc00b3900925fa4d5e7144899c2f88f671d4d9d","synthetic-lineage.json":"c0d4ed42c5435ad2c4595d157c38ef7c961b08f9038c9402b1c7b96624ec987e","synthetic-plan.json":"f235229723506e28e6ea148dd2f80bcc71b4612239f1f6b0009747dd37111702","synthetic-seal.json":"7dc2d9a59478b3daa8f1ba0b506373db33a1cc00e5be4488a90f2e3ea1ac5542","terminal-evidence.json":"16503bcb3d78becd58f9fcbb0f2a67de9f529eeaabce14d9697fe7ee7c1ce937","terminal-evidence.sha256.json":"667ef7b5eb899feea579f2c9a9affa12cf490e67997cd8b46127e8e69049e8b1"}},"supersession":{"scope":["counts.execution_result_append","counts.outer_shell_commands_cumulative"],"old_record_immutable":true,"append_only":true,"single_append":1,"integration_rerun":0,"root_source_mutation":0},"zero_budgets":{"builder":0,"runtime":0,"controller":0,"controller_process":0,"controller_git_ledgers":0,"integration":0,"source_create":0,"root_create":0,"source_root_writes":0,"source_root_delete_repair_rename_reuse":0,"old_er_prefix_writes":0,"tests":0,"compileall":0,"codegraph_sync":0,"codegraph_query":0,"code_writes":0,"test_writes":0,"production_writes":0,"implementation_commits":0,"old_p5_i1_source_reads":0,"old_failed_root_reads":0,"old_external_evidence_reads":0,"retained_artifact_reads":0,"candidate_payload_reads":0,"real_b2_dispatch":0,"subordinate_manifest_writes":0,"canonical_validator_calls":0,"eligibility_emissions":0,"retained_release_audit":0,"release_generation":0,"release_qualification":0,"release_copy":0,"release_consumption":0,"network":0,"dns":0,"environment":0,"credentials":0,"device":0,"camera":0,"ray":0,"strip":0,"cleanup":0,"capture":0,"formal":0,"public_analyzer":0,"td_c":0,"sentinel":0,"p8":0,"firmware":0,"deployment":0,"git_stage":0,"git_commit":0},"archive":{"path":".agent-work/PLANS/20260731-2023-p7-retained-r3-b2-p7-i1-synthetic-integration-review.md","bytes":8853,"sha256":"9a67735eba56f801998b8390add9eb69647df36f787a4f6331c586a12bad277f"},"expected_duration":"under_10_minutes","visible_terminal_required":false,"planner_stop":"B2_P7_I1_E1_TERMINAL_COUNT_EVIDENCE_SUPERSESSION_WAITING_PLANNER_REVIEW"}`

## 1. Activation gate and immutable prefix

Activation commit必须满足machine row的direct parent、subject和exact three changed
paths；完成后worktree必须clean。FULL必须把本reference/contract设为唯一active，保持
retained `RETAINED_UNVALIDATED_UNCONSUMED`、三个accepted owner状态、candidate的
synthetic-input-only consumable scope、synthetic integration尚未accepted，以及本次
rejection状态。该状态只表示terminal count evidence需要closure，不否定已证明的
integration语义。

Executer在任何external evidence read或ER append前，严格提取PLAN/FULL各唯一一条
literal backtick-wrapped machine row并strict JSON decode，校验activation和FULL
subset。随后只读验证当前HEAD、activation/evidence topology、exact paths，以及
dispatch worktree clean。ER必须仍exact bytes `1140609`、SHA-256
`85072a33ae2cf9d9074f70ec93263ce36e8ff9a25bf14ba1e1a290088cd2409f`；若不符，
fail closed且ER写入`0`。不得读取任何旧P5-I1 source/root/external evidence。

## 2. Exact read-only evidence audit

只允许一次bounded audit读取machine row中指定的fresh source/root与Git/ER evidence：

1. Source用`lstat`、`O_NOFOLLOW`只读；必须为regular `0600`，bytes/hash/device/inode
   exact match。不得import、compile、exec或作为stdin启动。
2. Root用`lstat`且不跟随symlink；必须为physical `0700`，device/inode exact。
   direct entries必须exact九个；每项regular `0600`、strict canonical JSON、
   hash exact、无symlink/path escape。
3. 两个sidecar必须绑定exact same-root target bytes/SHA；qualification必须exact
   ordered `16/16` true list-of-lists；terminal status与admission true必须保持。
4. Source/root audit前后physical identity、file set、bytes/hash必须完全相同。
5. Git必须证明旧evidence commit是activation的direct child、subject/path exact，且ER
   change为EOF-only `179` lines / `6668` bytes append；旧prefix bytes/hash exact。
6. 只复核已有process stdout/stderr/exit hashes和success envelope；不得启动process、
   builder、runtime、controller或再次运行Git6。

Runtime report未直接展开Git6、root chain、same-root4或matrix16的每个identity不是
failure：immutable source定义guarded order，qualification保存exact 16 true rows，
exact9 durable artifacts与success envelope共同提供独立证明。不得为了扩大报告字段而
修改代码、source/root或重跑integration。

## 3. Single append-only supersession

只有第2节全部通过后，才允许对`.agent-work/EXECUTION_RESULT.md`做一次single EOF
append。Append前必须再次验证旧prefix的bytes/SHA，使用append/no-follow语义且不得
seek、truncate、rewrite、repair或regenerate旧record。新section必须包含一个strict
JSON supersession record并清楚声明：

- bind activation `c245bbc7d7b120c83dd59b2b2cc87b8f9f01dae2`、evidence commit
  `6c85cdb07a115b16c3879805c0a14f37b866f0df`、旧ER before/after identities、
  exact append delta及source/root identities；
- supersede scope只能是旧record的
  `counts.execution_result_append`和`counts.outer_shell_commands_cumulative`；
- 旧值是record创建时的pre-append snapshot `0`和`4`，不是final cumulative facts；
- historical integration actual values exact为ER append `1`和final shell commands
  `5`，其中第五条是唯一terminal ER append；
- 所有其他旧terminal fields保持authoritative且不被覆盖；integration success仍只能是
  `FRESH_SYNTHETIC_INTEGRATION_QUALIFIED_NOT_RETAINED_ELIGIBLE`；
- 本supersession自身的append intent为exact `1`，实际single append由后续Git diff和
  Planner独立验收证明，不能在写前伪称已完成；
- source/root/旧ER prefix均未修改，integration/controller/tests/retained/release/
  network/device等全部hard locks保持`0`。

Append后只允许只读确认ER新bytes增加、旧prefix逐byte保持、且新增section位于EOF。
不得第二次append或自行commit。所有in-memory observations一并写入这一次append；若
append前任一检查失败，ER writes必须`0`并直接stop，由Orchestrator从terminal输出接管。

## 4. Acceptance criteria

Planner只在以下全部成立时接受：

1. activation/machine rows/FULL subset/current clean exact；
2. immutable source regular/0600/bytes/hash/device/inode exact且未执行；
3. root physical 0700、exact9 regular 0600 canonical artifacts及全部hash exact；
4. sidecars、ordered matrix16、terminal、admission与source/root before/after identity成立；
5. old activation/evidence topology与EOF-only `179` lines / `6668` bytes delta成立；
6. old ER prefix `1140609` bytes / frozen SHA逐byte不变；
7. new record只supersede exact two fields并如实区分snapshot与historical final；
8. historical actual append `1`、final shell `5`，且其他旧terminal facts不变；
9. current package只有single EOF append，外加post-append read-only prefix check；
10. source/root writes与所有rerun/retry/adjacent routes exact `0`。

若接受，Planner可将P7-I1标记为synthetic integration qualified，并为Orchestrator提出
下一reference route；本PLAN本身不解锁retained validation、validator或release。

## 5. Hard locks and stop

Builder、runtime、controller、process、controller Git6、integration、source/root create
或mutation、tests、compileall、CodeGraph、code/test/production write、implementation
commit、old paths、retained R3/candidate payload、real B2、subordinate manifest、canonical
validator、eligibility、retained audit、全部release、network/DNS/environment/credentials、
device/camera/Ray/strip/cleanup/capture/FORMAL/public analyzer、TD-C、sentinel、P8、
firmware/deployment全部exact `0`。不需要Advisor或Human checkpoint。

无论success或failure，Executer在single append或pre-append fail-closed后必须停在：

`B2_P7_I1_E1_TERMINAL_COUNT_EVIDENCE_SUPERSESSION_WAITING_PLANNER_REVIEW`

维护性判断：本包只为immutable terminal record建立窄范围append-only supersession，
不新增生产owner、parser、controller或evidence framework；后续由Git delta和Planner
独立审计闭环，避免修改历史证据。
