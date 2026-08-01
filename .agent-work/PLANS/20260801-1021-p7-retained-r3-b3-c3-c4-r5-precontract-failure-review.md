# P7 retained-R3 Option B：R5 pre-contract failure 验收归档

**Planner 日期：** `2026-08-01`

**Reference task：** `REF-P7-25-R2-B3-C3-C4-R5`

**被验收 contract：** `P7-TD-B-RETAINED-R3-OPTION-B-B3-C3-C4-R5-REAL-MANIFEST-SELF-CHECK-V1`

**Planner 决定：** `REJECTED_PRECONTRACT_JSON_BOUNDARY_AND_FAILURE_LIFECYCLE_GAP`

## 1. Topology与physical evidence

- activation `e40ce0dfed03dca4d7b71650907b895a07925311`是`bddf374606ff34a7cd32ad9ba15089df70d0bb05`direct child，subject `chore(plan): execute real manifest self-check`，activation gate通过。
- evidence `766408d6ad3bac646a19078fdb0ad04aab8b85b7`是activation direct child，subject `chore(evidence): record real manifest self-check`，changed path exact `.agent-work/EXECUTION_RESULT.md`。
- parent ER bytes/SHA-256 `1408527` / `43488ee147e21835e6ab81cb7b588f74236428b33f3a4924a858aceb74624ac0`；child `1411661` / `a44ed995502c1955c54f44a5e8c8d65c7f01889eda229e7f2cb435940b6eb125`。
- child以parent为exact prefix；唯一physical EOF suffix bytes/SHA-256 `3134` / `b2fc662f3b255efd6bbd157e689292f52f899fac437c2fc61b5101f14b20a7ca`；handoff heading只出现一次。
- fresh source `/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b3-real-self-check-r5-e40ce0dfed03-source.py`：device/inode `16777240/2273267`，mode `0600`，bytes `13352`，SHA-256 `0d285fbe1dd2ddf40b3b979c41b1f304b9ebb6fec108c9d1616240518b55e936`，pre/post exact。
- fresh root `/Volumes/4T/temp/rgbww-optimizer/p7-td-b-retained-r3-option-b-b3-real-self-check-r5-e40ce0dfed03`：device/inode `16777240/2273270`，mode `0700`，inventory exact empty。

## 2. Failure与scope containment

first failure发生于`contract_write`：execution contract仍含P3 strict decoder产生的frozen tuple/mapping containers，直接交给`persist_canonical_json`，其`canonical_json_bytes`以`json_unsupported_value`拒绝。

Planner独立source检查确认contract persist位于line 52，而primary `try`从line 55开始；因此serialization failure未进入计划要求的failure lifecycle，无法写`99-terminal-summary.json`及seal。root虽已创建但contract writes与terminal writes均0。这是controller transport/lifecycle缺口，不是manifest、C1、retained或typed owner结论。

失败严格发生在任何真实输入访问之前：R4 preparation、manifest、C1、retained root/file reads全部0；Git byte acquisition、required argv、owner call、18 ledgers全部0。canonical validator、eligibility、release consumption、network、device、camera、Ray、strip、formal、public analyzer均0。retry/fallback/postappend operations均0；无输入或repository写入。

## 3. Planner决定

拒绝R5执行，不能声称real self-check或terminal lifecycle通过。保留empty failure root与source为immutable evidence，禁止复用、删除、repair或从该root重建常量。

最小纠偏不是直接再次读取真实输入，而是先执行`REF-P7-25-R2-B3-C3-C4-R5-C1`纯离线synthetic contract/lifecycle gate：

1. local one-off `_json_native`递归把Mapping转plain dict、tuple/list转plain list；只允许string keys及`None/bool/int/str` concrete scalars，其他值stable fail closed。
2. contract native conversion、contract persist及seal必须全部位于primary failure lifecycle内。
3. golden synthetic root使用nested mapping proxy/tuple复现本次wire boundary，必须得到contract+seal及success terminal+seal。
4. injected unsupported object必须在contract落盘前失败，但仍在第二个fresh root得到exact failure terminal+seal；不得产生contract文件。
5. 两case均只验证lifecycle，不读取R4 preparation或任何真实artifact，不运行Git/self-check/validator。

C1被Planner接受后才可另行授权一次fresh R5 real execution；失败root永远不复用。

## 4. Failure branch与锁

C1任一source/root已存在、native conversion、contract/seal、failure terminal/seal、canonical re-encode、inventory或counter不符即hard fail；保留fresh证据，retry/fallback0，停止Planner门。不得把失败解释为real manifest结果或进入真实R5。

canonical validator、eligibility、release consumption、network/device及全部后续科学阶段继续锁定；不需要Advisor决策或Human设备授权。

维护性判断：缺口位于一次性controller的wire adapter与try边界；用bounded synthetic gate覆盖即可，无需修改P3或typed owner，也不应增加共享serialization abstraction。
