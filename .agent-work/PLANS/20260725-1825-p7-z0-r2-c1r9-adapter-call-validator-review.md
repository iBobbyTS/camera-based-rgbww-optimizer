# P7-TD-B Z0-R2-C1R9 assigned-signal adapter-call validator 验收归档

**归档时间：** 2026-07-25 18:25 MDT

**Reference task ID：** `REF-P7-01`

**Reviewed PLAN contract：** `P7-TD-B-Z0-R2-C1R9`

**Reviewed PLAN SHA-256：** `0473b5d74ebb1be9a6ff3d08f0fd9f9b3449adf33df9c74ddc1adea109145621`

**Planner decision：** `accepted_actual_signal_single_writer_watchdog_owner_dual_root_and_preflights; rejected_validator_assigned_primary_optional_call_gate; c1r10_required`

**Exact next branch：** `P7-TD-B-Z0-R2-C1R10`；只把assigned-signal primary adapter-call gate改为no-follow absent或exact regular call，并在absent分支继续完整验证attempt、controller-derived unknown、worker/wrapper reap、ordering与immutability。call若存在必须与attempt/stage/sequence exact绑定且不得包含与unknown矛盾的completion/success/zero payload；其他14个case仍严格要求001–005五个calls。

## Reviewed scope 与方法

C1R9 fresh root：

`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-e2-r1-z0-r2-c1r9-offline/20260726T001554Z/`

Executor冻结C1R8 review/source/evidence，实施assigned-signal child skip-result与parent-controller exclusive derived writer，完成preflight后启动driver一次。Planner核对 EXECUTION_RESULT 第58节、validation/failure/zero-budget、historical/signal/writer/seal matrices、全部18个case summaries、四个signal case的stage/call/derived/post-finalizer evidence以及C1R9 validator source；未运行old driver或访问设备。

## Evidence 与 accepted validation

- historical FIFO matrix `27/27`：SHA-256 `1ba7b621a7a7548b4a780381567de9e31292944e67a958420c6e389ea47931c3`。
- frozen signal eligibility `20/20`：SHA-256 `eefc723e87f8b172645dfa6d5216d4e0bab3c801ce0221b30da676858c9b809c`，与C1R8 exact。
- `unknown-writer-ordering-matrix.json`：bytes `5145`，SHA-256 `ab497f105896501c43c4d4c47cdcb8e4c442fc2a6b85d4eaa5c51eabc369134e`；`36/36`。
- seal typed delta `3/3`：SHA-256 `8713a29bb69840e4ab0702d57e93f5adc2441217a5a010785c6b163e9d7f9318`；unclassified/broad `0/0`。
- real adapter `12/12`：SHA-256 `2c7865a315b30117347bc9ebe9762461db2464c8983d9b2e94fe17af9637289f`。
- lifecycle matrix：bytes `128067`，SHA-256 `144442eb6983ca6f6db5bd6044d99eee875cf07b7c336d7890cbf9acaae57721`；`14/18`，stage reference sum `86`，只失败四个assigned-signal validator cases。
- fresh FIFO先fail closed再exact cleanup一次；historical FIFO content/mutation为0。C1R3/C1R6 before/after whole-tree manifests分别hash-exact；C1R7/C1R8未加入old-root tuple。
- `validation-summary.json`：bytes `12848`，SHA-256 `b9ad33e0def6ef6496f12dcdc95cbaf275b372cd3854f14843b45b625d2706de`。
- `first-failure-audit.json`：bytes `14455`，SHA-256 `d38f912cbf039e6faf9360de55d6559102db2702d4e37071a6f83b9074b4b87d`。
- `zero-budget-audit.json`：bytes `1890`，SHA-256 `78083d41e091cfc427008643fd72f2b4784a92050e960290eae96f33974491e3`。
- C1R9 harness：bytes `126839`，SHA-256 `ef81ad3ac635142e48e86c2e795329a897ed704ae59101449514e4a52eb417ee`；wrapper、adapter、launcher保持C1R8 byte-exact。

四个assigned-signal case实际均为5 attempts、4 child results、1 controller-derived、0 primary child result、4 adapter calls；primary result在signal前、reap后、derived后、finalizer后和validation时均no-follow absent，derived immutable，adapter worker与wrapper/child均reaped，owned residual process 0。四derived SHA-256分别：

- `08-sigint`：`0714a9bcdcf1fd8020ebf0ceed08c2161d1ae20d24d3538cb8e8b7588476c1e5`；
- `09-sigterm`：`3bd31b2a443911dfba8d7b745f69c387478577e0d87e6595765a87433b319a01`；
- `10-sighup`：`065f13447593f6c0f5da2041858138e795d51090936454b0151c538b146f36b9`；
- `12-signal-precedence`：`ee645321acde0ca851e96dfff9a29722cbbef90e009963bde7c79164a12382d4`。

`07-watchdog-unknown`实际5 attempts、5 child results、0 controller-derived并pass；primary result SHA-256 `766354284f7948d344c41dae3a21b463ee636205bdd27bde53d199aaeaed67fe`，`kind=result`、`outcome=attempted_result_unknown`、`response=null`。前五required matrices `47/47`。package JSON `514/514` strict parse；fresh package/driver/rerun=`1/1/0`，stdout/stderr均empty，index为空。

## Finding 与根因

assigned signal允许在primary attempt与owned child identity冻结后立即注入。adapter worker可能在写 `adapter-calls/001-primary-strip-zero.json` 前被终止并reap；C1R9四个signal case均观察到该合法顺序，所以call集合exact为002–005。

冻结validator仍先执行：attempt缺失或call缺失即记录 `missing artifact` 并 `continue`。因此它没有进入同stage的derived分支，随后固定要求10 stage files + 5 call files，又产生multiplicity、derived accounting和signal accounting错误。实际derived不是缺失或不合格；validator只是被旧call prerequisite短路。

该失败不是single writer、late result、watchdog、signal/cleanup、adapter或设备失败。terminal seal尚未启动，但old replay、strict JSON与zero budgets均保持。

## C1R10 decision 与 residual risk

assigned primary call必须建模为二态：

1. `absent`：exact path no-follow缺失；不得把symlink、directory、FIFO或其他non-regular伪装成缺失。validator仍必须读取并完整验证attempt与controller-derived，不得continue。
2. `present_exact`：ordinary non-symlink strict JSON；schema/sequence/stage、attempt existed-before-call、attempt path/hash全部exact；不得包含response、outcome、generation、success或zero proof。它表示worker已开始写call evidence，不表示结果已知，可与合法controller-derived并存。

assigned case的mandatory calls始终为002–005；001只能是上述absent或exact。按exact filename集合校验，不得仅接受count 4/5。其他14个cases，包括watchdog，仍必须exact拥有001–005五个ordinary call artifacts；任何缺失、额外、重复、wrong stage/sequence/path/hash均fail closed。

无需修改signal injection、writer、cleanup、historical、seal或production owner；无需Advisor。secrets、`.env`、credential、hostname、network、device、camera、Ray、strip、real cleanup、Z0、lineage、E2、formal、public analyzer、Git均为0。

## Exact next stop

C1R10任一 call state/cardinality、derived continuation、其他14case strictness、existing owner、matrix、old replay、seal或zero budget失败即保留首次证据并停Planner；全部通过也只停Planner验收，不能自动进入真实Z0。
