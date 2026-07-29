# REF-P7-25-R2-B1A-C3E6F12 review / worktree blob oracle false rejection

**Planner review date:** 2026-07-29

**Reviewed contract:**
`P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F12-CLEANUP-TEST-SUCCESSOR-PREREQUISITE-V1`

**Decision:** `rejected_worktree_blob_identity_oracle_false_rejection`

**Proposed next branch:** `REF-P7-25-R2-B1A-C3E6F13`

## Reviewed scope and evidence

Planner reviewed the active PLAN, the exact FULL machine row, the C3E6F12 handoff in
`.agent-work/EXECUTION_RESULT.md`, and every progressive/terminal artifact in the sealed root:

```text
/Volumes/4T/temp/rgbww-optimizer/
  p7-td-b-retained-r3-option-b-b1a-c3e6f12-offline/
  20260729T214215Z
```

The package passed its machine-row parser and 8/8 negative cases, the exact 12-key FULL subset,
shared HEAD/staged gates, lstat-only preflight, direct positional root transfer, exclusive `0700`
root acquisition and seal, one no-hardlink clone and detached checkout, exact parent/tree identity,
and the first observed-before-compare test-source acquisition. It then created the one fixed
same-directory temporary file, wrote the acquired 19,184 bytes, changed the mode to `0644`, fsynced
the file, proved same-filesystem placement, performed exactly one `os.replace`, fsynced the target
directory, and proved the temporary path absent.

Controller/process/invocation were `1/1/1`; retry, failed-root reuse, caller restart and alternate
root were all `0`. The single ledger contains seven actual events and derives consistent counters:
test-source read/materialization/test edit path `1/1/1`, aggregate reads/acquisitions `1/1`, with
all later fixture, AST, test, stage/commit, validator and manifest counters at `0`. All candidate,
production, retained-R3, eligibility, release, network, environment and device counters remained
`0`.

## Exact first failure

After the successful atomic replacement, the controller raised:

```text
ContractFailure: materialized target identity mismatch:
{'path': 'tests/test_measure_raw_shutter_response.py',
 'mode': '100644',
 'blob_oid': 'b6178d564a7bfdb5a218e5dddcfb0ebfbdd2bc59',
 'bytes': 19184,
 'sha256': 'f76726a0bb2ec3b9cf4daa713fd8878becae758690fbafc98b10ed2805e87fb8',
 'lstat_mode': '0o644'}
```

The materialized working-tree file is exact:

- bytes: `19184`;
- SHA-256: `f76726a0bb2ec3b9cf4daa713fd8878becae758690fbafc98b10ed2805e87fb8`;
- worktree Git blob from `git hash-object -- <path>`:
  `124b6adb449e8b93b478ce3e1facbae8437c5b53`;
- mode: `100644` / filesystem `0644`;
- changed path: only `tests/test_measure_raw_shutter_response.py`;
- staged paths: none.

The controller's shared `tracked_identity()` helper obtained `blob_oid` exclusively from
`git ls-files -s`. Before staging, that command correctly reports the index entry, which remains
the parent blob `b6178d564a7bfdb5a218e5dddcfb0ebfbdd2bc59`; it cannot report the replaced unstaged
working-tree blob. The controller therefore compared an index identity against the expected
working-tree identity and falsely rejected a correct materialization. This is an offline temporary
controller identity-oracle defect, not source drift, atomic-replace failure, test-content failure,
provenance acceptance, scientific failure or device failure.

## Frozen evidence

| Artifact | SHA-256 |
| --- | --- |
| `validation-summary.json` | `c403ab6a3a354fbcc57d23a8c50b6f4156ce731181a3a3633c615f1b0d2ca742` |
| `terminal-summary.json` | `39c81232831077194804bdd70f2532ad66f0e677c3f768495de8746ece7f093b` |
| `terminal-seal.json` | `f5bf203baac19fe33ba1cfaf274a5cbdad017aa88f53a262c65991554ff1cccf` |
| `failure-summary.json` | `9acaafe90892d29280546de6e9c501ad7ee6be573e8f803d0ab36784cb35fcee` |
| `ledger-consistency.json` | `bfb3684786b0ae05c78056d2a4b0cd44981cea526056c01e9443acfe246931a1` |
| `single-event-ledger.jsonl` | `4930ccfff55e8f515a0bdec4602aadc265e867d219fb9fd2b08af1224c9f8983` |

The terminal seal rebinds the recomputed validation and terminal-summary hashes exactly. The
ledger consistency report has no mismatches. Shared HEAD remains
`9303aa22a9bd37e8ec4f23147c78c6bea84b9a2e`; shared staged paths remain empty. Original retained
R3 remains `RETAINED_UNVALIDATED_UNCONSUMED`; rollback remains
`32b9e670ff3bbea0cd1505528c2ca87c2935446c`.

## Planner decision

**Rejected solely at the post-replacement worktree blob oracle.** C3E6F12 must not be retried,
resumed, repaired in place or reused. Its sealed root is evidence only. All completed reads and
materialization consume only this failed package's budgets and give no reusable execution budget.

The Orchestrator should activate exactly one fresh bounded successor, C3E6F13. Its only new
controller correction is to separate index identity from working-tree content identity:

1. Before replacement, prove the tracked parent through both the index owner (`git ls-files -s`)
   and independently computed worktree bytes/SHA/blob; both must equal the frozen parent facts.
2. After replacement but before staging, retain the index proof that the entry is still the frozen
   parent blob and compute the new worktree blob independently from the exact file bytes (equivalent
   to `git hash-object -- <path>` or Git blob framing over already acquired bytes). Require that
   worktree blob to equal `124b6adb449e8b93b478ce3e1facbae8437c5b53`.
3. Do not treat the pre-stage index blob as the post-replacement worktree blob. Do not stage early,
   refresh the index, use intent-to-add, or weaken any exact bytes/SHA/mode/path/diff gate.
4. Preserve the direct-root single-controller lifecycle, single-ledger accounting, five
   observed-before-compare acquisitions, semantic `config/*` ignore parser, exact closure owner and
   nested three-`ast.Div` predicate, one-path test-only commit, old canonical validator expected
   rejection, immutable unconsumable successor manifest, and every zero lock.

No Advisor scientific guidance or Human device authorization is required. The package is wholly
offline and does not alter the scientific branch.

## Residual risks and stop point

Runtime-fixture acquisition/copy, closure AST verification, pre/post tests, child commit, canonical
expected rejection and successor-manifest verification have still never been reached by this clean
single-controller route. C3E6F13 must stop at its first failure or at the prerequisite-success
Planner gate. It must not run full discovery, read retained R3, emit eligibility, consume release,
or access network/devices.

**Planner stop:** archive complete. Planner leaves the current active PLAN unchanged until the
Orchestrator records C3E6F13 as the sole active FULL reference task and authorizes a matching PLAN.
