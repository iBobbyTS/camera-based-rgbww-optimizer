# F19-C4 exact field-owner gate correction — Planner review archive

**Review time:** `2026-07-29T22:18:42-0600`

**Reviewed reference task:** `REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-4`

**Reviewed contract:** `P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F19-CORRECTIVE-4-FIELD-OWNER`

**Decision:** `REJECTED_EXECUTION_SIDE_EXPECTED_DIGEST_TRANSCRIPTION_ERROR`

## Reviewed scope and method

C4 was authorized to perform one helper-owned PLAN parse and one helper-owned FULL parse, verify the exact 12-entry
field-owner ledger, verify the immutable C2 five-artifact identity, then make only the dedicated-test lexical-local
`run` `STORE_FAST`/`LOAD_FAST` correction and run one fresh fail-fast validation chain. Controller execution,
candidate/retained-R3/release access, validator/eligibility work, network and device work remained locked.

The Planner independently read the committed C4 PLAN/FULL state, the single C4 execution-result append, and only the
allowed C2 root. It recalculated path type, symlink state, mode, bytes and SHA-256 for all five C2 artifacts, parsed the
C2 activation/pre-validation/terminal JSON, and compared the current identities with both the C2 terminal manifest
and the C2 execution-result artifact map. The forbidden C3 evidence root and candidate/R3/release paths were not
accessed.

## Evidence and independent findings

- C4 activation lineage passed: child `3c0f5999717e657b28e15c9ef1e59bdc16cb4e48`, parent
  `a647256cd49e477c73cf878101d5d6733d851dde`, changed path exactly `.agent-work/PLAN.md`.
- Helper calls were exactly PLAN `1` and FULL `1`; helper evidence passed; exact field ledger was `12/12` pass.
- C4 stopped before edits: helper edits `0`, dedicated-test edits `0`, controller edits/calls `0`, fresh C4 root/artifacts
  `0`, every validation command `0`, retry/fallback `0`.
- Controller remained SHA-256 `746fd13056c326489b48ca555b21618b65c8a78f198d035e18c02f68af689726`;
  dedicated test remained SHA-256 `e9b51d5d83319e68d29da68a2a023ef6feb248bf6c4b3ce8d776a70e63b957e6`.
- Retained R3 stayed `RETAINED_UNVALIDATED_UNCONSUMED`; candidate/R3/release/validator/eligibility/network/device
  counters were all `0`.

The C2 root is mode `0700`; every artifact is a regular non-symlink mode `0600`. Its exact current and terminal-bound
identities are:

| Artifact | Bytes | SHA-256 | Identity source |
| --- | ---: | --- | --- |
| `activation-gate.json` | 3243 | `cd52abf2bcf4dd7a59052771e4fa342f69dc21dd59b7697ad5e5b89d9b53ce5c` | C2 ER artifact map plus current bytes |
| `pre-validation.json` | 670 | `16ec941cd276846268d930c50e31492ea3c5198e0ed473953c5b1304f6a9d9f2` | C2 terminal manifest and ER map |
| `compileall.log` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | C2 terminal manifest, validation record and ER map |
| `targeted_unittest.log` | 3108 | `60e72a1e1bddd8afa34420ed2f4d56db3d7a769879f1a75e8025208360f0bc48` | C2 terminal manifest, validation record and ER map |
| `terminal-evidence.json` | 2519 | `41294a0cf35ace7dcc3389d0323015ebaacb42a3bbf0753c3295412be003d8f6` | C2 ER artifact map plus current bytes |

All current identities match the C2 terminal state. File mtimes are at the C2 terminal window; there is no byte,
size, mode, path-set or manifest contradiction indicating post-terminal drift.

## Root cause and verdict

The committed C4 PLAN froze the correct empty-file digest:
`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.
The C4 execution-result failure detail instead reports that it compared against
`e3b0c44298fc1c149afbf4d8996fb92427ae41e4649b934ca495991b7852b855`, which substitutes `d` for the
correct `c` in the `f4c8996f` segment. Therefore the reported mismatch cannot have come from the parsed PLAN identity value. It is an
execution-side shadow/transcription constant error. The C2 evidence must not be repaired, rewritten, regenerated or
deleted, and C4 cannot be accepted as completing its authorized correction.

## Next branch

Propose `REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-5`: one minimal exact C2 evidence-identity binding correction. Its
pre-edit gate must obtain every expected C2 artifact digest and byte count from one parsed PLAN identity map, compare
the actual file to that parsed value, and forbid any second/shadow expected digest literal or alias. It must first
reconfirm the already-proven helper `1/1`, field ledger `12/12`, five exact C2 identities, zero C3 access, unchanged
controller/test and all zero locks. Only after that gate may it perform the same one-file dedicated-test correction
and one fresh C5 validation chain.

This is an engineering/provenance correction. Advisor guidance and Human authorization are not required. Orchestrator
must align `FULL_PLAN_REFERENCE.md`, commit the reviewed state, and obtain a fresh Planner activation before any C5
Executer dispatch.

## Residual risks and stop point

- The C4 execution source is not retained as an artifact, so the precise shadow-literal location cannot be audited;
  C5 closes this by making the parsed PLAN map the sole expected-value owner and recording actual/expected values.
- C4 made no scientific or device progress. B2, candidate/retained R3, release consumption, validator/eligibility,
  FORMAL-R6, strip, TD-C, sentinel and P8 remain locked.
- Planner stop: `F19_CORRECTIVE_4_REVIEWED_WAITING_ORCHESTRATOR_C5_ALIGNMENT`.
