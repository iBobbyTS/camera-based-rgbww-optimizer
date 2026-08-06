# EXECUTION_RESULT

## REF-G4-06 source-attestation v2 engineering

**Contract:** `G4-R6-SOURCE-ATTESTATION-V2-ENGINEERING-V1`

**Status:** `FINAL_FULL_NON_GREEN_RETURN_FOR_PLANNER_TERMINAL_REVIEW`

**Planner stop:** `RETURN_FOR_G4_06_SOURCE_ATTESTATION_V2_ENGINEERING_REVIEW`

### Intake 与范围

- Activation HEAD：`f23f74a6fe1bee6a04131e75ef8969e8f4d0b3af`；parent `641482706e5efebc81f1f55dba284cffd58b8355`；subject `docs(plan): activate source attestation v2 engineering`；exact activation paths 为 PLAN 冻结的四个 `.agent-work/` 文件。
- Accepted start blobs：source `0015d7ce2f2a5dde9118478f98c929020a474a01`；test `2a60a987dda02675c2eddc7d8260d61a8f68edc3`。
- Historical Q1 ref仅执行 `show-ref` 与 ancestry isolation：ref存在、evidence commit `b5839d38ffa0c27bd5a6232a890cca3af0b8e7d9` 不在 live HEAD ancestry；未读取其diff/tree/blob/file，未merge/cherry-pick/rebase/copy。
- Production/test changed paths exact：
  - `src/camera_based_rgbww_optimizer/optimization/p7_td_b_r6_stage_gate.py`
  - `tests/test_p7_td_b_r6_stage_gate.py`
- 未修改 PLAN/FULL/PLAN-FULL/archive/debug/GUIDE/RESEARCH/config/wrapper；未commit。

### 实现与所有权

- 在既有 `p7_td_b_r6_stage_gate.py` owner内增加单一v2 seam：candidate qualification只验证closed provenance与冻结source/test bytes，不查询Git、不预测未出生commit、不构造package；post-accept commit attestation只读核验exact tree/direct-parent/subject/path/blob/current bytes/worktree scope。
- 既有 `validate_committed_source_attestation` 成功路径delegate到同一 `attest_qualified_source_commit` owner；旧descriptor和future activation错误码/后续lineage仍保留。
- 未新增module/controller/runner/parallel authority；future package descriptor继续锁定。
- 最终candidate实际changed lines：source 177 + test 122 = **299**，满足PLAN hard cap `<300`。

### Candidate freeze

以下身份于focused后冻结；自冻结后source/test无写入：

- source：mode `0644`；bytes `109143`；SHA-256 `00650231ff64645716212cb8c185d7e5bd5942d110109ca6b3fb9c4d47405c78`
- test：mode `0644`；bytes `161053`；SHA-256 `6354c74e357117e0b91fa68403dbe2ea5d30d162275a6894cc61e24894431719`

### 验证 ledger

1. Targeted v2 regressions：3 tests，exit `0`，`OK`，2.415s。
2. Stage-gate focused最终唯一有效run：
   - command：`.venv/bin/python -m unittest tests.test_p7_td_b_r6_stage_gate`
   - evidence：`/Volumes/4T/temp/rgbww-optimizer/g4-v2-focused-stage-gate-f23f74a`
   - 56 tests，exit `0`，`OK`，562.852s。
3. Harness/tool-yield bounded correction（全局保留，不删除账）：统一exec yield使前两次相同focused命令继续运行却错误呈现completed；重复PID `9064`（`-v`）和 `14704`（non-verbose）被Executer发现后发送SIGTERM，未作为验证结果；保留唯一PID `24415`完成上述56/56。Orchestrator已接受其为本包唯一harness/tool-yield correction；不是production owner failure。
4. Related focused：`.venv/bin/python -m unittest tests.test_p7_thermal_diagnostics tests.test_p7_td_b_r6_terminal`；evidence `/Volumes/4T/temp/rgbww-optimizer/g4-v2-focused-related-f23f74a`；95 tests，exit `1`，2 failures + 8 errors，27.756s。全部为live `AGENTS.md` governance-lineage/path identity既有漂移，未出现stage-gate/terminal/new owner failure；Executer不宣称可接受，交Planner独立裁决。
5. `compileall -q src tests` exit `0`；`git diff --check` exit `0`；exact scope pass；forbidden historical/package/formal literal scan pass。
6. `codegraph sync`：already up to date；query确认candidate qualification、post-accept commit attestation与legacy delegate位于同一owner，v2 seam没有package/backend effect。
7. Final full suite：invocation `1/1`，retry `0/0`，已在可见macOS Terminal完成：
   - command：`.venv/bin/python -m unittest discover -s tests`
   - token/root：`g4-r6-source-attestation-v2-full-f23f74a-20260805T234530Z` / `/Volumes/4T/temp/rgbww-optimizer/g4-r6-source-attestation-v2-full-f23f74a-20260805T234530Z`
   - wrapper：2195 bytes；mode `0700`；SHA-256 `7d8c906f51519ef25234373b2a8c7cc6dbc76293d5cae8a9c697edc5c99275ee`
   - PID `95333`；TTY `/dev/ttys014`；started `2026-08-05T23:46:04Z`；finished `2026-08-05T23:50:57Z`
   - liveness checks 3/3：约13s、33s、79s均存活；完成后automation已由Orchestrator删除。
   - 984 tests；293.094s；exit `1`；5 failures + 220 errors；full retry `0`。
   - terminal seal：478 bytes；SHA-256 `43c9760900449c0de24c15b2f93415e51e34453ae0524398389e5dfabd66bce5`。
   - stdout：4327 bytes；SHA-256 `fcdd529c8f730c74a7193339c7919327ce384c4354788967cc40120ea0ac77c2`。
   - stderr：491176 bytes；SHA-256 `d1686c3b20baea5fb91a1bd0cec472144817a2b79e2fa3112a369b0fd3aa7318`。
   - `validation.exit`：2 bytes；SHA-256 `4355a46b19d348dc2f57c046f8ef63d4538ebb936000f3c9ee954a27460dd865`；value `1`。
   - wrapper在full前再次核验frozen source/test SHA `00650231ff64645716212cb8c185d7e5bd5942d110109ca6b3fb9c4d47405c78` / `6354c74e357117e0b91fa68403dbe2ea5d30d162275a6894cc61e24894431719`；candidate freeze后没有source/test mutation。

### Final full failure classification

- Candidate-owned failure：`test_source_attestation_v2_candidate_guards_are_reachable_and_prioritized` 的digest subcase要求 `source_qualification_digest_drift`，实际先得到 `source_reference_drift`。这是候选自身的guard/error-priority不一致，超出允许baseline，必须fail closed。
- 约220个stage-gate errors主要在 `SyntheticGitRepository` 初始化中以stable `committed_source_candidate_blob_drift` 失败。此前同一最终candidate的stage-gate focused为56/56；因此这是full-order/integration mass regression，同样超出允许baseline且不可接受。
- 其余failures包含既有/环境governance-lineage与mode项；但candidate-owned failure本身已足以要求Planner terminal review。Executer不接受候选、不提出修复方案、不运行retry。
- 该结果不是科学、device、formal、package或release结果；不产生任何科学credit或阶段解锁。

### Effect 与权限计数

- package prepare/describe/replay/probe/root create/access：`0`
- formal/replacement/release consumption：`0`
- backend/device/network/camera/Ray/strip/capture/light：`0`
- analysis/G4-07/TD-C：`0`
- source/test commit：`0`
- full invocation/retry：`1/0`
- active validation owner：`0`；PID `95333`已结束；automation `0`。

请求Planner对本终局handoff进行terminal review并reject或依PLAN依法处置。Stop保持 `RETURN_FOR_G4_06_SOURCE_ATTESTATION_V2_ENGINEERING_REVIEW`；不得重启、retry、修改冻结candidate或把本结果解释为科学/设备/formal/package证据。
