# REF-G4-01-SUCCESSOR-LINEAGE：fresh successor release generation + validation

**计划状态：** `EXECUTABLE_PENDING_ORCHESTRATOR_ACTIVATION_PURE_OFFLINE_FRESH_RELEASE`

**Executable：** `true`（仅在Orchestrator按§2对齐FULL并提交activation后生效）

**Active task count：** `1`

**Active task：** `REF-G4-01-SUCCESSOR-LINEAGE`

**Reference goal：** `REF-G4-COMPLETE`

**唯一 Planner stop：** `RETURN_FOR_G4_01_FRESH_SUCCESSOR_RELEASE_REVIEW`

`PLAN_MACHINE_CONTRACT={"schema":"planner_execution_contract_v2","contract_id":"G4-SUCCESSOR-LINEAGE-FRESH-RELEASE-GENERATION-VALIDATION-V1","plan_status":"EXECUTABLE_PENDING_ORCHESTRATOR_ACTIVATION_PURE_OFFLINE_FRESH_RELEASE","executable":true,"active_task_count":1,"active_task":"REF-G4-01-SUCCESSOR-LINEAGE","reference_task_id":"REF-G4-01-SUCCESSOR-LINEAGE","reference_goal":"REF-G4-COMPLETE","reference_task_status":"ACTIVE_AFTER_ORCHESTRATOR_ACTIVATION_FRESH_RELEASE_GENERATION_VALIDATION","activation_state":"DRAFT_WAITING_ORCHESTRATOR_FULL_ALIGNMENT_AND_FOCUSED_COMMIT","verified_source_parent":"8b8f50c10dec5864c204e90d33cb39468b45ce51","activation_child_sha_recorded_in_plan":false,"activation_child_subject":"docs(plan): activate g4 fresh successor release","activation_changed_paths":[".agent-work/EXECUTION_RESULT.md",".agent-work/FULL_PLAN_REFERENCE.md",".agent-work/PLAN.md",".agent-work/archived/EXECUTION_RESULT-20260803-1041.md",".agent-work/archived/PLAN-20260803-1041.md"],"reviewed_plan_archive":{"path":".agent-work/archived/PLAN-20260803-1041.md","bytes":6744,"sha256":"31861823a47cb72812e371bc564a893985af5ca7c7634eb4c0ec08f7506ead82","source_body_bytes":5700,"source_body_sha256":"742f3d4e27e984b2dc635ecc6e56fec4cd3b967a8787523de298eed1cc562093"},"reviewed_execution_result_archive":{"path":".agent-work/archived/EXECUTION_RESULT-20260803-1041.md","bytes":2191,"sha256":"6781033283ad533f078fde23994bf8dbf9e5b1ddc5fff2efc195604ed18dbb2b","source_body_bytes":1149,"source_body_sha256":"caae77f59091a9a36a0077bb4b2b25e998f0fba5488d66154f21f5d92d74be23"},"accepted_owner_checkpoint":"2e8eeb59bac43bb437bbfcd3a266fca924e2ceae","single_current_action":"bind_the_activation_child_clean_source_and_exact_accepted_policy_eq_prerequisites_then_create_one_fresh_0700_evidence_family_and_use_the_repo_owned_successor_composer_once_with_public_final_strict_each_once","executor_repo_write_paths":[".agent-work/EXECUTION_RESULT.md"],"external_write_family_template":"/Volumes/4T/temp/rgbww-optimizer/g4-successor-lineage-<activation_head_12>-<utc_YYYYMMDDTHHMMSSZ>","bundle_direct_child_name":"release","family_root_acquisition_cap":1,"bundle_root_acquisition_cap":1,"production_build_inputs_invocation_cap":1,"production_compose_invocation_cap":1,"public_validator_invocation_cap":1,"final_validator_invocation_cap":1,"strict_validator_invocation_cap":1,"retry":0,"fallback":0,"repair":0,"alternate_root":0,"release_consumption":0,"retained_r3_access":0,"legacy_release_access":0,"other_external_experiment_payload_access":0,"full_suite_invocation_cap":0,"code_edits":0,"test_edits":0,"config_edits":0,"guide_edits":0,"research_edits":0,"plan_edits_by_executer":0,"full_edits_by_executer":0,"archive_edits_by_executer":0,"device_access":0,"network_access":0,"camera_access":0,"ray_access":0,"strip_access":0,"capture_access":0,"formal_r6_access":0,"td_c_access":0,"firmware_access":0,"deployment_access":0,"commit_by_executer":0,"eligibility":false,"release_consumable":false,"release_consumption_authorized":false,"retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","device_authorized":false,"formal_r6_authorized":false,"planner_stop":"RETURN_FOR_G4_01_FRESH_SUCCESSOR_RELEASE_REVIEW","future_reference_task":"REF-G4-01-SUCCESSOR-LINEAGE","future_stage_locked":true}`

## 1. 唯一动作与边界

本包只执行一次纯离线production successor composition：从activation后的live clean HEAD/tree取得source
identity，读取accepted state-C policy与accepted EQ-R6 root，通过repo-owned
`p7_successor_lineage`和`p7_retained_r3_provenance_io`生成一个fresh candidate lineage bundle，并在同一次
compose内使public/final/strict validator各运行exactly once。成功或失败均立即停回Planner。

本包仍属于同一个`REF-G4-01-SUCCESSOR-LINEAGE`，不得创建suffix、corrective task或新root family。它不消费
release、不设eligibility、不授权device/formal，也不恢复retained R3、legacy release、旧deep-corrective PLAN或
一次性external semantic controller。

Executer只可写：

```text
.agent-work/EXECUTION_RESULT.md
one fresh external evidence family from §4, including its production `release` child
```

PLAN、FULL、archive、source、tests、config、GUIDE、RESEARCH全部只读；Executer不得stage或commit。

## 2. Activation topology与archives

Orchestrator activation必须是下列verified parent的direct child：

```text
parent = 8b8f50c10dec5864c204e90d33cb39468b45ce51
subject = docs(plan): activate g4 fresh successor release
changed paths exact =
  .agent-work/EXECUTION_RESULT.md
  .agent-work/FULL_PLAN_REFERENCE.md
  .agent-work/PLAN.md
  .agent-work/archived/EXECUTION_RESULT-20260803-1041.md
  .agent-work/archived/PLAN-20260803-1041.md
```

Activation child SHA不得自嵌PLAN。Executer从live HEAD只读取得exact child SHA/tree，并在任何ER写入与external
root创建前证明：direct-child topology、subject/path set、branch `main`、worktree clean，以及repo-owned parser
给出PLAN/FULL contract ID一致、active count `1/1`、active task exact。

Reviewed archives：

- PLAN：`.agent-work/archived/PLAN-20260803-1041.md`，6744 bytes，SHA-256
  `31861823a47cb72812e371bc564a893985af5ca7c7634eb4c0ec08f7506ead82`；body replay 5700 bytes /
  `742f3d4e27e984b2dc635ecc6e56fec4cd3b967a8787523de298eed1cc562093`。
- ER：`.agent-work/archived/EXECUTION_RESULT-20260803-1041.md`，2191 bytes，SHA-256
  `6781033283ad533f078fde23994bf8dbf9e5b1ddc5fff2efc195604ed18dbb2b`；body replay 1149 bytes /
  `caae77f59091a9a36a0077bb4b2b25e998f0fba5488d66154f21f5d92d74be23`。

Archive identity、regular-file type、bytes/SHA、metadata与body replay任一不符即stop。

## 3. Frozen source、owner与accepted prerequisites

### 3.1 Source identity

Repo root exact：

```text
/Users/ibobby/Projects/WLED-RGBWW
```

`source_checkpoint`不得由Planner猜测；它必须是§2 verified activation direct-child live HEAD。调用
`provenance.read_git_source_identity(repo_root, source_checkpoint)`的production default必须证明：

```text
HEAD = checkpoint = activation child
tree = live activation tree
staged / unstaged / untracked = false / false / false
clean = true
```

因此Executer在`build_successor_lineage_inputs`完成之前不得写ER。若worktree不clean，停止；不得stash、reset、
clean、checkout、commit或绕过source owner。

Accepted owner checkpoint：

```text
2e8eeb59bac43bb437bbfcd3a266fca924e2ceae
```

Activation HEAD上的owner/test files必须与accepted checkpoint byte-exact：

| path | SHA-256 |
|---|---|
| `src/camera_based_rgbww_optimizer/optimization/p7_successor_lineage.py` | `a944cc8d6186f8659848e89f30388f4a5112e18ed2dc6ea6fa1aec50ff95ff33` |
| `src/camera_based_rgbww_optimizer/utils/p7_retained_r3_provenance_io.py` | `38a6a6c0402d08b8ba126e0e928fdd17244784c0fa9977c9955a3018bf6f3608` |
| `tests/test_p7_successor_lineage.py` | `bf2c3f36e5df7f78b4e607181bb8194bd6d589979ff9022af4060c69640780e4` |
| `tests/test_p7_retained_r3_provenance_io.py` | `21f47535106937f2f99acdece8b3fb5c6717e1f9900f974e60b0f744163d34c6` |

Production delegate hash：

```text
src/camera_based_rgbww_optimizer/optimization/p7_thermal_diagnostics.py
  14955da5f19e9cd73532910eee295aaaf612ec9a78559c99a51d38c239c674d1
```

GUIDE exact SHA-256：
`659152f6c0ae69c90c701de4e57c352d771e4f0bf75cf9410271ba0a94200e35`。

### 3.2 Accepted policy

```text
path = /Users/ibobby/Projects/WLED-RGBWW/config/hsi/p7-ray-td-b-exposure-policy-v2.json
bytes = 4065
SHA-256 = c9080d18571f617cb7d323ade843ff9c86bf92e3795d23e3999e26d413968681
```

必须由`provenance.read_exact_file`与`provenance.decode_strict_json_bytes`读取，并由production
`validate_td_b_exposure_policy_v2`验证。不得重新序列化policy作为input owner，也不得把pretty JSON误当canonical
JSON而拒绝。

Accepted post-EQ review：

```text
.agent-work/PLANS/20260727-2052-p7-post-eq-policy-c1e1-acceptance-review.md
bytes = 17030
SHA-256 = 6dd605a8d5f142d8fb50cc9a40020e6a816cc116581cccb414459f6c91cc1762
checkpoint = 161094ffa2bf1f84ed1fc787e708e8c3463f10db
```

### 3.3 Accepted EQ-R6 State C

```text
root = /Volumes/4T/temp/rgbww-optimizer/p7-td-b-exposure-qual-r6-f37517a-20260727T1928
accepted status = qualified_1_2500
selected shutter = 1/2500
manifest schema = planner_eq_family_manifest_v1
manifest payload bytes = 7980
manifest SHA-256 = 41136d0d1530163668e111b7a9213bb1b9df330d8a168b451c752e3e5dca28e9
candidate launch / candidate-2 / attempted / physical / accepted / retry = 1 / 0 / 4 / 4 / 4 / 0
```

Exact accepted archive：

```text
.agent-work/PLANS/20260727-2017-p7-eq-r6-qualified-1-2500-acceptance-review.md
bytes = 25296
SHA-256 = bf48528e826ba1fc8928f32acfd10e1cdcc08208a0adc8da8cc4d29f751203f7
```

Exact accepted owner artifact hashes remain frozen：

```text
run/outer-result.json = 20a4ee42c931e7df74b7fdd756eab3077530726e8ae5c03d3d48b45e8b562f0a
run/candidate-1-outer-terminal.json = 6401f0f162ce3efcd1ca6139e8394ed17411df7552fb1722e2db3eb7a8e4cd16
run/candidate-1/candidate-result.json = 7db4d60627c9a63304945664b4ba2e7918dafb12495f5fbf1d45500a46748612
run/candidate-1/terminal-seal.json = 8baa46bc6431e9e79c035a6f83954d810c25def2c8b662a761784fd1d81417a3
```

本包只允许production owner读取这个exact EQ root。先exactly once调用
`thermal.build_planner_eq_family_manifest(EQ_ROOT)`取得其`payload: bytes`；随后
`build_successor_lineage_inputs`内部exactly once调用production EQ audit。除此之外不得手工遍历、复制、修改或
读取其他external root。EQ before/after写次数必须为0。

## 4. 唯一fresh evidence family与preflight

Container exact：

```text
/Volumes/4T/temp/rgbww-optimizer
```

其当前mode为`0755`，因此不得伪装成`read_existing_root`要求的`0700` safe parent。Executer在activation intake
全通过后只采样一次UTC时间，并冻结：

```text
activation12 = live activation HEAD first 12 lowercase hex
timestamp = one sampled UTC YYYYMMDDTHHMMSSZ
family_name = g4-successor-lineage-<activation12>-<timestamp>
FAMILY_ROOT = /Volumes/4T/temp/rgbww-optimizer/<family_name>
BUNDLE_ROOT = <FAMILY_ROOT>/release
```

`family_name`必须匹配`g4-successor-lineage-[0-9a-f]{12}-[0-9]{8}T[0-9]{6}Z`。FAMILY_ROOT与
BUNDLE_ROOT在创建前必须都absent、non-symlink；不得预创建、删除、换名或搜索alternate。若碰撞即stop。

同一production invocation process先用`provenance.create_exclusive_root(FAMILY_ROOT)`exactly once创建mode
`0700`的唯一external evidence family，并取得其`DirectoryIdentity`；随后仅把该identity作为safe parent传给
`compose_successor_lineage_bundle(..., child_name="release")`。Compose通过
`create_exclusive_direct_child`exactly once创建BUNDLE_ROOT mode `0700`。FAMILY_ROOT是本包唯一external evidence
family；`release`只是其唯一production payload child，不是第二个平行release route。

创建前preflight必须在内存中完成且不得先写ER：

```text
activation/source/archives/owner files/policy/GUIDE hashes = exact
accepted EQ/post-EQ archive identities = exact
PLAN/FULL active contract = exact 1/1
retained R3 = RETAINED_UNVALIDATED_UNCONSUMED
eligibility/release consumable/device/formal = false
FAMILY_ROOT/BUNDLE_ROOT = absent non-symlink
forbidden old deep task, retained/legacy release input = 0
```

任一失败均在零root状态stop；之后才可把failure handoff写入ER。

## 5. Exact production invocation

使用`.venv/bin/python`在repo root运行一个foreground、无落盘source文件的thin invocation expression。它只负责
提供冻结参数、in-memory call counter、调用production APIs并把返回identity/status打印为operator evidence；
不得实现任何policy/EQ/release validation、canonical serialization、filesystem traversal或parallel semantic
owner。

Exact production sequence：

1. `manifest = thermal.build_planner_eq_family_manifest(EQ_ROOT)`；确认其payload type为exact `bytes`，metadata与
   §3.3 exact，且不另行手写manifest。
2. `inputs = successor.build_successor_lineage_inputs(...)` exactly once，参数exact：
   - `repo_root=/Users/ibobby/Projects/WLED-RGBWW`；
   - `source_checkpoint=<live activation HEAD>`；
   - policy path/SHA为§3.2；
   - EQ root为§3.3；
   - `eq_manifest_bytes=manifest["payload"]`；
   - `eq_manifest_sha256=41136...28e9`；
   - 全部owner/delegate保留production defaults，不注入fake、wrapper或custom validator。
3. `family = provenance.create_exclusive_root(FAMILY_ROOT)` exactly once。
4. 初始化in-memory counter exact `{"public":0,"final":0,"strict":0}`；callback只允许对应key各加1，其他key
   fail closed。
5. `bundle = successor.compose_successor_lineage_bundle(inputs, safe_parent=family,
   child_name="release", call_counter=counter)` exactly once；保留全部production defaults。
6. 调用返回后counter必须exact `{"public":1,"final":1,"strict":1}`。不得再次调用public、
   `replay_successor_lineage_bundle`或`strict_validate_successor_lineage_bundle`；compose内部的final/strict replay即
   本包唯一post-release replay。

Expected duration小于10分钟；不得使用background process、visible Terminal或automation。若实际达到10分钟仍未
terminal，停止Codex ownership并回Orchestrator按long-task规则处理，不得以后台process继续。

## 6. Success artifact与只读identity audit

Successful compose必须返回：

```text
bundle.root.path = <FAMILY_ROOT>/release
artifact count/order = exact 5 in production ARTIFACT_NAMES order
  frozen-inputs.json
  r6-formal-plan.json
  release-descriptor.json
  validation-summary.json
  terminal-seal.json
public_validation.status = public_descriptor_semantic_pass
final_replay.status = pass; artifact_count = 5
strict_validation.status = pass; artifact_count = 5
```

Post-compose只做一次non-semantic identity audit：以returned `DirectoryIdentity`与五个returned
`FileIdentity`调用repo-owned inventory/read owner，逐项证明direct child、regular non-symlink、root/file mode
`0700/0600`、path/order、bytes/SHA、same-target和canonical JSON decode。不得第二次调用三个validator，不得重写
artifact。

Cross-artifact/terminal contract必须已经由production final+strict同时证明：

```text
source HEAD/checkpoint/tree = activation live identity
policy path/bytes/SHA = §3.2 exact
EQ root/manifest bytes/SHA = §3.3 exact
R6 plan = selected_exposure_policy_non_executable
formal logical/physical = 16/16; retry = 0
old_new_frame_combination = prohibited
descriptor status = candidate_non_authorizing
terminal status = sealed_non_authorizing_pending_independent_replay
terminal references = exact first four artifacts; no terminal self-reference
artifact inventory = exact five; no extra/tmp
```

Authority invariant across descriptor/summary/terminal：

```text
retained_r3_status = RETAINED_UNVALIDATED_UNCONSUMED
release_consumable = false
release_consumption_authorized = false
eligibility = false
device_authorized = false
formal_r6_authorized = false
```

Returned final/strict `pass`只表示当前candidate bundle的离线identity/semantic replay通过，不得持久化或表达为
`release_usable`、`production_release_usable`、product readiness、hardware readiness、eligibility或formal pass。

## 7. Validation scope与failure convergence

Accepted owner validation按exact unchanged code/test identities继承：

```text
targeted = 45/45 PASS
focused/integration = 83/83 PASS
full suite = 844/844 PASS
compile/static/CodeGraph/diff scope = PASS
evidence = .agent-work/archived/{PLAN,EXECUTION_RESULT}-20260803-1033.md
```

本包对source/test/config零修改，故full suite/compile/CodeGraph sync invocation cap均为0；不得把外部release生成
误当作需要重复844 tests的code change。必须在production invocation前后分别证明accepted four owner/test paths相对
`2e8eeb59...`无diff，GUIDE/RESEARCH/PLAN/FULL在Executer运行中无未授权变化，并运行`git diff --check`。

Failure handling：

- source/policy/EQ manifest/accepted archive/history identity任一drift：fail closed，root未创建时保持0；记录
  exact owner error并停回Planner，归类为source/history contract stop，不现场修复或重新读取alternate evidence。
- family/root creation、persist、public/final/strict、identity audit任一failure：保留owner生成的root与truthful
  failure/pending seal，记录primary/seal error与已写artifact identities，停回Planner/Orchestrator做工程判断。
- 若出现GUIDE定义的scientific contradiction或无法选择科学分支，明确标记Advisor handoff candidate；不得由
  Executer猜测。普通serialization/persistence/provenance故障不是Advisor问题。

所有failure均：retry/fallback/repair/alternate root/second invocation=`0`。本PLAN不授权bounded correction；也不得
创建suffix task。

## 8. Absolute zero authority与handoff

```text
code/test/config/docs/skill/wrapper edits = 0
PLAN/FULL/archive/GUIDE/RESEARCH edits by Executer = 0
release consumption / retained R3 / legacy release = 0 / 0 / 0
device/network/camera/Ray/strip/capture/cleanup = 0
formal R6 / public experiment analyzer / TD-C = 0
firmware/deployment = 0
commit/amend/stage/push = 0
```

Executer在source identity已由production owner成功绑定后，才把完整handoff写入live ER。至少记录：

```text
activation HEAD/tree/parent/subject/path set and clean-source evidence
PLAN/FULL parser values and archive replay identities
frozen owner/policy/EQ/accepted archive checks
sampled timestamp, FAMILY_ROOT/BUNDLE_ROOT, absent-before and root identities
production sequence counters and exact call counts
five artifact paths/bytes/SHA/modes/order
public/final/strict returned status and post-compose identity audit
source/policy/EQ/R6/cross-reference/terminal/authority invariants
inherited 844 evidence identity and no-rerun rationale
pre/post owner diff, git diff --check and changed-path classification
all zero/no-consumption/no-device counters
decision request = RETURN_FOR_G4_01_FRESH_SUCCESSOR_RELEASE_REVIEW
```

成功只请求Planner接受一个`G4-01 candidate_non_authorizing` release并决定同一task是否已满足GUIDE §6 lineage
release gate；它不自行解锁G4-02、predevice、E2、device或formal。随后stop。

## 9. 维护性判断

本包不修改代码，也不引入controller文件。Persistence/provenance/serialization继续由accepted repo-owned
`p7_successor_lineage`与`p7_retained_r3_provenance_io`单一owner负责；thin invocation仅搬运冻结参数与返回identity。
既有844/844与负向contract覆盖保持适用，无后续重构建议。
