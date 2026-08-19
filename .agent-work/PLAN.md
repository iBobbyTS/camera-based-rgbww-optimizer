# PLAN — one GUIDE7 F2 reference/block-drift repeat

## Retained F2 result

- Root:
  `/Volumes/4T/temp/rgbww-optimizer/guide7-h120-s100-f2-alternate-face-20260819/20260819-225543-cw-active-base-repeat-fix`
- Acquisition: 12/12 accepted; quality, source isolation, cleanup and final zero pass.
- Ray bracket: pass (`3.6566 < 9.5432`).
- First strip base anchor: pass (`5.3259 < 9.5614`).
- Second strip base anchor: fail (`15.6161 > 9.5614`).
- Base repeats are not stable under the frozen same-state guard.
- Classification: `target_block_reference_invalid` / F2-E strip block drift.
- No candidate, stable-nonfaithful, solver, scale or gamut conclusion is allowed.

## Exact next action

- Run one fresh root with the unchanged
  `GUIDE7_H120_S100_F2_ALTERNATE_FACE_CONTROLLABILITY_V1` contract.
- Keep CW active, base `CW4095/WW0/R0/G3839/B0`, free WW/R/G/B, Ray `1/5000`,
  strip `1/400`, two anchors and three best/base repeats when nonfaithful.
- Do not pool or resume the invalid block.
- This is the one permitted reference/block-drift repeat.
- If the fresh block again fails Ray bracket or strip drift, enter
  `ADVISOR_GATE_REQUIRED`; do not start a third F2 block.
- If stable, follow F2-A/B/C/D automatically.

Keep 3072, 13-node grid, full boundary, Gate-6, P8 and LUT installation locked
until a stable F2 classification exists.
