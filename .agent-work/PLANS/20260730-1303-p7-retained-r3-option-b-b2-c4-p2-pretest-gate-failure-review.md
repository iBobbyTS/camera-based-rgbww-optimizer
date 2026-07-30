# REF-P7-25-R2-B2-C4-P2 pretest scope gate failure review

**Review date:** `2026-07-30`

**Reviewed reference task:** `REF-P7-25-R2-B2-C4-P2`

**Reviewed contract:**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-C4-P2-INTEGRATION-QUALIFICATION-V1`

**Planner decision:**
`REJECTED_GATE_DEFECT_IMPLEMENTATION_NOT_EVALUATED`

**Reviewed PLAN identity:** bytes `13993`, SHA-256
`9614ee5ef70a80fea46b3622d569bc344a4ec2eedb7c4150bf6aa7f7ac8846b5`.

**Reviewed stop:**
`B2_C4_P2_INTEGRATION_QUALIFICATION_COMPLETE_WAITING_PLANNER_REVIEW`.

## 1. Reviewed scope and implementation method

The reviewed package authorized exactly one new test path:

```text
tests/test_p7_retained_r3_controller_integration.py
```

Its intended method was a pure synthetic integration qualification through the
existing public APIs of the accepted controller-preparation owner and the
exact-five callback lifecycle. It prohibited production changes, a new adapter,
an external generated controller, real retained-R3 reads, the actual canonical
validator, eligibility, release, network, device and scientific-stage work.

The ordered workflow required the Executer to complete repository/FULL/input
preconditions, create the singleton test, prove the pretest path set, then run
targeted, owner, focused, full, compileall and CodeGraph gates before one exact
commit and one postcommit targeted test.

## 2. Execution evidence reviewed

The sole handoff is the final section of
`.agent-work/EXECUTION_RESULT.md`, whose current worktree identity at review was
bytes `958638`, SHA-256
`7048d2a8a8af50b1706dbba61e2a31352613d4cfe1453b29fedc3f97e58dd8e7`.

Independently observed activation topology:

- HEAD: `e45cf6a70204d87a5b4b47f19149e80e087cb634`;
- direct parent: `3458b4b60c49328703a6e2bc95a62f33e13cdfe8`;
- subject: `chore(plan): activate retained r3 integration qualification`.

The handoff records that the initial preconditions passed once and the
Executer created only the intended test. The preserved test identity is:

- path: `tests/test_p7_retained_r3_controller_integration.py`;
- type: regular file, not tracked by Git;
- bytes: `13147`;
- SHA-256:
  `106ddcafddbc31d8172b3f6a3a2557830f5581bad56b8fda50a6c2e86820ca5d`.

Independent Git classification at review showed:

```text
 M .agent-work/EXECUTION_RESULT.md
?? tests/test_p7_retained_r3_controller_integration.py
```

The tracked ER diff is exactly one 12-line P2 handoff append. The untracked-file
owner lists exactly the test path. The working-tree `git diff --name-only` lists
only the tracked ER path and cannot list the untracked test; before the ER append,
the same command necessarily produced the empty set reported by the Executer.

No test was invoked. The handoff freezes new-targeted/existing-owner/focused/
full/compileall/CodeGraph/postcommit-targeted counts at `0/0/0/0/0/0/0`, commit
at `0`, and retry/fallback at `0/0`. It also freezes all historical, retained,
actual-validator, eligibility, release, external-root, network and device
budgets at zero.

## 3. Planner findings

### Finding P2-GATE-001 — accepted

The failed assertion was not a test implementation failure. The PLAN required
`git diff --name-only` to equal a path that had just been created and remained
untracked. Standard Git diff traversal covers tracked index/worktree entries;
it does not enumerate an ordinary untracked path. The gate therefore required
an impossible observation at that lifecycle point.

`git diff --check` also cannot validate the content of an ordinary untracked
file. Its success did not prove that the new file was whitespace-clean. This is
the same gate-design defect, not a second implementation defect.

### Scope assessment

The source bytes have not been executed or behaviorally evaluated, so P2 cannot
be accepted. Conversely, no evidence justifies discarding, recreating or editing
the file. The narrow corrective route is to preserve its exact path/type/bytes/
hash, replace only the faulty scope observation with a deterministic
tracked-plus-untracked classification, and resume at the first targeted test.

This is an engineering/Git gate correction. No color-science question, Advisor
decision or Human device authorization is implicated.

## 4. Decision and residual risks

Decision:
`REJECTED_GATE_DEFECT_IMPLEMENTATION_NOT_EVALUATED`.

The original P2 is superseded only at its pretest path-classification step. Its
architecture, exact one-test scope, substantive behavioral requirements,
ordered validation gates after that point, exact implementation commit subject,
zero budgets and final Planner stop remain binding.

Residual risks:

1. The preserved test may still fail its first behavioral test; no current
   evidence evaluates it.
2. A path-union gate that concatenates human-readable Git output could be
   ambiguous. The correction must parse NUL-delimited porcelain/tracked and
   untracked classifications and require an exact singleton.
3. Because `git diff --check` excludes an untracked path, pretest whitespace
   validation must use a no-index check or an equivalently auditable content
   check without staging or intent-to-add.
4. The Orchestrator activation commit must preserve the test as the exact same
   untracked regular file and must not accidentally include it.

## 5. Exact next branch

The sole next package is
`REF-P7-25-R2-B2-C4-P2-C1`, contract
`P7-TD-B-RETAINED-R3-OPTION-B-B2-C4-P2-C1-PRETEST-SCOPE-GATE-CORRECTION-V1`.

It must:

- preserve the existing test at exact bytes/SHA and prohibit editing,
  recreation, staging or `git add -N` before the original commit gate;
- classify tracked and untracked paths through a NUL-safe Git owner and require
  the exact singleton untracked test with no tracked implementation diff;
- validate the untracked content without relying on ordinary `git diff --check`;
- not repeat the already-passed FULL/input/source-creation preconditions;
- continue from the first targeted test through the unchanged original ordered
  gates exactly once;
- retain the commit subject
  `test(p7): qualify retained r3 controller composition`, retry `0`, all locked
  operation budgets `0`, and stop
  `B2_C4_P2_C1_INTEGRATION_QUALIFICATION_COMPLETE_WAITING_PLANNER_REVIEW`.

P2-C1 does not authorize real B2, retained-R3 audit, canonical-validator use,
eligibility, release consumption or device/scientific work.
