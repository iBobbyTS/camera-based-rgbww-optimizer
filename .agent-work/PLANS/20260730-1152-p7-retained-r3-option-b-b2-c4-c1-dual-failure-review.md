# REF-P7-25-R2-B2-C4-C1 review：dual failure and evidence-lifecycle rejection

**Review date:** `2026-07-30`

**Planner decision:** `REJECTED_DUAL_OWNER_AND_EVIDENCE_LIFECYCLE_FAILURE`

**Reviewed contract:**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-C4-C1-BYTE-SPAN-STATEMENT-SELECTOR-CORRECTION-V1`

**Reviewed stop:** `B2_C4_C1_BYTE_SPAN_SELECTOR_WAITING_PLANNER_REVIEW`

## 1. Reviewed scope and method

The reviewed package authorized one content-free correction at one brand-new
external root. Its declared method was to consume the exact five durable C4 V3
evidence files and the frozen V3 builder once, structurally replace the
line-only statement selector with one byte-span helper, qualify it `12/12`,
write a terminal plus non-self-attested seal, and append ER only after a valid
strictly reloaded seal. It prohibited corrected generation retries, real C4,
upstream source/C3/C1/C2/retained reads, validator, eligibility, release,
network and device work.

Planner independently inspected only the active PLAN, the latest C4-C1 ER
append, the four physical C4-C1 artifacts, and the frozen C4-C1 controller. It
did not rerun the owner, tests, validator or any device/network action and did
not reopen the C4 V3 inputs, V3 builder, C3/source/retained evidence, or any
later stage.

## 2. Physical evidence

Brand-new root:
`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b2-c4-c1-byte-span-selector-df0020d-20260730T1745Z`

The root contains exactly four preserved regular mode-`0600` files:

| Artifact | Bytes | SHA-256 | Strict JSON |
| --- | ---: | --- | --- |
| `progressive-00-root-created.json` | 645 | `3d6e1ba53f2d8cb8384684179d526c371df78732f158a7e55af4e64181323b03` | valid |
| `progressive-01-v3-failure-accepted.json` | 2256 | `f36acbe877a27b9c2e5f75d86c6566df600532edad35bfc41c649278de20aacf` | valid |
| `terminal-evidence.json` | 962 | `09b4add8bfb7daf931087aa2d6b2c752028682035b1ed6dcd4f305d4c468a7c0` | valid |
| `terminal-evidence.sha256.json` | 336 | `8bc0fe09d02fb0cebbefb05554cef0f4f3b84cfb1403d5e8f01e6cf58be36ade` | **invalid** |

The root evidence binds dispatch
`02192d3110402ae9f477f1e76b31ac965bf6c584`, its direct parent
`149c2cabc94336407b324d21fe894f89e545d3c1`, one symbolic HEAD read, no
second read, PLAN bytes `15439`, and PLAN SHA-256
`3019317145675838866f7f0d985a5ae6a78f5f7763fdae66b7beb0b4860fcbfe`.
The progressive acceptance records exact V3 input budgets `5/5` and zero
retained, validator, release, network and device calls.

Frozen C4-C1 controller:
`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-b2-c4-c1-byte-span-controller-v1.py`,
bytes `28701`, SHA-256
`ba05a533f76dec4e64519b1a76970c791521223c1936ff3cb856222218d45dac`.

## 3. Findings

### REV-C4-C1-001 — AST scope owner is incorrect

The terminal truthfully hard-fails with exact
`RuntimeError: faulty assignment owner` before corrected-builder generation,
delta, or matrix output. The frozen controller first identifies the unique
faulty `containing` assignment structurally, but then requires its *direct*
parent to be `FunctionDef`/`AsyncFunctionDef`. The actual assignment is a
statement in an intermediate nested statement container under `main`; direct
parent and enclosing function scope are different concepts. Consequently the
correction cannot reach its intended byte-span helper generation.

This is an engineering selector defect, not a scientific contradiction. The
next owner must discover the nearest enclosing function by ancestor traversal,
prove it is the sole `main`, separately discover the exact list-valued
statement field that directly contains the assignment, and require the
cardinality validation to be the immediately following statement in that same
scope. It must never restore a direct-parent assumption or cross a statement
scope boundary.

### REV-C4-C1-002 — invalid physical seal and unauthorized ER append

The physical seal ends with the two literal bytes `\\n`, not one LF byte.
Strict JSON parsing therefore fails with extra data at byte `334`; the seal is
not canonical JSON and cannot prove terminal linkage. The frozen controller's
embedded child writer uses an escaping form that serializes literal
backslash-`n`. Its failure branch then appends ER immediately after the child
process returns without strict seal reload or target-link validation. The
terminal's pre-serialized `er_permission_after_seal=true` cannot create that
permission.

These are evidence-lifecycle violations. The invalid seal is preserved as
physical failure evidence and must not be repaired, rewritten, normalized,
renamed, regenerated or treated as valid. The ER append is an unauthorized
diagnostic observation only; it is **not** an accepted sealed handoff and must
not be used to advance C4-C1 or B2.

The next owner must introduce one canonical-LF terminal-seal writer plus a
strict reload/linkage gate shared by success and failure paths. No ER open or
append may be reachable until that gate returns successfully. A negative
matrix must prove literal-backslash-`n` and other noncanonical encodings are
rejected and leave the ER append count at zero.

## 4. Validation quality and budget conclusion

- Selector correction result: `0`; delta/matrix: `0/0`.
- Terminal physical file: present and hashable, but its declared seal is
  invalid; evidence strength is therefore `PHYSICAL_FAILURE_FILES_ONLY`, not a
  sealed execution handoff.
- Frozen controller invocation: `1`; C4 V3 inputs `5/5`; frozen V3 builder
  read `1` as reported by the durable progressive artifact.
- Retry/fallback/second owner/root: `0/0/0/0`.
- Retained/validator/eligibility/release/network/device and later-stage calls:
  `0`.
- The failed root and all four physical files remain immutable. No repair or
  reuse is allowed.

## 5. Decision, residual risk, and exact next branch

C4-C1 is rejected. It does not qualify a corrected builder, does not validate
real C4, and does not unlock B2/B3, retained R3, canonical validation,
eligibility or release.

The sole next branch is
`REF-P7-25-R2-B2-C4-C1-C1`, contract
`P7-TD-B-RETAINED-R3-OPTION-B-B2-C4-C1-C1-DUAL-OWNER-CONTROLLER-CORRECTION-V1`.
It is one content-free correction owner that reads the four frozen C4-C1
physical artifacts and frozen C4-C1 controller exactly once, without reading
any C4 V3 payload or builder. It may generate one corrected controller only,
repairing exactly (a) AST ancestor/statement-scope containment and (b)
canonical-LF seal writing plus strict pre-ER reload/linkage gating. A
brand-new root and exact negative matrix must qualify both repairs without
invoking the corrected controller's real `main`.

Residual risk remains that static structure alone might not establish control
flow dominance for both ER branches. The next matrix must combine AST proofs
with an isolated synthetic gate simulation showing every invalid seal,
including literal `\\n`, causes `ER append = 0`. Only a later, separately
authorized fresh C4-C1 attempt may execute the corrected real path.

All old payload repair/regeneration, C4 V3 input/builder reread, corrected real
main, B2/B3, retained R3, validator, eligibility, release, device, FORMAL-R6,
strip, TD-C, sentinel and P8 remain hard locked.

## 维护性判断

The rejection isolates two concrete controller-owned defects without widening
production architecture. The next correction keeps them in one disposable
lifecycle owner because both are prerequisites for a trustworthy retry; it
adds no production owner or parallel execution framework.
