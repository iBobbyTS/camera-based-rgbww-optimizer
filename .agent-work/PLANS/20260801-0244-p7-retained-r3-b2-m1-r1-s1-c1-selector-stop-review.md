# REF-P7-25-R2-B2-M1-R1-S1-C1 pre-append selector-stop review

**Reviewed reference task:** `REF-P7-25-R2-B2-M1-R1-S1-C1`

**Reviewed contract:**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-M1-R1-S1-C1-GIT-ER-ONLY-TERMINAL-ASSERTION-SUPERSESSION-V1`

**Planner decision:** `REJECTED_PRE_APPEND_NON_CONTRACTUAL_OLD_PLANNER_STOP_SELECTOR`

**Planner review date:** `2026-08-01`

## Reviewed immutable repository scope

- Activation is `7dceb396ebafe1ee38ca14411851fc7bc27a34c6`, direct parent
  `5d4e903b0d747be169d68032066b023d77f3a8f9`, exact subject
  `chore(plan): supersede strict retained terminal assertion`, and exact changed paths are FULL, PLAN, and
  `.agent-work/PLANS/20260801-0236-p7-retained-r3-b2-m1-r1-s1-terminal-link-review.md`.
- The activation's committed ER is unchanged at blob `4ebbaef274da8ed2f90ae071f55e92cc2e178000`, bytes `1243874`,
  SHA-256 `64274bd4a8c1f493914d18320488d9d1ff87b070d0ececa22465ca13688ca5dd`.
- The worktree was independently clean when Planner began this review. No S1-C1 ER append or evidence commit exists.
- Planner read only repository Git objects and the committed ER. External evidence, tests, CodeGraph, controller,
  validator, release, network and devices were not accessed.

## Result classification

The Executer reported that all twelve allowed Git invocations were consumed and the twelfth gate rejected a
self-authored exact old `planner_stop` selector. The package therefore stopped before its only permitted ER append;
retry and fallback remained zero. Because the package wrote no ER row, the exact invocation counter is an
Orchestrator/Executer handoff fact rather than committed canonical evidence. Git independently proves the stronger
repository boundary needed here: activation remains HEAD, ER is byte-identical to the activation object, and the
worktree is clean.

The rejected selector was not part of the active machine contract. The authoritative S1 JSON block in committed ER
stores `planner_stop` as `B2_M1_R1_S1_FRESH_REAL_INPUT_STRICT_RETAINED_WAITING_PLANNER_REVIEW`; the stopped S1-C1
gate instead expected a different invented old string. This mismatch does not reopen C1, production, tests, the
controller, or the retained inputs. It is a package-local execution-selector defect.

The earlier S1 scientific and physical disposition is unchanged: its complete seven-row input identity ledger and
strict-decode boundary remain failure evidence only; builder/runtime/output/eligibility/release credit remains zero.
The failed fresh S1 namespace remains immutable and non-consumable.

## Accepted and rejected claims

Accepted:

- the S1 failure classification remains `NON_CONTRACTUAL_EXECUTION_SELECTOR_MISMATCH`;
- accepted C1 evidence is not reopened;
- activation and ER committed identities above are exact;
- no S1-C1 append or evidence commit occurred.

Rejected:

- S1-C1 did not emit its supersession record and is not complete;
- no exact old narrative/ER `planner_stop` string is a successor eligibility gate;
- no production, test, runner, C1, retained, validator or release defect is established.

## Exact next branch

- Reference task: `REF-P7-25-R2-B2-M1-R1-S1-C1-C1`.
- Contract:
  `P7-TD-B-RETAINED-R3-OPTION-B-B2-M1-R1-S1-C1-C1-GIT-ER-ONLY-SELECTOR-FREE-SUPERSESSION-V1`.
- Single action: validate exact committed topology and facts within a maximum Git-read budget, then append exactly one
  canonical terminal payload whether the validation path succeeds or fails.
- Old record `planner_stop` values are data, never gate selectors. Only the active PLAN machine-contract stop may be
  checked as authorization state.
- Planner stop: `B2_M1_R1_S1_C1_C1_GIT_ER_ONLY_SELECTOR_FREE_SUPERSESSION_WAITING_PLANNER_REVIEW`.

## Residual locks and maintainability

No external path operation, code/test change, test or CodeGraph invocation, controller, validator, release, network,
device, camera, Ray, strip, cleanup, capture, FORMAL, analyzer, TD-C, sentinel or P8 action is unlocked.

维护性判断：successor删除一次性旧字符串selector，并复用现有Git/ER append边界；不新增scanner、harness、parser、helper或平行evidence owner，
无需架构重构。
