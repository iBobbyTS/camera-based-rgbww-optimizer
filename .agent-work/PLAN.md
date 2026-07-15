# Ray120c 远程相机观察者匹配总控计划

**计划状态：** active

**编写日期：** 2026-07-13；结构拆分：2026-07-14

**当前提交：** `17911bc feat(camera): add remote exposure backend`

**当前活动阶段：** `stage_1`

**当前阶段状态：** `code_complete_waiting_for_measurement`（P0-R 离线验收完成；未授权实机）

**上游设计：** `advisor/1/1.RESEARCH.md`、`advisor/1/1.PLAN.md`

---

## 1. 使用方式

本文件只负责导航、阶段锁和最新状态。详细规则已拆到 `.agent-work/PLAN/`，执行模型不得只读本文件后开始工作。

每次恢复任务按以下顺序读取：

1. 本文件。
2. `.agent-work/PLAN/00-CONTRACT.md` 全文。
3. 当前活动阶段文件全文。
4. `.agents/skills/camera-based-rgbww-optimizer/SKILL.md`。
5. `docs/README.md` 中对应命令。
6. `git status --short`；保留所有用户改动。
7. 用 CodeGraph 定位当前阶段代码，再读取未索引的配置/文档。

执行模型应连续完成当前阶段内已有明确处理规则的编码、测试、确定性诊断和获批实验，不因普通错误或小分支请求高级模型。只在阶段决策门或 `00-CONTRACT.md` 5.2 的高风险例外停止。

跨阶段必须同时满足：

- 当前阶段交接包完整。
- 高级模型在本文件写入明确出口决定。
- 下一阶段 prerequisites 满足。
- 涉及设备时另有用户明确实机授权。

技术放行不等于设备、安装、依赖、提交或 push 授权。

---

## 2. 计划文件

| 文件 | 执行内容 | 阶段末高风险决策 |
|---|---|---|
| `PLAN/00-CONTRACT.md` | 全局事实、安全、远程相机、产物、测试、归档 | 无；对所有阶段强制生效 |
| `PLAN/01-REMOTE-AND-P1.md` | P0/P0-R/P1：remote 迁移与 RAW 测量链 | Gate-1：测量链是否足以进入五通道建模 |
| `PLAN/02-BASIS-AND-ADDITIVITY.md` | P2/P3：五通道基底与随机混合 | Gate-2：主模型、分段模型或 seed-only |
| `PLAN/03-CCT-PILOT.md` | P4：4x3 multipatch A/B | Gate-3：是否值得扩大到 70 点 |
| `PLAN/04-CCT-FULL.md` | P5：完整 14x5、插值与独立验证 | Gate-4：CCT 候选处置及是否开始 HSI |
| `PLAN/05-RAY-HSI.md` | P6：Ray HSI 黑箱流形 | Gate-5：可分离或周期二维模型 |
| `PLAN/06-STRIP-HSI.md` | P7/P8：strip HSI、gamut、INT | Gate-6：产品语义、强度分支和候选冻结 |
| `PLAN/07-FINAL-VALIDATION.md` | P9：跨日独立验证、安装和审计 | Gate-7：安装、部分交付、保留或回滚 |

阶段文件保留完整实验分支。不要把阶段内的 B/C/D、G/H/I 子分支误当成新的高级模型断点；只有其结果会改变下一阶段架构、阈值或产品承诺时，才在对应 Gate 统一决策。

---

## 3. 阶段锁

| 阶段 | 状态 | 进入授权 | 允许的下一出口 |
|---|---|---|---|
| Stage 1：remote + P1 | `active_code_complete_waiting_for_measurement` | 已完成离线编码；未授权实机 | Gate-1 |
| Stage 2：basis + additivity | `locked` | 等待 Gate-1 | Gate-2 |
| Stage 3：CCT pilot | `locked` | 等待 Gate-2 | Gate-3 |
| Stage 4：CCT full | `locked` | 等待 Gate-3=`expand_to_70` | Gate-4 |
| Stage 5：Ray HSI | `locked` | 等待 Gate-4=`approve_stage_5` | Gate-5 |
| Stage 6：strip HSI | `locked` | 等待 Gate-5 | Gate-6 |
| Stage 7：final validation | `locked` | 等待 Gate-6=`freeze_candidates_for_stage_7` | Gate-7 |

锁定阶段允许读取以理解接口，不允许提前实现其专属模型、采集 runner 或实验。通用修复只有在当前阶段确实需要且有回归测试时才能提前抽取。

---

## 4. 当前不可回退事实

完整清单见 `PLAN/00-CONTRACT.md`。当前恢复任务最容易遗漏的是：

- 所有新实拍必须通过 `r6-camera-bridge` remote backend；本地 gphoto2 仅保留兼容和测试。
- 远程配置由脚本读取项目 `.env`；不得人工读取、source、打印或把 Token 放进 CLI/日志/JSON。
- API 文档：`http://ibobby-rpi-4.local:8088/v1/API.md`。
- 所有新实验固定使用 `config/location/locations-20260714-211759.json`。
- location SHA-256：`21f02328bff8b5ffcfc10c767e15cdefbf8bb883bc352eff6f0fb7ade38a8f80`。
- 当前默认 `config/white/white-lut.json` 仍是旧 4x3，不得覆盖。
- 当前最佳外置 70 点候选：
  `/Volumes/4T/temp/rgbww-optimizer/white-lut-calibration/14x5-off-cycle-refined-v2-20260713/white-lut-calibration.json`
- 最佳候选仅完成最高风险 10 点最终 60 秒 off/on 独立复测，不能声称 70/70。
- P1 当前仍为 fail；P2 被硬阻塞。
- 新实验必须 Python `finally` 与 shell `trap` 双关灯，且每张照片只能亮 Ray 或 strip 之一。

---

## 5. 已完成基线

- [x] 白点-only 14x5 候选和热态 rebase 修复。
- [x] 原生 Bayer `R/G1/G2/B` patch statistics、ambient subtraction 和 JSON-only 输出。
- [x] RAW repeatability/linearity/G1G2 分析模块与 synthetic tests。
- [x] CR3 recorded exposure 单一入口；v6/v7 全部保留 CR3 已重算。
- [x] total/global scale/shape residual 拆分与 non-reference 汇总。
- [x] native RAW exposure meter 和可选 `meter_fn`。
- [x] P1 5 张 preflight-only 与 31 张 full dry-run 计划能力。
- [x] remote config/capture backend、原子 CR3 落盘、有界 busy retry。
- [x] location picker/checker remote backend。
- [x] 最新远程相机点位文件已生成并冻结 hash。

历史 P1 证据：

- v6：`/Volumes/4T/temp/rgbww-optimizer/raw-observer-validation/20260714-030700-p1-provenance-envelope-v6/analysis-recorded-exposure-v1.json`
- v7：`/Volumes/4T/temp/rgbww-optimizer/raw-observer-validation/20260714-035100-p1-exposure-diagnostic-v7/analysis-recorded-exposure-v1.json`
- v6 `31/31`、v7 `27/27` 使用 `Canon:ExposureTime`，无 nominal fallback。
- 剩余高信号 shape residual 在 Ray/strip 同向，当前路线是先低信号 D1，不直接运行 strip-only P1-D。

---

## 6. 当前阶段清单

Stage 1 详细步骤见 `PLAN/01-REMOTE-AND-P1.md`。

### P0-R 离线迁移

- [x] 所有新实验 runner/measurement 默认点位迁移到 `locations-20260714-211759.json`。
- [x] P1/P1-D 和现有正式硬件 runner 接入可注入 remote backend。
- [x] 新增无拍摄 `camera_remote health --json` 与 `config --json`。
- [x] dry-run 不读取 `.env`、不访问网络、不调用灯具。
- [x] remote P1 计划冻结 backend、location path/hash 和双 cleanup。
- [x] 密钥脱敏、remote failure、atomic save 和 fake cleanup 测试通过。
- [x] 完整测试、`git diff --check`、CodeGraph sync 通过（243/243）。

### P1 实机门

- [x] P0-R 标记 `code_complete_waiting_for_measurement`。
- [ ] 用户明确批准实机操作。
- [ ] remote health/config、Ray、ESPHome 检查通过且只读检查不拍照。
- [ ] remote 5 张 D1 preflight 完成。
- [ ] 同配置 31 张 full P1 完成或按既定失败分支停止。
- [ ] Gate-1 交接包完成，等待高级模型决策。

---

## 7. 下一条唯一动作

等待用户明确批准 Stage 1 的 remote P1-D1 实机预检。没有新的实机授权，不得访问 `/health`、`/v1/config`、`/v1/capture`、Ray 或 ESPHome。

获批后的第一条实验路线固定为：remote health/config 和双灯检查，然后运行新目录下的 5 张 `--camera-backend remote --location-config config/location/locations-20260714-211759.json --preflight-only --target-max 19661`。不得跳到完整 P1、P1-D 或 P2。

---

## 8. 当前离线交接

```text
当前阶段：stage_1
阶段状态：code_complete_waiting_for_measurement
当前提交：17911bc
工作区状态：dirty（保留既有 PLAN 拆分；P0-R 代码、测试、docs、skill 和计划状态未提交）
用户授权范围：offline_only
运行目录：tmp/raw-observer-validation/offline/p1-recorded-exposure-low-signal-remote-preflight-dryrun-20260714
分析文件：无（仅生成离线 plan.json，未采集、未分析）
输入 hash：location=21f02328bff8b5ffcfc10c767e15cdefbf8bb883bc352eff6f0fb7ade38a8f80
已完成步骤：正式 runner remote backend 注入；health/config CLI；最新 location 迁移；remote busy/失败下载/原子落盘/hash/双关灯/fake backend 测试；remote bracket 快门 choices 由同一 backend 读取且禁止回退本地 gphoto2；remote provenance 冻结 ISO/光圈/快门 choices 并验证不含 Token；五张 preflight dry-run；243/243 tests；git diff --check；codegraph sync
失败和保留证据：无离线验收失败；未访问任何设备或远程 API
改动文件：control/camera_gphoto2.py、control/camera_remote.py、measurement/raw_mosaic_patches.py、optimization/measure_channel_response.py、measure_raw_observer_validation.py、measure_raw_shutter_response.py、measure_white_endpoints.py、measure_white_lut.py、white_calibration_common.py、tests/test_camera_remote.py、tests/test_measure_raw_observer_validation.py、tests/test_stage1_remote_migration.py、docs/README.md、项目 skill、两个 tmp shell wrapper、本 PLAN.md
推荐出口：保持 stage_1，等待 named_experiment 授权
高级模型决定：pending
下一条唯一动作：用户明确批准后，按 7.1 顺序执行 remote health/config 与双灯检查，再运行已冻结配置的五张 P1-D1 preflight；未批准前停止
```

## 9. 状态更新模板

每次实际工作后立即更新，不得到阶段末一次性补写：

```text
当前阶段：stage_1..stage_7
阶段状态：not_started | in_progress | code_complete_waiting_for_measurement | running | at_decision_gate | pass | conditional_pass | fail
当前提交：
工作区状态：clean | dirty（列出相关文件）
用户授权范围：offline_only | device_probe | named_experiment | install | commit | push
运行目录：
分析文件：
输入 hash：
已完成步骤：
失败和保留证据：
推荐出口：
高级模型决定：pending | approved_next_stage | repeat_current_stage | rollback_to_stage | stop_route
下一条唯一动作：
```

高级模型作出阶段决定后，必须同时更新“阶段锁”“当前活动阶段”和“下一条唯一动作”。仅在聊天中同意而不更新本文件，不算跨阶段授权。

归档规则见 `PLAN/00-CONTRACT.md` 第 17 节。
