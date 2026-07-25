# P7 TD-B sidecar atomicity C2

## Resolved Findings

- `REV-C1-001`: expected sidecar path/stat/read failures are normalized into
  structured association failures after the returned CR3 has been counted and
  persisted exactly once in the physical ledger.
- `REV-C1-002`: remote-v2 validation now records verified capture/request IDs
  before adapter timing metadata/evidence comparison, so later drift remains
  fail-closed without losing the verified remote owner.

## Root Cause

`_SidecarAssociationError.evidence` was not a complete atomic snapshot. Expected
filesystem failures were not normalized into that exception, and verified remote
IDs were added only on the success return path instead of immediately after
remote-v2 validation.

## Fix Boundary

- Kept the existing sidecar helper and physical-return ledger owner.
- Read the returned CR3 once and passed the retained bytes into sidecar validation.
- Converted expected sidecar inspection/read failures into structured association
  errors carrying all evidence available at that point.
- Added verified remote IDs to evidence before comparing adapter copies.
- Extended the old R1 audit to hash every retained regular file before and after
  replay, including CR3, sidecar and patch statistics.

## Verification

- Deterministic post-stat `read_bytes()` `OSError`, removal and replacement.
- Valid sidecar plus adapter timing metadata drift.
- Valid sidecar plus adapter timing evidence drift.
- Existing eight-case sidecar matrix and real-order feature rejection.
- Old R1 read-only replay with the full retained file set unchanged.
- Focused `150/150`, full suite `549/549`, compileall, wrapper syntax,
  `git diff --check` and CodeGraph sync passed.

Evidence:

`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-r1-c2-offline/20260723-202736`

Implementation commit: `e5cd0792c308c444064fd621622f0dead1140a8b`.

Validation summary SHA-256:
`bec837bc307f1590b9794e858346303d0ef2bf6e20ab246baaf3b7a7a361ee27`.

No device, network, `.env`, camera, light, `all_off`, new CR3, public analyzer,
lineage, E2, threshold, shutter, budget or scientific-strategy change occurred.
