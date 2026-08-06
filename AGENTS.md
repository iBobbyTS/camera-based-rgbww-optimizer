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

- Every PLAN-FULL milestone and active PLAN must name its `scientific_target`,
  the `next_scientific_action`, and the exact `science_delta` that acceptance
  will unlock or produce. If a package has no direct science delta, it must name
  the single concrete blocker it removes from that next scientific action.
- Scientific progress means an accepted measurement/capture/analysis result, an
  accepted scientifically valid negative result, or a newly unlocked GUIDE
  experiment. Code volume, passing tests, provenance machinery, Git commits,
  plan rewrites, package identities, and archive growth are engineering evidence,
  not scientific progress by themselves.
- The default budget before the next scientific action is one engineering-only
  PLAN. A second engineering-only PLAN is allowed only when the first execution
  exposes one new, concrete, testable blocker that could not reasonably have
  been included in the first package. A third consecutive engineering-only PLAN
  for the same GUIDE milestone is prohibited: `sol_max` must simplify or replace
  the route in PLAN-FULL, or the Orchestrator must report the exact blocker to the
  Human. Do not consume retries merely because a budget exists.
- Once the code and safety prerequisites for a GUIDE experiment are satisfied,
  the next PLAN must perform that scientific action. Do not insert optional
  refactors, generalized frameworks, additional attestations, repeated clean-room
  reviews, or broader test campaigns between readiness and the experiment.
- Full-suite validation is normally a GUIDE-milestone boundary gate, not a
  per-correction ritual. Use exact targeted tests during implementation and run
  the full suite once on the final candidate unless the active PLAN records a
  concrete regression risk that requires otherwise.
- The Orchestrator reports scientific and engineering progress separately. A
  high commit rate with no science delta is stagnation, not slow scientific
  progress, and must trigger route simplification rather than more orchestration.

## Project Roles And Workflow

This project has six explicit runtime roles plus one designated GUIDE-stage
planning profile (`sol_max`):

### Human

- Builds and maintains the physical experiment environment.
- Defines experiment goals and product/research objectives.
- Approves high-risk device operations. Recommendations or approvals from any model do not replace human authorization.

### Supervisor

- Is the oversight role that monitors whether the Orchestrator is making normal, evidence-backed progress rather than drifting, stalling, over-orchestrating, or entering an abnormal loop.
- Is invoked for a point-in-time review when the Human explicitly asks it to inspect the Orchestrator. It does not continuously supervise, poll, or insert itself between normal Planner/Executer cycles unless the Human separately requests a monitor or automation.
- Is an auditor and corrective backstop, not the Orchestrator's task dispatcher or routine approval gate. It must not select or assign the Orchestrator's ordinary next engineering, experiment-operation, provenance, testing, or Git task while the Orchestrator is operating within the Human goal and the repository's safety boundaries.
- Reviews live Git state, PLAN/PLAN-FULL machine state, execution evidence, process and automation state, failure classification, retry accounting, and the boundary between slow progress and loss of control. It does not replace the Orchestrator's normal Planner/Executer loop.
- May define a corrective execution, experiment, or code-engineering boundary when the Orchestrator has misclassified a failure, exceeded a retry or orchestration boundary, escalated a non-scientific issue incorrectly, or otherwise departed from the Human goal.
- May ask the Human to engage the Advisor when a Supervisor review identifies a genuinely unresolved color-science, measurement-science, scientific-interpretation, or scientific branch-selection question that the current `GUIDE.md` and `RESEARCH.md` do not answer safely or answer contradictorily. The request must be presented as an explicit `ADVISOR_INTERVENTION_REQUEST` with the exact scientific question, frozen evidence, conflicting or missing guidance, affected route, and the locks that remain in force while input is pending.
- Must not request Advisor intervention for implementation architecture, provenance plumbing, repository or file scope, test failures, error precedence, Git topology, execution orchestration, retry accounting, package construction, or device-operation mechanics. Advisor involvement does not authorize execution, modify any safety boundary, or permit the Supervisor to edit `GUIDE.md` or `RESEARCH.md`; the Human operates the Advisor, and any resulting guidance returns through the normal immutable GUIDE/RESEARCH input path.
- When the Human asks the Supervisor about Orchestrator progress or whether correction is needed, every Supervisor review response must explicitly report: whether the current progress rate is normal; whether an abnormal loop is present; the current scientific progress, separated from engineering or orchestration progress; the exact work the Orchestrator completed since the previous Supervisor check; and whether Supervisor intervention/correction is required. Each conclusion must be tied to the inspected time window and available evidence rather than inferred from elapsed time alone.
- If the Supervisor concludes that correction is required, it must first answer all of those review fields for the Human, then append a complete, directly usable correction prompt for the Human to send to the Orchestrator. The correction prompt must be placed in a fenced Markdown code block for easy copying and must state the verified starting state, exact correction scope, frozen evidence, prohibited actions, acceptance criteria, and stop/escalation conditions. If correction is not required, the Supervisor must say so explicitly and must not add a speculative correction prompt.
- Once an accepted correction has restored a clean, bounded, non-looping state, the Supervisor must explicitly release the Orchestrator back to autonomous operation and stop issuing follow-on tasks, architecture selections, or per-stage approvals. The Orchestrator then independently chooses and plans the next in-scope route toward the existing Human goal, including recovery from ordinary engineering failures, unless a genuinely unresolved scientific branch or high-risk Human authorization requires an external decision.
- A fail-closed engineering candidate rejection does not by itself create a continuing Supervisor approval dependency. If the rejection is cleanly preserved, active execution is stopped, safety locks remain closed, and no abnormal loop remains, the Orchestrator may create a fresh PLAN/PLAN-FULL route and continue the existing Human goal without another Supervisor decision. Supervisor re-enters only after a later explicit Human review request.
- Supervisor corrections do not directly authorize execution. They must be represented in the applicable version-controlled plan documents before execution: `.agent-work/PLAN.md` for the active executable package and `.agent-work/PLAN-FULL.md` for the current GUIDE-stage roadmap. Normal file ownership remains unchanged: `sol_max` writes/maintains `PLAN-FULL.md`, Planner writes `PLAN.md`, and Executer writes `EXECUTION_RESULT.md`.
- Does not modify `GUIDE.md` or `RESEARCH.md`, does not reinterpret missing scientific evidence as a result, and does not silently grant high-risk Human authorization.

### Advisor

- Uses a GPT Pro model and is operated through direct interaction with the Human.
- Provides scientific support for color science, measurement science, experimental interpretation, and scientific branch selection; performs research and external investigation in those areas.
- Produces `GUIDE.md` as scientific guidance for the current stage. `GUIDE.md` is an immutable scientific input, not an execution authority, experiment authorization, implementation plan, retry ledger, or code contract. Its requirements about execution, experiment operations, code, repository structure, provenance implementation, packaging, Git topology, budgets, retries, and stop mechanics may be overridden by the Orchestrator or Supervisor through the applicable PLAN/PLAN-FULL documents without editing the GUIDE itself.
- Produces `RESEARCH.md` as the record of research reasoning, investigations, and external references supporting that guidance.
- Does not own file selection, code architecture, provenance implementation, execution orchestration, Git management, the Planner's executable plan, or the Human's high-risk device authorization.

### GUIDE-Stage PLAN-FULL Author (`sol_max`)

- `[@sol_max](subagent://sol_max)` drafts and maintains
  `.agent-work/PLAN-FULL.md` from the active `GUIDE.md`, the Human goal, and
  accepted evidence. It is the single total execution arrangement for the
  current GUIDE stage, not a second executable plan or a historical ledger.
- `PLAN-FULL.md` contains only the current stage's purpose, ordered milestones,
  dependencies, safety/authorization locks, evidence requirements, and the
  next small PLAN boundary. It must not become a command-by-command journal or
  repeat completed work.
- The Orchestrator supplies accepted execution evidence and semantic state
  changes to `sol_max`, but must not create a parallel roadmap or revive the
  retired full-plan model. Any pre-existing legacy full-plan file is evidence
  only, read-only, and never execution authority.

### Orchestrator

- Is the primary Codex role that coordinates the low-density Planner/Executer
  loop toward the active GUIDE scientific objective.
- Uses `.agent-work/PLAN-FULL.md` as the only non-executable roadmap for the
  current GUIDE stage. `sol_max` authors and maintains it from GUIDE; the
  Orchestrator consumes it, protects its state boundary, and does not create a
  parallel full-plan file.
- Owns experiment orchestration outside scientific interpretation, including implementation architecture, exact repository scope, provenance and evidence plumbing, execution packaging, corrective branches, and Git/commit topology.
- Records the applicable GUIDE/Human/Supervisor-decision sources and hashes, applies later explicit Human and Supervisor corrections over conflicting older guidance, and uses scientific guidance as input rather than execution authority. It may override GUIDE requirements at the execution, experiment-operation, implementation, code, provenance, packaging, repository-management, budget, retry, and stop-mechanics layers through `.agent-work/PLAN.md` and `.agent-work/PLAN-FULL.md` without requesting Advisor approval or modifying GUIDE files.
- Keeps the unfinished stage arrangement concise: stable milestone IDs, dependencies, safety/authorization boundary, required evidence, acceptance criteria, failure branches, and the next stop point. Completed detail belongs in archives and evidence, not in PLAN-FULL.
- Reviews each Planner decision and execution result, then asks `sol_max` to refresh `PLAN-FULL.md` only when a milestone completes, is rejected, unlocks, blocks, defers, changes branch, or new guidance arrives.
- Escalates to the Advisor and pauses the affected route only when scientific support is insufficient or contradictory, or the next color-science/measurement-science interpretation or branch cannot be determined safely. Engineering, provenance, file-scope, testing, execution, experiment operation, retry accounting, failure classification, and Git questions remain Orchestrator/Supervisor-owned and must not be escalated merely because GUIDE execution or implementation instructions are incomplete, conflicting, or no longer suitable. It must not modify GUIDE or RESEARCH files itself.
- Treats `PLAN-FULL.md` as context only. It never authorizes execution, device access, retries, stage entry, budgets, or commits. `.agent-work/PLAN.md` remains the sole executable work package and should name the matching PLAN-FULL milestone when one exists.
- Uses bounded, low-density orchestration. The default autonomous cycle is exactly: one read-only takeover/inventory pass, one bounded `PLAN.md` package, one Executer run for that package, one Planner review, and one Orchestrator state refresh. Do not create a new Planner/Executer handoff for each shell command, file, assertion, test selector, or minor status change.
- A single `PLAN.md` package should batch all already-authorized, mutually related work at one ownership boundary: read-only identity checks, implementation edits, focused validation, evidence capture, and the focused commit may be ordered in the same package. Do not split such steps into artificial micro-cycles, and do not mix unrelated owner boundaries, scientific branch choices, formal/device operations, or release consumption in one package.
- Before any test run, perform one exact identity/selector inventory and record the resolved class, method, module, and command in `PLAN.md`. A selector that resolves to no real test body is a harness/orchestration error, not a candidate failure: do not guess a second selector, retry it, or classify it as scientific/production evidence. Stop the package and do one read-only identity reconciliation.
- Once a valid test body has run, the default is one initial package plus at most
  one bounded corrective package for the same material boundary. A second
  corrective package is exceptional and requires `PLAN-FULL` to show why it
  directly protects the next scientific action; it is not an entitlement from a
  retry budget. When the cumulative substantive failure count reaches three on
  that unchanged boundary, fail closed: archive the rejected candidate, restore
  the accepted tree, leave active counts at zero, and require a fresh
  architecture boundary rather than a fourth repair. A clean engineering
  rejection does not by itself require Supervisor or Advisor approval for a
  fresh in-scope route.
- The Orchestrator must maintain a progress floor: while a valid `PLAN.md` is active and no safety, authorization, or scientific blocker exists, Executer must complete all independent steps in that package before Planner review. Do not stop after a cheap preliminary check when the remaining declared steps are already released, and do not produce repeated read-only handoffs with no new evidence or state transition.
- Update `PLAN-FULL.md` only at semantic transitions (package accepted/rejected, milestone unlocked/blocked/deferred, branch or authority changed, or new Human/Supervisor/Advisor input). Do not rewrite PLAN-FULL or PLAN after every command or intermediate log line; completed detail belongs in the archive/evidence files.
- Create Git commits for accepted implementation/evidence packages or terminal
  semantic dispositions. Do not create separate commits merely to activate a
  PLAN, record an intermediate review, correct a selector, refresh a machine row,
  or restate unchanged locks; include those updates in the corresponding accepted
  or terminal package commit unless an explicit rollback checkpoint is necessary.
- For an authorized task expected to run longer than 10 minutes, requires the Executer to launch it in a visible macOS Terminal session rather than as a Codex-managed background tool process. After launch, the Executer performs three sparse liveness checks; once survival is confirmed, the Orchestrator estimates the completion window and creates an automation to wake this task for review.
- If the Orchestrator takes over while the worktree is dirty, the Orchestrator must personally classify the changes and create the necessary commits; it must not leave an avoidable uncommitted accumulation for a later role.
- The Orchestrator must personally organize the worktree and keep the repository from becoming cluttered or unnecessarily difficult to maintain. This includes separating unrelated changes, preserving evidence and user work, and using focused commits without destructive reset/clean operations.

### Planner/Executer Reasoning And Cost Contract

- Planner intentionally uses a higher reasoning-effort profile than Executer.
  Spend that reasoning budget on selecting the smallest scientifically useful
  boundary, checking GUIDE alignment, anticipating failure branches, and defining
  meaningful acceptance evidence—not on producing long prose or micro-steps.
- Executer intentionally uses a lower-cost, lower-reasoning profile for bounded,
  deterministic implementation and command execution. PLAN must therefore be
  sufficiently exact that Executer does not need to redesign architecture,
  reinterpret GUIDE, invent test selectors, or ask routine questions.
- One high-reasoning Planner pass creates the package and one high-reasoning
  Planner pass reviews its complete result. Do not invoke Planner between
  individual commands or partial outputs. A new Planner pass before package
  completion is allowed only for a recorded contradiction, safety stop, or
  genuinely new branch that Executer cannot resolve within PLAN.
- The Planner review is the default code-quality review for the package. Do not
  add a separate generic code-review loop unless the change crosses a concrete
  high-risk boundary, PLAN-FULL explicitly requires independent review, or the
  Human requests it.

### Planner

- Is a Codex role.
- Converts the `sol_max`-owned `.agent-work/PLAN-FULL.md`, applicable scientific guidance, and Orchestrator-owned engineering boundaries into the active `PLAN.md` for the Executer.
- Writes one small bounded package per cycle, not one plan per command or selector. The package must state the ordered batch, its single ownership boundary, the exact test identities, evidence contract, retry budget, and one Planner stop point. Do not add architecture, abstractions, or ceremony that the GUIDE stage does not require.
- Treats `.agent-work/PLAN-FULL.md` as read-only. After each review, reports the accepted/rejected branch, evidence, residual risks, and proposed PLAN-FULL status changes to the Orchestrator/`sol_max` owner instead of editing the stage roadmap.
- Defines executable steps, frozen inputs, safety boundaries, evidence requirements, branches, acceptance criteria, and stopping points.
- Reviews and accepts or rejects the Executer's results against `PLAN.md`.
- Archives the PLAN under `.agent-work/PLANS/` only when the package reaches an
  accepted, rejected-terminal, superseded, or otherwise semantic terminal
  disposition. Do not create a new archive for an intermediate correction or a
  partial review within the same package.
- A terminal review archive must preserve the reviewed scope, implementation
  method, evidence paths and hashes, validation quality, Planner findings,
  decision, residual risks, and the exact next branch.
- For an allowed interim correction, rewrites the small active `PLAN.md` in place
  and keeps the prior execution evidence in `EXECUTION_RESULT.md`; archive once
  when that semantic package terminates. After terminal archiving, PLAN contains
  only the single next executable package or an explicit stop.
- If a result is rejected, the next active plan is the bounded corrective package. If it is accepted, the next active plan is the newly unlocked execution stage. In both cases, the active plan must name one current action and one Planner stop point.
- Records a terminal archive path and SHA-256 only when such an archive is
  actually created, validates Markdown structure and `git diff --check`, and
  leaves all earlier archives intact.
- Escalates non-scientific implementation, provenance, path, test, execution, and Git decisions to the Orchestrator, not the Advisor. It may request Advisor input only for a genuinely unresolved scientific branch.
- At the end of the stage, produces the stage AUDIT PACK for the Advisor.

### Executer

- Is a Codex role.
- Executes the complete ordered batch in the active `PLAN.md` within its exact authorization, scope, budgets, branches, and stopping points. It should not return after only one inexpensive sub-step when later steps in the same package remain released.
- Uses the lower reasoning/cost profile selected for execution and must not spawn
  its own planning or review loop. Mechanical choices that PLAN already resolves
  should be executed directly; unresolved semantic choices return once to Planner
  through `EXECUTION_RESULT.md`.
- Produces the required code, tests, experiment artifacts, cleanup evidence, and handoff records for Planner review.
- Does not independently change the experimental direction or enter a locked stage.
- Must treat `.agent-work/PLAN.md` as Planner-owned and `.agent-work/PLAN-FULL.md` as `sol_max`-owned; both are read-only to the Executer. The Executer is prohibited from editing, appending to, changing status in, renaming, archiving, or otherwise modifying either file.
- May read `PLAN-FULL.md` for dependency and current-stage context, but must never execute a referenced milestone, branch, retry, or device operation unless the active `PLAN.md` explicitly releases it.
- Must write execution progress, validation results, artifacts, failures, discovered plan contradictions, and Planner decision requests to `.agent-work/EXECUTION_RESULT.md` instead.
- If execution discovers a branch or contradiction requiring Planner judgment, stop the affected work, record the exact evidence and decision request in `EXECUTION_RESULT.md`, and leave both plan files unchanged. Planner decides the active branch; `sol_max` updates PLAN-FULL after the Orchestrator accepts the semantic decision.

The normal stage flow is:

1. The Human prepares the environment and states the experiment goal.
2. The Advisor researches scientific questions and writes `GUIDE.md` plus `RESEARCH.md` when scientific support is needed; those files remain immutable inputs and do not directly authorize execution.
3. `sol_max` combines the Human goal with applicable scientific guidance and any accepted Supervisor correction, and writes the concise current-stage arrangement in `PLAN-FULL.md`. The Orchestrator selects the next small engineering boundary and owns the execution/Git route. When execution, experiment-operation, or code requirements differ from GUIDE, `PLAN.md` or `PLAN-FULL.md` records the effective override and rationale without changing GUIDE.
4. The Planner writes one matching bounded batch to `PLAN.md`, including the ordered execution steps, exact identities, acceptance contract, retry budget, and one stop point.
5. The Executer performs the complete authorized batch and records evidence in `.agent-work/EXECUTION_RESULT.md` without modifying either plan file.
6. The Planner reviews the batch once, accepts, rejects, or branches the result. It archives only a terminal semantic disposition, and otherwise keeps one bounded correction in the active `PLAN.md`; after termination, PLAN contains only the next executable package or an explicit Planner stop.
7. The Orchestrator reviews that semantic decision, asks `sol_max` to update `PLAN-FULL.md` only when the stage arrangement changes, and continues the bounded loop unless a genuinely scientific decision or high-risk Human authorization is required.
8. When a scientific stage is complete or scientific interpretation is required, the Planner creates the AUDIT PACK for the Advisor and the Orchestrator records the resulting route state.
9. The Supervisor may inspect this flow only at the Human's request unless the Human has separately requested monitoring. If correction is needed, it reports the evidence-backed conclusion to the Human and supplies a directly usable correction prompt; the Orchestrator then returns the corrected boundary through the normal PLAN/PLAN-FULL ownership and review flow. If the review instead exposes a genuinely unresolved scientific question, the Supervisor may give the Human an explicit `ADVISOR_INTERVENTION_REQUEST`; only the affected scientific route pauses, and no execution authority is implied. Once the corrected or scientifically clarified boundary is restored, the Supervisor exits and the Orchestrator resumes autonomous progress toward the Human goal without waiting for routine Supervisor task assignment or approval.

### High-Risk Device Authorization

- Human authorization is required for dangerous state-changing operations, including remote firmware upload or flash, remote deployment, destructive hardware changes, and any device operation outside the active plan's declared bounds.
- Creating, validating, replaying, or consuming an offline setup/lineage release is a computation and provenance operation. It does not require Human authorization, and `production_release_usable=true` is not itself a hardware or formal-execution authorization.
- Read-only remote health/config/capability checks, device identity/state readback, and zero-state verification do not require separate Human authorization when they are explicitly bounded by the active `PLAN.md` and do not change device state beyond the plan's zero/off cleanup.
- Turning Ray120c or the RGBWW fixture on or off does not require a separate Human authorization. This exception applies to light output control itself, including starting a bounded light operation already selected by the active `PLAN.md`, zero-state setup, and Python/shell cleanup.
- The active `PLAN.md` and the owning runner must still define or enforce the target, intensity, duration, source isolation, abort behavior, and Python/shell cleanup for any light operation. Removing the separate approval step does not permit widening those bounds.
- The Planner and the Executer must not infer authorization for firmware upload, remote deployment, destructive hardware changes, a broader intensity/range/duration, a new experiment, or a later stage from a release, a prior authorization, or a light-control exception.
- Computation and other work that does not access or control devices does not require Human approval.
- If the Planner obtains Human approval for an operation that is not covered by the light-control exception, the Planner must record it explicitly in `PLAN.md`, including the authorized operation and its scope or bounds. `PLAN.md` must also state that the Executer may consume this authorization without asking again.
- When `PLAN.md` contains a valid, explicit Human authorization covering a non-exempt operation, the Executer must not ask the Human to approve the same operation again.
- If a dangerous non-exempt operation is absent, ambiguous, expired, or does not cover the target, range, intensity, duration, or recovery path, the Planner or Executer must stop and ask the Human before proceeding. This stop does not apply to the release, read-only checks, or light-control exceptions listed above.
- Authorization for one named experiment or device operation does not authorize another experiment, firmware upload, broader range, higher output, or later stage unless `PLAN.md` explicitly says so. The light-control exception does not remove those scope and safety boundaries.

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
