# P7 retained-R3 Option B：M1-S1-C1-C1-C1 AST gate failure review

**Planner review date:** `2026-08-01`

**Reviewed reference task:** `REF-P7-25-R2-B2-M1-S1-C1-C1-C1`

**Reviewed contract:**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-M1-S1-C1-C1-C1-EVIDENCE-OWNER-CORRECTION-V1`

**Decision:** `REJECTED_EVIDENCE_HARNESS_SELF_BLOCKING`

**Exact next branch:** fresh `REF-P7-25-R2-B2-M1-S1-C1-C1-C1-C1` exact-diff correction. Preserve the frozen one-path test07/test13 semantic correction, but remove all ad-hoc AST/static gate/helper/scanner ownership. Before identity is owned only by the frozen Git blob/bytes/SHA-256; after semantics are owned by the exact diff limited to test07/test13, the existing dedicated-test runtime assertions, targeted/focused/full validation, postcommit blob/patch identity, and Planner's independent diff review.

## 1. Reviewed scope and immutable topology

The reviewed activation is commit `d00ba803058eb083c180c84c8a5f7267dccb4311`, direct child of evidence HEAD
`af29d6f0e29fc0b5bdc8e8ff084ae9706d28aafa`, with subject exact
`chore(plan): activate real manifest evidence owner correction`. Its changed paths are exact:

- `.agent-work/FULL_PLAN_REFERENCE.md`
- `.agent-work/PLAN.md`
- `.agent-work/PLANS/20260801-0000-p7-retained-r3-b2-m1-s1-c1-c1-codegraph-routing-review.md`

The Executer evidence commit is `aae2e5c8d1c87f0f12955d049b7c3c581774680c`, direct child of that activation, subject exact
`chore(evidence): record real manifest AST gate stop`, tree `a072fe57955cc5abc8ce5061b0e5d6c8ea3e2417`, and changes only
`.agent-work/EXECUTION_RESULT.md`.

The authoritative ER identity at the evidence HEAD is blob `6554db5ebc1e2f8e884c8f3ddeca46165142e730`, bytes `1190081`, SHA-256
`05e7ddfc2b3bc4f9e4e3db195d5cf9bbc5149c28432a289c98f97af5e6923b1d`. Its immutable prefix before the single append was blob
`643e91e13ebd71cdeec91aba368f580c68de2568`, bytes `1185329`, SHA-256
`60fbfb97f8c859d5c6d6c1c30cebf3d0fb1e0482edbfb0069b9a01d207725b84`.

The reviewed PLAN identity is bytes `17629`, SHA-256
`8c70a862c8e022bb3883b9defffd8f4fffb6d746b1991963fe5cd540f73da9a6`. Its predecessor archive
`.agent-work/PLANS/20260801-0000-p7-retained-r3-b2-m1-s1-c1-c1-codegraph-routing-review.md` remains bytes `8412`, SHA-256
`3b4ecd888ca81a38acede732e9396e7c1744828513c05e39522f39bb190bd047`.

The immutable rejected M1-S1 candidate remains commit `cddd23eb4ef53a8f90c9b869f96f84ccfcba36cf`, parent
`84b3458765849f9c50515067788af365006cef68`, tree `ff424f29e6a7a95349500ce356669a754d9ffa14`, and `consumable=false`.
Its exact two paths and identities remain:

| Path | Git blob | Bytes | SHA-256 |
| --- | --- | ---: | --- |
| `src/camera_based_rgbww_optimizer/utils/p7_retained_r3_real_manifest_domain_template.py` | `84fcd755225af39eb89459146de282392367b70b` | `23352` | `5a593fee05eb09e0a3c10d30661e480823baef2876446c25b9fd42e46d70c29d` |
| `tests/test_p7_retained_r3_real_manifest_domain_template.py` | `05db407f9fd6c67bf359f1874cff2f9baaf9564f` | `17413` | `cee73ccb729ad220f0dad76b54e91fa9c5b73904a262d897bf7b11a284fda4af` |

## 2. Execution evidence and validation quality

The activation, topology, archive, machine-row, candidate, and frozen production/test identity gates passed. The sole permitted pre-edit Python AST/static gate then exited `1` with a bare `AssertionError` at inline script line `39` and emitted no completed finding object.

Because the gate did not identify which assertion failed, none of its intended subclaims are promoted: method inventory, test07 before shape, test13 before shape, and the other eleven methods' AST freeze are all unproven by this invocation. Per fail-fast, the Executer did not rerun or modify the gate, use a fallback scanner, inspect raw source, start CodeGraph, edit a file, run a test, compile, stage, or create a correction commit.

Exact stopped ledger:

- ad-hoc Git/AST gates invoked/passed: `1/0`; second gate `0`;
- pre/post CodeGraph sync/query: `0/0` and `0/0`;
- targeted/focused/full/postcommit tests: `0/0/0/0`; compileall `0`;
- edits/diff/stage/correction commit: `0/0/0/0`;
- retry/fallback: `0/0`;
- ER append: `1`.

No retained-R3 artifact, external controller/root, canonical validator, release, network, device, camera, Ray, strip, cleanup, capture, FORMAL, public analyzer, TD-C, sentinel, P8, firmware, or deployment route was entered. Retained R3 remains `RETAINED_UNVALIDATED_UNCONSUMED`.

Validation quality is sufficient to reject the evidence harness and insufficient to accept or reject the intended test07/test13 correction, because the correction was never made and no relevant test ran. The bare assertion does not establish a product defect, production ownership defect, or dedicated-test defect beyond the already frozen two fixture findings from the original targeted run.

## 3. Planner findings

1. `REV-M1-S1-C1-C1-C1-001` — **accepted finding:** the inline AST/static gate is opaque and self-blocking. A bare line-number assertion without atomic findings cannot support a Planner acceptance decision.
2. `REV-M1-S1-C1-C1-C1-002` — **systemic evidence finding:** three consecutive corrective packages have stopped before the intended edit because of self-authored evidence routing or harness behavior: two CodeGraph test-source wrong routes followed by this opaque AST gate. Adding or correcting another inline helper, scanner, AST script, or assertion protocol would extend the verification framework rather than advance the bounded correction.
3. `REV-M1-S1-C1-C1-C1-003` — **no implementation finding:** code/test edits and tests were all zero. P3/P4/P5/M1 production ownership remains frozen, and the rejected candidate remains non-consumable.
4. `REV-M1-S1-C1-C1-C1-004` — **original correction retained:** test07 must still copy the first complete identity and replace only its label with the second expected label before asserting `path_collision`; test13 must still replace raw generated-source substring scanning with its own exact runtime AST import/alias/call-token assertions.

## 4. Simplified successor evidence contract

The successor must not add, repair, or invoke an inline AST/static gate, helper, scanner, source-shape script, or generic search fallback. It also must not query tests through CodeGraph.

Before-edit dedicated-test identity is owned solely by the frozen Git object at activation HEAD:

- path exact `tests/test_p7_retained_r3_real_manifest_domain_template.py`;
- blob `05db407f9fd6c67bf359f1874cff2f9baaf9564f`;
- bytes `17413`;
- SHA-256 `cee73ccb729ad220f0dad76b54e91fa9c5b73904a262d897bf7b11a284fda4af`.

The Executer may directly read the two PLAN-frozen methods and apply the exact one-path correction. It need not first re-prove their old syntax through an auxiliary program. Production-only CodeGraph remains one exact pre-edit and one exact post-edit query, each following one sync, and owns only the P3/P4/P5/M1 call graph and four ownership boundaries. Test source is neither required nor accepted as CodeGraph evidence.

After-edit semantics are jointly owned by:

- an exact unstaged/staged/committed diff whose only path is the dedicated test and whose only changed methods are existing test07 and test13;
- test07's existing runtime assertion reaching stable `path_collision` from a first-identity/second-label collision;
- test13's in-test `ast.parse` and exact qualified import/alias/call-token assertions, with the raw lowercase substring assertion removed;
- targeted `13/13`, focused `83/83`, compileall exit `0`, full `800/800`, and postcommit targeted `13/13`;
- the correction commit's exact parent/path/subject, test after blob/bytes/SHA-256, and canonical binary patch SHA-256;
- Planner's independent review of the exact committed diff before owner acceptance.

No new test method, helper, scanner, or production abstraction is permitted. Retry remains zero.

## 5. Decision, residual risks, and stop point

Decision is to reject only the current self-blocking evidence harness and issue the simplified exact-diff successor. Passing the successor produces a waiting-review one-path correction candidate; it does not accept the real-manifest owner, consume the rejected M1 candidate, or unlock M1-I1.

Residual risk is limited to whether the two frozen fixture corrections pass the existing test surface and whether the production-only CodeGraph query proves all four production boundaries. A Git identity mismatch, real production finding, query ownership mismatch, test failure, count mismatch, blast-radius mismatch, or commit mismatch must stop without retry or evidence-harness repair.

There is no scientific ambiguity and no Human authorization requirement. Locked after this review: M1-I1, retained-R3 reads/audit, canonical validator, eligibility, release generation/qualification/copy/consumption, network, devices, camera, Ray, strip, cleanup, capture, FORMAL-R6, public analyzer, TD-C, sentinel, P8, firmware, and deployment.

**Next Planner stop:** `B2_M1_S1_C1_C1_C1_C1_EXACT_DIFF_CORRECTION_WAITING_PLANNER_REVIEW`.
