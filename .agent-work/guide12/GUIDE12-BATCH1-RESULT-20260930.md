# GUIDE12 批次1结果 — 原生曝光资格化 + all-off 环境诊断

日期：2026-09-30（UTC）。运行根：
- `D:/rgbww-optimizer/guide12-batch1/formal-b1-20260929-r1`（13帧，工程失败已恢复，见根内 recovery-note）
- `D:/rgbww-optimizer/guide12-batch1/formal-b1-white-reverse-20260930-r1`（1帧反向复查）
- `D:/rgbww-optimizer/guide12-batch1/formal-b1-white-corrected-20260930-r1`（2帧修正臂）

分析：`D:/rgbww-optimizer/guide12-batch1/derived/b1-exposure-qualification-20260930.json`
（生成脚本 `tmp/analyze_b1_exposure_20260930.py`）。物理预算：16 CR3（资格化 12≤18 + all-off 4≤12）。

## 判定（预冻结规则：四平面合格 + 无削顶 + 相邻档 |Δz|≤0.01）

| 类 | 命令 | 判定 | 采用档 | 关键数值 |
|---|---|---|---|---|
| 满幅B | b=4095 | **qualified** | **1/320** | 四平面 accepted；p99 max 5355（余量 11026 DN）；1/400↔1/320 对 Δz≤9e-4 |
| 高白负载 | ww=4095,r=1965,g=312 | **qualified**（修正臂） | **1/100** | 1/100 与 1/80 全平面 accepted，p99 max 9126/11328；Δz=[-0.0006,0.0029]；1/80 与 W2 历史 ~12042 吻合 |
| 满幅R | r=4095 | **measurement_window_unqualified**（结构性） | — | B 平面在 1/500..1/320 全程贴黑（min≈black 512，noise_frac=1.0）；R 平面同档仅 2261 max；纯R 的 R:B 展宽 ~46dB，四平面主层在单一曝光内不可同时有效 |

## 修正记录（保持透明）

1. 白类初梯错误锚定在 C1 色彩档（1/8）——W2 白线实际运行 1/80（017 帧记录 0.0125s、块 max 12042）。
   1/10–1/20 的触顶帧保留为错误锚臂证据；**不存在灯带亮度变化**。修正臂 1/100+1/80 在类预算内（白类共6帧）。
2. 主根 13 帧完成后被事后校验器时序 bug 误拒（ENGINEERING_OR_HARNESS_FAILURE）；修复后重放校验 PASS，
   不重拍（commit 294131b）。

## all-off 环境结论

- A/on 比值：白系 ~1e-5；B 系（1/400 档配蓝类）最大 R 轴 0.0034。
- z(on)−z(on−A)：白系 {5.1e-7, 1.1e-5}；B 系 {0.0032, -1.2e-4}——全部远低于 0.01 产品容差预算，
  **环境项不改变当前判定**；批内漂移 end/start ≈1.0–1.3。
- 环境帧只作诊断记录，不做任何扣减（策略 unsubtracted_with_all_off_diagnostic）。

## 对后续批次的输入

- W12-1 白线 strip 快门冻结：**1/100**（满幅白命令首选，余量 7257 DN）；1/80 为次选确认档。
- C12-2 彩线满幅B 类命令：**1/320** 合格；纯R 类命令四平面主层结构性不可满足——凡含显著白/绿含量的
  实际 HSI 满幅命令不受此限制（C1 实际命令均含白通道），solver 输入不得使用纯R 帧。
- 曝光资格化帧不作独立模型验收帧；每帧 MakerNote 实际曝光与名义一致（0.05↔1/20 等，逐帧核验）。
