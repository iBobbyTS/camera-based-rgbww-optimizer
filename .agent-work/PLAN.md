# P7 retained-R3 Option B：B3-C2 governance identity production correction

**计划状态：** `WAITING_ORCHESTRATOR_ACTIVATION`

**Planner 日期：** `2026-08-01`

**Reference task：** `REF-P7-25-R2-B3-C2`

**Contract：**
`P7-TD-B-RETAINED-R3-OPTION-B-B3-C2-GOVERNANCE-IDENTITY-CORRECTION-V1`

**当前唯一动作：** Orchestrator先记录B3-C1-C1-S1 accepted状态并创建activation；Executer随后只在existing
real-manifest domain owner及其dedicated test内，把误导的baseline governance字段
`advisor_decision_sha256`纠正为`lineage_owner_decision_evidence_sha256`，保持serialized baseline的
positional shape/value与所有旧evidence immutable，并完成CodeGraph preflight、targeted/focused/compileall/full、
post-edit sync与离线终端证据。

**唯一 Planner stop：**
`B3_C2_GOVERNANCE_IDENTITY_CORRECTION_WAITING_PLANNER_REVIEW`。

**本轮新归档：**
`.agent-work/PLANS/20260801-0455-p7-retained-r3-b3-c1-c1-s1-acceptance-review.md`；
bytes `3886`，SHA-256 `3592e5cfdf4dec736d4283a03e47159595b2387fdc6262cc069dd7e6f87c3ee9`；不得覆盖earlier archives。

`PLAN_MACHINE_CONTRACT={"schema":"p7_td_b_retained_r3_option_b_b3_c2_governance_identity_correction_v1","reference_task_id":"REF-P7-25-R2-B3-C2","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B3-C2-GOVERNANCE-IDENTITY-CORRECTION-V1","execution_authorized_after_orchestrator_activation":true,"activation_commit":{"expected_parent":"751a04d14c263853d56836049ce1bb3038a5e990","expected_subject":"chore(plan): activate B3 governance identity correction","expected_changed_paths":[".agent-work/FULL_PLAN_REFERENCE.md",".agent-work/PLAN.md",".agent-work/PLANS/20260801-0455-p7-retained-r3-b3-c1-c1-s1-acceptance-review.md"],"clean_porcelain_required_after_activation":true},"accepted_b3_c1_c1_s1":{"activation":"c2949adc8230a7e624485fe4ecf8aaf8ec0a0380","evidence_commit":"751a04d14c263853d56836049ce1bb3038a5e990","decision":"ACCEPTED_COMPLETE_GIT_ER_TERMINAL_SUPERSESSION_RECORDED","evidence_changed_paths":[".agent-work/EXECUTION_RESULT.md"],"parent_er":{"bytes":1301614,"sha256":"6c2ccf6170aca4e1b51b1192b1be93ab0a43457063ac3675be5afb052c64128c"},"eof_suffix":{"bytes":8002,"sha256":"f091513ca4d160fbc0648e04d283591da8fc02a1934c264299a91b0b5f190142"},"evidence_er":{"bytes":1309616,"sha256":"f0474fcc4b6f835d91c9483f4923b9ca50f54ce3b0fa7816ca2be32caeee7546"},"parent_is_complete_prefix":true,"payload_strict_canonical_json":true,"outcome":"B3_C1_C1_S1_GIT_ER_ONLY_TERMINAL_SUPERSESSION_RECORDED","git_reads_actual":14,"git_reads_max":18,"execution_result_committed_reads":2,"external_code_test_codegraph_controller_validator_audit_device_actual":0},"required_full_machine_state":{"active_task_count":1,"active_task":"REF-P7-25-R2-B3-C2","active_plan_contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B3-C2-GOVERNANCE-IDENTITY-CORRECTION-V1","retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","manifest_authority":"SUBORDINATE_EVIDENCE_ONLY_CANONICAL_VALIDATOR_SOLE_ELIGIBILITY_OWNER","b3_c1_c1_s1_status":"ACCEPTED_COMPLETE_GIT_ER_TERMINAL_SUPERSESSION_RECORDED","b3_c2_status":"ACTIVE_BOUNDED_PRODUCTION_GOVERNANCE_IDENTITY_CORRECTION","executer_dispatched":true,"device_authorized_by_this_file":false},"exact_write_paths":["src/camera_based_rgbww_optimizer/utils/p7_retained_r3_real_manifest_domain_template.py","tests/test_p7_retained_r3_real_manifest_domain_template.py"],"production_owner_contract":{"dataclass":"RealManifestBaselineIdentity","old_field":"advisor_decision_sha256","new_field":"lineage_owner_decision_evidence_sha256","old_field_occurrences_after":0,"serialized_baseline_length":12,"serialized_shape_changed":false,"serialized_values_changed":false,"zero_based_positions":{"6":"governance_manifest_sha256","7":"guide_sha256","8":"lineage_owner_decision_evidence_sha256","9":"advisor_attachment_sha256","10":"human_governance_override","11":"helper_disposition"},"position_8_owner":{"kind":"external_lineage_owner_decision_evidence","path":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-release-lineage-owner-o3-c1r3/20260728T0121/lineage-owner-decision-evidence.json","bytes":7066,"sha256":"842cfad090549ebf6379df4551bd4f051267e4bf93014f899c5e329c57085620","status":"advisor_decision_required","accepted":false},"position_9_owner":{"kind":"advisor_option_b_attachment","path":"/Users/ibobby/.codex/attachments/cba7928d-712a-441e-a708-4301ee32bd66/pasted-text.txt","bytes":11146,"sha256":"91a88e5467e13c811794c2149b6a8d5669e613c3e259d8f4091ba08c048733d6"},"advisor_request_git_owner":{"path":"advisor/4/0.AUDIT/07-guide4-to-retained-r3-lineage-owner-decision.md","bytes":6754,"sha256":"5b23cbdfe97ac71e7438f1d30461455938828029c0ba32e931a9570e0ea88a34","included_in_serialized_baseline":false},"canonical_template_sha256_unchanged":"a83804d299c747c485dda86eecd3bcb576a90bb2be3c2ae03fe77951ed404ad6","golden_replacement_sha256_unchanged":"55c43ad338a83c11a2b2c8d2c5714a9efaf75ec4215dd30e103d540b0c6502ec","old_b2_manifest_repair":false,"old_b2_manifest_regeneration":false,"old_payload_repair":false,"old_payload_regeneration":false,"parallel_owner":false,"generic_path_allowlist":false},"test_contract":{"dedicated_test_methods":13,"targeted_command":".venv/bin/python -m unittest tests.test_p7_retained_r3_real_manifest_domain_template","targeted_expected":13,"focused_command":".venv/bin/python -m unittest tests.test_p7_retained_r3_provenance_io tests.test_p7_retained_r3_controller_conformance tests.test_p7_retained_r3_controller_runtime tests.test_p7_retained_r3_controller_domain_template tests.test_p7_retained_r3_real_manifest_domain_template","focused_expected":83,"compileall_command":".venv/bin/python -m compileall -q src tests","full_command":"PYTHONUNBUFFERED=1 .venv/bin/python -m unittest discover -s tests -p 'test_*.py'","full_expected":800,"git_diff_check_required":true},"codegraph_contract":{"pre_edit_query":1,"query_before_source_test_read_or_edit":true,"query_scope":"RealManifestBaselineIdentity build_real_manifest_domain_template and dedicated test blast radius","post_edit_sync":1,"changed_project_count":1,"post_sync_query":0},"execution_budgets":{"git_read_invocations_max":12,"execution_result_committed_reads":2,"execution_result_current_tail_reads":1,"repository_code_reads_max":1,"repository_test_reads_max":1,"repository_code_writes":1,"repository_test_writes":1,"codegraph_queries":1,"codegraph_sync":1,"test_invocations":3,"compileall_invocations":1,"git_diff_check_invocations":1,"execution_result_appends":1,"apply_patch_invocations_max":3,"postappend_operations":0,"implementation_commits_by_executer":0,"retry":0,"fallback":0},"orchestrator_commit_after_handoff":{"owner":"ORCHESTRATOR","executer_must_not_commit":true,"expected_subject":"fix(p7): correct manifest governance identity","expected_changed_paths":[".agent-work/EXECUTION_RESULT.md","src/camera_based_rgbww_optimizer/utils/p7_retained_r3_real_manifest_domain_template.py","tests/test_p7_retained_r3_real_manifest_domain_template.py"]},"zero_budgets":{"third_code_test_path_writes":0,"plan_writes_by_executer":0,"full_writes_by_executer":0,"archive_writes_by_executer":0,"debug_writes":0,"guide_reads":0,"guide_writes":0,"research_writes":0,"advisor_file_reads":0,"advisor_file_writes":0,"external_governance_evidence_reads":0,"advisor_attachment_reads":0,"old_execution_result_payload_reads":0,"old_b2_manifest_reads":0,"old_b2_manifest_writes":0,"real_manifest_reads":0,"real_manifest_writes":0,"real_source_reads":0,"c1_input_reads":0,"retained_artifact_reads":0,"retained_artifact_writes":0,"controller_invocations":0,"synthetic_runs":0,"actual_canonical_lineage_validator_calls":0,"canonical_validator_callbacks":0,"retained_release_audit":0,"eligibility_emissions":0,"release_generation":0,"release_qualification":0,"release_copy":0,"release_consumption":0,"network":0,"dns":0,"environment":0,"credentials":0,"device":0,"camera":0,"ray":0,"strip":0,"cleanup":0,"capture":0,"formal":0,"public_analyzer":0,"td_c":0,"sentinel":0,"p8":0,"firmware":0,"deployment":0},"authorization":{"classification":"PURE_OFFLINE_TWO_PATH_PRODUCTION_GOVERNANCE_IDENTITY_CORRECTION","human_device_authorization_required":false,"advisor_scientific_decision_required":false},"expected_duration":"under_10_minutes","visible_terminal_required":false,"archive":{"path":".agent-work/PLANS/20260801-0455-p7-retained-r3-b3-c1-c1-s1-acceptance-review.md","bytes":3886,"sha256":"3592e5cfdf4dec736d4283a03e47159595b2387fdc6262cc069dd7e6f87c3ee9"},"planner_stop":"B3_C2_GOVERNANCE_IDENTITY_CORRECTION_WAITING_PLANNER_REVIEW"}`

## 1. Activation、preflight 与scope

Activation必须以`751a04d...`为parent、exact subject/path set，随后porcelain clean。Executer先从activation
committed PLAN/FULL解析strict machine rows并只做typed semantic subset compare，不得要求canonical reencode、sorted
keys、raw/reencoded equality或叙事selector。

在读取production/test源码前，必须exact one CodeGraph query定位`RealManifestBaselineIdentity`、
`build_real_manifest_domain_template`与dedicated tests的blast radius。Preflight确认单一owner已存在，修改不会引入
第二manifest builder、parser、serializer、path allowlist或eligibility owner。随后只可读取、编辑machine contract冻结的
exact two paths；任何第三tracked code/test path需要修改即fail closed并进入Planner stop。

## 2. 唯一production correction

仅执行语义不变的owner命名纠偏：

1. 在frozen `RealManifestBaselineIdentity`将字段`advisor_decision_sha256`改名为
   `lineage_owner_decision_evidence_sha256`；
2. `build_real_manifest_domain_template`的唯一字段访问同步改名；
3. serialized baseline仍为exact 12 positions，position 8仍输出同一个SHA value，position 9及后续positions不移动；
4. 不增加path字段、不写入Advisor request Git SHA、不改变artifact schema/status、controller template、golden hashes、
   expected bound results、artifact names、lifecycle、Git targets、C1/retained inputs或retry/fallback；
5. 不读取或修改old B2 manifest five、old/new ER payload、external governance/Advisor/C1/retained inputs。PLAN冻结的
   path/hash只定义future owner语义，不授权本包访问这些文件。

Position 8的owner是exact external lineage-owner decision evidence `842cfad...`；它自身是Advisor请求前的
`advisor_decision_required/accepted=false` evidence。Position 9才是Advisor Option-B attachment `91a88...`。
Advisor request Git file `5b23...`有独立Git owner/path，不属于serialized baseline，不能替换position 8或9。

## 3. Dedicated regression 与验证顺序

Dedicated test只在existing test class中更新语义断言，不增加平行fixture owner：

- exact frozen dataclass fields包含`lineage_owner_decision_evidence_sha256`且不再包含legacy field；
- generated manifest baseline list length仍为12，positions 6..11的字段/value映射exact；
- position 8取new field，position 9仍取`advisor_attachment_sha256`；
- canonical template SHA与golden replacement SHA保持冻结值；
- source/test中legacy identifier在完成后为`0`，且不出现Advisor request Git path/hash绑定。

严格顺序：targeted exact `13/13` → focused exact `83/83` → compileall pass → durable full exact
`800/800`且唯一`OK` → `codegraph sync` exact one → `git diff --check` pass。Tests、compileall或sync任何失败均不
retry/fallback；保留two-path diff，记录first failure并停Planner。不得运行synthetic controller、real-input self-check、
canonical validator或retained audit。

## 4. Handoff、Git owner与locks

Executer在所有验证后可exact one读取current `EXECUTION_RESULT.md` tail以取得唯一EOF anchor，再向physical EOF追加
exact one terminal block，至少记录activation、
two-path pre/post SHA、semantic rename、position mapping、targeted/focused/full结果、compileall、CodeGraph query/sync、diff
check、actual/budget、zero locks、outcome与唯一Planner stop。Success outcome只能是
`B3_C2_GOVERNANCE_IDENTITY_CORRECTION_VALIDATED`。失败也必须记录first failure及已完成计数。

ER append是Executer最后side effect，之后Executer read/status/hash/test/sync/commit均为`0`。Executer不得commit；
Orchestrator收到handoff后可按AGENTS personally audit并创建exact code/test/ER focused commit，此Orchestrator动作不计入
Executer postappend budget。

本包不验证或消费old B2 manifest，不改变`RETAINED_UNVALIDATED_UNCONSUMED`。Canonical lineage validator仍是唯一
eligibility owner；B4、release、device、FORMAL-R6、strip、TD-C、sentinel与P8保持locked。成功只使production
governance field owner命名可用于下一次postcommit/synthetic verification，不直接解锁retained real audit。

成功或失败均停
`B3_C2_GOVERNANCE_IDENTITY_CORRECTION_WAITING_PLANNER_REVIEW`。

维护性判断：修改保持在existing frozen spec/dataclass与dedicated test两个owner内，不增加artifact字段、parallel
serializer或eligibility路径；targeted、focused、full与CodeGraph sync覆盖命名纠偏及其blast radius。
