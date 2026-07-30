# REF-P7-25-R2-B2 modern manifest seal failure review

**Reviewed reference task:** `REF-P7-25-R2-B2`

**Reviewed contract:**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-MODERN-MANIFEST-SEAL-V2`

**Planner decision:** `REJECTED_FROZEN_RETAINED_SOURCE_PATH_ENOENT`

**Planner review date:** `2026-07-30`

## Reviewed scope and implementation method

The active PLAN authorized one pure-offline controller invocation in one
brand-new external root. Its intended action was to recompute the accepted
Git/provenance baseline, read each of the three frozen retained-R3 artifacts
exactly once, and durably create one subordinate immutable v2 provenance
manifest, one hash seal, and one terminal artifact. It explicitly prohibited a
second root, retry, fallback, path enumeration, path substitution, artifact
repair/regeneration/copy, canonical validator, eligibility, release
consumption, repository implementation edits, tests, network, devices, and all
later stages.

The reviewed active PLAN was `18476` bytes with SHA-256
`9f14f1c0e4006dfffd6f5bb3b9c070a60e45b39ab6bb7dcad53b5775c5b19cb9`.
The Planner reviewed the specified physical terminal and the sole B2 handoff
appended to `.agent-work/EXECUTION_RESULT.md`. This review did not invoke the
controller, list or read the retained package, open any retained artifact,
call Git mutation, run tests, or access network/device/scientific routes.

## Authoritative evidence

- Dispatch HEAD:
  `995633a3f671acf50f4cbbaa0837ae357ca2d41f`.
- Execution root:
  `/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b2-modern-manifest-995633a-20260730T0932Z`.
- Physical terminal:
  `/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b2-modern-manifest-995633a-20260730T0932Z/terminal-evidence.json`,
  `1517` bytes, SHA-256
  `10aef59d4b2155bf6080a5bde5fcf3925871b592a8f6ddc402358351c5ab87b7`,
  schema `p7_retained_r3_option_b_b2_terminal_v2`, status
  `hard_failure_waiting_for_planner`.
- Execution-result snapshot at review: SHA-256
  `5e85fe2df55c880354209cb31b6882772a16eaac95b542c676749747fba9944f`.
- Historical retained-package review:
  `.agent-work/PLANS/20260727-2241-p7-lineage-release-r3-r2-audit-ledger-shape-review.md`,
  `6090` bytes, SHA-256
  `90521d3e6c4461dbf1816ab894b46e33d536ba38ba47727f887d2495ab3231e6`.
- Historical exact retained-source review:
  `.agent-work/PLANS/20260727-2313-p7-retained-r3-c1r2-third-failure-reassessment-stop-review.md`,
  `9695` bytes, SHA-256
  `e02b169a9b8ec84d113461695b7d68f4552ce4f2973b982cf5589dc444c575ae`.

## Validation quality and findings

Dispatch, root creation, and the in-memory negative matrix completed. The
controller then used its only permitted `lstat` on the first frozen path:

`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-lineage-release-r3/lineage-release-161094f-c1-20260727T2103/current-lineage-candidate.json`

That exact path returned `ENOENT`. The controller correctly stopped with
retained lstat/open/read=`1/0/0`, retained bytes=`0`, completed retained
artifacts=`0/3`, manifest/hash-seal writes=`0/0`, retry/fallback=`0/0`, and no
substitute path or directory enumeration. Self/negative checks were `12/12`.
All canonical-validator, audit, consumer, replay, eligibility, release,
repository implementation, test, network, credential, device, camera, Ray,
strip, cleanup, capture, FORMAL, analyzer, TD-C, sentinel, P8, firmware, and
deployment counters remained zero.

The physical terminal is durably present, but its embedded pre-write snapshot
reports `terminal_writes=0`. This is a truthful ordering caveat rather than
proof of a successful terminal-write counter. It must remain preserved; this
review does not rewrite or normalize it.

The historical immutable reviews identify a different retained package and
source chain:

`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-lineage-release-r3/lineage-release-32b9e67-r2-20260727T2227/child-output/lineage-release-r3`

They record the expected three names and SHA-256 values, but this Planner pass
did not access that external path. Historical text is sufficient to define a
small exact path-owner verification chain; it is not sufficient to claim that
the chain currently exists or to retry the manifest seal directly.

## Decision and residual risks

B2 is rejected. No manifest or seal exists, retained R3 remains
`RETAINED_UNVALIDATED_UNCONSUMED`, and B3, eligibility, release consumption,
devices, FORMAL-R6, TD-C, sentinel, and P8 remain locked.

The only bounded successor is a pure-offline path-owner discovery/index
package. It may verify the historically named package root and only the two
explicit child directories through non-following directory identity checks and
controlled direct-entry listings. It may record artifact names, types, and
exact absolute paths, but must not open/read/hash/parse any artifact content,
run a validator/audit, or create the B2 manifest. Any mismatch stops without
searching siblings, parent directories, alternate roots, or retrying.

This is an engineering provenance/path-selection correction. Advisor color or
measurement-science guidance and Human dangerous-device authorization are not
required.

## Exact next branch

- Proposed reference task: `REF-P7-25-R2-B2-C1`.
- Contract:
  `P7-TD-B-RETAINED-R3-OPTION-B-B2-C1-PATH-OWNER-INDEX-V1`.
- Single action: verify and seal the exact retained path-owner chain and three
  resulting artifact absolute paths without reading artifact content.
- Planner stop: `B2_C1_PATH_OWNER_INDEX_WAITING_PLANNER_REVIEW`.
- A passing C1 may only return to Planner/Orchestrator for a corrected B2 seal
  plan; it does not itself authorize or perform that seal.

## 维护性判断

The correction isolates stale path selection from scientific and canonical
validation ownership. It adds no repository abstraction or parallel validator;
follow-up cleanup is unnecessary unless the path-owner evidence itself exposes
multiple ambiguous retained families.
