# Reviewed EXECUTION_RESULT archive: early-terminated stage-gate focused evidence

**Archive status:** `REVIEWED_CONTROLLER_EVIDENCE_INCOMPLETE_HISTORICAL_NON_EXECUTABLE`

**Timestamp (UTC):** `2026-08-06T02:14Z`

**Source owner/type:** `Executer / EXECUTION_RESULT`

**Reviewed scope:** `REF-G4-06-MATERIALIZED-COMMIT-ATTESTATION` / `G4-R6-MATERIALIZED-COMMIT-ATTESTATION-ZERO-WRITE-QUALIFICATION-V1`

**Source checkpoint:** `87272f242417b0c1fa07405707023e0d7626480d`

**Original EXECUTION_RESULT bytes:** `5899`

**Original EXECUTION_RESULT SHA-256:** `dc1c3e70a8fbeb4e09837373cfac0bb36086e41a2f1ff25ea543f201e1400754`

**Planner disposition:** `ACCEPTED_TARGETED_GREEN_REJECTED_FOCUSED_HANDOFF_AS_CONTROLLER_EARLY_TERMINATION_EVIDENCE_INCOMPLETE_NO_CANDIDATE_FAILURE`

**Exact next branch:** same frozen candidate, zero-write qualification continuation with natural-exit focused evidence.

**Archive authority:** `historical_non_executable`; no correction, retry, package, formal, release, device, commit, or stage authority.

## Frozen evidence

- Targeted `01-targeted.log`: 123 bytes, mode `0644`, SHA-256 `f7d767b7b33d8e95477855ebbd1ab328dc617bd780a4d87b8df39b0290346f2a`; content proves `Ran 4 tests in 8.410s` and `OK`.
- Focused `02-stage-gate-focused.log`: 23 bytes, mode `0644`, SHA-256 `8a2c1d1a2680ad47d97e22e8e10f9c24a4e379210bf603bb2e98e88f40c9b201`; content only `...FFE....EEEEEEE......`.
- Focused process was SIGTERM-terminated after 76 seconds; no natural exit, test identities, traceback, final count or unittest summary exists.
- Source/test identity and 438/480 diff stayed unchanged; writes `0/0`.
- Related/static/CodeGraph/full invocations were zero; full invocation/retry `0/0`.
- No process/automation or external effect remained.

The focused evidence is incomplete controller output, not a candidate failure result. Targeted green remains reusable because the unittest log is complete despite its wrapper's separate readonly-variable metadata failure.

`historical_non_executable`
