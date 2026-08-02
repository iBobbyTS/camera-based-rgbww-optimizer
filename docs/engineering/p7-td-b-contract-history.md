# P7 TD-B Contract History

Last updated: 2026-08-01 22:10 MDT

Reference commit: `be8c4cdf75e447d128e3c7283cf5b3916d85d1cf`

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

## 2026-08-01 Orchestration Recovery Baseline

The retained-R3 route is paused after an independent loss-of-control audit. The
audit classified the prior orchestration as `ABNORMAL_ORCHESTRATION_LOOP`: local
fail-closed reviews usually preserved truth, but repeated disposable controllers
and unbounded corrective IDs did not advance the retained release state.

The canonical current state is deliberately small:

- `.agent-work/PLAN.md` is
  `NO_ACTIVE_EXECUTABLE_PLAN_WAITING_NEW_GOAL`, with `executable=false` and
  active task count `0`.
- `REF-P7-RECOVERY-NEXT-GOAL` is a non-executable intake placeholder. It is not
  a release, retry, device, formal, or commit authorization.
- Retained R3 remains `RETAINED_UNVALIDATED_UNCONSUMED`; canonical eligibility
  and release consumption have not occurred.
- The old deep `REF-P7-25-R2-...C1/R1/S1...` route is historical only and must
  not be resumed or extended by a new goal.
- EQ-R6 State C at `1/2500` remains the latest accepted scientific/device-stage
  result. Engineering owner acceptance after that result does not change the
  scientific or release state.

The retired waiting draft is recoverable from
`.agent-work/PLANS/20260801-2152-p7-orchestration-recovery-draft-retirement.md`.
The archive records the exact Git blob, byte count, SHA-256, and prior review
identity without copying or altering `EXECUTION_RESULT.md`.

## Retained-R3 Ownership Baseline

The following current repository boundaries are retained. Their tests prove
implementation behavior only within the listed authority:

| Boundary | Canonical owner | Authority |
| --- | --- | --- |
| PLAN/FULL machine rows | `utils/agent_work_machine_contract.py` | strict exact-bytes parser; no execution or eligibility authority |
| controller preparation | `utils/p7_retained_r3_controller_preparation.py` | AST/source preparation and terminal admission |
| controller conformance | `utils/p7_retained_r3_controller_conformance.py` | static owner/transport/lifecycle validation |
| controller runtime | `utils/p7_retained_r3_controller_runtime.py` | source persistence and process envelope |
| deterministic templates | `utils/p7_retained_r3_controller_domain_template.py` and `utils/p7_retained_r3_real_manifest_domain_template.py` | pure construction; synthetic/subordinate output only |
| provenance I/O and canonical JSON | `utils/p7_retained_r3_provenance_io.py` | filesystem/Git facts plus the sole immutable Mapping/tuple to JSON-native projection |
| offline patch preflight | `utils/p7_retained_r3_offline_patch_preflight.py` | delegates machine rows and canonical JSON to the owners above; no parallel parser |
| real-manifest self-check | `utils/p7_retained_r3_real_manifest_self_check.py` | subordinate validation only; eligibility and release consumability remain false |
| retained release audit helper v1 | `optimization/p7_retained_release_audit.py` | historically accepted prerequisite, superseded before real validation |

The accepted synthetic integration tests, exact-five helper, domain templates,
offline patch preflight, and subordinate self-check remain useful regression
surfaces. They must not be described as a canonical validator invocation,
retained eligibility, release consumption, or device readiness.

Rejected candidates remain in Git history, review archives, and immutable
external evidence roots. Disposable controller source under
`/Volumes/4T/temp/rgbww-optimizer` is not a production semantic owner and must
not be repaired, rerun, or reused. The recovery did not delete or move any such
root because its archive/ER hash references remain part of the evidence chain.

## Evidence Indexes

- `.agent-work/PLANS/INDEX.md` groups the 407 retained Planner archives by
  scientific result, accepted owner, synthetic/subordinate evidence, rejected
  controller loop, and recovery disposition.
- `.agent-work/EXECUTION_RESULT_INDEX.md` identifies the immutable ER snapshot,
  the one real self-check owner call, the last complete handoff, and safe lookup
  rules. It does not replace or summarize away the original 1.6 MB record.
- `audit/1/1.stop.md` through `audit/1/3.audit.md` are Human-owned and committed;
  `audit/1/4.recovery_baseline.md` is the final recovery attestation.

## Previous Wrong Attempts

- Rebuilding accepted owner shapes in one-off external controllers caused
  bytes/text, `mappingproxy`, tuple/list, marker, regex, Git-ledger, effect-order,
  and EOF drift before the real owner was reached.
- Treating each local fail-closed result as a reason to append another
  `C1/R1/S1/D1/D2` suffix preserved evidence but did not change the retained
  state. Three failures at one semantic boundary now require ownership and
  contract reassessment rather than another corrective ID.
- A PLAN header waiting for activation and a FULL machine row claiming active
  authorization were allowed to coexist. The recovery baseline requires one
  non-executable state until a Human starts a new goal and a future Planner
  writes a new PLAN.
- Synthetic/offline qualification and full unit-test success were sometimes
  visually adjacent to release routes. They remain engineering evidence only;
  the canonical validator is still the sole eligibility owner.
