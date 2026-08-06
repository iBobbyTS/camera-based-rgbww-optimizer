# REF-G4-06 materialized runtime consumer migration — independent Strategy B candidate

**计划状态：** `EXECUTABLE_PENDING_ORCHESTRATOR_ACTIVATION_ATOMIC_MATERIALIZED_RUNTIME_CONSUMER_MIGRATION_CANDIDATE_2`

**Executable：** `true`（仅表示本 PLAN 可由 Orchestrator 激活；当前尚未授权 Executer）

**Active task count：** `1`

**Active task / stable reference：** `REF-G4-06-MATERIALIZED-RUNTIME-CONSUMER-MIGRATION`

**Contract：** `G4-R6-ATOMIC-MATERIALIZED-RUNTIME-CONSUMER-MIGRATION-V1`

**Candidate identity:** `NEW_INDEPENDENT_STRATEGY_B_CANDIDATE_FROM_ACCEPTED_TREE`

**Planner stop：** `RETURN_FOR_G4_06_ATOMIC_MATERIALIZED_RUNTIME_CONSUMER_MIGRATION_REVIEW`

`PLAN_MACHINE_CONTRACT={"schema":"planner_execution_contract_v2","contract_id":"G4-R6-ATOMIC-MATERIALIZED-RUNTIME-CONSUMER-MIGRATION-V1","plan_status":"EXECUTABLE_PENDING_ORCHESTRATOR_ACTIVATION_ATOMIC_MATERIALIZED_RUNTIME_CONSUMER_MIGRATION_CANDIDATE_2","executable":true,"active_task_count":1,"active_task":"REF-G4-06-MATERIALIZED-RUNTIME-CONSUMER-MIGRATION","reference_task_id":"REF-G4-06-MATERIALIZED-RUNTIME-CONSUMER-MIGRATION","reference_goal":"REF-G4-COMPLETE","reference_task_status":"ACTIVE_AFTER_ORCHESTRATOR_EXACT_MACHINE_ALIGNMENT_ATOMIC_CONSUMER_MIGRATION","candidate_identity":"NEW_INDEPENDENT_STRATEGY_B_CANDIDATE_FROM_ACCEPTED_TREE","prior_candidate_rerun":false,"prior_candidate_repair":false,"historical_candidate_input_allowed":false,"historical_candidate_ref":"refs/heads/codex/historical-g4-r6-atomic-consumer-migration-targeted-rejected","historical_candidate_commit":"7bcc9db0f48e1d798b207e4507c674ea12d3e129","correction_fact":"decode_canonical_json_returns_immutable_mappingproxy; tests_use_json_native_value_and_assert_immutability","production_schema_relaxation":false,"production_scope":["src/camera_based_rgbww_optimizer/optimization/p7_td_b_r6_stage_gate.py","src/camera_based_rgbww_optimizer/optimization/measure_p7_thermal_diagnostics.py","src/camera_based_rgbww_optimizer/optimization/p7_td_b_r6_terminal.py"],"test_scope":["tests/test_p7_td_b_r6_stage_gate.py","tests/test_p7_thermal_diagnostics.py","tests/test_p7_td_b_r6_terminal.py","tests/p7_td_b_r6_materialized_runtime_support.py"],"targeted_invocation_cap":1,"focused_invocation_cap":1,"related_invocation_cap":1,"full_suite_invocation_cap":1,"full_suite_retry":0,"valid_non_green_stop":true,"package_prepare_authorized":false,"package_describe_authorized":false,"package_root_create_authorized":false,"formal_execution_authorized":false,"release_consumption_authorized":false,"device_authorized":false,"network_authorized":false,"camera_authorized":false,"ray_authorized":false,"strip_authorized":false,"capture_authorized":false,"analysis_authorized":false,"g4_07_authorized":false,"td_c_authorized":false,"scientific_result_created":false,"retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","planner_stop":"RETURN_FOR_G4_06_ATOMIC_MATERIALIZED_RUNTIME_CONSUMER_MIGRATION_REVIEW"}`

## 1. Boundary and source-of-truth

This is a new, independently reconstructed Strategy B candidate from the restored accepted tree. It is not a rerun, repair, cherry-pick, merge, rebase, copy, or patch application of the rejected historical candidate. The historical ref and commit above are isolation-only records and are forbidden implementation, production, package, formal, release, or device inputs.

The stage-gate module remains the single production owner for the committed-source attestation schema, canonical JSON serialization, activation construction, materialization, and strict validation. Measure and terminal are consumers only. The shared test support supplies deterministic values and delegates all schema construction to the production owner; it may not define a parallel schema, serializer, validator, digest, or authorizing fixture.

The one absorbed test-contract fact is immutable and non-relaxable: `provenance.decode_canonical_json(...)` returns nested `mappingproxy` values. The canonical round-trip regression must compare `provenance.json_native_value(decoded)` with the expected plain JSON-native value and must separately assert that the decoded mapping remains immutable. No production schema or validator may be widened or made mutable.

## 2. Authorized implementation scope

After Orchestrator activation, Executer may independently implement the complete atomic migration across exactly these paths (plus `.agent-work/EXECUTION_RESULT.md`):

- `src/camera_based_rgbww_optimizer/optimization/p7_td_b_r6_stage_gate.py`
- `src/camera_based_rgbww_optimizer/optimization/measure_p7_thermal_diagnostics.py`
- `src/camera_based_rgbww_optimizer/optimization/p7_td_b_r6_terminal.py`
- `tests/test_p7_td_b_r6_stage_gate.py`
- `tests/test_p7_thermal_diagnostics.py`
- `tests/test_p7_td_b_r6_terminal.py`
- `tests/p7_td_b_r6_materialized_runtime_support.py`

The implementation must construct one nested v2 committed-source attestation, one v3 future activation, and one v2 PLAN-bound authority, with old schemas, flat aliases, unknown fields, type drift, identity/parent/tree/subject/path/blob/reference-digest/post-child-lineage drift rejected before downstream consumers or callbacks. All three production consumers and all three fixture entry points must use the canonical stage-gate owner. The frozen materialized plan must remain immutable while runtime camera settings/provenance travel in independent runtime context and run evidence. Stable underlying error codes and error precedence must remain observable.

Required negative and positive coverage includes canonical deterministic round-trip with mappingproxy immutability, old/new exclusivity, missing/extra/unknown fields, native-type and digest/lineage drift, measure full-chain frozen-plan/runtime-context behavior without mocking `execute_plan`, terminal recognition/replay/finalizer rejection of stale contracts, and fake-only callbacks with zero device/camera/Ray/strip effects.

## 3. Intake and maintainability preflight

Executer must first record in `EXECUTION_RESULT.md`: branch/activation HEAD, clean-tree intake, CodeGraph call paths for the stage-gate owner and all consumers, and the accepted-tree rollback identities. The restored accepted source/test blobs are the only implementation baseline. Existing accepted identities include stage-gate source `0015d7ce2f2a5dde9118478f98c929020a474a01` and stage-gate test `2a60a987dda02675c2eddc7d8260d61a8f68edc3`; the remaining authorized paths must likewise be frozen before edits. No historical candidate diff may be inspected.

Because stage-gate is a large coordinator, keep the change limited to the materialized-runtime ownership boundary and its meaningful tests. Do not introduce a new module/controller or unrelated refactor. If the implementation cannot remain within this atomic scope, stop for Planner/Orchestrator reassessment.

## 4. Validation package and stop rules

Use exactly one fresh root under `/Volumes/4T/temp/rgbww-optimizer/g4-r6-atomic-materialized-runtime-consumer-migration-*`; do not access old roots or payloads. Once qualification starts, source/test/support write cap is zero. Run each gate at most once, in this order:

1. targeted canonical-construction, fixture-delegation, mappingproxy/native round-trip, schema exclusivity, error-precedence, frozen-plan/runtime-context, and terminal negative probes;
2. complete stage-gate focused tests;
3. complete terminal focused tests;
4. complete thermal focused tests;
5. one related stage-gate/terminal/thermal integration run;
6. compile/import/static checks, repo-owned PLAN/FULL parser and machine-state checks, `git diff --check`, and CodeGraph sync/query;
7. exact scope/identity/diff inspection;
8. one full `.venv/bin/python -m unittest discover -s tests` invocation.

Every valid candidate-owned failure, unexpected error, identity drift, callback effect, or out-of-scope change is an immediate fail-closed stop: do not repair, rerun, switch roots, or continue to later gates. Full budget is `1`, retry `0`; targeted/focused/related invocations are also capped at `1` each. A known unrelated governance baseline may be accepted only if its exact identities and first frames match the pre-existing 2 failures + 8 errors contract; no candidate error may be absorbed into it.

If any authorized task is expected to exceed ten minutes, launch it in a visible macOS Terminal, perform three sparse liveness checks, then let Orchestrator handle the automation/blocked protocol. No Codex-managed background owner is permitted.

## 5. Handoff and locks

Executer must write complete evidence, argv, environment, timestamps, counts, natural exits, log bytes/SHA-256, process/automation status, changed paths, and zero external effects to `EXECUTION_RESULT.md`, then stop at `RETURN_FOR_G4_06_ATOMIC_MATERIALIZED_RUNTIME_CONSUMER_MIGRATION_REVIEW`. Executer must not edit PLAN/FULL/PF, commit, push, prepare or consume a package, create a formal root, access release/device/network/camera/Ray/strip/capture, or claim scientific readiness.

Planner will archive this PLAN and the corresponding reviewed EXECUTION_RESULT without overwriting earlier archives, then decide acceptance or rejection. Acceptance only unlocks a later Orchestrator engineering checkpoint/clean review; it does not authorize package, formal, release, device, analysis, G4-07, or TD-C. Retained R3 remains `RETAINED_UNVALIDATED_UNCONSUMED`, and GUIDE/RESEARCH remain immutable.

**Prior reviewed PLAN archive retained:** `.agent-work/archived/PLAN-20260806-0349.md` (SHA-256 `33057e9593ab76d81c9ded529b4fa2df4ed21389fb2d0041b376c5a5b10bbc06`).
