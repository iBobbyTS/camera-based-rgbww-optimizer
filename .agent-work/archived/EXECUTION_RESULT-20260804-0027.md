# Archive record

- Archive status: `REVIEWED_ACCEPTED_HISTORICAL_NON_EXECUTABLE`
- Timestamp: `2026-08-04T00:27:54-0600`
- Source owner/type: Executer / `EXECUTION_RESULT`
- Reviewed scope: `REF-G4-06-RAY-R6` package preparation route bounded-correction handoff and immutable-child phase-2 review
- Source checkpoint at review: `ebc40bf8e40c4bb59bd070367a321a2e76c3ce5c`
- Source bytes: `8301`
- Source SHA-256: `8a3665b8be44f03644b8c3e345ee78d34afcec32e4966dec284063df427945b2`
- Terminal disposition: `ACCEPTED_G4_06_PACKAGE_PREPARATION_ROUTE_ENGINEERING`
- Reviewed PLAN pointer: `.agent-work/archived/PLAN-20260804-0027.md`
- First rejected candidate evidence: wrong-but-valid source parent prepare succeeded under the first candidate; its `961/961` suite did not close the missing source binding and grants no acceptance.
- Bounded correction evidence: exact PLAN/FULL source binding mirror, CLI parent args, accepted code owner/tree, subject/two paths, live ancestor and committed/current blobs validated before root creation; wrong-valid parent/code owner/tree and mirror drift are pre-root failures.
- Accepted validation: final candidate stage `406ac5c82ac9a098052a812af866f29083bdb2ee3fd5962964c8889100ef5d37`, tests `ff3964db91ba2bd19073be16eb4a45aa7ae81a96c2ff17cb54b108f4cf2915c3`; targeted `13/13`, stage-gate `46/46`, focused `251/251`, fresh full `963/963`, Planner representative `8/8`, independent prior-finding probe PASS.
- Exact next stop: Orchestrator must update FULL before any real fresh-package evidence PLAN; formal/device execution remains locked.
- Residual risk: synthetic/offline engineering evidence only; real package identity, root, formal acquisition, quality/history and G4-07 remain absent.
- Historical declaration: `historical_non_executable`; this archive authorizes no execution, device, release, retry, stage entry, budget, or commit.

## Archived source body

# REF-G4-06-RAY-R6 package preparation bounded-correction handoff

**Status:** `READY_FOR_ORCHESTRATOR_CONTROLLED_PACKAGE_PREPARATION_ROUTE_CODE_CHILD`

**Planner stop:** `RETURN_FOR_G4_06_PACKAGE_PREPARATION_ROUTE_TWO_PHASE_REVIEW`

本 handoff 取代被 Planner phase-1 拒绝的第一 candidate。它只证明当前 G4-06 fresh-package preparation route 在 synthetic/offline repository 中绑定 accepted A→C→L source topology；不生成、describe或读取真实 package/external root，不消费 release/retained R3，不授权 formal/device/camera/Ray/strip/capture/G4-07。

## 1. Activation 与不变边界

- branch：`main`
- activation HEAD：`310f547c91420c34f67d1d241ad4aedaa3bc9c2c`
- activation direct parent：`16b982c29e6f8bcc49d7a11e87b30eacf237f825`
- activation tree：`e5184c3236ba053909332fff032691c1aad167d0`
- activation subject：`docs(plan): activate ray r6 package preparation route engineering`
- activation paths exact：`.agent-work/FULL_PLAN_REFERENCE.md`、`.agent-work/PLAN.md`
- PLAN SHA-256 unchanged：`c0bf01d0fb2d45254b0b8a4e2741ee8d9bb60b9976521b9e3faa3677ab3361a0`
- FULL SHA-256 unchanged：`2b78acc9e6ca979c56bf3dba2330779327b7747e7bc67a67cc0fe23c44afdd2b`
- live strict machine：active `1/1`、current-plan `1`、task/current/canonical next均为`REF-G4-06-RAY-R6`、engineering contract为`G4-RAY-R6-PACKAGE-PREPARATION-ROUTE-ENGINEERING-V1`；PLAN executable true，FULL non-executable，顶层device/formal/release/TD-C authority全false。

## 2. Planner phase-1 rejection / failure 1

第一 candidate虽通过其synthetic tests及`961/961` full，但 Planner 独立验收构造了另一组Git中存在且内部自洽的`--source-parent-checkpoint/tree`。旧CLI只验证该commit/tree存在且匹配，未把args绑定到future evidence PLAN/FULL与accepted code owner，因此错误prepare成功；later source attestation才返回`committed_source_parent_drift`。

分类：`PRODUCTION_SOURCE_ATTESTATION_BINDING_MISSING_BEFORE_EXCLUSIVE_ROOT`。

该`961/961`只属于被拒candidate，不作为本 correction 的full证据。没有生成新PLAN/task/root/suffix；本次是同一PLAN允许的第一次且唯一 bounded production correction。

## 3. Bounded production correction

现有stage-gate owner新增closed schema：

`p7_td_b_r6_preparation_source_attestation_binding_v1`

Exact keys：

- `schema`
- `verified_parent_checkpoint`
- `verified_parent_tree`
- `accepted_code_owner_checkpoint`
- `accepted_code_owner_tree`
- `code_child_subject`
- `code_child_paths`

Future evidence PLAN必须持有该binding；FULL `g4_06_state.source_attestation_binding`必须exact mirror。Missing/extra/schema/identity/subject/path或PLAN/FULL mirror drift均fail closed。

`build_stage_gate_input`现在在evaluate、persist和exclusive root creation之前：

1. exact解析PLAN/FULL binding；
2. 要求CLI/source args checkpoint/tree exact等于binding verified parent；
3. 将accepted code owner、live HEAD/tree和candidate references交给existing `validate_committed_source_attestation`；
4. 复用其direct non-merge parent、exact subject、exact two paths、tree、committed blob bytes/SHA/mode、current bytes、HEAD ancestor、linear `.agent-work/` descendants与worktree scope验证；
5. 将同一binding投影到StageGateInput、stage-gate、launch descriptor、persistence input binding及replay validation。

没有复制Git topology/blob/current-byte语义，没有新增第二个attestation/serializer/controller owner。CodeGraph确认`measure_p7_thermal_diagnostics.py`未取得preparation或attestation ownership。

Later `validate_committed_source_attestation`还要求probe code owner checkpoint/tree exact等于descriptor binding；合法但不同的probe不能推迟到parent/path检查后才失败。

## 4. Pre-root evidence

Current G4-06 real module `prepare`/`describe` synthetic positive继续PASS；prepare owner counts：

- `build_stage_gate_input=1`
- `evaluate_stage_gate=1`
- `persist_stage_gate_package=1`
- `create_exclusive_root=1`
- public replay=`1`
- terminal internal replay=`true`

新增source binding/topology matrix `11` cases全部pre-root fail：

- wrong-but-valid source parent checkpoint/tree pair；
- verified parent被错误当作code owner；
- wrong-but-valid accepted code-owner checkpoint；
- accepted code-owner tree drift；
- PLAN binding missing/extra/subject/path drift；
- FULL binding missing/extra/mirror drift。

每项root不存在，evaluate/persist/replay/root-create=`0`。Later attestation probe checkpoint/tree与descriptor binding不一致均返回`committed_source_binding_drift`。

既有preparation machine matrix `24` cases、old G4-05、old subject、three-path child、wrong parent/merge、transient history、package substitution/stale identity、sealed replay、Package-A negative、Package-B formal pre-backend comparison、runtime hash、generic bypass和delegate no-retry回归均继续通过。

## 5. Failure convergence record

- substantive production failure：`1`（Planner发现的pre-root source binding缺口）
- bounded production correction：`1/1`，已完成
- 第二个production failure：`0`
- 第三次同边界失败：`0`
- 第一candidate中已记录的单次call-count harness correction没有改变production owner。
- correction实现后的测试红灯均为一次性fixture migration：动态真实A→C→L替换伪SHA后，旧断言未计orchestration L；deep mutation tests未同步descriptor binding而正确更早被新gate拒绝；alternate handwritten fixture漏新binding。分组机械更新后stage module完整通过；没有放宽production contract。
- 未创建corrective task/suffix、parallel adapter/controller、额外root或第四次retry。

## 6. Validation

- final targeted：`13/13` PASS，`126.277s`
- full stage-gate module：`46/46` PASS，`196.527s`
- focused五模块：`251/251` PASS，`240.775s`
  - `tests.test_p7_td_b_r6_stage_gate`
  - `tests.test_p7_td_b_r6_contract`
  - `tests.test_p7_thermal_diagnostics`
  - `tests.test_agent_work_machine_contract`
  - `tests.test_p7_successor_e2`
- `.venv/bin/python -m compileall -q src tests`：PASS
- `zsh -n tmp/run-p7-thermal-diagnostics.zsh`：PASS
- repo-owned PLAN/FULL strict parser：PASS
- `codegraph sync`：PASS；post-query确认single existing attestation owner、无measure/parallel owner
- `git diff --check`：PASS
- protected diff：empty
- staged/cached：empty
- semantic freeze后的correction唯一fresh full：`.venv/bin/python -m unittest discover -s tests` → `963/963` PASS，`404.540s`，exit `0`
- full后source/test bytes未修改，未重复full。

## 7. Frozen candidate identities

相对activation HEAD的最终two-file candidate：`+734/-112`。

- stage-gate：`93155` bytes，mode `0644`，SHA-256 `406ac5c82ac9a098052a812af866f29083bdb2ee3fd5962964c8889100ef5d37`
- focused tests：`130254` bytes，mode `0644`，SHA-256 `ff3964db91ba2bd19073be16eb4a45aa7ae81a96c2ff17cb54b108f4cf2915c3`
- wrapper unchanged：`2730d43507af14a531453978477439bb29ef93ae7dea8e0bddb6c2330e1242e5`
- measure unchanged：`babca565fafa7492a3fdcc7a498dc7d2be129367fe40118e489b5f0f7e11b02f`
- ER为本handoff，不属于controlled code child。

最终dirty set应exact为ER、stage-gate、focused tests；PLAN/FULL/archives/measure/wrapper/config/docs/GUIDE/RESEARCH无diff，staged为空。

## 8. Side-effect counters 与 disposition request

- real package generate/describe/read=`0/0/0`
- external experiment root/payload=`0`
- formal root access/create=`0/0`
- retained R3/release consumption=`0/0`
- real backend/device/network/camera/Ray/strip/capture/nonzero light=`0`
- firmware/deployment/TD-C=`0/0/0`
- stage/commit/push/PR=`0/0/0/0`

请求Planner重新执行phase-1 review。若接受，请返回：

`READY_FOR_ORCHESTRATOR_CONTROLLED_PACKAGE_PREPARATION_ROUTE_CODE_CHILD`

由Orchestrator创建activation commit的唯一direct non-merge code child：

- subject exact：`fix(stage-gate): bind package preparation to g4-06`
- paths exact：
  - `src/camera_based_rgbww_optimizer/optimization/p7_td_b_r6_stage_gate.py`
  - `tests/test_p7_td_b_r6_stage_gate.py`
- ER不得进入code child。

随后同一PLAN进入phase-2 read-only review。真实fresh package/external root/formal/device execution仍未授权。
