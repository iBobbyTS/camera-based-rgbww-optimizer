# REF-G4-06-REPLACEMENT-PACKAGE Section 2 accepted-review finding repair

**计划状态：** `EXECUTABLE_PENDING_ORCHESTRATOR_ACTIVATION_SECTION_2_ACCEPTED_REVIEW_FINDING_REPAIR`

**Executable：** `true_after_exact_activation`

**Active task count：** `1`

**Reference task：** `REF-G4-06-REPLACEMENT-PACKAGE`

**Large-change section：** `SECTION_2_REPLACEMENT_TASK_PROJECTION_AND_CHILD_TOPOLOGY`

**Contract：** `G4-R6-LARGE-CHANGE-SECTION-2-ACCEPTED-REVIEW-FINDING-REPAIR-V1`

**Executer：** `gpt-5.6-sol` / `high`

**唯一 Planner stop：** `RETURN_FOR_G4_06_SECTION_2_ACCEPTED_REVIEW_FINDING_REPAIR_REVIEW`

`PLAN_MACHINE_CONTRACT={"schema":"planner_execution_contract_v2","contract_id":"G4-R6-LARGE-CHANGE-SECTION-2-ACCEPTED-REVIEW-FINDING-REPAIR-V1","plan_status":"EXECUTABLE_PENDING_ORCHESTRATOR_ACTIVATION_SECTION_2_ACCEPTED_REVIEW_FINDING_REPAIR","executable":true,"active_task_count":1,"active_task":"REF-G4-06-REPLACEMENT-PACKAGE","reference_task_id":"REF-G4-06-REPLACEMENT-PACKAGE","reference_goal":"REF-G4-COMPLETE","reference_task_status":"ACTIVE_SECTION_2_ACCEPTED_REVIEW_FINDING_REPAIR_AFTER_EXACT_ACTIVATION","large_change_section":"SECTION_2_REPLACEMENT_TASK_PROJECTION_AND_CHILD_TOPOLOGY","single_current_action":"repair_the_two_orchestrator_accepted_section_2_review_findings_inside_the_existing_stage_gate_owner","planner_stop":"RETURN_FOR_G4_06_SECTION_2_ACCEPTED_REVIEW_FINDING_REPAIR_REVIEW","executer":{"role":"Executer","model":"gpt-5.6-sol","reasoning_effort":"high"},"activation_commit":{"expected_parent":"7d02562db0afcffaa8f2a341345235a6310b654c","expected_parent_tree":"5bfc4b79729cd5cec980cf46090b0e0998153ae4","expected_subject":"docs(plan): activate section 2 review repair","expected_changed_paths":[".agent-work/EXECUTION_RESULT.md",".agent-work/FULL_PLAN_REFERENCE.md",".agent-work/PLAN-FULL.md",".agent-work/PLAN.md",".agent-work/archived/EXECUTION_RESULT-20260805-0515.md",".agent-work/archived/EXECUTION_RESULT-20260805-0530.md",".agent-work/archived/PLAN-20260805-0515.md",".agent-work/archived/PLAN-20260805-0530.md",".agent-work/debug/INDEX.md",".agent-work/debug/active/20260805-g4-r6-owner-alignment-large-change.md",".agent-work/reviews/20260805-g4-r6-section2-round1.md",".agent-work/reviews/20260805-g4-r6-section2-round2.md"],"direct_non_merge_child":true,"source_test_clean_at_activation":true,"future_child_sha_recorded_in_plan":false},"base_code_commit":{"commit":"7d02562db0afcffaa8f2a341345235a6310b654c","parent":"4e94594c117cd684e76b3607815f340cd2ca5919","tree":"5bfc4b79729cd5cec980cf46090b0e0998153ae4","subject":"fix(stage-gate): align replacement package owner","changed_paths":["src/camera_based_rgbww_optimizer/optimization/p7_td_b_r6_stage_gate.py","tests/test_p7_td_b_r6_stage_gate.py"],"source_bytes":99962,"source_sha256":"0ea07b949436599097633c3514f64881e750ed7b45ee92ad88a54e7becee48e0","source_blob":"6f7a7756687f669c067c253a5d5a30f84b5d6075","test_bytes":146189,"test_sha256":"540234e353e43d0a1f8c75f3a71b45dd23ace610e7e96d59e250c88b52c4d352","test_blob":"65e54f1594ed39c2be641124de71b946858c1e6b"},"review_reports":[{"path":".agent-work/reviews/20260805-g4-r6-section2-round1.md","bytes":8970,"sha256":"cdb6ea0246f0f0c0c32f18901262c55396e429c872f6db02cca9647c59a04657","finding":"REV-S2-001","canonical_finding":"REV-S2-PROV-001","disposition":"ACCEPTED_AGENT_FIXABLE_MUST_FIX"},{"path":".agent-work/reviews/20260805-g4-r6-section2-round2.md","bytes":11062,"sha256":"8e3b945ba2f6d68479fefdb002e0f793ea8db46cbbade5952b100a2a7a9a5c58","findings":["REV-S2-R2-001","REV-S2-R2-002"],"canonical_findings":["REV-S2-AUTH-001","REV-S2-PROV-001"],"disposition":"ACCEPTED_AGENT_FIXABLE_MUST_FIX_ROOTS"}],"accepted_findings":{"REV-S2-AUTH-001":{"source":"REV-S2-R2-001","boundary":"unfinished_full_projection_authority_key_closedness","required_error":"machine_contract_drift"},"REV-S2-PROV-001":{"sources":["REV-S2-001","REV-S2-R2-002"],"boundary":"accepted_engineering_prerequisite_to_validated_source_attestation_cross_binding","required_error":"prerequisite_projection_drift"}},"reviewed_archives":{"qualified_plan":{"path":".agent-work/archived/PLAN-20260805-0515.md","sha256":"bab9cfb9c9e8d8def1ee4cbcf71c0052c29f465f6206d7998aa35f01d608d617"},"qualified_execution_result":{"path":".agent-work/archived/EXECUTION_RESULT-20260805-0515.md","sha256":"1702149cb72db4d242b8626a76ae6138c6142dbb1d92f8de299a2dd5b05a2d1b"},"superseded_terminal_plan":{"path":".agent-work/archived/PLAN-20260805-0530.md","bytes":7652,"sha256":"66ce56f1a16da799d4d8c8c7f3232f34dc87e4094193d755bbb86d19a4fe2d70"},"superseded_terminal_execution_result":{"path":".agent-work/archived/EXECUTION_RESULT-20260805-0530.md","bytes":1937,"sha256":"7445e2cd12b6324edea5177382602267591ccf79c26701da1d9d5eb2e6ba3ae7"}},"implementation_scope":{"production_paths":["src/camera_based_rgbww_optimizer/optimization/p7_td_b_r6_stage_gate.py"],"test_paths":["tests/test_p7_td_b_r6_stage_gate.py"],"new_module_cap":0,"new_owner_cap":0,"new_schema_cap":0,"new_controller_adapter_cap":0,"new_task_id_cap":0,"corrective_suffix_cap":0,"new_root_cap":0,"expected_total_changed_lines_min":80,"expected_total_changed_lines_max":180,"hard_stop_total_changed_lines":260,"bounded_correction_cap":1},"authority_contract":{"canonical_current_full_authority_keys":["replacement_package_authorized","replacement_formal_authorized","formal_execution_authorized","formal_root_creation_authorized","device_authorized","network_authorized","camera_authorized","ray_authorized","strip_authorized","capture_authorized","release_consumption_authorized","g4_07_authorized","td_c_authorized"],"forbidden_legacy_and_global_aliases":["formal_r6_authorized","device_authorized_by_this_file","camera_authorized_by_this_file","ray_authorized_by_this_file","strip_authorized_by_this_file","package_prepare_authorized","package_describe_authorized","package_root_selection_authorized","package_root_check_authorized","package_root_create_authorized","old_package_access_authorized","old_formal_root_access_authorized","cleanup_authorized","analysis_authorized","formal_authorized","device_control_authorized","execute_authorized","execution_authorized","materialized_plan_bound_authorized","run_authorized"],"unknown_authority_suffix_sentinel":"future_unlisted_authorized","production_literal_universe_required":true,"production_fail_closed_on_any_noncanonical_top_level_authority_key_presence":true,"canonical_keys_all_exact_false_required":true,"test_oracle_literal_and_independent_from_production_constants":true},"provenance_contract":{"comparison_owner":"validate_stage_gate_existing_owner","prerequisite_fields":["accepted_engineering_checkpoint","accepted_engineering_tree"],"source_attestation_fields":["accepted_engineering.checkpoint","accepted_engineering.tree"],"exact_equality_required_after_source_attestation_validation":true,"format_only_validation_forbidden":true,"parallel_binding_owner_forbidden":true},"test_contract":{"new_exact_test_methods":["test_full_projection_rejects_literal_authority_aliases_before_root_effects","test_stage_gate_rejects_accepted_engineering_cross_binding_drift"],"authority_probe":{"literal_oracle_required":true,"must_cover_all_forbidden_aliases":true,"must_cover_unknown_suffix_sentinel":true,"production_constant_iteration_forbidden":true,"root_backend_device_effect_count":0},"provenance_probe":{"mutations":["checkpoint_only_valid_sha40","tree_only_valid_sha40"],"reference_and_terminal_seal_rebuilt_consistently":true,"descriptor_reference_drift_must_not_shadow":true,"root_backend_formal_device_effect_count":0},"positive_generation_validation_persistence_replay_required":true},"validation_budget":{"targeted_negative_probe_invocations":2,"affected_focused_invocations":1,"stage_gate_focused_invocations":1,"terminal_focused_invocations":1,"thermal_focused_invocations":0,"compile_invocations":1,"codegraph_sync_invocations":1,"codegraph_query_invocations":1,"valid_full_collection_invocations":1,"valid_full_retry":0},"full_validation":{"classification":"NEW_FINAL_CANDIDATE_COLLECTION_NOT_OLD_CANDIDATE_RETRY","visible_macos_terminal":true,"command":"PYTHONPATH=/Users/ibobby/Projects/WLED-RGBWW /Users/ibobby/Projects/WLED-RGBWW/.venv/bin/python -P -B -m unittest discover -s tests -p 'test_*.py'","forbidden_argument":"-t","effective_collection_required":true,"expected_test_count":981,"acceptance":"FULL_GREEN_OR_EXACT_PRIOR_2_FAILURE_8_ERROR_GOVERNANCE_LINEAGE_GROUP_ONLY","full_green_label_requires_zero_failure_error":true,"flat_evidence_parent":"/Volumes/4T/temp/rgbww-optimizer","new_directory_root_cap":0,"fresh_flat_script_log_seal_allowed":true,"three_sparse_liveness_checks_required_if_running":true,"automation_owner":"Orchestrator"},"inherited_evidence":{"base_focused":"51/51_PASS_AT_BASE_BYTES_ONLY","base_valid_full":"979_RUN_969_PASS_2_FAIL_8_ERROR_AT_BASE_BYTES_ONLY","base_invalid_zero_collection_invocation":"PRESERVED_PLANNER_HARNESS_DEFECT","thermal_dedicated":"INHERITED_BASELINE_DIAGNOSTIC_ONLY_NOT_FINAL_REPAIR_EVIDENCE","reason_terminal_rerun":"validate_stage_gate_and_replay_impact","reason_thermal_no_dedicated_rerun":"no_thermal_owner_change_and_new_full_collection_covers_thermal_group"},"eventual_repair_commit":{"authorized_before_planner_acceptance":false,"subject":"fix(stage-gate): close section 2 review findings","paths":["src/camera_based_rgbww_optimizer/optimization/p7_td_b_r6_stage_gate.py","tests/test_p7_td_b_r6_stage_gate.py"],"direct_child_of_activation_docs_checkpoint":true},"post_commit_review":{"skill":"code-review","model":"gpt-5.6-sol","reasoning_effort":"xhigh","independent_agents_required":true,"consecutive_clean_reviews_required":2,"clean_review_streak_at_activation":0,"accepted_finding_resets_streak":true},"required_full_machine_state_after_activation":{"active_task_count":1,"active_task":"REF-G4-06-REPLACEMENT-PACKAGE","active_plan_contract_id":"G4-R6-LARGE-CHANGE-SECTION-2-ACCEPTED-REVIEW-FINDING-REPAIR-V1","current_plan_active_task_count":1,"current_plan_active_task":"REF-G4-06-REPLACEMENT-PACKAGE","canonical_next_reference_task":"REF-G4-06-REPLACEMENT-PACKAGE","canonical_next_reference_status":"ACTIVE_SECTION_2_ACCEPTED_REVIEW_FINDING_REPAIR","executable":false,"full_is_non_executable_reference":true,"plan_status":"EXECUTABLE_PENDING_ORCHESTRATOR_ACTIVATION_SECTION_2_ACCEPTED_REVIEW_FINDING_REPAIR","large_change_workflow":{"current_section":"SECTION_2_REPLACEMENT_TASK_PROJECTION_AND_CHILD_TOPOLOGY","section_1_accepted_commit":"5d01bcbb7e1a9ec1808e2fc05d238363d82a0a74","section_1_clean_review_streak":2,"section_2_base_code_commit":"7d02562db0afcffaa8f2a341345235a6310b654c","section_2_clean_review_streak":0,"section_2_status":"ACTIVE_ACCEPTED_REVIEW_FINDING_REPAIR","accepted_findings":["REV-S2-AUTH-001","REV-S2-PROV-001"]},"replacement_package_authorized":false,"replacement_formal_authorized":false,"formal_execution_authorized":false,"formal_root_creation_authorized":false,"device_authorized":false,"network_authorized":false,"camera_authorized":false,"ray_authorized":false,"strip_authorized":false,"capture_authorized":false,"release_consumption_authorized":false},"required_plan_full_state_after_activation":{"executable":false,"current_section":"SECTION_2_REPLACEMENT_TASK_PROJECTION_AND_CHILD_TOPOLOGY","section_2_status":"ACTIVE_ACCEPTED_REVIEW_FINDING_REPAIR","section_2_base_code_commit":"7d02562db0afcffaa8f2a341345235a6310b654c","section_2_clean_review_streak":0,"accepted_findings":["REV-S2-AUTH-001","REV-S2-PROV-001"]},"package_prepare_authorized":false,"package_describe_authorized":false,"package_root_selection_authorized":false,"package_root_check_authorized":false,"package_root_create_authorized":false,"old_package_access_authorized":false,"old_formal_root_access_authorized":false,"formal_execution_authorized":false,"formal_root_creation_authorized":false,"device_authorized":false,"network_authorized":false,"camera_authorized":false,"ray_authorized":false,"strip_authorized":false,"capture_authorized":false,"cleanup_authorized":false,"release_consumption_authorized":false,"analysis_authorized":false,"g4_07_authorized":false,"td_c_authorized":false}`

## 1. Frozen review decision and maintainability boundary

Orchestrator accepts exactly two Agent-Fixable roots and resets the Section 2
clean-review streak to `0`:

- `REV-S2-AUTH-001`: Round 2 `REV-S2-R2-001`;
- `REV-S2-PROV-001`: merged root of Round 1 `REV-S2-001` and Round 2
  `REV-S2-R2-002`.

This is the same stable task and Section 2. No suffix, new root, new module,
schema family, controller, adapter or semantic owner is allowed. The existing
stage-gate source and test remain the only owners. The repair is expected to be
80–180 changed lines and must stop at 260 before tests.

Maintainability preflight: both findings are pre-effect trust-boundary defects
inside the existing `validate_stage_gate`/FULL projection owner. A local literal
authority vocabulary and one exact cross-binding check reduce ambiguity without
splitting ownership. Any proposal that duplicates source-attestation parsing,
adds a second validator or broadens the package schema stops for Orchestrator.

## 2. Activation and read-only preflight

Orchestrator first creates the exact twelve-path direct non-merge activation
child specified in the machine row. FULL and PLAN-FULL must project the active
repair state but remain non-executable. Executer proves HEAD/parent/tree/subject/
paths, strict PLAN/FULL/PLAN-FULL agreement, base commit identity, both review
hashes, archive hashes and clean source/test before editing.

The review reports and prior invalid zero-collection invocation are immutable.
No old package/formal root, rejected branch, device, network or experiment
payload may be read.

## 3. Repair REV-S2-AUTH-001

Keep the current thirteen canonical FULL authority keys exact and false. In the
same projection owner, define an independent literal authority vocabulary and
fail closed when a top-level authority-shaped key is not one of those thirteen,
including every frozen legacy/global alias and the unknown sentinel in the
machine row. Merely setting an old alias to false is not acceptance: its
presence is noncanonical and must reject as `machine_contract_drift` before
root/backend/device effects.

The test oracle must spell its canonical and forbidden key sets literally. It
must not import, iterate, compare against or otherwise derive expected coverage
from the production authority constant. One table-driven persistent test method
must cover every frozen alias, one unknown `_authorized` sentinel, and a true
value for each canonical key, with zero downstream effects.

Do not change the machine parser, relax unrelated top-level fields, add fallback
authority spellings or introduce a generic policy/controller module.

## 4. Repair REV-S2-PROV-001

Inside `validate_stage_gate`, after the existing source-attestation binding has
passed strict Git/source validation, exact-bind
`prerequisites.accepted_engineering_checkpoint/tree` to that already validated
binding's `accepted_engineering.checkpoint/tree`. The format-only SHA-40 check
may remain subordinate, but it cannot be the semantic acceptance criterion.

Use the existing `prerequisite_projection_drift` fail-closed code. Do not call a
second source-attestation validator, reconstruct a parallel expected binding,
weaken descriptor/reference precedence or change persistence/serialization.

One persistent negative test method must independently mutate checkpoint and
tree to other valid SHA-40 values. It must rebuild the applicable reference and
terminal seal consistently so the dedicated cross-binding guard is reachable
instead of being shadowed by `descriptor_reference_drift`; root/backend/formal/
device effects remain zero. Preserve a positive generate → validate → persist/
replay path using one accepted engineering identity.

## 5. Validation and correction budget

Before any broad suite, run the two new negative methods as two separate exact
unittest invocations. Then run once an affected group containing both new tests,
`test_stage_gate_prerequisite_projection_is_closed`,
`test_package_a_engineering_machine_state_is_not_production_authority`, and
`test_formal_machine_authority_matrix_is_closed_and_pre_backend`. Run the whole
`tests.test_p7_td_b_r6_stage_gate` module once.

Because `validate_stage_gate` feeds persisted/replay boundaries, run
`tests.test_p7_td_b_terminal` once. A dedicated thermal focused rerun is not
required: no thermal owner changes, and the required new full collection covers
the thermal group on final repair bytes. Compile both changed files, run
CodeGraph sync/query, strict machine/scope checks and `git diff --check`.

At most one bounded correction may address a failure attributable to these two
findings before the final full command. It may not add behavior, schema, owner
or test method. A second same-boundary failure stops for Planner. No edit or
redispatch is allowed after the final full command starts.

The old `979` result belongs to base commit bytes and is not final repair
qualification. Run exactly one new valid full collection with the machine-row
command, no `-t`, in visible macOS Terminal. It is a new final-candidate
collection, not a retry of the old candidate. Expected count is `981` after the
two new test methods. Full green passes; otherwise only the exact existing ten
`test_p7_thermal_diagnostics` governance-lineage identities with `2 failures +
8 errors`, and no repair/stage-gate/terminal/additional failure, may be returned
as qualified non-green. Never call that full green.

Use fresh flat script/log/PID/TTY/exit/count/SHA/seal files directly under
`/Volumes/4T/temp/rgbww-optimizer`; do not create a directory root or overwrite
old evidence. Perform three sparse liveness checks if still running. After
survival, return ownership to Orchestrator for its automation/block protocol.
Valid-full retry is zero.

## 6. Handoff and stop

Executer may modify only the two existing source/test owners plus live ER and
the existing debug note/index. PLAN, FULL, PLAN-FULL, archives, reviews,
GUIDE/RESEARCH and all other files are read-only. Executer does not commit.

ER must include final source/test bytes, SHA, blobs, numstat, finding-by-finding
evidence, exact test commands/results, full terminal seal, correction count and
all zero-effect counters.

Unique stop:
`RETURN_FOR_G4_06_SECTION_2_ACCEPTED_REVIEW_FINDING_REPAIR_REVIEW`

After Planner acceptance, Orchestrator creates the exact two-path direct child
commit `fix(stage-gate): close section 2 review findings`, then obtains two new
consecutive independent GPT-5.6 Sol xhigh clean reviews. The streak starts at
zero.
