# REF-P7-25-R2-B2-P7-C1 targeted canonical-template NUL failure review

**Review date:** 2026-07-31

**Reviewed contract:**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-P7-C1-CODEGRAPH-PREFLIGHT-ORDER-CORRECTION-V1`

**Reviewed stop:**
`B2_P7_C1_CODEGRAPH_PREFLIGHT_ORDER_CORRECTION_WAITING_PLANNER_REVIEW`

**Planner decision:** `REJECTED_TARGETED_CANONICAL_TEMPLATE_PHYSICAL_NUL`

## 1. Frozen topology and evidence

The activation commit is
`13f79754daf549deeee5b470e2e620fa70e43545`, direct parent
`778576e1bc1df797e0293d52fa58dfe4fc385744`, subject
`chore(plan): activate p7 c1 codegraph preflight correction`, with exact changed
paths:

- `.agent-work/FULL_PLAN_REFERENCE.md`;
- `.agent-work/PLAN.md`;
- `.agent-work/PLANS/20260731-1656-p7-retained-r3-b2-p7-codegraph-ordering-failure-review.md`.

The rejected, immutable candidate commit is
`96b15f4d7e000cb2f2276f069ad92832226b1afd`, direct child of that activation,
subject `chore(p7): retain rejected p7 c1 runnable candidate`, with exact two
changed paths:

- `src/camera_based_rgbww_optimizer/utils/p7_retained_r3_controller_domain_template.py`;
- `tests/test_p7_retained_r3_controller_domain_template.py`.

Its canonical binary diff SHA-256 is
`1c31652a43350f50076a1d3e13da4dfd6ab5fc372341d3df3ad2e70cddc981ea`.
Committed candidate identities are:

| path | bytes | SHA-256 |
| --- | ---: | --- |
| `src/camera_based_rgbww_optimizer/utils/p7_retained_r3_controller_domain_template.py` | 19747 | `3a6a7c3b93d996369dfc7b0813cae098032d1c6c93136d82321ceb93886dcb59` |
| `tests/test_p7_retained_r3_controller_domain_template.py` | 20936 | `029233a25caa63b8f76b03557353ef748005d0e7f143425e36f5747cc688a841` |

Evidence commit
`158ea8c2385dede47cc090093f126a0a167acfb6` is the candidate's direct child,
subject `chore(evidence): record p7 c1 targeted nul failure`, and changes only
`.agent-work/EXECUTION_RESULT.md`. Review began at that clean HEAD.

## 2. Validation quality and finding

Activation and identity-only checks passed. The required exact one
`codegraph sync` exited `0`, and the immediately following exact one
`codegraph explore` exited `0`; no source/test content had been read first and
there was no post-edit CodeGraph invocation. This closes the earlier ordering
defect and remains valid preflight evidence for the direct successor correction.

The exact two authorized code/test paths were the only implementation paths.
The candidate introduced the intended replacement-only bindings, existing
provenance/lifecycle owners, exact one guarded controller entrypoint, eight
callbacks, persist-before-read ordering, canonical success envelope, and fake
owner coverage. The dedicated test file contained exact `11` test methods.

The unique targeted invocation exited `1`: exact `Ran 11 tests`, with `1` pass,
`10` errors, and `0` failures. All ten errors have the same first boundary:
`SyntaxError: source code string cannot contain null bytes`, surfaced as stable
`ControllerDomainTemplateError("canonical_template_invalid")`. The outer
Python bytes template interprets generated-source `\x00` separators while the
owner module is imported, so the generated source contains physical NUL bytes
before `ast.parse` or compilation. This is a single escape-layer defect, not a
runtime-owner, lifecycle, provenance, scientific, retained-evidence, or device
failure.

Retry/fallback were exact `0/0`. Focused `93`, compileall, full `778`, static
post-edit gates, implementation commit, and postcommit targeted `11` were all
correctly skipped. External controller/root/process, synthetic integration,
retained/candidate reads, validator, eligibility, release, network, environment,
credentials, device, camera, Ray, strip, cleanup, capture, FORMAL, public
analyzer, TD-C, sentinel, P8, firmware, and deployment all remained `0`.

## 3. Acceptance decision and residual risk

P7-C1 is rejected and cannot be consumed. Candidate
`96b15f4d7e000cb2f2276f069ad92832226b1afd` is retained solely as a rejected
direct-parent candidate for the bounded successor; it does not qualify
synthetic integration and does not unlock retained R3 or later stages.

Residual risk is narrowly bounded: the successor must preserve escaped NUL
syntax as generated-source bytes without changing separator semantics at
generated runtime. A broad string replacement, raw-template conversion, or
generic escaping helper could silently alter unrelated backslashes and is
therefore prohibited. A meaningful byte-level regression must prove both that
the owner-generated source contains no physical NUL and that the exact escaped
separator syntax remains present where the frozen Git-output comparisons and
value guard require it.

## 4. Exact next branch

The only next package is `REF-P7-25-R2-B2-P7-C1-C1`, an exact-two-path minimal
correction based on the rejected candidate. It may change only the existing
domain-template module and dedicated test. It must correct only the generated
source NUL separator escape layer, add or preserve the byte-level regression,
run fresh targeted `11`, focused `93`, compileall, unique full `778`, create one
direct-child implementation commit, and run postcommit targeted `11`.

The accepted P7-C1 CodeGraph preflight is frozen as the successor's pre-edit
ownership evidence; new CodeGraph sync/query invocations are `0`. Retry and
fallback remain `0`. All external, retained, validator, release, network, and
device routes remain locked. The successor stops at
`B2_P7_C1_C1_NUL_ESCAPE_CORRECTION_WAITING_PLANNER_REVIEW`.

## 5. Maintainability judgment

The correction remains within the existing deterministic template owner and
its dedicated tests. It introduces no helper, parallel state owner, lifecycle,
or coordinator; byte-level coverage protects the only changed semantic boundary.
