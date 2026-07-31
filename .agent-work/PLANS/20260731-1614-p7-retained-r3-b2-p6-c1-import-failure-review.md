# REF-P7-25-R2-B2-P6-C1：domain-template targeted correction review

**计划状态：** REVIEWED_REJECTED_TARGETED_TEST_IMPORT_FAILURE

**Planner 日期：** 2026-07-31

**Reference task：** REF-P7-25-R2-B2-P6-C1

**Contract ID：**
P7-TD-B-RETAINED-R3-OPTION-B-B2-P6-C1-DOMAIN-TEMPLATE-TARGETED-CORRECTION-V1

## 1. Reviewed scope

- Activation：`d8c45f3f3c1b7b7c5b5b2f966118e58deaa0f895`，direct parent
  `957538e491fd94f04e13c20f3020f476e79e384b`，subject exact
  `chore(plan): activate p6 c1 domain template correction`。
- Activation changed paths exact 为 `.agent-work/FULL_PLAN_REFERENCE.md`、`.agent-work/PLAN.md` 与
  `.agent-work/PLANS/20260731-1604-p7-retained-r3-b2-p6-targeted-failure-review.md`。
- Preserved candidate：`73e2f2cc3b9b1465a47381b55360cf941ac0cbc4`，direct parent 为 activation，subject
  `chore(p7): retain rejected p6 c1 template candidate`，changed paths exact 为：
  1. `src/camera_based_rgbww_optimizer/utils/p7_retained_r3_controller_domain_template.py`
  2. `tests/test_p7_retained_r3_controller_domain_template.py`
- Evidence HEAD：`e6520062bb1a60a0686066ccec39c4fb190905c0`，subject
  `chore(evidence): record p6 c1 targeted failure`，changed path exact 为 `.agent-work/EXECUTION_RESULT.md`。
- Review 时 porcelain clean。Active PLAN SHA-256：
  `c9db31fc8122549c8470fed3ed62e8983e60cfc852790267ed3361f25361d34e`；EXECUTION_RESULT SHA-256：
  `86bf8c7cb8b675c1ec87937fdc538d1828dc4ca5b3dba89f9fe17e49d3fb4e11`。

## 2. Reviewed implementation method

P6-C1 的授权范围是修复 P6 candidate 的两个局部合同缺陷，同时保持 P6 owner/API/source shape 不变：

- replacement statement 从 `ACTIVATION_CONTRACT` 的 `A` 开始，leading indentation bytes exact `0`，以 exact 一个 LF 结束；
- `prepare_controller_source` 仍只替换 assignment AST span；
- test 08 从错误的全局 `retained` substring ban 改为 imports、calls、public payload fields 与 generated-runtime
  semantics 的 AST/value inventory；
- exact 八个测试名、18/14/4/7 binding、Git6、single physical root、matrix16、exact9 与 lifecycle inventory保持冻结；
- external controller/root、retained R3/candidate、validator、eligibility、release、network/device/formal 全部锁定为 0。

Candidate 中 production source 已按合同产生 replacement bytes：文件 bytes `13918`、SHA-256
`56d838b6b1e7dd0d68586cb9829d9e328ca8a05c670e08ff047e3324d4b77032`、blob
`a1e196664840bc340be789829b8cf0826c9ec7f4`。Test 08 semantic rewrite也已落盘；test 文件 bytes `12929`、SHA-256
`17a011c8234c0acbad9b3bc3a3f1a26ad13ec9de41d284f4a458a616347fd44c`、blob
`d716f13cb31b26ac151d5b013c8ee989cbbae716`。

## 3. Evidence and validation quality

- Unique fresh targeted command：
  `.venv/bin/python -m unittest tests.test_p7_retained_r3_controller_domain_template`。
- Unified chunk/session：`2d8b33`；exit `1`；exact `Ran 8 tests`；`failures=0`、`errors=1`；七个方法通过。
- 唯一错误：test 08 在读取 public payload fields 时引用 `ControllerRuntimeRequest.__dataclass_fields__`，但 dedicated test
  只从 runtime owner 导入了 `compose_controller_source`，未显式导入 `ControllerRuntimeRequest`，因此触发
  `NameError: name 'ControllerRuntimeRequest' is not defined`。
- 因 retry/fallback `0/0`，Executer未补写 import、未重跑 targeted。Focused90、compileall、full775、CodeGraph、
  implementation acceptance commit 与 postcommit targeted 均为 `0`。
- `git diff --check` 通过；exact two-path scope保持。Planner未把七个通过方法推断为 owner acceptance，也未把未运行的检查报为通过。
- External controller/source/root/evidence create/read/write/process、synthetic integration、retained/candidate read、Git provenance replay、
  real B2、manifest、validator、eligibility、audit/release、network/DNS/environment/credentials、device/camera/Ray/strip/cleanup/capture、
  FORMAL/public analyzer/TD-C/sentinel/P8/firmware/deployment全部 exact `0`。

## 4. Planner findings and decision

**Finding P6-C1-001：dedicated test missing explicit runtime request import。**

Root cause exact 位于 test import boundary：测试使用既有 owner 类型，却没有将其导入当前模块命名空间。该错误发生在 test 08，
不表明 production builder、replacement bytes 或 existing owner API 需要修改；也没有证据支持扩大到 source、runtime、preparation、
conformance、provenance-I/O 或 lifecycle owner。

**Decision：** `REJECTED_TARGETED_TEST_RUNTIME_REQUEST_IMPORT_OMISSION`。

P6-C1 candidate `73e2f2cc3b9b1465a47381b55360cf941ac0cbc4` 保持
`retained_rejected_candidate_non_consumable`。Production zero-indent correction 与 semantic test rewrite可以作为 successor 的冻结 parent state
被重新验证，但该 candidate 本身不能被声称为 accepted/consumable。无需 Advisor、Human、科学分支或设备授权。

## 5. Exact next branch

下一分支必须是单一最小 successor `REF-P7-25-R2-B2-P6-C1-C1`：

- exact write path 只有 `tests/test_p7_retained_r3_controller_domain_template.py`；
- 唯一语义修改是从既有 runtime-owner import 显式导入 `ControllerRuntimeRequest`，保留
  `compose_controller_source`，不得改 production source、测试 body、断言、fixture、expected counts或第三路径；
- 从新 activation HEAD 按顺序运行 fresh targeted8、focused90、compileall source/test、unique full775、CodeGraph sync/query、
  diff/path/method/import gate、single test-only commit与 postcommit targeted8；retry/fallback `0/0`；
- 任一检查失败即 append ER并停在 Planner review，不得修第二次、放宽断言、触发 external/retained/device route；
- 全部通过只证明 P6 domain-template owner 的 composite successor ready for Planner review，不自动授权 synthetic integration、retained
  validation、validator、eligibility、release 或设备工作。

## 6. Residual risks and locks

- Source correction与 test 08 semantic body只有 targeted 七项通过的间接证据；在 focused/full/CodeGraph/postcommit完成前不能验收。
- 新 import 可解除当前 `NameError`，但不能预判后续测试层级；执行必须保持 fresh ordered fail-closed sequence。
- retained R3 继续为 `RETAINED_UNVALIDATED_UNCONSUMED`；candidate/old evidence不可读取或消费。
- Release、network、device、FORMAL-R6、strip、TD-C、sentinel 与 P8保持 locked。

**唯一 Planner stop：**
B2_P6_C1_C1_TEST_IMPORT_CORRECTION_WAITING_PLANNER_REVIEW。
