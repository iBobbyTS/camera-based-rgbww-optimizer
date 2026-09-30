# .agent-work 目录结构（2026-09-29 整理后）

按 GUIDE 阶段分组的协作证据记录。本次为**纯移动归档，未删除任何文件**；
Git 中的历史以 rename 形式保留。

| 目录 | 内容 |
|---|---|
| `guide4/` | GUIDE4 Ray R6 history 失败证据 handoff |
| `guide5/` | GUIDE5 strip/Ray history、TD-C 系列 handoff、COLD600/OP120 人工决策、advisor pack 目录。注：`ADVISOR_HANDOFF-20260811-GUIDE5-RAY-FAST-LONG-BRIDGE.md` 与 `.advisor-pack-guide5-ray-bridge-20260811/` 按原决定仍经 `.git/info/exclude` 本地排除，不进 Git |
| `guide6/` | GUIDE6 solver/measurement/LCB handoff、坐标系评审 |
| `guide7/` | GUIDE7 F2 漂移与 scale 稳定性 handoff、f2 局部括界探针派生数据 |
| `guide9/` | GUIDE9 H300 参考诊断 handoff、`EXECUTION_RESULT.md`（GUIDE9 时代执行结果） |
| `guide12/` | GUIDE12 活动阶段状态（`GUIDE12-STATUS-20260929.md`：离线确定性修正 W2割线/新鲜配对/W8单位/原生削顶门、批次计划与预算索引）。Advisor 输入在 `advisor/12/`（不可变） |
| `guide11/` | GUIDE11 全部批次结果（N1/W2–W4/W8+P6/C1–C5）、暂停记录、最终报告与最终包 manifest/ZIP；2026-09-29 审阅补齐包 `GUIDE11-COMPLETE-PROCESSED-EVIDENCE-20260929.zip`（1730 成员，外部校验 pass，说明见 `GUIDE11-COMPLETE-EVIDENCE-EXPORT-20260929.md`，未入 Git） |
| `archived/` `debug/` `evidence/` `plans/` | 原有归档结构，本次未改动 |
| `PLAN.md` `PLAN-FULL.md` | 留在顶层（AGENTS.md 引用的既定路径） |

## 引用换算

- `docs/engineering/p7-td-b-contract-history.md` 中提到的
  `.agent-work/EXECUTION_RESULT.md` 现位于 `guide9/EXECUTION_RESULT.md`。
- 数据盘 `D:/rgbww-optimizer` 同日做了同规则的分组整理，逐条 old→new
  映射见 `D:/rgbww-optimizer/REORG-MAP-20260929.json`；该 README 记录
  历史 manifest/脚本中旧绝对路径的换算规则。
- 移动脚本：仓库 `tmp/reorg_dirs_20260929.py`（幂等续跑，移动前断言
  源存在、目标不存在，并对 GUIDE11 最终包 ZIP 做了移动前后 SHA-256
  一致性校验）。
