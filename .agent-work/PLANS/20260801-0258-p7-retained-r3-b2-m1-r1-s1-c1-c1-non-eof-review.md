# REF-P7-25-R2-B2-M1-R1-S1-C1-C1 non-EOF evidence review

**Reviewed reference task:** `REF-P7-25-R2-B2-M1-R1-S1-C1-C1`

**Reviewed contract:**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-M1-R1-S1-C1-C1-GIT-ER-ONLY-SELECTOR-FREE-SUPERSESSION-V1`

**Planner decision:** `REJECTED_NON_EOF_INSERTION_CONTRACT_VIOLATION`

**Planner review date:** `2026-08-01 02:58 MDT`

## 1. Frozen repository evidence

- Activation is `376ab503622a695926f6b091a3e0a899dc5e1590`, direct parent
  `7dceb396ebafe1ee38ca14411851fc7bc27a34c6`, exact subject
  `chore(plan): activate selector-free retained supersession`, with exact changed paths FULL, PLAN, and
  `.agent-work/PLANS/20260801-0244-p7-retained-r3-b2-m1-r1-s1-c1-selector-stop-review.md`.
- Evidence commit is `7b747a0ad9d019ceb59af0089d8efa85f93ff51e`, direct parent the activation, exact subject
  `chore(evidence): record selector-free supersession attempt`, and changes only
  `.agent-work/EXECUTION_RESULT.md`.
- Activation ER identity is blob `4ebbaef274da8ed2f90ae071f55e92cc2e178000`, bytes `1243874`, SHA-256
  `64274bd4a8c1f493914d18320488d9d1ff87b070d0ececa22465ca13688ca5dd`.
- Evidence ER identity is blob `cc5e8a24fb30dc235a245118af5ea7d8e39e3306`, bytes `1248695`, SHA-256
  `75808b704952f1d4be3ad8ff273577c3962769ae47399694ee09d474fd7001d2`.
- Review began with a clean worktree. Planner used only repository Git objects and the worktree PLAN. It did not access
  any external path, retained evidence, test, CodeGraph, controller, validator, release, network, or device surface.

## 2. Independent physical-diff audit

Byte comparison of the two committed ER blobs establishes:

```text
common prefix bytes = 2579
inserted bytes = 4821
inserted SHA-256 = b3f18c72e09cdb647a0e597fd639c3d8d216bab5678d4f0bb34f6517f97be6a2
preserved old suffix bytes = 1241295
old suffix preserved byte-for-byte = true
physical append at old EOF = false
```

The inserted bytes begin with the exact S1-C1-C1 handoff heading. At old offset `2579`, the previous content had just
closed an early fenced block and immediately continued with `## 3. Artifact hashes`; the new payload was inserted
between those two existing regions. Every old byte from offset `2579` through old EOF survives unchanged after the
insertion. This is preservation of old content, but it is not the contract's required physical EOF append.

The evidence commit's five-line diff at repository line 37 corroborates the byte audit. Its position is near the
beginning of the 1.24 MB ledger, while the evidence ER still physically ends with the earlier
`REF-P7-25-R2-B2-M1-R1-S1 Executer handoff` block. `git diff --check` passes, but whitespace validity cannot establish
append location.

## 3. Claim disposition

The embedded payload is retained immutably as a rejected attempt. Its `result=PASS`, `execution_result_appends=1`, and
`append_is_last_side_effect`-equivalent success semantics do not override the committed byte topology. In particular,
the payload may still contain useful exact Git identities and selector counts, but it cannot close this contract or
be consumed as successful supersession evidence.

Accepted facts:

- the selector-free Git gates reported `23/24` maximum reads and no external/test/device work;
- the original S1 failure remains a non-contractual execution-selector mismatch;
- the bad block is immutable and its exact location/length/hash are now independently known;
- no production, test, runner, retained-input, validator, release, or scientific defect is established.

Rejected claims:

- S1-C1-C1 did not perform a physical EOF append;
- its embedded `PASS` is not authoritative completion evidence;
- no eligibility, release, retained audit, device, or later-stage credit is unlocked.

Decision:

```text
REF-P7-25-R2-B2-M1-R1-S1-C1-C1 =
  REJECTED_NON_EOF_INSERTION_CONTRACT_VIOLATION
retained R3 = RETAINED_UNVALIDATED_UNCONSUMED
```

## 4. Exact corrective branch

- Next reference task: `REF-P7-25-R2-B2-M1-R1-S1-C1-C1-C1`.
- Contract:
  `P7-TD-B-RETAINED-R3-OPTION-B-B2-M1-R1-S1-C1-C1-C1-GIT-ER-ONLY-PHYSICAL-EOF-SUPERSESSION-V1`.
- The only write is one new canonical supersession record at the current ER's physical EOF. The existing misplaced
  block is not edited, moved, deleted, regenerated, or credited.
- Before editing, the Executer must establish the committed ER identity and an exact unique final-block anchor from
  Git/worktree bytes. The `apply_patch` hunk must use the complete unique final S1 block, including its heading,
  one-line JSON, and closing fence, as context through physical EOF. A short generic fence or repeated heading is
  prohibited because it can match an earlier block.
- The terminal payload must explicitly mark the embedded block
  `REJECTED_NON_EOF_SELF_REPORTED_PASS`, record the two ER identities and `2579/4821/1241295` topology, preserve all old
  records, and grant no scientific or execution credit.
- The append is the Executer's last side effect. Independent prefix/suffix verification occurs only after the
  Orchestrator commits the evidence and returns it to Planner review.
- Planner stop:
  `B2_M1_R1_S1_C1_C1_C1_PHYSICAL_EOF_SUPERSESSION_WAITING_PLANNER_REVIEW`.

## 5. Locks and maintainability

External paths and retained files remain no-read/no-stat/no-list/no-glob/no-search/no-reuse/no-modify/no-delete. Tests,
compileall, CodeGraph, production/test writes, controller, validator, eligibility, retained audit, release, network,
DNS, environment, credentials, devices, camera, Ray, strip, cleanup, capture, FORMAL, analyzer, TD-C, sentinel, P8,
firmware, and deployment remain zero. Retry and fallback remain zero.

维护性判断：纠偏仅追加一个不可变 supersession row，并把物理 EOF 证明留给后续独立 Git blob 审核；不引入 helper、scanner、parser、
harness 或平行 evidence owner，无需架构重构。
