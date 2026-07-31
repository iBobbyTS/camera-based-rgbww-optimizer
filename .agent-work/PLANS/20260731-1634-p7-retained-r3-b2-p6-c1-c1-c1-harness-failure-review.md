# REF-P7-25-R2-B2-P6-C1-C1-C1 Planner review：regression-green candidate / validation-harness failure

**审核日期：** 2026-07-31

**Reviewed reference task：** `REF-P7-25-R2-B2-P6-C1-C1-C1`

**Reviewed contract：**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-P6-C1-C1-C1-EXACT-GENERATED-GUARD-CALL-ALLOWLIST-CORRECTION-V1`

**Reviewed PLAN SHA-256：**
`85e9e09d7cd7eec7362429af5ce5c77008375e063fc953e896780f34b47873a0`

**Planner decision：**
`REJECTED_POST_FULL_VALIDATION_HARNESS_STOPITERATION_CANDIDATE_REGRESSION_GREEN_NON_CONSUMABLE`

## 1. Reviewed scope and immutable lineage

Activation commit is exact `478d8c52e4a21d6628219e27b88b507d736f3aca`, direct parent
`0b704f535f3653429f527abec99f54c4c48d798a`, subject
`chore(plan): activate p6 c1 c1 c1 generated call correction`, changed paths exact:

- `.agent-work/FULL_PLAN_REFERENCE.md`
- `.agent-work/PLAN.md`
- `.agent-work/PLANS/20260731-1622-p7-retained-r3-b2-p6-c1-c1-generated-call-review.md`

The preserved candidate is commit `48b3979d6c0df5f488cd500597e26dc4c38877dd`, direct parent the activation commit,
subject `chore(p7): retain rejected p6 c1 c1 c1 guard candidate`, changed path exact
`tests/test_p7_retained_r3_controller_domain_template.py`. Its diff against activation is exact `2` insertions / `2`
deletions in that one path, adding only literal allowlist names `RuntimeError` and `type`; canonical binary-diff SHA-256 is
`96a38decb6664fec7f5744f568ddad86b7c206d969452a458ddff854881da781`.

Evidence commit is exact `2fc509b02fd8be0fee05653e5875709f0d05a141`, direct parent the candidate commit, subject
`chore(evidence): record p6 c1 c1 c1 gate failure`, changed path exact `.agent-work/EXECUTION_RESULT.md`.
Review began at that exact clean HEAD.

## 2. Validation quality and result

The Executer recorded one fresh ordered regression sequence with retry/fallback `0/0`:

- targeted domain-template suite: exact `8/8`, exit `0`, `OK`;
- focused six-module suite: exact `90/90`, exit `0`, `OK`;
- exact compileall: exit `0`;
- unique full-suite session `35090`: exact `775/775`, exit `0`, `OK`;
- CodeGraph sync: one invocation, exit `0`, `Already up to date`;
- CodeGraph query: one invocation, exit `0`, no second production effect/lifecycle/analyzer owner.

The subsequent one-off combined diff/identity/AST harness exited `1` with `StopIteration`. Per the active fail-closed
contract, the Executer correctly did not repair or rerun that harness, did not create an implementation commit, and did
not run postcommit targeted. This means the package cannot be accepted even though every repository regression surface
passed.

Independent read-only review confirms current identities:

- production source blob `a1e196664840bc340be789829b8cf0826c9ec7f4`, bytes `13918`, SHA-256
  `56d838b6b1e7dd0d68586cb9829d9e328ca8a05c670e08ff047e3324d4b77032`;
- candidate test blob `eb943384817996b96e332c83f618ba82cf210d4a`, bytes `12992`, SHA-256
  `6a072b9b52518f5a013112732992a9696d7de363b6bd893e70d478bb32d799fc`;
- runtime imports exact `ControllerRuntimeRequest` and `compose_controller_source`;
- exact eight test methods remain present;
- actual test08 method name is
  `test_08_static_owner_boundary_has_no_effect_retained_or_parallel_owner`;
- within that exact method, `ast.walk(selected_test08)` finds exactly one `generated_calls` assignment whose literal set
  contains both `RuntimeError` and `type`.

The ER classifies the temporary harness as using an unstable direct-body lookup. The ephemeral harness source was not
persisted, so this review does not overclaim its exact internal failing expression. The confirmed fact is narrower and
sufficient: the combined harness raised `StopIteration`, while a deterministic exact-name selection plus
`ast.walk(selected_test08)` succeeds against the committed candidate. Failure ownership is therefore the validation
harness, not the production owner, test candidate, scientific contract, or device boundary.

## 3. Safety / evidence accounting

The package made no external controller/root/source I/O and did not run synthetic integration. Old failed evidence,
retained R3, candidate payload, Git provenance replay, real B2, subordinate manifest, canonical validator, eligibility,
retained audit, and release operations remained exact `0`.

Network, DNS, environment, credentials, device, camera, Ray, strip, cleanup, capture, FORMAL, public analyzer, TD-C,
sentinel, P8, firmware, and deployment all remained exact `0`. PLAN/FULL/archive/debug/GUIDE/RESEARCH writes by the
Executer remained `0`. Retained R3 remains `RETAINED_UNVALIDATED_UNCONSUMED`.

## 4. Findings and residual risks

1. `48b3979d...` is regression-green but remains non-consumable because the frozen validation sequence did not reach a
   successful terminal static gate and post-gate admission.
2. Repeating another code/test correction would be incorrect: there is no remaining code/test defect demonstrated by
   this result.
3. A new implementation commit would obscure the already frozen candidate identity. The successor must consume that
   existing candidate without code/test writes and produce validation-only evidence.
4. The successor must freeze the real test08 method name and use `ast.walk(selected_test08)` or an equivalently
   deterministic subtree traversal; it must require exactly one literal `generated_calls` assignment rather than rely on
   a brittle positional/direct-body assumption.
5. Passing the successor still authorizes only Planner review. It does not itself emit eligibility, consume retained R3,
   enter synthetic integration, or unlock any device/scientific route.

## 5. Exact next branch

Archive this package and activate exactly one bounded validation-harness successor:
`REF-P7-25-R2-B2-P6-C1-C1-C1-V1` /
`P7-TD-B-RETAINED-R3-OPTION-B-B2-P6-C1-C1-C1-V1-DETERMINISTIC-VALIDATION-CLOSURE-V1`.

The successor writes no code/test file and creates no implementation commit. It validates exact candidate commit
`48b3979d...`, exact source/test identities, exact one-path candidate topology, real test08 name, runtime imports, eight
methods, and the unique literal generated-call set. It then runs a fresh targeted `8`, focused `90`, compileall, unique
full `775`, one CodeGraph query, the deterministic gate, and one ER append. Retry/fallback and all external/retained/
validator/release/network/device routes remain `0`. The sole stop is Planner review.
