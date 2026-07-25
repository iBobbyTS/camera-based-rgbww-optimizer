# P7-TD-B-F0B-R1-C3-E2-R1-Z0-R1 pre-device hard-failure Planner 验收归档

**验收时间：** `2026-07-25T11:48:23-0600`

**验收角色：** Planner

**被审 active PLAN SHA-256：**
`3b7abe5e06013e29a2e65608137177d618dc51485c54965895a4fc41f2fe5f56`

**Planner 决定：** `accepted_as_valid_pre_device_hard_failure; z0_not_started`

**精确下一分支：** `P7-TD-B-F0B-R1-C3-E2-R1-Z0-R1-C1_OFFLINE_PLAN_IDENTITY_AND_WRAPPER_CORRECTION`

## 被审范围与结果

被审 PLAN 只放行一个 fresh Z0 external package：先冻结输入并运行 no-device matrix，全部通过后才可运行一次 exact
zero-only ESPHome wrapper。Executor 创建了唯一 root：

`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-e2-r1-z0/20260725T173840Z`

package 在 frozen-input gate fail closed。external `source/run_z0.py` 把 active PLAN expected bytes 手工写成
`3_000_000`，实际 PLAN 为 `12933` bytes；同一 source 中 PLAN SHA-256
`3b7abe5e06013e29a2e65608137177d618dc51485c54965895a4fc41f2fe5f56` 正确。因该错误，matrix、production import、
secrets read、hostname/network/device 和 real wrapper 均未开始。

## Canonical evidence

| evidence | bytes | SHA-256 |
| --- | ---: | --- |
| `validation-summary.json` | 2981 | `abbb92b922ebc145bebb60734ba05f884325d037a6129e87febeced6f14d38d0` |
| `frozen-inputs/before.json` | 4203 | `50bdb258bc351c2eae74ca841de8b1292ecc4daea2833662ff827c2d08cd52a4` |
| `source-manifest.json` | 553 | `22b276fb40d7eae79a4e617dd6ec63319a93a0f0fea9438f4bdbc03e5c28e665` |
| `pre-device-hard-failure.json` | 158 | `d94533b3185900eeae3cd961529cfdb4657178917fc8eb251a565ae93154a641` |
| `terminal-summary.json` | 1545 | `e19229567e37993cd36761f7c781862e7b2d60e12a2885318a99365fe5dde45f` |
| `terminal-metadata.json` | 549 | `c2376511a84a38cae3937b64f8fece1cc92f889b444bc80e9edfdf51826a08c0` |
| `.agent-work/EXECUTION_RESULT.md` at review | 148535 | `cbbe2bdce0c4e683f82d3bdb5da170238f42904af44ac92161e1f4fa464418bf` |

## Planner 独立重放

1. Z0 root、`source/` 和 `frozen-inputs/` 均为普通目录；tree 中恰有 8 个普通文件、symlink `0`。
2. source manifest 的两个 source live bytes/SHA-256 均匹配。terminal summary 的 6 个 canonical artifacts live replay
   `6/6`，mismatch `0`；6 个 JSON 均 strict parse。
3. source 第 38 行明确包含 `FROZEN["plan"] = (PLAN, 3_000_000, exact_sha)`；实际 active PLAN bytes/hash 为
   `12933` / `3b7abe5e...fe5f56`，因此 `plan:drift` 完全由错误 bytes literal 触发。
4. `prepare()` 先写 frozen/source evidence，在 `before.status != pass` 时写 hard failure 并返回；matrix 调用位于其后，
   production ESPHome import 又位于 real worker 中。因此本次控制流不可能到达 matrix、import、secrets 或 device。
5. frozen HEAD 为 `8cd04d847d42ff5c7bcf7501f46be97cbbef429d`；checkpoint changed paths 恰为
   `.agent-work/FULL_PLAN_REFERENCE.md`、`.agents/skills/camera-based-rgbww-optimizer/SKILL.md`、`AGENTS.md`；
   production-scope staged/unstaged diff 为空。
6. count proof 的 explicit/per-stage/sealed 均为 `0`，只证明没有 real stage 消费，不是 Z0 pass。
7. 本次 Planner review 未访问网络、`.env`、device、hostname 或 secrets 内容，未执行 correction、matrix、Z0、cleanup、
   E2、capture、formal、analyzer、stage、commit 或 release rebuild。

## Findings 与处置

### `REV-Z0-R1-PLAN-ID-001` — Accepted failure / correction required

PLAN bytes/hash 被手工双录进一次性 source；PLAN rewrite 后容易产生录入错误，且 bytes 并未增加独立真实性。下一 source
不得再包含手填 `expected_plan_bytes` 或手填 current PLAN hash。应由单一 plan-identity owner 通过 no-follow fd 机械读取、
记录实际 bytes/SHA-256/inode/device 与稳定 contract markers，再由独立 pre-device validator 重放并 fail closed。

### `REV-Z0-R1-WRAPPER-SIGNAL-002` — Newly found / correction required

冻结 source 的 wrapper 对 INT/TERM/HUP 全部 `exit 128`，且没有持久化 exact signal name/code；这不足以满足 wrapper
signal evidence 与 `128+n` 退出语义。虽然本 run 未启动 wrapper，下一 real Z0 前必须离线纠正并覆盖
`INT=130 / TERM=143 / HUP=129`。

### `REV-Z0-R1-MATRIX-003` — Newly found / correction required

冻结 `run_matrix()` 直接合成 stage artifacts，没有执行最终 child/wrapper/finalizer control flow，因此不能证明实际
signal、cleanup ordering、exit precedence 或 once-only lifecycle。下一 correction 必须用 injected adapter 驱动最终 control
flow；纯 artifact fabrication 不能作为 wrapper lifecycle 验收。

## 验收决定、残余风险与下一分支

本次结果符合 fail-closed 停止点，接受为 valid pre-device failure；不接受为 matrix、reachability、zero-state 或 Z0 pass。
唯一 Z0 real budget 未消费，但本 PLAN 的 package build budget 已消费，禁止修补旧 source、复用 root 或直接重跑。

下一包只允许在 fresh external offline root 修复/验证 PLAN identity owner 与 wrapper lifecycle。它不得 import production
ESPHome、读取 secrets、解析 hostname、访问 network/device，亦不得启动 Z0。通过后仍须回 Planner；新的 real Z0 必须由再下一份
PLAN 单独放行。无需 Advisor 或 Human 危险操作授权。
