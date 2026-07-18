# P7-R0C formal closure

## Scope and locks

- Second-pass correction after Planner rejected P7-R0B named-experiment authorization.
- Offline only: no environment loading, network, camera, Ray, ESPHome, health/config, or all-off calls.
- Preserve solver hard caps `54/67` and `62/75`; preserve v1 and old sentinel hashes.
- Goal remains Blocked; `p7_targeted_reference_repeatability_v2` is not authorized.

## Confirmed observations

1. `analyze_strip_hsi_pilot` accepts only legacy v1 structures; no formal v2 analyzer closure exists.
2. Multiseed final selection sorts all best samples together, allowing an unconfirmed lower objective to replace a confirmed face.
3. Confirmation returns on the first legal gate failure and does not guarantee a complete n=3/n=5 group; a never-feasible solve lacks final verification.
4. `audit_repeatability_groups` regularizes within groups but computes trend, bimodality, and dominance after one cross-command centering operation.
5. The P7-R1 analyzer does not independently audit `commands.jsonl` or retained base/reacquire attempt evidence.
6. The 250 physical CR3 proposal is checked after adapter completion, not pre-reserved and independently reconstructed from retained evidence.

## Root-cause hypotheses

- Solver ownership is split incorrectly between per-attempt confirmation and overall selection: group collection and confirmed-first selection must be explicit invariants.
- Repeatability audit conflates product-state center differences with stochastic residuals; every diagnostic must consume chronological within-block residuals.
- R1 treats a logical capture as the only audit unit; physical attempts need an append-only evidence unit and pre-call reservation.
- V2 runner integration stopped at acquisition; analyzer dispatch and schema validation must be version-specific and fail closed.

## Regression surfaces required by PLAN 8.7.18

- Confirmed high-objective face wins over unconfirmed low-objective face.
- Started confirmation groups collect all measurable n=3/n=5 samples; partial rejection evidence and final verification are explicit.
- Stable H120/S100 and H300/S100 with distinct centers pass; within-command trend/bimodal/dominance/A-B shift fail deterministically.
- Fake formal v2 sentinel runs pass through the real analyzer; waiting/hash/cleanup/count/sequence corruptions reject.
- R1 retained base/reacquire attempts, command/readback, counters, pre-rejected one-over, and finalizer branches are independently audited.

## Next diagnostic

Run the final full-suite and artifact/hash checks, then move this note to resolved if all P7-R0C acceptance surfaces remain green.

## Implemented corrections

- Multiseed selection now constructs a confirmed-only pool before considering unconfirmed best-valid samples.
- Confirmation groups retain every measurable n=3/n=5 capture, record partial measurement rejection, and use at most the two declared groups; never-feasible solves verify the best-valid command with an unspent group.
- Repeatability trend runs in real chronology within each centered state/command/block; pooled bimodality and dominance consume only centered residuals, and A/B center shift is reported separately.
- `analyze_strip_hsi_pilot` now requires explicit v1/v2 dispatch. V2 validates the formal policy hash/status, reference blocks, multiseed selection, budgets, confirmation size, and three result layers.
- P7-R1 now retains `capture-attempts.jsonl`, uses a distinct capture/readback sequence for weak reacquisition, passes the remaining physical allowance into the shared adapter, and stores base/auto/reacquire counters.
- The P7-R1 analyzer reads command and attempt evidence, verifies each retained CR3/report/readback/settling sequence, reconstructs all counters, and keeps the 250 cap marked `proposed_not_frozen`.

## Regression evidence

- Focused P7 suite: 79 tests, command exit 0.
- Deterministic tests cover confirmed-first selection, full and partial confirmation groups, never-feasible final verification, n=5 collection, distinct stable command centers, real trend/bimodal/dominance, A/B shift, fake formal v2 sentinel analysis, retained weak reacquire evidence, cap precheck, counter/command tamper, and cleanup failures.
- Full suite: `395/395` passed in 81.545 seconds under the repository-documented verbose unittest command.
- `compileall`, four wrapper `zsh -n` checks, `git diff --check`, and `codegraph sync` passed.
- Final readiness keeps the P7-R1 250-CR3 absolute cap marked `proposed_not_frozen`; no device/environment/network path was used.
