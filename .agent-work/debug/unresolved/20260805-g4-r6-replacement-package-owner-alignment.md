# G4 R6 replacement-package owner alignment

## Status

- State: `unresolved`
- Reference task: `REF-G4-06-REPLACEMENT-PACKAGE`
- Scope: existing stage-gate owner plus its existing test file; offline fake/synthetic evidence only
- Root/package/device/formal authority: none

## Confirmed observations

1. Baseline HEAD `a7fd401fe5761d00233d7cef2f65c7532a8e8067`, tree `0b4be2e4a27f392fa5efacc6c08c4996ccb24c10`, is clean.
2. Accepted runtime-context prerequisite is commit `1fbe38d17ec9885dcd5b563edd90359761c51910`, tree `9535ac6bcd445898c48ff2227f659d2ea6955e60`, direct parent `08e27d0bde5f92f099219683f9dab06951707c07`, subject `fix(formal): preserve frozen plan runtime context`, exact paths `measure_p7_thermal_diagnostics.py` and `test_p7_thermal_diagnostics.py`.
3. Existing `p7_td_b_r6_stage_gate` is the sole package owner and already owns exclusive root creation, canonical persistence, exact inventory, internal replay, terminal seal, public replay and fail-closed validation.
4. Its current package task/projection remains bound to `REF-G4-06-RAY-R6`, old prerequisite fields and a stage-gate-only code-child attestation; it cannot consume the current unfinished-only FULL or accepted runtime-context checkpoint.
5. Existing negative tests already cover projection drift before root creation, source-attestation topology/path/blob drift, descriptor reference integrity precedence, specialized secret/historical guards, fresh-root rejection, artifact inventory, replay and terminal seal.
6. Owner file is 2213 lines and test file is 2660 lines. The seam is local but high-risk provenance state; direct change is acceptable only if it reuses these owners, stays under 300 combined changed lines and adds closed positive/negative regression coverage.
7. Activation `c02b4e2b92cdb98407883b38131c7bd8a8941e39` passed exact parent/tree/subject/seven-path, clean-worktree, PLAN/FULL `1/1`, archive/debug, baseline source/test, and accepted engineering checkpoint identity checks.
8. During the single candidate, observed source/test numstat reached `131+68+70+36=305`, exceeding the PLAN hard cap. This is a terminal package failure even though an already-issued mechanical compaction left the live diff at exactly `126+68+70+36=300` when execution stopped.
9. No targeted, focused, compile, CodeGraph sync, diff acceptance, or full discovery validation was run after the cap breach. The live candidate is incomplete and unvalidated; it must not be accepted, committed, or used to authorize package preparation.
10. Package-root selection/check/create, public prepare/describe, old package/root access, and device/network/camera/Ray/strip/capture/formal/release calls remained `0`.

## Root-cause hypothesis

The production persistence owner is sound; only its closed orchestration projection and committed-source attestation model predate the stable replacement-package reference and the accepted runtime-context checkpoint. Aligning those two contracts, while preserving a distinct future formal task identity, should unblock a later package plan without changing package persistence or formal semantics.

## Minimal candidate

- Keep the existing module, schema names, CLI, persistence functions, artifact names and validation order.
- Bind package preparation to `REF-G4-06-REPLACEMENT-PACKAGE` and keep future formal identity distinct as `REF-G4-06-REPLACEMENT-R6`.
- Accept the current unfinished-only FULL projection and exact accepted engineering prerequisite.
- Extend the existing attestation binding narrowly enough to prove both the accepted runtime-context checkpoint identity and the future focused stage-gate owner-alignment child; do not add a controller or bypass Git/source checks.
- Add synthetic real-Git tests for the current success topology and old/wrong task, projection, subject, tree, path and blob failures before root/package side effects.

## Stop conditions

- Estimated or actual combined production/test changed lines exceed 300.
- A new module, schema, runner, external controller, wide ignore/allowlist or strict-validator bypass is needed.
- Any test requires a real package root, old package/formal root, device, network, camera, Ray, strip, capture, release or formal execution.
- The single owner-alignment hypothesis fails twice; return to Orchestrator rather than creating a suffix or alternate design.

## Next action

Planner rejected the incomplete candidate as
`REJECTED_SOURCE_TEST_CHANGED_LINE_HARD_CAP_BREACHED_CANDIDATE_INCOMPLETE_UNVALIDATED`.
Executer must not compress further, validate, commit, or start a second semantic
scheme. Orchestrator owns recoverable preservation of the dirty source/test
draft on a rejected historical branch, restoration of the accepted main tree by
branch switching, and activation of the required repository large-change branch
plus PLAN-FULL section/subagent/commit/clean-review workflow under the same
stable reference task. The applicable top-level AGENTS instruction requires
that workflow for a non-trivial change that may reach 300 lines or more, and the
historical candidate reached 305.

Reviewed evidence is immutable at:

- `.agent-work/archived/PLAN-20260805-0226.md`, SHA-256
  `650cb336d3cb195d86321a2d56e94d97527048a614f6f983b5d8e608d5f3b317`;
- `.agent-work/archived/EXECUTION_RESULT-20260805-0226.md`, SHA-256
  `2a5aec2db4120cb6a3fd91d5cf9c6c0f72226884a582011d3b048cbb17a0ba24`.

The next stop is
`RETURN_FOR_ORCHESTRATOR_LARGE_CHANGE_BRANCH_AND_PLAN_FULL`. This remains an
engineering/orchestration issue, not a scientific/formal/Human/Advisor blocker.
