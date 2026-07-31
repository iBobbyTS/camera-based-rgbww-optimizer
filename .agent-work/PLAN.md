# REF-P7-25-R2-B2-P4-C1-C1-C1-I1-C1-C1-C1：outer first-command execution correction

**计划状态：** `WAITING_ORCHESTRATOR_ACTIVATION`

**Planner 日期：** `2026-07-31`

**Reference task：** `REF-P7-25-R2-B2-P4-C1-C1-C1-I1-C1-C1-C1`

**Contract ID：**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-P4-C1-C1-C1-I1-C1-C1-C1-OUTER-FIRST-COMMAND-CORRECTION-V1`

**当前唯一动作：** Orchestrator 审核本 PLAN、更新 FULL，并以
`0e9af614ad6a3212f80d6f5bdbf1c16db768e18a` 为 direct parent 创建 exact activation commit。Activation 后，Executer 先以绝对路径执行唯一
`/usr/bin/git rev-parse HEAD`，且它必须是本包第一条外部命令；随后创建并运行唯一
fresh external controller/source/root/process；严格纠正 frozen machine-row Markdown delimiter，修复 fresh source writer report import，并使 pre-root
failure 产生 structured primary evidence 而不被 missing terminal target 遮蔽。

**唯一 Planner stop：**
`B2_P4_C1_C1_C1_I1_C1_C1_C1_OUTER_FIRST_COMMAND_CORRECTION_WAITING_PLANNER_REVIEW`。

**本轮新归档：**
`.agent-work/PLANS/20260731-1436-p7-retained-r3-b2-p4-c1-c1-c1-i1-c1-c1-outer-status-violation-review.md`；activation 前由
Orchestrator 记录其 final bytes/SHA-256 到 FULL/commit handoff。

`PLAN_MACHINE_CONTRACT={"schema":"p7_td_b_retained_r3_option_b_b2_p4_c1_c1_c1_i1_c1_c1_c1_outer_first_command_correction_v1","reference_task_id":"REF-P7-25-R2-B2-P4-C1-C1-C1-I1-C1-C1-C1","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-P4-C1-C1-C1-I1-C1-C1-C1-OUTER-FIRST-COMMAND-CORRECTION-V1","execution_authorized_after_orchestrator_activation":true,"activation_commit":{"expected_parent":"0e9af614ad6a3212f80d6f5bdbf1c16db768e18a","expected_subject":"chore(plan): enforce p4 outer first command","expected_changed_paths":[".agent-work/FULL_PLAN_REFERENCE.md",".agent-work/PLAN.md",".agent-work/PLANS/20260731-1436-p7-retained-r3-b2-p4-c1-c1-c1-i1-c1-c1-outer-status-violation-review.md"],"clean_porcelain_required_after_activation":true},"required_full_machine_state":{"active_task_count":1,"active_task":"REF-P7-25-R2-B2-P4-C1-C1-C1-I1-C1-C1-C1","active_plan_contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-P4-C1-C1-C1-I1-C1-C1-C1-OUTER-FIRST-COMMAND-CORRECTION-V1","retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","candidate_machine_contract_sha256":"96ece8940a82d53ff6e61b8b2e0ecb4f0cb01d93770ce5a992942c2464ab449a","candidate_contract_orchestrator_verified":true,"executer_dispatched":true,"device_authorized_by_this_file":false},"accepted_transport_owner":{"implementation_commit":"0ec12f2de91b84f4379d64437170fa53c3ae4a28","source_sha256":"6e10594165016a06da462e74a9deb2d9817fd95fe1417addb7a5d26c55996745","test_sha256":"e3c4a421e691c3aaac182edc6a0963a16caea95ae04f25a68493f96277bddb72","expected_bound_results":18,"embedded_transport_report":true,"effect_transport_uses":0},"fresh_paths":{"activation_short_sha_source":"outer_head_stdout_first_seven_hex","controller_source_template":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-p4-c1-c1-c1-i1-c1-c1-c1-controller-{activation_short_sha}.py","output_root_template":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-p4-c1-c1-c1-i1-c1-c1-c1-qualification-{activation_short_sha}","must_be_absent_before_start":true,"source_mode":"0600","root_mode":"0700"},"machine_row_contract":{"strategy":"exact_markdown_delimiter_strip","plan_marker_ascii":"`PLAN_MACHINE_CONTRACT=","full_marker_ascii":"`FULL_PLAN_MACHINE_STATE=","required_suffix_ascii":"`\\n","candidate_count_each":1,"strict_utf8":true,"strict_json":true,"generic_parser":false,"repo_parser_calls":0,"owner_binding_delta":0,"source_writer_json_import":true,"source_writer_report_required":true},"controller_contract":{"source_create_once":true,"source_read_once":true,"strict_utf8_ast_compile":true,"controller_processes":1,"actual_runtime_source_analyzer_calls":1,"external_transport_ast_classifier_calls":0,"expected_bound_results":18,"effect_transport_uses_on_pass":0,"outer_git_invocations":1,"outer_git_argv":["/usr/bin/git","rev-parse","HEAD"],"outer_first_external_command_required":true,"outer_generic_worktree_preflight_allowed":false,"controller_activation_git_ledgers":6,"git_success_field":"exit_code","runtime_returncode_uses":0,"root_create_once":true,"synthetic_inputs":4,"semantic_matrix_cases":16,"same_root_reads":4,"exact_artifact_names":["synthetic-plan.json","synthetic-full.json","synthetic-lineage.json","synthetic-seal.json","integration-qualification.json","integration-qualification.sha256.json","terminal-evidence.json","terminal-evidence.sha256.json","execution-result-admission.json"],"final_root_file_count":9,"pre_root_primary_machine_json":true,"pre_root_target_reads":0,"pre_root_file_writes":0,"pre_root_original_primary_rethrown":true,"retry":0,"fallback":0,"second_source":0,"second_root":0,"second_process":0},"execution_budgets":{"outer_read_only_git_invocations":1,"controller_read_only_git_invocations":6,"controller_source_writes":1,"controller_source_reads":1,"controller_processes":1,"output_roots":1,"synthetic_input_writes":4,"qualification_writes":2,"terminal_writes":2,"admission_writes":1,"execution_result_appends":1,"retry":0,"fallback":0},"zero_budgets":{"extra_outer_git_invocations":0,"code_writes":0,"test_writes":0,"plan_writes_by_executer":0,"full_writes_by_executer":0,"archive_writes_by_executer":0,"debug_writes":0,"guide_writes":0,"research_writes":0,"tests":0,"compileall":0,"codegraph_sync":0,"git_stage":0,"git_commit":0,"generic_machine_row_parser":0,"repo_machine_parser_calls":0,"old_failed_controller_reads":0,"old_failed_root_reads":0,"old_external_evidence_reads":0,"retained_artifact_reads":0,"candidate_payload_reads":0,"git_provenance_replay":0,"real_b2_dispatch":0,"subordinate_manifest_writes":0,"actual_canonical_validator_calls":0,"eligibility_emissions":0,"retained_release_audit":0,"release_generation":0,"release_qualification":0,"release_copy":0,"release_consumption":0,"network":0,"dns":0,"environment":0,"credentials":0,"device":0,"camera":0,"ray":0,"strip":0,"cleanup":0,"capture":0,"formal":0,"public_analyzer":0,"td_c":0,"sentinel":0,"p8":0,"firmware":0,"deployment":0},"expected_duration":"under_10_minutes","visible_terminal_required":false,"planner_stop":"B2_P4_C1_C1_C1_I1_C1_C1_C1_OUTER_FIRST_COMMAND_CORRECTION_WAITING_PLANNER_REVIEW"}`

## 1. Activation、fresh paths 与 immutable old failure

Activation commit 必须 direct parent/subject/exact three paths 与 machine row 一致，之后 porcelain clean。FULL 只允许本 task/contract active，保持 retained
`RETAINED_UNVALIDATED_UNCONSUMED`、candidate hash/verification、Executer dispatch true 与 device authorization false。

Executer 接手本包后不得执行通用 worktree preflight，也不得先执行任何 shell、Python、文件、进程或 Git 探测。第一条外部命令必须且只能是绝对路径
`/usr/bin/git rev-parse HEAD`；它同时是 controller 外唯一 Git invocation。禁止 `git status/log/show/diff/rev-list`、裸 `git`、`command -v git`、Git library、
subprocess Git、第二条 outer Git、topology/path/blob inspection。该命令 exit `0`、stderr empty、stdout 为 activation full SHA 加单一 LF；去掉 LF 后须为
40 位小写 hex，前七位派生 fresh source/root。Activation clean 不由 Executer preflight 证明，只由 Orchestrator 的 exact focused activation commit 事实与
controller 内 frozen Git6 验证。

Fresh source/root 必须 absent、位于 exact `/Volumes/4T/temp/rgbww-optimizer` parent、不得 symlink/escape。Source exclusive
`O_CREAT|O_EXCL|O_NOFOLLOW`、mode `0600`、write/fsync/stat exact once；writer 必须显式 import `json`，并在成功写入后输出一个 strict JSON report，不能
让 report formatting 把成功 write 误报为 failure。Accepted `read_exact_file` 读取 source exact once；同一 bytes 完成 strict UTF-8、AST parse、builtin
compile 与唯一 process dispatch。Root 只由 accepted `create_exclusive_root` 创建 once、mode `0700`。

旧 I1-C1 source/root/evidence 以及本次 pre-source failure 所冻结的 `2fed3dc` intended paths 均不可读、不可修复、不可删除、不可复用、不可 rerun；
不得从旧 source 恢复 hash 或 payload。新 path suffix 只能来自 successor activation，不得与 `809eb85` 或 `2fed3dc` 混用。

## 2. Exact machine-row delimiter and unchanged conformance

Fresh controller 从 activation/runtime workspace 读取 PLAN/FULL exact bytes，各自只接受 exact one line：leading
`` `PLAN_MACHINE_CONTRACT= `` / `` `FULL_PLAN_MACHINE_STATE= ``，trailing exact `` `\n `` 且禁止 CRLF；只剥离该 exact prefix/suffix，再做 strict
UTF-8、duplicate-key/nonfinite-rejecting JSON object parse。Bare marker、missing/extra backtick、multiple candidates、wrong LF、malformed JSON均 stable fail。
不得把该逻辑扩展为 generic marker/path parser，也不得调用 repo machine parser（其 owner result 会改变 frozen 18 bindings）。

Lifecycle conformance callback 对 dispatched bytes 调用既有 `analyze_controller_source` exact once；external AST classifier `0`。Source ownership/public methods、
bound results exact `18`、embedded transport report、effect/fixture domains、effect transport empty 均不得改变。Effect identities 继续 direct binding，跨 callback
只用 explicit enclosing direct names + `nonlocal`；只 inline 读取 accepted fields，禁止 tuple/list/dict/set container、generic live projection helper、alias、
callback/closure return。唯一 grouping exception 仍是 exact `RootIdentityChain` + direct `validate_root_identity_chain`。Opaque terminal gate 只以 original direct
name 传 admission。

Conformance failure仍是 pre-effect hard failure：Git6/root/inputs/evaluate/artifacts `0`，但必须按第 5 节的 pre-root structured failure 输出 original primary；
process nonzero，retry/fallback/second source/root/process `0`。

## 3. Unchanged Git6、same-root four and matrix16

Conformance 通过后 activation callback 才用 accepted `run_read_only_git` exact six：verify activation commit；show exact full SHA/NUL parent/NUL subject；
diff-tree exact paths；以及 activation 的 FULL、PLAN、本 review archive 三个 blob OID。六个 `GitLedger` 必须 direct-bind、使用 `exit_code`，禁止
`returncode`、collection、generic projection helper或 retained provenance replay。它们证明 activation exact full SHA、parent
`169e786d724c2f7064906957272b35096f7cc43a`、subject `chore(plan): correct p4 activation row lifecycle`、exact three paths与 runtime blobs。

Root callback 后 exclusive 写 exact four inputs：`synthetic-plan.json`、`synthetic-full.json`、`synthetic-lineage.json`、`synthetic-seal.json`。每个由
accepted `read_exact_file(..., root=<same direct live root>)` exact once；构造/validate唯一 RootIdentityChain。禁止额外 lstat/read/count probe。

Evaluate exact `16/16` 不变：actual source positive；`GitLedger.exit_code` positive；`returncode` rejection；unknown owner/unbound；alias/reflection/opaque；
rootless；literal root；different live root；actual four-file chain；root drift；pure in-memory FileIdentity mismatch fixture edge；child escape；device drift；mode drift；
primary-failure original identity；terminal/seal failure blocks admission。每个 negative 必须匹配原 stable code/exception identity。禁止新增 case、test、probe、
manual fix、second owner或 classifier。

## 4. Success exact9

Success root 最终只依序包含 exact9：four synthetic inputs、qualification JSON+seal、terminal JSON+seal、admission JSON。全部 canonical JSON、mode
`0600`、same-root direct child，并记录 physical identity。Qualification seal 绑定 qualification identity；terminal target 绑定 qualification identity；terminal
seal 绑定 terminal identity；opaque gate 只传 admission。

Success order exact `conformance, activation, root, inputs, evaluate, terminal, terminal_seal, admission`。Primary phases 仍仅
`activation/root/inputs/evaluate`。成功 postflight 只读核对 exact9、strict JSON/hash/linkage/root identities、source/root identity、outer HEAD `1/1`、extra
outer `0`、Git6、matrix16、lifecycle/counters与 exit。最终 Executer 只 append ER once；porcelain 只能 ER 一个 unstaged modification。

## 5. Pre-root structured failure lifecycle

Source/conformance/activation 的任何 pre-root failure 必须在 controller memory 冻结一个 canonical plain mapping：schema、phase、primary exception fully
qualified type、stable primary code、repo machine-contract evidence mapping（仅当该 exception 提供）、root_created false、qualification_target_present false、
retry/fallback `0/0`。不得反射 unknown fields、不得序列化 exception repr/traceback、不得包含路径外 secrets。

Terminal callback 看到 `primary is not None` 且 root/qualification target absent 时，必须返回该 in-memory primary envelope；不得调用
`write_terminal_evidence`、不得读 target、不得抛 `qualification_target_missing`。Terminal-seal callback 对该 branch 只返回一个 in-memory seal mapping，
admission callback 只返回一个 in-memory FAIL mapping；三者写文件均 `0`。Lifecycle 完成后必须重抛 exact original primary。Controller top-level catch 以
canonical JSON 输出 exact one `CONTROLLER_PRIMARY_FAILURE_JSON=` machine line后 nonzero exit；outer launcher捕获并在 ER 原样引用该 structured record。
不得把 primary 改写成 `terminal_failed`、`terminal_seal_failed` 或 generic wrapper code。

若 root 已创建，继续使用原 progressive physical evidence 与 file-based terminal/seal/admission failure contract；不得以 pre-root branch 绕过或放宽。任一
failure禁止 repair/delete/reuse/root rerun，retry/fallback `0`。

## 6. Acceptance, failure branches, locks and stop

Acceptance 要求：activation exact；`/usr/bin/git rev-parse HEAD` 是第一条外部命令；无通用 worktree preflight；outer HEAD `1`、extra outer Git `0`；fresh source/root/process `1/1/1`；writer JSON report成功；source read once；两个 exact
marker candidate各 one、delimiter/LF/strict JSON通过、generic parser/repo parser calls zero；repo analyzer once/external classifier zero；18 bindings/effect empty；Git6；same-root4；matrix16；exact9；terminal/
seal/admission linkage；exit0；retry/fallback0；仅 ER append。

Pre-root negative spot checks 必须由同一 source 的 bounded in-memory matrix/contract assertions证明 structured primary envelope、target reads/writes `0`、original
primary rethrow且 no missing-target masking；禁止为此运行 second controller/process或另建root。真实 run若 pre-root fail则按第5节保留 machine record并立即 stop。

本包通过仅证明 repo-owned transport/machine-contract owners 的 fresh synthetic integration。所有旧 source/root/evidence、retained R3/candidate、retained Git
replay、real B2、subordinate manifest、actual canonical validator、eligibility、retained audit、release、network、DNS、environment、credentials、device、camera、
Ray、strip、cleanup、capture、FORMAL、public analyzer、TD-C、sentinel、P8、firmware、deployment hard locked `0`。不运行 tests、compileall、CodeGraph；不改
code/test/FULL/PLAN/archive/debug/GUIDE/RESEARCH；不 stage/commit。所有分支在唯一 Planner stop 结束。

维护性判断：successor 仅收紧 Executer outer command ordering，不改 machine-row、lifecycle、repo analyzer、Git6、root、matrix 或 artifact owner；不新增生产抽象、
generic parser或平行执行框架。
