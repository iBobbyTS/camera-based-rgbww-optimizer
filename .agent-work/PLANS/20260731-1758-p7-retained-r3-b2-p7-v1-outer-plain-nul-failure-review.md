# REF-P7-25-R2-B2-P7-C1-C1-C1-C1-V1 Planner review archive

**Reviewed contract:**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-P7-C1-C1-C1-C1-V1-CORRECT-DOMAIN-VALIDATION-CLOSURE-V1`

**Planner decision:**
`REJECTED_PRE_GATE_OUTER_PLAIN_PHYSICAL_NUL_REJECTION_MISSING_CANDIDATE_NOT_CONSUMABLE`

**Review date:** 2026-07-31

## Reviewed scope and frozen topology

The reviewed package was validation-only. Its purpose was to consume immutable candidate
`88c4c0370a5dc296c04e949823c952398c6a394d` and replace the superseded generated-AST CR assertion with a source-backed outer-builder ownership check. It did not authorize code/test edits, implementation commits, external controllers, retained-R3 reads, integration, validator/release work, network, environment, credentials, or device work.

The activation was exact:

- activation commit `12a38ea64040e8ab3eedd91c6feee80e6fe64494`;
- direct parent `6d400efb156e3d072cecb5ea42dc5e923f8b0854`;
- subject `chore(plan): activate p7 payload validation closure`;
- changed paths exactly `.agent-work/FULL_PLAN_REFERENCE.md`, `.agent-work/PLAN.md`, and `.agent-work/PLANS/20260731-1746-p7-retained-r3-b2-p7-canonical-payload-pregate-domain-review.md`.

The frozen candidate topology also matched:

- commit `88c4c0370a5dc296c04e949823c952398c6a394d`, parent `be0e4dafd725207d14c7862777f2739f68f99e81`, subject `chore(p7): retain rejected p7 payload candidate`;
- changed paths exactly `src/camera_based_rgbww_optimizer/utils/p7_retained_r3_controller_domain_template.py` and `tests/test_p7_retained_r3_controller_domain_template.py`;
- canonical binary diff SHA-256 `89cf2b7f7452deb7c139fbb26f1dfb91fa49574610e1a341a48610fbd1929fb4`;
- module blob/bytes/SHA-256 `bbbcb3390a275043d72883729ddb6c8246de9e5a` / `19754` / `4601582595b59ff9a82721550a87e6d720bb390bb8e39e57324a711f599e36cb`;
- dedicated-test blob/bytes/SHA-256 `4074404187191b18286d201d456ea167294632c3` / `26844` / `13ec55eaac578f58583c7d6541733b3d2ab237168f1185796d9a9e9f3a449032`.

## Evidence and validation quality

The Executer appended one terminal section to `.agent-work/EXECUTION_RESULT.md`; Orchestrator preserved it in evidence commit
`11eba96e2c971b2c6da1e0a7e3bdf9dd574d20d0` (`chore(evidence): record p7 outer plain nul gap`). Current reviewed ER identity is bytes `1123783`, SHA-256
`b57bc9c7049ff156a7eac035b55d378af600000805ad15b3702bf6000cf788ba`.

Activation, candidate topology, immutable source/test identities, strict UTF-8, module/test AST parse and compile, `git diff --check`, exact eleven test methods, and clean pre-gate porcelain all passed. The corrected deterministic pre-gate then ran exactly once and exited `1` at its first outer-owner assertion:

`AssertionError: outer_plain_physical_nul_rejection_missing`

Source-backed AST inspection establishes the cause. `_plain` currently tests the string constant `"\\x00"`, which denotes the four-character literal escape text backslash-`x00`; it does not test a physical NUL character. The same condition does contain physical LF and CR constants. This is therefore a real owner-semantic defect, distinct from the already superseded mistake of requiring a CR constant in the generated controller AST.

The fail-fast occurred before the CR behavior specimen and before generated-AST, exact-16 matrix, canonical JSON, runnable lifecycle, stdout, or stderr inventory. Corrected-gate invocations were `1`; second gate, retry, and fallback were `0`. Targeted11, focused93, compileall, unique full778, CodeGraph, implementation commit, and postcommit test were all `0`. Code/test/candidate writes were `0`.

Every external or later-stage budget remained zero: external controller/source/root/process, synthetic integration, retained artifacts, candidate payload, Git provenance replay, real B2, subordinate manifest, canonical validator, eligibility, retained audit, release, network, DNS, environment, credentials, device, camera, Ray, strip, cleanup, capture, FORMAL, public analyzer, TD-C, sentinel, P8, firmware, and deployment.

## Findings and decision

The V1 validation result is rejected exactly as executed. Candidate `88c4c03...` remains non-consumable; retained R3 remains `RETAINED_UNVALIDATED_UNCONSUMED`; no integration or later route is unlocked.

This is an engineering validation-boundary defect, not a color-science question, architecture decision, or Human-authorization boundary. The smallest correction remains inside the accepted deterministic template owner and its dedicated regression file. It must not add a serializer, matrix owner, helper, analyzer, fallback, or generic allowlist.

## Exact next branch

Next task:
`REF-P7-25-R2-B2-P7-C1-C1-C1-C1-V1-C1`.

The bounded correction may change exactly the existing module and dedicated test. It must:

1. make outer `_plain` reject a physical NUL character with the existing stable field-specific error code;
2. prove through public builder behavior that a physical-NUL specimen fails, while the literal four-character escape text backslash-`x00` remains accepted where otherwise valid;
3. keep `_CANONICAL_TEMPLATE` byte-identical at bytes `11999`, SHA-256 `0369231f11bc968ebc343bac57acab236d75faf5d5d6e2b9c3d82918df19a467`, with physical NUL count `0`, literal generated `\\x00` token count `8`, and literal generated `\\n` token count `3`;
4. keep the exact-spec replacement statement byte-identical at bytes `1907`, SHA-256 `502c303e6257d8f59a4d5bbd39b0339371e210a8c10c9e8fa3fd0d253016080`;
5. run one fresh pre-gate, targeted `11/11`, focused `93/93`, compileall, unique full `778/778`, one focused implementation commit, and postcommit targeted `11/11`, with inherited CodeGraph calls `0`, retry/fallback `0/0`, and all external/retained/device routes locked.

Planner stop after that package:
`B2_P7_C1_C1_C1_C1_V1_C1_OUTER_PLAIN_PHYSICAL_NUL_CORRECTION_WAITING_PLANNER_REVIEW`.

No earlier archive is overwritten, and this archive does not authorize execution by itself.
