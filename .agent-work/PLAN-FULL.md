# REF-G4-06 immutable qualification promotion large-change roadmap

**Document status:** `ACTIVE_IMMUTABLE_QUALIFICATION_PROMOTION`

**Executable authority:** `false`

**Stable reference task:** `REF-G4-06-IMMUTABLE-QUALIFICATION-PROMOTION`

**Selected architecture:** `DEDICATED_NON_PRODUCTION_QUALIFICATION_CHECKPOINT_WITH_EXACT_FAST_FORWARD_PROMOTION`

**Orchestration branch:** `codex/g4-r6-owner-alignment-large-change`

**Qualification branch:** `codex/g4-r6-immutable-qualification-q1`

`PLAN_FULL_MACHINE_CONTRACT={"schema":"g4_large_change_plan_full_v8","document_status":"ACTIVE_IMMUTABLE_QUALIFICATION_PROMOTION","executable":false,"active_task_count":1,"active_task":"REF-G4-06-IMMUTABLE-QUALIFICATION-PROMOTION","reference_goal":"REF-G4-COMPLETE","stable_reference_task":"REF-G4-06-IMMUTABLE-QUALIFICATION-PROMOTION","selected_architecture":"DEDICATED_NON_PRODUCTION_QUALIFICATION_CHECKPOINT_WITH_EXACT_FAST_FORWARD_PROMOTION","old_section_2_fourth_repair":false,"corrective_suffix_allowed":false,"orchestration_branch":"codex/g4-r6-owner-alignment-large-change","qualification_branch":"codex/g4-r6-immutable-qualification-q1","current_section":"IMMUTABLE_QUALIFICATION_CHECKPOINT_AND_EXACT_FAST_FORWARD_PROMOTION","current_section_status":"ACTIVE_PENDING_ACTIVATION_A","activation_a":{"expected_parent":"49ad47eceb1bb987eb83107deb8c892d2928c6c5","subject":"docs(plan): activate immutable qualification promotion","direct_single_parent":true,"docs_only":true},"qualification_q":{"status":"NOT_CREATED","direct_parent":"ACTIVATION_COMMIT_A","subject":"fix(stage-gate): bind immutable qualification checkpoint","changed_paths":["src/camera_based_rgbww_optimizer/optimization/p7_td_b_r6_stage_gate.py","tests/test_p7_td_b_r6_stage_gate.py"],"commit_before_tests":true,"source_of_truth":"QUALIFICATION_COMMIT_Q","non_production_pending_validation":true},"identity_documentation":{"required_before_validation":true,"agent_work_only":true,"status":"NOT_CREATED"},"validation":{"committed_q_only":true,"source_test_mutation_allowed":false,"full_suite_budget":1,"full_retry":0,"known_baseline_failures":2,"known_baseline_errors":8},"review":{"planner_review_required":true,"clean_review_count_required":2,"clean_review_model":"gpt-5.6-sol","clean_review_reasoning":"xhigh","must_fix_repair_allowed":false},"promotion":{"authorized":false,"exact_fast_forward_only":true,"cherry_pick_allowed":false,"merge_allowed":false,"rebase_allowed":false,"rebuild_allowed":false},"historical_candidate":{"ref":"refs/heads/codex/historical-g4-r6-section2-final-snapshot-rejected","commit":"3dc2fa2639ee19b1c10ec55e2412836527c8973b","diff_tree_blob_file_read_allowed":false,"reuse_allowed":false},"package_prepare_authorized":false,"package_describe_authorized":false,"package_root_selection_authorized":false,"package_root_check_authorized":false,"package_root_create_authorized":false,"formal_execution_authorized":false,"formal_root_creation_authorized":false,"release_consumption_authorized":false,"device_authorized":false,"network_authorized":false,"camera_authorized":false,"ray_authorized":false,"strip_authorized":false,"capture_authorized":false,"analysis_authorized":false,"g4_07_authorized":false,"td_c_authorized":false}`

## 1. Ownership and immutable inputs

- Orchestrator owns FULL, A, branch topology, Q identity documentation, rejection isolation and eventual promotion.
- Planner owns the single live PLAN and validation review.
- Executer may modify only the two PLAN-authorized source/test owners, create exact Q, and write ER after Q.
- Accepted starting blobs are source `0015d7ce2f2a5dde9118478f98c929020a474a01` and test `2a60a987dda02675c2eddc7d8260d61a8f68edc3`.
- Historical candidate content is forbidden input. Only ref/ancestry isolation checks are allowed.

## 2. Activation A and qualification Q

- A is a docs-only direct child of `49ad47eceb1bb987eb83107deb8c892d2928c6c5` with the exact six paths frozen by PLAN.
- Qualification branch is created from exact A and must not pre-exist or reuse a historical ref.
- Q is A's direct single-parent non-merge child with subject `fix(stage-gate): bind immutable qualification checkpoint` and exact stage-gate source/test paths.
- Q must be committed before any test, compile, import or syntax probe. Pre-Q work is limited to read-only current-source inspection, implementation, path scope and diff checks.
- No amend, Q2, repair commit, rebase, rebuild, merge or cherry-pick is allowed.

## 3. Identity documentation and validation

- After Q, Orchestrator records Q commit/tree/parent/subject/paths and source/test mode/blob/bytes/SHA in `.agent-work/`-only commits.
- Real Git topology and identity must pass before validation. Q source/test remain unchanged at every later tip.
- Focused tests, compile/static, CodeGraph and exactly one full suite run only on committed Q bytes.
- Full acceptance is green or exactly the unrelated known `tests.test_p7_thermal_diagnostics` governance-lineage `2 failures + 8 errors` group with no new identity.
- Any new failure, drift, mutation, extra full need or Must Fix rejects Q without repair or rerun.

## 4. Review and promotion locks

- Planner reviews the committed-Q evidence at `RETURN_FOR_COMMITTED_Q_VALIDATION_REVIEW`.
- A qualified Q requires two consecutive independent GPT-5.6 Sol xhigh clean reviews; any Must Fix rejects it.
- Current PLAN does not authorize promotion. After acceptance, Orchestrator may only exact fast-forward the unchanged orchestration branch from A to the qualification accepted tip.
- Promotion never unlocks package prepare/describe/root, formal, release or device operations.

## 5. Global locks

- GUIDE/RESEARCH, old package/formal roots, external payloads, Retained R3 payload and all devices/network are out of scope.
- Package/formal/release/device/camera/Ray/strip/capture/analysis authority remains false.
- Human goal, GUIDE and scientific stage remain incomplete.
