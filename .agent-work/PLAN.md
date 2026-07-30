# REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-9：exact governance successor implementation

**计划状态：** `DISPATCHABLE_AFTER_EXACT_PLAN_ONLY_ACTIVATION_COMMIT`

**Planner 日期：** `2026-07-30`

**Reference task：** `REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-9`

**Contract ID：** `P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F19-CORRECTIVE-9-GOVERNANCE-LINEAGE`

**唯一当前动作：** 在 exact PLAN-only activation commit 后，实现一个 repo-owned、append-only、validation-only 的
governance lineage successor manifest及fail-closed subordinate validator，提交唯一implementation commit，随后在fresh root运行
完整验证链并停在Planner验收门。不得执行candidate、retained R3、release、eligibility emission或任何设备/科学阶段。

**C8 review archive：**
`.agent-work/PLANS/20260729-2332-p7-retained-r3-option-b-b1a-c3e6f19-corrective-8-review.md`，SHA-256
`2a7891b73aa452ccde97a710a93f5b0ecbb2d669ab2056725bf819869c517b5b`。

`PLAN_MACHINE_CONTRACT={"schema":"f19_corrective_9_governance_lineage_successor_v1","reference_task_id":"REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-9","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F19-CORRECTIVE-9-GOVERNANCE-LINEAGE","dispatch_state":"dispatchable_after_exact_plan_only_activation_commit","single_current_action":"implement_commit_and_validate_exact_subordinate_governance_successor","activation":{"required_parent":"d12b0cec3b66afbf26eedadf34a938222b488a88","subject":"chore(plan): activate f19 governance lineage successor correction","changed_paths":[".agent-work/PLAN.md"],"commit_count":1,"initial_clean_required":true},"implementation":{"direct_parent":"exact_activation_child_at_dispatch","subject":"fix(p7): add exact governance lineage successor","commit_count":1,"changed_paths":["config/hsi/p7-governance-lineage-successor-v1.json","src/camera_based_rgbww_optimizer/optimization/p7_thermal_diagnostics.py","tests/test_p7_thermal_diagnostics.py"],"additional_paths":0,"baseline":{"config_state":"absent","source_blob":"ccb8558b585abcb5d6b439fabbbeb865949dda57","source_sha256":"61033c79e51a046ecce4f26b06bc2b10427350b10733967e72b109e506f835d9","test_blob":"16e91ee1e1fac64062c511b96f2f320b7ee6c806","test_sha256":"7ccc64a1f3182a0860b01dcc159f5b2ef505193fae9d2add41cbc161b49e5c7a"}},"historical_owner":{"commit":"3e2ebed132b6d4338bfa324bfc42c3565d2eeb3c","parent":"9303aa22a9bd37e8ec4f23147c78c6bea84b9a2e","changed_path_ledger_count":181,"changed_path_ledger_lf_sha256":"9596c3fa8aee58259aff13b44badcc7d448e0555c80f166b20706dcd1e321118","selected_path_count":2,"selected_order":[".agents/skills/camera-based-rgbww-optimizer/SKILL.md","AGENTS.md"],"selected_binary_diff_sha256":"5a6cd050cd1d096e0894508aec338f7249679810bea63626acdcff63df9d17c8"},"selected_entries":{".agents/skills/camera-based-rgbww-optimizer/SKILL.md":{"before_blob":"1f8bf2a7f568de77f0fa4290d18e300f0e48047e","after_blob":"4d7dfe66c73036cb87e199c322f9344863f8c64e","before_sha256":"c8dd57a23ad684b4f7001f342ed3413a1abf4349bc6aeb90dbee7f5158139607","after_sha256":"3a77c8a0f7b02b0c8b15d31b625273e88a0ee38fca5bb739dbdaaacb40dfe81e","binary_diff_sha256":"7127dfdfb608b7de284a181afcca704c36b107aa3859e2fecea059ae47af3049"},"AGENTS.md":{"before_blob":"440956792bf843c15b2f315e66e16826305d2154","after_blob":"58bfacb5fc46fcb42bf643d12974063533a684eb","before_sha256":"a035e6955ea113100031bf411f30abad3b84a9dd260fde848f1b1cfbd194c8a5","after_sha256":"604b10bedeac6c9285f6448f94323521bf021a58275cce84d64163e16a2f07a0","binary_diff_sha256":"5736f6992d6882b1012a26ae5123892674d1f88cde0fee6ad98a5d33f78f5066"}},"old_payloads":{"rewrite_count":0,"policy_freeze_sha256":"833b4229986dbe1e551cc4da36d2eeaeb7b55c6ae0bab34e887e7ee63cfe746b","workflow_manifest_sha256":"8f9189edfb1520be2e08913678d7e046b93cb0a3c42a0034331e16b39d982e94","public_default_manifest_sha256":"6915c68cbb9436a8aa96ee5384751be6f9405c6f5330d19112cab2b77e898cd3"},"owner_boundary":{"subordinate_validator_emits_eligibility":false,"canonical_candidate_builder":"build_td_b_setup_release_lineage_candidate","generic_path_allowlist":false,"old_payload_repair":false},"fresh_root_prefix":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b1a-c3e6f19-corrective-9-offline/","retry":0,"fallback":0,"locks":{"candidate":0,"retained_r3":0,"canonical_retained_validator":0,"eligibility_emission":0,"release":0,"network":0,"env":0,"device":0,"camera":0,"ray":0,"strip":0,"cleanup":0,"formal":0,"public_analyzer":0,"td_c":0,"sentinel":0,"p8":0},"retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","planner_stop":"F19_CORRECTIVE_9_TERMINAL_WAITING_PLANNER"}`

## 1. Activation gate

Orchestrator须从clean `d12b0cec3b66afbf26eedadf34a938222b488a88`创建且只创建一个PLAN-only activation commit：

- subject exact为`chore(plan): activate f19 governance lineage successor correction`；
- changed paths exact为`.agent-work/PLAN.md`；
- direct parent exact为`d12b0cec3b66afbf26eedadf34a938222b488a88`；
- commit后worktree必须clean；dispatch时HEAD必须是该activation child的完整40字符SHA。

Executer先验证上述commit、parent、subject、exact-one path及committed PLAN bytes等于worktree。任何不符在创建fresh root、编辑、测试、
stage或commit前hard-fail；仅向`EXECUTION_RESULT.md`追加一次失败记录后停止。

## 2. 冻结历史事实与owner边界

新successor只覆盖历史commit `3e2ebed132b6d4338bfa324bfc42c3565d2eeb3c`中两个selected治理路径；其direct parent
必须是`9303aa22a9bd37e8ec4f23147c78c6bea84b9a2e`。该commit不是two-path commit：Executer必须以raw stdout bytes运行
`git diff --name-only 9303aa22a9bd37e8ec4f23147c78c6bea84b9a2e 3e2ebed132b6d4338bfa324bfc42c3565d2eeb3c`，
证明LF终止ledger恰为181行、无空行/重复、SHA-256为
`9596c3fa8aee58259aff13b44badcc7d448e0555c80f166b20706dcd1e321118`。不得读取或分类其余179个路径的payload。

Selected ordered path set exact为：

1. `.agents/skills/camera-based-rgbww-optimizer/SKILL.md`
2. `AGENTS.md`

对每项以`git rev-parse commit:path`、`git show commit:path`及
`git diff --binary parent commit -- path`验证PLAN machine contract中的before/after blob、before/after SHA-256和single-path binary diff
SHA-256。两路径合并diff只允许运行
`git diff --binary parent commit -- .agents/skills/camera-based-rgbww-optimizer/SKILL.md AGENTS.md`，其SHA-256必须为
`5a6cd050cd1d096e0894508aec338f7249679810bea63626acdcff63df9d17c8`。当前working与dispatch checkpoint bytes必须分别等于
两个after SHA。禁止generic path search、allowlist、glob扩展、历史payload repair/regeneration或把commit其余179路径作为资格输入。

旧`TD_B_AGENTS_POLICY_FREEZE_*`、`TD_B_WORKFLOW_PATH_*`、`TD_B_PUBLIC_DEFAULT_SUCCESSOR_*`常量与其三个canonical payload
保持原owner/hash/语义；不得修改、再生成、复制或把旧current hash改成新hash。新层只解释3e2ebed之后的exact current owner。

## 3. Exact manifest与production接缝

只新增`config/hsi/p7-governance-lineage-successor-v1.json`。采用UTF-8 canonical JSON：`sort_keys=True`、
`separators=(",", ":")`、`ensure_ascii=False`、末尾单个LF。Top-level exact key set：

`schema,status,owner,scope,eligibility_owner,commit,parent_commit,changed_path_ledger,selected_path_count,selected_paths,selected_binary_diff_sha256,rollback,extra_paths,operation_counters`。

Exact值合同：

- `schema = p7_td_b_governance_lineage_successor_v1`，`status = pass`；
- `owner = subordinate_exact_governance_provenance_only`；
- `scope = validation_only_no_eligibility_emission`；
- `eligibility_owner = build_td_b_setup_release_lineage_candidate`；
- commit/parent为本PLAN冻结的3e2ebed/9303aa2；
- `changed_path_ledger` exact key set为`command,count,lf_sha256`，command为上述exact argv字符串数组，count `181`，hash为冻结值；
- `selected_path_count = 2`，`selected_paths`按上述lexical order排列，不得重复；
- 每个selected entry exact key set为
  `path,classification,scope,before_blob_oid,after_blob_oid,before_sha256,after_sha256,binary_diff_sha256,rollback,extra_paths`；
- 两项`classification = bounded_validation_or_documentation`；entry `scope = exact_authorized_governance_successor_only`；
- 每项rollback exact为`restore <path> from parent 9303aa22a9bd37e8ec4f23147c78c6bea84b9a2e without changing any other path`，
  `extra_paths=[]`；
- top-level rollback exact为`restore only the two selected parent blobs; do not alter the other 179 paths or any historical manifest`；
- top-level `extra_paths=[]`；`operation_counters` exact key set为
  `candidate_reads,retained_r3_reads,canonical_retained_validator_calls,eligibility_emissions,release_calls,network_calls,env_reads,device_calls,camera_calls,ray_calls,strip_calls,cleanup_calls,formal_calls,public_analyzer_calls,td_c_calls,sentinel_calls,p8_calls`，全部为整数0。

`p7_thermal_diagnostics.py`只新增该canonical repo manifest的path/hash常量和一个
`_validate_td_b_governance_lineage_successor` fail-closed subordinate validator。它验证regular non-symlink canonical owner、whole-file
hash、strict JSON key/type/value、full commit/parent、181-path raw ledger、exact selected set、两项blob/content/diff、combined diff、working及
checkpoint bytes；只返回固定two-path classification mapping，不生成candidate/release、不写文件、不emit eligibility。

现有canonical eligibility owner `build_td_b_setup_release_lineage_candidate`保持唯一。现有
`_validate_td_b_agents_policy_lineage`与`_validate_td_b_public_default_successor_lineage`继续完整验证历史payload，再仅对其各自重叠路径调用
新subordinate validator取得当前owner；不得跳过旧验证，不得让新validator拥有其他路径或新增generic classification。对未包含3e2ebed的
checkpoint继续使用历史owner并fail closed；对包含3e2ebed的checkpoint必须验证新层。不得修改其它production owner。

## 4. Exact三路径实现commit

Activation gate通过后，Executer创建一个fresh `0700` root（prefix如machine contract；若已存在即hard-fail，不得复用），然后只编辑：

- `config/hsi/p7-governance-lineage-successor-v1.json`（baseline absent）；
- `src/camera_based_rgbww_optimizer/optimization/p7_thermal_diagnostics.py`（baseline blob/SHA见machine contract）；
- `tests/test_p7_thermal_diagnostics.py`（baseline blob/SHA见machine contract）。

不得编辑AGENTS、project skill、旧manifest/config、F19 controller/helper/dedicated test、PLAN/FULL/archives。编辑后、commit前冻结三项
working SHA-256、before/after blob state及canonical
`git diff --binary <activation-child> -- <exact-three-paths>` SHA-256，证明`git diff --name-only` exact为上述三路径、additional=0。

随后只允许一个implementation commit，subject exact为`fix(p7): add exact governance lineage successor`，direct parent exact为dispatch
activation child，changed paths exact为三路径。Commit后验证child为full lowercase 40-char SHA、direct parent、subject、exact path set、
before/after blob、committed file SHA与committed canonical binary patch SHA均等于precommit freeze；任一不一致立即停，不得amend/retry。

## 5. Tests与negative matrix

Dedicated tests必须新增至少两个明确命名的case：

- `test_governance_lineage_successor_accepts_exact_authorized_history_and_preserves_canonical_owner`
- `test_governance_lineage_successor_fails_closed_on_exact_drift_without_widening`

Positive case必须证明：strict manifest、181 ledger、exact two selected entries、working/checkpoint bytes均通过；旧policy/workflow/public-default
payload仍被验证；`build_td_b_setup_release_lineage_candidate`仍是唯一产生planner-only candidate状态的owner；subordinate返回mapping中exact只有
两路径且没有eligibility/release字段。

Negative matrix至少逐项覆盖且每项必须有具体拒绝断言：canonical owner错位、missing/non-regular/symlink、whole-file hash drift、malformed JSON、
top-level missing/extra key、schema/status/owner/scope/eligibility owner drift、commit/parent drift、ledger argv/count/hash drift、selected count/order/
missing/extra/duplicate path、entry missing/extra key、classification/scope drift、before/after blob OID drift、before/after SHA drift、single/combined diff drift、
rollback drift、nonempty `extra_paths`、nonzero/wrong-type counter、invalid/abbreviated/non-descendant checkpoint、Git command failure、working bytes drift、
checkpoint bytes drift及第三路径widening。还须回归C8十个失败测试全部通过。

## 6. Fresh fail-fast validation与evidence

Implementation commit exact验证通过后，在同一fresh root中运行，每项最多一次，任一nonzero立即停止后续项；retry/fallback均为0：

1. `.venv/bin/python -m compileall -q src/camera_based_rgbww_optimizer/optimization/p7_thermal_diagnostics.py tests/test_p7_thermal_diagnostics.py`
2. targeted unittest：上述两个新case，加上C8十个失败case（均为
   `tests.test_p7_thermal_diagnostics.P7ThermalDiagnosticsTests.<method>` exact selector）。
3. focused unittest：`tests.test_p7_thermal_diagnostics`、`tests.test_agent_work_machine_contract`、
   `tests.test_p7_retained_r3_exact_five_controller`、`tests.test_p7_retained_release_audit`。
4. full unittest：`.venv/bin/python -m unittest discover -s tests -v`；必须exit 0，禁止以targeted/focused green覆盖。
5. `codegraph sync`；必须exit 0。
6. `git diff --check <activation-child>..HEAD`及`git diff --check`；两者均exit 0。

沿用C8已验收的single-fd日志owner：每个log以`O_WRONLY|O_CREAT|O_EXCL|O_NOFOLLOW`只open一次，stdout/stderr共用该fd，child后
flush/fsync/close再digest；禁止路径重开、second fd、shell redirection。所有artifact为regular non-symlink `0600`。Terminal strict JSON最后
exclusive-create/seal，记录activation/implementation完整Git topology、三路径pre/post identity、manifest schema/negative matrix、每条命令exact
argv/calls/exit/log bytes/SHA/mode、fail-fast、全部zero locks及retained状态。最后仅向`.agent-work/EXECUTION_RESULT.md`append一个record，
不得改旧ER；记录前worktree除ER外必须clean，记录后只允许ER dirty。

若完整链预计超过10分钟，须按AGENTS在Human可见macOS Terminal启动，并由Executer完成三次稀疏liveness检查后交Orchestrator安排automation；
否则可在当前执行环境完成。不得为规避此规则拆分或重跑。

## 7. 持续硬锁、验收与停止点

Candidate path probe/read/build、retained R3 path probe/read/copy/repair、canonical retained validator call、eligibility emission、release
qualification/generation/copy/consumption、network、`.env`、device、camera、Ray、strip、cleanup、FORMAL-R6、public analyzer、TD-C、sentinel、P8
全部为0。三个旧governance payload只允许现有测试/validator只读，不得修改、复制、重建。Retained R3保持
`RETAINED_UNVALIDATED_UNCONSUMED`。

成功仅表示C9 implementation及完整测试等待Planner验收，不授权release、R3或后续阶段。失败也不得重试、amend、fallback或自行改PLAN。

**Planner stop：** `F19_CORRECTIVE_9_TERMINAL_WAITING_PLANNER`。
