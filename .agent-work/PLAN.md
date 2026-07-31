# REF-P7-25-R2-B2-P4-C1-C1-C1-I1-C1-C1-C1-C1-C1：runtime-token fixture separation correction

**计划状态：** `WAITING_ORCHESTRATOR_ACTIVATION`

**Planner 日期：** `2026-07-31`

**Reference task：** `REF-P7-25-R2-B2-P4-C1-C1-C1-I1-C1-C1-C1-C1-C1`

**Contract ID：**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-P4-C1-C1-C1-I1-C1-C1-C1-C1-C1-RUNTIME-TOKEN-FIXTURE-SEPARATION-CORRECTION-V1`

**Planner decision：** evidence commit
`b28d5377682c0f2da71ecb078d1817591f6d19c3` 被拒绝为
`REJECTED_SELF_REFERENTIAL_FORBIDDEN_TOKEN_MATRIX_CHECK`。Launcher single-input contract 已通过，但 controller matrix 对
`RUNTIME_SOURCE_BYTES` 搜索 literal `.returncode`，同时该 literal 正由检查表达式自身写入相同 source bytes，导致 self-referential false。
Root 与 4 个 synthetic inputs 不构成 qualification；不接受 integration，不消费 retained R3，不解锁任何后续阶段。

**当前唯一动作：** Orchestrator 审核本 PLAN、更新 FULL，并以
`b28d5377682c0f2da71ecb078d1817591f6d19c3` 为 direct parent 创建 exact activation commit。Activation 后，Executer
从新的 activation HEAD 派生唯一 fresh source/root，仅纠正 matrix negative-token fixture：negative fixture/token construction 与
actual runtime-source scan 必须分离，不得让被搜索的 exact forbidden token literal 自身出现在受检 runtime bytes，也不得新增第二 classifier、
generic allowlist 或改动 repo owner。首命令、launcher、source lifecycle、machine-row、repo analyzer、Git6、same-root、matrix16、exact9 与
failure lifecycle 均冻结不变。

**唯一 Planner stop：**
`B2_P4_C1_C1_C1_I1_C1_C1_C1_C1_C1_RUNTIME_TOKEN_FIXTURE_SEPARATION_WAITING_PLANNER_REVIEW`。

**本轮新归档：**
`.agent-work/PLANS/20260731-1508-p7-retained-r3-b2-p4-c1-c1-c1-i1-c1-c1-c1-c1-matrix-self-reference-failure-review.md`；
activation 前由 Orchestrator 记录其 final bytes/SHA-256 到 FULL/commit handoff。

`PLAN_MACHINE_CONTRACT={"schema":"p7_td_b_retained_r3_option_b_b2_p4_c1_c1_c1_i1_c1_c1_c1_c1_c1_runtime_token_fixture_separation_correction_v1","reference_task_id":"REF-P7-25-R2-B2-P4-C1-C1-C1-I1-C1-C1-C1-C1-C1","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-P4-C1-C1-C1-I1-C1-C1-C1-C1-C1-RUNTIME-TOKEN-FIXTURE-SEPARATION-CORRECTION-V1","execution_authorized_after_orchestrator_activation":true,"activation_commit":{"expected_parent":"b28d5377682c0f2da71ecb078d1817591f6d19c3","expected_subject":"chore(plan): correct p4 runtime token fixture","expected_changed_paths":[".agent-work/FULL_PLAN_REFERENCE.md",".agent-work/PLAN.md",".agent-work/PLANS/20260731-1508-p7-retained-r3-b2-p4-c1-c1-c1-i1-c1-c1-c1-c1-matrix-self-reference-failure-review.md"],"clean_porcelain_required_after_activation":true},"required_full_machine_state":{"active_task_count":1,"active_task":"REF-P7-25-R2-B2-P4-C1-C1-C1-I1-C1-C1-C1-C1-C1","active_plan_contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-P4-C1-C1-C1-I1-C1-C1-C1-C1-C1-RUNTIME-TOKEN-FIXTURE-SEPARATION-CORRECTION-V1","retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","candidate_machine_contract_sha256":"96ece8940a82d53ff6e61b8b2e0ecb4f0cb01d93770ce5a992942c2464ab449a","candidate_contract_orchestrator_verified":true,"executer_dispatched":true,"device_authorized_by_this_file":false},"accepted_transport_owner":{"implementation_commit":"0ec12f2de91b84f4379d64437170fa53c3ae4a28","source_sha256":"6e10594165016a06da462e74a9deb2d9817fd95fe1417addb7a5d26c55996745","test_sha256":"e3c4a421e691c3aaac182edc6a0963a16caea95ae04f25a68493f96277bddb72","expected_bound_results":18,"embedded_transport_report":true,"effect_transport_uses":0},"fresh_paths":{"activation_short_sha_source":"outer_head_stdout_first_seven_hex","controller_source_template":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-p4-c1-c1-c1-i1-c1-c1-c1-c1-c1-controller-{activation_short_sha}.py","output_root_template":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-p4-c1-c1-c1-i1-c1-c1-c1-c1-c1-qualification-{activation_short_sha}","must_be_absent_before_start":true,"source_mode":"0600","root_mode":"0700"},"launcher_contract":{"process_api":"subprocess.run","input_bytes":"exact_frozen_source_bytes","stdin_argument_present":false,"pre_dispatch_pure_in_memory_assertions":1,"controller_processes":1},"matrix_token_contract":{"runtime_scan_owner":"existing_repo_analyze_controller_source","negative_fixture_separate_from_runtime_source":true,"exact_forbidden_attribute":"returncode","literal_forbidden_token_in_runtime_source":false,"second_classifier":false,"generic_allowlist":false,"ast_attribute_check_via_repo_owner_allowed":true},"controller_contract":{"source_create_once":true,"source_read_once":true,"strict_utf8_ast_compile":true,"controller_processes":1,"actual_runtime_source_analyzer_calls":1,"external_transport_ast_classifier_calls":0,"expected_bound_results":18,"effect_transport_uses_on_pass":0,"outer_git_invocations":1,"outer_git_argv":["/usr/bin/git","rev-parse","HEAD"],"outer_first_external_command_required":true,"outer_generic_worktree_preflight_allowed":false,"controller_activation_git_ledgers":6,"git_success_field":"exit_code","runtime_returncode_uses":0,"root_create_once":true,"synthetic_inputs":4,"semantic_matrix_cases":16,"same_root_reads":4,"exact_artifact_names":["synthetic-plan.json","synthetic-full.json","synthetic-lineage.json","synthetic-seal.json","integration-qualification.json","integration-qualification.sha256.json","terminal-evidence.json","terminal-evidence.sha256.json","execution-result-admission.json"],"final_root_file_count":9,"retry":0,"fallback":0,"second_source":0,"second_root":0,"second_process":0},"immutable_failure_evidence":{"evidence_commit":"b28d5377682c0f2da71ecb078d1817591f6d19c3","execution_result_blob_oid":"11b64d14a16c7d3e4a909892467b7f46b6295ef0","execution_result_sha256":"a86d222a6cc6ae6dd59609c8fd36da343eb42dd9213cf63b867dabb216ba39e1","malformed_heading_prefix":"literal_backslash_n_plus_before_markdown_heading","old_line_edits":0,"successor_truthful_supersession_append_required":true},"execution_budgets":{"outer_read_only_git_invocations":1,"controller_source_writes":1,"controller_source_reads":1,"launcher_in_memory_assertions":1,"controller_processes":1,"output_roots":1,"synthetic_input_writes":4,"qualification_writes":2,"terminal_writes":2,"admission_writes":1,"execution_result_appends":1,"retry":0,"fallback":0},"zero_budgets":{"extra_outer_git_invocations":0,"launcher_stdin_arguments":0,"second_classifier":0,"generic_allowlist":0,"old_execution_result_line_edits":0,"code_writes":0,"test_writes":0,"plan_writes_by_executer":0,"full_writes_by_executer":0,"archive_writes_by_executer":0,"debug_writes":0,"tests":0,"compileall":0,"codegraph_sync":0,"git_stage":0,"git_commit":0,"old_failed_controller_reads":0,"old_failed_root_reads":0,"old_external_evidence_reads":0,"retained_artifact_reads":0,"candidate_payload_reads":0,"git_provenance_replay":0,"real_b2_dispatch":0,"subordinate_manifest_writes":0,"actual_canonical_validator_calls":0,"eligibility_emissions":0,"retained_release_audit":0,"release_generation":0,"release_qualification":0,"release_copy":0,"release_consumption":0,"network":0,"dns":0,"environment":0,"credentials":0,"device":0,"camera":0,"ray":0,"strip":0,"cleanup":0,"capture":0,"formal":0,"public_analyzer":0,"td_c":0,"sentinel":0,"p8":0,"firmware":0,"deployment":0},"expected_duration":"under_10_minutes","visible_terminal_required":false,"planner_stop":"B2_P4_C1_C1_C1_I1_C1_C1_C1_C1_C1_RUNTIME_TOKEN_FIXTURE_SEPARATION_WAITING_PLANNER_REVIEW"}`

## 1. Activation、first command 与 immutable old attempts

Activation commit 必须满足 machine row 的 direct parent、subject、exact three paths，之后 porcelain clean。FULL 只允许本 task/contract
active，保持 retained `RETAINED_UNVALIDATED_UNCONSUMED`、candidate hash/verification、Executer dispatch true 与 device authorization false。

Executer 接手后不得先执行通用 worktree preflight。第一条 tool call/外部命令必须且只能是绝对路径
`/usr/bin/git rev-parse HEAD`；它也是 controller 外唯一 Git invocation。命令须 exit `0`、stderr empty、stdout activation full SHA 加单一 LF；
其前七位派生本 successor 的 fresh source/root。Fresh paths 必须 initially absent、exact temp parent、不得 symlink/escape。

所有旧 I1 系列 source/root/evidence 均不得读、探测、修复、删除、复用或 rerun，特别包括刚失败的
`...c1-c1-c1-c1-controller-e400262.py` 与 matching root。Committed ER 的 malformed `\\n+##` prefix 与此前全部 bytes immutable；
不得为了 Markdown 外观修复旧行。Successor 最后仅 append 新 section，明确该新 heading 才是 authoritative successor handoff，并说明旧 prefix
保留仅为 immutable failure evidence。

## 2. 唯一 runtime-token fixture correction

Outer source writer、accepted read、strict UTF-8、AST、builtin compile、single-input launcher assertion 与唯一 `subprocess.run` dispatch 沿用已通过合同：
真实 mapping 仅 `input=<exact frozen source bytes>`，`stdin` key absent；controller process exact `1`。

只允许纠正 `git_returncode_rejected` matrix case 的 token self-reference：

- negative fixture/token 必须在不属于 `RUNTIME_SOURCE_BYTES` 的数据域中构造；若需要 exact `.returncode` fixture，必须由 runtime 外的 fragments
  组合，或由既有 repo owner 的 AST attribute result表达，不得把 literal forbidden token写回待扫描 source；
- actual runtime-source 的判断继续由既有 `analyze_controller_source` 唯一 owner完成；controller消费其 structured report/bindings，不得实现第二套
  AST walker、regex/string classifier、path allowlist、attribute allowlist或 generic transport classifier；
- matrix positive/negative语义保持：runtime使用 `GitLedger.exit_code`，runtime `returncode` uses exact `0`，专门 negative fixture仍必须稳定 reject；
- correction 不得减少、合并、重命名或跳过任何 matrix case；semantic matrix仍 exact `16/16`。

若为了避免 literal 自引用而隐藏、编码或宽化 token，使实际 `.returncode` 行为不能由 repo owner拒绝，则 fail closed；不得以通过 string check
替代 repo owner analysis。

## 3. Frozen owner、Git6、root、matrix 与 exact9

Machine-row exact Markdown delimiter strip、strict UTF-8/JSON、duplicate/nonfinite rejection保持。Dispatched source bytes调用既有
`analyze_controller_source` exact once；external classifier `0`；public methods/bound results exact `18`；embedded transport report、effect/fixture
domains、effect transport empty保持。Effect identity只 direct binding；唯一 grouping仍 exact `RootIdentityChain` + direct validator。

Conformance pass 后运行 accepted `run_read_only_git` exact six，使用 `GitLedger.exit_code`，证明 successor activation full SHA、parent
`b28d5377682c0f2da71ecb078d1817591f6d19c3`、subject `chore(plan): correct p4 runtime token fixture`、exact FULL/PLAN/archive
paths与 blob OIDs。Controller 内 Git6之外不得增加 Git。

Root 由 accepted exclusive owner once 创建 mode `0700`；same-root 写/read exact four inputs，构造/validate唯一 RootIdentityChain。Evaluate exact
16 cases，包括 actual source、GitLedger positive、returncode negative、unknown/unbound、alias/reflection/opaque、rootless/literal/different live root、
actual four-file chain、root drift、pure in-memory mismatch fixture、child escape、device/mode drift、original primary identity、terminal/seal blocks admission。

Success root最终 exact9 canonical artifacts，regular/non-symlink/mode/hash/identity/linkage全核对。Success order仍
`conformance, activation, root, inputs, evaluate, terminal, terminal_seal, admission`；最终 postflight证明 analyzer18、Git6、same-root4、matrix16、
exact9、lifecycle/counters、exit0。Repository唯一写入是 ER EOF append once。

## 4. Failure lifecycle

Source、launcher assertion、conformance或activation pre-root failure冻结 canonical in-memory primary envelope，terminal callback不得用
`qualification_target_missing` 覆盖原 primary；top-level exact one `CONTROLLER_PRIMARY_FAILURE_JSON=` canonical line、无 traceback。Root已创建时沿用
progressive physical evidence/file-based terminal contract。任何 failure不 repair/delete/reuse/rerun。

若 matrix仍失败，必须报告 exact case、repo owner report与 stable primary code，保留 root/progressive artifacts，retry/fallback `0/0`并 stop。
若 success，terminal、terminal seal、admission必须按序落盘且 linkage一致；不得在成功前宣称 qualification。

## 5. Acceptance、locks 与 stop

Acceptance 要求：activation exact；first command exact；fresh source/root absent→once；source writer/read/UTF-8/AST/compile；single-input launcher；
controller process1；row exact；repo analyzer1、external classifier0、18 bindings/effect empty；negative fixture与 runtime bytes分域；literal forbidden token
不由 checker自写入受检 bytes；second classifier/allowlist0；Git6；same-root4；matrix16；exact9；terminal/seal/admission linkage；exit0；
retry/fallback/second source/root/process0；ER old bytes unchanged + truthful supersession append1。

旧 source/root/evidence、retained R3/candidate、Git provenance replay、real B2、subordinate manifest、actual canonical validator、eligibility、retained audit、
release、network、DNS、environment、credentials、device、camera、Ray、strip、cleanup、capture、FORMAL、public analyzer、TD-C、sentinel、P8、firmware、
deployment hard locked `0`。不运行 tests、compileall、CodeGraph；不改 code/test/FULL/PLAN/archive/debug/GUIDE/RESEARCH；不 stage/commit。

所有分支均停在唯一 Planner stop；本 PLAN 不授权 retained validation、release consumption、设备或 scientific stage。

维护性判断：本 successor只拆开一次性 matrix fixture 与受检 runtime-source 数据域，继续复用 repo-owned analyzer 作为唯一 source eligibility owner；
不新增 classifier、allowlist、生产抽象或并行 execution framework。
