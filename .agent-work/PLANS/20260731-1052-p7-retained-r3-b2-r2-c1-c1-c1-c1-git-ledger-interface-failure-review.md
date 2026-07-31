# REF-P7-25-R2-B2-R2-C1-C1-C1-C1 Planner failure review

## 1. Reviewed scope and immutable facts

Planner reviewed the active contract
`P7-TD-B-RETAINED-R3-OPTION-B-B2-R2-C1-C1-C1-C1-SOURCE-ROOT-DIRECT-CHILD-QUALIFICATION-V1`,
the committed Executer handoff at `67a5579382d1a52ce6de3d287cf57a70868c0c75`,
the current committed owner interfaces, and the persistent second-pass record
`.agent-work/debug/active/20260731-p7-retained-r3-b2-controller-contract-drift.md`.

The immutable failed controller is
`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b2-r2-c1-c1-c1-c1-source-root-binding-controller-486ae92-20260731T1639Z.py`,
bytes `23629`, SHA-256
`0fbda54d91a6941782ea0470100ab55ca66811ca6e31a3463523be5ff0bd9c93`.
It was dispatched once and exited `1`. All six allowlisted read-only Git calls
returned, but controller lines 172 and 180 accessed nonexistent
`GitLedger.returncode`; the owner field is `GitLedger.exit_code`. The resulting
error was `AttributeError:'GitLedger' object has no attribute 'returncode'`.

The failure was pre-root: fresh output-root creation, source-root observations,
accepted C1 reads, matrix cases, qualification/seal, terminal/seal and ER admission
were all `0`. Retained R3, real B2, manifest, validator, eligibility, release,
network and device operations were also `0`. The failed source and absent root are
immutable and must not be read, rerun, repaired, regenerated, reused or deleted.

## 2. Findings

### REV-B2-R2-C1-C1-C1-C1-001 — controller used a nonexistent GitLedger field

The committed provenance owner defines the exact frozen field set
`argv,cwd,exit_code,stdout,stderr,stdout_sha256,stderr_sha256`. The failed
controller instead used `returncode` twice. This is a deterministic controller
composition defect, not a Git failure and not evidence that the six returned
ledgers or activation tuple were invalid.

### REV-B2-R2-C1-C1-C1-C1-002 — pre-dispatch gates did not verify owner interfaces

Strict UTF-8, AST parsing, builtin compilation and import success only establish
syntax and importability. They do not prove that controller attribute accesses
belong to the accepted owner return types. Repeated one-off controllers have
therefore corrected the latest observed literal while leaving adjacent owner
contracts inferred. Another dispatch is unacceptable until a source-backed
pre-dispatch conformance gate enumerates every attribute access on every accepted
owner return type and rejects any attribute outside the committed dataclass field
set or explicitly frozen public method set.

### REV-B2-R2-C1-C1-C1-C1-003 — preserve the valid source-root and terminal contracts

The failure occurred before root acquisition, so it neither validates nor refutes
the already-planned root-first ordering, live `DirectoryIdentity`, four root-bound
direct-child reads, logical `"0600"`, exact 24-case matrix, or PASS/FAIL sealed
admission lifecycle. The successor must preserve all of them unchanged after the
new owner-API gate passes. A pre-root API failure must still append exactly one ER
handoff from the launcher's in-memory source identity and must not create a root.

## 3. Source-backed interface freeze

Planner independently inspected the current committed owners. The successor gate
must freeze and verify these exact dataclass fields before dispatch:

- `DirectoryIdentity`: `path,device,inode,mode`;
- `FileIdentity`: `path,data,byte_count,sha256,device,inode,mode,root`;
- `GitLedger`: `argv,cwd,exit_code,stdout,stderr,stdout_sha256,stderr_sha256`;
- `MachineContractEvidence`: `schema,owner,marker_ascii,source_bytes,source_sha256,candidate_count,candidate_lines,line_number,raw_row_bytes,raw_row_sha256,payload_bytes,payload_sha256,line_ending`, with public method `to_mapping` only;
- `ParsedMachineContract`: `value,evidence`;
- `ByteSpan`: `start,end`;
- `OwnedStatementPair`: `assignment_span,validation_span,function_name`;
- `PreparedControllerSource`: `source,source_sha256,pair`;
- `SealTargetIdentity`: `path,byte_count,sha256,device,inode`, with public method `as_mapping` only;
- the internal validated seal gate may be passed opaquely to the admission callback
  but controller code must not introspect or access attributes on it.

For every accepted-owner call site, the static gate must bind the assigned name to
its known return type, collect all direct attribute accesses on that name, compare
them to the exact frozen set, and reject unknown fields including `returncode`.
Aliasing, dynamic `getattr`, `vars`, `__dict__`, reflection, type guessing or an
unbound result name must fail closed. Six Git ledgers must then be checked with
`exit_code == 0` and exact empty `stderr`; `returncode` must occur only inside the
negative in-memory/static test specimen, never in dispatched controller code.

## 4. Decision and next branch

Decision:
`REJECTED_BOUNDED_B2_R2_C1_C1_C1_C1_GIT_LEDGER_OWNER_INTERFACE_CORRECTION_REQUIRED`.

The sole next branch is `REF-P7-25-R2-B2-R2-C1-C1-C1-C1-C1`, contract
`P7-TD-B-RETAINED-R3-OPTION-B-B2-R2-C1-C1-C1-C1-C1-OWNER-API-CONFORMANCE-SOURCE-ROOT-QUALIFICATION-V1`.
It authorizes one fresh pure-offline controller and root only after a pre-dispatch
source-backed owner API conformance gate passes. It preserves single-source active
activation, root-first creation, root-bound reads, logical `"0600"`, the exact
24-case matrix, qualification/terminal seals and admission. It does not authorize
reading old sources/roots/evidence, retained R3, real B2, Git provenance replay,
manifest, validator, eligibility, release, network or device work.

**Proposed FULL transition:** mark
`REF-P7-25-R2-B2-R2-C1-C1-C1-C1` as
`REJECTED_GIT_LEDGER_OWNER_INTERFACE_DRIFT`; add
`REF-P7-25-R2-B2-R2-C1-C1-C1-C1-C1` as the sole task waiting for Orchestrator
activation; set
`repair_v2_status=R2_C1_C1_C1_C1_REJECTED_GIT_LEDGER_API_C1_ACTIVE`; preserve
`retained_r3_status=RETAINED_UNVALIDATED_UNCONSUMED`; keep every real-B2,
retained, validator, release and device route locked.

## 5. Planner handoff

Planner modified only this archive and `.agent-work/PLAN.md`. FULL, ER, GUIDE,
RESEARCH and debug state remain read-only. Orchestrator must independently review,
update FULL and create the exact activation commit before dispatching a fresh
Executer. Planner stops at
`B2_R2_C1_C1_C1_C1_C1_OWNER_API_QUALIFICATION_WAITING_ORCHESTRATOR_ACTIVATION`.

维护性判断：纠偏仍局限于一次性外置 controller，但新增的 source-backed owner
API gate消除连续猜接口的根因；生产 owner、validator、release 与科学路径均不修改。
