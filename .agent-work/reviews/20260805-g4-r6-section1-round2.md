# G4 R6 Section 1 独立代码审查（Round 2）

## Findings

未发现可操作 finding。没有未解决的 `Must Fix`、`Should Fix`、`Needs Decision` 或 `External Blocker`。

## Mergeability

**`mergeable`** —— commit `5d01bcbb7e1a9ec1808e2fc05d238363d82a0a74` 在本次 Section 1 边界内可合并。本结论不解锁 Section 2，也不授权 package prepare/describe、formal、device、network、camera、Ray、strip、capture 或 release-consumption 操作。

## Review boundary

- Repository: `/Users/ibobby/Projects/WLED-RGBWW`
- Base: `6a5e2836b802940c3b58803a7a88b565b6050d37`
- Head: `5d01bcbb7e1a9ec1808e2fc05d238363d82a0a74`
- Exact range: `5d01bcb^..5d01bcb`
- Review depth: `Large`，因为变更位于正式执行前的 provenance/stage-gate 高影响边界。
- Changed paths only:
  - `src/camera_based_rgbww_optimizer/optimization/p7_td_b_r6_stage_gate.py` (`96+ / 1-`)
  - `tests/test_p7_td_b_r6_stage_gate.py` (`214+ / 0-`)
- Total changed lines: `311` additions/deletions；符合计划的 `300–320` 目标范围和 `330` hard cap。
- Head blobs:
  - source: `76c8821c915c58e7ad5cdb0133bf2940b51fd1f4`
  - test: `9b8f5781f175bae1fc93cd398b8bf362c0da20e2`
- Source SHA-256: `2dd469827fff3d6137e247b179035a685b42627aea207b18898a05d36fe18c11`，与冻结的 Section 1 production source identity 一致。
- 工作树中的 PLAN、EXECUTION_RESULT、debug/archive/review 状态均视为本 commit 审查范围外；本轮未修改、清理、暂存或回退这些状态。

## Intent and invariants

变更意图：在现有 stage-gate owner 内增加 accepted-engineering prerequisite 的闭合 binding、descriptor 投影和只读 Git 验证，并为 ancestry `subprocess.run` 的 `OSError` 提供稳定 fail-closed 错误码。

使用的关键不变量：

- production owner 与 test owner 不变，不新增 schema family、runner、controller、artifact/persistence owner 或旁路。
- accepted-engineering binding 必须闭合，并验证 commit/tree/direct parent/subject/exact changed paths/blob OIDs，以及到 verified alignment parent 的 ancestry。
- descriptor 只投影同一 binding；binding/descriptor/Git 任一漂移必须 fail closed。
- ancestry 查询的 `OSError` 和异常 return code 必须稳定映射到 `committed_source_engineering_ancestry_query_failed`；合法的 nonancestor 必须映射到 `committed_source_engineering_lineage_drift`。
- 失败发生在 output root、backend、delegate、设备或网络副作用之前。
- Planner/FULL machine contract 继续负责提供闭合 checkpoint/tree/parent/blob identity；本 section 按计划只在模块中固化 accepted subject/path constants。

## Coverage and critical paths

Reviewed lenses:

- Intent/domain semantics: 对照 commit parent 中的 `PLAN.md` 与 `PLAN-FULL.md` 重建 Section 1 契约及 Section 2 hard lock。
- Provenance/data integrity: closed shape、descriptor equality、tree/parent/subject/path/blob identity、当前 source reference、dirty-worktree scope。
- State/lineage: engineering checkpoint ancestry、code-owner direct child、post-child linear `.agent-work/` lineage、merge/nonancestor/alternate commit negatives。
- Reliability/error semantics: Git query failures、raised `OSError`、returncode `2`、stable error code、pre-root/pre-backend ordering。
- Security/trust: secret/historical semantic guard precedence、source substitution、same-path regeneration、symlink/path/mode checks。
- Architecture/maintainability: 复用既有 stage-gate owner、thermal changed-path owner 和现有 synthetic Git fixture；没有平行实现或新公共 owner。
- Tests/AI-agent risks: 检查 visible-test overfit、同步弱化断言、mock-only 假阳性、未授权 scope expansion；新增矩阵覆盖真实 synthetic Git，而非仅检查调用次数。

Critical path traced end to end:

`PLAN/FULL machine state -> source_attestation_binding -> build_stage_gate_input -> launch descriptor -> validate_committed_source_attestation -> future activation / production CLI delegation`

新增 prerequisite 校验位于任何 artifact root、backend factory、delegate、设备或网络动作之前。

## Checks run

- `git diff --check 5d01bcb^..5d01bcb` — pass。
- `git diff --numstat` / `--name-only` / blob and SHA identity checks — pass；exactly two implementation paths。
- CodeGraph impact query for `_source_attestation_binding`, `_committed_source_contract`, `_validate_descriptor_attestation_contract`, `validate_committed_source_attestation` and callers — reviewed。
- Exact new affected tests: `4/4` pass in `13.394s`：positive binding/descriptor/Git identity、closed-shape matrix、Git failure matrix、durable ancestry `OSError` regression。
- Focused file contains `51` test methods。One-shot file invocation was externally terminated by the tool limit with exit `143` after `29` observed passes and no assertion failure; the incomplete suffix was rerun deterministically in two groups: `9/9` pass (`52.655s`) and `13/13` pass (`31.592s`). Across the prefix and completion groups, all `51/51` methods were observed passing.
- Existing returncode-2、nonancestor、descriptor precedence、worktree scope、package substitution、production pre-backend、single-delegate and no-connect cases remained green。

## Checks not run and residual risk

- 按审查边界未运行 repository-wide discovery、package prepare/describe、formal execution、设备、网络、camera、Ray、strip、capture 或 release 操作。
- 未对真实未来 package/root/hardware 做运行时验证；本结论限于本 commit 的离线 Section 1 provenance gate 与 synthetic Git/mocked downstream seams。
- 当前工作树不干净，但其改动全部位于本 commit range 外；因此不影响对已冻结 commit 的代码结论，后续编排仍需自行维持其 PLAN/FULL/EXECUTION 状态一致性。

## Repair/reset record

- Repair authorized: no。
- Repairs made: none。
- Reset trigger: none；base/head 在审查期间保持稳定。
- Final decision: **`mergeable`**。
