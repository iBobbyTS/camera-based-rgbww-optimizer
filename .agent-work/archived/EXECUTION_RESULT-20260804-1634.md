# Reviewed EXECUTION_RESULT archive metadata

- Archive status: `REVIEWED_ACCEPTED_HISTORICAL_NON_EXECUTABLE`
- Archive timestamp UTC: `2026-08-04T16:34:00Z`
- Archive owner: `Planner`
- Archive type: `EXECUTION_RESULT`
- Reference task: `REF-G4-06-RAY-R6`
- Contract: `G4-RAY-R6-FORMAL-TERMINAL-EVIDENCE-ENGINEERING-V1`
- Reviewed scope: exact six-path offline engineering candidate authorized by the reviewed PLAN
- Source checkpoint: `f0d957da554d28443e66f235ca9721ace886165f`
- Source tree: `ca244cda8a7dc337c255e1f53359a121b64617d5`
- Source body bytes: `14017`
- Source body SHA-256: `8038dcc32db5a162315a6f6d211ea9d1a8aba35e2b88d169c99a4113beda7b12`
- Terminal disposition: `ACCEPTED_G4_06_FORMAL_TERMINAL_EVIDENCE_ENGINEERING_CANDIDATE_WAITING_ORCHESTRATOR_CODE_CHECKPOINT`
- Evidence pointers: activation topology exact; strict machine `1/1`; independent targeted `8/8`; focused `207/207`; final full suite `972/972`; source identities recorded in archived body
- Exact next stop: `WAITING_ORCHESTRATOR_ACCEPTED_CODE_CHECKPOINT`
- Historical execution authority: `historical_non_executable`

---

# EXECUTION_RESULT

## Status request

`READY_FOR_PLANNER_G4_06_FORMAL_TERMINAL_EVIDENCE_ENGINEERING_REVIEW`

- Reference task: `REF-G4-06-RAY-R6`
- Contract: `G4-RAY-R6-FORMAL-TERMINAL-EVIDENCE-ENGINEERING-V1`
- Planner stop: `RETURN_FOR_G4_06_FORMAL_TERMINAL_ENGINEERING_REVIEW`
- This is an engineering candidate only. No formal acquisition, device access,
  release consumption, analysis, retained-R3 replay, or later-stage execution
  occurred or is authorized by this handoff.

## Activation topology

- Activation HEAD: `f0d957da554d28443e66f235ca9721ace886165f`
- Direct parent: `db8188785079f15837c02d2d4632ed7a17543832`
- Activation tree: `ca244cda8a7dc337c255e1f53359a121b64617d5`
- Subject: `docs(plan): activate ray r6 terminal evidence engineering`
- Activation changed paths, exact:
  - `.agent-work/FULL_PLAN_REFERENCE.md`
  - `.agent-work/PLAN.md`
- Branch: `main`
- Intake worktree was clean.
- GUIDE SHA-256 remained
  `659152f6c0ae69c90c701de4e57c352d771e4f0bf75cf9410271ba0a94200e35`.

## Maintainability preflight and ownership

The pre-edit CodeGraph query traced the production path through
`run_production_cli_launch -> run_validated_td_b_r6_runtime_contract ->
run_authorized_plan -> execute_plan`. Existing acquisition, RAW measurement,
physical-return, cleanup, and capture-ledger owners were reusable. Putting the
terminal replay and serialization policy directly into the already-large
`measure_p7_thermal_diagnostics.py` would have enlarged its coordinator role,
so the implementation added one bounded owner:

- `p7_td_b_r6_terminal.py`: the only Ray-R6 terminal evidence owner. It owns
  exact wrapper argv classification, capture-ledger projection/replay,
  independent final-zero evidence, artifact identity/inventory replay, and the
  unique terminal audit/seal.
- `measure_p7_thermal_diagnostics.py`: only detects the exact materialized R6
  contract, projects existing RAW quality evidence, delegates the post-capture
  validator once, and promotes non-pass R6 Python cleanup to execution failure.
- `run-p7-thermal-diagnostics.zsh`: only consumes the repo-owned exact mode and
  enforces shell effect order; it does not implement terminal JSON semantics.

The owner reuses `thermal.validate_td_b_r6_capture_ledger`, existing RAW
observer reports, `control.all_off`, both-off/readback semantics, and
`p7_retained_r3_provenance_io`. No acquisition adapter, controller, scientific
validator, serializer, release owner, or analysis owner was duplicated.

Post-edit `codegraph sync` completed twice as the implementation converged. The
final sync reported `Modified: 2` Python files and the final query found:

- `validate_post_capture_ledger`: one production caller in
  `measure_p7_thermal_diagnostics.py`;
- `classify_wrapper_argv`, `run_independent_final_zero`, and
  `finalize_terminal`: only the single terminal module/CLI owner;
- no second Ray-R6 terminal seal owner.

## Effect-order and evidence closure

Production R6 execution now follows this order:

1. all 16 existing capture/physical-return/quality/readback/timing checks;
2. exact formal/ambient/physical budget checks;
3. exact R6 ledger projection bound to one root, R6 origin, frozen shutters,
   exact IDs/order, CR3/sidecar remote identities, and 58-feature quality;
4. one call to `thermal.validate_td_b_r6_capture_ledger(...,
   selected_c_shutter="1/2500")` before commands audit or final completion;
5. Python cleanup in the existing `finally`; exact status/2-step non-pass is
   promoted to failure and leaves `run.status=failed`;
6. wrapper waits for the child, runs shell all-off once, independent final-zero
   once, terminal finalize once, then writes wrapper result/state and exits.

Terminal replay reads exact regular evidence, replays the existing ledger
validator once, reprojects each retained patch-statistics report, binds every
CR3/sidecar/report and direct ledger artifact by path/bytes/SHA/device/inode/mode,
and rejects missing, extra, cross-root, symlink, or identity-drift artifacts.
PASS requires 16 logical/16 physical, setup 0, ambient 0, all three cleanup
gates, child exit 0, no signal, retry 0, and analysis/strip-nonzero call count 0.
Every tested hard failure writes only a FAIL seal with
`accepted_hard_failed_formal_attempt`, `formal_pass=false`, and retry 0.

The exact wrapper trigger requires parsed values for experiment
`p7_td_b_command_switch_history_v1`, source `ray`, phase `formal`, stage-gate
package, and code checkpoint. Duplicate/missing values and wrapper-owned argv
conflicts fail closed. Wrong experiment/source/phase, setup, strip, dry-run,
missing stage-gate, and similar strings retain legacy behavior and do not call
the independent-zero or terminal-finalize evidence boundaries.

## Positive and negative test mapping

Positive coverage proves:

- exact 16-row ledger replay through the existing validator;
- validator call count one while `run.status` is still `running`;
- exact wrapper child -> shell cleanup -> independent zero -> terminal finalize
  -> wrapper-result/state order;
- PASS terminal seal with complete static and dynamic artifact identities;
- exact R6 trigger and legacy/near-miss isolation.

Negative coverage proves fail-closed behavior for missing/reordered rows,
cross-root and R5 provenance, wrong shutter, quality and physical-return drift,
non-pass Python cleanup, shell cleanup failure, independent-zero failure, child
failure, INT/TERM/HUP, terminal finalizer failure, missing/symlink/extra/identity-
drift artifacts, duplicate/conflicting argv, and second seal attempts. Tests
also assert retry/alternate root/analysis/strip nonzero/release/TD-C calls stay
zero where applicable.

## Superseded initial candidate validation

All counts in this section, including the earlier `970/970` full suite, are
`SUPERSEDED_CANDIDATE_VALIDATION`. Orchestrator review identified additional
terminal-evidence closure requirements after that candidate. They are retained
only as execution history and are not the final validation claim.

The PLAN's requested pytest entrypoint was unavailable in the repository venv:

```text
.venv/bin/python -m pytest -q tests/test_p7_td_b_r6_terminal.py
-> No module named pytest
```

No dependency was installed and no network was used. With Orchestrator
direction, all test validation used the same `.venv/bin/python` and the
repository's unittest-compatible test modules:

1. Targeted final:

   ```text
   .venv/bin/python -m unittest tests.test_p7_td_b_r6_terminal
   Ran 5 tests in 0.286s — OK
   ```

2. Focused final:

   ```text
   .venv/bin/python -m unittest tests.test_p7_td_b_r6_terminal tests.test_p7_thermal_diagnostics tests.test_p7_td_b_r6_stage_gate tests.test_p7_td_b_r6_contract
   Ran 205 tests in 260.251s — OK
   ```

3. Compile and shell syntax:

   ```text
   .venv/bin/python -m py_compile src/camera_based_rgbww_optimizer/optimization/p7_td_b_r6_terminal.py src/camera_based_rgbww_optimizer/optimization/measure_p7_thermal_diagnostics.py tests/test_p7_td_b_r6_terminal.py tests/test_p7_thermal_diagnostics.py
   zsh -n tmp/run-p7-thermal-diagnostics.zsh
   PASS
   ```

4. CodeGraph:

   ```text
   codegraph sync
   codegraph explore "Where are classify_wrapper_argv, validate_post_capture_ledger, run_independent_final_zero, and finalize_terminal called, and is there any second Ray R6 terminal seal owner?"
   PASS
   ```

5. Diff and scope:

   ```text
   git diff --check
   PASS
   ```

   Before this ER write, the only changed code/test/wrapper paths were the five
   authorized implementation paths. The final expected path set adds only this
   `EXECUTION_RESULT.md`, for six authorized paths total.

6. Unique fresh full suite:

   ```text
   .venv/bin/python -m unittest discover -s tests
   Ran 970 tests in 378.948s — OK
   ```

The initial focused diagnostic reported 8 failures and 8 errors. Six wrapper
subcases were caused by a fake-harness experiment-ID constant; the remaining
historical lineage failures came from tests reading the intentionally changed
working wrapper instead of the immutable checkpoint bytes bound by old setup
evidence. The bounded correction changed only test harness replay/expectations;
the failing subset passed, and the complete focused suite then passed. This was
not a production retry or a new task/root.

## Orchestrator-review bounded correction and final validation

The same `REF-G4-06-RAY-R6` terminal-evidence owner was corrected without a
new task ID, corrective suffix, experiment root, or production/formal call.
The final implementation now additionally proves:

- every command row exactly follows the materialized-plan command grouping and
  binds source/state/exact-command hash; both applied response and readback are
  replayed through `hsi_source_evidence.validate_ray_readback`;
- every isolation gate has the exact plan-derived ID/order, nonempty off command,
  and embedded strip/Ray evidence replayed through
  `hsi_source_evidence.validate_both_off` with the frozen curve;
- run budgets, contiguous physical indices, unique current-root CR3/sidecar
  paths, and unique remote capture/request IDs are recomputed rather than
  inferred from pass markers;
- all 16 thermal covariates are validated by
  `thermal.validate_covariate_record`, bound to plan source/state/hash/order,
  and checked by `thermal.audit_chronology`;
- every retained capture reuses
  `measure_p7_thermal_diagnostics._validate_returned_sidecar` to bind the CR3,
  sidecar, remote IDs, bytes/SHA, timing metadata/receipt, accepted timing tier,
  provenance/status, estimate method, and within-group observed chronology;
- PASS inventory is closed over exact regular files plus necessary parent
  directories, rejecting extra empty directories, symlinks, and special nodes;
  FAIL seals preserve every safely readable regular artifact identity without
  following unsafe entries;
- cleanup statuses report their actual parsed Python/shell/independent-zero
  result after non-cleanup failures;
- exact-R6 wrapper result/state write failures return `73` and never retain a
  completed terminal status; legacy wrapper behavior remains unchanged;
- `returned-summary.json` is written canonically and exclusively once by the
  terminal owner, binds the root identity, capture/physical counts and order,
  CR3/sidecar/remote identities, and retry `0`, is included in terminal
  audit/seal identities and the closed inventory, and records
  `partial_or_invalid` on hard failure. A summary serialization failure is
  attempted once and makes the finalizer return nonzero.

The PLAN's GUIDE §7.7 exposure-policy alternative is satisfied by an immutable
reference rather than a duplicated `exposure-policy.json`: the materialized
plan binds frozen shutters plus immutable template/descriptor/source
attestation identities. No new exposure-policy semantic owner was added.

Final validation on the corrected production tree:

1. Targeted:

   ```text
   .venv/bin/python -m unittest -v tests.test_p7_td_b_r6_terminal tests.test_p7_thermal_diagnostics.P7ThermalDiagnosticsTests.test_r6_wrapper_terminal_effect_order_and_failure_precedence tests.test_p7_thermal_diagnostics.P7ThermalDiagnosticsTests.test_r6_wrapper_terminal_artifact_write_failure_is_nonzero_and_not_complete
   Ran 8 tests in 4.510s — OK
   ```

2. Focused:

   ```text
   .venv/bin/python -m unittest tests.test_p7_td_b_r6_terminal tests.test_p7_thermal_diagnostics tests.test_p7_td_b_r6_stage_gate tests.test_p7_td_b_r6_contract
   Ran 207 tests in 256.582s — OK
   ```

3. Compile, shell, diff, and CodeGraph:

   ```text
   py_compile (both production modules and both test modules) — PASS
   zsh -n tmp/run-p7-thermal-diagnostics.zsh — PASS
   git diff --check — PASS
   codegraph sync — PASS (Modified: 2; 94 nodes)
   focused CodeGraph call-path query — PASS
   ```

4. Unique valid final full suite:

   ```text
   .venv/bin/python -m unittest discover -s tests
   Ran 972 tests in 374.379s — OK
   ```

One full-suite process had already started when the final returned-summary
review finding arrived. It was immediately interrupted with exit `130` and is
explicitly superseded/incomplete, not a validation result. The `972/972` run
above is the only valid final full-suite result for the final production tree.

Final implementation/test source SHA-256 identities:

- `measure_p7_thermal_diagnostics.py`:
  `f6c5f6e4e002863d34eb39a578b56e92a31ad70c907570d3537152d73030f8e3`
- `p7_td_b_r6_terminal.py`:
  `4e38d97000f7e908fb56db5ac731e28182f7759f45b394881d66a1791a144e3e`
- `run-p7-thermal-diagnostics.zsh`:
  `a82a6689e6fe4b4d403f3b84c8612cf79c7d35463cd89047ccbf9febd43d52df`
- `test_p7_td_b_r6_terminal.py`:
  `034d4b828c73880d47b390ea63251ee408299cca95bd5a0071b74be12e7cc1d5`
- `test_p7_thermal_diagnostics.py`:
  `ac76eba85ab504d588a08cdee317670bd8a4b421cd6660433eb10c707baef47e`

## Scope and access counters

- Real device calls: `0`
- Real camera calls: `0`
- Real Ray calls: `0`
- Real strip calls: `0`
- Network calls: `0`
- Formal captures/launches: `0`
- External experiment payload/root reads: `0`
- Retained-R3 reads/consumption: `0`
- Release consumption: `0`
- Analyzer calls: `0`
- TD-C calls: `0`
- Firmware/deploy operations: `0`
- New experiment roots: `0`
- New task IDs/corrective suffixes: `0`
- Commits created by Executer: `0`

Relative to activation HEAD, `.agent-work/PLAN.md`,
`.agent-work/FULL_PLAN_REFERENCE.md`, GUIDE/RESEARCH, config, the scientific
owner `p7_thermal_diagnostics.py`, and analyzer
`analyze_p7_thermal_diagnostics.py` are unchanged. PLAN and FULL remain
read-only to the Executer.

## Proposed disposition

`READY_FOR_PLANNER_G4_06_FORMAL_TERMINAL_EVIDENCE_ENGINEERING_REVIEW`

The Planner should review this candidate against the live PLAN. Acceptance here
must remain engineering-only. The Orchestrator must create the required focused
immutable code checkpoint before any later Planner package may authorize formal
acquisition. No real formal execution is authorized or implied by these offline
tests.
