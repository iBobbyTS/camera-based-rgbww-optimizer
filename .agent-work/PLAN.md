# REF-P7-25-R2-B2-P5：repo-owned controller runtime owner

**计划状态：** `WAITING_ORCHESTRATOR_ACTIVATION`

**Planner 日期：** `2026-07-31`

**Reference task：** `REF-P7-25-R2-B2-P5`

**Contract ID：**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-P5-REPO-OWNED-CONTROLLER-RUNTIME-OWNER-V1`

**Planner decision：** evidence commit
`ec2dd705fbcf3349297fb141b732ebc9b61aaf94` 被拒绝为
`REJECTED_PRE_EFFECT_REFLECTION_AND_SOURCE_WRITER_PROOF_GAP`。Runtime-token fixture separation与 single-input launcher 已局部成功，但 disposable controller仍被 repo analyzer 以 `reflection_rejected` 在 effect 前拒绝，且 patch+chmod writer没有 exclusive/no-follow/fsync 证明。自 I1 起连续失败已经证明继续修补一次性 source 会恶化脆弱 controller state machine，因此本轮不授权任何新 external source/root/controller；先建立唯一 repo-owned outer-runtime owner。

**当前唯一动作：** Orchestrator审核本 PLAN、更新 FULL，并以
`ec2dd705fbcf3349297fb141b732ebc9b61aaf94` 为 direct parent 创建 exact activation commit。Activation后，Executer只在 exact two paths 中实现和测试一个新 `p7_retained_r3_controller_runtime` owner；它组合既有 preparation、conformance和 provenance-I/O owners，负责 deterministic source composition、exclusive source persistence proof与 single-input process launch，不复制 analyzer、physical read、lifecycle或 eligibility逻辑。

**唯一 Planner stop：**
`B2_P5_REPO_OWNED_CONTROLLER_RUNTIME_OWNER_WAITING_PLANNER_REVIEW`。

**本轮新归档：**
`.agent-work/PLANS/20260731-1521-p7-retained-r3-b2-p4-runtime-token-successor-architecture-review.md`；activation前由 Orchestrator记录其 final bytes/SHA-256到 FULL/commit handoff。

`PLAN_MACHINE_CONTRACT={"schema":"p7_td_b_retained_r3_option_b_b2_p5_repo_owned_controller_runtime_owner_v1","reference_task_id":"REF-P7-25-R2-B2-P5","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-P5-REPO-OWNED-CONTROLLER-RUNTIME-OWNER-V1","execution_authorized_after_orchestrator_activation":true,"activation_commit":{"expected_parent":"ec2dd705fbcf3349297fb141b732ebc9b61aaf94","expected_subject":"chore(plan): activate p5 controller runtime owner","expected_changed_paths":[".agent-work/FULL_PLAN_REFERENCE.md",".agent-work/PLAN.md",".agent-work/PLANS/20260731-1521-p7-retained-r3-b2-p4-runtime-token-successor-architecture-review.md"],"clean_porcelain_required_after_activation":true},"required_full_machine_state":{"active_task_count":1,"active_task":"REF-P7-25-R2-B2-P5","active_plan_contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-P5-REPO-OWNED-CONTROLLER-RUNTIME-OWNER-V1","retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","candidate_machine_contract_sha256":"96ece8940a82d53ff6e61b8b2e0ecb4f0cb01d93770ce5a992942c2464ab449a","candidate_contract_orchestrator_verified":true,"executer_dispatched":true,"device_authorized_by_this_file":false},"implementation":{"new_module":"src/camera_based_rgbww_optimizer/utils/p7_retained_r3_controller_runtime.py","dedicated_test":"tests/test_p7_retained_r3_controller_runtime.py","changed_paths_exact":2,"expected_subject":"feat(p7): own retained controller runtime","existing_preparation_owner":"camera_based_rgbww_optimizer.utils.p7_retained_r3_controller_preparation","existing_conformance_owner":"camera_based_rgbww_optimizer.utils.p7_retained_r3_controller_conformance.analyze_controller_source","existing_provenance_owner":"camera_based_rgbww_optimizer.utils.p7_retained_r3_provenance_io","new_analyzer":false,"new_lifecycle":false,"plan_specific_matrix":false,"retained_interpretation":false},"owner_contract":{"deterministic_source_bytes":true,"deterministic_report":true,"source_type":"bytes","strict_utf8_ast_compile":true,"conformance_before_writer":true,"analyzer_calls_per_attempt":1,"source_writes_per_attempt_max":1,"source_reads_per_written_attempt":1,"source_mode":"0600","writer_flags":["O_WRONLY","O_CREAT","O_EXCL","O_NOFOLLOW"],"complete_write_with_eintr_handling":true,"file_fsync":true,"parent_directory_fsync":true,"regular_nonsymlink_identity":true,"launcher_processes_per_accepted_attempt":1,"launcher_input":"exact_verified_source_bytes","launcher_stdin_keyword_present":false,"shell":false,"check":false,"result_success_field":"exit_code","reflection_helpers":false,"returncode_attribute_in_controller_source":false,"second_classifier":false,"generic_allowlist":false},"tests":{"targeted_expected":"6/6","focused_expected":"76/76","full_expected":"767/767","postcommit_targeted_expected":"6/6"},"execution_budgets":{"code_paths":2,"test_methods_added":6,"targeted_runs":1,"focused_runs":1,"compileall_runs":1,"full_runs":1,"codegraph_sync_runs":1,"codegraph_owner_queries":1,"git_commits":1,"postcommit_targeted_runs":1,"execution_result_appends":1},"zero_budgets":{"external_controller_source_writes":0,"external_controller_processes":0,"external_output_roots":0,"old_failed_source_reads":0,"old_failed_root_reads":0,"old_external_evidence_reads":0,"retained_artifact_reads":0,"candidate_payload_reads":0,"git_provenance_replay":0,"real_b2_dispatch":0,"subordinate_manifest_writes":0,"actual_canonical_validator_calls":0,"eligibility_emissions":0,"retained_release_audit":0,"release_generation":0,"release_qualification":0,"release_copy":0,"release_consumption":0,"network":0,"dns":0,"environment":0,"credentials":0,"device":0,"camera":0,"ray":0,"strip":0,"cleanup":0,"capture":0,"formal":0,"public_analyzer":0,"td_c":0,"sentinel":0,"p8":0,"firmware":0,"deployment":0,"plan_writes_by_executer":0,"full_writes_by_executer":0,"archive_writes_by_executer":0,"debug_writes":0},"expected_duration":"under_10_minutes","visible_terminal_required":false,"planner_stop":"B2_P5_REPO_OWNED_CONTROLLER_RUNTIME_OWNER_WAITING_PLANNER_REVIEW"}`

## 1. Activation 与 frozen baseline

Activation commit必须满足 machine row 的 direct parent、subject、exact three paths，之后 porcelain clean。FULL只允许本 task/contract active，保持 retained `RETAINED_UNVALIDATED_UNCONSUMED`、candidate hash/verification、Executer dispatched true、device authorization false，并将全部 I1 disposable-controller successor标为 rejected/superseded，不得将 token separation局部成功解释为 integration qualification。

Executer可执行普通只读 repository preflight；本 package不保留 I1 的 first-command/outer-Git budget，因为它不创建或启动 external controller。冻结 baseline：implementation parent exact activation HEAD；现有 accepted owners与 tests不得修改；implementation exact two new paths initially absent。若任一路径已存在、worktree有越界改动或 activation不匹配，fail closed并仅写 ER。

不得读取、探测、修复、删除、复用或 rerun任何旧 I1 source/root/evidence，尤其是 `1bc089e` attempt。不得访问 retained R3、candidate或 real-B2 external roots。

## 2. 单一 owner 边界

新增 `p7_retained_r3_controller_runtime.py`，只拥有 controller outer runtime envelope：

1. 接收严格、immutable、bytes-based composition request；调用既有 `prepare_controller_source` 或其更底层 pure byte primitives生成唯一 deterministic bytes和 SHA-256；相同输入必须得到逐字节相同结果与 frozen report。
2. 在任何 filesystem/process effect前，将 exact prepared bytes交给既有 `analyze_controller_source` exact once。它是 reflection、owner binding、transport与 forbidden `returncode` 的唯一 analyzer；新 module不得添加第二 AST walker、regex/token classifier、generic allowlist、path allowlist或 token编码逃逸。
3. Analyzer通过后，owner以 exact `O_WRONLY|O_CREAT|O_EXCL|O_NOFOLLOW`、mode `0600` 创建 caller明确给出的绝对 source path；处理 partial write和 `EINTR`，file fsync、close、parent directory以 no-follow directory descriptor fsync，并核对 regular/non-symlink/mode/device/inode/bytes/SHA。
4. 写后读取与 immutable physical identity必须复用 `p7_retained_r3_provenance_io.read_exact_file`，不得复制 accepted read implementation；读取 bytes必须与 prepared bytes exact相等。任何 existing path、symlink、short/no-progress write、fsync、close、parent或 identity drift均 stable fail closed，不 rewrite、delete、repair或 launch。
5. 只有 analyzer、writer、readback全部通过后才可 launch exact one Python controller process。真实 mapping必须使用 `input=<exact verified source bytes>`，不得传 `stdin` key，且 `shell=False`、`check=False`、stdout/stderr为 bytes。结果立即转换为 immutable repo report，成功字段命名 `exit_code`；不得让 consumer依赖 `CompletedProcess.returncode`。

新 owner不得包含 PLAN/FULL parser、Git topology、matrix16、retained artifact schema、exact-five lifecycle、terminal/seal/admission、canonical validator、eligibility、release或device逻辑。Preparation仍为 pure byte owner；conformance仍为唯一 source eligibility owner；provenance I/O仍为 physical identity/read owner；lifecycle仍为阶段/terminal owner。新 module只是明确的 composition/persistence/launch adapter，不得成为第二 analyzer或 god helper。

## 3. Exact six dedicated regressions

新增 dedicated test exact `6` methods，覆盖：

1. identical immutable request两次 composition产生 exact相同 source bytes、SHA-256与 deterministic report，且 strict UTF-8、AST和 builtin compile通过；
2. 含 reflection的 source被 existing analyzer stable拒绝，writer/read/launcher counters均 `0`，证明 conformance-before-effect；
3. success writer证明 exact flags、mode、partial-write/EINTR恢复、file fsync→close→parent open/fsync顺序以及 returned physical identity/readback exact；
4. existing target、symlink、write no progress、file/parent fsync failure、readback identity/hash drift子矩阵全部 fail closed，launch `0`，target不被 rewrite/delete/repair；
5. success launcher exact one process、`input`为 verified bytes、`stdin` key absent、`shell=False`、`check=False`，stdout/stderr/exit code被 immutable report承接；invalid process result或 launch exception stable fail，retry/second process `0`；
6. token-domain/source contract证明合法 source只用 `GitLedger.exit_code`且报告 analyzer调用 exact1；含 `.returncode` attribute或 generic reflection的 negative source只由 existing analyzer拒绝，不以 literal string self-scan、第二 classifier或 allowlist判断。

Tests必须检查 public exports与 static ownership boundary，确保新 module只导入/调用 existing owners和最小标准库 I/O/process primitives，无 network/device/camera/Ray/release/validator imports。不得用只执行不断言的 tests。

## 4. Validation、commit 与 evidence

按唯一顺序执行：

1. targeted：新 dedicated test exact `6/6`；
2. focused：controller runtime/preparation/conformance/provenance I/O/integration tests exact `76/76`；
3. `.venv/bin/python -m compileall -q` exact new module；
4. unique full suite `python -m unittest discover -s tests` exact `767/767`、exit `0`、`OK`；不得用第二 full或其它测试替代；
5. `codegraph sync` exact once，然后 query证明 runtime唯一调用 preparation/conformance/provenance owners且无第二 analyzer/lifecycle；
6. `git diff --check`、exact two-path gate、source/test bytes+SHA-256、staged exact two paths；
7. 创建唯一 commit，subject exact `feat(p7): own retained controller runtime`，changed paths exact two；
8. commit后 targeted exact `6/6`，HEAD/parent/subject/path/blob/SHA gate，最后只 append ER once。

ER必须记录 activation、implementation commit、exact paths/blob OIDs/bytes/SHA、每个 test/static gate的真实 count/exit、CodeGraph结果、owner边界、failure branch及全部 zero budgets。测试产生的 test-owned temporary files不是 external controller dispatch，但必须在 test temp-directory lifecycle内，不能写固定 `/Volumes/4T` controller path。

## 5. Acceptance、failure branches 与 locks

Acceptance要求 exact two-path implementation；单一 runtime owner边界；deterministic bytes/report；strict source validation；existing analyzer exact once pre-effect；exclusive/no-follow/0600/complete-write/file+parent fsync/readback proof；single-input exact-one launcher；exit_code report；six regressions、focused/full/compileall/CodeGraph/diff/commit/postcommit全部通过；无第二 analyzer、generic allowlist、PLAN-specific state machine或 retained/device behavior。

任何 analyzer、writer、readback、launcher、test、CodeGraph、path或 commit gate失败均 fail closed：保留 repo changes/evidence，不以 fallback隐藏 primary，不启动第二 process，不创建 external qualification root，不 retry；append truthful ER并停在同一 Planner stop。若实现发现必须修改第三个 production/test path，停止并请求 Planner/Orchestrator重新界定 owner，不得自行扩 scope。

旧 external source/root/evidence、retained R3/candidate、Git provenance replay、real B2、subordinate manifest、actual canonical validator、eligibility、retained audit、release、network、DNS、environment、credentials、device、camera、Ray、strip、cleanup、capture、FORMAL、public analyzer、TD-C、sentinel、P8、firmware、deployment全部 hard locked `0`。

本 PLAN只授权 repo-owned runtime owner implementation，不授权 fresh synthetic integration、retained validation、release consumption、设备或 scientific stage。所有分支均停在唯一 Planner stop。

维护性判断：这是连续 disposable-controller failure后的最小 enabling refactor。新 module只拥有 outer composition/write/launch envelope，复用并保持 preparation、conformance、provenance-I/O与 lifecycle边界；exact six回归保护高风险 source persistence和process启动语义。若未来出现第三种 controller envelope，应复用本 owner，不应再生成平行一次性实现。
