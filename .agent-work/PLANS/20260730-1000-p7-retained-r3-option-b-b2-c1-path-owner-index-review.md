# REF-P7-25-R2-B2-C1 path-owner index review

**Reviewed reference task:** `REF-P7-25-R2-B2-C1`

**Reviewed contract:**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-C1-PATH-OWNER-INDEX-V1`

**Planner decision:** `ACCEPTED_EXACT_PATH_OWNER_INDEX_ONLY`

**Planner review date:** `2026-07-30`

## Reviewed scope and implementation method

The active PLAN authorized one pure-offline controller invocation and one
brand-new external evidence root. The package could verify only the three
historically named directory levels through non-following `lstat` and direct
entry enumeration, mechanically resolve the three retained artifact paths,
and durably seal a path-owner index. It prohibited separate artifact `lstat`,
all artifact content access, B2 manifest creation, validators, audit, replay,
eligibility, release, repository implementation changes, tests, network,
devices, and later scientific stages.

The reviewed PLAN was `15007` bytes with SHA-256
`68ff8951ade8fc94c1b3ae185f6e9e4c7f79b906841087fe1db7cd8d2c07bde8`.
The Planner independently read and strict-parsed only the four C1 evidence
JSON files and the active PLAN/EXECUTION_RESULT handoff. It did not open,
read, hash, parse, mmap, copy, or otherwise access any retained-R3 artifact;
it did not invoke the controller, validator, audit helper, tests, Git mutation,
network, or devices.

## Authoritative evidence

- Dispatch HEAD: `e03b626c85021666411dac04e2209b9789e27ac4`.
- Evidence root:
  `/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b2-c1-path-owner-27aacbf-20260730T1547Z`;
  observed directory dev `16777240`, inode `2188341`, mode `0700`, regular
  directory/non-symlink.
- Path-owner index:
  `/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b2-c1-path-owner-27aacbf-20260730T1547Z/path-owner-index.json`,
  `12195` bytes, mode `0600`, SHA-256
  `b189117fdd0a9a65ca80660245ec84b7f2f533c3e496c96e76eb48a4666feb35`.
- Index seal:
  `/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b2-c1-path-owner-27aacbf-20260730T1547Z/path-owner-index.sha256.json`,
  `682` bytes, mode `0600`, SHA-256
  `867d1ffad5bd29f24dc81b24a58ce66393dd688833d3a4516fe7f45ef50875e9`.
- Terminal:
  `/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b2-c1-path-owner-27aacbf-20260730T1547Z/terminal-evidence.json`,
  `13455` bytes, mode `0600`, SHA-256
  `c21a691272ca7466271349daa5b10236c9f36dfeb481d592e9c368a87e7a4763`.
- Terminal seal:
  `/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b2-c1-path-owner-27aacbf-20260730T1547Z/terminal-evidence.sha256.json`,
  `772` bytes, mode `0600`, SHA-256
  `4bfebf4ad40e8c2e65ad2470faaed184f21d39eda73c13e689b09769d280752f`.
- EXECUTION_RESULT snapshot at review: SHA-256
  `7702bd4e3fce658f07668b82899d17f15edab1f6b23d415d4f3bd9879b454f4e`.

## Independent validation and findings

All four evidence files are physical regular non-symlink mode-`0600` files,
strict duplicate-key/non-finite JSON, and byte-identical to canonical compact
sorted UTF-8 serialization with one LF. Their schema/status pairs are exact:

1. `p7_retained_r3_path_owner_index_v1` /
   `path_owner_resolved_waiting_for_planner`;
2. `p7_retained_r3_path_owner_index_seal_v1` /
   `sealed_waiting_for_planner`;
3. `p7_retained_r3_b2_c1_path_owner_terminal_v1` /
   `pass_waiting_for_planner`;
4. `p7_retained_r3_b2_c1_path_owner_terminal_seal_v1` /
   `pass_waiting_for_planner`.

The index seal reproduces the physical index bytes/SHA/schema/status, the
terminal reproduces both index and index-seal identities, and the terminal
seal reproduces the physical terminal bytes/SHA/schema/status. The terminal
seal states `terminal_write_returned=true` only after the terminal writer
returned and states `terminal_seal_self_write_return=not_self_attested`.
This is the required non-circular physical-write semantics.

The earlier B2 counter ambiguity is not repeated. The index contains its
pre-index-write snapshot `(index,index-seal,terminal,terminal-seal) =
(0,0,0,0)`. The terminal contains its pre-terminal-write snapshot
`(1,1,0,0)`. Physical presence and exact identity of the terminal are then
confirmed by the separate seal; the seal does not claim to prove its own
return. The evidence root contains exactly those four files.

The directory-chain/cardinality recomputation is exact: three directory
`lstat`, three `scandir`, direct-entry counts `10 + 1 + 3 = 14`, and fourteen
entry stats. Package root contains exact directory child `child-output`, that
directory contains exact directory child `lineage-release-r3`, and the retained
source direct name set is exactly the three expected regular non-symlink names.
The three mechanical absolute paths are:

1. `/Volumes/4T/temp/rgbww-optimizer/p7-td-b-lineage-release-r3/lineage-release-32b9e67-r2-20260727T2227/child-output/lineage-release-r3/current-lineage-candidate.json`;
2. `/Volumes/4T/temp/rgbww-optimizer/p7-td-b-lineage-release-r3/lineage-release-32b9e67-r2-20260727T2227/child-output/lineage-release-r3/resolved-formal-plan.json`;
3. `/Volumes/4T/temp/rgbww-optimizer/p7-td-b-lineage-release-r3/lineage-release-32b9e67-r2-20260727T2227/child-output/lineage-release-r3/setup-lineage-release.json`.

Every resolved item says `content_identity=not_observed_by_this_package` and
`current_content_validated=false`. Separate artifact lstat and artifact
open/read/hash/parse/mmap/copy are all zero. Historical archive
lstat/open/read/hash are `3/3/3/3`; controller/root are `1/1`; retry,
fallback, alternate root, parent/sibling listing, recursive search, Git
mutation, tests, validators, eligibility, release, network, device, and all
later-stage counters are zero. The sole ER append occurred after the terminal
seal and is intentionally not part of the terminal's pre-write counter.

## Decision and residual risks

C1 is accepted only as exact path/type ownership evidence. It proves an
unambiguous current absolute path for each named artifact; it does not prove
artifact bytes, hashes, semantic validity, immutability during a future read,
canonical eligibility, consumability, or release authority. Retained R3
therefore remains `RETAINED_UNVALIDATED_UNCONSUMED`.

The corrected B2 manifest package must consume the exact C1 index and its
sealed identity rather than the stale historical source path. It must then
perform exactly one non-following lstat/open/read for each resolved artifact,
prove the three expected content hashes and before/after fstat stability, and
preserve the complete modern accepted-integration baseline. Any C1 evidence
drift, path mismatch, artifact mismatch, or read/persistence failure stops
without alternate-path discovery, retry, repair, regeneration, or release.

This is an engineering provenance transition. No unresolved color or
measurement science exists, and no dangerous device operation is in scope;
Advisor guidance and Human authorization are not required.

## Exact next branch

- Return to reference task `REF-P7-25-R2-B2`.
- Contract:
  `P7-TD-B-RETAINED-R3-OPTION-B-B2-CORRECTED-PATH-MANIFEST-SEAL-V3`.
- Single execution action after Orchestrator review and a later Planner
  activation: consume the accepted exact C1 index/seals, read each resolved
  artifact exactly once, and seal the corrected subordinate immutable v2
  provenance manifest in one brand-new root.
- Current stop: `B2_C1_ACCEPTED_WAITING_ORCHESTRATOR_REVIEW` with
  `execution_authorized=false`.
- Future execution stop after activation:
  `B2_CORRECTED_MANIFEST_SEALED_WAITING_PLANNER_REVIEW`.

## 维护性判断

C1 cleanly separates path ownership from artifact-content identity and from
the canonical eligibility owner. The next package reuses that single sealed
index rather than adding discovery or a parallel validator. No repository
abstraction or architectural refactor is needed.
