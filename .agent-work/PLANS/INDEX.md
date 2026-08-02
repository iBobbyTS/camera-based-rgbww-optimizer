# Planner Archive Index

Last updated: 2026-08-01 22:10 MDT

Reference commit: `be8c4cdf75e447d128e3c7283cf5b3916d85d1cf`

## Authority

This index routes readers to immutable Planner archives. It does not replace an
archive, change a decision, authorize execution, or make a FULL route
executable. The directory contains 407 Markdown archives including the recovery
retirement archive. Exact inventory is always the tracked path set under
`.agent-work/PLANS/`.

## Current recovery anchor

- `20260801-2152-p7-orchestration-recovery-draft-retirement.md` retires the
  unexecuted JSON-projection draft as
  `RETIRED_HISTORICAL_SUPERSEDED_WAITING_DRAFT` and binds its original blob,
  bytes, SHA-256, ref, and contract.
- Current PLAN state is `NO_ACTIVE_EXECUTABLE_PLAN_WAITING_NEW_GOAL`.
- Canonical next placeholder is `REF-P7-RECOVERY-NEXT-GOAL`; it is not an active
  task or an execution package.

## Scientific and retained-release anchors

| Class | Archive | Durable fact |
| --- | --- | --- |
| scientific result | `20260727-2017-p7-eq-r6-qualified-1-2500-acceptance-review.md` | EQ-R6 State C `1/2500` accepted |
| retained checkpoint | `20260727-2103-p7-lineage-release-r3-preacquisition-manifest-review.md` | retained-R3 lineage/release checkpoint history |
| release reality | `20260730-2228-p7-retained-r3-provenance-io-p3-c2-c1-acceptance-review.md` | implementation accepted; retained R3 still unvalidated/unconsumed |

## Accepted repo-owned boundaries

| Boundary | Acceptance archive |
| --- | --- |
| preparation owner | `20260730-1247-p7-retained-r3-option-b-b2-c4-p1-c1-implementation-review.md` |
| integration qualification | `20260730-1346-p7-retained-r3-option-b-b2-c4-p2-c4-integration-qualification-review.md` |
| provenance I/O | `20260730-2228-p7-retained-r3-provenance-io-p3-c2-c1-acceptance-review.md` |
| controller conformance | `20260731-1351-p7-retained-r3-b2-p4-c1-c1-c1-provenance-closure-review.md` |
| controller runtime | `20260731-1537-p7-retained-r3-b2-p5-runtime-owner-review.md` |
| runnable domain template | `20260731-1921-p7-retained-r3-b2-p7-acceptance-route-review.md` |
| real-manifest Git grammar | `20260801-0135-p7-retained-r3-b2-m1-i1-c1-git-grammar-acceptance-review.md` |
| offline patch preflight | `20260801-0824-p7-retained-r3-b3-c3-c4-r1-owner-acceptance-review.md` |
| subordinate self-check | `20260801-0955-p7-retained-r3-b3-c3-c4-r3-c1-r1-c1-sequence-correction-review.md` |
| machine-row parser | `20260801-1231-p7-retained-r3-machine-row-parser-acceptance.md` |
| real-manifest seam implementation | `20260801-1340-p7-retained-r3-r2-r1-c2-s1-c1-r1-git-stdout-review.md` |

Acceptance applies only to the archive's stated implementation/authority. A
subordinate or synthetic owner does not emit eligibility or make the retained
release consumable.

## Rejected and historical-only routes

- C3E6F17 and C3E6F19 numeric corrective chains are historical controller-loop
  evidence. Accepted helper facts inside them remain usable only through their
  accepted repo-owned commit; the branch itself is not resumable.
- B2 external-controller failures culminate in
  `20260731-1106-p7-retained-r3-b2-owner-api-controller-architecture-review.md`.
  That archive is the ownership reassessment anchor; failed external sources and
  roots must not be rerun.
- B3 marker/bytes/effect-order/EOF/attribution/spec-diagnostic successors are
  rejected or historical-only according to their individual review. The last
  reviewed failure is
  `20260801-2028-p7-retained-r3-spec-contract-serialization-failure-review.md`.
- S1/R1/D1/D2 packages that only seal EOF, supersession, or synthetic
  attribution preserve evidence but do not advance retained status.

## Lookup protocol

1. Start from this class index, then open only the named archive.
2. Verify exact historical content with `git log -- <archive>` and
   `git show <commit>:<archive>`; use `shasum -a 256` for the worktree copy.
3. Follow an archive's evidence commit into `.agent-work/EXECUTION_RESULT.md`
   through `.agent-work/EXECUTION_RESULT_INDEX.md`.
4. Never infer current authority from an archive filename, old `active` text, or
   task-ID depth. Only a future active PLAN may authorize work.
