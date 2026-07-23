# P7-TD-A 验收归档：采集有效但 600 秒内未证明稳定

**Planner 复验时间：** `2026-07-21T20:37:38-0600`

**被验收 active PLAN SHA-256：**
`971a8d1aacfac5ba6f845f4427ae4514f56ed3ebd83c8740314bdf9c0e03f75b`

**执行记录提交：** `a0cae5c14262ad07a372869a1c4d2f5cceb15055`

**Planner 决定：**

```text
acquisition_and_evidence = accepted
td_a_scientific_result = settling_not_demonstrated_by_600
guide_branch = TD-A-B
t_settle_ray_s = null
t_settle_strip_s = null
t_formal_provisional_s = null
next = stop_and_request_900_1200_extension_from_advisor
```

## 1. 已执行范围

Executor 按 active PLAN 完成唯一授权的 `p7_td_a_cold_settling_v1`：

- source 顺序为 Ray 后 strip，两个 run 不并发；
- 每个 source 使用固定 `H120/S100/INT100 equivalent`；
- 每个 source 三个独立 cold cycle；
- 每个 cycle 连续点亮并在 nominal `60/120/300/600 s` 拍摄；
- 每个 source 保存 start/mid/end 三张 ambient diagnostic；
- timing 使用 `best_effort_gphoto2_observed_elapsed_v2`，不宣称绝对 exposure start；
- Python finally、shell trap 和最终独立零读回全部执行；
- 未进入 TD-B、TD-C、sentinel、remaining 9、boundary、holdout、Gate-6 或 P8。

## 2. 正式证据

### 2.1 Run 路径

| source | run | analysis SHA-256 |
| --- | --- | --- |
| Ray | `/Volumes/4T/temp/rgbww-optimizer/p7-thermal-diagnostics/p7-td-a-ray-debug` | `13fac6336e95e6900003ff5ced50051b1b9ce2102af9d95729117eab3f46f69d` |
| strip | `/Volumes/4T/temp/rgbww-optimizer/p7-thermal-diagnostics/p7-td-a-strip-20260722-001426` | `3d265f9e57e92552f7dfb2b28c455373eb655911dec2e4e4bb8c59c013302155` |
| paired | `/Volumes/4T/temp/rgbww-optimizer/p7-thermal-diagnostics/p7-td-a-paired-20260722-022200` | `99550214c619160b39cbf7f393e6b8dc3a5b3feae8f91d0a1765c272283c3160` |

### 2.2 Paired artifact hashes

| artifact | SHA-256 |
| --- | --- |
| `td-a-combined-analysis.json` | `99550214c619160b39cbf7f393e6b8dc3a5b3feae8f91d0a1765c272283c3160` |
| `EXPERIMENT_SUMMARY.md` | `21470015f92eb3981753ad398abfdb9f73444e93bc303272cdde9ed717453ee3` |
| `input-manifest.json` | `a938e6f1bc84fee96635a11fcacc8cd2707a322c6b8f18ceedfb2dc8e97f710c` |
| `independent-final-zero.json` | `b83d96e000293f7413372b297b97a49fc676f437e099f8ad6d52f2b401824dc2` |

## 3. Planner 独立复验

### 3.1 数据和账本

| 检查 | Ray | strip | 结论 |
| --- | ---: | ---: | --- |
| formal captures | 12 | 12 | 与冻结 plan 一致 |
| ambient captures | 3 | 3 | 与冻结 plan 一致 |
| physical CR3 | 15 | 15 | 合计 30，低于 paired cap 44 |
| unique capture IDs | 15 | 15 | 通过 |
| unique CR3 paths | 15 | 15 | 通过 |
| non-empty CR3 | 15 | 15 | 通过 |
| recorded exposure | 15/15 | 15/15 | 通过 |
| retained NPY | 0 | 0 | 通过 |
| `failure.json` | 无 | 无 | 通过 |

两个 source 的 15 张 capture 均为 Tier B，正式 timing method 均为
`gphoto_capture_return_minus_recorded_exposure`。nominal slot 与 observed exposure-start estimate
保持分离；没有重新引入 proximity gate。

### 3.2 输入、隔离和退出

- paired manifest 中 Ray/strip `plan.json` 和 `run.json` 哈希与保留文件一致；
- location、observer、manifold、uncertainty、policy、operating envelope 和 R1 command ledger 均由
  `input-manifest.json` 冻结；
- 两个 run 的 command audit、timing、capture、source isolation、covariate、cleanup 和 wrapper
  contract 全部为 `pass`；
- 两个 wrapper 的 child、shell cleanup 和 wrapper exit code 全部为 `0`；
- Python cleanup 与 shell cleanup 都记录 ESPHome 全零和 Ray intensity `0`；
- 最终独立零读回记录 strip generation `7 -> 8`、五通道全零、Ray intensity `0`；
- Planner 复验时没有相关 runner/wrapper 进程；
- `config/hsi/p7-operating-envelope-v1.json` 未被本实验修改。

### 3.3 科学结果

冻结 trend limit 为 `4.0`，single-frame dominance limit 为 `0.5`：

| source | cycle 1 | cycle 2 | cycle 3 | max dominance | 结果 |
| --- | ---: | ---: | ---: | ---: | --- |
| Ray | 17.7369 | 16.8013 | 16.7317 | 0.2003 | 三轮 trend fail |
| strip | 16.8865 | 10.3106 | 11.8856 | 0.2059 | 三轮 trend fail |

dominance 没有失败，但两个 source 在全部三轮中均存在超过冻结门限的 chronology trend。因此这不是
单帧异常，也不能删除某张图后放行。600 秒只保留为 validation point，不能成为自动候选。

## 4. 质量判断

- **采集与证据质量：高。** 数量、CR3、曝光、输入哈希、source isolation、readback、物理账本、
  wrapper ownership 和三层关灯证据完整。
- **timing 绝对准确度：有限。** 全部为 Tier B gphoto2 best-effort estimate；它可用于本协议的
  observed chronology，但不是绝对 exposure-start 真值。
- **科学结论：有效的负结果。** 当前只证明 Ray 与 strip 在本协议下到 600 秒仍未达到冻结稳定门；
  不证明设备故障、相机故障、reference epoch shift、物理不可达或 gamut boundary。
- **代码验证：沿用已验收 checkpoint。** 本轮提交只增加执行结果文档，没有功能代码变更；Planner
  因此没有重复运行完整 Python suite。

## 5. Planner 分支决定

Advisor 第三轮 GUIDE 第 4.3/4.4 节明确规定：一个 source 未在 600 秒内稳定时进入
`stop_thermal_extension_required`，请求 900/1200 秒扩展，不进入 TD-B。当前两个 source 都满足该
停止条件，因此 Planner 接受采集但拒绝推进：

- 不重跑原 `60/120/300/600 s` TD-A；
- 不自行把 600 秒写为 `t_formal_provisional`；
- 不自行设计或授权 900/1200 秒实验；
- 不调整 trend、dominance、coverage、covariance、58-feature 或 operating-envelope 语义；
- 先提交新的 Advisor 审计包，由 Advisor 冻结扩展采样点、cycle 数、重叠 anchor、预算和停止分支。

## 6. 残余风险与唯一下一分支

残余风险：当前数据不能判断稳定时间只是略高于 600 秒，还是会持续超过 1200 秒；也不能决定新扩展
应复用现有 run、重新建立完整 cold cycle，或只测 source-specific 扩展。上述选择会直接影响可比性和
正式 dwell 语义，属于 Advisor 决策，不应由 Executor 猜测。

唯一下一分支：`waiting_for_advisor_900_1200_extension_decision`。在新 GUIDE 到达并经 Planner 转换为
新的单一 active PLAN 前，Executor 没有设备、网络、代码或分析任务。
