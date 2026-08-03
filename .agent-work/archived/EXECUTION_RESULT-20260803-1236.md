# Archive metadata

- archive_status: `HISTORICAL_NON_EXECUTABLE_REVIEWED_REJECTED_TEST_OVERREACH_PRODUCTION_CANDIDATE_ACCEPTED`
- archived_at: `2026-08-03T12:36:32-06:00`
- source_owner: `Executer`
- source_type: `EXECUTION_RESULT`
- reviewed_scope: `REF-G4-02-PREDEVICE / first durable offline oracle execution`
- source_checkpoint: `79b8f03e65107e1d62f8de3b33ffb31d3413e185`
- original_body_bytes: `5516`
- original_body_sha256: `04e1278aea64ab75202484116687e2e11fa1b6d0d921a263fd3440172987adc2`
- terminal_disposition: `REJECTED_ONLY_TEST_OVERREACH_ACCEPTED_PRODUCTION_CANDIDATE_WAITING_ZERO_EDIT_VALIDATION_CONTINUATION`
- reviewed_plan_pointer: `.agent-work/archived/PLAN-20260803-1236.md`
- exact_next_stop: `SAME_REF_G4_02_ZERO_EDIT_FULL_VALIDATION_THEN_ORIGINAL_SINGLE_DURABLE_PACKAGE`
- historical_non_executable: `true`

该archive不授权execution、durable root、release consumption、device、formal、retry、stage entry、budget或commit。下方逐字节
保留reviewed ER body。

---

# REF-G4-02-PREDEVICE：durable offline oracle首次执行结果

**状态：** `STOPPED_AFTER_FIRST_TARGETED_TEST_OVERREACH_RETURN_FOR_PLANNER_REVIEW`

**PLAN contract：** `G4-PREDEVICE-DURABLE-OFFLINE-ORACLE-V1`

**Reference task：** `REF-G4-02-PREDEVICE`

**Planner stop：** `RETURN_FOR_G4_02_DURABLE_OFFLINE_ORACLE_REVIEW`

## 1. Activation与intake

- branch：`main`
- activation HEAD：`79b8f03e65107e1d62f8de3b33ffb31d3413e185`
- direct parent：`125158a3c1b8fa36a3a377290d90ebd53e46ec8a`
- subject：`docs(plan): activate g4 durable predevice oracle`
- activation changed paths：PLAN冻结的exact 5 paths；intake worktree clean。
- PLAN/FULL repo-owned parser：contract exact `G4-PREDEVICE-DURABLE-OFFLINE-ORACLE-V1`，active count `1/1`，task
  exact `REF-G4-02-PREDEVICE`。
- 1217 PLAN/ER archive bytes/SHA与source-body bytes/SHA均exact。
- accepted owner/test identities：12066 /
  `0d6c529934b59a2faedf802bdd1e872a8c18085d055c4bfb1604e49032885be1`；19429 /
  `eb90e55026a1c4bd927c80ab80f198346eb23ac97122eb52dabf914f99c1c509`。
- frozen durable root仅以`lexists`检查，intake与stop时均为`false`；未读取payload。

首个checker曾错误地自行扩展Human/Orchestrator提供的短SHA `79b8f03`，实际full SHA及其parent/subject/path set均正确；归类为
只读checker假设错误，不是repository drift。

## 2. Maintainability preflight与candidate

CodeGraph确认provenance已完整提供exclusive 0700 root、exclusive canonical 0600 persist、file/root fsync、reload、existing root、
inventory、exact read与same-target；无API缺口。

本candidate在accepted module内新增有限public surface：

- `EVIDENCE_ARTIFACT_NAMES`
- frozen `PredeviceEvidencePackage`
- `persist_successor_predevice_evidence`
- `replay_successor_predevice_evidence`

并给既有`SuccessorPredeviceError`增加`primary/seal_failure`字段。Owner边界：predevice只拥有result/seal closed schema、
evaluate→persist lifecycle及independent replay orchestration；provenance仍独占mkdir/open/write/canonical bytes/fsync/reload/read/
inventory/same-target；successor仍独占bundle/public/final/strict；thermal仍独占policy/R6/machine semantics。

维护性复核前production增量为+403/-1；删除重复的source/R6/operational/locks值级validation后收敛为+316/-1。源码未引入
`json/hashlib/os/subprocess`或direct open/mkdir/write、CLI、第二module/controller。正式targeted前的`py_compile`与局部
`git diff --check`通过。

当前post-stop identities：

| path | bytes | SHA-256 |
| --- | ---: | --- |
| `src/camera_based_rgbww_optimizer/optimization/p7_successor_predevice.py` | 24232 | `4c8bf96dca444b5412120534a1df5519976afc98fe4aa1aaf2b83596177ffc81` |
| `tests/test_p7_successor_predevice.py` | 29738 | `44ac81ae18ae0a8f041d53837c4c7d6c4e867cf4761c616bfb640117550d4cfa` |

## 3. Fresh targeted结果与精确失败

执行：

```text
.venv/bin/python -m unittest tests.test_p7_successor_predevice -v
```

结果：`Ran 18 tests`，17 PASS / 1 FAIL，exit 1。唯一失败：

```text
test_root_and_return_identity_drift_fail_closed_after_creation
AssertionError: SuccessorPredeviceError not raised
```

失败发生在该测试的额外第二子例：注入的`persist_fn`先完整调用可信provenance owner，随后只伪造其returned
`FileIdentity.inode + 1`，同时保留root/path/mode/data/bytes/SHA。Production seam按
`persist_canonical_json`可信返回合同未再次stat，因此未raise。

分类：`FIRST_TARGETED_TEST_OVERREACH_TRUSTED_PROVENANCE_OWNER_RETURN_FABRICATION`。

- PLAN要求的physical root identity drift第一子例已PASS；
- evaluator-before-root、pre-existing root、result persist failure、terminal failure/failure seal、double failure、success+replay、
  inventory/hash/canonical/root/target replay drift均PASS；
- 不是real root、filesystem、source/science、successor或thermal失败；
- 不是provenance API缺口；
- 该额外returned-owner-lie子例不属于PLAN要求，最小收敛是不修改production并删除该overreach。

在Orchestrator stop消息到达前，Executer已删除上述额外第二子例并把test重命名为只描述physical root identity drift；删除后
**未重跑任何测试**。因此当前candidate不得宣称targeted green。未运行focused/full/compileall/CodeGraph sync/final explore。

## 4. Stop与zero ledger

Orchestrator明确要求不继续测试或root，并将本结果交回Planner。最终`git diff --check`通过；repo dirty set exact为PLAN允许的三个
Executer paths：production module、test和本ER。PLAN/FULL/archives保持未修改。

```text
durable root creation = 0
evaluate_successor_predevice real invocation = 0
real G4-01 bundle access = 0
independent package replay real invocation = 0
release consumption = 0
retained R3 / R2 / other external payload access = 0 / 0 / 0
device/network/camera/Ray/strip/capture/formal/TD-C = 0
firmware/deployment = 0
PLAN/FULL/archive/GUIDE/RESEARCH edits by Executer = 0
commit/amend/stage/push = 0
Terminal/background/automation = 0
```

Effective canonical validator success、eligibility、release consumable、release consumption authorization及全部device/formal
authority仍为`false`；retained R3仍为`RETAINED_UNVALIDATED_UNCONSUMED`；G4-03仍locked。

请求Planner在唯一stop `RETURN_FOR_G4_02_DURABLE_OFFLINE_ORACLE_REVIEW`审查candidate、首次targeted结果与已删除但未重跑的
overreach子例。不得创建real root或激活G4-03。
