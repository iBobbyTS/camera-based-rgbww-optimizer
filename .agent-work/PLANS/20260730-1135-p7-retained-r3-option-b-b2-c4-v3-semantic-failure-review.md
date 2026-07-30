# REF-P7-25-R2-B2-C4 V3 semantic failure review

**Review date:** `2026-07-30`

**Reviewed contract:**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-C4-AST-SPAN-SUCCESSOR-QUALIFICATION-V3`

**Planner decision:**
`REJECTED_TRANSFORM_PRECONDITION_LINE_ONLY_STATEMENT_CONTAINMENT`

**Exact next branch:**
`REF-P7-25-R2-B2-C4-C1` — one content-free byte-span statement-selector
correction; it remains unauthorized until a later PLAN-only activation.

## Reviewed scope and method

The review was limited to the active PLAN, the sole new ER handoff, the five
durable files beneath exact root
`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b2-c4-ast-span-successor-da90556-r3-20260730T1730Z`,
and the sole frozen builder
`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-b2-c4-ast-span-successor-builder-v3.py`.
Planner did not rerun the wrapper or builder, reopen C3 or the frozen controller,
read C1/C2/retained/decision inputs, generate a successor, run tests or the
canonical validator, consume a release, or access network/devices.

Planner independently checked physical file type, bytes, mode and SHA-256;
strictly parsed the progressive/terminal/seal JSON; compared their ordered
counters and stage transitions; and inspected the frozen builder implementation
that raised the sealed error. This evidence is sufficient to distinguish the
four possible failure classes without guessing or reopening a consumed input.

## Exact evidence

| Artifact | Bytes | Mode | SHA-256 |
| --- | ---: | ---: | --- |
| `progressive-00-root-created.json` | 1558 | `0600` | `8d4cff7212cf5c8615e411ee19dcb93ffa47664c294f8348796689277f75a219` |
| `progressive-01-c3-index-accepted.json` | 3830 | `0600` | `cb78f46f84f832ff701059cf235b67c742e91062df0f12da24a3a4204bee29eb` |
| `progressive-02-source-revalidated.json` | 2563 | `0600` | `2e94fa3740a8298349bc589808d28fa10e1b32a3fa84ee287d9432b1b077e56c` |
| `terminal-evidence.json` | 1869 | `0600` | `6b88723d8fca83bb7836a1a9adf1b3ab72fd23fe8b5b8625d5a7e8d73253fbee` |
| `terminal-evidence.sha256.json` | 285 | `0600` | `663a63e3191260d710abfb1bc831d13c7045408321c7fee1a504e8c48a9649d3` |
| frozen V3 builder | 21474 | `0644` | `df0020d9aa7c902cdd11bb6d5c52b80dabce01b31693808a60035a900dc68e37` |

The terminal seal binds the exact terminal bytes/hash, status
`hard_failure_waiting_for_planner`, and `terminal_write_returned=true` while
remaining `not_self_attested`. Dispatch HEAD is
`c9f6a9391cf76ef54d9cae003623f897dfb516c6`; pre-HEAD self-check is `8/8`;
C3 exact entries are `9`, exact content reads are `6`, and the source
lstat/open/read/hash/decode/tokenize/parse counts are each `1`.

## Finding and decision basis

`progressive-02-source-revalidated.json` was durably written before the failure.
It proves all four selectors have cardinality one; the module/main/predicate/
guard/mkdir normalized AST hashes matched the accepted C3 index; and the
main/predicate/guard/mkdir physical byte-span hashes matched that index. The
source identity also remained exact. Therefore this is not an accepted-C3
field-interpretation failure, a normalized-AST hashing failure, or a byte-offset
mapping failure.

The next frozen builder operation creates `containing` from direct
`main_node.body` statements using only
`statement.lineno <= mkdir.lineno` and
`statement.end_lineno >= mkdir.end_lineno`, then raises exact
`RuntimeError: mkdir statement cardinality` when that line-only relation is not
unique. It does not use the already validated `mkdir` byte span or each
statement's start/end columns. The sealed terminal reports that exact error at
stage `source_revalidated`, before successor generation. This is a local
transform-precondition defect: line containment is weaker than physical byte
containment and is ambiguous for legal same-line statement layouts.

C4 V3 is therefore rejected. C3 remains accepted only as
`ACCEPTED_EXACT_SOURCE_STRUCTURE_INDEX_ONLY`; no scientific contract or
retained-R3 state changes. Successor generation/write/seal, delta/seal,
compile/delegation and lifecycle matrix are respectively `0/0/0`, `0/0`, `0`,
`0`, and `0/12`. Retry/fallback/second builder/root/successor and all real B2,
validator, eligibility, release, network/device/scientific operations are zero.
Retained R3 remains `RETAINED_UNVALIDATED_UNCONSUMED`.

## Residual risk and exact next branch

The durable evidence proves the defect class and exact faulty builder block,
but it does not prove a replacement selector. The smallest safe next package is
content-free: consume only the five C4 V3 durable files and frozen V3 builder,
mechanically replace the line-only block with one byte-span containment helper,
and qualify that same helper against synthetic same-line, nested and ambiguous
cases. It must not read C3/source/C1/C2/retained/decision inputs and must not run
the corrected builder. A later Planner review is required before any actual C4
successor attempt.

Real B2, B3, retained R3, canonical validator, eligibility, release consumption,
devices, FORMAL-R6, strip, TD-C, sentinel and P8 remain locked.

## Validation quality

This review is based on immutable physical terminal/seal evidence, an ordered
durable progressive immediately before the failing operation, exact counters,
and the exact frozen source of the raising builder. It directly identifies the
failed precondition but intentionally does not claim that an unexecuted
correction works. That remaining claim is assigned to the next content-free
package.

