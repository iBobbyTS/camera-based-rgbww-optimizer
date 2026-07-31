# REF-P7-25-R2-B2-P4-V1 final-source validation review

**Planner 日期：** `2026-07-31`

**Reviewed contract：**
`P7-TD-B-RETAINED-R3-OPTION-B-B2-P4-V1-FINAL-SOURCE-FULL-VALIDATION-V1`

**Decision：** `ACCEPTED_COMPLETE`

**Exact next branch：** `REF-P7-25-R2-B2-P4-I1`，仅把已接受的repo-owned
conformance/composition owner用于一次fresh synthetic external integration qualification；通过前不解锁
retained R3、real B2、manifest、canonical validator、eligibility、release、network或device。

## 1. Frozen topology and file identity

- Implementation commit：`83bb193259fcf1de5b3f78798001e83496c2daae`，direct parent
  `5f2483c319b395b2aef2a43f4827b4c150f3f3fd`，subject exact
  `feat(p7): add retained controller conformance owner`，changed paths exact为：
  `src/camera_based_rgbww_optimizer/utils/p7_retained_r3_controller_conformance.py`与
  `tests/test_p7_retained_r3_controller_conformance.py`。
- Implementation source/test blob OID exact为
  `52fcdc73c69e367cd1b046b52d83ffc555a6d496` / `28a58c6051de378fbcc6485c316df9ff10d3a90c`；
  SHA-256 exact为
  `94a0992d662005df177b422d83fc1cefdd2cf7d43472571a27061df2bc7efeb7` /
  `447bf13cb61e5b34ef6637e926a499e63b5b3393aa29e0d5fca205a96d180726`。
- Initial implementation evidence commit：`de50071cd21a2459a9f68aca5e4357fe7d86abae`，是implementation
  direct child且只修改`.agent-work/EXECUTION_RESULT.md`。
- P4-V1 activation commit：`1e733ff58139e89dadf8bfa2b1068b050557e61e`，direct parent
  `de50071cd21a2459a9f68aca5e4357fe7d86abae`，subject exact
  `chore(plan): activate p4 final-source full validation`，changed paths exact为FULL、PLAN及
  `20260731-1126` review archive。
- P4-V1 validation evidence commit/current reviewed HEAD：
  `c89b2914af44eb3d10f4dc8b347340d86abc5756`，direct parent为activation commit，subject exact
  `chore(evidence): record p4 final-source full validation`，只修改
  `.agent-work/EXECUTION_RESULT.md`。
- Current source/test仍为上述exact blobs与SHA；dedicated test surface仍为exact `14`个
  `test_` methods。

## 2. Validation evidence reviewed

Executer保留了唯一full invocation的同一unified session `86444`，没有丢失session后重跑：

```text
PYTHONUNBUFFERED=1 .venv/bin/python -m unittest discover -s tests -p 'test_*.py'
processes = 1
exit = 0
Ran 755 tests in 169.249s
OK
failures = 0
errors = 0
skips = 0
```

Targeted、focused、count probe、compileall、CodeGraph、retry、fallback与第二full invocation均为
`0`。初始及full后/ER append前porcelain为空，`git diff --check`通过；validation本身没有修改
source、test、PLAN、FULL、archive、debug、GUIDE或RESEARCH。ER是唯一handoff写入，并已由exact
one-path evidence commit封存。

External controller/process/write、evidence/qualification root、旧controller/root/evidence读取、
retained artifact reads、Git provenance replay、real B2、subordinate manifest、canonical validator、
eligibility、retained audit、全部release操作及network/device/scientific预算均为 `0`。Retained R3
保持 `RETAINED_UNVALIDATED_UNCONSUMED`。

## 3. Findings and lifecycle conformance meaning

### REV-B2-P4-V1-001 — final-source full acceptance evidence complete

Severity：closure record；code finding：否。

Activation、implementation、initial evidence与validation evidence topology均为direct-child且exact
path集合无漂移。Final committed source/test identity未改变；唯一full process给出可观察exit `0`、
exact `755` discovery count、`OK`及failures/errors/skips全零。因此P4先前唯一acceptance blocker
`REV-B2-P4-001`关闭，P4-V1可验收为`ACCEPTED_COMPLETE`。

### REV-B2-P4-V1-002 — lifecycle conformance is a pre-effect gate

Severity：semantic closure；code finding：否。

`conformance`不是sealed primary phase，而是所有effect callbacks之前的fail-closed gate。它失败时
原异常直接重新抛出，`activation/root/inputs/evaluate/terminal/terminal_seal/admission` attempts均为
`0`。这不是“失败证据缺失”，而是防止未通过runtime/controller conformance的source产生任何
external effect或伪造terminal evidence。

只有conformance成功后，`activation`、`root`、`inputs`、`evaluate`才构成sealed primary phases。
其中任一失败后terminal attempt exact `1`；terminal成功后seal attempt exact `1`；seal成功后
admission attempt exact `1`；完成有效FAIL admission后仍重新抛出原primary exception identity。
Terminal失败或seal失败均阻止admission。Success顺序exact为
`conformance, activation, root, inputs, evaluate, terminal, terminal_seal, admission`；retry/fallback
始终为`0`。Source lines 366–416与dedicated tests 10–13共同冻结这一区分。

## 4. Maintainability and next integration boundary

Second-pass架构修复现已闭环：单一pure-in-memory owner集中管理owner schema、runtime AST、root
identity chain与lifecycle composition；provenance I/O、preparation/seal、manifest、canonical validator、
release及science边界保持分离。Exact 14 dedicated methods和final full `755/755`提供了充分回归保护，
不需要继续修改这两个implementation paths。

但repo owner尚未在fresh external controller/evidence root中做过integration qualification。因此下一包
只能使用accepted owner运行一次synthetic、无retained输入的fresh qualification：runtime source与
negative fixtures必须分域；live root identity必须传给所有synthetic direct-child reads；lifecycle必须
通过injected callbacks形成PASS terminal/seal/admission。该包只是integration qualification，不得解释为
real B2或retained-R3 audit。

## 5. Acceptance decision, residual locks and proposed FULL transition

Decision：`ACCEPTED_COMPLETE`。

- `REF-P7-25-R2-B2-P4` → `ACCEPTED_COMPLETE_VIA_P4_V1`。
- `REF-P7-25-R2-B2-P4-V1` → `ACCEPTED_COMPLETE`。
- 新增 `REF-P7-25-R2-B2-P4-I1` → `READY_FOR_ORCHESTRATOR_ACTIVATION`。
- `repair_v2_status` → `P4_OWNER_ACCEPTED_FRESH_SYNTHETIC_INTEGRATION_PENDING`。
- `retained_r3_status`保持 `RETAINED_UNVALIDATED_UNCONSUMED`。
- real B2 retry、retained reads、subordinate manifest、canonical validator、eligibility、release、network、
  device、FORMAL与later stages全部继续hard locked。

Planner只修改本archive与active PLAN；FULL、ER、debug、GUIDE、RESEARCH保持只读。Orchestrator须独立
审核、更新FULL并创建exact activation commit后，才可dispatch下一Executer。

维护性判断：P4 owner的职责边界和final full coverage已验收；下一包只做一次bounded integration，
不新增repo abstraction，也不扩大validator、release、science或device authority。
