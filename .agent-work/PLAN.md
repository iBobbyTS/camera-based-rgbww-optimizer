# REF-P7-25-R2-B2-C4-P2-C2：parser-free pretest gate correction

**计划状态：** `EXECUTION_AUTHORIZED_AFTER_EXACT_ORCHESTRATOR_ACTIVATION_COMMIT`

**Planner 日期：** `2026-07-30`

**Reference task：** `REF-P7-25-R2-B2-C4-P2-C2`

**Contract ID：**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-C4-P2-C2-PARSER-FREE-PRETEST-GATE-V1`

**当前唯一动作：** 保留现有未跟踪 integration test 的精确字节；在 Orchestrator
以冻结拓扑激活本 PLAN 后，Executer 只验证一次 HEAD/parent/subject、冻结测试
lstat/bytes/SHA、NUL-safe status/union 与 no-index whitespace gate，然后从首次
targeted test 继续原 P2 尚未执行的 ordered gates。Executer 不再解析或重建
PLAN/FULL machine rows，不重跑旧 preconditions，也不得编辑或重建冻结测试。

**唯一 Planner stop：**
`B2_C4_P2_C2_INTEGRATION_QUALIFICATION_COMPLETE_WAITING_PLANNER_REVIEW`。

**本次 review archive：**
`.agent-work/PLANS/20260730-1311-p7-retained-r3-option-b-b2-c4-p2-c1-parser-failure-review.md`，
bytes `5912`，SHA-256
`e20834857bcf7061b9d3ed3a2b4c8599d4245d89704b1d5a7fa2509e60fbb481`。

`PLAN_MACHINE_CONTRACT={"schema":"p7_td_b_retained_r3_option_b_b2_c4_p2_c2_parser_free_pretest_gate_v1","reference_task_id":"REF-P7-25-R2-B2-C4-P2-C2","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-C4-P2-C2-PARSER-FREE-PRETEST-GATE-V1","execution_authorized":true,"dispatch_state":"ready_only_after_exact_orchestrator_activation_commit","single_current_action":"verify_activation_and_frozen_file_scope_then_resume_unrun_p2_gates","preserved_test":{"path":"tests/test_p7_retained_r3_controller_integration.py","bytes":13147,"sha256":"106ddcafddbc31d8172b3f6a3a2557830f5581bad56b8fda50a6c2e86820ca5d","git_state":"untracked_regular_file","edit_budget":0,"recreate_budget":0},"orchestrator_activation":{"expected_parent":"c521447e9cefe51c1263565a3d8c1bba3e1aaaf3","required_subject":"chore(plan): activate retained r3 parser-free pretest gate correction","executer_plan_full_machine_row_parses":0,"implementation_parent":"full_activation_commit_sha_frozen_at_dispatch"},"exact_changed_paths":["tests/test_p7_retained_r3_controller_integration.py"],"implementation_commit_subject":"test(p7): qualify retained r3 controller composition","historical_c4_reads":0,"retained_r3_reads":0,"actual_canonical_validator_calls":0,"eligibility_emissions":0,"release_operations":0,"network_operations":0,"device_operations":0,"commit_budget":1,"retry_budget":0,"planner_stop":"B2_C4_P2_C2_INTEGRATION_QUALIFICATION_COMPLETE_WAITING_PLANNER_REVIEW"}`

## 1. Planner decision and bounded correction

P2-C1 的审核结论是
`REJECTED_EXECUTION_GATE_OWNER_PARSER_DEFECT_IMPLEMENTATION_NOT_EVALUATED`。
唯一 gate 在解析 Markdown machine row 时因前导反引号产生 `StopIteration`；它在
正式文件身份、Git union、no-index check 和任何测试之前失败。因此 integration
test 与两个既有 owner 均未被行为评估。

P2-C2 删除这项重复且表示敏感的 Executer-side authorization parser。Orchestrator
负责独立验证 PLAN/FULL 并以冻结 parent 与 subject 产生 activation commit；
Executer 消费该已激活状态时，只证明 Git 拓扑、冻结文件身份与真实 scope gate。
不得用另一种 Markdown/JSON parser、正则、行扫描或 FULL/PLAN hash gate 替代被删
要求。

若首次 targeted test 失败，保持测试原样，追加一次真实失败交接并停止。没有重试、
修复或 fallback 授权。

## 2. Frozen implementation and activation topology

冻结实现唯一为：

```text
tests/test_p7_retained_r3_controller_integration.py
```

其身份为未跟踪常规文件、bytes `13147`、SHA-256
`106ddcafddbc31d8172b3f6a3a2557830f5581bad56b8fda50a6c2e86820ca5d`。
从 activation 前到唯一授权 staging step 前，edit、recreate、delete/restore、
formatter、generator 和 content rewrite budgets 全为 `0`。

Orchestrator activation commit 必须满足：

- exact direct parent：`c521447e9cefe51c1263565a3d8c1bba3e1aaaf3`；
- exact subject：`chore(plan): activate retained r3 parser-free pretest gate correction`；
- activation 不 stage/commit/修改冻结测试或任何 production/existing-test source；
- activation 后冻结测试仍是唯一未跟踪 path，tracked/index worktree clean；
- activation full SHA 作为 immutable implementation parent 交给 Executer。

Executer 不得解析 PLAN/FULL machine contract、task row、active-task count、hash、
archive row 或 retained-status row来重新决定 authorization。Orchestrator 的 exact
activation commit 与 dispatch 已拥有该判断。Executer 仍须按本 PLAN 的普通文本边界
执行，且不得据此扩大范围。

下列旧 facts 已接受且重跑 budget 为 `0`：原 P2/P2-C1 的 PLAN/FULL/input ancestry
preflight、最初 clean-worktree check、source creation，以及已耗尽的两个旧 pretest
gate。既有 committed owners 保持只读：

| Path | Required SHA-256 |
| --- | --- |
| `src/camera_based_rgbww_optimizer/utils/p7_retained_r3_exact_five_controller.py` | `746fd13056c326489b48ca555b21618b65c8a78f198d035e18c02f68af689726` |
| `src/camera_based_rgbww_optimizer/utils/p7_retained_r3_controller_preparation.py` | `882f3819d161369012ce7fcd52cb1de1b9c56e4e1f821ff4554f6a1d8340738b` |
| `tests/test_p7_retained_r3_exact_five_controller.py` | `19858a64fb760c112783b176822e7dabf72dce1b0cf9fb21e3a4738b83cebc3d` |
| `tests/test_p7_retained_r3_controller_preparation.py` | `80ef2bead548856031c6d6f07f4ee0b6c74b8b917a45787e9f96fbf57b4d4527` |

不要为这些 frozen hashes 重跑旧 preflight；若在后续既有命令中偶然观察到 mismatch，
应 hard stop，不得修复。

## 3. Sole parser-free pretest gate

任何测试前，按以下顺序只执行一次：

1. 读取一次 HEAD、一次 direct parent 与一次 subject；require section 2 exact
   activation topology。不得读取或解析 PLAN/FULL machine rows、task/status rows、
   hashes 或旧 input preconditions。
2. 对冻结测试执行不跟随 symlink 的 `lstat`，require regular file、exact bytes 和
   exact SHA-256。
3. 将 `git status --porcelain=v1 -z --untracked-files=all` 作为 NUL-delimited bytes
   解析；require 唯一 record 为 `?? ` 加 exact test path。拒绝 rename、quoted path、
   additional record、tracked 或 index change。
4. 独立解析 `git diff --name-only -z --` 与
   `git diff --cached --name-only -z --`，require 两个 tracked sets 均为空；解析
   `git ls-files --others --exclude-standard -z --`，require untracked set 等于 exact
   singleton test。三者 union 必须等于 singleton，classification 必须 disjoint。
5. 运行一次
   `git diff --no-index --check -- /dev/null tests/test_p7_retained_r3_controller_integration.py`。
   因文件为新增，require exit `1` 且无 whitespace-error output；其他 exit 或诊断均
   fail closed。

本 gate 禁止 `git add -N`、intent-to-add、stage、stash、checkout、reset、clean、
formatter、content rewrite、PLAN/FULL parser、alternate scope command、retry 或
fallback。任一 mismatch 都只能追加一次真实 P2-C2 failure handoff 后停止。

## 4. Frozen integration behavior

冻结测试须通过既有 exact-five lifecycle 和 preparation owner 的真实 public APIs
验证：

1. success composition：exact callback order、five materializations、prepared-source
   identity、canonical terminal target validation、immutable gate payload、synthetic
   validator call 与 one post-seal ER admission；
2. preparation failure 发生在所有 lifecycle/terminal/ER callbacks 之前；
3. pre-terminal lifecycle failure 抑制 later phases，写 exactly one canonical failure
   terminal，并仅在 target validation 后准许 ER；
4. seal target 的错误 type/value 在 ER 前 fail，无 fallback；
5. 不 import/call real canonical validator、retained/release owner、filesystem、process、
   network、environment 或 device owner。

名为 `canonical_validator` 的 callback 必须只是 inline in-memory exact-bool stub。
单独记录其 synthetic invocation；actual canonical validator import/call 始终为 `0`。
测试不得复制两个 production owner 的实现。

## 5. Budgets and hard locks

| Operation | Remaining budget |
| --- | ---: |
| activation topology plus frozen-file/scope gate | 1 |
| new targeted test, precommit | 1 |
| existing two-owner combined suite | 1 |
| focused retained-controller group | 1 |
| full unittest suite | 1 |
| compileall | 1 |
| CodeGraph sync | 1 |
| postvalidation frozen-file/scope gate | 1 |
| implementation commit | 1 |
| new targeted test, postcommit | 1 |
| PLAN/FULL machine-row parse/revalidation | 0 |
| old preconditions/source creation/old gate rerun | 0 |
| test edit/recreate/delete-restore/formatter | 0 |
| amend/rebase/fixup/second commit | 0 |
| retry/fallback | 0 |
| historical C3/C4/failed-root reads | 0 |
| retained R3 candidate/artifact reads | 0 |
| real B2/controller dispatch | 0 |
| actual canonical validator import/call | 0 |
| eligibility emission/consumer | 0 |
| lineage/release create/validate/replay/consume | 0 |
| external root or temporary evidence file | 0 |
| network, DNS, `.env`, credentials | 0 |
| device/camera/Ray/strip/cleanup/capture/FORMAL | 0 |
| public analyzer, TD-C, sentinel, P8, firmware/deployment | 0 |

本包是 local sub-10-minute code/test qualification，不涉及 visible Terminal、
automation、Human device authorization 或 Advisor input。

## 6. Ordered continuation gates

Section 3 pass 后只按以下顺序各执行一次；任何失败均停止，不得 test repair、retry、
fallback 或 commit：

1. New integration targeted：
   `.venv/bin/python -m unittest tests.test_p7_retained_r3_controller_integration -v`。
2. Existing two-owner suite：
   `.venv/bin/python -m unittest tests.test_p7_retained_r3_exact_five_controller tests.test_p7_retained_r3_controller_preparation -v`。
3. Focused group：
   `.venv/bin/python -m unittest tests.test_p7_retained_r3_controller_integration tests.test_p7_retained_r3_exact_five_controller tests.test_p7_retained_r3_controller_preparation tests.test_p7_retained_release_audit -v`。
4. Full suite：
   `.venv/bin/python -m unittest discover -s tests -p 'test_*.py' -v`。
5. Compile：
   `.venv/bin/python -m compileall -q src/camera_based_rgbww_optimizer tests`。
6. `codegraph sync` 一次并 require success。重新验证 test lstat/bytes/SHA、NUL-safe
   tracked/cached/untracked exact singleton union，并再执行一次 no-index whitespace
   check 作为 postvalidation gate；不得解析 PLAN/FULL。
7. Freeze implementation parent full SHA、absent-before/new-after Git blob OIDs、file
   SHA-256 与 canonical binary Git patch SHA-256。仅此时运行
   `git add -- tests/test_p7_retained_r3_controller_integration.py`。Require staged
   NUL path set exact singleton、unstaged path set empty、`git diff --cached --check`
   success，并 require staged blob/patch identities 匹配 frozen values。
8. 创建 exactly one commit，subject
   `test(p7): qualify retained r3 controller composition`，detail 简述 existing-owner
   callback composition。
9. 验证 exact direct parent、subject、singleton tree change、absent-before/after blob、
   file/patch identities 与 zero implementation drift；只运行一次 new targeted 作为
   sole postcommit test。
10. 向 `.agent-work/EXECUTION_RESULT.md` 追加一次真实 P2-C2 handoff。记录 activation
    topology、preserved identity、parser counts `0`、NUL-safe classification、所有 ordered
    counts/results、synthetic stub/actual-validator counts、commit identity、explicit zero
    budgets 与 unique stop。不得编辑 PLAN/FULL/archive。

若 precommit gate 失败，不得 stage/commit。若 staging、commit 或 postcommit gate 失败，
不得 amend、repair 或 second commit。每个 terminal branch 都保留当时 test/commit state，
最多追加一次真实 handoff 并停止。

## 7. Acceptance and stop

Planner 仅在下列全部成立时接受 P2-C2：

- exact activation topology 和冻结测试身份通过，且 Executer 的 PLAN/FULL machine-row
  parser/revalidation count 为 `0`；
- NUL-safe status/union/no-index gate 与 postvalidation gate 均在 exact budgets 通过；
- test 在唯一 staging 前保持 exact bytes/SHA；
- section 4 的行为通过两个真实 public owners；
- targeted、owners、focused、full、compileall、CodeGraph、diff/staging 和 postcommit
  gates 全部在 exact budgets 通过；
- child 具有 frozen parent、exact subject、singleton tree change 和 exact file/blob/
  patch identities；
- actual validator、eligibility、release、historical、retained、network、device 与
  external-root counters 保持 zero；
- 唯一 ER handoff stop 为
  `B2_C4_P2_C2_INTEGRATION_QUALIFICATION_COMPLETE_WAITING_PLANNER_REVIEW`。

Success 只解锁 Orchestrator review 与下一个 provenance-bound C4 package。它不解锁
retained R3、real B2、canonical validator、eligibility、release consumption 或任何
device/scientific work。

## 维护性判断

本 correction 不增加 parser 或 owner；它删除重复的 Markdown 授权解析，将 Executer
gate 收敛到 immutable activation topology 与实际消费的 file/Git scope。后续验证和
production eligibility owner 均不变，无需额外重构。
