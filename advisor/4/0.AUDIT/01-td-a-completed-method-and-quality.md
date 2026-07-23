# P7-TD-A 已完成方法、结果与证据质量

## 1. 上轮指导与冻结输入

本轮执行依据：

| 文件 | SHA-256 |
| --- | --- |
| `advisor/3/1.RESEARCH.md` | `1fac3ed986b393aa3467722e3ee06ab240e6df1b64c4146741072bcae2f91a9c` |
| `advisor/3/1.GUIDE.md` | `92f766da523c40ff49c228c996dffd6d3839552f70bbd79aa7627485dd749be1` |

GUIDE 冻结 `H120/S100/INT100 equivalent`、Ray/strip 各三个 independent cold cycle，以及 nominal
`60/120/300/600 s` 四个采样点。600 秒只作 validation；若 300 到 600 仍有系统性变化，必须停止并
请求 900/1200 秒扩展。

代码实现 checkpoint 为 `4901f819a8c43b6ffea89427f3960d9dc5e41159`。执行交接提交
`a0cae5c14262ad07a372869a1c4d2f5cceb15055` 只更新
`.agent-work/EXECUTION_RESULT.md`，没有改变采集或 analyzer 代码。

## 2. 实验方法

Ray 与 strip 使用两个独立且不并发的 run，顺序为 Ray 后 strip。每个 source：

1. start/mid/end 各拍一张 ambient diagnostic；
2. 执行三个 independent cold cycle；
3. 每个 cycle 在 cold proxy 后施加同一 command，连续点亮 600 秒；
4. 在 nominal 60、120、300、600 秒各拍一张；
5. 使用 remote v2 metadata 重建 Tier B gphoto2 best-effort observed elapsed；
6. 每个 transition 与 capture 检查另一 source 关闭及 commanded-state readback；
7. run finally、shell trap 和最终独立 recovery 均把两个 source 关闭。

实际 observed elapsed median：

| source | nominal 60 | nominal 120 | nominal 300 | nominal 600 |
| --- | ---: | ---: | ---: | ---: |
| Ray | 64.2412 s | 124.9344 s | 304.8107 s | 604.8344 s |
| strip | 64.3691 s | 124.7842 s | 304.6654 s | 604.7721 s |

这些值仅是 `gphoto_capture_return_minus_recorded_exposure` estimate，
`absolute_exposure_start=false`。按 Developer/Human 已冻结决定，nominal slot 只用于调度和分组，
不使用 proximity gate。

## 3. Retained evidence

### 3.1 路径与核心哈希

| 项目 | 路径或 SHA-256 |
| --- | --- |
| Ray run | `/Volumes/4T/temp/rgbww-optimizer/p7-thermal-diagnostics/p7-td-a-ray-debug` |
| Ray analysis | `13fac6336e95e6900003ff5ced50051b1b9ce2102af9d95729117eab3f46f69d` |
| strip run | `/Volumes/4T/temp/rgbww-optimizer/p7-thermal-diagnostics/p7-td-a-strip-20260722-001426` |
| strip analysis | `3d265f9e57e92552f7dfb2b28c455373eb655911dec2e4e4bb8c59c013302155` |
| paired dir | `/Volumes/4T/temp/rgbww-optimizer/p7-thermal-diagnostics/p7-td-a-paired-20260722-022200` |
| combined analysis | `99550214c619160b39cbf7f393e6b8dc3a5b3feae8f91d0a1765c272283c3160` |
| input manifest | `a938e6f1bc84fee96635a11fcacc8cd2707a322c6b8f18ceedfb2dc8e97f710c` |
| final independent zero | `b83d96e000293f7413372b297b97a49fc676f437e099f8ad6d52f2b401824dc2` |

### 3.2 数量与完整性

| 项目 | Ray | strip | 合计 |
| --- | ---: | ---: | ---: |
| formal | 12 | 12 | 24 |
| ambient | 3 | 3 | 6 |
| physical CR3 | 15 | 15 | 30 |
| physical cap | 22 | 22 | 44 |
| retained NPY | 0 | 0 | 0 |
| failure.json | 无 | 无 | 无 |

全部 30 个 capture ID 与 CR3 path 唯一，CR3 非空且 recorded exposure 有效。paired manifest 绑定两
个 source 的 plan/run hash 及 location、observer、manifold、uncertainty、policy、operating envelope
和 R1 command ledger。

## 4. 科学结果

冻结门：trend `<=4.0`，single-frame dominance `<=0.5`。

| source | cycle 1 trend | cycle 2 trend | cycle 3 trend | max dominance |
| --- | ---: | ---: | ---: | ---: |
| Ray | 17.7369 | 16.8013 | 16.7317 | 0.2003 |
| strip | 16.8865 | 10.3106 | 11.8856 | 0.2059 |

两个 source 的三轮 trend 全部失败；single-frame dominance 没有失败。single-source 与 paired
analyzer 一致输出：

```text
status = settling_not_demonstrated_by_600
t_settle_ray_s = null
t_settle_strip_s = null
t_formal_provisional_s = null
t_formal_s = null
```

## 5. 方法与证据质量

| 维度 | 质量判断 | 边界 |
| --- | --- | --- |
| command/source isolation | 高 | generation-bearing strip readback 与 Ray readback 均保留 |
| CR3 ownership/exposure | 高 | 30 个唯一非空 CR3，recorded exposure 30/30 |
| timing chronology | 可用于当前协议 | Tier B best-effort，不是绝对 exposure-start |
| wrapper/process evidence | 高 | child、shell cleanup、wrapper exit 均为 0，无残留进程 |
| final safe state | 高 | Python、shell、最终独立 readback 三层证据，双灯为 0 |
| settling inference | 有效负结果 | 只证明本协议到 600 秒未过门，不外推到更长时间 |

本结果不支持删帧、放宽 covariance/coverage/trend、将 600 秒自动命名为 steady，或把失败改写成
reference shift、设备故障、物理不可达或 gamut boundary。
