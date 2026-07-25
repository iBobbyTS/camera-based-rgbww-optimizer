# GUIDE 当前未完成任务完整计划参考

**文档状态：** `planner_reference_current`

**快照日期：** `2026-07-25`

**Owner：** Planner

**执行属性：** `non_executable_reference`

> 本文件保存当前适用 GUIDE 所要求、但尚未完成的完整路线，包括 active、blocked、locked、conditional、
> deferred 和 decision-owned 分支。它不是执行队列，也不授权设备访问、重试、阶段进入、预算、Git 操作或
> 配置安装。Executer 只能执行 `.agent-work/PLAN.md` 中唯一已放行的工作包。

## 1. 文档合同

### 1.1 两层计划所有权

- `.agent-work/FULL_PLAN_REFERENCE.md`：Planner 维护的完整未完成路线，回答“整个 GUIDE 还有什么要做”。
- `.agent-work/PLAN.md`：唯一可执行合同，回答“Executer 现在只做什么、做到哪里必须停”。
- active PLAN 应引用本文件中的一个 task ID；当前 Z0 PLAN 早于本规则建立，由本文件反向绑定，下一次
  Planner 重写 PLAN 时必须显式加入 task ID。
- 本文件中的后续步骤、命令示例、预算上限和条件分支都不能被 Executer 直接消费为授权。

### 1.2 来源优先级

科学方向与产品决定按以下顺序解释：

1. 后来的显式 Human/Developer 决定；
2. 最新适用的 Advisor GUIDE；
3. 早期 GUIDE 中未被替代的要求；
4. Planner review archives 和实现文档提供的执行/证据现状。

active PLAN 是唯一执行边界，但不得静默放宽上述科学合同。发现冲突时，Planner 必须把冲突写成 decision task，
不能由 Executer 选择一个解释继续。

### 1.3 状态词

| 状态 | 含义 |
| --- | --- |
| `ACTIVE` | 当前 active PLAN 唯一放行的任务。 |
| `NEXT_REVIEW` | 只在当前结果交回后由 Planner 执行的验收/分支工作。 |
| `BLOCKED` | 前置证据或决定未满足，不能写入执行 PLAN。 |
| `LOCKED` | GUIDE 明确禁止当前进入。 |
| `CONDITIONAL` | 只有命名分支出现时才成为待执行任务。 |
| `DEFERRED` | 尚未完成，但后来的决定已将其移出当前主路线。 |
| `ADVISOR_DECISION` | 需要 Advisor 冻结科学方向；不是危险操作授权请求。 |
| `HUMAN_DECISION` | 需要 Human 决定产品范围、危险操作或最终安装。 |

### 1.4 Planner 更新规则

发生以下任一事件时，Planner 必须在归档 review 后、重写下一份 active PLAN 前更新本文件：

- 新 GUIDE、RESEARCH 结论或显式 Human/Developer 决定到达；
- Executer 结果被接受、拒绝、分支或发现计划矛盾；
- 某 task 完成、解锁、重新锁定、改为 deferred 或需要新的 decision owner；
- 依赖 artifact、checkpoint、产品语义或安全边界发生变化。

每次更新必须：

1. 更新来源路径、SHA-256 和快照日期；
2. 更新状态总表和依赖关系；
3. 为新任务分配稳定 ID，不复用已删除 ID；
4. 将已完成细节移入 `.agent-work/PLANS/` review archive，仅在第 3 节保留必要 baseline；
5. 在 active task 行记录当前 PLAN path/hash；
6. 验证所有 `ACTIVE` 恰好一个、所有依赖 ID 存在、Markdown 结构和 `git diff --check` 通过；
7. 不在本文件复制 secret、临时凭据或可执行的无界设备命令。

## 2. 冻结来源与当前证据锚点

| 来源 | SHA-256 | 本文件用途 |
| --- | --- | --- |
| `advisor/1/1.GUIDE.md` | `f89a6e79026f3cb765f84f0d98b254dff0a5807ee772368dbb935a6843c7871b` | P7/P8/P9 长期目标、验证与安装分支。 |
| `advisor/2/1.GUIDE.md` | `885d761ba04586613bafe399c6bf03519043a44341eb22b586d24dcbfb3d6e26` | P7 v2 uncertainty、sentinel 4+9、gamut、holdout 和 P8 lock。 |
| `advisor/3/1.GUIDE.md` | `92f766da523c40ff49c228c996dffd6d3839552f70bbd79aa7627485dd749be1` | 当前 thermal/reference 路线；替代直接进入 sentinel 的旧路径。 |
| `advisor/4/0.AUDIT/03-human-decision-no-extension.md` | `c917c54473aa3c5cc4da9098ddeb81fb109fe9a4186fb71e994c447c63d0454a` | Human 拒绝 900/1200 秒，选择 600 秒 operational dwell；不得称为 settled。 |
| `.agent-work/PLANS/20260725-1031-p7-td-b-r1-c3-e2-r1-c2-review.md` | `8bc00632f878041dde21fb03709f248f8e33b6cdf104f3055bdd041752c9b17a` | 最近已接受的 progressive-evidence C2 review。 |
| `.agent-work/PLAN.md` | `b34b4868d8ef8fbfad8a4fe174c8728be206170cd511e643f2b6f0d38e0668a9` | 当前唯一 Z0 执行合同。 |

若上表任一文件内容变化，Planner 必须重新判断是否为合法 source update，而不是只替换 hash。

## 3. 已完成或保留的 baseline（不再列为待执行）

- `P0-R through P6 = retained`；P6 保留 `full_periodic_2d_HB`、HSI/RGB endpoint 分离、SAT0 Hue
  undefined，不重拍完整 106 点。
- P4 已按后来 Gate-3 决定停止：`keep_white_lut_diagnostic_only; stop_before_p5`。当前 HSI 主路线不等待
  新 CCT P5；完整 CCT 分支见 `REF-CCT-01`。
- P7 offline implementation、identity RAW、58-feature、joint 99.73% coverage、trend `4.0`、dominance
  `0.5`、ordinary 3 confirmations、boundary/holdout 5 confirmations和 full-scale/INT100 scope 均保留。
- P7-D0 已接受；P7-R1 acquisition 作为 valid-failure evidence 保留，candidate 不是 formal，禁止自动重跑 R1。
- TD-A acquisition/evidence 已接受，科学结果仍是 Ray/strip
  `settling_not_demonstrated_by_600`。
- Human 明确拒绝 900/1200 秒 extension；`600` 仅是
  `developer_selected_operational_dwell_s`，`t_formal_provisional_s` 和 `t_formal_s` 仍不得伪造为 600。
- TD-B v2 离线合同、setup provenance、sidecar/physical ledger 修复、no-ambient statistic owner、evidence
  manifest 和 lineage release 已完成；这些只提供可重放前置证据，不表示 formal 完成。
- 首次 Ray TD-B formal 在首张 `A@600s` 后因六个 plane-feature 低信号 quality rejection hard-fail；该张
  CR3/sidecar 仅是 immutable forensic evidence，不计入未来 fresh 16。
- 随后的 E2 因 external Git-root bug 失败；C1 离线修复已接受。唯一 fresh E2 又因
  `bedroom-rgbww-strip.local` 解析超时 hard-fail；C2 progressive-evidence correction 已由 Planner 以实际
  count `265` 接受。当前只放行 Z0。

## 4. 未完成路线总表

| Task ID | 状态 | 任务 | 直接依赖 | 解锁/决定 owner |
| --- | --- | --- | --- | --- |
| `REF-P7-01` | `ACTIVE` | 一次 zero-only Z0 reachability gate | 已接受 C2 | active PLAN / Planner |
| `REF-P7-02` | `NEXT_REVIEW` | Z0 验收与恢复分支选择 | `REF-P7-01` 结果 | Planner |
| `REF-P7-03` | `BLOCKED` | fresh E2 readiness/final-zero gate | Z0 pass + 新 PLAN | Planner |
| `REF-P7-04` | `LOCKED` | fresh Ray/strip TD-B formal 与 paired finalizer | E2 pass + exact release | Planner |
| `REF-P7-05` | `BLOCKED` | TD-B 科学验收与 operating-envelope freeze | `REF-P7-04` | Planner |
| `REF-P7-06` | `CONDITIONAL` | H0 full-scale vs 3072 thermal diagnostic | TD-B 指定失败分支 | Planner；必要时 Advisor |
| `REF-P7-07` | `ADVISOR_DECISION` | 600-second override 下的 TD-C prerequisite 解释 | TD-B history compatible | Advisor/Planner |
| `REF-P7-08` | `LOCKED` | TD-C order-balanced core | `REF-P7-07` 明确放行 | Planner |
| `REF-P7-09` | `LOCKED` | TD-C endpoint expansion | TD-C core accepted | Planner |
| `REF-P7-10` | `BLOCKED` | reference epoch 分类与 P6 compatibility | TD-C required scope complete | Planner |
| `REF-P7-11` | `CONDITIONAL` | 7-point / 13-node Ray requalification | reference branch B/C | Advisor |
| `REF-P7-12` | `ADVISOR_DECISION` | thermal/reference AUDIT PACK 与 sentinel 解锁 | reference class explainable | Advisor |
| `REF-P7-13` | `LOCKED` | 四点 sentinel v2 | Advisor explicit release | Planner |
| `REF-P7-14` | `LOCKED` | remaining 9 INT100 pilot points | sentinel accepted | Planner |
| `REF-P7-15` | `LOCKED` | full-scale boundary 与 scale-relaxed diagnostics | 13-point pilot accepted | Planner |
| `REF-P7-16` | `LOCKED` | P7 independent holdout 与 runtime gamut semantics | boundary evidence | Planner |
| `REF-P7-17` | `ADVISOR_DECISION` | P8 entry review | P7 holdout accepted | Advisor |
| `REF-P8-01` | `LOCKED` | INT dimension acquisition/model/holdout | Advisor P8 release | Planner |
| `REF-G6-01` | `ADVISOR_DECISION` | Gate-6 final candidate/product freeze | P8 accepted or range restricted | Advisor + Human product decision |
| `REF-P9-01` | `LOCKED` | immutable final independent validation | Gate-6 freeze | Planner |
| `REF-G7-01` | `ADVISOR_DECISION` | Gate-7 technical delivery decision | P9 complete | Advisor |
| `REF-OPS-01` | `HUMAN_DECISION` | install、smoke test、rollback 与交付 | Gate-7 + Human approval | Human/Planner |
| `REF-CLOSE-01` | `BLOCKED` | final stage AUDIT PACK 与路线关闭 | install/hold/rollback result | Planner/Advisor |
| `REF-CCT-01` | `DEFERRED` | 完整 CCT/GM P5 候选分支 | 新 Advisor/Human reopen | Advisor/Human |
| `REF-ABBA-01` | `DEFERRED` | classic ABBA mini-run | drift assumptions separately proven | Advisor |
| `REF-P6-FULL-01` | `DEFERRED` | 完整 P6 106-point re-capture | 7/13 点证明 topology/curvature 变化 | Advisor |
| `REF-LUX-01` | `DEFERRED` | 绝对照度/绝对亮度复制 | 新 metrology GUIDE | Advisor/Human |

主依赖链为：

```text
Z0 -> Planner review -> E2 -> TD-B -> TD-B review
   -> TD-C contract decision -> TD-C core -> conditional endpoints
   -> reference classification -> conditional requalification -> Advisor review
   -> sentinel 4 -> remaining 9 -> boundary -> holdout -> P8 entry review
   -> P8 -> Gate-6 -> P9 -> Gate-7 -> Human install/hold decision -> final audit
```

任一箭头都只是依赖关系，不是自动续跑授权。

## 5. 当前恢复链

### REF-P7-01：一次 zero-only Z0 reachability gate

**状态：** `ACTIVE`

**active PLAN：** `.agent-work/PLAN.md`，SHA-256
`b34b4868d8ef8fbfad8a4fe174c8728be206170cd511e643f2b6f0d38e0668a9`

**目标：** 只判断 exact `bedroom-rgbww-strip.local:6053` 的 ESPHome Native API 是否可达，并取得五个
generation-bearing exact-zero readback；不重试 E2，不触发相机、Ray 或非零输出。

**执行纲要：**

1. 在唯一 fresh external root 构建 C2-style progressive evidence owner；冻结 C2、E2-R1、lineage、HEAD、
   production owner 和 secret-input hash。
2. 先执行 final control flow 的 no-device matrix `14/14`；fake network/secret/device call 为零。
3. 只有 matrix 全过才运行一次 real wrapper，按 frozen order 各尝试一次：primary zero、Python-finally zero、
   child-final zero、shell-trap zero、independent-final zero。
4. 每个 attempt 必须先落盘，result 绑定 attempt hash；timeout/signal 后不得把 unknown 写成未调用或成功。
5. 独立 terminal replay 验证 exact identity、state object、全零、generation 全局严格增加、退出优先级、
   progressive counts、strict JSON、redaction 和 source/frozen drift。

**通过：** 五个 stage 全部 returned-success、generation-bearing zero、所有 terminal mismatch 为空。通过只证明
当前 reachability 与 final zero，不恢复 E2/formal authorization。

**失败：** 任一 resolve/connect/identity/state/generation/cleanup/seal failure 即 hard-fail；剩余 assigned cleanup
仍按 plan 执行，禁止第二次 Z0、IP fallback、网络配置修改、firmware、capture 或 E2。

**停止点：** 无论 pass/fail，写 `EXECUTION_RESULT.md` 后立即停在 Planner。

### REF-P7-02：Z0 Planner 验收与恢复分支

**状态：** `NEXT_REVIEW`

**目标：** 独立重放 Z0 evidence，先归档当前 PLAN，再决定唯一下一包。

**验收步骤：**

1. 验证 external root freshness、source manifest、14-case self-check、五 stage immutable attempts/results、terminal
   inventory、actual count、identity/generation/zero evidence、cleanup、预算和 source/workspace drift。
2. 验证 Z0 没有 camera、Ray、非零 strip、standalone hostname probe、`.env`、firmware 或 network-config side effect。
3. 将 review 方法、artifact paths/hashes、mismatch、决定和 residual risk 写入新 archive。
4. 更新本文件状态，再写仅含一个下一动作的 active PLAN。

**分支：**

- Z0 pass：只可考虑 `REF-P7-03` 的一次 fresh E2；不得把 Z0 解释为 lineage/formal ready。
- hostname/connect 仍失败：请求 Human 检查 fixture power、Wi-Fi 和本机 local-network/mDNS 环境；这不是危险
  操作授权。不得自行换 hostname/IP、重启网络服务或刷 firmware。
- evidence owner/runner defect：写一个纯离线 corrective package，修复后仍须 Planner 决定是否有新的 real gate。
- identity/state/generation drift：停止，先调查设备身份/firmware provenance；任何 firmware 变更需 Human 授权。

### REF-P7-03：fresh E2 readiness/final-zero gate

**状态：** `BLOCKED`

**进入条件：** Z0 由 Planner 接受；新的 active PLAN 冻结 exact checkpoint、lineage release、root、owners、调用
预算和一次性语义。

**目标：** 在 formal 前证明代码、release、设备、相机 remote capability、Ray/strip final-zero 和进程 ownership
均满足运行条件。E2 本身不得 capture 或发出非零灯光。

**计划：**

1. 使用外置 child/root owner，显式传入 repository root；禁止依赖 child cwd 推导 Git root。
2. 重放 exact lineage release、resolved plan、checkpoint、changed-path classification 和 frozen input hashes。
3. 证明无无法识别 ownership 的 camera/calibration/thermal/wrapper process；不杀死无法证明属于本任务的进程。
4. 执行 strip generation-bearing zero、Ray intensity zero、Python/shell cleanup 和独立 final-zero。
5. 只做 bounded remote camera health/config/v2 capability/RAW/ISO/aperture 检查，不 capture。
6. progressive 落盘每一 stage 的 attempt/result；attempted-call accounting 必须区分
   `returned_success|returned_failure|attempted_result_unknown`。
7. seal 后由独立 auditor 重放；任一漂移或 cleanup uncertainty fail closed。

**通过：** 只写 `e2_pass_waiting_for_planner`，不自动进入 formal，除非同一份 active PLAN 已明确把“E2 通过后
条件进入 `REF-P7-04`”定义为一个连续 bounded package。

**失败：** 保留 evidence、执行剩余 cleanup/final-zero，禁止同包 retry、capture 或 formal。

**授权：** release、read-only checks、zero/off 和 cleanup 不需要 Human 授权；firmware/deployment/network config
仍禁止且需要另行 Human 授权。

### REF-P7-04：fresh Ray/strip TD-B formal 与 paired finalizer

**状态：** `LOCKED`

**进入条件：** exact E2 通过；lineage release 对当前 clean checkpoint production-usable；新 run paths 不存在；
Planner active PLAN 冻结一次连续包。若 implementation checkpoint 再变，只能先离线生成和验收新的 lineage release；
release 本身不授权 formal。

**科学合同：**

- `A=H120/S100`、`D=H120/S50`、`B=H0/S0`、`C=H300/S100`；Ray 使用 HSI command，strip 使用
  retained P7-R1 command。
- 每 source 恰好 16 formal、0 ambient：`A0@600`；D/B/C 各 `60/120/300/600`；每组后 A return `@600`。
- `600` 是 Human 选择的 operational dwell，不是 settled；D/B/C chronology 必须保留未稳定 warning。
- TD-B formal 独占 `unsubtracted_no_ambient` 和冻结的
  `statistics.normalized_per_second.trimmed_mean`；其他 caller 不得改变 ambient-subtracted default，也不得 fallback。

**执行顺序：**

1. fresh Ray run：16 个新 CR3/sidecar；不得复用旧失败 capture、不得新 auto-exposure/setup、不得 ambient。
2. Ray public analyzer 独立重放 physical-return/accepted ledgers、CR3/sidecar、recorded exposure、Tier A/B、
   58-feature statistic、source isolation、commands、budgets 和 cleanup。
3. 只有 Ray 结构有效且 active PLAN 明确条件续跑时，fresh strip run 才执行同样 16 formal；否则停止。
4. strip public analyzer 通过后，paired finalizer 只汇总两源结果和 history，不 refit、不改 status、不称 600 settled。
5. Python/shell cleanup、independent both-zero、wrapper/process audit 全部必须留证。

**hard failure：** 任何 quality、exposure、sidecar、timing、ledger、budget、analysis、source isolation、cleanup 或
final-zero failure 都保留所有 physical returns 后立即停止；不得自动重拍、删低信号 feature、放宽 threshold、运行
public analyzer 以外的补偿路径或启动另一 source。

**结果：** 只交回 `REF-P7-05` Planner review；绝不自动进入 TD-C/sentinel。

### REF-P7-05：TD-B 科学验收与 operating-envelope freeze

**状态：** `BLOCKED`

**目标：** 决定 600-second operational protocol 的 return-to-A history compatibility，同时保持科学 settle 字段和
产品 operational 字段分离。

**验收：**

1. 独立重放 A0、A_after_D/B/C、D/B/C chronology、两源 status、pair summary、physical/accepted counts、
   all-off 和 source isolation。
2. 只允许输出已冻结的分支：
   `td_b_operational_600_complete_waiting_for_planner` 或
   `history_dependent_at_operational_dwell_600`，以及结构/测量 hard-failure。
3. 即使 history compatible，也保持 `dwell_is_scientifically_settled=false`、
   `t_formal_provisional_s=null`、`t_formal_s=null`；只可冻结
   `developer_selected_operational_dwell_s=600` 和明确的 previous-state compatibility scope。
4. 更新 operating-envelope/reference artifacts 时版本化，不改 v1 legacy evidence，不扩大 covariance 或 threshold。

**分支：**

- history compatible：进入 `REF-P7-07`，解决 TD-C prerequisite 的 GUIDE/Human-override 语义。
- return anchors split：stage blocked，提交 Advisor 的 history-model decision；不得进入 TD-C/P7 solver。
- single state/load failure：若精确满足 GUIDE 的 full-scale H0 条件，可考虑 `REF-P7-06`；否则停止并分类原因。
- evidence/code defect：只允许新的 bounded offline correction；是否重新采集由后续 Planner 决定。

### REF-P7-06：H0 full-scale vs 3072 thermal diagnostic

**状态：** `CONDITIONAL`

**触发条件：** TD-B 只有 full-scale H0/S0 显示 load-specific unresolved，其他 state/history 足以解释且稳定；不得
把普通 measurement/solver failure 转写为此分支。

**计划：** 单独 PLAN 比较 frozen full-scale neutral 与 max-code `3072` 的 settling/history；相同 observer、时间轴、
source isolation、双 cleanup 和证据 owner。必要时 `2048` 只能在 Advisor/Planner 明确扩展后使用。

**语义：** 只判断 load/scale thermal effect，不是 P8 INT，不生成 gamut 或物理不可达结论，不改 Ray INT。

**授权：** bounded light operation 本身不需要另行 Human 授权；任何 firmware、deployment、破坏性变更仍需要。

**停止点：** 结果交回 Planner/Advisor；不能从 diagnostic 自动回到 TD-C。

## 6. Thermal/reference completion

### REF-P7-07：600-second override 下的 TD-C prerequisite 决定

**状态：** `ADVISOR_DECISION`

**原因：** 第三轮 GUIDE 原要求 TD-B 冻结由更晚点验证的 `t_formal<=300` 后才能运行 TD-C；后来的 Human 决定
拒绝延长并只选择 600-second operational dwell，同时明确不能把 600 写成 `t_formal`。Planner 不得静默把两个字段
合并。

**决策包：**

1. 提交 TD-A、TD-B chronology/history、600 override provenance、operating-envelope v1/v2 hashes 和 residual warning。
2. 要求 Advisor 明确选择：
   - 批准 TD-C 使用 versioned `operational_dwell_s=600`，同时保持 settle status false/null；
   - 修改 TD-C comparison design；
   - 因 history/nonstationarity 阻塞 source comparison。
3. 任何批准都必须冻结 TD-C exact dwell field、previous-state contract、cold proxy、ambient policy、session cap 和
   analyzer interpretation；不得恢复 900/1200 扩展。

**停止点：** Advisor 决定被 Planner 写入新的 active PLAN 前，不运行 TD-C。

### REF-P7-08：TD-C order-balanced core

**状态：** `LOCKED`

**进入条件：** `REF-P7-07` 明确解决 dwell 语义；TD-B history compatible；current Ray/strip state 可重复；
exact checkpoint、plans、inputs、budgets 和 new run roots 由 active PLAN 冻结。

**目标：** 在 `H120/S100` 比较 current Ray 与 strip，不宣称 classic ABBA 消除了线性 drift。

**四个独立 session：**

```text
S1 Ray -> strip
S2 strip -> Ray
S3 Ray -> strip
S4 strip -> Ray
```

每 session 两源先达到 frozen cold proxy，拍 start ambient，按顺序分别 command、等待 frozen operational/formal
dwell、capture、off，再拍 end ambient并双 cleanup/readback。Core 为 8 formal + 8 ambient，physical cap 16。

**core gate：** 四个 within-session `strip-Ray` difference 兼容；Ray-first/strip-first order effect 在 frozen envelope；
Ray current stable center 可算且对 P6 可解释；ambient/black-level/geometry 不解释 source difference；command/source
isolation、exposure、timing、physical/accepted ledger、双 cleanup 全过。

**失败：** 任一 gate false 即 `td_c_gate_failed`，不得写 Planner-waiting pass、不得 endpoint expansion。

**停止点：** core 无论 pass/fail 都先回 Planner；不能连续进入 endpoints。

### REF-P7-09：TD-C endpoint expansion

**状态：** `LOCKED`

**进入条件：** core 被 Planner 接受，且 endpoint comparison 对 reference classification 仍必要。

**计划：**

- `H0/S0`：one Ray->strip session + one strip->Ray session；
- `H300/S100`：one Ray->strip session + one strip->Ray session；
- 每 session 保留 start/end ambient、source isolation、frozen dwell、双 cleanup。

新增 8 formal + 8 ambient，physical cap 16；TD-C core+expansion formal max 16。仍只声明 order-balanced paired
comparison，不声称经典 ABBA drift elimination。

**停止点：** 结果回 Planner，进入 reference classification。

### REF-P7-10：reference epoch 分类与 P6 compatibility

**状态：** `BLOCKED`

**输入：** TD-C core、必要 endpoints、TD-A/B chronology、P6 frozen centers、operating-envelope 和 ambient/order-effect
evidence。

**产物：** versioned `reference-epoch-analysis-v2.json` 与更新后的 operating-envelope/thermal summary；必须包含
stationarity、raw compatibility、interpretable compatibility、shift class、order effect 和 envelope ID。

**唯一分类：**

- `none`：current Ray 与 P6 兼容，保留 P6 numerical centers；
- `common`：请求 `REF-P7-11` 7-point requalification；
- `state_dependent`：请求 7-point 后再决定 13-node；
- `operating_envelope_mismatch`：版本化 steady/operational envelope，不能称 calendar epoch shift；
- `not_identifiable`：stage blocked。

任何分支都不能自动移动 P6、回退 affine/HSL、合并 HSI/RGB endpoints、给 SAT0 定义 Hue 或重拍 106 点。

### REF-P7-11：7-point / 13-node Ray requalification

**状态：** `CONDITIONAL`

**进入条件：** reference class 为 `common` 或 `state_dependent`，且 Advisor 给出 exact target set、envelope、budget 和
decision criteria。

**计划边界：** 7 点先判断共同 shift 与局部 topology；只有 state-dependent/curvature 证据达到 Advisor 门槛才扩到
13 nodes。不得用同一 requalification data 同时 refit 并宣告通过；新 manifold 需版本化并有独立 holdout。

**停止点：** 7 点、13 点各自独立回 Advisor；完整 106 点只可能进入 `REF-P6-FULL-01`。

### REF-P7-12：thermal/reference AUDIT PACK 与 sentinel 解锁

**状态：** `ADVISOR_DECISION`

**进入条件：** reference class 可解释；required requalification（若有）已独立接受；所有 cleanup/readback 为零。

**AUDIT PACK 至少包含：** TD-A/B/C methods、actual budgets、all source artifacts/hashes、operating envelope、chronology/
history/order effect、reference classification、legacy regression、full tests/compileall/wrapper/diff/CodeGraph、failed runs、
residual risk 和 sentinel exact proposal。

**Advisor 允许出口：** explicit sentinel release、targeted thermal/reference correction、restricted envelope、stage blocked 或
stop route。即使所有自动 gate 通过，没有 Advisor explicit release 也不能进入 sentinel。

## 7. P7 INT100 candidate and gamut

### REF-P7-13：四点 sentinel v2

**状态：** `LOCKED`

**进入条件：** Advisor explicit release；operating-envelope hash、reference artifact、formal-eligible policy、uncertainty、
observer、location、manifold、code checkpoint和 exact target file 全冻结。不得沿用旧 v1 60-second settled 语义；
confirmation dwell 必须来自新批准 envelope。

**顺序：**

1. `H0/S0`：SAT0 pooled zero、Hue undefined、white participation、full-scale 和 measurement quality；
2. `H120/S100`：高饱和控制点，必须 `faithful=true`；
3. `H120/S50`：中间 SAT、WW/CW、二维路径和 inverse；
4. `H300/S100`：高曲率压力点。

**reference anchors：** run 前 Ray `H0/S0`、`H120/S100`、`H300/S100`，run 后 Ray `H120/S100`；使用 current
approved envelope，只做 health check，不进入 strip optimization samples。任一 anchor drift 立即停止，不同 run 重拟合 P6。

**每点合同：** frozen two-face solver、full-scale max-code 4095、普通三次独立 confirmation、scope-aware faithful fields、
physical/logical budget、weak reacquire `<=1.25x`、command/source-isolation audit、Python/shell cleanup。旧 ordinary cap
`54 logical / 67 physical` 只能在新 PLAN 对当前 policy/hash 重放后采用。

**放行：** 四点均结构合法；H120/S100 faithful；H120/S50 至少是稳定 valid candidate；H300/S100 即使 non-faithful
也必须有 best-valid、冻结 failure class 和稳定局部搜索；无 unexplained prediction reversal、budget drift、reference drift、
cleanup/source failure。

**失败分支：** measurement_unreachable、uncertainty_unresolved、solver coordinate/budget、reference drift、纯 code/audit
defect分别保留原证据并停 Planner。任何 retry 都需新 PLAN/new root；不得因为早期 GUIDE 曾允许一次 code retry 就自动执行。

### REF-P7-14：remaining 9 INT100 pilot points

**状态：** `LOCKED`

**进入条件：** sentinel 被 Planner 接受，combined analyzer 输入/policy/hash完全一致，active PLAN 冻结 exact target file。

**exact targets：**

```text
H0/S50, H0/S100,
H60/S50, H60/S100,
H180/S50, H180/S100,
H240/S50, H240/S100,
H300/S50
```

**计划：** 使用与 sentinel 相同的 approved envelope、reference anchors、solver、confirmation、full-scale、uncertainty、
source isolation、budgets 和 cleanup。不得把 sentinel/remaining 的不同 policy、hash 或 reference epoch 合并。

**完成门：** 13-point INT100 pilot 全部有可重放状态；六个主 Hue 至少有 faithful 区间或明确 unresolved reason；
任何 measurement/solver failure 不得标为 gamut/physical unreachable。

### REF-P7-15：full-scale boundary 与 scale-relaxed diagnostics

**状态：** `LOCKED`

**进入条件：** 13-point pilot 被 Planner 接受并识别需要搜索的 Hue/SAT 区域。

**每个 `s_exact_max_int100_fullscale(h)` 的最小证明：**

1. 同 Hue 至少一个 faithful SAT 下界；
2. 一个合法、重复稳定、非 measurement/solver failure 的 non-faithful SAT 上界；SAT100 faithful 可直接记 100；
3. bracket 内定向加密/二分，首轮 width `<=5 SAT`，Gate-6 freeze `<=2 SAT`；
4. 两端各五次独立 approved-envelope confirmation；
5. 保存 active set、full-scale channel、white fraction、sensitivity、inverse condition、Hue identifiability 和 failure cause；
6. active-set 切换附近额外采点，不用 spline 抹掉不连续。

**scale-relaxed diagnostic：** 对拟写为边界的 non-faithful 上界，至少用 max-code `3072` 做一次真实闭环；必要时
`2048`。它不改变 Ray INT100，也不是 P8 data。较低 scale 通过只能说明
`full_scale_operating_boundary`；较低 scale 仍失败也只能增强经验不可达证据，不能证明物理 gamut。

**自适应加点：** 只在 Hue curvature、active-set change、boundary jump、error peak 或 0/360 discontinuity 有证据时增加；
每次新批次由 PLAN 冻结 hard cap，禁止无界采样。

### REF-P7-16：P7 independent holdout 与 runtime gamut semantics

**状态：** `LOCKED`

**进入条件：** candidate/boundary model 已冻结，不再用 holdout 调阈值或同 run refit-and-pass。

**最低矩阵：**

- 0/360 periodic holdout；
- 至少 6 个未训练 non-node Hue/SAT，按六个 60-degree Hue sector 分层；
- 高曲率区至少 1 个 non-node holdout；
- 每个关键 boundary 两侧与 active-set transition；
- reference anchor、uncertainty、candidate、interpolation、code checkpoint全链可追溯；
- boundary/holdout 点五次 independent confirmation。

**runtime semantics：** 冻结 `faithful`、`unconfirmed`、`measurement_unreachable`、
`uncertainty_unresolved`、`solver_budget_exhausted`、`boundary_bracketed_at_full_scale`、
`gamut_compressed_int100_fullscale` 和 `empirically_unreachable_under_frozen_contract` 的 scope；不得输出无 scope 的
`s_exact_max(h)` 或“物理不可达”。验证 interpolation 的 0..4095、periodicity、gamut status 和 active-set 行为。

**失败：** 不进入 P8；根据 failure type 回到 targeted P7 correction 或缩小 product range，不能用 holdout 扩大 tolerance。

### REF-P7-17：P8 entry review

**状态：** `ADVISOR_DECISION`

**必须证明：** 13 points complete；六 Hue faithful/unresolved status；required boundaries complete；0/360、六 sector 和
high-curvature holdouts通过；full-scale/scale-relaxed 语义分离；runtime gamut fields冻结；candidate有独立 confirmation；
reference/uncertainty全程可追溯。

**Advisor 出口：** unlock P8 with exact product/intensity scope、targeted P7 repeat、restrict range 或 stop HSI route。
Planner/Executer 不得自行进入 P8 或命令 Ray INT50/20/5。

## 8. P8 intensity dimension

### REF-P8-01：INT acquisition、model branch 与 independent holdout

**状态：** `LOCKED`

**进入条件：** Advisor 在 `REF-P7-17` 明确放行；P7 INT100 candidate、gamut semantics、operating envelope、reference
and uncertainty artifacts frozen；active PLAN 冻结 target matrix/caps。

**采样：** INT `100,50,20,5`，覆盖 SAT0、R/G/B/C/M/Y、SAT50、最难 Hue boundary、white-heavy、RGB-only 和
低强度量化/PWM风险。默认只复制 Ray 相对强度曲线，允许 Ray100 与 strip100 有全局比例；绝对照度不在本任务。

**分析：** 检查 normalized target 是否可表示为
`t(h,s,I) ~= alpha(I,h,s) * t(h,s,100)`，并选择且只选择一个最小分支：

- I-A separable：INT100 color LUT + one-dimensional Ray relative intensity curve + per-channel code-duty inverse；
- I-B low-int color shift：增加 sparse `1,5,10,25,50,100` per-channel corrections；
- I-C broad coupling：sparse local correction/adaptive nodes；若规模不可控，限制产品为 INT100 或有限 INT range。

**holdout：** 模型/节点冻结后另做未用于选择的 Hue/SAT/INT、boundary、low-INT 和跨日 holdout；任何 candidate change
使旧 holdout 不再是完整证据。禁止直接扩成均匀 dense 3D LUT 或隐瞒 unsupported range。

**停止点：** 完成或任何规模/semantics/failure branch 后回 Gate-6，不安装 runtime candidate。

## 9. Gate-6、P9 与交付

### REF-G6-01：Gate-6 final candidate/product freeze

**状态：** `ADVISOR_DECISION`

**输入：** P7/P8 candidate hashes、training/holdout、gamut boundary、INT branch、supported range、failure ledger、
operating/reference/uncertainty provenance、safety/cleanup audits和 P9 proposal。

**冻结内容：** public faithful/gamut semantics、scoped boundary representation、I-A/B/C branch、supported INT/Hue/SAT
range、最终 HSI candidate hash、是否包含现有 CCT candidate、P9 immutable validation matrix和 acceptance thresholds。

**出口：** `freeze_candidates_for_stage_7`、`repeat_targeted_stage_6`、`restrict_product_range` 或 `stop_hsi_route`。
数据量不可控时缩小承诺，不能批准无界加点。

### REF-P9-01：immutable final independent validation

**状态：** `LOCKED`

**进入条件：** Gate-6 已冻结 candidate、产品范围、thresholds、matrix、checkpoint 和 all input hashes；validation run
内禁止优化。

**HSI 最低验证：** coarse nodes、至少 50 个按 Hue 分层且未用于拟合的随机 points、0/360、SAT0/2/5、SAT90/95/100、
每个 boundary 两侧、worst Hue、multiple INT、same-day/cross-day、training/holdout materials、fixed anchors。

**CCT 条件矩阵：** 只有 Gate-6 明确把 retained white-only candidate 纳入交付，或 `REF-CCT-01` 先被重开并完成时，才执行
Guide 的 70 nodes、至少20 non-node、extreme CCT、GM collapse、active-set boundary、same/cross-day 和 material holdout；
不能把 P4 diagnostic-only evidence冒充完整 CCT candidate validation。

**报告：** P50/P90/P95/max、repeatability/confidence、training vs holdout、same vs cross-day、所有 failed points；HSI
报告 Hue/SAT/e-perp/rendering/gamut/white fraction/INT drift，CCT（若在 scope）报告 RAW/Duv/CCT-mired/multipatch/
RGB-white contribution。

**失效条件：** candidate/hash变化、验证中调参、缺少跨日/失败点、source isolation或最终双关灯不完整。节点通过但
interpolation失败、same-day pass/cross-day fail、partial gamut等必须按 Guide 分支报告，不能现场修复后继续算同一 validation。

### REF-G7-01：Gate-7 technical delivery decision

**状态：** `ADVISOR_DECISION`

**输入：** immutable P9 report、all failures、candidate/plan hashes、rollback proposal、安全与关灯证据。

**技术出口：** `install_all`、`deliver_cct_only`、`deliver_hsi_with_explicit_gamut`、
`hold_external_candidates`、`repeat_validation`、`rollback` 或 `stop_route`。Advisor 给技术建议，不替代 Human 的最终
产品/安装决定。

### REF-OPS-01：install、smoke test、rollback 与交付

**状态：** `HUMAN_DECISION`

**进入条件：** Gate-7 出口明确；Human 明确批准 exact candidate/config target、安装范围和是否 commit。该批准与
firmware upload 分离；如方案需要 firmware/remote deployment，必须另有危险操作授权。

**计划：** 备份默认配置并记录 hash；原子安装已冻结 candidate；执行代表 CCT/HSI/INT/gamut-status commands；核对
runtime output和版本；双 cleanup/final-zero；验证 rollback 命令能恢复旧 hash。CCT/HSI 可独立交付，不能因一方失败
捆绑安装。

**失败：** 立即 rollback、双灯关闭、保留 evidence；不在 installed candidate 上现场继续优化。

### REF-CLOSE-01：final stage AUDIT PACK 与路线关闭

**状态：** `BLOCKED`

**计划：** 汇总全部 GUIDE/decision provenance、active/review archives、最终 candidate/config hashes、P9/Gate-7、
installation/hold/rollback result、known limitations、product scope、reproduction and rollback instructions、tests、安全和
未完成 deferred branches。Advisor 审阅后由 Human 决定关闭、维持实验状态或开启新 GUIDE。

## 10. 当前不执行的条件/延后分支

### REF-CCT-01：完整 CCT/GM P5 候选

**状态：** `DEFERRED`

第一轮 GUIDE 原计划完整 70-node CCT/GM global fit，但后来 Gate-3 已明确
`keep_white_lut_diagnostic_only; stop_before_p5`。因此它不是当前 HSI 路线的漏项，也不能由“尚未完成”自动恢复。

只有新 Advisor/Human 决定重开时，Planner 才能基于 P4 的 measurement_unreachable/neutral-gate 失败重新定义 observer、
target grid、solver、holdout和安装语义。重开后必须形成独立计划、独立 candidate和完整 P9 CCT validation；不得覆盖当前
default LUT 或把旧 external 70-point candidate 宣称为新 P5 结果。

### REF-ABBA-01：classic ABBA mini-run

**状态：** `DEFERRED`

当前只批准 order-balanced cross-session comparison。只有额外证据证明 observations 位于短、规则、共同线性 drift 窗，
Advisor 才能批准 classic ABBA mini-run；不得从 TD-C order balance 宣称线性 drift 已数学消除。

### REF-P6-FULL-01：完整 P6 106-point re-capture

**状态：** `DEFERRED`

只有 7/13-point requalification 证明二维 topology/curvature 已变化且 Advisor 明确批准时才考虑。任何 current reference
shift 都不能自动触发 full recapture。

### REF-LUX-01：绝对照度/绝对亮度复制

**状态：** `DEFERRED`

当前 INT 目标是 Ray relative intensity，允许 global scale。若产品改为绝对照度匹配，需要新 metrology GUIDE，冻结
照度计/几何/距离/环境/单位/uncertainty和安全预算；不得从 camera RGB 或曝光归一化 feature 推断绝对亮度。

## 11. 全局不可变 guardrails

- 不自动重跑 P7-R1、Z0、E2、TD-B、TD-C、sentinel、remaining、boundary、holdout、P8 或 P9；每次 real retry 都需
  新 active PLAN 和 new run root。
- 不修改 identity RAW、R/G1/G2/B、58-feature、`1.0x..1.25x` exposure envelope、joint coverage、trend `4.0`、
  dominance `0.5`、frozen uncertainty 或 P6 manifold，除非 Advisor 新 GUIDE 明确改动。
- 不把 600 秒称 steady/settled，不把 cold and steady centers/covariance 合并，不用 thermal covariates inflate tolerance，
  不 same-run fit-and-pass。
- Ray 与 strip 永不同时点亮；每个可留灯脚本必须有 Python cleanup、shell cleanup、independent final-zero 和 source
  isolation/readback evidence。
- release、offline replay、read-only checks、bounded light on/off/zero 和 cleanup 不需要单独 Human 授权；firmware upload/
  flash、remote deployment、destructive hardware change、network/device operation outside active PLAN bounds必须 Human 授权。
- 不把 `unconfirmed`、measurement/solver/uncertainty failure 写成 gamut 或物理不可达；full-scale boundary、scale-relaxed
  diagnostic和 P8 INT data必须分离。
- 不覆盖 default LUT、安装 runtime candidate或开展危险固件/部署操作，除非相应最终 Human decision 已写入 active PLAN。
- 不使用本文件替代 exact artifact hashes、budgets、commands、timeouts、run directories和 stop rules；这些必须在每个 active
  PLAN 中重新冻结。
