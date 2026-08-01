# P7 retained-R3 Option B：M1-R1-C1 supersession acceptance review

**Planner decision：** `ACCEPTED_COMPLETE_GIT_ER_ONLY_SUPERSESSION`

**Planner date：** `2026-08-01 02:19 MDT`

**Reviewed reference task：** `REF-P7-25-R2-B2-M1-R1-C1`

**Reviewed contract：**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-M1-R1-C1-GIT-ER-ONLY-SUPERSESSION-V1`

**Exact next branch：** `REF-P7-25-R2-B2-M1-R1-S1`

## 1. Frozen review identities

```text
activation = 7373e0cc18b74f06859d53f8a21810b339422792
activation parent = 4720f9ac2588397c484c54a8685988d57e56b83e
activation subject = chore(plan): activate real manifest evidence supersession
activation changed paths =
  .agent-work/FULL_PLAN_REFERENCE.md
  .agent-work/PLAN.md
  .agent-work/PLANS/20260801-0207-p7-retained-r3-b2-m1-r1-canonical-and-evidence-lifecycle-review.md
evidence commit = cb59091d67683ae0b31f3790bf8e110f610791ef
evidence parent = 7373e0cc18b74f06859d53f8a21810b339422792
evidence subject = chore(evidence): supersede real input manifest evidence
evidence changed path = .agent-work/EXECUTION_RESULT.md
reviewed PLAN bytes / SHA-256 =
  12391 /
  e3b0d3e933bb1c2c7022bbc0f2d8d5322984fc3f108a01c30e337e0e4515d0fe
reviewed FULL bytes / SHA-256 =
  390040 /
  bce2b089408aa76d7841f53cf416e887c47c20c5112d6607864699c339cbd45c
reviewed ER blob / bytes / SHA-256 =
  edc2229b4e6e24f63340cb0a4909747f70193c9e /
  1234268 /
  232e1dc4ced7a072adccd8e6e95dd46ca1d2b2ff3a580150db96c5c582fbdbb1
ER immutable prefix blob / bytes / SHA-256 =
  fca8bd45135ec4f22cf18bd66c7d990edb13f024 /
  1231056 /
  21da0337a25def9ef02a8bb718e5415c0daae01feae9fa6eb4674c2e03e563f6
```

本 review 只读取 repository worktree/Git objects。没有读取、stat、list、glob、search、重用或修改任何 external path；没有运行
test、compileall、CodeGraph、controller、validator、release、network 或 device 操作。

## 2. Immutable append 与 schema 验收

Evidence commit 是 activation 的 direct child，且只改变 ER。新 ER 前 `1231056` bytes 与 activation committed blob
byte-for-byte 相同；append suffix exact `3212` bytes。标题
`REF-P7-25-R2-B2-M1-R1-C1 Git/ER-only supersession handoff` 与 schema
`p7_td_b_retained_r3_option_b_b2_m1_r1_c1_supersession_v1` 在 whole ER 各 exact once。

Suffix 是 single Markdown heading、single fenced JSON block、one-line payload plus LF。Strict decode 通过 UTF-8、object root、duplicate-key 与
non-finite gate；payload 与 sort-key/minified canonical re-encode byte-for-byte 相同。原 M1-R1 record 未 rewrite。

首次 `apply_patch` 调用被工具拒绝且没有产生 file write；它是 failed tool invocation，不是 physical ER append。Git prefix/diff 与最终
worktree identity证明实际成功写入只有 sole append one。不得将 rejected/no-write attempt 计入 `execution_result_appends`；payload 中
`current_package_counts.execution_result_appends=1` 分类正确。

## 3. Supersession facts 验收

Payload exact绑定原 M1-R1 activation `2b3b58f...`、evidence `4720f9a...`、原 ER blob/bytes/SHA、原 schema 与
`ProvenanceIOError: json_not_canonical` first failure。它明确 original immutable/not rewritten，并纠正：

```text
physical ER append reported / actual = 0 / 1
fresh probes budget / actual = 2 / 4
fresh probes preacquisition / postappend = 2 / 2
successful file reads / preserved identity rows = 5 / 0
missing detailed identity reconstruction credit = false
```

Canonical failure boundary明确 C1 four canonical reads先完成，首件 retained
`current-lineage-candidate.json` 的 exact path/bytes/SHA/mode gate完成，然后 canonical re-encode失败。Payload没有补造缺失的五个
device/inode/mode/data/hash rows。

Retained acceptance owner已改为 immutable opaque exact physical identity plus strict JSON：UTF-8 object、duplicate-key rejected、non-finite
rejected。Canonical re-encode、schema/scientific validation、eligibility 与 release consumability全部false。C1 four与new output five继续要求
canonical bytes；canonical validator仍是sole eligibility owner。

旧 fresh namespace disposition为 immutable no-read/no-stat/no-list/no-glob/no-search/no-reuse/no-modify/no-delete。Successor要求明确：new
namespace、retained strict-only、每次successful read立即保留identity、failure保留partial ledger、final payload append前即记录append1、sole
append后external operation0，并同时保留probe budget与actual。

## 4. Scope、locks 与 decision

本 C1 的 builder/runtime/controller/tests/CodeGraph/validator/eligibility/retained audit/release/device均为0；external operations exact0；
retry/fallback exact0。Manifest seal、identity bundle、retained audit、eligibility、release credit全部false。

因此接受：

```text
REF-P7-25-R2-B2-M1-R1-C1 =
  ACCEPTED_COMPLETE_GIT_ER_ONLY_SUPERSESSION
m1_real_input_supersession_status = ACCEPTED_COMPLETE
retained R3 = RETAINED_UNVALIDATED_UNCONSUMED
```

该接受只关闭 evidence correction，不恢复旧M1-R1的manifest或identity credit，不使旧fresh namespace可用，也不解锁validator、eligibility、
release、network/device或later stage。

## 5. Exact successor

Planner解锁唯一 new-namespace `REF-P7-25-R2-B2-M1-R1-S1` real-input manifest-only successor。它复用accepted P3/M1/P5 owners，读取冻结
C1 four与retained three。Retained three只做exact physical identity + strict JSON，不做canonical re-encode；C1 four与new output five仍做
canonical decode。

执行owner必须在每次successful file read后立即把完整 `FileIdentity` append到append-safe in-memory ledger；任一后续failure仍保留ordered
partial ledger。Fresh namespace只允许preflight exact2 absence probes。Final ER payload在sole append前即冻结
`execution_result_appends=1`，append之后external/Git/worktree probe全部0；Planner后续通过Orchestrator evidence commit审查prefix与diff。

Success仍只能是 `FRESH_M1_REAL_INPUT_MANIFEST_SEALED_NOT_RETAINED_ELIGIBLE`。Canonical validator/eligibility、retained audit、release、network、
device、FORMAL与later routes继续锁定。

维护性判断：接受的supersession将错误计数和输入接受域收敛在one immutable record；successor继续复用P3/M1/P5 single owners，不新增
serializer、validator、filesystem helper或parallel evidence framework，无需架构重构。
