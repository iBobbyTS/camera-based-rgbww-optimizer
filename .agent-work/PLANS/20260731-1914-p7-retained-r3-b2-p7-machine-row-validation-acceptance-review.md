# REF-P7-25-R2-B2-P7-C1-C1-C1-C1-V1-C1-V1-C1-C1：Markdown machine-row validation acceptance review

**Planner 日期：** 2026-07-31

**Reviewed reference：**
`REF-P7-25-R2-B2-P7-C1-C1-C1-C1-V1-C1-V1-C1-C1`

**Reviewed contract：**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-P7-C1-C1-C1-C1-V1-C1-V1-C1-C1-MARKDOWN-MACHINE-ROW-DELIMITER-VALIDATION-CLOSURE-V1`

**Planner decision：**
`ACCEPTED_COMPLETE_REPO_OWNED_RUNNABLE_DOMAIN_TEMPLATE_OWNER`。

Candidate `864f08cc5436519a37e41d553e49ebde4a3c8bb2` 的 exact runnable-domain-template
implementation 现在可作为后续 pure-offline fresh synthetic-integration package 的 immutable implementation input。
该接受不代表 synthetic integration 已通过，不使 retained R3、subordinate manifest、canonical validator、eligibility 或 release
可消费，也不授权 network、device、camera、Ray、strip、FORMAL 或后续 scientific stage。

## 1. Reviewed scope and method

本 review 只读取 active PLAN、FULL reference、EXECUTION_RESULT、相关 Git commit/file identities 与既有 archive；没有重跑
pre-gate、targeted、focused、compileall 或 full tests，没有读取 retained R3/candidate payload，没有调用 external controller、validator、
release、network 或 device。Review 方法为：

1. 独立核对 activation、evidence 与 candidate 的 full commit topology、subject 和 exact changed paths；
2. 重算 candidate canonical binary diff SHA-256，并将 candidate source/test blob 与 current HEAD blob 对比；
3. 对 current PLAN/FULL 各自使用合同冻结的 exact backtick-wrapped line regex，要求 exact one match并 strict JSON decode；
4. 核对 active PLAN、prior archive、ER before/after bytes/SHA、evidence commit exact append 与 marker delta；
5. 对照 PLAN 检查 initial-clean、pre-gate、targeted、focused、compileall、full、final-clean 的唯一调用、顺序、exit、counts、
   evidence-write ordering、retry/fallback 与全部 zero budgets；
6. 从 FULL 选择下一依赖时确认：P5 runtime owner与P6 deterministic builder已 accepted，但 FULL 尚未登记 P7 acceptance 后的
   stable successor reference/contract，因此本 review 不自行发明可执行 ID或解锁 real B2。

## 2. Frozen topology and identities

- Review HEAD/evidence commit：`2e969389ded82fe0e6c3d6d19431c46c8e38cbd3`，direct parent
  `ecf5eb7310fa8470d0b47b09c692102e2238b9f2`，subject
  `chore(evidence): record p7 machine row validation`，changed path exact
  `.agent-work/EXECUTION_RESULT.md`。
- Activation：`ecf5eb7310fa8470d0b47b09c692102e2238b9f2`，direct parent
  `30aa4f281f6fe2fb825ba2240cfce779fdba47e4`，subject
  `chore(plan): activate p7 markdown machine row validation closure`，changed paths exact FULL、PLAN 与
  `.agent-work/PLANS/20260731-1835-p7-retained-r3-b2-p7-markdown-machine-row-gate-failure-review.md`。
- Reviewed active PLAN：bytes `12077`，SHA-256
  `ee8a42993ad4c01ea792bf9b81b2d73b76c5134de4b4ae5c74f47e23de361903`。
- Prior review archive：bytes `6222`，SHA-256
  `296b9eefb701efdf6b54cefe502881ca1b5c13e909bd4eb6058808452521da14`。
- Candidate：`864f08cc5436519a37e41d553e49ebde4a3c8bb2`，direct parent
  `44fb7295f0f71030833476225350da01ce3c71d3`，subject
  `chore(p7): retain rejected outer plain nul candidate`，changed paths exact：
  `src/camera_based_rgbww_optimizer/utils/p7_retained_r3_controller_domain_template.py` 与
  `tests/test_p7_retained_r3_controller_domain_template.py`。
- Candidate canonical binary diff SHA-256：
  `b03b1a049a407e2049f049b6f2514497e6d5bb82675f14dc750f00cc09ce6bd4`。
- Source blob/bytes/SHA-256：`5529ec27b3893c20995e9a8cb3a9fa5c0a87a3b5` / `19753` /
  `10969de79f5afece8018f094823efcf6f60237670ed1eeb54135f451ef0425c2`。
- Test blob/bytes/SHA-256：`d0f733426673aa9a57fcb1195ecea014f8c48062` / `27386` /
  `4c3b93d4a2f5967b91cb48a2dea1c0a0f8994fb687f6109830d24602bb93083e`。
- Current HEAD 的 source/test blob与 candidate上述两个 blob逐一相同；candidate之后这两个路径没有 later commit，证明本轮没有
  code/test drift。

## 3. Machine-row and evidence validation

Planner 对 authoritative current rows使用 exact patterns：

```text
^`PLAN_MACHINE_CONTRACT=(\{[^\r\n]*\})`$
^`FULL_PLAN_MACHINE_STATE=(\{[^\r\n]*\})`$
```

结果为 PLAN exact one match、FULL exact one match；两段 captured JSON均 strict decode为object，且 active/reference task都为
`REF-P7-25-R2-B2-P7-C1-C1-C1-C1-V1-C1-V1-C1-C1`。这关闭了前一包只匹配bare marker row的harness defect；没有使用
generic Markdown parser、alternative、fallback、repair或regeneration。

ER在 activation 时为 bytes `1129765`、SHA-256
`954e378e23fd9dfc4f6bf0f50da765076db54d5c62030995207c983f674c76b3`；当前为 bytes `1133941`、SHA-256
`a60e328ae4c47abd5f56d2116b8239fcb1bb4f23c969001a3b4dde8b1e060f6f`。Evidence commit只在EOF新增 exact `13` 行，
旧prefix未修改；旧prefix没有成功marker，本提交新增一条独立行 `PRE_GATE_LOGICAL_EXIT=0`，current total exact one。

## 4. Validation quality and invocation ledger

Committed terminal handoff证明同一 fresh validation sequence按合同顺序完成：

- initial-clean invocation `1`，exit `0`，在任何ER bytes之前确认 clean；
- corrected pre-gate invocation `1`，Python body与wrapper exit均 `0`，ordinary `pregate_exit`立即持有logical exit；
- targeted invocation `1`：`11/11`，exit `0`，`OK`；
- focused invocation `1`：`93/93`，exit `0`，`OK`；
- compileall invocation `1`：exit `0`；
- unique full invocation `1`：`778/778`，exit `0`，`OK`，同一terminal summary；
- final-clean invocation `1`：exit `0`，HEAD与candidate identities未变，porcelain bytes `0`；
- stream reconnection只恢复了in-memory observations；上述任何已完成stage均未重跑；
- pre-initial-clean ER bytes `0`、pre-terminal ER bytes `0`、terminal后single EOF append `1`；
- retry/fallback `0/0`，CodeGraph `0/0`，implementation commit与postcommit test `0/0`。

Gate还覆盖 strict UTF-8、source/test AST+compile、exact `11` methods、module physical NUL `0`、outer `_plain`
NUL/LF/CR `1/1/1`、public physical-NUL reject与literal escape accept、template/replacement exact identities、escape counts
`8/3`、exact16 ordered matrix、test03/test08与runnable lifecycle inventory。Evidence与current Git identities相互一致。

## 5. Zero budgets and acceptance boundary

Code/test/template/replacement/serializer/matrix/owner/API/helper writes，third path，PLAN/FULL/archive/debug/GUIDE/RESEARCH
writes by Executer，external controller/source/root/process，synthetic integration，old failed evidence reads，retained artifact与candidate
payload reads，Git provenance replay，real B2，subordinate manifest，canonical validator，eligibility，retained audit，release
generation/qualification/copy/consumption，network/DNS/environment/credentials/device/camera/Ray/strip/cleanup/capture/FORMAL/public
analyzer/TD-C/sentinel/P8/firmware/deployment全部保持 exact `0`。

因此，本 decision只把 `864f08c...`接受为repo-owned runnable domain-template owner，可由未来Orchestrator明确登记的pure-offline
synthetic-integration successor消费。Retained R3继续为`RETAINED_UNVALIDATED_UNCONSUMED`；canonical validator仍是唯一eligibility owner；
real B2、release与所有设备/科学路线继续locked。

## 6. Findings, residual risks and exact next branch

本 review没有发现 candidate semantic、test、topology或evidence-order finding。唯一 residual 是roadmap ownership：current FULL只记录
本 P7 task为active，尚未定义接受后的稳定 successor ID、exact synthetic input/root/process budgets、artifact/lifecycle evidence或 acceptance
contract。P5-I1的旧包因canonical domain template未冻结而rejected，不能被直接重试；现在P5 runtime、P6 deterministic builder、P7 runnable
template的依赖已具备，但必须由Orchestrator决定是创建fresh P5-I1 successor还是新的reference ID，并更新FULL machine state。

**Exact next branch：** `PLANNER_STOP_WAITING_ORCHESTRATOR_P7_ACCEPTANCE_AND_FRESH_SYNTHETIC_INTEGRATION_ROUTE`。

Orchestrator下一步应：

1. 接受或覆核本decision，并在FULL把P7标为accepted、candidate consumable仅限offline integration input；
2. 登记唯一fresh synthetic-integration successor ID与engineering contract，明确复用P5/P6/P7 owners且禁止第二controller/analyzer/lifecycle；
3. 保持retained R3、real B2、validator、eligibility、release、network/device/scientific locks；
4. 再让Planner把该唯一successor写成可执行PLAN。当前PLAN stop本身不授权Executer或任何effect。

维护性判断：P5 runtime、P6 deterministic builder与P7 runnable template保持分层单一owner；本接受不新增抽象。下一包应只组合
既有owners做fresh synthetic qualification，避免恢复disposable generated-controller或平行state machine。
