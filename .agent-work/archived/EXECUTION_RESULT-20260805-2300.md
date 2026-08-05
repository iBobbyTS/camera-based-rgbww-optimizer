# EXECUTION_RESULT archive — immutable Q terminal rejection review

**Archive status：** `HISTORICAL_NON_EXECUTABLE_REVIEWED_REJECTED_EVIDENCE`

**Archive timestamp：** `2026-08-05T23:00:00Z`

**Source owner/type：** Executer / `.agent-work/EXECUTION_RESULT.md`

**Reviewed scope：** committed Q `74f5c2ea0188bcca633193d1ee5775b951ff0a9d` topology validation

**Source checkpoint：** `961c1383e8843e5cc2705ce85591e8a6d82410ac`（ER-recorded docs-only identity tip）

**Source bytes：** `6624`

**Source SHA-256：** `ab227e15f00897148e6862aa1d949ebf37e7eec44bd20fb859dcce818f2b5130`

**Terminal disposition：** `REJECTED_IMMUTABLE_Q_TOPOLOGY_VALIDATION_COMMITTED_SOURCE_CANDIDATE_BLOB_DRIFT`

**Frozen evidence：** topology invocation `1`; 12 tests / 23.011s / exit 1 / 32 errors；dominant `committed_source_candidate_blob_drift`; full invocation/retry `0/0`; terminal seal SHA-256 `0cc8671eb3414aed26a8f067efb5c76d70fc2d2b6c51995e7ac04c984394728b`.

**Exact next branch/stop：** qualification branch historical-only；return orchestration branch to activation A；`WAIT_FOR_SUPERVISOR_AFTER_IMMUTABLE_Q_REJECTION`

**Execution property：** `historical_non_executable`

本 archive 不授权 repair、amend、Q2、rerun、review、promotion、package、formal、release、device或科学阶段。以下为 reviewed live EXECUTION_RESULT 的完整原文。

---

# EXECUTION_RESULT

## REF-G4-06 immutable qualification promotion — committed Q identity handoff

**Contract:** `G4-R6-IMMUTABLE-QUALIFICATION-PROMOTION-V1`

**Selected architecture:**
`DEDICATED_NON_PRODUCTION_QUALIFICATION_CHECKPOINT_WITH_EXACT_FAST_FORWARD_PROMOTION`

**Terminal status:**
`CANDIDATE_Q_COMMITTED_TOPOLOGY_VALIDATION_FAILED_WAITING_PLANNER_REVIEW`

**Qualification status:** `VALIDATION_FAILED_WAITING_PLANNER_REJECTION`

### 1. Frozen intake and implementation scope

- Qualification branch: `codex/g4-r6-immutable-qualification-q1`.
- Activation commit A:
  `6ed06636d382db7a66b83096f52e8dcbfa0d3263`.
- A parent:
  `49ad47eceb1bb987eb83107deb8c892d2928c6c5`.
- Accepted start source blob:
  `0015d7ce2f2a5dde9118478f98c929020a474a01`.
- Accepted start test blob:
  `2a60a987dda02675c2eddc7d8260d61a8f68edc3`.
- Preflight retained the existing canonical committed-source attestation owner in
  `p7_td_b_r6_stage_gate.py`; no module, controller, schema, runner, broad ignore,
  allowlist, or parallel identity owner was added.
- Q diff summary: `63 insertions`, `20 deletions`, exact two authorized paths.
- Q-before-test `git diff --check`: exit `0`.

### 2. Immutable qualification commit Q

- Q commit:
  `74f5c2ea0188bcca633193d1ee5775b951ff0a9d`.
- Q tree:
  `c50e09129e61bcf1e02b2cd7397ffb1321345a63`.
- Q direct parent:
  `6ed06636d382db7a66b83096f52e8dcbfa0d3263`.
- Q parent count: `1` (non-merge).
- Q subject:
  `fix(stage-gate): bind immutable qualification checkpoint`.
- Q exact changed paths:
  1. `src/camera_based_rgbww_optimizer/optimization/p7_td_b_r6_stage_gate.py`
  2. `tests/test_p7_td_b_r6_stage_gate.py`
- Q was committed before any test, compile, import, syntax probe, candidate code
  execution, or CodeGraph sync.
- Q amend/rebase/rebuild/Q2 count: `0/0/0/0`.
- Source/test post-Q mutation count before this handoff: `0`.

### 3. Q source/test identity

| path | mode | blob OID | bytes | SHA-256 |
| --- | --- | --- | ---: | --- |
| `src/camera_based_rgbww_optimizer/optimization/p7_td_b_r6_stage_gate.py` | `100644` | `0d8de0de2dc3e1a2a693066872dd9d5a60745412` | 101087 | `7ef4215d52602c70c61d0f086d6776d4fb79829afda32c44da9a9947b0241852` |
| `tests/test_p7_td_b_r6_stage_gate.py` | `100644` | `4f5f275e9f250f3c67bd4c9420ffb5fb7e1dc6fa` | 154972 | `4b2cb8b49ed51ecfb918fa535ae978f0d135f7d74990a3f565a129b5433b1146` |

Read-only `git ls-tree`, `git cat-file`, `git show`, filesystem bytes/SHA, and
`git hash-object` agreed for both paths. Worktree was clean immediately before
this ER handoff; after writing this handoff, only
`.agent-work/EXECUTION_RESULT.md` is expected to be dirty.

### 4. Historical isolation and zero counters

- Historical ref identity check used only `git show-ref --verify`; expected commit
  matched `3dc2fa2639ee19b1c10ec55e2412836527c8973b`.
- Read-only ancestry check result:
  historical commit is not an ancestor of Q (`merge-base --is-ancestor` exit `1`).
- Historical candidate diff/tree/blob/file read count: `0/0/0/0`.
- Historical candidate apply/copy/merge/cherry-pick/rebase/reuse count:
  `0/0/0/0/0/0`.
- Candidate test/unittest/compileall/py_compile/import/syntax-probe before Q:
  `0/0/0/0/0/0`.
- Candidate topology test invocation/tests/errors after Q: `1/12/32`.
- Candidate AUTH/PROV, stage-gate focused, terminal focused, compileall,
  CodeGraph and scope gates after Q: `0/0/0/0/0/0` because topology failed
  closed.
- Full invocation/retry: `0/0`.
- Package prepare/describe/replay/probe/root access/create: `0/0/0/0/0/0`.
- Formal/release/device/network/camera/Ray/strip/capture/analysis access:
  `0/0/0/0/0/0/0/0/0`.
- External experiment payload access: `0`.
- Human goal/GUIDE/scientific completion: `false/false/false`.

### 5. Read-only identity extraction harness note

The first post-Q identity-extraction shell used the zsh-special variable name
`path`, which temporarily shadowed `PATH` inside that command and caused its
loop tools to return `command not found`. It wrote no files, ran no candidate
code or test, and changed neither Q nor the worktree. The same read-only identity
extraction was rerun once with absolute tool paths and produced the identities
recorded above. This harness correction is not a candidate repair or validation
retry.

### 6. Stop

Orchestrator recorded Q identity in docs-only commit
`961c1383e8843e5cc2705ce85591e8a6d82410ac` and independently passed the
PLAN-required prevalidation gate. The subsequent committed-Q topology gate
failed closed:

- Visible Terminal token / PID / TTY:
  `g4-r6-immutable-q-validation-74f5c2e-20260805T224727Z` / `78015` /
  `/dev/ttys014`.
- Evidence prefix:
  `/Volumes/4T/temp/rgbww-optimizer/g4-r6-immutable-q-validation-74f5c2e-20260805T224727Z`.
- Started / finished UTC:
  `2026-08-05T22:52:01Z` / `2026-08-05T22:52:24Z`.
- Exact gate: meaningful committed-Q topology group; `12` tests in `23.011s`;
  exit `1`; `32` errors.
- Dominant stable error code: `committed_source_candidate_blob_drift`.
- `topology.meta`: 454 bytes; SHA-256
  `c118370b86123b0d19364809c2613f8a7d82204c4c4eb04a4c125113ad9373ee`.
- `topology.stderr.log` and `topology.combined.log`: each 68533 bytes;
  SHA-256
  `56d89e4f268c1f73f1a3577b4dd644a46655a2eaf51243bafce2386fec947fca`.
- `terminal-seal.txt`: 495 bytes; SHA-256
  `0cc8671eb3414aed26a8f067efb5c76d70fc2d2b6c51995e7ac04c984394728b`;
  status `FAILED_topology`, exit `1`.
- `validation.exit`: 2 bytes; SHA-256
  `4355a46b19d348dc2f57c046f8ef63d4538ebb936000f3c9ee954a27460dd865`;
  value `1`.
- Full invocation/retry: `0/0`; the exact known governance-lineage baseline
  branch was never reached. This topology result is therefore outside the only
  allowed full-suite baseline.
- Fail-fast left AUTH/PROV, stage-gate focused, terminal focused, compileall,
  CodeGraph, scope and full gates unrun. No test or validation was retried.
- Source/test blobs remained
  `0d8de0de2dc3e1a2a693066872dd9d5a60745412` /
  `4f5f275e9f250f3c67bd4c9420ffb5fb7e1dc6fa` in the terminal seal. Source/test
  mutation, Q amend, Q2, repair and alternate candidate counts remain
  `0/0/0/0/0`.
- Package/formal/release/device/network/camera/Ray/strip/capture/analysis effects
  remain `0`; no scientific, device, formal, package or release result exists.
- The visible Terminal owner ended; Orchestrator removed its automation.

Executer requests that Planner reject Q under the PLAN's committed-identity
failure branch, preserve the qualification branch as historical-only, and not
repair or rerun this candidate. Human goal, GUIDE completion and scientific
completion remain false.

`RETURN_FOR_COMMITTED_Q_VALIDATION_REVIEW`
