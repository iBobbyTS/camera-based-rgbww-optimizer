# GUIDE11 W2 有界纠偏结果（2026-09-23）

## 执行证据

- 父 run：`D:\rgbww-optimizer\guide11-w2\formal-w2-20260922`（用户暂停于 73/98，零态验证，
  `1f7aee6`）
- 后缀 run：`D:\rgbww-optimizer\guide11-w2\formal-w2-20260923-suffix`（25/25，26 gates pass，
  cleanup/all-off pass，无 failure；恢复校验 `b8e2a62`）
- 合并 98 观测 = 49 个新 strip 候选命令（各配对 Ray 参考），每节点 ≤2 新命令，
  遵守 GUIDE11 每节点 ≤3 上限；实测回退命令保留在本批之外。

## 选择分析（`derived/w2-selection-20260923.json`，选择帧不能认证）

对 W1 冻结 Ray 目标与三项容差计算全容差 E(u)：

- **9/25 节点**的 W2 候选命令 E<1（CCT、mired、Duv 同时达标），且这 9 个节点全部
  从 W6-fail 改善为达标——两阶段实测割线方向有效。
- 其余 16 个节点的最佳候选仍超容差：按 GUIDE11 语义记录为
  **已测试邻域内的稳定最佳近似**，不称硬件极限；每节点给出 E 值与各门分量。
- 全部 9 个达标命令标记 `independent_FAST_confirmation_required`（GUIDE11 W2：
  候选不能凭选择帧认证）——进入 W3 前或与 W3 合并安排独立确认。

## 预算与停止原因

- 每节点命令预算 2/3 已用；未用 probe（实测方向覆盖 26/33 开放节点，其余 7 个
  节点无实测方向证据，本轮诚实标记 `no_measured_direction`，不猜方向）。
- 1800/100 按 GUIDE10 决定保持关闭，仅 N1 重复性证据（±0.27 mired）。

## 下一步（W3）

1. 冻结最终控制模型：70 节点 LUT（9 个 W2 选择命令 + 其余节点实测最佳命令）
   × `guide11_mired_gm_bilinear_clamped_v1` 共享插值。
2. 20 个新的非节点配对留出（40 张），分冷暖段/GM 正负/active-face 切换分层，
   采集前固定坐标；每点报告节点本底残差与插值增量两个量。
