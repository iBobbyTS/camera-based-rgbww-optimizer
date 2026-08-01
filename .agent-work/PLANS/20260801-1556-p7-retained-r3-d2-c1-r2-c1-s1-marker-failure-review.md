# P7 retained-R3 Option B D2-C1-R2-C1-S1 marker failure review

**Planner 日期：** `2026-08-01`

**Reviewed reference task：** `REF-P7-25-R2-B3-C3-C4-R5-R1-C1-R2-R1-C2-S1-C1-R1-D1-D2-C1-R2-C1-S1`

**Reviewed contract：** `P7-TD-B-RETAINED-R3-OPTION-B-B3-C3-C4-R5-R1-C1-R2-R1-C2-S1-C1-R1-D1-D2-C1-R2-C1-S1-READ-ONLY-ATTRIBUTION-HANDOFF-SUPERSESSION-V1`

**Decision：** `REJECTED_PRE_EFFECT_HANDWRITTEN_BARE_MARKER_GATE_AND_MISSING_DURABLE_ER_HANDOFF`

## 1. Reviewed scope and frozen inputs

Activation is commit `f28aa4a968549a2f9ba1fa55fc45d9294026df43`, direct child of evidence `fd9291a49383c20f742137f5c798ddbca10240d6`, subject exact `chore(plan): seal attribution handoff deviation`. Its changed paths are the required exact three governance documents: `.agent-work/FULL_PLAN_REFERENCE.md`, `.agent-work/PLAN.md`, and `.agent-work/PLANS/20260801-1540-p7-retained-r3-d2-c1-r2-c1-procedural-deviation-review.md`.

Committed activation identities independently verified by Planner:

- `.agent-work/PLAN.md`: `12284` bytes, SHA-256 `a6d6d69bc2890ffa4f9e5f5514de7630aa9fbef51743a93a73b837368f403f2e`;
- `.agent-work/FULL_PLAN_REFERENCE.md`: `461183` bytes, SHA-256 `2e1237babe00664a0fded1fcb71d87fb2d194338a5321052855f81e6e2a90a83`;
- `.agent-work/EXECUTION_RESULT.md`: `1540765` bytes, SHA-256 `7cd4258114b184c29ed37916c1ea2a3045fb40f8700964336f5b35dbae36b6c3`.

The ER identity is exactly the already-reviewed evidence ER identity frozen in the activation PLAN. Therefore no S1 append or evidence child commit exists.

## 2. Execution method and validation quality

The Executer candidate account reports one raw committed read each for PLAN, FULL, and ER, followed by a hand-written requirement that the `PLAN_MACHINE_CONTRACT=` marker begin at byte zero of a physical line. The valid committed row is Markdown inline-code encoded: one leading backtick, the marker and JSON payload, then one trailing backtick. The hand-written gate reported the marker missing before any shell/controller/report operation.

Planner independently passed the exact committed PLAN raw Git stdout bytes to the accepted repo-owned `parse_plan_machine_contract`; parsing succeeded. This proves the committed row is accepted canonical input and the failure is a caller-side parallel parser defect, not a PLAN marker defect and not a defect in the accepted parser owner.

The candidate facts also report report reads `0`, report-seal reads `0`, `apply_patch` appends `0`, and all controller/selector/Git-ledger/source/test/device/network/camera/Ray/strip/cleanup/formal/release effects `0`. An earlier JavaScript wrapper `SyntaxError` occurred before the shell started and therefore did not consume shell or execution budgets. These facts are useful for selecting a bounded corrective route, but they are not accepted as durable execution evidence because no ER handoff was appended and no evidence commit exists.

## 3. Findings and decision

1. `S1-MARKER-001`: the activation used a hand-written bare-line marker search even though the accepted production parser owns Markdown machine-row decoding. This violates the package's parser-owner boundary and failed before report acquisition.
2. `S1-HANDOFF-002`: the failed attempt did not append its zero-effect record to physical ER EOF. A chat/orchestrator candidate report cannot substitute for the required durable Executer handoff.
3. No report/seal or complete 18-row matrix was reacquired, so the original S1 supersession remains unexecuted and unaccepted.
4. No production-owner, lineage, manifest-truth, eligibility, or release credit is created. `retained_r3_status` remains `RETAINED_UNVALIDATED_UNCONSUMED`.

The reviewed S1 execution is rejected. This is an engineering/parser-call-site correction; no Advisor scientific escalation and no Human device authorization are required.

## 4. Residual risks and exact next branch

The next branch is `REF-P7-25-R2-B3-C3-C4-R5-R1-C1-R2-R1-C2-S1-C1-R1-D1-D2-C1-R2-C1-S1-C1`. It is one parser-bound corrective supersession package:

1. acquire activation committed PLAN/FULL/ER raw bytes exactly once each;
2. call accepted `parse_plan_machine_contract` and `parse_full_plan_machine_state` directly on raw bytes, consume only `.value` and optionally `.evidence.to_mapping()`, and prohibit all handwritten marker scanning, decode, text-mode reads, regex/grep/sed/awk marker extraction, or row repair;
3. first append a durable zero-effect failure supersession at physical ER EOF, recording the missing prior handoff and the candidate zero counters;
4. only after that append succeeds, continue the original bounded read-only report/report-seal verification using the same in-memory committed-doc and ER baseline state; no ER reread is allowed;
5. append either the complete successful 18-row attribution supersession or a fail-closed terminal correction record as the second and final ER append, then perform zero operations.

The package must not rerun controller, selector, the 18-row Git ledger, the four Git file acquisitions, self-check, tests, CodeGraph, or validator. It must not read terminal/source/other fresh or old roots, access physical inputs, modify artifacts, or access any device/network path. The activation parent expected by this next package remains `f28aa4a968549a2f9ba1fa55fc45d9294026df43`; there is no evidence child to use as parent.
