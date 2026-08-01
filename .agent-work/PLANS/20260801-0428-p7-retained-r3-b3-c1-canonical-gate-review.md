# P7 retained-R3 Option B：B3-C1 canonical machine-row gate 拒绝审查归档

**归档时间：** `2026-08-01 04:28 America/Edmonton`

**Reference task：** `REF-P7-25-R2-B3-C1`

**Reviewed contract：**
`P7-TD-B-RETAINED-R3-OPTION-B-B3-C1-EXACT-TERMINAL-SCHEMA-SELF-CHECK-TEST-SYNTHETIC-V1`

**Reviewed activation：** `8555f5790b66f2eac7b777cec3d70b4bd2908f8b`

**Evidence commit：** `07d83391c918b20467e310ec72ec3554adda8271`

**Planner decision：**
`REJECTED_EXECUTION_ASSERTION_CANONICAL_MACHINE_ROW_REENCODE_NOT_CONTRACTUAL`

## 1. 审核范围与方法

Planner只读核对active `PLAN.md`、committed `FULL_PLAN_REFERENCE.md`、activation/evidence Git metadata和evidence commit新增的physical-EOF payload。没有读取真实manifest、C1、retained、失败B3 external root或任何其他外置evidence namespace；没有调用test、controller、validator、audit、release、network或device入口。

Reviewed PLAN：bytes `18289`，SHA-256
`0d9653a7944fad6df4ac487a16f09559fd73e477d899a96f261e72cbacda1c62`。

Activation `8555f5790b66f2eac7b777cec3d70b4bd2908f8b`：

- parent `8ae390444255d9bfe6082e64b31c25cdd5bdd399`；
- subject `chore(plan): activate exact terminal schema verification`；
- exact changed paths为`.agent-work/FULL_PLAN_REFERENCE.md`、`.agent-work/PLAN.md`和`.agent-work/PLANS/20260801-0416-p7-retained-r3-b3-terminal-self-check-review.md`。

Evidence lineage：

- activation commit的`EXECUTION_RESULT.md` prefix：bytes `1290261`，SHA-256 `24afc1b3876bf6988d8de139b81e2b8f094f8939b788d7ac75c9e4a54fb6cc8e`；
- physical EOF suffix：bytes `2830`，SHA-256 `5abd96713ea773704253279e74c4bc7a5991a7f875044e68f13286395a12bfd9`；
- evidence commit后的`EXECUTION_RESULT.md`：bytes `1293091`，SHA-256 `f0bf45501ae31d700eb3d0095d01d881b2a35ae1c17717936b36ec0a95240413`。

## 2. 执行结果与质量

Executer在唯一outer controller内完成activation Git identity、PLAN/FULL各一次repository decode，并从PLAN提取一条machine row。随后其`strict()` helper在完成duplicate-free/non-finite-safe object parse后，又把parsed object做canonical JSON reencode并要求原始machine-row bytes与重编码bytes完全相等，因此在`activation machine row`以`not strict canonical JSON`停止。

实际计数：repository decodes `2`、PLAN machine-row extraction `1`、Git reads `2`、outer controller `1`、ER append `1`；真实manifest/C1/retained reads、self-check、focused、full、synthetic均为`0`。Canonical validator、retained audit、eligibility、release、network/device和implementation writes均为`0`。EOF append是最后side effect，postappend operations `0`。

失败是早期fail-closed且没有污染真实输入，但尚未验证任何B3-C1 substantive acceptance criterion，不能报为通过。

## 3. Findings 与裁定

Active PLAN第1节明确要求的是：strict UTF-8、exact backtick-wrapped delimiter、duplicate-free/non-finite-safe JSON object parse；同一段明确禁止`canonical key-order gate`。JSON object的key顺序和空白编码不是该治理machine row的eligibility或activation语义。

Executer增加的`json.dumps(..., sort_keys=True, separators=(",", ":"), allow_nan=False)` byte-equality条件没有PLAN依据，并且与明确禁令冲突。失败不说明PLAN/FULL machine row无效，也不说明B2 manifest、C1或retained输入需要修复。

因此决定为：

`REJECTED_EXECUTION_ASSERTION_CANONICAL_MACHINE_ROW_REENCODE_NOT_CONTRACTUAL`。

B2仍为`ACCEPTED_COMPLETE_SEALED_SUBORDINATE_PROVENANCE_NOT_RETAINED_ELIGIBLE`；retained R3仍为`RETAINED_UNVALIDATED_UNCONSUMED`。

## 4. Residual risks 与 exact next branch

后继必须是fresh B3-C1 successor：

1. 复用exact delimiter与strict UTF-8/object/duplicate/nonfinite parser；
2. 明确禁止对PLAN/FULL machine-row原始bytes进行canonical reencode、sort-keys、whitespace normalization或byte-equality比较；
3. 解析后只按typed fields和required FULL subset比较语义；
4. 保留真实terminal/seal/admission exact schema与identity self-check；
5. self-check通过后仍只能按focused exact once → full exact once → brand-new synthetic exact once执行，任何失败后续为零；
6. 真实canonical validator、retained audit、eligibility、release和设备工作继续锁定。

Exact next reference task：`REF-P7-25-R2-B3-C1-C1`。

Exact next contract：
`P7-TD-B-RETAINED-R3-OPTION-B-B3-C1-C1-STRICT-MACHINE-ROW-SELF-CHECK-TEST-SYNTHETIC-V1`。

维护性判断：无需修改production、manifest owner或artifact schema；下一包只收窄一次性controller的repository machine-row parser，继续复用P3/M1/P5所有权边界。
