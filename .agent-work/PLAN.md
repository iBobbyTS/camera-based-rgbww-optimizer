# P7-TD-B-RAY-OP600-EXPOSURE-GUARDED-FORMAL-R6

## Active package and authorization state

- **reference:** `P7-TD-B-RAY-OP600-EXPOSURE-GUARDED-FORMAL-R6`
- **plan_status:** `PLANNER_STOP_WAITING_EXPLICIT_HUMAN_FORMAL_DEVICE_RELEASE`
- **executable:** `false`
- **active_task_count:** `0`
- **engineering_only_plan_budget:** `1` consumed and terminally accepted by
  package commit `21754a3`; no additional engineering-only package is inserted.
- This is the next scientific package after accepted runtime-consumer clearance.
  It remains locked until Human explicitly authorizes the named formal/device
  operation and Orchestrator records the release in this active PLAN. No release
  eligibility, prior evidence or archive implies authorization.

## Scientific contract

- **scientific_target:** obtain a new Ray-only operational-600 R6 sequence and
  evaluate its quality, chronology, and A-return history compatibility.
- **next_scientific_action:** once explicitly released, run exactly one formal R6
  acquisition in the exact new root below, slots `000..015` in the frozen release
  sequence; run Ray-only analysis only after all 16 captures pass quality.
- **science_delta:** 16 new Ray captures plus Ray-only chronology/history analysis,
  or the first scientifically valid hard-failure result. Engineering, Git,
  release, or PLAN records are not science results.

## Frozen inputs and exact launch bounds

Read-only identity bindings (must match before any release):

| artifact | SHA-256 |
| --- | --- |
| `config/hsi/p7-ray-td-b-exposure-policy-v2.json` | `c9080d18571f617cb7d323ade843ff9c86bf92e3795d23e3999e26d413968681` |
| `release/frozen-inputs.json` | `8a81a906d2a94903a365f54b33c224a8ec99ce8d519ae2317cdc213c6e0264f8` |
| `release/r6-formal-plan.json` | `dea5f979950909d5b3e8fd93c3a76e4fd18c0242158eade7967c4c62ec72cc3b` |
| `release/release-descriptor.json` | `6843ef5007b9ebe3bfef1f7c8c1864ed0b86b3000d3d72caa8f08f67ce3bb452` |
| `release/terminal-seal.json` | `d9d7b784a4ec910d7c7740bc560ed87f2b99ab1744c19df42097d5683b668850` |
| `release/validation-summary.json` | `07e831616c303e68f9bf863a722b8b640c3726556f47143db8299083f941cc07` |
| frozen zero-readiness terminal seal | `c6fc7b2a14cfce2474e1a1369721ebbdf660aa60baccb4caf237873a1af2a39d` |

Exact operation bounds after release:

- **root:** `/Volumes/4T/temp/rgbww-optimizer/p7-td-b-formal-r6-ray-only-20260806T0012Z`
  (must be absent and freshly created; collision is an immediate stop).
- **source:** Ray only; ESPHome strip is zero throughout and ambient is zero.
- **camera:** existing `control.camera_remote.RemoteCameraBackend`; no credentials
  in args, logs, or artifacts; no auto-exposure or weak reacquire.
- **sequence:** consume `release/r6-formal-plan.json` exact capture IDs/order
  `000..015`, frozen A/D/B commands and C=`1/2500`; no guessed state, shutter, or
  timing substitution.
- **caps:** physical/formal captures `16`, launch `1`, retry `0`; no second root,
  resume, replacement frame, or old/new pooling.
- **dispatch:** one visible macOS Terminal launch only; no Codex background runner.
- **cleanup:** Python and shell cleanup, independent final-zero/readback, and
  terminal seal are mandatory on success or failure.

## Ordered execution, once authorized

1. Verify Human authorization covers this exact root, Ray-only source, camera,
   16-frame cap, frozen shutter, launch/retry caps, abort and cleanup. Verify every
   frozen artifact hash above and that the root is absent. Any mismatch stops before
   device or camera connection.
2. Launch the existing formal R6 runner once in visible Terminal. Capture the exact
   frozen `000..015` sequence, preserving each CR3, sidecar, SHA-256, MakerNote actual
   exposure, command/readback, physical ledger, quality result, and chronology.
3. If any capture is invalid or missing, stop immediately, force both sources zero,
   seal the hard failure, and do not retry or analyze. This is a scientific negative
   result only if the capture-quality/chronology evidence is complete and sealed.
4. Only for 16/16 quality pass, run the existing Ray-only analyzer named by the
   frozen release/runner contract; do not invent a selector or analyzer path. Record
   A-return compatibility and `steady_status=not_demonstrated`.

## Acceptance and stop

Acceptance requires a fresh root, 16/16 ordered captures or a sealed hard failure,
per-frame identity/quality/readback evidence, chronology and A-return anchors, exact
exposure/source/physical ledger, double cleanup/final-zero/terminal seal, and a
Ray-only analysis artifact when quality passes. No strip entry is unlocked by this
PLAN; it requires the GUIDE conditional `accepted_for_strip_entry` result.

Until the Human authorization is explicit and recorded here, the following remain
`false`: `formal_execution_authorized`, `device_authorized`, `release_consumption_authorized`,
`camera_authorized`, `ray_authorized`, `strip_authorized`, `capture_authorized`,
`analysis_authorized`, `network_authorized`, `td_c_authorized`. Planner stop is
`WAIT_FOR_EXPLICIT_HUMAN_FORMAL_DEVICE_RELEASE`; do not execute tests, formal,
release consumption, or device operations while stopped.

`PLAN_MACHINE_CONTRACT={"schema":"planner_execution_contract_v2","contract_id":"P7-TD-B-RAY-OP600-EXPOSURE-GUARDED-FORMAL-R6-V1","plan_status":"PLANNER_STOP_WAITING_EXPLICIT_HUMAN_FORMAL_DEVICE_RELEASE","executable":false,"active_task_count":0,"active_task":null,"engineering_only_plan_budget_consumed":1,"formal_execution_authorized":false,"device_authorized":false,"release_consumption_authorized":false,"camera_authorized":false,"ray_authorized":false,"strip_authorized":false,"capture_authorized":false,"analysis_authorized":false,"network_authorized":false,"td_c_authorized":false,"formal_root":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-formal-r6-ray-only-20260806T0012Z","formal_capture_cap":16,"launch_cap":1,"retry":0,"scientific_result_created":false,"planner_stop":"WAIT_FOR_EXPLICIT_HUMAN_FORMAL_DEVICE_RELEASE"}`
