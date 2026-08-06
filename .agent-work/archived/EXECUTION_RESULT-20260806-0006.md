# EXECUTION_RESULT review archive — REF-G4-06 source-attestation v2

**Archive status:** `REVIEWED_REJECTED_TERMINAL`

**Archive timestamp UTC:** `2026-08-06T00:06:06Z`

**Source owner/type:** `Executer / EXECUTION_RESULT`

**Reviewed task:** `REF-G4-06-SOURCE-ATTESTATION-V2`

**Reviewed contract:** `G4-R6-SOURCE-ATTESTATION-V2-ENGINEERING-V1`

**Source checkpoint:** `f23f74a6fe1bee6a04131e75ef8969e8f4d0b3af`

**Original source bytes:** `6784`

**Original source SHA-256:** `1807fd44f5772d0f1ca1f145eb418f66974b5531b0198e183cc3d343729edb85`

**Terminal disposition:** `REJECTED_SOURCE_ATTESTATION_V2_FULL_ORDER_INTEGRATION_MASS_REGRESSION`

**Exact next stop:** `RETURN_TO_ORCHESTRATOR_FOR_CROSS_ARCHITECTURE_OWNER_REASSESSMENT`

**Execution authority:** `historical_non_executable`

## Frozen execution handoff

Activation HEAD为 `f23f74a6fe1bee6a04131e75ef8969e8f4d0b3af`；accepted start blobs为source `0015d7ce2f2a5dde9118478f98c929020a474a01`与test `2a60a987dda02675c2eddc7d8260d61a8f68edc3`。Historical Q1只执行ref identity与ancestry isolation检查；实现内容读取/复用、merge、cherry-pick、rebase与copy计数均为0。

Candidate exact paths：

- `src/camera_based_rgbww_optimizer/optimization/p7_td_b_r6_stage_gate.py`
- `tests/test_p7_td_b_r6_stage_gate.py`

实际diff为source 177 additions、test 122 additions，总计299 changed lines。未修改PLAN/FULL/PLAN-FULL/archive/debug/GUIDE/RESEARCH/config/wrapper，未commit。

Candidate freeze：

| Path | Mode | Bytes | SHA-256 |
| --- | --- | ---: | --- |
| `src/camera_based_rgbww_optimizer/optimization/p7_td_b_r6_stage_gate.py` | `0644` | 109143 | `00650231ff64645716212cb8c185d7e5bd5942d110109ca6b3fb9c4d47405c78` |
| `tests/test_p7_td_b_r6_stage_gate.py` | `0644` | 161053 | `6354c74e357117e0b91fa68403dbe2ea5d30d162275a6894cc61e24894431719` |

Focused后冻结candidate；最终full wrapper再次核验相同SHA，freeze后source/test mutation为0。

## Validation ledger

1. Targeted v2：3 tests，exit 0，2.415s。
2. Stage-gate focused：56 tests，exit 0，562.852s；evidence `/Volumes/4T/temp/rgbww-optimizer/g4-v2-focused-stage-gate-f23f74a`。
3. Harness/tool-yield bounded correction：重复PID 9064与14704被终止，不计有效验证；唯一PID 24415完成56/56。没有candidate mutation。
4. Related focused：95 tests，exit 1，2 failures + 8 errors，27.756s；evidence `/Volumes/4T/temp/rgbww-optimizer/g4-v2-focused-related-f23f74a`。ER将其限定为既有governance-lineage/path identity baseline，不含新的stage-gate/terminal owner failure。
5. Compileall、diff-check、scope、forbidden scan、CodeGraph全部通过。
6. Final full：invocation/retry `1/0`，984 tests，293.094s，exit 1，5 failures + 220 errors。

Final full visible Terminal identity：

- token/root：`g4-r6-source-attestation-v2-full-f23f74a-20260805T234530Z` / `/Volumes/4T/temp/rgbww-optimizer/g4-r6-source-attestation-v2-full-f23f74a-20260805T234530Z`
- PID/TTY：`95333` / `/dev/ttys014`
- started/finished：`2026-08-05T23:46:04Z` / `2026-08-05T23:50:57Z`
- wrapper：2195 bytes，mode 0700，SHA-256 `7d8c906f51519ef25234373b2a8c7cc6dbc76293d5cae8a9c697edc5c99275ee`
- terminal seal：478 bytes，SHA-256 `43c9760900449c0de24c15b2f93415e51e34453ae0524398389e5dfabd66bce5`
- stdout：4327 bytes，SHA-256 `fcdd529c8f730c74a7193339c7919327ce384c4354788967cc40120ea0ac77c2`
- stderr：491176 bytes，SHA-256 `d1686c3b20baea5fb91a1bd0cec472144817a2b79e2fa3112a369b0fd3aa7318`
- `validation.exit`：2 bytes，SHA-256 `4355a46b19d348dc2f57c046f8ef63d4538ebb936000f3c9ee954a27460dd865`，value 1。
- liveness 3/3；owner已结束；automation已删除。

## Failure evidence accepted by Planner

- Candidate guard failure：digest subcase expected `source_qualification_digest_drift`，observed `source_reference_drift`。
- Full-order/integration mass regression：约220 errors dominated by `committed_source_candidate_blob_drift` during `SyntheticGitRepository` initialization despite isolated focused 56/56。
- 该结果超出允许baseline。Other governance/mode failures不能抵消candidate-owned failure。
- Full retry为0，且不得重跑、repair、commit或把candidate当package input。
- Q1与本v2在committed-source candidate owner boundary的重复错误要求跨架构owner reassessment。

## Zero-effect ledger

- Package prepare/describe/replay/probe/root access/create：0。
- Formal/replacement/release：0。
- Backend/device/network/camera/Ray/strip/capture/light：0。
- Analysis/G4-07/TD-C：0。
- Candidate commit：0。
- Scientific/device/formal/package/release result：无。
- Active validation owner/process/automation：0。

Planner disposition：

`REJECTED_SOURCE_ATTESTATION_V2_FULL_ORDER_INTEGRATION_MASS_REGRESSION`

Cross-architecture status：

`CROSS_ARCHITECTURE_OWNER_BOUNDARY_REASSESSMENT_REQUIRED`

本archive永久为 `historical_non_executable`；它只保存冻结handoff与review evidence，不授权任何执行、retry、commit、package、formal、release、device或stage entry。
