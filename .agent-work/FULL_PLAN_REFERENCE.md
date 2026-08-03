# Advisor 4.GUIDE unfinished work reference

**文档状态：** `GUIDE4_COMPLETION_GOAL_ACTIVE_NON_EXECUTABLE_REFERENCE`

**快照日期：** `2026-08-03`

**Owner：** Orchestrator（唯一写入者）

**执行属性：** `non_executable_reference`

**适用 Advisor GUIDE：** `advisor/4/4.GUIDE.md`

**适用 GUIDE SHA-256：** `659152f6c0ae69c90c701de4e57c352d771e4f0bf75cf9410271ba0a94200e35`

**Archived predecessor：** `.agent-work/archived/FULL_PLAN_REFERENCE-20260803-1132.md`

**当前可执行任务数：** `0`

**当前 active task：** `none`

**唯一 canonical next reference：** `REF-G4-02-PREDEVICE`（`READY_FOR_PLANNING_AFTER_ACCEPTED_G4_01_RELEASE`）

`FULL_PLAN_MACHINE_STATE={"schema":"orchestrator_full_plan_guide4_goal_active_v12","snapshot_date":"2026-08-03","guide_path":"advisor/4/4.GUIDE.md","guide_sha256":"659152f6c0ae69c90c701de4e57c352d771e4f0bf75cf9410271ba0a94200e35","reference_revision_parent":"4e8d9c7330a0c2be6bb9f9dd912ec2b39348fbcd","content_policy":"UNFINISHED_TASKS_AND_REQUIRED_EXECUTION_INVARIANTS_ONLY","completed_content_allowed":false,"archive_policy":{"directory":".agent-work/archived","name_pattern":"{PLAN类型}-YYYYMMDD-HHMM.md","immutable":true,"overwrite":false},"archived_predecessor":{"path":".agent-work/archived/FULL_PLAN_REFERENCE-20260803-1132.md","status":"HISTORICAL_NON_EXECUTABLE_PRE_REWRITE_SNAPSHOT","source_commit":"779c7d9572d991f82076c892ec8198a059bbe44e","source_body_bytes":29546,"source_body_sha256":"0c8e15de428f401eb5e33da81b75ddf9d8e9d1e25b0b897c5396ac7816f3acc3","archive_bytes":30721,"archive_sha256":"ac72bcc4578aefcbf5aa23983d837cf749dbf982f9e1eeb75641dfa214c03d2d"},"active_task_count":0,"active_task":null,"active_plan_contract_id":null,"current_plan_active_task_count":0,"current_plan_active_task":null,"canonical_next_reference_task":"REF-G4-02-PREDEVICE","canonical_next_reference_status":"READY_FOR_PLANNING_AFTER_ACCEPTED_G4_01_RELEASE","executable":false,"plan_status":"ACCEPTED_G4_01_WAITING_ORCHESTRATOR_TERMINAL_DISPOSITION","active_human_goal_route":{"reference_goal":"REF-G4-COMPLETE","status":"GOAL_ACTIVE_WAITING_G4_02_PREDEVICE_PLANNING","objective":"COMPLETE_ADVISOR_4_GUIDE_REACHABLE_ROUTE_TO_MANDATED_STOP","first_reference_task":"REF-G4-02-PREDEVICE","first_reference_status":"READY_FOR_PLANNING_AFTER_ACCEPTED_G4_01_RELEASE"},"guide_completion_contract":{"success_definition":"ALL_REACHABLE_GUIDE4_STAGES_ACCEPTED_OR_MANDATED_FAIL_STOP_AND_ADVISOR_HANDOFF_REACHED","force_pass_prohibited":true,"historical_audit_inside_goal":false},"old_corrective_task_ids_reactivatable":false,"historical_route_policy":"ARCHIVED_ONLY_NO_REACTIVATION_NO_SUFFIX_GROWTH","legacy_retained_route":{"status":"HISTORICAL_ONLY_NOT_A_GUIDE4_PREDECESSOR","guide4_required":false,"execution_input_allowed":false,"task_ids_reactivatable":false},"frozen_guide_input":{"stage":"EQ-R6_STATE_C","selected_exposure":"1/2500","status":"ACCEPTED_QUALIFIED_INPUT_NOT_A_CURRENT_TASK"},"retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","canonical_validator_success":false,"eligibility":false,"release_consumable":false,"release_consumption_authorized":false,"device_authorized_by_this_file":false,"camera_authorized_by_this_file":false,"ray_authorized_by_this_file":false,"strip_authorized_by_this_file":false,"formal_r6_authorized":false,"td_c_authorized":false,"automatic_experiment_package_generation":false,"unresolved_scientific_questions_for_current_route":[],"allowed_next_action":"DELEGATE_PLANNER_FOR_REF_G4_02_PREDEVICE","planner_requirement":"WRITE_ONE_PURE_OFFLINE_G4_02_PREDEVICE_PACKAGE","full_is_non_executable_reference":true,"g4_01_prerequisite":{"disposition":"ACCEPTED_G4_01_SUCCESSOR_RELEASE_GENERATED_VALIDATED_NON_AUTHORIZING_UNCONSUMED","source_head":"779c7d9572d991f82076c892ec8198a059bbe44e","source_tree":"1ead5268917612d1232543b1a7eca28788f3980c","release_family":"/Volumes/4T/temp/rgbww-optimizer/g4-successor-lineage-779c7d9572d9-20260803T172055Z","release_bundle":"/Volumes/4T/temp/rgbww-optimizer/g4-successor-lineage-779c7d9572d9-20260803T172055Z/release","artifact_sha256":{"frozen-inputs.json":"8a81a906d2a94903a365f54b33c224a8ec99ce8d519ae2317cdc213c6e0264f8","r6-formal-plan.json":"dea5f979950909d5b3e8fd93c3a76e4fd18c0242158eade7967c4c62ec72cc3b","release-descriptor.json":"6843ef5007b9ebe3bfef1f7c8c1864ed0b86b3000d3d72caa8f08f67ce3bb452","validation-summary.json":"07e831616c303e68f9bf863a722b8b640c3726556f47143db8299083f941cc07","terminal-seal.json":"d9d7b784a4ec910d7c7740bc560ed87f2b99ab1744c19df42097d5683b668850"},"release_consumed":false,"eligibility":false,"device_or_formal_credit":false,"planner_review_archive":".agent-work/archived/PLAN-20260803-1126.md","execution_result_archive":".agent-work/archived/EXECUTION_RESULT-20260803-1126.md"}}`

## Current-state declaration

- `.agent-work/PLAN.md` 当前为G4-01 terminal acceptance checkpoint；PLAN与FULL active task count均为0，没有执行权。
- Human 已创建并恢复 `REF-G4-COMPLETE` goal；G4-01已按Planner验收为
  `ACCEPTED_G4_01_SUCCESSOR_RELEASE_GENERATED_VALIDATED_NON_AUTHORIZING_UNCONSUMED`，当前唯一 canonical next reference是
  `REF-G4-02-PREDEVICE`，只允许下一次Planner pass进行规划。
- G4-02所需compact frozen prerequisite：source HEAD `779c7d9572d991f82076c892ec8198a059bbe44e`、tree
  `1ead5268917612d1232543b1a7eca28788f3980c`、release bundle
  `/Volumes/4T/temp/rgbww-optimizer/g4-successor-lineage-779c7d9572d9-20260803T172055Z/release`；exact artifact hashes与
  Planner/ER archive identity只以machine row和`.agent-work/archived/FULL_PLAN_REFERENCE-20260803-1132.md`为准。
- Human 已明确：本 goal 的目标不是无脑推进某一个历史 package，而是完成当前适用的 Advisor
  `advisor/4/4.GUIDE.md`。下文 `REF-G4-*` 是本 goal 唯一允许规划的 canonical route。
- EQ-R6 State C `qualified_1_2500` 只作为当前路线的 frozen prerequisite；它不是本文件中的已完成 task条目，
  不得重跑，也不得降级成未确认结论。
- Retained R3 仍为 `RETAINED_UNVALIDATED_UNCONSUMED`；canonical validator success、eligibility、consumability 与 consumption 均为 false。
- Retained R3、旧 Option-B controller 链和所有深层 corrective task 只是历史工程证据，不是完成 4.GUIDE
  的 predecessor、release candidate 或默认实现输入；不得验证后直接消费、恢复、重试或继续追加 task-ID 后缀。
- 所有拆分前历史、G4-01完成叙述、rejection/corrective chain与handoff ledger只位于
  `.agent-work/archived/FULL_PLAN_REFERENCE-20260802-1038.md`与最新pre-rewrite snapshot；当前 FULL 不复制这些内容。
- 本文件不改变 GUIDE 科学结论，不授权设备、相机、Ray、灯带、network、FORMAL-R6、TD-C、固件、部署或任何实验。


> 本文件保存当前适用 GUIDE 要求、但尚未完成的完整路线。它不是执行队列，不授权设备访问、实验、
> retry、release、预算、Git commit 或阶段进入。Planner 与 Executer 只能读取本文件；只有由 Planner
> 写入 `.agent-work/PLAN.md` 的单一 active package 才能授权执行。

## 0. Canonical current route：完成 Advisor 4.GUIDE

### 0.1 目标、完成定义与控制边界

Human 已发起新 goal；Orchestrator 将 goal 解释为：从已接受的 EQ-R6 State C `1/2500`
开始，完成 `advisor/4/4.GUIDE.md` 当前仍可到达的所有阶段，直到 GUIDE 规定的成功出口或首个强制
fail-stop/Advisor handoff。不得把“完成 GUIDE”误写成“保证实验通过”；若 measurement quality、history、
source contract 或 combined gate 按 GUIDE 失败，冻结证据并正确停止也属于该路线的正确完成。

本节是本 goal 唯一 current unfinished route；第1节只提供当前路线仍需要的execution invariants。
历史设计与完成证据只允许从 archived snapshot、Git与既有evidence索引读取，不得从中恢复旧task ID、旧PLAN、
retained R3、旧release或一次性controller。独立clean-room审计已经在goal外完成；未来goal不重新做恢复审计，
除非新的可观测drift使当前前置事实失效。

本文件始终 non-executable。Orchestrator 已重读 Human goal、GUIDE、PLAN/FULL machine rows、失败夹具与当前 Git state，
确认G4-01已取得terminal accepted disposition并完成pre-rewrite FULL archive。当前没有active executable PLAN；唯一下一动作是
委派Planner为`REF-G4-02-PREDEVICE`写一个pure-offline predevice package。不得一次把后续设备阶段全部写进 PLAN，
不得由 FULL 自动生成实验 package。

### 0.2 Pending route 总表

| Reference ID | 当前状态 | 目的 | 直接依赖 | 解锁/验收 owner |
| --- | --- | --- | --- | --- |
| `REF-G4-COMPLETE` | `GOAL_ACTIVE_NON_EXECUTABLE_REFERENCE` | 完成 4.GUIDE 的全部可到达路线并在规定出口停下 | Human goal 已创建 | Human / Orchestrator |
| `REF-G4-02-PREDEVICE` | `READY_FOR_PLANNING_AFTER_ACCEPTED_G4_01_RELEASE` | 对 G4-01 的 fresh release 做严格 offline predevice oracle | G4-01 accepted release prerequisite | Planner |
| `REF-G4-03-ZERO-READINESS` | `BLOCKED` | fresh real zero/readiness 与设备身份/能力检查 | G4-02 accepted | Planner |
| `REF-G4-04-E2` | `BLOCKED` | fresh E2 preformal gate，不进行 formal capture | G4-03 accepted | Planner |
| `REF-G4-05-RAY-R6-STAGE-GATE` | `BLOCKED` | Orchestrator冻结一次 exact Ray R6 visible-Terminal launch | G4-04 accepted | Orchestrator |
| `REF-G4-06-RAY-R6` | `LOCKED` | 完整新 Ray-only formal R6 16 帧 | G4-05 exact stage gate | Planner |
| `REF-G4-07-RAY-ANALYSIS` | `BLOCKED` | Ray quality、chronology 与 A-return history gate | G4-06 terminal result | Planner |
| `REF-G4-08-STRIP-PLAN` | `CONDITIONAL` | Ray pass 后冻结独立 strip 16 帧 package | G4-07 history pass | Planner |
| `REF-G4-09-STRIP-RUN` | `LOCKED` | 新 root、strip-only formal 16 帧 | G4-08 accepted package | Planner |
| `REF-G4-10-STRIP-ANALYSIS` | `BLOCKED` | Strip quality、chronology 与 A-return history gate | G4-09 terminal result | Planner |
| `REF-G4-11-COMBINED-TDB` | `BLOCKED` | 生成 operating-envelope v3 与 operational600 analysis | G4-07 与 G4-10 pass | Planner |
| `REF-G4-12-TDC-CORE` | `LOCKED` | operational-600 transient 下的 TD-C core 8 帧 | G4-11 accepted | Planner |
| `REF-G4-13-ADVISOR-HANDOFF` | `BLOCKED` | 冻结 AUDIT PACK，交 Advisor 决定后续 scientific route | 成功终点或任一 GUIDE stop | Advisor |

以上状态不表示 FULL、release、device 或 experiment 权限；当前没有active executable PLAN，G4-01 release仍未消费且
eligibility/device/formal均为false。

### 0.4 `REF-G4-02-PREDEVICE`：fresh offline oracle

- **实现：** 对 G4-01 唯一 fresh release、current checkpoint、policy、R5 A/D/B shutter、EQ C shutter、R6 exact
  capture plan、16/16 与 physical cap、old/new pooling prohibition、operational-600/steady schema、cleanup/terminal
  paths做一次 fail-closed predevice oracle。全部输入都由 PLAN 冻结 exact path/hash。
- **安全边界：** pure offline；不得解析、验证或消费 retained R3，不得触碰设备或创建 formal root。
- **验收：** public/final/strict/replay/lineage checks一致；negative cases证明旧 R2、旧 retained R3、checkpoint drift、
  auto exposure、weak reacquire、wrong capture order与pooling都会拒绝；focused/full tests与 durable evidence 首次通过。
  Planner接受后，Orchestrator可为该 exact fresh release新增独立的current-route eligibility/consumption字段，供后续
  G4-03/G4-04 package使用；不得改写 retained R3 的 false字段或泛化为formal launch授权。
- **失败与 stop：** 普通代码缺陷只允许一次 bounded correction；contract/science conflict 停给 Orchestrator/Advisor。
  成功只解锁 G4-03，不授权 nonzero output或capture。

### 0.5 `REF-G4-03-ZERO-READINESS`：real zero/readiness

- **实现：** 在单一 PLAN 中冻结 fixture/camera/Ray/bridge identity 与 endpoint；执行 read-only health/config/capability、
  strip generation-bearing zero、Ray intensity 0、camera/bridge readiness、source isolation、Python finally、shell trap、
  independent final-zero 与 terminal seal。不得 capture，不得有 nonzero light output。
- **安全边界：** 只允许 AGENTS 所列 read-only 与 zero/off 例外；firmware/flash、remote deployment、配置写入、
  destructive operation、nonzero sweep均禁止。
- **验收：** identity/readback/chronology/cleanup exact，no stale process/root，所有设备最终为零；证据写入 fresh root，
  Planner 独立验收。失败时保持零并停止，不得现场修设备或绕过 capability mismatch。

### 0.6 `REF-G4-04-E2`：fresh preformal gate

- **实现：** 只消费 G4-01 release 与 G4-03 readiness evidence，验证 current checkpoint、exposure policy consumer、
  exact Ray states、strip-zero invariant、fixed shutter/no-reacquire、capture accounting、abort/cleanup 与 formal runner
  的 bounded dry/preformal path。不得执行 16 帧 formal，也不得留下 fixture nonzero。
- **验收：** E2 的 exact contract、side-effect ledger、cleanup、terminal evidence及相关测试全过；release/checkpoint未漂移。
- **失败与 stop：** 普通工程缺陷回离线一次 bounded correction；任何 measurement contract、source isolation或设备
  identity矛盾停止。成功只允许 Orchestrator进入 G4-05 stage review，不得自动进入 formal。

### 0.7 `REF-G4-05-RAY-R6-STAGE-GATE`：exact one-launch orchestration checkpoint

- **冻结内容：** exact experiment ID `P7-TD-B-RAY-OP600-EXPOSURE-GUARDED-FORMAL-R6`、新 root、Ray-only、
  strip始终为零、16 formal/physical cap16/setup0/ambient0/retry0/launch1、expected continuous-on window、fixed
  A/D/B shutters与C=`1/2500`、visible Terminal、abort、Python/shell cleanup与final-zero路径。
- **权限解释：** 4.GUIDE §6/§14/§16 的 Human visible-Terminal checkpoint是科学阶段隔离要求，但其重复授权
  建议受后来且更高优先级的 Human-owned AGENTS工程治理覆盖：有界灯光输出、相机capture、zero/off与本地实验
  不因其本身构成高危操作。G4-04 accepted后，Orchestrator可直接审查并要求 Planner把这一次精确launch写入
  G4-06 PLAN，不得让Planner/Executer重复向Human索取非必要授权。
- **仍需 Human 的边界：** firmware/flash、remote deployment、destructive hardware change、PLAN外设备操作，或需要
  扩大target/intensity/range/duration/retry/recovery path时必须停止并请求Human。Human若显式暂停或增加checkpoint，
  后来的明确决定优先。
- **stop：** exact target、root、budget、continuous-on window、abort或cleanup任一未冻结即不放行；不得生成半授权
  PLAN，也不得把一次 Ray launch扩成retry或strip stage。

### 0.8 `REF-G4-06-RAY-R6`：完整新 Ray 16 帧

- **固定合同：** GUIDE §7 的 exact `000-ray-a0-t600` 至 `015-ray-a-after-c-t600` 顺序；A/D/B exact R5
  frozen shutter，C exact EQ `1/2500`，ISO/aperture unchanged；auto exposure、weak reacquire、mid-run shutter change、
  R5 frame reuse与中途恢复均禁止。
- **运行：** 新 unique root；Ray-only；strip zero；16 logical/physical cap16；setup0；ambient0；launch1；retry0。
  每张 accepted 前验证 CR3/sidecar、bytes/SHA、remote IDs、MakerNote exposure、state/readback、58 features、
  clipping0、near-noise/finite/valid pixels、chronology、isolation与accounting。
- **长任务：** 若预计超过10分钟，Executer在可见 macOS Terminal 启动，做3次稀疏存活检查后回交；Orchestrator
  估算窗口、创建 automation唤醒本 task并按长任务规则阻塞，不使用 Codex background tool 持续轮询。
- **终止：** 任一 capture/cleanup/source failure立即形成 `accepted_hard_failed_formal_attempt`、formal pass false、
  retry0；无论成功失败均执行 Python finally、shell trap、independent final-zero、terminal seal并回 Planner。
  不在 formal run 内运行 analyzer、strip solver或生成 LUT。

### 0.9 `REF-G4-07-RAY-ANALYSIS`：Ray gate

- **入口：** 只接受 G4-06 terminal evidence；acquisition/quality hard fail直接转 G4-13，不运行 analyzer补救。
- **实现与验收：** Ray-only TD-B analyzer必须验证16/16 engineering quality，输出D/B/C的60/120/300/600 trend、
  dominance/direction，并以 existing same-state frozen joint coverage比较 A0/A-after-D/A-after-B/A-after-C。
  `steady_status=not_demonstrated` 始终保留；trend>4只表明未settled，不能单独否定 operational endpoint。
- **分支：** quality fail -> stop/Advisor；A-return history fail ->
  `history_dependent_at_operational_600` 与 `stop_history_model_required`，转 G4-13；只有16/16 quality pass且
  history pass才输出 `ray_td_b_operational_branch=accepted_for_strip_entry` 并解锁 G4-08。

### 0.10 `REF-G4-08-STRIP-PLAN`、`REF-G4-09-STRIP-RUN` 与 `REF-G4-10-STRIP-ANALYSIS`

- **Planning：** G4-08 必须是 Ray pass 后的新 Planner pass，冻结新 experiment/run ID、新 root、strip-only、Ray zero、
  existing strip command/observer/exposure/setup/no-ambient statistic、same A/D/B/C sequence、A returns@600、16 formal、
  retry0、source isolation、cleanup和old Ray manifest引用；本 task本身不运行设备。
- **科学变化 stop：** 若 strip 需要改变 observer、threshold、feature、exposure envelope或command，禁止现场调整，
  直接转 G4-13 交 Advisor；只有已有合同内 bounded exposure setup 才可写入 G4-09 PLAN。
- **运行：** G4-09 使用一个 fresh root，Ray始终为零；16/16、physical ledger、readback、chronology、retry0、
  Python/shell cleanup、independent final-zero、terminal seal。设备长任务遵循与 G4-06 相同的 visible-Terminal、
  3次liveness与automation规则。任一 formal failure立即 hard stop，不重跑。
- **分析：** G4-10 只消费 terminal result；验证16/16 quality与 A0/A-after-D/A-after-B/A-after-C compatibility，
  保留 `steady_status=not_demonstrated`。quality/history fail转 G4-13；两者全过才解锁 G4-11。

### 0.11 `REF-G4-11-COMBINED-TDB`：operational-600 gate

- **实现：** 只以两个已接受 source run的 immutable manifest运行 combined analyzer，不跨 source pooling；生成
  `p7-operating-envelope-v3.json` 与 `p7-td-b-operational600-analysis-v1.json`。
- **必须声明：** `developer_selected_operational_600s_transient_v1`、`operational_dwell_s=600`、
  `steady_status=not_demonstrated`、TD-A仍为`settling_not_demonstrated_by_600`、两source history pass、exact
  `A-D-A-B-A-C-A` previous-state scope。禁止 `t_formal=600`、settled/steady/TD-A pass。
- **验收：** GUIDE §10.2 十项条件逐项机器可判定；exposure/hash、ledger、source isolation、cleanup、worktree/checkpoint
  均闭合。任一失败转 G4-13且 TD-C保持 locked；不得用一 source的通过抵消另一 source失败。

### 0.12 `REF-G4-12-TDC-CORE`：operational-600 transient core

- **入口与范围：** 只有 G4-11 accepted并冻结 envelope v3后，Planner才可按 3.GUIDE core设计新 package：
  H120/S100，S1 Ray->strip、S2 strip->Ray、S3 Ray->strip、S4 strip->Ray，共8 formal；
  `developer_selected_operational_dwell_s=600`、`steady_claim=false`。
- **表述与锁：** 只称 `order-balanced comparison under operational_600s_transient`，不得称steady ABBA或
  linear-drift elimination。reference epoch final classification、TD-C expansion、sentinel、remaining9、boundary、
  holdout、Gate-6、P8 INT与default LUT/runtime install全部继续 locked。
- **安全/证据：** Planner必须先冻结exact device sequence、capture/physical budgets、source isolation、abort、cleanup、
  final-zero、analysis和failure branch；Human/PLAN边界按当时AGENTS适用规则取得，不得从G4-06/G4-09继承。
  terminal result经Planner验收后无论pass/fail都转 G4-13。

### 0.13 `REF-G4-13-ADVISOR-HANDOFF`：阶段 AUDIT PACK

- **触发：** Ray quality/history stop、strip contract/quality/history stop、combined fail、TD-C terminal result，或出现
  GUIDE无法决定的科学分支。
- **内容：** Human goal、GUIDE/hash、所有Planner archives、exact commits/trees/diffs/tests、release/checkpoint lineage、
  immutable artifact paths/bytes/SHA、capture/physical/accounting、quality/chronology/history、cleanup/final-zero、失败分类、
  remaining locks与一个不预选答案的scientific decision request。
- **验收与 stop：** Planner生成 AUDIT PACK；Orchestrator核对 provenance和状态后更新 FULL，并暂停受影响路线等待
  Advisor。不得在 handoff 期间自行改变阈值、feature、exposure、observer、command、dwell或继续后续 stage。

### 0.14 收敛、Git 与 Planner/Executer循环规则

- Orchestrator必须把每次plan编写和result验收实际委派给Planner subagent，把每次已授权执行实际委派给
  Executer subagent，并独立审查两者handoff；不得自己兼任三种角色以跳过交叉验收。
- 每轮只允许一个 flat `REF-G4-*` reference进入一个 PLAN；Planner验收后先归档并重写单一下一包，Orchestrator
  独立审查结果再更新 FULL。Executer只写 `EXECUTION_RESULT.md`，不得编辑 PLAN/FULL。
- PLAN通常只由Planner写。唯一窄例外是Planner把当前AGENTS未定义为高危的有界灯光、camera capture、read-only、
  zero/off、offline computation错误判为必须重复Human授权时，Orchestrator可直接删除该错误授权门并放行原exact
  bounds，同时记录override；不得借此修改科学合同、扩大设备范围，或覆盖firmware/flash、remote deployment、
  destructive hardware change及Human显式暂停。
- 普通工程边界第一次失败：一次 bounded correction；同边界第二次失败：重新判断 owner/state seam并允许一个最小
  enabling refactor；第三次相同边界失败：停止并回 Orchestrator，不得出现第四次同类 retry或 task-ID suffix增长。
- GUIDE明确的 scientific/formal hard stop（retry0、quality fail、history fail、strip contract变化、combined fail）首次
  命中即停止，不适用三轮工程纠偏规则。
- 任一已授权且预计超过10分钟的任务都由Executer在可见macOS Terminal启动，不使用Codex tool background process。
  Executer做3次稀疏liveness检查；确认存活后Orchestrator估算完成窗口、创建automation唤醒本task、把goal标为
  blocked并停止轮询。若Human主动恢复goal，只做1次状态检查：未完成则再次blocked且不继续轮询；已完成则删除
  automation，取得terminal evidence并恢复Planner验收循环。
- Orchestrator亲自分类 dirty worktree并为每个验收完成的离散工程单元建立 focused commit；不push。不得为追求
  “干净历史”重写、删除或reset旧evidence。任何旧 archive/root/release保持immutable。
- 新实现跨 persistence、device control、measurement、shared state或巨型P7 coordinator前必须执行维护性preflight；
  优先复用当前production owner和测试入口，禁止新增平行semantic owner。只有必要的最小重构进入当前task。

## 1. Current execution invariants

- Frozen R5 artifacts只读；其11帧仅可作为diagnostic provenance，old/new frame pooling一律禁止。
- 011 clipping不进入feature vector、center、covariance、history或reference analysis。
- Observer、58 features、P1 `1.0x..1.25x` identity-response/quality envelope、clipping threshold0、
  near-noise、valid-pixel、nonfinite、covariance、joint coverage、no-ambient statistic均不变；confirmation
  或qualification data不得扩大tolerance。
- A/D/B shutters exact取自frozen R5；C exact取自accepted EQ input `1/2500`。无新Advisor决定不得修改或重跑EQ。
- Ray R6 formal16/physical16/setup0/ambient0/launch1/retry0；formal内禁止auto exposure与weak reacquire。
- 600秒是selected transient，不是steady、settled、TD-A pass或`t_formal`。
- Ray R6 16/16且A history pass前strip locked；两source combined pass前TD-C locked；Advisor前sentinel/P8 locked。
- 每个设备stage使用新root、single PLAN、visible Terminal（>10min）、abort、Python/shell cleanup、
  independent final-zero、terminal seal；不得跨stage连续自动长跑。
- Ray与strip不得同时非零；每个returned CR3先写physical-return ledger，rejection也保留sidecar/remote IDs/hash。
- Release generation/qualification/consumption、device access与formal launch分离；R2与historical retained R3均不得
  复用或消费，当前G4路线只允许生成一个fresh unique successor release。
- Public shared protocol default按Human分类保留；private explicit override不打印、不序列化、不写CLI。
- Firmware/flash、remote deployment、destructive hardware change和PLAN外操作需Human授权；普通bounded light/zero、
  offline release/validation不因FULL而增加危险操作授权要求。
- 不将measurement/quality/solver/uncertainty failure写成gamut或物理不可达。
- 不覆盖default LUT、安装runtime candidate或进入P8/P9/交付，除非对应decision task完成。
