# Planner Review：P7-TD-B-Z0-R4 fresh zero-only reachability hard failure

审查日期：2026-07-26

## 审查范围

本归档审查 active `P7-TD-B-Z0-R4` 与 Executor 在以下 fresh root 的唯一执行结果：

`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-e2-r1-z0-r4/20260726T030222Z/`

本审查为只读离线验收；未访问设备、网络、hostname、`.env`，未重试，也未进入 E2/formal。

## 结果与证据

- self-check `1` 次；real wrapper `0`；retry `0`；hostname/network/device/production calls `0`。
- `wrapper-binding-selfcheck.json` status=`pass`，实际 SHA-256 `6dae6aea4d0ad11fe0d589065487ded54148d02ee84d931e494b20d03bcd6f9f`。
- `event-binding-selfcheck.json` status=`fail`，实际 SHA-256 `639a7ff74b75e350bea56895594f51a93ed2d2217ce2244356a31affb60b2f87`。
- 失败根因：fake binding 的 `r4_binding_metadata()` 引用未定义 `EXPECTED_SECRETS`，在首个 `adapter_secret_identity_read_attempted` 事件后抛出 `NameError`；success、load-failure、downstream-failure、partial-persistence rows 未完成预期事件矩阵。
- `pre-device-failure.json` 实际 SHA-256 `fee4daa7e56b028d3ce83cc6fdefb0e0d987b1696cbfa9f70e8e479c79514964`，状态 `hard_failure_waiting_for_planner`。
- failure 分支已落盘 `zero-budget-audit.json`、`terminal-seal.json`，driver 尾部再次 seal 因 `FileExistsError` 退出；`driver-failure.json` 实际 SHA-256 `19cdeb94dde1e66ee015ddac84a82778c172a569142b4a739659256ed3195bcf`。
- 磁盘实际 `post-execution-audit.json` SHA-256 `31d297355f840d40a138d8c3b331515591040c1f284ab36831aeff8801fc7b5c`；第66节交接中记录的 event-binding/post-audit 哈希与实际文件不一致，故本次交接哈希字段不接受为证据。
- root 内 10 个 JSON 均严格解析；post audit mismatch/drift 为空，owned residual process 为空；这些只证明 pre-device failure 的清理状态，不构成 Z0 可达性证据。

## Planner 决策

**拒绝 `P7-TD-B-Z0-R4`，不接受进入 real wrapper、E2 或 formal。** 本次只达到 pre-device hard-fail，不能证明设备可达性或任何 zero stage 成功。

冻结 findings：

1. `REV-Z0-R4-EVENT-BINDING-016` — fake binding 的 `EXPECTED_SECRETS` owner 缺失，导致事件矩阵在首事件后提前失败；必须由单一 binding owner 明确定义并覆盖 success、load failure、downstream failure、partial persistence 全部 progressive prefix/expected outcome。
2. `REV-Z0-R4-FAILURE-SEAL-017` — self-check failure 分支已写 seal/budget 后，driver 尾部再次写入同名 artifacts，触发 `FileExistsError`；必须实现一次性、幂等且可验证的 failure seal orchestration。
3. `REV-Z0-R4-EVIDENCE-HASH-018` — EXECUTION_RESULT 第66节记录的 event-binding/post-audit SHA 与 fresh root 实际文件不一致；必须由磁盘重算并在 handoff/validation index 中原子记录，禁止 stale hash 交接。

## 精确下一分支

`P7-TD-B-Z0-R4-C1_OFFLINE_BINDING_AND_FAILURE_SEAL_CORRECTION`

下一包只能是新的纯离线 corrective package：修复 R4 harness 的 `EXPECTED_SECRETS` owner、完整 event-binding matrix、failure-seal 幂等性，以及 evidence hash 原子生成/校验；冻结 C5 source、production owner、adapter、wrapper、科学合同和所有真实执行预算。纠偏包通过 Planner 验收前，不得执行 hostname probe、real wrapper、设备、E2、formal 或任何 retry。

维护性判断：问题局限于新增 R4 离线 harness 的常量绑定、failure seal 控制流和 evidence bookkeeping；未触及生产 owner、设备路径或科学合同。保持单一 event-binding/seal owner并补充回归矩阵即可，无需架构重构。
