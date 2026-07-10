# White LUT light isolation and exposure cache

## Root cause

- The formal LUT loop turned the strip off before Ray reference captures but did not turn Ray off before strip feedback captures.
- Strip feedback reused the Ray reference shutter instead of establishing an independent strip exposure.
- Outside the native white-channel CCT span, the model forced WW/CW to own the `4095` constraint even when R/B compensation needed to own it.

## Fix

- Ray is set to intensity `0` immediately after every reference capture; failure to turn it off aborts before strip capture.
- Ray and strip shutter caches both initialize from fixed `1/30` and advance only from the previous result for the same source.
- Each target's initial strip candidate auto-exposes from the strip cache; probes and feedback keep that target's resolved strip shutter fixed.
- Outside-range model candidates allow low-penalty compensation RGB channels to own `4095`, preserving the true active channel through feedback.
- Formal LUT feedback defaults to six rounds, with the existing early stop unchanged.
- `all_off` rejects invalid Ray off-state CCT/G-M reads and uses a valid fallback.

## Verification

- Regression test records `Ray -> strip -> Ray -> strip` captures with no simultaneous source state and independent shutter chains.
- Full isolated run: `tmp/white-lut-calibration/20260709-233232`.
- Focused successful retries: `20260709-235603` for 1800K/GM0, `20260709-235317` for 1800K/GM200, and `20260709-235842` for 20000K/GM100.
- Consolidated LUT: `config/white/white-lut.json` and `tmp/white-lut-calibration/white-lut-20260709-isolated-best.json`.
- All 12 targets satisfy absolute CCT error `<10K` and absolute Duv error `<0.01`.
- Full test suite: 133 tests passed.
