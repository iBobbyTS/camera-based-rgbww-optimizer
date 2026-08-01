# P7 retained-R3 Option B：R3-C1 pre-edit budget与non-EOF handoff review

**Planner review date：** `2026-08-01`

**Reviewed reference task：** `REF-P7-25-R2-B3-C3-C4-R3-C1`

**Decision：** `REJECTED_READ_ONLY_QUERY_BUDGET_EXCEEDED_AND_HANDOFF_NOT_AT_PHYSICAL_EOF`

**Exact next branch：** `REF-P7-25-R2-B3-C3-C4-R3-C1-S1`；执行最小Git/ER-only supersession。S1接受后才恢复same exact-two C1 correction及已冻结八findings。

## 1. Topology与candidate preservation

- Activation `ff372c136516fd785ec94adfeeb50063c3873c83`是parent `2a9ebca4fcddd0bfccfe051e45227c03891fecdf`的direct child，tree `27782d04de95f6b4e01abcdfc2a61a8bd0d42047`，subject exact `chore(plan): correct typed real self-check owner`，changed paths exact FULL/PLAN/`20260801-0909` archive。
- Evidence `b83ba49031d48c1545011fc7ca64910d636f575e`是activation direct child，tree `00779de551c13a27d3a8d23e4c98e5f11bbcaf09`，subject exact `chore(evidence): record real self-check correction`，changed path only ER。
- Exact-two untracked candidate未变：source 21578 bytes/SHA `e8e35afce150ac85cca816a6baf81c6b4dd394f061cfd93b44666f7c35842885`；test 17922 bytes/SHA `d913b633093f49ada912a226917a6cb254baeaad40cef935a8fd67427f29a3fb`。Patch writes、tests、compileall、post-CodeGraph与implementation commit均0。

## 2. Read-only budget review

C1错误新增一次pre-edit CodeGraph query，超过冻结预算0；它是只读工程治理偏差，不是production、scientific、real-artifact、network或device问题。该query不计作C1 credit，也不改变Planner已冻结的八项finding。Executer随后正确保持source/test patch0及所有后续validation0。

## 3. Physical placement proof

Activation ER blob/bytes/SHA为`a91062d7a47b4e20e5bed0e2ad1badd8932b3ee7` / `1389034` / `4a3bfe71e531b98d2ed76adf70eb9b9fde390c9ed3a673191f5f16474f6aee23`；evidence ER blob/bytes/SHA为`ecd97ade34e5aa7402afbe945d7194307e9284b4` / `1392359` / `e1407040bf5d1c454706cf1e4242d034f243539118db1f4aebab391ceabcca2b`。

Line-aware comparison证明：共同prefix为前40行、2580 bytes、SHA `6c18f5e876c3eb59b63fa9f6ddf8d42a7513bc5254dc1231c6c84d20feeb6f14`；新增block位于line41，共6行、3325 bytes、SHA `7ad28a388ec2f94e01ac128ed90b2ce854d97ad80c3aaf049ab6c37edb387c5d`；原preserved suffix为17705行、1386454 bytes、SHA `e69917f5a7017510bb9c0b5c79c77440d18bd5816300dd3ce856fb1d72229e58`，与新文件line47后完全一致。前后final 256 bytes SHA均`039f56395f2649fbce1ada716feb34f58394d11dd714f29d253de070bcdb5ed4`。

因此block内容可保留为历史事实，但不是physical terminal handoff，必须由EOF supersession明确降级。

## 4. Credit与next locks

R3-C1不获得patch/test/production credit。S1只修handoff placement，不重跑CodeGraph、不触碰candidate。S1接受后的fresh C1 activation继续要求new pre-edit query0，并直接消费已冻结candidate identity与八findings；不得把误发query包装成新credit。

Real artifacts、validator、eligibility、release、synthetic、网络及设备继续全部锁0。

维护性判断：保留不可变历史并用单一EOF supersession修正authority，避免重写大ER；production correction仍与治理修复隔离。
