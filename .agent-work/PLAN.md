# P7 retained-R3 Option B：M1-R1-C1 Git/ER-only supersession

**计划状态：** `WAITING_ORCHESTRATOR_ACTIVATION`

**Planner 日期：** `2026-08-01`

**Reference task：** `REF-P7-25-R2-B2-M1-R1-C1`

**Contract：**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-M1-R1-C1-GIT-ER-ONLY-SUPERSESSION-V1`

**当前唯一动作：** Orchestrator先记录M1-R1 rejection并创建activation；Executer随后只使用Git与repository ER证据，向
`.agent-work/EXECUTION_RESULT.md` EOF append exact one immutable supersession record，纠正 canonical acceptance owner、已获得但未保留的
identity ledger、ER append计数和fresh probe超预算事实，然后停止。

**唯一 Planner stop：**
`B2_M1_R1_C1_GIT_ER_ONLY_SUPERSESSION_WAITING_PLANNER_REVIEW`。

**本轮新归档：**
`.agent-work/PLANS/20260801-0207-p7-retained-r3-b2-m1-r1-canonical-and-evidence-lifecycle-review.md`；bytes
`8493`，SHA-256 `5e557e1ea15d554c26e6924150abff647af8e6ffed9e9859577793734ad7671a`；不得覆盖earlier archives。

`PLAN_MACHINE_CONTRACT={"schema":"p7_td_b_retained_r3_option_b_b2_m1_r1_c1_git_er_only_supersession_v1","reference_task_id":"REF-P7-25-R2-B2-M1-R1-C1","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-M1-R1-C1-GIT-ER-ONLY-SUPERSESSION-V1","execution_authorized_after_orchestrator_activation":true,"activation_commit":{"expected_parent":"4720f9ac2588397c484c54a8685988d57e56b83e","expected_subject":"chore(plan): activate real manifest evidence supersession","expected_changed_paths":[".agent-work/FULL_PLAN_REFERENCE.md",".agent-work/PLAN.md",".agent-work/PLANS/20260801-0207-p7-retained-r3-b2-m1-r1-canonical-and-evidence-lifecycle-review.md"],"clean_porcelain_required_after_activation":true},"reviewed_failure":{"activation":"2b3b58f02656609525c511853547dc51d63559c8","evidence_commit":"4720f9ac2588397c484c54a8685988d57e56b83e","evidence_parent":"2b3b58f02656609525c511853547dc51d63559c8","evidence_subject":"chore(evidence): record real input manifest canonical stop","evidence_changed_paths":[".agent-work/EXECUTION_RESULT.md"],"reviewed_plan_bytes":18346,"reviewed_plan_sha256":"b4f54398ab0e7eabe6f7aa6a8249577a13bfa3a781421fbdae9ec77a87c425bd","er_blob":"fca8bd45135ec4f22cf18bd66c7d990edb13f024","er_bytes":1231056,"er_sha256":"21da0337a25def9ef02a8bb718e5415c0daae01feae9fa6eb4674c2e03e563f6","result":"REJECTED_REAL_INPUT_CANONICAL_ACCEPTANCE_AND_EVIDENCE_LIFECYCLE","first_failure_type":"ProvenanceIOError","first_failure_message":"json_not_canonical","successful_file_reads":5,"preserved_file_identity_rows":0,"reported_er_appends":0,"actual_er_appends":1,"budgeted_fresh_probes":2,"actual_fresh_probes":4},"retained_contract":{"status":"RETAINED_UNVALIDATED_UNCONSUMED","first_name":"current-lineage-candidate.json","first_bytes":9819,"first_sha256":"3a2ff5a2af200c55c925b954488c5c5dd31a35a481440d17dfcdd8b68419f2e0","acceptance":"OPAQUE_EXACT_PHYSICAL_IDENTITY_PLUS_STRICT_JSON","strict_json_requirements":["utf8","object_root","duplicate_keys_rejected","nonfinite_rejected"],"canonical_reencode_required":false,"schema_validation":false,"scientific_validation":false,"eligibility":false,"release_consumable":false,"mutation":false},"canonical_contract":{"c1_input_count":4,"c1_inputs_canonical":true,"new_output_count":5,"new_outputs_canonical":true,"retained_inputs_canonical":false,"canonical_validator_remains_sole_eligibility_owner":true},"required_full_machine_state":{"active_task_count":1,"active_task":"REF-P7-25-R2-B2-M1-R1-C1","active_plan_contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-M1-R1-C1-GIT-ER-ONLY-SUPERSESSION-V1","retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","real_manifest_domain_owner_status":"ACCEPTED_COMPLETE_GIT_GRAMMAR_VALIDATED","m1_real_manifest_candidate_commit":"0f4c09e1b2b2afbf627f6f36d57a1a65847ab4a8","m1_real_manifest_candidate_consumable":true,"m1_synthetic_integration_status":"ACCEPTED_COMPLETE_QUALIFIED_NOT_RETAINED_ELIGIBLE","m1_real_input_manifest_status":"REJECTED_CANONICAL_ACCEPTANCE_AND_EVIDENCE_LIFECYCLE","m1_real_input_supersession_status":"ACTIVE_GIT_ER_ONLY","existing_root_identity_owner_status":"ACCEPTED_COMPLETE_COMPOSITE_VALIDATED","executer_dispatched":true,"device_authorized_by_this_file":false},"exact_write_paths":[".agent-work/EXECUTION_RESULT.md"],"execution_budgets":{"git_read_only_commands":12,"repository_file_reads":4,"execution_result_appends":1,"postappend_repository_checks":3,"tests":0,"compileall":0,"codegraph_sync":0,"codegraph_queries":0,"implementation_commits":0,"external_path_operations":0,"retry":0,"fallback":0},"zero_budgets":{"repository_code_writes":0,"repository_test_writes":0,"plan_writes_by_executer":0,"full_writes_by_executer":0,"archive_writes_by_executer":0,"debug_writes":0,"guide_writes":0,"research_writes":0,"external_path_reads":0,"external_path_stats":0,"external_path_lists":0,"external_path_globs":0,"external_path_searches":0,"external_path_writes":0,"failed_fresh_namespace_reuse":0,"retained_artifact_reads":0,"retained_artifact_writes":0,"c1_external_evidence_reads":0,"accepted_synthetic_external_evidence_reads":0,"builder_calls":0,"runtime_calls":0,"controller_processes":0,"fresh_absence_or_presence_probes":0,"actual_canonical_validator_calls":0,"canonical_validator_callbacks":0,"eligibility_emissions":0,"retained_release_audit":0,"release_generation":0,"release_qualification":0,"release_copy":0,"release_consumption":0,"network":0,"dns":0,"environment":0,"credentials":0,"device":0,"camera":0,"ray":0,"strip":0,"cleanup":0,"capture":0,"formal":0,"public_analyzer":0,"td_c":0,"sentinel":0,"p8":0,"firmware":0,"deployment":0},"authorization":{"classification":"PURE_OFFLINE_GIT_AND_REPOSITORY_EVIDENCE_ONLY","human_device_authorization_required":false,"advisor_scientific_decision_required":false},"expected_duration":"under_10_minutes","visible_terminal_required":false,"archive":{"path":".agent-work/PLANS/20260801-0207-p7-retained-r3-b2-m1-r1-canonical-and-evidence-lifecycle-review.md","bytes":8493,"sha256":"5e557e1ea15d554c26e6924150abff647af8e6ffed9e9859577793734ad7671a"},"planner_stop":"B2_M1_R1_C1_GIT_ER_ONLY_SUPERSESSION_WAITING_PLANNER_REVIEW"}`

## 1. Activation 与 immutable evidence gate

Orchestrator必须先更新FULL唯一active task并创建activation。Expected parent exact
`4720f9ac2588397c484c54a8685988d57e56b83e`，subject exact
`chore(plan): activate real manifest evidence supersession`，changed paths exact为FULL、PLAN与本轮新archive。Activation后porcelain必须clean。

Executer只可读取repository与Git object：

1. exact验证activation full SHA、direct parent、subject、tree changed-path set与clean porcelain；
2. 从activation committed tree读取PLAN/FULL各exact one strict machine row并验证required FULL subset；
3. 从activation committed tree验证archive bytes/SHA；
4. 以`git show`/`git cat-file`/`git ls-tree`验证reviewed failure evidence commit topology、ER blob/bytes/SHA及exact one changed path；
5. 只读核对review archive所引用的repository source owner：
   `src/camera_based_rgbww_optimizer/optimization/p7_retained_release_audit.py`与
   `src/camera_based_rgbww_optimizer/utils/p7_retained_r3_provenance_io.py`。只确认前者 strict decoder 不做canonical reencode且三件套strict decode先于
   schema audit；后者 canonical decoder要求exact reencode。不得修改、运行、import或生成临时scanner。

不得从ER、PLAN、FULL或archive提取任何external path并在filesystem上probe。尤其禁止读取/stat/list/glob/search/reuse M1-R1 fresh
source/output、retained R3、accepted C1、accepted synthetic或任何old failure root。

## 2. Exact supersession payload

只向`.agent-work/EXECUTION_RESULT.md` EOF append one Markdown section，其标题exact：

```text
## REF-P7-25-R2-B2-M1-R1-C1 Git/ER-only supersession handoff
```

标题后只放一个 fenced `json` block，内部为one-line strict canonical JSON plus LF。Payload schema exact
`p7_td_b_retained_r3_option_b_b2_m1_r1_c1_supersession_v1`，必须包含且不得模糊以下事实：

- `supersedes`绑定原M1-R1 activation、evidence commit、ER blob/bytes/SHA、原payload schema与first failure；
- `original_record_immutable=true`、`original_record_rewritten=false`；
- `corrections.er_appends={"reported":0,"actual":1,"basis":"committed_one_block_append"}`；
- `corrections.fresh_probes={"budget":2,"actual":4,"preacquisition":2,"postappend":2,"budget_compliant":false}`；
- `corrections.input_identity_ledger={"successful_reads":5,"preserved_rows":0,"reconstructable_from_repository":false,
  "credit":false}`；不得发明五个缺失FileIdentity的path/device/inode/mode/data/hash rows；
- `canonical_failure_boundary`明确前四个C1 reads完成，首个retained physical path/bytes/SHA/mode gate完成，随后exact canonical reencode失败；
- `retained_acceptance_owner` exact说明 immutable retained inputs是opaque exact physical identity plus strict JSON：UTF-8 object、duplicate key拒绝、
  non-finite拒绝；canonical reencode/schema/scientific/eligibility/release均false；
- `canonical_outputs`说明C1 four与new output five仍要求canonical；
- `disposition`明确旧fresh namespace immutable no-read/no-stat/no-list/no-glob/no-search/no-reuse/no-modify/no-delete；
- `future_successor_requirements`冻结：new namespace、retained strict-only、C1/output canonical、每次成功read立即append identity ledger、failure保留partial
  ledger、final payload在append前写入`er_appends=1`、sole append后external operation0、actual与budget同时保留；
- `credit`全部为false：manifest seal、identity bundle、retained audit、eligibility、release；
- `current_package_counts`只能陈述本C1：ER append1、external operations0、tests/CodeGraph/controller/validator/release/device0、retry/fallback0；
- Planner stop exact `B2_M1_R1_C1_GIT_ER_ONLY_SUPERSESSION_WAITING_PLANNER_REVIEW`。

该record是supersession index，不是对旧ER的rewrite，也不是retained content或validator result。不得声称五个缺失identity已恢复，不得改变原failure
结论，不得把strict JSON acceptance解释为schema、science、eligibility或consumability。

## 3. Append lifecycle 与验证

Append前必须用committed Git object验证ER exact prefix blob/bytes/SHA。允许读取worktree ER exact一次，必须与committed prefix byte-for-byte相同。
使用single atomic repository edit在EOF append exact section；不得先写placeholder、counter0、temporary record或第二append。

Final payload在写入前即冻结`execution_result_appends=1`。Append后只允许三项repository-only检查：

1. old prefix bytes exact unchanged；
2. exact标题与payload schema在whole ER各新增/出现exact once，JSON strict decode且exact canonical reencode pass；
3. `git status --short` changed path exact `.agent-work/EXECUTION_RESULT.md`，`git diff --check` pass。

禁止append后访问任何external path。Executer不得stage/commit；Orchestrator负责evidence commit与后续Planner review。

## 4. Budgets、locks 与 stop

本包budgets只允许bounded Git/repository reads与ER append1，machine row给出的Git read-only command上限12、repository file reads4、postappend
checks3。它不是再次执行M1-R1；builder/runtime/controller/fresh probes全部0。Tests、compileall、CodeGraph query/sync、implementation commit也全部0。

External path read/stat/list/glob/search/write，failed fresh namespace reuse，retained/C1/synthetic evidence access，canonical validator/callback、eligibility、
retained audit、release generation/qualification/copy/consumption、network/DNS/environment/credentials、device/camera/Ray/strip/cleanup/capture/FORMAL/
public analyzer/TD-C/sentinel/P8/firmware/deployment全部exact0。Retry/fallback exact0。

完成sole append与repository checks后立即停止在Planner门。不得自行写下一real-input PLAN、创建fresh namespace、读取retained inputs或进入B3。

## 5. Authorization 与 maintainability

本包是`PURE_OFFLINE_GIT_AND_REPOSITORY_EVIDENCE_ONLY`，无device或科学分支，不需要Human或Advisor授权。

维护性边界：不修改P3、M1、P5或旧retained artifacts；只用one immutable supersession纠正evidence ledger。后续fresh successor继续使用既有single
owners，不得新增serializer、validator、filesystem helper或parallel evidence framework。无需架构重构。
