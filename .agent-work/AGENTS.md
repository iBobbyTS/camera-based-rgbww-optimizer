# `.agent-work` scoped orchestration rules

本文件只治理 `.agent-work/` 下的计划、执行结果与归档文件。它记录 Human 于
2026-08-02 明确要求的 current/history 分离规则；对于 `.agent-work/` 内的文件，
本文件中的归档位置与内容规则覆盖根 `AGENTS.md` 中旧的 `.agent-work/PLANS/`
归档位置。其他角色、安全、设备授权、GUIDE 与 Git 规则继续继承根 `AGENTS.md`。

## Live documents

- `.agent-work/FULL_PLAN_REFERENCE.md` 由 Orchestrator 独占维护，只记录接下来仍需
  执行的全部 unfinished reference tasks、当前任务所需的最小 frozen prerequisites，
  以及仍适用的 safety/authorization locks。
- FULL 不得保留 completed、rejected、superseded 或 already-reviewed task表、corrective
  history、旧 handoff ledger、完成实现叙述或重复 evidence log。
- 当前未完成 task 确实依赖的已完成事实，只能以 compact immutable prerequisite 或
  archive path/bytes/SHA pointer 的形式保留；不得把完整历史复制回 FULL。
- `.agent-work/PLAN.md` 由 Planner 独占维护，只能包含一个当前 executable package，
  或一个明确的 non-executable wait/stop。Planner review 后，旧 package 必须先归档再
  从 PLAN 移除。
- `.agent-work/EXECUTION_RESULT.md` 只保存当前 Executer handoff。Executer不得修改、
  归档或重命名 PLAN/FULL；Planner/Orchestrator 按下述规则轮换已完成 handoff。

## Archive directory and filename

- 所有新 plan-family archive 都写入 `.agent-work/archived/`。
- 文件名必须精确使用 `{PLAN类型}-YYYYMMDD-HHMM.md`。
- `{PLAN类型}` 是稳定的大写 source-document type，只允许：
  `PLAN`、`FULL_PLAN_REFERENCE`、`EXECUTION_RESULT`、`AUDIT_PACK`。
- 示例：`PLAN-20260802-1038.md`、
  `FULL_PLAN_REFERENCE-20260802-1038.md`。
- 同一 PLAN 类型在同一分钟最多创建一个 archive。不得覆盖；若同分钟需要第二个，
  等到下一分钟生成新文件，不得追加无治理 suffix。
- 旧 `.agent-work/PLANS/` 是 immutable legacy archive。不得仅为采用新规则而移动、
  重命名、合并、删除或改写其中任何文件；从本规则生效后不再向该目录创建新 archive。

## Archive contract

每个新 archive 必须记录：

1. archive status 与 timestamp；
2. source owner/type、适用 task 或 reviewed scope；
3. source commit/checkpoint（存在时）；
4. 原始 bytes 与 SHA-256；
5. terminal disposition、evidence/index pointers；
6. exact next branch 或 stop；
7. 明确的 `historical_non_executable` 声明。

Archive 不授权 execution、device、release、retry、stage entry、budget 或 commit。
Archive 创建后 immutable；后续更正必须创建新 timestamp archive并引用被 supersede 的
旧 archive，不得原地修改历史正文。

## Archive-before-rewrite sequence

1. 在修改 live owner document 前，先按命名规则冻结待归档内容。
2. 验证 archive path、regular-file identity、bytes、SHA-256、Markdown结构和
   non-executable声明。
3. 只有归档验证通过后，才从 live document 删除 completed/rejected/superseded内容。
4. 将 live document 重写为唯一 next work，并更新 archive pointer 与 machine row。
5. 使用 repo-owned parser验证 PLAN/FULL machine contract，执行全文 task-bearing active
   scan、`git diff --check` 与适用测试。
6. 若任一归档或验证步骤失败，停止；不得留下已删除历史但没有可验证 archive 的状态。

## Role-specific archive actions

- Orchestrator：当 FULL 中任一 task取得 terminal disposition时，先归档完整 pre-rewrite
  FULL snapshot为 `FULL_PLAN_REFERENCE-YYYYMMDD-HHMM.md`，再从 live FULL移除该task
  的完成叙述并只保留 unfinished route。
- Planner：每次接受、拒绝或分支 Executer结果时，先将 reviewed PLAN归档为
  `PLAN-YYYYMMDD-HHMM.md`，再把 live PLAN重写为唯一 next package或明确stop。
- Planner/Orchestrator：轮换已完成 `EXECUTION_RESULT.md` 前，先归档为
  `EXECUTION_RESULT-YYYYMMDD-HHMM.md`；不得把完整ER历史复制进FULL或PLAN。
- Planner：stage结束时的Advisor材料归档为 `AUDIT_PACK-YYYYMMDD-HHMM.md`。

## Initial migration anchor

- 拆分前完整 FULL snapshot：
  `.agent-work/archived/FULL_PLAN_REFERENCE-20260802-1038.md`。
- Snapshot source commit：`805ee6b27da3ac757b84d85941a4ddc967feedeb`。
- 原始正文：`485726` bytes；SHA-256
  `1da4291a1ecab3285d9136d4019bdce3e3f9e3fe419c2ee55b38603f53151fe7`。
- 该 snapshot 只用于历史取证；当前任务选择只能读取 live
  `.agent-work/FULL_PLAN_REFERENCE.md`。
