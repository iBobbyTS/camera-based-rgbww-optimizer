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

This project has four explicit roles:

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

### Planner

- Is a Codex role.
- Converts the Advisor's `GUIDE.md` into the active `PLAN.md` for the Executer.
- Defines executable steps, frozen inputs, safety boundaries, evidence requirements, branches, acceptance criteria, and stopping points.
- Reviews and accepts or rejects the Executer's results against `PLAN.md`.
- At the end of the stage, produces the stage AUDIT PACK for the Advisor.

### Executer

- Is a Codex role.
- Executes the active `PLAN.md` within its exact authorization, scope, budgets, branches, and stopping points.
- Produces the required code, tests, experiment artifacts, cleanup evidence, and handoff records for Planner review.
- Does not independently change the experimental direction or enter a locked stage.
- Must treat `.agent-work/PLAN.md` as Planner-owned and read-only. The Executer is prohibited from editing, appending to, changing status in, renaming, archiving, or otherwise modifying `PLAN.md`.
- Must write execution progress, validation results, artifacts, failures, discovered plan contradictions, and Planner decision requests to `.agent-work/EXECUTION_RESULT.md` instead.
- If execution discovers a branch or contradiction requiring Planner judgment, stop the affected work, record the exact evidence and decision request in `EXECUTION_RESULT.md`, and leave `PLAN.md` unchanged for the Planner to update.

The normal stage flow is:

1. The Human prepares the environment and states the experiment goal.
2. The Advisor researches and writes `GUIDE.md` plus `RESEARCH.md`.
3. The Planner writes `PLAN.md`, including execution and acceptance contracts.
4. The Executer performs the authorized plan and returns evidence.
5. The Executer records that evidence in `.agent-work/EXECUTION_RESULT.md` without modifying `PLAN.md`.
6. The Planner reads `EXECUTION_RESULT.md`, accepts, rejects, or branches the result, updates `PLAN.md`, and, when the stage is complete, creates the AUDIT PACK for the Advisor.

### High-Risk Device Authorization

- Both the Planner and the Executer must ensure that the Human has approved a high-risk device operation before it is performed.
- Computation and other work that does not access or control devices does not require Human approval.
- If the Planner obtains Human approval, the Planner must record it explicitly in `PLAN.md`, including the authorized operation and its scope or bounds. `PLAN.md` must also state that the Executer may consume this authorization without asking again.
- When `PLAN.md` contains a valid, explicit Human authorization covering the exact operation, the Executer must not ask the Human to approve the same operation again.
- If authorization is absent, ambiguous, expired, or does not cover the requested target, range, intensity, duration, or recovery path, the Planner or Executer must stop and ask the Human before proceeding.
- Authorization for one named experiment or device operation does not authorize another experiment, firmware upload, broader range, higher output, or later stage unless `PLAN.md` explicitly says so.

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
