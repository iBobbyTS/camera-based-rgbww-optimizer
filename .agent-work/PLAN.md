# REF-P7-25-R2-B2-P4-C1-C1-C1-I1-C1：outer preflight owner correction

**计划状态：** `WAITING_ORCHESTRATOR_ACTIVATION`

**Planner 日期：** `2026-07-31`

**Reference task：** `REF-P7-25-R2-B2-P4-C1-C1-C1-I1-C1`

**Contract ID：**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-P4-C1-C1-C1-I1-C1-OUTER-PREFLIGHT-OWNER-CORRECTION-V1`

**当前唯一动作：** Orchestrator 审核本 PLAN、更新 FULL，并以
`32899a26f36fbb73c3ab32d95da011b26d0a403a` 为 direct parent 创建 exact activation commit。Activation 后，Executer
创建并运行唯一 fresh external controller/source/root/process。Outer 只运行一次 `git rev-parse HEAD`；activation topology/path/blob 验证全部在
同一 controller 内使用原 exact Git6 budget 完成。

**唯一 Planner stop：**
`B2_P4_C1_C1_C1_I1_C1_OUTER_PREFLIGHT_OWNER_CORRECTION_WAITING_PLANNER_REVIEW`。

**本轮新归档：**
`.agent-work/PLANS/20260731-1410-p7-retained-r3-b2-p4-c1-c1-c1-i1-outer-git-failure-review.md`；activation 前由
Orchestrator记录其 final bytes/SHA-256 到 FULL/commit handoff。

`PLAN_MACHINE_CONTRACT={"schema":"p7_td_b_retained_r3_option_b_b2_p4_c1_c1_c1_i1_c1_outer_preflight_owner_correction_v1","reference_task_id":"REF-P7-25-R2-B2-P4-C1-C1-C1-I1-C1","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-P4-C1-C1-C1-I1-C1-OUTER-PREFLIGHT-OWNER-CORRECTION-V1","execution_authorized_after_orchestrator_activation":true,"activation_commit":{"expected_parent":"32899a26f36fbb73c3ab32d95da011b26d0a403a","expected_subject":"chore(plan): correct p4 synthetic outer preflight","expected_changed_paths":[".agent-work/FULL_PLAN_REFERENCE.md",".agent-work/PLAN.md",".agent-work/PLANS/20260731-1410-p7-retained-r3-b2-p4-c1-c1-c1-i1-outer-git-failure-review.md"],"clean_porcelain_required_after_activation":true},"required_full_machine_state":{"active_task_count":1,"active_task":"REF-P7-25-R2-B2-P4-C1-C1-C1-I1-C1","active_plan_contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-P4-C1-C1-C1-I1-C1-OUTER-PREFLIGHT-OWNER-CORRECTION-V1","retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","candidate_machine_contract_sha256":"96ece8940a82d53ff6e61b8b2e0ecb4f0cb01d93770ce5a992942c2464ab449a","candidate_contract_orchestrator_verified":true,"executer_dispatched":true,"device_authorized_by_this_file":false},"accepted_transport_owner":{"implementation_commit":"0ec12f2de91b84f4379d64437170fa53c3ae4a28","source_path":"src/camera_based_rgbww_optimizer/utils/p7_retained_r3_controller_conformance.py","source_blob_oid":"1868ad4b4446defcc6d8187ea21d18ccf128fa31","source_sha256":"6e10594165016a06da462e74a9deb2d9817fd95fe1417addb7a5d26c55996745","test_path":"tests/test_p7_retained_r3_controller_conformance.py","test_blob_oid":"25eafb91d7794d4510c9d7da34f1d8666ab1ff55","test_sha256":"e3c4a421e691c3aaac182edc6a0963a16caea95ae04f25a68493f96277bddb72","dedicated_test_methods":20,"targeted_tests":20,"focused_tests":76,"full_tests":761,"truthful_provenance_closure_commit":"baa14d15bfcef7463f23a1a3186741c9c9704a76","orchestrator_acceptance_commit":"fd040d45b1ba604186b4c1e092ba16ab8beed4a6"},"fresh_paths":{"activation_short_sha_source":"outer_head_stdout_first_seven_hex","controller_source_template":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-p4-c1-c1-c1-i1-c1-controller-{activation_short_sha}.py","output_root_template":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-p4-c1-c1-c1-i1-c1-qualification-{activation_short_sha}","must_be_absent_before_start":true,"source_mode":"0600","root_mode":"0700"},"controller_contract":{"source_create_once":true,"source_read_once":true,"strict_utf8_ast_compile":true,"controller_processes":1,"actual_runtime_source_analyzer_calls":1,"external_transport_ast_classifier_calls":0,"embedded_transport_report_consumed":true,"expected_bound_results":18,"effect_transport_uses_on_pass":0,"direct_nonlocal_effect_bindings":true,"inline_plain_field_projection":true,"generic_live_projection_helper_calls":0,"live_owner_collections":0,"live_owner_container_writes":0,"live_owner_aliases":0,"exact_root_identity_chain":true,"outer_git_invocations":1,"outer_git_argv":["git","rev-parse","HEAD"],"controller_activation_git_ledgers":6,"git_success_field":"exit_code","runtime_returncode_uses":0,"root_create_once":true,"synthetic_inputs":4,"semantic_matrix_cases":16,"exact_artifact_names":["synthetic-plan.json","synthetic-full.json","synthetic-lineage.json","synthetic-seal.json","integration-qualification.json","integration-qualification.sha256.json","terminal-evidence.json","terminal-evidence.sha256.json","execution-result-admission.json"],"final_root_file_count":9,"retry":0,"fallback":0,"second_source":0,"second_root":0,"second_process":0},"execution_budgets":{"outer_read_only_git_invocations":1,"controller_read_only_git_invocations":6,"controller_source_writes":1,"controller_source_reads":1,"controller_processes":1,"output_roots":1,"synthetic_input_writes":4,"qualification_writes":2,"terminal_writes":2,"admission_writes":1,"execution_result_appends":1,"retry":0,"fallback":0},"zero_budgets":{"extra_outer_git_invocations":0,"code_writes":0,"test_writes":0,"plan_writes_by_executer":0,"full_writes_by_executer":0,"archive_writes_by_executer":0,"debug_writes":0,"guide_writes":0,"research_writes":0,"tests":0,"compileall":0,"codegraph_sync":0,"git_stage":0,"git_commit":0,"old_failed_controller_reads":0,"old_failed_root_reads":0,"old_external_evidence_reads":0,"retained_artifact_reads":0,"candidate_payload_reads":0,"git_provenance_replay":0,"real_b2_dispatch":0,"subordinate_manifest_writes":0,"actual_canonical_validator_calls":0,"eligibility_emissions":0,"retained_release_audit":0,"release_generation":0,"release_qualification":0,"release_copy":0,"release_consumption":0,"network":0,"dns":0,"environment":0,"credentials":0,"device":0,"camera":0,"ray":0,"strip":0,"cleanup":0,"capture":0,"formal":0,"public_analyzer":0,"td_c":0,"sentinel":0,"p8":0,"firmware":0,"deployment":0},"expected_duration":"under_10_minutes","visible_terminal_required":false,"planner_stop":"B2_P4_C1_C1_C1_I1_C1_OUTER_PREFLIGHT_OWNER_CORRECTION_WAITING_PLANNER_REVIEW"}`

## 1. Activation and exact outer preflight owner

Activation 必须 exact 匹配 machine row，之后 worktree clean；FULL 只允许本 task/contract active，并保持 retained/candidate、Orchestrator
verification、Executer dispatch 与 device authorization fields exact。

Controller 外只允许 exact 一次：`git rev-parse HEAD`。要求 exit `0`、stderr empty、stdout 为 activation full SHA 加单一 newline；去掉该 newline
后必须是 40 位小写 hex。该 stdout 是 activation full SHA 的唯一 outer source，取前七位生成两个 fresh path。禁止 controller 外执行第二 Git
command、Git library、subprocess Git、`git show`、`git diff-tree`、blob lookup、parent/subject/path inspection 或 topology freeze。任一 outer failure
立即 stop，source/root/process attempts 全零。

两个 fresh paths 必须 absent、parent exact `/Volumes/4T/temp/rgbww-optimizer`、不得 symlink/escape。Source 以
`O_CREAT|O_EXCL|O_NOFOLLOW` 创建一次、mode `0600`，accepted `read_exact_file` 读取一次；同一 bytes 完成 strict UTF-8、AST parse、builtin
compile 与唯一 process dispatch。Root 只由 accepted `create_exclusive_root` 创建一次、mode `0700`。

## 2. Repo-owned conformance and unchanged transport contract

Lifecycle `conformance` callback 对 exact dispatched bytes 调用既有 `analyze_controller_source` exact once。External source/launcher/postflight
不得实现 AST walker/classifier，不得调用 `ast.walk` 再判 transport，只消费 immutable `ControllerConformanceReport.transport`。

要求 source SHA、owner fields/public methods、bound results exact `18`；effect/fixture domains 来自 embedded report；
`effect_transport_uses == ()`。Effect identities 必须 unique direct binding，跨 callback 只用 explicit enclosing direct names + `nonlocal`；direct
binding 后仅 inline 读取 accepted fields 并构造 plain dict。禁止先进入 tuple/list/dict/set、generic projection helper、alias、callback/closure return。
唯一 live grouping exception 是 exact
`RootIdentityChain(before=<direct root>, files=(<direct files>...), after=<direct root>)` 加 direct
`validate_root_identity_chain`。Opaque terminal gate 只以原 direct name 传给 admission，不得反射、序列化、读属性、alias或入 container。

Negative fixtures 只作为独立 bytes 传同一 repo analyzer；不得拼入/exec actual source。Conformance failure 是 pre-effect hard failure：controller
内 Git6、root、inputs、evaluate、terminal、seal、admission attempts 全 `0`，process nonzero，retry/fallback/second source/root/process `0`。

## 3. Controller-owned exact Git6 and same-root four reads

Conformance 通过后，同一 controller 的 activation callback 才调用 accepted `run_read_only_git` exact six times，repo cwd exact：

1. `git rev-parse --verify <activation-full-sha>^{commit}`；
2. `git show -s --format=%H%x00%P%x00%s <activation-full-sha>`；
3. `git diff-tree --no-commit-id --name-only -r -z <activation-full-sha>`；
4. `git rev-parse <activation-full-sha>:.agent-work/FULL_PLAN_REFERENCE.md`；
5. `git rev-parse <activation-full-sha>:.agent-work/PLAN.md`；
6. `git rev-parse <activation-full-sha>:.agent-work/PLANS/20260731-1410-p7-retained-r3-b2-p4-c1-c1-c1-i1-outer-git-failure-review.md`。

Git6 必须证明 activation exact full SHA、direct parent、subject、exact three changed paths，以及三 blobs 对应 runtime activation files；每个
`GitLedger` 独立 direct-bind，`exit_code==0`、stderr empty、stdout exact，并立即 inline plain projection。禁止 `returncode`、live ledger
collection、generic helper 或 retained provenance replay。Outer HEAD 不计入 Git6；Git6 也不得在 controller 外提前执行。

Root callback 后 exclusive 写 exact four inputs：`synthetic-plan.json`、`synthetic-full.json`、`synthetic-lineage.json`、
`synthetic-seal.json`。Payload 只含 fixed synthetic fields。每个由 accepted `read_exact_file(..., root=<same direct live root>)` exact once；
构造并 validate 唯一 exact RootIdentityChain。禁止额外 lstat/read/count probe。

## 4. Unchanged exact 16-case semantic matrix

Evaluate callback 必须运行 exact `16/16`，每个 negative 匹配 exact stable code/exception identity：

1. actual source analyzer positive：SHA、18 bindings、embedded transport、effect transport empty；
2. `GitLedger.exit_code` positive；
3. `GitLedger.returncode` → `git_returncode_rejected`；
4. unknown owner attribute/unbound result negative；
5. alias/reflection/opaque introspection negative；
6. rootless read negative；
7. literal-root read negative；
8. different-live-root read negative；
9. actual four-file root chain positive；
10. pre/post root drift → `root_identity_drift`；
11. pure in-memory `FileIdentity(root=drift_root)` mismatch → `file_root_mismatch`，repo report classifies fixture edge；
12. non-direct-child/sibling escape → `file_not_direct_child`；
13. file device drift → `file_device_mismatch`；
14. file mode drift → `file_mode_mismatch`；
15. primary-failure lifecycle after valid admission preserves original exception identity；
16. terminal/seal failure blocks admission and returns accepted stable lifecycle code。

Matrix 外不得加 case、test、probe、manual fix、second owner 或 classifier。任一失败走 sealed primary failure，retry/fallback `0`。

## 5. Exact9 and lifecycle contract

成功 root 最终只能依序包含 machine row exact9。所有 canonical JSON、mode `0600`、same-root direct child，并记录 physical identity。
Qualification seal 绑定 qualification identity；terminal target 绑定 qualification identity；terminal seal 绑定 terminal identity；opaque gate 只传给
admission，admission 只记录 plain identities。

Success order exact：`conformance, activation, root, inputs, evaluate, terminal, terminal_seal, admission`。只有
`activation/root/inputs/evaluate` 为 sealed primary phases。Primary failure 后 terminal attempt `1`；terminal success 后 seal `1`；seal success 后
admission `1`；valid FAIL admission 后重新抛 original primary。Terminal/seal failure 阻止 admission 并保存双 failure identity。

Process terminal 后只读核对 exact9、strict JSON/hash/linkage/root identities、source/root identity、outer HEAD `1/1`、extra outer `0`、controller
Git6、matrix16、lifecycle/counters 与 exit。Executer最终只 append ER once；不得修改旧 ER。最终 porcelain 只能 ER 一个 unstaged modification。

## 6. Acceptance, failure branches, locks and stop

Acceptance 要求一个 outer HEAD、零额外 outer Git；一个 fresh source/root/process；source one-write/one-read；repo analyzer once、external classifier
zero；18 bindings、embedded transport/effect empty；direct/nonlocal bindings、inline projection、RootIdentityChain；controller Git6；same-root reads4；
matrix16；exact9；terminal/seal/admission linkage；exit0；retry/fallback0；仅 ER append。

Preflight/source/conformance failure 时 root/artifacts absent，terminal attempts0。Activation/root/inputs/evaluate failure 保留已写 progressive evidence，
执行一次 fail terminal/seal/admission lifecycle并重抛 primary。Terminal/seal/admission failure 保留所有 physical evidence与 failure identities，
exit nonzero。禁止修复、删除、复用root、重跑或补造。

本包通过仅证明 repo-owned transport report 的 fresh synthetic integration。所有旧 source/root/evidence、retained R3/candidate、retained Git
replay、real B2、subordinate manifest、canonical validator、eligibility、retained audit、release、network、DNS、environment、credentials、device、
camera、Ray、strip、cleanup、capture、FORMAL、public analyzer、TD-C、sentinel、P8、firmware、deployment hard locked `0`。所有分支在唯一 Planner
stop 结束。

维护性判断：只纠正 disposable outer preflight ownership；不改 repo code/test，不新增 analyzer、transport classifier、provenance owner 或 lifecycle
framework，原科学与 evidence contracts 完整保留。
