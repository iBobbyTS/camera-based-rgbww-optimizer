# P7 thermal/reference operating envelope

## Status

Second-pass offline contract repair implemented and fully validated; waiting for Planner review. Real TD-A remains locked and no device authorization may be requested.

## Planner rejection 2026-07-20

Confirmed root causes:

- plan/runner/analyzer have no canonical ambient+formal capture ledger;
- TD-C core needs 16 physical CR3 when all eight ambient frames are retained; Planner froze cap 16 and total allocation 128;
- unresolved TD-B/TD-C dependency times are replaced by an invalid 300-second fallback;
- remote camera response exposes no actual exposure-start timestamp, so host request-start cannot satisfy the timing contract and execute must fail closed;
- source isolation lacks an independently replayable both-source off/readback gate at run start, ambient boundaries, and transitions;
- TD-C analyzer reports waiting/pass without evaluating its required gates.

Current hypothesis: one canonical ordered capture ledger plus one replayable isolation-gate ledger fixes the ownership split. Actual exposure-start remains an adapter capability gate; this repository must not manufacture the timestamp.

## Repair result

- Canonical ordered capture ledger now contains ambient and formal owners; public analysis rejects missing, duplicate, reordered, or role-tampered evidence.
- TD-A owns three ambient frames; TD-C owns eight ambient plus eight formal frames with core physical cap 16 and total allocation 128.
- TD-B/TD-C unresolved dependency points remain null/deferred and are rejected before backend/device construction.
- The production path accepts only camera-adapter actual exposure-start provenance; the current remote adapter therefore fails closed before execution.
- Replayable both-source isolation evidence is required at run start, before ambient frames, and after transitions. TD-B now freezes all seven transition gates.
- TD-C implements structured compatibility, order-effect, stable-center, P6-interpretability, and ambient-trend gates.
- Runner-to-public-analyzer round-trip and deterministic tamper cases pass; focused 68/68 and full 461/461 are green.

## Retained finding

P7-R1 is valid failure evidence: acquisition and evidence integrity passed, but Ray and strip chronology show unresolved within-run nonstationarity. The legacy `reference_epoch_shift=false` cannot identify whether the stable reference moved because the current reference center was not stationary.

## Implemented boundary

- Operating-envelope v1 keeps all settle values null before TD-A.
- Timed points use monotonic readback-complete to exposure-start elapsed time.
- 60/120 tolerate 2 seconds; 300/600 tolerate 5 seconds.
- 600 seconds is validation-only, never an automatic settle result.
- Cold and conditioned-steady covariance remain separate.
- Thermal/history/load fields are diagnostic-only and cannot widen uncertainty.
- TD-B, TD-C, sentinel, remaining, boundary, holdout, Gate-6, and P8 stay locked.

## Offline artifacts

- Superseded first-pass plans remain under `/Volumes/4T/temp/rgbww-optimizer/p7-thermal-diagnostics-offline/`.
- Corrected six-plan checkpoint is under `/Volumes/4T/temp/rgbww-optimizer/p7-thermal-diagnostics-offline-r0b/`.
- Corrected derived R1 epoch artifacts are under `/Volumes/4T/temp/rgbww-optimizer/p7-thermal-diagnostics-offline-r0b/r1-derived/`.
- No device, network, `.env`, capture, or `all_off` call was made while generating them.

## Next decision

Planner reviews the offline checkpoint. If accepted, Planner asks the Human for the exact bounded `p7_td_a_cold_settling_v1` authorization; code completion alone does not authorize a run.
