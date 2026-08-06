# Reviewed EXECUTION_RESULT archive: materialized commit attestation engineering v1

**Archive status:** `REVIEWED_REJECTED_HISTORICAL_NON_EXECUTABLE`

**Timestamp (UTC):** `2026-08-06T01:31Z`

**Source owner/type:** `Executer / EXECUTION_RESULT`

**Reviewed scope:** `REF-G4-06-MATERIALIZED-COMMIT-ATTESTATION` / `G4-R6-MATERIALIZED-COMMIT-ATTESTATION-ENGINEERING-V1`

**Source checkpoint:** `f39539ff6c948d9adfa90a5b4eeb6b1337d7763a`

**Original EXECUTION_RESULT bytes:** `7181`

**Original EXECUTION_RESULT SHA-256:** `f45a680a0d4d53c4341789bbb0b17966b42ae6644717ebe5eac0288e67fd3572`

**Terminal disposition:** `REJECTED_MATERIALIZED_COMMIT_ATTESTATION_V1_PRODUCTION_ACTIVATION_SEAM_NOT_PROPAGATED`

**Exact next branch:** same stable reference bounded second engineering package after Orchestrator preserves/rejects this candidate and restores accepted tree.

**Archive authority:** `historical_non_executable`; this archive does not authorize execution, correction, retry, commit, package, release, formal, device, or stage entry.

## Frozen candidate identity and scope

- Source: `src/camera_based_rgbww_optimizer/optimization/p7_td_b_r6_stage_gate.py`; mode `0644`; 101443 bytes; SHA-256 `a771bd03ba485e42a743f19baf54a1edbea64509a628af61df26843e60798ae8`; numstat `+150/-145`.
- Test: `tests/test_p7_td_b_r6_stage_gate.py`; mode `0644`; 154241 bytes; SHA-256 `0e42dec6fc08c039b99bc3b1d06c92962eeef1ac23af544494c947d81fbd7252`; numstat `+70/-50`.
- Total changed lines: `415/420`.
- Candidate commit: none. Candidate accepted: false.
- Historical Q1/Section2/v2 implementation input access: `0`.

## Validation evidence

Fresh root: `/Volumes/4T/temp/rgbww-optimizer/g4-r6-materialized-attestation-20260805T-targeted`.

| Evidence | Result | SHA-256 |
| --- | --- | --- |
| `targeted-1.log` | 1 test, exit 0 | `6b09a6a1e21e276da0f3e14161f1b778c1786eb375b5ec1e0221897d7602a60e` |
| `targeted-materialized.log` | initial fixture migration failure | `512e576eabe95c5ff84c2de2f753a266d911c3374535311c8c5d079759a92ad8` |
| `targeted-materialized-after-harness-correction.log` | 4 tests, exit 0 | `09a10600b89d77d1df12e88b69e8443440c46c3ac53dd547d6c55865744465ed` |
| `stage-gate-focused.log` | 53 tests, 236.784s, exit 1, 4F+10E | `171bc8351d5e4bceb83e9a8b8cf89e2f3a163d4272ea8bfcbb53e5c2614fa340` |

Harness correction was consumed `1/1` for stale fixture/materialized post-child ledger migration. Production correction count remained `0`.

The terminal production defect is that `_build_production_activation` supplies only checkpoint/tree probe fields to `validate_committed_source_attestation`; the new owner requires the materialized identity in `future_activation["committed_source_attestation"]`. Production and measure CLI tests therefore report `committed_source_materialized_shape_drift`, including exact-delegate and parser/binding precedence paths. Remaining focused failures include stale static-child harness expectations; the production defect alone mandates rejection.

Related focused, final compile/static, CodeGraph sync/query and full were not run after the focused stop. Full invocation/retry is exactly `0/0`. No result from the allowed governance-lineage full baseline is claimed.

## Effects and disposition

Package prepare/describe/replay/probe/root, formal, release, device, network, camera, Ray, strip, capture, light, analysis, G4-07 and TD-C effect counts are all `0`. No scientific result was created; retained R3 remains `RETAINED_UNVALIDATED_UNCONSUMED`. Test processes ended and scratch fixtures cleaned.

Planner rejects this uncommitted candidate. It may not be accepted, committed on the orchestration branch, used as package input, repaired in place, or rerun. Orchestrator must preserve it historical-only and restore the accepted source/test blobs before activating the next independent package.
