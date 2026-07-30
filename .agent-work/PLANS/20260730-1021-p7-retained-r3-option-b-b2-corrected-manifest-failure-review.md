# REF-P7-25-R2-B2 corrected manifest failure review

**Reviewed reference task:** `REF-P7-25-R2-B2`

**Reviewed contract:**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-CORRECTED-PATH-MANIFEST-SEAL-V3`

**Planner decision:**
`REJECTED_C1_RESOLVED_PATH_STRUCTURE_AND_FAILURE_LIFECYCLE_MISMATCH`

**Planner review date:** `2026-07-30`

## Reviewed scope and implementation method

The active PLAN authorized one pure-offline controller invocation against one
brand-new external root. It required exact one-read validation of four accepted
C1 evidence files, then exact one-read byte provenance for three retained-R3
artifacts, construction of one subordinate immutable manifest, a physical
terminal seal, and one post-seal `EXECUTION_RESULT.md` append.

The reviewed PLAN was `20249` bytes with SHA-256
`48ce17f7fe237d043ad840aa459904ea2b89c2a22d2c66fd059d1e0d17d23b13`.
The activation/dispatch HEAD is
`cb38ac58b35106d92ba0fa0f56151452c3b34900`; the review found a clean
worktree before Planner-owned archive/PLAN changes.

The Planner independently inspected only:

- the active PLAN and accepted C1 review archive;
- the frozen controller source at
  `/Volumes/4T/temp/rgbww-optimizer/p7-td-b-b2-corrected-controller-cb38ac5.py`;
- the existence, type, mode, identity, and direct emptiness of the failed root;
- the frozen execution counters supplied for review; and
- the existing repository `EXECUTION_RESULT.md` C1 handoff text.

The Planner did **not** invoke or retry the controller, reuse/delete/rename the
failed root, reopen any of the four C1 evidence payloads, access any retained-R3
artifact or decision source, invoke Git/controller/tests/validator/release, or
access network/devices/camera/Ray/strip/formal/public analyzer.

## Authoritative evidence and evidence strength

### Strong physical/source evidence

- Frozen controller source bytes: `29841`; SHA-256
  `da9055626eac266f0eb983e713f246b18bdf26f7443a30d2a6f2ddb503cf3ba4`.
- Failed root:
  `/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b2-corrected-manifest-b189117-20260730T1600Z`.
  It is a physical non-symlink directory, mode `0700`, inode `2188351`, with
  no direct child at review time.
- The frozen source implements `contains(obj, value)` as an equality search
  over every recursively walked node. It then constructs a three-string
  `expected_paths` list and requires `contains(index, expected_paths)`.
- The frozen source creates the evidence root, reads/validates all four C1
  files, and performs the over-strong list-containment assertion before any
  retained-artifact access, memory-only self matrix, or manifest write.
- Its only outer exception handler prints a JSON error to stderr and re-raises.
  It has no post-root failure terminal writer, no failure terminal seal, and no
  controller-owned ER append path.

### Frozen execution observations

The execution-owner counters are accepted as the best available invocation
record:

```text
controller invocation = 1
C1 lstat/open/read/hash = 4/4/4/4
retained lstat/open/read/hash = 0/0/0/0
self matrix = 0/12
manifest/manifest-seal/terminal/terminal-seal writes = 0/0/0/0
retry/fallback/second root = 0/0/0
network/device/scientific/release locks = 0
EXECUTION_RESULT append = 0
```

These counters agree with the source ordering and the physically empty root.
They strongly prove the failure occurred after the four C1 reads and before
retained access or persistence. Because the controller did not persist a
terminal/seal and the Executer correctly did not append an unsealed claim to
ER, the exact exception text and complete runtime environment are not durable
package evidence. That limitation is explicit and is not upgraded into a
sealed fact.

### Existing accepted C1 semantic evidence

The accepted C1 review archive states that the path-owner index contains three
resolved **items**, each carrying its own path plus
`content_identity=not_observed_by_this_package` and
`current_content_validated=false`. It does not state that the exact three-path
array is itself serialized as one nested value. Therefore requiring
`contains(index, expected_paths)` is stronger than the accepted C1 schema and
is not justified by the PLAN.

## Findings

### Finding B2-F1: resolved-path structural false rejection

The controller's `contains(index, expected_paths)` predicate succeeds only if
some recursively visited JSON node is exactly equal to the entire ordered
three-string list. It does not establish the intended contract of three exact
resolved item records; conversely, three valid item records can fail this
predicate when paths are stored individually inside those records.

The source position, frozen counters, empty root, and accepted C1 semantic
description make this the uniquely supported failure branch. The package is
therefore rejected as a controller/schema-owner mismatch, not as evidence that
C1 drifted or retained R3 is missing/corrupt.

The correction must validate the actual accepted **record semantics**:

1. discover only record-shaped nodes within the already parsed C1 index;
2. require exactly three resolved records and no fourth candidate;
3. require each exact frozen absolute path exactly once;
4. require every record to preserve
   `content_identity=not_observed_by_this_package` and
   `current_content_validated=false`;
5. reject duplicate, missing, extra, abbreviated, reordered-by-substitution,
   generic-prefix, basename, glob, parent/sibling, or fallback authorization;
6. use the PLAN-frozen exact path order for later artifact processing only
   after the record set is proven exact.

No generic recursive equality assertion over an entire synthetic list may own
this semantic boundary.

### Finding B2-F2: failure evidence lifecycle is not implementable

The PLAN required a truthful hard-failure terminal and terminal seal, but the
controller put only the success terminal path in `main()` and left the outer
exception handler as stderr-only. Thus any failure after root creation but
before success persistence necessarily leaves no durable terminal/seal, and
the post-seal ER rule necessarily leaves no handoff. The physically empty root
is the expected consequence of this source, not a storage anomaly.

The next controller source must establish a single terminal lifecycle owner
immediately after successful root creation. Every post-root body failure must
be caught by that owner, persist one truthful failure terminal containing the
stage, exception class/message, actual counters, root identity, frozen source
identity and lock zeros, then persist its physical terminal seal. Only after a
durable seal may the Executer append exactly one ER handoff. A terminal/seal
write failure must remain non-repairing and non-successful; progressive
pre-terminal evidence must make the last durable stage distinguishable without
rewriting any earlier file.

## Decision

`REF-P7-25-R2-B2` is **not accepted**. No subordinate manifest, seal, terminal,
or eligibility evidence exists. B3, canonical validator, eligibility emission,
release consumption, device work, FORMAL-R6, strip, TD-C, sentinel, and P8 stay
locked. Retained state remains `RETAINED_UNVALIDATED_UNCONSUMED`.

The safe-negative portion is accepted: the sole controller invocation stopped
before retained artifacts, validators, release, devices, or scientific work;
there was no retry/fallback/second root. The failed root is immutable failed-run
evidence and must not be reused, deleted, renamed, repaired, or populated.

This is an engineering execution-packaging defect. It presents no unresolved
color-science or measurement-science branch and no high-risk device operation;
Advisor or Human authorization is not required.

## Residual risks

- There is no sealed failure artifact from the failed invocation, so exact
  stderr text is not independently durable.
- The four C1 evidence files have already consumed the prior PLAN's exact read
  budget. The corrective package must not read them again.
- A future B2 retry may receive a newly explicit, one-time C1 read budget only
  after the controller correction is independently accepted and a new PLAN is
  activated. That later budget is not granted by this archive.
- Merely replacing list equality with three substring/path membership checks
  would be under-specified and could admit duplicate or unrelated records.
- A success-only terminal path would repeat the current evidence gap.

## Exact next branch

- Reference task: `REF-P7-25-R2-B2-C2`.
- Contract:
  `P7-TD-B-RETAINED-R3-OPTION-B-B2-C2-CONTENT-FREE-CONTROLLER-LIFECYCLE-CORRECTION-V1`.
- Single action after Orchestrator review and later PLAN-only activation:
  consume the frozen failed controller source once, create one immutable
  successor controller in a brand-new external correction root, and validate
  record-semantic path ownership plus progressive failure terminal/seal/ER
  sequencing entirely with in-memory fixtures and injected writer failures.
- C2 may not read C1 payloads, retained artifacts, or decision sources and may
  not invoke the corrected B2 controller against real inputs.
- Current stop:
  `B2_CORRECTED_FAILURE_REVIEWED_WAITING_ORCHESTRATOR_REVIEW`, with
  `execution_authorized=false`.
- Future C2 execution stop:
  `B2_C2_CONTROLLER_CORRECTION_WAITING_PLANNER_REVIEW`.

## 维护性判断

The failure comes from two responsibilities being split incorrectly: schema
structure was inferred by a generic recursive helper, while failure persistence
was outside the controller's terminal lifecycle. C2 keeps the repair external
and local to the frozen one-shot controller, establishes one record-semantic
owner and one post-root terminal owner, and adds behavior-bearing fixtures. It
does not add a repository abstraction, parallel eligibility owner, or new
scientific route.
