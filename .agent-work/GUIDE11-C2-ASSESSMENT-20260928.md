# GUIDE11 C2 每 Hue SAT 可达范围评估（2026-09-28，离线）

产物：`D:\rgbww-optimizer\guide11-c1\derived\c2-reachability-assessment-20260928.json`
（repo 副本 `tmp/c2-reachability-assessment-20260928.json`，脚本
`tmp/assess_c2_reachability_20260928.py`）。输入仅用 C1C 确认分析（8 节点新鲜
Ray 夹持 + 有效确认观测）与 C3 锚点自检网格。

## 方法

每主 Hue 用自身 S50→S100 新鲜 Ray z 段定义径向（SAT 等效），正交方向为切向
（Hue 等效，度数标尺取同 SAT 相邻 Hue 锚点）。一阶局部分解；切向分量保守地
包含色度形状失配贡献，Hue 等效误差是上界读数。

## 产品层判定（2° / 2pp，SAT≥25）

| 节点 | ΔSAT (pp) | ΔHue (°) | 径向 z | 切向 z | 产品层有效 |
|---|---|---|---|---|---|
| H0/S50 | −16.6 | +11.4 | −0.475 | +0.199 | 否 |
| H0/S100 | +27.8 | −11.1 | +0.798 | −0.387 | 否（n=2 有效确认） |
| H60/S50 | −2.0 | −6.8 | −0.022 | −0.100 | 否（SAT 达标、Hue 超差） |
| H60/S100 | −54.4 | −2.9 | −0.585 | −0.100 | 否（gamut 饱和不足） |
| H180/S50 | +24.8 | −42.5 | +0.399 | −0.413 | 否 |
| H180/S100 | −25.2 | −21.5 | −0.404 | −0.414 | 否 |
| H240/S50 | +16.9 | **+0.4** | +0.325 | +0.007 | 否（Hue 完美、SAT 超差） |
| H240/S100 | −33.1 | **+0.3** | −0.638 | +0.006 | 否 |

误差结构分层明确：H240 为纯 gamut 边界型（色相可复制、饱和度有界）；H60 接近
SAT 容差但色相超差；H0/H180 切向形状失配主导（H180 的 −42.5° 应读作形状失配
上界，不代表菜单 Hue 旋转了 42°）。

## C2 三量（当前证据）

- `s_best_tested`：四 Hue 均为 **0**（无产品层有效节点；SAT0 白光主线有效）。
- `covered_intervals`：空（S50 与 S100 皆无效，且无中间点）。
- `search_upper_request`：S100 四 Hue 均已测试，状态
  `tested_bounded_best_outside_product_tolerance`（非物理不可达证明）。

## 判定：S25 下探批必要

按 GUIDE11 C2（S100→S50→必要时 S25；到 S25 仍无效则停止），四个主 Hue 均需
S25 层：每 Hue 一块（Ray 夹持 + strip 模型压缩命令观测），预计 12 张 ≈ 2.5h。
S25 命令由 C3 模型的 hue-first 白混合压缩策略给出（模型最低层为 S50）。

## 双会话路由（设备单 runner 规则）

- C4 留出批（`formal-c4-20260928-r1`，30 张）由并行会话拥有并监督（其一次性
  automation ~04:55 唤醒）；C5 计划亦在其路线内。
- **本会话认领 C2-S25 批**：在 C4 结束后、设备空闲（无任何活跃
  `measure_*` runner 进程）的第一个窗口启动；启动前必须复核单 runner 规则。
  若接管会话已在设备上启动 C5，则 C2-S25 顺延至其后，不得并发。
- 任一会话启动设备批次前检查：`Get-CimInstance Win32_Process` 过滤
  `measure_guide11` / `measure_p7` 无活跃进程。

### 2026-09-28 06:10 路由更新：并行会话监督链断裂，本会话接管全程

并行会话的一次性 automation 于 04:55 触发后 completed 且未续期（重现其
00:0x 的中断模式）。C4 runner 为独立后台进程仍在健康推进（06:00 时 15/30），
预计 ~09:05 完成。**本会话（automation-89cfc063，120 分钟循环）现为唯一监督
与推进所有者**，路线：08:08 唤醒守候 C4 完成 → 冻结分析器
`tmp/analyze_c4_holdout_20260928.py`（已于看到结果前写好）→ C4 结果文档 →
C2-S25 发射（12 张）→ C5 INT 批 → C6 打包。若并行会话复活：读本节与
git log，遵守单 runner 检查，不得重复启动已在运行的批次。

无新增 Human/Advisor 门。

### 2026-09-28 12:15 UTC 预建收口：C5/C2-S25 发射就绪（91ca48f + dfd5b3e）

本会话（89cfc063 循环监督所有者）在 C4 运行期间完成离线预建：

- C4 冻结分析器 `tmp/analyze_c4_holdout_20260928.py` 定稿：运行中守卫、C1
  锚点包络对照、G9 同源白锚（strip 白=G9 best-repeat ×2 散布 0.0003，
  即模型白层命令；Ray 白=G9 bracket）做低 SAT 径向比、锚图反解已往返
  自检（锚点与内点 residual=0）。
- C5 INT 分离性 builder/CLI/注册/测试全部就绪（33 测试过，离线计划验证
  PASS；dry-run 48 张表已核对：Ray 快门按 100/INT 缩放锚点并落在合法
  1/3 档表，strip 命令线性缩放，白光纯命令按亮度阶梯下行不再钉 1/400）。
- **修复发射阻塞**：C2-S25 计划原继承 C4 授权身份，runner 作用域检查
  会在发射时拒绝（experiment_id 不匹配）。已注册
  direct_guide11_c2_sat_reachability_s25_v1 并加 C4/C2/C5 作用域回归测试。
- C4 完成后的既定路线不变：分析器 → C4 结果文档 → C2-S25 发射
  （`measure_guide11_c2_s25 --execute --allow-device-control --run-name
  formal-c2s25-20260928-r1 --command-model D:\rgbww-optimizer\guide11-c1\
  derived\c3-command-model-20260928.json --output-dir D:\rgbww-optimizer\
  guide11-c2`，12 张）→ C5（48 张）→ C6 打包。各批发射前做单 runner
  进程检查；发射后 3 次 1 分钟间隔活性检查再配监控。
- 本会话无 CronCreate/CronDelete 工具：唤醒依赖后台任务退出自动通知 +
  89cfc063 循环心跳。并行会话若复活，读本节后按单 runner 规则继续。
