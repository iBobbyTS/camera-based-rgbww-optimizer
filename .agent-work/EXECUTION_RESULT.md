# EXECUTION_RESULT

## REF-G4-06 materialized attestation owner-seam refactor and qualification

**Contract:** `G4-R6-MATERIALIZED-COMMIT-ATTESTATION-OWNER-SEAM-REFACTOR-QUALIFICATION-V1`

**Status:** `REJECTED_RELATED_CHANGED_OWNER_ERRORS_THIRD_SAME_BOUNDARY_TERMINAL_CANDIDATE`

**Planner stop:** `RETURN_FOR_G4_06_MATERIALIZED_ATTESTATION_OWNER_SEAM_REFACTOR_REVIEW`

## Frozen intake and implementation

- Intake source/test SHA-256 matched exactly: `f7feed95f03a79b21842c265869005fe76a533322fb85375dff74a397b8c768d` / `c3556c99c1278e2fceddb3146ef5ec30c3d00bd920776b9cda5a271ea0a150fc`; intake changed-lines `438`.
- CodeGraph preflight confirmed the preparation path `build_stage_gate_input -> _validate_preparation_source_attestation` lacked the Git-fact owner used by `materialize_committed_source_attestation -> validate_committed_source_attestation`.
- Implemented one internal `_validate_accepted_engineering_prerequisite` owner, reused by preparation, materializer-before-candidate-query, and post-commit validator. It validates exact tree, direct parent, subject, changed paths, blob OIDs, and ancestry to the verified parent.
- Normalized `OSError`, `subprocess.CalledProcessError`, and `ValueError` from accepted-engineering, code-owner, and post-child changed-path queries to their exact existing StageGateError codes.
- Converged the authorized stage-gate tests: v2 attestation fixture fields/top-level alias removal; direct materializer ownership for invalid topology and old descriptors; identity tamper only after valid materialization; exact `committed_source_parent_drift` priority; protective nine-way changed-path exception matrix.
- No module, runner, static future subject/blob authority, alternate identity owner, task suffix, package/formal root, external/device/network/camera/Ray/strip/release effect, commit, push, or PR was created.
- Final source mode/bytes/SHA-256: `-rw-r--r--`, `106305`, `c4d04e0c4045520ffd9d262190cc9d9edd3b445c32afe2434f741cc3df7dd316`.
- Final test mode/bytes/SHA-256: `-rw-r--r--`, `153734`, `639999ab7615a8250eec1d3b6974e3516493941786009292f68257cb96dedb45`.
- Final source/test diff numstat: `251+151` and `100+96`; total changed-lines `598`; additional over intake `160`; caps `160/600` both pass. Path set remained the two authorized candidate paths plus this ER.

## Continuous validation evidence

Scratch root: `/Volumes/4T/temp/rgbww-optimizer/g4-r6-materialized-attestation-owner-seam-qualification-UmAwb4` (fresh; retained with exactly three log files).

Environment for all tests: cwd `/Users/ibobby/Projects/WLED-RGBWW`; `PYTHONHASHSEED=0`; `.venv/bin/python`; no device/network/camera/Ray/strip callbacks or package/formal roots.

### Targeted invocation 1/1 - PASS

- Argv: `.venv/bin/python -m unittest -v` followed by the 14 exact `tests.test_p7_td_b_r6_stage_gate.P7TdBR6StageGateTests` identities covering accepted-engineering binding/shape/Git/ancestry, all three changed-path exception seams, non-static subject, old binding/three-path/descriptor, production error priority, v2 runtime fixture, and both topology/tamper matrices.
- UTC: `2026-08-06T02:47:11Z` to `2026-08-06T02:47:59Z`; natural exit `0`; unittest `14`, `OK`, duration `47.849s`; wall `48.18s`.
- Log: `targeted.log`; bytes `3082`; SHA-256 `dec976ca8ebee577ddad07ee3784a766a2e2a987e051fc08bf84078297ff331d`.

### Stage-gate focused invocation 1/1 - PASS

- Argv: `.venv/bin/python -m unittest -v tests.test_p7_td_b_r6_stage_gate`.
- UTC: `2026-08-06T02:48:08Z` to `2026-08-06T02:52:25Z`; natural exit `0`; unittest `54`, `OK`, duration `256.077s`; wall `256.29s`.
- Log: `stage-gate-focused.log`; bytes `11090`; SHA-256 `766e0eb315177b9ddc4ae6d221001afa7c036e09d49f0048b312ef61a855e672`.

### Related invocation 1/1 - REJECTED, VALID NON-GREEN

- Argv: `.venv/bin/python -m unittest -v tests.test_p7_thermal_diagnostics tests.test_p7_td_b_r6_terminal`.
- UTC: `2026-08-06T02:52:55Z` to `2026-08-06T02:53:25Z`; natural exit `1`; unittest `95`, failures `2`, errors `21`, duration `30.008s`; wall `30.30s`.
- Allowed related baseline was exact governance-lineage `2F+8E`. Observed the same `2F+8E` governance group plus `13` additional changed-owner errors, so acceptance is prohibited.
- Additional thermal/materialized identities (`2E`):
  - `G4R6FrozenPlanRuntimeContextTests.test_unknown_runtime_template_drift_preserves_stable_outer_code_before_effects`
  - `P7ThermalDiagnosticsTests.test_r6_execute_calls_post_capture_validator_once_before_complete`
  - First frame for both: untouched related fixtures call `validate_materialized_runtime_plan`; stage-gate raises `StageGateError: runtime_authority_drift` at `p7_td_b_r6_stage_gate.py:1044`.
- Additional terminal/materialized identities (`11E`):
  - `TerminalOwnerTests.test_returned_summary_write_failure_is_attempted_once_and_nonzero`
  - nine subtests of `TerminalOwnerTests.test_terminal_finalize_hard_failures_never_write_pass`: `python_cleanup`, `shell_cleanup`, `missing_artifact`, `symlink_artifact`, `identity_drift`, `extra_artifact`, `extra_empty_directory`, `special_node`, `timing_payload_drift`
  - `TerminalOwnerTests.test_terminal_finalize_writes_unique_pass_seal_and_replays_ledger_once`
  - First frame: `test_p7_td_b_r6_terminal.py:69` fixture `materialized_plan` calls `validate_materialized_runtime_plan`; stage-gate raises `StageGateError: runtime_authority_drift` at line `1044`.
- Baseline governance failures/errors remained rooted in `TD-B governance successor path identity differs: AGENTS.md`; they do not absorb or authorize the 13 stage-gate/materialized errors.
- Log: `related.log`; bytes `55117`; SHA-256 `827ce63c1f0f62abf5fe7481e22627f2e9585572098ab9e82121b54be16a9580`.

## Fail-closed disposition

- This was the first valid non-green gate. Per PLAN, source/test were not modified after targeted began, and related was not rerun.
- Correction budget `1/1` consumed. The related integration evidence demonstrates the accepted-engineering/materialized authority shape is not converged across existing related owners. With the frozen same-boundary substantive failure count `2`, this is the third same-boundary terminal candidate and must be treated as terminal fail closed by Planner/Orchestrator review.
- Static/compile/parser/diff-check/forbidden scan, CodeGraph sync/post-sync query, identity-freeze validation stage, and full discovery were not invoked after the valid related failure. Full invocation/retry is `0/0`, not `1/0`; no result is inferred.
- Test invocation counts: targeted `1/1`; stage-gate focused `1/1`; related `1/1`; full `0/1`; retries `0` throughout.
- All launched test processes exited naturally. Final active unittest/qualification process count `0`; automation created/active `0/0`; visible Terminal was not required because no launched command was expected to exceed ten minutes.
- Scratch cleanup: test-owned temporary roots exited through their normal context cleanup; evidence root intentionally retained with only `targeted.log`, `stage-gate-focused.log`, and `related.log`. No repo temp data or external root was created.

`RETURN_FOR_G4_06_MATERIALIZED_ATTESTATION_OWNER_SEAM_REFACTOR_REVIEW`
