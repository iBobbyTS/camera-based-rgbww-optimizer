# EXECUTION_RESULT

## REF-G4-06 atomic materialized runtime consumer migration

**Contract:** `G4-R6-ATOMIC-MATERIALIZED-RUNTIME-CONSUMER-MIGRATION-V1`

**Status:** `REJECTED_TARGETED_CANDIDATE_OWNED_NON_GREEN_FAIL_CLOSED`

**Planner stop:** `RETURN_FOR_G4_06_ATOMIC_MATERIALIZED_RUNTIME_CONSUMER_MIGRATION_REVIEW`

## Activation and maintainability preflight

- Branch: `codex/g4-r6-owner-alignment-large-change`.
- Activation HEAD: `ecfa0ec71aef02aeb8b48edad4496009bcae74b8`.
- Intake worktree: clean; no pre-existing implementation/test changes.
- Machine state: PLAN/FULL/PLAN-FULL are exact `1/1/1` for `REF-G4-06-MATERIALIZED-RUNTIME-CONSUMER-MIGRATION` and contract `G4-R6-ATOMIC-MATERIALIZED-RUNTIME-CONSUMER-MIGRATION-V1`; PLAN executable=true, FULL/PF executable=false.
- `.codegraph/` existed before intake. CodeGraph blast-radius plus accepted-tree symbol inventory found production consumers only in the three authorized production modules; additional production consumer count: `0`.
- Maintainability boundary: the existing stage-gate coordinator is large, so this candidate is limited to one pure canonical materialized-runtime construction seam and its exact schema/validation helpers. Measure and terminal remain consumers. No package, capture, thermal algorithm, persistence, routing, device, or scientific ownership is moved.
- Large-change route remains the existing branch and the single non-executable `ATOMIC_PUBLIC_MATERIALIZED_RUNTIME_CONSUMER_MIGRATION` PLAN-FULL section. Atomic split is not used.

## Frozen six-path rollback ledger

| path | mode | bytes | SHA-256 | activation HEAD blob |
| --- | ---: | ---: | --- | --- |
| `src/camera_based_rgbww_optimizer/optimization/p7_td_b_r6_stage_gate.py` | `100644` | 101205 | `97b0a88c338b659ca887dfb626eee11ff96f52712b16a2d6f8b8b7de059298b7` | `0015d7ce2f2a5dde9118478f98c929020a474a01` |
| `src/camera_based_rgbww_optimizer/optimization/measure_p7_thermal_diagnostics.py` | `100644` | 198246 | `0ae294b08317983abbed838aac355233d12eaf0d602192229aa92ce755f1041f` | `90000ff11a6603fc63515061d391200a46765380` |
| `src/camera_based_rgbww_optimizer/optimization/p7_td_b_r6_terminal.py` | `100644` | 49180 | `4e38d97000f7e908fb56db5ac731e28182f7759f45b394881d66a1791a144e3e` | `2d22fc6db86df777f3eb9fe8f668b4fd96731be8` |
| `tests/test_p7_td_b_r6_stage_gate.py` | `100644` | 152759 | `f86c8dd121b549cf33f8e537454091859e60a466ebed70ff1f077b30defe5add` | `2a60a987dda02675c2eddc7d8260d61a8f68edc3` |
| `tests/test_p7_thermal_diagnostics.py` | `100644` | 249159 | `6cc395d76ea5ad1182f4671b2eb401bedb54d0b6a64dc4b1120a32ae0f9dbb46` | `272eacf4c302af5d64483620978411998497b242` |
| `tests/test_p7_td_b_r6_terminal.py` | `100644` | 35200 | `034d4b828c73880d47b390ea63251ee408299cca95bd5a0071b74be12e7cc1d5` | `9cf15ec1952b7a6162b60c7f586dfd80ba8506b6` |

Executer rollback is not authorized. Historical candidate implementation/ref/diff was not read or used.

## Consumer and fixture intake map

- Production owner: stage-gate `CommittedSourceAttestation`, serializer, activation builder, materializer, and validator.
- Measure consumers: shutter-ledger materialized recognition, `validate_authorized_execution_plan`, `run_validated_td_b_r6_runtime_contract`, `run_authorized_plan`, and `execute_plan` chain.
- Terminal consumers: `is_r6_materialized_plan` and replay/finalizer validation.
- Fixture constructors: `SyntheticGitRepository.future_activation`, the stage-gate synthetic pure helper, thermal `_r6_materialized_plan_for_test`, and terminal `materialized_plan`. All handwritten authority/attestation construction will be removed or delegated to production owner.

## Validation ledger

Qualification started once and stopped at targeted. Source/test/support write cap is now `0`; no same-candidate repair or rerun is permitted.

## Frozen implementation contract delta

- Old `p7_td_b_r6_committed_source_attestation_v1` → `v2`; old flat identity aliases are removed. The serialized attestation now has ordered nested `verified_parent_identity`, `code_owner_identity` (direct parent, subject, changed paths, blob OIDs), `current_candidate_identities`, `live_activation_identity`, `candidate_references_sha256`, and `post_child_linear_ledger` fields.
- Old `p7_td_b_r6_future_plan_activation_v2` → `v3`; activation no longer carries top-level code/live checkpoint/tree aliases. Old `p7_td_b_r6_plan_bound_authority_v1` → `v2`; its exact authority key set is still production-owned.
- `build_committed_source_attestation` and `construct_materialized_runtime_contract` are pure production-owner factories. `validate_materialized_runtime_plan` and `validate_future_activation` reject old schema, unknown/missing fields, wrong native types, identity/role/subject/path/blob/reference-digest/ledger drift before any downstream consumer or backend.
- Measure delegates R6 claim recognition/validation to stage-gate public helpers; terminal recognition delegates the same exact validator. No consumer copies schema constants, serializer, digest, or acceptance rules.
- Shared test support supplies only deterministic sample values and delegates all typed/schema construction to stage-gate production factories. Handwritten nested authority/attestation dictionaries in the three thermal/terminal fixture paths were removed.

At the qualification boundary, source/test/support write cap is now `0`; no implementation mutation or same-candidate rerun is authorized after a valid non-green gate.

## Targeted gate result and terminal stop

- Fresh validation root: `/Volumes/4T/temp/rgbww-optimizer/g4-r6-atomic-materialized-runtime-consumer-migration-20260806-214548`.
- Exact invocation was one `.venv/bin/python -m unittest` command selecting: canonical deterministic contract, old/new exclusivity and drift matrix, synthetic materialization, invalid activation/runtime probes, terminal exact recognition, thermal frozen-plan/runtime-context full-chain, and unknown-template precedence tests.
- Targeted result: `Ran 7 tests in 18.270s`; `6 passed, 1 failed`; process natural unittest exit `1`. Invocation/retry `1/0`.
- Failure identity: `tests.test_p7_td_b_r6_stage_gate.P7TdBR6StageGateTests.test_canonical_materialized_contract_is_deterministic_nested_and_json_native` at line 2391. The assertion expected strict dict equality after canonical JSON decode, but the decoder returns a `mappingproxy` for the nested mapping; this is candidate-owned and not an unrelated governance baseline. No production callback/effect occurred.
- Complete log: `/Volumes/4T/temp/rgbww-optimizer/g4-r6-atomic-materialized-runtime-consumer-migration-20260806-214548/targeted.log`; bytes `1038`; SHA-256 `c16e619f3c50fc175fac4df063210b03d4f196f50056fa781c52e9fcdf4d12ea`.
- The surrounding shell handoff attempted to assign the zsh readonly variable `status` after unittest completion; this did not alter the recorded unittest result or candidate source/test state. No second invocation was made.
- Per PLAN, stage-gate/terminal/thermal/related/compile/CodeGraph/diff/full gates were not run. No source, test, support, plan, GUIDE, RESEARCH, config, wrapper, package, formal, device, network, camera, Ray, strip, capture, or analysis files were changed after the targeted result.

**Planner stop:** `RETURN_FOR_G4_06_ATOMIC_MATERIALIZED_RUNTIME_CONSUMER_MIGRATION_REVIEW`

## Safety and external effects

- Package/formal/root/release/device/network/camera/Ray/strip/capture/analysis operations: `0`.
- Active process: `false`; active automation: `false`.
- Scientific result created: `false`; retained R3 remains `RETAINED_UNVALIDATED_UNCONSUMED`.
