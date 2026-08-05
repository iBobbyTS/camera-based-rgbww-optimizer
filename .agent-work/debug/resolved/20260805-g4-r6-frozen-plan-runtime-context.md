# G4 R6 frozen-plan/runtime-context engineering recovery

## Status

- State: `resolved`
- Reference task: `REF-G4-06-ENGINEERING-RECOVERY`
- Contract: `G4-R6-FROZEN-PLAN-RUNTIME-CONTEXT-RECOVERY-V1`
- Scope: offline code/test/debug evidence only
- Current hypothesis confidence: high from production traceback plus CodeGraph ownership trace

## Confirmed observations

1. The Supervisor-corrected visible-Terminal formal chain crossed the production package loader and Route A, then failed before capture in `execute_plan` validation.
2. Primary error: `runtime_template_drift`, surfaced as `PermissionError: thermal diagnostic R6 PLAN-bound authority differs`.
3. Secondary terminal projection: `terminal_replay/file_lstat_failed`; it is not the primary code defect.
4. Historical run classification is `ENGINEERING_INVALIDATED_PRECAPTURE_FORMAL_ABORT`: launch/attempt/root/loader `1/1/1/1`, captures/nonzero `0/0`, retry/alternate `0/0`, strip zero proven, Ray zero unproven.
5. Orchestrator CodeGraph trace: `run_authorized_plan` validates the frozen plan, resolves camera settings, deep-copies the plan, writes `camera.resolved_capture_settings`, then passes the changed plan to `execute_plan`; `execute_plan` validates again before writing `run.json` or capturing.
6. `validate_authorized_execution_plan` converts the stable `StageGateError` into a generic `PermissionError` surface, leaving the stable code only in the cause.
7. The bounded candidate now leaves the materialized plan untouched, threads one explicit `runtime_capture_settings_provenance` mapping into `execute_plan`, records it in `run.json`, and passes it beside the original plan to the post-capture callback.
8. The full fake chain regression passed without mocking `execute_plan`; frozen-plan SHA-256 before/after was `98272889c893a96d2a00396be30d59e26c5bab64a7a22cfcf5d901230214d8c3` in the recorded run.
9. Stable drift evidence now surfaces `runtime_template_drift` in the outer `PermissionError`, while `__cause__` remains the original `StageGateError` with the same code.
10. Targeted tests passed `2/2`; stage-gate focused completed without failure; terminal focused passed `6/6`; compileall passed. Thermal focused ran `89` tests and stopped with `2` failures plus `8` errors, all rooted in the pre-existing governance successor rejecting current `AGENTS.md` path identity before the assertions under test.
11. The single permitted full discovery invocation ran `975` tests in `334.424s`: `965` passed, `2` failed, and `8` errored. Its ten failures are the exact same governance-lineage group; no runtime-context test failed. Full discovery was not rerun.

## Failed or invalid approaches

- The prior standalone strict `describe` precheck was invalid after orchestration drift and is historical only.
- The corrected production launch proved the package/Route A path, but the offline suite lacked a full fake-backend regression through `run_validated_td_b_r6_runtime_contract -> run_authorized_plan -> execute_plan`.
- Retrying formal execution, reminting the package, changing the frozen template, or widening validator allowances would violate the current recovery contract.

## Root-cause hypothesis

The frozen materialized runtime plan is both the strict authority object and an implicit carrier for resolved camera runtime state. Adding `resolved_capture_settings` to that authority object makes the second strict validation correctly reject it. Runtime-resolved settings must instead have one explicit parameter/context owner while the frozen plan bytes and mapping remain unchanged.

## Minimal repair boundary

- Keep strict validation of the original materialized R6 plan unchanged.
- Pass resolved capture settings/provenance into existing `execute_plan` through an explicit runtime context/argument.
- Persist that runtime context in `run.json` and pass it explicitly to post-capture validation while retaining the original frozen plan.
- Preserve stable `StageGateError.code` at the outer error surface using the existing exception/cause path; do not introduce a new exception owner or broad ignore list.
- Limit production/test changes to `measure_p7_thermal_diagnostics.py` and `test_p7_thermal_diagnostics.py`; estimated production+test delta 140–240 lines, hard cap 300.

## Required regression

Use a materialized R6 plan and fake remote backend. Do not mock `execute_plan`. Exercise the complete chain:

`run_validated_td_b_r6_runtime_contract -> run_authorized_plan -> execute_plan`

Prove:

- resolution no longer causes `runtime_template_drift`;
- caller-owned input plan is unchanged before/after;
- `run.json` records resolved settings/provenance;
- post-capture validation receives the frozen plan plus explicit runtime evidence;
- a truly unknown template field still fails closed with a stable code;
- every device/light/capture effect is fake-only and performs no connection.

## Planner acceptance evidence

- Disposition: `ACCEPTED_G4_R6_FROZEN_PLAN_RUNTIME_CONTEXT_RECOVERY_CANDIDATE`.
- Reviewed PLAN archive: `.agent-work/archived/PLAN-20260805-0144.md`, 22046 bytes, SHA-256 `5f3f9c618cbe4056792f453e9a8ac998daea3cb85e7768d834a2ef56a8414035`.
- Reviewed EXECUTION_RESULT archive: `.agent-work/archived/EXECUTION_RESULT-20260805-0144.md`, 8376 bytes, SHA-256 `ed963caacf72a0f803b976999d6275dcee71b0c4dcff54b1d5c2225a3e149f4f`.
- Accepted production identity: `src/camera_based_rgbww_optimizer/optimization/measure_p7_thermal_diagnostics.py`, SHA-256 `0ae294b08317983abbed838aac355233d12eaf0d602192229aa92ce755f1041f`, Git blob `90000ff11a6603fc63515061d391200a46765380`.
- Accepted test identity: `tests/test_p7_thermal_diagnostics.py`, SHA-256 `6cc395d76ea5ad1182f4671b2eb401bedb54d0b6a64dc4b1120a32ae0f9dbb46`, Git blob `272eacf4c302af5d64483620978411998497b242`.
- Production/test delta is 235 changed lines (`43+/18-` production, `170+/4-` tests), below the 300-line hard cap; no new module, schema, runner, or semantic owner was introduced.
- Independent targeted log: `/Volumes/4T/temp/rgbww-optimizer/planner-g4-r6-review.5wz2jS/targeted-independent.log`, 643 bytes, SHA-256 `7f0640206f7f0203fdbbe7105645e8e99596a2361f4e41405fe32ec3efcb8074`; `2/2` passed and proved `execute_plan` identity unchanged plus restored keyword defaults. The test's temporary clock-default substitution exercises the real `execute_plan` body and is a bounded harness seam, not a parallel semantic owner.
- Independent thermal-focused stderr: `/Volumes/4T/temp/rgbww-optimizer/planner-g4-r6-review.5wz2jS/thermal-focused.stderr.log`, 17325 bytes, SHA-256 `01f223db353b85e70ddbafc7f782cd78ceec1e1ff154af58828fcf9d1fe9f9a2`; 89 tests ran in 23.022 seconds with the same `2` failures and `8` errors as full discovery. All ten terminate first at the governance successor rejecting `AGENTS.md` path identity.
- The activation baseline commit `dafcd619f57abfa3f395277504d84d2d374d9f6d` changes only `AGENTS.md`; the candidate does not change `AGENTS.md`, the governance owner, or any failing test method. The ten governance-lineage results therefore qualify as pre-existing activation/baseline drift, not candidate regressions.
- Candidate validation accepted: targeted `2/2`, stage-gate `47/47`, terminal `6/6`, compile, CodeGraph sync/query, and diff checks pass. The single full discovery ran 975 tests in 334.424 seconds: 965 passed, 2 failed, 8 errored; it was not rerun and is not represented as a green full suite.
- Historical formal ledger remains `ENGINEERING_INVALIDATED_PRECAPTURE_FORMAL_ABORT` with no scientific, quality, history, release, eligibility, or device-readiness credit.

## Next action and stop

Return to Orchestrator for one focused code checkpoint containing only the accepted production and test paths. Do not create or authorize a replacement package, formal task, device operation, or G4-07 package in this Planner review.
