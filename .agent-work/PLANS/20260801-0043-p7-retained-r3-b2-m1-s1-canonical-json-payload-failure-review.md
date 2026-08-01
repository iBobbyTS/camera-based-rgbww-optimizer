# REF-P7-25-R2-B2-M1-S1-C1-C1-C1-C1-C1 Planner review：canonical JSON payload failure

**Review date：** 2026-08-01

**Reviewed contract：**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-M1-S1-C1-C1-C1-C1-C1-CODEGRAPH-FREE-EXACT-DIFF-CORRECTION-V1`

**Planner decision：** `REJECTED_TARGETED_PRODUCTION_CANONICAL_JSON_PAYLOAD_VIOLATION`

**Consumable：** `false`

## 1. Reviewed topology and evidence identity

Activation `89b9b54f30a698700289a4e9ae006e01c9a6d53f` is the direct child of
`540568c84d266c115f2a4fcdf9078fccc4956279`, has exact subject
`chore(plan): activate real manifest CodeGraph-free correction`, and changed exactly:

1. `.agent-work/FULL_PLAN_REFERENCE.md`
2. `.agent-work/PLAN.md`
3. `.agent-work/PLANS/20260801-0026-p7-retained-r3-b2-m1-s1-c1-c1-c1-c1-codegraph-routing-review.md`

Evidence `1b6715a2326d5a8d62d503e34e4cd8da76dfdf67` is the direct child of that activation,
has subject `chore(evidence): record real manifest fake runtime stop`, and changed only
`.agent-work/EXECUTION_RESULT.md`. The committed ER identity is blob
`7a084f14c6e941ca3d899fa4b4932d0080106645`, bytes `1202556`, SHA-256
`171d14a5e6e276be044130c5dbec40490d55aeb9af57d9410c7ba88006b4be65`.
The final EOF delta is the exact 15-line M1-S1-C1-C1-C1-C1-C1 handoff.

Rejected M1 candidate `cddd23eb4ef53a8f90c9b869f96f84ccfcba36cf` remains the direct child of
`84b3458765849f9c50515067788af365006cef68`, tree
`ff424f29e6a7a95349500ce356669a754d9ffa14`, and non-consumable. Retained R3 remains
`RETAINED_UNVALIDATED_UNCONSUMED`.

## 2. Correct but incomplete carried test changes

The worktree contains exactly one uncommitted path:
`tests/test_p7_retained_r3_real_manifest_domain_template.py`. Its identity is blob
`1df5786db37e7bb9cd4d5ffe26e4310d53f700aa`, bytes `18553`, SHA-256
`9d6deea37ab7d33748b95fa1dabc1380a3ae9677b4008684387699bc40bd1dd6`.
The canonical binary diff from activation is bytes `3404`, SHA-256
`b01f78668e05e709d33d415020dcb388fefe34980f381f823b14e8103e1cf777`.

Independent diff review confirms only two intended method edits:

1. test07 now creates a true duplicate path while preserving every preceding identity predicate, using
   `replace(spec().c1_inputs[0], label=spec().c1_inputs[1].label)` and expecting
   `path_collision`.
2. test13 replaces the invalid whole-source substring check with exact generated AST import-module,
   import-alias, and callable-token checks. The legal package
   `camera_based_rgbww_optimizer` no longer fails merely because its name contains `camera`.

No import, helper, test method, production source, or second test path changed. These two changes are
semantically correct and must be preserved byte-for-byte, but they are not accepted or consumable because
the targeted suite did not complete successfully.

## 3. Validation result and finding

The sole targeted invocation ran exact `13` tests and returned exit `1`: `12 pass / 1 error`.
test07 passed. test13 passed compilation and exact authority-surface assertions, then entered the
previously unreachable fake success lifecycle. During `phase_evaluate`, its fake `persist()` called the
real P3 `canonical_json_bytes(payload)` and received
`ProvenanceIOError("json_unsupported_value")`. Per immediate-stop rules, focused, compileall, full,
postcommit targeted, CodeGraph sync, stage, and correction commit all remained `0`; retry/fallback were
`0/0`.

### Finding REV-M1-JSON-001 — production payload violates the frozen P3 JSON value domain

This is not a fake-runtime fixture defect. The fixture faithfully uses the same canonical serializer that
production `persist_canonical_json()` uses. P3 `_freeze_json()` accepts exact `dict`, `list`, finite scalar,
boolean, and null values and deliberately rejects tuple with stable code `json_unsupported_value`; its
dedicated tests preserve that fail-closed contract.

Generated M1 production code constructs:

`{"activation": ACTIVATION, "baseline": BASELINE, "c1": C1_INPUTS, "retained": RETAINED_INPUTS, ...}`

All four contract values are tuples and several contain nested tuples. Therefore the same production
payload would fail before the first manifest write under the real P3 persistence owner. Replacing or
weakening fake `persist()`, permitting tuple in P3, or bypassing canonical encoding would hide the defect
and break the accepted provenance boundary.

The correct ownership boundary is: keep the immutable tuple contract for generated runtime validation and
Git/input semantics, then make one explicit JSON-native projection only at M1's manifest persistence
boundary. This is an engineering/provenance decision and requires neither Advisor nor Human authorization.

## 4. Safety, evidence quality, and zero-effect audit

The evidence is sufficient for rejection and for selecting the production owner. Activation/evidence
topology, ER identity, one-path diff identity, complete targeted count, first failure, and stopped budgets
are independently reproducible. It is not sufficient for owner acceptance or M1-I1 entry.

Production writes, second test path writes, external controller/root/process activity, retained artifact
reads, Git provenance replay, real B2, subordinate manifest physical writes, canonical validator/callback,
eligibility, retained audit/release, network/DNS/environment/credentials, device/camera/Ray/strip/cleanup,
capture/FORMAL/public analyzer/TD-C/sentinel/P8/firmware/deployment were exact `0`. PLAN/FULL/archive/debug/
GUIDE/RESEARCH were not modified by Executer.

## 5. Exact successor and preservation topology

Next branch:
`REF-P7-25-R2-B2-M1-S1-C1-C1-C1-C1-C1-C1`, contract
`P7-TD-B-RETAINED-R3-OPTION-B-B2-M1-S1-C1-C1-C1-C1-C1-C1-CANONICAL-JSON-PAYLOAD-CORRECTION-V1`.

Because the evidence commit was created while the correct dedicated-test diff remained uncommitted, the
Orchestrator must preserve it without falsely calling it validated. The fresh activation is the direct child
of evidence `1b6715a...`, includes exact FULL, PLAN, this archive, and the dedicated test, and records the
test blob/hash above as `UNVALIDATED_CARRY_FORWARD`. This returns a clean worktree and prevents either loss
of the correct diff or a misleading standalone accepted-test commit.

The Executer may then write only M1 production plus the same dedicated test. Production must explicitly
project activation, baseline including seam rows, C1 rows, and retained rows into JSON-native ordered lists
at `manifest_payload`; internal tuple ownership, field order, values, schema, status, artifact names, and
canonical serializer remain unchanged. No generic converter/helper, serializer widening, fallback, or
parallel owner is permitted.

The dedicated test must preserve the carried test07/test13 corrections, update the golden template hash,
and make the fake success path assert the persisted manifest's exact JSON-native ordered shape. Tuple
rejection remains covered by the frozen P3 suite. Validation is targeted `13/13`, focused `83/83`,
compileall, full `800/800`, one post-test maintenance-only `codegraph sync`, single two-path implementation
commit, and postcommit targeted `13/13`; retry/fallback `0/0`.

维护性判断：下一包修复发生在唯一错误 owner——M1 的 manifest projection boundary；P3 serializer、
P4 lifecycle、P5 runtime composition和内部immutable tuple contract均保持不变，不新增helper、转换框架或
状态机。
