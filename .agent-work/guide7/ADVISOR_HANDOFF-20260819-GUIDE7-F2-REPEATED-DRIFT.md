# Advisor handoff — GUIDE7 F2 repeated strip block drift

## Exact question

Two complete CW-active F2 blocks have valid Ray references, quality, exposure,
source isolation and cleanup, but both fail the second strip base anchor. The
single allowed fresh repeat is exhausted. What exact scientific disposition and
next experiment, if any, should replace the current F2 block?

Please decide whether:

1. the fast F2 history/dwell/anchor design needs one bounded measurement-science
   correction;
2. the CW-active face should be classified as unstable under the current fast
   envelope and skipped for this route;
3. another already justified face/scale/lower-SAT branch should be used.

Do not interpret these roots as stable nonfaithful, solver-coordinate failure,
or gamut/physical unreachability. State whether 3072 may be unlocked or remains
locked. Preserve the frozen direct 58-feature estimand, covariance, coverage,
observer and thresholds unless the decision explicitly changes them.

## Current conclusion

```text
F2_block_1 = accepted_valid_reference_failure
F2_block_2 = accepted_valid_reference_failure
Ray_brackets = pass/pass
strip_anchor_1 = pass/pass
strip_anchor_2 = fail/fail
best_base_repeatability = fail/fail
F2_stable_nonfaithful = not_established
solver_attempt_count = 0
gamut_inference = prohibited
third_F2_block = prohibited
ADVISOR_GATE_REQUIRED = true
```

## Shared protocol

- Experiment: `GUIDE7_H120_S100_F2_ALTERNATE_FACE_CONTROLLABILITY_V1`.
- Offline-selected face: CW active.
- Base: `CW4095/WW0/R0/G3839/B0`.
- Free probes: WW, R, G and B; the G probe is `3839 -> 4095`.
- Ray before/after: fixed `1/5000`.
- Strip observations: fixed `1/400`.
- History: reset600, D120, A120, tested120.
- Two base anchors and three base repeats when no unique candidate exists.
- Every strip capture records Ray intensity zero; every Ray capture records all
  five strip channels zero.
- P2 predicted seed is seed-only and not scientific acceptance.
- Contaminated historical GUIDE6 roots and `1/320` guard were not used.

## Block 1

- Root:
  `/Volumes/4T/temp/rgbww-optimizer/guide7-h120-s100-f2-alternate-face-20260819/20260819-225543-cw-active-base-repeat-fix`
- Captures: 12; candidates 0; base repeats 3.
- Ray bracket: `3.6566 / 9.5432`, pass.
- Anchor 1: `5.3259 / 9.5614`, pass.
- Anchor 2: `15.6161 / 9.5614`, fail.
- Repeat pair scores: `9.7096`, `9.6119` against about `9.5614`.
- Analysis SHA-256:
  `0998b27b7d6ba58bc008b1ce26fc81fd087c138ec15e9200e3aa379a8c428bcb`.
- Captures SHA-256:
  `b388620ed5782d0f8946139d192a0f61d797b805ca21cae88862563c5f1d2a97`.

## Block 2 — permitted fresh repeat

- Root:
  `/Volumes/4T/temp/rgbww-optimizer/guide7-h120-s100-f2-reference-repeat-20260819/20260819-004620-cw-active-reference-repeat`
- Captures: 12; candidates 0; base repeats 3.
- Ray bracket: `3.5065 / 9.5433`, pass.
- Anchor 1: `2.2890 / 9.5614`, pass.
- Anchor 2: `12.4327 / 9.5614`, fail.
- Repeat pair scores: `14.7520` fail, `2.1592` pass.
- Analysis SHA-256:
  `121e909161c2d289f8cc0f385943cee8796b7e7f402b4c9711f1493abe71744b`.
- Captures SHA-256:
  `00f0b302b0521404232a115edfe5fa2bd895880e810235b251a1a764b0044eb3`.

## Interpretation boundary

- Ray references are stable in both blocks, so the failure is localized to the
  strip block rather than the Ray target.
- The second anchor fails after the full four-probe sequence in both roots.
- The repeat behavior is not consistently stable; therefore no valid F2-B/F2-C
  classification exists.
- No solver candidate was executed because the bounded solver returned no new
  unique command; this is permitted F2-C mechanics, but the drift gate overrides
  any local-inadequacy conclusion.
- Repository-local work cannot choose a new thermal/history design or skip the
  failed face without making a new scientific decision.

## Safety and state

- Both complete roots exit 0 and retain quality pass.
- Cleanup and independent final all-off/readback pass.
- Ray intensity is zero and all five strip channels are zero.
- Worktree is clean; no automation or experiment process remains.
- 3072, 13-node grid, full boundary, Gate-6, P8 and LUT installation remain locked.

## ZIP contents

The ZIP beside this Markdown contains calculated/derived evidence, run/quality/
command/isolation/cleanup summaries, exact relevant source/tests, GUIDE/RESEARCH/
PLAN documents and a SHA-256 manifest. It excludes CR3/RAW, decoded arrays,
image derivatives, firmware, build output, caches, credentials and nested archives.
