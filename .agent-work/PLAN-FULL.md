# REF-G4-06-REPLACEMENT-PACKAGE large-change implementation plan

**Document status:** `NON_EXECUTABLE_LARGE_CHANGE_SECTION_ROADMAP`

**Executable authority:** `false`

**Stable reference task:** `REF-G4-06-REPLACEMENT-PACKAGE`

**Branch:** `codex/g4-r6-owner-alignment-large-change`

**Base checkpoint:** `3c920c6d29e5c366ce3843a2532d30d80c6f0c33`

**Base tree:** `e7d20cd3ac98f21d3af5cb9d43d31ed40e00ec6d`

`PLAN_FULL_MACHINE_CONTRACT={"schema":"g4_large_change_plan_full_v6","document_status":"NON_EXECUTABLE_LARGE_CHANGE_SECTION_ROADMAP","executable":false,"reference_goal":"REF-G4-COMPLETE","stable_reference_task":"REF-G4-06-REPLACEMENT-PACKAGE","corrective_suffix_allowed":false,"branch":"codex/g4-r6-owner-alignment-large-change","base_checkpoint":"3c920c6d29e5c366ce3843a2532d30d80c6f0c33","base_tree":"e7d20cd3ac98f21d3af5cb9d43d31ed40e00ec6d","current_section":"SECTION_2_REPLACEMENT_TASK_PROJECTION_AND_CHILD_TOPOLOGY","section_1_accepted":{"commit":"5d01bcbb7e1a9ec1808e2fc05d238363d82a0a74","tree":"656fee670f289b0a20fea1a8c015762afd44a5c0","clean_review_streak":2},"sections":[{"section":"SECTION_1_ACCEPTED_ENGINEERING_CHECKPOINT_BINDING","status":"ACCEPTED_COMMITTED_TWO_CLEAN_REVIEWS"},{"section":"SECTION_2_REPLACEMENT_TASK_PROJECTION_AND_CHILD_TOPOLOGY","status":"ACTIVE_FINAL_SNAPSHOT_TOPOLOGY_REPAIR"}],"section_2_topology_repair":{"base_code_commit":"75d327729fdc479b6f9305e4e4a5ca3628fe2346","base_code_tree":"342e8c0b4f4444447a635132b0dfe333ef1ca483","clean_review_streak":0,"closed_findings":["REV-S2-AUTH-001","REV-S2-PROV-001"],"active_findings":["REV-S2-REPAIR-R2-001"],"final_code_snapshot_subject":"fix(stage-gate): bind final package to immutable code snapshot","history_rewrite":false,"multi_subject_fallback":false},"post_commit_review":{"skill":"code-review","model":"gpt-5.6-sol","reasoning_effort":"xhigh","consecutive_clean_reviews_required":2,"clean_streak_resets_after_repair":true,"real_git_production_validator_probe_required":true},"final_snapshot_full_collection_invocation_cap":1,"final_snapshot_full_retry_cap":0,"package_prepare_authorized":false,"package_describe_authorized":false,"package_root_selection_authorized":false,"package_root_check_authorized":false,"package_root_create_authorized":false,"old_package_access_authorized":false,"old_formal_root_access_authorized":false,"formal_execution_authorized":false,"formal_root_creation_authorized":false,"device_authorized":false,"network_authorized":false,"camera_authorized":false,"ray_authorized":false,"strip_authorized":false,"capture_authorized":false,"cleanup_authorized":false,"release_consumption_authorized":false,"analysis_authorized":false,"g4_07_authorized":false,"td_c_authorized":false}`

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
