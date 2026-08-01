# P7 retained-R3 Option B D2-C1-R2-C1-S1-C1 identity-owner failure review

**Planner 日期：** `2026-08-01`

**Reviewed reference task：** `REF-P7-25-R2-B3-C3-C4-R5-R1-C1-R2-R1-C2-S1-C1-R1-D1-D2-C1-R2-C1-S1-C1`

**Reviewed contract：** `P7-TD-B-RETAINED-R3-OPTION-B-B3-C3-C4-R5-R1-C1-R2-R1-C2-S1-C1-R1-D1-D2-C1-R2-C1-S1-C1-PARSER-BOUND-ZERO-EFFECT-AND-READ-ONLY-SUPERSESSION-V1`

**Decision：** `REJECTED_CURRENT_INPUT_IDENTITY_OWNER_MISBINDING_BEFORE_ACCEPTED_PARSERS`

## 1. Reviewed scope and frozen identities

Activation commit `079a768b1a4472a19241b60aed4fbe477132ad96` has direct parent `f28aa4a968549a2f9ba1fa55fc45d9294026df43`, subject exact `chore(plan): seal parser-bound attribution handoff`, and exact ordered changed paths:

1. `.agent-work/FULL_PLAN_REFERENCE.md`;
2. `.agent-work/PLAN.md`;
3. `.agent-work/PLANS/20260801-1556-p7-retained-r3-d2-c1-r2-c1-s1-marker-failure-review.md`.

The activation archive is `5348` bytes with SHA-256 `a6a4699cbbae8c4f53623d13fac16eabc521ed4997ff84c3e75f7e7bfd1cd5a6`; the activation/archive gates pass.

Evidence commit `01e4f1477f90fa34d69fea3e0fd63d227f82a7ae` is the direct child of activation, subject exact `chore(evidence): seal parser-bound attribution supersession`, with sole changed path `.agent-work/EXECUTION_RESULT.md`.

Planner independently acquired and consumed the complete committed files through physical EOF:

- activation `.agent-work/PLAN.md`: `13950` bytes, SHA-256 `770c96e5fb71b354e59f55b5fc160b5a683b006f510b4a5d0761513322de6a0e`;
- activation `.agent-work/FULL_PLAN_REFERENCE.md`: `462209` bytes, SHA-256 `c5f4539d4202ef4ba1696e57711e0176886ac178a858cc364611478f49be79ae`;
- evidence `.agent-work/EXECUTION_RESULT.md`: `1544856` bytes, SHA-256 `93937567107acb0a173a390dd30e057c487f7c171d1afc5cb970717ab36d5424`.

The complete last ER section, including its one leading newline through physical EOF, is `4091` bytes with SHA-256 `2ee711161b9a3111dfb0f3849842b4bf02028cc37da558f32efc6367c8b10f6c`.

## 2. Execution method and failure

The candidate passed activation topology/archive gates and acquired committed PLAN/FULL/ER raw bytes once each. Before either accepted parser call, it added an assertion comparing the current activation PLAN raw bytes against `PLAN_MACHINE_CONTRACT.reviewed_execution.committed_plan`.

That field is review provenance for the prior S1 object: `12284` bytes and SHA-256 `a6d6d69bc2890ffa4f9e5f5514de7630aa9fbef51743a93a73b837368f403f2e`. It is not the current activation input identity. The current PLAN is the Git object at `079a768...:.agent-work/PLAN.md`, whose independently verified identity is `13950` bytes and SHA-256 `770c96e...`. Treating the reviewed-object row as a current-input oracle caused `AssertionError: ('plan', 13950, 12284)` before `parse_plan_machine_contract` or `parse_full_plan_machine_state` ran.

Retry and fallback were both zero. Parser calls, ER suffix operations, report/seal reads, strict loads, identity checks, and matrix freezes were all zero. One allowed fail-closed ER append succeeded and post-append operations were zero. The ER handoff reports all 43 zero locks as exact zero, including controller, selector, Git ledger, Git file acquisitions, source, tests, validator, release, network, device, camera, Ray, strip, cleanup, formal, PLAN/FULL/archive writes, and implementation commit.

## 3. Independent report boundary check

Planner read only the two fixed allowed report paths. Their identities remain exact:

- `01-owner-expectation-attribution.json`: `41685` bytes, SHA-256 `923f32afae0f375469d03a6b6a18a71261c19e7bcfefcd0bb041bdfde11b849a`;
- `01-owner-expectation-attribution.sha256.json`: `166` bytes, SHA-256 `068ee79657f4765928b80909514d37b431d779fc2a6ccd914c127e1453c08c49`.

The seal targets the report and repeats its exact bytes/SHA. Strict JSON inspection confirms schema `p7_td_b_corrected_ledger_attribution_report_v1`, complete ordered indices `1..18`, matches `15`, mismatches `7/15/18`, first mismatch `7`, selector/Git attempts/processes `18/18/18`, retry/fallback `0/0`, PLAN-machine-root tuple binding with cardinality 18 and same-object identity, all report zero locks zero, and all production-owner/lineage/eligibility/release conclusions false. This review does not substitute for the still-unexecuted authorized read-only continuation or its durable full-matrix ER supersession.

## 4. Findings and decision

1. `S1-C1-IDENTITY-001`: current activation PLAN/FULL identity is owned by the activation Git objects selected by the activation contract. `reviewed_execution.committed_plan` and `reviewed_execution.committed_full` identify only the already-reviewed predecessor inputs and must never validate current activation inputs.
2. `S1-C1-PARSER-002`: the unauthorized identity assertion prevented both accepted parser calls, so the prior S1 zero-effect supersession and fixed-report continuation remain unexecuted.
3. `S1-C1-HANDOFF-003`: the fail-closed evidence lifecycle itself is valid: exact evidence child, sole ER path, complete physical-EOF record, retry/fallback zero, and post-append operations zero.
4. No production-owner, lineage, manifest-truth, eligibility, release, or device credit is created. `retained_r3_status` remains `RETAINED_UNVALIDATED_UNCONSUMED`.

The reviewed execution is rejected. This is an engineering identity-owner correction; no Advisor scientific escalation and no Human device authorization are required.

## 5. Exact next branch

The sole next branch is `REF-P7-25-R2-B3-C3-C4-R5-R1-C1-R2-R1-C2-S1-C1-R1-D1-D2-C1-R2-C1-S1-C1-C1`. It must:

1. freeze current PLAN/FULL raw identities exclusively from the activation Git objects named by the activation contract; predecessor identities under `reviewed_execution` are comparison/audit facts only;
2. pass those exact raw bytes directly to the accepted PLAN/FULL parsers and consume parser-owned values;
3. freeze the evidence-parent ER baseline and append the missing prior S1 durable zero-effect supersession;
4. only after that append succeeds, read the two fixed report files once each, complete strict identity/matrix verification, and append the full 18-row read-only supersession or one fail-closed terminal record;
5. stop with zero operations after the final append.

The branch must not rerun controller/selector/Git ledger/Git file acquisition, inspect any root/terminal/source/physical input, modify artifacts, call self-check/tests/CodeGraph/validator/release, access devices/network, modify PLAN/FULL/archive/code/tests/skill/docs/GUIDE, or commit.
