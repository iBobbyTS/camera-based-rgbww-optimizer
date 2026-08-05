# REF-G4-06 source-attestation v2 large-change roadmap

**Document status:** `ACTIVE_SOURCE_ATTESTATION_V2_ENGINEERING`

**Executable authority:** `false`

**Stable reference task:** `REF-G4-06-SOURCE-ATTESTATION-V2`

**Architecture:** `VALIDATE_FROZEN_CANDIDATE_BYTES_THEN_ATTEST_EXACT_COMMIT_BLOBS_BEFORE_SEPARATE_PACKAGE_PREPARATION`

`PLAN_FULL_MACHINE_CONTRACT={"schema":"g4_large_change_plan_full_v11","document_status":"ACTIVE_SOURCE_ATTESTATION_V2_ENGINEERING","executable":false,"active_task_count":1,"active_task":"REF-G4-06-SOURCE-ATTESTATION-V2","reference_goal":"REF-G4-COMPLETE","stable_reference_task":"REF-G4-06-SOURCE-ATTESTATION-V2","current_section":"SOURCE_ATTESTATION_V2_OWNER_SEAM","current_section_status":"ACTIVE_SOURCE_ATTESTATION_V2_ENGINEERING","architecture":"VALIDATE_FROZEN_CANDIDATE_BYTES_THEN_ATTEST_EXACT_COMMIT_BLOBS_BEFORE_SEPARATE_PACKAGE_PREPARATION","orchestration_branch":"codex/g4-r6-owner-alignment-large-change","intake_checkpoint":"641482706e5efebc81f1f55dba284cffd58b8355","accepted_source_blob":"0015d7ce2f2a5dde9118478f98c929020a474a01","accepted_test_blob":"2a60a987dda02675c2eddc7d8260d61a8f68edc3","historical_q1_ref":"refs/heads/codex/historical-g4-r6-immutable-qualification-q1-rejected","historical_q1_input_allowed":false,"maintainability_preflight_required":true,"parallel_attestation_owner_allowed":false,"candidate_bytes_must_be_frozen_for_validation":true,"post_validation_commit_blob_attestation_required":true,"package_preparation_in_current_section":false,"full_suite_budget":1,"full_retry":0,"candidate_implementation_authorized":true,"candidate_commit_authorized":false,"package_prepare_authorized":false,"package_describe_authorized":false,"package_root_selection_authorized":false,"package_root_check_authorized":false,"package_root_create_authorized":false,"formal_execution_authorized":false,"formal_root_creation_authorized":false,"release_consumption_authorized":false,"device_authorized":false,"network_authorized":false,"camera_authorized":false,"ray_authorized":false,"strip_authorized":false,"capture_authorized":false,"analysis_authorized":false,"g4_07_authorized":false,"td_c_authorized":false,"human_goal_complete":false,"guide_complete":false,"scientific_stage_complete":false,"allowed_next_action":"EXECUTER_EXECUTE_SOURCE_ATTESTATION_V2_ENGINEERING_PACKAGE"}`

## Current section

Planner应把以下内容合并为一个 bounded engineering package：maintainability preflight、单一 v2 attestation owner/seam、内部一致的 real-Git fixtures、positive/negative behavior probes、targeted/focused/compile/static/CodeGraph/scope checks，以及唯一 full suite和 Executer handoff。

候选资格与 future package construction是两个不同状态边界。本 section 只接受工程 owner；package preparation、root和formal必须等待 accepted exact code commit/blob checkpoint 后由下一 PLAN决定。

## Hard locks

- 不读取或复用 historical Q1 implementation，不创建 Q1 repair/Q2/corrective suffix。
- 不新增 parallel controller、宽泛 ignore/allowlist或第二个 identity source of truth。
- 不访问 package/formal roots、external experiment payload、设备或网络。
- Full budget/retry为 `1/0`；相同真实owner缺陷失败时 fail closed，harness自身问题单独归因。
