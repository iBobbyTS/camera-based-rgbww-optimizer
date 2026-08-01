# P7 retained-R3 Option B B3-C3-C4 V3 M1 patch-byte review

**Planner review date:** `2026-08-01`

**Reference task:** `REF-P7-25-R2-B3-C3-C4`

**Reviewed contract:**
`P7-TD-B-RETAINED-R3-OPTION-B-B3-C3-C4-SOURCE-FILE-IDENTITY-ONLY-FRESH-VERIFICATION-V3`

**Decision:**
`REJECTED_INSUFFICIENT_DURABLE_M1_PATCH_BYTE_DIAGNOSTIC_PURE_GIT_DIAGNOSTIC_REQUIRED`

## 1. Reviewed topology and scope

- Activation `d2c9794d566259660506925c49672b6cb55fdb14` is the direct child of
  `080f314eb8f7ab0829d08bed941fbf8177ab322e`, has the exact subject
  `chore(plan): retry B3-C3-C4 source identity only`, and changes exactly
  `.agent-work/FULL_PLAN_REFERENCE.md`, `.agent-work/PLAN.md`, and
  `.agent-work/PLANS/20260801-0722-p7-retained-r3-b3-c3-c4-v2-source-parent-mode-review.md`.
- Evidence `7d2e9ac93f388f5d9204ed3243f4cf8b16dfc83f` is the activation's direct child, has subject
  `chore(evidence): record C4 V3 patch-byte stop`, and changes only `.agent-work/EXECUTION_RESULT.md`.
- The reviewed PLAN has bytes `20452` and SHA-256
  `35e46affbc59e29d76d93b284c88093f1f8911e4d2a9a4dd8f51f80f66eb66ed`.
- The worktree was clean and `7d2e9ac` was HEAD at review start; no later commit existed.

This review read only committed Git objects and repository-owned PLAN, FULL, ER, and relevant review archives. It did not read, stat, list,
glob, search, or reuse the V3 failed root, any earlier failed/external package root, the retained-R3/candidate root, C1 input root, or the
production/test source files. It did not run a controller, test, CodeGraph, validator, retained audit, release operation, network/DNS/
environment/credential access, device, camera, Ray, strip, cleanup, capture, FORMAL, public analyzer, TD-C, sentinel, P8, firmware, or
deployment command.

## 2. ER integrity and execution evidence

The parent ER blob is exact bytes `1350396`, SHA-256
`1fa058cf4d9b468676925d4d7d2d3b8b6a2bb24d86ebcb90609d6f9672fecdf4`. The evidence ER blob is exact bytes `1354521`, SHA-256
`50fd97882b243d926ab7f4fd7b083c82068917aa7293f06a6d659b2449cb7ee9`. The parent is an exact byte prefix of the evidence blob. The single
physical-EOF suffix is exact bytes `4125`, SHA-256
`6a8df353e1ceebb12b2ad446fbbbd87bc12b75eef35e5c37e71d20ba5a86baaa`, contains one heading and one strict JSON handoff, and ends with one
newline. This satisfies the ER-only and physical-EOF evidence topology.

The payload binds the exact activation, reports one fresh V3 root, `reuse_permitted=false`, one file-backed non-TTY controller invocation,
retry/fallback `0/0`, and source controller pre/post identity equality. The frozen source file itself matched exact path, regular
non-symlink type, bytes `26644`, SHA-256 `0889b150daae9ba6313aea9f6502e09bcf838eb70312a3595c056edb0be1b09b`, and mode decimal `384`;
all source-parent lstat/stat/mode reads and assertions were `0`, so the V3 source-file-only correction was obeyed through that gate.

The first failure is only the string `M1 patch bytes`. The payload does not durably record the exact Git argv actually invoked, the expected
patch bytes/SHA, the observed stdout bytes/SHA, stderr, exit code, or the relevant object identities at the failure. Therefore it proves a
correct fail-closed stop but cannot distinguish a controller command-rendering/comparison defect from actual committed-provenance drift.
No actual drift finding is accepted.

All later stages remained unentered: focused invocations/tests `0/0`, full invocations/tests `0/0`, synthetic runs/processes/input writes/
output writes/replays all `0`. Retained audit, canonical validator, eligibility, release and every network/device-adjacent route remained
zero. The V3 failed root is immutable and non-reusable.

## 3. Decision and exact next branch

V3 is rejected as a completed verification because its self-check did not finish. Its source-file-only result and zero-later-stage locks are
accepted as factual, but `M1 patch bytes` is not accepted as proof of provenance drift.

The only next package is a pure Git-object diagnostic. It must use exactly this canonical argv, with no inferred or alternate flags:

`git diff --binary f2b38c530a6cbac5c29d761036eb3cd2a159f3b9 0f4c09e1b2b2afbf627f6f36d57a1a65847ab4a8 -- src/camera_based_rgbww_optimizer/utils/p7_retained_r3_real_manifest_domain_template.py tests/test_p7_retained_r3_real_manifest_domain_template.py`

It must persist the expected and observed argv, raw stdout bytes/SHA-256, stderr bytes/SHA-256, exit code, exact child/parent/subject/tree/path
and before/after blob identities, and a terminal classification. Expected canonical stdout is bytes `5874`, SHA-256
`6b26e49359f944bceafe5129b0b81a3d5600d400eae7d3b739c2baba12d6a5ca`. If all frozen object identities match and the exact command output
matches, classify the V3 failure as a controller command-rendering/comparison mismatch with no provenance drift. If object identities match
but rendered bytes differ, classify a Git command-rendering mismatch without declaring object drift. Only a mismatch in the frozen committed
object topology or blobs may classify actual provenance drift. Git command failure is indeterminate and must fail closed.

The diagnostic must not run the remaining self-check, focused/full tests, synthetic integration, real retained audit, validator, eligibility,
release, or any network/device work. It must use a fresh activation-derived root, retry/fallback `0`, append one physical-EOF ER handoff, and
stop at Planner review.

**Exact next branch:**
`B3_C3_C4_M1_PATCH_BYTE_PURE_GIT_DIAGNOSTIC_WAITING_ORCHESTRATOR_ACTIVATION`.

维护性判断：本分支只补齐一次性 Git-object 证据，不改 production/test、manifest owner、validator 或 eligibility owner；无需架构重构。
