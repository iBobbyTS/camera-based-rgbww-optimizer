# Planner Review：P7-TD-B-Z0-REAL-R1-C1 contract parser correction

审查日期：2026-07-26

## 审查范围

审查 active `P7-TD-B-Z0-REAL-R1-C1` 与 fresh root：

`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-e2-r1-z0-real-r1-c1/20260726T130000Z/`

仅执行离线证据/hash 核验；未运行 self-check、real wrapper、hostname、网络、设备、secret 内容、E2、formal 或 Git。

## 证据与验收

- Exact R1-C1 contract/reference/package/HEAD/archive owner 通过；parser matrix `11/11`，old REAL/old R1/unknown/prefix/package/HEAD/archive/missing/non-string/duplicate 全部 fail closed。
- strict JSON `17`；terminal/post/validation/zero handoff hash 从最终磁盘重算，mismatch/drift/residual 全闭合。
- parser-result SHA-256 `5e110b70e14ddd84705013c108f3bc15652d2dd36a32d7966d9ffe1b8dc2a8b1`；validation SHA `9b9b41da127b56cfe8a6824a3b5d5d4570c69f0e9b492a59d2b4ee12995b263e`；terminal SHA `d9ce2e70a17b4dce4682a8fcb1ce4d16053f8488961ad539407accefbdfcd22a`。
- package/driver/parser=`1/1/1`；self-check、real wrapper、hostname/network/device/secret/camera/Ray/nonzero/E2/formal/Git/retry/rerun=`0`；旧 roots 无漂移。

## Planner 决策

**接受 R1-C1，关闭 `REV-Z0-REAL-R1-CONTRACT-PARSER-024`。** 这只证明 R1 contract parser，不是实际设备可达性证据。

## 精确下一分支

`P7-TD-B-Z0-REAL-R1_BOUNDED_ZERO_ONLY_REACHABILITY`

下一 active PLAN 重新释放唯一 bounded real R1：self-check 一次、wrapper 一次、五个 zero-only stages、exact hostname/identity/generation/all-zero；无 retry/IP fallback/standalone probe，失败后 cleanup 并停；E2/formal、相机/Ray、非零输出继续锁定。

维护性判断：R1-C1 仅修复 exact contract parser，未增加生产路径；下一步为既有 bounded real gate 重放，无需架构重构。
