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

## Root-cause hypothesis

The only retained execution failure is the superseded exact-float exposure
comparison. A narrow opt-in revalidation can safely reconstruct the missing
derived command audit and prove the current validator result without changing
the original process outcome or creating another acquisition root.

## Next diagnostic and verification

1. Add a behavior test that reconstructs this exact failure from a complete fake
   direct Ray R6 run.
2. Prove default analysis rejects it, wrong exposure and failed cleanup reject
   revalidation, and exact exposure-only failure passes.
3. Preserve original artifact hashes, generate a small revalidation record, then
   run the analyzer once with explicit opt-in.

No device or acquisition action belongs to this debugging boundary.
