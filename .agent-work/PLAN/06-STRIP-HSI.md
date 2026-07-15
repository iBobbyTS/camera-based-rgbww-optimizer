# 阶段 6：灯带 HSI、Gamut 与强度

**覆盖原阶段：** P7、P8

**进入条件：** Gate-5 已冻结 Ray HSI 目标流形。

**阶段目标：** 生成 INT100 灯带 HSI 候选、测量精确 gamut 边界，再判断 INT 是否可分离。

**不得跨越：** 不得隐藏不可达 Hue/SAT，不得在 INT 分支未定前冻结最终产品语义，不得自行进入最终验证。

## 执行顺序

1. 实现 P7 求解、周期插值和显式 gamut 状态。
2. 获授权后完成 INT100 节点、随机留出和 `s_exact_max(h)` 搜索。
3. P7 通过后连续执行 P8 的强度采样；无需在 P7/P8 之间额外等待高级模型，除非需改变 gamut 产品语义。
4. 比较 I-A/I-B/I-C，完成对应最小模型和独立留出，不均匀扩成三维网格。
5. 形成 Gate-6 交接包并停止，不冻结或安装未审阅候选。

## 高级模型决策门 Gate-6

高级模型冻结：faithful/gamut-compressed/hue-unreachable 的公开语义、`s_exact_max` 表示、I-A/I-B/I-C 强度分支、支持的 INT 范围、最终 CCT/HSI 候选 hash 和 P9 验证矩阵。若数据规模不可控，应缩小承诺而不是批准无界加点。

允许出口：`freeze_candidates_for_stage_7`、`repeat_targeted_stage_6`、`restrict_product_range`、`stop_hsi_route`。

---

## 13. P7：灯带 HSI 候选和 gamut

### 13.1 求解优先级

1. Hue 误差。
2. Ray 等效 SAT 进度误差。
3. neutral/multipatch 误差。
4. 命令连续和 0/360 周期连续。
5. 白通道软先验。
6. headroom、功耗和敏感度。

不能只优化整体 RAW RMSE。

### 13.2 首轮节点

- 使用 P6 已测粗网格。
- 经验基底生成初值，实拍反馈修正。
- 保存 CW/WW/R/G/B、white/rgb sensor fraction、active channel、condition number 和 sensitivity。

### 13.3 `s_exact_max(h)`

每个 Hue 从低 SAT 向上搜索：

- 最后一个精确可达点。
- 第一个超门槛点。
- 边界附近二分或加密。
- 保存边界通道和原因。

分支：

- 请求 SAT 在边界内：`faithful`。
- 请求 SAT 超边界：Hue-preserving compression，并返回 `gamut_clipped=true`。
- Hue 本身不可保持：返回 `hue_unreachable`，不得只报 SAT 压缩。
- 边界不平滑：增加 Hue 节点或检查 active-set 切换，不能直接平滑掉真实不可达区。

### 13.4 插值

- Hue 优先周期 cubic 或周期分段插值。
- SAT 优先单调 PCHIP 或分段线性。
- 插值后检查 0..4095、gamut、active set 和 0/360。
- 若插值命令预测失败，可改为插值 Ray 目标后重新求解，但必须评估运行成本和确定性。

P7 只有 INT=100 的节点与随机留出通过后才进入 P8。

---

## 14. P8：HSI INT 强度维度

测试 INT：`100,50,20,5`，覆盖 SAT0、R/G/B/C/M/Y、SAT50、最难 Hue、white-heavy 和 RGB-only 点。

比较：

```text
t(h,s,I) ~= alpha(I,h,s) * t(h,s,100)
```

分支：

### I-A：颜色与强度可分离

- HSI 色彩 LUT 只保留 INT100。
- 用一维 Ray 相对强度曲线缩放。
- 再经过各通道 code-duty 反查。
- 在 INT5 验证量化和 PWM 色偏。

### I-B：仅低强度偏色

- 增加 `1,5,10,25,50,100` 稀疏修正。
- 优先 per-channel correction，不扩成均匀三维 LUT。

### I-C：Hue/SAT 与 INT 广泛耦合

- 使用稀疏局部修正层并自适应加点。
- 若数据量不可控，缩小产品承诺到 INT100 或受限 INT 范围，明确报告。

默认亮度语义为“复制 Ray 相对强度曲线，允许 Ray100 与 strip100 存在全局比例”。若未来要求绝对照度，必须另立测量计划。

---
