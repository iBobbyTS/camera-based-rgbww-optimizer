# REF-G4-06-REPLACEMENT-PACKAGE Section 2 frozen-candidate final qualification

**计划状态：** `EXECUTABLE_PENDING_ORCHESTRATOR_ACTIVATION_SECTION_2_FINAL_QUALIFICATION`

**Executable：** `true_after_exact_activation`

**Active task count：** `1`

**Reference task：** `REF-G4-06-REPLACEMENT-PACKAGE`

**Large-change section：** `SECTION_2_REPLACEMENT_TASK_PROJECTION_AND_CHILD_TOPOLOGY`

**Contract：** `G4-R6-LARGE-CHANGE-SECTION-2-FROZEN-CANDIDATE-FINAL-QUALIFICATION-V1`

**唯一 Planner stop：** `RETURN_FOR_G4_06_LARGE_CHANGE_SECTION_2_FINAL_QUALIFICATION_REVIEW`

`PLAN_MACHINE_CONTRACT={"schema":"planner_execution_contract_v2","contract_id":"G4-R6-LARGE-CHANGE-SECTION-2-FROZEN-CANDIDATE-FINAL-QUALIFICATION-V1","plan_status":"EXECUTABLE_PENDING_ORCHESTRATOR_ACTIVATION_SECTION_2_FINAL_QUALIFICATION","executable":true,"active_task_count":1,"active_task":"REF-G4-06-REPLACEMENT-PACKAGE","reference_task_id":"REF-G4-06-REPLACEMENT-PACKAGE","reference_goal":"REF-G4-COMPLETE","reference_task_status":"ACTIVE_SECTION_2_FROZEN_CANDIDATE_FINAL_QUALIFICATION_AFTER_EXACT_ACTIVATION","large_change_section":"SECTION_2_REPLACEMENT_TASK_PROJECTION_AND_CHILD_TOPOLOGY","single_current_action":"qualify_the_exact_frozen_section_2_candidate_with_one_post_correction_stage_gate_focused_run_and_one_valid_repository_full_collection","planner_stop":"RETURN_FOR_G4_06_LARGE_CHANGE_SECTION_2_FINAL_QUALIFICATION_REVIEW","review_disposition":"SEMANTICALLY_ACCEPTABLE_PENDING_FROZEN_CANDIDATE_FINAL_QUALIFICATION","activation_commit":{"expected_parent":"1f7556d36049c33bd4f99412d945db02fe448fa8","expected_parent_tree":"813d90d31fa4a4650ef4ccde338f64db30eaaada","expected_subject":"docs(plan): qualify section 2 frozen candidate","expected_changed_paths":[".agent-work/EXECUTION_RESULT.md",".agent-work/FULL_PLAN_REFERENCE.md",".agent-work/PLAN-FULL.md",".agent-work/PLAN.md",".agent-work/archived/EXECUTION_RESULT-20260805-0435.md",".agent-work/archived/PLAN-20260805-0435.md",".agent-work/debug/INDEX.md",".agent-work/debug/active/20260805-g4-r6-owner-alignment-large-change.md"],"direct_non_merge_child":true,"plan_version_controlled_before_validation":true,"implementation_paths_must_remain_dirty_unstaged":true,"future_child_sha_recorded_in_plan":false},"reviewed_archives":{"plan":{"path":".agent-work/archived/PLAN-20260805-0435.md","bytes":2578,"sha256":"0f73e25257ae85a081431745d815adcedcb673ab074713121e20c9243abd8ad5","version_controlled_source":"1f7556d36049c33bd4f99412d945db02fe448fa8:.agent-work/PLAN.md","source_bytes":15260,"source_sha256":"3344aa363f98829e88eaa6d3641b14ee8c23aa1965b497432eac31dd7ff86d82"},"execution_result":{"path":".agent-work/archived/EXECUTION_RESULT-20260805-0435.md","bytes":11291,"sha256":"5684e33970ad776c1cc3d14867e2688fbbd0a4513b02bbb0b6cc436845c4ad8f","source_bytes":7743,"source_sha256":"f88479ccd88ff3ba66a87ee694ccee50f4c0d5da6f74e1bc23ad91435554c659"}},"frozen_candidate":{"source_path":"src/camera_based_rgbww_optimizer/optimization/p7_td_b_r6_stage_gate.py","source_bytes":99962,"source_sha256":"0ea07b949436599097633c3514f64881e750ed7b45ee92ad88a54e7becee48e0","source_blob":"6f7a7756687f669c067c253a5d5a30f84b5d6075","source_numstat":{"added":102,"deleted":90},"test_path":"tests/test_p7_td_b_r6_stage_gate.py","test_bytes":146189,"test_sha256":"540234e353e43d0a1f8c75f3a71b45dd23ace610e7e96d59e250c88b52c4d352","test_blob":"65e54f1594ed39c2be641124de71b946858c1e6b","test_numstat":{"added":123,"deleted":140},"total_changed_lines":455,"semantic_review":"ACCEPTABLE_FOR_FINAL_QUALIFICATION","committed":false},"write_contract":{"production_source_write_cap":0,"test_source_write_cap":0,"other_repo_write_cap":0,"new_implementation_package_cap":0,"new_task_id_cap":0,"corrective_suffix_cap":0,"new_package_formal_experiment_root_cap":0},"inherited_validation":{"targeted_initial":"8/8_PASS","bounded_correction_count":1,"bounded_correction_scope":"TEST_FIXTURE_PROJECTION_CONTRACT_COPY_ONLY","targeted_final":"1/1_PASS","terminal_focused":"6/6_PASS","thermal_focused":"89_RUN_79_PASS_2_FAIL_8_ERROR_PREEXISTING_GOVERNANCE_LINEAGE_BASELINE","compile":"PASS","codegraph":"PASS","scope_diff_machine":"PASS","external_effect_count":0},"invalid_full_invocation":{"command":".venv/bin/python -m unittest discover -s tests -t .","classification":"PLANNER_COMMAND_HARNESS_CONTRACT_ERROR_BEFORE_COLLECTION","exit":1,"collected_tests":0,"output_sha256":"192c78c880e975096c5f4fe40292ad9c14c1c865cff1714c2fc2ba4d9e908703","historical_invocation_count":1,"production_semantic_failure_increment":0,"full_test_failure_increment":0,"valid_full_collection_budget_consumed":false,"full_retry_increment":0,"must_remain_recorded":true},"qualification_budget":{"post_correction_stage_gate_focused_invocation_cap":1,"valid_full_collection_invocation_cap":1,"valid_full_collection_retry_cap":0,"terminal_focused_invocation_cap":0,"thermal_focused_invocation_cap":0,"targeted_invocation_cap":0,"compile_invocation_cap":0,"codegraph_sync_cap":0,"codegraph_query_cap":0,"production_test_correction_cap":0},"valid_full_command":{"argv":["/usr/bin/env","PYTHONPATH=/Users/ibobby/Projects/WLED-RGBWW","/Users/ibobby/Projects/WLED-RGBWW/.venv/bin/python","-P","-B","-m","unittest","discover","-s","tests","-p","test_*.py"],"shell":"PYTHONPATH=/Users/ibobby/Projects/WLED-RGBWW /Users/ibobby/Projects/WLED-RGBWW/.venv/bin/python -P -B -m unittest discover -s tests -p 'test_*.py'","forbidden_argument":"-t","effective_collection_required":true},"terminal_evidence":{"visible_macos_terminal":true,"flat_parent":"/Volumes/4T/temp/rgbww-optimizer","new_directory_root_cap":0,"fresh_flat_script_log_seal_files_allowed":true,"three_sparse_liveness_checks_if_still_running":true,"automation_owner":"Orchestrator","full_retry_cap":0},"eventual_commit":{"authorized_before_planner_acceptance":false,"subject":"fix(stage-gate): align replacement package owner","paths":["src/camera_based_rgbww_optimizer/optimization/p7_td_b_r6_stage_gate.py","tests/test_p7_td_b_r6_stage_gate.py"],"direct_child_of_qualification_activation_docs_checkpoint":true},"required_full_machine_state_after_activation":{"active_task_count":1,"active_task":"REF-G4-06-REPLACEMENT-PACKAGE","active_plan_contract_id":"G4-R6-LARGE-CHANGE-SECTION-2-FROZEN-CANDIDATE-FINAL-QUALIFICATION-V1","current_plan_active_task_count":1,"current_plan_active_task":"REF-G4-06-REPLACEMENT-PACKAGE","canonical_next_reference_task":"REF-G4-06-REPLACEMENT-PACKAGE","canonical_next_reference_status":"ACTIVE_SECTION_2_FROZEN_CANDIDATE_FINAL_QUALIFICATION","executable":false,"full_is_non_executable_reference":true,"plan_status":"EXECUTABLE_PENDING_ORCHESTRATOR_ACTIVATION_SECTION_2_FINAL_QUALIFICATION","large_change_workflow":{"current_section":"SECTION_2_REPLACEMENT_TASK_PROJECTION_AND_CHILD_TOPOLOGY","section_1_accepted_commit":"5d01bcbb7e1a9ec1808e2fc05d238363d82a0a74","section_1_clean_review_streak":2,"section_2_status":"ACTIVE_FROZEN_CANDIDATE_FINAL_QUALIFICATION"},"replacement_package_authorized":false,"replacement_formal_authorized":false,"formal_execution_authorized":false,"formal_root_creation_authorized":false,"device_authorized":false,"network_authorized":false,"camera_authorized":false,"ray_authorized":false,"strip_authorized":false,"capture_authorized":false,"release_consumption_authorized":false},"package_prepare_authorized":false,"package_describe_authorized":false,"package_root_selection_authorized":false,"package_root_check_authorized":false,"package_root_create_authorized":false,"old_package_access_authorized":false,"old_formal_root_access_authorized":false,"formal_execution_authorized":false,"formal_root_creation_authorized":false,"device_authorized":false,"network_authorized":false,"camera_authorized":false,"ray_authorized":false,"strip_authorized":false,"capture_authorized":false,"cleanup_authorized":false,"release_consumption_authorized":false,"analysis_authorized":false,"g4_07_authorized":false,"td_c_authorized":false}`

## 1. Planner decision and frozen boundary

The Section 2 implementation is semantically acceptable for final
qualification. It remains unaccepted and uncommitted because the final
candidate never received a complete post-correction stage-gate focused result
or an effective repository full collection.

The invalid `-t .` invocation is permanently preserved in the reviewed ER
archive. Because `tests/` has no `__init__.py`, unittest rejected that start
directory before collecting any test. This is a Planner command/harness defect,
not a production semantic failure, full-test failure, retry, Human/Advisor gate,
or consumption of the effective full-collection budget.

Production and test bytes are now frozen exactly to the machine row. Source and
test writes are both zero. No correction, fixture edit, refactor, new owner,
task suffix, implementation package or package/formal/experiment root is
authorized.

## 2. Activation

Orchestrator must first create the exact direct non-merge docs child specified
in the machine row. FULL and PLAN-FULL must project the same frozen-candidate
qualification state. The dirty source/test candidate stays unstaged and its
bytes/SHA/blob/numstat identities must not change across activation.

Executer validates the activation topology, exact eight-path set, committed
PLAN, PLAN/FULL machine agreement, PLAN-FULL non-executable status, archive
hashes and candidate identities before any command. Drift stops without repair.

## 3. Only two qualification commands

First run exactly once on the frozen candidate:

`PYTHONPATH=/Users/ibobby/Projects/WLED-RGBWW /Users/ibobby/Projects/WLED-RGBWW/.venv/bin/python -P -B -m unittest tests.test_p7_td_b_r6_stage_gate`

This is the missing post-correction focused qualification. It is not a second
production correction or a full retry. It must complete the whole module with
no failure/error. No edit may follow it.

If and only if focused is green and identities remain frozen, run exactly once:

`PYTHONPATH=/Users/ibobby/Projects/WLED-RGBWW /Users/ibobby/Projects/WLED-RGBWW/.venv/bin/python -P -B -m unittest discover -s tests -p 'test_*.py'`

The `-t` argument is forbidden. A valid run must collect at least one test and
reach a unittest terminal summary. No redispatch or retry is allowed.

Full green qualifies. A non-green run may be classified only as qualified
baseline when it has exactly two failures and eight errors, every traceback
terminates first at the already attributed governance-lineage rejection of the
current `AGENTS.md` identity, no changed-owner/stage-gate/terminal test fails,
and no additional failure/error appears. Such a result is never called green.
Any other non-green result stops for Planner rejection.

Existing targeted, terminal, thermal, compile, CodeGraph and scope evidence is
inherited and must not be rerun. Read-only identity, status, process and
`git diff --check` checks do not consume test budgets.

## 4. Terminal and evidence discipline

Run the valid full command in visible macOS Terminal. Do not create a new
directory root. A fresh flat script and stdout/stderr/PID/exit/seal files may be
created directly under `/Volumes/4T/temp/rgbww-optimizer`; they must not
overwrite the invalid invocation's immutable script or evidence root.

If still running, perform three sparse liveness checks and return to
Orchestrator for the established automation/block protocol. If already
complete, do not invent missing checks or create automation. Record exact argv,
PID/TTY, timestamps, collected/passed/skipped/failure/error counts, terminal
summary, exit and every evidence-file identity.

## 5. Handoff and stop

Executer may update only live ER and the existing debug note/index. PLAN,
PLAN-FULL, FULL, archives, reviews, source/tests, GUIDE and RESEARCH are
read-only. No commit is authorized.

ER must preserve the invalid invocation ledger beside the new focused/full
evidence, prove candidate identity stability and report all authority/effect
counts as zero.

Unique stop:
`RETURN_FOR_G4_06_LARGE_CHANGE_SECTION_2_FINAL_QUALIFICATION_REVIEW`
