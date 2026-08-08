# RGBWW 灯带项目：GUIDE 4 科学优先去工程化与执行计划

**计划性质：** Human 对 GUIDE 4 实现边界的明确重置；可直接交给 Codex Planner / Executer。
**目标：** 在保留科学证据可复现性、设备安全和 fail-closed 测量判定的前提下，移除阻塞科学推进的治理型代码，并完成 GUIDE 4 规定的 Ray R6 → strip TD-B → combined TD-B → TD-C core → Advisor 回报路线。
**本计划不改变：** observer、58-feature、quality threshold、uncertainty、固定曝光、source isolation、cleanup、实验顺序、预算、失败分类和 downstream locks。
**本计划明确替代：** successor lineage release、stage-gate package、terminal seal、PLAN/FULL runtime binding、Git ancestry owner、predevice/E2/readiness attestation、archive machine contract 等实现机制。

---

## 0. 执行结论

当前不需要再次“设计一套正确架构”。正确路线是：

```text
从已保护的 main checkpoint 建立新分支
→ 让现有 P7 测量 CLI 成为唯一正式执行 owner
→ 用单一实验 spec + run manifest 保留可复现性
→ 删除 lineage/release/stage-gate/attestation/agent-work runtime 代码
→ 一次完整离线验证
→ 立即执行 Ray R6 16 帧
→ 按科学结果进入 strip TD-B、combined gate、TD-C core
→ 向 Advisor 回报
```

GUIDE 4 的科学执行完成定义不是“所有实验都必须通过”，而是：

1. 按冻结合同执行当前允许的实验；
2. 若出现合法 hard failure，保留为科学负结果并进入 GUIDE 指定停止分支；
3. 若通过，则继续到下一条件分支；
4. 最终形成可审计的 Advisor 回报材料；
5. 不擅自进入 sentinel、remaining 9、boundary、holdout、Gate-6、P8 或默认 LUT 安装。

---

## 1. 已核实的起始状态

### 1.1 Git 状态

归档中的关键 refs：

| Ref | Commit | 含义 |
|---|---|---|
| `origin/main` | `390321a6e903d86b167519e1c801e4046d7ba709` | 去工程化前的受保护 checkpoint |
| `origin/codex/backup-guide4-pre-deengineering-20260806` | 同上 | 已存在的远端备份 |
| `codex/guide4-science-first-deengineering` | `60ffc57e0589ca5bbd041ba3a5c7311c8321aac9` | 两轮去工程化失败后的 terminal 记录 |
| rejected initial candidate | `e62939456540c6de16b3cd05f8a15432ecf9ac94` | 删除 stage gate 后新建通用 science runtime，未接受 |
| rejected correction | `6234ffc3e2f87402b45402abbd036816bf09481a` | 对上述 runtime 的 bounded correction，仍未接受 |

当前失败分支的 production/test/docs blobs 已恢复到 `390321a`，因此无需再次合并、回滚或复制源码。

### 1.2 科学状态

已完成并继续保留：

- P0-R 至 P6；
- P7-R1 有效失败证据；
- TD-A 及 600 秒 operational transient 决策；
- R5 formal hard failure；
- EQ-R6 成功，state C 已选择固定曝光 `1/2500`；
- R5 前 11 帧仅允许 diagnostic，不得与 R6 pooling；
- Ray R6 是下一项科学动作。

下一实验：

```text
P7-TD-B-RAY-OP600-EXPOSURE-GUARDED-FORMAL-R6
```

它必须是 Ray-only、全新 root、完整 16 帧、launch=1、retry=0。

### 1.3 过度工程化规模

本次对归档的独立统计显示：

- 2026-07-29 后当前 ancestry 有约 556 个提交；
- `.agent-work` 产生约 1,575 次 file-touch events；
- 当前树中 `.agent-work` 有约 112,689 行、680 个文件；
- P7 相关 production 约 23,506 行，测试约 20,704 行；
- 可立即识别的 lineage/release/stage-gate/retained-R3 治理层至少包含：
  - production 11,129 行；
  - tests 13,975 行；
- 最大测试文件 `tests/test_p7_thermal_diagnostics.py` 约 4,934 行；
- 最大执行模块 `measure_p7_thermal_diagnostics.py` 约 4,562 行；
- `p7_thermal_diagnostics.py` 约 4,333 行，其中大段是 Git、lineage、release 与 owner 校验，不是测量科学。

这些数字只用于证明问题规模，不作为新的形式化验收门槛。

---

## 2. GUIDE 4 条款的保留、替代与删除

### 2.1 必须原样保留的科学与安全合同

以下内容不得在去工程化中修改：

- R5 为永久 hard-failed formal attempt；
- R5 retained 11 仅 diagnostic，R5/R6 pooling 禁止；
- identity RAW response；
- `R/G1/G2/B` 四平面；
- 58 个 frozen feature；
- clipping fraction 必须为 0；
- near-noise、valid pixels、finite、recorded exposure 等 quality gate；
- no ambient statistic；
- uncertainty、joint coverage 和 frozen evaluator；
- Ray R6 A/D/B/C 固定状态与 exact capture order；
- A=`1/5000`、D=`1/6400`、B=`1/8000`、C=`1/2500`；
- formal 16、physical cap 16、setup 0、launch 1、retry 0；
- formal 内禁止 auto exposure、weak reacquire、mid-run shutter change；
- strip 必须始终为零；
- 600 秒是 developer-selected operational transient，不是 steady；
- Ray history pass 才能进入新 strip TD-B；
- Ray 与 strip 通过后才可 combined gate；
- combined pass 后才可 TD-C core；
- TD-C core 仍是四个独立 session、8 captures 的 order-balanced comparison；
- sentinel、remaining 9、boundary、holdout、Gate-6、P8、默认 LUT 均继续锁定；
- Python cleanup、shell cleanup、readback zero 和失败证据保留。

### 2.2 由 Human 明确替代的实现机制

下列 GUIDE 4 实现条款不再按原工程形态执行：

| 原机制 | 替代机制 |
|---|---|
| successor lineage release | 单一 `experiment-spec.json` + 输入配置 SHA-256 + run manifest |
| release owner / path owner | 普通文件路径、内容 hash 与 schema 校验 |
| stage-gate package | 直接 protocol-specific CLI |
| launch descriptor / terminal seal | `run.json`、capture ledger、wrapper result 与 cleanup evidence |
| PLAN/FULL runtime binding | PLAN 只供人和 agent 阅读，production 不读取 |
| Git parent/tree/branch ancestry gate | 仅在 run manifest 记录当前 commit；不作为 runtime authority |
| public validator / predevice / E2 / zero-readiness 链 | 一次 direct fake-backend integration test + focused safety tests |
| materialized package identity | fresh run root + immutable experiment spec |
| archive-before-rewrite machine contract | Git history本身保留历史；`.agent-work` 为本地临时文件 |

这是实现机制替代，不是修改科学判断。不得以“GUIDE 文字曾要求 lineage”为理由重新引入 owner、manifest family、release consumption 或 package attestation。

### 2.3 明确禁止新增

本轮以及 GUIDE 4 后续不得新增：

- 新的 `runtime`, `owner`, `lineage`, `release`, `stage_gate`, `attestation`, `seal`, `qualification package`, `readiness package` 抽象；
- 为 Ray、strip、TD-C 预先设计的通用 workflow framework；
- production 对 `.agent-work`、`AGENTS.md`、Advisor Markdown、Git refs/branches/parents 的读取；
- 以 source-code string scan、AST identity、commit topology 或 plan machine row 作为设备执行门槛；
- 没有真实使用者的 replay CLI；
- 为证明“唯一入口”再建立另一层入口；
- 因普通实现 bug 创建 historical branch、terminal architecture boundary 或请求 Human 重新选架构；
- status-only、archive-only、plan-only 的高频提交。

---

## 3. 目标代码结构

不新增第三层 orchestration module。保留并收缩现有三个 owner：

```text
p7_thermal_diagnostics.py
  只拥有科学 protocol、capture sequence、状态、预算、quality/ledger validator

measure_p7_thermal_diagnostics.py
  唯一设备执行 CLI；拥有 command、readback、capture、timing、ledger、cleanup

analyze_p7_thermal_diagnostics.py
  唯一分析 CLI；拥有 Ray history、strip history、combined gate、TD-C analysis
```

允许抽取纯机械共享 helper，但必须满足：

- 解决已存在的重复，而不是为未来阶段设计；
- 不持有 stage/state machine；
- 不读取计划、Git 或 release；
- 不引入新的 execution authority；
- 不阻塞下一科学动作。

推荐最终 CLI：

```bash
python -m camera_based_rgbww_optimizer.optimization.measure_p7_thermal_diagnostics \
  ray-r6 --dry-run ...

python -m camera_based_rgbww_optimizer.optimization.measure_p7_thermal_diagnostics \
  ray-r6 --execute --human-authorization \
  P7-TD-B-RAY-OP600-EXPOSURE-GUARDED-FORMAL-R6 ...

python -m camera_based_rgbww_optimizer.optimization.measure_p7_thermal_diagnostics \
  strip-td-b ...

python -m camera_based_rgbww_optimizer.optimization.measure_p7_thermal_diagnostics \
  td-c-core ...
```

分析 CLI：

```bash
python -m camera_based_rgbww_optimizer.optimization.analyze_p7_thermal_diagnostics \
  ray-r6 --run-dir ...
```

具体 argparse 形式可沿用现有风格，但必须实现上述等价的一跳式用户路径。

---

## 4. Git 与工作区策略

### 4.1 不再重复 merge/backup

main 与 backup 已经存在于 `390321a`。本轮不得再次把 rejected deengineering commits 合并到 main，也不得再创建一组重复 backup。

### 4.2 新分支

从受保护 main checkpoint 新建干净分支：

```bash
git fetch origin
git switch -c codex/guide4-science-path-v2 \
  390321a6e903d86b167519e1c801e4046d7ba709
```

现有 `codex/guide4-science-first-deengineering` 保持历史证据，不再作为实现输入。

### 4.3 `.agent-work`

执行第一阶段时：

1. 从 live tree 删除所有已跟踪 `.agent-work` 文件；
2. 在 `.gitignore` 加入 `.agent-work/`；
3. Codex 仍可在本地创建 `PLAN.md`、`PLAN-FULL.md`、review 或 scratch，但一律不提交；
4. production/test 不得读取该目录；
5. 历史内容继续存在于 Git history，无需复制到新 archive。

### 4.4 提交纪律

预期在第一次 Ray R6 前最多 2–4 个有实质源码意义的提交，例如：

```text
refactor(project): remove agent governance from live runtime
refactor(p7): expose direct Guide 4 experiment path
refactor(p7): delete lineage and stage-gate dead code
test(p7): retain scientific and safety contracts
```

规则：

- 不为 PLAN、archive、status、review 单独提交；
- 不在每次小修复后 commit；
- 普通 bug 直接在当前 section 修复；
- 不自动 push；
- scientific run 完成后只提交必要的配置/摘要，不提交 CR3 或大运行目录。

---

## 5. PLAN-FULL 执行阶段

本计划只允许 **两个 engineering sections 位于 Ray R6 之前**。第二个完成后必须进入科学动作，不得插入第三个重构 section。

## E1 — 建立唯一直接科学执行路径

### E1.1 项目规则收缩

重写根 `AGENTS.md`，只保留：

- 项目科学目标与固定 Canon observer 范围；
- 设备安全、source isolation、cleanup；
- Human 高风险授权边界；
- GUIDE/RESEARCH 科学输入不可伪造；
- production 不读取 agent/Git/plan/governance 文件；
- 工程是科学手段，ready 后立即实验；
- 测试和提交的最小规则。

删除六角色 runtime governance、Supervisor/Orchestrator machine state、archive contract、package cap、PLAN machine row 等大段流程。

### E1.2 直接 Ray R6 plan

在现有 `p7_thermal_diagnostics.py` 中保留或建立一个纯函数：

```python
build_ray_r6_spec() -> dict
```

它只从冻结 scientific config 读取：

- exposure policy v2；
- operating envelope；
- observer/feature/uncertainty policy；
- frozen state commands；
- exact capture sequence。

它不得读取：

- `.agent-work`；
- Git parent/tree/branch；
- old release/package root；
- lineage candidate；
- launch descriptor；
- stage-gate package。

### E1.3 唯一生产入口

修改 `measure_p7_thermal_diagnostics.py`：

- direct `ray-r6` CLI 构建 spec；
- 验证 exact Human authorization token；
- 创建 fresh run root；
- 创建 `experiment-spec.json`；
- 调用现有真实 command/readback/capture/feature/cleanup mechanics；
- 不经过 `p7_td_b_r6_stage_gate`；
- 不经过 release consumption；
- 不需要 code-checkpoint 参数；
- run 起点可记录 `git rev-parse HEAD` 和 worktree clean 状态作为 metadata，但不得据 branch/parent 拒绝；
- direct CLI 的 dry-run 不访问网络或设备。

### E1.4 wrapper

把 `tmp/run-p7-thermal-diagnostics.zsh` 简化为：

1. 启动唯一 runner；
2. 记录 PID、exit code、signal；
3. 所有出口执行 shell `all_off`；
4. 写 `wrapper-result.json`；
5. 不调用 terminal classify/finalize；
6. 不支持旧 stage-gate package command；
7. 不保留双语义兼容分支。

### E1.5 critical quality extraction

从 `p7_td_b_r6_terminal.py` 提取真正与科学/安全有关的最小逻辑：

- per-capture quality projection；
- 16-row exact ledger validation；
- fixed shutter/feature/recorded exposure checks；
- final zero/cleanup evidence checks。

把它放回 `p7_thermal_diagnostics.py` 或 analyzer；不得以新的 `terminal owner` 名义建立模块。

### E1.6 E1 tests

必须真实覆盖：

1. dry-run exact 16 capture IDs；
2. A/D/B/C shutters exact；
3. fake remote backend 完整 16 captures；
4. physical cap=16；
5. strip zero before every Ray capture；
6. no ambient、no auto-exposure、no weak reacquire；
7. fresh root；
8. R5/R6 pooling 被拒；
9. clipping、near-noise、nonfinite、missing exposure、invalid pixels 各自 hard fail；
10. success/failure/signal 均执行 Python + shell cleanup；
11. output artifact 能被 analyzer 直接读取；
12. direct CLI 是唯一生产入口。

### E1 acceptance

```text
- direct ray-r6 dry-run 可用
- full fake 16-frame run 可用
- 无 production import p7_td_b_r6_stage_gate
- 无 production read .agent-work / Git topology / release package
- focused science+safety tests pass
- 一次 independent review；发现普通问题直接修复，不 terminal
```

E1 通过后立即进入 E2，不创建新的 architecture review package。

---

## E2 — 删除治理层并收缩测试

### E2.1 立即删除的 production 文件

在确认 direct runner 不依赖后，删除：

```text
src/.../optimization/p7_td_b_r6_stage_gate.py
src/.../optimization/p7_td_b_r6_terminal.py
src/.../optimization/p7_retained_release_audit.py
src/.../optimization/p7_successor_lineage.py
src/.../optimization/p7_successor_predevice.py
src/.../optimization/p7_successor_zero_readiness.py
src/.../optimization/p7_successor_e2.py
src/.../utils/agent_work_machine_contract.py
src/.../utils/p7_retained_r3_controller_conformance.py
src/.../utils/p7_retained_r3_controller_domain_template.py
src/.../utils/p7_retained_r3_controller_preparation.py
src/.../utils/p7_retained_r3_controller_runtime.py
src/.../utils/p7_retained_r3_exact_five_controller.py
src/.../utils/p7_retained_r3_offline_patch_preflight.py
src/.../utils/p7_retained_r3_provenance_io.py
src/.../utils/p7_retained_r3_real_manifest_domain_template.py
src/.../utils/p7_retained_r3_real_manifest_self_check.py
```

删除 `config/hsi/p7-governance-lineage-successor-v1.json`。

上述列表单独约 11,129 production LOC；Git history 已保留，不得把它们移动到 repo 内另一个 archive 目录。

### E2.2 从大模块删除的代码族

从 `p7_thermal_diagnostics.py` 删除：

- EQ family manifest build/audit runtime dependency；
- setup release lineage；
- changed-path/checkpoint ancestry；
- agents policy lineage；
- governance successor；
- public default successor lineage；
- workflow path lineage；
- cleanup test provenance owner；
- planner lineage candidate；
- setup lineage release/replay；
- stage gate machine status。

保留：

- scientific constants/spec；
- command/shutter/state mapping；
- direct plan builder；
- timed schedule；
- covariates；
- quality/ledger validator；
- TD-A/B/C science helpers。

从 `measure_p7_thermal_diagnostics.py` 删除：

- setup release writer/consumer；
- lineage qualification evidence；
- stage-gate package CLI；
- predevice/E2/zero-readiness；
- EQ-R6 orchestration machinery已完成且不再运行的 production branches；
- code checkpoint/tree authority；
- old CLI compatibility branches。

保留：

- actual camera backend；
- apply/readback；
- timed capture；
- RAW extraction；
- physical return ledger；
- source isolation；
- cleanup；
- direct Ray/strip/TD-C protocol commands。

从 analyzer 删除：

- release/commit/manifest owner 校验；
- retained package consumption；
- 与科学判定无关的 code checkpoint gate。

保留：

- capture/data integrity；
- feature hash；
- chronology；
- return-anchor compatibility；
- Ray/strip/combined/TD-C 分支；
- fail-closed scientific status。

### E2.3 测试删除与重组

删除所有对应 governance 测试，至少约 13,975 LOC，包括：

```text
test_agent_work_machine_contract.py
test_p7_td_b_r6_stage_gate.py
test_p7_td_b_r6_contract.py
test_p7_retained_release_audit.py
test_p7_successor_*.py
test_p7_retained_r3_*.py
```

同时删除下列测试类型：

- Markdown/PLAN/FULL parser；
- Git branch/parent/tree identity；
- source code string scan；
- package root owner；
- release qualification；
- attestation/terminal seal；
- “哪个模块是 owner”的结构性断言；
- 已删除旧 CLI 的 backward compatibility。

把 P7 测试收敛到少量按行为组织的文件，例如：

```text
test_p7_protocol.py
test_p7_acquisition.py
test_p7_analysis.py
test_p7_wrapper.py
```

文件名不是硬要求，行为覆盖才是要求。

### E2.4 strip 与 TD-C direct path

E2 同时建立但不解锁：

- `strip-td-b` direct protocol；
- `td-c-core` direct protocol；
- 对应 fake-backend tests；
- strip 只接受 `ray-r6-analysis.json` 中明确的 scientific pass；
- TD-C 只接受 combined analysis 中明确 pass；
- prerequisite 只校验 artifact schema、hash、experiment ID 和 scientific status；
- 不生成 package、release 或 lineage。

### E2.5 唯一完整验证

E2 完成后只运行一次：

- remaining full unit suite；
- compileall；
- wrapper syntax；
- `git diff --check`；
- direct fake R6 integration；
- direct fake strip integration；
- direct fake TD-C integration。

CodeGraph 可作为开发辅助，但不是 acceptance gate。

### E2 acceptance

```text
- 上述 governance modules/tests 已删除
- .agent-work 已从 live tree 移除并 gitignored
- production 不含 agent/Git/release/lineage/stage-gate authority
- direct Ray/strip/TD-C paths 都有行为测试
- remaining full suite once passes
- 一次 review；普通问题在 E2 内修复
- 下一 PLAN 必须是 Ray R6 scientific action
```

不得在 E2 后新增 E3 工程清理 section。

---

## S1 — Ray R6 正式 16 帧

### S1.1 Exact protocol

```text
experiment_id = P7-TD-B-RAY-OP600-EXPOSURE-GUARDED-FORMAL-R6
source = Ray only
strip = zero throughout
ambient = 0
launch = 1
retry = 0
formal logical = 16
physical cap = 16
operating dwell = 600 s transient, steady_claim=false
```

Capture order：

```text
000-ray-a0-t600
001-ray-d-t60
002-ray-d-t120
003-ray-d-t300
004-ray-d-t600
005-ray-a-after-d-t600
006-ray-b-t60
007-ray-b-t120
008-ray-b-t300
009-ray-b-t600
010-ray-a-after-b-t600
011-ray-c-t60
012-ray-c-t120
013-ray-c-t300
014-ray-c-t600
015-ray-a-after-c-t600
```

Exposure：

```text
A = 1/5000
D = 1/6400
B = 1/8000
C = 1/2500
```

### S1.2 Run artifact

每次 run root 必须包含最小集合：

```text
experiment-spec.json
run.json
commands.jsonl
captures.jsonl
physical-captures.jsonl
isolation-gates.jsonl
thermal-covariates.jsonl
capture-quality.jsonl 或等价字段
commands-audit.json
all-off-python.json
all-off-shell.json
wrapper-result.json
CR3 files
```

每个输入 config、spec 和 CR3 记录 SHA-256。

### S1.3 分支

#### A. Run invalid

包括 transport、missing CR3、source isolation、readback、capture ownership、cleanup 或 wrapper failure。

```text
classification = engineering_invalid
science conclusion = none
retry = prohibited automatically
next = Human receives exact invalidity evidence
```

普通 bug 不叫“新架构问题”，但 R6 retry=0 仍意味着不能自动再启动 formal run。

#### B. 任何 formal quality hard fail

```text
classification = accepted_hard_failed_formal_attempt
strip = blocked
science_delta = valid negative result
```

不得删帧、换 threshold、改曝光、pool R5、重跑或把失败改成工程错误。

#### C. 16/16 quality pass、history fail

```text
classification = history_dependent_at_operational_600
strip = blocked
science_delta = valid negative result
```

#### D. 16/16 quality pass、history pass

```text
classification = accepted_for_strip_entry
next = S2 strip TD-B
```

---

## S2 — 新 strip TD-B 16 帧

前提：Ray R6 analysis 明确 `accepted_for_strip_entry`。

要求：

- 新 root；
- 使用 frozen strip commands；
- 16 formal；
- A/D/B/C 结构与 600 秒 return anchors；
- Ray 在 strip capture 前为零；
- 不读取 R5 root；
- Ray R6 只通过 immutable artifact reference/hash 关联；
- observer、feature、uncertainty、command、exposure envelope 不变。

分支：

- invalid → 停止，保留工程 invalid evidence；
- quality fail → accepted scientific negative，combined/TD-C 锁定；
- history fail → accepted scientific negative，combined/TD-C 锁定；
- pass → S3 combined gate。

---

## S3 — Combined TD-B operational-600 gate

这是纯分析步骤，不创建设备 package。

输出建议：

```text
p7-td-b-operational600-analysis-v1.json
```

必须声明：

```text
operating_envelope = developer_selected_operational_600s_transient_v1
operational_dwell_s = 600
steady_claim = false
TD_A_status = settling_not_demonstrated_by_600
return_anchor_history_compatibility_ray = pass
return_anchor_history_compatibility_strip = pass
```

Combined pass 才生成简化后的：

```text
config/hsi/p7-operating-envelope-v3.json
```

该文件只含科学条件、来源 run hashes 和 status，不含 release/owner/lineage。

Combined fail 时 TD-C 锁定并形成 Advisor 材料。

---

## S4 — TD-C core

前提：combined TD-B pass 且 operating envelope v3 冻结。

Protocol：

```text
state = H120/S100
observation dwell = 600 s
steady_claim = false
S1 Ray -> strip
S2 strip -> Ray
S3 Ray -> strip
S4 strip -> Ray
formal = 8
```

只能称为：

```text
order-balanced comparison under operational_600s_transient
```

不得称为 ABBA drift elimination 或 steady comparison。

TD-C core 完成后停止设备推进，生成 Advisor audit pack。即使 core pass，也不自动运行 endpoint expansion、sentinel 或后续 P7/P8。

---

## S5 — GUIDE 4 Advisor 回报

Advisor pack 至少包含：

1. 去工程化后的唯一 runtime 路径与简化后的复现合同；
2. 删除的治理层列表及 remaining test suite；
3. Ray R6 acquisition、quality、chronology、history；
4. strip TD-B（若获解锁）；
5. combined gate（若获解锁）；
6. TD-C core（若获解锁）；
7. 每个未进入阶段的明确原因；
8. reference epoch 当前分类；
9. downstream locks；
10. exact code commit、config hashes、run roots 和 artifact hashes。

GUIDE 4 在以下任一情形视为“已按合同执行到终态”：

- Ray R6 合法 hard fail；
- Ray R6 history fail；
- strip 合法 fail；
- combined fail；
- TD-C core 完成；
- 或工程 invalid 导致无科学结论，但已按 retry=0 报告并停止。

其中只有前四类科学失败与 TD-C 完成属于 scientific result；工程 invalid 只是执行终止，不得伪报科学结论。

---

## 6. 最小可复现性合同

可复现性只要求以下内容：

### 6.1 Code and environment

- code commit；
- clean/dirty metadata；
- Python 与关键 package 版本；
- camera bridge/firmware/device readback；
- exact CLI argv。

commit 只作为 metadata；不校验 parent、branch、tree owner 或 package ancestry。

### 6.2 Frozen scientific inputs

- observer config path/hash；
- feature IDs/hash；
- uncertainty/hash；
- operating envelope/hash；
- exposure policy/hash；
- state commands/hash；
- capture sequence；
- budgets；
- Human authorization experiment ID。

### 6.3 Physical evidence

- CR3 path、bytes、SHA-256；
- recorded exposure；
- command/readback；
- source-isolation gates；
- monotonic timestamps和 thermal covariates；
- quality result；
- cleanup/readback zero。

### 6.4 Analysis

- analyzer version/commit；
- exact input run hashes；
- output JSON；
- pass/fail reason；
- no hidden frame deletion或 pooling。

不需要：

- release package；
- lineage owner；
- terminal seal；
- materialized stage gate；
- PLAN hash；
- Git ancestry manifest；
- public validator family；
- archive package。

---

## 7. Review 与失败处理规则

### 7.1 Review cadence

每个 engineering section：

1. 实现；
2. focused tests；
3. 一次独立 review；
4. 有问题则在同 section 修复并复测受影响项；
5. 修复后可再 review 一次；
6. 不要求连续两轮无发现；
7. 不把 review 次数写成 runtime contract。

### 7.2 不得 terminal 的普通问题

以下均在当前 section 内正常修复：

- import/name error；
- parser option遗漏；
- wrapper test仍引用旧 CLI；
- readiness字段过宽；
- fake backend adapter不完整；
- analyzer调用签名不一致；
- dead branch；
- skip body未删；
- ordinary test failure。

这些问题正是之前被错误升级为 `WAIT_FOR_HUMAN_NEW_ARCHITECTURE_BOUNDARY` 的类型。

### 7.3 真正停止条件

仅在以下情况停止并请求 Human/Advisor：

- 必须改变 frozen observer、58-feature、threshold、uncertainty 或 exposure；
- exact 16 sequence、budget、retry 或 600 秒语义需要改变；
- source isolation 或 cleanup 无法可靠实现；
- 设备/相机产生无法归类的 physical invalidity；
- 科学结果落入 GUIDE 未定义的新分支；
- 需要进入 sentinel/P8 等仍锁定阶段。

---

## 8. 去工程化完成标准

全部满足才可称为彻底完成：

### Runtime

- 正式执行一跳到真实 acquisition owner；
- 无 stage-gate package；
- 无 release consumption；
- 无 runtime plan/Git ownership；
- wrapper 只有 process + cleanup responsibility；
- analyzer 直接消费 run artifacts。

### Codebase

- 列出的 governance modules/tests 已删除；
- `.agent-work` 不再跟踪；
- production 无 `.agent-work`/Git topology/Advisor Markdown dependency；
- `p7_thermal_diagnostics.py` 与 `measure_p7_thermal_diagnostics.py` 的治理代码族已删除；
- 没有新建等价的 runtime framework；
- historical code只存在于 Git history，不存在 live archive copy。

### Tests

- 测试集中于科学和安全行为；
- 无 owner/lineage/package/plan parser tests；
- direct Ray/strip/TD-C fake integration均存在；
- remaining full suite在 E2 末尾一次通过。

### Scientific throughput

- E2 后下一动作确实是 Ray R6；
- 不再以 engineering readiness 为独立阶段；
- GUIDE 4 按结果推进到 prescribed stop 或 TD-C core；
- Advisor pack 可从 run artifacts直接生成。

---

## 9. 给 Codex 的执行指令

```text
你正在执行“GUIDE 4 科学优先去工程化与执行计划”。

Human 已明确覆盖 GUIDE 4 中纯工程性的 successor-lineage/release/package/stage-gate/PLAN-runtime-binding 实现要求；科学、测量、quality、预算、安全和阶段锁不变。不得请求 Advisor 解决工程架构、lineage owner、Git topology 或 package ownership。

从 390321a6e903d86b167519e1c801e4046d7ba709 新建 codex/guide4-science-path-v2。不要合并 60ffc57，不要创建新的 backup/historical branch，不要把 rejected runtime 当设计输入。

Ray R6 前只允许两个 engineering sections：E1 唯一直接执行路径，E2 删除治理层并完成一次完整离线验证。E2 后必须立即进入 Ray R6，不得插入第三个重构、review、readiness、attestation 或 archive package。

生产代码的唯一执行 owner 是 measure_p7_thermal_diagnostics.py；科学 protocol/validator 在 p7_thermal_diagnostics.py；分析 owner 是 analyze_p7_thermal_diagnostics.py。不得创建新的通用 science runtime。

普通实现 bug 在当前 section 内修复，不得升级为 terminal architecture boundary，不得因 package/review次数耗尽停止。只有 frozen scientific contract、安全合同或 GUIDE 未定义科学分支需要 Human/Advisor。

按本计划逐 section 实现并 review。所有计划和 scratch 可写本地 .agent-work，但该目录不跟踪、不归档、不被 production读取。
```

---

## 10. 唯一下一动作

新建 `codex/guide4-science-path-v2`，执行 **E1：建立唯一直接科学执行路径**。不得继续修补 `e629394`、`6234ffc`、`6b3a10d` 或 `00312b8`，也不得从它们复制 runtime 设计。
