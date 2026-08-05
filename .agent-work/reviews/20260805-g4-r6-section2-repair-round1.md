# G4-R6 Section 2 修复独立代码审查（Round 1）

## Findings

无 actionable finding。`REV-S2-AUTH-001` 与 `REV-S2-PROV-001` 的冻结触发均已由当前代码可见的 fail-closed guard 和独立回归 oracle 关闭；本轮没有发现 repair delta 或其失效影响锥内的新 root-cause class。

## 合并结论

`mergeable`

该结论只覆盖 `75d3277^..75d3277` 的 Section 2 repair delta。它不等于 full green，不解锁后续 Section 2/Package-B 阶段，也不授权 package prepare/describe、formal R6、root 创建、设备、网络、相机、Ray、strip、capture、release consumption、G4-07 或 TD-C。

## 已关闭 finding

### REV-S2-AUTH-001 — unfinished FULL projection authority vocabulary 未闭合

- 严重性：`Must Fix`
- 决策类：`Agent-Fixable`
- 状态：`Closed`
- 置信度：高
- 修复证据：
  - `src/camera_based_rgbww_optimizer/optimization/p7_td_b_r6_stage_gate.py:97-133` 保留 13 个 canonical authority keys，并独立列出冻结的 20 个 legacy/global aliases。
  - `_projection()` 在 `:519-524` 同时要求 13 个 canonical 值均为 exact `False`、所有 top-level `*_authorized` key 的集合精确等于 canonical vocabulary，并拒绝每个冻结 alias 的存在。因此 missing canonical、canonical true/non-false、未知 `*_authorized` 和即使值为 false 的 legacy alias 都以 `machine_contract_drift` fail closed。
  - `tests/test_p7_td_b_r6_stage_gate.py:959-1031` 使用测试内字面量 canonical/forbidden tuples；oracle 没有从 `_FULL_AUTHORITY_FIELDS` 派生。用例覆盖全部冻结 aliases、独立 unknown sentinel `future_unlisted_authorized` 和 13 个 canonical true mutation，并断言 package root 不存在且 `create_exclusive_root()` 未被调用。
- 反证尝试：检查了字段后缀、`device_authorized_by_this_file` 一类不以 `_authorized` 结尾的 aliases、nested `replacement_package_task.formal_authorized` 及 arbitrary extra-key parser 行为。前两类由 suffix closure 与 forbidden literals 组合覆盖；nested task state 仍由 `_offline_package_evidence_full_state()` exact equality 闭合。未发现能满足冻结 authority contract 且绕过 pre-root gate 的 top-level authority key。
- 关闭理由：冻结的生产 literal universe、unknown sentinel 和独立测试 oracle 均有直接代码证据，且未新增 fallback spelling、schema、owner 或并行 policy module。
- Reopen trigger：canonical/forbidden vocabulary、FULL parser key semantics、`_projection()` ordering 或 replacement task state shape 后续发生变化。

### REV-S2-PROV-001 — accepted-engineering prerequisite 未与 validated source attestation 交叉绑定

- 严重性：`Must Fix`
- 决策类：`Agent-Fixable`
- 状态：`Closed`
- 置信度：高
- 修复证据：
  - `_validate_prerequisite_projection()` 在 `src/camera_based_rgbww_optimizer/optimization/p7_td_b_r6_stage_gate.py:557-583` 保留 closed shape、SHA-40 形状和 authority/task state 验证，并返回已验证 projection。
  - `validate_stage_gate()` 在 `:1203-1241` 先完成 source-reference、`_source_attestation_binding()`、`_validate_preparation_source_attestation()` 的既有严格 Git/source 验证，再把 prerequisite 的 checkpoint/tree 与同一 normalized binding 做 exact equality；任一不一致稳定返回 `prerequisite_projection_drift`。
  - `tests/test_p7_td_b_r6_stage_gate.py:1033-1090` 分别把 checkpoint/tree 换成另一合法 SHA-40，重写 stage-gate/descriptor 并刷新 terminal references，使 `descriptor_reference_drift` 不会遮蔽专用 guard；production loader 在 backend factory/delegate 前拒绝，两个 mock 均未调用。
  - 正向路径先执行 generate -> validate -> persist -> replay，并确认 replay `status == "pass"`，随后才逐项构造 cross-binding mutation。
- 反证尝试：沿 `validate_stage_gate -> _load_stage_gate_package -> load_and_validate_stage_gate_package -> run_production_cli_launch` 检查错误顺序，并沿 `_source_attestation_binding -> _validate_preparation_source_attestation -> validate_committed_source_attestation` 检查绑定来源。没有发现使用另一 provenance owner、重复 Git validator、descriptor/reference precedence 放宽或仅做 format acceptance 的旁路。
- 关闭理由：原始 40 位合法但与 attestation 不同的 checkpoint/tree 触发已在唯一 validator owner 被 exact-bound，且回归用例到达同一 production load seam、证明 downstream backend/delegate effect 为零。
- Reopen trigger：stage-gate prerequisite 或 source-attestation binding shape、package replay ordering、descriptor construction 或 production loader dispatch 顺序后续改变。

## 审查范围与仓库现实

- Repository：`/Users/ibobby/Projects/WLED-RGBWW`
- Range：`110730db28d90513928c9b28bc4c49d75eee0c14..75d327729fdc479b6f9305e4e4a5ca3628fe2346`
- Patch SHA-256：`91c00011896792cda1bf2ca0658fccdff3037777a7a83618b15cd9a68042767e`
- Review depth：`Large`，因为变更位于 provenance/authority/formal dispatch 前置 trust boundary。
- 拓扑：repair head 是 activation commit `110730d` 的直接单父、非 merge child；activation commit 又是 Section 2 base code commit `7d02562d` 的直接子提交。repair subject 精确为 `fix(stage-gate): close section 2 review findings`。
- Exact changed paths：
  - `src/camera_based_rgbww_optimizer/optimization/p7_td_b_r6_stage_gate.py`
  - `tests/test_p7_td_b_r6_stage_gate.py`
- Head tree：`342e8c0b4f4444447a635132b0dfe333ef1ca483`。
- Current source/test identity：
  - source SHA-256/blob：`97b0a88c338b659ca887dfb626eee11ff96f52712b16a2d6f8b8b7de059298b7` / `0015d7ce2f2a5dde9118478f98c929020a474a01`
  - test SHA-256/blob：`f86c8dd121b549cf33f8e537454091859e60a466ebed70ff1f077b30defe5add` / `2a60a987dda02675c2eddc7d8260d61a8f68edc3`
- 审查时 HEAD 即 repair head，source/test 在 worktree 与 index 相对 HEAD 均无漂移。工作树另有 Orchestrator/Planner 的 `.agent-work/` 修改和未跟踪 archive；它们不属于本 range，本轮未修改、清理或纳入 mergeability 判断。

## 意图与不变量

变更意图：在既有 stage-gate owner 内关闭 Section 2 已接受的 authority vocabulary 与 accepted-engineering provenance cross-binding 两个 finding，不改变 task、schema、package/replay/formal owner 或任何执行授权。

本轮使用的不变量：

1. unfinished FULL projection 只能出现冻结的 13 个 canonical top-level authority keys，且全部 exact false；冻结 legacy/global aliases 和未知 `*_authorized` key 的存在本身即为 drift。
2. stage-gate prerequisite 声明的 accepted-engineering checkpoint/tree 必须与已经过严格 Git/source validation 的唯一 source-attestation binding 完全相同。
3. 两类 drift 都必须在 package-root 创建或 backend/formal/device dispatch 前失败。
4. descriptor/reference precedence、Section 1 Git topology/blob verification、artifact inventory、terminal seal、persistence/replay 和 future runtime/formal owner 不得弱化。

## Repair delta 与失效影响锥

1. `PLAN/FULL bytes -> strict machine-row parser -> _projection -> build_stage_gate_input -> prepare CLI -> create_exclusive_root`：重新验证 canonical key completeness、false semantics、unknown suffix、frozen aliases、nested replacement task exact shape 和 pre-root ordering。
2. `stage-gate.json -> validate_stage_gate -> public replay/load -> run_production_cli_launch -> backend/delegate`：重新验证 prerequisite shape、validated binding exact equality、artifact/reference-consistent mutation 和 pre-backend rejection。
3. `source_attestation_binding -> _validate_preparation_source_attestation -> validate_committed_source_attestation`：确认 repair 复用既有 single provenance owner，未改变 commit/tree/direct-parent/subject/path/blob/ancestry 验证。
4. `build_launch_descriptor -> validate_launch_descriptor -> validate_future_activation`：确认 repair 未把 prerequisites 复制成第二 owner，也未改变 secret/historical guard precedence、descriptor authority 或 future activation semantics。

没有 reset 事件。修复只收紧既有 authority/provenance gate，没有改变 public schema、task/state owner、auth direction、持久化结构、并发、破坏性行为或部署语义，也未扩出两个冻结 finding 的边界。

## 覆盖矩阵

| 风险镜头 | 状态 | 覆盖证据 |
| --- | --- | --- |
| Intent/domain semantics | Reviewed | raw diff、冻结 Section 2 PLAN/FULL contract、task/owner/non-goal 对照 |
| Local correctness | Reviewed | exact key-set predicates、false identity、checkpoint/tree 两个独立 mutation、错误码与顺序 |
| Data/provenance | Reviewed | prerequisite、source binding、Git attestation、artifact references、terminal replay 影响锥 |
| State/concurrency | Skipped | repair 未改变 async、锁、重试、计数或并发状态机 |
| Security/authority | Reviewed | canonical/legacy/unknown authority vocabulary 与 pre-effect fail closed |
| Reliability/release | Partial | 静态追到 production load/backend dispatch；按禁区未访问 package/formal surface |
| Performance/cost | Skipped | 无新无界循环、I/O fan-out、网络或模型调用 |
| Architecture/maintainability | Reviewed | 保持 existing source/test owner；未新增 module/schema/controller/adapter/task/root |
| Dependencies/supply chain | Skipped | 无 manifest、lockfile、CI 或 dependency 变更 |
| Tests/validation integrity | Reviewed | 两个 regression oracle 会在 base 行为上失败；authority oracle 不从 production constant 派生 |
| UI/accessibility | Skipped | 无 UI/交互变更 |
| AI-agent/review risks | Reviewed | 先冻结 raw Git/diff/identity，再检查 prior reports/ER claims；未以 repair/Planner 自述代替代码 closure |

## 验证

### 本轮独立运行

| 命令/流程 | 结果 | 限制 |
| --- | --- | --- |
| `git status --short --branch`、`git rev-parse`、`git rev-list --parents`、`git show`、`git diff-tree` | PASS | 冻结 base/head、直接父、subject、tree、两路径及 worktree source/test 无漂移 |
| `git diff --check 75d3277^ 75d3277` | PASS | 仅检查 patch whitespace/conflict marker |
| patch、source、test SHA-256 与 Git blob identity | PASS | 与当前 reviewed execution record 的 candidate identities 一致 |
| `git merge-base --is-ancestor 5d01bc... 75d3277` | PASS | accepted Section 1 位于 repair head 祖先链 |
| CodeGraph owner/caller/impact-cone queries | PASS | 确认 `validate_stage_gate` 的 replay/runtime callers 与 `_projection` prepare boundary |
| 对 head source/test 执行 Python AST parse（`-P -B`） | PASS | 语法/AST 级，不替代 unittest |
| raw source/test 的 adversarial static trace | PASS | 覆盖两个冻结触发、正向生成路径和 downstream effect ordering |

### 未独立运行或未访问

| 检查/证据 | 原因 | 剩余风险 |
| --- | --- | --- |
| 两个新增 unittest、affected/stage-gate/terminal suites | 本轮明确禁止 package/formal access；cross-binding regression 会构建 synthetic sealed package，因此未执行 | 测试代码和 production path 已静态核验，但本 reviewer 没有独立运行时退出码 |
| full unittest collection | 本轮不重复长时 collection，且现有执行记录明确为 qualified non-green | 未独立重现 `981` tests / `2 failures + 8 errors` |
| execution log/seal、package artifacts、formal roots | 明确禁区；未读取 `/Volumes/...` 日志、seal、package 或 formal payload | 执行记录的精确测试计数、错误归因和零外部 effect 是未独立验证 claim |
| device/network/camera/Ray/strip/capture/runtime | 明确禁区且本 repair 不要求 | 无真实外设或正式执行结论 |

当前 `.agent-work/EXECUTION_RESULT.md` 及其 reviewed archive 声明：targeted/affected/stage-gate/terminal/compile/CodeGraph checks 通过；新 valid full collection 运行 981 个测试，仍有与先前相同的 governance-lineage group `2 failures + 8 errors`，且没有 repair/stage-gate/terminal 新失败。候选 source/test SHA 与本轮独立计算一致，但上述运行结果和日志内容未由本 reviewer 重新执行或访问，因此不得写成 full green 或独立 runtime proof。

## 收敛、残余风险与维护性判断

- 本轮模式：`DELTA` repair review，范围为 repair delta 加 authority/provenance 失效影响锥。
- 关闭：`REV-S2-AUTH-001`、`REV-S2-PROV-001`。
- Reopened：0。
- 新 root cause：0。
- Reset：0。
- 当前 repair round：clean review round 1；后续 clean-streak/阶段推进由 Orchestrator 按版本化计划处理。
- 最大残余风险是 full suite 并非 green，且本 reviewer 受禁区约束未独立运行新增 tests、未读取 full log/seal。该风险已被限定为既有 governance-lineage 非绿 claim，不能泛化为全仓 green 或正式执行 readiness。
- 维护性判断：变更留在单一 stage-gate validation owner，新增一个小型 literal vocabulary 和一个局部 exact cross-binding；没有新增模块、schema、controller 或状态 owner。回归覆盖直接对应两个 root causes，本 Section 2 repair 不建议额外清理。
- 停止条件：对该 repair delta 满足；无 unresolved `Must Fix`/`Should Fix`，所有触发镜头已 reviewed 或明确列出 evidence gap。
