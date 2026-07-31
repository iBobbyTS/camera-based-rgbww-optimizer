# REF-P7-25-R2-B2-P4-C1-C1 pre-write shell failure review

**归档时间：** `2026-07-31T13:38:38-0600`

**归档类型：** Executer pre-write hard failure；拒绝本次执行并转入 bounded controller-shell correction successor。

**Reviewed reference task：** `REF-P7-25-R2-B2-P4-C1-C1`

**Reviewed contract：**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-P4-C1-C1-VALIDATION-ONLY-PROVENANCE-CLOSURE-V1`

**Reviewed PLAN identity：** bytes `13456`，SHA-256
`065ece06d0ed153f27626d83a9648868500b53cefec441f50ce90766c6e08457`。

## Reviewed scope and method

被审核计划授权一次 validation-only provenance closure：只读核验 activation、五个冻结历史 commits、最终 source/test
身份和 P4-C1 review archive；全部匹配后才可在 `.agent-work/EXECUTION_RESULT.md` EOF 追加一次 truthful supersession
record，并创建 exact-one-path evidence commit。计划明确锁定 code/test/FULL/PLAN/archive/debug/GUIDE/RESEARCH、所有
external/retained/validator/release/network/device/scientific 路线，retry/fallback 均为 `0`。

Executer 使用唯一只读 shell group 执行 pre-write gate。activation 与 topology 前半检查通过；随后 zsh loop 把普通循环变量命名为
`path`。zsh 的 `path` 是与 `PATH` 绑定的特殊数组变量，赋值后覆盖命令搜索路径，导致后续 `git` 无法解析并以 exit `127`
hard fail。该结果是 controller-shell contract defect，不是任何冻结 Git/file identity mismatch。

## Evidence and validation quality

- Runtime HEAD 保持 activation commit `b8e04eb61ddb42688a0650444db3d7ce64b569ad`；未创建后续 commit。
- Activation/topology 前半只读检查已观察为通过，但失败包不把未完成的整组 gate 记为通过，也不复用其部分结果作为 successor
  acceptance evidence。
- Hard failure 发生在 ER write gate 前：ER append `0`，旧 ER 修改 `0`，stage `0`，commit `0`。
- 工作区在审核时 clean；FULL/PLAN/archive/code/test/debug/GUIDE/RESEARCH 均未被 Executer 修改。
- Tests、compileall、CodeGraph、external controller/source/root、synthetic integration、retained R3/candidate、real B2、canonical
  validator、eligibility、release、network/DNS/environment/credentials、device/camera/Ray/strip/cleanup/capture/FORMAL/public
  analyzer/TD-C/sentinel/P8/firmware/deployment 调用全部为 `0`。
- 失败未写入 `.agent-work/EXECUTION_RESULT.md`，因此本归档保留协作层面的 truthful failure observation；不得伪造或补写成已完成
  C1-C1 evidence。

## Planner findings

### P4-C1-C1-SHELL-001 — zsh special parameter shadowed command search path

唯一 shell group 使用 `path` 作为 loop variable，意外改写 zsh 特殊参数 `path`/`PATH`，使后续 Git plumbing 无法启动。原计划的
科学、provenance、path、hash、append 和 commit acceptance contract 无需放宽；只需在 successor controller 中使用
`entry_path` 等非特殊局部变量，或直接把固定路径作为命令 argv，禁止任何对 `path`/`PATH` 的赋值。

## Planner decision

`REJECTED_PREWRITE_CONTROLLER_SHELL_SPECIAL_PARAMETER_COLLISION`。

本次执行不能验收：完整 pre-write identity gate 未结束，ER supersession record 与 evidence commit 均不存在。但 failure 符合原计划
hard-failure branch：未产生任何授权外写入、外部访问或历史改写。不得现场 retry，也不得把已完成的前半检查拼接到 successor。

## Residual risks and exact next branch

- Successor 是新 contract，不是本失败执行的 retry；它只允许一次新的 validation-only attempt，仍保持 retry/fallback `0/0`。
- Controller shell 必须明确禁用 `path`、`PATH`、`cdpath`、`fpath`、`manpath` 等会影响 shell/command resolution 的变量名；固定
  path comparison 优先直接 argv，确需循环时仅用 `entry_path` 并声明为普通局部变量。
- Successor 必须从头重放全部 activation/topology/file/archive gates；不得消费本次前半检查作为通过证据。
- ER 仍只允许一次 EOF append；唯一 commit 仍只允许 `.agent-work/EXECUTION_RESULT.md`，原 P4-C1 rejection 不变。
- 任一新 gate 失败仍须 pre-write fail closed；不得增加第二次 attempt、修复旧 ER、运行测试或进入 external/retained 路线。
- Exact next branch：`REF-P7-25-R2-B2-P4-C1-C1-C1` controller-shell-only validation successor。

维护性判断：该分支只纠正一次性 validation controller 的 zsh 变量命名，不新增生产 owner、证据格式或执行框架。

---

## Reviewed active PLAN full text

以下保存 reviewed PLAN 的完整文本；上方 decision 与 successor branch 是本次 Planner 审核结论。

# REF-P7-25-R2-B2-P4-C1-C1：validation-only activation provenance closure

**计划状态：** `ACTIVE_EXECUTION_AUTHORIZED`

**Planner 日期：** `2026-07-31`

**Reference task：** `REF-P7-25-R2-B2-P4-C1-C1`

**Contract ID：**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-P4-C1-C1-VALIDATION-ONLY-PROVENANCE-CLOSURE-V1`

**当前唯一动作：** 只读重放冻结的 committed topology、最终两文件身份与 P4-C1 review archive；全部匹配后仅向
`.agent-work/EXECUTION_RESULT.md` 追加一次 truthful supersession record，并创建一个 exact-one-path focused evidence commit。

**唯一 Planner stop：**
`B2_P4_C1_C1_VALIDATION_ONLY_PROVENANCE_CLOSURE_WAITING_PLANNER_REVIEW`。

**本轮新归档：**
`.agent-work/PLANS/20260731-1332-p7-retained-r3-b2-p4-c1-c1-provenance-disposition-review.md`，
bytes `4204`，SHA-256 `fc5185b930a6c8b39151f5e0233ac156047ac513520dd3bd977000353f14999f`；activation blob
由 Planner 在 commit 后交接，Executer 必须从该 commit 只读验证，不得修改。

`PLAN_MACHINE_CONTRACT={"schema":"p7_td_b_retained_r3_option_b_b2_p4_c1_c1_validation_only_provenance_closure_v1","reference_task_id":"REF-P7-25-R2-B2-P4-C1-C1","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-P4-C1-C1-VALIDATION-ONLY-PROVENANCE-CLOSURE-V1","execution_authorized":true,"executer_dispatch_allowed":true,"validation_only":true,"activation_runtime_head_required":true,"activation_parent":"1e63d808af45424f51ff0784955c95eccf4c3230","activation_subject":"chore(plan): activate p4 provenance closure","activation_changed_paths":[".agent-work/PLAN.md",".agent-work/PLANS/20260731-1332-p7-retained-r3-b2-p4-c1-c1-provenance-disposition-review.md"],"activation_archive_path":".agent-work/PLANS/20260731-1332-p7-retained-r3-b2-p4-c1-c1-provenance-disposition-review.md","activation_archive_bytes":4204,"activation_archive_sha256":"fc5185b930a6c8b39151f5e0233ac156047ac513520dd3bd977000353f14999f","rejected_activation_commit":"48adfd669dc8d49fe11c983a4ca36e928bef6c22","implementation_commit":"0ec12f2de91b84f4379d64437170fa53c3ae4a28","misstated_evidence_commit":"bd9d205cf7a4385d202666f87d225739e57c970c","planner_rejection_commit":"dfc2ed4d646e7c1a284c075810ae1424a3272504","orchestrator_disposition_commit":"1e63d808af45424f51ff0784955c95eccf4c3230","implementation_source_blob":"1868ad4b4446defcc6d8187ea21d18ccf128fa31","implementation_source_sha256":"6e10594165016a06da462e74a9deb2d9817fd95fe1417addb7a5d26c55996745","implementation_test_blob":"25eafb91d7794d4510c9d7da34f1d8666ab1ff55","implementation_test_sha256":"e3c4a421e691c3aaac182edc6a0963a16caea95ae04f25a68493f96277bddb72","review_archive_path":".agent-work/PLANS/20260731-1326-p7-retained-r3-b2-p4-c1-transport-domain-owner-correction-review.md","review_archive_blob":"ab3bf85d9365ec34834f66dd1aabbc5d4bc7c6bd","review_archive_bytes":21675,"review_archive_sha256":"d4c82e8479668db8bfce750e2f851bf8486db24f2c2c510ae56d00735e5997fd","allowed_write_path":".agent-work/EXECUTION_RESULT.md","required_evidence_subject":"chore(evidence): supersede p4 activation subject claim","required_evidence_changed_paths":[".agent-work/EXECUTION_RESULT.md"],"implementation_original_contract_status":"REJECTED_ACTIVATION_SUBJECT_AND_ER_PROVENANCE_MISMATCH","retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","planner_stop":"B2_P4_C1_C1_VALIDATION_ONLY_PROVENANCE_CLOSURE_WAITING_PLANNER_REVIEW","zero_budgets":{"code_writes":0,"test_writes":0,"old_execution_result_line_changes":0,"full_plan_writes":0,"plan_writes":0,"archive_writes":0,"debug_writes":0,"guide_writes":0,"research_writes":0,"tests":0,"compileall":0,"codegraph":0,"external_controller_writes":0,"external_controller_reads":0,"external_root_creates":0,"external_root_reads":0,"synthetic_integration_runs":0,"retained_artifact_reads":0,"real_b2_dispatch":0,"actual_canonical_validator_calls":0,"eligibility_emissions":0,"release_operations":0,"network":0,"dns":0,"environment":0,"credentials":0,"device":0,"camera":0,"ray":0,"strip":0,"cleanup":0,"capture":0,"formal":0,"public_analyzer":0,"td_c":0,"sentinel":0,"p8":0,"firmware":0,"deployment":0}}`

## 1. 冻结输入与 activation gate

Executer 开始时工作区必须 clean，runtime `HEAD` 即本 Planner activation commit。其 full SHA 可在运行时捕获，但必须同时满足：

- direct parent：`1e63d808af45424f51ff0784955c95eccf4c3230`；
- subject：`chore(plan): activate p4 provenance closure`；
- exact changed-path set（按字节排序比较）：
  - `.agent-work/PLAN.md`；
  - `.agent-work/PLANS/20260731-1332-p7-retained-r3-b2-p4-c1-c1-provenance-disposition-review.md`；
- 本 PLAN 的 machine contract 可 strict JSON 解析，且只包含一个 active executable package；
- FULL 必须仍由 Orchestrator-owned commit `1e63d808...` 提供本 reference 的
  `READY_FOR_PLANNING_VALIDATION_ONLY_SUCCESSOR` 路线；Executer 不得写 FULL。

任何 activation 条件不匹配：在 ER 写入、stage、commit 前 hard fail，并只向 Planner/Orchestrator 报告，不允许现场修复、retry
或 fallback。

## 2. 冻结 committed topology

使用 read-only Git plumbing 逐项验证 full commit、direct parent、exact subject 和 exact changed-path set：

| Role | Commit | Parent | Exact subject | Exact changed paths |
| --- | --- | --- | --- | --- |
| rejected activation | `48adfd669dc8d49fe11c983a4ca36e928bef6c22` | `781e410c43774c20da9f00e8c9e0f5bfd27b1f66` | `chore(plan): activate p4 transport domain correction` | `.agent-work/FULL_PLAN_REFERENCE.md`; `.agent-work/PLAN.md`; `.agent-work/PLANS/20260731-1308-p7-retained-r3-b2-p4-i1-c1-c1-fixture-classification-failure-review.md` |
| retained implementation | `0ec12f2de91b84f4379d64437170fa53c3ae4a28` | `48adfd669dc8d49fe11c983a4ca36e928bef6c22` | `fix(p7): own retained controller transport domains` | `src/camera_based_rgbww_optimizer/utils/p7_retained_r3_controller_conformance.py`; `tests/test_p7_retained_r3_controller_conformance.py` |
| misstated evidence prerequisite | `bd9d205cf7a4385d202666f87d225739e57c970c` | `0ec12f2de91b84f4379d64437170fa53c3ae4a28` | `chore(evidence): record p4 transport domain correction` | `.agent-work/EXECUTION_RESULT.md` |
| Planner rejection | `dfc2ed4d646e7c1a284c075810ae1424a3272504` | `bd9d205cf7a4385d202666f87d225739e57c970c` | `chore(plan): reject p4 activation provenance mismatch` | `.agent-work/PLAN.md`; `.agent-work/PLANS/20260731-1326-p7-retained-r3-b2-p4-c1-transport-domain-owner-correction-review.md` |
| Orchestrator disposition | `1e63d808af45424f51ff0784955c95eccf4c3230` | `dfc2ed4d646e7c1a284c075810ae1424a3272504` | `docs(orchestration): route p4 provenance successor` | `.agent-work/FULL_PLAN_REFERENCE.md`; `.agent-work/debug/active/20260731-p7-retained-r3-b2-controller-contract-drift.md` |

还必须验证上述五个 full commits 都是 runtime activation HEAD 的 ancestors，且链路之间没有以缩写 SHA 代替 full SHA 的比较。
不得 amend、rebase、reset、cherry-pick、checkout 历史内容、重建或删除任何 commit。

## 3. 冻结 implementation 与 archive 身份

只读验证 `0ec12f2...` tree 和 runtime activation tree 中下列身份完全一致：

- Source：
  `src/camera_based_rgbww_optimizer/utils/p7_retained_r3_controller_conformance.py`，blob
  `1868ad4b4446defcc6d8187ea21d18ccf128fa31`，SHA-256
  `6e10594165016a06da462e74a9deb2d9817fd95fe1417addb7a5d26c55996745`；
- Dedicated test：
  `tests/test_p7_retained_r3_controller_conformance.py`，blob
  `25eafb91d7794d4510c9d7da34f1d8666ab1ff55`，SHA-256
  `e3c4a421e691c3aaac182edc6a0963a16caea95ae04f25a68493f96277bddb72`。

只读验证 P4-C1 review archive：

- path：`.agent-work/PLANS/20260731-1326-p7-retained-r3-b2-p4-c1-transport-domain-owner-correction-review.md`；
- commit `dfc2ed4...` 与 runtime activation tree blob 均为
  `ab3bf85d9365ec34834f66dd1aabbc5d4bc7c6bd`；
- bytes `21675`；SHA-256
  `d4c82e8479668db8bfce750e2f851bf8486db24f2c2c510ae56d00735e5997fd`。

禁止读取 external controller/source/root、失败 external evidence、accepted-C1、retained R3/candidate 或 release。禁止运行测试、
compileall、CodeGraph、synthetic integration、validator 或 analyzer。任一身份不匹配都在写入前 hard fail。

## 4. 唯一允许的 ER append

前三节全部通过后，Executer 只可在 `.agent-work/EXECUTION_RESULT.md` EOF 追加一次新 section；必须保留所有旧 bytes，
不得修改、删除、格式化或“修正”旧行。新 section 必须明确包含：

1. contract/reference/stop，以及 runtime activation full SHA、parent、subject、exact two docs paths；
2. `bd9d205...` 的旧错误字段是 activation subject / activation-gate assertion：旧记录写成
   `chore(plan): activate p4 transport domain owner correction`，真实值是
   `chore(plan): activate p4 transport domain correction`；
3. supersession exact scope：只取代该错误 subject、由其导出的 “activation gate passed” assertion，以及由此导出的
   `repo_transport_owner_correction_pass_waiting_for_planner` disposition；旧记录中的 implementation identity 与已记录 validation
   observations 不被本包重新执行、重新认证或整体删除；
4. 原 P4-C1 contract 保持
   `REJECTED_ACTIVATION_SUBJECT_AND_ER_PROVENANCE_MISMATCH`，不得改称 accepted/pass；
5. 本包只证明 non-rewritten Git/file/archive provenance closure。它不证明 scientific correctness，不消费 retained R3，不调用
   canonical validator，不产生 eligibility/release/device/formal authority；
6. 五个 frozen topology roles、最终 source/test blob+SHA、archive blob/bytes/SHA 全部匹配；
7. 所有 hard locks 和零预算保持 `0`；写入次数 `1`、retry/fallback `0/0`。

Append 前后必须以 bytes/hash 证明 preexisting ER prefix 完全相同，且新内容只有一个 section。不得用脚本生成、修复或改写旧 payload；
允许用 `apply_patch` 做唯一 EOF append。

## 5. Exact-one-path evidence commit

Append 后按顺序执行：

1. 验证 `git diff --check` 通过；
2. 验证 unstaged/staged changed-path union exact
   `.agent-work/EXECUTION_RESULT.md`，并再次验证 old ER prefix 不变；
3. 只 stage `.agent-work/EXECUTION_RESULT.md`；
4. 创建唯一 commit，direct parent 必须是 runtime activation full SHA，subject exact
   `chore(evidence): supersede p4 activation subject claim`；
5. postcommit 只读验证 exact changed paths 仍只有 `.agent-work/EXECUTION_RESULT.md`，工作区 clean，commit parent/subject/path
   与本合同一致；
6. 不运行任何 postcommit tests、compileall、CodeGraph 或外部命令。

Evidence commit body 应说明它只追加 truthful supersession record，保留 P4-C1 rejection，不改 implementation 或历史记录。

## 6. Budgets、failure branches 与验收

### Non-zero maximum budgets

- historical/activation Git identity inspection：每个冻结 commit/activation 所需 read-only plumbing 各最多 `1` 组；
- source/test/archive identity read：每个 exact path 每个所需 tree 最多 `1` 次；
- ER append：exact `1`；
- `git diff --check`：exact `1`；stage：exact `1`；evidence commit：exact `1`；
- postcommit Git/status verification：exact `1` 组；
- retry `0`，fallback `0`，alternate package `0`。

### Hard-failure branch

任何 pre-write gate 不匹配：不写 ER、不 stage、不 commit，记录只读观察并停止。任何 append 后/precommit gate 失败：不得修补旧 ER、
不得 commit；保留工作区供 Planner 审核并停止。Commit 或 postcommit identity 不匹配：不得 amend/reset/retry/追加第二记录；停止并交
Planner。所有 failure 都只允许 Planner/Orchestrator 后续规划 bounded offline evidence correction，禁止回到 code implementation 或外部 integration。

### Acceptance criteria

Planner 仅在以下全部成立时接受 C1-C1：

- activation、五个历史 commits、最终 source/test、P4-C1 archive 的所有冻结 identity 精确匹配；
- ER 原 bytes 完整保留，只新增一个满足第4节的 truthful supersession section；
- evidence commit direct parent/subject/path 精确，工作区 clean；
- 原 P4-C1 明确保留 rejected，implementation validation facts 没有被重解释为原合同通过；
- tests/compileall/CodeGraph/external/retained/validator/release/network/device/scientific预算全为 `0`；
- Executer 到唯一 stop，不进入 synthetic integration、retained audit、eligibility 或 release。

验收后 Planner 归档本包并只向 Orchestrator建议：把 C1-C1 标记
`ACCEPTED_VALIDATION_ONLY_PROVENANCE_CLOSURE`，保留 P4-C1 rejected 历史，允许 Orchestrator 决定下一个 repo-owned synthetic
integration package。该建议本身不授权后续工作。

## Hard locks

Code/test、旧 ER lines、FULL/PLAN/archive/debug/GUIDE/RESEARCH 写入全锁 `0`。Tests、compileall、CodeGraph、external
controller/source/root、synthetic integration、failed/accepted external evidence、retained R3/candidate、real B2、subordinate manifest、
canonical validator、eligibility、retained audit、release generation/qualification/copy/consumption、network/DNS/environment/credentials、
device/camera/Ray/strip/cleanup/capture/FORMAL/public analyzer/TD-C/sentinel/P8/firmware/deployment全锁 `0`。

维护性判断：该包只追加不可变 supersession evidence，不增加生产抽象、重复 classifier 或新 provenance owner。
