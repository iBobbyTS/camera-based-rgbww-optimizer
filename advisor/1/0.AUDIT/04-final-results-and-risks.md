# 最终结果、证据和剩余风险

## 1. 当前最佳结果

最终 70 点候选：

```text
/Volumes/4T/temp/rgbww-optimizer/white-lut-calibration/
14x5-off-cycle-refined-v2-20260713/white-lut-calibration.json
```

文件级统计：

- 状态：`complete`
- 节点：70/70 complete
- 最大保存 CCT 误差：约 `109.09K`
- 最大保存 Duv 误差：约 `0.0004198794`
- 最大保存 goal score：约 `0.83976`

该文件由 strict 70 点结果逐层合并九个 off/on 重新优化节点。顶层 `point_refinements` 只列最后四个节点，因为前五个记录在上一层 `derived_from` 文件中；这属于 provenance 表达不完整，不影响最终节点命令。

## 2. 最终独立高风险复测

报告：`tmp/white-off-cycle-final-recheck-v2/20260713-024518/white-top10-recheck.json`

每个点流程为：灯带/Ray 全关 -> 单独拍 Ray -> Ray 全关 -> 从零启动灯带 -> 等待 60 秒 -> 单独拍灯带。结果：

| CCT/GM | CCT 误差 | Duv 误差 | goal score | 结果 |
| --- | ---: | ---: | ---: | --- |
| `14000/130` | `-68.40K` | `-0.0000878` | `0.737` | 通过 |
| `20000/200` | `-27.96K` | `+0.0000883` | `0.206` | 通过 |
| `2300/200` | `+6.14K` | `-0.0000481` | `0.246` | 通过 |
| `2300/130` | `+6.08K` | `-0.0000825` | `0.243` | 通过 |
| `2700/100` | `-3.47K` | `+0.0001205` | `0.241` | 通过 |
| `8000/130` | `-12.77K` | `-0.0001265` | `0.296` | 通过 |
| `14000/0` | `-23.59K` | `+0.0001698` | `0.340` | 通过 |
| `6500/100` | `-21.97K` | `-0.0004065` | `0.813` | 通过 |
| `3200/200` | `-18.39K` | `+0.0002858` | `0.736` | 通过 |
| `2300/70` | `+3.04K` | `-0.0001122` | `0.224` | 通过 |

汇总：10/10 通过，最大 score `0.8130`，最大绝对 CCT 误差 `68.40K`，最大绝对 Duv 误差 `0.0004065`。

`14000/130` 的 `68K` 不是优化器在 68K 时提前停止：优化阶段两次内部确认曾接近 `2K`；68K 来自之后的 verification-only 独立复测。该轮 Ray 标称 14000K 的相机估算为约 `9631K`，`1 mired` 对应 `92.75K`，所以 68K 的归一化 CCT 得分为 `0.737`。在已测得高 CCT 3 sigma 约 121K 的条件下，继续追单张读数容易过拟合噪声和热漂移。

## 3. 当前默认配置并非最终结果

`camera_based_rgbww_optimizer.control.white_lut` 默认读取：

```text
config/white/white-lut.json
```

该文件仍是历史 4x3 网格：CCT `1800,3200,5600,20000` x GM `0,100,200`，共 12 点。最终 70 点文件尚未复制到默认配置。使用最终结果必须显式传：

```bash
.venv/bin/python -m camera_based_rgbww_optimizer.control.white_lut \
  --lut /Volumes/4T/temp/rgbww-optimizer/white-lut-calibration/14x5-off-cycle-refined-v2-20260713/white-lut-calibration.json \
  5600 100 --intensity-percent 100
```

这条命令是显式 light-on 工具，会保持灯带亮起；手工结束后应调用 `control.all_off`。

## 4. 验证状态

当前工作区最终验证：

- `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m unittest discover -s tests -v`
- 143/143 测试通过；第一次受限沙箱运行有 4 个 localhost bind `PermissionError`，在允许回环网络后原命令全部通过。
- `git diff --check` 通过。
- CodeGraph 已同步。
- 九个成功单点优化目录残留 `.npy` 数量为 0。
- 最终复测目录残留 `.npy` 数量为 0。
- 最终 `all_off` 返回 ESPHome 五通道全零、Ray intensity 0。
- 最终无白光优化/相机测量进程残留。

## 5. 不能从当前结果推出的结论

### 5.1 不能称为 70 点全部最终复测

最终 verification-only 流程只覆盖原风险最高 10 点。九点在本轮被替换，`6500/100` 作为未替换对照也通过；其余 60 点没有逐点经过当前“全关 -> 60 秒 -> 独立拍摄”的最终复测。

### 5.2 不能称为光谱或 Lightroom 绝对匹配

CCT/Duv 来自 Canon camera RGB 和近似相机矩阵。它适合控制同一相机下 Ray 与灯带的相对白点，不是光谱功率分布、CRI/TM-30，也不是 Lightroom Temperature/Tint 的逆解。

### 5.3 不能称为彩色表面复现完成

反馈停止条件只使用白块 CCT/Duv。24 色块加权比较只作辅助排序，不是硬验收项。跨日复测中，同源变化很小，但灯带对 Ray 的加权 24 色块 RMSE 仍约 `14.28%..15.37%`。白点接近并不消除 metamerism 或窄带 RGB 对彩色物体的差异。

### 5.4 不能称为绝对亮度匹配

Ray 和灯带使用独立自动曝光，反馈主要优化色度。虽然每个节点要求至少一个通道 `4095` 以追求高输出，但当前没有照度计或统一曝光下的绝对 luminance 硬目标。

### 5.5 不能把每个 Kelvin 差都当可继续修正的确定误差

高 CCT 的 Kelvin 坐标非线性，极小 `uv` 变化会产生较大 Kelvin 数字；系统还存在相机重复性和灯带热漂移。应优先看 mired、`uv1960`、Duv 和重复拍摄分布。

## 6. 继续工作的优先级

1. **决定是否安装最终 LUT。** 在明确保留旧 4x3 备份后，再把最终 70 点复制到 `config/white/white-lut.json`；当前审计没有执行该替换。
2. **分批复测剩余 60 点。** 复用 verification-only runner，保持每点 60 秒 settle；不要重新优化已通过点，先测后决定。
3. **高 CCT 改为多次配对验收。** 对 Ray/灯带各拍多组 off/on 样本，在 mired 或 `uv1960` 上求稳健中心和置信区间，避免追单帧 Kelvin。
4. **若目标包括彩色物体，增加显式 24 色块目标。** 先定义允许的加权 RMSE/DeltaE，再决定是否扩展反馈状态，不应把当前白点成功直接包装成全色复现。
5. **若目标包括绝对亮度，增加固定曝光或外部照度测量。** 独立 auto-exposure 的结果不足以验收光通量。
6. **保留外置盘证据。** 最终 70 点、strict 基线、九个单点 refinement 和最终 10 点报告是重建 provenance 所需的最小集合。

## 7. 关键证据索引

### 追踪文件

- `config/white/white-endpoints.json`
- `config/white/white-lut.json`（旧 4x3 默认 LUT）
- `config/channel/code-duty-curve.json`
- `config/location/locations-20260709-012045.json`
- `docs/README.md`
- `.agent-work/debug/active/20260712-white-lut-repeatability-and-strict-anchors.md`
- `.agent-work/debug/resolved/20260709-white-lut-light-isolation-exposure-cache.md`
- `.agent-work/debug/resolved/20260710-white-lut-bounded-feedback-solver.md`

### 仓库临时证据

- `tmp/channel-response/merged/channel-code-duty-response-merged.json`
- `tmp/white-endpoints/20260709-023258/white-endpoints.json`
- `tmp/white-endpoints/20260709-023258/EXPERIMENT_SUMMARY.md`
- `tmp/manual-cr3-analysis-20260711-220754/manual-cr3-cct-duv-report.json`
- `tmp/manual-cr3-neutral-crosscheck-20260711-220922/neutral-patch-crosscheck.json`
- `tmp/white-thermal-stability/20260713-003204/white-thermal-stability.json`
- `tmp/white-top10-recheck/20260712-232005/white-top10-recheck.json`
- `tmp/white-off-cycle-final-recheck-v2/20260713-024518/white-top10-recheck.json`

### 外置盘证据

- `/Volumes/4T/temp/rgbww-optimizer/white-lut-calibration/14x5-20260711-021335/white-lut-calibration.json`
- `/Volumes/4T/temp/rgbww-optimizer/white-lut-calibration/14x5-strict-20260712-023352/white-lut-calibration.json`
- `/Volumes/4T/temp/rgbww-optimizer/white-lut-calibration/14x5-off-cycle-refined-v2-20260713/white-lut-calibration.json`
- `/Volumes/4T/temp/rgbww-optimizer/white-lut-calibration/top10-off-cycle-20260713-030000-2300K-gm70/white-lut-calibration.json`

## 8. 最终审计结论

项目已经从“能否独立控制五路 PWM”推进到“在同一 Canon 相机、同一色卡场景下，用 Ray120c 做相对白点参考，并生成可插值的 70 点 RGBWW 白光命令”。最可信的成果是 WW/CW 正式端点、完整 70 点候选、风险最高 10 点的独立热态复测以及围绕失败样本建立的反馈修复。

当前仍应把它称作**相机观测白点 LUT**，而不是光谱复现、全色色彩复现或绝对亮度校准。下一阶段是否继续扩大实机复测，取决于用户是否要把“高风险点通过”提升为“70 点全部最终复测通过”，以及是否把目标从白点扩展到彩色表面和亮度。

