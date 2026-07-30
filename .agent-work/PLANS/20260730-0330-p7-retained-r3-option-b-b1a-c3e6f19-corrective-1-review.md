# F19-C1 activation-gate failure review

**Planner review UTC：** `2026-07-30T03:30:48Z`

**Reviewed reference task：** `REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-1`

**Reviewed contract：** `P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F19-CORRECTIVE-1-STATIC-TEST`

**Verdict：** `REJECTED_BEFORE_PATH_OPERATIONS_WRONG_PLAN_MARKER_OWNER`

## 1. Reviewed scope and method

Planner reviewed the committed active PLAN at HEAD
`2413ef03f05c0d271879dbc4c873c93546074bdf`, the Orchestrator-owned FULL reference,
Git activation lineage, the Executer terminal handoff, and the committed machine-contract helper.
Planner did not run tests, create an evidence root, access old F19 evidence, retained R3,
candidate or release data, or perform any device/network operation.

The activation commit itself is valid:

- direct parent: `784b0de8722d60af2a08a7346015de127540ffe2`;
- exact subject: `chore(plan): activate f19 static-test corrective`;
- changed-path set: exactly `.agent-work/PLAN.md`;
- clean porcelain SHA-256:
  `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`;
- FULL raw SHA-256:
  `1125e0a0474f3e34f073c9b7c3639217a5ebe797a1be25e9c8b2efc192abae96`.

## 2. Root cause and exact evidence

Executer stopped with activation-gate exit `1` and
`missing PLAN_MACHINE_STATE`. Its gate had transcribed and searched for a line shaped
`PLAN_MACHINE_STATE={...}`. No such canonical owner exists.

The committed validation-only helper
`src/camera_based_rgbww_optimizer/utils/agent_work_machine_contract.py` is authoritative:

- `PLAN_MACHINE_MARKER = b"`PLAN_MACHINE_CONTRACT="` and
  `parse_plan_machine_contract(source)` owns PLAN parsing;
- `FULL_PLAN_MACHINE_MARKER = b"`FULL_PLAN_MACHINE_STATE="` and
  `parse_full_plan_machine_state(source)` owns FULL parsing.

Therefore the failure is an Executer activation-gate transcription error, not a PLAN/FULL
shape contradiction and not a scientific issue. Future execution must call those committed
helper APIs directly; it may not retype, alias, infer or independently scan either marker.

## 3. Fail-fast and immutability audit

The gate failed before any repository-path operation:

- fresh corrective root is independently confirmed absent;
- test file was not edited;
- compileall, targeted, focused, full unittest, CodeGraph and diff-check invocations: `0`;
- `.agent-work/EXECUTION_RESULT.md` append count: `0`; its HEAD and parent blob are both
  `90946b3053623069ba7100332605a21e0dc46ff7`;
- retry/fallback/alternate path: `0`;
- stage/commit/controller/candidate/retained-R3/validator/eligibility/manifest/release/network/
  env/device/camera/Ray/strip/cleanup/formal/public-analyzer operations: `0`.

Planner independently verified committed/worktree identity remains exact:

| Path | Blob OID | SHA-256 |
| --- | --- | --- |
| `src/camera_based_rgbww_optimizer/utils/p7_retained_r3_exact_five_controller.py` | `45097745bcc48aa1312b06fc07c6c910a4529325` | `746fd13056c326489b48ca555b21618b65c8a78f198d035e18c02f68af689726` |
| `tests/test_p7_retained_r3_exact_five_controller.py` | `656dbda9cf852e1a52affe5edd60148366f401bf` | `579ae0cbd6517cccdf184dfc2eb89e90b20c08cb502dcbe5c292ba5914edc647` |

Because the failed gate stopped before later identity/archive checks, those unchecked fields are
not promoted to Executer evidence. Planner's independent committed-byte checks prove only the two
repo identities above and fresh-root absence.

## 4. Decision, residual risk and exact next branch

F19-C1 is rejected without consuming its one test edit or any validation-chain budget.
The exact next branch is one bounded F19-C2 package preserving the same test-only correction,
fresh-root name, validation order, zero locks, retry `0`, and Planner stop. Its activation gate must:

1. import the committed helper by module API;
2. pass raw PLAN bytes only to `parse_plan_machine_contract`;
3. pass raw FULL bytes only to `parse_full_plan_machine_state`;
4. compare returned values/evidence to the frozen task/contract/FULL identity;
5. forbid handwritten marker constants, aliases, fallback scanners and payload repair.

The Orchestrator should update FULL from C1 rejected to
`REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-2` pending activation, then request one Planner activation
pass to freeze the aligned FULL raw SHA and exact activation lineage before dispatch.

No Advisor or Human decision is required: this is a local engineering/contract-owner correction,
and no high-risk device operation is present.

**Residual risk：** until FULL alignment and the next exact activation commit are independently
verified, C2 remains non-dispatchable. Retained R3 remains
`RETAINED_UNVALIDATED_UNCONSUMED` and B2 remains locked.

**Planner stop：** `F19_CORRECTIVE_1_REJECTED_WAITING_ORCHESTRATOR_FULL_ALIGNMENT`.

