# White LUT bounded feedback solver

## Scope

- Offline analysis only. Do not call the camera, Ray120c, or ESPHome.
- Evidence run: `tmp/white-lut-calibration/20260710-002702/white-lut-calibration.json`.
- The run contains 70 targets, 415 feedback samples, and three unmet targets.

## Confirmed observations

- `1800K/GM0` missed only the CCT tolerance: `+11.5929K`, with Duv error `+0.0004768`.
- `14000K/GM130` and `20000K/GM130` failed where WW and R were already at their lower bound.
- `solve_damped_step` solves an unconstrained regularized least-squares system, then clips each channel independently.
- For both high-CCT failures, the unconstrained solution depends on negative WW/R deltas. Clipping removes those deltas but leaves positive G and negative B movement, changing a near-zero predicted residual into a much worse one.
- Across the 70-point data set, the old clipped first step worsens its own predicted goal score for two targets; a box-constrained solve worsens none.

## Root-cause hypothesis

The optimizer is solving the wrong mathematical problem at channel limits. Bounds must be included in the least-squares solve instead of applied after the solution.

## Implemented fix

- `solve_damped_step` now solves the box-constrained regularized least-squares problem directly.
- The exact active-set solver enumerates only `3^4` states for the four free channels and adds no SciPy dependency.
- A regression test reproduces the `14000K/GM130` lower-bound failure.

## Offline verification

- Replayed all 53 targets in the 70-point run that had an initial Jacobian.
- Old post-solve clipping produced two predicted first-step regressions; the bounded solver produced zero.
- New predicted first commands for the three failed targets:
  - `1800K/GM0`: `cw=65 ww=3744 r=4095 g=23 b=113`, predicted score `0.0196`.
  - `14000K/GM130`: `cw=4095 ww=0 r=0 g=710 b=998`, predicted score `0.2277`.
  - `20000K/GM130`: `cw=4095 ww=0 r=0 g=768 b=1207`, predicted score `0.2033`.
- Repeated-command stability across the captured data: median CCT difference `1.43K`, P90 `5.31K`; median Duv difference `1.19e-5`, P90 `5.22e-5`.
- Two exposure-warning duplicate pairs were CCT outliers at `150-171K`; future cross-target sample reuse must exclude exposure warnings and outlier repeats.
- Focused feedback tests: 8 passed.
- Full suite: 134 passed.

## Remaining verification

- The predicted commands have not been photographed because this optimization pass explicitly forbids device calls.
- Keep this issue unresolved until the original three targets are rerun on hardware.
