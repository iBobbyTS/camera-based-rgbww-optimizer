# REF-P7-25-R2-B2-M1-R1-S2 machine-row repository-gate review

**Reviewed reference task:** `REF-P7-25-R2-B2-M1-R1-S2`

**Reviewed contract:**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-M1-R1-S2-FRESH-REAL-INPUT-STRICT-RETAINED-NO-TERMINAL-SELECTOR-V1`

**Planner decision:** `REJECTED_EXECUTION_ASSERTION_MACHINE_ROW_CANONICAL_ORDER_NOT_CONTRACTUAL`

**Planner review date:** `2026-08-01 03:28 MDT`

## 1. Immutable repository and execution scope

- Activation `df56622d8ed2963e2cdd76610592c9a55651c1df` is the direct child of
  `fd8bc48694ed7f69fc75af0ebd35f6ed3ad5424d`, has exact subject
  `chore(plan): activate selector-free strict retained successor`, and changes exactly FULL, PLAN, and
  `.agent-work/PLANS/20260801-0311-p7-retained-r3-b2-m1-r1-s1-c1-c1-c1-physical-eof-acceptance-review.md`.
- Evidence commit `82e5a13319642ccf6a584c6bd535094d6ac53a9a` is the direct child of the activation, has exact subject
  `chore(evidence): record S2 repository gate stop`, and changes only `.agent-work/EXECUTION_RESULT.md`.
- The activation archive is bytes `5899`, SHA-256
  `435a57bfeb7dd2a1fa7261e758607fb2650bbb9e256dc152f74036a94b0a5fe6`.
- This review used repository Git objects and current repository documents only. External C1/retained roots,
  fresh namespaces, tests, CodeGraph, controller, validator, release, network, and device surfaces were not accessed.

## 2. Contract interpretation

The active PLAN requires PLAN and FULL to contain exactly one **strict machine row** and requires the frozen FULL
subset to match. It does not require either complete machine JSON byte string to equal a sorted-key canonical
re-encoding, does not freeze top-level or nested key order, and does not name a `machine_row_not_canonical` gate.

Independent review of the activation Git objects found exactly one machine row in each document. Both rows decode as
strict duplicate-free JSON objects, and the Orchestrator activation had already validated the required subset. Both
raw rows differ from a sorted-key compact re-encoding; that fact is not a contract failure because canonical byte
encoding is required for the C1 inputs, generated output artifacts, and the final one-line ER payload where expressly
stated, not for the PLAN/FULL machine-row serialization.

Therefore `machine_row_not_canonical` is a non-contractual Executer assertion. It is not evidence of repository,
Planner, Orchestrator, M1, P3, P5, C1, retained-input, validator, release, or scientific failure. No production or test
repair is required.

## 3. Independent physical-EOF evidence verification

The activation ER is bytes `1252674`, SHA-256
`3203d390d2e0c43da03f40603e651c3bd967f83b2dc0af97950818c678076e3e`. The evidence ER is bytes `1258401`,
SHA-256 `681a5d12f7a5b53c4aa3269475cc009b51893320a1f3a3d41d41175ece3764f9`.

All `1252674` activation bytes are the exact prefix of the evidence ER. The only new suffix is `5727` bytes,
SHA-256 `45eb34ef341f5040ec908292279f45dca07184fa591b633b55ec0718bf5a7dfb`, followed by final LF. It contains exactly
one S2 heading, one fenced one-line JSON payload, and one closing fence. The payload strict-decodes as a duplicate-free
object, is byte-for-byte equal to its sorted compact canonical JSON encoding, and records:

- `result=FAIL` and first failure `repository_gate/machine_row_not_canonical`;
- fresh absence checks, C1/retained acquisition, builder, runtime, controller, output and terminal audit all `0`;
- exactly one outer Python invocation, one physical-EOF apply-patch/ER append, last-side-effect true, and postappend
  operations `0`;
- selector assertions, retry/fallback, tests/CodeGraph, validator/release, network/device/camera/Ray/strip/FORMAL and
  all other hard locks `0`.

The failure payload leaves `activation={}` and `owners={}` because the self-created assertion fired before those
ledgers were populated. This is accurate partial-failure evidence and does not need regeneration or supersession.

## 4. Decision and exact next branch

The S2 scientific/manifest objective is not complete, but its failure lifecycle is accepted as an immutable,
accurate physical-EOF record. Durable classification:

```text
REF-P7-25-R2-B2-M1-R1-S2 =
  REJECTED_EXECUTION_ASSERTION_MACHINE_ROW_CANONICAL_ORDER_NOT_CONTRACTUAL
retained R3 = RETAINED_UNVALIDATED_UNCONSUMED
```

Proceed directly to a brand-new activation-derived fresh successor:

- next reference task `REF-P7-25-R2-B2-M1-R1-S2-S1`;
- contract
  `P7-TD-B-RETAINED-R3-OPTION-B-B2-M1-R1-S2-S1-FRESH-REAL-INPUT-STRICT-MACHINE-ROW-NO-CANONICAL-ORDER-V1`;
- repository gate checks exact activation topology, clean porcelain, exact one strict duplicate-free object machine row
  in PLAN/FULL, and the frozen required FULL subset only;
- complete machine-row canonical re-encode, sorted-key equality, key-order assertions, or an equivalent generic
  canonical byte gate are explicitly prohibited;
- use a brand-new S2-S1 source/output namespace; the failed S2 namespace remains immutable and no-read/no-stat/no-list/
  no-glob/no-search/no-reuse/no-modify/no-delete;
- preserve the same exact C1 physical/canonical boundary, retained physical/strict boundary, accepted M1/P3/P5 owners,
  single builder/runtime/controller lifecycle, zero selectors, and physical-EOF partial-or-success append.

Planner stop:
`B2_M1_R1_S2_S1_FRESH_REAL_INPUT_STRICT_MACHINE_ROW_WAITING_PLANNER_REVIEW`.

## 5. Residual locks and maintainability

Canonical validator, eligibility emission, retained-release audit, release generation/qualification/copy/consumption,
network, DNS, environment, credentials, device, camera, Ray, strip, cleanup, capture, FORMAL, public analyzer, TD-C,
sentinel, P8, firmware, and deployment remain locked. The successor remains pure offline read-only existing inputs plus
new evidence output and requires neither Human device authorization nor Advisor scientific direction.

维护性判断：本次只移除执行脚本自建的 serialization gate，并把准入边界明确收敛为 strict decode + frozen subset；继续复用既有 P3/M1/P5 owner，
不新增 parser、helper、validator、runner 或平行 evidence framework，无需架构重构。
