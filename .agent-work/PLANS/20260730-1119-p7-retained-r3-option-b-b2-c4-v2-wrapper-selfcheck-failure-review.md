# REF-P7-25-R2-B2-C4 V2 wrapper self-check failure review

**Planner decision:** `REJECTED_PRE_HEAD_WRAPPER_SELFCHECK_FAILURE`

**Review date:** `2026-07-30`

**Reviewed contract:**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-C4-AST-SPAN-SUCCESSOR-QUALIFICATION-V2`

**Reviewed PLAN:** `.agent-work/PLAN.md`, bytes `19142`, SHA-256
`ce70a92b26a665a78aec31a01a06cbbd2627436a94c5105825c4e7d57babb36f`.

**Prior reviewed archive:**
`.agent-work/PLANS/20260730-1104-p7-retained-r3-option-b-b2-c4-pre-root-dispatch-failure-review.md`,
bytes `4552`, SHA-256
`05e8ec155c487a01ccd3ce5ace8a690005ba678500cfa4450870af99f9393463`.

## Reviewed result and evidence limit

The sole `zsh -f` wrapper invocation entered its first content-free helper
self-check and exited `42`. The helper attempted to validate the ordinary test
name `safe_local_value` with the zsh pattern `[a-z_][a-z0-9_]#`; under the
wrapper's default option state that expression did not provide the intended
cardinality semantics. This is a deterministic wrapper self-check defect.

Observed budgets for the only invocation are:

```text
zsh -f wrapper invocations = 1
wrapper self-check = 0/6
symbolic HEAD reads / emitted HEAD values = 0/0
builder invocations / root creates = 0/0
C3 / frozen source reads = 0/0
successor / terminal / terminal-seal writes = 0/0/0
EXECUTION_RESULT appends = 0
retry / fallback / alternate dispatch = 0/0/0
```

No builder or evidence root existed for this attempt, so there is no physical
terminal to replay and no ER append to inspect. This review is limited to the
pre-HEAD wrapper facts delivered to Planner and the immutable active PLAN
identity above. It does not claim an independently replayable wrapper trace,
HEAD identity, C3/source identity, transform result, matrix result, or C4
qualification evidence. The repository was reported clean after the failed
wrapper; this review did not perform a prohibited HEAD read or any Git/controller/
test invocation to strengthen that report.

## Decision

The execution is rejected. It proves no C4 content or acceptance condition.
The failure precedes the sole programmatic HEAD read and therefore also leaves
the activation-child identity deliberately unobserved by the execution.

The fault is confined to a self-check's reliance on zsh glob/cardinality option
semantics. It does not contradict the accepted C3 structure index or the frozen
C4 AST/span transform, lifecycle, matrix, evidence, and lock contracts. A new
reference task or separate corrective stage would create unnecessary ownership.
C4 may therefore proceed directly as V3 after Orchestrator review and one later
PLAN-only activation.

The V2 future root
`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b2-c4-ast-span-successor-da90556-r2-20260730T1710Z`
is superseded and reported uncreated/unprobed. It must remain unprobed,
uncreated, unreused, undeleted, and unrenamed. V3 must use a new root.

## Exact C4 V3 correction

The next PLAN keeps the single `zsh -f` dispatch owner and every C4 content
boundary unchanged, but removes all dependence on shell pattern options from
the pre-HEAD path:

1. the wrapper contains one statically written ordinary variable
   `dispatch_head_value`; no caller-provided or dynamically expanded variable
   name is ever evaluated, declared, assigned, or passed to `typeset`;
2. an embedded Python pure-memory validator owns exact bytewise name admission
   (`dispatch_head_value` only), exact lowercase 40-hex value validation,
   cardinality, and output-event accounting; it performs no filesystem, Git,
   process-launch, root, C3, or source operation;
3. before any HEAD read, the same validator path must pass an exact self-contained
   matrix covering the one allowed name, `safe_local_value`, zsh special names,
   valid/malformed/multiline values, and exactly-one output accounting;
4. only after the matrix passes may the wrapper execute exactly one
   `git rev-parse HEAD`, assign the validated bytes directly to the statically
   written variable, emit once, and invoke the sole builder once;
5. no `extendedglob`, `kshglob`, `bareglobqual`, `shglob`, `setopt`, shell glob
   operator, dynamic assignment, `eval`, retry, fallback, reconstruction, or
   second HEAD read is permitted.

The correction changes no C3/source input, AST/span selector, transform,
successor, `12/12` lifecycle matrix, evidence owner, retained/validator/release
lock, or acceptance criterion.

## Exact next branch and stop

`REF-P7-25-R2-B2-C4` remains the sole reference task. Active PLAN V3 is
non-executable until Orchestrator accepts this review, commits the reviewed
state, and a later exact PLAN-only activation freezes its direct parent and
sets `execution_authorized=true`.

Real B2, B3, retained R3, canonical validator, eligibility, release, devices,
FORMAL-R6, strip, TD-C, sentinel and P8 remain locked.

Planner stop:
`B2_C4_V2_SELFCHECK_FAILURE_REVIEWED_WAITING_PLAN_ONLY_ACTIVATION`.

## 维护性判断

The V3 correction deletes option-sensitive shell validation rather than adding
a second wrapper or lifecycle owner. Dispatch remains one wrapper, C4 remains
one builder and one lifecycle owner, and no repository production abstraction
or scientific rule changes.
