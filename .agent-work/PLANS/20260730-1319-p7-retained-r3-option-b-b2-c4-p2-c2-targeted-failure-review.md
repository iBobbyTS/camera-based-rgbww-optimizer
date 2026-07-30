# REF-P7-25-R2-B2-C4-P2-C2 targeted test failure review

**Review date:** `2026-07-30`

**Reviewed reference task:** `REF-P7-25-R2-B2-C4-P2-C2`

**Reviewed contract:**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-C4-P2-C2-PARSER-FREE-PRETEST-GATE-V1`

**Planner decision:**
`REJECTED_STATIC_GUARD_FALSE_POSITIVE_IMPLEMENTATION_NOT_YET_QUALIFIED`

**Reviewed PLAN identity:** bytes `13411`, SHA-256
`af20065a26493d2616742a6bd4814bb22bd9f81df0c60912a6a20fa82ed30b7d`.

**Reviewed stop:**
`B2_C4_P2_C2_INTEGRATION_QUALIFICATION_COMPLETE_WAITING_PLANNER_REVIEW`.

## 1. Reviewed scope and execution method

P2-C2 preserved the sole untracked integration test byte-for-byte, removed the
superseded Markdown machine-row parser, and authorized one parser-free pretest
gate followed by the original P2 ordered qualification sequence. The gate was
required to prove the activation topology, frozen test lstat/bytes/SHA, exact
NUL-safe Git classification and no-index whitespace state before the first
targeted invocation.

The integration test composes the public preparation and exact-five lifecycle
owners with in-memory callbacks. It must prove success, preparation failure,
lifecycle failure, seal-target tamper rejection and a static ownership boundary
without importing or calling the real validator, release, I/O, network or device
owners. Test edits, recreation, retry and fallback were prohibited in P2-C2.

## 2. Evidence independently reviewed

The final P2-C2 handoff in `.agent-work/EXECUTION_RESULT.md` had worktree
identity at review of bytes `964078`, SHA-256
`ca61ca530d30ef4f2f777d0d210240959674e6666ab2fbf3ab620d41abac446e`.
The tracked delta is exactly the twelve-line P2-C2 handoff append.

The activation topology independently observed at review was:

- HEAD: `4f0e4b72d7e9b3eb16ae71e02c4e2b495e6a632d`;
- direct parent: `c521447e9cefe51c1263565a3d8c1bba3e1aaaf3`;
- subject: `chore(plan): activate retained r3 parser-free pretest gate correction`.

The frozen implementation remained an untracked regular file:

- path: `tests/test_p7_retained_r3_controller_integration.py`;
- bytes: `13147`;
- SHA-256:
  `106ddcafddbc31d8172b3f6a3a2557830f5581bad56b8fda50a6c2e86820ca5d`.

The handoff reports that the sole parser-free pretest gate passed. Its porcelain
status was exactly one `??` record, tracked/cached sets were empty, the untracked
and union sets were the exact singleton, and the no-index whitespace gate had
the required clean-new-file exit and empty diagnostics. PLAN/FULL machine-row
parsing and revalidation remained zero.

The first targeted command ran once and reported `4/5` pass. The sole failure
was
`test_static_ownership_boundary_has_no_real_validator_or_io_surface`. All later
owner, focused, full, compileall, CodeGraph, postvalidation, staging, commit and
postcommit gates remained zero. Retry/fallback, actual canonical-validator,
eligibility, release, retained-R3, network and device counters remained zero.

No test command was run during this review. CodeGraph was consulted first; the
new untracked test was not indexed, so the frozen file was then inspected
read-only. No production source, test source, PLAN/FULL or evidence artifact was
mutated as part of diagnosis.

## 3. Planner finding

### Finding P2-C2-TEST-001 — accepted test-guard false positive

The static guard first requires the exact imported project-module set:

```text
camera_based_rgbww_optimizer.utils.p7_retained_r3_controller_preparation
camera_based_rgbww_optimizer.utils.p7_retained_r3_exact_five_controller
```

It then rejects any imported-module name containing the bare token `camera`.
Both required module names begin with `camera_based_rgbww_optimizer`, so the
second predicate necessarily rejects the modules required by the first. This is
an internally contradictory substring sentinel.

The frozen imports contain only standard-library modules, the machine-contract
symbols imported directly, and the two expected public owner modules. There is
no import or call of a camera-control module. The failure therefore does not
show a production integration violation, real validator import, or I/O surface.

The minimum semantic correction changes only the forbidden module token
`"camera"` to `".camera"`. The qualified substring continues to reject module
components such as `.camera_remote` or `.camera_gphoto2`, while it no longer
matches the top-level package prefix `camera_based_rgbww_optimizer`.

This is a single-file test-guard repair. Production owners, lifecycle semantics,
eligibility ownership and scientific contracts do not change. Advisor guidance
and Human device authorization are not required.

## 4. Decision, validation quality and residual risks

Decision:
`REJECTED_STATIC_GUARD_FALSE_POSITIVE_IMPLEMENTATION_NOT_YET_QUALIFIED`.

Validation quality is sufficient to classify this exact failure because the
predicate and required module strings directly prove the contradiction. It is
not sufficient to accept P2: only four of five targeted tests passed, and every
later qualification gate remains unrun.

Residual risks:

1. The corrected targeted suite may expose a different failure; no speculative
   second edit or retry is authorized.
2. Existing-owner, focused, full, compileall, CodeGraph, postvalidation, staging,
   commit and postcommit gates remain unexecuted.
3. The test must remain the sole implementation path; production owner edits
   would exceed this correction and require a new Planner branch.
4. The implementation commit must retain the original P2 subject and exact
   singleton tree scope.

## 5. Exact next branch

The sole next package is `REF-P7-25-R2-B2-C4-P2-C3`, contract
`P7-TD-B-RETAINED-R3-OPTION-B-B2-C4-P2-C3-STATIC-GUARD-CORRECTION-V1`.

It must preserve the accepted P2-C2 activation and scope-gate facts without
rerunning them, verify the newly activated HEAD plus the frozen pre-edit test
identity, perform exactly one byte-local replacement from `"camera",` to
`".camera",`, verify the frozen post-edit identity, and restart at the targeted
test. Every subsequent P2 gate, implementation commit subject, zero-operation
budget and final Planner stop remains unchanged. Any failure stops without a
second edit, retry, fallback, staging or commit.

P2-C3 does not authorize production edits, retained-R3 reads, real B2,
canonical-validator use, eligibility, release consumption, network or device
work.
