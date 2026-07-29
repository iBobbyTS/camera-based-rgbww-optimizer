# REF-P7-BASELINE-01 / C2 validation-only commit Planner验收归档

**验收时间：** `2026-07-25T16:05:43-0600`

**被审 active PLAN SHA-256：**
`b0adb55252d5c4352b8d4f7ad62dfe6e27bf984ce7d8f409fd8eac867c00d315`

**Planner决定：** `accepted_full_560_and_exact_commit; REF-P7-BASELINE-01_complete`

**精确下一分支：** `REF-P7-01_Z0-R2-C1_OFFLINE_ENGINEERING_RESUME_ON_NEW_HEAD`

## 验收结果

Executor未编辑任何文件，只在全新unittest进程内用`bytes(range(32))`runtime生成fake Ray key并覆盖process
`AMARAN_OPENAPI_SECRET`，运行full suite一次：`560/560`、121.479s、exit `0`。未读取、比较、打印或记录Human实际环境值；focused与TD-B
module均未重跑。

Evidence root：
`/Volumes/4T/temp/rgbww-optimizer/p7-baseline-lineage-r1-c2-validation/20260725T220022Z/`

| evidence | bytes | SHA-256 |
| --- | ---: | --- |
| full stdout | 4145 | `c75ab70a29720dbf0b038a4e5bdcfa2bfb8a7ad5a93409b956fa1cf64a84883a` |
| full stderr | 3633 | `b0ecd6d2c52d003032aa09c72c162645755784587f03fcf5d80f173cfc9cc091` |
| full exit | 2 | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` |
| `EXECUTION_RESULT.md` at review | 183389 | `b17f155becd7069a1b1ec4c7ec2cf8fa7738378a139ab4580c49681c4df8519f` |

## Commit独立核验

- commit：`0387bcfa53e52ee7f99d5308886e2b7873fe49f5`；parent：
  `db85e18b9738cfbe973187671111b6460388b385`。
- subject：`test(p7): isolate lineage baseline fixtures`；body：
  `Keep TD-B lineage tests deterministic across workflow checkpoint changes.`。
- diff-tree恰好一项：`tests/test_p7_thermal_diagnostics.py`，`72 insertions / 1 deletion`。
- commit blob mode `100644`、bytes `153769`、SHA-256
  `1bca571c42f5de51a27d183b831e75f8b98c4484ecbeab5f64a491a7f480a912`；live file exact相同且相对HEAD无diff。
- HEAD exact等于commit，index为空，remaining `git diff --check`通过；PLAN/FULL/EXECUTION_RESULT与三个Planner archives保持未stage、
  未commit、未revert。
- file edits `0`；stage/commit `1/1`；network/device/credential/.env/camera/Ray/strip/nonzero/Z0/E2/capture/formal/firmware/
  deployment/push均`0`。

## 决定与后续边界

关闭`REF-P7-BASELINE-01`。Human已明确继续goal，因此可恢复`REF-P7-01`的下一项工程前置，但不能直接进入real Z0：旧Z0-R2-C1
因Human优先级而superseded，且当前HEAD、ESPHome owner与lineage状态均已前移。下一PLAN必须重新冻结current HEAD/production owner，保持
lineage release不被消费，并先用fresh offline package关闭`REV-Z0-R2-EVIDENCE-TREE-005`与
`REV-Z0-R2-WRAPPER-BYTE-COPY-006`。通过后才由Planner决定是否另发real zero-only gate。

该分支是engineering ownership correction，未改变科学方向，不需要Advisor。
