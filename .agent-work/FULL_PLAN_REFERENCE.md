# GUIDE 当前未完成任务完整计划参考

**文档状态：** `orchestrator_reference_current`

**快照日期：** `2026-07-30`

**Owner：** Orchestrator（唯一写入者）

**执行属性：** `non_executable_reference`

**适用 Advisor GUIDE：** `advisor/4/4.GUIDE.md`

**适用 GUIDE SHA-256：** `659152f6c0ae69c90c701de4e57c352d771e4f0bf75cf9410271ba0a94200e35`

**当前代码 checkpoint：** `9303aa22a9bd37e8ec4f23147c78c6bea84b9a2e`

**当前可执行任务数：** `0`

**当前 active task：** `REF-P7-25-R2-B2 corrected exact-path modern manifest seal`

`FULL_PLAN_MACHINE_STATE={"schema":"orchestrator_full_plan_reference_v2","snapshot_date":"2026-07-30","guide_path":"advisor/4/4.GUIDE.md","guide_sha256":"659152f6c0ae69c90c701de4e57c352d771e4f0bf75cf9410271ba0a94200e35","active_task_count":0,"active_task":"REF-P7-25-R2-B2","active_plan_contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-CORRECTED-PATH-MANIFEST-SEAL-V3","next_reference_task":"REF-P7-25-R2-B3","next_reference_status":"BLOCKED_ON_B2_ACCEPTANCE","human_checkpoint":"REF-P7-22","human_confirmation_satisfied":true,"authorization_override":"REF-P7-23-H2_SUPERSEDED_AUTHORIZATION_MISCLASSIFICATION","engineering_governance_override":"HUMAN_2026_07_29_ORCHESTRATOR_OWNS_FILES_CODE_GIT","checkpoint_head":"9303aa22a9bd37e8ec4f23147c78c6bea84b9a2e","release_checkpoint":"32b9e670ff3bbea0cd1505528c2ca87c2935446c","eq_r6_status":"ACCEPTED_QUALIFIED_1_2500","selected_state_c_shutter":"1/2500","post_eq_policy":"ACCEPTED_COMPLETE","evidence_controller_ownership_selection":"OPTION_A_REPO_OWNED_RETAINED_RELEASE_AUDIT_HELPER","option_a_owner_status":"ACCEPTED_COMPLETE","advisor_lineage_owner_decision":"OPTION_B_SCIENTIFIC_INTENT_RETAINED_IMPLEMENTATION_LIMITS_SUPERSEDED","manifest_authority":"SUBORDINATE_EVIDENCE_ONLY_CANONICAL_VALIDATOR_SOLE_ELIGIBILITY_OWNER","helper_v1_disposition":"RETAINED_RELEASE_AUDIT_PREREQUISITE_V1_SUPERSEDED_BEFORE_REAL_VALIDATION","repair_v2_status":"B2_C1_ACCEPTED_B2_CORRECTED_WAITING_ACTIVATION","retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","executer_dispatched":false,"device_authorized_by_this_file":false,"candidate_machine_contract_sha256":"64a5b144faaa9b07f2e24d40a17b4b5938dada88f919136404b9da3d91a7fdac","candidate_contract_orchestrator_verified":true}`

> 本文件保存当前适用 GUIDE 要求、但尚未完成的完整路线。它不是执行队列，不授权设备访问、实验、
> retry、release、预算、Git commit 或阶段进入。Planner 与 Executer 只能读取本文件；只有未来由 Planner
> 写入 `.agent-work/PLAN.md` 的单一 active package 才能授权执行。

## 1. 文档合同

### 1.1 所有权与本轮边界

- `.agent-work/FULL_PLAN_REFERENCE.md` 由 Orchestrator 独占维护，回答“全部未完成 GUIDE 工作是什么”。
- `.agent-work/PLAN.md` 由 Planner 独占维护，回答“Executer 当前只执行哪一个 package”。
- `.agent-work/EXECUTION_RESULT.md` 由 Executer记录执行证据；Executer不得编辑两个计划文件。
- Human 后续明确要求恢复正常 Planner/Executer loop。Planner 已归档旧 R5 Advisor-stop，并写入唯一
  `REF-P7-18` active PLAN，contract ID
  `P7-TD-B-R6-PRE-EQ-OFFLINE-PREPARATION`。FULL 不嵌入 active PLAN hash，避免 PLAN 冻结 FULL hash
  时形成循环引用；exact PLAN hash 由 Orchestrator handoff 单独冻结。
- 旧 PLAN 已归档为
  `.agent-work/PLANS/20260727-1212-p7-r5-advisor-decision-review.md`，SHA-256
  `51367f7096b81406da138b5c43bbd059224189e5837ba9472037c9e36184a331`。
- Orchestrator 已独立验收该 PLAN 并只放行 `REF-P7-18` pure-offline package；设备、EQ、release、
  formal R6、strip 与 TD-C 仍未授权。

### 1.2 来源优先级

科学方向、工程治理与产品决定按以下顺序解释：

1. 后来的显式 Human/Developer 决定；
2. 最新适用的 Advisor GUIDE；
3. 早期 GUIDE 中未被替代的要求；
4. Planner review archives、执行 evidence 和实现文档。

Advisor GUIDE只对色彩科学、测量科学、实验解释和科学分支具有权威性。文件范围、代码架构、provenance实现、
execution packaging与Git topology由Orchestrator决定；这些工程事实与GUIDE实现建议冲突时，Planner回报Orchestrator
纠偏，不得停到Advisor。只有科学分支不确定或命中AGENTS高风险设备边界时才暂停；Executer不得现场选择解释。

### 1.3 状态词

| 状态 | 含义 |
| --- | --- |
| `ACTIVE` | 已由唯一 active PLAN 精确放行并交 Executer；权限只来自 PLAN，不来自 FULL。 |
| `PLANNER_REVIEW` | Executer 已终止并回交；在 Planner 接受、拒绝或改写下一包前不可执行。 |
| `READY_FOR_PLANNING` | 科学依赖已满足，可在未来独立 Planner pass 中转成唯一 active PLAN；当前仍不可执行。 |
| `BLOCKED` | 前置 task、证据、checkpoint 或决定未完成。 |
| `LOCKED` | GUIDE 明确禁止当前进入。 |
| `CONDITIONAL` | 只有命名失败/成功分支出现时才进入。 |
| `HUMAN_CHECKPOINT` | GUIDE 要求 Human 对一个精确实验阶段单独确认；不是 FULL 自行取得的设备授权。 |
| `ADVISOR_DECISION` | 需要 Advisor 冻结科学方向。 |
| `HUMAN_DECISION` | 需要 Human 决定产品、安装或危险操作。 |
| `DEFERRED` | 未完成，但不在当前主路线。 |

### 1.4 更新与验证规则

Orchestrator 在新 GUIDE、Human 决定、Planner review 或 Executer terminal result 到达后更新本文件。每次更新必须：

1. 更新 source path/hash、快照日期、状态表和依赖；
2. 为新任务分配不复用的稳定 ID；
3. 每个 unfinished task 保留依赖、owner、实现轮廓、安全边界、证据、验收、失败分支和 stop point；
4. 已完成细节只在 baseline 保留必要事实，完整历史继续位于 review archives/audit；
5. non-executable 等待状态保证 `ACTIVE=0`；
6. 验证所有 task ID 依赖存在、Markdown 结构和 `git diff --check`；
7. 不写 secret、private override、无界设备命令或可直接消费的授权。

## 2. 冻结来源与证据锚点

### 2.1 GUIDE 与 Human 决定

| 来源 | SHA-256 | 用途 |
| --- | --- | --- |
| `advisor/1/1.GUIDE.md` | `f89a6e79026f3cb765f84f0d98b254dff0a5807ee772368dbb935a6843c7871b` | P7/P8/P9 长期目标、validation 与交付。 |
| `advisor/2/1.GUIDE.md` | `885d761ba04586613bafe399c6bf03519043a44341eb22b586d24dcbfb3d6e26` | P7 v2 uncertainty、sentinel 4+9、boundary、holdout 和 P8 lock。 |
| `advisor/3/1.GUIDE.md` | `92f766da523c40ff49c228c996dffd6d3839552f70bbd79aa7627485dd749be1` | TD-A/B/C thermal/reference 基线；未被 4.GUIDE 替代的部分继续有效。 |
| `advisor/4/4.GUIDE.md` | `659152f6c0ae69c90c701de4e57c352d771e4f0bf75cf9410271ba0a94200e35` | R5 clipping 处置、EQ-R6、Ray R6、conditional strip、combined TD-B 与 TD-C 新合同。 |
| `/Users/ibobby/.codex/attachments/cba7928d-712a-441e-a708-4301ee32bd66/pasted-text.txt` | `91a88e5467e13c811794c2149b6a8d5669e613c3e259d8f4091ba08c048733d6` | Advisor 对 retained-R3 helper lineage owner 的后续显式决定：Option B subordinate exact provenance manifest。 |
| `3e2ebed132b6d4338bfa324bfc42c3565d2eeb3c:AGENTS.md` | blob `58bfacb5fc46fcb42bf643d12974063533a684eb`；file SHA-256 `604b10bedeac6c9285f6448f94323521bf021a58275cce84d64163e16a2f07a0` | 可由Git独立重放的Human工程治理落盘证据：Advisor仅指导色彩/测量科学；Orchestrator统筹实验、文件、代码与Git，仅科学问题或高风险设备操作停下。 |
| `advisor/4/0.AUDIT/03-human-decision-no-extension.md` | `c917c54473aa3c5cc4da9098ddeb81fb109fe9a4186fb71e994c447c63d0454a` | Human 拒绝 900/1200 秒；600 秒是 operational time limit，不是 settled。 |

Human 已在先前 thread 中解除设备暂停并允许有界设备调用。该决定不使 FULL 可执行，也不跨过
4.GUIDE 要求的 EQ-R6 与 R6 分阶段 Human checkpoint。远程 firmware/flash、remote deployment 和破坏性硬件
操作仍需明确 Human 危险操作授权；release、offline validation 和普通有界灯光/cleanup 本身不属于危险操作授权。

### 2.2 第四轮 AUDIT

| 来源 | SHA-256 | 用途 |
| --- | --- | --- |
| `advisor/4/0.AUDIT/README.md` | `35113be7cd3de782677708c70c76434da40aca96de8053c2ae6cc87519be45d8` | 第四轮包导航与完整性声明；07 是当前 lineage-owner 决策输入。 |
| `advisor/4/0.AUDIT/04-advisor3-to-formal-r5-completed-work.md` | `a870c51d9863a02215fa9db78d78f30dae5e8112e768fb4c8d5361c875f2a11e` | Advisor/3 到 R5 的完整任务与结果。 |
| `advisor/4/0.AUDIT/05-formal-r5-observer-quality-decision-request.md` | `5dd454fcc27faf5e1579457eea53e36c9afd5fa918c7f742d64f0260f1db6f94` | R5 clipping 决策问题；已由 4.GUIDE 回答。 |
| `advisor/4/0.AUDIT/06-commit-and-evidence-index.md` | `cf6977b231cc9461b4b2a46ec4a8814ae52051632e1df96d1666ceb48f8b4c58` | 47 个提交与 retained evidence 索引。 |
| `advisor/4/0.AUDIT/07-guide4-to-retained-r3-lineage-owner-decision.md` | `5b23cbdfe97ac71e7438f1d30461455938828029c0ba32e931a9570e0ea88a34` | Option A/B/C lineage-owner 决策证据；已由后续 Advisor attachment 选择 Option B。 |

### 2.3 R5 immutable evidence

Exact root：

```text
/Volumes/4T/temp/rgbww-optimizer/p7-td-b-formal-r5/formal-r5-1e3b107-20260726T220000Z
```

| Artifact | SHA-256 / 冻结事实 |
| --- | --- |
| `ray-formal/plan.json` | `94da09f240e2d0ca84ce545c52748522dfbaa9a674bf96ffcef5c8e74473ba9f` |
| `ray-formal/failure.json` | `2984ec745f2b7cddad1549535b730ae75397cdf7f1fa8602f71010f6613a9a65` |
| `ray-formal/measurements/011-ray-c-t60.patch-statistics.json` | `98b792f0ef2d89718102c054fa4c4ad43206cf3cce82855d9c67900b6223a8be` |
| `ray-formal/run.json` | `dfba25366d6deb093170ceb21ee2fa259143f0da4ba0628216de0d6f23f03079` |
| `ray-formal/physical-returns.jsonl` | `d6569f121c7a31ac1dfb427fe2de1dccc8b46fe3be6e4f3d7ba007d8019e6e02` |
| `terminal-audit.json` | `4bee490fa83bad33830cf5e8941ccc7fa0ca83191903639c617af5fe9d5e7d79` |
| `returned-summary.json` | `5e97023d84d91f0037b096bf84e1102a8b786aa174a383b65087669fb5401955` |
| `ray-formal/all-off-python.json` | `982cee95d59cc18ae1270fdc02f3c8947008796593fa22deb07f925ebd5327dc` |
| `ray-formal/all-off-shell.json` | `3c4ea47739e009cef740791e86195f8e76ec8ddb805b3a937efee75c01cf3381` |

R5 冻结 shutters 来自上述 `plan.json`，其 ledger hash 为
`b49dd52ebc1eabc8ae6ae0e3713884e5e939428d0682e6d7234eea8c17626e71`：

```text
A / ray-h120-s100 = 1/5000
D / ray-h120-s50  = 1/6400
B / ray-h0-s0     = 1/8000
C / ray-h300-s100 = 1/2000  (R5 failure policy；不得用于 R6)
ISO = 100
aperture = implicit auto
actual exposure owner = Canon:ExposureTime
```

R5 required inputs：

```text
observer = b81d563eba1910286d879e560538dd497385e422c1bab762008c2b28a26fc4d9
operating envelope v2 = 7012f254e5fa5182dd51b72624f64ce03645fd3d8b7227ab9144f5c7767cfc16
policy = db9ebef1503c5e54c989649c719c4a5f75445bbd5487edb14c274e1b2894f3b4
uncertainty = cedaa1e9d342beb7e464c4e38d77884ad8a7790771432ebdbb5a101ca604aa94
R2 lineage release = 36a2ecd7c68bda35b4f722548b3c7a3bbafc880fc012af28c8fc501eed19d519
```

R2 release 只作为历史 provenance；4.GUIDE 明确禁止为新 code/config 复用或改写它。

### 2.4 当前 orchestration evidence

```text
HEAD = 1e3b107b8fbfe97bae5624ef638c4883a0faee1d
EXECUTION_RESULT = cc4627828f97d41951945561bf82a22c491693eb9e894957d9964da08d4f1ff9
superseded FULL snapshot = cba7c8d66b9aacbbf0b431e7dc8972f5f37699a94f125d6fd19052cadfec992d
stale Advisor-stop PLAN = e28a1d4cd8c0af5a8dd2d3bf3eb7dcbf7d6b57900b62cf99561fd42f88f09bf9
```

### 2.5 4.GUIDE 顺序规范化

4.GUIDE 的 §4.4、§5、§6 与 §14.2 一致给出：

```text
pre-EQ offline implementation + checkpoint
-> Human EQ-R6 checkpoint
-> EQ-R6
-> finalize selected C policy + new checkpoint
-> unique successor lineage release
-> fresh predevice / real zero-readiness / E2
-> Human one-launch checkpoint
-> full Ray R6
```

§16 的摘要句把 `successor lineage` 写在申请 EQ-R6 之前；若按字面执行，会与 C shutter 尚为 null、§6 要求
EQ 后 finalize policy 以及“任何 config/hash 改变不得复用 release”冲突。本 FULL 采用上述四处更具体且相互一致的
顺序：EQ 前只生成 pre-EQ implementation checkpoint，不生成 final successor release；EQ 选定 C shutter 后再生成
final policy checkpoint 和唯一 R3 release。未来 Planner 若发现实现无法保持此顺序，必须停在 Advisor clarification，
不得提前生成一个随后必然失效的 release。

## 3. 已完成或被 4.GUIDE 决定的 baseline

- `P0-R through P6 = retained`。identity RAW、四 CFA plane、58 required features、P6
  `full_periodic_2d_HB`、SAT0 Hue undefined、HSI/RGB endpoint 分离继续冻结。
- P7-D0 已接受；P7-R1 作为 valid failure evidence 保留且不重跑。
- TD-A Ray/strip 均 `settling_not_demonstrated_by_600`；`t_formal` 与 provisional 字段仍为 null。
- Human 选择 `operational_dwell_s=600`，语义固定为
  `selected_fixed_time_transient_not_proven_steady`。
- TD-B no-ambient statistic、physical-return/accepted ledger、sidecar/remote-ID atomic evidence、cleanup 和
  lineage owners 已建立；不得由成功的离线 evidence 推导 formal pass。
- Human-classified Ray public shared protocol default 继续有效；optional explicit override 仍是 private runtime value，
  不得写入参数、日志或 artifact。
- R5 永久为 `retained_accepted_hard_failed_formal_attempt`，formal pass 永久 false，launch 1/1、retry 0、
  strip/public analyzer 0。
- R5 `011-ray-c-t60` 分类已由 Advisor 冻结为
  `state_specific_exposure_policy_failure_with_required_feature_observer_saturation`：
  `block_06/white:G1/G2` required features 出现非零 clipping；不是 low-signal。
- R5 前 11 帧只允许 `diagnostic_only`，不得用于 formal inference，不得与任何新 frame pooling。
- `REF-P7-04` 的 Advisor decision 已由 4.GUIDE 完成，不再是 unfinished task。
- 原 `REF-P7-07` 的 600-second/TD-C prerequisite 决策已由 4.GUIDE §11 完成：只有 combined TD-B
  operational-600 gate 通过后才可条件进入 TD-C；TD-C 仍不得称 steady。
- 旧 R5 root、R2 release 和旧 failed roots全部 immutable；不得追加“成功补拍”、改写或重新消费。
- `REF-P7-18-C1` 与 parent `REF-P7-18/19/20/21` 已由 Planner 接受完成；accepted checkpoint为
  `98de1a91c264d4b72c4a97fc499ae7d39a67dacc`。Acceptance archive：
  `.agent-work/PLANS/20260727-1309-p7-r6-pre-eq-c1-acceptance-review.md`，SHA-256
  `35e0e49aaa91f438602346cb70af46efdfd520e1a1a508b393dc1ddc37940470`。

## 4. 未完成路线总表

| Task ID | 状态 | 任务 | 直接依赖 | 解锁/决定 owner |
| --- | --- | --- | --- | --- |
| `REF-P7-23-C1E1` | `ACCEPTED_COMPLETE` | C1 immutable evidence seal纠偏 | terminal evidence accepted | Planner |
| `REF-P7-23-C2` | `REJECTED_EVIDENCE_LIFECYCLE` | EQ-R6 single prelaunch owner离线纠偏 | second generator after stop | Planner |
| `REF-P7-23-C2E1` | `REJECTED_PREFLIGHT_MAPPING` | C2 one-shot evidence lifecycle纠偏 | wrong frozen paths | Planner |
| `REF-P7-23-C2E2` | `ACCEPTED_COMPLETE` | C2 exact-path one-shot evidence纠偏 | exact terminal evidence accepted | Planner |
| `REF-P7-23-R1` | `REJECTED_REPEATED_RESOLVE` | Fresh zero-only hostname reachability gate | repeated resolve timeout | Planner |
| `REF-P7-23-H1` | `ACCEPTED_COMPLETE` | Current same-stack resolver事实 | Human same-stack nonempty return | Planner |
| `REF-P7-23-R2` | `ACCEPTED_COMPLETE` | Fresh zero-only recovery gate | exact pass evidence accepted | Planner |
| `REF-P7-23-C3` | `REJECTED_PLAN_PATH` | Feature-selection与physical-return accounting离线纠偏 | focused test path mismatch | Planner |
| `REF-P7-23-C3E1` | `REJECTED_PLAN_COMMAND` | C3 corrected focused path续包 | invalid postcommit git-show command | Planner |
| `REF-P7-23-C3E2` | `ACCEPTED_COMPLETE` | C3 one-shot evidence continuation | exact terminal evidence accepted | Planner |
| `REF-P7-23-C4` | `REJECTED_PREDEVICE_PATH_MAPPING` | 首次fresh activation static preflight误用无编号C3E2 alias | device/root entry均0 | Planner |
| `REF-P7-23-H2` | `SUPERSEDED_AUTHORIZATION_MISCLASSIFICATION` | 错误的fresh-attempt重复授权门；已由Orchestrator按AGENTS高危边界覆盖 | C3 accepted;既有EQ确认保留 | Orchestrator |
| `REF-P7-23` | `ACCEPTED_QUALIFIED_1_2500` | EQ-R6 state-C exposure qualification | Branch A 4/4 accepted；candidate2=0 | Planner |
| `REF-P7-24-R1` | `REJECTED_PREEDIT_MANIFEST_SERIALIZATION_AMBIGUITY` | Selected C policy finalization R1 | manifest hash不可独立重放；edit/device=0 | Planner |
| `REF-P7-24-C1` | `ACCEPTED_IMPLEMENTATION_EVIDENCE_INCOMPLETE` | Replayable manifest后selected-C implementation/checkpoint | commit161094f；generator parse前失败 | Planner |
| `REF-P7-24-C1E1` | `ACCEPTED_COMPLETE` | Accepted checkpoint的post-EQ exact-11 evidence seal | exact11；mismatch=[] | Planner |
| `REF-P7-24` | `ACCEPTED_COMPLETE` | Selected C policy finalization 与 post-EQ checkpoint | checkpoint161094f accepted | Planner |
| `REF-P7-25-R1` | `REJECTED_PREACQUISITION_MANIFEST_AMBIGUITY` | Successor R3 release首次尝试 | package/qualification/release=0 | Planner |
| `REF-P7-25-C1` | `REJECTED_CHANGED_PATH_POLICY` | 可重放old-R2 manifest与preacquisition owner后生成R3 release | qualification正确拒绝两条未分类路径 | Planner |
| `REF-P7-25-C2` | `REJECTED_POSTCOMMIT_FOCUSED_TEST` | accepted post-EQ两路径exact ancestry/blob classification纠偏 | production commit保留；postcommit negative mock失败 | Planner |
| `REF-P7-25-C2E1` | `REJECTED_FULL_DISCOVERY_INVOCATION` | checkpoint-drift test seam与one-shot evidence纠偏 | test diff保留；错误discovery命令hard stop | Planner |
| `REF-P7-25-C2E2` | `ACCEPTED_COMPLETE` | 用正确discovery验证并提交已冻结test diff，再seal evidence | 641/641；postcommit2/2；evidence accepted | Planner |
| `REF-P7-25-R2` | `REJECTED_RELEASE_AUDIT_LEDGER_SHAPE` | checkpoint32b9e67的唯一fresh successor R3 release generation/validation | qualification通过；retained release未验证/未消费 | Planner |
| `REF-P7-25-R2-C1` | `REJECTED_PRE_PERSISTENCE_PARENT_ROOT_CONTRACT` | schema-aware external adapter只读验收retained R3 artifacts | intermediate parent absent；所有audit为0 | Planner |
| `REF-P7-25-R2-C1R1` | `REJECTED_SOURCE_PERSISTENCE_WRITER_FAILURE` | fresh两级root与单一schema-aware controller只读验收 | writer缺os；empty root retained | Planner |
| `REF-P7-25-R2-C1R2` | `REJECTED_OUTER_WRITER_PREFLIGHT_FALSE_REJECTION` | 冻结outer imports并preflight binding后执行fresh retained audit | `__module__` predicate误拒有效binding | Planner |
| `REF-P7-25-R2-O1` | `REJECTED_FOCUSED_GATE` | repo-owned retained-release audit helper单一owner | 17/20 pass；1 owner gap+2 test contracts | Planner |
| `REF-P7-25-R2-O1-C1` | `REJECTED_FULL_SUITE_TERMINAL_EVIDENCE_UNPROVEN` | replay count invariant与两项test contract最小纠偏 | focused20/20；full exit/summary丢失 | Planner |
| `REF-P7-25-R2-O1-C1R1` | `ACCEPTED_COMPLETE` | 冻结diff后durable full capture、exact two-path commit与synthetic seal | full661/661；postcommit20/20；helper commit9303aa2 | Planner |
| `REF-P7-25-R2-O2` | `REJECTED_DYNAMIC_FULL_BYTES_BINDING` | 使用accepted helper对冻结retained R3做一次真实只读审计 | pre-acquisition FULL hash drift；audit credit=0 | Planner |
| `REF-P7-25-R2-O2-C1` | `REJECTED_HELPER_SCHEMA_BOUNDARY_BEFORE_PUBLIC_VALIDATION` | 用唯一FULL machine state语义绑定后执行同一冻结R3只读审计 | fail terminal；callbacks0/0；audit credit=0 | Planner |
| `REF-P7-25-R2-O3` | `REJECTED_LINEAGE_POLICY_OWNER_REQUIRED` | 对账真实retained/public/helper schema owner，仅在proven helper bug时两文件纠偏 | focused21/21；lineage4/5；two-path diff retained | Planner |
| `REF-P7-25-R2-O3-C1` | `REJECTED_CODEGRAPH_TARGET_EVIDENCE_UNPROVEN` | 冻结helper commit两路径的lineage owner缺口并生成durable决策证据 | Git proof carried；wrong-target CodeGraph；seal0 | Planner |
| `REF-P7-25-R2-O3-C1R1` | `REJECTED_INCOMPLETE_CODEGRAPH_VERBATIM_COVERAGE` | 一次精确targeted CodeGraph owner read后seal carried proof | target/no-stale pass；3 symbols+branch missing；seal0 | Planner |
| `REF-P7-25-R2-O3-C1R2` | `REJECTED_INCOMPLETE_WORKFLOW_MAP_RANGE` | 承接CodeGraph后仅窄读缺失owner ranges并seal证据 | 120/320 lines；workflow closing缺失；seal0 | Planner |
| `REF-P7-25-R2-O3-C1R3` | `ACCEPTED_ADVISOR_DECISION_EVIDENCE_READY` | 仅补读workflow map exact lines244-245后seal carried evidence | evidence842cfad；six-owner absence proven | Planner |
| `REF-P7-25-R2-ADVISOR-STOP` | `ACCEPTED_OPTION_B` | 选择helper commit exact lineage classification owner | subordinate exact manifest；canonical validator唯一eligibility owner | Advisor |
| `REF-P7-25-R2-B0` | `ACCEPTED_COMPLETE` | 冻结Option B决定、v1 disposition、v2 exact repair与持续锁 | Advisor attachment SHA91a88e5 | Orchestrator |
| `REF-P7-25-R2-B1` | `ACCEPTED_BLOCKED_CONTRACT_CONFLICT` | 证明clean-room exact commit/manifest/canonical-validator路径可行且无第三repo path | static seam证明第三repo path必需；clean-room未创建 | Planner/Executer |
| `REF-P7-25-R2-B1A` | `ACCEPTED_COMPLETE_CANONICAL_SEAM_INTEGRATION` | exact canonical-validator seam与subordinate provenance integration | C17 full691/691 accepted；retained R3仍未验证/消费 | Planner/Executer |
| `REF-P7-25-R2-B1A-C1` | `ACCEPTED_HARD_FAILURE_WITH_CANDIDATE_CARRY_FORWARD` | single Python fail-fast acquisition后执行原five-path合同 | candidate frozen；pytest launcher absent；tests0 | Planner/Executer |
| `REF-P7-25-R2-B1A-C2` | `ACCEPTED_FALSE_REJECTION_OWNER_REASSESSMENT` | fresh-root exact candidate carry-forward + clean-room unittest identity | controller transcribed wrong SHA；source unchanged | Planner/Executer |
| `REF-P7-25-R2-B1A-C3` | `ACCEPTED_PRE_ROOT_ORCHESTRATOR_ACTIVATION_FAILURE` | PLAN内唯一strict candidate machine contract驱动carry/test/commit/seal | FULL漏2 machine fields；root0 | Planner/Executer |
| `REF-P7-25-R2-B1A-C3E1` | `ACCEPTED_PRE_ROOT_FALSE_REJECTION` | nested required_full_machine_state驱动programmatic activation后执行C3 | controller错误拒绝合法Python symlink；root0 | Planner/Executer |
| `REF-P7-25-R2-B1A-C3E2` | `ACCEPTED_PRE_ROOT_FALSE_REJECTION` | resolved executable + unittest loader probe后执行同一candidate合同 | controller跨row扩张canonical predicate；root0 | Planner/Executer |
| `REF-P7-25-R2-B1A-C3E3` | `REJECTED_CORRECT_HARD_FAILURE` | machine-owned per-row parse policy后执行同一candidate合同 | patch argv漏`--full-index`且evidence过早pass | Planner/Executer |
| `REF-P7-25-R2-B1A-C3E4` | `REJECTED_FIRST_REAL_FOCUSED_FAILURE` | machine-owned exact patch argv与post-aggregate status后完成同一candidate合同 | 102 tests / 3 failures / 66 fixture errors | Planner/Executer |
| `REF-P7-25-R2-B1A-C3E5D1` | `ACCEPTED_FAIL_CLOSED_DECOMPOSITION` | exact external fixtures + three-failure bounded diagnostic/correction | historical2 pass；唯一checkout test fail | Planner/Executer |
| `REF-P7-25-R2-B1A-C3E5D2` | `REJECTED_CHECKOUT_FIX_ACCEPTED` | single test-only checkout correction + exact3/focused | checkout exact3 pass；focused ambient-HEAD defect | Planner/Executer |
| `REF-P7-25-R2-B1A-C3E5D3` | `ACCEPTED_TEST_ONLY_PASS` | retain checkout edit + explicit checkpoint lineage-test owner | targeted2/2 focused102/102 | Planner/Executer |
| `REF-P7-25-R2-B1A-C3E6F1` | `REJECTED_FULL_HERMETICITY` | new exact five-path candidate focused/full/commit/subordinate seal | focused102 pass；full664有18 input errors | Planner/Executer |
| `REF-P7-25-R2-B1A-C3E6F2` | `REJECTED_TARGETED_EXTERNAL_INPUT_AND_PROVENANCE_OWNER` | exact white-LUT fixture + one raw-shutter fake-backend test correction | raw-shutter test pass；targeted134 errors20 | Planner/Executer |
| `REF-P7-25-R2-B1A-C3E6F3` | `REJECTED_PRE_ACQUISITION_READ_ORDER` | one-path test prerequisite commit + immutable successor provenance seal | root0；两次budgeted read早于evidence persistence | Planner/Executer |
| `REF-P7-25-R2-B1A-C3E6F4` | `REJECTED_MACHINE_ROW_PARSER` | acquisition-first one-path test prerequisite + successor seal | root0；bare marker未匹配反引号row | Planner/Executer |
| `REF-P7-25-R2-B1A-C3E6F5` | `REJECTED_CLOSURE_AST_PREDICATE` | exact-row acquisition-first prerequisite + successor seal | 4/5 acquisition；BinOp误用literal_eval | Planner/Executer |
| `REF-P7-25-R2-B1A-C3E6F6` | `REJECTED_FULL_SUBSET_SHAPE` | structural-AST acquisition-first prerequisite + successor seal | 12/12 matched；错误whole-object equality | Planner/Executer |
| `REF-P7-25-R2-B1A-C3E6F7` | `REJECTED_IGNORE_PRESENTATION_BINDING` | FULL-subset structural-AST prerequisite + successor seal | observed2/5；错误绑定.gitignore行号 | Planner/Executer |
| `REF-P7-25-R2-B1A-C3E6F8` | `REJECTED_CLOSURE_OWNER_PATH` | semantic-ignore structural-AST prerequisite + successor seal | acquisitions5/5；错误measurement路径 | Planner/Executer |
| `REF-P7-25-R2-B1A-C3E6F9` | `REJECTED_TRACKED_TARGET_EXCLUSIVE_CREATE` | exact-owner semantic-ignore prerequisite + successor seal | acquisitions5/5；O_EXCL existing target | Planner/Executer |
| `REF-P7-25-R2-B1A-C3E6F10` | `REJECTED_NESTED_CLOSURE_AST_SHAPE` | atomic-replacement prerequisite + successor seal | atomic replace passed；flat BinOp predicate rejected real nested chain | Planner/Executer |
| `REF-P7-25-R2-B1A-C3E6F11` | `REJECTED_CONTROLLER_LIFECYCLE_AND_ACCOUNTING` | exact nested-AST prerequisite + successor seal | KeyError；same-root retry；5 reads与zero counters矛盾 | Planner/Executer |
| `REF-P7-25-R2-B1A-C3E6F12` | `REJECTED_WORKTREE_BLOB_ORACLE_FALSE_REJECTION` | direct-root single-controller prerequisite + truthful accounting | atomic replace exact；index parent blob误作worktree blob | Planner/Executer |
| `REF-P7-25-R2-B1A-C3E6F13` | `ACTIVE` | split index/worktree blob identity prerequisite + successor seal | C3E6F12 review archive SHA 81ddc4ce；matching PLAN active | Planner/Executer |
| `REF-P7-25-R2-B2` | `ACTIVE_CORRECTED_PATH_WAITING_PLAN_ONLY_ACTIVATION_FREEZE` | 由accepted C1 exact path-owner index驱动modern immutable subordinate manifest v2 | C1 path-owner index accepted | Planner/Executer |
| `REF-P7-25-R2-B2-C1` | `ACCEPTED_COMPLETE` | 只验证exact retained directory chain及artifact name/type/path | B2 wrong frozen path failure | Planner/Executer |
| `REF-P7-25-R2-B3` | `BLOCKED` | Manifest自校验后执行postcommit focused、durable full、synthetic terminal/replay | `REF-P7-25-R2-B2` accepted | Planner/Executer |
| `REF-P7-25-R2-B4` | `BLOCKED` | 对原retained R3三件套做首次真实audit并由canonical validator唯一判定eligibility | `REF-P7-25-R2-B3` accepted | Planner/Executer |
| `REF-P7-25-R2-B5` | `BLOCKED` | 独立验收validated-unconsumed状态、manifest与rollback provenance | `REF-P7-25-R2-B4` pass | Planner/Orchestrator |
| `REF-P7-25-R2-BR` | `SUPERSEDED_BY_HUMAN_GOVERNANCE_OVERRIDE` | exact two-path与canonical validator manifest seam合同矛盾 | Human将工程owner交Orchestrator | Orchestrator |
| `REF-P7-25` | `BLOCKED_ON_OPTION_B_ENGINEERING_SEQUENCE` | 唯一 successor R3 lineage release总体任务 | `REF-P7-25-R2-B5` accepted | Planner |
| `REF-P7-26` | `BLOCKED` | Fresh predevice oracle | `REF-P7-25` | Planner/Executer |
| `REF-P7-27` | `BLOCKED` | Fresh real zero/readiness gate | `REF-P7-26` | Planner/Executer |
| `REF-P7-28` | `BLOCKED` | Fresh E2 | `REF-P7-27` | Planner/Executer |
| `REF-P7-29` | `HUMAN_CHECKPOINT` | 单独确认一次 Ray R6 formal launch | `REF-P7-28` | Human |
| `REF-P7-30` | `LOCKED` | 完整新 Ray R6 16-frame acquisition | `REF-P7-29` | Planner/Executer |
| `REF-P7-31` | `BLOCKED` | Ray-only R6 TD-B analyzer gate | `REF-P7-30` 16/16 | Planner |
| `REF-P7-32` | `BLOCKED` | 新 strip TD-B 独立 planning gate | `REF-P7-31` history pass | Planner |
| `REF-P7-33` | `LOCKED` | 新 strip TD-B 16-frame acquisition | `REF-P7-32` | Planner/Executer |
| `REF-P7-34` | `BLOCKED` | Strip-only TD-B analyzer gate | `REF-P7-33` 16/16 | Planner |
| `REF-P7-35` | `BLOCKED` | Combined TD-B operational-600 analyzer与 envelope v3 | `REF-P7-31` + `REF-P7-34` pass | Planner |
| `REF-P7-05` | `BLOCKED` | TD-B 科学验收与 operating-envelope freeze | `REF-P7-35` | Planner |
| `REF-P7-36` | `CONDITIONAL` | EQ-R6 ordinary code-defect offline correction | `REF-P7-23=run_invalid` | Planner |
| `REF-P7-37` | `ADVISOR_DECISION` | `exposure_window_unresolved` 新 exposure 方向 | `REF-P7-23` unresolved | Advisor |
| `REF-P7-38` | `ADVISOR_DECISION` | Ray R6 history-model required | `REF-P7-31` history fail | Advisor |
| `REF-P7-39` | `ADVISOR_DECISION` | Strip 需要改变 frozen scientific contract | `REF-P7-33/34` contract stop | Advisor |
| `REF-P7-06` | `CONDITIONAL` | H0 full-scale vs 3072 thermal diagnostic | 新 GUIDE 明确重开 | Advisor/Planner |
| `REF-P7-08` | `LOCKED` | TD-C operational-600 order-balanced core | `REF-P7-05` pass | Planner |
| `REF-P7-09` | `LOCKED` | TD-C endpoint expansion | `REF-P7-08` accepted | Planner |
| `REF-P7-10` | `BLOCKED` | Reference epoch 分类与 P6 compatibility | TD-C required scope complete | Planner |
| `REF-P7-11` | `CONDITIONAL` | 7-point / 13-node Ray requalification | reference branch B/C | Advisor |
| `REF-P7-12` | `ADVISOR_DECISION` | Thermal/reference AUDIT PACK 与 sentinel 解锁 | reference class explainable | Advisor |
| `REF-P7-13` | `LOCKED` | 四点 sentinel v2 | Advisor explicit release | Planner |
| `REF-P7-14` | `LOCKED` | Remaining 9 INT100 pilot points | sentinel accepted | Planner |
| `REF-P7-15` | `LOCKED` | Full-scale boundary 与 scale-relaxed diagnostics | 13-point pilot accepted | Planner |
| `REF-P7-16` | `LOCKED` | P7 independent holdout 与 runtime gamut semantics | boundary evidence | Planner |
| `REF-P7-17` | `ADVISOR_DECISION` | P8 entry review | P7 holdout accepted | Advisor |
| `REF-P8-01` | `LOCKED` | INT dimension acquisition/model/holdout | Advisor P8 release | Planner |
| `REF-G6-01` | `ADVISOR_DECISION` | Gate-6 candidate/product freeze | P8 accepted or range restricted | Advisor/Human |
| `REF-P9-01` | `LOCKED` | Immutable final independent validation | Gate-6 freeze | Planner |
| `REF-G7-01` | `ADVISOR_DECISION` | Gate-7 technical delivery | P9 complete | Advisor |
| `REF-OPS-01` | `HUMAN_DECISION` | Install、smoke test、rollback 与交付 | Gate-7 | Human |
| `REF-CLOSE-01` | `BLOCKED` | Final AUDIT PACK 与路线关闭 | delivery result | Planner/Advisor |
| `REF-CCT-01` | `DEFERRED` | 完整 CCT/GM P5 候选 | 新 Advisor/Human reopen | Advisor/Human |
| `REF-ABBA-01` | `DEFERRED` | Classic ABBA mini-run | drift assumptions proven | Advisor |
| `REF-P6-FULL-01` | `DEFERRED` | 完整 P6 106-point re-capture | 7/13-point evidence | Advisor |
| `REF-LUX-01` | `DEFERRED` | 绝对照度复制 | 新 metrology GUIDE | Advisor/Human |

主依赖链：

```text
REF-P7-18 -> 19 -> 20 -> 21 -> Human 22 -> EQ 23
-> final policy/checkpoint 24 -> R3 release 25
-> predevice 26 -> zero/readiness 27 -> E2 28
-> Human 29 -> Ray R6 30 -> Ray analyzer 31
-> strip独立planning 32 -> strip 33 -> strip analyzer 34
-> combined 35 -> TD-B freeze 05
-> TD-C 08 -> optional endpoints 09 -> reference 10
-> Advisor 12 -> sentinel 13 -> remaining 14 -> boundary 15 -> holdout 16
-> P8 review 17 -> P8 -> Gate-6 -> P9 -> Gate-7 -> Human delivery -> close
```

任一箭头只是依赖，不是自动续跑。

## 5. 已完成的 R5 disposition 与 pre-EQ offline preparation baseline

### REF-P7-18：完整 pre-EQ offline preparation umbrella

**状态：** `COMPLETED`

**最新 execution disposition：** `integrated_validation_failure`。实现回归与 synthetic matrices通过，但
首次 evidence seal 至少有两项必须由 Planner 一并裁决：

1. `terminal-summary.json.artifact_count=12`，实际 root 有 `13` 个 JSON；
2. `validation-summary.json.status=fail` 且 `secret-path-scan.json.status=fail`，finding 为源码字面量
   `private_override_name`。Executer handoff 误写为 secret/path scan通过，并误称 validation summary
   自报 pass；后续不得把纠偏缩成单纯 artifact index重建。

### REF-P7-18-C1：pre-EQ evidence scan/index/handoff accuracy 纠偏

**状态：** `COMPLETED`

**目标：** 保留首次实现与 immutable evidence，建立 baseline-aware secret/path scan、canonical
13-artifact phase owner和 machine-derived truthful handoff；不得改变任何科学合同。

**实现与证据：**

- 首次 root和 R5 root前后 whole-tree完全不变；
- 区分 baseline identifier name 与新 credential/value/path/network target；只有 exact baseline
  name 可分类为 non-secret，所有真实 value、`.env` serialization、网络 target与越界路径继续 fail closed；
- 新 correction root只创建一次，按 10 payload + strict audit + validation summary + terminal summary
  的 phase顺序形成 exact 13 JSON；
- terminal self hash由外部 handoff持有，避免递归自引用；
- summary、terminal与 handoff任一状态不一致即失败；
- 通过 focused/full/static/adversarial验证后才允许严格逐路径 focused checkpoint commit。

**安全边界：** pure offline；device/network/.env/camera/light/all_off/release/EQ/formal/strip/TD-C全为0。

**失败与 stop：** 任一 scan、index、truthfulness、immutability、test或stage scope失败即停 Planner；
成功也只回 Planner验收，不自动解锁 `REF-P7-22`。

**目标：** 按 4.GUIDE §16 形成唯一 pre-EQ offline preparation package。未来 Planner 可让一个 active PLAN
引用 `REF-P7-18`，并在同一 package 内按顺序完成本节的 R5 disposition、`REF-P7-19` exposure/EQ owner、
`REF-P7-20` R6/analyzer/lock owner和 `REF-P7-21` integrated validation/checkpoint；任何子合同失败立即停，
不得跳到后续子合同或设备。`REF-P7-19..21` 保留独立 ID 便于逐项验收和失败分支追踪，不要求四次独立执行。

本节第一子目标是把 4.GUIDE 的 R5 决策落实为独立、非授权 derived diagnostic 和机器可判定 schema，同时保持
R5 root byte-immutable。

**实现轮廓与 owner：**

- 复用 `analyze_p7_thermal_diagnostics.py`、既有 exact 58-feature owner 和 R5 evidence reader；不得创建平行 analyzer。
- 在 R5 root 外的新 derived root 生成 `r5-partial-diagnostic-analysis-v1.json`。
- 固定：

```text
r5_failure_class = state_specific_exposure_policy_failure_with_required_feature_observer_saturation
r5_capture_011_quality = invalid
r5_formal_pass = false
retained_11_use = diagnostic_only
retained_11_formal_inference = prohibited
old_new_frame_combination = prohibited
formal_authorizing = false
incomplete_sequence = true
missing_slots = [011,012,013,014,015]
```

- 允许报告 retained 11 的 exposure、chronology、command 和 quality 描述；禁止输出 TD-B pass、
  history compatible、operating-envelope freeze 或 product LUT。
- 明确 R5 clipping 与早期 6-feature low-signal failure 是不同事件。

**安全与权限：** 纯离线、R5只读；device/network/camera/light/release/public formal analyzer/commit 均不得由本 task 推导。

**必要证据：**

- R5 root pre/post manifest 与关键 hash 相同；
- derived artifact path/bytes/SHA；
- missing slots、formal-authorizing、pooling prohibition 字段；
- negative fixtures：R5 root rewrite、011 feature ingestion、formal pass、history pass、old/new pooling 均 fail closed。

**验收：** 分类 exact；011 不进入 vector/center/covariance/history；retained 11 仅 diagnostic；R5所有原始文件不变。

**失败与 stop：** 任一 source hash、schema 或 negative fixture 不通过即停 Planner；不得修 R5 root。若同一 active PLAN
明确包含 `REF-P7-19..21` 子合同且本节全部通过，可继续纯离线子步骤；不得创建 EQ root、生成 final release或访问设备。
整个 package 最终只交 Planner review。

### REF-P7-19：Exposure policy v2 与 EQ-R6 runner/validator

**状态：** `COMPLETED`

**依赖：** `REF-P7-18` accepted。

**目标：** 建立 state-C successor exposure policy、两档固定资格 sequence 和 fail-closed quality/physical accounting。

**实现轮廓与 owner：**

- 新 artifact：`config/hsi/p7-ray-td-b-exposure-policy-v2.json`。
- 扩展现有 `p7_thermal_diagnostics.py` plan/schema owner、
  `measure_p7_thermal_diagnostics.py` capture/scheduler/physical-return owner和 `hsi_objective.py` required-feature reader；
  不创建平行 runner。
- A/D/B 从 R5 `plan.json` 和 frozen-shutter hash exact copy：
  A `1/5000`、D `1/6400`、B `1/8000`；ISO `100`、aperture `implicit auto`。
- C 初始为：

```text
status = pending_qualification
candidate_1 = 1/2500
candidate_2 = 1/3200
formal_shutter = null
```

- policy 必须绑定 R5 superseded hash、feature/observer/quality/operating-envelope hashes、Canon MakerNote actual exposure owner。
- EQ plan：

```text
experiment = P7-TD-B-RAY-C-EXPOSURE-QUAL-R6
source = Ray only
formal = 0
ambient = 0
strip = zero
slots = [60,120,300,600]
candidate physical = 4
total physical cap = 8
retry = 0
```

- 每 candidate sequence：strip zero → A H120/S100/INT100 600s → A→C H300/S100/INT100 →
  C 60/120/300/600 → Ray off → 双源 zero。
- A precondition 本身不拍 CR3，但 command、readback、chronology和600秒等待必须写 ledger。
- 未来 active PLAN 必须冻结 candidate-specific exact capture IDs；Executer不得现场命名或推导。
- candidate 1：
  - 4/4 pass：选择 1/2500，不运行 1/3200；
  - 任一 slot 仅 clipping failure：立即结束当前 candidate，不补其剩余 slot；完成 cleanup/final-zero 后允许 1/3200；
  - low-signal/nonfinite/valid-pixel/metadata/isolation/readback/cleanup 任一失败：停止，不运行 candidate 2。
- candidate 2：4/4 pass 才选择 1/3200；任一 required failure 为 `exposure_window_unresolved`。
- 禁止 1/4000、1/5000、自动搜索、auto exposure、weak reacquire 或现场增加 candidate。

**必要测试：**

1. R5 clipping exact 分类；
2. 任一 required feature nonzero clipped fraction hard-fail；
3. required feature 无法删除；
4. 只有 1/2500 clipping 才可进入 1/3200；
5. 1/2500 非 clipping quality failure 直接停；
6. candidate ≤2、setup physical ≤8；
7. selected candidate 必须 4/4；
8. A/D/B 与 R5 exact hash一致；
9. EQ formal count/ambient/retry 均0；
10. candidate 间必须双 cleanup/final-zero；
11. MakerNote recorded exposure与 nominal ratio gate；
12. strip zero generation/readback；
13. run-invalid evidence 与 same-root continuation prohibition；
14. signal/terminal accounting；
15. R5 sealed 不变。

**安全与证据：** 本 task 只实现 fake/offline fixtures；真实 EQ 未授权。保存 policy candidate、dry plan、matrix、negative fixtures、
source hashes 和 exact test counts。

**验收与 stop：** 所有 offline/fake paths pass 后回 Planner；不创建真实 EQ root、不访问设备、不生成 successor release。
EQ fake 4/4 只证明 exposure eligibility，不证明 state C settled、TD-B pass或history compatible。

### REF-P7-20：Full Ray R6 plan/validator、analyzer 与 downstream locks

**状态：** `COMPLETED`

**依赖：** `REF-P7-19` accepted。

**目标：** 在设备前冻结完整新 R6、Ray return-history analyzer、strip/TD-C locks 和 old/new pooling prohibition。

**实现轮廓与 owner：**

- 扩展同一 `p7_thermal_diagnostics.py` plan owner与 `analyze_p7_thermal_diagnostics.py::analyze_td_b`；
  复用 `frozen_same_state_compatibility`，不得创建第二套 compatibility/analyzer。
- R6 experiment：

```text
P7-TD-B-RAY-OP600-EXPOSURE-GUARDED-FORMAL-R6
Ray only
strip zero
ambient 0
formal logical = 16
formal physical cap = 16
setup in formal root = 0
launch = 1
retry = 0
```

- Exact capture IDs/order：

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

- A/D/B exact R5 shutters；C 必须引用 EQ selected policy；formal auto exposure、weak reacquire、mid-run shutter change 禁止。
- 每 capture accepted 前验证 CR3/sidecar/remote IDs/MakerNote exposure/state/readback/strip zero/58 features/
  zero clipping/near-noise/finite/valid pixels/timing/no-stale/budget。
- 任一 capture failure：accepted hard-failed、formal pass false、strip0、retry0。
- Ray analyzer 只有 16/16 才运行：
  - 比较 A0/A_after_D/A_after_B/A_after_C；
  - 四 anchor 同一 frozen joint coverage；
  - D/B/C trend、dominance、方向全部保留；
  - `trend>4` 表示未 settled，但不单独否定 fixed-600 endpoint；
  - blocking 为 capture invalid、A history fail、previous-state/elapsed invalid、source/cleanup/readback failure。
- schema 区分：

```text
steady_status = not_demonstrated
operational_endpoint_600_valid = true|false
time_dependent_within_600 = true|false
```

- 所有 pre-EQ、EQ、R6、strip和combined artifacts必须能归一到以下机器状态：

```json
{
  "r5": {
    "failure_class": "state_specific_exposure_policy_failure_with_required_feature_observer_saturation",
    "formal_pass": false,
    "retained_11_use": "diagnostic_only",
    "old_new_combination": "prohibited"
  },
  "exposure_qualification": {
    "status": "pending|qualified_1_2500|qualified_1_3200|exposure_window_unresolved|run_invalid",
    "slots_s": [60, 120, 300, 600],
    "physical_cap": 8
  },
  "ray_r6": {
    "formal_planned": 16,
    "formal_accepted": 0,
    "retry": 0,
    "return_anchor_history": "not_evaluated|pass|fail"
  },
  "operating_envelope": {
    "dwell_s": 600,
    "claim": "selected_fixed_time_transient_not_proven_steady",
    "steady_status": "not_demonstrated"
  },
  "locks": {
    "strip": "blocked_until_ray_r6_pass",
    "td_c": "blocked_until_combined_td_b_pass",
    "sentinel": true,
    "p8": true
  }
}
```

- old R5 11 与新 R6 frame pooling 必须被 validator 拒绝；R5 只能 immutable manifest reference。
- Ray pass 只可解锁新 strip，不可解锁 TD-C/sentinel。

**必要证据与测试：**

- exact 000..015 order、no skip/resume/mid-run change；
- 8 setup + 16 formal physical ledgers跨实验分离，总 cap 24；
- formal failure后 strip call count 0；
- analyzer 16/16 prerequisite；
- history pass/fail fixtures；
- trend vs operational endpoint semantic separation；
- old/new pooling negative；
- R5 sealed；
- Python/shell cleanup、final zero、terminal launch/retry accounting；
- strip/TD-C/sentinel/P8 lock tests。

**失败与 stop：** offline contract/fixture 任一不通过即停 Planner。不得创建设备 root、run analyzer on R5 或生成 release。

### REF-P7-21：Pre-EQ integrated validation 与 implementation checkpoint

**状态：** `COMPLETED`

**依赖：** `REF-P7-18..20` 全部 accepted。

**目标：** 对 pre-EQ implementation 做一次完整集成验证并创建明确 checkpoint；C formal shutter 仍为 null。

**验证合同：**

```text
focused tests with exact count
full suite with exact count
compileall
all wrapper/launcher syntax
public validator positive/negative fixtures
git diff --check
CodeGraph sync
secret/path scan
R5 immutable replay
pre-EQ checkpoint commit
```

**Planner 必须在 active PLAN/回报中回答：**

1. 哪些文件实现 exposure-policy v2；
2. A/D/B exact R5 shutter artifact/hash；
3. nominal 与 MakerNote actual exposure绑定；
4. EQ A→C scheduler；
5. 4-slot gate；
6. clipping 与 low-signal不同分支；
7. setup/formal ledgers；
8. pooling prohibition；
9. R6 IDs；
10. fixed shutter/no-reacquire；
11. post-EQ release/readiness顺序；
12. visible-Terminal launch owner；
13. A return history analyzer；
14. trend/operational endpoint语义；
15. strip条件分支；
16. combined pass/fail；
17. TD-C operational-600 scope；
18. sentinel/P8 locks；
19. cleanup/final-zero/terminal seal；
20. artifact paths/hashes/exact test counts。

**验收：** working tree只有该离线 implementation scope；checkpoint exact；R5 root、R2 release、GUIDE和audit不变；
policy C status仍 pending；没有 successor release。

**失败与 stop：** 任一验证失败返回 bounded offline correction；不得申请 EQ。Planner接受后才进入 Human `REF-P7-22`。

## 6. EQ-R6 exposure qualification

### REF-P7-22：Human EQ-R6 checkpoint

**状态：** `COMPLETED`

**依赖：** `REF-P7-21` accepted；已满足。

**请求必须精确说明：**

- experiment `P7-TD-B-RAY-C-EXPOSURE-QUAL-R6`；
- 只允许 Ray A→C，strip始终0，formal0、ambient0；
- candidate 1/2500，只有 clipping 才可进入 candidate 1/3200；
- maximum CR3 8、retry0；
- 每 candidate 约 A600 + C600 的连续灯光窗口；若两档均运行，总窗口按两条独立 sequence 计算；
- 新 unique root、visible Terminal、abort、Python/shell cleanup、independent final-zero、terminal seal；
- 不授权 full R6、strip、TD-C、release或更快 shutter。

**证据：** Human exact response与允许的 experiment/budget/stage写入未来 PLAN；不得将先前通用“允许调用设备”改写为
无界连续实验授权。

**完成证据：** Human 已逐字确认 exact candidate、budget、duration 与 cleanup/seal边界；archive
`.agent-work/PLANS/20260727-1324-p7-eq-r6-human-checkpoint-live-owner-review.md`，SHA-256
`9a8f959d9a471a9226a26ac829272665df88f8c6a0ffe70a690fb9cef88138a6`。科学边界不变时不得重复询问。

### REF-P7-23-C0：EQ-R6 live owner pre-execution correction

**状态：** `REJECTED_ACCEPTANCE_BLOCKING`

**目标：** 在 pure-offline package内把现有 `offline_contract_only` EQ plan接入 production CLI、single-candidate
wrapper lifecycle与 outer conditional owner；只用 injected fake/adversarial adapters验证，真实设备调用为0。

**实现边界：**

- 复用现有 thermal plan、camera backend、physical-return ledger、cleanup与wrapper owners，不建parallel runner；
- 每个 candidate是独立 wrapper lifecycle，candidate 1 complete cleanup/final-zero/seal后，只有
  clipping-only分类才能启动 candidate 2；
- 建立 immutable launch ledger、progressive evidence、physical-return-before-processing、terminal seal和
  visible-Terminal兼容接口；
- 保持 candidate、IDs、shutter、slots、cap、retry、quality与科学语义全部不变；
- focused/full/adversarial/static验证全过后只提交允许路径，随后停 Planner review。

**安全：** device/network/.env/camera/Ray/strip/light/real cleanup/capture/release/EQ launch/formal/TD-C全为0。

**失败与 stop：** 任一 ownership、fake lifecycle、evidence、test或commit scope失败立即停 Planner；不得现场
启动EQ。成功也必须由Planner验收后另写 `REF-P7-23` execution PLAN。

**Orchestrator review findings：**

- launch ledger validator未把 `outer_pid`、`wrapper_pid` 与 exact argv绑定到 expected runtime owner；
  这三个字段分别被安全值改写后仍通过验证，违反 immutable/tamper/rebinding合同；
- wrapper subprocess返回但缺少 `wrapper-result.json` 时，outer owner在调用 independent final-zero前抛错；
  实测 final-zero call count为0，违反异常路径cleanup/final-zero要求；
- C0 evidence matrix将上述 tamper/failure分支写为pass，但测试只覆盖 source hash tamper、second write/private
  argv及常规 wrapper runtime，没有覆盖这两个实际缺口。

因此 C0 checkpoint不得作为真实设备入口。Planner已拒绝并归档：
`.agent-work/PLANS/20260727-1401-p7-eq-r6-c0-rejection-review.md`，SHA-256
`804245bb5886fef09f99d44654d9c1779e114a4388e752504ec92264bb3b8f1e`。

### REF-P7-23-C1：EQ-R6 runtime binding 与 all-path final-zero correction

**状态：** `REJECTED_TERMINAL_EVIDENCE_ABSENT`

**目标：** 基于 C0 commit只修 measurement runner内的 runtime binding和 outer failure finalization边界，
不改变scientific/live activation contract。

**实现与验收：**

- launch ledger绑定 expected outer/wrapper/runner PID与 ordered exact argv；append/remove/reorder/replace安全flag
  及任一PID rebinding均在adapter前拒绝；
- candidate entry与terminal seal两次复用同一binding validator，并把wrapper-result/candidate-result runtime
  ownership、run_dir与ledger逐项交叉验证；
- 对subprocess exception/nonzero、missing/malformed/tampered artifact、seal failure、KeyboardInterrupt、
  SystemExit及final-zero自身失败，每个attempted launch都恰好一次best-effort final-zero；
- outer-owned durable failure evidence同时保留primary、final-zero、seal/evidence failure，原BaseException保持
  non-success并重新抛出，candidate2 launch为0；
- fresh adversarial matrices、focused/full/static/zero counters与唯一C1 evidence root全过后，才允许两文件
  allowlist的focused commit。

**安全：** pure offline；device/network/.env/backend/camera/Ray/strip/real all_off/capture/EQ root/release均0。

**失败与 stop：** 任一binding、final-zero、evidence、test或commit gate失败即停Planner；成功仍须Planner验收
并另写真实 `REF-P7-23` PLAN。

**最新 execution disposition：** runtime-binding `12/12`、final-zero `13/13`、focused `161/161`、
full `622/622`与commit `93e72b833c2ebefb6cdcfe05dd996a9ae4fc97e8`均存在；但唯一C1 evidence
root在任何JSON写入前因planned canonical order自检失败，现为空目录（canonical JSON `0`），validation/
terminal均不存在。Executer正确未修补、未重建。C1整体必须由Planner拒绝或转入新的只证据纠偏，不能凭
代码/测试green解锁设备。

Planner已拒绝C1整体并归档：
`.agent-work/PLANS/20260727-1424-p7-eq-r6-c1-evidence-failure-review.md`，SHA-256
`0a8c208eb32e94ce4777d9a8cf8a81f0110356532bf30e879f31023fd6d1bcc5`；commit `93e72b8`
保留为immutable implementation candidate。

### REF-P7-23-C1E1：C1 immutable evidence seal correction

**状态：** `ACCEPTED_COMPLETE`

**目标：** 不改source/test、不commit，只读重放C1 implementation与historical roots，在创建新root前先于内存
验证single ordered artifact owner，再一次性生成truthful 12-artifact C1 evidence seal。

**合同：**

- failed C1 empty root保持0 entries，canonical manifest digest
  `52378315a05a2b72d990aeace832287ce3a5dfe28c2ab1b37abe72ac43f2abf9`；
- C0 root与空C1 root before/after immutable；
- fresh运行runtime binding `12 + positive`、final-zero `13`及focused/full/static回归；
- exact writer order：9 payload → strict preterminal audit → validation → terminal；
- validation只索引前10，terminal引用前11且不自嵌hash，外部handoff持terminal hash；
- 新C1E1 root只创建一次；任何write/count/hash错误不得修补、重建或另建替代root。

**安全：** source/test edit=0、commit=0；device/network/.env/backend/camera/light/real all_off/capture/EQ/
release=0。

**失败与 stop：** 任一pre-root gate、test、immutability、writer order、summary或seal失败即停Planner；
成功仍须Planner验收后才能另写真实execution PLAN。

**最新 execution disposition：** 新C1E1 root
`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-eq-r6-c1e1-offline/e1-93e72b8-20260727T1424`
已一次性形成exact 12 JSON；runtime binding negative `12/12`、final-zero `13/13`、EQ contract
`49/49`、focused `161/161`、full `622/622`全部通过。validation SHA-256
`b670f74df58d81a952dcd1628be098449e841bedbe1ee29226922e6c13ad1703`，terminal SHA-256
`7e9ec5ea118dd8b67c83f213913e03fc7e2765154c86c8c6b4c98e75c3e2b680`；所有mismatch数组为空，
C0与失败空C1 root before/after一致，device/network/EQ/release调用均为0。Orchestrator独立重放了
strict JSON、artifact count/hash、historical manifests和side-effect accounting；现只等待Planner正式接受或拒绝。

Planner已正式接受C1E1并归档：
`.agent-work/PLANS/20260727-1445-p7-eq-r6-c1e1-acceptance-review.md`，SHA-256
`d78c3321f989e75f4f22bfd35e099e5c4dab025ee3e76a2b3b908318aa1e190e`。`REF-P7-23-C1`由C1E1
补齐证据后接受，`REV-EQ-R6-C0-001/002`关闭；accepted execution checkpoint为
`93e72b833c2ebefb6cdcfe05dd996a9ae4fc97e8`。

### REF-P7-23：EQ-R6 state-C exposure qualification

**状态：** `BLOCKED`

**依赖：** C1E1 accepted + 唯一 active PLAN；Human checkpoint已满足。

**最新 execution disposition：** Executer在进入任何设备/网络readiness或Terminal dispatch前确认，production
CLI虽有EQ outer/candidate入口，但没有active PLAN §5要求的single prelaunch/readiness/ordered cleanup/
nine-artifact failure-seal owner。为避免现场heredoc形成第二套高风险状态机，已fail closed：
`dispatch=0`、`FAMILY/PRELAUNCH/RUN`创建均为0，唯一root仍不存在；未新增device/network probe。
完整handoff见 `EXECUTION_RESULT.md` §139，文件SHA-256
`a0b94720f8d89f245f9ad0ae78968f5c2baa74c46bee828ce01a2088e6a9461f`。Human确认未消费且继续保留。
该次历史失败随后由C2/C2E1/C2E2纠偏关闭；它不能被解释为曾经允许绕过prelaunch直启outer。

**最新 live activation disposition：** static preflight invocation1 pass；production prelaunch invocation1
exit1。camera与Ray readiness pass，但strip `.local` resolve timeout导致Python cleanup、shell cleanup与
independent final-zero均fail。exact 9 artifacts已封存于
`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-exposure-qual-r6-0f36671-20260727T1601/prelaunch`；
terminal SHA-256 `f9f106652c32a506772f676175d60d317f3d5137a1891072b9ca448d1ec9bd02`，
manifest SHA-256 `1cc926a0b0212fa2c350cf50ad8863ad5c1741b9f3bb25c9694253b273d48dd4`，
二者status fail。RUN absent、dispatch/candidate/capture/CR3=0、Human确认未消费，无额外probe或retry。
Orchestrator独立确认9/9 strict、引用hash闭合与失败stage一致。当前只允许Planner branch D review。

**当前 fresh live 1650 runtime：** 在H1/R2恢复后，fresh FAMILY
`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-exposure-qual-r6-0f36671-20260727T1650`的static preflight、
production prelaunch、600秒内handoff validation均pass；outer argv SHA-256
`0009b21f2cebc0b73bec750e4fc1234405b701fe8ee723c52b0d58ae31153b89`。visible Terminal dispatch
attempted1，Human confirmation consumed。真实owner PID `61224`、PPID `61223`、Terminal window
`284793`、tty `/dev/ttys006`。L1/L2/L3（22:57:37Z / 23:01:39Z / 23:05:52Z）均单实例alive、无duplicate，
仍处candidate-1 A600 wait；RUN live-plan SHA `32abfa09…abcf9`、candidate-1 ledger
`8e1d1435…02a9`。candidate1-only ETA约23:21Z，clipping branch约23:46Z。heartbeat automation
`formal-r5-terminal-review`已更新为“EQ-R6 1650 terminal review”，每10分钟只读唤醒；禁止dispatch/retry/
device probe/cleanup/analyzer。L1的front-tab误识别`284096/ttys002`已由L2/L3的OS tty+Terminal枚举纠正，
dispatch count仍为1。

**1650 terminal disposition：** outer PID `61224`已terminal、owned residual0。Candidate-1只capture一次并
physical return1；唯一CR3/sidecar path、bytes、SHA-256、remote capture/request IDs均完整，Python/shell
cleanup、independent final-zero与terminal seal通过。RAW report本身quality accepted：
`92` accepted features、0 rejected、23 patches；但runner把完整92项直接与冻结58项policy tuple比较，未先
按policy IDs筛选/重排，造成missing0、extra34及首项expected `block_03::G1` / actual `block_02::R`。
classification=`runtime_contract_failure_feature_selection_order_owner`，属于branch D implementation
failure，不是clipping-only，candidate-2 launch0、retry0。另有progressive accounting gap：
`candidate-failure.json physical_returned=0`，而result/seal/physical ledger权威计数为1。1650 family必须
immutable；在Planner验收离线纠偏前不得1/3200、fresh live、formal或public analyzer。

Planner已判定`REF-P7-23=REJECTED_BRANCH_D_RUNTIME_FEATURE_SELECTION_CONTRACT`，打开
`REV-EQ-R6-FEATURE-001`与`REV-EQ-R6-PHYSICAL-FAILURE-002`。1650 immutable，candidate2 locked；
Human EQ authorization已由outer dispatch消费，future live不得自动延续。归档：
`.agent-work/PLANS/20260727-1721-p7-eq-r6-live-1650-runtime-contract-failure-review.md`，SHA-256
`868d6d17d53235d1224918173d5fb3a18df0f2af412fd43420c6d4dd02c62432`。

### REF-P7-23-C3：feature-selection与physical-return accounting correction

**状态：** `REJECTED_PLAN_PATH`

**目标：** pure offline exact两文件修复。single feature-selection helper将完整observations建unique map，
按frozen 58 IDs filter并依policy order输出；single strict physical-ledger count owner在cleanup后一次写failure，
使failure/result/seal/ledger一致。

**验收与边界：** failing-first 6 methods，post-fix `6/6`、R6 file `61/61`、focused 4 files无fail/skip、
full `634/634`，compileall/CodeGraph/diff；commit cap1 exact两paths，message
`fix(p7): select eq-r6 policy features atomically`。Evidence root
`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-eq-r6-c3-offline-0f36671-20260727T1721` one owner/root1、
exact12 non-circular seal，1650 whole-tree before/after identical。network/device/`.env`/capture/EQ/analyzer0。

**最新 execution disposition：** 两文件实现后exact-six `6/6`、R6 file `61/61` pass，1650 manifest
unchanged，C3 evidence root仍absent。但PLAN focused路径写为不存在的
`tests/test_measure_p7_thermal_diagnostics.py`，实际tracked file为`tests/test_p7_thermal_diagnostics.py`；
loader error按PLAN test failure stop。full/commit/evidence owner/root均0，无device/network/`.env`调用。
当前只允许Planner归档并写exact-path successor；不得Executer自行替换路径继续。

Planner已拒绝C3，唯一原因为PLAN focused path mismatch；implementation candidate与recorded failing-first
`1 pass / 2 failures / 3 errors`保留，不revert/restart。归档：
`.agent-work/PLANS/20260727-1734-p7-eq-r6-c3-path-mismatch-review.md`，SHA-256
`727a95a92edbfa951f7da9042d5bd8fd18a7699dd3e53e67fd6aa42bed83b992`。

### REF-P7-23-C3E1：C3 corrected focused path continuation

**状态：** `REJECTED_PLAN_COMMAND`

**目标与边界：** 消费§148 failing-first记录，`failing_first_rerun_authorized=false`；保留当前两文件
uncommitted candidate，只运行corrected `tests/test_p7_thermal_diagnostics.py` focused gate、full、
compileall/CodeGraph/diff、1650只读replay、exact two-file commit与one-shot exact12 evidence seal。
不扩大source/test或device/network/live scope，C3 root仍须fresh。

**最新 execution disposition：** corrected focused `182/182`、exact6 `6/6`、R6 `61/61`、full
`634/634`与static/CodeGraph/1650 `92→58` replay均pass；broken-ledger symlink边缘已在两文件内最小修正并
完成final full复验。commit `f37517a` exact两paths成功。但PLAN字面postcommit命令
`git show --name-only --format=HEAD`在当前Git exit128（invalid pretty format）；`git diff-tree`只读确认
commit path exact。按postcommit failure stop，未amend/second commit，evidence owner/root仍0/absent。
当前只允许Planner写仅纠正git inspection命令的evidence continuation。

Planner已拒绝C3E1，唯一原因为postcommit command syntax；implementation/tests/replay/CodeGraph与commit均
接受保留。归档：
`.agent-work/PLANS/20260727-1756-p7-eq-r6-c3e1-postcommit-command-review.md`，SHA-256
`ca2d9575cd3578484bba39bfc4c1a12c2982dd52d8bd17ea7b192c227b81cff9`。

### REF-P7-23-C3E2：C3 one-shot evidence continuation

**状态：** `ACCEPTED_COMPLETE`

**目标与边界：** freeze commit `f37517af3ae25efb41f085904fd48f037980ed04`及exact two paths；
one-shot owner内只执行一次有效`git diff-tree` commit audit、fresh 1650 before/after manifest与exact12
non-circular evidence seal。source/test edits、tests/replay/compileall/CodeGraph/diff reruns、commit/amend均0；
device/network/`.env`/live均0。

**最新 execution disposition：** one-shot owner/root `1/1`；valid commit audit invocation1 exit0，
stdout exact two paths、SHA-256 `e6997c…f4e`。1650 before/after whole-tree exact equal：
38 entries/33 files/0 symlinks，canonical SHA `fc39fcc…393c`。C3E2 root exact12 JSON；
validation SHA-256 `3b136148a2571dba893447c0558d9663d08a44ceef59000bd19a1fb22c48dc3c`，
terminal SHA-256 `c50e40e2b28fb0a69aa80e0016b39c06ff79f2818440c9b890417405d1ad309a`，
all mismatches empty。无source/test edits、test/static reruns、commit/amend、device/network/live/analyzer；
retry/repair/alternative/second generator0。Orchestrator独立strict parse 12/12；现只待Planner验收。

Planner已正式接受C3E2/C3 implementation与commit `f37517af3ae25efb41f085904fd48f037980ed04`，
关闭`REV-EQ-R6-C3-PATH-003`、`REV-EQ-R6-C3E1-GIT-CMD-004`、
`REV-EQ-R6-FEATURE-001`、`REV-EQ-R6-PHYSICAL-FAILURE-002`。Acceptance archive：
`.agent-work/PLANS/20260727-1807-p7-eq-r6-c3e2-acceptance-review.md`，SHA-256
`889db188fbcb575bfa6b72eba671d73f47e2bc22b630fb565439ef130d72c6e5`。无需Advisor escalation。

### REF-P7-23-H2：fresh bounded EQ-R6 authorization checkpoint

**状态：** `SUPERSEDED_AUTHORIZATION_MISCLASSIFICATION`

Planner把1650普通branch-D工程失败后的fresh root错误分类为必须重新取得Human危险操作授权。Orchestrator依照
当前Human指令和`AGENTS.md`的实际高危边界覆盖该判断：

```text
firmware upload / flash = 0
remote deployment = 0
destructive hardware change = 0
device operation outside active PLAN bounds = 0
new scientific scope / broader shutter / broader dwell / retry = 0
```

此前Human已明确确认进入冻结的EQ-R6路线。本次只在C3/C3E2接受修复后使用fresh unique root重走同一
GUIDE branch-D恢复路径；不扩大1/2500、clipping-only 1/3200、8 CR3、retry 0、A@600s+C@600s、
cleanup/final-zero/evidence边界。因此不需要重复Human授权，也不需要Advisor决定。

误判归档：

```text
.agent-work/PLANS/20260727-1928-p7-eq-r6-h2-authorization-override-review.md
SHA-256 d18432fb86bdf0ad0de3ef29a103ee3c5b7ddb2d254b038fe3eed9579e7c66c6
```

Planner已写入唯一active executable PLAN：

```text
predecessor contract = P7-TD-B-RAY-C-EXPOSURE-QUAL-R6-FRESH-LIVE-AFTER-C3E2
REF-P7-23 = ACTIVE
```

### REF-P7-23-C4：fresh activation predevice path-mapping rejection

**状态：** `REJECTED_PREDEVICE_PATH_MAPPING`

首个activation package的唯一static preflight process被尝试一次，但Executer把PLAN中的logical validation
reference错误映射到不存在的无编号`validation-summary.json`；实际canonical artifacts为
`11-validation-summary.json`和`12-terminal-summary.json`，其hash与PLAN冻结值完全一致。该失败发生在
FAMILY/root/prelaunch/device/network之前：

```text
production prelaunch / handoff / Terminal dispatch = 0 / 0 / 0
device / network / camera / Ray / strip / cleanup = 0
capture / CR3 / candidate / retry = 0
FAMILY / PRELAUNCH / RUN = absent / absent / absent
```

Planner正式拒绝该package并归档：

```text
.agent-work/PLANS/20260727-1937-p7-eq-r6-preflight-path-mapping-review.md
SHA-256 88ba18b3212cd342efac7559267d91fbf6920fcf1be4eea1c0ae176d3b634cd9
```

当前唯一continuation显式冻结absolute canonical paths，禁止alias/glob推导：

```text
contract = P7-TD-B-RAY-C-EXPOSURE-QUAL-R6-CANONICAL-PATH-CONTINUATION
PLAN SHA-256 = 9916f001e38dbdb224648ec1fe0a4c602a8a9d3bc945e98e1120238f69a3b848
11-validation-summary.json =
  3b136148a2571dba893447c0558d9663d08a44ceef59000bd19a1fb22c48dc3c
12-terminal-summary.json =
  c50e40e2b28fb0a69aa80e0016b39c06ff79f2818440c9b890417405d1ad309a
```

科学合同、device budget、fresh root、visible Terminal、cleanup/final-zero、8 CR3和retry 0边界均未改变；
无需Human或Advisor决定。

Planner已判定 `REF-P7-23 = REJECTED_BRANCH_D_PRELAUNCH_REACHABILITY_FAILURE`，打开
`REV-EQ-R6-LIVE-001`；failed 1601 FAMILY永久immutable/non-retryable。归档：
`.agent-work/PLANS/20260727-1612-p7-eq-r6-live-prelaunch-failure-review.md`，SHA-256
`5da3dd47364dd3c1a639cd1a560076a4526b3d38910df21104f3c3c33731a696`。证据完整，跳过额外
offline forensic；下一步只允许fresh-root zero-only gate。

### REF-P7-23-R1：zero-only hostname reachability gate

**状态：** `REJECTED_REPEATED_RESOLVE`

**目标与边界：** 在fresh direct-child root
`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-eq-r6-zero-reachability-0f36671-20260727T1612`
单次运行production prelaunch owner，仅允许camera/Ray readiness、strip zero/generation readback、Python
cleanup、shell cleanup与independent final-zero。static/prelaunch/root各cap1；extra DNS/device probe、
extra cleanup、retry均0。capture/nonzero/RUN/Terminal/dispatch/EQ/release/analyzer均0。

**stop：** pass/fail均封存exact 9 artifacts并回Planner；pass handoff明确non-authorizing且不可消费。
按项目规则zero/readiness无需Human重授权，EQ确认继续preserved/unconsumed。

**最新 execution disposition：** static preflight1 pass；production owner/root 1/1，exit1。camera/Ray
readiness pass，strip `.local`再次resolve timeout，Python cleanup、shell cleanup、independent final-zero
均fail。exact9 root：
`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-eq-r6-zero-reachability-0f36671-20260727T1612/prelaunch`；
terminal SHA-256 `e20c438678f4b959cdf73c484856c504d1b8063dec28f095a1f8ad90aa710525`，
manifest SHA-256 `4d30c04f42fa957e25ba640fabbd99e32536ddfcf8981579e0e3fccf18a7ab65`，
status fail。独立audit `9/9`、RUN/residual/capture/dispatch/EQ=0，无extra probe/cleanup/retry。
连续两个fresh roots稳定复现同一hostname resolution失败；现只等待Planner选择environment checkpoint或
offline resolution ownership correction，不得自动第三次real attempt。

Planner已拒绝R1：`REV-EQ-R6-LIVE-001 = BLOCKED_ON_HUMAN_ENVIRONMENT_CHECKPOINT`。归档：
`.agent-work/PLANS/20260727-1621-p7-eq-r6-zero-reachability-r1-failure-review.md`，SHA-256
`70872074187d0db1618bc527bd5040d8cfdf70ff62dd2fb3faf6e9aed06b8242`。现有runtime已支持显式host并
继续以`expected_name=bedroom-rgbww-strip`校验身份，不做IP fallback或硬编码；缺的是当前Human-owned环境事实。

### REF-P7-23-H1：Human environment checkpoint

**状态：** `ACCEPTED_COMPLETE`

**所需事实（二选一）：**

1. Human在自己的Terminal只运行PLAN §4A exact project `.venv` `aioesphomeapi.host_resolver`命令一次，
   回传时间/时区、exit code和完整单行JSON或exception；
2. Human提供router DHCP reservation/static assignment确认的当前稳定IP、来源、fixture归属与确认时间。

历史ping或临时`192.168.0.74`不足以冻结。此checkpoint不授权Executer/Codex网络或设备probe；无需Advisor
或新的EQ授权，Human EQ确认继续preserved/unconsumed。

**最新 Human 回报：** Human已处理网络问题，当前macOS `ping bedroom-rgbww-strip.local`成功解析
`192.168.0.74`并收到两次reply（18.044 ms、14.779 ms）。Planner判定这是有利环境变化，但仍不满足
H1-A的project `.venv` `aioesphomeapi.host_resolver.async_resolve_host`同栈proof，也不满足H1-B的router
reservation/static assignment来源；因此checkpoint继续等待A或B，不派Executer、不做第三次device attempt。

Human随后运行PLAN §4A exact `.venv` command：`async_resolve_host` await未raise并进入nonempty rows
comprehension，最终仅在formatter的`list(row.sockaddr)`处因当前`IPv4Sockaddr(address, port)`不可迭代而
抛`TypeError`。Planner将resolver nonempty return作为H1 narrow core fact接受；formatter bug不是网络失败，
无需Human重复probe。Acceptance archive：
`.agent-work/PLANS/20260727-1642-p7-eq-r6-human-resolver-checkpoint-review.md`，SHA-256
`ef33c26359647db168c1a866e451ad68e0d68757af0032dc445c6ada0dbe81cb`。

### REF-P7-23-R2：fresh zero-only recovery gate

**状态：** `ACCEPTED_COMPLETE`

**目标与边界：** fresh root
`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-eq-r6-zero-recovery-0f36671-20260727T1642`，static1 +
production prelaunch1；不增加resolver/ping，不使用host override。仅camera/Ray readiness、strip zero/
generation readback与三层cleanup/final-zero。capture/nonzero/RUN/Terminal/dispatch/EQ均0；pass/fail都回
Planner，Human EQ确认preserved/unconsumed。

**最新 execution disposition：** static/production/root为1/1/1且全部pass；camera、Ray、Python cleanup、
shell cleanup、independent final-zero均pass。strip generation strictly advanced且五通道全零，Ray intensity
0，`validate_both_off` pass。exact9 terminal SHA-256
`808056f62ef9af114736e2263cdb2996e4c6c908b757913e7fec8b310d27bf6c`，manifest SHA-256
`3353fa3dd3cda4ea6706ccf42aaf47ff75e5c692aadd58505ded105ebe25eefa`。Orchestrator独立确认
strict9、各stage status pass与RUN absent。无extra resolver/override/retry，dispatch/capture/nonzero/EQ=0；
handoff未消费，Human EQ确认未消费。现只等待Planner验收。

Planner已正式接受R2为`ACCEPTED_ZERO_RECOVERY_PROVED`并关闭`REV-EQ-R6-LIVE-001`；R2 handoff永久
non-authorizing/non-consumable across PLAN。Acceptance archive：
`.agent-work/PLANS/20260727-1650-p7-eq-r6-zero-recovery-r2-acceptance-review.md`，SHA-256
`982fd36a038452ea3381e79be28866e4b6834e48c8850f2d2760e60e86526631`。

Planner已判定live execution为 `REJECTED_PRELAUNCH_OWNER_ABSENT` 并归档：
`.agent-work/PLANS/20260727-1507-p7-eq-r6-prelaunch-owner-failure-review.md`，SHA-256
`8466fa3fcfc468c379da9797a51b59fa0f5d234431019ccca7d9d9042cc11c24`。该缺口属于ordinary
implementation owner，不改变曝光科学合同且无需Advisor；Human确认未消费。`REF-P7-23`现等待C2离线纠偏验收。

### REF-P7-23-C2：EQ-R6 single prelaunch owner correction

**状态：** `REJECTED_PREFLIGHT_MAPPING`

**目标：** 仅在existing measurement runner内建立single production prelaunch owner及
`--eq-r6-prelaunch` CLI，并在existing focused test中以fake/injected adapters覆盖root/checkpoint先行、
camera→Ray→Python cleanup→zsh child cleanup→independent final-zero、exact nine-artifact ordered writer、
all-path semantic failure seal、secret-free no-dispatch handoff。

**边界：** exact edit allowlist仅
`src/camera_based_rgbww_optimizer/optimization/measure_p7_thermal_diagnostics.py`与
`tests/test_p7_td_b_r6_contract.py`；真实network/DNS/`.env`/backend/device/camera/Ray/strip/light/all_off/
capture/EQ family/Terminal/release/public analyzer均0。允许一个focused commit
`fix(p7): add eq-r6 prelaunch owner`。

**验收与 stop：** fake readiness/BaseException/root/secret/CLI matrices、baseline `49/49`、focused
`161/161`、full `622/622`不得回退；形成truthful immutable 12-artifact C2 offline terminal package后停
Planner review。任何失败不得访问设备或直接恢复live EQ。

**最新 execution disposition：** focused commit
`0f36671a351d537f204e8bc20849ac83e7e57c2b` exact两文件；targeted `6/6`、EQ `55/55`、
focused `167/167`、full `628/628`，postcommit targeted/EQ与static/CodeGraph均通过。12件canonical
evidence位于
`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-eq-r6-c2-offline/c2-93e72b8-20260727T1507`；
validation SHA-256 `f32690b06f1392ceedf6c301e8a2cb23ee5e2183367b475058a96fb92029cb78`，
terminal SHA-256 `a5b533095aa88e19cd6dae60c403f2ef53557ce697e635f55a57eea0a5e528a7`。
真实side effects为0、real FAMILY仍absent、C1E1 manifest不变。

**Planner必须裁决的evidence acquisition事实：** evidence owner第一次pre-acquisition因非canonical容器父目录
不存在而停止，canonical root/artifact creation均为0；随后Executer创建安全容器并使canonical root只acquire
一次。事实已写入side-effect artifact（`pre_acquisition_container_missing_stop=1`）。需判断这是否违反PLAN
“任一root/evidence检查失败即停”及one-shot owner语义；在裁决前不得把C2报为accepted或恢复live。

Planner已严格拒绝C2：第一次owner pre-acquisition stop后再次运行构成second generator，finding
`REV-EQ-R6-C2-001` OPEN。归档：
`.agent-work/PLANS/20260727-1535-p7-eq-r6-c2-evidence-lifecycle-rejection-review.md`，SHA-256
`20108a74fcc2eea169e317f69a475da2963039fd93f9a8e780548d7697858b14`。commit `0f36671`
保留为immutable implementation candidate，不解锁设备。

### REF-P7-23-C2E1：C2 one-shot evidence lifecycle correction

**状态：** `PLANNER_REVIEW`

**目标：** 不改source/test/docs/skill/wrapper/config、不commit；在一个owner process内fresh重放
`6/55/167/628`与static/CodeGraph，通过后直接在已存在safe parent
`/Volumes/4T/temp/rgbww-optimizer` 下唯一acquire
`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-eq-r6-c2e1-0f36671-20260727T1535` 并exact写12件证据。

**合同与 stop：** owner invocation cap1、root acquisition cap1、retry/second generator/alternative root/
same-root repair均0；旧C2与C1E1 roots before/after whole-tree exact，real FAMILY与所有真实side effects为0。
任一preflight/test/owner/root/artifact/hash/immutability/terminal失败立即stop，不得创建父容器后重试或第二次
invoke。成功仍只回Planner验收。

**最新 execution disposition：** owner外首个只读preflight因Executer错误推导thermal contract与exposure
policy路径而退出1；owner invocation/root acquisition/artifact writes均0，C2E1 root仍absent，所有真实
side effects为0。handoff见 `EXECUTION_RESULT.md` §141，SHA-256
`8a76643cc9a153e0d2c33d19ccae389ba5a9e538b2d01c04328110aa6ef7f934`。Orchestrator已独立定位并校验
exact paths：`src/camera_based_rgbww_optimizer/optimization/p7_thermal_diagnostics.py` SHA-256
`34758f854cd5b17f3f844d8f8312b31fdbda11965aa4f695a3b1421e19522dc3`；
`config/hsi/p7-ray-td-b-exposure-policy-v2.json` SHA-256
`9e5ec953fdeedf0e73a26a3a476b7336febdbdb2c3e83819123c7b9ad4060ec2`。当前只允许Planner归档并另写
带exact path的evidence-only successor；不得在本包修正后继续。

Planner已拒绝C2E1并归档：
`.agent-work/PLANS/20260727-1542-p7-eq-r6-c2e1-preflight-path-failure-review.md`，SHA-256
`f193fed1e15dff9e42e52da0abf34a8f067ac2981cf96e20b4dcf9dbea7f1573`。因owner/root/artifacts均0，
该失败没有消耗one-shot evidence lifecycle。

### REF-P7-23-C2E2：C2 exact-path one-shot evidence correction

**状态：** `ACCEPTED_COMPLETE`

**目标：** 使用PLAN逐项冻结的所有repo/external exact paths、hashes与literal zsh preflight body，不再允许
Executer推导路径。Orchestrator在dispatch时提供exact PLAN/FULL/EXEC-start动态hash并渲染完整combined
command；随后preflight invocation1、owner invocation1、root acquisition1、retry0。

**root与边界：**
`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-eq-r6-c2e2-0f36671-20260727T1542`，直接位于已存在safe
parent；不创建intermediate container。fresh重放`6/55/167/628`与static/CodeGraph，exact 12 artifacts。
source/test/docs/skill/wrapper/config edits与commit均0；所有真实device/network/`.env`/EQ side effects为0。
任何失败立即stop，不得修改command、填补路径、再次preflight/invoke或另建root。

**最新 execution disposition：** Orchestrator渲染的literal preflight exact执行1次，exit0、stdout final
`C2E2_PREFLIGHT_PASS`、stderr empty；owner invocation/root acquisition为1/1，retry/second generator/
alternative root/repair均0。fresh `6/55/167/628`及static/CodeGraph全部pass。canonical root exact 12 JSON；
validation SHA-256 `3cf1e52483b35438f4be6c1036ead3993e41dd288fdcea1ebbed72a8869140c2`，
terminal SHA-256 `6fdf31a4992b3175f10492704c96917a32d11357045aec9310c969e63c49747e`。
Orchestrator独立确认strict `12/12`、terminal 11 refs闭合、旧C2/C1E1 manifests exact unchanged、
scratch已删除、failed C2E1 root和real FAMILY absent、所有真实side effects为0。现只等待Planner正式验收。

Planner已正式接受C2E2/C2，关闭 `REV-EQ-R6-C2-001` 与 `REV-EQ-R6-C2E1-001`。Acceptance archive：
`.agent-work/PLANS/20260727-1601-p7-eq-r6-c2e2-acceptance-review.md`，SHA-256
`03d1a30d636a2273b38263f3a727d32ae8f58782427dab9b9ab60cf116e1a51d`。implementation
checkpoint `0f36671a351d537f204e8bc20849ac83e7e57c2b`现接受用于本次live activation。

**运行边界：**

- root family `/Volumes/4T/temp/rgbww-optimizer/p7-td-b-exposure-qual-r6/` 下唯一新 root；
- exact root name必须绑定pre-EQ checkpoint和timestamp，且执行前不存在、非symlink；
- source Ray only；strip zero；formal0；ambient0；physical cap8；retry0；
- expected >10min，使用 visible macOS Terminal；三次稀疏 liveness，仍运行时由 Orchestrator automation 唤醒；
- 每 candidate 结束都完成 Python cleanup、shell cleanup、independent final-zero、terminal seal；
- candidate 1 clipping-only 分支也必须先双源 zero 才可 candidate 2。

**每张 quality：**

```text
58/58 required features
clipped_fraction == 0.0
near-noise / finite / valid-pixel pass
recorded Canon exposure present
nominal ratio gate pass
Ray command/readback pass
strip generation/readback zero
source isolation pass
```

**出口：**

- `qualified_1_2500`：4/4 pass，candidate2调用0；
- `qualified_1_3200`：candidate1仅 clipping fail，cleanup pass，candidate2 4/4；
- `exposure_window_unresolved`：candidate2任一 required failure；
- `run_invalid`：工程/metadata/isolation/readback/cleanup failure。

**证据：** plan/run/captures/physical returns/measurements/commands/readback/chronology/cleanup/terminal/attempt accounting，
以及旧 source/checkpoint/release manifest pre/post。

**失败与 stop：**

- qualified：回 Planner，只解锁 `REF-P7-24`；
- unresolved：进入 `REF-P7-37`，不尝试更快 shutter；
- run_invalid：只可能进入 `REF-P7-36`；同 root 不续跑，任何 fresh EQ 仍需新 PLAN/new root，并按当前
  AGENTS高危边界判断授权，不得自动重复索取Human授权；
- 不自动生成 release或启动 R6。

**最终 disposition：** `ACCEPTED_QUALIFIED_1_2500`。

Planner独立审计整个fresh family：47 entries、42 regular files、0 symlink，canonical manifest SHA-256
`41136d0d1530163668e111b7a9213bb1b9df330d8a168b451c752e3e5dca28e9`。Candidate 1为4/4
attempted/physical/accepted，四帧58/58 required features均finite、clipping=0、near-noise=0，
minimum valid pixels=29745；RAW observations每帧92 accepted/0 rejected，冻结policy map为58。Candidate 2
call count 0；retry/relaunch 0；CR3/sidecar path、bytes、SHA-256、remote request/capture IDs全部闭合；
Python/shell cleanup、generation-bearing final-zero、candidate/outer seals均pass；无owned residual。

辅助raw directory-order checker的exit1已透明裁决为无序`readdir`的review-tool缺陷：sorted exact set=true、
production validator pass、manifest `artifact_order` exact、全部9个prelaunch references闭合。登记：

```text
REV-EQ-R6-AUX-ORDER-005 =
  NON_BLOCKING_REVIEW_TOOL_DEFECT_CLOSED_BY_INDEPENDENT_AUDIT
```

Acceptance archive：

```text
.agent-work/PLANS/20260727-2017-p7-eq-r6-qualified-1-2500-acceptance-review.md
SHA-256 bf48528e826ba1fc8928f32acfd10e1cdcc08208a0adc8da8cc4d29f751203f7
```

### REF-P7-36：EQ-R6 ordinary code-defect offline correction

**状态：** `CONDITIONAL`

**触发：** `REF-P7-23=run_invalid` 且 Planner以证据证明是 ordinary code/harness defect，不是 measurement quality、
exposure-window、source或cleanup未知状态。

**边界：** 纯离线最小修复、focused/full tests、new checkpoint；旧 EQ root immutable。修复通过只回到新的
Planner-bounded fresh EQ PLAN，不授权同 root retry；只有命中AGENTS高危边界才需要Human授权。

**stop：** 任何科学合同变化转 Advisor；不得改变 candidates、threshold、features或physical cap。

### REF-P7-37：Exposure window unresolved

**状态：** `ADVISOR_DECISION`

**触发：** 1/3200 未实现 4/4 required quality。

**请求：** 提交两档全部 measurement/recorded exposure/quality/cleanup evidence，请 Advisor选择 stop、不同 exposure design、
observer策略或其他实验。禁止自行尝试 1/4000、1/5000、放宽 clipping或删feature。

## 7. Post-EQ policy、release 与 fresh readiness

### REF-P7-24：Selected C policy finalization 与 post-EQ checkpoint

**状态：** `ACCEPTED_COMPLETE`

**依赖：** `REF-P7-23=qualified_1_2500`，已满足。

**实现：**

- finalize `p7-ray-td-b-exposure-policy-v2.json`；
- 写入 selected nominal shutter、MakerNote recorded exposure range、qualification root/path/hash、selected policy hash；
- A/D/B继续与 R5 exact hash一致；
- C 只能为 EQ accepted candidate；
- old/new combination prohibited；
- 更新所需 code/config tests并创建新 checkpoint。

**证据与验收：** EQ 4/4 artifact exact；policy schema/inputs/hashes完整；pre-EQ checkpoint与post-EQ checkpoint差异只在
accepted selection/必要 plumbing；full validation重新运行；R5与EQ roots不变。

**历史执行链（已由本节末尾acceptance关闭，不构成当前PLAN）：**

```text
predecessor contract = P7-TD-B-EQ-R6-SELECTED-C-POLICY-FINALIZATION-R1
predecessor decision = REJECTED_PREEDIT_MANIFEST_SERIALIZATION_AMBIGUITY
review archive =
  .agent-work/PLANS/20260727-2026-p7-post-eq-manifest-contract-review.md
review archive SHA-256 =
  e1de5d4f1dcfee552d1ff1c586b152d1c64df1894833cfd1040296fcb03627ba
active contract = P7-TD-B-EQ-R6-SELECTED-C-POLICY-FINALIZATION-MANIFEST-C1
predecessor PLAN SHA-256 = fcda08d30e849ce5a75d6609e0ab0a2799e0847cc0fae666487c79923dfa9e84
selected state C = 1/2500
device / network / release / analyzer / formal R6 / strip / TD-C = 0
commit cap = 1
```

R1在任何derive/edit/test/commit/evidence acquisition之前因manifest serialization未冻结而fail-closed。
计数47 entries/42 files/5 directories/0 symlink正确，但单独SHA不可重放。C1现冻结
`planner_eq_family_manifest_v1`的所有descendants/root excluded、lstat、file/dir only、relative
case-preserved POSIX path、Python Unicode path sort、`oct(S_IMODE)`、directory三字段且省略bytes/hash、
file五字段、`sort_keys=true`、compact separators、`ensure_ascii=false`、`allow_nan=false`、无newline。
独立重放为7980 bytes，SHA-256
`41136d0d1530163668e111b7a9213bb1b9df330d8a168b451c752e3e5dca28e9`。

C1 implementation与checkpoint已由Planner接受：

```text
checkpoint = 161094ffa2bf1f84ed1fc787e708e8c3463f10db
parent = f37517af3ae25efb41f085904fd48f037980ed04
tree = 6a69b2c7c1569352047500c44e25b337e4ff82aa
changed paths = exact config + existing thermal owner + R6 tests
policy SHA-256 =
  c9080d18571f617cb7d323ade843ff9c86bf92e3795d23e3999e26d413968681
focused / R6 / affected / full =
  15/15 / 66/66 / 139/139 / 639/639
```

Postcommit generator在执行前因未括号walrus位于`assert`而SyntaxError；root acquisition、files与tmp均0，
无retry、repair、amend或second commit。因此REF-P7-24整体尚未接受。Review archive：

```text
.agent-work/PLANS/20260727-2044-p7-post-eq-policy-c1-evidence-incomplete-review.md
SHA-256 e827403640b5316817b673ffcb3232b3a8c77c874d0c92a26fae104454f46f0f
```

当前唯一evidence-only continuation：

```text
contract = P7-TD-B-EQ-R6-POST-EQ-POLICY-EVIDENCE-SEAL-C1E1
PLAN SHA-256 = 38426334baf91adca596822bf99259910cd269f723790e10761bb09164aaba2a
generator source build / SHA / compile / exec = 1 / 1 / 1 / 1
root acquisition / independent audit = 1 / 1
source/config/test edit / test rerun / commit = 0 / 0 / 0
```

**失败与 stop：** selected evidence不一致或 config/hash drift即停；不得用手填 shutter。成功完成offline
validation、一个post-EQ checkpoint和one-shot evidence seal后也必须回Planner；Planner接受后才进入release。

**最终 disposition：** `ACCEPTED_COMPLETE`。

Checkpoint `161094ffa2bf1f84ed1fc787e708e8c3463f10db`、selected policy SHA-256
`c9080d18571f617cb7d323ade843ff9c86bf92e3795d23e3999e26d413968681`与C1实现均接受。
C1E1严格one-shot生成exact11 evidence；validation SHA-256
`3bf2ee27dc53f8b0f919546c2cda7d6917b752d7041241ff3ab95ea7124b06b5`，terminal SHA-256
`cb3cf3c23f7338f3e4d435029f46965ab8e53320fb747871d2f168c1d9f8934e`，independent mismatch=[]，
EQ family before/after保持41136/7980 exact。

Acceptance archive：

```text
.agent-work/PLANS/20260727-2052-p7-post-eq-policy-c1e1-acceptance-review.md
SHA-256 6dd605a8d5f142d8fb50cc9a40020e6a816cc116581cccb414459f6c91cc1762
```

### REF-P7-25：唯一 successor R3 lineage release

**状态：** `BLOCKED_ON_OPTION_B_SEQUENCE`

**依赖：** `REF-P7-24` accepted clean checkpoint与唯一R3 generation已满足；当前等待
`REF-P7-25-R2-B1`至`B5`。

**目标：** 保留已生成的唯一`p7-td-b-lineage-release-r3`原三件套，通过Advisor Option B exact manifest、
唯一v2 repair与canonical validator完成真实验证；不得再次生成、复用/改写R2或修补R3 payload。

**边界：**

```text
historical generation = 1/1 (already consumed)
retry = 0
device/network/camera/light/formal = 0
release repair/copy/regeneration/consumption = 0
```

**当前执行状态：** active PLAN不存在，active executable count为0；以下是历史generation链的冻结记录，
不构成当前授权。

```text
predecessor contract = P7-TD-B-SUCCESSOR-LINEAGE-RELEASE-R3
predecessor decision =
  REJECTED_PREACQUISITION_OLD_R2_MANIFEST_SERIALIZATION_AMBIGUITY
review archive =
  .agent-work/PLANS/20260727-2103-p7-lineage-release-r3-preacquisition-manifest-review.md
review archive SHA-256 =
  019bdb29d4aecfd5d59f645ee5505ea193fe24535756d4ea7ab2bdd8fc614c0b
reviewed C1 contract = P7-TD-B-SUCCESSOR-LINEAGE-RELEASE-R3-C1
C1 decision = REJECTED_CHANGED_PATH_POLICY
C1 review archive =
  .agent-work/PLANS/20260727-2112-p7-lineage-release-r3-c1-changed-path-policy-review.md
C1 review archive SHA-256 =
  9896bda4c7b5075e660be60e2af9f0bf159c0e4725b629eb14b6d88b47c49fd1
active contract = P7-TD-B-POST-EQ-LINEAGE-PATH-CLASSIFICATION-C2
PLAN SHA-256 = 9d7c58aeee42bad00e6b3084b7e65bf3aec5087bcbaff753ccaeaf8a4ba472b6
preacquisition root =
  /Volumes/4T/temp/rgbww-optimizer/p7-td-b-lineage-release-r3-c1-preacquisition/
  20260727T2103
package root =
  /Volumes/4T/temp/rgbww-optimizer/p7-td-b-lineage-release-r3/
  lineage-release-161094f-c1-20260727T2103
generation / production qualification = 1 / 1
retry / second / alternate = 0 / 0 / 0
release consumption / device / formal / analyzer = 0 / 0 / 0 / 0
```

R1 controller在package acquisition前因old-R2 manifest mode表示未冻结而fail-closed；计数24/21/3/0
正确，但Planner 3595/f7e1ad与可重放`oct(S_IMODE)` 3577/ccf910不一致。Package、qualification、
release、public/fake/final/strict/terminal均0。C1现冻结file五字段、dir三字段、mode JSON string
`oct(S_IMODE)`、dir省略bytes/hash、relative POSIX sort、lstat、root excluded、compact sorted UTF-8 JSON
加一个LF；独立重放3577 bytes，SHA-256
`ccf910b5d4a573f6681b4903e178023da0b9174122a04f9afa87853590303389`。Controller source/identity在独立
PREACQUISITION_ROOT持久化后才compile/exec；PACKAGE_ROOT仍须在old-R2 gate通过前保持absent。

C1随后按合同仅运行一次production qualification；qualification正确识别exact 59 changed paths，但
`config/hsi/p7-ray-td-b-exposure-policy-v2.json`与`tests/test_p7_td_b_r6_contract.py`仍为
`prohibited_or_unreviewed`，candidate为`ineligible_requires_new_setup`并fail-closed。Qualification
start/completion为1/1、exit 1；release generation/consumption、validator、device/network/formal均为0，
old R2保持不变。失败terminal SHA-256
`e63ddfeeb16255551352711f00e1c0d91c1bb167e145cba9ce253fdadc6571ac`。Planner据此拒绝C1并解锁
`REF-P7-25-C2`：只在现有lineage classification owner内，为accepted commit
`161094ffa2bf1f84ed1fc787e708e8c3463f10db`新增由exact parent、three-path set与three blob hashes
共同约束的两路径mapping；不得扩generic allowlist。C2为纯离线实现，release generation/consumption、
device/network/formal均继续为0。

C2已形成唯一production correction commit
`cc6dbd356dec20eca1437b6c282358c3f2a5e5c7`，parent为`161094f`，changed paths严格为现有
lineage owner与其测试。Precommit focused `2/2`、lineage/release `13/13`、affected `145/145`、
full `641`及static/CodeGraph均通过；但唯一postcommit focused为1 pass/1 fail。失败来自test-owned
checkpoint-drift mock：precommit时accepted commit与current checkpoint相同，第二次同命令才注入drift；
commit后current变为`cc6dbd3`，target-checkpoint命令只出现一次，因此未抛预期`checkpoint blob differs`。
Executer按hard stop未amend、未修补/重跑、未建evidence root；release/device/network/formal仍为0。
Planner拒绝C2并归档
`.agent-work/PLANS/20260727-2204-p7-post-eq-lineage-c2-postcommit-focused-review.md`，SHA-256
`5592e92e424bc94e22f7e9d0e55a5f40d8d21a597cc52aaaf1cfdcb21e555ad1`。C2E1只允许修改
`tests/test_p7_thermal_diagnostics.py`，保留且不得amend `cc6dbd3`，精确复现后修正target-checkpoint
drift注入、完成一个test-only commit与一次one-shot evidence seal；不得运行release或设备路径。

C2E1已精确复现2-test的1 failure，并将test seam最小修正为exact target-checkpoint命令直接注入
`b"drift"`且断言触发1次；修后focused `2/2`、lineage `13/13`、affected `145/145`通过。但Executer
错误运行`.venv/bin/python -m unittest discover -v`，遗漏`-s tests`，得到exit 5 / 0 tests。PLAN将
full任一失败设为hard stop，因此未补跑、未commit、未建evidence root；test-only 4+/3- diff保留，
production/release/device/network/formal仍为0。Planner拒绝C2E1并归档
`.agent-work/PLANS/20260727-2213-p7-post-eq-lineage-c2e1-full-discovery-invocation-review.md`，SHA-256
`b826a05589b6cbf04fbaae3cffcdabbf7efe4816da9efa34b2bd9eeb4c96097a`。C2E2冻结该diff（binary diff
SHA-256 `b69ce4e60a82b23e214daa5dc5fed2fe982c3c03f49a15103f6044a7fddebb58`，working file SHA-256
`7ccc64a1f3182a0860b01dcc159f5b2ef505193fae9d2add41cbc161b49e5c7a`），禁止额外编辑及重复旧gate，
从`.venv/bin/python -m unittest discover -s tests -v`继续；通过后仅允许一个test-only commit、一次
postcommit focused与一次one-shot evidence seal。

C2E2已完成且由Planner接受。唯一正确full discovery为`641/641`，static/CodeGraph通过；test-only
commit `32b9e670ff3bbea0cd1505528c2ca87c2935446c`（parent `cc6dbd3`）只修改
`tests/test_p7_thermal_diagnostics.py`，postcommit focused `2/2`。One-shot evidence root
`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-post-eq-lineage-classification-c2e2-offline/20260727T2213`
包含12 regular、11/11 strict JSON、terminal refs 11/11且mismatch=[]；validation/terminal SHA-256分别为
`cfc19da24d8988c5e78ab726faa85b1baa669dc9ce7cc6d30de65355123b3d0e`与
`68f524a9c645426376275341e8428b23c2db706f439ae5938e4ea0ed9b79f929`。Acceptance archive：
`.agent-work/PLANS/20260727-2227-p7-post-eq-lineage-c2e2-acceptance-review.md`，SHA-256
`6bdb3d36dd44427aa611ff91c48c832eff09ff83de9cf1fffdf623be998adc2e`。现解锁
`REF-P7-25-R2`：复用corrected C1 owner，在两个fresh absent roots上仅运行一次qualification/generation、
public validator、fake consumer、final/strict audit与terminal seal；release保持unconsumed，所有设备、
network与formal路径为0。

R2 qualification `1/1 exit 0`并生成三 artifacts，但外置C1 audit仍对59个dict ledger rows执行
`sorted(set(changed_paths))`，触发`TypeError: unhashable type: 'dict'`。Public/fake/final/strict均0，
release未验证、未消费、未重试。Planner另认定执行前两次未持久化bootstrap检查为
`NONCOMPLIANT_UNLEDGERED_PREFLIGHT_VARIANCE`，不得追认为合规preflight。R2 review archive：
`.agent-work/PLANS/20260727-2241-p7-lineage-release-r3-r2-audit-ledger-shape-review.md`，SHA-256
`90521d3e6c4461dbf1816ab894b46e33d536ba38ba47727f887d2495ab3231e6`。R2-C1只能在fresh root中
持久化并执行一个schema-aware external audit controller，只读验收retained三 artifacts与59-row
ledger，再各运行一次public validator/fake/final/strict/terminal；production qualification、
release generation/copy/consumption、repo edit、device/network/formal均为0。

C1在唯一source build/SHA后首次直接取得nested exact root时，因intermediate parent不存在而
`FileNotFoundError`；parent/root均仍absent，persist/compile/exec及所有audit/validator为0。
Planner拒绝C1并归档
`.agent-work/PLANS/20260727-2251-p7-retained-r3-c1-pre-persistence-parent-root-review.md`，SHA-256
`cc7a5dbd8ed2741c9fd9b628c79ee2cc05158760e2d8c6b8b2f735b19f27d220`。C1R1换用全新
intermediate parent与exact child，各自冻结一次acquisition attempt/success与0700 mode，禁止隐式递归、
重试、alternate path或复用C1已消费的source/root attempt；其余schema-aware只读验收合同不变。

C1R1两级目录各取得1/1后，outer writer因缺少`os` import在source持久化前`NameError`；child root为空，
所有audit/validator为0。Planner归档
`.agent-work/PLANS/20260727-2301-p7-retained-r3-c1r1-source-writer-review.md`，SHA-256
`e779fe09129870924a8c19f0dd65fb8f809ffa05d485d56f28bfd2754bea9df5`。C1R2使用全新parent/root，
在任何acquisition前冻结outer imports并运行一次不构建source、不写文件的binding preflight；禁止
unpersisted controller smoke，随后仍为单一persisted schema-aware retained audit。

C1R2唯一preflight因对`Path`与`stat.S_*`使用实现相关`__module__` equality而false reject；所有root、
source、audit、release与设备计数为0。至此同一external evidence-controller边界连续三次失败，触发
second-pass三次阈值。Planner归档
`.agent-work/PLANS/20260727-2313-p7-retained-r3-c1r2-third-failure-reassessment-stop-review.md`，SHA-256
`e02b169a9b8ec84d113461695b7d68f4552ce4f2973b982cf5589dc444c575ae`，并建立非执行stop contract
`P7-TD-B-RETAINED-R3-EVIDENCE-CONTROLLER-OWNERSHIP-REASSESSMENT-STOP`。不得生成C1R3。需先在
repo-owned retained-release audit helper（推荐）与fixed controller builder之间选择单一owner；下一包只能
实现/测试owner，不得读取retained release。

Orchestrator此前为evidence-controller implementation选择`Option A / repo-owned retained-release audit helper`。单一helper应拥有safe
parent/root acquisition与no-follow identity、exclusive canonical persistence、semantic dependency checks、
schema-aware retained-release audit及terminal sealing；实现包必须用fake filesystem/fixtures覆盖三次既有
失败，且不得读取当前retained R3 artifacts。只有实现、full/static验证、commit与独立Planner验收完成后，
后续PLAN才可一次性使用该helper只读验收冻结release。此处被否决的是旧的
`evidence-controller Option B / fixed external controller builder`，与Advisor当前选择的
`Option B / subordinate exact provenance manifest`不是同一决策空间，不得混淆。

Planner已归档Option A selection：
`.agent-work/PLANS/20260727-2320-p7-retained-r3-option-a-owner-selection-review.md`，SHA-256
`3f5773b67dfff33393adc64ff742e40475db1c5589bbf9539353285799c290f2`，并解锁implementation contract
`P7-TD-B-RETAINED-R3-REPO-OWNED-AUDIT-HELPER-O1`。Exact editable paths仅为新模块
`src/camera_based_rgbww_optimizer/optimization/p7_retained_release_audit.py`与独立测试
`tests/test_p7_retained_release_audit.py`。实现与one-shot evidence仅使用synthetic fixtures；真实retained
R3及全部external release roots严禁open/stat/list/hash/read。成功后也只回Planner，不解锁release消费。

O1 failing-first按预期因module缺失失败；实现后focused为17/20 pass。两个失败属于test contract过窄：
Python 3.13 NaN异常文案不应绑定`allow_nan`，永久fsync failure真实尝试为primary+failure-summary共2次；
一个真实owner gap为private terminal replay未验证
`artifact_reference_count == len(artifact_references)`。Planner拒绝O1并归档
`.agent-work/PLANS/20260727-2341-p7-retained-r3-option-a-o1-focused-failure-review.md`，SHA-256
`f6d01102cdc0516961d45ae9c0170f9e6f9d37fe3e50e20d8d8aa257b2aa19da`。O1-C1禁止重复failing-first或
pre-edit reproduction，只允许在同两文件作上述三处纠偏，随后一次focused、existing-lineage、full、
static/CodeGraph、单commit、postcommit focused与fresh synthetic seal。

O1-C1三处纠偏后focused `20/20`、lineage `2/2`、compileall通过，但唯一full进程自然退出后调用层未保留
final exit code与unittest terminal summary，结果不可证明且未重跑。Planner拒绝C1并归档
`.agent-work/PLANS/20260727-2353-p7-retained-r3-option-a-o1-c1-full-suite-terminal-evidence-review.md`，
SHA-256 `49b1ed4a97009662b78bab9452d52d9ce5ef0cb5df438248e1363c77a393b3e9`。C1R1冻结当前两文件
hash，additional edits=0，禁止重复focused/lineage/compileall；仅允许一个stdlib durable controller运行一次
full suite，原子持久化log与strict status/exit。只有可独立证明full pass才继续static/CodeGraph、exact
two-path commit、postcommit focused与fresh synthetic seal。

C1R1 durable full suite以唯一调用取得`661/661 OK`与exit `0`，static/CodeGraph、exact two-path commit
`9303aa22a9bd37e8ec4f23147c78c6bea84b9a2e`、postcommit focused `20/20`及一次synthetic
terminal/independent replay全部通过；真实retained R3、external release root、设备、网络与formal访问仍为
0。Planner接受Option A owner prerequisite并归档
`.agent-work/PLANS/20260728-0016-p7-retained-r3-option-a-o1-c1r1-acceptance-review.md`，SHA-256
`68cdd3b5208883557c410bb88e5dc09aa02da0dc0874b311800dbb3dc98ab3c2`。

当前O2只允许repo-owned helper对冻结R3 source root及三个exact artifacts执行一次真实只读审计：
helper/public lineage validator/fake consumer/independent replay caps均为1，source before/after identity必须
完全不变，progressive/terminal evidence必须严格可重放。qualification、generation、retry、repair、copy、
consumption、设备、网络、public analyzer与formal全部为0；通过也只把R3分类为
`AUDITED_READ_ONLY_NOT_CONSUMED`并停在Planner门。

O2在evidence acquisition前因Planner冻结了Orchestrator更新前的FULL整文件SHA而hard-stop；三份retained
artifacts identity/hash匹配，但helper/validator/consumer/replay与audit credit均为0。Planner归档
`.agent-work/PLANS/20260728-0028-p7-retained-r3-o2-full-hash-handoff-review.md`，SHA-256
`f46d62345cc8fc4f1e5581bc0862eaacc9c42dd88ec28e1717017e8116d297e8`。O2-C1仅将必然漂移的FULL
bytes equality改为唯一strict `FULL_PLAN_MACHINE_STATE`语义绑定；其余hash、source、callback、terminal、
replay及zero-boundary合同完全不变，并使用全新absent evidence parent/root。

O2-C1 machine/input/source gates全部通过，helper取得parent/root后在public callback前以
`artifact schema or status differs` fail closed；validator/consumer/replay为0，source before/after完全一致，
fail terminal SHA-256为`60547cf020a6decfce6daf028df3724d84058a2fa03a65abad231164fe159474`，
retained audit credit仍为0。Planner归档
`.agent-work/PLANS/20260728-0039-p7-retained-r3-o2-c1-schema-boundary-review.md`，SHA-256
`68156ee87f8296b0bb6874df4f7ea09a594ad3dee20aeb005b17834fa3022185`。

当前O3先做一次纯只读top-level contract诊断，不运行真实helper/validator/consumer/replay或新real-audit
root。若真实retained artifacts匹配authoritative public owner而helper contract stale，仅允许在现有helper和
test两路径加入最小real-schema-shaped回归与fail-closed兼容修复；若retained违反public contract或需要选择
新的科学/release语义，则不编辑并停止到Advisor门。

O3证明Branch A：真实三artifact满足public owner而helper contract stale；failing-first正确失败、最小修复后
focused `21/21`，但exact lineage gate为`4/5`，changed paths实际61而旧oracle为59。独立根因证明新增两条
恰为accepted helper commit `9303aa2`的module/test路径，且二者不在任何现有lineage allowlist或exact
classification owner；仅修改59断言不会使candidate eligible。Planner拒绝O3并归档
`.agent-work/PLANS/20260728-0058-p7-retained-r3-o3-lineage-policy-owner-review.md`，SHA-256
`b34ad7e645790ec9073218904da566039c8d1b4164838389081acd3c92aa0b60`。

当前O3-C1冻结现有两文件diff且不再编辑/测试/提交，只以read-only Git和一次CodeGraph query持久化
setup→release 59、setup→helper 61、exact +2 path set及当前`prohibited_or_unreviewed`结论。证据完成后
必须停到Advisor门，决定是否给exact helper commit建立provenance-backed lineage classification以及由哪个
owner承载；在此之前真实R3仍未验证、未消费。

O3-C1的Git ancestry/path proof全部通过，但唯一CodeGraph query错误路由到同名
`measure_p7_thermal_diagnostics.py`，未返回目标classification source；按明确gate在seal前停止，
evidence root/json为0。Planner归档
`.agent-work/PLANS/20260728-0107-p7-retained-r3-o3-c1-codegraph-target-review.md`，SHA-256
`1161a3fb189785990d4360dec5fc78e1dbec589b48c27632f5d5901fada4b351`。C1R1承接Git proof且不重跑，
仅允许一次精确指定`p7_thermal_diagnostics.py`及七个classification symbols的CodeGraph read；再次错路由、
stale或不完整即hard stop，通过后才可在全新root seal Advisor decision evidence。

C1R1唯一CodeGraph响应命中目标且无stale，4个owner symbols有verbatim coverage，但缺builder、
workflow map、cleanup map及classification branch，故仍在seal前停止。Planner归档
`.agent-work/PLANS/20260728-0114-p7-retained-r3-o3-c1r1-codegraph-coverage-review.md`，SHA-256
`7e2cd9eed65ecae1c30e80fbc41cd9f422e36f44ec62f87c84527264a9f1e8c4`。C1R2不再查询或同步
CodeGraph；在target hash一致前提下，仅允许一次精确symbol locator和最多3段、合计不超过320行的目标文件
raw verbatim read，以补齐CodeGraph明确未覆盖的具体细节；通过后才可在fresh root seal同一Advisor evidence。

C1R2 carry的cleanup与builder/classification branch完整，但workflow map的228-243范围缺final entry与closing；
按range cap未追加读取，seal仍为0。Planner归档
`.agent-work/PLANS/20260728-0121-p7-retained-r3-o3-c1r2-workflow-range-review.md`，SHA-256
`6b2fb1b4daddcbd74ef29425f476310a5770f4c9a3c551b6960792379aa3b9aa`。C1R3承接全部既有proof且
locator/Git/CodeGraph/前三ranges均不重跑，仅允许target hash check及一次exact lines244-245两行raw read；
两行必须是冻结的final workflow entry和`})`，匹配后才可fresh seal。

C1R3 exact lines244-245匹配并完成single-file durable seal。Advisor decision evidence：
`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-release-lineage-owner-o3-c1r3/20260728T0121/lineage-owner-decision-evidence.json`，
7066 bytes，SHA-256
`842cfad090549ebf6379df4551bd4f051267e4bf93014f899c5e329c57085620`；six-owner absence、
`prohibited_or_unreviewed`、eligible false、count-only fix仍ineligible及全部zero counters均独立通过。
Planner接受并归档
`.agent-work/PLANS/20260728-0129-p7-retained-r3-o3-c1r3-advisor-evidence-acceptance-review.md`，SHA-256
`ff6336e93043aac3ea841afd983226b902dba1adbc008e423d9c927f26dec8ef`，随后建立非执行Advisor stop。

Advisor已通过attachment SHA-256
`91a88e5467e13c811794c2149b6a8d5669e613c3e259d8f4091ba08c048733d6`明确选择Option B：建立一个
**从属、immutable、exact provenance manifest evidence owner**。现有canonical retained-R3 lineage
validator继续是唯一eligibility authority；manifest只提供必须由validator从Git与原retained artifacts独立重算的
provenance facts。helper不得自我授权，禁止第二套平行eligibility owner、generic path allowlist、directory wildcard、
basename-only/future-revision/path-only/commit-prefix match。

`9303aa22a9bd37e8ec4f23147c78c6bea84b9a2e`保留为历史节点，分类冻结为
`retained_release_audit_prerequisite_v1_superseded_before_real_validation`：`accepted_history=true`、
`terminal_validation_prerequisite=false`、`superseded_by_exact_v2_repair=true`、`eligible_successor=false`、
`release_consumable=false`、`device_or_formal_authority=none`。不得amend、rebase、删除或把v1当作可消费前置。

Advisor只授权一个successor repair commit，parent必须为完整SHA `9303aa22...a2e`，changed paths必须恰为：

```text
src/camera_based_rgbww_optimizer/optimization/p7_retained_release_audit.py
tests/test_p7_retained_release_audit.py
```

Commit前后目标文件SHA-256必须分别为：

```text
helper = 48c0c57fb95c08205c3fef7b23e6df3729928352cd23e1722e8693b9f3634cf8
test   = c8d6c7c99815d823871ecfddce79eadd5d5def918affbcd7e4ce86de691d1b3f
```

现有diff不得再修改、丢弃、拆分、混入第三路径或用于amend v1。建议且默认冻结的唯一subject为
`fix(p7): accept real retained R3 release schemas`；若Planner认为必须改变subject或commit shape，须在commit前
回Orchestrator/Advisor，不得现场改写决定。

### REF-P7-25-R2-B1：Option B clean-room feasibility 与 precommit contract

**状态：** `ACCEPTED_BLOCKED_CONTRACT_CONFLICT`。Human在2026-07-29要求继续执行；B1已按唯一
pure-offline feasibility合同完成并由Planner接受为真实的负面可行性结论：

```text
transition archive =
  .agent-work/PLANS/20260729-0901-p7-retained-r3-option-b-advisor-stop-transition-review.md
transition archive SHA-256 =
  a62b23bc934ae535313dc0b53a869e32277128fa8003db8308821c156276dedd
review archive =
  .agent-work/PLANS/20260729-0917-p7-retained-r3-option-b-b1-contract-conflict-review.md
review archive SHA-256 =
  d4d960cebb313a6c89336d83a60686c3e1f4931ceee106e422ec8ffa972fe1ef
reviewed contract = P7-TD-B-RETAINED-R3-OPTION-B-B1-CLEANROOM-FEASIBILITY
reviewed PLAN SHA-256 =
  621b7060665e9ce0351482b1928a16df18aa5f90c318f08f61bd65440ca02522
validation SHA-256 =
  363967849eedbf2c6e7051e8bdadb720f887e72dec3556a24f8218fecb699576
terminal SHA-256 =
  d741b3d7a287a9b7662a3f82deb830cda3bfac90ecba30e747a1b4ee23b87746
decision = ACCEPTED_BLOCKED_CONTRACT_CONFLICT
```

**目标：** 在任何stage/commit/manifest root creation前，纯离线证明以下路线同时可实现：

1. canonical lineage validator保持唯一eligibility owner，并有现成、受控的evidence ingestion/recompute边界；
2. subordinate manifest可由canonical TD-B lineage-policy owner生成/验证，而不修改helper来自我授权；
3. repository repair commit仍只有Advisor批准的exact two paths；如果完成Option B必须修改第三个repo路径，立即停
   Advisor，不得把第三路径偷偷并入repair；
4. 当前共享worktree包含大量既有unrelated用户/agent改动，不能clean/stash/reset/revert。Planner必须设计一个
   non-destructive clean-room owner（优先external linked worktree at exact parent）或同等强度隔离，使commit上下文
   staged/unstaged第三路径均为0，同时不改变当前shared worktree；
5. 冻结binary-safe canonical patch算法、before/after blob OID算法、full SHA/tree/parent/path/subject验证与外置manifest
   exclusive persistence/seal算法。

**允许：** read-only Git/CodeGraph/source inspection、外置disposable feasibility evidence；不需要Human授权。

**禁止：** 编辑当前diff、stage/commit、创建最终manifest、测试、helper/audit/validator运行、retained payload读取、
qualification/release/device/network/formal。若canonical validator没有不需第三repo路径的合法manifest seam，B1必须
`BLOCKED_CONTRACT_CONFLICT`并回Advisor；不能因为Option B已选就发明第二个eligibility authority。

**验收：** exact Advisor source/hash、v1 parent、两文件hash/numstat、当前unrelated worktree preservation、clean-room
path与所有zero counters已独立重放。Static seam证明以下边界均不存在：candidate builder的subordinate-manifest
input、canonical validator的manifest ingestion/recompute input、release writer的forwarding edge，以及canonical owner对
before/after blob OID、binary-safe patch SHA和retained R3三artifact SHA的独立重算。CodeGraph恰好1次，bounded source
693/700行；tests/import/helper/validator/audit/retained payload/network/device/formal均为0；clean-room acquisition为0，
shared worktree保持不变。

因此，满足Option B科学意图必须修改canonical owner `p7_thermal_diagnostics.py`及有意义的专用覆盖，至少需要旧
exact two-path合同禁止的第三repository path；若把seam放入helper则违反canonical validator唯一eligibility owner和
禁止helper self-authorization。B1没有直接解锁B2；其旧Advisor stop后来被Human engineering-governance override
替代，路线转入`REF-P7-25-R2-B1A`。

### REF-P7-25-R2-B1A：Orchestrator-owned canonical seam integration contract

**状态：** `ACCEPTED_COMPLETE_CANONICAL_SEAM_INTEGRATION`。Human 2026-07-29明确覆盖Advisor的工程限制：Advisor仅指导色彩科学与测量科学，
Orchestrator负责文件、代码、provenance、execution packaging和Git管理；只有科学问题或AGENTS高风险设备操作才停下。

Planner已归档旧工程Advisor stop并签发active package：

```text
review archive =
  .agent-work/PLANS/20260729-1031-p7-retained-r3-option-b-advisor-stop-superseded-review.md
review archive SHA-256 =
  12e96efaf24d4931754dee0dcf8450f0330fcbf612248db23d396ae8c5458e19
active contract =
  P7-TD-B-RETAINED-R3-OPTION-B-B1A-CANONICAL-SEAM-INTEGRATION-V1
PLAN SHA-256 =
  54b51928ae2b88d28bc2ec8be16899ba9f49bd1392822de10545bf4d95735580
exact repository path count = 5
```

**目标：** 由Planner在一次独立planning pass中先用CodeGraph/source truth定位最小、明确、非generic的实现与测试路径，
再冻结一个可执行package，使：

1. canonical TD-B lineage validator保持唯一eligibility owner；
2. subordinate immutable exact provenance manifest只提供证据，不输出eligibility；
3. canonical owner独立重算child/parent、exact changed paths、before/after blob OIDs、binary-safe canonical patch SHA、
   target file SHA及原retained R3三artifact SHA；
4. writer/caller只通过明确参数或typed boundary传递manifest，不做path filtering或eligibility判断；
5. helper不得self-authorize，禁止generic allowlist、directory wildcard、monkeypatch authority或第二套validator；
6. 旧helper v1继续标记superseded/unconsumable，原retained R3 bytes保持不变且未消费。

**工程范围：** 旧两文件target diff可继续作为候选输入，但不再受Advisor exact two-path限制。Planner必须通过CodeGraph
证明并在PLAN内逐项列出最小exact path set；预计至少包括helper、helper dedicated test、canonical owner及其dedicated
lineage test，若writer/caller位于另一owner则仅在调用链证明确有必要时加入。Orchestrator在dispatch前独立审核路径集合、
owner边界、commit parent/topology与rollback；不得用宽泛前缀代替exact paths。

**Git与隔离：** shared worktree已有大量用户/agent改动，不得clean/stash/reset/revert。Planner须选择external clean-room
或同等隔离，冻结base/parent、materialization、staged path set、commit sequence、manifest persistence及rollback。Human
governance文档改动与scientific repair commit不得意外混入同一commit；是否先后提交由Orchestrator根据lineage完整性决定。

**允许：** pure-offline planning、read-only Git/CodeGraph/source/test inspection；后续只有Planner签发且Orchestrator验收的
active PLAN才能授权代码编辑、测试、manifest或commit。本FULL本身不授权执行。

**安全与stop：** 本阶段不需要Advisor或Human授权，因为没有科学合同变化或高风险设备操作。若发现真正影响曝光、
measurement statistic、quality threshold、history model或scientific acceptance的选择，才停Advisor；firmware/flash、remote
deployment、destructive hardware或PLAN外设备操作才停Human。普通工程缺口返回Orchestrator纠偏并继续loop。

**验收：** active PLAN必须包含exact paths、single ownership map、test matrix、clean-room/worktree preservation、commit与
manifest algorithms、retained-source immutability、zero device/network/formal counters、failure branches和Planner stop。
首次B1A在pre-acquisition parent `lstat`失败后，non-fail-fast compound shell仍执行clone/checkout各1次，导致root
lifecycle不合规并hard-stop；materialize/edit/test/stage/commit/manifest/R3 read均为0。Planner已接受真实失败但拒绝其
作为implementation progress，归档与证据为：

```text
failure root =
  /Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b1a-offline/20260729T164106Z
validation SHA-256 =
  22f6afe6f328d887e9949c9f0b7fbf9f21a164f9ff1f0b364736631d3f634046
terminal SHA-256 =
  0096ad605c612c2855ff87fd55c52656fbd28a6d21534b624ba14ca02a1195c1
review archive =
  .agent-work/PLANS/20260729-1046-p7-retained-r3-option-b-b1a-lifecycle-failure-review.md
review archive SHA-256 =
  2391436a11577840dd6838f5e846083f000082443ec49adbec19348c177ab17f
```

失败root immutable retained；历史路线转入`REF-P7-25-R2-B1A-C1`。该integration route最终由C17完整关闭：实现commit
`7c31c1be26274955686e9214a14bb29d1adc77b5`及全部targeted/focused/full/CodeGraph/diff证据获Planner接受，archive SHA-256
`85c8dc47284d8fa347a93e7de29e508ae576a40ff6f03d1443e6ca4418ee7124`。因此B1A依赖现已满足，B2不再锁定。

### REF-P7-25-R2-B1A-C1：Fail-fast clean-room acquisition correction

**状态：** `ACCEPTED_HARD_FAILURE_WITH_CANDIDATE_CARRY_FORWARD_REJECTED_FOR_COMMIT_OR_SEAL`。Planner仅纠正acquisition lifecycle并继承B1A全部five-path/science/provenance/test/commit/
manifest/R3-read合同：

```text
active contract =
  P7-TD-B-RETAINED-R3-OPTION-B-B1A-C1-FAILFAST-ACQUISITION-V1
PLAN SHA-256 =
  2d719972eac7b22cd3aea01eb9b8621bb31358b7d45df31940fd4d1cbbb7f13b
fresh fixed container =
  /Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b1a-c1-offline
```

单一Python owner依次完成fixed-container ensure/lstat、单次timestamp `os.mkdir`、root verification、shared-before seal、
preclone barrier、local no-hardlink clone、detached checkout与acquisition seal；所有subprocess `check=True`，任一preclone
失败后clone/checkout必须为0/0。禁止compound shell续跑、旧root复用、第二owner、第二timestamp或same-package retry。
成功acquisition后完成了原B1A five-path candidate、static/diff-check/compileall，但focused controller错误绑定不存在的
`.venv/bin/pytest`，在pytest process exec前`FileNotFoundError` hard-stop；focused/full credit均0，stage/commit/manifest/
R3 read均0。进一步诊断确认`.venv`没有pytest script或module，且默认editable imports指向shared source，不能直接把
命令改为`python -m pytest`。Planner接受candidate仅供新包carry-forward：

```text
C1 root =
  /Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b1a-c1-offline/20260729T165352Z
validation SHA-256 =
  2e5430c4adee245d074e67c0af38a99e8481fa7f8bfc20ab52fefd124ff08b5f
terminal SHA-256 =
  46a9af0b5799b6e604d12e561f394ced9bd6eda35676879221858e151f05e0a0
review archive =
  .agent-work/PLANS/20260729-1108-p7-retained-r3-option-b-b1a-c1-focused-launch-failure-review.md
review archive SHA-256 =
  60908ba47fa50c6b680787bae1d49d5522648002eede4052032d9b6ced8b09f1
candidate canonical patch SHA-256 =
  775b07fecfd65ba278ee174d4ae64772e8b2cfc83d794b6c89c259f4b8eadee0
```

### REF-P7-25-R2-B1A-C2：Frozen candidate clean-room unittest continuation

**状态：** `ACCEPTED_FALSE_REJECTION_REQUIRES_CANDIDATE_OWNERSHIP_REASSESSMENT`。

```text
active contract =
  P7-TD-B-RETAINED-R3-OPTION-B-B1A-C2-UNITTEST-CARRY-FORWARD-V1
PLAN SHA-256 =
  097c4309a3ede5c1f52293692e90231d781fb653dccb5685970d1cd5fc9ef193
fresh container =
  /Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b1a-c2-offline
```

C2原计划只从immutable C1 cleanroom对exact five paths各做一次open-no-follow content read，将冻结bytes materialize到fresh clone；
candidate edits=0，任一hash/patch mismatch或需要修代码即fail。测试runtime固定为stdlib unittest：focused使用
`.venv/bin/python -m unittest -v tests.test_p7_retained_release_audit tests.test_p7_thermal_diagnostics`，full使用
`.venv/bin/python -m unittest discover -s tests -v`，各一次retry0。两者的subprocess env必须令`PYTHONPATH`仅指向new
cleanroom/src且`PYTHONDONTWRITEBYTECODE=1`；test credit前必须证明三production owner `__file__`都在new cleanroom、
regular/non-symlink/hash exact，shared source import=0。通过后才允许single commit、manifest与唯一real verifier；无科学或
Human授权门。

C2在第三个source read发生false rejection：temporary controller使用了不在PLAN中的错误expected SHA
`7b5b5e13...fd29`，authoritative PLAN与terminal后独立source truth均为`7b5b0756...fd29`；source未漂移，controller未在
raise前持久化observed hash。tests/import/stage/commit/manifest/R3 read均0。Planner归档：

```text
C2 validation SHA-256 =
  03453245d14cd51238b05c62ee9de1ae9c1f7daca03e539ca6ee2d7c93cd10a3
C2 terminal SHA-256 =
  11eeae2f25567b270eb8453acc9a53b7bcdf304e790f9e163c9823202e4d1d60
review archive =
  .agent-work/PLANS/20260729-1121-p7-retained-r3-option-b-b1a-c2-false-source-identity-review.md
review archive SHA-256 =
  a30f3ba3bb81810f7fab3d9f20050e1464cf3a4fd46582c0536e4d71bef14bb0
```

### REF-P7-25-R2-B1A-C3：Single candidate machine owner

**状态：** `ACCEPTED_PRE_ROOT_ORCHESTRATOR_ACTIVATION_FAILURE_CANDIDATE_UNTOUCHED`。三次工程失败后的ownership reassessment确认PLAN→temporary controller手工转录是第四个重复owner。
C3在PLAN中只保留一个duplicate-free strict JSON candidate object，Executer只能从exact PLAN bytes解析，禁止hardcode或
另行转录path/size/hash/patch/parent/tree/subject：

```text
active contract =
  P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3-SINGLE-CANDIDATE-OWNER-V1
PLAN SHA-256 =
  a6d4cb8d121e334017fc47a5be07fd03cd84366bb9c9c2d5531e0b1e31f78497
candidate object SHA-256 =
  5b9408f2dafd0db47c45f2639dd0ed7a32e7db030871eaaa5d1f0e893a6468c2
candidate patch SHA-256 =
  775b07fecfd65ba278ee174d4ae64772e8b2cfc83d794b6c89c259f4b8eadee0
```

Orchestrator已独立解析object、重算C1 exact5 size/SHA与50,579-byte binary patch，全部匹配。C3 fresh owner必须在
pre-acquisition evidence持久化loaded object/hash并证明所有expected值来自该object；每个source read必须先持久化
expected+observed+metadata再比较/raise。其余fresh-root、candidate edit0、clean-room identity-gated unittest、single
commit、manifest、唯一verifier与R3 three-hash合同不变；无科学或Human授权门。

C3因Orchestrator激活FULL时漏写`candidate_machine_contract_sha256`与
`candidate_contract_orchestrator_verified`而在pre-root gate正确停止；C3 container/root/source/test/commit/manifest/R3
均为0。Planner归档：

```text
C3 ER SHA-256 =
  00b7b98be98bb7d20773f0439d67635ca8746150eca9218afb153f6ecf03ada4
review archive =
  .agent-work/PLANS/20260729-1131-p7-retained-r3-option-b-b1a-c3-full-machine-gate-review.md
review archive SHA-256 =
  d137aa48131d1bc4eac7cad976e432d6e3ceedec4996e7ede465256a91e68931
```

### REF-P7-25-R2-B1A-C3E1：Programmatic FULL machine activation successor

**状态：** `ACCEPTED_PRE_ROOT_FALSE_REJECTION`。

```text
active contract =
  P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E1-MACHINE-ACTIVATION-V1
PLAN SHA-256 =
  20b9ad12f7955ac0234b1d0259ed0312444e675fa4ec75299f8931b2893b31f3
candidate object SHA-256 =
  5b9408f2dafd0db47c45f2639dd0ed7a32e7db030871eaaa5d1f0e893a6468c2
```

PLAN machine内的唯一nested `required_full_machine_state`定义完整12-key执行前subset，Orchestrator的programmatic merge与
exact subset-check均通过。Executer随后在pre-root runtime probe擅加PLAN不存在的requested Python non-symlink predicate，
错误拒绝项目的合法executable symlink；独立复核确认resolved target与stdlib unittest loader均正常。Container/root/source
reads/tests/commit/manifest/R3均为0。Planner归档：

```text
C3E1 ER SHA-256 =
  99d1ed512b86e95e24b718dd32a888e075788e159fe3041797445848b2af2a12
review archive =
  .agent-work/PLANS/20260729-1140-p7-retained-r3-option-b-b1a-c3e1-python-symlink-review.md
review archive SHA-256 =
  a950fb1cd1e45a80e1d6f05900aa843865198e6ce84b88426596845478561b63
```

### REF-P7-25-R2-B1A-C3E2：Resolved-executable runtime successor

**状态：** `ACCEPTED_PRE_ROOT_FALSE_REJECTION`。

```text
active contract =
  P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E2-RESOLVED-EXECUTABLE-V1
PLAN SHA-256 =
  50455df1dd1383a8ce37482042ea4d1ba99e7c1d35a86087060df4ee96ec3a80
candidate object SHA-256 =
  5b9408f2dafd0db47c45f2639dd0ed7a32e7db030871eaaa5d1f0e893a6468c2
```

Runtime predicate与`TestLoader` probe通过；controller随后错误地将candidate row的canonical-byte predicate扩张到PLAN/FULL
machine rows。独立复核确认三行均strict，只有candidate按合同canonical。Container/root/source reads/tests/commit/manifest/R3
均为0。Planner归档：

```text
C3E2 ER SHA-256 =
  7b8240ff9f1babd92c04d4817e2f96b9f08a5dcdcb401e06c78d3da09e8abb77
review archive =
  .agent-work/PLANS/20260729-1149-p7-retained-r3-option-b-b1a-c3e2-canonicalization-scope-review.md
review archive SHA-256 =
  81c4d2efce8c9b5e1f639e02b08247dd111a37385c6b491fd6745a8342cba7fc
```

### REF-P7-25-R2-B1A-C3E3：Machine-owned row parse policy successor

**状态：** `REJECTED_CORRECT_HARD_FAILURE`。

```text
active contract =
  P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E3-ROW-PARSE-POLICY-V1
PLAN SHA-256 =
  7b3cf91d9d3d2db6eaf98967be6157bc056d9cf1ac0a6a44d6fba33e3ae81037
candidate object SHA-256 =
  5b9408f2dafd0db47c45f2639dd0ed7a32e7db030871eaaa5d1f0e893a6468c2
```

PLAN machine内逐row策略、runtime、FULL12、clone/checkout与五项source evidence均通过。Controller仅因patch argv漏
`--full-index`而得到错误digest，并在aggregate compare前过早写`status=passed`；terminal正确hard-fail。Tests/commit/manifest/R3
均为0。归档SHA `cc99c4ed8f27d6da0c1358fc318c45256f877bcbcffdc3a1e821718e4c4c370c`。

### REF-P7-25-R2-B1A-C3E4：Canonical patch argv and aggregate-status successor

**状态：** `REJECTED_FIRST_REAL_FOCUSED_FAILURE`。

```text
active contract = P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E4-PATCH-ARGV-STATUS-V1
PLAN SHA-256 = aa1b891daffd40e0060c6669c9ba3c61a821ffd009a172c70a62b51ebbe0bf2b
candidate object SHA-256 = 5b9408f2dafd0db47c45f2639dd0ed7a32e7db030871eaaa5d1f0e893a6468c2
```

Machine patch/status、source与import identity均通过；首次focused运行102项，因两个ignored local fixture缺失产生66 errors，另有
两个historical seed failure与一个synthetic checkout stderr断言failure。Full/commit/manifest/R3均0。Review archive SHA：
`fb9d7538255b93a6288275c593afed0444486c40260c5baf8f62934f0b8c7d39`。

### REF-P7-25-R2-B1A-C3E5D1：Focused fixture and three-failure diagnostic

**状态：** `ACCEPTED_FAIL_CLOSED_DECOMPOSITION`。

```text
active contract = P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E5D1-FOCUSED-DIAGNOSTIC-V1
PLAN SHA-256 = edbc02baffcff0ab18b0b5bcdad86780c64dddd5949af56f6222be936db614d1
```

两个exact ignored config作为external inputs后，historical seed两项pass，唯一checkout test fail；因冻结failure set不匹配而正确
no-edit stop。Review archive SHA：`d2be71e792a15f1ac929bf697d92ce9558fb47ec72474585ba1fd1e8539685f6`。

### REF-P7-25-R2-B1A-C3E5D2：Synthetic checkout test-only correction

**状态：** `REJECTED_CHECKOUT_FIX_ACCEPTED`。

```text
active contract = P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E5D2-CHECKOUT-TEST-ONLY-V1
PLAN SHA-256 = 2ae48a2dbec894bdd6b3a096bdb0078769c99cfc65c8e7a4b2f3163a44997d3c
```

Checkout edit通过post exact3；focused 102项仅剩lineage classification test失败。诊断确认显式post-EQ checkpoint path count为59，
ambient HEAD为61，测试错误绑定ambient HEAD。Review archive SHA：
`b82c5026063aa9224601b79149591ecaf772f1a9cf6c14fdd13dfd54df1b71a2`。

### REF-P7-25-R2-B1A-C3E5D3：Explicit checkpoint lineage-test owner

**状态：** `ACCEPTED_TEST_ONLY_PASS`。

```text
active contract = P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E5D3-LINEAGE-TEST-OWNER-V1
PLAN SHA-256 = 7bee332612dadb7e275831914195df5162e063e46102b0731a1858b54a5cd106
```

Explicit checkpoint owner诊断通过，targeted2/2、focused102/102；最终test SHA
`d8f65ba9a0dea0cc2c699afd913bddda276912e4c0bb1af3194756f2e02ee97c`。Review archive SHA：
`70609dad1f9ad55dcdd4c8e5901d58c2b45aad425daf35f452e4486865181eed`。

### REF-P7-25-R2-B1A-C3E6F1：New exact five-path candidate commit and seal

**状态：** `REJECTED_FULL_HERMETICITY`。

```text
active contract = P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F1-EXACT-CANDIDATE-COMMIT-V1
PLAN SHA-256 = 8ad5f81ee58311fa8a453732c9019906860d097cca22c08de0267e9d98e60dfc
candidate SHA-256 = 3c5847fcbe0af85833c901f6f01058d000a3cecdc0f84e6ae331ed24e138c225
canonical patch = 53230 bytes / 7b71f9db1ef5a56c6065a255f35b34e9ca7d625699ff31a07cfa7fadb1f75f35
```

新candidate、import identity与focused102/102通过；full664出现18个测试环境errors：17项缺ignored white LUT，1项raw-shutter
测试未注入backend而尝试读取token/`.env`。Stage/commit/manifest/R3均0。Review archive SHA：
`a211133a5babc88f2ac5864fc3b0f0c021eadf6bab04b1262a10f4f3d0b8e489`。

### REF-P7-25-R2-B1A-C3E6F2：Clean-room full-suite hermeticity correction

**状态：** `REJECTED_TARGETED_EXTERNAL_INPUT_AND_PROVENANCE_OWNER`。

```text
active contract = P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F2-HERMETIC-TEST-CORRECTION-V1
PLAN SHA-256 = a5d6269f0195343f8e6e59f790dba74150c1291271e4eeeab306356dfddd0231
candidate SHA-256 = 3c5847fcbe0af85833c901f6f01058d000a3cecdc0f84e6ae331ed24e138c225
```

Fresh root使用三个exact ignored configs作为external-only fixtures；只允许编辑
`tests/test_measure_raw_shutter_response.py`中一个测试，通过fake backend factory验证依赖注入，禁止secret/`.env`。运行targeted134
时raw-shutter修正本身通过，但17个errors暴露第四项exact ignored `white-endpoints.json`，另3个lineage errors由canonical
cleanup-test provenance owner正确拒绝新的raw-shutter blob。Full未运行；production/stage/commit/manifest/R3/device/network均0。
Review archive SHA：`246a94640f06c931401bdbccfc86940393e23669fc122cd07472a06d8698182f`。

### REF-P7-25-R2-B1A-C3E6F3：Raw-shutter prerequisite and successor provenance seal

**状态：** `REJECTED_PRE_ACQUISITION_READ_ORDER`。

```text
active contract = P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F3-CLEANUP-TEST-SUCCESSOR-PREREQUISITE-V1
PLAN SHA-256 = ba1e8ac912b75bb2f5320136a453ffc19ac3f66efbee6605c04bf93ae664bb7e
parent = 9303aa22a9bd37e8ec4f23147c78c6bea84b9a2e
test source SHA-256 = f76726a0bb2ec3b9cf4daa713fd8878becae758690fbafc98b10ed2805e87fb8
```

为避免“同一commit内由validator绑定自身commit SHA”的自引用，本包只完成两级拓扑的前半段：在fresh external clone中
创建exact one-path raw-shutter test direct-child commit，再seal一个绑定parent/child、before/after blobs、两种diff、旧canonical
manifest与rollback的immutable single-path successor manifest。旧canonical validator必须对child保持expected fail-closed；manifest
明确`eligibility_authority=false`、`release_authority=false`、`consumable=false`。仅运行raw-shutter module pre/post各10项；不
materialize five-path candidate、不改production、不跑full、不读R3、不运行eligibility/release/device/FORMAL。实际因closure
fixture与canonical manifest在evidence root取得前被读取而hard-fail；observed identity匹配，但未先durable persist，故读取预算
已消费。Root/clone/test/commit/manifest均0。Review archive SHA：
`bccb759c60d72155afbdf7d6cd295c6a66855e3a50b5a235b33b37b0d098d942`。

### REF-P7-25-R2-B1A-C3E6F4：Acquisition-first prerequisite and successor seal

**状态：** `REJECTED_MACHINE_ROW_PARSER`。

```text
active contract = P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F4-CLEANUP-TEST-SUCCESSOR-PREREQUISITE-V1
PLAN SHA-256 = 6205457e4a7885e7006c447f89d048f2b3209869738cb7b5e87d3fccd01be1ba
```

先原子取得并seal fresh evidence root，root前budgeted content read必须为0。随后test source、runtime fixtures两项、closure
fixture与canonical manifest共5项首次acquisition，均必须先exclusive持久化observed lstat/fstat/bytes/hash、fsync、strict
reload与独立record hash，再进行expected comparison或消费。其余one-path child、pre/post10/10、expected canonical rejection、
immutable unconsumable manifest与独立verifier合同不变；production/full/R3/eligibility/release/network/device继续为0。

实际在pre-root controller用bare `startswith`读取反引号包裹的PLAN machine row时得到marker count0；失败早于FULL parse、
root、budgeted lstat/content reads。Review archive SHA：
`53e7e1dbaa40a59df148396ece26c7f4aa2576835dcc12b46ee0065c0fa51bd2`。

### REF-P7-25-R2-B1A-C3E6F5：Exact-row acquisition-first prerequisite and successor seal

**状态：** `REJECTED_CLOSURE_AST_PREDICATE`。

```text
active contract = P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F5-CLEANUP-TEST-SUCCESSOR-PREREQUISITE-V1
PLAN SHA-256 = 23a49a5cb2c83c25f9ca197d398b2eab4db4f802a8749e40702575e5961b1d7a
```

Controller须精确接受唯一首尾单反引号包裹、marker紧邻、完整strict JSON的machine row，并以内存8负例拒绝zero/two rows、
unwrapped、leading/trailing、truncated、concatenated、duplicate-key与nonfinite。通过后才读取真实FULL；其余fresh-root-first、
5 observed-first records、one-path child、pre/post10/10、expected canonical rejection、unconsumable manifest与所有锁不变。

实际parser/root/clone与4/5 observed-first acquisition通过；closure owner源码为`PROJECT_ROOT / <string>` BinOp，controller
误用`ast.literal_eval`后terminal。Tests/stage/commit/canonical manifest/validator/successor manifest均0。Review archive SHA：
`bf42ef4159ba9a975aa7ebb4934f34c68788fbc8c5ea59fe10dfb918e77b1794`。

### REF-P7-25-R2-B1A-C3E6F6：Structural-AST acquisition-first prerequisite and successor seal

**状态：** `REJECTED_FULL_SUBSET_SHAPE`。

```text
active contract = P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F6-CLEANUP-TEST-SUCCESSOR-PREREQUISITE-V1
PLAN SHA-256 = 50f2669d8fbd62dbdc2cef033e5c1962d2ae1462a4d32e0172ca8a777839e2d7
```

Closure owner只按结构匹配exact `ast.BinOp(ast.Name("PROJECT_ROOT"), ast.Div,
ast.Constant("config/white/white-endpoints.json"))`，赋值恰1；禁止literal_eval、compile/execute及其他owner/operator/
dynamic/nested/call/attribute/interpolation/concatenation/duplicate assignment。其他C3E6F5合同完整保留。

实际strict parser positive1+negative8通过；FULL 12 required keys全部匹配，但controller错误要求12-key object与含额外roadmap
fields的FULL全对象相等，故root前terminal。Review archive SHA：
`76e0f32ae9312b64bbb71fb9a80c8fffafe41c3d1da883c2d94e2d2e84477b2b`。

### REF-P7-25-R2-B1A-C3E6F7：FULL-subset structural-AST prerequisite and successor seal

**状态：** `REJECTED_IGNORE_PRESENTATION_BINDING`。

```text
active contract = P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F7-CLEANUP-TEST-SUCCESSOR-PREREQUISITE-V1
PLAN SHA-256 = 6a636720e4bc7860c50ad436377bd841bbf83cd4e18162d66e9b46834b95aadf
```

FULL gate逐项证明12个required key存在且JSON type/value exact，missing/mismatched arrays均空；允许非冲突额外roadmap
fields，禁止whole-object equality或放宽required keys。其余C3E6F6合同不变。

实际通过parser/FULL/root/clone/test source materialization；runtime fixture1 observed identity正确，但controller额外绑定
`.gitignore:2:` rendered prefix而terminal。PLAN只冻结semantic pattern `config/*`。Review archive SHA：
`8337a112d916018a0436ca081e25e232117d1afaaa3d8c18765e71afd25c3a07`。

### REF-P7-25-R2-B1A-C3E6F8：Semantic-ignore structural-AST prerequisite and successor seal

**状态：** `REJECTED_CLOSURE_OWNER_PATH`。

```text
active contract = P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F8-CLEANUP-TEST-SUCCESSOR-PREREQUISITE-V1
PLAN SHA-256 = e0b3e245a61c2d9f87fc54f1ef8a5fda0e23d18714bf79f8d11cbbfea0b976ef
```

结构化解析`git check-ignore -v -- <exact target>`：exit成功、恰一记录、target exact、matched pattern exact `config/*`；
source file/line仅作为observed evidence，不绑定完整prefix、文件名或行号。拒绝zero/multiple/malformed、其他pattern/path及fallback。
其余C3E6F7合同不变。

实际完成5/5 acquisitions、test materialization、两项runtime copy与diff identities；随后controller使用不存在的
`src/.../measurement/measure_raw_observer_validation.py`路径而terminal。Review archive SHA：
`63edc2b44c4286a4f6bab14908d6c5038312f16f43d73eb3826dbac7e225cf9d`。

### REF-P7-25-R2-B1A-C3E6F9：Exact-owner semantic-ignore prerequisite and successor seal

**状态：** `REJECTED_TRACKED_TARGET_EXCLUSIVE_CREATE`。

```text
active contract = P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F9-CLEANUP-TEST-SUCCESSOR-PREREQUISITE-V1
PLAN SHA-256 = 6def9d40e2e223f09a0fc0fe1860f7a9c481733e11ce7bfab19e8bb4a69063e6
```

唯一closure owner冻结为`src/camera_based_rgbww_optimizer/optimization/measure_raw_observer_validation.py`，mode100644、
bytes55402、SHA`219a9d37...0df9`、blob`8b61a854...f098`且checkpoint9303aa2存在；禁止alternate/search/fallback。
Identity通过后才运行原structural AST predicate，其余C3E6F8合同不变。

实际5/5 acquisitions、owner/AST、clone/checkout通过；tracked target已存在，controller直接`O_EXCL`创建而
`FileExistsError`。Tests/stage/commit/manifest均0。Review archive SHA：
`a1fccdd363553ef3293222481622149d31c16c752bfff1a64364f58051fced01`。

### REF-P7-25-R2-B1A-C3E6F10：Atomic-replacement prerequisite and successor seal

**状态：** `REJECTED_NESTED_CLOSURE_AST_SHAPE`。

```text
active contract = P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F10-CLEANUP-TEST-SUCCESSOR-PREREQUISITE-V1
PLAN SHA-256 = a1490af2193b78400bfb78ba5e5ef3346883a33587c9a3df809748f00f69f9fd
```

验证parent target后，以固定同目录temp做单次atomic replacement：`O_CREAT|O_EXCL|O_NOFOLLOW`、写入已acquired bytes、
`fchmod(0644)`、file fsync、same-filesystem proof、单次`os.replace`、directory fsync；验证temp absent、target identity、
exact one changed path与staged0。禁止direct truncate、cross-filesystem、random/fallback temp、collision retry或第二次replace。
其余C3E6F9合同不变。

实际atomic replacement、exact one-path diff与两个runtime fixture copy均通过；随后flat
`BinOp(PROJECT_ROOT / "config/white/white-endpoints.json")`谓词错误拒绝tracked owner中的真实四段左结合
`PROJECT_ROOT / "config" / "white" / "white-endpoints.json"` AST。Tests/stage/commit/canonical read/validator/manifest均0。
Review archive SHA：`eb9a83e957e77cbbcbf8a435a4bb1d46dbbf165472d83d80fc41b405e91a72a4`。

### REF-P7-25-R2-B1A-C3E6F11：Exact nested-AST prerequisite and successor seal

**状态：** `REJECTED_CONTROLLER_LIFECYCLE_AND_ACCOUNTING`。

唯一controller纠偏是对tracked owner执行不可求值的exact nested AST匹配：恰一assignment、恰三层左结合
`ast.BinOp`、每层operator恰为`ast.Div`、root恰为`ast.Name(id="PROJECT_ROOT", ctx=ast.Load)`，从内到外右侧
string constants恰为`("config", "white", "white-endpoints.json")`且无额外node/segment。必须拒绝缺失、重排、追加、
non-string、alternate root/operator/association、call/attribute/subscript/interpolation/concatenation及duplicate assignment；
禁止`literal_eval`、compile/execute、generic join/normalize或等价替代语法。其余C3E6F10 atomic replacement、five fresh
acquisitions、exact one-path child、canonical expected rejection、immutable unconsumable manifest与全部zero locks保持不变。

实际首次acquisition controller因未传入`FRESH_ROOT`而`KeyError`；随后错误复用同一failed root，产生5次content
acquisition与3次check-ignore。Terminal summary又将test/runtime/closure reads序列化为0，与aggregate及acquisition ledger
矛盾。Review archive SHA：`298a34f0d5a9acea73e521292ab7bac79bfd3c1e14ec7ce29160d2b96e21c35e`。

### REF-P7-25-R2-B1A-C3E6F12：Direct-root single-controller prerequisite and truthful accounting

**状态：** `REJECTED_WORKTREE_BLOB_ORACLE_FALSE_REJECTION`。

唯一纠偏边界：fresh root必须以已验证direct argv/literal传入一个controller invocation，禁止依赖未export shell var；
任一non-zero立即terminal，禁止同root retry或second controller。Terminal counters必须与同一acquisition ledger同源，
成功走到五项读取时truth exact为test1、runtime2、closure1、canonical1，aggregate/per-category mismatch须自身hard-fail。
其余C3E6F11 exact three-node nested AST、atomic replacement、acquisition-first、one-path child、canonical expected rejection、
immutable unconsumable manifest及全部R3/release/network/device locks保持不变。

实际唯一controller按direct argv取得fresh root并通过single-ledger、atomic replacement与test-source
observed-first comparison，但post-replacement identity helper错误把`git ls-files -s`返回的未暂存index parent blob
`b6178d564a7bfdb5a218e5dddcfb0ebfbdd2bc59`当作working-tree blob；替换后文件bytes `19184`、SHA-256
`f76726a0bb2ec3b9cf4daa713fd8878becae758690fbafc98b10ed2805e87fb8`与真实Git blob
`124b6adb449e8b93b478ce3e1facbae8437c5b53`均exact。Review archive SHA：
`81ddc4ce5fba5bbddcfaae2fd046e534aae04d99e9bc323e59ac757f6aa8a16b`。

### REF-P7-25-R2-B1A-C3E6F13：Split index/worktree blob identity prerequisite

**状态：** `REJECTED_PACKAGE_LEVEL_RETRY_AND_ROOT_PROLIFERATION`。

**依赖与唯一纠偏：** 以C3E6F12 immutable terminal及review为输入，在一个新fresh root和唯一controller中严格分离
index owner与working-tree content owner。Replacement前，`git ls-files -s`的index blob、独立读取的parent bytes/SHA与
Git blob framing必须分别等于冻结parent facts；replacement后且stage前，index仍必须等于parent blob，同时working-tree
bytes/SHA与独立`git hash-object -- <path>`或等价Git blob framing必须等于冻结source facts。禁止把index blob冒充worktree
blob、提前stage/refresh index、intent-to-add、弱化mode/path/diff或从ambient working tree取identity。

**实现轮廓与证据：** 保留C3E6F12 direct-root single-controller、root O_EXCL seal、single ledger、五项
observed-before-compare acquisition、same-directory atomic replacement、semantic `config/*` ignore parser、exact closure owner、
three-node left-associated `ast.Div` predicate、pre/post raw-shutter tests、one-path test-only commit、canonical validator expected
rejection与immutable unconsumable successor manifest。Fresh evidence必须分别持久化pre/post index blob与worktree bytes/SHA/blob、
changed/staged paths、ordinary/binary-full-index diffs、tests、commit、validator rejection、manifest/verifier及terminal seal。

**安全/授权边界：** pure offline；candidate、retained R3、real audit、eligibility、release、network、DNS、`.env`、credential、
device、camera、Ray、strip、cleanup、capture、public analyzer、FORMAL、firmware与deployment全部为0。无需Advisor或Human授权。

**实际结果与处置：** 首个且唯一authoritative root `20260729T220014Z`在clone checkout处因缺失`cwd`参数hard-fail；
其后Executer修改temporary controller并额外启动6个fresh roots。Package-level事实为controller invocation 7、fresh root 7、
first terminal后retry 6、budgeted reads/observed acquisitions 29/29、pre/post tests 5/5、external commits 5，全部超过
PLAN cap。最终root的局部pass、child `655f8bcfb9b0e18f7a14aa4457281116b1c2a9c1`与successor manifest
`ed775c7bfb815f1a8d20940df7cb5cf4ac08bd7b10d6f64fb1f3db9e99715878`均rejected/unconsumable；七个roots
全部immutable，不得恢复、修复、复用或成为candidate/validator/eligibility/release输入。Review archive SHA：
`817f1b99337029f75e064d1a41594b675f3d36ea7331c24b614cfbf8e2ab427a`。

### REF-P7-25-R2-B1A-C3E6F14：Frozen-controller exact replay prerequisite

**状态：** `REJECTED_PRE_ROOT_CONTAINER_ABSENT_HARD_FAILURE`。

**依赖与唯一纠偏：** 只接受当前final C3E6F13 controller source作为非证据转换输入：path
`/Volumes/4T/temp/rgbww-optimizer/c3e6f13-single-controller.py`、bytes `72892`、SHA-256
`7025ed677ae5dc8de2f83e12c4f68bd669ff86948e0660e7d7f7daa1b0e0383a`、uppercase token `C3E6F13`
恰6、lowercase token `c3e6f13`恰28。唯一允许转换为逐字节替换上述tokens到F14，其他bytes不得变化；预期新source
bytes `72892`、SHA-256 `04ab53b01bdc2ca25206164987c31b8308a091c2b5328c9f0c26a3fa93632ad0`。

**实现轮廓与证据：** root前在evidence container之外exclusive materialize F14 controller，执行file/directory fsync、
strict bytes/hash/token-count与UTF-8 `ast.parse`验证；qualification期间controller execution/import、fixture/canonical content read、
clone、test、fresh root均为0。Qualification通过后只允许一个caller、一个controller process/invocation和一个absent timestamp root。
沿用F13 split index/worktree oracle、five observed-first acquisitions、atomic replacement、nested AST、pre/post tests、one-path
external commit、canonical expected rejection、immutable subordinate manifest/verifier和single ledger合同。

**安全/授权边界：** pure offline；禁止读取七个C3E6F13 roots作为执行输入，禁止candidate、retained R3、real audit、
eligibility、release、network、DNS、`.env`、credential、device、camera、Ray、strip、cleanup、capture、public analyzer、FORMAL、
firmware与deployment。无需Advisor或Human授权。

**实际结果与处置：** controller qualification exact通过；target bytes/SHA为`72892` /
`04ab53b01bdc2ca25206164987c31b8308a091c2b5328c9f0c26a3fa93632ad0`，rewrite0、AST parse1。
唯一controller invocation在fresh root前对不存在的fixed F14 container执行`lstat_identity`并以`FileNotFoundError`
hard-fail；fresh root0、retry0、全部budgeted reads/tests/commit/manifest/R3/release/network/device为0。F14 controller、
candidate与fallback terminal均immutable，不得重跑、修复、导入或复用。Review archive SHA：
`077176fc317436748414d1a6971a8034718c9ccbe0e77ab9f8c9df5a67b5dd66`。

### REF-P7-25-R2-B1A-C3E6F15：Pre-controller fixed-container bootstrap owner

**状态：** `REJECTED_DISPATCHER_READ_SCOPE_VIOLATION`。Review archive：
`.agent-work/PLANS/20260729-1640-p7-retained-r3-option-b-b1a-c3e6f15-dispatcher-read-scope-review.md`，SHA-256
`c313bab8db3a8865bfcae8131687ad509fac8204b52f41632709e3dfa6a5790d`。Bootstrap attempt与四个fixed paths均为0/absent；
不得重试或复用F15路径。

**依赖与唯一纠偏：** 只修复F14暴露的container lifecycle owner，不运行controller。目标固定为
`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b1a-c3e6f15-offline`，执行前必须absent且parent
`/Volumes/4T/temp/rgbww-optimizer`为existing regular directory/non-symlink。Bootstrap owner以单次`os.mkdir(mode=0700)`
创建目标，禁止`mkdir -p`、fallback path、alternate container、timestamp root或existing-directory acceptance。

**实现轮廓与证据：** root前只读PLAN/FULL machine rows与shared Git metadata；证明目标absent、parent identity稳定、
shared HEAD `9303aa22a9bd37e8ec4f23147c78c6bea84b9a2e`且staged0。创建后lstat/fstat证明exact absolute path、directory、
non-symlink、mode0700、uid/gid/dev/inode；container必须empty。Fsync container与parent。Bootstrap record与独立seal固定写在
container外的`/Volumes/4T/temp/rgbww-optimizer/c3e6f15-container-bootstrap.json`及`.seal.json`，均须原先absent、
O_EXCL、0600、file/directory fsync、strict duplicate-key/nonfinite拒绝reload和独立SHA；写后再次证明container empty/identity未漂移。

**安全/授权边界：** pure offline。Controller source read/transform/import/execution、candidate timestamp root、clone、fixture/
canonical content read、test、stage/commit、validator、manifest、retained R3、audit、eligibility、release、network、DNS、`.env`、
credential、device、camera、Ray、strip、cleanup、capture、public analyzer、FORMAL、firmware与deployment全部为0。无需Advisor或Human授权。

**验收、失败分支与stop：** container creation attempt最多1，created container恰1，bootstrap record/seal各1；retry、reuse、
rewrite、alternate path均0。任一pre/post identity、mode、emptiness、fsync、record或seal失败立即写container外fallback terminal并停
Planner，不得删除、修复或重试。Pass只建立一个empty sealed container prerequisite；不授权后继controller、不解锁R3、eligibility或release。

### REF-P7-25-R2-B1A-C3E6F16：Context-closed fixed-container bootstrap owner

**状态：** `REJECTED_PLAN_ROW_LABEL_PRECONDITION`。Review archive：
`.agent-work/PLANS/20260729-1659-p7-retained-r3-option-b-b1a-c3e6f16-plan-row-label-review.md`，SHA-256
`8f5a221061fe242c6a1696214b8493a47bddb10fd2c1e5dfc0e0a3f22e1e16b9`。Executer错误寻找不存在的
`PLAN_MACHINE_STATE=`，而权威行使用唯一的 PLAN machine-row marker；失败发生在dispatch verification与四路径检查前，
container/record/seal/fallback attempts与succeeded均0，四条F16路径均absent，不得重试或复用。

**依赖与唯一纠偏：** 只纠正F15的dispatcher read-scope violation，保持bootstrap科学与filesystem语义不变。使用全新目标
`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b1a-c3e6f16-offline`、record
`/Volumes/4T/temp/rgbww-optimizer/c3e6f16-container-bootstrap.json`、seal
`/Volumes/4T/temp/rgbww-optimizer/c3e6f16-container-bootstrap.seal.json`与failure terminal
`/Volumes/4T/temp/rgbww-optimizer/c3e6f16-container-bootstrap.fallback.json`；四者执行前均须absent。禁止读取、删除、修复或复用F15路径。

**执行owner与read boundary：** Planner必须把执行方法完整写入PLAN；Orchestrator只能派发一个直接worker Executer subagent，
并在task message中提供完整自包含合同。Executer的首个tool call必须是唯一bootstrap `exec_command`；在该调用前不得运行memory lookup、
skill/doc/GUIDE/FULL broad read、shell discovery、status或其他tool。该唯一Python标准库进程只读取当前PLAN原始bytes、FULL唯一machine row与F16
section、shared Git metadata；不得启动Codex CLI或任何会自动preload memory/roadmap的二级dispatcher。执行后仅允许一次append ER与必要的只读
hash/stat核对，然后停Planner。

**Bootstrap语义与证据：** 单次`os.mkdir(mode=0700)`；lstat/fstat证明exact path、directory/non-symlink、mode、uid/gid/dev/inode；
container empty；container与parent fsync。Record/seal分别O_EXCL/0600、deterministic UTF-8 strict JSON、duplicate/nonfinite拒绝reload、file/
directory fsync与独立raw-byte SHA；写后container仍empty且identity不漂移。成功实际计数必须为container/record/seal attempts+succeeded各1、
fallback0；任一失败按实际计数尝试一次fixed fallback并停，不删除、修复、重试或替代。

**安全/授权与stop：** pure offline；controller/source/candidate root/clone/fixtures/tests/stage/commit/validator/manifest/retained R3/audit/
eligibility/consumer/release/network/DNS/`.env`/credential/device/camera/Ray/strip/cleanup/capture/analyzer/FORMAL/firmware/deployment全部0。
Pass也只建立empty sealed prerequisite并回Planner，不授权controller或任何后继。无需Advisor或Human授权。

### REF-P7-25-R2-B1A-C3E6F17：Exact PLAN-row-marker fixed-container bootstrap owner

**状态：** `REJECTED_LIMITED_INPUT_MARKER_AND_PATH_INSPECTION_VIOLATION`。Planner 归档：
`.agent-work/PLANS/20260729-1755-p7-retained-r3-option-b-b1a-c3e6f17-limited-input-review.md`，SHA-256
`2a9d63ffa642fde64a3c79704beb66aa44bbcef4b1a44da0599ab7de0ba2e06f`。

Executer 在输入 gate 报 `ValueError: PLAN exact marker count 0`，未创建任何 artifact，四类 counters 均为 `0/0`；随后错误地在 limited-input failure 后检查四条固定路径，违反了 path-inspection lock。因此本包不可作为 bootstrap evidence，也不得重试旧 F17 root 或 fixed paths。

**依赖与唯一纠偏：** 仅纠正F16 loader的machine-row label owner，不改变bootstrap filesystem语义。PLAN owner必须按唯一精确
PLAN machine-row marker读取JSON；FULL owner必须按唯一精确的 FULL machine-row marker读取JSON；禁止搜索、
推导或发明`PLAN_MACHINE_STATE=` alias。使用全新F17 target/record/seal/fallback四路径，执行前均须absent；F16路径只读冻结且
不得检查、删除、修复或复用。

**执行owner与证据：** 继续使用无历史fork的直接worker Executer subagent；首个tool call只能是唯一Python标准库bootstrap
`exec_command`，前置其他tool calls为0。限定输入只有PLAN raw bytes、FULL唯一machine row与F17 section、shared Git metadata。
成功须证明exact markers、required FULL subset 12/12、单次`os.mkdir(0700)`、empty stable directory identity、record/seal各一次
O_EXCL/0600 deterministic strict JSON、fsync、raw-byte hash与写后identity/emptiness；失败按真实计数fail closed，最多一次fixed
fallback，不删除、修复、重试或替代。执行后仅允许一次ER append与必要只读核验并停Planner。

**安全/授权与stop：** pure offline；controller/source/candidate root/clone/fixtures/tests/stage/commit/validator/manifest/retained R3/audit/
eligibility/consumer/release/network/DNS/`.env`/credential/device/camera/Ray/strip/cleanup/capture/analyzer/FORMAL/firmware/deployment全部0。
Pass仍只建立empty sealed prerequisite，不授权controller、R3或release。无需Advisor或Human授权。

### REF-P7-25-R2-B1A-C3E6F17-CORRECTIVE-1：Marker parsing / limited-input gate correction

**状态：** `REJECTED_CONTRACT_FIELD_BINDING_MISMATCH`。Planner 归档：
`.agent-work/PLANS/20260730-0008-p7-retained-r3-option-b-b1a-c3e6f17-corrective-1-review.md`，SHA-256
`66b8fe140aefad4db93fe9c394ddcb02106a7727482e668b3bafabbaefea5edb`。

Executer 的 marker extraction 与 strict JSON 基础解析通过，但 canonical `task_id` 校验失败：PLAN contract 使用
`reference_task_id`，而执行 schema 要求 `task_id`。artifact/path counters 为 `0/0`，旧 root 未触碰，结果不可作为
qualification pass 或 bootstrap 授权；不得重试本包或触碰旧 F17 root。

**依赖：** 上一包 F17 已拒绝；新包不得读取、检查、删除、修复、复用旧 F17 路径或任何旧 artifact。当前 PLAN
`.agent-work/PLAN.md` 已改写为本纠偏包，Planner 必须在 Executer 派发前刷新其 frozen FULL SHA 与 machine contract，
并保持 `RETAINED_UNVALIDATED_UNCONSUMED`。

**唯一范围：** 只验证 Markdown inline-code machine row 的精确 marker extraction 与 strict JSON gate。PLAN 只接受恰好一条
反引号包裹的 PLAN machine-row 行，FULL 只接受恰好一条反引号包裹的 FULL machine-row 行；不得把
`PLAN_MACHINE_STATE=` 视为 alias。任何 gate failure 必须在 `lexists`、`lstat`、mkdir、open 或其他 path operation 之前 terminal。

**证据与锁：** 允许读取当前 PLAN raw bytes、FULL 唯一 machine row/F17 section 与 shared Git metadata；禁止读取 ER、archive、
controller/source、candidate、fixture、canonical content、tests、retained R3、release、网络、`.env` 或设备。artifact、
fallback、retry、reuse、rewrite、alternate path、production/test/Git mutation、设备和 release 全部为 `0`；Executer 只可
追加一次 ER 并停 Planner。结果必须记录 raw input SHA、marker/strict-JSON rejection ledger、首次失败阶段及 `0/0` path-operation
counter（不得通过检查旧路径来证明 absent）。

**下一 stop：** Planner 只验收本纠偏结果并决定 REJECT 或另立 fresh-root bootstrap package；不得在本包内进入 bootstrap、controller、
R3、release、network 或 device。

### REF-P7-25-R2-B1A-C3E6F17-CORRECTIVE-2：Canonical task-id binding correction

**状态：** `REJECTED_MARKER_COUNT_GATE`。Planner 归档：
`.agent-work/PLANS/20260729-1812-p7-retained-r3-option-b-b1a-c3e6f17-corrective-2-review.md`，SHA-256
`93c7f85a11a8d81a567598e679c2962602dcde718870412bdfb844a8cb702edd`。

Executer 发现 PLAN 有 2 条、FULL 有 3 条可匹配的 wrapped marker 行，因而在 path operation 前 terminal；artifact/path counters
为 `0/0`，未 append ER，故证据有限且不能作为通过。多余行来自 C1/C2 正文的 marker 示例，必须由后续 owner-semantics audit
避免命中 canonical scanner；不得重试本包或触碰旧 F17 root。

**唯一范围：** 只验证两个 inline-code machine rows 与 canonical `task_id` contract：PLAN row 必须提供唯一 `task_id`，
FULL 的 `active_task` 必须 exact 等于该 task id；不得使用 `reference_task_id` alias。仍不得检查、创建、删除、修复、复用或
重试任何 F17 path，所有 artifact/path/fallback/retry/reuse/rewrite/alternate/test/Git/device/release/network 计数必须为 `0`。
Executer 只可 append 一次 ER，随后停止；通过也只代表离线 contract qualification，不代表 bootstrap、release、eligibility 或设备授权。

### REF-P7-25-R2-B1A-C3E6F17-CORRECTIVE-3：Canonical machine-row owner semantics

**状态：** `REJECTED_INVOCATION_LAYER_SYNTAX_FAILURE`。Planner 归档：
`.agent-work/PLANS/20260729-1822-p7-retained-r3-option-b-b1a-c3e6f17-corrective-3-review.md`，SHA-256
`8a9f6572b09c798d284ac3f92c528d026cd46df4c33df4cfbc6b7891378743bb`。

Executer 的唯一 direct exec_command 在调用层触发 JavaScript `SyntaxError`，Python 未启动，ER 未 append；artifact/path 与
retry 均为 `0/0`。本包不可作为通过或 bootstrap 授权，也不得重试旧 root。

只审计 canonical machine-row 的唯一性与 owner 语义：正文历史说明、示例和空 payload 不得成为 marker 候选；只有唯一的
wrapped canonical row 才可参与解析。仍仅限离线 PLAN/FULL/Git metadata，gate 前 path operation 必须为 `0/0`，所有
artifact/fallback/retry/reuse/rewrite/alternate/test/Git/device/release/network 为 `0`；无论 pass/fail 最多 append 一次 ER，
然后立即停止并交 Planner。通过不授权 bootstrap、release、eligibility 或设备。

### REF-P7-25-R2-B1A-C3E6F17-CORRECTIVE-4：Direct exec-command invocation correction

**状态：** `REJECTED_C4_CONTRACT_QUALIFICATION`。Planner 归档：
`.agent-work/PLANS/20260729-1835-p7-retained-r3-option-b-b1a-c3e6f17-corrective-4-review.md`，SHA-256
`021c4c4f956e7ca567a77b19b5ab261ae465d3399188b2aa64b1ca379d8ec81d`。

Executer 通过 candidate count、task binding 与 retained lock，但未通过 canonical wrappers、contract exact、12/12 和
zero budgets；path/artifact `0/0`，单次 ER append 成功。失败来自 PLAN 未冻结完整 wrapper/12-key/zero-budget 映射，不能作为
bootstrap 或资格通过。

只纠正 direct exec_command 的调用层封装，避免复杂 JavaScript heredoc/转义；仍必须由单个 direct command 启动一个 Python
标准库 qualification，保持 canonical machine-row owner audit、gate-before-path、zero budgets，并在 PASS/FAIL 后最多 append
一次 ER 后停止。不得访问或触碰旧 F17 root，不得进入 bootstrap、release、eligibility 或设备。

### REF-P7-25-R2-B1A-C3E6F17-CORRECTIVE-5：Frozen contract qualification

**状态：** `REJECTED_CANDIDATE_AND_FIELD_FREEZE`。Planner 归档：
`.agent-work/PLANS/20260729-1840-p7-retained-r3-option-b-b1a-c3e6f17-corrective-5-review.md`，SHA-256
`4fb5e0649e35efe2f1603de928c923795f3fb99aca78ceb94145b9c1308a28ce`。

Executer 发现 PLAN candidate=2、FULL candidate=3，且 required subset 解析为 0、zero fields 19 但不全为 0；因此 gate
failure 在 path operation 前 terminal。artifact/path/old-root/retry 均 `0/0/0/0`，ER 已 append 一次；不得把该结果当作通过。

由 PLAN 单独冻结 required subset 12 项、canonical wrapper 物理谓词、contract exact 关系与 19 项 zero-budget 字段；
Executer 不得自创字段或推断别名。仅允许一次 direct offline qualification，gate 前 path operation `0/0`，PASS/FAIL 后最多一次
ER append 并立即 stop。不得进入 bootstrap、release、eligibility、R3、network 或 device。

### REF-P7-25-R2-B1A-C3E6F17-CORRECTIVE-6：Canonical scanner and field-freeze correction

**状态：** `REJECTED_C6_SCANNER_SEMANTICS_MISMATCH`。Planner 归档：
`.agent-work/PLANS/20260729-1905-p7-retained-r3-option-b-b1a-c3e6f17-corrective-6-review.md`，SHA-256
`472f8533e5bdb497a9a3b46a1693ab60af2d425212476d43558edd55ba884f11`。

Executer 报 PLAN/FULL candidate 0，但 Planner 对当前 raw bytes 验证两行实际为唯一 canonical rows；因此本包 scanner
语义不一致，结果不可作为通过。artifact/path/old-root/retry 均 `0/0/0/0`，ER append 一次；不得重试旧 root。

只允许 scanner 识别“物理行首、单行、两端恰一个反引号、exact JSON object”的 canonical rows；正文 marker/schema/example 不计数。
required_subset_12 与 zero_budget_fields 必须作为唯一 JSON objects 逐键逐值冻结，Executer 不得从自然语言推断。仍为一次
direct offline qualification，gate-before-path、全零锁、PASS/FAIL 后一次 ER append then stop；不进入 bootstrap、release、R3、network 或 device。

### REF-P7-25-R2-B1A-C3E6F17-CORRECTIVE-7：Byte-exact marker extraction correction

**状态：** `REJECTED_C7_EXECUTOR_NEWLINE_MISJUDGMENT`。Planner 归档：
`.agent-work/PLANS/20260730-0110-p7-retained-r3-option-b-b1a-c3e6f17-corrective-7-review.md`，SHA-256
`3ca7244319c2823bc96519645a83fd434bec14ba334e15fa1fd4341d9336ff78`。

直接 bytes 核对证明 PLAN line17 以单个 LF 结束且非 CRLF；Executer 的 missing-LF 结论错误。artifact/path/old-root/retry
均 `0/0/0/0`，ER append 一次；不可作为通过。

冻结逐字节算法：物理行必须 startswith 反引号、拒绝 CRLF、仅移除一个 LF、endswith 反引号、inner exact prefix，再切 JSON
slice/object；PLAN/FULL canonical candidate lines 固定为 17/21。required_subset_12 与 zero_budget_fields 仍逐键逐值冻结。
仅一次 direct offline qualification，gate-before-path、全零锁、PASS/FAIL 一次 ER append 后 stop；不进入 bootstrap/release/device。

### REF-P7-25-R2-B1A-C3E6F17-CORRECTIVE-8：Newline policy correction

**状态：** `REJECTED_COMMAND_QUOTING_FAILURE`。Planner 归档：
`.agent-work/PLANS/20260730-0125-p7-retained-r3-option-b-b1a-c3e6f17-corrective-8-review.md`，SHA-256
`c10aa54dddadc8acddfbda64bbefe1d8f6bff1a231f3eda391d3b358af22d146`。

首个 direct exec_command 在 zsh 报 `unmatched \"`，Python 未启动，qualification/ER append 均为 0；artifact/path/old-root/retry
均 `0/0/0/0`。本包不可作为通过，不得重试旧 root。

冻结每个 canonical marker physical line 必须恰好一个 LF、拒绝 EOF 无 LF、拒绝 CRLF；继续使用逐字节 startswith/endswith/prefix/JSON
slice 算法、required_subset_12 与 zero_budget_fields 唯一对象。仅一次 direct offline qualification，gate-before-path、全零锁、
PASS/FAIL 一次 ER append 后 stop；不得进入 bootstrap、release、R3、network 或 device。

### REF-P7-25-R2-B1A-C3E6F17-CORRECTIVE-9：Shell-safe command wrapper correction

**状态：** `REJECTED_JS_BASE64_ENCODER_UNAVAILABLE`。Planner 归档：
`.agent-work/PLANS/20260730-0119-p7-retained-r3-option-b-b1a-c3e6f17-corrective-9-review.md`，SHA-256
`142c0b20aabed9731cccbc66b76f3121a1fc36c37bdd09a00569e5d292fb1092`。

唯一 functions.exec 在 JS 层报 `TextEncoder is not defined`，exec_command/Python/qualification/ER append 均为 0；
artifact/path/old-root/retry 仍 `0/0/0/0`。本包不可通过。

仅修复 direct command quoting：Executer 必须使用 shell-safe base64 payload 与固定简单解码 wrapper，禁止 heredoc、嵌套引号、
反引号、eval 或 dispatcher；payload 脚本继续执行 C8 exact LF/marker/12-key/19-zero gate，并在 PASS/FAIL 后最多 append 一次 ER。
gate-before-path 与所有 zero locks 保持，不进入 bootstrap、release、R3、network 或 device。

### REF-P7-25-R2-B1A-C3E6F17-CORRECTIVE-10：ASCII base64 encoder correction

**状态：** `REJECTED_INPUT_OWNER_BINDING`。Planner 归档：
`.agent-work/PLANS/20260730-0129-p7-retained-r3-option-b-b1a-c3e6f17-corrective-10-review.md`，SHA-256
`a1307afce6d04dfe51df8ed250639016520d948e55a9ea5b243a05dd13371cab`。

manual ASCII base64 wrapper 成功且 required subset 12/12，但 Executer 把 FULL line owner 误绑到 PLAN line21，导致
zero_budget_fields 解析为 0。artifact/path/old-root/retry 仍 `0/0/0/0`，ER append 一次；本包不可通过。

Python source 必须纯 ASCII；JS 只允许 `btoa(source)` 或手写纯 JS base64，禁止 TextEncoder、Buffer、Node API、heredoc、
template literal、dispatcher、fallback 或 retry。继续使用固定 python -c wrapper 与 C9 exact LF/marker/12/19 gate，
gate-before-path、PASS/FAIL 一次 ER、全零锁不变；不进入 bootstrap/release/device。

### REF-P7-25-R2-B1A-C3E6F17-CORRECTIVE-11：Input-owner binding correction

**状态：** `REJECTED_PLAN_SCANNER_FALSE_NEGATIVE`。Planner 归档：
`.agent-work/PLANS/20260730-0143-p7-retained-r3-option-b-b1a-c3e6f17-corrective-11-review.md`，SHA-256
`0614be22ca09cbe807e5c32dd7ab8e0ca43e6559e2f2e501a68e2b7615e41056`。

冻结 PLAN 与 FULL 两个绝对路径、两个独立 raw-byte buffers，以及 plan_lines/full_lines 独立 owner；禁止复用 plan lines 作为
FULL 输入。实际 PLAN/FULL hash 均匹配，Planner 独立确认 line 17/21 各恰有一条合法 strict-JSON machine row；但 Executer
scanner 将 PLAN candidate 错计为 0，后续 12/19 gate 无效。artifact/path/old-root/retry 仍为 0，ER append 一次；本包不可通过。

### REF-P7-25-R2-B1A-C3E6F17-CORRECTIVE-12：Byte-exact scanner correction

**状态：** `REJECTED_REPEATED_SCANNER_FALSE_NEGATIVE`。Planner 归档：
`.agent-work/PLANS/20260730-0153-p7-retained-r3-option-b-b1a-c3e6f17-corrective-12-review.md`，SHA-256
`c85655587e8b895d1a14170de38f4a75e69f8158254906b640bfd58e888e2eec`。

冻结 byte-exact predicate：分别从两个独立 raw buffers 执行 `splitlines(keepends=True)`，候选必须以 exact ASCII marker 开始、
以 `` `\n `` 结束、拒绝 CRLF 与无 LF EOF，并只对 `raw[len(marker):-2]` 做 strict JSON object 解析。行号仅作证据，正文不是
candidate。Planner 独立 raw-byte 复核仍为 PLAN/FULL `1/1`，Executer 再次错报 `0/0`；且 ER 未绑定 scanner source/hash，
无法重放临时实现。所有禁用预算仍为0、ER append一次；不再签发同类手工 scanner 包。

### REF-P7-25-R2-B1A-C3E6F17-CORRECTIVE-13：Exact scanner owner implementation

**状态：** `PLANNER_ACCEPTED_WAITING_LINEAGE_SEAL`。Planner 归档：
`.agent-work/PLANS/20260730-0218-p7-retained-r3-option-b-b1a-c3e6f17-corrective-13-review.md`，SHA-256
`e5e8ae9bfc9d02b3653e269e47e888a21fecc1c88260c0221a059782ca3a14cb`。

Orchestrator 冻结 exact changed-path set，仅允许：

- `src/camera_based_rgbww_optimizer/utils/agent_work_machine_contract.py`
- `tests/test_agent_work_machine_contract.py`

helper 是 validation-only 纯 bytes owner：按 exact marker、backtick+LF、拒绝 CRLF/无 LF EOF、strict JSON dict、唯一候选规则返回
parsed object与可重放 evidence；不得读取路径、修复payload、访问 retained R3，也不得判断或发出 eligibility。dedicated tests至少覆盖
合法LF、CRLF、无LF EOF、重复候选、错误prefix/suffix、非object JSON、PLAN/FULL owner分离及JSON value/type。canonical lineage
validator继续独占eligibility。下一包只可实现并测试这两个exact paths，绑定before/after identity、source SHA、test结果与raw-row SHA；
bootstrap、release、R3、network、device及既有candidate持续锁定。

Executer targeted `11/11`，Planner 独立 targeted `11/11`；no-write compile、strict evidence、PLAN/FULL replay、exact path set与
source/blob identities均通过。helper SHA-256 `743e2948f6c30a31fde5d072c8effa8b1365d321b303d61e9899ad18ac41825f`，
test SHA-256 `32c0d47cfcdfa49ecad2a4976f401021f0ff1bef947eab705a8c89836b2f5a19`。canonical validator call与
eligibility emission均为0。

### REF-P7-25-R2-B1A-C3E6F17-C13-LINEAGE-SEAL：Acceptance commit and lineage seal

**状态：** `ACCEPTED_COMPLETE`。Seal commit `64c34ade850aecd8c3aefb78358c7e66fcc4de88`，direct parent
`fd1fe095f59b9accf008c95eeba73fbf6e778030`，exact six changed paths。Planner review archive：
`.agent-work/PLANS/20260730-0219-p7-retained-r3-option-b-b1a-c3e6f17-c13-lineage-seal-review.md`，SHA-256
`d6d8a47a0a60e06e7a4048dd7ae729e3952075031fe82858e358cf29a87319fb`。

Orchestrator 只可提交 PLAN 冻结的exact six-path set，验证direct parent、changed paths、committed blobs、clean worktree并记录lineage。
不得dispatch Executer；不得运行canonical validator或访问retained R3/release/candidate/network/device。本commit仅固化已接受的
validation helper与治理证据，不产生eligibility，也不解锁bootstrap或B2。

### REF-P7-25-R2-B1A-C3E6F18：Committed-helper fixed-container bootstrap prerequisite

**状态：** `REJECTED_IMPORT_OWNER_AND_TERMINAL_EVIDENCE_CONTRACT`。Planner archive：
`.agent-work/PLANS/20260730-0234-p7-retained-r3-option-b-b1a-c3e6f18-import-failure-review.md`，SHA-256
`732a279e908e26ad7b397b55d16e39527a0bedcffae1460245c82c8b79a31dd3`。

复用已提交 helper，仅创建一个全新empty fixed container及deterministic record/seal；不运行后继controller，不创建candidate root，
不读取retained R3，不调用canonical validator、不发出eligibility。允许的四条外置路径由PLAN exact冻结，执行前必须全部absent；
单进程/单调用，container `mkdir`一次，record/seal各exclusive create一次，任一失败最多写一次fixed fallback并停止。成功只证明
bootstrap prerequisite，不解锁release、R3 audit、consumer、network或device。Planner activation须先绑定更新后的FULL SHA与dispatch HEAD。

唯一Python进程在helper import时因`ModuleNotFoundError`停止；PLAN/FULL parse、Git/path gate、四路径create/fallback与ER append均为0，
四条路径仍absent，所有hard locks为0。本包不可重试。

### REF-P7-25-R2-B1A-C3E6F18-CORRECTIVE-1：Repo-local import and terminal evidence correction

**状态：** `ACCEPTED_BOOTSTRAP_PREREQUISITE_ONLY`。Planner archive：
`.agent-work/PLANS/20260730-0247-p7-retained-r3-option-b-b1a-c3e6f18-corrective-1-review.md`，SHA-256
`ff5e2039f672fe13334c934a57c259658bcf4225c7ce39703eb298d0a6b2e2e5`。

冻结repo `/Users/ibobby/Projects/WLED-RGBWW/src`一次插入`sys.path[0]`后按完整模块名import并验证`__file__`/blob/SHA；
禁止source loader、editable-install猜测、复制scanner或fallback parser。单进程在import前建立stdlib single-use ER writer与outer exception
boundary；writer ready后的PASS/FAIL均append一次，payload未启动或writer未建立则仅tool terminal取证，不虚报ER。其余F18路径、预算、
bootstrap语义与retained/release/device硬锁不变。

PASS evidence：container `/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b1a-c3e6f18-offline` empty mode0700；
record SHA-256 `56fb1c806db56ce7f68240c1a35b4443dc4c41806bd4bb3107e85a095a8ecf97`；seal SHA-256
`568a32cab44be41322f51be3e812a044e3976c7689a2ffd8b49fad2ab379cca4`；fallback absent；helper parse1/1、create1/1/1、
retry0、ER append1。该接受不验证或消费retained R3，也不调用validator或产生eligibility。

### REF-P7-25-R2-B1A-C3E6F19：Fixed-container exact-five controller preparation

**状态：** `REJECTED_DEDICATED_STATIC_TEST_FALSE_POSITIVE`。Planner archive：
`.agent-work/PLANS/20260730-0315-p7-retained-r3-option-b-b1a-c3e6f19-failure-review.md`，SHA-256
`b10e05fdf141c5864edf2eadcfa5022a7e92293bd573c51faf2c609bcad522de`。

Planner 下一包只可基于已接受的immutable F18 container/record/seal与已提交machine-contract helper，冻结一个single-process exact-five
candidate/controller执行合同及其输入、path、callback、test、Git和terminal evidence预算。准备阶段不得执行controller、创建candidate、
读取retained R3、调用canonical validator或产生eligibility；不得访问release、network或device。B2继续blocked，直到该后继真正完成并经
Planner验收。

Dispatch/bootstrap/absence与compileall均通过；targeted `11`项中`10 pass / 1 fail`。失败是 dedicated test 把lexically nested
local `ast.Name("run")`误判为`subprocess.run`；Planner独立确认controller无subprocess/os/pathlib import、无`.run()`属性调用、
无builtin open或direct filesystem I/O。focused/full/CodeGraph/diff-check均未启动，retry0；真实controller、R3、validator、release、
network与device均为0。controller source冻结SHA-256
`746fd13056c326489b48ca555b21618b65c8a78f198d035e18c02f68af689726`。

### REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-1：Dedicated static-test owner correction

**状态：** `REJECTED_BEFORE_PATH_OPERATIONS_WRONG_PLAN_MARKER_OWNER`。Planner archive：
`.agent-work/PLANS/20260730-0330-p7-retained-r3-option-b-b1a-c3e6f19-corrective-1-review.md`，SHA-256
`67eca7450faf11dfbf949279244357616b4fc964f93770ab602d33305d0e7026`。

只允许修改`tests/test_p7_retained_r3_exact_five_controller.py`，把`ast.Name` builtin/global callee与`ast.Attribute` method callee及
bytecode local/global/attribute owners分开；必须保留open、filesystem/subprocess attributes、forbidden imports、callback protocol与
eligibility边界断言。controller source byte-exact不变；fresh root运行一次compile/targeted/focused/full/CodeGraph/diff链，retry0。
不得读取candidate/R3/release或运行真实controller/validator/network/device。

Executer错误查找不存在的`PLAN_MACHINE_STATE`并在path operation前停止；正确owner是committed helper的
`parse_plan_machine_contract`/`parse_full_plan_machine_state`。fresh root absent，controller/test committed bytes与ER均未变，tests、
CodeGraph、controller、R3、release、network和device调用均为0。

### REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-2：Helper-owned activation gate

**状态：** `REJECTED_TEST_ONLY_FALSE_POSITIVE_STORE_FAST_LOCAL_BINDING`。Planner archive：
`.agent-work/PLANS/20260730-0348-p7-retained-r3-option-b-b1a-c3e6f19-corrective-2-review.md`，SHA-256
`d72cd628103396b51d05d3baeee1564da319582ed90aae0347984fd0e69a8072`。

所有PLAN/FULL machine-row解析必须直接调用committed helper APIs各一次；禁止execution source手写marker、splitlines/regex/substring
scanner、alias、fallback、inference或payload repair。其余C1 test-only scope、controller source preservation、fresh evidence与一次
fail-fast validation链全部不变；仍禁止candidate/R3/release、真实controller/validator、network和device。

Helper gate PLAN/FULL `1/1`、compileall pass；targeted仍`10/11`。唯一失败是测试只允许`LOAD_FAST run`，但nested local
`def run`的合法定义产生`STORE_FAST run`，随后同owner调用产生`LOAD_FAST run`。controller SHA未变，后续验证与所有真实/锁定操作为0。

### REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-3：Local-run bytecode owner correction

**状态：** `REJECTED_PRE_EDIT_FIELD_OWNER_KEYERROR`。Planner archive：
`.agent-work/PLANS/20260729-2203-p7-retained-r3-option-b-b1a-c3e6f19-corrective-3-review.md`，SHA-256
`95fbaf7c109d4a58214b0f8860f4f8b7ed367dbc20d8fdb15d2e67fcf2026b9c`。

只允许dedicated test将`execute_prepared_exact_five_controller` owner下的`STORE_FAST run`与`LOAD_FAST run`列为合法；
`LOAD_GLOBAL`、`LOAD_NAME`、`LOAD_ATTR`、`LOAD_METHOD` run仍拒绝，AST/global/attribute/direct-I/O/eligibility边界保持。controller source
byte-exact，fresh C3 root运行一次完整fail-fast链，retry0；candidate/R3/release、真实controller/validator、network/device仍锁定。

Helper calls `1/1`后Executer错误读取不存在的`FULL.value["candidate_contract"]`并停止。实际candidate digest与verified flag
分别是FULL顶层`candidate_machine_contract_sha256: str`与`candidate_contract_orchestrator_verified: bool`；test/source/root/tests均0，
ER append1，所有锁定操作0。

### REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-4：Exact field-owner gate correction

**状态：** `REJECTED_EXECUTION_SIDE_EXPECTED_DIGEST_TRANSCRIPTION_ERROR`。Planner archive：
`.agent-work/PLANS/20260729-2218-p7-retained-r3-option-b-b1a-c3e6f19-corrective-4-review.md`，SHA-256
`59e24e783eb59463ba048da5a11bb9d18473a5df6af1cc542331df63e82fa8b6`。

PLAN activation须逐字段冻结PLAN/FULL parsed mapping的exact owner/path/type/value；禁止未列candidate key、nested object、alias、
fallback、inference、`.get()`降级或cross-owner borrowing。实际FULL candidate fields只从上述两个顶层键读取。通过gate后仍只执行
C3 dedicated-test STORE_FAST/LOAD_FAST owner correction与fresh完整链；controller/R3/release/validator/network/device锁不变。

C4 field ledger `12/12`与helper `1/1`通过；Executer手抄`compileall.log` expected digest时把index22的`c`写成`d`。
C2五artifact未漂移，实际/PLAN expected空文件SHA为`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。
C4 root/test/tests均0，ER append1，所有锁定操作0。

### REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-5：Exact C2 evidence-identity binding

**状态：** `REJECTED_EXECUTION_SIDE_UNFROZEN_TERMINAL_SCHEMA_CARDINALITY_ASSUMPTION`。Planner archive：
`.agent-work/PLANS/20260729-2236-p7-retained-r3-option-b-b1a-c3e6f19-corrective-5-review.md`，SHA-256
`0137e2b36afce2a8120947fe140d9878ce0ccb9eb25c99784f543b6dbcf8c335`。

C2每个artifact expected bytes/SHA只能从parsed PLAN `immutable_c2_evidence.artifacts[name]`单次读取；执行源禁止shadow digest
literal、手抄字典、alias、fallback或repair。actual只来自lstat与single file bytes。通过后仍只改dedicated test的local
STORE_FAST/LOAD_FAST owner并运行fresh完整链；controller/R3/release/validator/network/device锁不变。

Helper/ledger/C2五项identity均通过；runner额外要求同构bytes/SHA二元组在manifest与validation中递归出现两次，但PLAN未冻结该
cardinality，实际两collection使用不同字段schema。C5 root/edit/tests均0，ER append1，所有锁定操作0。

### REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-6：Exact C2 terminal evidence-schema binding

**状态：** `REJECTED_EXECUTION_SIDE_UNAUTHORIZED_WHOLE_RECORD_KEY_SET_ASSERTION`。Planner archive：
`.agent-work/PLANS/20260729-2254-p7-retained-r3-option-b-b1a-c3e6f19-corrective-6-review.md`，SHA-256
`cb95512ac8e7d26df43552df913aaaf22ca66a776f065a36362397156fc1a6d6`。

Crosscheck exact冻结`artifact_manifest_before_terminal`长度3、按path唯一selector及bytes/sha/mode字段；`validation`长度2、按name
唯一selector及log/log_bytes/log_sha/log_mode/invocation/exit字段。禁止递归occurrence count、duplicate-shape inference、generic
search、字段同构化或二读terminal bytes。通过后仍只改dedicated test并fresh完整验证；其余硬锁不变。

C6通过activation/helper/ledger/identity/collection与selector gates，但runner额外要求validation record完整key set等于required fields，
错误拒绝合法`argv:list` extra。C6 root/edit/tests均0，ER append1，所有锁定操作0。

### REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-7：C2 terminal required-field subset binding

**状态：** `REJECTED_VALIDATION_LOG_EXCLUSIVE_CREATE_THEN_NOCLOBBER_REOPEN_CONFLICT`。Planner archive：
`.agent-work/PLANS/20260729-2310-p7-retained-r3-option-b-b1a-c3e6f19-corrective-7-review.md`，SHA-256
`6a7a2bc3467c5b63b634578b5a14252efffa4557f32d9ff65fbeb420dcf0a424`。

对listed fields仅做direct membership、exact builtin type与exact value；listed fields是required subset而非complete key set。extra key
不得导致拒绝，也不得枚举/读取/推断绑定；terminal whole-file bytes/SHA已固定完整payload。通过后仍只改dedicated test并fresh完整链；
controller/R3/release/validator/network/device锁不变。

C7所有pre-edit schema gates通过且test edit语义正确，实际test SHA
`19858a64fb760c112783b176822e7dabf72dce1b0cf9fb21e3a4738b83cebc3d`。日志exclusive-create后被zsh noclobber拒绝
路径重开，compileall实际调用0；terminal SHA`85f1895d48297d71d351f323e7024523cd68ccebfd88e84c8ed8acc2184e4369`。
旧ER误记after SHA，须append-only supersede，不改写旧terminal/ER。

### REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-8：Validation log single-owner corrective

**状态：** `REJECTED_FULL_SUITE_AMBIENT_GOVERNANCE_LINEAGE_DRIFT`。Planner archive：
`.agent-work/PLANS/20260729-2332-p7-retained-r3-option-b-b1a-c3e6f19-corrective-8-review.md`，SHA-256
`2a7891b73aa452ccde97a710a93f5b0ecbb2d669ab2056725bf819869c517b5b`。

每个log以exclusive open一次取得fd，child stdout/stderr直接绑定同一fd；禁止路径重开或shell redirection。child结束后
flush/fsync/close再digest。test/controller/helper不再编辑；fresh C8 root运行完整验证链，并在新terminal/ER显式supersede C7误记。
candidate/R3/release/validator/network/device锁不变。

C8 single-fd ledger `4/4`，compileall exit 0、targeted `11/11`、focused `43/43`；full suite运行684项后
`failures=1, errors=9`。十个失败只来自`AGENTS.md`与项目skill仍由历史freeze当作当前bytes验证；F19 controller/helper/test
均未漂移。C8 full log SHA-256 `289bb7275acfd7e3d4016cdff767999c53ef1b62565999a0e00bde5e087e9c2e`。

### REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-9：Governance lineage exact-successor corrective

**状态：** `REJECTED_FORMAL_COMPILEALL_CONSUMED_BEFORE_IMPLEMENTATION_COMMIT`。Planner archive：
`.agent-work/PLANS/20260729-2357-p7-retained-r3-option-b-b1a-c3e6f19-corrective-9-review.md`，SHA-256
`0463db1e302bb4a672845c8e98239aafc0a51928868dad734f69a2db11a47c3e`。

**Orchestrator engineering decision：** 保留既有AGENTS policy freeze、workflow-path manifest与e7ccdda public-default
successor manifest逐字节不变；新增唯一subordinate append-only governance successor owner。它只为历史治理提交
`3e2ebed132b6d4338bfa324bfc42c3565d2eeb3c`中的以下exact selected path set提供后继证明：

- `AGENTS.md`；
- `.agents/skills/camera-based-rgbww-optimizer/SKILL.md`。

该历史提交的parent必须为`9303aa22a9bd37e8ec4f23147c78c6bea84b9a2e`。因该提交实际包含181个changed paths，successor
不得声称它是two-path commit；必须同时绑定canonical `git diff --name-only parent commit` ledger count `181`与原始LF bytes
SHA-256 `9596c3fa8aee58259aff13b44badcc7d448e0555c80f166b20706dcd1e321118`，再绑定上述selected path set恰为2，禁止
generic allowlist或从commit其余179条路径推导新资格。

Exact selected provenance：

- `AGENTS.md`：before blob OID `440956792bf843c15b2f315e66e16826305d2154`，after blob OID
  `58bfacb5fc46fcb42bf643d12974063533a684eb`，before SHA-256
  `a035e6955ea113100031bf411f30abad3b84a9dd260fde848f1b1cfbd194c8a5`，after/current SHA-256
  `604b10bedeac6c9285f6448f94323521bf021a58275cce84d64163e16a2f07a0`，single-path canonical binary diff SHA-256
  `5736f6992d6882b1012a26ae5123892674d1f88cde0fee6ad98a5d33f78f5066`；
- `.agents/skills/camera-based-rgbww-optimizer/SKILL.md`：before blob OID
  `1f8bf2a7f568de77f0fa4290d18e300f0e48047e`，after blob OID `4d7dfe66c73036cb87e199c322f9344863f8c64e`，before
  SHA-256 `c8dd57a23ad684b4f7001f342ed3413a1abf4349bc6aeb90dbee7f5158139607`，after/current SHA-256
  `3a77c8a0f7b02b0c8b15d31b625273e88a0ee38fca5bb739dbdaaacb40dfe81e`，single-path canonical binary diff SHA-256
  `7127dfdfb608b7de284a181afcca704c36b107aa3859e2fecea059ae47af3049`；
- exact-two ordered canonical binary diff SHA-256
  `5a6cd050cd1d096e0894508aec338f7249679810bea63626acdcff63df9d17c8`；rollback为恢复parent中上述两个blob，且不得
  回滚或改写该提交的其余179条路径。

**最小实现scope：** exact repo paths仅
`config/hsi/p7-governance-lineage-successor-v1.json`、
`src/camera_based_rgbww_optimizer/optimization/p7_thermal_diagnostics.py`、
`tests/test_p7_thermal_diagnostics.py`。Manifest只绑定上述历史事实与validation-only governance scope；production代码新增一个
fail-closed subordinate validator，并由现有canonical lineage validator调用。现有canonical validator继续是唯一eligibility owner；
subordinate validator不得emit eligibility、不得分类其他路径、不得修复旧payload。

Planner下一包须冻结PLAN-only activation commit，再冻结唯一implementation commit的direct parent、exact三路径、subject与postcommit
验证；只允许上述三路径变更。验证链至少包括manifest strict schema/owner/hash、commit/parent/181-path ledger、two selected entries的
blob/SHA/diff/current bytes、negative drift cases、targeted lineage tests、focused F19 tests、fresh full suite、compileall、CodeGraph sync与
`git diff --check`。任一nonzero立即停，不得用focused green覆盖full failure。

所有candidate、retained R3、canonical retained validator、eligibility、release、network、`.env`、device、camera、Ray、strip、cleanup、
FORMAL-R6、public analyzer、TD-C、sentinel与P8保持0；retained R3仍为`RETAINED_UNVALIDATED_UNCONSUMED`。这是工程provenance问题，
不需要Advisor科学决策或Human高危设备授权。

C9 activation/history gate与fresh root建立成功，source/config草稿已形成，但Executer在implementation commit前误运行了与正式链重叠的
compileall argv，且缺少冻结的test路径、没有single-fd log。该调用消耗C9 compile预算；未重跑、未提交实现、test未修改。Terminal：
`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b1a-c3e6f19-corrective-9-offline/20260730T001500Z/terminal-evidence.json`，
SHA-256 `b5cb63fdbe9f51c22f582616eb7494b845ca55122575da415a96a501a4da5847`；该root不可复用。

### REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-10：Preserved-draft implementation and validation

**状态：** `REJECTED_TARGETED_AMBIENT_HEAD_AND_HISTORICAL_CHECKPOINT_SEAMS`。Planner archive：
`.agent-work/PLANS/20260730-0715-p7-retained-r3-option-b-b1a-c3e6f19-corrective-10-review.md`，SHA-256
`5e9eedd2adcfb284ee26991fc247c5a465d0b5587dafaa792d0e5e273a37826d`。

Orchestrator已按C9 review将未验证草稿独立保存为commit
`cc37da5664f50cdb5a2c7f3cc77b1f88728c4bf6`，parent
`bc13f50dfab9c2724d883befb2988f11548ccbe6`，subject
`chore(p7): preserve unvalidated governance successor draft`，exact changed paths只有：

- `config/hsi/p7-governance-lineage-successor-v1.json`：blob
  `46acad9b1992196cbcdb381718ea9b2dfda31e3b`，bytes `2574`，SHA-256
  `7ff96378e76c5b450c44db55d5b5eee922afe084bb0ea37d837a6f12db928795`；
- `src/camera_based_rgbww_optimizer/optimization/p7_thermal_diagnostics.py`：blob
  `6d274d59b60dcd38b26cb14d092bb7cd31d30d2e`，bytes `191641`，SHA-256
  `7030305c1a4b5e829fc8966880e80139a9e2a345453e7cf2766651c0039525f1`。

该commit的validation claim为false；test保持blob `16e91ee1e1fac64062c511b96f2f320b7ee6c806`、SHA-256
`7ccc64a1f3182a0860b01dcc159f5b2ef505193fae9d2add41cbc161b49e5c7a`，未纳入draft commit。新Planner须审查草稿语义，冻结
source/config是否需要修正，并至少补齐C9的positive case与完整negative matrix。新的implementation commit必须精确列出所有变更路径；
commit通过topology/bytes检查后，才可在brand-new `0700` root各运行一次compileall、targeted、focused、full、CodeGraph与diff-check。
C9 root与compile结果不得复用；full suite必须exit 0。

旧policy/workflow/public-default payload保持逐字节不变，canonical candidate builder仍是唯一eligibility owner。Candidate、retained R3、
canonical retained validator、eligibility、release、network、`.env`、device、camera、Ray、strip、cleanup、FORMAL-R6、public analyzer、
TD-C、sentinel与P8继续全部锁0；retained R3仍为`RETAINED_UNVALIDATED_UNCONSUMED`。

C10创建唯一implementation commit `0682cd8763516dfb19a8e1ad48c53cb9934b9d19`，parent `4316d0c...`，subject
`fix(p7): validate exact governance lineage successor`，exact config/source/test三路径。Config SHA-256
`69bbbb369e776e1aa11a227ecf3432de44bc517c7eb25828094f4820df45042e`；两个新governance tests均pass，compileall pass。
Targeted为`9/12`：一个failure来自ambient HEAD changed-path count硬编码59而实际265；两个errors来自历史qualification checkpoint
错误读取当前working skill bytes。Focused/full/CodeGraph/diff因fail-fast为0。Terminal SHA-256
`644439af182a007e88e6978aaecc8c6ec2e820add732c56b9e74716bce6bcbd5`。该commit仅作为
`retained_unaccepted_governance_successor_implementation_base_v1`，不可消费、不得产生eligibility。

### REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-11：Historical-checkpoint and ambient-HEAD seam correction

**状态：** `REJECTED_TARGETED_AMBIENT_FULL_SET_EXPECTATION_ONLY`。Planner archive：
`.agent-work/PLANS/20260730-0734-p7-retained-r3-option-b-b1a-c3e6f19-corrective-11-review.md`，SHA-256
`7082943b652a9687a28928285a12e3a138e64cb4f7da672abc13a8cc6894aa98`。

只允许修改source/test两路径；上述config必须byte-exact不变。Source须把historical requested checkpoint与ambient current HEAD owner分离：
历史checkpoint只验证checkpoint bytes，不读取working path；只有requested checkpoint解析为当前HEAD且HEAD包含3e2ebed时，旧public-default
payload先完成验证，再调用governance subordinate一次验证working/current bytes。不得fallback、跳过旧payload或新增eligibility owner。

Test须移除ambient HEAD changed-path总数的瞬时常量，改为sorted/unique、输入输出path一一对应、canonical classification、exact post-EQ
mapping与prohibited空集；新增historical qualification regression，证明working skill read漂移/禁止时仍以checkpoint bytes通过且subordinate不调用。
Current HEAD分支仍须证明subordinate恰调用一次与working drift fail closed。

下一Planner activation须从Orchestrator reviewed-state clean commit冻结PLAN-only parent；后继implementation subject exact为
`fix(p7): separate historical lineage checkpoint ownership`，changed paths exact source/test，additional0。Brand-new C11 root依次一次
compileall、原十二selector加historical regression、focused、full、CodeGraph、diff，fail-fast、retry/fallback0。所有R3/release/device/
scientific锁继续为0；无需Advisor或Human授权。

C11 source/test commit `ba816216af9d37397873e054f44dbb7eea0f9b10`完成historical/current seam修复；compileall pass，targeted
`12/13`，新增historical checkpoint、current HEAD subordinate/working-drift与两个governance tests均pass。唯一失败是PLAN错误要求
full ambient changed set eligible/prohibited空；canonical builder正确返回`ineligible_requires_new_setup`。Terminal SHA-256
`43fbf748d847b434f4661933c113b21a84f1f20d10d8415c28e096149686953a`。Production source SHA-256
`0a688f31728f8c7d072419b8a75a7d9b4b04315e906cde6daa17a80556f56b64`保留为pending test-only validation，不可消费。
旧ER手工bytes `1073/1895/5427`错误；terminal/artifact权威值为`1227/1842/5512`，对应SHA正确，下一ER只可append supersede。

### REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-12：Canonical classification expectation correction

**状态：** `REJECTED_POSTCOMMIT_EXPECTED_CHILD_SHA_TRANSCRIPTION_ONLY`。Planner archive：
`.agent-work/PLANS/20260730-0749-p7-retained-r3-option-b-b1a-c3e6f19-corrective-12-review.md`，bytes `6082`，SHA-256
`488e6953cd153109a14f3102a57bd2e40dc6d4f3ae2bcf05b545054d4f37ee20`。

只允许修改`tests/test_p7_thermal_diagnostics.py`中相关局部测试；production source、config与其它路径byte-exact。测试必须分别证明：

- canonical accepted subset返回`eligible_waiting_for_planner`且`prohibited_paths=[]`；
- full ambient changed set的returned paths与输入一一对应、sorted、unique，每项classification与canonical owner一致；
- accepted与prohibited分类均真实保留；prohibited非空时status为`ineligible_requires_new_setup`，prohibited paths与canonical truth一致；
- 不硬编码59、265或任一ambient path总数。

下一Planner须从Orchestrator reviewed-state clean commit冻结PLAN-only parent；后继唯一test commit subject
`test(p7): align canonical lineage classification expectations`，changed path exact test one-path。Brand-new C12 root运行exact 13 targeted、
focused、full、CodeGraph、diff one-shot链；terminal需append-only supersede C11 ER bytes误记。Retry/fallback与所有R3/release/device/
scientific调用为0；无需Advisor或Human授权。

C12 test-only commit `a9a817137969d9d2692fdd0b244d08e26e8a025d`的parent、subject、exact one path、blob、test SHA
`4eb823d5dfe22b95a172f4920b077285b50ad174b4a4c9cdda9fd7751dc164a5`与patch SHA均精确。唯一失败是controller
手抄expected child为错误的`a9a8171b80...`；postcommit controller exit1，所有正式validation调用0。Terminal SHA
`b412d9d5ca7d9a044945b3cfc71a8deb96f1e6bf99733f18323240a82c560c84`。ER误记precommit SHA `4f557d...`；
artifact权威SHA为`5821ab5d2b4d25cf218933c208b128854149150473c604a24131262ec0b6361a`，只能append supersede。

### REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-13：Programmatic HEAD validation-only recovery

**状态：** `REJECTED_SOURCE_TOPOLOGY_CONTRACT_MISMATCH`。Planner archive：
`.agent-work/PLANS/20260730-0804-p7-retained-r3-option-b-b1a-c3e6f19-corrective-13-review.md`，bytes `4434`，SHA-256
`c2018931bdb35e6424829177b0111a831bfbeab46f44ba7c69e5f7259f87f924`。

保留test commit `a9a8171...`与production `ba81621...`为pending validation；本包repo edits、stage、implementation commits均为0。
Executer controller必须从Git直接读取一次full lowercase dispatch HEAD并冻结，所有topology比较只消费该值；禁止人手抄expected child或
再次拼接。Brand-new C13 root执行activation/retained identities gate后，one-shot compileall、exact 13 targeted、focused、full、CodeGraph、
baseline/working diff-check；single-fd、fail-fast、retry/fallback0。Terminal/ER append-only supersede C12 precommit SHA误记。
所有candidate/R3/release/device/scientific锁为0；成功也只表示pending implementation完成验证，不授权eligibility或消费。

C13 programmatic dispatch HEAD single-read gate、activation/archive/FULL与retained三路径identities、C12 supersession全部通过。唯一失败是
controller错误要求`ba816216...`为exact one-path commit；实际changed paths精确为source与test两项，parent/subject均正确。
Validation items 0，terminal SHA-256 `94190eee0df9f0d49ea60b100fa4b0c77d24e2050fe3ad3f0b70e70604e3c02e`。

### REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-14：Retained source topology validation recovery

**状态：** `REJECTED_FULL_SUITE_EQ_R6_MANIFEST_METADATA_DRIFT`。Planner archive：
`.agent-work/PLANS/20260730-0825-p7-retained-r3-option-b-b1a-c3e6f19-corrective-14-review.md`，bytes `5792`，SHA-256
`febe5afa8dd3d4597ecafcc1778c73181a14ba3b91877813afbb5909a7a13685`。

Repo edits/stage/implementation commit继续为0。Controller必须programmatic single-read dispatch HEAD，并核验`ba816216...`的exact parent、subject、
whole-commit two-path set：source与`tests/test_p7_thermal_diagnostics.py`，additional0；随后分别核验retained source/test path identity。
禁止再推导source-only commit。Brand-new C14 root运行与C13相同的exact 13 targeted、focused、full、CodeGraph、diff one-shot链；
C12 supersession只引用C13已完成append，不重复。所有R3/release/device/scientific锁0；无需Advisor/Human。

C14实际compileall、targeted `13/13`、focused `125/125`通过，full运行`687`项后有`2`项失败；CodeGraph/diff按fail-fast未运行。
Authoritative terminal SHA-256 `0439ff6136737d41b168409a113f7df12e0794638eed39777cdfdf6f8b27e8fe`。两项失败同源：
accepted EQ-R6 root顶层新增6148-byte regular `.DS_Store`，令整树manifest从`47/42/5/0/0/7980`变成
`48/43/5/0/0/8119`，并提前遮蔽artifact-drift负例；四个canonical artifact未见改写。不得删除或改写旧root来取得green。

### REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-15：EQ-R6 non-evidence macOS metadata boundary

**状态：** `REJECTED_PREVALIDATION_EVIDENCE_ORDER`。Planner archive：
`.agent-work/PLANS/20260730-0837-p7-retained-r3-option-b-b1a-c3e6f19-corrective-15-review.md`，bytes `5301`，SHA-256
`f1a5f7300248aa74176c363f0d128bfb2214890572a16019b3d4e2ca5464afd3`。

仅允许在既有`build_planner_eq_family_manifest`owner与`tests/test_p7_td_b_r6_contract.py`dedicated tests内纠偏：先按现有
`lstat`安全分类，只将root-relative exact `.DS_Store`的regular file排除于rows/counters/payload；root symlink/directory/unsupported
type、嵌套`subdir/.DS_Store`、`._*`及任何其他未知路径继续fail closed或进入manifest造成drift。禁止generic basename/glob allowlist，
禁止读取或绑定该metadata payload，禁止修改accepted root、frozen 47-entry SHA、四个artifact hashes、qualification checkpoint或canonical
eligibility owner。C15实现commit `3a14fe0bd663250dd48c65e71f1a6550df89267f` 的exact source+test topology通过，但修改/commit先于
brand-new root和before identities创建，故未运行任何validation；terminal SHA-256
`507747e10989e4acd57274a013d512c21015a7bd05607deba17a3a61716a406e`，retry/fallback与所有locks均为0。不得将事后重建
identity冒充预冻结证据。Meaningful tests必须证明root regular metadata不影响manifest、unsafe/nested同名不被隐藏、真实accepted root恢复原digest且
artifact-drift负例重新到达准确错误。Brand-new C15 root按exact one implementation commit执行compileall、6 targeted、focused、full、
CodeGraph与diff one-shot链，retry/fallback0。所有retained-R3、release、network/device/scientific route保持锁定；成功也只回Planner验收门。

### REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-16：retained metadata-boundary validation-only successor

**状态：** `REJECTED_FOCUSED_POST_EQ_VALIDATION_SUCCESSOR_MISSING`。Planner archive：
`.agent-work/PLANS/20260730-0852-p7-retained-r3-option-b-b1a-c3e6f19-corrective-16-review.md`，bytes `5055`，SHA-256
`394223de840fcdeeaeda645cac9835c453d71ac758839122b7b6df5c16a16cc2`。

保留`3a14fe0bd663250dd48c65e71f1a6550df89267f`，不重做实现、不新增source/test/config commit。新C16 root必须先从
activation parent `431d9d8dd58a6c0df7fb0b225ce206d2e8c57f53`与实现commit的精确Git objects派生before/after identities，再验证
exact parent、subject与two-path topology，之后才可运行C15规定的6 targeted、focused、full、CodeGraph与diff one-shot链。
Prevalidation freeze、compileall与targeted `6/6`通过；focused运行`193`项后`1 failure + 2 errors`，full/CodeGraph/diff按
fail-fast保持0。Terminal SHA-256 `53372a9d08ed8f30c5f2f471c15cabf0f7fe9c432ce070a1d23a2ec30db7566a`。
三项失败同源：历史post-EQ owner要求classified R6 contract test的current checkpoint/working blob仍等于`161094f`历史blob，
但合法retained `3a14fe0`已精确更新该test。不得弱化历史blob校验或接受任意current blob。

### REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-17：post-EQ validation exact subordinate successor

**状态：** `ACCEPTED_COMPLETE_POST_EQ_VALIDATION_SUCCESSOR`。Planner archive：
`.agent-work/PLANS/20260730-0917-p7-retained-r3-option-b-b1a-c3e6f19-corrective-17-review.md`，bytes `7394`，SHA-256
`85c8dc47284d8fa347a93e7de29e508ae576a40ff6f03d1443e6ca4418ee7124`。

仅在既有post-EQ lineage owner与`tests/test_p7_thermal_diagnostics.py`内新增exact subordinate successor binding：冻结`3a14fe0`
commit/parent/subject、exact source+R6-test two paths、path-ledger、canonical/per-path patch与before/after blob identities；历史`161094f`
三路径及commit-qualified blobs继续完整验证。Successor source仅作provenance，不获classification；唯一延续的是exact
`tests/test_p7_td_b_r6_contract.py -> accepted_post_eq_exposure_policy_validation`。禁止generic allowlist、任意descendant/current blob、
近邻路径或第二candidate owner。Brand-new C17 root必须先pre-edit freeze，再exact one source+dedicated-test commit，运行5 targeted、focused、
full、CodeGraph与diff one-shot链。实现commit `7c31c1be26274955686e9214a14bb29d1adc77b5` exact source+dedicated-test，
terminal SHA-256 `e46158d6b0dae3ca600113f5a18bba57fbb58356e07769d4c06d9f9cca359d9a`；targeted `5/5`、focused
`195/195`、full `691/691`、CodeGraph与两项diff全部一次通过，retry/fallback0，全部locks0。历史owner未弱化，successor只延续
exact R6 validation path classification，canonical candidate/eligibility owner不变。该通过关闭B1A依赖但不读取/验证/消费retained R3。

### REF-P7-25-R2-B2：modern accepted-integration immutable manifest seal

**状态：** `ACTIVE_CORRECTED_PATH_WAITING_PLAN_ONLY_ACTIVATION_FREEZE`。首次失败的Planner archive：
`.agent-work/PLANS/20260730-1547-p7-retained-r3-option-b-b2-modern-manifest-failure-review.md`，bytes `5916`，SHA-256
`1c0cf905e468bad0a3349fe884775aa70ffb5201af74cddce8c4a770007e3c50`。

B1A及C17已accepted，现代manifest-only基线继续有效；首次B2 controller在错误冻结的首个artifact path `lstat`处ENOENT并
fail closed：R3 lstat/open/read=`1/0/0`、bytes0、manifest/seal0、retry/fallback0，terminal SHA-256
`10aef59d4b2155bf6080a5bde5fcf3925871b592a8f6ddc402358351c5ab87b7`。实体terminal存在但内嵌pre-write
`terminal_writes=0`，该caveat原样保留。不得重试旧root或寻找替代路径。C1现已独立验收exact path-owner index；corrected B2
只能由新的PLAN-only activation提交冻结parent/PLAN hash后执行，当前`active_task_count=0`。

**现代B2目标：** 不再创建、amend、cherry-pick或重做repository implementation commit。B2只在brand-new external root中
exclusive-create并seal一个`retained-r3-audit-provenance-manifest-v2.json`，schema
`p7_retained_r3_audit_provenance_manifest_v2`，status exact `sealed_subordinate_provenance_evidence`。它是canonical validator的
从属证据输入，不判断或emit eligibility，不创建/复制/修复release，不运行canonical retained validator；B2通过只解锁B3独立验证。

**必须绑定的accepted integration baseline：**

- historical helper v1：commit `9303aa22a9bd37e8ec4f23147c78c6bea84b9a2e`、parent/release checkpoint
  `32b9e670ff3bbea0cd1505528c2ca87c2935446c`，disposition exact
  `retained_release_audit_prerequisite_v1_superseded_before_real_validation`，不可消费；
- integration commit `3e2ebed132b6d4338bfa324bfc42c3565d2eeb3c`、parent `9303aa22...`、full 181-path LF ledger
  SHA-256 `9596c3fa8aee58259aff13b44badcc7d448e0555c80f166b20706dcd1e321118`，其中只有helper与dedicated test作为B2
  scientific-audit prerequisite selected paths；其他179 paths必须显式标记`present_in_commit_not_authorized_by_this_manifest`；
- selected helper/test after SHA-256分别为
  `48c0c57fb95c08205c3fef7b23e6df3729928352cd23e1722e8693b9f3634cf8`与
  `c8d6c7c99815d823871ecfddce79eadd5d5def918affbcd7e4ce86de691d1b3f`，并绑定其commit-qualified before/after blob OID、
  bytes、SHA-256及per-path/selected binary patch digests；
- canonical seam integration chain必须按full SHA、direct parent、subject、exact changed paths、before/after Git object与binary patch绑定：
  `0682cd8763516dfb19a8e1ad48c53cb9934b9d19`、`ba816216af9d37397873e054f44dbb7eea0f9b10`、
  `a9a817137969d9d2692fdd0b244d08e26e8a025d`、`3a14fe0bd663250dd48c65e71f1a6550df89267f`、
  `7c31c1be26274955686e9214a14bb29d1adc77b5`；任何遗漏、额外semantic path或identity不一致fail closed；
- canonical governance manifest `config/hsi/p7-governance-lineage-successor-v1.json` SHA-256
  `69bbbb369e776e1aa11a227ecf3432de44bc517c7eb25828094f4820df45042e`，以及历史post-EQ owner和exact validation successor
  的accepted constants/identities；
- GUIDE SHA、Advisor decision evidence SHA `842cfad090549ebf6379df4551bd4f051267e4bf93014f899c5e329c57085620`、
  attachment SHA `91a88e5467e13c811794c2149b6a8d5669e613c3e259d8f4091ba08c048733d6`与Human engineering-governance override；
- C1 sealed path-owner index exact
  `/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b2-c1-path-owner-27aacbf-20260730T1547Z/path-owner-index.json`
  SHA-256 `b189117fdd0a9a65ca80660245ec84b7f2f533c3e496c96e76eb48a4666feb35`，机械解析出的retained R3 source
  root exact `/Volumes/4T/temp/rgbww-optimizer/p7-td-b-lineage-release-r3/lineage-release-32b9e67-r2-20260727T2227/child-output/lineage-release-r3`
  及原三artifact paths/hashes。B2对四个C1 evidence各一次lstat/open/read/hash，对三件套各一次lstat/open/read/hash并做
  before/after identity；读取不等于audit、validation或consumption。

**Persistence与验证边界：** Planner须冻结一个single-process/single-root controller、exact input/read budgets、strict duplicate-key和
non-finite拒绝、canonical compact sorted UTF-8 JSON+LF、`O_EXCL|O_NOFOLLOW`、0600、file+directory fsync、strict reload、独立hash
seal及terminal。Manifest一旦seal不得rewrite/repair/replace/relocate。B2只做schema/self-consistency、Git-object重算、原三artifact hash与
immutability重算；不运行full suite或synthetic audit（留给B3），不修改repo，不生成eligibility。Retry/fallback0；network、`.env`、device、
camera、Ray、strip、cleanup、FORMAL、public analyzer、TD-C、sentinel、P8均0。

### REF-P7-25-R2-B2-C1：retained R3 exact path-owner index

**状态：** `ACCEPTED_COMPLETE`。Planner archive：
`.agent-work/PLANS/20260730-1000-p7-retained-r3-option-b-b2-c1-path-owner-index-review.md`，bytes `7795`，SHA-256
`d9fdec1891c9e251df2fa264eda615abbabe5d6b0a9bde2be67b650652917f34`。

只验证历史archives无歧义绑定的exact chain：
`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-lineage-release-r3/lineage-release-32b9e67-r2-20260727T2227/child-output/lineage-release-r3`。
三层directory各只允许一次non-following lstat与一次direct-entry scandir；只记录name/type/stat并机械构造三个artifact absolute paths。
Artifact separate lstat与content open/read/hash/parse/mmap/copy全部0；禁止parent/sibling search、递归、alternate root、B2 manifest seal、validator、
audit、eligibility、release或设备。执行结果为directory lstat/scandir `3/3`、artifact content access全零、resolved paths `3`；
path-owner index/index-seal/terminal/terminal-seal SHA-256依次为
`b189117fdd0a9a65ca80660245ec84b7f2f533c3e496c96e76eb48a4666feb35`、
`867d1ffad5bd29f24dc81b24a58ce66393dd688833d3a4516fe7f45ef50875e9`、
`c21a691272ca7466271349daa5b10236c9f36dfeb481d592e9c368a87e7a4763`、
`4bfebf4ad40e8c2e65ad2470faaed184f21d39eda73c13e689b09769d280752f`。该接受只确认path ownership，不验证artifact bytes。

> 以下旧two-path执行细节已由Human engineering-governance override与B1A exact-five contract supersede，不得作为未来
> PLAN输入；B1A-C2/后续Planner验收冻结的five-path child与manifest facts才是B2的新工程基线。本段保留仅作旧合同历史。

**执行合同：** 在B1批准的clean-room exact parent上，将冻结的两文件bytes materialize且不再编辑；验证diff path set
恰为2、additional path=0、target hashes匹配。Commit前冻结：

- parent full SHA与actual direct-parent事实；
- exact sorted two-path set；
- two before/after Git blob OIDs；
- Planner冻结算法产生的canonical binary-safe patch SHA-256；
- target file SHA-256；
- exact subject。

仅允许一次commit。Commit后必须验证child full 40-char SHA、parent=
`9303aa22a9bd37e8ec4f23147c78c6bea84b9a2e`、exact tree、exact subject、
changed paths、before/after blobs、committed file hashes及committed patch hash完全等于precommit freeze。任一不一致
立即进入BR；amend/rebase/第二commit/内容修复为0。

随后在fresh external root以exclusive create、0600、file fsync、directory fsync、strict duplicate-key/non-finite拒绝、
reload与独立hash seal恰好一个`retained-r3-audit-provenance-manifest.json`，schema
`p7_retained_r3_audit_provenance_manifest_v1`。Manifest至少绑定：

- GUIDE SHA `659152f6c0ae69c90c701de4e57c352d771e4f0bf75cf9410271ba0a94200e35`、
  decision evidence SHA `842cfad090549ebf6379df4551bd4f051267e4bf93014f899c5e329c57085620`与
  Advisor attachment SHA `91a88e5467e13c811794c2149b6a8d5669e613c3e259d8f4091ba08c048733d6`；
- setup checkpoint `9c804abdeabbc5da18a66d0acf25a1f13128bc2d`、release checkpoint
  `32b9e670ff3bbea0cd1505528c2ca87c2935446c`；
- helper v1 full SHA、actual parent与superseded/unconsumable classification；
- repair child/parent/tree/subject、exact paths、before/after blob OIDs、patch SHA、after file SHA；
- 原retained R3三artifact SHA：
  - `current-lineage-candidate.json` =
    `3a2ff5a2af200c55c925b954488c5c5dd31a35a481440d17dfcdd8b68419f2e0`；
  - `resolved-formal-plan.json` =
    `cf7c78b6a6cfda4055d05f5e9bbe9914161213b380dc7736ee09e257dd45eb6b`；
  - `setup-lineage-release.json` =
    `0bacf1878a97fcdc4436259e132e89f6e56611df6d7fb5d5a7da28f62c98ad3e`；
- helper exact category=`retained_release_validation_prerequisite_code`，scope=
  `retained_R3_schema_validation_and_terminal_count_audit`；
- test exact category=`retained_release_validation_prerequisite_test`，scope=
  `exact_helper_schema_owner_terminal_and_replay_regression`；它不得归入cleanup provenance；
- `production_runtime=false`、generation/copy/consumption/device/formal authority均为false/none；
- validation-only scope与逻辑rollback `32b9e67`。

Manifest status只能表示`sealed_subordinate_provenance_evidence`，不能包含或暗示eligible/consumable/authorized。
它一旦seal不得repair、rewrite、replace或relocate为新payload；B2通过只解锁B3。

### REF-P7-25-R2-B3：postcommit tests 与 synthetic lifecycle

**状态：** `BLOCKED` on B2 accepted。

严格顺序为：manifest独立自校验 → postcommit focused → durable full suite → fresh synthetic
owner/terminal/replay。Canonical manifest verifier必须从Git重新计算commit/parent/tree/path/blob/patch/file fields，并从
原artifact identities重新计算三SHA，不得仅信JSON；此阶段仍不得输出eligibility。

Focused、full与synthetic各一次，retry 0。Full suite若预计不超过既有约3分钟可由普通执行owner运行；若未来
Planner证据表明预计超过10分钟，才适用visible macOS Terminal、三次稀疏liveness与automation规则。任何失败进入
BR，repair commit与manifest作为rejected evidence保留，不得amend、重写manifest或生成第二repair。

### REF-P7-25-R2-B4：原retained R3真实audit与唯一eligibility判定

**状态：** `BLOCKED` on B3 accepted。

只对原exact retained R3 root的原三件套执行首次fresh真实audit；禁止copy、repair、rewrite、regenerate或用新payload
替代。Helper audit、public candidate/release/resolved callback、terminal-count/owner/replay各按未来PLAN冻结的exact
one-shot cap执行，source before/after identity必须完全不变。

Canonical lineage validator必须独立重算manifest关键事实并验证所有B2/B3/B4 gates；只有它可以在
`prohibited_or_unreviewed=[]`且全部通过后输出：

```text
retained_R3_status = RETAINED_VALIDATED_UNCONSUMED
candidate_eligible = true
```

Manifest、helper、consumer、replay或Planner都不能输出eligibility。即使pass，release consumption、设备、
FORMAL-R6、strip、TD-C、sentinel、P8与public scientific analyzer仍为0/locked，且必须停Planner验收。

### REF-P7-25-R2-B5：Option B 独立验收与路线状态转换

**状态：** `BLOCKED` on B4 pass。

Planner须独立重放manifest、Git、tests、synthetic、real audit、canonical validator与zero counters；确认repair child
没有第二commit/第三path，v1仍superseded/unconsumable，R3只是validated-unconsumed。Planner归档后由Orchestrator
更新FULL，才可将`REF-P7-25`接受并让`REF-P7-26`进入future planning；不得直接进入predevice或设备阶段。

### REF-P7-25-R2-BR：统一失败与逻辑rollback

**状态：** `SUPERSEDED_BY_HUMAN_GOVERNANCE_OVERRIDE`。B1 accepted negative feasibility曾触发本stop；Human
2026-07-29已明确将文件、代码、provenance、execution与Git决策交给Orchestrator，因此该非科学Advisor stop关闭。

该精确矛盾现在由`REF-P7-25-R2-B1A`解决：Orchestrator要求Planner基于实际调用链冻结minimal exact path set，保留
canonical validator唯一owner和禁止generic allowlist等实质边界，但不再保留Advisor的旧two-path/parent工程限制。

任一B1-B5 exact check、test、manifest、synthetic、real audit或validator失败：repair commit（若已产生）作为rejected
evidence保留；manifest（若已seal）immutable保留；不amend/rebase/delete；retained R3保持原bytes与
`RETAINED_UNVALIDATED_UNCONSUMED`；active release checkpoint逻辑回退
`32b9e670ff3bbea0cd1505528c2ca87c2935446c`；v1为superseded/unconsumable，
v2为rejected。禁止第二repair、修改manifest适配结果、重生成R3、generic allowlist、计数oracle放宽、设备或formal；
必须重新回Advisor。

**证据与验收：** exact source/checkpoint/policy/EQ provenance；changed-path policy；production qualification一次；
public/final/strict validators全通过；fake consumer与single shared owner；three-artifact terminal seal；secret/path scan；
old R2 release pre/post不变。

**失败与 stop：** 任一 release/validator失败即停 Planner，不生成第二个 release；任何 code/config改变使该 release
失效并需要新的计划决定。

### REF-P7-26：Fresh predevice oracle

**状态：** `BLOCKED`

**依赖：** `REF-P7-25` accepted。

**目标：** 在任何设备/root creation 前验证 current checkpoint、R3 release、policy、experiment、exact roots、
budgets、cleanup、single-flow、public default和无 stale process。

**证据：** positive/negative replay、zero adapter-call proof、strict JSON、terminal seal、source/release hashes。

**失败与 stop：** pre-child fail closed；只回 Planner，不访问设备、不自动进入 readiness。

### REF-P7-27：Fresh real zero/readiness gate

**状态：** `BLOCKED`

**依赖：** `REF-P7-26` pass。

**目标：** 有界验证 strip generation-bearing zero、Ray intensity0、camera/bridge所需 readiness、Python/shell cleanup、
independent final zero和residual process0。

**安全：** 只允许 zero/off/read-only readiness；不 capture、不生成 CR3、不施加非零 formal state。

**失败与 stop：** 任一 source零状态或 cleanup未知即停；不得自动 E2。

### REF-P7-28：Fresh E2

**状态：** `BLOCKED`

**依赖：** `REF-P7-27` pass。

**目标：** 对 R3 release和current checkpoint做 fresh E2，验证设备、camera、Ray、exposure-policy consumer、
cleanup和final-zero的正式前置路径；不做 formal capture。

**证据：** exact release consumption/validation accounting、preflight/self-check、remote/device/Ray attempts、
cleanup/final-zero、terminal seal、no stale/new formal roots。

**失败与 stop：** 任一 E2 failure保留 progressive/terminal evidence并停；无自动 retry。通过只进入 Human `REF-P7-29`。

## 8. Full Ray R6

### REF-P7-29：Human one-launch checkpoint

**状态：** `HUMAN_CHECKPOINT`

**依赖：** `REF-P7-28` accepted。

**请求必须冻结：**

- exact R6 experiment/root、checkpoint/release/policy hashes；
- full 16 IDs/order、formal physical16、ambient0、setup0、retry0；
- Ray-only、strip zero、expected run duration；
- visible Terminal exact single launch、PID/ledger、three liveness checks和automation；
- abort、Python/shell cleanup、final-zero、terminal seal；
- failure后strip/analyzer/retry0；
- 只授权一次 Ray R6，不授权 strip/TD-C。

**stop：** Human 未明确确认前不创建 activation/package root或launch ledger。

### REF-P7-30：完整新 Ray R6 16-frame acquisition

**状态：** `LOCKED`

**依赖：** `REF-P7-29` + exact active PLAN。

**执行合同：**

- experiment/root/IDs/order/shutters exact使用 `REF-P7-20/24`；
- formal16、physical cap16、ambient0、setup0、launch1、retry0；
- A/D/B frozen R5 values，C exact EQ selected；
- no auto exposure、no weak reacquire、no shutter change、no skipped slot、no mid-run resume；
- strip全程generation-bearing zero；
- 每 returned CR3在post-processing前写physical ledger，sidecar/remote IDs/hash全部保留；
- 每 capture accepted前通过 complete quality gate；
- Python/shell cleanup、independent final-zero、terminal audit无条件执行。
- formal root内不生成product LUT、不运行strip solver、不修改exposure policy。

**terminal artifact：** plan/run/captures/commands/physical-returns/measurements/policy reference/returned-summary/
all-off-python/all-off-shell/terminal-audit/failure-if-any。

**失败：** 任一 capture、quality、exposure、timing、source、ledger、cleanup或terminal failure：

```text
classification = accepted_hard_failed_formal_attempt
formal_pass = false
strip = 0
public analyzer = 0 unless acquisition 16/16
retry = 0
```

**stop：** 无论 pass/fail都先回 Planner。只有 16/16 quality/engineering pass 才可进入 `REF-P7-31`。

### REF-P7-31：Ray-only R6 TD-B analyzer gate

**状态：** `BLOCKED`

**依赖：** `REF-P7-30` 16/16 accepted。

**分析：**

- public Ray-only TD-B analyzer重放所有 physical/accepted/CR3/sidecar/exposure/state/timing/budget/cleanup evidence；
- A0/A_after_D/A_after_B/A_after_C frozen same-state joint coverage；
- D/B/C 60/120/300/600 trend、dominance、direction完整输出；
- `steady_status=not_demonstrated` 永久保留；
- `operational_endpoint_600_valid`与trend分离；
- 不读取 R5 frame作为R6样本，不生成 strip/product LUT。

**出口：**

- acquisition/quality invalid：stop，strip blocked；
- 16/16且history fail：
  `status=history_dependent_at_operational_600`，进入 `REF-P7-38`；
- 16/16且history pass：
  `ray_td_b_operational_branch=accepted_for_strip_entry`，只解锁 Human `REF-P7-32`。

**stop：** analyzer结果先回 Planner；不得在同一 package启动 strip。

### REF-P7-38：Ray history-model required

**状态：** `ADVISOR_DECISION`

**触发：** R6 16/16 quality pass但A return anchors不兼容。

**请求：** 提交完整 Ray chronology/history/previous-state/exposure/quality evidence，请 Advisor选择新的 history model、
restricted operational scope或stop。禁止用 covariance inflation、删 anchor或将trend warning改为pass。

## 9. Conditional strip 与 combined TD-B

### REF-P7-32：新 strip TD-B 独立 planning gate

**状态：** `BLOCKED`

**依赖：** `REF-P7-31` history pass。

**Planner 任务：** 在 Ray analyzer review 完成后另写一个只覆盖新 strip TD-B 的 active PLAN；冻结新
experiment/root、16 formal、retry0、exact A/D/B/C sequence、600-second anchors、existing frozen
commands/exposure/setup、Ray zero、双 cleanup和stop-before-combined。不得把 Ray R6 的 Human launch或PLAN范围
延伸到 strip/TD-C，也不得在Ray analyzer package内连续启动strip。

**授权边界：** 根据 Human 已冻结的项目规则，active PLAN 内普通有界灯光操作本身不需要新的危险操作授权；
但4.GUIDE要求stage分离，所以没有新的strip PLAN就不得执行。firmware/deployment/destructive operation仍需Human。

**stop：** Planner完成独立PLAN后才可委派Executer；本task本身不运行设备。

### REF-P7-33：新 strip TD-B 16-frame acquisition

**状态：** `LOCKED`

**依赖：** `REF-P7-32` + exact active PLAN。

**合同：**

- 新 experiment/run ID与新 root；
- 16 formal、ambient0、retry0；
- same A/D/B/C sequence和600 anchors；
- existing frozen strip commands、observer、quality、no-ambient statistic、Human 600 override；
- Ray intensity0，source isolation/readback；
- Ray R6只通过immutable manifest引用，不在 acquisition中pooling；
- 若 existing bounded strip exposure setup确有需要，可在旧合同内最多8 setup、formal16、总physical≤24；
  若需要改变 observer/threshold/feature/exposure envelope/command，立即进入 `REF-P7-39`；
- cleanup/final-zero/terminal seal与Ray同等级。

**失败与 stop：** 任一 failure即hard-stop、retry0；combined analyzer0。只有16/16才进入 `REF-P7-34`。

### REF-P7-34：Strip-only TD-B analyzer gate

**状态：** `BLOCKED`

**依赖：** `REF-P7-33` 16/16。

**分析：** 重放strip evidence；A0/A_after_D/B/C history；D/B/C chronology；steady warning；
quality/exposure/command/source/physical/cleanup gates。不得由Ray pass抵消strip fail。

**出口：** history/quality pass只解锁combined；history fail或contract failure停Planner/Advisor，不自动TD-C。

### REF-P7-39：Strip scientific contract change

**状态：** `ADVISOR_DECISION`

**触发：** strip必须改变 observer、threshold、required feature、exposure envelope或command才能继续。

**请求：** 提交现有合同失败 evidence和最小 proposed change；不得现场改变、扩大 covariance或自行重拍。

### REF-P7-35：Combined TD-B operational-600 analyzer与 envelope v3

**状态：** `BLOCKED`

**依赖：** `REF-P7-31` + `REF-P7-34` pass。

**产物：**

```text
p7-operating-envelope-v3.json
p7-td-b-operational600-analysis-v1.json
```

**必须声明：**

```text
operating_envelope = developer_selected_operational_600s_transient_v1
operational_dwell_s = 600
steady_status = not_demonstrated
TD_A_status = settling_not_demonstrated_by_600
return_anchor_history_compatibility_ray = pass
return_anchor_history_compatibility_strip = pass
previous_state_scope = exact_TD_B_A_D_A_B_A_C_A_sequence
```

**combined pass：** Ray16/16、strip16/16、两源quality/history/exposure/commands/source isolation/physical ledgers/
cleanup/final-zero通过；old/new不pool；working tree/checkpoint/release不漂移；steady warning保留。

**禁止：** `t_formal=600`、settled/steady true、TD-A pass、跨run refit或用一个source抵消另一个。

**失败与 stop：** 任一失败使 `REF-P7-05=blocked`、TD-C locked；无自动correction或device run。

### REF-P7-05：TD-B 科学验收与 operating-envelope freeze

**状态：** `BLOCKED`

**依赖：** `REF-P7-35`。

**Planner review：** 独立验证两 source run、analyzers、combined artifacts、R5/EQ/R6 pooling禁令、policy/release/checkpoint、
all counts/hashes/cleanup和machine status schema。

**接受：** 只冻结 `developer_selected_operational_600s_transient_v1` 及 exact previous-state scope；
保持科学 settle false/null。接受后只解锁 `REF-P7-08` 的新 planning，不自动设备执行。

**拒绝：** 按 failure type进入 bounded offline correction、Advisor decision或stop；不得重跑Ray/strip。

## 10. TD-C 与 reference completion

### REF-P7-06：H0 full-scale vs 3072 thermal diagnostic

**状态：** `CONDITIONAL`

4.GUIDE 已为 R6 history/quality failures给出明确stop，不再从普通 failure自动进入旧 H0 diagnostic。只有新 Advisor/Planner
明确判断仍需要该旧分支时，才可比较 full-scale H0与3072；保持observer、时间轴、cleanup和证据owner。它不是P8 data，
不能从结果自动返回TD-C。

### REF-P7-08：TD-C operational-600 order-balanced core

**状态：** `LOCKED`

**依赖：** `REF-P7-05` accepted；新的独立 active PLAN；不得与strip TD-B连续运行。

**scope：**

```text
comparison = order-balanced under operational_600s_transient
steady_claim = false
state = H120/S100
S1 Ray -> strip
S2 strip -> Ray
S3 Ray -> strip
S4 strip -> Ray
formal = 8
ambient = 8 (保留3.GUIDE未被替代的start/end diagnostics)
```

**实现/证据：** 四 independent sessions、frozen operational dwell和previous-state contract、source isolation、
exposure/timing/physical ledgers、ambient/geometry/black-level、双 cleanup。不得称 classic ABBA或linear drift eliminated。

**验收：** within-session difference兼容、order effect在frozen envelope、current Ray center/P6可解释、ambient不解释difference、
全部工程gate通过。

**失败与 stop：** 任一gate false为 `td_c_gate_failed`；无论pass/fail先回Planner，不自动endpoints。

### REF-P7-09：TD-C endpoint expansion

**状态：** `LOCKED`

**依赖：** `REF-P7-08` accepted且reference classification仍需要。

**计划：** H0/S0与H300/S100各一条Ray→strip和一条strip→Ray session；新增8 formal+8 ambient；
沿用operational-600 transient、source isolation和cleanup。不称steady ABBA。

**验收/stop：** exact gate与core一致；完成后回Planner，不能自动requalification。

### REF-P7-10：Reference epoch 分类与 P6 compatibility

**状态：** `BLOCKED`

**输入：** TD-A/B/C、P6 centers、operating envelope v3、ambient/order/history evidence。

**产物：** `reference-epoch-analysis-v2.json`；分类只允许 none/common/state_dependent/
operating_envelope_mismatch/not_identifiable。legacy `reference_epoch_shift=false` 不得解释为no shift。

**分支：** none保留P6；common/state-dependent进入`REF-P7-11`；envelope mismatch版本化scope；
not-identifiable阻塞。不得自动移动P6、回退HSL/affine或重拍106点。

### REF-P7-11：7-point / 13-node Ray requalification

**状态：** `CONDITIONAL`

**依赖：** reference common/state-dependent + Advisor exact targets/budget/criteria。

**边界：** 7点先判断common shift/local topology；只有满足门才13点；不得same-data refit-and-pass；新manifold需独立holdout。

**stop：** 7点、13点分别回Advisor；完整106点仍锁定。

### REF-P7-12：Thermal/reference AUDIT PACK 与 sentinel 解锁

**状态：** `ADVISOR_DECISION`

**依赖：** reference class可解释；必要requalification接受；cleanup/readback全零。

**AUDIT：** TD-A/B/C methods、budgets、sources/hashes、exposure policies、operating envelope、chronology/history/order、
reference classification、failed runs、tests/checkpoint/release、安全和residual risks。

**出口：** explicit sentinel release、targeted correction、restricted envelope、block或stop。无Advisor explicit release不进入sentinel。

## 11. P7 INT100、boundary 与 holdout

### REF-P7-13：四点 sentinel v2

**状态：** `LOCKED`

**依赖：** `REF-P7-12` explicit release；全部 observer/location/manifold/uncertainty/policy/envelope/checkpoint冻结。

**顺序：** H0/S0、H120/S100、H120/S50、H300/S100。每点沿用two-face solver、full-scale4095、
三次independent confirmation、scope-aware fields、physical/logical budget、source isolation和cleanup。

**reference anchors：** approved operational envelope下的pre/post Ray health checks，不进入strip samples。

**验收/失败：** 四点结构合法，冻结faithful/unresolved branch；任一measurement/solver/reference/cleanup failure停Planner；
retry必须new PLAN/root。

### REF-P7-14：Remaining 9 INT100 points

**状态：** `LOCKED`

**依赖：** sentinel accepted。

```text
H0/S50, H0/S100,
H60/S50, H60/S100,
H180/S50, H180/S100,
H240/S50, H240/S100,
H300/S50
```

使用同一approved envelope、solver、confirmation、uncertainty、budgets和cleanup。完成门是13点均有可重放status；
failure不得改写为gamut/physical unreachable。

### REF-P7-15：Full-scale boundary 与 scale-relaxed diagnostics

**状态：** `LOCKED`

**依赖：** 13-point pilot accepted。

**计划：** faithful下界+合法non-faithful上界、bracket≤5 SAT、Gate-6≤2 SAT、两端各5 confirmation、
active-set/white/inverse/Hue identifiability；transition附近加点有硬cap。

**scale relaxed：** 3072必测，必要时2048；不改变Ray INT100，不是P8。通过只证明full-scale operating boundary，
失败也不证明物理gamut。

### REF-P7-16：Independent holdout 与 runtime gamut semantics

**状态：** `LOCKED`

**依赖：** candidate/boundary冻结。

**矩阵：** 0/360、至少6个六sector non-node、高曲率、boundary两侧/active-set transition、五次confirmation、
reference/uncertainty/checkpoint全链。holdout不得调阈值或refit。

**semantics：** faithful/unconfirmed/measurement_unreachable/uncertainty_unresolved/solver_budget_exhausted/
boundary_bracketed/gamut_compressed/empirically_unreachable均带scope。

**失败与 stop：** 不进入P8；targeted correction或restrict range，不能扩大tolerance。

### REF-P7-17：P8 entry review

**状态：** `ADVISOR_DECISION`

**输入：** 13 points、六Hue status、boundaries、holdout、full-scale/relaxed语义、candidate confirmation、
reference/uncertainty provenance。

**出口：** exact P8 scope、targeted P7 repeat、restrict range或stop。Planner/Executer不得自行进入P8。

## 12. P8、Gate-6、P9 与交付

### REF-P8-01：INT acquisition、model branch 与 holdout

**状态：** `LOCKED`

**依赖：** `REF-P7-17` explicit release。

**采样：** INT100/50/20/5覆盖SAT0、主色/补色、SAT50、worst boundary、white-heavy、RGB-only和低PWM风险；
目标是Ray relative intensity，不是绝对照度。

**模型：** 只选择最小I-A separable、I-B low-int correction或I-C sparse coupling；规模不可控则限制产品range，
禁止无界dense 3D LUT。

**holdout/stop：** 冻结后独立Hue/SAT/INT/boundary/cross-day holdout；结果回Gate-6，不安装。

### REF-G6-01：Gate-6 final candidate/product freeze

**状态：** `ADVISOR_DECISION`

**输入：** P7/P8 candidates、training/holdout、gamut、INT branch、supported range、failure ledger、reference/
uncertainty/safety evidence和P9 proposal。

**出口：** freeze、targeted repeat、restrict range或stop。冻结public semantics、candidate hash、P9 immutable matrix。

### REF-P9-01：Immutable final independent validation

**状态：** `LOCKED`

**依赖：** Gate-6 freeze。

**最低矩阵：** coarse nodes、≥50分层未拟合随机点、0/360、SAT边缘、boundary两侧、worst Hue、multiple INT、
same/cross-day、fixed anchors。运行中禁止优化。

**报告/失败：** P50/P90/P95/max、training vs holdout、same vs cross-day、全部failures；candidate/hash变化或调参使run失效。

### REF-G7-01：Gate-7 technical delivery

**状态：** `ADVISOR_DECISION`

**输入：** immutable P9、all failures、candidate hashes、rollback和安全 evidence。

**出口：** install all、CCT only、HSI scoped、hold、repeat、rollback或stop；不替代Human产品决定。

### REF-OPS-01：Install、smoke test、rollback 与交付

**状态：** `HUMAN_DECISION`

**依赖：** Gate-7 + Human exact candidate/config/install决定；firmware/deployment若存在另需危险操作授权。

**计划：** backup/hash、atomic install、representative commands、runtime/version、cleanup/final-zero、rollback验证。
失败立即rollback并保留evidence，不现场优化。

### REF-CLOSE-01：Final AUDIT PACK 与关闭

**状态：** `BLOCKED`

汇总全部 GUIDE/Human provenance、archives、candidates/config hashes、P9/Gate-7、delivery/hold/rollback、
limitations、scope、reproduction/rollback、tests/safety/deferred branches。Advisor review后由Human关闭或新开GUIDE。

## 13. 当前延后分支

### REF-CCT-01：完整 CCT/GM P5

`DEFERRED`。只有新Advisor/Human重开；P4 diagnostic-only不得冒充完整candidate。

### REF-ABBA-01：Classic ABBA

`DEFERRED`。当前只批准operational-600 order-balanced comparison；不得声称linear drift eliminated。

### REF-P6-FULL-01：完整 P6 106-point re-capture

`DEFERRED`。只有7/13-point证明topology变化且Advisor明确批准。

### REF-LUX-01：绝对照度

`DEFERRED`。需要新metrology GUIDE、仪表/几何/单位/uncertainty；不得从camera RGB推断。

## 14. 全局不可变 guardrails

- R5 formal pass永久false；R5 root、failure/run/ledger/sidecar/terminal evidence只读。
- R5 retained 11仅diagnostic；old/new pooling一律禁止。
- 011 clipping不进入feature vector、center、covariance、history或reference analysis。
- Observer、58 features、P1 `1.0x..1.25x` identity-response/quality envelope、clipping threshold0、
  near-noise、valid-pixel、nonfinite、covariance、joint coverage、no-ambient statistic均不变；confirmation
  或qualification data不得扩大tolerance。
- A/D/B shutters exact取自R5；C只允许EQ选择1/2500或1/3200。无新Advisor决定不尝试更快或自动曝光。
- 1/2500只有clipping failure才能进入1/3200；其他failure立即停。
- EQ最多8 CR3、formal0；R6 formal16/physical16/setup0；EQ+R6 physical最大24；retry均0。
- 600秒是selected transient，不是steady、settled、TD-A pass或`t_formal`。
- Ray R6 16/16且A history pass前strip locked；两source combined pass前TD-C locked；Advisor前sentinel/P8 locked。
- 每个设备stage使用新root、single PLAN、visible Terminal（>10min）、abort、Python/shell cleanup、
  independent final-zero、terminal seal；不得跨stage连续自动长跑。
- Ray与strip不得同时非零；每个returned CR3先写physical-return ledger，rejection也保留sidecar/remote IDs/hash。
- Release generation/qualification/consumption、device access与formal launch分离；R2不得复用，R3只能在EQ后final policy checkpoint生成一次。
- Public shared protocol default按Human分类保留；private explicit override不打印、不序列化、不写CLI。
- Firmware/flash、remote deployment、destructive hardware change和PLAN外操作需Human授权；普通bounded light/zero、
  offline release/validation不因FULL而增加危险操作授权要求。
- 不将measurement/quality/solver/uncertainty failure写成gamut或物理不可达。
- 不覆盖default LUT、安装runtime candidate或进入P8/P9/交付，除非对应decision task完成。

## 15. Orchestrator 当前交接点

当前 loop 状态：

```text
REF-P7-22 Human checkpoint = accepted complete
REF-P7-23-C0 = superseded by accepted C1/C1E1 corrections
REF-P7-23-C1/C1E1 = accepted complete
REF-P7-23-C3/C3E2 = accepted complete
REF-P7-23-C4 = rejected predevice path mapping; archived
REF-P7-23-H2 = superseded authorization misclassification
REF-P7-23 = accepted qualified_1_2500
REF-P7-24 R1 = rejected preedit manifest serialization ambiguity
REF-P7-24-C1 implementation/checkpoint = accepted; evidence incomplete
REF-P7-24-C1E1 / REF-P7-24 = accepted complete
REF-P7-25 R1 = rejected preacquisition old-R2 manifest ambiguity
REF-P7-25-C1 = rejected changed-path policy after one truthful qualification
REF-P7-25-C2 = rejected postcommit focused test; production commit retained not accepted
REF-P7-25-C2E1 = rejected full discovery invocation; exact test diff retained
REF-P7-25-C2E2 = accepted complete
REF-P7-25-R2 = rejected release audit ledger shape; retained release unvalidated/unconsumed
REF-P7-25-R2-C1 = rejected pre-persistence parent-root contract
REF-P7-25-R2-C1R1 = rejected source-persistence writer failure
REF-P7-25-R2-C1R2 = rejected outer-writer preflight false rejection
current code HEAD = 9303aa22a9bd37e8ec4f23147c78c6bea84b9a2e
release checkpoint = 32b9e670ff3bbea0cd1505528c2ca87c2935446c
ownership selection = Option A repo-owned retained-release audit helper
Option A owner prerequisite = accepted complete
Advisor lineage owner decision = Option B subordinate exact provenance manifest
Human engineering governance override = Orchestrator owns files/code/provenance/execution/Git
helper v1 disposition = retained_release_audit_prerequisite_v1_superseded_before_real_validation
repair v2 status = B2-C1 path-owner index accepted; corrected B2 waiting PLAN-only activation
accepted B1 result = ACCEPTED_BLOCKED_CONTRACT_CONFLICT
accepted B1A result = HARD_FAILURE_PRE_ACQUISITION_LIFECYCLE; implementation progress 0
accepted B1A-C1 result = HARD_FAILURE_BEFORE_TEST_EXEC; candidate carry-forward only
accepted B1A-C2 result = FALSE_REJECTION_CONTROLLER_CONSTANT_DRIFT; source unchanged
accepted B1A-C3 result = PRE_ROOT_FULL_MACHINE_FIELD_OMISSION; candidate untouched
accepted B1A-C3E1 result = PRE_ROOT_PYTHON_SYMLINK_FALSE_REJECTION; candidate untouched
accepted B1A-C3E2 result = PRE_ROOT_CANONICALIZATION_SCOPE_FALSE_REJECTION; candidate untouched
accepted B1A-C3E3 result = PATCH_ARGV_AND_PREMATURE_STATUS_HARD_FAILURE; candidate exact
accepted B1A-C3E4 result = FIRST_REAL_FOCUSED_FAILURE; 3 failures / 66 fixture errors
accepted B1A-C3E5D1 result = FIXTURE_OWNED_HISTORICAL_PASS; one checkout test failure
accepted B1A-C3E5D2 result = CHECKOUT_FIX_ACCEPTED; focused ambient-HEAD lineage-test defect
accepted B1A-C3E5D3 result = TEST_ONLY_PASS; targeted2/2 focused102/102
old candidate SHA = 5b9408f2dafd0db47c45f2639dd0ed7a32e7db030871eaaa5d1f0e893a6468c2 SUPERSEDED
active candidate SHA = 3c5847fcbe0af85833c901f6f01058d000a3cecdc0f84e6ae331ed24e138c225
accepted B1A-C3E6F1 result = FULL_HERMETICITY_FAILURE; focused102 pass, full664 errors18
accepted B1A-C3E6F2 result = TARGETED_EXTERNAL_INPUT_AND_PROVENANCE_OWNER; raw test pass, targeted134 errors20
accepted B1A-C3E6F3 result = PRE_ACQUISITION_READ_ORDER_FAILURE; root0, budgeted reads consumed2
accepted B1A-C3E6F4 result = PRE_ROOT_MACHINE_ROW_PARSER_FAILURE; root0, budgeted reads0
accepted B1A-C3E6F5 result = CLOSURE_AST_PREDICATE_FAILURE; root1, acquisitions4/5, tests0
accepted B1A-C3E6F6 result = FULL_SUBSET_SHAPE_FAILURE; 12/12 matched, root0
accepted B1A-C3E6F7 result = IGNORE_PRESENTATION_BINDING_FAILURE; root1, observed2/5, tests0
accepted B1A-C3E6F8 result = CLOSURE_OWNER_PATH_FAILURE; root1, observed5/5, tests0
accepted B1A-C3E6F9 result = TRACKED_TARGET_EXCLUSIVE_CREATE_FAILURE; acquisitions5/5, tests0
accepted B1A-C3E6F10 result = NESTED_CLOSURE_AST_SHAPE_FAILURE; atomic replace passed, acquisitions4/5, tests0
accepted B1A-C3E6F11 result = CONTROLLER_KEYERROR_ROOT_REUSE_AND_ACCOUNTING_CONTRADICTION; retry1, contaminated reads5, tests0
accepted B1A-C3E6F12 result = WORKTREE_BLOB_ORACLE_FALSE_REJECTION; atomic replace exact, index parent blob misread as worktree blob
accepted B1A-C3E6F13 result = PACKAGE_LEVEL_RETRY_AND_ROOT_PROLIFERATION; authoritative first root failed checkout cwd, later6 retries rejected
accepted B1A-C3E6F14 result = PRE_ROOT_FIXED_CONTAINER_ABSENT_HARD_FAILURE; qualification pass, invocation1, root0, retry0
accepted B1A-C3E6F15 result = DISPATCHER_READ_SCOPE_VIOLATION; bootstrap attempts0, all fixed paths absent
accepted B1A-C3E6F16 result = PLAN_ROW_LABEL_PRECONDITION_FAILURE; paths unchecked and all attempts0
accepted B1A-C3E6F17 result = LIMITED_INPUT_MARKER_AND_PATH_INSPECTION_VIOLATION; counters0/0; no artifact
accepted B1A-C3E6F17-CORRECTIVE-1 result = CONTRACT_FIELD_BINDING_MISMATCH; counters0/0; no artifact
accepted B1A-C3E6F17-CORRECTIVE-2 result = MARKER_COUNT_GATE; PLAN2/FULL3; counters0/0; ER absent
accepted B1A-C3E6F17-CORRECTIVE-3 result = INVOCATION_LAYER_SYNTAX_FAILURE; counters0/0; ER absent
accepted B1A-C3E6F17-CORRECTIVE-4 result = CONTRACT_QUALIFICATION_8_OF_12; counters0/0; ER appended
accepted B1A-C3E6F17-CORRECTIVE-5 result = CANDIDATE_AND_FIELD_FREEZE; PLAN2/FULL3; subset0; counters0/0; ER appended
accepted B1A-C3E6F17-CORRECTIVE-6 result = SCANNER_SEMANTICS_MISMATCH; candidate0/0; counters0/0; ER appended
accepted B1A-C3E6F17-CORRECTIVE-7 result = EXECUTOR_NEWLINE_MISJUDGMENT; line17 LF present; counters0/0; ER appended
accepted B1A-C3E6F17-CORRECTIVE-8 result = COMMAND_QUOTING_FAILURE; counters0/0; ER absent
accepted B1A-C3E6F17-CORRECTIVE-9 result = JS_BASE64_ENCODER_UNAVAILABLE; exec0; ER absent
accepted B1A-C3E6F17-CORRECTIVE-10 result = INPUT_OWNER_BINDING; subset12/12; zero0/19; counters0/0; ER appended
accepted B1A-C3E6F17-CORRECTIVE-11 result = PLAN_SCANNER_FALSE_NEGATIVE; actual candidates1/1; reported plan0; counters0/0; ER appended
accepted B1A-C3E6F17-CORRECTIVE-12 result = REPEATED_SCANNER_FALSE_NEGATIVE; actual candidates1/1; reported0/0; counters0/0; ER appended
accepted B1A-C3E6F17-CORRECTIVE-13 result = VALIDATION_ONLY_SCANNER_OWNER_ACCEPTED; Executer11/11; Planner11/11; eligibility0
accepted B1A-C3E6F17-C13-LINEAGE-SEAL result = EXACT_SIX_PATH_COMMIT_ACCEPTED; commit64c34ad; retainedR3 untouched
accepted B1A-C3E6F18 result = IMPORT_OWNER_AND_TERMINAL_EVIDENCE_FAILURE; external paths untouched; ER0
accepted B1A-C3E6F18-CORRECTIVE-1 result = BOOTSTRAP_PREREQUISITE_ONLY; empty0700; record/seal0600; validator0
accepted B1A-C3E6F19 result = DEDICATED_STATIC_TEST_FALSE_POSITIVE; compile0; targeted10/11; later tests0; real operations0
accepted B1A-C3E6F19-CORRECTIVE-1 result = WRONG_PLAN_MARKER_OWNER; edits0; tests0; ER0; fresh root absent
accepted B1A-C3E6F19-CORRECTIVE-2 result = STORE_FAST_LOCAL_BINDING_FALSE_POSITIVE; helper1/1; targeted10/11; later0
accepted B1A-C3E6F19-CORRECTIVE-3 result = PRE_EDIT_FIELD_OWNER_KEYERROR; helper1/1; edits0; tests0; ER1
accepted B1A-C3E6F19-CORRECTIVE-4 result = EXPECTED_DIGEST_TRANSCRIPTION_ERROR; ledger12/12; evidence unchanged; edits0
accepted B1A-C3E6F19-CORRECTIVE-5 result = UNFROZEN_TERMINAL_SCHEMA_CARDINALITY; identities5/5; edits0; tests0
accepted B1A-C3E6F19-CORRECTIVE-6 result = UNAUTHORIZED_WHOLE_RECORD_KEY_SET; schema gates pass; edits0; tests0
accepted B1A-C3E6F19-CORRECTIVE-7 result = LOG_NOCLOBBER_REOPEN_CONFLICT; test edit accepted; validation0
accepted B1A-C3E6F19-CORRECTIVE-8 result = FULL_SUITE_AMBIENT_GOVERNANCE_LINEAGE_DRIFT; targeted11/11; focused43/43; full1 failure9 errors
accepted B1A-C3E6F19-CORRECTIVE-9 result = FORMAL_COMPILEALL_CONSUMED_BEFORE_IMPLEMENTATION_COMMIT; draft preserved cc37da5; test unchanged
accepted B1A-C3E6F19-CORRECTIVE-10 result = TARGETED_AMBIENT_HEAD_AND_HISTORICAL_CHECKPOINT_SEAMS; new tests pass; targeted9/12
accepted B1A-C3E6F19-CORRECTIVE-11 result = TARGETED_AMBIENT_FULL_SET_EXPECTATION_ONLY; production seam tests pass; targeted12/13
accepted B1A-C3E6F19-CORRECTIVE-12 result = POSTCOMMIT_EXPECTED_CHILD_SHA_TRANSCRIPTION_ONLY; test commit exact; validation0
accepted B1A-C3E6F19-CORRECTIVE-13 result = SOURCE_TOPOLOGY_CONTRACT_MISMATCH; programmatic HEAD pass; validation0
accepted B1A-C3E6F19-CORRECTIVE-14 result = FULL_SUITE_EQ_R6_MANIFEST_METADATA_DRIFT; targeted13/13; focused125/125; full687 failures2
accepted B1A-C3E6F19-CORRECTIVE-15 result = PREVALIDATION_EVIDENCE_ORDER; implementation3a14fe0 retained; validation0
accepted B1A-C3E6F19-CORRECTIVE-16 result = FOCUSED_POST_EQ_VALIDATION_SUCCESSOR_MISSING; targeted6/6; focused193 failures1 errors2
accepted B1A-C3E6F19-CORRECTIVE-17 result = ACCEPTED_COMPLETE_POST_EQ_VALIDATION_SUCCESSOR; targeted5/5; focused195/195; full691/691
accepted B2 result = FROZEN_RETAINED_SOURCE_PATH_ENOENT; lstat/open/read1/0/0; manifest0; retry0
accepted B2-C1 result = ACCEPTED_EXACT_PATH_OWNER_INDEX_ONLY; resolved paths3; artifact content reads0
active task = REF-P7-25-R2-B2 corrected exact-path modern manifest seal
active contract = P7-TD-B-RETAINED-R3-OPTION-B-B2-CORRECTED-PATH-MANIFEST-SEAL-V3
active executable task count = 0
next reference task = REF-P7-25-R2-B3 BLOCKED_ON_B2_ACCEPTANCE
selected state C shutter = 1/2500
device/network/camera/light = forbidden by active PLAN
release qualification/generation/copy/consumption = forbidden
full formal R6/strip/public analyzer/TD-C = forbidden
```

Human已明确恢复执行并覆盖旧Advisor工程限制。B1证明旧Option B exact two-path合同与canonical-validator seam要求
不相容且由Planner接受为`ACCEPTED_BLOCKED_CONTRACT_CONFLICT`；该证据继续有效，但不再构成Advisor stop。首次B1A
因acquisition lifecycle错误在implementation前hard-fail；C1修复acquisition并形成exact-five candidate，但因错误pytest
runtime在test exec前hard-fail；C2又因temporary controller手工转录错误SHA而false-reject未漂移的source。三次失败后
ownership reassessment已移除candidate fact副本；C3又因FULL漏写两个required machine字段在root前正确停止。C3E1的
programmatic activation与exact subset-check通过，但Executer controller擅加non-symlink predicate而错误拒绝合法Python
入口。C3E2修正runtime probe后又把candidate canonical predicate错误扩张到PLAN/FULL rows。Planner已签发
`REF-P7-25-R2-B1A-C3E3`已把同一strict candidate JSON object带过clone/source验证，但patch argv和evidence status时序失败。
`REF-P7-25-R2-B1A-C3E6F13`因package-level retry violation rejected；F14虽完成exact frozen-controller qualification，
但唯一controller在fresh root前因fixed container absent hard-fail。F15又因CLI dispatcher在bootstrap前自动读取memory/broad FULL而rejected，
F17 的 context-closed direct Executer 在输入 gate 报 `PLAN exact marker count 0`，且随后错误检查四条固定路径，故已由
Planner 拒绝并归档；C3E6F17-CORRECTIVE-1 又因 canonical `task_id` 与 PLAN `reference_task_id` 不一致而拒绝，均不得重试
旧 root。C3E6F17-CORRECTIVE-2 因 PLAN2/FULL3 marker rows 在 path operation 前拒绝，C3E6F17-CORRECTIVE-3 又因调用层
JavaScript SyntaxError 未启动 Python；C4 随后仅 8/12，C5 又因正文 marker candidates 与未冻结字段失败，C6 又报 candidate0；
之后 wrapper、newline、base64 与 input-owner 多轮纠偏均保持所有执行预算为零。C11 的两文件 hash 与真实 machine rows 均正确，
但 Executer scanner 将 PLAN candidate 错计为0；C12 的更精确文字合同仍因临时实现转录漂移错报0/0。当前 C13 将 scanner
收敛到一个validation-only helper与一个dedicated test并获Planner接受，避免继续复制实现；它不拥有eligibility或retained-release语义。
后继另包才可冻结新controller并建立 fresh bootstrap container；不得重跑F14、提前修改production或输出eligibility。retained R3继续为
`REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-14`已证明retained topology、targeted与focused均通过，但full被accepted EQ-R6 root
顶层非证据`.DS_Store`污染整树manifest而拒绝；`REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-15`仅在既有manifest owner内加入
root-relative exact regular `.DS_Store`边界并用dedicated tests锁定；C15实现已形成但因prevalidation evidence order拒收，
`REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-16`证明metadata实现targeted通过，但focused暴露post-EQ历史blob缺少exact successor；
`REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-17`在同一lineage owner内绑定`3a14fe0`exact subordinate successor并以full691/691获接受；
`REF-P7-25-R2-B2`首次manifest-only执行因stale frozen source path在首个lstat处拒绝；`REF-P7-25-R2-B2-C1`只验证历史命名的
exact三层directory chain及artifact name/type/path，content reads保持0，并已获Planner接受；corrected B2须在独立PLAN-only activation后
从sealed C1 evidence读取exact paths，旧root与旧路径不得重试；
canonical validator call、eligibility emission、retained R3/release/device访问仍为0；
retained R3 仍为 `RETAINED_UNVALIDATED_UNCONSUMED`。

B1A-B5均为offline validation/provenance工作，不命中AGENTS高危设备授权；但这不等于当前已授权执行。Release
consumption、qualification/re-generation、retained payload repair/copy、network、device、camera、Ray、FORMAL-R6、
strip、public scientific analyzer、TD-C、sentinel与P8持续锁定。

维护性判断：新路线继续复用现有 thermal plan、measurement、feature、analyzer、lineage和lifecycle owners；
新增的是 versioned exposure policy 与分阶段验证，不应建立平行 runner/analyzer。离线实现需按
R5 disposition、EQ owner、R6 analyzer三个边界逐步验收，避免把新策略堆入单一 coordinator。
