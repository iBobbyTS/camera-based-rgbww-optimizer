# REF-G4-06-REPLACEMENT-PACKAGE large-change implementation plan

**Document status:** `NON_EXECUTABLE_LARGE_CHANGE_SECTION_ROADMAP`

**Executable authority:** `false`

**Stable reference task:** `REF-G4-06-REPLACEMENT-PACKAGE`

**Branch:** `codex/g4-r6-owner-alignment-large-change`

**Base checkpoint:** `3c920c6d29e5c366ce3843a2532d30d80c6f0c33`

**Base tree:** `e7d20cd3ac98f21d3af5cb9d43d31ed40e00ec6d`

`PLAN_FULL_MACHINE_CONTRACT={"schema":"g4_large_change_plan_full_v1","document_status":"NON_EXECUTABLE_LARGE_CHANGE_SECTION_ROADMAP","executable":false,"reference_goal":"REF-G4-COMPLETE","stable_reference_task":"REF-G4-06-REPLACEMENT-PACKAGE","corrective_suffix_allowed":false,"branch":"codex/g4-r6-owner-alignment-large-change","base_checkpoint":"3c920c6d29e5c366ce3843a2532d30d80c6f0c33","base_tree":"e7d20cd3ac98f21d3af5cb9d43d31ed40e00ec6d","rejected_draft":{"branch":"codex/g4-r6-owner-alignment-rejected-305","commit":"1f28b4c04a0ca20888dd5a996af53fc2f3dd0faf","disposition":"REJECTED_INCOMPLETE_UNVALIDATED_READ_ONLY_DESIGN_INPUT","cherry_pick_allowed":false,"copy_as_production_truth_allowed":false},"section_count":2,"current_section":"SECTION_1_ACCEPTED_ENGINEERING_CHECKPOINT_BINDING","section_1_sizing_review":{"disposition":"REJECTED_PLAN_CAP_BREACH_NO_SEMANTIC_FAILURE","historical_peak_changed_lines":228,"live_changed_lines":220,"old_hard_cap":220,"section_boundary":"RETAINED_ATOMIC","section_boundary_reason":"binding_descriptor_git_validator_and_protective_fixture_must_coevolve","fresh_reimplementation_required":true,"rejected_draft_reuse_allowed":false,"historical_stash":{"commit":"b62eddd7563af43a20fd66a4960bae386f9ed54e","parent":"e202db90f0ffc38bbdf74a1a6ee01baa72f70e2e","changed_paths":["src/camera_based_rgbww_optimizer/optimization/p7_td_b_r6_stage_gate.py","tests/test_p7_td_b_r6_stage_gate.py"],"numstat":{"source_added":105,"source_deleted":1,"test_added":114,"test_deleted":0},"disposition":"HISTORICAL_NON_ACCEPTED_NON_AUTHORIZING","read_allowed_by_fresh_executer":false,"apply_pop_drop_branch_copy_allowed":false},"replacement_expected_range":[200,260],"replacement_hard_cap":300},"sections":[{"section":"SECTION_1_ACCEPTED_ENGINEERING_CHECKPOINT_BINDING","status":"BOUNDED_DURABLE_OSERROR_REGRESSION_PENDING_ORCHESTRATOR_ACTIVATION","production_owner":"src/camera_based_rgbww_optimizer/optimization/p7_td_b_r6_stage_gate.py","test_owner":"tests/test_p7_td_b_r6_stage_gate.py","commit_subject":"fix(stage-gate): bind accepted engineering checkpoint","switch_package_task":false,"change_full_projection":false,"package_root_access":0},{"section":"SECTION_2_REPLACEMENT_TASK_PROJECTION_AND_CHILD_TOPOLOGY","status":"LOCKED_PENDING_SECTION_1_COMMIT_AND_TWO_CLEAN_REVIEWS","production_owner":"src/camera_based_rgbww_optimizer/optimization/p7_td_b_r6_stage_gate.py","test_owner":"tests/test_p7_td_b_r6_stage_gate.py","commit_subject":"fix(stage-gate): align replacement package owner","switch_package_task":true,"change_full_projection":true,"package_root_access":0}],"implementation_agent":{"model":"gpt-5.6-sol","reasoning_effort":"medium","role":"Executer"},"post_commit_review":{"skill":"code-review","model":"gpt-5.6-sol","reasoning_effort":"xhigh","consecutive_clean_reviews_required":2,"independent_review_agents_required":true,"finding_repair_model":"gpt-5.6-sol","finding_repair_reasoning_effort":"high","repair_commit_required":true,"clean_streak_resets_after_repair":true},"section_1_bounded_correction":{"production_source_frozen":true,"source_write_cap":0,"test_write_cap":1,"required_durable_regression":"subject_subprocess_run_raises_oserror_to_committed_source_engineering_ancestry_query_failed","preserve_returncode_2":true,"preserve_nonancestor":true,"expected_final_changed_line_range":[300,320],"final_changed_line_hard_cap":330,"repo_global_300_limit":false,"affected_exact_tests_required":true,"focused_final_candidate_invocation_cap":1,"full_discovery_cap":0,"other_code_test_correction_allowed":false},"section_1_v2_review":{"candidate_numstat":295,"source_identity":{"sha256":"2dd469827fff3d6137e247b179035a685b42627aea207b18898a05d36fe18c11","blob":"76c8821c915c58e7ad5cdb0133bf2940b51fd1f4"},"test_identity":{"sha256":"2a412e2b405c7ddf59146fb522da3afaf84e66b106e50b3989552371dad30d17","blob":"efe7a16ff415b6e1397c8d11865423314662a82c"},"ownership_closed_shape_precedence_zero_effects":"ACCEPTED_FOR_CORRECTION_INPUT_ONLY","targeted":"15/15_PASS","focused":"50/50_PASS_BEFORE_LATE_OSERROR_CHANGE","late_probe":"1/1_PASS_NON_DURABLE","final_qualification":"REJECTED_MISSING_DURABLE_SUBPROCESS_OSERROR_REGRESSION","semantic_production_failure_count":0,"validation_qualification_failure_count":1,"section_2_locked":true},"single_full_suite_owner_section":"SECTION_2_REPLACEMENT_TASK_PROJECTION_AND_CHILD_TOPOLOGY","full_suite_invocation_cap":1,"package_prepare_authorized":false,"package_describe_authorized":false,"package_root_selection_authorized":false,"package_root_check_authorized":false,"package_root_create_authorized":false,"old_package_access_authorized":false,"old_formal_root_access_authorized":false,"formal_execution_authorized":false,"formal_root_creation_authorized":false,"device_authorized":false,"network_authorized":false,"camera_authorized":false,"ray_authorized":false,"strip_authorized":false,"capture_authorized":false,"cleanup_authorized":false,"release_consumption_authorized":false,"analysis_authorized":false,"g4_07_authorized":false,"td_c_authorized":false}`

## 1. Purpose and governing boundary

This document exists because the prior non-trivial owner-alignment candidate
reached an observed 305 changed lines. The applicable top-level AGENTS rule
therefore requires an isolated Git branch, a PLAN-FULL section roadmap, one
implementation subagent per section, focused commits, clean worktrees between
sections, and post-commit review loops.

PLAN-FULL is context only. It does not authorize implementation, tests, commits,
root access, package preparation, device access, formal execution, or release.
Only the single live `.agent-work/PLAN.md` can release the current section.

The rejected branch and commit are historical evidence only. An implementation
agent may read the frozen failure/contract description but must derive its edit
from the accepted branch source. It may not cherry-pick, apply, copy, or treat
the rejected diff as production truth.

## 2. Ownership and invariants shared by both sections

- Stable reference task remains `REF-G4-06-REPLACEMENT-PACKAGE`; section names
  are workflow labels, not new task IDs.
- Existing production owner remains
  `camera_based_rgbww_optimizer.optimization.p7_td_b_r6_stage_gate` and its
  existing test owner remains `tests/test_p7_td_b_r6_stage_gate.py`.
- No new production module, schema family, runner, controller, adapter, CLI,
  artifact, persistence owner, root-selection owner, or replay owner is allowed.
- Existing exclusive root creation, canonical persistence, exact inventory,
  internal replay, terminal seal, public replay and failure seal are frozen.
- Integrity-first descriptor ordering is frozen:
  stale bytes/SHA references fail as `descriptor_reference_drift`; the secret
  and historical semantic guards are tested only with internally
  reference-consistent fixtures.
- Accepted engineering prerequisite remains commit
  `1fbe38d17ec9885dcd5b563edd90359761c51910`, tree
  `9535ac6bcd445898c48ff2227f659d2ea6955e60`, direct parent
  `08e27d0bde5f92f099219683f9dab06951707c07`, subject
  `fix(formal): preserve frozen plan runtime context`, exact measure/test paths,
  and blobs `90000ff11a6603fc63515061d391200a46765380` /
  `272eacf4c302af5d64483620978411998497b242`.
- Retained R3 remains `RETAINED_UNVALIDATED_UNCONSUMED`; the historical formal
  ledger remains `ENGINEERING_INVALIDATED_PRECAPTURE_FORMAL_ABORT` with no new
  scientific, quality, eligibility, release, or readiness credit.

## 3. Section 1 — accepted-engineering checkpoint binding

### Independent behavior boundary

Section 1 adds one closed prerequisite-attestation seam to the existing owner.
It does not change `TASK_ID`, `FUTURE_TASK_ID`, package contract, current FULL
projection, package status, root behavior, or future child subject/topology.

The allowed implementation is limited to:

1. Exact accepted-engineering subject/path constants in the existing module.
2. Closed accepted-engineering checkpoint/tree/direct-parent/subject/path/blob
   fields in the existing source-attestation binding.
3. A matching descriptor contract projection.
4. Read-only Git validation of commit/tree/direct parent/subject/exact changed
   paths/blob OIDs and ancestry to the verified alignment parent.
5. Synthetic real-Git positive and negative coverage in the existing test file.

### Inputs and changed paths

- Input branch/base: this PLAN-FULL branch at its exact activation child.
- Frozen accepted checkpoint identity: the identity in section 2 above.
- Only implementation paths:
  - `src/camera_based_rgbww_optimizer/optimization/p7_td_b_r6_stage_gate.py`
  - `tests/test_p7_td_b_r6_stage_gate.py`
- Handoff/debug paths are separately owned by the active PLAN.

### Required tests and stop

- Exact new accepted-engineering binding/descriptor/Git-validator tests.
- Existing attestation matrix and committed-source topology negative tests.
- Existing descriptor reference-precedence and reference-consistent
  secret/historical tests.
- Full `tests.test_p7_td_b_r6_stage_gate` focused suite.
- Compile, CodeGraph sync/query, exact scope/numstat, and `git diff --check`.
- No repository full discovery in Section 1.
- Executer stop: `RETURN_FOR_G4_06_LARGE_CHANGE_SECTION_1_CANDIDATE_REVIEW`.

### Sizing failure review

The first independently derived Section 1 candidate reached 228 changed lines
before validation and therefore breached its live PLAN's 220-line hard cap. It
is rejected, incomplete and semantically unassessed; later mechanical
compaction to 220 does not revoke the breach.

The Section 1 behavior boundary is retained. Binding shape, descriptor
projection, read-only Git validation and the synthetic protective fixture form
one closed high-risk provenance contract and are not useful or safe as separate
production commits. The planning defect was the 220-line estimate, not evidence
of a production semantic defect. A fresh Section 1 implementation may be
released only after the rejected source/test draft is recoverably removed. Its
expected range is 200–260 changed lines with a 300-line hard stop. It must be
independently derived from the accepted branch and may not apply or copy the
rejected draft.

Orchestrator has now preserved the rejected source/test snapshot as historical
stash commit `b62eddd7563af43a20fd66a4960bae386f9ed54e`, whose first parent is the
accepted activation `e202db90f0ffc38bbdf74a1a6ee01baa72f70e2e` and whose
first-parent diff contains exactly the two owner paths with numstat
`105+/1-` and `114+`. The accepted source/test worktree is clean. The stash is
non-authorizing and the fresh Section 1 Executer is forbidden to read, apply,
pop, drop, branch from, copy or otherwise consume it. Section 1 is therefore
ready for a fresh independent activation; Section 2 remains locked.

The fresh V2 candidate later completed at 295 changed lines with targeted
`15/15` and one pre-late-change focused `50/50` pass. Independent Planner review
accepts its single-owner boundary, closed shape, Git identity validation,
descriptor-reference precedence and zero-effect ordering as correction input.
Final qualification is nevertheless rejected: after the focused run, production
added the stable OSError mapping around the ancestry subprocess, but the current
test source preserves only the returncode-2 assertion. The reported one-off
`1/1` probe is not a durable regression for this high-risk provenance error
boundary. Section 1 remains unaccepted and uncommitted until the same section
adds a persistent OSError assertion and requalifies the affected focused suite;
Section 2 remains locked.

Orchestrator accepts that review finding and releases only a bounded correction
inside the same task and Section 1 label. The production source and all
production semantics are frozen at SHA-256
`2dd469827fff3d6137e247b179035a685b42627aea207b18898a05d36fe18c11`
and blob `76c8821c915c58e7ad5cdb0133bf2940b51fd1f4`; source writes are zero.
The existing test owner may add exactly one durable case in which
`subject.subprocess.run` raises `OSError` for the ancestry query and the owner
returns `committed_source_engineering_ancestry_query_failed`. Existing
returncode-2 and nonancestor behavior must remain covered. Because this task is
already inside the mandatory large-change workflow, 300 is not a repository-
global limit: the final expected total is 300–320 changed lines and the hard
stop is 330. The final candidate requires affected exact tests, exactly one
fresh stage-gate focused invocation, two-file compile, CodeGraph, scope and diff
checks; repository full discovery remains zero. No other production or test
correction is authorized, and Section 2 stays locked.

### Commit and review loop

After Planner accepts the uncommitted candidate, Orchestrator creates the focused
commit `fix(stage-gate): bind accepted engineering checkpoint`. A clean
GPT-5.6 Sol xhigh `$code-review` pass is then run twice by independent review
agents. Both consecutive passes must report no findings. Any accepted finding is
repaired by a GPT-5.6 Sol high repair agent, validated and committed separately;
the clean-review streak resets to zero. Planner does not unlock Section 2 until
the section commit plus any repair commits have two consecutive clean reviews
and the worktree is clean.

## 4. Section 2 — replacement task, FULL projection and child topology

### Unlock inputs

Section 2 is locked until FULL and the next live PLAN record:

- exact accepted Section 1 implementation/repair tip commit and tree;
- focused validation ledger;
- two independent consecutive clean-review identities;
- clean worktree and Section 1 archive pointers.

### Independent behavior boundary

Starting only from the accepted Section 1 tip, Section 2:

1. Changes package task identity to `REF-G4-06-REPLACEMENT-PACKAGE`.
2. Keeps future formal identity distinct as `REF-G4-06-REPLACEMENT-R6` without
   granting formal/device/release authority.
3. Replaces archived completed-prerequisite expectations with the current
   unfinished-only FULL projection: accepted engineering checkpoint/tree,
   replacement-package task state, retained status and all authority false.
4. Binds the future focused owner-alignment commit as a direct non-merge child of
   the accepted Section 1 tip with exact subject, two paths and blob identities;
   later descendants remain linear `.agent-work/`-only commits.
5. Updates the existing synthetic Git fixtures and real behavior assertions.

It must not alter the Section 1 accepted-engineering validation, persistence,
CLI, artifact inventory, replay, terminal seal, failure seal, package-root
behavior, or formal/runtime owners.

### Required tests and stop

- Current positive package task/FULL projection/topology path.
- Old task, archived prerequisite projection, wrong authority, wrong
  subject/path/blob/tree/lineage and merge negatives before root effects.
- Descriptor reference drift and reference-consistent secret/historical guards.
- Stage-gate, terminal and thermal focused suites.
- Compile, CodeGraph sync/query, exact scope and `git diff --check`.
- Exactly one full unittest discovery invocation for the entire PLAN-FULL.
  Acceptance requires full green, or only the already independently attributed
  baseline governance-lineage group with identical test identities and no new
  failure/error; that qualified case must not be called full green.
- Executer stop: `RETURN_FOR_G4_06_LARGE_CHANGE_SECTION_2_CANDIDATE_REVIEW`.

### Commit and review loop

After Planner accepts the candidate, Orchestrator creates the focused commit
`fix(stage-gate): align replacement package owner`, then applies the same two
consecutive clean GPT-5.6 Sol xhigh `$code-review` rule. Accepted findings use a
GPT-5.6 Sol high repair agent and a separate focused commit, resetting the clean
streak. A clean worktree is mandatory before section closure.

## 5. Final PLAN-FULL exit

Section 2 closure means only that the repo-owned offline package owner alignment
is accepted. It does not create or validate a package, select/check/create a
root, call public `prepare`/`describe`, grant eligibility, consume release, or
authorize formal/device work.

Planner returns to Orchestrator at
`RETURN_FOR_ORCHESTRATOR_REPLACEMENT_PACKAGE_PLAN_SELECTION`. Orchestrator then
archives the terminal PLAN-FULL/FULL snapshots as applicable and independently
decides whether to request a new single package-preparation PLAN under the same
canonical route.

## 6. Global hard locks

Across both sections, counts for package-root selection/check/create, public
prepare/describe, old package/formal-root access, device, network, camera, Ray,
strip, capture, cleanup, formal execution, release consumption, analysis, G4-07
and TD-C remain zero. GUIDE/RESEARCH, FULL ownership, scientific contracts,
wrappers, config, measure/thermal/terminal production owners and all external
experiment payloads remain unchanged and inaccessible.
