# GUIDE11 W8 真实重算 + P6 锚点自检收口（2026-09-28）

## W8：白光最终报告由真实输入重算

产物：`D:\rgbww-optimizer\guide11-w8\guide11-white-final-report-20260928.json`
（schema `guide11_white_final_report_v1`，脚本 `tmp/recompute_w8_guide11_20260928.py`）

修正了旧 GUIDE10 W8 artifact 的四个问题：

1. **逐点命令与来源**：70 节点 = 9 个 W2 采纳命令（选择帧 E 达标）+ 61 个
   W6 回退命令。16 个 W2 处理但未采纳的节点明确记录
   `w2_no_remeasurement_of_shipped_command`（W2 只测新探针，装载命令未被重测；
   冻结保留回退是因为选择帧不能认证换命令）。
2. **误差身份与阈值来源**：每点标注 `w2_selection_frame`（n=1，不可作独立确认）
   或 `w6_single_observation`（n=1），阈值统一来自 W1 冻结目标
   （`guide11_w1_frozen_targets_v1`），E 按
   max(|e_K|/τ_K, |e_mired|/τ_mired, |e_Duv|/τ_Duv) 对全部节点重算。
3. **区间**：仅 6 个 N1 共置锚点给出条件区间（n=2 循环 Student-t）与预测区间
   （df=1，天然很宽）；其余 64 点 `applicable=false` 并写明原因（共置重复性
   缺失、池化迁移未验证）。3 个 burst 锚点注明短时噪声为组合分量不可分摊。
4. **FAST–LONG**：`true_LONG_observations=8`（4 锚点 × Ray/strip 各一），只有
   逐锚点 `delta_protocol` 差中之差块（两侧协议均由 timing label 验证：
   LONG 实测曝光起点 604.6–605.9 s，FAST reset600/D120）。旧 artifact 的
   `thermal_bias` 标量**不搬运**。

汇总：45/70 点估计在容差内（3000–5000K 9/15、5000–8000K 13/15、≥8000K 14/20、
<3000K 9/20）；连续插值仅 5300–7250K 中带（|GM 偏移|≤65）有留出支持；1800/GM100
维持 GUIDE10 永久关闭（仅重复性观测）；`steady_claim=false`。

## P6：当前锚点自检与多解检查（并入 C3 证据）

产物：`D:\rgbww-optimizer\guide11-c1\derived\c3-anchor-self-check-20260925.json`
（38 锚点，脚本 `tmp/c3_anchor_self_check_20260925.py`）

- **当前锚点**：hue×SAT z 网格由 C1/G9 新鲜 Ray 夹持 + N1 白光锚点构成，
  白光行 `hue=null` 即 SAT0 的 Hue `not_applicable` 编码；C1 计划的
  `sat0_hue_gate` 亦为 `not_applicable`，无任何 SAT0 Hue 门。
- **多解检查**：nearest-anchor 反解 10/10 `ambiguous`（最近/次近距离接近，
  如 H0/S50 最近 H300/S50 距 0.95、次近 H60/S50 距 1.15）。结论：当前锚点
  密度下 z→(H,S) 反解不可无歧义使用——因此 C1/C2/C4 一律使用**成对新鲜 Ray
  参考**定向，绝不用绝对锚点反解认证目标。
- **饱和度方向**：四个已测 hue 的 S50→S100 z 向量方向正确（红端 R/G 升、
  青端 B/G 降），拓扑有序。
- **历史 58 维最近点的地位**：仅作形状先验，不构成有效 SAT 覆盖；C6 最终
  覆盖图中无当前协议支持的区域报告模型区间与转移资格，不写百分比覆盖。

无未决科学问题；两项均为 GUIDE11 实现清单第 4、6 条的收口证据。
