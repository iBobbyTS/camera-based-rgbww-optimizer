# REF-P7-25-R2-B2-R2 real-B2 manifest failure review

**Review date:** `2026-07-31`

**Reviewed reference task:** `REF-P7-25-R2-B2-R2`

**Reviewed contract:**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-R2-REAL-MANIFEST-ONLY-V2`

**Planner decision:**
`REJECTED_BOUNDED_B2_R2_C1_LINKAGE_FAILURE_ADMISSION_AND_HANDOFF_IDENTITY_CORRECTION_REQUIRED`

**Reviewed PLAN identity:** bytes `17637`, SHA-256
`1890b879320116c3575f8548a8a7677bff468fa10a354bd66886af2dc824b651`.

**Reviewed stop:** `B2_R2_REAL_MANIFEST_TERMINAL_WAITING_PLANNER_REVIEW`.

## 1. Independent review scope

Planner independently inspected the active PLAN/FULL machine rows, activation and
evidence commits, exact package-local controller source, exact failed output root,
and the accepted C1 four-file root. The four C1 files and the two output files were
rehashed and strict-parsed; canonical compact sorted UTF-8 plus one LF was
reconstructed; physical path/bytes/SHA/mode/device/inode and logical linkage were
compared directly. The controller source was independently SHA-256 checked,
AST-parsed and compiled. No retained-R3 artifact was opened because execution never
passed acquire; no Git provenance replay, test, validator, eligibility, release,
network, environment, device, camera, light, cleanup, FORMAL or analyzer operation
was invoked.

Activation topology is exact: commit
`4fc3a85235173c4a5a38e21c2836e9f209decd77`, direct parent
`3a05490ae2f2e112db54010a4843f2be42393947`, subject
`chore(plan): activate real b2 manifest seal`, and exact changed paths
`.agent-work/FULL_PLAN_REFERENCE.md`, `.agent-work/PLAN.md`, and
`.agent-work/PLANS/20260730-2254-p7-retained-r3-provenance-io-acceptance-transition-stop.md`.
The evidence commit `b74944fb0bd5ffa064ba1ac92ae390fff7e008dc`
is its direct child and changes only `.agent-work/EXECUTION_RESULT.md`.

## 2. Reconstructed physical evidence

The unique controller source is mode `0600`, bytes `29162`, SHA-256
`a5a24ef557978eb9b76cb47bdf8c58808035d98a7470100dce18c1c838f8de4e`;
its AST parse and builtin compile pass. The unique output root is mode `0700`,
device `16777240`, inode `2217793`, and contains exactly two direct children:

- `terminal-evidence.json`: bytes `1547`, mode `0600`, device `16777240`,
  inode `2217794`, SHA-256
  `b94680160307e9c3577ed59da1217dff344f3011e2b2f5c99edb5fdaac1f6d69`;
- `terminal-evidence.sha256.json`: bytes `457`, mode `0600`, device `16777240`,
  inode `2217795`, SHA-256
  `e7ffc6b080729afaf926656b68f5d2e1f50fe2be8d3f5475af6a4986a908be90`.

Both are strict canonical JSON. The seal exactly binds the terminal absolute path,
bytes, SHA-256, device and inode, states `terminal_write_returned=true`, and does
not self-attest its own write. Terminal status is `fail_waiting_for_planner`, failed
phase `acquire`, stable code `RuntimeError:index_seal_link_drift`. Counters are
C1 reads `4`, retained reads `0`, Git calls `0`, candidate entries `0`, manifest/
seal `0/0`, validator `0`, retry/fallback/second-root `0/0/0`. Manifest, manifest
seal, and execution-result admission are physically absent.

The EXECUTION_RESULT handoff records terminal-seal SHA-256
`e7ffc6b080729af926656b68f5d2e1f50fe2be8d3f5475af6a4986a908be90`,
which is only `62` hexadecimal characters and omits the two-character `af` from the
authoritative digest. It therefore does **not** equal the independently recomputed
physical seal-file SHA-256 above. The handoff's terminal SHA, bytes, mode, device and
inode otherwise match the physical files. The immutable ER and physical evidence
remain unchanged; the corrected Planner contract must carry the physical
64-character value and reject the transcribed value.

The accepted C1 input root remains device `16777240`, inode `2188341`, mode `0700`.
Its four exact direct-child mode-`0600` files independently match their frozen
bytes/SHA values:

| File | Bytes | Device | Inode | SHA-256 |
| --- | ---: | ---: | ---: | --- |
| `path-owner-index.json` | `12195` | `16777240` | `2188342` | `b189117fdd0a9a65ca80660245ec84b7f2f533c3e496c96e76eb48a4666feb35` |
| `path-owner-index.sha256.json` | `682` | `16777240` | `2188343` | `867d1ffad5bd29f24dc81b24a58ce66393dd688833d3a4516fe7f45ef50875e9` |
| `terminal-evidence.json` | `13455` | `16777240` | `2188344` | `c21a691272ca7466271349daa5b10236c9f36dfeb481d592e9c368a87e7a4763` |
| `terminal-evidence.sha256.json` | `772` | `16777240` | `2188345` | `4bfebf4ad40e8c2e65ad2470faaed184f21d39eda73c13e689b09769d280752f` |

All four are strict canonical JSON with their accepted schema/status pairs. Their
accepted linkage is exact and unchanged: the index seal's direct `index` record
binds `relative_path + bytes + sha256 + mode + schema + status`; terminal direct
fields `index_identity` and `index_seal_identity` bind each direct child through
`relative_path + bytes + sha256 + mode`; terminal seal's direct `terminal` record
binds `relative_path + bytes + sha256 + mode + schema + status`. Physical root,
absolute direct-child path, device and inode are established independently by the
non-following descriptor reads; the older C1 logical records never claimed to
contain device/inode.

## 3. Planner findings

### REV-B2-R2-001 — Must Fix: controller over-constrained accepted C1 linkage

The controller's generic recursive `contains_identity` requires every matching
record to expose exact keys `path`, `bytes`, `sha256`, `device`, and `inode`.
Accepted C1 deliberately exposes schema-specific direct logical records using
`relative_path`, bytes/SHA/mode and, where applicable, schema/status. It contains no
device/inode in those target records because physical descriptor identity is a
separate proof. Therefore line 188's first predicate must reject an unchanged,
accepted index seal. The observed `index_seal_link_drift` is a deterministic
controller-composition defect, not C1 or retained evidence drift. A correction must
use direct schema-owned fields and exact key/type/value checks; recursive generic
containment, coercion, aliasing, or adding nonexistent C1 fields is forbidden.

### REV-B2-R2-002 — Must Fix: sealed FAIL terminal did not reach ER admission

The controller writes and independently seals a valid FAIL terminal, then requires
the overall exact-five result to be PASS before constructing the seal gate and
calling `validate_and_emit_execution_result`. Thus any earlier phase failure leaves
`execution-result-admission.json` absent even when terminal linkage is valid. The
reviewed PLAN required success or failure terminal evidence and permitted ER emission
only after the terminal-seal gate; it did not permit an overall-PASS prerequisite for
failure admission. The correction must make terminal sealing dominant: a valid
PASS or FAIL terminal seal admits one matching ER record, with manifest targets
nullable on pre-manifest failure; an invalid/missing seal admits none.

### REV-B2-R2-003 — Must Fix: ER handoff seal SHA transcription is not physical identity

The handoff's terminal-seal SHA has `62` characters and differs from the physical
seal-file SHA by the missing two-character substring `af`. It cannot be admitted as an exact SHA-256
identity even though the remaining handoff facts are accurate. The physical file
and its independently recomputed 64-character SHA-256 are authoritative. The
correction must carry exact physical value
`e7ffc6b080729afaf926656b68f5d2e1f50fe2be8d3f5475af6a4986a908be90`,
reject the transcribed 62-character value as malformed/mismatched, and keep both
the existing ER and evidence files immutable. No repair, rewrite or inference from
the handoff string is permitted.

No input drift, retained-artifact mismatch, Git mismatch, scientific ambiguity or
device-authority issue was observed. Because acquire failed before retained reads,
the original real-B2 scientific/provenance result remains entirely untested.

## 4. Decision and next bounded branch

Decision:
`REJECTED_BOUNDED_B2_R2_C1_LINKAGE_FAILURE_ADMISSION_AND_HANDOFF_IDENTITY_CORRECTION_REQUIRED`.

The next branch is `REF-P7-25-R2-B2-R2-C1`, contract
`P7-TD-B-RETAINED-R3-OPTION-B-B2-R2-C1-C1-LINKAGE-FAILURE-ADMISSION-PHYSICAL-SEAL-QUALIFICATION-V1`.
It is a pure-offline correction qualification only: one fresh correction root may
read the accepted C1 four-file set exactly once, prove the direct schema-specific
linkage, carry the authoritative physical terminal-seal identity, and exercise a
bounded in-memory drift/failure-admission/identity-admission matrix. It must not
open the retained R3, replay Git provenance, produce the subordinate manifest, retry
or reuse the failed real-B2 root, run the canonical validator, emit eligibility, or
perform release/device/scientific work. Passing only returns a corrected composition
contract for a later fresh real-B2 Planner package; it does not itself authorize that
execution.

**Proposed FULL transition:** mark `REF-P7-25-R2-B2-R2` as
`REJECTED_CONTROLLER_C1_LINKAGE_FAILURE_ADMISSION_AND_HANDOFF_IDENTITY_DEFECT`; add
`REF-P7-25-R2-B2-R2-C1` as the sole task waiting for Orchestrator activation; keep
retained R3 `RETAINED_UNVALIDATED_UNCONSUMED` and B3/B4/validator/eligibility/release
locked.

**Exact stop:** `B2_R2_REJECTED_WAITING_ORCHESTRATOR_C1_ACTIVATION`.

## 5. Residual locks and maintainability

The failed source/root are immutable rejected evidence and must never be repaired,
deleted, reused, or reinterpreted. Real B2 retry, alternate/second root, retained
reads, Git provenance replay, subordinate manifest, B3/B4, retained audit,
canonical validator, eligibility, release generation/qualification/copy/consumption,
network/DNS/environment/credentials, device/camera/Ray/strip/cleanup/capture,
FORMAL/public analyzer/TD-C/sentinel/P8/firmware/deployment remain locked at zero.

维护性判断：三个缺口都位于一次性 outer composition/handoff，不在 accepted provenance,
preparation 或 exact-five owners 内。下一包只冻结 schema-specific mapping 与
seal-dominant admission contract，不新增仓库生产 owner，也不扩张 eligibility 或
scientific ownership；通过后应由 later fresh real-B2 package直接消费该合同。
