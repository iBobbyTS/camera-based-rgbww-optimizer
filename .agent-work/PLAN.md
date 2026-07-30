# REF-P7-25-R2-B1A-C3E6F17-CORRECTIVE-13：exact scanner owner 工程激活门

**计划状态：** `planner_stop_waiting_for_orchestrator_engineering_activation`

**Planner 日期：** `2026-07-30`

**Reference task：** `REF-P7-25-R2-B1A-C3E6F17-CORRECTIVE-13`

**Parent reviewed task：** `REF-P7-25-R2-B1A-C3E6F17-CORRECTIVE-12`

**Proposed active_plan_contract_id：** `P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F17-CORRECTIVE-13`

**C12 review archive：** `.agent-work/PLANS/20260730-0153-p7-retained-r3-option-b-b1a-c3e6f17-corrective-12-review.md`；SHA-256 `c85655587e8b895d1a14170de38f4a75e69f8158254906b640bfd58e888e2eec`。

## 唯一 current package：Orchestrator 工程范围确认

C11/C12 已连续由临时手工 scanner 把真实的唯一 PLAN/FULL machine row 误报为 `0`。本 PLAN 不再授权 Executer 重抄或运行 scanner。唯一当前动作是由 Orchestrator 确认 C13 的最小工程范围，并把 `.agent-work/FULL_PLAN_REFERENCE.md` 唯一激活为 C13；完成前不得 dispatch Executer。

Orchestrator 应冻结以下工程决策：

- exact changed-path set：建议仅一个 repository helper module 与一个 dedicated test；具体两条路径由 Orchestrator 确认，不得使用 generic path allowlist；
- 单一 validation-only owner：纯 bytes 输入，按 exact marker、backtick+LF suffix、无 CRLF、`json.loads` object 与唯一候选规则返回 parsed object 及可重放 evidence；不得读取或修复 old/new payload，不得成为 eligibility owner；
- dedicated tests 至少覆盖合法 LF row、CRLF、EOF 无 LF、重复候选、错误 prefix/suffix、非-object JSON、PLAN/FULL owner 分离与 JSON value/type；
- Executer 后续 evidence 必须绑定 exact helper/test paths、before/after blob identity、source SHA、test command/result 与实际 raw-row SHA，不再依赖手工 scanner source 转录；
- canonical lineage validator 仍是 sole eligibility owner，retained R3 保持 `RETAINED_UNVALIDATED_UNCONSUMED`。

## 当前硬锁

- Executer dispatch、source edit、test execution、Git mutation、artifact/path operation、old-root/candidate/retained-R3/release/controller、network、`.env`、device、camera、Ray、strip、formal、public analyzer：全部锁定。
- 本门不授权 bootstrap、real retained-R3 audit、release consumption 或 eligibility emission。
- Orchestrator 激活后，Planner 必须重新读取 exact FULL SHA 与工程范围，只签发一个 bounded helper+test implementation package；不得把本 gate 当作执行授权。

**Planner stop：** 立即停在 Orchestrator activation/工程范围确认门；不得 dispatch Executer。
