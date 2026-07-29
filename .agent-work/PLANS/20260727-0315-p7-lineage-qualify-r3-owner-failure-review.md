# Planner 验收归档：REF-P7-04 LINEAGE-QUALIFY-R3 legacy owner failure

**审查日期：** 2026-07-27 03:15

## 证据与决定

- PLAN 错将历史 `p7_td_b_setup_lineage_release_v2` 作为 legacy input：
  `/Volumes/4T/temp/rgbww-optimizer/p7-td-b-lineage-release/lineage-release-fa6c95d-20260724-180618/setup-lineage-release.json`，
  SHA `1d3fffd82b66dcbca033a6d47bf13af4bbf98f10e9e544f308f4959047532529`。
- production qualifier 的 frozen legacy owner 是
  `/Volumes/4T/temp/rgbww-optimizer/p7-thermal-diagnostics/p7-td-b-canon-r2-setup-20260723-042002/setup-release.json`，
  schema `p7_td_b_exposure_setup_release_v1`。因此 owner gate 正确 fail closed。
- package/qualification attempts=`1/1`；run root 未创建；replay/candidate/deep manifest/
  release=`0`。57-path ledger 只读完成，三 manifests 仅 owner/schema/hash 预检，不能报 pass。
- device/network/.env/setup/formal/camera/Ray/Git 均为 `0`；未换路径重试。

接受首 owner failure，不接受 qualification。GUIDE 已明确原始 setup-release v1 是 lineage
qualification 的 immutable legacy source，而 v2 lineage release 是 qualification 输出/历史派生
证据；无需 Advisor。下一包只离线纠正 owner/schema 与三 manifest binding，不能执行 qualification。

