# REF-P7-25-R2-B2-C4-P2-C3：static ownership guard correction

**计划状态：** `EXECUTION_AUTHORIZED_AFTER_EXACT_ORCHESTRATOR_ACTIVATION_COMMIT`

**Planner 日期：** `2026-07-30`

**Reference task：** `REF-P7-25-R2-B2-C4-P2-C3`

**Contract ID：**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-C4-P2-C3-STATIC-GUARD-CORRECTION-V1`

**当前唯一动作：** 在 Orchestrator 以冻结拓扑激活本 PLAN 后，Executer 验证一次
activation 与冻结 pre-edit test 身份，只把 static forbidden-module token 从裸
`"camera"` 改为 component-qualified `".camera"`，验证冻结 post-edit 身份，然后从
首次 targeted test 重新开始原 P2 尚未完成的 ordered gates。除这一处精确替换外，
不得修改或重建 integration test、production owner 或任何其他实现路径。

**唯一 Planner stop：**
`B2_C4_P2_C3_INTEGRATION_QUALIFICATION_COMPLETE_WAITING_PLANNER_REVIEW`。

**本次 review archive：**
`.agent-work/PLANS/20260730-1319-p7-retained-r3-option-b-b2-c4-p2-c2-targeted-failure-review.md`，
bytes `6377`，SHA-256
`262cfb92e53db6adb0faca307f1738fc8f19e77f2c1570da4415b85b70ca41d8`。

`PLAN_MACHINE_CONTRACT={"schema":"p7_td_b_retained_r3_option_b_b2_c4_p2_c3_static_guard_correction_v1","reference_task_id":"REF-P7-25-R2-B2-C4-P2-C3","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-C4-P2-C3-STATIC-GUARD-CORRECTION-V1","execution_authorized":true,"dispatch_state":"ready_only_after_exact_orchestrator_activation_commit","single_current_action":"apply_exact_component_qualified_camera_guard_then_resume_p2_at_targeted","preserved_test":{"path":"tests/test_p7_retained_r3_controller_integration.py","pre_edit_bytes":13147,"pre_edit_sha256":"106ddcafddbc31d8172b3f6a3a2557830f5581bad56b8fda50a6c2e86820ca5d","post_edit_bytes":13148,"post_edit_sha256":"740652267178e3225edf03efacc293cfbdfb7c18efb749b6cd9aee281a728366","git_state":"untracked_regular_file","semantic_edit_budget":1,"other_edit_budget":0,"recreate_budget":0},"orchestrator_activation":{"expected_parent":"4f0e4b72d7e9b3eb16ae71e02c4e2b495e6a632d","required_subject":"chore(plan): activate retained r3 integration guard correction","implementation_parent":"full_activation_commit_sha_frozen_at_dispatch"},"exact_changed_paths":["tests/test_p7_retained_r3_controller_integration.py"],"implementation_commit_subject":"test(p7): qualify retained r3 controller composition","historical_c4_reads":0,"retained_r3_reads":0,"actual_canonical_validator_calls":0,"eligibility_emissions":0,"release_operations":0,"network_operations":0,"device_operations":0,"commit_budget":1,"retry_budget":0,"planner_stop":"B2_C4_P2_C3_INTEGRATION_QUALIFICATION_COMPLETE_WAITING_PLANNER_REVIEW"}`

## 1. Planner decision and exact finding

P2-C2 的审核结论是
`REJECTED_STATIC_GUARD_FALSE_POSITIVE_IMPLEMENTATION_NOT_YET_QUALIFIED`。
Parser-free pretest gate 已通过，首次 targeted 为 `4/5`；唯一失败是
`test_static_ownership_boundary_has_no_real_validator_or_io_surface`。

该 test 先要求 imported project modules 精确等于：

```text
camera_based_rgbww_optimizer.utils.p7_retained_r3_controller_preparation
camera_based_rgbww_optimizer.utils.p7_retained_r3_exact_five_controller
```

随后却以裸 substring `camera` 拒绝全部 imported module names，因此必然命中上述
两个被要求存在的 package names。冻结 imports 没有真实 camera-control module、real
canonical validator、release owner 或 I/O owner；这是 test guard 的内部矛盾，不是
integration 违规。

最小语义修复是将单个 forbidden token 改成 `.camera`。它不再命中顶层 package prefix
`camera_based_rgbww_optimizer`，但仍会拒绝 `.camera_remote`、`.camera_gphoto2` 等
camera module component。不得删除整个 camera guard，不得弱化其他 forbidden tokens
或 prohibited-call checks。

若修复后的首次 targeted 失败，保持现场，追加一次真实 failure handoff 并停止；没有
第二次 edit、retry 或 fallback 授权。

## 2. Frozen topology, file identity and accepted facts

冻结唯一实现路径：

```text
tests/test_p7_retained_r3_controller_integration.py
```

Pre-edit identity：untracked regular file，bytes `13147`，SHA-256
`106ddcafddbc31d8172b3f6a3a2557830f5581bad56b8fda50a6c2e86820ca5d`。

Post-edit identity：untracked regular file，bytes `13148`，SHA-256
`740652267178e3225edf03efacc293cfbdfb7c18efb749b6cd9aee281a728366`。

Orchestrator activation commit 必须满足：

- exact direct parent：`4f0e4b72d7e9b3eb16ae71e02c4e2b495e6a632d`；
- exact subject：`chore(plan): activate retained r3 integration guard correction`；
- activation 不 stage/commit/修改冻结 integration test 或 production/existing-test
  source；
- activation 后冻结 test 仍是唯一 worktree path，Git class 为 untracked；
- activation full SHA 作为 immutable implementation parent 交给 Executer。

下列 P2-C2 facts 已由 Planner 接受且 rerun budget 为 `0`：旧 PLAN/FULL/input
preconditions、source creation、parser-free pretest lstat/status/union/no-index gate，
以及首次 targeted `4/5` 失败 invocation。Executer 不得重读历史 C3/C4/evidence，
不得重新解析 PLAN/FULL machine rows，也不得重跑 superseded pretest 或首次失败 test。
本 PLAN 的 targeted budget 是 post-correction 的一轮 fresh invocation。

既有 committed owners 与 dedicated tests 保持只读：

| Path | Required SHA-256 |
| --- | --- |
| `src/camera_based_rgbww_optimizer/utils/p7_retained_r3_exact_five_controller.py` | `746fd13056c326489b48ca555b21618b65c8a78f198d035e18c02f68af689726` |
| `src/camera_based_rgbww_optimizer/utils/p7_retained_r3_controller_preparation.py` | `882f3819d161369012ce7fcd52cb1de1b9c56e4e1f821ff4554f6a1d8340738b` |
| `tests/test_p7_retained_r3_exact_five_controller.py` | `19858a64fb760c112783b176822e7dabf72dce1b0cf9fb21e3a4738b83cebc3d` |
| `tests/test_p7_retained_r3_controller_preparation.py` | `80ef2bead548856031c6d6f07f4ee0b6c74b8b917a45787e9f96fbf57b4d4527` |

## 3. Exact semantic correction gate

任何测试前只执行一次：

1. 读取一次 HEAD、一次 direct parent 与一次 subject，require section 2 exact
   activation topology。不得解析 PLAN/FULL machine rows 或重跑旧 preconditions。
2. 对冻结 test 执行不跟随 symlink 的 `lstat`，require untracked regular file、exact
   pre-edit bytes/SHA；require NUL-safe porcelain status 只有该 `??` singleton，tracked
   与 cached sets 为空。不得 stage、intent-to-add 或 formatter。
3. 在内存中 require exact byte sequence
   `b'            "camera",\n'` 出现 exactly once，且
   `b'            ".camera",\n'` 出现 zero times。只执行一次该等长语义位置的
   byte-local replacement；实际文件只增加前导 `.` 这一个 byte。
4. 重新 lstat/read/hash 一次，require exact post-edit bytes/SHA；require old sequence
   zero、new sequence exactly once。Require Git status/union 仍是 untracked exact
   singleton，production/existing-test/PLAN/FULL/archive drift 为 zero。

任一 mismatch 都 hard stop：不得 undo、repair、second edit、formatter、retry、fallback、
stage 或 commit；只追加一次真实 P2-C3 failure handoff。

## 4. Frozen integration behavior

修复后的 test 必须通过两个既有 public owners 验证：

1. success composition：exact callback order、five materializations、prepared-source
   identity、canonical terminal target validation、immutable gate payload、synthetic
   validator call 与 one post-seal ER admission；
2. preparation failure 发生在所有 lifecycle/terminal/ER callbacks 之前；
3. pre-terminal lifecycle failure 抑制 later phases，写 exactly one canonical failure
   terminal，并仅在 target validation 后准许 ER；
4. seal target 的错误 type/value 在 ER 前 fail，无 fallback；
5. static boundary 只允许两个预期项目 owner modules；component-qualified camera、
   real validator、retained/release、filesystem、process、network、environment 和 device
   owner/call 均不得出现。

名为 `canonical_validator` 的 callback 只能是 inline in-memory exact-bool stub；
synthetic invocation 单独计数，actual canonical validator import/call 始终为 `0`。

## 5. Budgets and hard locks

| Operation | Remaining budget |
| --- | ---: |
| activation plus pre-edit identity gate | 1 |
| exact component-qualified semantic edit | 1 |
| post-edit identity gate | 1 |
| corrected targeted test, precommit | 1 |
| existing two-owner combined suite | 1 |
| focused retained-controller group | 1 |
| full unittest suite | 1 |
| compileall | 1 |
| CodeGraph sync | 1 |
| postvalidation frozen-file/scope gate | 1 |
| implementation commit | 1 |
| corrected targeted test, postcommit | 1 |
| old preconditions/pretest/failed targeted rerun | 0 |
| PLAN/FULL machine-row parse/revalidation | 0 |
| other test edit/recreate/delete-restore/formatter | 0 |
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

本包是 local sub-10-minute single-test correction/qualification，不涉及 visible
Terminal、automation、Human device authorization 或 Advisor input。

## 6. Ordered continuation gates

Section 3 pass 后只按以下顺序各执行一次；任何失败均停止，不得 second edit、retry、
fallback 或 commit：

1. Corrected integration targeted：
   `.venv/bin/python -m unittest tests.test_p7_retained_r3_controller_integration -v`。
2. Existing two-owner suite：
   `.venv/bin/python -m unittest tests.test_p7_retained_r3_exact_five_controller tests.test_p7_retained_r3_controller_preparation -v`。
3. Focused group：
   `.venv/bin/python -m unittest tests.test_p7_retained_r3_controller_integration tests.test_p7_retained_r3_exact_five_controller tests.test_p7_retained_r3_controller_preparation tests.test_p7_retained_release_audit -v`。
4. Full suite：
   `.venv/bin/python -m unittest discover -s tests -p 'test_*.py' -v`。
5. Compile：
   `.venv/bin/python -m compileall -q src/camera_based_rgbww_optimizer tests`。
6. `codegraph sync` 一次并 require success。重新验证 test lstat/bytes/SHA、old/new
   sequence、NUL-safe tracked/cached/untracked exact singleton union，并运行一次
   `git diff --no-index --check -- /dev/null tests/test_p7_retained_r3_controller_integration.py`；
   require clean-new-file exit `1` 且无 whitespace diagnostic。
7. Freeze implementation parent full SHA、absent-before/new-after Git blob OIDs、file
   SHA-256 与 canonical binary Git patch SHA-256。仅此时运行
   `git add -- tests/test_p7_retained_r3_controller_integration.py`。Require staged
   NUL path set exact singleton、unstaged path set empty、`git diff --cached --check`
   success，并 require staged blob/patch identities匹配 frozen values。
8. 创建 exactly one commit，subject
   `test(p7): qualify retained r3 controller composition`，detail 简述 existing-owner
   callback composition。
9. 验证 exact direct parent、subject、singleton tree change、absent-before/after blob、
   file/patch identities与 zero implementation drift；只运行一次 corrected targeted
   作为 sole postcommit test。
10. 向 `.agent-work/EXECUTION_RESULT.md` 追加一次真实 P2-C3 handoff。记录 activation
    topology、pre/post identities、exact edit counts、所有 ordered results、synthetic
    stub/actual-validator counts、commit identity、explicit zero budgets 与 unique stop。
    不得编辑 PLAN/FULL/archive。

若 precommit gate 失败，不得 stage/commit。若 staging、commit 或 postcommit gate 失败，
不得 amend、repair 或 second commit。每个 terminal branch 都保留当时 test/commit state，
最多追加一次真实 handoff并停止。

## 7. Acceptance and stop

Planner 仅在下列全部成立时接受 P2-C3：

- exact activation topology、pre-edit identity、single semantic edit 与 post-edit identity
  在 budgets 内通过；
- bare `camera` guard 被 exact `.camera` guard 唯一替换，其他 static boundary 不变；
- corrected targeted、owners、focused、full、compileall、CodeGraph、postvalidation、
  diff/staging 和 postcommit gates 全部在 exact budgets 通过；
- child 具有 frozen parent、exact original P2 subject、singleton tree change 和 exact
  file/blob/patch identities；
- actual validator、eligibility、release、historical、retained、network、device 与
  external-root counters保持 zero；
- 唯一 ER handoff stop 为
  `B2_C4_P2_C3_INTEGRATION_QUALIFICATION_COMPLETE_WAITING_PLANNER_REVIEW`。

Success 只解锁 Orchestrator review 与下一个 provenance-bound C4 package。它不解锁
retained R3、real B2、canonical validator、eligibility、release consumption 或任何
device/scientific work。

## 维护性判断

本 correction 只修复 integration test 内单个自相矛盾的 substring sentinel，不改变
任何 production owner、validator ownership 或 execution architecture。使用
component-qualified token 保留 camera-module 防线，同时避免误伤顶层项目包名；无需
额外重构。
