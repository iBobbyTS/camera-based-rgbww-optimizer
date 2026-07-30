# REF-P7-25-R2-B2-C4-P1-C1：accepted；等待 Orchestrator provenance binding

**计划状态：** `PLANNER_ACCEPTED_EXECUTION_NOT_AUTHORIZED`

**Planner 日期：** `2026-07-30`

**Reviewed reference task：** `REF-P7-25-R2-B2-C4-P1-C1`

**Disposition contract ID：**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-C4-P1-C1-ACCEPTED-ORCHESTRATOR-GATE-V1`

**当前唯一动作：** Orchestrator 独立复核本次 Planner acceptance，将 successor
`4678a3e6f93704912952776bc11fa2b0945d80b1` 绑定到 Orchestrator-owned exact
provenance route，并决定下一份最小 C4 integration engineering package；本计划不向
Executer 放行任何动作。

**唯一 Planner stop：**
`B2_C4_P1_C1_ACCEPTED_WAITING_ORCHESTRATOR_PROVENANCE_BINDING`。

**本次 review archive：**
`.agent-work/PLANS/20260730-1247-p7-retained-r3-option-b-b2-c4-p1-c1-implementation-review.md`
（bytes `7625`，SHA-256
`45ddabac38649f6d635ede63821e21baaf4aca1fc37c47bd9077600fee776293`）。

`PLAN_MACHINE_CONTRACT={"schema":"p7_td_b_retained_r3_option_b_b2_c4_p1_c1_accepted_orchestrator_gate_v1","reference_task_id":"REF-P7-25-R2-B2-C4-P1-C1","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-C4-P1-C1-ACCEPTED-ORCHESTRATOR-GATE-V1","decision":"accepted_complete_waiting_orchestrator_provenance_binding","execution_authorized":false,"dispatch_state":"not_dispatchable","single_current_action":"orchestrator_bind_successor_provenance_and_select_next_integration_package","accepted_successor":"4678a3e6f93704912952776bc11fa2b0945d80b1","accepted_successor_parent":"a99292e3cc75345d3c783131fd4c716b8fe698f7","exact_changed_paths":["src/camera_based_rgbww_optimizer/utils/p7_retained_r3_controller_preparation.py","tests/test_p7_retained_r3_controller_preparation.py"],"canonical_validator_remains_sole_eligibility_owner":true,"historical_c4_reads":0,"retained_r3_reads":0,"canonical_validator_calls":0,"eligibility_emissions":0,"release_operations":0,"device_operations":0,"next_plan_owner":"Planner_after_orchestrator_reference_update","planner_stop":"B2_C4_P1_C1_ACCEPTED_WAITING_ORCHESTRATOR_PROVENANCE_BINDING"}`

## 1. Planner decision

Planner accepts the bounded P1-C1 correction as complete and mergeable.

- Exact successor topology passed: `4678a3e6...` has direct parent
  `a99292e3...`, one commit from dispatch parent, exact subject and exact two-path
  change set. `ce096155...` remains an ancestor through the PLAN-only activation
  commit.
- Current helper/test SHA-256 values are respectively
  `882f3819d161369012ce7fcd52cb1de1b9c56e4e1f821ff4554f6a1d8340738b`
  and
  `80ef2bead548856031c6d6f07f4ee0b6c74b8b917a45787e9f96fbf57b4d4527`.
- `REV-P1-001` through `REV-P1-004` and the `ImportFrom.module` static-guard
  gap are closed by current code and dedicated regressions.
- Executer reports targeted `21/21`, related `11/11` and `21/21`, full
  `712/712`, compileall, CodeGraph, diff/path and postcommit targeted gates all
  passed. Planner did not rerun tests; independent review used current commit
  topology, exact diff, CodeGraph and static AST inspection.
- No new `Must Fix` or accepted `Should Fix` finding remains. The canonical
  lineage validator remains the sole eligibility owner.

Full method, evidence quality, findings and residual risk are frozen in the new
review archive above. Completed implementation detail is intentionally removed
from this active PLAN.

## 2. Current non-executable gate

This PLAN is not an execution package. Orchestrator must now:

1. independently accept or reject the Planner disposition;
2. update `.agent-work/FULL_PLAN_REFERENCE.md` with the accepted successor and
   exact provenance-binding state;
3. decide the smallest next integration engineering branch;
4. request a new Planner pass to write exactly one successor package.

Only a later Planner-authored and Orchestrator-reviewed PLAN may set
`execution_authorized=true`. No Executer should be dispatched from this file.

## 3. Hard locks

Until the Orchestrator completes the gate and a new PLAN explicitly releases a
bounded action, all of the following remain locked:

- historical C4 external source, builder, root and artifacts;
- real B2, retained-R3 candidate/artifact reads and retained audit;
- B3, canonical validator invocation and eligibility emission;
- lineage/release creation, validation or consumption;
- public analyzer, network, `.env`, credentials and all device/camera/Ray/strip/
  cleanup/capture/FORMAL/TD-C/sentinel/P8/firmware/deployment work;
- any additional implementation edit, test run, commit, retry or fallback.

P1-C1 acceptance does not itself authorize C4 integration or any later stage.

## 4. Stop and handoff

Stop exactly at
`B2_C4_P1_C1_ACCEPTED_WAITING_ORCHESTRATOR_PROVENANCE_BINDING` and hand the
archive path/hash, accepted successor, exact changed paths and residual locks to
the Orchestrator. Planner must not edit `FULL_PLAN_REFERENCE.md`; Executer must
not act on this PLAN.

## 维护性判断

The accepted correction keeps all new semantics inside one pure preparation
owner and its dedicated test owner. The next route should integrate this owner
without creating another external controller framework or parallel eligibility
owner.
