# EXECUTION_RESULT (archived terminal package)

## Historical-only candidate identity

- ref: `refs/heads/codex/historical-g4-runtime-consumer-boundary-environment-rejected`
- commit: `ca1a6fc0b7a36f101c99cc85559a235b741b462a`
- tree: `424f1ec3f1bec7a8e8391e07fa784c64c08bf813`
- `implementation_input_allowed=false`; `live_accepted_source_test_restored=true`
- `/Volumes/4T` appeared only after terminal preflight for historical evidence-index
  creation; the recorded `FileNotFoundError: [Errno 2]` remains valid and no tests
  were rerun.

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

## G4 PLAN runtime-alignment correction terminal stop (2026-08-06)

- Executed the first and only permitted class-level command exactly once:
  `.venv/bin/python -m unittest tests.test_agent_work_machine_contract.AgentWorkMachineContractTests tests.test_p7_td_b_r6_stage_gate.P7TdBR6StageGateTests`.
- Selectors resolved to real test bodies. Result: `Ran 69 tests in 83.091s`, exit
  `1`, `failures=1`, `errors=213`; this is an engineering failure, not a harness
  selector failure or scientific result.
- Dominant failure: `build_stage_gate_input()` still calls
  `parse_full_plan_machine_state` at `p7_td_b_r6_stage_gate.py:601` after the
  production import was migrated to `parse_plan_full_machine_contract`, causing
  `NameError` before the affected stage-gate test bodies can exercise their intended
  contract assertions. The parser public-surface test also reports the new wrapper
  absent from `__all__`.
- Per active PLAN: zero retry, no second implementation/correction, no second
  command (including the four-test command), no full suite, and no device/network/
  camera/Ray/strip/capture/formal/root/release action. Return to Orchestrator for a
  terminal semantic disposition and route reassessment.

## REF-G4-RUNTIME-CONSUMER-BOUNDARY execution baseline (2026-08-06)

- Current accepted-tree HEAD before this package: `463a151bede3013db14d31802ea93fafa2322bf6`.
- Pre-existing worktree changes: `.agent-work/PLAN.md` and `.agent-work/PLAN-FULL.md`
  only; both remain untouched and read-only to Executer.
- Authorized implementation paths: parser module, G4 stage-gate module, and their
  two test modules. No rejected candidate, historical reference, device, network,
  release, or formal runtime input was accessed.
- Exact planned invocation is the eight-selector command in `.agent-work/PLAN.md`;
  it will be run once with zero retry after this baseline.

## Targeted validation terminal stop (2026-08-06)

- Executed the exact eight-selector command once. All eight selectors resolved to
  real test bodies; six passed and two errored. Result: `Ran 8 tests in 11.326s`,
  exit `1`, `errors=2`; output summary SHA-256
  `3889c42828011015acc9d9bb22fea77492c0ed89c694b985f6ac257c6cc9ff77`.
- The two errors were environment setup failures in the existing thermal and
  terminal consumers: both attempt to create their declared temporary roots under
  `/Volumes/4T/temp/rgbww-optimizer`, but this environment has no writable
  `/Volumes/4T` (`PermissionError: [Errno 13] Permission denied: '/Volumes/4T'`).
- This is a real test execution failure, not a selector mismatch. Per PLAN zero-retry
  rule, stopped immediately: did not run the four-test command, full suite, diff
  checks, compile/static checks, or CodeGraph sync; no device/formal/root/release/
  capture/network action and no commit was created.

## Corrective preflight terminal stop (2026-08-06)

- Read-only preflight target: `/Volumes/4T/temp/rgbww-optimizer`.
- Exact evidence: `exists=False`, `is_dir=False`, writable access `False`; `Path.stat()`
  raised `FileNotFoundError(Errno 2): [Errno 2] No such file or directory:
  '/Volumes/4T/temp/rgbww-optimizer'`.
- The parent `/Volumes/4T` is not writable/available to this environment. No directory
  was created, no `/tmp` fallback was used, and no selector was rerun. Corrective PLAN
  therefore terminal-stops before validation, with all device/formal/root/release/
  capture/network locks unchanged.

## Rejected candidate historical-only preservation

- Ref: `refs/heads/codex/historical-g4-r6-plan-full-runtime-alignment-rejected`.
- Commit: `f1ca21ce5df4a92ba9ebfbbb786d2d22c09269ba`.
- Tree: `03a504568b98d383f5d960be7a82b57a3144d469`.
- `implementation_input_allowed=false`.
- Live accepted source/test tree was restored without `reset` or `clean`.
- The historical ref is evidence only; it is not accepted production source and
  must not be merged, cherry-picked, copied, repaired, or used as future
  implementation input. Terminal rejection and all authority locks are unchanged.
