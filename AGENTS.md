# Camera-Based RGBWW Optimizer Codex Instructions

## Language

- Reply in Chinese by default unless the user explicitly asks for another language.
- Write implementation plans in Chinese by default.

## Project Scope

- This is a local-first camera-based RGBWW optimizer project.
- The default target ESPHome RGBWW device name is `bedroom-rgbww-strip`.
- The attached fixture is a PWM RGBWW strip. The first milestone is proving independent control over all five physical channels.
- The later calibration workflow uses a camera, black/white/18% gray cards, a 24-color chart, and an Aputure Amaran Ray120c reference light at 100% brightness.

## Project Roles And Workflow

This project has five explicit roles:

### Human

- Builds and maintains the physical experiment environment.
- Defines experiment goals and product/research objectives.
- Approves high-risk device operations. Recommendations or approvals from any model do not replace human authorization.

### Advisor

- Uses a GPT Pro model and is operated through direct interaction with the Human.
- Guides the experimental direction, performs research and external investigation, and advises the Planner.
- Produces `GUIDE.md` as the authoritative experimental guidance for the current stage.
- Produces `RESEARCH.md` as the record of research reasoning, investigations, and external references supporting that guidance.
- Does not directly replace the Planner's executable plan or the Human's high-risk device authorization.

### Orchestrator

- Is the primary Codex role that coordinates the Planner and Executer loop.
- Exclusively owns `.agent-work/FULL_PLAN_REFERENCE.md` as the non-executable roadmap for every task required by the currently applicable Advisor guidance that is not yet complete. Planner and Executer must treat it as read-only.
- Records the applicable GUIDE/Human-decision sources and hashes, applies later explicit Human/Advisor decisions over conflicting older guidance, and preserves non-conflicting requirements from earlier guides.
- Gives every unfinished reference task a stable ID, status, dependencies, unlock owner, implementation outline, safety/authorization boundary, required evidence, acceptance criteria, failure branches, and stop point.
- Reviews each Planner decision and execution result, then refreshes `FULL_PLAN_REFERENCE.md` when a task completes, is rejected, unlocks, blocks, defers, changes branch, or new guidance arrives.
- Escalates to the Advisor and pauses the affected route when the applicable GUIDE is insufficient, contradictory, or cannot safely determine the next scientific branch. It must not modify GUIDE files itself.
- Treats `FULL_PLAN_REFERENCE.md` as context only. It never authorizes execution, device access, retries, stage entry, budgets, or commits. `.agent-work/PLAN.md` remains the sole executable work package and should name the matching reference task ID when one exists.
- Delegates each planning/review pass to a Planner subagent and each authorized execution pass to an Executer subagent; the Orchestrator independently reviews both handoffs before advancing the loop.
- For an authorized task expected to run longer than 10 minutes, requires the Executer to launch it in a visible macOS Terminal session rather than as a Codex-managed background tool process. After launch, the Executer performs three sparse liveness checks; once survival is confirmed, the Orchestrator estimates the completion window and creates an automation to wake this task for review.

### Planner

- Is a Codex role.
- Converts the Orchestrator-owned unfinished-work reference and the applicable Advisor `GUIDE.md` into the active `PLAN.md` for the Executer.
- Treats `.agent-work/FULL_PLAN_REFERENCE.md` as Orchestrator-owned and read-only. After each review, reports the accepted/rejected branch, evidence, residual risks, and proposed reference-status changes to the Orchestrator instead of editing the reference.
- Defines executable steps, frozen inputs, safety boundaries, evidence requirements, branches, acceptance criteria, and stopping points.
- Reviews and accepts or rejects the Executer's results against `PLAN.md`.
- On every review result, whether the Executer is rejected for another corrective pass or accepted to advance, first archives every completed, superseded, or already-reviewed part of the active plan under `.agent-work/PLANS/` without overwriting earlier archives.
- Each review archive must preserve the reviewed scope, implementation method, evidence paths and hashes, validation quality, Planner findings, decision, residual risks, and the exact next branch.
- After archiving, rewrites `.agent-work/PLAN.md` so it contains only the single next executable work package. Completed history and detailed future-stage designs must not remain in the active plan; future work may appear only as concise hard locks or prerequisites.
- If a result is rejected, the next active plan is the bounded corrective package. If it is accepted, the next active plan is the newly unlocked execution stage. In both cases, the active plan must name one current action and one Planner stop point.
- Records every new archive path and SHA-256 in the active plan, validates Markdown structure and `git diff --check`, and leaves all earlier archives intact.
- At the end of the stage, produces the stage AUDIT PACK for the Advisor.

### Executer

- Is a Codex role.
- Executes the active `PLAN.md` within its exact authorization, scope, budgets, branches, and stopping points.
- Produces the required code, tests, experiment artifacts, cleanup evidence, and handoff records for Planner review.
- Does not independently change the experimental direction or enter a locked stage.
- Must treat `.agent-work/PLAN.md` as Planner-owned and `.agent-work/FULL_PLAN_REFERENCE.md` as Orchestrator-owned; both are read-only to the Executer. The Executer is prohibited from editing, appending to, changing status in, renaming, archiving, or otherwise modifying either file.
- May read `FULL_PLAN_REFERENCE.md` for dependency and future-stage context, but must never execute a referenced task, branch, retry, or device operation unless the active `PLAN.md` explicitly releases it.
- Must write execution progress, validation results, artifacts, failures, discovered plan contradictions, and Planner decision requests to `.agent-work/EXECUTION_RESULT.md` instead.
- If execution discovers a branch or contradiction requiring Planner judgment, stop the affected work, record the exact evidence and decision request in `EXECUTION_RESULT.md`, and leave both plan files unchanged. Planner decides the active branch; Orchestrator alone updates the complete reference.

The normal stage flow is:

1. The Human prepares the environment and states the experiment goal.
2. The Advisor researches and writes `GUIDE.md` plus `RESEARCH.md`.
3. The Orchestrator records all currently unfinished GUIDE work in `FULL_PLAN_REFERENCE.md` and selects the current reference task for planning.
4. The Planner writes one matching current work package to `PLAN.md`, including execution and acceptance contracts.
5. The Executer performs the authorized plan and records evidence in `.agent-work/EXECUTION_RESULT.md` without modifying either plan file.
6. The Planner reads `EXECUTION_RESULT.md`, accepts, rejects, or branches the result, archives the reviewed/completed plan material, and rewrites `PLAN.md` to contain only the next executable work package or an explicit Planner stop.
7. The Orchestrator reviews the Planner decision, updates `FULL_PLAN_REFERENCE.md` when required, and either continues the Planner/Executer loop or pauses for Advisor guidance.
8. When the stage is complete, the Planner creates the AUDIT PACK for the Advisor and the Orchestrator records the resulting route state.

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
