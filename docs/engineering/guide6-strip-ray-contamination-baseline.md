# GUIDE6 strip/Ray contamination baseline

## Status

- Recorded: 2026-08-17
- Classification: `ENGINEERING_OR_HARNESS_FAILURE / historical cross-source contamination`
- Device-health conclusion: camera/chart geometry, all five strip channels, and
  Ray white output are consistent with the accepted historical device baselines.
- Scientific reuse: the two listed GUIDE6 strip candidate captures are
  historical-only and must not define strip brightness, a strip target center,
  or a strip-minus-Ray acceptance residual.
- Device state after the recheck: strip five-channel zero and Ray intensity zero.

This document separates two facts that were previously confused:

1. The physical strip and Ray are currently producing substantially the same
   isolated outputs as their accepted 2026-07-16 references.
2. Two later GUIDE6 captures labeled as strip candidates contain a Ray-shaped
   observation and lack evidence that Ray was off before the strip exposure.

## Canonical comparison conditions

The current full-scale comparison root is:

```text
/Volumes/4T/temp/rgbww-optimizer/manual-five-channel-ray-comparison-20260817/current-vs-p2
```

The five strip channels use the accepted P2 root:

```text
/Volumes/4T/temp/rgbww-optimizer/chart-response-basis/p2-five-channel-basis-20260716-005935
```

The Ray white comparison uses the accepted P1 boundary root:

```text
/Volumes/4T/temp/rgbww-optimizer/raw-observer-validation/p1-d2-boundary-1x-1.25x-20260716-000647
```

All comparisons use:

- Canon native Bayer `R/G1/G2/B` patch statistics;
- ISO 100;
- location SHA-256
  `21f02328bff8b5ffcfc10c767e15cdefbf8bb883bc352eff6f0fb7ade38a8f80`;
- the same per-channel shutter used by P2, or `1/16000` for Ray white;
- one isolated source at a time and 60 seconds of source-on time;
- exposure-normalized trimmed means;
- the median of the three accepted historical repetitions;
- no ambient subtraction, refit, covariance change, threshold change, or
  pooling into a formal scientific result.

| Source | State | Shutter | Strong-feature current/history | L2 current/history | Shape cosine |
| --- | --- | ---: | ---: | ---: | ---: |
| R | `R=4095` | `1/125` | `0.954109` | `0.958818` | `0.999984` |
| G | `G=4095` | `1/320` | `0.960971` | `0.964009` | `0.999983` |
| B | `B=4095` | `1/400` | `0.950352` | `0.952244` | `0.999979` |
| CW | `CW=4095` | `1/200` | `0.947788` | `0.951478` | `0.999981` |
| WW | `WW=4095` | `1/200` | `0.946989` | `0.950543` | `0.999982` |
| Ray | `5600K/GM100/100%` | `1/16000` | `0.986892` | `0.980871` | `0.999859` |

Some current monochromatic reports reject weak off-spectrum CFA planes at the
frozen near-noise threshold. That does not imply a dead channel: the
strong-response feature ratios and near-unit shape cosines above are the bounded
device-emission diagnostic. These captures are not promoted into a formal GUIDE
fit or pass/fail result.

## Current evidence identity

| Source | CR3 SHA-256 | Patch-statistics SHA-256 |
| --- | --- | --- |
| R | `06304bdaab700d6c2e578ac410d9353cd69c997235a1816715374d74951ca7dc` | `f10e5874a9209adaaf14e2cc9a35542231a747354b2318218964440ecaa94020` |
| G | `299f9119eb824ca8c9f9c62a7b72119b842196bdac64d5de25b1f0df98303919` | `e952b52f4ec44d4508753d0dd24295fc9fd8b9055e552776e6491951f8712fd7` |
| B | `be12b0ccd6fcfe34bbd52858fcf80a042ff77d0df6e44e15295607805d35fd2e` | `5d38a06aa3c942680085431adcffbe5ed1ef0155cd0d6f946f3b333a84afb6d6` |
| CW | `4db74971a5fc56b5841dbb6ba4219e862da8db70a9691ea560e1079d0dbc2d6f` | `d5ecf40fe286a0f0498b3e26f7d39767e02a8f4f076bad90bf93b62456c7f996` |
| WW | `19174bc68b4bda3fbc2c31dc5c6ef7fd66efbd84e7216c6ae4e58862d5da3467` | `8bd30354509376b3b9c1eda4089e834bd0e45359bee0b845d6217b80591c2e8a` |
| Ray | `2938bce38a096a7635e56e53b2686007459121871dcdbbf21f0ea408a337698d` | `030c356164a14bd827288ee682dedb3543a83d695c7b5b3f63130a4ada7156c0` |

The CR3 and patch-statistics payloads remain external experiment data. They are
referenced here by retained absolute path and hash and are not tracked by Git.

## Invalid GUIDE6 strip-only reuse

The affected roots are:

```text
/Volumes/4T/temp/rgbww-optimizer/guide6-direct-target-local-h120-s100-20260813/20260814-075000-qualified-strip-1over1600-reference-repeat
/Volumes/4T/temp/rgbww-optimizer/guide6-direct-target-local-h120-s100-20260813/20260814-080000-qualified-strip-1over1600-solver-repeat
```

The affected capture in each root is:

```text
005-strip-h120-s100-strip_candidate
```

The command ledger first sets Ray to H120/S100 at intensity 1000, then records
the strip D and A commands without an intervening Ray-off entry. The capture row
does not contain `ray_zero_before_capture` or source-isolation evidence. The
first historical candidate compared with the isolated current Ray H120/S100
observation as follows:

| Comparison | Value |
| --- | ---: |
| L2 historical candidate / current Ray | `1.002719` |
| Shape cosine | `0.999947` |
| Pearson correlation | `0.999892` |
| Historical candidate median | `183.7965 /s` |
| Current isolated Ray median | `184.8804 /s` |

By contrast, the same historical candidate is `17.526x` the L2 magnitude of the
isolated post-power-cycle strip command `CW=518, G=4095`. Both historical CR3s
and the current strip CR3 record the same Canon MakerNote exposure
`0.000615195825143981 s` for nominal `1/1600`, so an exposure-normalization
mistake does not explain the discrepancy.

The only evidence-supported disposition is:

```text
guide6_reference_repeat.strip_candidate = HISTORICAL_CROSS_SOURCE_CONTAMINATED
guide6_solver_repeat.strip_candidate    = HISTORICAL_CROSS_SOURCE_CONTAMINATED
implementation_input_allowed            = false
strip_target_center_allowed             = false
strip_brightness_baseline_allowed       = false
```

## Reuse rules

1. Use P2 isolated channel captures and this 2026-08-17 recheck when deciding
   whether a physical RGBWW channel or the camera/chart geometry changed.
2. Use the P1 boundary root and this recheck when deciding whether Ray white
   output materially changed.
3. Never compare a new isolated strip observation against the contaminated
   GUIDE6 `183.8 /s` value or use that value to trigger a physical strip gate.
4. A future cross-source capture is eligible only when the retained evidence
   proves the opposite source was zero before exposure. A command ledger that
   merely switches owners is insufficient.
5. Do not correct, subtract, or salvage the contaminated GUIDE6 vectors. Preserve
   them unchanged as evidence of the execution defect.
6. Any GUIDE6/7 direct-target computation derived from those contaminated strip
   vectors must be rebuilt from an isolated target-local observation or returned
   to its scientific decision owner if the replacement changes the intended
   estimand.
