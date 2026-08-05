# REF-G4-06-REPLACEMENT-PACKAGE large-change Section 1 fresh reimplementation

**计划状态：** `EXECUTABLE_PENDING_ORCHESTRATOR_REACTIVATION_LARGE_CHANGE_SECTION_1`

**Executable：** `true_after_exact_activation`

**Active task count：** `1`

**Active reference task：** `REF-G4-06-REPLACEMENT-PACKAGE`

**Large-change section：** `SECTION_1_ACCEPTED_ENGINEERING_CHECKPOINT_BINDING`

**Contract：** `G4-R6-LARGE-CHANGE-SECTION-1-ACCEPTED-ENGINEERING-BINDING-V2`

**唯一 Planner stop：** `RETURN_FOR_G4_06_LARGE_CHANGE_SECTION_1_CANDIDATE_REVIEW`

`PLAN_MACHINE_CONTRACT={"schema":"planner_execution_contract_v2","contract_id":"G4-R6-LARGE-CHANGE-SECTION-1-ACCEPTED-ENGINEERING-BINDING-V2","plan_status":"EXECUTABLE_PENDING_ORCHESTRATOR_REACTIVATION_LARGE_CHANGE_SECTION_1","executable":true,"active_task_count":1,"active_task":"REF-G4-06-REPLACEMENT-PACKAGE","reference_task_id":"REF-G4-06-REPLACEMENT-PACKAGE","reference_goal":"REF-G4-COMPLETE","reference_task_status":"ACTIVE_AFTER_EXACT_ORCHESTRATOR_REACTIVATION_FRESH_LARGE_CHANGE_SECTION_1","large_change_section":"SECTION_1_ACCEPTED_ENGINEERING_CHECKPOINT_BINDING","single_current_action":"fresh_independent_reimplementation_of_closed_accepted_engineering_checkpoint_binding_descriptor_and_git_validator_from_clean_accepted_source","planner_stop":"RETURN_FOR_G4_06_LARGE_CHANGE_SECTION_1_CANDIDATE_REVIEW","activation_commit":{"expected_parent":"e202db90f0ffc38bbdf74a1a6ee01baa72f70e2e","expected_parent_tree":"e855f57b1ffb4a140f6123b5c8f3be8d9fed06fe","expected_subject":"docs(plan): reactivate owner alignment section 1","expected_changed_paths":[".agent-work/EXECUTION_RESULT.md",".agent-work/FULL_PLAN_REFERENCE.md",".agent-work/PLAN-FULL.md",".agent-work/PLAN.md",".agent-work/archived/EXECUTION_RESULT-20260805-0252.md",".agent-work/archived/PLAN-20260805-0252.md",".agent-work/debug/INDEX.md",".agent-work/debug/active/20260805-g4-r6-owner-alignment-large-change.md"],"direct_non_merge_child":true,"orchestration_debug_archive_only":true,"excluded_prefixes":["advisor/","config/","tmp/","src/","tests/"],"child_sha_recorded_in_plan":false},"plan_full":{"path":".agent-work/PLAN-FULL.md","bytes":14174,"sha256":"ac64beaf817de2f620316303772196c156975eec088a3d5e463439b749574d1e","executable":false,"section_count":2,"current_section":"SECTION_1_ACCEPTED_ENGINEERING_CHECKPOINT_BINDING","section_1_status":"FRESH_REIMPLEMENTATION_PENDING_ORCHESTRATOR_ACTIVATION"},"reviewed_plan_archive":{"path":".agent-work/archived/PLAN-20260805-0252.md","bytes":14701,"sha256":"b4bb653a7ddaa121d4c4c2f2ccaa49249d73fe7fe35f70f1664613ef129aa035","immutable":true},"reviewed_execution_result_archive":{"path":".agent-work/archived/EXECUTION_RESULT-20260805-0252.md","bytes":5378,"sha256":"9a7efee123b0aa16c9c746693fcd788b7ef53179057833b6efca0f3239093983","immutable":true},"prior_sizing_failure":{"count":1,"semantic_production_failure_count":0,"historical_peak_changed_lines":228,"old_hard_cap":220,"disposition":"REJECTED_SIZING_CAP_BREACH_NO_SEMANTIC_FAILURE","section_boundary_retained":true},"historical_stash":{"commit":"b62eddd7563af43a20fd66a4960bae386f9ed54e","first_parent":"e202db90f0ffc38bbdf74a1a6ee01baa72f70e2e","exact_changed_paths":["src/camera_based_rgbww_optimizer/optimization/p7_td_b_r6_stage_gate.py","tests/test_p7_td_b_r6_stage_gate.py"],"numstat":{"source_added":105,"source_deleted":1,"test_added":114,"test_deleted":0},"disposition":"HISTORICAL_NON_ACCEPTED_NON_AUTHORIZING","executer_read_count":0,"executer_read_authorized":false,"apply_pop_drop_branch_cherry_pick_copy_authorized":false},"rejected_branch":{"name":"codex/g4-r6-owner-alignment-rejected-305","commit":"1f28b4c04a0ca20888dd5a996af53fc2f3dd0faf","executer_read_count":0,"executer_read_authorized":false,"copy_or_cherry_pick_authorized":false},"implementation_agent":{"role":"Executer","model":"gpt-5.6-sol","reasoning_effort":"medium","implementation_agent_count":1,"independent_from_rejected_inputs":true},"post_commit_review":{"skill":"code-review","model":"gpt-5.6-sol","reasoning_effort":"xhigh","consecutive_clean_reviews_required":2,"finding_repair_model":"gpt-5.6-sol","finding_repair_reasoning_effort":"high","repair_commit_required":true,"clean_streak_resets_after_repair":true},"accepted_engineering_checkpoint":{"checkpoint":"1fbe38d17ec9885dcd5b563edd90359761c51910","tree":"9535ac6bcd445898c48ff2227f659d2ea6955e60","direct_parent":"08e27d0bde5f92f099219683f9dab06951707c07","subject":"fix(formal): preserve frozen plan runtime context","exact_changed_paths":["src/camera_based_rgbww_optimizer/optimization/measure_p7_thermal_diagnostics.py","tests/test_p7_thermal_diagnostics.py"],"blob_oids":[{"path":"src/camera_based_rgbww_optimizer/optimization/measure_p7_thermal_diagnostics.py","oid":"90000ff11a6603fc63515061d391200a46765380"},{"path":"tests/test_p7_thermal_diagnostics.py","oid":"272eacf4c302af5d64483620978411998497b242"}]},"baseline_owner_identity":{"source_path":"src/camera_based_rgbww_optimizer/optimization/p7_td_b_r6_stage_gate.py","source_bytes":94324,"source_sha256":"c4cd13e7fb64434914ccb12c862d1d12e81728a9a647d41ff23fb2d0d860fe83","source_blob":"d47c2ab2655d3e5ec2d425cb225d628d31fd32f2","test_path":"tests/test_p7_td_b_r6_stage_gate.py","test_bytes":133201,"test_sha256":"479dd8d5b0bb851d256045ee1535860ca23328874b7b7a1eb7de76dceb43ab6e","test_blob":"f41d1aa44056efed3e51847f25d3186b769664fd"},"allowed_repo_changed_paths":[".agent-work/EXECUTION_RESULT.md",".agent-work/debug/INDEX.md",".agent-work/debug/active/20260805-g4-r6-owner-alignment-large-change.md","src/camera_based_rgbww_optimizer/optimization/p7_td_b_r6_stage_gate.py","tests/test_p7_td_b_r6_stage_gate.py"],"production_test_expected_changed_line_min":200,"production_test_expected_changed_line_max":260,"production_test_changed_line_hard_cap":300,"source_write_cap":1,"test_write_cap":1,"semantic_candidate_cap":1,"ordinary_harness_correction_cap":1,"full_unittest_discovery_cap":0,"required_full_machine_state":{"active_task_count":1,"active_task":"REF-G4-06-REPLACEMENT-PACKAGE","active_plan_contract_id":"G4-R6-LARGE-CHANGE-SECTION-1-ACCEPTED-ENGINEERING-BINDING-V2","current_plan_active_task_count":1,"current_plan_active_task":"REF-G4-06-REPLACEMENT-PACKAGE","canonical_next_reference_task":"REF-G4-06-REPLACEMENT-PACKAGE","canonical_next_reference_status":"ACTIVE_FRESH_LARGE_CHANGE_SECTION_1_ACCEPTED_ENGINEERING_BINDING","executable":false,"full_is_non_executable_reference":true,"plan_status":"EXECUTABLE_PENDING_ORCHESTRATOR_REACTIVATION_LARGE_CHANGE_SECTION_1","accepted_engineering_checkpoint":"1fbe38d17ec9885dcd5b563edd90359761c51910","accepted_engineering_tree":"9535ac6bcd445898c48ff2227f659d2ea6955e60","retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","replacement_package_authorized":false,"replacement_formal_authorized":false,"formal_execution_authorized":false,"formal_root_creation_authorized":false,"device_authorized":false,"network_authorized":false,"camera_authorized":false,"ray_authorized":false,"strip_authorized":false,"capture_authorized":false,"release_consumption_authorized":false,"g4_07_authorized":false,"td_c_authorized":false,"large_change_workflow":{"required":true,"branch":"codex/g4-r6-owner-alignment-large-change","branch_status":"ACTIVE_FRESH_SECTION_1","plan_full_path":".agent-work/PLAN-FULL.md","current_section":"SECTION_1_ACCEPTED_ENGINEERING_CHECKPOINT_BINDING","section_1_sizing_failure_count":1,"section_1_semantic_failure_count":0,"section_1_accepted_commit":null,"section_1_clean_review_streak":0,"section_2_status":"LOCKED","historical_stash_commit":"b62eddd7563af43a20fd66a4960bae386f9ed54e"}},"task_id_change_authorized":false,"future_task_id_change_authorized":false,"full_projection_change_authorized":false,"code_child_subject_or_topology_change_authorized":false,"package_prepare_authorized":false,"package_describe_authorized":false,"package_root_selection_authorized":false,"package_root_check_authorized":false,"package_root_create_authorized":false,"old_package_access_authorized":false,"old_formal_root_access_authorized":false,"formal_execution_authorized":false,"formal_root_creation_authorized":false,"device_authorized":false,"network_authorized":false,"camera_authorized":false,"ray_authorized":false,"strip_authorized":false,"capture_authorized":false,"cleanup_authorized":false,"release_consumption_authorized":false,"analysis_authorized":false,"g4_07_authorized":false,"td_c_authorized":false,"expected_duration_under_10_minutes":true,"visible_terminal_required":false}`

## 1. Freshness and activation preflight

This is a fresh same-section implementation, not continuation of the rejected
draft. Executer must not inspect, read, diff, show, apply, pop, drop, branch from,
cherry-pick, copy or otherwise consume stash
`b62eddd7563af43a20fd66a4960bae386f9ed54e`, rejected branch
`codex/g4-r6-owner-alignment-rejected-305`, or its commit/diff. The allowed
starting code is only the clean accepted source/test at activation HEAD.

Before editing, Executer verifies:

1. HEAD is the exact direct non-merge child of `e202db90f0ffc38bbdf74a1a6ee01baa72f70e2e`
   with parent tree `e855f57b1ffb4a140f6123b5c8f3be8d9fed06fe`, exact subject
   `docs(plan): reactivate owner alignment section 1`, and exact eight paths in
   the machine row; no source/test/config/tmp/GUIDE/RESEARCH changed.
2. Branch/worktree are exact and clean; PLAN/FULL strict parsers pass active
   `1/1`, matching task/contract/section; FULL is non-executable.
3. PLAN-FULL and immutable 0252 archive identities match.
4. Baseline source/test bytes, hashes and blobs match the machine row.
5. Accepted engineering checkpoint/tree/parent/subject/two paths/two blobs match
   read-only Git.
6. CodeGraph confirms the existing binding→descriptor→Git validator path is the
   single owner and persistence/root paths are outside Section 1.
7. ER records rejected-input read counts `0/0`; no command may address those refs.

Any mismatch writes only ER/debug and stops before source/test edit.

## 2. Exact fresh Section 1 behavior

Independently derive from accepted code one closed change in the existing owner:

1. Add exact accepted-engineering subject/path constants.
2. Extend `_source_attestation_binding` with mandatory checkpoint, tree, direct
   parent, subject, exact paths and exact path/OID rows; missing/extra/malformed,
   reordered or duplicate values fail closed.
3. Project the same closed object through `_committed_source_contract` and
   `_validate_descriptor_attestation_contract`; binding and descriptor must
   agree exactly.
4. Extend `validate_committed_source_attestation` with read-only Git checks for
   commit/tree/direct parent/subject/exact changed paths/blob OIDs and accepted
   checkpoint ancestry to the existing verified parent, with stable errors.
5. Update the existing synthetic real-Git fixture and meaningful positive and
   negative assertions in the existing test owner.

Frozen: `TASK_ID`, `FUTURE_TASK_ID`, `_projection`,
`_validate_prerequisite_projection`, package contract, code-child
subject/topology, schema-family names, CLI, artifacts, persistence, root,
prepare/describe, replay and seals. Descriptor reference integrity remains
first; specialized secret/historical tests use reference-consistent fixtures.

No new module/controller/adapter/schema family, fallback, ignore rule, bypass or
other path is allowed. Section 2 cannot begin.

## 3. Budget and required regression

The corrected expected total production/test changed-line range is 200–260; the
hard stop is 300. Count additions plus deletions across exactly the two owner
paths. If the candidate exceeds 300 at any observation, stop immediately; later
compaction does not revoke the breach.

Tests must prove exact accepted identity success; wrong tree/parent/subject/path
order-set/blob/missing/nonancestor/query failures; closed descriptor shape;
unchanged code-child and `.agent-work/` descendant topology; descriptor drift
precedence; reference-consistent secret/historical guards; and zero package/
device/formal effect ledger. Assertions must cover behavior and error codes.

## 4. Validation ladder

Use one fresh auto-cleaned scratch under
`/Volumes/4T/temp/rgbww-optimizer/g4-lc-section1-fresh-test-*`; it is not an
experiment, package or formal root.

1. Exact new accepted-engineering tests plus existing attestation matrix,
   descriptor reference-precedence, reference-consistent secret/historical, and
   committed-source topology positive/negative tests.
2. Focused once:
   `PYTHONPATH=/Users/ibobby/Projects/WLED-RGBWW TMPDIR=<FRESH> .venv/bin/python -P -B -m unittest tests.test_p7_td_b_r6_stage_gate`
3. Compile the two changed files.
4. `codegraph sync` then query single-owner call path and unchanged persistence.
5. Exact five-path allowed subset, production/test total at most 300,
   PLAN/FULL/PLAN-FULL/GUIDE/RESEARCH/config/tmp and all other source/tests
   unchanged; `git diff --check` passes.

Full discovery is forbidden in Section 1. One harness-only correction is
allowed inside the same test path and cap; a second semantic scheme, second
harness correction, scope widening or any rejected-input read stops.

## 5. Handoff

Executer may write only the two owner paths, live ER, active debug note and
debug INDEX. PLAN/FULL/PLAN-FULL/archives/GUIDE/RESEARCH are read-only. Executer
does not commit.

ER must record activation, freshness/rejected-input read ledger, before/after
identities, exact Git/error/effect matrices, commands/counts/durations/exits,
numstat, CodeGraph, scope and zero authority counters.

Success: `READY_FOR_PLANNER_G4_06_LARGE_CHANGE_SECTION_1_CANDIDATE_REVIEW`

Failure: `READY_FOR_PLANNER_G4_06_LARGE_CHANGE_SECTION_1_FAILURE_REVIEW`

Unique stop: `RETURN_FOR_G4_06_LARGE_CHANGE_SECTION_1_CANDIDATE_REVIEW`

Only after Planner acceptance may Orchestrator create
`fix(stage-gate): bind accepted engineering checkpoint` and start the required
two consecutive independent clean xhigh code-review loop. Section 2 stays locked.

## 6. Authority locks

No package-root select/check/create, public prepare/describe, old roots, device,
network, camera, Ray, strip, capture, cleanup, formal, release, analysis, G4-07,
TD-C, firmware or deployment is authorized.
