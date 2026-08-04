# G4-05 committed-source lineage history bypass

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

## Next diagnostic

Planner must freeze one maximum safe continuous package around the existing
focused owner. Executer may make only the minimal per-commit traversal change
and extend the same focused tests. Because candidate bytes change, every rejected
package remains historical access 0; after all pre-package gates pass, the package
must create one new immutable root and may not retry, repair, or choose an
alternate root. The final candidate must receive targeted/focused/static/
CodeGraph/diff checks and one fresh full suite before the existing two-phase
controlled-child review.
