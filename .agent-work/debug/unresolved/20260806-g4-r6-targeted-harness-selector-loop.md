# G4 R6 targeted harness selector loop

**Status:** `TERMINAL_HARNESS_INVALID_NO_CANDIDATE_GATE_ORCHESTRATOR_REASSESSMENT_REQUIRED`

**Reference:** `REF-G4-06-MATERIALIZED-RUNTIME-CONSUMER-MIGRATION`

**Activation:** `eca2d426d58e501fddcef03d7c89e8dc796ad3c1`

## Confirmed facts

- Candidate 2 was independently reconstructed from accepted blobs, but was never qualified because the targeted command did not enter a candidate test body.
- First command used nonexistent class `tests.test_p7_td_b_r6_terminal.P7TdBR6TerminalTests`: `Ran 2`, `errors=1`, exit `1`; log SHA-256 `649217ee4cc29cb8886d019f1961636e047a79fa8e165f81f1b310d70fa65c3e`.
- The single permitted correction used class `TerminalOwnerTests` but nonexistent method `test_materialized_plan_recognized`: `Ran 2`, `errors=1`, exit `1`; log SHA-256 `eb70923f85acdb15d9d96ff91ab6bd18f63751c186cbc1d7d478ec975b82333d`.
- Both invocations were harness-invalid, produced no candidate test body, no production gate result, no package/formal/device/scientific effect, and no candidate-owned failure count.
- Planner disposition is `ACCEPTED_CONTROLLED_INVALID_HARNESS_METHOD_SELECTOR_NO_CANDIDATE_GATE`; no third selector or rerun is allowed for candidate 2.

## Root-cause classification

The orchestration validation command was assembled from guessed test identities instead of a read-only exact identity inventory. This is an Orchestrator/Planner harness contract defect. It is not evidence against the Strategy B production owner, and it must not be converted into a green result or a production same-boundary failure.

## Required reassessment

Before any new executable route, Orchestrator must perform one read-only test-identity inventory from the accepted tree, define a command using only verified module/class/method identities, and decide whether a fresh candidate is justified. Candidate 2 remains historical-only and cannot be repaired, rerun, or used as implementation input. No package, formal, release, device, network, camera, Ray, strip, capture or scientific permission is unlocked by this record.
