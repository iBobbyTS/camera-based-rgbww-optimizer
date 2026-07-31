# REF-P7-25-R2-B2-R2-C1-C1 activation-metadata pre-root failure review

**Planner review date:** `2026-07-31`

**Reviewed contract:**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-R2-C1-C1-LOGICAL-MODE-AND-FAIL-EVIDENCE-QUALIFICATION-V1`

**Reviewed active PLAN identity:** bytes `15291`, SHA-256
`6ce303f7f42e8aa94c5acb761b353feea1a186eeb8aab8653203b469c1ee358c`.

**Decision:**
`REJECTED_BOUNDED_B2_R2_C1_C1_ACTIVATION_IDENTITY_DOMAIN_MIXUP_CORRECTION_REQUIRED`

## 1. Reviewed scope and immutable evidence

Planner performed a bounded read-only review of the committed active PLAN, its sole
matching Executer handoff, the retained controller source, the frozen absent output
root, and the activation/evidence Git topology. Planner did not rerun the controller,
create or reuse a root, read accepted C1 or retained-R3 artifacts, replay retained Git
provenance, call the canonical validator, emit eligibility, perform release work, or
access network/device/scientific routes.

The actual activation topology is exact:

- activation commit `03ce3df268096abe67568a806267ebf8a44c2980`;
- direct parent `ebaddb5795720cc446f70ea1d32dfcb40cbae27a`;
- subject `chore(plan): activate b2 logical mode correction qualification`;
- changed paths exactly `.agent-work/FULL_PLAN_REFERENCE.md`,
  `.agent-work/PLAN.md`, and
  `.agent-work/PLANS/20260731-1011-p7-retained-r3-b2-r2-c1-linkage-qualification-failure-review.md`.

The matching evidence commit is
`e3a776e493e3c7e4aaf6d98e159bb3c13c676bfd`, direct child of the activation commit,
with subject `chore(evidence): record b2 activation metadata failure`.

The immutable controller source is
`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b2-r2-c1-c1-logical-mode-controller-ebaddb5-20260731T1611Z.py`,
bytes `19547`, mode `0600`, device `16777240`, inode `2217870`, independently
recomputed SHA-256
`0db566264282c3f97cee21bf5303bb91b830bd5aef53a3c9a27dfcf963d8b969`.
The frozen output root
`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b2-r2-c1-c1-logical-mode-qualification-ebaddb5-20260731T1611Z`
is absent and must remain absent. The source must not be rewritten or rerun.

The failure is safe and internally bounded: one controller process exited `1`;
PLAN/FULL each read once; activation Git invocations stopped at call `2/6`; root,
C1 reads, matrix, qualification/seal, terminal/seal and admission were all `0`.
Retry, fallback, alternate source/root and second process were all `0`. No scientific
conclusion can be drawn from this engineering preflight failure.

## 2. Findings

### REV-B2-R2-C1-C1-001 — Must Fix: active and reviewed-failure activation identities were mixed

The source freezes:

```text
HEAD = 1bd06c4a0279f51546cf22c38581e2ab411c67d1
PARENT = ebaddb5795720cc446f70ea1d32dfcb40cbae27a
SUBJECT = chore(plan): activate b2 logical mode correction qualification
```

`PARENT`, `SUBJECT`, and the three paths describe the current activation contract,
but `HEAD` is the predecessor package's `reviewed_failure.activation_head`. The
current activation is `03ce3df268096abe67568a806267ebf8a44c2980`. Git invocation
1 only proves the stale commit exists; invocation 2 returns its real parent/subject,
which cannot equal the mixed expected tuple, so the controller deterministically
raises `RuntimeError:activation_metadata`.

This is not Git drift. It is a controller-composition provenance-domain error. The
successor must obtain its activation head only from Git call 1 against current
`HEAD`, freeze that returned full SHA in memory, and use it for calls 2-6 and all
written evidence. Expected parent, subject and exact paths must come only from the
active `activation_commit` object. No field under `reviewed_failure`, no historical
activation SHA, and no abbreviated SHA may feed the active activation tuple.

### REV-B2-R2-C1-C1-002 — Must Fix: source identity must survive pre-root failure without reread

The source was written and read once before dispatch, but the Executer handoff says
its SHA existed only inside the failed child and therefore could not be reported.
The immutable source remains independently auditable, but this weakens a pre-root
handoff unnecessarily. The successor launcher must retain the one source-read
`FileIdentity` outside the child lifecycle and use that already-held identity in any
pre-root handoff. It must not perform a second source read after failure.

### REV-B2-R2-C1-C1-003 — Preserve accepted logical-mode, root-first and seal/admission contracts

The package failed before root acquisition and before C1 reads, so it did not test or
invalidate the frozen physical integer `384` to logical string `"0600"` mapping,
root-before-C1 ordering, exact `20`-case matrix, or valid PASS/FAIL terminal
seal-dominant admission. The successor must preserve those contracts unchanged.
It may only correct active activation binding and outer source-identity retention.

## 3. Validation quality and residual risk

Planner independently verified the source bytes/SHA/stat identity, source constants,
absent root, active PLAN bytes/SHA, actual activation metadata/path set, and evidence
commit parentage. The failure is localized before external evidence access.

No qualification artifact exists. Therefore logical-mode mapping, corrected direct
linkage, negative matrix, terminal seal and admission are still unproven. Retained R3
remains unvalidated and unconsumed; real B2, subordinate manifest, canonical
validator, eligibility, release and device/scientific work remain locked.

## 4. Decision and next branch

Reject the result as
`REJECTED_BOUNDED_B2_R2_C1_C1_ACTIVATION_IDENTITY_DOMAIN_MIXUP_CORRECTION_REQUIRED`.
The sole next branch is `REF-P7-25-R2-B2-R2-C1-C1-C1`, contract
`P7-TD-B-RETAINED-R3-OPTION-B-B2-R2-C1-C1-C1-ACTIVATION-BINDING-LOGICAL-MODE-QUALIFICATION-V1`.

It is one fresh pure-offline qualification with the same accepted-C1 reads,
logical `"0600"`, root-first lifecycle, `20` cases, terminal seal and admission
contracts. Its only correction is a single-source active activation tuple plus
retained outer source identity. It may not read or rerun either rejected controller,
create either absent rejected root, read retained R3, retry real B2, replay retained
Git provenance, write a subordinate manifest, call the canonical validator, emit
eligibility, perform release work, or access network/device/scientific routes.

Passing this successor only qualifies the composition controller for a later
fresh-real-B2 Planner package. It does not authorize real B2 or any later stage.

**Proposed FULL transition:** mark `REF-P7-25-R2-B2-R2-C1-C1` as
`REJECTED_ACTIVATION_IDENTITY_DOMAIN_MIXUP_PRE_ROOT`; add
`REF-P7-25-R2-B2-R2-C1-C1-C1` as the sole task waiting for Orchestrator activation;
set `repair_v2_status=R2_C1_C1_REJECTED_ACTIVATION_BINDING_C1_ACTIVE`; retain
`retained_r3_status=RETAINED_UNVALIDATED_UNCONSUMED`; keep real B2 retry, retained
reads, manifest, validator, eligibility, release, and all device/scientific work
locked.

## 5. Planner self-check and handoff

- replacement PLAN contains exactly one strict-JSON `PLAN_MACHINE_CONTRACT` row;
- the row identifies one next task, one contract and one Planner stop;
- archive and PLAN are the only Planner-owned changes;
- FULL, ER, GUIDE and RESEARCH remain unchanged;
- `git diff --check` passes;
- no stage, commit, controller execution, rejected-source/root mutation, C1 or
  retained read, manifest, validator, release, network or device operation occurred.

Orchestrator must independently review this archive/PLAN, update FULL, create the
exact activation commit, and only then dispatch a fresh Executer. Planner stops at
`B2_R2_C1_C1_C1_ACTIVATION_BINDING_QUALIFICATION_WAITING_ORCHESTRATOR_ACTIVATION`.

维护性判断：缺陷位于一次性外置 controller 的activation数据域绑定，不需要修改生产owner；
下一包保持既有20-case与evidence lifecycle，只增加明确的单一来源约束和pre-root身份保留。
