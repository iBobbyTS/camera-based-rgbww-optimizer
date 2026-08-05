# REF-G4-06-REPLACEMENT-PACKAGE large-change Section 2 alignment

**计划状态：** `EXECUTABLE_PENDING_ORCHESTRATOR_ACTIVATION_LARGE_CHANGE_SECTION_2`

**Executable：** `true_after_exact_activation`

**Active task count：** `1`

**Reference task：** `REF-G4-06-REPLACEMENT-PACKAGE`

**Large-change section：** `SECTION_2_REPLACEMENT_TASK_PROJECTION_AND_CHILD_TOPOLOGY`

**Contract：** `G4-R6-LARGE-CHANGE-SECTION-2-REPLACEMENT-PACKAGE-ALIGNMENT-V1`

**唯一 Planner stop：** `RETURN_FOR_G4_06_LARGE_CHANGE_SECTION_2_CANDIDATE_REVIEW`

`PLAN_MACHINE_CONTRACT={"schema":"planner_execution_contract_v2","contract_id":"G4-R6-LARGE-CHANGE-SECTION-2-REPLACEMENT-PACKAGE-ALIGNMENT-V1","plan_status":"EXECUTABLE_PENDING_ORCHESTRATOR_ACTIVATION_LARGE_CHANGE_SECTION_2","executable":true,"active_task_count":1,"active_task":"REF-G4-06-REPLACEMENT-PACKAGE","reference_task_id":"REF-G4-06-REPLACEMENT-PACKAGE","reference_goal":"REF-G4-COMPLETE","reference_task_status":"ACTIVE_SECTION_2_AFTER_EXACT_ORCHESTRATOR_ACTIVATION","large_change_section":"SECTION_2_REPLACEMENT_TASK_PROJECTION_AND_CHILD_TOPOLOGY","single_current_action":"align_existing_stage_gate_owner_to_replacement_package_task_unfinished_full_projection_and_linear_future_code_child_topology_then_complete_final_offline_validation","planner_stop":"RETURN_FOR_G4_06_LARGE_CHANGE_SECTION_2_CANDIDATE_REVIEW","activation_commit":{"expected_parent":"5d01bcbb7e1a9ec1808e2fc05d238363d82a0a74","expected_parent_tree":"656fee670f289b0a20fea1a8c015762afd44a5c0","expected_subject":"docs(plan): activate section 2 replacement package alignment","expected_changed_paths":[".agent-work/EXECUTION_RESULT.md",".agent-work/FULL_PLAN_REFERENCE.md",".agent-work/PLAN-FULL.md",".agent-work/PLAN.md",".agent-work/archived/EXECUTION_RESULT-20260805-0345.md",".agent-work/archived/PLAN-20260805-0345.md",".agent-work/debug/INDEX.md",".agent-work/debug/active/20260805-g4-r6-owner-alignment-large-change.md",".agent-work/reviews/20260805-g4-r6-section1-round1.md",".agent-work/reviews/20260805-g4-r6-section1-round2.md"],"direct_non_merge_child":true,"plan_version_controlled_before_execution":true,"future_child_sha_recorded_in_plan":false,"excluded_implementation_paths":["src/camera_based_rgbww_optimizer/optimization/p7_td_b_r6_stage_gate.py","tests/test_p7_td_b_r6_stage_gate.py"]},"intake_state":{"full":{"path":".agent-work/FULL_PLAN_REFERENCE.md","bytes":6146,"sha256":"67fdae70ffc514cd94596f2fb80cd5e75f6f79260ff587030e64029bdaf57149","active_task_count":0,"canonical_next_reference_status":"READY_FOR_SECTION_2_PLANNER_PASS"},"plan_full":{"path":".agent-work/PLAN-FULL.md","bytes":15903,"sha256":"22207c52c5519e8d6b120d1c5d8c7036ed451e6935b42c0fc572a86bb4b4ca1e","executable":false,"current_section":"SECTION_2_REPLACEMENT_TASK_PROJECTION_AND_CHILD_TOPOLOGY","section_2_status":"READY_FOR_PLANNER_PASS"}},"section_1_checkpoint":{"commit":"5d01bcbb7e1a9ec1808e2fc05d238363d82a0a74","tree":"656fee670f289b0a20fea1a8c015762afd44a5c0","subject":"fix(stage-gate): bind accepted engineering checkpoint","exact_changed_paths":["src/camera_based_rgbww_optimizer/optimization/p7_td_b_r6_stage_gate.py","tests/test_p7_td_b_r6_stage_gate.py"],"source_bytes":99811,"source_sha256":"2dd469827fff3d6137e247b179035a685b42627aea207b18898a05d36fe18c11","source_blob":"76c8821c915c58e7ad5cdb0133bf2940b51fd1f4","test_bytes":145652,"test_sha256":"891ccbdf3a3b3f62083ea680d8ddce56b6b65c15c40bb5722b95953e729ce056","test_blob":"9b8f5781f175bae1fc93cd398b8bf362c0da20e2","clean_review_streak":2,"reviews":[{"path":".agent-work/reviews/20260805-g4-r6-section1-round1.md","bytes":6472,"sha256":"7217d110fcad26d6389860976b3094d5cdf47a0424d3517c2647823dd7c18096","disposition":"CLEAN_MERGEABLE"},{"path":".agent-work/reviews/20260805-g4-r6-section1-round2.md","bytes":6067,"sha256":"05c9f2209df639d0cf7e68b991ce9ea8ab8c77a7990dbc99b3b7400b0be7e4a1","disposition":"CLEAN_MERGEABLE"}]},"implementation_scope":{"production_owner":"src/camera_based_rgbww_optimizer/optimization/p7_td_b_r6_stage_gate.py","test_owner":"tests/test_p7_td_b_r6_stage_gate.py","existing_production_files_edited":1,"existing_test_files_edited":1,"new_production_modules":0,"new_test_files":0,"new_controller_adapter_cli_schema_family":0,"source_write_cap":1,"test_write_cap":1,"bounded_correction_cap":1,"expected_changed_line_range":[180,420],"changed_line_hard_cap":500,"repo_global_300_limit":false},"projection_contract":{"package_task_id":"REF-G4-06-REPLACEMENT-PACKAGE","package_contract_id":"G4-R6-REPLACEMENT-PACKAGE-OWNER-V1","future_formal_task_id":"REF-G4-06-REPLACEMENT-R6","future_task_must_differ_from_package_task":true,"full_projection":"UNFINISHED_ONLY_CURRENT_G4_REPLACEMENT_STATE","accepted_engineering_checkpoint":"1fbe38d17ec9885dcd5b563edd90359761c51910","accepted_engineering_tree":"9535ac6bcd445898c48ff2227f659d2ea6955e60","retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","all_authority_false":true},"future_code_child_topology":{"verified_parent_is_version_controlled_activation_docs_checkpoint":true,"code_child_direct_non_merge":true,"code_child_subject":"fix(stage-gate): align replacement package owner","code_child_exact_paths":["src/camera_based_rgbww_optimizer/optimization/p7_td_b_r6_stage_gate.py","tests/test_p7_td_b_r6_stage_gate.py"],"candidate_blob_oids_computed_after_edit_before_commit":true,"future_checkpoint_tree_and_blobs_recorded_only_after_commit":true,"self_referential_sha_required":false,"post_child_descendants_agent_work_only_and_linear":true},"validation_budget":{"targeted_invocation_cap":2,"stage_gate_focused_invocation_cap":1,"terminal_focused_invocation_cap":1,"thermal_focused_invocation_cap":1,"compile_invocation_cap":1,"codegraph_sync_cap":1,"codegraph_query_cap":1,"scope_diff_machine_cap":1,"full_unittest_discovery_cap":1,"full_retry_cap":0,"long_full_visible_terminal_required":true,"three_sparse_liveness_checks_required":true,"automation_owner":"Orchestrator"},"eventual_commit":{"authorized_before_planner_acceptance":false,"subject":"fix(stage-gate): align replacement package owner","paths":["src/camera_based_rgbww_optimizer/optimization/p7_td_b_r6_stage_gate.py","tests/test_p7_td_b_r6_stage_gate.py"],"direct_child_of_activation_docs_checkpoint":true},"required_full_machine_state_after_activation":{"active_task_count":1,"active_task":"REF-G4-06-REPLACEMENT-PACKAGE","active_plan_contract_id":"G4-R6-LARGE-CHANGE-SECTION-2-REPLACEMENT-PACKAGE-ALIGNMENT-V1","current_plan_active_task_count":1,"current_plan_active_task":"REF-G4-06-REPLACEMENT-PACKAGE","canonical_next_reference_task":"REF-G4-06-REPLACEMENT-PACKAGE","canonical_next_reference_status":"ACTIVE_SECTION_2_REPLACEMENT_TASK_PROJECTION_AND_CHILD_TOPOLOGY","executable":false,"full_is_non_executable_reference":true,"plan_status":"EXECUTABLE_PENDING_ORCHESTRATOR_ACTIVATION_LARGE_CHANGE_SECTION_2","large_change_workflow":{"current_section":"SECTION_2_REPLACEMENT_TASK_PROJECTION_AND_CHILD_TOPOLOGY","section_1_accepted_commit":"5d01bcbb7e1a9ec1808e2fc05d238363d82a0a74","section_1_accepted_tree":"656fee670f289b0a20fea1a8c015762afd44a5c0","section_1_clean_review_streak":2,"section_2_status":"ACTIVE_AFTER_ORCHESTRATOR_ACTIVATION"},"replacement_package_authorized":false,"replacement_formal_authorized":false,"formal_execution_authorized":false,"formal_root_creation_authorized":false,"device_authorized":false,"network_authorized":false,"camera_authorized":false,"ray_authorized":false,"strip_authorized":false,"capture_authorized":false,"release_consumption_authorized":false},"package_prepare_authorized":false,"package_describe_authorized":false,"package_root_selection_authorized":false,"package_root_check_authorized":false,"package_root_create_authorized":false,"old_package_access_authorized":false,"old_formal_root_access_authorized":false,"formal_execution_authorized":false,"formal_root_creation_authorized":false,"device_authorized":false,"network_authorized":false,"camera_authorized":false,"ray_authorized":false,"strip_authorized":false,"capture_authorized":false,"cleanup_authorized":false,"release_consumption_authorized":false,"analysis_authorized":false,"g4_07_authorized":false,"td_c_authorized":false}`

## 1. Activation and immutable inputs

No implementation or test command may run before Orchestrator creates the exact
direct non-merge activation child defined in the machine row. The activation
commit must version-control this PLAN, the matching active FULL/PLAN-FULL
projection, both `0345` archives, both clean-review reports, ER and debug state.
It must not contain source or test changes.

Executer first verifies activation parent/tree/subject/exact ten-path set,
PLAN/FULL strict parser agreement, active task/contract/section, PLAN-FULL
non-executable status, clean worktree, Section 1 commit/tree/source/test
identities, and both review report hashes. Any mismatch stops without edit.

Section 1 is immutable accepted input. Historical rejected branch/stash,
legacy package/formal roots and external experiment payloads remain forbidden.

## 2. Maintainability preflight and single-owner implementation

The stage-gate owner is already large and contains the canonical provenance,
descriptor, persistence and pre-effect validation seams. Before editing,
Executer uses CodeGraph to confirm that the change can remain inside the
existing owner/test owner without a parallel adapter, controller, schema family,
CLI or helper. If the requested behavior would duplicate serialization,
validation, persistence or root ownership, stop for Orchestrator rather than
adding another owner.

Within those two files only, implement the smallest closed Section 2 change:

1. Align package identity and package contract to
   `REF-G4-06-REPLACEMENT-PACKAGE` /
   `G4-R6-REPLACEMENT-PACKAGE-OWNER-V1`.
2. Keep the later formal task distinct as `REF-G4-06-REPLACEMENT-R6`; do not
   grant formal, device, release or package-consumption authority.
3. Replace archived/completed-prerequisite assumptions with the current
   unfinished-only FULL projection: accepted engineering checkpoint/tree,
   replacement-package state, retained R3 status and every authority false.
4. Preserve Section 1 accepted-engineering validation, descriptor-reference
   precedence, reference-consistent secret/historical guards, persistence,
   replay, artifact inventory, terminal/failure seals and pre-effect ordering.
5. Validate the future code-owner child as a direct non-merge child of the
   already version-controlled activation docs checkpoint, with exact subject,
   two paths, tree/blob identities and linear `.agent-work/`-only descendants.

This PLAN deliberately contains no future child SHA. After the edit, Executer
computes candidate worktree blob OIDs and records them in ER. Planner reviews
those bytes; only then may Orchestrator create the code child. The resulting
commit/tree/blob identities belong in the subsequent orchestration/package PLAN,
never retroactively in this activation PLAN or in the code file itself. This
keeps the topology linear and avoids self-reference.

Expected production/test changed lines are 180–420; hard stop is 500. One
bounded correction is available for the first concrete engineering/test
failure. A repeated failure at the same seam stops for owner-boundary review;
no suffix, alternate owner or additional correction is allowed.

## 3. Required behavior tests

Add meaningful real-behavior assertions in the existing test owner for:

- positive replacement package task/contract, distinct future formal task,
  unfinished-only FULL projection and exact future child topology;
- rejection of the old `REF-G4-06-RAY-R6` task/contract and package/formal task
  collapse;
- archived/completed prerequisite projection, missing or wrong accepted
  engineering identity, any authority bit set, retained-state drift, and
  descriptor projection drift;
- wrong child parent/tree/subject/path/blob, merge child, nonancestor,
  post-child source/test changes and non-`.agent-work/` descendants;
- preservation of descriptor-reference drift precedence and internally
  reference-consistent secret/historical semantic guards;
- every negative failing before output root, delegate/backend, package, formal,
  device, network or release effects.

Tests must assert stable failure codes and zero effects, not only call counts or
fixture construction.

## 4. Validation order and budgets

After the candidate stabilizes:

1. Run exact new/affected tests. Cap is two invocations total: initial and, only
   after the one permitted bounded correction, final.
2. On the final candidate, run exactly once each:
   - `.venv/bin/python -m unittest tests.test_p7_td_b_r6_stage_gate`;
   - `.venv/bin/python -m unittest tests.test_p7_td_b_r6_terminal`;
   - `.venv/bin/python -m unittest tests.test_p7_thermal_diagnostics`.
3. Compile the changed production/test owners once.
4. Run `codegraph sync` once, then one query proving the existing owner remains
   the single task/projection/topology owner and root/persistence ownership did
   not move.
5. Verify exact implementation scope, numstat/hard cap, candidate bytes/SHA/blob,
   activation topology, machine contracts, authority false, no root/effect,
   and `git diff --check`.
6. Only after steps 1–5 pass, consume the entire PLAN-FULL's sole repository
   full-discovery budget with exactly one
   `.venv/bin/python -m unittest discover -s tests -t .` invocation. No retry.

Full green qualifies. If the sole full run is non-green, stop and preserve the
raw identities. Planner may qualify only the already independently attributed
governance-lineage baseline group when test identities and every failure/error
match prior evidence exactly and there is no new failure/error; that outcome
must be labeled qualified non-green, never full green. Any other failure rejects
the candidate without a second full run.

The full discovery is expected to exceed ten minutes. Executer launches it in a
visible macOS Terminal, performs three sparse liveness checks, and then returns
control to Orchestrator. Orchestrator owns any wake automation and blocked/resume
state. On resume there is one status check only. The durable terminal command,
PID/TTY, start/end time, exit code, counts and output identity must be recorded;
this validation scratch is not a package, formal or experiment root.

## 5. Handoff and stop

Executer may change only the source owner, test owner, live ER, active debug note
and debug index. PLAN, PLAN-FULL, FULL, archives, reviews, GUIDE and RESEARCH are
read-only. Executer does not commit.

ER must include activation proof, maintainability preflight, before/after
identities, exact behavior/error matrices, commands/counts/durations/exits,
CodeGraph evidence, full-suite terminal seal, correction count, scope/numstat,
and zero access/effect ledgers.

Success or any failure returns to the single stop:
`RETURN_FOR_G4_06_LARGE_CHANGE_SECTION_2_CANDIDATE_REVIEW`.

Only after Planner acceptance may Orchestrator create
`fix(stage-gate): align replacement package owner` as the direct code child of
the activation docs checkpoint with exactly the two owner paths. This PLAN does
not unlock package/root/prepare/describe, replacement formal R6, device,
network, camera, Ray, strip, capture, release, G4-07 or TD-C.
