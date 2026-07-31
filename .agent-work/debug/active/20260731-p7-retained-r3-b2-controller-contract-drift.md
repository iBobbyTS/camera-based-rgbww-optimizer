# P7 retained-R3 B2 controller contract drift

## Confirmed observations

- Real B2 failed before retained reads because its outer controller required physical fields inside accepted C1 logical linkage records.
- The first correction compared physical mode integer `384` with accepted logical JSON string `"0600"` and ran semantic work before evidence-root acquisition.
- The next correction copied the prior activation HEAD into the current activation tuple and failed before root/C1 reads.
- The following package passed activation and 20 cases but omitted `root=DirectoryIdentity` from all four C1 reads; its sealed PASS evidence is rejected because live source-root/direct-child provenance was unbound.
- The current source-root correction failed pre-root after six Git calls because it uses nonexistent `GitLedger.returncode` at controller lines 172 and 180.
- The committed owner defines `GitLedger.exit_code`; `run_read_only_git` returns that dataclass. The current controller source is bytes `23629`, SHA-256 `0fbda54d91a6941782ea0470100ab55ca66811ca6e31a3463523be5ff0bd9c93`, mode `0600`, device `16777240`, inode `2218110`.
- No current-package source root, C1, retained, manifest, validator, release, network, or device budget was consumed.

## Failed approaches

- Hand-copying owner data shapes and active identity literals into one-off controllers without a source-backed interface check.
- Treating a semantic matrix PASS as sufficient when the physical root ownership call was omitted.
- Correcting one observed field while leaving the generated controller's other owner interfaces unverified.

## Current hypothesis

Root cause is repeated manual controller composition against inferred rather than inspected owner contracts. The next package must freeze the exact `GitLedger` field set from the committed owner (`exit_code`, not `returncode`) and statically reject unknown ledger attributes before dispatch, while preserving the already-required single-source activation, root-first ordering, root-bound reads, logical `"0600"`, matrix, and sealed admission lifecycle.

## Next diagnostic and acceptance surface

- Planner must independently compare every controller attribute access on accepted owner return types against current committed dataclass fields before authorizing dispatch.
- The corrective matrix must include a pre-dispatch negative case for unknown `GitLedger` attributes and a positive case proving all six ledgers use `exit_code == 0` with empty stderr.
- The old controller/source/root remain immutable and must not be rerun or repaired.
- Success still does not authorize retained reads, real B2, manifest, validator, eligibility, release, network, or device work.
