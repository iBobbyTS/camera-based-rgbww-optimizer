# G4 PLAN/PLAN-FULL runtime alignment — terminal rejected Human report stop

## Terminal disposition

- **status:** `REJECTED_TERMINAL_PLAN_FULL_RUNTIME_ALIGNMENT_ENGINEERING_FAILURE`
- **executable:** `false`
- **active_task_count:** `0`
- **active_task:** `null`
- **planner_stop:** `HUMAN_REPORT_REQUIRED_EXACT_RUNTIME_ALIGNMENT_MISMATCH_NO_SECOND_CORRECTION`
- **engineering correction budget:** `1/1` consumed; retry `0`; second correction
  package prohibited.

## Exact reviewed evidence

The first and only authorized command resolved to real test bodies and completed:

- `Ran 69 tests in 83.091s`
- natural exit `1`
- `failures=1`
- `errors=213`

The dominant engineering mismatch is exact and bounded:

1. The candidate removed the production import of
   `parse_full_plan_machine_state`, while the accepted
   `build_stage_gate_input()` path still calls that name in
   `p7_td_b_r6_stage_gate.py`, causing `NameError` across affected stage-gate
   tests before their intended assertions.
2. The parser public-surface test proves the newly added PLAN-FULL parser wrapper
   is absent from `agent_work_machine_contract.__all__`.

This is an engineering failure, not a selector/harness failure and not a scientific
result. The second four-test command, full suite, CodeGraph sync and final diff gate
were not run. No device, network, camera, Ray, strip, capture, formal, package/root,
release-consumption, analysis or scientific effect occurred.

## Candidate and accepted-tree boundary

The current uncommitted changes under these paths are retained as rejected evidence
only and are not accepted implementation:

- `src/camera_based_rgbww_optimizer/utils/agent_work_machine_contract.py`
- `src/camera_based_rgbww_optimizer/optimization/p7_td_b_r6_stage_gate.py`
- `tests/test_agent_work_machine_contract.py`
- `tests/test_p7_td_b_r6_stage_gate.py`

They must not be repaired, copied, cherry-picked, used as implementation input, or
treated as a partial pass. Candidate 2 and every historical rejected candidate
remain evidence-only as well. The accepted runtime-consumer package commit remains
`21754a3`; no new accepted code/test commit exists.

The rejected source/test candidate is now preserved historical-only at:

- ref: `refs/heads/codex/historical-g4-r6-plan-full-runtime-alignment-rejected`
- commit: `f1ca21ce5df4a92ba9ebfbbb786d2d22c09269ba`
- tree: `03a504568b98d383f5d960be7a82b57a3144d469`
- `implementation_input_allowed=false`

The live branch accepted source/test tree has been restored without `reset` or
`clean`. The historical ref is recoverable evidence only and must not be merged,
cherry-picked, copied, repaired, or consumed by any future implementation route.

## Scientific status and required stop

- **scientific_target:** unchanged — obtain the new Ray R6 16-frame operational-600
  acquisition and Ray-only analysis.
- **science_delta:** none; captures remain `0` and no scientific negative result was
  created.
- **next_scientific_action:** remains
  `P7-TD-B-RAY-OP600-EXPOSURE-GUARDED-FORMAL-R6`, but it is not unlocked by this
  rejected candidate.
- **required next action:** report the exact runtime-alignment mismatch to Human.
  Do not create a second correction, infer a repair, or resume formal execution.
  Orchestrator may create one terminal semantic commit preserving this disposition;
  that commit does not authorize further work.

All authorities remain false: `package_prepare`, `release_consumption`,
`formal_execution`, `device`, `network`, `camera`, `ray`, `strip`, `capture`,
`analysis`, `root_creation`, and `td_c`. GUIDE, RESEARCH and
`FULL_PLAN_REFERENCE.md` remain unchanged by this review.

Reviewed terminal archives:

- `.agent-work/archived/PLAN-20260806-0822.md`
- `.agent-work/archived/EXECUTION_RESULT-20260806-0822.md`

`PLAN_MACHINE_CONTRACT={"schema":"planner_execution_contract_v2","contract_id":"G4-PLAN-RUNTIME-ALIGNMENT-CORRECTION-V1","plan_status":"REJECTED_TERMINAL_PLAN_FULL_RUNTIME_ALIGNMENT_ENGINEERING_FAILURE","executable":false,"active_task_count":0,"active_task":null,"reference_task_id":"G4-PLAN-RUNTIME-ALIGNMENT-CORRECTION","engineering_only_plan_budget_consumed":1,"engineering_retry":0,"second_engineering_package_allowed":false,"accepted_runtime_consumer_package_commit":"21754a3","candidate_status":"RETAINED_REJECTED_EVIDENCE_ONLY_FORBIDDEN_AS_IMPLEMENTATION_INPUT","candidate_historical_ref":"refs/heads/codex/historical-g4-r6-plan-full-runtime-alignment-rejected","candidate_historical_commit":"f1ca21ce5df4a92ba9ebfbbb786d2d22c09269ba","candidate_historical_tree":"03a504568b98d383f5d960be7a82b57a3144d469","implementation_input_allowed":false,"live_accepted_source_test_restored":true,"package_prepare_authorized":false,"release_consumption_authorized":false,"formal_execution_authorized":false,"device_authorized":false,"network_authorized":false,"camera_authorized":false,"ray_authorized":false,"strip_authorized":false,"capture_authorized":false,"analysis_authorized":false,"root_creation_authorized":false,"td_c_authorized":false,"scientific_result_created":false,"planner_stop":"HUMAN_REPORT_REQUIRED_EXACT_RUNTIME_ALIGNMENT_MISMATCH_NO_SECOND_CORRECTION"}`
