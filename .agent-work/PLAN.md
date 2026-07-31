# REF-P7-25-R2-B2-P4-C1-C1-C1-I1-C1-C1-C1-C1：outer launcher argument correction

**计划状态：** `WAITING_ORCHESTRATOR_ACTIVATION`

**Planner 日期：** `2026-07-31`

**Reference task：** `REF-P7-25-R2-B2-P4-C1-C1-C1-I1-C1-C1-C1-C1`

**Contract ID：**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-P4-C1-C1-C1-I1-C1-C1-C1-C1-LAUNCHER-ARGUMENT-CORRECTION-V1`

**Planner decision：** evidence commit
`62f91f431bcf38a4f100ae53567db8e40f94dc65` 被拒绝为
`REJECTED_OUTER_LAUNCHER_MUTUALLY_EXCLUSIVE_STDIN_INPUT`。唯一 controller dispatch 在 process 创建前因
`subprocess.run` 同时传入 `stdin` 与 `input` 而抛出 `ValueError`；不接受 synthetic integration，不消费 retained R3，
不解锁任何后续阶段。

**当前唯一动作：** Orchestrator 审核本 PLAN、更新 FULL，并以
`62f91f431bcf38a4f100ae53567db8e40f94dc65` 为 direct parent 创建 exact activation commit。Activation 后，Executer
从新的 activation HEAD 派生唯一 fresh source/root，仅把 launcher 改为
`subprocess.run(..., input=<exact frozen source bytes>, ...)` 且完全不传 `stdin`；首命令、source 生命周期、
machine-row、repo analyzer、Git6、same-root、matrix16、exact9 与 failure lifecycle 合同保持不变。

**唯一 Planner stop：**
`B2_P4_C1_C1_C1_I1_C1_C1_C1_C1_LAUNCHER_ARGUMENT_CORRECTION_WAITING_PLANNER_REVIEW`。

**本轮新归档：**
`.agent-work/PLANS/20260731-1457-p7-retained-r3-b2-p4-c1-c1-c1-i1-c1-c1-c1-launcher-argument-failure-review.md`；
activation 前由 Orchestrator 记录其 final bytes/SHA-256 到 FULL/commit handoff。

`PLAN_MACHINE_CONTRACT={"schema":"p7_td_b_retained_r3_option_b_b2_p4_c1_c1_c1_i1_c1_c1_c1_c1_launcher_argument_correction_v1","reference_task_id":"REF-P7-25-R2-B2-P4-C1-C1-C1-I1-C1-C1-C1-C1","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-P4-C1-C1-C1-I1-C1-C1-C1-C1-LAUNCHER-ARGUMENT-CORRECTION-V1","execution_authorized_after_orchestrator_activation":true,"activation_commit":{"expected_parent":"62f91f431bcf38a4f100ae53567db8e40f94dc65","expected_subject":"chore(plan): correct p4 launcher arguments","expected_changed_paths":[".agent-work/FULL_PLAN_REFERENCE.md",".agent-work/PLAN.md",".agent-work/PLANS/20260731-1457-p7-retained-r3-b2-p4-c1-c1-c1-i1-c1-c1-c1-launcher-argument-failure-review.md"],"clean_porcelain_required_after_activation":true},"required_full_machine_state":{"active_task_count":1,"active_task":"REF-P7-25-R2-B2-P4-C1-C1-C1-I1-C1-C1-C1-C1","active_plan_contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-P4-C1-C1-C1-I1-C1-C1-C1-C1-LAUNCHER-ARGUMENT-CORRECTION-V1","retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","candidate_machine_contract_sha256":"96ece8940a82d53ff6e61b8b2e0ecb4f0cb01d93770ce5a992942c2464ab449a","candidate_contract_orchestrator_verified":true,"executer_dispatched":true,"device_authorized_by_this_file":false},"accepted_transport_owner":{"implementation_commit":"0ec12f2de91b84f4379d64437170fa53c3ae4a28","source_sha256":"6e10594165016a06da462e74a9deb2d9817fd95fe1417addb7a5d26c55996745","test_sha256":"e3c4a421e691c3aaac182edc6a0963a16caea95ae04f25a68493f96277bddb72","expected_bound_results":18,"embedded_transport_report":true,"effect_transport_uses":0},"fresh_paths":{"activation_short_sha_source":"outer_head_stdout_first_seven_hex","controller_source_template":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-p4-c1-c1-c1-i1-c1-c1-c1-c1-controller-{activation_short_sha}.py","output_root_template":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-p4-c1-c1-c1-i1-c1-c1-c1-c1-qualification-{activation_short_sha}","must_be_absent_before_start":true,"source_mode":"0600","root_mode":"0700"},"launcher_contract":{"process_api":"subprocess.run","input_bytes":"exact_frozen_source_bytes","stdin_argument_present":false,"pre_dispatch_pure_in_memory_assertions":1,"assertion_requires_process":false,"assertion_requires_source_read":false,"controller_processes":1},"machine_row_contract":{"strategy":"exact_markdown_delimiter_strip","plan_marker_ascii":"`PLAN_MACHINE_CONTRACT=","full_marker_ascii":"`FULL_PLAN_MACHINE_STATE=","required_suffix_ascii":"`\n","candidate_count_each":1,"strict_utf8":true,"strict_json":true,"generic_parser":false,"repo_parser_calls":0,"owner_binding_delta":0,"source_writer_json_import":true,"source_writer_report_required":true},"controller_contract":{"source_create_once":true,"source_read_once":true,"strict_utf8_ast_compile":true,"controller_processes":1,"actual_runtime_source_analyzer_calls":1,"external_transport_ast_classifier_calls":0,"expected_bound_results":18,"effect_transport_uses_on_pass":0,"outer_git_invocations":1,"outer_git_argv":["/usr/bin/git","rev-parse","HEAD"],"outer_first_external_command_required":true,"outer_generic_worktree_preflight_allowed":false,"controller_activation_git_ledgers":6,"git_success_field":"exit_code","runtime_returncode_uses":0,"root_create_once":true,"synthetic_inputs":4,"semantic_matrix_cases":16,"same_root_reads":4,"exact_artifact_names":["synthetic-plan.json","synthetic-full.json","synthetic-lineage.json","synthetic-seal.json","integration-qualification.json","integration-qualification.sha256.json","terminal-evidence.json","terminal-evidence.sha256.json","execution-result-admission.json"],"final_root_file_count":9,"pre_root_primary_machine_json":true,"pre_root_target_reads":0,"pre_root_file_writes":0,"pre_root_original_primary_rethrown":true,"retry":0,"fallback":0,"second_source":0,"second_root":0,"second_process":0},"execution_budgets":{"outer_read_only_git_invocations":1,"controller_read_only_git_invocations":6,"controller_source_writes":1,"controller_source_reads":1,"launcher_in_memory_assertions":1,"controller_processes":1,"output_roots":1,"synthetic_input_writes":4,"qualification_writes":2,"terminal_writes":2,"admission_writes":1,"execution_result_appends":1,"retry":0,"fallback":0},"zero_budgets":{"extra_outer_git_invocations":0,"launcher_stdin_arguments":0,"launcher_second_input_channels":0,"launcher_assertion_processes":0,"launcher_assertion_source_reads":0,"code_writes":0,"test_writes":0,"plan_writes_by_executer":0,"full_writes_by_executer":0,"archive_writes_by_executer":0,"debug_writes":0,"guide_writes":0,"research_writes":0,"tests":0,"compileall":0,"codegraph_sync":0,"git_stage":0,"git_commit":0,"generic_machine_row_parser":0,"repo_machine_parser_calls":0,"old_failed_controller_reads":0,"old_failed_root_reads":0,"old_external_evidence_reads":0,"retained_artifact_reads":0,"candidate_payload_reads":0,"git_provenance_replay":0,"real_b2_dispatch":0,"subordinate_manifest_writes":0,"actual_canonical_validator_calls":0,"eligibility_emissions":0,"retained_release_audit":0,"release_generation":0,"release_qualification":0,"release_copy":0,"release_consumption":0,"network":0,"dns":0,"environment":0,"credentials":0,"device":0,"camera":0,"ray":0,"strip":0,"cleanup":0,"capture":0,"formal":0,"public_analyzer":0,"td_c":0,"sentinel":0,"p8":0,"firmware":0,"deployment":0},"expected_duration":"under_10_minutes","visible_terminal_required":false,"planner_stop":"B2_P4_C1_C1_C1_I1_C1_C1_C1_C1_LAUNCHER_ARGUMENT_CORRECTION_WAITING_PLANNER_REVIEW"}`

## 1. Activation、fresh paths 与 immutable old attempts

Activation commit 必须满足 machine row 的 direct parent、subject、exact three paths，之后 porcelain clean。FULL 只允许本 task/contract
active，保持 retained `RETAINED_UNVALIDATED_UNCONSUMED`、candidate hash/verification、Executer dispatch true 与 device authorization false。

Executer 接手后不得先执行通用 worktree preflight。第一条 tool call/外部命令必须且只能是绝对路径
`/usr/bin/git rev-parse HEAD`；它也是 controller 外唯一 Git invocation。禁止额外 outer Git、shell/Python/file/process probe。
命令须 exit `0`、stderr empty、stdout 为 activation full SHA 加单一 LF；其前七位派生本 successor 的 fresh source/root。

Fresh source/root 必须 absent、位于 exact temp parent、不得 symlink/escape。Source exclusive
`O_CREAT|O_EXCL|O_NOFOLLOW`、mode `0600`、write/fsync/stat once；writer 显式 import `json` 并输出 strict JSON success report。
accepted `read_exact_file` 对 source exact once；同一 in-memory bytes 完成 strict UTF-8、AST、builtin compile 与唯一 dispatch。Root 由
accepted `create_exclusive_root` once、mode `0700`。

所有旧 I1 系列 source/root/evidence，包括冻结 `8acaaf6` source
(bytes `35425`、SHA-256 `95c6e4cab1b53cb833a71b3a379c806a7c4c9751dd9bc314854904161039349b`)
和未创建 root，均不得读、探测、修复、删除、复用或 rerun。Successor suffix 只能来自新 activation HEAD。

## 2. 唯一 launcher correction

Source read/UTF-8/AST/compile 成功后，outer launcher 构造唯一 dispatch kwargs。必须满足：

- 传入 `input=<exact frozen source bytes>`；
- kwargs 中 `stdin` key 完全 absent；不得传 `stdin=None` 或 `stdin=PIPE`；
- 不得增加 pipe、file redirect、`Popen`、`communicate`、shell 或第二 input channel；
- command、cwd、environment、capture、timeout、check/return handling 均沿用被拒包，不做其他变化；
- 只创建一个 controller process，retry/fallback/second process `0`。

Dispatch 前执行 exact one 纯内存 assertion：对即将传入的 kwargs 证明 `input` present、值 identity/equality 为 frozen
source bytes，且 `stdin` absent；另以纯 mapping negative fixture 证明 simultaneous `stdin`+`input` 被该 assertion 拒绝。该 assertion
不得调用 subprocess、不得创建 process、不得读 source、不得写文件或改变计数。真实 dispatch 的 kwargs 必须是 assertion 检查的同一 mapping。
若 assertion fail，按 pre-root structured failure lifecycle fail closed，不得 dispatch。

## 3. Frozen row、analyzer、Git6、root/matrix/artifacts

Fresh controller 对 PLAN/FULL exact bytes各只接受一条 exact Markdown machine row：leading exact marker、trailing exact
backtick+LF、禁止 CRLF；只剥离 exact prefix/suffix，再做 strict UTF-8 与 duplicate-key/nonfinite rejecting JSON object parse。Bare marker、
missing/extra backtick、multiple candidate、wrong LF、malformed JSON stable fail；generic parser/repo parser calls `0`。

Lifecycle conformance 对 dispatched source bytes调用既有 `analyze_controller_source` exact once；external classifier `0`。Public methods、bound
results exact `18`、embedded transport report、effect/fixture domains、effect transport empty不变。Effect identity只 direct binding；禁止 collection、
generic projection、alias、callback return；唯一 grouping 仍 exact `RootIdentityChain` + direct validator。Conformance fail 是 pre-effect hard failure。

Conformance pass 后才运行 accepted `run_read_only_git` exact six，使用 `GitLedger.exit_code`，证明 successor activation full SHA、parent
`62f91f431bcf38a4f100ae53567db8e40f94dc65`、subject
`chore(plan): correct p4 launcher arguments`、exact FULL/PLAN/review-archive paths及其 blob OIDs；controller 内 Git6之外不得增加 Git。

Root 后写/read same-root exact four inputs；构造/validate唯一 RootIdentityChain。Evaluate exact `16/16` frozen cases不增减：
actual source；GitLedger positive/`returncode` reject；unknown owner/unbound；alias/reflection/opaque；rootless/literal/different live root；
actual four-file chain；root drift；pure in-memory mismatch fixture；child escape；device/mode drift；original primary identity；terminal/seal blocks
admission。Negative 匹配原 stable code/exception identity。

Success root最终 exact9，canonical JSON/mode `0600`/direct same-root child、physical identity/hash/linkage 全部核对。Success order仍
`conformance, activation, root, inputs, evaluate, terminal, terminal_seal, admission`；primary phases仅
`activation/root/inputs/evaluate`。最终 postflight 核对 exact9、source/root identity、outer HEAD `1/1`、extra outer `0`、Git6、
matrix16、lifecycle/counters/exit0；仅 append ER once。

## 4. Frozen failure lifecycle

Source、launcher assertion、conformance或activation的 pre-root failure须在 memory 冻结 canonical plain mapping：schema、phase、primary fully
qualified type、stable code、可用的 repo machine-contract evidence、root_created false、qualification_target_present false、retry/fallback
`0/0`。禁止 repr/traceback/secrets。

Terminal callback 在 primary non-null 且 root/target absent 时只返回 in-memory primary envelope，不读 target、不写 terminal、不抛
`qualification_target_missing`；terminal-seal/admission只返回 in-memory FAIL mappings，文件写 `0`；随后重抛 exact original primary。
Top-level catch输出 exact one `CONTROLLER_PRIMARY_FAILURE_JSON=` canonical line 后 nonzero。若 root 已创建，沿用原 progressive physical
evidence/file-based terminal contract。任何 failure都不得 repair/delete/reuse/rerun。

## 5. Acceptance、locks 与 stop

Acceptance 要求：activation exact；outer first command exact；fresh source/root absent→once；writer report；source read once；UTF-8/AST/compile；
launcher pure assertion `1`、assertion process/read `0/0`、`input` bytes且 `stdin` absent；controller process `1`；row exact；
repo analyzer `1`、external classifier `0`、18 bindings/effect empty；Git6；same-root4；matrix16；exact9；terminal/seal/admission linkage；
exit0；retry/fallback/second source/root/process `0`；repo仅 ER one append。

若真实 launcher仍在 controller process前失败，必须冻结 source identity和 exact Python exception/code，并立即 stop；不得用第二种 launcher
API fallback。若 controller已创建，则其 failure按第4节处理。所有分支均停在唯一 Planner stop。

旧 source/root/evidence、retained R3/candidate、Git provenance replay、real B2、subordinate manifest、actual canonical validator、eligibility、
retained audit、release、network、DNS、environment、credentials、device、camera、Ray、strip、cleanup、capture、FORMAL、public analyzer、
TD-C、sentinel、P8、firmware、deployment hard locked `0`。不运行 tests、compileall、CodeGraph；不改 code/test/FULL/PLAN/archive/debug/
GUIDE/RESEARCH；不 stage/commit。

维护性判断：successor 只纠正一次性外部 launcher kwargs，并用不产生 side effect 的本地 assertion 固化互斥条件；不改变 repo-owned analyzer、
machine-row、Git6、root、matrix、artifact或failure owner，不新增生产抽象或平行执行框架。
