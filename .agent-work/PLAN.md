# REF-P7-25-R2-B2-C4-C1-C1：Orchestrator engineering architecture stop

**计划状态：** `PLANNER_REVIEW_COMPLETE_WAITING_ORCHESTRATOR_ENGINEERING_DECISION`

**Planner 日期：** `2026-07-30`

**Reference task：** `REF-P7-25-R2-B2-C4-C1-C1`

**Contract ID：**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-C4-C1-C1-ARCHITECTURE-STOP-V1`

**当前唯一动作：** Orchestrator 决定并冻结一个最小、可维护的 enabling
architecture，用于替代连续失败的 hand-authored external controller correction
chain。优先选择 repo-owned、dedicated、tested 的 preparation/serialization/AST
owner；若仍保留 external owner，至少先建立 immutable builder source，并要求其在
任何 execution activation 前通过 compile 与 content-free matrix gate。

**唯一 decision request：**
`ORCHESTRATOR_FREEZE_MAINTAINABLE_CONTROLLER_PREPARATION_ROUTE`。

**Planner stop：**
`B2_C4_C1_C1_ARCHITECTURE_STOP_WAITING_ORCHESTRATOR`。

本文件当前 `execution_authorized=false`。它不授权 Planner 或 Executer 修补、
执行、重试或复用 failed owner，不授权创建 package root，也不授权 controller、
tests、retained evidence、validator、release、network 或 device 操作。

**Reviewed archive：**
`.agent-work/PLANS/20260730-1210-p7-retained-r3-option-b-b2-c4-c1-c1-syntax-failure-review.md`
（bytes `4665`，SHA-256
`1b6980ad928b0327a59e31b982153f2d01bc52a2baa9c80b86deef978fd7db2d`）。

`PLAN_MACHINE_CONTRACT={"schema":"p7_td_b_retained_r3_option_b_b2_c4_c1_c1_architecture_stop_v1","reference_task_id":"REF-P7-25-R2-B2-C4-C1-C1","contract_id":"P7-TD-B-RETAINED-R3-OPTION-B-B2-C4-C1-C1-ARCHITECTURE-STOP-V1","dispatch_state":"not_dispatchable_orchestrator_engineering_decision_required","execution_authorized":false,"single_current_action":"orchestrator_freeze_maintainable_controller_preparation_route","single_decision_request":"ORCHESTRATOR_FREEZE_MAINTAINABLE_CONTROLLER_PREPARATION_ROUTE","decision_owner":"Orchestrator","scientific_escalation":false,"human_authorization_required":false,"review_decision":"REJECTED_PRE_ROOT_OWNER_SYNTAX_FAILURE_NO_C4_PROGRESS","review_archive":{"path":".agent-work/PLANS/20260730-1210-p7-retained-r3-option-b-b2-c4-c1-c1-syntax-failure-review.md","bytes":4665,"sha256":"1b6980ad928b0327a59e31b982153f2d01bc52a2baa9c80b86deef978fd7db2d"},"failed_owner":{"path":"/Volumes/4T/temp/rgbww-optimizer/p7-td-b-b2-c4-c1-c1-dual-owner-correction-v1.py","bytes":33106,"sha256":"97e649afa018e6884b00eee991939a59aa35e6ee89049652452db4bd5ce93e65","failure":"SyntaxError_line_255_outer_f_string_triple_single_quote_terminated_early","owner_invocations":1,"python_parse_attempts":1,"owner_body_entries":0},"zero_budget":{"dispatch":0,"root_create":0,"input_reads":0,"corrected_controller_generations":0,"matrix_cases":0,"terminal_writes":0,"execution_result_appends":0,"retry":0,"fallback":0},"c4_progress":false,"preferred_enabling_route":"repo_owned_dedicated_tested_preparation_serialization_ast_owner","minimum_external_route":"immutable_builder_source_plus_pre_activation_compile_and_content_free_matrix_gate","future_planner_package_required":true,"failed_owner_repair_or_reuse":false,"canonical_validator_calls":0,"eligibility_emissions":0,"release_operations":0,"device_operations":0,"planner_stop":"B2_C4_C1_C1_ARCHITECTURE_STOP_WAITING_ORCHESTRATOR"}`

## 1. Planner review decision

1. C4-C1-C1 is rejected as
   `REJECTED_PRE_ROOT_OWNER_SYNTAX_FAILURE_NO_C4_PROGRESS`.
2. The immutable owner is `33106` bytes with SHA-256
   `97e649afa018e6884b00eee991939a59aa35e6ee89049652452db4bd5ce93e65`.
   At source line `255`, a triple-single-quoted `_child` literal appears inside an
   outer f-string using the same delimiter, so Python parsing terminates the outer
   string early and raises `SyntaxError`.
3. The only owner invocation performed Python parsing. Owner-body entry, dispatch,
   root creation, input access, corrected output, matrix, terminal and ER append
   are all `0`; retry and fallback are `0/0`.
4. A parse failure before root and dispatch cannot satisfy or partially satisfy any
   C4 transform, qualification, evidence lifecycle or terminal criterion. C4 has
   made no progress under this package.
5. The detailed reviewed scope, evidence quality, decision and residual risk are
   preserved in the immutable archive named above.

## 2. Maintainability finding

The current corrective route repeatedly hand-authors disposable external programs
that combine nested generated Python, AST selection and rewriting, canonical JSON
serialization, subprocess lifecycle, physical sealing and ER gating. The line-255
delimiter collision is not an isolated scientific failure; it is direct evidence
that the controller-preparation boundary lacks a parser/test gate before immutable
one-shot activation.

Another deeper one-shot correction would continue a fragile hand-built state
machine and make ownership harder to audit. Planner therefore does not issue or
pre-authorize a successor package.

## 3. Orchestrator engineering decision boundary

The Orchestrator must choose and freeze one minimal enabling route:

1. **Preferred:** a repo-owned, dedicated, tested
   preparation/serialization/AST owner. Generated-source quoting, AST selection,
   canonical serialization and gate dominance should have explicit unit boundaries
   and regression tests before the eventual execution package is activated.
2. **Minimum external alternative:** an immutable builder source separate from the
   one-shot execution owner. Before activation, its frozen bytes must pass Python
   compile and a content-free matrix that exercises nested-source serialization,
   AST selector cardinality, canonical LF, terminal linkage and both ER paths.

The Orchestrator owns this engineering choice, exact repository scope, provenance
design and Git topology. This is not a color-science or measurement-science branch,
so Advisor escalation is forbidden. It performs no dangerous device operation, so
Human authorization is not required.

After the Orchestrator updates `FULL_PLAN_REFERENCE.md` and freezes one route, a
future Planner must create exactly one next work package. That package must name one
current action, explicit regression coverage, frozen inputs/outputs, a single stop
and fail-closed budgets. Nothing in this PLAN pre-authorizes that package.

## 4. Hard locks

Until a future PLAN is independently activated:

- do not edit, execute, import, compile, retry, repair or reuse the failed owner;
- do not create or reuse any package root or corrected controller;
- do not read C4/C4-C1 payloads, builders, controllers, retained R3 or release
  evidence;
- do not call the canonical validator, emit eligibility or consume a release;
- do not run tests, CodeGraph, public analyzer or any controller;
- do not access network, `.env`, credentials, device, camera, Ray, strip, cleanup,
  capture, FORMAL-R6, TD-C, sentinel or P8.

The retained release remains unvalidated and unconsumed. The unique stop is
`B2_C4_C1_C1_ARCHITECTURE_STOP_WAITING_ORCHESTRATOR`.

## 维护性判断

Planner has stopped the repeated external-controller correction chain at its
ownership boundary. The next route should separate preparation from one-shot
execution and make syntax, serialization and AST behavior testable before
activation; no additional correction layer is justified without that enabling
architecture.
