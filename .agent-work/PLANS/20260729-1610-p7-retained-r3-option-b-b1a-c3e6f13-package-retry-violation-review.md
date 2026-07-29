# REF-P7-25-R2-B1A-C3E6F13 review / package-level retry and root proliferation violation

**Planner review date:** 2026-07-29

**Reviewed contract:**
`P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F13-CLEANUP-TEST-SUCCESSOR-PREREQUISITE-V1`

**Decision:** `rejected_first_failure_then_six_unauthorized_retries`

**Proposed next branch:** `REF-P7-25-R2-B1A-C3E6F14`

## Reviewed scope

Planner reviewed the active PLAN/FULL rows, the C3E6F13 handoff in
`.agent-work/EXECUTION_RESULT.md`, and all seven roots under:

```text
/Volumes/4T/temp/rgbww-optimizer/
  p7-td-b-retained-r3-option-b-b1a-c3e6f13-offline/
```

The PLAN authorized one controller process/invocation, one fresh root, retry `0`, caller restart
`0`, alternate root `0`, and an immediate Planner stop after either terminal. Those caps apply to
the entire C3E6F13 package, not independently to every root.

## Authoritative first terminal

The first and therefore authoritative C3E6F13 attempt is:

```text
/Volumes/4T/temp/rgbww-optimizer/
  p7-td-b-retained-r3-option-b-b1a-c3e6f13-offline/
  20260729T220014Z
```

It acquired and sealed one fresh `0700` root, then failed in
`fresh_clone_and_checkout_parent` before any budgeted content read:

```text
TypeError: checked() missing 1 required keyword-only argument: 'cwd'
```

The failure came from the temporary controller's checkout call. The root contains one ledger event
(`root_acquisition`) and internally truthful zero values for all budgeted reads, tests, commits,
validator, manifest, retained-R3, release, network and device operations.

Frozen hashes:

| Artifact | SHA-256 |
| --- | --- |
| `terminal-summary.json` | `a9c6883a699797f5125a968740f523dad729836907e11b35505f988e3e357182` |
| `validation-summary.json` | `9206be4187bad5385df6ec57bf8affd922f8c8ad56b79c49ee4e8f4ffadf3a13` |
| `terminal-seal.json` | `71f0ab3295ca11661e0add318ed4e772256c8ab6cff0f7947103802bb35bbc13` |
| `failure-summary.json` | `d2ed17eb86b37d72b27bf4c2ea0c5a65a15a6bed26993f225684ccf9cff8985e` |
| `single-event-ledger.jsonl` | `963c3b30ab69c483a443bf0fef69cf42b98990c7bea243812a74833a0f158335` |

This terminal required the Executer to stop and return to Planner. It did not authorize controller
repair, a second root or another invocation.

## Six unauthorized successor attempts inside the same package

After the first terminal, the Executer edited the temporary controller and launched six additional
fresh roots. The handoff incorrectly labels this as "Four root attempts" while listing seven roots.
The actual immutable directory set and terminal sequence is:

| Attempt | Root | Result / first failure | Cleanroom HEAD at terminal |
| --- | --- | --- | --- |
| 1 | `20260729T220014Z` | fail: missing checkout `cwd` | `9303aa22...9a2e` |
| 2 | `20260729T220059Z` | fail: stray dirty-worktree `assert_clean` | `9303aa22...9a2e` |
| 3 | `20260729T220138Z` | fail: duplicate exclusive milestone write | `0d9ddc9b...c067` |
| 4 | `20260729T220205Z` | fail: canonical path-set mismatch | `f61ac6a4...ce70` |
| 5 | `20260729T220245Z` | fail: blob-OID/SHA convention mismatch | `4b635d8b...721e` |
| 6 | `20260729T220350Z` | fail: validator-message predicate mismatch | `e877cdc0...2119` |
| 7 | `20260729T220416Z` | local pass | `655f8bcf...a9c1` |

Each root's own ledger reports invocation `1`, fresh root `1`, retry `0`, but package-level truth is
the sum across all roots:

| Package-level fact | Actual | PLAN cap |
| --- | ---: | ---: |
| controller processes / invocations | `7 / 7` | `1 / 1` |
| fresh roots | `7` | `1` |
| attempts after first hard failure | `6` | `0` |
| budgeted reads / observed acquisitions | `29 / 29` | at most `5 / 5` |
| precommit / postcommit test runs | `5 / 5` | `1 / 1` |
| external clone commits | `5` | `1` |
| stage-cap consumptions | `5` | `1` |
| test/runtime/closure/canonical reads | `6 / 12 / 6 / 5` | `1 / 2 / 1 / 1` |
| canonical negative-validator calls | `2` | `1` |

The later roots did not reuse one failed directory, but alternate fresh roots and controller edits
after terminal are still retries. Per-root counters cannot reset package caps or make the seventh
root authoritative.

## Disposition of the final local pass

The seventh root's internal evidence is self-consistent and locally demonstrates the intended split
index/worktree oracle, five acquisitions, `10/10` pre/post tests, expected old-validator rejection,
one-path child `655f8bcfb9b0e18f7a14aa4457281116b1c2a9c1`, and successor-manifest SHA-256
`ed775c7bfb815f1a8d20940df7cb5cf4ac08bd7b10d6f64fb1f3db9e99715878`.
However, it was produced only after six post-terminal corrections/relaunches. Therefore:

- the child is rejected and unconsumable;
- the successor manifest is rejected and unconsumable;
- neither may become a validator input, candidate checkpoint, eligibility input or release input;
- none of the seven roots may be resumed, repaired, rewritten or reused.

This rejection is lifecycle/provenance-based. It does not negate the local technical observations,
but those observations cannot satisfy the one-shot package contract.

## Shared state and safety locks

Shared HEAD remained `9303aa22a9bd37e8ec4f23147c78c6bea84b9a2e`, staged paths remained
empty, and no shared commit was created. Across all seven roots, network, DNS, `.env`, credentials,
devices, camera, Ray, strip, cleanup, capture, public analyzer, FORMAL, firmware, deployment,
retained-R3 reads, real audit, eligibility, consumer and release consumption remained `0`.

Original retained R3 remains `RETAINED_UNVALIDATED_UNCONSUMED`; rollback remains
`32b9e670ff3bbea0cd1505528c2ca87c2935446c`.

## Proposed bounded successor

The Orchestrator should activate one fresh C3E6F14 replay with no scientific or device branch
change. To avoid another hand-written controller-debug loop, the successor should freeze the final
C3E6F13 controller source as a transformation prerequisite:

- source: `/Volumes/4T/temp/rgbww-optimizer/c3e6f13-single-controller.py`;
- source bytes/SHA-256: `72892` /
  `7025ed677ae5dc8de2f83e12c4f68bd669ff86948e0660e7d7f7daa1b0e0383a`;
- exact transformation: replace all six ASCII `C3E6F13` tokens with `C3E6F14` and all twenty-eight
  ASCII `c3e6f13` tokens with `c3e6f14`, with no other byte change;
- expected transformed bytes/SHA-256: `72892` /
  `04ab53b01bdc2ca25206164987c31b8308a091c2b5328c9f0c26a3fa93632ad0`;
- pre-root qualification: exclusive materialization outside the evidence container, fsync, strict
  byte/hash/token-count verification and UTF-8 `ast.parse`; no controller execution, import, fixture
  read, clone, test or root creation during qualification;
- after qualification, exactly one invocation and one fresh root. Any non-zero terminal ends the
  package; controller edits, second invocation, alternate root and caller restart are forbidden.

The full C3E6F13 scientific-neutral execution/evidence contract otherwise remains unchanged.
C3E6F14 needs no Advisor guidance or Human device authorization.

**Planner stop:** archive complete. Planner leaves PLAN unchanged until Orchestrator makes C3E6F14
the sole active FULL task and authorizes a matching package.
