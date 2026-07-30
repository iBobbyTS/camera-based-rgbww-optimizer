# REF-P7-25-R2-B1A-C3E6F19：Repo-owned exact-five controller preparation

**计划状态：** `ACTIVE_EXECUTABLE_PACKAGE`

**Planner 日期：** `2026-07-30`

**Reference task：** `REF-P7-25-R2-B1A-C3E6F19`

**Contract ID：** `P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F19-CONTROLLER-PREPARATION`

**唯一动作：** 实现并离线验证一个 repo-owned、single-process、callback-driven 的 exact-five controller owner；本包不运行真实 controller，不读取 candidate 或 retained R3。

**Accepted prerequisite archive：** `.agent-work/PLANS/20260730-0247-p7-retained-r3-option-b-b1a-c3e6f18-corrective-1-review.md`；SHA-256 `ff5e2039f672fe13334c934a57c259658bcf4225c7ce39703eb298d0a6b2e2e5`。

`PLAN_MACHINE_CONTRACT={"schema":"f19_controller_preparation_plan_v1","reference_task_id":"REF-P7-25-R2-B1A-C3E6F19","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F19-CONTROLLER-PREPARATION","expected_full_sha256":"05d9d3458d71a176ffd197aeb46fdf812a7b34e226ee62fc3aa5094d67f6adc6","activation_commit":{"expected_parent":"2457844a5f0f1c9c279348dd4d5b5e2c5b4f393b","expected_subject":"chore(plan): activate f19 controller preparation","expected_changed_paths":[".agent-work/PLAN.md"],"child_head_owner":"runtime_actual_full_sha","plan_sha_owner":"runtime_actual_head_blob_and_worktree_bytes","clean_porcelain_required":true},"accepted_bootstrap":{"container":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b1a-c3e6f18-offline","container_device":16777240,"container_inode":2172267,"container_mode":"0700","container_empty":true,"record":"/Volumes/4T/temp/rgbww-optimizer/c3e6f18-container-bootstrap.json","record_sha256":"56fb1c806db56ce7f68240c1a35b4443dc4c41806bd4bb3107e85a095a8ecf97","seal":"/Volumes/4T/temp/rgbww-optimizer/c3e6f18-container-bootstrap.seal.json","seal_sha256":"568a32cab44be41322f51be3e812a044e3976c7689a2ffd8b49fad2ab379cca4","fallback":"/Volumes/4T/temp/rgbww-optimizer/c3e6f18-container-bootstrap.fallback.json","fallback_required_absent":true},"candidate_contract":{"identity_sha256":"3c5847fcbe0af85833c901f6f01058d000a3cecdc0f84e6ae331ed24e138c225","identity_only_no_payload_read":true,"exact_entry_count":5,"actual_entry_binding_deferred":true},"repo_read_only_paths":[".agent-work/PLAN.md",".agent-work/FULL_PLAN_REFERENCE.md",".agent-work/EXECUTION_RESULT.md",".agent-work/PLANS/20260730-0247-p7-retained-r3-option-b-b1a-c3e6f18-corrective-1-review.md","AGENTS.md",".agents/skills/camera-based-rgbww-optimizer/SKILL.md","src/camera_based_rgbww_optimizer/utils/agent_work_machine_contract.py","tests/test_agent_work_machine_contract.py"],"repo_edit_paths":["src/camera_based_rgbww_optimizer/utils/p7_retained_r3_exact_five_controller.py","tests/test_p7_retained_r3_exact_five_controller.py"],"external_read_only_paths":["/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b1a-c3e6f18-offline","/Volumes/4T/temp/rgbww-optimizer/c3e6f18-container-bootstrap.json","/Volumes/4T/temp/rgbww-optimizer/c3e6f18-container-bootstrap.seal.json"],"external_lstat_only_paths":["/Volumes/4T/temp/rgbww-optimizer/c3e6f18-container-bootstrap.fallback.json"],"evidence_root":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b1a-c3e6f19-preparation-offline","evidence_root_required_absent":true,"controller_api":{"module":"camera_based_rgbww_optimizer.utils.p7_retained_r3_exact_five_controller","exports":["ExactFiveControllerError","ExactFiveCandidateEntry","ExactFiveControllerRequest","ExactFiveControllerCallbacks","PreparedExactFiveController","prepare_exact_five_controller","execute_prepared_exact_five_controller"],"direct_io":false,"direct_subprocess":false,"direct_git":false,"eligibility_owner":false,"canonical_validator_callback_required":true,"release_consumer_callback_present":false},"test_budgets":{"compileall":1,"targeted_unittest":1,"focused_unittest":1,"full_unittest":1,"codegraph_sync":1,"git_diff_check":1,"retry":0},"operation_budgets":{"python_controller_process":0,"candidate_payload_reads":0,"retained_r3_reads":0,"canonical_validator_calls":0,"eligibility_emissions":0,"manifest_writes":0,"commits":0,"stages":0,"release_calls":0,"network_calls":0,"env_reads":0,"device_calls":0,"camera_calls":0,"ray_calls":0,"strip_calls":0,"cleanup_calls":0,"formal_calls":0,"public_analyzer_calls":0},"execution_result_append_cap":1,"planner_stop":"F19_CONTROLLER_PREPARATION_TERMINAL_WAITING_PLANNER"}`

## 1. Dispatch gate

Orchestrator 提交本 PLAN 后才可 dispatch。Executer 首先只读验证：

1. runtime HEAD 的 direct parent、subject、changed paths分别等于machine contract；child HEAD用实际40-char SHA记录，不在 PLAN 中预猜；
2. HEAD blob中的 PLAN bytes与worktree bytes相同；FULL raw SHA等于冻结值；`git status --porcelain=v1`为空；
3. 使用已提交 `agent_work_machine_contract` helper各解析一次 PLAN/FULL，并确认 task/contract、active count `1`、`retained_r3_status=RETAINED_UNVALIDATED_UNCONSUMED`、candidate identity与verified flag；
4. 只读重放 accepted archive、bootstrap record/seal及其hash/binding；container必须仍为同device/inode、mode `0700`、empty；fallback仅 `lstat` 且必须absent；
5. 两个repo edit paths与fixed evidence root必须absent。

任一不符：不创建evidence root、不编辑source/test、不运行tests；仅向 `EXECUTION_RESULT.md` append一次精确FAIL并停。不得修补、重试、换路径或放宽predicate。

## 2. Exact implementation scope

只允许新建以下两个repository paths，不得修改任何既有production/test/doc/skill/wrapper/plan/reference/archive：

- `src/camera_based_rgbww_optimizer/utils/p7_retained_r3_exact_five_controller.py`
- `tests/test_p7_retained_r3_exact_five_controller.py`

新module是 orchestration state owner，不是新的validator、release consumer或filesystem/Git adapter。它只能依赖Python stdlib与现有 `agent_work_machine_contract` helper；不得import设备、camera、Ray、measurement、public analyzer或release writer。不得调用 `open`/`Path.read_*`/`Path.write_*`、`os.*` filesystem mutator、`subprocess`或Git；真实I/O全部由未来package显式注入callback。本包只以fake callbacks执行其单元测试。

必须提供machine contract中列出的七个public exports，语义如下：

- `ExactFiveCandidateEntry`：冻结单一相对repo path、expected bytes SHA-256与after blob OID；拒绝绝对路径、`.`/`..`、反斜杠、glob/metacharacter、空path、重复或非小写hex。
- `ExactFiveControllerRequest`：只接受**恰好五条**、按UTF-8 byte order严格排序且唯一的entry tuple；绑定parent、expected subject、candidate identity、bootstrap record/seal identity、test argv和subordinate-manifest schema。不得接受generic allowlist或第六路径。
- `ExactFiveControllerCallbacks`：只定义 acquisition、materialize-one-entry、import/static gate、targeted/focused/full gate、single commit、subordinate manifest seal、canonical validator及terminal seal的窄callback；不得定义release consumer、eligibility emitter、network/device callback。
- `prepare_exact_five_controller`：纯验证阶段；验证request和PLAN/FULL parsed mappings，返回immutable `PreparedExactFiveController`。不得调用任何callback。
- `execute_prepared_exact_five_controller`：只运行已prepare object；顺序固定为 acquire once → materialize exactly five → gates → single commit → subordinate manifest seal → existing canonical validator exactly once → terminal seal。任何异常或non-pass均fail closed，terminal seal最多一次，后续callback为0，retry/fallback/repair/alternate path为0。

canonical validator callback仍是唯一eligibility owner。controller只能保存callback的原始pass/fail结果及调用次数；不得产生、推导或覆写 `eligibility=true`，不得把subordinate manifest当作授权。当前F19真实调用此API、真实candidate entries、canonical validator、commit和manifest均为0。

## 3. Dedicated regression contract

Dedicated tests至少覆盖：

1. valid synthetic exact-five prepare及完整fake callback顺序；
2. 4条、6条、重复、乱序、绝对/traversal/glob path、坏SHA/OID逐项fail closed；
3. PLAN/FULL task、contract、candidate identity或retained status drift在任何callback前拒绝；
4. prepare阶段callback调用严格为0；
5. 每个execution phase的exception与non-pass matrix：terminal seal一次、后继call 0、retry 0；
6. materialize恰好5次且每条只一次；targeted/focused/full各最多一次；commit/manifest/canonical-validator各最多一次；
7. canonical validator缺失、抛异常或non-pass不能成为成功；
8. callback protocol中不存在consumer/eligibility/network/device成员；
9. module AST/bytecode静态证明无direct filesystem/subprocess/Git/device/release import或调用；
10. terminal success只在canonical validator pass之后，且payload不含controller-owned eligibility授权。

执行预算（均一次、retry 0）：

```text
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m compileall -q \
  src/camera_based_rgbww_optimizer/utils/p7_retained_r3_exact_five_controller.py \
  tests/test_p7_retained_r3_exact_five_controller.py

PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m unittest -v \
  tests.test_p7_retained_r3_exact_five_controller

PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m unittest -v \
  tests.test_agent_work_machine_contract \
  tests.test_p7_retained_r3_exact_five_controller \
  tests.test_p7_retained_release_audit

PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m unittest discover -s tests -v

codegraph sync
git diff --check
```

任一命令nonzero立即停止，后续命令与任何Git mutation均为0；不得改测试来掩盖非F19 owner failure。

## 4. Evidence and terminal contract

通过dispatch gate后才允许exclusive-create fixed evidence root，mode `0700`。仅允许以下package-local artifacts，regular/non-symlink/mode `0600`、canonical strict JSON或raw log、不可覆盖：

```text
00-dispatch-and-bootstrap-replay.json
01-controller-source-identity.json
02-targeted.log
03-focused.log
04-full.log
05-codegraph-sync.log
06-validation-summary.json
07-terminal-summary.json
```

每个已开始阶段先持久化observed input/result，再判断pass/fail。Terminal必须绑定此前全部artifact path/bytes/SHA-256、source/test worktree SHA、exact diff path set、actual HEAD/parent/subject、PLAN/FULL/helper/bootstrap identities、command exit与test counts、callback matrix、zero-lock counters。terminal success只表示repo-owned controller preparation通过，不表示candidate、retained R3、manifest、validator、eligibility或release通过。

Executer最后只可向 `.agent-work/EXECUTION_RESULT.md` append一次摘要与terminal artifact SHA；不得编辑 PLAN/FULL/archive/GUIDE。source/test保留为未提交diff交Planner验收，stage/commit均为0。

## 5. Hard locks and branches

- 禁止读取或stat任何retained R3/candidate/release payload/path；candidate SHA只作opaque identity。
- 禁止真实controller execution、canonical validator、manifest、eligibility、consumer、release qualification/generation/copy/consumption。
- 禁止network、DNS、`.env`/credential、device、camera、Ray、strip、cleanup、capture、FORMAL-R6、public analyzer、TD-C、sentinel、P8、firmware或deployment。
- PASS：停止在Planner review；不自动commit、不进入B2。
- FAIL：保存truthful progressive/terminal evidence并停止；旧root/partial files不得reuse、repair、rewrite或retry。

**Planner stop：** `F19_CONTROLLER_PREPARATION_TERMINAL_WAITING_PLANNER`。

**维护性判断：** 本包以一个repo-owned纯callback状态机替代反复转录的临时controller；candidate facts、canonical eligibility和真实I/O仍由各自owner持有，新增范围仅一source一dedicated test，需在Planner验收后再决定是否提交与激活真实adapter。
