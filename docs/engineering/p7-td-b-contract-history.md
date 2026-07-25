# P7 TD-B Contract History

## Status and Use

P7 TD-B is currently paused and not authorized by this document. This is an
on-demand engineering history for provenance and regression work. It is not a
plan, release, retry permission, device authorization, or stage transition.
Only the active `.agent-work/PLAN.md` can authorize execution; the Orchestrator's
`.agent-work/FULL_PLAN_REFERENCE.md` records the non-executable route state.

## Scientific Contract

TD-B compares paired Ray120c and RGBWW sources through retained Canon RAW
captures. Ray120c CCT/G-M is reference-light metadata and must not be inferred
from camera RGB. Formal fitting uses the frozen TD-B no-ambient feature owner;
generic callers retain the ambient-subtracted default. Setup captures count
toward the physical cap but not formal captures, repeatability covariance, or
history aggregates.

The setup/formal split requires an exact checkpoint. Setup uses the shared
auto-exposure owner and retains every remote-v2 physical return. The child may
write only provisional setup evidence. Canonical setup, resolved formal plan,
and setup release are created only after the wrapper exits, Python and shell
cleanup succeed, and an independent both-zero readback passes. Formal work may
consume only the matching accepted release and checkpoint.

## Provenance and Physical Evidence

Every returned CR3 is paired with its canonical same-run metadata sidecar
before timing, feature, covariate, or report acceptance. The physical ledger
retains canonical paths, byte counts, SHA-256 hashes, and remote capture/request
IDs for both files. Missing, empty, external, symlinked, non-canonical, or
tampered sidecars fail closed while preserving the already-returned CR3 in the
physical count.

Implementation-only checkpoint changes do not silently rebind setup evidence.
They first produce a non-executable lineage candidate with a complete
changed-path classification. Planner acceptance is required. Any change to
camera, parser, setup inputs, budgets, commands, shutter, or cleanup requires a
new setup. An accepted candidate can be bound into a new lineage release; old
releases and same-content copies are never edited into executability.

Trusted prerequisite paths accept project-relative, `./`-relative, or exact
absolute spellings but persist one canonical repository path and frozen hash.
Traversal, outside-root paths, missing files, directories, symlinks, hash drift,
and same-content copies are rejected before backend or output access.

## Lifecycle and Failure Rules

The production wrapper, Python `finally`, shell trap, and independent finalizer
have separate evidence. Each semantic stage writes an immutable attempt before
an adapter call and binds its result to the attempt path and hash. Timeouts or
signals can leave an explicitly unknown result; they never imply success or an
automatic retry. Signal exit precedence remains above child failure, which
remains above cleanup-only failure.

TD-B hard failures do not automatically retry, run the public analyzer, start a
later capture stage, or consume a different release. Cleanup retains both
Python and shell off paths plus an independent final-zero check. Accepted
offline tests establish implementation behavior only; they do not establish
current hardware reachability or formal provenance.

## Historical R1/C1/C2/C3/E1/L1 Route

- The first Ray formal capture was physically returned but rejected for low
  plane-feature signal quality; no formal sample was accepted.
- C1/C2 made rejected-capture sidecar and remote-ID evidence atomic and
  fail-closed, including adapter drift and sidecar read failures.
- C3 bound exact TD-B formal work to the frozen no-ambient statistic and proved
  runner/analyzer feature-map equality while leaving generic behavior intact.
- E1 indexed canonical and superseded evidence without changing production
  behavior. L1 created and validated a new lineage release without device use.
- Later E2/Z0 attempts stopped at external-root or hostname/evidence gates.
  Their corrective packages did not authorize an experiment retry.

Consult archived Planner reviews and `.agent-work/EXECUTION_RESULT.md` only when
an active planning/review task needs exact artifact hashes or historical branch
decisions. Do not preload that history for ordinary control or calibration work.
