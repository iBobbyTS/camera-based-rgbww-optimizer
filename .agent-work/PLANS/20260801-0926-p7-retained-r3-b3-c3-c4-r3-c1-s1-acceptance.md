# P7 retained-R3 Option B：R3-C1-S1 physical-EOF supersession acceptance

**Planner review date：** `2026-08-01`

**Reviewed reference task：** `REF-P7-25-R2-B3-C3-C4-R3-C1-S1`

**Decision：** `ACCEPTED_COMPLETE_PHYSICAL_EOF_SUPERSESSION`

**Exact next branch：** `REF-P7-25-R2-B3-C3-C4-R3-C1-R1`；恢复same exact-two bounded correction，冻结new pre-edit CodeGraph queries为0并直接消费Planner/Orchestrator已提供的八findings。

## 1. Topology与candidate identity

- Activation `0ef6198038160ac19cfeaa780a289c9a9f0cd360`是parent `b83ba49031d48c1545011fc7ca64910d636f575e`的direct child，tree `d1b7e9370985a816595fee8ae0ff0748080c5cb0`，subject exact `chore(plan): supersede non-eof correction handoff`，changed paths exact FULL/PLAN/`20260801-0918` archive。
- Evidence `3bc46c5a866d5f3f8d303224fcb582a4de630e8d`是activation direct child，tree `50cfe0ee64c389d7eee1edb0b2555bcc76239928`，subject exact `chore(evidence): supersede non-eof correction handoff`，changed path only ER。
- Exact-two untracked candidate保持不变：source 21578 bytes/SHA `e8e35afce150ac85cca816a6baf81c6b4dd394f061cfd93b44666f7c35842885`；test 17922 bytes/SHA `d913b633093f49ada912a226917a6cb254baeaad40cef935a8fd67427f29a3fb`。Porcelain无其他项。

## 2. Independent physical-EOF proof

Activation ER blob/bytes/SHA为`ecd97ade34e5aa7402afbe945d7194307e9284b4` / `1392359` / `e1407040bf5d1c454706cf1e4242d034f243539118db1f4aebab391ceabcca2b`；evidence ER blob/bytes/SHA为`85892b64b4b5a85a15715ccf4c672017ac3746a6` / `1396492` / `55cf0d3daf6f2489d4f89685c12bb8542b36007d9d4f48e1cebe94a0629850c7`。

Evidence的前1392359 bytes与activation ER byte exact；其后append为6行、4133 bytes、SHA `0df6b914dca2988607d2adf403bbd6467beb410f93906d9c1443ed5cdd93591b`，并结束于closing fence+LF，故supersession位于physical EOF。

原non-EOF block仍为line41起6行、3325 bytes、SHA `7ad28a388ec2f94e01ac128ed90b2ce854d97ad80c3aaf049ab6c37edb387c5d`；其后preserved suffix仍为17705行、1386454 bytes、SHA `e69917f5a7017510bb9c0b5c79c77440d18bd5816300dd3ce856fb1d72229e58`。两者均未改写。

## 3. Acceptance scope

S1 exact budgets与locks成立：CodeGraph/source/test edits/tests/implementation commit、real artifacts、validator/eligibility/release、external/network/device均0。只读超预算query继续分类为`READ_ONLY_BUDGET_EXCESS_NO_CREDIT`，S1不授予production或B3 credit。

R1直接消费已经冻结的八findings：fixture JSON container、decoded mapping identity、report JSON container、physical root identity、typed position labels、seam key collision、diff-tree order、report ledger facts。无需新的pre-edit发现或CodeGraph query。

维护性判断：EOF authority已恢复且历史块保持不可变；后续可重新隔离执行production correction，不需重写ER或扩大owner边界。
