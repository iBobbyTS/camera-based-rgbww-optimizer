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

- Keep engineering ceremony proportional to the active GUIDE objective. No
  mandatory orchestration or acceptance-artifact workflow is required when it
  does not materially improve scientific correctness, safety or reproducibility.
- Scientific progress is an accepted measurement/capture/analysis result, a valid
  scientific negative, or a newly unlocked GUIDE experiment. Code, tests, plans,
  provenance and commits are engineering evidence only.
- Human owns the physical lab, experiment goal and dangerous-operation
  authorization. Advisor owns scientific guidance and immutable `GUIDE.md`/
  `RESEARCH.md`; it is consulted only for color science, measurement science,
  interpretation or scientific branch selection.
- Orchestrator owns the direct low-density implementation and experiment route,
  repository scope, evidence files and Git commits. It may use Planner and
  Executer as optional cost roles: Planner can spend more reasoning on the
  smallest useful boundary, while Executer can perform deterministic edits and
  checks at lower cost. Neither role is a required approval stage.
- Ordinary implementation or test problems are fixed in the current E1/E2
  worktree until meaningful behavior tests pass. Do not stop merely because a
  validation count, review count or correction budget would have been exhausted.
- `.agent-work/PLAN.md`, `.agent-work/PLAN-FULL.md`, debug notes, reviews and
  execution results are versioned records. They may be tracked by Git so the
  completed GUIDE stage can be reconstructed; they remain collaboration context,
  not production runtime state, test input, or hidden authorization.
- Track project material by default: source, tests, docs, plans, configuration,
  small logs, reports, manifests, hashes, analysis and cleanup evidence. PLAN and
  PLAN-FULL may be versioned for post-GUIDE reconstruction.
- Keep experimental payloads, generated firmware, compile/build output, archives
  and other large generated files out of Git. Small firmware source/configuration
  remains trackable as reproducible input. Raw experiment data belongs under
  `/Volumes/4T/temp/rgbww-optimizer`; retain the small manifests, hashes, quality,
  analysis and cleanup evidence needed for audit.
- Treat TIFF/JPEG/PNG derivatives, decoded camera arrays, rawpy per-capture JSON,
  white-LUT datasets and equivalent bulk measurement records as experiment data.
  Keep Markdown experiment reports and small audit metadata versioned.
- Supervisor is invoked only when Human asks for a point-in-time check. It reports
  progress speed, abnormal loops, scientific progress and whether intervention is
  needed; it does not dispatch routine work. It may ask Human to engage Advisor
  only for an unresolved scientific question.
- For commands expected to exceed 10 minutes, use the visible Terminal/liveness/
  automation workflow required by `AGENTS.md`.

## Core Safety and Runtime Rules

- Remote firmware upload/deployment, destructive hardware changes, and device
  work outside the current written execution scope require Human authorization.
- Bounded light output already selected by the current execution notes and zero/off cleanup do not
  require a separate approval. Keep exact target, intensity, duration, abort,
  isolation, and Python/shell cleanup bounds.
- Start new channel tests at low PWM, verify order and thermal behavior, then
  ramp only within the plan. Any script that can leave the fixture on must turn
  it off before exit unless it is an explicit light-on/control tool.
- Keep raw experimental outputs and disposable caches under
  `/Volumes/4T/temp/rgbww-optimizer`. Repository `tmp/` may hold versioned
  non-raw logs, reports and compile evidence; `tmp/*.zsh` files are versioned
  wrappers.
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
| Current executable work | The Orchestrator's current execution notes plus the applicable `GUIDE.md` |
| GUIDE-stage roadmap or dependency status | `.agent-work/PLAN-FULL.md` and relevant tracked evidence; context only, never production authority |
| P7 TD-B provenance or historical regression | `docs/engineering/p7-td-b-contract-history.md`, then only relevant archives/evidence |
| Exact production behavior | The relevant module and focused tests |

Do not preload P7 history for ordinary work. The history note is a reference,
not authorization; the current route follows the Orchestrator's written execution
scope and the immutable scientific guidance.
