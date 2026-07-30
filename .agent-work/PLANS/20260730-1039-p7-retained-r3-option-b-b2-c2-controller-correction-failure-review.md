# REF-P7-25-R2-B2-C2 controller correction failure review

**Reviewed reference task:** `REF-P7-25-R2-B2-C2`

**Reviewed contract:**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-C2-CONTENT-FREE-CONTROLLER-LIFECYCLE-CORRECTION-V1`

**Planner decision:**
`REJECTED_SOURCE_TRANSFORM_ANCHOR_UNPROVEN_WITH_CORRECTION_ROOT_FAILURE_LIFECYCLE_ACCEPTED`

**Planner review date:** `2026-07-30`

## Reviewed scope and method

The active PLAN authorized one pure-offline builder invocation against one
brand-new correction root. The builder could read the frozen rejected
controller once, inspect only metadata of the earlier empty failed root, create
one successor controller, and validate resolved-record semantics plus terminal
lifecycle behavior entirely with content-free fixtures. It was forbidden from
reading C1, retained-R3, or decision payloads and from invoking any real
successor, validator, release, network, device, or scientific stage.

The reviewed dispatch HEAD is
`93d34a802dba8d98a2337b88885b95e866f7f8c5`; its active PLAN blob is `17858`
bytes with SHA-256
`7524d0c9aaa881e6722ab6cad97fe0c494c7dda3950e7c054e8be0e16a10fb7c`.
The sole disposable builder is
`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-b2-c2-builder-da90556.py`, `21294`
bytes, SHA-256
`068cf2b083069ca4ab08d64e2fe4522268d085ddb8f8890c8e7a8a4b8fdb5596`.

The Planner independently read only the active PLAN, the latest C2 handoff,
the three direct files in the fresh C2 root, and the disposable builder. It did
not invoke the builder, reopen the rejected controller, inspect C1 or retained
payloads, reuse or modify either failed root, run a successor, tests, validator,
release, network, device, camera, Ray, strip, cleanup, formal, or analyzer.

## Authoritative physical evidence

Fresh immutable root:
`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b2-c2-controller-correction-da90556-20260730T1621Z`,
mode `0700`, device `16777240`, inode `2188356`. It contains exactly three
direct regular files, all mode `0600`:

1. `progressive-00-root-created.json`: `1062` bytes, SHA-256
   `7e72b76432d815c6040656b2e9d61092677437e3464c8a9e53bca6aba453b0d0`;
2. `terminal-evidence.json`: `1607` bytes, SHA-256
   `56bf421941259015d02531369dc21e6e1184468e2246cb7adec49e99b992ce48`;
3. `terminal-evidence.sha256.json`: `455` bytes, SHA-256
   `b3624e6c948afce349534461e54864dd19590489f3b454293a3af3b0f49db101`.

All three are strict JSON and exactly canonical under sorted keys, compact
separators, UTF-8, and one terminal LF. The terminal seal independently binds
the physical terminal bytes, SHA-256, schema, and
`hard_failure_waiting_for_planner` status; it records
`terminal_write_returned=true` and
`terminal_seal_self_write_return=not_self_attested`.

The progressive record binds the exact dispatch, source identity, prior failed
root metadata, and new-root identity. The terminal repeats those identities and
truthfully records `RuntimeError: main anchor count`. The direct file set proves
that no successor, patch, validation summary, fixture tree, or later progressive
stage was produced.

The latest ER contains exactly one C2 handoff. Its ordering claim is consistent
with the physical inode/order progression and the sealed hashes: root
progressive writer returned, failure terminal writer returned, terminal-seal
writer returned, then the sole ER append occurred.

## Evidence strength and limits

### Accepted strong evidence

- Dispatch topology, source identity, failed-root metadata, and brand-new-root
  identity are redundantly bound by the progressive and terminal evidence.
- The builder consumed the rejected controller exactly once and did not perform
  a second read after the failed transform.
- The correction-root owner durably persisted a truthful failure terminal and
  non-self-attested seal after a post-root builder failure.
- C1 evidence reads, retained artifact/directory access, decision-source reads,
  real/content-free successor invocations, validator, eligibility, release,
  network, device, and scientific operations remained zero.
- Retry, fallback, second builder, second root, repository implementation edit,
  and commit remained zero.

### Evidence that does not exist

- Resolved-record matrix evidence is `0/10`, not a pass.
- Successor lifecycle matrix evidence is `0/8`, not a pass.
- No successor controller, binary-safe patch, validation summary, or transformed
  source identity exists.
- The terminal records only `main anchor count`; it does not record the actual
  match count, the selected source span, the function signature shape, or an
  AST-derived structural index.

The Planner therefore cannot determine from durable evidence whether the
regex missed an annotated signature, a multiline signature, non-top-level
placement, multiple definitions, or another source shape. Reopening the already
consumed rejected source during this review would exceed the review boundary and
would not retroactively repair C2 evidence. The exact source shape remains
unproven, not inferred.

## Findings

### Finding C2-F1: mechanical regex is not a source-structure owner

The builder searched with
`(?m)^def main\([^\n]*\):\n` and required exactly one match. This recognizes
only one textual spelling: a non-indented, single-line, synchronous definition
whose closing parenthesis is followed immediately by a colon and LF. It is not
equivalent to the Python semantic concept of one top-level `main` function and
does not cover valid annotations, multiline signatures, decorators, or other
syntax forms.

The failure proves that this textual assumption did not match the frozen
source. It does not prove which alternative shape exists. A replacement package
must first produce an immutable AST/source-structure index from one newly
budgeted source read. Discovery must record every candidate and its exact source
span/hash without failing merely because a guessed cardinality is wrong.

### Finding C2-F2: successor lifecycle remains untested and unintegrated

The disposable builder contains an `ExactPostRootLifecycle` helper and eight
fixture definitions, but execution failed before the successor was written or
invoked. Those fixtures are therefore source intent only; `0/8` cannot be
reported as proven behavior.

Moreover, the attempted mechanical transform replaced the path predicate,
inserted helper text immediately before a regex-selected `main`, and replaced
the module entrypoint. It did not structurally wrap or route the real `main`
post-root body through `ExactPostRootLifecycle`. Thus fixing only the `main`
regex would still leave the real-input lifecycle requirement unproven and could
permit fixture-only behavior to diverge from the future real path.

The physically proven lifecycle is narrower: the C2 **builder/correction-root**
failure owner successfully persisted progressive, terminal, seal, and post-seal
handoff evidence. A future builder may reuse that persistence pattern, but it
must not claim that the successor lifecycle or real `main` integration has
already passed.

## Decision

`REF-P7-25-R2-B2-C2` is rejected as a controller-correction implementation.
The package safely failed and its correction-root failure lifecycle is accepted,
but none of the successor correction, resolved-record matrix, successor
lifecycle matrix, or real-path integration acceptance criteria were met.

Retained state remains `RETAINED_UNVALIDATED_UNCONSUMED`. B2 real input, B3,
canonical validator, eligibility, release consumption, device work, FORMAL-R6,
strip, TD-C, sentinel, and P8 remain locked. No Advisor or Human decision is
needed because this is an offline engineering/provenance defect with no
unresolved measurement-science branch or dangerous operation.

## Exact next branch

The next package is deliberately discovery-only:

- Reference task: `REF-P7-25-R2-B2-C3`.
- Contract:
  `P7-TD-B-RETAINED-R3-OPTION-B-B2-C3-CONTENT-FREE-SOURCE-STRUCTURE-INDEX-V1`.
- Single action after Orchestrator review and PLAN-only activation: use one new
  builder and one newly budgeted read of the exact frozen rejected controller to
  emit a sealed AST/source-structure index plus a content-free AST-selector
  fixture summary in one brand-new root.
- The index records all top-level/nested `main` candidates, exact semantic path
  predicate-call candidates, module `__main__` guards, and selected-main body
  statement/root-creation structure using positions, node kinds, normalized AST
  hashes, and source-span hashes. It does not transform or execute the source.
- Discovery completion is independent of candidate cardinality. Candidate
  counts are evidence for the subsequent Planner decision, not a reason to
  silently guess or repeat a regex anchor.
- The package may reuse the physically proven builder failure-persistence
  pattern, but successor generation, patching, real/content-free successor
  invocation, lifecycle matrix, C1/retained reads, validator, and release stay
  zero.
- Current stop:
  `B2_C2_FAILURE_REVIEWED_WAITING_ORCHESTRATOR_REVIEW`, with
  `execution_authorized=false`.
- Future C3 execution stop:
  `B2_C3_SOURCE_STRUCTURE_INDEX_WAITING_PLANNER_REVIEW`.

Only after C3 is independently accepted may a later package freeze an AST-based
transformation and actual real-main lifecycle integration strategy. C3 itself
does not authorize that later transform.

## Residual risks

- A structure index can prove selector candidates but cannot by itself prove a
  successor transform or runtime lifecycle.
- Normalized AST hashes must be accompanied by exact byte-span hashes and source
  identity; AST normalization alone would discard formatting boundaries needed
  for a minimal binary-safe patch.
- The discovery builder must record ambiguity rather than select the first
  candidate by traversal order.
- The next transform must connect the same lifecycle owner to both content-free
  fixtures and the future real-input body; a parallel fixture-only owner would
  repeat C2-F2.
- The C2 root and earlier failed root are immutable evidence and must never be
  reused, repaired, populated, or deleted.

## 维护性判断

The rejection identifies two ownership boundaries rather than adding a new
repository abstraction: semantic source selection belongs to one AST-derived
index/selector owner, while correction-root persistence belongs to one already
proven terminal lifecycle pattern. C3 isolates structural discovery from source
mutation so the later transformation can be small, evidence-bound, and testable.
No production module, scientific owner, or parallel eligibility path is added.
