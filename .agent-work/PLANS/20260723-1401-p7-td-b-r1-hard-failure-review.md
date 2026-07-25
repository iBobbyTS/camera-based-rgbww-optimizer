# P7-TD-B-F0B-R1：首张 Ray formal 低信号 hard failure 验收

**审查日期：** `2026-07-23`

**审查范围：** active `.agent-work/PLAN.md`（审查前 SHA-256
`98e29b863610492d6905889dafe573223893859899e7d668954ce31605a2cfdd`）、
`.agent-work/EXECUTION_RESULT.md`（SHA-256 `f5dd6ebab3c0e44cdc2e525ec8c687a336007f990b1fca37261ed6a12e8a1c1d`）和
Ray R1 首张 hard-failure run。

## 1. 实机结果与证据

Run：

```text
/Volumes/4T/temp/rgbww-optimizer/p7-td-b-formal-ray-r1-20260723-182500
```

本次只完成 `A = H120/S100/INT100 @ 600s` 的一次 capture。结果：

```text
status = failed
completed formal = 0
accepted formal = 0/16
ambient = 0
setup physical = 2
physical returned = 1
physical total = 3
CR3 = 1, non-empty
sidecar = 1, non-empty
NPY = 0
strip = not started
```

失败类型为 `HsiRejectedFeaturesError`，六个 plane-feature 仅因
`near_noise_floor_fraction_exceeded` 被拒绝；未放宽质量阈值、未重拍、未进入 analyzer。
记录的 Canon exposure 为 `0.000193774542476587s`，请求 `1/5000`，比例
`0.9688727123829349`；timing 为可接受 Tier B。该失败不是 exposure ratio、timing 或 cleanup failure。

关键 evidence：

| Artifact | SHA-256 |
| --- | --- |
| `run.json` | `dc24373391d7b39729750c8dfaa2c0b4db7dbbfac36fa962d433335397b0348e` |
| `failure.json` | `eea02c17ffc87b7fa99c339040de0ca9a35d7e8ba35e7a5e7b37c417b62f65ec` |
| `physical-returns.jsonl` | `6e10bf6a67bc469b9980e13dc03fc3bd0c9b2473f83e48ba9f8c6ca682287484` |
| CR3 | `0778e98d46d05e6bf13e218b79ee644178629076e4d9e6d8a1545fcb54a03889` |
| CR3 sidecar | `93d0e64f612ab591da717d99af25dc5606a98148729e1988cc43f667375b4e68` |
| patch statistics | `64a84ea2b6169c11eb457adc54b8a0839895afc5b2ac9a0729d17e62888ed5bd` |
| Python cleanup | `bd6a481ebec00a360ba8c797ee7b2ea58620ee3a0c4f523fe2de6488dfa8ccd3` |
| shell cleanup | `5298f1882f43052c049cc1f6428ce00dafb1ff5eb3d84a532955adcd6ce1ea72` |
| independent final zero | `a39c742c83e3137a6cb0d1d801e8c0371b5e986cb948643a018b9cea1c858f3f` |

`failure.json` 的 `rejected_capture` 正确记录了 CR3 path/hash/bytes、capture ID、physical count 和
`post_return_processing`，但 `sidecar_path` 与 `sidecar_sha256` 为 `null`。实际 sidecar 为 CR3 同目录
`.metadata.json`，非空且 hash 与 retained file 一致；因此这是 failure evidence association gap，不是 sidecar
丢失。

## 2. 根因定位

当前 owner 在 `measure_p7_thermal_diagnostics.py` 中的顺序为：

- `record_physical_return()` 先建立 CR3 physical ledger，并把 sidecar 字段初始化为 `null`（约 796-805 行）；
- `capture_fn` 在 `raw_capture()` 内完成 sidecar/RAW report 后进行 HSI feature extraction；本次 feature extraction
  先抛出异常，因此没有返回到 `retain_capture()`；
- `retain_capture()` 才会补写 sidecar path/hash（约 905-920 行）；
- `execute_plan()` 的 failure handler 直接写当前 `rejected_capture`（约 1048-1054 行）。

所以失败路径保留了真实 CR3 和 physical ledger，却无法把已存在 sidecar 的 owner/hash 传播到 failure payload。
CodeGraph 也显示 `execute_plan` 缺少直接覆盖的回归测试。

## 3. Planner 决定

```text
R1 hard failure = accepted as valid PLAN stop
accepted formal = 0; no scientific claim
physical total = 3 is authoritative
CR3/sidecar/run remain immutable evidence
Python cleanup = pass
shell cleanup = pass
independent final zero = pass
public analyzer = correctly not run
automatic retry / strip / TD-C / later stages = locked
failure sidecar path/hash gap = must be fixed offline before any retry
```

不得通过编辑旧 `failure.json` 来“修复”证据；旧 run 只允许只读 replay，修复必须产生新的 offline artifact 和新的
代码回归测试。

## 4. 残余风险

- 低信号被发现于第一张正式 Ray capture，不能推断其余 15 张的可测性或科学状态。
- 当前 failure payload 不能独立重放 CR3 sidecar 关联；在修复前，public hard-invalid analyzer 不应被放行。
- 未修改 raw-observer 阈值、曝光策略、timing 合同、58-feature 集合或 covariance；不能把该失败解释为应放宽门槛。

## 5. 精确下一分支

`offline_retain_sidecar_on_post_return_rejection`

Executor 只做离线代码/测试/证据包：让 physical-return 后任何 feature/report/timing/covariate rejection 在
`failure.json.rejected_capture` 中保留实际同 run sidecar path、byte count 和 SHA-256；补真实执行顺序的 fake
post-return feature rejection round-trip、缺失/越界/篡改 sidecar 负例，并对本次旧 CR3/sidecar 生成只读 replay
审计 artifact。完成后交回 Planner。

禁止新 setup、任何 Ray/strip capture、自动重拍、public scientific analyzer、阈值/曝光/时序修改和后续阶段。

