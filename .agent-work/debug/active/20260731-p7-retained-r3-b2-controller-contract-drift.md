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
- Repo-owned P4 commit `83bb193...` and final-source full `755/755` are accepted. Its first synthetic integration correctly rejected the runtime source pre-effect with `owner_alias_escape` because direct owner results were stored in a mutable `state` container. Git/root/inputs remained zero. The immutable source is bytes `20586`, SHA-256 `8c4cb131ed97bc38f5ff72947000d3b7932574759483b4172cd9fbfd992ea904`.
- The alias-safe successor passed the accepted analyzer with 18 bound results, then its additional transport gate rejected 16 live-object container/call occurrences before effects. The source still grouped Git ledgers in a tuple for checking, passed live objects to projection helpers, collected artifacts in a list, and grouped input identities. Controller bytes/SHA are `33510`/`de2038f4d520febb0984e6b8ff6a73c293a46503ee1d6f07118036343aff2f29`; Git/root/inputs remained zero.
- The field-only successor passed the accepted analyzer with 18 bindings, then its one-off transport gate rejected the required pure in-memory case-11 negative `FileIdentity(root=drift_root)` as `live_owner_transport:drift_root:Call`. Controller bytes/SHA are `32216`/`a9d982f88bc75ef09e029ce4311a46f3e9f59264fed86c98e1bb5fc284122010`; all effects remained zero.

## Failed approaches

- Hand-copying owner data shapes and active identity literals into one-off controllers without a source-backed interface check.
- Treating a semantic matrix PASS as sufficient when the physical root ownership call was omitted.
- Correcting one observed field while leaving the generated controller's other owner interfaces unverified.
- Mixing negative-test fixture text into the same AST/text domain used to certify dispatched runtime code.
- Passing live owner objects between lifecycle callbacks through a generic mutable state container instead of keeping direct-bound names and storing only plain serialized projections.
- Retaining temporary tuples/lists of live owner objects and generic `projection(identity)` calls after introducing direct/nonlocal bindings; field extraction must be unrolled at each binding, with only the repo-required immutable `RootIdentityChain` composition explicitly allowed.
- Maintaining a second, disposable AST transport classifier outside the accepted repo owner; its undifferentiated live-name set cannot distinguish effect-owned identities from pure in-memory negative-fixture identities.

## Current hypothesis

The repo-owned analyzer correctly catches its implemented boundary, but transport-domain classification remains outside it and has now produced two different pre-effect false/over-broad rejections. Another one-off allowlist would preserve duplicated AST ownership. The next step should extend the repo-owned conformance module and dedicated tests with an exact transport report that distinguishes effect-owned live identities, required immutable `RootIdentityChain` composition, and isolated pure in-memory fixture identities; external sources should consume that single owner rather than implement a second classifier.

## Next diagnostic and acceptance surface

- Planner should authorize only a fresh synthetic integration source that uses direct/nonlocal owner bindings and stores plain projections rather than live owner objects.
- Any successor must independently compare every runtime controller attribute access on accepted owner return types against current committed dataclass fields, while parsing negative fixtures in a separate AST that is excluded from runtime-occurrence assertions.
- The regression surface must prove a negative `GitLedger.returncode` specimen is rejected, the actual runtime AST has no `returncode`, all six ledgers use `exit_code == 0` with empty stderr, and four root negative cases remain pure in-memory without consuming an extra owner root lstat.
- The old controller/source/root remain immutable and must not be rerun or repaired.
- Success still does not authorize retained reads, real B2, manifest, validator, eligibility, release, network, or device work.
