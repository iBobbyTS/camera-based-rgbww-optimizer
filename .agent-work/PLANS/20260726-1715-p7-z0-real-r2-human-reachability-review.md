# Planner Review：REAL-R2 watchdog 后 Human reachability evidence

审查日期：2026-07-26

## 审查范围

审查当前 `P7-TD-B-Z0-HUMAN-STOP`、REAL-R2 unknown evidence，以及 Human 提供的新本地网络观察：

`ping bedroom-rgbww-strip.local` 成功解析至 `192.168.0.74`，ICMP reply `ttl=64`、`time=13.258ms`。

本审查不执行任何设备、网络、hostname 或 cleanup 命令；只更新 Planner 路线。

## 证据判断

- Human ping 证明当前 hostname 可解析且该 IP 对 ICMP 有响应，足以解除“完全不可达”的前置阻塞。
- ping **不证明** ESPHome identity/MAC、state object、generation、RGBWW 五通道全零或物理灯带熄灭。
- REAL-R2 旧证据仍冻结为未知：五次 production call/watchdog 均 `attempted_result_unknown`，五条 cleanup 无 identity/state/generation/all-zero readback；driver SHA `f9330e5286dbf02ce3a3fc66d1ef9126a925f8a85af3d63d5478794bb89f2ceb`，terminal SHA `86e0187dd7b5ef9f2ee0aaf8e99deb620a2be1b58cd0197450e030606f73b4fb`。

## Planner 决策

**接受 ping 作为 reachability-only evidence，不关闭 findings 026/027。** 发布一次新的 bounded real zero-only gate，允许在 exact active PLAN 范围内：

- 只读 identity/MAC/state/generation 读取；
- 五个 zero-only `verified_light(0,0,0,0,0)` cleanup/stage calls（灯光控制属于项目明确的 zero/off 例外）；
- 不允许任何非零输出、重试、IP fallback、独立 probe或后续 E2/formal。

若第一阶段 identity/MAC/state 不匹配，或任何 zero readback/generation 缺失，立即 hard-fail并保持 zero proof unknown。

## 精确下一分支

`P7-TD-B-Z0-REAL-R3_BOUNDED_ZERO_ONLY_AFTER_HUMAN_REACHABILITY`

该 gate 消费冻结 controller SHA `98849221977908e96a3ff042c69a8fce8e306013ceb4a33f543a14ce079c3509`，self-check 一次、wrapper 一次、五 stages；仍不自动解锁 E2/formal。

维护性判断：Human ping 仅改变 reachability 前置判断，不改变 source/runner/cleanup owner；新计划只增加一次受限 gate，无需架构重构。
