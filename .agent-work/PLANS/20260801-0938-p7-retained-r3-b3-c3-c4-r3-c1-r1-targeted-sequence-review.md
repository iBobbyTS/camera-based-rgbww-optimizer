# P7 retained-R3 Option B：R3-C1-R1 targeted sequence-boundary review

**Planner review date：** `2026-08-01`

**Reviewed reference task：** `REF-P7-25-R2-B3-C3-C4-R3-C1-R1`

**Decision：** `REJECTED_TARGETED_P3_FROZEN_SEQUENCE_REPRESENTATION_MISMATCH`

**Exact next branch：** `REF-P7-25-R2-B3-C3-C4-R3-C1-R1-C1`；保留当前exact-two untracked modified candidate，只修P3 decode后tuple/list JSON sequence语义、decoded report re-encode及剩余targeted assertions，然后fresh验证。

## 1. Topology、EOF与candidate identity

- Activation `fb97fe449bec04eda78c85e91a9185fde6139a98`是parent `3bc46c5a866d5f3f8d303224fcb582a4de630e8d`的direct child，tree `aeab8bf5a1b6c7fd08818ca86a2f3193fbd82228`，subject exact `chore(plan): resume real self-check correction`，changed paths exact FULL/PLAN/`20260801-0926` archive。
- Evidence `27424dd1feedb620d8b527c7aea4e8d27010dbed`是activation direct child，tree `b3ad633cb16ad40b770e72f310e57113a8d5e02e`，subject exact `chore(evidence): record fresh real self-check correction`，changed path only ER。
- Evidence ER以activation ER blob `85892b64b4b5a85a15715ccf4c672017ac3746a6`的1396492 bytes/SHA `55cf0d3daf6f2489d4f89685c12bb8542b36007d9d4f48e1cebe94a0629850c7`为byte-exact prefix；physical EOF append为6 lines、3468 bytes、SHA `7c5dcbbc5ecb699ee0e937a131be046797fb46c56b703d820bf6c3f90ddd2c48`。After blob/bytes/SHA为`d38db436786342558f565f6f2056056d1e4d09b3` / `1399960` / `cd3974db2939e8638eb663d4e4f56ddddb877ade0c7b0e80f3fa225dc696eba5`。
- 当前untracked source为24679 bytes/SHA `ddb20f987ab728489f9898ffd2ebcb23cf2100bb332c56d93653529453f7796c`；test为21583 bytes/SHA `5caef9716070f3a78a1ee1c73754dc3f0eb6a0c9259c3da4399a7ff3c2d11859`；无其他porcelain。

## 2. Execution result review

Executer满足activation/no-prequery/two-patch gate。Targeted12一次后hard stop：8 failures、3 errors、0 skipped，primary exact `MANIFEST_CONTRACT_MISMATCH_ON_GOLDEN_FIXTURE` / observed code `manifest_contract_mismatch`。Focused53、full822、compileall、CodeGraph sync/post、diff/status、commit、posttarget均0；retry/fallback0。

Real/C1/retained artifacts、external roots、validator/eligibility/release、network/device均0。Handoff为唯一physical EOF strict JSON。因此拒绝production/test completion但无需治理supersession，也不升级Advisor。

## 3. Independent candidate review

原八findings的代码方向已写入candidate但尚未通过验证，不能接受为closed。当前最小确定性缺口为：

1. P3 `decode_canonical_json`把JSON arrays冻结为tuple；subject `_json_native(expected_manifest)`产生lists，而`_exact`仍要求list/tuple concrete type相同，故合法manifest必然mismatch。
2. 同一representation mismatch也会发生在decoded report tuple与JSON-native payload list之间。
3. 即使comparison通过，`canonical_json_bytes(decoded_report)`仍直接接收mappingproxy/tuple并触发P3 `json_unsupported_value`；re-encode前必须显式转回JSON-native。
4. Test 09第一负例把`git_file_bytes`改成list，前置错误应是`git_file_bytes_invalid`而非预期seam mismatch；须保持tuple。
5. Test 09后两负例修改baseline却保留旧manifest，正确primary会是manifest mismatch，未真正覆盖seam/collision。应直接调用`required_real_manifest_git_argv`或重建一致manifest后再断言对应stable code。

JSON array没有list/tuple wire-level区别；最小production correction是在strict JSON comparator中仅对双方sequence容器允许tuple/list语义等价，仍保持mapping exact keys、position/order及scalar concrete type exact。不得放宽typed spec输入类型或P3 encoder。

## 4. Credit与next locks

R1不获得targeted、production、八finding closure或B3 credit；但exact-two patch结果保留为C1输入。C1只修上述representation/assertion缺口，不重做架构或扩大六API。

Real artifacts、validator、eligibility、release、synthetic、network/device继续锁0。

维护性判断：缺口集中于单一JSON boundary comparator、一次report re-native及测试前置条件；可在same exact-two路径局部关闭，无需新owner或Advisor介入。
