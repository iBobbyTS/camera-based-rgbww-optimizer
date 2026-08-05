# G4 R6 frozen-plan/runtime-context engineering recovery

## Status

- State: `active`
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

## Next action and stop

Implement one bounded candidate and run the PLAN's single validation ladder. One ordinary harness-only correction is allowed inside the same package. Any production ownership change, scope expansion, delta over 300 lines, second semantic failure, package/formal/device need, or inability to preserve strict validation returns to Planner/Orchestrator without another candidate.

