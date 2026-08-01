# P7 retained-R3 Option B：M1-S1-C1-C1 CodeGraph routing failure review

**Planner review date:** `2026-08-01`

**Reviewed reference task:** `REF-P7-25-R2-B2-M1-S1-C1-C1`

**Reviewed contract:**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-M1-S1-C1-C1-CODEGRAPH-SCOPE-CORRECTION-V1`

**Decision:** `REJECTED_PRE_EDIT_CODEGRAPH_DEDICATED_TEST_ROUTING_UNRELIABLE`

**Exact next branch:** fresh `REF-P7-25-R2-B2-M1-S1-C1-C1-C1` evidence-owner correction; preserve the same one-path test07/test13 semantic correction, but assign CodeGraph only the production P3/P4/P5/M1 ownership graph and assign dedicated-test identity/semantics to exact Git blob, one-path diff, Python AST/static assertions, and the targeted/focused/full suites.

## 1. Reviewed scope and immutable topology

The reviewed activation is commit `becc092a028d6607c1dedb7c544a9d032dcf97a3`, direct child of evidence HEAD
`850537007233a1517962afbef26e8e40e4782ad2`, with subject exact
`chore(plan): activate real manifest CodeGraph scope correction`. Its changed paths are exact:

- `.agent-work/FULL_PLAN_REFERENCE.md`
- `.agent-work/PLAN.md`
- `.agent-work/PLANS/20260731-2348-p7-retained-r3-b2-m1-s1-c1-codegraph-scope-failure-review.md`

The Executer evidence commit is `af29d6f0e29fc0b5bdc8e8ff084ae9706d28aafa`, direct child of the activation, subject exact
`chore(evidence): record deterministic CodeGraph routing stop`, and changes only `.agent-work/EXECUTION_RESULT.md`.

The authoritative ER identity at that evidence HEAD is blob `643e91e13ebd71cdeec91aba368f580c68de2568`, bytes `1185329`, SHA-256
`60fbfb97f8c859d5c6d6c1c30cebf3d0fb1e0482edbfb0069b9a01d207725b84`. The Executer message omitted the final two hex characters
`84`, but the committed ER body made no after-hash claim; this is a handoff-display truncation, not an evidence-content contradiction.

The immutable rejected M1-S1 candidate remains commit `cddd23eb4ef53a8f90c9b869f96f84ccfcba36cf`, parent
`84b3458765849f9c50515067788af365006cef68`, tree `ff424f29e6a7a95349500ce356669a754d9ffa14`, and `consumable=false`.
Its exact two paths and identities remain:

| Path | Git blob | Bytes | SHA-256 |
| --- | --- | ---: | --- |
| `src/camera_based_rgbww_optimizer/utils/p7_retained_r3_real_manifest_domain_template.py` | `84fcd755225af39eb89459146de282392367b70b` | `23352` | `5a593fee05eb09e0a3c10d30661e480823baef2876446c25b9fd42e46d70c29d` |
| `tests/test_p7_retained_r3_real_manifest_domain_template.py` | `05db407f9fd6c67bf359f1874cff2f9baaf9564f` | `17413` | `cee73ccb729ad220f0dad76b54e91fa9c5b73904a262d897bf7b11a284fda4af` |

## 2. Execution evidence and validation quality

The activation/topology/archive/machine-row gates passed. The pre-edit CodeGraph sync ran once and exited `0`.

Query group 1, scoped to the M1 production builder, exited `0` and returned the required production file and three required symbols; its semantic coverage was exact `4/4`.

Query group 2, scoped to the dedicated test, also exited `0` but returned line-numbered source blocks only for unrelated tests. The requested dedicated-test path, class, test07, and test13 appeared only in the echoed request header and not in returned source; semantic coverage was therefore exact `0/4`. This is the second consecutive package in which CodeGraph could not reliably return the dedicated-test source surface.

The Executer obeyed fail-fast semantics. Query groups 3–5 were not issued. Pre-edit CodeGraph totals were sync/query `1/2`, groups passed `1/2`, invoked semantic coverage `4/8`; post-edit CodeGraph was `0/0`. Dedicated-test reads/edits outside the query were `0/0`; production/test writes, targeted/focused/full/postcommit tests, compileall, diff/stage/correction commit were all `0`. Retry/fallback were exact `0/0`.

No retained-R3 artifact, external controller/root, canonical validator, release, network, device, camera, Ray, strip, cleanup, capture, FORMAL, public analyzer, TD-C, sentinel, P8, firmware, or deployment route was entered. Retained R3 remains `RETAINED_UNVALIDATED_UNCONSUMED`.

Validation quality is sufficient to reject this evidence contract and insufficient to accept or reject the one-path semantic correction, because no test edit or test invocation occurred. It is also sufficient to conclude that adding narrower, more numerous, or generic-scanner CodeGraph queries for the dedicated test would repeat an unreliable evidence-owner assignment rather than validate the implementation.

## 3. Planner findings

1. `REV-M1-S1-C1-C1-001` — **accepted finding:** CodeGraph is not a reliable owner for exact dedicated-test source/semantic evidence in this route. Two consecutive pre-edit packages produced wrong-route dedicated-test results despite increasingly exact query wording.
2. `REV-M1-S1-C1-C1-002` — **no production finding established:** the only completed production group passed `4/4`; P3/P4/P5 groups were correctly skipped after fail-fast. No source was edited, so there is no basis for changing production ownership or the frozen M1 candidate.
3. `REV-M1-S1-C1-C1-003` — **handoff truncation only:** the authoritative committed ER identity is bytes `1185329`, SHA-256 ending `...725b84`; the shortened message does not alter committed evidence.
4. `REV-M1-S1-C1-C1-004` — **original correction retained:** test07 must still copy the first complete identity and replace only its label with the second expected label before asserting `path_collision`; test13 must still replace raw generated-source substring scanning with exact Python AST import/call-token assertions.

## 4. Successor evidence-owner allocation

The successor must not add finer or more CodeGraph queries and must not introduce a generic scanner. It uses exact one production-only query before and after the correction. That query may establish only the P3/P4/P5/M1 production call graph and ownership boundaries: P3 physical provenance I/O, P4 static/effect provenance and lifecycle validation, P5 runtime composition, and M1 immutable domain-template composition.

The dedicated test is instead proven by:

- current Git blob identity `05db407f9fd6c67bf359f1874cff2f9baaf9564f` and frozen bytes/SHA-256;
- a deterministic pre-edit Python AST/static gate proving exactly 13 methods and the two known defective shapes;
- an unstaged and committed diff limited to the exact one dedicated-test path and the existing test07/test13 methods;
- a deterministic post-edit Python AST/static gate proving the exact collision fixture and exact generated-source import/call-token authority assertions, with no raw substring negative;
- targeted `13/13`, focused `83/83`, compileall exit `0`, full `800/800`, and postcommit targeted `13/13`.

Production source identities remain frozen throughout:

| Owner | Git blob | Bytes | SHA-256 |
| --- | --- | ---: | --- |
| M1 | `84fcd755225af39eb89459146de282392367b70b` | `23352` | `5a593fee05eb09e0a3c10d30661e480823baef2876446c25b9fd42e46d70c29d` |
| P3 | `d6d6cc628861baf8a95a09f13fa9204989693b5b` | `19767` | `118f8bdd086f3180088c99681e4dfbdfff05613c844a21bd83f3c1dd53c31a3d` |
| P4 | `07f89d15c8288e0d45c495d6d5737bc37427b769` | `30424` | `008d0aac24db8746b4ef7241e0f46091c5854d3a845aa88ceb020dcb64f362ee` |
| P5 | `075face6fd7453236affa303640b91eb16a42a9b` | `12320` | `07eaeac615ea79db45afad91ce4c82e28c1cdcb66b6119b5cdca6462d7c091d2` |

## 5. Decision, residual risks, and stop point

Decision is to reject only the current CodeGraph evidence contract and issue the bounded evidence-owner successor. The rejected M1 candidate remains non-consumable. Passing the successor produces only a waiting-review one-path correction candidate; it does not accept the owner or unlock M1-I1.

Residual risk is limited to whether the original test07/test13 corrections satisfy the frozen suites and static gates. If the production-only CodeGraph query cannot establish the four production ownership boundaries, or any Git/AST/test gate fails, the Executer must stop without modifying the contract or retrying. There is no scientific ambiguity and no Human authorization requirement.

Locked after this review: M1-I1, retained-R3 reads/audit, canonical validator, eligibility, release generation/qualification/copy/consumption, network, devices, camera, Ray, strip, cleanup, capture, FORMAL-R6, public analyzer, TD-C, sentinel, P8, firmware, and deployment.

**Next Planner stop:** `B2_M1_S1_C1_C1_C1_EVIDENCE_OWNER_CORRECTION_WAITING_PLANNER_REVIEW`.
