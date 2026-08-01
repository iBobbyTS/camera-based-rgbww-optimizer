# P7 retained-R3 Option B：B3-C3-C4-C1 internal-backtick gate review

**Planner review date：** `2026-08-01`

**Reviewed reference task：** `REF-P7-25-R2-B3-C3-C4-C1`

**Decision：**
`REJECTED_NON_CONTRACTUAL_INTERNAL_BACKTICK_CARDINALITY_GATE_PHASE1_FAIL_FAST_EFFECTIVE`

**Exact next branch：** `REF-P7-25-R2-B3-C3-C4-C2`；fresh successor只允许固定索引验证`row[0] == '`'`、
`row[-1] == '`'`，随后exact `inner = row[1:-1]`，再验证inner exact prefix并strict JSON。禁止对whole row或inner执行backtick
`count/find/index/rfind/rindex/in`扫描。Phase1仍保持root touch/create0；通过后才进入独立Phase2全新root与exact-one Git diagnostic。

## 1. Topology与EOF evidence

- Activation `eb33eba3aa2a6942370850b80645fc5e146a425b`是parent
  `e0b0e34116ddb3c09a7072f1c3782786ee6ad9d0`的direct child，subject exact
  `chore(plan): correct patch diagnostic pre-root gate`，tree `47794dd0d67ec8718a4bdb33c6c801692fff1dca`，changed paths exact
  FULL/PLAN/`20260801-0748-...failure-review.md`三项。
- Evidence `cdbb4b7f7a7461d9af490efb48f572e08b0cc862`是activation direct child，subject exact
  `chore(evidence): record C4-C1 delimiter stop`，只改ER。
- ER prefix blob/bytes/SHA-256为`cde8e55036f9368c2f17821d5559faa6b6171208` / `1358875` /
  `d5a8b60c676a6cd9f4d8eb39dd7f05a2bbdf28b2a4a38274d9d462677f6220fb`。Suffix是physical EOF-only 6行、2877 bytes，SHA-256
  `96d3e909e357f87c832efe6f07782dca6678b340d158a9c080098d89ae464b0f`；after blob/bytes/SHA-256为
  `2c3074a7a5c4ac0f60c17cc7bbd48065085bdcad` / `1361752` /
  `0e224d9bfc418fd476b70649f295cd6a8c868b5f92a0b3a95777dc880be6d9f7`。

## 2. First failure与Planner finding

Phase1正确读取committed PLAN/FULL各一次并strict UTF-8 decode，找到exact candidate row1；但Executer自行增加whole-row
`row.count(backtick) == 2` gate。PLAN只授权opening/closing delimiter与机械slice，并未要求row中只能有两个backtick。Machine JSON中的Markdown或contract
string可合法包含内部backtick，因此该新增cardinality gate在`row[1:-1]`和strict JSON前错误拒绝输入。

这不是PLAN/FULL schema、Git object或M1 patch finding，而是执行器扩大pre-root parser语义。C2必须避免任何whole-row/inner backtick扫描：

1. exact candidate row已经由冻结prefix定位；
2. 仅以固定索引断言首字符和末字符分别为backtick；
3. exact `inner = row[1:-1]`；
4. inner只检查expected `PLAN_MACHINE_CONTRACT=`或`FULL_PLAN_MACHINE_STATE=` prefix；
5. JSON payload只按prefix长度slice并strict parse。内部backtick属于JSON string内容，不得特殊处理。

## 3. Fail-fast、effects与locks

本轮fail-fast边界有效：Phase1 exit1后Phase2未启动；root touches/creates、controller creates/invocations、canonical Git diff、diagnostic writes全部0。
Failed roots reads/reuse0，retry/fallback0。Process scan1且owned processes0，ER single append后operations0。

Remaining self-check、focused/full、synthetic、external artifacts、working-tree source/test、canonical validator、retained audit、eligibility、release、network/DNS/
environment/credentials、device/camera/Ray/strip/cleanup/capture/FORMAL/public analyzer/TD-C/sentinel/P8/firmware/deployment全部0。Retained R3保持
`RETAINED_UNVALIDATED_UNCONSUMED`。Canonical Git stdout仍未观察，不得归因patch bytes或声称provenance drift。

维护性判断：纠偏只删除未授权的内部delimiter cardinality检查，保留既有two-phase process boundary；无需新增parser framework、production或test改动。
