# REF-G4-04-E2 fresh-root/source-binding engineering handoff

**状态：** `SOURCE_CHECKPOINT_TREE_BINDING_INCOMPLETE_WAITING_SAME_PACKAGE_EXECUTION`

**Reference task：** `REF-G4-04-E2`

**Contract：** `G4-E2-FRESH-ROOT-BINDING-ENABLING-V1`

**唯一 Planner stop：** `RETURN_FOR_G4_04_E2_FRESH_ROOT_BINDING_ENGINEERING_REVIEW`

## 0. Planner scope-gap review / contract alignment

Planner在terminal acceptance前独立发现：当前候选只把`output_root`改为run-specific explicit seam，`frozen_e2_input`仍硬编码旧G4-03
`source_checkpoint=4995f7d65141ce8a4086d74f9add21c5b44d593d`与
`source_tree=da458ce4a81344397354a8535e8a38cef5d59375`。这会使未来Package B无法把Package A accepted exact clean HEAD/tree
显式冻结为fresh E2 source owner。

Disposition为`SOURCE_CHECKPOINT_TREE_BINDING_INCOMPLETE`。这是Human刚明确的Package A合同相对原PLAN的scope gap，不是production owner failure，
不把此前root实现或912项验证改写为失败，也不消耗新的bounded correction。原唯一fixture/harness correction仍是已用`1/1`；本轮不新增
task、corrective suffix、PLAN类型或实验root，不接受当前候选、不归档。

Orchestrator必须以当前HEAD `32ba4319925b95887dbb79b352166989c5d906cf`为parent、subject
`docs(plan): align e2 source binding`、exact PLAN/ER/FULL三路径形成same-package alignment commit，并保持PLAN/FULL active `1/1`同一task后，
Executer才可继续同一Package A：把production factory收敛为exact三个keyword-only/no-default
`output_root/source_checkpoint/source_tree`，pure验证source pair为exact lowercase 40-hex，由未来Package B显式传入Package A accepted HEAD/tree。
不得通过global、env、Git read、monkeypatch或controller解决，也不得在Package A source中自引用未来commit/tree。

## 1. Activation intake

- branch：`main`；activation HEAD：`32ba4319925b95887dbb79b352166989c5d906cf`；direct parent：
  `ce4eaab9e06bdb1c6092b2ab104b7f2931a7fb44`；activation tree：
  `18ead014e76e8d44a32d42b0c91ea839a7c25bf6`。
- activation subject为`docs(plan): activate e2 fresh root binding`，changed paths exact为
  `.agent-work/EXECUTION_RESULT.md`、`.agent-work/FULL_PLAN_REFERENCE.md`、`.agent-work/PLAN.md`。
- parent tree exact为`e1682006013ec148435a16515cb3688823bfd3f8`；activation后worktree clean。
- GUIDE `advisor/4/4.GUIDE.md`：22702 bytes，SHA-256
  `659152f6c0ae69c90c701de4e57c352d771e4f0bf75cf9410271ba0a94200e35`。
- repo-owned PLAN/FULL strict parser在执行前PASS：active count `1/1`，task均为`REF-G4-04-E2`，canonical next同一task；retained
  R3为`RETAINED_UNVALIDATED_UNCONSUMED`，release consumption/device/formal/TD-C/G4-05/G4-06 authority均false/0。
- 已拒fixed E2 root未被读取、stat、遍历或创建；未预加载任何external payload。

## 2. Initial root-binding implementation evidence（pre-alignment）

只修改既有E2 owner与既有test file：

1. `frozen_e2_input(*, output_root: str)`现在exact一个keyword-only、无default参数；内部唯一
   `_validate_output_root`对exact `str`、TEMP_PARENT direct child、canonical lexical path、lowercase 12-hex basename和strict
   UTC timestamp parse/round-trip进行pure lexical validation。旧rejected root不再是source default或production selection。
2. `_validate_exact_input`先验证root，再以同一root构造frozen expected；其余GUIDE/policy/prerequisite/transport/authority/protected-source
   exact equality保持不变。
3. closed `reference_ledger`新增exact `output_root`；evaluate、persist shared validation和replay因而绑定同一root。
4. persist仍保持accepted public signature与canonical replay direct call；semantic validation继续先于I/O；create seam返回值必须是exact
   `DirectoryIdentity`且path等于inputs root，否则在result persist前以`created_root_identity_mismatch`拒绝。
5. replay先通过repo provenance owner绑定actual root，再以`frozen_e2_input(output_root=root.path)`建立expected并调用原shared result validator；
   cross-root artifact transplant即使重建terminal file identity仍因ledger root不一致而fail closed。
6. 测试fixture不再使用E2 nested `TemporaryDirectory`或patch runtime root constant。`OwnedE2Roots`每case/并发最多2个预先不存在的合法direct
   child，记录provenance `DirectoryIdentity`；finally再次验证exact path、identity、历史root排除和allowlisted regular inventory，只逐个
   `unlink` exact child并`rmdir` exact root。无glob、rmtree、prefix scan或parent cleanup；正常case residual均为0。

Source identity：

| Path | Activation bytes / SHA-256 | Worktree bytes / SHA-256 |
|---|---|---|
| `src/camera_based_rgbww_optimizer/optimization/p7_successor_e2.py` | 25075 / `c986255dc341b9ffdc54efff5e1cbb1d2c05b9fdd141fb0e660ad20c8c771bbf` | 26591 / `9ac77f4e7a88f07b65fbb716ed7e067e2c15bdda17cca84799e6385cc1764dfe` |
| `tests/test_p7_successor_e2.py` | 32097 / `5b3f250dbbfab1914b3faaebabd32ac1b0c74dc3ea5c399cdaa4a553aabdcb32` | 44324 / `4e111177d2352be0ccc5f272fbdcda393c67e63af58908f88b33f47048f6b5e0` |

## 3. Initial root-binding negative and behavior coverage（pre-alignment）

- signature exact一个kw-only/no-default `output_root`；no-arg/positional均`TypeError`；不存在production global root default/selection patch。
- accepted lowercase 12-hex + strict UTC root construction在provenance create/read/inventory调用均0时通过。
- invalid exact type覆盖`Path`、bytes、str subclass；invalid lexical覆盖empty/relative/wrong parent/extra child/double slash/trailing
  slash/`.`/`..`/backslash/control、uppercase/wrong-length hex、wrong timestamp case、invalid calendar/hour/second；create/persist/read均0。
- valid root可独立变化，其余frozen field漂移仍拒绝；ledger root missing/extra/tamper均拒绝。
- input/result ledger root mismatch在create/persist前拒绝且I/O `0/0`；create seam返回另一个合法root identity时result persist为0。
- 两个test-owned legal roots完成cross-root transplant negative：A的canonical result复制到B并用B result identity重建terminal，replay B仍因ledger A拒绝。
- accepted ephemeral package保持canonical bytes、0700/0600 modes、exact two-artifact inventory、success terminal、canonical direct replay与deep
  immutable result；context退出后exact root不存在。
- 既有closed result/terminal tamper、persist failure seal、inventory drift、canonical thermal owner、forged evaluator、removed semantic keyword
  I/O=0与public signature测试全部保留。
- AST测试证明root validator无filesystem method；owner无device/network/process/environment boundary；fixture无wide cleanup primitive。

## 4. Failure convergence

Targeted首次运行共32个test methods：31个通过，`test_terminal_shape_authority_and_result_identity_are_closed`的22个subcase失败。
根因是旧handcrafted fixture的result仍绑定`self.inputs` root，而新replay按actual owned root正确先报`result_contract_drift`，未到terminal tamper
断言。这是同一test fixture/harness transcription seam，不是production semantic boundary失败。

已使用唯一一次bounded correction：只调整existing tests，使handcrafted result从其实际owned root的explicit input生成；production source未因该失败
修改。第二次targeted 32/32 PASS；correction预算已用尽，没有第二个同类失败或retry。

## 5. Validation ledger

| Gate | Invocation | Result |
|---|---:|---|
| CodeGraph preflight | 1 | PASS；确认现有shared result validator、thermal/provenance owner与persist/replay seams |
| targeted first | 1/2 | 32 methods；31 pass，1 method的22 subcases为同一fixture root-binding mismatch |
| targeted second | 2/2 | `32/32 PASS` in 0.426s |
| focused lineage/predevice/zero-readiness/E2/thermal/analyze/provenance | 1/1 | `232/232 PASS` in 51.126s |
| full `unittest discover -s tests` | 1/1 | `912/912 PASS` in 163.126s |
| pre-target exact-two-file `py_compile` syntax smoke | 1 | PASS；在首次targeted前执行，非第二次test retry |
| formal `compileall -q src tests` + all `tmp/*.zsh` syntax | 1/1 | PASS |
| repo-owned baseline-aware source scan | 1/1 | PASS；activation→worktree exact 2 paths；findings/private/env/network/symlink/unsafe path均0 |
| `git diff --check` | 1 | PASS |
| dirty/protected path invariant before ER | 1 | PASS；dirty exact source/test；GUIDE/RESEARCH、PLAN/FULL、archives、config、wrappers、3个巨型P7 owner均未变 |
| `codegraph sync` | 1/1 | PASS；index already up to date |
| CodeGraph focused ownership queries | 2 | PASS；pure validator→exact input→ledger→persist/replay edges可见，canonical thermal/provenance owners未被平行controller替代 |

注：formal compile/static gate本身只运行1次；在其前另有一次exact-two-file `py_compile`开发期syntax smoke，已在本ledger单独、如实列出，留给
Planner按execution budget作最终判断。

## 6. Safety and authority ledger

- production evaluator/persist/replay：`0/0/0`；durable E2 root/package：`0/0`；测试仅使用context-owned ephemeral roots，最多2个并发，正常
  finally residual `0`。
- rejected fixed E2 root、G4-01 release root、G4-02 predevice root、G4-03 readiness root、retained R3、legacy/deep-corrective/external payload
  access全部`0`。
- device/network/app/process/listener/camera/Ray/strip/capture/nonzero light/release consumption/formal R6/formal root/TD-C/firmware/deployment全部
  `0`。
- 未修改PLAN/FULL/archive/GUIDE/RESEARCH/config/wrapper/巨型P7 owners；未stage、commit、push或创建PR；未创建goal/task/corrective suffix。
- 本包不表示fresh E2已经生成或接受，不表示hardware ready/formal pass，不解锁G4-05 planning/execution或G4-06。

## 7. Initial maintainability record and revised Planner decision request

维护性判断：fresh-root shape、frozen input、ledger与replay expected-input仍集中在单一E2 owner；I/O继续委托accepted provenance owner，formal/machine
truth继续委托accepted thermal owner。没有新增module/controller/helper service，也没有触及巨型P7模块；新增复杂度主要在严格test-owned cleanup
fixture和negative coverage，不建议本包内再做重构。

当前handoff不再请求terminal acceptance。Executer须等Orchestrator完成same-package contract-alignment commit后，按修订PLAN继续
source checkpoint/tree binding与新增验证，并把alignment diff/validation追加到本ER。唯一Planner stop仍为
`RETURN_FOR_G4_04_E2_FRESH_ROOT_BINDING_ENGINEERING_REVIEW`；不得由本handoff生成fresh durable package或后续PLAN。
