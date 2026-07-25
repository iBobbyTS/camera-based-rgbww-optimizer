# P7-TD-B-F0B-R1-C3-E2-A0 授权边界修订归档

**归档时间：** `2026-07-24T14:25:51-0600`

**被替代计划：** `.agent-work/PLAN.md`，审查前 SHA-256
`efca57238645e1fc247f5491606f32abee9195b0def22aab87c6f4e45da9253f`。

## 变更原因

Human 明确要求将授权边界写入项目规则：只有远程固件上传/刷写、远程部署、破坏性硬件变更等危险状态变更需要
Human authorization；离线 release/lineage qualification、只读 remote/device readback、计划内 Ray/strip 开关灯、
零状态建立和 Python/shell cleanup 不需要单独授权。

`AGENTS.md` 已新增该边界。它没有扩大任何实验预算，也没有授权 firmware、deployment、formal、capture 或后续阶段。

## 原计划审查与决定

- 原计划在等待当前 `fa6c95d` release 的新 Human E2 授权，但该等待条件与修订后的项目授权规则不一致。
- 已接受 release：
  `/Volumes/4T/temp/rgbww-optimizer/p7-td-b-lineage-release/lineage-release-fa6c95d-20260724-180618/setup-lineage-release.json`
  ，SHA-256 `1d3fffd82b66dcbca033a6d47bf13af4bbf98f10e9e544f308f4959047532529`。
- L1 validation summary：
  `/Volumes/4T/temp/rgbww-optimizer/p7-td-b-r1-c3-l1-offline/20260724-180618/validation-summary.json`，
  SHA-256 `fa0bd82d49ceff571053ff706a73bc6fa8e92a02482e58272591738e960f528d`。
- L1 archive：`.agent-work/PLANS/20260724-1409-p7-td-b-r1-c3-l1-review.md`，SHA-256
  `d565ecb6ce5ca8778fafd52ac85a9fa739e200f354e9029d834b374aebb6898e`。

## 新决定与边界

- 当前计划改为 `execute_bounded_e2_preflight_waiting_for_executor`，Executor 可消费 active PLAN，不再等待额外
  Human authorization。
- E2 仅是一次 fresh preflight：当前 release/checkpoint identity、remote health/config/v2 capability、RAW/ISO 100/
  非空 aperture、Ray 零状态 readback、`bedroom-rgbww-strip` identity/MAC/generation-bearing 全零 readback，以及
  Python/shell cleanup 与独立最终双零。
- 该包禁止 camera capture、CR3/NPY、Ray/strip 非零输出、formal、public analyzer actual run、自动 retry、firmware
  upload、remote deployment、破坏性硬件变更、strip formal、TD-C、sentinel、remaining、boundary、holdout、Gate-6、P8
  与 commit。
- 任一 release/checkpoint、设备身份、设置/能力、zero readback、cleanup、process ownership 或 evidence ledger 失败，
  必须保留证据、清理并停止；不得扩大范围。
- E2 完成后仍必须回到 Planner 验收门；本次放行不生成 accepted formal claim，也不预授权后续阶段。

## 精确下一分支

`P7-TD-B-F0B-R1-C3-E2-A0_EXECUTE_ONCE_THEN_RETURN_TO_PLANNER`

