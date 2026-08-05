# REF-G4-06-REPLACEMENT-PACKAGE large-change implementation plan

**Document status:** `NON_EXECUTABLE_LARGE_CHANGE_SECTION_ROADMAP`

**Executable authority:** `false`

**Stable reference task:** `REF-G4-06-REPLACEMENT-PACKAGE`

**Branch:** `codex/g4-r6-owner-alignment-large-change`

**Base checkpoint:** `3c920c6d29e5c366ce3843a2532d30d80c6f0c33`

**Base tree:** `e7d20cd3ac98f21d3af5cb9d43d31ed40e00ec6d`

`PLAN_FULL_MACHINE_CONTRACT={"schema":"g4_large_change_plan_full_v1","document_status":"NON_EXECUTABLE_LARGE_CHANGE_SECTION_ROADMAP","executable":false,"reference_goal":"REF-G4-COMPLETE","stable_reference_task":"REF-G4-06-REPLACEMENT-PACKAGE","corrective_suffix_allowed":false,"branch":"codex/g4-r6-owner-alignment-large-change","base_checkpoint":"3c920c6d29e5c366ce3843a2532d30d80c6f0c33","base_tree":"e7d20cd3ac98f21d3af5cb9d43d31ed40e00ec6d","rejected_draft":{"branch":"codex/g4-r6-owner-alignment-rejected-305","commit":"1f28b4c04a0ca20888dd5a996af53fc2f3dd0faf","disposition":"REJECTED_INCOMPLETE_UNVALIDATED_READ_ONLY_DESIGN_INPUT","cherry_pick_allowed":false,"copy_as_production_truth_allowed":false},"section_count":2,"current_section":"SECTION_1_ACCEPTED_ENGINEERING_CHECKPOINT_BINDING","sections":[{"section":"SECTION_1_ACCEPTED_ENGINEERING_CHECKPOINT_BINDING","status":"DRAFT_WAITING_ORCHESTRATOR_ACTIVATION","production_owner":"src/camera_based_rgbww_optimizer/optimization/p7_td_b_r6_stage_gate.py","test_owner":"tests/test_p7_td_b_r6_stage_gate.py","commit_subject":"fix(stage-gate): bind accepted engineering checkpoint","switch_package_task":false,"change_full_projection":false,"package_root_access":0},{"section":"SECTION_2_REPLACEMENT_TASK_PROJECTION_AND_CHILD_TOPOLOGY","status":"LOCKED_PENDING_SECTION_1_COMMIT_AND_TWO_CLEAN_REVIEWS","production_owner":"src/camera_based_rgbww_optimizer/optimization/p7_td_b_r6_stage_gate.py","test_owner":"tests/test_p7_td_b_r6_stage_gate.py","commit_subject":"fix(stage-gate): align replacement package owner","switch_package_task":true,"change_full_projection":true,"package_root_access":0}],"implementation_agent":{"model":"gpt-5.6-sol","reasoning_effort":"medium","role":"Executer"},"post_commit_review":{"skill":"code-review","model":"gpt-5.6-sol","reasoning_effort":"xhigh","consecutive_clean_reviews_required":2,"independent_review_agents_required":true,"finding_repair_model":"gpt-5.6-sol","finding_repair_reasoning_effort":"high","repair_commit_required":true,"clean_streak_resets_after_repair":true},"single_full_suite_owner_section":"SECTION_2_REPLACEMENT_TASK_PROJECTION_AND_CHILD_TOPOLOGY","full_suite_invocation_cap":1,"package_prepare_authorized":false,"package_describe_authorized":false,"package_root_selection_authorized":false,"package_root_check_authorized":false,"package_root_create_authorized":false,"old_package_access_authorized":false,"old_formal_root_access_authorized":false,"formal_execution_authorized":false,"formal_root_creation_authorized":false,"device_authorized":false,"network_authorized":false,"camera_authorized":false,"ray_authorized":false,"strip_authorized":false,"capture_authorized":false,"cleanup_authorized":false,"release_consumption_authorized":false,"analysis_authorized":false,"g4_07_authorized":false,"td_c_authorized":false}`

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
