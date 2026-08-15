# Advisor Handoff — GUIDE6 H120/S100 S-MEASUREMENT

## Gate

`ADVISOR_GATE_REQUIRED`

GUIDE6 的首个 H120/S100 direct local-controllability block 在第一个 Ray
`Q_before` 观察点失败。该点已真实执行并生成一张 CR3，但冻结的 58-feature
observer 无法从该曝光得到有效特征；因此不能构建 Ray bracket、strip probes
或 Jacobian。

## 运行身份

- Branch: `codex/guide4-science-path-v3`
- Git checkpoint: `c597259db27709e379da6dbc5369772c560ee9d7`
- Root: `/Volumes/4T/temp/rgbww-optimizer/guide6-direct-local-controllability-20260815/20260815-004300-h120-s100-retry1/guide6-h120-s100-20260815-retry1`
- `completed_formal=0/16`
- `ambient=0`
- cleanup: pass
- 最终 Ray/strip: 已执行 all-off；Ray 与灯带均归零

## 具体证据

失败类型：`HsiRejectedFeaturesError`

- capture: `000-ray-h120-s100-ray_q_before`
- nominal shutter: `1/5000`
- recorded exposure: `0.000193774542476587 s`
- CR3 byte count: `8,538,324`
- CR3 SHA-256: `a0db68955cac52582186ad0013b96da27c6af771994c723439d2e9f7175f643c`
- sidecar SHA-256: `78bff4294434876281bef5e07a5198cc08de404b1bb629491a488c2c2e18b386`
- 每个 CFA plane 的 observed max 约 `531..539`，接近 black level `512`
- 58 个 required HSI observer features 全部被拒绝；不是阈值放宽或特征删除问题

Ray 的 set/readback 命令均返回成功（H=120、S=100、intensity=1000），但图像内容
没有进入冻结 observer 的可观测包络。ESPHome all-off 和 Ray all-off cleanup 均通过。

## 诊断与限制

这是 `S-MEASUREMENT`：required point 在冻结 exposure/observer envelope 内不可观测，
不是 solver 失败、不是 gamut unreachable，也不是有效的颜色科学负结果。已检查既有
R6 evidence：`1/5000` 在历史 Ray 路径中可产生有效非黑 patch，但本次 Q_before 的
四个 plane 均停留在噪声底，说明当前数据不足以判定 protocol 或 source contrast。

按 GUIDE6，只能进行一次 bounded exposure-policy diagnosis；当前冻结 envelope 是
per-source auto 的 `1.0x..1.25x`，没有仓库内证据允许把本次曝光扩大到更长快门而仍保持
同一 observer 合同。若 Advisor 允许改变 exposure policy，需明确新的 shutter、包络、
以及是否仍可与既有 frozen 58-feature evidence 比较；否则本路线不能安全继续。

## 需要 Advisor 回答的问题

1. 是否批准在不改变 observer、feature、covariance 和质量阈值的前提下，扩大 Ray
   H120/S100 的曝光策略以获得可观测 Q_before？
2. 若批准，请给出精确 shutter/自动曝光上限及与既有 R6 evidence 的可比性要求。
3. 若不批准，是否将本次标为 `local_controllability_not_observable_under_frozen_exposure`
   并结束 GUIDE6 direct block？

## 附件说明

本 handoff ZIP 只包含派生 JSON、命令/物理返回/失败/运行摘要、observer metadata、
相关源码、测试、PLAN 与 GUIDE。原始 CR3 不进入 ZIP；其绝对路径、大小和 SHA-256
已在上方记录。
