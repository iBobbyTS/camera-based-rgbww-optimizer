# P7-TD-B Z0-R2-C1R5 historical negative FIFO 验收归档

**归档时间：** 2026-07-25 16:56 MDT

**Reference task ID：** REF-P7-01

**Reviewed PLAN contract：** P7-TD-B-Z0-R2-C1R5

**Reviewed PLAN SHA-256：** 2f98fb1f556f4be7d8621ba0e18f850d8cbb72e2384bcdcc9dd6b900db0f21b0

**Planner decision：** `accepted_precise_seal_owner_and_bootstrap; rejected_historical_fifo_manifest_policy; c1r6_required`

**Exact next branch：** P7-TD-B-Z0-R2-C1R6；只为exact C1R3 root中的exact historical negative FIFO path增加lstat-only manifest policy，open/read/follow均0；其他old/new roots的unsupported types继续fail closed。

## Reviewed scope 与方法

C1R5 fresh root：

`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-e2-r1-z0-r2-c1r5-offline/20260725T225045Z/`

Executor exact冻结C1R4 artifacts，保留cases bootstrap，实施精确seal owner raw-delta ledger与typed-sentinel normalization。所有pre-driver gates通过；唯一driver在构建old-root before manifests、任何新matrix前遇到C1R3保留FIFO并fail closed。未重跑。

## Evidence 与 accepted validation

- `seal-ast-delta-ledger.json`：bytes `3611`，SHA-256 `f925ee735f2b6b5cdc75c894e80291480fbbf46b722403d66ac0dcf27673c13c`。
- `pre-matrix-failure.json`：bytes `2589`，SHA-256 `56133b4eb3bcf7fff808663b03bda8297653c1f99db8dd7bccb8d54131a7a7e0`。
- `validation-summary.json`：bytes `560`，SHA-256 `2cd3e1f408a03cbd490c1a10d785009704388f61b0f1acf87a40d991523593cc`。
- C1R5 harness：bytes `82494`，SHA-256 `c2bd6ad453aa84712c0ad29e97cf770094785e36008c18bb8eac91ee876f5877`。
- cases bootstrap evidence SHA-256 `1a94e400f374cb7080c4d4a4612226189ece7e2e2a96db07639eb5678d8aa32b`；driver-start precheck SHA-256 `5510304be61f9e6480ccedefd5735fe880b189563d9167dce24af59aa62e149b`。

精确seal owner已接受：raw delta count `4`、unclassified `0`、broad/regex/all-constant normalization `0/0/0`；normalized baseline/current SHA exact。四项只为terminal schema、C1R4 old-root append、validation schema、validation contract；cases-parent count保持literal `1`。cases bootstrap亦全部通过。

## Finding、decision 与 residual risk

driver首次失败路径：C1R3 root内 `fixtures/evidence-tree/06-unsupported-fifo/tree/pipe`。该entry为C1R3 evidence-tree negative matrix生成并在验证FIFO fail-closed后保留的不可变fixture，不是C1R5新增或篡改。当前lstat为FIFO、mode `0644`、size `0`；C1R5未open/read/follow/modify。

Planner选择保留并显式记录该historical negative evidence，而不是排除整个subtree。C1R6 policy必须同时绑定frozen root identity与exact relative path/type/mode/size，使用lstat-only manifest entry；before/after/replay包含同一identity。任何额外FIFO、不同root同路径、不同类型/mode/size或new-package unsupported type继续fail closed。

driver尚未启动新matrix，terminal seal未运行。old-root driver/launcher、secrets/.env/credential、production import、hostname、network、device、camera、Ray、strip、Z0、lineage、E2、formal、Git均为0；workspace与production/scientific owner保持。
