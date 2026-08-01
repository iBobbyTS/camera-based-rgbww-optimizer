# P7 retained-R3 Option B：M1-R1-S2-S1 machine-row delimiter review

**Planner review date:** `2026-08-01`

**Reviewed reference task:** `REF-P7-25-R2-B2-M1-R1-S2-S1`

**Reviewed contract:**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-M1-R1-S2-S1-FRESH-REAL-INPUT-STRICT-MACHINE-ROW-NO-CANONICAL-ORDER-V1`

**Activation:** `9bd9d5a20583209ab1dbecd18065e9350da7e927`

**Evidence commit:** `30a5e97897b734499a6ec4a61cbb79f2d814b895`

**Decision:** `REJECTED_EXECUTION_ASSERTION_MARKDOWN_DELIMITER_NOT_CONTRACTUAL`

## 1. Reviewed scope and implementation method

S2-S1 was authorized as one fresh real-input manifest-only integration. Its repository gate was limited to exactly one PLAN machine row and exactly one FULL machine row, strict UTF-8 JSON object parsing with duplicate-key rejection, and equality of the frozen required FULL subset. The contract explicitly prohibited whole-row canonical re-encoding, sorted-key equality, key-order assertions, generic canonical-byte gates, and unversioned semantic selectors.

The active PLAN stores the machine contract as one Markdown inline-code row with the exact lexical shape
`` `PLAN_MACHINE_CONTRACT={...}` ``. FULL uses the corresponding exact shape
`` `FULL_PLAN_MACHINE_STATE={...}` ``. The JSON payload is the byte range after the first `=` and before the final single backtick. The Markdown delimiter is not part of the JSON payload.

The Executer instead counted lines beginning with the bare prefix `PLAN_MACHINE_CONTRACT=`. Because the only valid row begins with a single backtick, that implementation produced `PLAN_MACHINE_CONTRACT=row_count` before any external access.

## 2. Evidence and independent validation

- Activation topology: `9bd9d5a...` has parent `82e5a133...`, subject `chore(plan): activate strict-machine-row real input successor`, and the frozen exact three changed paths.
- Evidence topology: `30a5e978...` has parent `9bd9d5a...`, subject `chore(evidence): record S2-S1 machine row delimiter stop`, and changes only `.agent-work/EXECUTION_RESULT.md`.
- Activation ER prefix: bytes `1258401`, SHA-256 `681a5d12f7a5b53c4aa3269475cc009b51893320a1f3a3d41d41175ece3764f9`.
- Physical EOF suffix: bytes `7863`, SHA-256 `5976712ef800c85f65e5eae8db6bd4eb80fcc9df3a66d14007b6f9330cf75187`.
- Evidence ER: bytes `1266264`, SHA-256 `ddd34c672984309c954d19e5028327ce936f7f0182283121000a22cbb8d3763a`.
- PLAN machine row: quoted-row count `1`, bare-prefix count `0`; strict UTF-8 object parse and duplicate-key rejection pass.
- FULL machine row: quoted-row count `1`, bare-prefix count `0`; strict UTF-8 object parse and duplicate-key rejection pass.
- The S2-S1 handoff reports physical-EOF append `1`, apply-patch `1`, postappend operations `0`, and the frozen activation/owner identities.
- External/fresh/acquisition/builder/runtime/controller operations are all `0`; retry and fallback are `0`.
- No code, test, production helper, validator, release, network, device, camera, Ray, strip, cleanup, FORMAL, public-analyzer, TD-C, sentinel, or P8 work occurred.

## 3. Planner findings

1. `PLAN_MACHINE_CONTRACT=row_count` is an Executer extraction defect. It does not show malformed PLAN/FULL JSON, a duplicate machine row, or a production owner defect.
2. The prior contract specified the semantic machine-row requirements but did not freeze the Markdown delimiter/extraction algorithm explicitly enough to prevent the Executer from inventing a bare-prefix scanner.
3. The physical-EOF failure handoff is valid and independently reproducible from committed bytes. No Git/ER supersession is required.
4. The fresh S2-S1 namespace was never probed or created, so it remains unconsumed, but a successor must derive a brand-new namespace from a new activation rather than reuse it.
5. The failure occurred before the exact-two absence gate and all external acquisition; retained R3 remains `RETAINED_UNVALIDATED_UNCONSUMED`.

## 4. Exact next branch

Create one fresh successor `REF-P7-25-R2-B2-M1-R1-S2-S1-C1` with a new activation derived from evidence commit `30a5e978...`.

The repository gate must use only these exact extraction semantics for each file:

1. Decode the complete repository file as strict UTF-8.
2. Split with `str.splitlines()`.
3. Select lines satisfying both `line.startswith("`<KEY>=")` and `line.endswith("`")`, where `<KEY>` is exactly `PLAN_MACHINE_CONTRACT` or `FULL_PLAN_MACHINE_STATE`.
4. Require exactly one selected line for each key.
5. Extract bytes/text only from immediately after the exact prefix `` `<KEY>= `` through immediately before the one final backtick.
6. Strict-parse only that extracted JSON payload as an object, rejecting duplicate keys and non-finite constants.
7. Compare only the frozen required FULL subset.

The successor must not use a bare-prefix row scanner, regex/generic fence scanner, whole-file or whole-object search, fallback extraction, canonical re-encoding, sorted-key equality, top-level/nested key-order gate, or any generic canonical-order assertion.

After that gate, retain the same exact-two fresh absence gate, C1 exact physical identity plus canonical decode, retained exact physical identity plus strict JSON, accepted M1/P5 single execution, pre-append audit, physical-EOF single append, retry `0`, fallback `0`, and all existing hard locks.

## 5. Residual risks and stop point

- The successor still performs one bounded offline read of the frozen C1/retained inputs and may fail on any exact identity/decode/runtime/audit condition.
- A valid subordinate manifest remains non-eligibility evidence only. The canonical validator remains the sole eligibility owner.
- Release consumption, retained-R3 audit, device work, FORMAL-R6, strip, TD-C, sentinel, and P8 remain locked.
- No Human device authorization or Advisor scientific decision is needed for this offline engineering successor.

**Next Planner stop:**
`B2_M1_R1_S2_S1_C1_FRESH_REAL_INPUT_EXACT_DELIMITER_WAITING_PLANNER_REVIEW`.

维护性判断：本次仅收紧 PLAN 的 Markdown machine-row 提取合同；不新增生产 helper、通用 scanner、canonical-order owner 或并行证据框架。
