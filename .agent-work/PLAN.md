# REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-10：exact governance successor implementation and validation

**计划状态：** `DISPATCHABLE_AFTER_EXACT_PLAN_ONLY_ACTIVATION_COMMIT`

**Planner 日期：** `2026-07-30`

**Reference task：** `REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-10`

**Contract ID：** `P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F19-CORRECTIVE-10-GOVERNANCE-LINEAGE`

**唯一当前动作：** 从已保存但未验证的C9 config/source草稿出发，只在exact三路径内修正实现并补齐dedicated tests，创建唯一implementation commit，随后在brand-new root各运行一次完整验证链并停在Planner验收门。不得执行candidate、retained R3、canonical retained validator、eligibility、release或任何设备/科学阶段。

**C9 review archive：** `.agent-work/PLANS/20260729-2357-p7-retained-r3-option-b-b1a-c3e6f19-corrective-9-review.md`，SHA-256 `0463db1e302bb4a672845c8e98239aafc0a51928868dad734f69a2db11a47c3e`。

`PLAN_MACHINE_CONTRACT={"schema":"f19_corrective_10_governance_lineage_successor_v1","reference_task_id":"REF-P7-25-R2-B1A-C3E6F19-CORRECTIVE-10","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E6F19-CORRECTIVE-10-GOVERNANCE-LINEAGE","dispatch_state":"dispatchable_after_exact_plan_only_activation_commit","single_current_action":"correct_commit_and_validate_exact_subordinate_governance_successor","activation":{"required_parent":"6a912cb68f80ef701552d3c822e612aefa1fb75a","subject":"chore(plan): activate f19 governance successor validation","changed_paths":[".agent-work/PLAN.md"],"commit_count":1,"initial_clean_required":true},"preserved_draft":{"commit":"cc37da5664f50cdb5a2c7f3cc77b1f88728c4bf6","parent":"bc13f50dfab9c2724d883befb2988f11548ccbe6","subject":"chore(p7): preserve unvalidated governance successor draft","validation_claim":false},"implementation":{"direct_parent":"exact_activation_child_at_dispatch","subject":"fix(p7): validate exact governance lineage successor","commit_count":1,"changed_paths":["config/hsi/p7-governance-lineage-successor-v1.json","src/camera_based_rgbww_optimizer/optimization/p7_thermal_diagnostics.py","tests/test_p7_thermal_diagnostics.py"],"additional_paths":0,"baseline":{"config_blob":"46acad9b1992196cbcdb381718ea9b2dfda31e3b","config_bytes":2574,"config_sha256":"7ff96378e76c5b450c44db55d5b5eee922afe084bb0ea37d837a6f12db928795","source_blob":"6d274d59b60dcd38b26cb14d092bb7cd31d30d2e","source_bytes":191641,"source_sha256":"7030305c1a4b5e829fc8966880e80139a9e2a345453e7cf2766651c0039525f1","test_blob":"16e91ee1e1fac64062c511b96f2f320b7ee6c806","test_bytes":194978,"test_sha256":"7ccc64a1f3182a0860b01dcc159f5b2ef505193fae9d2add41cbc161b49e5c7a"}},"historical_owner":{"commit":"3e2ebed132b6d4338bfa324bfc42c3565d2eeb3c","parent":"9303aa22a9bd37e8ec4f23147c78c6bea84b9a2e","changed_path_ledger_count":181,"changed_path_ledger_lf_sha256":"9596c3fa8aee58259aff13b44badcc7d448e0555c80f166b20706dcd1e321118","selected_path_count":2,"selected_order":[".agents/skills/camera-based-rgbww-optimizer/SKILL.md","AGENTS.md"],"selected_binary_diff_sha256":"5a6cd050cd1d096e0894508aec338f7249679810bea63626acdcff63df9d17c8"},"old_payloads":{"rewrite_count":0,"policy_freeze_sha256":"833b4229986dbe1e551cc4da36d2eeaeb7b55c6ae0bab34e887e7ee63cfe746b","workflow_manifest_sha256":"8f9189edfb1520be2e08913678d7e046b93cb0a3c42a0034331e16b39d982e94","public_default_manifest_sha256":"6915c68cbb9436a8aa96ee5384751be6f9405c6f5330d19112cab2b77e898cd3"},"owner_boundary":{"subordinate_validator_emits_eligibility":false,"canonical_candidate_builder":"build_td_b_setup_release_lineage_candidate","generic_path_allowlist":false,"old_payload_repair":false},"fresh_root_prefix":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b1a-c3e6f19-corrective-10-offline/","formal_chain_invocations_per_item":1,"retry":0,"fallback":0,"locks":{"candidate":0,"retained_r3":0,"canonical_retained_validator":0,"eligibility_emission":0,"release":0,"network":0,"env":0,"device":0,"camera":0,"ray":0,"strip":0,"cleanup":0,"formal":0,"public_analyzer":0,"td_c":0,"sentinel":0,"p8":0},"retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","planner_stop":"F19_CORRECTIVE_10_TERMINAL_WAITING_PLANNER"}`

## 1. Activation与preserved baseline gate

Orchestrator须从clean HEAD `6a912cb68f80ef701552d3c822e612aefa1fb75a`创建且只创建一个PLAN-only activation commit：

- subject exact为`chore(plan): activate f19 governance successor validation`；
- changed path exact为`.agent-work/PLAN.md`，additional path为0；
- direct parent exact为上述HEAD；
- commit后worktree必须clean；dispatch时HEAD必须是该activation child的full lowercase 40-char SHA。

Executer在创建fresh root、编辑、测试、stage或commit前验证activation topology、committed PLAN bytes与worktree一致，并验证preserved draft commit `cc37da5664f50cdb5a2c7f3cc77b1f88728c4bf6`的parent、subject、exact two-path set以及machine contract冻结的config/source/test baseline identities。任一不符只向`EXECUTION_RESULT.md`追加一次失败记录并停止。

C9 root `/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b1a-c3e6f19-corrective-9-offline/20260730T001500Z`及其compile result均已消费，禁止读取、复用、补写、重建或计入C10。

## 2. 冻结历史owner与immutable payload

新successor只解释历史commit `3e2ebed132b6d4338bfa324bfc42c3565d2eeb3c`中两个selected治理路径；其direct parent必须是`9303aa22a9bd37e8ec4f23147c78c6bea84b9a2e`。Executer只可按machine contract对raw LF-terminated 181-path ledger及下列ordered exact set作验证，不得读取或分类其余179个payload：

1. `.agents/skills/camera-based-rgbww-optimizer/SKILL.md`；
2. `AGENTS.md`。

两项before/after blob、before/after bytes SHA、single-path binary diff SHA及combined binary diff SHA必须继续等于preserved config中的exact值；working与dispatch checkpoint bytes必须等于各自after SHA。禁止generic path search、glob allowlist、历史payload repair/regeneration或把其余179路径作为资格输入。

旧AGENTS policy freeze、workflow path manifest与public-default successor payload必须逐字节保持SHA `833b4229...46b`、`8f9189ed...2e94`、`6915c68c...cd3`，其既有canonical验证不能被跳过、替换或放宽。新层只能作为append-only subordinate provenance；canonical `build_td_b_setup_release_lineage_candidate`仍是唯一eligibility owner。

## 3. Exact implementation scope与语义要求

只允许修改并提交以下exact三路径，三者都必须出现在implementation commit中；不得把“草稿当前看似可用”解释为test-only scope：

1. `config/hsi/p7-governance-lineage-successor-v1.json`；
2. `src/camera_based_rgbww_optimizer/optimization/p7_thermal_diagnostics.py`；
3. `tests/test_p7_thermal_diagnostics.py`。

Config保持canonical UTF-8 JSON（sorted keys、compact separators、末尾单LF）及现有exact schema/value contract。Source可以在此三路径合同内修正preserved draft，但必须保证：

- manifest owner为canonical repo path，regular、non-symlink、whole-file exact hash；JSON必须fail closed拒绝malformed、duplicate key、missing/extra key、wrong type与non-finite值；
- 历史commit/parent、181-path raw ledger、exact two selected entries、before/after blob/content/diff、combined diff、working及checkpoint bytes均从Git/文件独立重算；
- subordinate validator只返回固定two-path classification mapping，不得生成candidate/release、写文件或emit eligibility；
- `_validate_td_b_agents_policy_lineage`与`_validate_td_b_public_default_successor_lineage`必须先保留并完成旧payload验证，再仅对checkpoint包含3e2ebed时消费新层的exact重叠owner；未包含时继续按历史owner fail closed；
- 不得新增generic classification/path allowlist，不得修改其他production owner。

## 4. Positive与完整negative matrix

Dedicated tests至少新增并精确命名：

- `test_governance_lineage_successor_accepts_exact_authorized_history_and_preserves_canonical_owner`；
- `test_governance_lineage_successor_fails_closed_on_exact_drift_without_widening`。

Positive case必须证明canonical manifest、181 ledger、two-entry exact set、working/checkpoint bytes和旧三payload验证均通过；subordinate返回exact two-path mapping且无eligibility/release字段；只有`build_td_b_setup_release_lineage_candidate`产生既有planner-only candidate状态。

Negative matrix须逐项有明确拒绝断言：owner错位；missing/non-regular/symlink；whole-file hash；malformed/duplicate-key/non-finite JSON；top-level missing/extra key；schema/status/owner/scope/eligibility-owner；commit/parent；ledger argv/count/hash；selected count/order/missing/extra/duplicate/third path；entry missing/extra key；classification/scope；before/after blob OID和SHA；single/combined diff；rollback；nonempty extra paths；counter missing/extra/nonzero/bool/wrong type；invalid/abbreviated/non-descendant checkpoint；Git command failure；working bytes；checkpoint bytes。测试还必须证明任何新层失败不会fallback到旧hash、跳过旧payload或扩大canonical eligibility owner。

## 5. Exact implementation commit

Activation gate通过后，Executer先创建brand-new mode `0700` root，prefix为machine contract所列；若路径已存在立即hard-fail，不得选择或复用C9 root。完成exact三路径编辑后，commit前冻结：三项working SHA-256、before/after blob、exact sorted changed paths和`git diff --binary <activation-child> -- <exact-three-paths>` SHA-256，并证明additional path为0。

随后只允许一个implementation commit：

- direct parent exact为activation child；
- subject exact为`fix(p7): validate exact governance lineage successor`；
- changed paths exact为上述三路径；
- commit count `1`，不得amend、rebase、第二commit或fallback。

Commit后独立验证child full SHA、parent、subject、exact path set、before/after blobs、committed file SHA和canonical binary patch SHA全部等于precommit freeze。任一不符立即停止。

## 6. Fresh one-shot validation与single-fd evidence

Implementation topology通过后，在同一brand-new root依次运行下列每项恰好一次，任一nonzero立即停止后续项；retry/fallback均为0：

1. `.venv/bin/python -m compileall -q src/camera_based_rgbww_optimizer/optimization/p7_thermal_diagnostics.py tests/test_p7_thermal_diagnostics.py`；
2. targeted unittest：上述两个新case，加上C8十个ambient-governance regression cases；
3. focused unittest：`tests.test_p7_thermal_diagnostics`、`tests.test_agent_work_machine_contract`、`tests.test_p7_retained_r3_exact_five_controller`、`tests.test_p7_retained_release_audit`；
4. `.venv/bin/python -m unittest discover -s tests -v`，必须exit 0；
5. `codegraph sync`，必须exit 0；
6. `git diff --check <activation-child>..HEAD`与`git diff --check`作为同一diff-check item，二者均须exit 0。

Targeted十个既有selector exact为：

- `test_agents_policy_lineage_rejects_wrong_bytes_owner_and_provenance`；
- `test_current_head_lineage_accepts_exact_human_policy_freeze`；
- `test_lineage_release_rebuilds_current_plan_and_reaches_formal_runner`；
- `test_lineage_release_rejects_candidate_and_resolved_plan_tampering`；
- `test_post_eq_policy_lineage_classifies_only_exact_accepted_paths`；
- `test_public_default_successor_lineage_layers_historical_and_current_owners`；
- `test_public_default_successor_manifest_fails_closed_on_exact_drift`；
- `test_qualification_evidence_adapter_is_release_isolated`；
- `test_qualification_evidence_adapter_rejects_preparation_drift`；
- `test_workflow_path_manifest_rejects_owner_hash_and_provenance_drift`。

所有test selector均须使用`tests.test_p7_thermal_diagnostics.P7ThermalDiagnosticsTests.<method>`。每个log由单一owner以`O_WRONLY|O_CREAT|O_EXCL|O_NOFOLLOW`只open一次，stdout/stderr共用同一fd，child后flush/fsync/close再digest；禁止预创建后重开、second fd或shell redirection。所有artifact必须regular、non-symlink、mode `0600`。Terminal strict JSON最后exclusive-create并seal，记录activation/implementation topology、三路径pre/post identities、manifest/negative matrix、每条命令exact argv/calls/exit/log bytes/SHA/mode、fail-fast状态、zero locks和retained状态。最后只向`.agent-work/EXECUTION_RESULT.md`append一次；append前除ER外worktree须clean，append后只允许ER dirty。

既有full suite约两分钟，当前不预计超过10分钟；若Executer重新估算会超过10分钟，则必须使用AGENTS规定的Human可见macOS Terminal、三次稀疏liveness与automation流程，不得拆分规避。

## 7. 持续硬锁与停止点

Candidate path probe/read/build、retained R3 path probe/read/copy/repair、canonical retained validator call、eligibility emission、release qualification/generation/copy/consumption、network、`.env`、device、camera、Ray、strip、cleanup、FORMAL-R6、public analyzer、TD-C、sentinel与P8全部为0。旧governance payload只允许现有tests/validator在本package内只读，不得修改、复制或重建。Retained R3保持`RETAINED_UNVALIDATED_UNCONSUMED`。

成功只表示C10 implementation及完整测试等待Planner验收，不授权R3、release或后续阶段。失败不得重试、amend、fallback或自行改PLAN。

**Planner stop：** `F19_CORRECTIVE_10_TERMINAL_WAITING_PLANNER`。
