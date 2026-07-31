# REF-P7-25-R2-B2-P6-C1-C1：generated-source static allowlist failure review

**计划状态：** REVIEWED_REJECTED_GENERATED_CALL_ALLOWLIST_GAP

**Planner 日期：** 2026-07-31

**Reference task：** REF-P7-25-R2-B2-P6-C1-C1

**Contract ID：** P7-TD-B-RETAINED-R3-OPTION-B-B2-P6-C1-C1-TEST-RUNTIME-REQUEST-IMPORT-CORRECTION-V1

## 1. Reviewed scope

- Activation：`3b7a95f0fec746276aa8933a375738ffde2bb348`，direct parent
  `e6520062bb1a60a0686066ccec39c4fb190905c0`，subject exact
  `chore(plan): activate p6 c1 c1 test import correction`。
- Activation changed paths exact 为 `.agent-work/FULL_PLAN_REFERENCE.md`、`.agent-work/PLAN.md` 与
  `.agent-work/PLANS/20260731-1614-p7-retained-r3-b2-p6-c1-import-failure-review.md`。
- Preserved candidate：`66532b5adef27de3c7839c5a7c783ebd7a053d38`，direct parent 为 activation，subject
  `chore(p7): retain rejected p6 c1 c1 import candidate`，changed path exact 为
  `tests/test_p7_retained_r3_controller_domain_template.py`。
- Evidence HEAD：`0b704f535f3653429f527abec99f54c4c48d798a`，direct parent 为 candidate，subject
  `chore(evidence): record p6 c1 c1 targeted failure`，changed path exact 为 `.agent-work/EXECUTION_RESULT.md`。
- Review时 porcelain clean。Reviewed PLAN SHA-256：
  `0390dc16621ce9ca72f95300074f12289c037923bcdf82bb2a5e5bc67ecda5c5`；EXECUTION_RESULT SHA-256：
  `fdd04835090428fc3f1831c3fb224a1e0b0cc2fa750ba940b951d22ea3d0f615`。

## 2. Reviewed implementation and evidence

Candidate只修改 dedicated test 的既有 runtime-owner import，显式加入 `ControllerRuntimeRequest` 并保留
`compose_controller_source`。Diff中无 alias、wildcard、动态/test-local import、test-body或 production-source修改。

唯一 fresh targeted invocation 使用 unified chunk/session `21bc05`，exit `1`，exact `Ran 8 tests in 0.028s`，
七项通过、`failures=1`、`errors=0`。Test08 已越过旧 `NameError`，唯一 failure 是 generated-source inventory报告
`unexpected_call:RuntimeError` 与 `unexpected_call:type`。按 retry/fallback `0/0`，focused90、compileall、full775、
CodeGraph、implementation acceptance commit与 postcommit targeted均为 `0`。External/retained/validator/release/network/device及所有
科学执行预算均为 `0`。

Production source保持 blob `a1e196664840bc340be789829b8cf0826c9ec7f4`、bytes `13918`、SHA-256
`56d838b6b1e7dd0d68586cb9829d9e328ca8a05c670e08ff047e3324d4b77032`。Import-only test candidate为 blob
`ea737487e549758bb5f37c46a444cdf880b32d0f`、bytes `12968`、SHA-256
`0fdad3f746d8f1e206897c1951c805fb6d4aa1f25e1d0a54cd6cb305f8403f0e`。

## 3. Independent static finding

**Finding P6-C1-C1-001：test08 generated-call expected set遗漏 canonical activation gate 的两个必要 builtin call。**

Current canonical template 的 `require_activation_contract(value)` 在 generated source中精确包含：

1. `type(value) is not tuple`：对 activation contract执行 exact-type fail-closed判定，避免将任意非精确 tuple值作为冻结合同接受；
2. `raise RuntimeError("activation_contract_invalid")`：当类型不符或值为空时，以稳定码在任何 Git/root/input effect前 hard fail。

`compose_controller_source` 只调用 accepted preparation owner替换 assignment span并返回 composed bytes；它不会向 generated source新增
`RuntimeError` 或 `type` call。当前 targeted failure的 exact two-call差集因此来自上述 canonical gate，而非 validator、eligibility、release、
network/device或新增 effect owner。证据只支持把 exact names `RuntimeError` 与 `type` 加入 test08 的 `generated_calls` expected set；不支持 generic
allowlist、prefix/pattern match、从实际 inventory动态派生 expected set，或放宽其他 import/call/payload边界。

## 4. Planner decision

**Decision：** `REJECTED_TARGETED_GENERATED_RUNTIME_ERROR_AND_TYPE_CALL_ALLOWLIST_GAP`。

Candidate `66532b5adef27de3c7839c5a7c783ebd7a053d38` 保持 rejected/non-consumable。Import correction是必要且应由 successor
冻结保留，但 targeted不是 `8/8`，不能把 candidate、P6 owner或任何后续 integration报为 accepted。该问题是单一 test expectation缺口，
无需 Advisor、Human、production source或架构重构。

## 5. Exact next branch

下一分支为唯一 bounded successor `REF-P7-25-R2-B2-P6-C1-C1-C1`：

- exact write path只有 `tests/test_p7_retained_r3_controller_domain_template.py`；
- 唯一允许修改 test08 的 `generated_calls` set，加入 exact `RuntimeError` 与 `type`；
- 保留 import correction、其余 generated call names、所有其他 test body、八个 test names与 production source；禁止 generic/dynamic allowlist；
- fresh ordered targeted8、focused90、compileall、unique full775、CodeGraph、diff/exact-AST gates、single test-only commit与 postcommit targeted8；
  retry/fallback `0/0`；
- 任一失败即唯一 ER append并停在 Planner review，不得同包继续修复或触发 external/retained/device route。

## 6. Residual risks and locks

这次静态判定只证明 exact expected-set correction有源码根据，不能预判 focused/full通过，也不能授权 synthetic integration。Retained R3继续为
`RETAINED_UNVALIDATED_UNCONSUMED`；所有 old evidence、retained/candidate、validator/eligibility/release、network/device/FORMAL及后续阶段锁定。

**唯一 Planner stop：** B2_P6_C1_C1_C1_GENERATED_CALL_ALLOWLIST_CORRECTION_WAITING_PLANNER_REVIEW。
