# P7 TD-B formal statistic owner C3

## Resolved Defect

The retained R1 capture contained all 58 frozen no-ambient feature values, but
the TD-B production runner called `required_hsi_features_from_report()` without
an explicit statistic. The shared ambient-subtracted default therefore produced
58 `missing_statistic` rejections.

## Fix

- The feature helper accepts a keyword-only explicit statistic while keeping
  `ambient_subtracted.trimmed_mean_per_second` as its unchanged default.
- `TD_B_FORMAL_FEATURE_STATISTIC` is the single owner for
  `statistics.normalized_per_second.trimmed_mean`.
- Only a validated exact TD-B v2 formal plan with the frozen no-ambient policy
  and owner selects that statistic.
- Runner and retained analyzer reject policy, subtraction, phase or formal-role
  context drift and use the same constant and feature helper.
- The lineage allowlist includes only the new feature-owner module and its test;
  unrelated paths remain prohibited.

## Evidence

- Frozen report: `58/58` finite and quality accepted.
- Six raw rejected planes remain diagnostic-only and disjoint from the frozen
  58 feature IDs.
- Runner/analyzer feature-map SHA-256:
  `549d76837ae351f87649ee922a1e065c8eb0cd211ea6a8fbc4b53b07a262e303`.
- Retained run: 16 files unchanged before/after replay.
- Targeted `113/113`, focused `197/197`, full suite `553/553`.
- Compileall, wrapper syntax, diff check and CodeGraph sync passed.

Implementation commit:
`fa6c95dbf79f4c0828e8633560d2828e3646204b`.

Evidence directory:
`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-r1-c3-offline/20260724-061143`.

Validation summary SHA-256:
`3dc83c0d98d7f76549724ebc92548ee8eca39e49ccf95846d6e5497a22256daa`.

No device, network, `.env`, camera, light, `all_off`, new CR3, formal analyzer
CLI, lineage release or E2 execution occurred.
