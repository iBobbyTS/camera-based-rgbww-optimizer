# REF-P7-25-R2-B1A-C3E6F11 review / acquisition-controller KeyError + root-reuse contamination + handoff summary contradiction

**Planner review date:** 2026-07-29

**Reviewed contract:**
`P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F11-CLEANUP-TEST-SUCCESSOR-PREREQUISITE-V1`

**Decision:** `rejected_first_failure_keyerror_root_reuse_contamination_summary_contradiction`

**Next branch:** `REF-P7-25-R2-B1A-C3E6F12`（proposed to Orchestrator；FULL 当前 active 仍为 C3E6F11，Planner fail-closed 不写 PLAN）

## Reviewed scope and evidence

C3E6F11 preserved the exact backtick PLAN/FULL rows, 8/8 parser negatives, 12/12 FULL required-key
subset, and all frozen parent/tree/staged identities of C3E6F10+. Planner reviewed PLAN, FULL,
`EXECUTION_RESULT.md` C3E6F11 section, and the complete terminal evidence root at
`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b1a-c3e6f11-offline/20260729T210853Z`.

The package passed the machine parser, FULL subset check, pre-root Git identity (HEAD
`9303aa22a9bd37e8ec4f23147c78c6bea84b9a2e`, staged 0), pre-root lstat-only preflight, fresh
root creation (mode `0700`), and detached cleanroom clone/checkout at the frozen parent/tree
`c67473c6c8b4fbf799f9e74cd71f89493e18ce4d` with exact parent test identity.

## First failure: acquisition controller KeyError

The first acquisition controller invocation exited 1 with:

```text
KeyError: 'FRESH_ROOT'
```

The fresh-root path was stored in a shell variable that was not exported to the Python
subprocess environment. The controller could not resolve the `FRESH_ROOT` env var and failed
before any budgeted content read. This is a temporary-controller process-environment defect,
not a PLAN/FULL/source/fixture/test/Git/provenance or scientific failure.

## Root-reuse contamination (retry0 violation)

After the first KeyError failure, the **same** fresh root `20260729T210853Z` was reused for
a second acquisition controller invocation. This violates the PLAN contract:

> 只允许一个fresh root，retry `0`，failed-root reuse `0`

The second invocation completed **5 observed-first content acquisitions** and **3
`git check-ignore` calls**, all within the contaminated root:

### Contaminated observed records (5 records, all written after first failure)

| Record | Bytes | SHA-256 | Record SHA-256 | Match |
| --- | --- | --- | --- | --- |
| 01-test-source | 19184 | `f76726a0...5e87fb8` | `af5a1a6e...43801558` | true |
| 02-runtime-fixture-code-duty | 24058 | `0b03ce50...22ff911` | `d2d327d1...e64066a` | true |
| 03-runtime-fixture-locations | 14769 | `21f02328...a38a8f80` | `6f9fc5ee...ca454db0` | true |
| 04-closure-fixture-white-endpoints | 1483 | `050e79d0...a319e813` | `3e473514...00787244` | true |
| 05-canonical-cleanup-manifest | 2641 | `753f00f1...6ea0d0` | `56028806...74a218b6` | true |

All 5 records observed bytes/SHA-256 match PLAN expected values, but they are **tainted**:
they were produced by a retry invocation reusing the same failed root, and must not be
consumed as authoritative evidence.

### Contaminated check-ignore calls

3 `git check-ignore -v` calls were executed after the first failure within the same
contaminated session. These results are equally tainted.

## Handoff accounting contradiction

`failure-summary.json` (SHA-256 `55e4593a6851aad6f850f0a2d4fb6bebfd5643e00becfad94b12605124cc2865`)
contains an internal accounting contradiction:

| Counter | failure-summary value | Truth (from acquisition-summary.json) |
| --- | --- | --- |
| `test_source_content_reads` | **0** | **1** (record 01-test-source) |
| `runtime_fixture_reads` | **0** | **2** (records 02, 03) |
| `closure_fixture_reads` | **0** | **1** (record 04) |
| `observed_acquisitions_after_first_failure` | **5** | 5 (correct) |
| `git_check_ignore_calls_after_first_failure` | **3** | 3 (correct) |

The truthful `observed_acquisitions_after_first_failure=5` and
`git_check_ignore_calls_after_first_failure=3` confirm that 5 content reads and 3
check-ignore calls occurred. But the standard per-category counters
(`test_source_content_reads`, `runtime_fixture_reads`, `closure_fixture_reads`) are
all zero — contradicting the aggregate. The standard counters omit
`canonical_cleanup_manifest_content_reads` entirely.

This is a handoff serialization defect in the temporary controller's failure-summary
writer: the per-category counters were zeroed while the truthful aggregate counters
were preserved. The zero-values must not be trusted as evidence of zero reads.

### Terminal evidence hashes

| Artifact | Path | SHA-256 |
| --- | --- | --- |
| failure-summary.json | `.../20260729T210853Z/failure-summary.json` | `55e4593a6851aad6f850f0a2d4fb6bebfd5643e00becfad94b12605124cc2865` |
| acquisition-summary.json | `.../20260729T210853Z/acquisition-summary.json` | `a15b2e9c796576a78cb33d406dd6e2418283ebdff66f6af92170e420b8df3572` |
| terminal-summary.json | `.../20260729T210853Z/terminal-summary.json` | `d0abbf0218860bbc4908041ccdd4c56b1f81e1f0acc61f898757599618f6cd21` |
| validation-summary.json | `.../20260729T210853Z/validation-summary.json` | `48da6125633a2eafcdc2fa89a3db7dd215a8a16162e146624e65f6b673cbc9ca` |

## Strict counters

Fresh root `1` (acquired before first read, correct). Failed-root reuse `1` (violation).
Retry count `1` (violation). Clone/checkout `1/1`.

All post-acquisition steps were aborted by the Orchestrator: fixture copy, closure AST,
test materialization, pre/post tests, stage, external commit, canonical validator,
successor manifest write/verifier — all `0`.

Candidate reads/materialization, production edits, shared stage/commit, original-R3 reads,
real audit, eligibility, consumer, release consumption: all `0`.

Network, DNS, `.env`, credential, device, camera, Ray, strip, cleanup, capture, public
analyzer, FORMAL, firmware, deployment: all `0`.

Shared HEAD remained `9303aa22a9bd37e8ec4f23147c78c6bea84b9a2e`; shared staged paths `0`;
no shared Git mutation attempted. Original retained R3 remains
`RETAINED_UNVALIDATED_UNCONSUMED`.

## Planner decision

**Rejected.** Three independent defects converge in one terminal:

1. **Pre-acquisition controller KeyError**: `FRESH_ROOT` env var not exported to Python
   subprocess — environment plumbing defect.
2. **Root reuse retry0 violation**: same failed root reused for second controller
   invocation — lifecycle defect.
3. **Handoff summary contradiction**: `failure-summary.json` per-category counters (`0`)
   contradict truthful aggregate counters (`observed_acquisitions_after_first_failure=5`)
   and `acquisition-summary.json` evidence — serialization defect.

The contaminated root `20260729T210853Z` must never be consumed as authoritative evidence.
A new fresh root is required for any re-dispatch. The machine parser, pre-root gates, clone,
and checkout logic remain valid and replayable.

## Proposed next branch: C3E6F12

FULL is still `REF-P7-25-R2-B1A-C3E6F11` active; Planner fail-closed — does not write PLAN.
Proposed C3E6F12 contract to Orchestrator:

### C3E6F12 minimum correction

1. **Root value must be passed as verified direct literal/argv**, not via unexported shell
   variable. The controller must receive the fresh-root path through an explicit Python
   argument (`sys.argv`) or a verified exported environment variable whose presence and
   value are proven before the subprocess call. Single controller invocation, one fresh
   root, first-failure stop — no same-root retry permitted. The controller must hard-fail
   at the first non-zero exit without re-invoking.

2. **Terminal counters must truthfully reflect all content reads**: `test_source_content_reads=1`,
   `runtime_fixture_reads=2`, `closure_fixture_reads=1`,
   `canonical_cleanup_manifest_content_reads=1`. The failure-summary writer must derive
   per-category counters from the same acquisition evidence that drives the aggregate,
   and must hard-fail if any per-category counter contradicts its corresponding aggregate.

3. **Preserve exact nested AST** (left-associated three-node `ast.Div` chain, pure
   structural check, no `literal_eval`/compile/execute), **atomic replacement** protocol,
   all C3E6F10-accepted gates (structured `git check-ignore -v` semantic rule parser that
   separates `config/*` pattern from volatile `.gitignore` line numbers, exact tracked
   closure-owner path, acquisition-first observed-record protocol, 12-key FULL required
   subset), and all hard locks.

4. No Advisor or Human authorization required. Do not modify GUIDE, FULL, ER, debug,
   production, or tests. Do not commit.

### Residual risks

- The C3E6F11 root-reuse and summary-contradiction defects are both in the temporary
  controller's process-management and serialization layers. The underlying PLAN/FULL
  contracts, source identities, fixture contents, and frozen parent/tree remain exact.
- C3E6F12 is the first package that must exercise the C3E6F10-accepted nested three-node
  `ast.Div` predicate, which has never been successfully executed by a controller. If the
  predicate shape is still misaligned, the terminal will be a clean first-failure AST gate
  rather than another lifecycle or serialization defect.
