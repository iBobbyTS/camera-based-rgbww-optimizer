# P7 retained-R3 Option B：M1-C1 pre-edit method-count gate failure review

**Planner 日期：** `2026-07-31`

**Reviewed reference task：** `REF-P7-25-R2-B2-M1-C1`

**Reviewed contract：**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-M1-C1-EXISTING-ROOT-IDENTITY-OWNER-V1`

**Planner decision：**
`REJECTED_PRE_EDIT_METHOD_COUNT_BASELINE_MISMATCH_NO_IMPLEMENTATION_ATTEMPT`

## 1. Reviewed scope 与 activation

本次审核只覆盖由activation `03533a442efa16909a2c0c80e0ffe1cc2d418630`授权的M1-C1 existing-root identity
owner correction。该activation是`195afbe54caeda01fcf65af4d97604665d5e7adb`的direct child，subject exact
`chore(plan): activate existing root identity owner correction`，changed paths exact FULL/PLAN/
`.agent-work/PLANS/20260731-2111-p7-retained-r3-b2-m1-existing-root-owner-gap-review.md`三项。

Evidence commit为`c3018460a6748e447894d83cee5cc8c2851bd750`，是activation direct child，subject
`chore(evidence): record existing root owner count gate`，changed path只有
`.agent-work/EXECUTION_RESULT.md`。Executer报告activation topology、clean porcelain、archive bytes/hash、PLAN/FULL strict machine
JSON与required FULL subset全部通过。

## 2. Execution evidence 与 first failure

Executer在任何source/test edit前按合同执行CodeGraph pre-edit sync/query exact `1/1`且均exit `0`。Query确认P3仍是physical
provenance-I/O owner、P4仍是AST/effect provenance owner、没有public existing-root owner，并确认当前shared-root rejection。

随后pre-edit静态method inventory发现：

- `tests/test_p7_retained_r3_provenance_io.py`（P3）实际已有`24`个`test_*` methods；
- `tests/test_p7_retained_r3_controller_conformance.py`（P4）实际已有`20`个`test_*` methods；
- targeted baseline实际为`44`，而active PLAN错误冻结为old `18/14`、final `22/19`、targeted `41`。

该差异命中active PLAN的mandatory pre-edit count gate。Executer按约束立即fail closed，未自行纠正PLAN，未执行测试或写入实现。
`.agent-work/EXECUTION_RESULT.md`中唯一handoff判定为`REJECTED_PRE_EDIT_METHOD_COUNT_BASELINE_MISMATCH`。

Planner另对focused命令中未受本包修改的两个owner做source-backed只读静态复核：

- `tests/test_p7_retained_r3_controller_runtime.py`（P5）为`6`个`test_*` methods；
- `tests/test_p7_retained_r3_controller_domain_template.py`（P7）为`11`个`test_*` methods。

因此new exact P3 `+4`、P4 `+5`后，correct final inventory应为P3 `28`、P4 `25`、targeted `53`；focused为
`28 + 25 + 6 + 11 = 70`。Full baseline仍为最后已验证的`778`，新增exact `9`后为`787`。

## 3. Validation quality 与 preservation

本次没有implementation attempt：authorized four paths都保持HEAD blob/bytes/SHA-256不变，`read_existing_root`仍未实现；source writes
`0`、test writes `0`、implementation commits `0`。Targeted/focused/compileall/full/postcommit targeted均为`0`，retry/fallback
`0/0`；这不是narrow-green acceptance，而是合同要求的早停。

CodeGraph pre-edit sync/query `1/1`已被失败包消耗；post-edit sync/query为`0/0`，因为没有edit。Accepted-C1/retained physical
reads、external controller/root/process、synthetic integration、Git replay、real B2、manifest/seal、canonical validator/callback/eligibility、retained
audit/release、network/DNS/environment/credentials、device/camera/Ray/strip/cleanup/capture/FORMAL/public analyzer/TD-C/sentinel/P8/
firmware/deployment全部保持`0`。Retained R3仍为`RETAINED_UNVALIDATED_UNCONSUMED`。

## 4. Decision、residual risk 与 exact next branch

Planner接受Executer的fail-closed行为及evidence真实性，但拒绝M1-C1作为implementation result。失败仅来自Planner冻结了过期的静态method
baseline；P3/P4 owner语义、API/security/path contracts没有被反证，也没有实现可以接受或拒绝。该包不消耗implementation commit机会，不能被视作M1-C1
retry。

唯一next branch是fresh bounded `REF-P7-25-R2-B2-M1-C1-C1`：逐字保留M1-C1的existing-root owner
semantic/API/security/path/CodeGraph/commit contracts，只把静态baseline与derived counts纠正为P3 `24 -> 28`、P4 `20 -> 25`、targeted
`53`、focused `70`、full `778 -> 787`。Fresh successor invocation独立，retry `0`，activation expected parent为current evidence
HEAD `c3018460a6748e447894d83cee5cc8c2851bd750`。

在successor被Planner验收前，M1、M1-I1、real B2、retained validation、release、network/device/FORMAL及所有later routes继续hard
lock。本review不需要Advisor或Human决定。

维护性判断：本轮没有代码变更；next branch只修正source-backed inventory，不改变P3/P4 ownership boundary或实现复杂度。
