# REF-P7-25-R2-B2-P7-I1 Planner review archive

**Review time:** `2026-07-31 20:23 -0600`

**Reviewed contract:**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-P7-I1-ACCEPTED-OWNER-FRESH-SYNTHETIC-INTEGRATION-QUALIFICATION-V1`

**Decision:**
`REJECTED_TERMINAL_COUNT_SNAPSHOT_INCONSISTENCY_INTEGRATION_SEMANTICS_PROVISIONALLY_PROVEN`

**Exact next branch:** `REF-P7-25-R2-B2-P7-I1-E1`, a pure-offline,
append-only evidence supersession/index closure. It must not rerun the builder,
runtime, controller, process, integration, tests, or Git6, and it must not mutate
the retained source/root or any byte of the existing ER prefix.

## 1. Reviewed topology and execution method

- Activation `c245bbc7d7b120c83dd59b2b2cc87b8f9f01dae2` has direct parent
  `9d8573fd4155851adc6e71b3b0ccc50365f6f6d3`, exact subject
  `chore(plan): activate p7 synthetic integration`, and exact paths
  `.agent-work/FULL_PLAN_REFERENCE.md`, `.agent-work/PLAN.md`, and
  `.agent-work/PLANS/20260731-1921-p7-retained-r3-b2-p7-acceptance-route-review.md`.
- Evidence commit `6c85cdb07a115b16c3879805c0a14f37b866f0df` is the direct child of
  activation, has subject `chore(evidence): record p7 synthetic integration`,
  and changes only `.agent-work/EXECUTION_RESULT.md` by appending `179` lines.
- The execution composed one frozen `ControllerDomainTemplateSpec`, invoked the
  accepted P6 builder once, passed its exact runtime request to the accepted P5
  runtime once, and retained the generated source and physical root. No retry,
  fallback, second source/root/process, test, device, release, or retained-R3
  route was entered.
- Accepted owner identities were independently checked without executing them:
  runtime `37f7d0021c7a81a9d6680815bc51c305cf807a7b`, builder
  `48b3979d6c0df5f488cd500597e26dc4c38877dd`, and runnable template
  `864f08cc5436519a37e41d553e49ebde4a3c8bb2`. Runtime source/test blob OIDs
  are `075face6fd7453236affa303640b91eb16a42a9b` and
  `a6aa7d7caf015e2eb858830dc89aaedaeb51aafa`; runnable source/test blob OIDs
  are `5529ec27b3893c20995e9a8cb3a9fa5c0a87a3b5` and
  `d0f733426673aa9a57fcb1195ecea014f8c48062`.

## 2. Immutable external evidence audit

Source, inspected read-only and never executed during review:

- `/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-p7-i1-source-c245bbc7d7b1.py`
- regular file, mode `0600`, bytes `13946`, device `16777240`, inode `2253709`
- SHA-256 `e66afc9b6d2a8b9092a5d051fc3260a3078cab1d60ea5ceb92baa755bca6bc0a`

Root, inspected with `lstat` and no symlink following:

- `/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-p7-i1-root-c245bbc7d7b1`
- physical directory, mode `0700`, device `16777240`, inode `2253710`
- exact direct file set `9/9`; every file is regular, mode `0600`, direct under
  the same physical root, strict UTF-8 JSON, and byte-for-byte canonical JSON.

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| `synthetic-plan.json` | 16 | `f235229723506e28e6ea148dd2f80bcc71b4612239f1f6b0009747dd37111702` |
| `synthetic-full.json` | 16 | `b3d452931897ddca36ea73587fc00b3900925fa4d5e7144899c2f88f671d4d9d` |
| `synthetic-lineage.json` | 19 | `c0d4ed42c5435ad2c4595d157c38ef7c961b08f9038c9402b1c7b96624ec987e` |
| `synthetic-seal.json` | 16 | `7dc2d9a59478b3daa8f1ba0b506373db33a1cc00e5be4488a90f2e3ea1ac5542` |
| `integration-qualification.json` | 435 | `1a37676bf034bc575f57570a9532d32db6395d675bb2addf0a7da4242c3768a8` |
| `integration-qualification.sha256.json` | 132 | `9e80d174ad63f8adc4423d0f94c7c249d6f14e7086c678a5ba4498d981c2a257` |
| `terminal-evidence.json` | 44 | `16503bcb3d78becd58f9fcbb0f2a67de9f529eeaabce14d9697fe7ee7c1ce937` |
| `terminal-evidence.sha256.json` | 123 | `667ef7b5eb899feea579f2c9a9affa12cf490e67997cd8b46127e8e69049e8b1` |
| `execution-result-admission.json` | 18 | `ae37face4b811daec3d0c6762e22bb2c99b47ee47e14d2a6d218a20a3afc9908` |

Both sidecars name the exact same-root target and bind its exact byte count and
SHA-256. Qualification contains the exact ordered `16/16` true list-of-lists:
six Git results, four same-root results, three fixture results, and three
terminal-stage sentinels. The immutable source performs exact Git6 before root
creation, persists and reads back four same-root inputs, rejects a non-true
matrix before qualification, writes qualification before terminal, verifies
terminal before seal, and writes admission last. Therefore the exact9 durable
artifacts plus source identity and successful process envelope independently
prove Git6, matrix16, same-root4, and
qualification -> terminal -> seal -> admission even though the compact runtime
report does not repeat their individual identities.

The process returned exit `0`; stdout is one canonical JSON envelope, bytes
`105`, SHA-256 `6a5c5cef84aec4b3bbad2361502756c1c05cf25b0ddddccbb36062185bc82abc`,
with artifact count `9` and the required waiting-for-review status. Stderr is
empty, SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.
The synchronous runtime report is terminal and a direct process-table scan found
no residual owned `/Users/ibobby/Projects/WLED-RGBWW/.venv/bin/python -` process.

## 3. ER append audit and finding

- ER immediately before integration handoff: bytes `1133941`, SHA-256
  `a60e328ae4c47abd5f56d2116b8239fcb1bb4f23c969001a3b4dde8b1e060f6f`.
- ER at evidence commit: bytes `1140609`, SHA-256
  `85072a33ae2cf9d9074f70ec93263ce36e8ff9a25bf14ba1e1a290088cd2409f`.
- Git proves an EOF-only append at `@@ -17166,0 +17167,179 @@`, exactly `179`
  lines and `6668` bytes, with no deletion or earlier-byte rewrite.

The machine-readable terminal record was assembled before its own append. It
therefore reports `counts.execution_result_append=0` and
`counts.outer_shell_commands_cumulative=4`. The actual historical terminal
facts, independently proved by the direct-child evidence commit and append
delta, are one integration ER append and five total outer shell commands: the
four captured before the record plus the final append command. Calling the
former values cumulative without a snapshot boundary makes terminal evidence
internally inconsistent. This violates the PLAN requirement for truthful actual
counts and exact append `1`; the independent proof cannot silently rewrite the
immutable record or let Planner reinterpret `0` as `1`.

## 4. Acceptance matrix

| Requirement | Result | Evidence quality |
| --- | --- | --- |
| Activation topology, exact paths, initial clean | PASS | Git objects plus clean dispatch handoff |
| Fresh derived source/root and no old-path access | PASS | owner-returned identities and unique exact paths |
| spec1/builder1/runtime1, override0 | PASS | immutable runtime report and terminal record |
| Runtime-owned source write/read/process | PASS | source physical identity and runtime report |
| Source regular/0600/bytes/hash | PASS | independent lstat/read/hash |
| Git6, same-root4, matrix16/16 | PASS | exact immutable source plus canonical qualification |
| qualification -> terminal -> seal -> admission, exact9 | PASS | source control flow plus independent artifact audit |
| stdout/stderr/exit and no residual process | PASS | report, independent hashes, process scan |
| retry/fallback/second owners and hard locks zero | PASS | bounded execution handoff; no contrary artifact |
| ER pre-terminal zero and EOF-only append | PASS | frozen pre-hash and Git append delta |
| Truthful actual terminal counts | **FAIL** | stale pre-append snapshot labeled cumulative |

## 5. Decision, residual risk, and next branch

The scientific or implementation route is not at fault; no Advisor or Human
decision is needed. The integration's substantive success label remains only
`FRESH_SYNTHETIC_INTEGRATION_QUALIFIED_NOT_RETAINED_ELIGIBLE`. It is not yet
accepted or permitted to unlock retained validation because the terminal count
record is not self-consistent.

The only successor is a minimal append-only evidence supersession/index closure.
It must freeze the existing ER prefix, source, root, and nine hashes; state that
only the two historical count fields are superseded; bind the supersession to
activation `c245bbc...`, evidence commit `6c85cdb...`, the exact old terminal
record, and the independent append proof; record historical actual append `1`
and historical final shell count `5`; and append once only after all checks pass.
It must not edit, regenerate, rename, delete, or reuse any old source/root/ER
byte, and must not rerun integration, controller Git6, tests, retained validation,
release, network, or device work. Planner must review that append before the
Orchestrator may mark synthetic integration accepted or unlock a successor.

维护性判断：本轮仅审计 immutable evidence，并把一个终端计数快照语义缺口隔离为
append-only evidence closure；不新增生产抽象、writer、controller 或状态 owner。
