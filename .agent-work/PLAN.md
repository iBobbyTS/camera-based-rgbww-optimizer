# REF-P7-25-R2-B2-P4-V1：final-source full validation

**计划状态：** `ACTIVE_EXECUTION_AUTHORIZED`

**Planner 日期：** `2026-07-31`

**Reference task：** `REF-P7-25-R2-B2-P4-V1`

**Contract ID：**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-P4-V1-FINAL-SOURCE-FULL-VALIDATION-V1`

**当前唯一动作：** Orchestrator独立审核本review与PLAN、更新FULL并创建exact activation
commit；activation后，Executer只读证明冻结implementation/evidence topology与final file identity，
然后对final committed source运行一次exact full suite并要求 `755/755`。

**唯一 Planner stop：**
`B2_P4_V1_FINAL_SOURCE_FULL_VALIDATION_WAITING_PLANNER_REVIEW`。

**本轮新归档：**
`.agent-work/PLANS/20260731-1126-p7-retained-r3-b2-p4-implementation-validation-gap-review.md`。
bytes `5856`，SHA-256
`73ff80c255a39cb17d8113bf56e185bc37f28268a3ba267ca7438dc81c31981b`。

`PLAN_MACHINE_CONTRACT={"schema":"p7_td_b_retained_r3_option_b_b2_p4_v1_final_source_full_validation_v1","reference_task_id":"REF-P7-25-R2-B2-P4-V1","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-P4-V1-FINAL-SOURCE-FULL-VALIDATION-V1","execution_authorized_after_orchestrator_activation":true,"activation_commit":{"expected_parent":"de50071cd21a2459a9f68aca5e4357fe7d86abae","expected_subject":"chore(plan): activate p4 final-source full validation","expected_changed_paths":[".agent-work/FULL_PLAN_REFERENCE.md",".agent-work/PLAN.md",".agent-work/PLANS/20260731-1126-p7-retained-r3-b2-p4-implementation-validation-gap-review.md"],"clean_porcelain_required_after_activation":true},"required_full_machine_state":{"active_task_count":1,"active_task":"REF-P7-25-R2-B2-P4-V1","active_plan_contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-P4-V1-FINAL-SOURCE-FULL-VALIDATION-V1","retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","candidate_machine_contract_sha256":"96ece8940a82d53ff6e61b8b2e0ecb4f0cb01d93770ce5a992942c2464ab449a","candidate_contract_orchestrator_verified":true,"executer_dispatched":true,"device_authorized_by_this_file":false},"frozen_topology":{"implementation_commit":"83bb193259fcf1de5b3f78798001e83496c2daae","implementation_parent":"5f2483c319b395b2aef2a43f4827b4c150f3f3fd","implementation_subject":"feat(p7): add retained controller conformance owner","implementation_changed_paths":["src/camera_based_rgbww_optimizer/utils/p7_retained_r3_controller_conformance.py","tests/test_p7_retained_r3_controller_conformance.py"],"evidence_commit":"de50071cd21a2459a9f68aca5e4357fe7d86abae","evidence_parent":"83bb193259fcf1de5b3f78798001e83496c2daae","evidence_changed_paths":[".agent-work/EXECUTION_RESULT.md"]},"final_file_identity":{"source_path":"src/camera_based_rgbww_optimizer/utils/p7_retained_r3_controller_conformance.py","source_blob_oid":"52fcdc73c69e367cd1b046b52d83ffc555a6d496","source_sha256":"94a0992d662005df177b422d83fc1cefdd2cf7d43472571a27061df2bc7efeb7","test_path":"tests/test_p7_retained_r3_controller_conformance.py","test_blob_oid":"28a58c6051de378fbcc6485c316df9ff10d3a90c","test_sha256":"447bf13cb61e5b34ef6637e926a499e63b5b3393aa29e0d5fca205a96d180726","dedicated_test_methods":14},"lifecycle_semantics":{"conformance_is_pre_effect_gate":true,"conformance_failure_terminal_attempts":0,"sealed_primary_phases":["activation","root","inputs","evaluate"],"sealed_primary_failure_terminal_attempts":1,"terminal_success_seal_attempts":1,"seal_success_admission_attempts":1,"valid_fail_admission_preserves_primary_error":true,"retry":0,"fallback":0},"validation_contract":{"full_command":"PYTHONUNBUFFERED=1 .venv/bin/python -m unittest discover -s tests -p 'test_*.py'","full_invocations":1,"expected_tests":755,"expected_failures":0,"expected_errors":0,"expected_skips":0,"expected_exit_code":0,"terminal_output_must_be_retained_in_handoff":true,"targeted_invocations":0,"focused_invocations":0,"compileall_invocations":0,"codegraph_sync_invocations":0,"diff_check_required":true},"execution_budgets":{"read_only_git_invocations":8,"full_test_processes":1,"execution_result_appends":1,"retry":0,"fallback":0},"zero_budgets":{"code_writes":0,"test_writes":0,"plan_writes_by_executer":0,"full_writes_by_executer":0,"archive_writes_by_executer":0,"debug_writes":0,"guide_writes":0,"research_writes":0,"implementation_commits":0,"test_commits":0,"targeted_tests":0,"focused_tests":0,"compileall":0,"codegraph_sync":0,"external_controller_processes":0,"external_controller_writes":0,"evidence_root_creates":0,"qualification_writes":0,"old_controller_reads":0,"old_root_reads":0,"old_evidence_reads":0,"retained_artifact_reads":0,"git_provenance_replay":0,"real_b2_dispatch":0,"subordinate_manifest_writes":0,"actual_canonical_validator_calls":0,"eligibility_emissions":0,"retained_release_audit":0,"release_generation":0,"release_qualification":0,"release_copy":0,"release_consumption":0,"network":0,"dns":0,"environment":0,"credentials":0,"device":0,"camera":0,"ray":0,"strip":0,"cleanup":0,"capture":0,"formal":0,"public_analyzer":0,"td_c":0,"sentinel":0,"p8":0,"firmware":0,"deployment":0},"expected_duration":"under_10_minutes","visible_terminal_required":false,"planner_stop":"B2_P4_V1_FINAL_SOURCE_FULL_VALIDATION_WAITING_PLANNER_REVIEW"}`

## 1. Activation 与 immutable target

只有Orchestrator将FULL切换到本task并创建machine row冻结的activation commit后，Executer才可
执行。Activation必须是evidence commit `de50071...`的direct child，subject与exact三路径必须
逐项相等，且activation后porcelain、stage与untracked均为空。Executer不得修改PLAN、FULL、
archive、debug、GUIDE或RESEARCH。

Validation target不是current HEAD的任意working files，而是commit `83bb193...`引入、并由
current activation HEAD ancestry保留的exact two blobs。Preflight只读核对：

1. activation HEAD的parent/subject/exact paths符合本PLAN；
2. implementation commit的parent/subject/exact two paths符合machine row；
3. evidence commit是implementation的direct child且只修改ER；
4. current source/test blob OID与SHA-256 exact等于machine row；
5. dedicated test class仍有exact `14`个 `test_` methods；
6. 初始worktree/stage/untracked为空。

任一preflight drift均fail closed，full process `0`，只append一次FAIL handoff后停在Planner门。
只读Git命令总数不得超过 `8`，不得借此进行retained/Git provenance replay。

## 2. Lifecycle semantic clarification

本PLAN明确替代旧machine row中未限定的 `failure_terminal_attempted_once`：

- `conformance`是pre-effect gate；conformance callback失败直接重新抛原异常，terminal、seal、
  admission attempts均为 `0`。
- 只有`activation`、`root`、`inputs`、`evaluate`是sealed primary phases。其一失败后terminal
  attempt exact `1`；terminal成功后seal attempt exact `1`；seal成功后admission attempt exact
  `1`，最终保留原primary exception identity。

这是对commit `83bb193...`现有实现与tests 11–13的无代码澄清，不授权修改source/test。

## 3. Unique validation execution

Preflight通过后只运行一次：

```bash
PYTHONUNBUFFERED=1 .venv/bin/python -m unittest discover -s tests -p 'test_*.py'
```

必须保留该同一process的terminal exit与完整summary。Acceptance只接受exit `0`、
`Ran 755 tests`、`OK`、failures `0`、errors `0`、skips `0`。不得丢失session后重跑；不得运行
targeted、focused、compileall、CodeGraph或第二个count probe。若process、terminal evidence或
count任一不满足，hard fail并停止。

Full完成后只运行`git diff --check`及只读porcelain核对。不得stage、commit、amend、reset、
revert或push。Executer只向ER追加一次handoff，记录preflight facts、exact command、process
count、exit、Ran/OK summary、duration与全部zero budgets。最终porcelain只允许
`.agent-work/EXECUTION_RESULT.md`一个unstaged modification；stage与untracked必须为空。

## 4. Acceptance 与 hard locks

Acceptance要求：frozen topology/file identity全部exact；dedicated methods exact `14`；唯一final-
source full process exact `755/755`、exit `0`、failures/errors/skips `0`；diff check pass；仅ER发生
一个unstaged append。通过后也只停在Planner门，不自动进入integration。

External controller、qualification/evidence root、旧root/evidence、retained R3 reads、Git
provenance replay、real B2、subordinate manifest、canonical validator、eligibility、release、
network、device、camera、Ray、strip、FORMAL、public analyzer、TD-C、sentinel与P8全部hard
locked `0`。

维护性判断：implementation ownership已在单一pure-in-memory owner内收敛；本包只补最终source
的full regression evidence，不增加代码、抽象或执行路径。
