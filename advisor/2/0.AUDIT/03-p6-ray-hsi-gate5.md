# P6 Ray-only HSI 实验与 Gate-5

## 1. 实验目标

P6 不控制灯带，只把 Ray120c 当作黑箱，测量其 HSI 数值在固定相机观察者下形成的颜色流形。核心问题是：

- SAT=0 是否真的与 Hue 无关；
- HSI SAT100 是否等同 Ray RGB 端点；
- SAT 是否能用 zero 与 endpoint 的单参数仿射混合表示；
- Hue 是否周期连续；
- 哪些局部区域需要加密。

## 2. 完整性和安全证据

运行目录：

`/Volumes/4T/temp/rgbww-optimizer/ray-hsi-manifold/p6-ray-hsi-remote-20260717-0403-retry1`

结果：

- `run.json status=complete`；
- 106/106 captures；
- 106 个非空 CR3；
- 106 个 recorded-exposure measurement report；
- 无 `failure.json`；
- 无 `.npy`；
- 528 条 command audit event；
- 105 条 Ray HSI/RGB command/readback，零 mismatch；
- 每张照片前 strip 显式关闭；
- Python `all-off` 和 shell `trap all-off` 均成功；
- 最终 ESPHome 五通道为 0，Ray intensity 为 0。

冻结 hash：

- `run.json`：`1c208227e453992a443a782f57693d56adaa3752271f88254dd2a370d7d3a357`
- `plan.json`：`63f4b6127d94969a168d0c2894deff7b0e2c235d333dac8b2f2421fb220a20ce`
- `ray-hsi-analysis.json`：`39dc23229be42615669ae843773c1f04972802b54635ccf36b7ee2287d53e034`

## 3. 关键测量结果

### 3.1 SAT=0

- scale-removed Hue effect maximum：`0.0011702`；
- repeatability 3-sigma proxy：`0.0014817`；
- Hue effect 未超过 3-sigma。

结论：SAT=0 的**颜色方向**可使用 pooled zero anchor，但 Ray 在 SAT=0 仍有 Hue-dependent brightness scale；亮度信息不能一起抹平。

### 3.2 HSI 与 RGB endpoints

六个主色端点的 scale-removed residual 为：

- 最小 `0.0079226`；
- 最大 `0.1853840`。

全部超过重复性，不能把 HSI SAT100 与 Ray RGB 模式当作相同方向。当前 HSI 和 RGB 必须保持独立模型。

### 3.3 可分离性

两个 affine 候选都明显不足：

- pooled SAT0：约 `45.0%` 中间点在 `2x repeatability` 内；
- periodic Hue-dependent SAT0：约 `46.7%`；
- 较优候选 P90 residual：`0.024747`；
- maximum residual：`0.052402`。

失败覆盖 10/12 个 Hue 和全部中间 SAT 档，不是少量离群点，因此不适合通过局部补拍挽救 affine 模型。

### 3.4 径向与周期性

- 12/12 Hue 的 radial SAT progress 单调；
- Hue 边界必须按周期处理，`360 == 0`；
- 初始插值采用无过冲 periodic/piecewise-linear；
- 不使用普通非周期 cubic，也不假设 HSL/HSV 几何。

## 4. Gate-5 决定

冻结分支：`full_periodic_2d_HB`。

模型合同：

1. Hue 使用周期分段线性插值；
2. SAT 使用分段线性、无过冲插值；
3. SAT0 共享颜色方向，但保留周期 Hue-dependent brightness scale；
4. HSI 与 RGB endpoint 独立；
5. 只使用 P6 所有目标共同接受的 58 个 native-Bayer feature 构造第一版坐标；
6. 不匹配绝对亮度。

建议加密区域：

- wrap `330..90`，SAT `20/50/80/95`；
- Hue `240..330`，SAT `20/50/80`。

## 5. Advisor 不需要重做的决定

除非发现 provenance、算法实现或数据文件损坏的具体证据，不建议 advisor 要求：

- 重拍 P6 全部 106 点；
- 回退到可分离 affine 模型；
- 合并 HSI/RGB endpoint；
- 把 SAT0 的 Hue-dependent brightness 误认为颜色方向差异；
- 用理论 HSL/HSV 坐标替代相机测得流形。

P6 当前的不确定性是模型插值和 feature 子集在**灯带闭环**中的工程效果，这应由 P7 pilot 和 holdout 检验，而不是继续扩大 Ray-only 网络。

