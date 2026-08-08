# Ray R6 exposure-gate revalidation

## Confirmed observations

- The retained Ray R6 root contains 16 accepted capture rows and 16 physical returns.
- The fixed exposure-setting gate accepts all 16 recorded Canon values.
- Python and shell cleanup artifacts pass; the original `run.json`, `failure.json`,
  and `wrapper-result.json` remain byte-preserved failed evidence.
- The old post-capture validator raised before writing `commands-audit.json` and
  before the runner could finish successfully.
- A post-fix `quality.json` was generated once and reports 16/16 pass.
- The default analyzer correctly refuses the failed run and must remain fail closed.
- The first real analyzer invocation exposed a second projection mismatch: the
  direct spec says `f/4`, while the remote backend and all 16 retained captures
  say `implicit auto`. The CR3 has manual exposure but no electronic lens/FNumber,
  and the frozen P6 reference run also uses ISO 100 plus `implicit auto`.
- Explicit revalidation now passes and the analyzer reaches a deterministic
  Ray R6 scientific result. The first analysis reported `history fail`, but it
  omitted the six A-anchor pair diagnostics and the D/B/C trend, dominance and
  direction fields required by GUIDE 4 sections 8.1-8.2.
- A first reporting implementation incorrectly reused the multi-group
  repeatability audit for each single R6 state and failed because D/B/C each
  contain one four-point chronology, not two independent repeatability groups.
  The corrected implementation uses the frozen per-capture same-state variance
  with the existing `4.0` trend and `0.5` dominance definitions; it does not
  synthesize an extra group or change the operational history gate.

## Root-cause hypothesis

The only retained execution failure is the superseded exact-float exposure
comparison. A narrow opt-in revalidation can safely reconstruct the missing
derived command audit and prove the current validator result without changing
the original process outcome or creating another acquisition root. The analyzer
must also distinguish the spec's inaccurate `f/4` projection from the uniform
runtime `implicit auto` setting shared by P6 and R6; it must not relax any other
camera-setting mismatch.

## Next diagnostic and verification

1. Add a behavior test that reconstructs this exact failure from a complete fake
   direct Ray R6 run.
2. Prove default analysis rejects it, wrong exposure and failed cleanup reject
   revalidation, and exact exposure-only failure passes.
3. Preserve original artifact hashes and the accepted revalidation record.
4. Add report-only diagnostics derived from the existing frozen covariance and
   chronology thresholds, without changing the pass/fail decision.
5. Rerun only the deterministic analyzer on the retained root.

No device or acquisition action belongs to this debugging boundary.

## Resolution

- Focused validation: 28 tests passed; compileall and `git diff --check` passed.
- Same-root explicit revalidation remained byte-preserving and passed.
- Final deterministic analyzer SHA-256:
  `7cb6ef267496342ae1145bb83295510438ea9bf45946187168ffb21e8b0e267b`.
- Scientific result: `history_dependent_at_operational_dwell_600` because
  `A0` versus `A_after_C` failed frozen same-state coverage.
- This is a GUIDE-defined valid scientific negative, not an engineering error.
  Strip, combined and TD-C remain locked pending Advisor guidance.
