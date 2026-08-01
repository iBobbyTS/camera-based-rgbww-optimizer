# P7 retained-R3 Option B S1-C1-C1-C1 worktree PLAN read violation review

**Planner 日期：** `2026-08-01`

**Reviewed reference task：** `REF-P7-25-R2-B3-C3-C4-R5-R1-C1-R2-R1-C2-S1-C1-R1-D1-D2-C1-R2-C1-S1-C1-C1-C1`

**Reviewed contract：** `P7-TD-B-RETAINED-R3-OPTION-B-B3-C3-C4-R5-R1-C1-R2-R1-C2-S1-C1-R1-D1-D2-C1-R2-C1-S1-C1-C1-C1-FIXED-REPORT-MATRIX-PATH-CORRECTIVE-SUPERSESSION-V1`

**Decision：** `REJECTED_PRE_EXECUTION_WORKTREE_PLAN_READ_CONTRACT_VIOLATION_ZERO_EFFECT_NO_DURABLE_HANDOFF`

## 1. Reviewed scope and frozen identities

Activation commit `5f663c2c2243cc1d34e7b66fc6799bd9ad3092cc` has direct parent `220e888664ab7b232a5718317cf3111c6aa31a0d`, subject exact `chore(plan): bind fixed report matrix path`, and exact ordered changed paths:

1. `.agent-work/FULL_PLAN_REFERENCE.md`;
2. `.agent-work/PLAN.md`;
3. `.agent-work/PLANS/20260801-1617-p7-retained-r3-s1-c1-c1-matrix-path-failure-review.md`.

The activation archive is `7197` bytes with SHA-256 `29dae7776b2cd99271b63f8c38f34141691842fb905b6e284f23b7a3eace7059`.

Planner independently consumed the complete committed files through physical EOF:

- activation `.agent-work/PLAN.md`: `15779` bytes, SHA-256 `923297c42edae64b357c930eae4d49760a86d7d046fd12e85cefe3c0a81f7cfe`;
- activation `.agent-work/FULL_PLAN_REFERENCE.md`: `464129` bytes, SHA-256 `322bfaaa0170131e825db6011fcdf05719462f3b4e3ea301902ab49cde7012d4`;
- activation `.agent-work/EXECUTION_RESULT.md`: `1550853` bytes, SHA-256 `438c95e27261fc5be49b05e500c185879e558e7fecbae86be7546fd6613ee5d3`.

There is no evidence child: HEAD remains the activation, activation ER is byte-identical to parent ER, and the worktree was clean at Planner takeover.

## 2. Observed violation and zero-effect accounting

The Executer stopped during role/input reading. It used `sed` against the worktree path `.agent-work/PLAN.md` before acquiring the activation PLAN/FULL through the contract-selected Git objects. The active machine contract expressly lists `worktree_plan_read` under `current_input_identity_owner.forbidden` and requires `EXACT_ACTIVATION_GIT_OBJECT_RAW_BYTES` as parser inputs.

Therefore the pre-execution identity-owner gate failed at `WORKTREE_PLAN_READ_BEFORE_ACTIVATION_GIT_OBJECT_ACQUISITION`. This is a contract violation even though the worktree bytes happened to equal the activation object bytes. Byte equality cannot retroactively change the forbidden owner or transport.

Observed completed counters after that read and stop:

- worktree PLAN reads: `1`;
- worktree FULL reads: `0`;
- activation PLAN/FULL Git-object acquisitions: `0/0`;
- accepted PLAN/FULL parser calls: `0/0`;
- report/seal raw reads and strict loads: `0/0`;
- ER appends: `0`;
- controller invocations, selector calls, ledger Git attempts/processes: all `0`;
- matrix freezes/structural checks: `0/0`;
- artifact writes/reseals, repository code/test/skill/GUIDE/FULL writes: all `0`;
- network/device/camera/Ray/strip/cleanup/formal/release operations: all `0`;
- retry/fallback: `0/0`.

No durable `EXECUTION_RESULT.md` handoff was created. Because there was no report access, no matrix freeze, and no final supersession, the original execution contract remains rejected and synthetic engineering attribution facts are not newly accepted. Production owner, lineage, manifest truth, eligibility, release consumption, and retained-R3 validation receive no credit.

## 3. Planner findings

1. `S1-C1-C1-C1-OWNER-001`: current PLAN/FULL identity ownership is transport-sensitive. Only raw bytes emitted by exact activation Git-object lookup are valid inputs; a worktree read is forbidden even when its hash matches.
2. `S1-C1-C1-C1-READ-002`: the successor must ban every worktree read of both `.agent-work/PLAN.md` and `.agent-work/FULL_PLAN_REFERENCE.md`, including role discovery, preflight, hashing, parsing, comparison, or convenience inspection. The first PLAN/FULL content reads must be exact activation Git stdout/raw committed bytes.
3. `S1-C1-C1-C1-MATRIX-003`: the prior scientific/engineering path correction remains unchanged: the 18-row report collection is exactly `$.matrix`; `$.ledger_rows` is verified only as the literal value at `$.ledger_binding_proof.frozen_path`.
4. `S1-C1-C1-C1-LIFECYCLE-004`: since ER has no new durable record, a successor may use its sole final append to record both this zero-effect violation and the completed fixed-path supersession. It must not append a preliminary violation section, and retry remains `0`.
5. `S1-C1-C1-C1-CREDIT-005`: report/seal/controller/selector/Git ledger/device/release effects were all zero. The route remains `RETAINED_UNVALIDATED_UNCONSUMED` with every production/lineage/eligibility/release conclusion false.

This is an engineering/provenance input-owner correction. No Advisor scientific escalation and no Human device authorization are required.

## 4. Exact next branch

The sole next branch is `REF-P7-25-R2-B3-C3-C4-R5-R1-C1-R2-R1-C2-S1-C1-R1-D1-D2-C1-R2-C1-S1-C1-C1-C1-C1`. It must preserve the exact fixed-path matrix semantics and:

1. receive a new Orchestrator activation whose direct parent is `5f663c2c2243cc1d34e7b66fc6799bd9ad3092cc` and whose FULL machine state names only this successor active;
2. obtain PLAN/FULL only from exact activation Git-object stdout as raw committed bytes, once each, before any PLAN/FULL content inspection; never read either worktree path for role discovery, hashing, parsing, or validation;
3. parse those exact raw bytes with the accepted PLAN/FULL helpers once each, freeze activation ER through physical EOF, and retain retry/fallback `0/0`;
4. read the same fixed report/seal once each, strict-load once each, freeze exactly one 18-row collection from `report_value["matrix"]`, and separately verify `report_value["ledger_binding_proof"]["frozen_path"] == "$.ledger_rows"`;
5. append exactly one complete success supersession or one fail-closed handoff. On success, that single append must also state this predecessor's forbidden worktree read, zero downstream effects, and absent prior durable ER record; after append, operations are exactly `0`.

The successor must not rerun controller/selector/ledger Git, inspect or mutate evidence roots, read terminal/source/physical inputs, run self-check/tests/compileall/CodeGraph/validator, modify FULL/archives/code/tests/skill/docs/GUIDE, commit, or access network/devices/release paths.

## 5. Required Orchestrator activation handoff

Planner requires the Orchestrator to update FULL before activation so the active task count remains exactly one and the active task/contract point to the successor. Expected activation:

- parent: `5f663c2c2243cc1d34e7b66fc6799bd9ad3092cc`;
- subject: `chore(plan): forbid worktree plan reads`;
- exact ordered changed paths: `.agent-work/FULL_PLAN_REFERENCE.md`, `.agent-work/PLAN.md`, `.agent-work/PLANS/20260801-1624-p7-retained-r3-s1-c1-c1-c1-worktree-plan-read-violation-review.md`.

The expected evidence child, only after a compliant execution, has sole changed path `.agent-work/EXECUTION_RESULT.md` and subject `chore(evidence): seal worktree-read corrective supersession`.
