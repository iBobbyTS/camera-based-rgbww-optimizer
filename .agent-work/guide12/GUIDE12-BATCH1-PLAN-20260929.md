# GUIDE12 批次1计划 — 原生曝光资格化 + all-off 环境诊断（冻结待执行）

日期：2026-09-29。状态：计划冻结，工程执行链（运行器 ambient 策略扩展 + 阶梯路径）下一步实现。
依据：`advisor/12/12.GUIDE.md` §2.2(4)、§2.3、§6 预算表。

## 本批要回答的科学问题

1. 满幅 R 主导、满幅 B 主导、高白通道负载三类灯带命令，在原生 CFA 域的合法曝光档是哪一档
   （`effective_white_level−2DN` 前瞻保护起点之上无大面积平台，且相邻档曝光归一化主平面/色度一致）？
2. 本实验室当前环境（无补光）在各实际曝光档对四个主 CFA 平面的贡献量 A 是多少？`z(on)−z(on−A)`
   的敏感性区间是否足以改变产品判定？

不在本批回答：任何模型/导数/容差结论（资格化帧不作独立模型验收帧，GUIDE12 §2.2）。

## 物理预算（GUIDE12 上限内的实际申请）

| 项 | 数量 | 上限依据 |
|---|---|---|
| 满幅R 阶梯帧 | 3（1/500, 1/400, 1/320） | 3类×最多6=18 |
| 满幅B 阶梯帧 | 3（1/500, 1/400, 1/320） | 同上 |
| 高白负载阶梯帧 | 3（1/10, 1/8, 1/6） | 同上 |
| all-off 帧（批前） | 2（1/400、1/8 各一） | ≤6类×2=12 |
| all-off 帧（批后） | 2（同上两档） | 同上 |
| **合计物理 CR3** | **13** | 18+12 内 |

无新增唯一命令预算消耗（3 个命令均为已存在命令；见下）。无 Ray 点亮帧（Ray 仅零态读回隔离证据）。

## 命令与满幅证据要求

- 类R：`{r:4095, g:0, b:0, cw:0, ww:0}`（actual max=4095，用户定义满幅）
- 类B：`{b:4095, ...0}`（同上）
- 类W：高白通道负载，采用 W2 已采用 2300/100 命令 `{ww:4095, r:1965, g:312, cw:0, b:0}`
  （2026-09-23 commands 账本 actual 读回 `{0,4095,1965,312,0}`，max=4095）
- 每次应用须有 apply 后 device_snapshot + readback；无读回记 unknown，不默认满幅。
- 阶梯只改相机曝光（nominal_shutter 冻结序列），不降低 Ray/strip 输出；不因慢档"看起来好"绕过削顶。

## 协议要点

- 每类：apply → dwell 120s → 3 帧相邻档（帧间隔≥15s）；同状态相邻档做曝光归一化一致性检查。
- 起点快门从既有锚点预测（C1 分层：满幅彩色 1/400；白基 1/8），先快后慢，首帧即最安全档。
- 每帧记录：原生逐平面 white level/min/max/p1/p99/mean/variance/MAD/近上限计数（v3 门已实现）、
  请求快门 vs MakerNote 实际曝光、渲染域画像（仅辅助，`rendered_rgb_exposure_profile`）。
- all-off：批首（点亮前、长关断后）与批末（隔离门后）各拍 1/400 与 1/8 两档；两源真实零读回为前置门。
  环境帧含环境+暗信号，不分离、不扣减（`unsubtracted_with_all_off_diagnostic` 策略，待运行器扩展）。
- 失败即停：任何帧质量/账本异常 → 保留失败根 + all_off 清理 + 零态读回，再分类（工程/科学/设备）。

## 停止分支（预冻结）

| 判定 | 名称 | 后续 |
|---|---|---|
| 存在档位：无平台、近上限计数<5%、相邻档归一化一致（|Δz|≤0.01） | `qualified` | 记录该档+余量，供 C12-2/W12-1 冻结快门 |
| 最快档已平台（1/500 仍触顶） | `measurement_window_unqualified_fast_edge` | 报告，不自动改 ISO/光圈 |
| 全部档位近噪底 | `measurement_window_unqualified_dark` | 报告，不叫 gamut 不足 |
| 环境敏感性上界改变产品判定 | `ambient_affects_verdict` | 先遮光/稳定环境后重复受影响目标 |

## 执行前工程清单（下一工作包）

1. 运行器扩展：`AMBIENT_POLICY_UNSUBTRACTED_WITH_ALL_OFF_DIAGNOSTIC`（不扣背景 + all-off 诊断帧）
   + `expected_native_raw_ambient_policy`/`validate_authorized_execution_plan` 分支 + ambient 逐帧快门。
2. `guide12.py` 增加 `build_guide12_batch1_plan()`（冻结阶梯/预算/门）+ `measure_guide12_batch1` 入口。
3. 单元测试：新策略校验、计划结构、阶梯相邻档一致性判定函数。
4. dry-run 写 spec 复核 → 设备可达性复查 → 执行（预计 25–35 分钟，可见终端 + 三次存活检查 + automation 交接）。

设备可达性（2026-09-29 已查）：ESPHome 灯带在线且零态；Ray get-cct 正常；相机桥 health ok。
