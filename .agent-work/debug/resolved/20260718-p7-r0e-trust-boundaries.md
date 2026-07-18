# P7-R0E trust-boundary closure

- 状态：resolved（离线实现完成，等待 Planner 验收）
- 基线：`27a68cfb3a7d48e3cfbb620bb1575adf3e003e51`
- 范围：仅 P7-R0E 离线实现；禁止设备、网络、`.env`、firmware upload、真实 run 与 P7-R1。

## 已确认 fail-open

1. ESPHome `light()` 返回本地 `_build_payload()`，不是设备状态。
2. `goal_confirmed` 未由合法 confirmed group 唯一反推。
3. formal row 可自行抬高 auto/weak 子预算。
4. capture owner 非唯一，sample feature/objective 未从 RAW report replay。
5. R1 只逐 row 查 plan membership，未验证完整同序 capture plan。

## 根因假设

证据对象的所有权仍分散在 runner 自报 row 中；device command acknowledgement、RAW measurement、solver-derived status 和 frozen plan sequence 没有各自独立的真值边界。

## 最小修复边界

- 保留 `esphome.light()` command-only 兼容接口；新增 generation + atomic JSON snapshot 的 verified API。
- Firmware 由单一 script 原子设置 PWM、commanded-state globals、generation 并发布 text sensor。
- Formal analyzer 重建全 run owner table、RAW features、v2 objective、confirmation spread/status 与冻结子预算。
- R1 analyzer 要求 captures/attempts/commands 与完整 frozen plan 同序同基数。

## 结果与保留阻塞

- fake aioesphomeapi 已覆盖 bare payload、stale/non-increasing generation、channel mismatch、missing entity、timeout；两个 formal runner 已只注入 `verified_light`。
- formal v2 analyzer 已从 retained capture/RAW report 重算 58 features、objective、confirmation group/status、capture owner 与 frozen sub-budget；R1 analyzer 已要求完整 frozen plan 同序同长，并拒绝 duplicate ambient replacement。
- 固件仅完成 YAML 结构检查；本机没有 `esphome` CLI，因此 compile 保持 blocked，未联网安装或刷写。
- 真实 device-state preflight 与 `p7_targeted_reference_repeatability_v2` 仍需独立授权，当前 Gate 保持 Blocked。
