# P7 retained-R3 Option B：R3 targeted failure与production static review

**Planner review date：** `2026-08-01`

**Reviewed reference task：** `REF-P7-25-R2-B3-C3-C4-R3`

**Decision：** `REJECTED_TARGETED_FIXTURE_AND_PRODUCTION_JSON_IDENTITY_CONTRACT_DEFECTS`

**Exact next branch：** `REF-P7-25-R2-B3-C3-C4-R3-C1`；保留当前exact-two untracked candidate，在同两路径完成bounded correction后执行fresh targeted12/focused53/full822。

## 1. Topology、EOF与candidate identity

- Activation `b955866b0418bf325c9dd3c0b90bfe5f2008a73e`是parent `329e501645bdeb58aae43087d09fb094ebbd2be2`的direct child，tree `90557e2414b6550336cfdfc5599448d4fe1b142c`，subject exact `chore(plan): activate typed real self-check owner`，changed paths exact FULL/PLAN/`20260801-0853` archive。
- Evidence `2a9ebca4fcddd0bfccfe051e45227c03891fecdf`是activation direct child，tree `a702895ceeb4c60579760929543daa5d4d00c057`，subject exact `chore(evidence): record typed real self-check owner`，changed path only ER。
- ER prefix blob/bytes/SHA为`fc0494465142104b64158db4746e59f63aaae80c` / `1385276` / `1424c20efce1eb9b082dbe17b92d22e0b876faf578941803c7b69d55c342ff61`；physical EOF suffix为6 lines、3758 bytes、SHA `e946a155ae8cc88e1af1799d66a3a8938cb90a7063da80c4f031462bfeafa71c`；after blob/bytes/SHA为`a91062d7a47b4e20e5bed0e2ad1badd8932b3ee7` / `1389034` / `4a3bfe71e531b98d2ed76adf70eb9b9fde390c9ed3a673191f5f16474f6aee23`。
- Preserved untracked source为21578 bytes/SHA `e8e35afce150ac85cca816a6baf81c6b4dd394f061cfd93b44666f7c35842885`；test为17922 bytes/SHA `d913b633093f49ada912a226917a6cb254baeaad40cef935a8fd67427f29a3fb`。除这两路径外porcelain为空。

## 2. Execution review

Targeted一次发现12/12 errors、0 failures，first failure exact `TEST_FIXTURE_CANONICAL_JSON_TUPLE_UNSUPPORTED`：fixture把tuple交给P3 strict JSON encoder，subject invocations与Git calls均0。Focused/full/compileall/CodeGraph post/commit/posttarget均0；retry/fallback0。Real/C1/retained artifacts、external roots、validator/eligibility/release、网络与设备均0。

因此不接受R3，也不授予production、test、B3或real-artifact credit。Pre-edit CodeGraph query与exact-two candidate creation可作为C1的已完成credit保留。

## 3. Frozen Agent-fixable findings

独立静态审查确认six-export与no-persistence/no-validator边界方向正确，但production不能默认正确：

1. `FIXTURE_JSON_CONTAINER`：manifest fixture须在P3 encoding前显式转成JSON lists。
2. `DECODED_MAPPING_IDENTITY`：P3 decoder返回immutable mapping；`_exact`先比较concrete type，导致所有合法decoded objects与expected dict mismatch。Mapping双方须按exact key set/value/type比较；scalar仍严格type equal。
3. `REPORT_JSON_CONTAINER`：success report payload仍含tuple，P3 canonical encoder必然`json_unsupported_value`；须显式构造JSON-native lists后canonical encode/redecode。
4. `PHYSICAL_ROOT_IDENTITY`：五artifact只比较共同root相等，未验证shared root absolute/direct identity、mode0700、positive device/inode，也未拒绝file inode alias。须fail closed。
5. `TYPED_POSITION_LABELS`：C1 four与retained three只验证cardinality，未冻结M1 exact labels/order；任意label可自洽通过manifest。须使用exact ordered constants。
6. `SEAM_KEY_COLLISION`：helper/test paths及commit/path key集合使用set后未先证明expected cardinality，collision可折叠。须冻结distinct path/commit chain及exact key cardinality。
7. `DIFF_TREE_ORDER`：现实现排序observed paths再比较，允许swapped stdout；ordered ledger必须要求decoded path tuple与activation.changed_paths exact一致。
8. `REPORT_LEDGER_FACTS`：report只保存stdout hashes；应确定性保存每条validated ledger的argv/cwd/exit/stdout SHA/stderr SHA，仍不产生authority。

以上均在原exact-two路径内局部可修，无需修改P3/M1或新增owner。

维护性判断：C1不改变owner边界，只修严格JSON/identity语义并补负例；完整ledger facts留在同一report owner，不引入durable persistence或第二Git authority。
