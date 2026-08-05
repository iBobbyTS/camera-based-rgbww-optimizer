# Supervisor engineering architecture decision request

**Status:** `SECTION_2_ENGINEERING_CONVERGENCE_STOP_SUPERVISOR_REVIEW_REQUIRED`

**Document authority:** `read_only_non_executable_decision_request`

**Stopped scope:** `REF-G4-06-REPLACEMENT-PACKAGE` /
`SECTION_2_REPLACEMENT_TASK_PROJECTION_AND_CHILD_TOPOLOGY`

**Planner disposition:**
`REJECTED_FINAL_FULL_MASS_REGRESSION_COMMITTED_SOURCE_CANDIDATE_BLOB_DRIFT`

This document requests a later Supervisor engineering architecture decision. It
does not select an option, authorize implementation, create a PLAN, permit a
fourth repair, or unlock package, formal, release, or device work.

## Frozen evidence and stop reason

- Historical-only candidate ref:
  `refs/heads/codex/historical-g4-r6-section2-final-snapshot-rejected`.
- Historical-only commit: `3dc2fa2639ee19b1c10ec55e2412836527c8973b`.
- Full evidence prefix:
  `/Volumes/4T/temp/rgbww-optimizer/g4-r6-s2-final-snapshot-full-20260805T065009Z-632cc86`.
- Result: `982` tests, exit `1`, `4 failures + 219 errors`, retry `0`.
- Log SHA-256:
  `6d57da77e5d8afe690787b74aae4cbc8e8fd8998672acfa49fef68cb621b5222`.
- Dominant boundary: `committed_source_candidate_blob_drift`.

The current orchestration requires the candidate's final full validation before
the final implementation commit, while the production validator requires the
same candidate to already have its final committed subject and blob identity.
AUTH/PROV repair, topology-subject repair, and this committed-identity mass
regression constitute three substantive convergence failures at the same
Section 2 boundary. The route is therefore fail-closed with no fourth repair.

## Architecture directions for Supervisor consideration

These are alternatives to evaluate later, not recommendations or executable
branches:

1. **Explicit two-phase validation and promotion.** Separate pre-commit
   behavioral qualification from post-commit immutable attestation. Define an
   atomic promotion rule that accepts neither phase alone and cannot consume a
   package until both identities agree.
2. **Content-addressed candidate identity before commit.** Bind validation to a
   frozen candidate tree/blob manifest that can exist before a branch commit,
   then require a later commit to reproduce that exact tree and add the final
   subject/ancestry proof without changing candidate bytes.
3. **Dedicated non-production qualification checkpoint.** Create an explicitly
   non-production candidate commit, run the one permitted qualification against
   that immutable checkpoint, then promote only through an exact, reviewable Git
   topology whose semantics do not require changing the qualified source/test
   bytes.

Any future selection must define one source of truth for candidate identity,
the exact point at which tests are valid, the promotion/rollback topology,
failure accounting, and proof that historical-only candidates cannot become
production inputs. It must start under a new Supervisor-approved PLAN/FULL
boundary and must not reuse the stopped repair as a fourth attempt.

## Locks pending decision

- PLAN/FULL active task count: `0/0`.
- Fourth repair and full rerun: `false/false`.
- Candidate acceptance or production use: `false`.
- Package prepare/describe/root access: `false`.
- Replacement formal, release consumption, and analysis: `false`.
- Device/network/camera/Ray/strip/capture: `false`.
- Scientific result or GUIDE completion claim: `false`.

The next action is only
`WAIT_FOR_SUPERVISOR_ENGINEERING_ARCHITECTURE_DECISION`.
