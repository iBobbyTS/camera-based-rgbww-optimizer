# P7 retained-R3 Option B：B3 terminal self-check 拒绝审查归档

**归档时间：** `2026-08-01 04:16 America/Edmonton`

**Reference task：** `REF-P7-25-R2-B3`

**Reviewed contract：**
`P7-TD-B-RETAINED-R3-OPTION-B-B3-POSTCOMMIT-SELF-CHECK-TEST-SYNTHETIC-V1`

**Reviewed activation：** `ab2b1d1dbf8d1977a154f06d5099e4d66251cfcb`

**Evidence commit：** `8ae390444255d9bfe6082e64b31c25cdd5bdd399`

**Planner decision：**
`REJECTED_EXECUTION_ASSERTION_TERMINAL_PASSED_FIELD_NOT_CONTRACTUAL`

## 1. 审核范围与方法

Planner独立读取active `PLAN.md`、evidence commit新增的physical-EOF payload，以及accepted B2 manifest五件套的exact paths。审核只比较PLAN冻结的terminal/seal/admission合同与实际artifact schema；没有调用canonical lineage validator、retained audit、release或任何network/device/camera/Ray/strip入口，也没有修改真实manifest、C1或retained artifacts。

Reviewed PLAN：bytes `16628`，SHA-256
`ddd24924267c48c4c758b8234eac838f54a97ea19f857be94c8e4dbea9349f50`。

Evidence lineage：

- parent commit `ab2b1d1dbf8d1977a154f06d5099e4d66251cfcb` 的 `EXECUTION_RESULT.md`：bytes `1287476`，SHA-256 `42057a760eabee310927b438f62ae2b8d84975c75c74bfa8bcf5e9b71eff069a`；
- physical EOF suffix：bytes `2785`，SHA-256 `1daa9742fab205c23cd3b4530b69260cac3f5f820166b9d1ad9e364a1aacf085`；
- evidence commit后的 `EXECUTION_RESULT.md`：bytes `1290261`，SHA-256 `24afc1b3876bf6988d8de139b81e2b8f094f8939b788d7ac75c9e4a54fb6cc8e`。

## 2. 实际 artifact schema 与冻结合同

Accepted B2 output root保持immutable。其五件套身份仍是active PLAN冻结的exact bytes/SHA：manifest、manifest seal、terminal、terminal seal与admission。

实际terminal合同为：

```json
{"status":"sealed_subordinate_provenance_evidence"}
```

该对象的exact key set只有`status`；bytes `52`，SHA-256
`b438e5c7cac0ef434205c748a003596d740c155f8b0ff3fa06df5a16f4a17893`。

实际terminal seal合同为：

```json
{"bytes":52,"sha256":"b438e5c7cac0ef434205c748a003596d740c155f8b0ff3fa06df5a16f4a17893","target":"terminal-evidence.json"}
```

seal自身bytes `123`，SHA-256
`d17c4836355406fba95bb2d564692a32ff4b94423ae69e4de8cfe4b542572d75`。

实际admission合同为：

```json
{"admitted":true,"eligibility":false,"release_consumable":false}
```

其exact key set只有`admitted`、`eligibility`、`release_consumable`；bytes `65`，SHA-256
`c43d97963373db7d61066de6ebb7e16e6d915281f1f30861f86e1bd6404d87e9`。

Manifest只冻结schema `p7_retained_r3_audit_provenance_manifest_v2` 与status
`sealed_subordinate_provenance_evidence`，不拥有eligibility判定。

## 3. 执行结果与质量

Executer在一次outer controller内完成activation、repository machine rows、真实manifest source/output、C1 four与retained three physical reads；随后因要求`terminal-evidence.json`顶层`passed=true`而在self-check阶段停止。实际计数：real manifest root `1`、files `5`、source `1`、C1 root/files `1/4`、retained root/files `1/3`、Git reads `5`；focused/full/synthetic均为`0`。Canonical validator、retained audit、eligibility、release、network/device及real artifact writes均为`0`。EOF append为最后side effect，postappend operations `0`。

该fail-closed行为和零锁有效，但失败选择器没有合同依据，因此不能据此认定manifest缺陷，也不能把本轮报为B3验证通过。

## 4. Findings 与决定

`terminal_passed=true`仅出现在此前Planner对B2整体验收的派生事实中；它不是`terminal-evidence.json`的字段。B3 PLAN冻结的是真实五件套身份、terminal schema/status、两条seal绑定和admission三元组，并未授权把派生验收事实反投影成artifact key。

因此本轮为execution assertion错误：

`REJECTED_EXECUTION_ASSERTION_TERMINAL_PASSED_FIELD_NOT_CONTRACTUAL`。

真实B2 manifest不修复、不重写、不再生成；其状态仍为
`ACCEPTED_COMPLETE_SEALED_SUBORDINATE_PROVENANCE_NOT_RETAINED_ELIGIBLE`。Retained R3仍为`RETAINED_UNVALIDATED_UNCONSUMED`。

## 5. Residual risks 与 exact next branch

后继必须是fresh B3 successor，并且：

1. 只核对PLAN明确冻结的terminal exact key/value、terminal seal target/bytes/SHA、admission exact keys/values，以及manifest/source/C1/retained physical identities；
2. 明确禁止要求、搜索或推导任何artifact顶层`passed`字段；self-check pass只能是完成全部冻结检查后的controller派生结果；
3. self-check通过后，仍按focused exact once → full exact once → brand-new synthetic exact once顺序执行；任何一步失败立即停止，后续为零；
4. canonical validator、真实retained audit、eligibility emission、release consumption与全部设备工作继续锁定。

Exact next reference task：`REF-P7-25-R2-B3-C1`。

Exact next contract：
`P7-TD-B-RETAINED-R3-OPTION-B-B3-C1-EXACT-TERMINAL-SCHEMA-SELF-CHECK-TEST-SYNTHETIC-V1`。

维护性判断：无需改production manifest owner或artifact schema；只需收窄一次性B3 controller的验收选择器，并保留既有P3/M1/P5所有权边界。
