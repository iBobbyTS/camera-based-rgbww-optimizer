# PLAN — GUIDE7 H120/S100 actual F1 local controllability

## Accepted prerequisite

- GUIDE8 root:
  `/Volumes/4T/temp/rgbww-optimizer/guide8-ray-emission-exposure-20260815/20260815-163556-diagnostic`
- Acquisition: complete, 4/16 diagnostic captures, formal 0, cleanup pass.
- Frozen analyzer branch: `E-C / historical_shutter_requalified`.
- Selected Ray shutter: `1/5000`; adjacent guard: `1/4000`.
- Derived analysis SHA-256:
  `4cf9aefed30acd141a8a08a2ee507aa26c9c7a9333253dd7b8d372bfd2278295`.
- Versioned policy:
  `config/hsi/ray-h120-s100-exposure-policy-v2.json`.

## Immediate scientific action

Execute one fresh
`GUIDE6-DIRECT-TARGET-LOCAL-H120-S100-V1` root through the existing direct
measurement owner. This is the GUIDE7 actual F1 local-controllability block
unlocked by GUIDE8 E-C; no new implementation section or authorization gate is
required.

Frozen bounds:

- Ray `Q_before` and `Q_after`: fixed `1/5000`, reset600/D120/A120/Q120.
- Strip measurements: fixed `1/1600`, one reset600, then D120/A120/tested120.
- Exact base command and four G-active probes remain those frozen in the direct
  plan; at most four solver candidates, one rebase, and three confirmations.
- Ray cap 2, strip cap 14, total/formal cap 16, ambient 0, in-run retry 0.
- Frozen observer, ordered 58 features, quality, covariance, guarded coverage,
  box constraints, 768 maximum step and backtrack remain unchanged.
- Preserve source isolation and final all-off/zero evidence.

## Branch continuation

Run the frozen GUIDE6 analyzer once and follow only LC-A/B/C/D/E and the GUIDE7
predefined continuation. Do not enter the 13-node grid, per-Hue boundary,
Gate-6, P8 or LUT installation before the four-point direct sentinel is
scientifically completed.
