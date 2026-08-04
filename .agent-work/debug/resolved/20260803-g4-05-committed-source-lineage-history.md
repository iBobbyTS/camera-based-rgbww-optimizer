# G4-05 committed-source lineage history bypass (resolved)

## Verified resolution

- Accepted code owner commit: `d813cba24f49ca8ae8b54004f7ec20592ee979ab`
  / tree `e5a940cb068ab1aec0d462edf8ea9f3b907eb1fe`.
- The validator now walks every linear direct-child commit from L back to C,
  rejects merge/nonlinear history, validates each adjacent changed-path set, and
  binds the ordered ledger into activation/runtime authority.
- The exact add-then-delete restored-tree repro, restored-tree merge, mixed-path
  commit, and positive ordered-ledger probes pass their expected outcomes.
- Validation: targeted `25/25`, real-owner `9/9`, focused `215/215`, fresh full
  suite `942/942`, compile/static/CodeGraph/diff checks all passed.
- Planner phase2 accepted
  `ACCEPTED_G4_05_PER_COMMIT_SOURCE_ATTESTED_LAUNCH_GATE_G4_06_PLANNING_UNLOCKED_EXECUTION_FALSE`.
- G4-06 is planning-unlocked only. Device/formal/release execution remains
  separately locked.

## Confirmed state

- Current task remains `REF-G4-05-RAY-R6-STAGE-GATE`; no corrective suffix or new task ID is allowed.
- Planner phase-1 disposition is `REJECTED_G4_05_POST_CHILD_HISTORY_NET_DIFF_BYPASS`.
- The accepted subordinate design separates activation parent A, committed code owner C, and live orchestration descendant L.
- `validate_committed_source_attestation()` currently obtains C..L paths from
  `thermal.changed_paths_between_checkpoints()`, which runs endpoint
  `git diff --name-only C..L`.
- A synthetic C -> L1 -> L2 history where L1 adds `src/transient-post-child.py`
  and L2 deletes it restores the C tree. The endpoint path set is empty and the
  validator incorrectly passes.
- The earlier `21/22 -> 22/22` change was only a negative-test error-code
  assertion correction. It did not change production code and is unrelated to
  this defect.
- The rejected candidate remains uncommitted and classified in place. G4-06,
  device, formal, release consumption, and all experiment operations remain
  unauthorized.

## Failure-boundary classification

The three G4-05 candidate failures are distinct owner/state seams:

1. real delegated runner argument shape;
2. non-self-referential A/C source checkpoint reachability;
3. per-descendant commit-history enforcement.

The current symptom is the first demonstrated failure of the per-commit history
seam. The completed PLAN is terminal and cannot authorize an in-place retry;
Orchestrator may release one new bounded same-task package after owner
reassessment, without suffix, alternate root, or new task.

## Root-cause hypothesis

Root cause is endpoint-tree comparison being used to attest a property of every
commit in a history. The single source of truth must walk the exact ancestry from
L back to C, reject merge/non-linear topology, and validate each adjacent
parent-child changed-path set before aggregating the attestation result.

## Required regression surface

- PASS: `L == C`.
- PASS: one or multiple linear `.agent-work/`-only descendants.
- FAIL: add then delete a `src/`, `tests/`, config, GUIDE/RESEARCH, wrapper, or
  `.agent-work-evil/` path, even when C and L trees are identical.
- FAIL: merge commit, skipped/non-ancestor checkpoint, wrong HEAD/tree, or any
  adjacent descendant with a non-orchestration path.
- Preserve all previously accepted A/C identities, candidate blob/worktree
  checks, runtime delegation, package authority=false, and offline safety locks.

## Completed diagnostic

The maximum safe continuous package completed exactly once around the existing
focused owner. Rejected roots remained historical access 0; one fresh immutable
root was created only after pre-package checks passed, then persisted and replayed
once. The two-phase controlled-child review accepted the committed owner.
