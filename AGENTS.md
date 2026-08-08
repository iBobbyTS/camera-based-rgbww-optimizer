# Camera-Based RGBWW Optimizer Codex Instructions

## Local Lab Scope

This project is used only for the Human-owned and Human-maintained local photography and lighting calibration lab. Its connection targets are the RGBWW fixture, camera bridge, and reference light in that same local lab.

## Language

- Reply in Chinese by default unless the user explicitly asks for another language.
- Write implementation plans in Chinese by default.

## Project Scope

- This is a local-first camera-based RGBWW optimizer project.
- The default target ESPHome RGBWW device name is `bedroom-rgbww-strip`.
- The attached fixture is a PWM RGBWW strip. The first milestone is proving independent control over all five physical channels.
- The later calibration workflow uses a camera, black/white/18% gray cards, a 24-color chart, and an Aputure Amaran Ray120c reference light at 100% brightness.

## Project-Specific Precedence And Minimal Engineering

- Everything in this repository is in service of completing the scientific
  objective in the active `GUIDE.md`. Engineering work is a means to that
  objective, not an independent deliverable or a reason to create additional
  orchestration layers.
- These project rules may override generic custom-instruction ceremony for a
  non-trivial change or a mandatory code-review loop when that ceremony would
  add process without materially improving scientific correctness, safety,
  evidence integrity, or maintainability. Keep the smallest implementation,
  validation, and evidence package that safely advances the GUIDE stage.
- This exception does not waive Human authorization for high-risk operations,
  real cleanup requirements, credential protection, GUIDE/RESEARCH immutability,
  or validation needed to support a scientific conclusion.

## Scientific Throughput Guardrails

- Everything serves the active GUIDE scientific objective. Scientific progress is
  an accepted measurement, capture, analysis result, valid scientific negative, or
  a newly unlocked GUIDE experiment; code, tests, plans and commits are engineering
  evidence only.
- Any engineering-only work must name the single concrete blocker it removes from
  the next scientific action. E1 and E2 are the only pre-Ray engineering sections in
  the current Human-approved route; after E2 the next action is the Ray R6 experiment.
- Ordinary implementation and test problems stay in the current E1/E2 worktree and
  are fixed there until meaningful behavior tests pass. No retry or validation budget
  turns an ordinary fix into a stop or a request for a new architecture boundary.
- Do not insert optional refactors, generalized frameworks, repeated clean-room runs,
  or extra review campaigns between readiness and the scientific action. Run the
  final validation once at the E2/science boundary, with extra checks only when a
  concrete safety or scientific risk requires them.
- The Supervisor is invoked only by a Human point-in-time request and reports
  engineering progress separately from `science_delta`; it does not dispatch routine
  work. Advisor input is requested only for unresolved scientific questions.

## Execution Policy (without a runtime state machine)

The repository has no mandatory role execution state machine. Human, Advisor,
Supervisor, Orchestrator, Planner and Executer are collaboration roles, not
machine-state owners or sequential approval gates.

### Human

- Owns the lab, scientific objective, and high-risk device authorization.
- May explicitly override non-scientific execution instructions in GUIDE without
  editing GUIDE/RESEARCH.

### Advisor

- Owns scientific guidance and research reasoning through immutable GUIDE/RESEARCH.
- Answers color science, measurement science, interpretation, and scientific branch
  questions; it does not own code architecture or routine execution.

### Supervisor

- Acts only when Human asks for a progress inspection.
- Reports progress speed, abnormal loops, science delta, completed work since the
  previous check, and whether correction is needed.
- May request Advisor input only for a genuinely unresolved scientific question.
- If correction is needed, provides a copyable prompt; it does not dispatch routine
  work or become an execution approval gate.

### Orchestrator

- Owns the direct, low-density implementation and experiment route toward GUIDE.
- May use Planner and Executer as optional helpers. It may also execute a small
  coherent batch itself when that is clearer and faster; no handoff is mandatory.
- Keeps one current worktree boundary, fixes ordinary implementation/test issues in
  that boundary, and moves to the scientific action as soon as safety prerequisites
  are satisfied.
- Does not modify GUIDE/RESEARCH, infer dangerous authorization, or create parallel
  runtime/framework layers.

### Optional Planner / Executer cost split

- Planner may use a higher-reasoning profile to choose the smallest scientifically
  useful implementation boundary and anticipate semantic risks.
- Executer may use a lower-cost profile for deterministic edits and checks already
  decided by the Orchestrator.
- They are not required to create or validate orchestration artifacts and do not
  form a separate approval loop. Ordinary issues are fixed in the current E1/E2
  worktree until the meaningful behavior tests pass.

### Local scratch and evidence

- `.agent-work/PLAN.md`, `.agent-work/PLAN-FULL.md`, debug notes and review notes are
  optional local scratch. They are not production inputs, test inputs, Git commit
  authorities, or release gates. Keep scratch notes short and disposable.
- Reproducibility belongs in experiment specs, input/config hashes, run/ledger/
  cleanup artifacts, source commit metadata, and analyzer outputs. A scratch plan
  may summarize these but cannot authorize or block production code.

The normal flow is a single Orchestrator-owned batch: understand GUIDE and the
existing owner, implement the smallest direct behavior, add meaningful behavior
tests, run the required checks once, review only when it materially improves
correctness, then perform the next scientific action. Do not create a plan or
handoff for each command, test selector, file, assertion, or intermediate status.

The Advisor researches scientific questions and writes `GUIDE.md` plus `RESEARCH.md`
when scientific support is needed; those files remain immutable inputs and do not directly authorize execution.

The Orchestrator records the outcome in the smallest useful evidence file and
commits a coherent accepted code/evidence package. A rejected implementation is
simply fixed in the same worktree when the issue is ordinary; preserve a branch or
commit only when needed for recovery, not as a mandatory candidate-rejection
protocol.

The Human prepares the physical environment and explicitly authorizes dangerous
operations. Bounded experiments follow the scientific protocol and safety contract,
not a generated machine-state contract.

### High-Risk Device Authorization

- Human authorization is required for dangerous state-changing operations, including remote firmware upload or flash, remote deployment, destructive hardware changes, and any device operation outside the current written execution scope.
- Creating, validating, replaying, or consuming an offline setup/lineage release is a computation and provenance operation. It does not require Human authorization, and `production_release_usable=true` is not itself a hardware or formal-execution authorization.
- Read-only remote health/config/capability checks, device identity/state readback, and zero-state verification do not require separate Human authorization when they are explicitly bounded by the current execution notes and do not change device state beyond the declared zero/off cleanup.
- Turning Ray120c or the RGBWW fixture on or off does not require a separate Human authorization. This exception applies to light output control itself, including starting a bounded light operation already selected by the current execution notes, zero-state setup, and Python/shell cleanup.
- The current execution notes and the owning runner must still define or enforce the target, intensity, duration, source isolation, abort behavior, and Python/shell cleanup for any light operation. Removing the separate approval step does not permit widening those bounds.
- No role may infer authorization for firmware upload, remote deployment, destructive hardware changes, a broader intensity/range/duration, a new experiment, or a later stage from a release, a prior authorization, or a light-control exception.
- Computation and other work that does not access or control devices does not require Human approval.
- If Human approval is required for an operation outside the light-control exception, the Orchestrator records the authorized operation and its scope or bounds in the current execution notes. The same authorization must not be requested again for that exact operation.
- If a dangerous non-exempt operation is absent, ambiguous, expired, or does not cover the target, range, intensity, duration, or recovery path, the Orchestrator stops and asks the Human before proceeding. This stop does not apply to the release, read-only checks, or light-control exceptions listed above.
- Authorization for one named experiment or device operation does not authorize another experiment, firmware upload, broader range, higher output, or later stage unless the current execution notes explicitly say so. The light-control exception does not remove those scope and safety boundaries.

## Development Model

- Treat Python as the planned implementation language for optimizer and calibration tooling.
- Keep Python implementation modules under `src/camera_based_rgbww_optimizer/`: `control/` for device control, `optimization/` for measurement and calibration workflows, `utils/` for shared helpers/post-processing, and `interaction/` for local UI tools.
- Do not add root-level CLI compatibility wrappers. Use `python -m camera_based_rgbww_optimizer...` module commands and document them in `docs/README.md`.
- The project uses a minimal `pyproject.toml`; install locally with `.venv/bin/python -m pip install -e .`.
- Prefer local execution. Use Docker only when a concrete dependency requires it; if Docker is needed, use Colima and prefer `docker-compose`.
- Put all temporary data, probe outputs, decoded images, scratch virtual environments, logs, and other disposable artifacts under `/Volumes/4T/temp/rgbww-optimizer`. Do not create new temporary data under this repository's `tmp/` directory or the system `/tmp`.
- Repository `tmp/*.zsh` files are version-controlled execution wrappers, not temporary data; keep those wrapper sources in the repository while their run directories and logs live under `/Volumes/4T/temp/rgbww-optimizer`.

## Documentation

- Keep `docs/README.md` as the project source of truth for hardware assumptions, calibration decisions, validation workflow, and open questions.
- When behavior or calibration strategy changes, update `docs/README.md` or the relevant project skill in `.agents/skills/`.
- When a reusable project-specific method emerges, update the project skill under `.agents/skills/`.

## Implementation Quality

- Before changing behavior that touches device control, camera measurement, color conversion, optimizer solving, persistence, or shared state, inspect existing docs and implementations for a shared convention first.
- Add or update meaningful tests for functional changes unless the change is purely mechanical or documentation-only.
- Cover real behavior and edge cases; avoid tests that only execute code without checking outcomes.
- Run relevant checks before finishing when the environment permits it. If checks cannot run, explain the blocker.

## Safety

- Preserve user work. Do not remove, reset, or revert changes unless the user explicitly asks.
- This is an agent-led research project. The agent owns Git commit management: after completing and appropriately validating a discrete piece of work, create a focused commit without waiting for an additional human instruction. Do not push or create pull requests unless explicitly requested.
- Do not send destructive or high-brightness device-control sweeps without an explicit bounded range and a clear recovery path.
- When testing RGBWW channel output, keep initial PWM values low and ramp only after confirming channel order and thermal behavior.
- All scripts that can leave the ESPHome RGBWW fixture on must explicitly turn the light off before exiting; dedicated light-on/control scripts are the only exception.
