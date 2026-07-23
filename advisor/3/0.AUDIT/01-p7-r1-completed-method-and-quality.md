# P7-R1 及前置阶段：已完成部分、方法与质量补充

## 说明与范围

本文是本轮 `advisor/3/0.AUDIT/` 的主报告。上一轮基线仍保留在 `advisor/2/0.AUDIT/`，不在本轮覆盖。
本文依据 `advisor/2/1.GUIDE.md` 回写截至 2026-07-19 已完成的实现、实机实验、分析方法和质量等级，
重点补足 P7-R1 执行后的证据。本文生成和复核期间没有访问相机、Ray120c、ESPHome、
`.env` 或 `all_off`；文中引用的实机结果来自已经完成并保留的 run artifact。

本补充遵守此前 GUIDE 的边界：不把有效采集失败改写为设备故障，不把
`uncertainty_unresolved` 改写为物理不可达，不修改冻结阈值、协方差、58-feature 空间或
P6 流形，也不解锁 sentinel、remaining 9、boundary、holdout 或 P8。

## 1. 按 GUIDE 的完成映射

| 阶段 | 已完成的工作 | 方法与质量 | 当前可用性 |
| --- | --- | --- | --- |
| P0-R remote camera | `RemoteCameraBackend`、health/config/capture、remote provenance、原子 CR3 落盘、`camera_busy` 有界重试、backend 注入和本地兼容路径 | token/URL 由脚本读取 `.env`；fake backend、失败下载、hash、原子替换和双 cleanup 有回归覆盖；远程采集链已有实机使用证据 | 作为后续实验的固定采集后端 |
| P1 RAW observer | identity RAW、`R/G1/G2/B` 四平面、每源 `1.0x..1.25x` 曝光包络、跨日 holdout、线性和边界诊断 | identity 在可靠包络内保留；correction candidate 的最坏 strip 误差约 `3.182 sigma_repeat`，被拒绝；修正模型没有进入正式链路 | 条件通过；仅限固定相机、机位、location 和曝光包络 |
| P2 五通道基底 | 5 通道、多个 code 档位的 chart-response basis，形成初始方向和归一化列 | 58/58 captures、CR3、recorded exposure、source isolation、无 `.npy`/failure、双 cleanup 通过；档位依赖和约 `125` 的条件数说明它只能作 seed | `forward_model_seed_only`，不是全局真值 |
| P3 加法性验证 | 多通道混合、重复命令和 forward-model 对照 | 55/55 captures，24 个 unique commands 各重复 2 次；`M-E / forward_model_seed_only` 被接受为诊断分支；约 20% seed RMSE 和广泛 shape error 证明不能依赖全局加法闭式模型 | 只能提供闭环初值；相机反馈必须保留 |
| P4 CCT multipatch | 12 个 Ray 白点目标的灯带 pilot | 192/192 CR3、曝光和命令审计完整；7 点可数值评估，5 点为 `measurement_unreachable`，没有把不可观测写成物理 gamut；Gate 3 停在诊断，不扩大到 70 点 | white-only 70 点候选仅外置保留，不覆盖默认 LUT |
| P6 Ray-only HSI | 106 点 Ray HSI/RGB 实拍、周期 Hue 和 SAT 流形分析 | 106/106 CR3、readback、source isolation、无 `.npy`、双 cleanup；Gate-5 冻结为 `full_periodic_2d_HB`；SAT0 Hue 不参与 Hue gate，HSI/RGB endpoint 分开 | 作为 P7 的冻结目标流形；不要求重拍 |
| P7 离线实现 | manifold、objective、feedback、runner、analyzer、v2 evidence contract、formalizer/finalizer 和 shell/Python cleanup | bounded solver、multi-seed、confirmation/rebase、joint coverage、physical/logical budget、replay 和 fail-closed rejection 均有测试；R0F-R0K 逐步收紧证据所有权 | 离线完成；可作为实机 runner，但不等于 P7 成功 |
| P7-D0 | firmware OTA 后 generation-bearing `rgbww_commanded_state` 和五步低输出 readback preflight | OTA 返回成功；generation `2 -> 3`；低输出最高 raw PWM `48`；重复命令 generation 递增；五通道、Ray intensity 和 Python/shell 双关灯均为零；wrapper 退出证据已原子保存 | D0-PASS；只证明设备状态读回链路，不证明颜色匹配 |
| P7-R1 | 定向 Ray reference/strip repeatability 实拍 | 采集完整性通过，但冻结统计 stability gate 失败；candidate 保持 `formal_capture_eligible=false` | 有效失败证据；等待 Advisor 冻结热状态和下一轮诊断协议 |

## 2. P7-R1 实验方法

### 2.1 冻结输入与目标

R1 使用 exact named experiment `p7_targeted_reference_repeatability_v2`，采用：

- remote camera backend 和最新 location `config/location/locations-20260714-211759.json`；
- P6 冻结的 `58` 个 native-Bayer feature、`full_periodic_2d_HB` 相关输入和四 CFA plane；
- Ray states：`H0/S0`、`H120/S100`、`H300/S100`，Ray intensity 100；
- strip commands：H0 full、H120/S100、H120/S50、H300/S100、H0 relaxed `3072`；
- 每个 Ray state A/B 各 5 次；strip 目标按冻结 plan 的正式和 confirmation 预算执行；
- logical budget `82`，physical cap `250`，允许范围 `82..170` no-weak、`82..250` permitted；
- 每次 source cycle 固定为 `off 1 s -> on 60 s -> capture -> off`；
- MC `20,000`、bootstrap `400`、seed `27072026`；协方差使用 CFA-plane block-isotropic diagonal/MAD/RMS 正则化；
- `SAT=0` 时 Hue 未定义，不执行 Hue gate。

### 2.2 实际采集顺序

本轮 formal 顺序为：

```text
start ambient -> Ray A -> strip A -> strip B -> Ray B -> end ambient
```

Ray A 与 Ray B 之间约相隔 50 分钟的 strip 高输出。该顺序不是事后拼接，所有
logical/physical、source、command、readback、capture owner、曝光和 cleanup ledger 均保留在同一 run。

### 2.3 证据与安全方法

采集层同时验证：

1. 每张 selected capture 的 CR3 非空、recorded exposure 和 patch statistics 存在；
2. Ray 与 strip 互斥，命令 readback 与冻结命令一致；
3. `commands.jsonl`、`capture-attempts.jsonl`、target rows 和 physical budget 可重算；
4. Python `finally` 和 shell `trap` 都执行双灯关闭；
5. child、Python cleanup、shell cleanup 和 wrapper exit 均留下独立证据；
6. run 完成后没有残留 runner/child 进程；
7. 不保存临时 `.npy`，不读取或打印 `.env`。

这使采集完整性、设备安全和数值 repeatability 成为三个独立判断，不会用 cleanup 成功掩盖
测量失败，也不会用数值失败否定 CR3 证据。

## 3. P7-R1 结果与质量分级

### 3.1 采集完整性：通过

Run：

```text
/Volumes/4T/temp/rgbww-optimizer/hsi-reference-repeatability/p7-r1-20260719-091000-terminal-retry1
```

结果：

```text
82 logical / 80 formal / 105 physical CR3
30 Ray / 50 strip / 2 ambient formal sources
8 auto-exposure caches / 31 physical exposure records
0 weak reacquire
82 retained selected CR3，全部非空
0 retained .npy
```

独立复核确认 `run.json` 为 complete；无 `failure.json`；source isolation、exact readback、
ownership、physical ledger 和曝光记录均可重算；Python/shell cleanup、child、shell-cleanup
和 wrapper exit 均为 0；run 结束后无残留进程。因此本轮不是 capture corruption、预算账本
错误或 cleanup failure。

### 3.2 统计稳定性：失败并阻塞

Analyzer 状态：

```text
analysis_status = calibrated_waiting_for_planner
analysis_branch = uncertainty_unresolved
ray_branch = R-REFERENCE-UNSTABLE
reference_epoch_shift = false
formal_capture_eligible = false
```

Ray 当前中心相对 P6 的 compatibility score 与当前 A/B repeatability score 必须分开解释：

| State | 当前中心 vs P6 | 当前 A/B repeatability |
| --- | ---: | ---: |
| H0/S0 | `51.97 > 9.51` | `139.46 > 9.50` |
| H120/S100 | `29.25 > 9.48` | `96.09 > 9.50` |
| H300/S100 | `17.81 > 9.63` | `14.35 > 9.63` |

三个 Ray state 都存在冻结 chronology trend failure。H120/S100 和 H300/S100 的 Ray B
首帧存在明显 single-frame dominance，方差占比分别约 `0.5633` 和 `0.7435`。五组 strip
command 均为 `uncertainty_unresolved`；3072 relaxed neutral 的 block-center 可以通过，
但 block-B trend 仍为 `7.71 > 4.0`，不能据此宣布稳定。

### 3.3 归因质量：工作假设，不是结论

当前最强假设是 source thermal/history non-stationarity 与可能的共同 camera/geometry drift
混在了本轮 chronology trend 中：

- 1 秒 off 不一定复位热状态，60 秒 on 不一定进入稳态；
- Ray B 在长时间关闭后的首帧离群与 cold-start history 一致；
- strip A/B 连续高输出后多个命令仍有 block 内趋势；
- Ray 多个 state 的 drift vector 方向相近，但 strip 的部分 command 有独立红/蓝方向变化；
- ISO 100、state/command 内固定 shutter、P6/R1 相同 `implicit auto` aperture provenance，
  使“本地默认曝光突然切换”不是首要解释；
- start/end ambient 只有两个 diagnostic frame，feature L2 差约 `7.5e-6`，不能单独证明环境
  没有影响。

因此，当前可以说“参考/光源运行状态未被当前协议证明稳定”，不能说“灯带物理不可达”、
“Ray 已发生确定 epoch shift”或“相机坏了”。不得删除首帧、修改 trend `4.0`、single-frame
dominance `0.5`、covariance、guard 或 58-feature 来挽救本轮。

## 4. 质量总评

### 4.1 工程和安全质量

等级：**通过**。

- remote capture、location/hash、command/readback、source isolation 和 owner ledger 有完整证据；
- Python/shell 双 cleanup 是实际 run 的 hard gate，不是只在 fake backend 中测试；
- retained CR3 完整、无 `.npy`、无残留进程；
- R0K 至 R0F 等离线收口持续把 evidence contract、budget ledger、rejection schema 和
  production round-trip 收紧为 fail-closed；
- Executor 报告 focused `65/65`、full `434/434`，并通过 compileall、wrapper/launcher
  syntax、`git diff --check` 和 CodeGraph；审计时又独立检查了关键 artifact、CR3 数量、cleanup
  JSON 和进程状态。

### 4.2 科学和统计质量

等级：**采集有效，稳定性不通过**。

本轮数据足以作为真实 non-stationarity evidence，不能作为可冻结的 P7 target model。Synthetic
joint coverage 全部通过只说明冻结 covariance 下的传播计算可运行，不能覆盖真实 A/B trend
failure。candidate 因此仍是 `calibrated_waiting_for_planner`，不得进入 sentinel 或产品配置。

### 4.3 产品结论质量

等级：**未形成**。

当前没有依据声明：

- HSI 13 点已完成或 13 点可用；
- 任一新的 strip HSI candidate 已 formal eligible；
- `s_exact_max(h)` 是无条件物理色域；
- 满幅策略边界等同于物理 gamut；
- P8 INT 维度可以开始；
- 任何新结果可以覆盖默认 LUT。

## 5. 证据索引

### P7-R1 主要 artifact

```text
plan.json = 55c25a4b51d4a247e1888f3d6a075dea313f3dadc3e5e8435e53c419131a1c2e
run.json = e14720376504dda8f1536aeb107a8d667253ab7094378edb7bd2ebbc65c924d7
captures.jsonl = ce8e74ab87e1570107f1c7708bcdaa9be360c254a6ff4047124370a9bdd979e4
capture-attempts.jsonl = 8da9b65385d464b0430e1ba028e43117c8797da8556f7ef7f789a7cb891e6977
commands.jsonl = 2d0667d235bffff9119eea54e76d76ed1914f246fec64903f2dd1a9b675b4ca3
analysis.json = ac5630e26180dc9f288eacb1ff0f8352e9acc6f9f0ea4a2e857ff3552eaf243f
strip-hsi-policy-v2-candidate.json = 755bbe775cf7cfe4ef6d01751aca2ea2e7b3a2d61fbc05f19bca087f47609a01
wrapper-result.json = 79d9d15bf5a88ba3e2a1f5e9cc0f6f40283eee33a7b70ceae38a62af946ef198
```

### 既有阶段

前置阶段的详细 run path、hash 和 Gate 结论仍分别以本目录 `01`、`02`、`03`、`04`、`05` 为准；
本文件只补充它们与 GUIDE 的完成关系，不复制全部历史 artifact。

## 6. 交给 Advisor 的决策问题

当前需要 Advisor 冻结的是实验定义和下一轮诊断，不是让 Executor 自行改模型：

1. 正式目标是 cold-start 后固定 60 秒的 transient、连续点亮后的 steady-state，还是两种 envelope 都要覆盖；
2. 下一轮是否采用 long-off cold-start repeats、60/120/300/600 秒 settling curve、command-switch
   对照或 ABBA anchor 交错设计，以及各自的时间/次数 bounds；
3. 是否允许引入可观测 thermal/time covariate；若允许，需明确它是条件 repeatability 还是额外
   worst-case uncertainty，并规定如何避免把真实颜色漂移吸收到噪声中；
4. 当前 P6 compatibility failure 应解释为协议/热状态问题、新自然日 epoch 重新锚定，还是
   analyzer 需要拆分 cold-start 与 steady-state。

在 Advisor 新 GUIDE 到达前，唯一允许的工作是保留证据、做离线 chronology/analyzer 诊断和
文档整理；不得重跑 R1、进入 sentinel-v2、扩大高输出或修改冻结门槛。
