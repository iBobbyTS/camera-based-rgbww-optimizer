# PLAN-FULL — GUIDE6 H120/S100 direct local controllability

<!-- FEATURE-CONTEXT:START -->
## Feature Context

### Feature identity

- Feature ID / slug: `guide6-h120-s100-local-controllability-v1`
- Feature base: `3e81a3202b091c19c7109638ca9087a9fb60f1a3`
- Active artifacts belong only to this feature: `yes`

### Original user request

Advisor/Human decision: accept both retained roots as valid exact-command negatives,
reclassify them as `repeatable_target_local_seed_mismatch`, retain the frozen direct
58-feature estimand, and create `GUIDE6_H120_S100_DIRECT_LOCAL_CONTROLLABILITY_V1`
with four G-active probes, bounded feedback candidates, confirmations, cleanup and
the stated result branches.

Later correction superseding prior guidance: the two roots are not two solver
failures because both measured only `CW=518, WW=0, R=0, G=4095, B=0`; solver attempt
count is zero. The prior analyzer `S-SOLVER-RETRY` label is historical-only.

### Requirement, example, and correction traceability

| ID | Current instruction/example/correction | Supersedes | Acceptance criterion | Test or probe |
|---|---|---|---|---|
| REQ-001 | Preserve both legacy analyses and create immutable seed-negative derived evidence | legacy solver-failure interpretation | AC-F-001 | exact two-root derived-artifact regression |
| REQ-002 | Final gate remains same-block ordered 58-feature strip-minus-Ray with frozen covariance/0.9973 guard | none | AC-F-002 | analyzer score/guard regression |
| REQ-003 | Four probes are CW/WW/R/B +256 around exact G-active base; repeat base after probe 2/4 | static single-candidate block | AC-F-003 | fake-backend exact command/order test |
| REQ-004 | Build whitened direct-feature Jacobian; <=4 solver candidates; box, max step 768, 1/.5/.25 backtrack, one rebase/Broyden | no actual solver | AC-F-004 | deterministic synthetic controllability test |
| REQ-005 | Candidate pass requires 3 D/A/Q confirmations | none | AC-F-005 | pass and failed-confirmation behavior tests |
| REQ-006 | Ray=2, strip<=14, total<=16, ambient=0, in-root retry=0; cleanup/source isolation always | none | AC-F-006 | fake-backend budget/abort/cleanup tests |
| REQ-007 | Valid improvement permits one centered continuation; no G-active improvement permits one P2 active-set screen; no gamut claim | premature terminal solver/gamut inference | AC-F-007 | analyzer branch regressions |
| REQ-008 | 13-node grid, B pre/post, cross-experiment synthesis, boundary, Gate-6 and P8 remain locked | none | AC-F-008 | plan/analyzer lock assertions |

### Minimum sufficient end-to-end outcome

One direct H120/S100 target block actually perturbs four command degrees of freedom,
constructs a local model in the frozen direct residual coordinate, measures bounded
solver candidates, and produces one truthful LC-A/B/C/D/E classification with complete
small evidence and cleanup. No new runtime/framework owner is introduced.

### Scope authority map

- Immutable seed correction: explicit Advisor decision REQ-001.
- Protocol builder, adaptive measurement and derived analyzer: explicit Advisor
  controllability experiment REQ-002..REQ-007 and existing three owners.
- Fake-backend behavior tests: repository safety rule and unavoidable proof that the
  actual device owner enforces commands, caps, isolation and cleanup.
- No generalized runtime, release, lineage, stage-gate, readiness or solver framework.

### Goal

Replace seed-only qualification with the first real bounded direct local-controllability
experiment while preserving the frozen scientific estimand and safety bounds.

### Observable behavior

- The old two roots receive a new immutable derived `repeatable_target_local_seed_mismatch` artifact.
- The direct CLI can execute the exact Ray/base/probe/anchor/candidate/confirmation protocol.
- The run records command hashes, Jacobian diagnostics, predicted/measured residuals,
  reduction, trust ratio, bounds, backtrack and model version.
- The analyzer emits only LC-A/B/C/D/E or the explicitly permitted continuation/screen branches.

### Constraints and invariants

- Canon native Bayer, ordered 58 features, identity response, frozen source covariance,
  coverage `0.9973`, guard, exposure map, reset600 and D/A/Q 120 s remain unchanged.
- Linearized command order is CW/WW/R/G/B; G remains 4095 in the first active set.
- D/A are command/readback/timing preconditions, not extra formal captures.
- All source transitions retain isolation, finally cleanup and zero readback.
- `retry=0` means no hidden reacquisition in one root; a later permitted root is separate.

### Non-goals and unsupported environments

- No physical/gamut-unreachable conclusion.
- No 13-node grid, B pre/post, cross-experiment absolute synthesis, boundary, Gate-6,
  P8, LUT installation, firmware or remote deployment.
- No generic adaptive runtime, orchestration machine, release package or new solver service.

### Ownership and state boundaries

- `p7_thermal_diagnostics.py`: static scientific contract and plan builder.
- `measure_p7_thermal_diagnostics.py`: sole device execution/adaptive command owner.
- `analyze_p7_thermal_diagnostics.py`: immutable derived classifications and final analysis.
- Existing bounded least-squares/multipatch solver functions may be reused; no new owner.

### Allowed structural changes

- Add one protocol-specific plan variant and one protocol-specific adaptive execution path
  inside the three existing owners.
- Add local helpers for whitened residual/Jacobian/candidate selection and existing-style
  JSON/JSONL evidence; no shared framework or public configuration surface.

### Audit-remediation scope, if applicable

- Accepted audit finding IDs: `none`
- Unrelated discoveries go to: separate audit backlog

### Feature acceptance criteria

- AC-F-001..008 all have deterministic behavior evidence.
- One clean checkpoint executes the bounded experiment only after S01/S02 acceptance.
- The device run never exceeds Ray=2, strip=14, total=16 and always finishes zero/off.

### Validation tiers

- Targeted: seed reclassification, exact plan, solver math and fake-backend protocol tests.
- Section/package: relevant `tests.test_p7_direct_r6` selectors plus compileall.
- Final integration/repository: one focused direct-path suite, wrapper syntax, CodeGraph sync,
  and `git diff --check`; no repeated full-suite campaign.

### Compatibility, migration, rollout, rollback, and cleanup

- Legacy analysis files remain byte-identical; new derived artifact is additive.
- Existing direct variants remain supported unchanged.
- A failed live root is preserved; cleanup and zero readback precede diagnosis.
<!-- FEATURE-CONTEXT:END -->

## Plan Review Gate

- Status: `APPROVED_AFTER_BOUNDED_CORRECTION`
- Reviewed PLAN-FULL SHA-256: initial `ccdc2e45801b8d303b21caa9148323b59e584ac66ef243a96f03fb0296dabc24`; corrected `b908e8b58e5e0260119a22f3f4279c30c41ed1b72da184c73e284754b267d570`
- Reviewer/profile/session: fresh `guide6_plan_review`
- Admitted IDs: `PR-001`, `PR-002`, `PR-003`
- Corrections applied: exact retained-root/SHA/oracle identity; frozen branch predicates; confirmation-reserved budget and no-extra-probe rebase semantics.
- `PLAN_DELTA` recheck: `not-required`

<!-- SECTION:S01:START -->
## S01 — Seed-negative immutable reclassification

### Goal

Create a new derived artifact that truthfully records two exact-command negatives and
zero solver attempts without modifying either legacy analysis.

### Authority and necessity

- Authority anchor: Advisor decision REQ-001.
- Required because the current artifact labels a seed-only failure as solver retry.
- The existing immutable legacy artifact cannot be edited; one additive derived analysis is the smallest correction.

### Dependencies

- Requires: `none`
- Base: `3e81a3202b091c19c7109638ca9087a9fb60f1a3`.

### Expected scope and direct impact cone

- Primary owner: `analyze_p7_thermal_diagnostics.py`.
- Allowed-to-edit: analyzer seed-reclassification helper/CLI path; `tests/test_p7_direct_r6.py`; current plan/state/review artifacts.
- Inspect-only exact fixtures:
  - root 1: `/Volumes/4T/temp/rgbww-optimizer/guide6-direct-target-local-h120-s100-20260813/20260814-075000-qualified-strip-1over1600-reference-repeat`
  - root 1 legacy analysis SHA-256: `c32dc70b5639ff0342dbef0c8dc2151d1bb1469fa717b3b17f9e032d57b5dd1b`
  - root 2: `/Volumes/4T/temp/rgbww-optimizer/guide6-direct-target-local-h120-s100-20260813/20260814-080000-qualified-strip-1over1600-solver-repeat`
  - root 2 legacy analysis SHA-256: `9651f2f3d706d2dd7b950737a58b93d71a947a841b1da44cda1b3b94261a0f87`
  - frozen policy and each root's capture/command evidence.
- Explicitly excluded: device execution, thresholds/covariance/features, old artifact mutation, solver implementation.

### Non-goals and deferred owner

- No live acquisition or solver inference; S02 owns actual controllability.

### Invariants

- Legacy bytes unchanged; exact command hash and score values are verified from retained evidence.

### Allowed structural changes

- One local derived-artifact function and explicit output path; no new analyzer framework.

### Review intensity

- `BOUNDED`

### Review assurance

- Requested: `AUTO`
- Resolved: `ONE`
- Reasons: offline additive artifact, exact regression values, no device behavior.

### Acceptance criteria

- Emits `repeatable_target_local_seed_mismatch`, solver count 0, distinct candidate count 1,
  probe/candidate count 0, exact hash, both scores/brackets, and prohibits gamut inference.
- Exact command/hash is `CW=518, WW=0, R=0, G=4095, B=0` /
  `f70a07889065ad105bf25a9fda103ec2a708ef056f4ae17b0279ef3886b5cfde`;
  exact scores are `80.2851456563` and `80.8620601083`; both Ray brackets are `pass`.
- Refuses overwrite and proves both legacy analyses byte-identical.

### Validation tiers

- Targeted: derived artifact exact regression and immutable overwrite test.
- Section/package: related direct analyzer tests.
- Integration checkpoint: S02 consumes only the corrected status, not historical solver failure.

### Reset triggers

- Any change to final estimand, source covariance, feature set or legacy artifact semantics.
<!-- SECTION:S01:END -->

<!-- SECTION:S02:START -->
## S02 — Direct local-controllability protocol and adaptive solver

### Goal

Execute the exact bounded Ray/probe/feedback/confirmation target block through the
existing measurement CLI and classify it without claiming gamut reachability.

### Authority and necessity

- Authority anchor: Advisor decision REQ-002..REQ-008.
- Required because no retained root contains a probe, Jacobian or solver-generated command.
- Static `execute_plan` cannot choose later commands from current-root observations;
  a protocol-specific adaptive path inside the existing measurement owner is necessary.

### Dependencies

- Requires: `S01`
- Base: exact accepted S01 head.

### Expected scope and direct impact cone

- Primary owner: `measure_p7_thermal_diagnostics.py`.
- Allowed-to-edit: `p7_thermal_diagnostics.py`, `measure_p7_thermal_diagnostics.py`,
  `analyze_p7_thermal_diagnostics.py`, existing bounded solver modules only if reuse needs
  a local generic parameter, `tests/test_p7_direct_r6.py`, wrapper only if an argument is needed,
  current plan/state/review artifacts.
- Inspect-only: HSI policy/covariance helpers, duty curve, camera backend, all-off owner,
  current direct variants and solver tests.
- Explicitly excluded: generalized runtime/coordinator, new persistence, release/lineage/stage-gate,
  B pre/post, cross-experiment synthesis, 13-node/boundary/Gate-6/P8.

### Non-goals and deferred owner

- Active-set screen and centered continuation are emitted as bounded next branches; they are
  executed only if the first block reaches LC-B/LC-C.
- H120/S50 and later sentinel points require LC-A and remain later GUIDE work.

### Invariants

- Exact base/probes, max step 768, backtracks 1/.5/.25, one rebase, <=4 feedback,
  3 confirmations only after candidate gate, Ray=2, strip<=14, total<=16, ambient=0.
- Every strip capture uses D120/A120/tested-command120; one strip reset600 per block.
- Cleanup/zero/source isolation and clean Git checkpoint remain mandatory.
- Budget scheduling is deterministic: initial base + 4 probes + 2 drift anchors use 7
  strip captures; 3 confirmation slots are reserved before any feedback candidate;
  therefore at most 4 feedback candidates may be launched. Before each candidate,
  `used_strip + 1 candidate + 3 reserved confirmations <= 14` must hold.
- The one permitted in-root rebase uses the measured candidate and one Broyden/model
  rebase without new probe captures. A full four-probe rebase is not allowed inside
  this root and may occur only in the explicitly permitted new-root continuation.

### Allowed structural changes

- One protocol-specific adaptive executor plus local solver/evidence helpers in existing owners.
- One new plan schema/variant and one derived analysis schema.

### Review intensity

- `HIGH_RISK`

### Review assurance

- Requested: `AUTO`
- Resolved: `TWO`
- Reasons: adaptive commands drive physical light output and later decisions depend on captured feedback.

### Acceptance criteria

- Exact order and commands, drift anchors, budgets and no hidden retry are enforced.
- Jacobian uses whitened direct residual; diagnostics include singular values/rank/condition.
- Every feedback row records command/hash, predicted/measured residual/score, reductions,
  trust ratio, active bounds, fraction and model version.
- Candidate pass triggers exactly three confirmations; any invalid confirmation cannot yield LC-A.
- LC-B/C/D/E and continuation/screen locks match Advisor decision; no gamut claim.
- All abort paths invoke cleanup and produce zero evidence.

### Frozen classification table

| Branch | Required observations/predicate | Output / next lock |
|---|---|---|
| LC-A | Ray bracket pass; 4 valid probes; Jacobian built; base anchors pass; a distinct solver-generated candidate passes; exactly 3/3 confirmations pass | `H120_S100_direct_local_solver_pass`; unlock only H120/S50 |
| LC-B | valid probes/Jacobian and at least one distinct solver candidate has positive measured reduction, but no confirmed pass within budget | `H120_S100_local_controllable_but_not_yet_faithful`; permit one new-root continuation centered on best command |
| LC-C | 4 valid probes/Jacobian/base anchors, actual bounded candidates/backtrack/one Broyden rebase executed, but no candidate improves base | `G_active_neighborhood_inadequate`; permit one P2-seeded active-set screen; gamut inference prohibited |
| LC-D | insufficient valid independent probes or frozen exposure cannot observe a required probe | `local_controllability_not_observable_under_frozen_exposure`; follow S-MEASUREMENT |
| LC-E | Ray before/after bracket fails | `target_block_reference_invalid`; permit one new-root repeat, second failure Advisor gate |

The first G-active block may output only LC-A, LC-B continuation-required, LC-C
active-set-screen-required, LC-D, or LC-E. It may not output
`multi_start_solver_unresolved`. `S-SOLVER-RETRY` requires valid probes, a built
Jacobian and at least one distinct measured solver-generated candidate;
`S-SOLVER-UNRESOLVED`/`multi_start_solver_unresolved` requires exhaustion of the
bounded G-active path plus the permitted continuation/alternate-active-set path.
The derived S01 artifact is orchestration/scientific disposition only: production,
runner and tests must not consume `.agent-work` or historical analysis as runtime
authorization.

### Validation tiers

- Targeted: synthetic solver math and exact fake-backend command sequence/branch tests.
- Section/package: direct runner/analyzer tests, compileall and wrapper syntax.
- Integration checkpoint: one clean fake-backend end-to-end run under physical caps.

### Reset triggers

- Changing device-control owner, final estimand/covariance, public CLI compatibility,
  cleanup semantics, or adding a generalized adaptive runtime.
<!-- SECTION:S02:END -->
