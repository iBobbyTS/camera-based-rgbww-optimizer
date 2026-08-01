# REF-P7-25 retained-R3 minimal EOF seal / global-index failure review

**Planner decision:** `REJECTED_HISTORICAL_OFFSET_GATE_GLOBAL_SEARCH_ZERO_WRITE`

**Reviewed activation:** `fa51dd0e9bc92671b78c3d964eb4371594015791`

**Activation parent:** `5e7e91e35f7c72d460c0aa5c6852847cb19372ef`

**Evidence child:** none. The failed attempt created no evidence commit and left the
worktree clean.

## Reviewed scope and frozen identities

The activation topology passed with exact parent, subject
`chore(plan): isolate physical EOF failure seal`, and ordered paths:

1. `.agent-work/FULL_PLAN_REFERENCE.md`
2. `.agent-work/PLAN.md`
3. `.agent-work/PLANS/20260801-1649-p7-retained-r3-raw-pipeline-repeat-non-eof-review.md`

The activation PLAN is `11861` bytes / SHA-256
`d45cc43b290f0c6d67ddb295d0f0ea51a43b15398dec998195a44edf86e72411`.
The activation FULL is `467143` bytes / SHA-256
`b78386562f39712c4029cc80cec2b25332d80395ec9e3f18e82d5447aceeac19`.
The activation archive is `5084` bytes / SHA-256
`117465da0e1382fce2a22934909c1506bbf9dffbc4b2179526d9a6d94ce5d4fe`.

The activation ER Git object and worktree ER matched exactly at `1559501` bytes /
SHA-256 `7b771a53aec9b06588398cfa536a8829979759ffc26b73966a01583f5b8ed69b`.
The historical rejected record begins at exact byte offset `1546782`. The true
physical-EOF anchor begins at exact byte offset `1555430`, is exactly `4071` bytes,
has SHA-256 `b91a59124220413e1f6037fb8429af934fdf1b53ebd048ab27141c42bd0bf62e`,
and ends with one LF.

## Failure and effect accounting

The controller correctly passed activation topology and ER identity. It then used
a global `String#index` lookup for the historical heading. Because that heading text
also occurs earlier in ER, the lookup returned the earlier duplicate rather than the
frozen record at byte offset `1546782`; the controller stopped at the historical
offset gate.

This is a controller addressing error, not ER drift and not evidence about the
report, seal, matrix, synthetic attribution, production owner, lineage, eligibility,
release, or retained R3. There was no tail freeze, no suffix extraction, no rendered
patch, no `apply_patch`, and no write of any kind. Retry and fallback were `0`.
FULL, PLAN, archives, ER, code, tests, skill, docs, GUIDE, artifacts, network, devices,
camera, Ray120c, strip, cleanup, formal execution, validator, and release operations
were unchanged.

## Decision

Reject the execution because it did not reach the only authorized ER append. The
minimal EOF failure is not yet durably sealed at physical EOF. Preserve the complete
ER baseline verbatim and do not accept the earlier non-EOF record or this zero-write
attempt as closure.

## Exact successor branch

Issue one bounded correction package. It must prohibit every global
find/index/search operation. After exact activation and ER identity gates, it must
compare only:

- `er_bytes[1546782:1546782 + len(HISTORICAL_HEADING_BYTES)]` against the exact
  frozen historical heading bytes; and
- `er_bytes[1555430:1555430 + 4071]` against the exact frozen complete-tail bytes,
  including SHA-256
  `b91a59124220413e1f6037fb8429af934fdf1b53ebd048ab27141c42bd0bf62e`.

Both exact byte comparisons must use a constant-time equality primitive such as
`hmac.compare_digest`; the historical check must not search for occurrence count or
position. The complete `4071`-byte tail is the sole `apply_patch` context, and the
new bounded supersession is appended only after its final line at physical EOF.
`apply_patch` is the only write and final operation. Retry/fallback remain `0`.

The successor remains pure offline provenance repair. Production-owner and lineage
conclusions remain `false`; eligibility and release-consumable remain `false`; retained
R3 remains `RETAINED_UNVALIDATED_UNCONSUMED`.

## Residual risk and validation quality

Validation quality is sufficient to classify this attempt because activation and
whole-ER identities passed before the deterministic addressing failure, and the
failure happened before any write-capable phase. The remaining risk is another
ambiguous context selection; the successor removes that ambiguity by using frozen
byte slices and the entire exact EOF tail as the patch context.

**Planner stop:** successor awaits Orchestrator activation; no report/seal/matrix or
later retained-R3 route is unlocked.
