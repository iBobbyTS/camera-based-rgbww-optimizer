# REF-P7-25-R2-B1A-C3E6F17-CORRECTIVE-4：C4 qualification review

**Review date:** `2026-07-29`

**Reviewed plan:** `.agent-work/PLAN.md`

**Reviewed execution record:** `.agent-work/EXECUTION_RESULT.md`，`F17 corrective-4 canonical machine-row qualification` section

**Decision:** `REJECTED_C4_CONTRACT_QUALIFICATION`

**Exact next branch:** `REF-P7-25-R2-B1A-C3E6F17-CORRECTIVE-5`

## Reviewed scope and frozen evidence

本轮仅做离线审计；未读取代码、测试、archive、controller、source、candidate、fixture、canonical content、release、retained R3、`.env`、网络或任何设备资源，未进行 Git mutation。

- PLAN raw SHA-256：`fb95192a98dd805e2d5e5ed35a1f14d9648cd79ee904279eaf22208681dfa5c3`
- FULL raw SHA-256：`359e12bdd766a2360a5349dd90dd49119acf2ac800401dcba81e6a41df756c49`
- candidate_count：PLAN `1`（line `15`），FULL `1`（line `21`）
- task binding：PLAN `task_id=REF-P7-25-R2-B1A-C3E6F17-CORRECTIVE-4`，FULL `active_task` exact；`retained_lock=true`，`owner_active_task=true`
- terminal：`FAIL`，qualification `8/12`；artifact/path `0/0`；old-root/retry `0/0`；prohibited calls all `0`；single ER append `1`；HEAD `c4b1a197efdc81015347eb62f31f66c5608a06d6`

## C4 assertion reconciliation

| 失败断言 | 当前行事实 | 分类 | Planner 结论 |
| --- | --- | --- | --- |
| `canonical_wrappers` | 两行虽为反引号包裹，但 C4 未冻结 wrapper 的完整物理定义（行首/行尾、唯一性、禁止正文前缀与空 payload 的组合谓词） | contract 缺字段 | 不能由 Executer 自行补全；C5 必须冻结 exact wrapper predicate |
| `contract_exact` | PLAN JSON 未声明 required-subset、wrapper 定义、zero-budget 字段集合及“无额外字段/谓词”规则；FULL 仅有 owner/status 元数据 | contract 缺字段 | 不是当前值单纯不一致；C5 需冻结可逐键比较的 exact contract |
| `twelve_of_twelve` | C4 只报告 `8/12`，但 12 项键值映射未在 PLAN/FULL 中冻结，故其中 4 项没有可审计的 canonical expected value | 执行器自造/漂移 | 8/12 不能升级为通过；C5 禁止自创 required keys 或通过条件 |
| `zero_budgets` | PLAN 有若干零预算键，但没有冻结完整字段集合；Executer 的 prohibited-call 集合与 PLAN 字段集并非同一 exact object | 命名不一致 + contract 缺字段 | C5 用单一 zero-budget 字段集合和全量 `0` 值逐键比对 |

其余 8 项（两份 raw SHA、两份 candidate count、PLAN/FULL identity、strict types/keys/hash、retained/owner）仅证明输入读取与基础绑定通过，不构成 C4 qualification pass。C4 因 contract 不完备被拒绝；不得重试、复用或触碰旧 F17 root。

## Residual risk and stop

`RETAINED_UNVALIDATED_UNCONSUMED` 保持不变。C5 dispatch 仍须由 Orchestrator 先将 FULL active task/contract 同步为 C5；在同步前 PLAN 仅为待执行 work package。不得进入 bootstrap、controller、R3、release、network 或 device。

