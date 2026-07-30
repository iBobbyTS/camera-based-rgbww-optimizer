# REF-P7-25-R2-B2-C4-P2-C1 gate-owner parser failure review

**Review date:** `2026-07-30`

**Reviewed reference task:** `REF-P7-25-R2-B2-C4-P2-C1`

**Reviewed contract:**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-C4-P2-C1-PRETEST-SCOPE-GATE-CORRECTION-V1`

**Planner decision:**
`REJECTED_EXECUTION_GATE_OWNER_PARSER_DEFECT_IMPLEMENTATION_NOT_EVALUATED`

**Reviewed PLAN identity:** bytes `13664`, SHA-256
`91165b72d928f422c1efb98f326b232942b59c096b92b7f8f87ec874829fc537`.

**Reviewed stop:**
`B2_C4_P2_C1_INTEGRATION_QUALIFICATION_COMPLETE_WAITING_PLANNER_REVIEW`.

## 1. Reviewed scope and intended method

P2-C1 preserved the existing untracked integration test and authorized one
corrected pretest scope gate. The intended gate was to prove the exact frozen
file identity, classify tracked and untracked paths with NUL-delimited Git
output, validate the new file with a no-index whitespace check, and then resume
the original P2 ordered validation sequence at its first targeted test.

The package prohibited test edits, recreation, staging before the original
commit gate, intent-to-add, retry, production changes, real retained-R3 reads,
the actual canonical validator, eligibility, release, network, device and
scientific-stage work.

## 2. Evidence independently reviewed

The final handoff in `.agent-work/EXECUTION_RESULT.md` had worktree identity at
review of bytes `961094`, SHA-256
`ac830b238a6095288046b551a01839141f883904c6f2345304dd8d992f9a52b9`.
The tracked delta is exactly the twelve-line P2-C1 handoff append.

The activation topology independently observed at review was:

- HEAD: `c521447e9cefe51c1263565a3d8c1bba3e1aaaf3`;
- direct parent: `e45cf6a70204d87a5b4b47f19149e80e087cb634`;
- subject: `chore(plan): activate retained r3 pretest gate correction`.

The frozen implementation remained:

- path: `tests/test_p7_retained_r3_controller_integration.py`;
- lstat type: regular file;
- Git class: untracked;
- bytes: `13147`;
- SHA-256:
  `106ddcafddbc31d8172b3f6a3a2557830f5581bad56b8fda50a6c2e86820ca5d`.

The observed worktree had only the tracked execution-result append and this
untracked test. No production or existing-test source changed.

The handoff reports one corrected-gate invocation. HEAD, direct-parent and
subject checks passed. The gate then searched for a raw line beginning exactly
`PLAN_MACHINE_CONTRACT=`. The Markdown source represents that row inside
backticks, so the generator expression had no candidate and raised Python
`StopIteration`. Formal lstat, porcelain/status parsing, tracked/cached/
untracked union classification and the no-index whitespace check were not
reached.

Targeted, owner, focused, full, compileall, CodeGraph, postvalidation scope,
staging, commit and postcommit targeted counts are all `0`; no-index check is
`0`; retry/fallback and implementation commit are `0/0` and `0`. All retained,
validator, eligibility, release, external-root, network and device budgets
remain zero.

No test command was run during this review. The frozen test was not read for
behavior, edited, recreated, staged or otherwise mutated.

## 3. Planner findings

### Finding P2-C1-GATE-001 — accepted

This is an execution gate-owner parser defect. It is not evidence of a defect
in the integration test or either production owner. The gate failed before the
first substantive validation command, so implementation behavior remains
unevaluated.

The parser was also unnecessary. Orchestrator owns activation and independently
validates the active PLAN/FULL state before creating an exact activation
commit. Requiring Executer to rediscover authorization by parsing Markdown
machine rows creates a second, representation-sensitive owner without adding a
meaningful provenance boundary.

### Maintainability finding

Another correction to the Markdown parser would continue the same fragile
pattern. The smallest maintainable correction removes Executer-side PLAN/FULL
machine-row parsing entirely. Executer should prove only the immutable Git
activation topology and the frozen implementation/Git scope that it actually
consumes.

This is an engineering execution-gate decision. It does not require Advisor
scientific guidance or Human device authorization.

## 4. Decision and residual risks

Decision:
`REJECTED_EXECUTION_GATE_OWNER_PARSER_DEFECT_IMPLEMENTATION_NOT_EVALUATED`.

Residual risks:

1. The frozen integration test has still never run and may fail its first
   targeted invocation. No speculative edit is authorized.
2. Activation must preserve the exact untracked file while committing only
   planning/evidence metadata.
3. The NUL-safe status/union/no-index gate remains necessary; removing Markdown
   parsing must not weaken the actual file and Git-scope proof.
4. All original post-gate validation, staging, commit, postcommit and zero-budget
   requirements remain untested and binding.

## 5. Exact next branch

The sole next package is `REF-P7-25-R2-B2-C4-P2-C2`, contract
`P7-TD-B-RETAINED-R3-OPTION-B-B2-C4-P2-C2-PARSER-FREE-PRETEST-GATE-V1`.

It must:

- let Orchestrator independently validate and activate the exact PLAN state;
- require Executer exactly once to verify only activation HEAD/direct-parent/
  subject topology, frozen-test lstat/bytes/SHA, NUL-safe status and
  tracked/cached/untracked union, plus the no-index whitespace check;
- contain no Executer parsing or semantic reconstruction of PLAN/FULL machine
  rows and no rerun of superseded preconditions;
- preserve the frozen test byte-for-byte with edit/recreate/delete/formatter
  and precommit-stage budgets zero;
- resume at the original first targeted test after the corrected gate;
- retain every later ordered gate, the exact implementation commit subject,
  retry `0`, all locked-operation budgets `0`, and one Planner stop.

P2-C2 does not authorize real B2, retained-R3 audit, canonical-validator use,
eligibility, release consumption or device/scientific work.
