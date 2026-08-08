# PLAN-FULL — GUIDE 4 科学优先去工程化与执行

**Status:** executable after Human adopts this plan
**Scientific target:** complete GUIDE 4 through its prescribed scientific stop branch or TD-C core
**Current next scientific action:** `P7-TD-B-RAY-OP600-EXPOSURE-GUARDED-FORMAL-R6`
**Engineering sections allowed before Ray R6:** exactly 2 (`E1`, `E2`)
**Runtime principle:** no new runtime layer; existing measurement CLI is the only execution owner

## 0. Human implementation override

Human explicitly replaces GUIDE 4's implementation-only lineage/release/package/stage-gate machinery with a minimal reproducibility contract. This does **not** modify the scientific or safety contract.

Keep unchanged:

- R5 hard failure; retained 11 diagnostic only; no R5/R6 pooling.
- Identity RAW, `R/G1/G2/B`, 58 features, frozen quality thresholds and uncertainty.
- A/D/B/C states and exact R6 order.
- Exposures: A `1/5000`, D `1/6400`, B `1/8000`, C `1/2500`.
- Ray-only R6: 16 logical/physical, launch 1, retry 0, no ambient, strip zero.
- No auto exposure, weak reacquire or mid-run shutter change.
- 600 s is an operational transient, not steady.
- Ray history pass unlocks strip only; combined pass unlocks TD-C core only.
- Sentinel, remaining 9, boundary, holdout, Gate-6, P8 and LUT installation remain locked.
- Python/shell cleanup, final zero readback and failure evidence.

Replace:

- successor lineage release → `experiment-spec.json` + input hashes + run manifest;
- stage-gate package → direct protocol-specific CLI;
- terminal seal → run/ledger/wrapper/cleanup artifacts;
- PLAN/FULL and Git topology authority → human-readable planning only; commit recorded as metadata;
- predevice/E2/readiness attestation → direct fake-backend integration and behavior tests.

Production must never read `.agent-work`, AGENTS/Advisor Markdown, Git branches/parents/trees, release packages or lineage owners.

## 1. Starting point and Git

Verified refs:

```text
origin/main = 390321a6e903d86b167519e1c801e4046d7ba709
origin/codex/backup-guide4-pre-deengineering-20260806 = same
failed terminal branch = 60ffc57e0589ca5bbd041ba3a5c7311c8321aac9
```

Do not merge `60ffc57` into main. Do not create another backup. Create:

```bash
git fetch origin
git switch -c codex/guide4-science-path-v2 \
  390321a6e903d86b167519e1c801e4046d7ba709
```

Rejected commits `6b3a10d`, `00312b8`, `e629394`, `6234ffc` are historical evidence only. Do not patch, cherry-pick or copy their runtime design.

Remove tracked `.agent-work`; add `.agent-work/` to `.gitignore`. Codex may use local ignored PLAN/scratch files. Git history already preserves old plans and reviews.

## 2. Prohibited architecture

Do not add or preserve as execution authorities:

```text
runtime owner
lineage owner
release owner/consumer
stage gate/package
terminal seal/attestation
readiness/predevice/E2 package
PLAN/FULL machine parser
Git ancestry/branch/path ownership
source string or AST identity gate
historical archive as runtime input
generic workflow for future stages
```

Do not create a replacement `p7_guide4_science_runtime.py`. The previous failure came from adding a new generic layer while leaving old execution semantics alive.

Target owners:

```text
p7_thermal_diagnostics.py         protocol, sequence, budgets, quality/ledger validation
measure_p7_thermal_diagnostics.py only device execution CLI
analyze_p7_thermal_diagnostics.py only analysis CLI
run-p7-thermal-diagnostics.zsh    process trapping and shell cleanup only
```

## 3. E1 — Direct scientific execution path

### Scope

1. Rewrite root `AGENTS.md` to a short science/safety document. Remove role state machines, archive contracts, package/review budgets and runtime PLAN semantics.
2. Add a direct `ray-r6` CLI path to the existing measurement module.
3. Build the exact R6 spec directly from frozen scientific configs.
4. Simplify the wrapper.
5. Extract only critical quality/ledger logic from `p7_td_b_r6_terminal.py`; do not preserve a terminal-owner abstraction.

### Direct CLI behavior

Equivalent user path:

```bash
python -m camera_based_rgbww_optimizer.optimization.measure_p7_thermal_diagnostics \
  ray-r6 --dry-run --output-dir <absolute-root> --run-name <name>

python -m camera_based_rgbww_optimizer.optimization.measure_p7_thermal_diagnostics \
  ray-r6 --execute --allow-device-control \
  --human-authorization P7-TD-B-RAY-OP600-EXPOSURE-GUARDED-FORMAL-R6 \
  --output-dir <absolute-root> --run-name <name>
```

The runner:

- loads exposure/observer/feature/uncertainty/operating configs;
- validates scientific schemas/hashes and selected C shutter;
- creates a fresh run root;
- writes `experiment-spec.json` before device access;
- uses the existing real apply/readback/capture/RAW/ledger/cleanup mechanics;
- records commit and clean/dirty status as metadata only;
- does not read old EQ root, release, stage gate, PLAN or Git ancestry;
- dry-run has zero network/device effects.

### Wrapper

Keep only:

- child start/wait;
- signal propagation;
- exit status;
- shell `all_off` on every exit;
- `wrapper-result.json`.

Remove terminal classification/finalization and old CLI compatibility.

### E1 behavior tests

Must cover:

- exact 16 IDs and order;
- exact A/D/B/C shutters;
- fake backend full 16 captures;
- physical cap 16;
- strip zero before each capture and at exit;
- no ambient/auto exposure/weak reacquire/shutter mutation;
- fresh root;
- R5/R6 pooling rejection;
- hard failure matrix: clipping, near-noise, nonfinite, invalid pixels, missing/mismatched exposure;
- Python and shell cleanup on success, exception and signal;
- analyzer can consume the generated run.

### E1 acceptance

- direct fake R6 passes;
- no production import of stage gate;
- no production read of `.agent-work`, Git topology or release package;
- one independent review; ordinary findings are fixed in E1, not terminalized.

Commit only substantive source/test/docs changes. No plan/status/archive commits.

## 4. E2 — Delete governance and finish direct Guide 4 paths

### Delete production governance

Delete these families after direct-path tests prove they are unused:

```text
p7_td_b_r6_stage_gate.py
p7_td_b_r6_terminal.py
p7_retained_release_audit.py
p7_successor_{lineage,predevice,zero_readiness,e2}.py
utils/agent_work_machine_contract.py
utils/p7_retained_r3_*.py
config/hsi/p7-governance-lineage-successor-v1.json
```

Do not move them into a live archive directory.

### Shrink existing modules

From `p7_thermal_diagnostics.py`, remove lineage, release, Git/checkpoint, agents-policy, owner-map, public-successor and package-validation code. Keep only protocol/science/timing/covariate/quality logic.

From `measure_p7_thermal_diagnostics.py`, remove setup-release, lineage qualification, stage-gate package, predevice/E2/readiness, old CLI compatibility and completed EQ-R6 orchestration branches. Keep real acquisition mechanics and direct protocol commands.

From analyzer, remove release/commit/owner validation. Keep data integrity, chronology, history, combined and TD-C scientific decisions.

### Delete governance tests

Delete:

```text
test_agent_work_machine_contract.py
test_p7_td_b_r6_stage_gate.py
test_p7_td_b_r6_contract.py
test_p7_retained_release_audit.py
test_p7_successor_*.py
test_p7_retained_r3_*.py
```

Delete tests of Markdown parsers, branch/tree identity, source strings, package ownership, release qualification, terminal seals and old CLI compatibility.

Consolidate tests around protocol, acquisition, analysis and wrapper behavior.

### Build downstream direct paths

In the same existing CLI, implement but keep scientifically locked:

```text
strip-td-b
td-c-core
```

- strip accepts a Ray R6 analysis artifact only when it declares the exact scientific pass.
- TD-C accepts combined analysis only when it declares pass.
- Prerequisites validate schema, experiment ID, content hash and scientific status only.
- No release/package/lineage materialization.

Add fake-backend tests for both paths.

### E2 final validation

Run once:

- remaining full unit suite;
- compileall;
- wrapper syntax;
- `git diff --check`;
- fake Ray R6, strip TD-B and TD-C integrations.

CodeGraph is optional, not a gate.

### E2 acceptance

- all listed governance code/tests removed;
- `.agent-work` untracked and ignored;
- direct Ray/strip/TD-C paths tested;
- remaining full suite passes once;
- one review; fixes stay inside E2;
- next action is S1 Ray R6. No third engineering section is allowed.

## 5. S1 — Ray R6 formal

Exact protocol:

```text
experiment_id = P7-TD-B-RAY-OP600-EXPOSURE-GUARDED-FORMAL-R6
source = ray
strip = zero throughout
ambient = 0
formal/physical = 16/16
launch/retry = 1/0
steady_claim = false
```

Capture IDs:

```text
000-ray-a0-t600
001-ray-d-t60
002-ray-d-t120
003-ray-d-t300
004-ray-d-t600
005-ray-a-after-d-t600
006-ray-b-t60
007-ray-b-t120
008-ray-b-t300
009-ray-b-t600
010-ray-a-after-b-t600
011-ray-c-t60
012-ray-c-t120
013-ray-c-t300
014-ray-c-t600
015-ray-a-after-c-t600
```

Artifacts minimally include spec, run, command/capture/physical ledgers, isolation, covariates, quality, audit, cleanup, wrapper result and CR3 hashes.

Branches:

```text
engineering_invalid:
  no scientific conclusion; no automatic retry; report exact invalidity

formal_quality_hard_fail:
  accepted scientific negative; strip locked; no threshold/exposure/frame changes

history_fail:
  accepted scientific negative; strip locked

quality_and_history_pass:
  unlock S2 only
```

R5 frames are never pooled or substituted.

## 6. S2 — New strip TD-B

Only after Ray pass:

- new root;
- frozen strip commands and observer contract;
- 16 formal captures and 600 s return anchors;
- Ray zero during strip captures;
- Ray R6 linked by artifact hash only;
- no R5 root consumption.

Quality/history fail is a scientific negative and locks combined/TD-C. Pass enters S3.

## 7. S3 — Combined operational-600 gate

Pure analysis. Output:

```text
p7-td-b-operational600-analysis-v1.json
```

Must state:

```text
operating_envelope = developer_selected_operational_600s_transient_v1
operational_dwell_s = 600
steady_claim = false
TD_A_status = settling_not_demonstrated_by_600
Ray and strip return-anchor compatibility
```

Pass creates a simple `p7-operating-envelope-v3.json` containing scientific conditions and source run hashes only. Fail locks TD-C.

## 8. S4 — TD-C core

Only after combined pass:

```text
H120/S100
600 s observation dwell
S1 Ray -> strip
S2 strip -> Ray
S3 Ray -> strip
S4 strip -> Ray
8 formal captures
```

Report only as `order-balanced comparison under operational_600s_transient`; never call it steady ABBA or drift elimination.

After core, stop device progression and prepare Advisor material. Do not automatically run endpoint expansion or sentinel.

## 9. S5 — Advisor handoff and GUIDE 4 completion

Report:

- deengineering diff and remaining test suite;
- exact runtime/reproducibility contract;
- Ray R6 result;
- conditional strip, combined and TD-C results;
- exact stop branch for unentered stages;
- reference epoch status;
- commit/config/run/artifact hashes;
- downstream locks.

GUIDE 4 is executed to its prescribed terminal branch when a valid Ray/strip/combined scientific failure is obtained or TD-C core is completed. An engineering-invalid R6 is a stopped execution, not a scientific result.

## 10. Minimal reproducibility contract

Required:

- code commit and environment versions;
- exact CLI;
- scientific input paths/hashes;
- exact experiment spec, commands, shutters, sequence and budgets;
- device readbacks and monotonic timing/covariates;
- CR3 bytes/hashes and recorded exposure;
- source isolation, quality, cleanup and final zero;
- analyzer input/output hashes and decision reason.

Not required:

- release or lineage owner;
- stage-gate package;
- terminal seal;
- PLAN hash;
- Git ancestry/branch authority;
- public validator family;
- archive package.

## 11. Review and stop rules

Per engineering section: implement → focused tests → one review → fix findings in the same section → affected retest. A second review is allowed after fixes; two consecutive clean reviews are not required.

Do not terminalize ordinary bugs such as imports, parser options, wrapper references, fake adapters, dead branches, skipped old bodies or test failures.

Stop only when:

- frozen observer/features/threshold/uncertainty/exposure/sequence/budget/600-s semantics must change;
- source isolation or cleanup cannot be guaranteed;
- device evidence is physically invalid and unclassifiable;
- GUIDE has no scientific branch for the result;
- a still-locked stage would be entered.

## 12. Unique next action

Create `codex/guide4-science-path-v2` from `390321a...` and execute **E1**. Do not continue any rejected deengineering candidate and do not design another runtime layer.
