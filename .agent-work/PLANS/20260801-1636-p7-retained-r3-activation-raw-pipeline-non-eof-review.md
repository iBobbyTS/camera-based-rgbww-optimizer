# P7 retained-R3 Option B：activation raw-pipeline / non-EOF evidence review

**Planner 日期：** `2026-08-01`

**Reviewed reference task：** `REF-P7-25-R2-B3-C3-C4-R5-R1-C1-R2-R1-C2-S1-C1-R1-D1-D2-C1-R2-C1-S1-C1-C1-C1-C1`

**Reviewed contract：** `P7-TD-B-RETAINED-R3-OPTION-B-B3-C3-C4-R5-R1-C1-R2-R1-C2-S1-C1-R1-D1-D2-C1-R2-C1-S1-C1-C1-C1-C1-ACTIVATION-OBJECT-ONLY-CORRECTIVE-SUPERSESSION-V1`

**Activation：** `4c6289b0ed64138b3e4f1c00c3496a268daacd23`

**Evidence child：** `e56b09af4b6d375ecce5f1f26531cbb5dd68dd0c`

**Decision：** `REJECTED_RAW_GIT_OBJECT_BYTES_NOT_PASSED_TO_ACCEPTED_PARSERS_AND_HANDOFF_NOT_AT_PHYSICAL_EOF`

## 1. Reviewed scope and immutable identities

- Activation direct parent：`5f663c2c2243cc1d34e7b66fc6799bd9ad3092cc`；subject exact `chore(plan): forbid worktree plan reads`。
- Activation committed PLAN：`15432` bytes / SHA-256 `de49bb1cabe9ad65a194c419ae4c429448a1ba8e0679a6685dfd3db211f073c0`。
- Activation committed FULL：`465095` bytes / SHA-256 `269428052b17ba111f3e92d6f79bbdd1bdbbddc5fd4df21acdb6f2ead1d4ce41`。
- Activation committed ER：`1550853` bytes / SHA-256 `438c95e27261fc5be49b05e500c185879e558e7fecbae86be7546fd6613ee5d3`。
- Evidence child ER：`1555130` bytes / SHA-256 `27a5f4adea3bc7d73f5e743cd2b4b701ae564bee818da48c3af888b9cd78e352`。
- `git diff 4c6289b0..e56b09af`证明evidence child只修改`.agent-work/EXECUTION_RESULT.md`，新增14行；PLAN、FULL、archive、代码、测试、skill、docs与GUIDE均未改。
- Read-only fixed report仍冻结为`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b3-owner-expectation-attribution-d2-c1-r2-c1-9ddd486d1923/01-owner-expectation-attribution.json`，`41685` bytes / SHA-256 `923f32afae0f375469d03a6b6a18a71261c19e7bcfefcd0bb041bdfde11b849a`；seal为`166` bytes / SHA-256 `068ee79657f4765928b80909514d37b431d779fc2a6ccd914c127e1453c08c49`。

## 2. Candidate method and observed effects

Candidate正确从exact activation Git objects取得PLAN/FULL raw committed bytes各一次，且没有读取worktree PLAN/FULL。可是两次Git stdout直接越过local process进入tool boundary，combined output发生截断；raw bytes没有保留在取得它们的process内，也没有直接传入accepted parsers。由于read/retry/fallback预算均已耗尽或为零，candidate fail closed：accepted PLAN/FULL parser calls `0/0`，required FULL subset未获得信用。

Candidate没有读取report/seal，没有strict load，没有冻结`$.matrix`，也没有核对`$.ledger_binding_proof.frozen_path == "$.ledger_rows"`。Controller、selector、18-row Git ledger、Git file acquisition、real self-check、canonical validator、tests、compileall、CodeGraph、network与全部device effects均为`0`；production owner、lineage、eligibility与release均为`false`，retained R3保持`RETAINED_UNVALIDATED_UNCONSUMED`。

## 3. Independent physical-EOF finding

Candidate声称其唯一failure block是final EOF append，但Git blob证明该说法不成立：

- failure heading起始byte offset为`1546782`；从该heading到blob physical EOF仍有`8348` bytes；
- candidate block后仍存在旧heading `D2-C1-R2-C1-S1-C1-C1 identity-owner corrective continuation fail-closed handoff`；该旧heading起始offset为`1551059`；
- 从该旧heading到physical EOF仍有`4071` bytes；因此新增14行是插在旧suffix之前，不是physical EOF append；
- current ER不是activation-parent ER的prefix extension。旧插入必须保留为immutable historical evidence，但不得获得durable final-handoff信用。

因此candidate同时违反两项关键边界：raw acquisition与accepted parse不在同一local process；final record不在physical EOF。其记录的candidate zero-effect事实可以作为被后继terminal supersession引用的历史事实，但synthetic engineering attribution facts仍不得接受。

## 4. Validation quality and decision

本次评审使用activation/evidence Git objects、exact commit topology、exact changed-path diff、blob byte/SHA identities、failure block byte offsets和physical EOF remainder完成独立复核。`git diff --check 4c6289b0..e56b09af`通过。未重跑controller、selector、Git ledger、tests、validator或任何设备操作，也未读取或修改外部artifact。

结论为拒绝：`REJECTED_RAW_GIT_OBJECT_BYTES_NOT_PASSED_TO_ACCEPTED_PARSERS_AND_HANDOFF_NOT_AT_PHYSICAL_EOF`。Original execution contract继续rejected；candidate failure block只能保留为non-terminal historical insertion。

## 5. Residual risks and exact next branch

下一个包可以安全地同时完成fixed `$.matrix` final supersession，但必须采用一个原子顺序：

1. 在同一个local process内以captured stdout bytes分别取得新activation PLAN/FULL，各立即交给accepted parser一次；禁止通过tool output再恢复、重建或二次读取。
2. 在同一process内验证evidence-parent ER exact blob、candidate non-EOF block及其后`8348` bytes preserved suffix，并冻结真正physical EOF。
3. 同一process才可各读取固定report/seal一次、strict-load一次，从`report_value["matrix"]`冻结18 rows一次，并独立核对`report_value["ledger_binding_proof"]["frozen_path"] == "$.ledger_rows"`。
4. 所有gate通过后，只在当前physical EOF append一次success terminal supersession；任一gate失败则只在当前physical EOF append一次fail-closed terminal supersession。两种分支都必须明确保留并supersede旧non-EOF insertion；append后立即停止。

Exact next branch：`REF-P7-25-R2-B3-C3-C4-R5-R1-C1-R2-R1-C2-S1-C1-R1-D1-D2-C1-R2-C1-S1-C1-C1-C1-C1-C1`，`ACTIVATION_RAW_PIPELINE_PHYSICAL_EOF_FIXED_MATRIX_CORRECTIVE_SUPERSESSION`。不得将pure EOF correction与fixed-matrix work拆成会留下第二个中间非terminal record的两次append。
