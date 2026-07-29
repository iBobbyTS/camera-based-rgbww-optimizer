# Planner Review：P7-TD-B-Z0-REAL-R2 watchdog unknown hard failure

审查日期：2026-07-26

## 审查范围

审查 active `P7-TD-B-Z0-REAL-R2` 与 fresh root：

`/Volumes/4T/temp/rgbww-optimizer/p7-td-b-e2-r1-z0-real-r2/20260726T160000Z/`

只读验收；未重试、未运行 E2/formal、未发送非零输出或执行其他设备操作。

## 证据与验收

- Candidate controller SHA `98849221977908e96a3ff042c69a8fce8e306013ceb4a33f543a14ce079c3509` byte-exact；pre-device source self-check `11/11` pass。
- 唯一 wrapper 使用 exact `bedroom-rgbww-strip.local:6053`；五 stages均落盘attempt/call和六events，production identity/import/secret-load totals均`5/5`。
- 五 stages全部在20秒watchdog后成为`attempted_result_unknown`，worker exit `-15`；没有任何identity/MAC/state/generation/all-zero readback。
- Python finally、child final、shell trap、independent finalizer均被尝试，但五条cleanup结果仍为unknown；后续cleanup没有覆盖首失败。
- attempt/call/production=`5/5/5`，wrapper/finalizer exits=`1/1`，retry/IP fallback/standalone probe=`0`，owned residual process=`0`，terminal mismatch=`[]`。
- driver SHA `f9330e5286dbf02ce3a3fc66d1ef9126a925f8a85af3d63d5478794bb89f2ceb`；terminal SHA `86e0187dd7b5ef9f2ee0aaf8e99deb620a2be1b58cd0197450e030606f73b4fb`；validation SHA `82f82874ddb5ed15140b020ce01180eab48b564ae3683c214b85f5c9fe961a6a`；pre-device pass SHA `037045c0b31c0db2e8e66702765d34a0bb52d00b1be822823bb8a92c8dc7060d`。
- nonzero/camera/Ray/E2/formal/lineage/firmware/deployment/Git=`0`。

## Planner 决策与安全状态

**拒绝 REAL-R2。不得自动重试或进入 E2/formal。** 所有真实调用结果未知，不能声明设备身份、generation或任何zero success。

安全状态冻结为：`RGBWW fixture zero/off proof = UNKNOWN`。无残留owned进程只证明runner已退出，不证明灯带物理全零。

冻结 findings：

1. `REV-Z0-REAL-R2-WATCHDOG-026` — exact production verified call连续五次超过20秒并被SIGTERM，失败位置在真实设备调用边界；需Human确认本地设备供电/网络/hostname状态后才能决定是否另发一次fresh gate。
2. `REV-Z0-REAL-R2-ZERO-UNKNOWN-027` — 五条cleanup均attempted-result-unknown，缺少identity/state/generation/all-zero readback；在Human物理确认前必须按可能未全零处理。

## 精确下一分支

`HUMAN_LOCAL_LAB_REACHABILITY_AND_ZERO_STATE_CHECK_STOP`

这是不可执行停止点，不授权Executor命令、probe、retry或device call。Human需：

1. 物理观察RGBWW灯带是否完全熄灭；若发光或无法确认，使用Human维护的物理电源开关/断电方式使其安全断电，并报告结果。
2. 确认ESPHome controller已供电、接入预期本地Wi-Fi/LAN，且在router/ESPHome dashboard/Home Assistant等Human可见界面中显示在线或明确离线。
3. 确认本地设备名仍为`bedroom-rgbww-strip`，预期MAC仍为`E0:8C:FE:63:C9:40`；报告是否能解析/发现`bedroom-rgbww-strip.local`，无需上传firmware或改网络配置。
4. 将上述观察结果明确回复Orchestrator。Human未确认前，Planner不得发布新的real gate。

维护性判断：source/runner/cleanup边界稳定，失败位于真实设备连接调用；此时继续改代码或放宽watchdog会掩盖环境状态，应先由Human确认本地lab安全与可达性。
