# P7 retained-R3 Option B：R4 real self-check immutable preparation

**计划状态：** `WAITING_ORCHESTRATOR_ACTIVATION`

**Planner 日期：** `2026-08-01`

**Reference task：** `REF-P7-25-R2-B3-C3-C4-R4`

**Contract：** `P7-TD-B-RETAINED-R3-OPTION-B-B3-C3-C4-R4-REAL-SELF-CHECK-PREPARATION-V1`

**当前唯一动作：** 生成一个fresh、immutable、pure-offline的real retained-R3 self-check preparation package；只把已经验收的committed identities与未来R5 exact acquisition/stop contract冻结为canonical JSON及seal，不读取三组真实artifact，不调用self-check owner或validator。

**唯一 Planner stop：** `B3_C3_C4_R4_REAL_SELF_CHECK_PREPARATION_WAITING_PLANNER_REVIEW`。

**本轮新归档：** `.agent-work/PLANS/20260801-0955-p7-retained-r3-b3-c3-c4-r3-c1-r1-c1-sequence-correction-review.md`；bytes `4726`，SHA-256 `0f7d4042efe8333bd87166e1b90f1030968e64b08ea407a30cd8bc0938de5837`。

`PLAN_MACHINE_CONTRACT={"schema":"p7_td_b_retained_r3_option_b_b3_c3_c4_r4_real_self_check_preparation_v1","reference_task_id":"REF-P7-25-R2-B3-C3-C4-R4","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B3-C3-C4-R4-REAL-SELF-CHECK-PREPARATION-V1","accepted_predecessor":{"activation":"20f6c0e59131e5fba8b8f7e8f23c0ae209ead063","implementation":"b23b358fd6322372587db6faa24e852bc38c3172","evidence":"36ea02ad1993c34e119c6bb80e5a841c2e77b205","decision":"ACCEPTED_COMPLETE_SUBORDINATE_OWNER_ONLY_NO_ELIGIBILITY","owner_source_sha256":"f139b6e4071b7ec9f2658a4b60305894011c64764236b3f10610e7effc04ecd9","owner_test_sha256":"361a5c268aff07d0b50c8788a4eb8bc8af5b311e5c263697fad3f2a34d404508"},"activation_commit":{"expected_parent":"36ea02ad1993c34e119c6bb80e5a841c2e77b205","expected_subject":"chore(plan): prepare real manifest self-check","expected_changed_paths":[".agent-work/FULL_PLAN_REFERENCE.md",".agent-work/PLAN.md",".agent-work/PLANS/20260801-0955-p7-retained-r3-b3-c3-c4-r3-c1-r1-c1-sequence-correction-review.md"]},"preparation_output":{"source_path_template":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b3-real-self-check-prep-<activation_short12>-source.py","root_path_template":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b3-real-self-check-prep-<activation_short12>","root_mode":"0700","exact_files":[{"name":"real-self-check-preparation.json","mode":"0600"},{"name":"real-self-check-preparation.sha256.json","mode":"0600"}],"status":"prepared_not_executed","execution_authorized":false,"eligibility":false,"release_consumable":false},"frozen_real_sources":{"manifest_root":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-m1-r1-s2-s1-c1-e939b639f40e-output","manifest_files":[["execution-result-admission.json",65,"c43d97963373db7d61066de6ebb7e16e6d915281f1f30861f86e1bd6404d87e9"],["retained-r3-audit-provenance-manifest-v2.json",4651,"c3ac3bc712965e39453b32e8cde15ebc7e53dcc7e1a99f1ecb38177f65cadfaf"],["retained-r3-audit-provenance-manifest-v2.sha256.json",148,"3a5f5a4b2c7fa203cad63a90d36a0b43a0e519534cc7c202eeb9b56fcddbfbbc"],["terminal-evidence.json",52,"b438e5c7cac0ef434205c748a003596d740c155f8b0ff3fa06df5a16f4a17893"],["terminal-evidence.sha256.json",123,"d17c4836355406fba95bb2d564692a32ff4b94423ae69e4de8cfe4b542572d75"]],"c1_root":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b2-c1-path-owner-27aacbf-20260730T1547Z","c1_files":[["path-owner-index.json",12195,"b189117fdd0a9a65ca80660245ec84b7f2f533c3e496c96e76eb48a4666feb35"],["path-owner-index.sha256.json",682,"867d1ffad5bd29f24dc81b24a58ce66393dd688833d3a4516fe7f45ef50875e9"],["terminal-evidence.json",13455,"c21a691272ca7466271349daa5b10236c9f36dfeb481d592e9c368a87e7a4763"],["terminal-evidence.sha256.json",772,"4bfebf4ad40e8c2e65ad2470faaed184f21d39eda73c13e689b09769d280752f"]],"retained_root":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-lineage-release-r3/lineage-release-32b9e67-r2-20260727T2227/child-output/lineage-release-r3","retained_files":[["current-lineage-candidate.json",9819,"3a2ff5a2af200c55c925b954488c5c5dd31a35a481440d17dfcdd8b68419f2e0"],["resolved-formal-plan.json",15137,"cf7c78b6a6cfda4055d05f5e9bbe9914161213b380dc7736ee09e257dd45eb6b"],["setup-lineage-release.json",1567,"0bacf1878a97fcdc4436259e132e89f6e56611df6d7fb5d5a7da28f62c98ad3e"]]},"future_r5":{"owner_commit":"b23b358fd6322372587db6faa24e852bc38c3172","owner_exports":["RealManifestSelfCheckError","RealManifestGitFileBytes","RealManifestSelfCheckSpec","RealManifestSelfCheckReport","required_real_manifest_git_argv","run_real_manifest_self_check"],"owner_calls":1,"ordered_git_ledgers":18,"physical_groups":[["manifest",5],["c1",4],["retained",3]],"canonical_validator_calls":0,"eligibility_emissions":0,"release_consumption":0,"stop":"REAL_SELF_CHECK_WAITING_PLANNER_REVIEW"},"execution_budgets":{"committed_plan_reads":1,"committed_full_reads":1,"accepted_archive_reads":1,"execution_result_reads":0,"source_writes":1,"source_compile_checks":1,"source_invocations":1,"fresh_root_creations":1,"canonical_json_writes":2,"canonical_json_reloads":2,"source_identity_postchecks":1,"root_inventory_checks":1,"process_table_scans":1,"execution_result_tail_reads":1,"execution_result_apply_patch_appends":1,"execution_result_appends":1,"postappend_operations":0,"retry":0,"fallback":0},"zero_budgets":{"real_manifest_root_reads":0,"real_manifest_file_reads":0,"c1_root_reads":0,"c1_file_reads":0,"retained_root_reads":0,"retained_file_reads":0,"self_check_owner_calls":0,"git_acquisition_ledgers":0,"canonical_validator_calls":0,"eligibility_emissions":0,"release_consumption":0,"repository_code_writes":0,"repository_test_writes":0,"implementation_commits":0,"network":0,"device":0,"camera":0,"ray":0,"strip":0,"cleanup":0,"formal":0,"public_analyzer":0,"plan_writes_by_executer":0,"full_writes_by_executer":0,"archive_writes_by_executer":0},"required_full_machine_state":{"active_task_count":1,"active_task":"REF-P7-25-R2-B3-C3-C4-R4","active_plan_contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B3-C3-C4-R4-REAL-SELF-CHECK-PREPARATION-V1","retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","manifest_authority":"SUBORDINATE_EVIDENCE_ONLY_CANONICAL_VALIDATOR_SOLE_ELIGIBILITY_OWNER","real_self_check_owner_status":"ACCEPTED_NOT_EXECUTED_ON_REAL_ARTIFACTS","real_execution_status":"BLOCKED_ON_R4_ACCEPTANCE","device_authorized_by_this_file":false},"orchestrator_commit_after_handoff":{"owner":"ORCHESTRATOR","executer_must_not_commit":true,"expected_subject":"chore(evidence): record real self-check preparation","expected_changed_paths":[".agent-work/EXECUTION_RESULT.md"]},"authorization":{"classification":"PURE_OFFLINE_REAL_SELF_CHECK_PREPARATION_NO_REAL_ARTIFACT_READS","human_device_authorization_required":false,"advisor_scientific_decision_required":false},"expected_duration":"under_10_minutes","visible_terminal_required":false,"archive":{"path":".agent-work/PLANS/20260801-0955-p7-retained-r3-b3-c3-c4-r3-c1-r1-c1-sequence-correction-review.md","bytes":4726,"sha256":"0f7d4042efe8333bd87166e1b90f1030968e64b08ea407a30cd8bc0938de5837"},"planner_stop":"B3_C3_C4_R4_REAL_SELF_CHECK_PREPARATION_WAITING_PLANNER_REVIEW"}`

## 1. Activation与输入边界

Activation必须是evidence `36ea02ad...`的direct child，subject/path set exact。Executer只可读取activation中committed `PLAN.md`、`FULL_PLAN_REFERENCE.md`和本轮accepted archive各一次，以严格duplicate-free JSON提取machine contract与冻结值；不得读取ER，不得搜索其他archive、root或artifact。

若activation topology、machine row、accepted predecessor、exact paths或任何冻结值不一致，立即停止并handoff；不得自行修复、猜测、重新派生或扩大读取范围。

## 2. Fresh preparation source与输出

由activation full SHA前12位替换`<activation_short12>`。先对source path和root path各做一次exact absence gate；任一已存在即fail closed，不得复用、删除或改名。

只用一次`apply_patch`在source path创建mode `0600`的standalone Python controller。controller只能导入stdlib与现有P3 provenance I/O owner；不得导入或调用real self-check owner、canonical validator、release、device/control模块，不得包含网络、subprocess或shell surface。

controller必须：

1. 用P3 exclusive-root owner创建fresh mode `0700` root。
2. 将machine contract中的accepted predecessor、三组exact roots/file `(name,bytes,SHA-256)`、未来R5 owner/18-ledger/order/stop contract及所有locks原样写入`real-self-check-preparation.json`。字段必须显式包含`status=prepared_not_executed`、`execution_authorized=false`、`eligibility=false`、`release_consumable=false`、`canonical_validator_sole_eligibility_owner=true`。
3. 用P3 canonical exclusive writer写主文件及seal；seal只绑定target basename、exact bytes、SHA-256。两文件mode均`0600`。
4. 不得stat/open/read三组external roots或其12个files；路径只作为已冻结字符串进入payload。

source写后先compile一次，再执行一次。无retry/fallback。controller失败时保留source/fresh root及已落盘证据，停止；不得repair或重跑。

## 3. Terminal audit

成功后独立只读复核：source path/mode/bytes/SHA在执行前后不变；root absolute、mode `0700`且exact two regular non-symlink files；两文件mode `0600`；strict decode、canonical re-encode、seal target/bytes/SHA、machine-contract semantic equality全部通过。

复核payload必须确认：只冻结12个external artifact identities但实际external root/file reads全部0；future R5 owner call和18条Git ledger均只是计划值，actual均0；eligibility/release/device locks为false/0。process scan一次且owned process为0。

不得运行unit/full tests或CodeGraph；本包不改repository code/test。不得commit；由Orchestrator在handoff后只提交ER evidence。

## 4. Handoff与停止

ER tail只读一次，以当前physical EOF完整block为anchor，一次`apply_patch`追加一个heading和一个strict duplicate-free canonical JSON block，必须记录activation、source identity、root/file identities、main/seal decode与re-encode结果、actual budgets、locks、first failure（若有）及planner stop。append必须为最后副作用，append后operations `0`。

成功只证明R5执行合同已被不可变冻结；不证明manifest facts、retained R3或lineage eligibility。等待Planner验收R4。只有R4被接受后，Planner才可另行编写一次独立pure-offline R5 real self-check execution；canonical validator、release consumption及设备工作仍保持锁定。

维护性判断：本包只建立一次性sealed execution spec，复用P3唯一持久化owner；不新增生产抽象、平行validator或权限面，并把真实artifact读取留给独立后继验收包。
