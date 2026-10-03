# GUIDE12 执行状态 — 2026-09-29

依据：`advisor/12/12.GUIDE.md`（不可变科学指导）、`CODEX_GUIDE12_IMPLEMENTATION_PROMPT.md`、
`GUIDE12_DATA_PACKAGE_REQUIREMENTS.md`。GUIDE11 证据包
（SHA-256 `5c348c023027e96b149edf41b4654d26b2dfc26e868add29f3b5e8243f9d5e65`）是审阅基线。

## 阶段边界（GUIDE12 §0）

- 研究对象：Ray CCT brightness=100%、HSI intensity=100%（API 1000↔100%），灯带实际五通道
  PWM `max(actual)=4095`（用户定义满幅，非全局光通量最大）。隔离/reset/all-off 真实关灯不受该约束。
- 停止低档实验：不再新增 Ray/strip INT50/20/5 或 strip max3072/2048；旧数据保留为历史诊断。
- 撤回的 GUIDE11 采用依据：45/70 独立认证、中带连续域、(0,25) 四主 Hue 边界、产品层 SAT0、
  C4 低/中 SAT 通过、有界搜索=硬件极限。

## 已完成（离线确定性修正，2026-09-29，本仓库）

| # | 修正 | 位置 | 证据 |
|---|---|---|---|
| 1 | W2 割线代数：A=u−u0、B=r(u)−r(u0)，唯一基点=最低E观测，基点不再被同命令帧覆盖；记录命令差秩/敏感度秩/奇异值/基点误差/active face | `optimization/guide11.py` `build_guide11_w2_candidate_rows` | `tests/test_guide12.py` 截距无关回归例（r(u)=a·u+b，b≠0 仍精确抵消） |
| 2 | W2 49组同候选新鲜配对 + 9采用命令 E 历史/新鲜对照 + 25节点命令差秩诊断 | `tmp/guide12_offline_corrections_20260929.py` Part A → `D:/rgbww-optimizer/guide11/guide11-w2/derived/w2-fresh-pairing-audit-20260929.json` | 49对全配对；1800/70→1.115872、2000/100→1.11843 越界，7/9 容差内（与 Advisor 复算一致）；命令差最大秩1 |
| 3 | W8 有符号单位重建（error_signed/tolerance/abs_normalized_error 分离；旧 artifact 只读） | 同上 Part C → `guide11-w8/derived/guide11-white-final-report-signed-20260929.json` | 70节点：61 W6 + 9 W2（fresh Ray 同块）；恒等式回放测试 |
| 4a | 原生 RAW 削顶门：near_white_rail_fraction（≥wl−2DN）、white_rail_plateau 无条件硬失败、p1/p99 分位数；raw-observer v3 | `measurement/raw_mosaic_patches.py`、`config/camera/raw-observer.json` | 平台（16382/16383, var=0）在旧 clipped_fraction=0 下也拒绝；分域不倒置 |
| 4b | 全量 raw-rail 审计（guide11+guide9 组 1071 帧，只读） | 同上 Part B → `guide11/derived/raw-rail-audit-20260929.json` | 38 平台帧（C1 r6/r7/r8=29 与 Advisor 一致；另发现 diag 5、c1b2 各 rerun 4）+1 触顶帧；37 个旧门漏检 |
| 4c | `frame_exposure_profile` 标域改名 `rendered_rgb_exposure_profile`（渲染RGB域，辅助诊断，不能推翻原生判定；旧名保留为别名） | `measurement/frame_exposure.py` | 域字段+别名恒等测试 |
| 5 | 满幅证据：actual payload 驱动，无读回=unknown 不默认 true | `optimization/guide12.py` `fullscale_evidence` | 单元测试（4095/unknown/3133 三态） |

全量测试：602 项，新增 14 项全过；138 错误/3 失败与 HEAD 基线完全一致（均为本机不存在的
Mac 路径数据依赖，非本次改动引入）。

## 关键数值结论（供 W12-1 队列）

- 9 个 W2 采用命令独立 FAST 确认全部 `not_acquired`；按同候选新鲜 Ray：7 个 E<1，
  1800/70（1.1159）与 2000/100（1.1184）越界。
- 25 个受审节点已有命令差全部秩≤1：五通道方向未搜索，旧导数不能当当前导数真值。
- C1 主 r8 的 24/32 strip 候选为上限平台帧，已从 GUIDE12 导数/选择/方差输入中排除
  （测量统计与失败身份保留于 rail 审计）。
- 历史统计不含近上限像素分数：部分污染不可复算，只有保守触顶标记。

## 待办（按 GUIDE12 科学顺序）

1. **批次1（观测性）已完成（2026-09-30）**：16 CR3。结果 → `GUIDE12-BATCH1-RESULT-20260930.md`：
   满幅B @1/320 qualified、高白负载 @1/100 qualified（白线快门锚=1/80 而非 C1 1/8 档，1/10–1/20 触顶
   为锚定错误臂，无亮度变化）、纯R 四平面主层结构性不可满足（R:B ~46dB）；all-off 环境项
   z 敏感性 ≤0.0032，不改判定。工程记录：事后校验器时序 bug 一次（恢复未重拍）；分析脚本
   g_corr 漏项一次修正。派生：`guide12-batch1/derived/b1-exposure-qualification-20260930.json`。
2. **N2 重复性（进行中，2026-10-03）**：设计冻结（`guide12/GUIDE12-N2-DESIGN-20261002.md`）+
   完整实现（`optimization/guide12_n2.py`、`measure_guide12_n2.py`、运行器 N2 路由与自包含校验器，
   13 项行为测试）。Ray HSI 快门实测定档：H0/S100 @1/1000、H240/S100 @1/2000（阶梯 r2-r4 证据）；
   strip 20000/100 @1/160。**会话 1 完成**：formal-n2-session1-r5（36 帧 = 24 主 + 12 burst，
   30 pass + 6 彩态 near_noise_only 记录、12 满幅态验证；r1-r4 工程失败根保留——formal 时序身份、
   ambient 集成回退、彩态特征容忍、校验器自包含四次修复链）。all-off 诊断剥离（batch1 A/on 证据
   ≤0.0032；分析需要时按 batch1 schema 补专用运行）。会话 2/3 待跨时间会话（需明确分隔）。
3. **W12-1（已完成，2026-10-02）**：开放队列 18 节点全部处理——**17 qualified + 20000/0
   reference/operating_limited**（修正链至 E=0.0748 但认证被 20000K Ray 间歇漂移阻断，留 W12-2 复测）。
   结果与方法库沉淀 → `guide12/GUIDE12-W12-RESULT-20260930.md`。实现：
   `optimization/guide12.py`（`build_guide12_w12_open_queue`/`guide12_w12_probe_candidates`/
   `solve_guide12_w12_face_step`/`build_guide12_w12_block_plan`）+ 执行 CLI
   `optimization/measure_guide12_w12.py` + 运行器 W12 路由与事后校验器
   （`direct_guide12_w12_fullscale_bounded_v1`）。face 步为共享
   `bounded_least_squares` 盒约束枚举解（(mired,duv) 子空间求解、K/mired 不当独立秩、
   face 通道锁定、单步≤768 码、就近取整后夹回盒内）；探针设计 = u0 复测 + 3 个
   单轴 +768 码探针（对面白/蓝/红优先，绿最后）。strip 快门冻结 1/100（批次1白线）+
   节点级 1/125 覆盖（预检超限时，白点为同快门比值导出量）；Ray 快门沿用 W2 冻结表；
   离线曝光预检（duty 比例缩放 W2 实测 raw max，上限 15000 DN）。
   块结构：Ray before + ≤4 strip 候选 + Ray after，各观测独立 FAST off600→命令120→capture。
4. **C12-1**：Ray HSI 真映射（真 HSI S0 作 SAT0；Ray 自反解留出≥10；映射预算 Hue0.5°/SAT0.5pp）。
5. W12-2/3/4、C12-2..5 按 GUIDE12 §4/§5。
6. 阶段结束交付 `GUIDE12-COMPLETE-PROCESSED-EVIDENCE-<日期>.zip`（合同：
   `GUIDE12_DATA_PACKAGE_REQUIREMENTS.md`）。

预算不机械相加；每个 batch 先列问题、unique-command/physical 预算、fullscale、参考与停止分支。
