# REF-P7-25-R2-B1A-C3E6F8 review / closure-owner path-resolution hard failure

**Planner review date:** 2026-07-29

**Reviewed contract:**
`P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F8-CLEANUP-TEST-SUCCESSOR-PREREQUISITE-V1`

**Decision:** `rejected_exact_closure_owner_path_resolution`

**Next branch:** `REF-P7-25-R2-B1A-C3E6F9`

## Reviewed scope and evidence

C3E6F8 retained the exact machine-row parser, required FULL subset, structured ignore
diagnostic, structural closure AST predicate, five-read acquisition-first protocol and
accepted non-self-referential prerequisite topology. Planner reviewed PLAN/FULL,
`EXECUTION_RESULT.md` section 69, terminal evidence, CodeGraph and the active debug record.

The package passed the exact-row positive and eight negatives, FULL subset, fresh root and
no-hardlink clone. All five first-acquisition observed records and comparisons passed. The
exact test path was materialized, both runtime fixtures were copied, structured ignore gates
passed and both frozen diff representations matched.

The first failure occurred before structural AST validation because the temporary controller
opened the nonexistent clean-room path:

```text
src/camera_based_rgbww_optimizer/measurement/measure_raw_observer_validation.py
```

It raised `FileNotFoundError` and did not search for or substitute another module. This is a
controller owner-path defect, not source/fixture/diff/canonical-manifest drift, production
behavior, provenance acceptance or scientific failure.

CodeGraph and independent Git/file identity checks establish the sole tracked owner as:

```text
src/camera_based_rgbww_optimizer/optimization/measure_raw_observer_validation.py
```

At checkpoint `9303aa22a9bd37e8ec4f23147c78c6bea84b9a2e`, this path is a regular tracked
mode-`100644` blob with:

- bytes: `55402`;
- SHA-256: `219a9d37fc8dfc34e8e201f55e0dac8aa98156ed7a58f260eba4d88e37ea0df9`;
- Git blob OID: `8b61a854cb6040130a42640cf2b40d70ddd9f098`;
- `DEFAULT_WHITE_ENDPOINTS` owner: line 24 in the authoritative source.

Strict terminal counters: fresh root `1`, retry `0`, pre-root reads `0`, observed records and
comparisons `5/5`, test-source read/materialization `1/1`, runtime reads/copies `2/2`, closure
read/copy `1/0`, canonical first acquisition `1`. Tests, stage, external commit, canonical
validator, successor manifest and verifier were zero. Candidate, production, shared Git,
retained R3, audit, eligibility, consumer, release, network, DNS, `.env`, credentials,
devices, camera, Ray, strip, cleanup, capture, analyzer, FORMAL, firmware and deployment were
zero.

Evidence hashes:

- `validation-summary.json`:
  `c876c6e1ec742418f5cc15992b4b96febce0aebce92980313b92f27234577730`;
- `terminal-summary.json`:
  `88e844b056d930e13b8898f3d6836e589978a318be1fe7d684c450fa8b24fc19`;
- `terminal-seal.json`:
  `2301bd75e10f2dc5ed5b84a18e51ec3e30d392d8a515a5c85887b964a1de2f34`;
- execution handoff file:
  `3351dfd175f8f8891d23e8a492b48056c7f739b5df264b35f3ed6a5bfd6cb795`.

Shared HEAD remains the frozen checkpoint and staged paths remain zero.

## Decision

C3E6F8 is rejected at the closure-owner path gate. Its completed acquisitions are historical
terminal evidence only; none of their budgets transfer. The root must remain read-only and
must not be resumed, repaired or reused.

The one-path child, old-validator expected rejection and immutable/unconsumable successor
manifest topology remains unchanged. Production validator binding remains a later package.

## Exact next branch

C3E6F9 starts from one new fixed container and fresh root. Its only controller correction is
to freeze and validate the exact tracked owner above before running the unchanged structural
AST predicate. It must prove from the frozen checkpoint and clean room:

- exact relative path, regular/non-symlink status and tracked mode `100644`;
- exact bytes, SHA-256 and Git blob OID;
- clean-room file identity equals the checkpoint blob before AST parsing.

No alternate module, directory search, basename search, fallback, working-tree-only identity
or inferred owner is permitted. Missing or mismatched exact owner hard-fails before AST
parsing. The line number is observed source location, not an identity gate; the AST assignment
and exact expression shape remain the semantic owner.

Every other C3E6F8 rule remains unchanged: exact rows, FULL subset, structured ignore parser,
fresh-root-first five acquisitions, structural AST predicate, one-path child, canonical
expected rejection, immutable unconsumable manifest and all zero locks. C3E6F8 must not be
retried. No Advisor or Human authorization is required.

## Residual risks

- The AST gate, tests, child commit and successor manifest still have not completed.
- Full clean-room discovery and production validator binding remain incomplete.
- Original retained R3 remains `RETAINED_UNVALIDATED_UNCONSUMED`; rollback remains
  `32b9e670ff3bbea0cd1505528c2ca87c2935446c`.

**Planner stop:** archive complete. Activate only C3E6F9 after Orchestrator synchronizes its
required FULL machine state.
