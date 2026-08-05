# REF-G4-06-REPLACEMENT-PACKAGE Section 2 final snapshot topology repair

**计划状态：** `EXECUTABLE_PENDING_ORCHESTRATOR_ACTIVATION_SECTION_2_FINAL_SNAPSHOT_TOPOLOGY_REPAIR`

**Executable：** `true_after_exact_activation`

**Active task count：** `1`

**Reference task：** `REF-G4-06-REPLACEMENT-PACKAGE`

**Large-change section：** `SECTION_2_REPLACEMENT_TASK_PROJECTION_AND_CHILD_TOPOLOGY`

**Contract：** `G4-R6-LARGE-CHANGE-SECTION-2-FINAL-SNAPSHOT-TOPOLOGY-REPAIR-V1`

**Executer：** `gpt-5.6-sol` / `high`

**唯一 Planner stop：** `RETURN_FOR_G4_06_SECTION_2_FINAL_SNAPSHOT_TOPOLOGY_REPAIR_REVIEW`

`PLAN_MACHINE_CONTRACT={"schema":"planner_execution_contract_v2","contract_id":"G4-R6-LARGE-CHANGE-SECTION-2-FINAL-SNAPSHOT-TOPOLOGY-REPAIR-V1","plan_status":"EXECUTABLE_PENDING_ORCHESTRATOR_ACTIVATION_SECTION_2_FINAL_SNAPSHOT_TOPOLOGY_REPAIR","executable":true,"active_task_count":1,"active_task":"REF-G4-06-REPLACEMENT-PACKAGE","reference_task_id":"REF-G4-06-REPLACEMENT-PACKAGE","reference_goal":"REF-G4-COMPLETE","reference_task_status":"ACTIVE_SECTION_2_FINAL_SNAPSHOT_TOPOLOGY_REPAIR_AFTER_EXACT_ACTIVATION","large_change_section":"SECTION_2_REPLACEMENT_TASK_PROJECTION_AND_CHILD_TOPOLOGY","single_current_action":"replace_the_single_code_owner_subject_with_the_final_snapshot_subject_and_add_durable_subject_blob_topology_regressions","planner_stop":"RETURN_FOR_G4_06_SECTION_2_FINAL_SNAPSHOT_TOPOLOGY_REPAIR_REVIEW","executer":{"role":"Executer","model":"gpt-5.6-sol","reasoning_effort":"high"},"activation_commit":{"expected_parent":"75d327729fdc479b6f9305e4e4a5ca3628fe2346","expected_parent_tree":"342e8c0b4f4444447a635132b0dfe333ef1ca483","expected_subject":"docs(plan): activate section 2 final snapshot topology repair","expected_changed_paths":[".agent-work/EXECUTION_RESULT.md",".agent-work/FULL_PLAN_REFERENCE.md",".agent-work/PLAN-FULL.md",".agent-work/PLAN.md",".agent-work/archived/EXECUTION_RESULT-20260805-0612.md",".agent-work/archived/EXECUTION_RESULT-20260805-0630.md",".agent-work/archived/PLAN-20260805-0612.md",".agent-work/archived/PLAN-20260805-0630.md",".agent-work/debug/INDEX.md",".agent-work/debug/active/20260805-g4-r6-owner-alignment-large-change.md",".agent-work/reviews/20260805-g4-r6-section2-repair-round1.md",".agent-work/reviews/20260805-g4-r6-section2-repair-round2.md"],"direct_non_merge_child":true,"source_test_clean_at_activation":true,"history_rewrite_allowed":false,"future_child_sha_recorded_in_plan":false},"base_repair_commit":{"commit":"75d327729fdc479b6f9305e4e4a5ca3628fe2346","parent":"110730db28d90513928c9b28bc4c49d75eee0c14","tree":"342e8c0b4f4444447a635132b0dfe333ef1ca483","subject":"fix(stage-gate): close section 2 review findings","changed_paths":["src/camera_based_rgbww_optimizer/optimization/p7_td_b_r6_stage_gate.py","tests/test_p7_td_b_r6_stage_gate.py"],"source_bytes":101205,"source_sha256":"97b0a88c338b659ca887dfb626eee11ff96f52712b16a2d6f8b8b7de059298b7","source_blob":"0015d7ce2f2a5dde9118478f98c929020a474a01","test_bytes":152759,"test_sha256":"f86c8dd121b549cf33f8e537454091859e60a466ebed70ff1f077b30defe5add","test_blob":"2a60a987dda02675c2eddc7d8260d61a8f68edc3","disposition":"HISTORICAL_REPAIR_CONTENT_INPUT_NOT_FINAL_CODE_OWNER"},"review_reports":[{"path":".agent-work/reviews/20260805-g4-r6-section2-repair-round1.md","bytes":13441,"sha256":"34d54753d091da3dd639b8be3bc949b4d2d90b8108cd2cc96b3202a704c7fdb3","disposition":"CLEAN_FOR_AUTH_PROV_DELTA_ONLY"},{"path":".agent-work/reviews/20260805-g4-r6-section2-repair-round2.md","bytes":13484,"sha256":"7b5305d804725121e16b670de6e229fadab7f4530a96edc1fd707301f497b9e6","finding":"REV-S2-REPAIR-R2-001","disposition":"ACCEPTED_AGENT_FIXABLE_MUST_FIX"}],"reviewed_archives":{"plan":{"path":".agent-work/archived/PLAN-20260805-0612.md","sha256":"c3e31f53360dd135679cac6a6444e201bd181e57e39114b68cd01febf1f14459"},"execution_result":{"path":".agent-work/archived/EXECUTION_RESULT-20260805-0612.md","sha256":"01cda6e74d68b8ed04f7194d96795081cab8487241fff039dcad73e600c11867"},"superseded_terminal_plan":{"path":".agent-work/archived/PLAN-20260805-0630.md","bytes":8919,"sha256":"1b846d1985481f4e9c98f783a884dc5fd4cd7e3d6f3cdf991f2b887f2d1005a2"},"superseded_terminal_execution_result":{"path":".agent-work/archived/EXECUTION_RESULT-20260805-0630.md","bytes":1818,"sha256":"e798aa471cf0c07a45b5f913970417a2252d707f4ac0d79b339232e83dfb0bb9"}},"finding":{"id":"REV-S2-REPAIR-R2-001","status":"ACCEPTED_AGENT_FIXABLE_MUST_FIX","boundary":"final_repaired_bytes_to_single_direct_code_owner_subject_path_blob_attestation","old_subject":"fix(stage-gate): align replacement package owner","final_subject":"fix(stage-gate): bind final package to immutable code snapshot"},"preserved_closed_findings":{"REV-S2-AUTH-001":"CLOSED_MUST_NOT_CHANGE","REV-S2-PROV-001":"CLOSED_MUST_NOT_CHANGE"},"implementation_scope":{"production_paths":["src/camera_based_rgbww_optimizer/optimization/p7_td_b_r6_stage_gate.py"],"test_paths":["tests/test_p7_td_b_r6_stage_gate.py"],"new_module_cap":0,"new_owner_cap":0,"new_schema_cap":0,"new_controller_adapter_cap":0,"new_task_id_cap":0,"corrective_suffix_cap":0,"new_root_cap":0,"multi_subject_fallback_cap":0,"expected_total_changed_lines_min":40,"expected_total_changed_lines_max":140,"hard_stop_total_changed_lines":200,"bounded_correction_cap":1},"subject_contract":{"final_code_snapshot_subject":"fix(stage-gate): bind final package to immutable code snapshot","allowed_code_child_subject_count":1,"allowed_code_child_subject_must_equal_final_snapshot_subject":true,"old_alignment_subject_accepted":false,"multi_subject_collection_allowed":false,"fallback_subject_allowed":false},"test_contract":{"updated_positive_method":"test_planned_subject_real_topology_binds_exact_two_committed_blobs","updated_old_subject_negative_method":"test_old_alignment_subject_is_rejected_before_package_or_backend","new_old_blob_negative_method":"test_old_alignment_blob_cannot_prove_final_snapshot_bytes","test_subject_oracle_literal":"fix(stage-gate): bind final package to immutable code snapshot","test_oracle_must_not_only_read_production_subject_constant":true,"positive_final_subject_current_blobs_required":true,"negative_old_subject_required":true,"negative_old_blob_required":true,"AUTH_guard_regression":"test_full_projection_rejects_literal_authority_aliases_before_root_effects","PROV_guard_regression":"test_stage_gate_rejects_accepted_engineering_cross_binding_drift","root_backend_device_effect_count":0},"validation_budget":{"exact_topology_targeted_invocations":3,"affected_focused_invocations":1,"stage_gate_focused_invocations":1,"terminal_focused_invocations":1,"compile_invocations":1,"codegraph_sync_invocations":1,"codegraph_query_invocations":1,"valid_full_collection_invocations":1,"valid_full_retry":0},"full_validation":{"classification":"NEW_FINAL_SNAPSHOT_CANDIDATE_COLLECTION_NOT_RETRY","visible_macos_terminal":true,"command":"PYTHONPATH=/Users/ibobby/Projects/WLED-RGBWW /Users/ibobby/Projects/WLED-RGBWW/.venv/bin/python -P -B -m unittest discover -s tests -p 'test_*.py'","forbidden_argument":"-t","effective_collection_required":true,"expected_test_count":982,"acceptance":"FULL_GREEN_OR_EXACT_PRIOR_2_FAILURE_8_ERROR_GOVERNANCE_LINEAGE_GROUP_ONLY","full_green_label_requires_zero_failure_error":true,"flat_evidence_parent":"/Volumes/4T/temp/rgbww-optimizer","new_directory_root_cap":0,"fresh_flat_script_log_seal_allowed":true,"three_sparse_liveness_checks_required_if_running":true,"automation_owner":"Orchestrator"},"eventual_final_code_commit":{"authorized_before_planner_acceptance":false,"expected_parent_kind":"ACTIVATION_DOCS_CHECKPOINT","subject":"fix(stage-gate): bind final package to immutable code snapshot","paths":["src/camera_based_rgbww_optimizer/optimization/p7_td_b_r6_stage_gate.py","tests/test_p7_td_b_r6_stage_gate.py"],"direct_non_merge_child":true,"history_rewrite_allowed":false},"post_commit_real_git_probe":{"owner":"Orchestrator","read_only":true,"required_before_clean_reviews":true,"production_validator_required":true,"final_commit_direct_parent_activation_required":true,"final_commit_subject_exact":true,"final_commit_changed_paths_exact":true,"final_commit_tree_required":true,"final_commit_source_test_blob_oids_match_tree_and_current_files":true,"final_source_references_bytes_sha_mode_exact":true,"positive_final_attestation_required":true,"old_7d02562_blob_oids_must_differ_from_final_current_blobs":true,"old_7d02562_must_fail_to_prove_current_bytes":true,"package_root_access":0,"formal_root_access":0,"device_network_effects":0},"post_commit_review":{"skill":"code-review","model":"gpt-5.6-sol","reasoning_effort":"xhigh","independent_agents_required":true,"consecutive_clean_reviews_required":2,"clean_review_streak_at_activation":0,"accepted_finding_resets_streak":true,"real_git_probe_must_pass_first":true},"required_full_machine_state_after_activation":{"active_task_count":1,"active_task":"REF-G4-06-REPLACEMENT-PACKAGE","active_plan_contract_id":"G4-R6-LARGE-CHANGE-SECTION-2-FINAL-SNAPSHOT-TOPOLOGY-REPAIR-V1","current_plan_active_task_count":1,"current_plan_active_task":"REF-G4-06-REPLACEMENT-PACKAGE","canonical_next_reference_task":"REF-G4-06-REPLACEMENT-PACKAGE","canonical_next_reference_status":"ACTIVE_SECTION_2_FINAL_SNAPSHOT_TOPOLOGY_REPAIR","executable":false,"full_is_non_executable_reference":true,"plan_status":"EXECUTABLE_PENDING_ORCHESTRATOR_ACTIVATION_SECTION_2_FINAL_SNAPSHOT_TOPOLOGY_REPAIR","large_change_workflow":{"current_section":"SECTION_2_REPLACEMENT_TASK_PROJECTION_AND_CHILD_TOPOLOGY","section_1_accepted_commit":"5d01bcbb7e1a9ec1808e2fc05d238363d82a0a74","section_1_clean_review_streak":2,"section_2_base_code_commit":"75d327729fdc479b6f9305e4e4a5ca3628fe2346","section_2_clean_review_streak":0,"section_2_status":"ACTIVE_FINAL_SNAPSHOT_TOPOLOGY_REPAIR","closed_findings":["REV-S2-AUTH-001","REV-S2-PROV-001"],"active_finding":"REV-S2-REPAIR-R2-001"},"replacement_package_authorized":false,"replacement_formal_authorized":false,"formal_execution_authorized":false,"formal_root_creation_authorized":false,"device_authorized":false,"network_authorized":false,"camera_authorized":false,"ray_authorized":false,"strip_authorized":false,"capture_authorized":false,"release_consumption_authorized":false},"required_plan_full_state_after_activation":{"executable":false,"current_section":"SECTION_2_REPLACEMENT_TASK_PROJECTION_AND_CHILD_TOPOLOGY","section_2_status":"ACTIVE_FINAL_SNAPSHOT_TOPOLOGY_REPAIR","section_2_base_code_commit":"75d327729fdc479b6f9305e4e4a5ca3628fe2346","section_2_clean_review_streak":0,"closed_findings":["REV-S2-AUTH-001","REV-S2-PROV-001"],"active_finding":"REV-S2-REPAIR-R2-001"},"package_prepare_authorized":false,"package_describe_authorized":false,"package_root_selection_authorized":false,"package_root_check_authorized":false,"package_root_create_authorized":false,"old_package_access_authorized":false,"old_formal_root_access_authorized":false,"formal_execution_authorized":false,"formal_root_creation_authorized":false,"device_authorized":false,"network_authorized":false,"camera_authorized":false,"ray_authorized":false,"strip_authorized":false,"capture_authorized":false,"cleanup_authorized":false,"release_consumption_authorized":false,"analysis_authorized":false,"g4_07_authorized":false,"td_c_authorized":false}`

## 1. Frozen finding and non-goals

Orchestrator accepts exactly one new Agent-Fixable Must Fix:
`REV-S2-REPAIR-R2-001`. `REV-S2-AUTH-001` and `REV-S2-PROV-001` remain closed
and their production guards, error codes, ordering and independent tests are
immutable regression requirements. Clean-review streak resets to zero.

This is the same stable task and Section 2. Do not rewrite history. Do not add a
suffix, root, module, schema, controller, adapter, second attestation owner or
multi-subject compatibility path. Production/test scope remains the existing
two owner files. Expected repair size is 40–140 changed lines; stop before tests
if the observed total exceeds 200.

## 2. Activation

Orchestrator creates the exact twelve-path direct non-merge governance activation
child specified in the machine row after `75d3277`. FULL and PLAN-FULL must
project the same active repair but remain non-executable. The source/test tree
must be clean and exact to base commit at activation.

Executer validates HEAD/parent/tree/subject/path set, strict PLAN/FULL/PLAN-FULL
agreement, base code commit/tree/source/test blobs, both repair review hashes and
all archive hashes before editing. Drift stops without repair.

## 3. Single-subject topology repair

In the existing production owner, make the existing literal
`FINAL_CODE_SNAPSHOT_SUBJECT` the sole value accepted by
`ALLOWED_CODE_CHILD_SUBJECT`. The sole accepted literal is exactly:

`fix(stage-gate): bind final package to immutable code snapshot`

The old alignment subject must not remain accepted. Do not add a tuple, set,
fallback branch, legacy alias or alternate validator. Preserve exact direct
parent, single-parent, two-path, tree, blob, ancestry and post-child
`.agent-work/`-only checks.

Update the existing synthetic Git fixture/tests so the positive code-owner
commit uses a test-literal final subject and current source/test blobs. The test
must independently assert the production constant equals that literal rather
than deriving its oracle only from the production constant.

Persist negative coverage proving:

1. the old literal `fix(stage-gate): align replacement package owner` fails
   with the subject-drift boundary before package/root/backend effects;
2. an old code-owner blob set cannot attest the current final-snapshot source
   references and reaches `committed_source_candidate_blob_drift` before effects.

Update/rename the two existing topology methods named in the machine row and
add exactly one old-blob negative method. Do not alter package schema or create
a synthetic shortcut that skips the production attestation owner.

## 4. Validation

Run the updated positive, old-subject negative and new old-blob negative methods
as three separate exact unittest invocations. Then run one affected group
containing those three plus the existing AUTH and PROV regression methods. Run
the complete `tests.test_p7_td_b_r6_stage_gate` module once.

Because this subject is consumed by source attestation and persisted replay,
run the actual `tests.test_p7_td_b_r6_terminal` module once. Compile both changed
files, run CodeGraph sync/query, strict machine/scope/single-subject/oracle
checks and `git diff --check`.

At most one bounded correction may address an implementation/test error inside
this exact finding before the final full command. A second same-boundary failure
stops. No edit or redispatch is allowed after full begins.

The source/test bytes change, so prior `981` evidence is historical only. Run
exactly one new final valid full collection in visible macOS Terminal with the
machine-row command, no `-t`, retry zero. Expected count is `982` after the one
new regression method. Full green passes. Otherwise only the exact known ten
`test_p7_thermal_diagnostics` `AGENTS.md` governance-lineage identities with
`2 failures + 8 errors` and no topology/AUTH/PROV/stage-gate/terminal/additional
failure may return as qualified non-green; never call it full green.

Use fresh flat script/log/PID/TTY/exit/count/SHA/seal files directly under
`/Volumes/4T/temp/rgbww-optimizer`; create no directory root and overwrite no
old evidence. Perform three sparse liveness checks if still running, then return
to Orchestrator for automation/block handling. Full retry is zero.

## 5. Handoff and post-commit real-Git proof

Executer may modify only the two existing source/test owners plus live ER and
the existing debug note/index. PLAN, FULL, PLAN-FULL, archives, reviews,
GUIDE/RESEARCH and all other paths are read-only. Executer does not commit.

ER records final identities, numstat, subject-count proof, positive/negative
topology evidence, preserved AUTH/PROV evidence, every validation result,
correction count and zero effects, then stops at:

`RETURN_FOR_G4_06_SECTION_2_FINAL_SNAPSHOT_TOPOLOGY_REPAIR_REVIEW`

After Planner acceptance, Orchestrator creates the exact two-path direct
non-merge child of the governance activation with exact subject
`fix(stage-gate): bind final package to immutable code snapshot`.

Before clean reviews, Orchestrator must run one read-only real-Git attestation
probe through the existing production validator. It must prove the final commit's
direct parent, single parent, exact subject, exact two paths, tree, source/test
blob OIDs and current bytes/SHA/mode; the positive attestation must return the
final commit as code owner. It must also show old `7d02562` blob OIDs differ from
the final current blobs and cannot validate current source references. No
package/formal root or device/network effect is permitted.

Only after that probe passes may Orchestrator obtain two consecutive independent
GPT-5.6 Sol xhigh clean reviews from streak zero. Any accepted finding resets
the streak.
