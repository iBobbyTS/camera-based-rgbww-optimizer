# P7 retained-R3 Option B S1-C1-C1 report-matrix path failure review

**Planner 日期：** `2026-08-01`

**Reviewed reference task：** `REF-P7-25-R2-B3-C3-C4-R5-R1-C1-R2-R1-C2-S1-C1-R1-D1-D2-C1-R2-C1-S1-C1-C1`

**Reviewed contract：** `P7-TD-B-RETAINED-R3-OPTION-B-B3-C3-C4-R5-R1-C1-R2-R1-C2-S1-C1-R1-D1-D2-C1-R2-C1-S1-C1-C1-CURRENT-INPUT-IDENTITY-OWNER-CORRECTIVE-SUPERSESSION-V1`

**Decision：** `REJECTED_REPORT_MATRIX_PATH_MISBINDING_AFTER_STRICT_LOAD`

## 1. Reviewed scope and frozen identities

Activation commit `0049e2043889ee3e8cba99ec39046fcc1712a161` has direct parent `01e4f1477f90fa34d69fea3e0fd63d227f82a7ae`, subject exact `chore(plan): freeze current input identity ownership`, and exact ordered changed paths:

1. `.agent-work/FULL_PLAN_REFERENCE.md`;
2. `.agent-work/PLAN.md`;
3. `.agent-work/PLANS/20260801-1605-p7-retained-r3-d2-c1-r2-c1-s1-c1-identity-owner-failure-review.md`.

The activation archive is `6535` bytes with SHA-256 `b1f49830e0100e2e0f7736028f3ccbd88687de38c3fb7484830d7f7020c0216f`.

Evidence commit `220e888664ab7b232a5718317cf3111c6aa31a0d` is the direct child of activation, subject exact `chore(evidence): seal identity-owner corrective supersession`, with sole changed path `.agent-work/EXECUTION_RESULT.md`.

Planner independently consumed the complete committed files through physical EOF:

- activation `.agent-work/PLAN.md`: `16031` bytes, SHA-256 `a035e160640606ba32bab9cf9ac62ed4c34fa8d54a2ef27a5b621c0b69af9323`;
- activation `.agent-work/FULL_PLAN_REFERENCE.md`: `463285` bytes, SHA-256 `8397fb97bdbb910d2764981f3ea43f53ff4977c7d568aea40fab8eb9a9998d22`;
- evidence `.agent-work/EXECUTION_RESULT.md`: `1550853` bytes, SHA-256 `438c95e27261fc5be49b05e500c185879e558e7fecbae86be7546fd6613ee5d3`.

The complete two-section evidence suffix, beginning with the prior-S1 durable seal and extending through physical EOF, is `5997` bytes with SHA-256 `b63b8174188e6a4364cdf956fbf790b6d63aeae176d31daab791c5044d259fe8`.

## 2. Accepted gates and failed gate

The candidate passed exact activation topology/archive identity. Current PLAN/FULL identity was correctly owned by the activation Git objects, not predecessor fields under `reviewed_execution`: PLAN `16031` bytes / `a035e160...`; FULL `463285` bytes / `8397fb97...`. Accepted PLAN and FULL parsers each passed exactly once, and the required FULL machine-state subset passed.

The evidence-parent ER baseline passed exact identity and complete-EOF suffix checks. The first append durably sealed the prior S1 bare-marker zero-effect failure before report access. The fixed report and seal were each raw-read once, passed exact identity and seal-target checks, and each strict JSON load passed once:

- `01-owner-expectation-attribution.json`: `41685` bytes, SHA-256 `923f32afae0f375469d03a6b6a18a71261c19e7bcfefcd0bb041bdfde11b849a`;
- `01-owner-expectation-attribution.sha256.json`: `166` bytes, SHA-256 `068ee79657f4765928b80909514d37b431d779fc2a6ccd914c127e1453c08c49`.

The sole planned matrix-freeze expression then indexed the strict-loaded report at top-level `$.ledger_rows` and failed with `KeyError: 'ledger_rows'`. Matrix freezes and structural checks therefore remained `0/0`. The second allowed append wrote the fail-closed handoff. Total ER appends were exactly `2`; retry/fallback and post-final-append operations were all zero.

## 3. Independent fixed-report schema evidence

Planner read only the two already named fixed evidence files and did not enumerate, stat, glob, search, modify, or reseal their root. The report top-level keys include `matrix`, `ledger_binding_proof`, and the stated conclusions; there is no top-level `ledger_rows`.

The exact path roles are:

- report matrix collection: `$.matrix`, exact JSON array length `18`;
- source-ledger binding claim: `$.ledger_binding_proof.frozen_path == "$.ledger_rows"`;
- source-ledger owner: `$.ledger_binding_proof.owner == "PLAN_MACHINE_ROOT"`;
- binding type/cardinality/same-object: `builtins.tuple` / `18` / `true`.

At actual report path `$.matrix`, strict inspection finds ordered indices `1..18`, match count `15`, mismatch indices `7/15/18`, first mismatch `7`, selector/Git-attempt/Git-process counts `18/18/18`, retry/fallback `0/0`, all zero locks zero, and production-owner/lineage/eligibility/release conclusions false with retained R3 `RETAINED_UNVALIDATED_UNCONSUMED`. The row roles/kinds/matches are complete and ordered; mismatches are activation changed paths at row 7 and the two baseline patch SHA rows at 15 and 18.

These are independent Planner schema facts only. The failed execution did not freeze or structurally verify the matrix, so it receives no synthetic engineering attribution acceptance credit.

## 4. Findings and decision

1. `S1-C1-C1-PATH-001`: `$.matrix` is the report's 18-row collection path. `$.ledger_rows` is not a report collection path.
2. `S1-C1-C1-BINDING-002`: the literal `$.ledger_rows` remains required evidence only as the value of `$.ledger_binding_proof.frozen_path`, proving the upstream PLAN machine-root owner. Replacing that semantic assertion with `$.matrix` would be a second, opposite misbinding.
3. `S1-C1-C1-LIFECYCLE-003`: activation ownership, accepted parsers, prior-S1 durable seal, report/seal identities, strict loads, fail-closed second append, zero locks, and EOF lifecycle are accepted. They need not be repeated except for the ordinary activation/parser and new evidence-parent guards required by the successor.
4. `S1-C1-C1-CREDIT-004`: the complete 18-row matrix gate did not execute, so the original execution contract and synthetic attribution facts remain unaccepted. No production-owner, lineage, manifest-truth, eligibility, release, or device credit is created.

The reviewed execution is rejected only at the report-matrix path binding. This is an engineering/provenance packaging correction; no Advisor scientific escalation and no Human device authorization are required.

## 5. Exact next branch

The sole next branch is `REF-P7-25-R2-B3-C3-C4-R5-R1-C1-R2-R1-C2-S1-C1-R1-D1-D2-C1-R2-C1-S1-C1-C1-C1`. It must:

1. use the Orchestrator activation Git objects as current PLAN/FULL identity owners, pass the accepted parsers once each, and freeze the evidence-parent ER at `220e888...` through physical EOF;
2. read only the same fixed report and seal once each, verify their unchanged identities and strict JSON loads, then freeze the report matrix exactly once from `report["matrix"]` (`$.matrix`);
3. separately verify `report["ledger_binding_proof"]["frozen_path"] == "$.ledger_rows"` and the remaining owner/type/cardinality/same-object facts; never index `report["ledger_rows"]`;
4. verify the complete ordered 18-row facts and structural identity, then append exactly one success supersession containing the full matrix inline, or exactly one fail-closed handoff;
5. stop with zero operations after that append.

The branch must not repeat the prior-S1 durable append, rerun controller/selector/Git ledger/Git acquisition, inspect root/terminal/source/physical inputs, modify artifacts, call self-check/tests/CodeGraph/validator/release, access network/devices, modify PLAN/FULL/archive/code/tests/skill/docs/GUIDE, or commit.
