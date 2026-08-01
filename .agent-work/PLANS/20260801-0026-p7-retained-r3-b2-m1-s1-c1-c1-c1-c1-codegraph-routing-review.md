# P7 retained-R3 Option B：M1-S1-C1-C1-C1-C1 CodeGraph routing review

**Planner review date:** `2026-08-01`

**Reviewed reference task:** `REF-P7-25-R2-B2-M1-S1-C1-C1-C1-C1`

**Reviewed contract:**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-M1-S1-C1-C1-C1-C1-EXACT-DIFF-CORRECTION-V1`

**Decision:** `REJECTED_PRE_EDIT_CODEGRAPH_PRODUCTION_OWNERSHIP_MISMATCH`

**Exact next branch:** fresh `REF-P7-25-R2-B2-M1-S1-C1-C1-C1-C1-C1` CodeGraph-free exact-diff correction. Preserve the frozen one-path test07/test13 correction, remove every CodeGraph explore/query budget and semantic coverage assertion, and retain exactly one post-test `codegraph sync` only to satisfy the repository changed-project maintenance rule. That sync is not a semantic owner or acceptance oracle; nonzero still stops before commit.

## 1. Reviewed scope and immutable topology

The reviewed activation is commit `3c46c3531766576d9f6d7172d12add911f934537`, direct child of evidence HEAD
`aae2e5c8d1c87f0f12955d049b7c3c581774680c`, tree `4e53a5a589576a41342ab05bc2d68df5373a302a`, with subject exact
`chore(plan): activate real manifest exact diff correction`. Its changed paths are exact:

- `.agent-work/FULL_PLAN_REFERENCE.md`
- `.agent-work/PLAN.md`
- `.agent-work/PLANS/20260801-0014-p7-retained-r3-b2-m1-s1-c1-c1-c1-ast-gate-failure-review.md`

The Executer evidence commit is `540568c84d266c115f2a4fcdf9078fccc4956279`, direct child of that activation, subject exact
`chore(evidence): record production CodeGraph routing stop`, tree `759b1be75fdaa1fb989fd46fad91308b5218438c`, and changes only
`.agent-work/EXECUTION_RESULT.md`.

The authoritative ER identity at the evidence HEAD is blob `ea2e26ac24649e284c6e76bc01ebc64a3cc29b57`, bytes `1195508`, SHA-256
`da00b05efcf259f717efdd5a5f9dcdf0df23a0250349da92c9a0ae77940e7966`. Its immutable prefix before the single append was blob
`6554db5ebc1e2f8e884c8f3ddeca46165142e730`, bytes `1190081`, SHA-256
`05e7ddfc2b3bc4f9e4e3db195d5cf9bbc5149c28432a289c98f97af5e6923b1d`.

The reviewed PLAN identity is blob `4cb882790a442c05e28baf02467224a80eff58d2`, bytes `19103`, SHA-256
`6d81209bed34831f65f0f8fc7b84492693111cacbfbd734f422dfd13f546de4b`. Its predecessor archive
`.agent-work/PLANS/20260801-0014-p7-retained-r3-b2-m1-s1-c1-c1-c1-ast-gate-failure-review.md` remains bytes `9009`, SHA-256
`f0c2f77b4b3c4254138df17a8216285175dad8d044eb601d2ed29ae35db3b7eb`.

The immutable rejected M1-S1 candidate remains commit `cddd23eb4ef53a8f90c9b869f96f84ccfcba36cf`, parent
`84b3458765849f9c50515067788af365006cef68`, tree `ff424f29e6a7a95349500ce356669a754d9ffa14`, and `consumable=false`.
Its exact two paths and identities remain:

| Path | Git blob | Bytes | SHA-256 |
| --- | --- | ---: | --- |
| `src/camera_based_rgbww_optimizer/utils/p7_retained_r3_real_manifest_domain_template.py` | `84fcd755225af39eb89459146de282392367b70b` | `23352` | `5a593fee05eb09e0a3c10d30661e480823baef2876446c25b9fd42e46d70c29d` |
| `tests/test_p7_retained_r3_real_manifest_domain_template.py` | `05db407f9fd6c67bf359f1874cff2f9baaf9564f` | `17413` | `cee73ccb729ad220f0dad76b54e91fa9c5b73904a262d897bf7b11a284fda4af` |

The other frozen production owners are P3 blob `d6d6cc628861baf8a95a09f13fa9204989693b5b`, bytes `19767`, SHA-256
`118f8bdd086f3180088c99681e4dfbdfff05613c844a21bd83f3c1dd53c31a3d`; P4 blob
`07f89d15c8288e0d45c495d6d5737bc37427b769`, bytes `30424`, SHA-256
`008d0aac24db8746b4ef7241e0f46091c5854d3a845aa88ceb020dcb64f362ee`; and P5 blob
`075face6fd7453236affa303640b91eb16a42a9b`, bytes `12320`, SHA-256
`07eaeac615ea79db45afad91ce4c82e28c1cdcb66b6119b5cdca6462d7c091d2`.

## 2. Execution evidence and validation quality

Activation, topology, archive, machine-row, candidate, and all five frozen Git object identity gates passed. Pre-edit `codegraph sync` then ran exact once, exited `0`, and reported `Already up to date`. The sole permitted production-only query also ran exact once and exited `0`, but its authoritative output reported `Found 50 symbols across 2 files` and supplied source coverage only for P3 and P4. It did not supply M1 or P5, so the required production-file coverage was `2/4`; correspondingly only the P3 physical provenance-I/O and P4 static/effect/lifecycle boundaries were supported, while P5 runtime composition and M1 immutable template composition were missing.

The first failure was exact `pre_edit_codegraph_production_ownership_mismatch`. Fail-fast was respected: there was no second or modified query, no source read/edit after the mismatch, no dedicated-test query, no fallback, no ad-hoc AST/static gate, no helper/scanner, no test, no compile, no diff/stage, and no correction commit.

Exact stopped ledger:

- pre-edit CodeGraph sync/query: `1/1`; post-edit sync/query: `0/0`;
- CodeGraph authoritative production-file coverage: `2/4`; full four-boundary proof incomplete;
- dedicated-test/finer/additional CodeGraph query: `0/0/0`;
- ad-hoc AST/static gates and evidence helper/scanner: `0/0`;
- targeted/focused/full/postcommit tests: `0/0/0/0`; compileall `0`;
- test/production writes, diff, stage, correction commit: all `0`;
- retry/fallback: `0/0`; ER append: `1`.

No retained-R3 artifact, external controller/root, canonical validator, release, network, device, camera, Ray, strip, cleanup, capture, FORMAL, public analyzer, TD-C, sentinel, P8, firmware, or deployment route was entered. Retained R3 remains `RETAINED_UNVALIDATED_UNCONSUMED`.

Validation quality is sufficient to reject this CodeGraph semantic prerequisite and insufficient to accept or reject the intended test07/test13 correction, because no edit or test occurred. The wrong-route output is not evidence of a production defect or an ownership-boundary defect.

## 3. Planner findings

1. `REV-M1-S1-C1-C1-C1-C1-001` — **accepted finding:** the fixed production-only query cannot reliably route all four requested production owners. Exit `0` plus a request header is not evidence for missing M1/P5 source coverage.
2. `REV-M1-S1-C1-C1-C1-C1-002` — **systemic evidence finding:** CodeGraph has now wrong-routed this correction three times: twice for dedicated-test source and once for production scope. Keeping another explore/query as a semantic hard gate would continue blocking a bounded test-only correction without improving product evidence.
3. `REV-M1-S1-C1-C1-C1-C1-003` — **no implementation finding:** edit/tests/commit were all zero. P3/P4/P5/M1 production identities remain frozen, and candidate `cddd23e...` remains non-consumable.
4. `REV-M1-S1-C1-C1-C1-C1-004` — **original correction retained:** test07 still must clone the first complete identity and replace only its label with the second expected label before asserting `path_collision`; test13 still must replace raw whole-source substring scanning with its own runtime AST exact import/alias/call-token assertions.

## 4. Simplified successor evidence contract

The successor removes all CodeGraph explore/query invocations, budgets, coverage counts, and semantic assertions. It must not add a replacement scanner, helper, static gate, AST harness, source-shape program, or generic search fallback.

Before edit, the five production/test identities are owned only by their frozen Git blob/bytes/SHA-256 values. Any mismatch stops with writes/tests zero. Production paths are read-only and have write budget zero. The Executer may directly read the PLAN-frozen test07/test13 and apply the exact correction to the one dedicated test path.

After edit, semantic evidence is owned by:

- the exact human-readable Git diff restricted to the one dedicated test path and the existing test07/test13 methods;
- test07's runtime `path_collision` assertion over a first-identity/second-label collision;
- test13's in-test `ast.parse` exact qualified import/module/alias/call-token authority-negative assertions, without the raw whole-source lowercase substring predicate;
- targeted `13/13`, focused `83/83`, compileall exit `0`, full `800/800`, and postcommit targeted `13/13`;
- the correction commit's exact parent/path/subject, test after blob/bytes/SHA-256, canonical binary patch SHA-256, and Planner's independent committed-diff review.

Only after the one-path edit plus targeted, focused, compileall, and full validation pass, run exact one `codegraph sync` because this repository has `.codegraph/` and the project rules require sync after a changed project. It has no accompanying query and is not a semantic gate or ownership oracle. A nonzero sync still stops before staging/commit because the repository-required maintenance action failed.

No new test method, helper, scanner, production abstraction, alternate evidence owner, retry, or fallback is permitted.

## 5. Decision, residual risks, and stop point

Decision is to reject only the unreliable CodeGraph semantic prerequisite and issue the CodeGraph-free exact-diff successor. Passing the successor creates a waiting-review one-path correction candidate; it does not accept the real-manifest owner, consume the rejected M1 candidate, or unlock M1-I1.

Residual risk is limited to whether the two frozen fixture corrections satisfy the existing runtime and regression suites, whether the exact diff stays inside those two methods, and whether the single required post-test CodeGraph sync exits successfully. A Git identity mismatch, blast-radius mismatch, test/count failure, sync nonzero, commit mismatch, or unexpected product behavior stops with retry zero.

There is no scientific ambiguity and no Human authorization requirement. Locked after this review: M1-I1, retained-R3 reads/audit, canonical validator, eligibility, release generation/qualification/copy/consumption, network, devices, camera, Ray, strip, cleanup, capture, FORMAL-R6, public analyzer, TD-C, sentinel, P8, firmware, and deployment.

**Next Planner stop:** `B2_M1_S1_C1_C1_C1_C1_C1_CODEGRAPH_FREE_CORRECTION_WAITING_PLANNER_REVIEW`.
