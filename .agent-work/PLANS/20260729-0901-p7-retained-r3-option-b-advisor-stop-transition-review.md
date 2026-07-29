# REF-P7-25-R2 Advisor-stop transition review

**Planner decision:** `ACCEPTED_OPTION_B_AND_SUPERSEDED_BY_B1_PLANNING`

**Review date:** 2026-07-29

**Reviewed PLAN SHA-256:**
`dd16cf047b787e3b28c98d6c6dcbea55e1dd7b2413f307060fd92fa661dc9b90`

## Reviewed scope and evidence

The reviewed PLAN was the non-executable
`P7-TD-B-RETAINED-R3-LINEAGE-OWNER-ADVISOR-STOP`. It correctly stopped all
execution while the exact provenance owner for the two helper paths was
unknown. Its accepted evidence remains:

- GUIDE `advisor/4/4.GUIDE.md`, SHA-256
  `659152f6c0ae69c90c701de4e57c352d771e4f0bf75cf9410271ba0a94200e35`;
- decision evidence
  `/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-release-lineage-owner-o3-c1r3/20260728T0121/lineage-owner-decision-evidence.json`,
  SHA-256
  `842cfad090549ebf6379df4551bd4f051267e4bf93014f899c5e329c57085620`;
- C1R3 acceptance archive
  `.agent-work/PLANS/20260728-0129-p7-retained-r3-o3-c1r3-advisor-evidence-acceptance-review.md`,
  SHA-256
  `ff6336e93043aac3ea841afd983226b902dba1adbc008e423d9c927f26dec8ef`;
- frozen helper-v1 HEAD
  `9303aa22a9bd37e8ec4f23147c78c6bea84b9a2e`, direct parent/release
  checkpoint `32b9e670ff3bbea0cd1505528c2ca87c2935446c`;
- the two unaccepted, unstaged target files remain at Advisor-approved SHA-256
  `48c0c57f...f3634cf8` and `c8d6c7c9...1b3f`.

## New Advisor decision

The later authoritative attachment
`/Users/ibobby/.codex/attachments/cba7928d-712a-441e-a708-4301ee32bd66/pasted-text.txt`,
SHA-256
`91a88e5467e13c811794c2149b6a8d5669e613c3e259d8f4091ba08c048733d6`,
selects Option B:

- one subordinate immutable exact provenance manifest;
- the existing canonical lineage validator remains the sole eligibility owner;
- helper v1 is retained as superseded and unconsumable;
- exactly one future successor repair commit may exist, with exact parent,
  two-path set and approved target bytes;
- no generic allowlist, parallel authority, payload repair/regeneration,
  release consumption, device work or later scientific stage is allowed.

This decision supersedes the waiting condition but does not itself prove that
the current canonical validator has a legal manifest ingestion/recompute seam.

## Planner decision and residual risk

The stop PLAN is accepted as correct historical control and is now archived.
Only `REF-P7-25-R2-B1` is unlocked. B1 is a pure-offline feasibility package;
it may not edit or commit the approved repair. If the current canonical
validator cannot consume and independently recompute subordinate manifest
facts without a third repository path or helper self-authorization, B1 must
fail closed as `BLOCKED_CONTRACT_CONFLICT` and return to Advisor.

The retained R3 remains `RETAINED_UNVALIDATED_UNCONSUMED`. Release generation,
repair, copy, consumption, qualification, tests, helper/audit/validator calls,
network, device, camera, Ray, strip, FORMAL-R6, TD-C, sentinel and P8 remain
locked by this review.

## Exact next branch

Rewrite active PLAN to contain only
`P7-TD-B-RETAINED-R3-OPTION-B-B1-CLEANROOM-FEASIBILITY`. Stop at Planner review
after one terminal B1 evidence package, whether feasibility passes or fails.

