# Planner 验收归档：REF-P7-04 LINEAGE-QUALIFY-R2

**审查日期：** 2026-07-26 23:35

## 冻结结果

- focused implementation commit：`6c42c6eafd51b441ab911b13115c5bceae2a39d9`，仅修改
  `p7_thermal_diagnostics.py` 与 `test_p7_thermal_diagnostics.py`；focused TD-B `71/71`。
- full suite `556/561`；五个 cleanup/complete tests 独立重放 `0/5`：chart analyzer `1`、
  raw observer `2`、raw shutter `2`。因此不能把该 package 作为完整验证通过。
- 唯一 replay/candidate/qualification=`1/1/1`；release=`0`。AGENTS exact policy entry 已接受，
  qualification 随后因仍有 10 个 prohibited paths 抛出 PermissionError。
- device/network/setup/formal/camera/Ray/strip/public analyzer/capture/CR3/NPY/retry 均为 `0`。

## 十个冻结 paths

```text
docs/engineering/p7-td-b-contract-history.md
docs/local-lab-connection-boundary.md
src/camera_based_rgbww_optimizer/control/camera_remote.py
src/camera_based_rgbww_optimizer/control/esphome.py
src/camera_based_rgbww_optimizer/control/local_lab_context.py
src/camera_based_rgbww_optimizer/control/ray120c.py
tests/test_all_off.py
tests/test_local_lab_context.py
tests/test_project_context_docs.py
tests/test_ray120c.py
```

## 决定

拒绝 release qualification 结果，但保留 commit 与 focused 证据。十个 paths 均来自 Human
明确要求优先修改代码/文档以减少网络安全误判后形成的 `3f8fb5c` workflow commit，具有明确
Human/workflow provenance，不需要 Advisor 决定科学方向，也无需回退 checkpoint。

其中 docs/tests 可精确分类为 bounded validation/documentation；camera remote、ESPHome 与
local context 的变更仅为 CLI local-lab context/测试入口；Ray 变更为 Human-directed credential
boundary，移除内置 secret 并要求显式环境输入。它不改变有凭据时的 Ray command payload，
但当前五个 cleanup tests 未注入 test-owned credential，必须先离线修复并证明行为等价。
在该 correction 与 exact path manifest 被 Planner 接受前，不得重试 qualification。

