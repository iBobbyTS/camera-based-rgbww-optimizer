# G4-R6 Section 2 独立代码审查（Round 2）

## 合并结论

`not mergeable`

存在 1 个 `Must Fix` 与 1 个 `Should Fix`。提交的两路径范围、直接非 merge
子提交拓扑及冻结候选字节均符合 Section 2 交付合同，但新增的 unfinished-only
FULL 投影和 stage-gate prerequisite 投影仍不是闭合的 fail-closed 合同。

## 主要发现

### REV-S2-R2-001 — 遗漏的权限键可以绕过 `all_authority_false`

- 严重性：`Must Fix`
- 决策类别：`Agent-Fixable`
- 状态：`Open`
- 位置：`src/camera_based_rgbww_optimizer/optimization/p7_td_b_r6_stage_gate.py:97`、`:497`
- 触发条件：在其余字段完全有效的 FULL machine row 中加入
  `formal_r6_authorized: true`、`device_authorized_by_this_file: true` 等旧权限键，
  或加入当前全局 hard lock 中但未列入 `_FULL_AUTHORITY_FIELDS` 的权限键；同时保持
  `_FULL_AUTHORITY_FIELDS` 中的字段为 `false`。
- 影响：`parse_full_plan_machine_state()` 会保留任意额外 JSON 键，而 `_projection()`
  只检查 `_FULL_AUTHORITY_FIELDS` 中的 13 个名字，并仅把
  `_ARCHIVED_PREREQUISITE_FIELDS` 当作禁止出现字段。上述权限键既不在前者，也不在
  后者，因此 machine contract 会被接受，随后 stage-gate 会序列化并宣称
  `all_authority_false`。这违反 Section 2 PLAN 的“any authority bit set 必须在 root
  effect 前拒绝”合同，也回退了父提交中对
  `device_authorized_by_this_file` / `camera_authorized_by_this_file` /
  `ray_authorized_by_this_file` / `strip_authorized_by_this_file` /
  `formal_r6_authorized` 的显式 fail-closed 检查。
- 证据：
  - 本提交删除了上述五个旧权限键的逐项 `is not False` 检查，改为
    `any(full.get(field) is not False for field in _FULL_AUTHORITY_FIELDS)`。
  - `agent_work_machine_contract._parse_machine_row()` 仅要求顶层是 JSON object，之后
    深冻结并原样返回，不执行 key allowlist。
  - 新测试矩阵通过遍历生产常量 `_FULL_AUTHORITY_FIELDS` 生成负例，因此无法发现
    生产列表本身漏项；它没有使用独立的字面量权限全集作 oracle。
- 最小修复方向：为 unfinished-only FULL projection 建立独立、权威的权限键集合；
  至少对被本提交移除的旧权限别名及 Section 2/global hard-lock 权限键 fail closed，
  并用不从 `_FULL_AUTHORITY_FIELDS` 派生的字面量负例验证遗漏键、旧别名和任一真值
  都在 `create_exclusive_root()` 前失败。
- 置信度：`High`

### REV-S2-R2-002 — stage-gate prerequisite 的 engineering 身份未绑定到 source attestation

- 严重性：`Should Fix`
- 决策类别：`Agent-Fixable`
- 状态：`Open`
- 位置：`src/camera_based_rgbww_optimizer/optimization/p7_td_b_r6_stage_gate.py:531`、`:1207`
- 触发条件：将已生成 stage-gate 的
  `prerequisites.accepted_engineering_checkpoint` 或
  `prerequisites.accepted_engineering_tree` 替换为任意其他合法 40 位十六进制值，并为
  包重新生成相应 canonical artifact reference / terminal seal。
- 影响：`validate_stage_gate()` 会先严格验证
  `source_attestation_binding` 中真正的 accepted-engineering commit/tree/path/blob，随后
  `_validate_prerequisite_projection()` 却只对 prerequisite 中这两个字段做 SHA-40
  格式检查，没有要求它们等于已验证 binding。公共 replay/production load 因此可以
  接受一个内部自相矛盾的 sealed package：source attestation 证明一个 engineering
  checkpoint，而 stage-gate prerequisite 对外声明另一个。当前执行权仍由 binding
  路径验证，故未证明直接设备授权绕过；但 replacement package 的 provenance claim
  不再可信。
- 证据：
  - `_projection()` 的创建路径从 `plan_binding` 派生这两个值，说明它们本应是同一身份。
  - `_validate_prerequisite_projection()` 仅在 `:546-549` 使用 `_SHA40.fullmatch()`；
    `validate_stage_gate()` 在调用该函数时没有传入或比较已验证的 binding。
  - `test_stage_gate_prerequisite_projection_is_closed` 只覆盖缺键、额外键和 authority
    漂移，没有覆盖 checkpoint/tree 与 binding 的交叉字段漂移。
- 最小修复方向：让 `_validate_prerequisite_projection()` 接受已规范化的
  `source_attestation_binding`（或在 `validate_stage_gate()` 中紧接着比较），强制两个
  prerequisite 身份与 binding 完全相等；新增 checkpoint/tree 各一个交叉字段漂移
  负例，并验证 public replay 在 backend/formal/device 前拒绝。
- 置信度：`High`

## 需要用户敲定的业务语义

无。两项均可从现有 Section 2 projection、fail-closed 和 provenance 合同直接确定，
不需要新增产品、科学或硬件政策。

## 审查范围与仓库状态

- 仓库：`/Users/ibobby/Projects/WLED-RGBWW`
- 审查范围：`7d02562^..7d02562`
- Base：`4e94594c117cd684e76b3607815f340cd2ca5919`
- Head：`7d02562db0afcffaa8f2a341345235a6310b654c`
- Patch SHA-256：`3912190464ffc74e141c99f06de931142324bcd0d1bc45d3143f802ca4eaf5df`
- 审查深度：`Large`（provenance、authority、formal/release 前置 gate）
- 提交拓扑：Head 是 base 的直接单父提交；subject 精确为
  `fix(stage-gate): align replacement package owner`；只修改既定 source/test 两路径。
- 冻结候选身份：source/test SHA-256 分别为
  `0ea07b949436599097633c3514f64881e750ed7b45ee92ad88a54e7becee48e0` /
  `540234e353e43d0a1f8c75f3a71b45dd23ace610e7e96d59e250c88b52c4d352`，
  blob 分别为 `6f7a7756687f669c067c253a5d5a30f84b5d6075` /
  `65e54f1594ed39c2be641124de71b946858c1e6b`，与冻结 PLAN 记录一致。
- 当前 `HEAD` 即审查 head。工作树存在 Orchestrator/Planner 的
  `.agent-work/` 未提交变更，但 source/test 两个提交路径相对 HEAD 无漂移；这些治理
  变更不属于本提交，也未纳入结论。
- Repair：未授权、未执行。

## 变更意图与关键不变量

变更意图：在既有 stage-gate 单一 owner 内，把 offline package 身份切换到
`REF-G4-06-REPLACEMENT-PACKAGE`，把未来 formal task 保持为独立的
`REF-G4-06-REPLACEMENT-R6`，采用 unfinished-only FULL projection，并绑定 exact
future code child topology。

关键不变量：

1. Package task 与 future formal task 必须不同，且 package evidence 不授予 formal、
   device、release 或后续阶段权限。
2. FULL 的 current unfinished projection 必须只投影当前 replacement task、accepted
   engineering identity、retained R3 与全部 false authority；旧 completed projection
   不得重新进入。
3. stage-gate 中的 accepted-engineering claim 必须与严格 Git 验证过的
   source-attestation binding 是同一身份。
4. 任何 machine/provenance 漂移必须在 package root、backend、formal 或 device effect
   之前失败。
5. Section 1 的 committed engineering Git 验证、descriptor reference precedence、
   persistence/replay/inventory/terminal/failure seal 与 runtime/formal owner 不得改变。

## 审查覆盖

| 风险镜头 | 状态 | 证据与边界 |
| --- | --- | --- |
| Intent/domain semantics | Reviewed | PLAN-FULL Section 2、激活 PLAN、raw diff、task/contract/status 常量 |
| Local correctness | Reviewed | `_projection`、`_validate_prerequisite_projection`、`validate_stage_gate` 边界/漂移路径 |
| Data/provenance | Reviewed | PLAN/FULL parser、source attestation、serialized gate、terminal replay |
| State/concurrency | Skipped | 本提交不改变 async、锁、重试或并发状态机 |
| Security/authority | Reviewed | 新/旧 authority 字段、all-false 声明、pre-root 拒绝顺序 |
| Reliability/release | Partial | 静态追踪到 production package load/formal dispatch；按授权未访问 package/formal root 或设备 |
| Performance/cost | Skipped | 无新增不受限循环、远程调用或重计算路径 |
| Architecture/maintainability | Reviewed | 保持既有单一 stage-gate owner，未新增模块/adapter/schema family |
| Dependencies/supply chain | Skipped | manifest、lockfile、CI/dependency 均未变 |
| Tests/validation integrity | Reviewed | 新负向矩阵、projection closedness、topology/subject tests；识别 production-derived oracle 缺口 |
| UI/accessibility | Skipped | 不涉及 UI |
| AI-agent/review risks | Reviewed | 冻结 candidate 身份、范围、测试 claim 与 raw Git 分离核对；未读取 Round 1 结论 |

### 关键路径

1. `PLAN/FULL bytes -> strict row parser -> _projection -> build_stage_gate_input ->
   evaluate_stage_gate -> persist_stage_gate_package/create_exclusive_root`：发现
   REV-S2-R2-001；其余 task/contract/current-state/accepted engineering cross-binding
   与 direct-child准备路径符合合同。
2. `sealed package -> terminal/artifact identity -> validate_stage_gate ->
   _validate_prerequisite_projection -> load_and_validate_stage_gate_package -> future formal
   dispatch`：发现 REV-S2-R2-002。
3. `descriptor binding -> validate_committed_source_attestation -> exact engineering commit /
   direct code child / linear .agent-work descendants`：未发现新的拓扑根因。

## 验证

### 已运行

| 命令/流程 | 结果 | 限制 |
| --- | --- | --- |
| `git rev-parse` / `git show` / `git diff-tree` / object SHA 与 blob 核对 | 通过 | 验证 base/head、单父、subject、两路径和冻结字节 |
| `git diff --check 7d02562^ 7d02562` | 通过 | 仅检查 patch whitespace/冲突标记 |
| `git merge-base --is-ancestor 5d01bc... 7d02562` | 通过 | 证明 accepted Section 1 位于当前提交祖先链 |
| CodeGraph 对 changed owner、machine parser、replay/formal impact cone 的查询 | 完成 | 静态 source/call-path 证据；未访问设备/网络 |

### 未运行

| 检查 | 原因 | 剩余风险 |
| --- | --- | --- |
| focused/full unittest | 当前 terminal PLAN 明确 `test_invocation_cap=0` 且禁止 test rerun；本轮只读审查不扩张授权 | 未独立复现历史 `51/51` 或 `979` non-green 结果；这不影响两个由源码可直接证明的 finding |
| package replay/formal/runtime 实操 | 用户明确禁止 package/formal roots、设备与网络 | 运行时/外设行为未复核；结论仅覆盖 offline owner/provenance 变更 |

既有 PLAN 中的 `51/51` focused 与 `979` 全量（`969 pass / 2 fail / 8 error`）仅作为
未在本轮复跑的历史 claim 记录，不作为关闭本轮 finding 的证据。

## 收敛与剩余风险

- 本轮模式：独立 `FINAL` fresh verification；先检查 raw commit/权威合同，再检查测试，
  未读取 Round 1 persuasive conclusion。
- Reset 事件：无；base/head 与冻结 candidate 身份一致。
- 新根因：2。
- 关闭/重开：0 / 0。
- 当前停止条件：不满足；存在未修复 `Must Fix` / `Should Fix`。
- 修复后应只复审 repair delta、上述两个 impact cone 和新增独立负向 oracle；任何修复
  均按 PLAN-FULL 规则重置 clean-review streak。
