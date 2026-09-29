# GUIDE9 H300 reference emission/path diagnostic readiness

- Advisor correction accepted: prior evidence is one incomplete run after a valid
  H300 Q-before plus one near-dark H300 observation without complete pre-capture
  state establishment, not two established first-reference failures.
- Current classification:
  `intermittent_H300_reference_emission_or_optical_path_dropout_unresolved`.
- Implemented `GUIDE9_RAY_H300_S100_REFERENCE_EMISSION_PATH_DIAG_V1` as a
  Ray-only, 0-formal/4-physical, order-balanced H0/S0 and H300/S100 diagnostic.
- Frozen shutters remain H0/S0 `1/16000` and H300/S100 `1/2500`; exposure,
  observer, 58 features, thresholds, covariance and coverage are unchanged.
- Capture-bound Ray set/immediate-readback/post-readback and strip-zero evidence
  is written before feature extraction, including rejected captures.
- Focused direct suite: 68 tests passed. Full discovery: 532 tests passed.
- `git diff --check` and `codegraph sync`: passed.
- Clean checkpoint: `9ad9be3`.
- First device attempt root:
  `/Volumes/4T/temp/rgbww-optimizer/guide9-ray-h300-reference-diagnostic-20260823/20260823-order-balanced-v1`.
- Classification: `ENGINEERING_OR_HARNESS_FAILURE`; the camera bridge health
  endpoint passed, but both the attempt and a bounded follow-up config check
  returned HTTP 502 `camera_config_failed` before any light or capture action.
- Captures: 0/4; `science_delta=none`; shell cleanup and independent Ray/strip
  zero readback passed; Git remained clean at the checkpoint.
- `HUMAN_GATE_REQUIRED`: physically wake/confirm the Canon camera and its USB
  connection. After `/v1/config` succeeds, start a fresh diagnostic root.
- Root 1 strip observations remain prohibited from pooling with this diagnostic
  or any fresh H300 batch.

## Completed diagnostic result

- Successful root:
  `/Volumes/4T/temp/rgbww-optimizer/guide9-ray-h300-reference-diagnostic-20260823/20260823-order-balanced-isolation-wired`.
- Acquisition completed 4/4 physical, 0 formal; wrapper, Python cleanup, shell
  cleanup, final Ray/strip zero and Git-clean checkpoint all passed.
- All four capture-bound state records show the exact HSI command, immediate
  readback and post-capture readback at intensity 1000, with strip five-channel
  zero evidence. Recorded shutters were H0 `0.00006103515625 s` and H300
  `0.000387549084953174 s`.
- Both H0 controls and both H300 observations rejected all 92 optimization
  planes as near-noise. Classification: `R-D /
  system_level_Ray_camera_or_optical_path_unresolved`.
- Immutable derived analysis:
  `analysis-guide9-h300-reference-derived.json` in the successful root.
- `HUMAN_GATE_REQUIRED`: inspect visible Ray emission for H0/S0 and H300/S100,
  Ray orientation/obstruction, camera framing/chart position and the physical
  camera/Ray optical path. H300/S50 and all later HSI work remain locked.

## Powered diagnostic correction and current route

- Human identified the concrete physical cause of the prior R-D result: the Ray
  was unplugged while the desktop protocol still returned successful commands.
  That root remains immutable but is not scientific input.
- Fresh powered root:
  `/Volumes/4T/temp/rgbww-optimizer/guide9-ray-h300-reference-diagnostic-20260823/20260823-powered-restored`.
- Acquisition completed 4/4 diagnostic captures with four physical returns,
  complete state evidence, cleanup pass, final zero and clean Git checkpoint.
- Frozen analyzer result: `R-C / H300_S100_reference_repeatability_unresolved`.
  Both H0 controls and both H300 captures were valid; the H300 pair score was
  `20.6931277037` against guarded limit `9.6325691794`.
- H300/S100 is closed. The next branch is the bounded
  `GUIDE9_H300_S50_FAST_DIRECT_BATCH1_V1`; no old strip frames or unplugged-Ray
  observations are pooled into it.

## H300/S50 Batch 1

- Root:
  `/Volumes/4T/temp/rgbww-optimizer/guide9-h300-s50-batch1-20260823/20260823-220027-fast-direct`.
- Acquisition completed 6/6 with six physical returns, quality pass, cleanup,
  final zero and clean checkpoint `4e25adc`.
- Frozen shutters: Ray `1/4000`, strip `1/400`; no prior H300 strip frame or
  unplugged-Ray diagnostic observation was pooled.
- Analyzer result: `H300_S50_batch1_candidate_selected`; Ray bracket passed at
  `3.7789218701 < 9.5994019868`.
- Selected exact command: `CW192/WW4095/R2495/G0/B2559`, direct score
  `1659.5267137795`. Two independent FAST repeats remain required.

## H300/S50 best repeat and route disposition

- Root:
  `/Volumes/4T/temp/rgbww-optimizer/guide9-h300-s50-best-repeat-20260823/20260823-234058-p2-best-ww-wired`.
- Acquisition completed 4/4 with quality, source isolation, cleanup, final zero
  and clean checkpoint `0beb4da`.
- Ray bracket passed: `2.1517060639 < 9.5994440853`.
- Strip repeatability passed: `2.1463390317 < 9.6269509209`.
- Direct scores were `1659.8555741638` and `1659.2476063447`.
- Classification: `H300_S50_stable_nonfaithful`; `faithful=false` and no
  physical-gamut inference is made. H300 route is complete.
- The 13-node grid remains locked because GUIDE9 requires at least one faithful
  chromatic Hue. The mandatory Advisor condition is not met because H120/S25
  and H300/S50 are both measurement-valid and repeatable. The active route moves
  to independent white FAST-DIRECT representative validation.

## GUIDE9 white representative readiness

- Implemented `GUIDE9_WHITE_FAST_DIRECT_REPRESENTATIVE_12_V1` against the retained
  14x5/70-node candidate identity `ea8bffce...a9006`.
- Scope: 12 nodes (`1800/3200/5600/20000 K x GM 0/100/200`), 24 physical/formal
  captures, each reset600 then dwell120, alternating Ray/strip source order.
- Frozen per-node Ray/strip shutters and exact strip commands come from the retained
  candidate. No adaptive solver, global refit, ambient, retry, or LUT installation.
- Analyzer reports native RAW white log-chroma, CCT/mired/Duv paired errors and
  full 58-feature multipatch diagnostic. Failed nodes route only to local correction.
- Focused behavior/runtime: 2/2 passed; dry-run and compileall passed; full suite:
  538/538 passed; `git diff --check` passed.

## White12 acquisition and analysis

- Root:
  `/Volumes/4T/temp/rgbww-optimizer/guide9-white12-20260824/20260824-010145-representative12`.
- Acquisition completed 24/24 with 24 physical returns, quality pass, cleanup,
  final Ray/strip zero and clean checkpoint `8472ec6`.
- Frozen analyzer result: `white_representative_nodes_require_local_correction`.
  Passed nodes: `1/12`; only `5600K/GM200` passed all paired CCT/mired/Duv gates.
- Eleven nodes failed at least one paired white-point gate. Largest deviation was
  `20000K/GM0`: `+2119.83 K`, `-8.3432 mired`, `+0.001365 Duv`.
- The 58-feature multipatch scores are retained as diagnostics, not zero gates.
  Default LUT and global model remain unchanged. Next is failed-node local paired
  correction only; 70/70 remains locked.

## White local-Jacobian candidate result

- Root:
  `/Volumes/4T/temp/rgbww-optimizer/guide9-white-local-jac-20260824/20260824-060631-model-ready5`.
- Acquisition completed 10/10 with quality, cleanup, source isolation, final
  zero and clean checkpoint `678561f`.
- Passed: `3200/GM100`, `5600/GM100`, `20000/GM100`.
- Remaining near-boundary failures:
  `3200/GM200` (`0.7182 mired`, `0.0002546 Duv`; limits `0.5/0.00025`) and
  `20000/GM200` (`155.67 K`, `-0.9527 mired`, `0.0002542 Duv`; limits
  `67.63/0.5/0.00025`).
- A second local-Jacobian step is preregistered for only these two nodes. This
  is a substantive residual-driven correction, not a blind retry; global model
  and default LUT remain unchanged.

## White local-Jacobian second confirmation

- Root:
  `/Volumes/4T/temp/rgbww-optimizer/guide9-white-confirm2-20260824/20260824-081417-gm200-confirm2`.
- Acquisition completed 4/4 with quality, cleanup, source isolation, final zero
  and clean checkpoint `dbb7ae3`.
- Both nodes passed: `3200/GM200` at `-0.585 K / +0.0545 mired /
  +0.000000295 Duv`; `20000/GM200` at `-5.493 K / +0.0340 mired /
  +0.00008334 Duv`.
- Five nodes with retained historical Jacobians are now corrected. Six failed
  nodes without a retained Jacobian remain and require bounded local probes before
  any candidate may be proposed. Default LUT/global model remain unchanged.

## White local-probe readiness

- Implemented `GUIDE9_WHITE12_LOCAL_PROBES_V1` for the six failed nodes without
  retained local Jacobians.
- Each node freezes one current Ray reference, one original base and four
  independent free-channel `±256` probes while retaining its original full-scale
  active channel. Total budget: 36 formal/physical, ambient 0, retry 0.
- The analyzer uses only current-root observations to estimate each 2x4 local
  white-point Jacobian and preregister one candidate. Candidate capture, global
  refit and default LUT mutation are prohibited in this root.
- Focused behavior: 1/1 passed; direct module: 77/77 passed; dry-run, compileall
  and `git diff --check` passed.

## White 70-node FAST-DIRECT recovery and analysis

- The interrupted root completed 4 captures before `KeyboardInterrupt`; a
  second suffix completed 41 captures before a transient device DNS timeout;
  after device restart, a final suffix completed the remaining 95 captures.
- Offline combination of all three roots produced `140/140` unique capture IDs
  (`000..139`). All physical returns, quality rows and source-isolation gates
  were present; Python cleanup and independent Ray/strip zero readback passed.
- The frozen white-node analysis found `11/70` pass and `59/70` failures. This
  is accepted characterization evidence and routes only to
  `GUIDE9_WHITE70_LOCAL_NODE_CORRECTION`; no global refit, default-LUT change,
  interpolation holdout or HSI expansion was performed.
- The canonical CLI rejected the custom recovery spec as differing from the
  12-node protocol, so the frozen white analyzer was run directly against the
  validated 140-row evidence with unchanged feature, covariance and gate
  semantics. The custom recovery spec and all root manifests remain retained
  for audit.

## White local-probe interrupted attempt

- Root:
  `/Volumes/4T/temp/rgbww-optimizer/guide9-white-local-probes-20260824/20260824-092424-no-model6`.
- Completed/expected: `24/36` accepted formal observations plus one rejected
  physical return. The first four target blocks are complete and recoverable.
- Failure classification: `DEVICE_OR_SAFETY_FAILURE` leading to
  `HUMAN_GATE_REQUIRED`; capture 25 (`5600/GM0` Ray reference) rejected all 58
  required features as near-noise.
- Two fresh non-formal diagnostics at `5600K/GM0` and `5600K/GM100`, 100%
  intensity and `1/2500`, both produced dark RAW frames with `median=512`,
  `p99=521`, and `max=534`. This rules out a GM0-only state issue and confirms
  that command/readback success is not currently accompanied by Ray emission
  reaching the camera.
- `science_delta=none` for the interrupted fifth block. The four completed
  blocks remain valid recoverable observations; the rejected frame and two
  diagnostics are not scientific inputs.
- Python cleanup passed; independent final readback confirmed Ray intensity 0
  and all five strip channels 0. Git remained clean at checkpoint `b15c310`.
- Fresh retry is justified only after Human restores/confirms physical Ray
  emission and optical path. Recovery must collect only the remaining two
  blocks and combine them offline with the immutable prefix; it must not repeat
  the first 24 observations.
