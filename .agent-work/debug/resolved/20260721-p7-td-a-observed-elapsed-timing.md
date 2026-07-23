# P7 TD-A Observed-Elapsed Timing Contract

## Status

`resolved_offline_correction_accepted_waiting_for_new_human_authorization`

## Symptom

The first authorized Ray TD-A formal capture at nominal `t60` was retained at a best-effort gphoto2
exposure-start elapsed of `64.40580299403518 s`. The v1 runner rejected it because the offset
`+4.40580299403518 s` exceeded a frozen `+/-2 s` nominal-proximity tolerance.

## Evidence

```text
run = /Volumes/4T/temp/rgbww-optimizer/p7-thermal-diagnostics/
      p7-td-a-ray-20260721-150200
plan sha256 = ebbe657c4b9b11b2dee0f93dd9d38d8fbeffc9d577e3dfc30675677153943c88
failure sha256 = a002378287807d353849048eabd40eace1a38ef25aba107d9838751358b81a91
failed t60 CR3 sha256 = 2c44295d5d949ef6f0b652b596173d2c177bb115e64f87efa061dc383b2c303c
failed t60 sidecar sha256 = 168d7cf616d5f95d3ef4851c1288370fcb5beec3040b54663fb481592c488fef
recovery sha256 = 7271ef39a4e245a58c280bb425fb0b96e50225662b5a17349aaa18ef2f1a8cb5
```

The Human authorization was consumed by the successful nonzero Ray command. Strip was not started,
Ray was not retried, and independent recovery proved both sources off.

## Root Cause

`best_effort_gphoto2_v1` correctly labels exposure-start as non-absolute, but the thermal plan, runner,
and analyzer also require proximity to a nominal scheduler slot. The runner waits until nominal `t60`
before starting the remote request, so the camera/bridge delay naturally moves the estimated exposure
start later. The same value is valid timing evidence but fails an incompatible acceptance rule.

The failed post-capture path also increments neither the accepted capture ledger nor the run physical
count, leaving `physical_cr3_count=1` while two nonempty CR3 files exist. V2 must count every produced
CR3 even when later validation fails.

## Human/Developer Decision

The Human/Developer decided that gphoto2's best available estimate is sufficient but is not guaranteed
to be absolute. The value must be recorded and used in calculations. Nominal offset must not be gated
by `+/-2 s` or a similar numeric tolerance. This is not a Planner-authored relaxation.

Tier A/B, finite nonnegative elapsed, exact sidecar replay, provenance, ownership, hashes, physical
accounting, and monotonic within-cycle chronology remain hard requirements. Tier C and corrupt or
missing evidence remain invalid.

## Planned Resolution

The active `.agent-work/PLAN.md` defines offline-only `P7-TD-A-T0`:

- add strict v1/v2 plan and timing-contract dispatch;
- separate nominal scheduler slot from best-effort observed exposure-start elapsed;
- remove nominal-proximity acceptance while retaining evidence-integrity gates;
- use observed elapsed in chronology and report selected slot plus conservative observed max;
- harden produced-CR3 accounting on post-capture failures;
- independently replay the retained t60 evidence without changing the failed run;
- run focused/full regression and stop at Planner review.

No new device run is authorized. A fresh exact Human authorization is required after T0 acceptance.

## Planner closure

R1 closed all five bounded offline findings and was accepted as `R1-PASS` on 2026-07-21. The focused
suite passed `58/58`, the independently rerun full suite passed `502/502`, and the retained old failure
and default operating-envelope hashes were unchanged. The current v2 dry-run plans for Ray and strip
were generated and passed their source-scoped ledger checks with zero device/network side effects.

The implementation defect is resolved, and the Human has since cleared the exact TD-A authorization gate:

```text
next = execute the exact p7_td_a_cold_settling_v1 plan
TD-A real run = authorized_once
TD-B / TD-C / sentinel / P8 = locked
```

The best-effort gphoto2 timing decision remains a Developer/Human decision. Observed elapsed is recorded
and used in calculations, `absolute_exposure_start=false`, and nominal proximity is not an acceptance gate.

## Planner Review of 0344a46

T0 was returned as `T0-CONTRACT-FAIL` after independent review. The no-proximity direction remains
accepted, but five bounded offline gaps must close before real reauthorization:

1. legacy v1 settled TD-A analysis raises `ValueError: max() iterable argument is empty` because v1 rows
   have no observed-elapsed field;
2. runner/analyzer chronology identity omits TD-C `session_index`, so a normal session reset is rejected as
   non-increasing;
3. physical count increments before proving a current-run nonempty CR3 and can report 1 with zero retained
   files;
4. the validated gphoto2 estimate method is lost and the T0 forensic summary records it as null;
5. the shallow-copied `accepted_tiers` list aliases the module contract and can mutate formal acceptance
   rules in-process.

At the time of this initial record, the active PLAN was the offline-only T0-R1 repair package. That
package is now accepted and archived; the current active PLAN is the new exact-Human-authorization gate.
TD-A real execution and all later stages remain locked.
