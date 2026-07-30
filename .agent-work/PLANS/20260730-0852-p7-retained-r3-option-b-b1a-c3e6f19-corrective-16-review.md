# F19 Corrective 16 Planner Review

**Reviewed reference task:** `REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-16`

**Decision:** `REJECTED_FOCUSED_POST_EQ_VALIDATION_SUCCESSOR_MISSING`

**Planner review date:** `2026-07-30`

## Reviewed scope and method

The Planner reviewed the complete active C16 PLAN, the single C16 append in
`.agent-work/EXECUTION_RESULT.md`, and the immutable artifacts under:

`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b1a-c3e6f19-corrective-16-offline/20260730T144754Z`

The review independently recomputed artifact SHA-256 values, inspected the terminal
seal and focused log, and compared the observed commands, topology, identities,
locks, and stop point against the C16 contract. No test, controller, Git mutation,
network, device, release, retained-R3 validator, cleanup, formal, or analyzer command
was invoked by the Planner.

## Authoritative evidence

- `terminal-evidence.json`: bytes `7577`, mode `0600`, SHA-256
  `53372a9d08ed8f30c5f2f471c15cabf0f7fe9c432ce070a1d23a2ec30db7566a`.
- `prevalidation-git-object-freeze.json`: bytes `9334`, mode `0600`, SHA-256
  `d928035c5a60c6da0162802ea269d887b3d162da892c797f02ae7ee06d6cfedd`.
- `03-focused.log`: bytes `47292`, mode `0600`, SHA-256
  `abbc6431d0ed70994b553d47631ecbca4b32f4382f1f2374b9d836dd9c78e26e`.
- Dispatch HEAD was read programmatically once as
  `7f2ce2393eaa0f4ed42d891ae666faccb422d445`; human-transcribed child SHA and
  second HEAD reads were both `0`.
- Retained C15 implementation remained
  `3a14fe0bd663250dd48c65e71f1a6550df89267f`, direct parent
  `431d9d8dd58a6c0df7fb0b225ce206d2e8c57f53`, subject
  `fix(p7): exclude root Finder metadata from EQ evidence`, exact source plus
  `tests/test_p7_td_b_r6_contract.py` paths, additional paths `0`, and canonical
  binary patch SHA-256
  `018cf00c4e452673f4303ce528fbea2c0b6667e8dc691f5ff44c6968603412de`.

## Validation quality and findings

- Prevalidation Git-object freeze: accepted. It truthfully records
  `derived_prevalidation_from_git_objects=true`,
  `recorded_before_historical_edit=false`, and makes no pre-edit-freeze claim.
- Compileall: one call, exit `0`.
- Exact targeted selectors: one call, `6/6`, exit `0`.
- Focused suite: one call, `193` tests, exit `1`, failures `1`, errors `2`.
- Full suite, CodeGraph, and diff checks: correctly left at `0` by fail-fast.
- Retry and fallback: `0/0`; repository implementation mutations: `0`.
- Candidate, retained R3, canonical retained validator, eligibility emission,
  release, network, `.env`, device, camera, Ray, strip, cleanup, FORMAL, public
  analyzer, TD-C, sentinel, and P8 calls all remained `0`.

All three focused failures share one engineering provenance cause. Historical
post-EQ accepted commit `161094ffa2bf1f84ed1fc787e708e8c3463f10db`
correctly freezes `tests/test_p7_td_b_r6_contract.py` at SHA-256
`10374ec2366fc8cbe928953690defc31c83dc5c04da192f599f59591ec196f23`.
The later exact retained commit `3a14fe0bd663250dd48c65e71f1a6550df89267f`
legitimately changes that validation path to SHA-256
`77ef59ccee5eee34d85658aadf7a6ce40f413fee9b8395cd11fb82145df27104`.
The current post-EQ owner has no exact subordinate successor binding, so it
compares the current checkpoint and working tree to the historical blob before
the ordinary candidate and negative-test semantics can run. Two positive tests
therefore error with `checkpoint blob differs`; the duplicate-ledger negative
test is masked by the same earlier error.

## Decision and residual risk

C16 cannot be accepted because focused validation is not green and the full,
CodeGraph, and diff gates were not reached. The prevalidation freeze and retained
C15 topology remain valid evidence; they do not imply eligibility.

The corrective route must preserve the exact historical accepted commit and all
of its commit-object blob validation. It may add only an exact subordinate
successor for retained commit `3a14fe0...`, binding its full commit and parent,
subject, exact two-path topology, before/after blob identities, LF path-ledger
digest, and canonical binary patch digest. Classification continuation is limited
to exact path `tests/test_p7_td_b_r6_contract.py` with the existing
`accepted_post_eq_exposure_policy_validation` meaning. The successor's source path
is provenance-only and must not become classified. A generic allowlist, arbitrary
current-blob acceptance, historical payload rewrite, or canonical candidate-owner
replacement is prohibited.

Residual risk is bounded to this lineage seam: an incomplete layer could weaken
historical validation, accidentally classify the successor source path, or allow
nearby paths/commits. C17 therefore requires explicit negative matrices and the
full validation chain.

## Exact next branch

`REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-17`: implement and validate the exact
post-EQ validation-path subordinate successor. Retained R3 remains
`RETAINED_UNVALIDATED_UNCONSUMED`; release consumption and all device/scientific
stages remain locked. The package returns to the Planner after one terminal seal.
