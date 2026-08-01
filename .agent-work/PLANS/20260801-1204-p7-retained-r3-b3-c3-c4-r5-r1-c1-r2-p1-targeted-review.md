# P7 retained-R3 Option B：P1 machine-row parser targeted failure Planner 验收归档

**Planner 日期：** `2026-08-01`

**Reviewed reference task：** `REF-P7-25-R2-B3-C3-C4-R5-R1-C1-R2-P1`

**Reviewed contract：** `P7-TD-B-RETAINED-R3-OPTION-B-B3-C3-C4-R5-R1-C1-R2-P1-REPO-OWNED-MACHINE-ROW-PARSER-V1`

**Reviewed PLAN identity：** bytes `12566`；SHA-256 `d14bbe18c78bac7689f3bdb567443e2cf333ab3935debfb429e7c7b1b18d7c06`。

## 1. 冻结输入与证据身份

- activation commit：`6d2a8c24554a9235f028a85ac316c25bca1951af`；parent `89099740bc0b4fa8babc3be233a5f53ab3d697b2`；subject exact `chore(plan): harden machine row parser owner`；changed paths exact FULL、PLAN与`.agent-work/PLANS/20260801-1153-p7-retained-r3-b3-c3-c4-r5-r1-c1-r2-review.md`。
- evidence commit：`6a8ae8fcbecb311bfe53c3cc4d13773ef49956be`；parent exact activation；subject exact `chore(evidence): record machine row parser owner`；changed path exact `.agent-work/EXECUTION_RESULT.md`。
- canonical handoff schema：`p7_td_b_retained_r3_option_b_b3_c3_c4_r5_r1_c1_r2_p1_machine_row_parser_result_v1`；complete-last-section-heading-to-physical-EOF handoff已由Orchestrator提交。
- implementation before identities：source bytes `7230`、SHA-256 `743e2948f6c30a31fde5d072c8effa8b1365d321b303d61e9899ad18ac41825f`、blob `5c581f9b502bcab1809b6a61a082a47f4150e09f`；test bytes `9820`、SHA-256 `32c0d47cfcdfa49ecad2a4976f401021f0ff1bef947eab705a8c89836b2f5a19`、blob `c9589947e876920f0cbd2fe7e113592e3cd390e1`。
- preserved dirty identities：source bytes `9414`、SHA-256 `a02a30c026fba548c81c04a277e2f235385ddb8a459c4ff2f73c91ee87c3737e`、Git blob `ce2200181bd2a493cfaab621daa17b89a13bdf1f`；test bytes `13411`、SHA-256 `5e5aa5831edc50d695a09cb473333450f68820cfaddedc054d8bb010314ba920`、Git blob `5efc93c11b37de900f67b3d1c4aa734048d035fc`。

## 2. 执行事实与 validation quality

Activation metadata、archive identity、required FULL subset与clean pre-edit gate均通过。一次CodeGraph preflight确认既有single owner、dedicated test及直接caller/test blast radius。Executer在exact source/test各完成一次patch，新增通用`parse_machine_row`，保留两个legacy wrapper并委派同一core；成功值递归冻结为`MappingProxyType`/tuple。

唯一targeted suite实际运行`15` tests：`13` pass、`2` fail。失败断言为：

1. `test_generic_parser_supports_custom_marker_and_legacy_wrappers_delegate`仍把deep-immutable结果与nested mutable dict/list literal直接比较；
2. `test_valid_plan_and_full_rows_preserve_values_and_replay_evidence[PLAN]`仍把deep-immutable结果与`json.loads`产生的nested dict/list直接比较。

失败后按PLAN fail-fast，focused/full、compileall、CodeGraph sync/post-query、diff/status、implementation commit及postcommit targeted全部为`0`。source/test更改保留为exact two uncommitted paths；没有新增parallel module或其他repository write。real artifacts、old roots、self-check owner、canonical validator、eligibility、release、network、device、camera、Ray、strip、cleanup、formal与public analyzer均为`0`；retained R3继续`RETAINED_UNVALIDATED_UNCONSUMED`。

## 3. Planner findings 与决定

**Decision：** `REJECTED_P1_COMPLETION_PRESERVE_CONTRACTUAL_IMPLEMENTATION_FOR_BOUNDED_TEST_CORRECTION`。

P1不得获得完成、full validation或implementation commit credit，因为targeted未全通过。但是失败分类不是生产实现违反deep immutability合同；恰好相反，失败是两处测试期望仍把JSON array视为mutable list，而active PLAN明确要求array递归变为tuple、mapping递归变为read-only Mapping。为让失败断言通过而把生产返回值改回dict/list会直接违反合同。

下一包只能在现有dedicated test内建立test-only JSON semantic comparison adapter（或等价逐层断言）：比较key、scalar及序列元素语义，同时继续由既有immutability test独立断言每层`MappingProxyType`和tuple。不得为测试方便在生产owner增加thaw/serializer、可变返回、第二个API或自定义相等语义。

现有source diff应原样保留且source write budget为`0`；现有test diff也应保留，仅允许一次bounded test patch修复这两类stale expectation并补足adapter自身对nested object/array/scalar的有效断言。纠偏后必须从targeted开始重新运行完整validation；在targeted通过前focused/full/commit继续锁定。

这是测试/工程合同纠偏，不是色彩或测量科学分支，不需要Advisor；没有设备操作，不需要Human授权。

## 4. Residual risks 与 exact next branch

- 当前实现尚未经过focused/full/compileall及postcommit targeted，不能推断caller兼容性或最终接受。
- test-only adapter必须只用于断言语义等价，不能掩盖container type；deep immutable container type由专门断言继续冻结。
- activation发生时worktree预期保留exact two dirty implementation paths；Orchestrator只能提交FULL、PLAN与本归档，不得误stage实现。
- successor不得读取real artifacts/old roots，不得调用self-check owner、validator或release；P1-C1验收前R2 real successor仍锁定。

**Exact next branch：** `REF-P7-25-R2-B3-C3-C4-R5-R1-C1-R2-P1-C1`，唯一test-expectation correction与完整validation package。Planner stop为`B3_C3_C4_R5_R1_C1_R2_P1_C1_IMMUTABLE_EXPECTATION_CORRECTION_WAITING_PLANNER_REVIEW`。
