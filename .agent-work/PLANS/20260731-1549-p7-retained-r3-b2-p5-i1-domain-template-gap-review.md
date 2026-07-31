# REF-P7-25-R2-B2-P5-I1：repo runtime fresh synthetic integration

**计划状态：** `WAITING_ORCHESTRATOR_ACTIVATION`

**Planner 日期：** `2026-07-31`

**Reference task：** `REF-P7-25-R2-B2-P5-I1`

**Contract ID：**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-P5-I1-REPO-RUNTIME-FRESH-SYNTHETIC-INTEGRATION-V1`

**Planner decision：** implementation `37f7d0021c7a81a9d6680815bc51c305cf807a7b` 与 evidence
`2cb1f2c6538d44d9bf002a570e2852b763feae07` 已被接受为
`ACCEPTED_COMPLETE_REPO_OWNED_CONTROLLER_RUNTIME_OWNER`。P5 关闭了 repeated disposable controller 的 source
composition/persistence/launch owner 缺口，但尚未证明完整 synthetic Git6/four-input/matrix16/exact9/terminal lifecycle 能消费该 owner；retained
R3 仍是 `RETAINED_UNVALIDATED_UNCONSUMED`。

**当前唯一动作：** Orchestrator 审核本 PLAN、更新 FULL，并以
`2cb1f2c6538d44d9bf002a570e2852b763feae07` 为 direct parent 创建 exact activation commit。Activation 后，Executer 运行唯一
fresh synthetic integration：外层只构造 immutable request/template domain inputs 并调用 repo-owned
`execute_controller_runtime` exact once；source preparation、existing conformance、exclusive persistence/readback与 single-input
process launch全部由该 owner完成。Controller 复用既有 Git/provenance/conformance/lifecycle owners完成 Git6、four inputs、matrix16、exact9、
terminal/seal/admission。不得再手写 external source writer/reader/launcher、第二 analyzer/classifier 或平行 lifecycle。

**唯一 Planner stop：**
`B2_P5_I1_REPO_RUNTIME_FRESH_SYNTHETIC_INTEGRATION_WAITING_PLANNER_REVIEW`。

**本轮新归档：**
`.agent-work/PLANS/20260731-1537-p7-retained-r3-b2-p5-runtime-owner-review.md`；bytes `7508`，SHA-256
`22fee71a6da19ac17f067faec506b3a31ba62371a931c9a0bee2726f6f07915a`。

`PLAN_MACHINE_CONTRACT={"schema":"p7_td_b_retained_r3_option_b_b2_p5_i1_repo_runtime_fresh_synthetic_integration_v1","reference_task_id":"REF-P7-25-R2-B2-P5-I1","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-P5-I1-REPO-RUNTIME-FRESH-SYNTHETIC-INTEGRATION-V1","execution_authorized_after_orchestrator_activation":true,"activation_commit":{"expected_parent":"2cb1f2c6538d44d9bf002a570e2852b763feae07","expected_subject":"chore(plan): activate p5 synthetic integration","expected_changed_paths":[".agent-work/FULL_PLAN_REFERENCE.md",".agent-work/PLAN.md",".agent-work/PLANS/20260731-1537-p7-retained-r3-b2-p5-runtime-owner-review.md"],"clean_porcelain_required_after_activation":true},"required_full_machine_state":{"active_task_count":1,"active_task":"REF-P7-25-R2-B2-P5-I1","active_plan_contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-P5-I1-REPO-RUNTIME-FRESH-SYNTHETIC-INTEGRATION-V1","retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","candidate_machine_contract_sha256":"96ece8940a82d53ff6e61b8b2e0ecb4f0cb01d93770ce5a992942c2464ab449a","candidate_contract_orchestrator_verified":true,"executer_dispatched":true,"device_authorized_by_this_file":false},"accepted_runtime_owner":{"commit":"37f7d0021c7a81a9d6680815bc51c305cf807a7b","parent":"099d1ad833c3e73b7dc157f5786ad66bb6718f5e","source_blob":"075face6fd7453236affa303640b91eb16a42a9b","source_sha256":"07eaeac615ea79db45afad91ce4c82e28c1cdcb66b6119b5cdca6462d7c091d2","test_blob":"a6aa7d7caf015e2eb858830dc89aaedaeb51aafa","test_sha256":"66b1806f68f110280da519e2376de8de7d03ebe6c262af67d9ea589fd51d3782","entrypoint":"camera_based_rgbww_optimizer.utils.p7_retained_r3_controller_runtime.execute_controller_runtime","calls":1,"second_analyzer":false,"second_lifecycle":false},"fresh_paths":{"activation_short_sha_source":"outer_head_stdout_first_seven_hex","controller_source_template":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-p5-i1-controller-{activation_short_sha}.py","output_root_template":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-p5-i1-qualification-{activation_short_sha}","must_be_absent_before_start":true,"source_mode":"0600","root_mode":"0700"},"runtime_contract":{"immutable_requests":1,"compose_calls":1,"existing_analyzer_calls":1,"source_open_writes":1,"source_readbacks":1,"runtime_launches":1,"controller_processes":1,"launcher_input":"exact_verified_source_bytes","launcher_stdin_key":false,"shell":false,"check":false,"report_success_field":"exit_code","outer_handwritten_source_writer":false,"outer_handwritten_source_reader":false,"outer_handwritten_launcher":false,"external_classifier_calls":0,"generic_allowlist":false},"controller_contract":{"outer_git_invocations":1,"outer_git_argv":["/usr/bin/git","rev-parse","HEAD"],"outer_first_external_command_required":true,"controller_activation_git_ledgers":6,"git_success_field":"exit_code","runtime_returncode_uses":0,"expected_bound_results":18,"embedded_transport_report":true,"effect_transport_uses_on_pass":0,"root_create_once":true,"synthetic_inputs":4,"same_root_reads":4,"semantic_matrix_cases":16,"exact_artifact_names":["synthetic-plan.json","synthetic-full.json","synthetic-lineage.json","synthetic-seal.json","integration-qualification.json","integration-qualification.sha256.json","terminal-evidence.json","terminal-evidence.sha256.json","execution-result-admission.json"],"final_root_file_count":9,"retry":0,"fallback":0,"second_source":0,"second_root":0,"second_process":0},"execution_budgets":{"outer_read_only_git_invocations":1,"runtime_owner_calls":1,"controller_source_writes":1,"controller_source_readbacks":1,"controller_processes":1,"output_roots":1,"synthetic_input_writes":4,"qualification_writes":2,"terminal_writes":2,"admission_writes":1,"execution_result_appends":1,"retry":0,"fallback":0},"zero_budgets":{"manual_external_source_open":0,"manual_external_source_chmod":0,"manual_external_source_read":0,"manual_controller_subprocess_launch":0,"second_analyzer":0,"second_classifier":0,"generic_allowlist":0,"parallel_lifecycle":0,"code_writes":0,"test_writes":0,"plan_writes_by_executer":0,"full_writes_by_executer":0,"archive_writes_by_executer":0,"debug_writes":0,"tests":0,"compileall":0,"codegraph_sync":0,"git_stage":0,"git_commit":0,"old_failed_controller_reads":0,"old_failed_root_reads":0,"old_external_evidence_reads":0,"retained_artifact_reads":0,"candidate_payload_reads":0,"git_provenance_replay":0,"real_b2_dispatch":0,"subordinate_manifest_writes":0,"actual_canonical_validator_calls":0,"eligibility_emissions":0,"retained_release_audit":0,"release_generation":0,"release_qualification":0,"release_copy":0,"release_consumption":0,"network":0,"dns":0,"environment":0,"credentials":0,"device":0,"camera":0,"ray":0,"strip":0,"cleanup":0,"capture":0,"formal":0,"public_analyzer":0,"td_c":0,"sentinel":0,"p8":0,"firmware":0,"deployment":0},"expected_duration":"under_10_minutes","visible_terminal_required":false,"planner_stop":"B2_P5_I1_REPO_RUNTIME_FRESH_SYNTHETIC_INTEGRATION_WAITING_PLANNER_REVIEW"}`

## 1. Activation、frozen owner 与 first command

Activation commit 必须满足 machine row 的 direct parent、subject、exact three paths，之后 porcelain clean。FULL 只允许本 task/contract
active，保持 candidate hash/verification、retained `RETAINED_UNVALIDATED_UNCONSUMED`、Executer dispatched true 与 device authorization false；P5
必须标为 accepted complete，但 synthetic integration 尚未 qualified。

Executer 不得先做通用 worktree/Git preflight。第一条 tool call/外部命令必须且只能是：

```text
/usr/bin/git rev-parse HEAD
```

它也是 controller 外唯一 Git invocation，必须 exit `0`、stderr empty、stdout exact activation full SHA 加单一 LF。前七位派生本包唯一
fresh source/root；二者必须 initially absent、位于 exact `/Volumes/4T/temp/rgbww-optimizer` parent、非 symlink/alternate spelling/escape。

Outer HEAD 确认后不得新增 Git 或 code/test inspection command；accepted runtime owner 的 commit ancestry、blob/bytes/SHA 由 controller Git6
统一证明，模块只通过正常 Python import消费，不重新验证或修改 code/test。所有旧 I1 source/root/evidence 不得读、探测、修复、删除、复用或
rerun。不得读取 retained R3/candidate/old external evidence。

## 2. Runtime-owner-only external controller boundary

Outer 执行材料只允许一个 immutable `ControllerRuntimeRequest`、默认 dependencies 与一次
`execute_controller_runtime(request)`：

- `template_source` 是本次 fresh controller 的 deterministic in-memory domain template；仅承载 Git6、synthetic inputs、matrix16、exact9 与
  lifecycle 领域逻辑，不得自带 source file open/write/chmod/readback、subprocess launcher、AST walker、token/regex classifier或 allowlist；
- template 中必须有唯一 `ACTIVATION_CONTRACT = {"placeholder": True}` assignment，下一条同-list statement必须 exact 为
  `require_activation_contract(ACTIVATION_CONTRACT)`；request 的 `assignment_name` exact `ACTIVATION_CONTRACT`、
  `validation_function` exact `require_activation_contract`；
- `replacement_statement` 是单一 `ACTIVATION_CONTRACT = <immutable literal>`，只冻结 activation HEAD/parent/subject/exact paths、accepted
  runtime commit/blob/SHA、fresh source/root与本包 counters/budgets；其 bytes/SHA须在 effect前记录到 in-memory envelope，不得 patch external file；
- `source_path` exact 等于 fresh source path；`process_argv` exact 指向项目 `.venv` Python 加 `-`，由 runtime owner 使用 verified bytes 作为
  sole `input`；
- outer caller 不得直接 `open`/`Path.write_*`/`chmod`/`read_*` source，不得自行调用 `analyze_controller_source`，不得直接
  `subprocess.run/Popen` controller；唯一 filesystem/process effects 必须来自 accepted runtime owner；
- dependencies 不得 override。Runtime report 必须证明 compose1、existing analyzer1、exclusive source write1、accepted readback1、process1，
  source identity/path/mode/bytes/SHA exact，process argv/input contract、bytes stdout/stderr与 truthful `exit_code`。

Runtime source 中不得使用 reflection、`.returncode`、owner alias/container/helper escape、generic transport或 duplicated classifier。Repo
`analyze_controller_source` 是 actual source 的唯一 semantic owner；controller只消费其 immutable report。Conformance/write/readback/launch
任一失败即保留 fresh source（若已产生）并 stop，不创建第二 source/process/root，不 fallback/retry/repair/delete。

## 3. Controller Git6、same-root four inputs 与 matrix16

Controller 启动后使用 accepted `run_read_only_git` exact six ledgers，仅以 `GitLedger.exit_code` 判定成功，证明：

1. activation full HEAD；
2. activation direct parent `2cb1f2c6538d44d9bf002a570e2852b763feae07`；
3. activation subject `chore(plan): activate p5 synthetic integration`；
4. activation exact FULL/PLAN/archive changed-path set；
5. accepted implementation `37f7d0021c7a81a9d6680815bc51c305cf807a7b` 为 ancestor且 exact two paths；
6. exact runtime/test blob OIDs与 committed bytes/SHA 没有漂移。

不得在 Git6 外增加 controller Git；outer 也不得增加 first/sole invocation以外的 Git。Git facts必须保持 immutable ledger，不得用 raw
`CompletedProcess`、reflection、dict/container或 helper transport绕过 owner contract。

Conformance与activation通过后，controller用 accepted provenance-I/O owner创建唯一 fresh root mode `0700`。在该 same-root 下写入并 exact read
四个 canonical synthetic inputs：`synthetic-plan.json`、`synthetic-full.json`、`synthetic-lineage.json`、`synthetic-seal.json`；每个 regular、
non-symlink、mode `0600`、strict canonical JSON/exact LF、physical identity/hash稳定。四个 reads必须绑定同一 live root并组成 exact
`RootIdentityChain(before, files=(four direct identities), after)`，随后 exact once `validate_root_identity_chain`；不得 alias、containerize或传入
generic helper。

Semantic matrix exact `16/16`，至少保留并独立报告：actual runtime source positive、GitLedger `exit_code` positive、forbidden attribute negative、
unknown/unbound owner、alias/reflection/opaque、rootless/literal/different live root、actual four-file chain、root drift、pure in-memory mismatch fixture、
child escape、device/mode drift、original primary identity、terminal/seal before admission。Negative fixture不得把完整 forbidden token自指注入受检
runtime source；actual source判断只使用 runtime owner返回的 existing conformance report，不得再次调用 analyzer或另写 classifier。

## 4. Exact9 lifecycle、terminal seal 与 admission

成功 lifecycle order exact：

```text
conformance -> activation -> root -> inputs -> evaluate -> terminal -> terminal_seal -> admission
```

Root 最终 exact九个 artifact：four synthetic inputs，加
`integration-qualification.json`、`integration-qualification.sha256.json`、`terminal-evidence.json`、
`terminal-evidence.sha256.json`、`execution-result-admission.json`。Qualification须记录 runtime owner commit/blob/SHA、source physical identity/SHA、
embedded conformance/transport report、Git6、same-root4、matrix16与all counters；sidecar绑定exact target bytes/hash。Terminal、seal、admission依次调用
既有 accepted lifecycle/terminal owners，证明 primary success、exact9、target/seal physical linkage、terminal dominance和 admission true。

Controller stdout 只能输出一个 canonical machine-readable success envelope；stderr empty、exit `0`。Outer 必须从 immutable
`ControllerRuntimeReport.process`读取 `exit_code/stdout/stderr`，不得读取 raw process `returncode`。Postflight只消费报告与本次 root exact9，不得用
额外 Git/analyzer/source read。Success也只能称 `FRESH_SYNTHETIC_INTEGRATION_QUALIFIED`，不得称 retained validated/eligible/release usable。

## 5. Failure lifecycle 与 evidence

Runtime owner返回前的 composition/conformance/persistence/readback/launch failure保留 typed primary及已有 physical source evidence；root不得创建。
Controller已启动但 root前失败时，stdout输出 exact one canonical primary envelope、无 traceback，不用 terminal callback 的
`qualification_target_missing` 覆盖 primary。Root创建后的 failure按既有 progressive physical evidence/file-based terminal contract seal，保留全部已有
artifacts且不修复、删除或重用。

任何失败均：retry/fallback/second source/root/process `0`；不得用 success terminal掩盖 primary；outer记录 runtime exception/report、source/root existence、
exact counters与hard locks。Repository唯一写入是 `.agent-work/EXECUTION_RESULT.md` EOF append once，记录 activation、fresh paths、runtime report、
Git6/same-root4/matrix16/exact9/lifecycle真实进度、failure/success、artifact bytes/SHA和所有 zero budgets。Executer不得写 PLAN/FULL/archive/debug。

## 6. Acceptance、validation quality 与 hard locks

Acceptance必须同时满足：activation/first command exact；accepted runtime code/blob/SHA不漂移；fresh source/root initially absent；runtime owner call1；
outer manual writer/read/launcher/analyzer0；prepared/conformance/exclusive write/readback/process各1；source mode/identity/bytes/SHA exact；controller
Git6；same-root4；matrix16；exact9；terminal/seal/admission linkage；stdout canonical、stderr empty、exit_code0；retry/fallback/second
source/root/process0；ER append1。

本包不运行 tests、compileall、CodeGraph sync，不改 code/test，不 stage/commit。Synthetic成功只关闭 integration residual risk；retained artifact/candidate
reads、Git provenance replay、real B2、subordinate manifest、actual canonical validator、eligibility emission、retained release audit、release
generation/qualification/copy/consumption、network、DNS、environment、credentials、device、camera、Ray、strip、cleanup、capture、FORMAL、public
analyzer、TD-C、sentinel、P8、firmware、deployment全部 hard locked exact `0`。

任何 path/hash/counter/semantic/lifecycle/terminal discrepancy均 fail closed并停在唯一 Planner stop；不得自行进入 retained validation、B3、release、设备或
scientific stage。

维护性判断：本包不新增 repo 文件或 execution framework。它首次让 fresh external consumer只调用已接受的 runtime owner，并继续复用 Git、
provenance-I/O、conformance 与 lifecycle 单一 owner；允许手写的仅是 immutable synthetic domain template，source persistence/readback/launch与
semantic analysis均禁止在 outer 重复实现。

## 7. Planner review：pre-effect under-specification

**Reviewed scope：** REF-P7-25-R2-B2-P5-I1 / P7-TD-B-RETAINED-R3-OPTION-B-B2-P5-I1-REPO-RUNTIME-FRESH-SYNTHETIC-INTEGRATION-V1。
计划方法是 outer 仅构造 immutable domain template/request 并 exact once 调用 accepted execute_controller_runtime；controller 预期复用现有
Git/provenance/conformance/lifecycle owners完成 Git6、same-root4、matrix16、exact9 与 terminal seal/admission。

**Evidence：** activation HEAD 0ca09a53b0bdb9f7a99ee6dee27420f7517ea702；evidence commit
4af057e0cd5f62d18a02cf02e088c1f293bddc4d，direct parent 0ca09a53b0bdb9f7a99ee6dee27420f7517ea702，subject
chore(evidence): record p5 template contract gap，changed path exact .agent-work/EXECUTION_RESULT.md。Authoritative ER handoff 为
REF-P7-25-R2-B2-P5-I1 Executer handoff — active PLAN under-specified before fresh effect。

**Validation quality：** first/sole outer Git exact /usr/bin/git rev-parse HEAD，exit 0、stdout exact activation SHA+LF；runtime calls、compose、
analyzer、source write/readback、process、Git6、root、four inputs、matrix、qualification/terminal/admission artifacts全部 exact 0。无 tests、
compileall、CodeGraph、device/network/retained calls；这是合约充分性 preflight，不是 synthetic execution pass。

**Finding REV-P5-I1-TEMPLATE-001：** accepted P5 public runtime API只接收 bytes/request，但 active PLAN没有冻结 canonical template bytes、
repo-owned builder、exact reconstructible 18-binding tuple或single physical root的 before/files/after source shape。继续由 Executer猜测 disposable
source会在 one-shot effect budget内重复已记录的 ownership drift，因此 pre-effect fail closed正确。

**Decision：** REJECTED_PRE_EFFECT_CANONICAL_DOMAIN_TEMPLATE_NOT_FROZEN。P5 runtime owner保持 accepted；P5-I1没有 qualification、没有消费
retained R3、没有解锁 validator/eligibility/release。

**Residual risks：** canonical builder尚未实现；generated source尚未被 existing analyzer验证 exact 18/14/4/7；Git6、matrix16、exact9/lifecycle
仍未运行。所有 external/retained/device/later-stage routes保持 hard locked。

**Exact next branch：** REF-P7-25-R2-B2-P6 /
P7-TD-B-RETAINED-R3-OPTION-B-B2-P6-REPO-OWNED-DETERMINISTIC-DOMAIN-TEMPLATE-V1。新增 exact
src/camera_based_rgbww_optimizer/utils/p7_retained_r3_controller_domain_template.py 与
tests/test_p7_retained_r3_controller_domain_template.py；pure deterministic builder only，完成后停在
B2_P6_REPO_OWNED_DETERMINISTIC_DOMAIN_TEMPLATE_WAITING_PLANNER_REVIEW。
