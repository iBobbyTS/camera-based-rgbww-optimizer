# P7 retained-R3 B2 owner-API controller architecture reassessment

## 1. Reviewed scope and evidence

Planner reviewed the active contract
`P7-TD-B-RETAINED-R3-OPTION-B-B2-R2-C1-C1-C1-C1-C1-OWNER-API-CONFORMANCE-SOURCE-ROOT-QUALIFICATION-V1`,
the committed handoff at `b768737`, current HEAD `102c625eb73cf49d7e14af12663f967397e28fa2`,
and `.agent-work/debug/INDEX.md` plus the active record
`.agent-work/debug/active/20260731-p7-retained-r3-b2-controller-contract-drift.md`.

The immutable failed controller is
`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b2-r2-c1-c1-c1-c1-c1-owner-api-controller-c48d8dd-20260731T1052Z.py`,
bytes `21024`, SHA-256
`703e813f09c543a654c64423fd09c6c527211b87bb3045c8aa7ed1e1969d2078`.
It failed its single pre-dispatch gate with `RuntimeError:returncode_occurrence`:
an isolated negative specimen correctly contained `ledger.returncode`, but a later
whole-source occurrence counter treated that fixture text as dispatched runtime
code. Git calls, root creation, C1 reads, artifacts and all later work were `0`.

The controller/source and absent root remain immutable. They must not be read,
executed, imported, repaired, regenerated, reused, deleted or used as a template.

## 2. Findings

### REV-B2-OWNER-001 — runtime and negative-fixture AST domains are not separated

The latest predicate is individually plausible but its evidence domain is wrong.
Runtime acceptance and negative-specimen rejection share one source/text counter,
so a required negative proves the runtime invalid. Another local exclusion or
string-count adjustment would only move the same ownership defect.

### REV-B2-OWNER-002 — repeated external controllers own too many contracts

Five successive external packages have failed on copied activation identity,
logical/physical mode representation, omitted live root binding, guessed
`GitLedger.returncode`, and now mixed AST domains. The one-off controller currently
owns runtime composition, owner-schema inference, negative fixtures, evidence
lifecycle and qualification orchestration. Those responsibilities are not
independently tested before dispatch and cannot be made reliable by another
hand-written predicate patch.

### REV-B2-OWNER-003 — existing repo owners stop below the composition boundary

`p7_retained_r3_provenance_io.py` correctly owns file/root/Git I/O and
`p7_retained_r3_controller_preparation.py` correctly owns source preparation and
terminal-seal admission primitives. Neither owns the in-memory composition contract
that binds accepted return schemas, validates a runtime AST independently from
negative fixtures, confirms root-bound read identities, and orders failure sealing.
That missing owner is the common source of the repeated drift.

### REV-B2-OWNER-004 — no retained or scientific result was produced

The failure occurred before Git/root/C1 work. It does not validate or refute retained
R3, the canonical validator, eligibility, release, or any color-science branch.
This is an engineering ownership stop; Advisor and Human authorization are not
required.

## 3. Maintainability preflight and selected boundary

Directly extending the 458-line preparation owner would mix source mutation with
controller execution composition. Extending provenance I/O would mix pure AST and
lifecycle policy with physical I/O. Planner therefore selects one new pure-in-memory
helper and one dedicated test as the smallest enabling refactor:

- `src/camera_based_rgbww_optimizer/utils/p7_retained_r3_controller_conformance.py`
- `tests/test_p7_retained_r3_controller_conformance.py`

The helper may import only AST/hash/dataclass/typing primitives and the accepted
repo-owned dataclasses/functions needed to identify schemas. It must perform no
filesystem, Git, subprocess, environment, network, device, validator, release or
scientific operation. It owns only:

1. exact accepted return-schema conformance derived from and checked against the
   committed dataclass owners;
2. runtime AST analysis in a domain that cannot include negative-fixture ASTs;
3. pure-in-memory root/read identity-chain conformance;
4. generic lifecycle ordering through injected callbacks, including terminal,
   seal and admission dominance on PASS and FAIL.

It does not own manifest meaning, canonical-validator meaning, eligibility,
release, experiment selection or device authorization.

## 4. Decision and next branch

Decision:
`REJECTED_ARCHITECTURE_OWNERSHIP_REASSESSMENT_REPO_CONFORMANCE_OWNER_REQUIRED`.

Do not dispatch another external controller qualification. The sole next branch is
`REF-P7-25-R2-B2-P4`, contract
`P7-TD-B-RETAINED-R3-OPTION-B-B2-P4-CONTROLLER-CONFORMANCE-COMPOSITION-OWNER-V1`.
It authorizes exactly the two repo paths above, their tests and one focused commit.
It does not authorize any external controller, evidence-root creation, retained
read, real B2, manifest, validator, release, network or device action.

Activation identity is deliberately non-self-referential. The PLAN freezes the
activation commit's expected parent `102c625eb73cf49d7e14af12663f967397e28fa2`,
subject and exact three paths. The Executer obtains the implementation parent as
the clean current HEAD full SHA at runtime, then proves that HEAD matches the
frozen activation parent/subject/path tuple before editing. The Orchestrator must
not attempt to embed the activation commit's own not-yet-computable SHA into that
same commit and must not perform a second PLAN rewrite.

After P4 is independently accepted, a later Planner package may integrate the
committed owner into one successor qualification. P4 itself stops before that
integration and cannot imply it.

**Proposed FULL transition:** mark
`REF-P7-25-R2-B2-R2-C1-C1-C1-C1-C1` as
`REJECTED_RUNTIME_NEGATIVE_AST_DOMAIN_COLLISION_ARCHITECTURE_STOP`; add
`REF-P7-25-R2-B2-P4` as the sole task waiting for Orchestrator activation; set
`repair_v2_status=R2_EXTERNAL_CONTROLLER_REJECTED_P4_REPO_OWNER_ACTIVE`; preserve
`retained_r3_status=RETAINED_UNVALIDATED_UNCONSUMED`; keep all external-controller,
retained, real-B2, manifest, validator, release and device routes locked.

## 5. Planner handoff

Planner modified only this archive and `.agent-work/PLAN.md`. FULL, ER, GUIDE,
RESEARCH and debug state remain read-only. Orchestrator must independently review,
update FULL and create the exact activation commit before dispatching an Executer.

维护性判断：新增单一 pure-in-memory composition owner，明确位于 preparation 与
provenance I/O 之上且 validator/release/science 之下；只新增一个模块和一个 dedicated
test，消除反复复制 controller contract 的根因，不扩大设备或实验表面。
