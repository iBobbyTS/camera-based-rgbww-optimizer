# REF-P7-25-R2-B2-C4-P2-C4：observable quiet full-suite validation continuation

**计划状态：** `ACTIVE_EXECUTION_AUTHORIZED_AFTER_EXACT_ORCHESTRATOR_ACTIVATION`

**Planner 日期：** `2026-07-30`

**Reference task：** `REF-P7-25-R2-B2-C4-P2-C4`

**Contract ID：**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-C4-P2-C4-OBSERVABLE-FULL-VALIDATION-V1`

**当前唯一动作：** Orchestrator 先冻结并提交 exact activation；其后 Executer 只读
验证 activation 与冻结 corrected test 身份，不修改任何 source/test，且不重跑已经接受的
targeted `5/5`、owner `32/32` 或 focused `58/58`。Executer 只运行一次低输出、同一
session 可观测真实 exit 与完整 terminal summary 的 full suite；仅在该 gate 通过后继续
原 P2 的 compileall、CodeGraph、scope/stage、single commit 和 postcommit targeted。

**唯一 Planner stop：**
`B2_C4_P2_C4_INTEGRATION_QUALIFICATION_COMPLETE_WAITING_PLANNER_REVIEW`。

**本次 review archive：**
`.agent-work/PLANS/20260730-1329-p7-retained-r3-option-b-b2-c4-p2-c3-full-output-review.md`，
bytes `6985`，SHA-256
`a76dc1be89ba2e2bed3ca6baef8a11ac3b2e9583be5aef23687407017cd9e4be`。

`PLAN_MACHINE_CONTRACT={"schema":"p7_td_b_retained_r3_option_b_b2_c4_p2_c4_observable_full_validation_v1","reference_task_id":"REF-P7-25-R2-B2-C4-P2-C4","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-C4-P2-C4-OBSERVABLE-FULL-VALIDATION-V1","execution_authorized":true,"dispatch_state":"active_after_exact_orchestrator_activation","single_current_action":"run_one_quiet_full_suite_with_observable_terminal_exit_then_finish_original_p2_gates","preserved_test":{"path":"tests/test_p7_retained_r3_controller_integration.py","bytes":13148,"sha256":"740652267178e3225edf03efacc293cfbdfb7c18efb749b6cd9aee281a728366","git_state":"untracked_regular_file","edit_budget":0,"recreate_budget":0},"accepted_no_rerun":{"corrected_targeted":"5/5","existing_owner":"32/32","focused":"58/58"},"full_command":".venv/bin/python -m unittest discover -s tests -p 'test_*.py' -q","full_invocation_budget":1,"full_expected_test_count":717,"orchestrator_activation":{"expected_parent":"52c087c2ed0f4d177388329397f77b442bfe5848","required_subject":"chore(plan): activate retained r3 observable full validation","implementation_parent":"full_activation_commit_sha_frozen_at_dispatch"},"exact_changed_paths":["tests/test_p7_retained_r3_controller_integration.py"],"implementation_commit_subject":"test(p7): qualify retained r3 controller composition","historical_c4_reads":0,"retained_r3_reads":0,"actual_canonical_validator_calls":0,"eligibility_emissions":0,"release_operations":0,"network_operations":0,"device_operations":0,"commit_budget":1,"retry_budget":0,"planner_stop":"B2_C4_P2_C4_INTEGRATION_QUALIFICATION_COMPLETE_WAITING_PLANNER_REVIEW"}`

## 1. Planner decision and exact finding

P2-C3 的审核结论是
`REJECTED_FULL_SUITE_TERMINAL_EVIDENCE_UNAVAILABLE_IMPLEMENTATION_NOT_YET_QUALIFIED`。

以下 P2-C3 结果已接受：

- frozen pre-edit identity gate passed；
- exact semantic edit `1`，只把裸 `"camera"` token 改为 `".camera"`；
- frozen post-edit identity gate passed；
- corrected targeted `5/5` passed；
- existing two-owner suite `32/32` passed；
- focused retained-controller group `58/58` passed。

上述三组 passing test 的 rerun budget 均为 `0`。本包不得重新运行、合并运行或以其他
pattern 间接覆盖它们作为单独 gate。

P2-C3 的 verbose full unittest invocation 已运行一次，但 output transport 被截断；完成
cell 在返回真实 exit code 和 terminal unittest summary 前关闭，后续只读 retrieval 又返回
`exec cell 9 not found`。未看到 failure 不等于 pass。由于 exit/summary 均不可验证，
full gate fail closed，不能 stage 或 commit。

本包只修复 validation observability：测试文件不再编辑。使用 quiet unittest command 和
一个 unified exec session owner，确保 terminal exit 与最终 summary 同时可见。若仍丢失
任一证据，立即停止，不得再次运行。

## 2. Frozen topology, file identity and accepted inputs

冻结唯一 implementation path：

```text
tests/test_p7_retained_r3_controller_integration.py
```

当前且 dispatch 时必须仍为 untracked regular file，bytes `13148`，SHA-256
`740652267178e3225edf03efacc293cfbdfb7c18efb749b6cd9aee281a728366`。
Test edit/recreate/delete/restore/formatter budgets 全部为 `0`。

既有 committed owners 与 dedicated tests 保持只读：

| Path | Required SHA-256 |
| --- | --- |
| `src/camera_based_rgbww_optimizer/utils/p7_retained_r3_exact_five_controller.py` | `746fd13056c326489b48ca555b21618b65c8a78f198d035e18c02f68af689726` |
| `src/camera_based_rgbww_optimizer/utils/p7_retained_r3_controller_preparation.py` | `882f3819d161369012ce7fcd52cb1de1b9c56e4e1f821ff4554f6a1d8340738b` |
| `tests/test_p7_retained_r3_exact_five_controller.py` | `19858a64fb760c112783b176822e7dabf72dce1b0cf9fb21e3a4738b83cebc3d` |
| `tests/test_p7_retained_r3_controller_preparation.py` | `80ef2bead548856031c6d6f07f4ee0b6c74b8b917a45787e9f96fbf57b4d4527` |

Orchestrator activation 必须：

1. 先独立 review 本 PLAN/archive/ER，并创建 focused review commit；
2. review commit full SHA 已冻结为 activation direct parent
   `52c087c2ed0f4d177388329397f77b442bfe5848`；
3. activation commit exact subject 为
   `chore(plan): activate retained r3 observable full validation`；
4. activation 不 stage/commit/修改冻结 test 或 production/existing-test source；
5. activation 后该 test 仍为 exact untracked singleton；
6. activation full SHA 作为 immutable implementation parent 交给 Executer。

Orchestrator 已完成以上冻结并把 `execution_authorized` 改为 `true`。Executer dispatch 后只验证 HEAD/direct parent/subject 与本节 file identities，
不得重读历史 C3/C4 roots、外部 evidence、retained R3 或旧 test output。

## 3. Exact quiet full-suite output and exit ownership

Pre-full identity gate 只执行一次：验证 activation topology；对 frozen test 不跟随 symlink
执行 `lstat` 并验证 regular/untracked/bytes/SHA；验证 NUL-safe porcelain status 的
implementation path union 正好是该 `??` singleton，tracked/cached sets 为空；验证四个
committed owner/test SHA-256。不得解析 PLAN/FULL machine rows 或重跑旧 pretest。

随后只运行一次 exact command：

```text
.venv/bin/python -m unittest discover -s tests -p 'test_*.py' -q
```

Output/exit owner 冻结如下：

1. 使用一个 unified `exec_command` invocation，`yield_time_ms=30000`，
   `max_output_tokens=12000`；不得把 unittest 放入完成后无法恢复 exit 的脚本 cell，
   不得使用 verbose mode、pipeline、`tee`、redirection、detached process 或第二 command
   owner。
2. 若 initial call 返回 terminal result，保存其真实 structured `exit_code` 与完整 output；
   若返回 `session_id`，只以同一 `session_id` 的空-input `write_stdin` 继续等待，直到该
   same session 返回 terminal `exit_code`。Poll 不是新的 unittest invocation。
3. Pass 必须同时满足：structured terminal `exit_code == 0`；output 中有完整且唯一的
   `Ran 717 tests in ...s` terminal summary；后续 terminal status 为 `OK`；没有
   `FAILED`、`ERROR`、traceback、transport truncation 或 missing-output marker。
4. 仅有 output prefix、process disappearance、session lookup failure、缺少 exit code、
   缺少 summary、summary count 非 `717` 或无法证明同一 session terminal，均视为 failure。

若该唯一 quiet invocation 本身失败或证据不全：保持 test untracked、不得 compile、
CodeGraph、stage、commit、rerun、retry 或 fallback；只追加一次真实 P2-C4 failure
handoff并停止。

## 4. Budgets and hard locks

| Operation | Remaining budget |
| --- | ---: |
| activation/pre-full frozen identity gate | 1 |
| quiet observable full unittest invocation | 1 |
| same-session liveness/output polls | only as needed for that one invocation |
| compileall | 1 after full pass |
| CodeGraph sync | 1 after compile pass |
| postvalidation frozen-file/scope gate | 1 |
| implementation staging | 1 |
| implementation commit | 1 |
| corrected targeted test, postcommit | 1 |
| corrected targeted/owner/focused precommit rerun | 0 |
| test/source edit/recreate/delete/restore/formatter | 0 |
| verbose full rerun or any second full invocation | 0 |
| PLAN/FULL machine-row parse/revalidation | 0 |
| production/existing-test edit | 0 |
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

本包是 local sub-10-minute validation continuation，不涉及 visible Terminal、automation、
Human device authorization 或 Advisor input。

## 5. Ordered post-full gates

Section 3 full gate pass 后只按以下顺序执行；任何失败均停止，不得 edit、full rerun、
retry、fallback 或 commit：

1. Compile exactly once：
   `.venv/bin/python -m compileall -q src/camera_based_rgbww_optimizer tests`。
2. `codegraph sync` exactly once并 require exit `0`。
3. Postvalidation：重新验证 frozen test 为 regular file、bytes/SHA 不变；验证四个
   committed owner/test SHA 不变；NUL-safe tracked/cached/untracked union 仍为 exact
   untracked singleton；运行一次
   `git diff --no-index --check -- /dev/null tests/test_p7_retained_r3_controller_integration.py`，
   require clean-new-file exit `1` 且 diagnostic bytes `0`。
4. Freeze implementation parent full SHA、absent-before/new-after Git blob OIDs、file
   SHA-256 与 canonical binary Git patch SHA-256。只在此时运行
   `git add -- tests/test_p7_retained_r3_controller_integration.py`。Require staged NUL
   path set exact singleton、unstaged implementation path set empty、
   `git diff --cached --check` exit `0`，且 staged blob/patch identities匹配 frozen values。
5. 创建 exactly one commit，subject
   `test(p7): qualify retained r3 controller composition`，detail 简述 existing-owner
   callback composition。不得 stage PLAN/FULL/ER/archive 或任何其他 path。
6. 验证 exact direct parent、subject、singleton tree change、absent-before/after blob、
   file/patch identities与 zero implementation drift。只运行一次 postcommit targeted：
   `.venv/bin/python -m unittest tests.test_p7_retained_r3_controller_integration -v`，
   require exit `0`、`5/5`。
7. 向 `.agent-work/EXECUTION_RESULT.md` 追加一次真实 P2-C4 handoff；记录 activation
   topology、preserved identity、accepted-no-rerun facts、quiet full command的 same-session
   owner与 terminal exit/summary、所有 downstream results、commit identities、explicit
   zero counters 与 unique stop。不得编辑 PLAN/FULL/archive。

若 compile/CodeGraph/postvalidation 失败，不得 stage/commit。若 staging、commit 或
postcommit gate 失败，不得 amend、repair、unstage/recreate 或 second commit。每个 terminal
branch 都保留当时 test/commit state，最多追加一次真实 handoff并停止。

## 6. Acceptance and stop

Planner 仅在下列全部成立时接受 P2-C4：

- exact activation topology 与 frozen test/owner identities通过；
- test/source edit count保持 `0`，corrected test 全程保持 bytes `13148`、SHA-256
  `740652267178e3225edf03efacc293cfbdfb7c18efb749b6cd9aee281a728366`；
- accepted targeted `5/5`、owner `32/32`、focused `58/58` 未重跑；
- unique quiet full command由同一 owner返回 real exit `0`、完整 `Ran 717 tests` summary
  与 `OK`；
- compileall、CodeGraph、postvalidation、scope/staging 和 postcommit targeted 全部在
  exact budgets通过；
- child 具有 frozen implementation parent、exact original P2 subject、singleton tree
  change和 exact file/blob/patch identities；
- actual validator、eligibility、release、historical、retained、network、device 与
  external-root counters保持 zero；
- 唯一 ER handoff stop 为
  `B2_C4_P2_C4_INTEGRATION_QUALIFICATION_COMPLETE_WAITING_PLANNER_REVIEW`。

Success 只解锁 Orchestrator/Planner review 与下一个 provenance-bound C4 package。它不
解锁 retained R3、real B2、canonical validator、eligibility、release consumption 或
任何 device/scientific work。

## 维护性判断

本 continuation 不再修改 test 或 production code，只把 full-suite 终端证据交给一个
quiet、same-session output/exit owner，并复用原 P2 downstream gates。没有新增 helper、
parallel validator、execution framework 或外部 evidence root；无需进一步重构。
