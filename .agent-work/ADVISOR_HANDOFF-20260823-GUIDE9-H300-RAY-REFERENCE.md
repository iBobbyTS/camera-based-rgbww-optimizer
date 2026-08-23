# Advisor Handoff: GUIDE9 H300/S100 Ray Reference Failure

## Gate

`ADVISOR_GATE_REQUIRED`

GUIDE9 H300/S100 FAST-DIRECT Batch 1 cannot be scientifically classified because
the Ray reference failed twice at the first observation. The two failures are
independent roots under the same frozen protocol and the same qualified exposure
policy. GUIDE9 §15.2 requires Advisor input after two reference/measurement
failures.

## Exact Question

Should this be classified as a system-level Ray/reference/optical measurement
failure, or is another bounded diagnostic/exposure or physical check required
before the H300 route can continue? In particular, should the route remain at
`GUIDE9_H300_S100_FAST_DIRECT_BATCH1_V1`, move to a Ray-only diagnosis, or mark
H300 as an isolated `measurement_unreachable` node while preserving the rest of
the GUIDE9 sentinel route?

## Frozen Protocol

- Experiment: `GUIDE9_H300_S100_FAST_DIRECT_BATCH1_V1`
- Ray: H300/S100, `reset600 -> D120 -> A120`, shutter `1/2500`
- Strip: four offline candidates, `reset600 -> D120 -> A120 -> tested120`, shutter `1/125`
- Budget: 6 formal, 6 physical, ambient 0, retry 0
- No probes, solver, 13-node grid, boundary, Gate-6, P8, or LUT installation
- Observer, 58 features, covariance, thresholds, and coverage were unchanged

## Results

### Root 1: interrupted late

`/Volumes/4T/temp/rgbww-optimizer/guide9-h300-s100-batch1-20260821/20260821-092100-fast-direct-auth-fixed`

- 5/6 physical captures completed; the first Ray and four strip observations passed feature quality.
- The process disappeared before Ray-after, so no complete scientific result exists.
- The root is retained as incomplete historical evidence and is not pooled as a valid six-capture result.
- Cleanup later passed; all channels and Ray intensity were zero.

### Root 2: repeated Ray reference failure

`/Volumes/4T/temp/rgbww-optimizer/guide9-h300-s100-batch1-20260823/20260823-h300-retry2`

- 0/6 accepted formal observations; one physical Ray CR3 returned.
- `HsiRejectedFeaturesError: 58 required HSI observer features were rejected`.
- No `captures.jsonl` or `quality.json` was produced; no strip capture began.
- Wrapper child exit `1`; shell cleanup exit `0`; `run.json cleanup=pass`.
- Final ESPHome payload and Ray intensity were both zero.

## Interpretation Boundary

This is not evidence about strip color fidelity, gamut reachability, or H300
direct-score performance. It is a repeated failure to establish the Ray
reference observation needed to define the target-local contrast. No threshold,
exposure, observer, covariance, feature, or frame-selection change was made.

## Evidence and Reproducibility

The adjacent ZIP contains derived patch-statistics JSON, experiment specs,
run/capture/physical-return/isolation/cleanup/wrapper summaries, failure logs,
the exact active source and focused test files, GUIDE9/RESEARCH, PLAN and
PLAN-FULL, plus a manifest of source paths, sizes and SHA-256 hashes.

Raw CR3/RAW payloads, camera arrays, firmware, build output, credentials and
generated archives are intentionally excluded. Their retained absolute paths,
sizes and hashes are recorded in the manifest where needed for identity.

Handoff files:

- Markdown: `.agent-work/ADVISOR_HANDOFF-20260823-GUIDE9-H300-RAY-REFERENCE.md`
- ZIP: `.agent-work/ADVISOR_HANDOFF-20260823-GUIDE9-H300-RAY-REFERENCE-v2.zip`
- ZIP SHA-256 is recorded after archive validation in the final response.

## Current State

- No experiment process or automation remains active.
- Device cleanup and zero-state readback passed.
- Git worktree is clean at commit `565dc7a57c66fad2d5a0cecc83b0d692635e3716`.
- No third H300 acquisition will be started until Advisor resolves the question above.
