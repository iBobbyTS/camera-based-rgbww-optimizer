# 阶段 5：Ray HSI 黑箱表征

**覆盖原阶段：** P6

**进入条件：** Gate-4 已给出 CCT 最终处置，并明确 `approve_stage_5`。

**阶段目标：** 只控制 Ray，测出 SAT=0、HSI/RGB 端点和粗网格，选择可验证的目标流形结构。

**不得跨越：** 在 Ray 流形分支冻结前，不控制灯带拟合 HSI，也不先写二维/三维 LUT。

## 执行顺序

1. 实现 Ray-only runner 和分析模块，完成 fake 硬件、周期 Hue 和安全测试。
2. 获授权后依次完成 SAT=0、RGB/HSI 端点与粗网格。
3. 对异常点按 H-C 先重拍；通信/热态异常按 H-D 使 run 失效。
4. 比较可分离与二维弯曲模型，但只生成候选和交叉验证结果。
5. 到达 Gate-5 后停止，不实现 strip HSI 求解器。

## 高级模型决策门 Gate-5

允许出口：`separable_manifold_HA`、`full_periodic_2d_HB`、`targeted_resample_HC`、`invalidate_and_repeat_HD`、`stop_hsi_route`。决策必须冻结 SAT=0 处理、HSI/RGB 是否共享方向、Hue 周期边界、SAT 插值类型及需要加密的局部区域。

---

## 12. P6：Ray HSI 黑箱表征

只有 CCT 路线形成明确“安装新候选”或“保留旧候选”的闭环结论后开始。

### 12.1 代码

```text
src/camera_based_rgbww_optimizer/optimization/measure_ray_hsi_manifold.py
src/camera_based_rgbww_optimizer/measurement/ray_hsi_analysis.py
tests/test_ray_hsi_analysis.py
tests/test_measure_ray_hsi_manifold.py
```

本阶段只控制 Ray，不控制 strip。仍需 shell/Python 双关灯。

### 12.2 SAT=0

Hue：`0,60,120,180,240,300`，SAT=0，每点两次；一个 Hue 做 5 次。

分支：

- Hue 影响不超过重复性：合并为一个 zero-sat anchor。
- Hue 影响超过 `3 sigma` 且重复：保留 Hue-dependent SAT=0 曲线。
- 影响不稳定：查 Ray mode/readback/热态，不选择模型。

### 12.3 HSI 与 RGB 端点

比较 Ray RGB R/G/B/C/M/Y 与 HSI 对应 Hue、SAT100：

- 若仅全局 scale 不同，可共享方向模型但保留 mode scale。
- 若 chroma 路径不同，HSI 和 RGB 必须独立建模。
- 若有白通道迹象，记录但不推测 Ray 内部 PWM。

### 12.4 粗网格

- Hue：`0..330` 每 30 度。
- SAT：`5,20,50,80,95,100`。
- INT=100。
- 共 73 个基础状态，加锚点和重复。

### 12.5 流形分支

#### H-A：近似可分离

条件建议：至少 90% 中间 SAT 节点的 affine 正交残差不高于约 `2x` 重复性底噪，且无系统 Hue 区域偏差。

动作：

- 保存 zero-sat anchor。
- Hue 使用周期端点曲线。
- 每 Hue 的 SAT 使用单调曲线。

#### H-B：存在稳定二维弯曲

- 使用完整周期二维 `t(h,s)`。
- 只在高曲率区域自适应加点。
- 不强制标准 HSV/HSL 几何。

#### H-C：只有局部异常

- 先重拍异常点。
- 重复后仍异常才加密节点。
- 不用单次异常决定二维模型。

#### H-D：Ray 读回与命令不一致或状态漂移

- 立即停止并关灯。
- 不拟合该 run。
- 修复通信/模式/热态后新 run 重测。

---
