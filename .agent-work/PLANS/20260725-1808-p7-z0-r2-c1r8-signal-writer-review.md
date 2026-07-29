# P7-TD-B Z0-R2-C1R8 signal unknown writer 验收归档

**归档时间：** 2026-07-25 18:08 MDT

**Reference task ID：** `REF-P7-01`

**Reviewed PLAN contract：** `P7-TD-B-Z0-R2-C1R8`

**Reviewed PLAN SHA-256：** `7a050a8e27f67097857ea40d2a505fbba6b82719dcdb3bda6efac7a0ea30f60b`

**Planner decision：** `accepted_dual_root_fifo27_signal_preflight20_seal3_fresh_cleanup_and_old_replay; rejected_assigned_signal_single_writer_ordering; c1r9_required`

**Exact next branch：** `P7-TD-B-Z0-R2-C1R9`；只修正 assigned-signal primary stage 的唯一 writer 与ordering：child捕获assigned signal后不得写stage result，parent controller在wrapper/child完整reap、result持续absent且eligibility exact后独占写derived unknown。watchdog的child-produced unknown result与signal controller-derived artifact必须保持不同path/schema/owner；双writer、任意late real result或unknown计success/zero全部拒绝。

## Reviewed scope 与方法

C1R8 fresh root：

`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-e2-r1-z0-r2-c1r8-offline/20260725T235321Z/`

Executor冻结C1R7 review/source/evidence，实施双冻结root historical FIFO policy与fresh negative FIFO exact cleanup，完成preflight后启动driver一次。Planner核对 EXECUTION_RESULT 第57节、validation/failure/zero-budget artifacts、双root policy、signal matrix、seal ledger、case `08-sigint` 全部stage/wrapper/signal evidence以及C1R8 harness对应signal/worker/controller代码；未运行old driver或访问设备。

## Evidence 与 accepted partial validation

- `historical-fifo-policy-matrix.json`：bytes `8792`，SHA-256 `1ba7b621a7a7548b4a780381567de9e31292944e67a958420c6e389ea47931c3`；dual-root exact policy `27/27`。
- `signal-unknown-accounting-matrix.json`：bytes `2861`，SHA-256 `eefc723e87f8b172645dfa6d5216d4e0bab3c801ce0221b30da676858c9b809c`；C1R7 synthetic eligibility负例 `20/20`。
- `seal-ast-delta-ledger.json`：bytes `1128`，SHA-256 `058e5d1dedc34b5c64d8134a81d7a9aa140bdd9d7ba2983702682b3b24bc2d2b`；typed raw delta `3/3`、unclassified `0`、broad normalization `0`。
- fresh negative FIFO先fail closed，随后exact cleanup `1`；cleanup before/after SHA-256分别为 `236d3bfe42809f72729e457194ea7876d4439e2afde4bb66232a7c1160aebd24`、`34453bec87397f04f7fed9fda8e3f0edad09bf7672f620a0ce08a051f92a357f`；historical FIFO unlink `0`。
- C1R3/C1R6 whole-tree before/current replay exact相等；两FIFO的path/type/mode/size/device/inode/nlink/provenance proof不变，content/mutation counters均 `0`。C1R7 root未加入old-root tuple。
- driver内前五 required matrices：evidence tree `6/6`、wrapper copy `10/10`、secrets identity `7/7`、source hygiene `10/10`、PLAN identity `14/14`，合计 `47/47`。
- `zero-budget-audit.json`：bytes `1805`，SHA-256 `1408ef23f96aca195aa8d41f26a2d6b993dd994ccfecc46235261a8a222512fe`。
- `validation-summary.json`：bytes `6838`，SHA-256 `d7cfec98379fa455180560d81e6f4cda56926de85dae44d15ec4c234b5ae26de`。
- `first-failure-audit.json`：bytes `8476`，SHA-256 `b39d1d9b04b91554fd034555fedca03ead92ce0c911bfeac8af2a8daa1082182`。
- C1R8 harness：bytes `113399`，SHA-256 `683e7b6b5f80c68c37a163b5b7a2c7438ff45bbde52a38e38ad9c1b1cd39432e`；wrapper、adapter、launcher保持C1R7 byte-exact。

package JSON `266/266` strict parse通过；fresh package/driver/rerun=`1/1/0`，owned residual process=`0`。driver stdout为空；stderr SHA-256 `efb9a0d03c2f105eb5ab8989c069bc524cb725820a5596058b9f5270dff52002`；launcher exact传播exit `1`。

## Finding 与根因

唯一首失败是 lifecycle `08-sigint`。signal dispatch时 primary result no-follow absent；child随后捕获assigned SIGINT、终止adapter worker并进入signal cleanup。C1R8 `run_stage`在重新抛出 `AssignedSignal` 之前仍无条件将一个child-produced stage result写到：

`cases/08-sigint/stages/001-primary-strip-zero-result.json`

该artifact bytes `592`、SHA-256 `a642d200336346451b151453cf8284fb2f4c5dcea42252bf8173557a2fe78493`，字段为 `kind=result`、`outcome=attempted_result_unknown`、`response=null`、`worker_exit=-15`、error `AssignedSignal/SIGINT`。它本身未声称success或zero；controller derived unknown没有写。

这不是reap后残留writer竞态：child result `ended_at=2026-07-26T00:04:15.104985Z`，wrapper exit记录时间为 `2026-07-26T00:04:15.427310Z`，所以result在signal之后、wrapper/child reap之前由child正常路径写出。错误文案 `late result after reap` 只表示controller在reap后的absence gate观察到它，不证明写入发生在reap后。

根因是C1R7 controller-only derived unknown合同与更早的 `run_stage` unconditional result writer并存。synthetic `20/20`没有执行实际 AssignedSignal child路径，因此未覆盖该集成边界。historical FIFO、fresh cleanup、seal、signal/trap/cleanup本身未失败；lifecycle总表、real adapter与terminal seal尚未启动。

## C1R9 decision 与 residual risk

assigned-signal stage必须保持单一权威unknown writer：

1. child可以写attempt和adapter-call evidence；捕获 `AssignedSignal` 后必须终止/reap其adapter worker并将信号向上重新抛出，但不得写stage result或derived unknown。
2. parent controller等待wrapper与owned child完整reap，验证signal/exit/trap/cleanup identity、result持续absent和无残留process后，才以exclusive no-follow方式写distinct `-attempted-result-unknown.json`。
3. watchdog并非assigned signal；其既有child-produced `...-result.json`/`outcome=attempted_result_unknown`可保留，但不能生成controller derived artifact。两类artifact不得共享writer、path或被互相解释。
4. signal case出现任何child result（unknown、returned success或raised failure）、controller写result path、child写derived path、result+derived、两个derived，或在controller write/finalizer/terminal audit后出现result，均fail closed。

controller-derived unknown继续不是result、success或zero proof；child/watchdog unknown也不得计success或zero。风险仅在外置lifecycle harness，未触及production或科学合同。secrets、`.env`、credential、production import、hostname、network、device、camera、Ray、strip、real cleanup、Z0、lineage、E2、formal、public analyzer、Git均为 `0`。不需要 Advisor。

## Exact next stop

C1R9任一single-writer、ordering、late-result rejection、existing owner、matrix、old-root replay、seal或zero budget失败即保留首次证据并停 Planner；全部通过也只停 Planner验收，不能自动进入真实Z0。
