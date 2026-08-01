# REF-P7-25-R2-B2-P7-I1-E1 Planner review：audit data-owner assertion failure

**审核日期：** `2026-07-31`

**审核结论：**
`REJECTED_TRANSIENT_AUDIT_DOMAIN_ASSERTION_DEFECT_CANDIDATE_AND_PRIOR_INTEGRATION_EVIDENCE_IMMUTABLE`

**审核对象：** active
`REF-P7-25-R2-B2-P7-I1-E1` / contract
`P7-TD-B-RETAINED-R3-OPTION-B-B2-P7-I1-E1-TERMINAL-COUNT-EVIDENCE-SUPERSESSION-V1`，
activation HEAD `75d6ac5326322f1503c7175c6190db6b26162e2c`，parent
`6c85cdb07a115b16c3879805c0a14f37b866f0df`。

## Reviewed method and evidence

Executer只运行唯一一次bounded read-only audit；未重跑integration、builder、runtime、
controller、process、tests或Git6。Planner独立核对：

- HEAD subject为`chore(plan): activate p7 synthetic evidence supersession`，changed paths
  exact为FULL、PLAN与上一轮review archive；worktree clean。
- `.agent-work/EXECUTION_RESULT.md`仍为`1140609` bytes，SHA-256
  `85072a33ae2cf9d9074f70ec93263ce36e8ff9a25bf14ba1e1a290088cd2409f`，
  Executer append为`0`。
- E1失败前通过machine/activation/FULL/clean、冻结ER prefix、source identity、root
  exact9/canonical、sidecars、ordered matrix `16/16`、terminal/admission与success label。
- 唯一failure发生于临时audit Python line 129：错误要求exact9 root artifacts重复携带
  process `exit_code`或`returncode=0`。因此after-identity、Git topology、EOF delta与single
  supersession append均未执行。
- Planner直接读取旧ER冻结record，确认`runtime_report.process.exit_code=0`，并确认
  stdout/stderr bytes与SHA-256均在同一process owner中；exact9 root artifacts没有这些
  process字段。active PLAN第2节第6项明确要求从已有process report复核这些事实，没有
  要求root重复持有。
- Source、root、旧ER prefix、candidate、代码、测试、FULL、PLAN archive以外文件均未被
  Executer修改；retry、rerun、external/device/retained/release routes均为`0`。

## Findings and decision

`REV-E1-001`：Executer transient audit owner mapping错误。Process exit/stdout/stderr的
唯一数据owner是旧ER的`runtime_report.process`；root exact9只负责PLAN冻结的durable
artifact identities、canonical payload、sidecar、matrix、terminal与admission事实。将
process字段强制投影到root既非PLAN要求，也会制造平行evidence owner。

因此E1不接受，且不能称为已完成supersession；但该failure不否定immutable source/root、
P7 candidate或此前provisionally proven integration semantics。旧E1 terminal没有ER记录可
修改或补写，后续只能建立新的stable validation successor。

## Residual risk and exact next branch

唯一next branch是`REF-P7-25-R2-B2-P7-I1-E1-C1`：修正临时audit的数据owner mapping，
执行一次新的bounded read-only audit。该调用是E1-C1 stable successor的唯一audit，明确
不是原E1 retry；原E1 retry仍为`0`。不得放宽source/root identity、hash、canonical、
sidecar、matrix、terminal/admission、lifecycle、Git topology或ER prefix/EOF delta检查。

只有全部audit通过后，才允许一次single EOF append，把旧terminal record的两个snapshot
计数字段用窄范围supersession纠正为historical actual values。若任何pre-append gate失败，
ER writes必须为`0`。Retained R3、validator、eligibility、release、网络、设备、相机、Ray、
strip、FORMAL、TD-C、sentinel与P8继续hard locked。

维护性判断：纠偏仅改变一次性validation脚本的事实owner mapping，不新增生产owner、
parser、controller或证据格式，也不修改任何immutable evidence。
