# P7 retained-R3 Option B：M1-S1 canonical JSON payload correction

**计划状态：** `WAITING_ORCHESTRATOR_ACTIVATION`

**Planner 日期：** `2026-08-01`

**Reference task：** `REF-P7-25-R2-B2-M1-S1-C1-C1-C1-C1-C1-C1`

**Contract：**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-M1-S1-C1-C1-C1-C1-C1-C1-CANONICAL-JSON-PAYLOAD-CORRECTION-V1`

**当前唯一动作：** Orchestrator建立一份同时冻结未验收test07/test13正确diff的fresh activation；Executer仅修M1生成manifest在P3 canonical JSON边界上的tuple payload缺陷，保留内部immutable tuple contract和既有两处测试纠偏，完成ordered offline validation、单一候选提交与ER handoff后停止。

**唯一 Planner stop：**
`B2_M1_S1_C1_C1_C1_C1_C1_C1_CANONICAL_JSON_PAYLOAD_WAITING_PLANNER_REVIEW`。

**本轮新归档：**
`.agent-work/PLANS/20260801-0043-p7-retained-r3-b2-m1-s1-canonical-json-payload-failure-review.md`；bytes `7356`，SHA-256
`e15d70b8075384107af48c9c3bf7531212f440916ec1e711d2eda5e4d273f44a`；不得覆盖earlier archives。

`PLAN_MACHINE_CONTRACT={"schema":"p7_td_b_retained_r3_option_b_b2_m1_s1_c1_c1_c1_c1_c1_c1_canonical_json_payload_correction_v1","reference_task_id":"REF-P7-25-R2-B2-M1-S1-C1-C1-C1-C1-C1-C1","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-M1-S1-C1-C1-C1-C1-C1-C1-CANONICAL-JSON-PAYLOAD-CORRECTION-V1","execution_authorized_after_orchestrator_activation":true,"activation_commit":{"expected_parent":"1b6715a2326d5a8d62d503e34e4cd8da76dfdf67","expected_subject":"chore(plan): activate real manifest canonical payload correction","expected_changed_paths":[".agent-work/FULL_PLAN_REFERENCE.md",".agent-work/PLAN.md",".agent-work/PLANS/20260801-0043-p7-retained-r3-b2-m1-s1-canonical-json-payload-failure-review.md","tests/test_p7_retained_r3_real_manifest_domain_template.py"],"carried_test_status":"UNVALIDATED_CARRY_FORWARD","carried_test_blob":"1df5786db37e7bb9cd4d5ffe26e4310d53f700aa","carried_test_bytes":18553,"carried_test_sha256":"9d6deea37ab7d33748b95fa1dabc1380a3ae9677b4008684387699bc40bd1dd6","carried_binary_diff_bytes":3404,"carried_binary_diff_sha256":"b01f78668e05e709d33d415020dcb388fefe34980f381f823b14e8103e1cf777","clean_porcelain_required_after_activation":true},"rejected_execution":{"activation_commit":"89b9b54f30a698700289a4e9ae006e01c9a6d53f","activation_parent":"540568c84d266c115f2a4fcdf9078fccc4956279","activation_subject":"chore(plan): activate real manifest CodeGraph-free correction","evidence_commit":"1b6715a2326d5a8d62d503e34e4cd8da76dfdf67","evidence_parent":"89b9b54f30a698700289a4e9ae006e01c9a6d53f","evidence_subject":"chore(evidence): record real manifest fake runtime stop","evidence_er_blob":"7a084f14c6e941ca3d899fa4b4932d0080106645","evidence_er_bytes":1202556,"evidence_er_sha256":"171d14a5e6e276be044130c5dbec40490d55aeb9af57d9410c7ba88006b4be65","first_failure":"targeted_production_canonical_json_payload_violation","targeted_total":13,"targeted_pass":12,"targeted_errors":1,"focused":0,"compileall":0,"full":0,"postcommit_targeted":0,"codegraph_sync":0,"commits":0,"retry":0},"rejected_candidate":{"candidate_commit":"cddd23eb4ef53a8f90c9b869f96f84ccfcba36cf","candidate_parent":"84b3458765849f9c50515067788af365006cef68","candidate_tree":"ff424f29e6a7a95349500ce356669a754d9ffa14","candidate_consumable":false},"implementation_commit":{"expected_parent_source":"current_activation_head_runtime","expected_subject":"fix(p7): project real manifest into canonical JSON","expected_changed_paths":["src/camera_based_rgbww_optimizer/utils/p7_retained_r3_real_manifest_domain_template.py","tests/test_p7_retained_r3_real_manifest_domain_template.py"],"single_commit":true,"clean_porcelain_required_after_commit":true},"required_full_machine_state":{"active_task_count":1,"active_task":"REF-P7-25-R2-B2-M1-S1-C1-C1-C1-C1-C1-C1","active_plan_contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-M1-S1-C1-C1-C1-C1-C1-C1-CANONICAL-JSON-PAYLOAD-CORRECTION-V1","retained_r3_status":"RETAINED_UNVALIDATED_UNCONSUMED","real_manifest_domain_owner_status":"ACTIVE_CANONICAL_JSON_PAYLOAD_CORRECTION","existing_root_identity_owner_status":"ACCEPTED_COMPLETE_COMPOSITE_VALIDATED","m1_real_manifest_candidate_commit":"cddd23eb4ef53a8f90c9b869f96f84ccfcba36cf","m1_real_manifest_candidate_consumable":false,"carried_test_status":"UNVALIDATED_CARRY_FORWARD","executer_dispatched":true,"device_authorized_by_this_file":false},"exact_write_paths":["src/camera_based_rgbww_optimizer/utils/p7_retained_r3_real_manifest_domain_template.py","tests/test_p7_retained_r3_real_manifest_domain_template.py"],"payload_contract":{"internal_contract_type":"immutable_tuple","persistence_value_domain":"exact_dict_list_finite_scalar_bool_null","schema":"p7_retained_r3_audit_provenance_manifest_v2","status":"sealed_subordinate_provenance_evidence","activation_shape":"ordered_five_item_list_with_changed_paths_list","baseline_shape":"ordered_twelve_item_list_with_two_six_item_seam_lists","c1_shape":"ordered_four_rows_each_eleven_item_list","retained_shape":"ordered_three_rows_each_eleven_item_list","generic_converter":false,"serializer_widening":false,"fake_persist_bypass":false,"field_value_or_order_change":false},"test_contract":{"carried_test_methods":["test_07_c1_exact_four_labels_order_children_uniqueness_and_hashes","test_13_generated_compile_fake_success_failure_and_negative_authority_surface"],"new_test_methods":0,"template_golden_sha_update":true,"persisted_manifest_exact_shape_assertion":true,"tuple_rejection_owner":"frozen_p3_tests","targeted_command":".venv/bin/python -m unittest tests.test_p7_retained_r3_real_manifest_domain_template","targeted_expected":13,"focused_command":".venv/bin/python -m unittest tests.test_p7_retained_r3_provenance_io tests.test_p7_retained_r3_controller_conformance tests.test_p7_retained_r3_controller_runtime tests.test_p7_retained_r3_controller_domain_template tests.test_p7_retained_r3_real_manifest_domain_template","focused_expected":83,"compileall_command":".venv/bin/python -m compileall -q src tests","full_command":"PYTHONUNBUFFERED=1 .venv/bin/python -m unittest discover -s tests -p 'test_*.py'","full_expected":800,"postcommit_targeted_expected":13},"execution_budgets":{"implementation_commits":1,"execution_result_appends":1,"test_invocations":4,"compileall_invocations":1,"codegraph_sync":1,"codegraph_queries":0,"retry":0,"fallback":0},"zero_budgets":{"third_code_test_path_writes":0,"p3_owner_edits":0,"p4_owner_edits":0,"p5_owner_edits":0,"p7_owner_edits":0,"serializer_widening":0,"generic_converter_helpers":0,"fake_persist_bypasses":0,"external_controller_reads":0,"external_controller_writes":0,"external_controller_processes":0,"external_root_reads":0,"external_root_creates":0,"synthetic_integration_runs":0,"accepted_c1_physical_reads":0,"retained_artifact_physical_reads":0,"git_provenance_replay":0,"real_b2_dispatch":0,"subordinate_manifest_physical_writes":0,"actual_canonical_validator_calls":0,"canonical_validator_callbacks":0,"eligibility_emissions":0,"retained_release_audit":0,"release_generation":0,"release_qualification":0,"release_copy":0,"release_consumption":0,"network":0,"dns":0,"environment":0,"credentials":0,"device":0,"camera":0,"ray":0,"strip":0,"cleanup":0,"capture":0,"formal":0,"public_analyzer":0,"td_c":0,"sentinel":0,"p8":0,"firmware":0,"deployment":0,"plan_writes_by_executer":0,"full_writes_by_executer":0,"archive_writes_by_executer":0,"debug_writes":0,"guide_writes":0,"research_writes":0},"expected_duration":"under_10_minutes","visible_terminal_required":false,"archive":{"path":".agent-work/PLANS/20260801-0043-p7-retained-r3-b2-m1-s1-canonical-json-payload-failure-review.md","bytes":7356,"sha256":"e15d70b8075384107af48c9c3bf7531212f440916ec1e711d2eda5e4d273f44a"},"planner_stop":"B2_M1_S1_C1_C1_C1_C1_C1_C1_CANONICAL_JSON_PAYLOAD_WAITING_PLANNER_REVIEW"}`

## 1. Fresh activation with exact carry-forward preservation

Orchestrator must create one fresh activation whose parent is exact evidence HEAD
`1b6715a2326d5a8d62d503e34e4cd8da76dfdf67`, subject exact
`chore(plan): activate real manifest canonical payload correction`, and changed paths exact:

1. `.agent-work/FULL_PLAN_REFERENCE.md`
2. `.agent-work/PLAN.md`
3. `.agent-work/PLANS/20260801-0043-p7-retained-r3-b2-m1-s1-canonical-json-payload-failure-review.md`
4. `tests/test_p7_retained_r3_real_manifest_domain_template.py`

The fourth path is not an accepted implementation. It is an explicit `UNVALIDATED_CARRY_FORWARD` of the
correct test07/test13 diff left dirty by the stopped execution. Before activation, its blob/bytes/SHA-256 must
be exact `1df5786db37e7bb9cd4d5ffe26e4310d53f700aa` / `18553` /
`9d6deea37ab7d33748b95fa1dabc1380a3ae9677b4008684387699bc40bd1dd6` and its binary diff from
`89b9b54...` must be exact bytes `3404`, SHA-256
`b01f78668e05e709d33d415020dcb388fefe34980f381f823b14e8103e1cf777`. Orchestrator must not alter,
reformat, stage separately, or call these changes validated. Activation must leave porcelain clean.

Executer starts only after verifying activation topology, strict PLAN/FULL machine rows and required FULL
subset. Candidate `cddd23e...` remains non-consumable. Passing this package creates only a waiting-review
candidate; it does not authorize M1-I1, retained audit, validator, release, or any device route.

## 2. Frozen owners and root-cause boundary

Before edit, verify with Git object identities only:

| Owner | Path | Git blob | Bytes | SHA-256 |
| --- | --- | --- | ---: | --- |
| M1 | `src/camera_based_rgbww_optimizer/utils/p7_retained_r3_real_manifest_domain_template.py` | `84fcd755225af39eb89459146de282392367b70b` | `23352` | `5a593fee05eb09e0a3c10d30661e480823baef2876446c25b9fd42e46d70c29d` |
| P3 | `src/camera_based_rgbww_optimizer/utils/p7_retained_r3_provenance_io.py` | `d6d6cc628861baf8a95a09f13fa9204989693b5b` | `19767` | `118f8bdd086f3180088c99681e4dfbdfff05613c844a21bd83f3c1dd53c31a3d` |
| carried test | `tests/test_p7_retained_r3_real_manifest_domain_template.py` | `1df5786db37e7bb9cd4d5ffe26e4310d53f700aa` | `18553` | `9d6deea37ab7d33748b95fa1dabc1380a3ae9677b4008684387699bc40bd1dd6` |

P3 is frozen and remains the sole canonical serialization owner. Its accepted domain is exact JSON-native
`dict`、`list`、finite numeric/string、boolean、null; tuple remains fail-closed
`json_unsupported_value`. Fake `persist()` must continue calling `canonical_json_bytes`; it is not a mock
escape hatch.

M1 remains owner of the generated real-manifest payload. Internal `REAL_MANIFEST_CONTRACT`, activation,
baseline, seam, C1, retained and Git targets remain immutable tuples for validation and deterministic source
composition. Only the value passed to `persist_canonical_json` at `phase_evaluate` is incorrect.

## 3. Exact production correction

Only in M1 `_CANONICAL_TEMPLATE`'s `phase_evaluate`, replace the tuple-valued manifest fields with an explicit,
ordered JSON-native projection:

- `activation`: one five-item list preserving commit、parent、subject、changed-paths、full patch SHA; changed
  paths becomes one ordered list;
- `baseline`: one twelve-item list preserving every existing value and order; its seam chain becomes one
  ordered two-row list, each row an exact six-item list;
- `c1`: one ordered four-row list, each row an exact eleven-item list;
- `retained`: one ordered three-row list, each row an exact eleven-item list;
- `schema` and `status` remain byte-for-byte unchanged.

The projection may use local list literals/comprehensions directly at `manifest_payload`. It must not add a
generic recursive converter, helper, serializer, tuple allowlist, fallback, second payload owner, or mutation
of the internal tuple contract. It must not drop, rename, reorder, normalize, stringify, or infer any value.
P3/P4/P5/P7 and all other source files are read-only.

After changing `_CANONICAL_TEMPLATE`, recompute and replace only the M1
`_CANONICAL_TEMPLATE_SHA256` golden constant. `_GOLDEN_REPLACEMENT_SHA256` must remain unchanged because the
replacement contract is unchanged. No public export/dataclass/builder/runtime-request/lifecycle/artifact/
root/read/Git budget may change.

## 4. Dedicated test correction and preserved assertions

The same dedicated test is the only test write path. Preserve the carried test07 and exact AST authority
logic in test13 without weakening or reverting either one.

Permitted additional test edits are only:

1. test02 continues to compare the template to the updated production golden SHA; no replacement golden
   update is allowed;
2. test13's fake success path inspects the stored first manifest artifact and proves schema/status plus the
   exact activation/baseline/C1/retained ordered shapes and values described above;
3. the existing fake `persist()` continues canonical encoding and the existing primary-failure identity
   assertion remains unchanged.

No new test method, generic fixture converter, serializer bypass, second fake runtime, helper, scanner, or
new test path is allowed. The focused P3 suite must continue proving tuple rejection; this package must not
change P3 or turn its negative assertion into tuple acceptance.

## 5. Ordered validation and candidate commit

After a human-readable Git diff confirms exact two paths, no carried-block regression, no other test method,
no P3/P4/P5/P7 changes, and `git diff --check` clean, run each exact once and stop on first nonzero/count
mismatch:

1. targeted: `.venv/bin/python -m unittest tests.test_p7_retained_r3_real_manifest_domain_template`, exact
   `13/13` and `OK`;
2. focused: `.venv/bin/python -m unittest tests.test_p7_retained_r3_provenance_io tests.test_p7_retained_r3_controller_conformance tests.test_p7_retained_r3_controller_runtime tests.test_p7_retained_r3_controller_domain_template tests.test_p7_retained_r3_real_manifest_domain_template`, exact `83/83` and `OK`;
3. compileall: `.venv/bin/python -m compileall -q src tests`, exit `0`;
4. full: `PYTHONUNBUFFERED=1 .venv/bin/python -m unittest discover -s tests -p 'test_*.py'`, exact
   `800/800` and unique `OK`;
5. only after all validation passes, run `codegraph sync` exact once, exit `0`; no CodeGraph explore/query or
   semantic claim is permitted;
6. recheck exact two-path diff and frozen owner identities; stage exact M1 + dedicated test and create one
   commit with subject `fix(p7): project real manifest into canonical JSON`;
7. require implementation commit direct child of current activation, exact two changed paths, clean
   porcelain; record tree, both final blob/bytes/SHA-256 values and canonical binary patch SHA-256;
8. run postcommit targeted exact once, exact `13/13` and `OK`;
9. append `.agent-work/EXECUTION_RESULT.md` exact once and stop.

Total budgets: test invocations `4`, compileall `1`, CodeGraph maintenance sync `1`, implementation commit
`1`, ER append `1`, retry/fallback `0/0`. Any failure before commit leaves the activation's carried test
content preserved; any additional uncommitted correction must be reported precisely and not called accepted.

## 6. Hard locks and stop

Exact zero: any third code/test path, P3/P4/P5/P7 edit, serializer widening, generic converter/helper, fake
persist bypass, CodeGraph query, external controller/root/process, synthetic integration, accepted-C1 or
retained physical reads, Git provenance replay, real B2, subordinate manifest physical write, actual canonical
validator/callback/eligibility, retained audit, release generation/qualification/copy/consumption, network,
DNS, environment, credentials, device, camera, Ray, strip, cleanup, capture, FORMAL, public analyzer, TD-C,
sentinel, P8, firmware, deployment, and Executer writes to PLAN/FULL/archive/debug/GUIDE/RESEARCH.

This is a pure offline engineering/provenance correction, expected under ten minutes. It needs no Advisor or
Human authorization and no visible Terminal. Success or failure stops at the sole Planner stop; M1-I1 remains
locked until a later Planner review accepts the composite result.

维护性边界：M1仅在自己的persist boundary做显式JSON-native projection；P3 serializer、P4 lifecycle、
P5 runtime composition和immutable tuple input contract保持单一owner，不引入共享转换层或并行框架。
