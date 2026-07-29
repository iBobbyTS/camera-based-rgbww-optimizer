# REF-P7-25-R2-B1A-C3E6F10 review / nested closure-owner AST hard failure

**Planner review date:** 2026-07-29

**Reviewed contract:**
`P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F10-CLEANUP-TEST-SUCCESSOR-PREREQUISITE-V1`

**Decision:** `rejected_exact_nested_closure_ast_shape`

**Next branch:** `REF-P7-25-R2-B1A-C3E6F11`

## Reviewed scope and evidence

C3E6F10 retained the exact rows/FULL subset, acquisition-first protocol, structured ignore,
exact tracked closure owner and atomic tracked-target materialization. Planner reviewed
PLAN/FULL, `EXECUTION_RESULT.md` section 70, terminal summaries, active debug state and an
independent non-executing AST dump of the frozen owner source.

The package passed PLAN/FULL gates, fresh-root acquisition, four observed-first acquisitions
and comparisons, clone/checkout, exact test-source atomic replacement, one-path diff identities
and two ignored runtime-fixture copies. The fixed same-directory temp lifecycle passed: one
exclusive temp, mode/fsync, same-filesystem proof, one `os.replace`, directory fsync, temp
absent, exact target identity, exact changed path and zero staged paths.

The first failure occurred after exact closure-owner path/mode/blob/bytes/SHA validation. The
controller expected one flat `BinOp(PROJECT_ROOT / "config/white/white-endpoints.json")` and
raised `ValueError: DEFAULT_WHITE_ENDPOINTS structural value differs`.

The frozen tracked source actually has one assignment at line 24 with this exact AST:

```text
BinOp(
  left=BinOp(
    left=BinOp(
      left=Name(id='PROJECT_ROOT'), op=Div(), right=Constant('config')),
    op=Div(), right=Constant('white')),
  op=Div(), right=Constant('white-endpoints.json'))
```

This is the left-associated Python representation of
`PROJECT_ROOT / "config" / "white" / "white-endpoints.json"`. It is not a source/path
identity drift and must not be reduced through evaluation or generic path normalization.

Terminal root:

```text
/Volumes/4T/temp/rgbww-optimizer/
  p7-td-b-retained-r3-option-b-b1a-c3e6f10-offline/
  20260729T204432Z
```

Strict counters: fresh root `1`, retry `0`, first acquisitions/comparisons `4/4` of planned
five, test-source read/materialization `1/1`, runtime reads/copies `2/2`, closure read/copy
`1/0`, canonical read `0`. Pre/post/full tests, stage, external commit, canonical validator,
successor manifest and verifier were zero. Candidate, production, shared Git, retained R3,
audit, eligibility, consumer, release, network, DNS, `.env`, credentials, devices, camera,
Ray, strip, cleanup, capture, analyzer, FORMAL, firmware and deployment were zero.

Evidence hashes:

- `validation-summary.json`:
  `71d1d0008817a329f1cc37b05197bc258133b9cab88c64740a5333298ec2830c`;
- `terminal-summary.json`:
  `59d19b4b2d9ab74a1ad0411e95ce10dc637a91b96428494b5db42475e3f40db8`;
- execution handoff file:
  `176247ca2ce9005b833b880e55280d55a66a32222c464ca7834557c8df90149e`.

Shared HEAD remains `9303aa22a9bd37e8ec4f23147c78c6bea84b9a2e`; staged paths remain zero.

## Decision

C3E6F10 is rejected solely at the structural AST positive gate. Its atomic replacement and
earlier gates receive historical evidence credit but no reusable budgets. The terminal root
must remain read-only and must not be resumed, repaired or reused.

The one-path child, old-validator expected rejection and immutable/unconsumable successor
manifest topology remains unchanged. Production validator binding remains a later package.

## Exact next branch

C3E6F11 starts from a new fixed container and one fresh root. Its only controller correction
is an exact non-executing structural match of the nested AST above. It must prove:

- exactly one `DEFAULT_WHITE_ENDPOINTS` assignment;
- exactly three left-associated `ast.BinOp` nodes;
- every operator exactly `ast.Div`;
- root exactly `ast.Name(id="PROJECT_ROOT", ctx=ast.Load)`;
- right constants in traversal order exactly
  `("config", "white", "white-endpoints.json")`;
- every segment is a string constant and there are no additional nodes/segments.

It must reject missing, reordered, additional or non-string segments; alternate root,
operator or association; calls, attributes, subscripts, interpolation, concatenation,
duplicate assignments or additional matching owner. It may use AST structure only and must
not call `literal_eval`, compile/execute the expression, join/normalize a generic path, or
accept equivalent alternate syntax.

Every other C3E6F10 rule remains unchanged, including the proven fixed-temp atomic replacement,
exact rows/FULL subset, structured ignore, exact source owner, five fresh acquisitions,
one-path child, expected canonical rejection, immutable unconsumable manifest and all zero
locks. C3E6F10 must not be retried. No Advisor or Human authorization is required.

## Residual risks

- Canonical acquisition, pre/post tests, child commit and successor manifest remain unexecuted.
- Full clean-room discovery and production validator binding remain incomplete.
- Original retained R3 remains `RETAINED_UNVALIDATED_UNCONSUMED`; rollback remains
  `32b9e670ff3bbea0cd1505528c2ca87c2935446c`.

**Planner stop:** archive complete. Activate only C3E6F11 after Orchestrator synchronizes its
required FULL machine state.
