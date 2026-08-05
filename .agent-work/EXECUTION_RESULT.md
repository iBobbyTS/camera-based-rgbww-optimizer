# EXECUTION_RESULT

## Pending Section 1 durable OSError regression execution

`PENDING_ORCHESTRATOR_ACTIVATION_AND_EXECUTER_HANDOFF`

- Contract: `G4-R6-LARGE-CHANGE-SECTION-1-DURABLE-OSERROR-REGRESSION-V1`
- Stable task/section: `REF-G4-06-REPLACEMENT-PACKAGE` /
  `SECTION_1_ACCEPTED_ENGINEERING_CHECKPOINT_BINDING`
- Source: frozen, no writes; 99811 bytes, SHA-256
  `2dd469827fff3d6137e247b179035a685b42627aea207b18898a05d36fe18c11`,
  blob `76c8821c915c58e7ad5cdb0133bf2940b51fd1f4`, numstat `96+/1-`
- Test input: 144723 bytes, SHA-256
  `2a412e2b405c7ddf59146fb522da3afaf84e66b106e50b3989552371dad30d17`,
  blob `efe7a16ff415b6e1397c8d11865423314662a82c`, numstat `198+`
- Candidate: unaccepted, uncommitted, total changed lines `295`
- Only authorized change: one durable existing-owner regression for raised
  ancestry `OSError` mapping to
  `committed_source_engineering_ancestry_query_failed`
- Required retained behavior: returncode 2 and nonancestor
- Expected final changed lines: `300–320`; hard cap `330`; 300 is not a
  repository-global limit
- Final validation: affected exact tests, one stage-gate focused invocation,
  two-file compile, CodeGraph, scope/numstat/diff/machine checks
- Full discovery invocation cap: `0`
- Section 2: locked
- Commit: none authorized before Planner acceptance
- Package/root/device/network/camera/Ray/strip/formal/release effects: `0`

Executer must append the final commands, counts, identities, zero-effect ledger
and decision request here, then stop at
`RETURN_FOR_G4_06_LARGE_CHANGE_SECTION_1_DURABLE_REGRESSION_REVIEW`.
