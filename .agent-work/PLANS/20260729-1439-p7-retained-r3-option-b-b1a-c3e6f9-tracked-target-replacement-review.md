# REF-P7-25-R2-B1A-C3E6F9 review / tracked-target materialization hard failure

**Planner review date:** 2026-07-29

**Reviewed contract:**
`P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F9-CLEANUP-TEST-SUCCESSOR-PREREQUISITE-V1`

**Decision:** `rejected_tracked_target_direct_exclusive_create`

**Next branch:** `REF-P7-25-R2-B1A-C3E6F10`

## Reviewed scope and evidence

C3E6F9 retained the exact machine rows, required FULL subset, structured ignore diagnostic,
exact tracked closure owner, structural AST predicate, five-read acquisition-first protocol
and accepted non-self-referential prerequisite topology. Planner reviewed PLAN/FULL, the
latest C3E6F9 execution handoff entry, terminal summaries and active debug record.

The package passed parser/FULL/root/clone/checkout, all five observed-first acquisitions and
comparisons, exact closure-owner path/blob/bytes/SHA and the structural AST predicate. The
frozen parent/test-source identities and both diff representations also matched.

The first failure occurred when the temporary controller tried to materialize corrected bytes
by opening the already tracked checkout target with `O_EXCL`:

```text
tests/test_measure_raw_shutter_response.py
```

Because a detached checkout necessarily contains that verified parent file, exclusive create
correctly raised `FileExistsError`. Exclusive create is appropriate for new evidence records,
not replacement of an existing tracked target. No direct truncation or fallback occurred.

The terminal root is:

```text
/Volumes/4T/temp/rgbww-optimizer/
  p7-td-b-retained-r3-option-b-b1a-c3e6f9-offline/
  20260729T203140Z
```

Strict terminal counters: fresh root `1`, retry `0`, test-source read `1`, runtime reads `2`,
closure read `1`, canonical first acquisition `1`, and therefore five acquisitions complete.
Test materialization/edit paths, runtime copies, pre/post/full tests, stage, external commit,
canonical validator, successor manifest and verifier were zero. Candidate, production,
shared Git, retained R3, audit, eligibility, consumer, release, network, DNS, `.env`,
credentials, device, camera, Ray, strip, cleanup, capture, analyzer, FORMAL, firmware and
deployment counters were zero.

Evidence hashes:

- `validation-summary.json`:
  `76b04aef9d7bda8434fece6af216cd32754a823996dc70d24ca42abf7cd36a6e`;
- `terminal-summary.json`:
  `25091299b5ec26231521547552fe62f14271dddc2fad542bbc9f72aedc45613a`;
- execution handoff file:
  `3bdf89f8d906aa801b67e6cc01badc7336ad4c0b11f515f63f2cef50431fcfeb`.

Shared HEAD remains `9303aa22a9bd37e8ec4f23147c78c6bea84b9a2e`; staged paths remain zero.

## Decision

C3E6F9 is rejected at tracked-target materialization. Its five acquisitions and prior gates
are terminal historical evidence only; no budget transfers. The root must remain read-only
and must not be resumed, repaired or reused.

The one-path child, old-validator expected rejection and immutable/unconsumable successor
manifest topology remains unchanged. Production validator binding remains a later package.

## Exact next branch

C3E6F10 starts from one new fixed container and fresh root. Its only controller correction is
one atomic replacement of the exact tracked test target after verifying parent target mode,
bytes, SHA and blob. It must:

1. create exactly one fixed-rule, collision-free same-directory temporary path using
   `O_CREAT|O_EXCL|O_NOFOLLOW` and mode `0600`;
2. write only the already acquired in-memory corrected bytes, `fchmod` to the verified parent
   mode `0644`, then file-fsync and close;
3. verify the temp remains a regular non-symlink on the same filesystem as target/parent;
4. call `os.replace(temp, exact_target)` exactly once;
5. fsync the containing directory;
6. verify temp absent and target regular/non-symlink with expected final mode, bytes, SHA and
   Git blob OID;
7. prove the worktree changed-path set is exactly
   `tests/test_measure_raw_shutter_response.py` and staged paths remain zero.

The replacement must preserve the verified parent target mode (`100644`). Direct truncate or
in-place write, cross-filesystem temp/move, random fallback name, collision retry, second
materialization, second replace or alternate target is prohibited. Any preexisting temp,
collision, mode/identity drift, replace failure, residual temp or extra changed path hard-fails.

Every other C3E6F9 rule remains unchanged: exact rows/FULL subset, structured ignore, exact
closure owner and structural AST, fresh-root-first five acquisitions, one-path child,
canonical expected rejection, immutable unconsumable successor manifest and all zero locks.
C3E6F9 must not be retried. No Advisor or Human authorization is required.

## Residual risks

- No pre/post test, child commit or successor manifest has yet completed.
- Full clean-room discovery and production validator binding remain incomplete.
- Original retained R3 remains `RETAINED_UNVALIDATED_UNCONSUMED`; rollback remains
  `32b9e670ff3bbea0cd1505528c2ca87c2935446c`.

**Planner stop:** archive complete. Activate only C3E6F10 after Orchestrator synchronizes its
required FULL machine state.
