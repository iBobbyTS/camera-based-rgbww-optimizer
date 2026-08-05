# G4-R6 Section 2 修复独立代码审查（Round 2）

## Findings

### REV-S2-REPAIR-R2-001 — repair commit 的真实 subject/字节无法满足唯一 code-owner attestation

- 严重性：`Must Fix`
- 决策类：`Agent-Fixable`
- 状态：`Open`
- 置信度：高
- 位置：
  `src/camera_based_rgbww_optimizer/optimization/p7_td_b_r6_stage_gate.py:78-85`、
  `:335-386`、`:1574-1605`、`:1606-1635`

#### 触发条件与证明路径

1. 当前 repair head `75d327729fdc479b6f9305e4e4a5ca3628fe2346`
   是 activation commit `110730db28d90513928c9b28bc4c49d75eee0c14`
   的直接单父提交，subject 为
   `fix(stage-gate): close section 2 review findings`，并修改了恰好两个
   attested code-owner 路径。
2. repair delta 没有更新 `ALLOWED_CODE_CHILD_SUBJECT`；head source 仍只允许
   `fix(stage-gate): align replacement package owner`，即旧 base code commit
   `7d02562db0afcffaa8f2a341345235a6310b654c` 的 subject。
3. `_source_attestation_binding()` 要求 package binding 的
   `code_child_subject` 精确等于该旧常量；
   `validate_committed_source_attestation()` 随后又要求绑定的实际 code-owner
   commit subject 与该值完全一致，并校验该 commit 的两个 blob 与当前
   source references/current files 一致。
4. 本轮只读真实 Git probe 将 repair head `75d3277` 绑定为 code owner，其他
   parent/tree/path/blob/accepted-engineering 字段全部取真实仓库值，稳定得到
   `committed_source_subject_drift`。
5. 同一 probe 改回旧 owner `7d02562`，但保留 repair head 的当前 source/test
   references，稳定得到 `committed_source_candidate_blob_drift`。而且
   `7d02562..75d3277` 还包含修改 source/test 的 repair descendant，不满足
   post-child `.agent-work/`-only 约束。
6. `FINAL_CODE_SNAPSHOT_SUBJECT` 虽存在于 `:79-81`，当前没有任何 production
   caller 或 alternate accepted-subject branch，不能为 repair head 提供可达的
   attestation 路径。

#### 影响

- 若 Section 2 在 `75d3277` 关闭并直接进入后续 single package-preparation
  PLAN，现有 owner 无法为修复后的 source/test 字节构造可通过验证的
  source-attestation binding。
- 把 repair head 当新 owner 会因 subject 不符失败；继续使用旧 owner 会因
  candidate blob/current bytes 与 repair 结果不符失败。也就是说，本次修复虽然
  关闭了 authority/provenance 两个局部 finding，却使 Section 2 的另一核心交付
  ——“最终两路径字节由唯一 direct code-owner child 证明”——没有可用身份。
- 该失败发生在 root/backend/device effect 之前，安全上仍然 fail closed；但会让
  已接受的 offline package owner 无法继续其唯一后续用途，因此阻塞 Section 2
  合并/接受。

#### 最小修复方向

- 让下一次最终、受复审的两路径 repair/snapshot commit 自身成为唯一 code owner：
  其实际 subject 必须与 `ALLOWED_CODE_CHILD_SUBJECT` 完全一致，并由后续 package
  PLAN 记录该 commit、tree、direct parent 和两个 blob。可以复用当前未被使用的
  `FINAL_CODE_SNAPSHOT_SUBJECT`，但 production 只能保留一个明确、可达的 accepted
  subject 规则，不能增加模糊 fallback。
- 在现有 synthetic Git owner 中增加持久回归：正例使用最终 repair/snapshot
  subject 与最终字节通过；负例证明旧 subject/旧 blob 不能代表修复后字节。另加
  一个仓库候选身份检查，避免 synthetic fixture 只引用 production constant 而再次
  遗漏“真实 commit subject 与常量不同”。
- 不需要新 module、schema、controller、package owner 或 device/formal 路径。

#### 冻结验收条件

- [ ] 最终 code-owner commit 是 activation parent 的直接非 merge child，实际
      subject 精确等于 production accepted subject，changed paths 精确为两个既定
      source/test 路径。
- [ ] 最终 commit 的 tree/blob 与当前修复后 source references 完全一致；真实 Git
      attestation 正例不再返回 `committed_source_subject_drift` 或
      `committed_source_candidate_blob_drift`。
- [ ] 旧 `7d02562` 不能被用来证明修复后的 source/test 字节。
- [ ] `REV-S2-AUTH-001`、`REV-S2-PROV-001` 的 guard、错误码、pre-effect 顺序和
      独立负向 oracle 均保持不变。
- [ ] 修复与验证仍不访问 package/formal/device/network surface。

## 合并结论

`not mergeable`

`REV-S2-AUTH-001` 与 `REV-S2-PROV-001` 已关闭，但新发现的
`REV-S2-REPAIR-R2-001` 使 repair head 没有可通过现有唯一 attestation owner 的
commit identity。Section 2 clean-review streak 不能递增；在该 finding 修复并经
独立 delta review 关闭前，不应接受/合并本 repair commit。

该结论只覆盖 `75d3277^..75d3277` 的 repair delta 及其失效影响锥，不授权
package prepare/describe、formal R6、root 创建、设备、网络、相机、Ray、strip、
capture、release consumption、G4-07 或 TD-C。

## 已关闭的 accepted finding

### REV-S2-AUTH-001 — unfinished FULL projection authority vocabulary 未闭合

- 状态：`Closed`
- 代码证据：`_projection()` 现在同时要求 13 个 canonical authority keys 全部为
  exact `False`、所有 top-level `*_authorized` keys 的集合精确等于 canonical
  vocabulary，并拒绝 20 个冻结 legacy/global aliases 的出现。
- 独立 oracle：本轮未从 production tuple 派生测试输入；使用字面量全集完成
  34 个内存负例（20 个 aliases、1 个未知 `future_unlisted_authorized`、13 个
  canonical true），均以 `machine_contract_drift` 失败；canonical 正例通过。
- 测试完整性：新增 repository test 同样使用测试内字面量 tuples，并断言
  `create_exclusive_root()` 未调用，不再存在原先 production-derived oracle 盲点。

### REV-S2-PROV-001 — accepted-engineering prerequisite 未与 validated source attestation 交叉绑定

- 状态：`Closed`
- 代码证据：`validate_stage_gate()` 先沿既有唯一 owner 完成 source references、
  normalized binding 与真实 Git attestation 验证，再将 prerequisite 的
  `accepted_engineering_checkpoint/tree` 与同一 binding 做 exact equality；任一漂移
  返回 `prerequisite_projection_drift`。
- 独立 oracle：本轮用无文件/package I/O 的内存 probe 验证同一身份正例通过，合法
  SHA-40 checkpoint-only 与 tree-only 漂移各自以目标错误码失败。
- 影响锥：`replay_stage_gate_package()`、
  `load_and_validate_stage_gate_package()` 与 production CLI loader 均复用
  `validate_stage_gate()`，没有平行 provenance owner 或 descriptor precedence 放宽。

## 审查范围与仓库现实

- Repository：`/Users/ibobby/Projects/WLED-RGBWW`
- Range：
  `110730db28d90513928c9b28bc4c49d75eee0c14..75d327729fdc479b6f9305e4e4a5ca3628fe2346`
- Patch SHA-256：
  `91c00011896792cda1bf2ca0658fccdff3037777a7a83618b15cd9a68042767e`
- Head tree：`342e8c0b4f4444447a635132b0dfe333ef1ca483`
- Exact changed paths：
  - `src/camera_based_rgbww_optimizer/optimization/p7_td_b_r6_stage_gate.py`
  - `tests/test_p7_td_b_r6_stage_gate.py`
- Review depth：`Large / DELTA`，因为 repair 位于 authority、provenance、package
  replay 与 future formal dispatch 前置 trust boundary。
- 审查时 `HEAD` 即 repair head，source/test 相对 HEAD 无 worktree/index 漂移。
  工作树另有 Planner/Orchestrator 的 `.agent-work/` 修改与 archive；它们不属于
  range，本轮未修改、清理或纳入代码结论。

## 意图、不变量与 repair impact cone

变更意图：只在现有 stage-gate/test owner 中关闭冻结的 authority vocabulary 与
accepted-engineering cross-binding finding，不改变 schema、task、artifact、package/
formal owner 或执行权限。

本轮使用的不变量：

1. 当前 FULL projection 的 canonical authority vocabulary 必须闭合且全为 false。
2. stage-gate prerequisite 的 accepted-engineering identity 必须与已验证的唯一
   source-attestation identity 完全一致。
3. 修复后的最终 source/test 字节仍必须由一个 actual subject/path/blob 均匹配的
   direct non-merge code-owner commit 证明；普通 repair commit 不能悬空在该拓扑外。
4. 所有 drift 必须在 root/backend/formal/device effect 前失败；descriptor-reference
   precedence、Section 1 engineering validation、artifact inventory、terminal seal、
   persistence/replay 与 runtime owner 不得弱化。

检查的失效影响锥：

- `FULL machine row -> _projection -> build_stage_gate_input -> prepare/root boundary`；
- `stage-gate prerequisite -> validate_stage_gate -> replay/production loader`；
- `source_attestation_binding -> committed Git subject/path/blob/lineage -> current repaired bytes`；
- 新 regression oracle、synthetic fixture 与真实 repair commit metadata 的一致性。

没有触发 full reset：public schema/API、state owner、persistence、formal dispatch、权限
方向和架构均未改变；本轮新增 finding 位于 repair 已经失效的 child-topology cone 内。

## 覆盖矩阵

| 风险镜头 | 状态 | 覆盖证据 |
| --- | --- | --- |
| Intent/domain semantics | Reviewed | raw repair diff、commit metadata、冻结 Section 2 PLAN/FULL 合同 |
| Local correctness | Reviewed | exact key closure、cross-binding、real subject/blob topology 两种候选路径 |
| Data/provenance | Reviewed | prerequisite、source binding、Git commit/tree/parent/subject/path/blob、replay caller |
| State/concurrency | Skipped | 未改变 async、锁、重试或并发状态机 |
| Security/authority | Reviewed | canonical/legacy/unknown vocabulary 与 pre-effect fail closed |
| Reliability/release | Partial | 静态/只读 Git 追踪到 production loader；未访问 package/formal surface |
| Performance/cost | Skipped | 无新增无界循环、网络、模型或大数据路径 |
| Architecture/maintainability | Reviewed | 仍是单一 stage-gate owner；发现的 defect 是现有 owner identity 不闭合 |
| Dependencies/supply chain | Skipped | 无 manifest、lockfile、CI 或 dependency 变更 |
| Tests/validation integrity | Reviewed | 两项 accepted finding 的独立 literal/in-memory oracle；识别 synthetic subject 自证盲点 |
| UI/accessibility | Skipped | 不涉及 UI |
| AI-agent/review risks | Reviewed | 先从 raw diff/Git/调用链独立推导，再核对 frozen finding 与前轮报告 |

## 验证

### 本轮独立运行

| 命令/流程 | 结果 | 限制 |
| --- | --- | --- |
| `git status` / `rev-parse` / `show` / `diff-tree` / patch fingerprint | PASS | 冻结 base/head/parent/subject/tree/two paths；worktree 有范围外 `.agent-work/` 改动 |
| `git diff --check 75d3277^ 75d3277` | PASS | 仅 whitespace/conflict-marker 检查 |
| CodeGraph owner/caller/impact 查询 | PASS | 确认 `_projection`、`validate_stage_gate`、replay/loader 与 committed-source attestation 影响锥 |
| source/test AST parse（`.venv/bin/python -P -B`） | PASS（2 files） | 语法/AST 级，不替代 unittest |
| 无 I/O authority/provenance adversarial probe | PASS：1 个 authority 正例、34 个 authority 负例、1 个 cross-binding 正例、2 个 cross-binding 负例 | 未构造或读取 package/formal artifact |
| 当前仓库真实 Git attestation probe | FAIL AS DESIGNED FOR REVIEW：repair head owner -> `committed_source_subject_drift`；旧 owner + repaired bytes -> `committed_source_candidate_blob_drift` | 只读 Git/source；无 package/formal/device/network |

### 未独立运行或未访问

| 检查/证据 | 原因 | 剩余风险 |
| --- | --- | --- |
| 两个新增 repository unittest、focused/terminal/full suites | cross-binding test 会构建 synthetic sealed package；本轮明确禁止 package/formal access | 测试代码已静态核验，accepted finding closure 另有无 I/O probe；未取得本 reviewer 的 unittest 退出码 |
| 执行 log/seal、package artifacts、formal roots | 明确禁区，未读取 `/Volumes/...` 对应 payload | 当前执行记录的精确计数/错误归因仍是未独立复核 claim |
| device/network/camera/Ray/strip/capture/runtime | 明确禁区且本 repair 不要求 | 无外设或正式执行结论 |

当前 `.agent-work/EXECUTION_RESULT.md` 声明 targeted/affected/stage-gate/terminal/
compile/CodeGraph checks 通过，并记录 `981` tests、既有 governance-lineage group
`2 failures + 8 errors`；本轮未执行或读取其外部 log/seal，因此不得把该声明写成
full green 或独立 runtime proof。无论该 claim 是否准确，都不能反证当前由 commit
metadata 与 production validator 直接复现的 owner-subject/blob 不闭合。

## 收敛、残余风险与维护性判断

- 本轮模式：`DELTA` repair review。
- Closed：`REV-S2-AUTH-001`、`REV-S2-PROV-001`。
- New root cause：`REV-S2-REPAIR-R2-001`。
- Reopened：0；Reset：0。
- 当前 clean review round 不是 clean；停止条件不满足。
- 最大额外证据缺口是 full suite 并非 green且未由本 reviewer 重跑；这不改变当前
  deterministic Git-attestation finding。
- 维护性判断：两个原 repair 都留在既有单一 validation owner，复杂度增量小且
  regression oracle 有意义；新 finding 也应在同一 subject/topology owner 中做最小
  修复，不建议新增兼容分支或第二 attestation abstraction。
