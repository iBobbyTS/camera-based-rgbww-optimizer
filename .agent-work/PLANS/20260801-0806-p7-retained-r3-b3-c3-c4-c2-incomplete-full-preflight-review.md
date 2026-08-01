# P7 retained-R3 Option B：B3-C3-C4-C2 incomplete FULL preflight review

**Planner review date：** `2026-08-01`

**Reviewed reference task：** `REF-P7-25-R2-B3-C3-C4-C2`

**Decision：**
`REJECTED_PHASE1_FALSE_SUCCESS_PLAN_ONLY_FULL_AND_REQUIRED_SUBSET_OMITTED`

**Exact next branch：** `REF-P7-25-R2-B3-C3-C4-R1`；停止继续堆叠one-off controller/parser条款，先实现一个repo-owned、dedicated-tested、
pure-offline `PLAN/FULL machine-row preflight + canonical patch diagnostic` owner。后续Executer只能调用accepted stable entry，不再现场重写parser/controller。

## 1. Topology与EOF evidence

- Activation `aa87fad66463fcb50da92c22e0b45460f5a8ab20`是parent
  `cdbb4b7f7a7461d9af490efb48f572e08b0cc862`的direct child，subject exact
  `chore(plan): correct C4-C1 internal backtick gate`，tree `57f74ea3f2fb416e444c6b18b2b62a1149486867`，changed paths exact
  FULL/PLAN/`20260801-0757-...internal-backtick-gate-review.md`。
- Evidence `9e865683b718d1954582bc6ca17489d4582572a4`是activation direct child，subject exact
  `chore(evidence): record C4-C2 incomplete preflight`，只改ER。
- ER prefix blob/bytes/SHA-256为`2c3074a7a5c4ac0f60c17cc7bbd48065085bdcad` / `1361752` /
  `0e224d9bfc418fd476b70649f295cd6a8c868b5f92a0b3a95777dc880be6d9f7`。EOF-only suffix为6行、3832 bytes，SHA-256
  `4124def8a29c89dac7024de9a37b5365b1c1696e3571c42321259c9498b1f649`；after blob/bytes/SHA-256为
  `686578122ac102d165371f5d79810c1da178cb9f` / `1365584` /
  `3e3414808aa54a10fc4523dcbcc1b50235708ef21b8379699145932ed7585126`。

## 2. First failure与effects

C2 fixed-index PLAN parse本身通过：committed PLAN/FULL reads1/1、strict UTF-8 decode2、PLAN candidate1、PLAN parse success1，内部backtick
count/find/index/membership scans0。但Phase1 process在只验证PLAN后错误报告exit0；FULL fixed-index parse attempts/successes均0，PLAN
`required_full_machine_state`与FULL machine state的exact subset comparison也未执行。

因此process exit0是false success，effective contract exit1；first failure exact
`PHASE1_FALSE_SUCCESS_MISSING_FULL_MACHINE_ROW_PARSE_AND_REQUIRED_SUBSET_GATE`。这不是PLAN/FULL内容错误，也不是patch-byte或Git provenance finding。

Fail-fast边界有效：Phase2未启动，fresh root touches/creates、controller、canonical Git diff、diagnostic writes全部0；all failed root reads/reuse0，
retry/fallback0。Process scan1、owned process0；single ER append后operations0。

## 3. Locks与validation limitation

Remaining self-check、focused/full、synthetic、external artifact、real manifest/source、C1/retained、working-tree PLAN/FULL/source/test reads均0。Canonical
validator/callback、retained audit、eligibility、release、network/DNS/environment/credentials、device/camera/Ray/strip/cleanup/capture/FORMAL/public analyzer/
TD-C/sentinel/P8/firmware/deployment全部0。Retained R3仍为`RETAINED_UNVALIDATED_UNCONSUMED`。

Canonical Git diagnostic仍从未执行；expected argv/stdout只来自PLAN，observed fields为null。不得声称provenance drift或恢复后续验证。

## 4. Maintainability decision与enabling refactor

连续三次one-off preflight分别暴露bare-prefix、internal-backtick cardinality、PLAN-only/FULL-omission错误。继续用active PLAN逐轮描述临时inline parser/controller已明显增加
脆弱状态机和审计复杂度。Orchestrator决定先建立最小repo-owned stable owner，Planner接受该维护性纠偏。

CodeGraph确认现有P3 `canonical_json_bytes`负责strict compact sorted UTF-8+LF encoding，`run_read_only_git`负责allowlisted read-only Git与immutable
`GitLedger`；其canonical diff要求exact `git diff --binary --full-index --no-ext-diff <parent> <child> -- <UTF-8-sorted unique paths>`。新owner必须复用这两个
public helper，不复制canonical serializer或通用Git runner。此前one-off argv缺少`--full-index --no-ext-diff`，不得作为新owner默认入口继续复制；它保留为历史
diagnostic evidence。Later stable invocation应使用P3 helper-compatible canonical argv并由新PLAN另行冻结其expected output identity。

New owner只拥有：

- 对caller提供的committed PLAN/FULL bytes做固定首尾索引、inner slice、strict duplicate/nonfinite JSON与required subset exact gate；
- 在preflight完整通过后，通过injected/default `run_read_only_git`执行exact one helper-compatible patch argv；
- 返回immutable typed result与`canonical_json_bytes` report；不persist、不建root、不读external evidence、不拥有validator/eligibility/release/device能力。

Implementation限定一个小module与一个dedicated test；不得编辑P3/P4/P5、manifest owner、GUIDE/FULL或引入CLI/controller framework。实现接受后，另起execution package调用
stable entry并提供committed bytes；本实现包不运行真实Git diagnostic。

维护性判断：两路径enabling refactor把已重复失败的parser/diagnostic状态收敛到单一typed owner与专测，复用P3 serializer/Git边界；这是当前最小必要重构，后续不应再生成
one-off controller。
