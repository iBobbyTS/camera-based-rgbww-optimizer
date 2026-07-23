# P7 TD-A: 600-second instability accepted as an operational limitation

## Status

`resolved_by_developer_operational_time_limit_not_scientific_settling`

## Valid completed evidence

- Ray run: `/Volumes/4T/temp/rgbww-optimizer/p7-thermal-diagnostics/p7-td-a-ray-debug`.
- Strip run: `/Volumes/4T/temp/rgbww-optimizer/p7-thermal-diagnostics/p7-td-a-strip-20260722-001426`.
- Paired analysis: `/Volumes/4T/temp/rgbww-optimizer/p7-thermal-diagnostics/p7-td-a-paired-20260722-022200/td-a-combined-analysis.json`.
- Combined SHA-256: `99550214c619160b39cbf7f393e6b8dc3a5b3feae8f91d0a1765c272283c3160`.
- Acquisition is valid: `24 formal + 6 ambient = 30 physical CR3`, all non-empty, recorded exposure present,
  no NPY, no failure, and all isolation/readback/cleanup/wrapper contracts pass.

## Scientific result

Frozen trend limit is `4.0`.

- Ray cycle scores: `17.7369 / 16.8013 / 16.7317`.
- Strip cycle scores: `16.8865 / 10.3106 / 11.8856`.
- Maximum single-frame variance fractions are `0.2003` and `0.2059`, below the frozen `0.5` limit.

The failure is persistent chronology trend in every cycle, not a single-frame dominance failure. Neither source
has a measured settle time; `t_formal_provisional_s` remains null.

## Developer resolution

Developer/Human explicitly rejected a 900/1200-second extension and selected 600 seconds as the operational time
limit because further delay is not desired at this point. This is not a Planner inference and does not claim
scientific settling.

The production contract must use `developer_selected_operational_dwell_s=600` and retain
`settling_not_demonstrated_by_600`. It must not write 600 into `t_formal_provisional_s`, change frozen gates, or
alter retained TD-A evidence.
