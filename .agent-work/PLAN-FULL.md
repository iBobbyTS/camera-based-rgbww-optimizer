# GUIDE 4 科研执行平台去工程化与完整科学路线

**Document status:** `GUIDE4_DEENGINEERING_PROGRAM_PENDING_GIT_PROTECTION`

**Roadmap authority:** `false`。本文件只描述当前 GUIDE 阶段的总路线；只有
Planner 写入 `.agent-work/PLAN.md` 的单一 active package 才能执行。

**Roadmap ownership:** 本次版本由 Supervisor 根据 Human 的明确指令重写；后续语义
状态更新仍交回 `sol_max`，Executer 不得编辑本文件。

**Active task count:** `0`

**Current milestone:** `G4-DEENG-00-GIT-PROTECTION`

**Next package (not active):** `REF-G4-DEENG-00-PRESERVE-MERGE-BACKUP-BRANCH`

**Current science delta:** `none`

**Scientific completion target:** 高效、可复现地执行完 Advisor GUIDE 4 的剩余路线：
Ray R6 acquisition/analysis、条件 strip TD-B、combined TD-B operational-600 gate、
条件 TD-C core，以及对应 scientific terminal/AUDIT PACK；不要求所有路线必须 pass，
GUIDE 定义的可复现 scientific negative result 也是合法出口。

`PLAN_FULL_MACHINE_CONTRACT={"schema":"guide4_science_completion_plan_full_v6","document_status":"GUIDE4_DEENGINEERING_PROGRAM_PENDING_GIT_PROTECTION","executable":false,"roadmap_context_only":true,"active_task_count":0,"active_task":null,"current_milestone":"G4-DEENG-00-GIT-PROTECTION","next_package":"REF-G4-DEENG-00-PRESERVE-MERGE-BACKUP-BRANCH","allowed_next_action":"PLANNER_WRITE_GIT_PROTECTION_PACKAGE","scientific_target":"COMPLETE_GUIDE4_WITH_REPRODUCIBLE_RAY_STRIP_COMBINED_AND_CONDITIONAL_TD_C_EVIDENCE","next_scientific_action":"RAY_R6_AFTER_DEENGINEERING_READINESS","science_delta":"none","human_directed_deengineering_program":true,"engineering_program":{"git_protection_package":1,"implementation_packages_max":3,"micro_plan_split_allowed":false,"generic_review_loop_required":false,"final_independent_architecture_review":true},"git_topology":{"source_branch":"codex/g4-r6-owner-alignment-large-change","source_head_at_design":"463a151bede3013db14d31802ea93fafa2322bf6","main_head_at_design":"3c920c6d29e5c366ce3843a2532d30d80c6f0c33","main_is_ancestor_of_source":true,"source_ahead_of_main":33,"merge_mode":"fast_forward_only_after_dirty_tree_commit","backup_branch":"codex/backup-guide4-pre-deengineering-20260806","backup_remote":"origin","backup_push_authorized":true,"main_push_authorized":false,"refactor_branch":"codex/guide4-science-first-deengineering"},"runtime_target":{"production_reads_agent_work":false,"production_reads_git_topology":false,"production_requires_stage_gate_package":false,"production_requires_authority_mirror":false,"plan_is_external_execution_authority":true,"scientific_and_safety_validation_retained":true,"reproducibility_evidence_retained":true},"frozen_science":{"guide_sha256":"659152f6c0ae69c90c701de4e57c352d771e4f0bf75cf9410271ba0a94200e35","research_sha256":"aa556cb8d8bf306921f3e4fd33ccae9646e78863ccd732e8529b98da6aad61d4","eq_r6":"qualified_1_2500","exposure_policy_sha256":"c9080d18571f617cb7d323ade843ff9c86bf92e3795d23e3999e26d413968681","r5_frames":"diagnostic_only_no_pooling","successor_release":"accepted_frozen_unconsumed"},"locks":{"device":true,"formal":true,"camera":true,"ray":true,"strip":true,"capture":true,"analysis":true,"td_c":true},"human_goal_complete":false,"guide_complete":false}`

## 1. Human 指令与一次性例外

本路线不是只为下一次 Ray R6 做局部补丁，而是一次覆盖 GUIDE 4 剩余阶段的科研执行
平台整治。Human 明确允许投入更多工程时间，条件是：

1. 现有科学成果、原始证据、输入 hash 与复现能力不得损失；
2. 当前分支先安全进入本地 `main`；
3. 合并后的完整状态必须有一个专用 backup branch 推送到 `origin`；
4. 所有去工程化工作只在新的 refactor branch 上进行；
5. 整治必须服务于完成整个 GUIDE 4，而不是生成新的通用框架；
6. 完成整治后，科学动作不得再被 Git、PLAN parser、package lineage 或历史治理状态阻塞。

因此，本计划一次性覆盖通常“科学动作前最多两个 engineering-only PLAN”的默认预算，
允许在 Git 保护包之后最多三个大颗粒 implementation PLAN。该例外不允许微任务、每个
文件一份 PLAN、重复 clean-room、每次修正一轮 review 或无限重构。

## 2. 当前可保护基线

### 2.1 Git 与工作树

- 当前分支：`codex/g4-r6-owner-alignment-large-change`。
- 设计时 HEAD：`463a151bede3013db14d31802ea93fafa2322bf6`。
- 本地 `main`：`3c920c6d29e5c366ce3843a2532d30d80c6f0c33`。
- `main` 是当前分支祖先；设计时 ahead/behind 为 `33/0`，因此预期可 fast-forward。
- 当前工作树包含 accepted runtime-consumer source/test、PLAN/PLAN-FULL、
  EXECUTION_RESULT 与 terminal archives，必须先分类、验证并提交，不能丢弃或 reset。
- `origin/main` 设计时为 `4e8d9c7330a0c2be6bb9f9dd912ec2b39348fbcd`；本计划不授权 push `main`。

### 2.2 冻结科学事实

- GUIDE SHA-256：`659152f6c0ae69c90c701de4e57c352d771e4f0bf75cf9410271ba0a94200e35`。
- RESEARCH SHA-256：`aa556cb8d8bf306921f3e4fd33ccae9646e78863ccd732e8529b98da6aad61d4`。
- EQ-R6：`qualified_1_2500`；policy SHA-256：
  `c9080d18571f617cb7d323ade843ff9c86bf92e3795d23e3999e26d413968681`。
- R5 的11帧永久为 diagnostic-only，禁止与新 R6 或 strip formal frame pooling。
- successor release 根保持 immutable：
  `/Volumes/4T/temp/rgbww-optimizer/g4-successor-lineage-779c7d9572d9-20260803T172055Z/release`。
- successor release 五文件及现有 hashes、accepted predevice、zero-readiness、fresh E2
  都是可复现基线；整治可以改变执行 plumbing，不得改写这些科学输入。
- 当前 capture/quality/chronology/history/scientific-negative 均为0；76项工程测试通过
  不是科学进度。

### 2.3 历史边界

- 所有 `historical-*`、rejected candidate、旧 stage-gate root 和旧 release 只作证据，
  禁止作为新实现输入。
- backup branch 是完整回退点；refactor branch 可以删除 active tree 中的治理噪音，
  但不能改写 Git 历史或删除远端 backup。
- `GUIDE.md` 与 `RESEARCH.md` 保持 immutable。

## 3. 重构后的最小科研架构

### 3.1 Production 不再消费治理状态

完成整治后，`src/`、正式 CLI、采集 runner 和 analyzer 都不得读取或解析：

- `.agent-work/PLAN.md`、`.agent-work/PLAN-FULL.md` 或任何 archive/debug/review；
- `FULL_PLAN_REFERENCE.md` 或任何 machine-row marker；
- Git parent/tree、commit subject、allowed changed paths 或 branch topology；
- replacement-package task ID、authority mirror、release-consumption ledger；
- `launch-descriptor.json` / `stage-gate.json` 作为启动前置。

PLAN 仍是 agent 的外部执行授权和边界记录，但 production Python 不从 Markdown 推导
权限。Git commit 仍记录到实验输出，作用是复现与审计，不是启动门槛。

### 3.2 唯一科研运行模型

剩余 GUIDE 4 只保留一个小型、sequence-driven experiment runner；它复用已有设备、
相机、RAW measurement、quality、analysis 与 cleanup owner，不复制算法。它必须能表达：

- Ray R6 与 strip TD-B 的 A-D-A-B-A-C-A sequence；
- TD-C core 的 order-balanced S1/S2/S3/S4 sequence；
- source-specific command/readback、fixed exposure、dwell 与 previous-state；
- exact capture ID/order、logical/physical cap、launch cap、retry；
- output root uniqueness、abort、cleanup 与 final-zero；
- per-frame quality 和科学分支。

禁止为 Ray、strip、combined、TD-C 各建一套 runner，也禁止抽象成超出 GUIDE 4 所需的
通用 workflow engine。

### 3.3 必须保留的科学与安全 gate

以下不是“过度工程化”，不得删除：

- frozen input/config/analysis schema 与 SHA-256；
- exact source/state/exposure/dwell/previous-state contract；
- remote capture/request identity、CR3/sidecar bytes/SHA、MakerNote actual exposure；
- 58 required features、clipped fraction 0、near-noise/finite/valid-pixel checks；
- source isolation、strip zero、Ray readback、physical/logical accounting；
- fresh root、禁止覆盖/续跑/old-new pooling；
- launch=1、retry=0，以及 GUIDE 各分支的 hard stop；
- Python cleanup、shell cleanup、independent final-zero；
- secret/credential 隔离；
- firmware、remote deployment、destructive operation 与 active PLAN bounds 外设备操作的
  Human authorization。

有界 Ray/RGBWW 灯光开关、相机采集、离线输入消费与 cleanup 在 active PLAN 精确约束
target/intensity/duration/isolation/abort/cleanup 后不需要额外 Human approval。

## 4. 科学可复现性的交付定义

每次正式 acquisition 必须留下足以独立重放分析的最小证据集：

- immutable experiment spec/plan 与 SHA；
- GUIDE/RESEARCH/config/input hashes；
- 运行代码 commit、Python/package/environment 版本（记录，不作 authorization gate）；
- device/camera anonymized identity、状态命令和 readback；
- exact sequence、nominal/actual exposure、monotonic/UTC timing 与 previous-state；
- CR3、sidecar、bytes/SHA、patch-statistics 和 accepted/rejected ledger；
- physical returns、capture accounting、failure/abort 原因；
- Python/shell cleanup 与 final-zero；
- analyzer 版本、输入 manifest、输出 artifact 和 hashes。

优先复用 GUIDE 已要求的 `run.json`、`plan.json`、`captures.jsonl`、`commands.jsonl`、
`physical-returns.jsonl`、measurement reports、returned summary、cleanup 和 audit artifact。
只有现有文件无法记录环境信息时才允许增加一个小型 environment artifact；禁止重新建立
release family、stage-gate package、terminal authority seal 或 provenance framework。

一次离线复现必须能在不读取 `.agent-work`、不连接设备、不访问 Git history 的情况下，
从保存的 spec、raw/sidecar/measurement 与 analyzer 版本重新生成相同科学判定。

## 5. 总里程碑

| Milestone | 状态 | 单一目标 | 解锁 |
| --- | --- | --- | --- |
| `G4-DEENG-00-GIT-PROTECTION` | CURRENT | 收敛当前分支、FF main、远端 backup、新 refactor branch | 安全整治环境 |
| `G4-DEENG-01-REPRODUCIBILITY-SEAM` | BLOCKED | 冻结最小复现合同并用行为测试保护科学/安全 owner | 可安全替换执行层 |
| `G4-DEENG-02-SCIENCE-RUNTIME` | BLOCKED | 建立覆盖 GUIDE 4 剩余 acquisition 的唯一小型 runner | Ray/strip/TD-C 可直接执行 |
| `G4-DEENG-03-DELETE-LEGACY` | BLOCKED | 删除 production 治理耦合、旧 package/attestation 与无科学价值测试 | 干净维护基线 |
| `G4-DEENG-04-SCIENCE-READINESS` | BLOCKED | 真实 frozen inputs no-connect 验证与一次最终 suite | Ray R6 active PLAN |
| `G4-RAY-R6-ACQUISITION` | BLOCKED | 完整新 Ray 16帧 | Ray analyzer 或科学负结果 |
| `G4-RAY-R6-ANALYSIS` | BLOCKED | quality/chronology/A-return history | strip 或 scientific stop |
| `G4-STRIP-TD-B` | BLOCKED | 条件新 strip 16帧及分析 | combined 或 scientific stop |
| `G4-COMBINED-TD-B` | BLOCKED | operational-600 双 source gate | TD-C core 或 blocked result |
| `G4-TD-C-CORE` | BLOCKED | 条件 order-balanced 8 formal | Advisor scientific review |
| `G4-GUIDE4-CLOSE` | BLOCKED | AUDIT PACK 与可复现 terminal disposition | GUIDE 4 complete/Advisor handoff |

## 6. G4-DEENG-00 — Git 保护与分支拓扑

- **scientific_target:** 在不损失任何 accepted/negative evidence 的前提下，建立完整、
  可远端恢复的整治起点。
- **next_scientific_action:** 整治完成后的 Ray R6；本 milestone 不产生 measurement。
- **science_delta:** `none`；它只解除“大规模删除没有远端回退点”的 blocker。
- **单一 package:** Planner 必须把 dirty-tree inventory、当前改动验证、focused commit、
  fast-forward main、backup push 和 refactor branch creation 放入同一个 Git 保护 PLAN，
  不拆成多个 activation/review cycle。
- **顺序合同:** 先在当前分支提交所有已分类改动；确认 `main` 仍是其祖先且无 divergence；
  将当前分支以 fast-forward-only 合入本地 `main`；从合并后的 exact main commit 创建
  `codex/backup-guide4-pre-deengineering-20260806` 并推送到 `origin`；确认远端 ref 与本地
  commit 精确相等；最后从同一 main commit 创建并切换
  `codex/guide4-science-first-deengineering`。
- **remote boundary:** 只授权创建/推送上述 backup branch；不 push `main`，不删除或
  force-update 任何远端 ref，不删除当前源分支和 historical refs。
- **acceptance evidence:** dirty path classification、commit/tree、main FF relation、backup
  local/remote OID、refactor branch base、clean worktree。
- **stop:** 未分类用户改动、非 fast-forward、remote name/URL 漂移、backup OID 不匹配或
  push 被拒绝时停止，不使用 rebase、force push、reset、clean 或覆盖式 checkout。

## 7. G4-DEENG-01 — 可复现科学 seam

- **scientific_target:** 把真正决定科学复现与设备安全的行为从治理代码中识别并冻结，
  使后续删除不会改变 measurand、quality 或 evidence semantics。
- **next_scientific_action:** Ray R6 acquisition。
- **science_delta:** `none`；唯一 blocker 是科学/安全 owner 与治理 owner 当前混在超长
  stage-gate/thermal coordinator 中，不能安全直接删除。
- **PLAN `DEENG-A`:** 使用 CodeGraph 建立 production call/dependency map；以现有真实
  行为补齐少量 characterization tests；定义唯一 experiment spec、最小 reproducibility
  evidence 与 acquisition/analyzer 接口。不得增加新 manifest family 或泛化框架。
- **必须冻结:** Ray/strip sequence、R6 exposure、quality、physical budget、camera v2
  metadata、readback、cleanup、history/chronology semantics、TD-C order balance。
- **acceptance evidence:** 每个保留 owner 有行为测试；一次 saved-evidence offline replay
  不访问 `.agent-work`/设备/Git；删除候选 ledger 将 production-science、science-analysis、
  safety、governance-only 四类明确分开。
- **stop:** 若某项 gate 无法判断是否影响科学结论，保留它并记录精确问题；只有科学语义
  GUIDE/RESEARCH 无法回答时才请求 Advisor，工程归类问题由 Orchestrator解决。

## 8. G4-DEENG-02 — 唯一 GUIDE 4 science runtime

- **scientific_target:** 让整个 GUIDE 4 剩余 acquisition 由一个小型、可测试、无治理依赖
  的 runner 执行，同时复用现有相机、Ray/strip、RAW、quality 与 cleanup owner。
- **next_scientific_action:** Ray R6 acquisition。
- **science_delta:** `none`；它解除当前 production 必须先满足 PLAN/Git/package lineage
  的直接 blocker。
- **PLAN `DEENG-B`:** 从现有超长 coordinator 提取或重写最小 sequence runner；迁移 Ray
  R6、strip TD-B 与 TD-C core spec；将 combined/analyzer 保持为离线科学 owner；提供
  module CLI，不新增 root-level wrapper。
- **runtime contract:** 只接受 immutable scientific inputs、fresh output root、设备适配器
  与运行边界；validate science/safety 后直接进入 backend。记录 Git/environment 但不据此
  拒绝启动；production 不读取 agent docs、archives、Git topology 或 stage-gate package。
- **tests:** exact sequences/caps/exposure、root uniqueness、backend-before-effect rejection、
  injected capture failure cleanup、source isolation、offline analyzer replay；使用 fake/no-connect
  adapter，不扩大为 orchestration matrix。
- **stop:** 不得复制 capture、quality、cleanup 或 analyzer 算法；如果现有 owner 没有可复用
  seam，只做最小提取并保持结果等价，不创建第二套 runner。

## 9. G4-DEENG-03 — 删除过度工程层

- **scientific_target:** 让后续 GUIDE 科学进度不再受历史治理实现和无关测试阻塞。
- **next_scientific_action:** Ray R6 acquisition。
- **science_delta:** `none`；本 milestone 完成后不允许再插入工程 package。
- **PLAN `DEENG-C`:** 在新 runtime tests 已绿的前提下删除或退出 production：
  - `p7_td_b_r6_stage_gate` 的 package/authority/Git-attestation 路线；
  - `agent_work_machine_contract` 的 runtime coupling；若无其他必要使用则删除整个模块；
  - `FULL_PLAN_REFERENCE.md` active copy、machine-row authority mirror、replacement task IDs；
  - launch/stage-gate/terminal authority package builders和production loader；
  - hard-coded commit subject/path/parent/tree gates；
  - 只验证 synthetic governance topology、没有科学/安全行为价值的 tests；
  - active tree 中仅有治理价值的旧 debug/review/archive；backup/history 保留其恢复能力；
  - 不再适用的 wrapper、docs 和 skill 条款。
- **保留/整理:** scientific artifacts、GUIDE/RESEARCH、config、accepted measurement evidence、
  device/camera adapters、quality/analyzers、cleanup、最小 active PLAN/PLAN-FULL workflow。
- **docs:** 更新 `AGENTS.md`、项目 skill、`docs/README.md` 与必要 engineering note，明确
  production 与 agent orchestration 完全分离。
- **acceptance evidence:** `src/` 对 `.agent-work`、machine marker、legacy FULL、stage-gate
  package、Git topology gate 的依赖为0；删除测试与删除行为一一对应；无 parallel owner。
- **stop:** 不因追求行数删除科学/安全 gate；不重写 GUIDE/RESEARCH；不清除 Git history、
  remote backup 或原始实验根。

## 10. G4-DEENG-04 — 全 GUIDE 科研 readiness

- **scientific_target:** 证明新平台能从当前 frozen evidence 直接、安全地进入 GUIDE 科学
  动作，且后续 Ray/strip/TD-C 共用同一执行模型。
- **next_scientific_action:** `P7-TD-B-RAY-OP600-EXPOSURE-GUARDED-FORMAL-R6`。
- **science_delta:** `GUIDE4_SCIENTIFIC_EXECUTION_UNLOCKED`；这是唯一允许在采集前计作科学
  解锁的工程出口，不宣称 measurement。
- **validation:** 使用真实 frozen successor release/inputs 做一次 no-connect dry validation；
  验证 Ray R6、strip TD-B 和 TD-C specs 均可解析；验证 saved-evidence offline replay；运行
  focused tests、compile/static、wrapper syntax、`git diff --check`、CodeGraph sync，并在整治
  最终候选上只运行一次 full suite和一次独立 architecture review。
- **acceptance:** worktree clean、refactor commits focused、legacy critical-path dependency为0、
  frozen artifacts未修改、fake backend effect=0、下一 active PLAN 可只描述科学动作。
- **failure:** 只修复会阻断科学/安全/复现的缺陷；非阻断清理进入 post-GUIDE backlog，
  不得延迟 Ray R6。

## 11. G4-RAY-R6-ACQUISITION — 完整新 Ray 16帧

- **scientific_target:** 在 operational-600 fixed transient 下取得完整、全新、可复现的
  Ray A-D-A-B-A-C-A sequence。
- **next_scientific_action:** 16/16 quality pass 后运行 Ray-only analyzer。
- **science_delta:** 16张新 Ray captures与quality ledger，或第一次 formal hard failure 的
  scientific valid negative evidence。
- **frozen contract:** IDs `000..015` 与 GUIDE 顺序完全一致；A/D/B使用 frozen R5 shutter，
  C使用 `1/2500`；ISO/aperture不变；Ray-only、strip/ambient zero；logical/physical=16，
  launch=1、retry=0；禁止 auto-exposure、weak reacquire、skip、resume、second root和pooling。
- **runtime:** 预计超过10分钟，使用 visible macOS Terminal、三次稀疏 liveness 与 automation
  规则；成功/失败均完成 Python/shell cleanup 与 independent final-zero。
- **acceptance:** GUIDE 7.7 的 run/plan/captures/commands/physical/measurement/exposure/
  summary/cleanup/audit/failure artifacts及hash完整。
- **stop:** 任一capture、source isolation、readback、quality、budget或cleanup failure立即停止；
  不重试，不运行 analyzer/strip，不把工程错误伪装成科学结果。

## 12. G4-RAY-R6-ANALYSIS — chronology 与 return history

- **scientific_target:** 判断600秒 endpoint的quality、D/B/C chronology与四个A-return
  history compatibility，不声称steady。
- **next_scientific_action:** history pass后进入strip；history fail则形成
  `stop_history_model_required`。
- **science_delta:** Ray operational-600 chronology/history result：
  `accepted_for_strip_entry`、`stop_history_model_required`或acquisition scientific failure。
- **required semantics:** 保留 `steady_status=not_demonstrated`、
  `selected_fixed_time_transient_not_proven_steady`；trend>4继续报告但不单独否定endpoint。
- **stop:** 只有16/16 quality pass才分析；A-return任一不兼容即锁strip并准备Advisor evidence，
  不由工程判断更改模型。

## 13. G4-STRIP-TD-B — 条件新 strip 16帧

- **scientific_target:** 仅在Ray result为`accepted_for_strip_entry`后，测量strip在相同
  operational-600 sequence下的quality、chronology与history。
- **next_scientific_action:** strip 16/16 quality/history pass后运行combined analyzer。
- **science_delta:** 新strip 16-frame dataset与analysis，或scientific valid hard failure。
- **contract:** 新experiment/root，same A/D/B/C sequence与A anchors，frozen strip command、
  observer、exposure/setup、no-ambient statistic，retry=0；Ray/R5只作immutable reference，
  禁止frame pooling。
- **stop:** 若必须改变observer、threshold、feature、exposure envelope或command，冻结证据并
  请求Advisor；quality/history/cleanup fail即锁combined/TD-C。

## 14. G4-COMBINED-TD-B — operational-600 双source gate

- **scientific_target:** 综合两个独立accepted source run，确定selected operational-600
  envelope，不把600秒解释为steady或TD-A pass。
- **next_scientific_action:** combined pass后执行TD-C core；combined fail则形成GUIDE定义的
  blocked scientific result。
- **science_delta:** `p7-operating-envelope-v3.json`与
  `p7-td-b-operational600-analysis-v1.json`及明确pass/fail。
- **pass:** Ray/strip均16/16、quality/history/source/exposure/physical/cleanup通过、无pooling、
  steady warning保留。
- **stop:** 任一条件失败则`REF-P7-05=blocked`、`TD-C=locked`；不得用另一source抵消。

## 15. G4-TD-C-CORE — 条件order-balanced 8 formal

- **scientific_target:** 在combined pass后，以600秒operational transient执行S1 Ray→strip、
  S2 strip→Ray、S3 Ray→strip、S4 strip→Ray的8 formal order-balanced comparison。
- **next_scientific_action:** 冻结TD-C core evidence并返回Advisor判断后续branch。
- **science_delta:** TD-C core order-balanced operational-600 evidence或scientific valid failure。
- **claim boundary:** `developer_selected_operational_dwell_s=600`、`steady_claim=false`；不得称
  steady ABBA或linear-drift elimination。
- **locks:** reference epoch final classification、endpoint expansion、sentinel、remaining-9、
  boundary、holdout、Gate-6、P8和default LUT/runtime install继续锁定，直到Advisor输入。

## 16. G4-GUIDE4-CLOSE — 阶段关闭

- **scientific_target:** 将完成或失败的整个GUIDE 4路线整理为可复现、可审查的科学结论。
- **next_scientific_action:** 由Advisor基于AUDIT PACK选择下一GUIDE或确认terminal branch。
- **science_delta:** GUIDE 4 terminal disposition；允许的出口为：Ray/strip/combined/TD-C的
  GUIDE定义科学负结果，或TD-C core完成等待Advisor。
- **AUDIT PACK:** 只含科学输入、实验spec、raw/measurement/analysis hashes、chronology、
  cleanup、negative/pass interpretation、remaining locks和明确科学问题；不恢复旧工程ledger。
- **complete:** 所有实际执行的run均可离线重放分析；repo docs反映新架构；PLAN/PLAN-FULL
  active=0；无进程/automation；设备final-zero；GUIDE/RESEARCH未修改。

## 17. 编排密度与提交策略

1. Git保护阶段一个PLAN；重构最多`DEENG-A/B/C`三个implementation PLAN；readiness是同一
   `DEENG-C`的终局验收，不另建工程计划。
2. 每个PLAN由一次高reasoning Planner设计、一次低成本Executer完整执行、一次Planner
   终局验收；不在命令/文件/test selector之间插入review。
3. 同一PLAN内允许修复该package暴露的局部缺陷；同一semantic seam第三次实质失败时停止
   并简化架构，不开第四轮。
4. accepted package形成focused commit；不为PLAN activation、状态行、selector或中间log
   单独提交。
5. generic code-review循环由本Human-directed program覆盖；只在最终整治候选做一次独立
   architecture/science-safety review。Planner review继续是每包默认质量门。
6. 整治完成后恢复默认科学吞吐规则：没有新的具体science blocker时不得再创建
   engineering-only PLAN。

## 18. 全局停止与升级

- Git非FF、backup push无法验证或用户改动无法分类：停止，仅报告Human。
- 可能损失raw/scientific evidence或改变已接受measurement interpretation：停止并保护数据。
- firmware、remote deploy、destructive hardware或active PLAN bounds外操作：请求Human。
- GUIDE/RESEARCH不足或矛盾，无法决定observer/threshold/exposure/scientific branch：生成
  `ADVISOR_INTERVENTION_REQUEST`。
- parser、path、Git、tests、module split、package format、runner architecture或cleanup实现：
  Orchestrator/Planner处理，不请求Advisor。
- refactor branch可以删除过度工程代码，但不得删除backup branch、历史Git对象、外部raw root
  或immutable scientific evidence。

## 19. GUIDE 4 完成判定

下列任一科学分支完成且证据可离线复现时，GUIDE 4 执行才可进入terminal review：

1. Ray R6 acquisition/quality scientific failure；
2. Ray history fail并输出`stop_history_model_required`；
3. strip acquisition/quality/history scientific failure；
4. combined TD-B fail并保持TD-C locked；
5. combined pass后TD-C core完成或产生GUIDE定义的科学失败。

工程重构、测试通过、代码删除、branch/commit或readiness unlock都不能单独标记GUIDE完成。
