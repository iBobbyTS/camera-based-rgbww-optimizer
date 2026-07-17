# Stage 6 HSI 路线审计与 Advisor 纠偏请求

## 审计目的

本文档集记录 `advisor/1/1.PLAN.md` 执行至 2026-07-17 的结果，重点回答两类问题：

1. P1 至 P6 哪些工作已经有实机证据，可以作为不可回退的输入；
2. P7 灯带 HSI 实拍前，哪些验收语义和实验分支需要 advisor 明确纠偏。

本次审计不要求重新设计已经完成的 Ray HSI 流形，也不把 P7 的 dry-run、fake hardware 或单元测试写成灯带实拍成功。审计生成期间没有调用相机、Ray120c 或 ESPHome，也没有修改算法和配置。

## 文件导航

1. [01-scope-baseline-and-status.md](01-scope-baseline-and-status.md)：当前基线、声明边界、冻结输入、安全合同和工作区状态。
2. [02-completed-p1-through-p4.md](02-completed-p1-through-p4.md)：remote/RAW 观察者、五通道基底、混合验证和 CCT multipatch 的完成结果。
3. [03-p6-ray-hsi-gate5.md](03-p6-ray-hsi-gate5.md)：106 张 Ray-only HSI 实拍、Gate-5 证据、冻结模型及其边界。
4. [04-p7-offline-implementation-and-risks.md](04-p7-offline-implementation-and-risks.md)：P7 当前代码、13 点 pilot、安全路径、离线验证和实拍前缺口。
5. [05-advisor-decisions-and-next-branches.md](05-advisor-decisions-and-next-branches.md)：需要 advisor 回答的决策、推荐默认值和各结果分支。

本目录共 6 个文件。后续 advisor 意见和执行结果应更新到最相关文件，不再增加同级文件，以保持在最多 7 个文件的限制内。

## 当前结论摘要

| 范围 | 当前结论 | 证据等级 | 是否需要 advisor 重审 |
| --- | --- | --- | --- |
| Remote 相机链 | 新实验统一使用 `r6-camera-bridge`，CR3 原子落盘，密钥由脚本从 `.env` 读取 | 实机验证 | 否 |
| RAW 观察者 | identity RAW；每源 `1.0x..1.25x` 曝光包络；保留 `R/G1/G2/B` | 跨日实机验证，conditional pass | 否 |
| 五通道基底 | P2 分档基底可作初值，但不是高精度全局前向模型 | 实机验证 | 否 |
| 通道加法性 | P3 选择 `M-E / forward_model_seed_only` | 实机验证 | 否 |
| CCT multipatch | 7 点可评估但 5 点不可观测，不扩到新 70 点网络 | 实机验证 | 否 |
| 既有白光候选 | 保留外置 white-only 70 点文件，不安装到默认 LUT | 部分最终复测 | 否 |
| Ray HSI | Gate-5=`full_periodic_2d_HB`，使用周期二维分段线性目标流形 | 106 张实机验证 | 否 |
| Strip HSI | runner/objective/feedback/analyzer 已离线完成；没有真实灯带结果 | dry-run、fake hardware、单元测试 | 是 |
| HSI INT | 尚未开始 P8 | 未实现、未实拍 | Gate-6 后再决定 |

## 最重要的审计判断

1. **项目可以继续。** P6 数据质量、设备状态审计和 Gate-5 证据足以进入 Stage 6，不需要重拍 Ray 的 106 点网络。
2. **不能直接把完整 13 点 P7 当作下一次无条件长跑任务。** 当前初值只是 seed-only，完整闭环最坏会产生数百张照片；应先验证少量 sentinel 点。
3. **P7 的核心缺口不是求解器是否存在，而是验收不确定性尚未冻结。** 当前目标函数可接收 strip Hue/SAT/shape 三项 3-sigma，但默认均为零，实际 runner 尚未提供有证据的 strip 重复性。
4. **`unconfirmed` 不能升级为 `physically unreachable`。** 精确 gamut 边界必须经过有上下界的定向搜索，不能仅由 SAT50/SAT100 pilot 的一次不收敛推断。
5. **Advisor 应做窄范围纠偏，不应重启 P1-P6。** 本次请求集中在验收噪声、pilot 分阶段和 gamut 公开语义。

## 证据等级

- **实机完成：** 有 CR3、measurement JSON、命令日志、run 状态和 Python/shell 双关灯证据。
- **条件通过：** 有实机证据，但只在明确包络、特征或产品范围内成立。
- **离线完成：** 代码、dry-run、fake hardware 或历史数据分析通过，尚无该阶段真实设备结果。
- **未决：** 会改变验收、公开语义或后续实验规模，必须由 advisor 或 Gate 决定。

