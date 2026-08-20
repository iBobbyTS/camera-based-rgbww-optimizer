# ADVISOR HANDOFF — GUIDE7 scale-relaxed stability exhausted

## Gate

`ADVISOR_GATE_REQUIRED`

The pre-defined scale-relaxed diagnostic sequence is now exhausted. The
full-scale short endpoint failed repeatability, and both permitted lower-scale
stability diagnostics (3072 and 2048) also failed the frozen direct
58-feature repeatability gate. This is a scientific measurement interpretation
and next-branch question, not an implementation or cleanup failure.

## Accepted measurements

### 3072

- Root: `/Volumes/4T/temp/rgbww-optimizer/guide7-h120-s100-scale3072-stability-20260820/20260820-020912-stability-first`
- Result: 5/5 formal and physical captures; quality, wrapper, cleanup and zero passed.
- Ray bracket: score `3.294860787963735`, guard `9.54309334973631`, pass.
- Strip repeat scores: `29.563302177583065`, `25.90464436278202`, and
  `4.738735074769447`; guard approximately `9.5614`.
- Classification: `R-UNSTABLE / scale3072_short_repeatability_unresolved`.

### 2048

- Root: `/Volumes/4T/temp/rgbww-optimizer/guide7-h120-s100-scale2048-stability-20260820/20260820-034957-stability-first`
- Result: 5/5 formal and physical captures; quality, wrapper, cleanup and zero passed.
- Ray bracket: score `1.4223787757934117`, guard `9.543215625186967`, pass.
- Strip repeat scores: `10.909252857513083`, `11.216105130033172`, and
  `1.7036074692778231`; guard approximately `9.5615`.
- Classification: `R-UNSTABLE / scale2048_short_repeatability_unresolved`.

Both runs used the exact frozen observer, 58 features, covariance, coverage,
thresholds, Ray `1/5000`, strip `1/400`, reset600 and D/A/tested120 protocol.
Neither run executed probes, Jacobian, solver candidates or in-run retries.
Both had Ray bracket pass and final all-off/readback zero.

## Scientific question for Advisor

Please decide the next scientific branch after both pre-defined scale-relaxed
stability diagnostics failed:

1. Should H120/S100 be classified as a reproducible short-block operating
   instability under the frozen FAST contract, while retaining the result as a
   valid negative and moving to the next GUIDE7 lower-SAT/H120/S50 route?
2. Is one additional measurement-science diagnostic justified, and if so what
   exact bounded protocol distinguishes source-age/block drift from a
   scale-dependent operating effect?
3. May any probe or bounded solver route be unlocked at 2048/3072, or must all
   solver/probe work remain locked until a stability design is changed?

Do not infer physical or gamut unreachability from these failures. Do not alter
the observer, features, covariance, coverage, thresholds, exposure or frame
selection without an explicit scientific decision.

## Repository state and implementation boundary

- Live branch: `codex/guide4-science-path-v3`
- Latest code/evidence checkpoint: `2ae78ea9b02c8c09bc5bf6c8699ba8ee008c36ca`
- Worktree: clean before this handoff document.
- Existing direct owner was reused; no generic runtime, stage-gate, solver or
  provenance framework was added.
- Active PLAN records the 2048 result and locks grid, boundary, Gate-6, P8 and
  LUT installation.

## Included evidence

The adjacent ZIP contains derived analysis, quality/run/cleanup summaries,
capture and physical ledgers (metadata only), thermal covariates, exact source
and behavior tests, active PLAN/PLAN-FULL/EXECUTION_RESULT, and applicable
GUIDE/RESEARCH documents. Raw CR3/RAW, decoded arrays, image derivatives,
firmware, build output, caches, credentials and nested archives are excluded.

The ZIP manifest records each included file's absolute source path, byte count
and SHA-256.
