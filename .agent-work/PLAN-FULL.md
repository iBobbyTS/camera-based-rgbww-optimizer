# PLAN-FULL — GUIDE 4 从 retained Ray R6 开始的完整科学路线

**计划性质：** 可由 Git 追踪、供 Human 与 agent 阅读的 `non-executable roadmap`

**不得作为：** production/test 输入、设备授权、runtime 状态机、release/lineage、stage-gate 或 hidden gate

**科学权威：** `advisor/4/4.GUIDE.md`；其中纯工程实现条款按 Human 后续去工程化决定与根 `AGENTS.md` 覆盖

**当前分支：** `codex/guide4-science-path-v3`

**Ray analyzer 代码 checkpoint：** `a3f2b864860a3b524999bd003c2b01f26748086a`

**路线状态：** `M1_RAY_R6_HISTORY_FAIL_PRESCRIBED_STOP_WAITING_ADVISOR`

**唯一下一动作：** Advisor 审阅 Ray R6 history-dependent 结果并选择新的科学模型或实验方向；strip、combined 与 TD-C 不得进入

> 本文件只描述依赖关系、科学分支与复现边界。真正执行设备动作前，Orchestrator 仍需在当前执行说明中写清本次实验的目标、状态、强度、时长、预算、source isolation、abort 与 cleanup。不得由本文件推导设备授权。

---

## 0. 决策优先级与总约束

冲突时按以下顺序解释：

1. Human 的最新明确决定与根 `AGENTS.md`；
2. `advisor/4/4.GUIDE.md` 的科学、测量、安全、预算与阶段锁；
3. `advisor/4/RGBWW_GUIDE4_SCIENCE_FIRST_DEENGINEERING_PLAN.md` 和 `advisor/4/RGBWW_GUIDE4_PLAN_FULL.md` 中仍适用的去工程化目标；
4. 本 PLAN-FULL 仅作路线 context。

Human 已明确用最小复现合同替代 GUIDE 中纯工程性的 successor lineage、release、stage-gate、terminal seal、PLAN/FULL runtime binding、Git ancestry owner、predevice/E2/readiness 链。不得重新引入这些机制，也不得建立新的通用 science runtime。

GUIDE/RESEARCH/Advisor 文档保持不变。本路线只使用现有三类 owner：

- `p7_thermal_diagnostics.py`：科学 protocol、sequence、budget 与判定逻辑；
- `measure_p7_thermal_diagnostics.py`：唯一设备采集 CLI；
- `analyze_p7_thermal_diagnostics.py`：唯一离线分析 CLI。

PLAN/PLAN-FULL 可以追踪，但 production、tests、runner、analyzer 和授权逻辑不得读取它们。

---

## 1. 当前 checkpoint 与已完成部分

### 1.1 工程完成状态

- E1/E2 去工程化已完成：direct Ray/strip/TD-C 路径已取代 lineage/release/stage-gate runtime。
- 当前 live tree 已删除旧 governance production/tests；不再创建 E3 清理阶段。
- Ray R6 连续光源顺序已修正为 `A → D → A → B → A → C → A`；首次 Ray on 到最终 cleanup 之间不发送 Ray-off command，状态间只验证 strip zero。
- strip zero readback 已按真实 ESPHome payload 字段修正。
- 曝光门禁已在 `ce065a3` 改为“快门档位一致性”门禁，而不是 raw float 相等或真实积分时长判断。
- 代码、测试、计划与提交都是 engineering evidence，不计作 `science_delta`。

### 1.2 Retained Ray R6 acquisition

唯一 retained root：

```text
/Volumes/4T/temp/rgbww-optimizer/
guide4-ray-r6-20260808-20260808-153400-post-fix-valid/ray-r6
```

采集时 checkpoint：

```text
acquisition_commit = 3e80e5fd30e079782b27a3545513de5821dbc4d2
acquisition_dirty = false
guide_experiment_id = P7-TD-B-RAY-OP600-EXPOSURE-GUARDED-FORMAL-R6
internal_experiment_id = p7_td_b_command_switch_history_v1
formal accepted/completed = 16/16
physical returned/CR3 = 16/16
ambient/setup = 0/0
cleanup = pass
```

已核对存在并顺序一致：

- 16 `captures.jsonl` rows；
- 16 `physical-returns.jsonl` rows；
- 16 CR3、16 sidecar、16 patch-statistics；
- 16 thermal-covariates；
- 7 个连续 Ray state command，顺序为 `A,D,A,B,A,C,A`；
- 1 个开始时 both-off gate + 7 个状态边界 strip-zero-only gate；
- Python cleanup 与 shell cleanup 均成功，Ray/strip 最终为零；
- 修复后 post-capture quality gate 已离线重跑，`quality.json` 为 16/16 pass、每帧 58 features。

### 1.3 原失败必须保留

旧 validator 在完成 16 帧后，因 Canon 记录值与名义快门做严格浮点比较而抛错。因此以下文件不得覆盖、改写或伪装成原 child 成功：

| 原始或现有 artifact | SHA-256 | 当前事实 |
| --- | --- | --- |
| `experiment-spec.json` | `b8a8274b2c786c5c896acfeb39f45c1501eefbd526606e60ded64d7db0f0c616` | exact 16-frame spec |
| `input-checkpoint.json` | `df63b7d92b2d25fb534a33047548d8ffeee9094b019953774da77faca8076d7a` | acquisition commit clean；location/curve copied into root |
| `run.json` | `ef1367a2078c9c95f9900cda066ce5a030d59ec1ce5e48e1ffde22905812a062` | `status=failed`，但 16/16 与 cleanup=pass |
| `failure.json` | `c60964f5d6f5a67207876ec8bd369502db8939dc4916e1f63c71991392d3529a` | exact message: recorded exposure differs from frozen shutter |
| `wrapper-result.json` | `f6b2c8e2781a531b2fb0ca391dac3a1eb761386f7455b078c1d545a710d2c20f` | `status=child_failed`，child/wrapper exit=1，shell cleanup=0 |
| `all-off-python.json` | `60bb673d7f07fdfcbf22e804da03982a32a9b8b07496daaa85cafba67d21d517` | cleanup pass |
| `all-off-shell.json` | `d254329059b2e6553210c19418ef0977b56a833d2d0884adfd3ac464408da4d7` | cleanup pass |
| `quality.json` | `ed4050b4cba2b53133ec9cb4e51c139ba6128e3051ca3dd541183b4df6915b3f` | 修复后派生，16/16 pass |

已从同一 root 完成并保留：

```text
commands-audit.json        sha256=98a1df5311ce789b6eff0e20a9ada8521efda83efbf3d999d71c0d566c298178
post-fix-revalidation.json sha256=9d531419ed94bcc1a0c5af29933eb82131082dbe0eea0d9f05f9dcfdec473e2e
analysis.json              sha256=7cb6ef267496342ae1145bb83295510438ea9bf45946187168ffb21e8b0e267b
```

`commands-audit.json` 是从同一 root 的 immutable spec/commands/gates/captures/physical/cleanup 离线派生，并明确标注为 post-fix derived evidence。原 `run/failure/wrapper` 仍保持失败身份和原 hash。

### 1.4 当前科学状态

```text
science_delta = retained_new_ray_r6_acquisition_16_of_16
ray_measurement_quality = 16_of_16_pass_after_fixed_gate
ray_history_conclusion = history_dependent_at_operational_dwell_600
ray_formal_pass = false
strip_td_b = locked
combined_operational_600 = locked
td_c_core = locked
```

完整新 Ray R6 数据集已得到合法科学负结果：六组 A-anchor 比较中，`A0` 对 `A_after_C` 的 score=`11.3712740731`，超过 guarded limit=`9.5439242182`；其余五组兼容。D/B/C chronology trend 分别为 `6.2989992683 / 8.1503454161 / 12.2215869835`，均超过 `4.0`，而 dominance 分别为 `0.4009237037 / 0.4733067736 / 0.4548462651`，均低于 `0.5`。trend 只作 chronology report，不单独改变 operational gate；真正 blocking 的是 A return history incompatibility。按 GUIDE 8.3 必须停止且不得运行 strip。

---

## 2. 全路线概览

```text
M1 同一 Ray root 离线重新验收 + 一次 Ray analyzer
 ├─ engineering invalid -> 无科学结论；保留证据并停止，禁止自动重采
 ├─ valid quality fail  -> Ray 科学负结果；停止并回报 Advisor
 ├─ history fail        -> Ray 科学负结果；停止并回报 Advisor
 └─ quality + history pass
       ↓ 只解锁 M2
M2 全新 strip TD-B 16 帧 + strip analyzer
 ├─ engineering invalid -> 无科学结论；停止，禁止自动重试
 ├─ quality/history fail -> strip 科学负结果；停止并回报 Advisor
 └─ pass
       ↓ 只解锁 M3
M3 combined operational-600 纯分析 gate
 ├─ fail -> 科学停止；TD-C 锁定；回报 Advisor
 └─ pass
       ↓ 只解锁 M4
M4 TD-C core：4 sessions / 8 formal + 8 ambient
 └─ pass 或 fail 均停止设备推进并回报 Advisor

sentinel / remaining 9 / endpoint expansion / boundary / holdout /
Gate-6 / P8 / default LUT install 始终锁定
```

---

## 3. M1 — 同一 retained root 的离线重新验收与 Ray-only analyzer

### Prerequisites

- 当前 root、16+16 ledger 与本计划第 1.3 节列出的原 artifact hash 不变；
- acquisition commit 记录为 `3e80e5f...` 且 acquisition 时 `dirty=false`；
- validator fix 为 `ce065a3...`；
- 不访问 camera、Ray、strip、network，不创建第二个 formal root；
- 默认 analyzer 继续拒绝普通 failed run，只有显式 post-fix revalidation 路径可处理此 exact failure。

### 唯一动作

在现有 measurement/analyzer owner 内实现并运行一次窄范围、显式 opt-in 的 same-root revalidation，然后立即对同一 root 运行一次 Ray-only analyzer。该入口只服务这类“16/16 已物理完成、唯一 child failure 为已修复 exposure-setting comparison”的 retained run；不得抽象成通用 recovery runtime。

若需代码调整，只允许：

1. 在现有 analyzer 或 measurement module 增加显式 revalidation 参数/函数；
2. 默认路径仍拒绝 `run.status=failed` 与 `wrapper.status=child_failed`；
3. 只有 exact failure message/type、16/16 完成、双 cleanup pass 且全部复验通过时，显式 analyzer 才可消费 `post-fix-revalidation.json`；
4. focused tests 覆盖 exact allowed failure、默认拒绝、相邻快门档拒绝、capture/hash/cleanup 任一缺失拒绝；一次运行即可，不引入 review/correction budget。

### 输入与必须复验的内容

1. **原失败身份**
   - 对原 `run.json`、`failure.json`、`wrapper-result.json` 重新计算 SHA-256，并与第 1.3 节精确一致；
   - 原 child exit 仍记录为 1，不写成 0，不改 `failed/child_failed`；
   - failure 必须仅为 `ValueError: direct Ray R6 recorded exposure differs from frozen shutter`。

2. **Spec 与 checkpoint**
   - internal/Guide experiment ID、schema、source、状态、16 capture IDs、顺序、预算、固定 shutters 与 spec 一致；
   - `input-checkpoint.json`、run-local `inputs/location.json`、`inputs/code-duty-curve.json` 的 bytes/hash 一致；
   - spec 中 observer/policy/uncertainty/manifold/location/curve 引用与 hash 可追踪；
   - acquisition commit 与 dirty=false 仅作 metadata，不检查 branch/parent/tree ownership。

3. **16+16 data integrity**
   - captures 与 physical returns 各精确 16 行、ID 顺序相同；
   - 每个 CR3 与 sidecar 均位于同一 root、非 symlink、非空，bytes/SHA 与 physical ledger 一致；
   - remote capture/request ID 唯一且 sidecar association 通过；
   - 16 patch-statistics、58 feature identity/order、finite、clipping=0、near-noise、valid-pixel 等 frozen quality 条件全部通过；
   - 不删除帧、不重算阈值、不与 R5 或其他 root pooling。

4. **Command、timing 与 isolation**
   - command/readback 精确为连续 `A → D → A → B → A → C → A`；
   - 从首次 Ray on 到正常/异常 cleanup 之间没有 Ray-off command；
   - 开始时 both-off；状态间只验证 strip five-channel zero；
   - 16 covariate rows 与 capture order/state/timestamp/previous-state/observed elapsed 对齐；
   - operational 600 仍是 scheduler target 与 transient，不声称 steady 或精确曝光起点。

5. **曝光档位合同**
   - 协议权威是名义档位：A=`1/5000`、D=`1/6400`、B=`1/8000`、C=`1/2500`；
   - `Canon:ExposureTime` 只证明相机仍处于对应快门档位，不作为独立测量的真实积分时长；
   - 允许 Canon Tv 编码与常见分数字符串有少量差异；当前门禁为 `1/8 EV`，小于相邻常见档位间隔；
   - missing/nonfinite/fallback source 或足以表明另一档位的差异仍 fail closed；
   - 不因当前 `0.0001937745` 等记录值与 `1/5000` 的小差异而失败，也不据此宣称真实积分时长。

6. **Cleanup 与派生审计**
   - Python cleanup、shell cleanup、shell exit status、Ray zero 与 strip five-channel zero 全部通过；
   - 从现有 immutable ledgers 生成缺失的 `commands-audit.json`，标明 `derived_after_original_child_failure=true`；
   - 不覆盖已存在的 `quality.json`；在内存中重算后应与现有 16/16 结论一致，否则停止；
   - 任一原 artifact hash 漂移、非曝光失败、missing capture/hash、source isolation、command、timing、quality 或 cleanup 不一致均拒绝。

### 输出与小型复现证据

- 同一 root 内新增 `post-fix-revalidation.json`：记录 acquisition/validator commit、原 artifact hashes、复验项目、derived artifact hashes、`original_child_exit=1` 与 `original_failure_preserved=true`；
- 同一 root 内新增 `commands-audit.json`，并由 revalidation evidence hash；
- revalidation pass 后运行现有 Ray-only analyzer **一次**，输出 `analysis.json` 与 SHA-256；
- 记录 analyzer argv、feature-set artifact/hash、input root/hash 集合与判定理由；
- repo 只追踪小型摘要/manifest/hash，不追踪 CR3、sidecar 或大测量 payload。

### 完成结果（2026-08-08）

- same-root explicit revalidation：pass；原 child exit 仍为 `1`，原 failure preserved；
- acquisition/physical/quality：`16/16 / 16/16 / 16/16`；
- Ray analyzer：`formal_pass=false`、`return_anchor_history_effect=fail`、`steady_status=not_demonstrated`；
- scientific status：`history_dependent_at_operational_dwell_600`；
- M2/M3/M4：未进入并保持 locked；
- Advisor handoff：`.agent-work/ADVISOR_HANDOFF-20260808-RAY-R6-HISTORY-FAIL.md`。

### Pass/fail branch

- **Revalidation engineering invalid：** `science_delta=none`；不得运行 analyzer、不得重采、不得创建第二 root。报告 exact mismatch；普通代码问题可离线修复，但任何新的 formal acquisition 必须由 Human 另行决定。
- **Revalidation 发现合法 frozen quality hard fail：** 作为 Ray 有效科学负结果，strip/combined/TD-C 保持锁定，进入 M5 Advisor 回报；不得删帧、改曝光/阈值或重采。
- **Revalidation pass + analyzer history fail：** `history_dependent_at_operational_600`，是有效科学负结果；strip 保持锁定，进入 M5。
- **Revalidation pass + analyzer history pass：** 产出 `formal_pass=true`、`return_anchor_history_effect=pass`、`steady_status=not_demonstrated`；只解锁 M2。

### 明确禁止

- 重拍、第二 formal root、retry 或 alternate root；
- 把原 run/wrapper 改成成功；
- 新 runtime/framework/release/lineage/stage-gate/readiness/attestation/owner 状态机；
- analyzer 之前进入 strip；
- 将 tests、commit、quality revalidation 当成科学 pass。

### science_delta

M1 只有 Ray analyzer 的 history pass/fail 或合法 frozen quality fail 才产生新科学结论；离线重新验收本身只是 engineering delta。

---

## 4. M2 — 条件解锁的全新 strip TD-B

### Prerequisites

- M1 `analysis.json` 内容 hash 固定；
- Ray 结果明确同时满足 `formal_pass=true` 与 `return_anchor_history_effect=pass`；
- `steady_status=not_demonstrated` 与 operational-600 transient 声明保留；
- 新的当前执行说明冻结 exact root、命令、强度、时长、预算、abort、Ray-zero 和 cleanup；
- 不消费 R5 root；Ray R6 只通过 analysis/run artifact hash 关联。

### 唯一动作

用现有 `measure_p7_thermal_diagnostics.py --direct-strip-td-b` 路径，在一个全新唯一 root 执行一次 strip TD-B，并在 acquisition/quality 完整后运行一次 strip analyzer。

Exact scientific sequence：

```text
A0@600
→ D@60/120/300/600 → A_after_D@600
→ B@60/120/300/600 → A_after_B@600
→ C@60/120/300/600 → A_after_C@600
```

### 输入

- retained P7-R1 frozen strip commands，A/D/B/C command bytes/hash 不变，不调用 solver；
- frozen identity RAW observer、58 features、quality threshold、uncertainty、no-ambient statistic；
- frozen source-specific strip shutters/exposure envelope；formal 内禁止 auto exposure、weak reacquire 与 mid-run shutter change；
- formal=16、ambient=0、retry=0；若现有冻结合同确实缺少某档 shutter，只允许合同内 bounded non-formal setup，setup physical cap=8，总 physical cap=24；不得借此搜索或扩大 envelope；
- Ray 必须在每次 strip capture 前和所有边界保持 zero/readback。

### 输出与小型复现证据

- 一个新 run root：spec、run、16 capture/physical ledgers、commands、isolation、covariates、quality、Python/shell cleanup、wrapper 与 CR3 hashes；
- strip `analysis.json`、输入/输出 hash、exact command/shutter/sequence/budget；
- Git 只保存小型摘要、manifest、analysis、hash 与 cleanup evidence。

### Pass/fail branch

- **首次 device access 前的普通实现问题：** 在当前 worktree 最小修复，不创建额外架构阶段；仍只允许一个实际 launch。
- **Engineering invalid after launch：** `science_delta=none`，停止且不自动 retry/new root；保留原 evidence。
- **16-frame quality hard fail：** 有效 strip 科学负结果；combined/TD-C 锁定，进入 M5。
- **A-return history fail：** 有效 strip 科学负结果；combined/TD-C 锁定，进入 M5。
- **16/16 quality + history pass：** 只解锁 M3。

### 明确禁止

- 使用 R5 frame、把 Ray R6 frame 与 strip frame提前 pooling、让 Ray 非零；
- 改 observer/58 features/threshold/uncertainty/command/exposure envelope；若必须改变其中任一项，停止并请 Advisor 处理科学问题；
- 自动 retry、进入 combined/TD-C 或声称 600 秒 steady。

### science_delta

新 strip 16 帧与其 quality/history pass/fail 是科学进展；为执行它所做的普通修复、测试和提交不是。

---

## 5. M3 — Combined TD-B operational-600 gate

### Prerequisites

- Ray 与 strip 各自都是完整 16/16 quality/history pass；
- 两个 source run、analysis、spec、exposure、commands、cleanup artifact hashes 已冻结；
- 无 R5 frame consumption，无隐藏删帧或跨 root 替换。

### 唯一动作

运行一次纯离线 combined analysis。当前 live analyzer 若尚缺少 combined output，只在既有 `analyze_p7_thermal_diagnostics.py` 内补最小纯函数/CLI 分支与 focused behavior test；不得提前实现、不得新建 package/runtime/framework。

Combined 必须验证：

1. Ray 16/16 与 strip 16/16；
2. 两 source frozen measurement quality 全部通过；
3. 两 source `A0/A_after_D/A_after_B/A_after_C` history compatibility 全部通过；
4. exact exposure policy/shutter 与 input hashes 可追踪；
5. command/readback/source isolation 全部通过；
6. physical/formal ledger 与预算全部通过；
7. Python/shell cleanup 与 final zero 全部通过；
8. 无 R5/R6/strip 非法 pooling；
9. `steady_status=not_demonstrated` 保留；
10. acquisition checkpoint 作为 metadata 可追踪，artifact 内容不漂移。

### 输出与小型复现证据

```text
p7-td-b-operational600-analysis-v1.json
config/hsi/p7-operating-envelope-v3.json   # 仅 combined pass 时冻结
```

必须声明：

```text
operating_envelope = developer_selected_operational_600s_transient_v1
operational_dwell_s = 600
steady_claim = false
steady_status = not_demonstrated
TD_A_status = settling_not_demonstrated_by_600
return_anchor_history_compatibility_ray = pass
return_anchor_history_compatibility_strip = pass
previous_state_scope = exact_TD_B_A_D_A_B_A_C_A_sequence
```

输出记录 Ray/strip run 与 analysis hashes、analyzer commit/argv 和 exact decision reason，不含 release/owner/lineage。

### Pass/fail branch

- **Engineering invalid：** 无科学结论；在同一最小纯分析边界修复普通问题并重新计算，不访问设备。
- **Combined scientific fail：** 有效科学停止；`TD-C=locked`，进入 M5。一个 source 的通过不得抵消另一个 source 的失败。
- **Combined pass：** 冻结简化的 operating envelope v3，只解锁 M4。

### 明确禁止

- 设备访问、新采集、把 600 秒写成 `steady=true`/`settled=true`/`t_formal=600`/`TD_A_pass=true`；
- 生成 release、stage-gate、lineage 或 materialized package；
- combined pass 直接解锁 sentinel、endpoint expansion 或 P8。

### science_delta

Combined pass/fail 是对两 source operational-600 合同性的科学结论；实现 analyzer、测试或生成配置文件本身不是。

---

## 6. M4 — TD-C core：operational-600 order-balanced comparison

### Prerequisites

- M3 combined analysis 明确 pass；
- `p7-operating-envelope-v3.json` 已冻结并由内容 hash 引用；
- 当前执行说明冻结一个新 root、四个 sessions、预算、source isolation、abort 与 cleanup；
- 只允许 core，不允许 endpoint expansion。

### 唯一动作

用现有 `measure_p7_thermal_diagnostics.py --direct-td-c-core` 路径执行一个 TD-C core root，再运行一次 TD-C analyzer。

Exact core：

```text
state = H120/S100
observation dwell = 600 s
steady_claim = false

S1 Ray -> strip
S2 strip -> Ray
S3 Ray -> strip
S4 strip -> Ray

formal captures = 8
ambient diagnostics = 8 (每 session start/end)
physical cap = 16
```

每个 session：cold-proxy/source setup → start ambient → source 1 command/readback → 600 s → capture → off → source 2 command/readback → 600 s → capture → off → end ambient → 双 cleanup/readback。它只能称为：

```text
order-balanced comparison under operational_600s_transient
```

不得称为 steady ABBA、linear-drift elimination 或 steady source equivalence。

### 输入

- combined pass artifact/hash 与 operating envelope v3；
- frozen Ray/strip H120/S100 commands、source-specific shutters、observer、58 features、quality、uncertainty 与 P6 comparison evidence；
- current analyzer 在真正解锁 M4 时必须绑定现有 frozen P6 interpretability comparison；不得让默认 `not_evaluated` 人为制造 scientific fail，也不得在 M1/M2 前提前扩建该路径；
- exact device readback、ambient/black-level/geometry、covariates、source isolation 与 cleanup。

### 输出与小型复现证据

- 新 TD-C root 与 spec/run/8 formal+8 ambient/physical/command/isolation/covariate/quality/cleanup/wrapper hashes；
- `analysis.json` 包含：within-session difference compatibility、Ray-first vs strip-first order effect、stable centers、current Ray center vs P6 interpretability、ambient trend、failure branches；
- Advisor handoff pack 引用 code/config/run/artifact hashes，不复制 raw data。

### Pass/fail branch

- **Engineering invalid：** `science_delta=none`；停止实际设备推进，不自动 retry；普通 analyzer 问题只在既有 module 内最小修复。
- **Quality 或 core gate fail：** 保留为有效 TD-C core 科学结果，停止设备推进并进入 M5。
- **Core pass：** 保留为 TD-C core 科学结果，停止设备推进并进入 M5；不得自动运行 endpoint expansion。

### 明确禁止

- TD-C endpoint expansion（H0/S0、H300/S100）、classic ABBA、额外 session 或自动 retry；
- reference epoch 自动改写、sentinel、remaining 9、boundary、holdout、Gate-6、P8 或 LUT install；
- 将 ambient 作为 no-ambient TD-B statistic 的替代或更改 frozen science contract。

### science_delta

TD-C core 的完整 pass/fail 是本 GUIDE 路线的最终设备科学结果；执行准备、测试和提交不是。

---

## 7. M5 — Prescribed stop 与 Advisor handoff

### Prerequisites

发生以下任一项：

- Ray 合法 quality hard fail；
- Ray history fail；
- strip 合法 quality/history fail；
- combined fail；
- TD-C core 完成（pass 或 fail）；
- 或工程 invalid 导致无科学结论且当前物理 retry=0 已停止。

### 唯一动作

停止设备推进，生成一个小型、可追踪的 Advisor handoff/audit pack。工程 invalid 只报告给 Human；只有需要改变 frozen science contract、结果落入 GUIDE 未定义分支，或已到 GUIDE 规定的科学回报点时才请求 Advisor。

### 输入与输出

Pack 至少记录：

- 去工程化后的三个 direct owners 与最小复现合同；
- code commit、环境版本、clean/dirty metadata；
- exact CLI、spec/config/input hashes；
- Ray root、原失败 preservation、post-fix revalidation 与 Ray analysis；
- strip、combined、TD-C 的 entered/not-entered 状态及原因；
- CR3/ledger/quality/commands/isolation/covariates/cleanup hashes；
- Ray/strip history 与 operational-600 声明；
- TD-C core gates（若进入）；
- reference epoch 当前分类只能按证据报告，不能把 legacy `reference_epoch_shift=false` 推断为 no shift；
- 所有 downstream locks。

Raw CR3、sidecar、TIFF/PNG/decoded arrays 或其他实验 payload 保留在外置盘，不进入 Git；Markdown 报告、小型 JSON、manifest、hash、analysis 与 cleanup evidence 可追踪。

### 终态解释

- 合法 Ray/strip/combined scientific fail 或 TD-C core 完成，表示 GUIDE 4 已执行到其 prescribed terminal branch；
- engineering invalid 不是科学结果，也不能伪报 GUIDE scientific completion；
- 无论何种终态，均不自动进入下一锁定阶段。

### science_delta

M5 本身不创造新科学结果，只把前述结果压缩为 Advisor 可审计材料。

---

## 8. 全局安全、授权与停止规则

### 无需单独 Human 授权

- 纯离线 revalidation、hash、analysis、报告与配置计算；
- 明确限定在当前执行说明内的 Ray/strip on/off、zero-state setup、bounded light operation 与 Python/shell cleanup；
- 明确限定、只读的设备 identity/state/capability 与 zero readback。

这不表示 PLAN-FULL 本身授权未来实验。每个条件阶段解锁后，必须先写当前执行说明，精确限定目标、强度、时长、预算、source isolation、abort 与 cleanup；不得从上一次实验、release、analysis 或 light-control exception 推断更宽范围。

### 必须 Human 授权

- firmware flash/upload、remote deployment、破坏性硬件改动；
- 超出当前 GUIDE/Human 路线的新实验、目标、强度、范围、持续时间或 recovery path；
- 任何含糊、过期或无法覆盖确切危险操作的授权边界。

### 必须停止并考虑 Advisor

- 必须改变 frozen observer、58 features、clipping/near-noise/valid-pixel threshold、uncertainty、no-ambient statistic、fixed shutters/exposure envelope；
- 必须改变 exact sequence、formal/physical budget、retry=0 或 operational-600 非 steady 语义；
- source isolation 或 cleanup 无法保证；
- physical evidence 无法归类；
- 科学结果落入 GUIDE 未定义分支；
- 需要进入仍锁定阶段。

普通 import/parser/wrapper/analyzer/test 问题不是 Advisor 或新 architecture boundary；在当前最小 owner 内修复，不新增路线层。

---

## 9. 始终锁定的后续范围

即使 M4 TD-C core pass，也全部保持 locked：

```text
TD-C endpoint expansion
reference epoch final mutation/requalification
four-point sentinel
remaining 9
boundary / s_exact_max
holdout
Gate-6
P8 INT
default LUT/runtime installation
```

只能在 TD-C core 后向 Advisor 回报；任何后续解锁都需要新的科学指导或 Human 明确决定，不能由本 PLAN-FULL 自动推出。

---

## 10. 执行密度与证据纪律

- 每个 milestone 是一个科学上连贯的 batch，不为单个命令、selector、文件、assertion 或状态更新建立 PLAN/handoff。
- 只有具体 blocker 才允许最小 engineering work；修复后立即回到该 milestone 的科学动作。
- 不运行多轮 clean-room、重复 full suite、连续 clean review 或 correction budget；只做与当前 blocker/设备安全直接相关的一次 focused validation。
- acquisition、accepted quality/history result、scientific negative 或新解锁实验才计 `science_delta`。
- source/test/PLAN/commit/review/validation 只记 `engineering_delta`。
- 每次实际设备 launch 只允许当前里程碑定义的一个 root；physical failure 后不得自动创建替代 root。

---

## 11. 当前唯一 next action（重复确认）

```text
对
/Volumes/4T/temp/rgbww-optimizer/
guide4-ray-r6-20260808-20260808-153400-post-fix-valid/ray-r6

执行一次 explicit same-root offline engineering revalidation，
保留原 run/failure/wrapper 失败 bytes 与 hashes，
生成缺失的 derived commands audit 与 post-fix evidence，
通过后运行一次 Ray-only analyzer。
```

在得到 Ray `quality/history` 科学结果之前：

- 不重采；
- 不创建第二 formal root；
- 不访问设备；
- 不执行 strip；
- 不预先开发 combined/TD-C；
- 不修改 GUIDE/RESEARCH/Advisor 文档；
- 不把本 PLAN-FULL 当作执行授权。
