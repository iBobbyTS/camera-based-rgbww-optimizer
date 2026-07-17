# 阶段 4：完整 14x5 CCT/GM

**覆盖原阶段：** P5

**进入条件：** Gate-3 明确 `expand_to_70`，pilot 权重、目标、patch 集和模型已冻结。

**阶段目标：** 生成、闭环、比较插值并独立验证完整 70 点候选。

**不得跨越：** 不得根据最终验证回调 pilot 权重；不得在 70/70 独立验证前安装；不得自行开始 HSI。

**最终状态（2026-07-17）：** `skipped`。Gate-3 未给出 `expand_to_70`；P4 在冻结测量合同下有 5/12 不可观测点并存在多个 neutral hard-gate 失败。Gate-4 直接冻结为 `retain_previous_candidate; approve_stage_5`：保留既有外置 white-only 70 点候选，不生成 P5 multipatch 候选，不覆盖默认 LUT，进入 Ray-only HSI 表征。

## 执行顺序

1. 实现全局求解、约束和合成测试；新增 SciPy 必须先获用户批准。
2. 获实机授权后采集同会话 Ray 目标并生成 70 点候选。
3. 完成实拍闭环、插值 A/B 和至少 20 个非节点留出。
4. 冻结候选后创建全新 run 做 70/70 独立验证；验证中绝不优化。
5. 任一候选改变都使旧完整验证失效；按本文件规则重新验证。
6. 到达 Gate-4 后停止，不覆盖默认 LUT，不启动 HSI。

## 高级模型决策门 Gate-4

高级模型决定 CCT 路线闭环及是否值得进入 HSI：

- `accept_cct_candidate_for_install_review`：70/70 与非节点均通过，multipatch 有稳定收益。
- `accept_external_candidate_only`：候选有价值但 provenance/跨日/安装条件不足，保持外置。
- `retain_previous_candidate`：新候选无收益或失败。
- `revise_interpolation_and_revalidate`：节点通过、插值失败。
- `repeat_full_validation`：候选未变但验证运行无效。
- `stop_before_hsi` 或 `approve_stage_5`。

安装默认 LUT 仍需用户明确授权；`approve_stage_5` 只批准开始 Ray HSI 表征。

---

## 11. P5：完整 14x5 CCT/GM

### 11.1 进入条件

只有 P4 分支 C-A 才进入。其他分支不得创建完整候选。

目标网格：

```text
CCT: 1800, 2000, 2300, 2700, 3200, 3800, 4500,
     5000, 5600, 6500, 8000, 10000, 14000, 20000
GM:  0, 70, 100, 130, 200
```

### 11.2 Ray 目标采集

- 每个节点 Ray 同会话实拍，不用命令数字代替目标。
- 至少两次配对；极端 CCT 和低 CCT GM 塌缩区增加第三次。
- 固定锚点穿插。
- 保存 native multipatch 向量、协方差和近似 CCT/Duv。

### 11.3 全局求解

变量为 70 个五通道命令，加每点允许的亮度 scale。目标包含：

- 数据项。
- CCT 方向按真实坐标距离加权的二阶平滑。
- GM 方向二阶平滑。
- 交叉方向平滑。
- RGB 软先验。
- active-channel 连续性和命令敏感度。

依赖分支：

#### GLOB-A：允许新增 SciPy 依赖

- 推荐路径。
- 在修改 `pyproject.toml` 前向用户说明新依赖。
- 使用有 bounds 的成熟优化器和明确 Jacobian；保存 solver 版本、终止原因和 KKT/残差指标。
- PCHIP/周期样条也可复用 SciPy。

#### GLOB-B：不允许新增 SciPy

- 使用 NumPy 的分块坐标求解加平滑投影。
- 每轮先逐点 bounded solve，再做平滑 proximal/projection，再重新投影到 bounds 和 active-channel 约束。
- 输出必须标明 `approximate_block_coordinate_solution`，不得声称全局最优。
- 用小型 synthetic grid 验证目标单调下降和约束不破坏。

### 11.4 实拍闭环

保留已验证策略：

- 两次独立确认。
- off 1 秒，上命令 60 秒。
- 确认失败成为 thermal base。
- 连续 secant 预测失准触发 rebase。
- 冷态样本不进入热态 active window。
- 所有历史样本留在 provenance。

### 11.5 插值 A/B

至少比较：

- Kelvin bilinear。
- mired x GM。
- per-channel shape-preserving。
- Ray 实测目标轨迹插值。

至少 20 个非节点留出点，覆盖低 CCT、高 CCT、GM 中点、2300K 塌缩区和 active-set 边界。

分支：

- 某方法在留出实拍上显著更优且连续：选该方法。
- 多方法差异不超过重复性：保留 Kelvin bilinear，优先简单和现有兼容性。
- 方法局部优劣不同：允许分区策略，但必须在边界检查命令和观测连续性。
- 所有方法留出失败：增加必要节点或回到全局平滑，不能安装。

### 11.6 70/70 最终验证

候选冻结后，独立新 run：

- 70/70 节点全部 off/on 60 秒。
- 每点至少两次，风险点三次。
- 顺序随机或分块平衡。
- 最少 20 个插值留出点。
- 固定锚点监控。
- 验证 run 内绝不再优化。

若任何节点失败：

1. 当前 candidate 标记失败，不安装。
2. 单独分析失败点并生成新 candidate 版本。
3. 先定向复核失败点。
4. 新 candidate 一旦改变，最终仍需重新完整 70/70 验证；旧通过帧不能拼成新 candidate 的 70/70。

### 11.7 安装分支

只有全部满足才安装：

- 70/70 和插值留出通过。
- multipatch 优于当前候选，白点不退化。
- provenance 完整。
- 默认 LUT 备份、hash 和回滚命令明确。
- 全测试通过。

否则保留旧默认和当前外置候选，并在总结中明确未安装原因。

---
