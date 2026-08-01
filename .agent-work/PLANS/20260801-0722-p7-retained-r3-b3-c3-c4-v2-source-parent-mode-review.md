# P7 retained-R3 Option B B3-C3-C4 V2 source-parent-mode review

**Planner review date:** `2026-08-01`

**Reference task:** `REF-P7-25-R2-B3-C3-C4`

**Reviewed contract:**
`P7-TD-B-RETAINED-R3-OPTION-B-B3-C3-C4-BASENAME-BOUND-BYTE-STABLE-POSTCOMMIT-VERIFICATION-V2`

**Decision:**
`REJECTED_CORRECT_FAIL_CLOSED_NONCONTRACTUAL_SOURCE_PARENT_MODE_ASSERTION_FRESH_V3_REQUIRED`

## 1. Reviewed scope and immutable inputs

- Activation commit: `23ab2d85ad0065b04fc5db35e2ec0b15f77ee7da`, direct child of
  `0f63ee43e34d0cab67b0975834984359d1218f61`, subject
  `chore(plan): resume B3-C3-C4 basename verification`.
- Activation exact changed paths:
  `.agent-work/FULL_PLAN_REFERENCE.md`, `.agent-work/PLAN.md`, and
  `.agent-work/PLANS/20260801-0707-p7-retained-r3-b3-c3-c4-s1-c1-eof-supersession-acceptance.md`.
- Evidence commit: `080f314eb8f7ab0829d08bed941fbf8177ab322e`, direct child of the activation,
  subject `chore(evidence): record C4 V2 source-mode stop`.
- Evidence commit exact changed path: `.agent-work/EXECUTION_RESULT.md` only.
- Reviewed active PLAN identity before this archive: bytes `20343`, SHA-256
  `31fa85881e885f2b4c878f48e7cf4f70a206d48360a3f8bcf695234d92dfa5b7`.

No failed package root, retained-R3/candidate root, C1 root, production source, or test source was read during this review. No controller,
test, validator, audit, release, network, DNS, environment, credential, device, camera, Ray, strip, cleanup, capture, formal, public analyzer,
TD-C, sentinel, P8, firmware, or deployment command was run.

## 2. Evidence integrity review

The parent ER blob has bytes `1346241` and SHA-256
`167146151120e189fa6684b7fc590e68cbccd53dce436e8441995be6a7db66ac`; the evidence ER blob has bytes `1350396` and SHA-256
`1fa058cf4d9b468676925d4d7d2d3b8b6a2bb24d86ebcb90609d6f9672fecdf4`.
The parent is an exact `1346241`-byte prefix of the evidence blob. The physical-EOF suffix is exactly `4155` bytes, SHA-256
`55dc6aabbf38e56d5297296eb363a3cdf04470460f021aba4d8d91f772451391`, and ends in newline byte `10`.
The suffix contains one heading and one terminal JSON payload. `git diff --check` for the evidence commit passed and the worktree was clean
at review start.

The terminal payload binds the exact activation and reports a fresh root, one source write, one non-TTY controller invocation, no stdin or
argv source transport, retry `0`, fallback `0`, and branch `BR-SELF-CHECK`. It reports exact-basename binding strategy
`EXACT_MACHINE_ROW_BASENAME_LOOKUP_NO_POSITION_INFERENCE`, required basename count `5`, and zero list-position reads, sorted-position reads,
generic selectors, guesses, and fallbacks. This is compliant with the basename-binding contract up to the failure point.

## 3. Finding and decision

The controller stopped on `SOURCE_PARENT_MODE_INVENTED_GATE`. The frozen source file itself independently matches the PLAN exactly:

- path: `/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-m1-r1-s2-s1-c1-e939b639f40e-source.py`
- regular file bytes: `26644`
- file mode: `0600` / decimal `384`
- SHA-256: `0889b150daae9ba6313aea9f6502e09bcf838eb70312a3595c056edb0be1b09b`

The V2 PLAN freezes only the source file path, bytes, SHA-256, and file mode. It does not require the source parent directory to be mode
`0700`. The payload reports that the invented expectation was decimal `448` (`0700`) while observed parent mode was decimal `493` (`0755`).
That assertion is non-contractual and must be removed. The source-file identity is accepted as matching, but V2 did not complete its
self-check and therefore is not accepted as a verification pass.

Actual later-stage counts are all zero: focused invocations/tests `0/0`, full invocations/tests `0/0`, synthetic runs/processes/input writes/
output writes/replays all `0`. The failed root is frozen non-reusable. No verification success, retained audit, eligibility, release consumption,
or B4 unlock is established.

## 4. Residual risk and exact next branch

The only accepted corrective branch is a fresh V3 package that removes the parent-directory mode assertion and all parent-directory
`lstat`/mode checks. It may verify only the frozen source file's direct path, regular-file/non-symlink identity, bytes, SHA-256, and `0600`
file mode. It must retain the mechanical file-backed non-TTY controller transport, the exact builder/runtime owners, the exact basename map,
and ordered self-check → focused `83` → full `800` → synthetic `1` sequence.

The V2 failed root must not be read, reused, repaired, retried, copied, or deleted. Retained R3 remains
`RETAINED_UNVALIDATED_UNCONSUMED`; canonical validator, retained audit, eligibility, release, B4, network, and all device-adjacent work remain
locked.

**Exact next branch:**
`B3_C3_C4_V3_SOURCE_FILE_IDENTITY_ONLY_FRESH_VERIFICATION_WAITING_ORCHESTRATOR_ACTIVATION`.

维护性判断：问题局限于 controller 自创的目录权限断言；V3 删除该断言即可，artifact、builder、runtime、validator 与 eligibility owner
均无需改变，也不引入新的生产抽象。
