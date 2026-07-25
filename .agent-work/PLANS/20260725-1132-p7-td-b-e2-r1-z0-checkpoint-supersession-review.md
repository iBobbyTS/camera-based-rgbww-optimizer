# P7-TD-B-F0B-R1-C3-E2-R1-Z0 checkpoint supersession Planner 归档

**验收时间：** `2026-07-25T11:34:33-0600`

**验收角色：** Planner

**被审 active PLAN SHA-256：**
`b34b4868d8ef8fbfad8a4fe174c8728be206170cd511e643f2b6f0d38e0668a9`

**Planner 决定：** `superseded_before_execution_due_to_documentation_checkpoint_advance`

**精确下一分支：** `P7-TD-B-F0B-R1-C3-E2-R1-Z0-R1_ZERO_ONLY_REACHABILITY`

## 被审范围

被审 PLAN 只放行一次 zero-only hostname/ESPHome reachability gate：先在 fresh external root 运行 no-device
`14/14` matrix，再按五个冻结 semantic stages 对 exact `bedroom-rgbww-strip.local:6053` 各执行一次
generation-bearing 全零调用。它禁止 E2、camera、Ray、capture、formal、非零输出、firmware、deployment、网络配置变更、
stage 和 commit。

该 PLAN 尚未由 Executor 执行；`.agent-work/EXECUTION_RESULT.md` 最新结果仍是已归档接受的 C2 离线纠偏。

## Planner 当前态复核

1. C2 review archive SHA-256 为
   `8bc00632f878041dde21fb03709f248f8e33b6cdf104f3055bdd041752c9b17a`。
2. C2 `validation-summary.json` SHA-256 为
   `a0e0f1ec6027ba6adb7850d5a3cb1a5f8a49ecdf2c69d8e13a0073ded25ec58c`；其 aggregate `239` 仍是
   non-authoritative derived index。
3. C2 11 个有效 case 的 immutable per-case stage totals 求和为 `265`；`terminal-summary.json` 的
   `301` 个 canonical artifacts 逐项 live bytes/SHA-256 replay，mismatch 为 `0`。
4. C2 matrix `14/14`、全部 JSON `296/296` strict parse 的既有结论保持；case 10 的 26 个 stage artifacts 存在并在
   terminal inventory 中。
5. ESPHome production owner SHA-256 仍为
   `37cb552524fa06d04ffde2d4cb2ba12f02b448041bfebe0ec63db9982dc638be`；exact secrets input SHA-256 仍为
   `908cae88a314de3d932286fae7c5a607f34156cdd0c2ee6ea4647e91edc5d8fc`。
6. 原 PLAN 冻结 `HEAD=fa6c95dbf79f4c0828e8633560d2828e3646204b`，但当前 HEAD 为
   `8cd04d847d42ff5c7bcf7501f46be97cbbef429d`。两者之间仅有两个 workflow documentation commits：
   `f92cd47 docs(workflow): add full guide plan reference` 与
   `8cd04d8 docs(workflow): assign roadmap to orchestrator`；累计 changed paths 恰为：
   `.agent-work/FULL_PLAN_REFERENCE.md`、`.agents/skills/camera-based-rgbww-optimizer/SKILL.md`、`AGENTS.md`。
   `src/`、`tests/`、`docs/`、`tmp/`、`firmware/` 和设备 owner 未变。
7. 本 review 未访问网络、`.env`、设备或 hostname，未执行 Z0、cleanup、E2、capture、formal、analyzer、stage、commit
   或 lineage rebuild。

## Finding 与决定

### `REV-Z0-CHECKPOINT-001` — Superseded before execution

原 PLAN 要求 HEAD/frozen evidence 无 drift，却绑定旧 HEAD。按原合同执行只会在 device access 前 deterministic
checkpoint failure，不能取得新的 reachability 证据。该失败不是 C2、设备或科学 finding，因此不应浪费唯一 real Z0。

Planner 将原 PLAN 作为未执行但已 superseded 的合同归档，并重发同一 narrow Z0 工作包，只把 workspace checkpoint
更新为当前文档流程提交。新的 PLAN 必须同时声明：旧 lineage release 仍仅绑定 `fa6c95d`，在 Z0 中只作为冻结历史证据，
不得被解释为对当前 `8cd04d8` 的 E2/formal executable release；任何后续 E2 计划须重新解决 current-checkpoint lineage
compatibility。

## 残余风险与停止点

- hostname/ESPHome reachability 和 generation-bearing strip zero 仍完全未知；C2 不能证明设备状态。
- 新 Z0 仍只能执行一次，pass/fail 都必须回 Planner，不能自动进入 E2 或 formal。
- `FULL_PLAN_REFERENCE.md` 由 Orchestrator 独占修改；本 Planner review 不修改该文件。

精确下一分支仅为：`P7-TD-B-F0B-R1-C3-E2-R1-Z0-R1_ZERO_ONLY_REACHABILITY`。
