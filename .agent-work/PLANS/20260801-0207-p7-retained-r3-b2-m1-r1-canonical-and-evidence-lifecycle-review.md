# P7 retained-R3 Option B：M1-R1 canonical 与 evidence lifecycle review

**Planner decision：**
`REJECTED_REAL_INPUT_CANONICAL_ACCEPTANCE_AND_EVIDENCE_LIFECYCLE`

**Planner date：** `2026-08-01 02:07 MDT`

**Reviewed reference task：** `REF-P7-25-R2-B2-M1-R1`

**Reviewed contract：**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-M1-R1-FRESH-REAL-INPUT-MANIFEST-ONLY-V1`

**Exact next branch：** `REF-P7-25-R2-B2-M1-R1-C1`

## 1. Frozen review inputs

```text
activation = 2b3b58f02656609525c511853547dc51d63559c8
activation parent = 0a7f718a8d49eb33974ce5f22f85dd8a00ea1110
activation subject = chore(plan): activate fresh real input manifest seal
evidence commit = 4720f9ac2588397c484c54a8685988d57e56b83e
evidence commit parent = 2b3b58f02656609525c511853547dc51d63559c8
evidence changed path = .agent-work/EXECUTION_RESULT.md
reviewed PLAN bytes / SHA-256 =
  18346 /
  b4f54398ab0e7eabe6f7aa6a8249577a13bfa3a781421fbdae9ec77a87c425bd
reviewed EXECUTION_RESULT bytes / SHA-256 =
  1231056 /
  21da0337a25def9ef02a8bb718e5415c0daae01feae9fa6eb4674c2e03e563f6
reviewed EXECUTION_RESULT blob =
  fca8bd45135ec4f22cf18bd66c7d990edb13f024
reviewed FULL_PLAN_REFERENCE bytes / SHA-256 =
  388473 /
  e11dd674375f6e223dcdc490fe0b0dfb551ff0eafafd77a76c8df16638ed7a51
```

本 review 只读取 repository、Git object 与 committed ER。没有读取、stat、list、glob、search、重用或修改任何
real/fresh/old external root；没有运行 test、compileall、CodeGraph、controller、validator、release、network 或 device 操作。

## 2. Accepted terminal facts

M1-R1 在任何 builder/runtime/controller/output create 之前 hard-fail：

```text
fresh absence checks reported before acquisition = 2
existing root acquisitions = 2
successful exact file reads before failure = 5
builder/runtime/controller = 0/0/0
output artifacts = 0
retry/fallback = 0/0
first failure = ProvenanceIOError: json_not_canonical
retained R3 = RETAINED_UNVALIDATED_UNCONSUMED
```

前四次 file read 是 accepted C1 four；第五次是首个 retained artifact
`current-lineage-candidate.json`。其 path/bytes/SHA/mode 与冻结 contract 匹配后，才在 exact canonical re-encode gate
失败。该结论只证明 retained 首件不是 P3 canonical byte serialization，不证明 JSON 无效、schema 无效、科学无效或 eligibility。

## 3. Finding 1：retained input acceptance owner 错位

历史 production qualification 生成并保留 exact retained three：

```text
current-lineage-candidate.json =
  9819 bytes /
  3a2ff5a2af200c55c925b954488c5c5dd31a35a481440d17dfcdd8b68419f2e0
resolved-formal-plan.json =
  15137 bytes /
  cf7c78b6a6cfda4055d05f5e9bbe9914161213b380dc7736ee09e257dd45eb6b
setup-lineage-release.json =
  1567 bytes /
  0bacf1878a97fcdc4436259e132e89f6e56611df6d7fb5d5a7da28f62c98ad3e
```

Repository owner evidence proves those historical bytes were intentionally accepted as strict JSON, not canonical bytes：

1. `p7_retained_release_audit._strict_json_load()` performs strict UTF-8 JSON decode with duplicate-key and non-finite rejection but does
   not require byte-for-byte canonical re-encoding；
2. the historical O2-C1 real audit applied `_strict_json_load` to all three `SOURCE_NAMES` before `_audit_schema`；
3. O2-C1 reached `_audit_schema` and failed only with `artifact schema or status differs`。因此 all three strict decodes had succeeded；
4. P3 `decode_canonical_json()` is the exact-reencode owner for newly canonicalized evidence, but it is stricter than the historical retained
   source contract and must not be retroactively imposed on immutable inputs。

Planner conclusion：M1 manifest-only route must preserve each retained artifact as exact physical identity plus opaque original bytes and prove
strict JSON validity only. It must not canonicalize, rewrite, repair, copy, regenerate or normalize retained bytes. C1 four and every newly
generated subordinate artifact remain byte-for-byte canonical JSON. The canonical validator remains the sole eligibility owner；M1 may not infer
schema science, audit status, eligibility or release consumability。

No Advisor decision is needed：this is an engineering provenance/serialization ownership correction, not a color- or measurement-science branch。

## 4. Finding 2：failure ER lost acquired identities and miscounted append

Committed ER payload reports：

```text
pre_file_reads = 5
input_preacquisition.identities = []
counts.er_appends = 0
physical committed ER append = 1
```

The five successful physical reads must have been retained in an append-safe in-memory ledger immediately after each successful owner return.
Failure on item six or any later stage must serialize all already-acquired `FileIdentity` rows in exact acquisition order. Clearing the list because
the seven-item acquisition was incomplete is invalid evidence lifecycle behavior。

`er_appends=0` describes the counter before its own append and therefore contradicts the immutable Git fact that evidence commit `4720f9a...`
added one ER block. Future handoff must construct the final record with `er_appends=1` before the exact one append, then verify the committed/dirty
EOF occurrence without re-probing external paths。

The missing five detailed identities cannot be reconstructed from repository evidence and must not be invented. This run receives no reusable
input-identity or retained-content credit beyond the frozen path/bytes/SHA facts already in PLAN plus the truthful count `5`。

## 5. Finding 3：post-append probes exceeded budget

The active PLAN budget allowed exact two fresh non-following absence checks before external input reads/writes. Executor handoff reported those two,
but orchestration performed two additional fresh presence checks after appending ER. Actual fresh presence/absence probes are therefore `4`, not `2`。

This is a budget violation even though no fresh source/output was created. A terminal handoff must not touch fresh paths after the sole ER append；
the append is the final side effect. Future execution must maintain one append-safe counter ledger and freeze actual counts before the append。

## 6. Decision and credit

```text
REF-P7-25-R2-B2-M1-R1 =
  REJECTED_REAL_INPUT_CANONICAL_ACCEPTANCE_AND_EVIDENCE_LIFECYCLE
manifest seal credit = 0
input identity bundle credit = 0
retained semantic/audit/eligibility credit = 0
fresh namespace disposition =
  IMMUTABLE_NO_READ_NO_STAT_NO_LIST_NO_GLOB_NO_SEARCH_NO_REUSE_NO_MODIFY_NO_DELETE
retained R3 = RETAINED_UNVALIDATED_UNCONSUMED
```

The hard-fail itself remains valid and fail-closed. Its ER is not rewritten；it is superseded only by a new append that states the three corrected
facts and preserves the original block/hash unchanged。

## 7. Exact next branch

`REF-P7-25-R2-B2-M1-R1-C1` is one Git/ER-only supersession package：

1. read only exact committed Git identities, the reviewed active PLAN/archive and the committed ER prefix；
2. append one strict canonical correction record to ER, without editing or replacing the old M1-R1 block；
3. record actual append `1`, total fresh probes `4` vs budget `2`, acquired/preserved identities `5/0`, canonical failure boundary and corrected retained
   acceptance owner；
4. lock every external root and all production/test/controller/validator/release/device routes；
5. stop for Planner review。

Only after C1 acceptance may Planner issue one new-namespace real-input successor. That later plan must use strict JSON decode for retained three,
canonical decode for C1 four/output five, append each successful identity immediately to a durable in-memory ledger, perform no external probe after
the sole ER append, and preserve exact actual-vs-budget counters on all failure paths。

## 8. Locks and maintainability

The corrective package does not read external evidence, modify production/tests, run tests or invoke CodeGraph. Canonical validator/eligibility,
release generation/qualification/copy/consumption, network/DNS/environment/credentials, device/camera/Ray/strip/cleanup/capture/FORMAL/public
analyzer/TD-C/sentinel/P8/firmware/deployment remain exact zero。

维护性判断：问题属于 manifest-only orchestration 的输入接受与 terminal evidence lifecycle，而不是 P3 serializer 或历史 retained payload
本身。先用一条 immutable supersession 收敛事实，再在后续 fresh successor 修正 orchestration，可避免修改旧证据、扩宽 serializer 或引入
平行 validator；无需架构重构。
