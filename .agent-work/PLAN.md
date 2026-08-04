# REF-G4-06-RAY-R6 bounded harness replacement package

**计划状态：** `EXECUTABLE_PENDING_ORCHESTRATOR_ACTIVATION_HARNESS_REPLACEMENT`

**Executable：** `true_after_exact_orchestrator_activation`

**Active task count：** `1`

**Active reference task：** `REF-G4-06-RAY-R6`

**Contract：** `G4-RAY-R6-STAGE-GATE-FRESH-PACKAGE-EVIDENCE-V1`

**Planner stop：** `RETURN_FOR_G4_06_REPLACEMENT_PACKAGE_REVIEW`

`PLAN_MACHINE_CONTRACT={"schema":"planner_execution_contract_v2","contract_id":"G4-RAY-R6-STAGE-GATE-FRESH-PACKAGE-EVIDENCE-V1","plan_status":"EXECUTABLE_PENDING_ORCHESTRATOR_ACTIVATION_HARNESS_REPLACEMENT","executable":true,"active_task_count":1,"active_task":"REF-G4-06-RAY-R6","reference_task_id":"REF-G4-06-RAY-R6","reference_goal":"REF-G4-COMPLETE","reference_task_status":"ACTIVE_BOUNDED_FRESH_HARNESS_REPLACEMENT_PACKAGE_AFTER_EXACT_ORCHESTRATOR_ACTIVATION","activation_state":"WAITING_ORCHESTRATOR_CONTROLLED_REVIEW_ARCHIVE_COMMIT","activation_commit":{"expected_parent":"411571f2aa7b70d931a5ccbac365c666d9c49ae9","expected_parent_tree":"8dc7e0ea42b5c92a24391aae96a302da9086bbcf","expected_subject":"docs(plan): retry ray r6 package after harness loss","expected_changed_paths":[".agent-work/EXECUTION_RESULT.md",".agent-work/PLAN.md",".agent-work/archived/EXECUTION_RESULT-20260804-0804.md",".agent-work/archived/PLAN-20260804-0804.md"],"direct_non_merge_child":true,"child_sha_recorded_in_plan":false},"single_current_action":"prepare_once_then_describe_once_one_fresh_replacement_package_with_unchanged_repo_owned_owner_and_native_tool_results","same_reference":true,"same_contract":true,"corrective_suffixes":0,"new_task_ids":0,"reviewed_failed_attempt_disposition":"REJECTED_G4_06_FRESH_PACKAGE_EVIDENCE_EXECUTION_HARNESS_RESULT_UNPROVEN","rejected_unactivated_drafts":["DESCRIBE_ONLY_DETERMINISTIC_SOURCE_DRIFT","CODE_SEAM_WOULD_INVALIDATE_ACCEPTED_SOURCE_LINEAGE"],"draft_corrections_count_as_execution_failures":false,"reviewed_plan_archive":{"path":".agent-work/archived/PLAN-20260804-0804.md","bytes":16639,"sha256":"1e2a5983c195023d8b5bbce4aa0d47a2dae498a6f249377f60c1f08ccda1f771"},"reviewed_execution_result_archive":{"path":".agent-work/archived/EXECUTION_RESULT-20260804-0804.md","bytes":7411,"sha256":"302b5ea3a3b1bdf5ad377d7465c82151051dcf6a157395bba6e0a8ab1af61b9b"},"historical_root":{"path":"/Volumes/4T/temp/rgbww-optimizer/g4-ray-r6-stage-gate-ebc40bf8e40c-20260804T063700Z","disposition":"HISTORICAL_UNCONSUMED_UNKNOWN_NOT_PROBED","access_authorized":false,"inspect_authorized":false,"reuse_authorized":false,"cleanup_authorized":false},"replacement_root":"/Volumes/4T/temp/rgbww-optimizer/g4-ray-r6-stage-gate-ebc40bf8e40c-harness-replacement-20260804T141423Z","replacement_root_must_be_fresh":true,"orchestration_harness_replacement_root_count":1,"prepare_cli_cap":1,"describe_cli_cap":1,"per_run_root_create_cap":1,"per_run_retry":0,"per_run_alternate_root":0,"further_replacement_root_cap":0,"accepted_code_checkpoint":"ebc40bf8e40c4bb59bd070367a321a2e76c3ce5c","accepted_code_tree":"9dc4b3fb70bc97b80fb1db3b2389585e349e8737","accepted_code_full_validation":"963_of_963","source_parent_checkpoint":"310f547c91420c34f67d1d241ad4aedaa3bc9c2c","source_parent_tree":"e5184c3236ba053909332fff032691c1aad167d0","code_or_test_changes_authorized":false,"allowed_repo_changed_paths":[".agent-work/EXECUTION_RESULT.md"],"raw_tool_evidence_contract":"EACH_NATIVE_EXEC_RESULT_EXIT_CODE_AND_RAW_COMBINED_OUTPUT","stdout_stderr_split_claim_authorized":false,"output_sha_claim_authorized":false,"outer_textencoder_or_crypto_authorized":false,"shell_wrapper_or_redirection_authorized":false,"handwritten_controller_authorized":false,"formal_execution_authorized":false,"formal_root_creation_authorized":false,"device_authorized":false,"network_authorized":false,"camera_authorized":false,"ray_authorized":false,"strip_authorized":false,"capture_authorized":false,"release_consumption_authorized":false,"retained_r3_access":0,"td_c_authorized":false,"tests_inherited":true,"test_rerun_authorized":false,"expected_duration_under_10_minutes":true,"visible_terminal_required":false,"planner_stop":"RETURN_FOR_G4_06_REPLACEMENT_PACKAGE_REVIEW","future_formal_package":"LOCKED_UNTIL_REPLACEMENT_PACKAGE_IS_PLANNER_TERMINAL_REVIEWED"}`

## 0. Reviewed history 与bounded replacement decision

上一fresh-package attempt已review并归档，terminal disposition为：

`REJECTED_G4_06_FRESH_PACKAGE_EVIDENCE_EXECUTION_HARNESS_RESULT_UNPROVEN`

其确定事实只有prepare launch count `1`；outer harness随后因`TextEncoder is not defined`丢失nested CLI result，prepare exit与raw output永久`UNPROVEN`，describe count `0`。这不是production owner failure，也未证明package成功或失败。

原root永久冻结为：

```text
/Volumes/4T/temp/rgbww-optimizer/g4-ray-r6-stage-gate-ebc40bf8e40c-20260804T063700Z
HISTORICAL_UNCONSUMED_UNKNOWN_NOT_PROBED
```

本PLAN禁止访问、inspect、list、stat、read、describe、reuse、repair、cleanup、rename或删除原root。不得从其存在与否推断任何结果。

此前未激活的describe-only草案会因live PLAN归档重写造成确定性source-reference drift；未激活的code-seam草案又会改变non-orchestration source identity并破坏`ebc40bf...`accepted-code后仅`.agent-work/`的lineage。两者均已在执行前丢弃，不计Executer failure、production retry或same-boundary failure。

Orchestrator现授权一次显式bounded harness replacement：使用unchanged repo-owned owner，在一个新的唯一fresh root执行prepare exact once；成功后立即describe exact once。透明记录`orchestration_harness_replacement_root_count=1`。这是一项harness evidence correction，不是对同一production invocation的retry；新invocation内部retry/alternate均为`0`，root create为`1`。

## 1. Activation gate

本PLAN只有在Orchestrator创建以下exact commit后可执行：

- parent：`411571f2aa7b70d931a5ccbac365c666d9c49ae9`；
- parent tree：`8dc7e0ea42b5c92a24391aae96a302da9086bbcf`；
- subject：`docs(plan): retry ray r6 package after harness loss`；
- changed paths exact：
  - `.agent-work/EXECUTION_RESULT.md`；
  - `.agent-work/PLAN.md`；
  - `.agent-work/archived/EXECUTION_RESULT-20260804-0804.md`；
  - `.agent-work/archived/PLAN-20260804-0804.md`；
- direct non-merge child；FULL不得修改。

Activation后worktree必须clean；PLAN/FULL active `1/1`，active/current/canonical task均为`REF-G4-06-RAY-R6`，contract exact为`G4-RAY-R6-STAGE-GATE-FRESH-PACKAGE-EVIDENCE-V1`；PLAN executable true，FULL executable false，formal/device/release-consumption authority均false。

任一topology、path、machine state或cleanliness不符，只写ER并停止，不得访问任何external root。

## 2. Frozen replacement root 与owner identity

唯一新root exact为：

```text
/Volumes/4T/temp/rgbww-optimizer/g4-ray-r6-stage-gate-ebc40bf8e40c-harness-replacement-20260804T141423Z
```

它必须由repo-owned `prepare`执行fresh-root validation及exclusive creation；Executer不得预先probe、mkdir、touch、list、stat或清理它。若owner报告root不fresh或任何creation failure，立即terminal stop；不得选择第三个root。

Frozen owner/source identity：

- accepted code checkpoint：`ebc40bf8e40c4bb59bd070367a321a2e76c3ce5c`；
- accepted code tree：`9dc4b3fb70bc97b80fb1db3b2389585e349e8737`；
- verified parent checkpoint：`310f547c91420c34f67d1d241ad4aedaa3bc9c2c`；
- verified parent tree：`e5184c3236ba053909332fff032691c1aad167d0`；
- inherited fresh validation：`963/963`。

不修改production code、tests、config、GUIDE/RESEARCH、PLAN/FULL或archives；不新增controller、wrapper、module、env/global override或monkeypatch。

## 3. Native tool evidence contract

两条CLI必须分别作为直接exec tool call执行。每次都先等待工具原生result完整返回模型，再进行下一步或写ER。只保留下列native fields：

- `exit_code`；
- `output`的原始combined text，保持工具返回的字符内容与newline，不自行encoding/decoding/摘要。

禁止：outer JavaScript `TextEncoder`、Web Crypto、hash、base64、自写parser/controller、`python -c`、heredoc、shell wrapper、redirection、pipeline、command substitution、tee或stdout/stderr分流声明。不得要求或伪报stdout/stderr各自内容、bytes或SHA；native combined output是本包唯一raw harness evidence。

每次成功都要求：

- native `exit_code == 0`；
- raw combined `output` exact为一行canonical JSON object加一个terminal newline，无其他文字；
- JSON可由模型在tool result返回后读取，并满足binding contract；
- prepare与describe两次raw combined output exact string equality。

## 4. Prepare exact once

唯一prepare命令：

```text
.venv/bin/python -m camera_based_rgbww_optimizer.optimization.p7_td_b_r6_stage_gate prepare --repo-root /Users/ibobby/Projects/WLED-RGBWW --source-parent-checkpoint 310f547c91420c34f67d1d241ad4aedaa3bc9c2c --source-parent-tree e5184c3236ba053909332fff032691c1aad167d0 --package-root /Volumes/4T/temp/rgbww-optimizer/g4-ray-r6-stage-gate-ebc40bf8e40c-harness-replacement-20260804T141423Z
```

Launch cap exact `1`。成功raw binding必须证明：

- schema `p7_td_b_r6_stage_gate_package_binding_v1`；
- package root path exact，且root identity含device/inode/mode `0700`；
- inventory exact、有序：`launch-descriptor.json`、`stage-gate.json`、`terminal-seal.json`；
- 每个artifact都有exact path、positive bytes、64-hex SHA-256、device/inode/mode `0600`。

Repo owner负责一次build/evaluate、exclusive root create、persist、internal replay、strict public replay与terminal seal。其sealed evidence必须保持retry/alternate/formal capture/device/release counts为`0`。

若native tool未返回completed exit code、exit非0、output不是exact canonical single line，prepare判定terminal failure；记录native result，`describe_launch_count=0`并停止。不得probe root、重新prepare、换root或修复。

## 5. Describe exact once

仅在prepare全部通过后运行：

```text
.venv/bin/python -m camera_based_rgbww_optimizer.optimization.p7_td_b_r6_stage_gate describe --repo-root /Users/ibobby/Projects/WLED-RGBWW --package-root /Volumes/4T/temp/rgbww-optimizer/g4-ray-r6-stage-gate-ebc40bf8e40c-harness-replacement-20260804T141423Z
```

Launch cap exact `1`。Describe必须由unchanged repo owner重新验证root、inventory、artifact identity、terminal seal、stage gate、descriptor、source references与authority，然后输出canonical binding。成功要求native exit `0`、raw combined output exact单行JSON加newline，并与prepare raw output逐字符相等。

若失败，记录native result并立即停止；不得第二次describe、direct probe、prepare rerun、repair、cleanup或第三root。

## 6. ER handoff 与acceptance

Executer唯一允许修改`.agent-work/EXECUTION_RESULT.md`。ER必须记录：

- activation HEAD/tree/subject/path set与clean intake；
- old root exact disposition及access count `0`；
- replacement root与`orchestration_harness_replacement_root_count=1`；
- 两次exact argv及launch counts；
- 每个native tool result的exit code与raw combined output原文；不得添加stdout/stderr分流或output SHA；
- prepare/describe raw exact equality结论；
- canonical binding的root/inventory/artifact identities；
- owner-produced terminal validation与per-run root create `1`、retry `0`、alternate `0`、formal/device/release counts `0`；
- changed paths与`git diff --check`；
- code/tests/GUIDE/RESEARCH/config/PLAN/FULL/archives未变；
- device/network/camera/Ray/strip/capture/formal/release/retained-R3/TD-C access均为`0`；
- proposed status：`READY_FOR_PLANNER_G4_06_REPLACEMENT_PACKAGE_EVIDENCE_REVIEW`或terminal fail-closed status。

不运行targeted/focused/full/compile；继承accepted checkpoint的fresh `963/963`，因为production tree完全不变。只允许运行repo read-only Git、strict PLAN/FULL parser、status与diff检查。

成功只代表新的offline durable stage-gate package成为Planner候选；不代表formal/device/quality/history pass，不授予release consumption或G4-07 authority。失败时不得再创建replacement root或corrective task。

唯一Planner stop：`RETURN_FOR_G4_06_REPLACEMENT_PACKAGE_REVIEW`。
