# REF-G4-06 materialized commit attestation engineering package

**计划状态：** `EXECUTABLE_PENDING_ORCHESTRATOR_ACTIVATION_MATERIALIZED_COMMIT_ATTESTATION_ENGINEERING`

**Executable：** `true`

**Active task count：** `1`

**Active task / reference task：** `REF-G4-06-MATERIALIZED-COMMIT-ATTESTATION`

**Contract：** `G4-R6-MATERIALIZED-COMMIT-ATTESTATION-ENGINEERING-V1`

**Planner stop：** `RETURN_FOR_G4_06_MATERIALIZED_COMMIT_ATTESTATION_ENGINEERING_REVIEW`

`PLAN_MACHINE_CONTRACT={"schema":"planner_execution_contract_v2","contract_id":"G4-R6-MATERIALIZED-COMMIT-ATTESTATION-ENGINEERING-V1","plan_status":"EXECUTABLE_PENDING_ORCHESTRATOR_ACTIVATION_MATERIALIZED_COMMIT_ATTESTATION_ENGINEERING","executable":true,"active_task_count":1,"active_task":"REF-G4-06-MATERIALIZED-COMMIT-ATTESTATION","reference_task_id":"REF-G4-06-MATERIALIZED-COMMIT-ATTESTATION","reference_goal":"REF-G4-COMPLETE","reference_task_status":"ACTIVE_AFTER_ORCHESTRATOR_EXACT_MACHINE_ALIGNMENT","architecture":"MATERIALIZE_EXACT_ACCEPTED_COMMIT_IDENTITY_AFTER_COMMIT_AND_VALIDATE_WITHOUT_STATIC_SELF_SUBJECT_OR_BLOB_CONSTANTS","activation_state":"WAITING_ORCHESTRATOR_FULL_AND_PLAN_FULL_ALIGNMENT_AND_FOCUSED_ACTIVATION_COMMIT","required_full_machine_state":{"active_task_count":1,"active_task":"REF-G4-06-MATERIALIZED-COMMIT-ATTESTATION","current_plan_active_task_count":1,"current_plan_active_task":"REF-G4-06-MATERIALIZED-COMMIT-ATTESTATION","active_plan_contract_id":"G4-R6-MATERIALIZED-COMMIT-ATTESTATION-ENGINEERING-V1","canonical_next_reference_task":"REF-G4-06-MATERIALIZED-COMMIT-ATTESTATION","canonical_next_reference_status":"ACTIVE_MATERIALIZED_COMMIT_ATTESTATION_ENGINEERING","executable":false,"full_is_non_executable_reference":true,"plan_status":"EXECUTABLE_PENDING_ORCHESTRATOR_ACTIVATION_MATERIALIZED_COMMIT_ATTESTATION_ENGINEERING"},"accepted_baseline":{"checkpoint":"7a7a3a9800af610a00d47c7cc635a066a7126555","accepted_owner_checkpoint":"75d327729fdc479b6f9305e4e4a5ca3628fe2346","source_blob":"0015d7ce2f2a5dde9118478f98c929020a474a01","test_blob":"2a60a987dda02675c2eddc7d8260d61a8f68edc3"},"superseded_stop_archive":{"path":".agent-work/archived/PLAN-20260806-0106.md","bytes":7389,"sha256":"36d9349babac4dac75883edcb80d2dd2c45f3af5da9f3b201c2f90d43eaa9c5d","source_bytes":6361,"source_sha256":"5797d22be32218d8ef09542810782a06cd0ca99999cf98f14afd2bad03e9cf9e"},"single_current_action":"replace_static_self_and_unborn_child_identity_authority_with_one_materialized_post_commit_attestation_owner_and_validate_it_offline","owner_boundary":"EXISTING_P7_TD_B_R6_STAGE_GATE_SINGLE_OWNER","executor_repo_write_paths":["src/camera_based_rgbww_optimizer/optimization/p7_td_b_r6_stage_gate.py","tests/test_p7_td_b_r6_stage_gate.py",".agent-work/EXECUTION_RESULT.md"],"production_test_paths":["src/camera_based_rgbww_optimizer/optimization/p7_td_b_r6_stage_gate.py","tests/test_p7_td_b_r6_stage_gate.py"],"third_production_or_test_path_allowed":false,"new_module_allowed":false,"new_controller_allowed":false,"parallel_identity_authority_allowed":false,"historical_candidate_input_allowed":false,"historical_q1_input_allowed":false,"historical_v2_input_allowed":false,"static_self_subject_authority_allowed":false,"static_self_blob_authority_allowed":false,"unborn_commit_proof_required":false,"candidate_tests_dynamic_real_git_identity_required":true,"post_accept_materialized_commit_identity_required":true,"future_package_binding_in_current_plan":false,"candidate_commit_by_executer":false,"expected_changed_lines_min":220,"expected_changed_lines_max":380,"hard_changed_lines_cap":420,"large_change_branch":"codex/g4-r6-owner-alignment-large-change","large_change_plan_full_section":"MATERIALIZED_COMMIT_ATTESTATION_OWNER","bounded_harness_correction_cap":1,"production_owner_same_boundary_correction_cap":0,"full_suite_invocation_cap":1,"full_suite_retry":0,"allowed_full_non_green_baseline":{"failures":2,"errors":8,"test_module":"tests.test_p7_thermal_diagnostics","classification":"CURRENT_AGENTS_GOVERNANCE_LINEAGE_IDENTITY_GROUP","exact_test_identities_required":true,"exact_first_failing_frames_required":true,"stage_gate_failure_allowed":false,"materialized_attestation_failure_allowed":false,"changed_owner_failure_allowed":false,"additional_failure_or_error_allowed":false},"package_prepare_authorized":false,"package_describe_authorized":false,"package_root_selection_authorized":false,"package_root_check_authorized":false,"package_root_create_authorized":false,"replacement_package_authorized":false,"replacement_formal_authorized":false,"formal_execution_authorized":false,"formal_root_creation_authorized":false,"release_consumption_authorized":false,"device_authorized":false,"network_authorized":false,"camera_authorized":false,"ray_authorized":false,"strip_authorized":false,"capture_authorized":false,"analysis_authorized":false,"g4_07_authorized":false,"td_c_authorized":false,"scientific_result_created":false,"retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","planner_stop":"RETURN_FOR_G4_06_MATERIALIZED_COMMIT_ATTESTATION_ENGINEERING_REVIEW"}`

## 1. Frozen intake and scope

Executer开始前必须证明：branch为 `codex/g4-r6-owner-alignment-large-change`；HEAD为Orchestrator随后创建的exact activation commit；worktree除PLAN授权写入外干净；PLAN/FULL/PLAN-FULL machine state均为本task active `1/1/1`；accepted source/test起始blob分别为 `0015d7ce2f2a5dde9118478f98c929020a474a01`、`2a60a987dda02675c2eddc7d8260d61a8f68edc3`。

Historical Q1、Section 2和source-attestation-v2 refs只作为禁止输入身份。不得读取其diff/tree/blob/file，亦不得merge、cherry-pick、rebase、copy、复用测试或实现。

唯一production/test scope：

- `src/camera_based_rgbww_optimizer/optimization/p7_td_b_r6_stage_gate.py`
- `tests/test_p7_td_b_r6_stage_gate.py`

Executer只可另写 `.agent-work/EXECUTION_RESULT.md`。若需要第三个production/test/config/wrapper路径、新module或parallel controller，立即停止交Orchestrator，不自行扩大。

## 2. Maintainability preflight

`p7_td_b_r6_stage_gate.py`是巨型高风险provenance owner。编辑前用CodeGraph从accepted tree核对 `validate_committed_source_attestation`、descriptor/binding validator、real-Git fixture与package调用链，并在ER记录：

1. 此改动是替换静态self identity authority，不是增加第二套validator；
2. public persist/replay/production loader继续调用同一canonical stage-gate owner；
3. 不复制Git serialization、path/blob验证或error owner；
4. candidate qualification与future package preparation仍是两个状态边界。

预计production+test changed lines `220..380`，hard cap `420`。当前large-change branch与PLAN-FULL `MATERIALIZED_COMMIT_ATTESTATION_OWNER` section已满足分段治理；若超过420行、需要新module/第三路径或会形成并行权威，停止，不实现。

## 3. Single-owner implementation contract

在现有stage-gate owner内完成最小替换：

1. 移除 `ALLOWED_CODE_CHILD_SUBJECT`、静态code-child blob OID或未出生child identity作为candidate/package放行权威的语义；不得以改名常量继续同一合同。
2. Candidate资格阶段只验证可在当前bytes上证明的schema、closed paths、canonical serialization与fail-closed输入，不要求未来commit SHA/tree/subject/blob。
3. 提供一个明确的materialized commit-attestation值，由后续已存在的accepted code commit生成；它必须包含且仅包含exact checkpoint、tree、唯一direct parent、subject、ordered changed paths、每个允许path的blob OID及必要current-file identity。
4. Production `validate_committed_source_attestation`（或其现有唯一delegate）接收该materialized值，并用read-only real Git验证commit存在、non-merge/direct-parent、tree、subject、ordered path set、mode/blob OID和current bytes；任一未知字段、缺失字段、重复path、顺序漂移、Git/current-byte漂移均fail closed。
5. Descriptor/source-reference完整性仍优先于内容semantic guard；测试必须让每一错误分支真正可达，不能用同一双重非法fixture要求较晚错误码。
6. 既有post-child `.agent-work/` linear lineage、worktree scope、accepted engineering prerequisite与public persist/replay ownership不得放宽或绕过。
7. Future package binding只能在Planner接受候选、Orchestrator创建exact code checkpoint并通过read-only post-commit probe后，由后续PLAN materialize；本PLAN不得prepare/describe/persist/replay/读取任何package。

## 4. Meaningful real-Git regression contract

所有新候选测试必须在各自fresh real-Git fixture中动态创建parent和candidate commit，再从该fixture实际commit读取checkpoint/tree/parent/subject/path/blob identity；不得引用live repo静态subject/blob或预填未来commit。

同一包至少覆盖：

- positive：动态real-Git direct child及合法post-child `.agent-work/` descendants通过；current bytes与commit一致；结果为JSON-native/deterministic；
- negative：missing/extra/unknown/reordered descriptor fields，malformed SHA，duplicate/reordered paths；
- topology：wrong tree/parent/merge/subject/changed path/non-ancestor/non-linear post-child；
- identity：wrong/missing blob、mode drift、tracked/staged/untracked current-byte或worktree scope drift；
- precedence：cross-file/source-reference integrity drift先报对应integrity错误；内部引用一致的semantic fixture分别到达secret/historical prohibitions；
- ownership：public persist/replay/loader仍只绑定canonical owner且无package/device callback；
- fixture isolation：测试只创建fresh scratch，清理后不残留process/root。

不得只修改预期错误码来获得绿色，也不得通过宽泛ignore/allowlist、mock production validator、跳过Git probe或monkey patch global identity实现。

## 5. Execution and validation sequence

1. 记录intake、CodeGraph maintainability preflight和exact baseline identities。
2. 实现single-owner replacement与上述测试；允许当前包内一次仅针对test fixture/validation harness的bounded correction。Harness错误不计production same-boundary失败，但必须保留调用、原因和修正账；production owner实质失败不在本PLAN内修补或重试。
3. 运行新增materialized-attestation targeted tests，要求green。
4. 运行整个 `tests.test_p7_td_b_r6_stage_gate` focused，要求green。
5. 运行相关 thermal diagnostics 与 terminal focused；任何新stage-gate/attestation failure拒绝。既有governance-lineage非绿只能如实列出，不能抵消candidate failure或自动转为接受。
6. 运行 `compileall`/适用static checks、`git diff --check`、exact path/changed-line/historical-string/package-effect scan。
7. 运行 `codegraph sync`，再查询确认只有一个attestation owner和canonical persist/replay/loader调用链。
8. 冻结source/test path、mode、bytes、SHA-256及diff stats；冻结后禁止再写source/test。
9. 对最终冻结candidate运行唯一full unittest discovery。Full budget `1`、retry `0`；不得以targeted/focused green替代。接受门为full完全green，或exactly `2 failures + 8 errors` 且全部test identities与first failing frames逐项匹配既有 `tests.test_p7_thermal_diagnostics` current-AGENTS governance-lineage identity group。该窄基线不允许任何stage-gate、materialized-attestation、changed-owner或额外failure/error；任何数量、identity、first-frame或owner偏离均返回Planner拒绝。
10. 所有scratch/log只可新建于 `/Volumes/4T/temp/rgbww-optimizer/g4-r6-materialized-attestation-*`，不得读取既有root；完成后记录cleanup与process count 0。若单个命令预计超过10分钟，按visible macOS Terminal、三次稀疏liveness及Orchestrator automation规则执行。

禁止单独为test、错误码、validation rerun或ER格式创建新PLAN。Final full后禁止source/test correction与rerun。

## 6. Acceptance, failure and handoff

接受要求：exact scope/hard cap满足；targeted与stage-gate focused green；related无新owner failure；compile/static/CodeGraph/diff/scope通过；frozen candidate唯一full完全green，或仅保留上节逐项匹配的exact `2 failures + 8 errors` governance-lineage窄基线；无package/formal/device/network side effect；historical input access为0。任何stage-gate/materialized-attestation/changed-owner failure或额外failure/error都不可由该基线吸收。

若接受，Executer仍不得commit。ER必须返回候选exact bytes/SHA/mode/diff、全部命令/count/exit/evidence identity、full invocation/retry `1/0`、zero-effect ledger，并停在：

`RETURN_FOR_G4_06_MATERIALIZED_COMMIT_ATTESTATION_ENGINEERING_REVIEW`

Planner接受候选后，Orchestrator才可建立exact code checkpoint并运行一次read-only post-commit materialized-attestation probe。该checkpoint/probe不自动解锁package、formal、release或device；package preparation必须由后续独立PLAN授权。

任何实质owner/identity failure、范围扩大、frozen mutation或full非绿均fail closed并交Planner terminal review；不得在本PLAN创建corrective suffix、Q2、alternate candidate/root或第二full。

## 7. Hard locks

- GUIDE/RESEARCH immutable；Human goal、GUIDE及scientific stage均未完成。
- Retained R3保持 `RETAINED_UNVALIDATED_UNCONSUMED`；旧formal ledger不变，本包不产生科学结果。
- Package prepare/describe/replay/probe/root、replacement formal、release consumption、device/network/camera/Ray/strip/capture/light、analysis、G4-07、TD-C全部为false。
- Executer不得修改PLAN、FULL、PLAN-FULL、archive、debug、config、wrapper、GUIDE或RESEARCH；不得commit、push或创建PR。
