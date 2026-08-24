# PLAN-FULL — GUIDE9 science-first route

1. Completed: H120/S100 search closed after scale-age classification; H120/S50
   was stable nonfaithful; H120/S25 established no faithful lower endpoint.
2. Completed: H0/S0 is `H0_S0_stable_nonfaithful` with valid Ray bracket and
   compatible strip repeats.
3. Diagnose the intermittent H300 reference/path dropout with the four-frame,
   Ray-only `GUIDE9_RAY_H300_S100_REFERENCE_EMISSION_PATH_DIAG_V1`.
4. If both H0 controls and both H300 observations pass and H300 repeats, run
   one fresh complete H300 Batch 1. If H300 alone fails or does not repeat,
   close S100 and continue at H300/S50. If either H0 control fails, stop HSI
   for a system-level physical inspection.
5. Reassess the 13-node grid unlock only after H300 is classified. Boundary,
   Gate-6, P8 and LUT remain locked.

## Historical GUIDE7 roadmap

1. Reject the two Ray-contaminated GUIDE6 strip candidates as historical-only
   evidence; never pool or import them into scientific analysis.
2. Completed: `GUIDE6_S_MEASUREMENT_STRIP_EXPOSURE_QUALIFICATION_V1` qualified
   strip `1/400`, with `1/320` retained as guard-only evidence.
3. Completed: fresh F1 produced valid `LC-B`; measurement was controllable but
   not faithful after four bounded candidates.
4. Completed: the single generation-1 continuation again produced valid LC-B.
   Advisor accepted both roots and closed the G-active full-scale face.
5. Advisor resolved the two F2 long-block failures as reproducible cumulative
   history shift. Offline probe bracketing preregistered a single candidate.
6. Completed: the 7-capture short endpoint returned S-D because full-scale base
   repeatability failed while the Ray bracket passed.
7. Completed: scale-3072 stability-first returned `R-UNSTABLE` with Ray bracket
   pass and one early strip observation separated from the later compatible pair.
8. Execute the optional 5-capture scale-2048 stability-first diagnostic. Faithful
   proceeds to H120/S50; unresolved/nonfaithful returns to Advisor.

Persistent locks remain unchanged: no cross-experiment absolute synthesis,
B pre/post, solver sentinel, 13-node grid, boundary, Gate-6, P8 or LUT install
before their active GUIDE branch unlocks them.

PLAN-FULL is short roadmap context, not a section graph or runtime authority.
