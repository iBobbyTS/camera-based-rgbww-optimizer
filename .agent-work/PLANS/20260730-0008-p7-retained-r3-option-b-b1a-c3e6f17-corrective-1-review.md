# REF-P7-25-R2-B1A-C3E6F17-CORRECTIVE-1：marker/strict-JSON qualification review

**Review date:** `2026-07-30`

**Reviewed plan:** `.agent-work/PLAN.md`

**Reviewed execution record:** `.agent-work/EXECUTION_RESULT.md`，`## F17 corrective qualification`

**Decision:** `REJECTED_CONTRACT_FIELD_BINDING_MISMATCH`

**Exact next branch:** `REF-P7-25-R2-B1A-C3E6F17-CORRECTIVE-2`

## Reviewed scope and frozen evidence

本次仅审阅当前 PLAN、FULL、EXECUTION_RESULT 的 F17 段及既有归档；未读取代码、测试、controller、candidate、fixture、canonical content、release、retained R3、`.env`，未访问网络、相机、Ray120c、strip 或任何设备，也未进行 Git mutation。

- Executer 报告的 PLAN raw SHA-256：`31c192d361214dd1dca55e32c320f6711afb78d960deb0fac6e7ca32a102f62d`。
- Executer 报告的 FULL raw SHA-256：`c352bb8e07238df36a0204ee613bbec72b58bf1445d1938e1035736d401d3a86`。
- marker extraction：PLAN line 17、FULL line 21 均 `ok=true`；`strict_json=true`。
- terminal：`FAIL`；`strict_json_rejection_ledger=[{"error":"task_id","stage":"marker/strict-json"}]`。
- artifact/path counters：`0/0`；old-root touch `0`；retry `0`；禁止调用全部为 `0`；仅单次 ER append；未创建 artifact。

## Planner findings and validation quality

现行 PLAN machine contract 的 identity 字段为 `reference_task_id`，但 qualification contract 的 required schema 绑定 canonical 字段 `task_id`；FULL 使用 `active_task`，执行结果也以 `task_id` 记录，三者未被同一字段语义绑定。故 marker 提取成功不能抵消 strict-JSON required-key mismatch，首次失败明确发生在 `marker/strict-json`，不是 path/bootstrap 或实现阶段。

验证质量为离线 pre-path contract rejection：零 artifact/path 计数只证明未发生副作用，不能升级为整体通过或 bootstrap evidence。`RETAINED_UNVALIDATED_UNCONSUMED` 保持不变；本 FAIL 不授权 bootstrap、controller、R3、release、网络或设备。

## Residual risk and stop

在 canonical task identity 字段及 PLAN/FULL loader 绑定重新冻结前，无法证明 qualification contract 可被一致解析。旧 F17 root 与其四条路径不得检查、创建、复用、修复或重试。

## Exact next branch

下一 active PLAN 只允许一次纯离线 marker/strict-JSON qualification：将 `task_id` 明确定义为 PLAN contract 与 execution evidence 的 canonical identity，FULL 的 `active_task` 只作为与该 identity 的显式等值约束；拒绝 `reference_task_id` 或 `PLAN_MACHINE_STATE=` 作为隐式 alias。仍须在任何 path operation 前 terminal，artifact/path/test/Git/device/release/network/`.env`/camera/Ray/strip 全为 `0`，仅允许一次 ER append 后 stop。
