# REF-P7-25-R2-B2-P4-C1-C1-C1 validation-only provenance closure review

**归档时间：** `2026-07-31T13:51:11-0600`

**归档类型：** Executer evidence acceptance；仅接受 validation-only provenance closure，不重解释原 P4-C1 contract。

**Reviewed reference task：** `REF-P7-25-R2-B2-P4-C1-C1-C1`

**Reviewed contract：**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-P4-C1-C1-C1-CONTROLLER-SHELL-ONLY-PROVENANCE-CLOSURE-V1`

**Reviewed PLAN identity：** bytes `14839`，SHA-256
`395c7de425aa180113689231fff0fee84d6ee85e66e0a233f19456f46ec2cc5a`。

## Reviewed scope and method

本包只授权一次新的 controller-shell-only、validation-only provenance closure：从 clean activation
`79a9f5390d85040ea1e5225ca814288e70dc4896` 只读重放六个冻结 topology roles、最终 source/test 身份及 P4-C1 review
archive；全部 pre-write gates 通过后，只可向 `.agent-work/EXECUTION_RESULT.md` EOF 追加一次 truthful supersession record，并创建
exact-one-path evidence commit。Tests、compileall、CodeGraph、external/retained/validator/release/network/device/scientific 路线全部
锁定为 `0`。

Planner 未重跑 controller、tests 或 CodeGraph，也未读取 external controller/source/root、retained R3/candidate 或 release。审核只使用
本地 Git plumbing、committed file identities、ER prefix/append 边界及 machine contracts。

## Evidence and validation quality

- Evidence commit `baa14d15bfcef7463f23a1a3186741c9c9704a76` 的 direct parent 为 activation
  `79a9f5390d85040ea1e5225ca814288e70dc4896`，subject exact
  `chore(evidence): supersede p4 activation subject claim`，changed paths exact 只有
  `.agent-work/EXECUTION_RESULT.md`；审核时工作区 clean。
- Activation `79a9f539...` 的 direct parent、subject 与 exact 三路径均与 PLAN machine contract 一致；FULL machine state 是唯一 active
  C1-C1-C1 包、`executer_dispatched=true`、`device_authorized_by_this_file=false`，retained 仍为
  `RETAINED_UNVALIDATED_UNCONSUMED`。
- 六个冻结 topology roles `48adfd6...`、`0ec12f2...`、`bd9d205...`、`dfc2ed4...`、`1e63d80...`、`b8e04eb...`
  的 full SHA、direct parent、subject 与 exact changed-path set 全部匹配。
- Final source blob/SHA-256：`1868ad4b4446defcc6d8187ea21d18ccf128fa31` /
  `6e10594165016a06da462e74a9deb2d9817fd95fe1417addb7a5d26c55996745`；dedicated test blob/SHA-256：
  `25eafb91d7794d4510c9d7da34f1d8666ab1ff55` /
  `e3c4a421e691c3aaac182edc6a0963a16caea95ae04f25a68493f96277bddb72`。
- P4-C1 review archive 在 Planner-rejection 与 HEAD tree 中 blob 均为
  `ab3bf85d9365ec34834f66dd1aabbc5d4bc7c6bd`，bytes `21675`，SHA-256
  `d4c82e8479668db8bfce750e2f851bf8486db24f2c2c510ae56d00735e5997fd`。
- ER preexisting prefix bytes `1045111`、SHA-256
  `edb7b41bbeea48fbabafa102dce371b4afe11446f84de882352b4efa73f4f031` 在 HEAD 文件前缀中完全一致；commit 仅新增一个 EOF
  section（13 insertions，old lines changed `0`）。Append 精确指出旧 subject 错误、supersession 范围、原 P4-C1 rejection 保留及
  所有 hard locks 为 `0`。

## Planner findings

无 acceptance-blocking finding。

先前 C1-C1 的 zsh `path` special-parameter collision 已由本 successor 的全新 controller contract 隔离；本验收只确认 committed
provenance closure，不认证先前执行包为通过，也不认证 scientific correctness 或 external integration。

## Planner decision

`ACCEPTED_VALIDATION_ONLY_PROVENANCE_CLOSURE`。

该决定仅接受 C1-C1-C1 successor。原 P4-C1 contract 继续保持
`REJECTED_ACTIVATION_SUBJECT_AND_ER_PROVENANCE_MISMATCH`，其旧错误记录没有被改写；`0ec12f2...` implementation 只作为 retained
implementation identity，不因本决定自动获得 synthetic integration、retained validation、eligibility 或 release authority。

## Residual risks and exact next branch

- Repo-owned analyzer 的 transport-domain correction 尚未经过新的 synthetic integration execution；现有 source/test/full-suite observations
  不能替代该外层集成合同。
- 下一建议 reference：`REF-P7-25-R2-B2-P4-C1-C1-C1-I1`，由 Orchestrator 定义一个 bounded repo-owned synthetic integration
  package，消费已关闭的 provenance ambiguity，但不得复用旧 external classifier 或失败 root。
- Orchestrator 应在 FULL 中把 C1-C1-C1 标为 `ACCEPTED_VALIDATION_ONLY_PROVENANCE_CLOSURE`，保留 P4-C1 rejected 历史与
  `RETAINED_UNVALIDATED_UNCONSUMED`，再决定 exact integration scope、fresh root、evidence 与 stop。
- 本归档与 active PLAN 不授权 synthetic integration、external root、retained audit、canonical validator、eligibility、release、network 或
  device 操作。

维护性判断：本次只关闭不可变 provenance evidence，不增加代码、controller、classifier 或新 owner；下一包应继续复用 repo-owned
conformance owner，避免在 external controller 中复制 transport classification。

---

## Reviewed active PLAN full text

以下完整保存本次 reviewed active PLAN；上方 decision 与下一 branch 建议为 Planner 验收结论。

# REF-P7-25-R2-B2-P4-C1-C1-C1：controller-shell-only provenance closure

**计划状态：** `ACTIVE_EXECUTION_AUTHORIZED`

**Planner 日期：** `2026-07-31`

**Reference task：** `REF-P7-25-R2-B2-P4-C1-C1-C1`

**Contract ID：**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-P4-C1-C1-C1-CONTROLLER-SHELL-ONLY-PROVENANCE-CLOSURE-V1`

**当前唯一动作：** 使用不覆盖 zsh 特殊参数的单一新 controller，从头只读重放冻结的 committed topology、最终两文件身份与
P4-C1 review archive；全部匹配后仅向 `.agent-work/EXECUTION_RESULT.md` 追加一次 truthful supersession record，并创建一个
exact-one-path focused evidence commit。

**唯一 Planner stop：**
`B2_P4_C1_C1_C1_CONTROLLER_SHELL_ONLY_PROVENANCE_CLOSURE_WAITING_PLANNER_REVIEW`。

**本轮新归档：**
`.agent-work/PLANS/20260731-1338-p7-retained-r3-b2-p4-c1-c1-shell-failure-review.md`，bytes `18181`，SHA-256
`4f31b5b348d7e5be95b41c394853ded6522d340a34a1dcad5c344e60cb18658a`；Executer 必须从 activation commit 只读验证，
不得修改。

`PLAN_MACHINE_CONTRACT={"schema":"p7_td_b_retained_r3_option_b_b2_p4_c1_c1_c1_controller_shell_only_provenance_closure_v1","reference_task_id":"REF-P7-25-R2-B2-P4-C1-C1-C1","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-P4-C1-C1-C1-CONTROLLER-SHELL-ONLY-PROVENANCE-CLOSURE-V1","execution_authorized":true,"executer_dispatch_allowed":true,"validation_only":true,"activation_runtime_head_required":true,"activation_parent":"b8e04eb61ddb42688a0650444db3d7ce64b569ad","activation_subject":"chore(plan): correct p4 provenance shell variable","activation_changed_paths":[".agent-work/FULL_PLAN_REFERENCE.md",".agent-work/PLAN.md",".agent-work/PLANS/20260731-1338-p7-retained-r3-b2-p4-c1-c1-shell-failure-review.md"],"activation_archive_path":".agent-work/PLANS/20260731-1338-p7-retained-r3-b2-p4-c1-c1-shell-failure-review.md","activation_archive_bytes":18181,"activation_archive_sha256":"4f31b5b348d7e5be95b41c394853ded6522d340a34a1dcad5c344e60cb18658a","required_full_machine_state":{"active_task_count":1,"active_task":"REF-P7-25-R2-B2-P4-C1-C1-C1","active_plan_contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-P4-C1-C1-C1-CONTROLLER-SHELL-ONLY-PROVENANCE-CLOSURE-V1","next_reference_task":"REF-P7-25-R2-B2-P4-C1-C1-C1","next_reference_status":"ACTIVE_EXECUTION_AUTHORIZED","repair_v2_status":"P4_C1_C1_C1_CONTROLLER_SHELL_ONLY_PROVENANCE_CLOSURE_ACTIVE","retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","executer_dispatched":true,"device_authorized_by_this_file":false},"rejected_execution_activation":"b8e04eb61ddb42688a0650444db3d7ce64b569ad","implementation_commit":"0ec12f2de91b84f4379d64437170fa53c3ae4a28","misstated_evidence_commit":"bd9d205cf7a4385d202666f87d225739e57c970c","planner_rejection_commit":"dfc2ed4d646e7c1a284c075810ae1424a3272504","orchestrator_disposition_commit":"1e63d808af45424f51ff0784955c95eccf4c3230","implementation_source_blob":"1868ad4b4446defcc6d8187ea21d18ccf128fa31","implementation_source_sha256":"6e10594165016a06da462e74a9deb2d9817fd95fe1417addb7a5d26c55996745","implementation_test_blob":"25eafb91d7794d4510c9d7da34f1d8666ab1ff55","implementation_test_sha256":"e3c4a421e691c3aaac182edc6a0963a16caea95ae04f25a68493f96277bddb72","review_archive_path":".agent-work/PLANS/20260731-1326-p7-retained-r3-b2-p4-c1-transport-domain-owner-correction-review.md","review_archive_blob":"ab3bf85d9365ec34834f66dd1aabbc5d4bc7c6bd","review_archive_bytes":21675,"review_archive_sha256":"d4c82e8479668db8bfce750e2f851bf8486db24f2c2c510ae56d00735e5997fd","allowed_write_path":".agent-work/EXECUTION_RESULT.md","required_evidence_subject":"chore(evidence): supersede p4 activation subject claim","required_evidence_changed_paths":[".agent-work/EXECUTION_RESULT.md"],"implementation_original_contract_status":"REJECTED_ACTIVATION_SUBJECT_AND_ER_PROVENANCE_MISMATCH","retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","planner_stop":"B2_P4_C1_C1_C1_CONTROLLER_SHELL_ONLY_PROVENANCE_CLOSURE_WAITING_PLANNER_REVIEW","retry_budget":0,"fallback_budget":0,"zero_budgets":{"code_writes":0,"test_writes":0,"old_execution_result_line_changes":0,"full_plan_writes":0,"plan_writes":0,"archive_writes":0,"debug_writes":0,"guide_writes":0,"research_writes":0,"tests":0,"compileall":0,"codegraph":0,"external_controller_writes":0,"external_controller_reads":0,"external_root_creates":0,"external_root_reads":0,"synthetic_integration_runs":0,"retained_artifact_reads":0,"real_b2_dispatch":0,"actual_canonical_validator_calls":0,"eligibility_emissions":0,"release_operations":0,"network":0,"dns":0,"environment":0,"credentials":0,"device":0,"camera":0,"ray":0,"strip":0,"cleanup":0,"capture":0,"formal":0,"public_analyzer":0,"td_c":0,"sentinel":0,"p8":0,"firmware":0,"deployment":0}}`

## 1. Controller-shell correction and activation gate

本包不是失败执行的 retry，而是只纠正 controller shell local-variable contract 的新 validation-only successor。Executer 必须：

- 只启动一个新的 pre-write read-only shell group；不得复用失败 shell 或其部分输出；
- 禁止声明、赋值、导出或循环绑定 `path`、`PATH`、`cdpath`、`fpath`、`manpath`；
- 固定路径集合优先作为命令 argv 直接比较；确需 loop 时变量名必须为 `entry_path`，并使用不会影响 command resolution 的普通
  local scalar；
- controller shell 中不得修改 shell options、command hash table、working tree 或 environment；
- shell group 失败即停止，不得在同一进程或新进程 retry/fallback。

Executer 开始时工作区必须 clean，runtime `HEAD` 即本 Planner activation commit。其 full SHA 可在运行时捕获，但必须同时满足：

- direct parent：`b8e04eb61ddb42688a0650444db3d7ce64b569ad`；
- subject：`chore(plan): correct p4 provenance shell variable`；
- exact changed-path set（按字节排序比较）：
  - `.agent-work/FULL_PLAN_REFERENCE.md`；
  - `.agent-work/PLAN.md`；
  - `.agent-work/PLANS/20260731-1338-p7-retained-r3-b2-p4-c1-c1-shell-failure-review.md`；
- 本 PLAN 的 machine contract 可 strict JSON 解析，且只包含一个 active executable package；
- FULL 的 `FULL_PLAN_MACHINE_STATE` 必须包含与 machine contract 中 `required_full_machine_state` 逐键相等的 subset：唯一 active task
  与 next task 均为 C1-C1-C1、active contract exact、next status 为 `ACTIVE_EXECUTION_AUTHORIZED`、repair status exact、retained
  状态不变、`executer_dispatched=true`、`device_authorized_by_this_file=false`。FULL 由 Orchestrator 在 activation commit 中更新；
  Executer 只能只读验证，不得写 FULL。

任何 activation 条件不匹配：在 ER 写入、stage、commit 前 hard fail，只报告 observed failure；retry/fallback `0/0`。

## 2. Frozen topology and identities

必须从头使用 read-only Git plumbing 验证以下 exact full identities，不得消费失败执行的部分结果：

| Role | Commit | Parent | Exact subject | Exact changed paths |
| --- | --- | --- | --- | --- |
| rejected activation | `48adfd669dc8d49fe11c983a4ca36e928bef6c22` | `781e410c43774c20da9f00e8c9e0f5bfd27b1f66` | `chore(plan): activate p4 transport domain correction` | `.agent-work/FULL_PLAN_REFERENCE.md`; `.agent-work/PLAN.md`; `.agent-work/PLANS/20260731-1308-p7-retained-r3-b2-p4-i1-c1-c1-fixture-classification-failure-review.md` |
| retained implementation | `0ec12f2de91b84f4379d64437170fa53c3ae4a28` | `48adfd669dc8d49fe11c983a4ca36e928bef6c22` | `fix(p7): own retained controller transport domains` | `src/camera_based_rgbww_optimizer/utils/p7_retained_r3_controller_conformance.py`; `tests/test_p7_retained_r3_controller_conformance.py` |
| misstated evidence prerequisite | `bd9d205cf7a4385d202666f87d225739e57c970c` | `0ec12f2de91b84f4379d64437170fa53c3ae4a28` | `chore(evidence): record p4 transport domain correction` | `.agent-work/EXECUTION_RESULT.md` |
| Planner rejection | `dfc2ed4d646e7c1a284c075810ae1424a3272504` | `bd9d205cf7a4385d202666f87d225739e57c970c` | `chore(plan): reject p4 activation provenance mismatch` | `.agent-work/PLAN.md`; `.agent-work/PLANS/20260731-1326-p7-retained-r3-b2-p4-c1-transport-domain-owner-correction-review.md` |
| Orchestrator disposition | `1e63d808af45424f51ff0784955c95eccf4c3230` | `dfc2ed4d646e7c1a284c075810ae1424a3272504` | `docs(orchestration): route p4 provenance successor` | `.agent-work/FULL_PLAN_REFERENCE.md`; `.agent-work/debug/active/20260731-p7-retained-r3-b2-controller-contract-drift.md` |
| rejected shell-attempt activation | `b8e04eb61ddb42688a0650444db3d7ce64b569ad` | `1e63d808af45424f51ff0784955c95eccf4c3230` | `chore(plan): activate p4 provenance closure` | `.agent-work/PLAN.md`; `.agent-work/PLANS/20260731-1332-p7-retained-r3-b2-p4-c1-c1-provenance-disposition-review.md` |

上述 full commits 必须都是 runtime activation HEAD ancestors；禁止缩写 SHA 比较、amend、rebase、reset、cherry-pick、checkout
历史内容、重建或删除 commit。

还须验证 implementation tree 与 runtime activation tree 的最终 source/test 身份相同：

- source path `src/camera_based_rgbww_optimizer/utils/p7_retained_r3_controller_conformance.py`，blob
  `1868ad4b4446defcc6d8187ea21d18ccf128fa31`，SHA-256
  `6e10594165016a06da462e74a9deb2d9817fd95fe1417addb7a5d26c55996745`；
- test path `tests/test_p7_retained_r3_controller_conformance.py`，blob
  `25eafb91d7794d4510c9d7da34f1d8666ab1ff55`，SHA-256
  `e3c4a421e691c3aaac182edc6a0963a16caea95ae04f25a68493f96277bddb72`。

只读验证 P4-C1 review archive 在 `dfc2ed4...` 与 runtime activation tree 中 blob 均为
`ab3bf85d9365ec34834f66dd1aabbc5d4bc7c6bd`，bytes `21675`，SHA-256
`d4c82e8479668db8bfce750e2f851bf8486db24f2c2c510ae56d00735e5997fd`。

禁止读取 external controller/source/root、失败 external evidence、accepted-C1、retained R3/candidate 或 release；禁止运行测试、
compileall、CodeGraph、synthetic integration、validator 或 analyzer。任一身份不匹配都在写入前 hard fail。

## 3. Exact one-time ER append

全部 pre-write gates 通过后，只可在 `.agent-work/EXECUTION_RESULT.md` EOF append 一个新 section；旧 bytes 必须保持原样。
Section 必须包含：

1. 本 contract/reference/stop；runtime activation full SHA、parent、subject、exact two docs paths；
2. 明确上一失败执行因 zsh `path` 特殊参数 collision 在 pre-write 阶段 exit `127`，ER/stage/commit/external 全为 `0`；
3. `bd9d205...` 的错误字段：旧记录声称 activation subject 为 `chore(plan): activate p4 transport domain owner correction`，真实
   subject 是 `chore(plan): activate p4 transport domain correction`；
4. supersession 只取代该错误 subject、由其导出的 activation-gate-passed assertion 与
   `repo_transport_owner_correction_pass_waiting_for_planner` disposition；旧 implementation identity/validation observations 不被本包
   重新执行或整体删除；
5. 原 P4-C1 contract 仍为 `REJECTED_ACTIVATION_SUBJECT_AND_ER_PROVENANCE_MISMATCH`，不得称 accepted/pass；
6. 六个 frozen topology roles、最终 source/test blob+SHA、review archive blob/bytes/SHA 全部匹配；
7. 本包只证明 non-rewritten provenance closure，不证明科学正确性，不消费 retained，不调用 validator，不产生 eligibility/release/
   device/formal authority；
8. 所有 hard locks 和零预算为 `0`；append `1`，本 successor retry/fallback `0/0`。

Append 前后以 bytes/hash 证明 preexisting ER prefix 完全相同且仅新增一个 section。不得修复、重写或生成旧 payload；唯一 EOF append
可使用 `apply_patch`。

## 4. Exact-one-path evidence commit

Append 后顺序固定：

1. `git diff --check` exact `1`；
2. 验证 changed-path union exact `.agent-work/EXECUTION_RESULT.md`，再次验证 old ER prefix 不变；
3. 只 stage `.agent-work/EXECUTION_RESULT.md`，stage exact `1`；
4. 创建唯一 commit，parent 为 runtime activation full SHA，subject exact
   `chore(evidence): supersede p4 activation subject claim`；
5. postcommit 只读验证 exact path、parent、subject、工作区 clean；
6. 不运行 postcommit test/compileall/CodeGraph/external command。

Commit body 只说明追加 truthful supersession record、保留 P4-C1 rejection、不改 implementation 或历史记录。

## 5. Budgets, failure branches and acceptance

### Non-zero maximum budgets

- 一个新的 pre-write read-only shell group `1`；每个冻结 Git/tree/file/archive identity 每个需要的只读检查最多 `1`；
- ER EOF append exact `1`；`git diff --check` exact `1`；stage exact `1`；evidence commit exact `1`；
- postcommit Git/status verification exact `1` group；
- retry `0`，fallback `0`，alternate package `0`。

### Failure branches

任一 pre-write gate 不匹配或 controller shell 失败：不写 ER、不 stage、不 commit，停止并交 Planner；不得修复 controller、retry 或
fallback。Append 后/precommit gate 失败：不得改旧 ER或 commit，保留工作区交 Planner。Commit/postcommit mismatch：不得 amend/reset/
retry/追加第二记录。后续只能由 Planner/Orchestrator规划新的 bounded offline evidence correction。

### Acceptance criteria

- corrected controller 不声明/赋值 `path`/`PATH` 等特殊参数，从头完成全部 pre-write gates；
- activation、六个历史 commits、source/test、P4-C1 archive identities 全部 exact；
- ER old prefix 不变，只增加一个合约完整的 truthful section；
- evidence commit parent/subject/path exact，工作区 clean；
- P4-C1 保留 rejected，不把既有 validation observations 重解释为原合同 pass；
- tests/compileall/CodeGraph/external/retained/validator/release/network/device/scientific 全为 `0`；
- 到唯一 Planner stop，不进入 synthetic integration、retained audit、eligibility 或 release。

验收后 Planner 归档本包并只向 Orchestrator建议：C1-C1-C1 标记
`ACCEPTED_VALIDATION_ONLY_PROVENANCE_CLOSURE`，保留 P4-C1 rejected 历史，下一步可由 Orchestrator 决定 repo-owned synthetic
integration package。本建议不授权后续工作。

## Hard locks

Code/test、旧 ER lines、FULL/PLAN/archive/debug/GUIDE/RESEARCH 写入全锁 `0`。Tests、compileall、CodeGraph、external
controller/source/root、synthetic integration、failed/accepted external evidence、retained R3/candidate、real B2、subordinate manifest、
canonical validator、eligibility、retained audit、release generation/qualification/copy/consumption、network/DNS/environment/credentials、
device/camera/Ray/strip/cleanup/capture/FORMAL/public analyzer/TD-C/sentinel/P8/firmware/deployment全锁 `0`。

维护性判断：该 successor 只纠正 validation controller 的 zsh variable ownership，不增加生产 abstraction、transport classifier 或
provenance owner。
