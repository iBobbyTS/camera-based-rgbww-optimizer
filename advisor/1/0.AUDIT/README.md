# Camera-Based RGBWW Optimizer 项目审计

## 审计范围

本文档集记录项目从 2026-06-02 建仓到 2026-07-13 当前工作区的主要设计、实机尝试、失败原因、算法演进、保留产物和最终结果。它不是只按 Git 提交整理的 changelog；未提交但已经完成实机验证的白光热稳定性工作也包含在内。

审计对象包括：

- GLEDOPTO GL-C-211WL 控制器从 stock WLED 到 ESPHome 的控制路径。
- 五个物理通道 `CW/WW/R/G/B` 的 12-bit PWM、响应测量和 code-duty 校正。
- Canon EOS R6 Mark III 的 RAW 采集、自动曝光、色卡定位和白点计算。
- Amaran Ray120c OpenAPI v2 控制及其作为相对参考光源的使用边界。
- WW/CW 端点搜索、4x3 和 14x5 白光 LUT、反馈求解、复测及热稳定性修复。
- 当前可用结果、不能据此声称的结论、后续继续实验时应复用的入口。

## 文件导航

1. [01-foundation-and-measurement.md](01-foundation-and-measurement.md)：固件、设备控制、相机、色卡和 PWM 响应链。
2. [02-white-endpoints-and-observation.md](02-white-endpoints-and-observation.md)：RAW 白点方法、端点搜索的全部主要尝试和环境结论。
3. [03-white-lut-iterations.md](03-white-lut-iterations.md)：4x3/14x5 LUT、求解器、实机失败与修复时间线。
4. [04-final-results-and-risks.md](04-final-results-and-risks.md)：最终数据、证据路径、当前配置差异、剩余风险和继续工作的边界。

本目录共 5 个文件，不再增加同级文档；后续补充应写入上述最相关文件。

## 当前结论摘要

| 项目 | 当前结论 | 证据强度 |
| --- | --- | --- |
| 五通道独立控制 | ESPHome Native API 可直接控制 `CW/WW/R/G/B`，输入 `0..4095` | 已实机验证 |
| PWM 线性化 | 五通道各 19 个 code 点，共 95 条响应，已生成 code-duty curve | 已测量；源 run 含一次中断后合并 |
| 色卡定位 | 当前定位文件为 `config/location/locations-20260709-012045.json` | 已用新 RAW 复核 |
| WW/CW 端点 | WW 对应 Ray `2931K/GM176`，CW 对应 Ray `7702K/GM160` | 最佳环境实机结果 |
| 正式 LUT 网格 | 14 个 CCT x 5 个 GM，共 70 点 | 已生成完整结果 |
| 最终 LUT 文件 | `/Volumes/4T/temp/rgbww-optimizer/white-lut-calibration/14x5-off-cycle-refined-v2-20260713/white-lut-calibration.json` | 文件状态 `complete` |
| 最终独立复测 | 风险最高的原 10 点在独立开关灯和 60 秒稳定后 `10/10` 通过 | 已实机验证 |
| 其余 60 点 | 没有在最终 off/on 策略下逐点独立复测 | 未验证，不得外推 |
| 默认控制 LUT | `config/white/white-lut.json` 仍是旧 4x3、12 点结果 | 已核对；不是最终 70 点 |
| 彩色色块一致性 | 白点优化不等于彩色表面匹配；跨光源 24 色块 RMSE 仍约 `14.28%..15.37%` | 已观察，未解决 |
| 绝对亮度一致性 | 不是当前反馈的硬验收项 | 未完成 |

## 最重要的审计判断

1. **最终 70 点文件可作为当前最佳白光 LUT 候选，但尚未安装为默认 LUT。** 调用 `camera_based_rgbww_optimizer.control.white_lut` 不传 `--lut` 时仍会读取旧的 12 点文件。
2. **“70/70 complete”不等于 70 点都完成了最终热态独立复测。** 九个高风险节点经过本轮 off/on 重新优化，最终复测覆盖原风险最高 10 点；其余 60 点沿用之前严格运行的数据。
3. **相机估算的 CCT 是相对搜索坐标，不是 Ray 标称 Kelvin 或 Lightroom 温度滑块的等价读数。** 例如 Ray 标称 `14000K` 在当前相机矩阵下可估算为约 `9631K`；匹配应比较同轮 Ray 与灯带，而不是把估算值当绝对光谱真值。
4. **此前几次“成功”后来被推翻，主要不是随机代码错误，而是实验状态不等价。** 关键问题依次包括同时亮灯、Ray/灯带曝光缓存串用、通道边界裁剪、单张即接受、未真正从全关状态确认，以及把冷态和热态样本放入同一 secant 窗口。
5. **当前停止阈值以实测重复性为基础。** 公共验收为 Duv `<0.0005`，CCT 至少 `25K`、高色温按 `1 mired` 放宽；单点优化内部目标收紧一半，并要求两次独立 off/on 确认。

## 证据等级

- **已实机验证**：有 RAW、JSON、日志和设备关闭结果，且当前代码能够解释该结果。
- **离线验证**：只回放已有数据或单元测试，没有重新控制设备。
- **历史结果**：当时成功，但后来发现实验条件或算法有缺陷；只用于解释演进。
- **未覆盖**：当前结果不能证明，后续不得把它写成已完成。

## 工作区状态说明

审计生成时 `main` 的最新提交为 `f0757d8 fix(calibration): refine white LUT workflow`。其后的 off/on 确认、热态 rebase、macOS PTP 恢复扩展及相关测试仍在当前未提交工作区中。本文档记录的是**当前工作区 + 外置盘实验产物**，不是只记录 `HEAD`。

