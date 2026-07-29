# REF-P7-25-R2-B1A-C3E6F3 review / pre-acquisition read-order hard failure

**Planner review date:** 2026-07-29

**Reviewed contract:**
`P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F3-CLEANUP-TEST-SUCCESSOR-PREREQUISITE-V1`

**Decision:** `rejected_pre_acquisition_controller_read_order`

**Next branch:** `REF-P7-25-R2-B1A-C3E6F4`

## Reviewed scope and method

C3E6F3 was authorized to create one fresh external evidence root, make an exact one-path
raw-shutter test-only direct-child commit, prove that the existing canonical cleanup-test
validator still rejects that child, and seal one immutable, unconsumable exact successor
manifest. The accepted topology deliberately separates the test prerequisite commit from
the later production validator-binding commit so no commit needs to bind its own SHA.

Planner reviewed the active PLAN, `EXECUTION_RESULT.md` section 64, shared Git state and the
active persistent debug record. No C3E6F3 evidence root exists, so there is no package
artifact whose claims can supersede the terminal handoff.

## Accepted evidence and execution facts

The Executer established these preconditions before the failure:

- shared HEAD was exactly `9303aa22a9bd37e8ec4f23147c78c6bea84b9a2e`;
- shared staged paths were zero;
- the fixed C3E6F3 container was absent;
- the closure fixture and canonical cleanup manifest existed and their observed identities
  matched the frozen PLAN values:
  - `config/white/white-endpoints.json`: 1,483 bytes, SHA-256
    `050e79d0b075cbbb894da68a21561b6e8f62633c0ec0faf1f8bfc027a319e813`;
  - canonical cleanup-test manifest: 2,641 bytes, SHA-256
    `753f00f15a9c40dd0e3a0c34773f063a2cd44605d7c1f5507f375d87f56ea0d0`.

Those matching identities are observations only. They do not receive acquisition or
validation credit because the bytes were read before a fresh evidence root existed and the
observed lstat/fstat/byte-count/hash facts were not durably persisted, fsynced, strictly
reloaded and sealed before comparison.

Fresh root, clone, checkout, test-source read/materialization, runtime-fixture reads/copies,
test runs, stage, external commit, canonical validator call, successor manifest and verifier
were all zero. Candidate materialization, production changes, full suite, original retained
R3 reads, real retained audit, eligibility, consumer and release operations were zero.
Network, DNS, `.env`, credentials, devices, camera, Ray, strip, cleanup, capture, public
analyzer, FORMAL, firmware and deployment were also zero. Shared PLAN and FULL remained
unchanged. `EXECUTION_RESULT.md` section 64 is the terminal evidence owner and its handoff
file SHA-256 is
`23912ebab3d2d9bee4f3d910bee15f29bf32cc931a23b8c8498850754d5e5df0`.

## Finding and decision

The controller consumed the closure fixture's single-read budget and one canonical-manifest
read before it could create valid observed-before-compare evidence. Continuing under C3E6F3
would require either repeating a consumed read or accepting an unsealed observation, both of
which violate the PLAN. The immediate stop was correct.

C3E6F3 is therefore rejected as a pre-acquisition controller read-order hard failure. It
receives no fresh-root, materialization, test, commit, manifest, validator, R3, eligibility,
release or device credit. Its absent container must not be created, repaired or reused.

The failure does not contradict the accepted non-self-referential topology. The exact route
remains:

1. one exact raw-shutter test-only direct-child commit;
2. one immutable, unconsumable exact successor provenance manifest;
3. only a later separately reviewed package may bind that exact successor in the production
   canonical validator while preserving it as sole eligibility owner.

No generic path allowlist, canonical owner rewrite, validator bypass or ambient working-tree
acceptance is permitted.

## Exact next branch

C3E6F4 is a fresh execution of the same prerequisite topology with one and only one
controller correction: acquire and seal a fresh evidence root before the first content read
of any budgeted source. For every first budgeted content acquisition, the controller must
persist observed path, lstat/fstat-before/fstat-after, byte count and SHA-256, fsync the
record and containing directory, strictly reload it and independently hash the record before
performing any expected-value comparison or handing the bytes to a consumer/materializer.

C3E6F4 may not read from or reuse the nonexistent/failed C3E6F3 package. It remains prohibited
from materializing the five-path production candidate, changing production, running full
discovery, reading original R3, emitting eligibility, consuming a release or accessing any
network or device. It requires neither Advisor guidance nor Human authorization.

## Residual risks

- The test-only child SHA and successor-manifest SHA do not yet exist.
- Full clean-room discovery remains unpassed.
- The production validator has not yet been extended to delegate to an exact successor.
- Original retained R3 remains `RETAINED_UNVALIDATED_UNCONSUMED`; release rollback remains
  `32b9e670ff3bbea0cd1505528c2ca87c2935446c`.

**Planner stop:** archive complete. Activate only C3E6F4 after the Orchestrator reviews the
package and synchronizes its required FULL machine state.
