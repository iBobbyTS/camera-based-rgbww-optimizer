# P7 retained-R3 B2 controller contract drift

## Confirmed observations

- Real B2 failed before retained reads because its outer controller required physical fields inside accepted C1 logical linkage records.
- The first correction compared physical mode integer `384` with accepted logical JSON string `"0600"` and ran semantic work before evidence-root acquisition.
- The next correction copied the prior activation HEAD into the current activation tuple and failed before root/C1 reads.
- The following package passed activation and 20 cases but omitted `root=DirectoryIdentity` from all four C1 reads; its sealed PASS evidence is rejected because live source-root/direct-child provenance was unbound.
- The current source-root correction failed pre-root after six Git calls because it uses nonexistent `GitLedger.returncode` at controller lines 172 and 180.
- The committed owner defines `GitLedger.exit_code`; `run_read_only_git` returns that dataclass. The current controller source is bytes `23629`, SHA-256 `0fbda54d91a6941782ea0470100ab55ca66811ca6e31a3463523be5ff0bd9c93`, mode `0600`, device `16777240`, inode `2218110`.
- No current-package source root, C1, retained, manifest, validator, release, network, or device budget was consumed.
- The owner-API successor then failed its own pre-dispatch gate with `RuntimeError:returncode_occurrence`: the gate correctly parsed an isolated negative specimen containing `ledger.returncode`, but later counted the specimen's source text as if it were dispatched runtime attribute usage. Git/root/C1 remained zero. Controller bytes/SHA are `21024`/`703e813f09c543a654c64423fd09c6c527211b87bb3045c8aa7ed1e1969d2078`.

## Failed approaches

- Hand-copying owner data shapes and active identity literals into one-off controllers without a source-backed interface check.
- Treating a semantic matrix PASS as sufficient when the physical root ownership call was omitted.
- Correcting one observed field while leaving the generated controller's other owner interfaces unverified.
- Mixing negative-test fixture text into the same AST/text domain used to certify dispatched runtime code.

## Current hypothesis

Root cause is now broader than one field: repeated one-off controllers combine runtime logic, static conformance, negative fixtures, evidence serialization, and lifecycle orchestration in one source domain. Fixing another local predicate would preserve the fragile state owner. The next engineering step should separate and test the reusable controller-conformance/qualification composition in repository-owned code, or otherwise establish disjoint runtime and negative-fixture AST domains before any further real external dispatch.

## Next diagnostic and acceptance surface

- Planner must reassess ownership and should not authorize another hand-written external-controller retry that merely adjusts the `returncode` counter.
- Any successor must independently compare every runtime controller attribute access on accepted owner return types against current committed dataclass fields, while parsing negative fixtures in a separate AST that is excluded from runtime-occurrence assertions.
- The regression surface must prove a negative `GitLedger.returncode` specimen is rejected, the actual runtime AST has no `returncode`, all six ledgers use `exit_code == 0` with empty stderr, and four root negative cases remain pure in-memory without consuming an extra owner root lstat.
- The old controller/source/root remain immutable and must not be rerun or repaired.
- Success still does not authorize retained reads, real B2, manifest, validator, eligibility, release, network, or device work.
