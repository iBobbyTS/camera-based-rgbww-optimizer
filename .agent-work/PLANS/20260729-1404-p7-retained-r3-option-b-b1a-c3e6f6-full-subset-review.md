# REF-P7-25-R2-B1A-C3E6F6 review / pre-root FULL subset comparison hard failure

**Planner review date:** 2026-07-29

**Reviewed contract:**
`P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F6-CLEANUP-TEST-SUCCESSOR-PREREQUISITE-V1`

**Decision:** `rejected_pre_root_full_subset_comparison_shape`

**Next branch:** `REF-P7-25-R2-B1A-C3E6F7`

## Reviewed scope and evidence

C3E6F6 retained the exact-row parser, strict structural-AST closure predicate,
fresh-root-first five-acquisition protocol and accepted non-self-referential prerequisite
topology. Planner reviewed the current PLAN/FULL, `EXECUTION_RESULT.md` section 67, shared Git
state and the active debug record.

The exact unique backtick-wrapped PLAN/FULL parser passed one positive and all eight negative
classes. The first failure occurred when the temporary controller compared the entire FULL
machine object to PLAN's nested 12-key `required_full_machine_state` object. All 12 required
keys existed and had exact required values. FULL also contained 17 legitimate roadmap fields,
so whole-object equality incorrectly emitted `FULL nested mismatch`.

The contract requires required-key subset equality, not equality of the two complete objects.
This is a controller comparison-shape defect, not PLAN/FULL drift or a source, fixture, test,
Git, provenance or scientific failure.

Failure preceded fresh-root acquisition, source content reads and clone. Root, retry,
failed-root reuse, five acquisition records, materialization, fixture reads/copies,
canonical-manifest reads, tests, stage, external commit, validator, successor manifest and
verifier were all zero. Candidate, production, shared Git, retained R3, audit, eligibility,
consumer, release, network, DNS, `.env`, credential, device, camera, Ray, strip, cleanup,
capture, analyzer, FORMAL, firmware and deployment counters were zero.

Shared HEAD remains `9303aa22a9bd37e8ec4f23147c78c6bea84b9a2e`; staged paths remain zero.
Reviewed PLAN and FULL SHA-256 values are
`50f2669d8fbd62dbdc2cef033e5c1962d2ae1462a4d32e0172ca8a777839e2d7` and
`547dfc5fe3fab675f1e103b789c52b9469bdc34f08de4a083eda79c55ca5f305`.
The execution handoff file SHA-256 is
`5d9856b5d738d8127909097acbebdf0969ca640ab6e8ece93ff58b1585d5a2de`.

## Decision

C3E6F6 is rejected solely at the pre-root FULL comparison gate and receives no reusable
execution credit. Its absent fixed container must not be created or reused. The exact-row
parser remains accepted, while the C3E6F6 structural-AST correction remains unexercised and
must be retained unchanged in a fresh successor.

The one-path test-only child, old-validator expected rejection and immutable/unconsumable
successor-manifest topology remain accepted. Production validator binding remains a later
separately reviewed package.

## Exact next branch

C3E6F7 changes only FULL comparison semantics. For each of the exactly 12 keys in PLAN's
`required_full_machine_state`, the controller must separately prove:

1. the key exists in the strict-parsed unique FULL object; and
2. its FULL value equals the expected value with exact JSON type and value.

Missing and mismatched arrays must both be empty before proceeding. Missing keys, type drift
or value drift remain hard failures. Additional strict-parsed FULL roadmap fields are allowed
only when their names are outside the 12-key required set; they cannot replace, shadow or
override any required key. Whole-object equality, weakening/removing a required key, ambient
fallback and permissive duplicate-key parsing are prohibited.

Every other C3E6F6 rule remains unchanged: exact backtick-row parser and eight negatives,
strict structural AST predicate, fresh-root-first ordering, five observed-before-compare
records, one-path child, expected canonical rejection, immutable unconsumable successor
manifest, and all zero-operation locks. C3E6F6 must not be retried. No Advisor or Human
authorization is required.

## Residual risks

- Structural-AST validation and all acquisition gates remain unexecuted in this branch.
- The test-only child and successor manifest do not yet exist.
- Full clean-room discovery remains unpassed.
- Production validator binding remains incomplete.
- Original retained R3 remains `RETAINED_UNVALIDATED_UNCONSUMED`; rollback remains
  `32b9e670ff3bbea0cd1505528c2ca87c2935446c`.

**Planner stop:** archive complete. Activate only C3E6F7 after Orchestrator synchronizes its
required FULL machine state.
