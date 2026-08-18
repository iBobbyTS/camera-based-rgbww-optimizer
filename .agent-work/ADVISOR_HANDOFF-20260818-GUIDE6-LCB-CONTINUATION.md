# Advisor handoff — GUIDE6 H120/S100 two valid LC-B blocks

## Exact question

Two isolated, exposure-qualified direct target-local blocks are scientifically
valid and both classify LC-B. The one permitted generation-1 centered
continuation is exhausted. What is the next scientifically valid branch and
exact experiment, if any?

Please decide among, or replace with a more precise route:

1. an alternate active-set screen with an exact bounded design;
2. a revised solver-navigation diagnostic that preserves the frozen final direct
   58-feature estimand, covariance and coverage;
3. termination of H120/S100 under an exact non-gamut classification.

Do not interpret these data as proof of gamut or physical unreachability. State
the lock disposition for the 13-node grid, boundary, Gate-6, P8 and LUT install.

## Current conclusion

```text
qualification = accepted
F1 = accepted_valid_LC_B
generation_1_continuation = accepted_valid_LC_B
second_continuation = prohibited
gamut_inference = prohibited
terminal_multi_start_solver_unresolved = false
ADVISOR_GATE_REQUIRED = true
```

Both blocks preserve the same scientific contract: direct same-block ordered
58-feature strip-minus-Ray contrast, frozen source covariance and 0.9973 guarded
coverage. Neither block pools the contaminated historical roots or compares Ray
and strip absolute brightness as color matching.

## Exposure and isolation prerequisite

- Strip qualification root:
  `/Volumes/4T/temp/rgbww-optimizer/guide6-strip-exposure-qualification-20260818/20260818-003422-s-measurement`
- Selected/guard shutter: `1/400` / `1/320`.
- Qualification: 8/8 diagnostic, 58/58 valid pair, shape compatible.
- Qualification evidence SHA-256:
  `13a289ad62e3b991166500ac354576efb8919866c64f97f5cb9199840e7abcce`.
- Every strip capture in both LC-B blocks records Ray intensity zero.
- Every Ray capture records all five strip channels zero.
- All captures use strip `1/400` or Ray `1/5000`; guard `1/320` is never used.

## Block 1 — fresh F1

- Root:
  `/Volumes/4T/temp/rgbww-optimizer/guide6-direct-target-local-f1-20260818/20260818-005758-strip-1over400-fresh`
- Center: `CW518/WW0/R0/G4095/B0`.
- Captures: 13 total; 2 Ray, 11 strip; 4 candidates; 0 confirmations.
- Classification: `H120_S100_local_controllable_but_not_yet_faithful`.
- Analyzer base score/guard: `1471.8684202769587 / 9.511252775532636`.
- Analyzer candidate scores: `1469.9201512237514`,
  `1468.2674910054316`, `1468.9092129200485`, `1469.9435390214342`.
- Ray bracket: `7.578398793600923 / 9.54298912856529`, pass.
- Strip anchors: `4.801721464065255`, `5.015452126809423`, pass.
- Analysis SHA-256:
  `1dd0a994749a41f2b649e64af5c75c46959f1e828599955dc1fc6ae81948e7b5`.
- Captures SHA-256:
  `68b76cb12e6c826a5bd9f26e1f74cb52f03e3dd10960ad6b7eaa60f400e0e043`.

## Block 2 — single centered continuation

- Root:
  `/Volumes/4T/temp/rgbww-optimizer/guide6-direct-target-local-lcb-continuation-20260818/20260818-030922-centered-r377-b107-auth-fixed`
- Generation: 1.
- Center: `CW0/WW0/R377/G4095/B107`.
- Captures: 13 total; 2 Ray, 11 strip; 4 candidates; 0 confirmations.
- Classification: `H120_S100_local_controllable_but_not_yet_faithful`.
- Analyzer base score/guard: `1459.4726873465686 / 9.507745630047346`.
- Analyzer candidate scores: `1460.6275781818379`,
  `1462.9196996395515`, `1460.599316880197`, `1457.9065349594123`.
- Ray bracket: `4.463160213152241 / 9.54312709398941`, pass.
- Strip anchors: `4.362800071159782`, `5.408211736783729`, pass.
- Acquisition-side best command: `CW0/WW93/R346/G4095/B101`.
- Analysis SHA-256:
  `1c4746976c6e60dd10d25d99c71a195e4165b0db1503ab03b5bdac9be5304bad`.
- Captures SHA-256:
  `d07f331bdbcce157f1dcb6ed37768d7b046516f838ef415b4d20a2ce45cfb1d2`.

## Interpretation boundary

- Same-source device health is normal under the isolated five-channel/Ray
  baseline at commit `99730c4`.
- Cross-source direct color-shape mismatch remains large under the frozen
  estimand.
- Absolute brightness is not the acceptance target and was not used to judge
  color matching.
- The continuation shows only a small local improvement. It does not establish
  that no other active set or scientifically justified navigation experiment
  could improve the result.
- Repository-local work cannot select the next scientific experiment without
  inventing a new branch beyond the exhausted GUIDE6 continuation allowance.

## Safety and state

- Both acquisitions exited 0 with quality pass.
- Python cleanup and independent final all-off/readback pass.
- Ray intensity is zero; all five strip channels are zero.
- Worktree was clean throughout acquisition and analysis.
- No automation, test, capture or experiment process remains.
- No raw CR3, decoded arrays, image derivatives, firmware or build output is
  included in the handoff ZIP.

## ZIP contents

The ZIP beside this Markdown contains derived/calculated experiment evidence,
small run/quality/command/isolation/cleanup artifacts, exact relevant source and
tests, GUIDE/RESEARCH/PLAN documents, policies, contamination baseline document,
and a manifest with original absolute paths, byte counts and SHA-256 values.
Raw and bulk payloads are referenced by their retained paths and hashes only.
