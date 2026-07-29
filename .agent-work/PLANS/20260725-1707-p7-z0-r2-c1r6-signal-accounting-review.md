# P7-TD-B Z0-R2-C1R6 lifecycle signal accounting 验收归档

**归档时间：** 2026-07-25 17:07 MDT

**Reference task ID：** REF-P7-01

**Reviewed PLAN contract：** P7-TD-B-Z0-R2-C1R6

**Reviewed PLAN SHA-256：** e3530eee46516d430fecae95f6c7e056ab8915c288ffd2e2aac9f8d47e68c1d2

**Planner decision：** `accepted_historical_fifo_first_five_and_adapter; rejected_four_signal_accounting_cases; c1r7_required`

**Exact next branch：** P7-TD-B-Z0-R2-C1R7；只为可证明attempt-before-signal、signal-before-result、child-terminated-without-result的assigned stage生成immutable `attempted_result_unknown`，不得计为成功或伪造result。

## Reviewed scope 与方法

C1R6 fresh root：

`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-e2-r1-z0-r2-c1r6-offline/20260725T230033Z/`

Executor冻结C1R5 artifacts，实施exact historical FIFO lstat-only policy并通过15-case policy matrix；完成cases bootstrap、seal owner与所有preflight后运行driver一次。前五矩阵、real-adapter与14个lifecycle cases通过；四个signal cases因primary result缺失且未归类unknown而失败。未修改或重跑。

## Evidence 与 accepted partial validation

- `historical-fifo-policy-matrix.json`：SHA-256 `e45a7564b07775927310656b6ad1bcefbfc37220f8ee96fc6f14e96b14cb1633`；`15/15`。
- `lifecycle-matrix.json`：bytes `121179`，SHA-256 `c0f8ed7bf6b85082e1f343140723d1b9114d27c54047e3cfed0d4b8b9fce3c0c`；`14/18`。
- `lifecycle-first-failure-audit.json`：bytes `1577`，SHA-256 `ef60ea8ac24986f9a62b075ed538f63e5b345b31d44e4f807fb0462aeedf3ef4`。
- `real-adapter-contract-matrix.json`：SHA-256 `2c7865a315b30117347bc9ebe9762461db2464c8983d9b2e94fe17af9637289f`；`12/12`。
- `validation-summary.json`：bytes `796`，SHA-256 `f45b5e6dde10ee6ff49cc851e0f62391ce99abfa0f1347cd59e917b687087f6d`。
- C1R6 harness：bytes `88326`，SHA-256 `310809b1314431888ebe96d5e7d89e50cec3ee8733e4ea87bbe564c706ae0856`。

接受结果：historical FIFO `15/15`，前五required matrices `47/47`，real adapter `12/12`；C1R3 FIFO before/after/replay exact，所有FIFO content/mutation counters为0。package JSON `494/494` strict parse。signal exit、wrapper trap与后续cleanup证据正确。

## Finding 与 residual risk

失败case exact为 `08-sigint`、`09-sigterm`、`10-sighup`、`12-signal-precedence`。四者primary attempt已atomic落盘，controller在delayed primary result写入前发送signal并终止child；result缺失。现validator将其同时报为missing artifact与assigned multiplicity，而没有使用既有安全语义 `attempted_result_unknown`。

C1R7必须保留primary result缺失这一事实，以派生artifact显式记录“attempted but result unknown”。unknown不是returned success、不是zero-state proof、不是补造result；case之所以可通过只因expected signal fail-closed、exit/trap/cleanup/finalizer均满足各自oracle。attempt/result同时存在、无法证明signal时序、child未终止或signal身份不匹配必须拒绝。

terminal seal尚未启动。secrets/.env/credential、production import、hostname、network、device、camera、Ray、strip、Z0、lineage、E2、formal、Git均为0；old roots和workspace保持。
