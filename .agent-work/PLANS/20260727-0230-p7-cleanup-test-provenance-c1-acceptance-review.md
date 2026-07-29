# Planner 验收归档：REF-P7-04 CLEANUP-TEST-PROVENANCE-C1

**审查日期：** 2026-07-27 02:30

## 证据与决定

- commit `a87b09fc4a701a76e5214d6ff6d3a4e3de090521` 仅修改 classifier 与 TD-B
  tests 两个文件；cleanup-test manifest SHA
  `753f00f15a9c40dd0e3a0c34773f063a2cd44605d7c1f5507f375d87f56ea0d0`。
- targeted `2/2`、isolated cleanup `6/6`、TD-B `73/73`、control/cleanup `59/59`、
  full `563/563`；post-commit targeted+isolated `8/8`、TD-B `73/73`。
- compileall、wrappers、CodeGraph、`git diff --check` 均通过；无额外 paths、filename
  allowlist 或 production behavior drift。
- qualification/replay/candidate/release/device/network/.env/setup/formal/camera/Ray 均为 `0`。

接受两测试 path 的 exact provenance、commit 与验证结果。当前 clean HEAD、AGENTS policy
freeze、十 workflow paths manifest 和两 cleanup-test paths manifest 均已独立接受；发布唯一
一次纯离线 lineage qualification。成功只生成待 Planner 验收的 release，不授权 formal。

