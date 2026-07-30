# REF-P7-25-R2-B2-C4-P1-C1 implementation review archive

**Planner review date:** `2026-07-30`

**Reviewed reference task:** `REF-P7-25-R2-B2-C4-P1-C1`

**Reviewed contract:**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-C4-P1-C1-EXACT-PREPARATION-CORRECTION-V1`

**Decision:** `ACCEPTED_COMPLETE_WAITING_ORCHESTRATOR_PROVENANCE_BINDING`

**Merge readiness for this bounded correction:** `mergeable`

**Exact reviewed stop:**
`B2_C4_P1_C1_ACCEPTED_WAITING_ORCHESTRATOR_PROVENANCE_BINDING`

## 1. Reviewed scope and repository topology

The reviewed implementation successor is
`4678a3e6f93704912952776bc11fa2b0945d80b1`, with direct parent
`a99292e3cc75345d3c783131fd4c716b8fe698f7`. The parent is the PLAN-only
activation commit whose direct parent is the retained P1 implementation
`ce096155227d4f24f1d6659550319aaf335d014b`; the P1 implementation therefore
remains an exact ancestor.

The successor has exact subject
`fix(p7): harden retained r3 preparation invariants`, commit count `1` from its
dispatch parent, and exactly these two changed paths:

```text
src/camera_based_rgbww_optimizer/utils/p7_retained_r3_controller_preparation.py
tests/test_p7_retained_r3_controller_preparation.py
```

Current file identities independently matched the Executer handoff:

| Path | SHA-256 |
| --- | --- |
| `src/camera_based_rgbww_optimizer/utils/p7_retained_r3_controller_preparation.py` | `882f3819d161369012ce7fcd52cb1de1b9c56e4e1f821ff4554f6a1d8340738b` |
| `tests/test_p7_retained_r3_controller_preparation.py` | `80ef2bead548856031c6d6f07f4ee0b6c74b8b917a45787e9f96fbf57b4d4527` |

There is no implementation-scope worktree drift. The only pre-review dirty path
was the truthful Executer append in `.agent-work/EXECUTION_RESULT.md`; it is not
part of the focused implementation commit and was preserved.

## 2. Implementation method and independent static review

The correction stays in the single pure preparation owner and its dedicated
test owner. Planner used CodeGraph before source inspection, then independently
reviewed the exact successor diff, commit graph, changed-path set, current file
hashes, helper AST and dedicated-test AST. Tests were not rerun in this review,
and no historical external evidence root or device/network path was accessed.

The five frozen semantic gaps are closed as follows:

1. **Type-exact key/type/value target binding — accepted.**
   `validate_terminal_seal` requires `target` to be an exact `dict`, requires
   its key set to equal the five-key `SealTargetIdentity` mapping, and requires
   both `type(actual) is type(expected)` and exact value equality for every
   field. Bool/int, integral-float/int, string/numeric coercions, missing keys
   and extra keys therefore fail closed with `terminal_target_mismatch`.
2. **Complete unique regular-function owner — accepted.**
   `_regular_function_owner` walks the complete explicit-parent chain, records
   every enclosing regular `FunctionDef`, rejects zero or multiple regular
   owners, and rejects any `AsyncFunctionDef` or `Lambda` boundary. Valid nested
   statements within one regular owner remain supported, while
   `locate_owned_statement_pair` still requires immediate same-list adjacency
   and the same unique owner for both statements.
3. **Recursive immutable snapshot — accepted.**
   `_freeze_json` recursively copies exact JSON dictionaries into
   `MappingProxyType`, lists into tuples, and preserves only JSON scalars. The
   internally token-gated `_ValidatedSealGate` freezes the strict-reloaded
   payload before callback visibility; the separate `SealTargetIdentity` is a
   frozen dataclass containing validated scalar fields.
4. **Pre-sort typed replacement validation — accepted.**
   `replace_byte_spans` first materializes the iterable, maps non-iterable
   `TypeError` to stable `invalid_replacement`, rejects empty sets, then requires
   every entry to have exact type `SourceReplacement` before the sort key can
   dereference `.span`. Existing range, order, overlap and parse/compile checks
   remain intact.
5. **Accurate `ImportFrom.module` guard — accepted.**
   The dedicated static test derives `Import` roots from alias names and
   `ImportFrom` roots from `node.module`. Independent AST inspection found only
   `__future__`, `ast`, `dataclasses`, `hashlib`, `json`, `re`, `types` and
   `typing`; no forbidden root or helper literal longer than 1000 bytes exists.

The dedicated test AST contains `21` behavioral test methods and the named
regressions for all five corrections. No new eligibility, release, filesystem,
network, process, environment or device owner was introduced.

## 3. Validation evidence reviewed

The Executer handoff records these ordered gates:

| Gate | Reported result |
| --- | --- |
| dedicated preparation suite, precommit | `21/21`, exit `0` |
| exact-five related suite | `11/11`, exit `0` |
| retained-release-audit related suite | `21/21`, exit `0` |
| full suite | `712/712`, exit `0`, `175.951s` |
| compileall | exit `0` |
| CodeGraph sync | exit `0`, `Already up to date` |
| precommit diff/path gate | exit `0`, exact two paths |
| dedicated preparation suite, postcommit | `21/21`, exit `0` |
| postcommit diff/drift gate | exit `0`, implementation drift `0` |

Planner did not rerun these commands, as required by the review package. The
reported counts are supported by the bounded ER handoff; semantic acceptance is
based additionally on the independent current-code and exact-diff inspection
above. Current `git diff --check` also produced no finding.

## 4. Findings and disposition

| Finding | Prior status | Current evidence | Decision |
| --- | --- | --- | --- |
| `REV-P1-001` exact target identity | open | exact key/type/value comparison plus negative regressions | closed |
| `REV-P1-002` complete unique owner | open | full ancestor traversal, alternate-boundary rejection, nested-owner regression | closed |
| `REV-P1-003` deep immutable gate | open | recursive detached freeze plus outer/nested mutation regressions | closed |
| `REV-P1-004` typed malformed replacement | open | materialize/type-check before sort/dereference plus stable-error regressions | closed |
| static `ImportFrom.module` guard | open | corrected AST branch plus independent import-root inventory | closed |

No new `Must Fix` or accepted `Should Fix` finding remains in this bounded
correction. No scientific or Human device decision is implicated.

## 5. Residual risk and exact next branch

This helper is still a preparation owner, not the canonical eligibility owner,
and is not yet integrated into a newly provenance-bound C4 package. The current
successor commit must first be bound into the Orchestrator-owned exact provenance
route. That engineering decision may select the smallest independent C4
integration/preparation package, but it must not infer permission to read old C4
roots, invoke real B2, inspect retained R3, call the canonical validator, emit
eligibility, consume a release or access devices.

The active PLAN is therefore rewritten as a non-executable Orchestrator decision
gate. `execution_authorized=false`; only the Orchestrator may update
`FULL_PLAN_REFERENCE.md`, bind the successor provenance and request a new Planner
package. The unique stop is
`B2_C4_P1_C1_ACCEPTED_WAITING_ORCHESTRATOR_PROVENANCE_BINDING`.

## 维护性判断

The correction keeps AST selection, canonical seal validation and callback gate
ownership cohesive in one pure module with one dedicated behavioral test owner.
It adds no parallel validator or execution framework; no follow-up refactor is
needed before the Orchestrator-owned integration decision.
