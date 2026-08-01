# REF-P7-25-R2-B3-C3 Planner route-selection archive

**Archive time:** `2026-08-01T05:28:12-0600`

**Selected reference task:** `REF-P7-25-R2-B3-C3`

**Selected contract:**
`P7-TD-B-RETAINED-R3-OPTION-B-B3-C3-FRESH-POSTCOMMIT-SELF-CHECK-TEST-SYNTHETIC-V1`

**Planner disposition:** `READY_FOR_ORCHESTRATOR_ACTIVATION`

## 1. Archived stop

The prior active PLAN was the accepted B3-C2-S1 Orchestrator route stop. Its committed identity at
`1f121b16502d869ed31d6b6cccc0a79d3dbdd737` was bytes `4336`, SHA-256
`87044f48ace7ba5eb160cbcda37ad9f17954622b28a90ef6de70b9a925ef897e`. It recorded:

- reviewed task `REF-P7-25-R2-B3-C2-S1`;
- decision `ACCEPTED_COMPLETE_EXECUTION_BUDGET_DISTINCTION_SEALED`;
- evidence commit `798e459761946f48f69d8c87c48dfaee6961becd`;
- retained state `RETAINED_UNVALIDATED_UNCONSUMED`;
- stop `B3_C2_S1_ACCEPTED_WAITING_ORCHESTRATOR_POSTCOMMIT_VERIFICATION_ROUTE`;
- execution authorization `false`.

That stop is complete and is archived without replacing or overwriting
`.agent-work/PLANS/20260801-0523-p7-retained-r3-b3-c2-s1-budget-supersession-review.md`.

## 2. Orchestrator selection basis

Orchestrator commit `1f121b16502d869ed31d6b6cccc0a79d3dbdd737`, parent
`798e459761946f48f69d8c87c48dfaee6961becd`, subject
`chore(plan): route fresh postcommit verification`, changed exactly:

1. `.agent-work/FULL_PLAN_REFERENCE.md`;
2. `.agent-work/PLAN.md`;
3. `.agent-work/PLANS/20260801-0523-p7-retained-r3-b3-c2-s1-budget-supersession-review.md`.

The committed FULL state selects `REF-P7-25-R2-B3-C3` as `READY_FOR_PLANNING`, with zero active executable tasks.
It preserves the accepted B3-C2 implementation commit
`e84f5b6adc7c004b388074f5e81a4d109a6541f2`, the accepted B3-C2-S1 evidence distinction, the canonical lineage
validator as sole eligibility owner, and the retained R3 state as unvalidated/unconsumed.

The selected package must supersede the failed execution routes without rewriting their history:

- B3 failed because it invented an artifact top-level `passed` field;
- B3-C1 failed because it invented canonical machine-row re-encoding/raw-byte equality;
- B3-C1-C1 failed because of non-EOF handoff, unauthorized CodeGraph, and governance identity misbinding;
- B3-C2 fixed the governance field owner while preserving all twelve serialized values, but its original execution
  exceeded source/test direct-read budgets;
- B3-C2-S1 accepted and sealed the distinction between the rejected execution and accepted implementation.

## 3. Selected executable route

The replacement active PLAN must authorize exactly one pure-offline fresh postcommit package in this order:

1. parse activation PLAN/FULL machine rows using only exact delimiter, strict UTF-8/JSON and typed semantic checks;
2. independently verify the accepted real manifest, exact terminal/seal/admission schema, frozen real input physical
   identities, and manifest-bound Git identities;
3. run the focused suite exactly once;
4. run durable full discovery exactly once;
5. create and verify one brand-new activation-derived synthetic terminal/replay root;
6. append one physical-EOF execution handoff as the final operation and stop for Planner review.

Machine-row acceptance must not use canonical re-encoding, key order, whitespace normalization or raw-vs-reencoded
byte equality. Artifact acceptance must not require or infer a top-level `passed` field. The baseline serialized position
8 is the external lineage-owner decision evidence SHA; position 9 is the Advisor Option-B attachment SHA. The Advisor
request Git document is not serialized baseline position 8.

## 4. Locks and acceptance boundary

The package may read only the frozen real manifest/source, C1 four files, retained R3 three files, and exact repository
Git/governance identities named by the PLAN. It may write only a fresh synthetic root and one
`EXECUTION_RESULT.md` EOF handoff. It must not repair, rewrite, regenerate, copy or relocate the accepted manifest or
any real input.

Canonical lineage validator calls, real retained audit, eligibility emission, release generation/qualification/copy/
consumption, network, DNS, environment, credentials, devices, camera, Ray, strip, cleanup, capture, formal, public
analyzer, TD-C, sentinel, firmware, deployment and P8 remain zero. Passing B3-C3 closes only the postcommit engineering
verification gate and permits Planner to propose B4; it does not itself unlock or perform B4.

No Advisor scientific decision or Human device authorization is needed for this offline package.

## 5. Activation topology chosen by Planner

Orchestrator activation must be the direct child of
`1f121b16502d869ed31d6b6cccc0a79d3dbdd737`, with exact subject
`chore(plan): activate fresh postcommit verification` and exact changed paths:

1. `.agent-work/FULL_PLAN_REFERENCE.md`;
2. `.agent-work/PLAN.md`;
3. `.agent-work/PLANS/20260801-0528-p7-retained-r3-b3-c3-postcommit-verification-selection.md`.

The worktree must be clean after activation. The executable package stops at
`B3_C3_FRESH_POSTCOMMIT_SELF_CHECK_TEST_SYNTHETIC_WAITING_PLANNER_REVIEW` whether it passes or fails.

维护性判断：该选择复用既有P3 physical/Git owner、M1 deterministic domain owner、P5 runtime owner及既有测试入口；
一次性controller仅编排冻结事实，不新增production schema、generic allowlist、validator或平行provenance owner。
