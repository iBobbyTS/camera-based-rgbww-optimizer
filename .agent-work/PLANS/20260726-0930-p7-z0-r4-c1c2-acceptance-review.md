# Planner Review：P7-TD-B-Z0-R4-C1C2 full offline replay gate

审查日期：2026-07-26

## 审查范围

审查 active `P7-TD-B-Z0-R4-C1C2` 与 fresh root：

`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-e2-r1-z0-r4-c1c2/20260726T090000Z/`

仅执行离线证据/hash 核验；未访问设备、hostname、网络、`.env` secret 内容、real wrapper、E2、formal 或 Git。

## 证据与验收

- C1C2 contract/archive/HEAD parser通过；C1A/C1B/C1C1A replay无漂移。
- C5 canonical terminal seal `322/322`，完整 `device/inode/mode/path/bytes/sha256` 比较，mismatch=`[]`。
- event replay（success六事件、失败合法prefix、五负例）、failure-seal `7/7`、evidence-hash `5/5`、typed path `20/20` 全部通过。
- strict JSON `14`；terminal/post/zero mismatch/drift/residual 全部闭合。
- validation SHA-256 `c49a74ed4493b658dbb947638a7699ebc295720139d7abe5e4b69ffeb2d793a6`；terminal SHA-256 `86591fd46b7c4b7b066b9bbf82c8448cdb3b340ca0b513b7bcc7f2f509e7f0a8`；driver SHA-256 `217400f4df74be801d119c4ba0fab0e5b32c69d199ee50f0f2997556d20946ae`。
- package/driver/C1A/C1B/C1C1A/C5/event/seal/hash/path runs=`1/1/1/1/1/1/1/1/1`；real wrapper、hostname、network、device、`.env`、E2、formal、Git、retry/rerun=`0`；残留进程=`0`。

## Planner 决策

**接受 C1C2。** 所有 R4 离线前置合同已闭合；这不等于真实设备可达性或 zero stage 成功。

## 精确下一分支

`P7-TD-B-Z0-R4-REAL-Z0_ZERO_ONLY_REACHABILITY`

下一 active PLAN 是唯一 bounded real Z0：先一次 strict no-device self-check，通过后一次 wrapper、五个具名 zero-only stages；exact hostname/port、exact identity/MAC/state/generation/all-zero readback；无 retry、IP fallback、standalone probe，失败即停止并完成可执行 cleanup。E2/formal、相机/Ray、非零输出继续锁定。

维护性判断：C1C2 仅完成既有离线 owner 的完整 replay，未新增生产抽象；下一步为单一 bounded real gate，无需架构重构。
