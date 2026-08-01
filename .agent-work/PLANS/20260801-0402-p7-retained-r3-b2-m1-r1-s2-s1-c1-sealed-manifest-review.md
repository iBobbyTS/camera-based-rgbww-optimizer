# REF-P7-25-R2-B2-M1-R1-S2-S1-C1 review / sealed subordinate real-input manifest

**Planner review date:** 2026-08-01

**Reviewed contract:**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-M1-R1-S2-S1-C1-FRESH-REAL-INPUT-EXACT-MARKDOWN-DELIMITER-V1`

**Evidence commit:** `3b9e60441062714115d9688e636891d591f3a6ef`

**Decision:** `ACCEPTED_COMPLETE_SEALED_SUBORDINATE_PROVENANCE_NOT_RETAINED_ELIGIBLE`

**Next branch:** `REF-P7-25-R2-B3`

## Reviewed scope

S2-S1-C1 authorized one fresh, offline real-input manifest-only integration after activation
`e939b639f40e3dee3d2199110ea2ae1d5e8108a4`. It could read only the frozen C1 four-file
root and retained-R3 three-file root, use the accepted P3/M1/P5 owners once, create one
activation-derived source plus one five-artifact output root, perform a pre-append terminal
audit, and append one physical-EOF handoff as its last side effect.

It explicitly prohibited C1 semantic/linkage selectors, retained canonical re-encoding,
schema/scientific interpretation, the canonical lineage validator, retained release audit,
eligibility emission, release work, network, environment, credentials, devices, camera,
Ray, strip, cleanup, capture, FORMAL, public analyzer, TD-C, sentinel, P8, firmware and
deployment.

## Independent evidence review

The activation commit has exact parent
`30a5e97897b734499a6ec4a61cbb79f2d814b895`, exact subject
`chore(plan): activate exact-delimiter real input successor`, and exact changed paths:

- `.agent-work/FULL_PLAN_REFERENCE.md`;
- `.agent-work/PLAN.md`;
- `.agent-work/PLANS/20260801-0341-p7-retained-r3-b2-m1-r1-s2-s1-delimiter-review.md`.

The evidence commit is the direct child of that activation and changes only
`.agent-work/EXECUTION_RESULT.md`. The committed/current active PLAN is 20,657 bytes with
SHA-256 `094e61f8d0e2fc6b8d6c28b2ff3c6fefd7f39366c5004864decf4c92d8db8353`.
The resulting ER is 1,287,476 bytes with SHA-256
`42057a760eabee310927b438f62ae2b8d84975c75c74bfa8bcf5e9b71eff069a`.

The Orchestrator independently established that the prior ER is the exact 1,266,264-byte
prefix with SHA-256 `ddd34c672984309c954d19e5028327ce936f7f0182283121000a22cbb8d3763a`,
the physical-EOF suffix is 21,212 bytes with SHA-256
`ea998ba6c72aecf9e1038fe02412e35d41e12250501770867936af68532053ba`, and the appended
payload is strict duplicate-free canonical JSON. Planner inspection confirms the new heading
and payload are the physical final block.

All actual counters equal their frozen success budgets, including repository decode/extraction
2/2, absence checks 2, pre-root/file reads 2/7, C1 canonical decodes 4, retained strict decodes
3, builder/runtime/process 1/1/1, Git ledgers 56, controller input root/file reads 7/7,
output writes/reloads 5/5, post-audit source/root/input/output reads 1/3/7/5, process scan 1,
append/apply-patch 1/1, and retry/fallback/post-append operations 0/0/0.

The seven pre-input and seven post-input identities are exactly equal in path, root, device,
inode, mode, bytes and SHA-256. The source remains the same 0600 inode, 26,644 bytes, SHA-256
`0889b150daae9ba6313aea9f6502e09bcf838eb70312a3595c056edb0be1b09b`.
The fresh output root is 0700 and contains exactly five regular 0600 canonical JSON files:

- `execution-result-admission.json`: 65 bytes,
  `c43d97963373db7d61066de6ebb7e16e6d915281f1f30861f86e1bd6404d87e9`;
- `retained-r3-audit-provenance-manifest-v2.json`: 4,651 bytes,
  `c3ac3bc712965e39453b32e8cde15ebc7e53dcc7e1a99f1ecb38177f65cadfaf`;
- `retained-r3-audit-provenance-manifest-v2.sha256.json`: 148 bytes,
  `3a5f5a4b2c7fa203cad63a90d36a0b43a0e519534cc7c202eeb9b56fcddbfbbc`;
- `terminal-evidence.json`: 52 bytes,
  `b438e5c7cac0ef434205c748a003596d740c155f8b0ff3fa06df5a16f4a17893`;
- `terminal-evidence.sha256.json`: 123 bytes,
  `d17c4836355406fba95bb2d564692a32ff4b94423ae69e4de8cfe4b542572d75`.

Independent strict decoding and canonical re-encoding of those five fresh outputs succeeds.
Both seal files bind the exact target name, byte count and SHA-256. Admission is exact
`{"admitted":true,"eligibility":false,"release_consumable":false}`; terminal and manifest
status are exact `sealed_subordinate_provenance_evidence`.

The accepted M1 commit is `0f4c09e1b2b2afbf627f6f36d57a1a65847ab4a8`, parent
`f2b38c530a6cbac5c29d761036eb3cd2a159f3b9`, subject
`fix(p7): align real manifest Git ledgers`. Its manifest-bound source/test identities and
authoritative two-path patch identity remain the already accepted M1 owner. No new production
or test path changed in this execution.

## Planner decision

Accept S2-S1-C1 as complete. It proves exactly one immutable, sealed subordinate provenance
manifest was produced from the frozen real inputs with stable physical identities and a valid
terminal/admission lifecycle. It does **not** validate retained R3, run the canonical lineage
validator, emit eligibility, qualify or consume a release, or authorize device/FORMAL work.

The retained state remains exactly `RETAINED_UNVALIDATED_UNCONSUMED`. The existing canonical
lineage validator remains the sole eligibility owner. The next package is the already defined
B3 offline sequence: independent manifest self-check, one postcommit focused suite, one durable
full suite, and one fresh synthetic terminal/replay. B3 itself must still emit no eligibility
and must not perform the B4 real retained audit.

## Residual risks and stop

- Manifest facts have not yet received the B3 independent Git/input recomputation pass.
- Postcommit focused/full tests and the B3 fresh synthetic replay have not yet run.
- Original retained R3 remains unvalidated and unconsumed; B4 remains locked until B3 acceptance.
- Release consumption, network/device work, FORMAL-R6, strip, TD-C, sentinel and P8 remain locked.

**Planner stop:** archive complete; activate only `REF-P7-25-R2-B3` after Orchestrator updates
the FULL reference and creates its activation commit.
