# 阶段 3：4x3 CCT Multipatch 先导

**覆盖原阶段：** P4

**进入条件：** Gate-2 已冻结前向模型分支、feature/patch 集和目标层级。

**阶段目标：** 只用 12 点回答 multipatch 是否在不损害白点的情况下产生超出重复性噪声的稳定改善。

**不得跨越：** 这是从 12 点扩大到完整 70 点前最重要的成本与方向门；执行模型绝不自行扩网格。

## 执行顺序

1. 按冻结分支实现独立 pilot objective/solver/runner 和合成测试。
2. dry-run 审计通过并获用户实机授权后完成 12 点同轮 A/B。
3. 任何 solver 修正只按 C-C/C-E 的既定规则重跑完整 12 点；不得只挑通过点拼结果。
4. 汇总白点、training、holdout、重复性、命令连续性、RGB 使用和不可达点。
5. 形成 Gate-3 交接包后停止，不创建 70 点候选。

## 高级模型决策门 Gate-3

允许出口：

- `expand_to_70`：仅 C-A，12/12 两次确认、白点非劣且 training/holdout 改善超过重复性。
- `retain_white_only_end_cct_route`：C-B，multipatch 无工程收益。
- `repeat_pilot_after_objective_fix`：C-C，词典序/约束实现错误。
- `revise_extreme_gamut_model_then_repeat_12`：C-D，只允许一次定向模型修正后重跑全部 12 点。
- `thermal_repeat`：C-E。
- `stop_route`：连续失败或证据不足。

只有高级模型写出 `expand_to_70`，阶段 4 才可开始。

---

## 10. P4：4x3 CCT multipatch 先导 A/B

### 10.1 固定目标

```text
CCT: 1800, 3200, 5600, 20000
GM raw: 0, 100, 200
总计: 12 points
```

每点同轮采集：

1. Ray 实测目标。
2. 当前最佳 70 点 LUT 命令。
3. 新 multipatch 候选命令。
4. 两种 strip 命令各两次独立 off/on 60 秒确认。

### 10.2 求解器代码边界

建议新增：

```text
src/camera_based_rgbww_optimizer/optimization/multipatch_objective.py
src/camera_based_rgbww_optimizer/optimization/multipatch_solver.py
src/camera_based_rgbww_optimizer/optimization/measure_cct_multipatch_pilot.py
tests/test_multipatch_objective.py
tests/test_multipatch_solver.py
tests/test_measure_cct_multipatch_pilot.py
```

不要直接把试验逻辑塞进 `measure_white_lut.py`。先让 pilot 独立，P4 通过后再抽取共享 capture/feedback 边界。

现有 `white_lut_feedback._solve_box_constrained_least_squares` 是小维度 active-bound 枚举。新求解器若需要同样语义：

1. 先给现有行为补完整回归测试。
2. 抽到 `optimization/bounded_least_squares.py`。
3. 现有白点 feedback 和新 solver 都调用同一实现。
4. 不复制一份略有不同的 bounds/clipping 代码。

### 10.3 词典序目标

严格按顺序，不能用一个加权总分允许后项抵消前项：

1. 中性 patch RAW chroma 进入硬门槛。
2. 当前 CCT/Duv 门槛通过。
3. 在前两项可行域内最小化彩色色块稳健误差。
4. 再最小化留出 patch 误差。
5. 再考虑邻点连续性、RGB 软先验、headroom 和敏感度。

模型包含允许的全局亮度比例 `k>=0`，以匹配光色而非绝对亮度。命令约束：

```text
0 <= u_j <= 1
max(u) = 1
```

通过枚举 active channel 保证 `max(u)=1`，不要先无约束求解再 clipping。

### 10.4 训练/留出冻结

- 所有可靠 neutral patch 都用于一级硬目标。
- 黑块只作诊断。
- 有色 patch 在优化前按固定规则分成 training 和 holdout，规则写入 config/hash。
- 不得看结果后重新选择留出 patch。
- 若有额外材质，作为第二层 holdout；没有则明确记录。

### 10.5 P4 分支

#### C-A：12 点全部通过并稳定改善

条件：

- 12/12 点两次确认均满足中性 RAW 和 CCT/Duv 门槛。
- 白点对当前候选非劣。
- training 与 holdout 的平均、P90、最坏误差改善超过配对重复性。
- 没有明显命令跳变或只靠大量 RGB 换来小于噪声的改善。

动作：冻结 pilot 权重和目标定义，进入 P5。P5 不允许根据最终验证结果继续调 pilot 权重。

#### C-B：白点通过，但有色/留出改善不超过噪声

- 保留当前 70 点候选。
- multipatch 只作为诊断和验收报告。
- 不进入完整 70 点重算。
- 可以结束 CCT 新算法路线，转 HSI 前需记录此结论。

#### C-C：有色误差改善，但白点越界

- 判定求解目标实现错误或硬约束不足。
- 不放宽当前白点门槛。
- 修正词典序/可行域后只重跑 12 点。
- 连续两版仍失败则停止该路线。

#### C-D：只在 1800/20000 或极端 GM 失败

- 检查 basis 外推、gamut、active channel 和 RGB 先验。
- 若目标不可达，输出明确 `unreachable`，不得靠放宽门槛伪装。
- 可做一次只针对极端点的模型修正，但修正后必须重跑完整 12 点。

#### C-E：两次确认不一致

- 优先判定热态/漂移，不先改 solver。
- 失败确认成为新 thermal base，重建局部 Jacobian。
- 冷态样本不得继续进入 active secant 窗口。
- 稳定后完整重跑受影响点的两次确认。

#### C-F：前向模型 P3 为 seed-only

- 用模型只生成初值。
- 实拍反馈目标扩展为 neutral + multipatch residual。
- 仍保留现有 bounded Jacobian、Broyden、secant 和 thermal rebase。
- 若高维反馈无法稳定估计，退回白点反馈并把 multipatch 仅用于候选排序。

---
