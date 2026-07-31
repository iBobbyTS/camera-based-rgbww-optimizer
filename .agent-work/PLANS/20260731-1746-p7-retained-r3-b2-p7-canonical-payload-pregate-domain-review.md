# REF-P7-25-R2-B2-P7-C1-C1-C1-C1 Planner review：canonical payload pre-gate domain mismatch

**Review date：** 2026-07-31

**Reviewed contract：**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-P7-C1-C1-C1-C1-CANONICAL-SEMANTIC-PAYLOAD-CORRECTION-V1`

**Reviewed PLAN SHA-256：**
`518490d15f4c13a6de6c45422ca204c05f6b00c0ac640fbce29cfdb00f47030b`

**Planner decision：**
`REJECTED_PRE_GATE_EXECUTER_CR_DOMAIN_ASSERTION_CANDIDATE_NOT_YET_CONSUMABLE`

## 1. Reviewed scope and immutable topology

Activation commit `be0e4dafd725207d14c7862777f2739f68f99e81` is the direct child of
`f6a22638ff19ae63c661a7d1fdc81ae0124166f3`, has subject
`chore(plan): activate p7 canonical semantic payload correction`, and changed exactly FULL、PLAN and
`.agent-work/PLANS/20260731-1730-p7-retained-r3-b2-p7-c1-c1-c1-targeted-residual-review.md`.
The Executer began from that clean activation and matched the frozen PLAN/FULL identities.

Orchestrator preserved the exact two-path candidate as commit
`88c4c0370a5dc296c04e949823c952398c6a394d`, direct parent the activation, subject
`chore(p7): retain rejected p7 payload candidate`, changed paths exact:

1. `src/camera_based_rgbww_optimizer/utils/p7_retained_r3_controller_domain_template.py`
2. `tests/test_p7_retained_r3_controller_domain_template.py`

The candidate canonical binary diff SHA-256 against activation is
`89cf2b7f7452deb7c139fbb26f1dfb91fa49574610e1a341a48610fbd1929fb4`.
Current source blob/bytes/SHA-256 is
`bbbcb3390a275043d72883729ddb6c8246de9e5a` / `19754` /
`4601582595b59ff9a82721550a87e6d720bb390bb8e39e57324a711f599e36cb`；current dedicated-test
blob/bytes/SHA-256 is
`4074404187191b18286d201d456ea167294632c3` / `26844` /
`13ec55eaac578f58583c7d6541733b3d2ab237168f1185796d9a9e9f3a449032`.

Evidence commit `6d400efb156e3d072cecb5ea42dc5e923f8b0854` is candidate's direct child, subject
`chore(evidence): record p7 payload pregate failure`, and changes exact
`.agent-work/EXECUTION_RESULT.md`. Review started from this exact clean HEAD. Retained R3 remains
`RETAINED_UNVALIDATED_UNCONSUMED`.

## 2. Implementation result and validation quality

The candidate completed the active package's exact bounded correction inside the two authorized paths:

- production `semantic_matrix` is now ordered exact `16` list-of-list entries; names, order, boolean sources,
  `len == 16` / `all(...)` decision and persisted `{"matrix": semantic_matrix}` remain unchanged;
- test03 now checks the actual escaped-NUL runtime-path source boundary instead of the stale nonexistent boundary;
- test08 explicitly accounts for the existing generated calls `any` and `join` without a generic allowlist;
- the in-memory owner harness records positive canonical exact-16 payload and tuple-negative behavior;
- the prior three generated LF and five generated NUL corrections, physical-NUL-zero invariant, owners, API,
  lifecycle, paths, budgets and guarded entrypoint remain frozen.

The unique fresh pre-gate exited `1`, but only after passing activation, exact paths, baseline identities,
`git diff --check`, strict UTF-8, module/test/generated AST parse and compile, exact production reconstruction,
exact `11` methods, literal test08 addition, physical NUL `0`, generated LF count `3`, outer-template NUL correction
locations `5`, generated runtime NUL constants `8`, and generated runtime LF constants `3`.

The sole failure was an Executer-authored validation-domain mismatch: the gate required a carriage-return string
constant in the generated-controller AST. Independent current-source inspection confirms CR rejection is owned by
the outer builder `_plain` boundary (`"\r" in value`), while `_CANONICAL_TEMPLATE` intentionally has no generated
CR constant. Therefore this result does not demonstrate a code/test semantic defect. It does demonstrate that the
executed package failed its exact fail-fast gate, so this review cannot accept or consume the candidate yet.

Because retry/fallback were exact `0/0`, the gate was not corrected or rerun. The later formal matrix/payload inventory,
targeted `11`, focused `93`, compileall, full `778`, implementation commit and postcommit targeted were all exact `0`.
This evidence is sufficient to reject the execution and bound a validation-only successor; it is insufficient to accept
the runnable template.

## 3. Safety and zero-effect audit

Code/test changes exist only in the preserved candidate commit. External controller/source/root/process、synthetic
integration、old failed evidence、retained artifacts/candidate payload reads、Git provenance replay、real B2、subordinate
manifest、canonical validator、eligibility、retained audit、release、network、DNS、environment、credentials、device、camera、
Ray、strip、cleanup、capture、FORMAL、public analyzer、TD-C、sentinel、P8、firmware and deployment remained exact `0`.
Executer writes to PLAN、FULL、archive、debug、GUIDE and RESEARCH remained `0`.

## 4. Residual risks and exact next branch

There is no evidence-backed reason for another production or dedicated-test correction. Re-editing the candidate or
creating another implementation commit would obscure the already frozen exact two-path identity. The next package must
therefore be validation-only and consume the committed candidate without code/test writes.

The successor must replace the invalid gate condition with exactly one correct deterministic domain check:

1. verify CR rejection in the outer builder source and behavior (`_plain`), including a bounded CR-bearing spec specimen
   that fails with the expected stable builder error;
2. parse/compile the generated controller and explicitly avoid requiring a CR constant there;
3. complete all previously unreached formal matrix/payload inventory checks, including exact ordered 16 list-of-list
   payload, canonical encode/strict decode/re-encode, tuple-negative fail closed, test03/test08 exact inventories and all
   frozen runnable-contract counts;
4. then run fresh targeted `11/11`, focused `93/93`, compileall and unique full `778/778` once each.

No code/test write and no implementation commit is authorized. Passing validation may make candidate `88c4c03...`
consumable only after independent Planner review. The exact successor is
`REF-P7-25-R2-B2-P7-C1-C1-C1-C1-V1` /
`P7-TD-B-RETAINED-R3-OPTION-B-B2-P7-C1-C1-C1-C1-V1-CORRECT-DOMAIN-VALIDATION-CLOSURE-V1`.
Retry/fallback、CodeGraph and all external/retained/validator/release/network/device routes remain `0`; the sole stop is
Planner review.

维护性判断：candidate remains inside the single deterministic template owner and dedicated test; the successor only
corrects a disposable validation gate and adds no owner、helper、serializer、allowlist or execution path.
