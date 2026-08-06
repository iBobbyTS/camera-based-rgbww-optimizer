# EXECUTION_RESULT

## REF-G4-06 targeted harness stop

**Status:** `ACCEPTED_CONTROLLED_INVALID_HARNESS_METHOD_SELECTOR_NO_CANDIDATE_GATE`

**Planner stop:** `RETURN_TO_ORCHESTRATOR_FOR_HARNESS_AND_ROUTE_REASSESSMENT`

- Candidate 2 never entered a candidate test body. First invalid class selector log SHA-256: `649217ee4cc29cb8886d019f1961636e047a79fa8e165f81f1b310d70fa65c3e`; second invalid method selector log SHA-256: `eb70923f85acdb15d9d96ff91ab6bd18f63751c186cbc1d7d478ec975b82333d`.
- Both commands exited naturally with `Ran 2`, `errors=1`, exit `1`; later gates `0/0`; no production, package, formal, release, device, network, camera, Ray, strip, capture or scientific effect.
- Candidate 2 source/test/support is not accepted and is forbidden as future implementation input. Accepted source/test tree was restored from `eca2d426d58e501fddcef03d7c89e8dc796ad3c1`.
- No third selector, retry, focused/full gate or new executable PLAN is authorized. Next action is read-only exact test-identity inventory by Orchestrator.

## Executer package baseline (2026-08-06)

- Active package: `REF-G4-06-MATERIALIZED-RUNTIME-CONSUMER-MIGRATION`; accepted-tree
  HEAD `e7c0fb49dcc06c45bb3097fcb65af8ed967781a2`, working tree pre-existing
  modifications limited to `.agent-work/PLAN.md` and `.agent-work/PLAN-FULL.md`.
- Exact identities and one allowed invocation are recorded in `.agent-work/PLAN.md`:
  `P7TdBR6StageGateTests.test_synthetic_materialization_passes_focused_and_existing_validators_without_connect`,
  `P7TdBR6StageGateTests.test_production_cli_seam_loads_materializes_and_delegates_exactly_once`,
  `G4R6FrozenPlanRuntimeContextTests.test_full_chain_keeps_materialized_plan_frozen_and_records_runtime_context`,
  `TerminalOwnerTests.test_capture_projection_passes_existing_validator_and_negative_matrix`.
- Frozen successor release read-only hashes: `release/frozen-inputs.json`
  `8a81a906d2a94903a365f54b33c224a8ec99ce8d519ae2317cdc213c6e0264f8`,
  `release/r6-formal-plan.json`
  `dea5f979950909d5b3e8fd93c3a76e4fd18c0242158eade7967c4c62ec72cc3b`,
  `release/release-descriptor.json`
  `6843ef5007b9ebe3bfef1f7c8c1864ed0b86b3000d3d72caa8f08f67ce3bb452`,
  `release/terminal-seal.json`
  `d9d7b784a4ec910d7c7740bc560ed87f2b99ab1744c19df42097d5683b668850`,
  `release/validation-summary.json`
  `07e831616c303e68f9bf863a722b8b640c3726556f47143db8299083f941cc07`.
- Frozen zero-readiness terminal seal hash:
  `c6fc7b2a14cfce2474e1a1369721ebbdf660aa60baccb4caf237873a1af2a39d`.
- Owner contract read-only check: stage-gate exposes materialization/validation;
  thermal owns runtime execution; terminal owns capture projection and final-zero
  seal. No targeted identity evidence currently proves contract drift, so source/test
  edits are not authorized before validation.

## Targeted validation result

- Command executed exactly once: the four fully-qualified unittest identities above.
- All four selectors entered real test bodies; result `Ran 4`, `OK`, exit code `0`,
  duration `7.781s`.
- Captured stdout/stderr summary SHA-256:
  `23818fd00cf0683ee5a6dc038079cf9a4ae325aa3f4da444ac97db8c09d67bf5`.
- Runtime materialization, production CLI seam delegation, frozen runtime context,
  terminal projection, and negative matrix all passed. No device/network/camera/Ray/
  strip/capture/analysis command was invoked.
- `git diff --check`: pass. No source or test files changed; only this execution
  record is in the package scope. Accepted package commit: `21754a3`.

## Planner terminal review (2026-08-06)

- **decision:** `ACCEPTED_ENGINEERING_ONLY_PACKAGE`
- The single targeted invocation entered all four verified test bodies: `Ran 4`, `OK`, exit 0.
- No source/test change occurred; the accepted package is commit `21754a31f8d9e97626e2478ea832b9ebb082b8be` (short `21754a3`). The engineering-only budget `1` is consumed.
- This result is engineering evidence only; formal/device/release/camera/Ray/strip/capture/analysis remain unauthorized.
- **next branch:** Ray R6 16-frame scientific acquisition PLAN.

