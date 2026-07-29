# REF-P7-25-R2-B1 Option B feasibility review

**Planner decision:** `ACCEPTED_BLOCKED_CONTRACT_CONFLICT`

**Review date:** 2026-07-29

**Reviewed contract:**
`P7-TD-B-RETAINED-R3-OPTION-B-B1-CLEANROOM-FEASIBILITY`

**Reviewed PLAN SHA-256:**
`621b7060665e9ce0351482b1928a16df18aa5f90c318f08f61bd65440ca02522`

## Reviewed scope and method

B1 was a pure-offline feasibility package. It could statically inspect the
existing canonical lineage validator and release caller, but it could not run
tests, helper/audit/validator/consumer/replay, read retained R3 payloads, edit
the two-file repair, stage/commit, write the final manifest, or perform any
network/device/formal operation. A clean-room could be acquired only after the
canonical subordinate-manifest seam passed.

The Executer used one CodeGraph read and bounded raw-source evidence over two
files (`693/700` lines), preserved the shared worktree, and sealed one exact
eight-artifact evidence package. It stopped before clean-room acquisition when
the seam was disproved.

## Evidence accepted

Evidence root:

```text
/Volumes/4T/temp/rgbww-optimizer/
p7-td-b-retained-r3-option-b-b1-feasibility-20260729T0901
```

Canonical summaries:

- `06-validation-summary.json`, SHA-256
  `363967849eedbf2c6e7051e8bdadb720f887e72dec3556a24f8218fecb699576`;
- `07-terminal-summary.json`, 2219 bytes, mode 0600, link count 1,
  SHA-256
  `d741b3d7a287a9b7662a3f82deb830cda3bfac90ecba30e747a1b4ee23b87746`;
- Executer handoff `.agent-work/EXECUTION_RESULT.md`, SHA-256 at review
  `10d459d6f7c31c1492e8a03a7b1bd4575b48be8167e77bb31fb288c0edfa8fd9`.

Independent review confirmed:

- all eight JSON files strict-load with duplicate-key/non-finite rejection;
- terminal references all seven preceding artifacts by exact path, bytes,
  SHA-256, 0600 mode and link count 1;
- evidence status is consistently `blocked_contract_conflict`;
- shared worktree before/after is exact excluding the required later ER append;
- target hashes, numstat, parent/target blob OIDs, HEAD/parent/tree and staged
  zero all match PLAN;
- clean-room root is absent and clone/checkout/materialization are `0/0/0`;
- tests, compileall, imports, helper, audit, canonical validator, consumer,
  replay, final manifest, stage and commit are all zero;
- retained payload read, qualification, generation, retry, repair, copy,
  consumption, network, device, camera, Ray, strip, cleanup, capture, analyzer,
  FORMAL-R6, firmware and deployment are all zero.

## Accepted technical finding

The existing frozen owners do not provide the seam required by Advisor Option
B:

1. `build_td_b_setup_release_lineage_candidate` has no subordinate exact
   provenance-manifest input;
2. `validate_td_b_setup_lineage_release` has no subordinate manifest input or
   independent recomputation boundary;
3. `write_td_b_setup_lineage_release` has no manifest-forwarding edge to the
   canonical validator;
4. the canonical validator does not independently recompute before/after blob
   OIDs, the canonical binary-safe patch hash, or the three retained R3
   artifact hashes.

Therefore the Advisor requirements are jointly contradictory under the
current authorization:

```text
successor changed paths = exact helper module + dedicated test only
canonical validator = sole eligibility owner and independent recomputer
current canonical validator seam = absent
```

Adding the seam requires at least a third repository implementation path
(and meaningful validator coverage), while implementing it in the helper would
be prohibited self-authorization or a parallel eligibility authority.

## Decision, residual risk and next branch

B1 is accepted as a truthful, contract-compliant negative feasibility result.
It does not unlock B2. The two-file diff remains unchanged, unstaged and
unaccepted. Helper v1 remains superseded/unconsumable, and retained R3 remains
`RETAINED_UNVALIDATED_UNCONSUMED`.

The exact next branch is a non-executable Advisor stop. Advisor must revise the
commit/path/parent contract to authorize a canonical-validator seam, or provide
an exact already-existing seam interpretation that satisfies independent
recomputation without helper self-authorization. No Planner/Executer work may
continue until that decision is recorded by Orchestrator.

All release consumption and downstream predevice, E2, FORMAL-R6, strip, TD-C,
sentinel and P8 routes remain locked.

