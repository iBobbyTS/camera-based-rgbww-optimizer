# 已完成工作：P0-R 至 P4

## 1. P0-R：Remote 相机迁移

已完成：

- `RemoteCameraBackend`、health/config CLI、同步 `/v1/capture` 接入；
- CR3 原子落盘、bounded `camera_busy` retry、失败 provenance；
- 正式 runner backend 注入，local backend 只作兼容；
- dry-run 不读取 `.env`、不访问网络、不调用灯具；
- 密钥脱敏和 fake backend 测试；
- Python/shell 双关灯。

该阶段已经过真实 remote 相机实验复用，不只是接口占位。后续无需重新讨论是否回退到本地 gphoto2。

## 2. P1：RAW 观察者和曝光包络

### 2.1 诊断过程

P1 先后完成：

- 五张 remote preflight；
- 31 张正式重复性/线性 run；
- 同快门连续点亮 D3；
- 跨自然日完整 holdout；
- `1.0x..1.25x` 15 张 boundary-only 验证；
- identity 与冻结 response correction 候选对比；
- G1/G2 独立性分析。

### 2.2 Gate-1 决定

冻结结论：

- `conditional_pass`；
- RAW response=`identity`；
- 每源曝光包络=`1.0x..1.25x`；
- response correction 不安装；
- G1/G2 选择 G-C，后续固定四平面。

关键数值：

- identity 在 `1.25x` 的 Ray/strip shape sigma P95 为 `0.279/1.796`；
- 最大为 `0.388/2.903`，可靠 feature 均在 `3 sigma_repeat` 内；
- correction 将 strip 最差 feature 提高到 `3.182 sigma_repeat`，因此拒绝；
- near-noise `0.05` 位于 boundary 可靠观测最大 `0.0351` 和失败簇最小 `0.9979` 之间。

Gate-1 出口为 `approve_stage_2`。Advisor 不应通过新 HSI 工作静默改变该包络或安装 response correction。

## 3. P2：五通道经验基底

### 3.1 实验完整性

- 58/58 captures；
- 全部 CR3 非空且 recorded exposure；
- Ray 始终关闭，strip/ambient 隔离；
- 无 `.npy`、无 failure；
- Python/shell 双 cleanup 成功。

### 3.2 B-B 决定

- `CW/WW/R/G/B` 均呈档位依赖；
- 使用 `1024/2048/4095` 三档的分段线性 normalized column；
- condition 约 125，不属于无法辨识的 rank deficient；
- 低信号缺失 cell 只允许按计划低权重借用，不能伪装成直接测量；
- P2 基底在 P3 前只作带正则的物理预测。

该基底目前仍有价值，但价值是生成初始命令和局部方向，不是开环复制 Ray。

## 4. P3：随机混合和加法性

### 4.1 实验完整性

- run：`/Volumes/4T/temp/rgbww-optimizer/chart-basis-mixtures/p3-additivity-20260716-0245-retry1`
- 55/55 captures；
- 24 个唯一命令、每命令两个正式重复；
- 冻结 P2 basis、remote/location、identity RAW 和四平面；
- Python/shell 双 cleanup 成功。

### 4.2 Gate-2 决定

- 分支：`M-E / forward_model_seed_only`；
- 加法模型的 shape 误差广泛存在，不由单一负载、采集顺序或锚点漂移解释；
- 不批准全局 load correction；
- 不扩展大量交互项来拟合现有 24 点；
- 后续必须依赖同轮相机闭环。

这也是 P7 dry-run 初值预测误差仍约两成的原因。它不是 P7 的失败，但意味着完整 13 点闭环可能很长。

## 5. P4：CCT multipatch pilot

### 5.1 最终 run

- 路径：`/Volumes/4T/temp/rgbww-optimizer/cct-multipatch-pilot/p4-c-f-remote-20260717-000819-retry9`
- 12/12 target row；
- 7 complete、5 `measurement_unreachable`；
- 192/192 CR3/report 非空且 recorded exposure；
- 无 `.npy`、无 failure；
- Python/shell 双 cleanup 成功；
- command audit 无光源隔离违规。

### 5.2 Gate-3 决定

7 个可评估点的 training/holdout mean、P90、maximum 改善均超过同轮 `3 sigma`，白点也未退化。但以下 5 点在冻结测量包络内不可观测：

- `1800K/gm100`
- `1800K/gm200`
- `5600K/gm100`
- `5600K/gm200`
- `20000K/gm200`

不可观测点包含内部 `5600K/gm100`，因此不能按“只在极端失败”处理。

最终决定：

- `keep_white_lut_diagnostic_only; stop_before_p5`；
- 不扩到新的 CCT multipatch 70 点网络；
- 不放宽 observer threshold，不删除被拒 feature；
- 保留既有 white-only 70 点候选；
- P4 multipatch 数据只作为诊断和 HSI 设计经验。

## 6. P1-P4 对 P7 的约束

1. 使用 identity RAW、四平面和 `1.0x..1.25x` 包络；
2. P2 只能给 seed，不能决定最终 HSI 命令；
3. 所有 `faithful` 必须由真实闭环和 settled repeat 证明；
4. 弱信号不能通过扩曝光、删 feature 或改阈值绕过；
5. 失败测量只能说明当前观察者不可观测，不能自动说明物理 gamut 不可达；
6. P4 已证明长任务中 setup、probe、feedback、confirmation 各阶段都可能出现不同失败，P7 必须保留阶段化证据。

