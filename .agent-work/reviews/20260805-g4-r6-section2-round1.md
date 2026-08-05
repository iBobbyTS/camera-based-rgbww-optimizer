# G4 R6 Section 2 独立代码审查（Round 1）

## 合并结论

`not mergeable`

发现 1 个开放的 `Must Fix` provenance 完整性缺陷：新增的
accepted-engineering prerequisite 投影只校验 SHA 外形，没有与同一
stage gate 中已经通过 Git 验证的 source-attestation identity 绑定。因此当前
validator 可以把内部自相矛盾的 package evidence 判为有效。

## 主要发现

### REV-S2-001 — prerequisite 中的 accepted-engineering identity 未与 source attestation 绑定

- 严重性：`Must Fix`
- 决策类：`Agent-Fixable`
- 状态：`Open`
- 置信度：高
- 范围：
  `src/camera_based_rgbww_optimizer/optimization/p7_td_b_r6_stage_gate.py:531`、
  `src/camera_based_rgbww_optimizer/optimization/p7_td_b_r6_stage_gate.py:1169`、
  `tests/test_p7_td_b_r6_stage_gate.py:941`

#### 触发条件与证据路径

1. Section 2 把 `accepted_engineering_checkpoint` / `accepted_engineering_tree`
   新增到 `prerequisites` 中。
2. `_validate_prerequisite_projection()` 对这两个值只做 `_SHA40`
   格式检查（约 545–549 行）。
3. `validate_stage_gate()` 会先从 `source_attestation_binding` 完成真实 Git
   checkpoint/tree/parent/subject/path/blob 验证，但在调用
   `_validate_prerequisite_projection()` 前后都没有将 prerequisite 中的两个字段
   与该 binding 比较。
4. 独立微型反证中，保留真实 synthetic Git attestation，仅把
   prerequisite checkpoint/tree 改为 `000...000` / `111...111`，然后调用
   `subject.validate_stage_gate(altered, repo_root=fixture.root)`。命令退出码为
   `0`，输出 `ALTERED_PREREQUISITES_ACCEPTED`；同时 binding 仍声明另一个
   checkpoint。

#### 影响

- `stage-gate.json` 可以声称一个从未被 attestation 证明的 accepted engineering
  checkpoint/tree，而同一 artifact 的 source binding 证明另一个。
- `_load_stage_gate_package()` / public replay 依赖 `validate_stage_gate()` 作为
  该 artifact 的语义门禁；因此在引用 SHA/终端 seal 也被一致重建的情况下，
  replay 无法识别这种内部 provenance 矛盾。
- 这直接违反本 section 的核心不变量：unfinished-only FULL 投影中的
  accepted engineering identity 必须与已验证的唯一 source-attestation
  identity 一致。

#### 最小修复方向

- 在 `validate_stage_gate()` 的同一边界上，将 validated prerequisite 中的
  `accepted_engineering_checkpoint` / `accepted_engineering_tree` 与
  `_source_attestation_binding()` 返回的对应值做 exact equality 绑定；不要新建平行
  provenance owner。
- 在现有 test owner 增加持久负例：分别置换 checkpoint/tree 为格式合法但
  与 binding 不同的 SHA，断言稳定失败码且发生在 root/package/backend/device
  effect 之前。

#### 冻结验收条件

- [ ] 上述 `000...000` / `111...111` 触发不再被
  `validate_stage_gate()` 接受。
- [ ] checkpoint 和 tree 任意一个与 binding 不同都 fail closed。
- [ ] 正向 generate -> validate -> persist/replay 路径仍只投影同一组 accepted
  engineering identity。
- [ ] 修复不放宽 source reference、Git topology、authority、root/effect 顺序或既有
  descriptor-reference precedence。

## 审查范围与基线

- Repository：`/Users/ibobby/Projects/WLED-RGBWW`
- Range：
  `4e94594c117cd684e76b3607815f340cd2ca5919..7d02562db0afcffaa8f2a341345235a6310b654c`
- Patch SHA-256：
  `3912190464ffc74e141c99f06de931142324bcd0d1bc45d3143f802ca4eaf5df`
- Commit 拓扑：直接非 merge child；subject exact
  `fix(stage-gate): align replacement package owner`；只修改方案授权的 source/test 两个路径。
- 审查深度：`Large`（provenance package、public replay、future formal activation
  trust boundary）。
- 审查时 worktree 有 Planner 后续 governance/archive/debug 改动；它们不在本
  commit range 内，本轮没有把它们并入审查基线，也没有修改或清理。

## 意图与关键不变量

变更意图：在现有 stage-gate owner 内将 package task 改为
`REF-G4-06-REPLACEMENT-PACKAGE`，保留独立 future formal task，改用
unfinished-only FULL 投影，并把未来 code owner 限定为指定两路径的直接
non-merge child。

用于审查的不变量：

- package task 与 future formal task 必须不同，不得由 offline evidence
  推导 formal/device/release authority。
- accepted engineering checkpoint/tree 在 PLAN projection、FULL projection、
  stage-gate prerequisite 和 Git-validated source attestation 中必须是同一身份。
- root 创建、package 持久化、backend/delegate/device 效果之前必须完成所有机器
  contract 与 provenance 验证。
- 不得改动 Section 1 accepted-engineering validator、artifact inventory、
  persistence/replay/terminal/failure seal、descriptor-reference precedence 或 formal/runtime
  owner。

## 覆盖与关键路径

- `Reviewed` — 意图/领域语义：task/contract 替换、future task 分离、
  unfinished-only FULL 语义。
- `Reviewed` — 正确性与状态：PLAN/FULL projection -> `build_stage_gate_input()`
  -> `_projection()` -> `evaluate_stage_gate()` -> `validate_stage_gate()`。
- `Reviewed` — 数据/provenance：source references、accepted engineering identity、
  code-child/post-child Git topology、artifact self-consistency。
- `Reviewed` — 安全/信任边界：authority false、secret/historical guards、
  pre-root ordering、失败封存。
- `Reviewed` — 可靠性/发布：persist -> terminal seal -> public replay ->
  future formal loader/activation 影响锥。
- `Reviewed` — 架构/维护性：变更仍留在原有 production/test owner，
  未新建平行 schema/controller/CLI/persistence owner。
- `Reviewed` — 测试/验证：synthetic real-Git fixture、projection drift matrix、
  topology negatives、已记录的 focused/full 结果，以及本轮独立微型反证。
- `Reviewed` — AI-agent 风险：检查了 synthetic fixture 自证、弱 oracle、
  projection 声明与真实 source-of-truth 脱节。
- `Skipped` — UI/accessibility：本 diff 无 UI 或交互面。
- `Skipped` — dependencies/supply chain：本 diff 无依赖、lockfile、CI 或
  build 配置变更。
- `Skipped` — performance/cost：无新的无界循环、网络请求、大数据处理或
  model 调用。

## 验证

### 本轮已运行/核验

| 命令/证据 | 结果 | 限制 |
| --- | --- | --- |
| `git status --short --branch`、`git show`、`git diff-tree`、blob/SHA 检查 | base/head、subject、parent、tree、exact two paths 和冻结 blob/SHA 相符 | worktree 存在不属于 range 的 Planner 后续改动 |
| `git diff --check 4e94594..7d02562` | PASS | 无 |
| `codegraph explore` 的 owner/caller/impact 查询 | 确认现有 owner、public package loader/replay 影响锥 | 无设备/网络路径 |
| prerequisite/binding 交叉身份微型反证 | FAIL AS DESIGNED FOR REVIEW：validator 错误接受矛盾身份，复现 `REV-S2-001` | 仅使用 ephemeral synthetic Git repo；未持久化 package，未访问正式 root |
| full log identity `/Volumes/4T/temp/rgbww-optimizer/g4-r6-section2-valid-full-20260805-b73d91f4.log` | `31889` bytes / `481` lines / SHA-256 `e71af39f...dedea`；`979` tests，`2 failures + 8 errors` | 非 full green；十个均是记录中的 `AGENTS.md` governance-lineage group |

### 未运行

| 检查 | 原因 | 剩余风险 |
| --- | --- | --- |
| 重跑 51-test stage-gate focused suite | 当前 Planner stop 对审查阶段记录 `test_invocation_cap=0`；已检查冻结候选身份和原始 full log，并使用更精确的独立反证检查新投影边界 | 归档的 `51/51 PASS` 未在本轮重放；它本身也未覆盖 finding 触发 |
| 重跑 full suite | 现行流程不允许 review 阶段新的 full 调用，且已有当前冻结身份对应的原始日志 | 当前 full 证据为 qualified non-green，不得称为 full green |
| 真实 package prepare/describe/replay 和 formal/device path | 本轮明确禁止 package/formal root、device、network 及外部效果 | 未执行端到端 package I/O；本 finding 在 pre-persistence validator 层已可确定复现 |

## 修复、reset 与剩余风险

- 本轮未授权 repair；修复 finding：无。
- Reset 事件：无；base/head 在审查期间保持
  `4e94594c..7d02562d`。
- 除 `REV-S2-001` 外，尚有一个明示证据缺口：仓库尚未有本
  Section 2 结束后的新 package-preparation executable PLAN，因此 synthetic
  positive fixture 与未来真实 PLAN/FULL 的完整集成只能在后续该 PLAN 冻结后复核。
  当前硬编码的
  `ACTIVE_SECTION_2_REPLACEMENT_TASK_PROJECTION_AND_CHILD_TOPOLOGY` 不应在没有
  Orchestrator 后续 machine-contract 决定的情况下被当作已验证的未来状态。
- 停止条件：未满足；`REV-S2-001` 修复并经独立 delta review 关闭前，
  本 commit 不可合并/接受。
