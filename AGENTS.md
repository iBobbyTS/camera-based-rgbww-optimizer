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
- For authorization conflicts, this file is authoritative: GUIDE, RESEARCH,
  PLAN and PLAN-FULL may describe scientific bounds, but they may not add a
  Human-authorization gate for an operation that this file classifies as
  non-high-risk. Human authorization remains mandatory only for the high-risk
  operations listed below. This precedence does not waive real cleanup,
  credential protection, GUIDE/RESEARCH immutability, or validation needed to
  support a scientific conclusion.

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

### Failure triage, retry policy, and the only permitted unresolved stop gates

- On any `error`, failed assertion, non-zero exit, timeout, interrupted run, or
  incomplete artifact set, first stop advancing the affected attempt. If a device
  may still be active, perform the bounded `all_off`/cleanup path and zero-state
  readback before debugging, retrying, editing evidence, or starting another run.
- Preserve the failed root, logs, command, exit status, cleanup evidence, Git
  identity, and completed-capture count. Never overwrite a failed root or describe
  captures that did not occur as scientific evidence.
- Classify the failure before choosing the next action:
  - `ENGINEERING_OR_HARNESS_FAILURE`: implementation exceptions, invalid selectors,
    missing fields/files, wrapper or analyzer defects, malformed commands, and
    contract mismatches that prevent the intended scientific protocol from running.
    Record `science_delta=none`, diagnose the concrete cause, fix it in the current
    worktree, add or update a meaningful behavior test, and first determine whether
    the existing run root and completed artifacts can be safely recovered. If they
    are intact and the protocol can resume without duplicating or mutating prior
    scientific observations, continue from that root; create a fresh root only when
    recovery is impossible or would make the evidence ambiguous.
  - `VALID_SCIENTIFIC_NEGATIVE`: the intended protocol actually ran and its frozen
    quality, history, coverage, or analysis criterion failed with trustworthy
    evidence. Preserve it as scientific progress. Do not weaken thresholds, alter
    exposure/frame selection, relabel it as an engineering failure, or automatically
    reacquire it. Follow the GUIDE's scientific branch; request Advisor input only
    when interpretation or the next scientific branch is genuinely unresolved.
  - `DEVICE_OR_SAFETY_FAILURE`: connection loss, unexpected device state, cleanup
    failure, source-isolation violation, or an out-of-bounds command. Make the
    equipment safe first, retain readback evidence, then diagnose. Use
    `HUMAN_GATE_REQUIRED` only when physical intervention or authorization for a
    high-risk operation is actually needed.
  - `INDETERMINATE_FAILURE`: use this only after safe relevant diagnostics cannot
    distinguish engineering, scientific, or physical causes. Route the unresolved
    concrete question to Human or Advisor according to the gate definitions below.
- A retry is never a blind rerun. Before retrying, state the diagnosed cause, the
  substantive correction or discriminating change, the evidence expected to prove
  it, and why the resumed or new attempt is safe. Run the smallest meaningful
  behavior check first, then recover the existing attempt when possible; otherwise
  start a fresh attempt without pooling or silently replacing prior data.
- Attempt counts apply to actual attempts at the same failure boundary, not to
  read-only inspection, cleanup, or a test that never entered the intended body.
  A changed stack trace alone is not scientific progress, but a demonstrated cause,
  corrected behavior, or newly discriminating evidence is a substantive change.
- Every failure report must state: classification, exact primary cause or unresolved
  question, captures completed/expected, `science_delta`, cleanup and zero-state
  result, Git/worktree state, whether a fresh retry is justified, and the next action
  or the single applicable unresolved gate.

- An implementation, validation, device, capture, or experiment attempt that fails
  is not by itself a terminal condition. Preserve the failed attempt and cleanup
  evidence, fix or narrow the identified cause, then retry in a fresh safe attempt.
  A run-level `retry=0` prohibits hidden in-run reacquisition or reusing/overwriting a
  failed root; it does not prohibit a new attempt after a substantive correction.
- Continue diagnosis and corrected retries while each attempt produces a substantive
  change: a different tested hypothesis, a corrected implementation or protocol, new
  discriminating evidence, or measurable movement of the failure boundary. Do not
  treat retry counts, validation budgets, review counts, candidate status, or an
  automation's fail-closed cleanup as permanent authorization barriers.
- Prohibit another retry only when either (a) three consecutive attempts at the same
  boundary produce no substantive change, or (b) the cause remains genuinely
  indeterminate after the safe, relevant diagnostics have been exhausted. Record the
  attempts and why they were materially unchanged or why the cause is indeterminate.
- An unfinished GUIDE route may stop only at one of two explicit unresolved gates:
  - `HUMAN_GATE_REQUIRED`: Human authorization for a high-risk operation,
    physical intervention, or an explicit goal/policy choice that cannot be
    resolved from the active GUIDE/PLAN is required. A GUIDE-only request for
    extra approval of bounded light/camera work is not this gate. Three materially
    unchanged non-scientific attempts or an indeterminate non-scientific cause
    are classified here.
  - `ADVISOR_GATE_REQUIRED`: a genuinely unresolved scientific interpretation,
    protocol, measurement-science, or scientific branch decision is required. Three
    materially unchanged attempts whose blocker is scientific, or an indeterminate
    scientific cause, are classified here.
- Every unresolved stop must name exactly one of those gates, state the concrete
  question or action needed to clear it, and explain why continued safe work cannot
  answer it. Planner review, Supervisor review, architecture-boundary language,
  retry/correction budgets, terminal candidate states, or ordinary test failures are
  not additional stop gates.
- A `HUMAN_GATE_REQUIRED` or `ADVISOR_GATE_REQUIRED` stop depends on an external
  decision and must not configure an automation merely to poll or self-wake for that
  decision. Record the exact unresolved question, mark the Goal `blocked`, and wait
  for the Human or Advisor response. The incoming response, not an automation, is
  what resumes the route.

### Long-running Goal handoff

- This section applies only to work that is expected to complete by itself, such as
  experiment execution, cooling, scheduled waiting, or long computation. It does
  not apply to `HUMAN_GATE_REQUIRED` or `ADVISOR_GATE_REQUIRED`.
- Any such self-completing task expected to take more than 10 minutes must run in a
  visible Terminal (for device or other long-running external work) or its
  equivalent persistent process.
  Before handing it off, perform three independent liveness checks; all three must
  pass. Then estimate the remaining completion time and configure a thread
  automation that can wake this thread and inspect the task state. Do not mark the
  Goal `blocked` until the automation has been created successfully.
- This `blocked` state is a temporary scheduling handoff, not a scientific or
  authorization stop. It does not replace `HUMAN_GATE_REQUIRED` or
  `ADVISOR_GATE_REQUIRED`, and it must not be used merely to hide an unresolved
  implementation failure. If the product Goal API imposes an additional system
  condition before changing a Goal to `blocked`, follow that system condition.
- When the thread is woken by the automation, or when the user sends a
  task-related message, first inspect whether the long-running task has completed.
  If it is incomplete, report only the current progress and end that response; keep
  the Goal in its scheduling handoff state. If it is complete, change the Goal back
  to `active` and continue the next PLAN step.
- For this handoff, `complete` means that the monitored process has terminated,
  whether it succeeded, failed, timed out, or was interrupted. A failed terminal
  state is not an incomplete long-running task. Delete the automation that no longer
  has a live process to monitor and change the Goal to `active` before applying the
  failure-triage rules above.
- If the terminated task is an `ENGINEERING_OR_HARNESS_FAILURE` with an identified
  cause and no Human or Advisor gate, continue in the same resumed turn: make the
  smallest direct fix, add or update the meaningful behavior test, validate it,
  create the focused Git commit, and resume the recoverable experiment attempt (or
  start a fresh one only when the prior result cannot be safely recovered).
  Do not stop after merely reporting the code error or ask the Human to reactivate
  the Goal. When the resumed or fresh attempt becomes a self-completing task expected
  to exceed 10 minutes, perform the three liveness checks, create its replacement
  automation, and only then return the Goal to `blocked` and end the response.
- After a monitored failure, ending the resumed turn without continuing the route is
  permitted only when exactly one unresolved `HUMAN_GATE_REQUIRED` or
  `ADVISOR_GATE_REQUIRED` has been established, or after a newly started live task
  has been handed off through the long-running procedure above.
- When the user manually changes the Goal to `active`, first inspect completion. If
  incomplete, report progress, verify that the existing automation still covers the
  task (recreate it if necessary), and change the Goal back to `blocked` only after
  the self-wakeup path is confirmed. If complete, keep it `active` and continue the
  subsequent PLAN step.
- If a user message is unrelated to the active task, answer that message directly
  without inspecting or changing the task state.
- Cooling, zero-state restoration, scheduled waiting, and automation handoff are
  therefore temporary execution states; they are not unresolved scientific gates,
  but long-running work must use the handoff procedure above.

## Execution Policy (without a runtime state machine)

The repository has no mandatory role execution state machine. Human, Advisor,
Supervisor, Orchestrator, Planner and Executer are collaboration roles, not
machine-state owners or sequential approval gates.

### Human

- Owns the lab, scientific objective, and high-risk device authorization.
- May explicitly override non-scientific execution instructions in GUIDE without
  editing GUIDE/RESEARCH.
- Human-authorization decisions are governed by this file's high-risk boundary;
  an extra authorization request written only in GUIDE/PLAN does not create a
  second gate for bounded light or camera work.

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

### Versioned plans, evidence, and reproducibility

- `.agent-work/PLAN.md`, `.agent-work/PLAN-FULL.md`, execution results, debug notes,
  reviews, and terminal evidence are versioned project records. They may be
  tracked by Git and should be retained when they explain a GUIDE decision,
  engineering blocker, experiment attempt, or recovery boundary.
- PLAN and PLAN-FULL remain collaboration context rather than a production
  runtime state machine, test input, or hidden authorization gate. Tracking them
  preserves reviewability; it does not make them executable authority.
- Track project material by default: source, tests, documentation, plans,
  configuration, small validation logs, reports, manifests, hashes, analysis,
  and cleanup evidence. PLAN/PLAN-FULL are therefore eligible for Git tracking.
- Do not track experimental payloads, firmware artifacts, compile/build output,
  generated archives, or other large generated files. Firmware source/configuration
  remains trackable when it is the small reproducible input rather than the
  generated firmware itself.
- Experimental payloads include TIFF/JPEG/PNG derivatives, decoded camera arrays,
  rawpy per-capture JSON, white-LUT calibration datasets, and equivalent bulk
  measurement records. Markdown experiment reports and small manifests, hashes,
  quality summaries, analysis, and cleanup evidence remain trackable.
- Keep credentials, local environments, caches, OS metadata, and raw experimental
  media (CR3/RAW/NEF/ARW/DNG and equivalent large capture payloads) outside Git.
  Store raw experiment data under `/Volumes/4T/temp/rgbww-optimizer` and retain
  the small run manifest, hashes, quality report, analysis, and cleanup evidence
  needed to reproduce and audit it.

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

- Human authorization is required only for high-risk operations: device firmware
  upload/flash, remote service update or deployment, destructive hardware change,
  credential/secret rotation, or an equivalent irreversible external mutation.
  A new bounded experiment selected by the active GUIDE/PLAN is not high-risk by
  itself.
- Creating, validating, replaying, or consuming an offline setup/lineage release is a computation and provenance operation. It does not require Human authorization, and `production_release_usable=true` is not itself a hardware or formal-execution authorization.
- Read-only remote health/config/capability checks, device identity/state readback, and zero-state verification do not require separate Human authorization when they are explicitly bounded by the current execution notes and do not change device state beyond the declared zero/off cleanup.
- Turning Ray120c or the RGBWW fixture on or off, and operating the camera for a
  bounded experiment, does not require Human authorization. This applies to a
  bounded light/camera operation already selected by the active GUIDE/PLAN,
  including zero-state setup and Python/shell cleanup.
- The current execution notes and owning runner must still define or enforce the
  target, intensity, duration, source isolation, abort behavior, and cleanup.
  Removing the separate approval step does not permit widening those bounds.
- No role may infer permission to widen intensity, range, duration, target, recovery
  path, or later-stage scope from a release, prior operation, or light-control
  exception. A new bounded experiment still needs to be explicitly selected by
  the active GUIDE/PLAN, but does not need a separate Human authorization unless
  it contains a high-risk operation.
- Computation and other work that does not access or control devices does not require Human approval.
- For a high-risk operation, the Orchestrator records the Human authorization and
  its exact scope in the current execution notes; the same authorization must
  not be requested again for that exact operation.
- If a high-risk operation lacks clear, current authorization or exceeds its
  approved target, range, intensity, duration, or recovery path, the Orchestrator
  stops and asks the Human. This stop does not apply to bounded light/camera work,
  read-only checks, cleanup, or offline computation.
- Authorization for one high-risk operation never authorizes another firmware
  upload, remote update, destructive change, or secret rotation. Bounded light
  and camera work remain governed by the active written scientific scope and
  cleanup contract, without an additional Human gate.

## Development Model

- Treat Python as the planned implementation language for optimizer and calibration tooling.
- Keep Python implementation modules under `src/camera_based_rgbww_optimizer/`: `control/` for device control, `optimization/` for measurement and calibration workflows, `utils/` for shared helpers/post-processing, and `interaction/` for local UI tools.
- Do not add root-level CLI compatibility wrappers. Use `python -m camera_based_rgbww_optimizer...` module commands and document them in `docs/README.md`.
- The project uses a minimal `pyproject.toml`; install locally with `.venv/bin/python -m pip install -e .`.
- Prefer local execution. Use Docker only when a concrete dependency requires it; if Docker is needed, use Colima and prefer `docker-compose`.
- Put raw experiment data, disposable caches, local environments, credentials,
  firmware artifacts, and compile/build output under `/Volumes/4T/temp/rgbww-optimizer`.
  Repository `tmp/` may contain versioned non-raw evidence, reports, and execution
  logs; do not put raw CR3/RAW capture payloads or generated build artifacts there.
- Repository `tmp/*.zsh` files remain version-controlled execution wrappers; non-raw logs and reports may be versioned beside them.

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
