# REF-P7-25-R2-B2-C4-C1-C1 architecture-stop review

**Planner review time:** `2026-07-30T12:17:43-06:00`

**Reviewed contract:**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-C4-C1-C1-ARCHITECTURE-STOP-V1`

**Decision:** `ACCEPTED_ORCHESTRATOR_MAINTAINABLE_ROUTE_READY_FOR_P1`

**Exact next branch:** `REF-P7-25-R2-B2-C4-P1`

## Reviewed scope and evidence

Planner reviewed only:

- `AGENTS.md` and the repository camera-calibration skill;
- the Orchestrator-owned `FULL_PLAN_REFERENCE.md` route for
  `REF-P7-25-R2-B2-C4-P1`;
- the superseded architecture-stop `PLAN.md`;
- the immutable C4-C1-C1 syntax-failure review archive.

The preceding C4-C1-C1 execution remains rejected as
`REJECTED_PRE_ROOT_OWNER_SYNTAX_FAILURE_NO_C4_PROGRESS`. Its frozen external
owner failed Python parsing before body entry, dispatch, package-root creation,
input reads, output generation, matrix, terminal evidence or ER append. The
failed owner remains immutable and non-reusable. Planner did not read or execute
that owner or any old C4 artifact.

The Orchestrator has accepted the architecture stop and frozen one replacement
route in `FULL_PLAN_REFERENCE.md`: a repo-owned, pure controller-preparation
helper with a dedicated test. At review time the repository is clean at
`253567fe9c92a43046d46a07e21752d8f30f7a23`, and both frozen target paths are
absent:

```text
src/camera_based_rgbww_optimizer/utils/p7_retained_r3_controller_preparation.py
tests/test_p7_retained_r3_controller_preparation.py
```

No implementation, test, CodeGraph, external evidence, controller, retained-R3,
validator, release, network or device operation was performed in this Planner
pass.

## Planner decision

Planner accepts the Orchestrator engineering decision and closes the stop
`B2_C4_C1_C1_ARCHITECTURE_STOP_WAITING_ORCHESTRATOR`. The exact next package is
`REF-P7-25-R2-B2-C4-P1`, limited to the two new repository paths above.

P1 must establish a typed, pure preparation owner for:

1. AST ancestor-edge and immediate same-list statement-scope selection;
2. deterministic source preparation without nested large generated programs;
3. canonical JSON bytes with exactly one final LF;
4. strict reload, canonical-byte equality and target identity linkage;
5. success/failure ER sequencing dominated by a valid-seal gate.

The helper may use pure standard-library parsing, hashing and typed data models.
It may expose callback-oriented sequencing for tests/future execution, but must
not perform filesystem, Git, subprocess, network, device, retained evidence,
validator, eligibility or release I/O itself. The existing canonical lineage
validator remains the sole eligibility owner.

## Validation quality and residual risk

This is a planning transition, not implementation acceptance. No runtime or test
result is credited. P1 must prove its behavior with dedicated positive and
negative tests, related focused tests, full discovery, compileall, CodeGraph sync
and diff checks before a focused exact-two-path commit, followed by a targeted
postcommit rerun.

Residual risk is bounded to the new helper implementation: AST scope ambiguity,
noncanonical or malformed terminal bytes, target identity rebinding and ER gate
bypass. Any failure must produce a bounded P1 corrective package; it must not
reactivate the external-owner correction chain.

## Preserved locks and stop

Old C4/C4-C1/C4-C1-C1 artifacts and owners, retained R3, the canonical validator,
eligibility, release creation/validation/consumption, public analyzer, network,
`.env`, credentials, devices, camera, Ray, strip, cleanup, capture, FORMAL-R6,
TD-C, sentinel and P8 remain locked.

The next package has exactly one Planner stop:
`B2_C4_P1_IMPLEMENTATION_COMPLETE_WAITING_PLANNER_REVIEW`.

## Maintainability judgment

The accepted route replaces a repeated disposable nested-program chain with one
small repository-owned semantic boundary and one dedicated regression owner. It
does not modify the canonical validator or production execution path; follow-up
integration is intentionally deferred to a later provenance-bound package.
