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
- Repo-owned P4-C1 transport classification was implemented in `0ec12f2...` with exact two paths and recorded 20 targeted / 76 focused / 761 full tests passing. Planner could not accept the package because activation `48adfd6...` has actual subject `chore(plan): activate p4 transport domain correction`, while the frozen PLAN and ER asserted `chore(plan): activate p4 transport domain owner correction`. The implementation remains a validation candidate, but provenance closure is required before synthetic integration.
- Validation-only successor C1-C1-C1 was accepted. Evidence commit `baa14d1...` preserves the old ER prefix, truthfully supersedes only the false activation-subject/pass assertion, and leaves the original P4-C1 contract rejected. The repo-owned implementation can now be consumed by a fresh synthetic integration qualification without rewriting history.
- The controller path was subsequently decomposed into accepted single owners: P5 repo-owned runtime `37f7d002...`, P6 deterministic builder `48b3979...`, and P7 runnable template `864f08cc...`. P7 validation passed exact backtick machine-row decoding, targeted `11/11`, focused `93/93`, compileall, full `778/778`, and final-clean with one terminal-only ER append. Planner accepted it as `ACCEPTED_COMPLETE_REPO_OWNED_RUNNABLE_DOMAIN_TEMPLATE_OWNER`.
- Orchestrator registered new successor `REF-P7-25-R2-B2-P7-I1` for one fresh pure-offline synthetic integration. It must compose the accepted P5/P6/P7 owners and must not revive the disposable controller, second analyzer/classifier, serializer, or lifecycle paths documented below.

## Failed approaches

- Hand-copying owner data shapes and active identity literals into one-off controllers without a source-backed interface check.
- Treating a semantic matrix PASS as sufficient when the physical root ownership call was omitted.
- Correcting one observed field while leaving the generated controller's other owner interfaces unverified.
- Mixing negative-test fixture text into the same AST/text domain used to certify dispatched runtime code.
- Passing live owner objects between lifecycle callbacks through a generic mutable state container instead of keeping direct-bound names and storing only plain serialized projections.
- Retaining temporary tuples/lists of live owner objects and generic `projection(identity)` calls after introducing direct/nonlocal bindings; field extraction must be unrolled at each binding, with only the repo-required immutable `RootIdentityChain` composition explicitly allowed.
- Maintaining a second, disposable AST transport classifier outside the accepted repo owner; its undifferentiated live-name set cannot distinguish effect-owned identities from pure in-memory negative-fixture identities.

## Resolution

Repeated failures were caused by copied owner contracts and transient validation harnesses around disposable controller source. The stable correction was architectural but bounded: keep runtime effects, deterministic domain construction, and runnable generated-template semantics in three repository-owned and independently tested owners. Their accepted commits are `37f7d002...`, `48b3979...`, and `864f08cc...`; the final validation evidence is `2e969389...`, and the Planner acceptance archive is `.agent-work/PLANS/20260731-1914-p7-retained-r3-b2-p7-machine-row-validation-acceptance-review.md`.

This debug route is resolved at the owner-contract level. Synthetic integration remains a separately planned qualification and is not evidence that retained R3, the canonical validator, eligibility, release, network, or device work is unlocked.

## Reusable acceptance surface

- A fresh synthetic integration must call the accepted P5/P6/P7 public owners and store only their contract-defined immutable/plain projections; it must not reconstruct their logic in an outer controller.
- Any future source gate must compare runtime attribute access against committed owner dataclasses, while parsing negative fixtures in a separate AST excluded from runtime-occurrence assertions.
- The regression surface must prove a negative `GitLedger.returncode` specimen is rejected, the actual runtime AST has no `returncode`, all six ledgers use `exit_code == 0` with empty stderr, and four root negative cases remain pure in-memory without consuming an extra owner root lstat.
- Old failed controller/source/root paths remain immutable and must not be rerun, repaired, or reused.
- P7-I1 success may qualify only the pure-offline owner composition; it does not itself authorize retained reads, real B2, manifest, validator, eligibility, release, network, or device work.
