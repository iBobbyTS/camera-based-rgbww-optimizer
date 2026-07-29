# FORMAL-R5 observer-quality hard failure：Advisor 决策请求

## 1. 当前硬停止

```text
run = P7-TD-B-RAY-PUBLIC-DEFAULT-FORMAL-R5
classification = accepted_hard_failed_formal_attempt
executed checkpoint = 1e3b107b8fbfe97bae5624ef638c4883a0faee1d
launch = 1/1
retry = 0
Ray accepted formal = 11/16
returned CR3 = 12
physical total = 14 (setup 2 + returned 12)
strip / paired / public analyzer = 0
formal pass = false
```

当前 GUIDE 要求 observer/measurement-quality failure hard-stop，并禁止自动 reshoot、删 feature、放宽 threshold 或以 analyzer
补偿。现有 GUIDE 没有定义下述 clipping 分支，因此 Planner/Orchestrator 都不能推导下一步。

## 2. 必须按原始 evidence 使用的失败事实

失败 capture：

```text
capture_id = 011-ray-c-t60
state = Ray H300/S100/INT100
requested elapsed = 60 s
rejection stage = post_return_processing
exception = HsiRejectedFeaturesError
message = 2 required HSI observer features were rejected
recorded Canon exposure = 0.00048828125 s
nominal shutter = 1/2000
recorded_to_nominal_ratio = 0.9765625
```

两个 required features：

| feature | status | exact failure | observed | frozen threshold |
| --- | --- | --- | ---: | ---: |
| `block_06/white:G1` | rejected | `clipped_fraction_exceeded` | `0.0007981642222887359` | max `0.0` |
| `block_06/white:G2` | rejected | `clipped_fraction_exceeded` | `0.000598503740648379` | max `0.0` |

这与早期 F0B-R1 的 6 个**低信号** plane-feature failure 是两个不同事件。请不要沿用 active PLAN 标题里的
`low-signal` 简称来分类 R5；R5 的 immutable evidence 是 white-patch green-plane clipping。

## 3. 请求 Advisor 冻结的决定

### 3.1 失败与 retained 11 帧的科学分类

请明确：

1. `011-ray-c-t60` 应归类为 exposure-policy invalid、state-specific observer saturation、capture quality invalid，还是其他
   指定类别；
2. 前 11 个 accepted formal frame 是否可以用于任何有限用途；若可以，只允许哪种用途，例如 exposure/chronology diagnostic、
   retained descriptive evidence 或下一轮设计依据；
3. 是否必须把全部 11 帧隔离，不得进入任何 TD-B scientific inference；
4. 无论选择哪一项，是否确认本次 run 永远不能被补写成 formal pass。

### 3.2 是否允许新的 repeat

请明确选择 `no_repeat`、`targeted_repeat` 或 `full_new_formal_run`。若允许 repeat，新 GUIDE 至少必须冻结：

- 新 experiment/run ID 与全新 root；
- 是只重拍 state C、重拍 Ray 全部 16 帧，还是采用其他完整性策略；
- 是否及如何引用旧 11 帧，禁止事后拼接时应明确写出；
- exact capture IDs、source/state 顺序、600 秒 anchors 与 60/120/300/600 slots；
- physical cap、setup capture 计数、formal budget 和 retry count；
- aperture、ISO、每 state shutter/exposure policy，以及 exposure setup 是否必须重做；
- quality gate、58-feature set、clipping/noise-floor thresholds；
- source isolation、abort、Python/shell cleanup、final-zero 和 terminal-seal contract；
- Ray 失败后 strip 是否仍必须保持永久未进入。

### 3.3 是否改变 observer、threshold、exposure 或 statistic

请分别回答：

1. frozen maximum clipped fraction `0.0` 是否保持；
2. `block_06/white:G1/G2` 是否继续是 required features；
3. 是否仅改变 exposure policy，而不改变 feature/threshold；
4. 是否要改变 observer/feature/threshold/covariance/no-ambient statistic 中任一项；
5. 若任一科学合同改变，是否要求新的 GUIDE、代码 checkpoint、lineage release、public validator 和 fresh predevice/E2 gate。

当前执行方没有删除 feature、放宽 threshold、改 exposure、扩大 covariance 或切换 statistic。请勿把未执行的候选修复写成
已验证结论。

### 3.4 strip、TD-B 和后续路线

请明确：

- 本次 attempt 的 strip 是否永久保持 blocked；
- `REF-P7-04` 应进入 repeat、hold、restricted diagnostic 还是 stop route；
- `REF-P7-05` 的 TD-B scientific acceptance 是否继续 blocked；
- 在 Ray 路线未解决前，TD-C、reference epoch classification、sentinel、remaining 9、boundary、holdout 和 P8 是否全部继续锁定。

### 3.5 600 秒 Human override 的关系

Human 的既有决定继续是：

```text
developer_selected_operational_dwell_s = 600
selected_time_limit_not_proven_steady = true
```

请确认任何 repeat/exposure 策略都不会把这个产品时间上限静默重分类为 `t_formal=600`、`settled_at_600` 或 TD-A pass。
若 R5 clipping 使 600 秒 operational protocol 本身需要产品层面调整，请明确指出；否则只修改 observer/exposure 分支。

## 4. 建议的 Advisor 回答字段

为避免 Planner 再次推断，建议新 GUIDE 至少给出：

```text
r5_failure_class = ...
retained_11_use = none|diagnostic_only|specified_other
r5_formal_pass = false
repeat_policy = no_repeat|targeted_repeat|full_new_formal_run
old_new_frame_combination = prohibited|exact_rule
observer_feature_policy = unchanged|exact_change
clipping_threshold_policy = unchanged|exact_change
exposure_policy = exact_state_specific_contract
new_checkpoint_required = true|false
new_lineage_release_required = true|false
strip_route = blocked|new_exact_branch
ref_p7_04_exit = ...
ref_p7_05_status = ...
td_c_and_later = locked|exact_unlock_condition
operational_600_semantics = selected_not_proven_steady
```

## 5. Retained evidence

| Artifact | SHA-256 |
| --- | --- |
| `ray-formal/failure.json` | `2984ec745f2b7cddad1549535b730ae75397cdf7f1fa8602f71010f6613a9a65` |
| `ray-formal/measurements/011-ray-c-t60.patch-statistics.json` | `98b792f0ef2d89718102c054fa4c4ad43206cf3cce82855d9c67900b6223a8be` |
| `ray-formal/run.json` | `dfba25366d6deb093170ceb21ee2fa259143f0da4ba0628216de0d6f23f03079` |
| `ray-formal/physical-returns.jsonl` | `d6569f121c7a31ac1dfb427fe2de1dccc8b46fe3be6e4f3d7ba007d8019e6e02` |
| `terminal-audit.json` | `4bee490fa83bad33830cf5e8941ccc7fa0ca83191903639c617af5fe9d5e7d79` |
| `returned-summary.json` | `5e97023d84d91f0037b096bf84e1102a8b786aa174a383b65087669fb5401955` |
| `ray-formal/all-off-python.json` | `982cee95d59cc18ae1270fdc02f3c8947008796593fa22deb07f925ebd5327dc` |
| `ray-formal/all-off-shell.json` | `3c4ea47739e009cef740791e86195f8e76ec8ddb805b3a937efee75c01cf3381` |

所有 12 个 returned CR3 与 sidecar 的 path、bytes、SHA-256、remote capture/request IDs 和 validation status 均保留并通过。
本请求整理期间没有重拍、运行 public analyzer、访问设备或修改 retained run。
