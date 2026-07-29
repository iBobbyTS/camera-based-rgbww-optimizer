# P7-TD-B Z0-R2-C1R1 首门失败验收归档

**归档时间：** 2026-07-25 16:22 MDT

**Reference task ID：** REF-P7-01

**Reviewed PLAN contract：** P7-TD-B-Z0-R2-C1R1

**Reviewed PLAN SHA-256：** 67ede53eb7eea85d3a957532231911e083b9b80b86260c5b40c0adb1238a3ebf

**Planner decision：** `accepted_hard_fail_behavior; rejected_completion; minimal_offline_correction_required`

**Exact next branch：** P7-TD-B-Z0-R2-C1R2，仅修正 secrets identity gate 与 launcher readonly variable；随后从全新 root 运行唯一离线 package。

## Reviewed scope 与执行方法

Executor按 PLAN 创建唯一 fresh root：

`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-e2-r1-z0-r2-c1r1-offline/20260725T221521Z/`

它冻结 current HEAD 与三份 executable source，以 no-follow binary copy 生成 canonical wrapper，完成 Python compile-only、`zsh -n`、source regular/non-symlink 与 accepted C2 evidence-tree planned-symlink 分类，然后启动 package driver 一次。driver 在任何 matrix 前 fail closed，未重跑。

## Evidence

- `pre-device-failure.json`：bytes 1912，SHA-256 `a79bbd20d100eac44db101a2055740ff0c229d5385d9ee249626fa29196c2c1e`。
- `validation-summary.json`：bytes 632，SHA-256 `6275bf4922c5e7e4538fa64ef6c47dc85ad225ed662e73f2f105bc74c05a139e`。
- `source/harness.py`：bytes 76954，SHA-256 `91d2062750d31e0eab43488e29db9567763d73003de699e5999ea5b72059dd94`。
- `source/run_wrapper.zsh`：bytes 1671，SHA-256 `890caf867a4f5630c52bd59b8c7d078daf0f59cd75dfc7b32c79879fe93354e6`。
- `source/real_adapter.py`：bytes 4240，SHA-256 `c2bc28683a1e789f1945164471f6693f48c79dd3c6dcdb1b7e36d1f0e37fc186`。
- EXECUTION_RESULT review snapshot SHA-256：`a5f730b3491b21731b4a2aee1e9ea4347b750dc696f1913858845fdbf61a13a7`。

## Validation quality 与 findings

已通过：HEAD/index freeze、canonical wrapper exact byte identity、三份 source regular/non-symlink、Python compile-only、wrapper `zsh -n`、accepted C2 tree no-follow classification、exact 两个 planned-negative symlink。

首次失败为 `ValueError: secrets path not tracked`。live `firmware/esphome/secrets.yaml` 是 regular、mode `0644`、bytes `296`，但属于 gitignored/untracked；harness错误地把“既有冻结 manifest identity + lstat identity”收紧为“必须有 Git index entry”。PLAN 未授权该要求。secrets 内容 open/hash/copy 均为 0。

driver失败后外层 launcher 又写入 zsh readonly/special parameter `status`。它未启动第二次 driver，故不改变 Python first-failure 结论，但必须在下一包改用普通退出码变量。

所有 evidence-policy、wrapper-copy、source-hygiene、identity、lifecycle 与 real-adapter matrices 均尚未启动；`REV-Z0-R2-EVIDENCE-TREE-005`、`REV-Z0-R2-WRAPPER-BYTE-COPY-006` 均未关闭。

## Safety、preservation 与 residual risk

`.env`/credential/secrets contents、production import、hostname、network、device、camera、Ray、strip、Z0、lineage、E2、formal 均为 0。repository source/test/docs/skill/wrapper edits、stage、commit均为 0；HEAD/index 与无关工作保持。

残余风险严格局限于两个外置离线 orchestration defect。下一包不得修改 production/scientific owner，不得重跑该旧 root，也不得以 corrective package 解锁真实 Z0 或后续阶段。
