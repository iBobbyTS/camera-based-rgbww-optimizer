# P7 qualification-evidence adapter C1-R1 review

**Review 时间：** 2026-07-26

**Reviewed PLAN SHA-256：** `52276d62ec8fe28a2585dfe7f234a3383b915f93021e659a1b98a0cc7beb84cf`

**Reference task：** `REF-P7-04`

**Decision：** `accepted_one_offline_evidence_run_unlocked`

## 1. Commit and implementation evidence

Commit `1e3b107b8fbfe97bae5624ef638c4883a0faee1d`，parent
`52a7168cd2510e9730e30101fc8fbf6f6d8153c1`，subject
`fix(p7): add evidence-only lineage qualification adapter`。Binary diff SHA-256
`3419e9d21e9bab8d7caad412ba32b4d140e991402f044300be7c1f7e8095e50d`，精确仅三 paths：

```text
src/camera_based_rgbww_optimizer/optimization/measure_p7_thermal_diagnostics.py
src/camera_based_rgbww_optimizer/optimization/p7_thermal_diagnostics.py
tests/test_p7_thermal_diagnostics.py
```

Final file hashes 与 §108 一致：measure `ef1a1a42...8272`、lineage `2f4d37c1...a26e`、tests
`3f753743...097f`；cached index 为空，三文件相对 HEAD 无 diff。

## 2. Adapter boundary acceptance

Adapter 精确绑定 C3-R1 path/mode/bytes/hash/schema/status，并验证 owner/current、canonical successor、ancestry、
17 inputs、13 retained artifacts、57 sorted changes、7/7 successor、5/5 overlap、empty mismatch/prohibited 和全零
side-effect budgets。Frozen C3 v1 不 fallback。

新 CLI `--prepare-lineage-qualification-evidence` 与 release mode mutually exclusive；evidence path 要求 fresh、
regular、non-symlink。Existing release writer 未修改且不被 evidence mode 调用；release/formal/backend/run/setup spies
全部为 0。

Fake evidence：
`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-qualification-evidence-adapter-c1-r1/20260726T100121Z/fake-evidence/qualification-evidence.json`，
bytes `5212`，SHA-256 `16658e497fab1246deb88a3d75dbc5c3edf311c28a49624de22a8ca79fce504c`。
独立解析确认 schema/status exact、17 references、side-effect budgets 全零，且不含
`production_release_usable`、setup-lineage-release、resolved formal plan、device authorization、readiness 或 consumer
claim。

## 3. Validation and safety

Adapter focused/postcommit `2/2`、TD-B `77/77`、public `26/26`、cleanup `127/127`、full `573/573`、compileall、
wrapper `23/23`、negative scan、diff check、CodeGraph 均通过；Planner 独立 focused `2/2` 通过。

Fake evidence writes 1、commit 1；qualification execution、release generation/consumption、device/network/live/formal
全部为 0。Human“暂时不得启动灯、相机或任何设备测试”继续冻结。

## 4. Exact next branch

允许下一唯一包 `P7-TD-B-RAY-PUBLIC-DEFAULT-LINEAGE-EVIDENCE-QUALIFICATION-R1`：只运行一次真实但纯离线的
evidence-only CLI invocation，输入严格为 C3-R1 exact artifact，只生成 qualification evidence。不得调用 release mode、
生成/消费 release、重试、probe、zero-only、Ray、strip、camera、formal 或设备/live。

本 review 使用 FULL SHA-256 `cc9ea41f8acabee34c247b7855eee1dbaeadc9d6811f72727438c3ba3a7af17f`，FULL 只读。

维护性判断：evidence validation/serialization 分属既有 lineage/measure owner，release writer 保持独立；测试覆盖
release isolation 与输入 drift，无需重构。
