---
name: camera-based-rgbww-optimizer
description: Use for camera-based RGBWW calibration, local RGBWW/Ray120c control, Canon capture, RAW measurement, and color-chart workflows.
---

# Camera-Based RGBWW Optimizer

## Scope

Use this skill for the Human-owned local photography and lighting calibration
lab: the local workstation, ESPHome RGBWW fixture, local camera bridge and
Canon camera, and Ray120c reference light. Python implementation belongs under
`src/camera_based_rgbww_optimizer/`; use package module commands rather than
adding root-level compatibility wrappers.

## When to Use

- RGBWW channel control, response measurement, optimization, or cleanup.
- Canon capture, remote camera bridge, RAW Bayer measurement, or chart location.
- Ray120c CCT/G-M, HSI, RGB, reference matching, or thermal diagnostics.
- Planning, executing, or reviewing experiment packages for this repository.

## Role and Ownership Core

- Human owns the physical lab, experiment goal, and dangerous-operation
  authorization.
- Advisor researches direction and owns `GUIDE.md`/`RESEARCH.md`; those files
  are guidance, not execution authorization.
- Orchestrator alone owns `.agent-work/FULL_PLAN_REFERENCE.md`, the complete
  non-executable roadmap of unfinished GUIDE work.
- Planner reads that roadmap and GUIDE, writes exactly one active executable
  package to `.agent-work/PLAN.md`, reviews evidence, and archives reviewed work.
- Executer treats GUIDE, PLAN, FULL reference, debug records, and archives as
  read-only; executes only active PLAN bounds and appends results to
  `.agent-work/EXECUTION_RESULT.md`.

Only the active PLAN authorizes a task, device operation, retry, budget, or
stage entry. If guidance cannot determine a safe scientific branch, pause for
Advisor direction. For an authorized command expected to exceed 10 minutes,
use the visible Terminal/liveness/automation workflow required by `AGENTS.md`.

## Core Safety and Runtime Rules

- Remote firmware upload/deployment, destructive hardware changes, and device
  work outside active PLAN bounds require Human authorization.
- Bounded light output already selected by PLAN and zero/off cleanup do not
  require a separate approval. Keep exact target, intensity, duration, abort,
  isolation, and Python/shell cleanup bounds.
- Start new channel tests at low PWM, verify order and thermal behavior, then
  ramp only within the plan. Any script that can leave the fixture on must turn
  it off before exit unless it is an explicit light-on/control tool.
- Keep disposable outputs under `/Volumes/4T/temp/rgbww-optimizer`.
  Repository `tmp/*.zsh` files are versioned wrappers, not data directories.
- Ray120c is the CCT/G-M reference. Never infer its CCT from camera RGB.
- Formal camera work uses `control.camera_remote.RemoteCameraBackend`; do not
  expose credentials in arguments, logs, artifacts, or source.
- Ray OpenAPI uses a Human-classified public shared protocol default; this is a
  Human/repository-history decision and not an external-vendor verification claim.
  `AMARAN_OPENAPI_SECRET` is an optional explicit override and remains a
  private runtime value: never pass, print, log, or serialize it. Empty or invalid
  overrides fail closed, and the CLI has no secret argument.

## Routine Entry Points

- Cleanup: `python -m camera_based_rgbww_optimizer.control.all_off`
- ESPHome fixture: `python -m camera_based_rgbww_optimizer.control.esphome`
- Ray reference: `python -m camera_based_rgbww_optimizer.control.ray120c`
- Canon remote bridge: `python -m camera_based_rgbww_optimizer.control.camera_remote`
- Local capture compatibility: `control.camera_gphoto2`
- RAW patches: `measurement.raw_mosaic_patches`
- Chart tools: `interaction.location_picker_ui` and
  `interaction.location_checker`

Before changing device control, camera measurement, color conversion,
optimizer solving, persistence, or shared state, inspect the routed source of
truth and existing implementation. Add meaningful regression tests and preserve
the existing cleanup and provenance owners.

## Progressive Routing

| Task | Read only what is needed |
| --- | --- |
| Hardware assumptions, commands, calibration decisions, validation workflow | `docs/README.md` |
| Local connection/configuration/credential boundary | `docs/local-lab-connection-boundary.md` |
| Current executable work | `.agent-work/PLAN.md` plus the applicable `GUIDE.md` |
| Orchestrator roadmap or dependency status | `.agent-work/FULL_PLAN_REFERENCE.md` (read-only except Orchestrator) |
| P7 TD-B provenance or historical regression | `docs/engineering/p7-td-b-contract-history.md`, then only relevant archives/evidence |
| Exact production behavior | The relevant module and focused tests |

Do not preload P7 history for ordinary work. The history note is a reference,
not authorization; its current route is paused until a future active PLAN
explicitly releases work.
