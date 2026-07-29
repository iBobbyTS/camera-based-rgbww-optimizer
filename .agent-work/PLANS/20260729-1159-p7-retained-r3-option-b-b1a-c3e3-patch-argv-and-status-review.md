# REF-P7-25-R2-B1A-C3E3 / Canonical patch argv and aggregate-status review

**Planner 日期：** 2026-07-29

**Reviewed contract：**
`P7-TD-B-RETAINED-R3-OPTION-B-B1A-C3E3-ROW-PARSE-POLICY-V1`

**Decision：**
`REJECTED_CORRECT_HARD_FAILURE_CANONICAL_PATCH_ARGV_AND_PREMATURE_PASS_STATUS`

## 1. Frozen evidence

```text
root = /Volumes/4T/temp/rgbww-optimizer/
  p7-td-b-retained-r3-option-b-b1a-c3e3-offline/20260729T175727Z
validation-summary.json SHA-256 =
  b5f90b2181d617352fd4a02848caee1ea6bd608bb2f90b47b98765a190a358ab
terminal-summary.json SHA-256 =
  d481d0d4ceb97351d0bb3f3bafe19e3d5d871d886babe97a1973490c25d4e275
clone-verification.json SHA-256 =
  7fe77ca9ee43588ca223fe1ba97b016d4433ec82f99f4badda68b6fd84bacc64
EXECUTION_RESULT.md §57 SHA-256 =
  fdb1a075cd5af48d3c9d03895bcc5e3a81036a09200d6af276d3832fd3523e9c
reviewed PLAN SHA-256 =
  7b3cf91d9d3d2db6eaf98967be6157bc056d9cf1ac0a6a44d6fba33e3ae81037
HEAD = 9303aa22a9bd37e8ec4f23147c78c6bea84b9a2e
staged paths = 0
```

Runtime probe、machine-row policy、FULL 12-key subset、五项source evidence-before-compare、五项materialization和candidate edit0均
通过。Focused/full tests、commit、manifest、R3 reads均为0；network/device/formal等锁定面调用均为0。

## 2. Independent diagnosis

Planner在同一immutable cleanroom、同一parsed parent与同一sorted five paths上独立重算：

```text
git diff --binary <parent> -- <sorted paths>
  bytes = 50249
  SHA-256 = ec91d7bf5115945a11da800b9f067d799f6d523577bd7883e60573308d5ab2e7

git diff --binary --full-index <parent> -- <sorted paths>
  bytes = 50579
  SHA-256 = 775b07fecfd65ba278ee174d4ae64772e8b2cfc83d794b6c89c259f4b8eadee0
```

Candidate object冻结的canonical patch SHA只对应第二条命令。C3E3 controller少传`--full-index`，所以clone aggregate mismatch与
terminal hard-fail正确；这不是candidate/source mutation或科学失败。

`clone-verification.json`同时把`status`预写为`passed`，但同一对象内的patch digest与candidate expected不匹配。Checks可以逐项
记录observed truth，但terminal status只能在所有aggregate comparisons完成后计算和赋值；禁止pre-pass或先写pass再依异常覆盖。

## 3. Fresh successor

Successor必须由PLAN machine冻结唯一canonical patch argv template：

```text
git diff --binary --full-index <parsed parent> -- <parsed sorted paths>
```

Parent、paths与expected patch SHA仍只能来自唯一candidate object；argv template不得复制candidate facts。Clone verification先记录
observed checks，再完成全部expected comparisons，最后一次性赋terminal status。Aggregate任一mismatch只能是failed，绝不可出现
内部mismatch而status passed。C3E3其余row policy、FULL merge、runtime、fresh root、source evidence、unittest、single commit/
manifest、R3 three hashes、retry0与全锁合同保持不变。无Advisor或Human gate。

建议FULL把C3E3记录为上述正确hard-fail并程序化激活fresh successor；candidate SHA、checkpoint、release和R3状态不变。
